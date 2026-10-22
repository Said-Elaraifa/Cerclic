"""A small bubble that asks for one value (password, text) where the wheel was.

No system dialog opens: the bubble has the wheel's look, takes the keyboard at
once, Enter validates; Escape or a click elsewhere cancels.
"""
from __future__ import annotations

from PySide6.QtCore import QPoint, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QGuiApplication
from PySide6.QtWidgets import (QGraphicsDropShadowEffect, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QVBoxLayout, QWidget)

from ..win.foreground import bring_to_front
from .dismiss import DismissGuard
from .theme import BORDER, BUTTON_QSS, INPUT_QSS, MUTED, SURFACE, TEXT


class PromptBubble(QWidget):
    accepted = Signal(str)
    cancelled = Signal()

    def __init__(self, title: str, subtitle: str = "", password: bool = False,
                 default: str = "", ok_label: str = "OK", allow_empty: bool = False):
        super().__init__(None, Qt.FramelessWindowHint | Qt.Tool
                         | Qt.WindowStaysOnTopHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Cerclic")
        self._allow_empty = allow_empty
        self._done = False

        card = QWidget(self)
        card.setObjectName("card")
        outer = QVBoxLayout(self)
        outer.setContentsMargins(22, 22, 22, 22)
        outer.addWidget(card)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(18, 16, 18, 16)
        lay.setSpacing(10)

        head = QLabel(title)
        head.setObjectName("head")
        head.setWordWrap(True)
        lay.addWidget(head)
        if subtitle:
            sub = QLabel(subtitle)
            sub.setObjectName("sub")
            sub.setWordWrap(True)
            lay.addWidget(sub)

        self.edit = QLineEdit(default)
        self.edit.setMinimumWidth(270)
        if password:
            self.edit.setEchoMode(QLineEdit.Password)
        self.edit.selectAll()
        self.edit.returnPressed.connect(self._accept)
        self.edit.textChanged.connect(self._sync)
        lay.addWidget(self.edit)

        row = QHBoxLayout()
        row.setSpacing(8)
        if password:
            self.eye = QPushButton("Afficher")
            self.eye.setObjectName("ghost")
            self.eye.setCheckable(True)
            self.eye.toggled.connect(self._toggle_echo)
            row.addWidget(self.eye)
        row.addStretch(1)
        cancel = QPushButton("Annuler")
        cancel.setObjectName("ghost")
        cancel.clicked.connect(self.cancel)
        self.ok = QPushButton(ok_label)
        self.ok.setObjectName("primary")
        self.ok.clicked.connect(self._accept)
        row.addWidget(cancel)
        row.addWidget(self.ok)
        lay.addLayout(row)

        self.setStyleSheet(
            f"#card{{background:{SURFACE};border:1px solid {BORDER};border-radius:16px;}}"
            f"#head{{color:{TEXT};font-size:14px;font-weight:700;}}"
            f"#sub{{color:{MUTED};font-size:12px;}}" + INPUT_QSS + BUTTON_QSS)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(36)
        shadow.setOffset(0, 10)
        shadow.setColor(QColor(0, 0, 0, 170))
        card.setGraphicsEffect(shadow)
        self._sync()
        self.adjustSize()
        self._guard = DismissGuard(self, self.cancel, leave_s=8.0, idle_s=180)

    def _toggle_echo(self, on: bool) -> None:
        self.edit.setEchoMode(QLineEdit.Normal if on else QLineEdit.Password)
        self.eye.setText("Masquer" if on else "Afficher")

    def _sync(self) -> None:
        self.ok.setEnabled(self._allow_empty or bool(self.edit.text().strip()))

    def popup_at(self, pos: QPoint) -> None:
        self.adjustSize()
        screen = QGuiApplication.screenAt(pos) or QGuiApplication.primaryScreen()
        geo = screen.availableGeometry()
        x = int(pos.x() - self.width() / 2)
        y = int(pos.y() - self.height() / 2)
        x = max(geo.left(), min(x, geo.right() + 1 - self.width()))
        y = max(geo.top(), min(y, geo.bottom() + 1 - self.height()))
        self.move(x, y)
        self.show()
        self.raise_()
        self.activateWindow()
        bring_to_front(int(self.winId()))
        self.edit.setFocus(Qt.PopupFocusReason)
        self._guard.start()
        QTimer.singleShot(120, self._refocus)   # in case Windows was slow to hand over

    def _refocus(self) -> None:
        if self._done or not self.isVisible():
            return
        if not self.isActiveWindow():
            self.activateWindow()
            bring_to_front(int(self.winId()))
        self.edit.setFocus(Qt.OtherFocusReason)

    def _accept(self) -> None:
        if self._done or not self.ok.isEnabled():
            return
        self._done = True
        self._guard.stop()
        value = self.edit.text()
        self.hide()
        self.accepted.emit(value)
        self.close()

    def cancel(self) -> None:
        if self._done:
            return
        self._done = True
        self._guard.stop()
        self.hide()
        self.cancelled.emit()
        self.close()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.cancel()
        else:
            super().keyPressEvent(e)
