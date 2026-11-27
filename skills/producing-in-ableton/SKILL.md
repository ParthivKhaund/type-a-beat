---
name: producing-in-ableton
description: Use when the user mentions Ableton, Live, AbletonMCP, their DAW, or asks to make, edit, play, arrange, or mix music in Ableton — before calling any mcp__AbletonMCP__ tool, searching the Live browser, or deciding which instrument or device to load.
---

# Producing in Ableton

## Overview
> Written against the author's install (Live 12 Lite, Core Library only). If your edition, packs or plugins differ, refresh `library-catalog.md` first (see "Refresh the catalog" below) and trust it over the absent-lists here.

This user's Ableton Live 12.2.5 is the **Intro/Lite edition**: 17 Audio Effects (no EQ Eight, Glue Compressor, or Multiband Dynamics), 6 instrument types (no Wavetable/Operator/Analog/Collision/Electric/Tension/Sampler/Meld), no Max for Live, and **zero third-party plugins**. The 170-tool AbletonMCP bridge and the full browser catalog are already documented here. **Read the catalog, don't explore.** Core rule: **read state → act → read back → verify.** Live is a shared, live instrument the user may be touching at the same time.

## Fast path: abl (no LLM, sub-second)
For the everyday loop — `beat <style> [bpm]`, `drums`, `bass [sound]`, `keys [sound] <chords>`, `tempo`, `go`, `stop`, `mute/solo/louder/quieter <role>`, `swing`, `hats`, `undo` — the user has `abl` (from the type-a-beat repo, installed on PATH). It speaks the same Remote Script socket directly and runs alongside this MCP. When the user asks for one of those actions, tell them the `abl` line (e.g. `abl "beat trap 140; bass 808; go"`) rather than driving it through MCP calls; use this skill for everything creative or open-ended. abl only overwrites clips it wrote itself and never deletes tracks it did not create.

## When to use
- Any request that will touch Live (beat, chords, instrument, mix, playback).
- Before `search_browser` / `get_browser_items_at_path` — check `library-catalog.md` first.
- Before any `batch_commands` or a `create_*` call.

Pair with `producing-music` for *what* to write (patterns, harmony, arrangement); this skill covers *how* to do it in Live.

## Files
| File | Read it when |
|---|---|
| `library-catalog.md` | Choosing any sound, kit, device, plugin; checking what does NOT exist |
| `tools-reference.md` | Unsure of a tool's params, flags, batchability |
| `session-recipes.md` | Building a track/beat/combo — verified sequences with URIs |
| `device-guide.md` | Setting EQ/comp/reverb/etc. parameters, chains, sidechain |

## Workflow contract
1. Tools may still be "connecting" at session start: `ToolSearch("select:mcp__AbletonMCP__get_session_info,...")` waits for them.
2. `get_session_info` + `get_session_snapshot` before the first edit.
3. Create one track at a time; **read the new index back** (`get_session_snapshot`) before naming/loading. Never hardcode an assumed index in a batch.
4. Pick URIs from the catalog. Only search for things the catalog marks unknown.
5. Generators that auto-create their clip: `generate_chord_progression` (documented), `generate_voiced_progression` (verified). For every other generator and `add_notes_to_clip`, `create_clip` first.
6. After writing notes: `get_clip_notes`; after firing: `get_session_info` (fire replies report pre-state).
7. Tell the user immediately when a requested sound doesn't exist (no sax, no acoustic jazz kit, no grand-piano search hits — see catalog) and name the stand-in.

## Gotchas (each one cost time before)
| Symptom | Fix |
|---|---|
| About to recommend EQ Eight, Glue Compressor, Wavetable, Operator, a Suite device, M4L, or a VST | **Don't — none exist in this user's Live (Intro/Lite edition, zero 3rd-party plugins).** Use Channel EQ (not EQ Eight), Compressor (not Glue Compressor), Drift/Simpler/Drum Sampler/Impulse (not Suite synths). Full absent-list in `library-catalog.md` › "NOT available"; substitutes in `device-guide.md` |
| `describe_device`/`list_known_devices` mention a device | That's Ableton's general curated knowledge, NOT a check against this install — verify with `get_browser_items_at_path("audio_effects")` or `search_browser` before recommending it |
| Wrong track renamed/loaded | Track count can shift mid-session; read index back after every create |
| `Missing required parameter: item_uri` in batch | In `batch_commands`, `load_instrument_or_effect` takes `item_uri` (pass both) |
| Batch fails on generate_*/load_drum_kit/apply_recipe/save_set/record_section | Not batchable — call directly |
| Notes vanished | `add_notes_to_clip` REPLACES; use `edit_notes` to add/remove a subset |
| Clip too short | No resize tool: `delete_clip` → `create_clip(length)` |
| Every call times out | Modal dialog in Live; ask user to press Enter; re-read state, don't blindly retry |
| Loudness/level | Fader 0.85 = 0 dB; device params are native range — `get_device_parameters` first |
| Swing sounds straight | 8th swing = off-beats at +0.667 beats; Groove Pool only has "Swing 16ths 66" |

## Want → do
| Want | Do |
|---|---|
| Classic 808 drums | `query:Drums#FileId_5409` (808 Core Kit), pad map in recipes R4 |
| Heavy sub | `Sub 808 Bass.adv` `query:Sounds#Bass:FileId_6515` |
| Jazz/neo-soul keys | `E-Piano Rhodish` `query:Sounds#Piano%20&%20Keys:FileId_4849` |
| Upright bass | `query:Sounds#Bass:FileId_6516` |
| Sax/horn solo | No sax; `Horns Mellow` `query:Sounds#Brass:FileId_5144` |
| Master/bus EQ | `Channel EQ` (not EQ Eight — absent) `query:AudioFx#Channel%20EQ` |
| Bus glue compression | Plain `Compressor` (not Glue Compressor — absent) `query:AudioFx#Compressor` |
| Full mastering chain | `Master Full Chain` rack `query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5527` (verify chain after loading) |
| Genre starter in one call | `apply_recipe("lofi_beat" \| "house_groove")` |
| Multi-step edit, one undo | `batch_commands` |

## Refresh the catalog
When the user installs packs/plugins: re-run the enumeration described at the top of `library-catalog.md` (read-only browser calls, sequential) and update the Plugins/Packs/best-picks sections.

## Red flags — stop and read the catalog/recipes
- About to call `search_browser` for a common sound.
- About to write `track_index` you didn't read back this session.
- About to batch a `generate_*` call.
- About to promise a sound (sax, strings, choir) without checking "NOT available".
