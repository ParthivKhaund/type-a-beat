import pytest

from abl.theory import (
    ChordError,
    bass_pitch,
    candidate_voicings,
    movement,
    parse_chord,
    parse_progression,
    scale_chord,
    voice,
)


@pytest.mark.parametrize(
    "symbol, root, intervals",
    [
        ("C", 0, (0, 4, 7)),
        ("Am", 9, (0, 3, 7)),
        ("Am7", 9, (0, 3, 7, 10)),
        ("Cmaj7", 0, (0, 4, 7, 11)),
        ("G7", 7, (0, 4, 7, 10)),
        ("Bb", 10, (0, 4, 7)),
        ("F#m", 6, (0, 3, 7)),
        ("Bdim", 11, (0, 3, 6)),
        ("Bm7b5", 11, (0, 3, 6, 10)),
        ("Csus4", 0, (0, 5, 7)),
        ("Csus2", 0, (0, 2, 7)),
        ("C6", 0, (0, 4, 7, 9)),
        ("Am6", 9, (0, 3, 7, 9)),
        ("Cadd9", 0, (0, 4, 7, 14)),
        ("C9", 0, (0, 4, 7, 10, 14)),
        ("Cmaj9", 0, (0, 4, 7, 11, 14)),
        ("Am9", 9, (0, 3, 7, 10, 14)),
        ("Caug", 0, (0, 4, 8)),
        ("Cdim7", 0, (0, 3, 6, 9)),
        ("Dmin7", 2, (0, 3, 7, 10)),
        ("Eb-7", 3, (0, 3, 7, 10)),
    ],
)
def test_parse_chord_root_and_intervals(symbol, root, intervals):
    chord = parse_chord(symbol)
    assert chord.root == root
    assert chord.intervals == intervals


def test_parse_chord_slash_bass_sets_bass_pitch_class():
    chord = parse_chord("C/E")
    assert chord.root == 0
    assert chord.bass == 4


def test_parse_chord_without_slash_has_no_bass_override():
    assert parse_chord("C").bass is None


def test_parse_chord_keeps_symbol():
    assert parse_chord("Am7").symbol == "Am7"


@pytest.mark.parametrize("bad", ["H7", "", "Cxyz", "7"])
def test_parse_chord_rejects_junk(bad):
    with pytest.raises(ChordError):
        parse_chord(bad)


def test_parse_progression_splits_on_dashes():
    chords = parse_progression("Cmaj7-Am7-Dm7-G7")
    assert [c.symbol for c in chords] == ["Cmaj7", "Am7", "Dm7", "G7"]


def test_parse_progression_splits_on_spaces_and_commas():
    assert [c.symbol for c in parse_progression("Am F, C G")] == ["Am", "F", "C", "G"]


def test_parse_progression_rejects_empty():
    with pytest.raises(ChordError):
        parse_progression("   ")


def test_voice_places_every_chord_tone_inside_range():
    pitches = voice(parse_chord("Cmaj7"), None, low=55, high=76)
    assert len(pitches) == 4
    assert pitches == sorted(pitches)
    assert all(55 <= p <= 76 for p in pitches)
    assert {p % 12 for p in pitches} == {0, 4, 7, 11}


def test_voice_picks_the_inversion_with_least_movement():
    prev = voice(parse_chord("Cmaj7"), None)
    chosen = voice(parse_chord("Fmaj7"), prev)
    candidates = candidate_voicings(parse_chord("Fmaj7"), low=55, high=76)
    assert chosen in candidates
    assert movement(prev, chosen) == min(movement(prev, c) for c in candidates)


def test_movement_sums_absolute_distance_per_voice():
    assert movement([60, 64, 67], [60, 65, 69]) == 3


def test_movement_handles_different_voice_counts():
    assert movement([60, 64, 67], [60, 64, 67, 71]) == 0


@pytest.mark.parametrize(
    "symbol, expected",
    [("C", 24), ("G", 31), ("A", 33), ("C/E", 28), ("B", 35)],
)
def test_bass_pitch_lands_in_the_808_octave(symbol, expected):
    assert bass_pitch(parse_chord(symbol), low=24, high=35) == expected


def test_bass_pitch_follows_range():
    assert bass_pitch(parse_chord("C"), low=36, high=47) == 36


def test_scale_chord_minor_scale_gives_minor_triad():
    chord = scale_chord(7, "Minor")
    assert chord.root == 7
    assert chord.intervals == (0, 3, 7)


def test_scale_chord_major_scale_gives_major_triad():
    assert scale_chord(0, "Major").intervals == (0, 4, 7)


def test_scale_chord_unknown_scale_defaults_to_major():
    assert scale_chord(2, "Phrygian Dominant").intervals == (0, 4, 7)


@pytest.mark.parametrize("root, scale, symbol", [(5, "Major", "F"), (6, "Major", "F#"), (0, "Minor", "Cm"), (10, "Major", "A#")])
def test_scale_chord_symbol_names_the_root_sensibly(root, scale, symbol):
    assert scale_chord(root, scale).symbol == symbol
