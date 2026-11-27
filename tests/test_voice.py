import pytest

from abl.voice import (
    Listener,
    rms,
    normalize_spoken,
    should_stop,
    spoken_number,
    transcribe,
)


# -- spoken numbers ---------------------------------------------------------------

@pytest.mark.parametrize(
    "words, value",
    [
        ("140", 140), ("one forty", 140), ("one twenty eight", 128), ("ninety", 90), ("sixty two", 62),
        ("eight oh eight", 808), ("three oh three", 303), ("a hundred", 100), ("one hundred and twenty", 120),
        ("seventy", 70), ("two", 2),
    ],
)
def test_spoken_number(words, value):
    assert spoken_number(words.split()) == value


def test_spoken_number_rejects_non_numbers():
    assert spoken_number(["trap"]) is None


# -- normalizing a transcript into a grammar line --------------------------------------

@pytest.mark.parametrize(
    "heard, line",
    [
        ("Beat trap, one forty.", "beat trap 140"),
        ("beat trap 140", "beat trap 140"),
        ("Bass eight oh eight", "bass 808"),
        ("keys rhodes A minor, F, C, G", "keys rhodes Am-F-C-G"),
        ("keys rhodes a minor f c g", "keys rhodes Am-F-C-G"),
        ("Keys piano C major seven, A minor seven, D minor seven, G seven", "keys piano Cmaj7-Am7-Dm7-G7"),
        ("keys B flat, F sharp minor, C", "keys Bb-F#m-C"),
        ("keys organ D minor F C G stab", "keys organ Dm-F-C-G stab"),
        ("tempo one twenty eight", "tempo 128"),
        ("swing sixty", "swing 60"),
        ("hi-hats double", "hats double"),
        ("hi hats off", "hats off"),
        ("Louder drums!", "louder drums"),
        ("quieter keys two", "quieter keys 2"),
        ("Go.", "go"),
        ("Stop", "stop"),
        ("mute the bass", "mute bass"),
        ("undo that", "undo"),
        ("play", "go"),
    ],
)
def test_normalize_spoken(heard, line):
    assert normalize_spoken(heard) == line


@pytest.mark.parametrize(
    "heard, line",
    [
        ("Keys-Rhodes A minor, F, C, G.", "keys rhodes Am-F-C-G"),
        ("base 808", "bass 808"),
        ("Lauter drums", "louder drums"),
        ("Beat Trap 140", "beat trap 140"),
        ("keys piano am f c g", "keys piano Am-F-C-G"),
        ("Beats house", "beat house"),
        ("quiet the keys", "quieter keys"),
        ("drum lofi", "drums lofi"),
    ],
)
def test_normalize_real_whisper_output(heard, line):
    assert normalize_spoken(heard) == line


def test_normalize_leaves_unknown_sentences_for_the_model():
    assert normalize_spoken("Something chill with piano, please") == "something chill with piano please"


# -- stopping on silence ------------------------------------------------------------

def test_should_stop_after_speech_then_a_second_of_silence():
    loud, quiet = 2000, 50
    history = [quiet] * 3 + [loud] * 8 + [quiet] * 10
    assert should_stop(history, threshold=300, silence_chunks=10) is True


def test_should_not_stop_while_still_speaking():
    history = [50] * 3 + [2000] * 8 + [50] * 4
    assert should_stop(history, threshold=300, silence_chunks=10) is False


def test_should_not_stop_before_any_speech():
    assert should_stop([50] * 40, threshold=300, silence_chunks=10) is False


def test_should_stop_at_the_hard_limit_even_in_silence():
    assert should_stop([50] * 100, threshold=300, silence_chunks=10, max_chunks=100) is True


# -- transcribe --------------------------------------------------------------------

def test_transcribe_runs_whisper_and_cleans_the_output():
    seen = {}

    def runner(args):
        seen["args"] = args
        return " [BLANK_AUDIO]\n  Beat trap one forty.\n"

    assert transcribe("/tmp/x.wav", model="/m/base.bin", runner=runner) == "Beat trap one forty."
    assert seen["args"][0] == "whisper-cli"
    assert "/m/base.bin" in seen["args"] and "/tmp/x.wav" in seen["args"]


@pytest.mark.parametrize("noise", [" (sighs)\n", "[Music]\n", " (silence) [BLANK_AUDIO]\n", "\n  \n"])
def test_transcribe_treats_whisper_non_speech_tags_as_nothing(noise):
    assert transcribe("/tmp/x.wav", model="/m/b.bin", runner=lambda args: noise) == ""


def test_transcribe_keeps_words_next_to_a_tag():
    assert transcribe("/tmp/x.wav", model="/m/b.bin", runner=lambda args: "(clears throat) beat house\n") == "beat house"


def test_listener_does_not_run_an_unknown_sentence_without_the_model(studio_live):
    from abl.session import Session

    listener = Listener(record=lambda: "/tmp/f.wav", transcribe=lambda p: "What a lovely day", notify=lambda t, x: None)
    lines = []
    code = listener.listen_once(Session(studio_live), out=lines.append, use_llm=False)
    assert code == 2
    assert studio_live.calls == []
    assert len(lines) == 2 and "not a command" in lines[1]


def test_transcribe_returns_empty_when_whisper_fails():
    def runner(args):
        raise RuntimeError("boom")

    assert transcribe("/tmp/x.wav", model="/m/base.bin", runner=runner) == ""


# -- the listen flow with fakes ------------------------------------------------------------

def test_listener_records_transcribes_normalizes_and_runs(studio_live, monkeypatch):
    monkeypatch.setenv("ABL_NO_LLM", "1")
    from abl.session import Session

    events = []
    listener = Listener(
        record=lambda: "/tmp/fake.wav",
        transcribe=lambda path: "Tempo one twenty eight.",
        notify=lambda title, text: events.append((title, text)),
    )
    session = Session(studio_live)
    lines = []
    code = listener.listen_once(session, out=lines.append, use_llm=False)
    assert code == 0
    assert studio_live.tempo == 128.0
    assert lines[0] == 'heard: "Tempo one twenty eight." -> tempo 128'
    assert events and "128" in events[-1][1]


def test_listener_reports_silence(studio_live):
    from abl.session import Session

    listener = Listener(record=lambda: "/tmp/fake.wav", transcribe=lambda path: "", notify=lambda t, x: None)
    lines = []
    code = listener.listen_once(Session(studio_live), out=lines.append, use_llm=False)
    assert code == 2
    assert "nothing" in lines[0].lower()
    assert studio_live.calls == []


def test_rms_of_silence_is_zero_and_of_a_square_wave_is_its_amplitude():
    from array import array
    assert rms(bytes(400)) == 0
    square = array("h", [3000, -3000] * 100).tobytes()
    assert rms(square) == 3000
