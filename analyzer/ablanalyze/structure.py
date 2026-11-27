"""Sections, beats, and downbeats from All-In-One (Kim & Nam 2023) through the NATTEN shim."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Callable

from ablanalyze import natten_shim

DEMUCS_STEMS = ("bass", "drums", "other", "vocals")


def available() -> bool:
    try:
        natten_shim.install()
        import allin1  # noqa: F401
    except Exception:
        return False
    return True


def _seed_demix(audio: Path, stems: dict[str, Path], demix_dir: Path) -> None:
    target = demix_dir / "htdemucs" / audio.stem
    target.mkdir(parents=True, exist_ok=True)
    for name in DEMUCS_STEMS:
        link = target / f"{name}.wav"
        if not link.exists() and name in stems:
            os.symlink(stems[name].resolve(), link)


def analyze_structure(audio: Path, stems: dict[str, Path], folder: Path, progress: Callable[[str], None], device: str = "cpu") -> dict | None:
    """{"tempo", "beats", "downbeats", "segments": [{"start", "end", "label"}]} in seconds, or None on failure."""
    if not available():
        return None
    import allin1

    demix_dir, spec_dir = folder / "demix", folder / "spec"
    _seed_demix(audio, stems, demix_dir)
    try:
        result = allin1.analyze(str(audio), demix_dir=str(demix_dir), spec_dir=str(spec_dir), device=device, keep_byproducts=True, multiprocess=False)
    except Exception as exc:
        progress(f"structure: All-In-One failed ({str(exc)[:80]}); falling back")
        return None
    return {
        "tempo": float(result.bpm),
        "beats": [float(b) for b in result.beats],
        "downbeats": [float(b) for b in result.downbeats],
        "segments": [{"start": float(s.start), "end": float(s.end), "label": str(s.label)} for s in result.segments],
    }
