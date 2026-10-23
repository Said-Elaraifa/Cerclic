"""Run an action and report the result, with no UI dependency.

The UI gathers what an action needs (crop box, password, text, signature
placement) into `opts`, then calls run() from a worker thread. run() never
raises: it returns a Result. Outputs are always new files beside the sources;
if an action fails or is cancelled, every file and folder it reserved is
removed again, so nothing half-written is ever left behind.
"""
from __future__ import annotations

import errno
import os
import threading
import time
from dataclasses import dataclass, field

from . import paths as _paths
from .actions import registry
from .errors import Cancelled, NeedsPassword, NothingToDo, UserError
from .log import log_exception

__all__ = ["Cancelled", "Context", "NeedsPassword", "NothingToDo", "Result",
           "UserError", "friendly_error", "missing_inputs", "run"]


@dataclass
class Result:
    action_id: str
    ok: bool
    outputs: list[str] = field(default_factory=list)
    error: str = ""
    seconds: float = 0.0
    cancelled: bool = False
    needs_password: bool = False
    info: bool = False          # nothing went wrong, there was just nothing to do

    @property
    def count(self) -> int:
        return len(self.outputs)


class Context:
    """Passed to handlers: progress reporting and cooperative cancellation."""

    def __init__(self, on_progress=None, cancel: threading.Event | None = None):
        self._on_progress = on_progress
        self._cancel = cancel or threading.Event()

    @property
    def cancelled(self) -> bool:
        return self._cancel.is_set()

    def check(self) -> None:
        if self._cancel.is_set():
            raise Cancelled()

    def progress(self, fraction: float | None, text: str = "") -> None:
        if self._on_progress is not None:
            try:
                if fraction is not None:
                    fraction = max(0.0, min(1.0, float(fraction)))
                self._on_progress(fraction, text)
            except Exception:
                pass


def friendly_error(exc: BaseException) -> str:
    """Turn an exception into a short French sentence."""
    if isinstance(exc, UserError):
        return str(exc)
    if isinstance(exc, PermissionError):
        return ("Accès refusé : le fichier est peut-être ouvert dans une autre "
                "application, ou le dossier est protégé.")
    long_name = len(str(getattr(exc, "filename", "") or "")) >= 250
    if isinstance(exc, OSError) and (long_name or getattr(exc, "errno", None) == errno.ENAMETOOLONG
                                     or getattr(exc, "winerror", None) == 206):
        return ("Nom ou chemin trop long pour Windows : renomme le fichier plus court, "
                "ou déplace-le dans un dossier moins profond.")
    if isinstance(exc, FileNotFoundError):
        return "Fichier introuvable : il a peut-être été déplacé ou supprimé."
    if isinstance(exc, MemoryError):
        return "Fichier trop lourd pour la mémoire disponible."
    if isinstance(exc, OSError) and getattr(exc, "errno", None) == errno.ENOSPC:
        return "Le disque est plein."
    name = type(exc).__name__
    if name in ("UnidentifiedImageError", "DecompressionBombError"):
        return "Image illisible ou format non pris en charge."
    if name in ("FileDataError", "EmptyFileError", "PdfError"):
        return "PDF endommagé ou illisible."
    return ("Erreur inattendue. Réessaie ; si cela recommence, le détail est dans "
            "le journal de Cerclic (cerclic.log).")


def _cleanup(reserved: list[str]) -> None:
    import shutil
    for p in reversed(reserved):
        try:
            if os.path.isdir(p):
                shutil.rmtree(p, ignore_errors=True)
            elif os.path.exists(p):
                os.remove(p)
        except OSError:
            pass


def run(action_id: str, paths: list[str], opts: dict | None = None,
        on_progress=None, cancel: threading.Event | None = None) -> Result:
    opts = dict(opts or {})
    action = registry.get(action_id)
    ctx = Context(on_progress, cancel)
    t0 = time.perf_counter()
    with _paths.tracking() as reserved:
        try:
            gone = [p for p in paths if not os.path.exists(p)]
            if gone:
                name = os.path.basename(gone[0])
                raise UserError(f"« {name} » n'est plus là : il a été déplacé, renommé "
                                "ou supprimé (ou la clé USB retirée)." if len(gone) == 1
                                else f"{len(gone)} fichiers ne sont plus là : ils ont été "
                                     "déplacés, renommés ou supprimés.")
            if len(paths) < action.min_files:
                raise UserError(f"{action.label} : il faut au moins "
                                f"{action.min_files} fichiers.")
            outputs = [o for o in action.handler(paths, opts, ctx) if o]
            ctx.check()
            return Result(action_id, True, outputs, "", time.perf_counter() - t0)
        except Cancelled:
            _cleanup(reserved)
            return Result(action_id, False, [], "Annulé", time.perf_counter() - t0,
                          cancelled=True)
        except NeedsPassword as exc:
            _cleanup(reserved)
            return Result(action_id, False, [], str(exc), time.perf_counter() - t0,
                          needs_password=True)
        except NothingToDo as exc:
            _cleanup(reserved)
            return Result(action_id, False, [], str(exc), time.perf_counter() - t0,
                          info=True)
        except UserError as exc:
            _cleanup(reserved)
            return Result(action_id, False, [], str(exc), time.perf_counter() - t0)
        except BaseException as exc:  # never raised up: shown as a card
            _cleanup(reserved)
            log_exception(f"action {action_id} a échoué")
            return Result(action_id, False, [], friendly_error(exc),
                          time.perf_counter() - t0)


def missing_inputs(action_id: str, opts: dict) -> list[str]:
    """Which required `needs` are not yet satisfied in opts (drives the UI)."""
    action = registry.get(action_id)
    out = []
    for need in action.needs:
        if need.endswith("?"):
            continue
        if opts.get(need) in (None, ""):
            out.append(need)
    return out
