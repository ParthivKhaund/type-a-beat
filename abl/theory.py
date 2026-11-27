"""Chord symbols, pitch classes, and voicings. Pure functions, no Live access."""

from __future__ import annotations

import re
from dataclasses import dataclass


class ChordError(ValueError):
    """A chord symbol or progression could not be parsed."""


NOTE_PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

MAJOR = (0, 4, 7)
MINOR = (0, 3, 7)

QUALITIES: dict[str, tuple[int, ...]] = {
    "": MAJOR, "maj": MAJOR, "M": MAJOR,
    "m": MINOR, "min": MINOR, "-": MINOR,
    "maj7": (0, 4, 7, 11), "M7": (0, 4, 7, 11), "Δ": (0, 4, 7, 11), "Δ7": (0, 4, 7, 11),
    "m7": (0, 3, 7, 10), "min7": (0, 3, 7, 10), "-7": (0, 3, 7, 10),
    "7": (0, 4, 7, 10),
    "dim": (0, 3, 6), "°": (0, 3, 6),
    "dim7": (0, 3, 6, 9), "°7": (0, 3, 6, 9),
    "m7b5": (0, 3, 6, 10), "ø": (0, 3, 6, 10), "ø7": (0, 3, 6, 10),
    "sus2": (0, 2, 7), "sus4": (0, 5, 7), "sus": (0, 5, 7),
    "6": (0, 4, 7, 9), "m6": (0, 3, 7, 9),
    "add9": (0, 4, 7, 14), "madd9": (0, 3, 7, 14),
    "9": (0, 4, 7, 10, 14), "maj9": (0, 4, 7, 11, 14), "M9": (0, 4, 7, 11, 14),
    "m9": (0, 3, 7, 10, 14), "min9": (0, 3, 7, 10, 14),
    "aug": (0, 4, 8), "+": (0, 4, 8),
}

_CHORD_RE = re.compile(r"^([A-Ga-g])([#b]?)(.*?)(?:/([A-Ga-g])([#b]?))?$")
_PROGRESSION_SPLIT = re.compile(r"[\s,\-]+")
_ACCIDENTAL = {"": 0, "#": 1, "b": -1}


@dataclass(frozen=True)
class Chord:
    symbol: str
    root: int
    quality: str
    intervals: tuple[int, ...]
    bass: int | None = None


def _pitch_class(letter: str, accidental: str) -> int:
    return (NOTE_PC[letter.upper()] + _ACCIDENTAL[accidental]) % 12


def parse_chord(symbol: str) -> Chord:
    match = _CHORD_RE.match(symbol.strip())
    if not match:
        raise ChordError(f"not a chord symbol: {symbol!r}")
    letter, accidental, quality, bass_letter, bass_accidental = match.groups()
    if quality not in QUALITIES:
        raise ChordError(f"unknown chord quality {quality!r} in {symbol!r}")
    bass = _pitch_class(bass_letter, bass_accidental or "") if bass_letter else None
    return Chord(
        symbol=symbol.strip(),
        root=_pitch_class(letter, accidental),
        quality=quality,
        intervals=QUALITIES[quality],
        bass=bass,
    )


def parse_progression(text: str) -> list[Chord]:
    tokens = [t for t in _PROGRESSION_SPLIT.split(text.strip()) if t]
    if not tokens:
        raise ChordError("empty progression")
    return [parse_chord(t) for t in tokens]


def scale_chord(root: int, scale_name: str) -> Chord:
    """Triad implied by Live's current root note and scale name."""
    lowered = scale_name.lower()
    is_minor = "minor" in lowered or lowered in {"dorian", "aeolian", "phrygian"}
    symbol = spell(root % 12) + ("m" if is_minor else "")
    return Chord(symbol=symbol, root=root % 12, quality="m" if is_minor else "", intervals=MINOR if is_minor else MAJOR)


def spell(pitch_class: int) -> str:
    """Name a pitch class with sharps: 0 -> C, 6 -> F#, 10 -> A#."""
    for name, value in NOTE_PC.items():
        if value == pitch_class:
            return name
    return next(name + "#" for name, value in NOTE_PC.items() if (value + 1) % 12 == pitch_class)


def _fold(pitch: int, low: int, high: int) -> int:
    while pitch > high:
        pitch -= 12
    while pitch < low:
        pitch += 12
    return pitch


def bass_pitch(chord: Chord, low: int, high: int) -> int:
    pitch_class = chord.bass if chord.bass is not None else chord.root
    return _fold(low + (pitch_class - low) % 12, low, high)


def candidate_voicings(chord: Chord, low: int = 55, high: int = 76) -> list[list[int]]:
    """Every inversion of the close voicing, at every octave that fits in [low, high]."""
    base = [chord.root + i for i in chord.intervals]
    inversions = []
    for k in range(len(base)):
        inv = base[k:] + [p + 12 for p in base[:k]]
        inversions.append(inv)
    found: list[list[int]] = []
    for inv in inversions:
        for octave in range(-1, 9):
            shifted = sorted(p + 12 * octave for p in inv)
            if shifted[0] >= low and shifted[-1] <= high and shifted not in found:
                found.append(shifted)
    if not found:
        lowest = sorted(base)[0]
        offset = 12 * ((low - lowest + 11) // 12)
        found.append(sorted(p + offset for p in base))
    return found


def movement(prev: list[int], nxt: list[int]) -> int:
    a, b = sorted(prev), sorted(nxt)
    if len(a) == len(b):
        return sum(abs(x - y) for x, y in zip(a, b))
    short, long_ = (a, b) if len(a) < len(b) else (b, a)
    return sum(min(abs(x - y) for y in long_) for x in short)


def voice(chord: Chord, prev: list[int] | None, low: int = 55, high: int = 76) -> list[int]:
    candidates = candidate_voicings(chord, low, high)
    center = (low + high) / 2

    def closeness(v: list[int]) -> float:
        return abs(sum(v) / len(v) - center)

    if prev is None:
        return min(candidates, key=closeness)
    return min(candidates, key=lambda v: (movement(prev, v), closeness(v)))
