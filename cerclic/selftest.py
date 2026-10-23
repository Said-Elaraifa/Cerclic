"""`Cerclic --selftest`: checks that the packaged Cerclic has everything it needs
(libraries, ffmpeg) and that a few real actions work, without any window.

Prints one line per check and writes the same report beside the log
(selftest.txt), so it can be read even from the Windows build, which has no
console. Exit code 0 when everything passed.
"""
from __future__ import annotations

import importlib
import os
import shutil
import sys
import tempfile
import time


def _qt() -> str:
    import PySide6
    for name in ("QtGui", "QtWidgets", "QtNetwork"):
        importlib.import_module(f"PySide6.{name}")
    return f"PySide6 {PySide6.__version__}"


def _pdf_engine() -> str:
    import pymupdf
    doc = pymupdf.open()
    page = doc.new_page(width=200, height=100)
    page.insert_text((20, 50), "Cerclic")
    pix = page.get_pixmap()
    assert pix.width > 0
    return f"PyMuPDF {pymupdf.VersionBind}"


def _pikepdf() -> str:
    import pikepdf
    return f"pikepdf {pikepdf.__version__}"


def _images() -> str:
    import PIL
    from PIL import Image
    Image.new("RGB", (8, 8)).tobytes()
    return f"Pillow {PIL.__version__}"


def _heic() -> str:
    try:
        import pi_heif as heif
    except ImportError:
        import pillow_heif as heif
    heif.register_heif_opener()
    return f"{heif.__name__} {heif.__version__} (libheif {heif.libheif_version()})"


def _word() -> str:
    for name in ("pdf2docx", "docx", "cv2"):
        importlib.import_module(name)
    return "pdf2docx"


def _ffmpeg() -> str:
    import subprocess
    from .actions.video import ffmpeg_path
    path = ffmpeg_path()
    out = subprocess.run([path, "-hide_banner", "-version"], capture_output=True,
                         text=True, timeout=30, stdin=subprocess.DEVNULL)
    first = (out.stdout or out.stderr).splitlines()[0] if (out.stdout or out.stderr) else ""
    assert out.returncode == 0, first
    return first[:60]


def _actions(work: str) -> str:
    """A photo rotated and turned into a PDF, the PDF drawn back into an image
    and protected, a short video made by ffmpeg then cut: the real code paths."""
    import subprocess
    from PIL import Image
    from . import engine
    from .actions.video import ffmpeg_path
    photo = os.path.join(work, "photo.jpg")
    Image.new("RGB", (320, 200), (46, 124, 246)).save(photo, quality=90)
    done = []
    for action, opts in (("img_rotate", {"degrees": 90}), ("img_to_pdf", {})):
        res = engine.run(action, [photo], opts)
        assert res.ok, f"{action} : {res.error}"
        done.append(action)
    pdf = next(os.path.join(work, n) for n in os.listdir(work) if n.endswith(".pdf"))
    for action, opts in (("pdf_to_images", {}), ("pdf_protect", {"new_password": "essai"})):
        res = engine.run(action, [pdf], opts)
        assert res.ok, f"{action} : {res.error}"
        done.append(action)
    video = os.path.join(work, "clip.mp4")
    subprocess.run([ffmpeg_path(), "-hide_banner", "-loglevel", "error", "-f", "lavfi",
                    "-i", "testsrc=duration=2:size=160x120:rate=10", "-pix_fmt", "yuv420p",
                    video], check=True, capture_output=True, timeout=60,
                   stdin=subprocess.DEVNULL)
    res = engine.run("vid_trim", [video], {"trim_start": 0.0, "trim_end": 1.0})
    assert res.ok, f"vid_trim : {res.error}"
    done.append("vid_trim")
    return ", ".join(done)


def run() -> int:
    work = tempfile.mkdtemp(prefix="cerclic-selftest-")
    lines: list[str] = []
    ok_all = True
    checks = [("Interface (Qt)", _qt), ("PDF", _pdf_engine), ("PDF protégés", _pikepdf),
              ("Images", _images), ("Photos HEIC", _heic), ("PDF en Word", _word),
              ("Vidéo et son (ffmpeg)", _ffmpeg), ("Actions réelles", lambda: _actions(work))]
    for name, check in checks:
        start = time.monotonic()
        try:
            detail = check()
            lines.append(f"OK      {name} : {detail} ({time.monotonic() - start:.1f} s)")
        except BaseException as exc:          # noqa: BLE001 - every failure is reported
            ok_all = False
            lines.append(f"ÉCHEC   {name} : {exc!r}")
    shutil.rmtree(work, ignore_errors=True)
    lines.append("Tout fonctionne." if ok_all else "Au moins un élément ne fonctionne pas.")
    report = "\n".join(lines)
    print(report, flush=True)
    try:
        from .settings import config_dir
        with open(os.path.join(config_dir(), "selftest.txt"), "w", encoding="utf-8") as f:
            f.write(report + "\n")
    except OSError:
        pass
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(run())
