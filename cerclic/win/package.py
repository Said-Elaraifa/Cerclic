"""The Microsoft Store version: Cerclic inside an MSIX package.

Windows gives the package an identity (its family name) and its own data
folder, %LOCALAPPDATA%\\Packages\\<family>. Inside a package:

* nothing is written to the registry (Windows would keep it private to the
  package): the right-click entry comes from CerclicMenu.dll, declared in the
  manifest, and starting with Windows is the package's startup task;
* the entry is hidden while "menu-off" exists in LocalState (CerclicMenu.dll
  checks it each time the menu opens);
* when Cerclic is not running, the entry starts it with --open-list and a
  file in TempState holding the selected files.
"""
from __future__ import annotations

import os
import re
import sys
import threading
import time

APP_ID = "Cerclic"                     # <Application Id="Cerclic">
STARTUP_TASK = "CerclicStartup"        # <desktop:StartupTask TaskId="CerclicStartup">
MENU_OFF = "menu-off"
CLASSIC_UNINSTALL_KEY = (r"Software\Microsoft\Windows\CurrentVersion\Uninstall"
                         r"\{B7E9B9B1-5C2A-4E2E-9E8A-CERCLIC00001}_is1")
_LIST_NAME = re.compile(r"^open-\d+-\d+\.txt$")
_FAKE = "CERCLIC_TEST_PACKAGE_FAMILY"  # tests: behave as if packaged

_family: str | None = None
_checked = False


def _current(name: str) -> str | None:
    """GetCurrentPackage<name> (kernel32): the value, or None outside a package."""
    import ctypes
    from ctypes import wintypes
    fn = getattr(ctypes.windll.kernel32, f"GetCurrentPackage{name}")
    fn.argtypes = [ctypes.POINTER(wintypes.UINT), wintypes.LPWSTR]
    fn.restype = wintypes.LONG
    length = wintypes.UINT(0)
    if fn(ctypes.byref(length), None) != 122:       # ERROR_INSUFFICIENT_BUFFER
        return None                                 # 15700: not in a package
    buf = ctypes.create_unicode_buffer(length.value)
    if fn(ctypes.byref(length), buf) != 0:
        return None
    return buf.value or None


def _same_dir(a: str, b: str) -> bool:
    if os.path.normcase(os.path.normpath(a)) == os.path.normcase(os.path.normpath(b)):
        return True
    try:
        return os.path.samefile(a, b)
    except OSError:
        return False


def family() -> str | None:
    """The package family name (like 'Cerclic_1abc2def3ghj4'), or None when
    Cerclic is not running from its own package. A package identity alone is
    not enough: Python from the Microsoft Store has one, and a program
    started by a packaged app may inherit its parent's. The Store version is
    Cerclic.exe in the folder of the package."""
    global _family, _checked
    fake = os.environ.get(_FAKE)
    if fake:
        return fake
    if _checked:
        return _family
    _checked = True
    if os.name != "nt" or not getattr(sys, "frozen", False):
        return None
    try:
        fam = _current("FamilyName")
        where = _current("Path") if fam else None
        if fam and where and _same_dir(where, os.path.dirname(sys.executable)):
            _family = fam
    except Exception:
        _family = None
    return _family


def is_packaged() -> bool:
    return family() is not None


def root() -> str:
    """%LOCALAPPDATA%\\Packages\\<family>: the package's own data folder."""
    base = os.environ.get("LOCALAPPDATA") or os.path.join(os.path.expanduser("~"),
                                                          "AppData", "Local")
    return os.path.join(base, "Packages", family() or "")


def local_state() -> str:
    """Cerclic's data folder in the package (settings, signature, log)."""
    d = os.path.join(root(), "LocalState")
    os.makedirs(d, exist_ok=True)
    return d


def temp_state() -> str:
    return os.path.join(root(), "TempState")


def aumid() -> str:
    return f"{family()}!{APP_ID}"


# ----- the right-click entry -------------------------------------------------------

def set_menu(enabled: bool) -> None:
    marker = os.path.join(local_state(), MENU_OFF)
    if enabled:
        try:
            os.remove(marker)
        except FileNotFoundError:
            pass
    else:
        with open(marker, "w", encoding="utf-8") as f:
            f.write("« Cerclic » retiré du clic droit dans les réglages de Cerclic.\n")


def menu_enabled() -> bool:
    return not os.path.exists(os.path.join(local_state(), MENU_OFF))


def read_open_list(path: str) -> list[str] | None:
    """The files sent by the right-click entry when it had to start Cerclic.
    Only a list written by CerclicMenu.dll is read (and then deleted): a name
    like open-<n>-<n>.txt, in TempState or the temporary folder."""
    path = os.path.abspath(path.strip().strip('"'))
    folder, name = os.path.split(path)
    allowed = [temp_state()] if is_packaged() else []
    import tempfile
    allowed.append(tempfile.gettempdir())
    norm = os.path.normcase(os.path.normpath(folder))
    if not _LIST_NAME.match(name) or not any(
            norm == os.path.normcase(os.path.normpath(a)) for a in allowed if a):
        return None
    try:
        with open(path, "rb") as f:
            data = f.read(8_000_000)
    except OSError:
        return None
    try:
        os.remove(path)
    except OSError:
        pass
    from ..launcher import decode
    parsed = decode(data)
    if not parsed or parsed[0] != "open":
        return None
    return parsed[1]


def clean_open_lists(max_age: float = 3600.0) -> None:
    """Lists left behind (Cerclic stopped while starting)."""
    d = temp_state()
    try:
        names = os.listdir(d)
    except OSError:
        return
    now = time.time()
    for n in names:
        if _LIST_NAME.match(n):
            p = os.path.join(d, n)
            try:
                if now - os.path.getmtime(p) > max_age:
                    os.remove(p)
            except OSError:
                pass


# ----- starting with Windows (the package's startup task) ------------------------------

# StartupTaskState: Disabled, DisabledByUser, Enabled, DisabledByPolicy, EnabledByPolicy
_STATES = {0: "disabled", 1: "disabled_by_user", 2: "enabled",
           3: "disabled_by_policy", 4: "enabled_by_policy"}


def _in_thread(fn, timeout: float = 5.0):
    """WinRT calls in a thread of their own (its own apartment, never the
    window's), with a time limit."""
    box: dict = {}

    def run():
        try:
            try:        # COM for this new thread (MTA), whatever pywinrt does by default
                from winrt.runtime import ApartmentType, init_apartment
                init_apartment(ApartmentType.MULTI_THREADED)
            except Exception:
                pass
            box["value"] = fn()
        except BaseException as exc:      # noqa: BLE001 - reported to the caller
            box["error"] = exc

    t = threading.Thread(target=run, daemon=True, name="cerclic-startup-task")
    t.start()
    t.join(timeout)
    if "error" in box:
        raise box["error"]
    if "value" not in box:
        raise TimeoutError("la tâche de démarrage ne répond pas")
    return box["value"]


def _task():
    from winrt.windows.applicationmodel import StartupTask
    op = StartupTask.get_async(STARTUP_TASK)
    return op.get()


def startup_state() -> str | None:
    """'enabled', 'disabled', 'disabled_by_user', ... or None if unknown."""
    if not is_packaged():
        return None

    def read():
        return _STATES.get(int(_task().state))
    return _in_thread(read)


def set_startup(enabled: bool) -> str | None:
    """Turn the startup task on or off; returns the state that results (the
    user's own choice in Task Manager always wins)."""
    if not is_packaged():
        return None

    def change():
        task = _task()
        if enabled:
            state = task.request_enable_async().get()
        else:
            task.disable()
            state = task.state
        return _STATES.get(int(state))
    return _in_thread(change)


def startup_on(state: str | None) -> bool:
    return state in ("enabled", "enabled_by_policy")


# ----- the classic version, if also installed ------------------------------------------------

def classic_installed() -> bool:
    """The classic (installer) version is installed too: two Cerclic would run."""
    if os.name != "nt":
        return False
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, CLASSIC_UNINSTALL_KEY):
            return True
    except OSError:
        return False


def classic_uninstaller() -> str | None:
    """The classic version's uninstaller (unins000.exe), when it is there.
    It must be started by the user from the Explorer: started by the Store
    version, it would run inside the package and miss what it must remove."""
    if os.name != "nt":
        return None
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, CLASSIC_UNINSTALL_KEY) as k:
            try:
                cmd = winreg.QueryValueEx(k, "UninstallString")[0]
            except OSError:
                cmd = ""
            try:
                where = winreg.QueryValueEx(k, "InstallLocation")[0]
            except OSError:
                where = ""
    except OSError:
        return None
    cands = []
    if cmd:
        cands.append(cmd.strip().strip('"').split('" ')[0].strip('"'))
    if where:
        cands.append(os.path.join(where, "unins000.exe"))
    for c in cands:
        if c.lower().endswith(".exe") and os.path.isfile(c):
            return c
    return None


def classic_settings() -> str | None:
    """settings.json of the classic version, to start from the same choices."""
    base = os.environ.get("APPDATA")
    if not base:
        return None
    p = os.path.join(base, "Cerclic", "settings.json")
    return p if os.path.isfile(p) else None


def open_apps_settings() -> None:
    """Settings, Applications installées (to uninstall the classic version
    when its uninstaller cannot be shown)."""
    try:
        os.startfile("ms-settings:appsfeatures")     # type: ignore[attr-defined]
    except Exception:
        pass


def open_startup_settings() -> None:
    try:
        os.startfile("ms-settings:startupapps")      # type: ignore[attr-defined]
    except Exception:
        pass


