"""Catalogue of actions and the rules that pick which ones a selection offers.

An Action is metadata plus a handler with a uniform signature:
    handler(paths: list[str], opts: dict, ctx) -> list[str]
returning the output paths. `needs` lists what the UI must gather first:
    "crop"       the crop editor (image or PDF)
    "place_sig"  the signature placement editor
    "password"   a password typed in a bubble
    "text"       a text typed in a bubble
`choices` turns the action into a small ring of variants (rotate left/right...).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from ..errors import NothingToDo
from ..paths import kind_of
from . import images, pdf, video
from .common import check, progress

# Category ids, French labels and ring colours.
CATEGORIES = {
    "image": ("Image", "#4C8DFF"),
    "pdf": ("PDF", "#FF5A5F"),
    "video": ("Vidéo", "#17B890"),
}


@dataclass(frozen=True)
class Choice:
    id: str
    label: str
    icon: str
    opts: tuple = ()            # (key, value) pairs merged into opts

    def as_opts(self) -> dict:
        return dict(self.opts)


@dataclass(frozen=True)
class Action:
    id: str
    label: str
    category: str
    applies: frozenset          # file kinds this works on
    handler: Callable
    icon: str = "dot"
    needs: tuple = ()
    min_files: int = 1
    max_files: int = 0          # 0 = no limit
    primary: bool = True        # first ring; otherwise under "Plus"
    choices: tuple = field(default_factory=tuple)


def each(paths, ctx, fn) -> list[str]:
    """Run fn on every file, with progress. In a batch, files that need nothing
    (already small...) are skipped; if all of them are, the reason is shown."""
    outputs: list[str] = []
    skipped: NothingToDo | None = None
    n = len(paths)
    for i, p in enumerate(paths):
        check(ctx)
        if n > 1:
            progress(ctx, i / n, f"Fichier {i + 1} sur {n}")
        try:
            out = fn(p)
        except NothingToDo as exc:
            if n == 1:
                raise
            skipped = exc
            continue
        if isinstance(out, list):
            outputs.extend(out)
        elif out:
            outputs.append(out)
    if not outputs and skipped is not None:
        raise skipped
    return outputs


def _q(opts) -> int:
    return int(opts.get("jpg_quality", images.DEFAULT_JPG_QUALITY))


def _pw(opts):
    return opts.get("password") or None


ROTATE_CHOICES = (
    Choice("cw", "Droite", "rotate_cw", (("degrees", 90),)),
    Choice("ccw", "Gauche", "rotate_ccw", (("degrees", 270),)),
    Choice("180", "180°", "rotate_180", (("degrees", 180),)),
)

ACTIONS: list[Action] = [
    # ---- Images ----
    Action("img_crop", "Rogner", "image", frozenset({"image"}),
           lambda paths, o, ctx: [images.crop_image(paths[0], o["crop_box"], _q(o))],
           icon="crop", needs=("crop",), max_files=1),
    Action("img_convert", "Convertir", "image", frozenset({"image"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: images.convert_image(
               p, o.get("fmt", "jpg"), _q(o))),
           icon="convert",
           choices=(Choice("jpg", "JPG", "jpg", (("fmt", "jpg"),)),
                    Choice("png", "PNG", "png", (("fmt", "png"),)),
                    Choice("webp", "WEBP", "webp", (("fmt", "webp"),)))),
    Action("img_compress", "Compresser", "image", frozenset({"image"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: images.compress_image(
               p, int(o.get("quality", 70)))),
           icon="compress"),
    Action("img_resize", "Redimensionner", "image", frozenset({"image"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: images.resize_image(
               p, max_side=o.get("max_side"), percent=o.get("percent"), quality=_q(o))),
           icon="resize",
           choices=(Choice("half", "50 %", "half", (("percent", 50),)),
                    Choice("1920", "1920 px", "px", (("max_side", 1920),)),
                    Choice("1280", "1280 px", "px", (("max_side", 1280),)),
                    Choice("800", "800 px", "px", (("max_side", 800),)))),
    Action("img_rotate", "Pivoter", "image", frozenset({"image"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: images.rotate_image(
               p, int(o.get("degrees", 90)), _q(o))),
           icon="rotate", choices=ROTATE_CHOICES),
    Action("img_to_pdf", "En PDF", "image", frozenset({"image"}),
           lambda paths, o, ctx: [pdf.images_to_pdf(paths, ctx=ctx)],
           icon="topdf"),

    # ---- PDF ----
    Action("pdf_sign", "Signer", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: [pdf.sign_pdf(paths[0], o["signature"],
                                               int(o.get("page", -1)), o.get("sig_box"),
                                               _pw(o))],
           icon="sign", needs=("place_sig",), max_files=1),
    Action("pdf_crop", "Rogner", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: [pdf.crop_pdf(paths[0], o["crop_rel"],
                                               o.get("crop_page"), _pw(o))],
           icon="crop", needs=("crop",), max_files=1),
    Action("pdf_compress", "Compresser", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.compress_pdf(
               p, _pw(o), ctx)),
           icon="compress"),
    Action("pdf_merge", "Fusionner", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: [pdf.merge_pdfs(paths, _pw(o), ctx)],
           icon="merge", min_files=2),
    Action("pdf_to_images", "En images", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.pdf_to_images(
               p, o.get("fmt", "jpg"), password=_pw(o), ctx=ctx)),
           icon="image",
           choices=(Choice("jpg", "JPG", "jpg", (("fmt", "jpg"),)),
                    Choice("png", "PNG", "png", (("fmt", "png"),)))),
    Action("pdf_to_word", "En Word", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.pdf_to_word(
               p, _pw(o), ctx)),
           icon="word"),
    Action("pdf_split", "Diviser", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.split_pdf(
               p, password=_pw(o), ctx=ctx)),
           icon="split", primary=False),
    Action("pdf_rotate", "Pivoter", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.rotate_pdf(
               p, int(o.get("degrees", 90)), _pw(o))),
           icon="rotate", primary=False, choices=ROTATE_CHOICES),
    Action("pdf_watermark", "Filigrane", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.add_watermark(
               p, o["text"], _pw(o), ctx=ctx)),
           icon="watermark", needs=("text",), primary=False),
    Action("pdf_numbers", "Numéroter", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.add_page_numbers(
               p, _pw(o), ctx=ctx)),
           icon="numbers", primary=False),
    Action("pdf_protect", "Protéger", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.protect_pdf(
               p, o["new_password"])),
           icon="lock", needs=("new_password",), primary=False),
    Action("pdf_unlock", "Déverrouiller", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.unlock_pdf(
               p, o.get("password", ""))),
           icon="unlock", primary=False),

    # ---- Video ----
    Action("vid_compress", "Compresser", "video", frozenset({"video"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: video.compress_video(
               p, ctx=ctx)),
           icon="compress"),
    Action("vid_mp4", "En MP4", "video", frozenset({"video"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: video.to_mp4(p, ctx=ctx)),
           icon="mp4"),
    Action("vid_gif", "En GIF", "video", frozenset({"video"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: video.to_gif(p, ctx=ctx)),
           icon="gif"),
    Action("vid_mp3", "Extraire le son", "video", frozenset({"video"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: video.extract_mp3(
               p, ctx=ctx)),
           icon="mp3"),
]

BY_ID = {a.id: a for a in ACTIONS}

# PDF actions that read the file content and so need its password if it has one.
# (Protect refuses protected files; unlock asks for the password itself.)
PASSWORD_AWARE = {a.id for a in ACTIONS if a.category == "pdf"} - {"pdf_protect"}


def get(action_id: str) -> Action:
    return BY_ID[action_id]


def files_for(action: Action, paths: list[str]) -> list[str]:
    return [p for p in paths if kind_of(p) in action.applies]


def paths_for_action(action_id: str, paths: list[str]) -> list[str]:
    """The selected files an action should actually receive."""
    return files_for(get(action_id), paths)


def available(action: Action, paths: list[str]) -> bool:
    n = len(files_for(action, paths))
    if n < action.min_files:
        return False
    if action.max_files and n > action.max_files:
        return False
    return True


def menu_for(paths: list[str]) -> dict[str, list[Action]]:
    """{category_id: [actions]} offered for this selection, in catalogue order.

    Each family present (images, PDFs, videos) contributes its own actions,
    counted on just that family's files: a mix of photos and PDFs offers an
    Image ring and a PDF ring, and each action runs only on the files it fits.
    """
    menu: dict[str, list[Action]] = {}
    for a in ACTIONS:
        if available(a, paths):
            menu.setdefault(a.category, []).append(a)
    return menu


def count_by_category(paths: list[str]) -> dict[str, int]:
    out: dict[str, int] = {}
    for p in paths:
        k = kind_of(p)
        if k in CATEGORIES:
            out[k] = out.get(k, 0) + 1
    return out
