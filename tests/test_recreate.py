import json

import pytest

from abl.actions import ActionError, execute
from abl.commands import parse
from abl.recreate import push, report, run_analyzer, sounds_for_analysis, sounds_for_tempo
from abl.session import Session


def note(pitch, start, dur=0.25, vel=100):
    return {"pitch": pitch, "start_time": start, "duration": dur, "velocity": vel}


@pytest.fixture
def analysis(tmp_path):
    audio = tmp_path / "audio.wav"
    audio.write_bytes(b"RIFF")
    drums = [note(36, b * 4.0) for b in range(20)] + [note(38, b * 4.0 + 2.0) for b in range(20)]
    bass = [note(33, b * 4.0, 3.5) for b in range(20)]
    keys = [note(p, b * 4.0, 3.9) for b in range(20) for p in (57, 60, 64)]
    return {
        "source": {"url": "https://youtu.be/x", "title": "Test Song", "duration_s": 52.0, "audio": str(audio)},
        "tempo": 92.0,
        "beats_per_bar": 4,
        "key": {"root": 9, "scale": "Minor", "name": "A minor", "confidence": 0.7},
        "sections": [
            {"label": "intro", "start_bar": 0, "bars": 4, "energy": 0.3},
            {"label": "verse", "start_bar": 4, "bars": 8, "energy": 0.6},
            {"label": "chorus", "start_bar": 12, "bars": 8, "energy": 1.0},
        ],
        "chords": [{"bar": b, "symbol": s} for b, s in enumerate(["Am", "F", "C", "G"] * 5)],
        "tracks": {"drums": drums, "bass": bass, "keys": keys, "lead": []},
    }


def test_push_sets_tempo_and_key(empty_live, analysis):
    push(Session(empty_live), analysis, progress=lambda s: None)
    assert empty_live.tempo == 92.0
    assert empty_live.scale == (9, "Minor")


def test_push_creates_missing_scenes_and_names_them_after_sections(empty_live, analysis):
    empty_live.scene_count = 2
    push(Session(empty_live), analysis, progress=lambda s: None)
    assert empty_live.scene_count == 3
    assert empty_live.scene_names == {0: "1 intro", 1: "2 verse", 2: "3 chorus"}


def test_push_writes_one_clip_per_role_per_section_in_the_section_slot(empty_live, analysis):
    push(Session(empty_live), analysis, progress=lambda s: None)
    drums = next(t for t in empty_live.tracks if t["name"] == "Drums")
    assert drums["slots"][:3] == [True, True, True] and not any(drums["slots"][3:])
    lengths = {c["clip_index"]: c["length"] for c in empty_live.batch_params("create_clip") if c["track_index"] == drums["index"]}
    assert lengths == {0: 16.0, 1: 32.0, 2: 32.0}
    verse = drums["notes"][1]
    assert min(n["start_time"] for n in verse) == 0.0
    assert max(n["start_time"] + n["duration"] for n in verse) <= 32.0
    assert drums["clip_names"][1] == "abl Test Song verse"


def test_push_skips_roles_with_no_notes(empty_live, analysis):
    push(Session(empty_live), analysis, progress=lambda s: None)
    assert not any(t["name"] == "Lead" for t in empty_live.tracks)


def test_push_loads_sounds_on_new_role_tracks_by_tempo(empty_live, analysis):
    push(Session(empty_live), analysis, progress=lambda s: None)
    uris = [c["item_uri"] for c in empty_live.batch_params("load_browser_item")]
    assert "query:Drums#FileId_5419" in uris  # 92 bpm -> Dry Session Kit


def test_sounds_for_tempo():
    assert sounds_for_tempo(150)["drums"].name == "808 Core Kit"
    assert sounds_for_tempo(124)["drums"].name == "909 Core Kit"
    assert sounds_for_tempo(92)["drums"].name == "Dry Session Kit"


def test_push_uses_an_empty_template_audio_track_as_reference_and_mutes_it(studio_live, analysis):
    push(Session(studio_live), analysis, progress=lambda s: None)
    ref = next(t for t in studio_live.tracks if t["name"] == "Reference")
    assert ref["type"] == "audio"
    assert studio_live.audio_clips[(ref["index"], 0)] == analysis["source"]["audio"]
    assert ref["muted"] is True


def test_push_never_takes_an_audio_track_that_has_clips(empty_live, analysis):
    empty_live.add_user_track("4-Audio", kind="audio")
    empty_live.tracks[0]["slots"][0] = True
    empty_live.track_limit = 4  # drums, bass, keys will fill the set
    out = push(Session(empty_live), analysis, progress=lambda s: None)
    assert not any(t["name"] == "Reference" for t in empty_live.tracks)
    assert "no reference" in out.lower()


def test_push_skips_a_section_slot_holding_a_users_clip(studio_live, analysis):
    studio_live.tracks[3]["slots"][1] = True  # user's own clip on Drums, slot 1
    studio_live.tracks[3]["clip_names"][1] = "my fill"
    out = push(Session(studio_live), analysis, progress=lambda s: None)
    assert studio_live.tracks[3]["clip_names"][1] == "my fill"
    assert studio_live.tracks[3]["slots"][0] is True and studio_live.tracks[3]["slots"][2] is True
    assert "skipped" in out.lower()


def test_push_replaces_its_own_earlier_clips(empty_live, analysis):
    session = Session(empty_live)
    push(session, analysis, progress=lambda s: None)
    push(session, analysis, progress=lambda s: None)
    drums = next(t for t in empty_live.tracks if t["name"] == "Drums")
    assert drums["slots"][:3] == [True, True, True]
    assert len([c for c in empty_live.batch_params("delete_clip") if c["track_index"] == drums["index"]]) == 3


def test_push_fires_the_first_scene_and_go_replays_it(empty_live, analysis):
    session = Session(empty_live)
    push(session, analysis, progress=lambda s: None)
    assert empty_live.fired_scenes == [0]
    execute(parse("go"), session)
    assert empty_live.last_batch_types()[-1] == "start_playback"
    assert empty_live.batch_params("fire_clip")[-1]["clip_index"] == 0


def test_push_caps_sections_at_eight_scenes(empty_live, analysis):
    analysis["sections"] = [{"label": f"s{i}", "start_bar": i * 2, "bars": 2, "energy": 0.5} for i in range(10)]
    push(Session(empty_live), analysis, progress=lambda s: None)
    assert empty_live.scene_count == 8
    drums = next(t for t in empty_live.tracks if t["name"] == "Drums")
    assert sum(drums["slots"]) == 8


def test_push_reports_progress_lines(empty_live, analysis):
    lines = []
    push(Session(empty_live), analysis, progress=lines.append)
    assert any("scene" in line.lower() for line in lines)


def test_report_lists_tempo_key_and_sections(analysis):
    text = report(analysis)
    assert "92" in text and "A minor" in text
    assert "chorus" in text and "8 bars" in text
    assert "Am-F-C-G" in text


def test_run_analyzer_streams_progress_and_loads_the_json(tmp_path):
    out = tmp_path / "analysis.json"
    out.write_text(json.dumps({"tempo": 100.0, "sections": [], "tracks": {}}))

    def runner(args, progress):
        progress("download: ok")
        progress("stems: ok")
        return str(out)

    seen = []
    data = run_analyzer("https://youtu.be/x", fresh=True, progress=seen.append, runner=runner)
    assert data["tempo"] == 100.0
    assert seen == ["download: ok", "stems: ok"]


def test_run_analyzer_failure_is_an_action_error():
    def runner(args, progress):
        raise RuntimeError("yt-dlp: video unavailable")

    with pytest.raises(ActionError, match="unavailable"):
        run_analyzer("https://youtu.be/x", fresh=False, progress=lambda s: None, runner=runner)


def test_run_analyzer_passes_fresh_and_source(tmp_path):
    out = tmp_path / "a.json"
    out.write_text("{}")
    seen = {}

    def runner(args, progress):
        seen["args"] = args
        return str(out)

    run_analyzer("song.mp3", fresh=True, progress=lambda s: None, runner=runner)
    assert "song.mp3" in seen["args"] and "--fresh" in seen["args"]


def test_analyze_command_prints_the_report_without_touching_live(empty_live, analysis, monkeypatch):
    monkeypatch.setattr("abl.recreate.run_analyzer", lambda source, fresh, progress, runner=None: analysis)
    lines = []
    out = execute(parse("analyze https://youtu.be/x"), Session(empty_live), progress=lines.append)
    assert "A minor" in out
    assert empty_live.calls == []


def test_recreate_command_runs_analysis_then_pushes(empty_live, analysis, monkeypatch):
    monkeypatch.setattr("abl.recreate.run_analyzer", lambda source, fresh, progress, runner=None: analysis)
    out = execute(parse("recreate https://youtu.be/x"), Session(empty_live), progress=lambda s: None)
    assert empty_live.tempo == 92.0
    assert "Test Song" in out


def test_push_refuses_before_changing_anything_when_the_set_cannot_fit_the_roles(studio_live, analysis):
    for name in ("Choir", "Choir 2", "Pad"):
        studio_live.add_user_track(name)  # a full Lite set: 8 tracks, Drums and Bass exist, Keys would be a 9th
    studio_live.track_limit = 8
    with pytest.raises(ActionError, match="Live Lite allows 8"):
        push(Session(studio_live), analysis, progress=lambda s: None)
    assert studio_live.tempo == 122.0 and studio_live.scene_names == {}
    assert studio_live.batches() == []


def test_push_falls_back_to_the_scenes_live_allows(empty_live, analysis):
    empty_live.scene_count = 2
    empty_live.scene_limit = 2
    out = push(Session(empty_live), analysis, progress=lambda s: None)
    assert empty_live.scene_count == 2
    drums = next(t for t in empty_live.tracks if t["name"] == "Drums")
    assert sum(drums["slots"]) == 2
    assert "2 scenes" in out


# -- Arrangement view -------------------------------------------------------------------

def _track(live, name):
    return next(t for t in live.tracks if t["name"] == name)


def test_push_lays_every_section_into_the_arrangement_in_order(empty_live, analysis):
    push(Session(empty_live), analysis, progress=lambda s: None)
    drums = _track(empty_live, "Drums")
    clips = empty_live.arrangement[drums["index"]]
    assert [(c["start_time"], c["length"]) for c in clips] == [(0.0, 16.0), (16.0, 32.0), (48.0, 32.0)]
    assert [c["name"] for c in clips] == ["abl Test Song intro", "abl Test Song verse", "abl Test Song chorus"]
    assert empty_live.arrangement[_track(empty_live, "Bass")["index"]]


def test_push_adds_a_named_locator_per_section_and_returns_the_playhead(empty_live, analysis):
    push(Session(empty_live), analysis, progress=lambda s: None)
    assert empty_live.locators == [(0.0, "1 intro"), (16.0, "2 verse"), (48.0, "3 chorus")]
    assert empty_live.song_time == 0.0


def test_push_ends_in_arrangement_view(empty_live, analysis):
    push(Session(empty_live), analysis, progress=lambda s: None)
    assert empty_live.view == "Arranger"


def test_push_never_lays_over_a_foreign_arrangement_clip(studio_live, analysis):
    studio_live.arrangement[3] = [{"name": "my take", "start_time": 8.0, "end_time": 40.0, "length": 32.0}]
    out = push(Session(studio_live), analysis, progress=lambda s: None)
    assert studio_live.arrangement[3] == [{"name": "my take", "start_time": 8.0, "end_time": 40.0, "length": 32.0}]
    assert studio_live.arrangement.get(1)  # Bass was laid
    assert "arrangement" in out.lower() and "Drums" in out


def test_push_rerun_replaces_its_own_arrangement_clips(empty_live, analysis):
    session = Session(empty_live)
    push(session, analysis, progress=lambda s: None)
    push(session, analysis, progress=lambda s: None)
    drums = _track(empty_live, "Drums")
    assert len(empty_live.arrangement[drums["index"]]) == 3
    assert len(empty_live.locators) == 3


def test_push_skips_arrangement_for_sections_whose_slot_was_skipped(studio_live, analysis):
    studio_live.tracks[3]["slots"][1] = True  # user's clip in Drums slot 1 -> verse not written
    studio_live.tracks[3]["clip_names"][1] = "my fill"
    push(Session(studio_live), analysis, progress=lambda s: None)
    starts = [c["start_time"] for c in studio_live.arrangement[3]]
    assert 16.0 not in starts


# -- instrument-aware sounds -------------------------------------------------------------

def test_sounds_for_analysis_picks_piano_guitar_or_tempo_default_for_keys(analysis):
    assert sounds_for_analysis({**analysis, "keys_source": "piano"})["keys"].name == "Grand Piano"
    assert sounds_for_analysis({**analysis, "keys_source": "guitar"})["keys"].name == "Guitar Electric Clean"
    assert sounds_for_analysis({**analysis, "keys_source": "other"})["keys"].name == "E-Piano Rhodish"
    assert sounds_for_analysis(analysis)["drums"].name == "Dry Session Kit"


def test_push_loads_a_guitar_when_the_keys_came_from_the_guitar_stem(empty_live, analysis):
    push(Session(empty_live), {**analysis, "keys_source": "guitar"}, progress=lambda s: None)
    uris = [c["item_uri"] for c in empty_live.batch_params("load_browser_item")]
    assert "query:Sounds#Guitar%20&%20Plucked:FileId_5054" in uris


def test_report_names_the_engines_when_present(analysis):
    text = report({**analysis, "engine": {"beats": "all-in-one", "drums": "adtof", "keys": "piano-transcription"}})
    assert "all-in-one" in text and "adtof" in text


def test_report_lists_the_chosen_sounds_with_reasons(analysis):
    text = report({**analysis, "kit": {"name": "Chicago Kit", "score": 0.94}, "instrument_tags": {"bass": [("a deep 808 sub bass", 0.4)], "keys": [("a hammond organ", 0.5)]}})
    assert "Chicago Kit" in text and "closest kit" in text
    assert "808" in text and "hammond organ" in text
