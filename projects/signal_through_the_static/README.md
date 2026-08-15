# Signal Through the Static

A roughly three-minute original pop-rock song project built for the current V2 Music Agent architecture.

## Musical brief

- Tempo: 124 BPM
- Meter: 4/4
- Tonal center: D major / B minor
- Length: 92 bars, about 178.1 seconds before the render tail
- Lead vocal: English, optional SoulX-Singer render
- Complexity: rich, with section-level role changes rather than one repeated full-band loop

## Form

| Section | Bars | Main arrangement idea |
| --- | ---: | --- |
| Intro | 4 | acoustic sixteenth-flow bed + electric-guitar hook |
| Verse 1 | 12 | vocal + acoustic bed + muted electric pulse + bass + restrained drums |
| Pre 1 | 6 | muted guitar tightens, organ enters, drums build |
| Chorus 1 | 12 | open overdrive bed replaces muted drive; wider rhythm section; lead answers vocal gaps |
| Verse 2 | 12 | returns to the dry verse frame with a slightly stronger low end |
| Pre 2 | 6 | second build, denser than Pre 1 |
| Chorus 2 | 12 | stronger open section with higher lead answers |
| Bridge | 8 | acoustic drops out; muted electric texture + organ + bass/drums support an 8-bar guitar solo |
| Final chorus | 16 | longest and densest section; vocal hook repeats and lead answers expand |
| Outro | 4 | drums/bass drop; acoustic and lead tail resolve to D |

## Instrumentation and roles

The lineup was chosen by musical function before Material retrieval.

- `acoustic_guitar`: steel-string rhythmic bed and vocal support. Uses a selective sixteenth-note flow with related four-bar variation.
- `muted_guitar`: dry palm-muted electric-guitar drive for verses, pre-choruses and bridge texture.
- `rhythm_guitar`: open overdriven power-chord bed only in choruses, so section lift is a role change rather than just a velocity boost.
- `lead_guitar`: intro hook, sparse chorus answers, bridge solo and outro tail. The part is phrase-led and leaves vocal space.
- `bass`: finger-bass foundation with fifths, approaches and small contour changes instead of root-only reporting.
- `drums`: restrained verse groove, denser chorus groove and transition fills.
- `organ`: thin voice-led sustained support in builds/open sections; absent from verses and outro.
- `vocal`: original English topline rendered optionally with SoulX-Singer.

## V2 Materials used as behavior guidance

The project applies current active Materials by role rather than treating them as finished-song templates:

- `warm-pop-sixteenth-strum`
- `muted-pop-rock-pulse`
- `continuous-overdrive-rhythm-bed`
- `section-linked-pop-rock-bass`
- `role-separated-midi-guitar-mix`

Lead-guitar phrase design follows the active Skill's target/answer/rest logic. The current General MIDI profile is intentionally used conservatively: this project does not invent unsupported keyswitches or spray slide/vibrato controllers onto the lead.

## Harmony

The harmonic language stays accessible enough for pop-rock while avoiding one four-chord loop for the entire song.

```text
Intro      Bm | G | D | A
Verse      Bm | G | D | A | Bm | G | D | A | Em | G | D/A | A
Pre        G | A | Bm | Bm | G | A
Chorus     D | A | Bm | G | D | A | G | G | Bm | A | G | A
Bridge     Em | Bm | G | D | Em | Bm | G | A
Final      D | A | Bm | G | D | A | Bm | G | Bm | A | G | D | G | A | D | D
Outro      Bm | G | A | D
```

## Lyrics

### Verse 1

City lights are bleeding through the rain  
Your name keeps ringing in the wires  
I was running circles from the same old fear  
Now the night is opening like fire

### Pre-chorus

Hold on, do not let the moment fall  
We are closer than we think  
Hear the room begin to sing

### Chorus

Send me a signal through the static  
I can hear you under all the noise  
If the whole world turns automatic  
I will follow that imperfect voice  
Stay until the morning finds us  
Maybe we are not too late

### Verse 2

I kept every answer in a locked room  
Made a habit out of missing trains  
Then the window shakes and starts to move  
And I want to try this road again

### Pre-chorus 2

Hold on, the distance is getting small  
We are closer than we think  
Hear the room begin to sing

### Bridge

Maybe I do not need a map tonight  
One small sound can pull me back to life

### Final chorus

Repeat the chorus hook, then close on:

Send me a signal through the static  
Maybe we are not too late

## Authoritative source

`build.py` is the project-local authoritative song specification. It writes the V2 execution inputs:

- `composition.json`
- `instruments.json`
- `render.json`
- `vocals.json`

Those JSON files are deterministic derived project artifacts. MIDI, stems, validation reports and WAV mixes are derived execution outputs.

## Build and render

From the repository root:

```powershell
.\.venv\Scripts\python.exe projects\signal_through_the_static\build.py
```

This writes the project JSON, renders the instrumental song through the current generic renderer, then runs the instrument, complexity and continuity critics.

To render the English vocal version too:

```powershell
.\.venv\Scripts\python.exe projects\signal_through_the_static\build.py --with-vocals
```

If the optional vocal environment has not been installed yet, set it up first with the repository's vocal setup script:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup_vocals.ps1
```

If FluidSynth or the default SoundFont is missing, use the repository asset setup:

```powershell
.\.venv\Scripts\python.exe scripts\setup_assets.py
```

To inspect/write the structured JSON without rendering:

```powershell
.\.venv\Scripts\python.exe projects\signal_through_the_static\build.py --write-only
```

Expected derived files after a full render include `output/full_song.mid`, `output/mix.wav`, track MIDI/stems, critic reports, and, with `--with-vocals`, `output/vocal_mix.wav`.

## Validation status

The project has been written against the current branch's declared composition schema, supported semantic phrase types and General MIDI profile. It has **not** been locally rendered or listening-validated in the environment that authored this commit, so do not treat this README as a test-pass claim. Run the command above after pulling and use the generated critic reports plus listening feedback for the next revision.
