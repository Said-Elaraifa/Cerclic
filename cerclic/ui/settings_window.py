"""Settings: how the wheel opens, signature, quality, start with Windows."""
from __future__ import annotations

import os

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QCheckBox, QFileDialog, QFormLayout, QGroupBox,
                               QHBoxLayout, QLabel, QPushButton, QSpinBox,
                               QVBoxLayout, QWidget)

from .. import __version__
from ..settings import Settings
from .theme import BORDER, BUTTON_QSS, MUTED, SURFACE, SURFACE_2, TEXT


def _hint(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setWordWrap(True)
    lbl.setStyleSheet(f"color:{MUTED};font-size:11px;font-weight:400;")
    return lbl


def _spin(lo, hi, val, suffix=""):
    s = QSpinBox()
    s.setRange(lo, hi)
    s.setValue(int(val))
    if suffix:
        s.setSuffix(suffix)
    return s


class SettingsWindow(QWidget):
    saved = Signal()
    draw_signature = Signal()

    def __init__(self, settings: Settings, windows_11: bool = False,
                 hotkey_label: str = "Ctrl+Alt+Espace"):
        super().__init__(None, Qt.Window)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.s = settings
        self.setWindowTitle("Cerclic · Paramètres")
        self.setMinimumWidth(500)
        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(12)

        # --- opening the wheel ---
        gb = QGroupBox("Ouvrir la roue")
        lay = QVBoxLayout(gb)
        self.context_menu = QCheckBox("« Cerclic » dans le clic droit des fichiers")
        self.context_menu.setChecked(bool(settings.get("context_menu")))
        lay.addWidget(self.context_menu)
        self.classic = None
        if windows_11:
            self.classic = QCheckBox("Menu clic droit complet (Cerclic en un clic)")
            from ..win.shell import classic_menu_enabled
            self.classic.setChecked(classic_menu_enabled())
            lay.addWidget(self.classic)
            lay.addWidget(_hint("Windows 11 range les entrées des applications sous "
                                "« Afficher d'autres options ». Cette option remet le "
                                "menu complet ; elle s'applique après le redémarrage de "
                                "l'Explorateur, proposé à l'enregistrement."))
        self.hotkey = QCheckBox(f"Raccourci {hotkey_label} sur les fichiers sélectionnés")
        self.hotkey.setChecked(bool(settings.get("hotkey")))
        lay.addWidget(self.hotkey)
        root.addWidget(gb)

        # --- signature ---
        gb_sign = QGroupBox("Signature")
        sl = QVBoxLayout(gb_sign)
        self.sign_preview = QLabel()
        self.sign_preview.setFixedHeight(84)
        self.sign_preview.setAlignment(Qt.AlignCenter)
        self.sign_preview.setStyleSheet("background:#FAFAF7;border-radius:10px;color:#777;")
        sl.addWidget(self.sign_preview)
        row = QHBoxLayout()
        draw = QPushButton("Dessiner…")
        draw.clicked.connect(self.draw_signature.emit)
        imp = QPushButton("Importer une image…")
        imp.clicked.connect(self._import_signature)
        clear = QPushButton("Effacer")
        clear.setObjectName("ghost")
        clear.clicked.connect(self._clear_signature)
        row.addWidget(draw)
        row.addWidget(imp)
        row.addStretch(1)
        row.addWidget(clear)
        sl.addLayout(row)
        root.addWidget(gb_sign)

        # --- quality ---
        gb_q = QGroupBox("Qualité")
        ql = QFormLayout(gb_q)
        self.compress_q = _spin(10, 95, settings.get("compress_quality"), " %")
        self.jpg_q = _spin(50, 100, settings.get("jpg_quality"), " %")
        ql.addRow("Compression des images", self.compress_q)
        ql.addRow("Qualité JPG", self.jpg_q)
        root.addWidget(gb_q)

        self.autostart = QCheckBox("Lancer Cerclic avec Windows")
        self.autostart.setChecked(bool(settings.get("autostart")))
        root.addWidget(self.autostart)
        root.addStretch(1)

        brow = QHBoxLayout()
        version = QLabel(f"Cerclic {__version__}")
        version.setStyleSheet(f"color:{MUTED};")
        brow.addWidget(version)
        brow.addStretch(1)
        close = QPushButton("Fermer")
        close.setObjectName("ghost")
        close.clicked.connect(self.close)
        save = QPushButton("Enregistrer")
        save.setObjectName("primary")
        save.setDefault(True)
        save.clicked.connect(self._save)
        brow.addWidget(close)
        brow.addWidget(save)
        root.addLayout(brow)

        self.setStyleSheet(
            f"SettingsWindow{{background:{SURFACE};}}"
            f"QGroupBox{{color:{TEXT};font-weight:700;border:1px solid {BORDER};"
            "border-radius:12px;margin-top:12px;padding:12px 12px 10px 12px;}"
            "QGroupBox::title{subcontrol-origin:margin;left:12px;padding:0 4px;}"
            f"QLabel{{color:{TEXT};}} QCheckBox{{color:{TEXT};spacing:8px;}}"
            f"QSpinBox{{background:{SURFACE_2};color:{TEXT};border:1px solid {BORDER};"
            "border-radius:6px;padding:4px 6px;min-width:80px;}" + BUTTON_QSS)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.refresh_signature()

    # -- signature ---------------------------------------------------------------
    def refresh_signature(self) -> None:
        path = self.s.get("signature")
        if path and os.path.exists(path):
            pix = QPixmap(path)
            if not pix.isNull():
                self.sign_preview.setPixmap(
                    pix.scaled(380, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                return
        self.sign_preview.setPixmap(QPixmap())
        self.sign_preview.setText("Aucune signature")

    def _import_signature(self) -> None:
        src, _ = QFileDialog.getOpenFileName(
            self, "Choisir une image de ta signature", "",
            "Images (*.png *.jpg *.jpeg *.webp *.heic *.bmp)")
        if not src:
            return
        from .signature import import_signature, signature_path
        try:
            path = import_signature(src, signature_path())
        except Exception as exc:
            self.sign_preview.setText(str(exc) if isinstance(exc, ValueError)
                                      else "Image illisible.")
            return
        self.s.set("signature", path)
        self.s.save()
        self.refresh_signature()

    def _clear_signature(self) -> None:
        self.s.set("signature", "")
        self.s.save()
        self.refresh_signature()

    # -- save ------------------------------------------------------------------------
    def classic_choice(self) -> bool | None:
        return None if self.classic is None else self.classic.isChecked()

    def _save(self) -> None:
        self.s.set("context_menu", self.context_menu.isChecked())
        self.s.set("hotkey", self.hotkey.isChecked())
        self.s.set("compress_quality", self.compress_q.value())
        self.s.set("jpg_quality", self.jpg_q.value())
        self.s.set("autostart", self.autostart.isChecked())
        self.s.save()
        self.saved.emit()
        self.close()
