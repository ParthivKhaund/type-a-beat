# abl

Fast, LLM-free command line for Ableton Live. Type `beat trap 140` and a trap beat is playing in Live under a second.

It talks straight to the AbletonMCP Remote Script socket (127.0.0.1:9877), the same one the MCP server uses, so it runs alongside Claude Code without conflict. Claude stays the brain for creative work; `abl` is the hands for everything you say more than once a session.

## Install

```bash
uv tool install --editable .
```

Live must be open with the AbletonMCP Remote Script loaded (it says "AbletonMCP: Listening for commands on port 9877" in Live's status bar).

## Use

```bash
abl                                  # REPL with history; macOS dictation types straight into it
abl "beat trap 140; bass 808; keys rhodes Am-F-C-G; go"
abl status
```

## Three ways in

| Way | How |
| --- | --- |
| Terminal | `abl "beat trap 140"` or the `abl` REPL |
| Claude Code | `/abl beat trap 140` (the `abl` skill in `~/.claude/skills/abl` runs it in one Bash call; plain sentences are translated by Claude) |
| Voice | `v` at the `abl>` prompt, or `abl --listen` from a hotkey. Records until you stop talking, transcribes on-device with whisper.cpp, normalizes the words ("a minor f c g" becomes `Am-F-C-G`, "one forty" becomes `140`), runs the line, and posts a macOS notification with the result |

Voice needs `brew install whisper-cpp ffmpeg` and the model at `~/.abl/models/ggml-base.en.bin` (`ABL_WHISPER_MODEL` to override). `extras/abl voice.shortcut` is a signed Shortcut that runs `abl --listen`; import it, turn on Allow Running Scripts (Shortcuts menu, Settings, Advanced), and give it a keyboard shortcut in its (i) panel. First run asks for microphone access. `ABL_MIC=":1"` picks another input device.

## Grammar

```
beat <style> [bpm]      styles: trap boombap hiphop house techno pop lofi jazz swing
drums <style>           same as beat, never changes tempo
bass [sound] [style]    sounds: 808 sub pure upright synth analog reese 303 saw fm electric
keys [sound] <chords> [stab|hold]   sounds: rhodes epiano wurli piano organ pad
                        chords: Cmaj7-Am7-Dm7-G7  or  Am F C G  (one chord per bar)
tempo <bpm>
go | play               fire every abl clip and start the transport
stop                    stop the transport
mute|unmute|solo|unsolo <drums|bass|keys|lead|track name|index>
louder|quieter <role> [steps]        one step = 0.05 on the fader
swing <50-75>           re-renders the drum clip with MPC-style 16th swing (50 = straight)
hats double|half|normal|off
clear <role>            delete the abl clip for that role
kill <role>             delete the role track (only if abl created it)
undo | redo | status | tracks | help
import <url or file>    download a song and put it on an audio track
recreate <url or file> [fresh]   analyze a song and lay it into Live
analyze <url or file> [fresh]    the analysis alone
catalog                 rescan Live's browser after installing packs or plugins
```

A line the grammar rejects is sent to a small model (`claude -p --model haiku`) which returns one grammar line; abl prints it, then runs it. That path takes several seconds because the `claude` CLI has to start, so it is a last resort, not the fast path. Turn that off with `--no-llm` or `ABL_NO_LLM=1`.

## Import a song

```bash
abl "import https://www.youtube.com/watch?v=..."
abl "import ~/Music/song.mp3"
```

Downloads the audio (yt-dlp), converts it to 44.1 kHz WAV, and puts it on an audio track named after the song: an empty template audio track like `3-Audio` if there is one, else a new audio track. Nothing else in the set changes, and a full Lite set is refused before anything downloads. The audio lands in the same cache as `recreate`, so recreating the same link later skips the download. If YouTube answers with a 403, run `brew upgrade yt-dlp`; YouTube breaks older downloaders every few weeks.

## Recreate a song (Tier 3)

```bash
abl "recreate https://www.youtube.com/watch?v=..."
abl "analyze ~/Music/song.mp3"
```

`recreate` downloads the audio (yt-dlp), splits it into six stems (Demucs htdemucs_6s on the Apple GPU: drums, bass, vocals, guitar, piano, other), then runs the best model available for each question and lays the answer into Live: tempo and key set, one scene per section named after it, MIDI clips on the Drums, Bass, Keys, and Lead tracks in the section's slot, the same clips laid left to right in Arrangement view with a locator per section, and the original audio muted on a Reference track for A/B. `analyze` prints the same report without touching Live. Add `fresh` to redo the analysis of a cached song (its stems are kept).

| Question | Engine | Fallback |
| --- | --- | --- |
| Beats, downbeats, sections with labels | All-In-One (Kim & Nam 2023), through a pure-PyTorch shim for its NATTEN attention | Beat This! (2024) for beats and downbeats, then librosa |
| Drum hits (kick, snare, hat, tom, cymbal) | ADTOF, in its own TensorFlow environment | Onset detection with band-energy classification |
| Chords per bar and key | Root-weighted chroma templates with Viterbi smoothing on bass + harmonic stems; Krumhansl key profiles | — |
| Keys part | ByteDance piano transcription when the piano stem carries it, else Basic Pitch on the guitar or harmonic stem; the Keys sound follows (piano, guitar, or Rhodes) | — |
| Bass and lead | Basic Pitch (isolated subprocess) | — |

**Choosing sounds.** The drum kit is the library kit whose own kick, snare, and hat samples sit closest to the song's hits (every kit preset is parsed once into `~/.abl/kits.json`, packs included), and the drum notes land on that kit's real pads. Bass, keys, and lead are tagged by CLAP, a zero-shot audio model, with role-restricted prompts ("an upright acoustic bass", "a hammond organ"...), and each tag maps to keyword searches over the catalog. Run `abl catalog` after installing packs or plugins so the searches see them; it walks Live's browser into `~/.abl/catalog.json`.

What to expect: tempo, downbeats, sections, drums, and bass are strong; chords are good for pop, hip-hop, and house and weak for jazz; keys and lead are transcriptions to edit, not finished parts. The sounds are Live Lite stand-ins. Results are cached in `~/.abl/cache/<song>/`, so a second run is instant.

The analyzer lives in `analyzer/` with its own Python 3.11 environment. Run `analyzer/setup.sh` once: it syncs the main environment, builds the isolated ADTOF environment, and fetches the piano checkpoint. abl calls the analyzer as a subprocess and streams its progress. Live Lite's 8-scene cap means long songs are merged into 8 sections.

## Rules it follows

- Role tracks are found by exact name: Drums, Bass, Keys, Lead (MIDI tracks only). Missing ones are created at the end, inside the same batch as the first clip.
- New material goes to the first empty clip slot. Clips abl writes are named `abl <what>`, and before abl reuses or rewrites a slot it checks that its own clip is still there. Anything else in that slot is left alone and a fresh slot is used.
- `kill` checks the track's identity, not just its name: if you delete abl's track and later name your own track "Keys", `kill keys` refuses.
- If you add a track in Live in the split second between abl reading the set and its batch landing, abl notices the index mismatch, undoes its batch, and asks you to try again.
- Loading a sound onto a role track that already has a different instrument replaces it; the result line says what was replaced. Every mutating command is one `batch`, so one `undo` in abl (or Cmd-Z in Live) reverts it.
- `kill` refuses tracks abl did not create.
- Tempo changes only when you give a number.
- Live 12 Lite caps a set at 8 tracks and 8 scenes. When the set is full, abl tells you and suggests renaming an existing MIDI track to Drums, Bass, Keys, or Lead so it can reuse it.

## Why it is fast

One Live round trip is about 400 ms. abl reads the session snapshot once, then sends every edit for a command in a single `batch`. On an existing role track a write is three round trips (snapshot, slot check, batch); creating the track adds one re-read to pin ownership. `go`, `stop`, `tempo`, `mute`, and friends are one or two.

## Develop

```bash
uv run pytest                              # fake Live, no Ableton needed
ABL_LIVE=1 uv run pytest -m live -s        # scratch-track round trip against a real Live
```

Modules: `wire` (socket), `theory` (chords, voicings), `patterns` (drum lanes, bass, keys), `catalog` (URIs verified for this Live Intro/Lite library), `commands` (grammar), `session` (tracks, ownership), `actions` (batches), `fallback`, `cli`.

Sounds and kits come from the `producing-in-ableton` skill catalog and are specific to Ableton Live 12 Intro/Lite with no third-party plugins.
