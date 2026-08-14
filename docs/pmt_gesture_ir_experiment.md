# PMT + Gesture IR experiment

Branch: `agent/pmt-gesture-ir`

This branch tests a replacement for the current flat note-event performance layer
without changing the composition layer on `main`.

## Scope of the first vertical slice

### PMT-Core

`src/performance/pmt.py` implements the paper-derived performance-timed PMT core:

- 10 ms time quantum
- `TRACK_0..15`
- `PROG_0..128`, with `128` reserved for drums
- `PITCH_0..127`
- `DURP_0..199`, representing 10..2000 ms
- `VEL_0..31`
- `TSHIFT_0..99`, representing 10..1000 ms
- true simultaneous onsets emit no `TSHIFT`
- long gaps are tiled with repeated `TSHIFT_99`
- deterministic serialization order is `(onset, track, pitch)`
- `<BAR>` is rejected in performance-timed mode

PMT intentionally stores the realized note performance, not section names, chord
labels, mixer state, pitch-bend curves, or instrument-specific body mechanics.

### Gesture sidecar

`src/performance/gesture_ir.py` stores performance relationships that PMT cannot
represent directly. The initial electric-guitar vocabulary is:

- `pick`
- `hammer_on`
- `pull_off`
- `slide`
- `vibrato`
- `release`

Transitions such as hammer-on, pull-off, and slide must name both endpoints,
provide a transition duration, and explicitly set `retrigger=false`. This prevents
the old failure mode where an articulation label still became a fresh MIDI attack.

## Intended project layout

```text
Song Project
├── composition.json          # form, harmony, motifs, track roles
├── performance.pmt           # realized onset/duration/velocity/instrument stream
├── performance.gestures.json # instrument-specific transition relationships
└── render.json               # sound library, effects, mixer, automation
```

## Migration path

1. Keep the current composition and instrument-phrase layers.
2. Make instrument compilers produce PMT notes plus gesture sidecars.
3. Add renderer adapters:
   - General MIDI fallback
   - pitch-bend/CC MIDI
   - MPE
   - future SFZ/VST/neural backends
4. Compare old note-event output and PMT output with the same composition.
5. Only replace the old path after the A/B tests are useful.

## Current limitations

- PMT duration is paper-compatible and therefore capped at 2000 ms.
- Gesture IR is validated but not yet rendered.
- No existing renderer path is changed in this commit.
- The branch does not claim that General MIDI can reproduce physical guitar
  transitions. It only preserves enough intent for a capable adapter to try.

## Test

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_pmt_gesture_ir -v
```
