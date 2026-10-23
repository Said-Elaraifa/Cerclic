/*
 * invoke_menu.exe <CerclicMenu.dll> <file>...: plays Explorer's click on
 * "Cerclic" for these files (end-to-end checks under Wine, with the real
 * Cerclic.exe beside the DLL). Prints the entry's state, then invokes it.
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

static const GUID CLSID_CerclicMenu =
    {0x2e424c09, 0x6978, 0x44d7, {0x88, 0xc6, 0x0d, 0x6f, 0xba, 0x9c, 0x0f, 0xd5}};
static const GUID T_IID_IClassFactory =
    {0x00000001, 0x0000, 0x0000, {0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x46}};
static const GUID T_IID_IExplorerCommand =
    {0xa08ce4d0, 0xfa25, 0x44ab, {0xb5, 0x7c, 0xc7, 0xb1, 0xc3, 0x23, 0xe0, 0xb9}};

typedef HRESULT (WINAPI *GetClassObject_t)(REFCLSID, REFIID, void **);

int wmain(int argc, wchar_t **argv)
{
    if (argc < 3)
        return 2;
    CoInitializeEx(NULL, COINIT_APARTMENTTHREADED);
    HMODULE dll = LoadLibraryW(argv[1]);
    GetClassObject_t get = dll ? (GetClassObject_t)(void *)GetProcAddress(dll, "DllGetClassObject") : NULL;
    IClassFactory *cf = NULL;
    IExplorerCommand *cmd = NULL;
    if (!get || FAILED(get(&CLSID_CerclicMenu, &T_IID_IClassFactory, (void **)&cf)) ||
        FAILED(IClassFactory_CreateInstance(cf, NULL, &T_IID_IExplorerCommand, (void **)&cmd))) {
        printf("no command\n");
        return 1;
    }
    PIDLIST_ABSOLUTE pidls[64];
    int n = 0;
    for (int i = 2; i < argc && n < 64; i++)
        if (SUCCEEDED(SHParseDisplayName(argv[i], NULL, &pidls[n], 0, NULL)))
            n++;
    IShellItemArray *items = NULL;
    if (n == 0 || FAILED(SHCreateShellItemArrayFromIDLists((UINT)n, (PCIDLIST_ABSOLUTE_ARRAY)pidls,
                                                           &items))) {
        printf("no items\n");
        return 1;
    }
    EXPCMDSTATE st = 0;
    IExplorerCommand_GetState(cmd, items, TRUE, &st);
    printf("state %d\n", (int)st);
    HRESULT hr = IExplorerCommand_Invoke(cmd, items, NULL);
    printf("invoke 0x%08lx\n", (unsigned long)hr);
    IShellItemArray_Release(items);
    IExplorerCommand_Release(cmd);
    return SUCCEEDED(hr) ? 0 : 1;
}
