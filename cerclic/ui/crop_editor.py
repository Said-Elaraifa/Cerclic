"""Crop editor for images and PDFs, in a compact popup where the wheel was.

The popup is sized to the picture (or PDF page) right away, from its header;
the picture itself is decoded in the background at exactly the size shown.
The frame starts on the whole picture: drag a corner or an edge to crop, drag
inside to move it, drag outside to draw a new one. Presets lock the
proportions. Enter crops, Escape cancels.

All selection maths happen in source units (pixels of the upright image, or
points of the visible PDF page), so nothing drifts with screen scaling.
"""
from __future__ import annotations

import os

from PySide6.QtCore import QPointF, QRectF, QSize, Qt, Signal
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QCheckBox, QLabel, QPushButton, QWidget

from ..paths import kind_of
from .editor_base import (EditorWindow, Loader, fit_view, qimage_from_pil,
                          qimage_from_rgb)
from ..system import ENTER_KEY
from .theme import MUTED, font

PRESETS = [("Libre", None), ("Original", "orig"), ("1:1", 1.0), ("4:5", 4 / 5),
           ("3:4", 3 / 4), ("16:9", 16 / 9), ("9:16", 9 / 16)]
HANDLE_HIT = 14     # px around a handle that grabs it
MARGIN = 12         # px around the picture (room for the handles)
MIN_VIEW = 12       # smallest frame, in screen px


def load_image_preview(path: str, max_w: int, max_h: int):
    """Upright preview that fits max_w x max_h, plus the full upright size."""
    from PIL import Image, ImageOps
    from ..actions import images as _images  # registers HEIC support
    _ = _images
    with Image.open(path) as im:
        w, h = im.size
        try:
            orient = im.getexif().get(0x0112, 1)
        except Exception:
            orient = 1
        full = (h, w) if orient in (5, 6, 7, 8) else (w, h)
        if im.format == "JPEG":
            want = (max_h, max_w) if orient in (5, 6, 7, 8) else (max_w, max_h)
            im.draft("RGB", want)
        im.load()
        up = ImageOps.exif_transpose(im)
    up.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
    return qimage_from_pil(up), full


def probe_size(path: str, page: int = 0, password=None):
    """Size of what the editor will show, read without decoding it (fast):
    (width, height, page_count, page_index). Pixels for an image, points of
    the visible page for a PDF. Falls back to 4:3 when unreadable."""
    try:
        if kind_of(path) == "pdf":
            from ..actions import pdf as _pdf
            with _pdf.open_pdf(path, password) as doc:
                n = doc.page_count
                i = max(0, min(page if page >= 0 else n - 1, n - 1))
                r = doc[i].rect
                return r.width, r.height, n, i
        from ..actions import images as _images
        w, h = _images.oriented_size(path)
        return float(w), float(h), 1, 0
    except Exception:
        return 800.0, 600.0, 1, 0


def load_pdf_preview(path: str, index: int, max_w: int, max_h: int, password):
    from ..actions import pdf as _pdf
    data, w, h, stride, count, size, index = _pdf.render_page(path, index, max_w, max_h,
                                                              password)
    return qimage_from_rgb(data, w, h, stride), size, count, index


class CropCanvas(QWidget):
    changed = Signal()
    double_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.setMinimumSize(120, 90)
        self.image = None
        self.full = (1.0, 1.0)
        self.sel = QRectF()
        self.aspect: float | None = None
        self.message = "Chargement…"
        self._mode = None
        self._press = QPointF()
        self._press_sel = QRectF()

    # -- data ------------------------------------------------------------------
    def set_image(self, image, full_size, keep_rel: tuple | None = None) -> None:
        self.image = image
        self.full = (float(full_size[0]), float(full_size[1]))
        W, H = self.full
        if keep_rel:              # another page: the frame the user drew stays
            x0, y0, x1, y1 = keep_rel
            self.sel = QRectF(x0 * W, y0 * H, (x1 - x0) * W, (y1 - y0) * H)
            if self.aspect:
                self.sel = self._with_aspect(self.sel)
        else:
            self.sel = QRectF(0, 0, W, H)
            if self.aspect:
                self.set_aspect(self.aspect)
        self.message = ""
        self.update()
        self.changed.emit()

    def _with_aspect(self, r: QRectF) -> QRectF:
        """`r` given the locked proportions (a page of another shape), same
        centre and width as far as the picture allows."""
        W, H = self.full
        w = min(r.width(), W)
        h = w / self.aspect
        if h > H:
            h = H
            w = h * self.aspect
        c = r.center()
        x = min(max(0.0, c.x() - w / 2), W - w)
        y = min(max(0.0, c.y() - h / 2), H - h)
        return QRectF(x, y, w, h)

    def bounds(self) -> QRectF:
        return QRectF(0, 0, self.full[0], self.full[1])

    def rel_box(self) -> tuple[float, float, float, float]:
        W, H = self.full
        s = self.sel.normalized()
        return (s.left() / W, s.top() / H, s.right() / W, s.bottom() / H)

    def pixel_box(self) -> tuple[int, int, int, int]:
        s = self.sel.normalized()
        W, H = self.full
        l = max(0, min(int(round(s.left())), int(W) - 1))
        t = max(0, min(int(round(s.top())), int(H) - 1))
        r = max(l + 1, min(int(round(s.right())), int(W)))
        b = max(t + 1, min(int(round(s.bottom())), int(H)))
        return (l, t, r, b)

    def reset(self) -> None:
        self.sel = self.bounds()
        if self.aspect:
            self.set_aspect(self.aspect)
        self.update()
        self.changed.emit()

    def set_aspect(self, aspect: float | None) -> None:
        """Largest frame of this aspect inside the picture, centred on the current one."""
        self.aspect = aspect
        if not aspect or self.image is None:
            self.update()
            return
        W, H = self.full
        w = W
        h = w / aspect
        if h > H:
            h = H
            w = h * aspect
        c = self.sel.center() if not self.sel.isEmpty() else QPointF(W / 2, H / 2)
        x = min(max(0.0, c.x() - w / 2), W - w)
        y = min(max(0.0, c.y() - h / 2), H - h)
        self.sel = QRectF(x, y, w, h)
        self.update()
        self.changed.emit()

    # -- view mapping ------------------------------------------------------------
    def _view(self) -> tuple[QRectF, float]:
        W, H = self.full
        aw = max(1.0, self.width() - 2 * MARGIN)
        ah = max(1.0, self.height() - 2 * MARGIN)
        s = min(aw / W, ah / H)
        dw, dh = W * s, H * s
        return QRectF((self.width() - dw) / 2, (self.height() - dh) / 2, dw, dh), s

    def to_view(self, r: QRectF) -> QRectF:
        v, s = self._view()
        return QRectF(v.x() + r.x() * s, v.y() + r.y() * s, r.width() * s, r.height() * s)

    def to_full(self, p: QPointF) -> QPointF:
        v, s = self._view()
        return QPointF((p.x() - v.x()) / s, (p.y() - v.y()) / s)

    # -- hit testing ---------------------------------------------------------------
    def _handles(self) -> dict[str, QPointF]:
        r = self.to_view(self.sel.normalized())
        cx, cy = r.center().x(), r.center().y()
        return {"tl": r.topLeft(), "tr": r.topRight(), "br": r.bottomRight(),
                "bl": r.bottomLeft(), "t": QPointF(cx, r.top()),
                "b": QPointF(cx, r.bottom()), "l": QPointF(r.left(), cy),
                "r": QPointF(r.right(), cy)}

    def handle_at(self, pos: QPointF) -> str | None:
        best, best_d = None, HANDLE_HIT + 1.0
        for name, pt in self._handles().items():
            d = max(abs(pt.x() - pos.x()), abs(pt.y() - pos.y()))
            if d < best_d:
                best, best_d = name, d
        return best if best_d <= HANDLE_HIT else None

    def _cursor_for(self, pos: QPointF):
        h = self.handle_at(pos)
        if h in ("tl", "br"):
            return Qt.SizeFDiagCursor
        if h in ("tr", "bl"):
            return Qt.SizeBDiagCursor
        if h in ("t", "b"):
            return Qt.SizeVerCursor
        if h in ("l", "r"):
            return Qt.SizeHorCursor
        if self.to_view(self.sel.normalized()).contains(pos):
            return Qt.SizeAllCursor
        return Qt.CrossCursor

    # -- mouse ----------------------------------------------------------------------
    def mousePressEvent(self, e):
        if self.image is None or e.button() != Qt.LeftButton:
            return
        pos = e.position()
        self._press = pos
        self._press_sel = QRectF(self.sel.normalized())
        h = self.handle_at(pos)
        if h:
            self._mode = h
        elif self.to_view(self._press_sel).contains(pos):
            self._mode = "move"
        else:
            self._mode = "new"

    def mouseMoveEvent(self, e):
        pos = e.position()
        if self._mode is None:
            if self.image is not None:
                self.setCursor(self._cursor_for(pos))
            return
        f = self._clamp_pt(self.to_full(pos))
        start = self._clamp_pt(self.to_full(self._press))
        if self._mode == "move":
            d = f - start
            r = self._press_sel.translated(d.x(), d.y())
            W, H = self.full
            r.moveLeft(min(max(0.0, r.left()), W - r.width()))
            r.moveTop(min(max(0.0, r.top()), H - r.height()))
            self.sel = r
        elif self._mode == "new":
            if (pos - self._press).manhattanLength() < 4:
                return
            self.sel = self._from_corners(start, f)
        else:
            self.sel = self._resize(self._mode, f)
        self.update()
        self.changed.emit()

    def mouseReleaseEvent(self, e):
        if self._mode is not None:
            self._mode = None
            self.sel = self._ensure_min(self.sel.normalized())
            self.update()
            self.changed.emit()

    def mouseDoubleClickEvent(self, e):
        if self.image is not None and self.to_view(self.sel.normalized()).contains(e.position()):
            self.double_clicked.emit()

    # -- geometry rules ----------------------------------------------------------------
    def _clamp_pt(self, p: QPointF) -> QPointF:
        W, H = self.full
        return QPointF(min(max(0.0, p.x()), W), min(max(0.0, p.y()), H))

    def _min_full(self) -> float:
        _, s = self._view()
        return max(1.0, MIN_VIEW / max(s, 1e-6))

    def _ensure_min(self, r: QRectF) -> QRectF:
        m = self._min_full()
        W, H = self.full
        if r.width() < m or r.height() < m:
            c = r.center()
            w, h = max(r.width(), min(m, W)), max(r.height(), min(m, H))
            if self.aspect:
                if w / h > self.aspect:
                    h = w / self.aspect
                else:
                    w = h * self.aspect
                w, h = min(w, W), min(h, H)
            x = min(max(0.0, c.x() - w / 2), W - w)
            y = min(max(0.0, c.y() - h / 2), H - h)
            return QRectF(x, y, w, h)
        return r

    def _from_corners(self, a: QPointF, b: QPointF) -> QRectF:
        """Frame from a fixed corner a to the cursor b, respecting the aspect."""
        W, H = self.full
        dx, dy = b.x() - a.x(), b.y() - a.y()
        w, h = abs(dx), abs(dy)
        if self.aspect:
            if h == 0 or w / max(h, 1e-9) > self.aspect:
                h = w / self.aspect
            else:
                w = h * self.aspect
            # keep inside the picture, shrinking both sides together
            maxw = a.x() if dx < 0 else W - a.x()
            maxh = a.y() if dy < 0 else H - a.y()
            k = min(1.0, maxw / w if w else 1.0, maxh / h if h else 1.0)
            w, h = w * k, h * k
        x = a.x() - w if dx < 0 else a.x()
        y = a.y() - h if dy < 0 else a.y()
        return QRectF(x, y, w, h)

    def _resize(self, handle: str, f: QPointF) -> QRectF:
        r = QRectF(self._press_sel)
        W, H = self.full
        if len(handle) == 2:  # corner: the opposite corner stays put
            anchor = {"tl": r.bottomRight(), "tr": r.bottomLeft(),
                      "br": r.topLeft(), "bl": r.topRight()}[handle]
            return self._from_corners(anchor, f)
        # edge
        if handle in ("l", "r"):
            if handle == "l":
                left, right = min(f.x(), r.right() - 1e-6), r.right()
            else:
                left, right = r.left(), max(f.x(), r.left() + 1e-6)
            w = right - left
            if not self.aspect:
                return QRectF(left, r.top(), w, r.height())
            h = w / self.aspect
            if h > H:
                h = H
                w = h * self.aspect
                if handle == "l":
                    left = right - w
            cy = r.center().y()
            top = min(max(0.0, cy - h / 2), H - h)
            return QRectF(left, top, w, h)
        if handle == "t":
            top, bottom = min(f.y(), r.bottom() - 1e-6), r.bottom()
        else:
            top, bottom = r.top(), max(f.y(), r.top() + 1e-6)
        h = bottom - top
        if not self.aspect:
            return QRectF(r.left(), top, r.width(), h)
        w = h * self.aspect
        if w > W:
            w = W
            h = w / self.aspect
            if handle == "t":
                top = bottom - h
        cx = r.center().x()
        left = min(max(0.0, cx - w / 2), W - w)
        return QRectF(left, top, w, h)

    # -- painting ---------------------------------------------------------------------
    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.SmoothPixmapTransform, True)
        if self.image is None:
            p.setPen(QColor(MUTED))
            p.setFont(font(12))
            p.drawText(self.rect(), Qt.AlignCenter, self.message)
            return
        v, _ = self._view()
        p.drawImage(v, self.image)
        s = self.to_view(self.sel.normalized())
        shade = QColor(0, 0, 0, 150)
        p.setPen(Qt.NoPen)
        p.setBrush(shade)
        p.drawRect(QRectF(v.left(), v.top(), v.width(), s.top() - v.top()))
        p.drawRect(QRectF(v.left(), s.bottom(), v.width(), v.bottom() - s.bottom()))
        p.drawRect(QRectF(v.left(), s.top(), s.left() - v.left(), s.height()))
        p.drawRect(QRectF(s.right(), s.top(), v.right() - s.right(), s.height()))
        p.setBrush(Qt.NoBrush)
        if self._mode is not None:
            p.setPen(QPen(QColor(255, 255, 255, 80), 1))
            for k in (1, 2):
                x = s.left() + s.width() * k / 3
                y = s.top() + s.height() * k / 3
                p.drawLine(QPointF(x, s.top()), QPointF(x, s.bottom()))
                p.drawLine(QPointF(s.left(), y), QPointF(s.right(), y))
        # frame, corner marks and edge bars: white over a dark halo, so they
        # show on dark photos and on white document pages alike
        halo = QColor(0, 0, 0, 140)
        p.setPen(QPen(halo, 3.5))
        p.drawRect(s)
        p.setPen(QPen(QColor(255, 255, 255, 235), 1.5))
        p.drawRect(s)
        L = min(20.0, s.width() / 3, s.height() / 3)
        E = min(18.0, s.width() / 4, s.height() / 4)
        mx, my = s.center().x(), s.center().y()
        marks = []
        for (cx, cy, sx, sy) in ((s.left(), s.top(), 1, 1), (s.right(), s.top(), -1, 1),
                                 (s.right(), s.bottom(), -1, -1), (s.left(), s.bottom(), 1, -1)):
            marks.append((QPointF(cx, cy), QPointF(cx + sx * L, cy)))
            marks.append((QPointF(cx, cy), QPointF(cx, cy + sy * L)))
        marks += [(QPointF(mx - E / 2, s.top()), QPointF(mx + E / 2, s.top())),
                  (QPointF(mx - E / 2, s.bottom()), QPointF(mx + E / 2, s.bottom())),
                  (QPointF(s.left(), my - E / 2), QPointF(s.left(), my + E / 2)),
                  (QPointF(s.right(), my - E / 2), QPointF(s.right(), my + E / 2))]
        for color, width in ((halo, 6.5), (QColor(255, 255, 255), 4.0)):
            pen = QPen(color, width)
            pen.setCapStyle(Qt.SquareCap)
            p.setPen(pen)
            for a, b in marks:
                p.drawLine(a, b)


class CropEditor(EditorWindow):
    """Image: accepted({"crop_box": (l, t, r, b)}).
    PDF: accepted({"crop_rel": (x0, y0, x1, y1), "crop_page": None | index})."""

    def __init__(self, path: str, password: str | None = None):
        self.path = path
        self.is_pdf = kind_of(path) == "pdf"
        super().__init__(os.path.basename(path),
                         f"Glisse les coins · {ENTER_KEY} pour rogner")
        self.password = password
        self.canvas = CropCanvas()
        self.canvas.changed.connect(self._sync)
        self.canvas.double_clicked.connect(self.validate)
        self.center.addWidget(self.canvas, 0, Qt.AlignCenter)

        self._preset_btns = []
        for label, a in PRESETS:
            b = self.chip(label)
            b.setChecked(a is None)
            b.clicked.connect(lambda _=False, asp=a, btn=b: self._preset(asp, btn))
            self.tools.addWidget(b)
            self._preset_btns.append(b)
        self.tools.addStretch(1)
        self.size_label = QLabel("")
        self.size_label.setObjectName("hint")
        self.size_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        # wide enough for "12000 × 12000 px": the popup does not change width
        # while the frame is dragged
        self.size_label.setMinimumWidth(
            self.size_label.fontMetrics().horizontalAdvance("00000 × 00000 px") + 6)
        self.tools.addWidget(self.size_label)

        self.page = 0
        self.page_count = 1
        if self.is_pdf:
            self.prev_btn = self.chip("‹", checkable=False)
            self.prev_btn.clicked.connect(lambda: self._goto(self.page - 1))
            self.page_label = QLabel("")
            self.page_label.setObjectName("hint")
            self.next_btn = self.chip("›", checkable=False)
            self.next_btn.clicked.connect(lambda: self._goto(self.page + 1))
            self.all_pages = QCheckBox("Toutes les pages")
            self.all_pages.setChecked(True)
            self.all_pages.setFocusPolicy(Qt.NoFocus)
            for w in (self.prev_btn, self.page_label, self.next_btn):
                self.bar.addWidget(w)
            self.bar.addSpacing(6)
            self.bar.addWidget(self.all_pages)
        else:
            reset = QPushButton("Image entière")
            reset.setObjectName("ghost")
            reset.setToolTip("Reprendre toute l'image")
            reset.setFocusPolicy(Qt.NoFocus)
            reset.clicked.connect(self.canvas.reset)
            self.bar.addWidget(reset)
        self.bar.addStretch(1)
        cancel = QPushButton("Annuler")
        cancel.setObjectName("ghost")
        cancel.setFocusPolicy(Qt.NoFocus)
        cancel.clicked.connect(self.cancel)
        self.ok_btn = QPushButton("Rogner")
        self.ok_btn.setObjectName("primary")
        self.ok_btn.setEnabled(False)
        self.ok_btn.setFocusPolicy(Qt.NoFocus)
        self.ok_btn.clicked.connect(self.validate)
        self.bar.addWidget(cancel)
        self.bar.addWidget(self.ok_btn)

        self._loader = Loader(self)
        self._loader.done.connect(self._loaded)
        self._token = 0
        self._keep_rel = None

    def start(self, anchor=None) -> None:
        if anchor is not None:
            self.anchor = anchor
        w, h, count, index = probe_size(self.path, 0, self.password)
        self.page_count, self.page = count, index
        if self.is_pdf:
            room_w, room_h = self.room(520, 580)
        elif h > 1.8 * w:            # a long screenshot: the screen's height
            room_w, room_h = self.room(600, 2000)
        elif w > 2.4 * h:            # a panorama: most of the screen's width
            room_w, room_h = self.room(1500, 470, screen_share=0.9)
        else:
            room_w, room_h = self.room()
        dpr = self.dpr()
        vw, vh = fit_view(w, h, room_w - 2 * MARGIN, room_h - 2 * MARGIN,
                          min_side=300, max_scale=1.0 / dpr if not self.is_pdf else 1.6)
        self.canvas.setFixedSize(QSize(vw + 2 * MARGIN, vh + 2 * MARGIN))
        if self.is_pdf:
            self._update_nav()
        self.open_at()
        self._load()

    def _target_px(self) -> tuple[int, int]:
        dpr = self.dpr()
        w = max(64, int((self.canvas.width() - 2 * MARGIN) * dpr))
        h = max(64, int((self.canvas.height() - 2 * MARGIN) * dpr))
        return w, h

    def _load(self) -> None:
        self._token += 1
        token = self._token
        w, h = self._target_px()
        page, path, pw = self.page, self.path, self.password
        if self.is_pdf:
            fn = lambda: (token, load_pdf_preview(path, page, w, h, pw))
        else:
            fn = lambda: (token, load_image_preview(path, w, h))
        self.canvas.image = None
        self.canvas.message = "Chargement…"
        self.canvas.update()
        self.ok_btn.setEnabled(False)
        self._loader.run(fn)

    def _loaded(self, res, err) -> None:
        if err:
            self.canvas.image = None
            self.canvas.message = err
            self.canvas.update()
            return
        token, payload = res
        if token != self._token:
            return  # an older page finished late
        if self.is_pdf:
            img, size, count, index = payload
            self.page_count, self.page = count, index
            self.canvas.set_image(img, size, keep_rel=self._keep_rel)
            self._update_nav()
        else:
            img, full = payload
            self.canvas.set_image(img, full)
        self.ok_btn.setEnabled(True)
        self._sync()

    def _update_nav(self) -> None:
        self.page_label.setText(f"{self.page + 1} / {self.page_count}")
        self.prev_btn.setEnabled(self.page > 0)
        self.next_btn.setEnabled(self.page < self.page_count - 1)
        many = self.page_count > 1
        for w in (self.prev_btn, self.page_label, self.next_btn, self.all_pages):
            w.setVisible(many)

    def _goto(self, index: int) -> None:
        if not (0 <= index < self.page_count) or index == self.page:
            return
        if self.canvas.image is not None:     # (while a page loads, keep the last frame)
            self._keep_rel = self.canvas.rel_box()
        self.page = index
        self._load()

    def _preset(self, aspect, btn) -> None:
        for b in self._preset_btns:
            b.setChecked(b is btn)
        if aspect == "orig":
            W, H = self.canvas.full
            aspect = W / H if H else None
        self.canvas.set_aspect(aspect)

    def _sync(self) -> None:
        if self.canvas.image is None:
            self.size_label.setText("")
            return
        if self.is_pdf:
            x0, y0, x1, y1 = self.canvas.rel_box()
            W, H = self.canvas.full
            cm = lambda pt: f"{pt / 72 * 2.54:.1f}".replace(".", ",")
            self.size_label.setText(f"{cm((x1 - x0) * W)} × {cm((y1 - y0) * H)} cm")
        else:
            l, t, r, b = self.canvas.pixel_box()
            self.size_label.setText(f"{r - l} × {b - t} px")

    def validate(self) -> None:
        if self.canvas.image is None:
            return
        if self.is_pdf:
            page = None if self.all_pages.isChecked() or self.page_count == 1 else self.page
            self.finish({"crop_rel": self.canvas.rel_box(), "crop_page": page})
        else:
            self.finish({"crop_box": self.canvas.pixel_box()})
