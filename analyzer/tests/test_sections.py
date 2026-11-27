from ablanalyze.sections import boundaries_to_sections, cap_sections, label_sections


def test_boundaries_become_spans_and_short_ones_merge_into_the_previous():
    spans = boundaries_to_sections([8, 10, 18], total_bars=24, min_bars=4)
    assert spans == [(0, 10), (10, 8), (18, 6)]


def test_a_short_first_span_merges_forward():
    assert boundaries_to_sections([2, 10], total_bars=16, min_bars=4) == [(0, 10), (10, 6)]


def test_no_boundaries_is_one_span():
    assert boundaries_to_sections([], total_bars=12) == [(0, 12)]


def test_label_sections_marks_loudest_as_chorus_and_quiet_ends():
    spans = [(0, 4), (4, 8), (12, 8), (20, 8), (28, 4)]
    energies = [0.2, 0.6, 1.0, 0.6, 0.2]
    labels = [s["label"] for s in label_sections(spans, energies)]
    assert labels == ["intro", "verse", "chorus", "verse", "outro"]


def test_label_sections_keeps_start_bar_and_bars():
    (section,) = label_sections([(0, 8)], [1.0])
    assert section["start_bar"] == 0 and section["bars"] == 8 and 0 <= section["energy"] <= 1


def test_cap_sections_merges_the_shortest_into_a_neighbour_until_eight_remain():
    sections = [{"label": f"s{i}", "start_bar": i * 4, "bars": 4, "energy": 0.5} for i in range(11)]
    sections[3]["bars"] = 2
    capped = cap_sections(sections, max_n=8)
    assert len(capped) == 8
    assert sum(s["bars"] for s in capped) == sum(s["bars"] for s in sections)
    assert [s["start_bar"] for s in capped] == sorted(s["start_bar"] for s in capped)
    assert capped[-1]["start_bar"] + capped[-1]["bars"] == 44


def test_the_first_section_is_never_a_chorus_even_when_loud():
    labels = [s["label"] for s in label_sections([(0, 8), (8, 8)], [0.95, 1.0])]
    assert labels == ["verse", "chorus"]


def test_sections_from_segments_maps_seconds_to_bars_and_drops_silence_labels():
    from ablanalyze.rhythm import Grid
    from ablanalyze.sections import sections_from_segments

    grid = Grid(beat_times=[i * 0.5 for i in range(200)], first_downbeat=0)  # 120 bpm, bar = 2 s
    segments = [
        {"start": 0.0, "end": 0.4, "label": "start"},
        {"start": 0.4, "end": 8.1, "label": "intro"},
        {"start": 8.1, "end": 24.0, "label": "verse"},
        {"start": 24.0, "end": 40.2, "label": "chorus"},
        {"start": 40.2, "end": 41.0, "label": "end"},
    ]
    sections = sections_from_segments(segments, grid, total_bars=20)
    assert [(s["label"], s["start_bar"], s["bars"]) for s in sections] == [("intro", 0, 4), ("verse", 4, 8), ("chorus", 12, 8)]


def test_sections_from_segments_merges_slivers_and_stays_contiguous():
    from ablanalyze.rhythm import Grid
    from ablanalyze.sections import sections_from_segments

    grid = Grid(beat_times=[i * 0.5 for i in range(200)], first_downbeat=0)
    segments = [{"start": 0.0, "end": 16.0, "label": "verse"}, {"start": 16.0, "end": 17.0, "label": "bridge"}, {"start": 17.0, "end": 32.0, "label": "chorus"}]
    sections = sections_from_segments(segments, grid, total_bars=16)
    assert [(s["label"], s["start_bar"], s["bars"]) for s in sections] == [("verse", 0, 8), ("chorus", 8, 8)]
    assert sum(s["bars"] for s in sections) == 16
