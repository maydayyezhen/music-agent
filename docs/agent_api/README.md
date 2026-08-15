# Agent API

This directory is the **creative-safe execution contract** for Music Agent V2.

Its purpose is to let a composition Agent build, validate and render structured music without opening demo builders, tests, fixtures or implementation source.

No complete melody, chord progression or finished arrangement belongs here.

## Context boundary

During ordinary composition, use this directory instead of reading:

```text
src/
scripts/
tests/
unrelated projects/
```

If the contract here is missing a required mechanical fact, that is a documentation bug. Fix the contract during an implementation/debug subtask rather than making demo code part of composition context.

## Composition contract

A composition contains:

```text
metadata
sections
tracks
```

Each track may provide section clips containing either:

```text
events
```

or:

```text
instrument_phrase
```

but not both in the same clip.

Generic event shape:

```text
type: note | chord | drum | rest
at: <BAR:BEAT>
duration: <POSITIVE_BEATS>
velocity: <1..127>
pitch / pitches / note: <EVENT-SPECIFIC VALUE>
```

Use the active project to hold concrete musical values.

## Stable Python entry points

Load and validate structured composition data:

```text
from src.composition import load_composition, validate_composition
```

Generate track MIDI files and the full-song MIDI:

```text
from src.midi import generate_song_midis
```

The project is responsible for supplying explicit instrument mappings.

Do not read a build script merely to discover these calls.

## Authored long-form melody

Canonical mode:

```text
phrase_generation_mode: long_form_authored
```

Compatibility aliases `long_form_experimental` and `long_form` currently route to the same authored-only executor.

Required conceptual fields:

```text
instrument
role
phrase_type
energy
performance_intent.seed

tonality
# or legacy compatibility fields: key_root + mode, both explicit

register_midi
motif_seed
harmony
section_arc.bars
phrase_relationships
```

No key or mode is inferred.

`motif_seed` is authored musical content. Each item has:

```text
offset
duration
exactly one of:
  degree
  pitch
```

When `degree` is used, provide:

```text
motif_root_midi
```

Pitch policy for degree-derived material:

```text
pitch_quantization: none | scale
```

Default for authored long-form material:

```text
none
```

Direct `pitch` entries are exact authored pitches. Degree-derived pitches are quantized only when `pitch_quantization: scale` is explicitly requested.

## Relationship semantics

Relationship labels are descriptive:

```text
introduce
repeat
variation
sequence
extension
fragmentation
augmentation
compression
continuation
answer
climax
resolution
```

They do **not** change notes by themselves.

Likewise:

```text
motif_operations
```

is descriptive provenance / intent metadata and is not executable.

To change the motif, author an explicit:

```text
transform
```

Supported transform fields:

```text
slice: [START_INDEX, END_INDEX]
time_scale: POSITIVE_NUMBER
offset_shift_beats: NUMBER
degree_shift: INTEGER
ending_degree_delta: INTEGER
ending_duration_delta: NUMBER
```

For note-specific edits, use:

```text
note_overrides
```

Each override selects a transformed motif note by `index` and explicitly replaces or adjusts fields such as:

```text
offset
duration
degree
pitch
action
gesture
velocity
velocity_delta
cross_bar_reason
rest_type_after
bend_semitones
slide_from_semitones
vibrato
```

## Section arc semantics

`section_arc` may describe project intent, but optional labels do not execute melody changes.

Optional fields such as:

```text
peak_bar
final_resolution_bar
delayed_target
cadence_plan
```

are metadata until a project explicitly uses them in authored content or enables a validator rule.

The executor does not force a peak pitch, tonic ending or cadence from these fields.

## Realization semantics

Performance shaping is opt-in.

Examples of opt-in realization switches:

```text
enable_articulations
enable_pitch_bend
velocity_shaping
shape_note_lengths
```

Without these switches, authored duration and basic velocity behavior remain unembellished.

For guitar-specific performance semantics and the boundary between current executable fields, the existing Gesture IR sidecar, renderer Profiles, and not-yet-implemented physical fingering features, read:

```text
docs/agent_api/guitar_performance.md
```

Do not open `src/performance/` during ordinary composition to rediscover that contract.

## Validator contract

Validators may always report measurements.

Style-sensitive warnings are activated only by explicit project rules under:

```text
long_form_phrase_rules
```

A missing rule means:

```text
measure if useful
do not judge
```

This prevents the validator from becoming a hidden style template.

## Context-policy API

The machine-readable policy lives at:

```text
config/creative_context.json
```

Path decisions are mirrored by:

```text
from src.context_policy import creative_context_allowed, require_creative_context_path
```

Composition mode is deny-by-default outside its allowlist.
