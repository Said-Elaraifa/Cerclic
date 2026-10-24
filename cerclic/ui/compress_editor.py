"""« Compresser » popup: how much, and the size it gives, before anything is
written.

Pictures: a « Qualité » slider. As it moves, the very bytes the action will
write are made in the background: the size shown is the size you get, and the
picture shown is the result (hover it: a loupe shows its pixels at 100 %).
PDF, videos, sounds: four strengths, « Légère » to « Maximale », each with its
size, worked out in the background: a PDF and a short video are compressed for
real (that result is then used as is, nothing is done twice), a longer video
through a few samples, a sound from its length.
Several files: the total, measured on the largest ones when there are many.
"""
from __future__ import annotations

import glob
import io
import os
import shutil
import tempfile
import time

from PySide6.QtCore import QPointF, QRectF, QSize, Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSlider, QVBoxLayout,
                               QWidget)

from .. import sizes
from ..i18n import N_, tr, trn
from ..paths import ext_of
from .editor_base import EditorWindow, Loader, enter_key, fit_view, qimage_from_pil
from .glass import SLIDER_QSS
from .theme import ACCENT, ACCENT_STRONG, BORDER, MUTED, OK, SURFACE_2, TEXT, WARN, font

# (French texts, translated where they are shown: tr(LEVEL_LABELS[level]))
LEVELS = ("light", "medium", "strong", "max")
LEVEL_LABELS = {"light": N_("Légère"), "medium": N_("Moyenne"), "strong": N_("Forte"),
                "max": N_("Maximale")}
LEVEL_TIPS = {
    "pdf": {"light": N_("Images à 220 ppp : très nettes, même imprimées"),
            "medium": N_("Images à 150 ppp : nettes à l'écran et à l'impression"),
            "strong": N_("Images à 110 ppp : pour l'écran"),
            "max": N_("Images à 80 ppp : le plus léger, images moins nettes")},
    "video": {"light": N_("Jusqu'à 1080p, très bonne qualité"),
              "medium": N_("Jusqu'à 1080p, bonne qualité"),
              "strong": N_("720p : pour un téléphone ou un message"),
              "max": N_("480p : le plus léger")},
    "audio": {"light": N_("MP3 192 kbit/s : musique, très bonne qualité"),
              "medium": N_("MP3 128 kbit/s : musique"),
              "strong": N_("MP3 96 kbit/s : voix, et musique sur un téléphone"),
              "max": N_("MP3 64 kbit/s : voix")},
}
# Why a strength gives no size (kept as is in the results, shown translated).
NO_GAIN, FAILED = "pas de gain", "impossible"
DEFAULT_LEVEL = {"pdf": "medium", "video": "medium", "audio": "strong"}
SAMPLE_PIXELS = 80_000_000      # pictures kept in memory to measure a batch
SAMPLE_FILES = 3
LOUPE = 84                      # radius of the loupe, px
LOUPE_PIXELS = 40_000_000       # the result kept for the loupe, at most
STALE_HOURS = 6


def clean_stale(now: float | None = None) -> None:
    """Remove what popups closed in a hurry (Cerclic stopped...) left in the
    temporary folder."""
    now = now or time.time()
    for d in glob.glob(os.path.join(tempfile.gettempdir(), "cerclic-compress-*")):
        try:
            if now - os.path.getmtime(d) > STALE_HOURS * 3600:
                shutil.rmtree(d, ignore_errors=True)
        except OSError:
            pass


def _sizes_of(paths) -> dict[str, int]:
    out = {}
    for p in paths:
        try:
            out[p] = os.path.getsize(p)
        except OSError:
            pass
    return out


# ----- pictures: background work ----------------------------------------------------------------

def load_samples(paths: list[str]):
    """The pictures the sizes are measured on: the first one (it is shown),
    then the largest others, within SAMPLE_PIXELS (read from their headers:
    nothing more is decoded than what is measured). Returns ([(path,
    picture, size)], the bytes of the files the action will really compress:
    unreadable files and multi-page scans are left out by it)."""
    from PIL import Image
    from ..actions import images
    from ..errors import Cancelled, UserError
    sizes_ = _sizes_of(paths)
    usable: dict[str, int] = {}
    pixels_of: dict[str, int] = {}
    for p in paths:
        if p not in sizes_:
            continue
        try:
            with Image.open(p) as im:
                n = getattr(im, "n_frames", 1) or 1
                if im.format == "TIFF" and n > 1:
                    continue
                w, h = im.size
                pixels_of[p] = w * h * (n if im.format in ("GIF", "WEBP", "PNG") else 1)
        except Exception:
            continue
        usable[p] = sizes_[p]
    first = [p for p in paths if p in usable][:1]
    order = first + sorted((p for p in usable if p not in first), key=lambda p: -usable[p])
    samples, pixels = [], 0
    for p in order:
        if len(samples) >= SAMPLE_FILES:
            break
        if samples and pixels + pixels_of.get(p, 0) > SAMPLE_PIXELS:
            continue
        try:
            pic = images.load(p).to_srgb()
            images._one_page(p, pic)
        except Cancelled:
            raise
        except Exception:
            usable.pop(p, None)
            continue
        samples.append((p, pic, usable[p]))
        pixels += pixels_of.get(p, 0)
    if not samples:
        raise UserError(tr("Image illisible ou format non pris en charge."))
    return samples, sum(usable.values()), len(usable)


def measure(samples, quality: int, preview_box: tuple[int, int]):
    """At `quality`: the size of each sample once compressed, and the first
    one as it will look (shown small, and whole for the loupe)."""
    from PIL import Image
    from ..actions import images
    out, shown, whole, exact_pixels = [], None, None, True
    for i, (p, pic, _) in enumerate(samples):
        _, _, data = images.compressed_data(pic, ext_of(p), quality)
        out.append(len(data))
        if i == 0:
            im = Image.open(io.BytesIO(data))
            W, H = im.size
            if W * H > LOUPE_PIXELS and im.format == "JPEG":   # a huge photo: decoded smaller
                k = (LOUPE_PIXELS / (W * H)) ** 0.5
                im.draft("RGB", (max(1, int(W * k)), max(1, int(H * k))))
            im.load()
            alpha = im.mode in ("RGBA", "LA", "PA") or "transparency" in im.info
            whole = im.convert("RGBA" if alpha else "RGB")
            if whole.width * whole.height > LOUPE_PIXELS:
                k = (LOUPE_PIXELS / (whole.width * whole.height)) ** 0.5
                whole = whole.resize((max(1, int(whole.width * k)),
                                      max(1, int(whole.height * k))),
                                     Image.Resampling.BILINEAR)
            exact_pixels = whole.size == (W, H)
            small = whole.copy()
            small.thumbnail(preview_box, Image.Resampling.LANCZOS)
            shown = qimage_from_pil(small)
    return quality, out, shown, whole, exact_pixels


# ----- PDF, videos, sounds: background work ---------------------------------------------------------

def estimate_level(kind: str, path: str, level: str, workdir: str, cancel, opts: dict):
    """(bytes, exact, file) « Compresser » gives at `level` for one file."""
    if kind == "pdf":
        from .. import jobs
        from ..errors import NothingToDo, UserError
        o = {k: v for k, v in opts.items() if k in ("password", "passwords")}
        o.update(level=level, _out_dir=workdir)
        # always in a process of its own: on a thread, MuPDF would hold the
        # interface up for a moment at each strength, even for a small PDF
        res = jobs.run_isolated("pdf_compress", [path], o, cancel=cancel)
        if res.cancelled:
            from ..errors import Cancelled
            raise Cancelled()
        if res.info:
            raise NothingToDo(res.error)
        if not res.ok or not res.outputs:
            raise UserError(res.error or tr("Compression impossible."))
        return os.path.getsize(res.outputs[0]), True, res.outputs[0]
    from ..actions import video
    return video.estimate_compressed(path, level, workdir, should_stop=cancel.is_set)


def _quality_text(q: int, colors: int | None | bool = False) -> str:
    """« 70 % », and for a PNG what it keeps: « 70 % · 256 couleurs » or
    « 95 % · sans perte » (colors None)."""
    if colors is False:
        return tr("{percent} %", percent=q)
    if colors is None:
        return tr("{percent} % · sans perte", percent=q)
    return trn("{percent} % · {n} couleur", "{percent} % · {n} couleurs", colors, percent=q)


def _problem_text(problem: str, first_word: bool = False) -> str:
    """Why a strength gives no size, in words (capitalised at the start of a line)."""
    if problem == NO_GAIN:
        return tr("Pas de gain") if first_word else tr("pas de gain")
    if problem == FAILED:
        return tr("Impossible") if first_word else tr("impossible")
    return problem.capitalize() if first_word else problem


class _Level(QPushButton):
    """A strength, with the size it gives under its name."""

    def __init__(self, level: str, tip: str):
        super().__init__()
        self.level = level
        self.setCheckable(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setObjectName("level")
        self.setToolTip(tip)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(10, 6, 10, 6)
        lay.setSpacing(1)
        self.name = QLabel(tr(LEVEL_LABELS[level]))
        self.size = QLabel(tr("calcul…"))
        for lbl in (self.name, self.size):
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setAttribute(Qt.WA_TransparentForMouseEvents)
            lay.addWidget(lbl)
        self.setMinimumSize(104, 50)
        self.toggled.connect(lambda _: self._colours())
        self._colours()

    def _colours(self) -> None:
        on = self.isChecked()
        self.name.setStyleSheet(f"color:{'white' if on else TEXT};font-weight:700;"
                                "font-size:12px;background:transparent;")
        self.size.setStyleSheet(f"color:{'white' if on else MUTED};font-size:11px;"
                                "background:transparent;")


# ----- the picture, with its loupe -------------------------------------------------------------

class _Preview(QWidget):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.image = None           # the result, small
        self.whole = None           # the result, every pixel (for the loupe)
        self.full = (1, 1)
        self.exact_pixels = True
        self.message = tr("Chargement…")
        self._mouse: QPointF | None = None

    def set_result(self, image, whole, exact_pixels: bool = True) -> None:
        self.image, self.whole = image, whole
        self.exact_pixels = exact_pixels
        if whole is not None:
            self.full = whole.size
        self.message = ""
        self.update()

    def rect_shown(self) -> QRectF:
        W, H = self.full
        s = min(self.width() / W, self.height() / H)
        w, h = W * s, H * s
        return QRectF((self.width() - w) / 2, (self.height() - h) / 2, w, h)

    def _loupe_useful(self) -> bool:
        dpr = self.devicePixelRatioF() or 1.0
        return self.whole is not None and self.rect_shown().width() * dpr < self.full[0] * 0.9

    def mouseMoveEvent(self, e):
        self._mouse = e.position()
        self.update()

    def leaveEvent(self, e):
        self._mouse = None
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.SmoothPixmapTransform, True)
        if self.image is None:
            p.setPen(QColor(MUTED))
            p.setFont(font(10))
            p.drawText(self.rect(), Qt.AlignCenter | Qt.TextWordWrap, self.message)
            return
        R = self.rect_shown()
        # a checkerboard under a see-through picture
        p.fillRect(R, QColor("white"))
        p.drawImage(R, self.image)
        if not self._loupe_useful():
            return
        m = self._mouse
        if m is None or not R.contains(m):
            text = (tr("Survole l'image : détail à 100 %") if self.exact_pixels
                    else tr("Survole l'image : détail"))
            p.setFont(font(8.5, True))
            tw = p.fontMetrics().horizontalAdvance(text) + 16
            x = R.right() - 8 - tw if self.isRightToLeft() else R.left() + 8
            pill = QRectF(x, R.bottom() - 30, tw, 22)
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(0, 0, 0, 140))
            p.drawRoundedRect(pill, 11, 11)
            p.setPen(QColor("white"))
            p.drawText(pill, Qt.AlignCenter, text)
            return
        dpr = self.devicePixelRatioF() or 1.0
        W, H = self.full
        ix = (m.x() - R.left()) / R.width() * W
        iy = (m.y() - R.top()) / R.height() * H
        half = int(LOUPE * dpr)
        box = (int(ix) - half, int(iy) - half, int(ix) + half, int(iy) + half)
        detail = qimage_from_pil(self.whole.crop(box))
        detail.setDevicePixelRatio(dpr)
        circle = QPainterPath()
        circle.addEllipse(m, LOUPE, LOUPE)
        p.save()
        p.setClipPath(circle)
        p.fillRect(QRectF(m.x() - LOUPE, m.y() - LOUPE, 2 * LOUPE, 2 * LOUPE),
                   QColor("white"))
        p.drawImage(QPointF(m.x() - LOUPE, m.y() - LOUPE), detail)
        p.restore()
        p.setBrush(Qt.NoBrush)
        p.setPen(QPen(QColor(16, 24, 40, 120), 3))
        p.drawEllipse(m, LOUPE, LOUPE)
        p.setPen(QPen(QColor("white"), 1.5))
        p.drawEllipse(m, LOUPE, LOUPE)


# ----- the popup ----------------------------------------------------------------------------------------

class CompressEditor(EditorWindow):
    """Pictures: accepted({"quality": 10 to 95}).
    PDF, videos, sounds: accepted({"level": "light"...,
    "precomputed": {path: the result already made}})."""

    def __init__(self, paths, kind: str, quality: int = 70, level: str | None = None,
                 opts: dict | None = None):
        self.paths = list(paths)
        self.kind = kind
        self.opts = dict(opts or {})          # passwords of protected PDF
        n = len(self.paths)
        title = (os.path.basename(self.paths[0]) if n == 1
                 else trn("{n} fichier", "{n} fichiers", n))
        hint = (tr("Choisis la qualité · {key} pour compresser", key=enter_key())
                if kind == "image"
                else tr("Choisis la force · {key} pour compresser", key=enter_key()))
        super().__init__(title, hint)
        self.originals = _sizes_of(self.paths)
        self.before = sum(self.originals.values())
        self.after: float | None = None
        self.exact = True
        self._workdir = tempfile.mkdtemp(prefix="cerclic-compress-")
        self._handed: str | None = None

        # result size, big, beside the choice
        self.size_big = QLabel("")
        self.size_big.setStyleSheet(f"color:{TEXT};font-size:20px;font-weight:800;")
        self.size_small = QLabel("")
        self.size_small.setObjectName("hint")
        box = QWidget()
        lay = QVBoxLayout(box)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        lay.addWidget(self.size_big)
        lay.addWidget(self.size_small)
        fm = self.size_small.fontMetrics()
        widest = tr("au lieu de {size} · {gain}", size=sizes.human(999 * sizes.BASE ** 2),
                    gain=sizes.gain(100, 0))
        box.setFixedWidth(fm.horizontalAdvance(widest) + 24)
        box.setMinimumHeight(self.size_big.sizeHint().height() + fm.lineSpacing() + 18)

        if kind == "image":
            self._build_picture(quality, box)
        else:
            self._build_levels(level, box)

        self.bar.addStretch(1)
        cancel = QPushButton(tr("Annuler"))
        cancel.setObjectName("ghost")
        cancel.setFocusPolicy(Qt.NoFocus)
        cancel.clicked.connect(self.cancel)
        self.ok_btn = QPushButton(tr("Compresser"))
        self.ok_btn.setObjectName("primary")
        self.ok_btn.setEnabled(False)
        self.ok_btn.setFocusPolicy(Qt.NoFocus)
        self.ok_btn.clicked.connect(self.validate)
        self.bar.addWidget(cancel)
        self.bar.addWidget(self.ok_btn)
        self.setStyleSheet(self.styleSheet() + SLIDER_QSS + (
            f"QPushButton#level{{background:{SURFACE_2};border:1px solid {BORDER};"
            "border-radius:10px;padding:0;}"
            f"QPushButton#level:hover{{border-color:{ACCENT};}}"
            f"QPushButton#level:checked{{background:{ACCENT_STRONG};"
            f"border-color:{ACCENT_STRONG};}}"))

    # -- pictures ---------------------------------------------------------------------------------
    def _build_picture(self, quality: int, size_box) -> None:
        self.preview = _Preview()
        self.center.addWidget(self.preview, 0, Qt.AlignCenter)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(10, 95)
        self.slider.setSingleStep(5)
        self.slider.setPageStep(10)
        self.slider.setValue(max(10, min(95, int(round(quality / 5) * 5))))
        self.slider.setFocusPolicy(Qt.NoFocus)
        self.slider.setMinimumWidth(220)
        self.slider.valueChanged.connect(self._quality_moved)
        name = QLabel(tr("Qualité"))
        name.setStyleSheet(f"color:{TEXT};font-weight:700;font-size:12px;")
        self.q_label = QLabel("")
        self.q_label.setStyleSheet(f"color:{TEXT};font-size:12px;font-weight:600;")
        widest = ([_quality_text(95, 256), _quality_text(95, None)]
                  if ext_of(self.paths[0]) == ".png" else [_quality_text(100)])
        fm = self.q_label.fontMetrics()
        self.q_label.setMinimumWidth(max(fm.horizontalAdvance(t) for t in widest) + 4)
        row = QHBoxLayout()
        row.setSpacing(10)
        row.addWidget(name)
        row.addWidget(self.slider, 1)
        row.addWidget(self.q_label)
        row.addSpacing(14)
        row.addWidget(size_box)
        self.tools.addLayout(row, 1)
        self.batch_note = QLabel("")
        self.batch_note.setObjectName("hint")
        self.center.addWidget(self.batch_note, 0, Qt.AlignCenter)
        self.batch_note.setVisible(len(self.paths) > 1)
        self.gif_only = all(ext_of(p) == ".gif" for p in self.paths)
        self.slider.setEnabled(not self.gif_only)
        self._samples = None
        self._count = len(self.paths)
        self._busy = False
        self._want: int | None = None
        self._timer = QTimer(self, singleShot=True, interval=140)
        self._timer.timeout.connect(self._measure)
        self._loader = Loader(self)
        self._loader.done.connect(self._measured)
        self._samples_loader = Loader(self)
        self._samples_loader.done.connect(self._samples_ready)
        self._show_quality()

    def _show_quality(self) -> None:
        q = self.slider.value()
        if self.gif_only:
            self.q_label.setText(tr("GIF : sans réglage"))
            return
        if ext_of(self.paths[0]) == ".png":
            from ..actions.images import png_colors
            self.q_label.setText(_quality_text(q, png_colors(q)))
        else:
            self.q_label.setText(_quality_text(q))

    def _quality_moved(self, _value: int) -> None:
        self._show_quality()
        self._want = self.slider.value()
        self.size_big.setStyleSheet(f"color:{MUTED};font-size:20px;font-weight:800;")
        self._timer.start()

    def _measure(self) -> None:
        if self._busy or self._samples is None or self._want is None:
            return
        q, self._want = self._want, None
        self._busy = True
        samples = self._samples
        dpr = self.dpr()
        box = (max(64, int(self.preview.width() * dpr)), max(64, int(self.preview.height() * dpr)))
        self._loader.run(lambda: measure(samples, q, box))

    def _measured(self, res, err) -> None:
        self._busy = False
        if err:
            self._unmeasured(err)
            return
        q, new_sizes, shown, whole, exact_pixels = res
        self.preview.set_result(shown, whole, exact_pixels)
        before = sum(size for _, _, size in self._samples)
        after = sum(min(n, size) for n, (_, _, size) in zip(new_sizes, self._samples))
        if len(self._samples) == self._count:
            self.after, self.exact = after, True
        else:                              # a batch: the others like the measured ones
            self.after, self.exact = after / max(1, before) * self.before, False
        self._show_result(gained=any(n < size for n, (_, _, size)
                                     in zip(new_sizes, self._samples)))
        if self._want is not None and self._want != q:
            self._measure()
        elif self._want == q:
            self._want = None

    def _unmeasured(self, err: str) -> None:
        """No size to show: say why, and let the action itself try (it names
        the files it cannot do)."""
        self.size_big.setText("")
        self.size_small.setText(err)
        self.preview.message = err
        self.preview.update()
        self.ok_btn.setEnabled(True)

    def _samples_ready(self, res, err) -> None:
        if err:
            self._unmeasured(err)
            return
        samples, self.before, usable = res
        self._samples = samples
        self._count = usable
        if len(self.paths) > 1:
            left = len(self.paths) - usable
            name = os.path.basename(samples[0][0])
            if len(samples) < usable:
                note = trn("Aperçu : {name} · total pour {n} image, estimé sur {sampled}",
                           "Aperçu : {name} · total pour {n} images, estimé sur {sampled}",
                           usable, name=name, sampled=len(samples))
            else:
                note = trn("Aperçu : {name} · total pour {n} image",
                           "Aperçu : {name} · total pour {n} images", usable, name=name)
            if left:
                note += " · " + trn("{n} laissée de côté", "{n} laissées de côté", left)
            self.batch_note.setText(note)
        self._want = self.slider.value()
        self._measure()

    # -- PDF, videos, sounds ----------------------------------------------------------------
    def _build_levels(self, level: str | None, size_box) -> None:
        self.level = level if level in LEVELS else DEFAULT_LEVEL.get(self.kind, "medium")
        tips = LEVEL_TIPS.get(self.kind, LEVEL_TIPS["video"])
        title = QLabel(tr("Compression"))
        title.setStyleSheet(f"color:{TEXT};font-weight:700;font-size:12px;")
        self.center.addWidget(title)
        row = QHBoxLayout()
        row.setSpacing(8)
        self.level_buttons: dict[str, _Level] = {}
        for lv in LEVELS:
            b = _Level(lv, tr(tips[lv]))
            b.setChecked(lv == self.level)
            b.clicked.connect(lambda _=False, x=lv: self.set_level(x))
            row.addWidget(b)
            self.level_buttons[lv] = b
        self.center.addLayout(row)
        self.tools.addWidget(size_box, 0, Qt.AlignLeft)
        self.tools.addStretch(1)
        self.results: dict[str, tuple] = {}      # level -> (bytes, exact, file, problem)
        self._state = {"want": self.level}
        self._levels_loader = Loader(self)
        self._levels_loader.progress.connect(self._level_ready)

    def set_level(self, level: str) -> None:
        self.level = level
        self._state["want"] = level
        for lv, b in self.level_buttons.items():
            b.setChecked(lv == level)
        self._show_level()

    def _level_ready(self, payload) -> None:
        level, size, exact, made, problem = payload
        self.results[level] = (size, exact, made, problem)
        b = self.level_buttons[level]
        if problem:
            b.size.setText(_problem_text(problem))
        else:
            after = self._scaled(size)
            b.size.setText(("" if exact and len(self.paths) == 1 else "≈ ") + sizes.human(after))
        if level == self.level:
            self._show_level()

    def _scaled(self, size: float) -> float:
        """A batch: the measured file stands for all of them."""
        if len(self.paths) == 1 or self.kind == "audio":
            return size
        return size / max(1, self._sample_size) * self.before

    def _show_level(self) -> None:
        got = self.results.get(self.level)
        if got is None:
            self.after = None
            self.size_big.setText(tr("calcul…"))
            self.size_big.setStyleSheet(f"color:{MUTED};font-size:20px;font-weight:800;")
            tip = LEVEL_TIPS.get(self.kind, {}).get(self.level, "")
            self.size_small.setText(tr(tip) if tip else "")
            self.ok_btn.setEnabled(True)            # no need to wait to compress
            return
        size, exact, _, problem = got
        if problem:
            self.after = None
            self.size_big.setText(_problem_text(problem, first_word=True))
            self.size_big.setStyleSheet(f"color:{WARN};font-size:16px;font-weight:800;")
            self.size_small.setText(tr("Essaie une compression plus forte.")
                                    if problem == NO_GAIN else "")
            self.ok_btn.setEnabled(problem != NO_GAIN)
            return
        self.after = self._scaled(size)
        self.exact = exact and len(self.paths) == 1
        self._show_result(gained=self.after < self.before * 0.98)

    # -- both -------------------------------------------------------------------------------------
    def _show_result(self, gained: bool) -> None:
        approx = "" if self.exact else "≈ "
        self.size_big.setText(approx + sizes.human(self.after))
        if gained:
            self.size_big.setStyleSheet(f"color:{TEXT};font-size:20px;font-weight:800;")
            gain = (f"<span style='color:{OK};font-weight:700'>"
                    f"{sizes.gain(self.before, self.after)}</span>")
            self.size_small.setText(tr("au lieu de {size} · {gain}",
                                       size=sizes.human(self.before), gain=gain))
            self.ok_btn.setEnabled(True)
        else:
            self.size_big.setText(tr("Pas plus léger"))
            self.size_big.setStyleSheet(f"color:{WARN};font-size:20px;font-weight:800;")
            before = sizes.human(self.before)
            self.size_small.setText(
                tr("Original : {size} · baisse la qualité", size=before) if self.kind == "image"
                else tr("Original : {size} · compresse plus fort", size=before))
            self.ok_btn.setEnabled(False)

    # -- opening -------------------------------------------------------------------------------------
    def start(self, anchor=None) -> None:
        if anchor is not None:
            self.anchor = anchor
        if self.kind == "image":
            from ..actions.images import oriented_size
            try:
                w, h = oriented_size(self.paths[0])
            except Exception:
                w, h = 800, 600
            room_w, room_h = self.room(560, 400)
            vw, vh = fit_view(w, h, room_w, room_h - 60, min_side=280,
                              max_scale=1.0 / self.dpr())
            self.preview.setFixedSize(QSize(vw, vh))
            self.size_big.setText(tr("calcul…"))
            self.size_big.setStyleSheet(f"color:{MUTED};font-size:20px;font-weight:800;")
            self.open_at()
            paths = list(self.paths)
            self._samples_loader.run(lambda: load_samples(paths))
            return
        self._show_level()
        self.open_at()
        self._start_estimates()

    def _start_estimates(self) -> None:
        kind, workdir, state, opts = self.kind, self._workdir, self._state, self.opts
        paths = list(self.paths)
        largest = max(paths, key=lambda p: self.originals.get(p, 0))
        self._sample_size = self.originals.get(largest, 1)
        cancel = self._levels_loader.stop_event

        def work(report, stop):
            from ..errors import Cancelled, NothingToDo
            done: set[str] = set()
            while len(done) < len(LEVELS) and not stop():
                want = state["want"]
                order = [want] + sorted((lv for lv in LEVELS if lv != want),
                                        key=lambda lv: abs(LEVELS.index(lv) - LEVELS.index(want)))
                level = next(lv for lv in order if lv not in done)
                done.add(level)
                try:
                    if kind == "audio":            # quick: every file, from its length
                        total = 0
                        for p in paths[:60]:
                            total += estimate_level(kind, p, level, workdir, cancel, opts)[0]
                        if len(paths) > 60:
                            total = total / max(1, sum(_sizes_of(paths[:60]).values())) \
                                * sum(_sizes_of(paths).values())
                        report((level, total, False, None, ""))
                        continue
                    size, exact, made = estimate_level(kind, largest, level, workdir,
                                                       cancel, opts)
                    report((level, size, exact, made if len(paths) == 1 else None, ""))
                except Cancelled:
                    try:                 # the popup is gone: its folder too, once empty
                        os.rmdir(workdir)
                    except OSError:
                        pass
                    return
                except NothingToDo:
                    report((level, None, False, None, NO_GAIN))
                except Exception as exc:
                    from ..errors import UserError
                    from ..log import log, log_exception
                    if isinstance(exc, UserError):
                        log(f"estimation de compression ({level}) : {exc}")
                    else:
                        log_exception(f"estimation de compression ({level})")
                    report((level, None, False, None, FAILED))
        self._levels_loader.run_reporting(work)

    # -- keyboard -------------------------------------------------------------------------------------
    def keyPressEvent(self, e):
        k = e.key()
        if self.kind == "image" and k in (Qt.Key_Left, Qt.Key_Down, Qt.Key_Right, Qt.Key_Up):
            step = 5 if k in (Qt.Key_Right, Qt.Key_Up) else -5
            self.slider.setValue(self.slider.value() + step)
        elif self.kind != "image" and k in (Qt.Key_Left, Qt.Key_Right):
            i = LEVELS.index(self.level) + (1 if k == Qt.Key_Right else -1)
            if 0 <= i < len(LEVELS):
                self.set_level(LEVELS[i])
        else:
            super().keyPressEvent(e)

    # -- result ---------------------------------------------------------------------------------------
    def validate(self) -> None:
        if not self.ok_btn.isEnabled():
            return
        if self.kind == "image":
            self.finish({"quality": self.slider.value()})
            return
        res = {"level": self.level}
        got = self.results.get(self.level)
        if got and got[2] and len(self.paths) == 1 and os.path.isfile(got[2]):
            self._handed = got[2]
            res["precomputed"] = {self.paths[0]: got[2]}
        self.finish(res)

    def closeEvent(self, e):
        super().closeEvent(e)
        self._clean()

    def _clean(self) -> None:
        """Everything worked out for nothing goes; the result handed over stays
        until the action takes it."""
        keep = os.path.normcase(os.path.abspath(self._handed)) if self._handed else None
        try:
            names = os.listdir(self._workdir)
        except OSError:
            return
        for name in names:
            p = os.path.join(self._workdir, name)
            if keep and os.path.normcase(os.path.abspath(p)) == keep:
                continue
            try:
                if os.path.isdir(p):
                    shutil.rmtree(p, ignore_errors=True)
                else:
                    os.remove(p)
            except OSError:
                pass
        if not keep:
            try:
                os.rmdir(self._workdir)
            except OSError:
                pass
