"""Tap-to-talk: record from the mic until you stop speaking, transcribe locally with whisper.cpp,
turn the words into a grammar line, run it. Everything stays on the machine."""

from __future__ import annotations

import math
import os
from array import array
import re
import subprocess
import tempfile
import wave
from dataclasses import dataclass, field
from typing import Callable

from abl.catalog import SOUNDS
from abl.commands import VERBS, is_known_verb
from abl.theory import ChordError, parse_chord

MODEL_PATH = os.environ.get("ABL_WHISPER_MODEL", os.path.expanduser("~/.abl/models/ggml-base.en.bin"))
MIC_DEVICE = os.environ.get("ABL_MIC", ":0")  # avfoundation "video:audio"; ":0" = first audio device
SAMPLE_RATE = 16000
SAMPLE_WIDTH = 2
CHUNK_SECONDS = 0.1
CHUNK_BYTES = int(SAMPLE_RATE * SAMPLE_WIDTH * CHUNK_SECONDS)
RMS_THRESHOLD = int(os.environ.get("ABL_VOICE_THRESHOLD", "400"))
SILENCE_CHUNKS = 10  # 1.0 s of quiet after speech ends the take
MAX_CHUNKS = 100  # 10 s hard stop
MIN_SPEECH_CHUNKS = 2
WHISPER_TIMEOUT = 60


class VoiceError(Exception):
    pass


# -- recording -------------------------------------------------------------------------

def should_stop(history: list[int], threshold: int = RMS_THRESHOLD, silence_chunks: int = SILENCE_CHUNKS, max_chunks: int = MAX_CHUNKS) -> bool:
    if len(history) >= max_chunks:
        return True
    spoke = sum(1 for level in history if level > threshold) >= MIN_SPEECH_CHUNKS
    if not spoke or len(history) < silence_chunks:
        return False
    return all(level <= threshold for level in history[-silence_chunks:])


def rms(chunk: bytes) -> int:
    """Root-mean-square level of little-endian 16-bit mono samples."""
    samples = array("h")
    samples.frombytes(chunk[: len(chunk) - len(chunk) % SAMPLE_WIDTH])
    if not samples:
        return 0
    return int(math.sqrt(sum(x * x for x in samples) / len(samples)))


def record_until_silence(device: str = MIC_DEVICE) -> str:
    args = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "avfoundation", "-i", device,
            "-ac", "1", "-ar", str(SAMPLE_RATE), "-f", "s16le", "-"]
    try:
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        raise VoiceError("ffmpeg is not installed (brew install ffmpeg)") from None
    chunks: list[bytes] = []
    history: list[int] = []
    try:
        while not should_stop(history):
            chunk = proc.stdout.read(CHUNK_BYTES)
            if not chunk:
                err = proc.stderr.read().decode(errors="replace").strip()
                raise VoiceError(
                    "no audio from the microphone. Allow microphone access for your terminal in "
                    "System Settings > Privacy & Security > Microphone" + (f" ({err})" if err else "")
                )
            chunks.append(chunk)
            history.append(rms(chunk))
    finally:
        proc.kill()
        proc.wait()
    handle, path = tempfile.mkstemp(prefix="abl-voice-", suffix=".wav")
    os.close(handle)
    with wave.open(path, "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(SAMPLE_WIDTH)
        out.setframerate(SAMPLE_RATE)
        out.writeframes(b"".join(chunks))
    return path


# -- transcription ---------------------------------------------------------------------

def _run_whisper(args: list[str]) -> str:
    result = subprocess.run(args, capture_output=True, text=True, timeout=WHISPER_TIMEOUT)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"whisper-cli exit {result.returncode}")
    return result.stdout


def transcribe(path: str, model: str = MODEL_PATH, runner: Callable[[list[str]], str] | None = None) -> str:
    args = ["whisper-cli", "-m", model, "-f", path, "-l", "en", "-nt", "-np"]
    try:
        output = (runner or _run_whisper)(args)
    except Exception:
        return ""
    text = NON_SPEECH.sub(" ", output)
    return " ".join(text.split())


NON_SPEECH = re.compile(r"\([^)]*\)|\[[^\]]*\]")  # Whisper's (sighs), [Music], [BLANK_AUDIO]


# -- words to grammar -----------------------------------------------------------------

ONES = {"zero": 0, "oh": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
        "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
        "eighteen": 18, "nineteen": 19}
TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}
NUMBER_WORDS = set(ONES) | set(TENS) | {"hundred", "and", "a"}
NOTE_LETTERS = set("abcdefg")
ACCIDENTALS = {"sharp": "#", "flat": "b"}
QUALITY_WORDS = {"minor": "m", "major": "maj", "seven": "7", "seventh": "7", "nine": "9", "ninth": "9", "six": "6", "sixth": "6",
                 "sus": "sus", "two": "2", "four": "4", "dim": "dim", "diminished": "dim", "aug": "aug", "augmented": "aug", "add": "add"}
FILLERS = {"the", "please", "that", "now", "it", "some", "on", "up"}
VERB_SYNONYMS = {
    "play": "go", "start": "go", "pause": "stop",
    "hihats": "hats", "hihat": "hats", "hat": "hats",
    "base": "bass", "beats": "beat", "drum": "drums", "key": "keys", "chords": "keys",
    "lauter": "louder", "loader": "louder", "quiet": "quieter", "softer": "quieter", "lower": "quieter",
}
SPOKEN_FIX = [(re.compile(r"\bhi[- ]?hats?\b"), "hats"), (re.compile(r"[.,!?;:]"), " "), (re.compile(r"(?<=\w)-(?=\w)"), " ")]


def spoken_number(tokens: list[str]) -> int | None:
    if not tokens or not all(t.isdigit() or t in NUMBER_WORDS for t in tokens):
        return None
    if len(tokens) == 1 and tokens[0].isdigit():
        return int(tokens[0])
    if all(t.isdigit() or (t in ONES and ONES[t] < 10) for t in tokens) and len(tokens) > 1:
        return int("".join(t if t.isdigit() else str(ONES[t]) for t in tokens))  # "eight oh eight"
    total = 0
    previous_ones: int | None = None
    for tok in tokens:
        if tok in ("and",):
            continue
        if tok == "a":
            previous_ones = 1
            continue
        if tok.isdigit():
            total += int(tok)
            previous_ones = None
        elif tok in ONES:
            total += ONES[tok]
            previous_ones = ONES[tok] if 1 <= ONES[tok] <= 9 else None
        elif tok in TENS:
            if previous_ones is not None:  # "one forty" -> 140
                total += previous_ones * 100 - previous_ones
            total += TENS[tok]
            previous_ones = None
        elif tok == "hundred":
            total = (previous_ones or total or 1) * 100 if previous_ones else (total or 1) * 100
            previous_ones = None
    return total if total else None


def _numbers_to_digits(tokens: list[str]) -> list[str]:
    """Replace every maximal run of number words with its digits."""
    out: list[str] = []
    i = 0
    while i < len(tokens):
        if tokens[i] in NUMBER_WORDS and tokens[i] not in ("a", "and"):
            j = i
            while j < len(tokens) and tokens[j] in NUMBER_WORDS:
                j += 1
            while j > i and tokens[j - 1] in ("a", "and"):
                j -= 1
            value = spoken_number(tokens[i:j])
            out.append(str(value) if value is not None else " ".join(tokens[i:j]))
            i = j
        else:
            out.append(tokens[i])
            i += 1
    return out


def _chords_from_words(tokens: list[str]) -> list[str]:
    chords: list[str] = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        try:
            parse_chord(tok)
            if len(tok) > 1:  # already a chord symbol such as am7 or F#m
                chords.append(tok[0].upper() + tok[1:])
                i += 1
                continue
        except ChordError:
            pass
        if tok in NOTE_LETTERS:
            symbol = tok.upper()
            i += 1
            if i < len(tokens) and tokens[i] in ACCIDENTALS:
                symbol += ACCIDENTALS[tokens[i]]
                i += 1
            quality = ""
            while i < len(tokens) and (tokens[i] in QUALITY_WORDS or tokens[i].isdigit()):
                word = tokens[i]
                piece = QUALITY_WORDS.get(word, word)
                if piece == "maj" and not (i + 1 < len(tokens) and (tokens[i + 1] in ("seven", "seventh", "nine", "ninth", "7", "9"))):
                    piece = ""  # plain major triad
                quality += piece
                i += 1
            chords.append(symbol + quality)
        else:
            i += 1
    return chords


def normalize_spoken(text: str) -> str:
    cleaned = text.lower()
    for pattern, replacement in SPOKEN_FIX:
        cleaned = pattern.sub(replacement, cleaned)
    tokens = cleaned.split()
    if not tokens:
        return ""
    verb = VERB_SYNONYMS.get(tokens[0], tokens[0])
    if verb not in VERBS:
        return " ".join(tokens)
    rest = [t for t in tokens[1:] if t not in FILLERS]
    if verb in ("go", "stop", "undo", "redo", "status", "tracks", "help"):
        return verb
    if verb == "keys":
        sound = None
        if rest and rest[0] in SOUNDS["keys"]:
            sound = rest.pop(0)
        mode = rest.pop() if rest and rest[-1] in ("stab", "hold") else None
        chords = _chords_from_words(rest)
        parts = [verb] + ([sound] if sound else []) + (["-".join(chords)] if chords else []) + ([mode] if mode else [])
        return " ".join(parts)
    return " ".join([verb] + _numbers_to_digits(rest))


# -- the flow ----------------------------------------------------------------------------

def notify(title: str, text: str) -> None:
    safe = lambda s: s.replace("\\", "\\\\").replace('"', '\\"')
    try:
        subprocess.run(["osascript", "-e", f'display notification "{safe(text)}" with title "{safe(title)}"'], capture_output=True, timeout=5)
    except Exception:
        pass


@dataclass
class Listener:
    record: Callable[[], str] = field(default=record_until_silence)
    transcribe: Callable[[str], str] = field(default=transcribe)
    notify: Callable[[str, str], None] = field(default=notify)

    def listen_once(self, session, out: Callable[[str], None], use_llm: bool) -> int:
        from abl.cli import run_line  # late import: cli imports this module

        try:
            path = self.record()
        except VoiceError as exc:
            out(f"!! {exc}")
            self.notify("abl", str(exc))
            return 1
        heard = self.transcribe(path).strip()
        if not heard:
            out("?? heard nothing")
            self.notify("abl", "Heard nothing")
            return 2
        line = normalize_spoken(heard)
        out(f'heard: "{heard}" -> {line}')
        if not use_llm and not is_known_verb(line):
            out(f'?? not a command: "{heard}" (say something like: beat trap 140)')
            self.notify("abl", f"Not a command: {heard}")
            return 2
        collected: list[str] = []
        code = run_line(line, session, use_llm, collected.append)
        for item in collected:
            out(item)
        self.notify("abl", f"{line}: {collected[-1] if collected else 'ok'}")
        return code
