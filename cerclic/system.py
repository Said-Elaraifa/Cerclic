"""What differs between Windows and macOS, in one place: the keyboard shortcut
module of this system and the words the interface uses for it."""
from __future__ import annotations

import os
import sys

IS_MAC = sys.platform == "darwin"
IS_WINDOWS = os.name == "nt"
OS_NAME = "macOS" if IS_MAC else "Windows"
FILES_APP = "le Finder" if IS_MAC else "l'Explorateur"     # « dans le Finder »
MOD_KEY = "Cmd" if IS_MAC else "Ctrl"                      # copy, paste, arrows
DELETE_KEY = "⌫" if IS_MAC else "Suppr"
ENTER_KEY = "Retour" if IS_MAC else "Entrée"


def hotkeys():
    """The keyboard shortcut module of this system. Both offer the same names:
    Hotkey, label, check, DEFAULT_MODS, DEFAULT_VK, VK_ESCAPE, MOD_*."""
    if IS_MAC:
        from .mac import hotkey
    else:
        from .win import hotkey
    return hotkey


def hotkey_supported() -> bool:
    return IS_MAC or IS_WINDOWS
