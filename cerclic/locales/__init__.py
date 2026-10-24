"""Translation catalogues: one module per language, T = {French text: translation}.
A text that changes with a number has a list of forms (i18n.NPLURALS)."""
from __future__ import annotations


def load(code: str) -> dict:
    """The catalogue of this language (written as plain imports, so that the
    packaged application includes every one of them)."""
    if code == "en":
        from . import en as m
    elif code == "es":
        from . import es as m
    elif code == "de":
        from . import de as m
    elif code == "it":
        from . import it as m
    elif code == "pt":
        from . import pt as m
    elif code == "ar":
        from . import ar as m
    elif code == "tr":
        from . import tr as m
    elif code == "zh":
        from . import zh as m
    elif code == "ja":
        from . import ja as m
    else:
        return {}
    return m.T
