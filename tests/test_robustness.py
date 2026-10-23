"""Real-world cases found in the second review: scans in multi-page TIFF,
16-bit pictures, browser recordings without a duration, sounds inside video
files, PDFs with different passwords, files that vanished, long names,
Windows environment for the programs Cerclic starts, and popup behaviour."""
import os
import subprocess
import sys

import pymupdf
import pytest
from PIL import Image
from PySide6.QtCore import QPoint, QRectF, Qt

from cerclic import engine
from cerclic.actions import pdf
from conftest import HAS_FFMPEG

needs_ffmpeg = pytest.mark.skipif(not HAS_FFMPEG, reason="ffmpeg missing")


def _ok(res):
    assert res.ok, res.error
    return res.outputs


# ----- pictures ------------------------------------------------------------------------------

@pytest.fixture
def fax_tiff(tmp_path):
    path = tmp_path / "fax.tif"
    pages = [Image.new("1", (300, 400), 1) for _ in range(3)]
    for i, im in enumerate(pages):
        for x in range(20, 280):
            im.putpixel((x, 50 + 100 * i), 0)
    pages[0].save(path, save_all=True, append_images=pages[1:], compression="group4")
    return str(path)


def test_multipage_tiff_to_pdf_keeps_every_page(fax_tiff):
    out = _ok(engine.run("img_to_pdf", [fax_tiff], {}))[0]
    with pymupdf.open(out) as doc:
        assert doc.page_count == 3


def test_multipage_tiff_edit_says_so_instead_of_dropping_pages(fax_tiff, jpg_photo):
    for action, opts in (("img_rotate", {"degrees": 90}), ("img_compress", {}),
                         ("img_convert", {"fmt": "png"})):
        res = engine.run(action, [fax_tiff], opts)
        assert not res.ok and "3 pages" in res.error and "En PDF" in res.error, action
        assert not res.outputs
    # in a batch, the other pictures are still done and the card says why one is not
    res = engine.run("img_rotate", [jpg_photo, fax_tiff], {"degrees": 90})
    assert res.ok and len(res.outputs) == 1
    assert res.notes and "3 pages" in res.notes[0]


def test_16_bit_grey_png_is_not_turned_white(tmp_path):
    import numpy as np
    src = tmp_path / "radio.png"
    arr = np.tile(np.linspace(0, 65535, 200), (120, 1)).astype("uint16")
    Image.fromarray(arr).save(src)
    out = engine.run("img_compress", [str(src)], {})
    if out.ok:
        with Image.open(out.outputs[0]) as im:
            mean = sum(im.convert("L").getdata()) / (200 * 120)
        assert 80 < mean < 180
    from cerclic.ui.editor_base import qimage_from_pil
    with Image.open(src) as im:
        q = qimage_from_pil(im)
    assert q.pixelColor(5, 60).red() < 60 and q.pixelColor(195, 60).red() > 200


def test_convert_to_its_own_format_is_refused(jpg_photo):
    res = engine.run("img_convert", [jpg_photo], {"fmt": "jpg"})
    assert res.info and "déjà un JPG" in res.error and not res.outputs


# ----- PDF -----------------------------------------------------------------------------------

def _locked(src, dst, password):
    import pikepdf
    with pikepdf.open(src) as p:
        p.save(dst, encryption=pikepdf.Encryption(owner=password, user=password, R=6))
    return str(dst)


def test_merge_with_a_password_per_file(tmp_path, pdf_3p, pdf_2p):
    a = _locked(pdf_3p, tmp_path / "a.pdf", "alpha")
    b = _locked(pdf_2p, tmp_path / "b.pdf", "beta")
    res = engine.run("pdf_merge", [a, b], {"passwords": {a: "alpha", b: "beta"}})
    with pymupdf.open(_ok(res)[0]) as doc:
        assert doc.page_count == 5


def test_page_files_get_short_names(tmp_path, pdf_2p):
    src = tmp_path / ("Contrat de location appartement centre ville signé " * 3 + ".pdf")
    os.replace(pdf_2p, src)
    outs = _ok(engine.run("pdf_split", [str(src)], {}))
    assert all(len(os.path.basename(o)) < 60 for o in outs)


def test_heavy_first_page_gets_no_wheel_preview(tmp_path, pdf_1p):
    assert pdf.quick_to_draw(pdf_1p)
    doc = pymupdf.open()
    page = doc.new_page()
    shape = page.new_shape()
    for i in range(60000):                      # a detailed plan
        shape.draw_line((i % 500, (i * 7) % 800), ((i * 13) % 500, (i * 3) % 800))
    shape.finish(width=0.2)
    shape.commit()
    heavy = tmp_path / "plan.pdf"
    doc.save(str(heavy), deflate=False)
    doc.close()
    assert not pdf.quick_to_draw(str(heavy))


def test_vanished_file_says_so(tmp_path, jpg_photo):
    os.remove(jpg_photo)
    res = engine.run("img_compress", [jpg_photo], {})
    assert not res.ok and "n'est plus là" in res.error


# ----- video and sound ------------------------------------------------------------------------

@needs_ffmpeg
def test_webm_without_duration_is_measured(tmp_path):
    from cerclic.actions import video
    path = tmp_path / "enregistrement.webm"
    with open(path, "wb") as f:                 # written as a stream: no duration
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
                        "-i", "testsrc=size=320x240:rate=15:duration=3",
                        "-c:v", "libvpx", "-b:v", "200k", "-f", "webm", "pipe:1"],
                       stdout=f, check=True)
    info = video.probe(str(path))
    assert 2.5 < info.duration < 3.5


@needs_ffmpeg
def test_sound_inside_a_video_file(tmp_path):
    from cerclic.actions import video
    path = tmp_path / "musique.mp4"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
                    "-i", "sine=frequency=330:duration=3", "-c:a", "aac", str(path)],
                   check=True)
    out = _ok(engine.run("vid_trim", [str(path)], {"trim_start": 0.5, "trim_end": 2.0}))[0]
    assert out.endswith(".mp3") and 1.2 < video.probe(out).duration < 1.8
    gif = engine.run("vid_gif", [str(path)], {})
    assert not gif.ok and "que du son" in gif.error


@needs_ffmpeg
def test_preview_stops_with_its_popup(tmp_path):
    import threading
    import time
    from cerclic.actions import video
    from cerclic.errors import Cancelled
    long_sound = tmp_path / "podcast.wav"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
                    "-i", "sine=frequency=200:duration=1800:sample_rate=22050",
                    str(long_sound)], check=True)
    stop = threading.Event()
    threading.Timer(0.3, stop.set).start()          # the popup closes
    t0 = time.monotonic()
    with pytest.raises(Cancelled):
        video.waveform_png(str(long_sound), 800, 80, should_stop=stop.is_set)
    assert time.monotonic() - t0 < 2.0              # ffmpeg was stopped, not waited for


# ----- Windows environment for programs Cerclic starts -----------------------------------------

def test_programs_started_by_cerclic_get_a_clean_environment(monkeypatch, tmp_path):
    from cerclic import sysenv
    app = tmp_path / "Cerclic"
    internal = app / "_internal"
    internal.mkdir(parents=True)
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "_MEIPASS", str(internal), raising=False)
    monkeypatch.setattr(sys, "executable", str(app / "Cerclic.exe"))
    base = {"PATH": os.pathsep.join([str(internal), "/usr/bin", str(internal / "PySide6")]),
            "QT_PLUGIN_PATH": str(internal / "PySide6" / "plugins"),
            "QML2_IMPORT_PATH": "x", "_PYI_APPLICATION_HOME_DIR": str(app),
            "HOME": "/home/me"}
    env = sysenv.clean_env(base)
    assert env["PATH"] == "/usr/bin" and env["HOME"] == "/home/me"
    assert not {"QT_PLUGIN_PATH", "QML2_IMPORT_PATH", "_PYI_APPLICATION_HOME_DIR"} & set(env)
    monkeypatch.setenv("QT_PLUGIN_PATH", "x")
    with sysenv.outside_env():
        assert "QT_PLUGIN_PATH" not in os.environ
    assert os.environ["QT_PLUGIN_PATH"] == "x"


def test_relative_paths_are_resolved_before_handing_over(monkeypatch, tmp_path):
    from cerclic import launcher
    sent = {}
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(launcher, "send",
                        lambda cmd, paths, timeout=4.0: sent.update(cmd=cmd, paths=paths) or True)
    launcher.main(["photo.jpg", '"C:/x/y.pdf"'])
    assert sent["paths"][0] == str(tmp_path / "photo.jpg")
    assert not sent["paths"][1].startswith('"')


# ----- popups and wheel ----------------------------------------------------------------------------

def test_popup_that_grows_stays_on_screen(qtbot, jpg_photo):
    from PySide6.QtGui import QGuiApplication
    from cerclic.ui.crop_editor import CropEditor
    from cerclic.ui.editor_base import EDGE, SHADOW
    avail = QGuiApplication.primaryScreen().availableGeometry()
    ed = CropEditor(jpg_photo)
    ed.start(QPoint(avail.right() - 3, avail.center().y()))
    qtbot.waitUntil(lambda: ed.canvas.image is not None, timeout=5000)
    ed.resize(ed.width() + 120, ed.height())        # a longer label, a new page...
    qtbot.wait(50)
    assert ed.geometry().right() - SHADOW <= avail.right() - EDGE + 1
    ed.cancel()


def test_pdf_crop_frame_survives_page_changes(qtbot, tmp_path):
    from cerclic.ui.crop_editor import CropEditor
    doc = pymupdf.open()
    doc.new_page(width=595, height=842)
    doc.new_page(width=842, height=595)              # a landscape annex
    doc.new_page(width=595, height=842)
    path = tmp_path / "mix.pdf"
    doc.save(str(path))
    doc.close()
    ed = CropEditor(str(path))
    ed.start(QPoint(600, 400))
    qtbot.waitUntil(lambda: ed.canvas.image is not None, timeout=5000)
    ed._preset(1.0, ed._preset_btns[2])              # 1:1
    ed.canvas.sel = QRectF(100, 100, 200, 200)
    ed._goto(1)
    ed._goto(2)                                      # quickly, while page 2 loads
    qtbot.waitUntil(lambda: ed.canvas.image is not None and ed.page == 2, timeout=5000)
    x0, y0, x1, y1 = ed.canvas.rel_box()
    assert x1 - x0 < 0.6                             # not reset to the whole page
    w, h = (x1 - x0) * ed.canvas.full[0], (y1 - y0) * ed.canvas.full[1]
    assert abs(w / h - 1.0) < 0.02                   # still square
    ed.cancel()


def test_signature_keeps_its_shape_on_a_page_of_another_size(qtbot, tmp_path, signature_png):
    from cerclic.ui.signature import SignPlacer
    doc = pymupdf.open()
    doc.new_page(width=595, height=842)
    doc.new_page(width=842, height=595)              # opens on this one (last page)
    path = tmp_path / "contrat.pdf"
    doc.save(str(path))
    doc.close()
    sp = SignPlacer(str(path), signature_png)
    sp.start(QPoint(600, 400))
    qtbot.waitUntil(lambda: sp.canvas.page_img is not None, timeout=5000)
    sp._goto(0)
    qtbot.waitUntil(lambda: sp.canvas.page_img is not None and sp.page == 0, timeout=5000)
    b = sp.canvas.box
    W, H = sp.canvas.page_size
    ratio = (b.width() * W) / (b.height() * H)
    assert abs(ratio - 400 / 160) < 0.05            # the signature's own proportions
    sp.cancel()


def test_password_bubble_enter_after_tab(qtbot):
    from cerclic.ui.bubble import PromptBubble
    b = PromptBubble("Mot de passe du PDF", password=True, ok_label="Continuer")
    got = []
    b.accepted.connect(got.append)
    b.popup_at(QPoint(400, 300))
    qtbot.keyClicks(b.edit, "secret")
    qtbot.keyClick(b.edit, Qt.Key_Tab)
    qtbot.keyClick(b.focusWidget() or b, Qt.Key_Return)
    assert got == ["secret"]


def _app():
    from PySide6.QtWidgets import QApplication
    from cerclic.app import CerclicApp
    return CerclicApp(QApplication.instance())


def _close(a):
    a.cards.close_all()
    if a.session:
        a.session.close()
    a.server.server.close()
    a.tray.hide()


def test_late_files_join_an_untouched_wheel(qtbot, pdf_3p, pdf_2p, pdf_1p):
    a = _app()
    try:
        a.handle_request("open", [pdf_3p])
        first = a.session
        first.last_add -= 3.0            # Cerclic was busy: the rest comes late
        a.handle_request("open", [pdf_2p])
        assert a.session is first and len(first.paths) == 2
        first.wheel._touched = True      # once the user points at it: a new wheel
        first.last_add -= 3.0
        a.handle_request("open", [pdf_1p])
        assert a.session is not first and a.session.paths == [pdf_1p]
    finally:
        _close(a)


def test_new_shortcut_taken_keeps_the_old_one(qtbot):
    from PySide6.QtWidgets import QLabel
    from cerclic.win import hotkey as hk

    class FakeHotkey:
        def __init__(self, mods, vk):
            self.mods, self.vk = mods, vk

        def stop(self):
            pass

    a = _app()
    try:
        a.hotkey = FakeHotkey(hk.DEFAULT_MODS, hk.DEFAULT_VK)
        a._on_hotkey_status(a._hk_serial, True)        # the default works
        assert a._good_combo == (hk.DEFAULT_MODS, hk.DEFAULT_VK)
        new = (hk.MOD_CONTROL | hk.MOD_SHIFT, 0x58)
        a.settings.set("hotkey_mods", new[0])
        a.settings.set("hotkey_vk", new[1])
        a._trying = a._good_combo                       # what choosing it does
        a.hotkey = FakeHotkey(*new)
        a._on_hotkey_status(a._hk_serial, False)       # Ctrl + Maj + X is taken
        assert (a.settings.get("hotkey_mods"), a.settings.get("hotkey_vk")) == \
            (hk.DEFAULT_MODS, hk.DEFAULT_VK)
        texts = [lbl.text() for c in a.cards._cards for lbl in c.findChildren(QLabel)]
        assert any("Ctrl + Maj + X" in t for t in texts)
        assert any("reste Ctrl + Alt + Espace" in t for t in texts)
        # a late answer about a replaced registration changes nothing
        a._good_combo = (1, 2)
        a._on_hotkey_status(a._hk_serial - 1, True)
        assert a._good_combo == (1, 2)
    finally:
        _close(a)


def test_recycle_bin_items_are_ignored(tmp_path):
    from cerclic.paths import clean_selection
    binned = tmp_path / "$Recycle.Bin" / "S-1-5-21" / "$RXK3Y2.jpg"
    binned.parent.mkdir(parents=True)
    binned.write_bytes(b"x")
    real = tmp_path / "photo.jpg"
    real.write_bytes(b"x")
    assert clean_selection([str(binned), str(real)]) == [str(real)]


def test_delete_that_fails_says_so(qtbot, tmp_path, monkeypatch):
    from cerclic.engine import Result
    from cerclic.ui import cards
    out = tmp_path / "x (compressed).pdf"
    out.write_bytes(b"x")
    card = cards.JobCard("Compression")
    card.finish(Result(action_id="pdf_compress", ok=True, outputs=[str(out)]))

    def locked(path):
        raise PermissionError(32, "used by another process")
    monkeypatch.setattr(cards.os, "remove", locked)
    card._undo()
    assert out.exists() and "impossible" in card._head.text()
    card.close()


def test_portable_keeps_its_settings_beside_it(tmp_path, monkeypatch):
    from cerclic import settings as st
    exe = tmp_path / "Cerclic" / "Cerclic.exe"
    exe.parent.mkdir()
    exe.write_bytes(b"")
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "executable", str(exe))
    monkeypatch.setattr(st, "_portable_dir", None)
    assert st.is_portable()
    assert st.config_dir() == str(tmp_path / "Cerclic" / st.PORTABLE_DATA)
    (exe.parent / "unins000.exe").write_bytes(b"")          # installed: %APPDATA%
    assert not st.is_portable() and st.PORTABLE_DATA not in st.config_dir()
    (exe.parent / "unins000.exe").unlink()
    monkeypatch.setattr(st, "_MAC", True)                    # Cerclic.app: never written in
    assert not st.is_portable()


def test_password_retry_uses_the_new_password(tmp_path, pdf_3p):
    import pikepdf
    src = tmp_path / "ancien.pdf"
    with pikepdf.open(pdf_3p) as p:          # AES-128: an accented password
        p.save(str(src), encryption=pikepdf.Encryption(owner="café", user="café", R=4))
    res = engine.run("pdf_unlock", [str(src)], {"passwords": {str(src): "café"}})
    assert res.ok, res.error
