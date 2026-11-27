"""Last resort for a line the grammar rejects: ask a small model for one grammar line. Off with ABL_NO_LLM=1."""

from __future__ import annotations

import os
import subprocess
from typing import Callable, Iterator

from abl.commands import HELP, ParseError, parse

DEFAULT_MODEL = os.environ.get("ABL_LLM_MODEL", "haiku")
TIMEOUT_SECONDS = float(os.environ.get("ABL_LLM_TIMEOUT", "30"))

PROMPT = """\
You translate a music producer's request into exactly one line of the `abl` command grammar below.
Output ONLY the command line. No prose, no backticks, no explanation. If nothing fits, output: help

Grammar:
{help}

Request: {line}
"""


def default_runner(args: list[str], prompt: str) -> str:
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    result = subprocess.run(args, input=prompt, capture_output=True, text=True, timeout=TIMEOUT_SECONDS, env=env)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"exit {result.returncode}")
    return result.stdout


def _candidates(text: str) -> Iterator[str]:
    for raw in text.splitlines():
        line = raw.strip().strip("`").strip('"').strip("'").strip()
        if line.lower().startswith("abl "):
            line = line[4:].strip()
        if line:
            yield line


def translate(line: str, runner: Callable[[list[str], str], str] | None = None, model: str = DEFAULT_MODEL) -> str | None:
    if os.environ.get("ABL_NO_LLM"):
        return None
    runner = runner or default_runner
    args = [
        "claude", "-p", "--model", model, "--output-format", "text",
        "--tools", "", "--no-session-persistence", "--disable-slash-commands",
        "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
    ]
    try:
        output = runner(args, PROMPT.format(help=HELP, line=line))
    except Exception:
        return None
    for candidate in _candidates(output or ""):
        try:
            parse(candidate)
        except ParseError:
            continue
        return candidate
    return None
