"""Run an action for the app: on a thread, or in a separate worker process for
heavy PDF work.

PyMuPDF keeps Python busy for the whole of a long call (saving a 100 MB scan,
re-encoding its images): run in the app itself, that would freeze the wheel and
the cards for seconds. In a worker process the app stays fluid, "Arrêter" stops
the work at once, and even a PDF that crashes the PDF library cannot take
Cerclic down with it.
"""
from __future__ import annotations

import dataclasses
import os
import queue
import threading

from . import engine, i18n
from .actions import registry
from .i18n import tr

ISOLATE_BYTES = 8_000_000          # PDFs bigger than this go to a worker process
ALWAYS_ISOLATED = {"pdf_to_word"}  # long pure-Python work, heavy imports
# Drawing every page (to images) or re-encoding every picture (compress) can
# take long even on a medium file (a detailed plan): a worker process for
# anything but small files, a thread for those (quicker to start).
RENDERING = {"pdf_to_images", "pdf_compress"}
RENDERING_BYTES = 1_500_000


def should_isolate(action_id: str, paths: list[str]) -> bool:
    action = registry.get(action_id)
    if action.category != "pdf":
        return False
    if action_id in ALWAYS_ISOLATED:
        return True
    total = 0
    for p in paths:
        try:
            total += os.path.getsize(p)
        except OSError:
            pass
    if action_id in RENDERING:
        return total > RENDERING_BYTES
    return total > ISOLATE_BYTES


def run_job(action_id: str, paths: list[str], opts: dict, on_progress=None,
            cancel: threading.Event | None = None, on_reserved=None) -> engine.Result:
    if should_isolate(action_id, paths):
        return run_isolated(action_id, paths, opts, on_progress, cancel, on_reserved)
    return engine.run(action_id, paths, opts, on_progress=on_progress, cancel=cancel)


# ----- worker process ----------------------------------------------------------

def _worker(action_id: str, paths: list[str], opts: dict, q, lang: str = "") -> None:
    """Entry point of the worker process (no Qt here). `lang`: the language
    Cerclic speaks, so that its messages and the names it gives are the app's."""
    if os.environ.get("CERCLIC_TEST_WORKER_DIES"):   # tests: a native crash
        os._exit(3)
    if lang:
        i18n.set_language(lang)
    from . import paths as _paths
    _paths.add_reserve_hook(lambda p: q.put(("reserved", p)))
    res = engine.run(action_id, paths, opts,
                     on_progress=lambda f, t: q.put(("progress", f, t)))
    q.put(("done", dataclasses.asdict(res)))


def run_isolated(action_id: str, paths: list[str], opts: dict, on_progress=None,
                 cancel: threading.Event | None = None, on_reserved=None) -> engine.Result:
    import multiprocessing as mp
    ctx = mp.get_context("spawn")
    q = ctx.Queue()
    proc = ctx.Process(target=_worker,
                       args=(action_id, list(paths), dict(opts), q, i18n.current()),
                       daemon=True, name="cerclic-worker")
    proc.start()
    try:
        from .win.jobobject import kill_with_cerclic
        kill_with_cerclic(proc.pid)
    except Exception:
        pass
    reserved: list[str] = []
    result: engine.Result | None = None

    def handle(msg) -> None:
        nonlocal result
        kind = msg[0]
        if kind == "reserved":
            reserved.append(msg[1])
            if on_reserved:
                on_reserved(msg[1])
        elif kind == "progress" and on_progress:
            on_progress(msg[1], msg[2])
        elif kind == "done":
            result = engine.Result(**msg[1])

    try:
        while result is None:
            if cancel is not None and cancel.is_set():
                proc.kill()
                proc.join(5)
                engine._cleanup(reserved)
                return engine.Result(action_id, False, [], tr("Annulé"), cancelled=True)
            try:
                handle(q.get(timeout=0.1))
            except queue.Empty:
                if not proc.is_alive():
                    while result is None:      # read what it sent before ending
                        try:
                            handle(q.get_nowait())
                        except queue.Empty:
                            break
                    if result is None:
                        engine._cleanup(reserved)
                        return engine.Result(
                            action_id, False, [],
                            tr("Le traitement s'est arrêté net : le fichier est "
                               "probablement endommagé."))
        proc.join(10)
        return result
    finally:
        if proc.is_alive():
            proc.kill()
        q.close()
