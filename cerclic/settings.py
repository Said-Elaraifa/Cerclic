"""User settings, stored as JSON in the per-user app data folder."""
from __future__ import annotations

import json
import os

APP_DIR_NAME = "Cerclic"

DEFAULTS: dict = {
    "signature": "",          # path to a transparent PNG signature
    "autostart": True,        # launch with Windows
    "jpg_quality": 90,
    "compress_quality": 70,
    "resize_max_side": 1600,
    "gesture": "left_hold",    # left_hold | right_hold | double_right
    "double_ms": 350,          # window for the second right-click
    "hold_ms": 350,            # press-and-hold duration to open the wheel
    "ring_theme": "dark",
    "primary_only": False,     # show only primary actions on the first ring
}


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
            self._data.update(data)

    @classmethod
    def load(cls) -> "Settings":
        try:
            with open(config_path(), "r", encoding="utf-8") as f:
                return cls(json.load(f))
        except Exception:
            return cls()

    def save(self) -> None:
        try:
            with open(config_path(), "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def get(self, key: str, default=None):
        return self._data.get(key, DEFAULTS.get(key, default))

    def set(self, key: str, value) -> None:
        self._data[key] = value

    def as_dict(self) -> dict:
        return dict(self._data)
