"""Match a song's drum hits to the closest kit preset in the Live library, using the kit's own samples.

Kit presets (.adg) are gzipped XML: each pad lists its receiving note and sample file. Indexing every
kit's kick, snare, hat, clap, tom, and cymbal sample once (~/.abl/kits.json) lets recreate score
all kits against the song's hits and load the best one with its exact pad map.
"""

from __future__ import annotations

import glob
import gzip
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np

CORE_LIBRARY = Path("/Applications/Ableton Live 12 Lite.app/Contents/App-Resources/Core Library")
LIBRARY_ROOTS = [CORE_LIBRARY, Path("~/Music/Ableton/Factory Packs").expanduser(), Path("~/Music/Ableton/User Library").expanduser()]
INDEX_PATH = Path("~/.abl/kits.json").expanduser()
CLASS_NOTES = {"kick": (36, 35), "snare": (38, 40, 37), "clap": (39,), "hat": (42, 44), "openhat": (46,), "tom": (45, 47, 48, 50, 43, 41), "cymbal": (49, 51, 52, 57, 55)}
CLASS_WEIGHTS = {"kick": 3.0, "snare": 3.0, "hat": 2.0, "clap": 1.0, "openhat": 1.0, "tom": 0.5, "cymbal": 0.5}
FEATURE_SR = 22050
FEATURE_SECONDS = 0.15
N_MELS = 48
MAX_HITS_PER_CLASS = 40


def midi_from_receiving_note(value: int) -> int:
    """Live stores a pad's note as 128 - MIDI note."""
    return 128 - int(value)


def parse_kit(path: Path) -> dict[int, str]:
    """{midi note: sample path relative to the kit's library root}."""
    root = ET.fromstring(gzip.open(path).read())
    pads: dict[int, str] = {}
    for branch in root.iter("DrumBranchPreset"):
        note = branch.find(".//ReceivingNote")
        rel = branch.find(".//SampleRef/FileRef/RelativePath")
        if rel is None:
            rel = branch.find(".//RelativePath")
        if note is not None and rel is not None and rel.get("Value"):
            pads.setdefault(midi_from_receiving_note(int(note.get("Value"))), rel.get("Value"))
    return pads


def library_root(kit_path: Path) -> Path | None:
    for root in LIBRARY_ROOTS:
        try:
            parts = kit_path.relative_to(root).parts
        except ValueError:
            continue
        if root == CORE_LIBRARY:
            return root
        return root / parts[0] if parts else root  # Factory Packs/<Pack>/...
    return None


def hit_features(y: np.ndarray, sr: int) -> np.ndarray:
    """Timbre vector for one drum hit: log-mel mean and spectral centroid, unit-normalised."""
    import librosa

    y = np.asarray(y, dtype=np.float32)[: int(FEATURE_SECONDS * sr)]
    if len(y) < 256:
        y = np.pad(y, (0, 256 - len(y)))
    mel = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=N_MELS, n_fft=1024, hop_length=256)
    logmel = np.log(mel + 1e-9).mean(axis=1)
    logmel = logmel - logmel.max()
    centroid = float(librosa.feature.spectral_centroid(y=y, sr=sr).mean()) / 5000.0
    vec = np.concatenate([logmel, [centroid]])
    return vec / (np.linalg.norm(vec) + 1e-9)


def _sample_features(path: Path) -> np.ndarray | None:
    import librosa

    try:
        y, sr = librosa.load(str(path), sr=FEATURE_SR, mono=True, duration=FEATURE_SECONDS + 0.05)
    except Exception:
        return None
    if len(y) == 0 or float(np.abs(y).max()) < 1e-4:
        return None
    onset = int(np.argmax(np.abs(y) > 0.05 * np.abs(y).max()))
    return hit_features(y[onset:], sr)


def find_kits() -> list[Path]:
    kits = []
    for root in LIBRARY_ROOTS:
        kits += [Path(p) for p in glob.glob(str(root / "**" / "*.adg"), recursive=True) if "Drum Rack" in p or "Kit" in Path(p).name]
    return sorted(set(kits))


def build_index(progress=lambda s: None) -> dict:
    """Index every kit's class samples. Cached at ~/.abl/kits.json."""
    kits = find_kits()
    index = {"kits": []}
    for i, kit in enumerate(kits):
        lib = library_root(kit)
        if lib is None:
            continue
        try:
            pads = parse_kit(kit)
        except Exception:
            continue
        classes: dict[str, dict] = {}
        for cls, notes in CLASS_NOTES.items():
            for note in notes:
                sample = lib / pads[note] if note in pads else None
                if sample is not None and sample.exists():
                    feats = _sample_features(sample)
                    if feats is not None:
                        classes[cls] = {"note": note, "features": [round(float(v), 5) for v in feats]}
                        break
        if "kick" in classes or "snare" in classes:
            index["kits"].append({"name": kit.stem, "path": str(kit), "pads": {str(k): v for k, v in pads.items()}, "classes": classes})
        if i % 25 == 0:
            progress(f"kits: indexed {i}/{len(kits)}")
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(index))
    return index


def load_index(progress=lambda s: None) -> dict:
    if INDEX_PATH.exists():
        return json.loads(INDEX_PATH.read_text())
    progress("kits: indexing the library's drum kits (one time)")
    return build_index(progress)


def score_kits(song_classes: dict[str, np.ndarray], index: dict) -> list[tuple[float, dict]]:
    """Kits ranked best first by weighted cosine similarity over the classes the song uses."""
    ranked = []
    for kit in index.get("kits", []):
        total, weight = 0.0, 0.0
        for cls, vec in song_classes.items():
            w = CLASS_WEIGHTS.get(cls, 1.0)
            entry = kit["classes"].get(cls)
            weight += w
            if entry is None:
                total -= 0.5 * w  # the kit lacks a class the song uses
                continue
            total += float(np.dot(vec, np.array(entry["features"]))) * w
        if weight:
            ranked.append((total / weight, kit))
    return sorted(ranked, key=lambda r: -r[0])


def song_hit_classes(y: np.ndarray, sr: int, hits_s: list[tuple[float, int]]) -> dict[str, np.ndarray]:
    """Average timbre per class from the drums stem at the transcribed hit times (seconds, live pitch)."""
    note_to_class = {n: cls for cls, notes in CLASS_NOTES.items() for n in notes}
    by_class: dict[str, list[np.ndarray]] = {}
    for t, pitch in hits_s:
        cls = note_to_class.get(int(pitch))
        if cls is None or len(by_class.get(cls, [])) >= MAX_HITS_PER_CLASS:
            continue
        start = int(t * sr)
        segment = y[start:start + int(FEATURE_SECONDS * sr)]
        if len(segment) >= 512:
            by_class.setdefault(cls, []).append(hit_features(segment, sr))
    out = {}
    for cls, vecs in by_class.items():
        if len(vecs) >= 2:
            mean = np.mean(vecs, axis=0)
            out[cls] = mean / (np.linalg.norm(mean) + 1e-9)
    return out


def pad_map_for(kit: dict) -> dict[str, int]:
    """abl's drum lane names -> this kit's MIDI notes."""
    classes = kit.get("classes", {})
    lanes = {"kick": 36, "snare": 38, "clap": 39, "ch": 42, "oh": 46, "ride": 51, "crash": 49, "rim": 37, "perc": 43}
    for lane, cls in (("kick", "kick"), ("snare", "snare"), ("clap", "clap"), ("ch", "hat"), ("oh", "openhat"), ("ride", "cymbal"), ("crash", "cymbal")):
        if cls in classes:
            lanes[lane] = int(classes[cls]["note"])
    return lanes


def remap_notes(notes: list[dict], kit: dict) -> list[dict]:
    """Move transcribed hits (GM-style pitches) onto the chosen kit's pads."""
    lanes = pad_map_for(kit)
    gm_to_lane = {36: "kick", 35: "kick", 38: "snare", 40: "snare", 37: "rim", 39: "clap", 42: "ch", 44: "ch", 46: "oh", 47: "perc", 45: "perc", 48: "perc", 49: "crash", 51: "ride", 57: "crash"}
    out = []
    for note in notes:
        lane = gm_to_lane.get(int(note["pitch"]))
        pitch = lanes[lane] if lane else int(note["pitch"])
        out.append({**note, "pitch": pitch})
    return out
