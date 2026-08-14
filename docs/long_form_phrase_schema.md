# Long-Form Phrase Planning Schema

Long-form lead planning remains inside `instrument_phrase`, but the schema describes optional
planning data rather than one preferred dramatic arc.

Use `phrase_generation_mode: long_form_experimental` only when the current piece benefits from
explicit long-range planning. Formal songs otherwise use `legacy_stable` or omit the field.

Read `docs/creative_context_policy.md` before using this schema. Do not copy curves, bar counts,
register paths or cadence plans from another project.

## Design principle

A long phrase may be:

- cumulative or decaying;
- arch-shaped, wave-shaped, terraced or flat;
- sparse or continuous;
- repetitive, developmental or deliberately static;
- goal-directed or suspended;
- metrically regular or asymmetrical;
- resolved, unresolved or cyclic.

The schema records the piece's chosen behavior. It does not require a delayed peak, late high
note, final cadence, motif return or fixed phrase length.

## Section arc

```json
{
  "section_arc": {
    "section_id": "lead_section_1",
    "bars": [1, 11],
    "shape": "custom",
    "register_plan": ["low_mid", "mid", "mid", "high_mid", "mid"],
    "energy_curve": [0.35, 0.38, 0.34, 0.42, 0.47, 0.45, 0.51, 0.48, 0.44, 0.40, 0.32],
    "density_curve": [0.25, 0.40, 0.20, 0.35, 0.50, 0.30, 0.45, 0.25, 0.35, 0.20, 0.15],
    "arrivals": [
      {"bar": 7, "kind": "registral", "strength": 0.6}
    ],
    "breath_regions": [[3, 3], [8, 8]],
    "resolution_policy": "open"
  }
}
```

Only `section_id` and `bars` are required. Curves, arrivals, targets and register plans are
optional. When present, a curve contains one value per section bar.

`shape` may be `custom`, `arch`, `wave`, `terrace`, `accumulate`, `decay`, `flat`, `cyclic` or
another project-local descriptive value.

`resolution_policy` may be `closed`, `open`, `cyclic`, `interrupted` or `none`.

## Phrase relationship graph

```json
{
  "phrase_relationships": [
    {
      "phrase_id": "P1",
      "bars": [1, 3],
      "relationship": "introduce",
      "continuation_from": null,
      "continuation_to": "P2",
      "motif_operations": []
    },
    {
      "phrase_id": "P2",
      "bars": [4, 6],
      "relationship": "fragmentation",
      "continuation_from": "P1",
      "continuation_to": null,
      "motif_operations": ["shorten", "change_register"]
    }
  ]
}
```

Relationships may include `introduce`, `repeat`, `variation`, `sequence`, `extension`,
`fragmentation`, `augmentation`, `compression`, `continuation`, `answer`, `interruption`,
`recontextualization`, `climax`, `dissolution`, `resolution` or a project-local extension.

The graph does not need to cover the section with uniform four-bar blocks. Nodes may overlap,
leave gaps or describe cyclic relationships when the piece requires them.

## Melodic state

State is optional. Use it only when the phrase genuinely carries information across local
boundaries.

```json
{
  "melodic_state": {
    "active_motif": "motif_A",
    "current_register": "mid",
    "direction": "mixed",
    "tension": 0.48,
    "resolved": false,
    "continuation_required": false,
    "last_interval": -2,
    "last_note_function": "chord_tone"
  }
}
```

Projects may add instrument-specific state such as hand position, string group, bow direction,
breath reserve or pedal state. Do not create state fields merely to imitate another project.

A rest may preserve, transform or reset state. Declare that behavior explicitly when it matters:

```json
{
  "rest": {
    "at": "5:3",
    "duration": 1.5,
    "state_effect": "preserve"
  }
}
```

`state_effect` may be `preserve`, `relax`, `transform` or `reset`.

## Optional rule profile

Rules are opt-in project declarations. Omitted rules are not silently enabled.

```json
{
  "long_form_phrase_rules": {
    "minimum_connected_span_bars": 4,
    "maximum_consecutive_full_rest_bars": 2,
    "require_declared_arrival": false,
    "require_delayed_peak": false,
    "require_delayed_resolution": false,
    "require_cross_bar_notes": false,
    "require_motif_development": true,
    "allowed_phrase_lengths": [2, 3, 5]
  }
}
```

Validators should inspect only declared rules plus universal data-integrity constraints. They may
report descriptive metrics without turning stylistic preferences into failures.

## Universal checks versus stylistic checks

Universal checks may reject:

- invalid bar ranges;
- malformed curves;
- references to missing phrase IDs;
- impossible pitch/fingering declarations;
- overlapping monophonic events when overlap is not declared;
- unsafe controller realization.

Stylistic checks must remain advisory unless explicitly enabled by the project. Examples include:

- peak timing;
- cadence count;
- breath frequency;
- motif-development count;
- cross-bar-note count;
- continuous activity;
- high-register arrival;
- final thematic return.

The schema is a planning surface, not a hidden composition template.
