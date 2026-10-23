"""The Cerclic logo, drawn in code: a ring cut into segments, like the wheel,
one of them lifted (the action you pick), and a dot in the centre.

paint_logo() draws it in any rectangle; it stays clear down to 16 px (fewer
gaps, thicker ring, no lift when tiny). Used for the app and tray icons, the
settings window and the installer icon (scripts/make_ico.py).
"""
from __future__ import annotations

import math

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import (QColor, QIcon, QLinearGradient, QPainter, QPainterPath,
                           QPixmap, QRadialGradient)

# Clockwise from the top: a cool, iridescent band, the lifted one in brand blue.
SEGMENTS = ["#2E7CF6", "#5AC8FA", "#34C7A6", "#7C6CF2", "#AF6BEA", "#5B8DEF"]
LIFTED = 0
BRAND = "#2E7CF6"


def _segment(c: QPointF, r_in: float, r_out: float, start: float, span: float) -> QPainterPath:
    """A ring segment from `start` degrees (clockwise from the top) over `span`."""
    path = QPainterPath()
    outer = QRectF(c.x() - r_out, c.y() - r_out, 2 * r_out, 2 * r_out)
    inner = QRectF(c.x() - r_in, c.y() - r_in, 2 * r_in, 2 * r_in)
    qt_start = 90.0 - start                     # Qt: counter-clockwise from 3 o'clock
    path.arcMoveTo(outer, qt_start)
    path.arcTo(outer, qt_start, -span)
    path.arcTo(inner, qt_start - span, span)
    path.closeSubpath()
    return path


def paint_logo(p: QPainter, rect: QRectF, mono: QColor | None = None) -> None:
    """Draw the logo in `rect`. `mono`: one flat colour (macOS menu bar)."""
    size = min(rect.width(), rect.height())
    c = rect.center()
    tiny = size < 28
    n = len(SEGMENTS)
    r_out = size * (0.48 if tiny else 0.45)
    r_in = size * (0.25 if tiny else 0.27)
    lift = 0.0 if tiny else size * 0.05
    if lift:
        r_out -= lift
    gap_px = 1.0 if tiny else max(1.2, size * 0.04)
    r_mid = (r_in + r_out) / 2
    gap = math.degrees(gap_px / r_mid)
    step = 360.0 / n
    p.save()
    p.setRenderHint(QPainter.Antialiasing, True)
    p.setPen(Qt.NoPen)
    for i in range(n):
        start = i * step - step / 2 + gap / 2   # segment 0 centred on the top
        span = step - gap
        mid = math.radians(i * step)
        off = QPointF(math.sin(mid) * lift, -math.cos(mid) * lift) if i == LIFTED else QPointF()
        path = _segment(c + off, r_in, r_out, start, span)
        if mono is not None:
            p.setBrush(mono)
        else:
            col = QColor(SEGMENTS[i % len(SEGMENTS)])
            g = QLinearGradient(rect.topLeft(), rect.bottomRight())
            g.setColorAt(0.0, col.lighter(118))
            g.setColorAt(1.0, col.darker(108))
            p.setBrush(g)
        p.drawPath(path)
    # the centre: a small dot, the point the wheel opens around
    dot = size * (0.11 if tiny else 0.095)
    if mono is not None:
        p.setBrush(mono)
    else:
        g = QRadialGradient(c - QPointF(dot * 0.35, dot * 0.35), dot * 1.6)
        g.setColorAt(0.0, QColor("#6FA8FF"))
        g.setColorAt(1.0, QColor(BRAND))
        p.setBrush(g)
    p.drawEllipse(c, dot, dot)
    p.restore()


def logo_pixmap(size: int, mono: QColor | None = None, plate: bool = False) -> QPixmap:
    """The logo on a transparent square; `plate`: on a frosted white tile
    (macOS app icon style)."""
    pix = QPixmap(size, size)
    pix.fill(Qt.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.Antialiasing, True)
    rect = QRectF(0, 0, size, size)
    if plate:
        m = size * 0.09
        tile = rect.adjusted(m, m, -m, -m)
        radius = tile.width() * 0.225
        shadow = QColor(20, 40, 90, 40)
        p.setPen(Qt.NoPen)
        p.setBrush(shadow)
        p.drawRoundedRect(tile.translated(0, size * 0.012), radius, radius)
        g = QLinearGradient(tile.topLeft(), tile.bottomLeft())
        g.setColorAt(0.0, QColor("#FFFFFF"))
        g.setColorAt(1.0, QColor("#E9F0FB"))
        p.setBrush(g)
        p.drawRoundedRect(tile, radius, radius)
        rect = tile.adjusted(tile.width() * 0.14, tile.width() * 0.14,
                             -tile.width() * 0.14, -tile.width() * 0.14)
    paint_logo(p, rect, mono)
    p.end()
    return pix


def make_icon(size: int = 64) -> QIcon:
    icon = QIcon()
    for s in sorted({16, 20, 24, 32, 48, 64, 128, 256, size}):
        icon.addPixmap(logo_pixmap(s))
    return icon


def make_tray_icon() -> QIcon:
    """Windows: the colour logo. macOS: a template image the menu bar tints."""
    import sys
    if sys.platform == "darwin":
        icon = QIcon()
        for s in (16, 18, 32, 36):
            icon.addPixmap(logo_pixmap(s, mono=QColor(0, 0, 0)))
        icon.setIsMask(True)
        return icon
    return make_icon(32)
