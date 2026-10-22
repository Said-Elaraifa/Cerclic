"""Files an action is writing, kept on disk until it ends.

If Cerclic is stopped abruptly in the middle of an action (Task Manager,
shutdown, installer), the half-written result would stay next to the original
and could be mistaken for a finished one. The journal lists what is being
written; at the next start, Cerclic removes what was left unfinished.
"""
from __future__ import annotations

import json
import os
import shutil
import threading
import time

_local = threading.local()


def set_current_job(job_id: str | None) -> None:
    _local.job = job_id


def current_job() -> str | None:
    return getattr(_local, "job", None)


class Journal:
    def __init__(self, path: str):
        self.path = path
        self._lock = threading.Lock()
        self._jobs: dict[str, list[tuple[str, float]]] = {}

    def add(self, job_id: str | None, path: str) -> None:
        if not job_id:
            return
        with self._lock:
            self._jobs.setdefault(job_id, []).append((path, time.time()))
            self._save()

    def finish(self, job_id: str | None) -> None:
        with self._lock:
            if self._jobs.pop(job_id, None) is not None:
                self._save()

    def _save(self) -> None:
        tmp = self.path + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump([[p, t] for items in self._jobs.values() for p, t in items], f,
                          ensure_ascii=False)
            os.replace(tmp, self.path)
        except OSError:
            pass

    def recover(self) -> list[str]:
        """Remove what a previous run left half-written. Returns the paths."""
        try:
            with open(self.path, encoding="utf-8") as f:
                items = json.load(f)
        except (OSError, ValueError):
            return []
        removed = []
        for entry in items if isinstance(items, list) else []:
            try:
                path, when = str(entry[0]), float(entry[1])
                if not os.path.exists(path):
                    continue
                if os.path.getmtime(path) < when - 5:
                    continue        # older than the action: not ours
                if os.path.isdir(path):
                    shutil.rmtree(path, ignore_errors=True)
                else:
                    os.remove(path)
                removed.append(path)
            except (OSError, ValueError, IndexError, TypeError):
                continue
        try:
            os.remove(self.path)
        except OSError:
            pass
        return removed
