"""Against a real Live. Skipped unless ABL_LIVE=1. Never touches a track it did not create."""

import json
import os
import time

import pytest

from abl.catalog import GM_PAD_MAP
from abl.patterns import render_drums
from abl.wire import LiveClient, LiveCommandError

pytestmark = pytest.mark.skipif(os.environ.get("ABL_LIVE") != "1", reason="set ABL_LIVE=1 with Live running")
SCRATCH = "abl-test"


@pytest.mark.live
def test_batch_of_read_only_commands_round_trips():
    client = LiveClient()
    try:
        started = time.perf_counter()
        reply = client.batch([
            {"type": "get_session_info", "params": {}},
            {"type": "get_session_snapshot", "params": {}},
        ])
        elapsed = (time.perf_counter() - started) * 1000
        text = json.dumps(reply)
        assert "tempo" in text and "tracks" in text
        print(f"\nread-only batch of 2: {elapsed:.0f} ms")
    finally:
        client.close()


@pytest.mark.live
def test_scratch_track_round_trip_and_batch_timing():
    client = LiveClient()
    before = client.send("get_session_snapshot")["track_count"]
    try:
        index = client.send("create_midi_track", {"index": -1})["index"]
    except LiveCommandError as exc:
        client.close()
        pytest.skip(f"Live refused a scratch track ({exc}); Live Lite caps a set at 8 tracks and this set has {before}")
    try:
        notes = render_drums("trap", GM_PAD_MAP)
        started = time.perf_counter()
        client.batch([
            {"type": "set_track_name", "params": {"track_index": index, "name": SCRATCH}},
            {"type": "create_clip", "params": {"track_index": index, "clip_index": 0, "length": 8.0}},
            {"type": "add_notes_to_clip", "params": {"track_index": index, "clip_index": 0, "notes": notes}},
            {"type": "set_clip_loop", "params": {"track_index": index, "clip_index": 0, "start": 0.0, "end": 8.0, "looping": True}},
            {"type": "set_clip_name", "params": {"track_index": index, "clip_index": 0, "name": SCRATCH}},
        ])
        batch_ms = (time.perf_counter() - started) * 1000
        back = client.send("get_clip_notes", {"track_index": index, "clip_index": 0})["notes"]
        written = {(n["pitch"], round(n["start_time"], 3)) for n in notes}
        read = {(n["pitch"], round(n["start_time"], 3)) for n in back}
        assert read == written
        assert client.send("get_track_info", {"track_index": index})["name"] == SCRATCH
        print(f"\nwrite batch of 5: {batch_ms:.0f} ms")
    finally:
        client.send("delete_track", {"track_index": index})
        client.close()
    assert LiveClient().send("get_session_snapshot")["track_count"] == before
