"""User settings, stored as JSON in the per-user app data folder."""
from __future__ import annotations

import json
import os

APP_DIR_NAME = "Cerclic"

DEFAULTS: dict = {
    "signature": "",            # path to the signature PNG (drawn or imported)
    "autostart": True,          # launch with Windows
    "context_menu": True,       # "Cerclic" entry in the right-click menu
    "hotkey": True,             # Ctrl+Alt+Space opens the wheel on the selection
    "classic_menu": False,      # Windows 11: show the full right-click menu at once
    "classic_menu_by_cerclic": False,  # we set it, so we may undo it on uninstall
    "jpg_quality": 90,
    "compress_quality": 70,
    "welcome_shown": False,
}
# Keys from older versions (gesture, hold_ms...) are dropped on load.


def config_dir() -> str:
    if os.name == "nt":
        base = os.environ.get("APPDATA") or os.path.expanduser("~")
    else:
        base = os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config")
    d = os.path.join(base, APP_DIR_NAME)
    os.makedirs(d, exist_ok=True)
    return d


def config_path() -> str:
    return os.path.join(config_dir(), "settings.json")


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
