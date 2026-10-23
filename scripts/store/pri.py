"""Package Resource Index (resources.pri) for the Store package of Cerclic.

Windows picks the right logo for each place (taskbar, Start, Settings) through
this index: without it, the taskbar shows the 44 px logo enlarged on a coloured
plate instead of the unplated icon made for it. Microsoft's makepri.exe only
runs on Windows, so the index is written here.

The format is not documented by Microsoft. This follows the description and
reader of PriTools (Apache 2.0, Christoph Hausner), and the writer reproduces
byte for byte the index that makepri made for Firefox's Store package
(tests/data/mozilla-Resources.pri), the same kind of index as Cerclic's: a few
logos at scale 200 and the 256 px taskbar icon in its three forms.
"""
from __future__ import annotations

import struct
import zlib

MAGIC = b"mrm_pri2"
SECTION_END = 0xDEF5FADE
FILE_END = 0xDEFFFADE

ID_DESCRIPTOR = b"[mrm_pridescex]\0"
ID_SCHEMA = b"[mrm_hschemaex] "
ID_SCHEMA_SMALL = b"[mrm_hschema]  \0"
ID_HNAMES = b"[def_hnamesx]  \0"
ID_DECISIONS = b"[mrm_decn_info]\0"
ID_MAP = b"[mrm_res_map2_]\0"
ID_MAP_V1 = b"[mrm_res_map__]\0"
ID_DATA = b"[mrm_dataitem] \0"

# Qualifier types and the priority makepri gives them (the ones Cerclic uses).
TYPES = {"Language": 0, "Contrast": 1, "Scale": 2, "HomeRegion": 3, "TargetSize": 4,
         "LayoutDirection": 5, "Theme": 6, "AlternateForm": 7, "DXFeatureLevel": 8,
         "Configuration": 9, "DeviceFamily": 10, "Custom": 11}
TYPE_NAMES = {v: k for k, v in TYPES.items()}
PRIORITY = {"Scale": 200, "TargetSize": 300, "AlternateForm": 100}
# Score of a value when Windows has nothing to compare it with (makepri's
# defaults are scale 200 and target size 256; an alternate form is optional).
FALLBACK = {("Scale", "200"): 750, ("TargetSize", "256"): 1000}

VALUE_TYPES = ("String", "Path", "EmbeddedData", "AsciiString", "Utf8String",
               "AsciiPath", "Utf8Path")


def _align(n: int, a: int = 8) -> int:
    return (n + a - 1) // a * a


def _pad(b: bytes, a: int = 8) -> bytes:
    return b + b"\0" * (_align(len(b), a) - len(b))


# ----- checksum of the hierarchical schema (verified on makepri's files) ----------

def _crc_string(crc: int, s: str | None) -> int:
    if s is None:
        return zlib.crc32(b"\0" * 8, crc)
    lowered = "".join(c.lower() if "A" <= c <= "Z" else c for c in s)
    data = (lowered + "\0").encode("utf-16-le")
    crc = zlib.crc32(struct.pack("<i", len(data)), crc)
    return zlib.crc32(data, crc)


def schema_checksum(unique_name: str, name: str, major: int, minor: int,
                    scope_paths: list[str], item_paths: list[str]) -> int:
    """scope_paths and item_paths: full names in file order, root scope first
    (empty), separated by '/' (like 'Files/Assets/Square44x44Logo.png')."""
    crc = _crc_string(0, unique_name)
    crc = _crc_string(crc, name)
    crc = zlib.crc32(struct.pack("<HH", major, minor), crc)
    crc = zlib.crc32(struct.pack("<iii", 0, 0, 1), crc)
    crc = zlib.crc32(struct.pack("<I", len(scope_paths)), crc)
    for p in scope_paths:
        crc = _crc_string(crc, p)
    crc = zlib.crc32(struct.pack("<iii", 0, 0, 1), crc)
    crc = zlib.crc32(struct.pack("<I", len(item_paths)), crc)
    for p in item_paths:
        crc = _crc_string(crc, p)
    return crc & 0xFFFFFFFF


# ----- writing -----------------------------------------------------------------------

def _section(ident: bytes, content: bytes) -> bytes:
    content = _pad(content)
    length = 32 + len(content) + 8
    return (ident + struct.pack("<IHHII", 0, 0, 0, length, 0) + content
            + struct.pack("<II", SECTION_END, length))


class _Tree:
    """Scopes and items of the resource names, in the order makepri writes
    them: the root, then each scope's children together, sorted by name."""

    def __init__(self, item_paths: list[str]):
        root: dict = {}
        for path in item_paths:
            node = root
            parts = path.split("/")
            for part in parts[:-1]:
                node = node.setdefault(part, {})
                if not isinstance(node, dict):
                    raise ValueError(f"{path} : « {part} » est déjà une ressource")
            if parts[-1] in node:
                raise ValueError(f"ressource en double : {path}")
            node[parts[-1]] = None
        # entries: (name, parent entry, is_scope, full path with '\\', children dict)
        self.entries: list[list] = [["", 0, True, "", root]]
        self.first_child: dict[int, int] = {}
        i = 0
        while i < len(self.entries):
            name, _, is_scope, full, children = self.entries[i]
            if is_scope:
                self.first_child[i] = len(self.entries)
                for child in sorted(children, key=lambda n: (n.upper(), n)):
                    sub = children[child]
                    path = child if not full else full + "\\" + child
                    self.entries.append([child, i, sub is not None, path, sub])
            i += 1
        self.scopes = [i for i, e in enumerate(self.entries) if e[2]]
        self.items = [i for i, e in enumerate(self.entries) if not e[2]]
        self.index = {}
        for n, i in enumerate(self.scopes):
            self.index[i] = n
        for n, i in enumerate(self.items):
            self.index[i] = n

    def item_path(self, entry: int) -> str:
        return self.entries[entry][3].replace("\\", "/")


def _schema(name: str, tree: _Tree) -> tuple[bytes, int]:
    unique = f"ms-appx://{name}/"
    ascii_block = bytearray()
    uni_block = bytearray()
    records = []
    for i, (nm, parent, is_scope, full, _) in enumerate(tree.entries):
        flags = 0x10 if is_scope else 0
        if i == 0:
            offset = 0              # the root: empty name
            ascii_block += b"\0"
        elif nm.isascii():
            flags |= 0x20
            offset = len(ascii_block)
            ascii_block += nm.encode("ascii") + b"\0"
        else:
            offset = len(uni_block) // 2
            uni_block += (nm + "\0").encode("utf-16-le")
        if offset >= 1 << 20:
            raise ValueError("noms trop longs pour l'index")
        flags |= offset >> 16
        first = ord(nm[0].upper()) if nm else 0
        records.append(struct.pack("<HHHBBHH", parent, len(full), first,
                                   len(nm) if len(nm) <= 255 else 0, flags,
                                   offset & 0xFFFF, tree.index[i]))
    scope_ex = b"".join(
        struct.pack("<HHHH", e, len(tree.entries[e][4]),
                    tree.first_child[e], 0) for e in tree.scopes)
    item_table = b"".join(struct.pack("<H", e) for e in tree.items)
    names = len(tree.entries)
    body = b"".join(records) + scope_ex + item_table + bytes(uni_block) + bytes(ascii_block)
    head_len = 2 + 2 + 4 * 6
    total = _align(head_len + len(body))
    max_path = max(len(e[3]) for e in tree.entries)
    hnames = struct.pack("<HHIIIIII", max_path, 0, names, len(tree.scopes),
                         len(tree.items), len(uni_block) // 2, total,
                         len(ascii_block)) + body
    hnames = hnames + b"\0" * (total - len(hnames))
    checksum = schema_checksum(
        unique, name, 1, 0,
        [tree.item_path(e) for e in tree.scopes],
        [tree.item_path(e) for e in tree.items])
    content = (struct.pack("<HHHH", 1, len(unique) + 1, len(name) + 1, 0) + ID_HNAMES
               + struct.pack("<HHIIII", 1, 0, 0, checksum, len(tree.scopes), len(tree.items))
               + (unique + "\0").encode("utf-16-le") + (name + "\0").encode("utf-16-le")
               + struct.pack("<H", 0) + hnames)
    return content, checksum


class _Decisions:
    """Qualifiers, qualifier sets and decisions, numbered as makepri does: the
    entries it always writes first (an empty qualifier, the empty set, the
    empty decision and the neutral one), then in the order they are met.
    The index table lists the members of each set and decision in that same
    order of creation."""

    def __init__(self):
        self.distinct = [(0, 0, 0, 1, "")]     # (a, type, b, value type, value)
        self.qualifiers = [(0, 0, 0)]          # (distinct, priority, fallback)
        self.sets = [()]                       # tuples of qualifier indices
        self.set_first = [0]
        self.decisions = [(), (0,)]            # tuples of set indices
        self.index_table = [0]
        self.decision_first = [0, 0]

    def qualifier(self, qtype: str, value: str) -> int:
        value = value.upper() if qtype == "AlternateForm" else value
        key = (2, TYPES[qtype], 0, 10, value)
        if key not in self.distinct:
            self.distinct.append(key)
        d = self.distinct.index(key)
        q = (d, PRIORITY[qtype], FALLBACK.get((qtype, value), 0))
        if q not in self.qualifiers:
            self.qualifiers.append(q)
        return self.qualifiers.index(q)

    def qualifier_set(self, quals) -> int:
        idx = [self.qualifier(t, v) for t, v in quals]
        idx.sort(key=lambda q: (-self.qualifiers[q][1], q))
        key = tuple(idx)
        if key not in self.sets:
            self.sets.append(key)
            self.set_first.append(len(self.index_table) if key else 0)
            self.index_table += key
        return self.sets.index(key)

    def _rank(self, s: int):
        """Most specific first: by the priorities of the set's qualifiers, then
        the latest set first (makepri's order for Firefox's icons)."""
        pr = sorted((self.qualifiers[q][1] for q in self.sets[s]), reverse=True)
        return tuple(-p for p in pr) + (1,), -s

    def decision(self, sets: list[int]) -> tuple[int, list[int]]:
        order = sorted(sets, key=self._rank)
        key = tuple(order)
        if key not in self.decisions:
            self.decisions.append(key)
            self.decision_first.append(len(self.index_table) if key else 0)
            self.index_table += key
        return self.decisions.index(key), order

    def content(self) -> bytes:
        values = ""
        offsets = []
        for d in self.distinct:
            v = d[4] + "\0"
            at = values.find(v)
            if at < 0:
                at = len(values)
                values += v
            offsets.append(at)
        index_table = self.index_table
        dec_rows = list(zip(self.decision_first, (len(d) for d in self.decisions)))
        set_rows = list(zip(self.set_first, (len(s) for s in self.sets)))
        out = struct.pack("<HHHHHH", len(self.distinct), len(self.qualifiers),
                          len(self.sets), len(self.decisions), len(index_table),
                          len(values))
        out += b"".join(struct.pack("<HH", *r) for r in dec_rows)
        out += b"".join(struct.pack("<HH", *r) for r in set_rows)
        out += b"".join(struct.pack("<HHHH", d, p, f, 0) for d, p, f in self.qualifiers)
        out += b"".join(struct.pack("<HHHHI", a, t, b, vt, offsets[i])
                        for i, (a, t, b, vt, _) in enumerate(self.distinct))
        out += b"".join(struct.pack("<H", i) for i in index_table)
        out += values.encode("utf-16-le")
        return out


def _data_section(paths: list[str]) -> bytes:
    blob = bytearray()
    rows = []
    for p in paths:
        raw = p.encode("ascii") + b"\0"
        blob += b"\0" * (_align(len(blob)) - len(blob))
        rows.append(struct.pack("<HH", len(blob), len(raw)))
        blob += raw
    blob = _pad(bytes(blob))
    return struct.pack("<IHHI", 0, len(paths), 0, len(blob)) + b"".join(rows) + blob


def build_pri(name: str, resources: dict[str, list[tuple[tuple, str]]]) -> bytes:
    """The index for these resources.

    name: the resource map's name (the package's identity name).
    resources: {"Files/Assets/Square44x44Logo.png": [(qualifiers, path), ...]}
      qualifiers: (("TargetSize", "256"), ("AlternateForm", "unplated")) or ()
      path: the candidate file, relative to the package ('Assets\\X.scale-200.png').
    """
    for cands in resources.values():
        for _, path in cands:
            if not path.isascii():
                raise ValueError(f"nom de fichier non ASCII : {path}")
    tree = _Tree(list(resources))
    dec = _Decisions()
    # qualifiers numbered in the order makepri meets the files: by file name
    by_file = sorted((path, quals) for cands in resources.values() for quals, path in cands)
    for path, quals in by_file:
        dec.qualifier_set(quals)
    item_info = []            # (decision, candidates in order) per item index
    for e in tree.items:
        cands = resources[tree.item_path(e)]
        sets = {}
        for quals, path in cands:
            s = dec.qualifier_set(quals)
            if s in sets:
                raise ValueError(f"deux fichiers pour le même cas : {path}")
            sets[s] = path
        d, order = dec.decision(list(sets))
        item_info.append((d, [(s, sets[s]) for s in order]))
    # one data section per qualifier set that has candidates, items in order
    per_set: dict[int, list[str]] = {}
    for _, cands in item_info:
        for s, path in cands:
            per_set.setdefault(s, [])
    for _, cands in item_info:
        for s, path in cands:
            per_set[s].append(path)
    set_order = sorted(per_set)

    # section indices: decisions, descriptor, schema, map, data sections
    n_data = len(set_order)
    i_dec, i_desc, i_schema, i_map = 0, 1, 2, 3
    data_index = {s: 4 + k for k, s in enumerate(set_order)}

    schema_content, _ = _schema(name, tree)
    desc = struct.pack("<HHHHHHHHHH", 2, 0xFFFF, 0, 1, 1, 1, i_map, 0, n_data, 0)
    desc += struct.pack("<HHH", i_schema, i_dec, i_map)
    desc += b"".join(struct.pack("<H", data_index[s]) for s in set_order)

    candidates = b""
    infos = b""
    n_cand = 0
    position = {s: 0 for s in set_order}
    for d, cands in item_info:
        infos += struct.pack("<HH", d, n_cand)
        for s, path in cands:
            candidates += struct.pack("<BBHHH", 1, VALUE_TYPES.index("AsciiPath"), 0,
                                      position[s], data_index[s])
            position[s] += 1
            n_cand += 1
    n_items = len(item_info)
    rmap = struct.pack("<HHHHHHHHIIII", 0, 0, i_schema, 0, i_dec, len(VALUE_TYPES),
                       1, 1, n_items, n_cand, 0, 0)
    rmap += b"".join(struct.pack("<II", 4, t) for t in range(len(VALUE_TYPES)))
    rmap += struct.pack("<HH", 0, 0) + struct.pack("<HH", n_items, 0)
    rmap += infos + candidates

    sections = [(ID_DECISIONS, dec.content()), (ID_DESCRIPTOR, desc),
                (ID_SCHEMA, schema_content), (ID_MAP, rmap)]
    sections += [(ID_DATA, _data_section(per_set[s])) for s in set_order]
    blobs = [_section(i, c) for i, c in sections]
    toc_off = 32
    first = toc_off + 32 * len(blobs)
    toc = b""
    off = 0
    for (ident, _), blob in zip(sections, blobs):
        toc += ident + struct.pack("<HHIII", 0, 0, 0, off, len(blob))
        off += len(blob)
    total = first + off + 16
    head = MAGIC + struct.pack("<HHIIIHHI", 0, 1, total, toc_off, first, len(blobs), 0xFFFF, 0)
    return head + toc + b"".join(blobs) + struct.pack("<II", FILE_END, total) + MAGIC


# ----- reading (to check an index) -------------------------------------------------

class PriError(ValueError):
    pass


def _u16(b, o):
    return struct.unpack_from("<H", b, o)[0]


def _u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


def _wstr(b: bytes, o: int, limit: int | None = None) -> str:
    end = o
    stop = len(b) if limit is None else min(len(b), o + 2 * limit)
    while end + 1 < stop and b[end:end + 2] != b"\0\0":
        end += 2
    return b[o:end].decode("utf-16-le")


def _astr(b: bytes, o: int) -> str:
    end = b.index(b"\0", o)
    return b[o:end].decode("ascii")


def read_pri(data: bytes) -> dict:
    """Parse an index; raises PriError if anything is inconsistent.
    Returns {"name", "unique_name", "checksum", "computed_checksum",
    "resources": {item: [(qualifiers, value), ...]}, "sections": [...]}."""
    if data[:8] not in (b"mrm_pri0", b"mrm_pri1", b"mrm_pri2", b"mrm_pri3", b"mrm_prif"):
        raise PriError("en-tête PRI absent")
    if _u16(data, 8) != 0 or _u16(data, 10) != 1:
        raise PriError("en-tête inattendu")
    total, toc_off, first, count = _u32(data, 12), _u32(data, 16), _u32(data, 20), _u16(data, 24)
    if total != len(data) or _u16(data, 26) != 0xFFFF or _u32(data, 28) != 0:
        raise PriError("taille ou en-tête incohérents")
    if _u32(data, total - 16) != FILE_END or _u32(data, total - 12) != total \
            or data[total - 8:] != data[:8]:
        raise PriError("pied de fichier incorrect")
    if first != toc_off + 32 * count:
        raise PriError("table des sections mal placée")
    sections = []
    for i in range(count):
        o = toc_off + 32 * i
        ident = data[o:o + 16]
        off, length = _u32(data, o + 24), _u32(data, o + 28)
        s = first + off
        if data[s:s + 16] != ident:
            raise PriError(f"section {i} : identifiant différent de la table")
        if _u32(data, s + 24) != length or _u32(data, s + 28) != 0:
            raise PriError(f"section {i} : longueur incohérente")
        if s % 8 or length % 8:
            raise PriError(f"section {i} : non alignée")
        if _u32(data, s + length - 8) != SECTION_END or _u32(data, s + length - 4) != length:
            raise PriError(f"section {i} : fin de section incorrecte")
        sections.append((ident, data[s + 32:s + length - 8]))
    if first + sum(len(c) + 40 for _, c in sections) + 16 != total:
        raise PriError("sections et taille totale incohérentes")

    def find(ident):
        return [i for i, (d, _) in enumerate(sections) if d == ident]

    desc_i = find(ID_DESCRIPTOR)
    if len(desc_i) != 1:
        raise PriError("descripteur absent")
    d = sections[desc_i[0]][1]
    n_schema, n_dec, n_map, primary, n_files, n_data = (
        _u16(d, 6), _u16(d, 8), _u16(d, 10), _u16(d, 12), _u16(d, 14), _u16(d, 16))
    refs = [_u16(d, 20 + 2 * k) for k in range(n_schema + n_dec + n_map + n_files + n_data)]
    schema_refs = refs[:n_schema]
    map_refs = refs[n_schema + n_dec:n_schema + n_dec + n_map]
    data_refs = refs[n_schema + n_dec + n_map + n_files:]
    if primary == 0xFFFF or primary not in map_refs:
        raise PriError("carte de ressources principale absente")

    # schema
    schema = _read_schema(sections[schema_refs[0]][1], sections[schema_refs[0]][0])
    # decisions and map
    m_ident, m = sections[primary]
    if m_ident not in (ID_MAP, ID_MAP_V1):
        raise PriError("carte de ressources illisible")
    env_len, env_n, schema_sec, ref_len, dec_sec, vt_n, i2g_n, g_n = struct.unpack_from("<8H", m, 0)
    info_n, cand_n, data_len, large_len = struct.unpack_from("<4I", m, 16)
    if schema_sec not in schema_refs:
        raise PriError("la carte ne désigne pas le schéma")
    decisions = _read_decisions(sections[dec_sec][1])
    o = 32 + env_len + ref_len
    vtypes = []
    for k in range(vt_n):
        four, t = struct.unpack_from("<II", m, o + 8 * k)
        if four != 4:
            raise PriError("table des types de valeurs inattendue")
        vtypes.append(VALUE_TYPES[t])
    o += 8 * vt_n
    i2g = [struct.unpack_from("<HH", m, o + 4 * k) for k in range(i2g_n)]
    o += 4 * i2g_n
    groups = [struct.unpack_from("<HH", m, o + 4 * k) for k in range(g_n)]
    o += 4 * g_n
    infos = [struct.unpack_from("<HH", m, o + 4 * k) for k in range(info_n)]
    o += 4 * info_n
    if large_len:
        raise PriError("grandes tables non prises en charge")
    cands = []
    for k in range(cand_n):
        kind = m[o]
        if kind == 1:
            _, vt, src, item, sec = struct.unpack_from("<BBHHH", m, o)
            cands.append((vtypes[vt], src, item, sec))
        elif kind == 0:
            _, vt, length, off = struct.unpack_from("<BBHI", m, o)
            cands.append((vtypes[vt], None, length, off))
        else:
            raise PriError("candidat de type inconnu")
        o += 8
    if _align(o + data_len) != len(m):
        raise PriError("longueur de la carte incohérente")
    data_items = {}
    for k in data_refs:
        data_items[k] = _read_data(sections[k][1])
    resources = {}
    seen = set()
    for first_item, g in i2g:
        size, first_info = groups[g] if g < len(groups) else (1, g - len(groups))
        for n in range(size):
            item = first_item + n
            dec_i, first_cand = infos[first_info + n]
            sets = decisions["decisions"][dec_i]
            values = []
            for j, qs in enumerate(sets):
                vt, src, a, b = cands[first_cand + j]
                if src is None:
                    raw = m[o + b:o + b + a]
                else:
                    if src != 0:
                        raise PriError("données dans un autre fichier PRI")
                    if b not in data_items or a >= len(data_items[b]):
                        raise PriError("donnée introuvable")
                    raw = data_items[b][a]
                values.append((decisions["sets"][qs], _decode_value(vt, raw)))
            name = schema["items"][item]
            if name in seen:
                raise PriError(f"ressource décrite deux fois : {name}")
            seen.add(name)
            resources[name] = values
    return {"name": schema["name"], "unique_name": schema["unique_name"],
            "checksum": schema["checksum"], "computed_checksum": schema["computed"],
            "resources": resources, "decisions": decisions,
            "sections": [s[0].rstrip(b"\0 ").decode("ascii") for s in sections]}


def _decode_value(vt: str, raw: bytes) -> str:
    if vt in ("AsciiPath", "AsciiString"):
        return raw.rstrip(b"\0").decode("ascii")
    if vt in ("Utf8Path", "Utf8String"):
        return raw.rstrip(b"\0").decode("utf-8")
    if vt in ("Path", "String"):
        return raw.decode("utf-16-le").rstrip("\0")
    return raw.hex()


def _read_schema(c: bytes, ident: bytes) -> dict:
    if _u16(c, 0) != 1 or _u16(c, 6) != 0:
        raise PriError("schéma inattendu")
    unique_len, name_len = _u16(c, 2), _u16(c, 4)
    o = 8
    extended_names = False
    if ident == ID_SCHEMA:
        hid = c[8:24]
        if hid == ID_HNAMES:
            extended_names = True
        elif hid != b"[def_hnames]   \0":
            raise PriError("noms du schéma inconnus")
        o = 24
    major, minor, zero, checksum, n_scopes, n_items = struct.unpack_from("<HHIIII", c, o)
    o += 20
    unique = _wstr(c, o, unique_len)
    o += 2 * unique_len
    name = _wstr(c, o, name_len)
    o += 2 * name_len
    if _u16(c, o) != 0:
        raise PriError("schéma inattendu")
    o += 2
    h = o
    max_path, zero2, n_names, n_sc, n_it, uni_len, total = struct.unpack_from("<HHIIIII", c, o)
    o += 24
    ascii_len = 0
    if extended_names:
        ascii_len = _u32(c, o)
        o += 4
    if (n_sc, n_it, n_names) != (n_scopes, n_items, n_scopes + n_items):
        raise PriError("nombre de noms incohérent")
    recs = []
    for k in range(n_names):
        parent, full_len, first, nlen, flags, noff, index = struct.unpack_from("<HHHBBHH", c, o)
        recs.append((parent, full_len, flags, noff | ((flags & 0xF) << 16), index))
        o += 12
    scope_ex = [struct.unpack_from("<HHHH", c, o + 8 * k) for k in range(n_scopes)]
    o += 8 * n_scopes
    item_table = [_u16(c, o + 2 * k) for k in range(n_items)]
    o += 2 * n_items
    uni_at = o
    ascii_at = o + 2 * uni_len
    end = ascii_at + ascii_len
    if _align(end - h) != total or _align(h + total) != len(c):
        raise PriError("longueur des noms incohérente")
    names = []
    for parent, full_len, flags, noff, index in recs:
        if full_len == 0:
            names.append("")
        elif flags & 0x20:
            names.append(_astr(c, ascii_at + noff))
        else:
            names.append(_wstr(c, uni_at + 2 * noff))

    def full(e):
        parts = []
        while e != 0:
            parts.append(names[e])
            e = recs[e][0]
        return "/".join(reversed(parts))

    for e, (parent, full_len, flags, _, _) in enumerate(recs):
        if len(full(e).replace("/", "\\")) != full_len:
            raise PriError(f"longueur de chemin incohérente : {full(e)}")
    scopes = {}
    items = {}
    for e, (_, _, flags, _, index) in enumerate(recs):
        (scopes if flags & 0x10 else items)[index] = full(e)
    if sorted(scopes) != list(range(n_scopes)) or sorted(items) != list(range(n_items)):
        raise PriError("index du schéma incohérents")
    scope_order = [recs[s[0]][4] for s in scope_ex]
    item_order = [recs[e][4] for e in item_table]
    computed = schema_checksum(unique, name, major, minor,
                               [scopes[i] for i in scope_order],
                               [items[i] for i in item_order])
    return {"unique_name": unique, "name": name, "checksum": checksum,
            "computed": computed, "scopes": scopes, "items": items}


def _read_data(c: bytes) -> list[bytes]:
    zero, n_strings, n_blobs, total = struct.unpack_from("<IHHI", c, 0)
    if zero != 0:
        raise PriError("section de données inattendue")
    start = 12 + 4 * n_strings + 8 * n_blobs
    if _align(start + total) != len(c):
        raise PriError("longueur des données incohérente")
    items = []
    for k in range(n_strings):
        off, length = struct.unpack_from("<HH", c, 12 + 4 * k)
        if off + length > total:
            raise PriError("donnée hors limites")
        items.append(c[start + off:start + off + length])
    for k in range(n_blobs):
        off, length = struct.unpack_from("<II", c, 12 + 4 * n_strings + 8 * k)
        if off + length > total:
            raise PriError("donnée hors limites")
        items.append(c[start + off:start + off + length])
    return items


def _read_decisions(c: bytes) -> dict:
    n_distinct, n_quals, n_sets, n_dec, n_index, n_values = struct.unpack_from("<6H", c, 0)
    o = 12
    dec_rows = [struct.unpack_from("<HH", c, o + 4 * k) for k in range(n_dec)]
    o += 4 * n_dec
    set_rows = [struct.unpack_from("<HH", c, o + 4 * k) for k in range(n_sets)]
    o += 4 * n_sets
    quals = [struct.unpack_from("<HHHH", c, o + 8 * k) for k in range(n_quals)]
    o += 8 * n_quals
    distinct = [struct.unpack_from("<HHHHI", c, o + 12 * k) for k in range(n_distinct)]
    o += 12 * n_distinct
    index = [_u16(c, o + 2 * k) for k in range(n_index)]
    o += 2 * n_index
    if _align(o + 2 * n_values) != len(c):
        raise PriError("longueur des décisions incohérente")
    qualifiers = []
    for d, prio, fallback, zero in quals:
        a, qtype, b, vt, voff = distinct[d]
        if voff >= n_values:
            raise PriError("valeur de qualificateur hors limites")
        qualifiers.append((TYPE_NAMES.get(qtype, str(qtype)), _wstr(c, o + 2 * voff),
                           prio, fallback))
    sets = []
    for first, n in set_rows:
        sets.append(tuple((qualifiers[index[first + k]][0], qualifiers[index[first + k]][1])
                          for k in range(n)))
    decisions = []
    for first, n in dec_rows:
        decisions.append([index[first + k] for k in range(n)])
    return {"qualifiers": qualifiers, "sets": sets, "decisions": decisions}
