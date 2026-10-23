#!/bin/sh
# Build Cerclic's Microsoft Store package (MSIX) after scripts/build_windows.sh.
# Needs a Python with PySide6 and lxml (requirements-dev.txt): $PYTHON.
# Output: dist_store/ (see scripts/store/build.py)
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
sh native/build.sh
"${PYTHON:-python3}" scripts/store/build.py
