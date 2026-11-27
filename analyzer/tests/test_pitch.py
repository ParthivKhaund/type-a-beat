import pytest

from ablanalyze.pitch import fold_range, limit_polyphony, monophonic, notes_from_events, quantize_notes


def n(pitch, start, dur, vel=100):
    return {"pitch": pitch, "start_time": start, "duration": dur, "velocity": vel}


def test_monophonic_keeps_the_lowest_note_at_each_onset_and_cuts_at_the_next():
    notes = [n(40, 0.0, 2.0), n(52, 0.0, 2.0), n(43, 1.0, 1.0)]
    assert monophonic(notes) == [n(40, 0.0, 1.0), n(43, 1.0, 1.0)]


def test_monophonic_leaves_a_gap_untouched():
    notes = [n(40, 0.0, 0.5), n(43, 2.0, 0.5)]
    assert monophonic(notes) == notes


def test_fold_range_moves_notes_by_octaves_into_range():
    assert [x["pitch"] for x in fold_range([n(20, 0, 1), n(50, 0, 1), n(30, 0, 1)], low=24, high=35)] == [32, 26, 30]


def test_quantize_notes_snaps_starts_and_enforces_a_minimum_duration():
    (note,) = quantize_notes([n(60, 1.13, 0.1)])
    assert note["start_time"] == 1.25 and note["duration"] == 0.25


def test_quantize_notes_drops_notes_before_zero():
    assert quantize_notes([n(60, -0.3, 1.0)]) == []


def test_limit_polyphony_keeps_the_strongest_voices_per_onset():
    notes = [n(60, 0, 1, 50), n(64, 0, 1, 90), n(67, 0, 1, 80), n(72, 0, 1, 20), n(76, 0, 1, 95)]
    kept = limit_polyphony(notes, max_voices=3)
    assert sorted(x["pitch"] for x in kept) == [64, 67, 76]


def test_notes_from_events_scales_amplitude_to_velocity():
    (note,) = notes_from_events([(0.5, 1.0, 45, 0.5, None)])
    assert note == {"pitch": 45, "start_s": 0.5, "end_s": 1.0, "velocity": 64}


def test_pick_keys_source_prefers_the_piano_stem_when_it_carries_the_part():
    from ablanalyze.pitch import pick_keys_source

    assert pick_keys_source({"piano": 0.05, "guitar": 0.01, "other": 0.02}) == "piano"
    assert pick_keys_source({"piano": 0.005, "guitar": 0.04, "other": 0.02}) == "guitar"
    assert pick_keys_source({"piano": 0.005, "guitar": 0.005, "other": 0.05}) == "other"
    assert pick_keys_source({"piano": 0.0, "guitar": 0.0, "other": 0.0}) == "other"
