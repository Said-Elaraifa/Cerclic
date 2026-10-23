/*
 * CerclicOpen.exe: the tiny program behind the "Cerclic" right-click entry.
 *
 * Explorer starts one copy per selected file. Each copy hands its file to the
 * running Cerclic over a named pipe and exits within milliseconds, so even a
 * hundred files open one wheel without delay. If Cerclic is not running, one
 * copy starts it and every copy waits until it listens, then hands over.
 *
 * Message (UTF-8 lines): CERCLIC/1, open, <path>..., END   -> reply "OK".
 * Build: x86_64-w64-mingw32-gcc -O2 -municode -mwindows -static ...
 */
#define WIN32_LEAN_AND_MEAN
#ifndef UNICODE
#define UNICODE
#endif
#ifndef _UNICODE
#define _UNICODE
#endif
#include <windows.h>
#include <shellapi.h>
#include <string.h>

#define FIRST_LIFETIME_MS 45000   /* bound for a blocked pipe call */
#define WAIT_MS 30000             /* Cerclic should listen within this... */
#define WAIT_STARTING_MS 120000   /* ...or this, while it is visibly starting */

static wchar_t g_pipe[96];
static volatile ULONGLONG g_deadline;
static volatile LONG g_showing;

static DWORD WINAPI watchdog(LPVOID unused)
{
    (void)unused;
    for (;;) {
        if (!g_showing && GetTickCount64() >= g_deadline)
            ExitProcess(2);
        Sleep(250);
    }
    return 0;
}

static BOOL resident_exists(void)
{
    HANDLE h = OpenMutexW(SYNCHRONIZE, FALSE, L"Local\\Cerclic.Resident");
    if (!h)
        return FALSE;
    CloseHandle(h);
    return TRUE;
}

static void make_pipe_name(void)
{
    DWORD sid = 0;
    if (!ProcessIdToSessionId(GetCurrentProcessId(), &sid))
        sid = 0;
    wsprintfW(g_pipe, L"\\\\.\\pipe\\Cerclic-%lu", (unsigned long)sid);
}

static char *build_message(int argc, wchar_t **argv, DWORD *len)
{
    static const char head[] = "CERCLIC/1\nopen\n";
    static const char tail[] = "END\n";
    size_t cap = sizeof head + sizeof tail;
    int i;
    for (i = 1; i < argc; i++) {
        int n = WideCharToMultiByte(CP_UTF8, 0, argv[i], -1, NULL, 0, NULL, NULL);
        if (n > 0)
            cap += (size_t)n + 1;
    }
    char *buf = (char *)HeapAlloc(GetProcessHeap(), 0, cap);
    if (!buf)
        return NULL;
    char *p = buf;
    memcpy(p, head, sizeof head - 1);
    p += sizeof head - 1;
    for (i = 1; i < argc; i++) {
        if (wcschr(argv[i], L'\n') || wcschr(argv[i], L'\r') || argv[i][0] == 0)
            continue;
        int room = (int)(cap - (size_t)(p - buf));
        int n = WideCharToMultiByte(CP_UTF8, 0, argv[i], -1, p, room, NULL, NULL);
        if (n <= 1)
            continue;
        p += n - 1;     /* drop the terminating NUL */
        *p++ = '\n';
    }
    memcpy(p, tail, sizeof tail - 1);
    p += sizeof tail - 1;
    *len = (DWORD)(p - buf);
    return buf;
}

/* 1 = delivered, 0 = no Cerclic listening, -1 = write error. */
static int try_send(const char *msg, DWORD len)
{
    HANDLE h = INVALID_HANDLE_VALUE;
    int tries;
    for (tries = 0;; tries++) {
        h = CreateFileW(g_pipe, GENERIC_READ | GENERIC_WRITE, 0, NULL,
                        OPEN_EXISTING, 0, NULL);
        if (h != INVALID_HANDLE_VALUE)
            break;
        if (GetLastError() == ERROR_PIPE_BUSY && tries < 40) {
            WaitNamedPipeW(g_pipe, 250);
            continue;
        }
        return 0;
    }
    ULONG pid = 0;
    if (GetNamedPipeServerProcessId(h, &pid))
        AllowSetForegroundWindow(pid);   /* the wheel may come to the front */
    DWORD sent = 0, done = 0;
    while (sent < len) {
        if (!WriteFile(h, msg + sent, len - sent, &done, NULL)) {
            CloseHandle(h);
            return -1;
        }
        sent += done;
    }
    char ack[16];
    DWORD got = 0;
    ReadFile(h, ack, sizeof ack, &got, NULL);  /* bounded by the watchdog */
    CloseHandle(h);
    return 1;
}

/* The started Cerclic (its process handle), or NULL if it could not start. */
static HANDLE start_cerclic(void)
{
    wchar_t exe[MAX_PATH + 32];
    DWORD n = GetModuleFileNameW(NULL, exe, MAX_PATH);
    if (n == 0 || n >= MAX_PATH)
        return NULL;
    wchar_t *slash = wcsrchr(exe, L'\\');
    if (!slash)
        return NULL;
    lstrcpyW(slash + 1, L"Cerclic.exe");
    wchar_t cmd[MAX_PATH + 64];
    wsprintfW(cmd, L"\"%s\" --background", exe);
    /* Cerclic's own folder, not the clicked file's (that folder could
       otherwise not be ejected or deleted while Cerclic runs). */
    wchar_t dir[MAX_PATH + 32];
    lstrcpyW(dir, exe);
    dir[slash - exe] = 0;
    STARTUPINFOW si;
    PROCESS_INFORMATION pi;
    ZeroMemory(&si, sizeof si);
    si.cb = sizeof si;
    ZeroMemory(&pi, sizeof pi);
    if (!CreateProcessW(exe, cmd, NULL, NULL, FALSE, 0, NULL, dir, &si, &pi))
        return NULL;
    AllowSetForegroundWindow(pi.dwProcessId);
    CloseHandle(pi.hThread);
    return pi.hProcess;
}

static void tell_failure(void)
{
    g_showing = 1;
    MessageBoxW(NULL,
                L"Cerclic n'a pas pu d\u00e9marrer.\n\n"
                L"Ouvre Cerclic depuis son ic\u00f4ne (Bureau ou menu D\u00e9marrer), "
                L"puis r\u00e9essaie. Si cela recommence, r\u00e9installe Cerclic.",
                L"Cerclic", MB_OK | MB_ICONWARNING | MB_SETFOREGROUND | MB_TOPMOST);
}

int WINAPI wWinMain(HINSTANCE inst, HINSTANCE prev, PWSTR cmdline, int show)
{
    (void)inst; (void)prev; (void)cmdline; (void)show;
    int argc = 0;
    wchar_t **argv = CommandLineToArgvW(GetCommandLineW(), &argc);
    if (!argv || argc < 2)
        return 0;
    g_deadline = GetTickCount64() + FIRST_LIFETIME_MS;
    HANDLE t = CreateThread(NULL, 0, watchdog, NULL, 0, NULL);
    if (t)
        CloseHandle(t);
    make_pipe_name();
    DWORD len = 0;
    char *msg = build_message(argc, argv, &len);
    if (!msg)
        return 1;
    if (try_send(msg, len) == 1)
        return 0;

    /* Cerclic is not running: one copy starts it, every copy waits for it. */
    HANDLE launch = CreateMutexW(NULL, FALSE, L"Local\\Cerclic.Launch");
    BOOL first = launch != NULL && GetLastError() != ERROR_ALREADY_EXISTS;
    HANDLE proc = NULL;
    if (first && !resident_exists()) {  /* else it is starting already */
        proc = start_cerclic();
        if (!proc) {                    /* missing, or blocked: say so at once */
            CloseHandle(launch);
            tell_failure();
            return 1;
        }
    }
    ULONGLONG t0 = GetTickCount64();
    for (;;) {
        Sleep(100);
        if (try_send(msg, len) == 1)
            return 0;
        if (proc && WaitForSingleObject(proc, 0) == WAIT_OBJECT_0) {
            DWORD code = 0;
            if (GetExitCodeProcess(proc, &code) && code != 0 && !resident_exists())
                break;                  /* it stopped at once: no need to wait */
            CloseHandle(proc);          /* (it handed over to another one) */
            proc = NULL;
        }
        ULONGLONG waited = GetTickCount64() - t0;
        /* A slow start (logon, antivirus scan) is waited for as long as
           Cerclic is visibly starting. */
        if (waited > WAIT_MS && (!resident_exists() || waited > WAIT_STARTING_MS))
            break;
        g_deadline = GetTickCount64() + 15000;
    }
    if (first) {               /* say it once, never in silence */
        if (launch)
            CloseHandle(launch);   /* the next right-click may start it again */
        tell_failure();
    }
    return 1;
}
