#!/bin/bash
# Build Cerclic for Windows from Linux, with Wine and mingw-w64.
# (The GitHub workflow does the same steps on a Windows machine.)
#
# Needs: a Windows Python with requirements-dev.txt installed  -> $WINPY
#        Inno Setup's ISCC.exe                                  -> $ISCC
#        the imageio-ffmpeg win_amd64 wheel (for ffmpeg.exe)   -> $FFMPEG_WHEEL
#        x86_64-w64-mingw32-gcc and -windres, wine, unzip, zip, python3 with pip
# Output: dist/Cerclic/ (app folder), dist_installer/CerclicSetup-<v>.exe,
#         dist_installer/Cerclic-<v>-portable.zip
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
: "${WINPY:?set WINPY to the Windows python.exe}"
: "${ISCC:?set ISCC to ISCC.exe}"
: "${FFMPEG_WHEEL:?set FFMPEG_WHEEL to imageio_ffmpeg-*-win_amd64.whl}"
export WINEDEBUG=-all
VERSION=$(python3 -c "import re;print(re.search(r'__version__ = \"(.+?)\"', open('cerclic/__init__.py').read()).group(1))")
echo "== Cerclic $VERSION"

echo "== 1/6 native forwarder"
native/build.sh

echo "== 2/6 ffmpeg"
mkdir -p assets/ffmpeg build/ffmpeg_wheel
unzip -q -o "$FFMPEG_WHEEL" -d build/ffmpeg_wheel
cp "$(find build/ffmpeg_wheel -name 'ffmpeg-win*.exe' | head -1)" assets/ffmpeg/ffmpeg.exe

echo "== 3/6 PyInstaller's starter (bootloader), compiled from its sources"
# Antivirus programs know the ready-made PyInstaller starter, which malware
# authors use too: Cerclic.exe starts with one built here, from PyInstaller's
# own sources (same code, compiled with mingw-w64).
PYI_VERSION=$(wine "$WINPY" -c "import PyInstaller; print(PyInstaller.__version__)" 2>/dev/null | tr -d '\r')
BOOT_DIR="build/bootloader-$PYI_VERSION"
if [ ! -f "$BOOT_DIR/runw.exe" ]; then
  rm -rf build/pyi-src
  mkdir -p build/pyi-src "$BOOT_DIR"
  "${PYTHON:-python3}" -m pip download --quiet --no-binary=:all: --no-deps \
    "pyinstaller==$PYI_VERSION" -d build/pyi-src
  tar -xzf "build/pyi-src/pyinstaller-$PYI_VERSION.tar.gz" -C build/pyi-src
  (cd "build/pyi-src/pyinstaller-$PYI_VERSION/bootloader" \
    && CC=x86_64-w64-mingw32-gcc WINDRES=x86_64-w64-mingw32-windres \
       "${PYTHON:-python3}" ./waf all --gcc --target-arch=64bit > ../../waf.log 2>&1)
  cp "build/pyi-src/pyinstaller-$PYI_VERSION/PyInstaller/bootloader/Windows-64bit-intel/"run*.exe \
    "$BOOT_DIR/"
fi
cp "$BOOT_DIR"/run*.exe "$(dirname "$WINPY")/Lib/site-packages/PyInstaller/bootloader/Windows-64bit-intel/"

echo "== 4/6 PyInstaller"
# A conda-based Windows Python keeps the DLLs of its stdlib (libffi, bz2, lzma...)
# in Library\bin: put it on the search path so PyInstaller bundles them.
if [ -d "$(dirname "$WINPY")/Library/bin" ]; then
  WINEPATH="$(winepath -w "$(dirname "$WINPY")/Library/bin" 2>/dev/null)"
  export WINEPATH
fi
rm -rf dist/Cerclic build/Cerclic
wine "$WINPY" -m PyInstaller cerclic.spec --noconfirm --clean < /dev/null 2>&1 | cat \
  > build/pyinstaller.log
grep -E "ERROR|WARNING: (Hidden|lib not found|Library not found)|Building COLLECT" build/pyinstaller.log || true
test -f dist/Cerclic/Cerclic.exe
cp dist_native/CerclicOpen.exe dist/Cerclic/CerclicOpen.exe
cp assets/LICENCES.txt dist/Cerclic/LICENCES.txt

echo "== 5/6 portable zip"
mkdir -p dist_installer
rm -f "dist_installer/Cerclic-$VERSION-portable.zip"
(cd dist && zip -q -r -9 "../dist_installer/Cerclic-$VERSION-portable.zip" Cerclic)

echo "== 6/6 installer"
python3 scripts/gen_installer_registry.py >/dev/null 2>&1 || true
wine "$ISCC" /Q "/DMyAppVersion=$VERSION" installer/cerclic.iss < /dev/null 2>&1 | cat
ls -la dist_installer/
