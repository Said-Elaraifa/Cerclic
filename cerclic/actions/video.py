"""Video and audio actions, driven by the bundled ffmpeg (or one on PATH).

Every run reports its progress and can be cancelled: ffmpeg is stopped and the
half-written file is removed by the engine.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from dataclasses import dataclass

from ..errors import Cancelled, UserError
from ..paths import output_for
from .common import progress

_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0


def ffmpeg_path() -> str:
    """Locate ffmpeg: explicit env, bundled with the app, then PATH."""
    env = os.environ.get("CERCLIC_FFMPEG")
    if env and os.path.exists(env):
        return env
    roots = [getattr(sys, "_MEIPASS", None), os.path.dirname(sys.executable)]
    for root in roots:
        if not root:
            continue
        for name in ("ffmpeg.exe", "ffmpeg"):
            p = os.path.join(root, "ffmpeg", name)
            if os.path.exists(p):
                return p
    found = shutil.which("ffmpeg")
    if found:
        return found
    raise UserError("ffmpeg est introuvable : réinstalle Cerclic.")


@dataclass
class Probe:
    duration: float = 0.0
    has_video: bool = False
    has_audio: bool = False
    width: int = 0
    height: int = 0


_DUR = re.compile(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)")
_VID = re.compile(r"Stream #\d+:\d+.*?: Video: .*?(\d{2,5})x(\d{2,5})")


def _tie(proc) -> None:
    """The process stops with Cerclic (a job object on Windows)."""
    if os.name == "nt":
        try:
            from ..win.jobobject import kill_with_cerclic
            kill_with_cerclic(proc.pid)
        except Exception:
            pass


def _stopper(ctx):
    return (lambda: ctx.cancelled) if ctx is not None else None


def probe(src: str, measure: bool = True, should_stop=None) -> Probe:
    """Read duration and streams from ffmpeg's banner (no ffprobe needed).
    With `measure`, a file whose header has no duration is read through to
    find it (stopped as soon as `should_stop()` says so)."""
    try:
        proc = subprocess.run([ffmpeg_path(), "-hide_banner", "-nostdin", "-i", src],
                              stdin=subprocess.DEVNULL, capture_output=True,
                              creationflags=_NO_WINDOW, timeout=60)
    except subprocess.TimeoutExpired:
        return Probe()
    text = proc.stderr.decode("utf-8", "replace")
    info = Probe()
    m = _DUR.search(text)
    if m:
        h, mi, s = m.groups()
        info.duration = int(h) * 3600 + int(mi) * 60 + float(s)
    info.has_audio = bool(re.search(r"Stream #\d+:\d+.*?: Audio:", text))
    v = _VID.search(text)
    if v:
        info.has_video = True
        info.width, info.height = int(v.group(1)), int(v.group(2))
        # phone videos filmed upright are stored sideways with a rotation flag
        rot = re.search(r"rotation of (-?\d+(?:\.\d+)?) degrees", text) or \
            re.search(r"\brotate\s*:\s*(-?\d+)", text)
        if rot and round(abs(float(rot.group(1)))) % 180 == 90:
            info.width, info.height = info.height, info.width
    elif re.search(r"Stream #\d+:\d+.*?: Video:", text):
        info.has_video = True
    if measure and info.duration <= 0 and (info.has_video or info.has_audio):
        info.duration = _measure_duration(src, should_stop)
    return info


_TIME = re.compile(r"time=(\d+):(\d+):(\d+(?:\.\d+)?)")


def _measure_duration(src: str, should_stop=None, timeout: float = 120.0) -> float:
    """Length of a file whose header does not give it (screen or browser
    recordings in WEBM): read through it without decoding anything."""
    try:
        proc = subprocess.Popen([ffmpeg_path(), "-hide_banner", "-nostdin", "-i", src,
                                 "-c", "copy", "-f", "null", "-"],
                                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                stderr=subprocess.PIPE, creationflags=_NO_WINDOW)
    except (OSError, UserError):
        return 0.0
    _tie(proc)
    deadline = time.monotonic() + timeout
    while True:
        try:
            _, err = proc.communicate(timeout=0.25)
            break
        except subprocess.TimeoutExpired:
            if (should_stop is not None and should_stop()) or time.monotonic() > deadline:
                proc.kill()
                proc.communicate()
                return 0.0
    found = _TIME.findall(err.decode("utf-8", "replace"))
    if not found:
        return 0.0
    h, mi, sec = found[-1]
    return int(h) * 3600 + int(mi) * 60 + float(sec)


def _friendly_ffmpeg_error(tail: str) -> str:
    low = tail.lower()
    if "invalid data found" in low or "moov atom not found" in low:
        return "Vidéo endommagée ou format non pris en charge."
    if "permission denied" in low:
        return "Accès refusé : le fichier est peut-être ouvert dans une autre application."
    if "no space left" in low:
        return "Le disque est plein."
    if "no such file" in low:
        return "Fichier introuvable : il a peut-être été déplacé ou supprimé."
    from ..log import log
    log("ffmpeg : " + tail.strip()[-600:])
    return ("Le traitement a échoué : le fichier est peut-être endommagé ou dans un "
            "format inhabituel.")


def _run(args: list[str], duration: float, ctx, label: str) -> None:
    exe = ffmpeg_path()
    cmd = [exe, "-y", "-hide_banner", "-nostdin", "-loglevel", "error",
           "-progress", "pipe:1", "-nostats", *args]
    err = tempfile.TemporaryFile()
    proc = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                            stderr=err, creationflags=_NO_WINDOW)
    _tie(proc)
    stop = threading.Event()

    def watchdog():
        while not stop.is_set():
            if ctx is not None and ctx.cancelled and proc.poll() is None:
                proc.kill()
                return
            time.sleep(0.1)

    guard = threading.Thread(target=watchdog, daemon=True)
    guard.start()
    try:
        progress(ctx, 0.0 if duration > 0 else None, label)
        for raw in proc.stdout:
            line = raw.decode("ascii", "ignore").strip()
            if line.startswith(("out_time_us=", "out_time_ms=")) and duration > 0:
                try:
                    done = int(line.split("=", 1)[1]) / 1_000_000
                except ValueError:
                    continue
                progress(ctx, min(0.99, done / duration), label)
        proc.wait()
    finally:
        stop.set()
        guard.join(timeout=1)
        if proc.poll() is None:
            proc.kill()
            proc.wait()
    if ctx is not None and ctx.cancelled:
        err.close()
        raise Cancelled()
    if proc.returncode != 0:
        err.seek(0)
        tail = err.read()[-2000:].decode("utf-8", "replace")
        err.close()
        raise UserError(_friendly_ffmpeg_error(tail))
    err.close()


def _need_video(info: Probe) -> None:
    if not info.has_video:
        if info.has_audio:
            raise UserError("Ce fichier ne contient que du son, pas d'image : utilise "
                            "« Extraire le son » pour en faire un MP3.")
        raise UserError("Aucune image vidéo dans ce fichier.")


EVEN = "scale=trunc(iw/2)*2:trunc(ih/2)*2"


def compress_video(src: str, crf: int = 27, max_short_side: int = 1080, ctx=None) -> str:
    """Lighter H.264 MP4, at most 1080p (short side, so phone videos filmed
    upright keep their 1080 x 1920), readable everywhere."""
    info = probe(src, should_stop=_stopper(ctx))
    if not info.has_video and info.has_audio:     # a sound in a video file (.webm...)
        return compress_audio(src, ctx=ctx)
    _need_video(info)
    out = output_for(src, "compressed", new_ext=".mp4")
    m = max_short_side
    vf = (f"scale='if(gte(iw,ih),-2,trunc(min({m},iw)/2)*2)'"
          f":'if(gte(iw,ih),trunc(min({m},ih)/2)*2,-2)'")
    _run(["-i", src, "-map", "0:v:0", "-map", "0:a:0?", "-vf", vf,
          "-c:v", "libx264", "-crf", str(crf), "-preset", "faster",
          "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
          "-movflags", "+faststart", out], info.duration, ctx, "Compression")
    return out


def to_mp4(src: str, ctx=None) -> str:
    """H.264 + AAC MP4 at high quality: plays on every phone, PC and site."""
    info = probe(src, should_stop=_stopper(ctx))
    _need_video(info)
    out = output_for(src, "mp4", new_ext=".mp4")
    _run(["-i", src, "-map", "0:v:0", "-map", "0:a:0?", "-vf", EVEN,
          "-c:v", "libx264", "-crf", "20", "-preset", "faster",
          "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
          "-movflags", "+faststart", out], info.duration, ctx, "Conversion en MP4")
    return out


GIF_MAX_SECONDS = 120


def to_gif(src: str, fps: int = 12, width: int = 480, ctx=None) -> str:
    """Palette-optimised GIF, 480 px wide at most. Two passes (palette, then
    frames) so memory stays flat whatever the length."""
    info = probe(src, should_stop=_stopper(ctx))
    _need_video(info)
    if info.duration > GIF_MAX_SECONDS:
        raise UserError("Vidéo trop longue pour un GIF (plus de 2 minutes : il "
                        "pèserait des centaines de Mo). Garde d'abord un passage avec "
                        "« Raccourcir ».")
    out = output_for(src, "gif", new_ext=".gif")
    scale = f"fps={fps},scale='min({width},iw)':-2:flags=lanczos"
    tmpdir = tempfile.mkdtemp(prefix="cerclic-gif-")
    palette = os.path.join(tmpdir, "palette.png")
    try:
        _run(["-i", src, "-vf", f"{scale},palettegen=stats_mode=diff", palette],
             info.duration, _Half(ctx, 0.0), "Conversion en GIF")
        _run(["-i", src, "-i", palette, "-lavfi", f"{scale}[x];[x][1:v]paletteuse",
              "-loop", "0", out], info.duration, _Half(ctx, 0.5), "Conversion en GIF")
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
    return out


class _Half:
    """Progress of one of two passes, mapped to its half of the bar."""

    def __init__(self, ctx, start: float):
        self._ctx, self._start = ctx, start

    @property
    def cancelled(self) -> bool:
        return self._ctx is not None and self._ctx.cancelled

    def check(self) -> None:
        if self._ctx is not None:
            self._ctx.check()

    def progress(self, fraction, text: str = "") -> None:
        if self._ctx is not None:
            f = None if fraction is None else self._start + fraction / 2
            self._ctx.progress(f, text)


def extract_mp3(src: str, ctx=None) -> str:
    from ..errors import NothingToDo
    info = probe(src, should_stop=_stopper(ctx))
    if not info.has_audio:
        raise NothingToDo("Cette vidéo n'a pas de son.")
    out = output_for(src, "audio", new_ext=".mp3")
    _run(["-i", src, "-map", "0:a:0", "-vn", "-c:a", "libmp3lame", "-q:a", "2", out],
         info.duration, ctx, "Extraction du son")
    return out


# ----- cut, mute, rotate -----------------------------------------------------------------

# Audio formats kept as they are when cutting a sound file: (extension, codec args)
_AUDIO_KEEP = {
    ".mp3": (".mp3", ["-c:a", "libmp3lame", "-q:a", "2"]),
    ".m4a": (".m4a", ["-c:a", "aac", "-b:a", "192k"]),
    ".aac": (".m4a", ["-c:a", "aac", "-b:a", "192k"]),
    ".wav": (".wav", ["-c:a", "pcm_s16le"]),
    ".flac": (".flac", ["-c:a", "flac"]),
    ".ogg": (".ogg", ["-c:a", "libvorbis", "-q:a", "5"]),
    ".oga": (".ogg", ["-c:a", "libvorbis", "-q:a", "5"]),
    ".opus": (".opus", ["-c:a", "libopus", "-b:a", "128k"]),
}
_MP3 = (".mp3", ["-c:a", "libmp3lame", "-q:a", "2"])


def _fmt_time(t: float) -> str:
    return f"{t:.3f}"


def trim_media(src: str, start: float, end: float, ctx=None) -> str:
    """Keep from `start` to `end` seconds. Videos become an MP4 readable
    everywhere; sounds keep their format (MP3 for the rarer ones)."""
    from ..paths import ext_of, kind_of
    info = probe(src, should_stop=_stopper(ctx))
    duration = info.duration
    start = max(0.0, float(start))
    end = float(end)
    if duration > 0:
        end = min(end, duration)
    if end - start < 0.1:
        raise UserError("Le passage à garder est trop court.")
    if duration > 0 and start <= 0.05 and end >= duration - 0.05:
        from ..errors import NothingToDo
        raise NothingToDo("Le passage choisi est la totalité du fichier.")
    length = end - start
    if kind_of(src) == "video" and (info.has_video or not info.has_audio):
        _need_video(info)
        out = output_for(src, "cut", new_ext=".mp4")
        _run(["-ss", _fmt_time(start), "-i", src, "-t", _fmt_time(length),
              "-map", "0:v:0", "-map", "0:a:0?", "-vf", EVEN,
              "-c:v", "libx264", "-crf", "20", "-preset", "faster",
              "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
              "-movflags", "+faststart", out], length, ctx, "Découpage")
        return out
    if not info.has_audio:
        raise UserError("Aucun son dans ce fichier.")
    ext, codec = _AUDIO_KEEP.get(ext_of(src), _MP3)
    out = output_for(src, "cut", new_ext=ext)
    _run(["-ss", _fmt_time(start), "-i", src, "-t", _fmt_time(length),
          "-map", "0:a:0", "-vn", *codec, out], length, ctx, "Découpage")
    return out


def mute_video(src: str, ctx=None) -> str:
    """Same video without its sound, not re-encoded (instant, no quality loss)."""
    from ..errors import NothingToDo
    from ..paths import ext_of
    info = probe(src, should_stop=_stopper(ctx))
    _need_video(info)
    if not info.has_audio:
        raise NothingToDo("Cette vidéo n'a pas de son.")
    out = output_for(src, "muted", new_ext=ext_of(src) or ".mp4")
    try:
        _run(["-i", src, "-map", "0:v", "-c", "copy", "-an", out],
             info.duration, ctx, "Suppression du son")
        return out
    except UserError:
        try:
            os.remove(out)
        except OSError:
            pass
    out = output_for(src, "muted", new_ext=".mp4")       # odd file: re-encode it
    _run(["-i", src, "-map", "0:v:0", "-an", "-vf", EVEN, "-c:v", "libx264",
          "-crf", "20", "-preset", "faster", "-pix_fmt", "yuv420p",
          "-movflags", "+faststart", out], info.duration, ctx, "Suppression du son")
    return out


_TRANSPOSE = {90: "transpose=1", 270: "transpose=2", 180: "transpose=1,transpose=1"}


def rotate_video(src: str, degrees: int = 90, ctx=None) -> str:
    """Turn the picture clockwise by 90, 180 or 270 degrees (a phone video
    filmed sideways), as an MP4 readable everywhere."""
    deg = int(degrees) % 360
    if deg not in _TRANSPOSE:
        raise ValueError("rotation must be a multiple of 90 degrees")
    info = probe(src, should_stop=_stopper(ctx))
    _need_video(info)
    out = output_for(src, "rotated", new_ext=".mp4")
    _run(["-i", src, "-map", "0:v:0", "-map", "0:a:0?",
          "-vf", f"{_TRANSPOSE[deg]},{EVEN}", "-c:v", "libx264", "-crf", "20",
          "-preset", "faster", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
          "-movflags", "+faststart", out], info.duration, ctx, "Rotation")
    return out


def audio_to_mp3(src: str, ctx=None) -> str:
    """Any sound file (WhatsApp voice note, M4A, WAV...) as an MP3 that plays
    everywhere."""
    from ..errors import NothingToDo
    from ..paths import ext_of
    if ext_of(src) == ".mp3":
        raise NothingToDo("C'est déjà un MP3.")
    info = probe(src, should_stop=_stopper(ctx))
    if not info.has_audio:
        raise UserError("Aucun son dans ce fichier.")
    out = output_for(src, "mp3", new_ext=".mp3")
    _run(["-i", src, "-map", "0:a:0", "-vn", "-c:a", "libmp3lame", "-q:a", "2", out],
         info.duration, ctx, "Conversion en MP3")
    return out


# ----- previews for the cutting popup ------------------------------------------------------

def _capture(args: list[str], timeout: float = 20.0, should_stop=None) -> bytes:
    """Run ffmpeg and return what it writes on stdout (a PNG). The process is
    tied to Cerclic (it stops with it), and killed if it takes too long or as
    soon as `should_stop()` says the popup that wanted it has closed."""
    if should_stop is not None and should_stop():
        raise Cancelled()
    proc = subprocess.Popen([ffmpeg_path(), "-hide_banner", "-nostdin", "-loglevel",
                             "error", *args], stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                            creationflags=_NO_WINDOW)
    _tie(proc)
    deadline = time.monotonic() + timeout
    while True:
        try:
            out, _ = proc.communicate(timeout=0.25)
            break
        except subprocess.TimeoutExpired:
            stopped = should_stop is not None and should_stop()
            if stopped or time.monotonic() > deadline:
                proc.kill()
                proc.communicate()
                if stopped:
                    raise Cancelled()
                raise UserError("Aperçu trop long à préparer.")
    if proc.returncode != 0 or not out:
        raise UserError("Aperçu impossible.")
    return out


def frame_png(src: str, t: float, max_w: int, max_h: int, should_stop=None) -> bytes:
    """One frame at `t` seconds, fitted in max_w x max_h, as PNG bytes."""
    vf = (f"scale=w={int(max_w)}:h={int(max_h)}:force_original_aspect_ratio=decrease,"
          "format=rgb24")
    return _capture(["-ss", _fmt_time(max(0.0, t)), "-i", src, "-frames:v", "1",
                     "-vf", vf, "-f", "image2pipe", "-c:v", "png", "-"],
                    should_stop=should_stop)


def waveform_png(src: str, width: int, height: int, color: str = "#F2A93B",
                 should_stop=None) -> bytes:
    """The sound drawn as a waveform, as PNG bytes (transparent background)."""
    graph = (f"aformat=channel_layouts=mono,showwavespic=s={int(width)}x{int(height)}"
             f":colors={color}:scale=sqrt")
    return _capture(["-i", src, "-filter_complex", graph, "-frames:v", "1",
                     "-f", "image2pipe", "-c:v", "png", "-"], timeout=120.0,
                    should_stop=should_stop)


def compress_audio(src: str, ctx=None) -> str:
    """Lighter MP3 (96 kbit/s, plenty for voice and fine for music on a phone)."""
    from ..errors import NothingToDo
    info = probe(src, should_stop=_stopper(ctx))
    if not info.has_audio:
        raise UserError("Aucun son dans ce fichier.")
    out = output_for(src, "compressed", new_ext=".mp3")
    _run(["-i", src, "-map", "0:a:0", "-vn", "-c:a", "libmp3lame", "-b:a", "96k", out],
         info.duration, ctx, "Compression")
    if os.path.getsize(out) >= os.path.getsize(src) * 0.95:
        os.remove(out)
        raise NothingToDo("Ce son est déjà léger.")
    return out
