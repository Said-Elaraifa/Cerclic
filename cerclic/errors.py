"""Exceptions shared by the actions and the engine."""
from __future__ import annotations

from .i18n import tr


class Cancelled(Exception):
    """Raised inside an action when the user cancels."""


class UserError(Exception):
    """An expected problem; the message, translated where it is raised
    (tr), is shown to the user as is."""


class NeedsPassword(UserError):
    """The PDF is protected and no (or a wrong) password was given."""

    def __init__(self, message: str | None = None, path: str = ""):
        super().__init__(tr("Ce PDF est protégé par un mot de passe.")
                         if message is None else message)
        self.path = path


class NothingToDo(UserError):
    """The action would not change anything (already small, not protected...)."""


class LeftOut(NothingToDo):
    """This file cannot get this action (a multi-page TIFF for an image edit):
    alone it is said on the card; in a batch, the others still get done and
    the card says which one was left out."""
