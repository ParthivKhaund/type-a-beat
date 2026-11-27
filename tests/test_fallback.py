import pytest

from abl.fallback import translate


def runner_returning(text):
    calls = []

    def runner(args, prompt):
        calls.append((args, prompt))
        return text

    runner.calls = calls
    return runner


def test_translate_returns_a_clean_grammar_line(monkeypatch):
    monkeypatch.delenv("ABL_NO_LLM", raising=False)
    runner = runner_returning("beat trap 140\n")
    assert translate("put on some trap drums at 140", runner=runner) == "beat trap 140"


def test_translate_strips_prose_and_backticks(monkeypatch):
    monkeypatch.delenv("ABL_NO_LLM", raising=False)
    runner = runner_returning("Sure! Here you go:\n`abl keys rhodes Am-F-C-G`\n")
    assert translate("some sad rhodes chords", runner=runner) == "keys rhodes Am-F-C-G"


def test_translate_sends_the_request_and_the_grammar_to_the_model(monkeypatch):
    monkeypatch.delenv("ABL_NO_LLM", raising=False)
    runner = runner_returning("go")
    translate("start it up", runner=runner)
    args, prompt = runner.calls[0]
    assert "start it up" in prompt
    assert "beat <style>" in prompt
    assert "haiku" in " ".join(args)
    assert "--no-session-persistence" in args and "--disable-slash-commands" in args
    assert args[args.index("--tools") + 1] == ""


def test_translate_returns_none_when_nothing_parses(monkeypatch):
    monkeypatch.delenv("ABL_NO_LLM", raising=False)
    assert translate("???", runner=runner_returning("I cannot help with that.")) is None


def test_translate_returns_none_when_the_runner_fails(monkeypatch):
    monkeypatch.delenv("ABL_NO_LLM", raising=False)

    def runner(args, prompt):
        raise FileNotFoundError("claude")

    assert translate("anything", runner=runner) is None


def test_translate_is_off_with_abl_no_llm(monkeypatch):
    monkeypatch.setenv("ABL_NO_LLM", "1")
    runner = runner_returning("go")
    assert translate("start", runner=runner) is None
    assert runner.calls == []
