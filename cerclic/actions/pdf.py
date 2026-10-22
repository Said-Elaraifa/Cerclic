"""PDF actions.

PyMuPDF (imported as pymupdf) does the rendering and page work, pikepdf handles
encryption and lossless structure edits, pdf2docx handles PDF to Word. Each
function returns the path(s) it wrote, always beside the source.
"""
from __future__ import annotations

import os
from typing import Sequence

import pymupdf

from ..paths import output_for, sibling_path, unique_path


# ----- raster <-> pdf -------------------------------------------------------

def pdf_to_images(src: str, fmt: str = "jpg", dpi: int = 150) -> list[str]:
    """One image per page, written into a sibling folder '<name> (images)'."""
    fmt = "jpg" if fmt.lower() in ("jpg", "jpeg") else fmt.lower()
    folder = os.path.dirname(os.path.abspath(src))
    stem = os.path.splitext(os.path.basename(src))[0]
    out_dir = unique_path(folder, stem, "", tag="images")
    os.makedirs(out_dir, exist_ok=True)
    written: list[str] = []
    with pymupdf.open(src) as doc:
        pad = len(str(doc.page_count))
        for i, page in enumerate(doc, start=1):
            pix = page.get_pixmap(dpi=dpi)
            name = f"{stem}-{str(i).zfill(pad)}.{ 'jpg' if fmt=='jpg' else fmt}"
            path = os.path.join(out_dir, name)
            if fmt == "jpg":
                pix.pil_save(path, format="JPEG", quality=90)
            else:
                pix.save(path)
            written.append(path)
    return written


def images_to_pdf(srcs: Sequence[str]) -> str:
    """Combine images (in the given order) into one PDF beside the first image."""
    srcs = list(srcs)
    if not srcs:
        raise ValueError("no images given")
    out = output_for(srcs[0], "pdf", new_ext=".pdf")
    doc = pymupdf.open()
    try:
        for img in srcs:
            imgdoc = pymupdf.open(img)
            rect = imgdoc[0].rect
            pdfbytes = imgdoc.convert_to_pdf()
            imgdoc.close()
            page = doc.new_page(width=rect.width, height=rect.height)
            page.show_pdf_page(rect, pymupdf.open("pdf", pdfbytes), 0)
        doc.save(out)
    finally:
        doc.close()
    return out


# ----- combine / divide -----------------------------------------------------

def merge_pdfs(srcs: Sequence[str]) -> str:
    srcs = list(srcs)
    if len(srcs) < 2:
        raise ValueError("need at least two PDFs to merge")
    out = sibling_path(srcs[0], "merged.pdf")
    doc = pymupdf.open()
    try:
        for p in srcs:
            with pymupdf.open(p) as part:
                doc.insert_pdf(part)
        doc.save(out)
    finally:
        doc.close()
    return out


def split_pdf(src: str, every: int = 1) -> list[str]:
    """Split into chunks of `every` pages. Default: one file per page."""
    folder = os.path.dirname(os.path.abspath(src))
    stem = os.path.splitext(os.path.basename(src))[0]
    out_dir = unique_path(folder, stem, "", tag="pages")
    os.makedirs(out_dir, exist_ok=True)
    written: list[str] = []
    with pymupdf.open(src) as doc:
        n = doc.page_count
        pad = len(str(n))
        start = 0
        while start < n:
            end = min(start + every, n)
            part = pymupdf.open()
            part.insert_pdf(doc, from_page=start, to_page=end - 1)
            label = (f"{start+1}" if every == 1 else f"{start+1}-{end}").zfill(pad)
            path = os.path.join(out_dir, f"{stem}-{label}.pdf")
            part.save(path)
            part.close()
            written.append(path)
            start = end
    return written


# ----- shrink / rotate ------------------------------------------------------

def compress_pdf(src: str) -> str:
    out = output_for(src, "compressed", new_ext=".pdf")
    with pymupdf.open(src) as doc:
        doc.save(out, garbage=4, deflate=True, deflate_images=True,
                 deflate_fonts=True, clean=True)
    return out


def rotate_pdf(src: str, degrees: int = 90) -> str:
    out = output_for(src, "rotated", new_ext=".pdf")
    with pymupdf.open(src) as doc:
        for page in doc:
            page.set_rotation((page.rotation + degrees) % 360)
        doc.save(out)
    return out


# ----- convert to office ----------------------------------------------------

def pdf_to_word(src: str) -> str:
    from pdf2docx import Converter
    out = output_for(src, "word", new_ext=".docx")
    cv = Converter(src)
    try:
        cv.convert(out)
    finally:
        cv.close()
    return out


# ----- stamp: watermark, page numbers, signature ----------------------------

def add_watermark(src: str, text: str, opacity: float = 0.12,
                  size: int = 48) -> str:
    out = output_for(src, "watermark", new_ext=".pdf")
    with pymupdf.open(src) as doc:
        for page in doc:
            r = page.rect
            pivot = pymupdf.Point(r.width / 2, r.height / 2)
            mat = pymupdf.Matrix(45)  # rotate the whole stamp 45 degrees
            tw = pymupdf.TextWriter(r, color=(0.5, 0.5, 0.5))
            tw.append(pymupdf.Point(r.width * 0.18, r.height * 0.55),
                      text, fontsize=size)
            tw.write_text(page, opacity=opacity, morph=(pivot, mat))
        doc.save(out)
    return out


def add_page_numbers(src: str, start: int = 1, size: int = 11) -> str:
    out = output_for(src, "numbered", new_ext=".pdf")
    with pymupdf.open(src) as doc:
        total = doc.page_count
        for i, page in enumerate(doc):
            r = page.rect
            label = f"{start + i} / {start + total - 1}"
            page.insert_text((r.width / 2 - 20, r.height - 24), label,
                             fontsize=size, color=(0.2, 0.2, 0.2))
        doc.save(out)
    return out


def sign_pdf(src: str, signature_png: str, page_index: int = -1,
             rel_pos: tuple[float, float] = (0.62, 0.82),
             width_ratio: float = 0.25) -> str:
    """Stamp a signature image onto one page (last page by default).

    rel_pos is the top-left of the signature as a fraction of page size;
    width_ratio is the signature width as a fraction of page width.
    """
    if not signature_png or not os.path.exists(signature_png):
        raise FileNotFoundError("signature image not set")
    out = output_for(src, "signed", new_ext=".pdf")
    with pymupdf.open(src) as doc:
        idx = page_index if page_index >= 0 else doc.page_count - 1
        page = doc[idx]
        from PIL import Image
        with Image.open(signature_png) as sig:
            ar = sig.height / sig.width
        r = page.rect
        w = r.width * width_ratio
        h = w * ar
        x = r.width * rel_pos[0]
        y = r.height * rel_pos[1]
        page.insert_image(pymupdf.Rect(x, y, x + w, y + h),
                          filename=signature_png, keep_proportion=True)
        doc.save(out)
    return out


# ----- protect / unlock -----------------------------------------------------

def protect_pdf(src: str, password: str) -> str:
    import pikepdf
    out = output_for(src, "protected", new_ext=".pdf")
    with pikepdf.open(src) as pdf:
        pdf.save(out, encryption=pikepdf.Encryption(owner=password,
                                                    user=password, R=6))
    return out


def unlock_pdf(src: str, password: str = "") -> str:
    import pikepdf
    out = output_for(src, "unlocked", new_ext=".pdf")
    with pikepdf.open(src, password=password) as pdf:
        pdf.save(out)
    return out


def pdf_page_count(src: str) -> int:
    with pymupdf.open(src) as doc:
        return doc.page_count
