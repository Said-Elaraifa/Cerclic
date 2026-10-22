"""Windows integration through the per-user registry (no admin rights needed).

* "Cerclic" at the top of the right-click menu of every supported file type,
  in Explorer, on the Desktop and in the Open/Save windows of all apps.
* Start with Windows (Run key).
* Windows 11 only, on request: the classic right-click menu, so the entry is
  one click away instead of under "Show more options".
"""
from __future__ import annotations

import os
import subprocess
import sys

from ..paths import SUPPORTED_EXTS

VERB = "Cerclic"
RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
RUN_VALUE = "Cerclic"
CLASSIC_KEY = r"Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}"


def _winreg():
    import winreg
    return winreg


def is_windows_11() -> bool:
    try:
        return os.name == "nt" and sys.getwindowsversion().build >= 22000
    except Exception:
        return False


# ----- what to launch -------------------------------------------------------------

def app_dir() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _pythonw() -> str:
    exe = sys.executable
    cand = os.path.join(os.path.dirname(exe), "pythonw.exe")
    return cand if os.path.exists(cand) else exe


def main_command(*args: str) -> str:
    """Command line that starts Cerclic itself."""
    extra = "".join(f" {a}" for a in args)
    if getattr(sys, "frozen", False):
        return f'"{sys.executable}"{extra}'
    script = os.path.join(app_dir(), "run_cerclic.py")
    return f'"{_pythonw()}" "{script}"{extra}'


def open_command() -> str:
    """Command line for the right-click entry: the tiny forwarder when it ships
    with the app (instant even with many files), else Cerclic itself."""
    forwarder = os.path.join(app_dir(), "CerclicOpen.exe")
    if os.path.exists(forwarder):
        return f'"{forwarder}" "%1"'
    return main_command("--open", '"%1"')


def icon_location() -> str:
    if getattr(sys, "frozen", False):
        return f"{sys.executable},0"
    return os.path.join(app_dir(), "assets", "cerclic.ico")


# ----- right-click entry --------------------------------------------------------------

def _verb_key(ext: str) -> str:
    return rf"Software\Classes\SystemFileAssociations\{ext}\shell\{VERB}"


def _delete_tree(root, path: str) -> None:
    winreg = _winreg()
    try:
        with winreg.OpenKey(root, path, 0, winreg.KEY_READ | winreg.KEY_WRITE) as k:
            while True:
                try:
                    child = winreg.EnumKey(k, 0)
                except OSError:
                    break
                _delete_tree(root, path + "\\" + child)
        winreg.DeleteKey(root, path)
    except FileNotFoundError:
        pass


def _notify_shell() -> None:
    try:
        import ctypes
        SHCNE_ASSOCCHANGED, SHCNF_IDLIST = 0x08000000, 0
        ctypes.windll.shell32.SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, None, None)
    except Exception:
        pass


def install_context_menu() -> None:
    winreg = _winreg()
    hk = winreg.HKEY_CURRENT_USER
    command, icon = open_command(), icon_location()
    for ext in sorted(SUPPORTED_EXTS):
        with winreg.CreateKey(hk, _verb_key(ext)) as k:
            winreg.SetValueEx(k, "MUIVerb", 0, winreg.REG_SZ, "Cerclic")
            winreg.SetValueEx(k, "Icon", 0, winreg.REG_SZ, icon)
            winreg.SetValueEx(k, "Position", 0, winreg.REG_SZ, "Top")
            winreg.SetValueEx(k, "MultiSelectModel", 0, winreg.REG_SZ, "Player")
        with winreg.CreateKey(hk, _verb_key(ext) + r"\command") as k:
            winreg.SetValueEx(k, "", 0, winreg.REG_SZ, command)
    _notify_shell()


def remove_context_menu() -> None:
    winreg = _winreg()
    for ext in sorted(SUPPORTED_EXTS):
        _delete_tree(winreg.HKEY_CURRENT_USER, _verb_key(ext))
    _notify_shell()


def context_menu_ok() -> bool:
    """True if the entry exists for every type and launches this copy."""
    winreg = _winreg()
    want = open_command()
    for ext in SUPPORTED_EXTS:
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _verb_key(ext) + r"\command") as k:
                if winreg.QueryValueEx(k, "")[0] != want:
                    return False
        except OSError:
            return False
    return True


# ----- start with Windows -----------------------------------------------------------------

def set_autostart(enabled: bool) -> None:
    winreg = _winreg()
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, RUN_KEY) as key:
        if enabled:
            winreg.SetValueEx(key, RUN_VALUE, 0, winreg.REG_SZ,
                              main_command("--background"))
        else:
            try:
                winreg.DeleteValue(key, RUN_VALUE)
            except FileNotFoundError:
                pass


def is_autostart() -> bool:
    winreg = _winreg()
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY) as key:
            return winreg.QueryValueEx(key, RUN_VALUE)[0] == main_command("--background")
    except OSError:
        return False


# ----- Windows 11 classic menu ------------------------------------------------------------

def classic_menu_enabled() -> bool:
    winreg = _winreg()
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, CLASSIC_KEY + r"\InprocServer32"):
            return True
    except OSError:
        return False


def set_classic_menu(enabled: bool) -> None:
    winreg = _winreg()
    if enabled:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, CLASSIC_KEY + r"\InprocServer32") as k:
            winreg.SetValueEx(k, "", 0, winreg.REG_SZ, "")
    else:
        _delete_tree(winreg.HKEY_CURRENT_USER, CLASSIC_KEY)


def restart_explorer() -> None:
    """Restart Explorer so a menu change applies now (folder windows close)."""
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    windir = os.environ.get("WINDIR", r"C:\Windows")
    subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], creationflags=flags,
                   stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
    subprocess.Popen([os.path.join(windir, "explorer.exe")], close_fds=True,
                     stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)


# ----- uninstall -----------------------------------------------------------------------------

def cleanup() -> None:
    """Remove everything Cerclic wrote to the registry (used by the uninstaller)."""
    from ..settings import Settings
    remove_context_menu()
    set_autostart(False)
    s = Settings.load()
    if s.get("classic_menu_by_cerclic"):
        set_classic_menu(False)
        s.set("classic_menu_by_cerclic", False)
        s.set("classic_menu", False)
        s.save()
