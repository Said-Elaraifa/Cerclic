"""Interactive crop window: shows the image, a draggable selection with corner
handles and aspect presets, and returns the box in source pixels.
"""
from __future__ import annotations

from PySide6.QtCore import Qt, QRect, QRectF, QPoint, QSize
from PySide6.QtGui import (QPixmap, QPainter, QColor, QPen, QImageReader,
                           QGuiApplication)
from PySide6.QtWidgets import (QDialog, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QLabel)

PRESETS = [("Libre", None), ("1:1", 1 / 1), ("4:5", 4 / 5), ("5:4", 5 / 4),
           ("16:9", 16 / 9), ("9:16", 9 / 16), ("3:2", 3 / 2), ("2:3", 2 / 3)]
HANDLE = 9


class _Canvas(QWidget):
    def __init__(self, pix: QPixmap):
        super().__init__()
        self.pix = pix
        self.setMinimumSize(200, 200)
        self.sel = QRect()
        self.aspect = None
        self._drag = None      # "new" | "move" | corner index 0..3
        self._press = QPoint()
        self._orig = QRect()
        self.setMouseTracking(True)

    # geometry of the displayed image inside the widget (letterboxed)
    def _img_rect(self) -> QRect:
        w, h = self.width(), self.height()
        iw, ih = self.pix.width(), self.pix.height()
        scale = min(w / iw, h / ih)
        dw, dh = int(iw * scale), int(ih * scale)
        return QRect((w - dw) // 2, (h - dh) // 2, dw, dh)

    def set_aspect(self, a):
        self.aspect = a
        r = self._img_rect()
        if a:
            # centre a max-size box of this aspect inside the image
            bw, bh = r.width(), int(r.width() / a)
            if bh > r.height():
                bh, bw = r.height(), int(r.height() * a)
            self.sel = QRect(r.x() + (r.width() - bw) // 2,
                             r.y() + (r.height() - bh) // 2, bw, bh)
        self.update()

    def _corners(self):
        r = self.sel
        return [r.topLeft(), r.topRight(), r.bottomRight(), r.bottomLeft()]

    def mousePressEvent(self, e):
        p = e.position().toPoint()
        self._press = p
        self._orig = QRect(self.sel)
        for i, c in enumerate(self._corners()):
            if (abs(c.x() - p.x()) <= HANDLE + 2 and
                    abs(c.y() - p.y()) <= HANDLE + 2) and not self.sel.isNull():
                self._drag = i
                return
        if not self.sel.isNull() and self.sel.contains(p):
            self._drag = "move"
        else:
            self._drag = "new"
            self.sel = QRect(p, QSize(1, 1))
        self.update()

    def mouseMoveEvent(self, e):
        if self._drag is None:
            return
        p = e.position().toPoint()
        r = self._img_rect()
        p.setX(max(r.left(), min(p.x(), r.right())))
        p.setY(max(r.top(), min(p.y(), r.bottom())))
        if self._drag == "move":
            d = p - self._press
            moved = self._orig.translated(d)
            if moved.left() < r.left():
                moved.moveLeft(r.left())
            if moved.top() < r.top():
                moved.moveTop(r.top())
            if moved.right() > r.right():
                moved.moveRight(r.right())
            if moved.bottom() > r.bottom():
                moved.moveBottom(r.bottom())
            self.sel = moved
        elif self._drag == "new":
            self.sel = self._constrained(self._press, p)
        else:  # corner resize
            fixed = self._corners()[(self._drag + 2) % 4]
            self.sel = self._constrained(fixed, p)
        self.update()

    def mouseReleaseEvent(self, e):
        self._drag = None
        self.sel = self.sel.normalized()

    def _constrained(self, a: QPoint, b: QPoint) -> QRect:
        rect = QRect(a, b).normalized()
        if self.aspect:
            w = rect.width()
            h = int(w / self.aspect)
            if b.y() < a.y():
                rect.setTop(rect.bottom() - h)
            else:
                rect.setHeight(h)
        return rect

    def paintEvent(self, _):
        p = QPainter(self)
        p.fillRect(self.rect(), QColor(18, 19, 24))
        r = self._img_rect()
        p.drawPixmap(r, self.pix)
        if self.sel.isNull():
            return
        # dim outside the selection
        shade = QColor(0, 0, 0, 130)
        s = self.sel.intersected(r)
        p.setPen(Qt.NoPen)
        p.setBrush(shade)
        p.drawRect(QRect(r.left(), r.top(), r.width(), s.top() - r.top()))
        p.drawRect(QRect(r.left(), s.bottom(), r.width(), r.bottom() - s.bottom()))
        p.drawRect(QRect(r.left(), s.top(), s.left() - r.left(), s.height()))
        p.drawRect(QRect(s.right(), s.top(), r.right() - s.right(), s.height()))
        # frame + thirds + handles
        p.setBrush(Qt.NoBrush)
        p.setPen(QPen(QColor(255, 255, 255), 2))
        p.drawRect(s)
        p.setPen(QPen(QColor(255, 255, 255, 90), 1))
        for k in (1, 2):
            x = s.left() + s.width() * k // 3
            y = s.top() + s.height() * k // 3
            p.drawLine(x, s.top(), x, s.bottom())
            p.drawLine(s.left(), y, s.right(), y)
        p.setBrush(QColor(255, 255, 255))
        p.setPen(Qt.NoPen)
        for c in self._corners():
            p.drawRect(QRect(c.x() - HANDLE // 2, c.y() - HANDLE // 2,
                             HANDLE, HANDLE))

    def box_in_image(self):
        r = self._img_rect()
        if self.sel.isNull() or self.sel.width() < 4 or self.sel.height() < 4:
            return None
        sx = self.pix.width() / r.width()
        sy = self.pix.height() / r.height()
        s = self.sel.intersected(r)
        return (round((s.left() - r.left()) * sx),
                round((s.top() - r.top()) * sy),
                round((s.right() - r.left()) * sx),
                round((s.bottom() - r.top()) * sy))


class CropDialog(QDialog):
    def __init__(self, image_path: str):
        super().__init__(None, Qt.Window)
        self.setWindowTitle("Rogner")
        reader = QImageReader(image_path)
        reader.setAutoTransform(True)
        pix = QPixmap.fromImage(reader.read())
        self._box = None

        screen = QGuiApplication.primaryScreen().availableGeometry()
        self.resize(min(pix.width() + 80, int(screen.width() * 0.85)),
                    min(pix.height() + 140, int(screen.height() * 0.85)))

        self.canvas = _Canvas(pix)
        lay = QVBoxLayout(self)
        tip = QLabel("Trace un cadre, ajuste les coins, puis valide. Entrée pour "
                     "rogner, Échap pour annuler.")
        tip.setStyleSheet("color:#9aa0b0;padding:4px;")
        lay.addWidget(tip)
        lay.addWidget(self.canvas, 1)

        row = QHBoxLayout()
        for label, a in PRESETS:
            b = QPushButton(label)
            b.setCheckable(True)
            b.clicked.connect(lambda _=False, asp=a, btn=b: self._preset(asp, btn))
            row.addWidget(b)
            self.__dict__.setdefault("_preset_btns", []).append(b)
        row.addStretch(1)
        ok = QPushButton("Rogner")
        ok.setDefault(True)
        ok.clicked.connect(self._confirm)
        cancel = QPushButton("Annuler")
        cancel.clicked.connect(self.reject)
        row.addWidget(cancel)
        row.addWidget(ok)
        lay.addLayout(row)
        self._style()

    def _style(self):
        self.setStyleSheet(
            "QDialog{background:#14151a;}"
            "QPushButton{background:#2a2d37;color:#eceef3;border:none;"
            "padding:7px 12px;border-radius:7px;}"
            "QPushButton:checked{background:#4C8DFF;}"
            "QPushButton:hover{background:#3a3e4c;}")

    def _preset(self, aspect, btn):
        for b in self._preset_btns:
            b.setChecked(b is btn)
        self.canvas.set_aspect(aspect)

    def _confirm(self):
        self._box = self.canvas.box_in_image()
        self.accept()

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key_Return, Qt.Key_Enter):
            self._confirm()
        elif e.key() == Qt.Key_Escape:
            self.reject()

    @property
    def box(self):
        return self._box

    @staticmethod
    def get_box(image_path: str):
        dlg = CropDialog(image_path)
        if dlg.exec() and dlg.box:
            return dlg.box
        return None
