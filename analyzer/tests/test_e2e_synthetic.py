"""Slow: renders a synthetic song and runs the whole pipeline, Demucs included. Run with -m slow."""

import json
import os
from pathlib import Path

import pytest

from ablanalyze.main import analyze
from tests.synth_song import render

pytestmark = pytest.mark.skipif(os.environ.get("ABL_SLOW") != "1", reason="set ABL_SLOW=1 to run the Demucs pipeline")


def test_pipeline_recovers_tempo_key_chords_and_drums(tmp_path):
    song = tmp_path / "song.wav"
    truth = render(str(song))
    lines = []
    cache = Path(os.environ.get("ABL_E2E_CACHE", str(tmp_path / "cache")))  # a fixed dir reuses the Demucs stems
    out = analyze(str(song), cache, fresh=True, progress=lines.append)  # fresh redoes the analysis but keeps cached stems
    data = json.loads(out.read_text())
    print("\n".join(lines))
    assert abs(data["tempo"] - truth["tempo"]) < 2.0 or abs(data["tempo"] - 2 * truth["tempo"]) < 2.0 or abs(data["tempo"] - truth["tempo"] / 2) < 2.0
    assert data["key"]["name"] in ("C major", "A minor")
    symbols = [c["symbol"] for c in data["chords"]][:8]
    expected = (truth["chords"] * 2)[:8]
    matches = sum(1 for a, b in zip(symbols, expected) if a == b)
    print("chords:", symbols, "matches", matches)
    assert matches >= 5
    kicks = {n["start_time"] % 4.0 for n in data["tracks"]["drums"] if n["pitch"] == 36}
    snares = {n["start_time"] % 4.0 for n in data["tracks"]["drums"] if n["pitch"] == 38}
    assert {0.0, 2.0} & kicks
    assert {1.0, 3.0} & snares
    assert data["tracks"]["bass"]
    assert 1 <= len(data["sections"]) <= 8
