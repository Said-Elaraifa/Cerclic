"""Every action, end to end through the engine, on real files.

Each test checks the output exists, sits beside the source, is right, and that
the original is untouched.
"""
import hashlib
import os
import threading

import pymupdf
import pytest
from PIL import Image, ImageChops

from cerclic import engine
from cerclic.actions import images, pdf, registry
from conftest import HAS_FFMPEG


def _ok(res):
    assert res.ok, res.error
    for o in res.outputs:
        assert os.path.exists(o), o
        assert os.path.getsize(o) > 0, o
    return res.outputs


def _sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def _render(page, dpi=72):
    pix = page.get_pixmap(dpi=dpi, alpha=False)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def _changed(a, b, threshold=60):
    """Bounding box of what clearly changed between two renders (ignores
    tiny anti-aliasing differences)."""
    d = ImageChops.difference(a, b).convert("L")
    return d.point(lambda v: 255 if v > threshold else 0).getbbox()


def _open_fds_to(path):
    """Paths this process still has open (Linux), to catch leaked handles."""
    if not os.path.isdir("/proc/self/fd"):
        return []
    out = []
    for fd in os.listdir("/proc/self/fd"):
        try:
            if os.readlink(f"/proc/self/fd/{fd}") == os.path.abspath(path):
                out.append(fd)
        except OSError:
            pass
    return out


# ---- images --------------------------------------------------------------------

def test_convert_formats_keep_original(png_with_alpha):
    before = _sha(png_with_alpha)
    for fmt, ext in (("jpg", ".jpg"), ("png", ".png"), ("webp", ".webp")):
        out = _ok(engine.run("img_convert", [png_with_alpha], {"fmt": fmt}))[0]
        assert out.lower().endswith(ext)
        assert os.path.dirname(out) == os.path.dirname(png_with_alpha)
    assert _sha(png_with_alpha) == before


def test_jpg_flattens_alpha_on_white(png_with_alpha):
    out = _ok(engine.run("img_convert", [png_with_alpha], {"fmt": "jpg"}))[0]
    with Image.open(out) as im:
        assert im.mode == "RGB"
        assert im.getpixel((5, 5))[0] > 240      # transparent became white


def test_source_file_is_released(jpg_photo):
    _ok(engine.run("img_rotate", [jpg_photo], {"degrees": 90}))
    _ok(engine.run("img_crop", [jpg_photo], {"crop_box": (0, 0, 100, 100)}))
    assert _open_fds_to(jpg_photo) == []


def test_compress_smaller_same_size(jpg_photo):
    out = _ok(engine.run("img_compress", [jpg_photo], {"quality": 60}))[0]
    assert os.path.getsize(out) < os.path.getsize(jpg_photo)
    assert images.image_size(out) == images.image_size(jpg_photo)


def test_compress_png_quantizes(png_with_alpha, tmp_path):
    import numpy as np
    arr = (np.random.default_rng(3).random((400, 600, 4)) * 255).astype("uint8")
    arr[..., 3] = 255
    src = tmp_path / "screen.png"
    Image.fromarray(arr, "RGBA").save(src)
    out = _ok(engine.run("img_compress", [str(src)], {}))[0]
    assert out.endswith(".png") and os.path.getsize(out) < os.path.getsize(src)


def test_compress_nothing_to_gain_is_info(tmp_path):
    src = tmp_path / "tiny.png"
    Image.new("L", (8, 8), 0).save(src, optimize=True)
    res = engine.run("img_compress", [str(src)], {})
    assert not res.ok and res.info and "déjà" in res.error
    assert sorted(os.listdir(tmp_path)) == ["tiny.png"]    # nothing left behind


def test_resize_choices(jpg_photo):
    out = _ok(engine.run("img_resize", [jpg_photo], {"max_side": 800}))[0]
    assert max(images.image_size(out)) == 800
    half = _ok(engine.run("img_resize", [jpg_photo], {"percent": 50}))[0]
    assert images.image_size(half) == (600, 450)
    res = engine.run("img_resize", [jpg_photo], {"max_side": 1920})
    assert res.info and not res.ok                         # never enlarges


def test_rotate_directions(jpg_photo):
    w, h = images.image_size(jpg_photo)
    for deg, size in ((90, (h, w)), (270, (h, w)), (180, (w, h))):
        out = _ok(engine.run("img_rotate", [jpg_photo], {"degrees": deg}))[0]
        assert images.image_size(out) == size


def test_rotate_clockwise_really(tmp_path):
    im = Image.new("RGB", (200, 100), (255, 0, 0))
    im.paste((0, 0, 255), (0, 0, 100, 100))    # left half blue
    src = tmp_path / "lr.png"
    im.save(src)
    cw = _ok(engine.run("img_rotate", [str(src)], {"degrees": 90}))[0]
    with Image.open(cw) as r:
        assert r.size == (100, 200)
        assert r.getpixel((50, 20))[2] > 200     # blue moved to the top


def test_exif_orientation_respected(jpg_rotated_exif):
    assert images.image_size(jpg_rotated_exif) == (200, 400)
    out = _ok(engine.run("img_crop", [jpg_rotated_exif], {"crop_box": (0, 0, 200, 100)}))[0]
    with Image.open(out) as im:
        assert im.size == (200, 100)
        assert im.getexif().get(0x0112, 1) == 1
        assert im.getpixel((100, 50))[2] > 150   # stored-left blue band is now on top


def test_crop_and_full_frame(jpg_photo):
    out = _ok(engine.run("img_crop", [jpg_photo], {"crop_box": (100, 100, 500, 400)}))[0]
    assert images.image_size(out) == (400, 300)
    res = engine.run("img_crop", [jpg_photo], {"crop_box": (0, 0, 1200, 900)})
    assert res.info


def test_crop_keeps_animation(animated_gif):
    out = _ok(engine.run("img_crop", [animated_gif], {"crop_box": (10, 10, 70, 50)}))[0]
    with Image.open(out) as im:
        assert im.n_frames == 3 and im.size == (60, 40)


def test_formats_keep_their_extension(tmp_path):
    for ext, fmt in ((".bmp", "BMP"), (".tif", "TIFF"), (".gif", "GIF"), (".webp", "WEBP")):
        src = tmp_path / f"pic{ext}"
        Image.new("RGB", (64, 48), (10, 120, 200)).save(src)
        out = _ok(engine.run("img_rotate", [str(src)], {"degrees": 90}))[0]
        assert out.endswith(ext)
        with Image.open(out) as im:
            assert im.format == fmt and im.size == (48, 64)


def test_heic_becomes_jpg(tmp_path):
    pillow_heif = pytest.importorskip("pillow_heif")
    src = tmp_path / "iphone.heic"
    pillow_heif.from_pillow(Image.new("RGB", (300, 200), (90, 160, 40))).save(str(src))
    out = _ok(engine.run("img_crop", [str(src)], {"crop_box": (0, 0, 150, 100)}))[0]
    assert out.endswith(".jpg") and images.image_size(out) == (150, 100)
    conv = _ok(engine.run("img_convert", [str(src)], {"fmt": "jpg"}))[0]
    assert conv.endswith(".jpg")


def test_icc_profile_kept(tmp_path):
    from PIL import ImageCms
    icc = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    src = tmp_path / "icc.jpg"
    Image.new("RGB", (100, 80), (200, 100, 50)).save(src, "JPEG", icc_profile=icc)
    out = _ok(engine.run("img_rotate", [str(src)], {"degrees": 180}))[0]
    with Image.open(out) as im:
        assert im.info.get("icc_profile") == icc


def test_images_to_pdf_a4_proportions(jpg_photo, png_with_alpha):
    out = _ok(engine.run("img_to_pdf", [jpg_photo, png_with_alpha], {}))[0]
    with pymupdf.open(out) as doc:
        assert doc.page_count == 2
        r = doc[0].rect
        assert abs(max(r.width, r.height) - 842) < 1
        assert abs(r.width / r.height - 1200 / 900) < 0.01


def test_crop_only_for_single_image(jpg_photo, png_with_alpha):
    m = registry.menu_for([jpg_photo, png_with_alpha])
    ids = {a.id for a in m.get("image", [])}
    assert "img_crop" not in ids and "img_compress" in ids


# ---- pdf ------------------------------------------------------------------------------

def test_pdf_to_images_folder(pdf_3p):
    outs = _ok(engine.run("pdf_to_images", [pdf_3p], {"fmt": "jpg"}))
    assert len(outs) == 3 and all(o.endswith(".jpg") for o in outs)
    folder = os.path.dirname(outs[0])
    assert os.path.basename(folder) == "doc (images)"
    pngs = _ok(engine.run("pdf_to_images", [pdf_3p], {"fmt": "png"}))
    assert os.path.basename(os.path.dirname(pngs[0])) == "doc (images) (2)"


def test_pdf_merge_order_and_split(pdf_3p, pdf_2p):
    merged = _ok(engine.run("pdf_merge", [pdf_3p, pdf_2p], {}))[0]
    with pymupdf.open(merged) as doc:
        assert doc.page_count == 5
        assert "Page 1" in doc[0].get_text() and "Autre 1" in doc[3].get_text()
    parts = _ok(engine.run("pdf_split", [pdf_3p], {}))
    assert [os.path.basename(p) for p in parts] == ["doc-01.pdf", "doc-02.pdf", "doc-03.pdf"]


def test_split_single_page_is_info(pdf_1p):
    res = engine.run("pdf_split", [pdf_1p], {})
    assert res.info and not os.path.exists(os.path.join(os.path.dirname(pdf_1p),
                                                        "single (pages)"))


def test_pdf_compress(pdf_with_photo, pdf_3p):
    out = _ok(engine.run("pdf_compress", [pdf_with_photo], {}))[0]
    assert os.path.getsize(out) < os.path.getsize(pdf_with_photo) * 0.5
    with pymupdf.open(out) as doc:
        assert "Texte 1" in doc[0].get_text()
    again = engine.run("pdf_compress", [out], {})
    assert again.info and not again.ok                      # nothing left to squeeze


def test_pdf_rotate(pdf_3p):
    out = _ok(engine.run("pdf_rotate", [pdf_3p], {"degrees": 270}))[0]
    with pymupdf.open(out) as doc:
        assert all(p.rotation == 270 for p in doc)


def test_pdf_crop_all_pages_tricky(pdf_tricky):
    """Crop the top-left quarter of what the reader sees, on rotated pages
    whose crop box is offset: the result must show exactly that quarter."""
    out = _ok(engine.run("pdf_crop", [pdf_tricky], {"crop_rel": (0, 0, 0.5, 0.5)}))[0]
    with pymupdf.open(pdf_tricky) as src, pymupdf.open(out) as dst:
        for a, b in zip(src, dst):
            before = _render(a)
            want = before.crop((0, 0, before.width // 2, before.height // 2))
            got = _render(b)
            assert got.size == want.size
            assert ImageChops.difference(got, want).getbbox() is None


def test_pdf_crop_one_page(pdf_3p):
    out = _ok(engine.run("pdf_crop", [pdf_3p], {"crop_rel": (0.1, 0.1, 0.9, 0.5),
                                               "crop_page": 1}))[0]
    with pymupdf.open(out) as doc:
        sizes = [(round(p.rect.width), round(p.rect.height)) for p in doc]
    assert sizes[0] == (595, 842) and sizes[2] == (595, 842)
    assert sizes[1] == (round(595 * 0.8), round(842 * 0.4))


def test_pdf_to_word(pdf_3p):
    out = _ok(engine.run("pdf_to_word", [pdf_3p], {}))[0]
    assert out.lower().endswith(".docx")


def test_watermark_on_every_visible_page(pdf_tricky):
    out = _ok(engine.run("pdf_watermark", [pdf_tricky], {"text": "CONFIDENTIEL"}))[0]
    with pymupdf.open(pdf_tricky) as src, pymupdf.open(out) as dst:
        for a, b in zip(src, dst):
            diff = _changed(_render(a), _render(b), threshold=8)
            assert diff is not None
            w, h = b.rect.width, b.rect.height
            # the stamp spreads across the page, around its centre
            assert diff[0] < w * 0.35 and diff[2] > w * 0.65
            assert diff[1] < h * 0.45 and diff[3] > h * 0.55


def test_page_numbers_bottom_centre(pdf_tricky):
    out = _ok(engine.run("pdf_numbers", [pdf_tricky], {}))[0]
    with pymupdf.open(pdf_tricky) as src, pymupdf.open(out) as dst:
        for i, (a, b) in enumerate(zip(src, dst)):
            diff = _changed(_render(a), _render(b))
            w, h = b.rect.width, b.rect.height
            cx = (diff[0] + diff[2]) / 2
            assert abs(cx - w / 2) < 6, (i, diff)
            assert diff[1] > h - 45, (i, diff)


def test_sign_lands_where_placed(pdf_tricky, signature_png):
    """The signature appears at the chosen spot of the visible page, upright,
    whatever the page rotation and crop box."""
    with pymupdf.open(pdf_tricky) as d:
        n = d.page_count
    for page in range(n):
        out = _ok(engine.run("pdf_sign", [pdf_tricky],
                             {"signature": signature_png, "page": page,
                              "sig_box": (0.5, 0.6, 0.9, 0.76)}))[0]
        with pymupdf.open(pdf_tricky) as src, pymupdf.open(out) as dst:
            a, b = _render(src[page]), _render(dst[page])
            diff = _changed(a, b)
            w, h = b.size
            assert diff is not None
            assert diff[0] >= w * 0.5 - 3 and diff[2] <= w * 0.9 + 3, (page, diff, b.size)
            assert diff[1] >= h * 0.6 - 3 and diff[3] <= h * 0.76 + 3, (page, diff, b.size)
            assert (diff[2] - diff[0]) > (diff[3] - diff[1])     # upright: wide, not tall


def test_sign_default_last_page(pdf_3p, signature_png):
    out = _ok(engine.run("pdf_sign", [pdf_3p], {"signature": signature_png}))[0]
    with pymupdf.open(pdf_3p) as src, pymupdf.open(out) as dst:
        assert _changed(_render(src[0]), _render(dst[0])) is None
        assert _changed(_render(src[2]), _render(dst[2])) is not None


def test_protect_unlock_cycle(pdf_3p):
    locked = _ok(engine.run("pdf_protect", [pdf_3p], {"new_password": "s3cret"}))[0]
    with pymupdf.open(locked) as d:
        assert d.needs_pass
    wrong = engine.run("pdf_unlock", [locked], {"password": "nope"})
    assert wrong.needs_password and "incorrect" in wrong.error
    unlocked = _ok(engine.run("pdf_unlock", [locked], {"password": "s3cret"}))[0]
    with pymupdf.open(unlocked) as d:
        assert not d.needs_pass and d.page_count == 3
    assert engine.run("pdf_unlock", [pdf_3p], {}).info        # not protected
    assert not engine.run("pdf_protect", [locked], {"new_password": "x"}).ok


def test_actions_on_locked_pdf(pdf_locked):
    res = engine.run("pdf_rotate", [pdf_locked], {"degrees": 90})
    assert res.needs_password and not res.ok
    out = _ok(engine.run("pdf_rotate", [pdf_locked], {"degrees": 90, "password": "secret"}))[0]
    with pymupdf.open(out) as d:
        assert d.needs_pass                                     # protection kept
        assert d.authenticate("secret") and d[0].rotation == 90
    assert pdf.needs_password(pdf_locked)


# ---- video --------------------------------------------------------------------------------

pytestmark_video = pytest.mark.skipif(not HAS_FFMPEG, reason="ffmpeg absent")


@pytestmark_video
def test_video_actions(small_video):
    seen = []
    res = engine.run("vid_compress", [small_video], {}, on_progress=lambda f, t: seen.append(f))
    _ok(res)
    assert seen, "progress was reported"
    _ok(engine.run("vid_mp4", [small_video], {}))
    gif = _ok(engine.run("vid_gif", [small_video], {}))[0]
    assert gif.endswith(".gif")
    mp3 = _ok(engine.run("vid_mp3", [small_video], {}))[0]
    assert mp3.endswith(".mp3")


@pytestmark_video
def test_video_odd_dimensions(odd_video):
    out = _ok(engine.run("vid_mp4", [odd_video], {}))[0]
    from cerclic.actions.video import probe
    info = probe(out)
    assert info.width % 2 == 0 and info.height % 2 == 0
    _ok(engine.run("vid_compress", [odd_video], {}))


@pytestmark_video
def test_video_without_sound(silent_video):
    res = engine.run("vid_mp3", [silent_video], {})
    assert not res.ok and "son" in res.error
    _ok(engine.run("vid_mp4", [silent_video], {}))


@pytestmark_video
def test_video_cancel_leaves_nothing(long_video):
    cancel = threading.Event()
    timer = threading.Timer(0.6, cancel.set)
    timer.start()
    res = engine.run("vid_mp4", [long_video], {}, cancel=cancel)
    timer.cancel()
    assert res.cancelled and not res.ok
    assert sorted(os.listdir(os.path.dirname(long_video))) == ["long.mp4"]


# ---- engine ---------------------------------------------------------------------------------

def test_failure_is_reported_not_raised(jpg_photo):
    res = engine.run("pdf_merge", [jpg_photo], {})
    assert not res.ok and res.error


def test_failure_cleans_reserved_files(tmp_path):
    bad = tmp_path / "broken.pdf"
    bad.write_bytes(b"%PDF-1.4 not really")
    res = engine.run("pdf_rotate", [str(bad)], {"degrees": 90})
    assert not res.ok
    assert sorted(os.listdir(tmp_path)) == ["broken.pdf"]


def test_missing_inputs():
    assert engine.missing_inputs("pdf_watermark", {}) == ["text"]
    assert engine.missing_inputs("pdf_watermark", {"text": "x"}) == []
    assert engine.missing_inputs("pdf_unlock", {}) == []


def test_non_destructive_names(jpg_photo):
    a = engine.run("img_compress", [jpg_photo], {})
    b = engine.run("img_compress", [jpg_photo], {})
    assert a.outputs[0] != b.outputs[0]


def test_batch_skips_files_with_nothing_to_do(tmp_path, jpg_photo):
    small = tmp_path / "small.jpg"
    Image.new("RGB", (100, 100), (1, 2, 3)).save(small)
    res = engine.run("img_resize", [jpg_photo, str(small)], {"max_side": 800})
    assert res.ok and len(res.outputs) == 1


def test_concurrent_runs_never_collide(jpg_photo):
    results = []
    threads = [threading.Thread(target=lambda: results.append(
        engine.run("img_rotate", [jpg_photo], {"degrees": 90}))) for _ in range(6)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    outs = [r.outputs[0] for r in results]
    assert all(r.ok for r in results) and len(set(outs)) == 6


def test_menu_rules(pdf_3p, pdf_2p, jpg_photo, small_video):
    m = registry.menu_for([pdf_3p])
    ids = [a.id for a in m["pdf"]]
    assert "pdf_merge" not in ids and "pdf_crop" in ids and "pdf_sign" in ids
    m2 = registry.menu_for([pdf_3p, pdf_2p, jpg_photo, small_video])
    assert set(m2) == {"pdf", "image", "video"}
    assert "pdf_merge" in [a.id for a in m2["pdf"]]
    assert "pdf_crop" not in [a.id for a in m2["pdf"]]
    for a in registry.ACTIONS:
        for c in a.choices:
            assert c.as_opts()


def _cmyk_pdf(tmp_path, big=True):
    import io
    import numpy as np
    h, w = (2000, 3000) if big else (200, 300)
    c = np.zeros((h, w, 4), "uint8")
    c[..., 0] = np.linspace(0, 255, w)[None, :]
    c[..., 1] = np.linspace(0, 200, h)[:, None]
    c[..., 2] = 40
    c[..., 3] = 10
    buf = io.BytesIO()
    Image.fromarray(c, "CMYK").save(buf, "JPEG", quality=95)
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)
    page.insert_image(pymupdf.Rect(50, 50, 545, 545), stream=buf.getvalue())
    page.insert_text((50, 600), "Texte", fontsize=14)
    path = tmp_path / "print.pdf"
    doc.save(str(path))
    doc.close()
    return str(path)


def test_pdf_compress_keeps_cmyk_colours(tmp_path):
    src = _cmyk_pdf(tmp_path)
    res = engine.run("pdf_compress", [src], {})
    assert res.ok or res.info, res.error
    if res.ok:
        with pymupdf.open(src) as a, pymupdf.open(res.outputs[0]) as b:
            assert _changed(_render(a[0]), _render(b[0]), threshold=12) is None


def test_looks_the_same_catches_damage(tmp_path, pdf_with_photo):
    from cerclic.actions.pdf import _looks_the_same
    damaged = tmp_path / "damaged.pdf"
    with pymupdf.open(pdf_with_photo) as doc:
        doc[0].draw_rect(pymupdf.Rect(50, 50, 545, 380), color=(1, 0, 1), fill=(1, 0, 1))
        doc.save(str(damaged))
    assert _looks_the_same(pdf_with_photo, pdf_with_photo, None)
    assert not _looks_the_same(pdf_with_photo, str(damaged), None)


def test_cmyk_to_png_is_colour_managed(tmp_path):
    from PIL import ImageCms
    import io
    # A CMYK JPEG with a real CMYK profile: convert to PNG must give sRGB pixels
    # (through the profile) and an sRGB profile, never the CMYK one.
    srgb = ImageCms.createProfile("sRGB")
    candidates = ["/usr/share/texlive/texmf-dist/tex/generic/colorprofiles/FOGRA39L_coated.icc",
                  "/usr/share/color/icc/ghostscript/default_cmyk.icc",
                  r"C:\Windows\System32\spool\drivers\color\RSWOP.icm"]
    found = next((c for c in candidates if os.path.exists(c)), None)
    if not found:
        pytest.skip("no CMYK profile on this system")
    with open(found, "rb") as f:
        cmyk_prof = ImageCms.ImageCmsProfile(io.BytesIO(f.read()))
    rgb = Image.new("RGB", (40, 30), (228, 8, 25))
    cmyk = ImageCms.profileToProfile(rgb, srgb, cmyk_prof, outputMode="CMYK")
    src = tmp_path / "print.jpg"
    cmyk.save(src, "JPEG", quality=95, icc_profile=cmyk_prof.tobytes())
    out = _ok(engine.run("img_convert", [str(src)], {"fmt": "png"}))[0]
    with Image.open(out) as im:
        assert im.mode == "RGB"
        r, g, b = im.getpixel((20, 15))
        assert r > 190 and g < 60 and b < 70           # still a strong red
        prof = ImageCms.ImageCmsProfile(io.BytesIO(im.info["icc_profile"]))
        assert prof.profile.xcolor_space.strip() == "RGB"


def test_cmyk_without_profile(tmp_path):
    src = tmp_path / "plain_cmyk.jpg"
    Image.new("CMYK", (40, 30), (0, 255, 255, 0)).save(src, "JPEG", quality=95)
    for fmt in ("png", "webp", "jpg"):
        out = _ok(engine.run("img_convert", [str(src)], {"fmt": fmt}))[0]
        with Image.open(out) as im:
            assert im.mode in ("RGB", "RGBA")
            assert "icc_profile" not in im.info or im.info["icc_profile"]


@pytestmark_video
def test_compress_keeps_upright_phone_video(tmp_path):
    from conftest import _video
    from cerclic.actions.video import probe
    vertical = _video(tmp_path / "story.mp4", size="720x1280")
    out = _ok(engine.run("vid_compress", [vertical], {}))[0]
    info = probe(out)
    assert (info.width, info.height) == (720, 1280)
    wide = _video(tmp_path / "wide.mp4", size="2560x1440")
    out = _ok(engine.run("vid_compress", [wide], {}))[0]
    info = probe(out)
    assert (info.width, info.height) == (1920, 1080)


@pytestmark_video
def test_gif_two_pass_and_length_limit(small_video, monkeypatch):
    seen = []
    out = _ok(engine.run("vid_gif", [small_video], {},
                         on_progress=lambda f, t: seen.append(f)))[0]
    with Image.open(out) as im:
        assert im.n_frames > 5
    assert all(f is None or 0 <= f <= 1 for f in seen)
    from cerclic.actions import video
    real = video.probe
    monkeypatch.setattr(video, "probe", lambda p: video.Probe(600.0, True, True, 640, 480)
                        if p == small_video else real(p))
    res = engine.run("vid_gif", [small_video], {})
    assert not res.ok and "trop longue" in res.error


def test_pdf_compress_mixed_print_and_photo(tmp_path):
    """A print-colour image does not stop the photos of the same PDF from being
    compressed, and it comes out untouched."""
    import io
    import numpy as np
    src = _cmyk_pdf(tmp_path, big=False)
    rng = np.random.default_rng(2)
    arr = (rng.random((2000, 3000, 3)) * 60 + np.linspace(0, 180, 3000)[None, :, None]).astype("uint8")
    buf = io.BytesIO()
    Image.fromarray(arr).save(buf, "JPEG", quality=95)
    with pymupdf.open(src) as doc:
        page = doc.new_page(width=595, height=842)
        page.insert_image(pymupdf.Rect(40, 40, 555, 400), stream=buf.getvalue())
        mixed = tmp_path / "mixed.pdf"
        doc.save(str(mixed))
    res = engine.run("pdf_compress", [str(mixed)], {})
    assert res.ok, res.error
    assert os.path.getsize(res.outputs[0]) < os.path.getsize(mixed) * 0.4
    with pymupdf.open(str(mixed)) as a, pymupdf.open(res.outputs[0]) as b:
        assert _changed(_render(a[0]), _render(b[0]), threshold=12) is None


def test_pdf_compress_never_damages_delicate_images(tmp_path):
    """Indexed palette over a CMYK profile, inverted /Decode: left alone."""
    import zlib
    import pikepdf
    import numpy as np
    W, H = 600, 400
    pal = Image.fromarray((np.random.default_rng(1).random((H, W, 3)) * 255).astype("uint8")
                          ).quantize(64)
    pdf = pikepdf.new()
    icc = pdf.make_stream(bytes(200), N=4)
    cs = pikepdf.Array([pikepdf.Name.Indexed,
                        pdf.make_indirect(pikepdf.Array([pikepdf.Name.ICCBased, icc])),
                        63, pikepdf.String(bytes(range(256)))])
    img = pdf.make_stream(zlib.compress(pal.tobytes()), Type=pikepdf.Name.XObject,
                          Subtype=pikepdf.Name.Image, Width=W, Height=H,
                          BitsPerComponent=8, ColorSpace=cs, Filter=pikepdf.Name.FlateDecode)
    page = pikepdf.Dictionary(Type=pikepdf.Name.Page, MediaBox=[0, 0, 595, 842],
                              Contents=pdf.make_stream(b"q 150 0 0 100 60 600 cm /Im0 Do Q"),
                              Resources=pikepdf.Dictionary(XObject=pikepdf.Dictionary(Im0=img)))
    pdf.pages.append(pikepdf.Page(page))
    path = tmp_path / "indexed.pdf"
    pdf.save(str(path))
    from cerclic.actions.pdf import _delicate_images
    with pymupdf.open(str(path)) as d:
        assert _delicate_images(d)


def test_read_only_folder_falls_back_to_downloads(tmp_path, monkeypatch, jpg_photo):
    # (root and Windows ignore folder modes: simulate the refusal)
    from cerclic import paths as P
    real = P._reserve_file

    def refuse(path):
        if os.path.dirname(path) == os.path.dirname(jpg_photo):
            raise PermissionError(13, "Permission denied")
        return real(path)
    monkeypatch.setattr(P, "_reserve_file", refuse)
    home = tmp_path / "home"
    (home / "Downloads").mkdir(parents=True)
    monkeypatch.setattr(P, "_windows_downloads", lambda: None)
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("USERPROFILE", str(home))
    out = _ok(engine.run("img_rotate", [jpg_photo], {"degrees": 90}))[0]
    assert os.path.dirname(out) == str(home / "Downloads")


def test_very_long_names_are_shortened(tmp_path):
    src = tmp_path / ("x" * 240 + ".jpg")
    Image.new("RGB", (20, 10)).save(src)
    out = _ok(engine.run("img_rotate", [str(src)], {"degrees": 90}))[0]
    assert len(os.path.basename(out)) < 255


def _photo_jpeg(w=2400, h=1800, seed=3, quality=92, icc=None):
    import io
    import numpy as np
    rng = np.random.default_rng(seed)
    arr = (rng.random((h, w, 3)) * 50 + np.linspace(30, 200, w)[None, :, None]).astype("uint8")
    buf = io.BytesIO()
    kw = {"icc_profile": icc} if icc else {}
    Image.fromarray(arr).save(buf, "JPEG", quality=quality, **kw)
    return buf.getvalue()


def test_pdf_compress_brings_photos_to_150_dpi(tmp_path):
    """A 290 dpi photo (MuPDF alone would leave it there) ends up at 150 dpi."""
    src = tmp_path / "scan.pdf"
    with pymupdf.open() as doc:
        page = doc.new_page(width=595, height=842)
        page.insert_image(pymupdf.Rect(0, 0, 595, 446), stream=_photo_jpeg())
        doc.save(str(src))
    out = _ok(engine.run("pdf_compress", [str(src)], {}))[0]
    with pymupdf.open(out) as d:
        w = d[0].get_images(full=True)[0][2]
    assert abs(w - 1240) <= 2
    assert os.path.getsize(out) < os.path.getsize(src) * 0.5


def test_pdf_compress_keeps_stencil_masks(tmp_path):
    """A 1-bit stencil mask painted in red over blue (common in scans) keeps its
    look: it is never turned into an opaque grey picture."""
    import zlib
    import pikepdf
    import numpy as np
    W, H = 2480, 1600                       # 300 dpi over the page width
    bits = np.zeros((H, W), dtype=bool)
    bits[200:1400, 300:2200] = True         # a big "painted" block
    bits[::40, :] = False
    mask = np.packbits(~bits, axis=1).tobytes()   # 0 = paint
    pdf = pikepdf.new()
    stencil = pdf.make_stream(zlib.compress(mask), Type=pikepdf.Name.XObject,
                              Subtype=pikepdf.Name.Image, Width=W, Height=H,
                              ImageMask=True, BitsPerComponent=1,
                              Filter=pikepdf.Name.FlateDecode)
    photo = pdf.make_stream(_photo_jpeg(), Type=pikepdf.Name.XObject,
                            Subtype=pikepdf.Name.Image, Width=2400, Height=1800,
                            BitsPerComponent=8, ColorSpace=pikepdf.Name.DeviceRGB,
                            Filter=pikepdf.Name.DCTDecode)
    content = (b"q 0 0 1 rg 0 0 595 842 re f Q "
               b"q 1 0 0 rg 595 0 0 384 0 420 cm /M Do Q "
               b"q 595 0 0 400 0 0 cm /P Do Q")
    page = pikepdf.Dictionary(Type=pikepdf.Name.Page, MediaBox=[0, 0, 595, 842],
                              Contents=pdf.make_stream(content),
                              Resources=pikepdf.Dictionary(
                                  XObject=pikepdf.Dictionary(M=stencil, P=photo)))
    pdf.pages.append(pikepdf.Page(page))
    src = tmp_path / "stencil.pdf"
    pdf.save(str(src))
    out = _ok(engine.run("pdf_compress", [str(src)], {}))[0]
    assert os.path.getsize(out) < os.path.getsize(src)
    with pymupdf.open(str(src)) as a, pymupdf.open(out) as b:
        assert _changed(_render(a[0]), _render(b[0]), threshold=12) is None
        masks = [x for x in range(1, b.xref_length())
                 if b.xref_get_key(x, "ImageMask")[1] == "true"]
        assert masks, "the stencil mask must stay a mask"


def test_only_true_srgb_images_are_reencoded_by_cerclic(tmp_path):
    from PIL import ImageCms
    from cerclic.actions.pdf import _plain_image
    srgb = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    other = srgb.replace("sRGB".encode("utf-16-be"), "P3xx".encode("utf-16-be")
                         ).replace(b"sRGB", b"P3xx")      # some other RGB profile
    assert other != srgb
    src = tmp_path / "icc.pdf"
    with pymupdf.open() as doc:
        page = doc.new_page(width=595, height=842)
        page.insert_image(pymupdf.Rect(0, 0, 595, 400), stream=_photo_jpeg(600, 400, icc=srgb))
        page.insert_image(pymupdf.Rect(0, 420, 595, 820),
                          stream=_photo_jpeg(600, 400, seed=4, icc=other))
        page.insert_image(pymupdf.Rect(0, 0, 10, 10), stream=_photo_jpeg(60, 40, seed=5))
        doc.save(str(src))
    with pymupdf.open(str(src)) as d:
        imgs = d[0].get_images(full=True)
        verdict = sorted((i[2], _plain_image(d, i)) for i in imgs)
    assert verdict == [(60, True), (600, False), (600, True)]


# ---- 0.3: new image tools ----------------------------------------------------------------

def _jpeg_with_private_info(path, appended=b""):
    import io
    from PIL import ImageCms
    im = Image.new("RGB", (300, 200), (200, 50, 50))
    for x in range(120):
        im.putpixel((x, 10), (0, 0, 255))
    ex = Image.Exif()
    ex[0x0112] = 6
    ex[0x010F] = "PhoneMaker"
    ex[0x0110] = "SuperPhone 15"
    ex[0x8825] = {1: "N", 2: (48.0, 51.0, 30.0), 3: "E", 4: (2.0, 17.0, 40.0)}
    icc = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    buf = io.BytesIO()
    im.save(buf, "JPEG", exif=ex.tobytes(), icc_profile=icc, quality=90,
            comment=b"secret comment")
    path.write_bytes(buf.getvalue() + appended)
    return str(path)


def test_anonymise_jpeg_keeps_picture_and_orientation(tmp_path):
    src = _jpeg_with_private_info(tmp_path / "photo.jpg",
                                  appended=b"\xff\xd8 second picture with GPS")
    out = _ok(engine.run("img_clean", [src], {}))[0]
    raw = open(out, "rb").read()
    assert b"PhoneMaker" not in raw and b"second picture" not in raw and b"secret" not in raw
    with Image.open(out) as o, Image.open(src) as a:
        assert dict(o.getexif()) == {0x0112: 6}           # still shown upright
        assert not o.getexif().get_ifd(0x8825)             # no GPS
        assert o.info.get("icc_profile")                   # colours kept
        assert o.tobytes() == a.tobytes()                  # not re-encoded
    again = engine.run("img_clean", [out], {})
    assert again.info                                      # nothing left to remove


def test_anonymise_png_and_webp(tmp_path):
    from PIL import PngImagePlugin
    meta = PngImagePlugin.PngInfo()
    meta.add_text("Author", "Said")
    meta.add_text("GPS", "48.85,2.29")
    png = tmp_path / "shot.png"
    Image.new("RGBA", (50, 40), (10, 200, 30, 128)).save(png, pnginfo=meta)
    out = _ok(engine.run("img_clean", [str(png)], {}))[0]
    with Image.open(out) as o:
        assert "Author" not in o.info and "GPS" not in o.info
        assert o.mode == "RGBA" and o.getpixel((5, 5)) == (10, 200, 30, 128)
    ex = Image.Exif()
    ex[0x010F] = "PhoneMaker"
    webp = tmp_path / "pic.webp"
    Image.new("RGB", (50, 40), (1, 2, 3)).save(webp, exif=ex.tobytes())
    out = _ok(engine.run("img_clean", [str(webp)], {}))[0]
    assert b"PhoneMaker" not in open(out, "rb").read()
    with Image.open(out) as o:
        o.load()
        assert o.size == (50, 40)


def test_mirror(jpg_photo):
    out = _ok(engine.run("img_rotate", [jpg_photo], {"mirror": True}))[0]
    assert "mirrored" in out
    with Image.open(jpg_photo) as a, Image.open(out) as b:
        assert a.size == b.size


def test_assemble_layouts(tmp_path):
    a = tmp_path / "a.jpg"
    b = tmp_path / "b.jpg"
    c = tmp_path / "c.png"
    Image.new("RGB", (400, 300), (255, 0, 0)).save(a)
    Image.new("RGB", (300, 600), (0, 255, 0)).save(b)
    Image.new("RGBA", (200, 200), (0, 0, 255, 100)).save(c)
    row = _ok(engine.run("img_assemble", [str(a), str(b)], {"layout": "row"}))[0]
    with Image.open(row) as im:
        assert im.height == 450 and im.width == 600 + 225     # median height
        assert row.endswith(".jpg")
    col = _ok(engine.run("img_assemble", [str(a), str(b)], {"layout": "column"}))[0]
    with Image.open(col) as im:
        assert im.width == 350
    grid = _ok(engine.run("img_assemble", [str(a), str(b), str(c)], {"layout": "grid"}))[0]
    assert grid.endswith(".png")                               # transparency kept
    with Image.open(grid) as im:
        assert im.mode == "RGBA" and im.width > im.height / 2


def test_clipboard_image_is_upright(jpg_rotated_exif):
    from cerclic.actions.images import clipboard_image
    im = clipboard_image(jpg_rotated_exif)
    assert im.size == (200, 400)


# ---- 0.3: new PDF tools -------------------------------------------------------------------

def test_arrange_pdf_order_rotation_removal(pdf_3p):
    out = _ok(engine.run("pdf_pages", [pdf_3p],
                         {"pages_order": [(2, 0), (0, 90)], "pages_mode": "save"}))[0]
    assert "organized" in out
    with pymupdf.open(out) as d:
        assert d.page_count == 2
        assert "Page 3" in d[0].get_text() and "Page 1" in d[1].get_text()
        assert d[1].rotation == 90
    ext = _ok(engine.run("pdf_pages", [pdf_3p],
                         {"pages_order": [(1, 0)], "pages_mode": "extract"}))[0]
    assert "extract" in ext
    with pymupdf.open(ext) as d:
        assert d.page_count == 1 and "Page 2" in d[0].get_text()
    same = engine.run("pdf_pages", [pdf_3p], {"pages_order": [0, 1, 2]})
    assert same.info


def test_pdf_pages_keeps_password(pdf_locked):
    out = _ok(engine.run("pdf_pages", [pdf_locked],
                         {"pages_order": [(1, 0), (0, 0)], "password": "secret"}))[0]
    with pymupdf.open(out) as d:
        assert d.needs_pass


def test_pdf_to_text(pdf_3p, tmp_path):
    out = _ok(engine.run("pdf_text", [pdf_3p], {}))[0]
    raw = open(out, "rb").read()
    assert raw.startswith(b"\xef\xbb\xbf")                  # Notepad reads the accents
    text = raw.decode("utf-8-sig")
    assert "Page 1" in text and "Page 3" in text and "\r\n" in text
    scan = tmp_path / "scan.pdf"
    with pymupdf.open() as d:
        page = d.new_page()
        pix = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, 50, 50), False)
        page.insert_image(page.rect, pixmap=pix)
        d.save(str(scan))
    res = engine.run("pdf_text", [str(scan)], {})
    assert res.info and "scan" in res.error


# ---- 0.3: video and sound tools -----------------------------------------------------------

@pytest.mark.skipif(not HAS_FFMPEG, reason="ffmpeg missing")
def test_trim_video(long_clip):
    from cerclic.actions.video import probe
    out = _ok(engine.run("vid_trim", [long_clip], {"trim_start": 1.0, "trim_end": 2.5}))[0]
    assert out.endswith(".mp4")
    assert abs(probe(out).duration - 1.5) < 0.2
    whole = engine.run("vid_trim", [long_clip], {"trim_start": 0, "trim_end": 4.0})
    assert whole.info


@pytest.mark.skipif(not HAS_FFMPEG, reason="ffmpeg missing")
def test_trim_sound_keeps_its_format(m4a_sound, wav_sound, opus_sound, mp3_sound):
    from cerclic.actions.video import probe
    for src, ext in ((m4a_sound, ".m4a"), (wav_sound, ".wav"), (opus_sound, ".opus"),
                     (mp3_sound, ".mp3")):
        out = _ok(engine.run("aud_trim", [src], {"trim_start": 0.5, "trim_end": 2.0}))[0]
        assert out.endswith(ext), out
        assert abs(probe(out).duration - 1.5) < 0.25, out


@pytest.mark.skipif(not HAS_FFMPEG, reason="ffmpeg missing")
def test_mute_and_rotate_video(small_video, silent_video):
    from cerclic.actions.video import probe
    out = _ok(engine.run("vid_mute", [small_video], {}))[0]
    info = probe(out)
    assert info.has_video and not info.has_audio
    assert engine.run("vid_mute", [silent_video], {}).info
    rot = _ok(engine.run("vid_rotate", [small_video], {"degrees": 90}))[0]
    info = probe(rot)
    assert (info.width, info.height) == (480, 640)


@pytest.mark.skipif(not HAS_FFMPEG, reason="ffmpeg missing")
def test_sound_to_mp3_and_compress(m4a_sound, mp3_sound, opus_sound):
    out = _ok(engine.run("aud_mp3", [opus_sound], {}))[0]
    assert out.endswith(".mp3") and os.path.getsize(out) > 1000
    assert engine.run("aud_mp3", [mp3_sound], {}).info
    small = _ok(engine.run("aud_compress", [mp3_sound], {}))[0]
    assert os.path.getsize(small) < os.path.getsize(mp3_sound)


@pytest.mark.skipif(not HAS_FFMPEG, reason="ffmpeg missing")
def test_previews_for_the_cutting_popup(small_video, m4a_sound):
    from cerclic.actions import video
    import io
    frame = video.frame_png(small_video, 0.5, 160, 120)
    with Image.open(io.BytesIO(frame)) as im:
        assert im.size == (160, 120)
    wave = video.waveform_png(m4a_sound, 300, 60)
    with Image.open(io.BytesIO(wave)) as im:
        assert im.size == (300, 60)


def test_probe_reads_phone_rotation(monkeypatch):
    from cerclic.actions import video

    class P:
        returncode = 1
        stderr = (b"  Duration: 00:00:05.00, start: 0.000000, bitrate: 100 kb/s\n"
                  b"  Stream #0:0[0x1](und): Video: h264 (High), yuv420p, 1920x1080, "
                  b"30 fps\n      Side data:\n        displaymatrix: rotation of -90.00 "
                  b"degrees\n  Stream #0:1: Audio: aac, 44100 Hz\n")
    monkeypatch.setattr(video.subprocess, "run", lambda *a, **k: P())
    monkeypatch.setattr(video, "ffmpeg_path", lambda: "ffmpeg")
    info = video.probe("x.mp4")
    assert (info.width, info.height) == (1080, 1920) and info.has_audio
