# PyInstaller spec for Cerclic (onedir, windowed).
# Build: pyinstaller cerclic.spec
import os
from PyInstaller.utils.hooks import collect_all

block_cipher = None
ROOT = os.path.abspath(os.getcwd())

datas = []
binaries = []
hiddenimports = [
    "win32timezone", "pythoncom", "pywintypes",
    "win32com", "win32com.client", "win32gui",
]

# Bundle libheif (HEIC/AVIF) and anything pillow_heif ships.
for pkg in ("pillow_heif",):
    d, b, h = collect_all(pkg)
    datas += d
    binaries += b
    hiddenimports += h

# ffmpeg is placed here by the build (CI downloads a static build).
_ffmpeg = os.path.join(ROOT, "assets", "ffmpeg", "ffmpeg.exe")
if os.path.exists(_ffmpeg):
    datas.append((_ffmpeg, "ffmpeg"))

a = Analysis(
    ["run_cerclic.py"],
    pathex=[ROOT],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=["PyQt5", "PyQt6", "PySide2", "tkinter", "matplotlib",
              "pandas", "scipy", "IPython", "pytest", "PySide6.QtWebEngineCore"],
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz, a.scripts, [],
    exclude_binaries=True,
    name="Cerclic",
    debug=False,
    strip=False,
    upx=False,
    console=False,
    icon=os.path.join(ROOT, "assets", "cerclic.ico"),
    version=os.path.join(ROOT, "assets", "version_info.txt")
    if os.path.exists(os.path.join(ROOT, "assets", "version_info.txt")) else None,
)
coll = COLLECT(
    exe, a.binaries, a.datas,
    strip=False, upx=False, name="Cerclic",
)
