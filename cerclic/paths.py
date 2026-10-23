"""Output path helpers.

Core rule of Cerclic: never overwrite the user's original file. Every result is
written next to its source with a readable suffix, and a counter is added when a
name is taken. Names are *reserved* atomically (an empty placeholder file or a
new folder is created on the spot), so two actions running at the same time can
never pick the same name.
"""
from __future__ import annotations

import contextlib
import os
import re
import threading

_track = threading.local()


@contextlib.contextmanager
def tracking():
    """Collect every path reserved in this thread while the block runs, so the
    engine can remove them if the action fails or is cancelled."""
    previous = getattr(_track, "items", None)
    _track.items = []
    try:
        yield _track.items
    finally:
        _track.items = previous


_hooks: list = []


def add_reserve_hook(fn) -> None:
    """fn(path) is called for every path reserved in this process (the app keeps
    a journal of them, a worker process reports them to the app)."""
    _hooks.append(fn)


def remove_reserve_hook(fn) -> None:
    if fn in _hooks:
        _hooks.remove(fn)


def _note(path: str) -> None:
    items = getattr(_track, "items", None)
    if items is not None:
        items.append(path)
    for fn in list(_hooks):
        try:
            fn(path)
        except Exception:
            pass

# Extension groups, lower case, dot included.
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".jfif", ".webp", ".bmp", ".gif", ".tif",
              ".tiff", ".heic", ".heif", ".avif"}
PDF_EXTS = {".pdf"}
VIDEO_EXTS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v", ".wmv", ".flv",
              ".3gp", ".mts", ".m2ts"}
AUDIO_EXTS = {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".oga", ".opus", ".flac",
              ".wma", ".amr", ".aif", ".aiff"}

SUPPORTED_EXTS = IMAGE_EXTS | PDF_EXTS | VIDEO_EXTS | AUDIO_EXTS


def ext_of(path: str) -> str:
    return os.path.splitext(path)[1].lower()


def kind_of(path: str) -> str:
    """Coarse family used to decide which actions apply."""
    e = ext_of(path)
    if e in IMAGE_EXTS:
        return "image"
    if e in PDF_EXTS:
        return "pdf"
    if e in VIDEO_EXTS:
        return "video"
    if e in AUDIO_EXTS:
        return "audio"
    return "other"


def natural_key(path: str):
    """Sort key so that 'page 2' comes before 'page 10'."""
    name = os.path.basename(path).lower()
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", name)]


def clean_selection(paths) -> list[str]:
    """Absolute, existing files only, without duplicates, in natural order."""
    seen: set[str] = set()
    out: list[str] = []
    for p in paths:
        if not p:
            continue
        p = os.path.abspath(str(p).strip().strip('"'))
        key = os.path.normcase(p)
        if key in seen or not os.path.isfile(p):
            continue
        if "$recycle.bin" in key.replace("\\", "/").lower().split("/"):
            continue        # an item of the Recycle Bin (named $R...): not a real file
        seen.add(key)
        out.append(p)
    out.sort(key=lambda p: (natural_key(p), p.lower()))
    return out


def _reserve_file(path: str) -> bool:
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return False
    os.close(fd)
    _note(path)
    return True


def _reserve_dir(path: str) -> bool:
    try:
        os.mkdir(path)
    except FileExistsError:
        return False
    _note(path)
    return True


MAX_NAME = 180     # characters kept from a long file name (Windows allows 255)


def _windows_downloads() -> str | None:
    """The real Downloads folder, even when the user moved it elsewhere."""
    if os.name != "nt":
        return None
    try:
        import ctypes
        import uuid
        from ctypes import wintypes
        shell32 = ctypes.WinDLL("shell32")
        ole32 = ctypes.WinDLL("ole32")
        shell32.SHGetKnownFolderPath.argtypes = [ctypes.c_void_p, wintypes.DWORD,
                                                 wintypes.HANDLE,
                                                 ctypes.POINTER(ctypes.c_void_p)]
        ole32.CoTaskMemFree.argtypes = [ctypes.c_void_p]
        guid = (ctypes.c_char * 16).from_buffer_copy(
            uuid.UUID("374DE290-123F-4565-9164-39C4925E467B").bytes_le)  # Downloads
        buf = ctypes.c_void_p()
        if shell32.SHGetKnownFolderPath(ctypes.byref(guid), 0, None,
                                        ctypes.byref(buf)) != 0:
            return None
        try:
            return ctypes.wstring_at(buf.value)
        finally:
            ole32.CoTaskMemFree(buf)
    except Exception:
        return None


def fallback_folder() -> str:
    """Where results go when the original's folder cannot be written to
    (read-only share, protected folder...): the user's Downloads."""
    home = os.path.expanduser("~")
    for d in (_windows_downloads(), *(os.path.join(home, n) for n in
                                      ("Downloads", "Téléchargements", "Documents"))):
        if d and os.path.isdir(d):
            return d
    return home


def _short(stem: str) -> str:
    return stem if len(stem) <= MAX_NAME else stem[:MAX_NAME].rstrip(" .")


def unique_path(folder: str, stem: str, ext: str, tag: str | None = None) -> str:
    """Reserve and return a free file path '<stem> (<tag>)<ext>', then
    '<stem> (<tag>) (2)<ext>'... The file exists (empty) when this returns."""
    if ext and not ext.startswith("."):
        ext = "." + ext
    stem = _short(stem)
    base = stem if not tag else f"{stem} ({tag})"
    n = 1
    while True:
        name = base if n == 1 else f"{base} ({n})"
        candidate = os.path.join(folder, name + ext)
        if _reserve_file(candidate):
            return candidate
        n += 1
        if n > 10000:
            raise OSError("no free name")


def unique_dir(folder: str, name: str) -> str:
    """Create and return a new folder '<name>', '<name> (2)'..."""
    name = _short(name)
    n = 1
    while True:
        candidate = os.path.join(folder, name if n == 1 else f"{name} ({n})")
        if _reserve_dir(candidate):
            return candidate
        n += 1
        if n > 10000:
            raise OSError("no free name")


def _with_fallback(reserve, folder: str):
    try:
        return reserve(folder)
    except PermissionError:
        pass
    except OSError as exc:  # read-only media or share
        if getattr(exc, "errno", None) not in (13, 30) and \
                getattr(exc, "winerror", None) not in (5, 19):
            raise
    return reserve(fallback_folder())


def output_for(src: str, tag: str, new_ext: str | None = None) -> str:
    """Reserved path next to src for a derived file (in Downloads if that
    folder cannot be written to). Keeps src extension unless new_ext is given."""
    folder = os.path.dirname(os.path.abspath(src))
    stem = os.path.splitext(os.path.basename(src))[0]
    ext = new_ext or ext_of(src)
    return _with_fallback(lambda f: unique_path(f, stem, ext, tag), folder)


def output_dir_for(src: str, tag: str) -> str:
    """New folder next to src, named '<stem> (<tag>)' (in Downloads if that
    folder cannot be written to)."""
    folder = os.path.dirname(os.path.abspath(src))
    stem = os.path.splitext(os.path.basename(src))[0]
    return _with_fallback(lambda f: unique_dir(f, f"{_short(stem)} ({tag})"), folder)


def sibling_path(src: str, name: str) -> str:
    """Reserved path for an explicitly named sibling."""
    folder = os.path.dirname(os.path.abspath(src))
    stem, ext = os.path.splitext(name)
    return _with_fallback(lambda f: unique_path(f, stem, ext or ".dat"), folder)
