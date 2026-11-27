"""`abl` entry point: one-shot (`abl "beat trap 140; go"`) or a REPL (`abl`)."""

from __future__ import annotations

import argparse
import atexit
import os
import sys
import time
from typing import Callable

from abl import __version__
from abl.actions import ActionError, execute
from abl.commands import ParseError, is_known_verb, parse, split_chain
from abl.fallback import translate
from abl.session import Session
from abl.voice import Listener
from abl.wire import DEFAULT_HOST, DEFAULT_PORT, LiveClient, LiveError

HISTORY_FILE = os.path.expanduser("~/.abl_history")
EXIT_WORDS = {"quit", "exit", "q"}
VOICE_WORDS = {"v", "voice", "listen"}
EXIT_OK, EXIT_LIVE, EXIT_PARSE = 0, 1, 2


def run_line(line: str, session: Session, use_llm: bool, out: Callable[[str], None]) -> int:
    for part in split_chain(line):
        try:
            command = parse(part)
        except ParseError as exc:
            translated = translate(part) if use_llm and not is_known_verb(part) else None
            if translated is None:
                out(f"?? {exc}")
                return EXIT_PARSE
            out(f"-> {translated}")
            command = parse(translated)
        started = time.perf_counter()
        try:
            message = execute(command, session, progress=out)
        except (ActionError, LiveError) as exc:
            out(f"!! {exc}")
            return EXIT_LIVE
        out(f"{message}  [{(time.perf_counter() - started) * 1000:.0f} ms]")
    return EXIT_OK


def _setup_readline() -> None:
    try:
        import readline
    except ImportError:
        return
    try:
        readline.read_history_file(HISTORY_FILE)
    except OSError:
        pass
    readline.set_history_length(500)
    atexit.register(lambda: _save_history(readline))


def _save_history(readline) -> None:
    try:
        readline.write_history_file(HISTORY_FILE)
    except OSError:
        pass


def repl(session: Session, use_llm: bool, input_fn: Callable[[str], str], out: Callable[[str], None], listener: Listener | None = None) -> int:
    _setup_readline()
    out(f"abl {__version__} - type help; v to talk; quit to leave")
    while True:
        try:
            line = input_fn("abl> ")
        except (EOFError, KeyboardInterrupt):
            out("")
            return EXIT_OK
        line = line.strip()
        if not line:
            continue
        if line.lower() in EXIT_WORDS:
            return EXIT_OK
        if line.lower() in VOICE_WORDS:
            (listener or Listener()).listen_once(session, out, use_llm)
            continue
        run_line(line, session, use_llm, out)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="abl", description="Fast, LLM-free control of Ableton Live. No arguments opens a REPL.")
    parser.add_argument("line", nargs="*", help='commands, chain with ";"  e.g. "beat trap 140; bass 808; go"')
    parser.add_argument("--no-llm", action="store_true", help="never translate unknown lines with a model (same as ABL_NO_LLM=1)")
    parser.add_argument("--listen", action="store_true", help="tap-to-talk: record one spoken command, run it, show a notification")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--version", action="version", version=f"abl {__version__}")
    return parser


def main(argv: list[str] | None = None, client_factory: Callable | None = None, input_fn: Callable[[str], str] = input, out: Callable[[str], None] = print, listener: Listener | None = None) -> int:
    args = _parser().parse_args(argv)
    use_llm = not args.no_llm and not os.environ.get("ABL_NO_LLM")
    factory = client_factory or (lambda host, port: LiveClient(host=host, port=port))
    session = Session(factory(args.host, args.port))
    if args.listen:
        return (listener or Listener()).listen_once(session, out, use_llm)
    if args.line:
        return run_line(" ".join(args.line), session, use_llm, out)
    return repl(session, use_llm, input_fn, out, listener)


if __name__ == "__main__":
    sys.exit(main())
