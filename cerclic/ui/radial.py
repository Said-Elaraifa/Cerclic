"""The radial (pie) menu shown at the cursor.

Navigation is internal: when several categories apply, the first ring shows the
categories and the centre cancels; choosing one swaps to a ring of its actions
with the centre acting as back. When a single category applies, its actions show
at once. Selecting a slice emits `selected(action_id)`.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass

from PySide6.QtCore import Qt, QRectF, QPointF, Signal, QVariantAnimation, QEasingCurve
from PySide6.QtGui import (QPainter, QColor, QPainterPath, QPen, QFont,
                           QGuiApplication, QRadialGradient)
from PySide6.QtWidgets import QWidget

from .icons import draw_icon
from ..actions.registry import CATEGORIES


@dataclass
class Slice:
    id: str
    label: str
    icon: str
    color: QColor
    kind: str  # "category" | "action"


THEME = {
    "dark": {
        "bg": QColor(22, 24, 30, 235),
        "ring": QColor(38, 41, 51, 255),
        "ring_hi": QColor(58, 62, 76, 255),
        "text": QColor(236, 238, 243),
        "sub": QColor(150, 156, 170),
        "center": QColor(28, 30, 38, 245),
    },
}

RI = 66      # inner radius
RO = 150     # outer radius
PAD = 26     # breathing room to the window edge


class RadialMenu(QWidget):
    selected = Signal(str)
    cancelled = Signal()

    def __init__(self, menu: dict, summary: str, theme: str = "dark",
                 primary_only: bool = False):
        super().__init__(None, Qt.FramelessWindowHint | Qt.Tool
                         | Qt.WindowStaysOnTopHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setMouseTracking(True)
        self._t = THEME.get(theme, THEME["dark"])
        self._menu = menu
        self._summary = summary
        self._primary_only = primary_only
        self._hover = -1
        self._grow = 1.0
        self._shown_at = 0.0
        self._closed = False

        self._single = len(menu) == 1
        self._level = "actions" if self._single else "categories"
        self._cat = next(iter(menu)) if self._single else ""
        self._slices: list[Slice] = []
        self._rebuild()

        side = 2 * (RO + PAD)
        self.resize(side, side)

        self._anim = QVariantAnimation(self, duration=140,
                                       startValue=0.82, endValue=1.0)
        self._anim.setEasingCurve(QEasingCurve.OutBack)
        self._anim.valueChanged.connect(self._on_grow)

    # -- data ----------------------------------------------------------------
    def _rebuild(self) -> None:
        self._slices = []
        if self._level == "categories":
            for cat_id, actions in self._menu.items():
                label, hexcol = CATEGORIES[cat_id]
                self._slices.append(Slice(cat_id, label, _cat_icon(cat_id),
                                          QColor(hexcol), "category"))
        else:
            actions = self._menu[self._cat]
            if self._primary_only and any(a.primary for a in actions):
                actions = [a for a in actions if a.primary]
            _, hexcol = CATEGORIES[self._cat]
            col = QColor(hexcol)
            for a in actions:
                self._slices.append(Slice(a.id, a.label, a.icon, col, "action"))
        self._hover = -1

    # -- show ----------------------------------------------------------------
    def popup_at(self, x: int, y: int) -> None:
        side = self.width()
        screen = QGuiApplication.screenAt(QPointF(x, y).toPoint()) \
            or QGuiApplication.primaryScreen()
        geo = screen.availableGeometry()
        left = int(x - side / 2)
        top = int(y - side / 2)
        left = max(geo.left(), min(left, geo.right() - side))
        top = max(geo.top(), min(top, geo.bottom() - side))
        self.move(left, top)
        self.show()
        self.raise_()
        self.activateWindow()
        self.setFocus(Qt.PopupFocusReason)
        self.grabMouse()
        self._shown_at = time.monotonic()
        self._anim.start()

    def _on_grow(self, v) -> None:
        self._grow = float(v)
        self.update()

    # -- geometry ------------------------------------------------------------
    def _center(self) -> QPointF:
        return QPointF(self.width() / 2, self.height() / 2)

    def _index_at(self, pos: QPointF) -> int:
        c = self._center()
        dx, dy = pos.x() - c.x(), pos.y() - c.y()
        dist = math.hypot(dx, dy)
        if dist < RI or dist > RO:
            return -2 if dist < RI else -1  # -2 = centre, -1 = outside
        n = len(self._slices)
        if n == 0:
            return -1
        ang = math.degrees(math.atan2(-dy, dx))
        seg = (90 - ang) % 360
        return int(seg / (360.0 / n))

    # -- paint ---------------------------------------------------------------
    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        c = self._center()
        g = self._grow
        ri, ro = RI * g, RO * g
        n = len(self._slices)

        if n:
            step = 360.0 / n
            for i, s in enumerate(self._slices):
                start = 90 - (i + 1) * step
                path = _donut_segment(c, ri, ro, start, step)
                base = self._t["ring_hi"] if i == self._hover else self._t["ring"]
                p.fillPath(path, base)
                # a thin coloured rim hints the category colour
                p.setPen(QPen(s.color if i == self._hover else
                              _dim(s.color, 120), 2))
                p.drawPath(path)
                mid = math.radians(90 - (i + 0.5) * step)
                rmid = (ri + ro) / 2
                ix = c.x() + rmid * math.cos(mid)
                iy = c.y() - rmid * math.sin(mid) - 10 * g
                col = self._t["text"] if i == self._hover else self._t["sub"]
                draw_icon(p, s.icon, ix, iy, 26 * g, col)
                self._draw_label(p, s.label, c, mid, ro, col)

        # centre disc
        grad = QRadialGradient(c, ri)
        grad.setColorAt(0, self._t["center"])
        grad.setColorAt(1, _dim(self._t["center"], 230))
        p.setBrush(grad)
        p.setPen(QPen(self._t["ring_hi"], 1))
        p.drawEllipse(c, ri, ri)
        self._draw_center(p, c, ri)

    def _draw_label(self, p, text, c, mid, ro, col):
        f = QFont("Segoe UI", 9)
        f.setBold(True)
        p.setFont(f)
        rlbl = (RI + RO) / 2 * self._grow + 20 * self._grow
        lx = c.x() + rlbl * math.cos(mid)
        ly = c.y() - rlbl * math.sin(mid) + 16 * self._grow
        p.setPen(col)
        p.drawText(QRectF(lx - 60, ly - 10, 120, 20), Qt.AlignCenter, text)

    def _draw_center(self, p, c, ri):
        p.setPen(self._t["text"])
        if self._level == "actions" and not self._single:
            f = QFont("Segoe UI", 16)
            p.setFont(f)
            p.drawText(QRectF(c.x() - ri, c.y() - ri, ri * 2, ri * 2),
                       Qt.AlignCenter, "‹  retour")
        else:
            f = QFont("Segoe UI", 10)
            p.setFont(f)
            p.setPen(self._t["sub"])
            p.drawText(QRectF(c.x() - ri + 6, c.y() - 18, ri * 2 - 12, 36),
                       Qt.AlignCenter, self._summary)

    # -- interaction ---------------------------------------------------------
    def mouseMoveEvent(self, e):
        pos = e.position()
        c = self._center()
        # Moving well past the ring dismisses the wheel, like most pie menus.
        if math.hypot(pos.x() - c.x(), pos.y() - c.y()) > RO + 90:
            self._cancel()
            return
        idx = self._index_at(pos)
        hv = idx if idx >= 0 else -1
        if hv != self._hover:
            self._hover = hv
            self.update()

    def leaveEvent(self, _):
        # Without a mouse grab the window stops getting moves once the cursor
        # leaves it: treat that as a cancel too (ignore the first instant).
        if time.monotonic() - self._shown_at > 0.25:
            self._cancel()

    def mouseReleaseEvent(self, e):
        idx = self._index_at(e.position())
        if idx == -2:            # centre
            self._activate_center()
        elif idx == -1:          # clicked outside the ring: dismiss
            self._cancel()
        else:
            self._choose(idx)

    def keyPressEvent(self, e):
        k = e.key()
        if k in (Qt.Key_Escape,):
            self._activate_center() if self._level == "actions" \
                and not self._single else self._cancel()
        elif k in (Qt.Key_Backspace,):
            self._activate_center()
        elif Qt.Key_1 <= k <= Qt.Key_9:
            i = k - Qt.Key_1
            if i < len(self._slices):
                self._choose(i)
        elif k in (Qt.Key_Return, Qt.Key_Enter) and self._hover >= 0:
            self._choose(self._hover)

    def _activate_center(self):
        if self._level == "actions" and not self._single:
            self._level = "categories"
            self._cat = ""
            self._rebuild()
            self.update()
        else:
            self._cancel()

    def _choose(self, idx):
        if idx >= len(self._slices):
            return
        s = self._slices[idx]
        if s.kind == "category":
            self._cat = s.id
            self._level = "actions"
            self._rebuild()
            self.update()
        else:
            if self._closed:
                return
            self._closed = True
            self.close()
            self.selected.emit(s.id)

    def _cancel(self):
        if self._closed:
            return
        self._closed = True
        self.close()
        self.cancelled.emit()

    def closeEvent(self, e):
        try:
            self.releaseMouse()
        except Exception:
            pass
        super().closeEvent(e)


def _donut_segment(c: QPointF, ri: float, ro: float, start_deg: float,
                   span_deg: float) -> QPainterPath:
    path = QPainterPath()
    outer = QRectF(c.x() - ro, c.y() - ro, 2 * ro, 2 * ro)
    inner = QRectF(c.x() - ri, c.y() - ri, 2 * ri, 2 * ri)
    path.arcMoveTo(outer, start_deg)
    path.arcTo(outer, start_deg, span_deg)
    path.arcTo(inner, start_deg + span_deg, -span_deg)
    path.closeSubpath()
    return path


def _dim(col: QColor, a: int) -> QColor:
    c = QColor(col)
    c.setAlpha(a)
    return c


def _cat_icon(cat_id: str) -> str:
    return {"image": "crop", "pdf": "topdf", "video": "mp4", "ai": "compress"}.get(
        cat_id, "dot")
