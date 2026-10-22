"""Run an action and report the result, with no UI dependency.

The UI gathers any `needs` (crop box, password, text, signature) into `opts`
before calling run(). Output files are always new files beside the sources, so a
failed run never damages an original.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field

from .actions import registry


@dataclass
class Result:
    action_id: str
    ok: bool
    outputs: list[str] = field(default_factory=list)
    error: str = ""
    seconds: float = 0.0

    @property
    def count(self) -> int:
        return len(self.outputs)


def run(action_id: str, paths: list[str], opts: dict | None = None) -> Result:
    opts = dict(opts or {})
    action = registry.get(action_id)
    t0 = time.perf_counter()
    try:
        if len(paths) < action.min_files:
            raise ValueError(f"{action.label}: {action.min_files} fichier(s) minimum")
        outputs = action.handler(paths, opts)
        outputs = [o for o in outputs if o]
        return Result(action_id, True, outputs, "", time.perf_counter() - t0)
    except Exception as exc:  # surfaced to the user as a toast, never raised up
        return Result(action_id, False, [], str(exc), time.perf_counter() - t0)


def missing_inputs(action_id: str, opts: dict) -> list[str]:
    """Which `needs` are not yet satisfied in opts (drives UI prompts)."""
    action = registry.get(action_id)
    out = []
    for need in action.needs:
        key = need.rstrip("?")
        optional = need.endswith("?")
        if optional:
            continue
        if key not in opts or opts[key] in (None, ""):
            out.append(key)
    return out
