#!/bin/sh
# Build CerclicOpen.exe with mingw-w64 (Linux or MSYS2). Output: ../dist_native/
set -e
cd "$(dirname "$0")"
mkdir -p ../dist_native
x86_64-w64-mingw32-windres -O coff cerclic_open.rc -o cerclic_open.res
x86_64-w64-mingw32-gcc -O2 -Wall -Wextra -municode -mwindows -static -s \
  -o ../dist_native/CerclicOpen.exe cerclic_open.c cerclic_open.res -lshell32
rm -f cerclic_open.res
echo "built ../dist_native/CerclicOpen.exe"
