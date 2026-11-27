"""Get a song as 44.1 kHz stereo WAV in the cache, from a URL (yt-dlp) or a local file."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Callable

SAMPLE_RATE = 44100
URL_RE = re.compile(r"^https?://", re.I)


def is_url(source: str) -> bool:
    return bool(URL_RE.match(source))


def _ffmpeg_to_wav(src: Path, dst: Path) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src), "-ac", "2", "-ar", str(SAMPLE_RATE), str(dst)], check=True)


def _duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        return 0.0


def fetch(source: str, cache_dir: Path, progress: Callable[[str], None]) -> dict:
    cache_dir.mkdir(parents=True, exist_ok=True)
    if is_url(source):
        import yt_dlp

        with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True, "skip_download": True}) as ydl:
            info = ydl.extract_info(source, download=False)
        key = re.sub(r"[^A-Za-z0-9_-]", "", str(info.get("id", "")))[:32] or hashlib.sha1(source.encode()).hexdigest()[:12]
        folder = cache_dir / key
        folder.mkdir(exist_ok=True)
        audio = folder / "audio.wav"
        title = str(info.get("title") or key)
        if not audio.exists():
            progress(f"download: {title}")
            opts = {
                "quiet": True, "no_warnings": True, "format": "bestaudio/best",
                "outtmpl": str(folder / "source.%(ext)s"),
                "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "wav"}],
            }
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([source])
            downloaded = next(folder.glob("source.wav"), None)
            if downloaded is None:
                raise RuntimeError("download produced no audio")
            _ffmpeg_to_wav(downloaded, audio)
            downloaded.unlink(missing_ok=True)
        meta = {"url": source, "title": title, "key": key}
    else:
        path = Path(source).expanduser().resolve()
        if not path.exists():
            raise RuntimeError(f"no such file: {path}")
        digest = hashlib.sha1(path.read_bytes()).hexdigest()[:12]
        folder = cache_dir / digest
        folder.mkdir(exist_ok=True)
        audio = folder / "audio.wav"
        if not audio.exists():
            progress(f"convert: {path.name}")
            _ffmpeg_to_wav(path, audio)
        meta = {"url": str(path), "title": path.stem, "key": digest}
    meta.update({"audio": str(audio), "duration_s": round(_duration(audio), 2), "folder": str(folder)})
    (folder / "source.json").write_text(json.dumps(meta, indent=1))
    return meta
