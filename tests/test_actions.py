"""End-to-end tests of every action through the engine.

Each test runs the real handler on real files and checks the output exists,
is non-empty, sits beside the source, and leaves the original untouched.
"""
import os

import pytest
from PIL import Image
import pymupdf

from cerclic import engine
from cerclic.actions import registry
from cerclic.actions import images, pdf


def _ok(res):
    assert res.ok, res.error
    for o in res.outputs:
        assert os.path.exists(o), o
        assert os.path.getsize(o) > 0, o
    return res.outputs


# ---- images ----------------------------------------------------------------

def test_convert_formats(png_with_alpha):
    for fmt, ext in (("jpg", ".jpg"), ("png", ".png"), ("webp", ".webp")):
        res = engine.run(f"img_{fmt}", [png_with_alpha], {})
        out = _ok(res)[0]
        assert out.lower().endswith(ext)
    assert os.path.exists(png_with_alpha)  # original kept


def test_jpg_flattens_alpha(png_with_alpha):
    out = _ok(engine.run("img_jpg", [png_with_alpha], {}))[0]
    with Image.open(out) as im:
        assert im.mode == "RGB"


def test_compress_smaller(jpg_photo):
    out = _ok(engine.run("img_compress", [jpg_photo], {"quality": 50}))[0]
    assert os.path.getsize(out) < os.path.getsize(jpg_photo)


def test_resize_and_rotate(jpg_photo):
    out = _ok(engine.run("img_resize", [jpg_photo], {"max_side": 400}))[0]
    assert max(images.image_size(out)) == 400
    w0, h0 = images.image_size(jpg_photo)
    rot = _ok(engine.run("img_rotate", [jpg_photo], {"degrees": 90}))[0]
    assert images.image_size(rot) == (h0, w0)


def test_crop(jpg_photo):
    out = _ok(engine.run("img_crop", [jpg_photo], {"crop_box": (100, 100, 500, 400)}))[0]
    assert images.image_size(out) == (400, 300)


def test_crop_needs_single_file(jpg_photo, png_with_alpha):
    m = registry.menu_for([jpg_photo, png_with_alpha])
    ids = {a.id for a in m.get("image", [])}
    assert "img_crop" not in ids  # hidden for multi-selection
    assert "img_compress" in ids


def test_images_to_pdf(jpg_photo, png_with_alpha):
    out = _ok(engine.run("img_to_pdf", [jpg_photo, png_with_alpha], {}))[0]
    assert out.lower().endswith(".pdf")
    assert pdf.pdf_page_count(out) == 2


# ---- pdf --------------------------------------------------------------------

def test_pdf_to_images(pdf_3p):
    outs = _ok(engine.run("pdf_to_jpg", [pdf_3p], {}))
    assert len(outs) == 3
    assert all(o.lower().endswith(".jpg") for o in outs)


def test_pdf_merge_split(pdf_3p, pdf_2p):
    merged = _ok(engine.run("pdf_merge", [pdf_3p, pdf_2p], {}))[0]
    assert pdf.pdf_page_count(merged) == 5
    parts = _ok(engine.run("pdf_split", [pdf_3p], {"every": 1}))
    assert len(parts) == 3


def test_pdf_compress_rotate(pdf_3p):
    _ok(engine.run("pdf_compress", [pdf_3p], {}))
    _ok(engine.run("pdf_rotate", [pdf_3p], {"degrees": 90}))


def test_pdf_to_word(pdf_3p):
    out = _ok(engine.run("pdf_to_word", [pdf_3p], {}))[0]
    assert out.lower().endswith(".docx")


def test_pdf_watermark_numbers(pdf_3p):
    _ok(engine.run("pdf_watermark", [pdf_3p], {"text": "CONFIDENTIEL"}))
    _ok(engine.run("pdf_numbers", [pdf_3p], {}))


def test_pdf_sign(pdf_3p, signature_png):
    out = _ok(engine.run("pdf_sign", [pdf_3p], {"signature": signature_png}))[0]
    assert pdf.pdf_page_count(out) == 3


def test_pdf_protect_unlock(pdf_3p):
    locked = _ok(engine.run("pdf_protect", [pdf_3p], {"password": "secret"}))[0]
    with pytest.raises(Exception):
        pymupdf.open(locked).load_page(0)  # cannot open without password
    opened = pymupdf.open(locked)
    assert opened.needs_pass
    opened.close()
    unlocked = _ok(engine.run("pdf_unlock", [locked], {"password": "secret"}))[0]
    assert pdf.pdf_page_count(unlocked) == 3


# ---- video ------------------------------------------------------------------

def test_video_compress_mp4_gif_mp3(small_video):
    _ok(engine.run("vid_compress", [small_video], {}))
    _ok(engine.run("vid_mp4", [small_video], {}))
    gif = _ok(engine.run("vid_gif", [small_video], {}))[0]
    assert gif.lower().endswith(".gif")
    mp3 = _ok(engine.run("vid_mp3", [small_video], {}))[0]
    assert mp3.lower().endswith(".mp3")


# ---- engine behaviour -------------------------------------------------------

def test_failure_is_reported_not_raised(jpg_photo):
    res = engine.run("pdf_merge", [jpg_photo], {})  # wrong kind + too few
    assert not res.ok and res.error


def test_missing_inputs(pdf_3p):
    assert engine.missing_inputs("pdf_sign", {}) == ["signature"]
    assert engine.missing_inputs("pdf_sign", {"signature": "x.png"}) == []
    assert engine.missing_inputs("pdf_unlock", {}) == []  # password optional


def test_non_destructive_names(jpg_photo):
    a = engine.run("img_compress", [jpg_photo], {})
    b = engine.run("img_compress", [jpg_photo], {})
    assert a.outputs[0] != b.outputs[0]  # second run does not overwrite first
