"""Drum hits from the drums stem: onsets classified into kick, snare, hat by band energy."""

from __future__ import annotations

import numpy as np

from ablanalyze.rhythm import Grid, quantize

KICK, SNARE, HAT = 36, 38, 42
BANDS = {"low": (20.0, 150.0), "mid": (150.0, 2500.0), "high": (4000.0, 16000.0)}
KICK_RATIO = 0.40   # share of energy below 150 Hz
HAT_RATIO = 0.60    # share above 4 kHz ...
HAT_MAX_MID = 0.30  # ... with little body in the mid band
WINDOW_S = 0.05
MIN_VELOCITY, VELOCITY_SPAN = 60, 60


def classify_hit(low: float, mid: float, high: float) -> int:
    total = low + mid + high + 1e-12
    if low / total > KICK_RATIO:
        return KICK
    if high / total > HAT_RATIO and mid / total < HAT_MAX_MID:
        return HAT
    return SNARE


def hits_to_notes(hits: list[tuple[float, int, float]], step: float = 0.25) -> list[dict]:
    best: dict[tuple[int, float], float] = {}
    for beat, pitch, strength in hits:
        start = quantize(beat, step)
        if start < 0:
            continue
        key = (pitch, start)
        if key not in best or strength > best[key]:
            best[key] = strength
    notes = []
    for (pitch, start), strength in sorted(best.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        velocity = int(max(1, min(127, round(MIN_VELOCITY + VELOCITY_SPAN * strength))))
        notes.append({"pitch": pitch, "start_time": start, "duration": step, "velocity": velocity})
    return notes


def band_energies(y: np.ndarray, sr: int, t: float) -> tuple[float, float, float]:
    length = int(WINDOW_S * sr)
    start = max(0, int(t * sr))
    segment = y[start:start + length]
    if len(segment) < 64:
        return 0.0, 0.0, 0.0
    spectrum = np.abs(np.fft.rfft(segment * np.hanning(len(segment)))) ** 2
    freqs = np.fft.rfftfreq(len(segment), 1.0 / sr)
    out = []
    for low, high in BANDS.values():
        out.append(float(spectrum[(freqs >= low) & (freqs < high)].sum()))
    return out[0], out[1], out[2]


def detect_hits(y: np.ndarray, sr: int, grid: Grid) -> list[tuple[float, int, float]]:
    import librosa

    envelope = librosa.onset.onset_strength(y=y, sr=sr)
    frames = librosa.onset.onset_detect(onset_envelope=envelope, sr=sr, units="frames", backtrack=False)
    times = librosa.frames_to_time(frames, sr=sr)
    peak = float(envelope.max()) if len(envelope) else 1.0
    hits = []
    for frame, t in zip(frames, times):
        strength = float(envelope[frame] / peak) if peak > 0 else 0.5
        low, mid, high = band_energies(y, sr, float(t))
        if low + mid + high <= 0:
            continue
        hits.append((grid.time_to_beats(float(t)), classify_hit(low, mid, high), strength))
    return hits
