# Session Recipes — verified tool sequences

Every sequence here ran successfully against Live 12.2.5 / bridge 1.8.1 on 2026-09-28. Copy the shape, swap the content. All indices 0-based, times in beats (4.0 = one 4/4 bar).

## R0. Orient (always first)
```
get_session_info            # tempo, signature, is_playing, track_count, scenes
get_session_snapshot        # every track: index, name, type, devices, clip count
```
The user's default set has 4 empty template tracks (`1-MIDI`, `2-MIDI`, `3-Audio`, `4-Audio`) and returns `A-Reverb`, `B-Delay`. Never assume — the user may be editing Live concurrently (playback state and track count changed mid-session).

## R1. New instrument track, safely (the index-shift fix)
```
create_midi_track(index=-1)          # reply may say "Created new MIDI track: 7-MIDI" with NO index
get_session_snapshot                  # find the new track's real index (last track, name "N-MIDI")
set_track_name(track_index=<real>, name="...")
load_instrument_or_effect(track_index=<real>, uri="<from library-catalog.md>")
get_track_info(<real>)                # confirm devices == [instrument]
```
Never chain create → set_track_name → load in one `batch_commands` with a hardcoded index. Do one create at a time and read back.

## R2. Replace an instrument on a track
```
get_track_info(t)                     # note device index (usually 0)
delete_device(track_index=t, device_index=0)
load_instrument_or_effect(t, uri)
```

## R3. Resize / rebuild a clip
There is no resize call. `delete_clip(t, c)` then `create_clip(t, c, length=<beats>)`. `generate_chord_progression` and `generate_voiced_progression` auto-create/resize their clip (voiced verified 2026-09-28); treat every other generator and `add_notes_to_clip` as needing `create_clip` first.

## R4. 808 drum track (classic 808 Core Kit)
```
load_instrument_or_effect(t, "query:Drums#FileId_5409")     # "808 Core Kit.adg"
get_drum_pads(t, device_index=0)
```
Pad map (MIDI note → sound): 36 Bass Drum · 37 Rim Shot · 38 Snare · 39 Hand Clap · 40 Low Conga · 41 Mid Conga · 42 Closed HH · 43 Hi Conga · 44 Low Tom · 45 Mid Tom · 46 Open HH · 47 Hi Tom · 48 Maracas · 49 Cymbal · 50 Cow Bell · 51 Claves.

Pop/backbeat 2 bars (8 beats): kick 36 @ 0,2,4,6 (v118/112); snare 38 + clap 39 @ 1,3,5,7 (v105/90); closed hat 42 every 0.5 (v80 on beats, 60 off); open hat 46 @ 3.5 and 7.5 (v85–90).

Trap 2 bars: kick @ 0, 2.75, 4, 5.5, 6.75; snare/clap @ 1, 3, 5, 7; hats every 0.5 with rolls (0.25 spacing) on the last beat of bar 2; open hat sparse.

## R5. 808 sub bass
`load_instrument_or_effect(t, "query:Sounds#Bass:FileId_6515")` — "Sub 808 Bass.adv". Alternates: `808 Pure.adg` FileId_5164, `808 Drifter.adg` FileId_5163, `808 Slapping.adg` FileId_5166, `Sub 808 Pitch Boom.adg` FileId_5251, `Talking 808 Bass.adg` FileId_5263 (all `query:Sounds#Bass:`). Sustained notes under each kick, pitch 24–36 (Live C0–C1), velocity 110–120, legato durations to the next hit.

## R6. Jazz combo (4-bar I–vi–ii–V)
Tracks: drums (808 Core Kit reprogrammed), `Upright Bass.adv` = `query:Sounds#Bass:FileId_6516`, `E-Piano Rhodish.adg` = `query:Sounds#Piano%20&%20Keys:FileId_4849`, solo voice `Horns Mellow.adg` = `query:Sounds#Brass:FileId_5144` (**no saxophone exists in this library** — say so up front; alt `Basic Silk Horns.adg` FileId_5137).
```
generate_voiced_progression(piano, 0, "Cmaj7-Am7-Dm7-G7", style="rootless", center_pitch=62, velocity=58, voices=4, humanize=5)   # creates 16-beat clip
create_clip(bass, 0, 16); generate_walking_bass(bass, 0, "Cmaj7-Am7-Dm7-G7", key="C", scale="major", octave=2, ghost=0.15, velocity=92)   # octave=2 → root at MIDI 36, line walks 36–46 (verified); octave=1 for 808 register
create_clip(solo, 0, 16); generate_melody(solo, 0, "Cmaj7-Am7-Dm7-G7", key="C", scale="bebop", density="medium", phrase_arc="arch", chromatic=0.25, low=55, high=82, swing=0.63)
create_clip(drums, 0, 16); add_notes_to_clip(drums, 0, <swing grid below>)
set_clip_loop(t, 0, start=0, end=16, looping=True) for each; fire_clip(t, 0) for each
```
Swing drum grid per bar b∈{0,4,8,12}: ride 49 @ b, b+1, b+1.667, b+2, b+3, b+3.667 (v80/88/62); hat-foot 42 @ b+1, b+3 (v55, dur 0.15); feathered kick 36 @ b, b+2 (v38–42); rim 37 / snare 38 comping on off-beat "a" positions (x.667), one accent into the top of the form.

## R7. Swing / groove
- Hand-placed 8th-note swing: off-beats at **+0.667** (triplet feel), not +0.5.
- Groove Pool (`get_grooves`) ships one groove: index 0 "Swing 16ths 66" — `set_clip_groove(t, c, groove_index=0)` then `set_groove_amount`. Good for hip-hop/house hats, wrong for jazz 8ths.
- `generate_melody(..., swing=0.5..0.66)` swings its own output. `humanize_clip(t, c, timing=0.02, velocity=8)` for feel.

## R8. One-call genre starters
`apply_recipe("lofi_beat")` — 82 BPM, F minor, 4 bars: swung drums, walking upright, rootless Rhodes.
`apply_recipe("house_groove")` — 124 BPM, A minor, 4 bars: four-on-the-floor, offbeat bass, shell piano stabs.
Check `list_recipes` for defaults; not batchable.

## R9. Playback and verification
```
fire_clip(t, c) per track  (or fire_scene(s) for a whole row)
get_session_info           # is_playing should now be true (fire replies are pre-state)
get_clip_notes(t, c)       # verify content actually landed
stop_all_clips / stop_playback
```
Use `batch_commands` for multi-step note edits: one round trip and one `undo` step. Batch translations: `load_instrument_or_effect` → pass `item_uri` (and `uri`).

## R10. If everything times out
A modal dialog is open in Live (e.g. trial nag). Ask the user to press Enter in Live, then re-read state before retrying — a timeout is not proof the edit failed.
