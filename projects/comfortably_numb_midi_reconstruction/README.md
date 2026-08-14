# Comfortably Numb MIDI Reconstruction Test

This project does not use the long-form composer. It tests whether the **existing explicit-event schema and MIDI exporter** can reproduce the user-supplied MIDI without changing the engine.

## What is preserved

- 480 PPQ timing
- exact note onsets and durations
- note pitches
- note velocities
- original two-track split
- original MIDI programs and channels
- exact tempo: 923076 microseconds per beat

The source contains no pitch-wheel, control-change, aftertouch or articulation events, so there is no expressive MIDI data for the project to lose. Sound may still differ between MIDI players because each player or SoundFont renders GM programs differently.

## Build the declarative project

```powershell
git pull --ff-only origin main
.\.venv\Scripts\python.exe projects\comfortably_numb_midi_reconstruction\build_project.py
```

## Render

```powershell
.\.venv\Scripts\python.exe scripts\render_song.py comfortably_numb_midi_reconstruction
```

Listen to:

```text
projects\comfortably_numb_midi_reconstruction\output\mix.wav
```

## Verify exact MIDI event reconstruction

After rendering:

```powershell
.\.venv\Scripts\python.exe projects\comfortably_numb_midi_reconstruction\verify_reconstruction.py
```

A successful result reports 82 lead notes and 746 rhythm-guitar notes with matching fingerprints.
