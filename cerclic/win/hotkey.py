"""System-wide keyboard shortcut (Ctrl+Alt+Space) through RegisterHotKey.

Windows delivers WM_HOTKEY only for this exact key combination; nothing else
typed on the keyboard reaches Cerclic. The registration lives on a small thread
with its own message loop; `on_hotkey()` is called from that thread.
"""
from __future__ import annotations

import ctypes
import threading
from ctypes import wintypes
from typing import Callable

from ..log import log

MOD_ALT, MOD_CONTROL, MOD_NOREPEAT = 0x0001, 0x0002, 0x4000
VK_SPACE = 0x20
WM_HOTKEY, WM_QUIT = 0x0312, 0x0012
HOTKEY_ID = 0xC3C1
LABEL = "Ctrl+Alt+Espace"


class _MSG(ctypes.Structure):
    _fields_ = [("hwnd", wintypes.HWND), ("message", wintypes.UINT),
                ("wParam", wintypes.WPARAM), ("lParam", wintypes.LPARAM),
                ("time", wintypes.DWORD), ("pt", wintypes.POINT),
                ("lPrivate", wintypes.DWORD)]


class Hotkey:
    def __init__(self, on_hotkey: Callable[[], None],
                 on_status: Callable[[bool], None] | None = None):
        self.on_hotkey = on_hotkey
        self.on_status = on_status or (lambda ok: None)
        self._thread: threading.Thread | None = None
        self._tid = 0
        self._ready = threading.Event()

    def start(self) -> None:
        self._thread = threading.Thread(target=self._run, name="cerclic-hotkey",
                                        daemon=True)
        self._thread.start()
        self._ready.wait(2.0)

    def stop(self) -> None:
        if self._tid:
            ctypes.windll.user32.PostThreadMessageW(self._tid, WM_QUIT, 0, 0)
        if self._thread:
            self._thread.join(timeout=2.0)
        self._thread = None
        self._tid = 0

    def _run(self) -> None:
        user32 = ctypes.WinDLL("user32", use_last_error=True)
        user32.RegisterHotKey.argtypes = [wintypes.HWND, ctypes.c_int,
                                          wintypes.UINT, wintypes.UINT]
        user32.UnregisterHotKey.argtypes = [wintypes.HWND, ctypes.c_int]
        user32.GetMessageW.argtypes = [ctypes.POINTER(_MSG), wintypes.HWND,
                                       wintypes.UINT, wintypes.UINT]
        self._tid = ctypes.windll.kernel32.GetCurrentThreadId()
        ok = bool(user32.RegisterHotKey(None, HOTKEY_ID,
                                        MOD_CONTROL | MOD_ALT | MOD_NOREPEAT, VK_SPACE))
        log(f"raccourci {LABEL} : {'actif' if ok else 'déjà pris par une autre application'}")
        self._ready.set()
        self.on_status(ok)
        if not ok:
            return
        msg = _MSG()
        try:
            while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
                if msg.message == WM_HOTKEY and msg.wParam == HOTKEY_ID:
                    try:
                        self.on_hotkey()
                    except Exception as exc:
                        log(f"erreur raccourci : {exc!r}")
        finally:
            user32.UnregisterHotKey(None, HOTKEY_ID)
