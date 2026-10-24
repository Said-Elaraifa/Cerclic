"""What differs between Windows and macOS, in one place: the keyboard shortcut
module of this system and the names of its keys.

A sentence that names the Finder or the Explorer is written whole for each
system: `tr("… dans le Finder …") if IS_MAC else tr("… dans l'Explorateur …")`.
The key names below are French texts marked N_(): show them with tr(ENTER_KEY)."""
from __future__ import annotations

import os
import sys

from .i18n import N_

IS_MAC = sys.platform == "darwin"
IS_WINDOWS = os.name == "nt"
OS_NAME = "macOS" if IS_MAC else "Windows"                 # a name: never translated
MOD_KEY = N_("Cmd") if IS_MAC else N_("Ctrl")              # copy, paste, arrows
DELETE_KEY = "⌫" if IS_MAC else N_("Suppr")
ENTER_KEY = N_("Retour") if IS_MAC else N_("Entrée")


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
