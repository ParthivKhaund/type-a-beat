# abl: Beats Without Music Theory

## What abl is

abl turns a short typed line into music playing in Ableton Live. You type `beat trap 140` in Terminal and about a second later a trap drum pattern is looping in Live at 140 beats per minute. You never open Live's browser, pick an instrument, or draw notes. abl does that for you through a script that lives inside Live.

It knows seven beat styles, a handful of bass and keyboard sounds, and how to turn chord names into notes. That is fixed knowledge, not AI, which is why it answers in about a second and does the same thing every time. Claude Code with the Ableton skills is still the tool for anything creative or open-ended. abl covers the things you say over and over: put a beat on, add bass, add chords, change the speed, play, stop, louder, undo.

## Before you start

Three things, once per session.

1. **Open Ableton Live** and wait for the bottom status bar to say "AbletonMCP: Listening for commands on port 9877". That is the script abl talks to.
2. **Start a fresh set** with File, then New Live Set. Live Lite allows 8 tracks per set. A new set starts with 4, and abl needs one each for Drums, Bass, Keys, and Lead, so a fresh set always has room.
3. **Open Terminal** (Cmd-Space, type Terminal, Enter), then type `abl` and press Enter. You get an `abl>` prompt. Type `quit` to leave it.

You can also run a single line from any Terminal without the prompt: `abl "beat trap 140"`. If you would rather talk than type, macOS dictation works at the `abl>` prompt: press the dictation key, say "beat trap one forty", then press Enter.

## Three ways to run it

They all do the same thing; pick whichever is closest to hand.

| Way | How | Speed |
| --- | --- | --- |
| Terminal | `abl "beat trap 140"` for one line, or `abl` alone for the `abl>` prompt | About a second |
| Inside Claude Code | Type `/abl beat trap 140` in any Claude Code session. Claude runs it and shows the result. Plain words work here too: `/abl something chill with piano` | A few seconds |
| Voice | At the `abl>` prompt type `v` and speak, for example "beat trap one forty". It stops listening a second after you go quiet, shows what it heard, and runs it. Speech is recognized on your Mac, nothing is uploaded | About two seconds after you stop talking |

For a voice hotkey that works from anywhere, even with Live in front, open `extras/abl voice.shortcut` to add the "abl voice" Shortcut. Then three one-time steps:

1. In Shortcuts, open the Shortcuts menu, then Settings, then Advanced, and turn on Allow Running Scripts. Without it macOS refuses to run the Shortcut.
2. Select "abl voice", click the (i) button, choose Add Keyboard Shortcut, and press the keys you want, for example Control-Option-Space.
3. Press them once and say a command. The first time, macOS asks to allow the microphone; click Allow.

After that: press the keys, speak, done. Every result appears as a notification, so you never have to look at Terminal.

## Your first beat in 60 seconds

Type these one at a time at the `abl>` prompt and listen after each.

| Type this | What happens |
| --- | --- |
| `beat trap 140` | A Drums track appears with an 808 kit, and a 2-bar trap pattern starts looping at 140 bpm. |
| `keys rhodes Am-F-C-G` | A Keys track with a warm electric piano plays four chords, one per bar. |
| `bass 808` | A Bass track with a deep 808 sub follows those same four chords. |
| `swing 60` | The drums loosen up a little. |
| `hats double` | Busier hi-hats, the rolling trap sound. |
| `stop` | Everything stops. `go` starts it all again. |
| `undo` | Takes back the last thing abl did. |

Order matters once: put `keys` before `bass`, because the bass copies whatever chords the keys are playing. Without keys, the bass follows the key Live is set to.

Everything abl makes shows up in Live's Session View as a clip named "abl ..." on a track named Drums, Bass, or Keys, so you can see it, hear it, and edit it there like anything else.

## The words, explained without theory

**Styles** set the feel of the drums and the bass pattern that goes with them. Speed is bpm, beats per minute. Give a number with `beat` to set it; leave it out and the speed stays as it is.

| Style | Feels like | Typical bpm |
| --- | --- | --- |
| trap | Slow and heavy, rolling hi-hats, big 808 bass | 130 to 160 |
| boombap (or hiphop) | 90s hip-hop, dusty and swung | 85 to 95 |
| lofi | Chill study beats, soft and lazy | 70 to 90 |
| house | Dance music, kick on every beat | 120 to 128 |
| techno | Harder, darker house | 128 to 140 |
| pop | Clean, straight backbeat | 100 to 120 |
| jazz (or swing) | Ride cymbal, walking bass, loose | 120 to 200 |

**Sounds** go right after `bass` or `keys`. Leave the name out and abl picks one that fits the current style.

| Use after | Name | Sounds like |
| --- | --- | --- |
| bass | 808 or sub | Deep booming trap bass |
| bass | upright | Acoustic jazz bass |
| bass | analog or synth | Fat synth bass |
| bass | reese | Growly and dark |
| bass | 303 | Squelchy acid |
| keys | rhodes | Warm electric piano, chill |
| keys | piano | Grand piano |
| keys | organ | Funky organ |
| keys | pad | Soft washy background |
| keys | epiano | Cleaner electric piano |

**Chords** are a few notes played together, and a progression is a short loop of them that gives a track its mood. You do not need to understand them. Pick a recipe and type it after `keys`.

| Mood | Type this |
| --- | --- |
| Sad, emotional | `Am-F-C-G` |
| Happy, big pop | `C-G-Am-F` |
| Chill, jazzy, lofi | `Cmaj7-Am7-Dm7-G7` |
| Dark trap | `Am-F-Dm-E` |
| Dreamy | `Fmaj7-Em7-Dm7-Cmaj7` |
| Uplifting dance | `Dm-F-C-G` |

How to read them: each chord is one bar, so four chords loop every four bars. The capital letter is the note name. A small `m` after it means minor, which sounds sadder. A `7` makes it jazzier. Add `stab` at the end for short choppy chords (the house piano sound) or `hold` for long sustained ones. abl picks stabs for house and techno and holds for everything else.

## Tweaking what is playing

These act on the tracks abl made. "Role" means drums, bass, keys, or lead. You can also name any track you see in Live, like `mute piano stab`, or use its number from `tracks`.

| Type this | What it does |
| --- | --- |
| `swing 60` | Loosens the drum timing. 50 is robot-straight, 75 is the most. Try 58 to 66. |
| `hats double` / `hats half` / `hats off` / `hats normal` | Busier, sparser, no, or normal hi-hats. |
| `louder drums` / `quieter keys 2` | Nudges that track's fader. The number is how many steps. |
| `mute bass` / `unmute bass` | Silences or restores a track. |
| `solo drums` / `unsolo drums` | Hear only that track, then everything again. |
| `tempo 128` | Changes the speed without touching anything else. |
| `beat house` | Swaps the drum pattern and kit in place. The speed stays. |
| `clear keys` | Deletes abl's keys clip, keeps the track. |
| `undo` / `redo` | Each abl command is one step, so one `undo` takes back the whole command. Cmd-Z in Live works too. |
| `status` / `tracks` / `help` | What is playing, what tracks exist, the full list of commands. |

Chain several with semicolons and they run in order: `beat lofi 85; keys rhodes Cmaj7-Am7-Dm7-G7; bass upright; swing 62`.

If you type a plain sentence instead, like `something chill with piano`, abl asks Claude to turn it into one command, shows you the command it chose, and runs it. That takes about 8 seconds, so use it when you do not know the word, not for every line.

## Starter sessions to copy

Each line is a whole loop. Paste it into Terminal as written, or type the part inside the quotes at the `abl>` prompt. Paste a different one on the same set and it swaps everything in place.

| Mood | Paste this |
| --- | --- |
| Chill study beat | `abl "beat lofi 82; keys rhodes Cmaj7-Am7-Dm7-G7; bass upright; swing 62"` |
| Trap banger | `abl "beat trap 145; keys piano Am-F-Dm-E; bass 808; hats double"` |
| Dance floor | `abl "beat house 124; keys piano Dm-F-C-G stab; bass analog"` |
| Sad piano | `abl "beat pop 100; keys piano Am-F-C-G; bass electric"` |
| Late-night jazz | `abl "beat jazz 130; keys rhodes Cmaj7-Am7-Dm7-G7; bass upright"` |
| Dark techno | `abl "beat techno 132; keys pad Am-Am-F-G; bass reese"` |

Then change one thing at a time and listen: `abl "swing 66"`, `abl "louder bass"`, `abl "hats half"`, `abl "keys organ Am-F-C-G"`. When you like it, leave it playing and open Live to see the three clips it made.

## Bring in a whole song

`abl "import https://www.youtube.com/watch?v=..."` downloads the song and puts it on its own audio track, named after the song, ready to play, chop, or sample. A file on your Mac works too: `abl "import ~/Music/song.mp3"`. It takes a few seconds. If it ever fails with "403", run `brew upgrade yt-dlp` in Terminal and try again, because YouTube regularly breaks older downloaders.

## Recreate a song you like

Give abl a YouTube link or an audio file and it rebuilds the song's skeleton in Live so you can start editing from something real instead of a blank set.

```
abl "recreate https://www.youtube.com/watch?v=..."
abl "analyze https://www.youtube.com/watch?v=..."
```

`recreate` downloads the audio, splits it into drums, bass, vocals, and everything else, then works out the speed, the key, where the sections are (intro, verse, chorus), the chords in each bar, the drum hits, the bass line, and rough keys and melody parts. It sets Live's tempo and key, makes one scene per section with the section's name, puts a clip for each part in that scene, lays the same clips left to right in Arrangement view with a marker at every section so you can edit on a timeline right away, and drops the original song, muted, on a track called Reference so you can unmute it to compare. `analyze` only prints the report and leaves Live alone. Add `fresh` at the end to redo a song it has already seen.

What to expect:

| Part | How good |
| --- | --- |
| Speed, bar lines, sections with names | Strong (All-In-One, a music-structure model) |
| Drums | Strong (ADTOF, a drum transcription model: kick, snare, hats, toms, cymbals) |
| Bass | Solid starting point |
| Chords per bar | Good for pop, hip-hop, house; shaky for jazz |
| Keys and melody | Transcriptions to clean up. Piano parts use a dedicated piano model and get a piano sound; guitar parts get a guitar sound |
| The actual sounds | Not recreated; you get the notes on Live's stand-in instruments |

The first run of a 3-minute song takes a few minutes, mostly the stem separation, and it prints what it is doing as it goes. Everything is kept in a cache, so running it again is instant. Recreating a song to study or remix at home is fine; publishing a copy of someone's track is a different matter.

**How it picks sounds.** It listens to each part: the drum kit is the library kit whose own kick, snare, and hat samples are closest to the song's hits, and bass, keys, and lead are chosen by an audio model that tags each stem ("an upright bass", "a hammond organ", "a warm pad") and looks that up in your library. It works with whatever is in your library. Free Ableton packs (Beat Tools, Build and Drop, Vibrations, Singularities, Recording Hybrid Kit, Break Selection, Beat Selection, Solid Sounds) and the free Surge XT and Dexed synths give it more to choose from. Whenever you add packs or plugins, run `abl catalog` once so the picker can see them.

## Limits and gotchas

- **8 tracks and 8 scenes** is Live Lite's cap. If abl says "Live could not create a track", delete a track in Live or rename one of yours to Drums, Bass, Keys, or Lead and abl will use it.
- **abl only touches its own clips.** It names them "abl ..." and checks that name before changing anything. Your own clips are never edited or deleted, and `kill` only removes a track abl created.
- **Loading a sound onto an existing Drums, Bass, or Keys track replaces that track's instrument.** abl tells you what it replaced, and `undo` brings it back.
- **Tempo changes only when you type a number.** `beat house` keeps the current speed; `beat house 124` sets it.
- **Keys before bass.** The bass copies whatever chords exist when you type `bass`. Typed the other way round, just run `bass` again.
- **abl makes loops, not songs.** Everything lives in Live's Session View. Turning loops into an intro, verse, and chorus is a job for Claude Code with the Ableton skills, or your own hands in Arrangement View.
- **If everything hangs,** a dialog box is probably open in Live. Press Enter in Live and try again.
- **For anything creative,** like "make it sound more like X", mixing, or arrangement, use Claude Code. abl is the keyboard shortcut; Claude is the producer.
