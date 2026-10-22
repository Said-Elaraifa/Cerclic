"""Full-screen editor frame shared by the crop and signature editors.

The window opens at once on the screen under the cursor (dark, borderless),
the document is decoded in the background and appears as soon as it is ready.
Enter validates, Escape cancels.
"""
from __future__ import annotations

import threading

from PySide6.QtCore import QObject, QPropertyAnimation, Qt, Signal
from PySide6.QtGui import QCursor, QGuiApplication, QImage
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QVBoxLayout,
                               QWidget)

from ..win.foreground import bring_to_front
from .theme import BG, BORDER, BUTTON_QSS, MUTED, TEXT


class Loader(QObject):
    """Run a function on a background thread; deliver its result on the GUI thread."""
    done = Signal(object, object)   # (result, error message)

    def run(self, fn, *args) -> None:
        def work():
            try:
                res, err = fn(*args), None
            except Exception as exc:  # shown in the editor, never raised
                from ..engine import friendly_error
                res, err = None, friendly_error(exc)
            try:
                self.done.emit(res, err)
            except RuntimeError:
                pass  # the editor was closed meanwhile
        threading.Thread(target=work, daemon=True, name="cerclic-load").start()


def qimage_from_rgb(data: bytes, w: int, h: int, stride: int) -> QImage:
    return QImage(data, w, h, stride, QImage.Format_RGB888).copy()


def qimage_from_pil(im) -> QImage:
    im = im.convert("RGBA")
    data = im.tobytes("raw", "RGBA")
    return QImage(data, im.width, im.height, im.width * 4,
                  QImage.Format_RGBA8888).copy()


class EditorWindow(QWidget):
    accepted = Signal(dict)
    cancelled = Signal()

    def __init__(self, title: str, hint: str):
        super().__init__(None, Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle(f"Cerclic · {title}")
        self.setStyleSheet(f"EditorWindow{{background:{BG};}}"
                           f"QLabel{{color:{TEXT};}}"
                           f"QLabel#hint{{color:{MUTED};}}"
                           f"QCheckBox{{color:{TEXT};spacing:8px;}}"
                           f"#bar{{background:{BG};border-top:1px solid {BORDER};}}"
                           + BUTTON_QSS)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self._done = False

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        top = QHBoxLayout()
        top.setContentsMargins(24, 14, 16, 8)
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-size:15px;font-weight:700;")
        top.addWidget(self.title_label)
        top.addSpacing(16)
        hint_label = QLabel(hint)
        hint_label.setObjectName("hint")
        top.addWidget(hint_label, 1)
        close = QPushButton("✕")
        close.setObjectName("ghost")
        close.setToolTip("Fermer (Échap)")
        close.setFixedWidth(44)
        close.clicked.connect(self.cancel)
        top.addWidget(close)
        root.addLayout(top)

        self.center = QVBoxLayout()
        self.center.setContentsMargins(0, 0, 0, 0)
        root.addLayout(self.center, 1)

        bar = QWidget()
        bar.setObjectName("bar")
        bar.setAttribute(Qt.WA_StyledBackground, True)
        self.bar = QHBoxLayout(bar)
        self.bar.setContentsMargins(24, 12, 24, 14)
        self.bar.setSpacing(8)
        root.addWidget(bar)

        self._fade = QPropertyAnimation(self, b"windowOpacity", self)
        self._fade.setDuration(140)
        self._fade.setStartValue(0.0)
        self._fade.setEndValue(1.0)

    def open_on_cursor_screen(self) -> None:
        screen = QGuiApplication.screenAt(QCursor.pos()) or QGuiApplication.primaryScreen()
        self.setGeometry(screen.geometry())
        self.setWindowOpacity(0.0)
        self.show()
        self.raise_()
        self.activateWindow()
        bring_to_front(int(self.winId()))
        self.setFocus()
        self._fade.start()

    def finish(self, result: dict) -> None:
        if self._done:
            return
        self._done = True
        self.hide()
        self.accepted.emit(result)
        self.close()

    def cancel(self) -> None:
        if self._done:
            return
        self._done = True
        self.hide()
        self.cancelled.emit()
        self.close()

    def closeEvent(self, e):
        if not self._done:
            self._done = True
            self.cancelled.emit()
        super().closeEvent(e)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.cancel()
        elif e.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.validate()
        else:
            super().keyPressEvent(e)

    def validate(self) -> None:  # overridden
        pass
