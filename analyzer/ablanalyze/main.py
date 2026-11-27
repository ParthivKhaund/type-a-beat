"""ablanalyze <url or file> [--cache-dir DIR] [--fresh]: progress on stderr, analysis.json path on stdout."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Callable

import numpy as np

from ablanalyze import beats as beats_mod
from ablanalyze import chords as chords_mod
from ablanalyze import download, drums, drums_adtof, instruments, kits, pitch, sections as sections_mod, separate, structure
from ablanalyze.rhythm import Grid, choose_downbeat_phase, extend_to_start, grid_from_downbeats, low_band_energy_at, track_beats

SR = 22050
HOP = 512
BEATS_PER_BAR = 4
BASS_RANGE = (28, 51)
BASS_CHROMA_WEIGHT = 2.0
KEYS_RANGE = (48, 84)
LEAD_RANGE = (55, 84)
MIN_LEAD_NOTES = 8
Progress = Callable[[str], None]


def _load(path: Path) -> np.ndarray:
    import librosa

    y, _ = librosa.load(str(path), sr=SR, mono=True)
    return y


def _beat_sync(feature: np.ndarray, beat_times: list[float]) -> np.ndarray:
    import librosa

    frames = librosa.time_to_frames(np.array(beat_times), sr=SR, hop_length=HOP)
    synced = librosa.util.sync(feature, frames, aggregate=np.median)
    return synced.T  # [beats, dims]


def _bar_means(beat_rows: np.ndarray, total_bars: int) -> np.ndarray:
    rows = beat_rows[: total_bars * BEATS_PER_BAR]
    if len(rows) < total_bars * BEATS_PER_BAR:
        pad = np.zeros((total_bars * BEATS_PER_BAR - len(rows), rows.shape[1]))
        rows = np.vstack([rows, pad]) if len(rows) else pad
    return rows.reshape(total_bars, BEATS_PER_BAR, -1).mean(axis=1)


def analyze(source: str, cache_dir: Path, fresh: bool, progress: Progress) -> Path:
    import librosa

    meta = download.fetch(source, cache_dir, progress)
    folder = Path(meta["folder"])
    out = folder / "analysis.json"
    if fresh:  # redo the analysis; the stems only depend on the audio, so they are kept
        out.unlink(missing_ok=True)
    if out.exists():
        progress("analysis: cached")
        return out
    stems = separate.separate(Path(meta["audio"]), folder, progress)
    harmonic = separate.harmonic_mix(stems, folder)
    four_stems = {"drums": stems["drums"], "bass": stems["bass"], "vocals": stems["vocals"], "other": harmonic}
    engine: dict[str, str] = {"stems": f"demucs {len(stems)}-stem"}
    audio_path = Path(meta["audio"])
    y_drums = _load(stems["drums"])
    y_mix = _load(audio_path)
    duration = float(meta.get("duration_s") or len(y_mix) / SR)

    # -- beats, downbeats, sections: All-In-One, else Beat This!, else librosa ----
    progress("structure: beats, downbeats, sections")
    segments = None
    result = structure.analyze_structure(audio_path, four_stems, folder, progress)
    if result and len(result["beats"]) >= 8:
        grid = grid_from_downbeats(result["beats"], result["downbeats"])
        segments = result["segments"]
        engine["beats"] = engine["sections"] = "all-in-one"
    elif beats_mod.available():
        try:
            beats, downbeats = beats_mod.track(audio_path)
            grid = grid_from_downbeats(beats, downbeats)
            engine["beats"] = "beat-this"
        except Exception as exc:
            progress(f"structure: Beat This! failed ({str(exc)[:60]})")
            grid = None
    else:
        grid = None
    if grid is None:
        tempo, beats = track_beats(y_drums, SR)
        if len(beats) < 8:
            tempo, beats = track_beats(y_mix, SR)
        grid = Grid(beats, choose_downbeat_phase(low_band_energy_at(y_drums, SR, beats)))
        engine["beats"] = "librosa"
    grid = extend_to_start(grid)
    total_bars = grid.total_bars(duration)
    progress(f"rhythm: {grid.tempo:.1f} bpm, {total_bars} bars ({engine['beats']})")

    # -- drums: ADTOF, else band classifier ----
    drum_notes = []
    drums_done = False
    hits_s: list[tuple[float, int]] = []
    if drums_adtof.available():
        try:
            progress("drums: ADTOF transcription")
            hits_s = drums_adtof.transcribe_drums(stems["drums"], folder)
            hits = [(grid.time_to_beats(t), pitch, 0.8) for t, pitch in hits_s]
            drum_notes = drums.hits_to_notes(hits)
            engine["drums"] = "adtof"
            drums_done = True  # an empty answer from ADTOF means the song has no drums; trust it
            if not drum_notes:
                progress("drums: none found (no drum part)")
        except Exception as exc:
            progress(f"drums: ADTOF failed ({str(exc)[:80]}); using onset classifier")
    if not drums_done:
        detected = drums.detect_hits(y_drums, SR, grid)
        hits_s = [(grid.beats_to_time(b), pitch) for b, pitch, _ in detected]
        drum_notes = drums.hits_to_notes(detected)
        engine["drums"] = "onset-bands"

    # -- which kit sounds most like the song's own hits ----
    kit_choice = None
    if drum_notes:
        try:
            index = kits.load_index(progress)
            classes = kits.song_hit_classes(y_drums, SR, hits_s)
            ranked = kits.score_kits(classes, index) if classes else []
            if ranked:
                score, best = ranked[0]
                kit_choice = {"name": best["name"], "path": best["path"], "score": round(score, 3), "pad_map": kits.pad_map_for(best),
                              "runners_up": [k["name"] for _, k in ranked[1:4]]}
                drum_notes = kits.remap_notes(drum_notes, best)
                progress(f"drums: closest kit {best['name']} ({score:.2f}); also {', '.join(kit_choice['runners_up'])}")
        except Exception as exc:
            progress(f"drums: kit matching failed ({str(exc)[:60]})")

    progress("harmony: chords and key")
    chroma = (librosa.feature.chroma_cqt(y=_load(harmonic), sr=SR, hop_length=HOP)
              + BASS_CHROMA_WEIGHT * librosa.feature.chroma_cqt(y=_load(stems["bass"]), sr=SR, hop_length=HOP))
    downbeat_times = [grid.beats_to_time(b) for b in range(total_bars * BEATS_PER_BAR + 1)]
    beat_chroma = _beat_sync(chroma, downbeat_times)[: total_bars * BEATS_PER_BAR]
    beat_symbols = chords_mod.chords_per_beat(beat_chroma) if len(beat_chroma) else []
    bar_symbols = chords_mod.chords_per_bar(beat_symbols, BEATS_PER_BAR)
    root, scale, confidence = chords_mod.detect_key(chroma.sum(axis=1))

    # -- notes: bass (Basic Pitch), keys (piano model or Basic Pitch by instrument), lead (Basic Pitch) ----
    levels = separate.levels({k: v for k, v in stems.items() if k in ("piano", "guitar", "other")})
    keys_source = pitch.pick_keys_source(levels)
    progress(f"notes: bass, keys from the {keys_source} stem, lead")
    bass_notes = pitch.fold_range(pitch.quantize_notes(pitch.monophonic(pitch.to_beats(pitch.transcribe(stems["bass"]), grid))), *BASS_RANGE)
    keys_raw = []
    if keys_source == "piano":
        try:
            keys_raw = pitch.piano_transcribe(stems["piano"])
            engine["keys"] = "piano-transcription"
        except Exception as exc:
            progress(f"notes: piano model failed ({str(exc)[:60]}); using Basic Pitch")
    if not keys_raw:
        keys_raw = pitch.transcribe(stems.get(keys_source, harmonic) if keys_source != "other" else harmonic)
        engine["keys"] = "basic-pitch"
    keys_notes = pitch.fold_range(pitch.limit_polyphony(pitch.quantize_notes(pitch.to_beats(keys_raw, grid))), *KEYS_RANGE)
    lead_notes = pitch.fold_range(pitch.quantize_notes(pitch.monophonic(pitch.to_beats(pitch.transcribe(stems["vocals"]), grid))), *LEAD_RANGE)
    if len(lead_notes) < MIN_LEAD_NOTES:
        lead_notes = []

    # -- what each part sounds like (CLAP zero-shot, per role) ----
    tags: dict[str, list] = {}
    if instruments.available():
        try:
            progress("instruments: listening to each stem")
            keys_stem = stems.get(keys_source, harmonic) if keys_source != "other" else harmonic
            tags = instruments.tag_roles({"bass": stems["bass"], "keys": keys_stem, "lead": stems["vocals"], "drums": stems["drums"]})
            heard = ", ".join(f"{role} {labels[0][0]}" for role, labels in tags.items() if labels)
            progress(f"instruments: {heard}")
        except Exception as exc:
            progress(f"instruments: tagging failed ({str(exc)[:60]})")

    # -- sections: All-In-One segments, else novelty on the mix ----
    if segments:
        section_list = sections_mod.sections_from_segments(segments, grid, total_bars)
    else:
        progress("sections: novelty boundaries")
        mfcc = librosa.feature.mfcc(y=y_mix, sr=SR, hop_length=HOP, n_mfcc=13)
        mix_chroma = librosa.feature.chroma_cqt(y=y_mix, sr=SR, hop_length=HOP)
        feats = np.vstack([mfcc / (np.abs(mfcc).max() + 1e-9), mix_chroma])
        bar_feats = _bar_means(_beat_sync(feats, downbeat_times), total_bars)
        boundaries = sections_mod.novelty_boundaries(bar_feats)
        spans = sections_mod.boundaries_to_sections(boundaries, total_bars)
        rms = librosa.feature.rms(y=y_mix, hop_length=HOP)
        bar_rms = _bar_means(_beat_sync(rms, downbeat_times), total_bars)[:, 0]
        energies = [float(bar_rms[s:s + b].mean()) if b else 0.0 for s, b in spans]
        section_list = sections_mod.cap_sections(sections_mod.label_sections(spans, energies))
        engine["sections"] = "novelty"

    analysis = {
        "source": {k: meta[k] for k in ("url", "title", "duration_s", "audio")},
        "tempo": round(grid.tempo, 2),
        "beats_per_bar": BEATS_PER_BAR,
        "key": {"root": root, "scale": scale, "name": chords_mod.key_name(root, scale), "confidence": round(confidence, 3)},
        "sections": section_list,
        "chords": [{"bar": i, "symbol": s} for i, s in enumerate(bar_symbols)],
        "tracks": {"drums": drum_notes, "bass": bass_notes, "keys": keys_notes, "lead": lead_notes},
        "instruments": {k: round(v, 5) for k, v in levels.items()},
        "keys_source": keys_source,
        "instrument_tags": tags,
        "kit": kit_choice,
        "engine": engine,
    }
    out.write_text(json.dumps(analysis))
    progress(f"done: {len(section_list)} sections, {len(drum_notes)} drum hits, {len(bass_notes)} bass, {len(keys_notes)} keys, {len(lead_notes)} lead notes; engines " + ", ".join(f"{k}={v}" for k, v in engine.items()))
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ablanalyze")
    parser.add_argument("source")
    parser.add_argument("--cache-dir", default=str(Path("~/.abl/cache").expanduser()))
    parser.add_argument("--fresh", action="store_true")
    args = parser.parse_args(argv)

    def progress(line: str) -> None:
        print(line, file=sys.stderr, flush=True)

    try:
        out = analyze(args.source, Path(args.cache_dir).expanduser(), args.fresh, progress)
    except Exception as exc:
        progress(f"error: {exc}")
        return 1
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
