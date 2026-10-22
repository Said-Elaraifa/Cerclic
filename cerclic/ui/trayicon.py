"""Draw the Cerclic tray/app icon in code (a ring of petals), no asset files."""
from __future__ import annotations

import math

from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPixmap, QPainter, QColor, QIcon, QPen


_PETAL_COLORS = ["#4C8DFF", "#FF5A5F", "#17B890", "#A66BFF",
                 "#4C8DFF", "#FF5A5F", "#17B890", "#A66BFF"]


def make_icon(size: int = 64) -> QIcon:
    pix = QPixmap(size, size)
    pix.fill(Qt.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.Antialiasing, True)
    c = QPointF(size / 2, size / 2)
    r = size * 0.33
    petal = size * 0.12
    for i, hexcol in enumerate(_PETAL_COLORS):
        ang = math.radians(90 - i * 45)
        x = c.x() + r * math.cos(ang)
        y = c.y() - r * math.sin(ang)
        p.setBrush(QColor(hexcol))
        p.setPen(Qt.NoPen)
        p.drawEllipse(QPointF(x, y), petal, petal)
    p.setBrush(QColor(26, 28, 36))
    p.setPen(QPen(QColor(236, 238, 243), max(1.0, size * 0.03)))
    p.drawEllipse(c, size * 0.14, size * 0.14)
    p.end()
    return QIcon(pix)
