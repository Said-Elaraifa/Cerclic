"""Small vector glyphs drawn with QPainter, so the app ships no icon files.

draw_icon(painter, name, cx, cy, size, color) renders one glyph centred on
(cx, cy). Unknown names fall back to a dot. Format names (JPG, PNG...) are
drawn as short bold labels, which read cleanly at small sizes.
"""
from __future__ import annotations

import math

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen

from .theme import base_font

_TEXT_GLYPHS = {
    "jpg": "JPG", "png": "PNG", "webp": "WEBP", "mp4": "MP4", "gif": "GIF",
    "mp3": "MP3", "word": "DOC", "topdf": "PDF", "half": "½", "px": "px",
}


def _label(p: QPainter, text: str, cx: float, cy: float, size: float) -> None:
    f = base_font()
    f.setPixelSize(max(6, int(size * (0.62 if len(text) <= 2 else 0.42))))
    f.setBold(True)
    p.setFont(f)
    p.drawText(QRectF(cx - size, cy - size / 2, size * 2, size), Qt.AlignCenter, text)


def _arrow_head(p: QPainter, tip: QPointF, angle_deg: float, length: float) -> None:
    a = math.radians(angle_deg)
    for off in (150, -150):
        b = a + math.radians(off)
        p.drawLine(tip, QPointF(tip.x() + length * math.cos(b),
                                tip.y() - length * math.sin(b)))


def _arc_arrow(p: QPainter, cx, cy, r, start_deg, span_deg) -> None:
    """Arc from start_deg spanning span_deg (Qt degrees, counter-clockwise
    positive) with an arrow head at its end."""
    rect = QRectF(cx - r, cy - r, 2 * r, 2 * r)
    p.drawArc(rect, int(start_deg * 16), int(span_deg * 16))
    end = math.radians(start_deg + span_deg)
    tip = QPointF(cx + r * math.cos(end), cy - r * math.sin(end))
    # tangent direction at the end of the arc
    tangent = start_deg + span_deg + (90 if span_deg > 0 else -90)
    _arrow_head(p, tip, tangent, r * 0.55)


def draw_icon(p: QPainter, name: str, cx: float, cy: float, size: float,
              color: QColor) -> None:
    p.save()
    pen = QPen(color)
    pen.setWidthF(max(1.5, size * 0.085))
    pen.setCapStyle(Qt.RoundCap)
    pen.setJoinStyle(Qt.RoundJoin)
    p.setPen(pen)
    p.setBrush(Qt.NoBrush)
    r = size / 2.0

    if name in _TEXT_GLYPHS:
        _label(p, _TEXT_GLYPHS[name], cx, cy, size)
    elif name == "crop":
        p.drawLine(QPointF(cx - r * 0.55, cy - r), QPointF(cx - r * 0.55, cy + r * 0.55))
        p.drawLine(QPointF(cx - r * 0.55, cy + r * 0.55), QPointF(cx + r, cy + r * 0.55))
        p.drawLine(QPointF(cx - r, cy - r * 0.55), QPointF(cx + r * 0.55, cy - r * 0.55))
        p.drawLine(QPointF(cx + r * 0.55, cy - r * 0.55), QPointF(cx + r * 0.55, cy + r))
    elif name == "compress":
        for d in (-1, 1):
            p.drawLine(QPointF(cx, cy + d * r), QPointF(cx, cy + d * r * 0.25))
            _arrow_head(p, QPointF(cx, cy + d * r * 0.25), -90 if d < 0 else 90, r * 0.45)
        p.drawLine(QPointF(cx - r, cy), QPointF(cx + r, cy))
    elif name == "resize":
        p.drawRoundedRect(QRectF(cx - r, cy - r * 0.75, size, size * 0.75), 2, 2)
        p.drawLine(QPointF(cx - r * 0.25, cy + r * 0.2), QPointF(cx + r * 0.75, cy - r * 0.55))
        _arrow_head(p, QPointF(cx + r * 0.75, cy - r * 0.55), 37, r * 0.45)
    elif name in ("rotate", "rotate_cw"):
        _arc_arrow(p, cx, cy, r * 0.8, 160, -250)
    elif name == "rotate_ccw":
        _arc_arrow(p, cx, cy, r * 0.8, 20, 250)
    elif name == "rotate_180":
        _arc_arrow(p, cx, cy, r * 0.8, 180, -180)
        p.setPen(Qt.NoPen)
        p.setBrush(color)
        p.drawEllipse(QPointF(cx, cy), size * 0.07, size * 0.07)
    elif name == "convert":
        p.drawLine(QPointF(cx - r, cy - r * 0.35), QPointF(cx + r, cy - r * 0.35))
        _arrow_head(p, QPointF(cx + r, cy - r * 0.35), 0, r * 0.5)
        p.drawLine(QPointF(cx + r, cy + r * 0.35), QPointF(cx - r, cy + r * 0.35))
        _arrow_head(p, QPointF(cx - r, cy + r * 0.35), 180, r * 0.5)
    elif name in ("merge",):
        p.drawLine(QPointF(cx - r, cy - r * 0.7), QPointF(cx - r * 0.1, cy))
        p.drawLine(QPointF(cx - r, cy + r * 0.7), QPointF(cx - r * 0.1, cy))
        p.drawLine(QPointF(cx - r * 0.1, cy), QPointF(cx + r, cy))
        _arrow_head(p, QPointF(cx + r, cy), 0, r * 0.5)
    elif name == "split":
        p.drawLine(QPointF(cx - r, cy), QPointF(cx + r * 0.1, cy))
        p.drawLine(QPointF(cx + r * 0.1, cy), QPointF(cx + r, cy - r * 0.7))
        p.drawLine(QPointF(cx + r * 0.1, cy), QPointF(cx + r, cy + r * 0.7))
        _arrow_head(p, QPointF(cx + r, cy - r * 0.7), 38, r * 0.45)
        _arrow_head(p, QPointF(cx + r, cy + r * 0.7), -38, r * 0.45)
    elif name == "sign":
        path = QPainterPath(QPointF(cx - r, cy + r * 0.2))
        path.cubicTo(QPointF(cx - r * 0.6, cy - r * 0.9), QPointF(cx - r * 0.2, cy - r * 0.6),
                     QPointF(cx - r * 0.3, cy + r * 0.2))
        path.cubicTo(QPointF(cx - r * 0.35, cy + r * 0.6), QPointF(cx + r * 0.3, cy - r * 0.5),
                     QPointF(cx + r, cy - r * 0.1))
        p.drawPath(path)
        p.drawLine(QPointF(cx - r, cy + r * 0.8), QPointF(cx + r, cy + r * 0.8))
    elif name == "watermark":
        path = QPainterPath(QPointF(cx, cy - r))
        path.cubicTo(QPointF(cx + r * 0.9, cy), QPointF(cx + r * 0.7, cy + r),
                     QPointF(cx, cy + r))
        path.cubicTo(QPointF(cx - r * 0.7, cy + r), QPointF(cx - r * 0.9, cy),
                     QPointF(cx, cy - r))
        p.drawPath(path)
    elif name == "numbers":
        _label(p, "1 2", cx, cy, size)
    elif name in ("lock", "unlock"):
        p.drawRoundedRect(QRectF(cx - r * 0.75, cy - r * 0.1, r * 1.5, r * 1.1), 2, 2)
        shift = 0.0 if name == "lock" else r * 0.55
        p.drawArc(QRectF(cx - r * 0.45 + shift, cy - r * 0.95, r * 0.9, r * 1.1),
                  0, 180 * 16)
        if name == "lock":
            p.drawLine(QPointF(cx - r * 0.45, cy - r * 0.4), QPointF(cx - r * 0.45, cy - r * 0.1))
        p.drawLine(QPointF(cx + r * 0.45 + shift, cy - r * 0.4),
                   QPointF(cx + r * 0.45 + shift, cy - r * 0.1))
    elif name in ("image", "cat_image"):
        p.drawRoundedRect(QRectF(cx - r, cy - r * 0.75, size, size * 0.75), 2, 2)
        path = QPainterPath(QPointF(cx - r * 0.75, cy + r * 0.45))
        path.lineTo(QPointF(cx - r * 0.2, cy - r * 0.1))
        path.lineTo(QPointF(cx + r * 0.15, cy + r * 0.25))
        path.lineTo(QPointF(cx + r * 0.45, cy))
        path.lineTo(QPointF(cx + r * 0.8, cy + r * 0.45))
        p.drawPath(path)
        p.drawEllipse(QPointF(cx + r * 0.45, cy - r * 0.38), r * 0.12, r * 0.12)
    elif name == "cat_pdf":
        path = QPainterPath(QPointF(cx - r * 0.7, cy - r))
        path.lineTo(QPointF(cx + r * 0.3, cy - r))
        path.lineTo(QPointF(cx + r * 0.7, cy - r * 0.6))
        path.lineTo(QPointF(cx + r * 0.7, cy + r))
        path.lineTo(QPointF(cx - r * 0.7, cy + r))
        path.closeSubpath()
        p.drawPath(path)
        for k in (-0.2, 0.15, 0.5):
            p.drawLine(QPointF(cx - r * 0.4, cy + r * k), QPointF(cx + r * 0.4, cy + r * k))
    elif name == "cat_video":
        p.drawRoundedRect(QRectF(cx - r, cy - r * 0.7, size, size * 0.7), 3, 3)
        path = QPainterPath(QPointF(cx - r * 0.25, cy - r * 0.35))
        path.lineTo(QPointF(cx + r * 0.4, cy))
        path.lineTo(QPointF(cx - r * 0.25, cy + r * 0.35))
        path.closeSubpath()
        p.setBrush(color)
        p.drawPath(path)
    elif name == "copy":
        p.drawRoundedRect(QRectF(cx - r * 0.85, cy - r * 0.55, r * 1.2, r * 1.4), 2.5, 2.5)
        p.drawRoundedRect(QRectF(cx - r * 0.35, cy - r * 0.95, r * 1.2, r * 1.4), 2.5, 2.5)
    elif name == "assemble":
        g = r * 0.12
        for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            p.drawRoundedRect(QRectF(cx + (g if dx > 0 else -r * 0.85),
                                     cy + (g if dy > 0 else -r * 0.85),
                                     r * 0.85 - g, r * 0.85 - g), 2, 2)
    elif name == "shield":
        path = QPainterPath(QPointF(cx, cy - r))
        path.lineTo(QPointF(cx + r * 0.8, cy - r * 0.62))
        path.cubicTo(QPointF(cx + r * 0.8, cy + r * 0.2), QPointF(cx + r * 0.4, cy + r * 0.7),
                     QPointF(cx, cy + r))
        path.cubicTo(QPointF(cx - r * 0.4, cy + r * 0.7), QPointF(cx - r * 0.8, cy + r * 0.2),
                     QPointF(cx - r * 0.8, cy - r * 0.62))
        path.closeSubpath()
        p.drawPath(path)
        p.drawLine(QPointF(cx - r * 0.32, cy), QPointF(cx - r * 0.05, cy + r * 0.28))
        p.drawLine(QPointF(cx - r * 0.05, cy + r * 0.28), QPointF(cx + r * 0.38, cy - r * 0.22))
    elif name == "pages":
        p.drawRoundedRect(QRectF(cx - r * 0.35, cy - r, r * 1.15, r * 1.45), 2, 2)
        p.setBrush(QColor(30, 33, 42))
        p.drawRoundedRect(QRectF(cx - r * 0.8, cy - r * 0.45, r * 1.15, r * 1.45), 2, 2)
    elif name == "text":
        p.drawLine(QPointF(cx - r * 0.75, cy - r * 0.75), QPointF(cx + r * 0.75, cy - r * 0.75))
        p.drawLine(QPointF(cx, cy - r * 0.75), QPointF(cx, cy + r * 0.85))
        p.drawLine(QPointF(cx - r * 0.35, cy + r * 0.85), QPointF(cx + r * 0.35, cy + r * 0.85))
    elif name == "trim":
        for sy in (-1, 1):
            p.drawEllipse(QPointF(cx - r * 0.55, cy + sy * r * 0.5), r * 0.3, r * 0.3)
            p.drawLine(QPointF(cx - r * 0.3, cy + sy * r * 0.36), QPointF(cx + r, cy - sy * r * 0.55))
    elif name == "mute":
        path = QPainterPath(QPointF(cx - r * 0.9, cy - r * 0.3))
        path.lineTo(QPointF(cx - r * 0.45, cy - r * 0.3))
        path.lineTo(QPointF(cx + r * 0.05, cy - r * 0.8))
        path.lineTo(QPointF(cx + r * 0.05, cy + r * 0.8))
        path.lineTo(QPointF(cx - r * 0.45, cy + r * 0.3))
        path.lineTo(QPointF(cx - r * 0.9, cy + r * 0.3))
        path.closeSubpath()
        p.drawPath(path)
        p.drawLine(QPointF(cx + r * 0.4, cy - r * 0.3), QPointF(cx + r, cy + r * 0.3))
        p.drawLine(QPointF(cx + r, cy - r * 0.3), QPointF(cx + r * 0.4, cy + r * 0.3))
    elif name == "mirror":
        dash = QPen(pen)
        dash.setStyle(Qt.DashLine)
        dash.setWidthF(max(1.0, pen.widthF() * 0.6))
        p.setPen(dash)
        p.drawLine(QPointF(cx, cy - r), QPointF(cx, cy + r))
        p.setPen(pen)
        left = QPainterPath(QPointF(cx - r * 0.2, cy - r * 0.65))
        left.lineTo(QPointF(cx - r * 0.2, cy + r * 0.65))
        left.lineTo(QPointF(cx - r, cy + r * 0.65))
        left.closeSubpath()
        p.setBrush(color)
        p.drawPath(left)
        p.setBrush(Qt.NoBrush)
        right = QPainterPath(QPointF(cx + r * 0.2, cy - r * 0.65))
        right.lineTo(QPointF(cx + r * 0.2, cy + r * 0.65))
        right.lineTo(QPointF(cx + r, cy + r * 0.65))
        right.closeSubpath()
        p.drawPath(right)
    elif name == "row":
        for k in (-1, 0, 1):
            p.drawRoundedRect(QRectF(cx + k * r * 0.7 - r * 0.3, cy - r * 0.55, r * 0.6, r * 1.1), 1.5, 1.5)
    elif name == "column":
        for k in (-1, 0, 1):
            p.drawRoundedRect(QRectF(cx - r * 0.55, cy + k * r * 0.7 - r * 0.3, r * 1.1, r * 0.6), 1.5, 1.5)
    elif name == "grid":
        for dx in (-1, 1):
            for dy in (-1, 1):
                p.drawRoundedRect(QRectF(cx + dx * r * 0.45 - r * 0.38, cy + dy * r * 0.45 - r * 0.38,
                                         r * 0.76, r * 0.76), 1.5, 1.5)
    elif name == "cat_audio":
        p.drawLine(QPointF(cx - r * 0.25, cy + r * 0.55), QPointF(cx - r * 0.25, cy - r * 0.8))
        p.drawLine(QPointF(cx - r * 0.25, cy - r * 0.8), QPointF(cx + r * 0.75, cy - r * 0.95))
        p.drawLine(QPointF(cx + r * 0.75, cy - r * 0.95), QPointF(cx + r * 0.75, cy + r * 0.4))
        p.setBrush(color)
        p.drawEllipse(QPointF(cx - r * 0.5, cy + r * 0.6), r * 0.3, r * 0.22)
        p.drawEllipse(QPointF(cx + r * 0.5, cy + r * 0.45), r * 0.3, r * 0.22)
    elif name == "more":
        p.setPen(Qt.NoPen)
        p.setBrush(color)
        for k in (-1, 0, 1):
            p.drawEllipse(QPointF(cx + k * r * 0.7, cy), size * 0.09, size * 0.09)
    elif name == "check":
        p.drawLine(QPointF(cx - r * 0.7, cy), QPointF(cx - r * 0.15, cy + r * 0.55))
        p.drawLine(QPointF(cx - r * 0.15, cy + r * 0.55), QPointF(cx + r * 0.75, cy - r * 0.5))
    elif name == "close":
        p.drawLine(QPointF(cx - r * 0.6, cy - r * 0.6), QPointF(cx + r * 0.6, cy + r * 0.6))
        p.drawLine(QPointF(cx + r * 0.6, cy - r * 0.6), QPointF(cx - r * 0.6, cy + r * 0.6))
    # ----- settings window -----
    elif name == "gear":
        for k in range(8):
            a = math.radians(k * 45)
            p.drawLine(QPointF(cx + r * 0.62 * math.cos(a), cy + r * 0.62 * math.sin(a)),
                       QPointF(cx + r * 0.95 * math.cos(a), cy + r * 0.95 * math.sin(a)))
        p.drawEllipse(QPointF(cx, cy), r * 0.62, r * 0.62)
        p.drawEllipse(QPointF(cx, cy), r * 0.22, r * 0.22)
    elif name == "keyboard":
        p.drawRoundedRect(QRectF(cx - r, cy - r * 0.62, size, r * 1.24), 2, 2)
        p.setPen(Qt.NoPen)
        p.setBrush(color)
        for row, n in ((-0.25, 4), (0.12, 3)):
            for k in range(n):
                x = cx - r * 0.62 + k * (r * 1.24 / max(1, n - 1)) if n > 1 else cx
                p.drawEllipse(QPointF(x, cy + row * r), size * 0.045, size * 0.045)
        p.drawRoundedRect(QRectF(cx - r * 0.45, cy + r * 0.32, r * 0.9, size * 0.07), 1, 1)
    elif name == "menu":
        p.drawRoundedRect(QRectF(cx - r * 0.85, cy - r * 0.9, r * 1.7, r * 1.8), 2.5, 2.5)
        for k in (-0.4, 0.0, 0.4):
            p.drawLine(QPointF(cx - r * 0.45, cy + k * r), QPointF(cx + r * 0.45, cy + k * r))
    elif name == "folder":
        path = QPainterPath()
        path.moveTo(cx - r, cy - r * 0.55)
        path.lineTo(cx - r * 0.25, cy - r * 0.55)
        path.lineTo(cx - r * 0.05, cy - r * 0.3)
        path.lineTo(cx + r, cy - r * 0.3)
        path.lineTo(cx + r, cy + r * 0.7)
        path.lineTo(cx - r, cy + r * 0.7)
        path.closeSubpath()
        p.drawPath(path)
    elif name == "sliders":
        for k, pos in ((-0.5, 0.35), (0.0, -0.4), (0.5, 0.1)):
            y = cy + k * r * 1.2
            p.drawLine(QPointF(cx - r, y), QPointF(cx + r, y))
            p.setBrush(color)
            p.drawEllipse(QPointF(cx + pos * r, y), size * 0.1, size * 0.1)
            p.setBrush(Qt.NoBrush)
    elif name == "info":
        p.drawEllipse(QPointF(cx, cy), r * 0.95, r * 0.95)
        p.drawLine(QPointF(cx, cy - r * 0.05), QPointF(cx, cy + r * 0.5))
        p.setPen(Qt.NoPen)
        p.setBrush(color)
        p.drawEllipse(QPointF(cx, cy - r * 0.42), size * 0.06, size * 0.06)
    elif name == "pen":
        p.drawLine(QPointF(cx - r * 0.75, cy + r * 0.75), QPointF(cx + r * 0.55, cy - r * 0.55))
        p.drawLine(QPointF(cx + r * 0.35, cy - r * 0.75), QPointF(cx + r * 0.75, cy - r * 0.35))
        p.drawLine(QPointF(cx - r * 0.75, cy + r * 0.75), QPointF(cx - r * 0.95, cy + r * 0.95))
    elif name == "mouse":
        p.drawRoundedRect(QRectF(cx - r * 0.6, cy - r * 0.95, r * 1.2, r * 1.9), r * 0.6, r * 0.6)
        p.drawLine(QPointF(cx, cy - r * 0.95), QPointF(cx, cy - r * 0.3))
    elif name == "chevron":                       # "go there", pointing right
        p.drawLine(QPointF(cx - r * 0.25, cy - r * 0.55), QPointF(cx + r * 0.3, cy))
        p.drawLine(QPointF(cx + r * 0.3, cy), QPointF(cx - r * 0.25, cy + r * 0.55))
    elif name == "drop":                          # an arrow coming down into a tray
        p.drawLine(QPointF(cx, cy - r * 0.95), QPointF(cx, cy + r * 0.25))
        _arrow_head(p, QPointF(cx, cy + r * 0.25), -90, r * 0.45)
        path = QPainterPath(QPointF(cx - r * 0.9, cy + r * 0.15))
        path.lineTo(QPointF(cx - r * 0.9, cy + r * 0.85))
        path.lineTo(QPointF(cx + r * 0.9, cy + r * 0.85))
        path.lineTo(QPointF(cx + r * 0.9, cy + r * 0.15))
        p.drawPath(path)
    elif name in ("eye", "eye_off"):
        path = QPainterPath(QPointF(cx - r * 0.95, cy))
        path.quadTo(QPointF(cx, cy - r * 0.95), QPointF(cx + r * 0.95, cy))
        path.quadTo(QPointF(cx, cy + r * 0.95), QPointF(cx - r * 0.95, cy))
        p.drawPath(path)
        p.drawEllipse(QPointF(cx, cy), r * 0.28, r * 0.28)
        if name == "eye_off":
            p.drawLine(QPointF(cx - r * 0.8, cy + r * 0.8), QPointF(cx + r * 0.8, cy - r * 0.8))
    else:
        p.setPen(Qt.NoPen)
        p.setBrush(color)
        p.drawEllipse(QPointF(cx, cy), size * 0.16, size * 0.16)
    p.restore()
