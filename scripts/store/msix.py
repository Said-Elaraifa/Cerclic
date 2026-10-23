"""MSIX packages, written and checked without Microsoft's tools.

An MSIX package is a ZIP file with three extra files at the end:
AppxManifest.xml (what the app is), AppxBlockMap.xml (a SHA-256 for each
64 KB block of each file, which Windows checks when installing) and
[Content_Types].xml (the type of each file).

The layout follows makeappx and Microsoft's msix-packaging SDK
(AppxPackageWriter, ZipObjectWriter, DeflateStream, BlockMapWriter and
ContentTypeWriter, read as documentation): zip64 records, a data descriptor
after each file, each 64 KB block compressed on its own (full flush, so
Windows can read any block alone), file names percent-encoded as OPC parts.
`verify()` reads a package back with its own reader and checks all of it;
it also accepts the packages made by makeappx that ship with the SDK's tests.
"""
from __future__ import annotations

import base64
import hashlib
import io
import os
import re
import struct
import time
import zlib
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

BLOCK = 65536
MANIFEST = "AppxManifest.xml"
BLOCKMAP = "AppxBlockMap.xml"
CONTENT_TYPES = "[Content_Types].xml"
SIGNATURE = "AppxSignature.p7x"
CODE_INTEGRITY = "AppxMetadata/CodeIntegrity.cat"
FOOTPRINT = {MANIFEST.lower(), BLOCKMAP.lower(), CONTENT_TYPES.lower(), SIGNATURE.lower()}

NS_BLOCKMAP = "http://schemas.microsoft.com/appx/2010/blockmap"
NS_TYPES = "http://schemas.openxmlformats.org/package/2006/content-types"
TYPE_MANIFEST = "application/vnd.ms-appx.manifest+xml"
TYPE_BLOCKMAP = "application/vnd.ms-appx.blockmap+xml"

SIG_LFH, SIG_DD, SIG_CDH = 0x04034B50, 0x08074B50, 0x02014B50
SIG_Z64_EOCD, SIG_Z64_LOC, SIG_EOCD = 0x06064B50, 0x07064B50, 0x06054B50
FLAG_DESCRIPTOR = 0x0008
MAX32 = 0xFFFFFFFE

# Extension -> (content type, compressed), as makeappx chooses them.
_NONE, _NORMAL = False, True
TYPES = {
    "atom": ("application/atom+xml", _NORMAL), "appx": ("application/vnd.ms-appx", _NONE),
    "b64": ("application/base64", _NORMAL), "cab": ("application/vnd.ms-cab-compressed", _NONE),
    "doc": ("application/msword", _NORMAL), "dot": ("application/msword", _NORMAL),
    "docm": ("application/vnd.ms-word.document.macroenabled.12", _NONE),
    "docx": ("application/vnd.openxmlformats-officedocument.wordprocessingml.document", _NONE),
    "dotm": ("application/vnd.ms-word.document.macroenabled.12", _NONE),
    "dotx": ("application/vnd.openxmlformats-officedocument.wordprocessingml.document", _NONE),
    "dll": ("application/x-msdownload", _NORMAL), "dtd": ("application/xml-dtd", _NORMAL),
    "exe": ("application/x-msdownload", _NORMAL), "gz": ("application/x-gzip-compressed", _NONE),
    "java": ("application/java", _NORMAL), "json": ("application/json", _NORMAL),
    "p7s": ("application/x-pkcs7-signature", _NORMAL), "pdf": ("application/pdf", _NORMAL),
    "ps": ("application/postscript", _NORMAL),
    "potm": ("application/vnd.ms-powerpoint.template.macroenabled.12", _NONE),
    "potx": ("application/vnd.openxmlformats-officedocument.presentationml.template", _NONE),
    "ppam": ("application/vnd.ms-powerpoint.addin.macroenabled.12", _NONE),
    "ppsm": ("application/vnd.ms-powerpoint.slideshow.macroenabled.12", _NONE),
    "ppsx": ("application/vnd.openxmlformats-officedocument.presentationml.slideshow", _NONE),
    "ppt": ("application/vnd.ms-powerpoint", _NORMAL), "pot": ("application/vnd.ms-powerpoint", _NORMAL),
    "pps": ("application/vnd.ms-powerpoint", _NORMAL), "ppa": ("application/vnd.ms-powerpoint", _NORMAL),
    "pptm": ("application/vnd.ms-powerpoint.presentation.macroenabled.12", _NONE),
    "pptx": ("application/vnd.openxmlformats-officedocument.presentationml.presentation", _NONE),
    "rar": ("application/x-rar-compressed", _NONE), "rss": ("application/rss+xml", _NORMAL),
    "soap": ("application/soap+xml", _NORMAL), "tar": ("application/x-tar", _NONE),
    "xaml": ("application/xaml+xml", _NORMAL), "xap": ("application/x-silverlight-app", _NONE),
    "xbap": ("application/x-ms-xbap", _NORMAL), "xhtml": ("application/xhtml+xml", _NORMAL),
    "xlam": ("application/vnd.ms-excel.addin.macroenabled.12", _NONE),
    "xls": ("application/vnd.ms-excel", _NORMAL), "xlt": ("application/vnd.ms-excel", _NORMAL),
    "xla": ("application/vnd.ms-excel", _NORMAL),
    "xlsb": ("application/vnd.ms-excel.sheet.binary.macroEnabled.12", _NONE),
    "xlsm": ("application/vnd.ms-excel.sheet.macroEnabled.12", _NONE),
    "xlsx": ("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", _NONE),
    "xltm": ("application/vnd.ms-excel.template.macroEnabled.12", _NONE),
    "xltx": ("application/vnd.openxmlformats-officedocument.spreadsheetml.template", _NONE),
    "xsl": ("application/xslt+xml", _NORMAL), "xslt": ("application/xslt+xml", _NORMAL),
    "zip": ("application/x-zip-compressed", _NONE),
    "c": ("text/plain", _NORMAL), "cpp": ("text/plain", _NORMAL), "cs": ("text/plain", _NORMAL),
    "css": ("text/css", _NORMAL), "csv": ("text/csv", _NORMAL), "h": ("text/plain", _NORMAL),
    "htm": ("text/html", _NORMAL), "html": ("text/html", _NORMAL),
    "js": ("application/x-javascript", _NORMAL), "rtf": ("text/richtext", _NORMAL),
    "sct": ("text/scriptlet", _NORMAL), "txt": ("text/plain", _NORMAL),
    "xml": ("text/xml", _NORMAL), "xsd": ("text/xml", _NORMAL),
    "aiff": ("audio/x-aiff", _NORMAL), "au": ("audio/basic", _NORMAL),
    "m4a": ("audio/mp4", _NONE), "mid": ("audio/mid", _NORMAL), "mp3": ("audio/mpeg", _NONE),
    "smf": ("audio/mid", _NORMAL), "wav": ("audio/wav", _NORMAL), "wma": ("audio/x-ms-wma", _NONE),
    "bmp": ("image/bmp", _NORMAL), "emf": ("image/x-emf", _NORMAL), "gif": ("image/gif", _NONE),
    "ico": ("image/vnd.microsoft.icon", _NORMAL), "jpg": ("image/jpeg", _NONE),
    "jpeg": ("image/jpeg", _NONE), "png": ("image/png", _NONE), "svg": ("image/svg+xml", _NORMAL),
    "tif": ("image/tiff", _NORMAL), "tiff": ("image/tiff", _NORMAL), "wmf": ("image/x-wmf", _NORMAL),
    "avi": ("video/avi", _NONE), "mpeg": ("video/mpeg", _NONE), "mpg": ("video/mpeg", _NONE),
    "mov": ("video/quicktime", _NONE), "wmv": ("video/x-ms-wmv", _NONE),
}
DEFAULT_TYPE = ("application/octet-stream", _NORMAL)


class PackageError(ValueError):
    pass


# ----- names ---------------------------------------------------------------------------

_ENCODED = {c: "%{:02X}".format(ord(c)) for c in " !#$%&'()+,;=@[]^`{}"}
_RESERVED = set('<>:"/|?*') | {chr(i) for i in range(32)}
_DEVICES = {"con", "prn", "aux", "nul"} | {f"com{i}" for i in range(1, 10)} \
    | {f"lpt{i}" for i in range(1, 10)}


def encode_name(name: str) -> str:
    """'a b/é.png' -> 'a%20b/%C3%A9.png': the name of a part inside the ZIP."""
    out = []
    for ch in name.replace("\\", "/"):
        if ch in _ENCODED:
            out.append(_ENCODED[ch])
        elif ord(ch) > 0x7F:
            out.extend("%{:02X}".format(b) for b in ch.encode("utf-8"))
        else:
            out.append(ch)
    return "".join(out)


def decode_name(name: str) -> str:
    raw = bytearray()
    i = 0
    while i < len(name):
        if name[i] == "%":
            digits = name[i + 1:i + 3]
            if len(digits) != 2 or not all(c in "0123456789abcdefABCDEF" for c in digits):
                raise PackageError(f"nom mal encodé : {name}")
            raw.append(int(digits, 16))
            i += 3
        else:
            raw += name[i].encode("utf-8")
            i += 1
    return raw.decode("utf-8")


def check_name(name: str) -> None:
    """Refuse what Windows refuses in a package (same rules as makeappx)."""
    if not name or len(name) > 32767 or "\\" in name:
        raise PackageError(f"nom de fichier refusé : {name!r}")
    if name.startswith("/"):
        raise PackageError(f"chemin absolu refusé : {name!r}")
    segments = name.split("/")
    for seg in segments:
        low = seg.lower()
        if (not seg or len(seg) > 255 or seg[-1] in " ." or low in _DEVICES
                or low in (".", "..") or any(low.startswith(d + ".") for d in _DEVICES)
                or low.startswith("xn--")):
            raise PackageError(f"nom de fichier refusé par Windows : {name!r}")
        if any(c in _RESERVED for c in seg) or "￾" in seg or "￿" in seg:
            raise PackageError(f"caractère refusé dans : {name!r}")
    if any(s.lower() == "_rels" for s in segments[:-1]) and name.lower().endswith(".rels"):
        raise PackageError(f"nom réservé : {name!r}")
    low = name.lower()
    if low in FOOTPRINT or low.startswith("appxmetadata") \
            or low.startswith("microsoft.system.package.metadata"):
        raise PackageError(f"nom réservé à Windows : {name!r}")


def content_type(name: str) -> tuple[str, bool]:
    base = name.rsplit("/", 1)[-1]
    if "." not in base:
        return DEFAULT_TYPE
    return TYPES.get(base.rsplit(".", 1)[1].lower(), DEFAULT_TYPE)


# ----- writing ------------------------------------------------------------------------------

def _dos_time(t: float) -> tuple[int, int]:
    lt = time.localtime(t)
    year = max(1980, lt.tm_year)
    return ((lt.tm_hour << 11) | (lt.tm_min << 5) | (lt.tm_sec // 2),
            ((year - 1980) << 9) | (lt.tm_mon << 5) | lt.tm_mday)


class _ContentTypes:
    def __init__(self):
        self.defaults: dict[str, str] = {}
        self.rows: list[str] = []

    def add(self, name: str, ctype: str) -> None:
        encoded = encode_name(name)
        base = encoded.rsplit("/", 1)[-1]
        if "." in base:
            ext = base.rsplit(".", 1)[1]
            known = self.defaults.get(ext.lower())
            if known is None:
                self.defaults[ext.lower()] = ctype
                self.rows.append(f'<Default ContentType="{escape(ctype)}" '
                                 f'Extension="{escape(ext)}"/>')
                return
            if known == ctype:
                return
        self.rows.append(f'<Override ContentType="{escape(ctype)}" '
                         f'PartName="/{escape(encoded)}"/>')

    def xml(self) -> bytes:
        return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                f'<Types xmlns="{NS_TYPES}">' + "".join(self.rows) + "</Types>").encode("utf-8")


class MsixWriter:
    """Write a package: add() each file, then close() with the manifest."""

    def __init__(self, path: str, timestamp: float | None = None):
        self.path = path
        self.f = open(path, "wb")
        self.entries: list[tuple] = []     # (zip name, crc, csize, usize, offset, method)
        self.names: set[str] = set()
        self.blockmap: list[str] = []
        self.types = _ContentTypes()
        self.dos = _dos_time(timestamp if timestamp is not None else time.time())
        self.closed = False

    # -- one part
    def _write(self, name: str, stream, compress: bool, in_blockmap: bool,
               ctype: str | None) -> None:
        zname = encode_name(name) if ctype is not None else name
        if zname.lower() in self.names:
            raise PackageError(f"fichier en double : {name}")
        self.names.add(zname.lower())
        if ctype is not None:
            self.types.add(name, ctype)
        raw_name = zname.encode("utf-8")
        method = 8 if compress else 0
        offset = self.f.tell()
        tm, dt = self.dos
        lfh = struct.pack("<IHHHHHIIIHH", SIG_LFH, 45, FLAG_DESCRIPTOR, method, tm, dt,
                          0, 0, 0, len(raw_name), 0) + raw_name
        self.f.write(lfh)
        crc = 0
        usize = csize = 0
        blocks = []
        deflate = zlib.compressobj(9, zlib.DEFLATED, -15, 9) if compress else None
        while True:
            block = stream.read(BLOCK)
            if not block:
                break
            crc = zlib.crc32(block, crc)
            usize += len(block)
            if deflate is not None:
                out = deflate.compress(block) + deflate.flush(zlib.Z_FULL_FLUSH)
            else:
                out = block
            self.f.write(out)
            csize += len(out)
            blocks.append((base64.b64encode(hashlib.sha256(block).digest()).decode("ascii"),
                           len(out)))
            if len(block) < BLOCK:
                tail = stream.read(1)
                if tail:
                    raise PackageError(f"lecture interrompue : {name}")
                break
        if deflate is not None:
            end = deflate.flush(zlib.Z_FINISH)
            self.f.write(end)
            csize += len(end)
        self.f.write(struct.pack("<IIQQ", SIG_DD, crc & 0xFFFFFFFF, csize, usize))
        self.entries.append((raw_name, crc & 0xFFFFFFFF, csize, usize, offset, method))
        if in_blockmap:
            rows = [f'<File Name="{escape(name.replace("/", chr(92)))}" Size="{usize}" '
                    f'LfhSize="{len(lfh)}"']
            if blocks:
                rows[0] += ">"
                for h, size in blocks:
                    rows.append(f'<Block Hash="{h}" Size="{size}"/>' if compress
                                else f'<Block Hash="{h}"/>')
                rows.append("</File>")
            else:
                rows[0] += "/>"
            self.blockmap.append("".join(rows))

    def add(self, name: str, source) -> None:
        """name: path inside the package, with '/'. source: a file path or bytes."""
        if self.closed:
            raise PackageError("paquet déjà fermé")
        check_name(name)
        ctype, compress = content_type(name)
        if isinstance(source, (bytes, bytearray)):
            self._write(name, io.BytesIO(source), compress, True, ctype)
        else:
            with open(source, "rb") as fh:
                self._write(name, fh, compress, True, ctype)

    def close(self, manifest: bytes) -> None:
        ET.fromstring(manifest)                  # at least well-formed
        self._write(MANIFEST, io.BytesIO(manifest), True, True, TYPE_MANIFEST)
        blockmap = ('<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
                    f'<BlockMap xmlns="{NS_BLOCKMAP}" '
                    'HashMethod="http://www.w3.org/2001/04/xmlenc#sha256">'
                    + "".join(self.blockmap) + "</BlockMap>").encode("utf-8")
        self._write(BLOCKMAP, io.BytesIO(blockmap), True, False, TYPE_BLOCKMAP)
        self._write(CONTENT_TYPES, io.BytesIO(self.types.xml()), True, False, None)
        cd_start = self.f.tell()
        tm, dt = self.dos
        for raw_name, crc, csize, usize, offset, method in self.entries:
            extra = b""
            fields = []
            c32, u32, o32 = csize, usize, offset
            if usize > MAX32:
                fields.append(usize)
                u32 = 0xFFFFFFFF
            if csize > MAX32:
                fields.append(csize)
                c32 = 0xFFFFFFFF
            if offset > MAX32:
                fields.append(offset)
                o32 = 0xFFFFFFFF
            if fields:
                extra = struct.pack("<HH", 1, 8 * len(fields)) + b"".join(
                    struct.pack("<Q", v) for v in fields)
            self.f.write(struct.pack("<IHHHHHHIIIHHHHHII", SIG_CDH, 45, 45, FLAG_DESCRIPTOR,
                                     method, tm, dt, crc, c32, u32, len(raw_name), len(extra),
                                     0, 0, 0, 0, o32) + raw_name + extra)
        cd_end = self.f.tell()
        n = len(self.entries)
        self.f.write(struct.pack("<IQHHIIQQQQ", SIG_Z64_EOCD, 44, 45, 45, 0, 0, n, n,
                                 cd_end - cd_start, cd_start))
        self.f.write(struct.pack("<IIQI", SIG_Z64_LOC, 0, cd_end, 1))
        self.f.write(struct.pack("<IHHHHIIH", SIG_EOCD, 0, 0, 0xFFFF, 0xFFFF,
                                 0xFFFFFFFF, 0xFFFFFFFF, 0))
        self.f.close()
        self.closed = True

    def abort(self) -> None:
        if not self.closed:
            self.f.close()
            self.closed = True
            try:
                os.remove(self.path)
            except OSError:
                pass


def pack(layout: str, out: str, timestamp: float | None = None) -> int:
    """Package the folder `layout` (with its AppxManifest.xml) into `out`.
    Returns the number of files in the package."""
    with open(os.path.join(layout, MANIFEST), "rb") as fh:
        manifest = fh.read()
    names = []
    for root, dirs, files in os.walk(layout):
        dirs.sort()
        for fname in files:
            full = os.path.join(root, fname)
            rel = os.path.relpath(full, layout).replace(os.sep, "/")
            if rel.lower() in FOOTPRINT:
                if rel.lower() == MANIFEST.lower():
                    continue
                raise PackageError(f"fichier réservé dans le dossier : {rel}")
            names.append((rel, full))
    names.sort(key=lambda x: x[0].lower())
    writer = MsixWriter(out, timestamp)
    try:
        for rel, full in names:
            writer.add(rel, full)
        writer.close(manifest)
    except BaseException:
        writer.abort()
        raise
    return len(names) + 1


# ----- checking ------------------------------------------------------------------------------

def _zip_entries(data: bytes) -> list[dict]:
    """The central directory, read through the zip64 records."""
    eocd = data.rfind(struct.pack("<I", SIG_EOCD))
    if eocd < 0 or len(data) - eocd < 22:
        raise PackageError("fin de ZIP introuvable")
    _, disk, disk_cd, n_disk, n_total, cd_size, cd_off, comment = struct.unpack_from(
        "<IHHHHIIH", data, eocd)
    if eocd + 22 + comment != len(data):
        raise PackageError("fin de ZIP mal placée")
    if (n_total, cd_size, cd_off) == (0xFFFF, 0xFFFFFFFF, 0xFFFFFFFF) or \
            data[eocd - 20:eocd - 16] == struct.pack("<I", SIG_Z64_LOC):
        loc = eocd - 20
        sig, ldisk, z64_off, ndisks = struct.unpack_from("<IIQI", data, loc)
        if sig != SIG_Z64_LOC or ndisks != 1:
            raise PackageError("localisateur zip64 incorrect")
        sig, size, made, need, d1, d2, n1, n2, cd_size, cd_off = struct.unpack_from(
            "<IQHHIIQQQQ", data, z64_off)
        if sig != SIG_Z64_EOCD or n1 != n2 or z64_off + 12 + size != loc:
            raise PackageError("fin de répertoire zip64 incorrecte")
        n_total = n2
        if cd_off + cd_size != z64_off:
            raise PackageError("répertoire central mal placé")
    elif cd_off + cd_size != eocd:
        raise PackageError("répertoire central mal placé")
    entries = []
    o = cd_off
    for _ in range(n_total):
        (sig, made, need, flags, method, tm, dt, crc, csize, usize, nlen, elen, clen,
         dstart, iattr, eattr, off) = struct.unpack_from("<IHHHHHHIIIHHHHHII", data, o)
        if sig != SIG_CDH:
            raise PackageError("répertoire central abîmé")
        name = data[o + 46:o + 46 + nlen].decode("utf-8")
        extra = data[o + 46 + nlen:o + 46 + nlen + elen]
        if 0xFFFFFFFF in (csize, usize, off):
            p = 0
            while p + 4 <= len(extra):
                tag, size = struct.unpack_from("<HH", extra, p)
                if tag == 1:
                    q = p + 4
                    if usize == 0xFFFFFFFF:
                        usize = struct.unpack_from("<Q", extra, q)[0]
                        q += 8
                    if csize == 0xFFFFFFFF:
                        csize = struct.unpack_from("<Q", extra, q)[0]
                        q += 8
                    if off == 0xFFFFFFFF:
                        off = struct.unpack_from("<Q", extra, q)[0]
                p += 4 + size
        if flags & 0x0001 or method not in (0, 8):
            raise PackageError(f"compression ou chiffrement non pris en charge : {name}")
        entries.append({"name": name, "flags": flags, "method": method, "crc": crc,
                        "csize": csize, "usize": usize, "offset": off})
        o += 46 + nlen + elen + clen
    if o != cd_off + cd_size:
        raise PackageError("taille du répertoire central incohérente")
    return entries


def _entry_data(data: bytes, e: dict) -> tuple[bytes, int]:
    o = e["offset"]
    sig, need, flags, method, tm, dt, crc, csize, usize, nlen, elen = struct.unpack_from(
        "<IHHHHHIIIHH", data, o)
    if sig != SIG_LFH:
        raise PackageError(f"en-tête local absent : {e['name']}")
    if data[o + 30:o + 30 + nlen].decode("utf-8") != e["name"] or method != e["method"]:
        raise PackageError(f"en-tête local différent du répertoire : {e['name']}")
    lfh = 30 + nlen + elen
    start = o + lfh
    payload = data[start:start + e["csize"]]
    if len(payload) != e["csize"]:
        raise PackageError(f"données tronquées : {e['name']}")
    if flags & FLAG_DESCRIPTOR:
        dd = data[start + e["csize"]:start + e["csize"] + 24]
        sig2 = struct.unpack_from("<I", dd)[0]
        if sig2 == SIG_DD:
            _, crc2, c2, u2 = struct.unpack_from("<IIQQ", dd)
            if (crc2, c2, u2) != (e["crc"], e["csize"], e["usize"]):
                # 32-bit descriptor
                _, crc2, c2, u2 = struct.unpack_from("<IIII", dd)
            if (crc2, c2, u2) != (e["crc"], e["csize"], e["usize"]):
                raise PackageError(f"descripteur de données incohérent : {e['name']}")
    elif (crc, csize, usize) != (e["crc"], e["csize"] & 0xFFFFFFFF, e["usize"] & 0xFFFFFFFF):
        raise PackageError(f"en-tête local incohérent : {e['name']}")
    return payload, lfh


def verify(path: str, check_blocks: bool = True) -> dict:
    """Read the package back and check everything Windows checks when
    installing (ZIP structure, block map, content types, names). Raises
    PackageError, else returns {"files": n, "bytes": total, "manifest": bytes}."""
    with open(path, "rb") as fh:
        data = fh.read()
    entries = _zip_entries(data)
    names = [e["name"] for e in entries]
    by_name = {e["name"]: e for e in entries}
    if len(set(n.lower() for n in names)) != len(names):
        raise PackageError("noms en double dans le paquet")
    for need in (MANIFEST, BLOCKMAP, CONTENT_TYPES):
        if need not in by_name:
            raise PackageError(f"{need} manque")
    order = [n for n in names if n not in (SIGNATURE, CODE_INTEGRITY)]
    if order[-1] != CONTENT_TYPES:
        raise PackageError("[Content_Types].xml doit être le dernier fichier")
    contents: dict[str, bytes] = {}
    lfh_sizes: dict[str, int] = {}
    total = 0
    for e in entries:
        payload, lfh = _entry_data(data, e)
        lfh_sizes[e["name"]] = lfh
        if e["method"] == 8:
            d = zlib.decompressobj(-15)
            raw = d.decompress(payload) + d.flush()
            if not d.eof or d.unused_data:
                raise PackageError(f"flux compressé incomplet : {e['name']}")
        else:
            raw = payload
        if len(raw) != e["usize"] or (zlib.crc32(raw) & 0xFFFFFFFF) != e["crc"]:
            raise PackageError(f"CRC ou taille incorrects : {e['name']}")
        contents[e["name"]] = raw
        total += len(raw)
    # block map
    try:
        bm = ET.fromstring(contents[BLOCKMAP])
    except ET.ParseError as exc:
        raise PackageError(f"AppxBlockMap.xml illisible : {exc}") from None
    if bm.tag != f"{{{NS_BLOCKMAP}}}BlockMap" or \
            bm.get("HashMethod") != "http://www.w3.org/2001/04/xmlenc#sha256":
        raise PackageError("AppxBlockMap.xml : racine inattendue")
    listed = set()
    for f in bm:
        if f.tag != f"{{{NS_BLOCKMAP}}}File":
            continue
        name = f.get("Name")
        zname = encode_name(name)
        if zname not in by_name:
            raise PackageError(f"carte des blocs : fichier absent du paquet : {name}")
        if zname in listed:
            raise PackageError(f"carte des blocs : fichier en double : {name}")
        listed.add(zname)
        e = by_name[zname]
        if int(f.get("Size")) != e["usize"]:
            raise PackageError(f"carte des blocs : taille fausse : {name}")
        if int(f.get("LfhSize")) != lfh_sizes[zname]:
            raise PackageError(f"carte des blocs : LfhSize faux : {name}")
        blocks = [b for b in f if b.tag == f"{{{NS_BLOCKMAP}}}Block"]
        raw = contents[zname]
        if len(blocks) != (len(raw) + BLOCK - 1) // BLOCK:
            raise PackageError(f"carte des blocs : nombre de blocs faux : {name}")
        if not check_blocks:
            continue
        payload, _ = _entry_data(data, e)
        pos = 0
        for i, b in enumerate(blocks):
            chunk = raw[i * BLOCK:(i + 1) * BLOCK]
            digest = base64.b64encode(hashlib.sha256(chunk).digest()).decode("ascii")
            if b.get("Hash") != digest:
                raise PackageError(f"carte des blocs : empreinte fausse : {name} bloc {i}")
            if e["method"] == 8:
                size = b.get("Size")
                if size is None:
                    raise PackageError(f"carte des blocs : taille compressée absente : {name}")
                part = payload[pos:pos + int(size)]
                d = zlib.decompressobj(-15)
                if d.decompress(part) != chunk:
                    raise PackageError(f"bloc {i} illisible seul : {name}")
                pos += int(size)
            elif b.get("Size") is not None:
                raise PackageError(f"carte des blocs : taille sur un bloc non compressé : {name}")
        if e["method"] == 8:
            d = zlib.decompressobj(-15)
            if d.decompress(payload[pos:]) != b"" or not d.eof:
                raise PackageError(f"fin du flux compressé inattendue : {name}")
    for n in names:
        if n in (BLOCKMAP, CONTENT_TYPES, SIGNATURE, CODE_INTEGRITY):
            continue                    # (the last two come with the signature)
        if n not in listed:
            raise PackageError(f"absent de la carte des blocs : {n}")
    # content types
    try:
        ct = ET.fromstring(contents[CONTENT_TYPES])
    except ET.ParseError as exc:
        raise PackageError(f"[Content_Types].xml illisible : {exc}") from None
    defaults = {}
    overrides = {}
    for el in ct:
        tag = el.tag.split("}")[-1]
        if tag == "Default":
            defaults[el.get("Extension").lower()] = el.get("ContentType")
        elif tag == "Override":
            overrides[el.get("PartName").lower()] = el.get("ContentType")
    for n in names:
        if n == CONTENT_TYPES:
            continue
        ctype = overrides.get("/" + n.lower())
        if ctype is None:
            base = n.rsplit("/", 1)[-1]
            ext = base.rsplit(".", 1)[1].lower() if "." in base else None
            ctype = defaults.get(ext)
        if ctype is None:
            raise PackageError(f"type de contenu manquant : {n}")
        if n == MANIFEST and ctype != TYPE_MANIFEST or n == BLOCKMAP and ctype != TYPE_BLOCKMAP:
            raise PackageError(f"type de contenu faux : {n}")
        decoded = decode_name(n)
        if n not in (MANIFEST, BLOCKMAP, SIGNATURE, CODE_INTEGRITY) and encode_name(decoded) != n:
            raise PackageError(f"nom mal encodé : {n}")
        if n not in (MANIFEST, BLOCKMAP, SIGNATURE, CODE_INTEGRITY):
            check_name(decoded)
    return {"files": len(entries), "bytes": total, "manifest": contents[MANIFEST],
            "names": [decode_name(n) for n in names if n != CONTENT_TYPES]}


def read_file(path: str, name: str) -> bytes:
    """One file of a package (by its name in the package)."""
    with open(path, "rb") as fh:
        data = fh.read()
    for e in _zip_entries(data):
        if e["name"] == encode_name(name) or e["name"] == name:
            payload, _ = _entry_data(data, e)
            if e["method"] == 8:
                d = zlib.decompressobj(-15)
                return d.decompress(payload) + d.flush()
            return payload
    raise KeyError(name)
