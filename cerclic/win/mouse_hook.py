"""Global gesture detector for Cerclic.

Gestures (chosen in settings):
  * "left_hold" (default): press and hold the LEFT button on a file for
    `hold_ms` without moving; the wheel opens around it. Clicks, double clicks
    and drags are untouched (they release quickly or move).
  * "right_hold": same with the right button.
  * "double_right": two quick right clicks; a lone right click is replayed so
    the normal context menu still appears.
Plus a keyboard fallback, Ctrl+Alt+Space, which opens the wheel at the cursor
for the current selection (also handy to test without the mouse gesture).

The listener runs on its own thread with a message loop and calls
`on_trigger(x, y)` from that thread; the caller marshals to the GUI thread.
`on_status(ok, detail)` reports whether the listener could start.

All ctypes signatures are declared for 64-bit Windows: handles and LRESULT are
pointer-sized, and leaving them as the default 32-bit int silently breaks the
listener installation.
"""
from __future__ import annotations

import ctypes
import threading
from ctypes import wintypes
from typing import Callable

from ..log import log

user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

LRESULT = ctypes.c_ssize_t
ULONG_PTR = ctypes.c_size_t
LPARAM = ctypes.c_ssize_t
WPARAM = ctypes.c_size_t

WH_MOUSE_LL = 14
WM_QUIT = 0x0012
WM_HOTKEY = 0x0312
WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP = 0x0205
WM_MBUTTONDOWN = 0x0207
LLMHF_INJECTED = 0x00000001

MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010

MOD_ALT, MOD_CONTROL, MOD_NOREPEAT = 0x0001, 0x0002, 0x4000
VK_SPACE = 0x20
HOTKEY_ID = 0xC3C1


class POINT(ctypes.Structure):
    _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]


class MSLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [("pt", POINT), ("mouseData", wintypes.DWORD),
                ("flags", wintypes.DWORD), ("time", wintypes.DWORD),
                ("dwExtraInfo", ULONG_PTR)]


class MSG(ctypes.Structure):
    _fields_ = [("hwnd", wintypes.HWND), ("message", wintypes.UINT),
                ("wParam", WPARAM), ("lParam", LPARAM),
                ("time", wintypes.DWORD), ("pt", POINT),
                ("lPrivate", wintypes.DWORD)]


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", wintypes.LONG), ("dy", wintypes.LONG),
                ("mouseData", wintypes.DWORD), ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD), ("dwExtraInfo", ULONG_PTR)]


class _INPUTunion(ctypes.Union):
    _fields_ = [("mi", MOUSEINPUT)]


class INPUT(ctypes.Structure):
    _fields_ = [("type", wintypes.DWORD), ("u", _INPUTunion)]


HOOKPROC = ctypes.CFUNCTYPE(LRESULT, ctypes.c_int, WPARAM, LPARAM)

kernel32.GetModuleHandleW.restype = ctypes.c_void_p
kernel32.GetModuleHandleW.argtypes = [ctypes.c_wchar_p]
kernel32.GetCurrentThreadId.restype = wintypes.DWORD
user32.SetWindowsHookExW.restype = ctypes.c_void_p
user32.SetWindowsHookExW.argtypes = [ctypes.c_int, HOOKPROC, ctypes.c_void_p,
                                     wintypes.DWORD]
user32.CallNextHookEx.restype = LRESULT
user32.CallNextHookEx.argtypes = [ctypes.c_void_p, ctypes.c_int, WPARAM, LPARAM]
user32.UnhookWindowsHookEx.argtypes = [ctypes.c_void_p]
user32.GetMessageW.restype = wintypes.BOOL
user32.GetMessageW.argtypes = [ctypes.POINTER(MSG), wintypes.HWND,
                               wintypes.UINT, wintypes.UINT]
user32.TranslateMessage.argtypes = [ctypes.POINTER(MSG)]
user32.DispatchMessageW.argtypes = [ctypes.POINTER(MSG)]
user32.PostThreadMessageW.argtypes = [wintypes.DWORD, wintypes.UINT, WPARAM,
                                      LPARAM]
user32.RegisterHotKey.argtypes = [wintypes.HWND, ctypes.c_int, wintypes.UINT,
                                  wintypes.UINT]
user32.UnregisterHotKey.argtypes = [wintypes.HWND, ctypes.c_int]
user32.GetCursorPos.argtypes = [ctypes.POINTER(POINT)]
user32.SetCursorPos.argtypes = [ctypes.c_int, ctypes.c_int]
user32.SendInput.argtypes = [wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int]

INPUT_MOUSE = 0
_EXTRA = 0x43524C43  # tag on our own synthetic events so the listener skips them


def _send(flag: int) -> None:
    inp = INPUT(type=INPUT_MOUSE,
                u=_INPUTunion(mi=MOUSEINPUT(0, 0, 0, flag, 0, _EXTRA)))
    user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))


def _cursor() -> tuple[int, int]:
    pt = POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y


class GestureHook:
    def __init__(self, on_trigger: Callable[[int, int], None],
                 mode: str = "left_hold", double_ms: int = 300,
                 hold_ms: int = 350, tolerance: int = 8,
                 on_status: Callable[[bool, str], None] | None = None):
        self.on_trigger = on_trigger
        self.on_status = on_status or (lambda ok, detail: None)
        self.mode = mode
        self.double_ms = double_ms
        self.hold_ms = hold_ms
        self.tolerance = tolerance
        self._thread: threading.Thread | None = None
        self._thread_id = 0
        self._hook = None
        self._proc = HOOKPROC(self._callback)
        self._lock = threading.Lock()
        self._timer: threading.Timer | None = None
        self._state = "idle"
        self._pt = (0, 0)
        self._seen_event = False

    # -- lifecycle -----------------------------------------------------------
    def start(self) -> None:
        self._thread = threading.Thread(target=self._run, daemon=True,
                                        name="cerclic-hook")
        self._thread.start()

    def stop(self) -> None:
        if self._thread_id:
            user32.PostThreadMessageW(self._thread_id, WM_QUIT, 0, 0)
        self._cancel_timer()

    def _install(self):
        hmod = kernel32.GetModuleHandleW(None)
        hook = user32.SetWindowsHookExW(WH_MOUSE_LL, self._proc, hmod, 0)
        if hook:
            return hook, ""
        err1 = ctypes.get_last_error()
        hook = user32.SetWindowsHookExW(WH_MOUSE_LL, self._proc, None, 0)
        if hook:
            return hook, ""
        return None, f"SetWindowsHookEx a échoué (codes {err1}, {ctypes.get_last_error()})"

    def _run(self) -> None:
        self._thread_id = kernel32.GetCurrentThreadId()
        self._hook, err = self._install()
        hot = bool(user32.RegisterHotKey(None, HOTKEY_ID,
                                         MOD_CONTROL | MOD_ALT | MOD_NOREPEAT,
                                         VK_SPACE))
        if self._hook:
            log(f"écoute de la souris active (geste: {self.mode}, "
                f"raccourci Ctrl+Alt+Espace: {'oui' if hot else 'non'})")
            self.on_status(True, "")
        else:
            log(f"ÉCHEC écoute de la souris: {err}")
            self.on_status(False, err)
        msg = MSG()
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
            if msg.message == WM_HOTKEY and msg.wParam == HOTKEY_ID:
                x, y = _cursor()
                log(f"raccourci clavier à ({x}, {y})")
                self.on_trigger(x, y)
                continue
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))
        if hot:
            user32.UnregisterHotKey(None, HOTKEY_ID)
        if self._hook:
            user32.UnhookWindowsHookEx(self._hook)
            self._hook = None

    # -- timers --------------------------------------------------------------
    def _cancel_timer(self) -> None:
        if self._timer:
            self._timer.cancel()
            self._timer = None

    def _arm(self, seconds: float, fn) -> None:
        self._cancel_timer()
        self._timer = threading.Timer(seconds, fn)
        self._timer.daemon = True
        self._timer.start()

    def _near(self, a, b) -> bool:
        return abs(a[0] - b[0]) <= self.tolerance and abs(a[1] - b[1]) <= self.tolerance

    # -- hold fire -----------------------------------------------------------
    def _hold_fire(self) -> None:
        with self._lock:
            if self._state != "holding":
                return
            pt = self._pt
            self._state = "suppress_up"
        log(f"appui maintenu détecté à {pt}")
        # Left button: complete the click now so Explorer keeps the file
        # selected and does not stay in a half-pressed (drag) state.
        if self.mode == "left_hold":
            _send(MOUSEEVENTF_LEFTUP)
        self.on_trigger(*pt)

    def _replay_single(self) -> None:
        with self._lock:
            if self._state != "wait":
                return
            pt = self._pt
            self._state = "idle"
        user32.SetCursorPos(int(pt[0]), int(pt[1]))
        _send(MOUSEEVENTF_RIGHTDOWN)
        _send(MOUSEEVENTF_RIGHTUP)

    # -- callback ------------------------------------------------------------
    def _callback(self, nCode, wParam, lParam):
        if nCode >= 0:
            try:
                info = ctypes.cast(lParam, ctypes.POINTER(MSLLHOOKSTRUCT)).contents
                if not self._seen_event:
                    self._seen_event = True
                    log("premier événement souris reçu")
                if not ((info.flags & LLMHF_INJECTED) or info.dwExtraInfo == _EXTRA):
                    pt = (info.pt.x, info.pt.y)
                    if self.mode == "double_right":
                        swallow = self._double_right(wParam, pt)
                    elif self.mode == "right_hold":
                        swallow = self._hold(wParam, pt, WM_RBUTTONDOWN, WM_RBUTTONUP)
                    else:
                        swallow = self._hold(wParam, pt, WM_LBUTTONDOWN, WM_LBUTTONUP)
                    if swallow:
                        return 1
            except Exception as exc:  # never let an error break the mouse
                log(f"erreur dans l'écoute: {exc}")
        return user32.CallNextHookEx(self._hook, nCode, wParam, lParam)

    def _hold(self, msg, pt, down_msg, up_msg) -> bool:
        if msg == down_msg:
            with self._lock:
                self._state = "holding"
                self._pt = pt
            self._arm(self.hold_ms / 1000.0, self._hold_fire)
            return False  # the click goes through: the file gets selected
        if msg == up_msg:
            with self._lock:
                st = self._state
                self._state = "idle"
            self._cancel_timer()
            return st == "suppress_up"  # eat only the release that opened the wheel
        if msg == WM_MOUSEMOVE:
            with self._lock:
                holding = self._state == "holding"
                start = self._pt
            if holding and not self._near(pt, start):
                self._cancel_timer()
                with self._lock:
                    if self._state == "holding":
                        self._state = "idle"
        return False

    def _double_right(self, msg, pt) -> bool:
        if msg == WM_RBUTTONDOWN:
            with self._lock:
                if self._state == "wait" and self._near(pt, self._pt):
                    self._cancel_timer()
                    self._state = "down2"
                    return True
                self._state = "down1"
                self._pt = pt
                return True
        if msg == WM_RBUTTONUP:
            with self._lock:
                st = self._state
                if st == "down1":
                    self._state = "wait"
                    self._arm(self.double_ms / 1000.0, self._replay_single)
                    return True
                if st == "down2":
                    self._state = "idle"
                    x, y = self._pt
            if st == "down2":
                self.on_trigger(x, y)
                return True
            return False
        if msg in (WM_LBUTTONDOWN, WM_MBUTTONDOWN):
            with self._lock:
                waiting = self._state == "wait"
            if waiting:
                self._replay_single()
        return False


DoubleRightClickHook = GestureHook
