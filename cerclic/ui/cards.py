"""Cards in the bottom-right corner: progress while an action runs, then the
result with Open / Folder / Undo, and short messages.

Undo is safe by construction: every output is a brand-new file beside the
original, so undoing only removes what Cerclic just created.
"""
from __future__ import annotations

import os
import subprocess
import sys

from PySide6.QtCore import QObject, QPoint, QRectF, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QCursor, QGuiApplication, QPainter
from PySide6.QtWidgets import (QGraphicsDropShadowEffect, QHBoxLayout, QLabel,
                               QPushButton, QVBoxLayout, QWidget)

from ..sizes import change, human, size_of
from .theme import (ACCENT, ACCENT_STRONG, BORDER, BUTTON_QSS, ERROR, MUTED, OK, TEXT,
                    WARN, card_qss)

GAP = 6


def open_path(path: str) -> None:
    try:
        if os.name == "nt":
            from ..sysenv import outside_env
            with outside_env():
                os.startfile(path)  # noqa: S606 - opens with the default app
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    except Exception:
        pass


def reveal_path(path: str) -> None:
    try:
        if os.name == "nt":
            from ..sysenv import clean_env, neutral_dir
            subprocess.Popen(["explorer", "/select,", os.path.normpath(path)],
                             env=clean_env(), cwd=neutral_dir())
        elif sys.platform == "darwin":
            subprocess.Popen(["open", "-R", path])
        else:
            subprocess.Popen(["xdg-open", os.path.dirname(path)])
    except Exception:
        pass


def undo_outputs(outputs: list[str]) -> list[str]:
    """Delete files Cerclic created, then the folders it created if now empty.
    Returns the files that could not be deleted (open in another app...)."""
    kept: list[str] = []
    for p in outputs:
        try:
            if os.path.isfile(p):
                os.remove(p)
        except OSError:
            kept.append(p)
    for d in sorted({os.path.dirname(p) for p in outputs}, key=len, reverse=True):
        try:
            if os.path.isdir(d) and not os.listdir(d):
                os.rmdir(d)
        except OSError:
            pass
    return kept


class _Bar(QWidget):
    """Thin progress bar; None = indeterminate (a sliding segment)."""

    def __init__(self):
        super().__init__()
        self.setFixedHeight(6)
        self._value: float | None = None
        self._phase = 0.0
        self._timer = QTimer(self, interval=30)
        self._timer.timeout.connect(self._tick)
        self._timer.start()

    def set_value(self, v: float | None) -> None:
        self._value = v
        self.update()

    def stop(self) -> None:
        self._timer.stop()

    def _tick(self):
        if self._value is None:
            self._phase = (self._phase + 0.018) % 1.4
            self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(BORDER))
        r = QRectF(self.rect())
        p.drawRoundedRect(r, 3, 3)
        p.setBrush(QColor(ACCENT))
        if self._value is None:
            w = r.width() * 0.32
            x = r.width() * (self._phase - 0.32)
            seg = QRectF(max(0.0, x), 0, min(w, r.width() - max(0.0, x)), r.height())
            if seg.width() > 0:
                p.drawRoundedRect(seg, 3, 3)
        else:
            p.drawRoundedRect(QRectF(0, 0, r.width() * self._value, r.height()), 3, 3)


class Card(QWidget):
    """Frameless card that never steals the keyboard."""
    closed = Signal(object)
    resized = Signal()

    def __init__(self, accent: str = ACCENT_STRONG, auto_ms: int = 0):
        super().__init__(None, Qt.FramelessWindowHint | Qt.Tool
                         | Qt.WindowStaysOnTopHint | Qt.WindowDoesNotAcceptFocus
                         | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAttribute(Qt.WA_MacAlwaysShowToolWindow)   # macOS: stays shown in the background
        self.setWindowTitle("Cerclic")
        self.screen_hint = QGuiApplication.screenAt(QCursor.pos()) or \
            QGuiApplication.primaryScreen()
        self._card = QWidget(self)
        self._card.setObjectName("card")
        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 16, 16, 16)
        outer.addWidget(self._card)
        self.body = QVBoxLayout(self._card)
        self.body.setContentsMargins(16, 13, 16, 13)
        self.body.setSpacing(8)
        self.setFixedWidth(360)
        self._accent = accent
        self._restyle()
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(20, 40, 90, 64))
        self._card.setGraphicsEffect(shadow)
        self._timer = QTimer(self, singleShot=True)
        self._timer.timeout.connect(self.close)
        self._auto_ms = auto_ms

    def _restyle(self):
        self.setStyleSheet(
            card_qss(14) +
            f"#head{{color:{self._accent};font-size:14px;font-weight:700;}}"
            f"#sub{{color:{MUTED};font-size:12px;}}"
            f"QLabel{{color:{TEXT};}}" + BUTTON_QSS +
            f"QPushButton#closeCard{{background:transparent;color:{MUTED};padding:0;"
            "font-size:12px;border-radius:7px;border:none;}"
            f"QPushButton#closeCard:hover{{background:{BORDER};color:{TEXT};}}")

    def set_accent(self, accent: str) -> None:
        self._accent = accent
        self._restyle()

    def start_auto_close(self, ms: int) -> None:
        self._auto_ms = ms
        if ms:
            self._timer.start(ms)

    def enterEvent(self, _):
        self._timer.stop()

    def leaveEvent(self, _):
        if self._auto_ms:
            self._timer.start(self._auto_ms)

    def closeEvent(self, e):
        self._timer.stop()
        self.closed.emit(self)
        super().closeEvent(e)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.resized.emit()


def _head(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setObjectName("head")
    lbl.setWordWrap(True)
    return lbl


def _sub(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setObjectName("sub")
    lbl.setWordWrap(True)
    lbl.setTextInteractionFlags(Qt.NoTextInteraction)
    return lbl


class MessageCard(Card):
    def __init__(self, title: str, text: str = "", kind: str = "info",
                 buttons: list[tuple[str, object]] | None = None, auto_ms: int = 8000):
        accent = {"info": ACCENT_STRONG, "ok": OK, "error": ERROR,
                  "warn": WARN}.get(kind, ACCENT_STRONG)
        super().__init__(accent)
        top = QHBoxLayout()
        top.addWidget(_head(title), 1)
        top.addWidget(_close_button(self), 0, Qt.AlignTop)
        self.body.addLayout(top)
        if text:
            self.body.addWidget(_sub(text))
        if buttons:
            row = QHBoxLayout()
            row.setSpacing(8)
            row.addStretch(1)
            for i, (label, fn) in enumerate(buttons):
                b = QPushButton(label)
                if i == len(buttons) - 1:
                    b.setObjectName("primary")
                else:
                    b.setObjectName("ghost")
                b.clicked.connect(lambda _=False, f=fn: self._click(f))
                row.addWidget(b)
            self.body.addLayout(row)
        self.start_auto_close(auto_ms)

    def _click(self, fn):
        self.close()
        if fn:
            fn()


def _close_button(card: "Card") -> QPushButton:
    b = QPushButton("✕")
    b.setObjectName("closeCard")
    b.setToolTip("Fermer")
    b.setFixedSize(26, 24)
    b.setFocusPolicy(Qt.NoFocus)
    b.clicked.connect(card.close)
    return b


_KNOWN = {"desktop": "Bureau", "downloads": "Téléchargements", "pictures": "Images",
          "videos": "Vidéos", "movies": "Vidéos", "music": "Musique",
          "documents": "Documents"}


def folder_label(outputs: list[str]) -> str:
    """Where the results are, as the file manager names that folder."""
    d = os.path.dirname(os.path.abspath(outputs[0]))
    name = os.path.basename(d.rstrip("\\/")) or d
    return _KNOWN.get(name.lower(), name)


def _elided(label: QLabel, text: str, width: int) -> str:
    """A long file name shortened in the middle, whole in the tooltip."""
    fm = label.fontMetrics()
    if fm.horizontalAdvance(text) <= width:
        return text
    label.setToolTip(text)
    return fm.elidedText(text, Qt.ElideMiddle, width)


class JobCard(Card):
    """Progress of one action, then its result."""
    cancel_requested = Signal()

    def __init__(self, title: str):
        super().__init__(ACCENT_STRONG)
        self._title = title
        top = QHBoxLayout()
        self._head = _head(title + "…")
        top.addWidget(self._head, 1)
        self._stop = QPushButton("Arrêter")
        self._stop.setObjectName("ghost")
        self._stop.clicked.connect(self._on_stop)
        top.addWidget(self._stop)
        self._top = top
        self.body.addLayout(top)
        self._status = _sub("En cours")
        self.body.addWidget(self._status)
        self._bar = _Bar()
        self.body.addWidget(self._bar)
        self._outputs: list[str] = []

    def _on_stop(self):
        self._stop.setEnabled(False)
        self._status.setText("Arrêt en cours…")
        self.cancel_requested.emit()

    def set_progress(self, fraction: float | None, text: str = "") -> None:
        self._bar.set_value(fraction)
        if text:
            pct = f"  {int(round(fraction * 100))} %" if fraction is not None else ""
            self._status.setText(text + pct)

    def finish(self, result, note: str = "") -> None:
        """Turn into the result card."""
        self._bar.stop()
        self._bar.hide()
        self._stop.hide()
        close = _close_button(self)
        self._top.addWidget(close, 0, Qt.AlignTop)
        close.show()
        self._outputs = list(result.outputs)
        if result.ok:
            self.set_accent(OK)
            self._head.setText("✓  " + self._title)
            n = len(self._outputs)
            text = (_elided(self._status, os.path.basename(self._outputs[0]), 290)
                    if n == 1 else f"{n} fichiers créés")
            where = "\u00a0«\u00a0" + folder_label(self._outputs) + "\u00a0»"
            # (sizes measured with the work, off the interface: a network drive
            # can be slow to answer)
            after = getattr(result, "bytes_after", 0) or size_of(self._outputs)
            sources = list(getattr(result, "sources", []) or [])
            if result.action_id.endswith("_compress") and sources:
                # what the compression gained, the reason it was done
                before = getattr(result, "bytes_before", 0) or size_of(sources)
                text += "\n" + change(before, after) + "\nDans" + where
            elif after:
                text += f"\n{human(after)}" + (" en tout" if n > 1 else "") + " · dans" + where
            else:
                text += "\nDans" + where
            if n == 1 and not self._status.toolTip():
                self._status.setToolTip(self._outputs[0])
            notes = list(getattr(result, "notes", []) or [])
            if len(notes) > 1:
                note = (note + "\n" if note else "") + (
                    f"{len(notes)} fichiers laissés de côté, par exemple : {notes[0]}")
            elif notes:
                note = (note + "\n" if note else "") + notes[0]
            self._status.setText(text + (f"\n{note}" if note else ""))
            row = QHBoxLayout()
            row.setSpacing(8)
            b_open = QPushButton("Ouvrir")
            b_open.setObjectName("primary")
            b_open.clicked.connect(self._open)
            b_dir = QPushButton("Dossier")
            b_dir.clicked.connect(self._reveal)
            b_undo = QPushButton("Supprimer")
            b_undo.setObjectName("danger")
            b_undo.setToolTip("Supprime ce que Cerclic vient de créer (ton fichier "
                              "d'origine ne bouge pas)")
            b_undo.clicked.connect(self._undo)
            row.addWidget(b_open)
            row.addWidget(b_dir)
            row.addStretch(1)
            row.addWidget(b_undo)
            self.body.addLayout(row)
            self._buttons = (b_open, b_dir, b_undo)
            for b in self._buttons:
                b.show()
            self.start_auto_close(8000)
        elif result.cancelled:
            self.set_accent(MUTED)
            self._head.setText(self._title)
            self._status.setText("Arrêté : rien n'a été créé.")
            self.start_auto_close(3500)
        elif result.info:
            self.set_accent(ACCENT_STRONG)
            self._head.setText(self._title)
            self._status.setText(result.error)
            self.start_auto_close(6000)
        else:
            self.set_accent(ERROR)
            self._head.setText("✕  " + self._title + " impossible")
            self._status.setText(result.error or "Erreur inconnue.")
            self.start_auto_close(12000)
        self.adjustSize()

    def _open(self):
        if self._outputs:
            target = self._outputs[0]
            if len(self._outputs) > 1:
                target = os.path.dirname(target)
            open_path(target)
        self.close()

    def _reveal(self):
        if self._outputs:
            reveal_path(self._outputs[0])
        self.close()

    def _undo(self):
        kept = undo_outputs(self._outputs)
        self._status.setToolTip("")
        if kept:                       # open in another app: say so, keep the buttons
            self.set_accent(WARN)
            self._head.setText("Suppression impossible")
            self._status.setText("Le fichier est sans doute ouvert dans une autre "
                                 "application : ferme-la, puis réessaie.")
            self._outputs = kept
            self.adjustSize()
            self.start_auto_close(8000)
            return
        for b in getattr(self, "_buttons", ()):
            b.hide()
        self.set_accent(MUTED)
        n = len(self._outputs)
        self._head.setText("Fichier supprimé" if n == 1 else "Fichiers supprimés")
        self._status.setText("Ton fichier d'origine n'a pas bougé.")
        self._outputs = []
        self.adjustSize()
        self.start_auto_close(2500)


class CardStack(QObject):
    """Keeps cards stacked in the bottom-right corner of their screen."""

    def __init__(self):
        super().__init__()
        self._cards: list[Card] = []
        self._pending = QTimer(self, singleShot=True, interval=0)
        self._pending.timeout.connect(self.relayout)

    def add(self, card: Card) -> Card:
        card.closed.connect(self._remove)
        card.resized.connect(self._pending.start)
        self._cards.append(card)
        card.adjustSize()
        self.relayout()
        card.show()
        return card

    def _remove(self, card) -> None:
        if card in self._cards:
            self._cards.remove(card)
            QTimer.singleShot(0, self.relayout)

    def relayout(self) -> None:
        by_screen: dict = {}
        for c in self._cards:
            by_screen.setdefault(c.screen_hint, []).append(c)
        for screen, cards in by_screen.items():
            try:
                geo = screen.availableGeometry()
            except RuntimeError:  # screen unplugged
                geo = QGuiApplication.primaryScreen().availableGeometry()
            # Widgets have a 16 px transparent margin (for the shadow): overlap
            # them so the visible cards are GAP apart, 12 px from the edges.
            bottom = geo.bottom() + 1 + 4
            for c in reversed(cards):
                try:
                    c.adjustSize()
                    top = bottom - c.height()
                    c.move(QPoint(geo.right() + 1 + 4 - c.width(), top))
                    bottom = top + 32 - GAP
                except RuntimeError:
                    continue

    def close_all(self) -> None:
        for c in list(self._cards):
            try:
                c.close()
            except RuntimeError:
                pass
