"""Colours, fonts and the "frosted glass" light style shared by every window.

Clair givré: white frosted panels on a soft pastel backdrop, one blue accent,
dark text. Painted glass (translucent white, a fine bright edge, a soft
shadow) looks the same on Windows and macOS.
"""
from __future__ import annotations

import sys

from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import QApplication

# surfaces
BG = "#EEF2F8"           # behind pictures in the editors, lists
SURFACE = "#FFFFFF"      # cards, bubbles, popups (drawn a little translucent)
SURFACE_2 = "#F1F4F9"    # secondary buttons, inputs, chips
BORDER = "#DCE2EC"
HOVER = "#E7ECF4"
# text (all at least 4.5:1 on the white cards)
TEXT = "#1B2232"
TEXT_SOFT = "#3A4457"     # section titles
MUTED = "#535D71"
FAINT = "#6B7487"
# colours: ACCENT for switches, sliders, selection, focus; ACCENT_STRONG
# under white text (4.9:1), the same blue a shade deeper
ACCENT = "#2E7CF6"
ACCENT_STRONG = "#1F6AE6"
ACCENT_HOVER = "#1A5CCB"
ACCENT_SOFT = "#E4EEFF"
OK = "#0F7A57"
ERROR = "#C8373C"
WARN = "#985A00"
OUTLINE = "#848EA1"       # empty radio rings, switches when off (3.3:1)

if sys.platform == "win32":
    FONT_FAMILY = "Segoe UI"
elif sys.platform == "darwin":
    FONT_FAMILY = ""            # the system font (San Francisco), see base_font()
else:
    FONT_FAMILY = "Sans Serif"
# macOS counts 72 points per inch, Windows 96: the same size in points would
# look a quarter smaller on a Mac. Sizes in points are scaled to match.
PT_SCALE = 96 / 72 if sys.platform == "darwin" else 1.0


def base_font() -> QFont:
    """The interface font (size to be set by the caller)."""
    if not FONT_FAMILY:
        app = QApplication.instance()
        return QFont(app.font()) if app is not None else QFont()
    return QFont(FONT_FAMILY)


def font(size: float = 10, bold: bool = False) -> QFont:
    f = base_font()
    f.setPointSizeF(size * PT_SCALE)
    f.setBold(bold)
    return f


def qcolor(hex_or_color, alpha: int | None = None) -> QColor:
    c = QColor(hex_or_color)
    if alpha is not None:
        c.setAlpha(alpha)
    return c


def _luminance(c: QColor) -> float:
    def lin(v: float) -> float:
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(c.redF()) + 0.7152 * lin(c.greenF()) + 0.0722 * lin(c.blueF())


def under_white_text(color: QColor, ratio: float = 4.6) -> QColor:
    """The same hue, deepened until white text on it reads well (WCAG AA)."""
    c = QColor(color)
    for _ in range(40):
        if 1.05 / (_luminance(c) + 0.05) >= ratio:
            break
        c = c.darker(104)
    return c


def glass(alpha: int = 214) -> QColor:
    """The frosted white of panels."""
    return QColor(255, 255, 255, alpha)


def card_qss(radius: int = 16, name: str = "card") -> str:
    """Frosted white card: a faint top-to-bottom sheen and a fine cool edge."""
    return (f"#{name}{{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,"
            "stop:0 rgba(255,255,255,253),stop:1 rgba(245,248,253,250));"
            f"border:1px solid rgba(30,50,100,28);border-radius:{radius}px;}}")


BUTTON_QSS = (
    f"QPushButton{{background:{SURFACE};color:{TEXT};border:1px solid {BORDER};"
    "padding:7px 15px;border-radius:9px;font-weight:600;}"
    f"QPushButton:hover{{background:#F7F9FD;border-color:#C9D2E1;}}"
    f"QPushButton:pressed{{background:{HOVER};}}"
    f"QPushButton:disabled{{color:{FAINT};background:{SURFACE_2};}}"
    f"QPushButton#primary{{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,"
    f"stop:0 #2A72E8, stop:1 {ACCENT_STRONG});color:white;border:1px solid {ACCENT_HOVER};}}"
    f"QPushButton#primary:hover{{background:{ACCENT_HOVER};}}"
    "QPushButton#primary:disabled{background:#B9CDEE;color:#F4F7FC;border-color:#B9CDEE;}"
    f"QPushButton#ghost{{background:transparent;color:{MUTED};border:1px solid transparent;}}"
    f"QPushButton#ghost:hover{{color:{TEXT};background:rgba(27,34,50,0.06);}}"
    f"QPushButton#ghost:disabled{{color:{FAINT};background:transparent;}}"
    f"QPushButton#danger{{background:transparent;color:{ERROR};border:1px solid transparent;}}"
    "QPushButton#danger:hover{background:rgba(200,55,60,0.08);}"
    f"QPushButton#danger:disabled{{color:{FAINT};background:transparent;}}"
    f"QPushButton:checked{{background:{ACCENT_STRONG};color:white;"
    f"border-color:{ACCENT_STRONG};}}"
)

SCROLL_QSS = (
    "QScrollBar:vertical{background:transparent;width:10px;margin:2px;}"
    "QScrollBar::handle:vertical{background:rgba(27,34,50,0.20);border-radius:4px;"
    "min-height:30px;}"
    "QScrollBar::handle:vertical:hover{background:rgba(27,34,50,0.32);}"
    "QScrollBar::add-line,QScrollBar::sub-line{height:0;width:0;}"
    "QScrollBar::add-page,QScrollBar::sub-page{background:transparent;}"
    "QScrollBar:horizontal{background:transparent;height:10px;margin:2px;}"
    "QScrollBar::handle:horizontal{background:rgba(27,34,50,0.20);border-radius:4px;"
    "min-width:30px;}"
)

INPUT_QSS = (
    f"QLineEdit{{background:{SURFACE};color:{TEXT};border:1px solid {BORDER};"
    f"border-radius:9px;padding:8px 10px;selection-background-color:{ACCENT};}}"
    f"QLineEdit:focus{{border:1px solid {ACCENT};}}"
)

# keyboard focus ring for the settings window (its buttons take the focus from
# the Tab key only, so a click never leaves a ring behind)
FOCUS_QSS = f"QPushButton:focus{{border:2px solid {ACCENT};padding:6px 14px;}}"

TOOLTIP_QSS = (
    f"QToolTip{{background:{SURFACE};color:{TEXT};border:1px solid {BORDER};"
    "border-radius:6px;padding:5px 8px;}"
)


def apply_app_theme(app: QApplication) -> None:
    app.setStyle("Fusion")
    pal = QPalette()
    pal.setColor(QPalette.Window, QColor("#F4F7FB"))
    pal.setColor(QPalette.WindowText, QColor(TEXT))
    pal.setColor(QPalette.Base, QColor(SURFACE))
    pal.setColor(QPalette.AlternateBase, QColor(SURFACE_2))
    pal.setColor(QPalette.Text, QColor(TEXT))
    pal.setColor(QPalette.Button, QColor(SURFACE))
    pal.setColor(QPalette.ButtonText, QColor(TEXT))
    pal.setColor(QPalette.Highlight, QColor(ACCENT))
    pal.setColor(QPalette.HighlightedText, QColor("white"))
    pal.setColor(QPalette.ToolTipBase, QColor(SURFACE))
    pal.setColor(QPalette.ToolTipText, QColor(TEXT))
    pal.setColor(QPalette.PlaceholderText, QColor(FAINT))
    pal.setColor(QPalette.Light, QColor("#FFFFFF"))
    pal.setColor(QPalette.Midlight, QColor(HOVER))
    pal.setColor(QPalette.Mid, QColor(BORDER))
    pal.setColor(QPalette.Dark, QColor("#B8C1D1"))
    app.setPalette(pal)
    app.setFont(font(10))
    app.setStyleSheet(TOOLTIP_QSS)
