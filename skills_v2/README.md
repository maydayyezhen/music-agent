# Skills V2

`skills_v2/` is the only active Music Agent Skill library in the current tree.

The legacy `skills/`, old composition/reference guides and old playbooks have been removed. Do not search Git history for them during normal work. Legacy recovery is opt-in and must be explicitly requested by the user.

## Directory model

```text
skills_v2/
├── README.md
├── registry.json
├── _template/
│   └── SKILL.md
├── project_architecture/
│   └── SKILL.md
├── instrumentation_arrangement/
│   └── SKILL.md
├── melody_structure_development/
│   └── SKILL.md
├── acoustic_strumming/
│   └── SKILL.md
├── lead_guitar_phrase_design/
│   └── SKILL.md
├── bass_line_continuity/
│   └── SKILL.md
├── midi_reference_analysis/
│   └── SKILL.md
└── chiptune_8bit/
    └── SKILL.md
```

Load Skills through `registry.json` and only when their triggers/scope match the current task.

`instrumentation-role-planning` is intentionally thin and is the default planning step for multi-instrument composition. It chooses musical functions, instrument roles and section entry/exit before detailed Material retrieval; it must not grow into fixed genre instrumentation templates.

`melody-structure-development` is the generic melody-composition layer. It separates structural targets from surface notes, develops small germs through recurrence and controlled transformation, plans phrase relationships, and adds embellishment only after the underlying line works. It is style-neutral and must not invent instrument articulation or turn historical common-practice exercise rules into universal constraints.

`lead-guitar-phrase-design` remains the lead-guitar-specific phrase layer: contour, target-note arrival, duration contrast, repeated-pitch permission, within-phrase continuity and phrase-level space. It may be used alongside the generic melody Skill, but bend, slide, vibrato and other guitar-specific articulations still require separate evidence or Profile capability and must not be inferred merely because the instrument is a guitar.

## Skill properties

A good V2 Skill is:

- narrow enough to load only when relevant;
- based on capabilities and decisions, not a finished song;
- explicit about inputs, outputs and failure conditions;
- style-neutral unless a style-specific capability genuinely needs a stable routing boundary;
- backed by a test, validator, source study or inspectable artifact as the capability matures;
- free of mandatory keys, chord loops, section lengths and melodic templates.

Concrete musical vocabulary belongs in `materials_v2/`. Sound-library, renderer and hardware implementation details belong in `profiles/`.

## Growth rule

Prefer:

```text
concrete task or source study
-> observed failure / evidence
-> reusable procedure
-> narrow Skill
-> validation
-> registry activation
```

Do not add a broad Skill merely because the library looks sparse.

A broad source study may justify a generic Skill when it produces stable decision procedures, but it does **not** automatically justify activating many Materials. Style-specific phrase devices, density choices and ornament habits should still be validated against real projects, MIDI / score sources or listening tests before registry activation.

## Forbidden shortcuts

Do not:

- reconstruct a deleted legacy Skill from Git history without explicit user request;
- paste a project's builder or complete composition into a Skill;
- promote exact source notes, progressions or density curves;
- treat one song's validator statistics as universal quality targets;
- load all Skills for every task;
- encode renderer, plugin or hardware-specific parameters as universal composition rules;
- duplicate Material cards inside Skills;
- encode `genre -> fixed instrument lineup` or `genre -> fixed energy` shortcuts into a Skill;
- turn one historical pedagogy source into universal modern style law.

The V2 library should grow slowly enough that every active file has a clear reason to exist.
