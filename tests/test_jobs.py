"""Worker processes for heavy PDF work, journal of unfinished files, merging
of right-click bursts, password retries."""
import os
import threading
import time

import pymupdf

from cerclic import jobs
from cerclic.journal import Journal


def test_isolated_run_matches_in_thread(pdf_with_photo):
    res = jobs.run_isolated("pdf_compress", [pdf_with_photo], {})
    assert res.ok, res.error
    assert os.path.getsize(res.outputs[0]) < os.path.getsize(pdf_with_photo)
    seen = []
    res = jobs.run_isolated("pdf_to_images", [pdf_with_photo], {"fmt": "jpg"},
                            on_progress=lambda f, t: seen.append((f, t)))
    assert res.ok and len(res.outputs) == 2 and seen


def test_isolated_errors_come_back(tmp_path):
    bad = tmp_path / "broken.pdf"
    bad.write_bytes(b"%PDF-1.4 nothing")
    res = jobs.run_isolated("pdf_compress", [str(bad)], {})
    assert not res.ok and res.error
    assert sorted(os.listdir(tmp_path)) == ["broken.pdf"]


def test_isolated_cancel_kills_and_cleans(tmp_path):
    doc = pymupdf.open()
    for i in range(400):
        doc.new_page().insert_text((72, 72), f"Page {i}", fontsize=20)
    src = tmp_path / "long.pdf"
    doc.save(str(src))
    doc.close()
    cancel = threading.Event()
    reserved = []
    threading.Timer(1.5, cancel.set).start()
    t0 = time.monotonic()
    res = jobs.run_isolated("pdf_to_images", [str(src)], {"fmt": "png"}, cancel=cancel,
                            on_reserved=reserved.append)
    assert res.cancelled and time.monotonic() - t0 < 10
    assert reserved and not any(os.path.exists(p) for p in reserved)
    assert sorted(os.listdir(tmp_path)) == ["long.pdf"]


def test_isolated_worker_crash_is_reported(tmp_path, monkeypatch, pdf_3p):
    """If the worker dies (a native crash in a library), the app gets a clear
    error, keeps running, and nothing is left behind."""
    monkeypatch.setenv("CERCLIC_TEST_WORKER_DIES", "1")
    res = jobs.run_isolated("pdf_rotate", [pdf_3p], {"degrees": 90})
    assert not res.ok and "endommagé" in res.error
    assert sorted(os.listdir(os.path.dirname(pdf_3p))) == ["doc.pdf"]


def test_should_isolate(pdf_3p, pdf_with_photo, jpg_photo, monkeypatch):
    assert jobs.should_isolate("pdf_to_word", [pdf_3p])
    assert not jobs.should_isolate("pdf_compress", [pdf_3p])
    assert not jobs.should_isolate("img_compress", [jpg_photo])
    monkeypatch.setattr(jobs, "ISOLATE_BYTES", 1000)
    assert jobs.should_isolate("pdf_rotate", [pdf_with_photo])
    monkeypatch.setattr(jobs, "RENDERING_BYTES", 1000)
    assert jobs.should_isolate("pdf_compress", [pdf_with_photo])


def test_journal_recovers_unfinished(tmp_path):
    j = Journal(str(tmp_path / "pending.json"))
    done = tmp_path / "done (compressed).jpg"
    half = tmp_path / "half (compressed).mp4"
    folder = tmp_path / "doc (images)"
    for p in (done, half):
        p.write_bytes(b"x")
    folder.mkdir()
    (folder / "doc-01.jpg").write_bytes(b"x")
    j.add("a", str(done))
    j.finish("a")
    j.add("b", str(half))
    j.add("b", str(folder))
    removed = Journal(str(tmp_path / "pending.json")).recover()
    assert sorted(removed) == sorted([str(half), str(folder)])
    assert done.exists() and not half.exists() and not folder.exists()
    assert not (tmp_path / "pending.json").exists()


def test_journal_ignores_older_files(tmp_path):
    old = tmp_path / "user file.jpg"
    old.write_bytes(b"x")
    os.utime(old, (time.time() - 3600, time.time() - 3600))
    j = Journal(str(tmp_path / "pending.json"))
    j.add("a", str(old))
    assert Journal(str(tmp_path / "pending.json")).recover() == []
    assert old.exists()
