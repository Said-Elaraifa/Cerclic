"""Image actions: convert, compress, resize, rotate, crop.

Every function takes a source path and returns the path it wrote, always a new
file beside the source. Results are upright (EXIF orientation applied), keep the
colour profile and EXIF data, and animations (GIF, WEBP) keep all their frames.
HEIC/HEIF photos are read through pillow-heif; AVIF is native in Pillow.
"""
from __future__ import annotations

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
