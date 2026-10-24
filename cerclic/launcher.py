"""Process entry point.

Cerclic runs as one resident process per user session (the tray icon on
Windows, the menu bar icon on macOS). Every later launch (right-click entry,
shortcut double-click, files dropped on the icon, the installer) hands its
request to that process over a local pipe (a local socket on macOS) and exits.
This module only uses the standard library, so the hand-off is quick. (On
macOS, the system itself sends files to the running Cerclic: see app.py.)

Protocol (UTF-8 lines):  CERCLIC/1, <command>, <path>..., END   -> reply "OK".
"""
from __future__ import annotations

import os
import sys
import threading
import time

PROTOCOL = "CERCLIC/1"
COMMANDS = {"open", "hello", "background", "settings", "quit"}
RESIDENT_MUTEX = "Local\\Cerclic.Resident"
STORE_MUTEX = "Local\\CerclicStore.Resident"


def _store() -> bool:
    """The Microsoft Store version has its own pipe and lock: if the classic
    version is installed too, each runs apart (and the Store one says so)."""
    from .settings import is_packaged
    return is_packaged()


def resident_mutex() -> str:
    return STORE_MUTEX if _store() else RESIDENT_MUTEX


# ----- naming ------------------------------------------------------------------

def session_tag() -> str:
    """One Cerclic per Windows session (two accounts logged in = two Cerclic)."""
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes
        sid = wintypes.DWORD(0)
        k32 = ctypes.windll.kernel32
        if k32.ProcessIdToSessionId(k32.GetCurrentProcessId(), ctypes.byref(sid)):
            return str(sid.value)
        return "0"
    return str(os.getuid())


def server_name() -> str:
    """Name for QLocalServer; on Windows the pipe is \\\\.\\pipe\\<name>."""
    base = "CerclicStore" if _store() else "Cerclic"
    return os.environ.get("CERCLIC_SERVER_NAME") or f"{base}-{session_tag()}"


# ----- arguments and messages ----------------------------------------------------

def parse_args(argv: list[str]) -> tuple[str, list[str]]:
    """Cerclic.exe                -> ("hello", [])
       Cerclic.exe --background   -> ("background", [])   (start with Windows)
       Cerclic.exe --open a b     -> ("open", [a, b])
       Cerclic.exe a b            -> ("open", [a, b])      (files dropped on it)
       --settings, --quit, --cleanup, --selftest"""
    flags = {"--open": "open", "--settings": "settings", "--quit": "quit",
             "--cleanup": "cleanup", "--background": "background",
             "--selftest": "selftest"}
    cmd = "hello"
    paths: list[str] = []
    for a in argv:
        if a in flags:
            cmd = flags[a]
        elif a.startswith("--") or a.startswith("-psn"):
            continue
        elif a.strip():
            paths.append(a)
    if paths and cmd in ("hello", "background"):
        cmd = "open"
    return cmd, paths


def encode(cmd: str, paths: list[str]) -> bytes:
    lines = [PROTOCOL, cmd, *[p for p in paths if "\n" not in p and "\r" not in p], "END"]
    return ("\n".join(lines) + "\n").encode("utf-8")


def decode(data: bytes) -> tuple[str, list[str]] | None:
    try:
        lines = data.decode("utf-8").replace("\r", "").split("\n")
    except UnicodeDecodeError:
        return None
    if len(lines) < 3 or lines[0] != PROTOCOL or "END" not in lines:
        return None
    end = lines.index("END")
    cmd = lines[1]
    if cmd not in COMMANDS or end < 2:
        return None
    return cmd, [p for p in lines[2:end] if p]


# ----- client side -----------------------------------------------------------------

def send(cmd: str, paths: list[str], timeout: float = 4.0) -> bool:
    """Deliver a request to the resident Cerclic. False when none is running."""
    payload = encode(cmd, paths)
    try:
        if os.name == "nt":
            return _send_windows(server_name(), payload, timeout)
        return _send_posix(server_name(), payload, timeout)
    except Exception:
        return False


def _send_posix(name: str, payload: bytes, timeout: float) -> bool:
    import socket
    import tempfile
    path = name if os.path.isabs(name) else os.path.join(tempfile.gettempdir(), name)
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect(path)
    except OSError:
        s.close()
        return False
    try:
        s.sendall(payload)
        try:
            ack = s.recv(16)
        except socket.timeout:
            return True  # delivered; the reply is just late
        return ack.startswith(b"OK")
    finally:
        s.close()


def _send_windows(name: str, payload: bytes, timeout: float) -> bool:
    import ctypes
    from ctypes import wintypes

    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    u32 = ctypes.WinDLL("user32", use_last_error=True)
    k32.CreateFileW.restype = wintypes.HANDLE
    k32.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
                                ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD,
                                wintypes.HANDLE]
    k32.WaitNamedPipeW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD]
    k32.WriteFile.argtypes = [wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD,
                              ctypes.POINTER(wintypes.DWORD), ctypes.c_void_p]
    k32.ReadFile.argtypes = [wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD,
                             ctypes.POINTER(wintypes.DWORD), ctypes.c_void_p]
    k32.CloseHandle.argtypes = [wintypes.HANDLE]
    k32.GetNamedPipeServerProcessId.argtypes = [wintypes.HANDLE,
                                                ctypes.POINTER(wintypes.ULONG)]
    u32.AllowSetForegroundWindow.argtypes = [wintypes.DWORD]

    GENERIC_READ, GENERIC_WRITE = 0x80000000, 0x40000000
    OPEN_EXISTING = 3
    ERROR_PIPE_BUSY = 231
    INVALID = wintypes.HANDLE(-1).value

    path = "\\\\.\\pipe\\" + name
    deadline = time.monotonic() + timeout
    while True:
        h = k32.CreateFileW(path, GENERIC_READ | GENERIC_WRITE, 0, None,
                            OPEN_EXISTING, 0, None)
        if h and h != INVALID:
            break
        if ctypes.get_last_error() == ERROR_PIPE_BUSY and time.monotonic() < deadline:
            k32.WaitNamedPipeW(path, 250)
            continue
        return False

    reader_alive = False
    try:
        pid = wintypes.ULONG(0)
        if k32.GetNamedPipeServerProcessId(h, ctypes.byref(pid)):
            # The resident may now bring the wheel to the front.
            u32.AllowSetForegroundWindow(pid.value)
        buf = ctypes.create_string_buffer(payload, len(payload))
        done = wintypes.DWORD(0)
        sent = 0
        while sent < len(payload):
            if not k32.WriteFile(h, ctypes.byref(buf, sent), len(payload) - sent,
                                 ctypes.byref(done), None):
                return False
            sent += done.value
        ack = ctypes.create_string_buffer(16)
        got = wintypes.DWORD(0)
        result: dict = {}

        def read_ack():
            ok = k32.ReadFile(h, ack, 16, ctypes.byref(got), None)
            result["ok"] = bool(ok) and ack.raw[:got.value].startswith(b"OK")

        t = threading.Thread(target=read_ack, daemon=True)
        t.start()
        t.join(max(0.5, deadline - time.monotonic()))
        reader_alive = t.is_alive()
        return result.get("ok", True)
    finally:
        if not reader_alive:  # never close a handle a blocked read still uses
            k32.CloseHandle(h)


# ----- single instance ------------------------------------------------------------------

class ResidentLock:
    """Held for the whole life of the resident process."""

    def __init__(self):
        self.handle = None
        self.already = False
        if os.name == "nt":
            import ctypes
            k32 = ctypes.WinDLL("kernel32", use_last_error=True)
            k32.CreateMutexW.restype = ctypes.c_void_p
            k32.CreateMutexW.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_wchar_p]
            self.handle = k32.CreateMutexW(None, 0, resident_mutex())
            self.already = ctypes.get_last_error() == 183  # ERROR_ALREADY_EXISTS
        else:
            import fcntl
            import tempfile
            path = os.path.join(tempfile.gettempdir(), server_name() + ".lock")
            self.handle = open(path, "a")
            try:
                fcntl.flock(self.handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                self.already = True


def resident_running() -> bool:
    if os.name == "nt":
        import ctypes
        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        k32.OpenMutexW.restype = ctypes.c_void_p
        k32.OpenMutexW.argtypes = [ctypes.c_uint32, ctypes.c_int, ctypes.c_wchar_p]
        h = k32.OpenMutexW(0x00100000, 0, resident_mutex())   # SYNCHRONIZE
        if h:
            k32.CloseHandle(ctypes.c_void_p(h))
            return True
        return False
    import fcntl
    import tempfile
    path = os.path.join(tempfile.gettempdir(), server_name() + ".lock")
    try:
        with open(path, "a") as f:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            fcntl.flock(f, fcntl.LOCK_UN)
        return False
    except OSError:
        return True


def wait_resident_exit(timeout: float) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if not resident_running():
            return True
        time.sleep(0.1)
    return False


# ----- main ------------------------------------------------------------------------------

def take_open_list(argv: list[str]) -> tuple[list[str], list[str] | None]:
    """--open-list FILE: the files sent by the right-click entry of the
    Microsoft Store version when it had to start Cerclic (see win/package.py).
    Returns the other arguments and those files (None without the option)."""
    if "--open-list" not in argv:
        return argv, None
    i = argv.index("--open-list")
    rest = argv[:i] + argv[i + 2:]
    files: list[str] = []
    if i + 1 < len(argv):
        from .win.package import read_open_list
        files = read_open_list(argv[i + 1]) or []
    return rest, files


def apply_language() -> str:
    """The language chosen in the settings (« auto »: the computer's), in use
    before any text is shown, even before Qt exists."""
    from . import i18n
    try:
        from .settings import Settings
        choice = Settings.load().get("language")
    except Exception:
        choice = "auto"
    return i18n.set_language(choice)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    argv, listed = take_open_list(argv)
    cmd, paths = parse_args(argv)
    if listed is not None:
        cmd, paths = "open", paths + listed
    # Relative paths mean "from here": resolve them before handing them over
    # (the resident Cerclic works from another folder).
    paths = [os.path.abspath(p.strip().strip('"')) for p in paths if p.strip().strip('"')]

    if cmd == "cleanup":  # called by the uninstaller
        send("quit", [], timeout=2.0)
        try:
            if sys.platform == "darwin":
                from .mac.integration import cleanup
            else:
                from .win.shell import cleanup
            cleanup()
        except Exception:
            pass
        return 0
    if cmd == "selftest":  # checks the packaged Cerclic (no window)
        from .selftest import run
        return run()

    if send(cmd, paths):
        if cmd == "quit":       # the installer waits for Cerclic to be gone
            wait_resident_exit(10.0)
        return 0
    if cmd == "quit":
        return 0

    lock = ResidentLock()
    if lock.already:
        # Another Cerclic is starting right now: wait for it, then hand over.
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            time.sleep(0.2)
            if send(cmd, paths):
                return 0
        return 1

    apply_language()                    # the resident Cerclic speaks it from the start
    from .app import run_resident
    return run_resident(cmd, paths, lock)
