import pytest

from abl.cli import main
from abl.wire import LiveNotRunning


def run_cli(live, argv, monkeypatch, **kwargs):
    monkeypatch.setenv("ABL_NO_LLM", "1")
    lines = []
    code = main(argv, client_factory=lambda host, port: live, out=lines.append, **kwargs)
    return code, lines


def test_one_shot_runs_one_line_per_command_with_timing(studio_live, monkeypatch):
    code, lines = run_cli(studio_live, ["tempo 128; stop"], monkeypatch)
    assert code == 0
    assert len(lines) == 2
    assert "128" in lines[0] and "ms" in lines[0]
    assert studio_live.tempo == 128.0


def test_one_shot_joins_separate_argv_words(studio_live, monkeypatch):
    code, lines = run_cli(studio_live, ["tempo", "100"], monkeypatch)
    assert code == 0 and studio_live.tempo == 100.0


def test_parse_error_exits_2_with_the_hint(studio_live, monkeypatch):
    code, lines = run_cli(studio_live, ["beat dubstep"], monkeypatch)
    assert code == 2
    assert "trap" in lines[0]
    assert studio_live.calls == []


def test_action_error_exits_1(studio_live, monkeypatch):
    code, lines = run_cli(studio_live, ["mute vocals"], monkeypatch)
    assert code == 1
    assert "vocals" in lines[0]


def test_live_not_running_exits_1_with_message(monkeypatch):
    class Dead:
        def send(self, *a, **k):
            raise LiveNotRunning("Live is not running")

        def batch(self, *a, **k):
            raise LiveNotRunning("Live is not running")

    code, lines = run_cli(Dead(), ["status"], monkeypatch)
    assert code == 1
    assert "not running" in lines[0]


def test_chain_stops_at_the_first_failure(studio_live, monkeypatch):
    code, lines = run_cli(studio_live, ["mute vocals; tempo 90"], monkeypatch)
    assert code == 1
    assert studio_live.tempo == 122.0


def test_repl_runs_until_quit(studio_live, monkeypatch):
    prompts = iter(["tempo 99", "quit"])
    code, lines = run_cli(studio_live, [], monkeypatch, input_fn=lambda prompt: next(prompts))
    assert code == 0
    assert studio_live.tempo == 99.0
    assert any("99" in line for line in lines)


def test_repl_exits_cleanly_on_eof(studio_live, monkeypatch):
    def input_fn(prompt):
        raise EOFError

    code, _ = run_cli(studio_live, [], monkeypatch, input_fn=input_fn)
    assert code == 0


def test_repl_keeps_going_after_a_bad_line(studio_live, monkeypatch):
    prompts = iter(["beat dubstep", "tempo 77", "exit"])
    code, lines = run_cli(studio_live, [], monkeypatch, input_fn=lambda prompt: next(prompts))
    assert code == 0 and studio_live.tempo == 77.0


def test_no_llm_flag_skips_translation(studio_live, monkeypatch):
    monkeypatch.delenv("ABL_NO_LLM", raising=False)
    called = []
    monkeypatch.setattr("abl.cli.translate", lambda line: called.append(line) or None)
    lines = []
    main(["--no-llm", "make it jazzier"], client_factory=lambda host, port: studio_live, out=lines.append)
    assert called == []


def test_translation_is_shown_then_executed(studio_live, monkeypatch):
    monkeypatch.delenv("ABL_NO_LLM", raising=False)
    monkeypatch.setattr("abl.cli.translate", lambda line: "tempo 111")
    lines = []
    code = main(["make it a bit faster"], client_factory=lambda host, port: studio_live, out=lines.append)
    assert code == 0
    assert any("tempo 111" in line for line in lines)
    assert studio_live.tempo == 111.0


def test_a_known_verb_with_bad_arguments_never_calls_the_model(studio_live, monkeypatch):
    monkeypatch.delenv("ABL_NO_LLM", raising=False)
    called = []
    monkeypatch.setattr("abl.cli.translate", lambda line: called.append(line) or "tempo 100")
    lines = []
    code = main(["tempo 500"], client_factory=lambda host, port: studio_live, out=lines.append)
    assert code == 2 and called == []
    assert studio_live.tempo == 122.0


def test_listen_flag_runs_one_voice_command(studio_live, monkeypatch):
    monkeypatch.setenv("ABL_NO_LLM", "1")

    class FakeListener:
        def listen_once(self, session, out, use_llm):
            out("heard: stop")
            return 0

    lines = []
    code = main(["--listen"], client_factory=lambda host, port: studio_live, out=lines.append, listener=FakeListener())
    assert code == 0 and lines == ["heard: stop"]


def test_repl_voice_word_listens_once(studio_live, monkeypatch):
    monkeypatch.setenv("ABL_NO_LLM", "1")
    heard = []

    class FakeListener:
        def listen_once(self, session, out, use_llm):
            heard.append(True)
            return 0

    prompts = iter(["v", "voice", "quit"])
    main([], client_factory=lambda host, port: studio_live, out=lambda s: None, input_fn=lambda p: next(prompts), listener=FakeListener())
    assert len(heard) == 2
