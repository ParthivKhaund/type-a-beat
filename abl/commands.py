"""The abl grammar: one line in, one Command out. No Live access."""

from __future__ import annotations

from dataclasses import dataclass, field

from abl.catalog import ROLE_TRACK_NAMES, SOUNDS
from abl.patterns import DRUM_STYLES, HAT_MODES, normalize_style
from abl.theory import ChordError, parse_progression

MIN_TEMPO, MAX_TEMPO = 20.0, 300.0
MAX_SWING = 75
MAX_STEPS = 20
KEYS_MODES = ("stab", "hold")
ROLES = tuple(ROLE_TRACK_NAMES)

HELP = """\
beat <style> [bpm]      styles: trap boombap hiphop house techno pop lofi jazz swing
drums <style>           same as beat, never changes tempo
bass [sound] [style]    sounds: 808 sub pure upright synth analog reese 303 saw fm electric
keys [sound] <chords> [stab|hold]   sounds: rhodes epiano wurli piano organ pad
                        chords: Cmaj7-Am7-Dm7-G7  or  Am F C G  (one chord per bar, minor = m)
tempo <bpm>
go | play               fire every abl clip and start the transport
stop                    stop the transport
mute|unmute|solo|unsolo <drums|bass|keys|lead|track name|index>
louder|quieter <role> [steps]        one step = 0.05 on the fader
swing <50-75>           MPC-style 16th swing on the drum clip (50 = straight)
hats double|half|normal|off
clear <role>            delete the abl clip for that role
kill <role>             delete the role track (only if abl created it)
undo | redo | status | tracks | help
catalog                 rescan Live's browser (after installing packs or plugins)
import <url or file>    download a song and put it on an audio track
recreate <url or file> [fresh]   analyze a song and lay it into Live, one scene per section
analyze <url or file> [fresh]    the analysis alone: tempo, key, sections, chords
Chain with ';'   e.g.  beat trap 140; bass 808; keys rhodes Am-F-C-G; go"""


class ParseError(ValueError):
    """The line does not match the grammar."""


@dataclass(frozen=True)
class Command:
    name: str
    args: dict = field(default_factory=dict)


def split_chain(text: str) -> list[str]:
    return [part.strip() for part in text.split(";") if part.strip()]


def _style(token: str) -> str:
    try:
        return normalize_style(token)
    except KeyError:
        raise ParseError(f"unknown style {token!r}; styles: {', '.join(sorted(DRUM_STYLES))}") from None


def _is_style(token: str) -> bool:
    try:
        normalize_style(token)
        return True
    except KeyError:
        return False


def _number(token: str, low: float, high: float, what: str) -> float:
    try:
        value = float(token)
    except ValueError:
        raise ParseError(f"{what} must be a number, got {token!r}") from None
    if not low <= value <= high:
        raise ParseError(f"{what} must be between {low:g} and {high:g}, got {value:g}")
    return value


def _beat(rest: list[str]) -> Command:
    if not rest:
        raise ParseError("beat needs a style: " + ", ".join(sorted(DRUM_STYLES)))
    bpm = _number(rest[1], MIN_TEMPO, MAX_TEMPO, "tempo") if len(rest) > 1 else None
    return Command("beat", {"style": _style(rest[0]), "bpm": bpm})


def _drums(rest: list[str]) -> Command:
    if not rest:
        raise ParseError("drums needs a style: " + ", ".join(sorted(DRUM_STYLES)))
    return Command("drums", {"style": _style(rest[0])})


def _bass(rest: list[str]) -> Command:
    sound_alias = None
    style = None
    for token in rest[:2]:
        lowered = token.lower()
        if _is_style(lowered):
            style = normalize_style(lowered)
        elif lowered in SOUNDS["bass"]:
            sound_alias = lowered
        else:
            raise ParseError(f"bass: {token!r} is neither a sound ({', '.join(SOUNDS['bass'])}) nor a style")
    return Command("bass", {"sound": sound_alias, "style": style})


def _keys(rest: list[str]) -> Command:
    tokens = list(rest)
    sound_alias = None
    mode = None
    if tokens and tokens[0].lower() in SOUNDS["keys"]:
        sound_alias = tokens.pop(0).lower()
    if tokens and tokens[-1].lower() in KEYS_MODES:
        mode = tokens.pop().lower()
    if not tokens:
        raise ParseError("keys needs a chord progression, e.g. keys rhodes Cmaj7-Am7-Dm7-G7")
    progression = "-".join(tokens)
    try:
        parse_progression(progression)
    except ChordError as exc:
        raise ParseError(f"keys: {exc}") from None
    return Command("keys", {"sound": sound_alias, "progression": progression, "mode": mode})


def _tempo(rest: list[str]) -> Command:
    if not rest:
        raise ParseError("tempo needs a number, e.g. tempo 128")
    return Command("tempo", {"bpm": _number(rest[0], MIN_TEMPO, MAX_TEMPO, "tempo")})


def _target(verb: str):
    def build(rest: list[str]) -> Command:
        if not rest:
            raise ParseError(f"{verb} needs a target: drums, bass, keys, lead, a track name, or an index")
        return Command(verb, {"target": " ".join(rest).lower()})

    return build


def _level(verb: str):
    def build(rest: list[str]) -> Command:
        if not rest:
            raise ParseError(f"{verb} needs a target, e.g. {verb} bass")
        steps = 1
        if len(rest) > 1 and rest[-1].isdigit():
            steps = int(_number(rest[-1], 1, MAX_STEPS, "steps"))
            rest = rest[:-1]
        return Command(verb, {"target": " ".join(rest).lower(), "steps": steps})

    return build


def _swing(rest: list[str]) -> Command:
    if not rest:
        raise ParseError(f"swing needs a percentage 50-{MAX_SWING}")
    return Command("swing", {"pct": int(_number(rest[0], 0, MAX_SWING, "swing"))})


def _hats(rest: list[str]) -> Command:
    if not rest or rest[0].lower() not in HAT_MODES:
        raise ParseError("hats needs one of: " + ", ".join(HAT_MODES))
    return Command("hats", {"mode": rest[0].lower()})


def _role(verb: str):
    def build(rest: list[str]) -> Command:
        if not rest or rest[0].lower() not in ROLES:
            raise ParseError(f"{verb} needs a role: " + ", ".join(ROLES))
        return Command(verb, {"role": rest[0].lower()})

    return build


def _source(verb: str):
    def build(rest: list[str]) -> Command:
        tokens = list(rest)
        fresh = bool(tokens) and tokens[-1].lower() == "fresh"
        if fresh:
            tokens.pop()
        source = " ".join(tokens)
        if not source:
            raise ParseError(f"{verb} needs a YouTube URL or an audio file, e.g. {verb} https://youtu.be/...")
        return Command(verb, {"source": source, "fresh": fresh})

    return build


def _import(rest: list[str]) -> Command:
    source = " ".join(rest)
    if not source:
        raise ParseError("import needs a YouTube URL or an audio file, e.g. import https://youtu.be/...")
    return Command("import", {"source": source})


def _bare(name: str):
    def build(rest: list[str]) -> Command:
        if rest:
            raise ParseError(f"{name} takes no arguments (got {' '.join(rest)!r})")
        return Command(name, {})

    return build


VERBS = {
    "beat": _beat,
    "drums": _drums,
    "bass": _bass,
    "keys": _keys,
    "tempo": _tempo,
    "go": _bare("go"),
    "play": _bare("go"),
    "stop": _bare("stop"),
    "mute": _target("mute"),
    "unmute": _target("unmute"),
    "solo": _target("solo"),
    "unsolo": _target("unsolo"),
    "louder": _level("louder"),
    "quieter": _level("quieter"),
    "swing": _swing,
    "hats": _hats,
    "clear": _role("clear"),
    "kill": _role("kill"),
    "undo": _bare("undo"),
    "redo": _bare("redo"),
    "status": _bare("status"),
    "tracks": _bare("tracks"),
    "help": _bare("help"),
    "catalog": _bare("catalog"),
    "import": _import,
    "recreate": _source("recreate"),
    "analyze": _source("analyze"),
}


def is_known_verb(line: str) -> bool:
    tokens = line.split()
    return bool(tokens) and tokens[0].lower() in VERBS


def parse(line: str) -> Command:
    tokens = line.split()
    if not tokens:
        raise ParseError("empty line; try: help")
    verb = tokens[0].lower()
    handler = VERBS.get(verb)
    if handler is None:
        raise ParseError(f"unknown command {tokens[0]!r}\n{HELP}")
    return handler(tokens[1:])
