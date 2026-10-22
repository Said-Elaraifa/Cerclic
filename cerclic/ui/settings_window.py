"""Settings window: signature, gesture, autostart and quality defaults."""
from __future__ import annotations

import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                               QLabel, QPushButton, QCheckBox, QComboBox,
                               QSlider, QSpinBox, QFileDialog, QGroupBox)

from ..settings import Settings


class SettingsWindow(QDialog):
    def __init__(self, settings: Settings, on_apply=None):
        super().__init__(None, Qt.Window)
        self.s = settings
        self.on_apply = on_apply
        self.setWindowTitle("Cerclic, paramètres")
        self.resize(460, 560)
        root = QVBoxLayout(self)

        # --- signature ---
        gb_sign = QGroupBox("Signature")
        sl = QVBoxLayout(gb_sign)
        self.sign_preview = QLabel("Aucune signature")
        self.sign_preview.setFixedHeight(80)
        self.sign_preview.setAlignment(Qt.AlignCenter)
        self.sign_preview.setStyleSheet("background:#14151a;border-radius:8px;")
        sl.addWidget(self.sign_preview)
        srow = QHBoxLayout()
        pick = QPushButton("Choisir une image...")
        pick.clicked.connect(self._pick_signature)
        clear = QPushButton("Effacer")
        clear.clicked.connect(self._clear_signature)
        srow.addWidget(pick)
        srow.addWidget(clear)
        srow.addStretch(1)
        sl.addLayout(srow)
        sl.addWidget(_hint("Une image PNG au fond transparent donne le meilleur "
                           "résultat. « Signer » la posera sur le PDF."))
        root.addWidget(gb_sign)

        # --- gesture ---
        gb_g = QGroupBox("Geste d'ouverture")
        gl = QFormLayout(gb_g)
        self.gesture = QComboBox()
        self.gesture.addItem("Clic gauche maintenu", "left_hold")
        self.gesture.addItem("Clic droit maintenu", "right_hold")
        self.gesture.addItem("Double clic droit", "double_right")
        idx = max(0, self.gesture.findData(self.s.get("gesture")))
        self.gesture.setCurrentIndex(idx)
        gl.addRow("Geste", self.gesture)
        self.delay_ms = QSlider(Qt.Horizontal)
        self.delay_ms.setRange(200, 700)
        self.delay_ms.setValue(int(self.s.get("hold_ms")))
        self.delay_ms_lbl = QLabel()
        self._sync_ms()
        self.delay_ms.valueChanged.connect(self._sync_ms)
        msrow = QHBoxLayout()
        msrow.addWidget(self.delay_ms)
        msrow.addWidget(self.delay_ms_lbl)
        gl.addRow("Délai", msrow)
        gl.addRow("", _hint("Pour « maintenu » : durée d'appui avant que la roue "
                            "s'ouvre. Un clic normal, un double clic ou un glisser "
                            "ne déclenchent rien."))
        root.addWidget(gb_g)

        # --- menu ---
        gb_m = QGroupBox("Menu")
        ml = QVBoxLayout(gb_m)
        self.primary_only = QCheckBox("Afficher seulement les actions principales")
        self.primary_only.setChecked(bool(self.s.get("primary_only")))
        ml.addWidget(self.primary_only)
        root.addWidget(gb_m)

        # --- quality ---
        gb_q = QGroupBox("Qualité par défaut")
        ql = QFormLayout(gb_q)
        self.compress_q = _spin(10, 95, int(self.s.get("compress_quality")))
        self.jpg_q = _spin(50, 100, int(self.s.get("jpg_quality")))
        self.resize_side = _spin(400, 6000, int(self.s.get("resize_max_side")), step=100)
        ql.addRow("Compression image", self.compress_q)
        ql.addRow("Qualité JPG", self.jpg_q)
        ql.addRow("Redimension (px)", self.resize_side)
        root.addWidget(gb_q)

        # --- autostart + save ---
        self.autostart = QCheckBox("Lancer Cerclic au démarrage de Windows")
        self.autostart.setChecked(bool(self.s.get("autostart")))
        root.addWidget(self.autostart)
        root.addStretch(1)
        brow = QHBoxLayout()
        brow.addStretch(1)
        save = QPushButton("Enregistrer")
        save.setDefault(True)
        save.clicked.connect(self._save)
        close = QPushButton("Fermer")
        close.clicked.connect(self.reject)
        brow.addWidget(close)
        brow.addWidget(save)
        root.addLayout(brow)

        self._refresh_signature()
        self._style()

    # -- helpers -------------------------------------------------------------
    def _sync_ms(self):
        self.delay_ms_lbl.setText(f"{self.delay_ms.value()} ms")

    def _pick_signature(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Choisir une signature", "",
            "Images (*.png *.jpg *.jpeg *.webp)")
        if path:
            self.s.set("signature", path)
            self._refresh_signature()

    def _clear_signature(self):
        self.s.set("signature", "")
        self._refresh_signature()

    def _refresh_signature(self):
        path = self.s.get("signature")
        if path and os.path.exists(path):
            pix = QPixmap(path).scaledToHeight(70, Qt.SmoothTransformation)
            self.sign_preview.setPixmap(pix)
        else:
            self.sign_preview.setText("Aucune signature")

    def _save(self):
        self.s.set("gesture", self.gesture.currentData())
        self.s.set("hold_ms", self.delay_ms.value())
        self.s.set("double_ms", self.delay_ms.value())
        self.s.set("primary_only", self.primary_only.isChecked())
        self.s.set("compress_quality", self.compress_q.value())
        self.s.set("jpg_quality", self.jpg_q.value())
        self.s.set("resize_max_side", self.resize_side.value())
        self.s.set("autostart", self.autostart.isChecked())
        self.s.save()
        if self.on_apply:
            self.on_apply()
        self.accept()

    def _style(self):
        self.setStyleSheet(
            "QDialog{background:#1b1d24;} QGroupBox{color:#eceef3;font-weight:700;"
            "border:1px solid #2a2d37;border-radius:10px;margin-top:10px;padding:10px;}"
            "QGroupBox::title{subcontrol-origin:margin;left:10px;padding:0 4px;}"
            "QLabel{color:#eceef3;} QCheckBox{color:#eceef3;}"
            "QComboBox,QSpinBox{background:#14151a;color:#eceef3;border:1px solid "
            "#2a2d37;border-radius:6px;padding:4px;}"
            "QPushButton{background:#2a2d37;color:#eceef3;border:none;padding:7px 14px;"
            "border-radius:8px;}QPushButton:hover{background:#3a3e4c;}")


def _hint(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setWordWrap(True)
    lbl.setStyleSheet("color:#9aa0b0;font-size:11px;font-weight:400;")
    return lbl


def _spin(lo, hi, val, step=1):
    s = QSpinBox()
    s.setRange(lo, hi)
    s.setSingleStep(step)
    s.setValue(val)
    return s
