import pytest

from abl.actions import ActionError, execute
from abl.commands import HELP, parse
from abl.session import Session


def run(live, *lines):
    session = Session(live)
    outputs = [execute(parse(line), session) for line in lines]
    return session, outputs


# -- beat / drums -----------------------------------------------------------

def test_beat_on_a_set_without_drums_creates_names_loads_and_fires(empty_live):
    _, (out,) = run(empty_live, "beat trap 140")
    assert empty_live.types() == ["get_session_snapshot", "batch", "get_session_snapshot"]  # re-read pins ownership to the new track id
    assert empty_live.last_batch_types() == [
        "create_midi_track", "set_track_name", "set_tempo", "load_browser_item", "create_clip", "add_notes_to_clip", "set_clip_loop", "set_clip_name", "fire_clip",
    ]
    assert empty_live.batch_params("load_browser_item") == [{"track_index": 0, "item_uri": "query:Drums#FileId_5409"}]
    assert empty_live.batch_params("set_tempo") == [{"tempo": 140.0}]
    assert empty_live.batch_params("create_clip") == [{"track_index": 0, "clip_index": 0, "length": 8.0}]
    assert empty_live.batch_params("set_clip_loop")[0]["end"] == 8.0
    assert empty_live.tracks[0]["name"] == "Drums"
    assert empty_live.tracks[0]["notes"][0]
    assert "trap" in out and "808 Core Kit" in out


def test_beat_reuses_an_existing_drums_track_and_first_empty_slot(studio_live):
    run(studio_live, "beat house")
    assert "create_midi_track" not in studio_live.types()
    assert studio_live.batch_params("create_clip") == [{"track_index": 3, "clip_index": 1, "length": 8.0}]
    assert studio_live.tracks[3]["slots"][0] is True  # the user's own clip is untouched


def test_beat_replaces_a_different_kit_and_says_so(studio_live):
    _, (out,) = run(studio_live, "beat house")
    assert studio_live.batch_params("load_browser_item") == [{"track_index": 3, "item_uri": "query:Drums#FileId_5410"}]
    assert "Garage Kit" in out and "909 Core Kit" in out


def test_beat_does_not_reload_a_kit_that_is_already_there(studio_live):
    studio_live.tracks[3]["devices"] = ["808 Core Kit"]
    run(studio_live, "beat trap")
    assert "load_browser_item" not in studio_live.last_batch_types()


def test_beat_without_bpm_leaves_tempo_alone(studio_live):
    run(studio_live, "beat trap")
    assert "set_tempo" not in studio_live.last_batch_types()
    assert studio_live.tempo == 122.0


def test_second_beat_overwrites_abls_own_clip_not_a_new_slot(studio_live):
    run(studio_live, "beat trap", "beat house")
    assert studio_live.batch_params("delete_clip") == [{"track_index": 3, "clip_index": 1}]
    assert [p["clip_index"] for p in studio_live.batch_params("create_clip")] == [1, 1]


def test_drums_never_touches_tempo(studio_live):
    run(studio_live, "drums lofi")
    assert "set_tempo" not in studio_live.last_batch_types()


# -- bass -----------------------------------------------------------------

def test_bass_follows_the_keys_progression(empty_live):
    session, _ = run(empty_live, "keys rhodes Am-F-C-G", "bass 808")
    assert empty_live.batch_params("load_browser_item")[-1]["item_uri"] == "query:Sounds#Bass:FileId_6515"
    assert empty_live.batch_params("create_clip")[-1]["length"] == 16.0
    notes = empty_live.batch_params("add_notes_to_clip")[-1]["notes"]
    assert all(24 <= n["pitch"] <= 35 for n in notes)


def test_bass_without_a_progression_uses_the_live_key(empty_live):
    run(empty_live, "bass upright")
    assert "get_session_info" in empty_live.types()
    notes = empty_live.batch_params("add_notes_to_clip")[-1]["notes"]
    assert {n["pitch"] % 12 for n in notes} <= {7, 10, 2}  # G minor tones
    assert empty_live.batch_params("create_clip")[-1]["length"] == 8.0


def test_bass_defaults_its_sound_and_pattern_from_the_current_beat(empty_live):
    run(empty_live, "beat trap", "bass")
    assert empty_live.batch_params("load_browser_item")[-1]["item_uri"] == "query:Sounds#Bass:FileId_6515"


def test_bass_reuses_the_users_bass_track(studio_live):
    run(studio_live, "bass analog")
    assert studio_live.batch_params("create_clip")[-1]["track_index"] == 1


# -- keys -----------------------------------------------------------------

def test_keys_writes_one_bar_per_chord(empty_live):
    session, (out,) = run(empty_live, "keys rhodes Cmaj7-Am7-Dm7-G7")
    assert empty_live.batch_params("create_clip")[-1]["length"] == 16.0
    assert empty_live.batch_params("load_browser_item")[-1]["item_uri"].endswith("FileId_4849")
    assert [c.symbol for c in session.progression] == ["Cmaj7", "Am7", "Dm7", "G7"]
    assert "4 bars" in out


def test_keys_hold_by_default_and_stab_for_house(empty_live):
    run(empty_live, "keys piano C-F")
    held = empty_live.batch_params("add_notes_to_clip")[-1]["notes"]
    assert all(n["duration"] == pytest.approx(3.9) for n in held)
    run(empty_live, "beat house", "keys piano C-F")
    stabbed = empty_live.batch_params("add_notes_to_clip")[-1]["notes"]
    assert all(n["duration"] == pytest.approx(0.3) for n in stabbed)


def test_keys_explicit_mode_wins(empty_live):
    run(empty_live, "keys piano C-F stab")
    assert all(n["duration"] == pytest.approx(0.3) for n in empty_live.batch_params("add_notes_to_clip")[-1]["notes"])


# -- transport / tempo ------------------------------------------------------

def test_tempo(empty_live):
    _, (out,) = run(empty_live, "tempo 128")
    assert empty_live.tempo == 128.0 and "128" in out


def test_go_fires_every_abl_clip_then_starts_playback(empty_live):
    run(empty_live, "beat trap", "keys piano C", "go")
    assert empty_live.last_batch_types() == ["fire_clip", "fire_clip", "start_playback"]


def test_go_with_nothing_remembered_just_starts_playback(empty_live):
    run(empty_live, "go")
    assert empty_live.types()[-1] == "start_playback"
    assert empty_live.is_playing


def test_stop(empty_live):
    empty_live.is_playing = True
    run(empty_live, "stop")
    assert not empty_live.is_playing


# -- mixer ----------------------------------------------------------------

def test_mute_and_unmute_by_role(studio_live):
    run(studio_live, "mute drums")
    assert studio_live.tracks[3]["muted"] is True
    run(studio_live, "unmute drums")
    assert studio_live.tracks[3]["muted"] is False


def test_solo_by_index_and_name(studio_live):
    run(studio_live, "solo 1", "unsolo bass")
    assert ("set_track_solo", {"track_index": 1, "solo": True}) in studio_live.calls
    assert ("set_track_solo", {"track_index": 1, "solo": False}) in studio_live.calls


def test_mute_unknown_target_is_an_error_without_side_effects(studio_live):
    with pytest.raises(ActionError, match="vocals"):
        run(studio_live, "mute vocals")
    assert "set_track_mute" not in studio_live.types()


def test_louder_moves_the_fader_in_steps_of_0_05(studio_live):
    run(studio_live, "louder bass 2")
    assert studio_live.tracks[1]["volume"] == pytest.approx(0.675)


def test_quieter_clamps_at_zero(studio_live):
    studio_live.tracks[1]["volume"] = 0.03
    run(studio_live, "quieter bass")
    assert studio_live.tracks[1]["volume"] == 0.0


# -- drum edits -----------------------------------------------------------------

def test_swing_without_a_beat_is_an_error(empty_live):
    with pytest.raises(ActionError, match="beat"):
        run(empty_live, "swing 60")


def test_swing_rewrites_the_drum_clip_with_shifted_off_beats(empty_live):
    run(empty_live, "beat trap", "swing 66")  # trap has 16th hats; house has nothing on the off-16ths
    notes = empty_live.batch_params("add_notes_to_clip")[-1]["notes"]
    assert empty_live.last_batch_types() == ["add_notes_to_clip"]
    assert any(abs(n["start_time"] * 4 - round(n["start_time"] * 4)) > 0.01 for n in notes)


def test_hats_off_removes_hats_and_keeps_the_style(empty_live):
    session, _ = run(empty_live, "beat trap", "hats off")
    notes = empty_live.batch_params("add_notes_to_clip")[-1]["notes"]
    assert not any(n["pitch"] in (42, 46) for n in notes)
    assert session.style == "trap"


def test_hats_setting_persists_through_swing(empty_live):
    run(empty_live, "beat trap", "hats off", "swing 60")
    notes = empty_live.batch_params("add_notes_to_clip")[-1]["notes"]
    assert not any(n["pitch"] in (42, 46) for n in notes)


# -- clear / kill -----------------------------------------------------------

def test_clear_deletes_only_abls_clip(studio_live):
    run(studio_live, "beat trap", "clear drums")
    assert studio_live.calls[-1] == ("delete_clip", {"track_index": 3, "clip_index": 1})
    assert studio_live.tracks[3]["slots"][0] is True


def test_clear_without_a_clip_is_an_error(studio_live):
    with pytest.raises(ActionError):
        run(studio_live, "clear keys")


def test_kill_refuses_tracks_abl_did_not_create(studio_live):
    with pytest.raises(ActionError, match="did not create"):
        run(studio_live, "kill drums")
    assert "delete_track" not in studio_live.types()


def test_kill_deletes_a_track_abl_created(studio_live):
    run(studio_live, "keys piano C", "kill keys")
    assert ("delete_track", {"track_index": 5}) in studio_live.calls
    assert len(studio_live.tracks) == 5


# -- misc -------------------------------------------------------------------

def test_undo_and_redo(empty_live):
    run(empty_live, "undo", "redo")
    assert empty_live.types() == ["undo", "redo"]


def test_status_reports_tempo_and_abl_clips(studio_live):
    _, (_, out) = run(studio_live, "beat trap", "status")
    assert "122" in out and "trap" in out


def test_tracks_lists_every_track(studio_live):
    _, (out,) = run(studio_live, "tracks")
    assert "Piano Stab" in out and "Garage Kit" in out


def test_help_returns_the_grammar(empty_live):
    _, (out,) = run(empty_live, "help")
    assert out == HELP


def test_full_lite_set_gives_a_clear_error_and_nothing_changes(studio_live):
    studio_live.track_limit = 5
    with pytest.raises(ActionError, match="8 tracks"):
        run(studio_live, "keys piano C-F")
    assert len(studio_live.tracks) == 5
    assert all(not any(t["notes"].values()) for t in studio_live.tracks)


# -- review regressions: stale slots, foreign clips, ownership, atomicity ---------------

def test_undo_then_beat_recovers_by_verifying_the_slot(studio_live):
    run(studio_live, "beat trap")
    studio_live.tracks[3]["slots"][1] = False  # the user pressed Cmd-Z in Live
    session, (out,) = run(studio_live, "beat house")
    assert "delete_clip" not in studio_live.last_batch_types()
    assert studio_live.batch_params("create_clip")[-1]["clip_index"] == 1
    assert session.clip_for("drums") == (3, 1)


def test_a_users_clip_in_abls_old_slot_is_never_touched(studio_live):
    run(studio_live, "beat trap")
    t = studio_live.tracks[3]
    t["clip_names"][1] = "my fill"
    t["notes"][1] = [{"pitch": 60, "start_time": 0.0, "duration": 1.0, "velocity": 100, "mute": False}]
    run(studio_live, "beat house")
    assert "delete_clip" not in studio_live.last_batch_types()
    assert studio_live.batch_params("create_clip")[-1]["clip_index"] == 2
    assert t["clip_names"][1] == "my fill" and t["notes"][1][0]["pitch"] == 60


def test_swing_refuses_to_rewrite_a_clip_it_did_not_write(studio_live):
    run(studio_live, "beat trap")
    studio_live.tracks[3]["clip_names"][1] = "my fill"
    before = list(studio_live.tracks[3]["notes"][1])
    with pytest.raises(ActionError, match="beat"):
        run(studio_live, "swing 60")
    assert studio_live.tracks[3]["notes"][1] == before


def test_go_skips_a_clip_that_disappeared_and_still_plays_the_rest(empty_live):
    session, _ = run(empty_live, "beat trap", "keys piano C")
    empty_live.tracks[0]["slots"][0] = False  # drums clip undone in Live
    out = execute(parse("go"), session)
    assert empty_live.is_playing
    assert empty_live.last_batch_types() == ["fire_clip", "start_playback"]
    assert "keys" in out and "drums" not in out.split(":")[-1]


def test_clear_on_a_vanished_clip_just_forgets_it(empty_live):
    session, _ = run(empty_live, "beat trap")
    empty_live.tracks[0]["slots"][0] = False
    out = execute(parse("clear drums"), session)
    assert "delete_clip" not in empty_live.types()[-1:]
    assert "gone" in out
    assert session.clip_for("drums") is None


def test_kill_refuses_a_track_the_user_renamed_to_the_role(studio_live):
    session = Session(studio_live)
    execute(parse("keys piano C"), session)
    del studio_live.tracks[5]  # user deletes abl's Keys track...
    studio_live._renumber()
    studio_live.add_user_track("Keys", ["Grand Piano"])  # ...and later names their own track Keys
    with pytest.raises(ActionError, match="did not create"):
        execute(parse("kill keys"), session)
    assert [t["name"] for t in studio_live.tracks][-1] == "Keys"


def test_track_creation_and_first_clip_are_one_batch(empty_live):
    run(empty_live, "keys piano C")
    assert empty_live.types()[:2] == ["get_session_snapshot", "batch"]
    assert empty_live.last_batch_types()[0] == "create_midi_track"


def test_a_track_added_by_the_user_in_the_race_window_is_reverted(studio_live):
    studio_live.before_batch = lambda: studio_live.add_user_track("Vocals")
    with pytest.raises(ActionError, match="reverted"):
        run(studio_live, "keys piano C")
    assert ("undo", {}) in studio_live.calls


def test_failed_keys_leaves_the_progression_unset(studio_live):
    studio_live.track_limit = 5
    session = Session(studio_live)
    with pytest.raises(ActionError):
        execute(parse("keys piano C-F"), session)
    assert session.progression is None


def test_failed_beat_leaves_style_unset(empty_live):
    empty_live.track_limit = 0
    session = Session(empty_live)
    with pytest.raises(ActionError):
        execute(parse("beat trap"), session)
    assert session.style is None


def test_mute_a_multi_word_track_name(studio_live):
    run(studio_live, "mute piano stab")
    assert studio_live.tracks[4]["muted"] is True
    assert studio_live.tracks[0]["muted"] is False


def test_louder_a_multi_word_track_name_with_steps(studio_live):
    run(studio_live, "louder piano stab 2")
    assert studio_live.tracks[4]["volume"] == pytest.approx(0.9)


def test_bass_third_and_fifth_come_from_the_chord_root_not_the_slash_bass(empty_live):
    run(empty_live, "keys piano C/E-C/E", "bass upright jazz")
    notes = empty_live.batch_params("add_notes_to_clip")[-1]["notes"]
    bar1 = sorted(n["pitch"] % 12 for n in notes if n["start_time"] < 3.0)
    assert bar1 == [4, 4, 7]  # E (slash bass) on the root beat, then E and G from C major
