"""The macOS parts, checked on any system: shortcut names and rules, the Finder
Quick Action and login item files, files sent by macOS, the settings window
as it looks on a Mac."""
import os
import plistlib
import shutil
import subprocess

import pytest
from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QFileOpenEvent, QKeyEvent

from cerclic.mac import hotkey as mk
from cerclic.mac import integration


# ----- keyboard shortcut ---------------------------------------------------------------------

def test_mac_shortcut_names():
    assert mk.label(mk.DEFAULT_MODS, mk.DEFAULT_VK) == "Maj + Cmd + Espace"
    assert mk.label(mk.CTRL | mk.OPTION, mk.vk_of(0x08)) == "Ctrl + Option + C"
    assert mk.key_name(mk.vk_of(0x7A)) == "F1" and mk.key_name(mk.vk_of(0x69)) == "F13"
    assert mk.key_name(mk.vk_of(0x14)) == "3"           # the digit printed on the key
    assert mk.key_name(mk.vk_of(0x00)) == "A"           # 0 is a real key: the A key
    assert mk.key_name(0) == "…"


def test_mac_shortcut_rules():
    ok = [(mk.CMD | mk.SHIFT, mk.VK_SPACE), (mk.CTRL | mk.OPTION, mk.vk_of(0x08)),
          (mk.CMD | mk.SHIFT, mk.vk_of(0x07)), (0, mk.vk_of(0x69))]       # X, F13 alone
    for mods, vk in ok:
        assert mk.check(mods, vk) is None, mk.label(mods, vk)
    refused = {
        (mk.CMD, mk.VK_SPACE): "Spotlight",
        (mk.CMD, mk.vk_of(0x08)): "copier",                  # Cmd + C
        (mk.OPTION | mk.SHIFT, mk.vk_of(0x08)): "Cmd ou Ctrl",   # macOS refuses those
        (mk.CMD | mk.SHIFT, mk.vk_of(0x14)): "capture",          # Maj + Cmd + 3
        (mk.CMD | mk.SHIFT, mk.vk_of(0x05)): "Finder",           # Maj + Cmd + G
        (mk.CTRL | mk.CMD, mk.vk_of(0x0C)): "verrouille",        # Ctrl + Cmd + Q
        (mk.CTRL, mk.vk_of(0x7B)): "Mission Control",
        (mk.CMD | mk.SHIFT, mk.vk_of(0x38)): "Ajoute une touche",   # Shift as the key
    }
    for (mods, vk), word in refused.items():
        problem = mk.check(mods, vk)
        assert problem and word in problem, (mk.label(mods, vk), problem)


def test_mac_key_events_give_key_codes():
    e = QKeyEvent(QEvent.KeyPress, Qt.Key_X, Qt.ControlModifier | Qt.ShiftModifier,
                  0, 0x07, 0, "x")
    assert mk.from_native(e) == mk.vk_of(0x07)
    e = QKeyEvent(QEvent.KeyPress, Qt.Key_A, Qt.NoModifier, 0, 0x00, 0, "a")
    assert mk.from_native(e) == mk.vk_of(0x00) != 0


def test_mac_hotkey_reports_failure_without_carbon(monkeypatch):
    """Off a Mac (or if macOS refuses), the shortcut says it is unavailable."""
    seen = []
    monkeypatch.setattr(mk, "_carbon_instance", None)
    monkeypatch.setattr(mk, "CARBON", "/nonexistent/Carbon")
    h = mk.Hotkey(lambda: None, seen.append)
    h.start()
    assert seen == [False] and h.ok is False
    h.stop()


# ----- Quick Action and opening at login -------------------------------------------------------

@pytest.fixture
def mac_home(tmp_path, monkeypatch):
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setattr(integration, "PBS", str(tmp_path / "no-pbs"))
    return home


def test_quick_action_files(mac_home):
    app = "/Applications/Cerclic d'Ali.app"           # a quote and a space in the path
    assert integration.install_quick_action(app) is True
    root = mac_home / "Library" / "Services" / "Cerclic.workflow" / "Contents"
    info = plistlib.loads((root / "Info.plist").read_bytes())
    service = info["NSServices"][0]
    assert service["NSMenuItem"]["default"] == "Cerclic"
    assert service["NSMessage"] == "runWorkflowAsService"
    assert service["NSRequiredContext"]["NSApplicationIdentifier"] == "com.apple.finder"
    flow = plistlib.loads((root / "document.wflow").read_bytes())
    action = flow["actions"][0]["action"]
    params = action["ActionParameters"]
    assert action["BundleIdentifier"] == "com.apple.RunShellScript"
    assert params["inputMethod"] == 1                 # the files as arguments
    assert flow["workflowMetaData"]["workflowTypeIdentifier"] == \
        "com.apple.Automator.servicesMenu"
    assert integration.quick_action_installed()
    assert integration.install_quick_action(app) is False     # unchanged: not rewritten
    integration.remove_quick_action()
    assert not integration.quick_action_installed()


def test_quick_action_script_passes_every_file(mac_home, tmp_path):
    """The script, run with a stand-in for `open`: the app path survives its
    quote and space, every selected file arrives as one argument."""
    shell = shutil.which("zsh") or shutil.which("bash")
    if not shell:
        pytest.skip("no shell")
    app = "/Applications/Cerclic d'Ali.app"
    script = integration.quick_action_command(app)
    fake = tmp_path / "bin"
    fake.mkdir()
    record = tmp_path / "args.txt"
    (fake / "open").write_text(f'#!/bin/sh\nfor a in "$@"; do echo "$a" >> "{record}"; done\n')
    (fake / "open").chmod(0o755)
    script = script.replace("/usr/bin/open", str(fake / "open"))
    files = ["/Users/ali/Photos/été 2026.jpg", "/Users/ali/a b.pdf"]
    subprocess.run([shell, "-c", script, "cerclic", *files], check=True, timeout=20)
    assert record.read_text().splitlines() == ["-a", app, *files]


def test_login_item(mac_home):
    integration.set_autostart(True, app="/Applications/Cerclic.app")
    plist = plistlib.loads(open(integration.launch_agent_path(), "rb").read())
    assert plist["ProgramArguments"][:4] == ["/usr/bin/open", "-g", "-a",
                                             "/Applications/Cerclic.app"]
    assert plist["ProgramArguments"][-1] == "--background" and plist["RunAtLoad"]
    assert integration.is_autostart()
    integration.cleanup()
    assert not integration.is_autostart()


def test_nothing_installed_from_the_sources(mac_home):
    assert integration.app_bundle() is None            # not the packaged app
    assert integration.install_quick_action() is False
    integration.set_autostart(True)
    assert not integration.is_autostart()


# ----- files sent by macOS -------------------------------------------------------------------------

def test_files_sent_by_macos_open_one_wheel(qtbot, jpg_photo, png_with_alpha):
    from PySide6.QtWidgets import QApplication
    from cerclic.app import CerclicApp, FileOpenApp

    class Early:                                  # before Cerclic is ready: kept
        on_file = None
        early_files: list = []
    early = Early()
    assert FileOpenApp.event(early, QFileOpenEvent(jpg_photo)) is True
    assert early.early_files == [jpg_photo]

    a = CerclicApp(QApplication.instance())
    try:
        a._file_opened(jpg_photo)                 # one event per file, in a burst
        a._file_opened(png_with_alpha)
        assert a.session is None                  # gathered first
        qtbot.waitUntil(lambda: a.session is not None, timeout=3000)
        assert sorted(a.session.paths) == sorted([jpg_photo, png_with_alpha])
        assert a.files_received
    finally:
        a.cards.close_all()
        if a.session:
            a.session.close()
        a.server.server.close()
        a.tray.hide()


# ----- settings on a Mac -------------------------------------------------------------------------------

def test_settings_window_as_on_a_mac(qtbot, monkeypatch, tmp_path):
    from cerclic import settings as settings_mod
    from cerclic.ui import settings_window as sw
    monkeypatch.setattr(settings_mod, "_MAC", True)
    monkeypatch.setenv("HOME", str(tmp_path))
    assert settings_mod.config_dir() == os.path.join(str(tmp_path), "Library",
                                                     "Application Support", "Cerclic")
    monkeypatch.setattr(sw, "IS_MAC", True)
    monkeypatch.setattr(sw, "OS_NAME", "macOS")
    monkeypatch.setattr(sw, "FILES_APP", "le Finder")
    monkeypatch.setattr(sw, "hk", mk)
    s = settings_mod.Settings()
    s.set("hotkey_mods", mk.DEFAULT_MODS)
    s.set("hotkey_vk", mk.DEFAULT_VK)
    w = sw.SettingsWindow(s, welcome=True)
    qtbot.addWidget(w)
    w.show()
    assert w.classic is None
    assert "Finder" in w.way_keyboard.text.text() and "Cmd" in w.way_keyboard.text.text()
    assert "Actions rapides" in w.way_mouse.text.text()
    texts = " ".join(lbl.text() for lbl in w.findChildren(sw.QLabel))
    assert "Désinstaller Cerclic" in texts and "Explorateur" not in texts
    # recording a combination the Mac way (Qt names Command "Control")
    edit = w.shortcut
    chosen = []
    edit.chosen.connect(lambda m, v: chosen.append((m, v)))
    edit.start_recording()
    edit.keyPressEvent(QKeyEvent(QEvent.KeyPress, Qt.Key_X,
                                 Qt.ControlModifier | Qt.ShiftModifier, 0, 0x07, 0, "x"))
    assert chosen[-1] == (mk.CMD | mk.SHIFT, mk.vk_of(0x07))
    assert edit.caps.parts == ["Maj", "Cmd", "X"]
    w.close()


def test_finder_gets_the_keyboard_back(qtbot, monkeypatch, jpg_photo):
    """macOS: once the wheel is gone, the Finder is made active again (not while
    Cerclic's own window is open)."""
    from PySide6.QtWidgets import QApplication
    from cerclic import app as app_mod
    from cerclic.mac import foreground
    calls = []
    monkeypatch.setattr(app_mod, "IS_MAC", True)
    monkeypatch.setattr(foreground, "give_back_to_finder", lambda: calls.append(1) or True)
    a = app_mod.CerclicApp(QApplication.instance())
    try:
        a.handle_request("open", [jpg_photo])
        a.session.wheel.cancel()                  # Échap on the wheel
        qtbot.waitUntil(lambda: calls == [1], timeout=2000)
        a.open_settings()
        a.handle_request("open", [jpg_photo])
        a.session.wheel.cancel()
        qtbot.wait(500)
        assert calls == [1]                       # Cerclic's window keeps the keyboard
        a._settings_window().close()
    finally:
        a.cards.close_all()
        if a.session:
            a.session.close()
        a.server.server.close()
        a.tray.hide()


# ----- OpenCV inside Cerclic.app -----------------------------------------------------------

_LOAD_CV2 = r"""
import sys
app, site, hook = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, site)
import numpy                     # the app's own numpy (cv2 needs it)
sys.path.remove(site)
fw = app + "/Contents/Frameworks"
sys.path[:] = [fw] + [p for p in sys.path if "-packages" not in p] + [fw]   # as in the .app
if hook:
    exec(open(hook, encoding="utf-8").read())
import cv2
print("cv2 ok" if hasattr(cv2, "imread") else "cv2 incomplete")
"""


@pytest.mark.skipif(os.name == "nt", reason="symbolic links, as in a .app bundle")
def test_opencv_loads_in_the_app_layout(tmp_path):
    """PyInstaller puts cv2's .py files in Contents/Resources and its binary in
    Contents/Frameworks, each linked into the other: OpenCV's loader then
    imports itself again ("recursion is detected", the "En Word" action failed
    on the Mac) unless scripts/pyi_rth_cv2.py, declared in cerclic_mac.spec,
    runs first."""
    import sys
    cv2 = pytest.importorskip("cv2")
    src = os.path.dirname(os.path.realpath(cv2.__file__))
    site = os.path.dirname(src)
    contents = tmp_path / "Cerclic.app" / "Contents"
    fw, res = contents / "Frameworks" / "cv2", contents / "Resources" / "cv2"
    fw.mkdir(parents=True)
    res.mkdir(parents=True)
    for name in os.listdir(src):
        p = os.path.join(src, name)
        if name.startswith("cv2") and name.endswith((".so", ".pyd")):
            os.symlink(p, fw / name)                     # binary: Frameworks
            os.symlink(fw / name, res / name)
        elif os.path.isdir(p):
            if name != "__pycache__":
                os.symlink(p, res / name)                # data folder: Resources
                os.symlink(res / name, fw / name)
        elif name.endswith(".py"):
            shutil.copy(p, res / name)                   # .py files: Resources
            os.symlink(res / name, fw / name)
    for libs in os.listdir(site):                        # the wheel's own libraries
        if libs.startswith("opencv") and libs.endswith(".libs"):
            for side in ("Frameworks", "Resources"):
                os.symlink(os.path.join(site, libs), contents / side / libs)

    def run(hook: str) -> str:
        done = subprocess.run([sys.executable, "-I", "-c", _LOAD_CV2,
                               str(tmp_path / "Cerclic.app"), site, hook],
                              capture_output=True, text=True, timeout=120)
        return done.stdout + done.stderr

    hook = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts", "pyi_rth_cv2.py")
    assert "recursion is detected" in run("")            # the layout reproduces the failure
    assert "cv2 ok" in run(hook)                         # and the hook fixes it
    with open(os.path.join(os.path.dirname(hook), "..", "cerclic_mac.spec"), encoding="utf-8") as f:
        assert "pyi_rth_cv2.py" in f.read()
