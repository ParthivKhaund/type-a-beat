from ablanalyze.drums import KICK, SNARE, HAT, classify_hit, hits_to_notes


def test_classify_low_heavy_hit_as_kick():
    assert classify_hit(low=1.0, mid=0.2, high=0.05) == KICK


def test_classify_bright_hit_as_hat():
    assert classify_hit(low=0.05, mid=0.2, high=1.0) == HAT


def test_classify_mid_broadband_hit_as_snare():
    assert classify_hit(low=0.4, mid=1.0, high=0.5) == SNARE


def test_hits_to_notes_quantizes_and_scales_velocity():
    (note,) = hits_to_notes([(1.13, KICK, 1.0)])
    assert note == {"pitch": KICK, "start_time": 1.25, "duration": 0.25, "velocity": 120}


def test_hits_to_notes_merges_duplicates_on_the_same_step_keeping_the_strongest():
    notes = hits_to_notes([(0.0, HAT, 0.2), (0.05, HAT, 0.8), (0.0, KICK, 0.5)])
    hats = [n for n in notes if n["pitch"] == HAT]
    assert len(hats) == 1 and hats[0]["velocity"] == 108
    assert len(notes) == 2


def test_hits_to_notes_drops_hits_before_the_first_downbeat():
    assert hits_to_notes([(-0.5, KICK, 1.0)]) == []


def test_a_bright_hit_with_a_real_body_is_a_snare_not_a_hat():
    assert classify_hit(low=0.1, mid=0.5, high=0.7) == SNARE
