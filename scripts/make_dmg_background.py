"""Fond de la fenêtre de l'image disque Mac (assets/dmg/fond.png et fond@2x.png).

    python scripts/make_dmg_background.py

La fenêtre fait 640 x 440 points ; Cerclic.app est à (160, 180), Applications à
(480, 180) (scripts/mac_dmg.py). Le Finder écrit le nom des icônes dessous :
rien n'est dessiné à cet endroit. Les consignes restent au-dessus de y = 400,
au cas où la barre de titre mange le bas de la fenêtre.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtCore import QPointF, QRectF, Qt  # noqa: E402
from PySide6.QtGui import (QColor, QFont, QFontMetricsF, QGuiApplication, QImage,  # noqa: E402
                           QLinearGradient, QPainter, QPainterPath, QPen)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "dmg")
W, H = 640, 440
ICON_Y = 180
LEFT_X, RIGHT_X = 160, 480
INK, SOFT, BLUE, BORDER = "#1B2232", "#3A4457", "#2E7CF6", "#DCE2EC"

TITLE = "Glisse Cerclic dans Applications"
CARD_TITLE = "Première ouverture"
STEPS = [  # (number, line); a line without a number continues the step above
    ("1.", "Ouvre le dossier Applications et double-clique sur Cerclic."),
    ("2.", "Si le Mac le bloque : Réglages Système, Confidentialité et sécurité,"),
    ("", "tout en bas, « Ouvrir quand même »."),
    ("3.", "Clique sur une photo, puis appuie sur Maj + Cmd + Espace."),
]


def font(px: float, weight: QFont.Weight = QFont.Normal) -> QFont:
    f = QFont("Inter")
    f.setPixelSize(int(round(px)))
    f.setWeight(weight)
    return f


def draw(scale: int) -> QImage:
    img = QImage(W * scale, H * scale, QImage.Format_ARGB32_Premultiplied)
    img.setDevicePixelRatio(scale)
    p = QPainter(img)
    p.setRenderHint(QPainter.Antialiasing, True)
    p.setRenderHint(QPainter.TextAntialiasing, True)
    bg = QLinearGradient(0, 0, 0, H)
    bg.setColorAt(0.0, QColor("#FFFFFF"))
    bg.setColorAt(1.0, QColor("#EDF2FA"))
    p.fillRect(QRectF(0, 0, W, H), bg)

    # title
    p.setPen(QColor(INK))
    p.setFont(font(22, QFont.DemiBold))
    p.drawText(QRectF(0, 30, W, 40), Qt.AlignHCenter | Qt.AlignVCenter, TITLE)

    # arrow from Cerclic to Applications
    x0, x1, y = LEFT_X + 88, RIGHT_X - 92, ICON_Y
    pen = QPen(QColor(BLUE), 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
    p.setPen(pen)
    p.drawLine(QPointF(x0, y), QPointF(x1 - 10, y))
    head = QPainterPath(QPointF(x1 + 6, y))
    head.lineTo(QPointF(x1 - 14, y - 13))
    head.lineTo(QPointF(x1 - 14, y + 13))
    head.closeSubpath()
    p.setPen(QPen(QColor(BLUE), 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
    p.setBrush(QColor(BLUE))
    p.drawPath(head)

    # first opening, in a card
    card = QRectF(24, 282, W - 48, 112)
    p.setPen(QPen(QColor(BORDER), 1))
    p.setBrush(QColor("#FFFFFF"))
    p.drawRoundedRect(card, 14, 14)
    p.setPen(QColor(INK))
    p.setFont(font(14, QFont.DemiBold))
    p.drawText(QPointF(card.left() + 20, card.top() + 26), CARD_TITLE)
    p.setPen(QColor(SOFT))
    f = font(13)
    p.setFont(f)
    fm = QFontMetricsF(f)
    for i, (number, line) in enumerate(STEPS):
        assert fm.horizontalAdvance(line) < card.width() - 60, line
        y = card.top() + 48 + i * 18
        if number:
            p.drawText(QPointF(card.left() + 20, y), number)
        p.drawText(QPointF(card.left() + 42, y), line)
    p.end()
    return img


def main() -> int:
    QGuiApplication.instance() or QGuiApplication(sys.argv[:1])
    os.makedirs(OUT, exist_ok=True)
    draw(1).save(os.path.join(OUT, "fond.png"))
    draw(2).save(os.path.join(OUT, "fond@2x.png"))
    print("écrit dans", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
