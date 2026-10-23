"""The logos of the Microsoft Store package, drawn from Cerclic's own logo
(cerclic/ui/logo.py), and the resource index that lets Windows pick them.

The set is the one Firefox ships in its Store package (proven in daily use):
each logo at scale 200, plus the taskbar icon at 256 px in its three forms
(plated, unplated for dark taskbars, unplated for light ones). Windows scales
them down where needed.
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# file -> (width, height, logo size as a share of the height, vertical shift)
ASSETS = {
    "Square44x44Logo.scale-200.png": (88, 88, 0.78, 0.0),
    "Square44x44Logo.targetsize-256.png": (256, 256, 0.78, 0.0),
    "Square44x44Logo.altform-unplated_targetsize-256.png": (256, 256, 1.0, 0.0),
    "Square44x44Logo.altform-lightunplated_targetsize-256.png": (256, 256, 1.0, 0.0),
    "Square150x150Logo.scale-200.png": (300, 300, 0.50, -0.06),
    "Wide310x150Logo.scale-200.png": (620, 300, 0.52, -0.05),
    "SmallTile.scale-200.png": (142, 142, 0.66, 0.0),
    "LargeTile.scale-200.png": (620, 620, 0.46, -0.05),
    "StoreLogo.scale-200.png": (100, 100, 0.92, 0.0),
}

# What the manifest names -> the files Windows chooses from (with their qualifiers).
RESOURCES = {
    "Files/Assets/Square44x44Logo.png": [
        ((("TargetSize", "256"), ("AlternateForm", "unplated")),
         "Assets\\Square44x44Logo.altform-unplated_targetsize-256.png"),
        ((("TargetSize", "256"), ("AlternateForm", "lightunplated")),
         "Assets\\Square44x44Logo.altform-lightunplated_targetsize-256.png"),
        ((("TargetSize", "256"),), "Assets\\Square44x44Logo.targetsize-256.png"),
        ((("Scale", "200"),), "Assets\\Square44x44Logo.scale-200.png"),
    ],
    "Files/Assets/Square150x150Logo.png": [
        ((("Scale", "200"),), "Assets\\Square150x150Logo.scale-200.png")],
    "Files/Assets/Wide310x150Logo.png": [
        ((("Scale", "200"),), "Assets\\Wide310x150Logo.scale-200.png")],
    "Files/Assets/SmallTile.png": [
        ((("Scale", "200"),), "Assets\\SmallTile.scale-200.png")],
    "Files/Assets/LargeTile.png": [
        ((("Scale", "200"),), "Assets\\LargeTile.scale-200.png")],
    "Files/Assets/StoreLogo.png": [
        ((("Scale", "200"),), "Assets\\StoreLogo.scale-200.png")],
}


def _qt():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    from PySide6.QtWidgets import QApplication     # (widgets may follow: tests)
    return QApplication.instance() or QApplication([])


def render(width: int, height: int, share: float, shift: float):
    """A QImage: the logo centred on a transparent canvas."""
    _qt()
    from PySide6.QtCore import QRectF, Qt
    from PySide6.QtGui import QImage, QPainter
    from cerclic.ui.logo import paint_logo
    img = QImage(width, height, QImage.Format_ARGB32_Premultiplied)
    img.fill(Qt.transparent)
    p = QPainter(img)
    p.setRenderHint(QPainter.Antialiasing, True)
    size = height * share
    x = (width - size) / 2
    y = (height - size) / 2 + shift * height
    paint_logo(p, QRectF(x, y, size, size))
    p.end()
    return img


def write_assets(folder: str) -> list[str]:
    """Write the logos into folder/Assets; returns the paths written."""
    out = os.path.join(folder, "Assets")
    os.makedirs(out, exist_ok=True)
    written = []
    for name, (w, h, share, shift) in ASSETS.items():
        path = os.path.join(out, name)
        if not render(w, h, share, shift).save(path, "PNG"):
            raise OSError(f"impossible d'écrire {path}")
        written.append(path)
    return written


def write_index(folder: str, name: str) -> str:
    """resources.pri for these logos (name: the package's identity name)."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import pri
    path = os.path.join(folder, "resources.pri")
    with open(path, "wb") as f:
        f.write(pri.build_pri(name, RESOURCES))
    return path


def store_listing_images(folder: str) -> list[str]:
    """The square and poster images Partner Center asks for the listing, on
    Cerclic's frosted tile (1:1 at 1080 and 2160 px, 2:3 at 720x1080 and
    1440x2160)."""
    _qt()
    from PySide6.QtCore import QPointF, QRectF, Qt
    from PySide6.QtGui import QColor, QImage, QLinearGradient, QPainter, QRadialGradient
    from cerclic.ui.logo import paint_logo
    os.makedirs(folder, exist_ok=True)
    written = []
    for w, h, fname in ((1080, 1080, "logo-carre-1080.png"), (2160, 2160, "logo-carre-2160.png"),
                        (720, 1080, "affiche-720x1080.png"), (1440, 2160, "affiche-1440x2160.png")):
        img = QImage(w, h, QImage.Format_ARGB32_Premultiplied)
        p = QPainter(img)
        p.setRenderHint(QPainter.Antialiasing, True)
        g = QLinearGradient(QPointF(0, 0), QPointF(w, h))
        g.setColorAt(0.0, QColor("#F4F8FF"))
        g.setColorAt(1.0, QColor("#DCE7FA"))
        p.fillRect(QRectF(0, 0, w, h), g)
        glow = QRadialGradient(QPointF(w * 0.5, h * 0.45), max(w, h) * 0.55)
        glow.setColorAt(0.0, QColor(255, 255, 255, 200))
        glow.setColorAt(1.0, QColor(255, 255, 255, 0))
        p.fillRect(QRectF(0, 0, w, h), glow)
        size = min(w, h) * 0.56
        paint_logo(p, QRectF((w - size) / 2, (h - size) / 2 - h * 0.02, size, size))
        p.setPen(Qt.NoPen)
        p.end()
        path = os.path.join(folder, fname)
        img.save(path, "PNG")
        written.append(path)
    return written
