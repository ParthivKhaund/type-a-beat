"""`abl import <url or file>`: fetch a song's audio into the shared cache and put it on an audio track.

Uses the same cache layout as the analyzer (~/.abl/cache/<id>/audio.wav + source.json), so a later
`recreate` of the same link skips the download.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Callable

from abl.errors import ActionError
from abl.recreate import CACHE_DIR, is_template_audio
from abl.session import LITE_TRACK_LIMIT, Session, SessionError
from abl.wire import LiveCommandError

SAMPLE_RATE = 44100
MAX_TRACK_NAME = 30
URL_RE = re.compile(r"^https?://", re.I)
Progress = Callable[[str], None]
Runner = Callable[[list[str]], str]


def default_run(args: list[str]) -> str:
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        lines = (result.stderr or result.stdout).strip().splitlines()
        raise RuntimeError(lines[-1] if lines else f"{args[0]} exit {result.returncode}")
    return result.stdout


def _to_wav(src: Path, dst: Path, run: Runner) -> None:
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src), "-ac", "2", "-ar", str(SAMPLE_RATE), str(dst)])


def _duration(path: Path, run: Runner) -> float:
    try:
        return round(float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]).strip()), 2)
    except (RuntimeError, ValueError):
        return 0.0


def _save(folder: Path, meta: dict) -> dict:
    (folder / "source.json").write_text(json.dumps(meta, indent=1))
    return meta


def _known_duration(folder: Path, audio: Path, run: Runner) -> float:
    """Reuse the length saved on an earlier run; probe only for a new file."""
    try:
        saved = json.loads((folder / "source.json").read_text())
        if saved.get("duration_s"):
            return float(saved["duration_s"])
    except (OSError, ValueError):
        pass
    return _duration(audio, run)


def _fetch_url(url: str, cache_dir: Path, progress: Progress, run: Runner) -> dict:
    info = run(["yt-dlp", "--no-playlist", "--skip-download", "--print", "%(id)s", "--print", "%(title)s", "--print", "%(duration)s", url]).splitlines()
    video_id = re.sub(r"[^A-Za-z0-9_-]", "", info[0] if info else "")[:32] or hashlib.sha1(url.encode()).hexdigest()[:12]
    title = (info[1] if len(info) > 1 else "").strip() or video_id
    folder = cache_dir / video_id
    folder.mkdir(parents=True, exist_ok=True)
    audio = folder / "audio.wav"
    if not audio.exists():
        progress(f"import: downloading {title}")
        run(["yt-dlp", "--no-playlist", "-f", "bestaudio/best", "-x", "--audio-format", "wav", "-o", str(folder / "source.%(ext)s"), url])
        downloaded = folder / "source.wav"
        if not downloaded.exists():
            raise RuntimeError("the download produced no audio")
        progress("import: converting to 44.1 kHz WAV")
        _to_wav(downloaded, audio, run)
        downloaded.unlink(missing_ok=True)
    else:
        progress(f"import: {title} already downloaded")
    return _save(folder, {"url": url, "title": title, "key": video_id, "audio": str(audio), "duration_s": _known_duration(folder, audio, run), "folder": str(folder)})


def _fetch_file(source: str, cache_dir: Path, progress: Progress, run: Runner) -> dict:
    path = Path(source).expanduser().resolve()
    if not path.exists():
        raise ActionError(f"no such file: {path}")
    digest = hashlib.sha1(path.read_bytes()).hexdigest()[:12]
    folder = cache_dir / digest
    folder.mkdir(parents=True, exist_ok=True)
    audio = folder / "audio.wav"
    if not audio.exists():
        progress(f"import: converting {path.name}")
        _to_wav(path, audio, run)
    return _save(folder, {"url": str(path), "title": path.stem, "key": digest, "audio": str(audio), "duration_s": _known_duration(folder, audio, run), "folder": str(folder)})


def fetch_audio(source: str, cache_dir: Path, progress: Progress, run: Runner | None = None) -> dict:
    run = run or default_run
    try:
        if URL_RE.match(source):
            return _fetch_url(source, cache_dir, progress, run)
        return _fetch_file(source, cache_dir, progress, run)
    except ActionError:
        raise
    except Exception as exc:
        hint = ""
        if "403" in str(exc) or "Sign in to confirm" in str(exc):
            hint = " YouTube often breaks older downloaders; run `brew upgrade yt-dlp` and try again."
        raise ActionError(f"import failed: {exc}.{hint}") from None


def _track_name(title: str) -> str:
    name = re.sub(r"\s+", " ", title).strip()
    return name if len(name) <= MAX_TRACK_NAME else name[: MAX_TRACK_NAME - 1].rstrip() + "…"


def _audio_track(session: Session, name: str) -> int:
    template = next((t for t in session.tracks if is_template_audio(t)), None)
    try:
        if template is not None:
            index = template.index
        else:
            results = session.batch([{"type": "create_audio_track", "params": {"index": -1}}])
            index = int((results[0].get("result") or {}).get("index", len(session.tracks)))
        session.batch([{"type": "set_track_name", "params": {"track_index": index, "name": name}}])
    except SessionError as exc:
        raise ActionError(str(exc)) from None
    return index


def import_song(session: Session, source: str, progress: Progress, cache_dir: Path | None = None, run: Runner | None = None) -> str:
    session.refresh()
    if not any(is_template_audio(t) for t in session.tracks) and len(session.tracks) >= LITE_TRACK_LIMIT:
        raise ActionError(
            f"this set has {len(session.tracks)} tracks and Live Lite allows {LITE_TRACK_LIMIT}; "
            "free a track or empty an audio track first. Nothing was downloaded."
        )
    meta = fetch_audio(source, cache_dir or CACHE_DIR, progress, run)
    name = _track_name(meta["title"])
    index = _audio_track(session, name)
    slots = session.client.send("get_track_info", {"track_index": index}).get("clip_slots", [])
    slot = next((int(s["index"]) for s in slots if not s.get("has_clip")), 0)
    try:
        session.batch([
            {"type": "create_audio_clip", "params": {"track_index": index, "clip_index": slot, "path": meta["audio"]}},
            {"type": "set_clip_name", "params": {"track_index": index, "clip_index": slot, "name": f"abl {name}"}},
        ])
    except (SessionError, LiveCommandError) as exc:
        raise ActionError(f"Live could not load the audio: {exc}") from None
    minutes, seconds = divmod(int(meta.get("duration_s") or 0), 60)
    return f"Imported: {meta['title']} ({minutes}:{seconds:02d}) on track {index} '{name}', slot {slot}. Click the clip in Live to play it."
