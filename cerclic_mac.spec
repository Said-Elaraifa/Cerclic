# PyInstaller spec for Cerclic on macOS: Cerclic.app, a menu bar app.
# Build on a Mac with scripts/build_mac.sh (it puts ffmpeg in assets/ffmpeg/).
import os
import re

from PyInstaller.utils.hooks import collect_all

ROOT = os.path.abspath(os.getcwd())
with open(os.path.join(ROOT, "cerclic", "__init__.py"), encoding="utf-8") as f:
    VERSION = re.search(r'__version__ = "([^"]+)"', f.read()).group(1)

datas = [(os.path.join(ROOT, "assets", "LICENCES.txt"), ".")]
binaries = []
hiddenimports = []

# libheif (HEIC photos, decoder only) and anything pi_heif ships.
for pkg in ("pi_heif",):
    d, b, h = collect_all(pkg)
    datas += d
    binaries += b
    hiddenimports += h

# ffmpeg for the video and sound actions (signed again with the app).
_ffmpeg = os.path.join(ROOT, "assets", "ffmpeg", "ffmpeg")
if os.path.exists(_ffmpeg):
    binaries.append((_ffmpeg, "ffmpeg"))

a = Analysis(
    ["run_cerclic.py"],
    pathex=[ROOT],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=["PyQt5", "PyQt6", "PySide2", "tkinter", "matplotlib", "pandas",
              "pillow_heif", "scipy", "IPython", "pytest", "pytestqt",
              "PySide6.QtWebEngineCore", "PySide6.QtQml", "PySide6.QtQuick", "PySide6.QtPdf",
              "PySide6.QtSql", "PySide6.QtTest", "PySide6.QtOpenGL", "PySide6.QtDBus",
              "imageio_ffmpeg",
              "win32com", "pythoncom", "pywintypes", "win32gui"],
    noarchive=False,
)


def _wanted(entry) -> bool:
    """Drop what Cerclic never uses: Qt's own translations."""
    dest = entry[0].replace("\\", "/").lower()
    return not dest.startswith("pyside6/qt/translations/") \
        and not dest.startswith("pyside6/translations/")


a.binaries = [b for b in a.binaries if _wanted(b)]
a.datas = [d for d in a.datas if _wanted(d)]
pyz = PYZ(a.pure)

exe = EXE(
    pyz, a.scripts, [],
    exclude_binaries=True,
    name="Cerclic",
    debug=False,
    strip=False,
    upx=False,
    console=False,
    argv_emulation=False,       # files arrive as "open documents" events (app.py)
    target_arch=None,           # this Mac's own architecture
    codesign_identity=None,     # signed ad hoc, as macOS requires
    entitlements_file=None,
)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name="Cerclic")

def _imported(uti: str, conforms: str, exts: list[str], name: str) -> dict:
    """A file format macOS may not know: declared so that it counts as an
    image, a video or a sound (Quick Action, « Ouvrir avec »)."""
    return {"UTTypeIdentifier": uti, "UTTypeDescription": name,
            "UTTypeConformsTo": [conforms, "public.data"],
            "UTTypeTagSpecification": {"public.filename-extension": exts}}


IMPORTED_TYPES = [
    _imported("org.matroska.mkv", "public.movie", ["mkv"], "Vidéo Matroska"),
    _imported("org.webmproject.webm", "public.movie", ["webm"], "Vidéo WebM"),
    _imported("com.adobe.flash.video", "public.movie", ["flv"], "Vidéo Flash"),
    _imported("com.microsoft.windows-media-wmv", "public.movie", ["wmv"], "Vidéo WMV"),
    _imported("org.xiph.ogg-audio", "public.audio", ["ogg", "oga"], "Son Ogg"),
    _imported("org.xiph.opus", "public.audio", ["opus"], "Son Opus"),
    _imported("org.xiph.flac", "public.audio", ["flac"], "Son FLAC"),
    _imported("com.microsoft.windows-media-wma", "public.audio", ["wma"], "Son WMA"),
    _imported("org.3gpp.adaptive-multi-rate-audio", "public.audio", ["amr"], "Son AMR"),
    _imported("public.avif", "public.image", ["avif"], "Image AVIF"),
]

app = BUNDLE(
    coll,
    name="Cerclic.app",
    icon=os.path.join(ROOT, "assets", "cerclic.icns"),
    bundle_identifier="com.jannahmarketing.cerclic",
    version=VERSION,
    info_plist={
        "CFBundleName": "Cerclic",
        "CFBundleDisplayName": "Cerclic",
        "CFBundleShortVersionString": VERSION,
        "CFBundleVersion": VERSION,
        "CFBundleDevelopmentRegion": "fr",
        "NSPrincipalClass": "NSApplication",
        "LSUIElement": True,                         # menu bar app, no Dock icon
        "LSMinimumSystemVersion": "12.0",
        "LSApplicationCategoryType": "public.app-category.productivity",
        "NSHighResolutionCapable": True,
        "NSRequiresAquaSystemAppearance": True,      # light, like Cerclic's windows
        "NSHumanReadableCopyright": "Said El Araifa, licence MIT",
        "NSAppleEventsUsageDescription": (
            "Cerclic lit les fichiers sélectionnés dans le Finder quand tu utilises "
            "son raccourci clavier."),
        # « Ouvrir avec » and drops on the icon (never the default application)
        "CFBundleDocumentTypes": [{
            "CFBundleTypeName": "Fichier pour Cerclic",
            "CFBundleTypeRole": "Viewer",
            "LSHandlerRank": "Alternate",
            "LSItemContentTypes": ["public.image", "com.adobe.pdf", "public.movie",
                                   "public.audio", "public.audiovisual-content"],
        }],
        "UTImportedTypeDeclarations": IMPORTED_TYPES,
    },
)
