# Clean-Slate Bootstrap

This repository has completed the first cleanup step of the V2 reset.

## Active default context

```text
root SKILL.md
AGENTS.md
skills_v2/
materials_v2/
profiles/
the explicitly active project
required implementation under src/ scripts/ config/ tests/
```

`source_library/` is explicit-study only.

## Removed legacy context

The current tree no longer carries the former default creative knowledge system:

- old `skills/`;
- old `references/` composition/style guides;
- old instrument-research documents;
- long-form phrase/playbook experiments that were replaced by the V2 reset;
- clearly obsolete proof/demo projects.

Do not recreate these paths simply because old commits or stale comments mention them.

## Legacy recovery

Git history is archival storage, not default Agent context.

Only when the user explicitly requests recovery of a named old capability:

1. identify the exact missing capability;
2. inspect the smallest relevant old commit/file;
3. extract only the reusable fact;
4. verify it against the current implementation or a controlled experiment;
5. rewrite it as a V2 Skill, Material or Profile change;
6. keep obsolete project-specific material out of the current tree.

## Growth rule

Grow V2 through evidence:

```text
concrete task
-> failure or source observation
-> narrow fix
-> validation / listening success
-> reusable abstraction
-> Skill / Material / Profile promotion
```

Do not refill the repository with broad speculative playbooks merely to replace what was deleted.
