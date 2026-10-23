#!/bin/sh
# Build the native helpers with mingw-w64 (Linux or MSYS2). Output: ../dist_native/
#   CerclicOpen.exe   the right-click entry of the classic version
#   CerclicMenu.dll   the right-click entry of the Microsoft Store version
set -e
cd "$(dirname "$0")"
mkdir -p ../dist_native
HARDEN="-Wl,--dynamicbase,--nxcompat,--high-entropy-va"
x86_64-w64-mingw32-windres -O coff cerclic_open.rc -o cerclic_open.res
x86_64-w64-mingw32-gcc -O2 -Wall -Wextra -municode -mwindows -static -s $HARDEN \
  -o ../dist_native/CerclicOpen.exe cerclic_open.c cerclic_open.res -lshell32
rm -f cerclic_open.res
x86_64-w64-mingw32-windres -O coff cerclic_menu.rc -o cerclic_menu.res
x86_64-w64-mingw32-gcc -O2 -Wall -Wextra -shared -s -static-libgcc $HARDEN \
  -o ../dist_native/CerclicMenu.dll cerclic_menu.c cerclic_menu.def cerclic_menu.res \
  -lole32 -lshell32 -lshlwapi -luuid -luser32
rm -f cerclic_menu.res
echo "built ../dist_native/CerclicOpen.exe and CerclicMenu.dll"
