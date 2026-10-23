"""Compact popup shared by the editors (crop, signature, pages, trim).

The popup opens where the wheel was, sized to what it shows (a small picture
gets a small popup, a big one is scaled down), and always stays inside the
screen. Nothing else opens: no full-screen window, no other application.
Enter validates, Escape or a click elsewhere cancels.
"""
from __future__ import annotations

import itertools
import threading

from PySide6.QtCore import (QEasingCurve, QObject, QPoint, QPropertyAnimation,
                            QRect, QSize, Qt, QTimer, Signal)
from PySide6.QtGui import QColor, QCursor, QGuiApplication, QImage
from PySide6.QtWidgets import (QGraphicsDropShadowEffect, QHBoxLayout, QLabel,
                               QPushButton, QVBoxLayout, QWidget)

from ..win.foreground import bring_to_front
from .dismiss import DismissGuard
from .theme import BORDER, BUTTON_QSS, MUTED, SCROLL_QSS, SURFACE, SURFACE_2, TEXT

SHADOW = 18          # transparent margin around the card, for its shadow
EDGE = 10            # minimum gap between the card and the screen edges


class _Hub(QObject):
    """Lives as long as the app: background loads report here, never to an
    object that may already be gone (an editor closed while it was loading)."""
    done = Signal(int, object, object)
    progress = Signal(int, object)


_hub: _Hub | None = None
_keys = itertools.count(1)


def _get_hub() -> _Hub:
    global _hub
    if _hub is None:
        _hub = _Hub()           # created on the GUI thread, by the first editor
    return _hub


class Loader(QObject):
    """Run a function on a background thread; deliver its result (and, with
    run_reporting, partial results) on the GUI thread, to this loader only and
    only while it exists. stop() asks a reporting function to finish early."""
    done = Signal(object, object)   # (result, error message)
    progress = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._mine: set[int] = set()
        self.stop_event = threading.Event()
        hub = _get_hub()
        hub.done.connect(self._route)
        hub.progress.connect(self._route_progress)

    def _route(self, key: int, res, err) -> None:
        if key in self._mine:
            self._mine.discard(key)
            self.done.emit(res, err)

    def _route_progress(self, key: int, obj) -> None:
        if key in self._mine:
            self.progress.emit(obj)

    def stop(self) -> None:
        self.stop_event.set()

    def run(self, fn, *args) -> None:
        self._start(lambda key: fn(*args))

    def run_reporting(self, fn) -> None:
        """fn(report, should_stop): report(obj) sends obj to `progress`."""
        hub, stop = _get_hub(), self.stop_event
        self._start(lambda key: fn(lambda obj: hub.progress.emit(key, obj), stop.is_set))

    def _start(self, call) -> None:
        key = next(_keys)
        self._mine.add(key)
        hub = _get_hub()

        def work():
            try:
                res, err = call(key), None
            except Exception as exc:  # shown in the editor, never raised
                from ..engine import friendly_error
                res, err = None, friendly_error(exc)
            hub.done.emit(key, res, err)
        threading.Thread(target=work, daemon=True, name="cerclic-load").start()


def qimage_from_rgb(data: bytes, w: int, h: int, stride: int) -> QImage:
    return QImage(data, w, h, stride, QImage.Format_RGB888).copy()


def qimage_from_pil(im) -> QImage:
    im = im.convert("RGBA")
    data = im.tobytes("raw", "RGBA")
    return QImage(data, im.width, im.height, im.width * 4,
                  QImage.Format_RGBA8888).copy()


def screen_for(pos: QPoint):
    return QGuiApplication.screenAt(pos) or QGuiApplication.primaryScreen()


def fit_view(content_w: float, content_h: float, room_w: float, room_h: float,
             min_side: float = 300, max_scale: float = 1.0) -> tuple[int, int]:
    """Size to show a content_w x content_h picture in: as big as it is (never
    blown up beyond max_scale), scaled down to fit room_w x room_h, and not
    smaller than min_side on its long side (tiny pictures stay workable)."""
    cw, ch = max(1.0, float(content_w)), max(1.0, float(content_h))
    s = min(room_w / cw, room_h / ch, max_scale)
    w, h = cw * s, ch * s
    if max(w, h) < min_side:
        k = min(min_side / max(w, h), room_w / w, room_h / h)
        w, h = w * k, h * k
    return max(1, round(w)), max(1, round(h))


def popup_rect(anchor: QPoint, size: QSize, avail: QRect) -> QRect:
    """Where a popup of `size` (shadow margin included) goes: centred on the
    anchor, its card kept EDGE px inside the available screen area."""
    w, h = size.width(), size.height()
    x = anchor.x() - w // 2
    y = anchor.y() - h // 2
    lo_x = avail.left() + EDGE - SHADOW
    hi_x = avail.right() + 1 - EDGE + SHADOW - w
    lo_y = avail.top() + EDGE - SHADOW
    hi_y = avail.bottom() + 1 - EDGE + SHADOW - h
    x = max(lo_x, min(x, hi_x)) if hi_x >= lo_x else lo_x
    y = max(lo_y, min(y, hi_y)) if hi_y >= lo_y else lo_y
    return QRect(x, y, w, h)


class EditorWindow(QWidget):
    """The popup frame: a header (name, hint, close), the editor's content,
    a row of tools and the action buttons."""
    accepted = Signal(dict)
    cancelled = Signal()

    def __init__(self, title: str, hint: str = ""):
        super().__init__(None, Qt.FramelessWindowHint | Qt.Tool
                         | Qt.WindowStaysOnTopHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle(f"Cerclic · {title}")
        self.setFocusPolicy(Qt.StrongFocus)
        self._done = False
        self.anchor = QCursor.pos()

        self.card = QWidget(self)
        self.card.setObjectName("card")
        self.card.setAttribute(Qt.WA_StyledBackground, True)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(SHADOW, SHADOW, SHADOW, SHADOW)
        outer.addWidget(self.card)

        root = QVBoxLayout(self.card)
        root.setContentsMargins(14, 10, 14, 12)
        root.setSpacing(8)

        top = QHBoxLayout()
        top.setSpacing(10)
        self.title_label = QLabel(_elide(title, 38))
        self.title_label.setObjectName("title")
        self.title_label.setToolTip(title)
        top.addWidget(self.title_label)
        self.hint_label = QLabel(hint)
        self.hint_label.setObjectName("hint")
        top.addWidget(self.hint_label, 1)
        close = QPushButton("✕")
        close.setObjectName("close")
        close.setToolTip("Fermer (Échap)")
        close.setFixedSize(28, 26)
        close.setFocusPolicy(Qt.NoFocus)
        close.clicked.connect(self.cancel)
        top.addWidget(close)
        root.addLayout(top)

        self.center = QVBoxLayout()
        self.center.setContentsMargins(0, 0, 0, 0)
        root.addLayout(self.center, 1)

        self.tools = QHBoxLayout()
        self.tools.setSpacing(6)
        root.addLayout(self.tools)
        self.bar = QHBoxLayout()
        self.bar.setSpacing(8)
        root.addLayout(self.bar)

        self.setStyleSheet(
            f"#card{{background:{SURFACE};border:1px solid {BORDER};border-radius:16px;}}"
            f"QLabel{{color:{TEXT};}}"
            f"#title{{font-size:12px;font-weight:700;}}"
            f"#hint{{color:{MUTED};font-size:11px;}}"
            f"QCheckBox{{color:{TEXT};spacing:6px;font-size:12px;}}"
            + BUTTON_QSS +
            "QPushButton{padding:6px 12px;border-radius:8px;}"
            f"QPushButton#chip{{background:{SURFACE_2};color:{MUTED};padding:4px 9px;"
            "border-radius:11px;font-size:11px;font-weight:600;}"
            f"QPushButton#chip:hover{{color:{TEXT};}}"
            "QPushButton#chip:checked{background:#4C8DFF;color:white;}"
            f"QPushButton#close{{background:transparent;color:{MUTED};padding:0;"
            "font-size:13px;border-radius:8px;}"
            f"QPushButton#close:hover{{background:{SURFACE_2};color:{TEXT};}}"
            + SCROLL_QSS)
        shadow = QGraphicsDropShadowEffect(self.card)
        shadow.setBlurRadius(34)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.card.setGraphicsEffect(shadow)

        self._guard = DismissGuard(self, self.cancel, leave_s=45.0, idle_s=900.0,
                                   keep_once_used=True)
        self._fade = QPropertyAnimation(self, b"windowOpacity", self)
        self._fade.setDuration(130)
        self._fade.setStartValue(0.0)
        self._fade.setEndValue(1.0)
        self._fade.setEasingCurve(QEasingCurve.OutCubic)

    # -- sizing and placing -----------------------------------------------------------
    def room(self, max_w: int = 600, max_h: int = 470) -> tuple[int, int]:
        """Content area for this popup: a small window by default, never more
        than the screen comfortably allows (tools and buttons take ~190 px)."""
        avail = screen_for(self.anchor).availableGeometry()
        w = min(max_w, int(avail.width() * 0.6))
        h = min(max_h, int(avail.height() - 190 - 2 * EDGE))
        return max(240, w), max(160, h)

    def chip(self, label: str, checkable: bool = True) -> QPushButton:
        b = QPushButton(label)
        b.setObjectName("chip")
        b.setCheckable(checkable)
        b.setFocusPolicy(Qt.NoFocus)
        return b

    def open_at(self, anchor: QPoint | None = None) -> None:
        """Show the popup centred on `anchor` (the wheel position)."""
        if anchor is not None:
            self.anchor = QPoint(anchor)
        self.adjustSize()
        self.place()
        self.setWindowOpacity(0.0)
        self.show()
        self.raise_()
        self.activateWindow()
        bring_to_front(int(self.winId()))
        self.setFocus(Qt.PopupFocusReason)
        self._fade.start()
        self._guard.start()
        QTimer.singleShot(120, self._refocus)   # Windows may hand over late

    def place(self) -> None:
        avail = screen_for(self.anchor).availableGeometry()
        self.setGeometry(popup_rect(self.anchor, self.size(), avail))

    def refit(self) -> None:
        """The content changed size (another page...): resize, stay on screen."""
        for lay in (self.card.layout(), self.layout()):
            lay.invalidate()
            lay.activate()
        self.resize(self.sizeHint())
        if self.isVisible():
            self.place()

    def _refocus(self) -> None:
        if self._done or not self.isVisible():
            return
        if not self.isActiveWindow():
            self.activateWindow()
            bring_to_front(int(self.winId()))

    def pause_dismiss(self, paused: bool) -> None:
        """Keep the popup open while one of our own dialogs is up."""
        if paused:
            self._guard.stop()
        elif not self._done:
            self._guard.resume()

    # -- result -----------------------------------------------------------------------------
    def finish(self, result: dict) -> None:
        if self._done:
            return
        self._done = True
        self._guard.stop()
        self.hide()
        self.accepted.emit(result)
        self.close()

    def cancel(self) -> None:
        if self._done:
            return
        self._done = True
        self._guard.stop()
        self.hide()
        self.cancelled.emit()
        self.close()

    def closeEvent(self, e):
        for loader in self.findChildren(Loader):
            loader.stop()
        if not self._done:
            self._done = True
            self._guard.stop()
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

    # kept for older callers
    def start(self) -> None:
        self.open_at()


def _elide(text: str, n: int) -> str:
    return text if len(text) <= n else text[: n - 1] + "…"
