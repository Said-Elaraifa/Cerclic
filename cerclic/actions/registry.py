"""Catalogue of actions and the rules that pick which ones a selection offers.

An Action is metadata plus a handler. The handler signature is uniform:
    handler(paths: list[str], opts: dict) -> list[str]
returning the output paths. `needs` lists inputs the UI must gather first
(a crop box, a password, the signature image, some text). `combine` marks an
action that consumes the whole selection as one set instead of file by file.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from . import images, pdf, video
from ..paths import kind_of

# Category ids and their French labels / ring colours.
CATEGORIES = {
    "image": ("Image", "#4C8DFF"),
    "pdf": ("PDF", "#FF5A5F"),
    "video": ("Vidéo", "#17B890"),
    "ai": ("IA", "#A66BFF"),
}


@dataclass(frozen=True)
class Action:
    id: str
    label: str
    category: str
    applies: frozenset          # file kinds this works on
    handler: Callable
    icon: str = "dot"
    needs: tuple = ()           # e.g. ("crop_box",), ("password",)
    combine: bool = False       # consume the selection as one set
    min_files: int = 1
    primary: bool = False       # surface directly in the top ring


def _img(paths, opts, fn, **kw):
    return [fn(p, **kw) for p in paths]


ACTIONS: list[Action] = [
    # ---- Images ----
    Action("img_crop", "Rogner", "image", frozenset({"image"}),
           lambda paths, opts: [images.crop_image(paths[0], opts["crop_box"])],
           icon="crop", needs=("crop_box",), primary=True, min_files=1),
    Action("img_jpg", "En JPG", "image", frozenset({"image"}),
           lambda paths, opts: _img(paths, opts, images.convert_image, fmt="jpg"),
           icon="jpg", primary=True),
    Action("img_png", "En PNG", "image", frozenset({"image"}),
           lambda paths, opts: _img(paths, opts, images.convert_image, fmt="png"),
           icon="png"),
    Action("img_webp", "En WEBP", "image", frozenset({"image"}),
           lambda paths, opts: _img(paths, opts, images.convert_image, fmt="webp"),
           icon="webp"),
    Action("img_compress", "Compresser", "image", frozenset({"image"}),
           lambda paths, opts: _img(paths, opts, images.compress_image,
                                    quality=opts.get("quality", 70)),
           icon="compress", primary=True),
    Action("img_resize", "Redimensionner", "image", frozenset({"image"}),
           lambda paths, opts: _img(paths, opts, images.resize_image,
                                    max_side=opts.get("max_side", 1600)),
           icon="resize"),
    Action("img_rotate", "Pivoter", "image", frozenset({"image"}),
           lambda paths, opts: _img(paths, opts, images.rotate_image,
                                    degrees=opts.get("degrees", 90)),
           icon="rotate"),
    Action("img_to_pdf", "Images en PDF", "image", frozenset({"image"}),
           lambda paths, opts: [pdf.images_to_pdf(paths)],
           icon="topdf", combine=True, min_files=1, primary=True),

    # ---- PDF ----
    Action("pdf_to_jpg", "En JPG", "pdf", frozenset({"pdf"}),
           lambda paths, opts: _flatten_lists(
               [pdf.pdf_to_images(p, fmt="jpg") for p in paths]),
           icon="jpg", primary=True),
    Action("pdf_to_png", "En PNG", "pdf", frozenset({"pdf"}),
           lambda paths, opts: _flatten_lists(
               [pdf.pdf_to_images(p, fmt="png") for p in paths]),
           icon="png"),
    Action("pdf_to_word", "En Word", "pdf", frozenset({"pdf"}),
           lambda paths, opts: _img(paths, opts, pdf.pdf_to_word),
           icon="word", primary=True),
    Action("pdf_compress", "Compresser", "pdf", frozenset({"pdf"}),
           lambda paths, opts: _img(paths, opts, pdf.compress_pdf),
           icon="compress", primary=True),
    Action("pdf_merge", "Fusionner", "pdf", frozenset({"pdf"}),
           lambda paths, opts: [pdf.merge_pdfs(paths)],
           icon="merge", combine=True, min_files=2, primary=True),
    Action("pdf_split", "Diviser", "pdf", frozenset({"pdf"}),
           lambda paths, opts: _flatten_lists(
               [pdf.split_pdf(p, every=opts.get("every", 1)) for p in paths]),
           icon="split", primary=True),
    Action("pdf_rotate", "Pivoter", "pdf", frozenset({"pdf"}),
           lambda paths, opts: _img(paths, opts, pdf.rotate_pdf,
                                    degrees=opts.get("degrees", 90)),
           icon="rotate"),
    Action("pdf_sign", "Signer", "pdf", frozenset({"pdf"}),
           lambda paths, opts: _img(paths, opts, pdf.sign_pdf,
                                    signature_png=opts["signature"]),
           icon="sign", needs=("signature",), primary=True),
    Action("pdf_watermark", "Filigrane", "pdf", frozenset({"pdf"}),
           lambda paths, opts: _img(paths, opts, pdf.add_watermark,
                                    text=opts["text"]),
           icon="watermark", needs=("text",)),
    Action("pdf_numbers", "Numéros de page", "pdf", frozenset({"pdf"}),
           lambda paths, opts: _img(paths, opts, pdf.add_page_numbers),
           icon="numbers"),
    Action("pdf_protect", "Protéger", "pdf", frozenset({"pdf"}),
           lambda paths, opts: _img(paths, opts, pdf.protect_pdf,
                                    password=opts["password"]),
           icon="lock", needs=("password",)),
    Action("pdf_unlock", "Déverrouiller", "pdf", frozenset({"pdf"}),
           lambda paths, opts: _img(paths, opts, pdf.unlock_pdf,
                                    password=opts.get("password", "")),
           icon="unlock", needs=("password?",)),

    # ---- Video ----
    Action("vid_compress", "Compresser", "video", frozenset({"video"}),
           lambda paths, opts: _img(paths, opts, video.compress_video),
           icon="compress", primary=True),
    Action("vid_mp4", "En MP4", "video", frozenset({"video"}),
           lambda paths, opts: _img(paths, opts, video.to_mp4),
           icon="mp4", primary=True),
    Action("vid_gif", "En GIF", "video", frozenset({"video"}),
           lambda paths, opts: _img(paths, opts, video.to_gif),
           icon="gif", primary=True),
    Action("vid_mp3", "Extraire le son", "video", frozenset({"video"}),
           lambda paths, opts: _img(paths, opts, video.extract_mp3),
           icon="mp3", primary=True),
]

BY_ID = {a.id: a for a in ACTIONS}


def _flatten_lists(lists: list[list[str]]) -> list[str]:
    out: list[str] = []
    for part in lists:
        out.extend(part)
    return out


def get(action_id: str) -> Action:
    return BY_ID[action_id]


def selection_kinds(paths: list[str]) -> set[str]:
    return {kind_of(p) for p in paths}


def paths_for_action(action_id: str, paths: list[str]) -> list[str]:
    """The selected files an action should actually receive: those whose family
    it applies to, in the original order."""
    a = get(action_id)
    return [p for p in paths if kind_of(p) in a.applies]


def menu_for(paths: list[str]) -> dict[str, list[Action]]:
    """Return {category_id: [actions]} offered for this selection.

    Built per family: each present family (image, pdf, video) contributes its
    own actions, counted against just that family's files. So a mixed selection
    of photos and PDFs offers an Image ring and a PDF ring, and each action runs
    only on the files it fits. Crop is offered only for a single image.
    """
    menu: dict[str, list[Action]] = {}
    for a in ACTIONS:
        family_files = [p for p in paths if kind_of(p) in a.applies]
        count = len(family_files)
        if count < a.min_files:
            continue
        if a.id == "img_crop" and count != 1:
            continue
        menu.setdefault(a.category, []).append(a)
    return menu
