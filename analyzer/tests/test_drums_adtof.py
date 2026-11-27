from ablanalyze.drums_adtof import ADTOF_TO_LIVE, parse_adtof


def test_parse_adtof_reads_time_and_pitch_columns_and_maps_to_live_pads():
    text = "0.512\t35\n0.998\t38\n1.240\t42\n1.500\t47\n2.000\t49\n"
    hits = parse_adtof(text)
    assert [(round(t, 3), p) for t, p in hits] == [(0.512, 36), (0.998, 38), (1.24, 42), (1.5, 47), (2.0, 49)]


def test_parse_adtof_skips_blank_and_unknown_lines():
    assert parse_adtof("\n# comment\n0.1\t38\n0.2\t99\n") == [(0.1, 38)]


def test_adtof_map_covers_kick_snare_hat_tom_cymbal():
    assert {ADTOF_TO_LIVE[p] for p in (35, 38, 42, 47, 49)} == {36, 38, 42, 47, 49}
