"""Tiny vector glyphs drawn with QPainter, so the app ships no icon assets.

draw_icon(painter, name, center, size, color) renders one glyph centred on
`center`. Unknown names fall back to a dot. Text glyphs (JPG, PNG...) are drawn
as short labels, which reads cleanly at small sizes.
"""
from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QPainter, QPen, QPolygonF, QColor, QFont

_TEXT_GLYPHS = {
    "jpg": "JPG", "png": "PNG", "webp": "WEBP", "mp4": "MP4", "gif": "GIF",
    "mp3": "MP3", "word": "DOC", "topdf": "PDF",
}


def draw_icon(p: QPainter, name: str, cx: float, cy: float, size: float,
              color: QColor) -> None:
    p.save()
    pen = QPen(color)
    pen.setWidthF(max(1.6, size * 0.09))
    pen.setCapStyle(Qt.RoundCap)
    pen.setJoinStyle(Qt.RoundJoin)
    p.setPen(pen)
    p.setBrush(Qt.NoBrush)
    r = size / 2.0

    if name in _TEXT_GLYPHS:
        f = QFont("Segoe UI", int(size * 0.42))
        f.setBold(True)
        p.setFont(f)
        p.drawText(QRectF(cx - size, cy - r, size * 2, size),
                   Qt.AlignCenter, _TEXT_GLYPHS[name])
        p.restore()
        return

    if name == "crop":
        p.drawLine(QPointF(cx - r, cy - r * 0.4), QPointF(cx - r, cy + r))
        p.drawLine(QPointF(cx - r, cy + r), QPointF(cx + r * 0.4, cy + r))
        p.drawLine(QPointF(cx + r, cy + r * 0.4), QPointF(cx + r, cy - r))
        p.drawLine(QPointF(cx + r, cy - r), QPointF(cx - r * 0.4, cy - r))
    elif name == "compress":
        p.drawLine(QPointF(cx, cy - r), QPointF(cx, cy - r * 0.2))
        p.drawLine(QPointF(cx, cy + r), QPointF(cx, cy + r * 0.2))
        _arrow(p, cx, cy - r * 0.2, up=True, w=r * 0.5)
        _arrow(p, cx, cy + r * 0.2, up=False, w=r * 0.5)
        p.drawLine(QPointF(cx - r, cy), QPointF(cx + r, cy))
    elif name == "resize":
        p.drawRect(QRectF(cx - r, cy - r * 0.7, size, size * 0.7))
        p.drawLine(QPointF(cx + r * 0.2, cy + r * 0.1),
                   QPointF(cx + r, cy + r))
        _arrow_head(p, cx + r, cy + r, 225)
    elif name == "rotate":
        p.drawArc(QRectF(cx - r, cy - r, size, size), 60 * 16, 250 * 16)
        _arrow_head(p, cx + r * 0.5, cy - r * 0.75, 20)
    elif name in ("merge", "topdf"):
        p.drawLine(QPointF(cx - r * 0.6, cy - r), QPointF(cx - r * 0.6, cy + r))
        p.drawLine(QPointF(cx + r * 0.6, cy - r), QPointF(cx + r * 0.6, cy + r))
        _arrow_head(p, cx, cy, 0)
    elif name == "split":
        p.drawLine(QPointF(cx, cy - r), QPointF(cx, cy + r))
        p.setPen(QPen(color, pen.widthF(), Qt.DashLine))
        p.drawLine(QPointF(cx - r, cy), QPointF(cx + r, cy))
    elif name == "sign":
        p.drawArc(QRectF(cx - r, cy - r * 0.2, r, r), 0, 360 * 16)
        p.drawLine(QPointF(cx - r * 0.5, cy + r * 0.3),
                   QPointF(cx + r, cy - r))
        p.drawLine(QPointF(cx - r, cy + r), QPointF(cx + r, cy + r))
    elif name == "watermark":
        p.drawEllipse(QPointF(cx, cy), r * 0.7, r * 0.7)
        f = QFont("Segoe UI", int(size * 0.3))
        p.setFont(f)
        p.drawText(QRectF(cx - r, cy - r, size, size), Qt.AlignCenter, "%")
    elif name == "numbers":
        f = QFont("Segoe UI", int(size * 0.5))
        f.setBold(True)
        p.setFont(f)
        p.drawText(QRectF(cx - r, cy - r, size, size), Qt.AlignCenter, "1 2")
    elif name == "lock" or name == "unlock":
        body = QRectF(cx - r * 0.7, cy - r * 0.1, r * 1.4, r * 1.1)
        p.drawRect(body)
        if name == "lock":
            p.drawArc(QRectF(cx - r * 0.5, cy - r * 0.9, r, r), 0, 180 * 16)
        else:
            p.drawArc(QRectF(cx - r * 0.1, cy - r * 0.9, r, r), 0, 180 * 16)
    else:
        p.setBrush(color)
        p.drawEllipse(QPointF(cx, cy), size * 0.16, size * 0.16)
    p.restore()


def _arrow(p: QPainter, x: float, y: float, up: bool, w: float) -> None:
    d = -1 if up else 1
    p.drawLine(QPointF(x - w, y + d * w), QPointF(x, y))
    p.drawLine(QPointF(x + w, y + d * w), QPointF(x, y))


def _arrow_head(p: QPainter, x: float, y: float, angle_deg: float) -> None:
    import math
    a = math.radians(angle_deg)
    size = 6
    for off in (150, 210):
        b = a + math.radians(off)
        p.drawLine(QPointF(x, y),
                   QPointF(x + size * math.cos(b), y - size * math.sin(b)))
