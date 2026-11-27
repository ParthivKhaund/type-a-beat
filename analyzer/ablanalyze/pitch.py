"""Note transcription (Basic Pitch) and the clean-up that makes it usable as a clip."""

from __future__ import annotations

from ablanalyze.rhythm import Grid, quantize

SIXTEENTH = 0.25


def monophonic(notes: list[dict]) -> list[dict]:
    ordered = sorted((dict(n) for n in notes), key=lambda n: (n["start_time"], n["pitch"]))
    result: list[dict] = []
    for note in ordered:
        if result:
            last = result[-1]
            if note["start_time"] == last["start_time"]:
                if note["pitch"] < last["pitch"]:
                    result[-1] = note
                continue
            if note["start_time"] < last["start_time"] + last["duration"]:
                last["duration"] = round(note["start_time"] - last["start_time"], 6)
        result.append(note)
    return result


def fold_range(notes: list[dict], low: int, high: int) -> list[dict]:
    out = []
    for note in notes:
        pitch = int(note["pitch"])
        while pitch > high:
            pitch -= 12
        while pitch < low:
            pitch += 12
        out.append({**note, "pitch": pitch})
    return out


def quantize_notes(notes: list[dict], step: float = SIXTEENTH, min_duration: float = SIXTEENTH) -> list[dict]:
    out = []
    for note in notes:
        start = quantize(note["start_time"], step)
        if start < 0:
            continue
        duration = max(min_duration, quantize(note["duration"], step))
        out.append({**note, "start_time": start, "duration": duration})
    return out


def limit_polyphony(notes: list[dict], max_voices: int = 4) -> list[dict]:
    by_onset: dict[float, list[dict]] = {}
    for note in notes:
        by_onset.setdefault(note["start_time"], []).append(note)
    out = []
    for onset in sorted(by_onset):
        group = sorted(by_onset[onset], key=lambda n: -n.get("velocity", 0))[:max_voices]
        out.extend(sorted(group, key=lambda n: n["pitch"]))
    return out


def notes_from_events(events) -> list[dict]:
    """Basic Pitch note events (start_s, end_s, pitch, amplitude, bends) -> {pitch, start_s, end_s, velocity}."""
    notes = []
    for start_s, end_s, pitch, amplitude, _bends in events:
        notes.append({"pitch": int(pitch), "start_s": float(start_s), "end_s": float(end_s),
                      "velocity": int(max(1, min(127, round(float(amplitude) * 127))))})
    return notes


def transcribe(path: str) -> list[dict]:
    """Run Basic Pitch in a fresh interpreter: its CoreML backend is not importable once torch is loaded."""
    import json
    import subprocess
    import sys

    result = subprocess.run([sys.executable, "-m", "ablanalyze.pitch", str(path)], capture_output=True, text=True, timeout=600)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "basic-pitch failed")
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    return json.loads(lines[-1]) if lines else []


def _main(argv: list[str]) -> int:
    import contextlib
    import json
    import sys

    with contextlib.redirect_stdout(sys.stderr):  # Basic Pitch prints debug lines to stdout
        from basic_pitch import ICASSP_2022_MODEL_PATH
        from basic_pitch.inference import predict

        _, _, events = predict(argv[0], ICASSP_2022_MODEL_PATH)
    print(json.dumps(notes_from_events(events)))
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(_main(sys.argv[1:]))


def to_beats(notes_s: list[dict], grid: Grid) -> list[dict]:
    out = []
    for note in notes_s:
        start = grid.time_to_beats(note["start_s"])
        end = grid.time_to_beats(note["end_s"])
        out.append({"pitch": note["pitch"], "start_time": start, "duration": max(0.0, end - start), "velocity": note["velocity"]})
    return out


PIANO_SHARE = 0.35
GUITAR_SHARE = 0.45


def pick_keys_source(levels: dict[str, float]) -> str:
    """Which stem carries the keys part: 'piano', 'guitar', or 'other', from stem RMS levels."""
    total = sum(max(0.0, v) for v in levels.values())
    if total <= 0:
        return "other"
    if levels.get("piano", 0.0) / total >= PIANO_SHARE:
        return "piano"
    if levels.get("guitar", 0.0) / total >= GUITAR_SHARE:
        return "guitar"
    return "other"


def piano_transcribe(path: str) -> list[dict]:
    """ByteDance piano transcription (Kong et al.) -> {pitch, start_s, end_s, velocity}."""
    import librosa
    import soundfile as sf
    from piano_transcription_inference import PianoTranscription, sample_rate

    y, sr = sf.read(str(path), dtype="float32", always_2d=True)
    y = y.mean(axis=1)
    if sr != sample_rate:
        y = librosa.resample(y, orig_sr=sr, target_sr=sample_rate)
    model = PianoTranscription(device="cpu", checkpoint_path=None)
    result = model.transcribe(y, None)
    notes = []
    for event in result.get("est_note_events", []):
        notes.append({"pitch": int(event["midi_note"]), "start_s": float(event["onset_time"]), "end_s": float(event["offset_time"]),
                      "velocity": int(max(1, min(127, int(event.get("velocity", 90)))))})
    return notes
