"""Render the logo to the icon files committed in assets/:
cerclic.ico (Windows, many sizes), cerclic.png (256 px), cerclic.icns (macOS,
on its frosted tile, as macOS app icons are)."""
import io
import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from PIL import Image  # noqa: E402
from PySide6.QtCore import QBuffer, QByteArray, QIODevice  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from cerclic.ui.logo import logo_pixmap  # noqa: E402


def to_pil(pix) -> Image.Image:
    ba = QByteArray()
    buf = QBuffer(ba)
    buf.open(QIODevice.WriteOnly)
    pix.save(buf, "PNG")
    return Image.open(io.BytesIO(bytes(ba))).convert("RGBA")


app = QApplication(sys.argv)
out_dir = os.path.join(ROOT, "assets")
os.makedirs(out_dir, exist_ok=True)

sizes = [256, 128, 64, 48, 40, 32, 24, 20, 16]
imgs = {s: to_pil(logo_pixmap(s)) for s in sizes}
imgs[256].save(os.path.join(out_dir, "cerclic.ico"), format="ICO",
               sizes=[(s, s) for s in sizes], append_images=[imgs[s] for s in sizes[1:]])
imgs[256].save(os.path.join(out_dir, "cerclic.png"))

mac = to_pil(logo_pixmap(1024, plate=True))
mac.save(os.path.join(out_dir, "cerclic.icns"), format="ICNS")
mac.resize((512, 512), Image.LANCZOS).save(os.path.join(out_dir, "cerclic-mac.png"))
print("wrote cerclic.ico, cerclic.png, cerclic.icns")
