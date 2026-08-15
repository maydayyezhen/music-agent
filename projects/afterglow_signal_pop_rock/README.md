# Afterglow Signal

A roughly three-minute pop-rock song project for the V2 clean-slate branch.

## Musical plan

- 120 BPM, 4/4, 90 bars, about 180 seconds before render tail
- tonal center: B minor / D major
- form: Intro 6 -> Verse 1 12 -> Pre 1 6 -> Chorus 1 12 -> Verse 2 12 -> Pre 2 6 -> Chorus 2 12 -> Bridge 8 -> Final Chorus 12 -> Outro 4
- the vocal role is represented by a flute lead, written as phrase-based melody with rests, long tones, repeated chorus hook, second-verse variation and final-chorus lift
- verses use compact muted-guitar eighth pulses and sparser section-linked bass
- choruses switch to double-tracked continuous overdrive rhythm beds, fuller bass pulse, stronger drums and subtle organ support
- bridge drops the overdrive wall, opens the rhythmic space, uses a half-time drum feel and guitar response phrases before the last chorus
- nine rendered tracks: lead flute, muted guitar, two overdrive guitars, clean guitar, lead guitar, bass, drums and organ

## Build and render

From the repository root:

```powershell
.\.venv\Scripts\python.exe projects\afterglow_signal_pop_rock\build_song.py
```

If the repository environment is already activated, this is enough:

```powershell
python projects\afterglow_signal_pop_rock\build_song.py
```

The build writes the authoritative project JSON files and invokes the normal repository renderer. Main outputs:

```text
projects/afterglow_signal_pop_rock/output/full_song.mid
projects/afterglow_signal_pop_rock/output/mix.wav
projects/afterglow_signal_pop_rock/output/final.wav
```

`final.wav` is just a convenient listening copy of the generated mix.
