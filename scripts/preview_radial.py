"""Render the wheel to PNGs (off-screen) for the README: docs/preview_*.png."""
import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from PySide6.QtCore import QPoint  # noqa: E402
from PySide6.QtGui import QColor, QImage, QPainter, QLinearGradient  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from cerclic.actions.registry import count_by_category, menu_for  # noqa: E402
from cerclic.ui.radial import Wheel  # noqa: E402
from cerclic.ui.theme import apply_app_theme  # noqa: E402


def render(paths, summary, name, hover=-1):
    w = Wheel(menu_for(paths), count_by_category(paths), summary)
    w.popup_at(QPoint(500, 500))
    w._grow = w._fade = 1.0
    w._hover = hover
    img = QImage(w.size(), QImage.Format_ARGB32)
    p = QPainter(img)
    g = QLinearGradient(0, 0, img.width(), img.height())
    g.setColorAt(0, QColor(58, 78, 118))
    g.setColorAt(1, QColor(32, 40, 62))
    p.fillRect(img.rect(), g)
    p.end()
    w.render(img)
    out = os.path.join(ROOT, "docs", name)
    img.save(out)
    w.close()
    print("wrote", out)


app = QApplication(sys.argv)
apply_app_theme(app)
render(["photo.jpg"], "photo.jpg", "preview_image.png", hover=2)
render(["a.jpg", "b.pdf", "c.pdf"], "3 fichiers", "preview_mixed.png")
