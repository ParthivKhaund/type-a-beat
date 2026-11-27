# Sound Selection, Sound Design & Mixing

## Frequency map
| Band | Hz | Lives here | Problem if too much |
|---|---|---|---|
| Sub | 20–60 | 808 fundamental, sub sine | inaudible on phones, eats headroom |
| Bass | 60–250 | kick body (50–100), bass notes, low toms | boomy |
| Low-mid | 250–500 | chord bodies, guitar/keys warmth, snare body (200) | mud (cut 250–400 on non-bass) |
| Mid | 500–2k | vocals, snare crack (1–2k), keys, clav | boxy 300–600, honky 800–1.5k |
| Upper-mid | 2–5k | presence, attack, intelligibility, kick click (3–4k) | harsh 3–4k, fatiguing |
| High | 5–10k | hats, snare snap, sibilance (5–8k) | sizzle, ess |
| Air | 10–20k | shimmer, reverb tails, vocal air | hiss |

Instrument fundamentals: kick 50–100 · 808 30–60 · bass 40–200 · male vocal 100–300 · female vocal 200–500 · piano 27–4k · guitar 80–1.2k · snare 150–250 (body), 2–5k (crack) · hats 3–10k · Rhodes 100–1k body, 2–4k bell.

## Instrument roles (one per slot per section)
| Slot | Role | Typical picks in this library (see `producing-in-ableton/library-catalog.md`) |
|---|---|---|
| Sub / 808 | pitch foundation | Sub 808 Bass, 808 Pure, 808 Drifter |
| Bass | rhythm + root | Upright Bass, synth basses (Sounds/Bass) |
| Kick | pulse | 808 Core Kit, 909 Core Kit, genre kits |
| Chords / pad | harmony, width | E-Piano Rhodish, Grand Piano, Pad/Ambient racks |
| Lead / vocal | melody, focus | Synth Lead racks, Horns Mellow (sax stand-in), Winds flutes |
| Hats / perc | motion, high end | drum kits, Percussive racks, Drum Hits shakers |
| FX / texture | transitions, space | Sounds/Effects, Ambient & Evolving |

## Sound choice by genre
| Genre | Kick | Bass | Chords | Lead | Hats/perc | Space |
|---|---|---|---|---|---|---|
| Trap | 808 long boom + click layer | 808 with glide, distorted | dark bells, pluck, choir pad, minor | flute, bell, vocal chop | crisp closed 808 hats, rolls | short plate on snare, long hall on melody |
| Boom-bap | dusty sampled kick | upright/sampled bass, filtered | sampled Rhodes/soul chops, LP 8–10k | horn/vocal chop | vinyl hats, shakers | room reverb, saturation, vinyl noise |
| Lo-fi | soft, saturated | mellow sub or upright | Rhodes with chorus/wobble, LP | muted trumpet, flute | brushed, low velocity | tape wobble, vinyl, spring |
| House | punchy 909/tight | offbeat synth bass, sub | piano stabs, organ, filtered pad | vocal hook, pluck | 909 open hat, shaker, ride | plate on claps, delay throws |
| Techno | tuned heavy, distorted | rolling mono synth | drone, detuned stab | none/FX | metallic hats, rides | big dark reverb on percs |
| Trance | 909 layered | rolling offbeat saw | supersaw pads/chords, sidechained | supersaw/pluck lead | open hat offbeats | long hall, dotted delay |
| Future bass | punchy w/ tail | sub + sidechain | saw chords with sus/9ths, pitch-wobble LFO | vocal chops, lead saw | sparse | wide reverb |
| DnB | tight punchy | Reese, sub | pads, stabs | vocal, stab | breaks, rides | plate |
| Pop | punchy modern layered | synth/electric bass | piano, guitar, synth pad | vocal | tight hats, claps, tambourine | plate/hall on vocal, slap delay |
| R&B | soft/tight, 808 blend | smooth sub, electric bass | Rhodes, EP, guitar, lush pad | vocal, guitar licks | crisp hats, snaps | lush reverb, wide doubles |
| Neo-soul | soft loose | electric/upright, chromatic | Rhodes with tremolo, Wurli, quartal | Rhodes/guitar/horn | brushed, rims, shakers | room + spring, mono-ish |
| Jazz | acoustic feathered | upright walking | piano rootless, guitar | horn, piano | ride, brushes | small room |
| Funk | tight punchy | slap/fingered electric, synth (Moog) | clav, Rhodes, rhythm guitar | horns, synth lead | tight hats, ohat barks | dry! short plate |
| Afrobeats | soft rounded | log-drum-ish pluck bass | guitar plucks, marimba, pads | vocal, flute | shakers, congas, rim | short reverb, delay on vocal |
| Amapiano | soft | log drum (pitched perc-bass, long decay) | spacious piano/keys, pads | vocal, sax stand-in | shakers, congas | big reverb on keys |
| Reggaeton | punchy 808-style | short sub/808 on 1 and "and" of 2 | dark synth pad, piano stab, nylon guitar | vocal, synth lead, brass stab | tight 808 hats, sparse | short plate on snare, delay on vocal |
| Drill | 808 with click | sliding 808, distorted | dark bells, choir/violin sample, harmonic-minor pad | vocal chop, bell | stuttering 808 hats | dark hall on melody, dry drums |

## Sound design starting points
| Sound | Recipe |
|---|---|
| 808 | Sine/triangle, pitch envelope: +12–24 st decaying in 20–60 ms (the click), amp decay 0.5–2 s, glide 50–120 ms for slides, Saturator drive for harmonics so it reads on phones, tune to the key (root on 24–33). Layer a short punchy kick on top |
| Punchy kick | Short click layer (2–5 kHz) + body (50–80 Hz) + tail; EQ HP at 30 Hz |
| Supersaw | 5–7 saws detuned ±10–25 cents, unison spread, HP 100 Hz, LP 8–12 kHz, chorus, sidechain |
| Pluck | Saw/square, amp decay 200–500 ms, filter env decay ~200 ms, LP cutoff mid, delay dotted-8th |
| Pad | 2 detuned saws or wavetable, slow attack 0.5–2 s, LP with slow LFO, chorus + long reverb, HP 150 Hz |
| Reese | 2 saws detuned ±20 cents, LP 300–800 Hz with subtle LFO, saturation, mono below 120 Hz |
| FM bell | Operator: carrier + modulator ratio 3.5:1 or 7:1, fast decay on mod index, long release |
| Trap bell/keys | Bell or pluck in minor pentatonic, pitch 72–84, wide reverb |
| Rhodes (neo-soul/R&B) | E-Piano preset, tremolo 4–6 Hz or synced 1/8 (Auto Pan device, amount 30–50%), light chorus, drive for bark, LP 8–10 kHz, velocity-sensitive |
| Lo-fi treatment | LP at 6–10 kHz, HP 60 Hz, Saturator drive, subtle pitch wobble (chorus/vibrato), bit reduction, vinyl noise layer, Compressor for pumping |
| Sidechain pump | Compressor on bass/pad, sidechain input = kick, threshold for 6–10 dB GR, ratio 4–8:1, attack fastest. Release: 150–300 ms for a subtle pump, or a full quarter note = 60000 ÷ BPM ms (484 @ 124, 429 @ 140) for the obvious EDM pump; an 8th = ÷ 2 (242 @ 124), a 16th = ÷ 4 |
| Sidechain by genre | Trance bass: 8–12 dB GR, ratio ≥ 4:1, attack 0.1 ms, release 100–140 ms · Future bass: duck the chords hard with a ghost kick on every quarter, even where no kick plays · Trap 808 vs kick: attack 0–1 ms, release 30–80 ms, 3–6 dB GR (or just shorten the kick tail) · House: 6–10 dB GR, release ≈ an 8th |
| Vocal chop | Slice a phrase to 8ths (Simpler slice mode), pitch to key, reverse one slice, formant shift |

## Mixing fundamentals
1. **Gain staging**: average each track around −18 dBFS (peaks −12 to −10); mix bus peaking −6 to −10 dBFS, ~6 dB headroom before mastering. Fader 0.85 = 0 dB in AbletonMCP.
2. **Order**: kick + bass balance first (they define headroom) → drums → chords → lead/vocal → FX. Solo nothing; mix in context.
3. **EQ moves** (cut before boost, 2–3 dB):
   - Kick: HP 30, boost 60–80 body, cut 250–400 mud, boost 3–4k click.
   - 808/sub: HP 25, mono below 120, cut 200–300 if muddy, saturate for 100–300 harmonics.
   - Bass (non-sub): HP 40, cut 250, boost 700–1k for definition; sidechain or EQ notch at kick fundamental.
   - Snare/clap: HP 100, body 200, crack 2–4k, air 8k.
   - Hats: HP 300–500, tame 8k harshness, air 12k.
   - Vocal: HP 80–100, cut 300–500 box, presence 3k, air 10k, de-ess 5–8k.
   - Keys/Rhodes: HP 80–120, cut 300 mud, bell 2–4k gentle.
   - Pads: HP 150–200, LP 10k, carve a hole 1–3k for the vocal.
4. **Compression starting points** (ratio / attack / release / GR):
   - Vocal 3:1 / 10 ms / 50–80 ms / 3–6 dB (plus a second slower comp).
   - Kick 4:1 / 10–20 ms / 150–300 ms or Auto / 3 dB. Snare 4:1 / 5–10 ms / 150–300 ms or Auto / 3–5 dB.
   - Bass 4:1 / 10–30 ms / 100 ms / 3–5 dB (evens the notes).
   - Drum bus (Glue) 4:1 / 10–30 ms (Glue's max; use 30–80 ms on Compressor to keep more transient) / Auto / 2–4 dB. Parallel crush: 10:1, fast, blend 30–50%.
   - Mix bus (Glue) 2:1 / 30 ms / Auto / 1–2 dB.
5. **Space**: reverb and delay on **returns** (`A-Reverb`, `B-Delay` exist). Short plate (0.8–1.2 s) for drums/vocal presence, hall (2–4 s) for pads/leads, pre-delay 20–40 ms keeps vocals forward. Dotted-8th delay on leads, 1/4 on vocals with feedback 20–30%. HP the returns at 200–300 Hz. Liquid DnB: three sends — drums short, music hall, bass LP-filtered — and mute the bass on the last 2 beats of every 16-bar phrase for lift.
6. **Width**: mono below 120 Hz (Utility Bass Mono); widen pads/hats/doubles, keep kick/bass/vocal centered.
7. **Master chain**: EQ (HP 30) → Glue (1–2 dB) → Limiter ceiling −1 dBTP.
8. **Loudness targets** (integrated LUFS): Spotify/YouTube/Tidal −14 (normalized; louder gets turned down), Apple −16, club/festival masters −6 to −8, pop/hip-hop streaming masters −8 to −10, EDM −6 to −9, R&B/neo-soul −10 to −12, jazz/acoustic −12 to −16. True peak ≤ −1 dBTP. `analyze_mix` gives heuristics, not LUFS.

## Mix checklist ("why does it sound weak?")
- Kick and 808/bass fighting → tune 808 to the key, sidechain, or shorten the kick tail; check phase.
- Mud → HP everything that isn't kick/bass at 80–150; cut 250–400 on chords.
- No punch → transients crushed by fast attack; lengthen attack, use parallel compression.
- Flat / lifeless → velocities all equal, no swing, no automation, no contrast between sections.
- Small → no width (doubles, chorus, stereo pads), no low end on phones (add 808 harmonics via saturation).
- Harsh → 2–5k build-up; dynamic EQ on hats/vocals; de-ess.
- Cluttered → two elements in the same slot/register; drop one or move it an octave.
- Drop feels weak → no removal before it, sub missing in the drop, no crash/impact, hook not louder than verse (+1–2 dB).
