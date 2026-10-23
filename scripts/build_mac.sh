#!/bin/bash
# Construit Cerclic pour Mac, puis l'installe dans Applications et l'ouvre.
#
#   bash scripts/build_mac.sh            (depuis le dossier de Cerclic)
#
# Il faut macOS 12 ou plus récent et Internet. La première fois, macOS propose
# d'installer ses outils de développement (une fenêtre : « Installer »), puis la
# construction continue toute seule. Tout ce que le script télécharge (uv,
# Python, bibliothèques) reste dans le dossier .outils, à côté : le supprimer
# efface tout.
#
# Résultat : Cerclic.app dans Applications, et dist/Cerclic-<version>-mac-<puce>.dmg
# à partager. Options : --no-install (ne rien copier dans Applications),
# --no-open (ne pas lancer Cerclic à la fin).
set -euo pipefail

cd "$(dirname "$0")/.."
ROOT="$(pwd)"
TOOLS="$ROOT/.outils"
INSTALL=1
OPEN=1
for arg in "$@"; do
  case "$arg" in
    --no-install) INSTALL=0 ;;
    --no-open) OPEN=0 ;;
    *) echo "Option inconnue : $arg" >&2; exit 2 ;;
  esac
done

say()  { printf '\n\033[1;34m==> %s\033[0m\n' "$1"; }
fail() { printf '\n\033[1;31mProblème : %s\033[0m\n' "$1" >&2; exit 1; }

[ "$(uname)" = "Darwin" ] || fail "ce script se lance sur un Mac."
MACOS="$(sw_vers -productVersion)"
[ "${MACOS%%.*}" -ge 12 ] || fail "Cerclic demande macOS 12 (Monterey) ou plus récent (ici : $MACOS)."
ARCH="$(uname -m)"                       # arm64 (puce Apple) ou x86_64 (Intel)
echo "macOS $MACOS, $ARCH"

# ----- 1. outils de développement d'Apple (PyInstaller s'en sert) --------------------------
have_tools() {
  xcode-select -p >/dev/null 2>&1 && xcrun --find install_name_tool >/dev/null 2>&1
}
if ! have_tools; then
  say "Outils de développement d'Apple (une seule fois)"
  echo "Une fenêtre s'ouvre : clique sur « Installer » et accepte. Cela prend 5 à 20 minutes ;"
  echo "la construction reprend toute seule ensuite."
  xcode-select --install >/dev/null 2>&1 || true
  waited=0
  until have_tools; do
    sleep 15
    waited=$((waited + 15))
    [ $waited -lt 3600 ] || fail "les outils d'Apple ne sont pas installés. Lance « xcode-select --install », puis relance ce script."
  done
fi

# ----- 2. uv : Python et bibliothèques, dans .outils -------------------------------------------
UV_VERSION=0.13.5
if [ "$ARCH" = "arm64" ]; then
  UV_URL="https://files.pythonhosted.org/packages/d2/26/9ac45211123244ea68be852775093af487a64debc13621a2de239f8ebe73/uv-0.13.5-py3-none-macosx_11_0_arm64.whl"
  UV_SHA256="a42c85fa8156e1e5e2cecdbc77bb818ea1dcf5f78b8e2a8f84c7fe4f16f0702e"
else
  UV_URL="https://files.pythonhosted.org/packages/e3/2a/dcae794203261e49564bb9ff7c4b64a093f69ac73476cc8ce54c1deed3a1/uv-0.13.5-py3-none-macosx_10_12_x86_64.whl"
  UV_SHA256="337a14829bb499e114989df4f908f134ff37f1fb6c33497541cfb05b28080e39"
fi
UV="$TOOLS/bin/uv"
export UV_PYTHON_INSTALL_DIR="$TOOLS/python" UV_CACHE_DIR="$TOOLS/cache"
if [ ! -x "$UV" ] || [ "$("$UV" --version 2>/dev/null | cut -d' ' -f2)" != "$UV_VERSION" ]; then
  say "uv $UV_VERSION (installe Python et les bibliothèques)"
  mkdir -p "$TOOLS/bin" "$TOOLS/dl"
  curl -fL --retry 3 --progress-bar -o "$TOOLS/dl/uv.whl" "$UV_URL" \
    || fail "téléchargement impossible : vérifie la connexion Internet, puis relance."
  echo "$UV_SHA256  $TOOLS/dl/uv.whl" | shasum -a 256 -c - >/dev/null \
    || fail "le fichier téléchargé est abîmé : relance le script."
  rm -rf "$TOOLS/dl/x"
  mkdir -p "$TOOLS/dl/x"
  unzip -oq "$TOOLS/dl/uv.whl" -d "$TOOLS/dl/x"
  cp "$TOOLS"/dl/x/uv-*.data/scripts/uv "$UV"
  chmod +x "$UV"
fi

say "Python 3.12 et les bibliothèques de Cerclic"
"$UV" python install --no-bin 3.12          # stays in .outils (no link in ~/.local/bin)
rm -rf "$TOOLS/venv"
"$UV" venv --python 3.12 "$TOOLS/venv"
PY="$TOOLS/venv/bin/python"
# Libraries built for macOS 12, whatever this Mac's version: the app (and its
# disk image) then runs on every Mac from macOS 12, as its Info.plist says.
if [ "$ARCH" = "arm64" ]; then TRIPLE="aarch64-apple-darwin"; else TRIPLE="x86_64-apple-darwin"; fi
ONLY_BINARY=""
for pkg in PySide6-Essentials shiboken6 pillow pi-heif pymupdf pikepdf numpy \
           opencv-python-headless lxml pyinstaller; do
  ONLY_BINARY="$ONLY_BINARY --only-binary $pkg"
done
# shellcheck disable=SC2086
MACOSX_DEPLOYMENT_TARGET=12.0 "$UV" pip install --python "$PY" --python-platform "$TRIPLE" \
  $ONLY_BINARY -r requirements-mac.txt \
  || fail "installation des bibliothèques impossible (voir le message au-dessus)."

say "ffmpeg (vidéo et son)"
mkdir -p assets/ffmpeg
"$PY" -c "import imageio_ffmpeg, shutil; shutil.copy(imageio_ffmpeg.get_ffmpeg_exe(), 'assets/ffmpeg/ffmpeg')"
chmod +x assets/ffmpeg/ffmpeg
assets/ffmpeg/ffmpeg -hide_banner -version | head -1

# ----- 3. Cerclic.app ------------------------------------------------------------------------------
say "Construction de Cerclic.app (quelques minutes)"
rm -rf build/mac dist/mac
"$PY" -m PyInstaller --noconfirm --clean --log-level WARN \
  --distpath dist/mac --workpath build/mac cerclic_mac.spec
APP="$ROOT/dist/mac/Cerclic.app"
[ -d "$APP" ] || fail "la construction n'a pas abouti (voir les messages au-dessus)."
codesign --verify --deep --strict "$APP" 2>/dev/null || codesign --force --deep -s - "$APP"

say "Vérification de Cerclic.app"
"$APP/Contents/MacOS/Cerclic" --selftest || fail "Cerclic.app ne fonctionne pas entièrement (voir au-dessus)."

VERSION="$("$PY" -c 'import re; print(re.search(r"__version__ = \"([^\"]+)\"", open("cerclic/__init__.py").read()).group(1))')"
DMG="$ROOT/dist/Cerclic-$VERSION-mac-$ARCH.dmg"
say "Image disque à partager : dist/$(basename "$DMG")"
rm -f "$DMG"
# La fenêtre qui s'ouvre montre quoi faire : glisser Cerclic dans Applications,
# puis la marche à suivre la première fois (scripts/mac_dmg.py).
if ! "$PY" -m dmgbuild -s scripts/mac_dmg.py -D app="$APP" \
     -D background="$ROOT/assets/dmg/fond.png" "Cerclic" "$DMG"; then
  echo "(fenêtre décorée impossible : image disque simple)"
  STAGE="$ROOT/build/mac-dmg"
  rm -rf "$STAGE" "$DMG"
  mkdir -p "$STAGE"
  ditto "$APP" "$STAGE/Cerclic.app"
  ln -s /Applications "$STAGE/Applications"
  hdiutil create -quiet -volname "Cerclic" -srcfolder "$STAGE" -ov -format UDZO "$DMG"
  rm -rf "$STAGE"
fi

# ----- 4. installation ----------------------------------------------------------------------------
if [ $INSTALL = 1 ]; then
  say "Installation dans Applications"
  if pgrep -x Cerclic >/dev/null 2>&1; then           # an older Cerclic is running
    "$APP/Contents/MacOS/Cerclic" --quit >/dev/null 2>&1 || true
    for _ in 1 2 3 4 5 6 7 8 9 10; do
      pgrep -x Cerclic >/dev/null 2>&1 || break
      sleep 0.5
    done
  fi
  DEST="/Applications"
  [ -w "$DEST" ] || DEST="$HOME/Applications"
  mkdir -p "$DEST"
  if [ -d "$DEST/Cerclic.app" ]; then
    # A new build has a new signature: macOS would keep refusing the Finder
    # to it without asking. Forget the old answer, macOS will ask again.
    tccutil reset AppleEvents com.jannahmarketing.cerclic >/dev/null 2>&1 || true
  fi
  if rm -rf "$DEST/Cerclic.app" && ditto "$APP" "$DEST/Cerclic.app"; then
    rm -rf "$APP"         # one Cerclic.app only: macOS opens files with this one
    echo "Installé : $DEST/Cerclic.app"
    if [ $OPEN = 1 ]; then
      open "$DEST/Cerclic.app"
    fi
  else
    echo "Copie impossible : ouvre l'image disque et glisse Cerclic dans Applications."
    open "$DMG"
  fi
fi

say "Terminé"
echo "Cerclic tourne dans la barre des menus, en haut de l'écran."
echo "Clic droit sur une image, un PDF, une vidéo ou un son : Actions rapides, puis « Cerclic »."
echo "Ou sélectionne-les dans le Finder et appuie sur Maj + Cmd + Espace."
