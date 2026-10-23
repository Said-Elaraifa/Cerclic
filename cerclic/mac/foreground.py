"""Bring Cerclic to the front on macOS, so its window gets the keyboard, and
give the keyboard back to the Finder afterwards.

Cerclic lives in the menu bar (no Dock icon): when the wheel opens from the
keyboard shortcut, another application is in front. Asking AppKit to make
Cerclic the active application lets Échap, Entrée and the arrows reach it.
The wheel always works on files of the Finder: once it and its popups are
gone, the Finder gets the keyboard back (as Windows does by itself).
"""
from __future__ import annotations

import ctypes

_objc: dict = {}


def _load() -> dict:
    if not _objc:
        lib = ctypes.CDLL("/usr/lib/libobjc.A.dylib")
        lib.objc_getClass.restype = ctypes.c_void_p
        lib.objc_getClass.argtypes = [ctypes.c_char_p]
        lib.sel_registerName.restype = ctypes.c_void_p
        lib.sel_registerName.argtypes = [ctypes.c_char_p]
        # objc_msgSend must be called with the exact signature of each method
        address = ctypes.cast(lib.objc_msgSend, ctypes.c_void_p).value
        vp = ctypes.c_void_p
        _objc.update(
            lib=lib,
            send=ctypes.CFUNCTYPE(vp, vp, vp)(address),
            send_bool=ctypes.CFUNCTYPE(None, vp, vp, ctypes.c_bool)(address),
            send_str=ctypes.CFUNCTYPE(vp, vp, vp, ctypes.c_char_p)(address),
            send_obj=ctypes.CFUNCTYPE(vp, vp, vp, vp)(address),
            count=ctypes.CFUNCTYPE(ctypes.c_ulong, vp, vp)(address),
            at=ctypes.CFUNCTYPE(vp, vp, vp, ctypes.c_ulong)(address),
            activate_with=ctypes.CFUNCTYPE(ctypes.c_bool, vp, vp, ctypes.c_ulong)(address),
            responds=ctypes.CFUNCTYPE(ctypes.c_bool, vp, vp, vp)(address),
            yield_to=ctypes.CFUNCTYPE(None, vp, vp, vp)(address),
            activate_from=ctypes.CFUNCTYPE(ctypes.c_bool, vp, vp, vp, ctypes.c_ulong)(address))
    return _objc


def activate() -> bool:
    """Make Cerclic the active application. Call on the interface thread."""
    try:
        o = _load()
        lib = o["lib"]
        cls = lib.objc_getClass(b"NSApplication")
        if not cls:
            return False
        app = o["send"](cls, lib.sel_registerName(b"sharedApplication"))
        if not app:
            return False
        o["send_bool"](app, lib.sel_registerName(b"activateIgnoringOtherApps:"), True)
        return True
    except Exception:
        return False


def give_back_to_finder() -> bool:
    """Make the Finder the active application again. Call on the interface thread."""
    try:
        o = _load()
        lib = o["lib"]
        sel = lib.sel_registerName
        ident = o["send_str"](lib.objc_getClass(b"NSString"), sel(b"stringWithUTF8String:"),
                              b"com.apple.finder")
        apps = o["send_obj"](lib.objc_getClass(b"NSRunningApplication"),
                             sel(b"runningApplicationsWithBundleIdentifier:"), ident)
        if not apps or not o["count"](apps, sel(b"count")):
            return False
        finder = o["at"](apps, sel(b"objectAtIndex:"), 0)
        if not finder:
            return False
        me_app = o["send"](lib.objc_getClass(b"NSApplication"), sel(b"sharedApplication"))
        # macOS 14 and later: the active application hands over (cooperative
        # activation); earlier versions do not know these messages.
        if me_app and o["responds"](me_app, sel(b"respondsToSelector:"),
                                    sel(b"yieldActivationToApplication:")):
            o["yield_to"](me_app, sel(b"yieldActivationToApplication:"), finder)
            if o["responds"](finder, sel(b"respondsToSelector:"),
                             sel(b"activateFromApplication:options:")):
                me = o["send"](lib.objc_getClass(b"NSRunningApplication"),
                               sel(b"currentApplication"))
                return bool(o["activate_from"](finder, sel(b"activateFromApplication:options:"),
                                               me, 0))
        return bool(o["activate_with"](finder, sel(b"activateWithOptions:"), 0))
    except Exception:
        return False
