"""Output path helpers.

Core rule of Cerclic: never overwrite the user's original file. Every result is
written next to its source with a readable suffix, and a numeric counter is added
if a name is already taken.
"""
from __future__ import annotations

import os
import re

# Extension groups, lower case, dot included.
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".tif", ".tiff",
              ".heic", ".heif", ".avif"}
PDF_EXTS = {".pdf"}
VIDEO_EXTS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v", ".wmv", ".flv"}
AUDIO_EXTS = {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg"}
OFFICE_WORD = {".doc", ".docx"}
OFFICE_PPT = {".ppt", ".pptx"}
OFFICE_XLS = {".xls", ".xlsx"}


def ext_of(path: str) -> str:
    return os.path.splitext(path)[1].lower()


def kind_of(path: str) -> str:
    """Return a coarse family name used to decide which actions apply."""
    e = ext_of(path)
    if e in IMAGE_EXTS:
        return "image"
    if e in PDF_EXTS:
        return "pdf"
    if e in VIDEO_EXTS:
        return "video"
    if e in AUDIO_EXTS:
        return "audio"
    if e in OFFICE_WORD:
        return "word"
    if e in OFFICE_PPT:
        return "ppt"
    if e in OFFICE_XLS:
        return "xls"
    return "other"


_counter_re = re.compile(r" \((\d+)\)$")


def unique_path(folder: str, stem: str, ext: str, tag: str | None = None) -> str:
    """Build a free path in folder: '<stem> (<tag>)<ext>', then ' (2)', ' (3)'...

    ext must start with a dot. tag is an optional readable label such as
    'compressed' or 'jpg'.
    """
    if not ext.startswith("."):
        ext = "." + ext
    base = stem if not tag else f"{stem} ({tag})"
    candidate = os.path.join(folder, base + ext)
    if not os.path.exists(candidate):
        return candidate
    n = 2
    while True:
        candidate = os.path.join(folder, f"{base} ({n}){ext}")
        if not os.path.exists(candidate):
            return candidate
        n += 1


def output_for(src: str, tag: str, new_ext: str | None = None) -> str:
    """Path next to src for a derived file. Keeps src extension unless new_ext."""
    folder = os.path.dirname(os.path.abspath(src))
    stem = os.path.splitext(os.path.basename(src))[0]
    ext = (new_ext if new_ext else ext_of(src)) or ext_of(src)
    return unique_path(folder, stem, ext, tag)


def sibling_path(src: str, name: str) -> str:
    """Path for an explicitly named sibling, de-duplicated if needed."""
    folder = os.path.dirname(os.path.abspath(src))
    stem, ext = os.path.splitext(name)
    return unique_path(folder, stem, ext or ".dat")
