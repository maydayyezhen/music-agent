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
├── acoustic_strumming/
│   └── SKILL.md
├── midi_reference_analysis/
│   └── SKILL.md
└── chiptune_8bit/
    └── SKILL.md
```

Load Skills through `registry.json` and only when their triggers/scope match the current task.

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

## Forbidden shortcuts

Do not:

- reconstruct a deleted legacy Skill from Git history without explicit user request;
- paste a project's builder or complete composition into a Skill;
- promote exact source notes, progressions or density curves;
- treat one song's validator statistics as universal quality targets;
- load all Skills for every task;
- encode renderer, plugin or hardware-specific parameters as universal composition rules;
- duplicate Material cards inside Skills.

The V2 library should grow slowly enough that every active file has a clear reason to exist.
