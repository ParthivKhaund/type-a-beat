import pytest

from abl.patterns import (
    BASS_STYLES,
    DRUM_STYLES,
    STYLE_ALIASES,
    hat_variant,
    lane_to_notes,
    normalize_style,
    render_bass,
    render_drums,
    render_keys,
)
from abl.theory import parse_chord, parse_progression

PAD_MAP = {"kick": 36, "rim": 37, "snare": 38, "clap": 39, "ch": 42, "oh": 46, "crash": 49, "ride": 51, "perc": 43}


def test_lane_to_notes_places_hits_at_step_boundaries():
    notes = lane_to_notes("x.o.", pitch=36, total_beats=1.0)
    assert [n["start_time"] for n in notes] == [0.0, 0.5]
    assert all(n["pitch"] == 36 for n in notes)


def test_lane_to_notes_velocity_by_symbol():
    notes = lane_to_notes("xog", pitch=38, total_beats=0.75)
    assert [n["velocity"] for n in notes] == [118, 96, 55]


def test_lane_to_notes_has_all_wire_fields():
    (note,) = lane_to_notes("x", pitch=36, total_beats=1.0)
    assert set(note) == {"pitch", "start_time", "duration", "velocity", "mute"}
    assert note["mute"] is False


def test_lane_to_notes_duration_never_exceeds_step():
    notes = lane_to_notes("xxxx", pitch=42, total_beats=1.0)
    assert all(n["duration"] <= 0.25 for n in notes)


def test_swing_delays_only_off_steps():
    straight = lane_to_notes("xxxx", pitch=42, total_beats=1.0)
    swung = lane_to_notes("xxxx", pitch=42, total_beats=1.0, swing=66)
    assert swung[0]["start_time"] == straight[0]["start_time"] == 0.0
    assert swung[2]["start_time"] == straight[2]["start_time"] == 0.5
    assert swung[1]["start_time"] == pytest.approx(0.25 + 0.08, abs=0.01)
    assert swung[3]["start_time"] == pytest.approx(0.75 + 0.08, abs=0.01)


def test_swing_50_is_straight():
    assert lane_to_notes("xxxx", pitch=42, total_beats=1.0, swing=50) == lane_to_notes("xxxx", pitch=42, total_beats=1.0)


def test_hat_variant_double_fills_every_half_step():
    assert hat_variant("x.o.", "double") == "xooooooo"


def test_hat_variant_half_keeps_even_steps_only():
    assert hat_variant("xooo", "half") == "x.o."


def test_hat_variant_normal_is_identity():
    assert hat_variant("x.o.", "normal") == "x.o."


def test_hat_variant_rejects_unknown_mode():
    with pytest.raises(ValueError):
        hat_variant("x.o.", "sideways")


@pytest.mark.parametrize("style", ["trap", "boombap", "house", "techno", "pop", "lofi", "jazz"])
def test_every_drum_style_renders_two_bars_inside_the_pad_map(style):
    notes = render_drums(style, PAD_MAP)
    assert notes
    assert all(0.0 <= n["start_time"] < 8.0 for n in notes)
    assert all(n["pitch"] in PAD_MAP.values() for n in notes)


def test_trap_has_kick_on_the_one_and_snare_on_three():
    notes = render_drums("trap", PAD_MAP)
    kicks = {n["start_time"] for n in notes if n["pitch"] == 36}
    snares = {n["start_time"] for n in notes if n["pitch"] in (38, 39)}
    assert 0.0 in kicks
    assert {2.0, 6.0} <= snares


def test_house_is_four_on_the_floor():
    notes = render_drums("house", PAD_MAP)
    kicks = sorted(n["start_time"] for n in notes if n["pitch"] == 36)
    assert kicks == [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]


def test_hats_off_removes_hi_hats():
    notes = render_drums("house", PAD_MAP, hats="off")
    assert not any(n["pitch"] in (42, 46) for n in notes)


def test_hats_double_adds_more_closed_hats_than_normal():
    normal = sum(1 for n in render_drums("trap", PAD_MAP) if n["pitch"] == 42)
    double = sum(1 for n in render_drums("trap", PAD_MAP, hats="double") if n["pitch"] == 42)
    assert double > normal


def test_lane_missing_from_pad_map_is_skipped_not_crashed():
    notes = render_drums("jazz", {"kick": 36, "snare": 38})
    assert notes
    assert {n["pitch"] for n in notes} <= {36, 38}


def test_render_drums_unknown_style_raises():
    with pytest.raises(KeyError):
        render_drums("dubstep", PAD_MAP)


def test_normalize_style_maps_aliases():
    assert normalize_style("swing") == "jazz"
    assert normalize_style("hiphop") == "boombap"
    assert normalize_style("hip-hop") == "boombap"
    assert normalize_style("TRAP") == "trap"


def test_normalize_style_rejects_unknown():
    with pytest.raises(KeyError):
        normalize_style("dubstep")


def test_every_alias_targets_a_real_style():
    assert set(STYLE_ALIASES.values()) <= set(DRUM_STYLES)


def test_every_drum_style_has_a_bass_style():
    assert set(DRUM_STYLES) <= set(BASS_STYLES)


def test_house_bass_is_offbeat_eighths_following_the_chords():
    notes = render_bass("house", parse_progression("C-F"), low=24, high=35)
    assert [n["start_time"] for n in notes] == [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5]
    assert [n["pitch"] for n in notes] == [24] * 4 + [29] * 4


def test_jazz_bass_walks_and_approaches_the_next_root_from_below():
    notes = render_bass("jazz", parse_progression("C-G"), low=36, high=47)
    bar1 = [n for n in notes if n["start_time"] < 4.0]
    assert [n["start_time"] for n in bar1] == [0.0, 1.0, 2.0, 3.0]
    assert bar1[0]["pitch"] == 36
    assert bar1[3]["pitch"] == 42  # G is 43; approach from a half step below


def test_bass_covers_every_bar_of_the_progression():
    notes = render_bass("trap", parse_progression("Am-F-C-G"), low=24, high=35)
    assert max(n["start_time"] for n in notes) >= 12.0
    assert all(n["start_time"] + n["duration"] <= 16.0 + 1e-9 for n in notes)


def test_bass_never_leaves_its_range():
    for style in BASS_STYLES:
        for n in render_bass(style, parse_progression("Bb-E-G#m-C#7"), low=24, high=35):
            assert 24 <= n["pitch"] <= 35, style


def test_keys_hold_sustains_each_chord_for_a_bar():
    notes = render_keys(parse_progression("Cmaj7-Fmaj7"), mode="hold")
    assert len(notes) == 8
    assert {n["start_time"] for n in notes} == {0.0, 4.0}
    assert all(n["duration"] == pytest.approx(3.9) for n in notes)


def test_keys_stab_hits_the_offbeats():
    notes = render_keys([parse_chord("C")], mode="stab")
    assert sorted({n["start_time"] for n in notes}) == [0.5, 1.5, 2.5, 3.5]


def test_keys_voice_lead_between_chords():
    notes = render_keys(parse_progression("Cmaj7-Fmaj7"), mode="hold")
    first = sorted(n["pitch"] for n in notes if n["start_time"] == 0.0)
    second = sorted(n["pitch"] for n in notes if n["start_time"] == 4.0)
    assert sum(abs(a - b) for a, b in zip(first, second)) <= 8


def test_swing_leaves_triplet_grids_alone():
    assert render_drums("jazz", PAD_MAP, swing=66) == render_drums("jazz", PAD_MAP)


def test_bass_degrees_follow_the_chord_root_when_a_slash_bass_is_given():
    notes = render_bass("jazz", parse_progression("C/E-C/E"), low=36, high=47)
    bar1 = [n["pitch"] for n in notes if n["start_time"] < 4.0]
    assert bar1[0] == 40  # E: the slash bass on the root beat
    assert bar1[1] % 12 == 4 and bar1[2] % 12 == 7  # third and fifth of C, not of E
