"""Pictures and videos at the sizes social networks expect.

A format is a shape and an exact size in pixels (an Instagram portrait post is
1080 x 1350). Two ways to get there:
  "fill"    the picture covers the whole frame and what sticks out is cut; the
            user chooses the part that stays (a centre and a zoom, from the popup)
  "blur", "white", "black"   the whole picture fits inside the frame, on a
            blurred enlargement of itself, or on plain white or black
Pictures become JPG (what every network expects, without the photo's private
information such as its GPS position), videos an H.264 MP4. The result goes
beside the original: "photo (story).jpg".
"""
from __future__ import annotations

from dataclasses import dataclass

from PIL import Image, ImageEnhance, ImageFilter

from ..errors import NothingToDo, UserError
from ..i18n import N_, tr
from ..paths import output_for
from . import images, video


@dataclass(frozen=True)
class Format:
    """label, ratio, where and tag stay French (N_): tr(f.label) shows them."""
    key: str
    label: str          # on its button
    ratio: str          # its shape, as the networks write it
    width: int
    height: int
    where: str          # what it is for
    tag: str            # in the result's name (translated when the file is made)

    @property
    def aspect(self) -> float:
        return self.width / self.height

    @property
    def size_text(self) -> str:
        return f"{self.width} × {self.height} px"


FORMATS = (
    Format("square", N_("Carré"), "1:1", 1080, 1080,
           N_("Publication Instagram, Facebook ou LinkedIn"), N_("carré")),
    Format("portrait", N_("Portrait"), "4:5", 1080, 1350,
           N_("Publication Instagram ou Facebook, la plus grande dans le fil"),
           N_("portrait")),
    Format("grid", N_("Grille"), "3:4", 1080, 1440,
           N_("Instagram, à la forme exacte de la grille du profil"), N_("grille")),
    Format("story", N_("Story"), "9:16", 1080, 1920,
           N_("Plein écran de téléphone : Story, Reels, TikTok, YouTube Shorts"),
           N_("story")),
    Format("landscape", N_("Paysage"), "16:9", 1920, 1080,
           N_("Écran d'ordinateur : YouTube, présentation, X"), N_("paysage")),
    Format("banner", N_("Bannière"), N_("1,91:1"), 1200, 630,
           N_("Lien partagé ou image large sur Facebook, LinkedIn ou X"), N_("bannière")),
)
BY_KEY = {f.key: f for f in FORMATS}
MODES = ("fill", "blur", "white", "black")
MAX_ZOOM = 6.0

# "Fond flou": the background is the picture reduced to a tenth of the final
# size, blurred there, then enlarged (very soft) and a little darkened so the
# picture itself stands out.
BLUR_SHRINK = 10
BLUR_SIGMA = 4
BLUR_DARKEN = 0.85


def fmt_of(key: str) -> Format:
    try:
        return BY_KEY[key]
    except KeyError:
        raise ValueError(f"unknown social format: {key}") from None


def place_box(W: float, H: float, aspect: float, center=(0.5, 0.5),
              zoom: float = 1.0) -> tuple[float, float, float, float]:
    """The part of a W x H picture that fills a frame of this shape: the
    largest one, divided by `zoom`, centred on `center` (fractions of W and H)
    as far as the picture allows. (left, top, right, bottom)."""
    W, H = max(1e-9, float(W)), max(1e-9, float(H))
    w = W
    h = w / aspect
    if h > H:
        h = H
        w = h * aspect
    z = min(MAX_ZOOM, max(1.0, float(zoom)))
    w, h = w / z, h / z
    cx, cy = float(center[0]), float(center[1])
    x = min(max(0.0, cx * W - w / 2), W - w)
    y = min(max(0.0, cy * H - h / 2), H - h)
    return (x, y, x + w, y + h)


def fit_size(W: float, H: float, f: Format) -> tuple[int, int]:
    """The whole picture inside the frame: its size there, in pixels."""
    s = min(f.width / W, f.height / H)
    return max(1, round(W * s)), max(1, round(H * s))


def enlarged(W: float, H: float, f: Format, mode: str, zoom: float = 1.0) -> bool:
    """Whether the picture has to be enlarged to that size (it gets softer)."""
    if mode == "fill":
        x0, _, x1, _ = place_box(W, H, f.aspect, zoom=zoom)
        return x1 - x0 < f.width * 0.98
    return fit_size(W, H, f)[0] > W * 1.02


# ----- pictures ------------------------------------------------------------------------------

def to_screen_rgb(im: Image.Image, icc: bytes | None = None) -> Image.Image:
    """8-bit RGB (RGBA if see-through) in screen colours (sRGB): what the
    networks show. Print colours (CMYK) and wide-gamut profiles (an iPhone's
    Display P3) are converted through their profile."""
    if im.mode == "CMYK":
        im = images._cmyk_to_srgb(im, icc)
        icc = None
    im = images._to_8bit(im)
    alpha = im.mode in ("RGBA", "LA", "PA") or (im.mode == "P" and "transparency" in im.info)
    return images._rgb_to_srgb(im.convert("RGBA" if alpha else "RGB"), icc)


def blurred_background(im: Image.Image, f: Format, final: bool = True) -> Image.Image:
    """The "Fond flou" background for this picture: at the format's size, or
    (final=False) the small blurred picture it is enlarged from."""
    W, H = im.size
    box = place_box(W, H, f.aspect)
    if im.mode != "RGB":
        im = images._flatten(im).convert("RGB")
    sw, sh = max(1, f.width // BLUR_SHRINK), max(1, f.height // BLUR_SHRINK)
    small = im.resize((sw, sh), Image.Resampling.BILINEAR, box=box, reducing_gap=2.0)
    small = small.filter(ImageFilter.GaussianBlur(BLUR_SIGMA))
    small = ImageEnhance.Brightness(small).enhance(BLUR_DARKEN)
    if not final:
        return small
    return small.resize((f.width, f.height), Image.Resampling.BICUBIC)


def compose(im: Image.Image, f: Format, mode: str = "fill", center=(0.5, 0.5),
            zoom: float = 1.0) -> Image.Image:
    """The picture at the format's exact size, as an RGB image."""
    if mode not in MODES:
        raise ValueError(f"unknown mode: {mode}")
    W, H = im.size
    if mode == "fill":
        flat = images._flatten(im, (255, 255, 255)).convert("RGB")
        box = place_box(W, H, f.aspect, center, zoom)
        return flat.resize((f.width, f.height), Image.Resampling.LANCZOS, box=box,
                           reducing_gap=3.0)
    if mode == "blur":
        canvas = blurred_background(im, f)
    else:
        canvas = Image.new("RGB", (f.width, f.height),
                           (255, 255, 255) if mode == "white" else (0, 0, 0))
    tw, th = fit_size(W, H, f)
    pic = im.resize((tw, th), Image.Resampling.LANCZOS, reducing_gap=3.0)
    pos = ((f.width - tw) // 2, (f.height - th) // 2)
    canvas.paste(pic, pos, pic if pic.mode == "RGBA" else None)
    return canvas


def social_image(src: str, key: str, mode: str = "fill", center=(0.5, 0.5),
                 zoom: float = 1.0, quality: int | None = None) -> str:
    """`src` in the format `key` ("story"...), as a JPG beside it."""
    f = fmt_of(key)
    pic = images.load(src, first_frame=True)          # an animation: its first picture
    images._one_page(src, pic)
    im = to_screen_rgb(pic.frames[0], pic.icc)
    W, H = im.size
    if (W, H) == (f.width, f.height) and (mode != "fill" or zoom <= 1.001) \
            and im.mode == "RGB":
        raise NothingToDo(tr("Cette image est déjà en {size}.", size=f.size_text))
    result = compose(im, f, mode, center, zoom)
    out = output_for(src, f.tag, new_ext=".jpg")
    images.save(images.Picture([result]), out, "jpg", quality=quality)
    return out


# ----- videos ----------------------------------------------------------------------------------

def _even(n: int) -> int:
    return max(2, n - n % 2)


def video_filter(W: float, H: float, f: Format, mode: str = "fill", center=(0.5, 0.5),
                 zoom: float = 1.0, fps: float = 0.0) -> str:
    """The ffmpeg filter graph that makes a W x H video (as seen) into the
    format: its output is labelled [v]."""
    if mode not in MODES:
        raise ValueError(f"unknown mode: {mode}")
    fw, fh = f.width, f.height
    pre = f"[0:v:0]{video.SQUARE_PIXELS}"
    tail = (",fps=60" if fps > 60.5 else "") + ",format=yuv420p[v]"
    fit = (f"scale=w={fw}:h={fh}:force_original_aspect_ratio=decrease"
           ":force_divisible_by=2:flags=lanczos")
    if mode == "fill":
        x0, y0, x1, y1 = place_box(W, H, f.aspect, center, zoom)
        rx, ry, rw, rh = x0 / W, y0 / H, (x1 - x0) / W, (y1 - y0) / H
        # (relative to the frame ffmpeg works on; 2 pixels at least for a tiny video)
        return (f"{pre},crop=w='max(2,iw*{rw:.6f})':h='max(2,ih*{rh:.6f})'"
                f":x=iw*{rx:.6f}:y=ih*{ry:.6f},"
                f"scale={fw}:{fh}:flags=lanczos,setsar=1{tail}")
    if mode in ("white", "black"):
        return (f"{pre},{fit},pad={fw}:{fh}:(ow-iw)/2:(oh-ih)/2:color={mode},"
                f"setsar=1{tail}")
    sw, sh = _even(fw // BLUR_SHRINK), _even(fh // BLUR_SHRINK)
    return (f"{pre},split=2[a][b];"
            f"[a]scale={sw}:{sh}:force_original_aspect_ratio=increase,crop={sw}:{sh},"
            f"gblur=sigma={BLUR_SIGMA},lutyuv=y=(val-16)*{BLUR_DARKEN}+16"
            f":u=(val-128)*{BLUR_DARKEN}+128:v=(val-128)*{BLUR_DARKEN}+128,"
            f"scale={fw}:{fh}:flags=bicubic,setsar=1[bg];"
            f"[b]{fit},setsar=1[fg];"
            f"[bg][fg]overlay=x=(W-w)/2:y=(H-h)/2{tail}")


def social_video(src: str, key: str, mode: str = "blur", center=(0.5, 0.5),
                 zoom: float = 1.0, ctx=None) -> str:
    """`src` in the format `key`, as an MP4 (H.264 and AAC) beside it."""
    f = fmt_of(key)
    info = video.probe(src, should_stop=video._stopper(ctx))
    video._need_video(info)
    W, H = info.display_size
    if W <= 0 or H <= 0:
        raise UserError(tr("Taille de la vidéo illisible : fichier endommagé ?"))
    if (round(W), round(H)) == (f.width, f.height) and (mode != "fill" or zoom <= 1.001):
        raise NothingToDo(tr("Cette vidéo est déjà en {size}.", size=f.size_text))
    graph = video_filter(W, H, f, mode, center, zoom, info.fps)
    out = output_for(src, f.tag, new_ext=".mp4")
    # (-map_metadata -1: nothing of the original's tags, such as the place
    # where a phone filmed it, goes with a video made to be published)
    video._run(["-i", src, "-filter_complex", graph, "-map", "[v]", "-map", "0:a:0?",
                "-map_metadata", "-1", "-map_chapters", "-1",
                "-c:v", "libx264", "-crf", "20", "-preset", "faster",
                "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out],
               info.duration, ctx, tr("Format {name}", name=tr(f.tag)))
    return out
