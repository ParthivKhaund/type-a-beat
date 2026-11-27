import numpy as np
import pytest

from ablanalyze.chords import (
    NOTE_NAMES,
    TEMPLATE_NAMES,
    chords_per_bar,
    chords_per_beat,
    detect_key,
    key_name,
    score_frames,
    template_vector,
    viterbi,
)


def chroma(symbol, noise=0.05, seed=0):
    rng = np.random.default_rng(seed)
    return template_vector(symbol) + rng.uniform(0, noise, 12)


def test_template_vector_c_major_has_c_e_g():
    assert set(np.flatnonzero(template_vector("C"))) == {0, 4, 7}


def test_template_vector_a_minor_and_g_seven():
    assert set(np.flatnonzero(template_vector("Am"))) == {9, 0, 4}
    assert set(np.flatnonzero(template_vector("G7"))) == {7, 11, 2, 5}


def test_templates_cover_major_minor_and_seventh_for_every_root():
    assert len(TEMPLATE_NAMES) == 36
    assert "F#m" in TEMPLATE_NAMES and "Bb" not in TEMPLATE_NAMES and "A#" in TEMPLATE_NAMES


def test_score_frames_prefers_the_matching_template():
    scores = score_frames(np.array([chroma("Am")]))
    assert TEMPLATE_NAMES[int(np.argmax(scores[0]))] == "Am"


def test_chords_per_beat_recovers_a_clean_progression():
    symbols = ["C"] * 4 + ["Am"] * 4 + ["F"] * 4 + ["G"] * 4
    frames = np.array([chroma(s, seed=i) for i, s in enumerate(symbols)])
    assert chords_per_beat(frames) == symbols


def test_viterbi_smooths_a_single_noisy_beat():
    n = len(TEMPLATE_NAMES)
    c, am = TEMPLATE_NAMES.index("C"), TEMPLATE_NAMES.index("Am")
    scores = np.full((8, n), 0.2)
    scores[:, c] = 0.9
    scores[4, c], scores[4, am] = 0.6, 0.65  # one beat leans Am, barely
    assert viterbi(scores) == [c] * 8


def test_chords_per_bar_takes_the_majority_and_breaks_ties_by_first():
    beats = ["C", "C", "Am", "C", "F", "F", "G", "G"]
    assert chords_per_bar(beats, beats_per_bar=4) == ["C", "F"]


def test_detect_key_major_and_minor_from_profiles():
    from ablanalyze.chords import MAJOR_PROFILE, MINOR_PROFILE
    root, scale, conf = detect_key(np.roll(MAJOR_PROFILE, 7))  # G major
    assert (root, scale) == (7, "Major") and conf > 0.9
    root, scale, conf = detect_key(np.roll(MINOR_PROFILE, 9))  # A minor
    assert (root, scale) == (9, "Minor")


def test_key_name():
    assert key_name(9, "Minor") == "A minor"
    assert key_name(6, "Major") == "F# major"
    assert NOTE_NAMES[10] == "A#"


def test_root_weighted_templates_separate_a_minor_from_f_major_on_the_bass_note():
    frame = template_vector("Am") * 0 + np.array([1, 0, 0, 0, 1, 0, 0, 0, 0, 2.5, 0, 0], dtype=float)  # A strong, C, E
    scores = score_frames(np.array([frame]))[0]
    assert TEMPLATE_NAMES[int(np.argmax(scores))] == "Am"
