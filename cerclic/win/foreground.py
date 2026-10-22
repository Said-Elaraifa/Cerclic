"""Bring a Cerclic window to the front so it gets the keyboard at once.

Windows lets a process take the foreground right after the user acted on it:
the right-click entry grants it through AllowSetForegroundWindow (see
launcher.py) and the keyboard shortcut grants it by itself.
"""
from __future__ import annotations

import os


def bring_to_front(hwnd: int) -> bool:
    if os.name != "nt" or not hwnd:
        return False
    import ctypes
    user32 = ctypes.windll.user32
    try:
        user32.BringWindowToTop(hwnd)
        ok = bool(user32.SetForegroundWindow(hwnd))
        return ok and user32.GetForegroundWindow() == hwnd
    except Exception:
        return False
