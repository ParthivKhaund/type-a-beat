# Ableton Live Library Catalog
Generated 2026-09-28 from Live 12.2.5 via AbletonMCP. Refresh: re-run the enumeration in this file's header comment when packs/plugins change.

<!--
REFRESH PROCEDURE (read-only, sequential calls only, never parallel — the Live bridge is a single socket):
  get_browser_tree("all")
  get_browser_items_at_path("Sounds") then each subfolder "Sounds/<name>"
  get_browser_items_at_path("Drums"), "Drums/Drum Hits", "Drums/Drum Hits/<sub>"
  get_browser_items_at_path("Instruments"), "Audio Effects", "MIDI Effects", "Max for Live", "Plugins", "Packs", "User Library", "Samples" (+ one level each)
  search_browser(term, max_results=5) for the availability-check terms below
-->

## How to load anything here
load_instrument_or_effect(track_index, uri) — uri column below. In batch_commands the param is `item_uri`.
Top-level browser categories (get_browser_tree): Instruments, Sounds, Drums, Audio Effects, MIDI Effects, Clips, Current_project, Max_for_live, Packs, Plugins, Samples, User_library.
File types: .adg = Instrument/Drum/Effect Rack preset, .adv = single-device preset. Both load with load_instrument_or_effect.
search_browser caveats (learned the hard way): (1) literal substring, so "acoustic guitar" misses "Guitar Acoustic" — search one word; (2) it does NOT search Samples, nor presets nested two folders deep under Audio Effects (e.g. Reverb/Hall/*, Delay/Clean Delay/*, all Audio Effect Rack subfolders) — use the URIs in this file instead; (3) short terms like "arp" match "harp"/"carpet" first and the top-5 cap hides real hits — browse the folder; (4) get_browser_items_at_path needs underscore names for Audio Effects/MIDI Effects/Max for Live/User Library (`audio_effects`, `midi_effects`, `max_for_live`, `user_library`); Sounds/Drums/Instruments/Packs/Plugins/Samples accept plain names.
Fastest correct path for a known thing: copy its URI from this file and call load_instrument_or_effect directly — zero browser calls.

## Best picks by role (by name, unauditioned — refine after listening)
| Role | Pick | URI | Alternates |
|---|---|---|---|
| 808 / sub bass | 808 Pure.adg | query:Sounds#Bass:FileId_5164 | Sub 808 Bass.adv (…Bass:FileId_6515), Hip-Hop Sub Bass.adg (5220), 808 Selector Rack.adg (5165), Basic Sub Sine.adg (5183), Talking 808 Bass.adg (5263) |
| Upright / acoustic bass | Upright Bass.adv | query:Sounds#Bass:FileId_6516 | Electric Bass Soft.adg (5203), Electric Bass Raw.adg (5202) |
| Synth bass | Basic Analog Bass.adg | query:Sounds#Bass:FileId_5170 | Basic Reese Bass.adg (5178), Basic Saw Bass.adg (5180), Mini 3 OSC Bass.adv (6511), Basic 303 Bass.adg (5169), FM Knock Bass.adg (5207) |
| Rhodes / e-piano | E-Piano Rhodish.adg | query:Sounds#Piano%20&%20Keys:FileId_4849 | E-Piano Classic.adg (4841), E-Piano Roads.adg (4850), E-Piano Wurli.adg (4854), FM Piano Classic.adg (4856), E-Piano Light.adg (4846) |
| Grand piano | Grand Piano.adg | query:Sounds#Piano%20&%20Keys:FileId_4857 | Grand Piano Single Sample.adv (6490), Ac Piano Upright.adg (4834), Childhood Home Piano.adg (4835) |
| Organ | Organ Funky.adg | query:Sounds#Piano%20&%20Keys:FileId_4866 | Organ House.adg (4868), Organ Plush.adg (4872), Organ Analog.adg (4862), Organ Bandstand.adg (4864), Organ Dynamic.adg (4865) |
| Pad | Warm Analog Pad.adg | query:Sounds#Pad:FileId_4980 | Basic Saw Pad.adg (4888), Classic Ensemble Pad.adg (4903), Choir Pad Avalon.adg (4897), Drift Pad.adv (6493), Basic Mellow Pad.adg (4887) |
| Lead | Classic Club Saw.adg | query:Sounds#Synth%20Lead:FileId_4593 | Basic OG Lead.adg (4581), Mega Saw.adg (4614), Basic Glide Lead.adg (4580), Sweet Lead.adg (4637), Basic Retro Lead.adg (4583) |
| Pluck | Simple Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4811 | Basic Vintage Pluck.adg (4777), Karplus-Strong Plucks.adg (4794), Glass Pluck.adg (4792), Kyoto Pluck.adg (4796) |
| Brass | Basic Synth Brass.adg | query:Sounds#Brass:FileId_5138 | Some Trumpets.adg (5155), Ac Flugelhorn.adg (5132), Horns Mellow.adg (5144), Poly Synth Brass.adg (5150), Basic Silk Horns.adg (5137) |
| Strings | Ac Strings Orch.adg | query:Sounds#Strings:FileId_4752 | Ac Strings Pizz Basic.adg (4753), String Machine.adg (4766), Basic Jun Strings.adg (4756), MPE Cello Bow.adg (4770) |
| Guitar | Guitar Acoustic.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5053 | Basic Nylon Concerto Guitar.adg (5047), Guitar Electric Clean.adg (5054), Guitar Jazz Muted.adg (5057), Palm Guitar.adg (5063) |
| Mallets | Vibraphone.adg | query:Sounds#Mallets:FileId_5040 | Marimba Concert.adg (5023), Celeste.adg (5009), Basic Bells.adg (5001), Steel Pan.adg (5035) |
| Flute / winds | Basic Synth Flute.adg | query:Sounds#Winds:FileId_4517 | Clay Flute.adg (4518), Indian Flute.adg (4519) — this is the ENTIRE winds section |
| Drum kit: trap / hip-hop | 808 Core Kit.adg | query:Drums#FileId_5409 | BNYX Boot Kit.adg (5355), DECAP DTK 1 Kit.adg (5302), Boom Bap Kit.adg (5292), Late Nite Kit.adg (5381), Street Mind Kit.adg (5341) |
| Drum kit: house / techno | 909 Core Kit.adg | query:Drums#FileId_5410 | AG Techno Kit.adg (5354), Chicago Kit.adg (5362), Garage Kit.adg (5373), Warehouse Stutter Kit.adg (5352), 707 Core Kit.adg (5408) |
| Drum kit: pop | Dry Session Kit.adg | query:Drums#FileId_5419 | Gen Purpose Kit.adg (5420), Golden Kit.adg (5314), Crystal Clear Kit.adg (5300), Plymouth Kit.adg (5425) |
| Drum kit: jazz-ish | Dry Session Kit.adg (+ brush one-shots) | query:Drums#FileId_5419 | Acuff Kit.adg (5416), Heritage Kit.adg (5316), Sticks Kit.adg (5340), Corvaire Kit.adg (5418); brush hits in Drum Hits/Snare, Hihat, Ride |
| Drum kit: lo-fi | LDre Cozy Kit.adg | query:Drums#FileId_5319 | LDre Cafe Kit.adg (5318), LDre Mellow Kit.adg (5320), Lo-Fi Tech Kit.adg (5383), Cardboard Kit.adg (5359), Boom Bap Kit.adg (5292) |
| Percussion | Percussion Core Kit.adg | query:Drums#FileId_5423 | Percussion Spirit Kit.adg (5424), Perc Kitchen Kit.adg (5422), Ahlimba Kit.adg (5417), Conga Bongo Timbales (Impulse: query:Synths#Impulse:FileId_7046) |
| Vocal FX chain | Vocal Strip.adg (rack) | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5545 | Auto Shift → Tune Hard.adv (…Auto%20Shift:FileId_8149), Compressor → De-esser.adv (…Compressor:FileId_8070), Reverb → Vocal Hall.adv (…Reverb:Hall:FileId_7527), Space rack → Adlib Delay.adg (…Space:FileId_5428) |
| Master chain | Master Full Chain.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5527 | Master EQ & Compressor.adg (5525), Master Punchy Dance.adg (5532), Limiter → True Peak Limiter.adv (…Limiter:FileId_7610) |
| Sidechain pump | Ducker.adg (rack) | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5485 | Compressor device (has sidechain input) query:AudioFx#Compressor; Filter Pumper.adg (…Performance%20&%20DJ:FileId_5466) |
(Numbers in parentheses are the FileId within the same URI prefix as the pick.)

## NOT available (searched, absent)
- **Saxophone / sax, trombone, clarinet, oboe, bassoon** — no reed or brass-solo patches other than "Some Trumpets" and "Ac Flugelhorn". Winds = 5 flutes only.
- **Solo violin / viola / orchestral ensemble** — only "Ac Strings Orch" (section rack), pizz variants, and "MPE Cello Bow". "Chord Rotaviolin" is a synth, not a violin.
- **Real vocals / vocal instrument** — no sung/choir multisample instrument. Only 52 one-shot "Vocal *" chops in Samples (not indexed by search_browser) and "Choir Pad" style synth pads.
- **Suite instruments: Operator, Wavetable, Analog, Collision, Electric, Tension, Sampler, Meld** — none exist. Only Drift, Simpler, Drum Sampler, Impulse, Drum Rack, Instrument Rack.
- **Effects: EQ Eight, Glue Compressor, Multiband Dynamics, Gate, Drum Buss, Echo, Hybrid Reverb, Roar, Vocoder, Overdrive, Pedal, Amp, Cabinet, Corpus, Resonators, Grain Delay, Filter Delay, Looper, Spectrum, Vinyl Distortion, Dynamic Tube, Frequency Shifter, Spectral Resonator, Spectral Time, Shifter, Align Delay** — absent. Only the 17 Intro/Lite devices listed under Audio Effects.
- **Max for Live entirely** — no LFO, Envelope Follower, Shaper, CV Tools, Granulator, Drum Synths, Convolution Reverb, etc. (three non-loadable stubs only).
- **MIDI Tools (generators / transformations)** — folder placeholders only.
- **Any third-party plugin** — Plugins category is empty (no VST2/VST3/AU).
- **Any add-on Pack** — only Core Library is installed (no Session Drums, Drum Booth, Orchestral packs, Grand Piano pack, vocal packs, Skitter & Step, etc.).
- **By-name misses that DO have equivalents:** "supersaw" → Mega Saw / Classic Club Saw; "jazz kit" → Dry Session Kit + brush hits; "autotune" → Auto Shift "Tune *"; "sidechain" → Compressor sidechain / Ducker rack; "rhodes" → E-Piano Rhodish; "clavinet" → Clav *; "acoustic guitar" → Guitar Acoustic; "upright piano" → Ac Piano Upright.
- **User Library** — nothing saved (no user presets, samples, clips, grooves, templates).
- Edition inference: instrument + effect sets match **Live 12 Intro / Lite**, not Standard or Suite. Racks whose names reference Glue/Multiband/Drum Buss/Amp/Cabinet may load with missing chain devices — verify after loading.

## Availability check results
(search_browser, all categories, max_results 5. Search is a literal case-insensitive substring on display names; it does NOT index the Samples category or presets nested more than one folder below a device, and word order matters.)
| Term | Found? | Top match | URI |
|---|---|---|---|
| saxophone | NO | — | — |
| sax | NO | — | — |
| trumpet | YES | Some Trumpets.adg | query:Sounds#Brass:FileId_5155 |
| trombone | NO | — | — |
| flugelhorn | YES | Ac Flugelhorn.adg | query:Sounds#Brass:FileId_5132 |
| clarinet | NO | — | — |
| flute | YES (5) | Basic Synth Flute.adg | query:Sounds#Winds:FileId_4517 |
| violin | NO (only "Chord Rotaviolin", a synth-keys preset) | Chord Rotaviolin.adg | query:Sounds#Synth%20Keys:FileId_4684 |
| cello | YES | MPE Cello Bow.adg | query:Sounds#Strings:FileId_4770 |
| strings | YES (5+) | Ac Strings Orch.adg | query:Sounds#Strings:FileId_4752 |
| orchestra | PARTIAL (no ensemble patch; timpani hits + a pad) | MPE Slide Orchestrator.adg | query:Sounds#Pad:FileId_4993 |
| choir | YES (5) | Choir Pad Avalon.adg | query:Sounds#Pad:FileId_4897 |
| vocal | NO via search (search_browser does not index Samples or nested effect presets; "Vocal *" samples and "Vocal Strip" rack DO exist — see Samples / Audio Effects) | Vocal 05.wav | query:Samples#FileId_399 |
| voice | synth only | Voicelike Pad.adg | query:Sounds#Pad:FileId_4978 |
| acoustic guitar | NO literally — word order. "Guitar Acoustic.adg" exists | Guitar Acoustic.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5053 |
| electric guitar | NO literally — word order. "Guitar Electric Clean.adg" exists | Guitar Electric Clean.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5054 |
| nylon | YES | Basic Nylon Concerto Guitar.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5047 |
| grand piano | YES (2) | Grand Piano.adg | query:Sounds#Piano%20&%20Keys:FileId_4857 |
| upright piano | NO literally — word order. "Ac Piano Upright.adg" exists | Ac Piano Upright.adg | query:Sounds#Piano%20&%20Keys:FileId_4834 |
| rhodes | NO literally — library spells it "Rhodish"/"Roads" | E-Piano Rhodish.adg | query:Sounds#Piano%20&%20Keys:FileId_4849 |
| wurli | YES (2) | E-Piano Wurli.adg | query:Sounds#Piano%20&%20Keys:FileId_4854 |
| organ | YES (13 "Organ *" in Piano & Keys) | Organ Incoming.adg / Organ Funky.adg | query:Sounds#Piano%20&%20Keys:FileId_4866 |
| clavinet | NO literally — search "Clav" | Clav Variations.adg | query:Sounds#Piano%20&%20Keys:FileId_4838 |
| harp | YES (3 + Harpsichord) | Harp Concert.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5058 |
| vibraphone | YES (2) | Vibraphone.adg | query:Sounds#Mallets:FileId_5040 |
| marimba | YES (4) | Marimba Concert.adg | query:Sounds#Mallets:FileId_5023 |
| 808 | YES (5 bass racks + 808 Core Kit + many hits) | 808 Core Kit.adg / 808 Pure.adg | query:Drums#FileId_5409 |
| 909 | YES (909 Core Kit + hits) | 909 Core Kit.adg | query:Drums#FileId_5410 |
| 707 | YES (707 Core Kit + hits) | 707 Core Kit.adg | query:Drums#FileId_5408 |
| 606 | YES (606 Core Kit + hits) | 606 Core Kit.adg | query:Drums#FileId_5407 |
| jazz kit | NO (no jazz-named kit; nearest: Dry Session Kit, brush hits, Kick Jazz 8, Kick Solid Jazz) | Dry Session Kit.adg | query:Drums#FileId_5419 |
| brush | YES (brush hihat/ride/snare one-shots; Brushed Bells racks) | Hihat Closed Brush Club Sizzle.aif | query:Drums#Drum%20Hits:Hihat:FileId_2259 |
| ride | YES (69 hits + Analog Ride.adv) | Ride 505.aif | query:Drums#Drum%20Hits:Ride:FileId_1692 |
| hihat | YES (383 hits) | Hihat Closed 2B.aif | query:Drums#Drum%20Hits:Hihat:FileId_2223 |
| clap | YES (111 hits) | Clap 808.aif | query:Drums#Drum%20Hits:Clap:FileId_2943 |
| snare | YES (356 hits + Hyper Snare.adg) | Snare 3k Hiss.wav | query:Drums#Drum%20Hits:Snare:FileId_1166 |
| kick | YES (360 hits + kick-bass racks) | Kick 808 1.aif | query:Drums#Drum%20Hits:Kick:FileId_1877 |
| sub bass | YES (2 + Sub 808 Bass.adv, Basic Sub Sine, Sub * racks) | Hip-Hop Sub Bass.adg | query:Sounds#Bass:FileId_5220 |
| reese | YES (8+) | Basic Reese Bass.adg | query:Sounds#Bass:FileId_5178 |
| pluck | YES (40+ across Guitar & Plucked / Bass) | Simple Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4811 |
| arp | YES — but search "arp" is polluted by "harp"/"carpet"; browse Sounds/Synth Rhythmic (20+ "* Arp") or load MIDI Arpeggiator | Basic Pluck Arp.adg | query:Sounds#Synth%20Rhythmic:FileId_4526 |
| pad | YES (137) | Warm Analog Pad.adg | query:Sounds#Pad:FileId_4980 |
| lead | YES (85) | Classic Club Saw.adg | query:Sounds#Synth%20Lead:FileId_4593 |
| supersaw | NO literally — use Mega Saw / Classic Club Saw / Basic Saw Large | Mega Saw.adg | query:Sounds#Synth%20Lead:FileId_4614 |
| vocoder | NO device (Suite-only) — only "FX Vocoder *" one-shot samples | FX Vocoder Robot.aif | query:Drums#Drum%20Hits:FX%20Hit:FileId_2680 |
| drum rack | YES (device) | Drum Rack | query:Synths#Drum%20Rack |
| operator | NO (Suite-only device, absent) | — | — |
| wavetable | NO (Suite-only device, absent) | — | — |
| analog | presets only ("Analog *" racks); the Analog DEVICE is absent (Suite-only) | Analog Bass.adg | query:Sounds#Bass:FileId_5168 |
| drift | YES (device + presets) | Drift | query:Synths#Drift |
| meld | NO device (Suite-only) — only "MPE Meld Kit.adg" kit name | MPE Meld Kit.adg | query:Drums#FileId_5388 |
| collision | NO (Suite-only device, absent) | — | — |
| electric | presets only (Electric Bass Raw/Soft, Guitar Electric Clean/Muted); the Electric DEVICE is absent (Suite-only) | Electric Bass Soft.adg | query:Sounds#Bass:FileId_5203 |
| tension | NO (Suite-only device, absent) | — | — |
| sampler | only Drum Sampler; the full Sampler device is absent (Suite-only) | Drum Sampler | query:Synths#Drum%20Sampler |
| simpler | YES (device) | Simpler | query:Synths#Simpler |
| roar | NO (device absent) | — | — |
| spectral | NO devices (Spectral Resonator/Time absent); only "Spectral Movement Pad" preset | Spectral Movement Pad.adg | query:Sounds#Pad:FileId_4958 |
| granulator | NO (M4L device, absent) | — | — |
| cv | NO (CV Tools are M4L, absent) | — | — |
| lfo | NO (M4L LFO device absent; note "Formant LFO" Auto Shift presets exist but search does not index nested effect presets) | Formant LFO.adv | query:AudioFx#Auto%20Shift:FileId_8138 |
| sidechain | NO by name — but Compressor & Auto Filter have sidechain inputs, and the "Ducker" rack exists | Ducker.adg | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5485 |
| autotune | NO by name — use Auto Shift "Tune Hard/Gentle/Slow/Smooth" | Tune Hard.adv | query:AudioFx#Auto%20Shift:FileId_8149 |
| pitch | YES (Pitch MIDI device; Auto Shift audio device; "Pitch*" presets) | Pitch | query:MidiFx#Pitch |
| vocal chain | NO by name — build from: Vocal Strip rack + Auto Shift Tune + Compressor De-esser + Reverb Vocal Hall | Vocal Strip.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5545 |


## Sounds
Subfolders (15): Ambient & Evolving, Bass, Brass, Effects, Guitar & Plucked, Mallets, MPE Sounds, Pad, Percussive, Piano & Keys, Strings, Synth Keys, Synth Lead, Synth Rhythmic, Winds.
URI pattern: `query:Sounds#<Folder%20Name>:FileId_NNNN`

### Ambient & Evolving (29 items)
| Name | URI |
|---|---|
| Ambient Swells.adv | query:Sounds#Ambient%20&%20Evolving:FileId_6519 |
| ASMR Cave Texture.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5072 |
| Choiriffic.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5073 |
| Dark Swarm.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5074 |
| Duetta Pad.adv | query:Sounds#Ambient%20&%20Evolving:FileId_6520 |
| Ethereal Tones.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5075 |
| Evolutionary.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5076 |
| Exoplanet Rain.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5077 |
| Interplanetary Trip Pad.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5078 |
| Jarble Ambience.adv | query:Sounds#Ambient%20&%20Evolving:FileId_6521 |
| Lab Ambient.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5079 |
| Mindfulness.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5080 |
| MPE Artic Premonition.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5094 |
| MPE Bower Close.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5095 |
| MPE Dream Grain Drone.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5096 |
| MPE Inside Angel.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5097 |
| MPE Objectivism Drone.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5098 |
| Multitude Of Space.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5081 |
| On A Cold Day.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5082 |
| Organ Incoming.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5083 |
| Over Berlin.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5084 |
| Pitched Ambience.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5085 |
| Play Area.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5086 |
| Seashore Pad.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5087 |
| Shaped Sine.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5088 |
| Sunrise Waves.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5089 |
| Textural Machine.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5090 |
| Tizzy Carpet.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5091 |
| Wave Evolve Pad.adg | query:Sounds#Ambient%20&%20Evolving:FileId_5092 |

### Bass (135 items)
| Name | URI |
|---|---|
| 808 BNYX Stopper.adg | query:Sounds#Bass:FileId_5162 |
| 808 Drifter.adg | query:Sounds#Bass:FileId_5163 |
| 808 Pure.adg | query:Sounds#Bass:FileId_5164 |
| 808 Selector Rack.adg | query:Sounds#Bass:FileId_5165 |
| 808 Slapping.adg | query:Sounds#Bass:FileId_5166 |
| Abel Bass.adg | query:Sounds#Bass:FileId_5167 |
| AG Bass.adv | query:Sounds#Bass:FileId_7162 |
| Airfare Bass.adv | query:Sounds#Bass:FileId_7163 |
| Analog Bass.adg | query:Sounds#Bass:FileId_5168 |
| B Bass.adv | query:Sounds#Bass:FileId_6505 |
| B Seven Bass.adv | query:Sounds#Bass:FileId_6506 |
| Basic 303 Bass.adg | query:Sounds#Bass:FileId_5169 |
| Basic Analog Bass.adg | query:Sounds#Bass:FileId_5170 |
| Basic Electric Drive Bass.adg | query:Sounds#Bass:FileId_5171 |
| Basic Fanatik Bass.adg | query:Sounds#Bass:FileId_5173 |
| Basic Fine Line Bass.adg | query:Sounds#Bass:FileId_5174 |
| Basic FM House Bass.adg | query:Sounds#Bass:FileId_5172 |
| Basic Jupo Bass.adg | query:Sounds#Bass:FileId_5175 |
| Basic Mello Bass.adg | query:Sounds#Bass:FileId_5176 |
| Basic Organ Bass.adg | query:Sounds#Bass:FileId_5177 |
| Basic Reese Bass.adg | query:Sounds#Bass:FileId_5178 |
| Basic Saturated Bass.adg | query:Sounds#Bass:FileId_5179 |
| Basic Saw Bass.adg | query:Sounds#Bass:FileId_5180 |
| Basic Shape Bass.adg | query:Sounds#Bass:FileId_5181 |
| Basic Sub Boom.adg | query:Sounds#Bass:FileId_5182 |
| Basic Sub Sine.adg | query:Sounds#Bass:FileId_5183 |
| Basic Sync Bass.adg | query:Sounds#Bass:FileId_5184 |
| Basic Trigger Bass.adg | query:Sounds#Bass:FileId_5185 |
| Basic Wash Bass.adg | query:Sounds#Bass:FileId_5186 |
| Bit Growl Bass.adv | query:Sounds#Bass:FileId_6507 |
| Bitbass.adg | query:Sounds#Bass:FileId_5187 |
| Blurred Bass.adg | query:Sounds#Bass:FileId_5188 |
| Body Bass.adg | query:Sounds#Bass:FileId_5189 |
| Bonfire Bass.adg | query:Sounds#Bass:FileId_5190 |
| Bounce Bass.adg | query:Sounds#Bass:FileId_5191 |
| Burned Bass.adg | query:Sounds#Bass:FileId_5192 |
| Caustic Bass.adg | query:Sounds#Bass:FileId_5193 |
| Climb The Ladder.adv | query:Sounds#Bass:FileId_7164 |
| Clob Bass.adv | query:Sounds#Bass:FileId_7165 |
| Complex Cletter Bass.adg | query:Sounds#Bass:FileId_5194 |
| Complex Grunge Bass.adg | query:Sounds#Bass:FileId_5195 |
| Complex Gut Kicked Bass.adg | query:Sounds#Bass:FileId_5196 |
| Complex Neurologist Bass.adg | query:Sounds#Bass:FileId_5197 |
| Complex Reese Bass.adg | query:Sounds#Bass:FileId_5198 |
| Corrosive Bass.adg | query:Sounds#Bass:FileId_5199 |
| Dark Bass.adg | query:Sounds#Bass:FileId_5200 |
| Deep Bass.adv | query:Sounds#Bass:FileId_7166 |
| Drive Bass.adg | query:Sounds#Bass:FileId_5201 |
| Dub Techno Bass.adv | query:Sounds#Bass:FileId_7167 |
| Dub Wob Bass.adv | query:Sounds#Bass:FileId_7168 |
| Electric Bass Raw.adg | query:Sounds#Bass:FileId_5202 |
| Electric Bass Soft.adg | query:Sounds#Bass:FileId_5203 |
| Esperienza Bass.adg | query:Sounds#Bass:FileId_5204 |
| Fat Leather Bass.adg | query:Sounds#Bass:FileId_5211 |
| Fat Square Bass.adg | query:Sounds#Bass:FileId_5212 |
| Fifth Bass.adg | query:Sounds#Bass:FileId_5213 |
| Floot Bass.adv | query:Sounds#Bass:FileId_7169 |
| FM Choke Bass.adg | query:Sounds#Bass:FileId_5205 |
| FM Deep Bass.adg | query:Sounds#Bass:FileId_5206 |
| FM Knock Bass.adg | query:Sounds#Bass:FileId_5207 |
| FM Motor City.adg | query:Sounds#Bass:FileId_5208 |
| FM Pluck Bass.adg | query:Sounds#Bass:FileId_5209 |
| FM Space Ball.adg | query:Sounds#Bass:FileId_5210 |
| Formant Bass.adg | query:Sounds#Bass:FileId_5214 |
| Glass Stomper Bass.adg | query:Sounds#Bass:FileId_5215 |
| Go Bass.adg | query:Sounds#Bass:FileId_5216 |
| Grimer Bass.adv | query:Sounds#Bass:FileId_7170 |
| Hammer Bass.adg | query:Sounds#Bass:FileId_5217 |
| Harsh Computer Bass.adg | query:Sounds#Bass:FileId_5218 |
| Hello Bass.adg | query:Sounds#Bass:FileId_5219 |
| Hip-Hop Sub Bass.adg | query:Sounds#Bass:FileId_5220 |
| Humonger Bass.adg | query:Sounds#Bass:FileId_5221 |
| Hybrid Bass.adg | query:Sounds#Bass:FileId_5222 |
| Intense Pluck Bass.adg | query:Sounds#Bass:FileId_5223 |
| Jarble Disto Bass.adg | query:Sounds#Bass:FileId_5224 |
| JX Chorus Bass.adv | query:Sounds#Bass:FileId_6508 |
| Kind Bass.adg | query:Sounds#Bass:FileId_5225 |
| Log Drum.adg | query:Sounds#Bass:FileId_5226 |
| Low Vintage Bass.adg | query:Sounds#Bass:FileId_5227 |
| Malicious Bass.adg | query:Sounds#Bass:FileId_5228 |
| Mini 1 OSC Bass.adv | query:Sounds#Bass:FileId_6509 |
| Mini 2 OSC Solo Bass.adv | query:Sounds#Bass:FileId_6510 |
| Mini 3 OSC Bass.adv | query:Sounds#Bass:FileId_6511 |
| Mini 3 OSC Xectro Bass.adv | query:Sounds#Bass:FileId_6512 |
| Mondo Star Bass.adg | query:Sounds#Bass:FileId_5229 |
| MPE 3rd Major Bass.adg | query:Sounds#Bass:FileId_5272 |
| MPE Ghost Rave Bass.adg | query:Sounds#Bass:FileId_5273 |
| MPE Her Desher Bass.adg | query:Sounds#Bass:FileId_5274 |
| MPE Reese Shape.adg | query:Sounds#Bass:FileId_5275 |
| MPE Reese Throat.adg | query:Sounds#Bass:FileId_5276 |
| MPE Screamer Bass.adg | query:Sounds#Bass:FileId_5277 |
| MPE Source Bass.adg | query:Sounds#Bass:FileId_5278 |
| MPE Subtle Wobble Bass.adg | query:Sounds#Bass:FileId_5279 |
| Muugy Bass.adv | query:Sounds#Bass:FileId_6513 |
| Noise Bass.adg | query:Sounds#Bass:FileId_5230 |
| Not Enough Bass.adv | query:Sounds#Bass:FileId_7171 |
| Ominous Thud.adg | query:Sounds#Bass:FileId_5231 |
| Optimo Time Bass.adg | query:Sounds#Bass:FileId_5232 |
| Overtone Bass.adg | query:Sounds#Bass:FileId_5233 |
| Piano Bass.adv | query:Sounds#Bass:FileId_6514 |
| Pixelated Bass.adg | query:Sounds#Bass:FileId_5234 |
| Plain Bass.adg | query:Sounds#Bass:FileId_5235 |
| Reese Bass Filtered.adg | query:Sounds#Bass:FileId_5236 |
| Reese Classic.adg | query:Sounds#Bass:FileId_5237 |
| Reese Filtered.adg | query:Sounds#Bass:FileId_5238 |
| Reese Odysssey.adg | query:Sounds#Bass:FileId_5239 |
| Ride Pluck Bass.adg | query:Sounds#Bass:FileId_5240 |
| Rose Bass.adg | query:Sounds#Bass:FileId_5241 |
| Round Pluck Bass.adg | query:Sounds#Bass:FileId_5242 |
| Saturated Bass.adg | query:Sounds#Bass:FileId_5243 |
| Screech Lead Bass.adg | query:Sounds#Bass:FileId_5244 |
| Seventy Two Bass.adv | query:Sounds#Bass:FileId_7172 |
| Simpleton Bass.adg | query:Sounds#Bass:FileId_5245 |
| Singularity Bass.adg | query:Sounds#Bass:FileId_5246 |
| Skanker Bass.adg | query:Sounds#Bass:FileId_5247 |
| Sol Bass.adv | query:Sounds#Bass:FileId_7173 |
| Space Session.adg | query:Sounds#Bass:FileId_5248 |
| Static Bass.adg | query:Sounds#Bass:FileId_5249 |
| Stretch Bass.adg | query:Sounds#Bass:FileId_5250 |
| Sub 808 Bass.adv | query:Sounds#Bass:FileId_6515 |
| Sub 808 Pitch Boom.adg | query:Sounds#Bass:FileId_5251 |
| Sub Cave Bass.adg | query:Sounds#Bass:FileId_5252 |
| Sub Drive.adg | query:Sounds#Bass:FileId_5253 |
| Sub L8LY.adg | query:Sounds#Bass:FileId_5254 |
| Sub Mellow.adg | query:Sounds#Bass:FileId_5255 |
| Sub Shaped.adg | query:Sounds#Bass:FileId_5256 |
| Sub Stomach.adg | query:Sounds#Bass:FileId_5257 |
| Sub Sub Bass.adg | query:Sounds#Bass:FileId_5258 |
| Synth Pick Bass.adg | query:Sounds#Bass:FileId_5259 |
| Synth Pluck Bass.adg | query:Sounds#Bass:FileId_5260 |
| Synth Pop Bass.adg | query:Sounds#Bass:FileId_5261 |
| Synthetic Kick Bass.adg | query:Sounds#Bass:FileId_5262 |
| Talking 808 Bass.adg | query:Sounds#Bass:FileId_5263 |
| The Beat Of History.adg | query:Sounds#Bass:FileId_5264 |
| Thermal Runway Bass.adg | query:Sounds#Bass:FileId_5265 |
| Thick Bass.adg | query:Sounds#Bass:FileId_5266 |
| Throat Bass.adg | query:Sounds#Bass:FileId_5267 |
| Tubular Bass.adg | query:Sounds#Bass:FileId_5268 |
| Upright Bass.adv | query:Sounds#Bass:FileId_6516 |
| Vintage Chorus Bass.adv | query:Sounds#Bass:FileId_7174 |
| Womp Bass.adg | query:Sounds#Bass:FileId_5269 |
| Wonk Bass.adv | query:Sounds#Bass:FileId_6517 |
| Wub Bass.adg | query:Sounds#Bass:FileId_5270 |

### Brass (30 items)
| Name | URI |
|---|---|
| Ac Flugelhorn.adg | query:Sounds#Brass:FileId_5132 |
| Alpha Brass Affair.adg | query:Sounds#Brass:FileId_5133 |
| Analog Jungle.adg | query:Sounds#Brass:FileId_5134 |
| Analog Sparkle.adg | query:Sounds#Brass:FileId_5135 |
| Basic FM Brass.adg | query:Sounds#Brass:FileId_5136 |
| Basic Silk Horns.adg | query:Sounds#Brass:FileId_5137 |
| Basic Synth Brass.adg | query:Sounds#Brass:FileId_5138 |
| Block Minor Brass.adg | query:Sounds#Brass:FileId_5139 |
| Chord Analog Brass.adg | query:Sounds#Brass:FileId_5140 |
| Drop Brass.adg | query:Sounds#Brass:FileId_5141 |
| Duality Brass.adg | query:Sounds#Brass:FileId_5142 |
| Four Brass.adg | query:Sounds#Brass:FileId_5143 |
| Horns Mellow.adg | query:Sounds#Brass:FileId_5144 |
| Instant Parade.adg | query:Sounds#Brass:FileId_5145 |
| Meneo Velo.adg | query:Sounds#Brass:FileId_5146 |
| Moody Fanfare.adg | query:Sounds#Brass:FileId_5147 |
| MPE Luna Dreaming.adg | query:Sounds#Brass:FileId_5160 |
| Neo Jab.adg | query:Sounds#Brass:FileId_5148 |
| Plate Stab.adg | query:Sounds#Brass:FileId_5149 |
| Poly Synth Brass.adg | query:Sounds#Brass:FileId_5150 |
| Prime Brass.adv | query:Sounds#Brass:FileId_7159 |
| Quadra Brass.adg | query:Sounds#Brass:FileId_5151 |
| Retro Deluxe.adg | query:Sounds#Brass:FileId_5152 |
| Slider Brass.adg | query:Sounds#Brass:FileId_5153 |
| Soft Stereo Brass.adg | query:Sounds#Brass:FileId_5154 |
| Some Trumpets.adg | query:Sounds#Brass:FileId_5155 |
| Swell Brass.adg | query:Sounds#Brass:FileId_5156 |
| Transilvania Brass.adg | query:Sounds#Brass:FileId_5157 |
| Vanguard Brass.adv | query:Sounds#Brass:FileId_7160 |
| Woozy Brass.adg | query:Sounds#Brass:FileId_5158 |

### Effects (38 items)
| Name | URI |
|---|---|
| Bleeps Don't Lie.adg | query:Sounds#Effects:FileId_5100 |
| Broadcast Noise.adg | query:Sounds#Effects:FileId_5101 |
| Chimes Finger Down.adv | query:Sounds#Effects:FileId_6499 |
| Chopped Robot.adg | query:Sounds#Effects:FileId_5102 |
| Complex Zipper FX.adg | query:Sounds#Effects:FileId_5103 |
| Dead City FX.adg | query:Sounds#Effects:FileId_5104 |
| Detune Tune.adg | query:Sounds#Effects:FileId_5105 |
| Dropping Vehicle.adg | query:Sounds#Effects:FileId_5106 |
| Dub Siren.adg | query:Sounds#Effects:FileId_5107 |
| ENCOM Riser.adg | query:Sounds#Effects:FileId_5108 |
| Gear Shift.adv | query:Sounds#Effects:FileId_7155 |
| Glowstick SFX.adg | query:Sounds#Effects:FileId_5109 |
| Hoover.adg | query:Sounds#Effects:FileId_5110 |
| Hyper Riser.adg | query:Sounds#Effects:FileId_5111 |
| Low Expansion.adg | query:Sounds#Effects:FileId_5112 |
| Metallo Shake.adv | query:Sounds#Effects:FileId_6500 |
| MPE Alder Waldgeist.adg | query:Sounds#Effects:FileId_5127 |
| MPE Sci-Fi Flicks.adg | query:Sounds#Effects:FileId_5128 |
| MPE Slide Swarmer.adg | query:Sounds#Effects:FileId_5129 |
| MPE Thunder Drum.adg | query:Sounds#Effects:FileId_5130 |
| Ominous Signal.adg | query:Sounds#Effects:FileId_5113 |
| Passing By.adv | query:Sounds#Effects:FileId_7156 |
| Rain On The Servers.adg | query:Sounds#Effects:FileId_5114 |
| Rainstorm.adg | query:Sounds#Effects:FileId_5115 |
| Rave Signal.adg | query:Sounds#Effects:FileId_5116 |
| Rhyt Mo.adv | query:Sounds#Effects:FileId_6501 |
| Riser Arcade.adg | query:Sounds#Effects:FileId_5117 |
| Riser Basic.adg | query:Sounds#Effects:FileId_5118 |
| Riser Crisis.adg | query:Sounds#Effects:FileId_5119 |
| Rusty Spacecraft.adg | query:Sounds#Effects:FileId_5120 |
| Siren Stutter.adg | query:Sounds#Effects:FileId_5121 |
| Sloppy Kicker.adg | query:Sounds#Effects:FileId_5122 |
| Start Me Up.adg | query:Sounds#Effects:FileId_5123 |
| Supersine.adv | query:Sounds#Effects:FileId_6502 |
| Synth Vox Ai.adg | query:Sounds#Effects:FileId_5124 |
| Toy Helicopter.adv | query:Sounds#Effects:FileId_7157 |
| Vinyl Rub.adg | query:Sounds#Effects:FileId_5125 |
| Vinyl Siren.adv | query:Sounds#Effects:FileId_6503 |

### Guitar & Plucked (82 items)
| Name | URI |
|---|---|
| Atmo Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4774 |
| Axe Of Velvet.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4775 |
| Basic Flange Harp.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5045 |
| Basic Guzheng.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5046 |
| Basic Nylon Concerto Guitar.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5047 |
| Basic Radar Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4776 |
| Basic Shamisen.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5048 |
| Basic Vintage Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4777 |
| Berimbau.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5049 |
| Big Floor Stab.adv | query:Sounds#Guitar%20&%20Plucked:FileId_7108 |
| Bridge Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4778 |
| Chirp Pluck.adv | query:Sounds#Guitar%20&%20Plucked:FileId_7109 |
| Chord Cold Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4779 |
| Chord Dub Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4780 |
| Chord Key Stabs.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4781 |
| Chord Minor Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4782 |
| Classic Fifth Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4783 |
| Condo.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4784 |
| Deep Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4785 |
| Dobro.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5050 |
| Drippy Cave Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4786 |
| Drubb Stabs.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4787 |
| Falter Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4789 |
| Floomery Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4790 |
| FM Four Pluck.adv | query:Sounds#Guitar%20&%20Plucked:FileId_7110 |
| FM Pluck Guitar.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4788 |
| Generation Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4791 |
| Glacial Tolerance.adv | query:Sounds#Guitar%20&%20Plucked:FileId_7111 |
| Glass Guitar.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5051 |
| Glass Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4792 |
| Guit Layter.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5052 |
| Guitar Acoustic.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5053 |
| Guitar Electric Clean.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5054 |
| Guitar Electric Muted.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5055 |
| Guitar Jazz Cmaj7.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5056 |
| Guitar Jazz Muted.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5057 |
| Harp Concert.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5058 |
| House Stab.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4793 |
| Ionosphere Guitar.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5059 |
| Kanun.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5060 |
| Karplus-Strong Plucks.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4794 |
| Kyoto Guitar.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4795 |
| Kyoto Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4796 |
| Lift Delay Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4797 |
| Lost in Plucks.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4798 |
| Lyre Albany.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5061 |
| Membrane Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4799 |
| Metallic Noise Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4800 |
| Miami Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4801 |
| Mod Amp Sine Bleep.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4802 |
| Mouse Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4803 |
| Multi Saw Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4804 |
| Mutation Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4805 |
| Ocean Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4806 |
| Oscillation Guitar.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5062 |
| Palm Guitar.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5063 |
| Perc Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4807 |
| Point Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4808 |
| Powder Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4809 |
| Shimmer Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4810 |
| Simple Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4811 |
| Sitar.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5064 |
| Snappy Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4812 |
| Soft Attention.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4813 |
| Sponge House.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4814 |
| Square Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4815 |
| Stab Big Room.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4816 |
| Stab Dense.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4817 |
| Stab Ibiza.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4818 |
| Stab Proga.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4819 |
| Stadium Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4820 |
| Strum-o-Matic.adg | query:Sounds#Guitar%20&%20Plucked:FileId_5065 |
| Subtle Look Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4821 |
| Synth Harp.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4822 |
| Synth Koto.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4823 |
| Thumb Piano Tiny.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4824 |
| Trinidad Plucks.adv | query:Sounds#Guitar%20&%20Plucked:FileId_7112 |
| Tube Lead Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4825 |
| Vector Connector.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4826 |
| Water Pluck.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4827 |
| With Twelve.adg | query:Sounds#Guitar%20&%20Plucked:FileId_4828 |
| Zonk Pluck.adv | query:Sounds#Guitar%20&%20Plucked:FileId_7113 |

### Mallets (55 items)
| Name | URI |
|---|---|
| Ambient Computer Bell.adg | query:Sounds#Mallets:FileId_4997 |
| Analog Chime.adg | query:Sounds#Mallets:FileId_4998 |
| Balsam Gamelan.adg | query:Sounds#Mallets:FileId_4999 |
| Basic Analog Chime.adg | query:Sounds#Mallets:FileId_5000 |
| Basic Bells.adg | query:Sounds#Mallets:FileId_5001 |
| Basic Bright Marimba.adg | query:Sounds#Mallets:FileId_5002 |
| Basic Brushed Bells.adg | query:Sounds#Mallets:FileId_5003 |
| Basic FM Bells.adg | query:Sounds#Mallets:FileId_5004 |
| Basic Mallet.adg | query:Sounds#Mallets:FileId_5005 |
| Bell and Swell.adg | query:Sounds#Mallets:FileId_5008 |
| Bell Away.adg | query:Sounds#Mallets:FileId_5006 |
| Bell Variations.adg | query:Sounds#Mallets:FileId_5007 |
| Bell Wave.adv | query:Sounds#Mallets:FileId_7145 |
| Celeste.adg | query:Sounds#Mallets:FileId_5009 |
| Ceramic Bowl.adg | query:Sounds#Mallets:FileId_5010 |
| Ceramic Tiles.adg | query:Sounds#Mallets:FileId_5011 |
| Church Bell.adv | query:Sounds#Mallets:FileId_7146 |
| Corrosion Bells.adg | query:Sounds#Mallets:FileId_5012 |
| Cycle Chimes.adg | query:Sounds#Mallets:FileId_5013 |
| Digi Bells.adg | query:Sounds#Mallets:FileId_5014 |
| Dusty Bells.adg | query:Sounds#Mallets:FileId_5015 |
| Echo Bells.adv | query:Sounds#Mallets:FileId_7147 |
| Ethereal Brushed Bells.adg | query:Sounds#Mallets:FileId_5016 |
| Fake Phone.adg | query:Sounds#Mallets:FileId_5017 |
| Faux Microtonal Glass Mallet.adg | query:Sounds#Mallets:FileId_5018 |
| Fear Gong.adg | query:Sounds#Mallets:FileId_5019 |
| Gritty Bells.adg | query:Sounds#Mallets:FileId_5020 |
| Hickory Bells.adv | query:Sounds#Mallets:FileId_7148 |
| Island Bells.adg | query:Sounds#Mallets:FileId_5021 |
| Island Pans.adg | query:Sounds#Mallets:FileId_5022 |
| Majestic FM Bells.adv | query:Sounds#Mallets:FileId_7149 |
| Marimba Concert.adg | query:Sounds#Mallets:FileId_5023 |
| Marimba Maple.adg | query:Sounds#Mallets:FileId_5024 |
| Mellow Bells.adg | query:Sounds#Mallets:FileId_5025 |
| Metropolis Bells.adg | query:Sounds#Mallets:FileId_5026 |
| MPE Misty Bells.adg | query:Sounds#Mallets:FileId_5043 |
| Nostalgic VHS Bells.adg | query:Sounds#Mallets:FileId_5027 |
| Obelisk Bells.adg | query:Sounds#Mallets:FileId_5028 |
| Orbit Mallets.adg | query:Sounds#Mallets:FileId_5029 |
| Outland Bells.adg | query:Sounds#Mallets:FileId_5030 |
| Plastic Toy.adg | query:Sounds#Mallets:FileId_5031 |
| Product Bells.adg | query:Sounds#Mallets:FileId_5032 |
| Queen Pans.adg | query:Sounds#Mallets:FileId_5033 |
| Ranger Bells.adv | query:Sounds#Mallets:FileId_7150 |
| Rubber Bell.adv | query:Sounds#Mallets:FileId_7151 |
| Spetses Bell.adg | query:Sounds#Mallets:FileId_5034 |
| Steel Pan.adg | query:Sounds#Mallets:FileId_5035 |
| Summer Time.adg | query:Sounds#Mallets:FileId_5036 |
| Sunken Bells.adg | query:Sounds#Mallets:FileId_5037 |
| Synthetic Xylophone.adv | query:Sounds#Mallets:FileId_7152 |
| Tin Bell.adg | query:Sounds#Mallets:FileId_5038 |
| Toy Xylophone.adv | query:Sounds#Mallets:FileId_7153 |
| Tubular FM Bells.adg | query:Sounds#Mallets:FileId_5039 |
| Vibraphone.adg | query:Sounds#Mallets:FileId_5040 |
| Water Bells.adg | query:Sounds#Mallets:FileId_5041 |

### MPE Sounds (58 items) — aggregates every MPE-* preset from the other folders (same FileIds). Unique-to-this-listing entries marked *.
| Name | URI |
|---|---|
| MPE 3rd Major Bass.adg | query:Sounds#MPE%20Sounds:FileId_5272 |
| MPE Airy Pad & Sub.adg | query:Sounds#MPE%20Sounds:FileId_4984 |
| MPE Alder Waldgeist.adg | query:Sounds#MPE%20Sounds:FileId_5127 |
| MPE Artic Premonition.adg | query:Sounds#MPE%20Sounds:FileId_5094 |
| MPE Bower Close.adg | query:Sounds#MPE%20Sounds:FileId_5095 |
| MPE Cello Bow.adg (Strings) | query:Sounds#MPE%20Sounds:FileId_4770 |
| MPE Con Amore Pad.adg | query:Sounds#MPE%20Sounds:FileId_4985 |
| MPE Creep Pluck.adg | query:Sounds#MPE%20Sounds:FileId_4830 |
| MPE Dark Cinema Pad.adg | query:Sounds#MPE%20Sounds:FileId_4986 |
| MPE Depth Pressure Pad.adg | query:Sounds#MPE%20Sounds:FileId_4987 |
| MPE Dream Grain Drone.adg | query:Sounds#MPE%20Sounds:FileId_5096 |
| MPE Dub String.adg | query:Sounds#MPE%20Sounds:FileId_5067 |
| MPE Dulcimatica.adg | query:Sounds#MPE%20Sounds:FileId_5068 |
| MPE Dusty Memory Organette.adg | query:Sounds#MPE%20Sounds:FileId_4741 |
| MPE Evil Underneath.adg | query:Sounds#MPE%20Sounds:FileId_4742 |
| MPE Faulty Wurli.adg | query:Sounds#MPE%20Sounds:FileId_4744 |
| MPE FM Arp.adg | query:Sounds#MPE%20Sounds:FileId_4570 |
| MPE FM Land.adg | query:Sounds#MPE%20Sounds:FileId_4743 |
| MPE Ghost Choir Pad.adg | query:Sounds#MPE%20Sounds:FileId_4988 |
| MPE Ghost Rave Bass.adg | query:Sounds#MPE%20Sounds:FileId_5273 |
| MPE Ghost Ship Pad.adg | query:Sounds#MPE%20Sounds:FileId_4989 |
| MPE Glorious Chord.adg | query:Sounds#MPE%20Sounds:FileId_4745 |
| MPE Gravity.adg | query:Sounds#MPE%20Sounds:FileId_4990 |
| MPE Her Desher Bass.adg | query:Sounds#MPE%20Sounds:FileId_5274 |
| MPE Inside Angel.adg | query:Sounds#MPE%20Sounds:FileId_5097 |
| MPE Level Ives Pad.adg | query:Sounds#MPE%20Sounds:FileId_4571 |
| MPE Luna Dreaming.adg | query:Sounds#MPE%20Sounds:FileId_5160 |
| MPE Mahogany Rose Organ.adg | query:Sounds#MPE%20Sounds:FileId_4746 |
| MPE Metallic Keys.adg | query:Sounds#MPE%20Sounds:FileId_4572 |
| MPE Misty Bells.adg | query:Sounds#MPE%20Sounds:FileId_5043 |
| MPE Monomorph.adg | query:Sounds#MPE%20Sounds:FileId_4747 |
| MPE Mountain Guitar.adg | query:Sounds#MPE%20Sounds:FileId_5069 |
| MPE Objectivism Drone.adg | query:Sounds#MPE%20Sounds:FileId_5098 |
| MPE Pearlescent Tides Pad.adg | query:Sounds#MPE%20Sounds:FileId_4991 |
| MPE Polypulse Pressure.adg | query:Sounds#MPE%20Sounds:FileId_4573 |
| MPE Power Plant Pad.adg | query:Sounds#MPE%20Sounds:FileId_4992 |
| MPE Reese Shape.adg | query:Sounds#MPE%20Sounds:FileId_5275 |
| MPE Reese Throat.adg | query:Sounds#MPE%20Sounds:FileId_5276 |
| MPE Sci-Fi Flicks.adg | query:Sounds#MPE%20Sounds:FileId_5128 |
| MPE Screamer Bass.adg | query:Sounds#MPE%20Sounds:FileId_5277 |
| MPE Sine Pressure.adg | query:Sounds#MPE%20Sounds:FileId_4748 |
| MPE Single Coil Thumb.adg | query:Sounds#MPE%20Sounds:FileId_5070 |
| MPE Slide Orchestrator.adg | query:Sounds#MPE%20Sounds:FileId_4993 |
| MPE Slide Pluck FM.adg | query:Sounds#MPE%20Sounds:FileId_4831 |
| MPE Slide Swarmer.adg | query:Sounds#MPE%20Sounds:FileId_5129 |
| MPE Smeary Plucks.adg | query:Sounds#MPE%20Sounds:FileId_4832 |
| MPE Source Bass.adg | query:Sounds#MPE%20Sounds:FileId_5278 |
| MPE Spieluhr.adg | query:Sounds#MPE%20Sounds:FileId_4574 |
| MPE Standup Lead.adg | query:Sounds#MPE%20Sounds:FileId_4650 |
| MPE Subtle Wobble Bass.adg | query:Sounds#MPE%20Sounds:FileId_5279 |
| MPE Synth Bow.adg | query:Sounds#MPE%20Sounds:FileId_4771 |
| MPE Synth Pipe Organ.adg | query:Sounds#MPE%20Sounds:FileId_4749 |
| MPE Thunder Drum.adg | query:Sounds#MPE%20Sounds:FileId_5130 |
| MPE Toxic Lead.adg | query:Sounds#MPE%20Sounds:FileId_4651 |
| MPE Velocity Grain.adg | query:Sounds#MPE%20Sounds:FileId_4750 |
| MPE Velvet Robe.adg | query:Sounds#MPE%20Sounds:FileId_4994 |
| MPE Warping Strings.adg | query:Sounds#MPE%20Sounds:FileId_4772 |
| MPE Windwhistle Pad.adg | query:Sounds#MPE%20Sounds:FileId_4995 |

### Pad (137 items)
| Name | URI |
|---|---|
| Abilene Winter Pad.adg | query:Sounds#Pad:FileId_4881 |
| After Glow Pad.adg | query:Sounds#Pad:FileId_4882 |
| Airport Pad.adg | query:Sounds#Pad:FileId_4883 |
| Awakening Pad.adg | query:Sounds#Pad:FileId_4884 |
| Basic Brass Pad.adg | query:Sounds#Pad:FileId_4885 |
| Basic Digi Pad.adg | query:Sounds#Pad:FileId_4886 |
| Basic Mellow Pad.adg | query:Sounds#Pad:FileId_4887 |
| Basic Saw Pad.adg | query:Sounds#Pad:FileId_4888 |
| Bell Pad.adg | query:Sounds#Pad:FileId_4889 |
| Bloom Pad.adv | query:Sounds#Pad:FileId_7128 |
| Boxed Pad.adg | query:Sounds#Pad:FileId_4890 |
| Bronto Pad.adg | query:Sounds#Pad:FileId_4891 |
| Casino Blips Pad.adg | query:Sounds#Pad:FileId_4892 |
| Cave Talkers Pad.adg | query:Sounds#Pad:FileId_4893 |
| Celestial Pad.adg | query:Sounds#Pad:FileId_4894 |
| Chimes and Bow Pad.adg | query:Sounds#Pad:FileId_4895 |
| Chip Breeze.adg | query:Sounds#Pad:FileId_4896 |
| Choir Pad Avalon.adg | query:Sounds#Pad:FileId_4897 |
| Chord Anthem Pad.adg | query:Sounds#Pad:FileId_4898 |
| Chord Eno Pad.adg | query:Sounds#Pad:FileId_4899 |
| Chord Float Pad.adg | query:Sounds#Pad:FileId_4900 |
| Chord Floot Aboot Pad.adv | query:Sounds#Pad:FileId_6492 |
| Chord Pacific Pad.adg | query:Sounds#Pad:FileId_4901 |
| Chord Rave Pad.adg | query:Sounds#Pad:FileId_4902 |
| Classic Ensemble Pad.adg | query:Sounds#Pad:FileId_4903 |
| Coffee Leaf.adg | query:Sounds#Pad:FileId_4904 |
| Complex Amp Pad.adg | query:Sounds#Pad:FileId_4905 |
| Covalent Theorem Pad.adg | query:Sounds#Pad:FileId_4906 |
| Dark Corner Pad.adg | query:Sounds#Pad:FileId_4907 |
| Dark Poly Pad.adg | query:Sounds#Pad:FileId_4908 |
| Dark Swell Pad.adg | query:Sounds#Pad:FileId_4909 |
| Daysleeper Swells Pad.adg | query:Sounds#Pad:FileId_4910 |
| Detuned Square.adg | query:Sounds#Pad:FileId_4911 |
| Digi Noise Choir.adg | query:Sounds#Pad:FileId_4912 |
| Dojo Sky Pad.adg | query:Sounds#Pad:FileId_4913 |
| Drapes Pad.adg | query:Sounds#Pad:FileId_4914 |
| Dreamlike Motif Bells.adg | query:Sounds#Pad:FileId_4915 |
| Drift Pad.adv | query:Sounds#Pad:FileId_6493 |
| Dub Striker.adg | query:Sounds#Pad:FileId_4916 |
| Dunkel Pad.adg | query:Sounds#Pad:FileId_4917 |
| Echo Moved Pad.adg | query:Sounds#Pad:FileId_4918 |
| Echo Pad.adg | query:Sounds#Pad:FileId_4919 |
| Flutter Pad.adg | query:Sounds#Pad:FileId_4921 |
| Flutter Pad.adv | query:Sounds#Pad:FileId_7129 |
| FM Cassini Pad.adg | query:Sounds#Pad:FileId_4920 |
| Foglie Pad.adv | query:Sounds#Pad:FileId_7130 |
| Format World.adg | query:Sounds#Pad:FileId_4922 |
| Freudian Pad.adg | query:Sounds#Pad:FileId_4923 |
| Frozen Rings Pad.adg | query:Sounds#Pad:FileId_4924 |
| Gentle Pulse Pad.adv | query:Sounds#Pad:FileId_7131 |
| Goddess Flight Pad.adg | query:Sounds#Pad:FileId_4925 |
| Hallowed Pad.adg | query:Sounds#Pad:FileId_4926 |
| Haven Pad.adg | query:Sounds#Pad:FileId_4927 |
| Hera Pad.adg | query:Sounds#Pad:FileId_4928 |
| Hit Slide Pad.adg | query:Sounds#Pad:FileId_4929 |
| Inclement Drone Pad.adg | query:Sounds#Pad:FileId_4930 |
| Ion Afterburn Pad.adg | query:Sounds#Pad:FileId_4931 |
| Jarble Ambience Pad.adv | query:Sounds#Pad:FileId_6494 |
| Ladybird Pad.adg | query:Sounds#Pad:FileId_4932 |
| Light Frost.adv | query:Sounds#Pad:FileId_7132 |
| Lo-Fi Reso Pad.adg | query:Sounds#Pad:FileId_4933 |
| Marble Pad.adg | query:Sounds#Pad:FileId_4934 |
| Mello Patience.adg | query:Sounds#Pad:FileId_4935 |
| Metal Pad.adg | query:Sounds#Pad:FileId_4936 |
| Metallic Flutter Pad.adv | query:Sounds#Pad:FileId_7133 |
| Metallic Swell Pad.adv | query:Sounds#Pad:FileId_7134 |
| Mindgrowth.adg | query:Sounds#Pad:FileId_4937 |
| Modular Organ Pad.adv | query:Sounds#Pad:FileId_6495 |
| Monday Morning.adv | query:Sounds#Pad:FileId_7135 |
| Morning Chorus Pad.adv | query:Sounds#Pad:FileId_7136 |
| Mourning Stories Pad.adg | query:Sounds#Pad:FileId_4938 |
| Moving Pictures Pad.adg | query:Sounds#Pad:FileId_4939 |
| MPE Airy Pad & Sub.adg | query:Sounds#Pad:FileId_4984 |
| MPE Con Amore Pad.adg | query:Sounds#Pad:FileId_4985 |
| MPE Dark Cinema Pad.adg | query:Sounds#Pad:FileId_4986 |
| MPE Depth Pressure Pad.adg | query:Sounds#Pad:FileId_4987 |
| MPE Ghost Choir Pad.adg | query:Sounds#Pad:FileId_4988 |
| MPE Ghost Ship Pad.adg | query:Sounds#Pad:FileId_4989 |
| MPE Gravity.adg | query:Sounds#Pad:FileId_4990 |
| MPE Pearlescent Tides Pad.adg | query:Sounds#Pad:FileId_4991 |
| MPE Power Plant Pad.adg | query:Sounds#Pad:FileId_4992 |
| MPE Slide Orchestrator.adg | query:Sounds#Pad:FileId_4993 |
| MPE Velvet Robe.adg | query:Sounds#Pad:FileId_4994 |
| MPE Windwhistle Pad.adg | query:Sounds#Pad:FileId_4995 |
| Perception Pad.adg | query:Sounds#Pad:FileId_4940 |
| Phase Riser Pad.adg | query:Sounds#Pad:FileId_4941 |
| Phasing Bell Pad.adg | query:Sounds#Pad:FileId_4942 |
| Pluck Pad.adg | query:Sounds#Pad:FileId_4943 |
| PPP Pad.adv | query:Sounds#Pad:FileId_6496 |
| Rectangular Bliss.adg | query:Sounds#Pad:FileId_4944 |
| Rising Fog Pad.adv | query:Sounds#Pad:FileId_7137 |
| Ruggine Pad.adg | query:Sounds#Pad:FileId_4945 |
| Sandman Pad.adg | query:Sounds#Pad:FileId_4946 |
| Scape Shape Pad.adv | query:Sounds#Pad:FileId_7138 |
| Scream Shim Pad.adg | query:Sounds#Pad:FileId_4947 |
| Screech Pad.adg | query:Sounds#Pad:FileId_4948 |
| Sea Pad.adg | query:Sounds#Pad:FileId_4949 |
| Shark Pad.adv | query:Sounds#Pad:FileId_7139 |
| Sharp Edge.adg | query:Sounds#Pad:FileId_4950 |
| Shocker Swell.adg | query:Sounds#Pad:FileId_4951 |
| Shy Guy.adg | query:Sounds#Pad:FileId_4952 |
| Silky Sheen Pad.adg | query:Sounds#Pad:FileId_4953 |
| Sitar Soundtrack Pad.adg | query:Sounds#Pad:FileId_4954 |
| Slow Drown Pad.adg | query:Sounds#Pad:FileId_4955 |
| Soundtrack Lore Pad.adg | query:Sounds#Pad:FileId_4956 |
| Space Blip Pad.adg | query:Sounds#Pad:FileId_4957 |
| Spectral Movement Pad.adg | query:Sounds#Pad:FileId_4958 |
| Star Talk Pad.adv | query:Sounds#Pad:FileId_7140 |
| Stars Pad.adg | query:Sounds#Pad:FileId_4959 |
| Starshower Pad.adg | query:Sounds#Pad:FileId_4960 |
| Stencil Pad.adg | query:Sounds#Pad:FileId_4961 |
| Stratus Formation.adg | query:Sounds#Pad:FileId_4962 |
| Super Bloom.adg | query:Sounds#Pad:FileId_4963 |
| Sweeper Saege Pad.adg | query:Sounds#Pad:FileId_4964 |
| Sweet Tooth.adv | query:Sounds#Pad:FileId_7141 |
| Swimming Pool.adg | query:Sounds#Pad:FileId_4965 |
| Synorch Pad.adg | query:Sounds#Pad:FileId_4966 |
| Synth on Screen.adv | query:Sounds#Pad:FileId_7142 |
| Thicket Wail Pad.adg | query:Sounds#Pad:FileId_4967 |
| Transcending Pluck Pad.adg | query:Sounds#Pad:FileId_4968 |
| Tree Branches.adg | query:Sounds#Pad:FileId_4969 |
| Tube Step Pad.adg | query:Sounds#Pad:FileId_4970 |
| Van The Man Pad.adg | query:Sounds#Pad:FileId_4972 |
| Vapor Chimes Pad.adg | query:Sounds#Pad:FileId_4973 |
| Vapor Trails.adg | query:Sounds#Pad:FileId_4974 |
| Vaporesque Pad.adg | query:Sounds#Pad:FileId_4975 |
| VHS Dreams.adg | query:Sounds#Pad:FileId_4971 |
| Vibrato Pad.adg | query:Sounds#Pad:FileId_4976 |
| Vista Cruiser.adg | query:Sounds#Pad:FileId_4977 |
| Voicelike Pad.adg | query:Sounds#Pad:FileId_4978 |
| Wailing Poly Pad.adg | query:Sounds#Pad:FileId_4979 |
| Warm Analog Pad.adg | query:Sounds#Pad:FileId_4980 |
| Warm Bubbly Pad.adv | query:Sounds#Pad:FileId_6497 |
| Wave Pad.adv | query:Sounds#Pad:FileId_7143 |
| Wet Air Pad.adg | query:Sounds#Pad:FileId_4981 |
| Yin Yang.adg | query:Sounds#Pad:FileId_4982 |

### Percussive (11 items)
| Name | URI |
|---|---|
| 3D Reso Percussion.adg | query:Sounds#Percussive:FileId_4876 |
| Analog Ride.adv | query:Sounds#Percussive:FileId_7120 |
| Analog Tom.adv | query:Sounds#Percussive:FileId_7121 |
| FM Halfstep Clang.adv | query:Sounds#Percussive:FileId_7122 |
| FM Halfstep Sticks.adv | query:Sounds#Percussive:FileId_7123 |
| FM Halfstep Whirr.adv | query:Sounds#Percussive:FileId_7124 |
| Hyper Pot.adg | query:Sounds#Percussive:FileId_4877 |
| Hyper Snare.adg | query:Sounds#Percussive:FileId_4878 |
| Lo-Fi Kick.adg | query:Sounds#Percussive:FileId_4879 |
| Lo-Fi Metal Hit.adv | query:Sounds#Percussive:FileId_7125 |
| Lo-Fi Tech Tom.adv | query:Sounds#Percussive:FileId_7126 |

### Piano & Keys (50 items)
| Name | URI |
|---|---|
| Ac Piano Upright.adg | query:Sounds#Piano%20&%20Keys:FileId_4834 |
| Bellatine.adv | query:Sounds#Piano%20&%20Keys:FileId_7115 |
| Childhood Home Piano.adg | query:Sounds#Piano%20&%20Keys:FileId_4835 |
| Clav Anvil.adg | query:Sounds#Piano%20&%20Keys:FileId_4836 |
| Clav Chord Delay.adv | query:Sounds#Piano%20&%20Keys:FileId_6486 |
| Clav Rebel Musak.adg | query:Sounds#Piano%20&%20Keys:FileId_4837 |
| Clav Variations.adg | query:Sounds#Piano%20&%20Keys:FileId_4838 |
| E-Piano Basic.adg | query:Sounds#Piano%20&%20Keys:FileId_4839 |
| E-Piano Blue Cmin9.adg | query:Sounds#Piano%20&%20Keys:FileId_4840 |
| E-Piano Cheap.adv | query:Sounds#Piano%20&%20Keys:FileId_6489 |
| E-Piano Classic.adg | query:Sounds#Piano%20&%20Keys:FileId_4841 |
| E-Piano CMaj7 Chord.adv | query:Sounds#Piano%20&%20Keys:FileId_6487 |
| E-Piano CMin7 Chord.adv | query:Sounds#Piano%20&%20Keys:FileId_6488 |
| E-Piano Crep Slide.adg | query:Sounds#Piano%20&%20Keys:FileId_4842 |
| E-Piano Detuned.adg | query:Sounds#Piano%20&%20Keys:FileId_4843 |
| E-Piano Faceplant.adg | query:Sounds#Piano%20&%20Keys:FileId_4844 |
| E-Piano Floating.adg | query:Sounds#Piano%20&%20Keys:FileId_4845 |
| E-Piano Light.adg | query:Sounds#Piano%20&%20Keys:FileId_4846 |
| E-Piano Moody.adg | query:Sounds#Piano%20&%20Keys:FileId_4847 |
| E-Piano Old School.adg | query:Sounds#Piano%20&%20Keys:FileId_4848 |
| E-Piano Rhodish.adg | query:Sounds#Piano%20&%20Keys:FileId_4849 |
| E-Piano Roads.adg | query:Sounds#Piano%20&%20Keys:FileId_4850 |
| E-Piano Rusty.adg | query:Sounds#Piano%20&%20Keys:FileId_4851 |
| E-Piano Straight.adg | query:Sounds#Piano%20&%20Keys:FileId_4852 |
| E-Piano Synth.adg | query:Sounds#Piano%20&%20Keys:FileId_4853 |
| E-Piano Wurli.adg | query:Sounds#Piano%20&%20Keys:FileId_4854 |
| FM Piano Bright Tines.adg | query:Sounds#Piano%20&%20Keys:FileId_4855 |
| FM Piano Classic.adg | query:Sounds#Piano%20&%20Keys:FileId_4856 |
| Grand Piano Single Sample.adv | query:Sounds#Piano%20&%20Keys:FileId_6490 |
| Grand Piano.adg | query:Sounds#Piano%20&%20Keys:FileId_4857 |
| Harmonium Synth.adg | query:Sounds#Piano%20&%20Keys:FileId_4858 |
| Harpsichord.adg | query:Sounds#Piano%20&%20Keys:FileId_4859 |
| Kuti Keys.adg | query:Sounds#Piano%20&%20Keys:FileId_4860 |
| Music Box.adg | query:Sounds#Piano%20&%20Keys:FileId_4861 |
| Organ Analog.adg | query:Sounds#Piano%20&%20Keys:FileId_4862 |
| Organ Angry.adg | query:Sounds#Piano%20&%20Keys:FileId_4863 |
| Organ Bandstand.adg | query:Sounds#Piano%20&%20Keys:FileId_4864 |
| Organ Dynamic.adg | query:Sounds#Piano%20&%20Keys:FileId_4865 |
| Organ Funky.adg | query:Sounds#Piano%20&%20Keys:FileId_4866 |
| Organ Ghost.adg | query:Sounds#Piano%20&%20Keys:FileId_4867 |
| Organ House.adg | query:Sounds#Piano%20&%20Keys:FileId_4868 |
| Organ Klick.adg | query:Sounds#Piano%20&%20Keys:FileId_4869 |
| Organ LoFi.adg | query:Sounds#Piano%20&%20Keys:FileId_4870 |
| Organ Plus Synth.adg | query:Sounds#Piano%20&%20Keys:FileId_4871 |
| Organ Plush.adg | query:Sounds#Piano%20&%20Keys:FileId_4872 |
| Organ Rough.adg | query:Sounds#Piano%20&%20Keys:FileId_4873 |
| Organ Transistor Series.adg | query:Sounds#Piano%20&%20Keys:FileId_4874 |
| Paddles Out.adv | query:Sounds#Piano%20&%20Keys:FileId_7116 |
| Synth Piano.adv | query:Sounds#Piano%20&%20Keys:FileId_7117 |
| Transistor Reeds.adv | query:Sounds#Piano%20&%20Keys:FileId_7118 |

### Strings (25 items)
| Name | URI |
|---|---|
| Ac Strings Orch.adg | query:Sounds#Strings:FileId_4752 |
| Ac Strings Pizz Basic.adg | query:Sounds#Strings:FileId_4753 |
| Ac Strings Pizz Oct.adg | query:Sounds#Strings:FileId_4754 |
| Ac Strings Pizz Stage.adg | query:Sounds#Strings:FileId_4755 |
| Basic Jun Strings.adg | query:Sounds#Strings:FileId_4756 |
| Cruiser Strings.adg | query:Sounds#Strings:FileId_4757 |
| Darkened Strings.adv | query:Sounds#Strings:FileId_7102 |
| Drama Synth.adg | query:Sounds#Strings:FileId_4758 |
| Evangelis Strings.adg | query:Sounds#Strings:FileId_4759 |
| Feedback Bow.adg | query:Sounds#Strings:FileId_4760 |
| M Tron Strings.adg | query:Sounds#Strings:FileId_4761 |
| Magnetic Strings.adg | query:Sounds#Strings:FileId_4762 |
| Metallic Strings.adv | query:Sounds#Strings:FileId_7103 |
| MPE Cello Bow.adg | query:Sounds#Strings:FileId_4770 |
| MPE Synth Bow.adg | query:Sounds#Strings:FileId_4771 |
| MPE Warping Strings.adg | query:Sounds#Strings:FileId_4772 |
| Off World Strings.adg | query:Sounds#Strings:FileId_4763 |
| Pitch Rise Strings.adv | query:Sounds#Strings:FileId_7104 |
| Razor Strings.adg | query:Sounds#Strings:FileId_4764 |
| Second Stellar Strings.adg | query:Sounds#Strings:FileId_4765 |
| Slow Roll Strings.adv | query:Sounds#Strings:FileId_7105 |
| Star Dust Strings.adv | query:Sounds#Strings:FileId_7106 |
| String Machine.adg | query:Sounds#Strings:FileId_4766 |
| Synthetic Choir Strings.adg | query:Sounds#Strings:FileId_4767 |
| Synthetic Strings.adg | query:Sounds#Strings:FileId_4768 |

### Synth Keys (116 items)
| Name | URI |
|---|---|
| 80s Tape.adv | query:Sounds#Synth%20Keys:FileId_7085 |
| Abyss Keys.adg | query:Sounds#Synth%20Keys:FileId_4653 |
| Analog Emulation Keys.adg | query:Sounds#Synth%20Keys:FileId_4654 |
| Analog Piano.adg | query:Sounds#Synth%20Keys:FileId_4655 |
| Ancient Dream.adg | query:Sounds#Synth%20Keys:FileId_4656 |
| Angelina.adg | query:Sounds#Synth%20Keys:FileId_4657 |
| Arcade Keys.adg | query:Sounds#Synth%20Keys:FileId_4658 |
| Arcade Split.adv | query:Sounds#Synth%20Keys:FileId_7086 |
| Ashburn Funk Keys.adg | query:Sounds#Synth%20Keys:FileId_4659 |
| Atlas Keys.adv | query:Sounds#Synth%20Keys:FileId_7087 |
| Autumn Grifter.adg | query:Sounds#Synth%20Keys:FileId_4660 |
| Basic Bell Keys.adg | query:Sounds#Synth%20Keys:FileId_4661 |
| Basic Electronic Keys.adg | query:Sounds#Synth%20Keys:FileId_4662 |
| Basic Pluck Keys.adg | query:Sounds#Synth%20Keys:FileId_4663 |
| Basic Saw Dirty.adg | query:Sounds#Synth%20Keys:FileId_4664 |
| Basic Saw Large.adg | query:Sounds#Synth%20Keys:FileId_4665 |
| Basic Sine Keys.adg | query:Sounds#Synth%20Keys:FileId_4666 |
| Basic Square.adg | query:Sounds#Synth%20Keys:FileId_4667 |
| Basic Tape Keys.adg | query:Sounds#Synth%20Keys:FileId_4668 |
| Basic Teared Down Keys.adg | query:Sounds#Synth%20Keys:FileId_4669 |
| Basic Trip Keys.adg | query:Sounds#Synth%20Keys:FileId_4670 |
| Beating Vibraphone.adv | query:Sounds#Synth%20Keys:FileId_7088 |
| Belleville Keys.adg | query:Sounds#Synth%20Keys:FileId_4671 |
| Bright Square.adg | query:Sounds#Synth%20Keys:FileId_4672 |
| Broken Token.adg | query:Sounds#Synth%20Keys:FileId_4673 |
| Canadian Keys.adg | query:Sounds#Synth%20Keys:FileId_4674 |
| Cars In The 80s Keys.adg | query:Sounds#Synth%20Keys:FileId_4675 |
| Cathedral Keys.adg | query:Sounds#Synth%20Keys:FileId_4676 |
| Childhood Keys.adg | query:Sounds#Synth%20Keys:FileId_4677 |
| Chord Afterfade.adg | query:Sounds#Synth%20Keys:FileId_4678 |
| Chord Deep Keys.adg | query:Sounds#Synth%20Keys:FileId_4679 |
| Chord Det Keys.adg | query:Sounds#Synth%20Keys:FileId_4680 |
| Chord Dub Keys.adg | query:Sounds#Synth%20Keys:FileId_4681 |
| Chord Minor to Major.adg | query:Sounds#Synth%20Keys:FileId_4682 |
| Chord Raise Keys.adg | query:Sounds#Synth%20Keys:FileId_4683 |
| Chord Rotaviolin.adg | query:Sounds#Synth%20Keys:FileId_4684 |
| Chord Soft Keys.adv | query:Sounds#Synth%20Keys:FileId_6483 |
| Complex Morphed Keys.adg | query:Sounds#Synth%20Keys:FileId_4685 |
| Contact Keys.adg | query:Sounds#Synth%20Keys:FileId_4686 |
| Dance Keys.adg | query:Sounds#Synth%20Keys:FileId_4687 |
| Dark Sky Keys.adg | query:Sounds#Synth%20Keys:FileId_4688 |
| Delta Polylogue.adv | query:Sounds#Synth%20Keys:FileId_7089 |
| Digital Dawn Keys.adg | query:Sounds#Synth%20Keys:FileId_4689 |
| Distant Dream.adg | query:Sounds#Synth%20Keys:FileId_4690 |
| Double Take Keys.adg | query:Sounds#Synth%20Keys:FileId_4691 |
| Dream Keys.adg | query:Sounds#Synth%20Keys:FileId_4692 |
| Evolve Organ.adg | query:Sounds#Synth%20Keys:FileId_4693 |
| Exo Keys.adg | query:Sounds#Synth%20Keys:FileId_4694 |
| Faded Keys.adg | query:Sounds#Synth%20Keys:FileId_4695 |
| Fake Whirlie.adg | query:Sounds#Synth%20Keys:FileId_4696 |
| Fez Keys.adg | query:Sounds#Synth%20Keys:FileId_4697 |
| Floom.adv | query:Sounds#Synth%20Keys:FileId_7090 |
| Fluttering North.adg | query:Sounds#Synth%20Keys:FileId_4698 |
| Fuzzy Analog Keys.adg | query:Sounds#Synth%20Keys:FileId_4699 |
| Galleon Pianola.adg | query:Sounds#Synth%20Keys:FileId_4700 |
| Gentle Sixty.adv | query:Sounds#Synth%20Keys:FileId_7091 |
| Gliss Keys.adg | query:Sounds#Synth%20Keys:FileId_4701 |
| Glitter Keys.adg | query:Sounds#Synth%20Keys:FileId_4702 |
| Harmonic Slide.adg | query:Sounds#Synth%20Keys:FileId_4703 |
| House Play.adg | query:Sounds#Synth%20Keys:FileId_4704 |
| Hyaline Mentality Keys.adg | query:Sounds#Synth%20Keys:FileId_4705 |
| Keynell.adv | query:Sounds#Synth%20Keys:FileId_7092 |
| Koleko Plux Keys.adg | query:Sounds#Synth%20Keys:FileId_4706 |
| La String Machine.adv | query:Sounds#Synth%20Keys:FileId_7093 |
| Light Electro.adg | query:Sounds#Synth%20Keys:FileId_4707 |
| Light Keys.adg | query:Sounds#Synth%20Keys:FileId_4708 |
| Little Synth Piano.adg | query:Sounds#Synth%20Keys:FileId_4709 |
| Maverick Keys.adg | query:Sounds#Synth%20Keys:FileId_4710 |
| Mellow Sine Keys.adg | query:Sounds#Synth%20Keys:FileId_4711 |
| Mellow Tine Keys.adg | query:Sounds#Synth%20Keys:FileId_4712 |
| Modded Keys.adg | query:Sounds#Synth%20Keys:FileId_4713 |
| Morphing Chords.adg | query:Sounds#Synth%20Keys:FileId_4714 |
| MPE Dusty Memory Organette.adg | query:Sounds#Synth%20Keys:FileId_4741 |
| MPE Evil Underneath.adg | query:Sounds#Synth%20Keys:FileId_4742 |
| MPE Faulty Wurli.adg | query:Sounds#Synth%20Keys:FileId_4744 |
| MPE FM Land.adg | query:Sounds#Synth%20Keys:FileId_4743 |
| MPE Glorious Chord.adg | query:Sounds#Synth%20Keys:FileId_4745 |
| MPE Mahogany Rose Organ.adg | query:Sounds#Synth%20Keys:FileId_4746 |
| MPE Monomorph.adg | query:Sounds#Synth%20Keys:FileId_4747 |
| MPE Sine Pressure.adg | query:Sounds#Synth%20Keys:FileId_4748 |
| MPE Synth Pipe Organ.adg | query:Sounds#Synth%20Keys:FileId_4749 |
| MPE Velocity Grain.adg | query:Sounds#Synth%20Keys:FileId_4750 |
| Night Crystal.adg | query:Sounds#Synth%20Keys:FileId_4715 |
| Numan Keystrike.adv | query:Sounds#Synth%20Keys:FileId_7094 |
| OK Corral Keys.adg | query:Sounds#Synth%20Keys:FileId_4716 |
| Orange Sky Keys.adg | query:Sounds#Synth%20Keys:FileId_4717 |
| Orbit Ray.adv | query:Sounds#Synth%20Keys:FileId_7095 |
| Oregon Trail.adg | query:Sounds#Synth%20Keys:FileId_4718 |
| Organ Mutations.adg | query:Sounds#Synth%20Keys:FileId_4719 |
| Particles Keys.adg | query:Sounds#Synth%20Keys:FileId_4720 |
| Peculiar Galaxy Keys.adg | query:Sounds#Synth%20Keys:FileId_4721 |
| Phase Keys.adg | query:Sounds#Synth%20Keys:FileId_4722 |
| Pointastic Keys.adg | query:Sounds#Synth%20Keys:FileId_4723 |
| Primaneve Keys.adg | query:Sounds#Synth%20Keys:FileId_4724 |
| Rectangular Bliss.adv | query:Sounds#Synth%20Keys:FileId_7096 |
| Retro Bell Keys.adv | query:Sounds#Synth%20Keys:FileId_7097 |
| Reverberant Keys.adv | query:Sounds#Synth%20Keys:FileId_6484 |
| Rezowire.adg | query:Sounds#Synth%20Keys:FileId_4725 |
| Saw Echo Keys.adg | query:Sounds#Synth%20Keys:FileId_4726 |
| Shapemod Keys.adg | query:Sounds#Synth%20Keys:FileId_4727 |
| Shy LoFi Keys.adg | query:Sounds#Synth%20Keys:FileId_4728 |
| Slip Sliding.adv | query:Sounds#Synth%20Keys:FileId_7098 |
| Spheric Keys.adg | query:Sounds#Synth%20Keys:FileId_4729 |
| Stars Keys.adg | query:Sounds#Synth%20Keys:FileId_4730 |
| Stereo Saw.adv | query:Sounds#Synth%20Keys:FileId_7099 |
| Suburban Keys.adg | query:Sounds#Synth%20Keys:FileId_4731 |
| Synth Marimba.adg | query:Sounds#Synth%20Keys:FileId_4732 |
| Tape Beast Keys.adg | query:Sounds#Synth%20Keys:FileId_4733 |
| Tiny Echoes.adv | query:Sounds#Synth%20Keys:FileId_7100 |
| Tree Line.adg | query:Sounds#Synth%20Keys:FileId_4734 |
| Twisted Keys.adg | query:Sounds#Synth%20Keys:FileId_4735 |
| Vintage Saw Keys.adg | query:Sounds#Synth%20Keys:FileId_4736 |
| Wah Synth Organ.adg | query:Sounds#Synth%20Keys:FileId_4737 |
| Warm Saw Keys.adg | query:Sounds#Synth%20Keys:FileId_4738 |
| X-Square Keys.adg | query:Sounds#Synth%20Keys:FileId_4739 |

### Synth Lead (85 items)
| Name | URI |
|---|---|
| Acceleration Lead.adg | query:Sounds#Synth%20Lead:FileId_4576 |
| Analog Stab Lead.adv | query:Sounds#Synth%20Lead:FileId_6479 |
| Apple Solo.adg | query:Sounds#Synth%20Lead:FileId_4577 |
| Badass Lead.adg | query:Sounds#Synth%20Lead:FileId_4578 |
| Ballroom Blues.adg | query:Sounds#Synth%20Lead:FileId_4579 |
| Basic Glide Lead.adg | query:Sounds#Synth%20Lead:FileId_4580 |
| Basic OG Lead.adg | query:Sounds#Synth%20Lead:FileId_4581 |
| Basic Peak Lead.adg | query:Sounds#Synth%20Lead:FileId_4582 |
| Basic Retro Lead.adg | query:Sounds#Synth%20Lead:FileId_4583 |
| Basic Sine Drive Lead.adg | query:Sounds#Synth%20Lead:FileId_4584 |
| Basic Waves Lead.adg | query:Sounds#Synth%20Lead:FileId_4585 |
| Basic Wind Lead.adg | query:Sounds#Synth%20Lead:FileId_4586 |
| Bottle Blower.adg | query:Sounds#Synth%20Lead:FileId_4587 |
| Brainsticker.adg | query:Sounds#Synth%20Lead:FileId_4588 |
| Burrow Lead.adg | query:Sounds#Synth%20Lead:FileId_4589 |
| Chord Vintage Lead.adg | query:Sounds#Synth%20Lead:FileId_4590 |
| Chrome Frame.adg | query:Sounds#Synth%20Lead:FileId_4591 |
| Clara Lead.adg | query:Sounds#Synth%20Lead:FileId_4592 |
| Classic Club Saw.adg | query:Sounds#Synth%20Lead:FileId_4593 |
| Complex Rotor Lead.adg | query:Sounds#Synth%20Lead:FileId_4594 |
| Crunch Arcade.adv | query:Sounds#Synth%20Lead:FileId_7078 |
| Dense Lead.adg | query:Sounds#Synth%20Lead:FileId_4595 |
| Dialogue Lead.adg | query:Sounds#Synth%20Lead:FileId_4596 |
| Disto Lead.adg | query:Sounds#Synth%20Lead:FileId_4597 |
| Doublette.adg | query:Sounds#Synth%20Lead:FileId_4598 |
| Dreamscape Lead.adg | query:Sounds#Synth%20Lead:FileId_4599 |
| Drifting Interferences.adg | query:Sounds#Synth%20Lead:FileId_4600 |
| Dusty Lead.adg | query:Sounds#Synth%20Lead:FileId_4601 |
| Epic Chords.adg | query:Sounds#Synth%20Lead:FileId_4602 |
| Euphoria Lead.adv | query:Sounds#Synth%20Lead:FileId_7079 |
| Filtered Sync Lead.adg | query:Sounds#Synth%20Lead:FileId_4603 |
| Flint Blaster.adg | query:Sounds#Synth%20Lead:FileId_4604 |
| Floppy Disc Lead.adg | query:Sounds#Synth%20Lead:FileId_4605 |
| Formaggio Lead.adg | query:Sounds#Synth%20Lead:FileId_4606 |
| Freak Bounce Lead.adg | query:Sounds#Synth%20Lead:FileId_4607 |
| Game Console.adv | query:Sounds#Synth%20Lead:FileId_7080 |
| Grime Lead.adg | query:Sounds#Synth%20Lead:FileId_4608 |
| Hardcastle Solo.adg | query:Sounds#Synth%20Lead:FileId_4609 |
| Hentai Dream.adg | query:Sounds#Synth%20Lead:FileId_4610 |
| Homebound Lead.adg | query:Sounds#Synth%20Lead:FileId_4611 |
| Horn Lead.adg | query:Sounds#Synth%20Lead:FileId_4612 |
| Hubus Lead.adv | query:Sounds#Synth%20Lead:FileId_7081 |
| Kentucky Lead.adv | query:Sounds#Synth%20Lead:FileId_7082 |
| Lead Thing.adg | query:Sounds#Synth%20Lead:FileId_4613 |
| Mega Saw.adg | query:Sounds#Synth%20Lead:FileId_4614 |
| Mirror Girl.adg | query:Sounds#Synth%20Lead:FileId_4615 |
| Mod Saw Lead.adg | query:Sounds#Synth%20Lead:FileId_4616 |
| Moving Square.adg | query:Sounds#Synth%20Lead:FileId_4617 |
| MPE Standup Lead.adg | query:Sounds#Synth%20Lead:FileId_4650 |
| MPE Toxic Lead.adg | query:Sounds#Synth%20Lead:FileId_4651 |
| Musette Lead.adg | query:Sounds#Synth%20Lead:FileId_4618 |
| Nature Lead.adg | query:Sounds#Synth%20Lead:FileId_4619 |
| Noise Sweep Lead.adg | query:Sounds#Synth%20Lead:FileId_4620 |
| Parade Saw Lead.adg | query:Sounds#Synth%20Lead:FileId_4621 |
| Power Surge.adg | query:Sounds#Synth%20Lead:FileId_4622 |
| Purple Lead.adg | query:Sounds#Synth%20Lead:FileId_4623 |
| Rave Lead.adg | query:Sounds#Synth%20Lead:FileId_4624 |
| Reed Synth.adg | query:Sounds#Synth%20Lead:FileId_4625 |
| Ring Modular Lead.adv | query:Sounds#Synth%20Lead:FileId_6480 |
| Robot Lead.adg | query:Sounds#Synth%20Lead:FileId_4626 |
| Rogue Mischief Lead.adg | query:Sounds#Synth%20Lead:FileId_4627 |
| Rogue.adv | query:Sounds#Synth%20Lead:FileId_7083 |
| Rusty Lead.adg | query:Sounds#Synth%20Lead:FileId_4628 |
| Sauce Lead.adg | query:Sounds#Synth%20Lead:FileId_4629 |
| Saw Peak.adg | query:Sounds#Synth%20Lead:FileId_4630 |
| Saw Sweep.adg | query:Sounds#Synth%20Lead:FileId_4631 |
| Smores Lead.adg | query:Sounds#Synth%20Lead:FileId_4632 |
| Soover Lead.adv | query:Sounds#Synth%20Lead:FileId_6481 |
| Sparkle Lead.adg | query:Sounds#Synth%20Lead:FileId_4633 |
| Subterranea Lead.adg | query:Sounds#Synth%20Lead:FileId_4634 |
| Super Soover Lead.adg | query:Sounds#Synth%20Lead:FileId_4635 |
| Superstring Lead.adg | query:Sounds#Synth%20Lead:FileId_4636 |
| Sweet Lead.adg | query:Sounds#Synth%20Lead:FileId_4637 |
| Swirl Lead.adg | query:Sounds#Synth%20Lead:FileId_4638 |
| Sync Electrik Lead.adg | query:Sounds#Synth%20Lead:FileId_4639 |
| Synchro Lead.adg | query:Sounds#Synth%20Lead:FileId_4640 |
| Syripples Lead.adg | query:Sounds#Synth%20Lead:FileId_4641 |
| Tech Lead.adg | query:Sounds#Synth%20Lead:FileId_4642 |
| The Sword Saint.adg | query:Sounds#Synth%20Lead:FileId_4643 |
| Theremin Whistle.adg | query:Sounds#Synth%20Lead:FileId_4644 |
| Tunnel Lead.adg | query:Sounds#Synth%20Lead:FileId_4645 |
| UK Siren Lead.adg | query:Sounds#Synth%20Lead:FileId_4646 |
| Utah Lead.adg | query:Sounds#Synth%20Lead:FileId_4647 |
| Wedding Lead.adg | query:Sounds#Synth%20Lead:FileId_4648 |

### Synth Rhythmic (54 items)
| Name | URI |
|---|---|
| Alien Army.adg | query:Sounds#Synth%20Rhythmic:FileId_4523 |
| Basic Harp Arp.adg | query:Sounds#Synth%20Rhythmic:FileId_4524 |
| Basic Keys Loop.adg | query:Sounds#Synth%20Rhythmic:FileId_4525 |
| Basic Pluck Arp.adg | query:Sounds#Synth%20Rhythmic:FileId_4526 |
| Basic Retro Arp.adg | query:Sounds#Synth%20Rhythmic:FileId_4527 |
| Basic Signal Arp.adg | query:Sounds#Synth%20Rhythmic:FileId_4528 |
| Bass Horn.adg | query:Sounds#Synth%20Rhythmic:FileId_4529 |
| Bell Patterns.adg | query:Sounds#Synth%20Rhythmic:FileId_4530 |
| Chord Molecule Pulse.adg | query:Sounds#Synth%20Rhythmic:FileId_4531 |
| Cloud Cover Arp.adg | query:Sounds#Synth%20Rhythmic:FileId_4532 |
| Daily Routine.adg | query:Sounds#Synth%20Rhythmic:FileId_4533 |
| Digital Whisper Pulse.adg | query:Sounds#Synth%20Rhythmic:FileId_4534 |
| Downwards Retro Arp.adg | query:Sounds#Synth%20Rhythmic:FileId_4535 |
| Echo Pulse.adv | query:Sounds#Synth%20Rhythmic:FileId_7075 |
| Ecstatic Pluck.adg | query:Sounds#Synth%20Rhythmic:FileId_4536 |
| Eurythmical Arp.adg | query:Sounds#Synth%20Rhythmic:FileId_4537 |
| Felixian Pluck Arp.adg | query:Sounds#Synth%20Rhythmic:FileId_4538 |
| Formant Rhythm.adg | query:Sounds#Synth%20Rhythmic:FileId_4539 |
| Git Proc Loop.adv | query:Sounds#Synth%20Rhythmic:FileId_6477 |
| Gizmodo Swapshop.adg | query:Sounds#Synth%20Rhythmic:FileId_4540 |
| Glitch Sequence.adg | query:Sounds#Synth%20Rhythmic:FileId_4541 |
| Helly Belly.adg | query:Sounds#Synth%20Rhythmic:FileId_4542 |
| Lightest Night Arp.adg | query:Sounds#Synth%20Rhythmic:FileId_4543 |
| Live Wire.adg | query:Sounds#Synth%20Rhythmic:FileId_4544 |
| Mean Pulse.adg | query:Sounds#Synth%20Rhythmic:FileId_4545 |
| Mikado.adg | query:Sounds#Synth%20Rhythmic:FileId_4546 |
| Mouse Arp.adg | query:Sounds#Synth%20Rhythmic:FileId_4547 |
| MPE FM Arp.adg | query:Sounds#Synth%20Rhythmic:FileId_4570 |
| MPE Level Ives Pad.adg | query:Sounds#Synth%20Rhythmic:FileId_4571 |
| MPE Metallic Keys.adg | query:Sounds#Synth%20Rhythmic:FileId_4572 |
| MPE Polypulse Pressure.adg | query:Sounds#Synth%20Rhythmic:FileId_4573 |
| MPE Spieluhr.adg | query:Sounds#Synth%20Rhythmic:FileId_4574 |
| Neptune Arp.adg | query:Sounds#Synth%20Rhythmic:FileId_4548 |
| Neuro Pulse Bass.adg | query:Sounds#Synth%20Rhythmic:FileId_4549 |
| Octaves Pad.adg | query:Sounds#Synth%20Rhythmic:FileId_4550 |
| Precision Keys.adg | query:Sounds#Synth%20Rhythmic:FileId_4551 |
| Pulsating Pad.adv | query:Sounds#Synth%20Rhythmic:FileId_7076 |
| Pulsing Click Pad.adg | query:Sounds#Synth%20Rhythmic:FileId_4552 |
| Pulsing LoFi Pluck.adg | query:Sounds#Synth%20Rhythmic:FileId_4553 |
| Pulsing Organ Synth.adg | query:Sounds#Synth%20Rhythmic:FileId_4554 |
| Pulsing Raum Keys.adg | query:Sounds#Synth%20Rhythmic:FileId_4555 |
| Rhythmic Filter Keys.adg | query:Sounds#Synth%20Rhythmic:FileId_4556 |
| Rhythmic Oshima Pluck.adg | query:Sounds#Synth%20Rhythmic:FileId_4557 |
| Rhythmic Paradise Pad.adg | query:Sounds#Synth%20Rhythmic:FileId_4558 |
| Rolling Hi Tech Perc.adg | query:Sounds#Synth%20Rhythmic:FileId_4559 |
| Sencha Arp.adg | query:Sounds#Synth%20Rhythmic:FileId_4560 |
| Snow Peaks Arp.adg | query:Sounds#Synth%20Rhythmic:FileId_4561 |
| Sogawni Split Arp.adg | query:Sounds#Synth%20Rhythmic:FileId_4562 |
| Space Arp.adg | query:Sounds#Synth%20Rhythmic:FileId_4563 |
| Steeple Chaser Arp.adg | query:Sounds#Synth%20Rhythmic:FileId_4564 |
| Stranger Pad.adg | query:Sounds#Synth%20Rhythmic:FileId_4565 |
| Trippy Drops Arp.adg | query:Sounds#Synth%20Rhythmic:FileId_4566 |
| Uplift Strings Arp.adg | query:Sounds#Synth%20Rhythmic:FileId_4567 |
| Vapor Games Arp.adg | query:Sounds#Synth%20Rhythmic:FileId_4568 |

### Winds (5 items) — FLUTES ONLY. No saxophone, clarinet, oboe, bassoon, or reed patches exist anywhere in this library.
| Name | URI |
|---|---|
| Basic Synth Flute.adg | query:Sounds#Winds:FileId_4517 |
| Clay Flute.adg | query:Sounds#Winds:FileId_4518 |
| Indian Flute.adg | query:Sounds#Winds:FileId_4519 |
| Synthetic Flute.adg | query:Sounds#Winds:FileId_4520 |
| Vacuum Flute.adg | query:Sounds#Winds:FileId_4521 |

## Drums
URI pattern for kits: `query:Drums#FileId_NNNN`. The bare Drum Rack device is `query:Drums#Drum%20Rack`.
Tip: search_browser("808 Core Kit", category="drums") returns it directly — no need to browse.

### Drum Rack device
| Name | URI |
|---|---|
| Drum Rack (empty device) | query:Drums#Drum%20Rack |

### Kits (144)
| Name | URI |
|---|---|
| 505 Core Kit.adg | query:Drums#FileId_5406 |
| 606 Core Kit.adg | query:Drums#FileId_5407 |
| 707 Core Kit.adg | query:Drums#FileId_5408 |
| 808 Core Kit.adg | query:Drums#FileId_5409 |
| 909 Core Kit.adg | query:Drums#FileId_5410 |
| Acuff Kit.adg | query:Drums#FileId_5416 |
| AG Techno Kit.adg | query:Drums#FileId_5354 |
| Ahlimba Kit.adg | query:Drums#FileId_5417 |
| Akustichord Kit.adg | query:Drums#FileId_5285 |
| Alert Kit.adg | query:Drums#FileId_5286 |
| Atom Kit.adg | query:Drums#FileId_5287 |
| Battu Kit.adg | query:Drums#FileId_5288 |
| Beard Kit.adg | query:Drums#FileId_5289 |
| Beastly Kit.adg | query:Drums#FileId_5356 |
| Bimini 828 Kit.adg | query:Drums#FileId_5290 |
| Bird Kit.adg | query:Drums#FileId_5291 |
| BNYX Boot Kit.adg | query:Drums#FileId_5355 |
| Boom Bap Kit.adg | query:Drums#FileId_5292 |
| Borja Kit.adg | query:Drums#FileId_5357 |
| C78 Core Kit.adg | query:Drums#FileId_5411 |
| Cage Kit.adg | query:Drums#FileId_5293 |
| Caption Kit.adg | query:Drums#FileId_5358 |
| Cardboard Kit.adg | query:Drums#FileId_5359 |
| Cashon Kit.adg | query:Drums#FileId_5360 |
| Cheetah Kit.adg | query:Drums#FileId_5361 |
| Chicago Kit.adg | query:Drums#FileId_5362 |
| Chromatone Kit.adg | query:Drums#FileId_5294 |
| Citizen Drop Kit.adg | query:Drums#FileId_5363 |
| Clint West Kit.adg | query:Drums#FileId_5295 |
| Clockwork Kit.adg | query:Drums#FileId_5364 |
| Coma Kit.adg | query:Drums#FileId_5296 |
| Combine Kit.adg | query:Drums#FileId_5297 |
| Control Kit.adg | query:Drums#FileId_5365 |
| Coral Kit.adg | query:Drums#FileId_5298 |
| Cortex Kit.adg | query:Drums#FileId_5366 |
| Corvaire Kit.adg | query:Drums#FileId_5418 |
| Count In Kit.adg | query:Drums#FileId_5299 |
| Crisp Kit.adg | query:Drums#FileId_5367 |
| Crushed Ice Kit.adg | query:Drums#FileId_5368 |
| Crystal Clear Kit.adg | query:Drums#FileId_5300 |
| Cutlass Kit.adg | query:Drums#FileId_5301 |
| Dancehall 80s Kit.adg | query:Drums#FileId_5370 |
| Datai Kit.adg | query:Drums#FileId_5371 |
| DECAP DTK 1 Kit.adg | query:Drums#FileId_5302 |
| DECAP DTK 2 Kit.adg | query:Drums#FileId_5303 |
| DECAP DTK 3 Kit.adg | query:Drums#FileId_5304 |
| DMX Core Kit.adg | query:Drums#FileId_5412 |
| Driller Kit.adg | query:Drums#FileId_5305 |
| Drum Machine Selector Kit.adg | query:Drums#FileId_5281 |
| Dry Session Kit.adg | query:Drums#FileId_5419 |
| DS Drum Rack.adg | query:Drums#FileId_5369 |
| ER Core Kit.adg | query:Drums#FileId_5413 |
| Fabrik Kit.adg | query:Drums#FileId_5306 |
| Feat Pete Kit.adg | query:Drums#FileId_5307 |
| Fixation Kit.adg | query:Drums#FileId_5308 |
| Flares Kit.adg | query:Drums#FileId_5372 |
| Focus Kit.adg | query:Drums#FileId_5309 |
| Formaggio 1 Kit.adg | query:Drums#FileId_5310 |
| Formaggio 2 Kit.adg | query:Drums#FileId_5311 |
| Four AM Kit.adg | query:Drums#FileId_5312 |
| Frantik Kit.adg | query:Drums#FileId_5313 |
| Garage Kit.adg | query:Drums#FileId_5373 |
| Gen Purpose Kit.adg | query:Drums#FileId_5420 |
| Glas Kit.adg | query:Drums#FileId_5374 |
| Glide Kit.adg | query:Drums#FileId_5421 |
| Golden Kit.adg | query:Drums#FileId_5314 |
| Grain Slap Kit.adg | query:Drums#FileId_5315 |
| Grit Life KIt.adg | query:Drums#FileId_5375 |
| Halfstep Kit.adg | query:Drums#FileId_5376 |
| Heritage Kit.adg | query:Drums#FileId_5316 |
| Hot Rod Kit.adg | query:Drums#FileId_5377 |
| Ichor Kit.adg | query:Drums#FileId_5378 |
| Ironman Kit.adg | query:Drums#FileId_5317 |
| Jarble Kit.adg | query:Drums#FileId_5379 |
| Kinky Kit.adg | query:Drums#FileId_5380 |
| Late Nite Kit.adg | query:Drums#FileId_5381 |
| Lay Down Kit.adg | query:Drums#FileId_5382 |
| LD Core Kit.adg | query:Drums#FileId_5414 |
| LDre Cafe Kit.adg | query:Drums#FileId_5318 |
| LDre Cozy Kit.adg | query:Drums#FileId_5319 |
| LDre Mellow Kit.adg | query:Drums#FileId_5320 |
| Lo-Fi Tech Kit.adg | query:Drums#FileId_5383 |
| Loaded Kit.adg | query:Drums#FileId_5321 |
| Lunacy Kit.adg | query:Drums#FileId_5322 |
| Lycra Kit.adg | query:Drums#FileId_5384 |
| Mad Mollusc Kit.adg | query:Drums#FileId_5390 |
| Mad Skill Kit.adg | query:Drums#FileId_5391 |
| Melt Kit.adg | query:Drums#FileId_5392 |
| Morning Driver Kit.adg | query:Drums#FileId_5325 |
| MPE Analog Kit.adg | query:Drums#FileId_5385 |
| MPE Baker Kit.adg | query:Drums#FileId_5323 |
| MPE Butta Kit.adg | query:Drums#FileId_5324 |
| MPE Chrome Kit.adg | query:Drums#FileId_5386 |
| MPE Hyper Kit.adg | query:Drums#FileId_5387 |
| MPE Meld Kit.adg | query:Drums#FileId_5388 |
| MPE Synth Lab Kit.adg | query:Drums#FileId_5389 |
| Mt Dill Kit.adg | query:Drums#FileId_5393 |
| Oracle Cohiba Kit.adg | query:Drums#FileId_5326 |
| Oracle Dirty Work Kit.adg | query:Drums#FileId_5327 |
| Oracle Electric Flankers Kit.adg | query:Drums#FileId_5328 |
| Oracle Halo Dust Kit.adg | query:Drums#FileId_5329 |
| Patience Kit.adg | query:Drums#FileId_5330 |
| Perc Kitchen Kit.adg | query:Drums#FileId_5422 |
| Percussion Core Kit.adg | query:Drums#FileId_5423 |
| Percussion Spirit Kit.adg | query:Drums#FileId_5424 |
| Planet Kit.adg | query:Drums#FileId_5394 |
| Plymouth Kit.adg | query:Drums#FileId_5425 |
| Product Kit.adg | query:Drums#FileId_5395 |
| Quark Kit.adg | query:Drums#FileId_5396 |
| Railway Kit.adg | query:Drums#FileId_5331 |
| Rattle Kit.adg | query:Drums#FileId_5332 |
| Reliance Kit.adg | query:Drums#FileId_5333 |
| Riddim Rager Kit.adg | query:Drums#FileId_5334 |
| Rushmore Kit.adg | query:Drums#FileId_5397 |
| Selectah Kit.adg | query:Drums#FileId_5335 |
| Selector Kit Clean.adg | query:Drums#FileId_5282 |
| Selector Kit Warm.adg | query:Drums#FileId_5283 |
| Sensor Kit.adg | query:Drums#FileId_5398 |
| Slackjaw Kit.adg | query:Drums#FileId_5336 |
| Sliced Break.adg | query:Drums#FileId_5337 |
| So Future Kit.adg | query:Drums#FileId_5399 |
| Source Kit.adg | query:Drums#FileId_5338 |
| Stark Kit.adg | query:Drums#FileId_5339 |
| Sticks Kit.adg | query:Drums#FileId_5340 |
| Stratus Rise Kit.adg | query:Drums#FileId_5400 |
| Street Mind Kit.adg | query:Drums#FileId_5341 |
| Strutter Kit.adg | query:Drums#FileId_5342 |
| Subtle Electronics Kit.adg | query:Drums#FileId_5401 |
| Swan Song Kit.adg | query:Drums#FileId_5343 |
| Taka School Kit.adg | query:Drums#FileId_5344 |
| Taka Spike Kit.adg | query:Drums#FileId_5345 |
| Taka Vibe Kit.adg | query:Drums#FileId_5346 |
| Taxi Kit.adg | query:Drums#FileId_5347 |
| That Feel Kit.adg | query:Drums#FileId_5348 |
| Thicket Kit.adg | query:Drums#FileId_5349 |
| Trancil Exit Kit.adg | query:Drums#FileId_5402 |
| Unseen Kit.adg | query:Drums#FileId_5350 |
| Vibrance Kit.adg | query:Drums#FileId_5351 |
| Viral Kit.adg | query:Drums#FileId_5403 |
| Warehouse Stutter Kit.adg | query:Drums#FileId_5352 |
| Yakiman Kit.adg | query:Drums#FileId_5404 |

### Drum Hits (17 subfolders, ~2,271 one-shots)
Path: `Drums/Drum Hits/<Subfolder>`. URI pattern: `query:Drums#Drum%20Hits:<Subfolder>:FileId_NNNN` (spaces in subfolder names are `%20`, e.g. `FX%20Hit`, `Misc%20Percussion`).
Loading a single hit URI with load_instrument_or_effect puts it in a Simpler on the track. Naming convention across all folders: `<Type> <Machine|Character|Pack> [N].wav|aif`. Machine tokens: 505, 606, 707, 808, 909, C78, DMX, LD, ER, MPC, SP. Pack tokens: DECAP, LDre, Taka, BNYX, Fenk, RKTD, Vinyl, Acoustified, Dry Session, Vintage, Gen Purpose, Plymouth, Yakiman, Mad Skill, Slackjaw, Pete, Ironman.

| Subfolder | Count | FileId range |
|---|---|---|
| Kick | 360 | 1862–2221 |
| Snare | 356 | (see below) |
| Hihat | 383 | (see below) |
| Tom | 326 | (see below) |
| Misc Percussion | 244 | (see below) |
| FX Hit | 137 | 692–739, 2607–2690, 3844–3848 |
| Clap | 111 | 2937–3049 |
| Rim | 98 | 1593–1690 |
| Cymbal | 86 | 2801–2886 |
| Shaker | 70 | 1522–1591 |
| Bell | 69 | 3066–3134 |
| Ride | 69 | 1692–1760 |
| Wood | 55 | 742–796 |
| Conga | 47 | 2888–2935 |
| Tambourine | 32 | 1132–1163 |
| Bongo | 14 | 3051–3064 |
| Timbales | 4 | 1127–1130 |

#### Kick — 360 items (aif/wav); 211 naming families
URI pattern: `query:Drums#Drum%20Hits:Kick:FileId_NNNN`

| Family (count) | Representative name → URI |
|---|---|
| Kick Vinyl * (32) | Kick Vinyl 45 1.wav → `query:Drums#Drum%20Hits:Kick:FileId_2182`<br>Kick Vinyl DLD 2.wav → `query:Drums#Drum%20Hits:Kick:FileId_2192`<br>Kick Vinyl SP 3.wav → `query:Drums#Drum%20Hits:Kick:FileId_2205`<br>Kick Vinyl Sub.wav → `query:Drums#Drum%20Hits:Kick:FileId_2213` |
| Kick 808 * (14) | Kick 808 1.aif → `query:Drums#Drum%20Hits:Kick:FileId_1877`<br>Kick 808 DMX.wav → `query:Drums#Drum%20Hits:Kick:FileId_1880`<br>Kick 808 Reverse Thud.wav → `query:Drums#Drum%20Hits:Kick:FileId_1886`<br>Kick 808 Tone.aif → `query:Drums#Drum%20Hits:Kick:FileId_1890` |
| Kick LDre * (10) | Kick LDre 1.wav → `query:Drums#Drum%20Hits:Kick:FileId_2039`<br>Kick LDre 4.wav → `query:Drums#Drum%20Hits:Kick:FileId_2043`<br>Kick LDre 7.wav → `query:Drums#Drum%20Hits:Kick:FileId_2046`<br>Kick LDre 10.wav → `query:Drums#Drum%20Hits:Kick:FileId_2040` |
| Kick Sub * (9) | Kick Sub 808 Long A1.wav → `query:Drums#Drum%20Hits:Kick:FileId_2146`<br>Kick Sub Abyss.wav → `query:Drums#Drum%20Hits:Kick:FileId_2149`<br>Kick Sub Shine.wav → `query:Drums#Drum%20Hits:Kick:FileId_2152`<br>Kick Sub Wool.wav → `query:Drums#Drum%20Hits:Kick:FileId_2154` |
| Kick 909 * (8) | Kick 909 1.aif → `query:Drums#Drum%20Hits:Kick:FileId_1893`<br>Kick 909 Click Layer.wav → `query:Drums#Drum%20Hits:Kick:FileId_1895`<br>Kick 909 DMX LX.wav → `query:Drums#Drum%20Hits:Kick:FileId_1898`<br>Kick 909 Prommer.wav → `query:Drums#Drum%20Hits:Kick:FileId_1900` |
| Kick Taka * (7) | Kick Taka Cut Thru.wav → `query:Drums#Drum%20Hits:Kick:FileId_2160`<br>Kick Taka Hollow.wav → `query:Drums#Drum%20Hits:Kick:FileId_2162`<br>Kick Taka School.wav → `query:Drums#Drum%20Hits:Kick:FileId_2164`<br>Kick Taka Zulu.wav → `query:Drums#Drum%20Hits:Kick:FileId_2166` |
| Kick Felt * (5) | Kick Felt Crack.wav → `query:Drums#Drum%20Hits:Kick:FileId_2004`<br>Kick Felt Hard Dry Session.aif → `query:Drums#Drum%20Hits:Kick:FileId_2005`<br>Kick Felt Soft Dry Session.aif → `query:Drums#Drum%20Hits:Kick:FileId_2007`<br>Kick Felt Yester Years.aif → `query:Drums#Drum%20Hits:Kick:FileId_2008` |
| Kick Short * (5) | Kick Short and Prune.wav → `query:Drums#Drum%20Hits:Kick:FileId_2116`<br>Kick Short and Solid 1.wav → `query:Drums#Drum%20Hits:Kick:FileId_2117`<br>Kick Short Breath.wav → `query:Drums#Drum%20Hits:Kick:FileId_2114`<br>Kick Short Solid Blau.wav → `query:Drums#Drum%20Hits:Kick:FileId_2115` |
| Kick * (4) | Kick 007.aif → `query:Drums#Drum%20Hits:Kick:FileId_1862`<br>Kick 030.wav → `query:Drums#Drum%20Hits:Kick:FileId_1863`<br>Kick 505.aif → `query:Drums#Drum%20Hits:Kick:FileId_1868` |
| Kick 70s * (4) | Kick 70s 1.wav → `query:Drums#Drum%20Hits:Kick:FileId_1873`<br>Kick 70s 2.wav → `query:Drums#Drum%20Hits:Kick:FileId_1874`<br>Kick 70s 3.wav → `query:Drums#Drum%20Hits:Kick:FileId_1875` |
| Kick Alien * (4) | Kick Alien Fash.wav → `query:Drums#Drum%20Hits:Kick:FileId_1905`<br>Kick Alien Spawn 1.wav → `query:Drums#Drum%20Hits:Kick:FileId_1906`<br>Kick Alien Spawn 2.wav → `query:Drums#Drum%20Hits:Kick:FileId_1907` |
| Kick Black * (4) | Kick Black Bread.wav → `query:Drums#Drum%20Hits:Kick:FileId_1928`<br>Kick Black Diamond.wav → `query:Drums#Drum%20Hits:Kick:FileId_1929`<br>Kick Black Hole 1.wav → `query:Drums#Drum%20Hits:Kick:FileId_1930` |
| Kick Hat * (4) | Kick Hat Combo Clatter.wav → `query:Drums#Drum%20Hits:Kick:FileId_2022`<br>Kick Hat Combo Dirty.aif → `query:Drums#Drum%20Hits:Kick:FileId_2023`<br>Kick Hat Feel.wav → `query:Drums#Drum%20Hits:Kick:FileId_2024` |
| Kick Plastic * (4) | Kick Plastic 90s Heavy Rock.wav → `query:Drums#Drum%20Hits:Kick:FileId_2080`<br>Kick Plastic Hard Bright Room.aif → `query:Drums#Drum%20Hits:Kick:FileId_2081`<br>Kick Plastic Open Mid Tuned.wav → `query:Drums#Drum%20Hits:Kick:FileId_2082` |
| Kick 90s * (3) | Kick 90s 1.wav → `query:Drums#Drum%20Hits:Kick:FileId_1901`<br>Kick 90s 2.wav → `query:Drums#Drum%20Hits:Kick:FileId_1902`<br>Kick 90s 3.wav → `query:Drums#Drum%20Hits:Kick:FileId_1903` |
| Kick Analog * (3) | Kick Analog 1.aif → `query:Drums#Drum%20Hits:Kick:FileId_1912`<br>Kick Analog 2.aif → `query:Drums#Drum%20Hits:Kick:FileId_1913`<br>Kick Analog Skitter.aif → `query:Drums#Drum%20Hits:Kick:FileId_1914` |
| Kick Burst * (3) | Kick Burst 1.aif → `query:Drums#Drum%20Hits:Kick:FileId_1943`<br>Kick Burst 2.aif → `query:Drums#Drum%20Hits:Kick:FileId_1944`<br>Kick Burst 3.aif → `query:Drums#Drum%20Hits:Kick:FileId_1945` |
| Kick DECAP * (3) | Kick DECAP 1.wav → `query:Drums#Drum%20Hits:Kick:FileId_1966`<br>Kick DECAP 2.wav → `query:Drums#Drum%20Hits:Kick:FileId_1967`<br>Kick DECAP 3.wav → `query:Drums#Drum%20Hits:Kick:FileId_1968` |
| Kick Electronic * (3) | Kick Electronic 1.aif → `query:Drums#Drum%20Hits:Kick:FileId_1994`<br>Kick Electronic 2.aif → `query:Drums#Drum%20Hits:Kick:FileId_1995`<br>Kick Electronic.aif → `query:Drums#Drum%20Hits:Kick:FileId_1996` |
| Kick ER * (3) | Kick ER Fenk 1.wav → `query:Drums#Drum%20Hits:Kick:FileId_1990`<br>Kick ER Fenk 2.aif → `query:Drums#Drum%20Hits:Kick:FileId_1991`<br>Kick ER Fenk.wav → `query:Drums#Drum%20Hits:Kick:FileId_1992` |
| Kick Ring * (3) | Kick Ring Click Fenk.wav → `query:Drums#Drum%20Hits:Kick:FileId_2098`<br>Kick Ring ER.wav → `query:Drums#Drum%20Hits:Kick:FileId_2099`<br>Kick Ring Master.wav → `query:Drums#Drum%20Hits:Kick:FileId_2100` |
| Kick Sine * (3) | Kick Sine Me Up.wav → `query:Drums#Drum%20Hits:Kick:FileId_2121`<br>Kick Sine Slope Gentle.wav → `query:Drums#Drum%20Hits:Kick:FileId_2122`<br>Kick Sine.aif → `query:Drums#Drum%20Hits:Kick:FileId_2123` |
| Other multi-item families (29) | Kick Skin (3), Kick Solid (3), Kick Stereo (3), Kick Synth (3), Kick 49 (2), Kick 80s (2), Kick 505 (2), Kick 707 (2), Kick BNYX (2), Kick Burned (2), Kick Dark (2), Kick Dirt (2), Kick Distorted (2), Kick DM (2), Kick DMX (2), Kick Drum (2), Kick Funky (2), Kick Jungle (2), Kick Layered (2), Kick Low (2), Kick Machine (2), Kick Partial (2), Kick RKTD (2), Kick Slam (2), Kick Slappy (2), Kick SW (2), Kick Thud (2), Kick Tight (2), Kick Tiny (2) |
| One-off names (160) | Kick 606 Mod.wav → `query:Drums#Drum%20Hits:Kick:FileId_1869`<br>Kick Buzzy Bang.wav → `query:Drums#Drum%20Hits:Kick:FileId_1947`<br>Kick Door.aif → `query:Drums#Drum%20Hits:Kick:FileId_1986`<br>Kick In The Room.wav → `query:Drums#Drum%20Hits:Kick:FileId_2031`<br>Kick Pesozoan.wav → `query:Drums#Drum%20Hits:Kick:FileId_2078`<br>Kick Shuffle.wav → `query:Drums#Drum%20Hits:Kick:FileId_2119`<br>All: Kick 606 Mod, Kick Acoustic Room, Kick All In, Kick Amber, Kick Amethyst, Kick Ascend, Kick Atmos, Kick Aurora, Kick Aztec, Kick Bam Vin, Kick Barrel Bop, Kick Beat, Kick Beats, Kick Beryl, Kick Bghn, Kick Big Sine, Kick Blitzen, Kick Blue Room, Kick Bluesbreak, Kick Blunt, Kick Bonk, Kick Boot, Kick Bricks, Kick Build 4, Kick Bull, Kick Buss Ride, Kick Buzzy Bang, Kick C78, Kick Caltroit, Kick Calypso, Kick Can, Kick Charred, Kick Chatt, Kick Cigs, Kick Click Layer Real Drum, Kick Cockpit, Kick Code 1, Kick Combo Burned, Kick Conga Weback, Kick Constant, Kick Crash Combo, Kick Creh, Kick Crush Master, Kick Crystal Wires, Kick Cyanide, Kick Deep 3k, Kick Delta, Kick Disco Mars, Kick Distort, Kick Dizzy, Kick Doctor M, Kick Doom Dungeon, Kick Door, Kick Dump, Kick Electrified, Kick Endorphin, Kick Evidence, Kick Factory, Kick Fat Matt Break, Kick Featherhead, Kick Feel, Kick Fishnet, Kick Flabby, Kick Flat Noise, Kick FM Bass, Kick Foot Late Nite, Kick Future Proof, Kick Gambling, Kick Garage, Kick Gawgeous, Kick Gin, Kick Grit, Kick Hard Vapour, Kick Heavy, Kick Hed Deck, Kick Horsen, Kick Hundred, Kick Impact, Kick In The Room, Kick Ironman, Kick Jazz 8, Kick Jollyvilles, Kick Lazers, Kick LD, Kick LDW Plymouth, Kick Leaner, Kick Leftover, Kick Logical, Kick Mach, Kick Mad Skill, Kick Mainz, Kick Marching Drum, Kick Maschine, Kick Micronoi, Kick Moldy, Kick Mood Board, Kick Muffled Feel, Kick Mule Hit, Kick Numerology, Kick Old Tool, Kick Open Hat Combo, Kick Oracle, Kick Overdrive Siner, Kick Overdrop, Kick Pesozoan, Kick Pete, Kick Popped Noise, Kick Post Flash, Kick Processed, Kick PT Vinyl, Kick Punch, Kick Push It, Kick Rattle, Kick Reentry, Kick Remo, Kick Rerubbed Punch, Kick Resobully, Kick Reverse Bghn, Kick Riddim, Kick Rock MPC, Kick Room Bang, Kick Rounded Impact, Kick Rumble, Kick S2, Kick Sampled Basic, Kick Saturated, Kick Sci Fi, Kick Seeing Daisies, Kick Shadow, Kick Shoreline, Kick Shuffle, Kick Simple Tone, Kick Slackjaw, Kick Slow, Kick Smacky, Kick Smooth Punt, Kick Soap Box Slap, Kick Source, Kick Space Man Cig, Kick Spacey, Kick Strong Build, Kick Tailed, Kick Tamb Combo, Kick The Duke, Kick Titan, Kick TL, Kick Topaz, Kick Trim Down, Kick Twang, Kick Twenty-Two, Kick V2, Kick Victor, Kick Volt, Kick Whim, Kick Wolomp, Kick Wood, Kick XDFG, Kick XYXY, Kick Yesteryear, Kick Yolo |

#### Snare — 356 items (aif/wav); 192 naming families
URI pattern: `query:Drums#Drum%20Hits:Snare:FileId_NNNN`

| Family (count) | Representative name → URI |
|---|---|
| Snare Vinyl * (28) | Snare Vinyl 01.wav → `query:Drums#Drum%20Hits:Snare:FileId_1485`<br>Snare Vinyl 10.wav → `query:Drums#Drum%20Hits:Snare:FileId_1494`<br>Snare Vinyl DLB 2.wav → `query:Drums#Drum%20Hits:Snare:FileId_1503`<br>Snare Vinyl Slap.wav → `query:Drums#Drum%20Hits:Snare:FileId_1512` |
| Snare Stick * (17) | Snare Stick Hit 1.wav → `query:Drums#Drum%20Hits:Snare:FileId_1436`<br>Snare Stick Hit Hard British Vintage.aif → `query:Drums#Drum%20Hits:Snare:FileId_1441`<br>Snare Stick Hit Rim 2 Dry Session.aif → `query:Drums#Drum%20Hits:Snare:FileId_1447`<br>Snare Stick Rim L Yester Years.aif → `query:Drums#Drum%20Hits:Snare:FileId_1452` |
| Snare 808 * (8) | Snare 808 2.wav → `query:Drums#Drum%20Hits:Snare:FileId_1180`<br>Snare 808 4.wav → `query:Drums#Drum%20Hits:Snare:FileId_1182`<br>Snare 808 Tite.aif → `query:Drums#Drum%20Hits:Snare:FileId_1185`<br>Snare 808 Tone 11.aif → `query:Drums#Drum%20Hits:Snare:FileId_1187` |
| Snare 909 * (8) | Snare 909 DMX.wav → `query:Drums#Drum%20Hits:Snare:FileId_1191`<br>Snare 909 Hard 2.wav → `query:Drums#Drum%20Hits:Snare:FileId_1193`<br>Snare 909 Tune 8.wav → `query:Drums#Drum%20Hits:Snare:FileId_1198`<br>Snare 909 Tune 10s.aif → `query:Drums#Drum%20Hits:Snare:FileId_1196` |
| Snare 70s * (7) | Snare 70s Funk MPC.wav → `query:Drums#Drum%20Hits:Snare:FileId_1173`<br>Snare 70s MPC 2.wav → `query:Drums#Drum%20Hits:Snare:FileId_1175`<br>Snare 70s MPC 4.wav → `query:Drums#Drum%20Hits:Snare:FileId_1177`<br>Snare 70s Vinyl.wav → `query:Drums#Drum%20Hits:Snare:FileId_1179` |
| Snare Mkit * (7) | Snare Mkit Sample 2.wav → `query:Drums#Drum%20Hits:Snare:FileId_1374`<br>Snare Mkit Sample 4.wav → `query:Drums#Drum%20Hits:Snare:FileId_1377`<br>Snare Mkit Sample 9.wav → `query:Drums#Drum%20Hits:Snare:FileId_1379`<br>Snare Mkit Synth 5.wav → `query:Drums#Drum%20Hits:Snare:FileId_1380` |
| Snare Taka * (7) | Snare Taka Cracker.wav → `query:Drums#Drum%20Hits:Snare:FileId_1462`<br>Snare Taka Money.wav → `query:Drums#Drum%20Hits:Snare:FileId_1464`<br>Snare Taka Rude.wav → `query:Drums#Drum%20Hits:Snare:FileId_1466`<br>Snare Taka Sticky.wav → `query:Drums#Drum%20Hits:Snare:FileId_1468` |
| Snare Clap * (6) | Snare Clap Back.wav → `query:Drums#Drum%20Hits:Snare:FileId_1243`<br>Snare Clap Days Off.wav → `query:Drums#Drum%20Hits:Snare:FileId_1245`<br>Snare Clap Dog.wav → `query:Drums#Drum%20Hits:Snare:FileId_1247`<br>Snare Clap Snap Combo.wav → `query:Drums#Drum%20Hits:Snare:FileId_1248` |
| Snare DECAP * (6) | Snare DECAP 1.wav → `query:Drums#Drum%20Hits:Snare:FileId_1263`<br>Snare DECAP 3.wav → `query:Drums#Drum%20Hits:Snare:FileId_1265`<br>Snare DECAP 5.wav → `query:Drums#Drum%20Hits:Snare:FileId_1267`<br>Snare DECAP 6.wav → `query:Drums#Drum%20Hits:Snare:FileId_1268` |
| Snare LDre * (6) | Snare LDre 1.wav → `query:Drums#Drum%20Hits:Snare:FileId_1340`<br>Snare LDre 3.wav → `query:Drums#Drum%20Hits:Snare:FileId_1342`<br>Snare LDre 5.wav → `query:Drums#Drum%20Hits:Snare:FileId_1344`<br>Snare LDre 6.wav → `query:Drums#Drum%20Hits:Snare:FileId_1345` |
| Snare Short * (6) | Snare Short And Solid.wav → `query:Drums#Drum%20Hits:Snare:FileId_1415`<br>Snare Short Machine.aif → `query:Drums#Drum%20Hits:Snare:FileId_1417`<br>Snare Short Trap.aif → `query:Drums#Drum%20Hits:Snare:FileId_1419`<br>Snare Short.aif → `query:Drums#Drum%20Hits:Snare:FileId_1420` |
| Snare Acoustic * (5) | Snare Acoustic Crystal.aif → `query:Drums#Drum%20Hits:Snare:FileId_1201`<br>Snare Acoustic Nightly.aif → `query:Drums#Drum%20Hits:Snare:FileId_1202`<br>Snare Acoustic Quark 2.aif → `query:Drums#Drum%20Hits:Snare:FileId_1204`<br>Snare Acoustic.aif → `query:Drums#Drum%20Hits:Snare:FileId_1205` |
| Snare Jungle * (5) | Snare Jungle 1 SP1200R.wav → `query:Drums#Drum%20Hits:Snare:FileId_1331`<br>Snare Jungle 2 SP1200R.wav → `query:Drums#Drum%20Hits:Snare:FileId_1332`<br>Snare Jungle Skitter.aif → `query:Drums#Drum%20Hits:Snare:FileId_1334`<br>Snare Jungle.aif → `query:Drums#Drum%20Hits:Snare:FileId_1335` |
| Snare Lot * (5) | Snare Lot 1.wav → `query:Drums#Drum%20Hits:Snare:FileId_1355`<br>Snare Lot 2.wav → `query:Drums#Drum%20Hits:Snare:FileId_1356`<br>Snare Lot 4.wav → `query:Drums#Drum%20Hits:Snare:FileId_1358`<br>Snare Lot Roll.wav → `query:Drums#Drum%20Hits:Snare:FileId_1359` |
| Snare * (4) | Snare 505.aif → `query:Drums#Drum%20Hits:Snare:FileId_1169`<br>Snare 606.aif → `query:Drums#Drum%20Hits:Snare:FileId_1170`<br>Snare 707.wav → `query:Drums#Drum%20Hits:Snare:FileId_1172` |
| Snare DMX * (4) | Snare DMX A1.wav → `query:Drums#Drum%20Hits:Snare:FileId_1269`<br>Snare DMX Analog.wav → `query:Drums#Drum%20Hits:Snare:FileId_1270`<br>Snare DMX Core.wav → `query:Drums#Drum%20Hits:Snare:FileId_1271` |
| Snare Mad * (4) | Snare Mad Skill 1.aif → `query:Drums#Drum%20Hits:Snare:FileId_1364`<br>Snare Mad Skill 2.aif → `query:Drums#Drum%20Hits:Snare:FileId_1365`<br>Snare Mad Skill 3.wav → `query:Drums#Drum%20Hits:Snare:FileId_1366` |
| Snare Mars * (4) | Snare Mars Disco 1.wav → `query:Drums#Drum%20Hits:Snare:FileId_1368`<br>Snare Mars Disco 2.wav → `query:Drums#Drum%20Hits:Snare:FileId_1369`<br>Snare Mars Disco 3.wav → `query:Drums#Drum%20Hits:Snare:FileId_1370` |
| Snare BNYX * (3) | Snare BNYX High.wav → `query:Drums#Drum%20Hits:Snare:FileId_1209`<br>Snare BNYX Low.wav → `query:Drums#Drum%20Hits:Snare:FileId_1210`<br>Snare BNYX South.wav → `query:Drums#Drum%20Hits:Snare:FileId_1211` |
| Snare Combo * (3) | Snare Combo Grounded.wav → `query:Drums#Drum%20Hits:Snare:FileId_1251`<br>Snare Combo Right.aif → `query:Drums#Drum%20Hits:Snare:FileId_1252`<br>Snare Combo Segamega.wav → `query:Drums#Drum%20Hits:Snare:FileId_1253` |
| Snare eGrit * (3) | Snare eGrit Low.wav → `query:Drums#Drum%20Hits:Snare:FileId_1518`<br>Snare eGrit Tones 2.wav → `query:Drums#Drum%20Hits:Snare:FileId_1519`<br>Snare eGrit Tones 3.wav → `query:Drums#Drum%20Hits:Snare:FileId_1520` |
| Snare Fat * (3) | Snare Fat Hand Drummer.wav → `query:Drums#Drum%20Hits:Snare:FileId_1288`<br>Snare Fat Matt Break 1.wav → `query:Drums#Drum%20Hits:Snare:FileId_1289`<br>Snare Fat Matt Break 2.wav → `query:Drums#Drum%20Hits:Snare:FileId_1290` |
| Other multi-item families (29) | Snare Gen (3), Snare Hat (3), Snare Heavy (3), Snare Noise (3), Snare Prommer (3), Snare Rim (3), Snare RKTD (3), Snare Roll (3), Snare 80s (2), Snare 90s (2), Snare BlackHole (2), Snare Bluesbreak (2), Snare Crack (2), Snare Dry (2), Snare Frogger (2), Snare Funk (2), Snare Future (2), Snare Grit (2), Snare Hot (2), Snare Impact (2), Snare Loose (2), Snare Low (2), Snare Phive (2), Snare RK (2), Snare Soft (2), Snare Trap (2), Snare Verb (2), Snare Vintage (2), Snare Yesteryear (2) |
| One-off names (141) | Snare 3k Hiss.wav → `query:Drums#Drum%20Hits:Snare:FileId_1166`<br>Snare Buss Ride.wav → `query:Drums#Drum%20Hits:Snare:FileId_1231`<br>Snare Dirtbags.wav → `query:Drums#Drum%20Hits:Snare:FileId_1275`<br>Snare High Strung.wav → `query:Drums#Drum%20Hits:Snare:FileId_1320`<br>Snare Nois.wav → `query:Drums#Drum%20Hits:Snare:FileId_1382`<br>Snare Snipp.aif → `query:Drums#Drum%20Hits:Snare:FileId_1430`<br>All: Snare 3k Hiss, Snare 4 A Ride, Snare 12 Bit, Snare 505 ASR, Snare 707 Variation, Snare Air Lock, Snare Alien Spawn, Snare Azimuth, Snare Baker, Snare BamVin, Snare Bandroom, Snare Beaded Up, Snare Belly Ring, Snare Biz, Snare Bizzness SP1200R, Snare Block Snare, Snare Blue Room, Snare Bottom Mic Plymouth, Snare Box Slap, Snare Breeze, Snare Brick, Snare Brush Hit Hard Club Sizzle, Snare Build, Snare Buss Ride, Snare Butta Soft, Snare C78, Snare Cable Car, Snare Caked, Snare Canon, Snare Celebrate, Snare Cereal Factory, Snare Charred, Snare Chop, Snare Chrome Mono, Snare Chronicle, Snare Clapper, Snare Classic Canvas, Snare Crackle Basket, Snare Crispi, Snare Crispy, Snare Crunch Squeeze, Snare Cryptic, Snare Cust, Snare Daisies, Snare Damp Stick Center, Snare DC Snare, Snare Dirtbags, Snare Double Slackjaw, Snare Dram, Snare Dream, Snare Dubbers, Snare Dubplate, Snare Edged, Snare Electrified, Snare Emanation, Snare Endtro, Snare Ewtery, Snare Feel, Snare Film With Gatlope, Snare Flaxe, Snare Full House, Snare Funky Moon, Snare Gated Verb, Snare Geomatrix, Snare GrainUrs DnB, Snare Gram, Snare Grounded, Snare Gym, Snare Hard Source, Snare High Strung, Snare Hit Crack, Snare Ironman, Snare Issued, Snare IzoVinyl, Snare Jazz, Snare Jethro, Snare Keep Tight, Snare Kind, Snare Kindified, Snare Laser Blip, Snare Layered End Game, Snare LD, Snare Ldw, Snare Leaner, Snare Leedy, Snare Little DM, Snare Loki, Snare Machine, Snare Melba Toast, Snare Mighty Bit Reduce, Snare Modular 3, Snare MPL FX, Snare Nois, Snare Oddities Squash, Snare On Your Mark, Snare Perc Combo, Snare Pete, Snare Rattle, Snare ReEntry, Snare Reverb, Snare Ro-Fli, Snare Rolling, Snare Room, Snare Rubber Duck, Snare Ruff, Snare Shake It Kind Of, Snare Shuffle, Snare Sidestick YMA, Snare Skin Only, Snare Slackjaw, Snare Small Slap, Snare Smoke, Snare Snabbis, Snare Snapalappa, Snare Snappy Wood, Snare Snipp, Snare Stacked, Snare Stackery, Snare Stew, Snare Street, Snare Strike Kindified, Snare Strong, Snare Subsnare, Snare Succinct, Snare Support, Snare Swisher, Snare Synth, Snare Tam Tam, Snare Tambo Ironman, Snare Thin Smack, Snare Tight Rim, Snare Time Warp, Snare Tommy, Snare TRS, Snare TurntableTrick, Snare Tweed, Snare Umbra, Snare VB, Snare Wingman, Snare Wood Combo Hoosier, Snare Zombie 80s |

#### Hihat — 383 items (aif/wav); 6 naming families
URI pattern: `query:Drums#Drum%20Hits:Hihat:FileId_NNNN`

| Family (count) | Representative name → URI |
|---|---|
| Hihat Closed * (245) | Hihat Closed 2B.aif → `query:Drums#Drum%20Hits:Hihat:FileId_2223`<br>Hihat Closed Echo.wav → `query:Drums#Drum%20Hits:Hihat:FileId_2310`<br>Hihat Closed Plymouth 1.wav → `query:Drums#Drum%20Hits:Hihat:FileId_2386`<br>Hihat Closed Yolo Soft.wav → `query:Drums#Drum%20Hits:Hihat:FileId_2467` |
| Hihat Open * (123) | Hihat Open 53 TL.wav → `query:Drums#Drum%20Hits:Hihat:FileId_2485`<br>Hihat Open Drill.aif → `query:Drums#Drum%20Hits:Hihat:FileId_2522`<br>Hihat Open Peace Corp.wav → `query:Drums#Drum%20Hits:Hihat:FileId_2563`<br>Hihat Open Window.wav → `query:Drums#Drum%20Hits:Hihat:FileId_2603` |
| Hihat Foot * (6) | Hihat Foot Acoustic.aif → `query:Drums#Drum%20Hits:Hihat:FileId_2469`<br>Hihat Foot Hard.aif → `query:Drums#Drum%20Hits:Hihat:FileId_2471`<br>Hihat Foot Taka.wav → `query:Drums#Drum%20Hits:Hihat:FileId_2473`<br>Hihat Foot West Coast Band.wav → `query:Drums#Drum%20Hits:Hihat:FileId_2474` |
| Hihat Half-Open * (5) | Hihat Half-Open Stick Shank Yester Years.aif → `query:Drums#Drum%20Hits:Hihat:FileId_2478`<br>Hihat Half-Open Stick Tip Hard 1.aif → `query:Drums#Drum%20Hits:Hihat:FileId_2479`<br>Hihat Half-Open Stick Tip Soft 1.aif → `query:Drums#Drum%20Hits:Hihat:FileId_2481`<br>Hihat Half-Open Stick Tip Soft 2.aif → `query:Drums#Drum%20Hits:Hihat:FileId_2482` |
| Hihat Half * (3) | Hihat Half Open 1.aif → `query:Drums#Drum%20Hits:Hihat:FileId_2475`<br>Hihat Half Open 2.aif → `query:Drums#Drum%20Hits:Hihat:FileId_2476`<br>Hihat Half Open.wav → `query:Drums#Drum%20Hits:Hihat:FileId_2477` |
| One-off names (1) | Hihat Combo 606.aif → `query:Drums#Drum%20Hits:Hihat:FileId_2468`<br>All: Hihat Combo 606 |

#### Tom — 326 items (aif/wav); 99 naming families
URI pattern: `query:Drums#Drum%20Hits:Tom:FileId_NNNN`

| Family (count) | Representative name → URI |
|---|---|
| Tom 909 * (22) | Tom 909 DMX.wav → `query:Drums#Drum%20Hits:Tom:FileId_837`<br>Tom 909 Low Alt.wav → `query:Drums#Drum%20Hits:Tom:FileId_844`<br>Tom 909 Mid K.wav → `query:Drums#Drum%20Hits:Tom:FileId_851`<br>Tom 909 Tran 5.wav → `query:Drums#Drum%20Hits:Tom:FileId_858` |
| Tom Stick * (17) | Tom Stick Hit Hard Bright Room 12.aif → `query:Drums#Drum%20Hits:Tom:FileId_1083`<br>Tom Stick Hit Hard Dry Session 10.aif → `query:Drums#Drum%20Hits:Tom:FileId_1088`<br>Tom Stick Hit L Yester Years 11.aif → `query:Drums#Drum%20Hits:Tom:FileId_1094`<br>Tom Stick Hit Soft Dry Session 16.aif → `query:Drums#Drum%20Hits:Tom:FileId_1099` |
| Tom 808 * (15) | Tom 808 DMX.wav → `query:Drums#Drum%20Hits:Tom:FileId_816`<br>Tom 808 Low DMX.wav → `query:Drums#Drum%20Hits:Tom:FileId_821`<br>Tom 808 Mid.aif → `query:Drums#Drum%20Hits:Tom:FileId_826`<br>Tom 808 PEQ 4.wav → `query:Drums#Drum%20Hits:Tom:FileId_830` |
| Tom DMX * (15) | Tom DMX Analog 1.wav → `query:Drums#Drum%20Hits:Tom:FileId_908`<br>Tom DMX Fatso 3.wav → `query:Drums#Drum%20Hits:Tom:FileId_913`<br>Tom DMX Hi 2.wav → `query:Drums#Drum%20Hits:Tom:FileId_918`<br>Tom DMX Low 3.wav → `query:Drums#Drum%20Hits:Tom:FileId_922` |
| Tom Low * (13) | Tom Low Acoustic.wav → `query:Drums#Drum%20Hits:Tom:FileId_982`<br>Tom Low DMX Tonic.wav → `query:Drums#Drum%20Hits:Tom:FileId_986`<br>Tom Low Machine.wav → `query:Drums#Drum%20Hits:Tom:FileId_990`<br>Tom Low Taka School.wav → `query:Drums#Drum%20Hits:Tom:FileId_994` |
| Tom Mid * (13) | Tom Mid Acoustic Light.wav → `query:Drums#Drum%20Hits:Tom:FileId_1012`<br>Tom Mid Bullets.wav → `query:Drums#Drum%20Hits:Tom:FileId_1016`<br>Tom Mid Electronic.aif → `query:Drums#Drum%20Hits:Tom:FileId_1020`<br>Tom Mid Mad Skill 2.aif → `query:Drums#Drum%20Hits:Tom:FileId_1024` |
| Tom RKTD * (10) | Tom RKTD 1.wav → `query:Drums#Drum%20Hits:Tom:FileId_1042`<br>Tom RKTD 4.wav → `query:Drums#Drum%20Hits:Tom:FileId_1045`<br>Tom RKTD 7.wav → `query:Drums#Drum%20Hits:Tom:FileId_1048`<br>Tom RKTD.wav → `query:Drums#Drum%20Hits:Tom:FileId_1051` |
| Tom MKS * (8) | Tom MKS 1.wav → `query:Drums#Drum%20Hits:Tom:FileId_1000`<br>Tom MKS 3.wav → `query:Drums#Drum%20Hits:Tom:FileId_1002`<br>Tom MKS 6.wav → `query:Drums#Drum%20Hits:Tom:FileId_1005`<br>Tom MKS 8.wav → `query:Drums#Drum%20Hits:Tom:FileId_1007` |
| Tom Analog * (7) | Tom Analog 1.aif → `query:Drums#Drum%20Hits:Tom:FileId_868`<br>Tom Analog 3.aif → `query:Drums#Drum%20Hits:Tom:FileId_870`<br>Tom Analog 5.aif → `query:Drums#Drum%20Hits:Tom:FileId_872`<br>Tom Analog Drop.aif → `query:Drums#Drum%20Hits:Tom:FileId_874` |
| Tom 80s * (6) | Tom 80s Low.aif → `query:Drums#Drum%20Hits:Tom:FileId_831`<br>Tom 80s Space Craft 1.wav → `query:Drums#Drum%20Hits:Tom:FileId_833`<br>Tom 80s Space Craft 3.wav → `query:Drums#Drum%20Hits:Tom:FileId_835`<br>Tom 80s Space Craft 4.wav → `query:Drums#Drum%20Hits:Tom:FileId_836` |
| Tom 505 * (6) | Tom 505 ASR 1.wav → `query:Drums#Drum%20Hits:Tom:FileId_800`<br>Tom 505 ASR 3.wav → `query:Drums#Drum%20Hits:Tom:FileId_802`<br>Tom 505 Low.aif → `query:Drums#Drum%20Hits:Tom:FileId_804`<br>Tom 505 Mid.aif → `query:Drums#Drum%20Hits:Tom:FileId_805` |
| Tom B * (6) | Tom B SP 1.wav → `query:Drums#Drum%20Hits:Tom:FileId_875`<br>Tom B SP 3.wav → `query:Drums#Drum%20Hits:Tom:FileId_877`<br>Tom B SP 5.wav → `query:Drums#Drum%20Hits:Tom:FileId_879`<br>Tom B SP 6.wav → `query:Drums#Drum%20Hits:Tom:FileId_880` |
| Tom ED10 * (6) | Tom ED10 Fat 1.wav → `query:Drums#Drum%20Hits:Tom:FileId_930`<br>Tom ED10 Fat 3.wav → `query:Drums#Drum%20Hits:Tom:FileId_932`<br>Tom ED10 Fat 5.wav → `query:Drums#Drum%20Hits:Tom:FileId_934`<br>Tom ED10 Fat 6.wav → `query:Drums#Drum%20Hits:Tom:FileId_935` |
| Tom Electronic * (6) | Tom Electronic SP 1.wav → `query:Drums#Drum%20Hits:Tom:FileId_940`<br>Tom Electronic SP 3.wav → `query:Drums#Drum%20Hits:Tom:FileId_942`<br>Tom Electronic SP 5.wav → `query:Drums#Drum%20Hits:Tom:FileId_944`<br>Tom Electronic.aif → `query:Drums#Drum%20Hits:Tom:FileId_945` |
| Tom High * (6) | Tom High Bullets.wav → `query:Drums#Drum%20Hits:Tom:FileId_963`<br>Tom High Crack.wav → `query:Drums#Drum%20Hits:Tom:FileId_965`<br>Tom High Gen Purpose.aif → `query:Drums#Drum%20Hits:Tom:FileId_967`<br>Tom High Rough.wav → `query:Drums#Drum%20Hits:Tom:FileId_968` |
| Tom SP * (6) | Tom SP 1.wav → `query:Drums#Drum%20Hits:Tom:FileId_1071`<br>Tom SP 3.wav → `query:Drums#Drum%20Hits:Tom:FileId_1073`<br>Tom SP 5.wav → `query:Drums#Drum%20Hits:Tom:FileId_1075`<br>Tom SP 6.wav → `query:Drums#Drum%20Hits:Tom:FileId_1076` |
| Tom R100 * (5) | Tom R100 Clean 1.wav → `query:Drums#Drum%20Hits:Tom:FileId_1036`<br>Tom R100 Clean 2.wav → `query:Drums#Drum%20Hits:Tom:FileId_1037`<br>Tom R100 Electronic 2.wav → `query:Drums#Drum%20Hits:Tom:FileId_1039`<br>Tom R100 Electronic 3.wav → `query:Drums#Drum%20Hits:Tom:FileId_1040` |
| Tom Rudebot * (5) | Tom Rudebot High Mid.wav → `query:Drums#Drum%20Hits:Tom:FileId_1066`<br>Tom Rudebot High.wav → `query:Drums#Drum%20Hits:Tom:FileId_1067`<br>Tom Rudebot Low.wav → `query:Drums#Drum%20Hits:Tom:FileId_1069`<br>Tom Rudebot Very High.wav → `query:Drums#Drum%20Hits:Tom:FileId_1070` |
| Tom 90s * (4) | Tom 90s Heavy Rock 1.wav → `query:Drums#Drum%20Hits:Tom:FileId_859`<br>Tom 90s Heavy Rock 2.wav → `query:Drums#Drum%20Hits:Tom:FileId_860`<br>Tom 90s Heavy Rock 3.wav → `query:Drums#Drum%20Hits:Tom:FileId_861` |
| Tom 606 * (4) | Tom 606 Hi.aif → `query:Drums#Drum%20Hits:Tom:FileId_806`<br>Tom 606 Low.aif → `query:Drums#Drum%20Hits:Tom:FileId_807`<br>Tom 606 PEQ2 B2.wav → `query:Drums#Drum%20Hits:Tom:FileId_808` |
| Tom Blue * (4) | Tom Blue Room 1.wav → `query:Drums#Drum%20Hits:Tom:FileId_885`<br>Tom Blue Room 2.wav → `query:Drums#Drum%20Hits:Tom:FileId_886`<br>Tom Blue Room 3.wav → `query:Drums#Drum%20Hits:Tom:FileId_887` |
| Tom Floor * (4) | Tom Floor Dry Funk 1.wav → `query:Drums#Drum%20Hits:Tom:FileId_950`<br>Tom Floor Dry Funk 2.wav → `query:Drums#Drum%20Hits:Tom:FileId_951`<br>Tom Floor Gritty.aif → `query:Drums#Drum%20Hits:Tom:FileId_952` |
| Other multi-item families (35) | Tom Hi (4), Tom MG1 (4), Tom Roto (4), Tom Yam (4), Tom Yesteryear (4), Tom 70s (3), Tom 707 (3), Tom Achad (3), Tom Brush (3), Tom D-ulator (3), Tom DDD (3), Tom ER (3), Tom Jupiter (3), Tom Likewise (3), Tom Metatom (3), Tom Rack (3), Tom Real (3), Tom Reg (3), Tom Slam (3), Tom TL (3), Tom Vintage (3), Tom Acoustic (2), Tom Bluesbreak (2), Tom Cheap (2), Tom Digital (2), Tom E501 (2), Tom Factory (2), Tom Haskell (2), Tom Jack (2), Tom KPR (2), Tom Pluto (2), Tom Prommer (2), Tom Syn (2), Tom TV (2), Tom Vinyl (2) |
| One-off names (42) | Tom Baby Whale.aif → `query:Drums#Drum%20Hits:Tom:FileId_881`<br>Tom CD 456.aif → `query:Drums#Drum%20Hits:Tom:FileId_897`<br>Tom Flamboyant.wav → `query:Drums#Drum%20Hits:Tom:FileId_948`<br>Tom LD.aif → `query:Drums#Drum%20Hits:Tom:FileId_978`<br>Tom Powered.wav → `query:Drums#Drum%20Hits:Tom:FileId_1031`<br>Tom Slap Kindified.wav → `query:Drums#Drum%20Hits:Tom:FileId_1082`<br>All: Tom Baby Whale, Tom Big Slackjaw, Tom Bit Crush, Tom Blop Electrified, Tom Bolly, Tom Bonk, Tom Bucket, Tom CD 456, Tom Crush Source, Tom Crushed, Tom Dirty, Tom Dry Funk Brush, Tom E4, Tom EDM Bit Crush, Tom Flamboyant, Tom Fleet, Tom Future Proof, Tom Graded, Tom Grounded, Tom High-Mid Gen Purpose, Tom Kindified, Tom LD, Tom Low-Mid Gen Purpose, Tom Marching Trade Aid, Tom Mid-High Crack, Tom Mid-Low Crack, Tom Pete, Tom Phive, Tom Powered, Tom Processed, Tom ProL Abuse, Tom Red Ana, Tom RK Dry, Tom Scorched, Tom Sister ST, Tom Slap Kindified, Tom Super, Tom Synth Mkit 8, Tom Unsounded, Tom Various, Tom Wiggle, Tom Wood Combo |

#### Misc Percussion — 244 items (aif/wav); 175 naming families
URI pattern: `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_NNNN`

| Family (count) | Representative name → URI |
|---|---|
| E-Perc Strike * (8) | E-Perc Strike Burned 1.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2769`<br>E-Perc Strike Burned 3.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2771`<br>E-Perc Strike Grounded 2.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2774`<br>E-Perc Strike Shadowed.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2776` |
| Tabla SP * (7) | Tabla SP 1.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1836`<br>Tabla SP 3.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1838`<br>Tabla SP 5.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1840`<br>Tabla SP.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1842` |
| E-Perc Blop * (5) | E-Perc Blop Charred.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2711`<br>E-Perc Blop Electrified.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2712`<br>E-Perc Blop Melodized 1.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2714`<br>E-Perc Blop RK.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2715` |
| E-Perc * (4) | E-Perc 7.aif → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2693`<br>E-Perc 8.aif → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2694`<br>E-Perc 9.aif → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2695` |
| E-Perc Analog * (4) | E-Perc Analog Hi.aif → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2698`<br>E-Perc Analog Low.aif → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2699`<br>E-Perc Analog Perc Hi.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2700` |
| E-Perc Metal * (4) | E-Perc Metal 1.aif → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2742`<br>E-Perc Metal 2.aif → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2743`<br>E-Perc Metal 3.aif → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2744` |
| E-Perc Ring * (4) | E-Perc Ring Shift Moon Golf 1.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2758`<br>E-Perc Ring Shift Moon Golf 2.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2759`<br>E-Perc Ring Shift Moon Golf 3.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2760` |
| Perc African * (4) | Perc African MPC 1.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1780`<br>Perc African MPC 2.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1781`<br>Perc African MPC 3.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1782` |
| E-Perc Blip * (3) | E-Perc Blip Charred.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2706`<br>E-Perc Blip EDM.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2707`<br>E-Perc Blip Hi.aif → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2708` |
| E-Perc Click * (3) | E-Perc Click Chop.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2722`<br>E-Perc Click Grounded.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2723`<br>E-Perc Click Unsounded.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2724` |
| E-Perc Digital * (3) | E-Perc Digital Bleep.aif → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2729`<br>E-Perc Digital Knock.aif → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2730`<br>E-Perc Digital Plonk.aif → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2731` |
| Flexitone * (3) | Flexitone 1.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1767`<br>Flexitone 2.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1768`<br>Flexitone 3.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1769` |
| Perc Hit * (3) | Perc Hit Hard.aif → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1794`<br>Perc Hit Rattle.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1795`<br>Perc Hit Soft.aif → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1796` |
| Perc Slap * (3) | Perc Slap 1.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1816`<br>Perc Slap 2.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1817`<br>Perc Slap 3.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1818` |
| Rattle DECAP * (3) | Rattle DECAP 1.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1830`<br>Rattle DECAP 2.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1831`<br>Rattle DECAP 3.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1832` |
| Temple Drum * (3) | Temple Drum Vinyl 1.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1843`<br>Temple Drum Vinyl 2.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1844`<br>Temple Drum Vinyl 3.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1845` |
| Timbale Skin * (3) | Timbale Skin 1.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1848`<br>Timbale Skin 2.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1849`<br>Timbale Skin 3.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1850` |
| E-Perc Bell * (2) | E-Perc Bell 1.aif → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2703`<br>E-Perc Bell 2.aif → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2704` |
| E-Perc Block * (2) | E-Perc Block 1.aif → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2709`<br>E-Perc Block 2.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2710` |
| E-Perc Low * (2) | E-Perc Low EDM.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2739`<br>E-Perc Low Knock.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2740` |
| E-Perc Noise * (2) | E-Perc Noise Charred.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2747`<br>E-Perc Noise.aif → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2748` |
| E-Perc PO * (2) | E-Perc PO Noise.aif → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2750`<br>E-Perc PO Snare.aif → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2751` |
| Other multi-item families (14) | E-Perc Toy (2), E-Perc Tube (2), E-Perc Tuned (2), E-Perc Vocoder (2), Mini Drum (2), Perc Combo (2), Perc Metallic (2), Perc Plastic (2), Perc Pot (2), Perc Stick (2), Stick Vinyl (2), Timpani Orchestra (2), Timpani Soft (2), Xylophone Rub (2) |
| One-off names (139) | Agogo Atabaques 112 bpm.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_3881`<br>E-Perc Bolly.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2716`<br>E-Perc Reson.aif → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2756`<br>E-Perc Wood Knock.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_2798`<br>Perc Illusion.wav → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_1797`<br>Percussion Ensemble 92 bpm.aif → `query:Drums#Drum%20Hits:Misc%20Percussion:FileId_3902`<br>All: Agogo Atabaques 112 bpm, Agogo Bells 90 bpm, Akeem Groove 120 bpm, Bongos 121 bpm, Bongos 130 bpm, Castanet Reverb, Clapping Flamenco 120 bpm, Claps and Caixa 184 bpm, Click Button Arcade 109 bpm, Click Vinyl, Conga 100 bpm, Conga and Tambourine 106 bpm, Congas 128 bpm, Cuica High, Cuica Low, Djembe 120 bpm, Djembe High Hard, Dolak 85 bpm, Drum Machine Vintage 100 bpm, E-Perc Abstract, E-Perc Alien, E-Perc Beetle Talk, E-Perc BittyBot, E-Perc Bolly, E-Perc Bottle Tap, E-Perc Busted, E-Perc Buttoned, E-Perc Buzz Hymned, E-Perc Chirpster, E-Perc Clop, E-Perc Compact, E-Perc Digiding, E-Perc DMX East, E-Perc Donk, E-Perc Dull, E-Perc ENIAC Error, E-Perc ER Ring, E-Perc Git Up, E-Perc Hoot, E-Perc Knock Buzz, E-Perc Maser Blip, E-Perc Metallic Grounded, E-Perc Object, E-Perc R100, E-Perc Record Pullback, E-Perc Reso, E-Perc Reson, E-Perc Rim Synth Mkit, E-Perc RK Electric, E-Perc Scrape Shake, E-Perc Screech Kick, E-Perc Short and Prune, E-Perc Sine Sigh, E-Perc Sound Objects Knock Ambient, E-Perc Spring, E-Perc Squeak, E-Perc Submarine Pong, E-Perc Surprised Bee, E-Perc Tape Measure, E-Perc Techno Bell, E-Perc Tiny Cavern Anvil, E-Perc Tone, E-Perc Train Track, E-Perc Trigger, E-Perc Tunk, E-Perc Vintage Blip, E-Perc Warp, E-Perc Weighty Knock, E-Perc Weouh, E-Perc Wood Knock, E-Perc Yellow Jacket, Flexitone MPC, Foley Coin LDre, Foley Drop LDre, Found Object, Guiro 110 bpm, Guiro Vintage Cut, Kick 4-4 Soft 128 bpm, Metallic Charred, Metallic High Short, Metallic Rattle, Outer Bongos 140bpm, Pandeiro 110 bpm, Pandeiro 184 bpm, Perc Atom, Perc Bass Pluck, Perc Chamber Spin, Perc Childish Rattle, Perc Clapstick CD, Perc Dirty Metal, Perc Foley Tap, Perc Glass Low, Perc Illusion, Perc Jingle, Perc Kettle, Perc Klang, Perc Kling, Perc Knifes, Perc Knock Rattle, Perc Mafic, Perc Object, Perc Pan, Perc Ping, Perc Rattle New Year, Perc Sauce 75 bpm, Perc Semba 100 bpm, Perc Shaken, Perc Snap Tap, Perc Spoons, Perc Strike, Perc Tiny, Perc Tuned High, Perc Vinyl X, Perc Wood Scratch, Perc Wooden Shadowed, Percussion Ensemble 92 bpm, Plastic Tube A2, Sauce Loop 75 bpm, Semba Percussion 100 bpm, Shaker 87 bpm, Shaker 100 bpm, Shaker 102 bpm, Shaker 134 bpm, Shaker Ambient 80 bpm, Shaker and Stick 130 bpm, Stick Bluesbreak, Tabla 130 bpm, Tabla and Dolak 85 bpm, Tamb 12bit 120 bpm, Tamb Snoopy 100 bpm, Tambourine 110 bpm, Tambourine Sampled 86 bpm, Timbale Chop Processed, Timbale Rim Thumb, Timbale Stick Slap, Triangle 118 bpm, Tube Hit, Tumba Low, Whistle Verb |

#### FX Hit — 137 items (aif/wav); 84 "FX *", 14 "Impact *", 7 "Riser *", 3 "Blip *", 3 "Siren *", plus one-offs
URI pattern: `query:Drums#Drum%20Hits:FX%20Hit:FileId_NNNN` (FX_* = FileId_2607–2690; others FileId_692–739 and 3844–3848)

| Family (count) | Representative name → URI |
|---|---|
| FX Zap * (8) | FX Zap Lo Fi.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2685`<br>FX Zap Vocoder.aif → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2688`<br>FX Zap Ring Long ER Fenk.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2686`<br>FX Zappy.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2690` |
| FX Vocoder * (6) | FX Vocoder Robot.aif → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2680`<br>FX Vocoder Chord Bbmin.aif → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2678`<br>FX Vocoder Scratch.aif → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2681` |
| FX Blop/Blip/Bleep (7) | FX Blop Techno.aif → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2616`<br>FX Blop Hi ER.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2613`<br>FX Blip Perc EDM.aif → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2612`<br>FX Bleep High.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2611` |
| FX Buzz * (4) | FX Buzz Hi.aif → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2619`<br>FX Buzz Stutter Runaway.aif → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2621` |
| FX Ring * (4) | FX Ring Blipp.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2656`<br>FX Ring Home Run.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2659` |
| FX Drip * (4) | FX Drip 1.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2632` … FX Drip 4.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2635` |
| FX Strike/Reverse/Noise/Synth/Metallic (13) | FX Reverse.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2655`<br>FX Strike Doubled.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2664`<br>FX Noise Short.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2648`<br>FX Synth Chord Dmin.aif → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2669`<br>FX Metallic Charred.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2643` |
| FX one-offs (~38) | FX Laser Hit BNYX.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2641`<br>FX Record Stop.aif → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2651`<br>FX Turn Off TV.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2673`<br>FX Sub Verb.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2668`<br>FX Glitch Chop.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_2637`<br>All: Alien Perc, Alien Warning, Bell Hum, Broken Box, Brute Hit, Clap Combo, Click Glitch, Combo Chop, Crunch Short, Dark Swell, Denial, Digital Scrape, Dist Streamed, DMX Perc, Funkit, Guitar Chop C, Ice Cubes, Laser Hardware, Lighter Spark, Motor Windup, Punch Unsounded, Reso Hat, RKTD Noise, Scorched Hit, Scrape Snare, Scratch Slackjaw, Squeak, Stutter Sweep, Tick Shatter, Turn On TV, Verb Synth D, Water, Whip Digital |
| Impact * (14) | Impact Gunshot.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_709`<br>Impact Layered.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_711`<br>Impact Dub Chamber.aif → `query:Drums#Drum%20Hits:FX%20Hit:FileId_706`<br>Impact Slam.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_716`<br>All: Current, Deep Pad 120 bpm, Flanged, GE, Layered Reversed, Mov Digi, Robotic, Short Metal, Shot, Soft Top (FileId_704–717) |
| Riser * (7) | Riser White Noise.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_723`<br>Riser Whoosh Up.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_724`<br>Riser Sine.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_720`<br>Riser Synth.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_721`; also Klic, Noise Gated, Taka Breath (FileId_718–722) |
| Siren / Sweep / Swell / Whoosh (8) | Siren Alarm Charred.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_726`<br>Siren Wind.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_728`<br>Sweep White Noise Fall.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_732`<br>Swell Rusher.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_734`<br>Whoosh Down Dark.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_737` |
| Foley / one-offs (19) | Airhorn Verb.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_692`<br>Cash Register.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_699`<br>Camera Shutter.aif → `query:Drums#Drum%20Hits:FX%20Hit:FileId_698`<br>Broken Glass.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_697`<br>Video Game.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_736`<br>Stylus Scratch.wav → `query:Drums#Drum%20Hits:FX%20Hit:FileId_730`<br>All: Blip Dropped/Impact/Water (693–695), Bomb Tick 101 bpm (3844), Bowl Swell B1 (696), Echo Strike (700), Foley Door Lock (701), Ghost Impact (702), Guitar Strings FX Sequence (3845), Heart Rate (703), Hum and Hiss Swepdustry 90 bpm (3846), Noise Blaze 130 bpm (3847), Scratch Baby (3848), Scratch Baby Reflect (725), Sonar Submarine (729), Sweeper Game (733), Wire Shudder (738), Zap Disco (739) |

#### Clap — 111 items (aif/wav); 103 "Clap *", 7 "Snap *", 1 "Hand Clap 505"
URI pattern: `query:Drums#Drum%20Hits:Clap:FileId_NNNN` (FileId_2937–3049)

| Family (count) | Representative name → URI |
|---|---|
| Clap 808 * (5) | Clap 808.aif → `query:Drums#Drum%20Hits:Clap:FileId_2943`<br>Clap 808 Light Quick.aif → `query:Drums#Drum%20Hits:Clap:FileId_2939`<br>Clap 808 Prommer.wav → `query:Drums#Drum%20Hits:Clap:FileId_2940`<br>Clap 808 Reviv 1.wav → `query:Drums#Drum%20Hits:Clap:FileId_2941` |
| Clap 909 * (2) | Clap 909.aif → `query:Drums#Drum%20Hits:Clap:FileId_2945`<br>Clap 909 Reviv.wav → `query:Drums#Drum%20Hits:Clap:FileId_2944` |
| Clap 505/707/DMX (5) | Clap 505 ASR.wav → `query:Drums#Drum%20Hits:Clap:FileId_2937`<br>Clap 707.wav → `query:Drums#Drum%20Hits:Clap:FileId_2938`<br>Clap DMX.wav → `query:Drums#Drum%20Hits:Clap:FileId_2969`<br>Hand Clap 505.aif → `query:Drums#Drum%20Hits:Clap:FileId_3042` |
| Clap DECAP * (3) | Clap DECAP 1.wav → `query:Drums#Drum%20Hits:Clap:FileId_2965`<br>Clap DECAP 3.wav → `query:Drums#Drum%20Hits:Clap:FileId_2967` |
| Clap Fenk * (3) | Clap Fenk Dry.wav → `query:Drums#Drum%20Hits:Clap:FileId_2979`<br>Clap Fenk Wet.wav → `query:Drums#Drum%20Hits:Clap:FileId_2981`<br>Clap Fenk Toy.wav → `query:Drums#Drum%20Hits:Clap:FileId_2980` |
| Clap Machine * (3) | Clap Machine 1.aif → `query:Drums#Drum%20Hits:Clap:FileId_2999`<br>Clap Machine 12.aif → `query:Drums#Drum%20Hits:Clap:FileId_3000` |
| Clap RK * (3) | Clap RK 1.wav → `query:Drums#Drum%20Hits:Clap:FileId_3011`<br>Clap RK TD1 Uluru 2.wav → `query:Drums#Drum%20Hits:Clap:FileId_3013` |
| Clap Vinyl/Vintage (4) | Clap Vinyl.wav → `query:Drums#Drum%20Hits:Clap:FileId_3037`<br>Clap Vinyl SP.wav → `query:Drums#Drum%20Hits:Clap:FileId_3036`<br>Clap Vintage 5.aif → `query:Drums#Drum%20Hits:Clap:FileId_3034`<br>Clap Vintage Yakiman.aif → `query:Drums#Drum%20Hits:Clap:FileId_3035` |
| Clap Layer/Layered (4) | Clap Layered.wav → `query:Drums#Drum%20Hits:Clap:FileId_2996`<br>Clap Trap Layer.wav → `query:Drums#Drum%20Hits:Clap:FileId_3032`<br>Clap Super Layer.wav → `query:Drums#Drum%20Hits:Clap:FileId_3022`<br>Clap Super Duper Layer.wav → `query:Drums#Drum%20Hits:Clap:FileId_3021` |
| Clap Snap Fings / Snap * (9) | Clap Snap Fings.wav → `query:Drums#Drum%20Hits:Clap:FileId_3019`<br>Snap Fingers SP.wav → `query:Drums#Drum%20Hits:Clap:FileId_3045`<br>Snap BNYX.wav → `query:Drums#Drum%20Hits:Clap:FileId_3043`<br>Snap Lounge.wav → `query:Drums#Drum%20Hits:Clap:FileId_3046` |
| Clap Synth/Digital (4) | Clap Synth Double White.aif → `query:Drums#Drum%20Hits:Clap:FileId_3026`<br>Clap Synth Slap Shot.aif → `query:Drums#Drum%20Hits:Clap:FileId_3027`<br>Clap Digital Rasp.aif → `query:Drums#Drum%20Hits:Clap:FileId_2972` |
| Clap Acoustified/Foley (3) | Clap Acoustified.aif → `query:Drums#Drum%20Hits:Clap:FileId_2950`<br>Clap Acoustified Dry.wav → `query:Drums#Drum%20Hits:Clap:FileId_2949`<br>Clap Foley.aif → `query:Drums#Drum%20Hits:Clap:FileId_2984` |
| One-off names (~65) | Clap Tight.wav → `query:Drums#Drum%20Hits:Clap:FileId_3031`<br>Clap Crunch.wav → `query:Drums#Drum%20Hits:Clap:FileId_2964`<br>Clap BNYX.wav → `query:Drums#Drum%20Hits:Clap:FileId_2954`<br>Clap ATL.wav → `query:Drums#Drum%20Hits:Clap:FileId_2946`<br>Clap Wood Block.wav → `query:Drums#Drum%20Hits:Clap:FileId_3039`<br>Clap White Noise.wav → `query:Drums#Drum%20Hits:Clap:FileId_3038`<br>All: Abstract 3, Abstract Build, Analog Source, Asap, BF, Bit Colored, Bit Nighties, Blap, Bockety Reverse, Boss, Bryant, Burned, Cargo, Cracker, Dead Nap, Demure Synth, Digital Vox, DMX Analog, Dummy, eClap, Electrified, Enemy Flac, ER Fenk, Feel, Finger, Flange Hint, Grandfather, Grounded, Hans, Hit Hard 1/2, Hugo Clones, Ina, Kiss, Knock, Last Min, LD, LoFi Processed, Loose, Mannschaft, Mate, Over There, Peace, People, Perc Combo, Pete, Prommer Vinyl DMX/ST, Rewrite, Septet, Simple Snap, Slackjaw, Snap Fings Inna Big Room, Streets, Surround, Sustain, Swept Metallic, Taka Identify, Taka Spiky, Tear, Trax, Woody; Snap Beyond Click, Snap SP, Snap Vid Mo, Snap Xrated |

#### Rim — 98 items (aif/wav); 97 "Rim *", 1 "Rimshot *"
URI pattern: `query:Drums#Drum%20Hits:Rim:FileId_NNNN` (FileId_1593–1690)

| Family (count) | Representative name → URI |
|---|---|
| Rim Sidestick * (acoustic) (13) | Rim Sidestick Hard Dry Session.aif → `query:Drums#Drum%20Hits:Rim:FileId_1664`<br>Rim Sidestick Soft Dry Session.aif → `query:Drums#Drum%20Hits:Rim:FileId_1671`<br>Rim Sidestick Gen Purpose.aif → `query:Drums#Drum%20Hits:Rim:FileId_1662`<br>Rim Sidestick Acoustified.wav → `query:Drums#Drum%20Hits:Rim:FileId_1660`<br>Rim Sidestick Pop Rock Video.wav → `query:Drums#Drum%20Hits:Rim:FileId_1668`; also Direct Injection, Hard Bright Room, Mad Skill, Open, Plymouth, Punch, Raged, X Snare (1661–1672) |
| Rim 808 * (5) | Rim 808.aif → `query:Drums#Drum%20Hits:Rim:FileId_1600`<br>Rim 808 DMX.wav → `query:Drums#Drum%20Hits:Rim:FileId_1597`<br>Rim 808 SP 1.wav → `query:Drums#Drum%20Hits:Rim:FileId_1598`<br>Rim BNYX 808.wav → `query:Drums#Drum%20Hits:Rim:FileId_1605` |
| Rim 909/707/505/C78 (7) | Rim 909.aif → `query:Drums#Drum%20Hits:Rim:FileId_1603`<br>Rim 909 SP 1.wav → `query:Drums#Drum%20Hits:Rim:FileId_1601`<br>Rim 707.wav → `query:Drums#Drum%20Hits:Rim:FileId_1596`<br>Rim 505.aif → `query:Drums#Drum%20Hits:Rim:FileId_1595`<br>Rim C78.aif → `query:Drums#Drum%20Hits:Rim:FileId_1614` |
| Rim DMX * (5) | Rim DMX.wav → `query:Drums#Drum%20Hits:Rim:FileId_1627`<br>Rim DMX Fatso 1.wav → `query:Drums#Drum%20Hits:Rim:FileId_1623`<br>Rim DMX Lo Fi.wav → `query:Drums#Drum%20Hits:Rim:FileId_1625`<br>Rim DMX Vinyl.wav → `query:Drums#Drum%20Hits:Rim:FileId_1626` |
| Rim Taka * (6) | Rim Taka Natural 1.wav → `query:Drums#Drum%20Hits:Rim:FileId_1680`<br>Rim Taka Ding.wav → `query:Drums#Drum%20Hits:Rim:FileId_1678`<br>Rim Taka Sizzle.wav → `query:Drums#Drum%20Hits:Rim:FileId_1682` |
| Rim BNYX * (3) | Rim BNYX Classic.wav → `query:Drums#Drum%20Hits:Rim:FileId_1607`<br>Rim BNYX Bright.wav → `query:Drums#Drum%20Hits:Rim:FileId_1606` |
| Rim Lofi / Vinyl / 90s MPC (7) | Rim Lofi Clack.aif → `query:Drums#Drum%20Hits:Rim:FileId_1648`<br>Rim Lofi Vinyl.wav → `query:Drums#Drum%20Hits:Rim:FileId_1650`<br>Rim Vinyl 1.wav → `query:Drums#Drum%20Hits:Rim:FileId_1687`<br>Rim 90s MPC.wav → `query:Drums#Drum%20Hits:Rim:FileId_1604`<br>Rim Sampled Vinyl.wav → `query:Drums#Drum%20Hits:Rim:FileId_1659` |
| Rim DECAP/LDre/Cheap/Fenk/S-series (13) | Rim DECAP 1.wav → `query:Drums#Drum%20Hits:Rim:FileId_1620`<br>Rim LDre 1.wav → `query:Drums#Drum%20Hits:Rim:FileId_1644`<br>Rim Cheap 1.wav → `query:Drums#Drum%20Hits:Rim:FileId_1615`<br>Rim Fenk Clap.wav → `query:Drums#Drum%20Hits:Rim:FileId_1634`<br>Rim S1.wav → `query:Drums#Drum%20Hits:Rim:FileId_1656` |
| One-offs (~39) | Rim Tight.aif → `query:Drums#Drum%20Hits:Rim:FileId_1686`<br>Rim Crack.wav → `query:Drums#Drum%20Hits:Rim:FileId_1619`<br>Rim Drum Machine.aif → `query:Drums#Drum%20Hits:Rim:FileId_1632`<br>Rim Electronic.aif → `query:Drums#Drum%20Hits:Rim:FileId_1633`<br>Rim Jungle.wav → `query:Drums#Drum%20Hits:Rim:FileId_1642`<br>Rimshot Serendipity of Surprise.wav → `query:Drums#Drum%20Hits:Rim:FileId_1690`<br>All: 3k Sharp, BamVim, Bedroom, Bedroom SP, Bipp, Brixton, Bupp, Clap ER, Clean Thin Res, Dirty Feel, Dobbs, Doggie, Donk, Glitcha, GR, Ham, Hard S10, Hihat Combo, Izo Viny, Large Hall, LD, Paddle Clack, Plymouth, Processed, Pump It, Rung, Slackjaw, Snap Combo, Snark, Something, Stereo Crunch, Tangerine, Three Iron, Way Source |

#### Cymbal — 86 items (aif/wav); 61 "Crash *", 23 "Cymbal *", 2 "Splash *"
URI pattern: `query:Drums#Drum%20Hits:Cymbal:FileId_NNNN` (FileId_2801–2886)

| Family (count) | Representative name → URI |
|---|---|
| Crash 505/707/808/909 (5) | Crash 505.aif → `query:Drums#Drum%20Hits:Cymbal:FileId_2802`<br>Crash 707.wav → `query:Drums#Drum%20Hits:Cymbal:FileId_2803`<br>Crash 808 Prommer.wav → `query:Drums#Drum%20Hits:Cymbal:FileId_2804`<br>Crash 909.aif → `query:Drums#Drum%20Hits:Cymbal:FileId_2805` |
| Crash Dry Session * (4) | Crash Dry Session Hard 1.aif → `query:Drums#Drum%20Hits:Cymbal:FileId_2826`<br>Crash Dry Session Soft 1.aif → `query:Drums#Drum%20Hits:Cymbal:FileId_2828` |
| Crash China * (3) | Crash China Edge ML.wav → `query:Drums#Drum%20Hits:Cymbal:FileId_2815`<br>Crash China Edge TW.wav → `query:Drums#Drum%20Hits:Cymbal:FileId_2816`<br>Crash China Stick Hit Cop Style.wav → `query:Drums#Drum%20Hits:Cymbal:FileId_2817` |
| Crash DMX * (3) | Crash DMX.wav → `query:Drums#Drum%20Hits:Cymbal:FileId_2825`<br>Crash DMX Real 1.wav → `query:Drums#Drum%20Hits:Cymbal:FileId_2823` |
| Crash Acoustified/Real SP/Soft Acoustic (5) | Crash Acoustified High.wav → `query:Drums#Drum%20Hits:Cymbal:FileId_2806`<br>Crash Acoustified Low.wav → `query:Drums#Drum%20Hits:Cymbal:FileId_2807`<br>Crash Real SP 1.wav → `query:Drums#Drum%20Hits:Cymbal:FileId_2847`<br>Crash Soft Acoustic.wav → `query:Drums#Drum%20Hits:Cymbal:FileId_2853` |
| Crash Crack/Stick Crack (4) | Crash Crack 1.aif → `query:Drums#Drum%20Hits:Cymbal:FileId_2819`<br>Crash Stick Crack 1.wav → `query:Drums#Drum%20Hits:Cymbal:FileId_2856` |
| Crash DECAP/Kindified/Gen Purpose (6) | Crash DECAP 1.wav → `query:Drums#Drum%20Hits:Cymbal:FileId_2821`<br>Crash Kindified 1.wav → `query:Drums#Drum%20Hits:Cymbal:FileId_2838`<br>Crash Gen Purpose.aif → `query:Drums#Drum%20Hits:Cymbal:FileId_2834` |
| Crash one-offs (31) | Crash Heavy Rock.wav → `query:Drums#Drum%20Hits:Cymbal:FileId_2835`<br>Crash Room.aif → `query:Drums#Drum%20Hits:Cymbal:FileId_2849`<br>Crash Lofi.wav → `query:Drums#Drum%20Hits:Cymbal:FileId_2843`<br>Crash Kick Reverse.aif → `query:Drums#Drum%20Hits:Cymbal:FileId_2837`<br>Crash Layered.wav → `query:Drums#Drum%20Hits:Cymbal:FileId_2841`<br>Crash Light.wav → `query:Drums#Drum%20Hits:Cymbal:FileId_2842`<br>All: BamVin, Bandicute, Bluesbreak, Bolt, Boring, Brkroni, Build, Chop Yolo, ER Fenk, Feel, Flanger Sweep, Ironman, LD, Mansion, Old Time, Pete, Roomy, Sing, Smoke, Squashed, Stacked, Synth DECAP, Taka School, Terrified, Tremlow (FileId_2808–2861) |
| Cymbal 808 * (8) | Cymbal 808 1.wav → `query:Drums#Drum%20Hits:Cymbal:FileId_2863`<br>Cymbal 808 Full.wav → `query:Drums#Drum%20Hits:Cymbal:FileId_2866`<br>Cymbal 808 Hard.aif → `query:Drums#Drum%20Hits:Cymbal:FileId_2867`<br>Cymbal 808 Soft.aif → `query:Drums#Drum%20Hits:Cymbal:FileId_2868` |
| Cymbal Acoustic/606/C78 (5) | Cymbal Acoustic.aif → `query:Drums#Drum%20Hits:Cymbal:FileId_2873`<br>Cymbal Acoustic 96.aif → `query:Drums#Drum%20Hits:Cymbal:FileId_2872`<br>Cymbal 606.aif → `query:Drums#Drum%20Hits:Cymbal:FileId_2862`<br>Cymbal C78.aif → `query:Drums#Drum%20Hits:Cymbal:FileId_2874` |
| Cymbal one-offs (10) | Cymbal Acid House.aif → `query:Drums#Drum%20Hits:Cymbal:FileId_2871`<br>Cymbal Crash Reverse Gnirob.wav → `query:Drums#Drum%20Hits:Cymbal:FileId_2875`<br>Cymbal HH Sizzle.wav → `query:Drums#Drum%20Hits:Cymbal:FileId_2879`<br>Cymbal Lofi.aif → `query:Drums#Drum%20Hits:Cymbal:FileId_2880`<br>Cymbal Machine.wav → `query:Drums#Drum%20Hits:Cymbal:FileId_2881`<br>All: Dax, DM Vintage, Grindage, Mad Skill, Mini Taka, RK Acid (FileId_2876–2884) |
| Splash * (2) | Splash Code Long.aif → `query:Drums#Drum%20Hits:Cymbal:FileId_2885`<br>Splash Grounded.wav → `query:Drums#Drum%20Hits:Cymbal:FileId_2886` |

#### Shaker — 70 items (aif/wav); 51 "Shaker *", 12 "Cabasa/Cabassa *", 6 "Shake *", 1 "Maracas 808"
URI pattern: `query:Drums#Drum%20Hits:Shaker:FileId_NNNN` (FileId_1522–1591)

| Family (count) | Representative name → URI |
|---|---|
| Shaker Vinyl * (5) | Shaker Vinyl 1.wav → `query:Drums#Drum%20Hits:Shaker:FileId_1586` … Shaker Vinyl 5.wav → `query:Drums#Drum%20Hits:Shaker:FileId_1590` |
| Shaker Acoustic/Acoustified (5) | Shaker Acoustic.aif → `query:Drums#Drum%20Hits:Shaker:FileId_1547`<br>Shaker Acoustic Step 3.aif → `query:Drums#Drum%20Hits:Shaker:FileId_1546`<br>Shaker Acoustified.aif → `query:Drums#Drum%20Hits:Shaker:FileId_1550`<br>Shaker Acoustified 1.wav → `query:Drums#Drum%20Hits:Shaker:FileId_1548` |
| Shaker Noise * (4) | Shaker Noise.wav → `query:Drums#Drum%20Hits:Shaker:FileId_1574`<br>Shaker Noise Step 1.aif → `query:Drums#Drum%20Hits:Shaker:FileId_1573` |
| Shaker DMX * (3) | Shaker DMX.wav → `query:Drums#Drum%20Hits:Shaker:FileId_1557`<br>Shaker DMX Vinyl.aif → `query:Drums#Drum%20Hits:Shaker:FileId_1556` |
| Shaker Short/Long/Full/Low (5) | Shaker Short.aif → `query:Drums#Drum%20Hits:Shaker:FileId_1582`<br>Shaker Long.aif → `query:Drums#Drum%20Hits:Shaker:FileId_1567`<br>Shaker Full.aif → `query:Drums#Drum%20Hits:Shaker:FileId_1561`<br>Shaker Low Short.wav → `query:Drums#Drum%20Hits:Shaker:FileId_1569` |
| Shaker 808/70s MPC/007/013/A1 (5) | Shaker 808 Reviv.wav → `query:Drums#Drum%20Hits:Shaker:FileId_1544`<br>Shaker 70s MPC.wav → `query:Drums#Drum%20Hits:Shaker:FileId_1543`<br>Shaker 007.aif → `query:Drums#Drum%20Hits:Shaker:FileId_1541` |
| Shaker one-offs (24) | Shaker Egg.aif → `query:Drums#Drum%20Hits:Shaker:FileId_1559`<br>Shaker Live Vinyl.wav → `query:Drums#Drum%20Hits:Shaker:FileId_1566`<br>Shaker Transient.aif → `query:Drums#Drum%20Hits:Shaker:FileId_1585`<br>Shaker Source.aif → `query:Drums#Drum%20Hits:Shaker:FileId_1583`<br>All: AlienFash, Build, Burned, Chop, Drop, Electrified 06, GrooveShadow, Ironman, LDre 1/2, Low Chop, Nobody, Pete, Prommer Vinyl, Rattle SP, RKTD, Sad, SeedPodBangle, SW2, Sweep, Yolo (1551–1591) |
| Cabasa * (12) | Cabasa SP.wav → `query:Drums#Drum%20Hits:Shaker:FileId_1531`<br>Cabasa DECAP 1.wav → `query:Drums#Drum%20Hits:Shaker:FileId_1523` (…DECAP 6 = 1528)<br>Cabasa 60s Vinyl.wav → `query:Drums#Drum%20Hits:Shaker:FileId_1522`<br>Cabasa Short Mid.aif → `query:Drums#Drum%20Hits:Shaker:FileId_1532`; also Filtered Chekov, LD, Cabassa SP (1529, 1530, 1533) |
| Shake * / Maracas (7) | Shake Maracas Hard.aif → `query:Drums#Drum%20Hits:Shaker:FileId_1538`<br>Shake Maracas Soft.aif → `query:Drums#Drum%20Hits:Shaker:FileId_1539`<br>Maracas 808.wav → `query:Drums#Drum%20Hits:Shaker:FileId_1534`<br>Shake Cabasa Short.aif → `query:Drums#Drum%20Hits:Shaker:FileId_1535`; also Shake Deep Fried, Delay, Shakeur (1536, 1537, 1540) |

#### Bell — 69 items (aif/wav); 36 "Cowbell *", 16 "Bell *", 13 "Triangle *", 2 "Chimes *", 1 Bells Agogo Hi, 1 Metallic C78
URI pattern: `query:Drums#Drum%20Hits:Bell:FileId_NNNN` (FileId_3066–3134)

| Family (count) | Representative name → URI |
|---|---|
| Cowbell 808/707/505/C78 (8) | Cowbell 808.aif → `query:Drums#Drum%20Hits:Bell:FileId_3088`<br>Cowbell 808 DMX.wav → `query:Drums#Drum%20Hits:Bell:FileId_3086`<br>Cowbell 707.aif → `query:Drums#Drum%20Hits:Bell:FileId_3085`<br>Cowbell Hi 505.aif → `query:Drums#Drum%20Hits:Bell:FileId_3101`<br>Cowbell Low 505.aif → `query:Drums#Drum%20Hits:Bell:FileId_3107`<br>Cowbell C78.aif → `query:Drums#Drum%20Hits:Bell:FileId_3096` |
| Cowbell acoustic (Big Stick / Mid Stick / Dry Session) (4) | Cowbell Big Stick Dry Session.aif → `query:Drums#Drum%20Hits:Bell:FileId_3093`<br>Cowbell Big Stick British Vintage.aif → `query:Drums#Drum%20Hits:Bell:FileId_3092`<br>Cowbell Mid Stick Dry Session.aif → `query:Drums#Drum%20Hits:Bell:FileId_3109`<br>Cowbell Latin Ting.wav → `query:Drums#Drum%20Hits:Bell:FileId_3106` |
| Cowbell Vinyl SP / SP (5) | Cowbell Vinyl SP 1.wav → `query:Drums#Drum%20Hits:Bell:FileId_3119`<br>Cowbell SP.wav → `query:Drums#Drum%20Hits:Bell:FileId_3112`<br>Cowbell SP Sweetened.wav → `query:Drums#Drum%20Hits:Bell:FileId_3111` |
| Cowbell Cheap/Small/LDre/Fenk (8) | Cowbell Cheap 1.wav → `query:Drums#Drum%20Hits:Bell:FileId_3097`<br>Cowbell Small 1.wav → `query:Drums#Drum%20Hits:Bell:FileId_3114`<br>Cowbell LDre 1.wav → `query:Drums#Drum%20Hits:Bell:FileId_3104`<br>Cowbell Fenk Chick.wav → `query:Drums#Drum%20Hits:Bell:FileId_3099` |
| Cowbell one-offs (11) | Cowbell Hi.aif → `query:Drums#Drum%20Hits:Bell:FileId_3102`<br>Cowbell Simple.aif → `query:Drums#Drum%20Hits:Bell:FileId_3113`<br>Cowbell MPC 90s.wav → `query:Drums#Drum%20Hits:Bell:FileId_3108`<br>Cowbell BNYX.wav → `query:Drums#Drum%20Hits:Bell:FileId_3090`<br>All: ABB, Bessie, Brkroni, Broken, LD, Noise Anvil, Stick Crack, Taka School, Uppermost, 808 Wood Combo (3087–3118) |
| Bell Reso Noise * (6) | Bell Reso Noise 1.aif → `query:Drums#Drum%20Hits:Bell:FileId_3071` … 6.aif → `query:Drums#Drum%20Hits:Bell:FileId_3076` |
| Bell one-offs (10) | Bell Tin.wav → `query:Drums#Drum%20Hits:Bell:FileId_3081`<br>Bell Foley.aif → `query:Drums#Drum%20Hits:Bell:FileId_3068`<br>Bell Cash.aif → `query:Drums#Drum%20Hits:Bell:FileId_3066`<br>Bell Ring ER Fenk 1.wav → `query:Drums#Drum%20Hits:Bell:FileId_3077`<br>Bells Agogo Hi.aif → `query:Drums#Drum%20Hits:Bell:FileId_3082`<br>All: Chop, Lo Charred, Mid Metallic Electrified, Ring ER Fenk 2, Strike Raged, Tambo FX (3067–3080) |
| Triangle * (13) | Triangle Open.aif → `query:Drums#Drum%20Hits:Bell:FileId_3128`<br>Triangle Mute.aif → `query:Drums#Drum%20Hits:Bell:FileId_3127`<br>Triangle Short.wav → `query:Drums#Drum%20Hits:Bell:FileId_3133`<br>Triangle SP 1.wav → `query:Drums#Drum%20Hits:Bell:FileId_3131`<br>All: Build, Charred, DECAP, DMX Vinyl, Pete, Prommer Vinyl, SP 2, Synthetic (3123–3134) |
| Chimes * (2) | Chimes Finger Down.aif → `query:Drums#Drum%20Hits:Bell:FileId_3083`<br>Chimes Jingle Bell.aif → `query:Drums#Drum%20Hits:Bell:FileId_3084` |
| Metallic C78 (1) | Metallic C78.aif → `query:Drums#Drum%20Hits:Bell:FileId_3122` |

#### Ride — 69 items (aif/wav), all "Ride *"
URI pattern: `query:Drums#Drum%20Hits:Ride:FileId_NNNN` (FileId_1692–1760)

| Family (count) | Representative name → URI |
|---|---|
| Ride Stick * (acoustic, Dry Session/Vintage) (10) | Ride Stick Mid Medium Dry Session.aif → `query:Drums#Drum%20Hits:Ride:FileId_1755`<br>Ride Stick Mid Hard Vintage.aif → `query:Drums#Drum%20Hits:Ride:FileId_1754`<br>Ride Stick Edge 90s Heavy Rock.wav → `query:Drums#Drum%20Hits:Ride:FileId_1751`<br>Ride Stick Clean.wav → `query:Drums#Drum%20Hits:Ride:FileId_1750`<br>Ride Stick Tight.aif → `query:Drums#Drum%20Hits:Ride:FileId_1759`; also Bell, Edge Medium Vintage, Mid Hard Dry Session, Mid Soft Dry Session, Mid Yester Years (1749–1758) |
| Ride Bell * (6) | Ride Bell Songwriter.wav → `query:Drums#Drum%20Hits:Ride:FileId_1703`<br>Ride Bell Stick Alternative Rock.aif → `query:Drums#Drum%20Hits:Ride:FileId_1704`<br>Ride Bell Stick Heavy.wav → `query:Drums#Drum%20Hits:Ride:FileId_1705`<br>Ride Bell Crack.wav → `query:Drums#Drum%20Hits:Ride:FileId_1701`; also Ironman, Taka (1702, 1706) |
| Ride Brush (jazz-ish) (2) | Ride Brush Hit Hard Club Sizzle.aif → `query:Drums#Drum%20Hits:Ride:FileId_1708`<br>Ride Dry Funk Brush.wav → `query:Drums#Drum%20Hits:Ride:FileId_1716` |
| Ride Acoustic/Acoustified/Real (7) | Ride Acoustic Ocean.aif → `query:Drums#Drum%20Hits:Ride:FileId_1697`<br>Ride Acoustic Yakiman.aif → `query:Drums#Drum%20Hits:Ride:FileId_1698`<br>Ride Acoustified.wav → `query:Drums#Drum%20Hits:Ride:FileId_1700`<br>Ride Real SP 1.wav → `query:Drums#Drum%20Hits:Ride:FileId_1740`<br>Ride Real Tasty.wav → `query:Drums#Drum%20Hits:Ride:FileId_1742` |
| Ride 505/707/909/DMX (4) | Ride 505.aif → `query:Drums#Drum%20Hits:Ride:FileId_1692`<br>Ride 707.aif → `query:Drums#Drum%20Hits:Ride:FileId_1693`<br>Ride 909.aif → `query:Drums#Drum%20Hits:Ride:FileId_1694`<br>Ride DMX.wav → `query:Drums#Drum%20Hits:Ride:FileId_1715` |
| Ride Cup * (3) | Ride Cup 1.wav → `query:Drums#Drum%20Hits:Ride:FileId_1712`<br>Ride Cup Gen Purpose.aif → `query:Drums#Drum%20Hits:Ride:FileId_1714` |
| Ride RKTD * (5) | Ride RKTD1.wav → `query:Drums#Drum%20Hits:Ride:FileId_1737`<br>Ride RKTD Low.wav → `query:Drums#Drum%20Hits:Ride:FileId_1736` |
| Ride Acid House / Hi Acid House (2) | Ride Acid House.wav → `query:Drums#Drum%20Hits:Ride:FileId_1696`<br>Ride Hi Acid House.wav → `query:Drums#Drum%20Hits:Ride:FileId_1726` |
| One-offs (30) | Ride Clean.aif → `query:Drums#Drum%20Hits:Ride:FileId_1709`<br>Ride Neutral.wav → `query:Drums#Drum%20Hits:Ride:FileId_1733`<br>Ride Full.wav → `query:Drums#Drum%20Hits:Ride:FileId_1722`<br>Ride Lofi.aif → `query:Drums#Drum%20Hits:Ride:FileId_1729`<br>Ride Gen Purpose.aif → `query:Drums#Drum%20Hits:Ride:FileId_1724`<br>Ride Ping.aif → `query:Drums#Drum%20Hits:Ride:FileId_1734`<br>All: Abacus, Bluesbreak, Code 1, Court, EDM Toned, Eighto, Electrified, Feel, Filter Swell, Gated, HH Med, Layered, LD, Machine, Mid Crack, Mid Taka, Reso Synth, Rock My Bells, Roomy, Slackjaw, Spread, Stacked, Thin Synth (1695–1760) |

#### Wood — 55 items (aif/wav); 39 "Wood *", 10 "Clave *", 3 "Guiro *", plus Castanet, Jam Block, Perc Wood
URI pattern: `query:Drums#Drum%20Hits:Wood:FileId_NNNN` (FileId_742–796)

| Family (count) | Representative name → URI |
|---|---|
| Wood Block * (6) | Wood Block High.aif → `query:Drums#Drum%20Hits:Wood:FileId_762`<br>Wood Block Low.aif → `query:Drums#Drum%20Hits:Wood:FileId_763`<br>Wood Block Combo.aif → `query:Drums#Drum%20Hits:Wood:FileId_760`<br>Wood Block DMX Vinyl.wav → `query:Drums#Drum%20Hits:Wood:FileId_761`; also Mad Skill, Prommer Vinyl (764, 765) |
| Wood MPC * (4) | Wood MPC 1.wav → `query:Drums#Drum%20Hits:Wood:FileId_782` … 4.wav → `query:Drums#Drum%20Hits:Wood:FileId_785` |
| Wood Stick * (3) | Wood Stick LDre.wav → `query:Drums#Drum%20Hits:Wood:FileId_791`<br>Wood Stick Ring.wav → `query:Drums#Drum%20Hits:Wood:FileId_793` |
| Wood DECAP * (3) | Wood DECAP 1.wav → `query:Drums#Drum%20Hits:Wood:FileId_772` |
| Wood one-offs (23) | Wood Claves.aif → `query:Drums#Drum%20Hits:Wood:FileId_770`<br>Wood Vibraslap.aif → `query:Drums#Drum%20Hits:Wood:FileId_796`<br>Wood Clack.wav → `query:Drums#Drum%20Hits:Wood:FileId_769`<br>Wood Bright.aif → `query:Drums#Drum%20Hits:Wood:FileId_766`<br>Wood Dark.aif → `query:Drums#Drum%20Hits:Wood:FileId_775`<br>All: Bell Acoustified, Blawk, Buzz, Charred, Clog Medium, Dry Low, Feel, GR, Hall, Insert Cassette, Lofi Twig, MS, Prod Soft, Resonant Knock, Rough Low, Scrape, Tip Tag, Under The Rug (758–795) |
| Clave * (10) | Clave 808.aif → `query:Drums#Drum%20Hits:Wood:FileId_743`<br>Clave C78.aif → `query:Drums#Drum%20Hits:Wood:FileId_748`<br>Clave Bright Wide.wav → `query:Drums#Drum%20Hits:Wood:FileId_746`<br>Clave Synth.aif → `query:Drums#Drum%20Hits:Wood:FileId_752`; also Bam Vin, BNYX, C78 Processed, Mad Skill 1/2, Spring (744–751) |
| Guiro C78 * (3) | Guiro C78 Long.aif → `query:Drums#Drum%20Hits:Wood:FileId_753`<br>Guiro C78 Short.aif → `query:Drums#Drum%20Hits:Wood:FileId_755` |
| Castanet / Jam Block / Perc Wood (3) | Castanet Reverb.wav → `query:Drums#Drum%20Hits:Wood:FileId_742`<br>Jam Block Hi.aif → `query:Drums#Drum%20Hits:Wood:FileId_756`<br>Perc Wood.aif → `query:Drums#Drum%20Hits:Wood:FileId_757` |

#### Conga — 47 items (aif/wav)
URI pattern: `query:Drums#Drum%20Hits:Conga:FileId_NNNN` (FileId_2888–2935)

| Family (count) | Representative name → URI |
|---|---|
| Conga 808 * (5) | Conga 808 Hi.aif → `query:Drums#Drum%20Hits:Conga:FileId_2891`<br>Conga 808 Mid.aif → `query:Drums#Drum%20Hits:Conga:FileId_2893`<br>Conga 808 Low.aif → `query:Drums#Drum%20Hits:Conga:FileId_2892`<br>Conga 808 Prommer 1.wav → `query:Drums#Drum%20Hits:Conga:FileId_2894` |
| Conga Hi * (6) | Conga Hi 505.aif → `query:Drums#Drum%20Hits:Conga:FileId_2908`<br>Conga Hi Drive.aif → `query:Drums#Drum%20Hits:Conga:FileId_2909`<br>Conga Hi Muted.aif → `query:Drums#Drum%20Hits:Conga:FileId_2910`<br>Conga Hi Slap.aif → `query:Drums#Drum%20Hits:Conga:FileId_2911` |
| Conga Low * (7) | Conga Low 505.aif → `query:Drums#Drum%20Hits:Conga:FileId_2915`<br>Conga Low Drive.aif → `query:Drums#Drum%20Hits:Conga:FileId_2916`<br>Conga Low Ring 1.aif → `query:Drums#Drum%20Hits:Conga:FileId_2917`<br>Conga Low Slap 1.aif → `query:Drums#Drum%20Hits:Conga:FileId_2919` |
| Conga Open/Soft/Hard/Medium (6) | Conga Open Hard.aif → `query:Drums#Drum%20Hits:Conga:FileId_2923`<br>Conga Open Soft.aif → `query:Drums#Drum%20Hits:Conga:FileId_2924`<br>Conga Hard.aif → `query:Drums#Drum%20Hits:Conga:FileId_2907`<br>Conga Soft.aif → `query:Drums#Drum%20Hits:Conga:FileId_2930` |
| Conga Acoustified * (3) | Conga Acoustified.aif → `query:Drums#Drum%20Hits:Conga:FileId_2898`<br>Conga Acoustified Hi.wav → `query:Drums#Drum%20Hits:Conga:FileId_2896`<br>Conga Acoustified Low.wav → `query:Drums#Drum%20Hits:Conga:FileId_2897` |
| Conga Processed * (3) | Conga Processed 1.wav → `query:Drums#Drum%20Hits:Conga:FileId_2927`<br>Conga Processed 3.wav → `query:Drums#Drum%20Hits:Conga:FileId_2929` |
| Conga DECAP * (3) | Conga DECAP 1.wav → `query:Drums#Drum%20Hits:Conga:FileId_2903`<br>Conga DECAP 3.wav → `query:Drums#Drum%20Hits:Conga:FileId_2905` |
| Conga Weed Killa * (3) | Conga Weed Killa 1.wav → `query:Drums#Drum%20Hits:Conga:FileId_2933`<br>Conga Weed Killa 3.wav → `query:Drums#Drum%20Hits:Conga:FileId_2935` |
| Conga Chop * (3) | Conga Chop.wav → `query:Drums#Drum%20Hits:Conga:FileId_2902`<br>Conga Chop 1.aif → `query:Drums#Drum%20Hits:Conga:FileId_2900` |
| Conga 70s / LD (4) | Conga 70s 1.wav → `query:Drums#Drum%20Hits:Conga:FileId_2889`<br>Conga LD 1.aif → `query:Drums#Drum%20Hits:Conga:FileId_2913` |
| One-offs (7) | Conga 505 Low Classic.aif → `query:Drums#Drum%20Hits:Conga:FileId_2888`<br>Conga C78.aif → `query:Drums#Drum%20Hits:Conga:FileId_2899`<br>Conga Dirt.wav → `query:Drums#Drum%20Hits:Conga:FileId_2906`<br>Conga Mid Drive.aif → `query:Drums#Drum%20Hits:Conga:FileId_2922`<br>Conga Pete.wav → `query:Drums#Drum%20Hits:Conga:FileId_2925`<br>Conga Pitched SP.wav → `query:Drums#Drum%20Hits:Conga:FileId_2926`<br>Conga Verb.wav → `query:Drums#Drum%20Hits:Conga:FileId_2931`; Conga Vinyl.wav → `query:Drums#Drum%20Hits:Conga:FileId_2932` |

#### Tambourine — 32 items (aif/wav), all "Tamb *"
URI pattern: `query:Drums#Drum%20Hits:Tambourine:FileId_NNNN` (FileId_1132–1163)

| Family (count) | Representative name → URI |
|---|---|
| Tamb Hit Hard/Soft, Stick British Vintage (acoustic) (4) | Tamb Hit Hard.aif → `query:Drums#Drum%20Hits:Tambourine:FileId_1145`<br>Tamb Hit Soft.aif → `query:Drums#Drum%20Hits:Tambourine:FileId_1146`<br>Tamb Stick Hard British Vintage.aif → `query:Drums#Drum%20Hits:Tambourine:FileId_1161`<br>Tamb Stick Soft British Vintage.aif → `query:Drums#Drum%20Hits:Tambourine:FileId_1162` |
| Tamb Chop * (3) | Tamb Chop.wav → `query:Drums#Drum%20Hits:Tambourine:FileId_1140`<br>Tamb Chop LoFi.wav → `query:Drums#Drum%20Hits:Tambourine:FileId_1139`<br>Tamb Chop Jagged Glass.wav → `query:Drums#Drum%20Hits:Tambourine:FileId_1138` |
| Tamb 707/C78/DMX/LD (machines) (4) | Tamb 707.aif → `query:Drums#Drum%20Hits:Tambourine:FileId_1132`<br>Tamb C78.aif → `query:Drums#Drum%20Hits:Tambourine:FileId_1137`<br>Tamb DMX.wav → `query:Drums#Drum%20Hits:Tambourine:FileId_1141`<br>Tamb LD.aif → `query:Drums#Drum%20Hits:Tambourine:FileId_1148` |
| Tamb Short/Long/Simple/Shake/Rattle (6) | Tamb Short.aif → `query:Drums#Drum%20Hits:Tambourine:FileId_1158`<br>Tamb Long.aif → `query:Drums#Drum%20Hits:Tambourine:FileId_1149`<br>Tamb Simple.wav → `query:Drums#Drum%20Hits:Tambourine:FileId_1159`<br>Tamb Shake.aif → `query:Drums#Drum%20Hits:Tambourine:FileId_1156`<br>Tamb Rattle.aif → `query:Drums#Drum%20Hits:Tambourine:FileId_1155`; Tamb Short And Solid → 1157 |
| One-offs (15) | Tamb Dry Tap.wav → `query:Drums#Drum%20Hits:Tambourine:FileId_1142`<br>Tamb Acoustified Plymouth.wav → `query:Drums#Drum%20Hits:Tambourine:FileId_1134`<br>Tamb Prommer Vinyl.wav → `query:Drums#Drum%20Hits:Tambourine:FileId_1154`<br>Tamb Source.wav → `query:Drums#Drum%20Hits:Tambourine:FileId_1160`<br>All: 80s Space Craft, Alien Fash, Bang, Frame, Ghost, Jiggy, Metal, Perc Combo, Processed, Processed 2, Wood (1133–1163) |

#### Bongo — 14 items (aif/wav), all "Bongo *"
URI pattern: `query:Drums#Drum%20Hits:Bongo:FileId_NNNN` (FileId_3051–3064)

| Family (count) | Representative name → URI |
|---|---|
| Bongo High/Low Open Hard/Soft (4) | Bongo High Open Hard.aif → `query:Drums#Drum%20Hits:Bongo:FileId_3060`<br>Bongo High Open Soft.aif → `query:Drums#Drum%20Hits:Bongo:FileId_3061`<br>Bongo Low Open Hard.aif → `query:Drums#Drum%20Hits:Bongo:FileId_3062`<br>Bongo Low Open Soft.aif → `query:Drums#Drum%20Hits:Bongo:FileId_3063` |
| Bongo C78 Hi/Low (2) | Bongo C78 Hi.aif → `query:Drums#Drum%20Hits:Bongo:FileId_3053`<br>Bongo C78 Low.aif → `query:Drums#Drum%20Hits:Bongo:FileId_3054` |
| Bongo Edge High/Low (2) | Bongo Edge High.wav → `query:Drums#Drum%20Hits:Bongo:FileId_3057`<br>Bongo Edge Low.wav → `query:Drums#Drum%20Hits:Bongo:FileId_3058` |
| One-offs (6) | Bongo Basic.wav → `query:Drums#Drum%20Hits:Bongo:FileId_3051`<br>Bongo Break Chop.wav → `query:Drums#Drum%20Hits:Bongo:FileId_3052`<br>Bongo Chop.wav → `query:Drums#Drum%20Hits:Bongo:FileId_3055`<br>Bongo EDM.wav → `query:Drums#Drum%20Hits:Bongo:FileId_3056`<br>Bongo Hi Dry.wav → `query:Drums#Drum%20Hits:Bongo:FileId_3059`<br>Bongo Shy and Dry.aif → `query:Drums#Drum%20Hits:Bongo:FileId_3064` |

#### Timbales — 4 items (aif/wav)
URI pattern: `query:Drums#Drum%20Hits:Timbales:FileId_NNNN` (FileId_1127–1130)

| Family (count) | Representative name → URI |
|---|---|
| All (4) | Timbale 505.aif → `query:Drums#Drum%20Hits:Timbales:FileId_1127`<br>Timbales High Open Hard.aif → `query:Drums#Drum%20Hits:Timbales:FileId_1128`<br>Timbales Low Open Hard.aif → `query:Drums#Drum%20Hits:Timbales:FileId_1129`<br>Timbales Pete.wav → `query:Drums#Drum%20Hits:Timbales:FileId_1130` |


## Instruments
**Edition finding: this is Live 12 Standard/Intro-class instrument set — NOT Suite.** Only 6 native instruments exist. Operator, Wavetable, Analog, Collision, Electric, Tension, Sampler, Meld, and Max for Live instruments are absent. Every Sounds preset above is therefore built on Drift, Simpler, Drum Rack, Impulse, or Instrument Rack (multisample .adg racks use Simpler chains).
URI pattern: `query:Synths#<Device%20Name>` (note: the Instruments category URI root is `query:Synths`, not `query:Instruments`).

| Device | Type | URI | Notes |
|---|---|---|---|
| Drift | synth (folder + device) | query:Synths#Drift | 2-osc analog-style synth. Loading the folder URI loads the default device. Subfolders: Bass, Brass, Effects, Guitar & Plucked, Mallets, Pad, Percussive, Piano & Keys, Strings, Synth Keys, Synth Lead, Synth Rhythmic, Winds — these hold the .adv presets already listed under Sounds (e.g. `query:Synths#Drift:Bass`). |
| Drum Rack | device | query:Synths#Drum%20Rack | Empty rack; same as `query:Drums#Drum%20Rack`. |
| Drum Sampler | device | query:Synths#Drum%20Sampler | New in Live 12: single-sample drum synth/sampler. No preset folder. |
| Impulse | sampler (folder + device) | query:Synths#Impulse | 8-slot drum sampler. 13 presets below. |
| Instrument Rack | rack (folder + device) | query:Synths#Instrument%20Rack | Subfolders mirror Sounds (Ambient & Evolving … Winds); presets are the .adg entries listed under Sounds. Path form: `query:Synths#Instrument%20Rack:<Category>`. |
| Simpler | sampler (folder + device) | query:Synths#Simpler | Subfolders mirror Sounds (minus Percussive); presets are Simpler-based .adv/.adg from Sounds. Path form: `query:Synths#Simpler:<Category>`. |

### Impulse presets (13)
| Name | URI |
|---|---|
| Backbeat Room.adg | query:Synths#Impulse:FileId_7043 |
| Blue Thunder Kit.adg | query:Synths#Impulse:FileId_7044 |
| Brainfreeze Kit.adg | query:Synths#Impulse:FileId_7045 |
| Conga Bongo Timbales.adg | query:Synths#Impulse:FileId_7046 |
| Dub Delay.adg | query:Synths#Impulse:FileId_7047 |
| Grinder Kit.adg | query:Synths#Impulse:FileId_7048 |
| Impulse 606.adv | query:Synths#Impulse:FileId_7049 |
| Impulse 808.adv | query:Synths#Impulse:FileId_7050 |
| Percussion 1.adg | query:Synths#Impulse:FileId_7051 |
| Percussion 2.adg | query:Synths#Impulse:FileId_7052 |
| Soft Saturated.adg | query:Synths#Impulse:FileId_7053 |
| Vintage Funky Good Time.adg | query:Synths#Impulse:FileId_7054 |
| Wicked Chillin.adg | query:Synths#Impulse:FileId_7055 |

## Audio Effects
Path quirk: `get_browser_items_at_path("Audio Effects")` ERRORS — use the underscore form `audio_effects` (same for `midi_effects`, `max_for_live`, `user_library`). URI root is `query:AudioFx`.
**Edition finding: exactly the Live 12 Intro/Lite device set (17 devices).** Absent: EQ Eight, Glue Compressor, Multiband Dynamics, Gate, Drum Buss, Echo, Hybrid Reverb, Roar, Overdrive, Pedal, Amp, Cabinet, Vocoder, Corpus, Resonators, Grain Delay, Filter Delay, Looper, Spectrum, Vinyl Distortion, Dynamic Tube, Frequency Shifter, all Spectral devices, Shifter, Align Delay, Envelope Follower, LFO, Shaper (the last three are M4L).
Every device URI below also loads with load_device_to_master / load_device_to_return.

| Device | URI | Presets |
|---|---|---|
| Audio Effect Rack | query:AudioFx#Audio%20Effect%20Rack | 146 racks in 6 subfolders (below) |
| Auto Filter | query:AudioFx#Auto%20Filter | 24 |
| Auto Shift | query:AudioFx#Auto%20Shift | 19 |
| Beat Repeat | query:AudioFx#Beat%20Repeat | 13 |
| Channel EQ | query:AudioFx#Channel%20EQ | 18 |
| Chorus-Ensemble | query:AudioFx#Chorus-Ensemble | 12 |
| Compressor | query:AudioFx#Compressor | 18 |
| Delay | query:AudioFx#Delay | 31 in 4 subfolders |
| EQ Three | query:AudioFx#EQ%20Three | 7 |
| Erosion | query:AudioFx#Erosion | 8 |
| Limiter | query:AudioFx#Limiter | 11 |
| Phaser-Flanger | query:AudioFx#Phaser-Flanger | 12 |
| Redux | query:AudioFx#Redux | 9 |
| Reverb | query:AudioFx#Reverb | 79 in 3 subfolders |
| Saturator | query:AudioFx#Saturator | 22 |
| Tuner | query:AudioFx#Tuner | none (device only) |
| Utility | query:AudioFx#Utility | 10 |

### Auto Filter (24 presets) — `query:AudioFx#Auto%20Filter`
| Name | URI |
|---|---|
| Band-pass Spinner.adv | query:AudioFx#Auto%20Filter:FileId_8168 |
| Beat Mosaic.adv | query:AudioFx#Auto%20Filter:FileId_8169 |
| Comb Envelope.adv | query:AudioFx#Auto%20Filter:FileId_8170 |
| Comb Filtered Beat.adv | query:AudioFx#Auto%20Filter:FileId_8171 |
| Comb Tumble Synced.adv | query:AudioFx#Auto%20Filter:FileId_8172 |
| Crashing Waves.adv | query:AudioFx#Auto%20Filter:FileId_8173 |
| Cut-O-Move HPF.adv | query:AudioFx#Auto%20Filter:FileId_8174 |
| Cut-O-Move LPF.adv | query:AudioFx#Auto%20Filter:FileId_8175 |
| Disco Filter.adv | query:AudioFx#Auto%20Filter:FileId_8177 |
| DJ Filter Soft Clip.adv | query:AudioFx#Auto%20Filter:FileId_8176 |
| Guitar Auto-Wah.adv | query:AudioFx#Auto%20Filter:FileId_8178 |
| High-pass Slide Away.adv | query:AudioFx#Auto%20Filter:FileId_8179 |
| Move & Color.adv | query:AudioFx#Auto%20Filter:FileId_8180 |
| Notch Slide Crunch.adv | query:AudioFx#Auto%20Filter:FileId_8181 |
| Notch Stereo Sweep.adv | query:AudioFx#Auto%20Filter:FileId_8182 |
| Psycho Band.adv | query:AudioFx#Auto%20Filter:FileId_8183 |
| Resampling Filter S&H.adv | query:AudioFx#Auto%20Filter:FileId_8184 |
| Step by Step.adv | query:AudioFx#Auto%20Filter:FileId_8185 |
| Stereo Contours.adv | query:AudioFx#Auto%20Filter:FileId_8186 |
| Swirl.adv | query:AudioFx#Auto%20Filter:FileId_8187 |
| Top Spreader.adv | query:AudioFx#Auto%20Filter:FileId_8188 |
| Tops Off & Crunch.adv | query:AudioFx#Auto%20Filter:FileId_8189 |
| Twin Peaks.adv | query:AudioFx#Auto%20Filter:FileId_8190 |
| Vocal Quivver.adv | query:AudioFx#Auto%20Filter:FileId_8191 |

### Auto Shift (19 presets) — `query:AudioFx#Auto%20Shift` — pitch/formant shifter; "Tune *" presets are the closest thing to autotune in this library
| Name | URI |
|---|---|
| Added Fifth.adv | query:AudioFx#Auto%20Shift:FileId_8136 |
| Added Third.adv | query:AudioFx#Auto%20Shift:FileId_8137 |
| Formant LFO.adv | query:AudioFx#Auto%20Shift:FileId_8138 |
| Formant Low.adv | query:AudioFx#Auto%20Shift:FileId_8139 |
| Live Mode.adv | query:AudioFx#Auto%20Shift:FileId_8140 |
| MIDI In Harmonies.adv | query:AudioFx#Auto%20Shift:FileId_8141 |
| Octave Down.adv | query:AudioFx#Auto%20Shift:FileId_8142 |
| Octave Up.adv | query:AudioFx#Auto%20Shift:FileId_8143 |
| Pan Fast.adv | query:AudioFx#Auto%20Shift:FileId_8144 |
| Pitch & Formant LFO.adv | query:AudioFx#Auto%20Shift:FileId_8145 |
| Pitch Vibrato.adv | query:AudioFx#Auto%20Shift:FileId_8146 |
| Scale Aware.adv | query:AudioFx#Auto%20Shift:FileId_8147 |
| Tune Gentle.adv | query:AudioFx#Auto%20Shift:FileId_8148 |
| Tune Hard.adv | query:AudioFx#Auto%20Shift:FileId_8149 |
| Tune Slow.adv | query:AudioFx#Auto%20Shift:FileId_8150 |
| Tune Smooth.adv | query:AudioFx#Auto%20Shift:FileId_8151 |
| Voice Bass.adv | query:AudioFx#Auto%20Shift:FileId_8152 |
| Voice Soprano.adv | query:AudioFx#Auto%20Shift:FileId_8153 |
| Vox Guitar.adv | query:AudioFx#Auto%20Shift:FileId_8154 |

### Beat Repeat (13 presets) — `query:AudioFx#Beat%20Repeat`
| Name | URI |
|---|---|
| Airpusher.adv | query:AudioFx#Beat%20Repeat:FileId_8123 |
| Brain Dance.adv | query:AudioFx#Beat%20Repeat:FileId_8124 |
| Chopping Block.adv | query:AudioFx#Beat%20Repeat:FileId_8125 |
| Deconstruct.adv | query:AudioFx#Beat%20Repeat:FileId_8126 |
| Fill In The Gaps.adv | query:AudioFx#Beat%20Repeat:FileId_8127 |
| Insect.adv | query:AudioFx#Beat%20Repeat:FileId_8128 |
| Microfillz.adv | query:AudioFx#Beat%20Repeat:FileId_8129 |
| Repeight.adv | query:AudioFx#Beat%20Repeat:FileId_8130 |
| Robo Voice.adv | query:AudioFx#Beat%20Repeat:FileId_8131 |
| Semisubtle.adv | query:AudioFx#Beat%20Repeat:FileId_8132 |
| Slap Back.adv | query:AudioFx#Beat%20Repeat:FileId_8133 |
| Squishy.adv | query:AudioFx#Beat%20Repeat:FileId_8134 |
| Vocal Fun.adv | query:AudioFx#Beat%20Repeat:FileId_8135 |

### Channel EQ (18 presets) — `query:AudioFx#Channel%20EQ` — the only EQ besides EQ Three (no EQ Eight in this edition)
| Name | URI |
|---|---|
| Boom Capture.adv | query:AudioFx#Channel%20EQ:FileId_8094 |
| Drum Loop Smoother.adv | query:AudioFx#Channel%20EQ:FileId_8095 |
| Heartbeat Kick.adv | query:AudioFx#Channel%20EQ:FileId_8096 |
| Hi End Regulator.adv | query:AudioFx#Channel%20EQ:FileId_8097 |
| Hi Hat Boost.adv | query:AudioFx#Channel%20EQ:FileId_8098 |
| High End Boost.adv | query:AudioFx#Channel%20EQ:FileId_8099 |
| High Shelf.adv | query:AudioFx#Channel%20EQ:FileId_8100 |
| Keys Bright.adv | query:AudioFx#Channel%20EQ:FileId_8101 |
| Low Cut.adv | query:AudioFx#Channel%20EQ:FileId_8102 |
| Low End Boost.adv | query:AudioFx#Channel%20EQ:FileId_8103 |
| Low Shelf.adv | query:AudioFx#Channel%20EQ:FileId_8104 |
| Mid Accent.adv | query:AudioFx#Channel%20EQ:FileId_8105 |
| Mid Focus.adv | query:AudioFx#Channel%20EQ:FileId_8106 |
| Middle Area.adv | query:AudioFx#Channel%20EQ:FileId_8107 |
| Radio 40's.adv | query:AudioFx#Channel%20EQ:FileId_8108 |
| Snare Focus.adv | query:AudioFx#Channel%20EQ:FileId_8109 |
| Upper Middle.adv | query:AudioFx#Channel%20EQ:FileId_8110 |
| Vocal Curve.adv | query:AudioFx#Channel%20EQ:FileId_8111 |

### Chorus-Ensemble (12 presets) — `query:AudioFx#Chorus-Ensemble`
| Name | URI |
|---|---|
| Chorus Bass.adv | query:AudioFx#Chorus-Ensemble:FileId_8082 |
| Chorus Classic.adv | query:AudioFx#Chorus-Ensemble:FileId_8083 |
| Chorus Subtle Funk.adv | query:AudioFx#Chorus-Ensemble:FileId_8084 |
| Ensemble Deep.adv | query:AudioFx#Chorus-Ensemble:FileId_8085 |
| Ensemble Feedback.adv | query:AudioFx#Chorus-Ensemble:FileId_8086 |
| Vibrato Flutter.adv | query:AudioFx#Chorus-Ensemble:FileId_8087 |
| Vibrato Kaleidoscope.adv | query:AudioFx#Chorus-Ensemble:FileId_8088 |
| Vibrato Spacial.adv | query:AudioFx#Chorus-Ensemble:FileId_8089 |
| Vibrato Subtle.adv | query:AudioFx#Chorus-Ensemble:FileId_8090 |
| Vibrato Wobble.adv | query:AudioFx#Chorus-Ensemble:FileId_8091 |
| Warm Chorale.adv | query:AudioFx#Chorus-Ensemble:FileId_8092 |
| Warm Ensemble.adv | query:AudioFx#Chorus-Ensemble:FileId_8093 |

### Compressor (18 presets) — `query:AudioFx#Compressor` — has sidechain input; "De-esser" and "Sustained Lead Vocal" are the vocal-chain picks
| Name | URI |
|---|---|
| Acoustic Kick Compressor.adv | query:AudioFx#Compressor:FileId_8064 |
| Acoustic.adv | query:AudioFx#Compressor:FileId_8065 |
| Basic Peak Compressor.adv | query:AudioFx#Compressor:FileId_8066 |
| Brick Wall.adv | query:AudioFx#Compressor:FileId_8067 |
| Brute Compression.adv | query:AudioFx#Compressor:FileId_8068 |
| Classical Compression.adv | query:AudioFx#Compressor:FileId_8069 |
| De-esser.adv | query:AudioFx#Compressor:FileId_8070 |
| Flattenator.adv | query:AudioFx#Compressor:FileId_8071 |
| Generic Compressor.adv | query:AudioFx#Compressor:FileId_8072 |
| Gentle Squeeze.adv | query:AudioFx#Compressor:FileId_8073 |
| Gentle-Kneeless.adv | query:AudioFx#Compressor:FileId_8074 |
| Kick Reducer.adv | query:AudioFx#Compressor:FileId_8075 |
| Loud-Kneeless.adv | query:AudioFx#Compressor:FileId_8076 |
| Mildly Aggresive.adv | query:AudioFx#Compressor:FileId_8077 |
| Mix Gel.adv | query:AudioFx#Compressor:FileId_8078 |
| Precise.adv | query:AudioFx#Compressor:FileId_8079 |
| Soft Snare Compressor.adv | query:AudioFx#Compressor:FileId_8080 |
| Sustained Lead Vocal.adv | query:AudioFx#Compressor:FileId_8081 |

### Delay — `query:AudioFx#Delay` — presets are in 4 subfolders (listed further below): Ambient Spaces `query:AudioFx#Delay:Ambient%20Spaces`, Clean Delay `query:AudioFx#Delay:Clean%20Delay`, Modulated Delay `query:AudioFx#Delay:Modulated%20Delay`, Vintage Delay `query:AudioFx#Delay:Vintage%20Delay`

### EQ Three (7 presets) — `query:AudioFx#EQ%20Three`
| Name | URI |
|---|---|
| Boost HiHats.adv | query:AudioFx#EQ%20Three:FileId_7901 |
| Edges.adv | query:AudioFx#EQ%20Three:FileId_7902 |
| Hi.adv | query:AudioFx#EQ%20Three:FileId_7903 |
| Infrasonic.adv | query:AudioFx#EQ%20Three:FileId_7904 |
| Less Low More Mid.adv | query:AudioFx#EQ%20Three:FileId_7905 |
| Midnight.adv | query:AudioFx#EQ%20Three:FileId_7906 |
| Remove.adv | query:AudioFx#EQ%20Three:FileId_7907 |

### Erosion (8 presets) — `query:AudioFx#Erosion`
| Name | URI |
|---|---|
| Hiss.adv | query:AudioFx#Erosion:FileId_7836 |
| Noisy.adv | query:AudioFx#Erosion:FileId_7837 |
| Sine 3.2 Max.adv | query:AudioFx#Erosion:FileId_7839 |
| Sine 4.6 Mid.adv | query:AudioFx#Erosion:FileId_7840 |
| Sine 16 Max.adv | query:AudioFx#Erosion:FileId_7838 |
| Sine 962 High.adv | query:AudioFx#Erosion:FileId_7841 |
| Snorz.adv | query:AudioFx#Erosion:FileId_7842 |
| Wide and Dirty.adv | query:AudioFx#Erosion:FileId_7843 |

### Limiter (11 presets) — `query:AudioFx#Limiter`
| Name | URI |
|---|---|
| Fast.adv | query:AudioFx#Limiter:FileId_7601 |
| Independence.adv | query:AudioFx#Limiter:FileId_7602 |
| Lookahead.adv | query:AudioFx#Limiter:FileId_7603 |
| Low Latency.adv | query:AudioFx#Limiter:FileId_7604 |
| Maximizer.adv | query:AudioFx#Limiter:FileId_7605 |
| Mid-Side Limiter.adv | query:AudioFx#Limiter:FileId_7606 |
| Push.adv | query:AudioFx#Limiter:FileId_7607 |
| Reduce.adv | query:AudioFx#Limiter:FileId_7608 |
| Slow.adv | query:AudioFx#Limiter:FileId_7609 |
| True Peak Limiter.adv | query:AudioFx#Limiter:FileId_7610 |
| Upper Ceiling.adv | query:AudioFx#Limiter:FileId_7611 |

### Phaser-Flanger (12 presets) — `query:AudioFx#Phaser-Flanger`
| Name | URI |
|---|---|
| Doubler Default.adv | query:AudioFx#Phaser-Flanger:FileId_7551 |
| Doubler Ether.adv | query:AudioFx#Phaser-Flanger:FileId_7552 |
| Doubler Mirror.adv | query:AudioFx#Phaser-Flanger:FileId_7553 |
| Doubler Thick.adv | query:AudioFx#Phaser-Flanger:FileId_7554 |
| Flanger Default.adv | query:AudioFx#Phaser-Flanger:FileId_7555 |
| Flanger Rebound.adv | query:AudioFx#Phaser-Flanger:FileId_7556 |
| Flanger Spinning.adv | query:AudioFx#Phaser-Flanger:FileId_7557 |
| Flanger Warm.adv | query:AudioFx#Phaser-Flanger:FileId_7558 |
| Phaser Feedback.adv | query:AudioFx#Phaser-Flanger:FileId_7559 |
| Phaser Follower.adv | query:AudioFx#Phaser-Flanger:FileId_7560 |
| Phaser Guitar.adv | query:AudioFx#Phaser-Flanger:FileId_7561 |
| Phaser Particle Alliance.adv | query:AudioFx#Phaser-Flanger:FileId_7562 |

### Redux (9 presets) — `query:AudioFx#Redux` — bitcrusher; lo-fi go-to
| Name | URI |
|---|---|
| Chiptune Filter.adv | query:AudioFx#Redux:FileId_7542 |
| Dirt & Grit.adv | query:AudioFx#Redux:FileId_7543 |
| Epoxy Crush.adv | query:AudioFx#Redux:FileId_7544 |
| Kaputt.adv | query:AudioFx#Redux:FileId_7545 |
| Low Sample Rate.adv | query:AudioFx#Redux:FileId_7546 |
| New Mirage.adv | query:AudioFx#Redux:FileId_7547 |
| Some Dust.adv | query:AudioFx#Redux:FileId_7548 |
| Synth Bite.adv | query:AudioFx#Redux:FileId_7549 |
| Vintage Sampler.adv | query:AudioFx#Redux:FileId_7550 |

### Reverb — `query:AudioFx#Reverb` — presets in 3 subfolders (listed further below): Hall `query:AudioFx#Reverb:Hall`, Room `query:AudioFx#Reverb:Room`, Special `query:AudioFx#Reverb:Special`

### Saturator (22 presets) — `query:AudioFx#Saturator` — "808 Shaper" is the trap-808 pick
| Name | URI |
|---|---|
| 808 Shaper.adv | query:AudioFx#Saturator:FileId_7363 |
| A Bit Warmer.adv | query:AudioFx#Saturator:FileId_7364 |
| Analog Clip.adv | query:AudioFx#Saturator:FileId_7365 |
| Basic Soft.adv | query:AudioFx#Saturator:FileId_7366 |
| Beat Clipper.adv | query:AudioFx#Saturator:FileId_7367 |
| Crew Cut.adv | query:AudioFx#Saturator:FileId_7368 |
| Digital Clip Center.adv | query:AudioFx#Saturator:FileId_7369 |
| Gritty Bass.adv | query:AudioFx#Saturator:FileId_7370 |
| Hard Color.adv | query:AudioFx#Saturator:FileId_7371 |
| Hard Punch.adv | query:AudioFx#Saturator:FileId_7372 |
| Hot Tubes.adv | query:AudioFx#Saturator:FileId_7373 |
| Lurching Drums.adv | query:AudioFx#Saturator:FileId_7374 |
| Manic Smash.adv | query:AudioFx#Saturator:FileId_7375 |
| Mid-Range Phattener.adv | query:AudioFx#Saturator:FileId_7376 |
| Rage Clipper.adv | query:AudioFx#Saturator:FileId_7377 |
| Rectifier.adv | query:AudioFx#Saturator:FileId_7378 |
| Reso Grind.adv | query:AudioFx#Saturator:FileId_7379 |
| Rough Tone.adv | query:AudioFx#Saturator:FileId_7380 |
| Sinoid Fold.adv | query:AudioFx#Saturator:FileId_7381 |
| Soft Shaper.adv | query:AudioFx#Saturator:FileId_7382 |
| Warm Up Highs.adv | query:AudioFx#Saturator:FileId_7383 |
| Warm Up Lows.adv | query:AudioFx#Saturator:FileId_7384 |

### Tuner — `query:AudioFx#Tuner` — device only, no presets

### Utility (10 presets) — `query:AudioFx#Utility`
| Name | URI |
|---|---|
| Bass Mono.adv | query:AudioFx#Utility:FileId_7292 |
| Difference.adv | query:AudioFx#Utility:FileId_7293 |
| Left.adv | query:AudioFx#Utility:FileId_7294 |
| Mid Only.adv | query:AudioFx#Utility:FileId_7295 |
| Mono.adv | query:AudioFx#Utility:FileId_7296 |
| Narrow Stereo.adv | query:AudioFx#Utility:FileId_7297 |
| Phase Invert.adv | query:AudioFx#Utility:FileId_7298 |
| Right.adv | query:AudioFx#Utility:FileId_7299 |
| Sides Only.adv | query:AudioFx#Utility:FileId_7300 |
| Wide Stereo.adv | query:AudioFx#Utility:FileId_7301 |

### Audio Effect Rack presets
Device: `query:AudioFx#Audio%20Effect%20Rack`. Six subfolders. CAVEAT: several rack names reference devices absent from this edition (Glue Compressor, Multiband Dynamics, Drum Buss, Cabinet, Overdrive). They appear in the browser, but may load with those chain devices missing or greyed — verify with get_rack_chains (not get_device_parameters, which can't see inside a rack's nested chain) after loading.

#### Mixing & Mastering (46) — `query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering`
| Name | URI |
|---|---|
| Car Listening Environment.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5502 |
| Channel Kick.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5503 |
| Channel Snare.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5504 |
| Channel Strip Analog Tape.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5505 |
| Channel Strip Basic.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5506 |
| Channel Strip EQ & Cabinet.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5507 |
| Dirty Bounce.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5508 |
| Drum Buss Grand.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5509 |
| Drum Buss Gritty.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5510 |
| Drums Boombox.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5511 |
| Drums Core Effects.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5512 |
| Drums Crushed.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5513 |
| Drums Extra.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5514 |
| Drums Overdriven.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5515 |
| Drums Punchy.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5516 |
| Drums Studio.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5517 |
| Drums Warm & Wide.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5518 |
| Master Big Boom.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5521 |
| Master Bright & Edgy.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5522 |
| Master Crisp Saturation.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5523 |
| Master Dance Aggressive.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5524 |
| Master EQ & Compressor.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5525 |
| Master EQ & Glue.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5526 |
| Master Full Chain.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5527 |
| Master Meaty Analogue.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5528 |
| Master Overdriven Tape.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5529 |
| Master Parallel Punch.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5530 |
| Master Patience.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5531 |
| Master Punchy Dance.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5532 |
| Master Small Speaker.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5533 |
| Master Softknee.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5534 |
| Master Stereo Enhanced.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5535 |
| Master Wide & Warm.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5536 |
| Master Worn Out Vinyl.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5537 |
| Maximizer Minus Bar.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5538 |
| MS Rack EQ.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5519 |
| MS Rack Template.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5520 |
| Multiband & Limiter.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5540 |
| MultiComp & EQ Three.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5539 |
| Percussion Effects Basic.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5541 |
| S Suppresor.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5542 |
| Stereo Widener Mod.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5543 |
| Strings Submix.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5544 |
| Vocal Strip.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5545 |
| Voice Articulator.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5546 |
| Voice Enhancer.adg | query:AudioFx#Audio%20Effect%20Rack:Mixing%20&%20Mastering:FileId_5547 |

#### Amp Simulation (19) — `query:AudioFx#Audio%20Effect%20Rack:Amp%20Simulation` (Amp/Cabinet devices are not in this edition's device list — see caveat above)
| Name | URI |
|---|---|
| Basic Bass Amp.adg | query:AudioFx#Audio%20Effect%20Rack:Amp%20Simulation:FileId_5559 |
| Basic Heavy Guitar Amp.adg | query:AudioFx#Audio%20Effect%20Rack:Amp%20Simulation:FileId_5560 |
| Basic Lead Guitar Amp.adg | query:AudioFx#Audio%20Effect%20Rack:Amp%20Simulation:FileId_5561 |
| Basic Rock Dual Cab Guitar Amp.adg | query:AudioFx#Audio%20Effect%20Rack:Amp%20Simulation:FileId_5562 |
| Basic Stereo Chorus Jazz Amp.adg | query:AudioFx#Audio%20Effect%20Rack:Amp%20Simulation:FileId_5563 |
| Basic Tolex Crunch Guitar Amp.adg | query:AudioFx#Audio%20Effect%20Rack:Amp%20Simulation:FileId_5564 |
| Basic Twin Tremolo Guitar Amp.adg | query:AudioFx#Audio%20Effect%20Rack:Amp%20Simulation:FileId_5565 |
| Cabinet Mic Mixer.adg | query:AudioFx#Audio%20Effect%20Rack:Amp%20Simulation:FileId_5566 |
| Clean Guitar Amp.adg | query:AudioFx#Audio%20Effect%20Rack:Amp%20Simulation:FileId_5567 |
| Dreamy Amp Space.adg | query:AudioFx#Audio%20Effect%20Rack:Amp%20Simulation:FileId_5568 |
| Drop G Solo.adg | query:AudioFx#Audio%20Effect%20Rack:Amp%20Simulation:FileId_5569 |
| Electric Piano Amp.adg | query:AudioFx#Audio%20Effect%20Rack:Amp%20Simulation:FileId_5570 |
| Frontal Lobe.adg | query:AudioFx#Audio%20Effect%20Rack:Amp%20Simulation:FileId_5571 |
| Rhythm Chunks.adg | query:AudioFx#Audio%20Effect%20Rack:Amp%20Simulation:FileId_5572 |
| Scream Dream.adg | query:AudioFx#Audio%20Effect%20Rack:Amp%20Simulation:FileId_5573 |
| Slap Bass Amp.adg | query:AudioFx#Audio%20Effect%20Rack:Amp%20Simulation:FileId_5574 |
| Stevie Blues Stack.adg | query:AudioFx#Audio%20Effect%20Rack:Amp%20Simulation:FileId_5575 |
| Thick Trick.adg | query:AudioFx#Audio%20Effect%20Rack:Amp%20Simulation:FileId_5576 |
| Thump Bass Amp.adg | query:AudioFx#Audio%20Effect%20Rack:Amp%20Simulation:FileId_5577 |

#### Distortion (9) — `query:AudioFx#Audio%20Effect%20Rack:Distortion`
| Name | URI |
|---|---|
| Drum Noise Glitcher.adg | query:AudioFx#Audio%20Effect%20Rack:Distortion:FileId_5549 |
| Heavy Tube.adg | query:AudioFx#Audio%20Effect%20Rack:Distortion:FileId_5550 |
| Jimi's Feedback Guitar.adg | query:AudioFx#Audio%20Effect%20Rack:Distortion:FileId_5551 |
| Multi Waveshaper.adg | query:AudioFx#Audio%20Effect%20Rack:Distortion:FileId_5552 |
| Plug In & Wail.adg | query:AudioFx#Audio%20Effect%20Rack:Distortion:FileId_5553 |
| Power Chord Nation.adg | query:AudioFx#Audio%20Effect%20Rack:Distortion:FileId_5554 |
| Ruffhouse.adg | query:AudioFx#Audio%20Effect%20Rack:Distortion:FileId_5555 |
| Smokey Water.adg | query:AudioFx#Audio%20Effect%20Rack:Distortion:FileId_5556 |
| Vintage Tape Channel.adg | query:AudioFx#Audio%20Effect%20Rack:Distortion:FileId_5557 |

#### Modulation & Rhythmic (24) — `query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic` — "Ducker" = sidechain-style pumping rack; "Vinyl Warble"/"Tape Flutter"/"Drum Cassette" = lo-fi
| Name | URI |
|---|---|
| Alien Ice Cream.adg | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5477 |
| Creative Synth Buss.adg | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5478 |
| Crossover Phaser.adg | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5479 |
| Dirty Drum Synthesizer.adg | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5480 |
| Dirty Tape Head.adg | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5481 |
| Drum Cassette.adg | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5482 |
| Drum Transistor.adg | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5483 |
| Drumolish Squeeze.adg | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5484 |
| Ducker.adg | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5485 |
| Filter Dirty Stereo.adg | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5486 |
| Filter Phaser.adg | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5487 |
| Filter Tilter.adg | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5488 |
| Harmonic Tremolo.adg | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5489 |
| Jittery Swells.adg | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5490 |
| Loop Off Beat.adg | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5491 |
| Major Wah.adg | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5492 |
| Shortwave Dial.adg | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5493 |
| Strange Creatures.adg | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5494 |
| Sweep Overdrive.adg | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5495 |
| Tape Flutter.adg | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5496 |
| Tape Shaper.adg | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5497 |
| Trance Pad Gate.adg | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5498 |
| Vinyl Warble.adg | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5499 |
| Wah Pedal.adg | query:AudioFx#Audio%20Effect%20Rack:Modulation%20&%20Rhythmic:FileId_5500 |

#### Performance & DJ (15) — `query:AudioFx#Audio%20Effect%20Rack:Performance%20&%20DJ`
| Name | URI |
|---|---|
| Cut-o-matic.adg | query:AudioFx#Audio%20Effect%20Rack:Performance%20&%20DJ:FileId_5461 |
| DJ Master Channel.adg | query:AudioFx#Audio%20Effect%20Rack:Performance%20&%20DJ:FileId_5462 |
| DJ Tools.adg | query:AudioFx#Audio%20Effect%20Rack:Performance%20&%20DJ:FileId_5463 |
| EQ Three Rack.adg | query:AudioFx#Audio%20Effect%20Rack:Performance%20&%20DJ:FileId_5464 |
| Filter Driver.adg | query:AudioFx#Audio%20Effect%20Rack:Performance%20&%20DJ:FileId_5465 |
| Filter Pumper.adg | query:AudioFx#Audio%20Effect%20Rack:Performance%20&%20DJ:FileId_5466 |
| Frozen Smear.adg | query:AudioFx#Audio%20Effect%20Rack:Performance%20&%20DJ:FileId_5467 |
| Instant Repeat.adg | query:AudioFx#Audio%20Effect%20Rack:Performance%20&%20DJ:FileId_5468 |
| Kamoni Live Strip.adg | query:AudioFx#Audio%20Effect%20Rack:Performance%20&%20DJ:FileId_5469 |
| Knob 1 Fade to Grey.adg | query:AudioFx#Audio%20Effect%20Rack:Performance%20&%20DJ:FileId_5470 |
| Knob 1 Super Looper.adg | query:AudioFx#Audio%20Effect%20Rack:Performance%20&%20DJ:FileId_5471 |
| Module Later.adg | query:AudioFx#Audio%20Effect%20Rack:Performance%20&%20DJ:FileId_5472 |
| Re-Pulsor.adg | query:AudioFx#Audio%20Effect%20Rack:Performance%20&%20DJ:FileId_5473 |
| Washed Out.adg | query:AudioFx#Audio%20Effect%20Rack:Performance%20&%20DJ:FileId_5474 |
| Zone 62 DJ EQ.adg | query:AudioFx#Audio%20Effect%20Rack:Performance%20&%20DJ:FileId_5475 |

#### Space (33) — `query:AudioFx#Audio%20Effect%20Rack:Space` — delay/reverb racks; "Adlib Delay" & "Dub Echo" are the vocal/throw picks
| Name | URI |
|---|---|
| 3 Band Ambience Reverb.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5427 |
| Adlib Delay.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5428 |
| Ample Space Delay.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5429 |
| Bit-ter.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5430 |
| Buck Jones.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5431 |
| Call Back.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5432 |
| Chamber Trio Delay.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5433 |
| Chorus Echo.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5434 |
| Compressed Room Reverb.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5435 |
| Constantine Apple.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5436 |
| Delayed Hall Reverb.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5437 |
| Delayed Room Reverb.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5438 |
| Drop In The Bucket.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5439 |
| Dub Echo.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5440 |
| Eastern Brain.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5441 |
| Echo Fuzz.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5442 |
| Echo Grains.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5443 |
| Elephant Smile.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5444 |
| Fadeaway.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5445 |
| Ghostly Swirls.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5446 |
| Guitar Echo.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5447 |
| Hang Up.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5448 |
| Jamaica Plains.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5449 |
| Mid-Side Echo Distort.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5450 |
| Multiband Beat Repeat Echo.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5451 |
| Multiband Delay Notes Stereo .adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5452 |
| Neptune Rising.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5453 |
| Octo Room.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5454 |
| Out Of Orbit.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5455 |
| Rhythmic Space.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5456 |
| Rub A Dub.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5457 |
| Stun Echo.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5458 |
| Verb Expand.adg | query:AudioFx#Audio%20Effect%20Rack:Space:FileId_5459 |

### Delay presets (device `query:AudioFx#Delay`)
#### Delay / Ambient Spaces (7) — `query:AudioFx#Delay:Ambient%20Spaces`
| Name | URI |
|---|---|
| Disharmonics.adv | query:AudioFx#Delay:Ambient%20Spaces:FileId_8031 |
| Full Range Spatial.adv | query:AudioFx#Delay:Ambient%20Spaces:FileId_8032 |
| Harmonics.adv | query:AudioFx#Delay:Ambient%20Spaces:FileId_8033 |
| Hi Buzz.adv | query:AudioFx#Delay:Ambient%20Spaces:FileId_8034 |
| Pan Left.adv | query:AudioFx#Delay:Ambient%20Spaces:FileId_8035 |
| Pan Right.adv | query:AudioFx#Delay:Ambient%20Spaces:FileId_8036 |
| Robot.adv | query:AudioFx#Delay:Ambient%20Spaces:FileId_8037 |

#### Delay / Clean Delay (17) — `query:AudioFx#Delay:Clean%20Delay`
| Name | URI |
|---|---|
| 4th Bandpass.adv | query:AudioFx#Delay:Clean%20Delay:FileId_8015 |
| 4th Distant.adv | query:AudioFx#Delay:Clean%20Delay:FileId_8016 |
| 8th Groove.adv | query:AudioFx#Delay:Clean%20Delay:FileId_8017 |
| 16th Dub.adv | query:AudioFx#Delay:Clean%20Delay:FileId_8013 |
| 16th Ping Pong.adv | query:AudioFx#Delay:Clean%20Delay:FileId_8014 |
| Dotted Eighth Note.adv | query:AudioFx#Delay:Clean%20Delay:FileId_8018 |
| Dotted Quarter Note.adv | query:AudioFx#Delay:Clean%20Delay:FileId_8019 |
| Eighth Note.adv | query:AudioFx#Delay:Clean%20Delay:FileId_8020 |
| Groove.adv | query:AudioFx#Delay:Clean%20Delay:FileId_8021 |
| High.adv | query:AudioFx#Delay:Clean%20Delay:FileId_8022 |
| Longest Ping Pong.adv | query:AudioFx#Delay:Clean%20Delay:FileId_8023 |
| Ping.adv | query:AudioFx#Delay:Clean%20Delay:FileId_8024 |
| Pong.adv | query:AudioFx#Delay:Clean%20Delay:FileId_8025 |
| Quarter Note.adv | query:AudioFx#Delay:Clean%20Delay:FileId_8026 |
| Sixteenth Note.adv | query:AudioFx#Delay:Clean%20Delay:FileId_8027 |
| Slight Slap.adv | query:AudioFx#Delay:Clean%20Delay:FileId_8028 |
| Uneven Two Beat.adv | query:AudioFx#Delay:Clean%20Delay:FileId_8029 |

#### Delay / Modulated Delay (5) — `query:AudioFx#Delay:Modulated%20Delay`
| Name | URI |
|---|---|
| Chopped Delay.adv | query:AudioFx#Delay:Modulated%20Delay:FileId_8007 |
| Fake Phaser.adv | query:AudioFx#Delay:Modulated%20Delay:FileId_8008 |
| Glitch Delay.adv | query:AudioFx#Delay:Modulated%20Delay:FileId_8009 |
| Simple Chorus.adv | query:AudioFx#Delay:Modulated%20Delay:FileId_8010 |
| Simple Flanger.adv | query:AudioFx#Delay:Modulated%20Delay:FileId_8011 |

#### Delay / Vintage Delay (2) — `query:AudioFx#Delay:Vintage%20Delay`
| Name | URI |
|---|---|
| Flutter.adv | query:AudioFx#Delay:Vintage%20Delay:FileId_8004 |
| Sloppy Delay.adv | query:AudioFx#Delay:Vintage%20Delay:FileId_8005 |

### Reverb presets (device `query:AudioFx#Reverb`)
#### Reverb / Hall (25) — `query:AudioFx#Reverb:Hall` — "Vocal Hall"/"Vocal Space" for vocals; "Long Tail"/"Cathedral" for ambient
| Name | URI |
|---|---|
| Arena Tail.adv | query:AudioFx#Reverb:Hall:FileId_7506 |
| Ballad Reverb.adv | query:AudioFx#Reverb:Hall:FileId_7507 |
| Cathedral.adv | query:AudioFx#Reverb:Hall:FileId_7508 |
| Church.adv | query:AudioFx#Reverb:Hall:FileId_7509 |
| Concert Hall.adv | query:AudioFx#Reverb:Hall:FileId_7510 |
| Dark Hall.adv | query:AudioFx#Reverb:Hall:FileId_7511 |
| Foyer.adv | query:AudioFx#Reverb:Hall:FileId_7512 |
| Gymnasium.adv | query:AudioFx#Reverb:Hall:FileId_7513 |
| Hall Damped.adv | query:AudioFx#Reverb:Hall:FileId_7514 |
| Hall Shine.adv | query:AudioFx#Reverb:Hall:FileId_7515 |
| Large Factory.adv | query:AudioFx#Reverb:Hall:FileId_7516 |
| Large Hall.adv | query:AudioFx#Reverb:Hall:FileId_7517 |
| Large Stage.adv | query:AudioFx#Reverb:Hall:FileId_7518 |
| Late Wrapper.adv | query:AudioFx#Reverb:Hall:FileId_7519 |
| Long Tail.adv | query:AudioFx#Reverb:Hall:FileId_7520 |
| Main Hall.adv | query:AudioFx#Reverb:Hall:FileId_7521 |
| Medium Concert.adv | query:AudioFx#Reverb:Hall:FileId_7522 |
| Medium Hall.adv | query:AudioFx#Reverb:Hall:FileId_7523 |
| Medium Stage.adv | query:AudioFx#Reverb:Hall:FileId_7524 |
| Small Hall.adv | query:AudioFx#Reverb:Hall:FileId_7525 |
| Spacious.adv | query:AudioFx#Reverb:Hall:FileId_7526 |
| Vocal Hall.adv | query:AudioFx#Reverb:Hall:FileId_7527 |
| Vocal Space.adv | query:AudioFx#Reverb:Hall:FileId_7528 |
| Warm Reverb Long.adv | query:AudioFx#Reverb:Hall:FileId_7529 |
| Wooden Hall.adv | query:AudioFx#Reverb:Hall:FileId_7530 |

#### Reverb / Room (32) — `query:AudioFx#Reverb:Room` — "Drums Room"/"Snare Room"/"Plate Damped" for drums; "Ambience" for glue
| Name | URI |
|---|---|
| Ambience Medium.adv | query:AudioFx#Reverb:Room:FileId_7473 |
| Ambience.adv | query:AudioFx#Reverb:Room:FileId_7474 |
| Backbone.adv | query:AudioFx#Reverb:Room:FileId_7475 |
| Big Room.adv | query:AudioFx#Reverb:Room:FileId_7476 |
| Bright Room.adv | query:AudioFx#Reverb:Room:FileId_7477 |
| Concrete Chamber.adv | query:AudioFx#Reverb:Room:FileId_7478 |
| Corridor.adv | query:AudioFx#Reverb:Room:FileId_7479 |
| Dark Medium Room.adv | query:AudioFx#Reverb:Room:FileId_7480 |
| Dark Small Room.adv | query:AudioFx#Reverb:Room:FileId_7481 |
| Drums Room.adv | query:AudioFx#Reverb:Room:FileId_7482 |
| Garage.adv | query:AudioFx#Reverb:Room:FileId_7483 |
| Guitar Room.adv | query:AudioFx#Reverb:Room:FileId_7484 |
| High Verb.adv | query:AudioFx#Reverb:Room:FileId_7485 |
| In A Box.adv | query:AudioFx#Reverb:Room:FileId_7486 |
| Large Chamber.adv | query:AudioFx#Reverb:Room:FileId_7487 |
| Living Room.adv | query:AudioFx#Reverb:Room:FileId_7488 |
| Long Ambience.adv | query:AudioFx#Reverb:Room:FileId_7489 |
| Marble Lobby.adv | query:AudioFx#Reverb:Room:FileId_7490 |
| Medium Room.adv | query:AudioFx#Reverb:Room:FileId_7491 |
| Museum Lobby.adv | query:AudioFx#Reverb:Room:FileId_7492 |
| Office.adv | query:AudioFx#Reverb:Room:FileId_7493 |
| Plate Damped.adv | query:AudioFx#Reverb:Room:FileId_7494 |
| Room Wood.adv | query:AudioFx#Reverb:Room:FileId_7495 |
| Small Chamber.adv | query:AudioFx#Reverb:Room:FileId_7496 |
| Small Room.adv | query:AudioFx#Reverb:Room:FileId_7497 |
| Small Tile.adv | query:AudioFx#Reverb:Room:FileId_7498 |
| Snare Room.adv | query:AudioFx#Reverb:Room:FileId_7499 |
| Standard Room.adv | query:AudioFx#Reverb:Room:FileId_7500 |
| Storage Space.adv | query:AudioFx#Reverb:Room:FileId_7501 |
| Tile Room.adv | query:AudioFx#Reverb:Room:FileId_7502 |
| Venus Bright.adv | query:AudioFx#Reverb:Room:FileId_7503 |
| Wooden Room.adv | query:AudioFx#Reverb:Room:FileId_7504 |

#### Reverb / Special (22) — `query:AudioFx#Reverb:Special`
| Name | URI |
|---|---|
| Basement.adv | query:AudioFx#Reverb:Special:FileId_7450 |
| Bright Long Verb.adv | query:AudioFx#Reverb:Special:FileId_7451 |
| Bright Reflections.adv | query:AudioFx#Reverb:Special:FileId_7452 |
| Empty Club.adv | query:AudioFx#Reverb:Special:FileId_7453 |
| Forest Floor.adv | query:AudioFx#Reverb:Special:FileId_7454 |
| Frozen Build Up.adv | query:AudioFx#Reverb:Special:FileId_7455 |
| Halluzinatione.adv | query:AudioFx#Reverb:Special:FileId_7456 |
| Large Space Chorus.adv | query:AudioFx#Reverb:Special:FileId_7457 |
| Oil Barrel.adv | query:AudioFx#Reverb:Special:FileId_7458 |
| Outer Space.adv | query:AudioFx#Reverb:Special:FileId_7459 |
| Parallel Walls.adv | query:AudioFx#Reverb:Special:FileId_7460 |
| Parking Garage.adv | query:AudioFx#Reverb:Special:FileId_7461 |
| Red Canyon.adv | query:AudioFx#Reverb:Special:FileId_7462 |
| Reflections.adv | query:AudioFx#Reverb:Special:FileId_7463 |
| Short Ambience.adv | query:AudioFx#Reverb:Special:FileId_7464 |
| Singing Can.adv | query:AudioFx#Reverb:Special:FileId_7465 |
| Six Seconds.adv | query:AudioFx#Reverb:Special:FileId_7466 |
| Sixty Seconds.adv | query:AudioFx#Reverb:Special:FileId_7467 |
| Sizzle.adv | query:AudioFx#Reverb:Special:FileId_7468 |
| Space Reverb.adv | query:AudioFx#Reverb:Special:FileId_7469 |
| Stadium.adv | query:AudioFx#Reverb:Special:FileId_7470 |
| Wide Ambience.adv | query:AudioFx#Reverb:Special:FileId_7471 |


## MIDI Effects
Path: `midi_effects` (underscore form). URI root `query:MidiFx`. 12 devices; no "MIDI Tools" (generators/transformers) folder — consistent with Intro/Lite.

| Device | URI | Presets |
|---|---|---|
| Arpeggiator | query:MidiFx#Arpeggiator | 7 |
| CC Control | query:MidiFx#CC%20Control | device only |
| Chord | query:MidiFx#Chord | 21 |
| Expression Control | query:MidiFx#Expression%20Control | device only |
| MIDI Effect Rack | query:MidiFx#MIDI%20Effect%20Rack | 19 racks in 3 subfolders |
| MIDI Monitor | query:MidiFx#MIDI%20Monitor | device only |
| MPE Control | query:MidiFx#MPE%20Control | 7 |
| Note Length | query:MidiFx#Note%20Length | 4 |
| Pitch | query:MidiFx#Pitch | 3 |
| Random | query:MidiFx#Random | 8 |
| Scale | query:MidiFx#Scale | 36 |
| Velocity | query:MidiFx#Velocity | 15 |

### Arpeggiator (7 presets) — `query:MidiFx#Arpeggiator`
| Name | URI |
|---|---|
| Bach 16th.adv | query:MidiFx#Arpeggiator:FileId_6071 |
| Bouncy Chords.adv | query:MidiFx#Arpeggiator:FileId_6072 |
| C Major Walk 16th Grooved.adv | query:MidiFx#Arpeggiator:FileId_6073 |
| Classic UpDown 8th.adv | query:MidiFx#Arpeggiator:FileId_6074 |
| Descending Chords 12th.adv | query:MidiFx#Arpeggiator:FileId_6075 |
| Housier Than Thou.adv | query:MidiFx#Arpeggiator:FileId_6076 |
| Ubiquitous.adv | query:MidiFx#Arpeggiator:FileId_6077 |

### Chord (21 presets) — `query:MidiFx#Chord`
| Name | URI |
|---|---|
| Add Fifth.adv | query:MidiFx#Chord:FileId_6050 |
| Add Fourth.adv | query:MidiFx#Chord:FileId_6051 |
| Debusian.adv | query:MidiFx#Chord:FileId_6052 |
| Einfach Schoen.adv | query:MidiFx#Chord:FileId_6053 |
| Eternal Sunshine.adv | query:MidiFx#Chord:FileId_6054 |
| Fifth Chord.adv | query:MidiFx#Chord:FileId_6055 |
| Film Noir.adv | query:MidiFx#Chord:FileId_6056 |
| Fourth Chord.adv | query:MidiFx#Chord:FileId_6057 |
| Grandiosa.adv | query:MidiFx#Chord:FileId_6058 |
| Half-dim 7 Chord.adv | query:MidiFx#Chord:FileId_6059 |
| House for to go.adv | query:MidiFx#Chord:FileId_6060 |
| Jazz for Dummies.adv | query:MidiFx#Chord:FileId_6061 |
| Ligetian.adv | query:MidiFx#Chord:FileId_6062 |
| Major 6 Chord.adv | query:MidiFx#Chord:FileId_6063 |
| Major 7 Chord.adv | query:MidiFx#Chord:FileId_6064 |
| Major Triad.adv | query:MidiFx#Chord:FileId_6065 |
| Minor 7 Chord.adv | query:MidiFx#Chord:FileId_6066 |
| Minor Triad.adv | query:MidiFx#Chord:FileId_6067 |
| Stacked Fifths.adv | query:MidiFx#Chord:FileId_6068 |
| Stacked Fourths.adv | query:MidiFx#Chord:FileId_6069 |
| Zukunft Futur.adv | query:MidiFx#Chord:FileId_6070 |

### MIDI Effect Rack — `query:MidiFx#MIDI%20Effect%20Rack` — presets in 3 subfolders (listed below): Experimental `query:MidiFx#MIDI%20Effect%20Rack:Experimental`, Rhythmic `query:MidiFx#MIDI%20Effect%20Rack:Rhythmic`, Utility `query:MidiFx#MIDI%20Effect%20Rack:Utility`

### MPE Control (7 presets) — `query:MidiFx#MPE%20Control`
| Name | URI |
|---|---|
| Force Relative Slide.adv | query:MidiFx#MPE%20Control:FileId_6038 |
| MPE Off.adv | query:MidiFx#MPE%20Control:FileId_6039 |
| MPE to MIDI.adv | query:MidiFx#MPE%20Control:FileId_6040 |
| Note PB 25.adv | query:MidiFx#MPE%20Control:FileId_6041 |
| Note PB 50.adv | query:MidiFx#MPE%20Control:FileId_6042 |
| Note PB Off.adv | query:MidiFx#MPE%20Control:FileId_6043 |
| Pressure and Slide Invert.adv | query:MidiFx#MPE%20Control:FileId_6044 |

### Note Length (4 presets) — `query:MidiFx#Note%20Length`
| Name | URI |
|---|---|
| 16th Notes.adv | query:MidiFx#Note%20Length:FileId_6024 |
| Note Off.adv | query:MidiFx#Note%20Length:FileId_6025 |
| Ten Milliseconds.adv | query:MidiFx#Note%20Length:FileId_6026 |
| Ten Seconds.adv | query:MidiFx#Note%20Length:FileId_6027 |

### Pitch (3 presets) — `query:MidiFx#Pitch`
| Name | URI |
|---|---|
| + 12.adv | query:MidiFx#Pitch:FileId_6021 |
| + 24.adv | query:MidiFx#Pitch:FileId_6022 |
| - 12.adv | query:MidiFx#Pitch:FileId_6023 |

### Random (8 presets) — `query:MidiFx#Random`
| Name | URI |
|---|---|
| Blue.adv | query:MidiFx#Random:FileId_6013 |
| Chaos.adv | query:MidiFx#Random:FileId_6014 |
| Drama.adv | query:MidiFx#Random:FileId_6015 |
| Fifth.adv | query:MidiFx#Random:FileId_6016 |
| Forced Jazz.adv | query:MidiFx#Random:FileId_6017 |
| Jazz Again.adv | query:MidiFx#Random:FileId_6018 |
| Low Oct.adv | query:MidiFx#Random:FileId_6019 |
| Orange.adv | query:MidiFx#Random:FileId_6020 |

### Scale (36 presets) — `query:MidiFx#Scale`
| Name | URI |
|---|---|
| 8-Tone Spanish.adv | query:MidiFx#Scale:FileId_5977 |
| Bhairav.adv | query:MidiFx#Scale:FileId_5978 |
| Dorian #4.adv | query:MidiFx#Scale:FileId_5979 |
| Dorian.adv | query:MidiFx#Scale:FileId_5980 |
| Half-Whole Diminished.adv | query:MidiFx#Scale:FileId_5981 |
| Harmonic Major.adv | query:MidiFx#Scale:FileId_5982 |
| Harmonic Minor.adv | query:MidiFx#Scale:FileId_5983 |
| Hirajoshi.adv | query:MidiFx#Scale:FileId_5984 |
| Hungarian Minor.adv | query:MidiFx#Scale:FileId_5985 |
| In-Sen.adv | query:MidiFx#Scale:FileId_5986 |
| Iwato.adv | query:MidiFx#Scale:FileId_5987 |
| Kumoi.adv | query:MidiFx#Scale:FileId_5988 |
| Locrian.adv | query:MidiFx#Scale:FileId_5989 |
| Lydian Augmented.adv | query:MidiFx#Scale:FileId_5990 |
| Lydian Dominant.adv | query:MidiFx#Scale:FileId_5991 |
| Lydian.adv | query:MidiFx#Scale:FileId_5992 |
| Major Pentatonic.adv | query:MidiFx#Scale:FileId_5993 |
| Major.adv | query:MidiFx#Scale:FileId_5994 |
| Melodic Minor Ascending.adv | query:MidiFx#Scale:FileId_5995 |
| Melodic Minor Descending.adv | query:MidiFx#Scale:FileId_5996 |
| Messiaen 3.adv | query:MidiFx#Scale:FileId_5997 |
| Messiaen 4.adv | query:MidiFx#Scale:FileId_5998 |
| Messiaen 5.adv | query:MidiFx#Scale:FileId_5999 |
| Messiaen 6.adv | query:MidiFx#Scale:FileId_6000 |
| Messiaen 7.adv | query:MidiFx#Scale:FileId_6001 |
| Minor Blues.adv | query:MidiFx#Scale:FileId_6002 |
| Minor Pentatonic.adv | query:MidiFx#Scale:FileId_6003 |
| Minor.adv | query:MidiFx#Scale:FileId_6004 |
| Mixolydian.adv | query:MidiFx#Scale:FileId_6005 |
| Pelog Selisir.adv | query:MidiFx#Scale:FileId_6006 |
| Pelog Tembung.adv | query:MidiFx#Scale:FileId_6007 |
| Phrygian Dominant.adv | query:MidiFx#Scale:FileId_6008 |
| Phrygian.adv | query:MidiFx#Scale:FileId_6009 |
| Super Locrian.adv | query:MidiFx#Scale:FileId_6010 |
| Whole Tone.adv | query:MidiFx#Scale:FileId_6011 |
| Whole-Half Diminished.adv | query:MidiFx#Scale:FileId_6012 |

### Velocity (15 presets) — `query:MidiFx#Velocity`
| Name | URI |
|---|---|
| Add some Random.adv | query:MidiFx#Velocity:FileId_5962 |
| Compression I.adv | query:MidiFx#Velocity:FileId_5963 |
| Compression II.adv | query:MidiFx#Velocity:FileId_5964 |
| Cut Above 64.adv | query:MidiFx#Velocity:FileId_5965 |
| Dynamic I.adv | query:MidiFx#Velocity:FileId_5966 |
| Dynamic II.adv | query:MidiFx#Velocity:FileId_5967 |
| Fix 1.adv | query:MidiFx#Velocity:FileId_5968 |
| Fix 32.adv | query:MidiFx#Velocity:FileId_5970 |
| Fix 64.adv | query:MidiFx#Velocity:FileId_5971 |
| Fix 96.adv | query:MidiFx#Velocity:FileId_5972 |
| Fix 127.adv | query:MidiFx#Velocity:FileId_5969 |
| Forte.adv | query:MidiFx#Velocity:FileId_5973 |
| Invert.adv | query:MidiFx#Velocity:FileId_5974 |
| Piano.adv | query:MidiFx#Velocity:FileId_5975 |
| Total Random.adv | query:MidiFx#Velocity:FileId_5976 |

### MIDI Effect Rack presets
#### Experimental (3) — `query:MidiFx#MIDI%20Effect%20Rack:Experimental`
| Name | URI |
|---|---|
| Chord Echo Variations.adg | query:MidiFx#MIDI%20Effect%20Rack:Experimental:FileId_4513 |
| One Note Twist.adg | query:MidiFx#MIDI%20Effect%20Rack:Experimental:FileId_4514 |
| Scale Driver.adg | query:MidiFx#MIDI%20Effect%20Rack:Experimental:FileId_4515 |

#### Rhythmic (12) — `query:MidiFx#MIDI%20Effect%20Rack:Rhythmic`
| Name | URI |
|---|---|
| Arp Autobahn.adg | query:MidiFx#MIDI%20Effect%20Rack:Rhythmic:FileId_4500 |
| Arp Chance.adg | query:MidiFx#MIDI%20Effect%20Rack:Rhythmic:FileId_4501 |
| Arp Chord.adg | query:MidiFx#MIDI%20Effect%20Rack:Rhythmic:FileId_4502 |
| Arp Descending Note.adg | query:MidiFx#MIDI%20Effect%20Rack:Rhythmic:FileId_4503 |
| Arp Double.adg | query:MidiFx#MIDI%20Effect%20Rack:Rhythmic:FileId_4504 |
| Arp Harmony.adg | query:MidiFx#MIDI%20Effect%20Rack:Rhythmic:FileId_4505 |
| Arp Progressive.adg | query:MidiFx#MIDI%20Effect%20Rack:Rhythmic:FileId_4506 |
| Arp Streets Echo.adg | query:MidiFx#MIDI%20Effect%20Rack:Rhythmic:FileId_4507 |
| Arp Up.adg | query:MidiFx#MIDI%20Effect%20Rack:Rhythmic:FileId_4508 |
| Arp Variations.adg | query:MidiFx#MIDI%20Effect%20Rack:Rhythmic:FileId_4509 |
| Echo Note Bounce.adg | query:MidiFx#MIDI%20Effect%20Rack:Rhythmic:FileId_4510 |
| Echo Single Strum.adg | query:MidiFx#MIDI%20Effect%20Rack:Rhythmic:FileId_4511 |

#### Utility (4) — `query:MidiFx#MIDI%20Effect%20Rack:Utility`
| Name | URI |
|---|---|
| Keys & Scales.adg | query:MidiFx#MIDI%20Effect%20Rack:Utility:FileId_4495 |
| MIDI to MPE.adg | query:MidiFx#MIDI%20Effect%20Rack:Utility:FileId_4496 |
| MPE Invert.adg | query:MidiFx#MIDI%20Effect%20Rack:Utility:FileId_4497 |
| MPE Note PB Range.adg | query:MidiFx#MIDI%20Effect%20Rack:Utility:FileId_4498 |


## Max for Live
Path: `max_for_live`. URI root `query:M4L`. **Nothing loadable.** Only three placeholder entries exist and every one reports `is_loadable: false` — Max for Live is not licensed/installed in this edition. Do not try to load LFO, Envelope Follower, Shaper, CV Tools, Granulator, etc.

| Entry | URI | Loadable |
|---|---|---|
| Max Audio Effect | query:M4L#Max%20Audio%20Effect | no |
| Max Instrument | query:M4L#Max%20Instrument | no |
| Max MIDI Effect | query:M4L#Max%20MIDI%20Effect | no |

## Plugins
Path: `plugins`. URI root `query:Plugins`. **EMPTY — no third-party VST2/VST3/AU plugins are installed or enabled.** `get_browser_items_at_path("plugins")` returns `items: []` and the node itself is not a folder. There are no vendor folders (no Serum, Vital, Kontakt, Omnisphere, Arturia, Native Instruments, iZotope, FabFilter, Waves, Spitfire, etc.). If the user believes plugins are installed, the plugin folders/AU scan must be enabled in Live > Settings > Plug-Ins and Live rescanned; until then, all sound design must use the native devices above.

## Packs
Path: `packs`. URI root `query:LivePacks`. **Only ONE pack is installed: Core Library.** No add-on packs (no Session Drums, Drum Booth, Orchestral Strings/Brass/Woodwinds, Grand Piano, Vocal packs, Skitter & Step, Drive & Glow, Build & Drop, Chop & Swing, Latin Percussion, etc.). Everything in Sounds/Drums/Effects above comes from Core Library.

| Pack | URI | Contents (one level) |
|---|---|---|
| Core Library | query:LivePacks#www.ableton.com/0 | Devices (`…/0:Devices`), Grooves (`…/0:Grooves`), MIDI Clips (`…/0:MIDI%20Clips`), Racks (`…/0:Racks`), Samples (`…/0:Samples`), Templates (`…/0:Templates`), Tunings (`…/0:Tunings`) |

Full subfolder URIs: `query:LivePacks#www.ableton.com/0:Devices`, `query:LivePacks#www.ableton.com/0:Grooves`, `query:LivePacks#www.ableton.com/0:MIDI%20Clips`, `query:LivePacks#www.ableton.com/0:Racks`, `query:LivePacks#www.ableton.com/0:Samples`, `query:LivePacks#www.ableton.com/0:Templates`, `query:LivePacks#www.ableton.com/0:Tunings`.
Note: the Grooves folder is also reachable via the `get_grooves` tool; Tunings holds .ascl scale files for Live 12's tuning system.

## User Library
Path: `user_library`. URI root `query:UserLibrary`. **Effectively empty — no user-saved presets, samples, clips, grooves, templates or tunings.** Enumerated two levels deep; every leaf is an auto-created empty placeholder (`is_folder: false, is_loadable: false`).

| Level 1 | Level 2 | Notes |
|---|---|---|
| Clips (`query:UserLibrary#Clips`) | — | empty |
| Defaults (`query:UserLibrary#Defaults`) | Audio Effects, Audio to MIDI*, Creating Tracks*, Dropping Samples*, Instruments, MIDI Effects, Slicing | Live's stock default-preset slots; * are folders but hold only Live's defaults, nothing user-made |
| Grooves (`query:UserLibrary#Grooves`) | — | empty |
| MIDI Tools (`query:UserLibrary#MIDI%20Tools`) | Max Generators, Max Transformations | both empty placeholders (M4L not available anyway) |
| Presets (`query:UserLibrary#Presets`) | Audio Effects (21 empty per-device slots), Instruments (6 empty slots: Drift, Drum Rack, Drum Sampler, Impulse, Instrument Rack, Simpler), MIDI Effects (9 empty slots) | no saved presets. Curiosity: the Audio Effects slots include "Repitch", "Chorus", "Auto Filter Legacy", "Redux Legacy" — names not present in the Audio Effects browser category (legacy/hidden devices). |
| Remote Scripts (`query:UserLibrary#Remote%20Scripts`) | AbletonMCP (`query:UserLibrary#Remote%20Scripts:AbletonMCP`) | the MCP bridge's own control-surface script |
| Samples (`query:UserLibrary#Samples`) | — | empty |
| Templates (`query:UserLibrary#Templates`) | — | empty |
| Tunings (`query:UserLibrary#Tunings`) | — | empty |

## Samples
Path: `samples`. URI root `query:Samples`; item URI pattern `query:Samples#FileId_NNNN` (FileId 399–3988). **3,503 files, flat — no subfolders.** 2,188 .wav + 1,315 .aif. Loading a sample URI with load_instrument_or_effect drops it into a Simpler. Names are `<Family> <descriptor> [N]` or, for loops, `<Name> [Key] <NNN> bpm`. 171 files are bpm-tagged loops. The drum one-shots here are the same files exposed under Drums/Drum Hits (different URIs, same audio).
Prefer `search_browser("<term>")` over walking this list — searching "Vocal", "GrandPiano", "Upright", "bpm" hits these directly.

### Family counts (first word of filename)
| Family | Count | Family | Count | Family | Count |
|---|---|---|---|---|---|
| Snare | 413 | Hihat | 399 | Kick | 399 |
| Tom | 326 | GrandPiano | 120 | E-Perc | 108 |
| Clap | 105 | Rim | 97 | FX | 84 |
| Synth | 72 | Ride | 70 | Crash | 61 |
| Shaker | 57 | Stab | 56 | Perc | 52 |
| Vocal | 52 | Conga | 50 | Cymbal | 39 |
| Wood | 39 | Cowbell | 37 | Tamb | 34 |
| Sandblaster | 24 | 808 | 23 | Smooth | 22 |
| Ob | 21 | Galactica | 20 | ARP | 19 |
| Bass | 18 | Bell | 18 | E-Piano | 17 |
| Guitar | 17 | Mallet | 17 | Bongo | 14 |
| Impact | 14 | Infected | 14 | Machine | 14 |
| Mamas | 13 | Phantasm | 13 | Sh | 13 |
| Triangle | 13 | Break | 12 | Lo | 12 |
| Upright | 12 | Byte | 11 | Cabasa | 11 |
| Electroflow | 11 | Pulse | 11 | Atmos | 10 |
| Clave | 10 | Metallic | 10 | Tabla | 9 |
| Ikembe | 8 | Strings | 8 | Ambient | 7 |
| Dark | 7 | Riser | 7 | Snap | 7 |
| Timbale | 7 | Organ | 6 | Saw | 6 |

…plus 204 rarer first-words (single loops, textures, one-offs).

### Non-drum families — representative name → URI
| Family (count) | Representatives |
|---|---|
| GrandPiano (120) | GrandPiano A# 1 f.aif → `query:Samples#FileId_3497`<br>GrandPiano B5 f.aif → `query:Samples#FileId_3521`<br>GrandPiano C4 f.aif → `query:Samples#FileId_3545`<br>GrandPiano D#5 f.aif → `query:Samples#FileId_3569`<br>GrandPiano F#4 f.aif → `query:Samples#FileId_3593` |
| Vocal (52) | Vocal 05.wav → `query:Samples#FileId_399`<br>Vocal Chant Yeah.aif → `query:Samples#FileId_409`<br>Vocal Demo Know.aif → `query:Samples#FileId_416`<br>Vocal Inhale.wav → `query:Samples#FileId_424`<br>Vocal Screeeem.aif → `query:Samples#FileId_429` |
| Guitar (17) | Guitar Acoustic C3.aif → `query:Samples#FileId_656`<br>Guitar Electric Bend C3.aif → `query:Samples#FileId_659`<br>Guitar Electric Taka Gbmin7.wav → `query:Samples#FileId_662`<br>Guitar Jazz Mute C2.wav → `query:Samples#FileId_665`<br>Guitar Pluck and Bow G.aif → `query:Samples#FileId_3800` |
| Upright (12) | Upright Home Piano C1.aif → `query:Samples#FileId_3137`<br>Upright Home Piano C3.aif → `query:Samples#FileId_3139`<br>Upright Home Piano C5.aif → `query:Samples#FileId_3141`<br>Upright Home Piano G2.aif → `query:Samples#FileId_3143`<br>Upright Home Piano G4.aif → `query:Samples#FileId_3145` |
| Strings (8) | Strings Amin7.aif → `query:Samples#FileId_603`<br>Strings Bmin7.aif → `query:Samples#FileId_604`<br>Strings Ens C4.wav → `query:Samples#FileId_605`<br>Strings Motion C4.wav → `query:Samples#FileId_606`<br>Strings Orch C4.wav → `query:Samples#FileId_607` |
| Bass (18) | Bass 04 A.aif → `query:Samples#FileId_679`<br>Bass Deep Money D1.aif → `query:Samples#FileId_682`<br>Bass Given E1.wav → `query:Samples#FileId_527`<br>Bass Pluck B1.wav → `query:Samples#FileId_687`<br>Bass Sub C#0.wav → `query:Samples#FileId_529` |
| E-Piano (17) | E-Piano 2-5-1 AMaj.wav → `query:Samples#FileId_614`<br>E-Piano Chord Pan.wav → `query:Samples#FileId_618`<br>E-Piano GbMaj-C7b5-Fmin.wav → `query:Samples#FileId_620`<br>E-Piano LDre BbMaj7.wav → `query:Samples#FileId_623`<br>E-Piano Motion CMaj9.wav → `query:Samples#FileId_626` |
| Organ (6) | Organ Laid Back C 105 bpm.aif → `query:Samples#FileId_3787`<br>Organ Pad LDre Amin7.wav → `query:Samples#FileId_633`<br>Organ Pad LDre Dmin7.wav → `query:Samples#FileId_634`<br>Organ Pad LDre Emin7.wav → `query:Samples#FileId_635`<br>Organ Pad LDre FMaj7.wav → `query:Samples#FileId_636` |
| Synth (72) | Synth 04 Cmin.wav → `query:Samples#FileId_3778`<br>Synth Bass Pulse Quick Pluck.aif → `query:Samples#FileId_547`<br>Synth Chord Pad Cosmic Fmin.wav → `query:Samples#FileId_561`<br>Synth Note Hi Pulse.aif → `query:Samples#FileId_574`<br>Synth Note Simple Analogue F.wav → `query:Samples#FileId_588` |
| Stab (56) | Stab Apprentice Dmin.wav → `query:Samples#FileId_443`<br>Stab Guitar Sunrise Gmin.wav → `query:Samples#FileId_454`<br>Stab Orchester Energy.wav → `query:Samples#FileId_465`<br>Stab Strings Phased 2.wav → `query:Samples#FileId_476`<br>Stab Synth Zambia A.wav → `query:Samples#FileId_487` |
| ARP (19) | ARP 5th - C0.aif → `query:Samples#FileId_3452`<br>ARP 5th - C3.aif → `query:Samples#FileId_3455`<br>ARP 5th - C6.aif → `query:Samples#FileId_3458`<br>ARP Poly Lead - C3.aif → `query:Samples#FileId_3441`<br>ARP Poly Lead - C6.aif → `query:Samples#FileId_3444` |
| 808 (23) | 808 Heavy E.wav → `query:Samples#FileId_504`<br>808 Oracle 3.wav → `query:Samples#FileId_517`<br>808 Oracle 7.wav → `query:Samples#FileId_521`<br>808 Oracle 11.wav → `query:Samples#FileId_508`<br>808 Oracle 15.wav → `query:Samples#FileId_512` |
| Break (12) | Break 3 Round 95 bpm.aif → `query:Samples#FileId_3922`<br>Break Ahmir's Voodoo 119 bpm.wav → `query:Samples#FileId_3924`<br>Break Claves 92 bpm.aif → `query:Samples#FileId_3926`<br>Break Funky 102 bpm.aif → `query:Samples#FileId_3928`<br>Break Ghosts 90 bpm.wav → `query:Samples#FileId_3930` |
| E-Perc (108) | E-Perc 7.aif → `query:Samples#FileId_2693`<br>E-Perc Blop Grounded 2.wav → `query:Samples#FileId_2713`<br>E-Perc ENIAC Error.wav → `query:Samples#FileId_2734`<br>E-Perc Reson.aif → `query:Samples#FileId_2756`<br>E-Perc Strike Shadowed.wav → `query:Samples#FileId_2776` |
| FX (84) | FX Alien Perc.aif → `query:Samples#FileId_2607`<br>FX Clap Combo.wav → `query:Samples#FileId_2623`<br>FX Ice Cubes.aif → `query:Samples#FileId_2639`<br>FX Ring Blipp.wav → `query:Samples#FileId_2656`<br>FX Synth Lofi Chop.wav → `query:Samples#FileId_2671` |
| Atmos (10) | Atmos Calm 130 bpm.wav → `query:Samples#FileId_3753`<br>Atmos Dark Bells.aif → `query:Samples#FileId_3755`<br>Atmos First One.aif → `query:Samples#FileId_3757`<br>Atmos Hi Ho.aif → `query:Samples#FileId_3759`<br>Atmos Third One.aif → `query:Samples#FileId_3761` |
| Mallet (17) | Mallet Guitar Bb0.wav → `query:Samples#FileId_3470`<br>Mallet Guitar Bb3.wav → `query:Samples#FileId_3473`<br>Mallet Guitar C2.wav → `query:Samples#FileId_3476`<br>Mallet Guitar E0.wav → `query:Samples#FileId_3479`<br>Mallet Guitar E3.wav → `query:Samples#FileId_3482` |
| Tabla (9) | Tabla 130 bpm.aif → `query:Samples#FileId_3911`<br>Tabla and Dolak 85 bpm.aif → `query:Samples#FileId_3912`<br>Tabla SP 1.wav → `query:Samples#FileId_1836`<br>Tabla SP 2.wav → `query:Samples#FileId_1837`<br>Tabla SP 3.wav → `query:Samples#FileId_1838` |
| Ikembe (8) | Ikembe A1.aif → `query:Samples#FileId_3488`<br>Ikembe A2.aif → `query:Samples#FileId_3489`<br>Ikembe B2.aif → `query:Samples#FileId_3490`<br>Ikembe C2.aif → `query:Samples#FileId_3491`<br>Ikembe C3.aif → `query:Samples#FileId_3492` |
| Sandblaster (24) | Sandblaster - C0 - 1.aif → `query:Samples#FileId_3213`<br>Sandblaster - C2 - 1.aif → `query:Samples#FileId_3217`<br>Sandblaster - C4 - 1.aif → `query:Samples#FileId_3221`<br>Sandblaster - F#0 - 1.aif → `query:Samples#FileId_3225`<br>Sandblaster - F#2 - 1.aif → `query:Samples#FileId_3229` |
| Galactica (20) | Galactica - C1 - 1.aif → `query:Samples#FileId_3374`<br>Galactica - C3 - 1.aif → `query:Samples#FileId_3378`<br>Galactica - C5 - 1.aif → `query:Samples#FileId_3382`<br>Galactica - F#2 - 1.aif → `query:Samples#FileId_3386`<br>Galactica - F#4 - 1.aif → `query:Samples#FileId_3390` |
| Smooth (22) | Smooth Synth - C0 - 1.aif → `query:Samples#FileId_3156`<br>Smooth Synth - C2 - 1.aif → `query:Samples#FileId_3160`<br>Smooth Synth - C4 - 1.aif → `query:Samples#FileId_3164`<br>Smooth Synth - F#0 - 1.aif → `query:Samples#FileId_3168`<br>Smooth Synth - F#2 - 1.aif → `query:Samples#FileId_3172` |
| Ob (21) | Ob Kn PW 1.aif → `query:Samples#FileId_3293`<br>Ob Kn PW 5.aif → `query:Samples#FileId_3297`<br>Ob Saw 4.aif → `query:Samples#FileId_3286`<br>Ob SawSq 3.aif → `query:Samples#FileId_3279`<br>Ob Sq B 1.aif → `query:Samples#FileId_3271` |
| Machine (14) | Machine Noise Ambient.wav → `query:Samples#FileId_3820`<br>Machine Punk - C1.aif → `query:Samples#FileId_3321`<br>Machine Punk - C3.aif → `query:Samples#FileId_3323`<br>Machine Punk - C5.aif → `query:Samples#FileId_3325`<br>Machine Punk - F#0.aif → `query:Samples#FileId_3327` |
| Impact (14) | Impact Current.wav → `query:Samples#FileId_704`<br>Impact Dub Chamber.aif → `query:Samples#FileId_706`<br>Impact GE.wav → `query:Samples#FileId_708`<br>Impact Layered Reversed.wav → `query:Samples#FileId_710`<br>Impact Mov Digi.wav → `query:Samples#FileId_712` |
| Riser (7) | Riser Klic.aif → `query:Samples#FileId_718`<br>Riser Noise Gated.wav → `query:Samples#FileId_719`<br>Riser Sine.wav → `query:Samples#FileId_720`<br>Riser Synth.wav → `query:Samples#FileId_721`<br>Riser Taka Breath.wav → `query:Samples#FileId_722` |
| bpm-tagged loops (171) | 80s Beat 90 bpm.wav → `query:Samples#FileId_3919`<br>Break Funky 102 bpm.aif → `query:Samples#FileId_3928`<br>Dirty Neptune 96 bpm.aif → `query:Samples#FileId_3940`<br>Funk 111 bpm.aif → `query:Samples#FileId_3953`<br>Hihat Monarch 92 bpm.wav → `query:Samples#FileId_3866`<br>Lava Beat 130 bpm.wav → `query:Samples#FileId_3969`<br>Reggae 88 bpm.aif → `query:Samples#FileId_3973`<br>Straight EDM Beat 128 bpm.wav → `query:Samples#FileId_3980` |

Loop keys tagged in names: {'F': 4, 'Fmin': 2, 'E': 2, 'Dm': 2, 'C': 2, 'Bmin': 1, 'D#': 1, 'G#': 1, 'G': 1, 'B': 1, 'Abmin': 1, 'Fm': 1}
Loop tempos: [(70, 4), (72, 1), (73, 1), (75, 2), (77, 1), (78, 1), (80, 4), (82, 2), (84, 2), (85, 3), (86, 1), (87, 2), (88, 2), (90, 7), (92, 3), (95, 2), (96, 2), (98, 1), (100, 14), (101, 2), (102, 3), (105, 2), (106, 1), (109, 1), (110, 5), (111, 1), (112, 2), (115, 4), (117, 1), (118, 2), (119, 1), (120, 12), (121, 2), (122, 3), (123, 3), (125, 5), (126, 1), (127, 3), (128, 12), (129, 1), (130, 18), (134, 2), (135, 4), (138, 1), (140, 8), (141, 1), (142, 1), (145, 1), (150, 1), (155, 1), (160, 2), (170, 3), (172, 2), (174, 2), (184, 2)]

## Could not enumerate
- Nothing was permanently unreachable. Notes on partial/derived coverage:
  - `get_browser_items_at_path("Audio Effects")` (display name) errors; the underscore form worked on the single retry. Same applies to MIDI Effects / Max for Live / User Library.
  - The Kick, Snare, Hihat, Tom, Misc Percussion and Samples listings exceeded the tool's output cap; each was saved to disk by the harness and parsed completely with a script (counts and families above are from 100% of each listing).
  - Drift, Instrument Rack and Simpler preset subfolders (13–14 category folders each) were listed but not drilled — their contents are the same .adv/.adg presets already tabulated under Sounds.
  - Core Library was drilled one level (7 subfolders) as specified, not deeper. User Library "Defaults" subfolders (Audio to MIDI, Creating Tracks, Dropping Samples) hold only Live's stock defaults and were not drilled.
  - One transient permission-classifier failure occurred on search_browser("choir"); the retry succeeded. No Live-bridge timeouts occurred during the whole run.
  - Clips and Current_project categories exist at the top level and were intentionally skipped.
