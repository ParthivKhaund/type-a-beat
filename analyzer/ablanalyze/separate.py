"""Stem separation with Demucs (htdemucs) through its Python API; audio I/O via soundfile."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

import numpy as np
import soundfile as sf

STEMS = ("drums", "bass", "other", "vocals")
SIX_STEMS = ("drums", "bass", "other", "vocals", "guitar", "piano")
MODELS = ("htdemucs_6s", "htdemucs")  # six stems first (adds guitar and piano); four-stem fallback


def _device() -> str:
    import torch

    return "mps" if torch.backends.mps.is_available() else "cpu"


def _existing(stems_dir: Path) -> dict[str, Path] | None:
    for names in (SIX_STEMS, STEMS):
        paths = {name: stems_dir / f"{name}.wav" for name in names}
        if all(p.exists() for p in paths.values()):
            return paths
    return None


def separate(audio: Path, folder: Path, progress: Callable[[str], None]) -> dict[str, Path]:
    """Stems by name. Six with htdemucs_6s (drums, bass, other, vocals, guitar, piano), else four."""
    stems_dir = folder / "stems"
    cached = _existing(stems_dir)
    if cached:
        progress(f"stems: cached ({len(cached)} stems)")
        return cached
    import torch
    from demucs.apply import apply_model
    from demucs.pretrained import get_model

    model = None
    for name in MODELS:
        try:
            model = get_model(name)
            break
        except Exception as exc:
            progress(f"stems: {name} unavailable ({str(exc)[:60]})")
    if model is None:
        raise RuntimeError("no Demucs model could be loaded")
    model.eval()
    wav, sr = sf.read(str(audio), dtype="float32", always_2d=True)
    if sr != model.samplerate:
        import librosa

        wav = np.stack([librosa.resample(wav[:, c], orig_sr=sr, target_sr=model.samplerate) for c in range(wav.shape[1])], axis=1)
    if wav.shape[1] == 1:
        wav = np.repeat(wav, 2, axis=1)
    mix = torch.from_numpy(wav.T.copy()).unsqueeze(0)
    ref = mix.mean(1)
    mean, std = ref.mean(), ref.std() + 1e-8
    mix = (mix - mean) / std
    stems_dir.mkdir(parents=True, exist_ok=True)
    for device in (_device(), "cpu"):
        try:
            progress(f"stems: separating with Demucs {len(model.sources)}-stem on {device}")
            with torch.no_grad():
                out = apply_model(model, mix, device=device, shifts=0, split=True, overlap=0.25, progress=False)[0]
            break
        except Exception as exc:  # MPS lacks some ops; fall back to CPU
            if device == "cpu":
                raise
            progress(f"stems: {device} failed ({str(exc)[:60]}); retrying on cpu")
    out = out * std + mean
    paths = {}
    for i, name in enumerate(model.sources):
        paths[name] = stems_dir / f"{name}.wav"
        sf.write(str(paths[name]), out[i].T.cpu().numpy(), model.samplerate)
    progress("stems: " + ", ".join(model.sources))
    return paths


def harmonic_mix(stems: dict[str, Path], folder: Path) -> Path:
    """other + guitar + piano as one file (the four-stem 'other'), for chords and All-In-One."""
    target = folder / "stems" / "other4.wav"
    if target.exists():
        return target
    parts = [stems[n] for n in ("other", "guitar", "piano") if n in stems]
    if len(parts) == 1:
        return parts[0]
    mixed = None
    rate = 44100
    for part in parts:
        wav, rate = sf.read(str(part), dtype="float32", always_2d=True)
        mixed = wav if mixed is None else mixed[: len(wav)] + wav[: len(mixed)]
    sf.write(str(target), mixed, rate)
    return target


def levels(stems: dict[str, Path]) -> dict[str, float]:
    """RMS per stem, for instrument routing."""
    out = {}
    for name, path in stems.items():
        wav, _ = sf.read(str(path), dtype="float32", always_2d=True)
        out[name] = float(np.sqrt((wav ** 2).mean())) if len(wav) else 0.0
    return out
