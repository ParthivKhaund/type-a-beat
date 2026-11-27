---
name: abl
description: Run one abl line against Ableton Live from inside Claude Code, e.g. "/abl beat trap 140; bass 808; go". Use when the user types /abl, or asks for a quick everyday Live action (beat, drums, bass, keys, tempo, go, stop, mute, solo, louder, quieter, swing, hats, clear, kill, undo, status, tracks) that abl covers, before reaching for AbletonMCP tools.
---

# /abl — fast path into Ableton Live

`abl` is the user's local, LLM-free command line for Live (from the type-a-beat repo, installed on PATH). It talks to the same Remote Script socket as AbletonMCP and answers in about a second. This skill exists so `/abl ...` inside Claude Code costs one Bash call and no deliberation.

## Do exactly this

1. Take everything after `/abl` as the line. If it is empty, run `abl --no-llm help` and show the output.
2. If the line already uses abl's grammar (its first word is one of: beat drums bass keys tempo go play stop mute unmute solo unsolo louder quieter swing hats clear kill undo redo status tracks help recreate analyze import catalog), run:
   ```bash
   abl --no-llm "<line>"
   ```
3. Otherwise the user spoke plainly ("something chill with piano"). Translate it yourself into ONE grammar line using the grammar below, show the line you chose, then run it with `--no-llm`. Do not call abl without `--no-llm`; you are the translator here, which is faster than abl's own Haiku fallback.
4. Print abl's output verbatim (one line per command, each ends with a timing). Add nothing unless abl printed an error (`!!` or `??`), in which case explain it in one sentence.

Never substitute AbletonMCP tool calls for a line abl can run. Use the `producing-in-ableton` skill only for things abl cannot do (arrangement, mixing, sound design, "make it sound like X").

## Grammar

```
beat <style> [bpm]      styles: trap boombap hiphop house techno pop lofi jazz swing
drums <style>           same as beat, never changes tempo
bass [sound] [style]    sounds: 808 sub pure upright synth analog reese 303 saw fm electric
keys [sound] <chords> [stab|hold]   sounds: rhodes epiano wurli piano organ pad
                        chords: Cmaj7-Am7-Dm7-G7  or  Am F C G  (one chord per bar, minor = m)
tempo <bpm>
go | play               fire every abl clip and start the transport
stop
mute|unmute|solo|unsolo <drums|bass|keys|lead|track name|index>
louder|quieter <role> [steps]
swing <50-75>
hats double|half|normal|off
clear <role> | kill <role>
undo | redo | status | tracks | help
import <url or file>             download a song and put it on an audio track (seconds)
catalog                          rescan Live's browser after installing packs or plugins
recreate <url or file> [fresh]   analyze a song and lay it into Live, one scene per section (takes minutes; streams progress)
analyze <url or file> [fresh]    the analysis alone: tempo, key, sections, chords
```

`recreate` and `analyze` run for minutes on a new song (Demucs stem separation). Run them with a long Bash timeout (600000 ms) and relay the progress lines as they come.

Chain with `;`. Put `keys` before `bass` so the bass follows the chords. Tempo changes only with a number.

## Facts that matter

- Live 12 Lite: 8 tracks and 8 scenes max. "Live could not create a track" means the set is full; tell the user to free a track or rename one to Drums/Bass/Keys/Lead.
- abl only rewrites clips it wrote (named `abl ...`) and only deletes tracks it created.
- If every command times out, a modal dialog is open in Live; ask the user to press Enter there.
