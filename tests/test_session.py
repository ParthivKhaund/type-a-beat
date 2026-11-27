import pytest

from abl.session import Session, SessionError


def test_find_track_by_role_name(studio_live):
    session = Session(studio_live)
    session.refresh()
    assert session.find_track("drums").index == 3


def test_find_track_by_index_string(studio_live):
    session = Session(studio_live)
    session.refresh()
    assert session.find_track("1").name == "Bass"


def test_find_track_by_exact_name_case_insensitive(studio_live):
    session = Session(studio_live)
    session.refresh()
    assert session.find_track("piano stab").index == 4


def test_find_track_missing_returns_none(studio_live):
    session = Session(studio_live)
    session.refresh()
    assert session.find_track("vocals") is None


def test_plan_role_track_reuses_an_existing_track(studio_live):
    session = Session(studio_live)
    session.refresh()
    assert session.plan_role_track("drums") == (3, False)
    assert not session.owns("drums")


def test_plan_role_track_predicts_the_next_index_without_sending_anything(studio_live):
    session = Session(studio_live)
    session.refresh()
    assert session.plan_role_track("keys") == (5, True)
    assert studio_live.types() == ["get_session_snapshot"]
    assert not session.owns("keys")


def test_record_created_then_refresh_pins_ownership_to_the_track_id(studio_live):
    session = Session(studio_live)
    session.refresh()
    studio_live.send("create_midi_track", {"index": -1})
    studio_live.send("set_track_name", {"track_index": 5, "name": "Keys"})
    session.record_created("keys", 5)
    session.refresh()
    assert session.owns("keys")
    assert session.owned_track("keys").id == studio_live.tracks[5]["id"]


def test_owned_track_is_none_when_the_track_at_the_role_name_has_another_id(studio_live):
    session = Session(studio_live)
    session.refresh()
    studio_live.send("create_midi_track", {"index": -1})
    studio_live.send("set_track_name", {"track_index": 5, "name": "Keys"})
    session.record_created("keys", 5)
    session.refresh()
    del studio_live.tracks[5]
    studio_live._renumber()
    studio_live.add_user_track("Keys")
    session.refresh()
    assert session.owned_track("keys") is None


def test_find_track_by_role_prefers_a_midi_track(studio_live):
    studio_live.add_user_track("Drums", kind="audio", at=0)
    session = Session(studio_live)
    session.refresh()
    assert session.find_track("drums").type == "midi"
    assert session.find_track("drums").index == 4


def test_find_track_by_role_ignores_an_audio_track_alone(empty_live):
    empty_live.add_user_track("Drums", kind="audio")
    session = Session(empty_live)
    session.refresh()
    assert session.find_track("drums") is None


def test_first_empty_slot_skips_filled_slots(studio_live):
    session = Session(studio_live)
    assert session.first_empty_slot(3) == 1


def test_first_empty_slot_raises_when_full(empty_live):
    empty_live.send("create_midi_track", {"index": -1})
    empty_live.tracks[0]["slots"] = [True] * 8
    session = Session(empty_live)
    with pytest.raises(SessionError, match="empty"):
        session.first_empty_slot(0)


def test_remembered_clip_resolves_to_a_track_index_after_refresh(studio_live):
    session = Session(studio_live)
    session.refresh()
    session.remember_clip("drums", 2, "abl trap")
    assert session.clip_for("drums") == (3, 2)


def test_remembered_clip_survives_a_track_being_added_before_it(studio_live):
    session = Session(studio_live)
    session.refresh()
    session.remember_clip("drums", 0, "abl trap")
    studio_live.tracks.insert(0, dict(studio_live.tracks[0], name="Intro", index=0))
    for i, t in enumerate(studio_live.tracks):
        t["index"] = i
    session.refresh()
    assert session.clip_for("drums") == (4, 0)


def test_clip_for_unknown_role_is_none(studio_live):
    session = Session(studio_live)
    session.refresh()
    assert session.clip_for("bass") is None


def test_forget_clip(studio_live):
    session = Session(studio_live)
    session.refresh()
    session.remember_clip("drums", 0, "abl trap")
    session.forget_clip("drums")
    assert session.clip_for("drums") is None


def test_info_is_read_lazily_once_per_refresh(studio_live):
    session = Session(studio_live)
    session.refresh()
    assert session.info()["root_note"] == 7
    session.info()
    assert studio_live.types().count("get_session_info") == 1
    session.refresh()
    session.info()
    assert studio_live.types().count("get_session_info") == 2


def test_locate_slot_reuses_a_remembered_clip_that_is_still_abls(studio_live):
    session = Session(studio_live)
    session.refresh()
    studio_live.tracks[3]["slots"][2] = True
    studio_live.tracks[3]["clip_names"][2] = "abl trap"
    session.remember_clip("drums", 2, "abl trap")
    assert session.locate_slot("drums", 3) == (2, True)


def test_locate_slot_forgets_a_slot_holding_someone_elses_clip(studio_live):
    session = Session(studio_live)
    session.refresh()
    studio_live.tracks[3]["slots"][2] = True
    studio_live.tracks[3]["clip_names"][2] = "my fill"
    session.remember_clip("drums", 2, "abl trap")
    assert session.locate_slot("drums", 3) == (1, False)
    assert session.clip_for("drums") is None
