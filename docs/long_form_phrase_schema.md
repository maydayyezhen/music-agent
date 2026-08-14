# Long-Form Phrase Schemas

Long-form lead phrases remain inside `instrument_phrase`, but experimental use must explicitly
set `phrase_generation_mode` to `long_form_experimental`. Formal songs either omit the field or
set it to `legacy_stable`. The old names `long_form` and `legacy_short_phrase` remain migration
aliases only.

## Section arc

```json
{
  "section_arc": {
    "section_id": "lead_chorus_1",
    "bars": [1, 16],
    "opening_register": "mid",
    "peak_register": "high",
    "peak_bar": 12,
    "final_resolution_bar": 16,
    "energy_curve": [0.42, 0.48, 0.54, 0.60, 0.64, 0.70, 0.78, 0.84, 0.90, 0.96, 1.0, 0.94, 0.86, 0.76, 0.64, 0.52],
    "density_curve": [0.42, 0.48, 0.50, 0.46, 0.54, 0.58, 0.62, 0.58, 0.66, 0.72, 0.80, 0.74, 0.64, 0.56, 0.48, 0.34],
    "cadence_plan": {
      "strong_cadences": [16],
      "weak_cadences": [8],
      "avoid_resolution_bars": [4, 12]
    },
    "breath_bars": [4, 8, 13],
    "cross_bar_note_bars": [2, 6, 10, 14],
    "delayed_target": {"pitch": "E6", "bar": 12}
  }
}
```

The curves must contain one value per section bar. `peak_bar` and the delayed target must
not precede the midpoint when delayed peak/resolution rules are enabled.

## Phrase relationship graph

```json
{
  "phrase_relationships": [
    {
      "phrase_id": "A1",
      "bars": [1, 4],
      "relationship": "introduce",
      "continuation_from": null,
      "continuation_to": "A2",
      "resolution": "deferred",
      "motif_operations": []
    },
    {
      "phrase_id": "A2",
      "bars": [5, 8],
      "relationship": "variation",
      "continuation_from": "A1",
      "continuation_to": "A3",
      "resolution": "deferred",
      "motif_operations": ["transpose_up", "change_ending"]
    }
  ]
}
```

Relationships may be `introduce`, `repeat`, `variation`, `sequence`, `extension`,
`fragmentation`, `augmentation`, `compression`, `continuation`, `answer`, `climax`, or
`resolution`. Bar ranges must cover the arc in order. A phrase marked deferred must link
forward and preserve unresolved state.

## Melodic state

The state is generated, not hand-authored as final notes:

```json
{
  "melodic_state": {
    "active_motif": "motif_A",
    "motif_version": 2,
    "current_register": "mid_high",
    "direction": "ascending",
    "tension": 0.68,
    "resolved": false,
    "continuation_required": true,
    "target_pitch": 76,
    "target_bar": 12,
    "last_interval": 2,
    "last_note_function": "non_chord_tone",
    "phrase_breath_remaining": 0.75,
    "cadence_strength": 0.2
  }
}
```

The compiler writes a state snapshot at the start and end of every relationship node.
`rest_type: breath` never resets this object. `rest_type: structural_end` is legal only
at a planned strong cadence or section end.

## Rules

```json
{
  "long_form_phrase_rules": {
    "planning_window_bars": 16,
    "minimum_connected_span_bars": 6,
    "maximum_strong_cadences_per_8_bars": 1,
    "minimum_cross_bar_notes_per_8_bars": 2,
    "minimum_motif_developments_per_section": 3,
    "maximum_independent_phrase_resets_per_8_bars": 1,
    "maximum_consecutive_full_rest_bars": 1,
    "require_delayed_peak": true,
    "require_delayed_resolution": true
  }
}
```

These values are validator targets. The compiler does not turn every musical preference
into an unconditional hard error.
