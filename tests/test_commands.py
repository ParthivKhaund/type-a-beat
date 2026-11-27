import pytest

from abl.commands import HELP, Command, ParseError, is_known_verb, parse, split_chain


def test_beat_with_style_and_bpm():
    assert parse("beat trap 140") == Command("beat", {"style": "trap", "bpm": 140.0})


def test_beat_without_bpm():
    assert parse("beat house") == Command("beat", {"style": "house", "bpm": None})


def test_beat_normalizes_style_aliases():
    assert parse("beat swing").args["style"] == "jazz"
    assert parse("beat hiphop").args["style"] == "boombap"


def test_beat_unknown_style_is_a_parse_error_listing_styles():
    with pytest.raises(ParseError) as exc:
        parse("beat dubstep")
    assert "trap" in str(exc.value)


def test_drums_is_beat_without_tempo():
    assert parse("drums lofi") == Command("drums", {"style": "lofi"})


def test_bare_bass():
    assert parse("bass") == Command("bass", {"sound": None, "style": None})


def test_bass_with_sound():
    assert parse("bass 808").args == {"sound": "808", "style": None}


def test_bass_with_sound_and_style():
    assert parse("bass upright jazz").args == {"sound": "upright", "style": "jazz"}


def test_bass_with_style_only():
    assert parse("bass jazz").args == {"sound": None, "style": "jazz"}


def test_keys_with_sound_and_dashed_progression():
    cmd = parse("keys rhodes Cmaj7-Am7-Dm7-G7")
    assert cmd == Command("keys", {"sound": "rhodes", "progression": "Cmaj7-Am7-Dm7-G7", "mode": None})


def test_keys_with_spaced_progression_and_mode():
    cmd = parse("keys Am F C G stab")
    assert cmd.args == {"sound": None, "progression": "Am-F-C-G", "mode": "stab"}


def test_keys_preserves_chord_case():
    assert parse("keys piano Am7").args["progression"] == "Am7"


def test_keys_requires_a_progression():
    with pytest.raises(ParseError):
        parse("keys")
    with pytest.raises(ParseError):
        parse("keys rhodes")


def test_tempo():
    assert parse("tempo 128") == Command("tempo", {"bpm": 128.0})


@pytest.mark.parametrize("bad", ["tempo", "tempo fast", "tempo 500", "tempo 5"])
def test_tempo_rejects_bad_values(bad):
    with pytest.raises(ParseError):
        parse(bad)


@pytest.mark.parametrize("line, name", [("go", "go"), ("play", "go"), ("stop", "stop"), ("undo", "undo"), ("redo", "redo"), ("status", "status"), ("tracks", "tracks"), ("help", "help")])
def test_bare_verbs(line, name):
    assert parse(line) == Command(name, {})


@pytest.mark.parametrize("verb", ["mute", "unmute", "solo", "unsolo"])
def test_mixer_verbs_take_a_target(verb):
    assert parse(f"{verb} drums") == Command(verb, {"target": "drums"})
    assert parse(f"{verb} 3") == Command(verb, {"target": "3"})
    with pytest.raises(ParseError):
        parse(verb)


def test_louder_defaults_to_one_step():
    assert parse("louder bass") == Command("louder", {"target": "bass", "steps": 1})


def test_quieter_with_steps():
    assert parse("quieter drums 2") == Command("quieter", {"target": "drums", "steps": 2})


def test_swing_percent():
    assert parse("swing 60") == Command("swing", {"pct": 60})


@pytest.mark.parametrize("bad", ["swing", "swing 120", "swing 80", "swing lots"])
def test_swing_rejects_bad_values(bad):
    with pytest.raises(ParseError):
        parse(bad)


@pytest.mark.parametrize("mode", ["double", "half", "normal", "off"])
def test_hats_modes(mode):
    assert parse(f"hats {mode}") == Command("hats", {"mode": mode})


def test_hats_rejects_unknown_mode():
    with pytest.raises(ParseError):
        parse("hats up")


def test_clear_and_kill_take_a_role():
    assert parse("clear keys") == Command("clear", {"role": "keys"})
    assert parse("kill lead") == Command("kill", {"role": "lead"})
    with pytest.raises(ParseError):
        parse("clear vocals")


def test_verbs_are_case_insensitive():
    assert parse("BEAT TRAP").args["style"] == "trap"


@pytest.mark.parametrize("junk", ["", "   ", "make it jazzier", "beat"])
def test_junk_is_a_parse_error(junk):
    with pytest.raises(ParseError):
        parse(junk)


def test_split_chain_on_semicolons():
    assert split_chain("beat trap 140; bass 808 ;go") == ["beat trap 140", "bass 808", "go"]


def test_split_chain_drops_empty_segments():
    assert split_chain("go;;") == ["go"]


def test_help_mentions_every_verb():
    for verb in ["beat", "bass", "keys", "tempo", "go", "stop", "mute", "louder", "swing", "hats", "undo"]:
        assert verb in HELP


def test_swing_accepts_the_mpc_range_up_to_75():
    assert parse("swing 75").args["pct"] == 75


@pytest.mark.parametrize("line", ["undo isn't what you want", "play it cool", "go now", "stop the music"])
def test_bare_verbs_reject_trailing_words(line):
    with pytest.raises(ParseError):
        parse(line)


def test_mixer_target_can_be_several_words():
    assert parse("mute piano stab").args["target"] == "piano stab"


def test_level_target_can_be_several_words_with_trailing_steps():
    assert parse("louder piano stab 2").args == {"target": "piano stab", "steps": 2}
    assert parse("quieter piano stab").args == {"target": "piano stab", "steps": 1}


def test_is_known_verb():
    assert is_known_verb("tempo 500")
    assert is_known_verb("BEAT dubstep")
    assert not is_known_verb("make it jazzier")
    assert not is_known_verb("")


def test_recreate_takes_a_url():
    assert parse("recreate https://youtu.be/abc123") == Command("recreate", {"source": "https://youtu.be/abc123", "fresh": False})


def test_analyze_takes_a_path_and_fresh_flag():
    assert parse("analyze ~/Music/song.mp3 fresh") == Command("analyze", {"source": "~/Music/song.mp3", "fresh": True})


def test_recreate_keeps_spaces_in_a_path():
    assert parse("recreate /Users/me/My Song.wav").args["source"] == "/Users/me/My Song.wav"


@pytest.mark.parametrize("bad", ["recreate", "analyze", "recreate fresh"])
def test_recreate_needs_a_source(bad):
    with pytest.raises(ParseError):
        parse(bad)


def test_catalog_is_a_bare_verb():
    assert parse("catalog") == Command("catalog", {})


def test_import_takes_a_url_or_a_path_with_spaces():
    assert parse("import https://youtu.be/abc") == Command("import", {"source": "https://youtu.be/abc"})
    assert parse("import /Users/me/My Song.mp3").args["source"] == "/Users/me/My Song.mp3"


def test_import_needs_a_source():
    with pytest.raises(ParseError):
        parse("import")
