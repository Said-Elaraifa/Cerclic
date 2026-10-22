"""Tiny diagnostic log: prints to the console and appends to cerclic.log.

When running from source the log sits in the project folder (easy to find and
share); the installed app writes it to %APPDATA%\\Cerclic.
"""
from __future__ import annotations

import datetime
import os
import sys
import threading

_lock = threading.Lock()


def log_path() -> str:
    if getattr(sys, "frozen", False):
        from .settings import config_dir
        return os.path.join(config_dir(), "cerclic.log")
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root, "cerclic.log")


def log(msg: str) -> None:
    line = f"{datetime.datetime.now():%H:%M:%S} [Cerclic] {msg}"
    with _lock:
        try:
            print(line, flush=True)
        except Exception:
            pass
        try:
            with open(log_path(), "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass
