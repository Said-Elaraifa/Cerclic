"""Catalogue of actions and the rules that pick which ones a selection offers.

An Action is metadata plus a handler with a uniform signature:
    handler(paths: list[str], opts: dict, ctx) -> list[str]
returning the output paths. `needs` lists what the UI must gather first:
    "crop"       the crop popup (image or PDF)
    "place_sig"  the signature placement popup
    "pages"      the page organiser popup (PDF)
    "trim"       the cutting popup (video, sound)
    "social"     the social networks popup (format, background, framing)
    "compress"   the compression popup (how much, and the size it gives)
    "text"       a text typed in a bubble
    "new_password"  a password typed in a bubble
`choices` turns the action into a small ring of variants (rotate left/right...).
`ui` marks actions done by the app itself, without a file ("clipboard").
`desc` is the short line the wheel shows when the action is under the mouse.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Callable

from ..errors import LeftOut, NeedsPassword, NothingToDo, UserError
from ..i18n import N_, tr
from ..paths import kind_of, undone_on_error
from . import images, pdf, social, video
from .common import check, progress

# Category ids, French labels and ring colours. The texts of the actions
# and of their choices stay French here (N_): the places that show them
# translate them, tr(label).
CATEGORIES = {
    "image": (N_("Image"), "#2E7CF6"),
    "pdf": ("PDF", "#EF4E52"),
    "video": (N_("Vidéo"), "#10A37F"),
    "audio": (N_("Son"), "#8B5CF6"),
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
        """French, as the other texts here: tr(action.card_title) shows it."""
        return self.title or self.label


def each(paths, ctx, fn) -> list[str]:
    """Run fn on every file, with progress. In a batch, files that need nothing
    (already small...) are skipped; if all of them are, the reason is shown.
    A file that cannot be done (unreadable...) does not stop the others: the
    result card names it. A PDF that needs its password still stops the
    batch, so that it can be asked for."""
    outputs: list[str] = []
    skipped: NothingToDo | None = None
    failed: UserError | None = None
    n = len(paths)
    for i, p in enumerate(paths):
        check(ctx)
        if n > 1:
            progress(ctx, i / n, tr("Fichier {i} sur {n}", i=i + 1, n=n))
        try:
            with undone_on_error():
                out = fn(p)
        except NeedsPassword:
            raise
        except NothingToDo as exc:
            if n == 1:
                raise
            skipped = exc
            if isinstance(exc, LeftOut) and ctx is not None and hasattr(ctx, "note"):
                ctx.note(str(exc))          # said on the result card
            continue
        except UserError as exc:
            if n == 1:
                raise
            text = tr("« {name} » : {error}", name=os.path.basename(p), error=str(exc))
            failed = failed or UserError(text)
            if ctx is not None and hasattr(ctx, "note"):
                ctx.note(text)
            continue
        if isinstance(out, list):
            outputs.extend(out)
        elif out:
            outputs.append(out)
        if out and ctx is not None and hasattr(ctx, "sources"):
            ctx.sources.append(p)
    if not outputs and failed is not None:
        raise failed
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
    Choice("cw", N_("Droite"), "rotate_cw", (("degrees", 90),)),
    Choice("ccw", N_("Gauche"), "rotate_ccw", (("degrees", 270),)),
    Choice("180", "180°", "rotate_180", (("degrees", 180),)),
)
IMAGE_TURN_CHOICES = ROTATE_CHOICES + (
    Choice("mirror", N_("Miroir"), "mirror", (("mirror", True),)),
)


def _turn_image(p: str, o: dict) -> str:
    if o.get("mirror"):
        return images.mirror_image(p, _q(o))
    return images.rotate_image(p, int(o.get("degrees", 90)), _q(o))


def _framing(o: dict, path: str) -> tuple:
    """(centre, zoom) the user chose for this file in the social popup;
    centred and whole for the files of a batch they did not look at."""
    f = (o.get("social_frames") or {}).get(path)
    if f:
        return (float(f[0]), float(f[1])), float(f[2])
    return (0.5, 0.5), 1.0


def _precomputed(o: dict, path: str, run):
    """run(file already made by the « Compresser » popup for this path, or
    None); that file never stays behind in the temporary folder."""
    made = (o.get("precomputed") or {}).get(path)
    try:
        return run(made)
    finally:
        if made:
            try:
                if os.path.exists(made):
                    os.remove(made)
                os.rmdir(os.path.dirname(made))
            except OSError:
                pass


def _social_image(p: str, o: dict) -> str:
    return social.social_image(p, o["social"], o.get("social_mode", "fill"),
                               *_framing(o, p), quality=_q(o))


def _social_video(p: str, o: dict, ctx) -> str:
    return social.social_video(p, o["social"], o.get("social_mode", "blur"),
                               *_framing(o, p), ctx=ctx)


ACTIONS: list[Action] = [
    # ---- Images ----
    Action("img_crop", N_("Rogner"), "image", frozenset({"image"}),
           lambda paths, o, ctx: [images.crop_image(paths[0], o["crop_box"], _q(o))],
           icon="crop", needs=("crop",), max_files=1,
           desc=N_("Garder une partie"), title=N_("Rognage")),
    Action("img_social", N_("Réseaux"), "image", frozenset({"image"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: _social_image(p, o)),
           icon="social", needs=("social",), desc=N_("Insta, Story, mobile, PC"),
           title=N_("Format réseaux sociaux")),
    Action("img_rotate", N_("Pivoter"), "image", frozenset({"image"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: _turn_image(p, o)),
           icon="rotate", choices=IMAGE_TURN_CHOICES,
           desc=N_("Tourner ou retourner"), title=N_("Rotation")),
    Action("img_resize", N_("Redimensionner"), "image", frozenset({"image"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: images.resize_image(
               p, max_side=o.get("max_side"), percent=o.get("percent"), quality=_q(o))),
           icon="resize", desc=N_("Moins de pixels"), title=N_("Redimensionnement"),
           choices=(Choice("half", N_("50 %"), "half", (("percent", 50),)),
                    Choice("1920", "1920 px", "px", (("max_side", 1920),)),
                    Choice("1280", "1280 px", "px", (("max_side", 1280),)),
                    Choice("800", "800 px", "px", (("max_side", 800),)))),
    Action("img_compress", N_("Compresser"), "image", frozenset({"image"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: images.compress_image(
               p, int(o.get("quality", 70)))),
           icon="compress", needs=("compress",), desc=N_("Plus léger, même taille"),
           title=N_("Compression")),
    Action("img_convert", N_("Convertir"), "image", frozenset({"image"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: images.convert_image(
               p, o.get("fmt", "jpg"), _q(o))),
           icon="convert", desc=N_("Changer de format"), title=N_("Conversion"),
           choices=(Choice("jpg", "JPG", "jpg", (("fmt", "jpg"),)),
                    Choice("png", "PNG", "png", (("fmt", "png"),)),
                    Choice("webp", "WEBP", "webp", (("fmt", "webp"),)))),
    Action("img_to_pdf", N_("En PDF"), "image", frozenset({"image"}),
           lambda paths, o, ctx: [pdf.images_to_pdf(paths, ctx=ctx)],
           icon="cat_pdf", desc=N_("Une page par image"), title=N_("Création du PDF")),
    Action("img_copy", N_("Copier"), "image", frozenset({"image"}),
           lambda paths, o, ctx: [], icon="copy", max_files=1, ui="clipboard",
           desc=N_("À coller où tu veux"), title=N_("Copie")),
    Action("img_assemble", N_("Assembler"), "image", frozenset({"image"}),
           lambda paths, o, ctx: [images.assemble_images(
               paths, o.get("layout", "row"), _q(o), ctx=ctx)],
           icon="assemble", min_files=2, desc=N_("Plusieurs en une"), title=N_("Assemblage"),
           choices=(Choice("row", N_("Côte à côte"), "row", (("layout", "row"),)),
                    Choice("column", N_("En colonne"), "column", (("layout", "column"),)),
                    Choice("grid", N_("En grille"), "grid", (("layout", "grid"),)))),
    Action("img_clean", N_("Anonymiser"), "image", frozenset({"image"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: images.strip_metadata(
               p, _q(o))),
           icon="shield", primary=False, desc=N_("Retire GPS, appareil, date"),
           title=N_("Anonymisation")),

    # ---- PDF ----
    Action("pdf_sign", N_("Signer"), "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: [pdf.sign_pdf(paths[0], o["signature"],
                                               int(o.get("page", -1)), o.get("sig_box"),
                                               _pw(o, paths[0]))],
           icon="sign", needs=("place_sig",), max_files=1,
           desc=N_("Placer ta signature"), title=N_("Signature")),
    Action("pdf_crop", N_("Rogner"), "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: [pdf.crop_pdf(paths[0], o["crop_rel"],
                                               o.get("crop_page"), _pw(o, paths[0]))],
           icon="crop", needs=("crop",), max_files=1,
           desc=N_("Couper les marges"), title=N_("Rognage")),
    Action("pdf_compress", N_("Compresser"), "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: _precomputed(o, p, lambda pre:
               pdf.compress_pdf(p, _pw(o, p), ctx, o.get("level", "medium"), pre))),
           icon="compress", needs=("compress",), desc=N_("Plus léger à envoyer"),
           title=N_("Compression")),
    Action("pdf_merge", N_("Fusionner"), "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: [pdf.merge_pdfs(paths, {p: _pw(o, p) for p in paths},
                                                 ctx)],
           icon="merge", min_files=2, desc=N_("Un seul PDF"), title=N_("Fusion")),
    Action("pdf_pages", N_("Pages"), "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: [pdf.arrange_pdf(
               paths[0], o["pages_order"], _pw(o, paths[0]),
               tag="extract" if o.get("pages_mode") == "extract" else "organized")],
           icon="pages", needs=("pages",), max_files=1,
           desc=N_("Trier, tourner, supprimer"), title=N_("Organisation des pages")),
    Action("pdf_to_word", N_("En Word"), "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.pdf_to_word(
               p, _pw(o, p), ctx)),
           icon="word", desc=N_("Modifiable dans Word"), title=N_("Conversion en Word")),
    Action("pdf_to_images", N_("En images"), "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.pdf_to_images(
               p, o.get("fmt", "jpg"), password=_pw(o, p), ctx=ctx)),
           icon="image", desc=N_("Une image par page"), title=N_("Conversion en images"),
           choices=(Choice("jpg", "JPG", "jpg", (("fmt", "jpg"),)),
                    Choice("png", "PNG", "png", (("fmt", "png"),)))),
    Action("pdf_split", N_("Diviser"), "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.split_pdf(
               p, password=_pw(o, p), ctx=ctx)),
           icon="split", primary=False, desc=N_("Un PDF par page"), title=N_("Découpage en pages")),
    Action("pdf_rotate", N_("Pivoter"), "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.rotate_pdf(
               p, int(o.get("degrees", 90)), _pw(o, p))),
           icon="rotate", primary=False, choices=ROTATE_CHOICES,
           desc=N_("Toutes les pages"), title=N_("Rotation")),
    Action("pdf_watermark", N_("Filigrane"), "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.add_watermark(
               p, o["text"], _pw(o, p), ctx=ctx)),
           icon="watermark", needs=("text",), primary=False,
           desc=N_("Un texte en travers"), title=N_("Filigrane")),
    Action("pdf_numbers", N_("Numéroter"), "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.add_page_numbers(
               p, _pw(o, p), ctx=ctx)),
           icon="numbers", primary=False,
           desc=N_("Numéros en bas de page"), title=N_("Numérotation")),
    Action("pdf_text", N_("En texte"), "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.pdf_to_text(
               p, _pw(o, p), ctx=ctx)),
           icon="text", primary=False,
           desc=N_("Le texte en .txt"), title=N_("Extraction du texte")),
    Action("pdf_protect", N_("Protéger"), "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.protect_pdf(
               p, o["new_password"])),
           icon="lock", needs=("new_password",), primary=False,
           desc=N_("Avec un mot de passe"), title=N_("Protection")),
    Action("pdf_unlock", N_("Déverrouiller"), "pdf", frozenset({"pdf"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: pdf.unlock_pdf(
               p, _pw(o, p) or "")),
           icon="unlock", primary=False,
           desc=N_("Retirer le mot de passe"), title=N_("Déverrouillage")),

    # ---- Video ----
    Action("vid_trim", N_("Raccourcir"), "video", frozenset({"video"}),
           lambda paths, o, ctx: [video.trim_media(paths[0], o["trim_start"],
                                                   o["trim_end"], ctx=ctx)],
           icon="trim", needs=("trim",), max_files=1,
           desc=N_("Garder un passage"), title=N_("Découpe")),
    Action("vid_social", N_("Réseaux"), "video", frozenset({"video"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: _social_video(p, o, ctx)),
           icon="social", needs=("social",), desc=N_("Reels, TikTok, Shorts, PC"),
           title=N_("Format réseaux sociaux")),
    Action("vid_compress", N_("Compresser"), "video", frozenset({"video"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: _precomputed(o, p, lambda pre:
               video.compress_video(p, o.get("level", "medium"), ctx, pre))),
           icon="compress", needs=("compress",), desc=N_("Plus légère, en MP4"),
           title=N_("Compression")),
    Action("vid_mp4", N_("En MP4"), "video", frozenset({"video"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: video.to_mp4(p, ctx=ctx)),
           icon="mp4", desc=N_("Lisible partout"), title=N_("Conversion en MP4")),
    Action("vid_gif", N_("En GIF"), "video", frozenset({"video"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: video.to_gif(p, ctx=ctx)),
           icon="gif", desc=N_("Une animation sans son"), title=N_("Création du GIF")),
    Action("vid_mp3", N_("Extraire le son"), "video", frozenset({"video"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: video.extract_mp3(
               p, ctx=ctx)),
           icon="mp3", desc=N_("La bande son en MP3"), title=N_("Extraction du son")),
    Action("vid_mute", N_("Couper le son"), "video", frozenset({"video"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: video.mute_video(
               p, ctx=ctx)),
           icon="mute", desc=N_("La vidéo sans son"), title=N_("Suppression du son")),
    Action("vid_rotate", N_("Pivoter"), "video", frozenset({"video"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: video.rotate_video(
               p, int(o.get("degrees", 90)), ctx=ctx)),
           icon="rotate", choices=ROTATE_CHOICES,
           desc=N_("Remettre à l'endroit"), title=N_("Rotation")),

    # ---- Sound ----
    Action("aud_trim", N_("Raccourcir"), "audio", frozenset({"audio"}),
           lambda paths, o, ctx: [video.trim_media(paths[0], o["trim_start"],
                                                   o["trim_end"], ctx=ctx)],
           icon="trim", needs=("trim",), max_files=1,
           desc=N_("Garder un passage"), title=N_("Découpe")),
    Action("aud_mp3", N_("En MP3"), "audio", frozenset({"audio"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: video.audio_to_mp3(
               p, ctx=ctx)),
           icon="mp3", desc=N_("Lisible partout"), title=N_("Conversion en MP3")),
    Action("aud_compress", N_("Compresser"), "audio", frozenset({"audio"}),
           lambda paths, o, ctx: each(paths, ctx, lambda p: video.compress_audio(
               p, o.get("level", "strong"), ctx=ctx)),
           icon="compress", needs=("compress",), desc=N_("Plus léger, en MP3"),
           title=N_("Compression")),
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
