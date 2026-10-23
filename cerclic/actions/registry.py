"""Catalogue of actions and the rules that pick which ones a selection offers.

An Action is metadata plus a handler with a uniform signature:
    handler(paths: list[str], opts: dict, ctx) -> list[str]
returning the output paths. `needs` lists what the UI must gather first:
    "crop"       the crop popup (image or PDF)
    "place_sig"  the signature placement popup
    "pages"      the page organiser popup (PDF)
    "trim"       the cutting popup (video, sound)
    "text"       a text typed in a bubble
    "new_password"  a password typed in a bubble
`choices` turns the action into a small ring of variants (rotate left/right...).
`ui` marks actions done by the app itself, without a file ("clipboard").
`desc` is the short line the wheel shows when the action is under the mouse.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from ..errors import LeftOut, NothingToDo
from ..paths import kind_of
from . import images, pdf, video
from .common import check, progress

# Category ids, French labels and ring colours.
CATEGORIES = {
    "image": ("Image", "#4C8DFF"),
    "pdf": ("PDF", "#FF5A5F"),
    "video": ("Vidéo", "#17B890"),
    "audio": ("Son", "#A66BFF"),
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
    desc: str = ""              # one short line, shown in the wheel
    ui: str = ""                # done by the app itself ("clipboard")
    title: str = ""             # what the progress and result cards call it

    @property
    def card_title(self) -> str:
        return self.title or self.label


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
            if isinstance(exc, LeftOut) and ctx is not None and hasattr(ctx, "note"):
                ctx.note(str(exc))          # said on the result card
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


def _pw(opts, path=None):
    """The password to open this PDF: each protected file may have its own."""
    if path is not None:
        pw = (opts.get("passwords") or {}).get(path)
        if pw:
            return pw
    return opts.get("password") or None


ROTATE_CHOICES = (
    Choice("cw", "Droite", "rotate_cw", (("degrees", 90),)),
    Choice("ccw", "Gauche", "rotate_ccw", (("degrees", 270),)),
    Choice("180", "180°", "rotate_180", (("degrees", 180),)),
)
IMAGE_TURN_CHOICES = ROTATE_CHOICES + (
    Choice("mirror", "Miroir", "mirror", (("mirror", True),)),
)


def _turn_image(p: str, o: dict) -> str:
    if o.get("mirror"):
        return images.mirror_image(p, _q(o))
    return images.rotate_image(p, int(o.get("degrees", 90)), _q(o))


ACTIONS: list[Action] = [
    # ---- Images ----
    Action("img_crop", "Rogner", "image", frozenset({"image"}),
           lambda paths, o, ctx: [images.crop_image(paths[0], o["crop_box"], _q(o))],
           icon="crop", needs=("crop",), max_files=1, desc="Garder une partie", title="Rognage"),
    Action("img_rotate", "Pivoter", "image", frozenset({"image"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: _turn_image(p, o)),
           icon="rotate", choices=IMAGE_TURN_CHOICES, desc="Tourner ou retourner", title="Rotation"),
    Action("img_resize", "Redimensionner", "image", frozenset({"image"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: images.resize_image(
               p, max_side=o.get("max_side"), percent=o.get("percent"), quality=_q(o))),
           icon="resize", desc="Moins de pixels", title="Redimensionnement",
           choices=(Choice("half", "50 %", "half", (("percent", 50),)),
                    Choice("1920", "1920 px", "px", (("max_side", 1920),)),
                    Choice("1280", "1280 px", "px", (("max_side", 1280),)),
                    Choice("800", "800 px", "px", (("max_side", 800),)))),
    Action("img_compress", "Compresser", "image", frozenset({"image"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: images.compress_image(
               p, int(o.get("quality", 70)))),
           icon="compress", desc="Plus léger, même taille", title="Compression"),
    Action("img_convert", "Convertir", "image", frozenset({"image"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: images.convert_image(
               p, o.get("fmt", "jpg"), _q(o))),
           icon="convert", desc="Changer de format", title="Conversion",
           choices=(Choice("jpg", "JPG", "jpg", (("fmt", "jpg"),)),
                    Choice("png", "PNG", "png", (("fmt", "png"),)),
                    Choice("webp", "WEBP", "webp", (("fmt", "webp"),)))),
    Action("img_copy", "Copier", "image", frozenset({"image"}),
           lambda paths, o, ctx: [], icon="copy", max_files=1, ui="clipboard",
           desc="À coller où tu veux", title="Copie"),
    Action("img_to_pdf", "En PDF", "image", frozenset({"image"}),
           lambda paths, o, ctx: [pdf.images_to_pdf(paths, ctx=ctx)],
           icon="topdf", desc="Une page par image", title="Création du PDF"),
    Action("img_assemble", "Assembler", "image", frozenset({"image"}),
           lambda paths, o, ctx: [images.assemble_images(
               paths, o.get("layout", "row"), _q(o), ctx=ctx)],
           icon="assemble", min_files=2, desc="Plusieurs en une", title="Assemblage",
           choices=(Choice("row", "Côte à côte", "row", (("layout", "row"),)),
                    Choice("column", "En colonne", "column", (("layout", "column"),)),
                    Choice("grid", "En grille", "grid", (("layout", "grid"),)))),
    Action("img_clean", "Anonymiser", "image", frozenset({"image"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: images.strip_metadata(
               p, _q(o))),
           icon="shield", desc="Retire GPS, appareil, date", title="Anonymisation"),

    # ---- PDF ----
    Action("pdf_sign", "Signer", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: [pdf.sign_pdf(paths[0], o["signature"],
                                               int(o.get("page", -1)), o.get("sig_box"),
                                               _pw(o, paths[0]))],
           icon="sign", needs=("place_sig",), max_files=1, desc="Placer ta signature", title="Signature"),
    Action("pdf_crop", "Rogner", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: [pdf.crop_pdf(paths[0], o["crop_rel"],
                                               o.get("crop_page"), _pw(o, paths[0]))],
           icon="crop", needs=("crop",), max_files=1, desc="Couper les marges", title="Rognage"),
    Action("pdf_compress", "Compresser", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.compress_pdf(
               p, _pw(o, p), ctx)),
           icon="compress", desc="Plus léger à envoyer", title="Compression"),
    Action("pdf_merge", "Fusionner", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: [pdf.merge_pdfs(paths, {p: _pw(o, p) for p in paths},
                                                 ctx)],
           icon="merge", min_files=2, desc="Un seul PDF", title="Fusion"),
    Action("pdf_pages", "Pages", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: [pdf.arrange_pdf(
               paths[0], o["pages_order"], _pw(o, paths[0]),
               tag="extract" if o.get("pages_mode") == "extract" else "organized")],
           icon="pages", needs=("pages",), max_files=1,
           desc="Trier, tourner, supprimer", title="Organisation des pages"),
    Action("pdf_to_word", "En Word", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.pdf_to_word(
               p, _pw(o, p), ctx)),
           icon="word", desc="Modifiable dans Word", title="Conversion en Word"),
    Action("pdf_to_images", "En images", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.pdf_to_images(
               p, o.get("fmt", "jpg"), password=_pw(o, p), ctx=ctx)),
           icon="image", desc="Une image par page", title="Conversion en images",
           choices=(Choice("jpg", "JPG", "jpg", (("fmt", "jpg"),)),
                    Choice("png", "PNG", "png", (("fmt", "png"),)))),
    Action("pdf_split", "Diviser", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.split_pdf(
               p, password=_pw(o, p), ctx=ctx)),
           icon="split", primary=False, desc="Un PDF par page", title="Découpage en pages"),
    Action("pdf_rotate", "Pivoter", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.rotate_pdf(
               p, int(o.get("degrees", 90)), _pw(o, p))),
           icon="rotate", primary=False, choices=ROTATE_CHOICES,
           desc="Toutes les pages", title="Rotation"),
    Action("pdf_watermark", "Filigrane", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.add_watermark(
               p, o["text"], _pw(o, p), ctx=ctx)),
           icon="watermark", needs=("text",), primary=False,
           desc="Un texte en travers", title="Filigrane"),
    Action("pdf_numbers", "Numéroter", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.add_page_numbers(
               p, _pw(o, p), ctx=ctx)),
           icon="numbers", primary=False, desc="Numéros en bas de page", title="Numérotation"),
    Action("pdf_text", "En texte", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.pdf_to_text(
               p, _pw(o, p), ctx=ctx)),
           icon="text", primary=False, desc="Le texte en .txt", title="Extraction du texte"),
    Action("pdf_protect", "Protéger", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.protect_pdf(
               p, o["new_password"])),
           icon="lock", needs=("new_password",), primary=False,
           desc="Avec un mot de passe", title="Protection"),
    Action("pdf_unlock", "Déverrouiller", "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.unlock_pdf(
               p, _pw(o, p) or "")),
           icon="unlock", primary=False, desc="Retirer le mot de passe", title="Déverrouillage"),

    # ---- Video ----
    Action("vid_trim", "Raccourcir", "video", frozenset({"video"}),
           lambda paths, o, ctx: [video.trim_media(paths[0], o["trim_start"],
                                                   o["trim_end"], ctx=ctx)],
           icon="trim", needs=("trim",), max_files=1, desc="Garder un passage", title="Découpe"),
    Action("vid_compress", "Compresser", "video", frozenset({"video"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: video.compress_video(
               p, ctx=ctx)),
           icon="compress", desc="Plus légère, en MP4", title="Compression"),
    Action("vid_mp4", "En MP4", "video", frozenset({"video"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: video.to_mp4(p, ctx=ctx)),
           icon="mp4", desc="Lisible partout", title="Conversion en MP4"),
    Action("vid_gif", "En GIF", "video", frozenset({"video"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: video.to_gif(p, ctx=ctx)),
           icon="gif", desc="Une animation sans son", title="Création du GIF"),
    Action("vid_mp3", "Extraire le son", "video", frozenset({"video"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: video.extract_mp3(
               p, ctx=ctx)),
           icon="mp3", desc="La bande son en MP3", title="Extraction du son"),
    Action("vid_mute", "Couper le son", "video", frozenset({"video"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: video.mute_video(
               p, ctx=ctx)),
           icon="mute", desc="La vidéo sans son", title="Suppression du son"),
    Action("vid_rotate", "Pivoter", "video", frozenset({"video"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: video.rotate_video(
               p, int(o.get("degrees", 90)), ctx=ctx)),
           icon="rotate", choices=ROTATE_CHOICES, desc="Remettre à l'endroit", title="Rotation"),

    # ---- Sound ----
    Action("aud_trim", "Raccourcir", "audio", frozenset({"audio"}),
           lambda paths, o, ctx: [video.trim_media(paths[0], o["trim_start"],
                                                   o["trim_end"], ctx=ctx)],
           icon="trim", needs=("trim",), max_files=1, desc="Garder un passage", title="Découpe"),
    Action("aud_mp3", "En MP3", "audio", frozenset({"audio"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: video.audio_to_mp3(
               p, ctx=ctx)),
           icon="mp3", desc="Lisible partout", title="Conversion en MP3"),
    Action("aud_compress", "Compresser", "audio", frozenset({"audio"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: video.compress_audio(
               p, ctx=ctx)),
           icon="compress", desc="Plus léger, en MP3", title="Compression"),
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
