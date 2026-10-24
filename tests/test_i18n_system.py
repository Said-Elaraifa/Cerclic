"""Languages of the system parts: keyboard shortcut names and rules (Windows
and macOS), the languages of Cerclic.app (Info.plist, InfoPlist.strings, where
PyInstaller puts them) and of the Windows installer (Inno Setup)."""
import importlib.util
import os
import re
import sys
import types

import pytest

from cerclic import i18n, locales
from cerclic.mac import hotkey as mk
from cerclic.win import hotkey as hk

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = "touche Windows" + i18n.CTX_SEP
M = "touche Mac" + i18n.CTX_SEP
F5_FR = ("{key} sert déjà dans Windows et les applications (aide, renommer, actualiser, "
         "orthographe…). Ajoute par exemple Ctrl + Alt : Ctrl + Alt + {key}.")
CATALOG = {
    W + "Ctrl": "Ctrl", W + "Maj": "Shift", W + "Espace": "Space",
    W + "Retour": "Backspace", W + "Touche {code}": "Key {code}", W + "Pavé {key}": "Num {key}",
    M + "Maj": "Shift", M + "Espace": "Space", M + "Retour": "Return", M + "Ctrl": "Control",
    "Alt + F4 ferme les fenêtres.": "Alt + F4 closes windows.",
    F5_FR: "{key} is already used by Windows and apps. Add Ctrl + Alt: Ctrl + Alt + {key}.",
    "Cmd + Espace ouvre Spotlight.": "Command + Space opens Spotlight.",
    "Ajoute une touche après Cmd, Ctrl, Option ou Maj.": "Add a key after Command, Control, "
                                                         "Option or Shift.",
}


@pytest.fixture
def english(monkeypatch):
    """Cerclic in English, with a small catalogue; back in French afterwards."""
    monkeypatch.delenv("CERCLIC_LANG", raising=False)
    monkeypatch.setattr(locales, "load", lambda code: CATALOG if code == "en" else {})
    assert i18n.set_language("en") == "en"
    yield
    i18n.set_language("fr")
    assert i18n.current() == "fr"


def _load_script(name: str):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "scripts", name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ----- keyboard shortcut -----------------------------------------------------------------

def test_windows_shortcut_in_english(english, monkeypatch):
    monkeypatch.setattr(hk, "_layout_char", lambda vk: "")      # the AZERTY fallback
    assert hk.label(hk.MOD_CONTROL | hk.MOD_SHIFT, hk.VK_SPACE) == "Ctrl + Shift + Space"
    assert hk.label(hk.MOD_CONTROL | hk.MOD_ALT, 0x08) == "Ctrl + Alt + Backspace"
    assert hk.label(hk.MOD_WIN, 0x43) == "Win + C"            # not in the catalogue: French
    assert hk.key_name(0x61) == "Num 1" and hk.key_name(0x6B) == "Num +"
    assert hk.key_name(0xBF) == ":" and hk.key_name(0xE1) == "Key 225"
    assert hk.key_name(0xFF) == "Key 255"
    assert hk.check(hk.MOD_ALT, 0x73) == "Alt + F4 closes windows."
    assert hk.check(0, 0x74) == ("F5 is already used by Windows and apps. "
                                 "Add Ctrl + Alt: Ctrl + Alt + F5.")
    # parts are split on " + " by the settings window: never inside a name
    assert hk.label(hk.MOD_CONTROL | hk.MOD_ALT, 0x6B).split(" + ") == ["Ctrl", "Alt", "Num +"]


def test_mac_shortcut_in_english(english, monkeypatch):
    monkeypatch.setattr(mk, "_layout_char", lambda code: "")   # same answers on a Mac
    monkeypatch.setattr(mk, "_system_shortcuts", lambda: set())
    assert mk.label(mk.DEFAULT_MODS, mk.DEFAULT_VK) == "Shift + Cmd + Space"
    assert mk.label(mk.CTRL, mk.vk_of(0x24)) == "Control + Return"
    assert mk.key_name(mk.vk_of(0x00)) == "A" and mk.key_name(mk.vk_of(0x7B)) == "←"
    assert mk.check(mk.CMD, mk.VK_SPACE) == "Command + Space opens Spotlight."
    assert mk.check(mk.CMD | mk.SHIFT, mk.vk_of(0x38)) == ("Add a key after Command, "
                                                           "Control, Option or Shift.")
    # the letter rules still see the letter (French text: not in the catalogue)
    assert "Maj + Cmd + G" in mk.check(mk.CMD | mk.SHIFT, mk.vk_of(0x05))


def test_shortcut_back_in_french():
    assert i18n.current() == "fr"
    assert hk.label(hk.DEFAULT_MODS, hk.DEFAULT_VK) == "Ctrl + Alt + Espace"
    assert hk.key_name(0x08) == "Retour" and hk.key_name(0xFF) == "Touche 255"
    assert mk.label(mk.DEFAULT_MODS, mk.DEFAULT_VK) == "Maj + Cmd + Espace"
    assert hk.check(hk.MOD_CONTROL, 0x56) == (
        "Ctrl + une seule touche sert déjà dans beaucoup d'applications (gras, copier, "
        "coller, enregistrer…). Ajoute Maj ou Alt, par exemple Ctrl + Maj + V.")


def test_key_names_never_hold_the_separator():
    """The settings window shows label() as key caps, split on " + "."""
    for code in i18n.LANGS:
        if code == i18n.SOURCE:
            continue
        for key, value in locales.load(code).items():
            if key.startswith((W, M)) and isinstance(value, str):
                assert " + " not in value, (code, key, value)


def test_shortcut_texts_are_extracted():
    msgs = _load_script("i18n_messages").messages()
    tables = list(hk._RESERVED.values()) + list(mk._SYSTEM.values()) + list(mk._BY_LETTER.values())
    for text in tables + [F5_FR, W + "Retour", M + "Retour", W + "Pavé {key}", M + "Cmd",
                          "Ajoute une touche après Ctrl, Alt, Maj ou Win."]:
        assert text in msgs, text


# ----- Cerclic.app -------------------------------------------------------------------------

APPLE = {"fr": "fr", "en": "en", "es": "es", "de": "de", "it": "it", "pt": "pt-BR",
         "ar": "ar", "tr": "tr", "zh": "zh-Hans", "ja": "ja"}


def _mac_spec(monkeypatch) -> dict:
    """Run cerclic_mac.spec with PyInstaller's objects replaced: what it gives
    to Analysis and BUNDLE."""
    seen: dict = {}

    class Analysis:
        def __init__(self, scripts, **kw):
            seen["Analysis"] = kw
            self.binaries, self.datas, self.pure, self.scripts = [], [], [], []

    def keep(name):
        def make(*args, **kw):
            seen[name] = kw
            return types.SimpleNamespace()
        return make

    hooks = types.ModuleType("PyInstaller.utils.hooks")
    hooks.collect_all = lambda pkg: ([], [], [])
    for name in ("PyInstaller", "PyInstaller.utils"):
        monkeypatch.setitem(sys.modules, name, types.ModuleType(name))
    monkeypatch.setitem(sys.modules, "PyInstaller.utils.hooks", hooks)
    monkeypatch.chdir(ROOT)
    path = os.path.join(ROOT, "cerclic_mac.spec")
    code = compile(open(path, encoding="utf-8").read(), path, "exec")
    exec(code, {"__name__": "__main__", "Analysis": Analysis, "PYZ": keep("PYZ"),
                "EXE": keep("EXE"), "COLLECT": keep("COLLECT"), "BUNDLE": keep("BUNDLE")})
    return seen


def parse_strings(text: str) -> dict:
    """A .strings file ("key" = "value"; and comments), strictly."""
    entry = re.compile(r'\s*"((?:[^"\\\n]|\\.)*)"\s*=\s*"((?:[^"\\]|\\.)*)"\s*;')
    comment = re.compile(r"\s*(/\*.*?\*/|//[^\n]*)", re.S)

    def unescape(s: str) -> str:
        return re.sub(r"\\(.)", lambda m: {"n": "\n", "t": "\t"}.get(m.group(1), m.group(1)), s)

    out, pos = {}, 0
    while True:
        m = comment.match(text, pos) or entry.match(text, pos)
        if not m:
            assert not text[pos:].strip(), f"unreadable: {text[pos:pos + 60]!r}"
            return out
        if m.re is entry:
            key = unescape(m.group(1))
            assert key not in out, f"twice: {key!r}"
            out[key] = unescape(m.group(2))
        pos = m.end()


def test_parse_strings():
    text = '/* a */\n"A" = "x \\"y\\"";\n// b\n"B"="é";\n'
    assert parse_strings(text) == {"A": 'x "y"', "B": "é"}
    with pytest.raises(AssertionError):
        parse_strings('"A" = "x"\n')                          # no ;


def test_mac_bundle_declares_the_languages(monkeypatch):
    spec = _mac_spec(monkeypatch)
    plist = spec["BUNDLE"]["info_plist"]
    assert plist["CFBundleDevelopmentRegion"] == "en"
    assert sorted(plist["CFBundleLocalizations"]) == sorted(APPLE[c] for c in i18n.LANGS)
    datas = spec["Analysis"]["datas"]
    for lang in plist["CFBundleLocalizations"]:
        src = os.path.join(ROOT, "installer", "mac", f"{lang}.lproj", "InfoPlist.strings")
        assert (src, f"{lang}.lproj") in datas and os.path.isfile(src)


def test_infoplist_strings_complete(monkeypatch):
    plist = _mac_spec(monkeypatch)["BUNDLE"]["info_plist"]
    # what macOS shows of Info.plist: its own keys, and names used as keys
    want = {"NSAppleEventsUsageDescription": plist["NSAppleEventsUsageDescription"],
            "NSHumanReadableCopyright": plist["NSHumanReadableCopyright"]}
    for t in plist["CFBundleDocumentTypes"]:
        want[t["CFBundleTypeName"]] = t["CFBundleTypeName"]
    for t in plist["UTImportedTypeDeclarations"]:
        want[t["UTTypeDescription"]] = t["UTTypeDescription"]
    found = {}
    for lang in plist["CFBundleLocalizations"]:
        with open(os.path.join(ROOT, "installer", "mac", f"{lang}.lproj", "InfoPlist.strings"),
                  "rb") as f:
            text = f.read().decode("utf-8")                # UTF-8, no BOM
        found[lang] = parse_strings(text)
        assert set(found[lang]) == set(want), lang
        for key, value in found[lang].items():
            assert value.strip(), (lang, key)
            assert ("Cerclic" in value) == ("Cerclic" in want[key]), (lang, key)
            assert "\u2013" not in value and "\u2014" not in value, (lang, key)
    assert found["fr"] == want                             # French: as Info.plist says
    assert all(found[lang] != want for lang in found if lang != "fr")


def test_pyinstaller_puts_lproj_in_resources(tmp_path):
    """BUNDLE (PyInstaller) places data folders in Contents/Resources and only
    links them from Contents/Frameworks: macOS finds real .lproj folders."""
    osx = pytest.importorskip("PyInstaller.building.osx")
    src = str(tmp_path / "InfoPlist.strings")
    toc = [("Cerclic", "/x/Cerclic", "EXECUTABLE"), ("libz.dylib", "/x/libz.dylib", "BINARY"),
           ("LICENCES.txt", "/x/LICENCES.txt", "DATA"),
           ("en.lproj/InfoPlist.strings", src, "DATA"),
           ("zh-Hans.lproj/InfoPlist.strings", src, "DATA")]
    bundle = object.__new__(osx.BUNDLE)
    out = {d.replace("\\", "/"): (s.replace("\\", "/"), t)
           for d, s, t in bundle._process_bundle_toc(toc)}
    for lang in ("en", "zh-Hans"):
        assert out[f"Contents/Resources/{lang}.lproj/InfoPlist.strings"] == (src, "DATA")
        assert f"Contents/Resources/{lang}.lproj" not in out          # a real folder
        assert out[f"Contents/Frameworks/{lang}.lproj"] == (f"../Resources/{lang}.lproj",
                                                            "SYMLINK")


def test_build_mac_checks_the_lproj_folders():
    with open(os.path.join(ROOT, "scripts", "build_mac.sh"), encoding="utf-8") as f:
        script = f.read()
    assert "installer/mac/*.lproj" in script and "InfoPlist.strings" in script
    assert "CFBundleLocalizations" in script and "plutil -lint" in script


# ----- Windows installer -----------------------------------------------------------------

LANGUAGES = {"english": "compiler:Default.isl",
             "french": "compiler:Languages\\French.isl",
             "spanish": "compiler:Languages\\Spanish.isl",
             "german": "compiler:Languages\\German.isl",
             "italian": "compiler:Languages\\Italian.isl",
             "brazilianportuguese": "compiler:Languages\\BrazilianPortuguese.isl",
             "arabic": "compiler:Languages\\Arabic.isl",
             "turkish": "compiler:Languages\\Turkish.isl",
             "japanese": "compiler:Languages\\Japanese.isl"}
FRENCH = {
    "DesktopIcon": "Créer un raccourci sur le Bureau",
    "ShortcutsGroup": "Raccourcis :",
    "LaunchCerclic": "Lancer Cerclic",
    "DirNotWritable": ("Cerclic ne peut pas s'installer dans ce dossier : Windows le protège "
                       "(il faudrait des droits d'administrateur) ou il n'est pas accessible."
                       "%nChoisis un dossier à toi, par exemple dans Documents, ou garde "
                       "celui proposé."),
}


def _iss():
    with open(os.path.join(ROOT, "installer", "cerclic.iss"), encoding="utf-8-sig") as f:
        text = f.read()
    section, guard = "", False
    setup, langs, messages, arabic_guarded = {}, {}, {}, []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("#ifdef HaveArabic"):
            guard = True
        elif s.startswith("#endif"):
            guard = False
        if not s or s.startswith((";", "#")):
            continue
        m = re.fullmatch(r"\[(\w+)\]", s)
        if m:
            section = m.group(1)
        elif section == "Setup" and "=" in s:
            setup.__setitem__(*s.split("=", 1))
        elif section == "Languages":
            m = re.fullmatch(r'Name: "(\w+)"; MessagesFile: "([^"]+)"', s)
            assert m, s
            langs[m.group(1)] = m.group(2)
            arabic_guarded.append(guard if m.group(1) == "arabic" else True)
        elif section == "CustomMessages":
            m = re.fullmatch(r"(\w+)\.(\w+)=(.+)", s)
            assert m, f"custom message without language: {s}"
            messages.setdefault(m.group(1), {})[m.group(2)] = m.group(3)
            arabic_guarded.append(guard if m.group(1) == "arabic" else True)
    return text, setup, langs, messages, arabic_guarded


def test_installer_languages():
    text, setup, langs, _, arabic_guarded = _iss()
    assert langs == LANGUAGES
    assert next(iter(langs)) == "english"         # Windows in another language: English
    assert setup["ShowLanguageDialog"] == "no"    # chosen from Windows, never asked,
    assert setup["UsePreviousLanguage"] == "no"   # even when updating a French-only install
    assert setup.get("LanguageDetectionMethod", "uilanguage") == "uilanguage"
    # Arabic is official from Inno Setup 6.4.1 on: older compilers leave it out
    assert all(arabic_guarded)
    assert '#if FileExists(CompilerPath + "Languages\\Arabic.isl")' in text


def test_installer_texts_in_every_language():
    text, _, langs, messages, _ = _iss()
    used = (set(re.findall(r"\{cm:(\w+)\}", text))
            | set(re.findall(r"CustomMessage\('(\w+)'\)", text)))
    assert used == set(FRENCH)
    assert set(messages) == set(langs)
    for lang, msgs in messages.items():
        assert set(msgs) == used, lang
        for name, value in msgs.items():
            assert value.count("%n") == FRENCH[name].count("%n"), (lang, name)
            assert "%" not in value.replace("%n", ""), (lang, name)
            assert "\u2013" not in value and "\u2014" not in value, (lang, name)
    assert messages["french"] == FRENCH                    # French: as before
    assert all(messages[lang] != FRENCH for lang in messages if lang != "french")
    # no text left in French outside [CustomMessages]
    assert "Description: \"{cm:DesktopIcon}\"; GroupDescription: \"{cm:ShortcutsGroup}\"" in text
    assert "Description: \"{cm:LaunchCerclic}\"" in text
    assert "s''installer" not in text
