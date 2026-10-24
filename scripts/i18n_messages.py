"""The texts to translate: every tr("..."), trc("...", "..."), trn("...", "...", n)
and N_("...") of cerclic/, found in the code itself (ast), with where they are.

    python scripts/i18n_messages.py                 all the texts, as JSON
    python scripts/i18n_messages.py --missing en    those the English catalogue lacks
    python scripts/i18n_messages.py --check         every catalogue complete and right
"""
from __future__ import annotations

import ast
import json
import os
import string
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODE = os.path.join(ROOT, "cerclic")
SKIP = {os.path.join(CODE, "locales"), os.path.join(CODE, "i18n.py")}
CTX_SEP = "\x04"


def _name(func) -> str:
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return ""


def _lit(node) -> str | None:
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def messages() -> dict:
    """{key: {"plural": French plural or None, "where": [...]}} in code order."""
    found: dict = {}
    for folder, _, files in os.walk(CODE):
        if folder in SKIP or "__pycache__" in folder:
            continue
        for f in sorted(files):
            path = os.path.join(folder, f)
            if not f.endswith(".py") or path in SKIP:
                continue
            tree = ast.parse(open(path, encoding="utf-8").read(), path)
            rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                fn, args = _name(node.func), node.args
                key = plural = None
                if fn in ("tr", "N_") and args:
                    key = _lit(args[0])
                elif fn == "trc" and len(args) >= 2 and _lit(args[0]) and _lit(args[1]):
                    key = _lit(args[0]) + CTX_SEP + _lit(args[1])
                elif fn == "trn" and len(args) >= 2:
                    key, plural = _lit(args[0]), _lit(args[1])
                if key is None:
                    continue
                entry = found.setdefault(key, {"plural": plural, "where": []})
                entry["where"].append(f"{rel}:{node.lineno}")
                if plural:
                    entry["plural"] = plural
    return found


def fields(text: str) -> set:
    """The {placeholders} of a text."""
    out = set()
    for _, name, _, _ in string.Formatter().parse(text):
        if name is not None:
            out.add(name)
    return out


def catalog(code: str) -> dict:
    sys.path.insert(0, ROOT)
    from cerclic.locales import load
    return load(code)


def problems(code: str, msgs: dict | None = None) -> list[str]:
    """What is wrong with this catalogue: missing, unknown, wrong placeholders,
    wrong number of plural forms."""
    sys.path.insert(0, ROOT)
    from cerclic.i18n import NPLURALS
    msgs = messages() if msgs is None else msgs
    cat = catalog(code)
    out = []
    for key, m in msgs.items():
        if key not in cat:
            out.append(f"{code}: manque {key!r} ({m['where'][0]})")
            continue
        value = cat[key]
        source = key.split(CTX_SEP)[-1]
        want = fields(source) | (fields(m["plural"]) if m["plural"] else set())
        if m["plural"]:
            n = NPLURALS.get(code, 2)
            if not isinstance(value, (list, tuple)) or len(value) != n:
                out.append(f"{code}: {key!r} demande {n} forme(s) au pluriel")
                continue
            values = list(value)
        elif not isinstance(value, str) or not value.strip():
            out.append(f"{code}: {key!r} doit être un texte non vide")
            continue
        else:
            values = [value]
        for v in values:
            got = fields(v)
            if m["plural"]:
                want_v, got_v = want - {"n"}, got - {"n"}   # « une page » may drop {n}
            else:
                want_v, got_v = want, got
            if got_v != want_v:
                out.append(f"{code}: {key!r} : champs {sorted(got)} au lieu de {sorted(want)}")
    for key in cat:
        if key not in msgs:
            out.append(f"{code}: inconnu {key!r}")
    return out


def main(argv: list[str]) -> int:
    msgs = messages()
    if "--missing" in argv:
        code = argv[argv.index("--missing") + 1]
        cat = catalog(code)
        print(json.dumps({k: v for k, v in msgs.items() if k not in cat},
                         ensure_ascii=False, indent=1))
        return 0
    if "--check" in argv:
        sys.path.insert(0, ROOT)
        from cerclic.i18n import LANGS, SOURCE
        bad = [p for code in LANGS if code != SOURCE for p in problems(code, msgs)]
        print("\n".join(bad) or f"{len(msgs)} textes, toutes les langues complètes")
        return 1 if bad else 0
    print(json.dumps(msgs, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
