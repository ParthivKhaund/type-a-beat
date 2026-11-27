# AbletonMCP Tools Reference

Every `mcp__AbletonMCP__*` tool, grouped by the server's own capability map, with required
params, key optional params (defaults), and risk flags. Built from the live tool schemas on
2026-09-28 (156 tools: every tool the server exposes). Read this instead of loading schemas one at a time.

**Flags:** DESTRUCTIVE = replaces/overwrites/deletes content · NOT-BATCHABLE = composite, cannot
go inside `batch_commands` · READ-ONLY = changes nothing · CREATES-CLIP-IF-EMPTY = writes into an
empty slot without `create_clip` · PRE-STATE-REPLY = reply shows state *before* the command ran ·
SHIFTS-INDICES = later indices move after this call.

---

## Conventions (from the server)

- **All indices are 0-based**: `track_index`, `clip_index` (Session slot), `scene_index`,
  `return_index` (0 = Return A), `device_index` (position in the track's chain),
  `send_index` (0 = Return A).
- **Times, lengths, positions are in BEATS** (quarter notes), floats allowed. `4.0` = one 4/4 bar;
  `8.0` = bar 3 in 4/4.
- **Volume faders**: Live's normalized `0.0–1.0`, where **`0.85` = 0 dB unity**. Same for
  `set_master_volume`, `set_send`, and meter readings (`0.85` ≈ 0 dB).
- **Device parameters use each parameter's native range** — call `get_device_parameters`
  (or the `_master_`/`_return_` variant) first and read min/max/display before setting. Numeric
  values are clamped; display strings like `'250 Hz'`, `'-6 dB'` or exact enum labels also work;
  unsupported mappings fail before writing.
- **MIDI notes**: `pitch` 0–127 (**60 = C3 in Live's naming**), `velocity` 1–127,
  `start_time`/`duration` in beats relative to clip start, `mute` bool.
- **Transport replies are PRE-state**: `start_playback` may answer `playing: false` right after
  starting. Confirm with `get_session_info`.
- **A timeout is not proof of failure** — inspect state (`get_session_snapshot`, `session_diff`)
  before retrying, or you will double-apply the edit.
- **If every call suddenly times out, a modal dialog is open in Live** (e.g. the trial nag). It
  freezes the Remote Script. Ask the user to press Enter in Live, then retry.
- **Typical workflow**: `create_midi_track` → *read back the new index* → `load_instrument_or_effect`
  (or `search_browser` + load) → `create_clip` → `add_notes_to_clip` → `fire_clip` /
  `duplicate_to_arrangement`. Check `get_session_info` / `get_track_info` first.
- **Prefer `batch_commands`** for multi-step edits: one round trip, one undo step.
- Mix heuristics (`analyze_mix`) are not measured audio; decoded sample peak/RMS
  (`analyze_audio_file`) is not LUFS.

---

## Session (transport, global state, scenes)

| Tool | Purpose | Required params | Key optional params (defaults) | Flags |
|---|---|---|---|---|
| get_session_info | Global set + transport state: tempo, sig, position, play state, loop, track/return/scene counts, scene names, key/scale, record mode, launch quantization, master vol/pan, Live version | — | — | READ-ONLY |
| get_session_snapshot | One-call overview: tempo, sig, play state, every track's name/type/mute/solo/arm/volume/clip count/device names, return names. Prefer over many get_track_info calls | — | — | READ-ONLY |
| session_diff | What changed since the LAST session_diff call (tempo, tracks added/removed/renamed/reordered, per-track vol/mute/solo/arm/clip count/devices). First call = baseline only | — | — | READ-ONLY |
| set_tempo | Set BPM | `tempo` (number) | — | — |
| tap_tempo | Tap once; repeated taps set tempo, single tap nudges transport. Returns resulting tempo | — | — | — |
| set_time_signature | Global time signature (does not rewrite clip notes) | `numerator`, `denominator` (ints ≥1) | — | — |
| set_metronome | Click on/off | `enabled` (bool) | — | — |
| set_song_scale | Song key context | — | `root_note` 0–11 (0=C, 2=D…) (null), `scale_name` e.g. "Major"/"Minor"/"Dorian" (null) | — |
| get_scale_info | Scale name, root, intervals, active tuning system (Live 12.3+) | — | — | READ-ONLY |
| start_playback | Start Arrangement playback from current song time | — | — | PRE-STATE-REPLY |
| stop_playback | Stop transport | — | — | PRE-STATE-REPLY |
| continue_playing | Resume from current position (start_playback restarts from last start point) | — | — | PRE-STATE-REPLY |
| set_record_mode | Arm/disarm global Arrangement Record (still need armed tracks + start_playback) | `enabled` (bool) | — | — |
| set_session_record | Toggle Session record into armed tracks' selected slots; enables MIDI overdub | `enabled` (bool) | — | — |
| trigger_session_record | Start Session recording into armed tracks | — | `record_length` beats, e.g. 16.0 = 4 bars, then auto-switches to playback (null) | — |
| set_session_automation_record | Record parameter rides into Session clip envelopes | `enabled` (bool) | — | — |
| set_arrangement_overdub | Layer recorded MIDI onto existing arrangement clips instead of replacing | `enabled` (bool) | — | — |
| capture_midi | Live's Capture MIDI → new clip (needs recently played MIDI on armed/monitored track) | — | — | — |
| capture_and_insert_scene | Snapshot currently playing Session clips into a new scene | — | — | SHIFTS-INDICES (adds scene) |
| set_clip_trigger_quantization | Global launch quantization: 0=None, 4=1 bar (default), 7=1/4, 13=1/32 | `value` (int) | — | — |
| set_groove_amount | Global Groove Amount 0.0–1.0 | `amount` | — | — |
| set_swing_amount | Global swing 0.0–1.0 used when quantizing with swing | `amount` | — | — |
| get_grooves | Groove Pool list (index + name) and global groove amount | — | — | READ-ONLY |
| set_ableton_link | Enable/disable Ableton Link | `enabled` (bool) | — | — |
| set_master_volume | Main/Master fader 0.0–1.0 (0.85 = 0 dB) | `volume` | — | — |
| get_master_meters | Master output meters; pinned near 1.0 = clipping | — | — | READ-ONLY |
| set_crossfader | Master crossfader -1.0 (A) … 0 … 1.0 (B) | `value` | — | — |
| create_scene | New scene row; -1 appends | — | `index` (-1) | SHIFTS-INDICES when index ≥ 0 |
| delete_scene | Delete a scene row | `scene_index` | — | DESTRUCTIVE, SHIFTS-INDICES |
| duplicate_scene | Copy a scene incl. all its clips (new content, scene count +1) | `scene_index` | — | SHIFTS-INDICES |
| set_scene_name | Rename a scene | `scene_index`, `name` | — | — |
| fire_scene | Launch a scene row with launch quantization | `scene_index` | — | — |
| stop_all_clips | Stop every playing Session clip (transport keeps running) | — | — | — |
| setup_session | Bootstrap: set tempo + create named MIDI tracks, optionally loading instruments by search query | `tempo`, `tracks` [{"name", "instrument"?}] | `instrument` = search_browser query, best match loaded; omit for empty track | Composite (server-side multi-step); verify indices after |
| save_set | Save to existing file IF the Live API supports it (most versions do not). Returns availability + success | — | — | NOT-BATCHABLE |

---

## Tracks (regular, return, group)

| Tool | Purpose | Required params | Key optional params (defaults) | Flags |
|---|---|---|---|---|
| create_midi_track | New MIDI track; -1 = end of list | — | `index` (-1) | SHIFTS-INDICES when index ≥ 0; **reply index not reliable — read back** |
| create_audio_track | New empty audio track; -1 appends | — | `index` (-1, min -1) | SHIFTS-INDICES when index ≥ 0; read back |
| create_return_track | New return (send bus) track | — | — | — |
| delete_track | Delete a regular track | `track_index` | — | DESTRUCTIVE, SHIFTS-INDICES |
| delete_return_track | Delete a return track (0 = Return A) | `return_index` | — | DESTRUCTIVE, SHIFTS-INDICES |
| duplicate_track | Copy a track incl. devices + clips (track count +1) | `track_index` | — | SHIFTS-INDICES |
| get_track_info | One track: name/type, mixer, arm/mute/solo, sends, freeze/color, playing/fired slots, every slot's clip state, device chain names/types | `track_index` | — | READ-ONLY |
| get_return_tracks | List returns (index + name) | — | — | READ-ONLY |
| get_track_meters | Post-fader L/R meters (0.85 ≈ 0 dB); poll during playback to "listen" | `track_index` | — | READ-ONLY |
| set_track_name | Rename a track | `track_index`, `name` | — | — |
| set_track_color | Color index 0–69 in Live's palette | `track_index`, `color_index` | — | — |
| set_track_volume | Fader 0.0–1.0 (0.85 = 0 dB) | `track_index`, `volume` | — | — |
| set_track_pan | Pan -1.0 (L) … 0.0 … 1.0 (R) | `track_index`, `pan` | — | — |
| set_track_mute | Mute/unmute | `track_index`, `mute` (bool) | — | — |
| set_track_solo | Solo/unsolo (other solos stay — clear separately) | `track_index`, `solo` (bool) | — | — |
| set_track_arm | Arm/disarm (fails on group/return tracks) | `track_index`, `arm` (bool) | — | — |
| set_track_monitoring | Input monitoring 0=In, 1=Auto, 2=Off (needed for resampling/bounce) | `track_index`, `state` (int) | — | — |
| get_track_routing | Input/output routing (current + options by display_name) and monitoring state | `track_index` | — | READ-ONLY |
| set_track_routing | Set routing by display name. `field`: input_routing_type / output_routing_type / input_routing_channel / output_routing_channel | `track_index`, `field`, `display_name` | — | Get options from get_track_routing first |
| set_send | Send level 0.0–1.0 (send_index 0 = Return A) | `track_index`, `send_index`, `value` | — | — |
| set_crossfade_assign | Crossfader side: 0=A, 1=none, 2=B | `track_index`, `assign` (0–2) | — | — |
| get_group_info | Is group track? inside a group? fold state, parent group name | `track_index` | — | READ-ONLY |
| set_fold_state | Fold/unfold a group track (errors if not a group) | `track_index` | `folded` (true) | — |
| create_take_lane | Add a take lane for comping; returns new lane count | `track_index` | — | — |

---

## Clips (Session view)

| Tool | Purpose | Required params | Key optional params (defaults) | Flags |
|---|---|---|---|---|
| create_clip | Empty MIDI clip in a Session slot. Fails if slot occupied or track is audio | `track_index`, `clip_index` | `length` beats (4) | — |
| create_audio_clip | Import an audio file into an EMPTY slot on an AUDIO track. Requires Live ≥ 12.0.5 | `track_index`, `clip_index`, `path` (absolute) | — | — |
| delete_clip | Delete the clip in a slot (slot stays, indices don't shift; fails on empty slot) | `track_index`, `clip_index` | — | DESTRUCTIVE |
| add_notes_to_clip | **REPLACES the clip's entire note content**. Clip must exist | `track_index`, `clip_index`, `notes` [{pitch, start_time, duration, velocity, mute}] | — | DESTRUCTIVE |
| edit_notes | Add/remove a subset of notes without rewriting the rest. `remove` matches by pitch+start_time | `track_index`, `clip_index` | `add` [{pitch,start_time,duration,velocity,mute}] (null), `remove` [{pitch,start_time}] (null) | Safe incremental edit |
| get_clip_notes | Every MIDI note (pitch, start, duration, velocity, mute). Fails on empty slot / audio clip | `track_index`, `clip_index` | — | READ-ONLY |
| get_clip_info | Full clip state: loop points, markers, playing position, per-clip sig; audio: file path, gain, warp markers | `track_index`, `clip_index` | — | READ-ONLY |
| set_clip_name | Rename clip | `track_index`, `clip_index`, `name` | — | — |
| set_clip_color | Palette color 0–69 | `track_index`, `clip_index`, `color_index` | — | — |
| set_clip_loop | Loop brace / start marker / looping on one clip; omitted fields unchanged | `track_index`, `clip_index` | `start`, `end` (clip-relative beats, end > start), `start_marker`, `looping` (all null) | Provide ≥1 optional |
| set_clip_signature | Per-clip time signature (polymeter) | `track_index`, `clip_index`, `numerator`, `denominator` | — | — |
| set_clip_groove | Attach a Groove Pool groove by index; omit to clear | `track_index`, `clip_index` | `groove_index` (null = clear) | — |
| set_clip_audio | Audio-clip props: gain 0–1, pitch_coarse -48..48, pitch_fine cents, warping, warp_mode 0=Beats 1=Tones 2=Texture 3=Re-Pitch 4=Complex 6=Complex Pro | `track_index`, `clip_index` | `gain`, `pitch_coarse`, `pitch_fine`, `warping`, `warp_mode` (all null) | — |
| fire_clip | Launch one Session clip (replaces other playing clip on that track) | `track_index`, `clip_index` | — | — |
| stop_clip | Stop a playing clip | `track_index`, `clip_index` | — | — |
| duplicate_clip_to | Copy a clip to any other track/scene slot (**overwrites destination**) | `src_track`, `src_scene`, `dst_track`, `dst_scene` | — | DESTRUCTIVE (dest) |
| clip_operation | Structural edits. `op`: "duplicate_loop" (double loop + notes), "crop" (discard outside loop), "duplicate_region" (copy region_start/region_length → destination_time, optional transposition_amount; pitch=-1 = all) | `track_index`, `clip_index`, `op` | `region_start`, `region_length`, `destination_time`, `transposition_amount`, `pitch` (all null) | DESTRUCTIVE (crop) |
| humanize_clip | Read notes, jitter timing + velocity, write back | `track_index`, `clip_index` | `timing` beats (0.02), `velocity` (8), `seed` (null) | DESTRUCTIVE (replaces notes) |
| quantize_clip | Quantize to grid: quarter/eighth/eighth_triplet/sixteenth/sixteenth_triplet/thirtysecond | `track_index`, `clip_index` | `grid` ("sixteenth"), `amount` 0–1 (1.0) | DESTRUCTIVE (moves notes) |
| transform_clip | Motif transform: transpose (amount = semitones), invert, retrograde, augment (amount = time factor > 0). Overwrites source unless dest_clip_index given (then dest is REPLACED) | `track_index`, `clip_index`, `op` | `amount` (0), `dest_clip_index` (null) | DESTRUCTIVE |
| write_automation | Clip automation envelope for a device parameter; **replaces existing envelope for that param** | `track_index`, `clip_index`, `device_index`, `parameter` (name or index), `points` [{time, value}] | — | DESTRUCTIVE (envelope) |
| clear_automation | Delete one parameter's ENTIRE envelope on a clip (not a time range) | `track_index`, `clip_index`, `device_index`, `parameter` | — | DESTRUCTIVE (envelope) |
| re_enable_automation | Restore automation overridden by manual parameter changes (setting a param with an envelope overrides it until this is called) | — | — | — |

---

## Devices (track, chain, master, return, drum rack, simpler, loading)

| Tool | Purpose | Required params | Key optional params (defaults) | Flags |
|---|---|---|---|---|
| get_device_parameters | All params of a device on a track: names, values, min/max, display strings. **Call before any set_device_parameter** | `track_index`, `device_index` | — | READ-ONLY |
| set_device_parameter | Set one param. Number = native range (clamped/quantized); string = display units ('250 Hz', '-6 dB') or exact enum label. Returns Live's readback + warnings | `track_index`, `device_index`, `parameter` (name or index), `value` (number or string) | — | Overrides automation until re_enable_automation |
| set_device_enabled | Enable (true) / bypass (false) a device, preserving params | `track_index`, `device_index`, `enabled` | — | — |
| delete_device | Remove a device from a track chain | `track_index`, `device_index` | — | DESTRUCTIVE, SHIFTS-INDICES (later devices) |
| describe_device | Curated guidance for a native device (EQ Eight, Compressor, Glue Compressor, Reverb, Auto Filter, Saturator, Utility, Limiter, Delay…): which params matter, units, sensible values | `device_name` (case-insensitive) | — | READ-ONLY (static knowledge) |
| list_known_devices | Devices that describe_device covers | — | — | READ-ONLY |
| get_device_routing | Sidechain input routing (type/channel + options). Only Compressor/Gate-type devices | `track_index`, `device_index` | — | READ-ONLY |
| set_device_routing | Set sidechain source. `field`: "input_routing_type" (source track/return) or "input_routing_channel" (Pre FX / Post FX / Post Mixer); `display_name` from get_device_routing. Also enable device's Sidechain param via set_device_parameter | `track_index`, `device_index`, `field`, `display_name` | — | — |
| get_rack_chains | List an Instrument/Effect Rack's chains and nested devices | `track_index`, `device_index` | — | READ-ONLY |
| set_chain_device_parameter | Set a param on a device INSIDE a rack chain (indices from get_rack_chains); clamps to native range | `track_index`, `device_index`, `chain_index`, `chain_device_index`, `parameter`, `value` (number) | — | — |
| rack_variation | Macro snapshots. `action`: "store", "recall" (needs `index`), "randomize" (all macros) | `track_index`, `device_index`, `action` | `index` (null) | randomize = DESTRUCTIVE to current macro state |
| get_drum_pads | Drum Rack occupied pads (MIDI note, name, mute, solo) | `track_index`, `device_index` | — | READ-ONLY |
| set_drum_pad | Mute/solo/rename a Drum Rack pad by MIDI note (36 = kick) | `track_index`, `device_index`, `note` | `mute`, `solo`, `name` (all null) | — |
| get_master_device_parameters | Params of a device on the Master chain | `device_index` | — | READ-ONLY |
| set_master_device_parameter | Set one param on a Master-chain device (same value rules as set_device_parameter). Affects the full mix | `device_index`, `parameter`, `value` | — | — |
| get_return_device_parameters | Params of a device on a return track | `return_index`, `device_index` | — | READ-ONLY |
| set_return_device_parameter | Set one param on a return-chain device | `return_index`, `device_index`, `parameter`, `value` | — | — |
| set_simpler_playback_mode | Simpler mode 0=Classic, 1=One-Shot, 2=Slicing (errors if not a Simpler) | `track_index`, `device_index`, `mode` | — | — |
| replace_simpler_sample | Swap a Simpler's sample with an absolute local audio path. Requires Live 12.4+ AND runtime API support | `track_index`, `device_index`, `path` | — | DESTRUCTIVE (replaces musical content) |
| load_instrument_or_effect | Load an instrument/effect onto a track by browser URI. Appends to chain (repeat calls = duplicates) | `track_index`, `uri` | — | **In batch_commands the internal name is `load_browser_item` and it needs `item_uri`** |
| load_device_to_master | Load a browser device onto Master (e.g. limiter) | `item_uri` | — | Appends; repeats duplicate |
| load_device_to_return | Append a browser device/preset to a return track's chain (selects the return in Live) | `return_index`, `item_uri` | — | Appends; repeats duplicate |
| load_drum_kit | Two-step: load a Drum Rack (`rack_uri`), then the first loadable kit at `kit_path` (e.g. "drums/acoustic"). If path fails, empty rack remains | `track_index`, `rack_uri`, `kit_path` | — | NOT-BATCHABLE; repeats add racks |

---

## Browser

| Tool | Purpose | Required params | Key optional params (defaults) | Flags |
|---|---|---|---|---|
| search_browser | Case-insensitive substring search by display name → loadable items with URIs. **Prefer this when you know a name** | `query` | `category` one of instruments/sounds/drums/audio_effects/midi_effects/packs (null = all), `max_results` (25) | READ-ONLY |
| get_browser_tree | Shallow listing of top-level categories + immediate entries | — | `category_type` "all"/"instruments"/"sounds"/"drums"/"audio_effects"/"midi_effects" ("all") | READ-ONLY |
| get_browser_items_at_path | Items at "category/folder/subfolder" (e.g. "sounds/Piano & Keys") | `path` | — | READ-ONLY |
| preview_browser_item | Audition an item through Live's preview tab without loading | `item_uri` | — | — |
| stop_browser_preview | Stop the preview | — | — | — |

---

## Arrangement (timeline, playhead, locators, bounce)

| Tool | Purpose | Required params | Key optional params (defaults) | Flags |
|---|---|---|---|---|
| duplicate_to_arrangement | Copy a Session clip onto the Arrangement at `destination_time` on the same track. **OVERWRITES whatever overlaps the destination range** (this is also how you REPLACE a section). Call once per repeat | `track_index`, `clip_index`, `destination_time` (beats) | — | DESTRUCTIVE |
| get_arrangement_clips | List a track's Arrangement clips (name, start_time, end_time, length, type) | `track_index` | — | READ-ONLY |
| delete_arrangement_clip | Delete a clip by its position in get_arrangement_clips' list | `track_index`, `arrangement_clip_index` | — | DESTRUCTIVE, SHIFTS-INDICES (re-read between deletes) |
| set_arrangement_time | Move playhead to an absolute beat | `time` | — | — |
| set_loop | Global Arrangement loop region + enabled state (region updates even when enabled=false) | `start` (beats ≥0), `length` (>0) | `enabled` (true) | — |
| jump_by | Move playhead by relative beats (negative = back); works during playback | `beats` | — | — |
| jump_to_cue | Playhead to next (direction ≥0) or previous (<0) locator | — | `direction` (1) | — |
| jump_to_locator | Playhead to a locator by index from get_locators | `locator_index` | — | — |
| get_locators | List locators (index, name, beat time) | — | — | READ-ONLY |
| create_locator | Create/rename a locator at an absolute beat. **SIDE EFFECT: moves the playhead to `time` first.** Existing locator at that time is reused/renamed | `time` (≥0) | `name` (null = Live's generated name) | Moves playhead |
| back_to_arranger | Return playback control to the Arrangement (clears the orange Back-to-Arrangement state) | — | — | — |
| switch_to_arrangement_view | Show the Arrangement view in Live's window | — | — | — |
| record_section | Bounce an arrangement section to WAV without the Export dialog: temp audio track, input = `source`, arms, records start→end in REAL TIME (capped 5 min). Returns WAV path | `start_beat`, `end_beat` | `source` ("Resampling" = master; or a track name), `cleanup` (true; false keeps the recording track) | NOT-BATCHABLE; runs transport; adds an arrangement clip |

---

## Generators (write MIDI into a Session clip)

All generate_* tools are composite and **NOT-BATCHABLE**. All REPLACE the target clip's notes.
See "Generator tools quick guide" below for progression/scale/key formats.

| Tool | Purpose | Required params | Key optional params (defaults) | Flags |
|---|---|---|---|---|
| generate_chord_progression | Voiced chords from chord symbols. Creates clip if slot empty; otherwise resizes loop + replaces notes | `track_index`, `clip_index`, `progression` | `beats_per_chord` (4), `center_pitch` (60), `rhythm` held/stabs/quarters ("held"), `strum` beats (0.02), `velocity` (62) | DESTRUCTIVE, NOT-BATCHABLE, CREATES-CLIP-IF-EMPTY |
| generate_voiced_progression | Voice-led jazz voicings. `style`: rootless (3-7-9-13), quartal, shell (root-3-7), block | `track_index`, `clip_index`, `progression` | `style` ("rootless"), `beats_per_chord` (4), `center_pitch` (60), `voices` (4), `velocity` (64), `humanize` (4), `seed` (null) | DESTRUCTIVE, NOT-BATCHABLE, CREATES-CLIP-IF-EMPTY (verified 2026-09-28: wrote 16 notes into an empty slot, clip sized to chords × beats_per_chord) |
| generate_genre_progression | Genre-idiomatic progression (lofi, boom_bap, hip_hop, trap, house, deep_house, techno, trance, dnb, rnb, neo_soul, jazz, bossa_nova, ambient, synthwave, pop, afrobeats, amapiano… fuzzy) transposed into key+scale, then voiced. Returns chord symbols used | `track_index`, `clip_index`, `genre` | `key` ("C"), `scale` ("minor"), `bars` = number of chords (4), `beats_per_chord` (4), `center_pitch` (60), `style` ("rootless"), `voices` (4), `velocity` (64), `seed` (null) | DESTRUCTIVE, NOT-BATCHABLE |
| generate_bassline | Bassline under a progression. `style`: roots, root_fifth, walking, eighth_pump. `octave`: 1 = MIDI 24, 2 = MIDI 36 (scientific numbering — Live labels 36 as "C1") | `track_index`, `clip_index`, `progression` | `style` ("roots"), `octave` (2), `beats_per_chord` (4), `velocity` (88) | DESTRUCTIVE, NOT-BATCHABLE |
| generate_walking_bass | Quarter-note walking bass: root on 1, chord/scale tones, chromatic approach on last beat, ghost notes | `track_index`, `clip_index`, `progression` | `key` ("C"), `scale` ("minor"), `octave` (2), `ghost` 0–1 (0.15), `beats_per_chord` (4), `velocity` (90), `seed` (null) | DESTRUCTIVE, NOT-BATCHABLE |
| generate_melody | Voice-led melody over a progression from key+scale. `density` low/medium/high; `phrase_arc` rising/arch/ascend_descend/static; `chromatic` 0–1; `low`/`high` MIDI bounds; `swing` 0.5 straight … ~0.66 | `track_index`, `clip_index`, `progression` | `key` ("C"), `scale` ("minor"), `density` ("medium"), `phrase_arc` ("arch"), `chromatic` (0.15), `low` (60), `high` (84), `swing` (0.5), `beats_per_chord` (4), `seed` (null) | DESTRUCTIVE, NOT-BATCHABLE |
| generate_drum_pattern | Genre drum pattern on a Drum Rack track. `style`: lofi, boom_bap, house, techno, trap, dnb, ambient. Standard Live drum map (36 kick, 38 snare, 42/46 hats) | `track_index`, `clip_index` | `style` ("lofi"), `bars` (2), `swing` beats 0.0–0.1 (0.06 ≈ MPC), `humanize` velocity (6), `seed` (null) | DESTRUCTIVE, NOT-BATCHABLE |
| generate_groove | Pocketed drum groove. `style`: lofi, boom_bap, house, trap, jazz, funk. `pocket` beats behind (0–0.1), `swing` 0.5–~0.66, `ghost` 0–1 | `track_index`, `clip_index` | `style` ("lofi"), `bars` (2), `pocket` (0.02), `swing` (0.55), `ghost` (0.3), `humanize` (8), `seed` (null) | DESTRUCTIVE, NOT-BATCHABLE |
| generate_euclidean_drums | Bjorklund rhythm for ONE drum voice. pulses=3, steps=8 = tresillo. `instrument`: kick/snare/chat/ohat/clap/ride/… or raw MIDI number | `track_index`, `clip_index` | `pulses` (3), `steps` (8; 16 = 16ths), `rotate` (0), `instrument` ("kick"), `bars` (2), `velocity` (100), `humanize` (6), `seed` (null) | DESTRUCTIVE, NOT-BATCHABLE |
| generate_additive | Philip Glass additive process: motif from `pitches` (space/comma MIDI numbers), plays first 1, first 2, first 3… notes. `steps` 0 = all | `track_index`, `clip_index` | `pitches` ("60 62 64 65 67 69"), `note_length` (0.5), `steps` (0), `velocity` (90), `source_clip_index` (null = read motif from that clip instead) | DESTRUCTIVE, NOT-BATCHABLE |
| generate_phase | Steve Reich phasing: motif from `pitches`, stacked `repeats` copies each `shift` beats later | `track_index`, `clip_index` | `pitches` ("60 62 64 67 69"), `note_length` (0.5), `repeats` (8), `shift` (0.25), `velocity` (90), `source_clip_index` (null) | DESTRUCTIVE, NOT-BATCHABLE |
| write_drum_grid | Drums from an ASCII grid of 16th steps. Lines "name: pattern"; chars X (vel 105) x (85) o (55) . or - (rest). Instruments: kick snare rim clap chat phat ohat ltom mtom htom crash ride perc shaker or raw MIDI "36: x..." | `track_index`, `clip_index`, `grid` | `swing` (0) | DESTRUCTIVE (replaces notes); batchable status unverified — treat as NOT-BATCHABLE to be safe |

---

## Audio (files, samples)

| Tool | Purpose | Required params | Key optional params (defaults) | Flags |
|---|---|---|---|---|
| analyze_audio_file | Measure a local WAV/AIFF/FLAC/Ogg/MP3/AAC/M4A: per-channel sample peak/RMS dBFS, DC offset, crest factor, full-scale samples. First `max_seconds` only. **Not LUFS or true peak.** No Live needed | `path` | `max_seconds` (30, max 120) | READ-ONLY |
| *(see also)* | create_audio_clip, set_clip_audio, replace_simpler_sample, record_section, set_track_monitoring, set_track_routing (resampling) | | | |

---

## Analysis (live set, key detection, meters)

| Tool | Purpose | Required params | Key optional params (defaults) | Flags |
|---|---|---|---|---|
| analyze_mix | Heuristic session-state leads (high faders, muted/empty tracks, MIDI track with no devices). **Not audio/LUFS measurement** | — | — | READ-ONLY |
| detect_clip_key | Key/scale of one Session MIDI clip (Krumhansl-Kessler): best key, confidence -1..1, margin, runner-up | `track_index`, `clip_index` | `weight` duration/velocity/product/count ("duration") | READ-ONLY |
| detect_track_key | Key of a whole track (pools all its Session clips) | `track_index` | `weight` ("duration") | READ-ONLY |
| detect_session_key | Key of the whole set (pools every MIDI track's Session clips) | — | `weight` ("duration") | READ-ONLY |
| *(see also)* | get_track_meters, get_master_meters, session_diff, get_session_snapshot | | | |

---

## Offline (.als / .adg / .adv with Live closed)

All take filesystem paths and never touch the running Live instance.

| Tool | Purpose | Required params | Key optional params (defaults) | Flags |
|---|---|---|---|---|
| als_summary | Version/creator, tempo, sig, each track's kind/name/mute/solo/devices/clip count/note count | `path` | — | READ-ONLY |
| als_list_tracks | Every track with its clips (name, MIDI/audio, start, length, looping, sample path, note count) | `path` | — | READ-ONLY |
| als_details | Locators (name + beat) and per-track fader volume, pan, automation-lane count | `path` | — | READ-ONLY |
| als_extract_midi | Notes {pitch,start,duration,velocity} per clip for one track (index from als_summary) | `path`, `track_index` | — | READ-ONLY |
| als_detect_key | Key/scale of a saved set (all MIDI clips, or one track) | `path` | `track_index` (null = all), `weight` ("duration") | READ-ONLY |
| als_diff | Diff two .als files: tempo/sig, tracks added/removed, per-track device/clip/note/mute deltas | `path_a`, `path_b` | — | READ-ONLY |
| als_find_unfinished | Lint: no master limiter/compressor, MIDI track w/o instrument, empty MIDI clip, empty audio track, muted tracks | `path` | — | READ-ONLY |
| adg_summary | .adg/.adv summary: name, rack type, device count, chain count, macro count, required edition, `is_drum_rack` | `path` | — | READ-ONLY |
| adg_analyze | Full .adg/.adv analysis: macros, recursive chain/device tree, macro mappings, referenced samples, edition, drum pad map | `path` | — | READ-ONLY |
| adg_edition | Required Live edition ("suite"/"standard"/"intro") + the devices that drove the verdict | `path` | — | READ-ONLY |

---

## Recipes (one-call scaffolding)

| Tool | Purpose | Required params | Key optional params (defaults) | Flags |
|---|---|---|---|---|
| list_recipes | Built-in recipes (name, description, default tempo/key/scale/bars) | — | — | READ-ONLY |
| apply_recipe | Scaffold a genre starter: set tempo, add Drums/Bass/Chords MIDI tracks, load instruments, write generated parts. Adds tracks; does not overwrite existing ones | `name` (from list_recipes, e.g. "lofi_beat", "house_groove") | `tempo`, `key`, `scale`, `bars` (all null = recipe default) | NOT-BATCHABLE; read back indices after |
| *(see also)* | setup_session (Session group) — tempo + named tracks + instruments by search query | | | |

---

## Meta

| Tool | Purpose | Required params | Key optional params (defaults) | Flags |
|---|---|---|---|---|
| describe_capabilities | Server map: tool groups, what each covers, conventions. Orient before first call | — | — | READ-ONLY |
| batch_commands | Run several commands in ONE round trip and ONE undo step; stops at first error | `commands` [{"type", "params"}] | — | See cheat sheet below |
| undo | Revert the top undo-history entry (no target param; Live picks) | — | — | Mutates set |
| redo | Reapply the last undone action | — | — | Mutates set |

---

## batch_commands cheat sheet

**Format**

```json
{"commands": [
  {"type": "set_tempo",         "params": {"tempo": 84}},
  {"type": "create_clip",       "params": {"track_index": 2, "clip_index": 0, "length": 8}},
  {"type": "add_notes_to_clip", "params": {"track_index": 2, "clip_index": 0, "notes": [
      {"pitch": 36, "start_time": 0.0, "duration": 0.5, "velocity": 100, "mute": false}]}},
  {"type": "set_clip_name",     "params": {"track_index": 2, "clip_index": 0, "name": "Kick"}}
]}
```

- `type` = the MCP tool name (without the `mcp__AbletonMCP__` prefix). "The few that differ are
  auto-translated" — but not their param names (see below).
- One round trip, **one undo step** (`undo` reverts the whole batch).
- **Stops at the first error**; steps already completed stay applied (and are one undo away).
- Command results come back in order; a failed step reports which index failed.

**Param-name translations known**

| Tool you call | Internal command | Gotcha |
|---|---|---|
| load_instrument_or_effect | `load_browser_item` | Requires `item_uri`, not `uri`. Pass **both** `uri` and `item_uri` in a batch to be safe. |
| load_device_to_master / load_device_to_return | (same) | Already use `item_uri`. |

Everything else observed so far uses the same param names as the MCP tool schema.

**NOT batchable (composite, orchestrated server-side)** — call these on their own:

- `record_section`
- `load_drum_kit`
- `apply_recipe`
- `save_set`
- every `generate_*`: generate_additive, generate_bassline, generate_chord_progression,
  generate_drum_pattern, generate_euclidean_drums, generate_genre_progression, generate_groove,
  generate_melody, generate_phase, generate_voiced_progression, generate_walking_bass
- Treat as not batchable until proven otherwise: `write_drum_grid`, `humanize_clip`,
  `quantize_clip`, `transform_clip`, `setup_session` (all read-modify-write or multi-step).

**Batch-safe workhorses**: set_tempo, set_time_signature, create_midi_track / create_audio_track
(index -1 only — see verify pattern), set_track_name/color/volume/pan/mute/solo/arm, set_send,
create_clip, add_notes_to_clip, edit_notes, set_clip_name/color/loop, set_device_parameter,
set_device_enabled, duplicate_to_arrangement, set_arrangement_time, set_loop, create_locator,
fire_clip, fire_scene, stop_clip, create_scene, set_scene_name.

**Never put a track index you have not read back into a batch that also creates the track.**
Split into: batch A (create) → get_session_snapshot → batch B (name, load, clip, notes).

---

## Generator tools quick guide

**Shared formats**

- **progression**: dash-, comma-, or space-separated chord symbols, e.g. `"Dm7-G7-Cmaj7"`,
  `"Am9, Fmaj7, Cmaj9, G13"`. Supported qualities include maj7, m7, m9, 9, 13, 7#9, sus4, dim,
  add9 (plus plain major/minor triads).
- **key**: note name with optional accidental — `"C"`, `"F#"`, `"Bb"`. Default `"C"`.
- **scale**: `major`, `minor`, `dorian`, `lydian`, `mixolydian`, `blues`, `bebop`,
  `minor_pentatonic`, and more. Default `"minor"`.
- **pitches** (additive/phase): space- or comma-separated MIDI numbers, `"60 62 64 67 69"`.
- **seed**: integer for reproducibility on the tools that take it (drum_pattern, euclidean,
  groove, melody, genre_progression, voiced_progression, walking_bass, humanize_clip).
  Re-running with the same seed + params reproduces the same notes.
- **beats_per_chord**: default 4 (one 4/4 bar per chord). Clip length = chords × beats_per_chord.
- **center_pitch**: 60 = C3 in Live naming. Bass `octave` uses *scientific* octave numbers, one higher than Live's labels: `octave=1` → C at MIDI 24 (Live "C0"), `octave=2` → C at MIDI 36 (Live "C1"). Verified 2026-09-28: `generate_walking_bass(key="C", octave=2)` put the root at 36 and walked 36–46. For 808-register roots (24–33) use `octave=1`.

| Tool | Writes | Needs existing clip? |
|---|---|---|
| generate_chord_progression | Voiced chords (held / stabs / quarters) | **No** — creates clip if slot empty; otherwise resizes loop and replaces all notes |
| generate_voiced_progression | Voice-led jazz voicings (rootless/quartal/shell/block) | **No** — verified 2026-09-28: creates and sizes the clip in an empty slot |
| generate_genre_progression | Genre grammar → voiced chords in key+scale; returns symbols used (feed them to bassline/melody!) | Unverified — `create_clip` first, or test once on an empty slot and record the result here |
| generate_bassline | Root-based bass under progression | Same as above |
| generate_walking_bass | Quarter-note walking bass with approach tones | Same as above |
| generate_melody | Voice-led melody biased to chord tones, register bounded by low/high | Same as above |
| generate_drum_pattern | Full-kit genre pattern on standard drum map (Drum Rack track) | Same as above |
| generate_groove | Full-kit pocketed groove with ghost snares | Same as above |
| generate_euclidean_drums | ONE drum voice, Euclidean distribution. Layer voices by writing to separate clips or merging via get_clip_notes + edit_notes | Same as above |
| generate_additive | Glass additive process from motif (or from `source_clip_index`) | Same as above |
| generate_phase | Reich phasing texture from motif (or from `source_clip_index`) | Same as above |
| write_drum_grid | Exact drum hits from ASCII 16th grid (most precise drum tool) | "REPLACES existing notes" — `create_clip` first with length = steps/4 beats |
| humanize_clip | Jitters timing (±`timing` beats) and velocity (±`velocity`) of existing notes | **Yes** — reads the clip |
| quantize_clip | Snaps existing notes to grid, `amount` < 1.0 = partial | **Yes** |
| transform_clip | transpose / invert / retrograde / augment of existing notes; optional `dest_clip_index` (dest slot REPLACED) | **Yes** (source); dest slot content is replaced |

**Recommended chain for a musical section**

1. `generate_genre_progression` (or `generate_chord_progression` with your own symbols) on the
   Chords track → read the returned chord symbols.
2. Feed the *same* progression string into `generate_bassline` / `generate_walking_bass` on the
   Bass track and `generate_melody` on the Lead track so all parts share harmony.
3. `generate_drum_pattern` or `write_drum_grid` on the Drums track (must have a Drum Rack).
4. `humanize_clip` lightly (timing 0.01–0.02) if the generator output is too rigid.
5. Verify with `get_clip_notes` / `detect_clip_key`, then `fire_scene` or
   `duplicate_to_arrangement`.

---

## Verify-then-act patterns

**1. Creating a track — never assume the index**

`create_midi_track` / `create_audio_track` replies may not include a usable index, and if any
track was inserted earlier in the same batch or by the user, your assumed index is wrong. Today's
session edited the wrong track for exactly this reason.

```
create_midi_track {index: -1}
get_session_snapshot                       # find the new track: last entry, name "MIDI"/"Audio"
   -> track_index = N (confirm name + type)
batch_commands [
  set_track_name {track_index: N, ...},
  load_instrument_or_effect {track_index: N, uri: U, item_uri: U},
  create_clip {track_index: N, clip_index: 0, length: 8}
]
get_track_info {track_index: N}            # confirm device loaded and clip exists
```

Same rule after `setup_session`, `apply_recipe`, `duplicate_track`, `create_return_track`.

**2. Deleting shifts later indices**

`delete_track`, `delete_return_track`, `delete_scene`, `delete_device`,
`delete_arrangement_clip` all shift later indices down by one. Delete from highest index to
lowest, or re-read (`get_session_snapshot` / `get_track_info` / `get_arrangement_clips`) between
deletes. Inserting with `index ≥ 0` (create_*_track, create_scene, duplicate_*) shifts indices
up.

**3. Read device params before writing**

`get_device_parameters {track_index, device_index}` → note the parameter name/index, min, max,
display → `set_device_parameter` → read the returned readback; if it differs from intent the value
was clamped or quantized. Setting a param that has an automation envelope overrides the envelope
until `re_enable_automation`.

**4. Transport replies are pre-state**

After `start_playback` / `stop_playback` / `continue_playing`, call `get_session_info` and check
`is_playing` rather than trusting the reply.

**5. Timeouts**

A timeout does not mean the edit failed. Run `session_diff` (or `get_track_info` / `get_clip_notes`)
before retrying so you do not double-add notes, load a second instrument, or duplicate a clip on
the arrangement. If *every* call times out, a modal dialog is open in Live — ask the user to press
Enter in Live.

**6. Session vs Arrangement**

`duplicate_to_arrangement` OVERWRITES the overlapping range. Before writing over bar N,
`get_arrangement_clips` to see what is there. After Session clips are fired, Live shows the orange
"Back to Arrangement" state — call `back_to_arranger` before judging the arrangement by ear.

**7. Loading devices appends**

`load_instrument_or_effect`, `load_device_to_master`, `load_device_to_return`, `load_drum_kit`
each append a new device on every call. Check `get_track_info` device list before loading to avoid
stacking duplicates; `delete_device` to clean up.

**8. session_diff as a cheap assertion**

Call `session_diff` once before a multi-step edit (baseline), then again after; the diff should
list exactly the tracks/clips/devices you meant to change. Anything extra is a wrong-target bug.

---

## Unverified

None — all 155 tools in the requested list resolved via ToolSearch on 2026-09-28, plus
`set_loop` (present on the server, not in the original list; documented under Arrangement).
Batchability of `write_drum_grid`, `humanize_clip`, `quantize_clip`, `transform_clip` and
`setup_session` is not stated in the schemas; the server only names record_section,
load_drum_kit, apply_recipe, save_set and the generate_* tools as non-batchable.
