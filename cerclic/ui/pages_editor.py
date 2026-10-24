"""Page organiser for a PDF, in a compact popup: every page as a thumbnail.

Drag a page to move it (or Ctrl + arrows), select pages and turn them or
remove them (Suppr). "Enregistrer" writes the PDF as arranged; "Extraire"
writes only the selected pages. The original file is never changed.
"""
from __future__ import annotations

import os

from PySide6.QtCore import QRectF, QSize, Qt
from PySide6.QtGui import QColor, QImage, QPainter, QPen, QTransform
from PySide6.QtWidgets import (QAbstractItemView, QLabel, QListView, QListWidget,
                               QListWidgetItem, QPushButton, QStyle,
                               QStyledItemDelegate)

from ..i18n import tr, trn
from .editor_base import EditorWindow, Loader, delete_key, mod_key, qimage_from_rgb
from .theme import ACCENT, BG, MUTED, TEXT, base_font

THUMB_H = 118           # thumbnail height, logical px
CELL = QSize(108, 150)  # one page in the grid, label included
ROLE_PAGE = Qt.UserRole          # original page index
ROLE_ROT = Qt.UserRole + 1       # extra rotation, degrees clockwise
ROLE_IMG = Qt.UserRole + 2       # QImage thumbnail (None until rendered)


def _step_of(widget, key) -> int:
    """-1 towards the first page, 1 towards the last, for an arrow key: the
    pages run from the right when the interface reads from the right."""
    back = key in (Qt.Key_Left, Qt.Key_Up)
    if key in (Qt.Key_Left, Qt.Key_Right) and widget.isRightToLeft():
        back = not back
    return -1 if back else 1


class _PageDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index) -> QSize:
        return CELL

    def paint(self, p: QPainter, option, index) -> None:
        p.save()
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setRenderHint(QPainter.SmoothPixmapTransform, True)
        r = QRectF(option.rect).adjusted(4, 4, -4, -4)
        selected = bool(option.state & QStyle.State_Selected)
        if selected:
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(46, 124, 246, 38))
            p.drawRoundedRect(r, 10, 10)
        box = QRectF(r.left() + 6, r.top() + 6, r.width() - 12, r.height() - 34)
        img: QImage | None = index.data(ROLE_IMG)
        rot = int(index.data(ROLE_ROT) or 0)
        if img is not None and not img.isNull():
            if rot:
                img = img.transformed(QTransform().rotate(rot), Qt.SmoothTransformation)
            s = min(box.width() / img.width(), box.height() / img.height())
            w, h = img.width() * s, img.height() * s
            target = QRectF(box.center().x() - w / 2, box.center().y() - h / 2, w, h)
            p.fillRect(target.adjusted(-1, -1, 1, 1), QColor(20, 40, 90, 50))
            p.drawImage(target, img)
            if selected:
                p.setPen(QPen(QColor(ACCENT), 2))
                p.setBrush(Qt.NoBrush)
                p.drawRect(target.adjusted(-2, -2, 2, 2))
        else:
            p.setPen(QPen(QColor("#C5CEDC"), 1, Qt.DashLine))
            p.setBrush(Qt.NoBrush)
            p.drawRoundedRect(box.adjusted(12, 6, -12, -6), 4, 4)
        f = base_font()
        f.setPixelSize(12)
        f.setBold(selected)
        p.setFont(f)
        p.setPen(QColor(TEXT if selected else MUTED))
        label = str(int(index.data(ROLE_PAGE)) + 1)
        if rot:
            label += f"  ↻{rot}°"
        p.drawText(QRectF(r.left(), r.bottom() - 24, r.width(), 20), Qt.AlignCenter, label)
        p.restore()


class PageGrid(QListWidget):
    """The pages, in order; drag and drop to move them."""

    def __init__(self):
        super().__init__()
        self.setViewMode(QListView.ListMode)
        self.setFlow(QListView.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(QListView.Adjust)
        self.setUniformItemSizes(True)
        self.setSpacing(2)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setItemDelegate(_PageDelegate(self))
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet(f"QListWidget{{background:{BG};border:none;border-radius:10px;"
                           "padding:4px;outline:0;}")

    move_requested = None        # set by the editor: fn(step)

    def keyPressEvent(self, e):
        k = e.key()
        if e.modifiers() & Qt.ControlModifier and self.move_requested is not None and k in (
                Qt.Key_Left, Qt.Key_Up, Qt.Key_Right, Qt.Key_Down):
            self.move_requested(_step_of(self, k))
            return
        super().keyPressEvent(e)

    def order(self) -> list[tuple[int, int]]:
        return [(int(self.item(i).data(ROLE_PAGE)), int(self.item(i).data(ROLE_ROT) or 0))
                for i in range(self.count())]

    def selected_rows(self) -> list[int]:
        return sorted(self.row(it) for it in self.selectedItems())


class PagesEditor(EditorWindow):
    """accepted({"pages_order": [(index, rotation)...], "pages_mode": "save" | "extract"})"""

    def __init__(self, path: str, password: str | None = None):
        super().__init__(os.path.basename(path),
                         tr("Glisse pour trier · {key} pour enlever", key=delete_key()))
        self.path, self.password = path, password
        self.grid = PageGrid()
        self.grid.move_requested = self.move_selection
        self.grid.itemSelectionChanged.connect(self._sync)
        self.grid.model().rowsMoved.connect(lambda *_: self._sync())
        self.center.addWidget(self.grid)

        self.rot_left = self.chip("↺", checkable=False)
        self.rot_left.setToolTip(tr("Pivoter à gauche"))
        self.rot_left.clicked.connect(lambda: self.rotate_selection(270))
        self.rot_right = self.chip("↻", checkable=False)
        self.rot_right.setToolTip(tr("Pivoter à droite ({key} + R)", key=mod_key()))
        self.rot_right.clicked.connect(lambda: self.rotate_selection(90))
        self.remove_btn = self.chip(tr("Supprimer"), checkable=False)
        self.remove_btn.clicked.connect(self.remove_selection)
        # (the first page is on the right when the interface reads from the right)
        back, forward = self.nav_arrows()
        rtl = self.isRightToLeft()
        self.left_btn = self.chip(back, checkable=False)
        self.left_btn.setToolTip(tr("Vers le début ({key} + {arrow})", key=mod_key(),
                                    arrow="→" if rtl else "←"))
        self.left_btn.clicked.connect(lambda: self.move_selection(-1))
        self.right_btn = self.chip(forward, checkable=False)
        self.right_btn.setToolTip(tr("Vers la fin ({key} + {arrow})", key=mod_key(),
                                     arrow="←" if rtl else "→"))
        self.right_btn.clicked.connect(lambda: self.move_selection(1))
        for w in (self.rot_left, self.rot_right, self.remove_btn, self.left_btn,
                  self.right_btn):
            self.tools.addWidget(w)
        self.tools.addStretch(1)
        self.count_label = QLabel("")
        self.count_label.setObjectName("hint")
        self.tools.addWidget(self.count_label)

        self.extract_btn = QPushButton(tr("Extraire la sélection"))
        self.extract_btn.setObjectName("ghost")
        self.extract_btn.setToolTip(tr("Un nouveau PDF avec seulement les pages choisies"))
        self.extract_btn.setFocusPolicy(Qt.NoFocus)
        self.extract_btn.clicked.connect(self.extract)
        reset = QPushButton(tr("Réinitialiser"))
        reset.setObjectName("ghost")
        reset.setFocusPolicy(Qt.NoFocus)
        reset.clicked.connect(self._fill)
        cancel = QPushButton(tr("Annuler"))
        cancel.setObjectName("ghost")
        cancel.setFocusPolicy(Qt.NoFocus)
        cancel.clicked.connect(self.cancel)
        self.ok = QPushButton(tr("Enregistrer"))
        self.ok.setObjectName("primary")
        self.ok.setFocusPolicy(Qt.NoFocus)
        self.ok.clicked.connect(self.validate)
        self.bar.addWidget(self.extract_btn)
        self.bar.addWidget(reset)
        self.bar.addStretch(1)
        self.bar.addWidget(cancel)
        self.bar.addWidget(self.ok)

        self.page_count = 0
        self._thumbs: dict[int, QImage] = {}
        self._loader = Loader(self)
        self._loader.done.connect(self._loaded)
        self._loader.progress.connect(self._thumb)

    # -- opening -----------------------------------------------------------------------------
    def start(self, anchor=None) -> None:
        if anchor is not None:
            self.anchor = anchor
        from ..actions import pdf as _pdf
        try:
            self.page_count = _pdf.pdf_page_count(self.path, self.password)
        except Exception:
            self.page_count = 0
        room_w, room_h = self.room(640, 470)
        cols = max(3, min(6, (room_w - 16) // CELL.width(), max(1, self.page_count)))
        rows = 1 if self.page_count <= cols else (2 if self.page_count <= 2 * cols else 2.5)
        w = cols * (CELL.width() + 4) + 36           # + scroll bar and padding
        h = int(rows * (CELL.height() + 4)) + 12
        self.grid.setFixedSize(QSize(w, min(h, room_h)))
        self._fill()
        self.open_at()
        self.grid.setFocus()
        dpr = self.dpr()
        height = int(THUMB_H * dpr)
        path, pw = self.path, self.password
        self._loader.run_reporting(
            lambda report, stop: _pdf.render_thumbs(
                path, height, pw, report=lambda i, raw: report((i, qimage_from_rgb(*raw))),
                should_stop=stop))

    def _fill(self) -> None:
        self.grid.clear()
        for i in range(self.page_count):
            it = QListWidgetItem()
            it.setData(ROLE_PAGE, i)
            it.setData(ROLE_ROT, 0)
            it.setData(ROLE_IMG, self._thumbs.get(i))
            it.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)
            self.grid.addItem(it)
        self._sync()

    def _thumb(self, payload) -> None:
        i, img = payload
        self._thumbs[i] = img
        for row in range(self.grid.count()):
            it = self.grid.item(row)
            if int(it.data(ROLE_PAGE)) == i:
                it.setData(ROLE_IMG, img)

    def _loaded(self, res, err) -> None:
        if err:
            self.count_label.setText(err)

    # -- editing --------------------------------------------------------------------------------
    def rotate_selection(self, degrees: int) -> None:
        for it in self.grid.selectedItems():
            it.setData(ROLE_ROT, (int(it.data(ROLE_ROT) or 0) + degrees) % 360)
        self._sync()

    def remove_selection(self) -> None:
        rows = self.grid.selected_rows()
        if not rows:
            return
        for row in reversed(rows):
            self.grid.takeItem(row)
        if self.grid.count():
            self.grid.setCurrentRow(min(rows[0], self.grid.count() - 1))
        self._sync()

    def move_selection(self, step: int) -> None:
        rows = self.grid.selected_rows()
        if not rows:
            return
        if (step < 0 and rows[0] == 0) or (step > 0 and rows[-1] == self.grid.count() - 1):
            return
        items = [self.grid.item(r) for r in rows]
        for r in (rows if step < 0 else reversed(rows)):
            it = self.grid.takeItem(r)
            self.grid.insertItem(r + step, it)
        self.grid.clearSelection()
        for it in items:
            it.setSelected(True)
        self.grid.scrollToItem(items[0])
        self._sync()

    def _sync(self) -> None:
        n = self.grid.count()
        sel = len(self.grid.selectedItems())
        self.count_label.setText(
            trn("{n} sélectionnée sur {count}", "{n} sélectionnées sur {count}", sel, count=n)
            if sel else trn("{n} page", "{n} pages", n))
        for w in (self.rot_left, self.rot_right, self.remove_btn, self.left_btn,
                  self.right_btn, self.extract_btn):
            w.setEnabled(sel > 0)
        self.ok.setEnabled(n > 0)

    def keyPressEvent(self, e):
        k = e.key()
        if k in (Qt.Key_Delete, Qt.Key_Backspace):
            self.remove_selection()
        elif e.modifiers() & Qt.ControlModifier and k in (Qt.Key_Left, Qt.Key_Up,
                                                          Qt.Key_Right, Qt.Key_Down):
            self.move_selection(_step_of(self, k))
        elif e.modifiers() & Qt.ControlModifier and k == Qt.Key_R:
            self.rotate_selection(90)
        else:
            super().keyPressEvent(e)

    # -- result ------------------------------------------------------------------------------------
    def validate(self) -> None:
        if self.grid.count():
            self.finish({"pages_order": self.grid.order(), "pages_mode": "save"})

    def extract(self) -> None:
        rows = self.grid.selected_rows()
        if rows:
            order = self.grid.order()
            self.finish({"pages_order": [order[r] for r in rows], "pages_mode": "extract"})
