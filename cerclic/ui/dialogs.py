"""Small prompts (password, text) and a lightweight busy indicator."""
from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QGuiApplication
from PySide6.QtWidgets import (QInputDialog, QLineEdit, QWidget, QHBoxLayout,
                               QLabel, QGraphicsDropShadowEffect)

_DIALOG_QSS = (
    "QInputDialog{background:#1b1d24;}"
    "QLabel{color:#eceef3;}"
    "QLineEdit{background:#14151a;color:#eceef3;border:1px solid #2a2d37;"
    "border-radius:6px;padding:6px;}"
    "QPushButton{background:#2a2d37;color:#eceef3;border:none;padding:6px 14px;"
    "border-radius:8px;}QPushButton:hover{background:#3a3e4c;}")


def ask_password(prompt: str, confirm: bool = False) -> str | None:
    dlg = QInputDialog()
    dlg.setStyleSheet(_DIALOG_QSS)
    dlg.setWindowTitle("Cerclic")
    dlg.setLabelText(prompt)
    dlg.setTextEchoMode(QLineEdit.Password)
    dlg.setInputMode(QInputDialog.TextInput)
    if not dlg.exec():
        return None
    return dlg.textValue() or None


def ask_text(prompt: str, default: str = "") -> str | None:
    dlg = QInputDialog()
    dlg.setStyleSheet(_DIALOG_QSS)
    dlg.setWindowTitle("Cerclic")
    dlg.setLabelText(prompt)
    dlg.setTextValue(default)
    if not dlg.exec():
        return None
    return dlg.textValue() or None


class Busy(QWidget):
    """Indeterminate 'working...' card, bottom-right, shown during long runs."""

    def __init__(self, label: str):
        super().__init__(None, Qt.FramelessWindowHint | Qt.Tool
                         | Qt.WindowStaysOnTopHint | Qt.WindowDoesNotAcceptFocus)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        card = QWidget(self)
        card.setObjectName("card")
        lay = QHBoxLayout(self)
        lay.setContentsMargins(16, 16, 16, 16)
        inner = QHBoxLayout(card)
        inner.setContentsMargins(16, 12, 18, 12)
        inner.setSpacing(12)
        self._dot = QLabel("●")
        self._dot.setStyleSheet("color:#4C8DFF;font-size:16px;")
        inner.addWidget(self._dot)
        inner.addWidget(_lbl(label))
        lay.addWidget(card)
        self.setStyleSheet(
            "#card{background:#1b1d24;border:1px solid #2a2d37;border-radius:14px;}")
        sh = QGraphicsDropShadowEffect(self)
        sh.setBlurRadius(30)
        sh.setOffset(0, 7)
        sh.setColor(QColor(0, 0, 0, 150))
        card.setGraphicsEffect(sh)
        self.adjustSize()
        geo = QGuiApplication.primaryScreen().availableGeometry()
        self.move(geo.right() - self.width() + 2, geo.bottom() - self.height() + 2)
        self._phase = 0
        self._timer = QTimer(self, interval=400)
        self._timer.timeout.connect(self._pulse)
        self._timer.start()

    def _pulse(self):
        self._phase = (self._phase + 1) % 3
        self._dot.setText("●" * (self._phase + 1))

    def close(self):
        self._timer.stop()
        super().close()


def _lbl(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet("color:#eceef3;font-size:13px;font-weight:600;")
    return lbl
