"""The wheel shown at the cursor.

Levels: categories (when the selection mixes images, PDFs, videos and sounds),
then the actions of a category (the main ones, plus "Plus" for the others),
then the variants of an action (rotate left/right...). The centre shows the
file (a small preview), or what the action under the mouse does; it goes back
one level, or closes the wheel at the top. Choosing emits `chosen(action_id, opts)`.

It never captures the mouse nor covers the screen: it closes when Cerclic loses
the foreground (a click elsewhere), on Escape, or when the pointer clearly goes
away (see dismiss.py).
"""
from __future__ import annotations

import math
import sys
import time
from dataclasses import dataclass

from PySide6.QtCore import (QEasingCurve, QPointF, QRectF, Qt, QTimer,
                            QVariantAnimation, Signal)
from PySide6.QtGui import (QColor, QFontMetricsF, QGuiApplication, QImage,
                           QLinearGradient, QPainter, QPainterPath, QPen,
                           QRadialGradient)
from PySide6.QtWidgets import QWidget

from ..actions.registry import CATEGORIES, Action
from ..paths import kind_of
from ..win.foreground import bring_to_front
from .dismiss import DismissGuard
from .icons import draw_icon
from .theme import MUTED, TEXT, font, qcolor, under_white_text

RI = 64          # radius of the centre disc
RO = 158         # outer radius of the ring
POP = 7          # how far a hovered slice grows
PAD = 34         # room around the ring (shadow, hover growth)
MAX_SLICES = 8
LABEL_W = 92     # label width before it wraps on two lines

# frosted white glass (the light "Clair givré" style)
BASE_IN = QColor(255, 255, 255, 236)
BASE_OUT = QColor(244, 247, 253, 232)
CENTER = QColor(255, 255, 255, 250)
INK = QColor(27, 34, 50)


@dataclass
class Slice:
    id: str
    label: str
    icon: str
    color: QColor
    kind: str          # "category" | "action" | "more" | "choice"
    payload: object = None
    desc: str = ""


def _category_icon(cat_id: str) -> str:
    return {"image": "image", "pdf": "cat_pdf", "video": "cat_video",
            "audio": "cat_audio"}.get(cat_id, "dot")


def _mix(a: QColor, b: QColor, t: float) -> QColor:
    t = max(0.0, min(1.0, t))
    return QColor(round(a.red() + (b.red() - a.red()) * t),
                  round(a.green() + (b.green() - a.green()) * t),
                  round(a.blue() + (b.blue() - a.blue()) * t),
                  round(a.alpha() + (b.alpha() - a.alpha()) * t))


def _alpha(col: QColor, a: int) -> QColor:
    c = QColor(col)
    c.setAlpha(max(0, min(255, int(a))))
    return c


def load_preview(path: str, size: int):
    """Small picture of a file for the centre of the wheel (None if none)."""
    k = kind_of(path)
    if k == "image":
        from .crop_editor import load_image_preview
        return load_image_preview(path, size, size)[0]
    if k == "pdf":
        from ..actions.pdf import quick_to_draw
        if not quick_to_draw(path):         # a detailed plan would hold Cerclic up
            return None
        from .crop_editor import load_pdf_preview
        return load_pdf_preview(path, 0, size, size, None)[0]
    if k == "video":
        from ..actions import video
        info = video.probe(path, measure=False)      # (a frame near the start is enough)
        t = min(1.0, info.duration / 3) if info.duration else 0.0
        img = QImage.fromData(video.frame_png(path, t, size, size), "PNG")
        return img if not img.isNull() else None
    return None


class Wheel(QWidget):
    chosen = Signal(str, dict)
    cancelled = Signal()

    def __init__(self, menu: dict[str, list[Action]], counts: dict[str, int],
                 summary: str, preview: str | None = None):
        super().__init__(None, Qt.FramelessWindowHint | Qt.Tool
                         | Qt.WindowStaysOnTopHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAttribute(Qt.WA_MacAlwaysShowToolWindow)   # macOS: stays shown in the background
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
        self._touched = False         # the user pointed at a slice, clicked, typed
        self._done = False
        self._shown_at = 0.0
        self._glow: list[float] = []
        self._thumb: QImage | None = None
        self._thumb_fade = 0.0
        self._open = 1.0          # 0 -> 1 while the ring appears
        self._from_grow = 0.84
        self._reset_levels()

        self._guard = DismissGuard(self, self.cancel, leave_s=2.5, idle_s=30)
        self._anim = QVariantAnimation(self, duration=230, startValue=0.0, endValue=1.0)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
        self._anim.valueChanged.connect(self._on_anim)
        self._ticker = QTimer(self, interval=16)
        self._ticker.timeout.connect(self._step)
        if preview:
            self._load_preview(preview)

    # -- preview ------------------------------------------------------------------
    def _load_preview(self, path: str) -> None:
        from .editor_base import Loader
        self._loader = Loader(self)
        self._loader.done.connect(self._preview_ready)
        size = int(2 * RI * (self.devicePixelRatioF() or 1.0))
        self._loader.run(lambda: load_preview(path, size))

    def _preview_ready(self, img, err) -> None:
        if img is not None and not img.isNull():
            self._thumb = img
            self._thumb_fade = 0.0
            self._ticker.start()

    # -- levels ----------------------------------------------------------------
    @property
    def navigated(self) -> bool:
        return self._navigated

    @property
    def touched(self) -> bool:
        return self._touched or self._navigated

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
                                 _category_icon(cat_id), QColor(hexcol), "category",
                                 desc=f"{n} fichier{'s' if n > 1 else ''}"))
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
                out.append(Slice(a.id, a.label, a.icon, col, "action", a, a.desc))
            if level == "actions" and secondary:
                out.append(Slice("__more__", "Plus", "more", col, "more", cat_id,
                                 "D'autres outils"))
            if level == "actions" and not primary and secondary:
                out = [Slice(a.id, a.label, a.icon, col, "action", a, a.desc)
                       for a in secondary]
        elif level == "choices":
            action: Action = payload
            _, hexcol = CATEGORIES[action.category]
            col = QColor(hexcol)
            for c in action.choices:
                out.append(Slice(c.id, c.label, c.icon, col, "choice", (action, c),
                                 action.label))
        self._slices = out[:MAX_SLICES]
        self._glow = [0.0] * len(self._slices)
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
        self._start_anim(0.84)
        self.show()
        self.raise_()
        self.activateWindow()
        bring_to_front(int(self.winId()))
        self.setFocus(Qt.PopupFocusReason)
        self._shown_at = time.monotonic()
        self._guard.start()

    def _start_anim(self, grow_from: float, duration: int = 230) -> None:
        self._from_grow = grow_from
        self._open = 0.0
        self._anim.stop()
        self._anim.setDuration(duration)
        self._anim.start()
        self.update()

    def _bump(self) -> None:
        self._start_anim(0.93, 170)

    def _on_anim(self, v) -> None:
        self._open = float(v)
        self.update()

    def _step(self) -> None:
        """Ease the hover glow of every slice (and the preview fade-in)."""
        busy = False
        for i in range(len(self._glow)):
            target = 1.0 if i == self._hover else 0.0
            g = self._glow[i]
            if abs(g - target) > 0.01:
                self._glow[i] = g + (target - g) * 0.35
                busy = True
            else:
                self._glow[i] = target
        if self._thumb is not None and self._thumb_fade < 1.0:
            self._thumb_fade = min(1.0, self._thumb_fade + 0.12)
            busy = True
        self.update()
        if not busy:
            self._ticker.stop()

    def _set_hover(self, idx: int, centre: bool) -> None:
        if idx >= 0:
            self._touched = True
        if idx != self._hover or centre != self._center_hover:
            self._hover, self._center_hover = idx, centre
            self._ticker.start()
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
        step = 360.0 / len(self._slices)
        seg = (90 - ang + step / 2) % 360          # slice 0 is centred at the top
        return min(len(self._slices) - 1, int(seg / step))

    def slice_center(self, i: int) -> QPointF:
        """Middle of slice i, in widget coordinates (used by tests)."""
        n = len(self._slices)
        mid = math.radians(90 - i * 360.0 / n)
        rm = (RI + RO) / 2
        c = self._c()
        return QPointF(c.x() + rm * math.cos(mid), c.y() - rm * math.sin(mid))

    # -- painting --------------------------------------------------------------
    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.SmoothPixmapTransform, True)
        v = self._open
        ease = QEasingCurve(QEasingCurve.OutBack)
        ease.setOvershoot(1.3)
        g = self._from_grow + (1.0 - self._from_grow) * ease.valueForProgress(v)
        p.setOpacity(min(1.0, 0.15 + v * 1.7))
        c = self._c()
        ri, ro = RI * g, RO * g

        # soft shadow
        shadow = QRadialGradient(QPointF(c.x(), c.y() + 6), ro + PAD * 0.95)
        shadow.setColorAt(0.0, QColor(20, 40, 90, 70))
        shadow.setColorAt(ro / (ro + PAD * 0.95), QColor(20, 40, 90, 46))
        shadow.setColorAt(1.0, QColor(20, 40, 90, 0))
        p.setPen(Qt.NoPen)
        p.setBrush(shadow)
        p.drawEllipse(QPointF(c.x(), c.y() + 6), ro + PAD * 0.95, ro + PAD * 0.95)

        # the ring itself, like frosted glass
        ring = QPainterPath()
        ring.addEllipse(c, ro, ro)
        inner = QPainterPath()
        inner.addEllipse(c, ri, ri)
        ring = ring.subtracted(inner)
        base = QRadialGradient(c, ro)
        base.setColorAt(ri / ro, BASE_IN)
        base.setColorAt(1.0, BASE_OUT)
        p.fillPath(ring, base)
        sheen = QLinearGradient(QPointF(c.x(), c.y() - ro), QPointF(c.x(), c.y() + ro))
        sheen.setColorAt(0.0, QColor(255, 255, 255, 120))
        sheen.setColorAt(0.5, QColor(255, 255, 255, 0))
        p.fillPath(ring, sheen)
        p.setBrush(Qt.NoBrush)
        p.setPen(QPen(QColor(30, 50, 100, 40), 1))
        p.drawEllipse(c, ro, ro)
        p.setPen(QPen(QColor(255, 255, 255, 230), 1.4))
        p.drawEllipse(c, ro - 1.2, ro - 1.2)

        n = len(self._slices)
        if n:
            step = 360.0 / n
            gap = 1.6 if n > 1 else 0.0
            for i, s in enumerate(self._slices):
                appear = max(0.0, min(1.0, (v - i * 0.045) / 0.55))
                if appear <= 0:
                    continue
                h = self._glow[i] if i < len(self._glow) else 0.0
                outer = ro + POP * h * g
                start = 90 - i * step - step / 2 + gap / 2
                path = _donut_segment(c, ri + 3, outer, start, step - gap)
                p.save()
                p.setOpacity(p.opacity() * appear)
                p.fillPath(path, QColor(30, 50, 100, 7))
                if h > 0.01:
                    deep = under_white_text(s.color)       # the label reads on it
                    fill = QRadialGradient(c, outer)
                    fill.setColorAt(ri / max(outer, 1), _alpha(deep.darker(106), 240 * h))
                    fill.setColorAt(1.0, _alpha(deep, 250 * h))
                    p.fillPath(path, fill)
                    p.setPen(QPen(_alpha(QColor(255, 255, 255), 200 * h), 1.2))
                    p.setBrush(Qt.NoBrush)
                    p.drawPath(path)
                mid = math.radians(90 - i * step)
                rm = (ri + outer) / 2 + 2
                ix = c.x() + rm * math.cos(mid)
                iy = c.y() - rm * math.sin(mid)
                icon_col = _mix(s.color.darker(106), QColor(255, 255, 255), h)
                text_col = _mix(QColor(43, 51, 69), QColor(255, 255, 255), h)
                lines = self._label_lines(s.label)
                lift = 6 if len(lines) > 1 else 0
                draw_icon(p, s.icon, ix, iy - 11 * g - lift, 25 * g, icon_col)
                p.setFont(self._label_font(lines))
                p.setPen(text_col)
                for k, line in enumerate(lines):
                    p.drawText(QRectF(ix - 60, iy + 5 * g - lift + k * 13, 120, 16),
                               Qt.AlignCenter, line)
                p.restore()

        # centre
        p.setPen(Qt.NoPen)
        cg = QRadialGradient(QPointF(c.x(), c.y() - ri * 0.4), ri * 1.4)
        cg.setColorAt(0.0, CENTER)
        cg.setColorAt(1.0, QColor(238, 243, 251, 250))
        p.setBrush(cg)
        p.drawEllipse(c, ri, ri)
        self._paint_center(p, c, ri)
        ring_col = QColor(46, 124, 246, 120) if self._center_hover else QColor(30, 50, 100, 38)
        p.setPen(QPen(ring_col, 1.2))
        p.setBrush(Qt.NoBrush)
        p.drawEllipse(c, ri, ri)

    @staticmethod
    def _label_font(lines: list[str]):
        """8.6 pt, a little smaller for a single long word (Redimensionner)."""
        size = 8.6
        while size > 7.4:
            fm = QFontMetricsF(font(size, bold=True))
            if max(fm.horizontalAdvance(t) for t in lines) <= LABEL_W + 4:
                break
            size -= 0.3
        return font(size, bold=True)

    def _label_lines(self, text: str) -> list[str]:
        fm = QFontMetricsF(font(8.6, bold=True))
        if fm.horizontalAdvance(text) <= LABEL_W or " " not in text:
            return [text]
        words = text.split(" ")
        best = None
        for k in range(1, len(words)):
            a, b = " ".join(words[:k]), " ".join(words[k:])
            w = max(fm.horizontalAdvance(a), fm.horizontalAdvance(b))
            if best is None or w < best[0]:
                best = (w, [a, b])
        return best[1]

    def _paint_center(self, p: QPainter, c: QPointF, ri: float) -> None:
        hovered = self._slices[self._hover] if 0 <= self._hover < len(self._slices) else None
        title = self._title()
        if hovered is not None and hovered.desc:
            p.setPen(qcolor(TEXT))
            p.setFont(font(9.6, bold=True))
            p.drawText(QRectF(c.x() - ri + 8, c.y() - 26, 2 * ri - 16, 20),
                       Qt.AlignCenter, hovered.label)
            p.setPen(_mix(QColor(MUTED), hovered.color.darker(120), 0.35))
            p.setFont(font(8.2))
            p.drawText(QRectF(c.x() - ri + 10, c.y() - 4, 2 * ri - 20, 32),
                       Qt.AlignHCenter | Qt.AlignTop | Qt.TextWordWrap, hovered.desc)
            return
        if title:
            p.setPen(qcolor(TEXT))
            p.setFont(font(9.6, bold=True))
            p.drawText(QRectF(c.x() - ri + 6, c.y() - 22, 2 * ri - 12, 20),
                       Qt.AlignCenter, title)
            p.setPen(qcolor(TEXT if self._center_hover else MUTED))
            p.setFont(font(8.6))
            p.drawText(QRectF(c.x() - ri, c.y() + 2, 2 * ri, 20), Qt.AlignCenter,
                       "‹ Retour")
            return
        if self._thumb is not None:
            clip = QPainterPath()
            clip.addEllipse(c, ri - 3, ri - 3)
            p.save()
            p.setClipPath(clip)
            p.setOpacity(p.opacity() * (0.35 + 0.65 * self._thumb_fade))
            img = self._thumb
            d = 2 * (ri - 3)
            s = max(d / img.width(), d / img.height())
            w, h = img.width() * s, img.height() * s
            p.drawImage(QRectF(c.x() - w / 2, c.y() - h / 2, w, h), img)
            veil = QLinearGradient(QPointF(c.x(), c.y()), QPointF(c.x(), c.y() + ri))
            veil.setColorAt(0.0, QColor(0, 0, 0, 0))
            veil.setColorAt(0.55, QColor(0, 0, 0, 170))
            veil.setColorAt(1.0, QColor(0, 0, 0, 220))
            p.fillRect(QRectF(c.x() - ri, c.y(), 2 * ri, ri), veil)
            p.restore()
            p.setPen(QColor(255, 255, 255, 235))
            p.setFont(font(8.0, bold=True))
            p.drawText(QRectF(c.x() - ri + 14, c.y() + ri * 0.28, 2 * ri - 28, 18),
                       Qt.AlignCenter, self._summary)
            return
        p.setPen(qcolor(TEXT if self._center_hover else MUTED))
        p.setFont(font(8.8))
        p.drawText(QRectF(c.x() - ri + 8, c.y() - 20, 2 * ri - 16, 40),
                   Qt.AlignCenter | Qt.TextWordWrap, self._summary)

    # -- interaction -------------------------------------------------------------
    def mouseMoveEvent(self, e):
        idx = self.index_at(e.position())
        self._set_hover(idx if idx >= 0 else -1, idx == -2)

    def leaveEvent(self, _):
        self._set_hover(-1, False)

    def mousePressEvent(self, e):
        self._touched = True
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
        self._touched = True
        k = e.key()
        n = len(self._slices)
        number = _slice_number(e)
        if k in (Qt.Key_Escape, Qt.Key_Backspace):
            self._back()
        elif number is not None:
            if number < n:
                self.activate(number)
        elif k in (Qt.Key_Right, Qt.Key_Down, Qt.Key_Tab) and n:
            self._set_hover((self._hover + 1) % n, False)
        elif k in (Qt.Key_Left, Qt.Key_Up, Qt.Key_Backtab) and n:
            self._set_hover((self._hover - 1) % n if self._hover >= 0 else n - 1, False)
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
        self._ticker.stop()
        self.hide()
        self.chosen.emit(action_id, opts)
        self.close()

    def cancel(self) -> None:
        if self._done:
            return
        self._done = True
        self._guard.stop()
        self._ticker.stop()
        self.hide()
        self.cancelled.emit()
        self.close()


# The digit row of an AZERTY keyboard types & é " ' ( - è _ ç without Maj.
_AZERTY_DIGITS = {Qt.Key_Ampersand: 0, Qt.Key_Eacute: 1, Qt.Key_QuoteDbl: 2,
                  Qt.Key_Apostrophe: 3, Qt.Key_ParenLeft: 4, Qt.Key_Minus: 5,
                  Qt.Key_Egrave: 6, Qt.Key_Underscore: 7, Qt.Key_Ccedilla: 8}


def _slice_number(e) -> int | None:
    """0 for the 1 key... 8 for the 9 key, whatever the keyboard layout
    (top row with or without Maj, numeric keypad); None for other keys."""
    if sys.platform == "win32":
        vk = e.nativeVirtualKey()
        if 0x31 <= vk <= 0x39:
            return vk - 0x31
        if 0x61 <= vk <= 0x69:
            return vk - 0x61
    k = e.key()
    if Qt.Key_1 <= k <= Qt.Key_9:
        return k - Qt.Key_1
    return _AZERTY_DIGITS.get(k)


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
