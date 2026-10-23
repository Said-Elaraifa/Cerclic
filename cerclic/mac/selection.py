"""The files selected in the Finder, for the keyboard shortcut.

Asked to the Finder through AppleScript, when the Finder is the application
in front (a window or the Desktop), or when Cerclic itself is (its window was
clicked after choosing the files): with any other application in front,
nothing is returned and Cerclic explains what to do. The first time, macOS
asks the user whether Cerclic may control the Finder (System Settings,
Privacy & Security, Automation); Cerclic only reads the selection.
"""
from __future__ import annotations

import subprocess

from ..log import log

SCRIPT = """
tell application "Finder"
    {front_check}
    set found to ""
    repeat with anItem in (get selection)
        try
            set found to found & (POSIX path of (anItem as alias)) & linefeed
        end try
    end repeat
    return found
end tell
"""
NOT_ALLOWED = "-1743"          # errAEEventNotPermitted: the user said no


class NotAllowed(Exception):
    """macOS does not let Cerclic ask the Finder (Automation permission)."""


def script(finder_in_front: bool = True) -> str:
    check = 'if not frontmost then return ""' if finder_in_front else ""
    return SCRIPT.replace("{front_check}", check)


def finder_selection(timeout: float = 90.0, finder_in_front: bool = True) -> list[str]:
    """Paths selected in the Finder; [] when it is not in front, unless
    `finder_in_front` is False (Cerclic is in front). The timeout leaves time
    to answer macOS's permission question."""
    try:
        res = subprocess.run(["/usr/bin/osascript", "-e", script(finder_in_front)],
                             capture_output=True,
                             text=True, timeout=timeout, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        log("sélection du Finder : pas de réponse")
        return []
    except OSError as exc:
        log(f"sélection du Finder : {exc}")
        return []
    if res.returncode != 0:
        err = (res.stderr or "").strip()
        if NOT_ALLOWED in err:
            raise NotAllowed()
        log(f"sélection du Finder : {err[:300]}")
        return []
    return [line for line in res.stdout.splitlines() if line.strip()]
