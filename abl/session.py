"""What abl knows about the open Live set: tracks, which ones it created, and the clips it wrote."""

from __future__ import annotations

from dataclasses import dataclass, field

from abl.catalog import ROLE_TRACK_NAMES
from abl.wire import LiveCommandError

LITE_TRACK_LIMIT = 8
FULL_SET_MSG = (
    "Live could not create a track (Live Lite allows {limit} tracks; this set has {count}). "
    "Free a track, or rename an existing track to the role name (Drums, Bass, Keys, Lead, Reference) and abl will use it."
)


class SessionError(Exception):
    pass


@dataclass(frozen=True)
class Track:
    index: int
    id: int
    name: str
    type: str
    devices: tuple[str, ...]
    clips: int
    muted: bool
    soloed: bool
    volume: float

    @classmethod
    def from_snapshot(cls, raw: dict) -> "Track":
        return cls(
            index=int(raw["index"]),
            id=int(raw.get("id", -1)),
            name=str(raw.get("name", "")),
            type=str(raw.get("type", "")),
            devices=tuple(raw.get("devices", ())),
            clips=int(raw.get("clips", 0)),
            muted=bool(raw.get("muted", False)),
            soloed=bool(raw.get("soloed", False)),
            volume=float(raw.get("volume", 0.85)),
        )


@dataclass
class ClipRef:
    slot: int
    name: str
    description: str = ""


@dataclass
class OwnedTrack:
    index: int
    id: int | None = None  # pinned on the first refresh after creation


@dataclass
class Session:
    client: object
    tracks: list[Track] = field(default_factory=list)
    tempo: float = 0.0
    is_playing: bool = False
    style: str | None = None
    progression: list | None = None
    hats: str = "normal"
    swing: int | None = None
    _info: dict | None = None
    _clips: dict[str, ClipRef] = field(default_factory=dict)
    _owned: dict[str, OwnedTrack] = field(default_factory=dict)

    # -- reading Live -----------------------------------------------------------
    def refresh(self) -> dict:
        snapshot = self.client.send("get_session_snapshot")
        self.tracks = [Track.from_snapshot(t) for t in snapshot.get("tracks", [])]
        self.tempo = float(snapshot.get("tempo", 0.0))
        self.is_playing = bool(snapshot.get("is_playing", False))
        self._info = None
        self._pin_pending_ids()
        return snapshot

    def info(self) -> dict:
        if self._info is None:
            self._info = self.client.send("get_session_info")
        return self._info

    def batch(self, commands: list[dict]) -> list[dict]:
        """One round trip, one undo step. Live's track-cap refusal becomes a readable SessionError."""
        try:
            reply = self.client.batch(commands)
        except LiveCommandError as exc:
            if "create track" in str(exc).lower():
                raise SessionError(FULL_SET_MSG.format(limit=LITE_TRACK_LIMIT, count=len(self.tracks))) from None
            raise
        return list(reply.get("results", [])) if isinstance(reply, dict) else []

    # -- tracks -------------------------------------------------------------------
    def find_track(self, target: str) -> Track | None:
        key = target.lower()
        if key.isdigit():
            index = int(key)
            return next((t for t in self.tracks if t.index == index), None)
        if key in ROLE_TRACK_NAMES:
            wanted = ROLE_TRACK_NAMES[key].lower()
            return next((t for t in self.tracks if t.name.lower() == wanted and t.type == "midi"), None)
        return next((t for t in self.tracks if t.name.lower() == key), None)

    def plan_role_track(self, role: str) -> tuple[int, bool]:
        """Index the role track has, or will have once `create_midi_track` runs at the end of the set."""
        existing = self.find_track(role)
        if existing is not None:
            return existing.index, False
        return len(self.tracks), True

    def record_created(self, role: str, index: int) -> None:
        self._owned[role] = OwnedTrack(index=index)

    def _pin_pending_ids(self) -> None:
        for role, owned in self._owned.items():
            if owned.id is not None:
                continue
            wanted = ROLE_TRACK_NAMES[role].lower()
            at_index = next((t for t in self.tracks if t.index == owned.index), None)
            if at_index is not None and at_index.name.lower() == wanted:
                owned.id = at_index.id

    def owns(self, role: str) -> bool:
        return role in self._owned

    def owned_track(self, role: str) -> Track | None:
        owned = self._owned.get(role)
        if owned is None or owned.id is None:
            return None
        return next((t for t in self.tracks if t.id == owned.id), None)

    def disown(self, role: str) -> None:
        self._owned.pop(role, None)

    # -- clip slots ---------------------------------------------------------------
    def _clip_slots(self, track_index: int) -> list[dict]:
        return self.client.send("get_track_info", {"track_index": track_index}).get("clip_slots", [])

    def first_empty_slot(self, track_index: int) -> int:
        return self._first_empty(self._clip_slots(track_index), track_index)

    @staticmethod
    def _first_empty(slots: list[dict], track_index: int) -> int:
        for slot in slots:
            if not slot.get("has_clip"):
                return int(slot["index"])
        raise SessionError(f"track {track_index} has no empty clip slot (Live Lite has 8 scenes); clear one in Live")

    @staticmethod
    def _slot_holds(slots: list[dict], ref: ClipRef) -> bool:
        entry = next((s for s in slots if int(s.get("index", -1)) == ref.slot), None)
        return bool(entry and entry.get("has_clip") and entry.get("name") == ref.name)

    def locate_slot(self, role: str, track_index: int) -> tuple[int, bool]:
        """(slot, True) when abl's remembered clip is still there; otherwise (first empty slot, False)."""
        slots = self._clip_slots(track_index)
        ref = self._clips.get(role)
        if ref is not None:
            if self._slot_holds(slots, ref):
                return ref.slot, True
            self.forget_clip(role)
        return self._first_empty(slots, track_index), False

    def verify_clip(self, role: str) -> bool:
        """True when the clip abl wrote for the role is still in its slot; forgets it otherwise."""
        clip = self.clip_for(role)
        if clip is None:
            return False
        if self._slot_holds(self._clip_slots(clip[0]), self._clips[role]):
            return True
        self.forget_clip(role)
        return False

    # -- clips abl wrote -------------------------------------------------------------
    def remember_clip(self, role: str, slot: int, name: str, description: str = "") -> None:
        self._clips[role] = ClipRef(slot, name, description or name)

    def forget_clip(self, role: str) -> None:
        self._clips.pop(role, None)

    def clip_for(self, role: str) -> tuple[int, int] | None:
        ref = self._clips.get(role)
        if ref is None:
            return None
        track = self.find_track(role)
        if track is None:
            return None
        return track.index, ref.slot

    def clip_description(self, role: str) -> str:
        ref = self._clips.get(role)
        return ref.description if ref else ""

    def remembered_roles(self) -> list[str]:
        return [role for role in ROLE_TRACK_NAMES if role in self._clips]
