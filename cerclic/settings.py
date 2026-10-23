"""User settings, stored as JSON in the per-user app data folder."""
from __future__ import annotations

import json
import os
import sys

APP_DIR_NAME = "Cerclic"
PORTABLE_DATA = "Données Cerclic"     # beside Cerclic.exe in the portable version
_MAC = sys.platform == "darwin"

DEFAULTS: dict = {
    "signature": "",            # path to the signature PNG (drawn or imported)
    "autostart": True,          # launch with Windows (macOS: at login)
    "context_menu": True,       # "Cerclic" in the right-click menu (macOS: Quick Action)
    "hotkey": True,             # the keyboard shortcut opens the wheel on the selection
    # Its combination. Windows: MOD_* flags and virtual-key code, Ctrl + Alt + Espace.
    # macOS: Carbon flags and key code + 0x100, Maj + Cmd + Espace (mac/hotkey.py).
    "hotkey_mods": 0x300 if _MAC else 0x3,
    "hotkey_vk": 0x131 if _MAC else 0x20,
    "classic_menu": False,      # Windows 11: show the full right-click menu at once
    "classic_menu_by_cerclic": False,  # we set it, so we may undo it on uninstall
    "jpg_quality": 90,
    "compress_quality": 70,
    "output_mode": "beside",    # results: "beside" the original, in "folder", or "ask"
    "output_folder": "",        # that folder
    "social_last": {},          # format and background last chosen: {"image": [...], "video": [...]}
    "compress_levels": {},      # strength last chosen to compress: {"pdf": "medium", ...}
    "welcome_shown": False,
}
# Keys from older versions (gesture, hold_ms...) are dropped on load.


def is_packaged() -> bool:
    """The Microsoft Store version (an MSIX package)."""
    if os.name != "nt" and not os.environ.get("CERCLIC_TEST_PACKAGE_FAMILY"):
        return False
    from .win.package import is_packaged as packaged
    return packaged()


def is_portable() -> bool:
    """The portable version of Windows (unzipped anywhere): no uninstaller beside
    it. Never on macOS: nothing is written into Cerclic.app (that would break
    its signature). Never from the Microsoft Store either."""
    if not getattr(sys, "frozen", False) or _MAC or is_packaged():
        return False
    return not os.path.exists(os.path.join(os.path.dirname(sys.executable),
                                           "unins000.exe"))


_portable_dir: str | None = None


def _portable_data() -> str | None:
    """The portable version keeps its settings, signature and log beside it,
    apart from an installed Cerclic (when that folder can be written to)."""
    global _portable_dir
    if _portable_dir is None:
        d = os.path.join(os.path.dirname(sys.executable), PORTABLE_DATA)
        try:
            os.makedirs(d, exist_ok=True)
            probe = os.path.join(d, ".ecriture")
            with open(probe, "w"):
                pass
            os.remove(probe)
            _portable_dir = d
        except OSError:
            _portable_dir = ""
    return _portable_dir or None


def config_dir() -> str:
    if is_packaged():           # the package's own folder, seen by every program
        from .win.package import local_state
        return local_state()
    if os.name == "nt":
        base = os.environ.get("APPDATA") or os.path.expanduser("~")
    elif _MAC:
        base = os.path.join(os.path.expanduser("~"), "Library", "Application Support")
    else:
        base = os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config")
    name = APP_DIR_NAME
    if is_portable():
        here = _portable_data()
        if here:
            return here
        name = APP_DIR_NAME + " Portable"
    d = os.path.join(base, name)
    os.makedirs(d, exist_ok=True)
    return d


def config_path() -> str:
    return os.path.join(config_dir(), "settings.json")


def import_classic_settings() -> bool:
    """Microsoft Store version, first start: begin with the choices made in the
    classic version installed before (signature included)."""
    if not is_packaged() or os.path.exists(config_path()):
        return False
    from .win.package import classic_settings
    src = classic_settings()
    if not src:
        return False
    try:
        with open(src, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return False
    if not isinstance(data, dict):
        return False
    sig = data.get("signature")
    if isinstance(sig, str) and sig:
        inside = os.path.normcase(os.path.dirname(os.path.abspath(sig))) == \
            os.path.normcase(os.path.dirname(os.path.abspath(src)))
        if inside:
            try:
                new = os.path.join(config_dir(), os.path.basename(sig))
                with open(sig, "rb") as fi, open(new, "wb") as fo:
                    fo.write(fi.read())
                data["signature"] = new
            except OSError:
                data["signature"] = ""
    # Windows 11's full menu is not needed here (the entry is in the short
    # menu), and the welcome shows what changed.
    for key in ("classic_menu", "classic_menu_by_cerclic", "welcome_shown"):
        data.pop(key, None)
    Settings(data).save()
    return True


class Settings:
    def __init__(self, data: dict | None = None):
        self._data = dict(DEFAULTS)
        if data:
            for k, v in data.items():
                if k in DEFAULTS and isinstance(v, type(DEFAULTS[k])):
                    self._data[k] = v

    @classmethod
    def load(cls) -> "Settings":
        try:
            with open(config_path(), "r", encoding="utf-8") as f:
                data = json.load(f)
            return cls(data if isinstance(data, dict) else None)
        except Exception:
            return cls()

    def save(self) -> None:
        path = config_path()
        tmp = path + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
            os.replace(tmp, path)
        except Exception:
            try:
                os.remove(tmp)
            except OSError:
                pass

    def get(self, key: str, default=None):
        return self._data.get(key, DEFAULTS.get(key, default))

    def set(self, key: str, value) -> None:
        self._data[key] = value

    def as_dict(self) -> dict:
        return dict(self._data)
