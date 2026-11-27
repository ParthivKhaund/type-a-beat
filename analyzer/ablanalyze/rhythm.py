"""Beats, downbeats, and the beat grid everything else is measured on."""

from __future__ import annotations

from bisect import bisect_right
from dataclasses import dataclass

import numpy as np

SIXTEENTH = 0.25
LOW_BAND = (20.0, 150.0)


def quantize(value: float, step: float = SIXTEENTH) -> float:
    return round(round(value / step) * step, 6)


def choose_downbeat_phase(energies: list[float], beats_per_bar: int = 4) -> int:
    if len(energies) < beats_per_bar:
        return 0
    sums = [sum(energies[phase::beats_per_bar]) for phase in range(beats_per_bar)]
    return int(np.argmax(sums))


@dataclass
class Grid:
    beat_times: list[float]
    first_downbeat: int = 0

    @property
    def _first_period(self) -> float:
        return self.beat_times[1] - self.beat_times[0] if len(self.beat_times) > 1 else 0.5

    @property
    def _last_period(self) -> float:
        return self.beat_times[-1] - self.beat_times[-2] if len(self.beat_times) > 1 else 0.5

    @property
    def tempo(self) -> float:
        if len(self.beat_times) < 2:
            return 120.0
        return float(60.0 / np.median(np.diff(self.beat_times)))

    def time_to_beats(self, t: float) -> float:
        bt = self.beat_times
        if len(bt) < 2:
            return 0.0
        if t <= bt[0]:
            beats = (t - bt[0]) / self._first_period
        elif t >= bt[-1]:
            beats = (len(bt) - 1) + (t - bt[-1]) / self._last_period
        else:
            i = bisect_right(bt, t) - 1
            beats = i + (t - bt[i]) / (bt[i + 1] - bt[i])
        return beats - self.first_downbeat

    def beats_to_time(self, beats: float) -> float:
        bt = self.beat_times
        b = beats + self.first_downbeat
        if len(bt) < 2:
            return 0.0
        if b <= 0:
            return bt[0] + b * self._first_period
        if b >= len(bt) - 1:
            return bt[-1] + (b - (len(bt) - 1)) * self._last_period
        i = int(b)
        return bt[i] + (b - i) * (bt[i + 1] - bt[i])

    def total_bars(self, duration_s: float, beats_per_bar: int = 4) -> int:
        return max(1, int(self.time_to_beats(duration_s) // beats_per_bar))


def track_beats(y: np.ndarray, sr: int) -> tuple[float, list[float]]:
    import librosa

    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units="time", trim=False)
    tempo_value = float(np.atleast_1d(tempo)[0])
    return tempo_value, [float(b) for b in beats]


def low_band_energy_at(y: np.ndarray, sr: int, times: list[float], window_s: float = 0.08) -> list[float]:
    """Energy in the kick band in a short window after each beat time."""
    energies = []
    half = int(window_s * sr)
    for t in times:
        start = max(0, int(t * sr) - half // 4)
        segment = y[start:start + half]
        if len(segment) < 64:
            energies.append(0.0)
            continue
        spectrum = np.abs(np.fft.rfft(segment * np.hanning(len(segment)))) ** 2
        freqs = np.fft.rfftfreq(len(segment), 1.0 / sr)
        band = (freqs >= LOW_BAND[0]) & (freqs < LOW_BAND[1])
        energies.append(float(spectrum[band].sum()))
    return energies


def grid_from_downbeats(beats: list[float], downbeats: list[float]) -> Grid:
    """A grid whose bar 0 starts on the beat nearest the first model downbeat."""
    beats = [float(b) for b in beats]
    if not beats:
        return Grid([0.0, 0.5], 0)
    if not downbeats:
        return Grid(beats, 0)
    first = float(downbeats[0])
    nearest = min(range(len(beats)), key=lambda i: abs(beats[i] - first))
    return Grid(beats, nearest)


def extend_to_start(grid: Grid, beats_per_bar: int = 4) -> Grid:
    """Prepend whole bars of virtual beats so bar 0 starts at the audio start, not at the first detected downbeat.
    Drum-less intros and pickups otherwise fall before bar 0 and are dropped."""
    if len(grid.beat_times) < 2:
        return grid
    first = grid.beat_times[grid.first_downbeat]
    period = grid._first_period
    bar = period * beats_per_bar
    bars_before = int((first + 0.25 * period) // bar)
    if bars_before <= 0:
        return grid
    extra = bars_before * beats_per_bar
    prepended = [grid.beat_times[0] - period * n for n in range(extra, 0, -1)]
    return Grid(prepended + list(grid.beat_times), grid.first_downbeat)  # same index: bar 0 moves to the audio start
