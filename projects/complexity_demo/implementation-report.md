# Music Complexity System implementation report

## Files inspected

- `AGENTS.md`, `README.md`
- `src/composition/loader.py`
- `src/midi/generator.py`, `src/midi/pitches.py`
- rendering, mixer, path/config loading, and narrow render scripts
- `projects/demo_song/composition.json`
- `references/composition-guidelines.md`
- `references/composer-checklist.md`
- `references/midi-agent-skill/SKILL.md`
- chord, groove, arrangement, voice-leading, and MIDI-cleanup references
- `work/validate_benchmarks.py`

There is no root project `SKILL.md`; project behavior is governed by
`AGENTS.md` plus the references above. The embedded MIDI Agent skill is
reference material and was not installed as a global Codex skill.

## Root cause

The former schema could express legal events, loops, pitches, instruments, and
sections, but had no structured target for complexity, section contour,
rhythmic identity, silence, or distributed role budgets. The MIDI generator
correctly expanded already-authored events, so it was not the right place to
guess artistic complexity. Existing review guidance could describe excessive
density after the fact, but it had no measurable profile-aware critic.

## Architecture

The new layer stays above MIDI rendering:

```text
brief / natural language
  -> global complexity + contour
  -> rhythm motifs + instrument identities + section budgets
  -> explicit composition events
  -> profile-aware critic
  -> unchanged MIDI / SoundFont / WAV pipeline
```

Pitch, rhythm design, and performance are separate decisions. The renderer
still consumes explicit events and does not add random notes.

## Changed and new files

- `src/complexity/schema.py`: levels, six dimensions, presets, contours,
  section override resolution, natural-language mapping.
- `src/complexity/rhythm.py`: pitch-independent A/A'/B/B'/C motif variations.
- `src/complexity/critic.py`: track/section metrics and contextual warnings.
- `src/composition/loader.py`: optional schema validation for complexity,
  motifs, clip annotations, and section budgets.
- `scripts/resolve_complexity.py`: inspect natural-language/preset resolution.
- `scripts/critic_complexity.py`: write a song complexity report.
- `scripts/build_complexity_demo.py`: deterministic five-level same-theme demo.
- `scripts/validate_complexity_demo.py`: WAV, stem, MIDI, critic, and progression validation.
- `config/complexity-presets.json`: minimal, simple, standard, rich, dense plus
  quiet_galgame, pop, brit_rock, minimal_ambient, and battle_dense.
- `config/composition.complexity.example.json`: compact schema example.
- `references/music-complexity.md`: mandatory Agent authoring guidance.
- `AGENTS.md`, `README.md`, `references/composer-checklist.md`: workflow integration.
- `tests/test_complexity.py`: compatibility, resolution, parsing, motifs,
  budgets, and demo identity/progression tests.

## Schema example

```json
{
  "complexity": {
    "level": "rich",
    "rhythm": 4,
    "harmony": 4,
    "arrangement": 4,
    "melodic_ornamentation": 3,
    "density": 3,
    "variation": 4
  },
  "complexity_contour": "verse_chorus",
  "sections": [{
    "name": "chorus",
    "bars": 8,
    "complexity_budget": {"lead": 4, "drums": 3, "bass": 2, "chords": 3, "texture": 1}
  }]
}
```

Section complexity overrides contour and global values. Budget points allocate
attention; they are not note quotas.

## Critic metrics

Track metrics: `note_density`, `rest_ratio`, `duration_entropy`,
`same_grid_ratio`, `velocity_variance`, `pattern_repetition`, and event count.
Section metrics: density, active tracks, track overlap, onset overlap, and
target/declared budget. Warnings cover melody without breath, unintentional
equal-grid behavior, shared onsets, continuous full arrangement, profile
mismatch, and duplicated busyness. Stable percussion and intentional minimal
repetition are not automatically treated as errors.

## Demo and compatibility result

Signal Garden keeps D Dorian, 100 BPM, 24 bars, piano lead, form, and the
structural eight-tone theme fixed. Its Theme B progresses from 3.50 to 12.75,
19.50, 23.75, and 30.50 events/bar. Track counts progress 3, 4, 5, 6, 6.
All five real WAVs are 59.6 seconds; every intended stem is non-silent, and all
full MIDIs have zero same-pitch overlaps, tiny notes, and stuck notes.

Complexity fields are optional. Missing fields resolve in memory to `standard`;
the loader never rewrites old composition files. The old `demo_song` loads and
renders through the unchanged MIDI/SoundFont/WAV path.
