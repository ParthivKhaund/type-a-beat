# Harmony & Theory Reference

## MIDI numbers and Live's naming
Live labels **C3 = 60** (scientific pitch calls 60 "C4"). Octave step = 12.

| Live name | MIDI | Hz | Use |
|---|---|---|---|
| C0 | 24 | 32.7 | deep 808 / sub floor |
| E0 | 28 | 41.2 | low E of a bass guitar; common 808 root |
| A0 | 33 | 55 | 808 / sub sweet spot upper edge |
| C1 | 36 | 65.4 | kick drum pad in GM/drum racks; bass "low" register |
| C2 | 48 | 130.8 | bass melodic register; low chord tones |
| C3 | 60 | 261.6 | middle C; chord center for comping |
| C4 | 72 | 523 | melody / vocal center |
| C5 | 84 | 1047 | leads, top of melodies |

Pitch classes: C=0 C#/Db=1 D=2 D#/Eb=3 E=4 F=5 F#/Gb=6 G=7 G#/Ab=8 A=9 A#/Bb=10 B=11. MIDI = 12 × (LiveOctave + 2) + pitchClass. Registers: 808/sub 24–33 (C0–A0; 36 = 65 Hz is already the top of sub territory) · bass 28–52 · chords 48–72 · melody 60–84 · leads 67–91.

## Intervals (semitones)
m2 1 · M2 2 · m3 3 · M3 4 · P4 5 · TT 6 · P5 7 · m6 8 · M6 9 · m7 10 · M7 11 · P8 12 · b9 13 · 9 14 · #9 15 · 11 17 · #11 18 · b13 20 · 13 21.

## Scales and modes (intervals from root; mood; where it lives)
| Scale | Steps | Mood | Genres |
|---|---|---|---|
| Major (Ionian) | 0 2 4 5 7 9 11 | bright, resolved | pop, gospel, afrobeats |
| Natural minor (Aeolian) | 0 2 3 5 7 8 10 | sad, serious | trap, house, techno, DnB, pop |
| Harmonic minor | 0 2 3 5 7 8 11 | dramatic, exotic V | trap, drill, cinematic |
| Dorian | 0 2 3 5 7 9 10 | minor but hopeful, funky | neo-soul, funk, house, lo-fi |
| Phrygian | 0 1 3 5 7 8 10 | dark, tense, Spanish | trap, drill, techno |
| Lydian | 0 2 4 6 7 9 11 | dreamy, floating | synthwave, ambient, film |
| Mixolydian | 0 2 4 5 7 9 10 | bluesy major, dominant | funk, soul, rock, jam |
| Locrian | 0 1 3 5 6 8 10 | unstable | rare; metal, tension cues |
| Minor pentatonic | 0 3 5 7 10 | universal riff/melody scale | everything; safe melody default |
| Major pentatonic | 0 2 4 7 9 | happy, folk, afro | pop, afrobeats, amapiano leads |
| Blues | 0 3 5 6 7 10 | gritty | blues, funk, hip-hop leads |
| Bebop dominant | 0 2 4 5 7 9 10 11 | jazz lines land chord tones on beats | jazz solos (`scale="bebop"` in generate_melody) |
| Whole tone | 0 2 4 6 8 10 | dreamy/unsettled | transitions, FX |
| Melodic minor (asc) | 0 2 3 5 7 9 11 | jazz minor, sophisticated | jazz, neo-soul |

Generator scale names accepted by AbletonMCP `generate_melody`: major, minor, dorian, lydian, mixolydian, blues, bebop, minor_pentatonic (plus others fuzzy-matched). `set_song_scale(root, name)` locks Live's scale highlight.

## Chord construction
| Symbol | Formula (semitones) | Notes in C |
|---|---|---|
| C (maj) | 0 4 7 | C E G |
| Cm | 0 3 7 | C Eb G |
| Cdim | 0 3 6 | C Eb Gb |
| Caug | 0 4 8 | C E G# |
| Csus2 / Csus4 | 0 2 7 / 0 5 7 | C D G / C F G |
| Cadd9 | 0 4 7 14 | C E G D |
| C6 / Cm6 | 0 4 7 9 / 0 3 7 9 | C E G A / C Eb G A |
| Cmaj7 | 0 4 7 11 | C E G B |
| C7 (dominant) | 0 4 7 10 | C E G Bb |
| Cm7 | 0 3 7 10 | C Eb G Bb |
| Cm(maj7) | 0 3 7 11 | C Eb G B |
| Cm7b5 (ø, half-dim) | 0 3 6 10 | C Eb Gb Bb |
| Cdim7 (°7) | 0 3 6 9 | C Eb Gb A |
| Cmaj9 / Cm9 / C9 | add 14 | + D |
| C11 / Cm11 | add 14 17 | + D F |
| Cmaj13 / C13 | add 14 (17) 21 | + D (F) A |
| C7#9 ("Hendrix") | 0 4 7 10 15 | C E G Bb D# |
| C7b9 | 0 4 7 10 13 | C E G Bb Db |
| C7alt | 0 4 10 13 15 18 20 | dominant with b9 #9 #11 b13 |
| C7sus4 | 0 5 7 10 | C F G Bb |
| Cmaj7#11 | 0 4 7 11 18 | C E G B F# (Lydian color) |

Progression strings for AbletonMCP generators: dash-, comma-, or space-separated symbols — `"Dm7-G7-Cmaj7"`, qualities supported include maj7, m7, m9, 9, 13, 7#9, sus4, dim, add9.

## Diatonic chords and function
| Degree | Major key | Minor key (natural) | Function |
|---|---|---|---|
| I / i | Imaj7 | im7 | tonic (home) |
| ii / ii° | iim7 | iiø7 | subdominant (pre-dominant) |
| iii / III | iiim7 | IIImaj7 | tonic substitute / relative major |
| IV / iv | IVmaj7 | ivm7 | subdominant |
| V / v | V7 | vm7 (often raised to V7 via harmonic minor) | dominant (tension → I) |
| vi / VI | vim7 | VImaj7 | tonic substitute / relative minor |
| vii° / VII | viiø7 | VII7 | dominant substitute |

Cadences: **authentic** V→I (strongest), **plagal** IV→I (gospel "amen"), **half** anything→V (open), **deceptive** V→vi (surprise, extends a phrase), **backdoor** bVII7→I (soul, jazz).

## Progressions by genre (Roman numerals + a worked key)
| Genre | Progression | Example | Notes |
|---|---|---|---|
| Pop (universal) | I–V–vi–IV | C–G–Am–F | "Axis"; also vi–IV–I–V (Am–F–C–G) darker start |
| Pop / EDM | vi–IV–I–V | Am–F–C–G | build-friendly, loops forever |
| Pop ballad | I–vi–IV–V | C–Am–F–G | 50s doo-wop; sincere |
| 4-chord minor (trap/house/EDM) | i–VI–III–VII | Am–F–C–G in A minor | same notes as pop axis, minor framing |
| Trap dark | i–bVI–bVII–i or i–iv–v | Fm–Db–Eb–Fm; Cm–Fm–Gm | melody in harmonic minor; single-chord bells over 808 common |
| Drill | UK: i–v–VI or i–bII–i · NY: i–iv, i–VI–VII | Cm–Gm–Ab (the classic UK drill loop); Em–Fm–Em | i–bVI–bVII–V7 (Em–C–D–B7) when you want the harmonic-minor lift |
| Lo-fi / jazzy hip-hop | iim7–V7–Imaj7–vim7 | Dm7–G7–Cmaj7–Am7 | swap Imaj7 for Imaj9; add tritone sub Db7 for G7 |
| Boom-bap | i7–iv7 or one sampled loop | Am7–Dm7 | keep it two chords; the drums do the work |
| House / deep house | i7–iv7–v7 (or i–bVII–bVI–bVII) | Am7–Dm7–Em7; Am–G–F–G | stab on the offbeat "and"; 7ths and 9ths |
| Techno | i drone / i–bII | Am pedal; Am–Bb | harmony via filter and texture, not changes |
| Trance / big-room | i–VI–III–VII (breakdown) · VI–VII–i rising into the drop · i–v–VI–VII · vi–IV–I–V | Am–F–C–G; F–G–Am; Am–Em–F–G | 8- or 16-bar holds; add the 9th to almost every chord |
| Future bass | I–V–vi–IV with 9ths/sus | Cadd9–Gsus4–Am7–Fmaj7 | big saw chords, side-chained |
| DnB | i–VI–VII or single-chord Reese | Fm–Db–Eb | liquid: iim7–V7–Imaj7 |
| UK garage | ii–V–I in major or i–iv | Dm7–G7–Cmaj7 | skippy bass on the 2-step |
| R&B (90s) | Imaj7–iiim7–vim7–IVmaj7 | Cmaj7–Em7–Am7–Fmaj7 | 9ths on everything; iiø–V7alt into vi |
| R&B / neo-soul | iim9–V13–Imaj9–VI7#9 | Dm9–G13–Cmaj9–A7#9 | chromatic bass approaches, quartal voicings |
| Neo-soul (Dorian) | i9–IV9 vamp | Dm9–G9 | two-chord vamp, everything in the pocket |
| Gospel | I–IV–I–V with passing dim, 2-5-1 chains | C–F–C–G; C–C#dim–Dm7–G7 | "walk-ups": I–I°/#i°–ii–iii |
| Jazz standard | iim7–V7–Imaj7 (2-5-1) | Dm7–G7–Cmaj7 | the atom of jazz; chain through keys |
| Jazz turnaround | I–vi–ii–V ("rhythm changes" A) | Cmaj7–Am7–Dm7–G7 | substitute iii for I, VI7 for vi |
| Jazz minor | iiø7–V7b9–im7 | Dø7–G7b9–Cm7 | melodic minor over the i |
| Modal jazz | im7 vamp / two-chord | Dm7 (16 bars)–Ebm7 (8)–Dm7 (8) | "So What" AABA; Dorian lines |
| Bossa nova | Imaj7–iim7–V7–Imaj7, ii–V chains, bVI7 | Fmaj7–Gm7–C7; Gm7–C7–Fmaj7–Db7 | chromatic descending bass, 9ths |
| Funk | I7 one-chord vamp, or I7–IV7 | E7#9 vamp; D9–G9 | Dorian/Mixolydian lines; rhythm > harmony |
| Soul / Motown | I–vi–IV–V, I–IV–V, ii–V–I with 7ths | C–Am–F–G | bass plays chord tones + walk-ups |
| Blues (12-bar) | I7 I7 I7 I7 / IV7 IV7 I7 I7 / V7 IV7 I7 V7 | A7 D7 E7 | jazz blues adds ii–V in bars 9–10 |
| Afrobeats | I–V–vi–IV or vi–IV–I–V, pentatonic hooks | C–G–Am–F | keep major; percussion carries |
| Amapiano | i–VI–III–VII or long i–iv holds | Fm–Db–Ab–Eb | log-drum bass answers the chords |
| Reggaeton | i–VI–III–VII or i–bVII–bVI | Am–F–C–G; Am–G–F | 4-chord minor |
| Synthwave | vi–IV–I–V, add Lydian IV | Am–F–C–G; Fmaj7#11 | arpeggiated, 80s pads |
| Ambient | Imaj7–IVmaj7#11 float, or single drone | Cmaj7–Fmaj7#11 | 8–16 bars per chord |

## Color moves
- **Modal interchange (borrowed chords)** in a major key: iv (Fm in C), bVI (Ab), bVII (Bb), bIII (Eb), iiø (Dø7), bII (Db — Neapolitan). In minor: IV major (D in Am), Picardy I major at the end.
- **Secondary dominants**: V7 of any diatonic chord — V7/ii = A7→Dm; V7/V = D7→G; V7/vi = E7→Am.
- **Tritone substitution**: replace V7 with bII7 (G7 → Db7) — same tritone, chromatic bass G→Db→C.
- **Passing diminished**: between I and ii (C–C#°7–Dm7), between ii and iii.
- **Line clichés**: hold a chord, move one voice chromatically (Am–Am(maj7)–Am7–Am6).
- **Pedal point**: keep the bass on I or V while chords change above (EDM builds, gospel).
- **Reharm a melody note**: any melody note can be 3rd, 7th, 9th, 11th, or 13th of a new chord — pick the chord that makes it a color tone.

## Voicings
| Style | Recipe | Use |
|---|---|---|
| Root position triad | 1 3 5 | pop synths, big-room stabs (doubled octaves) |
| Shell | 1 3 7 (or 1 7 3) | jazz/soul piano left hand, house stabs |
| Rootless A (ii–V–I) | 3 5 7 9 → 7 9 3 13 → 3 5 7 9 | jazz comping; bass has the root |
| Rootless B | 7 9 3 5 → 3 13 7 9 → 7 9 3 5 | same, inverted |
| Quartal | stacked 4ths from 3rd or 7th | neo-soul, modal, "So What" chord |
| Drop-2 | take a close 4-note voicing, drop the 2nd-from-top an octave | spread guitar/piano/horn section voicings |
| Spread (open) | 1 – 5 – 3 – 7 across two octaves | pads, orchestral, cinematic |
| Sus / add9 | replace 3 with 2 or 4; stack 9 on top | pop, EDM, worship, future bass |
| Octave + 5th ("power") | 1 5 8 | trap/drill bells, rock |

Range rules: bass alone below ~C2 (48); chord voicings mostly 48–72; avoid m2/M2 clusters below 60; keep the 3rd out of the bass register in low-voiced chords.

**Voice leading**: move each voice the shortest distance; hold common tones; contrary motion between bass and top voice; resolve 7→3 and 3→7 across a ii–V–I; resolve leading tone up, 7th of a dominant down. AbletonMCP's `generate_voiced_progression` does this automatically (rootless/quartal/shell/block styles).

## Bassline writing
| Genre | Rule |
|---|---|
| Trap / drill 808 | Root under each kick, long notes (0.75–2 beats), octave jumps, pitch slides (glide) on the last hit of the bar into the next root; sit on 24–33 |
| House | Root on the offbeat "and" of 1 and 3 (or all offbeats), short notes (0.25–0.4 beat); kick owns the downbeat; sidechain |
| Techno | Rolling 16ths on the root, or offbeat, filtered; a b2 or b7 for tension |
| DnB / dubstep | Reese/sub holds the root for bars; movement via modulation not notes |
| Trance (uplifting) | 16th off-beats (e/&/a of every beat = 12 notes per bar) on the chord root, 1/32 length, mono saw with 5–15 ms glide; classic/progressive = off-beat 8ths |
| Pop / rock | Root on every kick; walk 5→6→b7 into the next chord; octave pops for energy |
| Funk | Syncopated 16ths; hit "the one" hard, then chromatic and octave ghost notes; leave space |
| R&B / neo-soul | Root on 1, then chromatic approaches from a half-step below/above the next root, ghost notes, "drunk" placement 10–30 ms late |
| Jazz walking | Quarter notes: 1 = root, 2 = chord tone, 3 = chord/scale tone, 4 = chromatic or dominant approach to next root; occasional triplet skip (AbletonMCP `generate_walking_bass`) |
| Bossa | Root on 1, 5th on "and of 2" and beat 3 (dotted-quarter feel) |
| Reggaeton / dembow | Root on 1 and the "and of 2", answering the dembow snare |
| Afrobeats / amapiano | Log drum: syncopated root/5th/octave hits landing off the kick, pentatonic |

### Bass note lengths by genre (duration in beats)
Trap/drill 808: 0.75–2 (legato to next hit) · House: 0.25–0.4 · Techno: 0.2–0.25 · DnB/dubstep Reese: 4–8 (hold) · Pop/rock: 0.5–1 · Funk: 0.2–0.5 with rests · R&B/neo-soul: 0.5–1.5 · Jazz walking: 0.9 · Bossa: 0.7–1.2 · Reggaeton: 0.5–0.75 · Afrobeats/amapiano log drum: 0.4–0.6.

## Chord symbol → MIDI worked example
Goal: ii–V–I in Eb major, rootless A voicings, bass below.
1. Scale: Eb major = Eb F G Ab Bb C D (pitch classes 3 5 7 8 10 0 2).
2. Degrees: ii = F → Fm7; V = Bb → Bb7; I = Eb → Ebmaj7. Progression string `"Fm7-Bb7-Ebmaj7"`.
3. Rootless A = 3 5 7 9 → 7 9 3 13 → 3 5 7 9, placed in 55–72:
   - Fm7: Ab C Eb G → **56 60 63 67**
   - Bb7: Ab C D G → **56 60 62 67** (only Eb→D moves: the 7→3 resolution)
   - Ebmaj7: G Bb D F → **55 58 62 65**
4. Bass roots below 48: F **41**, Bb **46**, Eb **39** (or `generate_walking_bass(progression, key="Eb", scale="major", octave=2)`).
5. Live: `generate_voiced_progression(track, 0, "Fm7-Bb7-Ebmaj7", style="rootless", center_pitch=62)` produces equivalent voicings automatically.
General method: pitch class of the root (table above) + interval formula (chord table) → choose the octave so chord tones land 48–72 → MIDI = 12 × (LiveOctave + 2) + pitchClass.

## Melody & hook writing
- Chord tones (1 3 5 7) on strong beats (1 and 3), tensions (9 11 13) on weak beats/off-beats, passing tones between.
- One motif (2–4 notes + rhythm), repeat it with variation: transpose to the next chord, change the last note, invert, augment. Pop hooks repeat every 2 bars; verses vary more.
- Contour: arch (rise then fall) per 4-bar phrase; leaps larger than a 5th resolve by step in the opposite direction.
- Range: keep hooks within an octave; vocal comfort C3–C5 (48–72) male, G3–G5 (55–79) female, sax/lead 55–82.
- Rhythm first: write the rhythm of the hook on one note, then assign pitches.
- Call and response: 2 bars statement, 2 bars answer that ends on a different chord tone.
- Anticipation: start the hook an 8th before the bar (pop/R&B), or lay back after the beat (neo-soul).
- Swing melodies: `generate_melody(swing=0.6–0.66)`; straight for house/trance.

## Key selection tips
- Trap/808: choose the key so the 808 root sits 24–33 (C0–A0 in Live, 33–55 Hz) — F, F#, G, Ab minor put the root at 29–32.
- Vocal songs: pick the key from the singer's comfortable top note for the chorus.
- Sample-based: detect the sample's key (`detect_clip_key`) and build in it or a relative/parallel key.
- Match the existing session: `get_scale_info` / `detect_session_key` before adding parts.

## Time & rhythm quick math (beats, 4/4)
- Straight 8ths at 0, 0.5; swing 8ths at 0, 0.667 (66% triplet); 58% ≈ 0.58; 16ths at 0.25 steps; swing 16ths shift every second 16th late (0.25 → 0.29–0.33).
- Tresillo (3-3-2): hits at 0, 0.75, 1.5 (then repeat at 2). Son clave 3-2: 0, 0.75, 1.5, 2.5, 3.0. Dembow: kick 0, 1, 2, 3; snare 0.75, 1.5, 2.75, 3.5.
- Half-time: snare only on beat 3 (of 4) — 140 BPM trap feels like 70.
- Polymeter: a 3-beat pattern over 4/4 realigns every 12 beats (3 bars).
