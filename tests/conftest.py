"""Real fixture files, so the tests exercise the actual processing code."""
import os
import shutil
import subprocess
import sys

import pytest
from PIL import Image

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymupdf  # noqa: E402

HAS_FFMPEG = shutil.which("ffmpeg") is not None


@pytest.fixture(scope="session", autouse=True)
def _gc_on_main_thread():
    """As in the app: never let the cycle collector run in a worker thread
    (it could destroy a Qt widget there)."""
    import gc
    gc.disable()
    yield
    gc.enable()


@pytest.fixture(autouse=True)
def _collect_after_each_test():
    yield
    import gc
    gc.collect()


@pytest.fixture(autouse=True)
def _isolated_config(tmp_path, monkeypatch):
    """Settings and the request pipe never touch the real user profile."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("APPDATA", str(tmp_path / "config"))
    monkeypatch.setenv("CERCLIC_SERVER_NAME", f"cerclic-test-{os.getpid()}-{id(tmp_path)}")
    monkeypatch.setenv("CERCLIC_NO_INTEGRATION", "1")   # no registry, no shortcut


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
    """A photo-like JPEG (gradient + noise) so compression has work to do."""
    import numpy as np
    rng = np.random.default_rng(7)
    arr = (rng.random((900, 1200, 3)) * 50
           + np.linspace(30, 200, 1200)[None, :, None]).astype("uint8")
    p = tmp_path / "photo.jpg"
    Image.fromarray(arr).save(p, "JPEG", quality=95)
    return str(p)


@pytest.fixture
def jpg_rotated_exif(tmp_path):
    """Stored landscape 400x200, EXIF says 'rotate 90' (like a phone photo)."""
    im = Image.new("RGB", (400, 200), (200, 50, 50))
    im.paste((50, 50, 200), (0, 0, 100, 200))       # blue band on the stored left
    exif = Image.Exif()
    exif[0x0112] = 6
    p = tmp_path / "phone.jpg"
    im.save(p, "JPEG", quality=95, exif=exif.tobytes())
    return str(p)


@pytest.fixture
def animated_gif(tmp_path):
    frames = [Image.new("RGB", (120, 80), c) for c in ((255, 0, 0), (0, 255, 0), (0, 0, 255))]
    p = tmp_path / "anim.gif"
    frames[0].save(p, save_all=True, append_images=frames[1:], duration=120, loop=0)
    return str(p)


def _pdf(path, pages=3, text="Page {n} test Cerclic", size=(595, 842)):
    doc = pymupdf.open()
    for i in range(pages):
        page = doc.new_page(width=size[0], height=size[1])
        page.insert_text((72, 72), text.format(n=i + 1), fontsize=24)
    doc.save(str(path))
    doc.close()
    return str(path)


@pytest.fixture
def pdf_3p(tmp_path):
    return _pdf(tmp_path / "doc.pdf")


@pytest.fixture
def pdf_2p(tmp_path):
    return _pdf(tmp_path / "other.pdf", pages=2, text="Autre {n}")


@pytest.fixture
def pdf_1p(tmp_path):
    return _pdf(tmp_path / "single.pdf", pages=1)


@pytest.fixture
def pdf_tricky(tmp_path):
    """Four pages rotated 0/90/180/270 with a crop box offset from the media box."""
    doc = pymupdf.open()
    for rot in (0, 90, 180, 270):
        p = doc.new_page(width=600, height=800)
        p.insert_text((80, 140), f"rot {rot}", fontsize=20)
        p.set_cropbox(pymupdf.Rect(50, 100, 550, 700))
        p.set_rotation(rot)
    path = tmp_path / "tricky.pdf"
    doc.save(str(path))
    doc.close()
    return str(path)


@pytest.fixture
def pdf_locked(tmp_path, pdf_3p):
    import pikepdf
    out = tmp_path / "locked.pdf"
    with pikepdf.open(pdf_3p) as pdf:
        pdf.save(str(out), encryption=pikepdf.Encryption(owner="secret", user="secret", R=6))
    return str(out)


@pytest.fixture
def pdf_with_photo(tmp_path):
    import io
    import numpy as np
    rng = np.random.default_rng(1)
    arr = (rng.random((1600, 2400, 3)) * 60 + np.linspace(0, 180, 2400)[None, :, None]).astype("uint8")
    buf = io.BytesIO()
    Image.fromarray(arr).save(buf, "JPEG", quality=95)
    doc = pymupdf.open()
    for i in range(2):
        page = doc.new_page(width=595, height=842)
        page.insert_image(pymupdf.Rect(50, 50, 545, 380), stream=buf.getvalue())
        page.insert_text((50, 420), f"Texte {i + 1}", fontsize=14)
    path = tmp_path / "scan.pdf"
    doc.save(str(path))
    doc.close()
    return str(path)


@pytest.fixture
def signature_png(tmp_path):
    p = tmp_path / "sign.png"
    im = Image.new("RGBA", (400, 160), (0, 0, 0, 0))
    for x in range(20, 380):
        for dy in range(-3, 4):
            im.putpixel((x, 80 + (x % 30) - 15 + dy), (10, 10, 120, 255))
    im.save(p)
    return str(p)


def _video(path, size="640x480", audio=True, duration=1):
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
           "-f", "lavfi", "-i", f"testsrc=size={size}:rate=24:duration={duration}"]
    if audio:
        cmd += ["-f", "lavfi", "-i", f"sine=frequency=440:duration={duration}",
                "-c:a", "aac", "-shortest"]
    cmd += ["-c:v", "mpeg4", "-q:v", "5", str(path)]
    subprocess.run(cmd, check=True)
    return str(path)


@pytest.fixture
def small_video(tmp_path):
    return _video(tmp_path / "clip.mp4")


@pytest.fixture
def odd_video(tmp_path):
    return _video(tmp_path / "odd.avi", size="641x481")


@pytest.fixture
def silent_video(tmp_path):
    return _video(tmp_path / "silent.mp4", audio=False)


@pytest.fixture
def long_video(tmp_path):
    return _video(tmp_path / "long.mp4", size="1280x720", duration=20)


def _sound(path, duration=3, codec_args=()):
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
           "-i", f"sine=frequency=330:duration={duration}", *codec_args, str(path)]
    subprocess.run(cmd, check=True)
    return str(path)


@pytest.fixture
def m4a_sound(tmp_path):
    return _sound(tmp_path / "voix.m4a", codec_args=("-c:a", "aac", "-b:a", "128k"))


@pytest.fixture
def wav_sound(tmp_path):
    return _sound(tmp_path / "son.wav")


@pytest.fixture
def opus_sound(tmp_path):
    return _sound(tmp_path / "note vocale.opus", codec_args=("-c:a", "libopus"))


@pytest.fixture
def mp3_sound(tmp_path):
    return _sound(tmp_path / "chanson.mp3", duration=4,
                  codec_args=("-c:a", "libmp3lame", "-b:a", "320k"))


@pytest.fixture
def long_clip(tmp_path):
    return _video(tmp_path / "long.mp4", duration=4)
