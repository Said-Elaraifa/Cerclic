"""Cerclic's own window: how to open the wheel, the keyboard shortcut (record
any combination), the right-click entry, the signature, quality and startup.

It opens when Cerclic is launched from its icon (Desktop, Start menu) or from
the tray icon. Every change applies at once; there is nothing to save.
"""
from __future__ import annotations

import os
import sys

from PySide6.QtCore import QPoint, QRectF, QSize, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QFont, QGuiApplication, QPainter, QPixmap
from PySide6.QtWidgets import (QCheckBox, QFileDialog, QFrame, QHBoxLayout, QLabel,
                               QPushButton, QScrollArea, QSpinBox, QVBoxLayout,
                               QWidget)

from .. import __version__
from ..settings import Settings
from ..win import hotkey as hk
from .theme import (ACCENT, BG, BORDER, BUTTON_QSS, ERROR, FONT_FAMILY, MUTED, OK,
                    SURFACE, SURFACE_2, TEXT)

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
    """(Windows modifier flags, virtual key) of a key press; vk 0 while only
    modifiers are held. On Windows the physical key is used, so the digits of
    an AZERTY keyboard count as digits."""
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
        self.setMinimumHeight(38)

    def set_parts(self, parts: list[str], placeholder: str = "") -> None:
        self.parts, self.placeholder = parts, placeholder
        self.updateGeometry()
        self.update()

    def sizeHint(self) -> QSize:
        return QSize(260, 38)

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        f = QFont(FONT_FAMILY)
        f.setPixelSize(13)
        f.setBold(True)
        p.setFont(f)
        fm = p.fontMetrics()
        x, h = 2.0, 30.0
        y = (self.height() - h) / 2
        if not self.parts:
            p.setPen(QColor(ACCENT if self.active else MUTED))
            f.setBold(False)
            p.setFont(f)
            p.drawText(QRectF(4, 0, self.width() - 4, self.height()),
                       Qt.AlignVCenter | Qt.AlignLeft, self.placeholder)
            return
        for i, part in enumerate(self.parts):
            w = max(34.0, fm.horizontalAdvance(part) + 22.0)
            r = QRectF(x, y, w, h)
            p.setPen(QColor(ACCENT) if self.active else QColor("#3A3F4E"))
            p.setBrush(QColor("#2A2E3A"))
            p.drawRoundedRect(r.adjusted(0, 0, 0, -1), 7, 7)
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(0, 0, 0, 70))
            p.drawRoundedRect(QRectF(r.left() + 1, r.bottom() - 4, r.width() - 2, 4), 3, 3)
            p.setPen(QColor(TEXT))
            p.drawText(r.adjusted(0, -2, 0, -2), Qt.AlignCenter, part)
            x += w
            if i < len(self.parts) - 1:
                p.setPen(QColor(MUTED))
                p.drawText(QRectF(x, y, 18, h), Qt.AlignCenter, "+")
                x += 18


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
        self.change_btn = QPushButton("Modifier")
        self.change_btn.setFocusPolicy(Qt.NoFocus)      # keep the recording focused
        self.change_btn.clicked.connect(self.toggle_recording)
        self.default_btn = QPushButton("Par défaut")
        self.default_btn.setObjectName("ghost")
        self.default_btn.setFocusPolicy(Qt.NoFocus)
        self.default_btn.clicked.connect(self._default)
        row.addWidget(self.change_btn)
        row.addWidget(self.default_btn)
        lay.addLayout(row)
        self.status = QLabel("")
        self.status.setWordWrap(True)
        self.status.setObjectName("status")
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
        self.status.setStyleSheet(f"color:{color};font-size:12px;")
        self.status.setText(text)

    def toggle_recording(self) -> None:
        if self.recording:
            self.stop_recording("Raccourci inchangé.")
        else:
            self.start_recording()

    def start_recording(self) -> None:
        self.recording = True
        self.change_btn.setText("Annuler")
        self.caps.active = True
        self.caps.set_parts([], "Appuie sur ta combinaison…")
        self.set_status("Exemples : Ctrl + Alt + Espace, Ctrl + Maj + X, Win + Maj + C, "
                        "F8. Échap pour annuler.", "accent")
        self.setFocus(Qt.OtherFocusReason)
        self.grabKeyboard()
        self.capturing.emit(True)

    def stop_recording(self, message: str = "") -> None:
        if not self.recording:
            return
        self.recording = False
        self.releaseKeyboard()
        self.change_btn.setText("Modifier")
        self._show_combo()
        if message:
            self.set_status(message, "muted")
        self.capturing.emit(False)

    def _default(self) -> None:
        self.stop_recording()
        self.chosen.emit(hk.DEFAULT_MODS, hk.DEFAULT_VK)

    def keyPressEvent(self, e):
        if not self.recording:
            return super().keyPressEvent(e)
        mods, vk = combo_from_event(e)
        if vk == 0x1B and not mods:
            self.stop_recording("Raccourci inchangé.")
            return
        if not vk:
            parts = hk.label(mods, 0).split(" + ")[:-1] if mods else []
            self.caps.set_parts(parts + ["…"] if parts else [],
                                "Appuie sur ta combinaison…")
            return
        problem = hk.check(mods, vk)
        if problem:
            self.caps.set_parts(hk.label(mods, vk).split(" + "))
            self.set_status(problem, "error")
            return
        self.mods, self.vk = mods, vk
        self.recording = False
        self.releaseKeyboard()
        self.change_btn.setText("Modifier")
        self._show_combo()
        self.set_status("Vérification…", "muted")
        self.chosen.emit(mods, vk)          # saved first: then the pause ends
        self.capturing.emit(False)

    def keyReleaseEvent(self, e):
        if self.recording:
            m = e.modifiers()
            if not (m & (Qt.ControlModifier | Qt.AltModifier | Qt.ShiftModifier
                         | Qt.MetaModifier)):
                self.caps.set_parts([], "Appuie sur ta combinaison…")
            return
        super().keyReleaseEvent(e)

    def focusOutEvent(self, e):
        super().focusOutEvent(e)
        if self.recording:
            QTimer.singleShot(0, lambda: self.recording and not self.hasFocus()
                              and self.stop_recording("Raccourci inchangé."))


# ----- the window ---------------------------------------------------------------------------

def _section(title: str) -> tuple[QFrame, QVBoxLayout]:
    box = QFrame()
    box.setObjectName("section")
    lay = QVBoxLayout(box)
    lay.setContentsMargins(16, 12, 16, 14)
    lay.setSpacing(8)
    head = QLabel(title)
    head.setObjectName("sectionTitle")
    lay.addWidget(head)
    return box, lay


def _hint(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setWordWrap(True)
    lbl.setObjectName("hint")
    return lbl


def _spin(lo, hi, val, suffix=""):
    s = QSpinBox()
    s.setRange(lo, hi)
    s.setValue(int(val))
    if suffix:
        s.setSuffix(suffix)
    return s


class SettingsWindow(QWidget):
    changed = Signal(str)            # the setting that just changed (already saved)
    capturing = Signal(bool)         # recording a shortcut: pause the current one
    draw_signature = Signal()
    quit_requested = Signal()

    def __init__(self, settings: Settings, windows_11: bool = False,
                 welcome: bool = False, classic_enabled: bool = False):
        super().__init__(None, Qt.Window)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.s = settings
        self.setWindowTitle("Cerclic")
        from .trayicon import make_icon
        self.setWindowIcon(make_icon(64))

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        body = QWidget()
        body.setObjectName("body")
        scroll.setWidget(body)
        outer.addWidget(scroll, 1)
        root = QVBoxLayout(body)
        root.setContentsMargins(20, 18, 20, 12)
        root.setSpacing(12)

        # --- header ---
        head = QHBoxLayout()
        logo = QLabel()
        logo.setPixmap(make_icon(96).pixmap(48, 48))
        head.addWidget(logo)
        titles = QVBoxLayout()
        titles.setSpacing(0)
        name = QLabel("Cerclic")
        name.setObjectName("appName")
        tag = QLabel("Rogner, signer, compresser, convertir… en un geste.")
        tag.setObjectName("hint")
        titles.addWidget(name)
        titles.addWidget(tag)
        head.addLayout(titles, 1)
        root.addLayout(head)

        if welcome:
            hello = QLabel("Bienvenue ! Cerclic tourne maintenant en fond, à côté de "
                           "l'horloge. Sélectionne une image, un PDF, une vidéo ou un son, "
                           "puis appuie sur ton raccourci (ou fais un clic droit, puis "
                           "« Cerclic ») : la roue apparaît. Pour revenir ici, ouvre "
                           "Cerclic depuis le Bureau ou le menu Démarrer.")
            hello.setWordWrap(True)
            hello.setObjectName("welcome")
            root.addWidget(hello)

        # --- opening the wheel ---
        box, lay = _section("Ouvrir la roue")
        self.hotkey_on = QCheckBox("Raccourci clavier sur les fichiers sélectionnés")
        self.hotkey_on.setChecked(bool(settings.get("hotkey")))
        self.hotkey_on.toggled.connect(self._hotkey_toggled)
        lay.addWidget(self.hotkey_on)
        self.shortcut = ShortcutEdit(int(settings.get("hotkey_mods")),
                                     int(settings.get("hotkey_vk")))
        self.shortcut.chosen.connect(self._combo_chosen)
        self.shortcut.capturing.connect(self.capturing.emit)
        self.shortcut.setEnabled(self.hotkey_on.isChecked())
        lay.addWidget(self.shortcut)
        lay.addWidget(_hint("Dans l'Explorateur ou sur le Bureau : clique sur une image, "
                            "un PDF, une vidéo ou un son (ou en sélectionne plusieurs), "
                            "puis appuie sur le raccourci. La roue s'ouvre sous la souris."))
        sep = QFrame()
        sep.setObjectName("sep")
        sep.setFixedHeight(1)
        lay.addWidget(sep)
        self.context_menu = QCheckBox("« Cerclic » dans le clic droit des fichiers")
        self.context_menu.setChecked(bool(settings.get("context_menu")))
        self.context_menu.toggled.connect(lambda on: self._set("context_menu", on))
        lay.addWidget(self.context_menu)
        self.classic = None
        if windows_11:
            self.classic = QCheckBox("Menu clic droit complet (Cerclic sans « Afficher "
                                     "d'autres options »)")
            self.classic.setChecked(classic_enabled)
            self.classic.toggled.connect(lambda on: self.changed.emit("classic_menu"))
            lay.addWidget(self.classic)
            lay.addWidget(_hint("Windows 11 range les entrées des applications sous "
                                "« Afficher d'autres options ». Cette option remet le menu "
                                "complet de Windows 10 (après un redémarrage de "
                                "l'Explorateur, proposé tout de suite)."))
        root.addWidget(box)

        # --- signature ---
        box, sl = _section("Signature")
        self.sign_preview = QLabel()
        self.sign_preview.setFixedHeight(76)
        self.sign_preview.setAlignment(Qt.AlignCenter)
        self.sign_preview.setObjectName("signPreview")
        sl.addWidget(self.sign_preview)
        row = QHBoxLayout()
        draw = QPushButton("Dessiner…")
        draw.clicked.connect(self.draw_signature.emit)
        imp = QPushButton("Importer une photo…")
        imp.clicked.connect(self._import_signature)
        clear = QPushButton("Effacer")
        clear.setObjectName("ghost")
        clear.clicked.connect(self._clear_signature)
        row.addWidget(draw)
        row.addWidget(imp)
        row.addStretch(1)
        row.addWidget(clear)
        sl.addLayout(row)
        root.addWidget(box)

        # --- quality and startup ---
        box, ql = _section("Qualité et démarrage")
        grid = QHBoxLayout()
        grid.addWidget(QLabel("Compression des images"))
        grid.addStretch(1)
        self.compress_q = _spin(10, 95, settings.get("compress_quality"), " %")
        self.compress_q.valueChanged.connect(lambda v: self._set("compress_quality", v))
        grid.addWidget(self.compress_q)
        ql.addLayout(grid)
        grid = QHBoxLayout()
        grid.addWidget(QLabel("Qualité des JPG créés"))
        grid.addStretch(1)
        self.jpg_q = _spin(50, 100, settings.get("jpg_quality"), " %")
        self.jpg_q.valueChanged.connect(lambda v: self._set("jpg_quality", v))
        grid.addWidget(self.jpg_q)
        ql.addLayout(grid)
        self.autostart = QCheckBox("Lancer Cerclic avec Windows (recommandé)")
        self.autostart.setChecked(bool(settings.get("autostart")))
        self.autostart.toggled.connect(lambda on: self._set("autostart", on))
        ql.addWidget(self.autostart)
        root.addWidget(box)
        root.addStretch(1)

        # --- footer ---
        foot = QWidget()
        foot.setObjectName("foot")
        fl = QHBoxLayout(foot)
        fl.setContentsMargins(20, 10, 20, 12)
        version = QLabel(f"Cerclic {__version__}")
        version.setObjectName("hint")
        fl.addWidget(version)
        fl.addStretch(1)
        quit_btn = QPushButton("Quitter Cerclic")
        quit_btn.setObjectName("ghost")
        quit_btn.setToolTip("Arrête Cerclic. Pour le relancer, ouvre-le depuis le Bureau "
                            "ou le menu Démarrer.")
        quit_btn.clicked.connect(self.quit_requested.emit)
        close = QPushButton("Fermer")
        close.setObjectName("primary")
        close.setDefault(True)
        close.clicked.connect(self.close)
        fl.addWidget(quit_btn)
        fl.addWidget(close)
        outer.addWidget(foot)

        self.setStyleSheet(
            f"SettingsWindow, #body, QScrollArea{{background:{BG};}}"
            f"#foot{{background:{SURFACE};border-top:1px solid {BORDER};}}"
            f"#section{{background:{SURFACE};border:1px solid {BORDER};border-radius:14px;}}"
            f"#sectionTitle{{color:{TEXT};font-size:14px;font-weight:700;}}"
            f"#appName{{color:{TEXT};font-size:20px;font-weight:800;}}"
            f"#hint{{color:{MUTED};font-size:12px;}}"
            f"#welcome{{background:#1F2B45;color:{TEXT};border:1px solid #2F4A7A;"
            "border-radius:12px;padding:10px 12px;font-size:12px;}"
            f"#sep{{background:{BORDER};}}"
            "#signPreview{background:#FAFAF7;border-radius:10px;color:#777;}"
            f"QLabel{{color:{TEXT};}} QCheckBox{{color:{TEXT};spacing:8px;}}"
            f"QSpinBox{{background:{SURFACE_2};color:{TEXT};border:1px solid {BORDER};"
            "border-radius:6px;padding:4px 6px;min-width:80px;}" + BUTTON_QSS)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.refresh_signature()
        self.resize(560, 700)
        self._apply_hotkey_status(None)

    # -- placing -----------------------------------------------------------------------
    def show_centered(self, near: QPoint | None = None) -> None:
        screen = (QGuiApplication.screenAt(near) if near is not None else None) \
            or QGuiApplication.primaryScreen()
        avail = screen.availableGeometry()
        h = min(self.height(), int(avail.height() * 0.92))
        self.resize(self.width(), h)
        self.move(avail.center().x() - self.width() // 2,
                  avail.center().y() - h // 2)
        self.show()
        self.raise_()
        self.activateWindow()

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
        self.changed.emit("hotkey_combo")

    def set_hotkey_status(self, ok: bool | None) -> None:
        """What the app learnt when registering the shortcut."""
        self._apply_hotkey_status(ok)

    def _apply_hotkey_status(self, ok: bool | None) -> None:
        if not self.hotkey_on.isChecked():
            self.shortcut.set_status(
                "Raccourci désactivé : le clic droit « Cerclic » reste disponible."
                if self.context_menu.isChecked() else "Raccourci désactivé.")
        elif ok is None:
            self.shortcut.set_status("")
        elif ok:
            self.shortcut.set_status("✓ Actif partout dans Windows.", "ok")
        else:
            self.shortcut.set_status("Une autre application utilise déjà cette "
                                     "combinaison. Choisis-en une autre avec "
                                     "« Modifier ».", "error")

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
                    pix.scaled(380, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                return
        self.sign_preview.setPixmap(QPixmap())
        self.sign_preview.setText("Aucune signature : elle sera demandée la première "
                                  "fois que tu signes.")

    def _import_signature(self) -> None:
        src, _ = QFileDialog.getOpenFileName(
            self, "Choisir une photo de ta signature", "",
            "Images (*.png *.jpg *.jpeg *.webp *.heic *.bmp)")
        if not src:
            return
        from .signature import import_signature, signature_path
        try:
            path = import_signature(src, signature_path())
        except Exception as exc:
            self.sign_preview.setPixmap(QPixmap())
            self.sign_preview.setText(str(exc) if isinstance(exc, ValueError)
                                      else "Image illisible.")
            return
        self._set("signature", path)
        self.refresh_signature()

    def _clear_signature(self) -> None:
        self._set("signature", "")
        self.refresh_signature()

    def closeEvent(self, e):
        self.shortcut.stop_recording()
        super().closeEvent(e)
