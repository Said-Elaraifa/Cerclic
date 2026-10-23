"""Image actions: convert, compress, resize, rotate, mirror, crop, remove
private information, assemble several pictures into one.

Every function takes a source path and returns the path it wrote, always a new
file beside the source. Results are upright (EXIF orientation applied), keep the
colour profile and EXIF data, and animations (GIF, WEBP) keep all their frames.
HEIC/HEIF photos are read through pillow-heif; AVIF is native in Pillow.
"""
from __future__ import annotations

import io
import os
from dataclasses import dataclass, field
from typing import Callable, Sequence

from PIL import Image, ImageOps, ImageSequence

from ..errors import NothingToDo, UserError
from ..paths import ext_of, output_for

# Allow very large panoramas, but still refuse absurd (malicious) sizes.
Image.MAX_IMAGE_PIXELS = 1_000_000_000

try:  # optional at import time so the tests can run without it
    import pillow_heif  # type: ignore
    pillow_heif.register_heif_opener()
    _HEIF = True
except Exception:  # pragma: no cover
    _HEIF = False

# Output formats we write: (Pillow format, canonical extension).
FORMATS = {
    "jpg": ("JPEG", ".jpg"),
    "png": ("PNG", ".png"),
    "webp": ("WEBP", ".webp"),
    "gif": ("GIF", ".gif"),
    "bmp": ("BMP", ".bmp"),
    "tiff": ("TIFF", ".tif"),
}
_EXT_FORMAT = {".jpg": "jpg", ".jpeg": "jpg", ".jfif": "jpg", ".png": "png",
               ".webp": "webp", ".gif": "gif", ".bmp": "bmp", ".tif": "tiff",
               ".tiff": "tiff"}
_ANIMATED_FORMATS = {"GIF", "WEBP", "PNG"}

DEFAULT_JPG_QUALITY = 90


@dataclass
class Picture:
    """A decoded image, upright and fully detached from its file."""
    frames: list
    durations: list = field(default_factory=list)
    loop: int = 0
    icc: bytes | None = None
    exif: bytes | None = None
    dpi: tuple | None = None
    source_format: str = ""

    @property
    def animated(self) -> bool:
        return len(self.frames) > 1

    @property
    def size(self) -> tuple[int, int]:
        return self.frames[0].size

    @property
    def has_alpha(self) -> bool:
        im = self.frames[0]
        return im.mode in ("RGBA", "LA", "PA") or (
            im.mode == "P" and "transparency" in im.info)

    def map(self, fn: Callable) -> "Picture":
        return Picture([fn(f) for f in self.frames], list(self.durations),
                       self.loop, self.icc, self.exif, self.dpi, self.source_format)

    @property
    def is_cmyk(self) -> bool:
        return self.frames[0].mode == "CMYK"

    def to_srgb(self) -> "Picture":
        """Print colours (CMYK) to screen colours, through the embedded colour
        profile when there is one, and tag the result as sRGB."""
        if not self.is_cmyk:
            return self
        frames = [_cmyk_to_srgb(f, self.icc) for f in self.frames]
        return Picture(frames, list(self.durations), self.loop, _srgb_icc(),
                       self.exif, self.dpi, self.source_format)


def load(src: str) -> Picture:
    """Read an image (all frames if animated). The file is closed on return."""
    try:
        im = Image.open(src)
    except Image.UnidentifiedImageError:
        raise UserError("Image illisible ou format non pris en charge.")
    with im:
        fmt = im.format or ""
        icc = im.info.get("icc_profile")
        dpi = im.info.get("dpi")
        n = getattr(im, "n_frames", 1) or 1
        if n > 1 and fmt in _ANIMATED_FORMATS:
            frames, durations = [], []
            for fr in ImageSequence.Iterator(im):
                durations.append(int(fr.info.get("duration", 100) or 100))
                frames.append(fr.convert("RGBA"))
            return Picture(frames, durations, int(im.info.get("loop", 0) or 0),
                           icc, None, dpi, fmt)
        im.load()
        upright = ImageOps.exif_transpose(im)  # a copy, orientation reset
        exif = None
        try:
            ex = upright.getexif()
            if len(ex):
                ex[0x0112] = 1
                exif = ex.tobytes()
        except Exception:
            exif = None
        return Picture([upright], [], 0, icc, exif, dpi, fmt)


def oriented_size(src: str) -> tuple[int, int]:
    """Size of the image once upright, read from the header only (fast)."""
    with Image.open(src) as im:
        w, h = im.size
        try:
            orient = im.getexif().get(0x0112, 1)
        except Exception:
            orient = 1
    return (h, w) if orient in (5, 6, 7, 8) else (w, h)


def image_size(src: str) -> tuple[int, int]:
    return oriented_size(src)


# ----- colour profiles --------------------------------------------------------

def _srgb_icc() -> bytes | None:
    try:
        from PIL import ImageCms
        return ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    except Exception:
        return None


def _icc_space(icc: bytes | None) -> str:
    """'RGB', 'CMYK', 'GRAY'... of a profile, '' if unknown."""
    if not icc:
        return ""
    try:
        import io as _io
        from PIL import ImageCms
        prof = ImageCms.ImageCmsProfile(_io.BytesIO(icc))
        return (prof.profile.xcolor_space or "").strip().upper()
    except Exception:
        return ""


def _cmyk_to_srgb(im: Image.Image, icc: bytes | None) -> Image.Image:
    if icc and _icc_space(icc) == "CMYK":
        try:
            import io as _io
            from PIL import ImageCms
            return ImageCms.profileToProfile(
                im, ImageCms.ImageCmsProfile(_io.BytesIO(icc)),
                ImageCms.createProfile("sRGB"), outputMode="RGB")
        except Exception:
            pass
    return im.convert("RGB")


_MODE_SPACE = {"RGB": "RGB", "RGBA": "RGB", "P": "RGB", "PA": "RGB", "CMYK": "CMYK",
               "L": "GRAY", "LA": "GRAY", "1": "GRAY", "I": "GRAY", "I;16": "GRAY"}


def _profile_for(frame: Image.Image, icc: bytes | None) -> bytes | None:
    """Keep a profile only if it matches the pixels it describes."""
    space = _icc_space(icc)
    want = _MODE_SPACE.get(frame.mode, "")
    return icc if icc and (not space or not want or space == want) else None


# ----- saving ---------------------------------------------------------------

def _to_8bit(im: Image.Image) -> Image.Image:
    if im.mode in ("I;16", "I;16B", "I;16L", "I"):
        return im.convert("I").point(lambda v: v * (1 / 256)).convert("L")
    if im.mode == "F":
        return im.convert("L")
    return im


def _flatten(im: Image.Image, bg=(255, 255, 255)) -> Image.Image:
    """Put an image with transparency onto a white background."""
    im = _to_8bit(im)
    if im.mode in ("RGBA", "LA", "PA") or (im.mode == "P" and "transparency" in im.info):
        rgba = im.convert("RGBA")
        canvas = Image.new("RGB", rgba.size, bg)
        canvas.paste(rgba, mask=rgba.getchannel("A"))
        return canvas
    if im.mode in ("RGB", "L", "CMYK"):
        return im
    return im.convert("RGB")


def _prepare(im: Image.Image, fmt: str) -> Image.Image:
    """Convert to a mode the target format accepts."""
    im = _to_8bit(im)
    alpha = im.mode in ("RGBA", "LA", "PA") or (
        im.mode == "P" and "transparency" in im.info)
    if fmt == "jpg":
        return _flatten(im)
    if fmt == "webp":
        return im.convert("RGBA" if alpha else "RGB")
    if fmt == "png":
        if im.mode in ("1", "L", "LA", "P", "RGB", "RGBA", "I"):
            return im
        return im.convert("RGBA" if alpha else "RGB")
    if fmt == "bmp":
        if im.mode in ("1", "L", "P", "RGB", "RGBA") and not (im.mode == "P" and alpha):
            return im
        return im.convert("RGBA" if alpha else "RGB")
    if fmt == "gif":
        if im.mode in ("P", "L", "RGB", "RGBA"):
            return im
        return im.convert("RGBA" if alpha else "RGB")
    if fmt == "tiff":
        if im.mode in ("1", "L", "LA", "P", "RGB", "RGBA", "CMYK", "I", "F"):
            return im
        return im.convert("RGBA" if alpha else "RGB")
    return im


def save(pic: Picture, out: str, fmt: str, quality: int | None = None,
         optimize: bool = False) -> None:
    pil_fmt, _ = FORMATS[fmt]
    if pic.is_cmyk and fmt not in ("jpg", "tiff"):
        pic = pic.to_srgb()        # PNG, WEBP, GIF, BMP have no CMYK
    frames = [_prepare(f, fmt) for f in pic.frames]
    params: dict = {}
    icc = _profile_for(frames[0], pic.icc)
    if icc and fmt in ("jpg", "png", "webp", "tiff"):
        params["icc_profile"] = icc
    if pic.exif and fmt in ("jpg", "png", "webp", "tiff"):
        params["exif"] = pic.exif
    if pic.dpi and fmt in ("jpg", "png", "tiff", "bmp"):
        try:
            params["dpi"] = tuple(float(v) for v in pic.dpi[:2])
        except Exception:
            pass
    if fmt == "jpg":
        params.update(quality=int(quality or DEFAULT_JPG_QUALITY), optimize=True,
                      progressive=True)
    elif fmt == "webp":
        params.update(quality=int(quality or DEFAULT_JPG_QUALITY), method=4)
    elif fmt == "png":
        params.update(optimize=True) if optimize else params.update(compress_level=6)
    elif fmt == "gif":
        params.update(optimize=optimize)

    animated = len(frames) > 1 and fmt in ("gif", "webp", "png")
    if animated:
        params.update(save_all=True, append_images=frames[1:],
                      duration=pic.durations or 100, loop=pic.loop)
        if fmt == "gif":
            params["disposal"] = 2
    frames[0].save(out, pil_fmt, **params)


# ----- choosing the output format ------------------------------------------

def keep_format(src: str, pic: Picture | None = None) -> tuple[str, str]:
    """(format, extension) to use when an edit keeps the file's own format.
    HEIC, HEIF and AVIF become JPG (PNG if transparent), which every app opens."""
    e = ext_of(src)
    fmt = _EXT_FORMAT.get(e)
    if fmt:
        return fmt, e if e in (".jpg", ".jpeg", ".jfif", ".tif", ".tiff") else FORMATS[fmt][1]
    if pic is not None and pic.has_alpha:
        return "png", ".png"
    return "jpg", ".jpg"


def _write(src: str, pic: Picture, tag: str, fmt: str | None = None,
           quality: int | None = None, optimize: bool = False) -> str:
    if fmt is None:
        fmt, ext = keep_format(src, pic)
    else:
        ext = FORMATS[fmt][1]
    out = output_for(src, tag, new_ext=ext)
    save(pic, out, fmt, quality=quality, optimize=optimize)
    return out


# ----- actions --------------------------------------------------------------

def convert_image(src: str, fmt: str, quality: int | None = None) -> str:
    """Convert to jpg/png/webp, written next to the source."""
    fmt = "jpg" if fmt.lower() in ("jpg", "jpeg") else fmt.lower()
    if fmt not in ("jpg", "png", "webp"):
        raise ValueError(f"unsupported target format: {fmt}")
    pic = load(src).to_srgb()
    if pic.animated and fmt != "webp":
        pic = Picture(pic.frames[:1], [], 0, pic.icc, pic.exif, pic.dpi,
                      pic.source_format)
    return _write(src, pic, fmt, fmt=fmt, quality=quality)


def to_jpg(src: str) -> str:
    return convert_image(src, "jpg")


def _quantize(im: Image.Image) -> Image.Image:
    """256-colour palette with dithering: the TinyPNG trick, keeps alpha."""
    if im.mode in ("RGBA", "LA", "PA") or (im.mode == "P" and "transparency" in im.info):
        return im.convert("RGBA").quantize(256, method=Image.Quantize.FASTOCTREE,
                                           dither=Image.Dither.FLOYDSTEINBERG)
    return im.convert("RGB").quantize(256, method=Image.Quantize.MEDIANCUT,
                                      dither=Image.Dither.FLOYDSTEINBERG)


def compress_image(src: str, quality: int = 70) -> str:
    """Lighter copy with the same dimensions. JPG and WEBP are re-encoded at
    `quality`; PNG is reduced to an optimised 256-colour palette; other formats
    become JPG. Raises NothingToDo when the result would not be smaller."""
    pic = load(src).to_srgb()
    e = ext_of(src)
    if e == ".png" and not pic.animated:
        pic = pic.map(_quantize)
        out = _write(src, pic, "compressed", fmt="png", optimize=True)
    elif e == ".webp":
        out = _write(src, pic, "compressed", fmt="webp", quality=quality)
    elif e == ".gif":
        out = _write(src, pic, "compressed", fmt="gif", optimize=True)
    else:
        if pic.animated:
            pic = Picture(pic.frames[:1], [], 0, pic.icc, pic.exif, pic.dpi,
                          pic.source_format)
        fmt = "png" if pic.has_alpha and e not in (".jpg", ".jpeg", ".jfif") else "jpg"
        if fmt == "png":
            pic = pic.map(_quantize)
        out = _write(src, pic, "compressed", fmt=fmt, quality=quality,
                     optimize=fmt == "png")
    if os.path.getsize(out) >= os.path.getsize(src):
        os.remove(out)
        raise NothingToDo("Cette image est déjà bien compressée.")
    return out


def resize_image(src: str, max_side: int | None = None,
                 percent: float | None = None, quality: int | None = None) -> str:
    """Resize by longest side (px) or by percent, keeping the aspect ratio.
    Never enlarges: an image already small enough raises NothingToDo."""
    pic = load(src)
    w, h = pic.size
    if percent:
        target = (max(1, round(w * percent / 100)), max(1, round(h * percent / 100)))
    elif max_side:
        if max(w, h) <= max_side:
            raise NothingToDo(f"L'image fait déjà {max(w, h)} px ou moins.")
        scale = max_side / max(w, h)
        target = (max(1, round(w * scale)), max(1, round(h * scale)))
    else:
        raise ValueError("resize needs max_side or percent")
    pic = pic.map(lambda f: f.resize(target, Image.Resampling.LANCZOS))
    return _write(src, pic, "resized", quality=quality)


_ROTATIONS = {90: Image.Transpose.ROTATE_270,   # clockwise
              180: Image.Transpose.ROTATE_180,
              270: Image.Transpose.ROTATE_90}   # counter-clockwise


def rotate_image(src: str, degrees: int = 90, quality: int | None = None) -> str:
    """Rotate clockwise by 90, 180 or 270 degrees."""
    deg = int(degrees) % 360
    if deg not in _ROTATIONS:
        raise ValueError("rotation must be a multiple of 90 degrees")
    op = _ROTATIONS[deg]
    pic = load(src).map(lambda f: f.transpose(op))
    return _write(src, pic, "rotated", quality=quality)


def crop_image(src: str, box: Sequence[float], quality: int | None = None) -> str:
    """Crop to box = (left, top, right, bottom) in pixels of the upright image."""
    pic = load(src)
    w, h = pic.size
    left, top, right, bottom = (int(round(float(v))) for v in box)
    left, top = max(0, left), max(0, top)
    right, bottom = min(w, right), min(h, bottom)
    if right - left < 1 or bottom - top < 1:
        raise UserError("La zone à rogner est vide.")
    if (left, top, right, bottom) == (0, 0, w, h):
        raise NothingToDo("Le cadre couvre toute l'image : rien à rogner.")
    pic = pic.map(lambda f: f.crop((left, top, right, bottom)))
    return _write(src, pic, "cropped", quality=quality)


def mirror_image(src: str, quality: int | None = None) -> str:
    """Flip left to right (a selfie the right way round)."""
    pic = load(src).map(lambda f: f.transpose(Image.Transpose.FLIP_LEFT_RIGHT))
    return _write(src, pic, "mirrored", quality=quality)


# ----- private information --------------------------------------------------------

def _minimal_exif(orientation: int) -> bytes:
    ex = Image.Exif()
    ex[0x0112] = orientation
    raw = ex.tobytes()
    return raw if raw.startswith(b"Exif\x00\x00") else b"Exif\x00\x00" + raw


def _strip_jpeg(data: bytes) -> tuple[bytes, bool]:
    """Remove EXIF (GPS, camera, dates), XMP, IPTC, comments and anything glued
    after the picture (phones append extra images and videos there, with their
    own GPS) from a JPEG, without re-encoding it. The colour profile and the
    orientation are kept."""
    if data[:2] != b"\xff\xd8":
        raise UserError("JPEG illisible.")
    orientation = 1
    try:
        with Image.open(io.BytesIO(data)) as im:
            orientation = int(im.getexif().get(0x0112, 1) or 1)
    except Exception:
        pass
    out = bytearray(b"\xff\xd8")
    state = {"removed": False, "inserted": orientation == 1}

    def insert_orientation():
        if not state["inserted"]:
            out.extend(_app1(_minimal_exif(orientation)))
            state["inserted"] = True

    i, n = 2, len(data)
    while True:
        if i >= n:
            raise UserError("JPEG incomplet.")
        if data[i] != 0xFF:
            raise UserError("JPEG endommagé.")
        while i < n and data[i] == 0xFF:          # fill bytes
            i += 1
        if i >= n:
            raise UserError("JPEG incomplet.")
        marker = data[i]
        i += 1
        if marker == 0xD9:                         # end of the picture
            insert_orientation()
            out += b"\xff\xd9"
            if data[i:].strip(b"\x00"):
                state["removed"] = True            # appended images, videos...
            break
        if marker == 0x01 or 0xD0 <= marker <= 0xD7:
            out += bytes((0xFF, marker))
            continue
        if i + 2 > n:
            raise UserError("JPEG endommagé.")
        length = int.from_bytes(data[i:i + 2], "big")
        if length < 2 or i + length > n:
            raise UserError("JPEG endommagé.")
        seg = b"\xff" + bytes((marker,)) + data[i:i + length]
        body = data[i + 2:i + length]
        i += length
        if marker == 0xDA:                         # scan: header, then coded data
            insert_orientation()
            out += seg
            j = i
            while True:
                j = data.find(b"\xff", j)
                if j < 0 or j + 1 >= n:
                    raise UserError("JPEG incomplet.")
                nxt = data[j + 1]
                if nxt == 0x00 or 0xD0 <= nxt <= 0xD7:
                    j += 2
                    continue
                break
            out += data[i:j]
            i = j
            continue
        drop = marker in (0xE1, 0xED, 0xFE) or (0xE3 <= marker <= 0xEF and marker != 0xEE)
        if marker == 0xE2 and not body.startswith(b"ICC_PROFILE\x00"):
            drop = True                            # multi-picture index, FlashPix...
        if drop:
            if not (marker == 0xE1 and orientation != 1
                    and body == _minimal_exif(orientation)):
                state["removed"] = True          # (our own orientation tag is no info)
            continue
        if marker != 0xE0:
            insert_orientation()
        out += seg
    return bytes(out), state["removed"]


def _orientation(data: bytes) -> int:
    try:
        with Image.open(io.BytesIO(data)) as im:
            return int(im.getexif().get(0x0112, 1) or 1)
    except Exception:
        return 1


def _app1(payload: bytes) -> bytes:
    return b"\xff\xe1" + (len(payload) + 2).to_bytes(2, "big") + payload


_PNG_PRIVATE = {b"tEXt", b"zTXt", b"iTXt", b"eXIf", b"tIME"}


def _strip_png(data: bytes) -> tuple[bytes, bool]:
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise UserError("PNG illisible.")
    out = bytearray(data[:8])
    removed = False
    i = 8
    while i + 8 <= len(data):
        length = int.from_bytes(data[i:i + 4], "big")
        kind = data[i + 4:i + 8]
        end = i + 12 + length
        if kind in _PNG_PRIVATE:
            removed = True
        else:
            out += data[i:end]
        i = end
        if kind == b"IEND":
            break
    return bytes(out), removed


def _strip_webp(data: bytes) -> tuple[bytes, bool]:
    if data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        raise UserError("WEBP illisible.")
    chunks = []
    removed = False
    i = 12
    while i + 8 <= len(data):
        kind = data[i:i + 4]
        size = int.from_bytes(data[i + 4:i + 8], "little")
        body = data[i + 8:i + 8 + size]
        if kind in (b"EXIF", b"XMP "):
            removed = True
        else:
            if kind == b"VP8X" and len(body) >= 1:
                body = bytes([body[0] & ~0x0C]) + body[1:]      # no EXIF / XMP flags
            chunks.append(kind + len(body).to_bytes(4, "little") + body
                          + (b"\x00" if size % 2 else b""))
        i += 8 + size + (size % 2)
    payload = b"WEBP" + b"".join(chunks)
    return b"RIFF" + len(payload).to_bytes(4, "little") + payload, removed


def strip_metadata(src: str, quality: int | None = None) -> str:
    """Copy without private information: GPS position, camera and phone model,
    dates, author, comments. JPEG, PNG and WEBP are not re-encoded (no quality
    loss); the picture stays upright and keeps its colours."""
    e = ext_of(src)
    with open(src, "rb") as f:
        data = f.read()
    try:
        if e in (".jpg", ".jpeg", ".jfif"):
            clean, removed = _strip_jpeg(data)
        elif e in (".png", ".webp") and _orientation(data) != 1:
            clean, removed = None, True         # turned by a tag: write it upright
        elif e == ".png":
            clean, removed = _strip_png(data)
        elif e == ".webp":
            clean, removed = _strip_webp(data)
        else:
            clean, removed = None, True
    except UserError:
        clean, removed = None, True             # unusual file: re-encode it instead
    if clean is not None:
        if not removed:
            raise NothingToDo("Cette image ne contient aucune information privée.")
        out = output_for(src, "clean")
        with open(out, "wb") as f:
            f.write(clean)
        try:
            with Image.open(out) as check_im:
                check_im.load()
            return out
        except Exception:
            os.remove(out)                       # fall back to a re-encoded copy
    pic = load(src)
    pic = Picture(pic.frames, pic.durations, pic.loop, pic.icc, None, pic.dpi,
                  pic.source_format)
    return _write(src, pic, "clean", quality=quality)


# ----- several pictures into one ------------------------------------------------------

def _rgb_to_srgb(im: Image.Image, icc: bytes | None) -> Image.Image:
    """Pixels described by another RGB profile (Display P3, Adobe RGB...) to
    sRGB, so they keep their colours once the profile is gone."""
    if not icc or _icc_space(icc) != "RGB" or im.mode not in ("RGB", "RGBA"):
        return im
    try:
        from PIL import ImageCms
        src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
        dst = ImageCms.createProfile("sRGB")
        if im.mode == "RGBA":
            alpha = im.getchannel("A")
            rgb = ImageCms.profileToProfile(im.convert("RGB"), src, dst, outputMode="RGB")
            rgb.putalpha(alpha)
            return rgb
        return ImageCms.profileToProfile(im, src, dst, outputMode="RGB")
    except Exception:
        return im


def assemble_images(srcs: Sequence[str], layout: str = "row",
                    quality: int | None = None, ctx=None) -> str:
    """Put pictures side by side ("row"), one under the other ("column") or in
    a grid, in the given order, into one new picture beside the first one.
    Sizes are read from the headers first, then each picture is shrunk to its
    place as soon as it is read, so memory stays low even with many photos."""
    import math as _math
    from statistics import median
    srcs = list(srcs)
    if len(srcs) < 2:
        raise UserError("Il faut au moins deux images.")
    sizes = []
    for s_ in srcs:
        try:
            sizes.append(oriented_size(s_))
        except Exception:
            raise UserError(f"Image illisible : {os.path.basename(s_)}")
    gap = 0
    if layout == "row":
        H = min(2400, median(h for _, h in sizes))
        boxes = [(w * H / h, H) for w, h in sizes]
        width, height = sum(w for w, _ in boxes), H
    elif layout == "column":
        W = min(2400, median(w for w, _ in sizes))
        boxes = [(W, h * W / w) for w, h in sizes]
        width, height = W, sum(h for _, h in boxes)
    else:
        n = len(srcs)
        cols = _math.ceil(_math.sqrt(n))
        rows = _math.ceil(n / cols)
        cw = min(1200, median(w for w, _ in sizes))
        ch = cw * median(h / w for w, h in sizes)
        gap = max(4, int(cw // 60))
        width, height = cols * cw + (cols + 1) * gap, rows * ch + (rows + 1) * gap
    k = min(1.0, 16000 / max(width, height))      # JPEG and viewers have limits
    width, height = max(1, round(width * k)), max(1, round(height * k))

    has_alpha = any(_has_alpha_hint(p) for p in srcs)
    canvas = Image.new("RGBA" if has_alpha else "RGB", (width, height),
                       (255, 255, 255, 0) if has_alpha else (255, 255, 255))
    x = y = 0
    for i, src in enumerate(srcs):
        if ctx is not None:
            ctx.check()
            ctx.progress(i / (len(srcs) + 1), f"Image {i + 1} sur {len(srcs)}")
        pic = load(src)
        icc = pic.icc
        im = _to_8bit(pic.to_srgb().frames[0])
        alpha = im.mode in ("RGBA", "LA", "PA") or (im.mode == "P" and "transparency" in im.info)
        im = _rgb_to_srgb(im.convert("RGBA" if alpha else "RGB"),
                          None if pic.is_cmyk else icc)
        del pic
        if alpha and canvas.mode == "RGB":           # header said opaque: flatten
            flat = Image.new("RGB", im.size, (255, 255, 255))
            flat.paste(im, mask=im.getchannel("A"))
            im = flat
        if layout in ("row", "column"):
            bw, bh = boxes[i]
            tw, th = max(1, round(bw * k)), max(1, round(bh * k))
            im = im.resize((tw, th), Image.Resampling.LANCZOS)
            canvas.paste(im, (x, y), im if im.mode == "RGBA" else None)
            if layout == "row":
                x += tw
            else:
                y += th
        else:
            r, c = divmod(i, cols)
            cell_w, cell_h, g = cw * k, ch * k, gap * k
            s_ = min(cell_w / im.width, cell_h / im.height)
            im = im.resize((max(1, round(im.width * s_)), max(1, round(im.height * s_))),
                           Image.Resampling.LANCZOS)
            px = round(g + c * (cell_w + g) + (cell_w - im.width) / 2)
            py = round(g + r * (cell_h + g) + (cell_h - im.height) / 2)
            canvas.paste(im, (px, py), im if im.mode == "RGBA" else None)
    fmt = "png" if canvas.mode == "RGBA" else "jpg"
    out = output_for(srcs[0], "assembled", new_ext=FORMATS[fmt][1])
    if ctx is not None:
        ctx.progress(len(srcs) / (len(srcs) + 1), "Assemblage")
    save(Picture([canvas]), out, fmt, quality=quality)
    return out


def _has_alpha_hint(path: str) -> bool:
    """Whether a picture may be transparent, from its header (cheap)."""
    try:
        with Image.open(path) as im:
            return im.mode in ("RGBA", "LA", "PA") or (
                im.mode == "P" and "transparency" in im.info)
    except Exception:
        return False


def clipboard_image(src: str, max_side: int = 8000):
    """The picture, upright and not bigger than max_side, for the clipboard."""
    pic = load(src).to_srgb()
    im = _to_8bit(pic.frames[0])
    alpha = im.mode in ("RGBA", "LA", "PA") or (im.mode == "P" and "transparency" in im.info)
    im = im.convert("RGBA" if alpha else "RGB")
    if max(im.size) > max_side:
        im.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    return im
