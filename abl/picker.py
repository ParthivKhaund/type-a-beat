"""Turn what the analyzer heard into sounds from the library: the matched kit for drums, and
keyword searches driven by the CLAP tags for bass, keys, and lead."""

from __future__ import annotations

import re

from abl import catalog, library
from abl.catalog import Sound

# CLAP label -> (preferred catalog categories, name keywords in priority order)
TAG_KEYWORDS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "a deep 808 sub bass": (("Bass",), ("Sub 808", "808", "Sub")),
    "an electric bass guitar": (("Bass",), ("Electric Bass", "Fingered", "Picked", "Studio Bass")),
    "an upright acoustic bass": (("Bass",), ("Upright", "Double Bass", "Acoustic Bass")),
    "a synthesizer bass": (("Bass",), ("Analog Bass", "Saw Bass", "Basic Analog", "Synth Bass", "Moog")),
    "an acid 303 bass": (("Bass",), ("303", "Acid")),
    "an electric piano": (("Piano & Keys", "Synth Keys"), ("E-Piano Rhodish", "E-Piano", "Rhodes", "Wurli")),
    "a grand piano": (("Piano & Keys",), ("Grand Piano", "Upright Piano", "Piano")),
    "a hammond organ": (("Piano & Keys",), ("Organ",)),
    "a warm synth pad": (("Pad",), ("Warm", "Analog Pad", "Pad")),
    "a plucked synth": (("Guitar & Plucked", "Synth Keys"), ("Pluck",)),
    "a string ensemble": (("Strings",), ("Strings Orch", "Strings", "String")),
    "a brass section": (("Brass",), ("Brass", "Horns", "Trumpet")),
    "a choir": (("Pad", "Ambient & Evolving"), ("Choir", "Voice", "Vocal")),
    "bells and mallets": (("Mallets",), ("Bells", "Vibraphone", "Marimba", "Glock")),
    "a synth lead": (("Synth Lead",), ("Lead",)),
    "an acoustic guitar": (("Guitar & Plucked",), ("Guitar Acoustic", "Nylon", "Acoustic")),
    "a clean electric guitar": (("Guitar & Plucked",), ("Guitar Electric Clean", "Guitar Electric", "Guitar")),
    "a singing voice": (("Pad", "Ambient & Evolving", "Synth Lead"), ("Choir", "Vocal", "Voice", "Sweet Lead")),
    "a flute": (("Winds",), ("Flute",)),
    "a violin": (("Strings",), ("Violin", "Strings")),
    "a trumpet": (("Brass",), ("Trumpet", "Horns", "Brass")),
    "an electric guitar solo": (("Guitar & Plucked", "Synth Lead"), ("Guitar Electric", "Lead")),
}

ROLE_SECTIONS = {"bass": ("Sounds", "Packs", "User Library"), "keys": ("Sounds", "Packs", "User Library"), "lead": ("Sounds", "Packs", "User Library")}
KEYS_SOURCE_TAGS = {"piano": "a grand piano", "guitar": "a clean electric guitar"}
MIN_TAG_MARGIN = 0.0


def _matches(entry: dict, keyword: str, categories: tuple[str, ...]) -> bool:
    name = entry.get("name", "")
    in_category = not categories or any(c.lower() in entry.get("category", "").lower() for c in categories) or entry.get("section") in ("Packs", "User Library")
    return in_category and re.search(re.escape(keyword), name, re.I) is not None


def search(entries: list[dict], keywords: tuple[str, ...], categories: tuple[str, ...], sections: tuple[str, ...]) -> Sound | None:
    """First entry whose name contains the highest-priority keyword, preferring the given categories."""
    pool = [e for e in entries if e.get("section") in sections and e.get("uri", "").startswith("query:")]
    for keyword in keywords:
        strict = [e for e in pool if _matches(e, keyword, categories)]
        loose = strict or [e for e in pool if re.search(re.escape(keyword), e.get("name", ""), re.I)]
        if loose:
            best = loose[0]
            return Sound(re.sub(r"\.(adg|adv)$", "", best["name"]), best["uri"])
    return None


def sound_for_tag(entries: list[dict], role: str, tags: list) -> Sound | None:
    for label, _score in tags[:3]:
        spec = TAG_KEYWORDS.get(label)
        if spec is None:
            continue
        found = search(entries, spec[1], spec[0], ROLE_SECTIONS.get(role, ("Sounds",)))
        if found:
            return found
    return None


def kit_sound(entries: list[dict], kit_name: str) -> Sound | None:
    wanted = kit_name.lower()
    for entry in entries:
        if entry.get("section") in ("Drums", "Packs") and re.sub(r"\.adg$", "", entry.get("name", "")).lower() == wanted:
            return Sound(kit_name, entry["uri"])
    return None


def pick_sounds(analysis: dict, entries: list[dict] | None = None, fallback: dict[str, Sound] | None = None) -> tuple[dict[str, Sound], dict[str, str]]:
    """(sounds by role, one-line reason per role). Falls back per role to the tempo-based defaults."""
    entries = library.load() if entries is None else entries
    sounds = dict(fallback or {})
    reasons: dict[str, str] = {}
    kit = analysis.get("kit") or {}
    if kit.get("name"):
        found = kit_sound(entries, kit["name"])
        if found:
            sounds["drums"] = found
            reasons["drums"] = f"closest kit to the song's own hits ({kit.get('score', 0):.2f})"
    tags = analysis.get("instrument_tags") or {}
    for role in ("bass", "keys", "lead"):
        role_tags = list(tags.get(role) or [])
        if role == "keys" and analysis.get("keys_source") in KEYS_SOURCE_TAGS:
            role_tags = [(KEYS_SOURCE_TAGS[analysis["keys_source"]], 1.0)] + role_tags
        found = sound_for_tag(entries, role, role_tags)
        if found:
            sounds[role] = found
            reasons[role] = f"heard {role_tags[0][0]}" if role_tags else "tag"
    return sounds, reasons
