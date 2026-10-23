"""Render the wheel to PNGs (off-screen) for the README: docs/preview_*.png."""
import os
import sys
import time

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from PySide6.QtCore import QPoint  # noqa: E402
from PySide6.QtGui import QColor, QImage, QPainter, QLinearGradient  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from cerclic.actions.registry import count_by_category, menu_for  # noqa: E402
from cerclic.ui.radial import Wheel  # noqa: E402
from cerclic.ui.theme import apply_app_theme  # noqa: E402


def _pump(seconds: float) -> None:
    end = time.time() + seconds
    while time.time() < end:
        QApplication.processEvents()
        time.sleep(0.01)


def render(paths, summary, name, hover=-1, preview=None):
    w = Wheel(menu_for(paths), count_by_category(paths), summary, preview=preview)
    w.popup_at(QPoint(500, 500))
    _pump(0.6)
    if hover >= 0:
        w._set_hover(hover, False)
        _pump(0.4)
    img = QImage(w.size(), QImage.Format_ARGB32)
    p = QPainter(img)
    g = QLinearGradient(0, 0, img.width(), img.height())
    g.setColorAt(0, QColor(150, 185, 230))          # a light desktop, like Windows 11
    g.setColorAt(1, QColor(70, 110, 180))
    p.fillRect(img.rect(), g)
    w.render(p, QPoint(0, 0))
    p.end()
    out = os.path.join(ROOT, "docs", name)
    img.save(out)
    w.close()
    print("wrote", out)


app = QApplication(sys.argv)
apply_app_theme(app)
sample = os.environ.get("CERCLIC_PREVIEW_PHOTO")
render(["photo.jpg"], "photo.jpg", "preview_image.png", hover=3, preview=sample)
render(["a.jpg", "b.pdf", "c.mp4", "d.m4a"], "4 fichiers", "preview_mixed.png", hover=1)
