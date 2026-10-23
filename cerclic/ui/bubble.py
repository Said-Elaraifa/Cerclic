"""A small bubble that asks for one value (password, text) where the wheel was.

No system dialog opens: the bubble has the wheel's look, takes the keyboard at
once, Enter validates, Escape cancels. It stays while the user goes to fetch
the value in another window (a password in a mail).
"""
from __future__ import annotations

from PySide6.QtCore import QPoint, Qt, QTimer, Signal
from PySide6.QtGui import QAction, QColor, QGuiApplication, QIcon, QPainter, QPixmap
from PySide6.QtWidgets import (QGraphicsDropShadowEffect, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QVBoxLayout, QWidget)

from ..win.foreground import bring_to_front
from .dismiss import DismissGuard
from .theme import BUTTON_QSS, INPUT_QSS, MUTED, TEXT, card_qss


def _glyph_icon(name: str, size: int = 18) -> QIcon:
    from .icons import draw_icon
    pix = QPixmap(size * 2, size * 2)
    pix.setDevicePixelRatio(2.0)
    pix.fill(Qt.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.Antialiasing, True)
    draw_icon(p, name, size / 2, size / 2, size * 0.8, QColor(MUTED))
    p.end()
    return QIcon(pix)


class PromptBubble(QWidget):
    accepted = Signal(str)
    cancelled = Signal()

    def __init__(self, title: str, subtitle: str = "", password: bool = False,
                 default: str = "", ok_label: str = "OK", allow_empty: bool = False):
        super().__init__(None, Qt.FramelessWindowHint | Qt.Tool
                         | Qt.WindowStaysOnTopHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAttribute(Qt.WA_MacAlwaysShowToolWindow)   # macOS: stays shown in the background
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
        self.eye = None
        if password:
            self.edit.setEchoMode(QLineEdit.Password)
            # show / hide the password, inside the field (the typing stays there)
            self.eye = QAction(_glyph_icon("eye"), "Afficher le mot de passe", self.edit)
            self.eye.setCheckable(True)
            self.eye.toggled.connect(self._toggle_echo)
            self.edit.addAction(self.eye, QLineEdit.TrailingPosition)
        self.edit.selectAll()
        self.edit.returnPressed.connect(self._accept)
        self.edit.textChanged.connect(self._sync)
        lay.addWidget(self.edit)

        row = QHBoxLayout()
        row.setSpacing(8)
        row.addStretch(1)
        cancel = QPushButton("Annuler")
        cancel.setObjectName("ghost")
        cancel.setFocusPolicy(Qt.NoFocus)
        cancel.clicked.connect(self.cancel)
        self.ok = QPushButton(ok_label)
        self.ok.setObjectName("primary")
        self.ok.setFocusPolicy(Qt.NoFocus)
        self.ok.clicked.connect(self._accept)
        row.addWidget(cancel)
        row.addWidget(self.ok)
        lay.addLayout(row)

        self.setStyleSheet(
            card_qss(16) +
            f"#head{{color:{TEXT};font-size:14px;font-weight:700;}}"
            f"#sub{{color:{MUTED};font-size:12px;}}" + INPUT_QSS + BUTTON_QSS)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(36)
        shadow.setOffset(0, 10)
        shadow.setColor(QColor(20, 40, 90, 64))
        card.setGraphicsEffect(shadow)
        self._sync()
        self.adjustSize()
        self._guard = DismissGuard(self, self.cancel, idle_s=180, sticky=True)

    def _toggle_echo(self, on: bool) -> None:
        self.edit.setEchoMode(QLineEdit.Normal if on else QLineEdit.Password)
        self.eye.setIcon(_glyph_icon("eye_off" if on else "eye"))
        self.eye.setText("Masquer le mot de passe" if on else "Afficher le mot de passe")

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
        elif e.key() in (Qt.Key_Return, Qt.Key_Enter):
            self._accept()
        else:
            super().keyPressEvent(e)
