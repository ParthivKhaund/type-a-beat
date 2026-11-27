# Type a Beat

Make music in Ableton Live by typing or talking, with Claude as the producer.

- **abl** is a fast command line. `abl "beat trap 140; keys rhodes Am-F-C-G; bass 808"` has a beat playing in about a second. No AI in the loop.
- **Voice**: type `v` at the `abl>` prompt and speak. Recognised on your Mac with whisper.cpp.
- **Import**: `abl "import <youtube url or file>"` puts a song on its own audio track.
- **Recreate**: `abl "recreate <youtube url or file>"` splits a song into stems, finds tempo, key, sections, chords, drums and bass, and lays it out in Live.
- **Claude skills**: `producing-in-ableton`, `producing-music` and `/abl` teach Claude Code how to work in Live.

New to all of this? Read [docs/beginner-guide.md](docs/beginner-guide.md).

## Set up

Needs macOS on Apple Silicon, Ableton Live 12 (any edition, built on Lite), [Homebrew](https://brew.sh), [uv](https://docs.astral.sh/uv/) and [Claude Code](https://claude.com/claude-code).

```bash
git clone https://github.com/ParthivKhaund/type-a-beat.git ~/type-a-beat
~/type-a-beat/scripts/install.sh               # abl, skills, AbletonMCP, voice model
~/type-a-beat/scripts/install.sh --analyzer    # also the recreate models (about 3 GB, one time)
```

Then open Live, pick **AbletonMCP** as a Control Surface in Settings > Link, Tempo & MIDI, and run `abl status`.

## How Claude fits in

| Piece | Where | What it does |
| --- | --- | --- |
| AbletonMCP server | `claude/mcp.json` | Lets Claude act inside Live through the AbletonMCP Remote Script (port 9877). Third-party, open source: [`mcp-server-ableton-live`](https://pypi.org/project/mcp-server-ableton-live/). |
| `producing-in-ableton` | `skills/` | How to drive Live: a library catalog with browser URIs, verified tool sequences, a device guide. |
| `producing-music` | `skills/` | What to write: drum patterns, harmony, arrangement, sound and mix advice. |
| `abl` | `skills/` | `/abl <line>` runs one abl command from inside Claude Code. |

`scripts/install.sh` symlinks the skills into `~/.claude/skills/`, so a `git pull` updates Claude too.

The library catalog (`skills/producing-in-ableton/library-catalog.md` and `abl/catalog.json`) describes one specific Live 12 Lite install. After adding packs or plugins, run `abl catalog` and ask Claude to refresh `library-catalog.md` as described at its top.

## What's where

| Folder | Contents |
| --- | --- |
| `abl/`, `tests/` | The command line and its tests (a fake Live, runs anywhere) |
| `analyzer/` | Song analysis for `recreate` and `analyze` |
| `skills/` | The three Claude Code skills |
| `claude/` | AbletonMCP config |
| `docs/` | [Beginner guide](docs/beginner-guide.md) and [abl reference](docs/abl-reference.md) |
| `extras/` | The "abl voice" Shortcut for a voice hotkey |
| `scripts/` | `install.sh` |

## Develop

```bash
uv run pytest
cd analyzer && uv run pytest --ignore=tests/test_e2e_synthetic.py
```

## Rules abl keeps

- It never changes a clip it did not write (its clips are named `abl ...`) and never deletes a track it did not create.
- Tempo changes only when you give a number.
- It checks Live Lite's 8-track and 8-scene caps before changing anything.

Not affiliated with Ableton or Anthropic. Recreating a song to study or remix at home is fine; publishing a copy of someone's track is a different matter.
