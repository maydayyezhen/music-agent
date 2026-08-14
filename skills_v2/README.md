# Skills V2

This directory is the only default Music Agent knowledge/skill workspace during the clean-slate
phase.

It starts intentionally small. Do not bulk-copy files from `references/`, `skills/`, old
playbooks or proof projects.

## Directory model

```text
skills_v2/
├── README.md
├── _template/
│   └── SKILL.md
└── project_architecture/
    └── SKILL.md
```

Add a new skill only after a concrete project exposes a reusable problem.

## Skill properties

A good V2 skill is:

- narrow enough to load only when relevant;
- based on capabilities and decisions, not a finished song;
- explicit about inputs, outputs and failure conditions;
- style-neutral unless the user asks for a style-specific skill;
- backed by a test, validator or inspectable artifact;
- free of mandatory keys, chord loops, section lengths and melodic templates.

## Forbidden migration shortcuts

Do not:

- copy an old skill and rename it V2;
- paste a proof project's builder into a skill;
- promote exact notes, progressions or density curves;
- treat validator statistics from one song as universal quality targets;
- load all skills for every task.

The V2 library should grow slowly enough that every file still has a clear reason to exist.
