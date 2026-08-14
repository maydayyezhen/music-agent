# Electric guitar writing

Read `docs/creative_context_policy.md`, then read
`docs/instrument_research/electric_rhythm_guitar.md` or
`docs/instrument_research/electric_lead_guitar.md` as needed.

Choose the musical role, tuning, register, physical vocabulary, energy and performance intent
from the current brief. Keep keyswitches out of the phrase.

For a substantial Lead Guitar theme or solo, read
`docs/guitar_native_lead_playbook.md` as a playability and realization guide. It provides a menu
of operations such as position-preserving variation, sequence, fragmentation, repeated picking,
legato groups, slides, bends and vibrato. It does not prescribe one form.

Do not automatically impose:

- motif -> upward sequence -> delayed high target -> descending thematic return;
- a continuous 16/32-bar solo;
- minor-pentatonic vocabulary;
- a late peak;
- fixed four-bar phrase relationships;
- the form, harmony, register path or density arc of an existing proof project.

Before opening any complete guitar proof/demo project, write the new piece's `creative-seed.md`
and first-draft structure independently. A proof project may be inspected only to answer a
specific implementation question after rendering, such as lost fingering, missing slide curves,
unsafe pitch bend or broken continuity. Read the smallest relevant passage and record the narrow
fact used.

For lead parts spanning 8–16 bars, `docs/long_form_phrase_schema.md` offers optional planning
fields. Declare only the rules serving the current piece. Formal generation defaults to
`legacy_stable`; use `phrase_generation_mode: long_form_experimental` only for an explicit
planning experiment. A breath preserves state only when the piece actually declares a persistent
stateful phrase.

When a guitar-native line has an intentional fingering path, motif notes may declare zero-based
`planned_string` plus `planned_fret`; the compiler verifies that the pair produces the authored
pitch. A position-changing note may also declare `slide_from_semitones` with the semantic
`slide` articulation. Use these for deliberate physical motion, not as decorative stamps.

The plain-note skeleton must work before articulation. Playability is a constraint; one prior
song's dramatic architecture is not.
