/*
 * CerclicMenu.dll: "Cerclic" in the right-click menu of the Microsoft Store
 * version, at the top of the Windows 11 menu (and in the Windows 10 one).
 *
 * The package manifest declares this COM object for the supported file types
 * (desktop4:FileExplorerContextMenus, com:SurrogateServer). Explorer has it
 * loaded in a COM surrogate (dllhost.exe), asks for the title, icon and state
 * of the entry, then calls Invoke with the selected items. Their paths go to
 * the running Cerclic over its named pipe (CerclicStore-<session>: the Store
 * version runs apart from a classic one), with the message CerclicOpen.exe
 * sends in the classic version. If Cerclic is not running, the list is
 * written to a file in the package's TempState folder and Cerclic is started
 * through the package (so it runs as the Store app) with --open-list.
 *
 * The entry is hidden while "menu-off" exists in Cerclic's LocalState folder
 * (Cerclic writes it when "« Cerclic » dans le clic droit" is turned off).
 *
 * Build: see build.sh (mingw-w64, x64).
 */
#define COBJMACROS
#define WIN32_LEAN_AND_MEAN
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
#include <shlwapi.h>
#include <stdio.h>
#include <string.h>

/* {2E424C09-6978-44D7-88C6-0D6FBA9C0FD5}: Cerclic's entry (also in AppxManifest) */
static const GUID CLSID_CerclicMenu =
    {0x2e424c09, 0x6978, 0x44d7, {0x88, 0xc6, 0x0d, 0x6f, 0xba, 0x9c, 0x0f, 0xd5}};
static const GUID MY_IID_IUnknown =
    {0x00000000, 0x0000, 0x0000, {0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x46}};
static const GUID MY_IID_IClassFactory =
    {0x00000001, 0x0000, 0x0000, {0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x46}};
static const GUID MY_IID_IExplorerCommand =
    {0xa08ce4d0, 0xfa25, 0x44ab, {0xb5, 0x7c, 0xc7, 0xb1, 0xc3, 0x23, 0xe0, 0xb9}};
static const GUID MY_CLSID_ActivationManager =
    {0x45ba127d, 0x10a8, 0x46ea, {0x8a, 0xb7, 0x56, 0xea, 0x90, 0x78, 0x94, 0x3c}};
static const GUID MY_IID_ActivationManager =
    {0x2e941141, 0x7f97, 0x4756, {0xba, 0x1d, 0x9d, 0xec, 0xde, 0x89, 0x4a, 0x3d}};
static const GUID MY_GUID_NULL = {0, 0, 0, {0, 0, 0, 0, 0, 0, 0, 0}};

#define APP_ID L"Cerclic"            /* <Application Id="Cerclic"> */
#define PIPE_TIMEOUT_MS 3000

static HMODULE g_module;
static LONG g_locks;                  /* live objects and LockServer calls */

/* ----- where things are ---------------------------------------------------------- */

/* Folder of this DLL (and of Cerclic.exe), without the trailing backslash. */
static BOOL module_dir(wchar_t *out, DWORD cap)
{
    DWORD n = GetModuleFileNameW(g_module, out, cap);
    if (n == 0 || n >= cap)
        return FALSE;
    wchar_t *slash = wcsrchr(out, L'\\');
    if (!slash)
        return FALSE;
    *slash = 0;
    return TRUE;
}

typedef LONG (WINAPI *GetCurrentPackageFamilyName_t)(UINT32 *, PWSTR);
typedef LONG (WINAPI *PackageFamilyNameFromFullName_t)(PCWSTR, UINT32 *, PWSTR);

/* The package family name: from the surrogate's own identity, else from the
   install folder (C:\Program Files\WindowsApps\<package full name>). */
static BOOL package_family(wchar_t *pfn, UINT32 cap)
{
    HMODULE k32 = GetModuleHandleW(L"kernel32.dll");
    if (!k32)
        return FALSE;
    GetCurrentPackageFamilyName_t current =
        (GetCurrentPackageFamilyName_t)(void *)GetProcAddress(k32, "GetCurrentPackageFamilyName");
    UINT32 len = cap;
    if (current && current(&len, pfn) == ERROR_SUCCESS)
        return TRUE;
    PackageFamilyNameFromFullName_t from_full =
        (PackageFamilyNameFromFullName_t)(void *)GetProcAddress(k32, "PackageFamilyNameFromFullName");
    wchar_t dir[MAX_PATH];
    if (!from_full || !module_dir(dir, MAX_PATH))
        return FALSE;
    wchar_t *name = wcsrchr(dir, L'\\');
    if (!name)
        return FALSE;
    len = cap;
    return from_full(name + 1, &len, pfn) == ERROR_SUCCESS;
}

/* %LOCALAPPDATA%\Packages\<family>\<sub>, or FALSE outside a package. */
static BOOL package_folder(const wchar_t *sub, wchar_t *out, DWORD cap)
{
    wchar_t pfn[128];
    if (!package_family(pfn, 128))
        return FALSE;
    PWSTR local = NULL;
    if (FAILED(SHGetKnownFolderPath(&FOLDERID_LocalAppData, 0, NULL, &local)))
        return FALSE;
    int n = _snwprintf(out, cap, L"%s\\Packages\\%s\\%s", local, pfn, sub);
    CoTaskMemFree(local);
    return n > 0 && (DWORD)n < cap;
}

/* Cerclic's data folder: LocalState of the package, else beside the DLL
   (outside a package: tests). */
static BOOL data_dir(wchar_t *out, DWORD cap)
{
    if (package_folder(L"LocalState", out, cap))
        return TRUE;
    return module_dir(out, cap);
}

static BOOL menu_hidden(void)
{
    wchar_t path[MAX_PATH + 16];
    if (!data_dir(path, MAX_PATH))
        return FALSE;
    lstrcatW(path, L"\\menu-off");
    return GetFileAttributesW(path) != INVALID_FILE_ATTRIBUTES;
}

/* ----- handing the files to Cerclic ------------------------------------------------ */

/* "CERCLIC/1\nopen\n<path>\n...END\n" in UTF-8, or NULL. */
static char *build_message(IShellItemArray *items, DWORD *len, DWORD *count)
{
    static const char head[] = "CERCLIC/1\nopen\n";
    static const char tail[] = "END\n";
    size_t cap = 4096, used = 0;
    char *buf = (char *)HeapAlloc(GetProcessHeap(), 0, cap);
    if (!buf)
        return NULL;
    memcpy(buf, head, sizeof head - 1);
    used = sizeof head - 1;
    *count = 0;
    DWORD n = 0;
    if (items && FAILED(IShellItemArray_GetCount(items, &n)))
        n = 0;
    for (DWORD i = 0; i < n; i++) {
        IShellItem *item = NULL;
        if (FAILED(IShellItemArray_GetItemAt(items, i, &item)) || !item)
            continue;
        PWSTR path = NULL;
        /* A file in an ordinary folder; else its full name (inside a ZIP...),
           which Cerclic then says it cannot open. */
        if (FAILED(IShellItem_GetDisplayName(item, SIGDN_FILESYSPATH, &path)))
            if (FAILED(IShellItem_GetDisplayName(item, SIGDN_DESKTOPABSOLUTEPARSING, &path)))
                path = NULL;
        IShellItem_Release(item);
        if (!path)
            continue;
        if (path[0] && !wcschr(path, L'\n') && !wcschr(path, L'\r')) {
            int need = WideCharToMultiByte(CP_UTF8, 0, path, -1, NULL, 0, NULL, NULL);
            if (need > 1) {
                if (used + (size_t)need + sizeof tail + 1 > cap) {
                    size_t ncap = (used + (size_t)need + sizeof tail + 1) * 2;
                    char *nbuf = (char *)HeapReAlloc(GetProcessHeap(), 0, buf, ncap);
                    if (!nbuf) {
                        CoTaskMemFree(path);
                        HeapFree(GetProcessHeap(), 0, buf);
                        return NULL;
                    }
                    buf = nbuf;
                    cap = ncap;
                }
                WideCharToMultiByte(CP_UTF8, 0, path, -1, buf + used, need, NULL, NULL);
                used += (size_t)need - 1;
                buf[used++] = '\n';
                (*count)++;
            }
        }
        CoTaskMemFree(path);
    }
    if (used + sizeof tail > cap) {
        char *nbuf = (char *)HeapReAlloc(GetProcessHeap(), 0, buf, used + sizeof tail);
        if (!nbuf) {
            HeapFree(GetProcessHeap(), 0, buf);
            return NULL;
        }
        buf = nbuf;
    }
    memcpy(buf + used, tail, sizeof tail - 1);
    used += sizeof tail - 1;
    *len = (DWORD)used;
    return buf;
}

static BOOL wait_io(HANDLE h, OVERLAPPED *ov, BOOL started, DWORD *done)
{
    if (!started && GetLastError() != ERROR_IO_PENDING)
        return FALSE;
    if (WaitForSingleObject(ov->hEvent, PIPE_TIMEOUT_MS) != WAIT_OBJECT_0) {
        CancelIo(h);
        GetOverlappedResult(h, ov, done, TRUE);
        return FALSE;
    }
    return GetOverlappedResult(h, ov, done, FALSE);
}

/* 1 = delivered, 0 = no Cerclic listening. Never blocks for long: Explorer
   waits for Invoke to return. */
static int try_send(const char *msg, DWORD len)
{
    wchar_t pipe[96];
    DWORD sid = 0;
    if (!ProcessIdToSessionId(GetCurrentProcessId(), &sid))
        sid = 0;
    wsprintfW(pipe, L"\\\\.\\pipe\\CerclicStore-%lu", (unsigned long)sid);
    HANDLE h = INVALID_HANDLE_VALUE;
    for (int tries = 0;; tries++) {
        h = CreateFileW(pipe, GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING,
                        FILE_FLAG_OVERLAPPED, NULL);
        if (h != INVALID_HANDLE_VALUE)
            break;
        if (GetLastError() == ERROR_PIPE_BUSY && tries < 8) {
            WaitNamedPipeW(pipe, 250);
            continue;
        }
        return 0;
    }
    ULONG pid = 0;
    if (GetNamedPipeServerProcessId(h, &pid))
        AllowSetForegroundWindow(pid);   /* the wheel may come to the front */
    OVERLAPPED ov;
    ZeroMemory(&ov, sizeof ov);
    ov.hEvent = CreateEventW(NULL, TRUE, FALSE, NULL);
    int result = 0;
    if (ov.hEvent) {
        DWORD sent = 0;
        BOOL ok = TRUE;
        while (ok && sent < len) {
            DWORD done = 0;
            ResetEvent(ov.hEvent);
            BOOL started = WriteFile(h, msg + sent, len - sent, NULL, &ov);
            ok = wait_io(h, &ov, started, &done) && done > 0;
            sent += done;
        }
        if (ok) {
            char ack[16];
            DWORD got = 0;
            ResetEvent(ov.hEvent);
            BOOL started = ReadFile(h, ack, sizeof ack, NULL, &ov);
            wait_io(h, &ov, started, &got);   /* a late reply still means delivered */
            result = 1;
        }
        CloseHandle(ov.hEvent);
    }
    CloseHandle(h);
    return result;
}

/* Write the message for the Cerclic about to start; FALSE if impossible. */
static BOOL write_list(const char *msg, DWORD len, wchar_t *path, DWORD cap)
{
    wchar_t dir[MAX_PATH];
    if (package_folder(L"TempState", dir, MAX_PATH))
        CreateDirectoryW(dir, NULL);
    else if (!GetTempPathW(MAX_PATH, dir))
        return FALSE;
    size_t n = wcslen(dir);
    if (n && dir[n - 1] == L'\\')
        dir[n - 1] = 0;
    if (_snwprintf(path, cap, L"%s\\open-%lu-%llu.txt", dir,
                   (unsigned long)GetCurrentProcessId(),
                   (unsigned long long)GetTickCount64()) <= 0)
        return FALSE;
    HANDLE f = CreateFileW(path, GENERIC_WRITE, 0, NULL, CREATE_NEW, FILE_ATTRIBUTE_NORMAL, NULL);
    if (f == INVALID_HANDLE_VALUE)
        return FALSE;
    DWORD done = 0;
    BOOL ok = WriteFile(f, msg, len, &done, NULL) && done == len;
    CloseHandle(f);
    if (!ok)
        DeleteFileW(path);
    return ok;
}

/* Start Cerclic with the list: through the package (ActivateApplication), so
   that it runs as the Store app; else directly (outside a package). */
static BOOL start_cerclic(const wchar_t *list)
{
    wchar_t args[MAX_PATH + 32];
    _snwprintf(args, MAX_PATH + 32, L"--open-list \"%s\"", list);
    args[MAX_PATH + 31] = 0;
    wchar_t pfn[128];
    if (package_family(pfn, 128)) {
        wchar_t aumid[160];
        _snwprintf(aumid, 160, L"%s!%s", pfn, APP_ID);
        aumid[159] = 0;
        IApplicationActivationManager *aam = NULL;
        if (SUCCEEDED(CoCreateInstance(&MY_CLSID_ActivationManager, NULL, CLSCTX_LOCAL_SERVER,
                                       &MY_IID_ActivationManager, (void **)&aam)) && aam) {
            DWORD pid = 0;
            HRESULT hr = IApplicationActivationManager_ActivateApplication(
                aam, aumid, args, AO_NONE, &pid);
            IApplicationActivationManager_Release(aam);
            if (SUCCEEDED(hr)) {
                if (pid)
                    AllowSetForegroundWindow(pid);
                return TRUE;
            }
        }
    }
    wchar_t dir[MAX_PATH], exe[MAX_PATH + 16], cmd[2 * MAX_PATH + 64];
    if (!module_dir(dir, MAX_PATH))
        return FALSE;
    _snwprintf(exe, MAX_PATH + 16, L"%s\\Cerclic.exe", dir);
    exe[MAX_PATH + 15] = 0;
    _snwprintf(cmd, 2 * MAX_PATH + 64, L"\"%s\" %s", exe, args);
    cmd[2 * MAX_PATH + 63] = 0;
    STARTUPINFOW si;
    PROCESS_INFORMATION pi;
    ZeroMemory(&si, sizeof si);
    si.cb = sizeof si;
    ZeroMemory(&pi, sizeof pi);
    if (!CreateProcessW(exe, cmd, NULL, NULL, FALSE, 0, NULL, dir, &si, &pi))
        return FALSE;
    AllowSetForegroundWindow(pi.dwProcessId);
    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);
    return TRUE;
}

static void tell_failure(void)
{
    MessageBoxW(NULL,
                L"Cerclic n'a pas pu d\u00e9marrer.\n\n"
                L"Ouvre Cerclic depuis le menu D\u00e9marrer, puis r\u00e9essaie. "
                L"Si cela recommence, r\u00e9installe Cerclic depuis le Microsoft Store.",
                L"Cerclic", MB_OK | MB_ICONWARNING | MB_SETFOREGROUND | MB_TOPMOST);
}

/* ----- IExplorerCommand ------------------------------------------------------------- */

typedef struct {
    IExplorerCommand iface;
    LONG refs;
} Command;

static HRESULT STDMETHODCALLTYPE Cmd_QueryInterface(IExplorerCommand *This, REFIID riid, void **ppv)
{
    if (!ppv)
        return E_POINTER;
    if (IsEqualIID(riid, &MY_IID_IUnknown) || IsEqualIID(riid, &MY_IID_IExplorerCommand)) {
        *ppv = This;
        IExplorerCommand_AddRef(This);
        return S_OK;
    }
    *ppv = NULL;
    return E_NOINTERFACE;
}

static ULONG STDMETHODCALLTYPE Cmd_AddRef(IExplorerCommand *This)
{
    return (ULONG)InterlockedIncrement(&((Command *)This)->refs);
}

static ULONG STDMETHODCALLTYPE Cmd_Release(IExplorerCommand *This)
{
    LONG n = InterlockedDecrement(&((Command *)This)->refs);
    if (n == 0) {
        HeapFree(GetProcessHeap(), 0, This);
        InterlockedDecrement(&g_locks);
    }
    return (ULONG)n;
}

static HRESULT STDMETHODCALLTYPE Cmd_GetTitle(IExplorerCommand *This, IShellItemArray *items,
                                              LPWSTR *name)
{
    (void)This; (void)items;
    return SHStrDupW(L"Cerclic", name);
}

static HRESULT STDMETHODCALLTYPE Cmd_GetIcon(IExplorerCommand *This, IShellItemArray *items,
                                             LPWSTR *icon)
{
    (void)This; (void)items;
    wchar_t dir[MAX_PATH], res[MAX_PATH + 32];
    if (!module_dir(dir, MAX_PATH))
        return E_FAIL;
    _snwprintf(res, MAX_PATH + 32, L"%s\\Cerclic.exe,0", dir);
    res[MAX_PATH + 31] = 0;
    return SHStrDupW(res, icon);
}

static HRESULT STDMETHODCALLTYPE Cmd_GetToolTip(IExplorerCommand *This, IShellItemArray *items,
                                                LPWSTR *tip)
{
    (void)This; (void)items;
    if (tip)
        *tip = NULL;
    return E_NOTIMPL;
}

static HRESULT STDMETHODCALLTYPE Cmd_GetCanonicalName(IExplorerCommand *This, GUID *guid)
{
    (void)This;
    if (!guid)
        return E_POINTER;
    *guid = MY_GUID_NULL;
    return S_OK;
}

static HRESULT STDMETHODCALLTYPE Cmd_GetState(IExplorerCommand *This, IShellItemArray *items,
                                              WINBOOL slow_ok, EXPCMDSTATE *state)
{
    (void)This; (void)items; (void)slow_ok;
    if (!state)
        return E_POINTER;
    *state = menu_hidden() ? ECS_HIDDEN : ECS_ENABLED;
    return S_OK;
}

static HRESULT STDMETHODCALLTYPE Cmd_Invoke(IExplorerCommand *This, IShellItemArray *items,
                                            IBindCtx *bc)
{
    (void)This; (void)bc;
    DWORD len = 0, count = 0;
    char *msg = build_message(items, &len, &count);
    if (!msg)
        return E_OUTOFMEMORY;
    if (try_send(msg, len) != 1) {
        wchar_t list[MAX_PATH + 64];
        BOOL started = write_list(msg, len, list, MAX_PATH + 64);
        if (started && !start_cerclic(list)) {
            DeleteFileW(list);
            started = FALSE;
        }
        if (!started)
            tell_failure();
    }
    HeapFree(GetProcessHeap(), 0, msg);
    return S_OK;
}

static HRESULT STDMETHODCALLTYPE Cmd_GetFlags(IExplorerCommand *This, EXPCMDFLAGS *flags)
{
    (void)This;
    if (!flags)
        return E_POINTER;
    *flags = ECF_DEFAULT;
    return S_OK;
}

static HRESULT STDMETHODCALLTYPE Cmd_EnumSubCommands(IExplorerCommand *This,
                                                     IEnumExplorerCommand **list)
{
    (void)This;
    if (list)
        *list = NULL;
    return E_NOTIMPL;
}

static IExplorerCommandVtbl g_cmd_vtbl = {
    Cmd_QueryInterface, Cmd_AddRef, Cmd_Release,
    Cmd_GetTitle, Cmd_GetIcon, Cmd_GetToolTip, Cmd_GetCanonicalName,
    Cmd_GetState, Cmd_Invoke, Cmd_GetFlags, Cmd_EnumSubCommands
};

/* ----- class factory and exports ------------------------------------------------------------ */

static HRESULT STDMETHODCALLTYPE CF_QueryInterface(IClassFactory *This, REFIID riid, void **ppv)
{
    if (!ppv)
        return E_POINTER;
    if (IsEqualIID(riid, &MY_IID_IUnknown) || IsEqualIID(riid, &MY_IID_IClassFactory)) {
        *ppv = This;
        return S_OK;
    }
    *ppv = NULL;
    return E_NOINTERFACE;
}

static ULONG STDMETHODCALLTYPE CF_AddRef(IClassFactory *This)
{
    (void)This;
    return 2;
}

static ULONG STDMETHODCALLTYPE CF_Release(IClassFactory *This)
{
    (void)This;
    return 1;
}

static HRESULT STDMETHODCALLTYPE CF_CreateInstance(IClassFactory *This, IUnknown *outer,
                                                   REFIID riid, void **ppv)
{
    (void)This;
    if (!ppv)
        return E_POINTER;
    *ppv = NULL;
    if (outer)
        return CLASS_E_NOAGGREGATION;
    Command *c = (Command *)HeapAlloc(GetProcessHeap(), HEAP_ZERO_MEMORY, sizeof *c);
    if (!c)
        return E_OUTOFMEMORY;
    c->iface.lpVtbl = &g_cmd_vtbl;
    c->refs = 1;
    InterlockedIncrement(&g_locks);
    HRESULT hr = Cmd_QueryInterface(&c->iface, riid, ppv);
    Cmd_Release(&c->iface);
    return hr;
}

static HRESULT STDMETHODCALLTYPE CF_LockServer(IClassFactory *This, WINBOOL lock)
{
    (void)This;
    if (lock)
        InterlockedIncrement(&g_locks);
    else
        InterlockedDecrement(&g_locks);
    return S_OK;
}

static IClassFactoryVtbl g_cf_vtbl = {
    CF_QueryInterface, CF_AddRef, CF_Release, CF_CreateInstance, CF_LockServer
};
static IClassFactory g_factory = { &g_cf_vtbl };

HRESULT WINAPI DllGetClassObject(REFCLSID clsid, REFIID riid, void **ppv)
{
    if (!ppv)
        return E_POINTER;
    *ppv = NULL;
    if (!IsEqualCLSID(clsid, &CLSID_CerclicMenu))
        return CLASS_E_CLASSNOTAVAILABLE;
    return CF_QueryInterface(&g_factory, riid, ppv);
}

HRESULT WINAPI DllCanUnloadNow(void)
{
    return g_locks == 0 ? S_OK : S_FALSE;
}

BOOL WINAPI DllMain(HINSTANCE inst, DWORD reason, LPVOID reserved)
{
    (void)reserved;
    if (reason == DLL_PROCESS_ATTACH) {
        g_module = inst;
        DisableThreadLibraryCalls(inst);
    }
    return TRUE;
}
