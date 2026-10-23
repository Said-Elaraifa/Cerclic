"""Frosted-glass building blocks: the pastel backdrop, glass panels, switches,
sidebar items and the setting rows of Cerclic's window.

Everything is painted (no images, no platform blur), so it looks the same on
Windows and macOS and never depends on a graphics driver.
"""
from __future__ import annotations

from PySide6.QtCore import (QEasingCurve, QPointF, QRectF, QSize, Qt,
                            QVariantAnimation, Signal)
from PySide6.QtGui import (QColor, QLinearGradient, QPainter, QPainterPath, QPen,
                           QPixmap, QRadialGradient)
from PySide6.QtWidgets import (QAbstractButton, QCheckBox, QHBoxLayout, QLabel,
                               QSizePolicy, QVBoxLayout, QWidget)

from .icons import draw_icon
from .theme import (ACCENT, ACCENT_SOFT, BORDER, FAINT, MUTED, OUTLINE, TEXT, TEXT_SOFT,
                    font)

# soft colour clouds behind the glass: (x, y as fractions, radius, colour)
_BLOBS = [(0.08, 0.10, 0.55, QColor(120, 176, 255, 120)),
          (0.92, 0.18, 0.50, QColor(196, 160, 255, 105)),
          (0.70, 0.95, 0.60, QColor(110, 214, 190, 95)),
          (0.15, 0.85, 0.45, QColor(255, 196, 214, 70))]


def paint_backdrop(p: QPainter, rect: QRectF) -> None:
    g = QLinearGradient(rect.topLeft(), rect.bottomRight())
    g.setColorAt(0.0, QColor("#EEF4FF"))
    g.setColorAt(0.55, QColor("#F5F3FF"))
    g.setColorAt(1.0, QColor("#EEF8F6"))
    p.fillRect(rect, g)
    span = max(rect.width(), rect.height())
    for fx, fy, fr, col in _BLOBS:
        c = QPointF(rect.left() + fx * rect.width(), rect.top() + fy * rect.height())
        rg = QRadialGradient(c, fr * span)
        rg.setColorAt(0.0, col)
        edge = QColor(col)
        edge.setAlpha(0)
        rg.setColorAt(1.0, edge)
        p.fillRect(rect, rg)


def paint_glass(p: QPainter, rect: QRectF, radius: float = 16.0, alpha: int = 168,
                shadow: bool = True) -> None:
    """A frosted panel: translucent white, a light sheen, a bright top edge."""
    p.save()
    p.setRenderHint(QPainter.Antialiasing, True)
    if shadow:
        for i, a in enumerate((10, 7, 4)):
            r = rect.adjusted(-1 - i, 1 + i, 1 + i, 3 + 2 * i)
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(30, 50, 100, a))
            p.drawRoundedRect(r, radius + i + 1, radius + i + 1)
    path = QPainterPath()
    path.addRoundedRect(rect, radius, radius)
    fill = QLinearGradient(rect.topLeft(), rect.bottomLeft())
    fill.setColorAt(0.0, QColor(255, 255, 255, min(255, alpha + 40)))
    fill.setColorAt(1.0, QColor(255, 255, 255, alpha))
    p.fillPath(path, fill)
    p.setPen(QPen(QColor(255, 255, 255, 230), 1.2))
    p.setBrush(Qt.NoBrush)
    p.drawRoundedRect(rect.adjusted(0.6, 0.6, -0.6, -0.6), radius, radius)
    p.setPen(QPen(QColor(30, 50, 100, 26), 1))
    p.drawRoundedRect(rect.adjusted(-0.5, -0.5, 0.5, 0.5), radius + 0.5, radius + 0.5)
    p.restore()


class Backdrop(QWidget):
    """The window background: the pastel clouds, drawn once per size."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._cache: QPixmap | None = None
        self.setAttribute(Qt.WA_StyledBackground, False)

    def paintEvent(self, _):
        dpr = self.devicePixelRatioF() or 1.0
        want = QSize(max(1, int(self.width() * dpr)), max(1, int(self.height() * dpr)))
        if self._cache is None or self._cache.size() != want:
            pix = QPixmap(want)
            pix.setDevicePixelRatio(dpr)
            q = QPainter(pix)
            paint_backdrop(q, QRectF(0, 0, self.width(), self.height()))
            q.end()
            self._cache = pix
        p = QPainter(self)
        p.drawPixmap(0, 0, self._cache)


class GlassPanel(QWidget):
    """A frosted card holding other widgets."""

    def __init__(self, parent=None, radius: float = 16.0, alpha: int = 168,
                 shadow: bool = True):
        super().__init__(parent)
        self.radius, self.alpha, self.shadow = radius, alpha, shadow

    def paintEvent(self, _):
        p = QPainter(self)
        r = QRectF(self.rect()).adjusted(2, 1, -2, -4 if self.shadow else -1)
        paint_glass(p, r, self.radius, self.alpha, self.shadow)


class KeyboardFocus:
    """Remembers whether the focus came from the keyboard (Tab): the focus ring
    is only drawn then, not when a window opens or after a click."""
    _kbd_focus = False

    def focusInEvent(self, e):
        self._kbd_focus = e.reason() in (Qt.TabFocusReason, Qt.BacktabFocusReason,
                                         Qt.ShortcutFocusReason)
        super().focusInEvent(e)
        self.update()

    def focusOutEvent(self, e):
        self._kbd_focus = False
        super().focusOutEvent(e)
        self.update()

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
            self._kbd_focus = True                 # arrows in a group: still keyboard
        super().keyPressEvent(e)

    def show_focus(self) -> bool:
        return self.hasFocus() and self._kbd_focus


class Toggle(KeyboardFocus, QCheckBox):
    """An on/off switch (a QCheckBox underneath: setChecked, toggled...)."""

    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.TabFocus)          # a click leaves no focus ring
        self.setAccessibleName(text)
        self._pos = 1.0 if self.isChecked() else 0.0
        self._anim = QVariantAnimation(self, duration=160)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
        self._anim.valueChanged.connect(self._moved)
        self.toggled.connect(self._animate)

    def sizeHint(self) -> QSize:
        return QSize(46, 28)

    def minimumSizeHint(self) -> QSize:
        return self.sizeHint()

    def hitButton(self, pos) -> bool:
        return self.rect().contains(pos)

    def setChecked(self, on: bool) -> None:
        super().setChecked(on)
        self._anim.stop()
        self._pos = 1.0 if on else 0.0
        self.update()

    def _animate(self, on: bool) -> None:
        self._anim.stop()
        self._anim.setStartValue(self._pos)
        self._anim.setEndValue(1.0 if on else 0.0)
        self._anim.start()

    def _moved(self, v) -> None:
        self._pos = float(v)
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        w, h = 44.0, 26.0
        r = QRectF((self.width() - w) / 2, (self.height() - h) / 2, w, h)
        off, on = QColor("#D3DAE6"), QColor(ACCENT)
        t = self._pos
        track = QColor(round(off.red() + (on.red() - off.red()) * t),
                       round(off.green() + (on.green() - off.green()) * t),
                       round(off.blue() + (on.blue() - off.blue()) * t))
        if not self.isEnabled():
            track.setAlpha(110)
        p.setPen(Qt.NoPen)
        p.setBrush(track)
        p.drawRoundedRect(r, h / 2, h / 2)
        if t < 1.0:                               # off: an outline that reads (3:1)
            edge = QColor(OUTLINE)
            edge.setAlphaF(1.0 - t)
            p.setPen(QPen(edge, 1))
            p.setBrush(Qt.NoBrush)
            p.drawRoundedRect(r.adjusted(0.5, 0.5, -0.5, -0.5), h / 2, h / 2)
        if self.show_focus():
            focus_ring(p, r, h / 2)
        d = h - 4
        x = r.left() + 2 + (w - d - 4) * t
        knob = QRectF(x, r.top() + 2, d, d)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(20, 40, 80, 45))
        p.drawEllipse(knob.translated(0, 1.2))
        p.setBrush(QColor("#FFFFFF"))
        p.drawEllipse(knob)


class NavItem(KeyboardFocus, QAbstractButton):
    """A sidebar entry: glyph + label; highlighted when its page is shown."""

    def __init__(self, label: str, glyph: str, color: str, parent=None):
        super().__init__(parent)
        self.setText(label)
        self.glyph, self.color = glyph, QColor(color)
        self.setCheckable(True)
        self.setAutoExclusive(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.TabFocus)          # arrows then move between pages
        self.setMinimumHeight(38)
        self._hover = False

    def sizeHint(self) -> QSize:
        return QSize(190, 38)

    def enterEvent(self, _):
        self._hover = True
        self.update()

    def leaveEvent(self, _):
        self._hover = False
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        r = QRectF(self.rect()).adjusted(4, 2, -4, -2)
        if self.isChecked():
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(255, 255, 255, 235))
            p.drawRoundedRect(r, 10, 10)
            p.setPen(QPen(QColor(30, 50, 100, 22), 1))
            p.setBrush(Qt.NoBrush)
            p.drawRoundedRect(r, 10, 10)
            p.setPen(Qt.NoPen)                    # the page shown, readable from afar
            p.setBrush(QColor(ACCENT))
            p.drawRoundedRect(QRectF(r.left() + 1, r.center().y() - 8, 3, 16), 1.5, 1.5)
        elif self._hover:
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(255, 255, 255, 120))
            p.drawRoundedRect(r, 10, 10)
        # a small coloured tile with the glyph, like system settings
        tile = QRectF(r.left() + 8, r.center().y() - 12, 24, 24)
        g = QLinearGradient(tile.topLeft(), tile.bottomLeft())
        g.setColorAt(0.0, self.color.lighter(118))
        g.setColorAt(1.0, self.color)
        p.setPen(Qt.NoPen)
        p.setBrush(g)
        p.drawRoundedRect(tile, 7, 7)
        draw_icon(p, self.glyph, tile.center().x(), tile.center().y(), 15, QColor("white"))
        p.setPen(QColor(TEXT))
        p.setFont(font(10, bold=self.isChecked()))
        p.drawText(QRectF(tile.right() + 10, r.top(), r.width() - 44, r.height()),
                   Qt.AlignVCenter | Qt.AlignLeft, self.text())
        if self.show_focus():
            focus_ring(p, r, 10)


def focus_ring(p: QPainter, rect: QRectF, radius: float) -> None:
    """The keyboard focus mark, the same everywhere: 2 px of accent, 2 px out."""
    p.save()
    p.setPen(QPen(QColor(ACCENT), 2))
    p.setBrush(Qt.NoBrush)
    p.drawRoundedRect(rect.adjusted(-2, -2, 2, 2), radius + 2, radius + 2)
    p.restore()


def french(text: str) -> str:
    """Non-breaking spaces where French typography wants them, so a line never
    starts with « : » or a lone guillemet."""
    for a, b in (("« ", "«\u00a0"), (" »", "\u00a0»"), (" :", "\u00a0:"),
                 (" ?", "\u00a0?"), (" !", "\u00a0!"), (" ;", "\u00a0;")):
        text = text.replace(a, b)
    return text


def label(text: str, kind: str = "body") -> QLabel:
    lbl = QLabel(french(text))
    lbl.setWordWrap(True)
    styles = {
        "title": f"color:{TEXT};font-size:22px;font-weight:700;",
        "subtitle": f"color:{MUTED};font-size:13px;",
        "group": f"color:{TEXT_SOFT};font-size:13px;font-weight:600;",
        "note": f"color:{MUTED};font-size:12px;",
        "row": f"color:{TEXT};font-size:13px;font-weight:600;",
        "desc": f"color:{MUTED};font-size:12px;",
        "faint": f"color:{FAINT};font-size:11px;",
        "body": f"color:{TEXT};font-size:13px;",
    }
    lbl.setStyleSheet(styles.get(kind, styles["body"]) + "background:transparent;")
    if kind in ("desc", "faint", "subtitle", "note"):
        lbl.setTextInteractionFlags(Qt.NoTextInteraction)
    return lbl


class Row(QWidget):
    """One setting: its name and a short explanation on the left, its control
    on the right (or below, for wide ones)."""

    def __init__(self, title: str, desc: str = "", control: QWidget | None = None,
                 below: QWidget | None = None):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 12, 16, 12)
        lay.setSpacing(8)
        top = QHBoxLayout()
        top.setSpacing(14)
        texts = QVBoxLayout()
        texts.setSpacing(2)
        self.title = label(title, "row")
        texts.addWidget(self.title)
        self.desc = label(desc, "desc") if desc else None
        if self.desc is not None:
            texts.addWidget(self.desc)
        top.addLayout(texts, 1)
        if control is not None:
            top.addWidget(control, 0, Qt.AlignVCenter | Qt.AlignRight)
        lay.addLayout(top)
        if below is not None:
            lay.addWidget(below)


class Group(GlassPanel):
    """Rows on one glass card, separated by hairlines, under a small caption."""

    def __init__(self, caption: str = ""):
        super().__init__(radius=14, alpha=170)
        self._outer = QVBoxLayout(self)
        self._outer.setContentsMargins(2, 2, 2, 6)
        self._outer.setSpacing(0)
        self._rows: list[QWidget] = []
        self.caption = caption

    def add(self, row: QWidget) -> QWidget:
        if self._rows:
            line = QWidget()
            line.setFixedHeight(1)
            line.setStyleSheet("background:rgba(30,50,100,0.08);margin:0 16px;")
            self._outer.addWidget(line)
        self._rows.append(row)
        self._outer.addWidget(row)
        return row


def group_block(group: Group | None, notes: tuple[str, ...] | list[str] = (),
                caption: str = "") -> QWidget:
    """The caption above its card, and the notes under it: help is plain grey
    text, only settings sit on a card (as in the system settings)."""
    w = QWidget()
    w.setAttribute(Qt.WA_TranslucentBackground)
    lay = QVBoxLayout(w)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(6)
    caption = caption or (group.caption if group is not None else "")
    if caption:
        cap = label(caption, "group")
        cap.setContentsMargins(6, 0, 0, 0)
        lay.addWidget(cap)
    if group is not None:
        lay.addWidget(group)
    if notes:
        box = QVBoxLayout()
        box.setContentsMargins(8, 2, 8, 0)
        box.setSpacing(5)
        for text in notes:
            box.addWidget(label(text, "note"))
        lay.addLayout(box)
    return w


class Choice(KeyboardFocus, QAbstractButton):
    """A radio card: a title, a line of explanation, a round check mark."""
    picked = Signal()

    def __init__(self, title: str, desc: str, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setAutoExclusive(True)
        self.setText(title)
        self.desc = desc
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.TabFocus)
        self.setMinimumHeight(58)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.clicked.connect(lambda: self.picked.emit())

    def sizeHint(self) -> QSize:
        return QSize(260, 58)

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        r = QRectF(self.rect()).adjusted(1, 1, -1, -1)
        on = self.isChecked()
        p.setPen(QPen(QColor(ACCENT) if on else QColor(BORDER), 1.6 if on else 1))
        p.setBrush(QColor(ACCENT_SOFT) if on else QColor(255, 255, 255, 200))
        p.drawRoundedRect(r, 12, 12)
        dot = QPointF(r.left() + 20, r.center().y())
        p.setPen(QPen(QColor(ACCENT) if on else QColor(OUTLINE), 1.6))
        p.setBrush(QColor("white"))
        p.drawEllipse(dot, 8, 8)
        if on:
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(ACCENT))
            p.drawEllipse(dot, 4.5, 4.5)
        p.setPen(QColor(TEXT))
        p.setFont(font(10, bold=True))
        p.drawText(QRectF(r.left() + 38, r.top() + 9, r.width() - 46, 20),
                   Qt.AlignLeft | Qt.AlignVCenter, self.text())
        p.setPen(QColor(MUTED))
        p.setFont(font(9))
        p.drawText(QRectF(r.left() + 38, r.top() + 29, r.width() - 46, 20),
                   Qt.AlignLeft | Qt.AlignVCenter, self.desc)
        if self.show_focus():
            focus_ring(p, r, 12)


SLIDER_QSS = (
    "QSlider{background:transparent;min-height:26px;}"
    "QSlider::groove:horizontal{height:6px;border-radius:3px;background:#D9E0EB;}"
    f"QSlider::sub-page:horizontal{{height:6px;border-radius:3px;background:{ACCENT};}}"
    "QSlider::handle:horizontal{width:20px;height:20px;margin:-8px 0;border-radius:10px;"
    "background:white;border:1px solid #C5CEDC;}"
    "QSlider::handle:horizontal:hover{border:1px solid #9FB3D3;}"
    f"QSlider::handle:horizontal:focus{{border:2px solid {ACCENT};}}"
)
