"""The wheel shown at the cursor.

Levels: categories (when the selection mixes images, PDFs and videos), then the
actions of a category (the main ones, plus "Plus" for the others), then the
variants of an action (rotate left/right...). The centre goes back one level, or
closes the wheel at the top. Choosing an action emits `chosen(action_id, opts)`.

It never captures the mouse nor covers the screen: it closes when Cerclic loses
the foreground (a click elsewhere), on Escape, or when the pointer clearly goes
away (see dismiss.py).
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass

from PySide6.QtCore import (QEasingCurve, QPointF, QRectF, Qt,
                            QVariantAnimation, Signal)
from PySide6.QtGui import (QColor, QGuiApplication, QPainter, QPainterPath, QPen,
                           QRadialGradient)
from PySide6.QtWidgets import QWidget

from ..actions.registry import CATEGORIES, Action
from ..win.foreground import bring_to_front
from .dismiss import DismissGuard
from .icons import draw_icon
from .theme import MUTED, TEXT, font, qcolor

RI = 60          # inner radius (centre button)
RO = 148         # outer radius of the ring
POP = 8          # how far a hovered slice grows
PAD = 30         # room around the ring (shadow, hover growth)
MAX_SLICES = 8

RING = QColor(36, 39, 49, 245)
RING_HOVER = QColor(52, 56, 70, 250)
CENTER = QColor(26, 28, 36, 250)


@dataclass
class Slice:
    id: str
    label: str
    icon: str
    color: QColor
    kind: str          # "category" | "action" | "more" | "choice"
    payload: object = None


def _category_icon(cat_id: str) -> str:
    return {"image": "image", "pdf": "cat_pdf", "video": "cat_video"}.get(cat_id, "dot")


class Wheel(QWidget):
    chosen = Signal(str, dict)
    cancelled = Signal()

    def __init__(self, menu: dict[str, list[Action]], counts: dict[str, int],
                 summary: str):
        super().__init__(None, Qt.FramelessWindowHint | Qt.Tool
                         | Qt.WindowStaysOnTopHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setWindowTitle("Cerclic")
        side = 2 * (RO + PAD)
        self.setFixedSize(side, side)

        self._menu, self._counts, self._summary = menu, counts, summary
        self._stack: list[tuple[str, object]] = []   # (level, payload)
        self._slices: list[Slice] = []
        self._hover = -1
        self._center_hover = False
        self._pressed_inside = False
        self._navigated = False
        self._done = False
        self._shown_at = 0.0
        self._grow = self._g0 = 1.0
        self._fade = self._f0 = 1.0
        self._reset_levels()

        self._guard = DismissGuard(self, self.cancel, leave_s=2.5, idle_s=30)
        self._anim = QVariantAnimation(self, duration=170, startValue=0.0, endValue=1.0)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
        self._anim.valueChanged.connect(self._on_anim)

    # -- levels ----------------------------------------------------------------
    @property
    def navigated(self) -> bool:
        return self._navigated

    def _reset_levels(self) -> None:
        if len(self._menu) == 1:
            self._stack = [("actions", next(iter(self._menu)))]
        else:
            self._stack = [("categories", None)]
        self._rebuild()

    def set_menu(self, menu, counts, summary) -> None:
        """Replace the content (more files arrived) while still at the top."""
        self._menu, self._counts, self._summary = menu, counts, summary
        self._reset_levels()
        self.update()

    def _rebuild(self) -> None:
        level, payload = self._stack[-1]
        out: list[Slice] = []
        if level == "categories":
            for cat_id in self._menu:
                label, hexcol = CATEGORIES[cat_id]
                n = self._counts.get(cat_id, 0)
                out.append(Slice(cat_id, f"{label} ({n})" if n > 1 else label,
                                 _category_icon(cat_id), QColor(hexcol), "category"))
        elif level in ("actions", "more"):
            cat_id = payload
            _, hexcol = CATEGORIES[cat_id]
            col = QColor(hexcol)
            actions = self._menu.get(cat_id, [])
            primary = [a for a in actions if a.primary]
            secondary = [a for a in actions if not a.primary]
            if level == "more":
                chosen = secondary
            elif secondary and len(primary) + 1 > MAX_SLICES:
                chosen = primary[:MAX_SLICES - 1]
            else:
                chosen = primary
            for a in chosen:
                out.append(Slice(a.id, a.label, a.icon, col, "action", a))
            if level == "actions" and secondary:
                out.append(Slice("__more__", "Plus", "more", col, "more", cat_id))
            if level == "actions" and not primary and secondary:
                out = [Slice(a.id, a.label, a.icon, col, "action", a) for a in secondary]
        elif level == "choices":
            action: Action = payload
            _, hexcol = CATEGORIES[action.category]
            col = QColor(hexcol)
            for c in action.choices:
                out.append(Slice(c.id, c.label, c.icon, col, "choice", (action, c)))
        self._slices = out[:MAX_SLICES]
        self._hover = -1

    def _push(self, level: str, payload) -> None:
        self._navigated = True
        self._stack.append((level, payload))
        self._rebuild()
        self._bump()

    def _back(self) -> None:
        if len(self._stack) > 1:
            self._navigated = True
            self._stack.pop()
            self._rebuild()
            self._bump()
        else:
            self.cancel()

    def _title(self) -> str:
        level, payload = self._stack[-1]
        if level == "more":
            return "Plus"
        if level == "choices":
            return payload.label
        if level == "actions" and len(self._stack) > 1:
            return CATEGORIES[payload][0]
        return ""

    # -- show / animation ------------------------------------------------------
    def popup_at(self, pos) -> None:
        """Show centred on `pos` (logical coordinates), kept inside its screen."""
        side = self.width()
        screen = QGuiApplication.screenAt(pos) or QGuiApplication.primaryScreen()
        geo = screen.geometry()
        left = int(pos.x() - side / 2)
        top = int(pos.y() - side / 2)
        left = max(geo.left(), min(left, geo.right() + 1 - side))
        top = max(geo.top(), min(top, geo.bottom() + 1 - side))
        self.move(left, top)
        self._start_anim(0.86, 0.0)
        self.show()
        self.raise_()
        self.activateWindow()
        bring_to_front(int(self.winId()))
        self.setFocus(Qt.PopupFocusReason)
        self._shown_at = time.monotonic()
        self._guard.start()

    def _start_anim(self, grow: float, fade: float) -> None:
        self._g0, self._f0 = grow, fade
        self._grow, self._fade = grow, fade
        self._anim.stop()
        self._anim.start()
        self.update()

    def _bump(self) -> None:
        self._start_anim(0.94, 0.6)

    def _on_anim(self, v) -> None:
        v = float(v)
        self._grow = self._g0 + (1.0 - self._g0) * v
        self._fade = self._f0 + (1.0 - self._f0) * v
        self.update()

    # -- geometry --------------------------------------------------------------
    def _c(self) -> QPointF:
        return QPointF(self.width() / 2, self.height() / 2)

    def index_at(self, pos: QPointF) -> int:
        """Slice index under pos; -2 for the centre, -1 outside."""
        c = self._c()
        dx, dy = pos.x() - c.x(), pos.y() - c.y()
        dist = math.hypot(dx, dy)
        if dist < RI:
            return -2
        if dist > RO + POP or not self._slices:
            return -1
        ang = math.degrees(math.atan2(-dy, dx))
        seg = (90 - ang) % 360
        return min(len(self._slices) - 1, int(seg / (360.0 / len(self._slices))))

    def slice_center(self, i: int) -> QPointF:
        """Middle of slice i, in widget coordinates (used by tests)."""
        n = len(self._slices)
        mid = math.radians(90 - (i + 0.5) * 360.0 / n)
        rm = (RI + RO) / 2
        c = self._c()
        return QPointF(c.x() + rm * math.cos(mid), c.y() - rm * math.sin(mid))

    # -- painting --------------------------------------------------------------
    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setOpacity(max(0.0, min(1.0, self._fade)))
        c = self._c()
        g = self._grow
        ri, ro = RI * g, RO * g

        # soft shadow
        shadow = QRadialGradient(c, ro + PAD * 0.9)
        shadow.setColorAt(0.0, QColor(0, 0, 0, 110))
        shadow.setColorAt(ro / (ro + PAD * 0.9), QColor(0, 0, 0, 70))
        shadow.setColorAt(1.0, QColor(0, 0, 0, 0))
        p.setPen(Qt.NoPen)
        p.setBrush(shadow)
        p.drawEllipse(c, ro + PAD * 0.9, ro + PAD * 0.9)

        n = len(self._slices)
        if n:
            step = 360.0 / n
            gap = 1.2 if n > 1 else 0.0
            for i, s in enumerate(self._slices):
                hov = i == self._hover
                outer = ro + (POP * g if hov else 0)
                start = 90 - (i + 1) * step + gap / 2
                path = _donut_segment(c, ri + 2, outer, start, step - gap)
                p.fillPath(path, RING_HOVER if hov else RING)
                if hov:
                    glow = QColor(s.color)
                    glow.setAlpha(60)
                    p.fillPath(path, glow)
                p.setPen(QPen(s.color if hov else _alpha(s.color, 90), 2 if hov else 1.2))
                p.setBrush(Qt.NoBrush)
                p.drawPath(path)

                mid = math.radians(90 - (i + 0.5) * step)
                rm = (ri + outer) / 2
                ix = c.x() + rm * math.cos(mid)
                iy = c.y() - rm * math.sin(mid)
                col = QColor(TEXT) if hov else QColor(200, 204, 214)
                draw_icon(p, s.icon, ix, iy - 9 * g, 24 * g, s.color if hov else col)
                p.setFont(font(8.6, bold=True))
                p.setPen(col)
                p.drawText(QRectF(ix - 58, iy + 7 * g, 116, 18), Qt.AlignCenter, s.label)

        # centre button
        grad = QRadialGradient(c, ri)
        grad.setColorAt(0, CENTER)
        grad.setColorAt(1, _alpha(CENTER, 235))
        p.setBrush(grad)
        p.setPen(QPen(QColor(70, 74, 90) if self._center_hover else QColor(52, 56, 70), 1.4))
        p.drawEllipse(c, ri, ri)
        self._paint_center(p, c, ri)

    def _paint_center(self, p: QPainter, c: QPointF, ri: float) -> None:
        title = self._title()
        if title:
            p.setPen(qcolor(TEXT))
            p.setFont(font(9.5, bold=True))
            p.drawText(QRectF(c.x() - ri + 6, c.y() - 22, 2 * ri - 12, 20),
                       Qt.AlignCenter, title)
            p.setPen(qcolor(TEXT if self._center_hover else MUTED))
            p.setFont(font(8.6))
            p.drawText(QRectF(c.x() - ri, c.y() + 2, 2 * ri, 20), Qt.AlignCenter,
                       "‹ Retour")
        else:
            p.setPen(qcolor(TEXT if self._center_hover else MUTED))
            p.setFont(font(8.8))
            p.drawText(QRectF(c.x() - ri + 8, c.y() - 20, 2 * ri - 16, 40),
                       Qt.AlignCenter | Qt.TextWordWrap, self._summary)

    # -- interaction -------------------------------------------------------------
    def mouseMoveEvent(self, e):
        idx = self.index_at(e.position())
        hv = idx if idx >= 0 else -1
        ch = idx == -2
        if hv != self._hover or ch != self._center_hover:
            self._hover, self._center_hover = hv, ch
            self.update()

    def leaveEvent(self, _):
        if self._hover != -1 or self._center_hover:
            self._hover, self._center_hover = -1, False
            self.update()

    def mousePressEvent(self, e):
        self._pressed_inside = True
        if e.button() == Qt.RightButton:
            self._back()
            self._pressed_inside = False

    def mouseReleaseEvent(self, e):
        if not self._pressed_inside or e.button() != Qt.LeftButton:
            return
        self._pressed_inside = False
        idx = self.index_at(e.position())
        if idx == -2:
            self._back()
        elif idx == -1:
            self.cancel()
        else:
            self.activate(idx)

    def keyPressEvent(self, e):
        k = e.key()
        n = len(self._slices)
        if k == Qt.Key_Escape:
            self._back()
        elif k == Qt.Key_Backspace:
            self._back()
        elif Qt.Key_1 <= k <= Qt.Key_9:
            i = k - Qt.Key_1
            if i < n:
                self.activate(i)
        elif k in (Qt.Key_Right, Qt.Key_Down, Qt.Key_Tab) and n:
            self._hover = (self._hover + 1) % n
            self.update()
        elif k in (Qt.Key_Left, Qt.Key_Up, Qt.Key_Backtab) and n:
            self._hover = (self._hover - 1) % n if self._hover >= 0 else n - 1
            self.update()
        elif k in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Space) and self._hover >= 0:
            self.activate(self._hover)

    def focusNextPrevChild(self, _next: bool) -> bool:
        return False  # keep Tab for moving around the ring

    def activate(self, idx: int) -> None:
        if self._done or not (0 <= idx < len(self._slices)):
            return
        s = self._slices[idx]
        if s.kind == "category":
            self._push("actions", s.id)
        elif s.kind == "more":
            self._push("more", s.payload)
        elif s.kind == "action":
            action: Action = s.payload
            if action.choices:
                self._push("choices", action)
            else:
                self._finish(action.id, {})
        elif s.kind == "choice":
            action, choice = s.payload
            self._finish(action.id, choice.as_opts())

    def _finish(self, action_id: str, opts: dict) -> None:
        self._done = True
        self._guard.stop()
        self.hide()
        self.chosen.emit(action_id, opts)
        self.close()

    def cancel(self) -> None:
        if self._done:
            return
        self._done = True
        self._guard.stop()
        self.hide()
        self.cancelled.emit()
        self.close()


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


def _alpha(col: QColor, a: int) -> QColor:
    c = QColor(col)
    c.setAlpha(a)
    return c
