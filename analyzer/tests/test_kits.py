import numpy as np

from ablanalyze.kits import midi_from_receiving_note, pad_map_for, remap_notes, score_kits


def unit(v):
    v = np.array(v, dtype=float)
    return v / np.linalg.norm(v)


def kit(name, **classes):
    return {"name": name, "path": name, "pads": {}, "classes": {cls: {"note": note, "features": list(unit(feat))} for cls, (note, feat) in classes.items()}}


def test_live_receiving_note_is_128_minus_midi():
    assert midi_from_receiving_note(92) == 36
    assert midi_from_receiving_note(82) == 46


def test_score_kits_ranks_the_kit_whose_samples_match_the_song_first():
    song = {"kick": unit([1, 0, 0]), "snare": unit([0, 1, 0])}
    index = {"kits": [kit("far", kick=(36, [0, 0, 1]), snare=(38, [0, 0, 1])), kit("near", kick=(36, [1, 0.1, 0]), snare=(38, [0.1, 1, 0]))]}
    ranked = score_kits(song, index)
    assert [k["name"] for _, k in ranked] == ["near", "far"]
    assert ranked[0][0] > ranked[1][0]


def test_score_kits_penalises_a_kit_missing_a_class_the_song_uses():
    song = {"kick": unit([1, 0, 0]), "hat": unit([0, 0, 1])}
    with_hat = kit("with", kick=(36, [1, 0, 0]), hat=(42, [0, 0, 1]))
    without = kit("without", kick=(36, [1, 0, 0]))
    ranked = score_kits(song, {"kits": [without, with_hat]})
    assert ranked[0][1]["name"] == "with"


def test_pad_map_uses_the_kits_own_notes_and_falls_back_to_gm():
    k = kit("x", kick=(60, [1, 0, 0]), hat=(61, [0, 0, 1]))
    lanes = pad_map_for(k)
    assert lanes["kick"] == 60 and lanes["ch"] == 61 and lanes["snare"] == 38


def test_remap_notes_moves_gm_hits_onto_the_kits_pads():
    k = kit("x", kick=(60, [1, 0, 0]), snare=(62, [0, 1, 0]))
    notes = [{"pitch": 36, "start_time": 0.0}, {"pitch": 38, "start_time": 1.0}, {"pitch": 42, "start_time": 0.5}]
    assert [n["pitch"] for n in remap_notes(notes, k)] == [60, 62, 42]
