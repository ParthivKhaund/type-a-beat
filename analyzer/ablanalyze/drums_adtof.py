"""Drum transcription with ADTOF (Zehren et al.), run in its own environment because it needs TensorFlow."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ADTOF_TO_LIVE = {35: 36, 36: 36, 38: 38, 40: 38, 37: 38, 42: 42, 44: 42, 46: 46, 47: 47, 45: 47, 48: 47, 43: 47, 49: 49, 51: 49, 57: 49}
ENV_DIR = Path(__file__).resolve().parent.parent / ".venv-adtof"
SCRIPT = """
import os, sys
from adtof.model.model import Model
model, hparams = Model.modelFactory(modelName="Frame_RNN", scenario="adtofAll", fold=0)
model.predictFolder(sys.argv[1], sys.argv[2], writeMidi=False, **hparams)
"""


def available() -> bool:
    return (ENV_DIR / "bin" / "python").exists()


def parse_adtof(text: str) -> list[tuple[float, int]]:
    hits = []
    for line in text.splitlines():
        parts = line.split()
        if len(parts) < 2 or line.lstrip().startswith("#"):
            continue
        try:
            t, pitch = float(parts[0]), int(float(parts[1]))
        except ValueError:
            continue
        if pitch in ADTOF_TO_LIVE:
            hits.append((t, ADTOF_TO_LIVE[pitch]))
    return hits


def transcribe_drums(stem: Path, work_dir: Path) -> list[tuple[float, int]]:
    """(time_s, live_pitch) hits, or raises RuntimeError."""
    inputs, outputs = work_dir / "adtof_in", work_dir / "adtof_out"
    shutil.rmtree(inputs, ignore_errors=True)
    shutil.rmtree(outputs, ignore_errors=True)
    inputs.mkdir(parents=True)
    shutil.copy(stem, inputs / "drums.wav")
    env = {k: v for k, v in os.environ.items() if not k.startswith("VIRTUAL_ENV")}
    env["TF_CPP_MIN_LOG_LEVEL"] = "3"
    env["TF_USE_LEGACY_KERAS"] = "True"  # ADTOF's model uses Keras 2 optimizers
    result = subprocess.run([str(ENV_DIR / "bin" / "python"), "-c", SCRIPT, str(inputs / "drums.wav"), str(outputs)], capture_output=True, text=True, timeout=1800, env=env)
    out_file = next(iter(outputs.glob("*.txt")), None) if outputs.exists() else None
    if result.returncode != 0 or out_file is None:
        tail = (result.stderr.strip().splitlines() or ["adtof failed"])[-1]
        raise RuntimeError(tail)
    return parse_adtof(out_file.read_text())
