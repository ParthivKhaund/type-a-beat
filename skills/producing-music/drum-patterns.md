# Drum Patterns Reference

BPM and swing numbers here match the canonical table in `SKILL.md`; if they ever differ, the table wins.

## How to read
- **16-step grids** = one 4/4 bar in 16th notes. `x` hit · `X` accent · `o` ghost (vel 30–55) · `.` rest. Steps 1|5|9|13 = beats 1|2|3|4. Step n → `start_time = (n−1) × 0.25`. Off-beat 8ths = steps 3,7,11,15 → 0.5, 1.5, 2.5, 3.5.
- **12-step grids** (marked `[12]`) = one bar in 8th-note triplets, for swing/shuffle feels. Step n → `start_time = (n−1) × 0.3333`. Beats at steps 1|4|7|10; the swung "a" of each beat is step 3|6|9|12 (0.667, 1.667, 2.667, 3.667).
- Every genre has a **Beats:** line — the authoritative paste-ready list. Grids are for scanning; if a grid and its Beats line disagree, the Beats line wins.
- **Pitches = the 808 Core Kit pad map (verified)**: kick **36** · rim **37** · snare **38** · clap **39** · low conga 40 · mid conga 41 · closed hat **42** · hi conga 43 · low tom **44** · mid tom **45** · open hat **46** · hi tom **47** · maracas/shaker **48** · cymbal/ride **49** · cowbell **50** · claves **51**. GM differs (ride 51, pedal hat 44, cowbell 56, maracas 70, claves 75, crash 49) — run `get_drum_pads` on any other kit.
- **Velocity shaping** (always): hats — beats 1 & 3 ≈ 80, beats 2 & 4 ≈ 72, off-beat 8ths ≈ 60, 16ths between ≈ 45; snare/clap 95–110; kick 105–120; ghost snares 30–50. Randomize ±6 (`humanize_clip(velocity=6)`).
- **Swing**: move every 2nd 8th (or 16th) late. 50% straight · 54–58% light (house/pop hats; MPC boom-bap kick/snare) · 60–70% hip-hop hats · 66% triplet (jazz, shuffle, gospel). 8th swing: 0.5 → 0.667 at 66%, → 0.58 at 58%. 16th swing: every 2nd 16th 0.25 → 0.29 (58%) … 0.33 (66%).
- **"Late" / drunk feel** (neo-soul, lo-fi, R&B): kick on-grid or 2–5 ms early, snare 10–30 ms late = 0.015–0.04 beats at 80 BPM (`start_time` 1.02–1.04 instead of 1.0); hats straight or lightly swung — the kick-pushes / snare-drags contrast is the feel.
- Length: write 2 bars minimum (bar 2 = bar 1 + one variation), 4 bars with a fill in bar 4. `b` below = bar offset (0, 4, 8, 12).
- AbletonMCP helpers: `write_drum_grid` (ASCII grid → notes, most precise), `generate_drum_pattern`, `generate_groove`, `generate_euclidean_drums`, `humanize_clip`, `quantize_clip`. `add_notes_to_clip` for exact control.

---

## HIP-HOP FAMILY

### Trap — 140 BPM (130–160), half-time, straight
```
        1...2...3...4...
kick    x..........x....    bar 2: x.....x....x....
snare   ........x.......    snare + clap on beat 3 only
chat    x.x.x.x.x.x.x.x.    8ths; roll on beat 4 of bar 2
ohat    ..............x.
```
**Beats (2 bars):** kick 36 @ 0, 2.75, 4, 5.5, 6.75 (v115) · snare 38 + clap 39 @ 2, 6 (v105/95) · chat 42 @ every 0.5 from 0 to 6.5 (v80 on beats, 60 off) · roll @ 7.0, 7.125, 7.25, 7.375, 7.5, 7.625, 7.75, 7.875 (v70→98 ramp) · ohat 46 @ 3.5, 7.5 (v70).
Hat-roll math: 32nds = 0.125; triplet 16ths = 0.1667; alternate a bar of 16ths with a bar of triplets; velocity crescendo. 808 mirrors the kick with slides on the last hit (`harmony-and-theory.md` › Bassline).
Variant "bounce": kick @ 0, 0.75, 2.75; ohat @ 1.5. NI variant (2 bars): kick @ 0, 3.0, 5.0; clap @ 2, 6; snare fill @ 7.0, 7.5; replace the last 8th hat of EVERY bar with 3×32nds @ b+3.5, b+3.625, b+3.75 (middle one v94).

### Drill (UK) — 142 BPM (138–146), half-time, 0% swing
```
        bar 1               bar 2
kick    x.............x.    x..x..x.......x.
snare   ........x.......    ............x...    beat 3 in bar 1 → beat 4 in bar 2 (the drill displacement)
chat    x..x..x........o    x..x..x........o    tresillo hats (3-3-2), soft pickup on step 16
```
**Beats (2 bars):** kick 36 @ 0, 3.5, 4, 4.75, 5.5, 7.5 (v115) · snare 38 + clap 39 @ 2.0, 7.0 (v110) · chat 42 @ 0, 0.75, 1.5, 4, 4.75, 5.5 (v100/87) and 3.75, 7.75 (v52), plus 16th/32nd rolls on the last beat of bar 2 · 808 glides between roots on the kick hits · no swing. NY/Chicago variant: snare on 3 every bar, chat 8ths with 16th stutters.

### Boom-bap — 90 BPM (85–95), MPC swing 54–58% (hats swung harder)
```
kick    x..x......x.x...
snare   ....X.......X...
ghost   ......o.......o.
chat    x.x.x.x.x.x.x.x.    swung
```
**Beats (per bar):** kick @ b, b+0.75, b+2.5, b+3 (v112) · snare @ b+1, b+3 (v110) · ghost snare @ b+1.5, b+3.5 (v40) · chat @ b, b+0.62, b+1, b+1.62, b+2, b+2.62, b+3, b+3.62 (hats 62%; kick/snare on a 54–58% 16th grid so the 0.75 kick sits ≈ 0.77; v78/58).
Variant "Dilla": hats straight at 0.5, kick 10 ms early (−0.015), snare 30 ms late (+0.045).

### Lo-fi — 80 BPM (70–90), swing 60–66%, snares late
```
kick    x.....x...x.....
snare   ....x.......x...    +10–30 ms; kick stays on-grid
chat    x.xxx.x.x.xxx.x.    or brushed 8ths at low velocity
shaker  ..x...x...x...x.
```
**Beats (per bar):** kick @ b, b+1.5, b+2.5 (v100) · snare @ b+1.03, b+3.03 (v95) · chat @ b, b+0.62, b+0.75, b+1, b+1.62, b+2, b+2.62, b+2.75, b+3, b+3.62 (v65/45) · shaker 48 @ b+0.5, b+1.5, b+2.5, b+3.5 (v40). Add vinyl noise, Saturator, LP 8 kHz.

---

## HOUSE / TECHNO / EDM FAMILY

### House — 124 BPM (120–128), 16th swing 54–58%
```
kick    x...x...x...x...
clap    ....x.......x...
ohat    ..x...x...x...x.    open hat on every off-beat 8th
chat    xx.xxx.xxx.xxx.x    16ths everywhere the open hat isn't
shaker  xxxxxxxxxxxxxxxx    v35–50
```
**Beats (per bar):** kick @ b, b+1, b+2, b+3 (v118) · clap 39 @ b+1, b+3 (v100) · ohat 46 @ b+0.5, b+1.5, b+2.5, b+3.5 (v85) · chat 42 @ b, b+0.25, b+0.75, b+1, b+1.25, b+1.75, b+2, b+2.25, b+2.75, b+3, b+3.25, b+3.75 (v45; 58% swing moves the .25/.75 hits to .29/.79) · shaker 48 16ths v40.
Deep house: rim 37 instead of clap, conga 41 @ b+1.75. Tech house: second kick layer, chat shorter, ohat duration 0.2.

### UK garage 2-step — 130 BPM (124–138), 16th swing 60–68%
```
kick    x.........x.....    two kicks a bar: 1 and the "and" of 3; no kick on 3
rim     ....x.......x...    rim or tight snare on 2 & 4
chat    x.xx.xx.xx.xxxx.    skippy 16ths (grid shows unswung positions)
```
**Beats (per bar):** kick @ b, b+2.5 (v112; bar 2 opens with a double: b, b+0.25) · rim 37 or tight snare 38 @ b+1, b+3 (v100) · chat @ b, b+0.5, b+0.79, b+1.29, b+1.5, b+2, b+2.29, b+2.79, b+3, b+3.29, b+3.5 (v70/50; 16th swing 60%: every .25 → .29, .75 → .79) · variants: kick @ b, b+1.5, b+2.5 or b, b+1.75, b+2.5.

### Techno — 130 BPM (125–140), straight
```
kick    x...x...x...x...
clap    ....x.......x...    rim or noise clap
chat    ..x...x...x...x.
ride    x.x.x.x.x.x.x.x.
perc    x..x..x..x..x..x    dotted-8th perc (3-3-3-3-3-1) — or Euclidean 5/16: x..x..x..x..x...
```
**Beats (per bar):** kick @ b, b+1, b+2, b+3 (v120) · clap/rim @ b+1, b+3 (v90) · chat @ b+0.5, b+1.5, b+2.5, b+3.5 (v70) · ride 49 8ths (v60) · perc 41 @ b, b+0.75, b+1.5, b+2.25, b+3, b+3.75 (v65). Add/remove one element every 8–16 bars; filters instead of fills.
Berlin variant: clap on beat 2 only (extra clap in the last bar of 8), LP-filtered low tom 44 @ b+1.5, b+3.5 as a second kick, noise stab on 3, hats off-beat. "Thumping" variant: snare on off-beats/16ths never on 2 & 4, ride on quarters.

### Trance / progressive — 138 BPM (136–142; progressive 128–134)
```
kick    x...x...x...x...
clap    ....x.......x...
ohat    ..x...x...x...x.
crash   x...............    every 8/16 bars
```
**Beats (per bar):** kick @ b, b+1, b+2, b+3 (v120) · clap @ b+1, b+3 (v105, layered) · ohat @ b+0.5, b+1.5, b+2.5, b+3.5 (v80) · crash 49 @ 0 of bars 1, 9, 17. Build (8 bars): snare @ quarters → 8ths → 16ths → 32nds, kick out for the last 1–2 bars.

### Big-room / EDM — 128 BPM (126–130)
```
kick    x...x...x...x...
clap    ....x.......x...
ohat    ..x...x...x...x.
```
**Beats:** same as trance; drop = kick + lead stab on every beat, clap on 2 & 4, white-noise riser into bar 1.

### Future bass — 150 BPM (140–160), half-time
```
kick    x.....x.....x...
snare   ........x.......    or clap on 2 & 4 for double-time sections
chat    x.x.x.x.x.x.x.x.
```
**Beats (per bar):** kick @ b, b+1.5, b+3 (v115) · snare + clap @ b+2 (v110) · chat @ 8ths (v60/45, filtered) · sidechain everything to the kick.

### Dubstep — 140 BPM (138–142), half-time
```
kick    x......x..x.....
snare   ........X.......
chat    x.x.x.x.x.x.x.x.    or triplets [12]: x.xx.xx.xx.x
```
**Beats (per bar):** kick @ b, b+1.75, b+2.5 (v118) · snare @ b+2 (v120, huge) · chat @ 8ths (v55) · wobble bass LFO at 1/4–1/8.

### Drum & bass — 174 BPM (165–178), 2-step break
```
kick    x.........x.....
snare   ....x.......x...
chat    x.x.x.x.x.x.x.x.
ghost   ..o.....o..o....
```
**Beats (per bar):** kick @ b, b+2.5 (v115) · snare @ b+1, b+3 (v110) · ghost snare @ b+0.5, b+2, b+2.75 (v40) · chat @ 8ths (v65/50); ride 49 8ths for liquid. "Amen" variant: kick @ b, b+0.5, b+2.5; snare @ b+1, b+1.75, b+3, b+3.5.

### Breakbeat / big beat — 125 BPM (110–135)
```
kick    x.....x.x.......
snare   ....x.......x..x
chat    x.x.x.x.x.x.x.x.
```
**Beats (per bar):** kick @ b, b+1.5, b+2 (v112) · snare @ b+1, b+3, b+3.75 (v108) · chat 8ths (v70/50).

---

## POP / R&B / SOUL FAMILY

### Pop — 110 BPM (95–125), straight, hats 54%
```
kick    x.......x.......    lift: x.....x.x.......
snare   ....x.......x...    snare + clap
chat    x.x.x.x.x.x.x.x.
ohat    ..............x.
```
**Beats (verified, per bar):** kick @ b, b+2 (v118/112) · snare 38 + clap 39 @ b+1, b+3 (v105/90) · chat @ 8ths (v80/60) · ohat @ b+3.5 (v88). Chorus: kick on every beat, tambourine 8ths, crash on bar 1.

### 80s / synthwave — 110 BPM (100–120)
```
kick    x.......x.......
snare   ....X.......X...    gated reverb
chat    x.x.x.x.x.x.x.x.
toms    ............xxxx    every 8 bars
```
**Beats (per bar):** kick @ b, b+2 (v115) · snare @ b+1, b+3 (v118) · chat 8ths (v70, straight, no swing) · fill bar: toms 47, 45, 44, 44 @ 3.0, 3.25, 3.5, 3.75.

### Disco / nu-disco — 118 BPM (110–125)
```
kick    x...x...x...x...
snare   ....x.......x...
ohat    ..x...x...x...x.
chat    x...x...x...x...
```
**Beats (per bar):** kick @ b, b+1, b+2, b+3 (v112) · snare @ b+1, b+3 (v105) · ohat @ b+0.5, b+1.5, b+2.5, b+3.5 (v90) · chat @ b, b+1, b+2, b+3 (v65).

### R&B (90s slow jam) — 70 BPM (60–75), swing 58–62%
```
kick    x.....x...x.....
snare   ....x.......x...    rimshot or tight snare
snaps   ....x.......x...    layer (use clap 39 at v60)
chat    x.xx.xx.xxx.xx.x    swung 16ths (grid shows unswung positions)
ghost   ..o....o......o.
```
**Beats (per bar):** kick @ b, b+1.5, b+2.5 (v108) · snare 38 @ b+1, b+3 (v100) · clap 39 @ b+1, b+3 (v60, snaps) · chat @ b, b+0.5, b+0.79, b+1.29, b+1.5, b+2, b+2.29, b+2.5, b+3, b+3.29, b+3.79 (v65/45) · ghost snare @ b+0.5, b+1.75, b+3.5 (v38). Contemporary / trap-soul (SZA, Bryson): 70 half-time, trap hats at half speed, snare on 3, 808 slides, snaps.
New jack swing (105, 100–112, 16th swing 60–66%): 808 kick @ b, b+1.5, b+2, b+2.5 · gated snare + clap @ b+1, b+3 · chat swung 16ths with off-beat accents · ohat @ b+1.75, b+3.75 · 808 cowbell 50 or orchestra hit on the "and" of 4.

### Neo-soul — 80 BPM (65–90), drunk feel
```
kick    x......x..x.....
snare   ....x.......x...    +10–30 ms; rim in verses
chat    x.x.x.x.x.x.x.x.    straight (or 56–58%)
ghost   ..o..o....o..o..
```
**Beats (per bar):** kick @ b, b+1.75, b+2.5 (on-grid, or 2–5 ms ≈ 0.005 beat early; v100) · snare @ b+1.02, b+3.03 (v98) · chat @ 8ths straight (v70/50) · ghost snare @ b+0.5, b+1.25, b+2.5, b+3.25 (v35). Don't quantize; `humanize_clip(timing=0.03, velocity=8)`. Optional groove 58–62% on kick/snare only.

### Gospel / shuffle — 90 BPM (70–100), triplet 66%  `[12]`
```
        1..2..3..4..
kick    x....xx.....
snare   ...x.....x..
hat     x.xx.xx.xx.x
```
**Beats (per bar):** kick @ b, b+1.667, b+2 (v110) · snare @ b+1, b+3 (v108) · hat @ b, b+0.667, b+1, b+1.667, b+2, b+2.667, b+3, b+3.667 (v75/55) · clap on 2 & 4 in choruses.

---

## JAZZ / FUNK / LATIN FAMILY

### Jazz swing — 140 BPM (110–200), triplet 66%  `[12]`
```
        1..2..3..4..
ride    x..x.xx..x.x    "spang-a-lang"
hat ft  ...x.....x..    hi-hat foot on 2 & 4
kick    x.....x.....    feathered v35–45
snare   ..o.....x...    comping: sparse, vary each bar
```
**Beats (verified, per bar):** ride 49 @ b, b+1, b+1.667, b+2, b+3, b+3.667 (v80/88/62) · hat 42 @ b+1, b+3 (v55, dur 0.15) · kick 36 @ b, b+2 (v40) · rim 37 / snare 38 comping on "a" positions (b+0.667, b+1.667, b+2.667), 1–2 per bar (v55–70) · "bomb" kick+snare @ 15.667 into the top of a 4-bar form. Brushes: hat/shaker 8ths v40 + snare "sweep" as a long low note. Ballad: ride quarters only, all v−20. Bebop 200+: ride 8ths, bombs every 2 bars.

### Bossa nova — 130 BPM (120–140), straight, soft
```
kick    x.....x.x.....x.    1, "and" of 2, 3, "and" of 4
rim     x..x..x...x..x..    bossa clave
chat    x.x.x.x.x.x.x.x.
```
**Beats (per bar):** kick @ b, b+1.5, b+2, b+3.5 (v70/55) · rim 37 @ b, b+0.75, b+1.5, b+2.5, b+3.25 (v65) · chat/shaker 8ths (v50). Bass = kick pattern on root and 5th.

### Funk — 105 BPM (95–115), 16th syncopation, swing 52–56%
```
kick    x..x..x...x.x...
snare   ..o.X.o..o..X.o.    backbeat + ghosts
chat    x.xx.xx.x.xx.xx.
ohat    .......x.......x    barks on the "a" of 2 and 4
```
**Beats (per bar):** kick @ b, b+0.75, b+1.5, b+2.5, b+3 (v112) · snare @ b+1, b+3 (v115) · ghost snare @ b+0.5, b+1.5, b+2.25, b+3.5 (v40) · chat @ b, b+0.5, b+0.75, b+1.25, b+1.5, b+2, b+2.5, b+2.75, b+3.25, b+3.5 (v65/45) · ohat @ b+1.75, b+3.75 (v90). "Funky Drummer" variant: kick @ b, b+0.75, b+2.5, b+2.75; snare @ b+1, b+3; ghosts @ b+1.5, b+1.75, b+3.5.

### Soul / Motown — 115 BPM (95–130), straight
```
kick    x...x...x...x...
snare   x...x...x...x...    Motown: snare on all four; or 2 & 4
tamb    x.x.x.x.x.x.x.x.
```
**Beats (per bar):** kick @ b, b+1, b+2, b+3 (v105) · snare @ b, b+1, b+2, b+3 (v95; or b+1, b+3 v110) · tambourine (shaker 48) 8ths (v60/45).

### Afrobeats — 105 BPM (98–112), straight, syncopated
```
kick    x.....x.....x...    1, "and" of 2, 4
rim     ...x......x.....    rim/snap on the "a" of 1 and the "and" of 3
shaker  xxxxxxxxxxxxxxxx    16ths, accent the downbeats
perc    ..x..x..x...x..x
```
**Beats (per bar):** kick @ b, b+1.5, b+3 (v108) · rim 37 @ b+0.75, b+2.5 (v85) · shaker 48 16ths (v55, downbeats v65) · conga 41 @ b+0.5, b+1.25, b+2, b+3, b+3.75 (v70). Variant: add rim @ b+1, b+3 for a pop-leaning backbeat.

### Amapiano — 112 BPM (108–115), spacious, shakers 55–60%
```
kick    x.......x.......    1 & 3, soft
clap    ....x.......x...    2 & 4
shaker  xxxxxxxxxxxxxxxx    16ths, never stops
chat    ..x...x...x...x.    offbeat 8ths
log drm .x....x.....x.x.    pitched perc-bass with glides
```
**Beats (per bar):** kick @ b, b+2 (v90, soft) · clap 39 @ b+1, b+3 (v85) · shaker 48 16ths (v55; 2nd/4th 16ths at +0.29) · chat @ b+0.5, b+1.5, b+2.5, b+3.5 (v60) · log drum (bass track, pitch 36–48, root/5th/octave, pitch glides) @ b+0.25, b+1.5, b+3, b+3.5, durations 0.4–0.6, v100. Drop the clap for 16+ bars in intros.

### Reggaeton / dembow — 92 BPM (88–100)
```
kick    x...x...x...x...
snare   ...x..x....x..x.    dembow: 0.75, 1.5, 2.75, 3.5
chat    x.x.x.x.x.x.x.x.
```
**Beats (per bar):** kick @ b, b+1, b+2, b+3 (v115) · snare 38 @ b+0.75, b+1.5, b+2.75, b+3.5 (v105) · chat @ 8ths (v72 on beats 1/3, 65 on 2/4, 55 off — genre override, softer than the global rule) · perreo variant: remove the kick on beat 2 (kick @ b, b+2, b+3). Reggaeton fill (bar 4, beats 3–4): snare @ 14.0, 14.25, 14.5, 14.75, 15.0, 15.5, 15.75 (v70→110), kick @ 15.5.

### Latin clave / tresillo
- Tresillo: 0, 0.75, 1.5 (repeat per 2 beats: +2).
- Son clave 3-2: 0, 0.75, 1.5, 2.5, 3.0 · Rumba clave: 0, 0.75, 1.75, 2.5, 3.0 · 2-3 = swap halves.
- Cascara: 0, 0.5, 1.0, 1.5, 2.0, 2.75, 3.0, 3.5.
- Bossa clave: 0, 0.75, 1.5, 2.5, 3.25 · Cinquillo E(5,8): 0, 0.5, 0.75, 1.25, 1.5 · Tresillo = E(3,8); rotate for variants with `generate_euclidean_drums(pulses, steps, rotate)`.

---

## Fills and turnarounds (bar 4 or 8, beats 3–4 unless noted)
1. Snare 16ths crescendo: 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75 v60→115.
2. Tom walk-down: hi 47 @ 2.5, 2.75 · mid 45 @ 3.0, 3.25 · low 44 @ 3.5, 3.75 · crash on the next 1.
3. Trap hat roll: 32nds on beat 4 (3.0–3.875, 0.125 steps), velocity ramp.
4. Jazz "bomb": kick + snare @ 3.667, crash on 1.
5. House: drop the kick for beat 4 (or all of bar 8), open-hat 16ths, reverse crash into 1.
6. Funk ghost chain: o o o X @ 3.25, 3.5, 3.75, 4.0 (next 1).
7. Pop pickup: snare @ 3.5 + crash on the next 1.
8. Silence: remove everything except one hit on beat 4.

## Variation strategies for bar 2 / 4
Remove one kick · add a ghost snare · move the open hat one 8th · add a single tom · drop hats for a beat · double the snare on the "a" of 4 · shift a kick from 2.5 to 2.75 · swap clap for rim for one bar.
