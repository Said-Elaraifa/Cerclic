"""System-wide keyboard shortcut that opens the wheel, through RegisterHotKey.

Windows delivers WM_HOTKEY only for the one combination Cerclic registered;
nothing else typed on the keyboard reaches Cerclic. The registration lives on
a small thread with its own message loop; `on_hotkey()` is called from it.

The combination is chosen in the settings (default Ctrl+Alt+Espace): `check()`
refuses the ones that would get in the way of typing or of Windows itself.
"""
from __future__ import annotations

import ctypes
import sys
import threading
from ctypes import wintypes
from typing import Callable

from ..i18n import N_, tr, trc
from ..log import log

MOD_ALT, MOD_CONTROL, MOD_SHIFT, MOD_WIN, MOD_NOREPEAT = 0x1, 0x2, 0x4, 0x8, 0x4000
VK_SPACE = 0x20
VK_ESCAPE = 0x1B
WM_HOTKEY, WM_QUIT = 0x0312, 0x0012
HOTKEY_ID = 0xC3C1

DEFAULT_MODS = MOD_CONTROL | MOD_ALT
DEFAULT_VK = VK_SPACE
_ON_WINDOWS = sys.platform == "win32"

_ARROWS = {0x25: "←", 0x26: "↑", 0x27: "→", 0x28: "↓"}
_KEYPAD_SIGNS = {0x6A: "*", 0x6B: "+", 0x6D: "-", 0x6E: ".", 0x6F: "/"}


def _names() -> dict[int, str]:
    """The keys that type no character, named as on the keyboards of the
    language in use (made at each call: the language can change)."""
    return {
        0x20: trc("touche Windows", "Espace"), 0x09: trc("touche Windows", "Tab"),
        0x0D: trc("touche Windows", "Entrée"),
        0x08: trc("touche Windows", "Retour"),               # Backspace
        0x1B: trc("touche Windows", "Échap"), 0x2D: trc("touche Windows", "Inser"),
        0x2E: trc("touche Windows", "Suppr"), 0x24: trc("touche Windows", "Origine"),
        0x23: trc("touche Windows", "Fin"), 0x21: trc("touche Windows", "Page préc."),
        0x22: trc("touche Windows", "Page suiv."), 0x13: trc("touche Windows", "Pause"),
        0x2C: trc("touche Windows", "Impr. écran"),
    }


# Punctuation keys depend on the keyboard layout: asked to Windows, else AZERTY.
_AZERTY = {0xBA: "$", 0xBB: "=", 0xBC: ",", 0xBD: "-", 0xBE: ";", 0xBF: ":",
           0xC0: "ù", 0xDB: ")", 0xDC: "*", 0xDD: "^", 0xDE: "²", 0xDF: "!", 0xE2: "<"}
_RESERVED = {                         # N_(): translated when shown (check)
    (MOD_ALT, 0x73): N_("Alt + F4 ferme les fenêtres."),
    (MOD_ALT, 0x09): N_("Alt + Tab change de fenêtre."),
    (MOD_ALT, 0x1B): N_("Alt + Échap change de fenêtre."),
    (MOD_ALT, 0x20): N_("Alt + Espace ouvre le menu des fenêtres."),
    (MOD_CONTROL, 0x1B): N_("Ctrl + Échap ouvre le menu Démarrer."),
    (MOD_CONTROL | MOD_ALT, 0x2E): N_("Ctrl + Alt + Suppr est réservé à Windows."),
    (MOD_CONTROL | MOD_SHIFT, 0x1B): N_("Ctrl + Maj + Échap ouvre le Gestionnaire des tâches."),
}
_ALTGR_LETTERS = set(b"EQMOAC")       # AltGr types €, @, µ, œ, æ, © with them (AZERTY)


def _layout_char(vk: int) -> str:
    try:
        code = ctypes.windll.user32.MapVirtualKeyW(vk, 2) & 0x7FFFFFFF  # VK_TO_CHAR
        return chr(code).upper() if 32 < code < 0x110000 else ""
    except Exception:
        return ""


def key_name(vk: int) -> str:
    """The name of a key, in the language in use. Never " + " in it: the
    settings window splits label() on it (tests/test_i18n_system.py checks
    the catalogues)."""
    if 0x41 <= vk <= 0x5A or 0x30 <= vk <= 0x39:
        return chr(vk)
    if 0x70 <= vk <= 0x87:
        return f"F{vk - 0x6F}"
    if 0x60 <= vk <= 0x69:
        return trc("touche Windows", "Pavé {key}", key=str(vk - 0x60))
    if vk in _KEYPAD_SIGNS:
        return trc("touche Windows", "Pavé {key}", key=_KEYPAD_SIGNS[vk])
    if vk in _ARROWS:
        return _ARROWS[vk]
    names = _names()
    if vk in names:
        return names[vk]
    if 0xBA <= vk <= 0xE2:
        return (_layout_char(vk) or _AZERTY.get(vk)
                or trc("touche Windows", "Touche {code}", code=vk))
    return trc("touche Windows", "Touche {code}", code=vk)


def label(mods: int, vk: int) -> str:
    """'Ctrl + Alt + Espace', 'Win + Maj + C' (in the order Windows writes them),
    in the language in use."""
    parts = []
    if mods & MOD_WIN:
        parts.append(trc("touche Windows", "Win"))
    if mods & MOD_CONTROL:
        parts.append(trc("touche Windows", "Ctrl"))
    if mods & MOD_ALT:
        parts.append(trc("touche Windows", "Alt"))
    if mods & MOD_SHIFT:
        parts.append(trc("touche Windows", "Maj"))
    parts.append(key_name(vk))
    return " + ".join(parts)


def _altgr_types(vk: int, shift: bool) -> bool | None:
    """Does AltGr (+ Maj) + this key type a character with the keyboard layout
    in use? None when it cannot be asked (not on Windows)."""
    try:
        user32 = ctypes.WinDLL("user32")
    except Exception:
        return None
    try:
        user32.GetKeyboardLayout.restype = ctypes.c_void_p
        user32.GetKeyboardLayout.argtypes = [wintypes.DWORD]
        user32.MapVirtualKeyExW.argtypes = [wintypes.UINT, wintypes.UINT, ctypes.c_void_p]
        user32.ToUnicodeEx.argtypes = [wintypes.UINT, wintypes.UINT,
                                       ctypes.POINTER(ctypes.c_ubyte), wintypes.LPWSTR,
                                       ctypes.c_int, wintypes.UINT, ctypes.c_void_p]
        hkl = user32.GetKeyboardLayout(0)
        state = (ctypes.c_ubyte * 256)()
        for k in (0x11, 0x12, 0xA2, 0xA5):           # Ctrl, Alt, left Ctrl, right Alt
            state[k] = 0x80
        if shift:
            state[0x10] = state[0xA0] = 0x80
        buf = ctypes.create_unicode_buffer(8)
        scan = user32.MapVirtualKeyExW(vk, 0, hkl)
        n = user32.ToUnicodeEx(vk, scan, state, buf, 8, 0x4, hkl)   # 0x4: state kept
        if n < 0:
            return True                                # a dead key (~, `...)
        return any(ord(ch) >= 0x20 for ch in buf.value[:n])
    except Exception:
        return None


def check(mods: int, vk: int) -> str | None:
    """Why this combination should not be used (in the language in use), or
    None if it is fine."""
    mods &= MOD_CONTROL | MOD_ALT | MOD_SHIFT | MOD_WIN
    if not vk or vk in (0x10, 0x11, 0x12, 0x5B, 0x5C):
        return tr("Ajoute une touche après Ctrl, Alt, Maj ou Win.")
    if (mods, vk) in _RESERVED:
        return tr(_RESERVED[(mods, vk)])
    if 0x7C <= vk <= 0x87 and not mods:
        return None          # F13 to F24 alone: rare keys (programmable mouse buttons)
    if 0x70 <= vk <= 0x7B and not mods & (MOD_CONTROL | MOD_ALT | MOD_WIN):
        return tr("{key} sert déjà dans Windows et les applications (aide, renommer, "
                  "actualiser, orthographe…). Ajoute par exemple Ctrl + Alt : "
                  "Ctrl + Alt + {key}.", key=key_name(vk))
    if 0x60 <= vk <= 0x69 and mods & MOD_ALT and not mods & (MOD_CONTROL | MOD_WIN):
        return tr("Alt avec le pavé numérique sert à taper des caractères "
                  "(Alt + 0201 = É). Choisis une autre combinaison.")
    if not mods & (MOD_CONTROL | MOD_ALT | MOD_WIN):
        return tr("Il faut Ctrl, Alt ou Win dans la combinaison (sinon cette touche "
                  "ne s'écrirait plus).")
    if mods & MOD_WIN:
        pass                                           # Win + key: Windows says if taken
    elif bin(mods).count("1") < 2:
        if mods & MOD_CONTROL:
            return tr("Ctrl + une seule touche sert déjà dans beaucoup d'applications "
                      "(gras, copier, coller, enregistrer…). Ajoute Maj ou Alt, par "
                      "exemple Ctrl + Maj + {key}.", key=key_name(vk))
        return tr("Alt + une seule touche sert déjà dans beaucoup d'applications "
                  "(les menus des applications). Ajoute Maj ou Ctrl, par exemple "
                  "Alt + Maj + {key}.", key=key_name(vk))
    if mods & MOD_CONTROL and mods & MOD_ALT and not mods & MOD_WIN:
        typed = _altgr_types(vk, bool(mods & MOD_SHIFT)) if _ON_WINDOWS else None
        if typed is None:
            typed = 0x30 <= vk <= 0x39 or vk >= 0xBA or vk in _ALTGR_LETTERS
        if typed:
            return tr("Cette combinaison sert à taper des caractères (@, €, #, œ…) "
                      "avec AltGr. Choisis-en une autre.")
    return None


class _MSG(ctypes.Structure):
    _fields_ = [("hwnd", wintypes.HWND), ("message", wintypes.UINT),
                ("wParam", wintypes.WPARAM), ("lParam", wintypes.LPARAM),
                ("time", wintypes.DWORD), ("pt", wintypes.POINT),
                ("lPrivate", wintypes.DWORD)]


class Hotkey:
    def __init__(self, on_hotkey: Callable[[], None],
                 on_status: Callable[[bool], None] | None = None,
                 mods: int = DEFAULT_MODS, vk: int = DEFAULT_VK):
        self.on_hotkey = on_hotkey
        self.on_status = on_status or (lambda ok: None)
        self.mods, self.vk = int(mods), int(vk)
        self.ok: bool | None = None
        self._thread: threading.Thread | None = None
        self._tid = 0
        self._ready = threading.Event()

    @property
    def label(self) -> str:
        return label(self.mods, self.vk)

    def start(self) -> None:
        self._thread = threading.Thread(target=self._run, name="cerclic-hotkey",
                                        daemon=True)
        self._thread.start()
        self._ready.wait(2.0)

    def stop(self) -> None:
        # Only a live registration thread is asked to quit: a thread id is
        # reused by Windows once its thread has ended.
        if self._tid and self._thread is not None and self._thread.is_alive():
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
        ok = bool(user32.RegisterHotKey(None, HOTKEY_ID, self.mods | MOD_NOREPEAT,
                                        self.vk))
        self.ok = ok
        log(f"raccourci {self.label} : "
            f"{'actif' if ok else 'déjà pris par Windows ou une autre application'}")
        if not ok:
            self._tid = 0
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
            self._tid = 0
            user32.UnregisterHotKey(None, HOTKEY_ID)
