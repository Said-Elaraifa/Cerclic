"""Image actions: convert, compress, resize, rotate, crop.

All functions take a source path and return the path they wrote. HEIC/HEIF and
AVIF are read through pillow-heif when it is installed (it is, on Windows builds).
"""
from __future__ import annotations

import os
from typing import Sequence

from PIL import Image, ImageOps

from ..paths import output_for, ext_of

try:  # optional at import time so tests can run without it
    import pillow_heif  # type: ignore
    pillow_heif.register_heif_opener()
    try:
        pillow_heif.register_avif_opener()
    except Exception:
        pass
    _HEIF = True
except Exception:  # pragma: no cover
    _HEIF = False

# Formats we can write, mapped to (Pillow format, extension).
WRITE_FORMATS = {
    "png": ("PNG", ".png"),
    "jpg": ("JPEG", ".jpg"),
    "jpeg": ("JPEG", ".jpg"),
    "webp": ("WEBP", ".webp"),
}

_JPEG_QUALITY = 90
_WEBP_QUALITY = 90


def _load(src: str) -> Image.Image:
    im = Image.open(src)
    # Bake EXIF orientation so results are always upright.
    im = ImageOps.exif_transpose(im)
    return im


def _flatten(im: Image.Image, bg=(255, 255, 255)) -> Image.Image:
    """Put an image with alpha onto a solid background (needed for JPEG)."""
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        im = im.convert("RGBA")
        canvas = Image.new("RGB", im.size, bg)
        canvas.paste(im, mask=im.split()[-1])
        return canvas
    return im.convert("RGB")


def _save(im: Image.Image, out: str, fmt: str, quality: int | None = None) -> None:
    pil_fmt, _ = WRITE_FORMATS[fmt]
    params: dict = {}
    if pil_fmt == "JPEG":
        im = _flatten(im)
        params.update(quality=quality or _JPEG_QUALITY, optimize=True, progressive=True)
    elif pil_fmt == "WEBP":
        params.update(quality=quality or _WEBP_QUALITY, method=6)
    elif pil_fmt == "PNG":
        params.update(optimize=True)
    im.save(out, pil_fmt, **params)


def convert_image(src: str, fmt: str) -> str:
    """Convert to png/jpg/webp, written next to the source."""
    fmt = fmt.lower()
    if fmt not in WRITE_FORMATS:
        raise ValueError(f"unsupported target format: {fmt}")
    _, out_ext = WRITE_FORMATS[fmt]
    tag = "jpg" if fmt in ("jpg", "jpeg") else fmt
    out = output_for(src, tag, new_ext=out_ext)
    with _load(src) as im:
        _save(im, out, fmt)
    return out


def to_jpg(src: str) -> str:
    """Shortcut used for HEIC and other phone photos."""
    return convert_image(src, "jpg")


def compress_image(src: str, quality: int = 70, max_side: int | None = None) -> str:
    """Make a lighter copy. Non-JPEG/PNG/WEBP inputs become JPEG."""
    e = ext_of(src)
    if e in (".png",):
        fmt = "png"
    elif e in (".webp",):
        fmt = "webp"
    else:
        fmt = "jpg"
    _, out_ext = WRITE_FORMATS[fmt]
    out = output_for(src, "compressed", new_ext=out_ext)
    with _load(src) as im:
        if max_side:
            im.thumbnail((max_side, max_side), Image.LANCZOS)
        _save(im, out, fmt, quality=quality)
    return out


def resize_image(src: str, max_side: int | None = None, percent: float | None = None) -> str:
    """Resize by longest side (px) or by percent, keeping aspect ratio."""
    out = output_for(src, "resized")
    with _load(src) as im:
        w, h = im.size
        if percent:
            target = (max(1, int(w * percent / 100)), max(1, int(h * percent / 100)))
            im = im.resize(target, Image.LANCZOS)
        elif max_side:
            im.thumbnail((max_side, max_side), Image.LANCZOS)
        fmt = _fmt_for_ext(ext_of(out))
        _save(im, out, fmt)
    return out


def rotate_image(src: str, degrees: int = 90) -> str:
    """Rotate clockwise by a multiple of 90 without quality loss where possible."""
    out = output_for(src, "rotated")
    with _load(src) as im:
        # PIL rotate is counter-clockwise; negate so degrees means clockwise.
        im = im.rotate(-degrees, expand=True)
        fmt = _fmt_for_ext(ext_of(out))
        _save(im, out, fmt)
    return out


def crop_image(src: str, box: Sequence[int]) -> str:
    """Crop to box = (left, top, right, bottom) in source pixels."""
    left, top, right, bottom = (int(round(v)) for v in box)
    out = output_for(src, "cropped")
    with _load(src) as im:
        left = max(0, left)
        top = max(0, top)
        right = min(im.width, right)
        bottom = min(im.height, bottom)
        if right <= left or bottom <= top:
            raise ValueError("empty crop box")
        im = im.crop((left, top, right, bottom))
        fmt = _fmt_for_ext(ext_of(out))
        _save(im, out, fmt)
    return out


def _fmt_for_ext(e: str) -> str:
    e = e.lower().lstrip(".")
    if e in ("jpg", "jpeg"):
        return "jpg"
    if e == "webp":
        return "webp"
    if e == "png":
        return "png"
    return "png"


def image_size(src: str) -> tuple[int, int]:
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        return im.size
