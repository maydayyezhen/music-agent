# 下一站还亮着 (Next Stop Still Lit)

Original structured pop-rock project created for the `skills-v2-clean-slate` workflow.

## Composition target

- Tempo: 116 BPM
- Meter: 4/4
- Tonal center: D major with B minor color
- Form: 88 bars
- Score duration: about 182 seconds, roughly 3:02 before render tail
- Complexity: rich overall, with denser later choruses and a wave-shaped arrangement contour
- Vocal surrogate: Harmonica

## Instrumentation and roles

This project deliberately separates genre, instrument choice, section role, and energy.

- `vocal_lead`: Harmonica as the foreground vocal-surrogate melody. It uses longer singable phrases, recurring hook shapes, rests, and a bridge handoff instead of nonstop note-filling.
- `acoustic_guitar`: Steel-string acoustic guitar as a flowing rhythmic bed. It uses a sixteenth-note hand-motion concept with broad anchors, narrower connective strokes, and deliberate holes.
- `muted_guitar`: Short compact electric-guitar pulses for verse and pre-chorus propulsion. It is not a quieter copy of the chorus guitar.
- `rhythm_guitar`: Overdriven electric-guitar bed for open chorus sections, with stable re-articulation and near-continuous occupancy.
- `lead_guitar`: Sparse sustained answers plus a bridge foreground passage, leaving the main melody room elsewhere.
- `bass`: Section-linked finger bass. Restrained sections use fewer attacks and longer middle support; open sections use fuller pulses plus small contour and approach-note identity.
- `organ`: Low-level sustained harmonic color for pre-choruses, choruses, and bridge only.
- `drums`: Dynamic pop-rock kit with verse groove, pre-chorus build, chorus lift, half-time bridge contrast, fills, and final-chorus expansion.

## V2 material vocabulary applied

The arrangement realizes the active reusable behavior from:

- `warm-pop-sixteenth-strum`
- `section-linked-pop-rock-bass`
- `muted-pop-rock-pulse`
- `continuous-overdrive-rhythm-bed`
- `sustained-overdrive-guitar`
- `role-separated-midi-guitar-mix`

The song-specific harmony, melody, form, section lengths, entry/exit plan, and mix settings are original to this project rather than copied from another song project.

## Build and render

From the repository root:

```powershell
python projects/next_stop_still_lit_pop_rock/build_song.py
python scripts/render_project.py next_stop_still_lit_pop_rock
```

Or build and render in one command:

```powershell
python projects/next_stop_still_lit_pop_rock/build_song.py --render
```

The builder writes the authoritative project artifacts:

- `composition.json`
- `instruments.json`
- `render.json`
- `manifest.json`

The renderer then derives:

- per-track MIDI under `tracks/`
- `output/full_song.mid`
- WAV stems under `stems/`
- `output/mix.wav`

The render route intentionally goes through `scripts/render_project.py`, so the generated manifest remains the thin project facade rather than bypassing it.
