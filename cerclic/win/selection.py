"""Resolve the file(s) the user has selected where the cursor is.

Uses only the documented Shell automation model (Shell.Application):
  * Explorer windows: the window under the cursor is matched by handle and its
    selected items are read. With Windows 11 tabs, several entries share one
    window handle, so the active tab is picked by its title and selection.
  * Desktop: located with IShellWindows.FindWindowSW(SWC_DESKTOP), whose
    folder view exposes the same SelectedItems() call.
If nothing resolves, the caller falls back to a file picker.
"""
from __future__ import annotations

import ctypes
import os
import sys
from ctypes import wintypes

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
    import win32gui
    import win32com.client
    import pythoncom
    _PYWIN32 = True
except Exception:  # pragma: no cover - only importable on Windows
    _PYWIN32 = False

user32 = ctypes.windll.user32 if os.name == "nt" else None

GA_ROOT = 2
EXPLORER_CLASSES = {"CabinetWClass", "ExploreWClass"}
SWC_DESKTOP = 8
SWFO_NEEDDISPATCH = 1


def _root_window_at_cursor() -> tuple[int, str, str]:
    pt = wintypes.POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    hwnd = user32.WindowFromPoint(pt)
    if not hwnd:
        return 0, "", ""
    root = user32.GetAncestor(hwnd, GA_ROOT)
    return root, win32gui.GetClassName(root), win32gui.GetWindowText(root)


def selected_paths() -> list[str]:
    """Best-effort list of selected file paths under the cursor."""
    if not (_PYWIN32 and os.name == "nt"):
        return []
    pythoncom.CoInitialize()
    try:
        root, cls, title = _root_window_at_cursor()
        log(f"fenêtre sous le curseur : {cls!r} {title!r}")
        if cls in EXPLORER_CLASSES:
            paths = _explorer_selection(root, title)
            if paths:
                return paths
        paths = _desktop_selection()
        log(f"lecture du Bureau : {len(paths)} fichier(s)")
        return paths
    except Exception as exc:
        log(f"erreur sélection : {exc!r}")
        return []
    finally:
        pythoncom.CoUninitialize()


def _items_to_paths(items) -> list[str]:
    out = []
    for i in range(items.Count):
        p = items.Item(i).Path
        if p and os.path.exists(p):
            out.append(p)
    return out


def _explorer_selection(hwnd: int, title: str) -> list[str]:
    shell = win32com.client.Dispatch("Shell.Application")
    candidates = []
    for window in shell.Windows():
        try:
            if int(window.HWND) != int(hwnd):
                continue
            paths = _items_to_paths(window.Document.SelectedItems())
            name = str(window.LocationName or "")
            candidates.append((name, paths))
        except Exception:
            continue
    if not candidates:
        return []
    # Windows 11 tabs: prefer the tab whose name matches the window title,
    # then any tab that has a selection.
    for name, paths in candidates:
        if paths and name and name in title:
            return paths
    for _, paths in candidates:
        if paths:
            return paths
    return []


def _desktop_selection() -> list[str]:
    shell = win32com.client.Dispatch("Shell.Application")
    windows = shell.Windows()
    try:
        res = windows.FindWindowSW(0, pythoncom.Empty, SWC_DESKTOP, 0,
                                   SWFO_NEEDDISPATCH)
    except Exception as exc:
        log(f"FindWindowSW a échoué : {exc!r}")
        return []
    desktop = res[0] if isinstance(res, tuple) else res
    if desktop is None:
        return []
    try:
        return _items_to_paths(desktop.Document.SelectedItems())
    except Exception as exc:
        log(f"lecture de la sélection du Bureau a échoué : {exc!r}")
        return []
