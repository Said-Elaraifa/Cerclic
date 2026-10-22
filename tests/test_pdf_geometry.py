"""PDF stamps and crops on awkward pages: every rotation, crop boxes offset from
the media box, and media boxes that do not start at (0, 0) (pdfcrop, scanners).
What the reader sees must match what the editor showed."""

import pikepdf
import pymupdf
import pytest
from PIL import Image, ImageChops

from cerclic import engine

LAYOUTS = [([0, 0, 600, 800], None), ([100, 50, 700, 850], None),
           ([-50, -80, 550, 720], None), ([100, 50, 700, 850], [150, 150, 650, 750])]
CASES = [(mb, cb, rot) for mb, cb in LAYOUTS for rot in (0, 90, 180, 270)]


def _make(path, mb, cb, rot):
    pdf = pikepdf.new()
    x0, y0, x1, y1 = mb
    content = (f"q 0.8 g {x0 + 20} {y0 + 20} {x1 - x0 - 40} {y1 - y0 - 40} re f Q "
               f"BT /F1 24 Tf {x0 + 80} {y1 - 140} Td (rot {rot}) Tj ET").encode()
    font = pikepdf.Dictionary(Type=pikepdf.Name.Font, Subtype=pikepdf.Name.Type1,
                              BaseFont=pikepdf.Name.Helvetica)
    page = pikepdf.Dictionary(Type=pikepdf.Name.Page, MediaBox=list(mb),
                              Contents=pdf.make_stream(content),
                              Resources=pikepdf.Dictionary(Font=pikepdf.Dictionary(F1=font)))
    if cb:
        page.CropBox = list(cb)
    if rot:
        page.Rotate = rot
    pdf.pages.append(pikepdf.Page(page))
    pdf.save(path)
    return str(path)


def _render(page):
    pix = page.get_pixmap(dpi=72, alpha=False)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def _changed(a, b, threshold=60):
    d = ImageChops.difference(a, b).convert("L")
    return d.point(lambda v: 255 if v > threshold else 0).getbbox()


def _ids(case):
    mb, cb, rot = case
    return f"mb{mb[0]}_{mb[1]}{'_cb' if cb else ''}_rot{rot}"


@pytest.fixture(params=CASES, ids=[_ids(c) for c in CASES])
def odd_pdf(request, tmp_path):
    mb, cb, rot = request.param
    return _make(tmp_path / "odd.pdf", mb, cb, rot)


def test_sign_position(odd_pdf, signature_png):
    r = engine.run("pdf_sign", [odd_pdf], {"signature": signature_png, "page": 0,
                                          "sig_box": (0.5, 0.6, 0.9, 0.76)})
    assert r.ok, r.error
    with pymupdf.open(odd_pdf) as s, pymupdf.open(r.outputs[0]) as d:
        a, b = _render(s[0]), _render(d[0])
    diff = _changed(a, b)
    w, h = b.size
    assert diff is not None
    assert diff[0] >= w * 0.5 - 3 and diff[2] <= w * 0.9 + 3, (diff, b.size)
    assert diff[1] >= h * 0.6 - 3 and diff[3] <= h * 0.76 + 3, (diff, b.size)


def test_crop_quarter(odd_pdf):
    r = engine.run("pdf_crop", [odd_pdf], {"crop_rel": (0, 0, 0.5, 0.5)})
    assert r.ok, r.error
    with pymupdf.open(odd_pdf) as s, pymupdf.open(r.outputs[0]) as d:
        before, got = _render(s[0]), _render(d[0])
    want = before.crop((0, 0, before.width // 2, before.height // 2))
    assert got.size == want.size
    assert _changed(got, want, 30) is None


def test_numbers_position(odd_pdf):
    r = engine.run("pdf_numbers", [odd_pdf], {})
    assert r.ok, r.error
    with pymupdf.open(odd_pdf) as s, pymupdf.open(r.outputs[0]) as d:
        a, b = _render(s[0]), _render(d[0])
        w, h = d[0].rect.width, d[0].rect.height
    diff = _changed(a, b)
    assert diff is not None
    assert abs((diff[0] + diff[2]) / 2 - w / 2) < 6 and diff[1] > h - 45, (diff, w, h)


def test_watermark_spread(odd_pdf):
    r = engine.run("pdf_watermark", [odd_pdf], {"text": "CONFIDENTIEL"})
    assert r.ok, r.error
    with pymupdf.open(odd_pdf) as s, pymupdf.open(r.outputs[0]) as d:
        a, b = _render(s[0]), _render(d[0])
        w, h = d[0].rect.width, d[0].rect.height
    diff = _changed(a, b, 8)
    assert diff is not None
    assert diff[0] < w * 0.35 and diff[2] > w * 0.65
    assert diff[1] < h * 0.45 and diff[3] > h * 0.55
