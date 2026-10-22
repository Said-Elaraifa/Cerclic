"""Small diagnostic log, kept in %APPDATA%\\Cerclic\\cerclic.log (capped at 1 MB,
one previous copy kept). Running from the source tree, it sits in the project
folder instead, where it is easy to find and share.
"""
from __future__ import annotations

import datetime
import os
import sys
import threading
import traceback

_lock = threading.Lock()
_MAX_BYTES = 1_000_000
_path_cache: str | None = None


def log_path() -> str:
    global _path_cache
    if _path_cache:
        return _path_cache
    if getattr(sys, "frozen", False):
        from .settings import config_dir
        p = os.path.join(config_dir(), "cerclic.log")
    else:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        p = os.path.join(root, "cerclic.log")
    _path_cache = p
    return p


def _rotate(path: str) -> None:
    try:
        if os.path.getsize(path) > _MAX_BYTES:
            old = path + ".1"
            if os.path.exists(old):
                os.remove(old)
            os.replace(path, old)
    except OSError:
        pass


def log(msg: str) -> None:
    line = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
    with _lock:
        stream = sys.stderr
        if stream is not None:
            try:
                stream.write(line + "\n")
            except Exception:
                pass
        try:
            path = log_path()
            _rotate(path)
            with open(path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass


def log_exception(context: str) -> None:
    """Log the exception being handled, with its traceback."""
    log(f"{context}\n{traceback.format_exc().rstrip()}")
