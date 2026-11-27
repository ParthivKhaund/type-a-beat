"""One Command in, one batch to Live out, one line of text back."""

from __future__ import annotations

from abl import catalog
from abl import recreate as recreate_mod
from abl.catalog import Sound, kit_for_style, pad_map
from abl.errors import ActionError
from abl.commands import HELP, Command
from abl.patterns import BAR, DRUM_BEATS, DRUM_STYLES, render_bass, render_drums, render_keys
from abl.session import Session, SessionError, Track
from abl.theory import ChordError, parse_progression, scale_chord
from abl.wire import LiveCommandError

FADER_STEP = 0.05
STAB_STYLES = ("house", "techno")
SUB_RANGE = (24, 35)
BASS_RANGE = (36, 47)
DEFAULT_STYLE = "house"
DEFAULT_KEYS_STYLE = "lofi"
RACE_MSG = "Live added a track while abl was working, so the change was reverted. Try again."


def _has_device(track: Track | None, sound: Sound) -> bool:
    if track is None:
        return False
    wanted = sound.name.lower()
    return any(wanted == d.lower() or wanted == d.lower().removesuffix(".adg").removesuffix(".adv") for d in track.devices)


def _instrument_name(track: Track | None) -> str | None:
    return track.devices[0] if track and track.devices else None


def _run_batch(session: Session, commands: list[dict], role: str | None = None) -> list[dict]:
    try:
        return session.batch(commands)
    except SessionError as exc:
        raise ActionError(str(exc)) from None


def _write_clip(session: Session, role: str, sound: Sound, length: float, notes: list[dict], clip_name: str, description: str, bpm: float | None = None) -> str:
    """One batch: (create + name), tempo, load, (delete own clip), create clip, notes, loop, name, fire."""
    index, created = session.plan_role_track(role)
    track = None if created else session.find_track(role)
    slot, existing = (0, False) if created else session.locate_slot(role, index)
    load = created or not _has_device(track, sound)
    replaced = _instrument_name(track) if load and not created else None
    name = f"abl {clip_name}"

    commands: list[dict] = []
    if created:
        commands += [
            {"type": "create_midi_track", "params": {"index": -1}},
            {"type": "set_track_name", "params": {"track_index": index, "name": catalog.ROLE_TRACK_NAMES[role]}},
        ]
    if bpm is not None:
        commands.append({"type": "set_tempo", "params": {"tempo": bpm}})
    if load:
        commands.append({"type": "load_browser_item", "params": {"track_index": index, "item_uri": sound.uri}})
    if existing:
        commands.append({"type": "delete_clip", "params": {"track_index": index, "clip_index": slot}})
    commands += [
        {"type": "create_clip", "params": {"track_index": index, "clip_index": slot, "length": float(length)}},
        {"type": "add_notes_to_clip", "params": {"track_index": index, "clip_index": slot, "notes": notes}},
        {"type": "set_clip_loop", "params": {"track_index": index, "clip_index": slot, "start": 0.0, "end": float(length), "looping": True}},
        {"type": "set_clip_name", "params": {"track_index": index, "clip_index": slot, "name": name}},
        {"type": "fire_clip", "params": {"track_index": index, "clip_index": slot}},
    ]
    results = _run_batch(session, commands, role)
    if created:
        got = (results[0].get("result") or {}).get("index") if results else None
        if got is not None and int(got) != index:
            session.client.send("undo")
            raise ActionError(RACE_MSG)
        session.record_created(role, index)
        session.refresh()  # pins ownership to the new track's id
    session.remember_clip(role, slot, name, description)
    note = f" (replaced {replaced})" if replaced else ""
    return f"{catalog.ROLE_TRACK_NAMES[role]}: {description} on {sound.name}, slot {slot}{note}"


# -- drums -------------------------------------------------------------------

def _drum_notes(style: str, hats: str, swing: int | None) -> tuple[Sound, list[dict]]:
    kit = kit_for_style(style)
    notes = render_drums(style, pad_map(kit.name), hats=hats, swing=swing)
    return kit, notes


def beat(session: Session, style: str, bpm: float | None = None) -> str:
    session.refresh()
    kit, notes = _drum_notes(style, "normal", None)
    line = _write_clip(session, "drums", kit, DRUM_BEATS, notes, style, f"{style} beat, 2 bars", bpm=bpm)
    session.style, session.hats, session.swing = style, "normal", None
    if bpm is not None:
        return f"{line}, {bpm:g} bpm"
    return f"{line} (tempo stays {session.tempo:g}; {style} is usually {DRUM_STYLES[style].tempo_hint})"


def drums(session: Session, style: str) -> str:
    return beat(session, style, None)


def _rewrite_drums(session: Session, hats_mode: str, swing_pct: int | None, what: str) -> str:
    if session.style is None:
        raise ActionError("no abl beat yet; run `beat <style>` first")
    session.refresh()
    if not session.verify_clip("drums"):
        raise ActionError("the abl drum clip is gone or was replaced; run `beat <style>` again")
    index, slot = session.clip_for("drums")
    _, notes = _drum_notes(session.style, hats_mode, swing_pct)
    _run_batch(session, [{"type": "add_notes_to_clip", "params": {"track_index": index, "clip_index": slot, "notes": notes}}])
    session.hats, session.swing = hats_mode, swing_pct
    return f"Drums: {session.style} rewritten with {what}"


def swing(session: Session, pct: int) -> str:
    return _rewrite_drums(session, session.hats, pct, f"swing {pct}%")


def hats(session: Session, mode: str) -> str:
    return _rewrite_drums(session, mode, session.swing, f"hats {mode}")


# -- bass / keys -------------------------------------------------------------------

def bass(session: Session, sound: str | None, style: str | None) -> str:
    session.refresh()
    style = style or session.style or DEFAULT_STYLE
    chosen = catalog.sound("bass", sound) if sound else catalog.default_sound("bass", style)
    low, high = SUB_RANGE if "808" in chosen.name else BASS_RANGE
    if session.progression:
        chords = session.progression
        source = "the keys progression"
    else:
        info = session.info()
        chord = scale_chord(int(info.get("root_note", 0)), str(info.get("scale_name", "Major")))
        chords = [chord, chord]
        source = f"Live's key ({chord.symbol})"
    notes = render_bass(style, chords, low, high)
    return _write_clip(session, "bass", chosen, len(chords) * BAR, notes, f"bass {style}", f"{style} bass over {len(chords)} bars from {source}")


def keys(session: Session, sound: str | None, progression: str, mode: str | None) -> str:
    session.refresh()
    try:
        chords = parse_progression(progression)
    except ChordError as exc:
        raise ActionError(str(exc)) from None
    style = session.style
    chosen = catalog.sound("keys", sound) if sound else catalog.default_sound("keys", style or DEFAULT_KEYS_STYLE)
    mode = mode or ("stab" if style in STAB_STYLES else "hold")
    notes = render_keys(chords, mode)
    symbols = "-".join(c.symbol for c in chords)
    line = _write_clip(session, "keys", chosen, len(chords) * BAR, notes, f"keys {symbols}", f"{symbols}, {len(chords)} bars, {mode}")
    session.progression = chords
    return line


# -- transport ---------------------------------------------------------------------

def tempo(session: Session, bpm: float) -> str:
    session.client.send("set_tempo", {"tempo": bpm})
    return f"Tempo: {bpm:g} bpm"


def _fire_commands(session: Session) -> tuple[list[dict], list[str]]:
    fires, roles = [], []
    for role in session.remembered_roles():
        clip = session.clip_for(role)
        if clip:
            fires.append({"type": "fire_clip", "params": {"track_index": clip[0], "clip_index": clip[1]}})
            roles.append(role)
    return fires, roles


def go(session: Session) -> str:
    session.refresh()
    fires, roles = _fire_commands(session)
    if fires:
        try:
            _run_batch(session, fires + [{"type": "start_playback", "params": {}}])
            return "Playing: " + ", ".join(roles)
        except LiveCommandError as exc:
            if "no clip in slot" not in str(exc).lower():
                raise
            for role in list(roles):  # something abl wrote was undone or deleted; drop it and retry once
                session.verify_clip(role)
            fires, roles = _fire_commands(session)
            if fires:
                _run_batch(session, fires + [{"type": "start_playback", "params": {}}])
                return "Playing: " + ", ".join(roles)
    session.client.send("start_playback")
    return "Playing (no abl clips to fire)"


def stop(session: Session) -> str:
    session.client.send("stop_playback")
    return "Stopped"


# -- mixer ---------------------------------------------------------------------------

def _target_track(session: Session, target: str) -> Track:
    session.refresh()
    track = session.find_track(target)
    if track is None:
        names = ", ".join(f"{t.index}:{t.name}" for t in session.tracks)
        raise ActionError(f"no track {target!r}; tracks: {names}")
    return track


def _mute(session: Session, target: str, mute: bool) -> str:
    track = _target_track(session, target)
    session.client.send("set_track_mute", {"track_index": track.index, "mute": mute})
    return f"{track.name}: {'muted' if mute else 'unmuted'}"


def _solo(session: Session, target: str, solo: bool) -> str:
    track = _target_track(session, target)
    session.client.send("set_track_solo", {"track_index": track.index, "solo": solo})
    return f"{track.name}: {'solo' if solo else 'unsolo'}"


def _level(session: Session, target: str, steps: int, direction: int) -> str:
    track = _target_track(session, target)
    volume = round(min(1.0, max(0.0, track.volume + direction * FADER_STEP * steps)), 3)
    session.client.send("set_track_volume", {"track_index": track.index, "volume": volume})
    return f"{track.name}: fader {track.volume:.2f} -> {volume:.2f}"


# -- clean-up ----------------------------------------------------------------------

def clear(session: Session, role: str) -> str:
    session.refresh()
    clip = session.clip_for(role)
    if clip is None:
        raise ActionError(f"abl has no {role} clip to clear")
    if not session.verify_clip(role):
        return f"{catalog.ROLE_TRACK_NAMES[role]}: abl's clip in slot {clip[1]} was already gone"
    session.client.send("delete_clip", {"track_index": clip[0], "clip_index": clip[1]})
    session.forget_clip(role)
    return f"{catalog.ROLE_TRACK_NAMES[role]}: cleared slot {clip[1]}"


def kill(session: Session, role: str) -> str:
    session.refresh()
    track = session.owned_track(role)
    if track is None:
        if session.owns(role):
            session.disown(role)
            session.forget_clip(role)
        raise ActionError(
            f"abl did not create the current {catalog.ROLE_TRACK_NAMES[role]} track (or the one it made is gone); delete it in Live yourself"
        )
    session.client.send("delete_track", {"track_index": track.index})
    session.forget_clip(role)
    session.disown(role)
    return f"{track.name}: deleted"


# -- info ----------------------------------------------------------------------------

def status(session: Session) -> str:
    session.refresh()
    info = session.info()
    lines = [
        f"{session.tempo:g} bpm, {'playing' if session.is_playing else 'stopped'}, {len(session.tracks)} tracks, "
        f"key {info.get('root_note', '?')} {info.get('scale_name', '?')}"
    ]
    for role in session.remembered_roles():
        clip = session.clip_for(role)
        where = f"track {clip[0]} slot {clip[1]}" if clip else "track missing"
        lines.append(f"  {role}: {session.clip_description(role)} ({where})")
    if not session.remembered_roles():
        lines.append("  no abl clips yet; try: beat trap 140")
    return "\n".join(lines)


def tracks(session: Session) -> str:
    session.refresh()
    rows = []
    for t in session.tracks:
        flags = ("M" if t.muted else "") + ("S" if t.soloed else "")
        rows.append(f"{t.index:2d} {t.name:<20} [{', '.join(t.devices) or '-'}] {flags}".rstrip())
    return "\n".join(rows)


def help_(session: Session) -> str:
    return HELP


def catalog_rescan(session: Session, progress=None) -> str:
    from abl import library

    entries = library.rescan(session.client, progress or (lambda line: None))
    sections = {}
    for entry in entries:
        sections[entry["section"]] = sections.get(entry["section"], 0) + 1
    return f"Catalog: {len(entries)} sounds (" + ", ".join(f"{k} {v}" for k, v in sorted(sections.items())) + f") saved to {library.USER_CATALOG}"


def import_audio(session: Session, source: str, progress=None) -> str:
    from abl import importer

    return importer.import_song(session, source, progress or (lambda line: None))


def recreate(session: Session, source: str, fresh: bool, progress=None) -> str:
    report_progress = progress or (lambda line: None)
    analysis = recreate_mod.run_analyzer(source, fresh, report_progress)
    return recreate_mod.push(session, analysis, report_progress)


def analyze(session: Session, source: str, fresh: bool, progress=None) -> str:
    analysis = recreate_mod.run_analyzer(source, fresh, progress or (lambda line: None))
    return recreate_mod.report(analysis)


HANDLERS = {
    "beat": beat,
    "drums": drums,
    "bass": bass,
    "keys": keys,
    "tempo": tempo,
    "go": go,
    "stop": stop,
    "mute": lambda s, target: _mute(s, target, True),
    "unmute": lambda s, target: _mute(s, target, False),
    "solo": lambda s, target: _solo(s, target, True),
    "unsolo": lambda s, target: _solo(s, target, False),
    "louder": lambda s, target, steps: _level(s, target, steps, +1),
    "quieter": lambda s, target, steps: _level(s, target, steps, -1),
    "swing": swing,
    "hats": hats,
    "clear": clear,
    "kill": kill,
    "undo": lambda s: (s.client.send("undo"), "Undone")[1],
    "redo": lambda s: (s.client.send("redo"), "Redone")[1],
    "status": status,
    "tracks": tracks,
    "help": help_,
    "recreate": recreate,
    "analyze": analyze,
    "catalog": catalog_rescan,
    "import": import_audio,
}
PROGRESS_HANDLERS = {"recreate", "analyze", "catalog", "import"}


def execute(command: Command, session: Session, progress=None) -> str:
    handler = HANDLERS[command.name]
    extra = {"progress": progress} if command.name in PROGRESS_HANDLERS else {}
    try:
        return handler(session, **command.args, **extra)
    except (SessionError, catalog.CatalogError) as exc:
        raise ActionError(str(exc)) from None
