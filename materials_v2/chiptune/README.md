# Chiptune Materials Scaffold

This directory is a routing/index surface for future 8-bit/chiptune Materials.

Do **not** treat files here as active musical knowledge by default. Active reusable knowledge must still be promoted into the canonical Material kind directories and registered in `materials_v2/registry.json`.

## Intended destinations

Future chiptune knowledge should be classified by existing Material kinds instead of creating a parallel all-in-one chiptune schema.

```text
materials_v2/
├── accompaniment_patterns/
│   └── chiptune/
├── instrument_gestures/
│   └── chiptune/
├── phrase_devices/
│   └── chiptune/
├── timbre_recipes/
│   └── chiptune/
└── production_chains/
    └── chiptune/
```

Create those subdirectories only when there is at least one real promoted Material for the category.

## Promotion rule

A future agent should not add a card because a pattern is stereotypically associated with chiptune.

Preferred workflow:

```text
reference study or controlled experiment
→ extract reusable invariant
→ identify Material kind
→ write narrow card
→ validate in a project
→ register active card
```

Keep exact source melody, harmony and full rhythmic sequences out of reusable Materials.

## Examples of possible future families

These names are placeholders for research directions, not currently validated Materials:

- pulse-based harmony implication
- rapid arpeggio texture
- limited-voice counter-line
- low-register chip bass motion
- noise/percussion gesture
- register-sharing orchestration
- voice-stealing / role-handoff recipe
- chip-style pitch ornament

Do not register these names until they are actually studied.
