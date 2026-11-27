"""A tiny in-memory stand-in for Live's Remote Script: enough state and the same failure modes."""

from __future__ import annotations

import copy

import pytest

from abl.wire import LiveCommandError

SLOTS = 8


def _track(index: int, name: str, devices: list[str], slots: list[bool] | None = None, volume: float = 0.85, kind: str = "midi", track_id: int | None = None) -> dict:
    return {
        "index": index,
        "id": track_id if track_id is not None else 100 + index,
        "name": name,
        "type": kind,
        "muted": False,
        "soloed": False,
        "armed": False,
        "volume": volume,
        "devices": list(devices),
        "slots": slots or [False] * SLOTS,
        "clip_names": {},
        "notes": {},
    }


class FakeLive:
    """Answers the wire commands abl uses and mutates its own state like Live would."""

    def __init__(self, tracks: list[dict] | None = None, tempo: float = 122.0, root_note: int = 7, scale_name: str = "Minor"):
        self.tracks = tracks if tracks is not None else []
        self.tempo = tempo
        self.root_note = root_note
        self.scale_name = scale_name
        self.is_playing = False
        self.calls: list[tuple[str, dict]] = []
        self.undo_count = 0
        self.track_limit: int | None = None  # Live Lite refuses a 9th track
        self.scene_count = SLOTS
        self.scene_limit: int | None = None  # Live Lite refuses a 9th scene
        self.scene_names: dict[int, str] = {}
        self.fired_scenes: list[int] = []
        self.scale: tuple[int, str] = (0, "Major")
        self.audio_clips: dict[tuple[int, int], str] = {}
        self.arrangement: dict[int, list[dict]] = {}  # track index -> clips laid in Arrangement view
        self.song_time = 0.0
        self.locators: list[tuple[float, str]] = []
        self.view = "Session"
        self.before_batch = None  # hook: something the user does right before a batch lands
        self._next_id = 1000

    # -- what abl's LiveClient exposes -------------------------------------
    def send(self, command_type: str, params: dict | None = None):
        params = params or {}
        self.calls.append((command_type, copy.deepcopy(params)))
        return self._dispatch(command_type, params)

    def batch(self, commands: list[dict]):
        self.calls.append(("batch", {"commands": copy.deepcopy(commands)}))
        if self.before_batch is not None:
            hook, self.before_batch = self.before_batch, None
            hook()
        results = []
        for i, c in enumerate(commands):
            try:
                results.append({"type": c["type"], "result": self._dispatch(c["type"], c.get("params", {}))})
            except LiveCommandError as exc:
                raise LiveCommandError(f"batch failed at step {i} of {len(commands)}: {exc}") from None
        return {"executed": len(results), "results": results}

    # -- helpers for tests ---------------------------------------------------
    def types(self) -> list[str]:
        return [t for t, _ in self.calls]

    def batches(self) -> list[list[dict]]:
        return [p["commands"] for t, p in self.calls if t == "batch"]

    def last_batch_types(self) -> list[str]:
        return [c["type"] for c in self.batches()[-1]]

    def batch_params(self, command_type: str) -> list[dict]:
        return [c.get("params", {}) for b in self.batches() for c in b if c["type"] == command_type]

    def add_user_track(self, name: str, devices: list[str] | None = None, kind: str = "midi", at: int | None = None) -> dict:
        """Something the user does in Live: add a track with a fresh id."""
        self._next_id += 1
        track = _track(0, name, devices or [], kind=kind, track_id=self._next_id)
        self.tracks.insert(len(self.tracks) if at is None else at, track)
        self._renumber()
        return track

    def _renumber(self) -> None:
        for i, t in enumerate(self.tracks):
            t["index"] = i

    # -- Live behaviour --------------------------------------------------------
    def _t(self, index: int) -> dict:
        if not 0 <= index < len(self.tracks):
            raise LiveCommandError("Track index out of range")
        return self.tracks[index]

    def _slot(self, p: dict, must_have_clip: bool) -> dict:
        t = self._t(p["track_index"])
        if not 0 <= p["clip_index"] < SLOTS:
            raise LiveCommandError("Clip index out of range")
        if must_have_clip and not t["slots"][p["clip_index"]]:
            raise LiveCommandError("No clip in slot")
        return t

    def _dispatch(self, kind: str, p: dict):
        if kind == "get_session_snapshot":
            return {
                "tempo": self.tempo,
                "is_playing": self.is_playing,
                "track_count": len(self.tracks),
                "scene_count": self.scene_count,
                "tracks": [
                    {k: v for k, v in t.items() if k not in ("slots", "notes", "clip_names")} | {"clips": sum(t["slots"])}
                    for t in self.tracks
                ],
            }
        if kind == "get_session_info":
            return {"tempo": self.tempo, "is_playing": self.is_playing, "track_count": len(self.tracks), "root_note": self.root_note, "scale_name": self.scale_name, "scene_count": self.scene_count}
        if kind == "get_track_info":
            t = self._t(p["track_index"])
            slots = []
            for i, has in enumerate(t["slots"]):
                entry = {"index": i, "has_clip": has}
                if has:
                    entry["name"] = t["clip_names"].get(i, "")
                slots.append(entry)
            return {"index": t["index"], "name": t["name"], "clip_slots": slots, "devices": [{"index": i, "name": d} for i, d in enumerate(t["devices"])]}
        if kind == "create_midi_track":
            if self.track_limit is not None and len(self.tracks) >= self.track_limit:
                raise LiveCommandError("Couldn't create track")
            self._next_id += 1
            index = len(self.tracks)
            self.tracks.append(_track(index, f"{index + 1}-MIDI", [], track_id=self._next_id))
            return {"index": index, "name": self.tracks[index]["name"]}
        if kind == "create_audio_track":
            if self.track_limit is not None and len(self.tracks) >= self.track_limit:
                raise LiveCommandError("Couldn't create track")
            self._next_id += 1
            index = len(self.tracks)
            self.tracks.append(_track(index, f"{index + 1}-Audio", [], kind="audio", track_id=self._next_id))
            return {"index": index, "name": self.tracks[index]["name"]}
        if kind == "create_audio_clip":
            t = self._slot(p, must_have_clip=False)
            if t["type"] != "audio":
                raise LiveCommandError("Audio clips need an audio track")
            if t["slots"][p["clip_index"]]:
                raise LiveCommandError("Clip slot already has a clip")
            t["slots"][p["clip_index"]] = True
            t["clip_names"][p["clip_index"]] = ""
            self.audio_clips[(p["track_index"], p["clip_index"])] = p["path"]
            return {"path": p["path"]}
        if kind == "create_scene":
            if self.scene_limit is not None and self.scene_count >= self.scene_limit:
                raise LiveCommandError("Couldn't create scene")
            self.scene_count += 1
            return {"scene_count": self.scene_count}
        if kind == "set_scene_name":
            if not 0 <= p["scene_index"] < self.scene_count:
                raise LiveCommandError("Scene index out of range")
            self.scene_names[p["scene_index"]] = p["name"]
            return {"name": p["name"]}
        if kind == "fire_scene":
            if not 0 <= p["scene_index"] < self.scene_count:
                raise LiveCommandError("Scene index out of range")
            self.fired_scenes.append(p["scene_index"])
            self.is_playing = True
            return {}
        if kind == "get_arrangement_clips":
            self._t(p["track_index"])
            return {"clips": list(self.arrangement.get(p["track_index"], []))}
        if kind == "duplicate_session_clip_to_arrangement":
            t = self._slot(p, must_have_clip=True)
            length = 4.0 * max(1, len(t["notes"].get(p["clip_index"], [])) and 1) if False else t.get("clip_lengths", {}).get(p["clip_index"], 4.0)
            start = float(p["destination_time"])
            end = start + length
            kept = [c for c in self.arrangement.get(p["track_index"], []) if c["end_time"] <= start or c["start_time"] >= end]
            kept.append({"name": t["clip_names"].get(p["clip_index"], ""), "start_time": start, "end_time": end, "length": length})
            self.arrangement[p["track_index"]] = sorted(kept, key=lambda c: c["start_time"])
            return {"start_time": start, "end_time": end}
        if kind == "set_current_song_time":
            self.song_time = float(p.get("time", 0.0))
            return {"current_song_time": self.song_time}
        if kind == "create_locator":  # Live renames a locator that already sits at the playhead
            for i, (t, _) in enumerate(self.locators):
                if abs(t - self.song_time) < 1e-3:
                    self.locators[i] = (t, p.get("name") or "")
                    return {"time": t, "name": p.get("name"), "created": False}
            self.locators.append((self.song_time, p.get("name") or ""))
            return {"time": self.song_time, "name": p.get("name"), "created": True}
        if kind == "switch_to_arrangement_view":
            self.view = "Arranger"
            return {"view": "Arranger"}
        if kind == "set_song_scale":
            self.scale = (int(p.get("root_note", self.scale[0])), p.get("scale_name", self.scale[1]))
            self.root_note, self.scale_name = self.scale
            return {"root_note": self.scale[0], "scale_name": self.scale[1]}
        if kind == "set_track_name":
            self._t(p["track_index"])["name"] = p["name"]
            return {"name": p["name"]}
        if kind == "load_browser_item":
            t = self._t(p["track_index"])
            t["devices"] = ["loaded:" + p["item_uri"].rsplit("FileId_", 1)[-1]]
            return {"uri": p["item_uri"]}
        if kind == "create_clip":
            t = self._slot(p, must_have_clip=False)
            if t["type"] != "midi":
                raise LiveCommandError("MIDI clips need a MIDI track")
            if t["slots"][p["clip_index"]]:
                raise LiveCommandError("Clip slot already has a clip")
            t["slots"][p["clip_index"]] = True
            t["notes"][p["clip_index"]] = []
            t["clip_names"][p["clip_index"]] = ""
            t.setdefault("clip_lengths", {})[p["clip_index"]] = float(p["length"])
            return {"length": p["length"]}
        if kind == "delete_clip":
            t = self._slot(p, must_have_clip=True)
            t["slots"][p["clip_index"]] = False
            t["notes"].pop(p["clip_index"], None)
            t["clip_names"].pop(p["clip_index"], None)
            return {"deleted": True}
        if kind == "add_notes_to_clip":
            t = self._slot(p, must_have_clip=True)
            t["notes"][p["clip_index"]] = list(p["notes"])
            return {"note_count": len(p["notes"])}
        if kind == "get_clip_notes":
            t = self._slot(p, must_have_clip=True)
            return {"notes": t["notes"].get(p["clip_index"], [])}
        if kind == "set_clip_name":
            t = self._slot(p, must_have_clip=True)
            t["clip_names"][p["clip_index"]] = p["name"]
            return {"name": p["name"]}
        if kind in ("set_clip_loop", "fire_clip", "stop_clip"):
            self._slot(p, must_have_clip=True)
            if kind == "fire_clip":
                self.is_playing = True
            return {}
        if kind == "set_tempo":
            self.tempo = float(p["tempo"])
            return {"tempo": self.tempo}
        if kind == "start_playback":
            self.is_playing = True
            return {}
        if kind == "stop_playback":
            self.is_playing = False
            return {}
        if kind == "set_track_mute":
            self._t(p["track_index"])["muted"] = bool(p["mute"])
            return {"mute": p["mute"]}
        if kind == "set_track_solo":
            self._t(p["track_index"])["soloed"] = bool(p["solo"])
            return {"solo": p["solo"]}
        if kind == "set_track_volume":
            self._t(p["track_index"])["volume"] = float(p["volume"])
            return {"volume": p["volume"]}
        if kind == "delete_track":
            self._t(p["track_index"])
            del self.tracks[p["track_index"]]
            self._renumber()
            return {"deleted": True}
        if kind in ("undo", "redo"):
            self.undo_count += 1
            return {kind: True}
        raise LiveCommandError(f"FakeLive: unknown command {kind}")


@pytest.fixture
def empty_live() -> FakeLive:
    return FakeLive()


@pytest.fixture
def studio_live() -> FakeLive:
    """Mirrors the user's real set: Piano, Bass, an audio track, Drums with a Garage Kit, Piano Stab."""
    return FakeLive(
        tracks=[
            _track(0, "Piano", ["Grand Piano"], slots=[True] + [False] * 7),
            _track(1, "Bass", ["Basic Mello Bass"], slots=[True] + [False] * 7, volume=0.575),
            _track(2, "3-Audio", [], kind="audio"),
            _track(3, "Drums", ["Garage Kit"], slots=[True] + [False] * 7),
            _track(4, "Piano Stab", ["E-Piano Rhodish"], slots=[True] + [False] * 7, volume=0.8),
        ]
    )
