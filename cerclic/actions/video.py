"""Video and audio actions, driven by a bundled or system ffmpeg."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

from ..paths import output_for


def ffmpeg_path() -> str:
    """Locate ffmpeg: explicit env, bundled next to the frozen app, then PATH."""
    env = os.environ.get("CERCLIC_FFMPEG")
    if env and os.path.exists(env):
        return env
    base = getattr(sys, "_MEIPASS", None)
    if base:
        for name in ("ffmpeg.exe", "ffmpeg"):
            p = os.path.join(base, "ffmpeg", name)
            if os.path.exists(p):
                return p
    found = shutil.which("ffmpeg")
    if found:
        return found
    raise FileNotFoundError("ffmpeg introuvable")


def _run(args: list[str]) -> None:
    exe = ffmpeg_path()
    flags = 0
    if os.name == "nt":  # hide the console window of the child process
        flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    proc = subprocess.run([exe, "-y", "-hide_banner", "-loglevel", "error", *args],
                          capture_output=True, text=True, creationflags=flags)
    if proc.returncode != 0:
        tail = (proc.stderr or "").strip().splitlines()[-4:]
        raise RuntimeError("ffmpeg: " + " | ".join(tail))


def compress_video(src: str, crf: int = 28, max_height: int | None = 1080) -> str:
    out = output_for(src, "compressed", new_ext=".mp4")
    vf = []
    if max_height:
        vf.append(f"scale=-2:'min({max_height},ih)'")
    args = ["-i", src]
    if vf:
        args += ["-vf", ",".join(vf)]
    args += ["-c:v", "libx264", "-crf", str(crf), "-preset", "medium",
             "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out]
    _run(args)
    return out


def to_mp4(src: str) -> str:
    out = output_for(src, "mp4", new_ext=".mp4")
    _run(["-i", src, "-c:v", "libx264", "-crf", "20", "-preset", "medium",
          "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out])
    return out


def to_gif(src: str, fps: int = 12, width: int = 480) -> str:
    """Two-pass palette GIF for clean colours."""
    out = output_for(src, "gif", new_ext=".gif")
    vf = (f"fps={fps},scale={width}:-1:flags=lanczos,"
          "split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse")
    _run(["-i", src, "-vf", vf, "-loop", "0", out])
    return out


def extract_mp3(src: str, bitrate: str = "192k") -> str:
    out = output_for(src, "audio", new_ext=".mp3")
    _run(["-i", src, "-vn", "-c:a", "libmp3lame", "-b:a", bitrate, out])
    return out
