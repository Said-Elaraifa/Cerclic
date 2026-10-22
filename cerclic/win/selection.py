"""The files selected in the window the user is working in (for the shortcut).

Uses the documented Shell automation model (Shell.Application):
  * Explorer window in front: its selected items. With Windows 11 tabs, several
    entries share one window; the active tab is the one whose browser window
    is the first ShellTabWindowClass child (fallback: the tab named like the
    window title, then any tab with a selection).
  * Desktop in front: located with IShellWindows.FindWindowSW(SWC_DESKTOP).
Anything else returns an empty list (the caller then explains what to do).
"""
from __future__ import annotations

import ctypes
import os
import sys

from ..log import log


def _add_pywin32_dll_dir() -> None:
    """In a venv the pywin32 DLLs live in a side folder that is not on the DLL
    search path, so win32gui/pythoncom fail to import. Add it up front."""
    if os.name != "nt" or not hasattr(os, "add_dll_directory"):
        return
    for root in (sys.prefix, os.path.dirname(sys.executable)):
        cand = os.path.join(root, "Lib", "site-packages", "pywin32_system32")
        if os.path.isdir(cand):
            try:
                os.add_dll_directory(cand)
            except Exception:
                pass


_add_pywin32_dll_dir()

try:
    import pythoncom
    import win32com.client
    import win32gui
    _PYWIN32 = True
except Exception:  # pragma: no cover - only importable on Windows
    _PYWIN32 = False

GA_ROOT = 2
EXPLORER_CLASSES = {"CabinetWClass", "ExploreWClass"}
DESKTOP_CLASSES = {"Progman", "WorkerW"}
SWC_DESKTOP = 8
SWFO_NEEDDISPATCH = 1
SID_STopLevelBrowser = "{4C96BE40-915C-11CF-99D3-00AA004AE837}"


def _foreground_root() -> tuple[int, str, str]:
    user32 = ctypes.windll.user32
    hwnd = user32.GetForegroundWindow()
    if not hwnd:
        return 0, "", ""
    root = user32.GetAncestor(hwnd, GA_ROOT) or hwnd
    return root, win32gui.GetClassName(root), win32gui.GetWindowText(root)


def foreground_selection() -> list[str]:
    """Best-effort list of the files selected in the foreground window."""
    if not (_PYWIN32 and os.name == "nt"):
        return []
    pythoncom.CoInitialize()
    try:
        root, cls, title = _foreground_root()
        log(f"fenêtre au premier plan : {cls!r} {title!r}")
        if cls in EXPLORER_CLASSES:
            return _explorer_selection(root, title)
        if cls in DESKTOP_CLASSES:
            return _desktop_selection()
        return []
    except Exception as exc:
        log(f"erreur de lecture de la sélection : {exc!r}")
        return []
    finally:
        pythoncom.CoUninitialize()


def _items_to_paths(items) -> list[str]:
    out = []
    for i in range(items.Count):
        try:
            p = items.Item(i).Path
        except Exception:
            continue
        if p and os.path.isfile(p):
            out.append(p)
    return out


def _tab_browser_hwnd(window) -> int:
    """Window handle of the tab behind a Shell.Application entry (0 if unknown)."""
    try:
        from win32com.shell import shell as _shell  # registers IShellBrowser
        sp = window._oleobj_.QueryInterface(pythoncom.IID_IServiceProvider)
    except Exception:
        return 0
    for service in (_shell.IID_IShellBrowser, SID_STopLevelBrowser):
        try:
            browser = sp.QueryService(service, _shell.IID_IShellBrowser)
            return int(browser.GetWindow())
        except Exception:
            continue
    return 0


def _explorer_selection(hwnd: int, title: str) -> list[str]:
    shell = win32com.client.Dispatch("Shell.Application")
    tabs = []
    for window in shell.Windows():
        try:
            if int(window.HWND) != int(hwnd):
                continue
            tabs.append(window)
        except Exception:
            continue
    if not tabs:
        return []
    if len(tabs) == 1:
        return _items_to_paths(tabs[0].Document.SelectedItems())
    active = win32gui.FindWindowEx(hwnd, 0, "ShellTabWindowClass", None)
    if active:
        for window in tabs:
            if _tab_browser_hwnd(window) == active:
                try:
                    return _items_to_paths(window.Document.SelectedItems())
                except Exception:
                    break
    # Fallback: the tab named like the window, then any tab with a selection.
    found = []
    for window in tabs:
        try:
            paths = _items_to_paths(window.Document.SelectedItems())
            found.append((str(window.LocationName or ""), paths))
        except Exception:
            continue
    for name, paths in found:
        if paths and name and name in title:
            return paths
    for _, paths in found:
        if paths:
            return paths
    return []


def _desktop_selection() -> list[str]:
    shell = win32com.client.Dispatch("Shell.Application")
    try:
        res = shell.Windows().FindWindowSW(0, pythoncom.Empty, SWC_DESKTOP, 0,
                                           SWFO_NEEDDISPATCH)
    except Exception as exc:
        log(f"FindWindowSW a échoué : {exc!r}")
        return []
    # (the window object, with the handle as an extra out value)
    cands = res if isinstance(res, tuple) else (res,)
    desktop = next((c for c in cands if c is not None and not isinstance(c, int)), None)
    if desktop is None:
        return []
    try:
        return _items_to_paths(desktop.Document.SelectedItems())
    except Exception as exc:
        log(f"lecture de la sélection du Bureau a échoué : {exc!r}")
        return []
