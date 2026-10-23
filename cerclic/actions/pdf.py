"""PDF actions.

PyMuPDF (imported as pymupdf) does rendering and page work, pikepdf handles
encryption, pdf2docx does PDF to Word. Each function returns the path(s) it
wrote, always beside the source.

Coordinates: the editors work in what the reader *sees* (the page after its
rotation and crop box are applied), as fractions of the visible page. The
helpers below translate that into the coordinates PyMuPDF expects, which is
verified by tests on rotated and cropped pages.
"""
from __future__ import annotations

import io
import math
import os
import re
from typing import Sequence

import pymupdf

from ..errors import Cancelled, NeedsPassword, NothingToDo, UserError
from ..paths import output_dir_for, output_for
from .common import check, progress

for _quiet in ("mupdf_display_errors", "mupdf_display_warnings"):
    try:  # keep MuPDF from printing to a console the app does not have
        getattr(pymupdf.TOOLS, _quiet)(False)
    except Exception:
        pass

A4_LONG_SIDE = 842.0  # points


# ----- opening ---------------------------------------------------------------

def open_pdf(src: str, password: str | None = None) -> pymupdf.Document:
    """Open a PDF, unlocking it with `password` if it is protected."""
    try:
        doc = pymupdf.open(src)
    except Exception:
        raise UserError(f"PDF endommagé ou illisible : {os.path.basename(src)}")
    if not doc.is_pdf:
        doc.close()
        raise UserError(f"Ce fichier n'est pas un PDF : {os.path.basename(src)}")
    if doc.needs_pass:
        if not password or not doc.authenticate(password):
            doc.close()
            msg = ("Mot de passe incorrect." if password
                   else f"« {os.path.basename(src)} » est protégé par un mot de passe.")
            raise NeedsPassword(msg, path=src)
    return doc


def needs_password(src: str) -> bool:
    try:
        with pymupdf.open(src) as doc:
            return bool(doc.needs_pass)
    except Exception:
        return False


def password_ok(src: str, password: str) -> bool:
    """True if `password` opens this PDF (or if it needs none)."""
    try:
        with pymupdf.open(src) as doc:
            return not doc.needs_pass or bool(doc.authenticate(password or ""))
    except Exception:
        return False


def is_encrypted(src: str) -> bool:
    """True if the PDF has any encryption (password or restrictions)."""
    try:
        with pymupdf.open(src) as doc:
            return bool(doc.needs_pass or (doc.metadata or {}).get("encryption"))
    except Exception:
        return False


def _save(doc: pymupdf.Document, out: str, **kw) -> None:
    """Save, keeping the original protection if the document had one."""
    if (doc.metadata or {}).get("encryption"):
        kw.setdefault("encryption", pymupdf.PDF_ENCRYPT_KEEP)
    kw.setdefault("garbage", 3)
    kw.setdefault("deflate", True)
    doc.save(out, **kw)


def pdf_page_count(src: str, password: str | None = None) -> int:
    with open_pdf(src, password) as doc:
        return doc.page_count


# ----- coordinates -------------------------------------------------------------

def _visible_to_insert(page: pymupdf.Page, pt) -> pymupdf.Point:
    """A point as the reader sees it -> PyMuPDF insertion coordinates."""
    uv = pymupdf.Point(pt) * page.derotation_matrix      # unrotated, crop-box relative
    cb = page.cropbox                                     # unrotated, top-left based
    # PDF user space: x as is, y flipped against the top of the media box
    # (which is not 0 when the media box does not start at the origin).
    pdf_pt = pymupdf.Point(cb.x0 + uv.x, (page.mediabox.y1 - cb.y0) - uv.y)
    return pdf_pt * page.transformation_matrix


def visible_rect_to_insert(page: pymupdf.Page, r) -> pymupdf.Rect:
    r = pymupdf.Rect(r)
    return pymupdf.Rect(_visible_to_insert(page, r.tl),
                        _visible_to_insert(page, r.br)).normalize()


def _rel_to_visible(page: pymupdf.Page, rel: Sequence[float]) -> pymupdf.Rect:
    W, H = page.rect.width, page.rect.height
    x0, y0, x1, y1 = (max(0.0, min(1.0, float(v))) for v in rel)
    return pymupdf.Rect(min(x0, x1) * W, min(y0, y1) * H,
                        max(x0, x1) * W, max(y0, y1) * H)


def _stamp(page: pymupdf.Page, draw) -> None:
    """Draw on a blank page the size of what the reader sees, then lay it on top
    of `page`. Works the same whatever the page rotation and crop box."""
    W, H = page.rect.width, page.rect.height
    overlay = pymupdf.open()
    try:
        op = overlay.new_page(width=W, height=H)
        draw(op, W, H)
        page.show_pdf_page(visible_rect_to_insert(page, page.rect), overlay, 0,
                           rotate=page.rotation, keep_proportion=False, overlay=True)
    finally:
        overlay.close()


# ----- rendering (used by the editors) ----------------------------------------

def render_page(src: str, index: int, max_w: int, max_h: int,
                password: str | None = None):
    """Render one page to fit max_w x max_h pixels.

    `index` past the end means the last page. Returns
    (rgb_bytes, width, height, stride, page_count, (page_w_pt, page_h_pt), index)."""
    with open_pdf(src, password) as doc:
        index = max(0, min(index, doc.page_count - 1))
        page = doc[index]
        W, H = page.rect.width, page.rect.height
        zoom = max(0.05, min(max_w / W, max_h / H))
        pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False)
        return (bytes(pix.samples), pix.width, pix.height, pix.stride,
                doc.page_count, (W, H), index)


# ----- raster <-> pdf ----------------------------------------------------------

def pdf_to_images(src: str, fmt: str = "jpg", dpi: int = 150,
                  password: str | None = None, ctx=None) -> list[str]:
    """One image per page, written into a new folder '<name> (images)'."""
    from PIL import Image
    fmt = "jpg" if fmt.lower() in ("jpg", "jpeg") else "png"
    stem = os.path.splitext(os.path.basename(src))[0]
    with open_pdf(src, password) as doc:
        out_dir = output_dir_for(src, "images")
        n = doc.page_count
        pad = max(2, len(str(n)))
        written: list[str] = []
        for i, page in enumerate(doc, start=1):
            check(ctx)
            progress(ctx, (i - 1) / n, f"Page {i} sur {n}")
            pix = page.get_pixmap(dpi=dpi, alpha=False)
            im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            path = os.path.join(out_dir, f"{stem}-{str(i).zfill(pad)}.{fmt}")
            if fmt == "jpg":
                im.save(path, "JPEG", quality=90, optimize=True)
            else:
                im.save(path, "PNG", compress_level=6)
            written.append(path)
    return written


def images_to_pdf(srcs: Sequence[str], ctx=None) -> str:
    """Combine images (in the given order) into one PDF beside the first image.
    Each page keeps the image proportions, sized like an A4 sheet."""
    from .images import load, _flatten
    srcs = list(srcs)
    if not srcs:
        raise UserError("Aucune image.")
    out = output_for(srcs[0], "pdf", new_ext=".pdf")
    doc = pymupdf.open()
    try:
        for i, src in enumerate(srcs):
            check(ctx)
            progress(ctx, i / len(srcs), f"Image {i + 1} sur {len(srcs)}")
            pic = load(src)
            im = pic.frames[0]
            buf = io.BytesIO()
            if pic.has_alpha:
                im.convert("RGBA").save(buf, "PNG")
            else:
                _flatten(im).convert("RGB").save(buf, "JPEG", quality=90)
            w, h = im.size
            scale = A4_LONG_SIDE / max(w, h)
            page = doc.new_page(width=w * scale, height=h * scale)
            page.insert_image(page.rect, stream=buf.getvalue())
        _save(doc, out, garbage=3, deflate=True)
    finally:
        doc.close()
    return out


# ----- combine / divide ---------------------------------------------------------

def merge_pdfs(srcs: Sequence[str], password: str | None = None, ctx=None) -> str:
    srcs = list(srcs)
    if len(srcs) < 2:
        raise UserError("Il faut au moins deux PDF pour fusionner.")
    out = output_for(srcs[0], "merged", new_ext=".pdf")
    doc = pymupdf.open()
    try:
        for i, p in enumerate(srcs):
            check(ctx)
            progress(ctx, i / len(srcs), f"PDF {i + 1} sur {len(srcs)}")
            with open_pdf(p, password) as part:
                doc.insert_pdf(part)
        doc.save(out, garbage=3, deflate=True)
    finally:
        doc.close()
    return out


def split_pdf(src: str, every: int = 1, password: str | None = None,
              ctx=None) -> list[str]:
    """Split into files of `every` pages (one file per page by default)."""
    stem = os.path.splitext(os.path.basename(src))[0]
    with open_pdf(src, password) as doc:
        n = doc.page_count
        if n < 2:
            raise NothingToDo("Ce PDF n'a qu'une page.")
        out_dir = output_dir_for(src, "pages")
        pad = max(2, len(str(n)))
        written: list[str] = []
        start = 0
        while start < n:
            check(ctx)
            progress(ctx, start / n, f"Page {start + 1} sur {n}")
            end = min(start + every, n)
            part = pymupdf.open()
            part.insert_pdf(doc, from_page=start, to_page=end - 1)
            label = (str(start + 1).zfill(pad) if every == 1
                     else f"{str(start + 1).zfill(pad)}-{str(end).zfill(pad)}")
            path = os.path.join(out_dir, f"{stem}-{label}.pdf")
            part.save(path, garbage=3, deflate=True)
            part.close()
            written.append(path)
            start = end
    return written


# ----- pages: reorder, rotate, remove, extract -------------------------------------

def arrange_pdf(src: str, order: Sequence, password: str | None = None,
                tag: str = "organized") -> str:
    """New PDF made of the pages listed in `order`, in that order: each item is
    a page index, or (page index, extra clockwise rotation in degrees).
    Pages left out are removed; links and bookmarks to them go away."""
    items = []
    for it in order:
        idx, rot = (it, 0) if isinstance(it, int) else (int(it[0]), int(it[1]))
        items.append((idx, rot % 360))
    if not items:
        raise UserError("Aucune page à garder.")
    with open_pdf(src, password) as doc:
        n = doc.page_count
        if any(not 0 <= idx < n for idx, _ in items):
            raise UserError("Page introuvable dans ce PDF.")
        if [idx for idx, _ in items] == list(range(n)) and not any(r for _, r in items):
            raise NothingToDo("Les pages n'ont pas changé.")
        out = output_for(src, tag, new_ext=".pdf")
        doc.select([idx for idx, _ in items])
        for page, (_, rot) in zip(doc, items):
            if rot:
                page.set_rotation((page.rotation + rot) % 360)
        _save(doc, out, garbage=3, deflate=True)
    return out


def pdf_to_text(src: str, password: str | None = None, ctx=None) -> str:
    """The text of the PDF in a .txt file (opens in Notepad, accents included)."""
    with open_pdf(src, password) as doc:
        n = doc.page_count
        pages = []
        for i, page in enumerate(doc):
            check(ctx)
            progress(ctx, i / max(1, n), f"Page {i + 1} sur {n}")
            pages.append(page.get_text("text").strip())     # reading order
    if not any(pages):
        raise NothingToDo("Aucun texte dans ce PDF : c'est sûrement un scan (une image).")
    out = output_for(src, "text", new_ext=".txt")
    text = "\n\n".join(p for p in pages)
    with open(out, "w", encoding="utf-8-sig", newline="\r\n") as f:
        f.write(text + "\n")
    return out


def render_thumbs(src: str, height: int, password: str | None = None, report=None,
                  should_stop=None) -> int:
    """Render every page `height` px high, one after the other; report(index,
    (rgb, w, h, stride)) for each. Returns the page count."""
    with open_pdf(src, password) as doc:
        n = doc.page_count
        for i, page in enumerate(doc):
            if should_stop is not None and should_stop():
                break
            zoom = max(0.02, height / max(1.0, page.rect.height))
            pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False)
            if report is not None:
                report(i, (bytes(pix.samples), pix.width, pix.height, pix.stride))
        return n


# ----- shrink / rotate / crop ---------------------------------------------------

_PRINT_COLOURS = ("CMYK", "DeviceN", "Separation", "/Lab", "ICC N 4")


def _resolve(doc: pymupdf.Document, text: str, depth: int = 0) -> str:
    """Inline the indirect references (N 0 R) of a PDF object, a few levels
    deep; colour profile streams become 'ICC N <components>'."""
    if depth > 6:
        return text

    def inline(m):
        x = int(m.group(1))
        try:
            if doc.xref_is_stream(x):
                return f"<<ICC N {doc.xref_get_key(x, 'N')[1].strip()}>>"
            return _resolve(doc, doc.xref_object(x, compressed=True), depth + 1)
        except Exception:
            return "<<?>>"

    return re.sub(r"(\d+)\s+0\s+R", inline, text)


def _image_is_delicate(doc: pymupdf.Document, xref: int) -> bool:
    """Images whose colours a rewrite could change: print colours (CMYK, spot
    colours, Lab, including inside an indexed palette), inverted /Decode, /Mask."""
    try:
        if doc.xref_get_key(xref, "Decode")[0] != "null":
            return True
        if doc.xref_get_key(xref, "Mask")[0] != "null":
            return True
        cs = _resolve(doc, doc.xref_get_key(xref, "ColorSpace")[1])
        return any(k in cs for k in _PRINT_COLOURS) or "<<?>>" in cs
    except Exception:
        return True


def _delicate_images(doc: pymupdf.Document) -> set[int]:
    out: set[int] = set()
    seen: set[int] = set()
    for pno in range(doc.page_count):
        for img in doc.get_page_images(pno, full=True):
            xref = img[0]
            if xref not in seen:
                seen.add(xref)
                if _image_is_delicate(doc, xref):
                    out.add(xref)
    return out


def _plain_image(doc: pymupdf.Document, img) -> bool:
    """8-bit RGB or grey image whose colours survive a JPEG re-encode as is:
    DeviceRGB, DeviceGray or an sRGB profile. (1-bit scans and stencil masks,
    other profiles, palettes... are left to MuPDF, which keeps them right.)"""
    xref, bpc, cs = img[0], img[4], img[5]
    if bpc != 8:
        return False
    if cs in ("DeviceRGB", "DeviceGray"):
        return True
    if cs != "ICCBased":
        return False
    try:
        kind, val = doc.xref_get_key(xref, "ColorSpace")
        if kind == "xref":
            val = doc.xref_object(int(val.split()[0]), compressed=True)
        m = re.search(r"/ICCBased\s*(\d+)\s+0\s+R", val)
        if not m:
            return False
        prof = (doc.xref_stream(int(m.group(1))) or b"")[:8192]
        return prof[16:20] == b"RGB " and (b"sRGB" in prof
                                          or "sRGB".encode("utf-16-be") in prof)
    except Exception:
        return False


def _downsample_images(doc: pymupdf.Document, skip: set[int], dpi_threshold: int = 180,
                       dpi_target: int = 150, quality: int = 72, ctx=None) -> int:
    """Bring the plain colour or grey images shown above dpi_threshold down to
    dpi_target, one by one, leaving `skip` (delicate images) untouched.
    Returns how many were replaced."""
    import io as _io
    from PIL import Image
    shown: dict[int, float] = {}     # largest displayed size, in points
    for page in doc:
        for img in page.get_images(full=True):
            try:
                for r in page.get_image_rects(img[0]):
                    shown[img[0]] = max(shown.get(img[0], 0.0), r.width, r.height)
            except Exception:
                continue
    changed, done = 0, set()
    total = max(1, len(shown))
    for page in doc:
        for img in page.get_images(full=True):
            xref, smask, w, h = img[0], img[1], img[2], img[3]
            if xref in done or xref in skip or smask:
                continue
            done.add(xref)
            check(ctx)
            if not _plain_image(doc, img):
                continue
            progress(ctx, min(1.0, len(done) / total), "Compression des images")
            size_pt = shown.get(xref, 0.0)
            if size_pt <= 0:
                continue
            dpi = max(w, h) / (size_pt / 72.0)
            if dpi <= dpi_threshold:
                continue
            try:
                pix = pymupdf.Pixmap(doc, xref)
                if pix.alpha or pix.n not in (1, 3):
                    continue
                im = Image.frombytes("L" if pix.n == 1 else "RGB",
                                     (pix.width, pix.height), pix.samples)
                k = dpi_target / dpi
                im = im.resize((max(1, round(pix.width * k)), max(1, round(pix.height * k))),
                               Image.Resampling.LANCZOS)
                buf = _io.BytesIO()
                im.save(buf, "JPEG", quality=quality, optimize=True)
                if len(buf.getvalue()) >= len(doc.xref_stream_raw(xref) or b""):
                    continue
                page.replace_image(xref, stream=buf.getvalue())
                changed += 1
            except Exception:
                continue
    return changed


def _looks_the_same(a: str, b: str, password: str | None, max_pages: int = 40) -> bool:
    """Compare small renders of both files, area by area: a re-encoded image may
    differ a little, never a lot (inverted or scrambled colours), however small."""
    from PIL import Image, ImageChops
    with open_pdf(a, password) as da, open_pdf(b, password) as db:
        if da.page_count != db.page_count:
            return False
        n = da.page_count
        step = max(1, n // max_pages)
        for i in range(0, n, step):
            pa = da[i].get_pixmap(dpi=40, alpha=False)
            pb = db[i].get_pixmap(dpi=40, alpha=False)
            if (pa.width, pa.height) != (pb.width, pb.height):
                return False
            ia = Image.frombytes("RGB", (pa.width, pa.height), pa.samples)
            ib = Image.frombytes("RGB", (pb.width, pb.height), pb.samples)
            diff = ImageChops.difference(ia, ib).convert("L")
            cells = diff.resize((max(1, diff.width // 10), max(1, diff.height // 10)),
                                Image.Resampling.BOX)
            if cells.getextrema()[1] > 24:
                return False
    return True


def compress_pdf(src: str, password: str | None = None, ctx=None) -> str:
    """Downsample and re-encode heavy images, then rewrite the file compactly.
    Text stays sharp and selectable. Delicate images (print colours...) are
    kept as they are, and the result is compared with the original."""
    out = output_for(src, "compressed", new_ext=".pdf")
    save_opts = dict(garbage=4, deflate=True, deflate_images=True, deflate_fonts=True,
                     clean=True, use_objstms=1)
    touched = False
    with open_pdf(src, password) as doc:
        progress(ctx, None, "Compression des images")
        delicate = _delicate_images(doc)
        try:
            # Plain photos and scans go to exactly 150 dpi (MuPDF alone only
            # halves or quarters them: a 290 dpi photo would stay at 290 dpi)...
            touched = _downsample_images(doc, delicate, ctx=ctx) > 0
            if not delicate:
                # ...then MuPDF re-encodes everything else (masks, palettes...).
                progress(ctx, None, "Compression des images")
                doc.rewrite_images(dpi_threshold=180, dpi_target=150, quality=72)
                touched = True
        except Cancelled:
            raise
        except Exception:
            touched = False
        check(ctx)
        if touched:
            _save(doc, out, **save_opts)
    if touched:
        progress(ctx, None, "Vérification")
        if not _looks_the_same(src, out, password):
            touched = False      # keep every image as it was
    if not touched:
        with open_pdf(src, password) as doc:
            _save(doc, out, **save_opts)
    check(ctx)
    if os.path.getsize(out) >= os.path.getsize(src) * 0.98:
        os.remove(out)
        raise NothingToDo("Ce PDF est déjà bien compressé.")
    return out


def rotate_pdf(src: str, degrees: int = 90, password: str | None = None) -> str:
    """Rotate every page clockwise by 90, 180 or 270 degrees."""
    out = output_for(src, "rotated", new_ext=".pdf")
    with open_pdf(src, password) as doc:
        for page in doc:
            page.set_rotation((page.rotation + int(degrees)) % 360)
        _save(doc, out)
    return out


def crop_pdf(src: str, rel_box: Sequence[float], page_index: int | None = None,
             password: str | None = None) -> str:
    """Crop to rel_box = (x0, y0, x1, y1), fractions of the visible page.
    Applies to every page, or only to `page_index` when given."""
    x0, y0, x1, y1 = (float(v) for v in rel_box)
    if x1 - x0 < 0.005 or y1 - y0 < 0.005:
        raise UserError("La zone à rogner est vide.")
    if x0 <= 0.001 and y0 <= 0.001 and x1 >= 0.999 and y1 >= 0.999:
        raise NothingToDo("Le cadre couvre toute la page : rien à rogner.")
    out = output_for(src, "cropped", new_ext=".pdf")
    with open_pdf(src, password) as doc:
        for i, page in enumerate(doc):
            if page_index is not None and i != page_index:
                continue
            visible = _rel_to_visible(page, rel_box)
            rel = (visible * page.derotation_matrix).normalize()
            cp = page.cropbox_position
            target = pymupdf.Rect(rel.x0 + cp.x, rel.y0 + cp.y,
                                  rel.x1 + cp.x, rel.y1 + cp.y)
            mb = page.mediabox     # same top-left based frame as cropbox_position
            target = target & pymupdf.Rect(mb.x0, 0, mb.x1, mb.height)
            if target.is_empty:
                continue
            page.set_cropbox(target)
        _save(doc, out)
    return out


# ----- convert to office --------------------------------------------------------

def pdf_to_word(src: str, password: str | None = None, ctx=None) -> str:
    from pdf2docx import Converter
    with open_pdf(src, password):
        pass  # fails early with a clear message if locked or damaged
    out = output_for(src, "word", new_ext=".docx")
    progress(ctx, None, "Conversion en Word")
    cv = Converter(src, password=password) if password else Converter(src)
    try:
        cv.convert(out)
    finally:
        cv.close()
    return out


# ----- stamps: watermark, page numbers, signature -------------------------------

def add_watermark(src: str, text: str, password: str | None = None,
                  opacity: float = 0.14, ctx=None) -> str:
    text = (text or "").strip()
    if not text:
        raise UserError("Le texte du filigrane est vide.")
    font = pymupdf.Font("helv")
    out = output_for(src, "watermark", new_ext=".pdf")

    def draw(op, W, H):
        diag = math.hypot(W, H)
        length = font.text_length(text, fontsize=1) or 1
        size = max(10.0, min(0.62 * diag / length, H / 5))
        angle = math.degrees(math.atan2(H, W))
        width = font.text_length(text, fontsize=size)
        center = pymupdf.Point(W / 2, H / 2)
        start = pymupdf.Point(center.x - width / 2, center.y + size * 0.35)
        tw = pymupdf.TextWriter(op.rect, color=(0.45, 0.45, 0.45))
        tw.append(start, text, font=font, fontsize=size)
        tw.write_text(op, opacity=opacity, morph=(center, pymupdf.Matrix(angle)))

    with open_pdf(src, password) as doc:
        n = doc.page_count
        for i, page in enumerate(doc):
            check(ctx)
            progress(ctx, i / n, f"Page {i + 1} sur {n}")
            _stamp(page, draw)
        _save(doc, out)
    return out


def add_page_numbers(src: str, password: str | None = None, size: float = 10,
                     ctx=None) -> str:
    font = pymupdf.Font("helv")
    out = output_for(src, "numbered", new_ext=".pdf")
    with open_pdf(src, password) as doc:
        total = doc.page_count
        for i, page in enumerate(doc):
            check(ctx)
            progress(ctx, i / total, f"Page {i + 1} sur {total}")
            label = f"{i + 1} / {total}"

            def draw(op, W, H, label=label):
                width = font.text_length(label, fontsize=size)
                op.insert_text(pymupdf.Point((W - width) / 2, H - 22), label,
                               fontsize=size, fontname="helv", color=(0.25, 0.25, 0.25))

            _stamp(page, draw)
        _save(doc, out)
    return out


def default_signature_box(page_w: float, page_h: float, sig_w: int, sig_h: int,
                          width_ratio: float = 0.28) -> tuple[float, float, float, float]:
    """Where a signature goes by default: bottom right, as fractions of the page."""
    w = width_ratio
    h = w * (sig_h / max(1, sig_w)) * (page_w / page_h)
    x0, y0 = 1 - 0.08 - w, 1 - 0.09 - h
    return (x0, max(0.02, y0), x0 + w, max(0.02, y0) + h)


def sign_pdf(src: str, signature_png: str, page_index: int = -1,
             rel_box: Sequence[float] | None = None,
             password: str | None = None) -> str:
    """Place the signature image on one page (last page by default).
    rel_box = (x0, y0, x1, y1), fractions of the visible page."""
    if not signature_png or not os.path.exists(signature_png):
        raise UserError("Aucune signature enregistrée.")
    from PIL import Image
    with Image.open(signature_png) as sig:
        sw, sh = sig.size
        buf = io.BytesIO()
        sig.convert("RGBA").save(buf, "PNG")
    data = buf.getvalue()
    out = output_for(src, "signed", new_ext=".pdf")
    with open_pdf(src, password) as doc:
        idx = page_index if page_index >= 0 else doc.page_count - 1
        idx = max(0, min(idx, doc.page_count - 1))
        page = doc[idx]
        if rel_box is None:
            rel_box = default_signature_box(page.rect.width, page.rect.height, sw, sh)
        visible = _rel_to_visible(page, rel_box)
        page.insert_image(visible_rect_to_insert(page, visible), stream=data,
                          rotate=page.rotation, keep_proportion=True)
        _save(doc, out)
    return out


# ----- protect / unlock ---------------------------------------------------------

def protect_pdf(src: str, password: str) -> str:
    import pikepdf
    if not password:
        raise UserError("Le mot de passe est vide.")
    if needs_password(src):
        raise UserError("Ce PDF est déjà protégé par un mot de passe.")
    out = output_for(src, "protected", new_ext=".pdf")
    with pikepdf.open(src) as pdf:
        pdf.save(out, encryption=pikepdf.Encryption(owner=password, user=password, R=6))
    return out


def unlock_pdf(src: str, password: str = "") -> str:
    import pikepdf
    if not is_encrypted(src):
        raise NothingToDo("Ce PDF n'est pas protégé.")
    try:
        pdf = pikepdf.open(src, password=password or "")
    except pikepdf.PasswordError:
        raise NeedsPassword("Mot de passe incorrect." if password else
                            f"« {os.path.basename(src)} » est protégé par un mot de passe.",
                            path=src)
    out = output_for(src, "unlocked", new_ext=".pdf")
    with pdf:
        pdf.save(out)
    return out
