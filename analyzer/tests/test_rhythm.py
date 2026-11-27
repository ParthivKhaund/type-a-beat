import pytest

from ablanalyze.rhythm import Grid, choose_downbeat_phase, quantize


def test_choose_downbeat_phase_picks_the_phase_with_most_low_energy():
    energies = [1.0, 0.1, 0.3, 0.1, 0.9, 0.2, 0.4, 0.1, 1.1, 0.1, 0.2, 0.1]
    assert choose_downbeat_phase(energies) == 0
    assert choose_downbeat_phase([0.1] + energies) == 1


def test_choose_downbeat_phase_on_too_few_beats_is_zero():
    assert choose_downbeat_phase([0.5, 0.9]) == 0


def test_grid_maps_time_to_beats_from_the_first_downbeat():
    grid = Grid(beat_times=[0.5, 1.0, 1.5, 2.0, 2.5], first_downbeat=1)
    assert grid.time_to_beats(1.0) == pytest.approx(0.0)
    assert grid.time_to_beats(1.25) == pytest.approx(0.5)
    assert grid.time_to_beats(0.5) == pytest.approx(-1.0)


def test_grid_extrapolates_past_the_last_beat():
    grid = Grid(beat_times=[0.0, 0.5, 1.0], first_downbeat=0)
    assert grid.time_to_beats(2.0) == pytest.approx(4.0)


def test_grid_beats_to_time_round_trips():
    grid = Grid(beat_times=[0.5, 1.0, 1.5, 2.0], first_downbeat=1)
    assert grid.beats_to_time(grid.time_to_beats(1.8)) == pytest.approx(1.8)


def test_grid_tempo_and_bars():
    grid = Grid(beat_times=[0.0, 0.5, 1.0, 1.5, 2.0], first_downbeat=0)
    assert grid.tempo == pytest.approx(120.0)
    assert grid.total_bars(duration_s=4.0) == 2


def test_quantize_to_sixteenths():
    assert quantize(1.13) == 1.25
    assert quantize(1.12) == 1.0
    assert quantize(0.9, step=0.5) == 1.0


def test_grid_from_downbeats_uses_the_beat_nearest_the_first_downbeat():
    from ablanalyze.rhythm import grid_from_downbeats

    grid = grid_from_downbeats(beats=[0.5, 1.0, 1.5, 2.0, 2.5, 3.0], downbeats=[1.52, 3.5])
    assert grid.first_downbeat == 2
    assert grid.time_to_beats(1.5) == pytest.approx(0.0)


def test_grid_from_downbeats_without_downbeats_starts_at_the_first_beat():
    from ablanalyze.rhythm import grid_from_downbeats

    assert grid_from_downbeats([0.0, 0.5, 1.0], []).first_downbeat == 0


def test_extend_to_start_prepends_whole_bars_when_the_first_downbeat_is_late():
    from ablanalyze.rhythm import Grid, extend_to_start

    grid = Grid(beat_times=[2.6 + 0.65 * i for i in range(12)], first_downbeat=0)
    extended = extend_to_start(grid)
    assert extended.first_downbeat == 0  # bar 0 now starts at the audio start
    assert extended.beat_times[0] == pytest.approx(0.0, abs=0.05)
    assert extended.time_to_beats(2.6) == pytest.approx(4.0, abs=1e-6)  # the model's first downbeat is bar 1
    assert extended.time_to_beats(0.0) == pytest.approx(0.0, abs=0.1)


def test_extend_to_start_leaves_an_early_downbeat_alone():
    from ablanalyze.rhythm import Grid, extend_to_start

    grid = Grid(beat_times=[0.3 + 0.5 * i for i in range(8)], first_downbeat=0)
    assert extend_to_start(grid) is grid
