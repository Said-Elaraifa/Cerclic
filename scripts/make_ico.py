"""Render the app icon to a multi-size Windows .ico, committed to assets/."""
import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QBuffer, QByteArray, QIODevice
from PIL import Image
import io

from cerclic.ui.trayicon import make_icon

app = QApplication(sys.argv)
sizes = [256, 128, 64, 48, 32, 16]
imgs = []
for s in sizes:
    pix = make_icon(s).pixmap(s, s)
    ba = QByteArray()
    buf = QBuffer(ba)
    buf.open(QIODevice.WriteOnly)
    pix.save(buf, "PNG")
    imgs.append(Image.open(io.BytesIO(bytes(ba))).convert("RGBA"))

out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "assets")
os.makedirs(out_dir, exist_ok=True)
out = os.path.join(out_dir, "cerclic.ico")
imgs[0].save(out, format="ICO", sizes=[(s, s) for s in sizes])
imgs[0].save(os.path.join(out_dir, "cerclic.png"))
print("wrote", out)
