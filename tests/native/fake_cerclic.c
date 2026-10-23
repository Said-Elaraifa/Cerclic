/* Stands in for Cerclic.exe in the CerclicMenu.dll test: writes its command
   line (UTF-8) to launched.txt beside itself, then exits. */
#ifndef UNICODE
#define UNICODE
#endif
#ifndef _UNICODE
#define _UNICODE
#endif
#include <windows.h>

int WINAPI wWinMain(HINSTANCE inst, HINSTANCE prev, PWSTR cmdline, int show)
{
    (void)inst; (void)prev; (void)cmdline; (void)show;
    wchar_t path[MAX_PATH + 16];
    DWORD n = GetModuleFileNameW(NULL, path, MAX_PATH);
    if (n == 0 || n >= MAX_PATH)
        return 1;
    wchar_t *slash = wcsrchr(path, L'\\');
    if (!slash)
        return 1;
    lstrcpyW(slash + 1, L"launched.txt");
    char utf8[8192];
    int len = WideCharToMultiByte(CP_UTF8, 0, GetCommandLineW(), -1, utf8, sizeof utf8, NULL, NULL);
    if (len <= 0)
        return 1;
    HANDLE f = CreateFileW(path, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, 0, NULL);
    if (f == INVALID_HANDLE_VALUE)
        return 1;
    DWORD done;
    WriteFile(f, utf8, (DWORD)(len - 1), &done, NULL);
    CloseHandle(f);
    return 0;
}
