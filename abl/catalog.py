"""Sounds this user's Live Intro/Lite library actually has, by role. URIs verified in the producing-in-ableton skill catalog."""

from __future__ import annotations

from dataclasses import dataclass


class CatalogError(ValueError):
    """Requested a sound, kit, or style the catalog does not have."""


@dataclass(frozen=True)
class Sound:
    name: str
    uri: str


def _bass(name: str, file_id: int) -> Sound:
    return Sound(name, f"query:Sounds#Bass:FileId_{file_id}")


def _keys(name: str, file_id: int) -> Sound:
    return Sound(name, f"query:Sounds#Piano%20&%20Keys:FileId_{file_id}")


def _kit(name: str, file_id: int) -> Sound:
    return Sound(name, f"query:Drums#FileId_{file_id}")


KITS: dict[str, Sound] = {
    "trap": _kit("808 Core Kit", 5409),
    "boombap": _kit("Boom Bap Kit", 5292),
    "house": _kit("909 Core Kit", 5410),
    "techno": _kit("AG Techno Kit", 5354),
    "pop": _kit("Dry Session Kit", 5419),
    "lofi": _kit("LDre Cozy Kit", 5319),
    "jazz": _kit("Dry Session Kit", 5419),
}

SOUNDS: dict[str, dict[str, Sound]] = {
    "bass": {
        "808": _bass("Sub 808 Bass", 6515),
        "sub": _bass("Sub 808 Bass", 6515),
        "pure": _bass("808 Pure", 5164),
        "upright": _bass("Upright Bass", 6516),
        "synth": _bass("Basic Analog Bass", 5170),
        "analog": _bass("Basic Analog Bass", 5170),
        "reese": _bass("Basic Reese Bass", 5178),
        "303": _bass("Basic 303 Bass", 5169),
        "saw": _bass("Basic Saw Bass", 5180),
        "fm": _bass("Basic FM House Bass", 5172),
        "electric": _bass("Electric Bass Soft", 5203),
    },
    "keys": {
        "rhodes": _keys("E-Piano Rhodish", 4849),
        "epiano": _keys("E-Piano Classic", 4841),
        "wurli": _keys("E-Piano Wurli", 4854),
        "piano": _keys("Grand Piano", 4857),
        "grand": _keys("Grand Piano", 4857),
        "organ": _keys("Organ Funky", 4866),
        "pad": Sound("Warm Analog Pad", "query:Sounds#Pad:FileId_4980"),
        "guitar": Sound("Guitar Electric Clean", "query:Sounds#Guitar%20&%20Plucked:FileId_5054"),
    },
    "lead": {
        "saw": Sound("Classic Club Saw", "query:Sounds#Synth%20Lead:FileId_4593"),
        "og": Sound("Basic OG Lead", "query:Sounds#Synth%20Lead:FileId_4581"),
        "glide": Sound("Basic Glide Lead", "query:Sounds#Synth%20Lead:FileId_4580"),
        "sweet": Sound("Sweet Lead", "query:Sounds#Synth%20Lead:FileId_4637"),
        "pluck": Sound("Simple Pluck", "query:Sounds#Guitar%20&%20Plucked:FileId_4811"),
    },
}

DEFAULTS: dict[str, dict[str, str]] = {
    "bass": {"trap": "808", "boombap": "upright", "lofi": "upright", "jazz": "upright", "house": "analog", "techno": "reese", "pop": "electric"},
    "keys": {"trap": "piano", "boombap": "rhodes", "lofi": "rhodes", "jazz": "rhodes", "house": "piano", "techno": "pad", "pop": "piano"},
    "lead": {},
}

GM_PAD_MAP = {"kick": 36, "rim": 37, "snare": 38, "clap": 39, "ch": 42, "perc": 43, "oh": 46, "crash": 49, "ride": 51}

PAD_MAPS: dict[str, dict[str, int]] = {
    "808 Core Kit": {**GM_PAD_MAP, "ride": 49, "crash": 49, "perc": 51},
}

ROLE_TRACK_NAMES = {"drums": "Drums", "bass": "Bass", "keys": "Keys", "lead": "Lead"}


def kit_for_style(style: str) -> Sound:
    try:
        return KITS[style.lower()]
    except KeyError:
        raise CatalogError(f"no kit for style {style!r}; styles: {', '.join(sorted(KITS))}") from None


def sound(role: str, alias: str) -> Sound:
    table = SOUNDS.get(role)
    if table is None:
        raise CatalogError(f"unknown role {role!r}; roles: {', '.join(SOUNDS)}")
    try:
        return table[alias.lower()]
    except KeyError:
        raise CatalogError(f"no {role} sound {alias!r}; options: {', '.join(table)}") from None


def default_sound(role: str, style: str) -> Sound:
    table = SOUNDS[role]
    alias = DEFAULTS.get(role, {}).get(style.lower()) or next(iter(table))
    return table[alias]


def pad_map(kit_name: str) -> dict[str, int]:
    return dict(PAD_MAPS.get(kit_name, GM_PAD_MAP))
