"""The 10 languages: every catalogue complete and consistent with the code,
plural rules, the computer's language, and real windows with no French left."""
import os
import sys

import pytest
from PySide6.QtWidgets import QAbstractButton, QApplication, QLabel, QWidget

from cerclic import i18n

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts"))
import i18n_messages  # noqa: E402

LANGS = [c for c in i18n.LANGS if c != i18n.SOURCE]
MSGS = i18n_messages.messages()


@pytest.mark.parametrize("code", LANGS)
def test_catalogue_complete_and_consistent(code):
    """Every text of the code, same {fields}, right number of plural forms,
    nothing unknown, no em or en dash."""
    assert i18n_messages.problems(code, MSGS) == []
    for value in i18n_messages.catalog(code).values():
        for v in ([value] if isinstance(value, str) else value):
            assert "—" not in v and "–" not in v, v


def test_plural_rules():
    assert [i18n.plural_index("fr", n) for n in (0, 1, 2)] == [0, 0, 1]
    assert [i18n.plural_index("en", n) for n in (0, 1, 2)] == [1, 0, 1]
    assert [i18n.plural_index("ar", n) for n in (0, 1, 2, 5, 12, 100, 103)] == [0, 1, 2, 3, 4, 5, 3]
    assert i18n.plural_index("ja", 7) == 0


def test_language_of_the_computer(monkeypatch):
    monkeypatch.delenv("CERCLIC_LANG", raising=False)
    assert i18n._match("pt-BR") == "pt" and i18n._match("zh_Hans_CN") == "zh"
    assert i18n._match("ru-RU") is None
    assert i18n.resolve("de") == "de"
    monkeypatch.setattr(i18n, "system_language", lambda: "en")
    assert i18n.resolve("auto") == "en"


@pytest.fixture
def lang(monkeypatch):
    """Switch to a real language for one test, French again afterwards."""
    monkeypatch.delenv("CERCLIC_LANG", raising=False)

    def use(code):
        assert i18n.set_language(code) == code
    yield use
    i18n.set_language("fr")
    QApplication.setLayoutDirection(QApplication.instance().layoutDirection().LeftToRight)


def _shown_texts(root: QWidget) -> list[str]:
    out = [root.windowTitle()]
    for w in [root, *root.findChildren(QWidget)]:
        if isinstance(w, (QLabel, QAbstractButton)):
            out.append(w.text())
        out.append(w.toolTip())
        if hasattr(w, "count") and hasattr(w, "itemText"):
            out += [w.itemText(i) for i in range(w.count())]
    return [t for t in out if t and t.strip()]


@pytest.mark.parametrize("code", LANGS)
def test_settings_window_has_no_french_left(qtbot, lang, code):
    """The Cerclic window, every section built, in each language: no text is
    still the French source of a text that has a translation."""
    from cerclic.settings import Settings
    from cerclic.ui import settings_window as sw
    lang(code)
    cat = i18n_messages.catalog(code)
    french = {k for k, v in cat.items() if isinstance(v, str) and v != k}
    w = sw.SettingsWindow(Settings(), welcome=True)
    qtbot.addWidget(w)
    w.show()
    left = sorted({t for t in _shown_texts(w) if t in french})
    assert left == [], left
    w.close()


def test_arabic_is_right_to_left(qtbot, lang):
    from cerclic.settings import Settings
    from cerclic.ui import settings_window as sw
    lang("ar")
    assert i18n.is_rtl()
    w = sw.SettingsWindow(Settings())
    qtbot.addWidget(w)
    w.show()
    assert any(t != "" and any("؀" <= ch <= "ۿ" for ch in t)
               for t in _shown_texts(w))
    w.close()


def test_sizes_and_files_in_english(lang):
    from cerclic import sizes
    from cerclic.paths import tag_name
    lang("en")
    assert sizes.human(1_500_000).endswith("MB") and "." in sizes.human(1_500_000)
    assert "compress" in tag_name("compressé").lower()
