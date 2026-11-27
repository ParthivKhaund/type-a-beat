"""Chord recognition by chroma templates with Viterbi smoothing, and key detection."""

from __future__ import annotations

import numpy as np

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
QUALITIES = {"": (0, 4, 7), "m": (0, 3, 7), "7": (0, 4, 7, 10)}
TEMPLATE_NAMES = [f"{NOTE_NAMES[r]}{q}" for r in range(12) for q in QUALITIES]
EMISSION_GAIN = 10.0
STAY_PROBABILITY = 0.85
ROOT_WEIGHT = 2.0  # the root counts double, so Am (A C E) and F (F A C) separate on the bass note

MAJOR_PROFILE = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MINOR_PROFILE = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])


def _parse(symbol: str) -> tuple[int, str]:
    root = NOTE_NAMES.index(symbol[:2]) if symbol[1:2] == "#" else NOTE_NAMES.index(symbol[:1])
    quality = symbol[2:] if symbol[1:2] == "#" else symbol[1:]
    return root, quality


def template_vector(symbol: str) -> np.ndarray:
    root, quality = _parse(symbol)
    vector = np.zeros(12)
    for interval in QUALITIES[quality]:
        vector[(root + interval) % 12] = ROOT_WEIGHT if interval == 0 else 1.0
    return vector


TEMPLATES = np.array([template_vector(name) for name in TEMPLATE_NAMES])
TEMPLATES_UNIT = TEMPLATES / np.linalg.norm(TEMPLATES, axis=1, keepdims=True)


def score_frames(chroma: np.ndarray) -> np.ndarray:
    """Cosine similarity of every frame [T, 12] against every template -> [T, 36]."""
    frames = np.asarray(chroma, dtype=float)
    norms = np.linalg.norm(frames, axis=1, keepdims=True) + 1e-9
    return (frames / norms) @ TEMPLATES_UNIT.T


def viterbi(scores: np.ndarray, stay: float = STAY_PROBABILITY) -> list[int]:
    frames, states = scores.shape
    if frames == 0:
        return []
    emission = EMISSION_GAIN * scores
    log_stay = np.log(stay)
    log_switch = np.log((1.0 - stay) / max(states - 1, 1))
    best = emission[0].copy()
    back = np.zeros((frames, states), dtype=int)
    for t in range(1, frames):
        stay_score = best + log_stay
        switch_from = int(np.argmax(best))
        switch_score = best[switch_from] + log_switch
        choose_stay = stay_score >= switch_score
        back[t] = np.where(choose_stay, np.arange(states), switch_from)
        best = np.where(choose_stay, stay_score, switch_score) + emission[t]
    path = [int(np.argmax(best))]
    for t in range(frames - 1, 0, -1):
        path.append(int(back[t][path[-1]]))
    return path[::-1]


def chords_per_beat(chroma: np.ndarray) -> list[str]:
    return [TEMPLATE_NAMES[i] for i in viterbi(score_frames(chroma))]


def chords_per_bar(beat_symbols: list[str], beats_per_bar: int = 4) -> list[str]:
    bars = []
    for start in range(0, len(beat_symbols), beats_per_bar):
        chunk = beat_symbols[start:start + beats_per_bar]
        counts: dict[str, int] = {}
        for symbol in chunk:
            counts[symbol] = counts.get(symbol, 0) + 1
        bars.append(max(counts, key=lambda s: counts[s]))  # dict order breaks ties by first seen
    return bars


def detect_key(chroma_sum: np.ndarray) -> tuple[int, str, float]:
    vector = np.asarray(chroma_sum, dtype=float)
    best = (0, "Major", -2.0)
    for scale, profile in (("Major", MAJOR_PROFILE), ("Minor", MINOR_PROFILE)):
        for root in range(12):
            corr = float(np.corrcoef(vector, np.roll(profile, root))[0, 1])
            if corr > best[2]:
                best = (root, scale, corr)
    root, scale, corr = best
    return root, scale, float(max(0.0, min(1.0, corr)))


def key_name(root: int, scale: str) -> str:
    return f"{NOTE_NAMES[root % 12]} {scale.lower()}"
