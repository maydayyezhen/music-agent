# Long-Form Phrase Analysis

## Scope inspected

The audit covered the root `SKILL.md`, composition validation in
`src/composition/loader.py`, lead realization in
`src/instruments/electric_guitar.py`, instrument dispatch/export in
`src/instruments/compiler.py`, clip materialization in
`src/accompaniment/generator.py`, MIDI articulation encoding in
`src/midi/generator.py`, instrument validation in
`src/validation/instrument_aware.py`, and the current
`projects/instrument_aware_full_song/composition.json` and
`semantic_phrases.json`.

## Concrete source of the short-sentence bias

### The schema has no long-range melody object

`validate_composition()` validates an `instrument_phrase` as one flat object with
`instrument`, `role`, `phrase_type`, `energy`, `performance_intent` and a seed. It has
no representation for a section arc, phrase relationships, unresolved state, cadence
placement, delayed target notes, breaths, or structural silence. A four-bar fill and a
sixteen-bar melodic paragraph therefore look identical to the loader.

### `_lead()` is a literal local event translator

`src/instruments/electric_guitar.py::_lead()` iterates directly over
`phrase["motif"]`. For each item it assigns a string/fret, copies the item's onset,
duration and articulations, and emits one note. It neither sees nor plans the complete
section, and it stores only a local `preferred_fret`. There is no melodic state object;
unresolved pitch, direction, motif version and continuation intent are discarded.

The function also accents item zero and bend items. That makes each newly authored
motif list sound like a fresh entrance. Bend and vibrato are encoded correctly later,
but no structural layer decides whether they mean continuation, climax or cadence.

### Clip looping can repeat a closed phrase

`src/midi/generator.py::_expand_track()` materializes one clip and repeats it for every
`loop_bars` window. This is correct infrastructure, but if a lead clip contains a
closed one-to-four-bar motif it repeats the closure wholesale. The MIDI layer cannot
recover the missing long-range intent.

### The latest song manually restarts every four bars

In `projects/instrument_aware_full_song/composition.json`, the lead sections use
`phrase_type: melodic_lead`. The sixteen-bar Verse, Chorus and Final Chorus place new
groups at bars 1, 5, 9 and 13. These groups reuse near-identical onset contours and end
with a 1.3-beat sustained note; chorus groups also repeatedly attach bend plus vibrato.
The gap before the next group resets the perceived sentence even though the containing
clip is sixteen bars long.

This is the prohibited architecture in practice:

```text
for each four-bar block:
    author a complete motif list
    end on long sustain/vibrato
    leave a multi-bar gap
```

### Current validators cannot see narrative continuity

`src/validation/instrument_aware.py::analyze_instrument_aware()` checks range,
guitar string/fret feasibility, repetition, velocity, density, register collision and
note spacing. It does not count independent resets, cadence strength, cross-bar notes,
motif transformations, phrase-boundary state, peak timing, or articulation concentration
at phrase endings. A playable MIDI can therefore pass while still behaving as unrelated
short sentences.

## Articulation is downstream, not the root cause

`src/midi/generator.py::_expand_track()` correctly converts semantic bend and vibrato to
pitch-wheel curves. The defect occurs earlier: a flat motif list mechanically places
those articulations at each local ending. Adding more pitch curves, random overlap or
velocity variation would preserve the same sentence structure.

## Missing state

The existing generator preserves fret preference inside one compile call but does not
preserve:

- active motif and transformation version;
- current register and long-range direction;
- unresolved/resolved status;
- continuation requirement across phrase boundaries;
- delayed target pitch and target bar;
- last interval and harmonic function;
- breath versus structural-end semantics;
- cadence strength.

Consequently, the next phrase cannot be required to answer or complete the previous one.

## Required architectural correction

Keep `melodic_lead` plus `phrase_generation_mode: legacy_short_phrase` unchanged for
compatibility. Add a `long_form` path with three mandatory representations, in this
order:

1. section arc for the complete 8–16 bars;
2. relationship graph for dependent subphrases;
3. deterministic note/performance realization driven by a persistent melodic state.

The long-form compiler must see the entire harmony window. Breaths preserve state;
only a structural ending may reset it. Articulation is assigned after the arc and
relationship decisions, and the dedicated validator measures narrative continuity rather
than merely MIDI legality.
