"""Launch Cerclic with Windows via the per-user Run registry key."""
from __future__ import annotations

import os
import sys

RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
VALUE_NAME = "Cerclic"


def _exe_command() -> str:
    if getattr(sys, "frozen", False):
        return f'"{sys.executable}"'
    # Dev run: python -m cerclic
    return f'"{sys.executable}" -m cerclic'


def set_autostart(enabled: bool) -> None:
    if os.name != "nt":
        return
    import winreg
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, RUN_KEY) as key:
        if enabled:
            winreg.SetValueEx(key, VALUE_NAME, 0, winreg.REG_SZ, _exe_command())
        else:
            try:
                winreg.DeleteValue(key, VALUE_NAME)
            except FileNotFoundError:
                pass


def is_autostart() -> bool:
    if os.name != "nt":
        return False
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY) as key:
            winreg.QueryValueEx(key, VALUE_NAME)
            return True
    except FileNotFoundError:
        return False
