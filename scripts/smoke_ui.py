"""Offscreen smoke test: build each UI piece and render where visual.

Does not start the Windows hook. Catches import errors, Qt construction errors
and obvious paint crashes on Linux CI and in the cloud.
"""
import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QImage, QColor
from PIL import Image

from cerclic.settings import Settings
from cerclic.ui.toast import Toast
from cerclic.ui.dialogs import Busy
from cerclic.ui.settings_window import SettingsWindow
from cerclic.ui.crop import CropDialog
from cerclic.ui.trayicon import make_icon
import cerclic.app  # import graph must be clean

HERE = os.path.dirname(__file__)


def grab(widget, name, bg=QColor(60, 63, 72)):
    widget.adjustSize()
    img = QImage(widget.size(), QImage.Format_ARGB32)
    img.fill(bg)
    widget.render(img)
    img.save(os.path.join(HERE, name))
    print("ok", name, widget.size().width(), "x", widget.size().height())


app = QApplication(sys.argv)

make_icon(64).pixmap(64, 64).save(os.path.join(HERE, "smoke_icon.png"))
print("ok icon")

grab(Toast("Compresser", ["/tmp/a (compressed).jpg"], ok=True), "smoke_toast.png")
grab(Toast("Signer a échoué", [], ok=False, error="signature introuvable"),
     "smoke_toast_err.png")
grab(Busy("Compresser..."), "smoke_busy.png")
grab(SettingsWindow(Settings()), "smoke_settings.png")

# crop needs a real image
p = os.path.join(HERE, "_crop_src.png")
Image.new("RGB", (900, 600), (70, 130, 180)).save(p)
dlg = CropDialog(p)
dlg.canvas.sel = dlg.canvas._img_rect().adjusted(60, 40, -60, -40)
grab(dlg, "smoke_crop.png")

print("ALL UI OK")
