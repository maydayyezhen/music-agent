# Music Agent V2 Checkpoint

Updated: 2026-08-15
Branch: `agent/skills-v2-clean-slate`

## Current architecture

The repository now uses one canonical knowledge path:

```text
skills_v2/
materials_v2/
source_library/
profiles/
projects/<active-project>/
src + scripts + tests
```

The former `skills/` and `references/` knowledge systems, old instrument-research / long-form playbooks and clearly obsolete proof/demo projects have been removed from the current tree. They remain recoverable from Git history only when the user explicitly requests legacy recovery.

## Active knowledge policy

- `skills_v2/` contains reusable procedures and decision rules.
- `materials_v2/` contains reusable musical vocabulary promoted from evidence or validated experiments.
- `source_library/` contains original study sources and is explicit-study only.
- `profiles/` declares sound/performance implementation capabilities.
- `projects/` contains song-specific work and is not a default knowledge library.

## Current notable state

- `projects/gpt_etude_no_1/` is completed and archived.
- `skills_v2/chiptune_8bit/` provides the new chiptune routing scaffold.
- `profiles/chiptune_basic/` is a generic scaffold and does not claim real-console accuracy.
- `projects/_templates/chiptune_8bit/` is available for future 8-bit projects.
- Chiptune Materials must still be learned and validated before activation.

## Agent rule

For ordinary work, do not search Git history, deleted legacy files, unrelated complete projects or original source material.

Use:

```text
user request
-> active project
-> skills_v2 registry
-> materials_v2 registry
-> relevant profiles / implementation
-> render / validate / listen
```

Use `source_library` only for explicit study. Use Git history only for explicit legacy recovery.

## Execution boundary

The cleanup intentionally preserves implementation under `src/`, `scripts/`, `config/`, `profiles/` and `tests/`. Removing old Agent knowledge must not be confused with removing the deterministic execution layer.

No test-pass claim is recorded in this checkpoint. Run the repository's current validators/tests when a code change requires it.
