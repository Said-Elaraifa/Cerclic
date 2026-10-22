"""Colours, fonts and the dark style shared by every Cerclic window."""
from __future__ import annotations

import sys

from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import QApplication

BG = "#14151A"          # editors background
SURFACE = "#1B1D24"     # cards, bubbles
SURFACE_2 = "#23262F"   # buttons, inputs
BORDER = "#2A2D37"
HOVER = "#343845"
TEXT = "#ECEEF3"
MUTED = "#9AA0B0"
ACCENT = "#4C8DFF"
OK = "#17B890"
ERROR = "#FF5A5F"
WARN = "#F2B84B"

FONT_FAMILY = "Segoe UI" if sys.platform == "win32" else "Sans Serif"


def font(size: float = 10, bold: bool = False) -> QFont:
    f = QFont(FONT_FAMILY)
    f.setPointSizeF(size)
    f.setBold(bold)
    return f


def qcolor(hex_or_color, alpha: int | None = None) -> QColor:
    c = QColor(hex_or_color)
    if alpha is not None:
        c.setAlpha(alpha)
    return c


BUTTON_QSS = (
    f"QPushButton{{background:{SURFACE_2};color:{TEXT};border:none;"
    "padding:8px 16px;border-radius:9px;font-weight:600;}"
    f"QPushButton:hover{{background:{HOVER};}}"
    f"QPushButton:pressed{{background:{BORDER};}}"
    f"QPushButton:disabled{{color:{MUTED};}}"
    f"QPushButton#primary{{background:{ACCENT};color:white;}}"
    "QPushButton#primary:hover{background:#6A9FFF;}"
    "QPushButton#primary:disabled{background:#2B3550;color:#7D869C;}"
    f"QPushButton#ghost{{background:transparent;color:{MUTED};}}"
    f"QPushButton#ghost:hover{{color:{TEXT};background:{SURFACE_2};}}"
    f"QPushButton:checked{{background:{ACCENT};color:white;}}"
)

INPUT_QSS = (
    f"QLineEdit{{background:{BG};color:{TEXT};border:1px solid {BORDER};"
    "border-radius:8px;padding:8px 10px;selection-background-color:#4C8DFF;}"
    f"QLineEdit:focus{{border:1px solid {ACCENT};}}"
)


def apply_app_theme(app: QApplication) -> None:
    app.setStyle("Fusion")
    pal = QPalette()
    pal.setColor(QPalette.Window, QColor(SURFACE))
    pal.setColor(QPalette.WindowText, QColor(TEXT))
    pal.setColor(QPalette.Base, QColor(BG))
    pal.setColor(QPalette.AlternateBase, QColor(SURFACE_2))
    pal.setColor(QPalette.Text, QColor(TEXT))
    pal.setColor(QPalette.Button, QColor(SURFACE_2))
    pal.setColor(QPalette.ButtonText, QColor(TEXT))
    pal.setColor(QPalette.Highlight, QColor(ACCENT))
    pal.setColor(QPalette.HighlightedText, QColor("white"))
    pal.setColor(QPalette.ToolTipBase, QColor(SURFACE))
    pal.setColor(QPalette.ToolTipText, QColor(TEXT))
    pal.setColor(QPalette.PlaceholderText, QColor(MUTED))
    app.setPalette(pal)
    app.setFont(font(10))
