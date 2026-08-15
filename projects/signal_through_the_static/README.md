# Signal Through the Static

A roughly three-minute original pop-rock song project built for the current V2 Music Agent architecture.

## Musical brief

- Tempo: 124 BPM
- Meter: 4/4
- Tonal center: D major / B minor
- Length: 92 bars, about 178.1 seconds before the render tail
- Primary melody: clean electric guitar, no vocal renderer
- Complexity: rich, with section-level role changes rather than one repeated full-band loop

## Form

| Section | Bars | Main arrangement idea |
| --- | ---: | --- |
| Intro | 4 | acoustic sixteenth-flow bed + distorted electric-guitar hook |
| Verse 1 | 12 | clean melody guitar + acoustic bed + muted electric pulse + bass + restrained drums |
| Pre 1 | 6 | clean melody rises while muted guitar tightens and organ enters |
| Chorus 1 | 12 | open overdrive bed supports the clean-guitar topline |
| Verse 2 | 12 | returns to the drier verse frame with a slightly stronger low end |
| Pre 2 | 6 | second build, denser than Pre 1 |
| Chorus 2 | 12 | stronger open section with a lifted clean-guitar melody |
| Bridge | 8 | acoustic drops out; distorted lead owns the first half, then hands off to clean melody guitar |
| Final chorus | 16 | longest and densest section; clean guitar carries the full hook without a competing lead-answer layer |
| Outro | 4 | drums/bass drop; acoustic and distorted lead tail resolve to D |

## Instrumentation and roles

The lineup is organized by musical function rather than genre stereotypes.

- `acoustic_guitar`: steel-string rhythmic bed and primary-melody support, using selective sixteenth-note flow.
- `muted_guitar`: palm-muted electric-guitar drive for verses, pre-choruses and bridge texture.
- `rhythm_guitar`: open overdriven power-chord bed only in choruses.
- `melody_guitar`: clean electric guitar, GM program 27, now carries the former vocal topline as the primary melody.
- `lead_guitar`: distorted guitar used only for the intro hook, first half of the bridge and outro tail so it does not fight the main melody.
- `bass`: finger-bass foundation with connective motion.
- `drums`: restrained verse groove, denser chorus groove and transition fills.
- `organ`: thin voice-led sustained support in builds and open sections.

The old lyric-syllable attacks are not copied mechanically. Adjacent repeated pitches are merged into longer held guitar notes, giving the replacement line more instrumental phrasing and fewer unnecessary re-attacks.

## V2 Materials used as behavior guidance

- `warm-pop-sixteenth-strum`
- `muted-pop-rock-pulse`
- `continuous-overdrive-rhythm-bed`
- `section-linked-pop-rock-bass`
- `role-separated-midi-guitar-mix`

Lead-guitar writing follows the active phrase-design guidance: phrase contour and held targets first, effects second. The General MIDI profile is used conservatively without invented keyswitches.

## Harmony

```text
Intro      Bm | G | D | A
Verse      Bm | G | D | A | Bm | G | D | A | Em | G | D/A | A
Pre        G | A | Bm | Bm | G | A
Chorus     D | A | Bm | G | D | A | G | G | Bm | A | G | A
Bridge     Em | Bm | G | D | Em | Bm | G | A
Final      D | A | Bm | G | D | A | Bm | G | Bm | A | G | D | G | A | D | D
Outro      Bm | G | A | D
```

## Authoritative source

`build.py` is the project-local authoritative song specification. It writes:

- `composition.json`
- `instruments.json`
- `render.json`

There is intentionally no `vocals.json` in this version. If an old generated `vocals.json` exists locally, the builder removes it.

## Build and render

From the repository root:

```powershell
.\.venv\Scripts\python.exe projects\signal_through_the_static\build.py
```

This writes the structured project files, renders the song through the normal instrumental pipeline, then runs the instrument, complexity and continuity critics.

If FluidSynth or the default SoundFont is missing:

```powershell
.\.venv\Scripts\python.exe scripts\setup_assets.py
```

To write the structured JSON without rendering:

```powershell
.\.venv\Scripts\python.exe projects\signal_through_the_static\build.py --write-only
```

Expected derived files include `output/full_song.mid`, `output/mix.wav`, track MIDI/stems and critic reports.

## Validation status

This revision is written against the current branch's supported semantic phrase types and General MIDI route. It has not been listening-validated in the environment that authored the commit, so local rendering and listening feedback remain the musical authority.
