"""Generate real fixture files so tests exercise the actual processing code."""
import os
import subprocess

import pytest
from PIL import Image
import pymupdf


@pytest.fixture
def workdir(tmp_path):
    return tmp_path


@pytest.fixture
def png_with_alpha(tmp_path):
    p = tmp_path / "shot.png"
    im = Image.new("RGBA", (800, 600), (0, 0, 0, 0))
    for x in range(0, 800, 40):
        for y in range(0, 600, 40):
            im.putpixel((x, y), (x % 256, y % 256, 128, 255))
    im.save(p)
    return str(p)


@pytest.fixture
def jpg_photo(tmp_path):
    p = tmp_path / "photo.jpg"
    Image.new("RGB", (1200, 900), (180, 120, 60)).save(p, "JPEG", quality=95)
    return str(p)


@pytest.fixture
def pdf_3p(tmp_path):
    p = tmp_path / "doc.pdf"
    doc = pymupdf.open()
    for i in range(3):
        page = doc.new_page()
        page.insert_text((72, 72), f"Page {i + 1} test Cerclic", fontsize=24)
    doc.save(str(p))
    doc.close()
    return str(p)


@pytest.fixture
def pdf_2p(tmp_path):
    p = tmp_path / "other.pdf"
    doc = pymupdf.open()
    for i in range(2):
        page = doc.new_page()
        page.insert_text((72, 100), f"Autre {i + 1}", fontsize=20)
    doc.save(str(p))
    doc.close()
    return str(p)


@pytest.fixture
def signature_png(tmp_path):
    p = tmp_path / "sign.png"
    im = Image.new("RGBA", (400, 160), (0, 0, 0, 0))
    for x in range(20, 380):
        im.putpixel((x, 80 + (x % 30) - 15), (10, 10, 120, 255))
    im.save(p)
    return str(p)


@pytest.fixture
def small_video(tmp_path):
    p = tmp_path / "clip.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-f", "lavfi", "-i", "testsrc=size=640x480:rate=24:duration=1",
         "-f", "lavfi", "-i", "sine=frequency=440:duration=1",
         "-c:v", "libx264", "-c:a", "aac", "-shortest", str(p)],
        check=True)
    return str(p)
