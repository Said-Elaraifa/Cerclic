"""Exceptions shared by the actions and the engine."""


class Cancelled(Exception):
    """Raised inside an action when the user cancels."""


class UserError(Exception):
    """An expected problem; the message (French) is shown to the user as is."""


class NeedsPassword(UserError):
    """The PDF is protected and no (or a wrong) password was given."""

    def __init__(self, message: str = "Ce PDF est protégé par un mot de passe.",
                 path: str = ""):
        super().__init__(message)
        self.path = path


class NothingToDo(UserError):
    """The action would not change anything (already small, not protected...)."""
