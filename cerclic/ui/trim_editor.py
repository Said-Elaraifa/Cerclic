"""Cut a video or a sound file, in a compact popup.

Video: the frame at the handle being moved, above a strip of thumbnails.
Sound: its waveform. Drag the two handles (or the passage between them),
or use the arrow keys (Maj for one second steps, Tab to switch handle).
Enter keeps the passage; the original file is never changed.
"""
from __future__ import annotations

import os

from PySide6.QtCore import QPointF, QRectF, QSize, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QFont, QImage, QPainter, QPen
from PySide6.QtWidgets import QLabel, QPushButton, QWidget

from ..paths import kind_of
from .editor_base import EditorWindow, Loader, fit_view
from .theme import ACCENT, FONT_FAMILY, MUTED, TEXT

STRIP_FRAMES = 8
HANDLE_W = 10


def fmt_time(t: float) -> str:
    """1:05,3 or 1:02:05,3"""
    t = max(0.0, float(t))
    tenths = int(round(t * 10))
    s, d = divmod(tenths, 10)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d},{d}" if h else f"{m}:{s:02d},{d}"


class TrimTrack(QWidget):
    """The timeline with its two handles."""
    changed = Signal(str)        # "start" or "end": the handle that moved
    released = Signal()

    def __init__(self, color: str):
        super().__init__()
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.duration = 0.0
        self.start = 0.0
        self.end = 0.0
        self.active = "start"
        self.color = QColor(color)
        self.strip: list[QImage | None] = []
        self.wave: QImage | None = None
        self.message = "Chargement…"
        self._drag = None
        self._grab_dt = 0.0

    def set_duration(self, d: float) -> None:
        self.duration = max(0.0, d)
        self.start, self.end = 0.0, self.duration
        self.message = "" if self.duration > 0 else "Durée inconnue"
        self.update()

    # -- mapping ---------------------------------------------------------------------
    def _lane(self) -> QRectF:
        return QRectF(HANDLE_W, 6, max(1.0, self.width() - 2 * HANDLE_W), self.height() - 12)

    def x_of(self, t: float) -> float:
        lane = self._lane()
        return lane.left() + (t / self.duration) * lane.width() if self.duration else lane.left()

    def t_of(self, x: float) -> float:
        lane = self._lane()
        if not self.duration:
            return 0.0
        return min(self.duration, max(0.0, (x - lane.left()) / lane.width() * self.duration))

    @property
    def min_len(self) -> float:
        return min(0.2, self.duration)

    def set_range(self, start: float, end: float, which: str = "start") -> None:
        d = self.duration
        start = min(max(0.0, start), d)
        end = min(max(0.0, end), d)
        if end - start < self.min_len:
            if which == "start":
                start = max(0.0, end - self.min_len)
            else:
                end = min(d, start + self.min_len)
        self.start, self.end = start, end
        self.update()
        self.changed.emit(which)

    def nudge(self, dt: float) -> None:
        if self.active == "start":
            self.set_range(self.start + dt, self.end, "start")
        else:
            self.set_range(self.start, self.end + dt, "end")

    # -- mouse -------------------------------------------------------------------------
    def mousePressEvent(self, e):
        if not self.duration or e.button() != Qt.LeftButton:
            return
        x = e.position().x()
        xs, xe = self.x_of(self.start), self.x_of(self.end)
        if abs(x - xs) <= HANDLE_W + 2 and abs(x - xs) <= abs(x - xe):
            self._drag = "start"
        elif abs(x - xe) <= HANDLE_W + 2:
            self._drag = "end"
        elif xs < x < xe:
            self._drag = "move"
            self._grab_dt = self.t_of(x) - self.start
        else:                                   # click outside: nearest handle jumps
            self._drag = "start" if abs(x - xs) < abs(x - xe) else "end"
            self._apply(x)
        if self._drag in ("start", "end"):
            self.active = self._drag
        self.update()

    def mouseMoveEvent(self, e):
        x = e.position().x()
        if self._drag is None:
            if self.duration:
                xs, xe = self.x_of(self.start), self.x_of(self.end)
                near = min(abs(x - xs), abs(x - xe)) <= HANDLE_W + 2
                self.setCursor(Qt.SizeHorCursor if near else
                               Qt.OpenHandCursor if xs < x < xe else Qt.PointingHandCursor)
            return
        self._apply(x)

    def _apply(self, x: float) -> None:
        t = self.t_of(x)
        if self._drag == "start":
            self.set_range(min(t, self.end - self.min_len), self.end, "start")
        elif self._drag == "end":
            self.set_range(self.start, max(t, self.start + self.min_len), "end")
        elif self._drag == "move":
            length = self.end - self.start
            s = min(max(0.0, t - self._grab_dt), self.duration - length)
            self.start, self.end = s, s + length
            self.update()
            self.changed.emit(self.active)

    def mouseReleaseEvent(self, e):
        if self._drag is not None:
            self._drag = None
            self.released.emit()

    def keyPressEvent(self, e):
        step = 1.0 if e.modifiers() & Qt.ShiftModifier else 0.1
        if e.key() == Qt.Key_Left:
            self.nudge(-step)
        elif e.key() == Qt.Key_Right:
            self.nudge(step)
        elif e.key() == Qt.Key_Tab:
            self.active = "end" if self.active == "start" else "start"
            self.changed.emit(self.active)
            self.update()
        else:
            super().keyPressEvent(e)

    def focusNextPrevChild(self, _next: bool) -> bool:
        return False                            # Tab switches handle

    # -- painting ------------------------------------------------------------------------
    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.SmoothPixmapTransform, True)
        lane = self._lane()
        p.setPen(Qt.NoPen)
        p.setBrush(QColor("#11131A"))
        p.drawRoundedRect(lane, 6, 6)
        if self.strip:
            n = len(self.strip)
            w = lane.width() / n
            for i, img in enumerate(self.strip):
                if img is None or img.isNull():
                    continue
                cell = QRectF(lane.left() + i * w, lane.top(), w, lane.height())
                s = max(cell.width() / img.width(), cell.height() / img.height())
                src_w, src_h = cell.width() / s, cell.height() / s
                src = QRectF((img.width() - src_w) / 2, (img.height() - src_h) / 2,
                             src_w, src_h)
                p.drawImage(cell, img, src)
        elif self.wave is not None and not self.wave.isNull():
            p.drawImage(lane, self.wave)
        if not self.duration:
            p.setPen(QColor(MUTED))
            f = QFont(FONT_FAMILY)
            f.setPixelSize(12)
            p.setFont(f)
            p.drawText(lane, Qt.AlignCenter, self.message)
            return
        xs, xe = self.x_of(self.start), self.x_of(self.end)
        shade = QColor(8, 9, 12, 185)
        p.setBrush(shade)
        p.drawRect(QRectF(lane.left(), lane.top(), xs - lane.left(), lane.height()))
        p.drawRect(QRectF(xe, lane.top(), lane.right() - xe, lane.height()))
        p.setBrush(Qt.NoBrush)
        p.setPen(QPen(self.color, 2.5))
        p.drawRect(QRectF(xs, lane.top() + 1, xe - xs, lane.height() - 2))
        for which, x in (("start", xs), ("end", xe)):
            r = QRectF(x - HANDLE_W / 2, 0, HANDLE_W, self.height())
            p.setPen(Qt.NoPen)
            p.setBrush(self.color.lighter(125) if which == self.active and self.hasFocus()
                       else self.color)
            p.drawRoundedRect(r, 4, 4)
            p.setPen(QPen(QColor(255, 255, 255, 220), 1.5))
            p.drawLine(QPointF(x - 1.5, r.center().y() - 7), QPointF(x - 1.5, r.center().y() + 7))
            p.drawLine(QPointF(x + 1.5, r.center().y() - 7), QPointF(x + 1.5, r.center().y() + 7))


class _Frame(QWidget):
    """The video frame shown above the track."""

    def __init__(self):
        super().__init__()
        self.image: QImage | None = None
        self.caption = ""

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.SmoothPixmapTransform, True)
        p.setRenderHint(QPainter.Antialiasing, True)
        r = QRectF(self.rect())
        p.setPen(Qt.NoPen)
        p.setBrush(QColor("#0B0C10"))
        p.drawRoundedRect(r, 8, 8)
        if self.image is not None and not self.image.isNull():
            s = min(r.width() / self.image.width(), r.height() / self.image.height())
            w, h = self.image.width() * s, self.image.height() * s
            p.drawImage(QRectF(r.center().x() - w / 2, r.center().y() - h / 2, w, h),
                        self.image)
        if self.caption:
            f = QFont(FONT_FAMILY)
            f.setPixelSize(12)
            f.setBold(True)
            p.setFont(f)
            tw = p.fontMetrics().horizontalAdvance(self.caption) + 16
            box = QRectF(r.left() + 8, r.bottom() - 30, tw, 22)
            p.setBrush(QColor(0, 0, 0, 150))
            p.drawRoundedRect(box, 6, 6)
            p.setPen(QColor(TEXT))
            p.drawText(box, Qt.AlignCenter, self.caption)


class TrimEditor(EditorWindow):
    """accepted({"trim_start": seconds, "trim_end": seconds})"""

    def __init__(self, path: str):
        self.path = path
        self.is_video = kind_of(path) == "video"
        super().__init__(os.path.basename(path),
                         "Tire les poignées · Entrée pour raccourcir")
        color = "#17B890" if self.is_video else "#A66BFF"
        self.frame = _Frame() if self.is_video else None
        if self.frame is not None:
            self.center.addWidget(self.frame, 0, Qt.AlignCenter)
        self.track = TrimTrack(color)
        self.track.changed.connect(self._changed)
        self.track.released.connect(self._request_frame)
        self.center.addWidget(self.track)

        self.times = QLabel("")
        self.times.setObjectName("hint")
        self.tools.addWidget(self.times)
        self.tools.addStretch(1)
        self.length_label = QLabel("")
        self.length_label.setStyleSheet(f"color:{TEXT};font-size:12px;font-weight:700;")
        self.tools.addWidget(self.length_label)

        self.bar.addStretch(1)
        cancel = QPushButton("Annuler")
        cancel.setObjectName("ghost")
        cancel.setFocusPolicy(Qt.NoFocus)
        cancel.clicked.connect(self.cancel)
        self.ok = QPushButton("Raccourcir")
        self.ok.setObjectName("primary")
        self.ok.setEnabled(False)
        self.ok.setFocusPolicy(Qt.NoFocus)
        self.ok.clicked.connect(self.validate)
        self.bar.addWidget(cancel)
        self.bar.addWidget(self.ok)

        self._info = Loader(self)
        self._info.done.connect(self._probed)
        self._strip = Loader(self)
        self._strip.progress.connect(self._strip_part)
        self._wave = Loader(self)
        self._wave.done.connect(self._wave_ready)
        self._frames = Loader(self)
        self._frames.done.connect(self._frame_ready)
        self._frame_busy = False
        self._frame_want: float | None = None
        self._frame_timer = QTimer(self, singleShot=True, interval=90)
        self._frame_timer.timeout.connect(self._request_frame)

    # -- opening ------------------------------------------------------------------------
    def start(self, anchor=None) -> None:
        if anchor is not None:
            self.anchor = anchor
        room_w, room_h = self.room(560, 420)
        width = max(420, min(room_w, 560))
        if self.frame is not None:
            self.frame.setFixedSize(QSize(width, int(width * 9 / 16)))
        self.track.setFixedSize(QSize(width, 64 if self.is_video else 92))
        self.open_at()
        self.track.setFocus()
        from ..actions import video as _video
        path = self.path
        self._info.run(lambda: _video.probe(path))

    def _probed(self, info, err) -> None:
        if err or info is None or info.duration <= 0:
            self.track.message = err or "Durée illisible : fichier endommagé ?"
            self.track.update()
            return
        self.track.set_duration(info.duration)
        self.ok.setEnabled(True)
        self._changed("start")
        from ..actions import video as _video
        path = self.path
        if self.frame is not None and info.width and info.height:
            room_w, room_h = self.room(560, 420)
            width = self.track.width()
            fw, fh = fit_view(info.width, info.height, width, max(160, room_h - 120),
                              min_side=160, max_scale=10)
            self.frame.setFixedSize(QSize(fw, fh))
            self.refit()
        dpr = self.devicePixelRatioF() or 1.0
        if self.is_video:
            h = int(52 * dpr)
            dur = info.duration
            self.track.strip = [None] * STRIP_FRAMES

            def strip(report, stop):
                for i in range(STRIP_FRAMES):
                    if stop():
                        return
                    t = dur * (i + 0.5) / STRIP_FRAMES
                    try:
                        data = _video.frame_png(path, t, int(h * 1.8), h)
                    except Exception:
                        continue
                    report((i, QImage.fromData(data, "PNG")))
            self._strip.run_reporting(strip)
            self._frame_want = 0.0
            self._request_frame()
        else:
            w, h = int(self.track.width() * dpr), int(80 * dpr)
            self._wave.run(lambda: _video.waveform_png(path, w, h, color="#B79BFF"))

    def _strip_part(self, payload) -> None:
        i, img = payload
        if 0 <= i < len(self.track.strip):
            self.track.strip[i] = img
            self.track.update()

    def _wave_ready(self, data, err) -> None:
        if data:
            self.track.wave = QImage.fromData(data, "PNG")
            self.track.update()

    # -- frames ----------------------------------------------------------------------------
    def _changed(self, which: str) -> None:
        t = self.track
        self.times.setText(f"{fmt_time(t.start)}  →  {fmt_time(t.end)}")
        self.length_label.setText(f"Durée {fmt_time(t.end - t.start)}")
        if self.frame is not None:
            self._frame_want = t.start if which == "start" else t.end
            self.frame.caption = ("Début " if which == "start" else "Fin ") + \
                fmt_time(self._frame_want)
            self.frame.update()
            self._frame_timer.start()

    def _request_frame(self) -> None:
        if self.frame is None or self._frame_want is None or self._frame_busy:
            return
        t, self._frame_want = self._frame_want, None
        self._frame_busy = True
        dpr = self.devicePixelRatioF() or 1.0
        w, h = int(self.frame.width() * dpr), int(self.frame.height() * dpr)
        if t >= self.track.duration - 0.05:          # the very end has no frame
            t = max(0.0, self.track.duration - 0.1)
        from ..actions import video as _video
        path = self.path
        self._frames.run(lambda: _video.frame_png(path, t, w, h))

    def _frame_ready(self, data, err) -> None:
        self._frame_busy = False
        if data:
            img = QImage.fromData(data, "PNG")
            if not img.isNull():
                self.frame.image = img
                self.frame.update()
        if self._frame_want is not None:
            self._request_frame()

    # -- result ---------------------------------------------------------------------------------
    def validate(self) -> None:
        t = self.track
        if t.duration > 0:
            self.finish({"trim_start": round(t.start, 3), "trim_end": round(t.end, 3)})
