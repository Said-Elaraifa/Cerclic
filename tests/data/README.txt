Reference files for tests/test_store.py:

mozilla-Resources.pri
    The resource index of Firefox's Microsoft Store package, made by Microsoft's
    makepri.exe (Mozilla, browser/installer/windows/msix/Resources.pri,
    Mozilla Public License 2.0). scripts/store/pri.py must rebuild it byte for byte.

makeappx-TestAppxPackage_x64.appx
    A package made by Microsoft's makeappx.exe, from the tests of Microsoft's
    msix-packaging SDK (MIT licence, Copyright (c) 2018 Microsoft Corporation).
    scripts/store/msix.py must accept it, and repack its files the same way.
