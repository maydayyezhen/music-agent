# Electric guitar writing

Read `docs/instrument_research/electric_rhythm_guitar.md` and
`docs/instrument_research/electric_lead_guitar.md`. Choose a rhythm or lead phrase type, tuning,
register, energy and performance intent. Keep keyswitches out of the phrase.

For a substantial Lead Guitar theme or solo, `docs/guitar_native_lead_playbook.md` is required
reading. Follow its motif -> hand path -> connected development -> delayed target -> thematic
return workflow. Render and audit the real MIDI before proposing system changes. Use
`projects/guitar_native_rock_proof/` as evidence, never as a lick library.

For lead parts spanning 8–16 bars, also read `docs/long_form_phrase_analysis.md` and
`docs/long_form_phrase_schema.md`. Formal generation defaults to `legacy_stable`. Use
`phrase_generation_mode: long_form_experimental` only for an explicit planning experiment.
Plan the section arc and relationship graph before note realization; breaths preserve state.

When a guitar-native line has an intentional fingering path, motif notes may declare zero-based
`planned_string` plus `planned_fret`; the compiler verifies that the pair produces the authored
pitch. A position-changing note may also declare `slide_from_semitones` with the semantic
`slide` articulation. Use these only for deliberate hand movement, not on every note.
