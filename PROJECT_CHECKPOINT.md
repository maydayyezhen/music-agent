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

- `instrumentation-role-planning` is the thin default planning step for multi-instrument composition.
- Instrumentation and section roles are resolved before detailed Material retrieval.
- Genre tags are compatibility hints only; genre must not select instruments or imply energy.
- Broad Material shortlists should be expanded when one instrument family dominates without an explicit user constraint.
- Acoustic-guitar Materials now include broader `pop-rock` compatibility where the existing behavior already supports it.
- The shared ambiguous `guitar` render fallback no longer defaults to overdrive; new projects should use explicit guitar mappings.
- Demo/full-song scripts remain implementation examples only and are not creative templates.
- `lead-guitar-phrase-design` now teaches phrase-level lead-guitar writing: target-note arrivals, local motion, repeated-pitch permission, duration contrast, phrase-level space and arrangement-aware density.
- `expressive-target-note` is an active electric-guitar Material for developing important held arrivals through early pitch shaping, target establishment, delayed modulation/vibrato growth and optional same-pitch re-articulation.
- The user-provided `Still-Got-The-Blues-(For-You)-1.mid` study is registered as explicit-study source evidence for pitch-wheel/CC1 timing relationships; it does not establish universal bend intervals, slide labels or real finger-vibrato rate/depth.
- `projects/gpt_etude_no_1/` is completed and archived.
- `skills_v2/chiptune_8bit/` provides the chiptune routing scaffold.
- `profiles/chiptune_basic/` is a generic scaffold and does not claim real-console accuracy.
- `projects/_templates/chiptune_8bit/` is available for future 8-bit projects.
- Chiptune Materials must still be learned and validated before activation.

## Agent rule

For ordinary multi-instrument composition, use:

```text
user request
-> active project
-> skills_v2 registry
-> instrumentation / role / section-entry plan
-> materials_v2 registry by chosen instrument + role + behavior
-> relevant profiles / implementation
-> render / validate / listen
```

Do not reverse this into `genre -> Material -> instrument`.

Do not search Git history, deleted legacy files, unrelated complete projects or original source material during ordinary work.

Use `source_library` only for explicit study. Use Git history only for explicit legacy recovery.

## Execution boundary

The cleanup intentionally preserves implementation under `src/`, `scripts/`, `config/`, `profiles/` and `tests/`. Removing old Agent knowledge must not be confused with removing the deterministic execution layer.

Some preserved demo/full-song scripts may be inspected for schema/API/mechanics when necessary, but their instrumentation, form, harmony, density and mix decisions are not reusable creative authority.

No test-pass claim is recorded in this checkpoint. Run the repository's current validators/tests when a code change requires it.