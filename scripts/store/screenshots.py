"""Screenshots and the tile icon for the Microsoft Store listing.

    python scripts/store/screenshots.py     -> dist_store/fiche/

Cerclic's real windows (the wheel, the compression and social formats
popups, the settings), drawn off-screen at 1920 x 1080 (1.5 x scale, as on
most laptops) over a plain desktop background, with a sample photo drawn here.
"""
from __future__ import annotations

import os
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)
# A 1920 x 1080 screen shown at 150 %, as on most laptops: Cerclic lays its
# windows out for 1280 x 720 and draws them with 1.5 times more pixels.
# (Qt cuts the platform options at each ":", so the file is named without its
# folder: no drive letter. Every other path here is absolute.)
os.chdir(tempfile.gettempdir())
_CFG = "cerclic-ecran-fiche.json"
with open(_CFG, "w", encoding="utf-8") as _f:
    _f.write('{"screens": [{"name": "Ecran", "x": 0, "y": 0, "width": 1920, '
             '"height": 1080, "logicalDpi": 96, "logicalBaseDpi": 96}]}')
os.environ["QT_QPA_PLATFORM"] = "offscreen:configfile=" + _CFG
os.environ["QT_SCALE_FACTOR"] = "1.5"

from PySide6.QtCore import QPoint, QPointF, QRectF, Qt  # noqa: E402
from PySide6.QtGui import (QColor, QFont, QImage, QLinearGradient, QPainter,  # noqa: E402
                           QPainterPath, QRadialGradient)
from PySide6.QtWidgets import QApplication  # noqa: E402

W, H = 1920, 1080
OUT = os.path.join(ROOT, "dist_store", "fiche")

CAPTIONS = {
    "1-roue.png": "Clic droit sur une image, puis « Cerclic » : toutes les actions "
                  "s'ouvrent en roue, autour de ta souris.",
    "2-compresser.png": "Compresser en voyant la taille obtenue avant de valider, "
                        "avec une loupe pour juger la qualité.",
    "3-reseaux.png": "Mettre une photo ou une vidéo au format d'Instagram, TikTok ou "
                     "YouTube : tu choisis le cadrage.",
    "4-pdf.png": "Signer, fusionner, compresser, protéger ou convertir tes PDF en "
                 "un geste.",
    "5-reglages.png": "Des réglages simples : raccourci clavier, clic droit, lancement "
                      "avec Windows. Tout reste sur ton PC.",
}


def pump(seconds: float) -> None:
    end = time.time() + seconds
    while time.time() < end:
        QApplication.processEvents()
        time.sleep(0.01)


def wait_for(cond, timeout: float = 30.0) -> None:
    end = time.time() + timeout
    while time.time() < end:
        QApplication.processEvents()
        if cond():
            return
        time.sleep(0.02)
    raise TimeoutError("l'écran ne s'est pas préparé à temps")


def sample_photo(folder: str) -> str:
    """A landscape drawn here (no outside picture): sky, sun, hills, a lake."""
    w, h = 3000, 2000
    img = QImage(w, h, QImage.Format_RGB32)
    p = QPainter(img)
    p.setRenderHint(QPainter.Antialiasing, True)
    sky = QLinearGradient(0, 0, 0, h * 0.62)
    sky.setColorAt(0.0, QColor("#2B4C8C"))
    sky.setColorAt(0.55, QColor("#E58C7A"))
    sky.setColorAt(1.0, QColor("#F6C97F"))
    p.fillRect(0, 0, w, h, sky)
    sun = QRadialGradient(QPointF(w * 0.62, h * 0.50), h * 0.22)
    sun.setColorAt(0.0, QColor(255, 236, 190, 255))
    sun.setColorAt(0.25, QColor(255, 214, 150, 230))
    sun.setColorAt(1.0, QColor(255, 200, 140, 0))
    p.setPen(Qt.NoPen)
    p.setBrush(sun)
    p.drawEllipse(QPointF(w * 0.62, h * 0.50), h * 0.22, h * 0.22)
    for i, (color, base, amp) in enumerate((("#6B5B8E", 0.50, 0.10), ("#4A4878", 0.56, 0.08),
                                            ("#2F3560", 0.61, 0.06))):
        path = QPainterPath(QPointF(0, h))
        steps = 12
        for k in range(steps + 1):
            x = w * k / steps
            y = h * (base - amp * (0.5 + 0.5 * __import__("math").sin(k * 1.3 + i * 2.1)))
            path.lineTo(x, y)
        path.lineTo(w, h)
        path.closeSubpath()
        p.setBrush(QColor(color))
        p.drawPath(path)
    lake = QLinearGradient(0, h * 0.64, 0, h)
    lake.setColorAt(0.0, QColor("#F2B88A"))
    lake.setColorAt(0.4, QColor("#8C7CA8"))
    lake.setColorAt(1.0, QColor("#22305A"))
    p.fillRect(QRectF(0, h * 0.64, w, h * 0.36), lake)
    p.setBrush(QColor(255, 230, 190, 120))
    for k in range(9):
        y = h * (0.68 + k * 0.03)
        p.drawRoundedRect(QRectF(w * 0.62 - (180 - k * 14), y, 2 * (180 - k * 14), 6), 3, 3)
    p.end()
    path = os.path.join(folder, "Lac au coucher du soleil.jpg")
    img.save(path, "JPG", 92)
    return path


def sample_pdf(folder: str) -> str:
    import pymupdf
    doc = pymupdf.open()
    for n in range(3):
        page = doc.new_page()
        page.insert_text((72, 90), f"Contrat de prestation, page {n + 1}", fontsize=18)
        for k in range(18):
            page.insert_text((72, 140 + k * 26), "Texte du contrat. " * 5, fontsize=10)
    path = os.path.join(folder, "Contrat.pdf")
    doc.save(path)
    return path


def desktop() -> QImage:
    img = QImage(W, H, QImage.Format_ARGB32_Premultiplied)
    p = QPainter(img)
    p.setRenderHint(QPainter.Antialiasing, True)
    g = QLinearGradient(0, 0, W, H)
    g.setColorAt(0.0, QColor("#B9CCEB"))
    g.setColorAt(0.5, QColor("#7E9DD6"))
    g.setColorAt(1.0, QColor("#4C6FB5"))
    p.fillRect(img.rect(), g)
    for cx, cy, r, a in ((0.18, 0.25, 0.45, 70), (0.85, 0.80, 0.55, 60), (0.70, 0.15, 0.30, 45)):
        glow = QRadialGradient(QPointF(W * cx, H * cy), W * r)
        glow.setColorAt(0.0, QColor(255, 255, 255, a))
        glow.setColorAt(1.0, QColor(255, 255, 255, 0))
        p.fillRect(img.rect(), glow)
    p.end()
    return img


def thumbnail(path: str) -> QImage:
    """The file as the desktop shows it: the picture, or a PDF's first page."""
    if path.lower().endswith(".pdf"):
        import pymupdf
        with pymupdf.open(path) as doc:
            pix = doc[0].get_pixmap(dpi=60)
            img = QImage(pix.samples, pix.width, pix.height, pix.stride,
                         QImage.Format_RGB888).copy()
    else:
        img = QImage(path)
    return img.scaled(330, 330, Qt.KeepAspectRatio, Qt.SmoothTransformation)


def file_tile(canvas: QImage, path: str, center: QPointF) -> None:
    """A selected file on the desktop: its thumbnail and its name."""
    thumb = thumbnail(path)
    p = QPainter(canvas)
    p.setRenderHint(QPainter.Antialiasing, True)
    p.setRenderHint(QPainter.SmoothPixmapTransform, True)
    box = QRectF(center.x() - 210, center.y() - 225, 420, 470)
    p.setPen(QColor(255, 255, 255, 150))
    p.setBrush(QColor(255, 255, 255, 60))
    p.drawRoundedRect(box, 22, 22)
    tw, th = thumb.width(), thumb.height()
    top = QRectF(center.x() - tw / 2, box.top() + 30 + (330 - th) / 2, tw, th)
    p.setPen(Qt.NoPen)
    for k in range(16, 0, -1):                       # a soft shadow
        p.setBrush(QColor(20, 40, 90, 5))
        p.drawRoundedRect(top.adjusted(-k, -k + 8, k, k + 8), 8 + k, 8 + k)
    clip = QPainterPath()
    clip.addRoundedRect(top, 8, 8)
    p.setClipPath(clip)
    p.drawImage(top, thumb)
    p.setClipping(False)
    font = QFont("Inter")
    font.setPixelSize(27)
    font.setWeight(QFont.DemiBold)
    p.setFont(font)
    text_rect = QRectF(box.left() + 10, box.bottom() - 82, box.width() - 20, 70)
    p.setPen(QColor(20, 40, 90, 110))
    p.drawText(text_rect.translated(0, 2), Qt.AlignHCenter | Qt.AlignTop | Qt.TextWordWrap,
               os.path.basename(path))
    p.setPen(QColor("#FFFFFF"))
    p.drawText(text_rect, Qt.AlignHCenter | Qt.AlignTop | Qt.TextWordWrap,
               os.path.basename(path))
    p.end()


def put(canvas: QImage, widget, center: QPointF) -> None:
    """Draw a window as the screen shows it, centred on `center` (pixels)."""
    pm = widget.grab()
    pm.setDevicePixelRatio(1.0)          # its own pixels, one for one
    p = QPainter(canvas)
    p.drawPixmap(QPointF(center.x() - pm.width() / 2, center.y() - pm.height() / 2), pm)
    p.end()


def main() -> int:
    app = QApplication.instance() or QApplication(sys.argv[:1])
    QFont.insertSubstitution("Segoe UI", "Inter")      # Windows' font, as close as here
    from cerclic.ui.theme import apply_app_theme
    apply_app_theme(app)
    os.makedirs(os.path.join(OUT, "captures"), exist_ok=True)
    work = tempfile.mkdtemp(prefix="cerclic-fiche-")
    photo = sample_photo(work)
    pdf = sample_pdf(work)
    from cerclic.actions.registry import count_by_category, menu_for
    from cerclic.ui.radial import Wheel

    def wheel(paths, summary, hover, name, preview=None):
        w = Wheel(menu_for(paths), count_by_category(paths), summary, preview=preview)
        w.popup_at(QPoint(640, 360))
        pump(0.6)
        w._set_hover(hover, False)
        pump(0.5)
        img = desktop()
        file_tile(img, paths[0], QPointF(W * 0.27, H * 0.50))
        put(img, w, QPointF(W * 0.60, H * 0.50))
        img.save(os.path.join(OUT, "captures", name))
        w.close()

    wheel([photo], os.path.basename(photo), 1, "1-roue.png", preview=photo)
    wheel([pdf], os.path.basename(pdf), 0, "4-pdf.png")

    from cerclic.ui.compress_editor import CompressEditor
    ed = CompressEditor([photo], "image", quality=60)
    ed.start(QPoint(640, 360))
    wait_for(lambda: ed.after is not None and not ed._busy, 60)
    pump(0.4)
    img = desktop()
    put(img, ed, QPointF(W / 2, H / 2))
    img.save(os.path.join(OUT, "captures", "2-compresser.png"))
    ed.close()

    from cerclic.ui.social_editor import SocialEditor
    se = SocialEditor([photo], "story", "blur")
    se.start(QPoint(640, 360))
    wait_for(lambda: se.canvas.image is not None, 30)
    pump(0.6)
    img = desktop()
    put(img, se, QPointF(W / 2, H / 2))
    img.save(os.path.join(OUT, "captures", "3-reseaux.png"))
    se.close()

    from cerclic.settings import Settings
    from cerclic.ui.settings_window import SettingsWindow
    sw = SettingsWindow(Settings(), store=True)
    sw.resize(900, 600)
    sw.show()
    pump(0.6)
    img = desktop()
    put(img, sw, QPointF(W / 2, H / 2))
    img.save(os.path.join(OUT, "captures", "5-reglages.png"))
    sw.close()

    sys.path.insert(0, HERE)
    import assets
    icon = assets.render(300, 300, 0.92, 0.0)
    icon.save(os.path.join(OUT, "icone-300x300.png"))
    with open(os.path.join(OUT, "captures", "legendes.txt"), "w", encoding="utf-8-sig",
              newline="\r\n") as f:
        for name, text in CAPTIONS.items():
            f.write(f"{name}\n{text}\n\n")
    print("écrit dans", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
