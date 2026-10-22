"""Small vector glyphs drawn with QPainter, so the app ships no icon files.

draw_icon(painter, name, cx, cy, size, color) renders one glyph centred on
(cx, cy). Unknown names fall back to a dot. Format names (JPG, PNG...) are
drawn as short bold labels, which read cleanly at small sizes.
"""
from __future__ import annotations

import math

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath, QPen

from .theme import FONT_FAMILY

_TEXT_GLYPHS = {
    "jpg": "JPG", "png": "PNG", "webp": "WEBP", "mp4": "MP4", "gif": "GIF",
    "mp3": "MP3", "word": "DOC", "topdf": "PDF", "half": "½", "px": "px",
}


def _label(p: QPainter, text: str, cx: float, cy: float, size: float) -> None:
    f = QFont(FONT_FAMILY)
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
    else:
        p.setPen(Qt.NoPen)
        p.setBrush(color)
        p.drawEllipse(QPointF(cx, cy), size * 0.16, size * 0.16)
    p.restore()
