"""Languages of Cerclic. The French text written in the code is the source:
it is shown as is in French, and is the key of each translation catalogue
(cerclic/locales/<code>.py). Standard library only (the launcher uses it).

    tr("Rogner")                                  -> "Crop" in English
    tr("{name} est prêt", name=n)                 placeholders, by name
    trn("{n} fichier", "{n} fichiers", n)         plural forms of each language
    trc("son", "Son")                             same French word, other meaning
    N_("Rogner")                                  marks a text kept in a constant;
                                                  translated where shown: tr(value)

Rules for the catalogues: see docs/I18N.md.
"""
from __future__ import annotations

import os
import sys

# Code -> name of the language, in that language (as the language menu shows it).
LANGS = {
    "fr": "Français",
    "en": "English",
    "es": "Español",
    "de": "Deutsch",
    "it": "Italiano",
    "pt": "Português",
    "ar": "العربية",
    "tr": "Türkçe",
    "zh": "简体中文",
    "ja": "日本語",
}
SOURCE = "fr"
FALLBACK = "en"           # a computer in another language gets English
RTL = {"ar"}
NPLURALS = {"ja": 1, "zh": 1, "ar": 6}        # others: 2 (singular, plural)
CTX_SEP = "\x04"                               # trc: "context\x04text"

_lang = SOURCE
_catalog: dict = {}
_listeners: list = []


def N_(text: str) -> str:
    """Marks a text to translate that is kept as is (a constant): the place
    that shows it calls tr() on it."""
    return text


def plural_index(code: str, n) -> int:
    """Which plural form of this language goes with n (CLDR rules)."""
    try:
        n = abs(int(n)) if float(n) == int(n) else abs(float(n))
    except (TypeError, ValueError):
        n = 0
    if NPLURALS.get(code) == 1:
        return 0
    if code == "fr":
        return 0 if n < 2 else 1
    if code == "ar":
        if not isinstance(n, int):
            return 5
        if n in (0, 1, 2):
            return n
        m = n % 100
        return 3 if 3 <= m <= 10 else 4 if 11 <= m <= 99 else 5
    return 0 if n == 1 else 1


def _fmt(text: str, kw: dict) -> str:
    if not kw:
        return text
    try:
        return text.format(**kw)
    except (KeyError, IndexError, ValueError):
        return text


def tr(text: str, **kw) -> str:
    """The text in the language in use (the French text if no translation)."""
    found = _catalog.get(text) if _catalog else None
    return _fmt(found if isinstance(found, str) and found else text, kw)


def trc(context: str, text: str, **kw) -> str:
    """tr() for a French text that means different things (« Son » the
    sound, « son » his): the catalogue key is context + \\x04 + text."""
    found = _catalog.get(context + CTX_SEP + text) if _catalog else None
    return _fmt(found if isinstance(found, str) and found else text, kw)


def trn(singular: str, plural: str, n, **kw) -> str:
    """The form for n of a text that changes with a number ({n} is filled)."""
    kw.setdefault("n", n)
    forms = _catalog.get(singular) if _catalog else None
    if isinstance(forms, (list, tuple)) and forms:
        i = min(plural_index(_lang, n), len(forms) - 1)
        return _fmt(forms[i] or (singular if plural_index(SOURCE, n) == 0 else plural), kw)
    return _fmt(singular if plural_index(SOURCE, n) == 0 else plural, kw)


def current() -> str:
    return _lang


def is_rtl() -> bool:
    return _lang in RTL


def decimal(x: float, digits: int = 1) -> str:
    """A number with its decimals, written the way of the language in use
    (« 1,5 » in French, « 1.5 » in English)."""
    text = f"{x:.{digits}f}"
    return text.replace(".", ",") if _lang in ("fr", "es", "de", "it", "pt", "tr") else text


def _match(tag: str) -> str | None:
    """« fr-FR », « zh_Hans_CN », « pt-BR » -> a language Cerclic has, or None."""
    code = tag.replace("_", "-").split("-")[0].lower()
    return code if code in LANGS else None


def system_language() -> str:
    """The language of this computer's interface, if Cerclic has it; else English."""
    tags: list[str] = []
    qt = sys.modules.get("PySide6.QtCore")
    if qt is not None:
        try:
            tags += list(qt.QLocale.system().uiLanguages())
        except Exception:
            pass
    if not tags and os.name == "nt":
        try:
            import ctypes
            import locale
            lcid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            tags.append(locale.windows_locale.get(lcid, ""))
        except Exception:
            pass
    for var in ("LC_ALL", "LC_MESSAGES", "LANGUAGE", "LANG"):
        tags += [t for t in os.environ.get(var, "").split(":") if t]
    for tag in tags:
        code = _match(tag)
        if code:
            return code
    return FALLBACK


def resolve(choice: str | None) -> str:
    """The language to use for this setting: a code, or « auto » (the
    computer's). CERCLIC_LANG, when set, wins (tests, screenshots)."""
    forced = os.environ.get("CERCLIC_LANG", "")
    if forced in LANGS:
        return forced
    if choice in LANGS:
        return choice
    return system_language()


def set_language(choice: str | None) -> str:
    """Use this language from now on (« auto »: the computer's). Windows
    opened afterwards speak it; on_change() listeners rebuild the others."""
    global _lang, _catalog
    code = resolve(choice)
    if code == SOURCE:
        catalog = {}
    else:
        from .locales import load
        catalog = load(code)
    changed = code != _lang
    _lang, _catalog = code, catalog
    if changed:
        for fn in list(_listeners):
            try:
                fn()
            except Exception:
                pass
    return code


def on_change(fn) -> None:
    """Call fn() after each change of language (menus, open windows...)."""
    if fn not in _listeners:
        _listeners.append(fn)
