# Neon After Rain — Generic Melody Validation

This project is a listening/structure test for the active `melody-structure-development` Skill.

It deliberately avoids lead-guitar articulation so the result tests the **generic melody layer** rather than a guitar-specific realization path.

## Brief

- style context: night-city game BGM / restrained synth-pop
- mood: cool, reflective, quietly hopeful
- tempo: 92 BPM
- meter: 4/4
- key center: E minor
- length: 20 bars, about 52 seconds
- foreground: GM Marimba, channel 1 / zero-based channel 0, program 12
- harmonic bed: GM Electric Piano 1, channel 2 / zero-based channel 1, program 4

The palette is intentionally small: one foreground melody and one sustained harmonic bed. No guitar articulation, drum groove, bass Material or renderer-specific expression is used to rescue the melody.

## What this tests

The composition is built around one motif family rather than unrelated per-bar fragments:

```text
A        bars 1-4   establish identity
A'       bars 5-8   preserve identity, vary rhythm / ending
B        bars 9-12  sequence + register expansion + release
A''      bars 13-16 recognizable return with more ornament
Coda     bars 17-20 augmentation + resolution
```

The declared melody distinguishes:

```text
structural tones
surface / embellishing tones
```

Surface motion uses passing, neighboring and connector roles around explicit bar-level structural targets.

The climax is intentionally in bar 11, roughly the middle of the active span. This project therefore does **not** validate the old shortcut `highest note must arrive late`.

## Evidence boundary

The design combines two kinds of reusable evidence already established by the project research:

1. Goetschius source study: structural vs embellishing tones, germ-first reasoning, recurrence, modified recurrence and hierarchical development.
2. Cross-source real-MIDI study: identity before novelty, selective variation, predominantly local connective motion, and the negative result that density / apex timing / repeated-pitch percentages are not universal melody-quality rules.

No source melody, source chord progression or full source rhythmic sequence is copied into this project.

## Build

From the repository root:

```powershell
python projects/neon_after_rain_melody_validation/build.py
```

Outputs:

```text
projects/neon_after_rain_melody_validation/output/neon_after_rain.mid
projects/neon_after_rain_melody_validation/output/melody_events.json
projects/neon_after_rain_melody_validation/reports/validation.json
```

The validator checks declared hierarchy and internal consistency only. A passing report does **not** mean the melody sounds good; listening feedback remains authoritative.

## Suggested local render

Using the repository's usual GeneralUser-GS / FluidSynth path:

```powershell
.\tools\fluidsynth\bin\fluidsynth.exe -ni -F "projects\neon_after_rain_melody_validation\output\neon_after_rain.wav" -T wav -r 44100 -g 0.8 ".\assets\soundfonts\GeneralUser-GS.sf2" "projects\neon_after_rain_melody_validation\output\neon_after_rain.mid"
```
