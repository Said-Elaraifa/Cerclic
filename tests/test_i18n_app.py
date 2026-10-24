"""Choosing Cerclic's language: the setting, the window and the menu made again
in it at once, Arabic from right to left."""
import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel

from cerclic import i18n

FAKE_EN = {
    "Général": "General",
    "Langue": "Language",
    "Ouvrir Cerclic": "Open Cerclic",
    "Quitter Cerclic": "Quit Cerclic",
    "Automatique (langue de l'ordinateur)": "Automatic (computer language)",
}


@pytest.fixture
def any_language(monkeypatch):
    """The language may change (the tests otherwise stay in French): this
    computer speaks French, English has a small catalogue. French again
    afterwards."""
    from cerclic import locales
    monkeypatch.delenv("CERCLIC_LANG", raising=False)
    monkeypatch.setattr(i18n, "system_language", lambda: "fr")
    monkeypatch.setattr(locales, "load", lambda code: dict(FAKE_EN) if code == "en" else {})
    yield
    i18n.set_language("fr")
    assert i18n.current() == "fr"


@pytest.fixture
def app(qtbot, any_language):
    from cerclic.app import CerclicApp
    a = CerclicApp(QApplication.instance())
    yield a
    win = a._settings_window()
    if win is not None:
        win.close()
    a.cards.close_all()
    a.server.server.close()
    a.tray.hide()


def _choose(win, code):
    i = win.language.findData(code)
    assert i >= 0
    win.language.setCurrentIndex(i)
    win.language.activated.emit(i)


def _texts(win):
    return [lbl.text() for lbl in win.findChildren(QLabel)]


def test_language_setting_defaults_to_the_computers(any_language):
    from cerclic import launcher
    from cerclic.settings import DEFAULTS, Settings
    assert DEFAULTS["language"] == "auto" and Settings().get("language") == "auto"
    s = Settings({"language": "en"})
    assert s.get("language") == "en"
    s.save()
    assert launcher.apply_language() == "en"           # before Qt shows anything
    assert i18n.tr("Général") == "General"


def test_language_menu_lists_every_language_by_its_own_name(qtbot):
    from cerclic.settings import Settings
    from cerclic.ui.settings_window import SettingsWindow
    w = SettingsWindow(Settings())
    qtbot.addWidget(w)
    items = [(w.language.itemText(i), w.language.itemData(i))
             for i in range(w.language.count())]
    assert items[0] == ("Automatique (langue de l'ordinateur)", "auto")
    assert items[1:] == [(name, code) for code, name in i18n.LANGS.items()]
    assert w.language.currentData() == "auto"
    assert "Langue" in _texts(w)


def test_choosing_a_language_relabels_the_window_at_once(qtbot, app):
    from cerclic.settings import Settings
    app.open_settings()
    win = app._settings_window()
    win.show_page("general")
    win.move(win.x() + 7, win.y() + 5)
    place = win.geometry()
    assert win.nav["general"].text() == "Général"
    _choose(win, "en")
    assert Settings.load().get("language") == "en"
    qtbot.waitUntil(lambda: app._settings_window() not in (None, win), timeout=3000)
    new = app._settings_window()
    assert new.isVisible() and not win.isVisible()
    assert new.nav["general"].text() == "General"         # rebuilt in English
    assert "General" in _texts(new) and "Language" in _texts(new)
    assert new.language.currentData() == "en"
    assert new.language.itemText(0) == "Automatic (computer language)"
    assert new.current_page() == "general" and new.geometry() == place
    assert [a.text() for a in app._menu.actions() if a.text()] == \
        ["Open Cerclic", "Quit Cerclic"]
    # and back to the computer's language (French here)
    _choose(new, "auto")
    qtbot.waitUntil(lambda: app._settings_window() not in (None, new), timeout=3000)
    again = app._settings_window()
    assert again.nav["general"].text() == "Général"
    assert Settings.load().get("language") == "auto"
    assert [a.text() for a in app._menu.actions() if a.text()] == \
        ["Ouvrir Cerclic", "Quitter Cerclic"]


def test_arabic_reads_from_right_to_left(qtbot, app):
    from cerclic.settings import Settings
    from cerclic.ui.settings_window import SettingsWindow
    qapp = QApplication.instance()
    assert qapp.layoutDirection() == Qt.LeftToRight
    app.open_settings()
    win = app._settings_window()
    _choose(win, "ar")
    assert i18n.current() == "ar" and i18n.is_rtl()
    assert qapp.layoutDirection() == Qt.RightToLeft
    qtbot.waitUntil(lambda: app._settings_window() not in (None, win), timeout=3000)
    rtl = app._settings_window()
    assert rtl.layoutDirection() == Qt.RightToLeft
    other = SettingsWindow(Settings.load())
    qtbot.addWidget(other)
    assert other.layoutDirection() == Qt.RightToLeft
    _choose(rtl, "fr")
    assert qapp.layoutDirection() == Qt.LeftToRight
    qtbot.waitUntil(lambda: app._settings_window() not in (None, rtl), timeout=3000)
    assert app._settings_window().layoutDirection() == Qt.LeftToRight


def test_language_menu_ignores_the_mouse_wheel(qtbot):
    """Scrolling the page over the menu never changes the language."""
    from PySide6.QtCore import QPoint, QPointF
    from PySide6.QtGui import QWheelEvent
    from cerclic.settings import Settings
    from cerclic.ui.settings_window import SettingsWindow
    w = SettingsWindow(Settings())
    qtbot.addWidget(w)
    seen = []
    w.language.activated.connect(seen.append)
    ev = QWheelEvent(QPointF(5, 5), QPointF(5, 5), QPoint(0, 0), QPoint(0, -120),
                     Qt.NoButton, Qt.NoModifier, Qt.NoScrollPhase, False)
    QApplication.sendEvent(w.language, ev)
    assert w.language.currentData() == "auto" and not seen
