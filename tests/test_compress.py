"""« Compresser » with its popup: the size shown before compressing is the size
obtained, for pictures (exact), PDF (exact, and reused), videos and sounds
(estimated); the strengths; the result cards that say how much was gained."""
import os
import tempfile
import time

import pytest
from PIL import Image
from PySide6.QtCore import QPoint

from cerclic import engine, sizes
from cerclic.actions import images, video
from conftest import HAS_FFMPEG

needs_ffmpeg = pytest.mark.skipif(not HAS_FFMPEG, reason="ffmpeg missing")


@pytest.fixture(autouse=True)
def _close_windows():
    yield
    from PySide6.QtWidgets import QApplication
    for w in QApplication.topLevelWidgets():
        try:
            w.close()
        except RuntimeError:
            pass
    QApplication.processEvents()


# ----- sizes in words ------------------------------------------------------------------------

def test_sizes_in_words():
    assert sizes.human(0) == "0 octet" and sizes.human(512) == "512 octets"
    assert sizes.human(1536) == "1,5 Ko"
    assert sizes.human(4.2 * 1024 ** 2) == "4,2 Mo"
    assert sizes.human(612 * 1024) == "612 Ko"
    assert sizes.human(1023.7 * 1024) == "1,0 Mo"
    assert sizes.human(3 * 1024 ** 3) == "3,0 Go"
    assert sizes.gain(1000, 150) == "85 % de moins" and sizes.gain(100, 120) == "20 % de plus"
    assert sizes.change(4.2 * 1024 ** 2, 612 * 1024) == "De 4,2 Mo à 612 Ko · 86 % de moins"
    for text in (sizes.human(123456789), sizes.change(10, 5)):
        assert "—" not in text and "–" not in text


def test_size_of_counts_folders(tmp_path):
    (tmp_path / "d").mkdir()
    (tmp_path / "d" / "a.bin").write_bytes(b"x" * 300)
    (tmp_path / "b.bin").write_bytes(b"x" * 200)
    assert sizes.size_of([str(tmp_path / "d"), str(tmp_path / "b.bin"),
                          str(tmp_path / "gone")]) == 500


# ----- pictures: the size shown is the size made ---------------------------------------------------

@pytest.mark.parametrize("quality", [15, 45, 70, 90])
def test_picture_size_is_exact(jpg_photo, quality):
    pic = images.load(jpg_photo).to_srgb()
    _, ext, data = images.compressed_data(pic, ".jpg", quality)
    out = images.compress_image(jpg_photo, quality)
    assert ext == ".jpg" and os.path.getsize(out) == len(data)


def test_png_keeps_fewer_colours_as_quality_goes_down(png_with_alpha, tmp_path):
    assert [images.png_colors(q) for q in (95, 90, 70, 55, 40, 25, 10)] == \
        [None, None, 256, 128, 64, 32, 16]
    # a busy picture, so the palette has work to do
    import numpy as np
    rng = np.random.default_rng(5)
    arr = (rng.random((300, 400, 4)) * 255).astype("uint8")
    arr[..., 3] = 255
    src = tmp_path / "shot.png"
    Image.fromarray(arr, "RGBA").save(src)
    sizes_by_q = {}
    for q in (70, 40, 10):
        out = images.compress_image(str(src), q)
        with Image.open(out) as im:
            assert im.mode == "P" and len(im.getcolors(1000)) <= images.png_colors(q)
        sizes_by_q[q] = os.path.getsize(out)
    assert sizes_by_q[70] > sizes_by_q[40] > sizes_by_q[10]


def test_batch_says_which_files_gave_a_result(tmp_path, jpg_photo):
    other = tmp_path / "b.jpg"
    Image.open(jpg_photo).save(other, quality=97)
    res = engine.run("img_compress", [jpg_photo, str(other)], {"quality": 50})
    assert res.ok and res.sources == [jpg_photo, str(other)]


# ----- PDF strengths, and the result made once -----------------------------------------------------

def test_pdf_strengths(pdf_with_photo, tmp_path):
    made = {}
    for level in ("light", "medium", "strong", "max"):
        res = engine.run("pdf_compress", [pdf_with_photo],
                         {"level": level, "_out_dir": str(tmp_path / level)})
        assert res.ok, (level, res.error)
        made[level] = os.path.getsize(res.outputs[0])
    assert made["light"] > made["medium"] > made["strong"] > made["max"]
    default = engine.run("pdf_compress", [pdf_with_photo], {"_out_dir": str(tmp_path / "d")})
    assert os.path.getsize(default.outputs[0]) == made["medium"]


def test_pdf_result_made_by_the_popup_is_reused(pdf_with_photo, tmp_path):
    work = tempfile.mkdtemp(prefix="cerclic-compress-")
    est = engine.run("pdf_compress", [pdf_with_photo], {"level": "strong", "_out_dir": work})
    made = est.outputs[0]
    data = open(made, "rb").read()
    t = time.monotonic()
    res = engine.run("pdf_compress", [pdf_with_photo],
                     {"level": "strong", "precomputed": {pdf_with_photo: made}})
    assert res.ok and time.monotonic() - t < 2
    assert open(res.outputs[0], "rb").read() == data
    assert os.path.dirname(res.outputs[0]) == os.path.dirname(pdf_with_photo)
    assert not os.path.exists(made) and not os.path.exists(work)     # nothing left behind


# ----- videos and sounds ------------------------------------------------------------------------------

@pytest.fixture
def moving_video(tmp_path):
    """20 s of moving pictures with sound, closer to a real video than a still
    test pattern."""
    import subprocess
    p = tmp_path / "film.mp4"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
                    "-i", "testsrc2=size=960x540:rate=25:duration=20", "-f", "lavfi",
                    "-i", "sine=frequency=440:duration=20", "-c:v", "libx264", "-crf", "16",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest",
                    str(p)], check=True)
    return str(p)


@needs_ffmpeg
def test_video_strengths_and_estimates(moving_video, tmp_path):
    work = str(tmp_path / "w")
    os.mkdir(work)
    est, exact, made = video.estimate_compressed(moving_video, "medium", work)
    assert not exact and made is None                  # 20 s: measured on samples
    real = video.compress_video(moving_video, "medium")
    assert abs(est - os.path.getsize(real)) / os.path.getsize(real) < 0.1
    light = video.compress_video(moving_video, "light")
    tiny = video.compress_video(moving_video, "max")
    assert os.path.getsize(light) > os.path.getsize(real) > os.path.getsize(tiny)
    assert video.probe(tiny).height <= 480
    assert os.listdir(work) == []                      # the samples went


@needs_ffmpeg
def test_short_video_is_compressed_once(small_video, tmp_path):
    est, exact, made = video.estimate_compressed(small_video, "medium", str(tmp_path))
    assert exact and os.path.getsize(made) == est
    res = engine.run("vid_compress", [small_video],
                     {"level": "medium", "precomputed": {small_video: made}})
    assert res.ok and os.path.getsize(res.outputs[0]) == est and not os.path.exists(made)


@needs_ffmpeg
def test_still_video_with_a_busy_moment(tmp_path):
    """Samples go where the original spends its bytes."""
    import subprocess
    src = tmp_path / "burst.mp4"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-f", "lavfi", "-i", "color=c=0x336699:s=640x360:r=25:d=20",
                    "-f", "lavfi", "-i", "testsrc2=s=640x360:r=25:d=5",
                    "-f", "lavfi", "-i", "color=c=0x336699:s=640x360:r=25:d=8",
                    "-filter_complex", "[0:v][1:v][2:v]concat=n=3:v=1[v]", "-map", "[v]",
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(src)],
                   check=True)
    est = video.estimate_compressed(str(src), "medium", str(tmp_path))[0]
    real = os.path.getsize(video.compress_video(str(src), "medium"))
    assert abs(est - real) / real < 0.25


@needs_ffmpeg
def test_variable_frame_rate_keeps_its_pictures(tmp_path):
    import subprocess
    src = tmp_path / "vfr.mp4"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
                    "-i", "testsrc2=s=480x270:r=60:d=20", "-vf", "select='lt(random(0),0.45)'",
                    "-fps_mode", "vfr", "-c:v", "libx264", "-crf", "18", "-pix_fmt",
                    "yuv420p", str(src)], check=True)

    def pictures(p):
        out = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", p,
                              "-map", "0:v:0", "-c", "copy", "-f", "framecrc", "-"],
                             capture_output=True, text=True).stdout
        return sum(1 for line in out.splitlines() if line and not line.startswith("#"))
    out = video.compress_video(str(src), "medium")
    assert pictures(out) == pictures(str(src))         # none repeated to make a steady rate
    est = video.estimate_compressed(str(src), "medium", str(tmp_path))[0]
    assert abs(est - os.path.getsize(out)) / os.path.getsize(out) < 0.2


@needs_ffmpeg
def test_estimate_writes_its_statistics_in_the_work_folder(small_video, tmp_path, monkeypatch):
    """(ffmpeg opens -vstats_file in a way that does not take accented names on
    Windows: the file is named shortly, in the work folder given as cwd.)"""
    seen = []
    real_run = video._run

    def spy(args, duration, ctx, label, cwd=None):
        if "-vstats_file" in args:
            seen.append((args[args.index("-vstats_file") + 1], cwd))
        return real_run(args, duration, ctx, label, cwd=cwd)
    monkeypatch.setattr(video, "WHOLE_UP_TO", 0.0)      # (the 1 s clip goes through samples)
    monkeypatch.setattr(video, "SAMPLE_SECONDS", 0.3)
    monkeypatch.setattr(video, "_run", spy)
    work = tmp_path / "Hélène dossier"
    work.mkdir()
    video.estimate_compressed(small_video, "medium", str(work))
    assert seen and all(os.sep not in name and name.isascii() and cwd == str(work)
                        for name, cwd in seen)
    assert os.listdir(work) == []


@needs_ffmpeg
def test_sound_only_video_keeps_the_former_strength(tmp_path):
    import subprocess
    voice = tmp_path / "voix.mp4"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
                    "-i", "sine=frequency=330:duration=10", "-c:a", "aac", "-b:a", "256k",
                    str(voice)], check=True)
    res = engine.run("vid_compress", [str(voice)], {})
    assert res.ok and res.outputs[0].endswith(".mp3")
    kbps = os.path.getsize(res.outputs[0]) * 8 / 10 / 1000
    assert kbps == pytest.approx(96, rel=0.1)          # « Moyenne » of a video: 96 kbit/s sound


def test_mp3_ceiling_for_low_sample_rates():
    assert video.mp3_kbps(192, 8000) == 64 and video.mp3_kbps(192, 22050) == 160
    assert video.mp3_kbps(192, 44100) == 192 and video.mp3_kbps(96, 0) == 96


@needs_ffmpeg
def test_sound_strengths(wav_sound, tmp_path):
    est = {lv: video.estimate_compressed(wav_sound, lv, str(tmp_path))[0]
           for lv in ("light", "max")}
    light = video.compress_audio(wav_sound, "light")
    small = video.compress_audio(wav_sound, "max")
    assert os.path.getsize(light) > os.path.getsize(small)
    assert est["light"] == pytest.approx(os.path.getsize(light), rel=0.05)
    assert est["max"] == pytest.approx(os.path.getsize(small), rel=0.05)


# ----- the popup -------------------------------------------------------------------------------------

def _picture_editor(qtbot, paths, quality=70):
    from cerclic.ui.compress_editor import CompressEditor
    ed = CompressEditor(paths, "image", quality=quality)
    ed.start(QPoint(400, 400))
    qtbot.waitUntil(lambda: ed.after is not None and not ed._busy, timeout=20000)
    return ed


def test_popup_shows_the_size_it_will_make(qtbot, jpg_photo):
    ed = _picture_editor(qtbot, [jpg_photo], 70)
    assert ed.exact and ed.preview.image is not None
    assert "au lieu de" in ed.size_small.text() and "% de moins" in ed.size_small.text()
    ed.slider.setValue(30)
    qtbot.waitUntil(lambda: not ed._busy and ed._want is None
                    and ed.after < ed.before * 0.5, timeout=20000)
    shown = ed.after
    with qtbot.waitSignal(ed.accepted, timeout=2000) as sig:
        ed.validate()
    assert sig.args[0] == {"quality": 30}
    out = images.compress_image(jpg_photo, 30)
    assert os.path.getsize(out) == shown                # what was shown is what is made
    assert ed.size_big.text() == sizes.human(shown)


def test_popup_loupe_and_keys(qtbot, jpg_photo):
    from PySide6.QtCore import QPointF, Qt
    from PySide6.QtGui import QImage
    ed = _picture_editor(qtbot, [jpg_photo], 70)
    qtbot.keyClick(ed, Qt.Key_Left)
    assert ed.slider.value() == 65
    p = ed.preview
    p._mouse = QPointF(p.width() / 2, p.height() / 2)
    img = QImage(p.size(), QImage.Format_ARGB32)
    p.render(img)                                       # the loupe paints
    assert not img.isNull()


def test_popup_says_when_nothing_is_gained(qtbot, tmp_path):
    import numpy as np
    src = tmp_path / "light.jpg"
    noise = (np.random.default_rng(2).random((240, 320, 3)) * 255).astype("uint8")
    Image.fromarray(noise).save(src, quality=10, optimize=True)     # already very light
    ed = _picture_editor(qtbot, [str(src)], 95)
    assert not ed.ok_btn.isEnabled() and "Pas plus léger" in ed.size_big.text()


def test_popup_for_many_pictures_estimates(qtbot, tmp_path, jpg_photo):
    paths = []
    for i in range(5):
        p = tmp_path / f"p{i}.jpg"
        Image.open(jpg_photo).save(p, quality=95)
        paths.append(str(p))
    ed = _picture_editor(qtbot, paths, 50)
    assert not ed.exact and ed.size_big.text().startswith("≈ ")
    assert "5 images" in ed.batch_note.text()


def test_popup_batch_with_a_broken_picture(qtbot, tmp_path, jpg_photo):
    """A picture that cannot be read does not block the others; a scan of
    several pages, which the action leaves out, is not counted."""
    broken = tmp_path / "a0 cassée.jpg"
    broken.write_bytes(b"not a picture")
    scan = tmp_path / "scan.tif"
    pages = [Image.new("RGB", (400, 300), c) for c in ((255, 0, 0), (0, 0, 255))]
    pages[0].save(scan, save_all=True, append_images=pages[1:])
    good = tmp_path / "b1.jpg"
    Image.open(jpg_photo).save(good, quality=95)
    ed = _picture_editor(qtbot, [str(broken), str(scan), str(good)], 50)
    assert ed.ok_btn.isEnabled()
    assert ed.before == os.path.getsize(good)
    assert "2 laissées de côté" in ed.batch_note.text()


def test_popup_cannot_read_anything_still_lets_the_action_say_so(qtbot, tmp_path):
    from cerclic.ui.compress_editor import CompressEditor
    broken = tmp_path / "x.jpg"
    broken.write_bytes(b"nope")
    ed = CompressEditor([str(broken)], "image")
    ed.start(QPoint(400, 400))
    qtbot.waitUntil(ed.ok_btn.isEnabled, timeout=10000)
    assert "illisible" in ed.size_small.text()


def _levels_editor(qtbot, paths, kind, level=None, opts=None):
    from cerclic.ui.compress_editor import CompressEditor
    ed = CompressEditor(paths, kind, level=level, opts=opts)
    ed.start(QPoint(400, 400))
    qtbot.waitUntil(lambda: len(ed.results) == 4, timeout=60000)
    return ed


def test_popup_pdf_strengths_then_reuse(qtbot, pdf_with_photo):
    ed = _levels_editor(qtbot, [pdf_with_photo], "pdf")
    assert ed.level == "medium" and ed.level_buttons["medium"].isChecked()
    got = {lv: ed.results[lv][0] for lv in ("light", "medium", "strong", "max")}
    assert got["light"] > got["medium"] > got["strong"] > got["max"]
    ed.set_level("strong")
    assert ed.size_big.text() == sizes.human(got["strong"])
    workdir = ed._workdir
    with qtbot.waitSignal(ed.accepted, timeout=2000) as sig:
        ed.validate()
    res = sig.args[0]
    assert res["level"] == "strong" and os.path.isfile(res["precomputed"][pdf_with_photo])
    qtbot.wait(50)
    assert os.listdir(workdir) == [os.path.basename(res["precomputed"][pdf_with_photo])]
    run = engine.run("pdf_compress", [pdf_with_photo], res)
    assert run.ok and os.path.getsize(run.outputs[0]) == got["strong"]
    assert not os.path.exists(workdir)


def test_popup_closed_leaves_nothing(qtbot, pdf_with_photo):
    ed = _levels_editor(qtbot, [pdf_with_photo], "pdf")
    workdir = ed._workdir
    ed.cancel()
    qtbot.wait(50)
    assert not os.path.exists(workdir)


def test_stale_estimates_are_cleaned():
    from cerclic.ui import compress_editor
    old = tempfile.mkdtemp(prefix="cerclic-compress-")
    fresh = tempfile.mkdtemp(prefix="cerclic-compress-")
    past = time.time() - 10 * 3600
    os.utime(old, (past, past))
    compress_editor.clean_stale()
    assert not os.path.exists(old) and os.path.exists(fresh)
    os.rmdir(fresh)


@needs_ffmpeg
def test_popup_for_sounds(qtbot, wav_sound, m4a_sound):
    ed = _levels_editor(qtbot, [wav_sound, m4a_sound], "audio")
    assert ed.level == "strong"                        # 96 kbit/s, as before
    assert all(ed.results[lv][0] for lv in ("light", "max"))
    assert ed.level_buttons["max"].size.text().startswith("≈ ")


# ----- result cards ------------------------------------------------------------------------------------

def test_result_card_says_how_much_was_gained(qtbot, jpg_photo, tmp_path):
    from cerclic.engine import Result
    from cerclic.ui.cards import JobCard
    out = images.compress_image(jpg_photo, 40)
    card = JobCard("Compression")
    card.finish(Result("img_compress", True, [out], sources=[jpg_photo]))
    text = card._status.text()
    assert text.count("De ") == 1 and "% de moins" in text
    assert sizes.human(os.path.getsize(out)) in text
    other = JobCard("Rotation")
    rotated = images.rotate_image(jpg_photo, 90)
    other.finish(Result("img_rotate", True, [rotated], sources=[jpg_photo]))
    assert sizes.human(os.path.getsize(rotated)) + " · dans" in other._status.text()
    card.close()
    other.close()


# ----- from the wheel to the file ------------------------------------------------------------------------

@pytest.fixture
def cerclic_app(qtbot):
    from PySide6.QtWidgets import QApplication
    from cerclic.app import CerclicApp
    app = CerclicApp(QApplication.instance())
    yield app
    app.cards.close_all()
    if app.session:
        app.session.close()
    app.server.server.close()
    app.tray.hide()


def test_compress_flow_remembers_the_choice(qtbot, cerclic_app, jpg_photo, pdf_with_photo):
    from cerclic.ui.compress_editor import CompressEditor

    def editor():
        qtbot.waitUntil(lambda: any(isinstance(w, CompressEditor) and w.isVisible()
                                    for w in cerclic_app._live), timeout=5000)
        return next(w for w in cerclic_app._live if isinstance(w, CompressEditor))

    cerclic_app.start_action("img_compress", [jpg_photo], {}, QPoint(300, 300))
    ed = editor()
    qtbot.waitUntil(ed.ok_btn.isEnabled, timeout=20000)
    ed.slider.setValue(35)
    qtbot.waitUntil(lambda: not ed._busy and ed._want is None, timeout=20000)
    ed.validate()
    folder = os.path.dirname(jpg_photo)
    done = lambda n: sum(1 for c in cerclic_app.cards._cards        # noqa: E731
                         if getattr(c, "_outputs", None)) >= n
    qtbot.waitUntil(lambda: done(1), timeout=20000)
    assert any("(compressé)" in f for f in os.listdir(folder))
    assert cerclic_app.settings.get("compress_quality") == 35

    cerclic_app.start_action("pdf_compress", [pdf_with_photo], {}, QPoint(300, 300))
    ed = editor()
    ed.set_level("max")
    ed.validate()
    qtbot.waitUntil(lambda: done(2), timeout=60000)
    assert any(f.startswith("scan (compressé)") for f in os.listdir(folder))
    assert cerclic_app.settings.get("compress_levels") == {"pdf": "max"}
    cerclic_app.start_action("pdf_compress", [pdf_with_photo], {}, QPoint(300, 300))
    ed = editor()
    assert ed.level == "max"                           # proposed again
    ed.cancel()
