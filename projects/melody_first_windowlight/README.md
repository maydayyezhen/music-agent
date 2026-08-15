# Windowlight Relay

A melody-first composition experiment for Music Agent V2.

## Intent

The arrangement is deliberately subordinate to the foreground line. The listening test is whether the melody remains memorable, connected and singable after one or two passes, rather than whether the backing sounds impressive on its own.

- Tempo: 108 BPM
- Meter: 4/4
- Tonal center: D major with B-minor shading
- Length: 52 bars, about 1:56
- Form: intro -> theme_a -> theme_a2 -> lift -> interlude -> hook -> hook_ext -> outro

## Roles

- `main_melody`: flute as a neutral singing lead
- `acoustic_guitar`: restrained steel-string harmonic/rhythmic bed
- `finger_bass`: connected low foundation with small approaches
- `electric_piano`: sparse sustained harmonic color
- `strings_pad`: enters only for lift and hook weight
- `drums`: light pulse and section definition

## Melody design

The opening germ is intentionally small: `F# -> A -> B -> A`.

Later sections preserve recognizable contour/rhythm fragments while changing destinations, register and phrase endings. The line gradually expands toward the upper register, leaves a short interlude breathing space, then states the strongest hook before a final extension and D-centered close.

The arrangement avoids a competing counter-melody so the lead can be judged directly.

## Build

From the repository root:

```powershell
python projects/melody_first_windowlight/build.py
```

Expected full MIDI:

```text
projects/melody_first_windowlight/output/full_song.mid
```

## Render with the repository SoundFont

```powershell
.\tools\fluidsynth\bin\fluidsynth.exe -ni -F "projects\melody_first_windowlight\output\full_song.wav" -T wav -r 44100 -g 0.8 ".\assets\soundfonts\GeneralUser-GS.sf2" "projects\melody_first_windowlight\output\full_song.mid"
```

For the first listening pass, judge the melody before changing timbre or adding more arrangement layers.
