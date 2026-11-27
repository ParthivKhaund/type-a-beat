"""A synthetic song with known tempo, key, chords, and drum hits, for end-to-end tests."""

from __future__ import annotations

import numpy as np
import soundfile as sf

SR = 44100
TEMPO = 92.0
CHORDS = [("C", [48, 52, 55]), ("Am", [45, 48, 52]), ("F", [41, 45, 48]), ("G", [43, 47, 50])]
BARS = 16
DRUMS_FROM_BAR = 4


def _tone(freq: float, seconds: float, amp: float = 0.2, decay: float = 0.0) -> np.ndarray:
    t = np.arange(int(seconds * SR)) / SR
    env = np.exp(-decay * t) if decay else np.ones_like(t)
    return (amp * env * np.sin(2 * np.pi * freq * t)).astype(np.float32)


def _noise(seconds: float, amp: float, decay: float, highpass: bool) -> np.ndarray:
    rng = np.random.default_rng(1)
    n = int(seconds * SR)
    x = rng.standard_normal(n).astype(np.float32)
    if highpass:
        x = np.diff(x, prepend=0.0).astype(np.float32)
    else:  # a snare is band-limited noise with a body, not flat white noise
        kernel = np.ones(12, dtype=np.float32) / 12
        x = np.convolve(x, kernel, mode="same").astype(np.float32)
        x += 0.6 * np.sin(2 * np.pi * 185.0 * np.arange(n) / SR).astype(np.float32)
    env = np.exp(-decay * np.arange(n) / SR)
    return (amp * env * x / (np.abs(x).max() + 1e-9)).astype(np.float32)


def midi_hz(pitch: int) -> float:
    return 440.0 * 2 ** ((pitch - 69) / 12)


def render(path: str) -> dict:
    beat = 60.0 / TEMPO
    bar = 4 * beat
    total = np.zeros(int(BARS * bar * SR) + SR, dtype=np.float32)

    def add(signal: np.ndarray, at: float) -> None:
        start = int(at * SR)
        end = min(len(total), start + len(signal))
        total[start:end] += signal[: end - start]

    kick = _tone(55.0, 0.25, amp=0.9, decay=18.0)
    snare = _noise(0.2, 0.5, 25.0, highpass=False)
    hat = _noise(0.06, 0.25, 90.0, highpass=True)
    for b in range(BARS):
        name, pitches = CHORDS[b % len(CHORDS)]
        at = b * bar
        for p in pitches:
            add(_tone(midi_hz(p), bar * 0.95, amp=0.12), at)
        add(_tone(midi_hz(pitches[0] - 12), bar * 0.9, amp=0.25), at)  # bass root an octave down
        if b >= DRUMS_FROM_BAR:
            add(kick, at)
            add(kick, at + 2 * beat)
            add(snare, at + beat)
            add(snare, at + 3 * beat)
            for k in range(8):
                add(hat, at + k * beat / 2)
    total /= max(1.0, np.abs(total).max() / 0.9)
    sf.write(path, np.stack([total, total], axis=1), SR)
    return {"tempo": TEMPO, "chords": [c[0] for c in CHORDS], "bars": BARS, "drums_from_bar": DRUMS_FROM_BAR}
