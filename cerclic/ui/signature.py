"""Signature: draw it once (or import a photo of it), then place it on the page.

SignaturePad   draw with the mouse; saved as a transparent PNG for next time.
SignPlacer     the PDF page with the signature on it: drag to move, drag a
               corner to resize, Enter to sign.
"""
from __future__ import annotations

import os

from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from PySide6.QtGui import QColor, QImage, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QFileDialog, QLabel, QPushButton, QWidget

from ..settings import config_dir
from .editor_base import EditorWindow, Loader
from .theme import MUTED, font

INK = QColor(16, 32, 74)
PEN_W = 3.0
HANDLE = 12


def signature_path() -> str:
    return os.path.join(config_dir(), "signature.png")


# ----- importing a picture of a signature ----------------------------------------

def import_signature(src: str, dst: str) -> str:
    """Copy a signature picture as a transparent PNG: paper becomes see-through,
    ink keeps its colour, the result is trimmed to the ink."""
    from PIL import Image, ImageOps
    from ..actions import images as _images  # HEIC support
    _ = _images
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        im.load()
    has_alpha = im.mode in ("RGBA", "LA", "PA") or (im.mode == "P" and "transparency" in im.info)
    rgba = im.convert("RGBA")
    if has_alpha and rgba.getchannel("A").getextrema()[0] < 250:
        out = rgba
    else:
        gray = rgba.convert("L")
        hist = gray.histogram()
        total = sum(hist)

        def pct(q):
            acc = 0
            for v, c in enumerate(hist):
                acc += c
                if acc >= total * q:
                    return v
            return 255

        paper, ink = pct(0.80), pct(0.02)
        span = max(16, paper - ink)
        alpha = gray.point(lambda v: max(0, min(255, int((paper - v) * 255 * 1.4 / span))))
        out = rgba.copy()
        out.putalpha(alpha)
    box = out.getchannel("A").point(lambda a: 255 if a > 24 else 0).getbbox()
    if not box:
        raise ValueError("Aucun trait de signature trouvé dans cette image.")
    pad = 6
    box = (max(0, box[0] - pad), max(0, box[1] - pad),
           min(out.width, box[2] + pad), min(out.height, box[3] + pad))
    out = out.crop(box)
    if out.width > 1400:
        out.thumbnail((1400, 1400), Image.Resampling.LANCZOS)
    tmp = dst + ".tmp.png"
    out.save(tmp, "PNG")
    os.replace(tmp, dst)
    return dst


# ----- drawing pad ---------------------------------------------------------------------

class _Pad(QWidget):
    changed = Signal()

    def __init__(self):
        super().__init__()
        self.setMinimumSize(520, 220)
        self.setCursor(Qt.CrossCursor)
        self.strokes: list[list[QPointF]] = []

    def area(self) -> QRectF:
        w = min(self.width() - 80, 900)
        h = min(self.height() - 60, w * 0.38)
        return QRectF((self.width() - w) / 2, (self.height() - h) / 2, w, h)

    def clear(self) -> None:
        self.strokes = []
        self.update()
        self.changed.emit()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton and self.area().contains(e.position()):
            self.strokes.append([e.position()])
            self.update()

    def mouseMoveEvent(self, e):
        if self.strokes and e.buttons() & Qt.LeftButton:
            a = self.area()
            p = e.position()
            p = QPointF(min(max(a.left(), p.x()), a.right()),
                        min(max(a.top(), p.y()), a.bottom()))
            last = self.strokes[-1][-1]
            if (p - last).manhattanLength() >= 1.5:
                self.strokes[-1].append(p)
                self.update()

    def mouseReleaseEvent(self, e):
        if self.strokes:
            self.changed.emit()

    @staticmethod
    def _path(points: list[QPointF]) -> QPainterPath:
        path = QPainterPath(points[0])
        if len(points) == 1:
            path.lineTo(points[0] + QPointF(0.1, 0.1))
            return path
        for i in range(1, len(points) - 1):
            mid = (points[i] + points[i + 1]) / 2
            path.quadTo(points[i], mid)
        path.lineTo(points[-1])
        return path

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        a = self.area()
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(250, 250, 247))
        p.drawRoundedRect(a, 14, 14)
        p.setPen(QPen(QColor(190, 192, 200), 1, Qt.DashLine))
        base = a.bottom() - a.height() * 0.25
        p.drawLine(QPointF(a.left() + 40, base), QPointF(a.right() - 40, base))
        if not self.strokes:
            p.setPen(QColor(150, 152, 160))
            p.setFont(font(12))
            p.drawText(a, Qt.AlignCenter, "Signe ici avec la souris")
        pen = QPen(INK, PEN_W)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        p.setPen(pen)
        p.setBrush(Qt.NoBrush)
        for s in self.strokes:
            p.drawPath(self._path(s))

    def export(self, path: str) -> bool:
        pts = [pt for s in self.strokes for pt in s]
        if not pts:
            return False
        xs, ys = [pt.x() for pt in pts], [pt.y() for pt in pts]
        pad = PEN_W * 2
        box = QRectF(min(xs) - pad, min(ys) - pad,
                     max(xs) - min(xs) + 2 * pad, max(ys) - min(ys) + 2 * pad)
        scale = 3.0
        img = QImage(int(box.width() * scale) + 1, int(box.height() * scale) + 1,
                     QImage.Format_ARGB32_Premultiplied)
        img.fill(Qt.transparent)
        p = QPainter(img)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.scale(scale, scale)
        p.translate(-box.left(), -box.top())
        pen = QPen(INK, PEN_W)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        p.setPen(pen)
        for s in self.strokes:
            p.drawPath(self._path(s))
        p.end()
        tmp = path + ".tmp.png"
        if not img.save(tmp, "PNG"):
            return False
        os.replace(tmp, path)
        return True


class SignaturePad(EditorWindow):
    """accepted({"signature": path})"""

    def __init__(self):
        super().__init__("Ta signature", "Elle sera gardée pour les prochaines fois · "
                                         "Entrée pour enregistrer · Échap pour annuler")
        self.pad = _Pad()
        self.pad.changed.connect(self._sync)
        self.center.addWidget(self.pad, 1)
        imp = QPushButton("Importer une image…")
        imp.setObjectName("ghost")
        imp.setToolTip("Une photo de ta signature sur papier blanc")
        imp.clicked.connect(self._import)
        clear = QPushButton("Effacer")
        clear.setObjectName("ghost")
        clear.clicked.connect(self.pad.clear)
        self.msg = QLabel("")
        self.msg.setObjectName("hint")
        cancel = QPushButton("Annuler")
        cancel.setObjectName("ghost")
        cancel.clicked.connect(self.cancel)
        self.ok = QPushButton("Enregistrer")
        self.ok.setObjectName("primary")
        self.ok.clicked.connect(self.validate)
        for w in (imp, clear, self.msg):
            self.bar.addWidget(w)
        self.bar.addStretch(1)
        self.bar.addWidget(cancel)
        self.bar.addWidget(self.ok)
        self._sync()

    def start(self) -> None:
        self.open_on_cursor_screen()

    def _sync(self) -> None:
        self.ok.setEnabled(bool(self.pad.strokes))

    def _import(self) -> None:
        src, _ = QFileDialog.getOpenFileName(
            self, "Choisir une image de ta signature", "",
            "Images (*.png *.jpg *.jpeg *.webp *.heic *.bmp)")
        if not src:
            return
        try:
            path = import_signature(src, signature_path())
        except Exception as exc:
            self.msg.setText(str(exc) if isinstance(exc, ValueError)
                             else "Image illisible.")
            return
        self.finish({"signature": path})

    def validate(self) -> None:
        if self.pad.strokes and self.pad.export(signature_path()):
            self.finish({"signature": signature_path()})


# ----- placement editor -------------------------------------------------------------------

class _PlaceCanvas(QWidget):
    double_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.page_img = None
        self.page_size = (1.0, 1.0)
        self.sig_img: QImage | None = None
        self.box = QRectF(0.6, 0.8, 0.28, 0.08)   # relative to the page
        self.message = "Chargement…"
        self._mode = None
        self._press = QPointF()
        self._press_box = QRectF()

    def _view(self) -> QRectF:
        W, H = self.page_size
        m = 36
        aw, ah = max(1.0, self.width() - 2 * m), max(1.0, self.height() - 2 * m)
        s = min(aw / W, ah / H)
        return QRectF((self.width() - W * s) / 2, (self.height() - H * s) / 2, W * s, H * s)

    def box_view(self) -> QRectF:
        v = self._view()
        b = self.box
        return QRectF(v.x() + b.x() * v.width(), v.y() + b.y() * v.height(),
                      b.width() * v.width(), b.height() * v.height())

    def rel_box(self) -> tuple[float, float, float, float]:
        b = self.box
        return (b.left(), b.top(), b.right(), b.bottom())

    def _corner_at(self, pos: QPointF) -> str | None:
        r = self.box_view()
        for name, pt in (("tl", r.topLeft()), ("tr", r.topRight()),
                         ("br", r.bottomRight()), ("bl", r.bottomLeft())):
            if abs(pt.x() - pos.x()) <= HANDLE and abs(pt.y() - pos.y()) <= HANDLE:
                return name
        return None

    def mousePressEvent(self, e):
        if self.page_img is None or e.button() != Qt.LeftButton:
            return
        pos = e.position()
        self._press, self._press_box = pos, QRectF(self.box)
        corner = self._corner_at(pos)
        if corner:
            self._mode = corner
        elif self.box_view().contains(pos):
            self._mode = "move"
        else:  # click elsewhere on the page: bring the signature there
            v = self._view()
            if v.contains(pos):
                b = QRectF(self.box)
                b.moveCenter(QPointF((pos.x() - v.x()) / v.width(),
                                     (pos.y() - v.y()) / v.height()))
                self.box = self._clamp(b)
                self._press_box = QRectF(self.box)
                self._mode = "move"
                self.update()

    def mouseMoveEvent(self, e):
        pos = e.position()
        if self._mode is None:
            c = self._corner_at(pos)
            if c in ("tl", "br"):
                self.setCursor(Qt.SizeFDiagCursor)
            elif c in ("tr", "bl"):
                self.setCursor(Qt.SizeBDiagCursor)
            elif self.box_view().contains(pos):
                self.setCursor(Qt.SizeAllCursor)
            else:
                self.setCursor(Qt.PointingHandCursor if self._view().contains(pos)
                               else Qt.ArrowCursor)
            return
        v = self._view()
        dx = (pos.x() - self._press.x()) / v.width()
        dy = (pos.y() - self._press.y()) / v.height()
        b = QRectF(self._press_box)
        if self._mode == "move":
            b.translate(dx, dy)
            self.box = self._clamp(b)
        else:
            self.box = self._resize(self._mode, pos)
        self.update()

    def mouseReleaseEvent(self, e):
        self._mode = None

    def mouseDoubleClickEvent(self, e):
        if self.box_view().contains(e.position()):
            self.double_clicked.emit()

    def _clamp(self, b: QRectF) -> QRectF:
        b.moveLeft(min(max(0.0, b.left()), 1.0 - b.width()))
        b.moveTop(min(max(0.0, b.top()), 1.0 - b.height()))
        return b

    def _resize(self, corner: str, pos: QPointF) -> QRectF:
        """Resize from a corner, the opposite corner fixed, keeping proportions."""
        v = self._view()
        b = self._press_box
        anchor = {"tl": b.bottomRight(), "tr": b.bottomLeft(),
                  "br": b.topLeft(), "bl": b.topRight()}[corner]
        px = min(max(0.0, (pos.x() - v.x()) / v.width()), 1.0)
        aspect = b.width() / max(b.height(), 1e-9)       # in page fractions
        w = max(0.03, abs(px - anchor.x()))
        h = w / aspect
        right = corner in ("tr", "br")
        down = corner in ("bl", "br")
        maxw = (1.0 - anchor.x()) if right else anchor.x()
        maxh = (1.0 - anchor.y()) if down else anchor.y()
        k = min(1.0, maxw / w, maxh / h if h else 1.0)
        w, h = w * k, h * k
        x = anchor.x() if right else anchor.x() - w
        y = anchor.y() if down else anchor.y() - h
        return QRectF(x, y, w, h)

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.SmoothPixmapTransform, True)
        if self.page_img is None:
            p.setPen(QColor(MUTED))
            p.setFont(font(12))
            p.drawText(self.rect(), Qt.AlignCenter, self.message)
            return
        v = self._view()
        p.fillRect(v.adjusted(-1, -1, 1, 1), QColor(0, 0, 0, 90))
        p.drawImage(v, self.page_img)
        r = self.box_view()
        if self.sig_img is not None:
            p.drawImage(r, self.sig_img)
        p.setPen(QPen(QColor(76, 141, 255), 1.5, Qt.DashLine))
        p.setBrush(Qt.NoBrush)
        p.drawRect(r)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(76, 141, 255))
        for pt in (r.topLeft(), r.topRight(), r.bottomRight(), r.bottomLeft()):
            p.drawEllipse(pt, 5.5, 5.5)


class SignPlacer(EditorWindow):
    """accepted({"signature": path, "page": index, "sig_box": (x0, y0, x1, y1)})"""

    def __init__(self, pdf_path: str, signature: str, password: str | None = None):
        super().__init__(os.path.basename(pdf_path),
                         "Glisse la signature où tu veux, tire un coin pour la "
                         "redimensionner · Entrée pour signer")
        self.path, self.signature, self.password = pdf_path, signature, password
        self.canvas = _PlaceCanvas()
        self.canvas.double_clicked.connect(self.validate)
        self.center.addWidget(self.canvas, 1)
        self._load_signature()

        change = QPushButton("Changer de signature")
        change.setObjectName("ghost")
        change.clicked.connect(self._change_signature)
        self.prev_btn = QPushButton("‹")
        self.prev_btn.setFixedWidth(40)
        self.prev_btn.clicked.connect(lambda: self._goto(self.page - 1))
        self.page_label = QLabel("")
        self.next_btn = QPushButton("›")
        self.next_btn.setFixedWidth(40)
        self.next_btn.clicked.connect(lambda: self._goto(self.page + 1))
        cancel = QPushButton("Annuler")
        cancel.setObjectName("ghost")
        cancel.clicked.connect(self.cancel)
        self.ok = QPushButton("Signer")
        self.ok.setObjectName("primary")
        self.ok.setEnabled(False)
        self.ok.clicked.connect(self.validate)
        self.bar.addWidget(change)
        self.bar.addStretch(1)
        for w in (self.prev_btn, self.page_label, self.next_btn):
            self.bar.addWidget(w)
        self.bar.addStretch(1)
        self.bar.addWidget(cancel)
        self.bar.addWidget(self.ok)

        self.page = -1          # last page first
        self.page_count = 1
        self._placed = False
        self._token = 0
        self._loader = Loader(self)
        self._loader.done.connect(self._loaded)
        self._pad = None

    def start(self) -> None:
        self.open_on_cursor_screen()
        self._load()

    def _load_signature(self) -> None:
        img = QImage(self.signature)
        self.canvas.sig_img = img if not img.isNull() else None

    def _load(self) -> None:
        from .crop_editor import load_pdf_preview
        self._token += 1
        token = self._token
        dpr = self.devicePixelRatioF() or 1.0
        w = max(400, int((self.width() - 72) * dpr))
        h = max(300, int((self.height() - 180) * dpr))
        index = self.page if self.page >= 0 else 10 ** 6
        self.canvas.page_img = None
        self.canvas.message = "Chargement…"
        self.canvas.update()
        self._loader.run(lambda: (token, load_pdf_preview(self.path, index, w, h,
                                                          self.password)))

    def _loaded(self, res, err) -> None:
        if err:
            self.canvas.message = err
            self.canvas.update()
            return
        token, (img, size, count, index) = res
        if token != self._token:
            return
        self.page, self.page_count = index, count
        self.canvas.page_img = img
        self.canvas.page_size = size
        if not self._placed and self.canvas.sig_img is not None:
            from ..actions.pdf import default_signature_box
            x0, y0, x1, y1 = default_signature_box(size[0], size[1],
                                                   self.canvas.sig_img.width(),
                                                   self.canvas.sig_img.height())
            self.canvas.box = QRectF(x0, y0, x1 - x0, y1 - y0)
            self._placed = True
        self.page_label.setText(f"Page {index + 1} / {count}")
        self.prev_btn.setEnabled(index > 0)
        self.next_btn.setEnabled(index < count - 1)
        self.ok.setEnabled(self.canvas.sig_img is not None)
        self.canvas.update()

    def _goto(self, index: int) -> None:
        if 0 <= index < self.page_count and index != self.page:
            self.page = index
            self._load()

    def _change_signature(self) -> None:
        self.hide()
        pad = SignaturePad()
        self._pad = pad
        pad.accepted.connect(self._new_signature)
        pad.cancelled.connect(self._back_from_pad)
        pad.start()

    def _new_signature(self, result: dict) -> None:
        self.signature = result["signature"]
        self._load_signature()
        img = self.canvas.sig_img
        if img is not None:   # keep the place, adopt the new proportions
            b = self.canvas.box
            W, H = self.canvas.page_size
            h = b.width() * (img.height() / max(1, img.width())) * (W / H)
            self.canvas.box = self.canvas._clamp(QRectF(b.left(), b.bottom() - h,
                                                        b.width(), h))
        self._back_from_pad()

    def _back_from_pad(self, *_):
        self._pad = None
        self.ok.setEnabled(self.canvas.sig_img is not None)
        self.show()
        self.activateWindow()
        self.canvas.update()

    def validate(self) -> None:
        if self.canvas.page_img is None or self.canvas.sig_img is None:
            return
        self.finish({"signature": self.signature, "page": self.page,
                     "sig_box": self.canvas.rel_box()})
