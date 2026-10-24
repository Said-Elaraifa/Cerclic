"""The wheel, the popups and the cards in another language: every text they
show goes through the catalogue (a small fake one here), plurals included,
and the interface reads from the right in Arabic. French comes back after."""
import pytest
from PySide6.QtCore import QPoint, Qt

from cerclic import i18n
from cerclic.actions import registry

FAKE = {
    "en": {
        # wheel
        "Image": "Picture",
        "{category} ({n})": "{category} · {n}",
        "{n} fichier": ["{n} file", "{n} files"],
        "Rogner": "Crop",
        "Pivoter": "Rotate",
        "Gauche": "Left",
        "Plus": "More",
        "D'autres outils": "Other tools",
        "‹ Retour": "‹ Back",
        # popups
        "Annuler": "Cancel",
        "Enregistrer": "Save",
        "touche\x04Suppr": "Delete",
        "touche\x04Entrée": "Enter",
        "Glisse pour trier · {key} pour enlever": "Drag to sort · {key} to remove",
        "{n} page": ["{n} page", "{n} pages"],
        "{n} sélectionnée sur {count}": ["{n} of {count} selected", "{n} of {count} selected"],
        "Libre": "Free",
        "Glisse les coins · {key} pour rogner": "Drag the corners · {key} to crop",
        "Légère": "Light",
        "Images à 220 ppp : très nettes, même imprimées": "Pictures at 220 dpi",
        "Fermer (Échap)": "Close (Esc)",
        # cards
        "{n} fichier créé": ["{n} file created", "{n} files created"],
        "dossier\x04Bureau": "Desktop",
        "Dans « {folder} »": "In “{folder}”",
        "Ouvrir": "Open",
    },
    "ar": {
        "{n} page": ["{n} 0", "{n} 1", "{n} 2", "{n} few", "{n} many", "{n} other"],
        "{index} / {count}": "{index} / {count}",
    },
}


@pytest.fixture(autouse=True)
def _close_windows():
    yield
    from PySide6.QtWidgets import QApplication
    for w in QApplication.topLevelWidgets():
        try:
            w.close()
        except RuntimeError:
            pass
    QApplication.processEvents()


@pytest.fixture
def speak(monkeypatch, qapp):
    """speak("en"): the interface in that language, with the fake catalogue;
    French again after the test."""
    import cerclic.locales
    monkeypatch.delenv("CERCLIC_LANG", raising=False)
    monkeypatch.setattr(cerclic.locales, "load", lambda code: FAKE.get(code, {}))
    yield i18n.set_language
    i18n.set_language("fr")
    qapp.setLayoutDirection(Qt.LeftToRight)
    assert i18n.current() == "fr"


def _wheel(paths):
    from cerclic.ui.radial import Wheel
    w = Wheel(registry.menu_for(paths), registry.count_by_category(paths), "test")
    w.popup_at(QPoint(400, 400))
    return w


def _slice(w, label):
    return next(i for i, s in enumerate(w._slices) if s.label == label)


def test_wheel_in_english(qtbot, speak, jpg_photo):
    speak("en")
    w = _wheel([jpg_photo])
    labels = [s.label for s in w._slices]
    assert labels[0] == "Crop" and labels[-1] == "More"
    assert "Redimensionner" in labels           # no translation yet: the French text
    assert w._slices[-1].desc == "Other tools"
    w.activate(_slice(w, "Rotate"))
    assert w._title() == "Rotate"
    left = w._slices[_slice(w, "Left")]
    assert left.desc == "Rotate"                # the centre names the action


def test_wheel_categories_use_plurals(qtbot, speak, jpg_photo, png_with_alpha, pdf_1p):
    speak("en")
    w = _wheel([jpg_photo, png_with_alpha, pdf_1p])
    image = w._slices[_slice(w, "Picture · 2")]
    assert image.desc == "2 files"
    pdf = w._slices[_slice(w, "PDF")]
    assert pdf.desc == "1 file"
    w.activate(_slice(w, "Picture · 2"))
    assert w._title() == "Picture"


def test_wheel_speaks_french_again(qtbot, speak, jpg_photo):
    speak("en")
    assert _wheel([jpg_photo])._slices[0].label == "Crop"
    speak("fr")                     # built when it opens: no text kept from before
    w = _wheel([jpg_photo])
    assert w._slices[0].label == "Rogner" and w._slices[-1].label == "Plus"


def test_pages_editor_in_english(qtbot, speak, pdf_3p):
    from cerclic.ui.pages_editor import PagesEditor
    speak("en")
    ed = PagesEditor(pdf_3p)
    ed.start(QPoint(400, 400))
    assert ed.hint_label.text() == "Drag to sort · Delete to remove"
    assert ed.count_label.text() == "3 pages"               # trn, plural
    ed.grid.item(1).setSelected(True)
    assert ed.count_label.text() == "1 of 3 selected"
    ed.remove_selection()
    ed.grid.clearSelection()
    assert ed.count_label.text() == "2 pages"
    ed.grid.item(0).setSelected(True)
    ed.remove_selection()
    ed.grid.clearSelection()
    assert ed.count_label.text() == "1 page"                # trn, singular
    assert ed.ok.text() == "Save"
    assert ed.findChild(type(ed.ok), "close").toolTip() == "Close (Esc)"


def test_crop_and_compress_in_english(qtbot, speak, jpg_photo, pdf_1p):
    from cerclic.ui.compress_editor import CompressEditor
    from cerclic.ui.crop_editor import CropEditor
    speak("en")
    ed = CropEditor(jpg_photo)
    assert ed.hint_label.text() == "Drag the corners · Enter to crop"
    assert ed._preset_btns[0].text() == "Free"
    assert ed._preset_btns[2].text() == "1:1"
    ed.close()
    comp = CompressEditor([pdf_1p], "pdf")
    light = comp.level_buttons["light"]
    assert light.name.text() == "Light" and light.toolTip() == "Pictures at 220 dpi"
    assert comp.level_buttons["max"].name.text() == "Maximale"     # not translated yet
    comp.close()


def test_trim_times_use_the_decimal_sign_of_the_language(speak):
    from cerclic.ui.trim_editor import fmt_time
    assert fmt_time(65.3) == "1:05,3"
    speak("en")
    assert fmt_time(3725.26) == "1:02:05.3"


def test_result_card_in_english(qtbot, speak, tmp_path):
    from cerclic.engine import Result
    from cerclic.ui.cards import JobCard
    speak("en")
    desk = tmp_path / "Desktop"
    desk.mkdir()
    outs = [desk / "a.jpg", desk / "b.jpg"]
    for p in outs:
        p.write_bytes(b"")                       # no size: only where they are
    card = JobCard("Rotate")
    card.finish(Result(action_id="img_rotate", ok=True, outputs=[str(p) for p in outs]))
    assert card._status.text() == "2 files created\nIn “Desktop”"
    assert "Open" in [b.text() for b in card._buttons]
    card.close()


def test_arabic_reads_from_the_right(qtbot, speak, qapp, pdf_3p):
    from cerclic.ui.crop_editor import CropEditor
    from cerclic.ui.pages_editor import PagesEditor
    speak("ar")
    assert i18n.is_rtl()
    qapp.setLayoutDirection(Qt.RightToLeft)     # (what the app does for Arabic)
    ed = PagesEditor(pdf_3p)
    ed.start(QPoint(400, 400))
    assert ed.count_label.text() == "3 few"                 # Arabic: 3 to 10
    assert ed.left_btn.text() == "›" and ed.right_btn.text() == "‹"
    ed.grid.item(2).setSelected(True)
    qtbot.keyClick(ed, Qt.Key_Right, Qt.ControlModifier)    # towards the first page
    assert ed.grid.order() == [(0, 0), (2, 0), (1, 0)]
    ed.close()
    crop = CropEditor(pdf_3p)
    crop.start(QPoint(400, 400))
    assert crop.prev_btn.text() == "›" and crop.next_btn.text() == "‹"
    assert crop.page_label.text() == "1 / 3"
    crop.close()
