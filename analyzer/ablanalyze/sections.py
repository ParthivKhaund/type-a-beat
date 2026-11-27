"""Song sections: novelty boundaries on bar-level features, labels, and the Live Lite cap of 8."""

from __future__ import annotations

import numpy as np

MIN_BARS = 4
MAX_SECTIONS = 8
CHORUS_ENERGY = 0.85
QUIET_ENERGY = 0.5
PHRASE_BARS = 4


def boundaries_to_sections(boundaries: list[int], total_bars: int, min_bars: int = MIN_BARS) -> list[tuple[int, int]]:
    starts = [0] + sorted({b for b in boundaries if 0 < b < total_bars})
    spans = [(s, (starts[i + 1] if i + 1 < len(starts) else total_bars) - s) for i, s in enumerate(starts)]
    changed = True
    while changed and len(spans) > 1:
        changed = False
        for i, (start, bars) in enumerate(spans):
            if bars >= min_bars:
                continue
            if i > 0:
                prev_start, prev_bars = spans[i - 1]
                spans[i - 1:i + 1] = [(prev_start, prev_bars + bars)]
            else:
                next_start, next_bars = spans[i + 1]
                spans[i:i + 2] = [(start, bars + next_bars)]
            changed = True
            break
    return spans


def label_sections(spans: list[tuple[int, int]], energies: list[float]) -> list[dict]:
    peak = max(energies) if energies and max(energies) > 0 else 1.0
    normalized = [e / peak for e in energies]
    sections = []
    last = len(spans) - 1
    for i, ((start, bars), energy) in enumerate(zip(spans, normalized)):
        if energy >= CHORUS_ENERGY and i > 0:
            label = "chorus"
        elif i == 0 and energy < QUIET_ENERGY:
            label = "intro"
        elif i == last and energy < QUIET_ENERGY and last > 0:
            label = "outro"
        else:
            label = "verse"
        sections.append({"label": label, "start_bar": int(start), "bars": int(bars), "energy": round(float(energy), 3)})
    return sections


def cap_sections(sections: list[dict], max_n: int = MAX_SECTIONS) -> list[dict]:
    result = [dict(s) for s in sections]
    while len(result) > max_n:
        i = min(range(len(result)), key=lambda k: result[k]["bars"])
        if i > 0:
            keep, gone = result[i - 1], result[i]
            keep["bars"] += gone["bars"]
            keep["energy"] = max(keep["energy"], gone["energy"])
            del result[i]
        else:
            keep, gone = result[1], result[0]
            keep["start_bar"] = gone["start_bar"]
            keep["bars"] += gone["bars"]
            keep["energy"] = max(keep["energy"], gone["energy"])
            del result[0]
    return result


def novelty_boundaries(bar_features: np.ndarray, kernel_bars: int = PHRASE_BARS) -> list[int]:
    """Checkerboard novelty on the bar-level self-similarity matrix; peaks snapped to 4-bar phrases."""
    features = np.asarray(bar_features, dtype=float)
    n = len(features)
    if n < 2 * kernel_bars:
        return []
    unit = features / (np.linalg.norm(features, axis=1, keepdims=True) + 1e-9)
    ssm = unit @ unit.T
    k = kernel_bars
    kernel = np.kron(np.array([[1, -1], [-1, 1]]), np.ones((k, k)))
    novelty = np.zeros(n)
    for b in range(k, n - k):
        novelty[b] = float((ssm[b - k:b + k, b - k:b + k] * kernel).sum())
    threshold = novelty.mean() + 0.5 * novelty.std()
    peaks = [b for b in range(k, n - k) if novelty[b] > threshold and novelty[b] >= novelty[max(0, b - 2):b + 3].max()]
    snapped = []
    for b in peaks:
        nearest = int(round(b / PHRASE_BARS) * PHRASE_BARS)
        candidate = nearest if abs(nearest - b) <= 1 else b
        if candidate not in snapped and 0 < candidate < n:
            snapped.append(candidate)
    return sorted(snapped)


SILENCE_LABELS = {"start", "end"}
MIN_SEGMENT_BARS = 2


def sections_from_segments(segments: list[dict], grid, total_bars: int, beats_per_bar: int = 4) -> list[dict]:
    """All-In-One segments (seconds, labeled) -> contiguous bar-aligned sections, slivers merged, capped at 8."""
    raw = []
    for seg in segments:
        if str(seg.get("label", "")).lower() in SILENCE_LABELS:
            continue
        start_bar = int(round(grid.time_to_beats(float(seg["start"])) / beats_per_bar))
        raw.append((max(0, min(start_bar, total_bars)), str(seg["label"])))
    if not raw:
        return [{"label": "song", "start_bar": 0, "bars": total_bars, "energy": 1.0}]
    raw.sort(key=lambda r: r[0])
    raw[0] = (0, raw[0][1])
    sections: list[dict] = []
    for i, (start, label) in enumerate(raw):
        end = raw[i + 1][0] if i + 1 < len(raw) else total_bars
        bars = end - start
        if bars <= 0:
            continue
        if bars < MIN_SEGMENT_BARS and sections:
            sections[-1]["bars"] += bars
            continue
        sections.append({"label": label, "start_bar": start, "bars": bars, "energy": 1.0})
    if sections and sections[-1]["start_bar"] + sections[-1]["bars"] != total_bars:
        sections[-1]["bars"] = total_bars - sections[-1]["start_bar"]
    return cap_sections(sections)
