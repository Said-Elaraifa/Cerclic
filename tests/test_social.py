"""« Réseaux »: pictures and videos at the exact sizes of the social networks,
the popup that frames them, and the way the wheel offers them."""
import io
import os
import subprocess

import pytest
from PIL import Image
from PySide6.QtCore import QPoint, Qt

from cerclic import engine
from cerclic.actions import registry, social, video
from cerclic.errors import NothingToDo
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


@pytest.fixture
def halves(tmp_path):
    """1600 x 900, left half red, right half blue."""
    im = Image.new("RGB", (1600, 900), (220, 30, 30))
    im.paste((30, 30, 220), (800, 0, 1600, 900))
    p = tmp_path / "photo.jpg"
    im.save(p, quality=95)
    return str(p)


def _near(c, ref, tol=40):
    return all(abs(a - b) <= tol for a, b in zip(c, ref))


RED, BLUE = (220, 30, 30), (30, 30, 220)


# ----- formats and framing -------------------------------------------------------------------

def test_formats_are_the_networks_sizes():
    sizes = {f.key: (f.width, f.height) for f in social.FORMATS}
    assert sizes == {"square": (1080, 1080), "portrait": (1080, 1350),
                     "grid": (1080, 1440), "story": (1080, 1920),
                     "landscape": (1920, 1080), "banner": (1200, 630)}
    for f in social.FORMATS:
        assert f.where and f.ratio and f.tag and f.width % 2 == 0 and f.height % 2 == 0
        assert ":" not in f.tag and "/" not in f.tag          # fine in a file name


def test_place_box():
    assert social.place_box(1600, 900, 1.0) == (350, 0, 1250, 900)
    assert social.place_box(1600, 900, 1.0, (0.0, 0.5)) == (0, 0, 900, 900)
    assert social.place_box(1600, 900, 1.0, (1.0, 0.5)) == (700, 0, 1600, 900)
    assert social.place_box(1600, 900, 1.0, zoom=2) == (575, 225, 1025, 675)
    x0, y0, x1, y1 = social.place_box(900, 1600, 16 / 9)       # a tall picture, wide frame
    assert (x0, x1) == (0, 900) and y1 - y0 == pytest.approx(506.25)
    assert social.place_box(100, 100, 1.0, zoom=50)[2] == pytest.approx(
        50 + 50 / social.MAX_ZOOM)                               # zoom is limited
    assert social.place_box(100, 100, 1.0, (0.5, 0.5), zoom=0.2) == (0, 0, 100, 100)


@pytest.mark.parametrize("key", [f.key for f in social.FORMATS])
@pytest.mark.parametrize("mode", social.MODES)
def test_every_format_and_background_has_the_exact_size(tmp_path, key, mode):
    src = tmp_path / "small.png"
    Image.new("RGB", (300, 200), (90, 160, 90)).save(src)
    out = social.social_image(str(src), key, mode)
    f = social.BY_KEY[key]
    with Image.open(out) as im:
        assert im.format == "JPEG" and im.size == (f.width, f.height)
    assert os.path.basename(out) == f"small ({f.tag}).jpg"


def test_fill_keeps_the_part_chosen(halves):
    out = social.social_image(halves, "square", "fill", (0.0, 0.5))
    with Image.open(out) as im:
        assert _near(im.getpixel((540, 540)), RED) and _near(im.getpixel((1075, 540)), BLUE)
    out = social.social_image(halves, "square", "fill", (1.0, 0.5))
    with Image.open(out) as im:
        assert _near(im.getpixel((5, 540)), RED) and _near(im.getpixel((540, 540)), BLUE)
    out = social.social_image(halves, "story", "fill", (0.75, 0.5), zoom=2.0)
    with Image.open(out) as im:                        # zoomed into the blue half
        assert all(_near(im.getpixel((x, 960)), BLUE) for x in (5, 540, 1075))


def test_whole_picture_on_bands(halves):
    white = social.social_image(halves, "story", "white")
    black = social.social_image(halves, "story", "black")
    blur = social.social_image(halves, "story", "blur")
    with Image.open(white) as w, Image.open(black) as b, Image.open(blur) as bl:
        assert _near(w.getpixel((540, 40)), (255, 255, 255), 6)
        assert _near(b.getpixel((540, 40)), (0, 0, 0), 6)
        band = bl.getpixel((540, 40))
        assert not _near(band, (255, 255, 255), 30) and not _near(band, (0, 0, 0), 30)
        for im in (w, b, bl):                          # the picture itself, all of it
            assert _near(im.getpixel((20, 960)), RED) and _near(im.getpixel((1060, 960)), BLUE)


def test_transparent_picture_becomes_a_jpg(png_with_alpha):
    white = social.social_image(png_with_alpha, "square", "white")
    black = social.social_image(png_with_alpha, "square", "black")
    fill = social.social_image(png_with_alpha, "square", "fill")
    with Image.open(white) as w, Image.open(black) as b, Image.open(fill) as f:
        assert w.mode == b.mode == f.mode == "RGB"
        assert _near(w.getpixel((540, 540)), (255, 255, 255), 30)   # see-through: white
        assert _near(b.getpixel((540, 540)), (0, 0, 0), 30)         # or black
        assert _near(f.getpixel((540, 540)), (255, 255, 255), 30)


def test_phone_photo_upright_and_without_its_gps(tmp_path, jpg_rotated_exif):
    # stored 400 x 200 with "turn 90": upright 200 x 400, the blue band on top
    out = social.social_image(jpg_rotated_exif, "square", "fill", (0.5, 0.0))
    with Image.open(out) as im:
        assert _near(im.getpixel((540, 60)), (50, 50, 200), 50)
        assert _near(im.getpixel((540, 1000)), (200, 50, 50), 50)
    gps = tmp_path / "gps.jpg"
    exif = Image.Exif()
    exif[0x8825] = {1: "N", 2: (48.0, 51.0, 24.0)}
    Image.new("RGB", (640, 480), (10, 120, 200)).save(gps, exif=exif.tobytes())
    with Image.open(social.social_image(str(gps), "portrait", "blur")) as im:
        assert not im.getexif()                         # nothing about the place


def test_already_at_the_size(tmp_path):
    src = tmp_path / "post.jpg"
    Image.new("RGB", (1080, 1080), (200, 200, 30)).save(src)
    with pytest.raises(NothingToDo):
        social.social_image(str(src), "square", "fill")
    res = engine.run("img_social", [str(src)], {"social": "square"})
    assert res.info and "1080 × 1080" in res.error
    res = engine.run("img_social", [str(src)], {"social": "story"})   # another shape: done
    assert res.ok


def test_batch_with_one_framing_per_file(tmp_path, halves):
    other = tmp_path / "other.jpg"
    Image.open(halves).save(other)
    opts = {"social": "square", "social_mode": "fill",
            "social_frames": {halves: (0.0, 0.5, 1.0)}}       # the other one: centred
    res = engine.run("img_social", [halves, str(other)], opts)
    assert res.ok and len(res.outputs) == 2
    first, second = sorted(res.outputs, key=lambda p: "other" in p)
    with Image.open(first) as a, Image.open(second) as b:
        assert _near(a.getpixel((540, 540)), RED)
        assert _near(b.getpixel((300, 540)), RED) and _near(b.getpixel((800, 540)), BLUE)


def test_already_at_the_size_whatever_the_zoom_kept(tmp_path):
    src = tmp_path / "post.jpg"
    Image.new("RGB", (1080, 1080), (200, 200, 30)).save(src)
    with pytest.raises(NothingToDo):                   # (a zoom only counts in Remplir)
        social.social_image(str(src), "square", "blur", zoom=2.0)
    assert social.social_image(str(src), "square", "fill", zoom=2.0)


def test_animation_gives_its_first_picture(animated_gif):
    out = social.social_image(animated_gif, "square", "white")
    with Image.open(out) as im:
        assert im.format == "JPEG" and _near(im.getpixel((540, 540)), (255, 0, 0), 30)


def test_batch_goes_on_without_a_bad_file(tmp_path, halves):
    bad = tmp_path / "abîmée.jpg"
    bad.write_bytes(b"not a picture")
    res = engine.run("img_social", [halves, str(bad)], {"social": "story"})
    assert res.ok and len(res.outputs) == 1
    assert res.notes and "abîmée.jpg" in res.notes[0]
    assert not any("abîmée (" in f for f in os.listdir(tmp_path))   # nothing left of it
    res = engine.run("img_social", [str(bad), str(bad) + "2.jpg"], {"social": "story"})
    assert not res.ok and "abîmée.jpg" in res.error   # all of them: the first one is named


def test_a_file_that_fails_halfway_leaves_nothing(tmp_path):
    from cerclic import paths
    from cerclic.errors import UserError
    a, b = tmp_path / "a.jpg", tmp_path / "b.jpg"
    a.write_bytes(b"x")
    b.write_bytes(b"x")

    def half(p):
        out = paths.output_for(p, "story", ".jpg")     # reserved, then b fails
        if p.endswith("b.jpg"):
            raise UserError("raté")
        return out
    with paths.tracking():
        assert registry.each([str(a), str(b)], None, half) == [str(tmp_path / "a (story).jpg")]
        with pytest.raises(UserError):
            registry.each([str(b)], None, half)
    assert sorted(os.listdir(tmp_path)) == ["a (story).jpg", "a.jpg", "b.jpg"]


def test_enlarged_warning():
    f = social.BY_KEY["story"]
    assert social.enlarged(1600, 900, f, "fill")           # 506 px wide kept for 1080
    assert not social.enlarged(4032, 3024, f, "fill")
    assert social.enlarged(4032, 3024, f, "fill", zoom=3)
    assert social.enlarged(800, 450, f, "blur") and not social.enlarged(4000, 2250, f, "blur")


# ----- videos ---------------------------------------------------------------------------------

def test_video_filters():
    f = social.BY_KEY["story"]
    fill = social.video_filter(1920, 1080, f, "fill", (0.5, 0.5), 1.0)
    assert "iw*0.316406" in fill and "scale=1080:1920" in fill and fill.endswith("[v]")
    assert "fps=60" in social.video_filter(1920, 1080, f, "fill", fps=240)
    assert "fps=60" not in social.video_filter(1920, 1080, f, "fill", fps=59.94)
    blur = social.video_filter(1920, 1080, f, "blur")
    assert "gblur" in blur and "overlay" in blur and blur.endswith("format=yuv420p[v]")
    assert "color=white" in social.video_filter(1920, 1080, f, "white")
    with pytest.raises(ValueError):
        social.video_filter(1920, 1080, f, "sepia")


@needs_ffmpeg
@pytest.mark.parametrize("key,mode", [("story", "blur"), ("square", "fill"),
                                      ("landscape", "black"), ("portrait", "white")])
def test_video_in_every_shape(small_video, key, mode):
    out = social.social_video(small_video, key, mode)
    info = video.probe(out)
    f = social.BY_KEY[key]
    assert (info.width, info.height) == (f.width, f.height)
    assert info.has_audio and info.duration == pytest.approx(1.0, abs=0.15)
    assert out.endswith(f"clip ({f.tag}).mp4")


def _frame(path, t=0.5):
    return Image.open(io.BytesIO(video.frame_png(path, t, 2000, 2000))).convert("RGB")


@needs_ffmpeg
def test_video_framing_follows_the_choice(tmp_path):
    src = tmp_path / "halves.mp4"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
                    "-i", "color=c=red:s=640x360:d=1,drawbox=x=320:y=0:w=320:h=360:"
                    "color=blue:t=fill", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(src)],
                   check=True)
    left = _frame(social.social_video(str(src), "square", "fill", (0.0, 0.5)))
    right = _frame(social.social_video(str(src), "square", "fill", (1.0, 0.5)))
    mid = (left.width // 2, left.height // 2)
    assert left.size == right.size and left.width == left.height
    assert left.getpixel(mid)[0] > 150 and right.getpixel(mid)[2] > 150


@needs_ffmpeg
def test_video_filmed_upright_and_stretched_pixels(tmp_path):
    """A phone video stored sideways is framed as it is seen; a video with
    stretched pixels too (its picture is not squeezed)."""
    plain = tmp_path / "plain.mp4"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
                    "-i", "color=c=red:s=640x360:d=1,drawbox=x=0:y=0:w=160:h=360:"
                    "color=blue:t=fill", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    str(plain)], check=True)
    rot = tmp_path / "phone.mp4"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-display_rotation", "90", "-i", str(plain), "-c", "copy", str(rot)],
                   check=True)
    info = video.probe(str(rot))
    assert info.rotated and info.display_size == (360, 640)
    out = social.social_video(str(rot), "story", "fill")         # same shape: all kept
    made = video.probe(out)
    assert (made.width, made.height) == (1080, 1920) and not made.rotated
    seen, shot = _frame(str(rot)), _frame(out)                   # both fitted the same way
    assert seen.size == shot.size

    def blue_rows(im):
        return [y for y in range(0, im.height, 10) if im.getpixel((im.width // 2, y))[2] > 150]
    a, b = blue_rows(seen), blue_rows(shot)
    assert a and abs(len(a) - len(b)) <= 2 and abs(a[0] - b[0]) <= 20

    sar = tmp_path / "sar.mp4"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
                    "-i", "color=c=green:s=320x240:d=1", "-vf", "setsar=2",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(sar)], check=True)
    info = video.probe(str(sar))
    assert info.sar == 2 and info.display_size == (640, 240)
    w, h = _frame(str(sar)).size
    assert w / h == pytest.approx(640 / 240, rel=0.01)  # the preview is not squeezed
    made = video.probe(social.social_video(str(sar), "landscape", "fill"))
    assert (made.width, made.height, made.sar) == (1920, 1080, 1.0)


@needs_ffmpeg
def test_published_video_keeps_no_tags(tmp_path):
    src = tmp_path / "tour.mp4"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
                    "-i", "testsrc=size=320x240:rate=10:duration=1", "-c:v", "libx264",
                    "-pix_fmt", "yuv420p", "-metadata", "location=+48.8566+002.3522/",
                    "-metadata", "title=Chez moi", str(src)], check=True)
    out = social.social_video(str(src), "square", "black")
    banner = subprocess.run(["ffmpeg", "-hide_banner", "-i", out], capture_output=True,
                            text=True).stderr
    assert "48.8566" not in banner and "Chez moi" not in banner


@needs_ffmpeg
def test_tiny_and_one_picture_videos(tmp_path):
    tiny = tmp_path / "tiny.mp4"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
                    "-i", "testsrc=size=16x16:rate=10:duration=1", "-c:v", "libx264",
                    "-pix_fmt", "yuv420p", str(tiny)], check=True)
    made = video.probe(social.social_video(str(tiny), "banner", "fill", zoom=6.0))
    assert (made.width, made.height) == (1200, 630)
    one = tmp_path / "one.mp4"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
                    "-i", "color=c=red:s=320x240:d=1", "-frames:v", "1", "-c:v", "libx264",
                    "-pix_fmt", "yuv420p", str(one)], check=True)
    from cerclic.ui.social_editor import load_preview
    pil, full = load_preview(str(one), 400)
    assert full == (320, 240) and pil.size[0] > 0


@needs_ffmpeg
def test_song_with_its_cover_is_not_a_video(tmp_path):
    cover = tmp_path / "cover.png"
    Image.new("RGB", (300, 300), (240, 80, 20)).save(cover)
    song = tmp_path / "titre.mp4"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
                    "-i", "sine=frequency=330:duration=1", "-i", str(cover), "-map", "0",
                    "-map", "1", "-c:a", "aac", "-c:v", "png", "-disposition:v:0",
                    "attached_pic", str(song)], check=True)
    info = video.probe(str(song))
    assert info.has_audio and not info.has_video
    res = engine.run("vid_social", [str(song)], {"social": "story"})
    assert not res.ok and "son" in res.error


@needs_ffmpeg
def test_sound_only_video_is_refused(tmp_path):
    p = tmp_path / "voice.mp4"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
                    "-i", "sine=frequency=330:duration=1", "-c:a", "aac", str(p)], check=True)
    res = engine.run("vid_social", [str(p)], {"social": "story"})
    assert not res.ok and "son" in res.error


# ----- the wheel ---------------------------------------------------------------------------------

def test_wheel_offers_social_formats(jpg_photo, small_video, tmp_path):
    from cerclic.ui.radial import ring_split
    menu = registry.menu_for([jpg_photo])
    main, more = ring_split(menu["image"])
    assert [a.label for a in main] == ["Rogner", "Réseaux", "Pivoter", "Redimensionner",
                                       "Compresser", "Convertir", "En PDF"]
    assert [a.label for a in more] == ["Copier", "Anonymiser"]
    assert "Réseaux" in [a.label for a in registry.menu_for([small_video])["video"]]


def test_every_action_stays_reachable(tmp_path, jpg_photo, pdf_3p, pdf_2p, small_video):
    """Whatever the selection, each action is on the ring or under « Plus »,
    and the ring never has more than 8 slices."""
    from cerclic.ui.radial import MAX_SLICES, ring_split
    png = tmp_path / "b.png"
    Image.new("RGB", (40, 30)).save(png)
    song = tmp_path / "s.m4a"
    song.write_bytes(b"x")
    for paths in ([jpg_photo], [jpg_photo, str(png)], [pdf_3p], [pdf_3p, pdf_2p],
                  [small_video], [small_video, small_video + "2.mp4"], [str(song)]):
        for cat, actions in registry.menu_for(paths).items():
            main, more = ring_split(actions)
            assert sorted(a.id for a in main + more) == sorted(a.id for a in actions)
            assert len(main) + (1 if more else 0) <= MAX_SLICES
            assert len(more) <= MAX_SLICES


# ----- the popup -------------------------------------------------------------------------------------

def _editor(qtbot, paths, *args):
    from cerclic.ui.social_editor import SocialEditor
    ed = SocialEditor(paths, *args)
    ed.start(QPoint(400, 400))
    qtbot.waitUntil(lambda: ed.canvas.image is not None, timeout=10000)
    return ed


def test_popup_shows_the_shape_and_returns_the_choice(qtbot, halves):
    ed = _editor(qtbot, [halves])
    c = ed.canvas
    assert c.fmt.key == "portrait" and c.mode == "fill"          # pictures: a post
    for f in social.FORMATS:
        ed.format_buttons[f.key].click()
        F = c.frame_rect()
        assert F.width() / F.height() == pytest.approx(f.aspect, rel=0.01)
        assert ed.format_buttons[f.key].isChecked()
        assert f.size_text in ed.info.text()
    ed.format_buttons["square"].click()
    # drag the picture to the left: the right part (blue) comes into the frame
    F = c.frame_rect()
    start = F.center().toPoint()
    qtbot.mousePress(c, Qt.LeftButton, pos=start)
    qtbot.mouseMove(c, start - QPoint(400, 0))
    qtbot.mouseRelease(c, Qt.LeftButton, pos=start - QPoint(400, 0))
    assert c.shown_center()[0] == pytest.approx((1600 - 450) / 1600)   # as far as it goes
    # zoom with the wheel, then a double-click puts it back
    c.zoom_by(2.0, F.center())
    assert c.zoom == pytest.approx(2.0)
    qtbot.mouseDClick(c, Qt.LeftButton, pos=F.center().toPoint())
    assert c.zoom == 1.0 and c.shown_center() == pytest.approx((0.5, 0.5))
    c.move_by(300, 0)                                             # the red side
    ed.mode_buttons["blur"].click()
    assert "Rien n'est coupé" in ed.hint_label.text()
    ed.mode_buttons["fill"].click()
    with qtbot.waitSignal(ed.accepted, timeout=2000) as sig:
        qtbot.keyClick(ed, Qt.Key_Return)
    res = sig.args[0]
    assert res["social"] == "square" and res["social_mode"] == "fill"
    cx, cy, zoom = res["social_frames"][halves]
    assert cx < 0.5 and zoom == 1.0
    # what the popup showed is what is made
    out = social.social_image(halves, res["social"], res["social_mode"], (cx, cy), zoom)
    with Image.open(out) as im:
        assert _near(im.getpixel((540, 540)), RED)


def test_popup_paints_every_background(qtbot, halves, png_with_alpha):
    from PySide6.QtGui import QImage
    ed = _editor(qtbot, [halves, png_with_alpha], "story", "blur")
    for mode in social.MODES:
        ed.set_mode(mode)
        img = QImage(ed.canvas.size(), QImage.Format_ARGB32)
        ed.canvas.render(img)
        F = ed.canvas.frame_rect()
        top = img.pixelColor(int(F.center().x()), int(F.top() + 6))
        if mode == "white":
            assert top.lightness() > 245
        elif mode == "black":
            assert top.lightness() < 10
    ed.goto(1)                                         # the next file
    qtbot.waitUntil(lambda: ed.canvas.image is not None and ed.index == 1, timeout=10000)
    assert ed.count_label.text() == "2 / 2" and ed.title_label.text() == "shot.png"


def test_popup_keeps_a_framing_per_file(qtbot, halves, tmp_path):
    other = str(tmp_path / "other.jpg")
    Image.open(halves).save(other)
    ed = _editor(qtbot, [halves, other], "square", "fill")
    ed.canvas.move_by(400, 0)                          # first file: the left part
    left = ed.canvas.shown_center()
    qtbot.keyClick(ed, Qt.Key_PageDown)
    qtbot.waitUntil(lambda: ed.index == 1 and ed.canvas.image is not None, timeout=10000)
    assert ed.canvas.shown_center() == pytest.approx((0.5, 0.5))
    qtbot.keyClick(ed, Qt.Key_Plus)                    # second file: zoomed in
    assert ed.canvas.zoom == pytest.approx(1.15)
    ed.goto(0)
    qtbot.waitUntil(lambda: ed.index == 0 and ed.canvas.image is not None, timeout=10000)
    assert ed.canvas.shown_center() == pytest.approx(left)
    with qtbot.waitSignal(ed.accepted, timeout=2000) as sig:
        ed.validate()
    frames = sig.args[0]["social_frames"]
    assert frames[halves][0] == pytest.approx(left[0]) and frames[other][2] == pytest.approx(1.15)


def test_preview_size():
    from cerclic.ui.social_editor import PREVIEW_PIXELS, preview_box
    assert preview_box(20000, 300, 1256) == (20000, 300)          # a panorama keeps its height
    assert preview_box(4000, 3000, 1256) == (1675, 1256)
    assert preview_box(800, 600, 1256) == (800, 600)               # never enlarged
    w, h = preview_box(100000, 1000, 3000)
    assert w * h <= PREVIEW_PIXELS * 1.001 and w / h == pytest.approx(100, rel=0.01)


def test_preview_in_screen_colours(tmp_path):
    from cerclic.ui.social_editor import load_preview
    cmyk = tmp_path / "print.jpg"
    Image.new("CMYK", (400, 300), (0, 200, 200, 0)).save(cmyk, quality=95)
    pil, full = load_preview(str(cmyk), 600)
    assert pil.mode == "RGB" and full == (400, 300)
    out = social.social_image(str(cmyk), "landscape", "white")
    with Image.open(out) as im:                        # what is shown is what is made
        assert _near(pil.getpixel((200, 150)), im.getpixel((960, 540)), 12)


def test_popup_arrow_keys_and_bad_file(qtbot, halves, tmp_path):
    ed = _editor(qtbot, [halves], "square", "fill")
    x = ed.canvas.shown_center()[0]
    qtbot.keyClick(ed, Qt.Key_Left)                    # the picture moves left
    assert ed.canvas.shown_center()[0] > x
    bad = tmp_path / "bad.jpg"
    bad.write_bytes(b"not a picture")
    from cerclic.ui.social_editor import SocialEditor
    ed2 = SocialEditor([str(bad)])
    ed2.start(QPoint(400, 400))
    qtbot.waitUntil(lambda: ed2.canvas.message not in ("", "Chargement…"), timeout=5000)
    assert not ed2.ok_btn.isEnabled()


@needs_ffmpeg
def test_popup_for_a_video(qtbot, small_video):
    ed = _editor(qtbot, [small_video])
    assert ed.canvas.fmt.key == "story" and ed.canvas.mode == "blur"   # videos: a reel
    assert ed.canvas.full == (640, 480)
    with qtbot.waitSignal(ed.accepted, timeout=2000):
        ed.validate()


# ----- from the wheel to the file -------------------------------------------------------------------

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


def test_social_flow_end_to_end(qtbot, cerclic_app, halves):
    from cerclic.ui.social_editor import SocialEditor
    cerclic_app.start_action("img_social", [halves], {}, QPoint(300, 300))
    qtbot.waitUntil(lambda: any(isinstance(w, SocialEditor) for w in cerclic_app._live),
                    timeout=3000)
    ed = next(w for w in cerclic_app._live if isinstance(w, SocialEditor))
    qtbot.waitUntil(lambda: ed.canvas.image is not None, timeout=10000)
    ed.set_format(social.BY_KEY["story"])
    ed.set_mode("blur")
    ed.validate()
    folder = os.path.dirname(halves)
    qtbot.waitUntil(lambda: "photo (story).jpg" in os.listdir(folder), timeout=10000)
    qtbot.waitUntil(lambda: any(getattr(c, "_outputs", None) for c in cerclic_app.cards._cards),
                    timeout=8000)
    with Image.open(os.path.join(folder, "photo (story).jpg")) as im:
        assert im.size == (1080, 1920)
    assert cerclic_app.settings.get("social_last")["image"] == ["story", "blur"]
    # next time, the popup proposes the same
    cerclic_app.start_action("img_social", [halves], {}, QPoint(300, 300))
    qtbot.waitUntil(lambda: any(isinstance(w, SocialEditor) and w.isVisible()
                                for w in cerclic_app._live), timeout=3000)
    ed = next(w for w in cerclic_app._live if isinstance(w, SocialEditor))
    assert ed.canvas.fmt.key == "story" and ed.canvas.mode == "blur"
    ed.cancel()


def test_scan_with_pages_is_announced_before_the_popup(qtbot, cerclic_app, tmp_path):
    from cerclic.ui.social_editor import SocialEditor
    tif = tmp_path / "scan.tif"
    pages = [Image.new("RGB", (200, 300), c) for c in ((255, 0, 0), (0, 255, 0))]
    pages[0].save(tif, save_all=True, append_images=pages[1:])
    cerclic_app.start_action("img_social", [str(tif)], {}, QPoint(300, 300))
    qtbot.wait(200)
    assert not any(isinstance(w, SocialEditor) for w in cerclic_app._live)
    assert cerclic_app.cards._cards
