"""Tier 3: run the analyzer on a song and lay the result into Live as one scene per section."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Callable

from abl import catalog
from abl.catalog import ROLE_TRACK_NAMES, Sound
from abl.errors import ActionError
from abl.session import LITE_TRACK_LIMIT, Session, SessionError, Track
from abl.wire import LiveCommandError

ANALYZER_DIR = Path(os.environ.get("ABL_ANALYZER_DIR", Path(__file__).resolve().parent.parent / "analyzer"))
CACHE_DIR = Path(os.environ.get("ABL_CACHE_DIR", "~/.abl/cache")).expanduser()
MAX_SCENES = 8
BAR = 4.0
ROLES = ("drums", "bass", "keys", "lead")
REFERENCE_NAME = "Reference"
TEMPLATE_AUDIO = "-audio"
TRAP_TEMPO, HOUSE_TEMPO = 130, 118
RACE_MSG = "Live added a track while abl was working, so the change was reverted. Try again."

Progress = Callable[[str], None]


# -- the analyzer subprocess -------------------------------------------------------------

def default_runner(args: list[str], progress: Progress) -> str:
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    last = ""
    assert proc.stderr is not None and proc.stdout is not None
    for line in proc.stderr:
        line = line.rstrip()
        if line:
            last = line
            progress(line)
    out = proc.stdout.read().strip()
    proc.wait()
    if proc.returncode != 0:
        raise RuntimeError(last or f"analyzer exit {proc.returncode}")
    if not out:
        raise RuntimeError("analyzer produced no output path")
    return out.splitlines()[-1].strip()


def run_analyzer(source: str, fresh: bool, progress: Progress, runner: Callable[[list[str], Progress], str] | None = None) -> dict:
    args = ["uv", "run", "--project", str(ANALYZER_DIR), "ablanalyze", source, "--cache-dir", str(CACHE_DIR)]
    if fresh:
        args.append("--fresh")
    try:
        path = (runner or default_runner)(args, progress)
    except Exception as exc:
        raise ActionError(f"analysis failed: {exc}") from None
    try:
        return json.loads(Path(path).read_text())
    except Exception as exc:
        raise ActionError(f"could not read the analysis at {path}: {exc}") from None


# -- choices -------------------------------------------------------------------------------

def sounds_for_tempo(tempo: float) -> dict[str, Sound]:
    style = "trap" if tempo >= TRAP_TEMPO else "house" if tempo >= HOUSE_TEMPO else "pop"
    return {
        "drums": catalog.kit_for_style(style),
        "bass": catalog.default_sound("bass", style),
        "keys": catalog.sound("keys", "piano"),
        "lead": catalog.sound("lead", "sweet"),
    }


KEYS_BY_SOURCE = {"piano": "piano", "guitar": "guitar", "other": "rhodes"}


def sounds_for_analysis(analysis: dict) -> dict[str, Sound]:
    """Tempo defaults, overridden by the stem the keys came from, then by what the analyzer heard."""
    sounds = sounds_for_tempo(float(analysis.get("tempo") or 120.0))
    source = str(analysis.get("keys_source") or "")
    if source in KEYS_BY_SOURCE:
        sounds["keys"] = catalog.sound("keys", KEYS_BY_SOURCE[source])
    if analysis.get("kit") or analysis.get("instrument_tags"):
        from abl.picker import pick_sounds

        sounds, _ = pick_sounds(analysis, None, sounds)
    return sounds


def _cap_sections(sections: list[dict]) -> list[dict]:
    if len(sections) <= MAX_SCENES:
        return [dict(s) for s in sections]
    total_bars = sections[-1]["start_bar"] + sections[-1]["bars"]
    kept = [dict(s) for s in sections[:MAX_SCENES]]
    kept[-1]["bars"] = total_bars - kept[-1]["start_bar"]
    return kept


def _slice(notes: list[dict], start_beat: float, length: float) -> list[dict]:
    out = []
    for n in notes:
        rel = float(n["start_time"]) - start_beat
        if not 0.0 <= rel < length:
            continue
        duration = min(float(n.get("duration", 0.25)), length - rel)
        out.append({"pitch": int(n["pitch"]), "start_time": round(rel, 4), "duration": round(max(duration, 0.05), 4),
                    "velocity": int(n.get("velocity", 100)), "mute": False})
    return out


def _chords_for(analysis: dict, start_bar: int, bars: int) -> str:
    by_bar = {c["bar"]: c["symbol"] for c in analysis.get("chords", [])}
    symbols = [by_bar[b] for b in range(start_bar, start_bar + bars) if b in by_bar]
    collapsed: list[str] = []
    for symbol in symbols:
        if not collapsed or collapsed[-1] != symbol:
            collapsed.append(symbol)
    return "-".join(collapsed[:8])


def report(analysis: dict) -> str:
    src = analysis.get("source", {})
    key = analysis.get("key", {})
    lines = [f"{src.get('title', 'song')}: {analysis.get('tempo', 0):g} bpm, {key.get('name', 'key unknown')}, "
             f"{len(analysis.get('sections', []))} sections, {src.get('duration_s', 0):.0f} s"]
    for i, section in enumerate(analysis.get("sections", [])):
        chords = _chords_for(analysis, section["start_bar"], section["bars"])
        lines.append(f"  {i + 1}. {section['label']}: {section['bars']} bars" + (f"  {chords}" if chords else ""))
    counts = {role: len(notes) for role, notes in analysis.get("tracks", {}).items() if notes}
    if counts:
        lines.append("  notes: " + ", ".join(f"{role} {n}" for role, n in counts.items()))
    engine = analysis.get("engine") or {}
    if engine:
        lines.append("  engines: " + ", ".join(f"{k} {v}" for k, v in engine.items()))
    if analysis.get("kit") or analysis.get("instrument_tags"):
        from abl.picker import pick_sounds

        sounds, reasons = pick_sounds(analysis, None, sounds_for_tempo(float(analysis.get("tempo") or 120.0)))
        lines.append("  sounds: " + "; ".join(f"{role} {sounds[role].name} ({reasons.get(role, 'default')})" for role in ("drums", "bass", "keys", "lead") if role in sounds))
    return "\n".join(lines)


# -- push into Live ----------------------------------------------------------------------------

def _ensure_scenes(session: Session, sections: list[dict], progress: Progress) -> list[dict]:
    """Create scenes up to the section count; if Live refuses (Lite caps at 8), fold the tail into the last scene."""
    count = int(session.info().get("scene_count", 0))
    for _ in range(len(sections) - count):
        try:
            count = int(session.batch([{"type": "create_scene", "params": {"index": -1}}])[0].get("result", {}).get("scene_count", count + 1))
        except LiveCommandError:
            break
    if count < len(sections):
        total_bars = sections[-1]["start_bar"] + sections[-1]["bars"]
        sections = [dict(s) for s in sections[:count]]
        sections[-1]["bars"] = total_bars - sections[-1]["start_bar"]
        progress(f"scenes: Live allows {count}, so the remaining sections were folded into the last scene")
    session.batch([{"type": "set_scene_name", "params": {"scene_index": i, "name": f"{i + 1} {s['label']}"}} for i, s in enumerate(sections)])
    progress(f"scenes: {len(sections)} ({', '.join(s['label'] for s in sections)})")
    return sections


def _ensure_role_tracks(session: Session, roles: list[str], sounds: dict[str, Sound], progress: Progress) -> None:
    missing = [r for r in roles if session.find_track(r) is None]
    if not missing:
        return
    base = len(session.tracks)
    commands: list[dict] = []
    for k, role in enumerate(missing):
        index = base + k
        commands += [
            {"type": "create_midi_track", "params": {"index": -1}},
            {"type": "set_track_name", "params": {"track_index": index, "name": ROLE_TRACK_NAMES[role]}},
            {"type": "load_browser_item", "params": {"track_index": index, "item_uri": sounds[role].uri}},
        ]
    results = session.batch(commands)
    for k, role in enumerate(missing):
        got = (results[3 * k].get("result") or {}).get("index") if len(results) > 3 * k else None
        if got is not None and int(got) != base + k:
            session.client.send("undo")
            raise ActionError(RACE_MSG)
        session.record_created(role, base + k)
    session.refresh()
    progress("tracks: created " + ", ".join(f"{ROLE_TRACK_NAMES[r]} ({sounds[r].name})" for r in missing))


def is_template_audio(track: Track) -> bool:
    return track.type == "audio" and track.clips == 0 and not track.devices and track.name.lower().endswith(TEMPLATE_AUDIO)


def _ensure_reference(session: Session, audio: str | None, progress: Progress) -> str:
    if not audio or not Path(audio).exists():
        return "no reference audio available"
    track = session.find_track(REFERENCE_NAME)
    if track is None:
        template = next((t for t in session.tracks if is_template_audio(t)), None)
        try:
            if template is not None:
                session.batch([{"type": "set_track_name", "params": {"track_index": template.index, "name": REFERENCE_NAME}}])
            else:
                results = session.batch([{"type": "create_audio_track", "params": {"index": -1}}])
                index = int((results[0].get("result") or {}).get("index", len(session.tracks)))
                session.batch([{"type": "set_track_name", "params": {"track_index": index, "name": REFERENCE_NAME}}])
        except (SessionError, LiveCommandError):
            return "no reference track (the set is full; free a track to get the original audio for A/B)"
        session.refresh()
        track = session.find_track(REFERENCE_NAME)
        if track is None:
            return "no reference track"
    slots = session.client.send("get_track_info", {"track_index": track.index}).get("clip_slots", [])
    if slots and slots[0].get("has_clip"):
        return f"reference: {track.name} slot 0 already holds a clip, left alone"
    try:
        session.batch([
            {"type": "create_audio_clip", "params": {"track_index": track.index, "clip_index": 0, "path": audio}},
            {"type": "set_track_mute", "params": {"track_index": track.index, "mute": True}},
        ])
    except (SessionError, LiveCommandError) as exc:
        return f"no reference audio ({exc})"
    progress("reference: original audio on the Reference track (muted; unmute to A/B)")
    return "reference: original audio on the Reference track, muted"


def _overlaps(clip: dict, start: float, end: float) -> bool:
    return float(clip.get("start_time", 0)) < end and float(clip.get("end_time", 0)) > start


def _lay_arrangement(session: Session, sections: list[dict], written: dict[str, set[int]], progress: Progress) -> str:
    """Copy each section's clip to its bar position in Arrangement view, add a locator per section, show the timeline."""
    total = float(sections[-1]["start_bar"] + sections[-1]["bars"]) * BAR
    laid, skipped = [], []
    for role, slots in written.items():
        track = session.find_track(role)
        if track is None or not slots:
            continue
        reply = session.client.send("get_arrangement_clips", {"track_index": track.index})
        existing = reply.get("clips", []) if isinstance(reply, dict) else list(reply or [])
        foreign = [c for c in existing if not str(c.get("name", "")).startswith("abl ") and _overlaps(c, 0.0, total)]
        if foreign:
            skipped.append(f"{track.name} (your clip '{foreign[0].get('name', '')}' is in the way)")
            continue
        commands = [
            {"type": "duplicate_session_clip_to_arrangement", "params": {"track_index": track.index, "clip_index": i, "destination_time": sections[i]["start_bar"] * BAR}}
            for i in sorted(slots)
        ]
        session.batch(commands)
        laid.append(track.name)
    for i, section in enumerate(sections):
        session.client.send("set_current_song_time", {"time": section["start_bar"] * BAR})
        session.client.send("create_locator", {"name": f"{i + 1} {section['label']}"})
    session.client.send("set_current_song_time", {"time": 0.0})
    session.client.send("switch_to_arrangement_view")
    progress(f"arrangement: {', '.join(laid) or 'nothing'} laid out with {len(sections)} locators")
    if skipped:
        return f"arrangement: laid {', '.join(laid) or 'nothing'}; skipped {', '.join(skipped)}"
    return f"arrangement: {', '.join(laid)} laid out in order with a locator per section"


def push(session: Session, analysis: dict, progress: Progress) -> str:
    session.refresh()
    tempo = float(analysis.get("tempo") or 120.0)
    title = str(analysis.get("source", {}).get("title") or "song")
    sections = _cap_sections(analysis.get("sections") or [{"label": "song", "start_bar": 0, "bars": 8, "energy": 0.5}])
    track_notes = analysis.get("tracks", {})
    roles = [r for r in ROLES if track_notes.get(r)]
    sounds = sounds_for_analysis(analysis)
    key = analysis.get("key") or {}

    missing = [r for r in roles if session.find_track(r) is None]
    if len(session.tracks) + len(missing) > LITE_TRACK_LIMIT:
        raise ActionError(
            f"this set has {len(session.tracks)} tracks and recreate needs {len(missing)} more "
            f"({', '.join(ROLE_TRACK_NAMES[r] for r in missing)}); Live Lite allows {LITE_TRACK_LIMIT}. "
            "Start a new set or free some tracks first. Nothing was changed."
        )

    commands = [{"type": "set_tempo", "params": {"tempo": tempo}}]
    if "root" in key:
        commands.append({"type": "set_song_scale", "params": {"root_note": int(key["root"]), "scale_name": key.get("scale", "Major")}})
    session.batch(commands)
    progress(f"tempo {tempo:g} bpm, key {key.get('name', 'unchanged')}")

    sections = _ensure_scenes(session, sections, progress)
    _ensure_role_tracks(session, roles, sounds, progress)

    slot_maps: dict[str, list[dict]] = {}
    for role in roles:
        track = session.find_track(role)
        if track is not None:
            slot_maps[role] = session.client.send("get_track_info", {"track_index": track.index}).get("clip_slots", [])

    skipped: list[str] = []
    written_slots: dict[str, set[int]] = {role: set() for role in roles}
    for i, section in enumerate(sections):
        start_beat = section["start_bar"] * BAR
        length = section["bars"] * BAR
        label = section["label"]
        name = f"abl {title} {label}"
        commands = []
        written: list[str] = []
        for role in roles:
            track = session.find_track(role)
            if track is None:
                continue
            slot = next((s for s in slot_maps.get(role, []) if int(s.get("index", -1)) == i), {"has_clip": False})
            if slot.get("has_clip") and not str(slot.get("name", "")).startswith("abl "):
                skipped.append(f"{ROLE_TRACK_NAMES[role]} slot {i + 1} ({label}) holds your clip")
                continue
            notes = _slice(track_notes[role], start_beat, length)
            if not notes:
                continue
            if slot.get("has_clip"):
                commands.append({"type": "delete_clip", "params": {"track_index": track.index, "clip_index": i}})
            commands += [
                {"type": "create_clip", "params": {"track_index": track.index, "clip_index": i, "length": length}},
                {"type": "add_notes_to_clip", "params": {"track_index": track.index, "clip_index": i, "notes": notes}},
                {"type": "set_clip_loop", "params": {"track_index": track.index, "clip_index": i, "start": 0.0, "end": length, "looping": True}},
                {"type": "set_clip_name", "params": {"track_index": track.index, "clip_index": i, "name": name}},
            ]
            written.append(role)
        if commands:
            session.batch(commands)
        for role in written:
            written_slots[role].add(i)
        if i == 0:
            for role in written:
                session.remember_clip(role, 0, name, f"{title} {label}")
        progress(f"scene {i + 1} {label}: {section['bars']} bars, " + (", ".join(written) or "nothing to write"))

    arrangement = _lay_arrangement(session, sections, written_slots, progress)
    reference = _ensure_reference(session, analysis.get("source", {}).get("audio"), progress)
    session.client.send("fire_scene", {"scene_index": 0})

    lines = [report(analysis), f"  {len(sections)} scenes written", f"  {arrangement}", f"  {reference}"]
    if skipped:
        lines.append("  skipped: " + "; ".join(skipped))
    lines.append("  playing scene 1; click other scenes in Live, or `go` for scene 1 again")
    return "\n".join(lines)
