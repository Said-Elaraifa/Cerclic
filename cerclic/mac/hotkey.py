"""System-wide keyboard shortcut on macOS, through Carbon's RegisterEventHotKey.

It is the macOS counterpart of Windows' RegisterHotKey: macOS sends Cerclic an
event for the one combination it registered, and nothing else typed on the
keyboard reaches Cerclic. No Accessibility or Input Monitoring permission is
involved. The event arrives on the interface thread (Qt runs the Cocoa event
loop), where `on_hotkey()` is called.

Combinations are stored like the Windows ones, as (mods, vk), so the settings
window records them the same way:
  * mods: Carbon modifier flags (CMD, SHIFT, OPTION, CTRL below);
  * vk: the macOS key code + KEY_BASE, so that 0 (the A key) is not taken
    for "no key".
Qt on macOS reports Command as ControlModifier and Control as MetaModifier:
the MOD_* names follow Qt's, so the recorder maps them the same way as on
Windows.
"""
from __future__ import annotations

import ctypes
import sys
import threading
from typing import Callable

from ..log import log

CMD, SHIFT, OPTION, CTRL = 0x100, 0x200, 0x800, 0x1000
MOD_CONTROL, MOD_ALT, MOD_SHIFT, MOD_WIN = CMD, OPTION, SHIFT, CTRL   # Qt's names
KEY_BASE = 0x100

CARBON = "/System/Library/Frameworks/Carbon.framework/Carbon"
CORE_FOUNDATION = "/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation"


def vk_of(keycode: int) -> int:
    return KEY_BASE + keycode


def keycode_of(vk: int) -> int:
    return vk - KEY_BASE if vk >= KEY_BASE else -1


VK_SPACE = vk_of(0x31)
VK_ESCAPE = vk_of(0x35)
DEFAULT_MODS = CMD | SHIFT            # Maj + Cmd + Espace
DEFAULT_VK = VK_SPACE

# Key codes are positions on the keyboard (US names): the letter a key types is
# asked to macOS (_layout_char); these are the fallbacks.
_LETTERS = {0x00: "A", 0x0B: "B", 0x08: "C", 0x02: "D", 0x0E: "E", 0x03: "F", 0x05: "G",
            0x04: "H", 0x22: "I", 0x26: "J", 0x28: "K", 0x25: "L", 0x2E: "M", 0x2D: "N",
            0x1F: "O", 0x23: "P", 0x0C: "Q", 0x0F: "R", 0x01: "S", 0x11: "T", 0x20: "U",
            0x09: "V", 0x0D: "W", 0x07: "X", 0x10: "Y", 0x06: "Z"}
_DIGITS = {0x1D: "0", 0x12: "1", 0x13: "2", 0x14: "3", 0x15: "4", 0x17: "5", 0x16: "6",
           0x1A: "7", 0x1C: "8", 0x19: "9"}
_PUNCTUATION = {0x18: "=", 0x1B: "-", 0x1E: "]", 0x21: "[", 0x27: "'", 0x29: ";",
                0x2A: "\\", 0x2B: ",", 0x2C: "/", 0x2F: ".", 0x32: "`", 0x0A: "§"}
_NAMES = {0x31: "Espace", 0x24: "Retour", 0x4C: "Entrée", 0x30: "Tab", 0x33: "⌫",
          0x75: "Suppr", 0x35: "Échap", 0x73: "Début", 0x77: "Fin", 0x74: "Page préc.",
          0x79: "Page suiv.", 0x7B: "←", 0x7C: "→", 0x7D: "↓", 0x7E: "↑", 0x72: "Aide",
          0x47: "Pavé ⌧", 0x41: "Pavé .", 0x43: "Pavé *", 0x45: "Pavé +", 0x4B: "Pavé /",
          0x4E: "Pavé -", 0x51: "Pavé ="}
_KEYPAD = {0x52: 0, 0x53: 1, 0x54: 2, 0x55: 3, 0x56: 4, 0x57: 5, 0x58: 6, 0x59: 7,
           0x5B: 8, 0x5C: 9}
_F_KEYS = {0x7A: 1, 0x78: 2, 0x63: 3, 0x76: 4, 0x60: 5, 0x61: 6, 0x62: 7, 0x64: 8,
           0x65: 9, 0x6D: 10, 0x67: 11, 0x6F: 12, 0x69: 13, 0x6B: 14, 0x71: 15,
           0x6A: 16, 0x40: 17, 0x4F: 18, 0x50: 19, 0x5A: 20}
_MODIFIER_CODES = {0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x3E, 0x3F}
_ARROWS = {0x7B, 0x7C, 0x7D, 0x7E}

# ----- what a key types, asked to macOS -------------------------------------------------

_tis: dict = {}


def _layout_char(code: int) -> str:
    """The character this key types with the keyboard layout in use ('' when
    it cannot be asked). macOS only answers on the interface thread."""
    if sys.platform != "darwin" or threading.current_thread() is not threading.main_thread():
        return ""
    try:
        if not _tis:
            carbon = ctypes.CDLL(CARBON)
            cf = ctypes.CDLL(CORE_FOUNDATION)
            carbon.TISCopyCurrentKeyboardLayoutInputSource.restype = ctypes.c_void_p
            carbon.TISCopyCurrentKeyboardLayoutInputSource.argtypes = []
            carbon.TISGetInputSourceProperty.restype = ctypes.c_void_p
            carbon.TISGetInputSourceProperty.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
            carbon.LMGetKbdType.restype = ctypes.c_uint8
            carbon.LMGetKbdType.argtypes = []
            carbon.UCKeyTranslate.restype = ctypes.c_int32
            carbon.UCKeyTranslate.argtypes = [
                ctypes.c_void_p, ctypes.c_uint16, ctypes.c_uint16, ctypes.c_uint32,
                ctypes.c_uint32, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32),
                ctypes.c_ulong, ctypes.POINTER(ctypes.c_ulong),
                ctypes.POINTER(ctypes.c_uint16)]
            cf.CFDataGetBytePtr.restype = ctypes.c_void_p
            cf.CFDataGetBytePtr.argtypes = [ctypes.c_void_p]
            cf.CFRelease.restype = None
            cf.CFRelease.argtypes = [ctypes.c_void_p]
            _tis.update(carbon=carbon, cf=cf, prop=ctypes.c_void_p.in_dll(
                carbon, "kTISPropertyUnicodeKeyLayoutData").value)
        carbon, cf = _tis["carbon"], _tis["cf"]
        source = carbon.TISCopyCurrentKeyboardLayoutInputSource()
        if not source:
            return ""
        try:
            data = carbon.TISGetInputSourceProperty(source, _tis["prop"])
            if not data:
                return ""
            dead = ctypes.c_uint32(0)
            length = ctypes.c_ulong(0)
            chars = (ctypes.c_uint16 * 4)()
            err = carbon.UCKeyTranslate(cf.CFDataGetBytePtr(data), code, 3,   # display
                                        0, carbon.LMGetKbdType(), 1,          # no dead keys
                                        ctypes.byref(dead), 4, ctypes.byref(length), chars)
            if err or not length.value:
                return ""
            text = "".join(chr(c) for c in chars[:length.value]).strip()
        finally:
            cf.CFRelease(source)
        return text.upper() if text and text.isprintable() else ""
    except Exception:
        return ""


def key_name(vk: int) -> str:
    code = keycode_of(vk)
    if code < 0:
        return "…"
    if code in _NAMES:
        return _NAMES[code]
    if code in _F_KEYS:
        return f"F{_F_KEYS[code]}"
    if code in _KEYPAD:
        return f"Pavé {_KEYPAD[code]}"
    if code in _DIGITS:                    # the digit printed on the key (AZERTY too)
        return _DIGITS[code]
    if code in _LETTERS or code in _PUNCTUATION:
        return _layout_char(code) or _LETTERS.get(code) or _PUNCTUATION[code]
    return f"Touche {code}"


def label(mods: int, vk: int) -> str:
    """'Maj + Cmd + Espace', 'Ctrl + Option + C' (in the order Apple writes them:
    Control, Option, Shift, Command)."""
    parts = []
    if mods & CTRL:
        parts.append("Ctrl")
    if mods & OPTION:
        parts.append("Option")
    if mods & SHIFT:
        parts.append("Maj")
    if mods & CMD:
        parts.append("Cmd")
    parts.append(key_name(vk))
    return " + ".join(parts)


# ----- combinations to avoid -----------------------------------------------------------

_SYSTEM = {
    (CMD, 0x31): "Cmd + Espace ouvre Spotlight.",
    (CMD | OPTION, 0x31): "Option + Cmd + Espace ouvre la recherche du Finder.",
    (CTRL, 0x31): "Ctrl + Espace change la langue du clavier.",
    (CTRL | OPTION, 0x31): "Ctrl + Option + Espace change la langue du clavier.",
    (CTRL | CMD, 0x31): "Ctrl + Cmd + Espace ouvre les emojis.",
    (CMD, 0x30): "Cmd + Tab passe d'une application à l'autre.",
    (CMD | SHIFT, 0x30): "Maj + Cmd + Tab passe d'une application à l'autre.",
    (CMD | OPTION, 0x35): "Option + Cmd + Échap force une application à quitter.",
    (CMD | SHIFT, 0x14): "Maj + Cmd + 3 fait une capture d'écran.",
    (CMD | SHIFT, 0x15): "Maj + Cmd + 4 fait une capture d'écran.",
    (CMD | SHIFT, 0x17): "Maj + Cmd + 5 ouvre l'outil de capture d'écran.",
    (CMD | SHIFT, 0x16): "Maj + Cmd + 6 fait une capture de la Touch Bar.",
}
_BY_LETTER = {
    (CTRL | CMD, "Q"): "Ctrl + Cmd + Q verrouille l'écran.",
    (CMD | SHIFT, "Q"): "Maj + Cmd + Q ferme la session.",
    (CTRL | CMD, "F"): "Ctrl + Cmd + F passe en plein écran.",
    (CMD | OPTION, "D"): "Option + Cmd + D masque le Dock.",
    (CMD | OPTION, "C"): "Option + Cmd + C copie le chemin d'un fichier dans le Finder.",
    (CMD | OPTION, "H"): "Option + Cmd + H masque les autres applications.",
    (CMD | OPTION, "M"): "Option + Cmd + M réduit toutes les fenêtres.",
    (CMD | OPTION, "W"): "Option + Cmd + W ferme toutes les fenêtres.",
    (CMD | OPTION, "V"): "Option + Cmd + V déplace un fichier copié dans le Finder.",
}
_FINDER_SHIFT = set("ACDFGHIKLNOPRTU")      # Maj + Cmd + these: places and views


def check(mods: int, vk: int) -> str | None:
    """Why this combination should not be used, or None if it is fine."""
    mods &= CMD | SHIFT | OPTION | CTRL
    code = keycode_of(vk)
    if code < 0 or code in _MODIFIER_CODES:
        return "Ajoute une touche après Cmd, Ctrl, Option ou Maj."
    if (mods, code) in _SYSTEM:
        return _SYSTEM[(mods, code)]
    name = key_name(vk)
    if (mods, name) in _BY_LETTER:
        return _BY_LETTER[(mods, name)]
    if mods == CMD | SHIFT and name in _FINDER_SHIFT:
        return (f"Maj + Cmd + {name} sert déjà dans le Finder. Choisis une autre "
                "lettre, ou Maj + Cmd + Espace.")
    if code in _F_KEYS and _F_KEYS[code] >= 13 and not mods:
        return None          # F13 to F20 alone: rare keys (programmable mouse buttons)
    if not mods & (CMD | CTRL):
        return ("Il faut Cmd ou Ctrl dans la combinaison : macOS refuse les raccourcis "
                "faits seulement d'Option ou de Maj.")
    if mods == CMD:
        return ("Cmd + une seule touche sert déjà dans toutes les applications (copier, "
                f"coller, enregistrer…). Ajoute Maj, Option ou Ctrl, par exemple "
                f"Maj + Cmd + {name}.")
    if mods == CTRL and code in _ARROWS:
        return "Ctrl + les flèches passent d'un bureau à l'autre (Mission Control)."
    return None


def from_native(e) -> int:
    """The vk of a Qt key event: on macOS, Qt gives the key code itself."""
    try:
        code = int(e.nativeVirtualKey())
    except Exception:
        return 0
    return vk_of(code) if 0 <= code <= 0x7F else 0


# ----- registration -----------------------------------------------------------------------

def _four(s: str) -> int:
    return int.from_bytes(s.encode("ascii"), "big")


K_EVENT_CLASS_KEYBOARD = _four("keyb")
K_EVENT_HOTKEY_PRESSED = 5
K_EVENT_PARAM_DIRECT_OBJECT = _four("----")
TYPE_EVENT_HOTKEY_ID = _four("hkid")
SIGNATURE = _four("Ccl1")
NO_ERR = 0
EVENT_NOT_HANDLED = -9874


class EventTypeSpec(ctypes.Structure):
    _fields_ = [("eventClass", ctypes.c_uint32), ("eventKind", ctypes.c_uint32)]


class EventHotKeyID(ctypes.Structure):
    _fields_ = [("signature", ctypes.c_uint32), ("id", ctypes.c_uint32)]


_HANDLER = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_void_p, ctypes.c_void_p,
                            ctypes.c_void_p)


class _Carbon:
    """The one event handler Cerclic installs, and its registered combinations."""

    def __init__(self):
        lib = ctypes.CDLL(CARBON)
        lib.GetApplicationEventTarget.restype = ctypes.c_void_p
        lib.GetApplicationEventTarget.argtypes = []
        lib.InstallEventHandler.restype = ctypes.c_int32
        lib.InstallEventHandler.argtypes = [ctypes.c_void_p, _HANDLER, ctypes.c_ulong,
                                            ctypes.POINTER(EventTypeSpec), ctypes.c_void_p,
                                            ctypes.POINTER(ctypes.c_void_p)]
        lib.RegisterEventHotKey.restype = ctypes.c_int32
        lib.RegisterEventHotKey.argtypes = [ctypes.c_uint32, ctypes.c_uint32, EventHotKeyID,
                                            ctypes.c_void_p, ctypes.c_uint32,
                                            ctypes.POINTER(ctypes.c_void_p)]
        lib.UnregisterEventHotKey.restype = ctypes.c_int32
        lib.UnregisterEventHotKey.argtypes = [ctypes.c_void_p]
        lib.GetEventParameter.restype = ctypes.c_int32
        lib.GetEventParameter.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32,
                                          ctypes.c_void_p, ctypes.c_ulong, ctypes.c_void_p,
                                          ctypes.c_void_p]
        self.lib = lib
        self.callbacks: dict[int, Callable[[], None]] = {}
        self.next_id = 1
        self._handler = _HANDLER(self._on_event)        # kept alive with this object
        self._spec = EventTypeSpec(K_EVENT_CLASS_KEYBOARD, K_EVENT_HOTKEY_PRESSED)
        self._handler_ref = ctypes.c_void_p()
        err = lib.InstallEventHandler(lib.GetApplicationEventTarget(), self._handler, 1,
                                      ctypes.byref(self._spec), None,
                                      ctypes.byref(self._handler_ref))
        if err != NO_ERR:
            raise OSError(f"InstallEventHandler a échoué ({err})")

    def register(self, mods: int, keycode: int, callback) -> tuple[int, ctypes.c_void_p]:
        hk_id = EventHotKeyID(SIGNATURE, self.next_id)
        self.next_id += 1
        ref = ctypes.c_void_p()
        err = self.lib.RegisterEventHotKey(keycode, mods, hk_id,
                                           self.lib.GetApplicationEventTarget(), 0,
                                           ctypes.byref(ref))
        if err != NO_ERR or not ref.value:
            raise OSError(f"RegisterEventHotKey a refusé la combinaison ({err})")
        self.callbacks[hk_id.id] = callback
        return hk_id.id, ref

    def unregister(self, hk_id: int, ref) -> None:
        self.callbacks.pop(hk_id, None)
        if ref is not None and ref.value:
            self.lib.UnregisterEventHotKey(ref)

    def _on_event(self, _call_ref, event, _user_data) -> int:
        try:
            hk_id = EventHotKeyID()
            err = self.lib.GetEventParameter(event, K_EVENT_PARAM_DIRECT_OBJECT,
                                             TYPE_EVENT_HOTKEY_ID, None,
                                             ctypes.sizeof(hk_id), None, ctypes.byref(hk_id))
            if err != NO_ERR or hk_id.signature != SIGNATURE:
                return EVENT_NOT_HANDLED
            callback = self.callbacks.get(hk_id.id)
            if callback is None:
                return EVENT_NOT_HANDLED
            callback()
            return NO_ERR
        except Exception:
            return EVENT_NOT_HANDLED


_carbon_instance: _Carbon | None = None


def _carbon() -> _Carbon:
    global _carbon_instance
    if _carbon_instance is None:
        _carbon_instance = _Carbon()
    return _carbon_instance


class Hotkey:
    """Same use as the Windows one: start() registers the combination and calls
    on_status(ok); on_hotkey() then runs each time it is pressed; stop()
    releases it. Call them on the interface thread."""

    def __init__(self, on_hotkey: Callable[[], None],
                 on_status: Callable[[bool], None] | None = None,
                 mods: int = DEFAULT_MODS, vk: int = DEFAULT_VK):
        self.on_hotkey = on_hotkey
        self.on_status = on_status or (lambda ok: None)
        self.mods, self.vk = int(mods), int(vk)
        self.ok: bool | None = None
        self._id = 0
        self._ref = None

    @property
    def label(self) -> str:
        return label(self.mods, self.vk)

    def start(self) -> None:
        ok = False
        try:
            self._id, self._ref = _carbon().register(self.mods, keycode_of(self.vk),
                                                     self._pressed)
            ok = True
        except Exception as exc:
            log(f"raccourci {self.label} : {exc}")
        self.ok = ok
        log(f"raccourci {self.label} : {'actif' if ok else 'indisponible'}")
        self.on_status(ok)

    def _pressed(self) -> None:
        try:
            self.on_hotkey()
        except Exception as exc:
            log(f"erreur raccourci : {exc!r}")

    def stop(self) -> None:
        if self._ref is not None:
            try:
                _carbon().unregister(self._id, self._ref)
            except Exception:
                pass
        self._ref = None
        self._id = 0
