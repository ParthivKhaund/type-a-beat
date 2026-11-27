"""Drum lanes, bass patterns, and keys rhythms per style, rendered to note dicts."""

from __future__ import annotations

from dataclasses import dataclass, field

from abl.theory import Chord, bass_pitch, voice

VELOCITY = {"x": 118, "o": 96, "g": 55}
SIXTEENTH = 0.25
BAR = 4.0
DRUM_BARS = 2
DRUM_BEATS = BAR * DRUM_BARS
HIT_DURATION = 0.25
HAT_MODES = ("normal", "double", "half", "off")


def _note(pitch: int, start: float, duration: float, velocity: int) -> dict:
    return {
        "pitch": pitch,
        "start_time": round(start, 4),
        "duration": round(duration, 4),
        "velocity": velocity,
        "mute": False,
    }


SWING_GRIDS = (SIXTEENTH, SIXTEENTH / 2)


def _swing_offset(start: float, swing: float, step: float) -> float:
    """MPC-style swing on 16th and 32nd grids: off-16ths move later; 32nds between them move half as far."""
    if not swing or swing <= 50 or not any(abs(step - grid) < 1e-9 for grid in SWING_GRIDS):
        return 0.0
    amount = (swing / 100 - 0.5) * 2 * SIXTEENTH
    position = round(start / (SIXTEENTH / 2)) % 4
    if position == 2:
        return amount
    if position in (1, 3):
        return amount / 2
    return 0.0


def lane_to_notes(lane: str, pitch: int, total_beats: float, swing: float = 0.0, duration: float | None = None) -> list[dict]:
    if not lane:
        return []
    step = total_beats / len(lane)
    hit_duration = duration if duration is not None else min(HIT_DURATION, step * 0.9)
    notes = []
    for index, symbol in enumerate(lane):
        if symbol == ".":
            continue
        if symbol not in VELOCITY:
            raise ValueError(f"unknown lane symbol {symbol!r}")
        start = index * step
        start += _swing_offset(start, swing, step)
        notes.append(_note(pitch, start, hit_duration, VELOCITY[symbol]))
    return notes


def hat_variant(lane: str, mode: str) -> str:
    if mode == "normal":
        return lane
    if mode == "double":
        return "".join((c if c != "." else "o") + "o" for c in lane)
    if mode == "half":
        return "".join(c if i % 2 == 0 else "." for i, c in enumerate(lane))
    if mode == "off":
        return ""
    raise ValueError(f"unknown hat mode {mode!r}; use one of {', '.join(HAT_MODES)}")


@dataclass(frozen=True)
class DrumStyle:
    lanes: dict[str, str]
    tempo_hint: str
    swing: float = 0.0


def _bars(*bars: str) -> str:
    return "".join(bars)


DRUM_STYLES: dict[str, DrumStyle] = {
    "trap": DrumStyle(
        tempo_hint="130-160",
        lanes={
            "kick": _bars("x..........x....", "x.....x....x...."),
            "snare": _bars("........x.......", "........x......."),
            "clap": _bars("........o.......", "........o......."),
            "ch": _bars("xooo" * 4, "xooo" * 4),
            "oh": _bars("................", "..............o."),
        },
    ),
    "boombap": DrumStyle(
        tempo_hint="85-95",
        swing=58,
        lanes={
            "kick": _bars("x..x......x.....", "x.........x..x.."),
            "snare": _bars("....x.......x...", "....x.......x..."),
            "ch": _bars("x.o.x.o.x.o.x.o.", "x.o.x.o.x.o.x.o."),
            "oh": _bars("................", "..............o."),
        },
    ),
    "house": DrumStyle(
        tempo_hint="120-128",
        lanes={
            "kick": _bars("x...x...x...x...", "x...x...x...x..."),
            "clap": _bars("....x.......x...", "....x.......x..."),
            "ch": _bars("o.o.o.o.o.o.o.o.", "o.o.o.o.o.o.o.o."),
            "oh": _bars("..x...x...x...x.", "..x...x...x...x."),
        },
    ),
    "techno": DrumStyle(
        tempo_hint="128-140",
        lanes={
            "kick": _bars("x...x...x...x...", "x...x...x...x..."),
            "clap": _bars("....x.......x...", "....x.......x..."),
            "ch": _bars("xooo" * 4, "xooo" * 4),
            "oh": _bars("..o...o...o...o.", "..o...o...o...o."),
            "rim": _bars("..g...g.g...g..g", "..g...g.g...g..g"),
        },
    ),
    "pop": DrumStyle(
        tempo_hint="100-120",
        lanes={
            "kick": _bars("x......x..x.....", "x......x..x.x..."),
            "snare": _bars("....x.......x...", "....x.......x..."),
            "ch": _bars("x.o.x.o.x.o.x.o.", "x.o.x.o.x.o.x.o."),
            "oh": _bars("................", "..............o."),
            "crash": _bars("x...............", "................"),
        },
    ),
    "lofi": DrumStyle(
        tempo_hint="70-90",
        swing=62,
        lanes={
            "kick": _bars("x......x..x.....", "x.....x...x..x.."),
            "snare": _bars("....o.......o...", "....o.......o..."),
            "ch": _bars("o.g.o.g.o.g.o.g.", "o.g.o.g.o.g.o.g."),
            "rim": _bars("......g.......g.", "......g........."),
        },
    ),
    "jazz": DrumStyle(
        tempo_hint="120-200",
        lanes={  # triplet grid: 12 steps per bar
            "ride": _bars("x..o.ox..o.o", "x..o.ox..o.o"),
            "ch": _bars("...x.....x..", "...x.....x.."),
            "kick": _bars("g.....g.....", "g.....g....."),
            "snare": _bars(".....g......", "..........g."),
        },
    ),
}

STYLE_ALIASES = {"swing": "jazz", "hiphop": "boombap", "boom": "boombap", "bap": "boombap"}


def normalize_style(name: str) -> str:
    key = name.lower().replace("-", "").replace(" ", "")
    key = STYLE_ALIASES.get(key, key)
    if key not in DRUM_STYLES:
        raise KeyError(name)
    return key


def render_drums(style: str, pad_map: dict[str, int], hats: str = "normal", swing: float | None = None) -> list[dict]:
    drum_style = DRUM_STYLES[normalize_style(style)]
    lanes = dict(drum_style.lanes)
    if hats == "off":
        lanes.pop("ch", None)
        lanes.pop("oh", None)
    elif "ch" in lanes:
        lanes["ch"] = hat_variant(lanes["ch"], hats)
    else:
        hat_variant("", hats)
    amount = drum_style.swing if swing is None else swing
    notes: list[dict] = []
    for lane_name, lane in lanes.items():
        pitch = pad_map.get(lane_name)
        if pitch is None:
            continue
        notes.extend(lane_to_notes(lane, pitch, DRUM_BEATS, swing=amount))
    return sorted(notes, key=lambda n: (n["start_time"], n["pitch"]))


@dataclass(frozen=True)
class BassStyle:
    events: tuple[tuple[float, float, str], ...]
    cycle_bars: int = 1


BASS_STYLES: dict[str, BassStyle] = {
    "trap": BassStyle(cycle_bars=2, events=((0, 2.75, "root"), (2.75, 1.25, "root"), (4, 1.5, "root"), (5.5, 1.25, "root"), (6.75, 1.25, "root"))),
    "boombap": BassStyle(events=((0, 0.7, "root"), (0.75, 1.7, "root"), (2.5, 0.9, "5"), (3.5, 0.45, "root"))),
    "house": BassStyle(events=((0.5, 0.4, "root"), (1.5, 0.4, "root"), (2.5, 0.4, "root"), (3.5, 0.4, "root"))),
    "techno": BassStyle(events=tuple((i * 0.5, 0.25, "root") for i in range(8))),
    "pop": BassStyle(events=tuple((i * 0.5, 0.45, "root") for i in range(8))),
    "lofi": BassStyle(events=((0, 1.4, "root"), (1.5, 0.9, "root"), (2.5, 1.2, "5"), (3.75, 0.2, "root"))),
    "jazz": BassStyle(events=((0, 1, "root"), (1, 1, "3"), (2, 1, "5"), (3, 1, "approach"))),
}


def _fold(pitch: int, low: int, high: int) -> int:
    while pitch > high:
        pitch -= 12
    while pitch < low:
        pitch += 12
    return pitch


def _degree_pitch(degree: str, chord: Chord, next_chord: Chord, low: int, high: int) -> int:
    if degree == "root":
        return bass_pitch(chord, low, high)  # honours a slash bass
    if degree == "3":
        return _fold(low + (chord.root + chord.intervals[1] - low) % 12, low, high)
    if degree == "5":
        return _fold(low + (chord.root + chord.intervals[2] - low) % 12, low, high)
    if degree == "approach":
        return _fold(bass_pitch(next_chord, low, high) - 1, low, high)
    raise ValueError(f"unknown degree {degree!r}")


def render_bass(style: str, chords: list[Chord], low: int = 24, high: int = 35, velocity: int = 110) -> list[dict]:
    bass_style = BASS_STYLES[normalize_style(style)]
    total = len(chords) * BAR
    notes: list[dict] = []
    for bar, chord in enumerate(chords):
        next_chord = chords[(bar + 1) % len(chords)]
        cycle_pos = bar % bass_style.cycle_bars
        for start, duration, degree in bass_style.events:
            if not cycle_pos * BAR <= start < (cycle_pos + 1) * BAR:
                continue
            absolute = bar * BAR + (start - cycle_pos * BAR)
            clipped = min(duration, total - absolute)
            notes.append(_note(_degree_pitch(degree, chord, next_chord, low, high), absolute, clipped, velocity))
    return notes


STAB_OFFSETS = (0.5, 1.5, 2.5, 3.5)
HOLD_DURATION = 3.9
STAB_DURATION = 0.3


def render_keys(chords: list[Chord], mode: str = "hold", low: int = 55, high: int = 76, velocity: int = 72) -> list[dict]:
    if mode not in ("hold", "stab"):
        raise ValueError(f"unknown keys mode {mode!r}")
    notes: list[dict] = []
    prev: list[int] | None = None
    for bar, chord in enumerate(chords):
        pitches = voice(chord, prev, low, high)
        prev = pitches
        if mode == "hold":
            notes.extend(_note(p, bar * BAR, HOLD_DURATION, velocity) for p in pitches)
        else:
            for offset in STAB_OFFSETS:
                notes.extend(_note(p, bar * BAR + offset, STAB_DURATION, velocity + 20) for p in pitches)
    return notes
