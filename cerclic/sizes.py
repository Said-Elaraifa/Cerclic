"""File sizes in words, the way the file manager shows them: the Explorer
counts in 1024s (1 Ko = 1024 octets), the Finder in 1000s."""
from __future__ import annotations

import os
import sys

from .i18n import decimal, tr, trn

BASE = 1000 if sys.platform == "darwin" else 1024


def _unit(i: int, size: str) -> str:
    """size + unit (Ko, Mo, Go, To), as each language writes them."""
    if i == 0:
        return tr("{size} Ko", size=size)
    if i == 1:
        return tr("{size} Mo", size=size)
    if i == 2:
        return tr("{size} Go", size=size)
    return tr("{size} To", size=size)


def human(n: float) -> str:
    """1 234 567 octets -> « 1,2 Mo »."""
    n = max(0.0, float(n))
    if n < BASE:
        return trn("{n} octet", "{n} octets", int(n))
    for i in range(4):
        n /= BASE
        if n < BASE - 0.5 or i == 3:
            return _unit(i, decimal(n, 1 if n < 10 else 0))
    return ""


def size_of(paths) -> int:
    """Bytes of these files; a folder (the pages of a PDF as images...)
    counts for everything in it."""
    total = 0
    for p in paths:
        try:
            if os.path.isdir(p):
                for root, _, names in os.walk(p):
                    for name in names:
                        try:
                            total += os.path.getsize(os.path.join(root, name))
                        except OSError:
                            pass
            else:
                total += os.path.getsize(p)
        except OSError:
            pass
    return total


def gain(before: float, after: float) -> str:
    """« 85 % de moins », or how much bigger: the change in words."""
    if before <= 0:
        return ""
    pct = round((before - after) * 100 / before)
    if pct > 0:
        return tr("{pct} % de moins", pct=pct)
    if pct < 0:
        return tr("{pct} % de plus", pct=-pct)
    return tr("même taille")


def change(before: float, after: float) -> str:
    """« De 4,2 Mo à 612 Ko · 85 % de moins » (in words: an arrow is missing
    from some fonts)."""
    text = tr("De {before} à {after}", before=human(before), after=human(after))
    g = gain(before, after)
    return f"{text} · {g}" if g else text
