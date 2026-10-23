"""Close a popup (the wheel, a bubble) once the user is clearly elsewhere.

Only the popup's own events are used, nothing global:
* Cerclic loses the foreground: a click on another window, Alt+Tab...
  (except in the first moment, when the window that launched Cerclic may still
  take the focus back: then Cerclic simply takes it again);
* the popup is not in front and the pointer left it without coming back;
* nothing happens on it for a long while.
"""
from __future__ import annotations

import time

from PySide6.QtCore import QEvent, QObject, Qt, QTimer
from PySide6.QtGui import QGuiApplication

from ..log import log

_ACTIVITY = {QEvent.MouseMove, QEvent.MouseButtonPress, QEvent.KeyPress,
             QEvent.Wheel, QEvent.InputMethod}


class DismissGuard(QObject):
    GRACE_S = 1.5

    def __init__(self, widget, on_dismiss, leave_s: float = 2.5, idle_s: float = 60.0,
                 keep_once_used: bool = False, sticky: bool = False):
        super().__init__(widget)
        self.widget, self.on_dismiss = widget, on_dismiss
        self.leave_s, self.idle_s = leave_s, idle_s
        # An editor the user already worked in is not thrown away by a click
        # elsewhere (only by Escape, its buttons, or a long inactivity).
        self.keep_once_used = keep_once_used
        # A question that may need something from another window (a password to
        # copy from a mail) only goes on Escape, its buttons or a long inactivity.
        self.sticky = sticky
        self._shown = self._activity = time.monotonic()
        self._left_at: float | None = None
        self._touched = False      # the user pressed inside the popup
        self._retook = False
        self._timer = QTimer(self, interval=200)
        self._timer.timeout.connect(self._tick)
        widget.installEventFilter(self)

    def start(self) -> None:
        self._shown = self._activity = time.monotonic()
        self._left_at = None
        self._touched = self._retook = False
        from PySide6.QtWidgets import QWidget
        try:
            for child in self.widget.findChildren(QWidget):   # clicks on the content
                child.removeEventFilter(self)
                child.installEventFilter(self)
        except RuntimeError:
            pass
        self._timer.start()

    def resume(self) -> None:
        """Start again after a pause, keeping what the user already did."""
        touched = self._touched
        self.start()
        self._touched = touched

    def stop(self) -> None:
        self._timer.stop()

    def eventFilter(self, obj, e):
        t = e.type()
        if t in _ACTIVITY:
            self._activity = time.monotonic()
            self._left_at = None
            if t in (QEvent.MouseButtonPress, QEvent.KeyPress):
                self._touched = True
        elif t == QEvent.Enter:
            self._left_at = None
        elif t == QEvent.Leave and obj is self.widget:
            self._left_at = time.monotonic()
        elif t == QEvent.ActivationChange and obj is self.widget:
            if not self.widget.isActiveWindow():
                QTimer.singleShot(0, self._check_deactivated)
        return False

    def _dismiss(self, reason: str) -> None:
        self._timer.stop()
        log(f"fermeture automatique ({reason})")
        self.on_dismiss()

    def _check_deactivated(self) -> None:
        try:
            visible = self.widget.isVisible()
        except RuntimeError:
            return
        if not visible or QGuiApplication.applicationState() == Qt.ApplicationActive:
            return
        if self.sticky or (self.keep_once_used and self._touched):
            return
        early = time.monotonic() - self._shown < self.GRACE_S and not self._touched
        if early:
            if not self._retook:   # the launching window took the focus back
                self._retook = True
                from ..win.foreground import bring_to_front
                bring_to_front(int(self.widget.winId()))
            return
        self._dismiss("clic ailleurs")

    def _tick(self) -> None:
        try:
            if not self.widget.isVisible():
                return
            active = self.widget.isActiveWindow()
        except RuntimeError:
            self._timer.stop()
            return
        now = time.monotonic()
        if now - self._activity > self.idle_s:
            self._dismiss("inactivité")
        elif (not active and self._left_at is not None
              and now - self._left_at > self.leave_s and not self.sticky
              and not (self.keep_once_used and self._touched)):
            self._dismiss("pointeur parti")
