# Long-form tonality

The original experimental long-form planner interpreted every `key_root` as natural minor.
That remains the compatibility fallback, but new work should declare tonal intent explicitly.

```json
{
  "tonality": {
    "tonic": "D",
    "mode": "major",
    "additional_intervals": [10]
  }
}
```

Intervals are semitone distances from the tonic. In D major, interval `10` adds C natural as an
explicit borrowed bVII color while retaining C# from the major scale.

Supported named modes:

- `major` / `ionian`
- `natural_minor` / `minor` / `aeolian`
- `dorian`
- `mixolydian`
- `major_pentatonic`
- `minor_pentatonic`
- `minor_blues`

A custom palette may replace the mode:

```json
{
  "tonality": {
    "tonic": "D",
    "scale_intervals": [0, 2, 4, 5, 7, 9, 10]
  }
}
```

Optional `additional_intervals` and `excluded_intervals` are applied after the base mode.
The resolved palette is exported in `long-form-plans.json` so generated notes can be audited.

## Expression preservation

The long-form path now preserves authored slide and vibrato data:

```json
{
  "action": "slide",
  "slide_from_semitones": -2.0
}
```

```json
{
  "action": "vibrato",
  "vibrato": {"delay": 0.32, "depth": 0.28, "rate": 5.0}
}
```

These actions require `realization.enable_articulations: true`. Explicit bends require
`realization.enable_pitch_bend: true`.

The demo `projects/connected_lead_reference_demo` shows an original lead built from repeated-note
propulsion, triplet-like bursts, cross-bar continuation and a delayed register peak. It uses
structural statistics from a reference MIDI without copying its notes.
