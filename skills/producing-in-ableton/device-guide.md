# Native Device Guide (this user's Live: 12.2.5, Intro/Lite edition)

**Edition warning:** `describe_device`/`list_known_devices` return Ableton's general curated knowledge for 9 devices (EQ Eight, Compressor, Glue Compressor, Reverb, Auto Filter, Saturator, Utility, Limiter, Delay) — that list is NOT a check against what's installed. Verified against the live browser (`audio_effects`) on 2026-09-28: **this Live has only 17 Audio Effects, and EQ Eight and Glue Compressor are NOT among them.** Suite devices (Multiband Dynamics, Gate, Drum Buss, Echo, Hybrid Reverb, Roar, Vocoder, Corpus, Resonators, Grain/Filter Delay, Spectral*, etc.), all Max for Live, and every third-party plugin are also absent — see `library-catalog.md` › "NOT available" for the full list. Always cross-check a `describe_device` recommendation against the table below before telling the user to load it.

Units: `db`, `hz`, `ms` are literal; `linear` is 0–1; `curve` is **perceptual, not proportional**. Always call `get_device_parameters(track_index, device_index)` before `set_device_parameter`. Load with `load_instrument_or_effect` using the URI below (all under `query:AudioFx#`).

## Actually-installed Audio Effects (17)
| Device | Role | Key params (unit) | Notes |
|---|---|---|---|
| EQ Three | 3-band EQ/isolator with kill switches | Freq Hi/Mid/Low (hz), Gain Hi/Mid/Low (db), kill buttons | DJ-style tonal shaping; not surgical — use for broad cuts/isolation, not narrow notches |
| Channel EQ | 4-band sweepable EQ (the closer EQ Eight substitute) | HP freq, Low/Mid/High Gain (db) + Freq, Mid Q, HP on/off | **Use this in place of EQ Eight.** 18 presets exist (`Channel EQ` folder). Cut before boost, 2–3 dB moves |
| Compressor | Dynamics + sidechain input | Threshold (db), Ratio, Attack (ms), Release (ms), Dry/Wet | Fast attack kills transients, slow keeps punch. **Use this in place of Glue Compressor** — no vari-ratio "2/4/10" knob, but full manual control covers the same job (ratio ~4:1, attack 10–30 ms, release Auto-equivalent ≈ 150–300 ms, 1–3 dB GR for bus glue). Sidechain: `set_device_routing` input → kick track, fast attack, release ≈ an 8th |
| Reverb | Algorithmic reverb | DecayTime (ms), Room Size (curve), Dry/Wet | Put on a **return** (A-Reverb exists), Dry/Wet 100% there |
| Delay | Tempo-syncable delay | `L 16th` (enum), Feedback (linear), Dry/Wet | Dotted-8th sync is the classic rhythmic delay; B-Delay return exists |
| Auto Filter | Resonant filter + LFO/envelope | Frequency (curve), Resonance (curve) | Slow LP sweep on a pad = motion |
| Saturator | Warmth/distortion | Drive (curve), Dry/Wet | Light drive on drums/bass = analog warmth (lo-fi, hip-hop) |
| Utility | Gain, width, mono, DC | Gain (db), Stereo Width (linear: 0 mono, 100 original, 400 max) | Mono the low end (narrow width) |
| Limiter | Brickwall for master | Gain (db), Ceiling (db) | Ceiling −1 dB; raise Gain for ~2–3 dB peak reduction |
| Audio Effect Rack | Container for chained devices + presets | — | 146 factory rack presets exist (Mixing & Mastering, Modulation & Rhythmic, Performance & DJ, Space, etc.) — see library-catalog.md. **Caution**: some rack presets reference devices absent from this edition (Glue Compressor, Multiband Dynamics, Drum Buss, Cabinet, Overdrive) and may load with a chain device missing — check `get_rack_chains` after loading |
| Auto Shift | Pitch/time correction | — | Has "Tune *" presets — this is the autotune substitute |
| Beat Repeat | Glitch/stutter repeater | Interval, Grid, Chance | Build risers, glitch fills |
| Chorus-Ensemble | Chorus/ensemble widener | Rate, Amount | Widen pads, Rhodes, guitars |
| Erosion | Lo-fi noise/bit texture | Amount, Frequency | Lo-fi and texture work |
| Phaser-Flanger | Phaser/flanger | Rate, Feedback | Movement on leads/guitars |
| Redux | Bit-crush / sample-rate reducer | Bit Depth, Downsample | Lo-fi, 8-bit textures |
| Tuner | Visual pitch tuner | — | Utility, not a processor |

## Common chains (real devices/racks only)
| Goal | Chain |
|---|---|
| Sub/808 bass | Saturator (light) → Channel EQ (HP 25–30 Hz, cut mud 200–400) → Utility (Bass Mono) → Compressor sidechained to kick |
| Drum bus | Compressor (ratio ~4:1, attack 10–30 ms, release ≈150–300 ms, 1–3 dB GR) → Saturator (subtle) |
| Keys / Rhodes | Channel EQ (HP ~80 Hz) → Compressor gentle 2:1 → send to Reverb return |
| Lead / solo voice | Channel EQ (presence 2–5 kHz) → Delay return (dotted 8th, low feedback) → Reverb return |
| Pad | Auto Filter (LP sweep automated) → Chorus-Ensemble → Reverb return (long decay) |
| Vocal chain (fast) | Load the **Vocal Strip** rack (`query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5545`) instead of building by hand — verify its chain with `get_rack_chains` |
| Sidechain pump (fast) | Load the **Ducker** rack (`query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5485`) or a plain Compressor with sidechain routing |
| Master (manual) | Channel EQ (HP 30 Hz) → Compressor (ratio ~2:1, slow attack, release ≈150–300 ms, 1–2 dB GR) → Limiter (ceiling −1 dB) |
| Master (fast) | Load the **Master Full Chain** rack (`query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5527`) or **Master EQ & Compressor** (5525) — verify chain devices after loading |

## Returns already present in the default set
`A-Reverb` (return_index 0) and `B-Delay` (return_index 1). Check with `get_return_tracks` before creating more. Feed with `set_send(track_index, send_index, value)`.

## Instruments actually installed
Only **Drift, Drum Rack, Drum Sampler, Impulse, Instrument Rack, Simpler** (+ 13 Impulse presets). No Operator, Wavetable, Analog, Collision, Electric, Tension, Sampler, or Meld — this is Live Intro/Lite, not Suite. Every "instrument" recommended in `library-catalog.md` best-picks is a Simpler/Sampler-based preset under Sounds/Drums, which is why they load without a Suite license.
