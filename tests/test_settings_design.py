"""The settings window (sidebar, pages, switches), where results are saved,
and the new logo."""
import os

from PySide6.QtCore import QPoint, Qt

from cerclic import engine


def test_results_go_to_the_chosen_folder(tmp_path, jpg_photo):
    chosen = tmp_path / "Mes créations"
    res = engine.run("img_rotate", [jpg_photo], {"degrees": 90, "_out_dir": str(chosen)})
    assert res.ok, res.error
    assert os.path.dirname(res.outputs[0]) == str(chosen)      # created on the way
    res = engine.run("img_rotate", [jpg_photo], {"degrees": 90})
    assert os.path.dirname(res.outputs[0]) == os.path.dirname(jpg_photo)


def test_chosen_folder_unavailable_falls_back_beside(tmp_path, jpg_photo):
    blocker = tmp_path / "fichier"
    blocker.write_text("x")                                     # not a folder
    res = engine.run("img_rotate", [jpg_photo],
                     {"degrees": 90, "_out_dir": str(blocker / "sous-dossier")})
    assert res.ok and os.path.dirname(res.outputs[0]) == os.path.dirname(jpg_photo)
    from cerclic import app as app_mod
    note = app_mod._elsewhere_note([jpg_photo], res.outputs, str(blocker / "sous-dossier"))
    assert "introuvable" in note


def test_card_says_where_the_file_is(qtbot, tmp_path):
    from cerclic.engine import Result
    from cerclic.ui.cards import JobCard, folder_label
    desk = tmp_path / "Desktop"
    desk.mkdir()
    out = desk / "photo (compressed).jpg"
    out.write_bytes(b"x")
    assert folder_label([str(out)]) == "Bureau"
    card = JobCard("Compression")
    card.finish(Result(action_id="img_compress", ok=True, outputs=[str(out)]))
    assert "Bureau" in card._status.text()
    card.close()


def test_settings_pages_and_output_choice(qtbot, monkeypatch, tmp_path):
    from cerclic.settings import Settings
    from cerclic.ui import settings_window as sw
    s = Settings()
    w = sw.SettingsWindow(s, windows_11=True, welcome=True)
    qtbot.addWidget(w)
    w.show()
    for key, *_ in sw.PAGES:                         # every section opens
        w.show_page(key)
        assert w.stack.currentWidget() is w.pages[key]
        assert w.nav[key].isChecked()
    # "in a folder of my choice", the folder dialog cancelled: stays beside
    monkeypatch.setattr(sw.QFileDialog, "getExistingDirectory", lambda *a, **k: "")
    w.out_folder.click()
    assert Settings.load().get("output_mode") == "beside" and w.out_beside.isChecked()
    # a folder picked: saved, shown
    target = tmp_path / "Créations"
    target.mkdir()
    monkeypatch.setattr(sw.QFileDialog, "getExistingDirectory", lambda *a, **k: str(target))
    w.out_folder.click()
    again = Settings.load()
    assert again.get("output_mode") == "folder"
    assert again.get("output_folder") == os.path.normpath(str(target))
    assert str(target) in w.folder_label.text()
    w.out_beside.click()
    assert Settings.load().get("output_mode") == "beside"
    w.out_ask.click()                                # « Me demander à chaque fois »
    assert Settings.load().get("output_mode") == "ask"
    again = sw.SettingsWindow(Settings.load())
    qtbot.addWidget(again)
    assert again.out_ask.isChecked()


def test_switch_is_a_checkbox(qtbot):
    from cerclic.ui.glass import Toggle
    t = Toggle("Essai")
    qtbot.addWidget(t)
    t.show()
    seen = []
    t.toggled.connect(seen.append)
    qtbot.mouseClick(t, Qt.LeftButton, pos=QPoint(t.width() // 2, t.height() // 2))
    assert t.isChecked() and seen == [True]
    t.setChecked(False)
    assert not t.isChecked()


def test_quality_sliders_save(qtbot):
    from cerclic.settings import Settings
    from cerclic.ui.settings_window import SettingsWindow
    w = SettingsWindow(Settings())
    qtbot.addWidget(w)
    w.jpg_q.setValue(80)
    assert Settings.load().get("jpg_quality") == 80 and w.jpg_val.text() == "80 %"
    w._quality_defaults()
    assert Settings.load().get("jpg_quality") == 90


def test_logo_reads_at_every_size(qtbot):
    from PySide6.QtGui import QColor
    from cerclic.ui.logo import logo_pixmap
    for size in (16, 24, 32, 256):
        img = logo_pixmap(size).toImage()
        centre = img.pixelColor(size // 2, size // 2)
        assert centre.alpha() > 200 and centre.blue() > centre.red()     # the blue dot
        corner = img.pixelColor(0, 0)
        assert corner.alpha() == 0                                       # transparent
    mono = logo_pixmap(18, mono=QColor(0, 0, 0)).toImage()
    assert mono.pixelColor(9, 9).alpha() > 200


def test_result_names_are_french(jpg_photo):
    res = engine.run("img_compress", [jpg_photo], {"quality": 60})
    assert res.ok and os.path.basename(res.outputs[0]) == "photo (compressé).jpg"


def test_password_bubble_waits_while_the_user_fetches_it(qtbot, monkeypatch):
    from PySide6.QtWidgets import QLineEdit
    from cerclic.ui import dismiss
    from cerclic.ui.bubble import PromptBubble
    b = PromptBubble("Mot de passe du PDF", "« contrat.pdf » est protégé.", password=True)
    gone = []
    b.cancelled.connect(lambda: gone.append(True))
    b.popup_at(QPoint(300, 300))
    # the eye inside the field shows, then hides, the password
    assert b.edit.echoMode() == QLineEdit.Password
    b.eye.trigger()
    assert b.edit.echoMode() == QLineEdit.Normal
    b.eye.trigger()
    assert b.edit.echoMode() == QLineEdit.Password
    # going to another window (to copy the password from a mail) keeps it open
    monkeypatch.setattr(dismiss.QGuiApplication, "applicationState",
                        staticmethod(lambda: Qt.ApplicationInactive))
    b._guard._shown -= 10
    b._guard._check_deactivated()
    b._guard._left_at = 0.0
    b._guard._tick()
    assert not gone and b.isVisible()
    b.cancel()                                      # Échap or Annuler: it goes
    assert gone == [True]


def test_settings_help_is_plain_text_and_buttons_honest(qtbot, monkeypatch, tmp_path):
    from cerclic.settings import Settings
    from cerclic.ui import settings_window as sw
    w = sw.SettingsWindow(Settings(), windows_11=True)
    qtbot.addWidget(w)
    w.show()
    assert not w.clear_sig.isVisible()              # no signature: nothing to erase
    w.show_page("files")
    assert not w.open_btn.isVisible()               # no folder chosen: nothing to open
    w.show_page("general")
    w.way_keyboard.opened.emit()                    # the row is a link to its page
    assert w.stack.currentWidget() is w.pages["hotkey"]
    texts = " ".join(lbl.text() for lbl in w.findChildren(sw.QLabel))
    assert "photo (compressé).jpg" in texts and "Bon à savoir" not in texts
    assert "—" not in texts and "–" not in texts


def test_switching_pages_leaves_no_trace_of_the_previous_one(qtbot):
    """What is on screen after going from page to page is exactly the page shown
    (a see-through page taken for opaque left the previous one's pixels)."""
    from cerclic.settings import Settings
    from cerclic.ui.settings_window import SettingsWindow
    w = SettingsWindow(Settings(), windows_11=True, welcome=True)
    qtbot.addWidget(w)
    w.resize(900, 640)
    w.show()
    qtbot.wait(100)
    for key in ("signature", "general", "menu", "quality"):
        w.show_page(key)
        qtbot.wait(60)
    shown = w.screen().grabWindow(w.winId()).toImage()
    fresh = w.grab().toImage()
    differing = sum(1 for y in range(0, shown.height(), 6) for x in range(0, shown.width(), 6)
                    if shown.pixel(x, y) != fresh.pixel(x, y))
    assert differing == 0


def test_ask_each_time_where_results_go(qtbot, monkeypatch, tmp_path, jpg_photo):
    from PySide6.QtWidgets import QApplication, QFileDialog
    from cerclic.app import CerclicApp
    a = CerclicApp(QApplication.instance())
    try:
        a.settings.set("output_mode", "ask")
        target = tmp_path / "Pour Instagram"
        target.mkdir()
        asked = []
        monkeypatch.setattr(QFileDialog, "getExistingDirectory",
                            staticmethod(lambda *args, **kw: asked.append(args) or str(target)))
        a.start_action("img_compress", [jpg_photo], {}, QPoint(300, 300))
        qtbot.waitUntil(lambda: any(f.endswith(".jpg") for f in os.listdir(target)),
                        timeout=8000)
        assert asked and asked[0][2] == os.path.dirname(jpg_photo)   # the original's folder first
        # cancelled: nothing is created anywhere
        monkeypatch.setattr(QFileDialog, "getExistingDirectory",
                            staticmethod(lambda *args, **kw: ""))
        before = set(os.listdir(os.path.dirname(jpg_photo)))
        a.start_action("img_rotate", [jpg_photo], {"degrees": 90}, QPoint(300, 300))
        qtbot.wait(600)
        assert set(os.listdir(os.path.dirname(jpg_photo))) == before
        assert len(os.listdir(target)) == 1
    finally:
        a.cards.close_all()
        a.server.server.close()
        a.tray.hide()
