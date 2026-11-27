#!/bin/zsh
# Set up Type a Beat on a Mac: abl on PATH, Claude skills linked, AbletonMCP registered and its
# Remote Script installed, the voice model downloaded. --analyzer also builds the recreate models.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
WITH_ANALYZER=0
for arg in "$@"; do [[ "$arg" == "--analyzer" ]] && WITH_ANALYZER=1; done
step() { print -P "%F{cyan}==>%f $1"; }
note() { print -P "%F{yellow}   note:%f $1"; }

[[ "$(uname)" == "Darwin" ]] || { echo "Type a Beat needs macOS (Ableton Live and the Apple GPU models)."; exit 1; }
command -v brew >/dev/null || { echo "Install Homebrew first: https://brew.sh"; exit 1; }
command -v uv >/dev/null || { echo "Install uv first: curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }

step "Homebrew tools: ffmpeg, yt-dlp, whisper-cpp"
for formula in ffmpeg yt-dlp whisper-cpp; do
  brew list "$formula" >/dev/null 2>&1 || brew install "$formula"
done

step "abl on PATH (editable install from $REPO)"
uv tool install --editable "$REPO" --force >/dev/null
print "   $(abl --version)"

step "Claude skills -> ~/.claude/skills (symlinks into this repo)"
mkdir -p "$HOME/.claude/skills"
BACKUP="$HOME/.abl/backup/skills-$(date +%Y%m%d-%H%M%S)"
for dir in "$REPO"/skills/*(/); do
  name="${dir:t}"
  target="$HOME/.claude/skills/$name"
  if [[ -L "$target" ]]; then
    ln -sfn "$dir" "$target"
  elif [[ -e "$target" ]]; then
    mkdir -p "$BACKUP" && mv "$target" "$BACKUP/" && ln -s "$dir" "$target"
    note "moved your existing $name skill to $BACKUP"
  else
    ln -s "$dir" "$target"
  fi
  print "   $name -> $dir"
done

step "AbletonMCP server in Claude Code"
if command -v claude >/dev/null; then
  if claude mcp list 2>/dev/null | grep -q "^AbletonMCP"; then
    print "   already registered"
  else
    claude mcp add --scope user AbletonMCP -- uvx mcp-server-ableton-live@1.8.1 && print "   registered"
  fi
else
  note "Claude Code not found; register later with: claude mcp add --scope user AbletonMCP -- uvx mcp-server-ableton-live@1.8.1"
fi

step "AbletonMCP Remote Script in Live's User Library"
uvx --from mcp-server-ableton-live@1.8.1 ableton-live-mcp install || note "Remote Script install reported a problem; run: uvx --from mcp-server-ableton-live@1.8.1 ableton-live-mcp doctor"

step "Voice model (whisper.cpp base.en)"
MODEL="$HOME/.abl/models/ggml-base.en.bin"
if [[ -f "$MODEL" ]]; then
  print "   already downloaded"
else
  mkdir -p "${MODEL:h}" && curl -L --fail -o "$MODEL" "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin"
fi

if (( WITH_ANALYZER )); then
  step "Analyzer for recreate (several GB, one time)"
  "$REPO/analyzer/setup.sh"
else
  note "skipped the recreate models; run scripts/install.sh --analyzer when you want recreate and analyze"
fi

step "Done. Next:"
print "   1. Open Live > Settings > Link, Tempo & MIDI > Control Surface: AbletonMCP"
print "   2. abl status"
print "   3. Optional voice hotkey: open 'extras/abl voice.shortcut', allow Running Scripts in Shortcuts > Settings > Advanced, assign a key"
