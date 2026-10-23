"""« Réseaux » popup: a picture or a video in a social network format.

It shows the result itself, in the shape of the chosen format (square,
story...). « Remplir »: the picture covers the frame; drag it to choose the
part that stays, the mouse wheel (or a pinch on a trackpad) zooms, a
double-click recentres. What gets cut stays visible around the frame, veiled.
« Fond flou », « Fond blanc », « Fond noir »: the whole picture, nothing cut.
With several files, ‹ › go from one to the next, each keeping its own
framing; the format and the background apply to all of them.
"""
from __future__ import annotations

import io
import math
import os

from PySide6.QtCore import QEvent, QPointF, QRectF, QSize, Qt, Signal
from PySide6.QtGui import QColor, QIcon, QPainter, QPainterPath, QPen, QPixmap
from PySide6.QtWidgets import QLabel, QPushButton, QWidget

from ..actions import social
from ..paths import kind_of
from ..system import ENTER_KEY
from .editor_base import EditorWindow, Loader, _elide, qimage_from_pil
from .theme import MUTED, WARN, font

MARGIN = 14                              # px around the frame: what gets cut shows there
VEIL = QColor(240, 243, 249, 205)        # over what gets cut
ZOOM_STEP = 1.15
MODES = (
    ("fill", "Remplir", "L'image couvre tout le cadre, ce qui dépasse est coupé.\n"
                        "Glisse-la pour choisir la partie gardée, molette pour zoomer."),
    ("blur", "Fond flou", "Toute l'image, rien n'est coupé.\n"
                          "Autour : la même image, floutée."),
    ("white", "Fond blanc", "Toute l'image, rien n'est coupé.\nAutour : du blanc."),
    ("black", "Fond noir", "Toute l'image, rien n'est coupé.\nAutour : du noir."),
)


PREVIEW_PIXELS = 24_000_000       # at most, for a panorama shown whole


def preview_box(W: float, H: float, short_px: int) -> tuple[int, int]:
    """Size to decode the original at for the popup: its short side about
    `short_px` (sharp once zoomed in, and a long panorama keeps its height),
    never more than the original nor than PREVIEW_PIXELS."""
    W, H = max(1.0, float(W)), max(1.0, float(H))
    s = min(1.0, short_px / min(W, H))
    if W * H * s * s > PREVIEW_PIXELS:
        s = math.sqrt(PREVIEW_PIXELS / (W * H))
    return max(1, math.ceil(W * s)), max(1, math.ceil(H * s))


def load_preview(path: str, short_px: int, should_stop=None):
    """(preview as a Pillow image in screen colours, size of the original as
    seen) of a picture or of a video (one of its frames)."""
    if kind_of(path) == "video":
        from PIL import Image
        from ..actions import video
        from ..errors import Cancelled
        info = video.probe(path, should_stop=should_stop)
        video._need_video(info)
        W, H = info.display_size
        bw, bh = preview_box(W, H, short_px) if W > 0 and H > 0 else (1920, 1920)
        try:
            data = video.frame_png(path, info.duration / 3 if info.duration > 0 else 0.0,
                                   bw, bh, should_stop=should_stop)
        except Cancelled:
            raise
        except Exception:                        # a very short clip: its first picture
            data = video.frame_png(path, 0.0, bw, bh, should_stop=should_stop)
        im = Image.open(io.BytesIO(data))
        im.load()
        im = im.convert("RGB")
        return im, ((W, H) if W > 0 and H > 0 else im.size)
    from ..actions.images import oriented_size
    from .crop_editor import pil_preview
    try:
        W, H = oriented_size(path)
    except Exception:
        W, H = 4000, 4000                        # (read again, and refused, just below)
    im, full = pil_preview(path, *preview_box(W, H, short_px))
    return social.to_screen_rgb(im, im.info.get("icc_profile")), full


def shape_icon(f: social.Format, dpr: float = 1.0) -> QIcon:
    """The format's shape, drawn small: grey, white once chosen."""
    icon = QIcon()
    for state, color in ((QIcon.Off, QColor(MUTED)), (QIcon.On, QColor("white"))):
        pm = QPixmap(round(16 * dpr), round(16 * dpr))
        pm.setDevicePixelRatio(dpr)
        pm.fill(Qt.transparent)
        p = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing, True)
        a = f.aspect
        w, h = (13.0, 13.0 / a) if a >= 1 else (13.0 * a, 13.0)
        p.setPen(QPen(color, 1.4))
        p.drawRoundedRect(QRectF((16 - w) / 2 + 0.7, (16 - h) / 2 + 0.7, w - 1.4, h - 1.4),
                          1.6, 1.6)
        p.end()
        for mode in (QIcon.Normal, QIcon.Active):
            icon.addPixmap(pm, mode, state)
    return icon


class SocialCanvas(QWidget):
    """The result as it will look, at the centre of the popup."""
    changed = Signal()

    def __init__(self, fmt: social.Format, mode: str):
        super().__init__()
        self.setMouseTracking(True)
        self.fmt = fmt
        self.mode = mode
        self.pil = None              # the preview as Pillow (for the blurred background)
        self.image = None            # the same, to draw
        self.full = (1.0, 1.0)       # size of the original, as seen
        self.center = (0.5, 0.5)     # what the user asked for (kept inside when shown)
        self.zoom = 1.0
        self.message = "Chargement…"
        self._blur: dict = {}
        self._scaled = (None, None)  # (size, the preview at that size): dragging only moves it
        self._press = None           # (mouse position, centre) while dragging

    # -- content ----------------------------------------------------------------------------
    def set_picture(self, pil, image, full, center=(0.5, 0.5), zoom: float = 1.0) -> None:
        """`pil` and `image`: the preview, as Pillow and as QImage (made off the
        interface thread); `full`: the original's size as seen."""
        self.pil = pil
        self.image = image
        self.full = (max(1.0, float(full[0])), max(1.0, float(full[1])))
        self._blur = {}
        self._scaled = (None, None)
        self.message = ""
        self._press = None
        self.center = (float(center[0]), float(center[1]))
        self.zoom = min(social.MAX_ZOOM, max(1.0, float(zoom)))
        self._cursor()
        self.update()
        self.changed.emit()

    def clear(self, message: str) -> None:
        self.pil = self.image = None
        self._scaled = (None, None)
        self.message = message
        self._press = None
        self._cursor()
        self.update()
        self.changed.emit()

    def set_format(self, fmt: social.Format) -> None:
        self.fmt = fmt
        self.update()
        self.changed.emit()

    def set_mode(self, mode: str) -> None:
        self.mode = mode
        self._cursor()
        self.update()
        self.changed.emit()

    def recentre(self) -> None:
        self.center, self.zoom = (0.5, 0.5), 1.0
        self.update()
        self.changed.emit()

    # -- geometry ---------------------------------------------------------------------------
    def frame_rect(self) -> QRectF:
        """The result's shape, as large as the canvas allows."""
        aw = max(1.0, self.width() - 2 * MARGIN)
        ah = max(1.0, self.height() - 2 * MARGIN)
        a = self.fmt.aspect
        w, h = aw, aw / a
        if h > ah:
            h, w = ah, ah * a
        return QRectF((self.width() - w) / 2, (self.height() - h) / 2, w, h)

    def box(self) -> tuple[float, float, float, float]:
        """The part of the original kept (Remplir), in its pixels."""
        W, H = self.full
        return social.place_box(W, H, self.fmt.aspect, self.center, self.zoom)

    def shown_center(self) -> tuple[float, float]:
        x0, y0, x1, y1 = self.box()
        W, H = self.full
        return ((x0 + x1) / 2 / W, (y0 + y1) / 2 / H)

    def _scale(self) -> float:
        """Screen pixels per pixel of the original (Remplir)."""
        x0, _, x1, _ = self.box()
        return self.frame_rect().width() / max(1e-9, x1 - x0)

    def picture_rect(self) -> QRectF:
        """Where the whole picture is drawn (Remplir): beyond the frame too."""
        F = self.frame_rect()
        x0, y0, _, _ = self.box()
        k = self._scale()
        W, H = self.full
        return QRectF(F.left() - x0 * k, F.top() - y0 * k, W * k, H * k)

    def fit_rect(self) -> QRectF:
        """Where the whole picture sits inside the frame (the other modes)."""
        F = self.frame_rect()
        W, H = self.full
        tw, th = social.fit_size(W, H, self.fmt)
        s = F.width() / self.fmt.width
        w, h = tw * s, th * s
        return QRectF(F.center().x() - w / 2, F.center().y() - h / 2, w, h)

    # -- moving and zooming -----------------------------------------------------------------------
    def _movable(self) -> bool:
        return self.image is not None and self.mode == "fill"

    def _cursor(self) -> None:
        if self._movable():
            self.setCursor(Qt.ClosedHandCursor if self._press else Qt.OpenHandCursor)
        else:
            self.unsetCursor()

    def move_by(self, dx: float, dy: float) -> None:
        """Slide the picture by dx, dy screen pixels (from where it is shown)."""
        if not self._movable():
            return
        k = self._scale()
        W, H = self.full
        cx, cy = self.shown_center()
        self.center = (cx - dx / k / W, cy - dy / k / H)
        self.center = self.shown_center()
        self.update()
        self.changed.emit()

    def zoom_by(self, factor: float, at: QPointF | None = None) -> None:
        """Zoom in (factor > 1) or out, the point under `at` staying put."""
        if not self._movable():
            return
        F = self.frame_rect()
        at = QPointF(at) if at is not None else F.center()
        W, H = self.full
        x0, y0, x1, y1 = self.box()
        k = self._scale()
        sx = x0 + (at.x() - F.left()) / k
        sy = y0 + (at.y() - F.top()) / k
        zoom = min(social.MAX_ZOOM, max(1.0, self.zoom * factor))
        if abs(zoom - self.zoom) < 1e-9:
            return
        bw, bh = (x1 - x0) * self.zoom / zoom, (y1 - y0) * self.zoom / zoom
        k2 = F.width() / bw
        nx0 = sx - (at.x() - F.left()) / k2
        ny0 = sy - (at.y() - F.top()) / k2
        self.zoom = zoom
        self.center = ((nx0 + bw / 2) / W, (ny0 + bh / 2) / H)
        self.center = self.shown_center()
        self.update()
        self.changed.emit()

    def mousePressEvent(self, e):
        if not self._movable() or e.button() != Qt.LeftButton:
            return
        self.center = self.shown_center()
        self._press = (e.position(), self.center)
        self._cursor()
        self.update()

    def mouseMoveEvent(self, e):
        if self._press is None:
            return
        pos0, (cx, cy) = self._press
        d = e.position() - pos0
        k = self._scale()
        W, H = self.full
        self.center = (cx - d.x() / k / W, cy - d.y() / k / H)
        self.update()
        self.changed.emit()

    def mouseReleaseEvent(self, e):
        if self._press is not None:
            self._press = None
            self.center = self.shown_center()
            self._cursor()
            self.update()
            self.changed.emit()

    def mouseDoubleClickEvent(self, e):
        if self._movable():
            self.recentre()

    def wheelEvent(self, e):
        steps = e.angleDelta().y() / 120.0
        if not self._movable() or not steps:
            e.ignore()
            return
        self.zoom_by(ZOOM_STEP ** steps, e.position())
        e.accept()

    def event(self, e):
        # a pinch on a Mac trackpad
        if e.type() == QEvent.NativeGesture and self._movable():
            if e.gestureType() == Qt.ZoomNativeGesture:
                self.zoom_by(1.0 + e.value(), e.position())
                return True
        return super().event(e)

    # -- painting -------------------------------------------------------------------------------
    def _blurred(self):
        q = self._blur.get(self.fmt.key)
        if q is None and self.pil is not None:
            q = qimage_from_pil(social.blurred_background(self.pil, self.fmt, final=False))
            self._blur[self.fmt.key] = q
        return q

    def _draw_picture(self, p: QPainter, R: QRectF) -> None:
        """The preview in R, smoothly reduced once per size (moving it then
        costs nothing); zoomed in past its own pixels, only what shows."""
        dpr = self.devicePixelRatioF() or 1.0
        w, h = max(1, round(R.width() * dpr)), max(1, round(R.height() * dpr))
        if w <= self.image.width() * 1.02:
            if self._scaled[0] != (w, h):
                img = self.image.scaled(w, h, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                img.setDevicePixelRatio(dpr)
                self._scaled = ((w, h), img)
            p.drawImage(R.topLeft(), self._scaled[1])
            return
        vis = R.intersected(QRectF(self.rect()))
        if vis.isEmpty():
            return
        sx, sy = self.image.width() / R.width(), self.image.height() / R.height()
        p.drawImage(vis, self.image, QRectF((vis.left() - R.left()) * sx,
                                            (vis.top() - R.top()) * sy,
                                            vis.width() * sx, vis.height() * sy))

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.SmoothPixmapTransform, True)
        F = self.frame_rect()
        if self.image is None:
            p.setPen(QPen(QColor(MUTED), 1.2, Qt.DashLine))
            p.drawRoundedRect(F.adjusted(0.6, 0.6, -0.6, -0.6), 3, 3)
            p.setPen(QColor(MUTED))
            p.setFont(font(10))
            p.drawText(F.adjusted(10, 10, -10, -10), Qt.AlignCenter | Qt.TextWordWrap,
                       self.message)
            return
        if self.mode == "fill":
            R = self.picture_rect()
            p.fillRect(F, QColor("white"))        # under a see-through picture, as in the result
            self._draw_picture(p, R)
            veil = QPainterPath()
            veil.addRect(R.intersected(QRectF(self.rect())))
            kept = QPainterPath()
            kept.addRect(F)
            p.fillPath(veil.subtracted(kept), VEIL)
            if self._press is not None:           # thirds, while placing
                p.setPen(QPen(QColor(255, 255, 255, 120), 1))
                for k in (1, 2):
                    x = F.left() + F.width() * k / 3
                    y = F.top() + F.height() * k / 3
                    p.drawLine(QPointF(x, F.top()), QPointF(x, F.bottom()))
                    p.drawLine(QPointF(F.left(), y), QPointF(F.right(), y))
        else:
            p.save()
            p.setClipRect(F)
            if self.mode == "blur":
                small = self._blurred()
                if small is not None:
                    p.drawImage(F, small)
            else:
                p.fillRect(F, QColor("white" if self.mode == "white" else "black"))
            self._draw_picture(p, self.fit_rect())
            p.restore()
        p.setBrush(Qt.NoBrush)
        p.setPen(QPen(QColor(16, 24, 40, 110), 3))
        p.drawRect(F)
        p.setPen(QPen(QColor(255, 255, 255, 235), 1.2))
        p.drawRect(F)


class SocialEditor(EditorWindow):
    """accepted({"social": format key, "social_mode": "fill" | "blur" | "white" |
    "black", "social_frames": {path: (centre x, centre y, zoom)}})"""

    def __init__(self, paths, fmt_key: str | None = None, mode: str | None = None):
        self.paths = list(paths)
        self.is_video = kind_of(self.paths[0]) == "video"
        if self.is_video:
            fmt0, mode0 = social.BY_KEY["story"], "blur"
        else:
            fmt0, mode0 = social.BY_KEY["portrait"], "fill"
        fmt = social.BY_KEY.get(fmt_key or "", fmt0)
        mode = mode if mode in social.MODES else mode0
        super().__init__(os.path.basename(self.paths[0]), "")
        self.index = 0
        self.frames: dict[str, tuple] = {}
        self.canvas = SocialCanvas(fmt, mode)
        self.canvas.changed.connect(self._sync)
        self.center.addWidget(self.canvas, 0, Qt.AlignCenter)
        self.info = QLabel("")
        self.info.setObjectName("hint")
        self.info.setAlignment(Qt.AlignCenter)
        self.info.setWordWrap(True)
        self.info.setTextFormat(Qt.RichText)
        self.center.addWidget(self.info, 0, Qt.AlignCenter)

        dpr = self.dpr()
        self.format_buttons: dict[str, QPushButton] = {}
        for f in social.FORMATS:
            b = self.chip(f"{f.label} {f.ratio}")
            b.setIcon(shape_icon(f, dpr))
            b.setIconSize(QSize(16, 16))
            b.setToolTip(f"{f.where}\n{f.size_text}")
            b.setChecked(f is fmt)
            b.clicked.connect(lambda _=False, ff=f: self.set_format(ff))
            self.tools.addWidget(b)
            self.format_buttons[f.key] = b

        self.mode_buttons: dict[str, QPushButton] = {}
        for key, label, tip in MODES:
            b = self.chip(label)
            b.setToolTip(tip)
            b.setChecked(key == mode)
            b.clicked.connect(lambda _=False, m=key: self.set_mode(m))
            self.bar.addWidget(b)
            self.mode_buttons[key] = b
        self.bar.addStretch(1)
        self.prev_btn = self.chip("‹", checkable=False)
        self.prev_btn.setToolTip("Fichier précédent")
        self.prev_btn.clicked.connect(lambda: self.goto(self.index - 1))
        self.count_label = QLabel("")
        self.count_label.setObjectName("hint")
        self.next_btn = self.chip("›", checkable=False)
        self.next_btn.setToolTip("Fichier suivant")
        self.next_btn.clicked.connect(lambda: self.goto(self.index + 1))
        for w in (self.prev_btn, self.count_label, self.next_btn):
            self.bar.addWidget(w)
            w.setVisible(len(self.paths) > 1)
        self.bar.addSpacing(4)
        cancel = QPushButton("Annuler")
        cancel.setObjectName("ghost")
        cancel.setFocusPolicy(Qt.NoFocus)
        cancel.clicked.connect(self.cancel)
        self.ok_btn = QPushButton("Créer")
        self.ok_btn.setObjectName("primary")
        self.ok_btn.setEnabled(False)
        self.ok_btn.setFocusPolicy(Qt.NoFocus)
        self.ok_btn.clicked.connect(self.validate)
        self.bar.addWidget(cancel)
        self.bar.addWidget(self.ok_btn)

        self._loader = Loader(self)
        self._loader.done.connect(self._loaded)
        self._token = 0
        self._update_nav()
        self._sync()

    # -- opening ----------------------------------------------------------------------------------
    def start(self, anchor=None) -> None:
        if anchor is not None:
            self.anchor = anchor
        room_w, room_h = self.room(680, 430)
        self.ensurePolished()                       # (the buttons' real size, styled)
        for row in (self.tools, self.bar):
            row.invalidate()
        rows = max(self.tools.sizeHint().width(), self.bar.sizeHint().width())
        w = max(360, min(room_w, max(rows, 480)))
        h = max(220, min(room_h, 420))
        self.canvas.setFixedSize(QSize(w, h))
        self.info.setFixedWidth(w)
        self.info.setMinimumHeight(2 * self.info.fontMetrics().lineSpacing() + 4)
        self.open_at()
        self._load()

    def _load(self) -> None:
        self._token += 1
        token = self._token
        path = self.paths[self.index]
        # sharp in the frame even zoomed in a little: twice the canvas, on its long side
        short_px = int(2 * max(self.canvas.width(), self.canvas.height()) * self.dpr())
        stop = self._loader.stop_event.is_set       # closing the popup stops ffmpeg

        def work():
            try:
                pil, full = load_preview(path, short_px, stop)
                return token, (pil, qimage_from_pil(pil), full), ""
            except Exception as exc:  # shown in the popup
                from ..engine import friendly_error
                from ..errors import Cancelled, UserError
                if not isinstance(exc, (Cancelled, UserError)):
                    from ..log import log_exception
                    log_exception("aperçu réseaux")
                return token, None, friendly_error(exc)

        self.canvas.clear("Chargement…")
        self._loader.run(work)

    def _loaded(self, res, err) -> None:
        if res is None:
            return
        token, payload, error = res
        if token != self._token:
            return                          # another file was asked for since
        if error:
            self.canvas.clear(error)
        else:
            pil, image, full = payload
            center, zoom = self.frames.get(self.paths[self.index], ((0.5, 0.5), 1.0))
            self.canvas.set_picture(pil, image, full, center, zoom)
        self.ok_btn.setEnabled(self.canvas.image is not None or len(self.paths) > 1)

    # -- choices ------------------------------------------------------------------------------------
    def set_format(self, f: social.Format) -> None:
        for key, b in self.format_buttons.items():
            b.setChecked(key == f.key)
        self.canvas.set_format(f)

    def set_mode(self, mode: str) -> None:
        for key, b in self.mode_buttons.items():
            b.setChecked(key == mode)
        self.canvas.set_mode(mode)

    def goto(self, index: int) -> None:
        if not 0 <= index < len(self.paths) or index == self.index:
            return
        self._remember()
        self.index = index
        name = os.path.basename(self.paths[index])
        self.title_label.setText(_elide(name, 38))
        self.title_label.setToolTip(name)
        self._update_nav()
        self._load()

    def _remember(self) -> None:
        if self.canvas.image is not None:
            self.frames[self.paths[self.index]] = (self.canvas.shown_center(),
                                                   self.canvas.zoom)

    def _update_nav(self) -> None:
        n = len(self.paths)
        self.count_label.setText(f"{self.index + 1} / {n}")
        self.prev_btn.setEnabled(self.index > 0)
        self.next_btn.setEnabled(self.index < n - 1)

    def _sync(self) -> None:
        c = self.canvas
        f = c.fmt
        if c.mode == "fill":
            self.hint_label.setText(f"Glisse et zoome · {ENTER_KEY} pour créer")
        else:
            self.hint_label.setText(f"Rien n'est coupé · {ENTER_KEY} pour créer")
        text = f"<b>{f.size_text}</b> · {f.where}"
        if c.image is not None and social.enlarged(*c.full, f, c.mode, c.zoom):
            if c.mode == "fill":
                what = "La partie gardée est plus petite"
            else:
                what = "La vidéo est plus petite" if self.is_video else "L'image est plus petite"
            text += (f"<br><span style='color:{WARN}'>{what} que le format : "
                     "agrandie, elle sera un peu moins nette.</span>")
        self.info.setText(text)

    # -- keyboard -------------------------------------------------------------------------------------
    def keyPressEvent(self, e):
        k = e.key()
        step = 24 if e.modifiers() & Qt.ShiftModifier else 6
        moves = {Qt.Key_Left: (-step, 0), Qt.Key_Right: (step, 0),     # the picture moves
                 Qt.Key_Up: (0, -step), Qt.Key_Down: (0, step)}
        if k in (Qt.Key_Plus, Qt.Key_Equal):
            self.canvas.zoom_by(ZOOM_STEP)
        elif k in (Qt.Key_Minus, Qt.Key_Underscore):
            self.canvas.zoom_by(1 / ZOOM_STEP)
        elif k in moves:
            self.canvas.move_by(*moves[k])
        elif k == Qt.Key_PageDown:
            self.goto(self.index + 1)
        elif k == Qt.Key_PageUp:
            self.goto(self.index - 1)
        else:
            super().keyPressEvent(e)

    # -- result ------------------------------------------------------------------------------------------
    def validate(self) -> None:
        if not self.ok_btn.isEnabled():
            return
        self._remember()
        frames = {p: (c[0], c[1], z) for p, (c, z) in self.frames.items()}
        self.finish({"social": self.canvas.fmt.key, "social_mode": self.canvas.mode,
                     "social_frames": frames})
