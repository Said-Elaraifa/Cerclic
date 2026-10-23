# PyInstaller spec for Cerclic (one folder, no console window).
# Build: pyinstaller cerclic.spec   (see scripts/build_windows.sh / the CI workflow)
import os

from PyInstaller.utils.hooks import collect_all

ROOT = os.path.abspath(os.getcwd())

datas = []
binaries = []
hiddenimports = [
    "win32timezone", "pythoncom", "pywintypes", "win32com", "win32com.client",
    "win32com.shell", "win32com.shell.shell", "win32gui",
    # Microsoft Store version: its startup task (Windows.ApplicationModel)
    "winrt.runtime", "winrt.system", "winrt.windows.foundation",
    "winrt.windows.applicationmodel",
]

# libheif (HEIC photos, decoder only) and anything pi_heif ships.
for pkg in ("pi_heif",):
    d, b, h = collect_all(pkg)
    datas += d
    binaries += b
    hiddenimports += h

# ffmpeg for the video actions: put in assets/ffmpeg/ by the build script.
_ffmpeg = os.path.join(ROOT, "assets", "ffmpeg", "ffmpeg.exe")
if os.path.exists(_ffmpeg):
    datas.append((_ffmpeg, "ffmpeg"))

datas.append((os.path.join(ROOT, "assets", "cerclic.ico"), "assets"))

a = Analysis(
    ["run_cerclic.py"],
    pathex=[ROOT],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=["PyQt5", "PyQt6", "PySide2", "tkinter", "matplotlib", "pandas",
              "pillow_heif",                    # tests only (its wheels contain x265, GPL)
              "scipy", "IPython", "pytest", "pytestqt", "PySide6.QtWebEngineCore",
              "PySide6.QtQml", "PySide6.QtQuick", "PySide6.QtPdf", "PySide6.QtSql",
              "PySide6.QtTest", "PySide6.QtOpenGL", "PySide6.QtDBus",
              "win32ui", "win32uiole", "pythonwin", "dde"],
    noarchive=False,
)


def _wanted(entry) -> bool:
    """Drop what Cerclic never uses: Qt's software OpenGL (20 MB), Qt's own
    translations, the MFC part of pywin32, OpenCV's video plugin (30 MB, only
    loaded to read videos with OpenCV, which Cerclic does with ffmpeg), and
    python-docx's unpacked template (it reads default.docx; the folder's
    _rels/.rels names are refused in a Microsoft Store package)."""
    dest = entry[0].replace("\\", "/").lower()
    return not (dest.endswith("opengl32sw.dll")
                or dest.startswith("pyside6/translations/")
                or dest.startswith("pythonwin/")
                or "/opencv_videoio_ffmpeg" in dest
                or dest.startswith("docx/templates/default-docx-template/"))


a.binaries = [b for b in a.binaries if _wanted(b)]
a.datas = [d for d in a.datas if _wanted(d)]
pyz = PYZ(a.pure)

_version = os.path.join(ROOT, "assets", "version_info.txt")
exe = EXE(
    pyz, a.scripts, [],
    exclude_binaries=True,
    name="Cerclic",
    debug=False,
    strip=False,
    upx=False,
    console=False,
    icon=os.path.join(ROOT, "assets", "cerclic.ico"),
    version=_version if os.path.exists(_version) else None,
)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name="Cerclic")
