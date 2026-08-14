# Long-Form Minimal Rollback Audit

## Planning-layer changes retained

- `docs/long_form_phrase_analysis.md` documents the original short-fragment problem.
- `docs/long_form_phrase_schema.md` defines Section Arc, Phrase Relationship and Melodic State.
- `src/melody/long_form.py::RELATIONSHIPS`, `_operations()` and the state trace in
  `compile_long_form_lead()` preserve motif development, peak, cadence and continuation plans.
- `src/validation/long_form_phrase_validator.py::analyze_long_form_phrases()` retains cadence,
  peak, motif, reset, silence, register-curve and cross-bar continuity statistics.
- `scripts/build_long_form_phrase_demos.py`, `tests/test_long_form_phrase.py` and
  `projects/long_form_phrase_demos/` remain the reproducible experimental A/B framework.

## Melody-generation changes

`src/instruments/electric_guitar.py::compile_phrase()` is the mode gate. A missing mode or
`legacy_stable` calls the original `_lead()` translator. Only an explicit
`long_form_experimental` (plus the readable migration alias `long_form`) calls
`_long_form_lead()`.

`src/melody/long_form.py::compile_long_form_lead()` still converts the complete Section Arc and
relationship graph to notes, but its safe default realization now:

- uses plain picked notes unless articulation is explicitly enabled;
- emits no bend unless `realization.enable_pitch_bend` is explicitly true;
- ends each note no later than the next note unless a sound-library profile explicitly allows
  legato overlap;
- permits a bar-crossing duration only when `cross_bar_reason` names a musical purpose;
- does not automatically lengthen a resolution or append vibrato at every phrase ending.

## Articulation and realization changes

The previous implementation mechanically mapped motif `action` values to slide, hammer-on,
pull-off and bend, and added `vibrato` to the last note of every resolution relationship. The
same function also expanded any `cross_bar` note beyond the bar by at least 0.45 beat. Those
behaviors caused an effect-heavy result and made a validation quota capable of changing the
sound. They are disabled by default and cross-bar notes now require semantic reasons.

`profiles/general_midi/profile.json` previously used a 1.04 gate ratio for its legato fallback,
which could create overlap even though General MIDI has no profile-defined overlap-legato
trigger. It now uses 1.0.

## MIDI export and Pitch Bend risk

`src/midi/generator.py::_expand_track()` builds pitch curves from `bend_semitones` and
`vibrato`. Previously `_musical_track()` emitted those channel-wide Pitch Bend events without
checking whether another note was sounding on the same channel. A bend could therefore move a
second overlapping note. `_musical_track()` now drops a note's pitch curve whenever any other
note overlaps its active interval. The bend generator also uses a gradual multi-point curve
instead of a two-step target/reset jump.

The new skeleton fixture contains no Pitch Bend, vibrato, slide, hammer/pull, keyswitch, random
CC, timing randomness, chords or overlapping notes.

## Formal-flow integration

`scripts/render_song.py` exports Long-Form plans and validation only when a composition contains
an explicitly experimental Long-Form phrase. It does not choose the experimental mode.
Composition loading defaults a missing `phrase_generation_mode` to `legacy_stable`.

No data in `projects/instrument_aware_full_song/` was modified or rendered. Its composition,
MIDI and final-WAV hashes were recorded before and after this work.

## Test-only and independent assets

- The original demos under `projects/long_form_phrase_demos/` remain experiments.
- The dependent song `projects/electric_guitar_rock_long_form/` remains an experimental artifact;
  it is not a default template or formal song dependency.
- `tests/fixtures/lead_guitar_long_form_v2/` is the new plain eight-bar melody skeleton.

## Current default

The formal and legacy-compatible default is `legacy_stable`. Experimental planning and
realization require the explicit value `long_form_experimental`. The old strings
`legacy_short_phrase` and `long_form` remain readable migration aliases, not defaults.
