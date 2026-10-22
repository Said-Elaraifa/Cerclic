"""Render the radial menu to PNGs (offscreen) to eyeball the painting."""
import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QColor, QPainter, QImage

from cerclic.actions.registry import menu_for
from cerclic.ui.radial import RadialMenu


def render(menu, summary, name):
    w = RadialMenu(menu, summary)
    w._grow = 1.0
    w.resize(w.width(), w.height())
    img = QImage(w.size(), QImage.Format_ARGB32)
    img.fill(QColor(90, 94, 104))  # grey backdrop so translucency shows
    w.render(img)
    out = os.path.join(os.path.dirname(__file__), name)
    img.save(out)
    print("wrote", out)


app = QApplication(sys.argv)
render(menu_for(["a.pdf", "b.pdf"]), "2 PDF", "preview_pdf.png")
render(menu_for(["p.jpg"]), "photo.jpg", "preview_image.png")
render(menu_for(["a.jpg", "b.png", "c.pdf"]), "3 fichiers", "preview_mixed.png")
