"""Cerclic's window: real settings, laid out like the system ones.

A sidebar of sections (Général, Raccourci clavier, Clic droit, Fichiers créés,
Signature, Qualité, À propos) and, for each, rows on frosted glass: what the
setting does on the left, its switch or button on the right. It opens when
Cerclic is launched from its icon (Desktop, Start menu, Applications) or from
the tray icon. Every change applies at once; there is nothing to save. A new
language makes the app build the window again in it (app.py).
"""
from __future__ import annotations

import os
import sys

from PySide6.QtCore import QPoint, QRectF, QSize, Qt, QTimer, Signal
from PySide6.QtGui import (QColor, QGuiApplication, QKeySequence, QPainter, QPen,
                           QPixmap, QShortcut)
from PySide6.QtWidgets import (QButtonGroup, QFileDialog, QFrame, QHBoxLayout,
                               QLabel, QPushButton, QScrollArea, QSlider,
                               QStackedWidget, QVBoxLayout, QWidget)

from .. import __version__, i18n
from ..i18n import N_, tr
from ..settings import Settings
from ..system import ENTER_KEY, IS_MAC, hotkeys
from .glass import (SLIDER_QSS, Backdrop, Choice, GlassPanel, Group, KeyboardFocus,
                    NavItem, Row, Select, Toggle, focus_ring, group_block, label, mirrored)
from .theme import (ACCENT, BUTTON_QSS, ERROR, FOCUS_QSS, MUTED, OK, SCROLL_QSS, TEXT,
                    base_font)

hk = hotkeys()            # this system's shortcut module (same names on both)

# ----- shortcut recording ------------------------------------------------------------

_QT_TO_VK = {}


def _qt_vk_table() -> dict:
    if not _QT_TO_VK:
        table = {Qt.Key_Space: 0x20, Qt.Key_Tab: 0x09, Qt.Key_Return: 0x0D,
                 Qt.Key_Enter: 0x0D, Qt.Key_Backspace: 0x08, Qt.Key_Insert: 0x2D,
                 Qt.Key_Delete: 0x2E, Qt.Key_Home: 0x24, Qt.Key_End: 0x23,
                 Qt.Key_PageUp: 0x21, Qt.Key_PageDown: 0x22, Qt.Key_Left: 0x25,
                 Qt.Key_Up: 0x26, Qt.Key_Right: 0x27, Qt.Key_Down: 0x28,
                 Qt.Key_Pause: 0x13, Qt.Key_Print: 0x2C, Qt.Key_Escape: 0x1B}
        for i in range(26):
            table[Qt.Key(Qt.Key_A.value + i)] = 0x41 + i
        for i in range(10):
            table[Qt.Key(Qt.Key_0.value + i)] = 0x30 + i
        for i in range(24):
            table[Qt.Key(Qt.Key_F1.value + i)] = 0x70 + i
        _QT_TO_VK.update({int(k.value if hasattr(k, "value") else k): v
                          for k, v in table.items()})
    return _QT_TO_VK


_MODIFIER_KEYS = {Qt.Key_Control, Qt.Key_Alt, Qt.Key_Shift, Qt.Key_Meta,
                  Qt.Key_AltGr, Qt.Key_Super_L, Qt.Key_Super_R}


def combo_from_event(e) -> tuple[int, int]:
    """(modifier flags, key) of a key press as the shortcut module stores them;
    key 0 while only modifiers are held. The physical key is used, so the
    digits of an AZERTY keyboard count as digits. (On macOS, Qt names Command
    ControlModifier and Control MetaModifier: the macOS module's MOD_* follow.)"""
    m = e.modifiers()
    mods = 0
    if m & Qt.ControlModifier:
        mods |= hk.MOD_CONTROL
    if m & Qt.AltModifier:
        mods |= hk.MOD_ALT
    if m & Qt.ShiftModifier:
        mods |= hk.MOD_SHIFT
    if m & Qt.MetaModifier:
        mods |= hk.MOD_WIN
    key = e.key()
    if key in _MODIFIER_KEYS:
        return mods, 0
    native = getattr(hk, "from_native", None)
    if native is not None:                      # macOS: the key code itself
        return mods, native(e)
    vk = 0
    if sys.platform == "win32":
        native = e.nativeVirtualKey()
        if 0 < native < 0xFF:
            vk = native
    if not vk:
        vk = _qt_vk_table().get(int(key.value if hasattr(key, "value") else key), 0)
    if not vk and m & Qt.KeypadModifier and Qt.Key_0 <= key <= Qt.Key_9:
        vk = 0x60 + (int(key) - int(Qt.Key_0))
    return mods, vk


class KeyCaps(QWidget):
    """The combination drawn as keyboard keys."""

    def __init__(self):
        super().__init__()
        self.parts: list[str] = []
        self.placeholder = ""
        self.active = False
        self.setMinimumHeight(40)

    def set_parts(self, parts: list[str], placeholder: str = "") -> None:
        self.parts, self.placeholder = parts, placeholder
        self.updateGeometry()
        self.update()

    def sizeHint(self) -> QSize:
        return QSize(280, 40)

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        f = base_font()
        f.setPixelSize(13)
        f.setBold(True)
        p.setFont(f)
        fm = p.fontMetrics()
        x, h = 2.0, 32.0
        y = (self.height() - h) / 2
        if not self.parts:
            p.setPen(QColor(ACCENT if self.active else MUTED))
            f.setBold(False)
            p.setFont(f)
            p.drawText(QRectF(4, 0, self.width() - 4, self.height()),
                       Qt.AlignVCenter | Qt.AlignLeft, self.placeholder)
            return
        for i, part in enumerate(self.parts):
            w = max(36.0, fm.horizontalAdvance(part) + 24.0)
            r = QRectF(x, y, w, h)
            p.setPen(Qt.NoPen)                          # the key's thickness
            p.setBrush(QColor(30, 50, 100, 38))
            p.drawRoundedRect(r.translated(0, 2), 8, 8)
            p.setBrush(QColor("#FFFFFF"))
            p.setPen(QPen(QColor(ACCENT) if self.active else QColor("#D3DAE6"), 1.2))
            p.drawRoundedRect(r, 8, 8)
            p.setPen(QColor(TEXT))
            p.drawText(r, Qt.AlignCenter, part)
            x += w
            if i < len(self.parts) - 1:
                p.setPen(QColor(MUTED))
                p.drawText(QRectF(x, y, 20, h), Qt.AlignCenter, "+")
                x += 20


class ShortcutEdit(QWidget):
    """Shows the shortcut; "Modifier" records the next combination pressed."""
    chosen = Signal(int, int)        # mods, vk
    capturing = Signal(bool)

    def __init__(self, mods: int, vk: int):
        super().__init__()
        self.mods, self.vk = mods, vk
        self.recording = False
        self.setFocusPolicy(Qt.StrongFocus)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(6)
        row = QHBoxLayout()
        row.setSpacing(8)
        self.caps = KeyCaps()
        row.addWidget(self.caps, 1)
        self.change_btn = QPushButton(tr("Modifier"))
        self.change_btn.setFocusPolicy(Qt.TabFocus)     # a click keeps the recording focused
        self.change_btn.clicked.connect(self.toggle_recording)
        self.default_btn = QPushButton(tr("Par défaut"))
        self.default_btn.setObjectName("ghost")
        self.default_btn.setFocusPolicy(Qt.TabFocus)
        self.default_btn.clicked.connect(self._default)
        row.addWidget(self.change_btn)
        row.addWidget(self.default_btn)
        lay.addLayout(row)
        self.status = QLabel("")
        self.status.setWordWrap(True)
        self.status.setObjectName("status")
        self.status.setStyleSheet("background:transparent;")
        lay.addWidget(self.status)
        self._show_combo()

    def _show_combo(self) -> None:
        self.caps.active = False
        self.caps.set_parts(hk.label(self.mods, self.vk).split(" + "))

    def set_combo(self, mods: int, vk: int) -> None:
        self.mods, self.vk = mods, vk
        if not self.recording:
            self._show_combo()

    def set_status(self, text: str, kind: str = "muted") -> None:
        color = {"ok": OK, "error": ERROR, "muted": MUTED, "accent": ACCENT}[kind]
        self.status.setStyleSheet(f"color:{color};font-size:12px;background:transparent;")
        self.status.setText(text)

    def toggle_recording(self) -> None:
        if self.recording:
            self.stop_recording(tr("Raccourci inchangé."))
        else:
            self.start_recording()

    def start_recording(self) -> None:
        self.recording = True
        self.change_btn.setText(tr("Annuler"))
        self.caps.active = True
        self.caps.set_parts([], tr("Appuie sur ta combinaison…"))
        self.set_status(tr("Exemples : Maj + Cmd + Espace, Ctrl + Option + X. Échap pour "
                           "annuler.") if IS_MAC
                        else tr("Exemples : Ctrl + Alt + Espace, Ctrl + Maj + X, "
                                "Win + Maj + C. Échap pour annuler."), "accent")
        self.setFocus(Qt.OtherFocusReason)
        self.grabKeyboard()
        self.capturing.emit(True)

    def stop_recording(self, message: str = "") -> None:
        if not self.recording:
            return
        self.recording = False
        self.releaseKeyboard()
        self.change_btn.setText(tr("Modifier"))
        self._show_combo()
        if message:
            self.set_status(message, "muted")
        self.capturing.emit(False)

    def _default(self) -> None:
        # Same order as a recorded combination: saved first, then the pause ends.
        was_recording = self.recording
        if was_recording:
            self.recording = False
            self.releaseKeyboard()
            self.change_btn.setText(tr("Modifier"))
        self.mods, self.vk = hk.DEFAULT_MODS, hk.DEFAULT_VK
        self._show_combo()
        self.set_status(tr("Vérification…"), "muted")
        self.chosen.emit(hk.DEFAULT_MODS, hk.DEFAULT_VK)
        if was_recording:
            self.capturing.emit(False)

    def keyPressEvent(self, e):
        if not self.recording:
            return super().keyPressEvent(e)
        mods, vk = combo_from_event(e)
        if vk == hk.VK_ESCAPE and not mods:
            self.stop_recording(tr("Raccourci inchangé."))
            return
        if not vk:
            parts = hk.label(mods, 0).split(" + ")[:-1] if mods else []
            self.caps.set_parts(parts + ["…"] if parts else [],
                                tr("Appuie sur ta combinaison…"))
            return
        problem = hk.check(mods, vk)
        if problem:
            self.caps.set_parts(hk.label(mods, vk).split(" + "))
            self.set_status(problem, "error")
            return
        self.mods, self.vk = mods, vk
        self.recording = False
        self.releaseKeyboard()
        self.change_btn.setText(tr("Modifier"))
        self._show_combo()
        self.set_status(tr("Vérification…"), "muted")
        self.chosen.emit(mods, vk)          # saved first: then the pause ends
        self.capturing.emit(False)

    def keyReleaseEvent(self, e):
        if self.recording:
            m = e.modifiers()
            if not (m & (Qt.ControlModifier | Qt.AltModifier | Qt.ShiftModifier
                         | Qt.MetaModifier)):
                self.caps.set_parts([], tr("Appuie sur ta combinaison…"))
            return
        super().keyReleaseEvent(e)

    def focusOutEvent(self, e):
        super().focusOutEvent(e)
        if self.recording:
            QTimer.singleShot(0, lambda: self.recording and not self.hasFocus()
                              and self.stop_recording(tr("Raccourci inchangé.")))


# ----- the window ---------------------------------------------------------------------------

def _button(text: str, kind: str = "", tip: str = "") -> QPushButton:
    b = QPushButton(text)
    if kind:
        b.setObjectName(kind)
    if tip:
        b.setToolTip(tip)
    b.setCursor(Qt.PointingHandCursor)
    b.setFocusPolicy(Qt.TabFocus)                 # a click leaves no focus ring
    return b


class _Slider(QSlider):
    """A slider the mouse wheel does not change while the page scrolls past it."""

    def wheelEvent(self, e):
        if self.hasFocus():
            super().wheelEvent(e)
        else:
            e.ignore()                       # the page scrolls instead


def _scale(slider: QSlider, low: str | None = None, high: str | None = None) -> QWidget:
    """The slider with what each end means, under it."""
    w = QWidget()
    w.setAttribute(Qt.WA_TranslucentBackground)
    lay = QVBoxLayout(w)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(2)
    lay.addWidget(slider)
    ends = QHBoxLayout()
    ends.addWidget(label(low or tr("Plus léger"), "note"))
    ends.addStretch(1)
    ends.addWidget(label(high or tr("Plus net"), "note"))
    lay.addLayout(ends)
    return w


def _slider(lo: int, hi: int, value: int) -> QSlider:
    s = _Slider(Qt.Horizontal)
    s.setFocusPolicy(Qt.TabFocus)
    s.setRange(lo, hi)
    s.setValue(int(value))
    s.setPageStep(5)
    s.setMinimumWidth(220)
    s.setStyleSheet(SLIDER_QSS)
    s.setCursor(Qt.PointingHandCursor)
    return s


class _Page(QScrollArea):
    """One section: a big title, a line of explanation, then its groups."""

    def __init__(self, title: str, subtitle: str):
        super().__init__()
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet("QScrollArea{background:transparent;}" + SCROLL_QSS)
        self.viewport().setAutoFillBackground(False)
        body = QWidget()
        body.setAttribute(Qt.WA_TranslucentBackground)
        self.setWidget(body)
        # QScrollArea turns autoFillBackground on for its widget: Qt would then
        # take this see-through page for opaque and not repaint the backdrop
        # under it, leaving the previous page's pixels behind.
        body.setAutoFillBackground(False)
        self.lay = QVBoxLayout(body)
        self.lay.setContentsMargins(28, 24, 28, 24)
        self.lay.setSpacing(18)
        head = QVBoxLayout()
        head.setSpacing(4)
        head.addWidget(label(title, "title"))
        if subtitle:
            head.addWidget(label(subtitle, "subtitle"))
        self.lay.addLayout(head)
        self._end = None

    def add(self, w: QWidget) -> QWidget:
        self.lay.addWidget(w)
        return w

    def finish(self) -> None:
        self.lay.addStretch(1)


class _Banner(GlassPanel):
    """The welcome note shown on the first launch."""

    def __init__(self, text: str):
        super().__init__(radius=16, alpha=205)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(18, 14, 18, 18)
        lay.setSpacing(14)
        from .logo import logo_pixmap
        logo = QLabel()
        logo.setPixmap(logo_pixmap(96).scaled(44, 44, Qt.KeepAspectRatio,
                                              Qt.SmoothTransformation))
        logo.setStyleSheet("background:transparent;")
        lay.addWidget(logo, 0, Qt.AlignTop)
        texts = QVBoxLayout()
        texts.setSpacing(4)
        texts.addWidget(label(tr("Bienvenue dans Cerclic"), "row"))
        texts.addWidget(label(text, "desc"))
        lay.addLayout(texts, 1)


class _Way(KeyboardFocus, QWidget):
    """One way of opening the wheel: a glyph tile and a sentence. With a page to
    set it up, the whole row is a link to it (tile in that page's colour, ›)."""
    opened = Signal()

    def __init__(self, glyph: str, color: str, title: str, text: str, link: bool = False,
                 tip: str = ""):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.glyph, self.color, self.link = glyph, QColor(color), link
        self._hover = False
        lay = QHBoxLayout(self)
        start, end = 60, 36 if link else 16             # the tile is on the reading side
        if self.layoutDirection() == Qt.RightToLeft:
            start, end = end, start
        lay.setContentsMargins(start, 12, end, 12)
        texts = QVBoxLayout()
        texts.setSpacing(2)
        texts.addWidget(label(title, "row"))
        self.text = label(text, "desc")
        texts.addWidget(self.text)
        lay.addLayout(texts, 1)
        if link:
            self.setCursor(Qt.PointingHandCursor)
            self.setFocusPolicy(Qt.TabFocus)
            if tip:
                self.setToolTip(tip)

    def enterEvent(self, _):
        self._hover = True
        self.update()

    def leaveEvent(self, _):
        self._hover = False
        self.update()

    def mouseReleaseEvent(self, e):
        if self.link and e.button() == Qt.LeftButton and self.rect().contains(e.pos()):
            self.opened.emit()
        super().mouseReleaseEvent(e)

    def keyPressEvent(self, e):
        if self.link and e.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Space):
            self.opened.emit()
            return
        super().keyPressEvent(e)

    def paintEvent(self, e):
        super().paintEvent(e)
        from .icons import draw_icon
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        if self.link and self._hover:
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(30, 50, 100, 10))
            p.drawRoundedRect(QRectF(self.rect()).adjusted(6, 2, -6, -2), 10, 10)
        tile = mirrored(self, QRectF(16, self.height() / 2 - 16, 32, 32))
        p.setPen(Qt.NoPen)
        p.setBrush(self.color)
        p.drawRoundedRect(tile, 9, 9)
        draw_icon(p, self.glyph, tile.center().x(), tile.center().y(), 18, QColor("white"))
        if self.link:
            at = mirrored(self, QRectF(self.width() - 22, self.height() / 2, 0, 0))
            p.save()
            p.translate(at.x(), at.y())
            if self.layoutDirection() == Qt.RightToLeft:
                p.scale(-1, 1)                          # « go there » points left
            draw_icon(p, "chevron", 0, 0, 12, QColor(MUTED))
            p.restore()
            if self.show_focus():
                focus_ring(p, QRectF(self.rect()).adjusted(6, 4, -6, -4), 10)


class _SignTile(QLabel):
    """The signature on a sheet of paper."""

    def __init__(self):
        super().__init__()
        self.setFixedHeight(110)
        self.setAlignment(Qt.AlignCenter)
        self.setWordWrap(True)
        self.setMargin(16)
        self.setStyleSheet(f"background:#FFFFFF;border:1px solid #DCE2EC;border-radius:12px;"
                           f"color:{MUTED};font-size:12px;")


PAGES = [  # (key, label, glyph, tile colour); the label is shown with tr()
    ("general", N_("Général"), "gear", "#2E7CF6"),
    ("hotkey", N_("Raccourci clavier"), "keyboard", "#5B5CE6"),
    ("menu", N_("Clic droit"), "menu", "#0EA5B7"),
    ("files", N_("Fichiers créés"), "folder", "#F29A13"),
    ("signature", N_("Signature"), "pen", "#8B5CF6"),
    ("quality", N_("Qualité"), "sliders", "#12A87E"),
    ("about", N_("À propos"), "info", "#64748B"),
]

AUTO_LANGUAGE = "auto"


class SettingsWindow(QWidget):
    changed = Signal(str)            # the setting that just changed (already saved)
    capturing = Signal(bool)         # recording a shortcut: pause the current one
    draw_signature = Signal()
    quit_requested = Signal()
    uninstall_requested = Signal()   # macOS: take Cerclic out of the Finder and login

    def __init__(self, settings: Settings, windows_11: bool = False,
                 welcome: bool = False, classic_enabled: bool = False,
                 store: bool = False):
        super().__init__(None, Qt.Window)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.s = settings
        self.windows_11 = windows_11
        self.welcome = welcome
        self.store = store                # the Microsoft Store version
        self.setWindowTitle("Cerclic")
        from .logo import make_icon
        self.setWindowIcon(make_icon(64))
        self.setMinimumSize(780, 540)
        self.setStyleSheet(BUTTON_QSS + FOCUS_QSS + f"QLabel{{color:{TEXT};}}")

        self.backdrop = Backdrop(self)
        root = QHBoxLayout(self)
        root.setContentsMargins(14, 14, 14, 14)
        root.setSpacing(14)

        # --- sidebar ---
        side = GlassPanel(radius=18, alpha=118, shadow=True)
        side.setFixedWidth(232)
        sl = QVBoxLayout(side)
        sl.setContentsMargins(12, 18, 12, 14)
        sl.setSpacing(2)
        brand = QHBoxLayout()
        brand.setContentsMargins(8, 0, 0, 10)
        from .logo import logo_pixmap
        logo = QLabel()
        logo.setPixmap(logo_pixmap(96).scaled(36, 36, Qt.KeepAspectRatio,
                                              Qt.SmoothTransformation))
        logo.setStyleSheet("background:transparent;")
        brand.addWidget(logo)
        names = QVBoxLayout()
        names.setSpacing(0)
        names.addWidget(label("Cerclic", "row"))
        names.addWidget(label(self._version_text(), "faint"))
        brand.addLayout(names, 1)
        sl.addLayout(brand)
        self.nav: dict[str, NavItem] = {}
        group = QButtonGroup(self)
        for key, text, glyph, color in PAGES:
            item = NavItem(tr(text), glyph, color)
            group.addButton(item)
            item.clicked.connect(lambda _=False, k=key: self.show_page(k))
            sl.addWidget(item)
            self.nav[key] = item
        sl.addStretch(1)
        sl.addWidget(label(tr("Les changements s'appliquent aussitôt."), "faint"))
        root.addWidget(side)

        # --- pages ---
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("QStackedWidget{background:transparent;}")
        root.addWidget(self.stack, 1)
        self.pages: dict[str, _Page] = {}
        self._build_general(welcome, windows_11 and not classic_enabled)
        self._build_hotkey()
        self._build_menu(windows_11, classic_enabled)
        self._build_files()
        self._build_signature()
        self._build_quality()
        self._build_about()

        self.refresh_signature()
        self._apply_hotkey_status(None)
        # Cmd + W (macOS) or Ctrl + F4 closes the window; not while a shortcut is
        # being recorded (the combination belongs to the recording then).
        self._close_key = QShortcut(QKeySequence(QKeySequence.Close), self, self.close)
        self.shortcut.capturing.connect(lambda on: self._close_key.setEnabled(not on))
        self.resize(900, 640)
        self.show_page("general")

    # -- structure --------------------------------------------------------------------
    def _page(self, key: str, title: str, subtitle: str) -> _Page:
        page = _Page(title, subtitle)
        self.pages[key] = page
        self.stack.addWidget(page)
        return page

    def show_page(self, key: str) -> None:
        if key in self.pages:
            self.stack.setCurrentWidget(self.pages[key])
            self.nav[key].setChecked(True)

    def current_page(self) -> str:
        shown = self.stack.currentWidget()
        return next((k for k, page in self.pages.items() if page is shown), "general")

    def resizeEvent(self, e):
        self.backdrop.setGeometry(self.rect())
        self.backdrop.lower()
        super().resizeEvent(e)

    def _version_text(self) -> str:
        if self.store:
            return tr("Version {version} · Microsoft Store", version=__version__)
        return tr("Version {version}", version=__version__)

    # -- Général -----------------------------------------------------------------------
    def _how_keyboard(self) -> str:
        if IS_MAC:
            return tr("Sélectionne un ou plusieurs fichiers dans le Finder ou sur le Bureau, "
                      "puis appuie sur {combo}.", combo=self._combo_label())
        return tr("Sélectionne un ou plusieurs fichiers dans l'Explorateur ou sur le Bureau, "
                  "puis appuie sur {combo}.", combo=self._combo_label())

    def _combo_label(self) -> str:
        return hk.label(int(self.s.get("hotkey_mods")), int(self.s.get("hotkey_vk")))

    def _build_general(self, welcome: bool, win11_menu: bool) -> None:
        page = self._page("general", tr("Général"),
                          tr("Deux façons d'ouvrir la roue, le démarrage et la langue.")
                          if self.store else
                          tr("Trois façons d'ouvrir la roue, le démarrage et la langue."))
        if welcome:
            page.add(_Banner(
                tr("Cerclic tourne maintenant en arrière-plan : son icône est dans la barre "
                   "des menus, en haut de l'écran. Choisis ci-dessous ta façon préférée "
                   "d'ouvrir la roue.") if IS_MAC else
                tr("Cerclic tourne maintenant en arrière-plan : son icône est près de "
                   "l'horloge (parfois cachée sous la petite flèche ^). Choisis ci-dessous "
                   "ta façon préférée d'ouvrir la roue.")))
        ways = Group(tr("Ouvrir la roue"))
        self.way_keyboard = ways.add(_Way("keyboard", "#5B5CE6", tr("Au clavier"),
                                          self._how_keyboard(), link=True,
                                          tip=tr("Régler : au clavier")))
        self.way_keyboard.opened.connect(lambda: self.show_page("hotkey"))
        if IS_MAC:
            mouse = tr("Clic droit sur le fichier, Actions rapides, puis « Cerclic ». "
                       "Ou : Ouvrir avec, puis Cerclic.")
        elif win11_menu:
            mouse = tr("Maj + clic droit sur le fichier, puis « Cerclic ». Sans Maj, passe "
                       "par « Afficher d'autres options ».")
        else:
            mouse = tr("Clic droit sur le fichier, puis « Cerclic ».")
        self.way_mouse = ways.add(_Way("mouse", "#0EA5B7", tr("À la souris"), mouse,
                                       link=True, tip=tr("Régler : à la souris")))
        self.way_mouse.opened.connect(lambda: self.show_page("menu"))
        if not self.store:          # (no icon to drop files on: Start opens the app)
            ways.add(_Way("drop", "#7A8497", tr("En glissant"),
                          tr("Glisse des fichiers sur l'icône de Cerclic (dans Applications "
                             "ou le Dock).") if IS_MAC else
                          tr("Glisse des fichiers sur l'icône de Cerclic.")))
        page.add(group_block(ways))

        start = Group(tr("Démarrage"))
        self.autostart = Toggle(tr("Lancer Cerclic avec le Mac") if IS_MAC
                                else tr("Lancer Cerclic avec Windows"))
        self.autostart.setChecked(bool(self.s.get("autostart")))
        self.autostart.toggled.connect(lambda on: self._set("autostart", on))
        start.add(Row(tr("Ouvrir Cerclic à l'ouverture de session") if IS_MAC else
                      tr("Lancer Cerclic avec Windows"),
                      tr("Recommandé : la roue est prête dès que tu en as besoin."),
                      self.autostart))
        if IS_MAC:
            again = tr("Arrête Cerclic. Pour le relancer, ouvre-le depuis le dossier "
                       "Applications.")
        elif self.store:
            again = tr("Arrête Cerclic. Pour le relancer, ouvre-le depuis le menu Démarrer.")
        else:
            again = tr("Arrête Cerclic. Pour le relancer, ouvre-le depuis le Bureau ou le "
                       "menu Démarrer.")
        quit_btn = _button(tr("Quitter Cerclic"), "", again)
        quit_btn.clicked.connect(self.quit_requested.emit)
        start.add(Row(tr("Arrêter Cerclic"), tr("La roue ne s'ouvrira plus jusqu'au "
                                                 "prochain lancement."), quit_btn))
        page.add(group_block(start))

        langs = Group()
        self.language = Select()
        self.language.setAccessibleName(tr("Langue"))
        self.language.addItem(tr("Automatique (langue de l'ordinateur)"), AUTO_LANGUAGE)
        for code, name in i18n.LANGS.items():       # each in its own language
            self.language.addItem(name, code)
        chosen = self.language.findData(self.s.get("language"))
        self.language.setCurrentIndex(max(0, chosen))
        self.language.activated.connect(self._language_chosen)
        langs.add(Row(tr("Langue"), tr("Celle des menus, des fenêtres et des messages de "
                                       "Cerclic."), self.language))
        page.add(group_block(langs))
        page.finish()

    def _language_chosen(self, index: int) -> None:
        """Applies at once: saved, then in use (the app builds this window again
        in the new language, see app.py)."""
        code = self.language.itemData(index) or AUTO_LANGUAGE
        if code == self.s.get("language"):
            return
        self._set("language", code)
        i18n.set_language(code)

    def _confirm_uninstall(self) -> None:
        from PySide6.QtWidgets import QMessageBox
        box = QMessageBox(QMessageBox.Question, tr("Désinstaller Cerclic"),
                          tr("Retirer Cerclic du clic droit et de l'ouverture de session, "
                             "puis le quitter ?"), QMessageBox.NoButton, self)
        yes = box.addButton(tr("Désinstaller"), QMessageBox.AcceptRole)
        box.setDefaultButton(box.addButton(tr("Annuler"), QMessageBox.RejectRole))
        box.exec()
        if box.clickedButton() is yes:
            self.uninstall_requested.emit()

    def _open_automation(self) -> None:
        from ..mac.integration import open_automation_settings
        open_automation_settings()

    # -- Raccourci clavier ---------------------------------------------------------------
    def _build_hotkey(self) -> None:
        page = self._page("hotkey", tr("Raccourci clavier"),
                          tr("Une combinaison de touches ouvre la roue sur les fichiers "
                             "sélectionnés."))
        g = Group()
        self.hotkey_on = Toggle(tr("Ouvrir la roue au clavier"))
        self.hotkey_on.setChecked(bool(self.s.get("hotkey")))
        self.hotkey_on.toggled.connect(self._hotkey_toggled)
        g.add(Row(tr("Ouvrir la roue au clavier"),
                  tr("Sur les fichiers sélectionnés dans le Finder ou sur le Bureau.")
                  if IS_MAC else
                  tr("Sur les fichiers sélectionnés dans l'Explorateur ou sur le Bureau."),
                  self.hotkey_on))
        self.shortcut = ShortcutEdit(int(self.s.get("hotkey_mods")),
                                     int(self.s.get("hotkey_vk")))
        self.shortcut.chosen.connect(self._combo_chosen)
        self.shortcut.capturing.connect(self.capturing.emit)
        self.shortcut.setEnabled(self.hotkey_on.isChecked())
        holder = QWidget()
        holder.setAttribute(Qt.WA_TranslucentBackground)
        hl = QVBoxLayout(holder)
        hl.setContentsMargins(16, 4, 16, 14)
        hl.addWidget(self.shortcut)
        g.add(holder)
        if IS_MAC:
            notes = (tr("« Modifier », puis appuie sur ta combinaison. Si elle est déjà prise "
                        "par macOS ou une autre application, Cerclic te le dit et garde "
                        "l'ancienne."),
                     tr("Une souris à boutons programmables ? Règle un bouton sur une touche "
                        "F13 à F20, puis choisis-la ici : un clic sur ce bouton ouvrira la "
                        "roue."))
        else:
            notes = (tr("« Modifier », puis appuie sur ta combinaison. Si elle est déjà prise "
                        "par Windows ou une autre application, Cerclic te le dit et garde "
                        "l'ancienne."),
                     tr("Une souris à boutons programmables ? Règle un bouton sur une touche "
                        "F13 à F24, puis choisis-la ici : un clic sur ce bouton ouvrira la "
                        "roue."))
        page.add(group_block(g, notes=notes))
        if IS_MAC:
            mac = Group(tr("Autorisation"))
            allow = _button(tr("Réglages…"))
            allow.clicked.connect(self._open_automation)
            mac.add(Row(tr("Lire la sélection du Finder"),
                        tr("La première fois, macOS demande si Cerclic peut contrôler le "
                           "Finder : accepte. Cerclic y lit seulement les fichiers "
                           "sélectionnés."), allow))
            page.add(group_block(mac, notes=(
                tr("Refusé par erreur ? Dans Automatisation, coche « Finder » sous "
                   "Cerclic."),)))
        page.finish()

    # -- Clic droit ---------------------------------------------------------------------------
    def _build_menu(self, windows_11: bool, classic_enabled: bool) -> None:
        page = self._page("menu", tr("Clic droit"),
                          tr("« Cerclic » dans le menu du clic droit de tes fichiers."))
        g = Group()
        self.context_menu = Toggle(tr("« Cerclic » dans le clic droit"))
        self.context_menu.setChecked(bool(self.s.get("context_menu")))
        self.context_menu.toggled.connect(lambda on: self._set("context_menu", on))
        if IS_MAC:
            g.add(Row(tr("« Cerclic » dans le clic droit du Finder"),
                      tr("Dans le menu Actions rapides de tes fichiers, dans le Finder et sur "
                         "le Bureau."), self.context_menu))
        elif self.store:
            g.add(Row(tr("« Cerclic » dans le clic droit des fichiers"),
                      tr("En haut du menu des images, PDF, vidéos et sons, dans "
                         "l'Explorateur et sur le Bureau."), self.context_menu))
        else:
            g.add(Row(tr("« Cerclic » dans le clic droit des fichiers"),
                      tr("Sur les images, PDF, vidéos et sons, dans l'Explorateur, sur le "
                         "Bureau et dans les fenêtres Ouvrir et Enregistrer."),
                      self.context_menu))
        self.classic = None
        if windows_11 and not IS_MAC:
            self.classic = Toggle(tr("Menu clic droit complet"))
            self.classic.setChecked(classic_enabled)
            self.classic.toggled.connect(lambda on: self.changed.emit("classic_menu"))
            g.add(Row(tr("Menu clic droit complet"),
                      tr("Affiche le menu complet sans passer par « Afficher d'autres "
                         "options ». Cerclic proposera de redémarrer l'Explorateur."),
                      self.classic))
        if IS_MAC:
            notes = (tr("Pas dans Actions rapides ? Clic droit sur un fichier, Actions "
                        "rapides puis Personnaliser, et coche « Cerclic ». Il est aussi "
                        "toujours dans Ouvrir avec."),)
        elif windows_11:
            notes = (tr("Astuce : sans rien changer, Maj + clic droit sur un fichier ouvre "
                        "directement le menu complet, avec « Cerclic »."),)
        else:
            notes = ()
        page.add(group_block(g, notes=notes))
        page.finish()

    # -- Fichiers créés ----------------------------------------------------------------------
    def _build_files(self) -> None:
        page = self._page("files", tr("Fichiers créés"),
                          tr("Ton fichier d'origine n'est jamais modifié : chaque action crée "
                             "un nouveau fichier."))
        g = Group(tr("Où les enregistrer"))
        box = QWidget()
        box.setAttribute(Qt.WA_TranslucentBackground)
        bl = QVBoxLayout(box)
        bl.setContentsMargins(16, 14, 16, 14)
        bl.setSpacing(10)
        self.out_beside = Choice(tr("À côté du fichier d'origine"),
                                 tr("Dans le même dossier, par exemple sur le Bureau si la "
                                    "photo y est. Recommandé."))
        self.out_folder = Choice(tr("Dans un dossier de mon choix"),
                                 tr("Tous les fichiers créés au même endroit."))
        self.out_ask = Choice(tr("Me demander à chaque fois"),
                              tr("Cerclic te demande le dossier avant de créer le fichier."))
        mode = self.s.get("output_mode")
        {"folder": self.out_folder, "ask": self.out_ask}.get(
            mode, self.out_beside).setChecked(True)
        self.out_beside.picked.connect(lambda: self._set_output("beside"))
        self.out_folder.picked.connect(lambda: self._set_output("folder"))
        self.out_ask.picked.connect(lambda: self._set_output("ask"))
        bl.addWidget(self.out_beside)
        bl.addWidget(self.out_folder)
        row = QHBoxLayout()
        row.setContentsMargins(38, 0, 0, 0)
        self.folder_label = label("", "desc")
        row.addWidget(self.folder_label, 1)
        self.pick_btn = _button(tr("Choisir…"))
        self.pick_btn.clicked.connect(self._pick_folder)
        self.open_btn = _button(tr("Ouvrir"), "ghost")
        self.open_btn.clicked.connect(self._open_folder)
        row.addWidget(self.pick_btn)
        row.addWidget(self.open_btn)
        bl.addLayout(row)
        bl.addWidget(self.out_ask)
        g.add(box)
        page.add(group_block(g, notes=(
            tr("Leur nom : le nom d'origine, plus ce qui a changé, par exemple "
               "photo (compressé).jpg à côté de photo.jpg. Si ce nom est déjà pris, Cerclic "
               "ajoute un numéro : rien n'est jamais écrasé."),
            tr("Un résultat ne te plaît pas ? « Supprimer » sur sa carte l'efface "
               "aussitôt."))))
        page.finish()
        self._refresh_output()

    def _refresh_output(self) -> None:
        folder = self.s.get("output_folder") or ""
        on = self.out_folder.isChecked()
        if on and folder:
            self.folder_label.setText(folder)
        elif on:
            self.folder_label.setText(tr("Aucun dossier choisi."))
        elif folder:
            self.folder_label.setText(tr("Dossier de ton choix : {folder}", folder=folder))
        else:
            self.folder_label.setText(tr("Dossier de ton choix : aucun pour l'instant."))
        self.pick_btn.setEnabled(True)
        self.open_btn.setVisible(bool(folder) and os.path.isdir(folder))

    def _set_output(self, mode: str) -> None:
        if mode == "folder" and not self.s.get("output_folder"):
            if not self._pick_folder():             # no folder chosen: as before
                mode = self.s.get("output_mode")
                {"folder": self.out_folder, "ask": self.out_ask}.get(
                    mode, self.out_beside).setChecked(True)
        self._set("output_mode", mode)
        self._refresh_output()

    def _pick_folder(self) -> bool:
        from .signature import pictures_folder
        start = self.s.get("output_folder") or pictures_folder()
        folder = QFileDialog.getExistingDirectory(self, tr("Dossier des fichiers créés"),
                                                  start)
        if not folder:
            return False
        self.s.set("output_folder", os.path.normpath(folder))
        self.out_folder.setChecked(True)
        self._set("output_mode", "folder")
        self._refresh_output()
        return True

    def _open_folder(self) -> None:
        folder = self.s.get("output_folder")
        if folder and os.path.isdir(folder):
            from .cards import open_path
            open_path(folder)

    # -- Signature ----------------------------------------------------------------------------
    def _build_signature(self) -> None:
        page = self._page("signature", tr("Signature"),
                          tr("Pour signer tes PDF en un geste. Elle reste sur cet "
                             "ordinateur."))
        g = Group()
        box = QWidget()
        box.setAttribute(Qt.WA_TranslucentBackground)
        bl = QVBoxLayout(box)
        bl.setContentsMargins(16, 16, 16, 14)
        bl.setSpacing(12)
        self.sign_preview = _SignTile()
        bl.addWidget(self.sign_preview)
        row = QHBoxLayout()
        draw = _button(tr("Dessiner…"))
        draw.clicked.connect(self.draw_signature.emit)
        imp = _button(tr("Importer une photo…"))
        imp.clicked.connect(self._import_signature)
        self.clear_sig = _button(tr("Effacer"), "danger")
        self.clear_sig.clicked.connect(self._clear_signature)
        row.addWidget(draw)
        row.addWidget(imp)
        row.addStretch(1)
        row.addWidget(self.clear_sig)
        bl.addLayout(row)
        g.add(box)
        page.add(group_block(g, notes=(
            tr("Une photo de ta signature sur papier blanc suffit : Cerclic rend le papier "
               "transparent et garde l'encre."),
            tr("Pour signer : clic droit ou raccourci sur un PDF, puis « Signer ». Place la "
               "signature et appuie sur {key}.", key=tr(ENTER_KEY)))))
        page.finish()

    # -- Qualité ------------------------------------------------------------------------------
    def _build_quality(self) -> None:
        page = self._page("quality", tr("Qualité"),
                          tr("Le juste milieu entre le poids des fichiers et leur netteté."))
        g = Group()
        self.compress_q = _slider(10, 95, self.s.get("compress_quality"))
        self.compress_val = label("", "row")
        self.compress_q.valueChanged.connect(self._quality_changed)
        g.add(Row(tr("Compression des images"),
                  tr("Réglage proposé par « Compresser », qui montre la taille obtenue et "
                     "retient ton dernier choix."),
                  self.compress_val, below=_scale(self.compress_q)))
        self.jpg_q = _slider(50, 100, self.s.get("jpg_quality"))
        self.jpg_val = label("", "row")
        self.jpg_q.valueChanged.connect(self._quality_changed)
        g.add(Row(tr("JPG créés par les autres actions"),
                  tr("Rogner, pivoter, convertir… À 90 %, la perte ne se voit pas."),
                  self.jpg_val, below=_scale(self.jpg_q)))
        reset = _button(tr("Par défaut"), "ghost")
        reset.clicked.connect(self._quality_defaults)
        line = QWidget()
        line.setAttribute(Qt.WA_TranslucentBackground)
        ll = QHBoxLayout(line)
        ll.setContentsMargins(16, 0, 10, 4)
        ll.addStretch(1)
        ll.addWidget(reset)
        g.add(line)
        page.add(group_block(g))
        page.finish()
        self._quality_changed()

    def _quality_changed(self, *_):
        cq, jq = self.compress_q.value(), self.jpg_q.value()
        self.compress_val.setText(tr("{value} %", value=cq))
        self.jpg_val.setText(tr("{value} %", value=jq))
        if cq != self.s.get("compress_quality"):
            self._set("compress_quality", cq)
        if jq != self.s.get("jpg_quality"):
            self._set("jpg_quality", jq)

    def _quality_defaults(self) -> None:
        from ..settings import DEFAULTS
        self.compress_q.setValue(DEFAULTS["compress_quality"])
        self.jpg_q.setValue(DEFAULTS["jpg_quality"])

    # -- À propos -----------------------------------------------------------------------------
    def _build_about(self) -> None:
        page = self._page("about", tr("À propos"), "")
        hero = GlassPanel(radius=18, alpha=190)
        hl = QHBoxLayout(hero)
        hl.setContentsMargins(22, 20, 22, 24)
        hl.setSpacing(18)
        from .logo import logo_pixmap
        logo = QLabel()
        logo.setPixmap(logo_pixmap(192).scaled(72, 72, Qt.KeepAspectRatio,
                                               Qt.SmoothTransformation))
        logo.setStyleSheet("background:transparent;")
        hl.addWidget(logo)
        texts = QVBoxLayout()
        texts.setSpacing(3)
        texts.addWidget(label("Cerclic", "title"))
        texts.addWidget(label(self._version_text(), "desc"))
        texts.addWidget(label(tr("Rogner, signer, compresser, convertir, mettre au format "
                                 "des réseaux sociaux… en un geste, sans ouvrir d'autre "
                                 "application."), "desc"))
        hl.addLayout(texts, 1)
        page.add(hero)
        g = Group()
        log_btn = _button(tr("Ouvrir"))
        log_btn.clicked.connect(self._open_log)
        g.add(Row(tr("Journal"), tr("En cas de souci, ce fichier aide à comprendre ce qui "
                                    "s'est passé."), log_btn))
        lic_btn = _button(tr("Voir"))
        lic_btn.clicked.connect(self._open_licences)
        g.add(Row(tr("Licences"),
                  tr("Les composants libres qu'utilise Cerclic et leurs licences."), lic_btn))
        if IS_MAC:
            remove = _button(tr("Désinstaller…"))
            remove.clicked.connect(self._confirm_uninstall)
            g.add(Row(tr("Désinstaller Cerclic"),
                      tr("Retire « Cerclic » du clic droit et de l'ouverture de session, puis "
                         "quitte. Il restera à mettre Cerclic.app à la corbeille."), remove))
        page.add(group_block(g))
        page.finish()

    def _open_log(self) -> None:
        from ..log import log_path
        from .cards import open_path, reveal_path
        path = log_path()
        if os.path.exists(path):
            reveal_path(path)
        else:
            open_path(os.path.dirname(path))

    def _open_licences(self) -> None:
        from .cards import open_path
        base = (os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else
                os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
                    os.path.abspath(__file__)))), "assets"))
        for cand in (os.path.join(base, "LICENCES.txt"),
                     os.path.join(getattr(sys, "_MEIPASS", base), "LICENCES.txt")):
            if os.path.exists(cand):
                open_path(cand)
                return

    # -- placing -----------------------------------------------------------------------
    def show_centered(self, near: QPoint | None = None) -> None:
        screen = (QGuiApplication.screenAt(near) if near is not None else None) \
            or QGuiApplication.primaryScreen()
        avail = screen.availableGeometry()
        w = min(self.width(), int(avail.width() * 0.94))
        h = min(self.height(), int(avail.height() * 0.92))
        self.resize(w, h)
        self.move(avail.center().x() - w // 2, avail.center().y() - h // 2)
        self.show()
        self.raise_()
        self.activateWindow()
        from ..win.foreground import bring_to_front
        bring_to_front(int(self.winId()))

    # -- values ------------------------------------------------------------------------
    def _set(self, key: str, value) -> None:
        self.s.set(key, value)
        self.s.save()
        self.changed.emit(key)

    def _hotkey_toggled(self, on: bool) -> None:
        self.shortcut.setEnabled(on)
        if not on:
            self.shortcut.stop_recording()
        self._set("hotkey", on)

    def _combo_chosen(self, mods: int, vk: int) -> None:
        self.s.set("hotkey_mods", int(mods))
        self.s.set("hotkey_vk", int(vk))
        self.s.save()
        self.shortcut.set_combo(mods, vk)
        if hasattr(self, "way_keyboard"):
            self.way_keyboard.text.setText(self._how_keyboard())
        self.changed.emit("hotkey_combo")

    def set_hotkey_status(self, ok: bool | None, note: str = "") -> None:
        """What the app learnt when registering the shortcut."""
        if note:
            self.shortcut.set_status(note, "error")
            return
        self._apply_hotkey_status(ok)

    def show_combo(self, mods: int, vk: int) -> None:
        self.shortcut.set_combo(mods, vk)
        if hasattr(self, "way_keyboard"):
            self.way_keyboard.text.setText(self._how_keyboard())

    def _apply_hotkey_status(self, ok: bool | None) -> None:
        if not self.hotkey_on.isChecked():
            self.shortcut.set_status(
                tr("Raccourci désactivé : le clic droit « Cerclic » reste disponible.")
                if self.context_menu.isChecked() else tr("Raccourci désactivé."))
        elif ok is None:
            self.shortcut.set_status("")
        elif ok:
            self.shortcut.set_status(tr("✓ Actif partout sur le Mac.") if IS_MAC
                                     else tr("✓ Actif partout dans Windows."), "ok")
        elif IS_MAC:
            self.shortcut.set_status(tr("macOS ou une autre application utilise déjà cette "
                                        "combinaison. Choisis-en une autre avec "
                                        "« Modifier »."), "error")
        else:
            self.shortcut.set_status(tr("Windows ou une autre application utilise déjà "
                                        "cette combinaison. Choisis-en une autre avec "
                                        "« Modifier »."), "error")

    def set_autostart(self, on: bool) -> None:
        """What Windows says about starting with it (Microsoft Store version:
        the user may also change it in Task Manager)."""
        self.autostart.blockSignals(True)
        self.autostart.setChecked(on)
        self.autostart.blockSignals(False)

    def classic_choice(self) -> bool | None:
        return None if self.classic is None else self.classic.isChecked()

    def set_classic(self, on: bool) -> None:
        if self.classic is not None:
            self.classic.blockSignals(True)
            self.classic.setChecked(on)
            self.classic.blockSignals(False)

    # -- signature ---------------------------------------------------------------------
    def refresh_signature(self) -> None:
        path = self.s.get("signature")
        if path and os.path.exists(path):
            pix = QPixmap(path)
            if not pix.isNull():
                self.sign_preview.setPixmap(
                    pix.scaled(420, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.clear_sig.setVisible(True)
                return
        self.clear_sig.setVisible(False)              # nothing to erase
        self.sign_preview.setPixmap(QPixmap())
        from .glass import french
        self.sign_preview.setText(french(tr("Aucune signature pour l'instant : dessine-la "
                                            "ou importe une photo. Sinon, elle te sera "
                                            "demandée la première fois que tu signes.")))

    def _import_signature(self) -> None:
        from .signature import pictures_folder
        src, _ = QFileDialog.getOpenFileName(
            self, tr("Choisir une photo de ta signature"), pictures_folder(),
            tr("Images") + " (*.png *.jpg *.jpeg *.webp *.heic *.bmp)")
        if not src:
            return
        from .signature import import_signature, signature_path
        try:
            path = import_signature(src, signature_path())
        except Exception as exc:
            self.sign_preview.setPixmap(QPixmap())
            self.sign_preview.setText(str(exc) if isinstance(exc, ValueError)
                                      else tr("Image illisible."))
            return
        self._set("signature", path)
        self.refresh_signature()

    def _clear_signature(self) -> None:
        """Forget the signature, and erase the picture Cerclic kept of it."""
        path = self.s.get("signature")
        from ..settings import config_dir
        base = os.path.normcase(os.path.abspath(config_dir()))
        mine = bool(path) and os.path.normcase(os.path.abspath(path)).startswith(base + os.sep)
        if path and mine and os.path.isfile(path):
            try:
                os.remove(path)
            except OSError:
                pass
        self._set("signature", "")
        self.refresh_signature()

    def closeEvent(self, e):
        self.shortcut.stop_recording()
        super().closeEvent(e)
