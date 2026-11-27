"""Beats and downbeats from Beat This! (Foscarin et al. 2024)."""

from __future__ import annotations

from pathlib import Path


def available() -> bool:
    try:
        import beat_this  # noqa: F401
    except Exception:
        return False
    return True


def track(audio: Path, device: str = "cpu") -> tuple[list[float], list[float]]:
    from beat_this.inference import File2Beats

    beats, downbeats = File2Beats(checkpoint_path="final0", device=device, dbn=False)(str(audio))
    return [float(b) for b in beats], [float(b) for b in downbeats]
