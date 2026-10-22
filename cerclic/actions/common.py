"""Helpers shared by the action modules: progress reporting and cancellation.

Actions receive an optional `ctx` (the engine's Context). These helpers let the
same functions run without one, in tests or scripts.
"""
from __future__ import annotations


def check(ctx) -> None:
    """Raise Cancelled if the user cancelled."""
    if ctx is not None:
        ctx.check()


def progress(ctx, fraction: float | None, text: str = "") -> None:
    if ctx is not None:
        ctx.progress(fraction, text)
