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


def probe(src: str) -> Probe:
    """Read duration and streams from ffmpeg's banner (no ffprobe needed)."""
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
    elif re.search(r"Stream #\d+:\d+.*?: Video:", text):
        info.has_video = True
    return info


def _friendly_ffmpeg_error(tail: str) -> str:
    low = tail.lower()
    if "invalid data found" in low or "moov atom not found" in low:
        return "Vidéo endommagée ou format non pris en charge."
    if "permission denied" in low:
        return "Accès refusé : le fichier est peut-être ouvert dans une autre application."
    if "no space left" in low:
        return "Le disque est plein."
    last = tail.strip().splitlines()[-1:] or ["erreur inconnue"]
    return "La conversion a échoué : " + last[0][:160]


def _run(args: list[str], duration: float, ctx, label: str) -> None:
    exe = ffmpeg_path()
    cmd = [exe, "-y", "-hide_banner", "-nostdin", "-loglevel", "error",
           "-progress", "pipe:1", "-nostats", *args]
    err = tempfile.TemporaryFile()
    proc = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                            stderr=err, creationflags=_NO_WINDOW)
    if os.name == "nt":
        try:
            from ..win.jobobject import kill_with_cerclic
            kill_with_cerclic(proc.pid)
        except Exception:
            pass
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
        raise UserError("Aucune image vidéo dans ce fichier.")


EVEN = "scale=trunc(iw/2)*2:trunc(ih/2)*2"


def compress_video(src: str, crf: int = 27, max_short_side: int = 1080, ctx=None) -> str:
    """Lighter H.264 MP4, at most 1080p (short side, so phone videos filmed
    upright keep their 1080 x 1920), readable everywhere."""
    info = probe(src)
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
    info = probe(src)
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
    info = probe(src)
    _need_video(info)
    if info.duration > GIF_MAX_SECONDS:
        raise UserError("Vidéo trop longue pour un GIF (plus de 2 minutes) : "
                        "un GIF de cette durée pèserait des centaines de Mo.")
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
    info = probe(src)
    if not info.has_audio:
        raise UserError("Cette vidéo n'a pas de son.")
    out = output_for(src, "audio", new_ext=".mp3")
    _run(["-i", src, "-map", "0:a:0", "-vn", "-c:a", "libmp3lame", "-q:a", "2", out],
         info.duration, ctx, "Extraction du son")
    return out
