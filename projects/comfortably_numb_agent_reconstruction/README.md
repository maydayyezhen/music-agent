# Comfortably Numb agent-performance reconstruction

This project tests the music agent rather than the explicit-event MIDI container.

## What is preserved from the reference MIDI

- Lead pitch sequence
- Lead onsets and notated durations
- Overall 12-bar timing and tempo
- Harmony inferred from the source rhythm track

## What the agent must reconstruct

- Lead velocity and accent hierarchy
- Guitar string/fret assignment
- Pick, hammer-on, pull-off, slide, legato, sustain and vibrato intent
- Performance-profile fallback behavior
- Every rhythm-guitar note
- Rhythm voicings, strum direction, hand motion, four-bar variation and foreground thinning

Neither track contains an explicit `events` list. Both use `instrument_phrase` and pass through the current instrument/performance pipeline.

The source MIDI contains no pitch-bend, CC, aftertouch or articulation metadata. The builder therefore infers performance intent from intervals, timing, note length and phrase gaps. This is an interpretation test, not an exact MIDI hash test.

## Build

```powershell
.\.venv\Scripts\python.exe projects\comfortably_numb_agent_reconstruction\build_agent_project.py
```

## Inspect the semantic compilation

```powershell
.\.venv\Scripts\python.exe projects\comfortably_numb_agent_reconstruction\inspect_agent_reconstruction.py
```

## Render

```powershell
.\.venv\Scripts\python.exe scripts\render_song.py comfortably_numb_agent_reconstruction
```

Listen to:

```text
projects\comfortably_numb_agent_reconstruction\output\mix.wav
```

The useful comparison is:

1. Does the lead still communicate the same phrase structure?
2. Do long notes, repeated notes and connected runs behave like guitar gestures?
3. Does the regenerated accompaniment support the lead without copying the 746 source events?
4. Which differences are caused by the current composition/performance logic, and which are caused by the SoundFont?
