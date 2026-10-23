"""Interface tests, run off-screen: the wheel, bubbles, editors, cards and the
whole flow from a request to a result card."""
import os

import pytest
from PIL import Image
from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QImage

from cerclic.actions import registry
from conftest import HAS_FFMPEG


@pytest.fixture(autouse=True)
def _close_windows():
    """Close every top-level window a test left open (several delete themselves
    on close, so they are not registered with qtbot.addWidget)."""
    yield
    from PySide6.QtWidgets import QApplication
    for w in QApplication.topLevelWidgets():
        try:
            w.close()
        except RuntimeError:
            pass
    QApplication.processEvents()


# ---- wheel ---------------------------------------------------------------------------

def _wheel(qtbot, paths):
    from cerclic.ui.radial import Wheel
    w = Wheel(registry.menu_for(paths), registry.count_by_category(paths), "test")
    w.popup_at(QPoint(400, 400))
    return w


def _click_slice(qtbot, w, label):
    idx = next(i for i, s in enumerate(w._slices) if s.label.startswith(label))
    pos = w.slice_center(idx).toPoint()
    qtbot.mouseMove(w, pos)
    qtbot.mouseClick(w, Qt.LeftButton, pos=pos)


def test_wheel_single_category_shows_actions(qtbot, jpg_photo):
    w = _wheel(qtbot, [jpg_photo])
    labels = [s.label for s in w._slices]
    assert labels == ["Rogner", "Réseaux", "Pivoter", "Redimensionner", "Compresser",
                      "Convertir", "En PDF", "Plus"]
    assert all(s.desc for s in w._slices)              # every action says what it does
    _click_slice(qtbot, w, "Plus")
    assert [s.label for s in w._slices] == ["Copier", "Anonymiser"]


def test_wheel_slices_are_where_they_are_drawn(qtbot, jpg_photo):
    w = _wheel(qtbot, [jpg_photo])
    for i in range(len(w._slices)):
        assert w.index_at(w.slice_center(i)) == i
    top = w._c() + QPoint(0, -100)                      # first slice is at the top
    assert w.index_at(top) == 0


def test_wheel_choice_flow(qtbot, jpg_photo):
    w = _wheel(qtbot, [jpg_photo])
    with qtbot.waitSignal(w.chosen, timeout=2000) as sig:
        _click_slice(qtbot, w, "Pivoter")
        assert [s.label for s in w._slices] == ["Droite", "Gauche", "180°", "Miroir"]
        _click_slice(qtbot, w, "Gauche")
    assert sig.args == ["img_rotate", {"degrees": 270}]


def test_wheel_menus_per_family(qtbot, jpg_photo, pdf_3p, pdf_2p, small_video, tmp_path):
    from cerclic.actions.registry import menu_for
    two_images = [jpg_photo, str(tmp_path / "b.png")]
    Image.new("RGB", (40, 30)).save(two_images[1])
    labels = lambda paths, cat: [a.label for a in menu_for(paths)[cat]]
    assert "Assembler" in labels(two_images, "image")
    assert "Rogner" not in labels(two_images, "image") and "Copier" not in labels(two_images, "image")
    assert "Fusionner" in labels([pdf_3p, pdf_2p], "pdf")
    assert "Pages" in labels([pdf_3p], "pdf") and "Signer" in labels([pdf_3p], "pdf")
    assert labels([small_video], "video")[0] == "Raccourcir"
    song = tmp_path / "note.m4a"
    song.write_bytes(b"x")
    assert labels([str(song)], "audio") == ["Raccourcir", "En MP3", "Compresser"]


def test_wheel_shows_a_preview_of_the_file(qtbot, jpg_photo):
    w = _wheel(qtbot, [jpg_photo])
    w._load_preview(jpg_photo)
    qtbot.waitUntil(lambda: w._thumb is not None, timeout=5000)


def test_wheel_categories_more_and_back(qtbot, jpg_photo, pdf_3p):
    w = _wheel(qtbot, [jpg_photo, pdf_3p])
    assert [s.kind for s in w._slices] == ["category", "category"]
    _click_slice(qtbot, w, "PDF")
    assert "Plus" in [s.label for s in w._slices]
    _click_slice(qtbot, w, "Plus")
    assert "Protéger" in [s.label for s in w._slices]
    # centre = back, twice, then the categories again
    centre = w._c().toPoint()
    qtbot.mouseClick(w, Qt.LeftButton, pos=centre)
    qtbot.mouseClick(w, Qt.LeftButton, pos=centre)
    assert [s.kind for s in w._slices] == ["category", "category"]
    with qtbot.waitSignal(w.cancelled, timeout=2000):
        qtbot.mouseClick(w, Qt.LeftButton, pos=centre)


def test_wheel_keyboard(qtbot, pdf_3p):
    w = _wheel(qtbot, [pdf_3p])
    with qtbot.waitSignal(w.chosen, timeout=2000) as sig:
        qtbot.keyClick(w, Qt.Key_3)          # third slice: Compresser
    assert sig.args[0] == "pdf_compress"


def test_wheel_escape_cancels(qtbot, pdf_3p):
    w = _wheel(qtbot, [pdf_3p])
    with qtbot.waitSignal(w.cancelled, timeout=2000):
        qtbot.keyClick(w, Qt.Key_Escape)


def test_wheel_release_without_press_does_nothing(qtbot, jpg_photo):
    """The release of the click that chose the menu entry must not pick a slice."""
    w = _wheel(qtbot, [jpg_photo])
    fired = []
    w.chosen.connect(lambda *a: fired.append(a))
    qtbot.mouseRelease(w, Qt.LeftButton, pos=w.slice_center(0).toPoint())
    assert fired == [] and w.isVisible()


def test_wheel_merges_more_files(qtbot, jpg_photo, pdf_3p):
    w = _wheel(qtbot, [jpg_photo])
    w.set_menu(registry.menu_for([jpg_photo, pdf_3p]),
               registry.count_by_category([jpg_photo, pdf_3p]), "2 fichiers")
    assert [s.kind for s in w._slices] == ["category", "category"]


def test_wheel_render(qtbot, jpg_photo, pdf_3p, tmp_path):
    """Paint every level: catches painting errors."""
    w = _wheel(qtbot, [jpg_photo, pdf_3p])
    for _ in range(3):
        img = QImage(w.size(), QImage.Format_ARGB32)
        img.fill(0xFF505560)
        w._grow = w._fade = 1.0
        w.render(img)
        assert not img.isNull()
        if w._slices and w._slices[0].kind == "category":
            _click_slice(qtbot, w, "PDF")
        elif "Plus" in [s.label for s in w._slices]:
            _click_slice(qtbot, w, "Plus")


# ---- bubble -----------------------------------------------------------------------------

def test_bubble_accept_and_cancel(qtbot):
    from cerclic.ui.bubble import PromptBubble
    b = PromptBubble("Mot de passe", "test", password=True)
    b.popup_at(QPoint(300, 300))
    assert not b.ok.isEnabled()
    qtbot.keyClicks(b.edit, "secret")
    with qtbot.waitSignal(b.accepted, timeout=2000) as sig:
        qtbot.keyClick(b.edit, Qt.Key_Return)
    assert sig.args == ["secret"]
    b2 = PromptBubble("Texte", default="CONFIDENTIEL")
    b2.popup_at(QPoint(300, 300))
    with qtbot.waitSignal(b2.cancelled, timeout=2000):
        qtbot.keyClick(b2.edit, Qt.Key_Escape)


# ---- crop canvas & editor ------------------------------------------------------------------

def _canvas(qtbot, full=(1000, 500)):
    from cerclic.ui.crop_editor import MARGIN, CropCanvas
    c = CropCanvas()
    qtbot.addWidget(c)
    c.resize(1000 + 2 * MARGIN, 500 + 2 * MARGIN)    # 1000x500 view at scale 1
    img = QImage(100, 50, QImage.Format_RGB32)
    img.fill(0xFF336699)
    c.set_image(img, full)
    c.show()
    return c


def _drag(qtbot, w, a, b):
    qtbot.mousePress(w, Qt.LeftButton, pos=QPoint(*a))
    qtbot.mouseMove(w, QPoint((a[0] + b[0]) // 2, (a[1] + b[1]) // 2))
    qtbot.mouseMove(w, QPoint(*b))
    qtbot.mouseRelease(w, Qt.LeftButton, pos=QPoint(*b))


def test_canvas_starts_full_and_corner_drag(qtbot):
    c = _canvas(qtbot)
    assert c.pixel_box() == (0, 0, 1000, 500)
    v, s = c._view()
    assert abs(s - 1.0) < 1e-6
    # drag the top-left corner by (+100, +50) screen px = source px at scale 1
    tl = (int(v.left()), int(v.top()))
    _drag(qtbot, c, tl, (tl[0] + 100, tl[1] + 50))
    assert c.pixel_box() == (100, 50, 1000, 500)


def test_canvas_edge_move_and_bounds(qtbot):
    c = _canvas(qtbot)
    v, _ = c._view()
    right_mid = (int(v.right()), int(v.center().y()))
    _drag(qtbot, c, right_mid, (right_mid[0] - 300, right_mid[1]))
    assert c.pixel_box() == (0, 0, 700, 500)
    # move inside, far to the right: stays inside the picture
    inside = (int(v.left()) + 300, int(v.top()) + 250)
    _drag(qtbot, c, inside, (inside[0] + 900, inside[1] + 900))
    assert c.pixel_box() == (300, 0, 1000, 500)


def test_canvas_aspect_presets(qtbot):
    c = _canvas(qtbot)
    c.set_aspect(1.0)
    l, t, r, b = c.pixel_box()
    assert (r - l) == (b - t) == 500
    v, _ = c._view()
    s = c.to_view(c.sel)
    _drag(qtbot, c, (int(s.right()), int(s.bottom())), (int(s.right()) - 200, int(s.bottom()) - 50))
    l, t, r, b = c.pixel_box()
    assert abs((r - l) - (b - t)) <= 1


def test_canvas_new_selection_outside(qtbot):
    c = _canvas(qtbot)
    v, _ = c._view()
    right_mid = (int(v.right()), int(v.center().y()))
    _drag(qtbot, c, right_mid, (right_mid[0] - 500, right_mid[1]))      # frame = left half
    start = (int(v.left()) + 700, int(v.top()) + 100)                     # outside the frame
    _drag(qtbot, c, start, (start[0] + 200, start[1] + 150))
    assert c.pixel_box() == (700, 100, 900, 250)


def test_crop_editor_image_end_to_end(qtbot, jpg_rotated_exif):
    from cerclic.ui.crop_editor import CropEditor
    ed = CropEditor(jpg_rotated_exif)
    ed.start()
    qtbot.waitUntil(lambda: ed.canvas.image is not None, timeout=5000)
    assert ed.canvas.full == (200.0, 400.0)          # upright size
    ed.canvas.set_aspect(1.0)
    with qtbot.waitSignal(ed.accepted, timeout=2000) as sig:
        qtbot.keyClick(ed, Qt.Key_Return)
    l, t, r, b = sig.args[0]["crop_box"]
    assert (r - l, b - t) == (200, 200)


def test_crop_editor_pdf_pages(qtbot, pdf_tricky):
    from cerclic.ui.crop_editor import CropEditor
    ed = CropEditor(pdf_tricky)
    ed.start()
    qtbot.waitUntil(lambda: ed.canvas.image is not None, timeout=5000)
    assert ed.page_count == 4
    ed._goto(1)
    qtbot.waitUntil(lambda: ed.canvas.image is not None and ed.page == 1, timeout=5000)
    assert ed.canvas.full == (600.0, 500.0)            # rotated page, offset crop box
    ed.all_pages.setChecked(False)
    with qtbot.waitSignal(ed.accepted, timeout=2000) as sig:
        ed.validate()
    assert sig.args[0]["crop_page"] == 1
    assert sig.args[0]["crop_rel"] == (0.0, 0.0, 1.0, 1.0)


def test_crop_editor_bad_file_shows_message(qtbot, tmp_path):
    from cerclic.ui.crop_editor import CropEditor
    bad = tmp_path / "bad.jpg"
    bad.write_bytes(b"not an image")
    ed = CropEditor(str(bad))
    ed.start()
    qtbot.waitUntil(lambda: ed.canvas.message not in ("Chargement…", ""), timeout=5000)
    assert not ed.ok_btn.isEnabled()


# ---- signature ---------------------------------------------------------------------------------

def test_signature_pad_draw_and_save(qtbot):
    from cerclic.ui.signature import SignaturePad
    pad = SignaturePad()
    pad.start()
    pad.resize(1200, 700)
    a = pad.pad.area()
    start = QPoint(int(a.left()) + 60, int(a.center().y()))
    qtbot.mousePress(pad.pad, Qt.LeftButton, pos=start)
    for k in range(1, 30):
        qtbot.mouseMove(pad.pad, QPoint(start.x() + k * 12, start.y() + (k % 5) * 6))
    qtbot.mouseRelease(pad.pad, Qt.LeftButton, pos=QPoint(start.x() + 360, start.y()))
    assert pad.ok.isEnabled()
    with qtbot.waitSignal(pad.accepted, timeout=2000) as sig:
        pad.validate()
    path = sig.args[0]["signature"]
    with Image.open(path) as im:
        assert im.mode == "RGBA"
        assert im.getchannel("A").getextrema() == (0, 255)
        assert im.width > im.height


def test_import_signature_photo(tmp_path):
    from cerclic.ui.signature import import_signature
    photo = Image.new("RGB", (800, 400), (235, 233, 228))       # paper
    for x in range(100, 700):
        for dy in range(-4, 5):
            photo.putpixel((x, 200 + int(40 * ((x % 80) / 80 - 0.5)) + dy), (20, 25, 60))
    src = tmp_path / "photo_signature.jpg"
    photo.save(src, quality=92)
    out = import_signature(str(src), str(tmp_path / "sig.png"))
    with Image.open(out) as im:
        assert im.mode == "RGBA"
        assert im.width < 700 and im.height < 150              # trimmed to the ink
        assert im.getpixel((2, 2))[3] < 30                      # paper is transparent


def test_sign_placer_flow(qtbot, pdf_3p, signature_png):
    from cerclic.ui.signature import SignPlacer
    ed = SignPlacer(pdf_3p, signature_png)
    ed.start()
    qtbot.waitUntil(lambda: ed.canvas.page_img is not None, timeout=5000)
    assert ed.page == 2                                        # last page first
    before = ed.canvas.rel_box()
    r = ed.canvas.box_view()
    _drag(qtbot, ed.canvas, (int(r.center().x()), int(r.center().y())),
          (int(r.center().x()) - 200, int(r.center().y()) - 300))
    after = ed.canvas.rel_box()
    assert after[0] < before[0] and after[1] < before[1]
    with qtbot.waitSignal(ed.accepted, timeout=2000) as sig:
        ed.validate()
    res = sig.args[0]
    assert res["page"] == 2 and res["signature"] == signature_png
    x0, y0, x1, y1 = res["sig_box"]
    assert 0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1


# ---- cards & settings -------------------------------------------------------------------------------

def test_job_card_states(qtbot, tmp_path):
    from cerclic.engine import Result
    from cerclic.ui.cards import CardStack, JobCard
    stack = CardStack()
    out = tmp_path / "x (compressed).jpg"
    out.write_bytes(b"x")
    ok = JobCard("Compresser")
    stack.add(ok)
    ok.set_progress(0.4, "Fichier 1 sur 2")
    ok.set_progress(None, "Compression")
    ok.finish(Result("img_compress", True, [str(out)]))
    err = JobCard("Signer")
    stack.add(err)
    err.finish(Result("pdf_sign", False, [], "Mot de passe incorrect."))
    info = JobCard("Compresser")
    stack.add(info)
    info.finish(Result("img_compress", False, [], "Déjà compressée.", info=True))
    assert ok.y() < err.y() < info.y() or ok.y() > err.y()       # stacked, not overlapping
    ok._undo()
    assert not out.exists()
    stack.close_all()


def test_settings_window_applies_at_once(qtbot):
    from cerclic.settings import Settings
    from cerclic.ui.settings_window import SettingsWindow
    s = Settings()
    w = SettingsWindow(s)
    qtbot.addWidget(w)
    seen = []
    w.changed.connect(seen.append)
    w.hotkey_on.setChecked(False)
    w.compress_q.setValue(55)
    again = Settings.load()
    assert again.get("hotkey") is False and again.get("compress_quality") == 55
    assert "hotkey" in seen and "compress_quality" in seen
    assert not w.shortcut.isEnabled()


def test_shortcut_recorder(qtbot):
    from cerclic.settings import Settings
    from cerclic.ui.settings_window import SettingsWindow
    from cerclic.win import hotkey as hk
    s = Settings()
    w = SettingsWindow(s)
    qtbot.addWidget(w)
    w.show()
    pauses = []
    w.capturing.connect(pauses.append)
    sc = w.shortcut
    sc.start_recording()
    assert pauses == [True]
    qtbot.keyClick(sc, Qt.Key_C, Qt.ControlModifier)         # refused: copy
    assert sc.recording and "copier" in sc.status.text()
    with qtbot.waitSignal(w.changed, timeout=2000) as sig:
        qtbot.keyClick(sc, Qt.Key_X, Qt.ControlModifier | Qt.ShiftModifier)
    assert sig.args == ["hotkey_combo"]
    assert not sc.recording and pauses == [True, False]
    again = Settings.load()
    assert (again.get("hotkey_mods"), again.get("hotkey_vk")) == \
        (hk.MOD_CONTROL | hk.MOD_SHIFT, 0x58)
    sc.start_recording()
    qtbot.keyClick(sc, Qt.Key_Escape)                         # cancel: unchanged
    assert not sc.recording and Settings.load().get("hotkey_vk") == 0x58
    sc._default()
    assert Settings.load().get("hotkey_vk") == hk.DEFAULT_VK


def test_hotkey_rules():
    from cerclic.win import hotkey as hk
    assert hk.label(hk.DEFAULT_MODS, hk.DEFAULT_VK) == "Ctrl + Alt + Espace"
    assert hk.check(hk.DEFAULT_MODS, hk.DEFAULT_VK) is None
    assert hk.check(hk.MOD_CONTROL | hk.MOD_SHIFT, 0x58) is None      # Ctrl+Maj+X
    assert hk.check(0, 0x77)                                          # F8 alone (Word…)
    assert hk.check(hk.MOD_CONTROL | hk.MOD_ALT, 0x77) is None        # Ctrl+Alt+F8
    assert hk.check(0, 0x7C) is None                                  # F13 (mouse button)
    assert hk.label(hk.MOD_WIN | hk.MOD_SHIFT, 0x43) == "Win + Maj + C"
    assert hk.check(hk.MOD_WIN | hk.MOD_SHIFT, 0x43) is None
    assert hk.check(0, 0x41)                                          # a plain letter
    assert hk.check(hk.MOD_SHIFT, 0x41)                               # a capital letter
    assert hk.check(hk.MOD_CONTROL, 0x56)                             # paste
    assert hk.check(hk.MOD_CONTROL | hk.MOD_ALT, 0x30)                # AltGr+0 = @
    assert hk.check(hk.MOD_CONTROL | hk.MOD_ALT, 0x45)                # AltGr+E = €
    assert hk.check(hk.MOD_ALT, 0x73)                                 # Alt+F4
    assert hk.check(0, 0x74)                                          # F5
    assert hk.check(hk.MOD_CONTROL, 0)                                # no key yet


def test_hello_opens_cerclic_window(qtbot, cerclic_app):
    cerclic_app.handle_request("hello", [])
    win = cerclic_app._settings_window()
    assert win is not None and win.isVisible()
    cerclic_app.handle_request("hello", [])                   # the same window again
    assert cerclic_app._settings_window() is win
    win.close()


# ---- the whole flow -----------------------------------------------------------------------------------

@pytest.fixture
def cerclic_app(qtbot):
    from PySide6.QtWidgets import QApplication
    from cerclic.app import CerclicApp
    app = CerclicApp(QApplication.instance())
    yield app
    app.cards.close_all()
    if app.session:
        app.session.close()
    app.server.server.close()
    app.tray.hide()


def _accept_compress(qtbot, app):
    """« Compresser » now asks how much: take what it proposes."""
    from cerclic.ui.compress_editor import CompressEditor
    qtbot.waitUntil(lambda: any(isinstance(w, CompressEditor) for w in app._live),
                    timeout=5000)
    ed = next(w for w in app._live if isinstance(w, CompressEditor))
    qtbot.waitUntil(ed.ok_btn.isEnabled, timeout=20000)
    ed.validate()


def test_request_opens_wheel_and_runs_action(qtbot, cerclic_app, jpg_photo):
    cerclic_app.handle_request("open", [jpg_photo])
    s = cerclic_app.session
    assert s is not None and s.wheel.isVisible()
    _click_slice(qtbot, s.wheel, "Compresser")
    assert cerclic_app.session is None
    _accept_compress(qtbot, cerclic_app)
    folder = os.path.dirname(jpg_photo)
    qtbot.waitUntil(lambda: any("(compressé)" in f for f in os.listdir(folder)), timeout=8000)
    qtbot.waitUntil(lambda: any(getattr(c, "_outputs", None) for c in cerclic_app.cards._cards),
                    timeout=8000)


def test_burst_of_requests_merges_into_one_wheel(qtbot, cerclic_app, pdf_3p, pdf_2p):
    cerclic_app.handle_request("open", [pdf_3p])
    first = cerclic_app.session
    cerclic_app.handle_request("open", [pdf_2p])
    assert cerclic_app.session is first and len(first.paths) == 2
    qtbot.waitUntil(lambda: "Fusionner" in [s.label for s in first.wheel._slices],
                    timeout=2000)


def test_unsupported_file_shows_card(qtbot, cerclic_app, tmp_path):
    txt = tmp_path / "notes.txt"
    txt.write_text("x")
    cerclic_app.handle_request("open", [str(txt)])
    assert cerclic_app.session is None
    assert cerclic_app.cards._cards


def test_password_flow(qtbot, cerclic_app, pdf_locked):
    from cerclic.ui.bubble import PromptBubble
    cerclic_app.handle_request("open", [pdf_locked])
    _click_slice(qtbot, cerclic_app.session.wheel, "Compresser")
    bubble = next(w for w in cerclic_app._live if isinstance(w, PromptBubble))
    qtbot.keyClicks(bubble.edit, "secret")
    qtbot.keyClick(bubble.edit, Qt.Key_Return)
    _accept_compress(qtbot, cerclic_app)
    folder = os.path.dirname(pdf_locked)
    qtbot.waitUntil(lambda: any(getattr(c, "_outputs", None) or "échoué" in
                                c._head.text() for c in cerclic_app.cards._cards
                                if hasattr(c, "_head")), timeout=8000)
    assert any("locked (compressé)" in f for f in os.listdir(folder)) or \
        any("déjà" in c._status.text() for c in cerclic_app.cards._cards if hasattr(c, "_status"))


def test_dismiss_guard_idle_and_leave(qtbot, monkeypatch):
    """The wheel closes by itself when nobody uses it, or when the pointer left
    it while Cerclic could not take the foreground. Only the popup's own
    events are used: nothing reads the global pointer."""
    from PySide6.QtCore import QEvent
    from PySide6.QtWidgets import QWidget
    from cerclic.ui import dismiss
    assert not hasattr(dismiss, "QCursor")
    w = QWidget()
    w.resize(100, 100)
    w.show()
    hits = []
    g = dismiss.DismissGuard(w, lambda: hits.append("idle"), idle_s=0.3)
    g.start()
    qtbot.waitUntil(lambda: bool(hits), timeout=3000)
    hits.clear()
    g2 = dismiss.DismissGuard(w, lambda: hits.append("leave"), leave_s=0.2, idle_s=60)
    monkeypatch.setattr(w, "isActiveWindow", lambda: False)
    g2.start()
    QApplication_send = __import__("PySide6.QtWidgets", fromlist=["QApplication"]).QApplication
    QApplication_send.sendEvent(w, QEvent(QEvent.Leave))
    qtbot.waitUntil(lambda: bool(hits), timeout=3000)
    assert hits == ["leave"]
    w.close()


def test_big_burst_stays_one_wheel(qtbot, cerclic_app, tmp_path):
    """Explorer starts one forwarder per selected file: 100 requests in a row
    (the right-click limit) all land in the same wheel."""
    files = []
    for i in range(100):
        p = tmp_path / f"photo {i}.jpg"
        Image.new("RGB", (8, 8)).save(p)
        files.append(str(p))
    import time as _time
    t0 = _time.monotonic()
    for f in reversed(files):
        cerclic_app.handle_request("open", [f])
    assert _time.monotonic() - t0 < 2.0
    s = cerclic_app.session
    qtbot.waitUntil(lambda: not s._refresh_pending, timeout=2000)
    assert s is not None and len(s.paths) == 100
    assert os.path.basename(s.paths[2]) == "photo 2.jpg"       # natural order
    assert "100 fichiers" in s.wheel._summary


def test_wrong_password_asks_again_before_editor(qtbot, cerclic_app, pdf_locked):
    from cerclic.ui.bubble import PromptBubble
    from cerclic.ui.crop_editor import CropEditor
    cerclic_app.handle_request("open", [pdf_locked])
    _click_slice(qtbot, cerclic_app.session.wheel, "Rogner")

    def bubble():
        return next((w for w in cerclic_app._live if isinstance(w, PromptBubble)), None)

    first = bubble()
    qtbot.keyClicks(first.edit, "faux")
    qtbot.keyClick(first.edit, Qt.Key_Return)
    qtbot.waitUntil(lambda: bubble() is not None and bubble() is not first, timeout=3000)
    second = bubble()
    from PySide6.QtWidgets import QLabel
    assert "incorrect" in second.findChild(QLabel, "sub").text()
    qtbot.keyClicks(second.edit, "secret")
    qtbot.keyClick(second.edit, Qt.Key_Return)
    qtbot.waitUntil(lambda: any(isinstance(w, CropEditor) for w in cerclic_app._live),
                    timeout=3000)
    editor = next(w for w in cerclic_app._live if isinstance(w, CropEditor))
    qtbot.waitUntil(lambda: editor.canvas.image is not None, timeout=5000)
    editor.cancel()


def test_result_note_only_when_saved_elsewhere(tmp_path, monkeypatch):
    from cerclic import app as app_mod
    src = str(tmp_path / "a" / "x.pdf")
    beside = str(tmp_path / "a" / "x (compressé).pdf")
    inside = str(tmp_path / "a" / "x (images)" / "x 1.jpg")
    assert app_mod._elsewhere_note([src], [beside]) == ""
    assert app_mod._elsewhere_note([src], [inside]) == ""
    assert app_mod._elsewhere_note(["/x.pdf"], ["/x (compressé).pdf"]) == ""   # drive root
    monkeypatch.setattr(app_mod, "fallback_folder", lambda: str(tmp_path / "Downloads"))
    note = app_mod._elsewhere_note([src], [str(tmp_path / "Downloads" / "x (compressé).pdf")])
    assert "Téléchargements" in note and "protégé" in note


def test_shortcut_reads_selection_and_drops_late_answers(qtbot, cerclic_app, monkeypatch,
                                                         jpg_photo, pdf_1p):
    """Ctrl+Alt+Espace: the selection is read off the UI thread; a read stuck on
    a frozen Explorer does not block the shortcut, and its late answer is dropped."""
    import threading
    from cerclic.win import selection
    gate = threading.Event()
    calls = []

    def read():
        calls.append(1)
        if len(calls) == 1:
            gate.wait(5)                # Explorer not answering
            return [pdf_1p]
        return [jpg_photo]

    monkeypatch.setattr(selection, "foreground_selection", read)
    cerclic_app._on_hotkey()
    qtbot.waitUntil(lambda: len(calls) == 1, timeout=2000)
    cerclic_app._on_hotkey()            # ignored: a read is running
    qtbot.wait(100)
    assert len(calls) == 1 and cerclic_app.session is None
    cerclic_app._reading_since -= 10    # ...for too long: the shortcut works again
    cerclic_app._on_hotkey()
    qtbot.waitUntil(lambda: cerclic_app.session is not None, timeout=3000)
    assert cerclic_app.session.paths == [jpg_photo]
    gate.set()
    qtbot.wait(300)
    assert cerclic_app.session.paths == [jpg_photo]


def test_result_card_stays_on_screen(qtbot, tmp_path):
    """The result buttons appear inside the card, and the card stays above the
    bottom of the screen once it has grown."""
    from PySide6.QtWidgets import QPushButton
    from cerclic.engine import Result
    from cerclic.ui.cards import CardStack, JobCard
    stack = CardStack()
    card = JobCard("Compresser")
    stack.add(card)
    qtbot.wait(50)
    before = card.height()
    out = tmp_path / "x (compressed).pdf"
    out.write_bytes(b"x")
    card.finish(Result(action_id="pdf_compress", ok=True, outputs=[str(out)]))
    stack.relayout()                     # what the app does
    qtbot.wait(150)
    geo = card.screen_hint.availableGeometry()
    assert card.height() > before
    assert card.geometry().bottom() <= geo.bottom() + 5   # 16 px of it is shadow
    buttons = [b for b in card.findChildren(QPushButton) if b.isVisible()]
    assert {b.text() for b in buttons} >= {"Ouvrir", "Dossier", "Supprimer", "✕"}
    for b in buttons:
        bottom = b.mapTo(card, b.rect().bottomLeft()).y()
        assert bottom <= card.height() - 16
    # "Supprimer" removes the new file, says so, and leaves the original alone
    [delete] = [b for b in buttons if b.text() == "Supprimer"]
    delete.click()
    assert not out.exists()
    assert card.isVisible() and "supprimé" in card._head.text()
    card.close()


def test_result_card_shortens_a_long_name(qtbot, tmp_path):
    from cerclic.engine import Result
    from cerclic.ui.cards import CardStack, JobCard
    stack = CardStack()
    card = JobCard("Compression")
    stack.add(card)
    name = "Releve_de_compte_janvier_fevrier_mars_avril_mai_juin_definitif (compressed).pdf"
    out = tmp_path / name
    out.write_bytes(b"x")
    card.finish(Result(action_id="pdf_compress", ok=True, outputs=[str(out)]))
    qtbot.wait(50)
    assert "…" in card._status.text() and card._status.toolTip() == name
    assert card.width() <= 360
    card.close()


# ---- 0.3: popups -------------------------------------------------------------------------------

def test_popups_open_small_where_the_wheel_was(qtbot, jpg_photo, pdf_3p):
    from PySide6.QtGui import QGuiApplication
    from cerclic.ui.crop_editor import CropEditor
    from cerclic.ui.editor_base import EDGE, SHADOW
    avail = QGuiApplication.primaryScreen().availableGeometry()
    for path in (jpg_photo, pdf_3p):
        for anchor in (QPoint(avail.center()), QPoint(avail.right() - 5, avail.bottom() - 5),
                       QPoint(avail.left() + 3, avail.top() + 3)):
            ed = CropEditor(path)
            ed.start(anchor)
            card = ed.geometry().adjusted(SHADOW, SHADOW, -SHADOW, -SHADOW)
            assert avail.adjusted(EDGE - 1, EDGE - 1, 1 - EDGE, 1 - EDGE).contains(card), \
                (path, anchor, card)
            assert card.width() < avail.width() * 0.75
            ed.close()
    ed = CropEditor(jpg_photo)
    ed.start(QPoint(avail.center()))
    assert ed.geometry().center().x() == pytest.approx(avail.center().x(), abs=2)
    ed.close()


def test_editor_closed_while_loading_is_safe(qtbot, tmp_path):
    from cerclic.ui.crop_editor import CropEditor
    big = tmp_path / "big.png"
    Image.new("RGB", (5000, 4000), (40, 90, 160)).save(big)
    for _ in range(3):
        ed = CropEditor(str(big))
        ed.start(QPoint(300, 300))
        ed.close()
    qtbot.wait(1500)                                     # the loads finish meanwhile


def test_pages_editor(qtbot, pdf_3p):
    from cerclic.ui.pages_editor import PagesEditor
    ed = PagesEditor(pdf_3p)
    ed.start(QPoint(400, 400))
    assert ed.grid.count() == 3
    qtbot.waitUntil(lambda: len(ed._thumbs) == 3, timeout=5000)
    ed.grid.item(2).setSelected(True)
    ed.move_selection(-1)
    ed.move_selection(-1)                                  # page 3 is now first
    ed.rotate_selection(90)
    assert ed.grid.order() == [(2, 90), (0, 0), (1, 0)]
    ed.grid.clearSelection()
    ed.grid.item(2).setSelected(True)
    qtbot.keyClick(ed, Qt.Key_Delete)                      # remove page 2
    assert ed.grid.order() == [(2, 90), (0, 0)]
    with qtbot.waitSignal(ed.accepted, timeout=2000) as sig:
        qtbot.keyClick(ed, Qt.Key_Return)
    assert sig.args[0] == {"pages_order": [(2, 90), (0, 0)], "pages_mode": "save"}


def test_pages_editor_extract(qtbot, pdf_3p):
    from cerclic.ui.pages_editor import PagesEditor
    ed = PagesEditor(pdf_3p)
    ed.start(QPoint(400, 400))
    assert not ed.extract_btn.isEnabled()
    ed.grid.item(0).setSelected(True)
    ed.grid.item(2).setSelected(True)
    with qtbot.waitSignal(ed.accepted, timeout=2000) as sig:
        ed.extract_btn.click()
    assert sig.args[0] == {"pages_order": [(0, 0), (2, 0)], "pages_mode": "extract"}


@pytest.mark.skipif(not HAS_FFMPEG, reason="ffmpeg missing")
def test_trim_editor_video(qtbot, long_clip):
    from cerclic.ui.trim_editor import TrimEditor, fmt_time
    ed = TrimEditor(long_clip)
    ed.start(QPoint(400, 400))
    qtbot.waitUntil(lambda: ed.track.duration > 3.5, timeout=10000)
    qtbot.waitUntil(lambda: ed.frame.image is not None, timeout=10000)
    t = ed.track
    t.set_range(1.0, 3.0, "start")
    t.setFocus()
    qtbot.keyClick(t, Qt.Key_Right, Qt.ShiftModifier)     # start + 1 s
    assert t.start == pytest.approx(2.0)
    qtbot.keyClick(t, Qt.Key_Tab)                          # now the end handle
    qtbot.keyClick(t, Qt.Key_Left)                         # end - 0.1 s
    assert t.end == pytest.approx(2.9)
    assert "Durée 0:00,9" == ed.length_label.text()
    with qtbot.waitSignal(ed.accepted, timeout=2000) as sig:
        ed.validate()
    assert sig.args[0] == {"trim_start": 2.0, "trim_end": 2.9}
    assert fmt_time(3725.26) == "1:02:05,3"


@pytest.mark.skipif(not HAS_FFMPEG, reason="ffmpeg missing")
def test_trim_editor_sound_and_handles(qtbot, m4a_sound):
    from cerclic.ui.trim_editor import TrimEditor
    ed = TrimEditor(m4a_sound)
    ed.start(QPoint(400, 400))
    assert ed.frame is None
    qtbot.waitUntil(lambda: ed.track.duration > 2.5, timeout=10000)
    qtbot.waitUntil(lambda: ed.track.wave is not None, timeout=10000)
    t = ed.track
    x_end = int(t.x_of(t.end))
    y = t.height() // 2
    qtbot.mousePress(t, Qt.LeftButton, pos=QPoint(x_end, y))
    qtbot.mouseMove(t, QPoint(int(t.x_of(1.5)), y))
    qtbot.mouseRelease(t, Qt.LeftButton, pos=QPoint(int(t.x_of(1.5)), y))
    assert t.end == pytest.approx(1.5, abs=0.05)
    t.set_range(1.4, 1.45, "end")                          # never shorter than 0.2 s
    assert t.end - t.start == pytest.approx(0.2)


def test_copy_image_to_clipboard(qtbot, cerclic_app, jpg_photo):
    from PySide6.QtWidgets import QApplication
    QApplication.clipboard().clear()
    cerclic_app.start_action("img_copy", [jpg_photo], {}, QPoint(300, 300))
    qtbot.waitUntil(lambda: not QApplication.clipboard().image().isNull(), timeout=5000)
    assert QApplication.clipboard().image().width() > 10


def test_pages_flow_end_to_end(qtbot, cerclic_app, pdf_3p):
    from cerclic.ui.pages_editor import PagesEditor
    cerclic_app.handle_request("open", [pdf_3p])
    _click_slice(qtbot, cerclic_app.session.wheel, "Pages")
    qtbot.waitUntil(lambda: any(isinstance(w, PagesEditor) for w in cerclic_app._live),
                    timeout=3000)
    ed = next(w for w in cerclic_app._live if isinstance(w, PagesEditor))
    ed.grid.item(0).setSelected(True)
    ed.remove_selection()
    ed.validate()
    folder = os.path.dirname(pdf_3p)
    qtbot.waitUntil(lambda: any("(réorganisé)" in f for f in os.listdir(folder)), timeout=8000)


def test_used_editor_survives_a_click_elsewhere(qtbot, monkeypatch):
    from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget
    from cerclic.ui import dismiss

    class Inactive:
        @staticmethod
        def applicationState():
            return Qt.ApplicationInactive
    monkeypatch.setattr(dismiss, "QGuiApplication", Inactive)
    w = QWidget()
    lay = QVBoxLayout(w)
    button = QPushButton("x")
    lay.addWidget(button)
    w.show()
    hits = []
    fresh = dismiss.DismissGuard(w, lambda: hits.append("fresh"), keep_once_used=True)
    fresh.start()
    fresh._shown -= 10                               # past the first moment
    fresh._check_deactivated()                       # opened by mistake: it goes
    assert hits == ["fresh"]
    used = dismiss.DismissGuard(w, lambda: hits.append("used"), keep_once_used=True)
    used.start()
    used._shown -= 10
    qtbot.mouseClick(button, Qt.LeftButton)          # the user worked in it
    used._check_deactivated()
    assert hits == ["fresh"]
    w.close()


def test_recorder_cancel_button_really_cancels(qtbot):
    from cerclic.settings import Settings
    from cerclic.ui.settings_window import SettingsWindow
    w = SettingsWindow(Settings())
    qtbot.addWidget(w)
    w.show()
    sc = w.shortcut
    pauses = []
    w.capturing.connect(pauses.append)
    sc.start_recording()
    qtbot.mouseClick(sc.change_btn, Qt.LeftButton)          # labelled "Annuler"
    assert not sc.recording and pauses == [True, False]
    assert "inchangé" in sc.status.text()


def test_wheel_digits_on_azerty_top_row(qtbot, pdf_3p):
    w = _wheel(qtbot, [pdf_3p])
    with qtbot.waitSignal(w.chosen, timeout=2000) as sig:
        qtbot.keyClick(w, Qt.Key_QuoteDbl)                 # the 3 key on AZERTY
    assert sig.args[0] == "pdf_compress"


def test_pages_editor_ctrl_arrows_move_pages(qtbot, pdf_3p):
    from cerclic.ui.pages_editor import PagesEditor
    ed = PagesEditor(pdf_3p)
    ed.start(QPoint(400, 400))
    ed.grid.setCurrentRow(2)
    ed.grid.item(2).setSelected(True)
    qtbot.keyClick(ed.grid, Qt.Key_Left, Qt.ControlModifier)
    assert [i for i, _ in ed.grid.order()] == [0, 2, 1]
    qtbot.keyClick(ed.grid, Qt.Key_Right, Qt.ControlModifier)
    assert [i for i, _ in ed.grid.order()] == [0, 1, 2]
