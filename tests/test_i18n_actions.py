"""The actions in another language (a small fake English catalogue): names of
the files made, sizes, messages, and the worker process for heavy PDFs."""
import os
import queue
import threading

import pytest

from cerclic import engine, i18n, jobs, locales, paths, sizes
from cerclic.actions import images
from cerclic.errors import NeedsPassword

FAKE = {
    "compressé": "compressed",
    "rogné": "cropped/cut?",                 # characters no file name may hold
    "pivoté": "turned",
    "{n} octet": ["{n} byte", "{n} bytes"],
    "{size} Ko": "{size} KB",
    "{size} Mo": "{size} MB",
    "{size} Go": "{size} GB",
    "{pct} % de moins": "{pct}% smaller",
    "même taille": "same size",
    "De {before} à {after}": "From {before} to {after}",
    "La zone à rogner est vide.": "The area to crop is empty.",
    "Assembler": "Combine",
    "{action} : il faut au moins {n} fichier.": ["{action}: needs at least {n} file.",
                                                 "{action}: needs at least {n} files."],
    "Ce PDF est protégé par un mot de passe.": "This PDF is password protected.",
    "«\xa0{name}\xa0» est protégé par un mot de passe.": "“{name}” is password protected.",
}


@pytest.fixture
def english(monkeypatch):
    monkeypatch.delenv("CERCLIC_LANG", raising=False)
    monkeypatch.setattr(locales, "load", lambda code: dict(FAKE) if code == "en" else {})
    assert i18n.set_language("en") == "en"
    try:
        yield
    finally:
        i18n.set_language("fr")


def test_result_names_in_the_language(english, jpg_photo):
    out = images.compress_image(jpg_photo, 50)
    assert os.path.basename(out) == "photo (compressed).jpg"
    out = images.crop_image(jpg_photo, (10, 10, 200, 200))
    assert os.path.basename(out) == "photo (cropped cut).jpg"
    i18n.set_language("fr")
    out = images.compress_image(jpg_photo, 50)
    assert os.path.basename(out) == "photo (compressé).jpg"


def test_sizes_in_the_language(english):
    b = sizes.BASE
    assert sizes.human(1) == "1 byte" and sizes.human(512) == "512 bytes"
    assert sizes.human(1.2 * b ** 2) == "1.2 MB"
    assert sizes.human(612 * b) == "612 KB"
    assert sizes.change(4.2 * b ** 2, 612 * b) == "From 4.2 MB to 612 KB · 86% smaller"
    assert sizes.gain(100, 100) == "same size"


def test_messages_in_the_language(english, jpg_photo, pdf_locked):
    res = engine.run("img_crop", [jpg_photo], {"crop_box": (5, 5, 5, 5)})
    assert res.error == "The area to crop is empty."
    res = engine.run("img_assemble", [jpg_photo], {})
    assert res.error == "Combine: needs at least 2 files."
    assert str(NeedsPassword()) == "This PDF is password protected."
    res = engine.run("pdf_rotate", [pdf_locked], {"degrees": 90})
    assert res.needs_password and res.error == "“locked.pdf” is password protected."


class _Queue(queue.Queue):
    def close(self):
        pass


class _Process:
    """Runs the worker here, starting in French as a new process does."""
    seen: list = []

    def __init__(self, target, args, **kw):
        self.target, self.args, self.pid = target, args, os.getpid()
        _Process.seen.append(args)

    def start(self):
        i18n.set_language("fr")
        t = threading.Thread(target=self.target, args=self.args)
        t.start()
        t.join()

    def is_alive(self):
        return False

    def join(self, timeout=None):
        pass

    def kill(self):
        pass


class _Spawn:
    Queue = _Queue
    Process = _Process


def test_worker_process_speaks_the_app_language(english, monkeypatch, pdf_3p):
    import multiprocessing
    monkeypatch.setattr(multiprocessing, "get_context", lambda method: _Spawn)
    monkeypatch.setattr(paths, "_hooks", [])
    _Process.seen.clear()
    res = jobs.run_isolated("pdf_crop", [pdf_3p], {"crop_rel": (0.5, 0.5, 0.5, 0.5)})
    assert _Process.seen[-1][-1] == "en"
    assert res.error == "The area to crop is empty."
    i18n.set_language("en")
    res = jobs.run_isolated("pdf_rotate", [pdf_3p], {"degrees": 90})
    assert res.ok and os.path.basename(res.outputs[0]) == "doc (turned).pdf"
