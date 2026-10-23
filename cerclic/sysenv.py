"""What programs started by Cerclic inherit: environment and working folder.

The packaged Cerclic sets a few variables for itself (where its Qt plugins
are, its own folder first in PATH). A program Cerclic starts for the user
(Explorer, the application that opens a result) must not inherit them, or it
could load Cerclic's copies of Qt or of other libraries instead of its own.
Cerclic's working folder is also kept neutral: a program's working folder
cannot be deleted, renamed or ejected (USB key) while it runs.
"""
from __future__ import annotations

import os
import sys
from contextlib import contextmanager

_OWN_VARS = ("QT_PLUGIN_PATH", "QML2_IMPORT_PATH", "QT_QPA_PLATFORM_PLUGIN_PATH")
_OWN_PREFIXES = ("_PYI", "_MEI", "PYINSTALLER")


def _own_dirs() -> list[str]:
    if not getattr(sys, "frozen", False):
        return []
    dirs = [os.path.dirname(os.path.abspath(sys.executable))]
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        dirs.append(os.path.abspath(meipass))
    return [os.path.normcase(os.path.normpath(d)) for d in dirs]


def _is_own(entry: str, own: list[str]) -> bool:
    e = os.path.normcase(os.path.normpath(entry.strip().strip('"')))
    return any(e == d or e.startswith(d + os.sep) for d in own)


def clean_env(base=None) -> dict:
    """A copy of the environment without what the packaging added for Cerclic."""
    env = dict(os.environ if base is None else base)
    for key in list(env):
        if key.upper() in _OWN_VARS or key.upper().startswith(_OWN_PREFIXES):
            del env[key]
    own = _own_dirs()
    if own:
        for key in [k for k in env if k.upper() == "PATH"]:
            parts = [p for p in env[key].split(os.pathsep) if p and not _is_own(p, own)]
            env[key] = os.pathsep.join(parts)
    return env


def neutral_dir() -> str:
    """A folder nobody needs to eject, rename or delete."""
    for d in (os.environ.get("SystemRoot"), os.environ.get("WINDIR"),
              os.path.expanduser("~")):
        if d and os.path.isdir(d):
            return d
    return os.path.abspath(os.sep)


@contextmanager
def outside_env():
    """For calls that start a program without taking an environment
    (os.startfile): the process environment is cleaned during the call."""
    clean = clean_env()
    saved = {}
    for key in list(os.environ):
        if os.environ[key] != clean.get(key):
            saved[key] = os.environ[key]
    try:
        for key in saved:
            if key in clean:
                os.environ[key] = clean[key]
            else:
                del os.environ[key]
        yield
    finally:
        for key, value in saved.items():
            os.environ[key] = value
