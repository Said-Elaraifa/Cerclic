"""Result toast: a small card bottom-right with Open, Folder and Undo.

Undo is safe by construction: every output is a brand-new file beside the
original, so undoing just removes what Cerclic created and never touches the
source.
"""
from __future__ import annotations

import os
import subprocess
import sys

from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QColor, QGuiApplication
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel,
                               QPushButton, QGraphicsDropShadowEffect)

_AUTO_MS = 6000


def open_path(path: str) -> None:
    try:
        if os.name == "nt":
            os.startfile(path)  # noqa: shell open with default app
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    except Exception:
        pass


def reveal_path(path: str) -> None:
    try:
        if os.name == "nt":
            subprocess.Popen(["explorer", "/select,", os.path.normpath(path)])
        elif sys.platform == "darwin":
            subprocess.Popen(["open", "-R", path])
        else:
            subprocess.Popen(["xdg-open", os.path.dirname(path)])
    except Exception:
        pass


class Toast(QWidget):
    def __init__(self, title: str, outputs: list[str], ok: bool = True,
                 error: str = ""):
        super().__init__(None, Qt.FramelessWindowHint | Qt.Tool
                         | Qt.WindowStaysOnTopHint | Qt.WindowDoesNotAcceptFocus)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self._outputs = outputs

        card = QWidget(self)
        card.setObjectName("card")
        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 16, 16, 16)
        outer.addWidget(card)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(16, 13, 16, 13)
        lay.setSpacing(9)

        head = QLabel(("✓  " if ok else "✕  ") + title)
        head.setObjectName("head")
        lay.addWidget(head)

        if ok:
            n = len(outputs)
            sub = (os.path.basename(outputs[0]) if n == 1
                   else f"{n} fichiers créés")
            lay.addWidget(_muted(sub))
            row = QHBoxLayout()
            row.setSpacing(8)
            b_open = QPushButton("Ouvrir")
            b_open.clicked.connect(self._open)
            b_dir = QPushButton("Dossier")
            b_dir.clicked.connect(self._reveal)
            b_undo = QPushButton("Annuler")
            b_undo.setObjectName("ghost")
            b_undo.clicked.connect(self._undo)
            row.addWidget(b_open)
            row.addWidget(b_dir)
            row.addStretch(1)
            row.addWidget(b_undo)
            lay.addLayout(row)
        else:
            lay.addWidget(_muted(error or "Échec"))

        self._style(ok)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(34)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 160))
        card.setGraphicsEffect(shadow)

        self.adjustSize()
        self._place()
        self._timer = QTimer(self, singleShot=True, interval=_AUTO_MS)
        self._timer.timeout.connect(self.close)
        self._timer.start()

    def _style(self, ok: bool):
        accent = "#17B890" if ok else "#FF5A5F"
        self.setStyleSheet(
            "#card{background:#1b1d24;border:1px solid #2a2d37;border-radius:14px;}"
            f"#head{{color:{accent};font-size:14px;font-weight:700;}}"
            "QLabel{color:#eceef3;}"
            "QPushButton{background:#2a2d37;color:#eceef3;border:none;"
            "padding:6px 14px;border-radius:8px;font-weight:600;}"
            "QPushButton:hover{background:#3a3e4c;}"
            "QPushButton#ghost{background:transparent;color:#9aa0b0;}"
            "QPushButton#ghost:hover{color:#ff8a8f;}")

    def _place(self):
        geo = QGuiApplication.primaryScreen().availableGeometry()
        self.move(geo.right() - self.width() + 2,
                  geo.bottom() - self.height() + 2)

    def enterEvent(self, _):
        self._timer.stop()

    def leaveEvent(self, _):
        self._timer.start()

    def _open(self):
        if self._outputs:
            open_path(self._outputs[0])
        self.close()

    def _reveal(self):
        if self._outputs:
            reveal_path(self._outputs[0])
        self.close()

    def _undo(self):
        for p in self._outputs:
            try:
                if os.path.isfile(p):
                    os.remove(p)
            except OSError:
                pass
        # remove now-empty sibling folders (pdf to images, split)
        for p in self._outputs:
            d = os.path.dirname(p)
            try:
                if os.path.isdir(d) and not os.listdir(d):
                    os.rmdir(d)
            except OSError:
                pass
        self.close()


def _muted(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet("color:#9aa0b0;font-size:12px;")
    return lbl
