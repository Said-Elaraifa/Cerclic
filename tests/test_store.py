"""The Microsoft Store version: package writer and checker, resource index,
manifest, the right-click DLL (under Wine when available) and Cerclic's
behaviour inside a package."""
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "tests", "data")
sys.path.insert(0, os.path.join(ROOT, "scripts", "store"))

import msix  # noqa: E402
import pri   # noqa: E402

try:
    import lxml  # noqa: F401
    HAS_LXML = True
except ImportError:
    HAS_LXML = False

TEST_ID = {"Name": "Cerclic.Test",
           "Publisher": "CN=Cerclic Test, OID.2.25.311729368913984317654407730594956997722=1",
           "PublisherDisplayName": "Cerclic (test)"}


# ----- resource index -----------------------------------------------------------------

def test_reads_makepri_index_and_its_checksum():
    with open(os.path.join(DATA, "mozilla-Resources.pri"), "rb") as f:
        data = f.read()
    r = pri.read_pri(data)
    assert r["name"] == "firefox"
    assert r["checksum"] == r["computed_checksum"] == 0xBA2F2087
    cands = r["resources"]["Files/Assets/Square44x44Logo.png"]
    assert [v for _, v in cands][0].endswith("altform-unplated_targetsize-256.png")


def test_rebuilds_makepri_index_byte_for_byte():
    with open(os.path.join(DATA, "mozilla-Resources.pri"), "rb") as f:
        data = f.read()
    r = pri.read_pri(data)
    assert pri.build_pri("firefox", r["resources"]) == data


def test_cerclic_index_matches_firefox_tables():
    import assets
    mine = pri.read_pri(pri.build_pri("Cerclic.Test", assets.RESOURCES))
    with open(os.path.join(DATA, "mozilla-Resources.pri"), "rb") as f:
        moz = pri.read_pri(f.read())
    assert mine["decisions"] == {**moz["decisions"]}
    assert mine["name"] == "Cerclic.Test"
    assert mine["checksum"] == mine["computed_checksum"]
    assert set(mine["resources"]) == set(assets.RESOURCES)
    for logical, cands in assets.RESOURCES.items():
        got = {v for _, v in mine["resources"][logical]}
        assert got == {v for _, v in cands}


def test_index_refuses_what_windows_could_not_read():
    with pytest.raises(ValueError):
        pri.build_pri("x.y", {"Files/Assets/a.png": [((), "Assets\\é.png")]})
    with pytest.raises(ValueError):
        pri.build_pri("x.y", {"Files/Assets/a.png": [((("Scale", "200"),), "A\\a.png"),
                                                     ((("Scale", "200"),), "A\\b.png")]})
    import assets
    good = bytearray(pri.build_pri("Cerclic.Test", assets.RESOURCES))
    for at in (12, len(good) - 10, 0x60):       # size, footer, a section length
        bad = bytearray(good)
        bad[at] ^= 0x41
        with pytest.raises(pri.PriError):
            pri.read_pri(bytes(bad))


# ----- package writer and checker ---------------------------------------------------------------

def test_names_are_encoded_like_makeappx():
    for name in ("a b/é [1].png", "100%+x/=,;@^`{}'!.txt", "plain/file.dll"):
        enc = msix.encode_name(name)
        assert re.fullmatch(r"[A-Za-z0-9._/~%-]+", enc), enc
        assert msix.decode_name(enc) == name
    assert msix.encode_name("a b") == "a%20b"
    assert msix.encode_name("é") == "%C3%A9"


@pytest.mark.parametrize("bad", ["con.txt", "x/aux", "a/_rels/b.rels", "AppxManifest.xml",
                                 "AppxBlockMap.xml", "[Content_Types].xml", "AppxMetadata/x",
                                 "dir/", "name.", "name ", "a\\b", "c:x", "/abs", "a//b",
                                 "xn--foo", "a/*.txt"])
def test_names_windows_refuses(bad):
    with pytest.raises(msix.PackageError):
        msix.check_name(bad)


def test_names_windows_accepts():
    for ok in ("Cerclic.exe", "_internal/docx/templates/[Content_Types].xml",
               "a/b c/é.png", "conx.txt", "x/rels/a.rels"):
        msix.check_name(ok)


def _layout(tmp_path):
    lay = tmp_path / "layout"
    (lay / "sub dir").mkdir(parents=True)
    rnd = os.urandom(150_000)
    text = ("Cerclic " * 40_000).encode()
    (lay / "big.dll").write_bytes(text + rnd)                    # compressed, 4 blocks
    (lay / "photo.png").write_bytes(rnd[:70_000])                # stored, 2 blocks
    (lay / "empty.dat").write_bytes(b"")
    (lay / "sub dir" / "été [1].txt").write_bytes("bonjour\n".encode())
    (lay / "LICENSE").write_bytes(b"MIT\n")                      # no extension
    (lay / "notes.xml").write_bytes(b"<a/>")                     # .xml before the manifest
    (lay / "AppxManifest.xml").write_bytes(
        b'<?xml version="1.0" encoding="utf-8"?><Package xmlns='
        b'"http://schemas.microsoft.com/appx/manifest/foundation/windows10"/>')
    return lay


def test_pack_then_verify(tmp_path):
    lay = _layout(tmp_path)
    out = tmp_path / "t.msix"
    assert msix.pack(str(lay), str(out), timestamp=0) == 7
    report = msix.verify(str(out))
    assert report["files"] == 9
    assert sorted(report["names"])[0] == "AppxBlockMap.xml"
    z = zipfile.ZipFile(out)
    assert z.testzip() is None
    names = z.namelist()
    assert names[-3:] == ["AppxManifest.xml", "AppxBlockMap.xml", "[Content_Types].xml"]
    assert "sub%20dir/%C3%A9t%C3%A9%20%5B1%5D.txt" in names
    assert z.read("sub%20dir/%C3%A9t%C3%A9%20%5B1%5D.txt") == b"bonjour\n"
    info = {i.filename: i for i in z.infolist()}
    assert info["photo.png"].compress_type == zipfile.ZIP_STORED
    assert info["big.dll"].compress_type == zipfile.ZIP_DEFLATED
    assert all(i.flag_bits & 0x08 for i in z.infolist())
    ct = msix.read_file(str(out), "[Content_Types].xml").decode()
    assert '<Override ContentType="application/vnd.ms-appx.manifest+xml" ' \
           'PartName="/AppxManifest.xml"/>' in ct          # .xml was already text/xml
    assert 'PartName="/LICENSE"' in ct
    bm = msix.read_file(str(out), "AppxBlockMap.xml").decode()
    assert 'Name="sub dir\\été [1].txt"' in bm
    assert '<File Name="empty.dat" Size="0" LfhSize="39"/>' in bm


@pytest.mark.skipif(not HAS_LXML, reason="lxml absent")
def test_package_xml_follows_microsoft_schemas(tmp_path):
    from lxml import etree
    lay = _layout(tmp_path)
    out = tmp_path / "t.msix"
    msix.pack(str(lay), str(out))
    base = os.path.join(ROOT, "store", "schemas")
    for xsd, part in (("BlockMap/schema/BlockMapSchema.xsd", "AppxBlockMap.xml"),
                      ("ContentTypes/opc-contentTypes.xsd", "[Content_Types].xml")):
        schema = etree.XMLSchema(etree.parse(os.path.join(base, xsd)))
        assert schema.validate(etree.fromstring(msix.read_file(str(out), part))), \
            schema.error_log


def test_verify_finds_damage(tmp_path):
    lay = _layout(tmp_path)
    out = tmp_path / "t.msix"
    msix.pack(str(lay), str(out))
    data = out.read_bytes()
    z = zipfile.ZipFile(out)
    i = z.getinfo("photo.png")
    start = i.header_offset + 30 + len(i.filename)
    for at in (start + 10, start + 66_000):            # first block, second block
        bad = bytearray(data)
        bad[at] ^= 0xFF
        p = tmp_path / "bad.msix"
        p.write_bytes(bytes(bad))
        with pytest.raises(msix.PackageError):
            msix.verify(str(p))


def test_verify_accepts_makeappx_and_repack_matches(tmp_path):
    ref = os.path.join(DATA, "makeappx-TestAppxPackage_x64.appx")
    msix.verify(ref)
    lay = tmp_path / "lay"
    skip = {"AppxBlockMap.xml", "[Content_Types].xml", "AppxSignature.p7x",
            "AppxMetadata/CodeIntegrity.cat"}
    z = zipfile.ZipFile(ref)
    for i in z.infolist():
        if i.filename in skip:
            continue
        p = lay / msix.decode_name(i.filename)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(z.read(i))
    out = tmp_path / "re.appx"
    msix.pack(str(lay), str(out))
    msix.verify(str(out))

    def files(path):
        bm = msix.read_file(path, "AppxBlockMap.xml").decode()
        got = {}
        for m in re.finditer(r'<File ([^>]*?)(/>|>(.*?)</File>)', bm, re.S):
            attrs = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
            got[attrs["Name"]] = (attrs["Size"], attrs["LfhSize"],
                                  re.findall(r'Hash="([^"]+)"', m.group(3) or ""))
        return got
    assert files(ref) == files(str(out))


def test_block_sizes_let_windows_read_each_block_alone(tmp_path):
    lay = _layout(tmp_path)
    out = tmp_path / "t.msix"
    msix.pack(str(lay), str(out))
    import zlib
    data = out.read_bytes()
    z = zipfile.ZipFile(out)
    i = z.getinfo("big.dll")
    start = i.header_offset + 30 + len(i.filename)
    payload = data[start:start + i.compress_size]
    bm = msix.read_file(str(out), "AppxBlockMap.xml").decode()
    blocks = re.search(r'<File Name="big.dll"[^>]*>(.*?)</File>', bm).group(1)
    sizes = [int(s) for s in re.findall(r'Size="(\d+)"', blocks)]
    raw = z.read("big.dll")
    pos = 0
    for n, size in enumerate(sizes):
        assert zlib.decompressobj(-15).decompress(payload[pos:pos + size]) == \
            raw[n * 65536:(n + 1) * 65536]
        pos += size
    assert payload[pos:] == b"\x03\x00"                # the end of the stream, as makeappx


# ----- manifest ---------------------------------------------------------------------------------

def test_manifest_declares_menu_startup_and_types():
    import manifest
    from cerclic.paths import SUPPORTED_EXTS
    from cerclic.win import package
    xml = manifest.build_manifest(TEST_ID, version="0.7.0.0").decode()
    for ext in SUPPORTED_EXTS:
        assert f'<desktop5:ItemType Type="{ext}">' in xml
    assert xml.count(manifest.MENU_CLSID) == len(SUPPORTED_EXTS) + 1
    with open(os.path.join(ROOT, "native", "cerclic_menu.c"), encoding="utf-8") as f:
        c = f.read()
    assert "{" + manifest.MENU_CLSID + "}" in c
    assert f'TaskId="{package.STARTUP_TASK}"' in xml and manifest.STARTUP_TASK == package.STARTUP_TASK
    assert f'<Application Id="{package.APP_ID}"' in xml
    assert 'uap10:Parameters="--background"' in xml
    assert re.search(r'Version="\d+\.\d+\.\d+\.0"', manifest.build_manifest(TEST_ID).decode())


@pytest.mark.skipif(not HAS_LXML, reason="lxml absent")
def test_manifest_follows_microsoft_schemas():
    import manifest
    xml = manifest.build_manifest(TEST_ID)
    assert manifest.validate(xml) == []
    broken = xml.replace(b'ThreadingModel="STA"', b'ThreadingModel="Bogus"')
    assert manifest.validate(broken)


def test_manifest_identity_checked():
    import manifest
    for bad in ({**TEST_ID, "Name": "a b"}, {**TEST_ID, "Publisher": "Saïd"},
                {**TEST_ID, "PublisherDisplayName": ""}):
        with pytest.raises(ValueError):
            manifest.build_manifest(bad)


def test_identity_file_and_test_kit():
    with open(os.path.join(ROOT, "store", "identity.json"), encoding="utf-8") as f:
        ids = json.load(f)
    assert ids["test"] == TEST_ID
    assert set(ids["store"]) == {"Name", "Publisher", "PublisherDisplayName"}
    kit = os.path.join(ROOT, "store", "test-kit")
    for name in ("installer.ps1", "desinstaller.ps1", "LISEZ-MOI.txt"):
        with open(os.path.join(kit, name), "rb") as f:
            raw = f.read()
        assert raw.startswith(b"\xef\xbb\xbf")         # PowerShell 5 and Notepad read UTF-8
        assert "—".encode() not in raw and "–".encode() not in raw
    with open(os.path.join(kit, "installer.ps1"), encoding="utf-8-sig") as f:
        ps = f.read()
    assert "-AllowUnsigned" in ps and "'Cerclic.Test'" in ps


def test_logo_files(tmp_path):
    import assets
    from PySide6.QtGui import QImage
    assets.write_assets(str(tmp_path))
    for name, (w, h, _, _) in assets.ASSETS.items():
        img = QImage(str(tmp_path / "Assets" / name))
        assert (img.width(), img.height()) == (w, h), name
        assert img.hasAlphaChannel()
        corner = img.pixelColor(0, 0)
        assert corner.alpha() == 0, name               # transparent: no plate of ours


# ----- Cerclic inside a package ------------------------------------------------------------------

@pytest.fixture
def packaged(tmp_path, monkeypatch):
    monkeypatch.setenv("CERCLIC_TEST_PACKAGE_FAMILY", "Cerclic.Test_abc123xyz")
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "local"))
    root = tmp_path / "local" / "Packages" / "Cerclic.Test_abc123xyz"
    return root


def test_packaged_paths(packaged, monkeypatch):
    from cerclic import settings
    from cerclic import launcher
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    assert settings.is_packaged()
    assert not settings.is_portable()
    assert settings.config_dir() == str(packaged / "LocalState")
    monkeypatch.delenv("CERCLIC_SERVER_NAME")
    assert launcher.server_name().startswith("CerclicStore-")
    assert launcher.resident_mutex() == launcher.STORE_MUTEX


def test_classic_paths_unchanged(monkeypatch):
    from cerclic import launcher, settings
    monkeypatch.delenv("CERCLIC_SERVER_NAME")
    assert not settings.is_packaged()
    assert launcher.server_name().startswith("Cerclic-")
    assert launcher.resident_mutex() == launcher.RESIDENT_MUTEX


def test_menu_marker(packaged):
    from cerclic.win import package
    package.set_menu(False)
    assert (packaged / "LocalState" / "menu-off").exists()
    assert not package.menu_enabled()
    package.set_menu(True)
    package.set_menu(True)
    assert package.menu_enabled()


def test_open_list_from_the_right_click_entry(packaged, tmp_path):
    from cerclic import launcher
    from cerclic.win import package
    temp = packaged / "TempState"
    temp.mkdir(parents=True)
    a, b = str(tmp_path / "a b.jpg"), str(tmp_path / "é.pdf")
    good = temp / "open-12-345.txt"
    good.write_bytes(launcher.encode("open", [a, b]))
    rest, files = launcher.take_open_list(["--open-list", str(good), "--background"])
    assert files == [a, b] and rest == ["--background"]
    assert not good.exists()                            # read once, then removed
    # only the entry's own lists are read (and nothing else is ever deleted)
    for name, folder in (("notes.txt", temp), ("open-1-2.txt", tmp_path)):
        p = folder / name
        p.write_bytes(launcher.encode("open", [a]))
        assert package.read_open_list(str(p)) is None
        assert p.exists()
    junk = temp / "open-1-3.txt"
    junk.write_bytes(b"not a request")
    assert package.read_open_list(str(junk)) is None
    assert launcher.take_open_list(["a.jpg"]) == (["a.jpg"], None)


def test_old_lists_cleaned(packaged):
    from cerclic.win import package
    temp = packaged / "TempState"
    temp.mkdir(parents=True)
    old, new, other = temp / "open-1-1.txt", temp / "open-1-2.txt", temp / "keep.txt"
    for p in (old, new, other):
        p.write_text("x")
    os.utime(old, (1, 1))
    os.utime(other, (1, 1))
    package.clean_open_lists()
    assert not old.exists() and new.exists() and other.exists()


def test_settings_taken_from_the_classic_version(packaged, tmp_path, monkeypatch):
    from cerclic import settings
    classic = tmp_path / "roaming" / "Cerclic"
    classic.mkdir(parents=True)
    sig = classic / "signature.png"
    sig.write_bytes(b"png")
    (classic / "settings.json").write_text(json.dumps({
        "signature": str(sig), "hotkey_vk": 0x4B, "classic_menu": True,
        "classic_menu_by_cerclic": True, "welcome_shown": True}), encoding="utf-8")
    monkeypatch.setenv("APPDATA", str(tmp_path / "roaming"))
    assert settings.import_classic_settings()
    s = settings.Settings.load()
    assert s.get("hotkey_vk") == 0x4B
    assert s.get("classic_menu") is False and s.get("welcome_shown") is False
    assert s.get("signature") == str(packaged / "LocalState" / "signature.png")
    assert os.path.exists(s.get("signature"))
    assert not settings.import_classic_settings()     # only the first time


def test_app_inside_a_package(qtbot, packaged, monkeypatch):
    from PySide6.QtWidgets import QApplication
    from cerclic import app as app_mod
    from cerclic.win import package
    calls = []
    monkeypatch.setattr(package, "startup_state", lambda: calls.append("read") or "enabled")
    monkeypatch.setattr(package, "set_startup",
                        lambda on: calls.append(on) or ("disabled_by_user" if on else "disabled"))
    monkeypatch.setattr(package, "classic_installed", lambda: True)
    a = app_mod.CerclicApp(QApplication.instance())
    shown = []
    a.message = lambda title, text="", kind="info", buttons=None, auto_ms=8000: \
        shown.append((title, [b[0] for b in buttons or []]))
    try:
        assert a.packaged and a._quit_window is None
        assert a.right_click_how() == "clic droit, puis « Cerclic »"
        a.settings.set("context_menu", False)
        a._apply_package()
        qtbot.waitUntil(lambda: calls == ["read"], timeout=3000)
        assert not package.menu_enabled()
        qtbot.wait(50)
        assert a.settings.get("autostart") is True
        # the user turns it on, but Task Manager had it disabled: Cerclic says so
        a.open_settings()
        win = a._settings_window()
        assert win.store and "Microsoft Store" in win._version_text()
        assert win.classic is None
        a.settings.set("autostart", True)
        a._apply_package("autostart")
        qtbot.waitUntil(lambda: a.settings.get("autostart") is False, timeout=3000)
        assert calls[-1] is True
        assert not win.autostart.isChecked()
        assert shown and shown[-1][1] == ["Plus tard", "Ouvrir"]
        monkeypatch.setattr(package, "classic_uninstaller", lambda: "C:/x/unins000.exe")
        a._check_package()
        assert shown[-1] == ("Deux Cerclic installés", ["Plus tard", "Montrer le désinstalleur"])
        monkeypatch.setattr(package, "classic_uninstaller", lambda: None)
        a._check_package()
        assert shown[-1] == ("Deux Cerclic installés", ["Plus tard", "Ouvrir les applications"])
    finally:
        a.cards.close_all()
        win = a._settings_window()
        if win is not None:
            win.close()
        a.server.server.close()
        a.tray.hide()


def test_classic_choice_to_not_start_with_windows_is_kept(qtbot, packaged, tmp_path,
                                                         monkeypatch):
    from PySide6.QtWidgets import QApplication
    from cerclic import app as app_mod
    from cerclic.win import package
    classic = tmp_path / "roaming" / "Cerclic"
    classic.mkdir(parents=True)
    (classic / "settings.json").write_text(json.dumps({"autostart": False}), encoding="utf-8")
    monkeypatch.setenv("APPDATA", str(tmp_path / "roaming"))
    calls = []
    monkeypatch.setattr(package, "startup_state", lambda: calls.append("read") or "enabled")
    monkeypatch.setattr(package, "set_startup",
                        lambda on: calls.append(on) or ("enabled" if on else "disabled"))
    monkeypatch.setattr(package, "classic_installed", lambda: False)
    a = app_mod.CerclicApp(QApplication.instance())
    try:
        a._apply_package()                      # first start: the classic choice is applied
        qtbot.waitUntil(lambda: calls == [False], timeout=3000)
        qtbot.wait(50)
        assert a.settings.get("autostart") is False
        a._apply_package()                      # later starts: Windows' state is read
        qtbot.waitUntil(lambda: calls == [False, "read"], timeout=3000)
    finally:
        a.cards.close_all()
        a.server.server.close()
        a.tray.hide()


def test_package_identity_must_be_cerclics_own(monkeypatch, tmp_path):
    from cerclic.win import package
    monkeypatch.delenv("CERCLIC_TEST_PACKAGE_FAMILY", raising=False)
    monkeypatch.setattr(os, "name", "nt")
    exe = tmp_path / "app" / "Cerclic.exe"
    exe.parent.mkdir()
    monkeypatch.setattr(sys, "executable", str(exe))
    values = {}
    monkeypatch.setattr(package, "_current", lambda name: values.get(name))

    def fresh():
        package._checked = False
        package._family = None
        return package.family()
    try:
        monkeypatch.setattr(sys, "frozen", True, raising=False)
        values.update(FamilyName="Cerclic_abc", Path=str(exe.parent))
        assert fresh() == "Cerclic_abc"
        values["Path"] = str(tmp_path / "python")           # another app's identity
        assert fresh() is None
        values["Path"] = str(exe.parent)
        monkeypatch.setattr(sys, "frozen", False)            # from the sources
        assert fresh() is None
    finally:
        package._checked = False
        package._family = None


def test_store_settings_window(qtbot):
    from cerclic.settings import Settings
    from cerclic.ui.settings_window import SettingsWindow
    w = SettingsWindow(Settings(), windows_11=False, store=True)
    qtbot.addWidget(w)
    seen = []
    w.changed.connect(seen.append)
    w.set_autostart(False)
    assert not w.autostart.isChecked() and seen == []      # Windows' state, not a change
    assert w.classic is None
    from PySide6.QtWidgets import QLabel
    texts = " ".join(lbl.text() for lbl in w.findChildren(QLabel))
    assert "En glissant" not in texts
    assert "Microsoft Store" in texts


# ----- the right-click DLL, under Wine -----------------------------------------------------------------

def _wine_ready():
    return (shutil.which("wine") and shutil.which("x86_64-w64-mingw32-gcc")
            and os.environ.get("CERCLIC_WINE_TESTS"))


@pytest.mark.skipif(not _wine_ready(), reason="Wine et mingw-w64 (CERCLIC_WINE_TESTS=1)")
def test_menu_dll_under_wine(tmp_path):
    native = os.path.join(ROOT, "native")
    subprocess.run(["sh", os.path.join(native, "build.sh")], check=True, capture_output=True)
    w = tmp_path / "menu"
    w.mkdir()
    gcc = "x86_64-w64-mingw32-gcc"
    subprocess.run([gcc, "-O1", "-municode", "-o", str(w / "menu_harness.exe"),
                    os.path.join(ROOT, "tests", "native", "menu_harness.c"),
                    "-lole32", "-lshell32", "-luuid"], check=True)
    subprocess.run([gcc, "-O1", "-municode", "-mwindows", "-o", str(w / "Cerclic.exe"),
                    os.path.join(ROOT, "tests", "native", "fake_cerclic.c")], check=True)
    shutil.copy(os.path.join(ROOT, "dist_native", "CerclicMenu.dll"), w)
    (w / "photo été.jpg").write_bytes(b"x")
    (w / "doc (1).pdf").write_bytes(b"x")

    def win(p):
        return "Z:" + str(p).replace("/", "\\")
    out = subprocess.run(["wine", str(w / "menu_harness.exe"), win(w / "CerclicMenu.dll"),
                          win(w / "photo été.jpg"), win(w / "doc (1).pdf")],
                         capture_output=True, text=True, timeout=180,
                         env={**os.environ, "WINEDEBUG": "-all"})
    assert "ALL CHECKS PASSED" in out.stdout, out.stdout + out.stderr
