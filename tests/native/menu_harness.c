/*
 * Test harness for CerclicMenu.dll (run under Wine by tests/test_store.py).
 *
 *   menu_harness.exe <CerclicMenu.dll> <file1> <file2>
 *
 * Plays Explorer's part: creates the object through DllGetClassObject, checks
 * the title, icon, flags and state (hidden while menu-off exists), then calls
 * Invoke twice: with a pipe server standing in for a running Cerclic (the
 * message must arrive intact), then with none (the DLL must start the
 * Cerclic.exe beside it with --open-list and a list file holding the same
 * message). Prints one line per check; exit code 0 when all pass.
 */
#define COBJMACROS
#ifndef UNICODE
#define UNICODE
#endif
#ifndef _UNICODE
#define _UNICODE
#endif
#include <windows.h>
#include <objbase.h>
#include <shlobj.h>
#include <shobjidl.h>
#include <stdio.h>
#include <string.h>

static const GUID CLSID_CerclicMenu =
    {0x2e424c09, 0x6978, 0x44d7, {0x88, 0xc6, 0x0d, 0x6f, 0xba, 0x9c, 0x0f, 0xd5}};
static const GUID T_IID_IClassFactory =
    {0x00000001, 0x0000, 0x0000, {0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x46}};
static const GUID T_IID_IExplorerCommand =
    {0xa08ce4d0, 0xfa25, 0x44ab, {0xb5, 0x7c, 0xc7, 0xb1, 0xc3, 0x23, 0xe0, 0xb9}};

typedef HRESULT (WINAPI *GetClassObject_t)(REFCLSID, REFIID, void **);
typedef HRESULT (WINAPI *CanUnload_t)(void);

static int failures;

static void check(int ok, const char *what)
{
    printf("%s %s\n", ok ? "OK  " : "FAIL", what);
    if (!ok)
        failures++;
}

static char received[65536];
static DWORD received_len;
static wchar_t pipe_name[96];

static DWORD WINAPI pipe_server(LPVOID ready)
{
    HANDLE p = CreateNamedPipeW(pipe_name, PIPE_ACCESS_DUPLEX, PIPE_TYPE_BYTE | PIPE_WAIT,
                                1, 65536, 65536, 0, NULL);
    SetEvent((HANDLE)ready);
    if (p == INVALID_HANDLE_VALUE)
        return 1;
    if (!ConnectNamedPipe(p, NULL) && GetLastError() != ERROR_PIPE_CONNECTED) {
        CloseHandle(p);
        return 1;
    }
    received_len = 0;
    while (received_len < sizeof received - 1) {
        DWORD got = 0;
        if (!ReadFile(p, received + received_len, sizeof received - 1 - received_len, &got, NULL)
            || got == 0)
            break;
        received_len += got;
        received[received_len] = 0;
        if (strstr(received, "\nEND\n"))
            break;
    }
    DWORD done;
    WriteFile(p, "OK\n", 3, &done, NULL);
    FlushFileBuffers(p);
    DisconnectNamedPipe(p);
    CloseHandle(p);
    return 0;
}

static IShellItemArray *make_items(int n, wchar_t **paths)
{
    PIDLIST_ABSOLUTE pidls[8];
    int count = 0;
    for (int i = 0; i < n && i < 8; i++) {
        if (SUCCEEDED(SHParseDisplayName(paths[i], NULL, &pidls[count], 0, NULL)))
            count++;
    }
    IShellItemArray *arr = NULL;
    if (count == 0 ||
        FAILED(SHCreateShellItemArrayFromIDLists((UINT)count, (PCIDLIST_ABSOLUTE_ARRAY)pidls, &arr)))
        arr = NULL;
    for (int i = 0; i < count; i++)
        CoTaskMemFree(pidls[i]);
    return arr;
}

static void expected_message(int n, wchar_t **paths, char *out, size_t cap)
{
    strcpy(out, "CERCLIC/1\nopen\n");
    for (int i = 0; i < n; i++) {
        char utf8[1024];
        WideCharToMultiByte(CP_UTF8, 0, paths[i], -1, utf8, sizeof utf8, NULL, NULL);
        strncat(out, utf8, cap - strlen(out) - 1);
        strncat(out, "\n", cap - strlen(out) - 1);
    }
    strncat(out, "END\n", cap - strlen(out) - 1);
}

int wmain(int argc, wchar_t **argv)
{
    if (argc < 4) {
        printf("usage: menu_harness <dll> <file1> <file2>\n");
        return 2;
    }
    CoInitializeEx(NULL, COINIT_APARTMENTTHREADED);
    HMODULE dll = LoadLibraryW(argv[1]);
    check(dll != NULL, "LoadLibrary");
    if (!dll)
        return 1;
    GetClassObject_t get = (GetClassObject_t)(void *)GetProcAddress(dll, "DllGetClassObject");
    CanUnload_t can_unload = (CanUnload_t)(void *)GetProcAddress(dll, "DllCanUnloadNow");
    check(get && can_unload, "exports");
    if (!get || !can_unload)
        return 1;

    GUID other = CLSID_CerclicMenu;
    other.Data1 ^= 1;
    void *unused = NULL;
    check(get(&other, &T_IID_IClassFactory, &unused) == CLASS_E_CLASSNOTAVAILABLE,
          "unknown class refused");

    IClassFactory *cf = NULL;
    check(SUCCEEDED(get(&CLSID_CerclicMenu, &T_IID_IClassFactory, (void **)&cf)) && cf,
          "class factory");
    IExplorerCommand *cmd = NULL;
    check(SUCCEEDED(IClassFactory_CreateInstance(cf, NULL, &T_IID_IExplorerCommand, (void **)&cmd))
          && cmd, "IExplorerCommand");
    if (!cmd)
        return 1;
    check(can_unload() == S_FALSE, "kept loaded while in use");

    LPWSTR s = NULL;
    check(SUCCEEDED(IExplorerCommand_GetTitle(cmd, NULL, &s)) && s && wcscmp(s, L"Cerclic") == 0,
          "title Cerclic");
    CoTaskMemFree(s);
    s = NULL;
    BOOL icon_ok = SUCCEEDED(IExplorerCommand_GetIcon(cmd, NULL, &s)) && s;
    if (icon_ok) {
        size_t n = wcslen(s);
        icon_ok = n > 14 && _wcsicmp(s + n - 14, L"\\Cerclic.exe,0") == 0;
    }
    check(icon_ok, "icon from Cerclic.exe");
    CoTaskMemFree(s);
    EXPCMDFLAGS flags = 99;
    check(SUCCEEDED(IExplorerCommand_GetFlags(cmd, &flags)) && flags == ECF_DEFAULT, "flags");

    /* state: shown, hidden while menu-off exists beside the DLL (no package here) */
    wchar_t marker[MAX_PATH];
    lstrcpyW(marker, argv[1]);
    wchar_t *slash = wcsrchr(marker, L'\\');
    if (slash)
        lstrcpyW(slash + 1, L"menu-off");
    DeleteFileW(marker);
    EXPCMDSTATE st = 99;
    check(SUCCEEDED(IExplorerCommand_GetState(cmd, NULL, TRUE, &st)) && st == ECS_ENABLED,
          "shown by default");
    HANDLE m = CreateFileW(marker, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, 0, NULL);
    CloseHandle(m);
    st = 99;
    check(SUCCEEDED(IExplorerCommand_GetState(cmd, NULL, FALSE, &st)) && st == ECS_HIDDEN,
          "hidden when turned off");
    DeleteFileW(marker);

    IShellItemArray *items = make_items(2, argv + 2);
    check(items != NULL, "items for the two files");
    char expect[8192];
    expected_message(2, argv + 2, expect, sizeof expect);

    /* 1. a running Cerclic: the message arrives on the pipe */
    DWORD sid = 0;
    ProcessIdToSessionId(GetCurrentProcessId(), &sid);
    wsprintfW(pipe_name, L"\\\\.\\pipe\\CerclicStore-%lu", (unsigned long)sid);
    HANDLE ready = CreateEventW(NULL, TRUE, FALSE, NULL);
    HANDLE t = CreateThread(NULL, 0, pipe_server, ready, 0, NULL);
    WaitForSingleObject(ready, 5000);
    Sleep(100);
    check(SUCCEEDED(IExplorerCommand_Invoke(cmd, items, NULL)), "invoke (Cerclic running)");
    WaitForSingleObject(t, 5000);
    CloseHandle(t);
    check(strcmp(received, expect) == 0, "message received intact");
    if (strcmp(received, expect) != 0)
        printf("     got: [%s]\n     want: [%s]\n", received, expect);

    /* 2. no Cerclic: the Cerclic.exe beside the DLL is started with a list */
    wchar_t launched[MAX_PATH];
    lstrcpyW(launched, argv[1]);
    slash = wcsrchr(launched, L'\\');
    if (slash)
        lstrcpyW(slash + 1, L"launched.txt");
    DeleteFileW(launched);
    check(SUCCEEDED(IExplorerCommand_Invoke(cmd, items, NULL)), "invoke (Cerclic not running)");
    char line[4096] = {0};
    for (int i = 0; i < 100; i++) {
        FILE *f = _wfopen(launched, L"rb");
        if (f) {
            size_t n = fread(line, 1, sizeof line - 1, f);
            line[n] = 0;
            fclose(f);
            if (n)
                break;
        }
        Sleep(100);
    }
    char *opt = strstr(line, "--open-list \"");
    check(opt != NULL, "Cerclic started with --open-list");
    if (opt) {
        char list_path[MAX_PATH * 3];
        strncpy(list_path, opt + 13, sizeof list_path - 1);
        list_path[sizeof list_path - 1] = 0;
        char *q = strchr(list_path, '"');
        if (q)
            *q = 0;
        char content[8192] = {0};
        FILE *f = fopen(list_path, "rb");
        size_t n = 0;
        if (f) {
            n = fread(content, 1, sizeof content - 1, f);
            fclose(f);
            remove(list_path);
        }
        content[n] = 0;
        check(strcmp(content, expect) == 0, "list file holds the message");
        check(strstr(list_path, "open-") != NULL && strstr(list_path, ".txt") != NULL,
              "list file name");
    }
    DeleteFileW(launched);

    IShellItemArray_Release(items);
    check(IExplorerCommand_Release(cmd) == 0, "released");
    check(can_unload() == S_OK, "can unload when unused");
    printf(failures ? "SOME CHECKS FAILED\n" : "ALL CHECKS PASSED\n");
    return failures ? 1 : 0;
}
