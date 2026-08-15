---
name: music-agent-v2
description: Route structured music work through the current V2 Skills, Materials, Profiles, project artifacts and deterministic execution layer.
---

# Music Agent V2

## Default composition route

```text
user request
-> creative-context policy
-> active project
-> complexity judgment
-> host subagent orchestration when useful and supported
-> relevant skills_v2
-> instrumentation / role plan when arranging multiple instruments
-> relevant materials_v2 per chosen instrument + role
-> profile
-> creative-safe Agent API contract
-> compiler / renderer without reading its source
-> MIDI / audio / report
-> listening feedback
```

For multi-instrument composition, **do not let Material retrieval choose the band lineup**. Resolve a lightweight instrumentation/role plan first, including section entry/exit, then retrieve Materials for those chosen roles.

For long, multi-section, multi-instrument or otherwise context-heavy composition, a capable host agent should also consider `complex-composition-orchestration`. The host may create focused subagents, but this repository does not implement a custom multi-agent framework.

## Complex composition route

For a short cue, small arrangement or narrow edit, work directly.

When scope becomes large enough that one context is likely to flatten details or pad duration with repetition:

```text
parent host agent
-> compact shared blueprint
-> smallest useful set of focused subagents
-> longitudinal musical responsibilities where possible
-> structured active-project artifacts
-> parent integration
-> instrument performance realization
-> build / render / inspect / patch
```

Prefer responsibility ownership such as melody, harmony, rhythm section, guitar arrangement, color layers or performance realization over arbitrary splits such as first minute / second minute / third minute.

More duration should create room for intentional recurrence, development, role evolution, section contrast, return and breathing space. Do not force constant novelty, but do not meet a long duration request primarily with low-information copying.

Every child uses the same creative-context firewall and only the active project plus relevant V2 knowledge surfaces. The parent remains responsible for accepting, rejecting, thinning and repairing child work.

See `skills_v2/complex_composition_orchestration/SKILL.md` for the full delegation contract.

## Creative-context firewall

Ordinary composition is allowlist-based. Read `config/creative_context.json` before expanding context.

Composition context may contain:

```text
AGENTS.md / SKILL.md / README.md / PROJECT_CHECKPOINT.md
skills_v2/
materials_v2/
profiles/
docs/agent_api/
projects/<active-project>/ only
```

Do not read or repo-wide search these surfaces during ordinary composition:

```text
scripts/
tests/
src/
source_library/
projects/<non-active-project>/
other docs/
```

Running a documented command is not permission to read its implementation.

If implementation knowledge is genuinely required, change task mode explicitly to `implementation_debug`, inspect the smallest necessary `src/` surface, update a neutral contract under `docs/agent_api/` when useful, then return to composition mode. `scripts/` and `tests/` remain outside that mode; use `test_maintenance` only for an explicit testing/maintenance task.

Use `source_study` only when the user explicitly asks to study, compare, verify or revisit an original source.

## Read order for composition

1. `config/creative_context.json`
2. `AGENTS.md`
3. this file
4. the active project explicitly named by the user, if one exists
5. `skills_v2/registry.json`
6. `complex-composition-orchestration` when task scope and host capabilities justify delegation
7. other relevant Skills
8. for multi-instrument composition, `instrumentation-role-planning`
9. `materials_v2/registry.json` and relevant Materials for chosen instruments/roles
10. required Profiles
11. `docs/agent_api/` for stable execution mechanics

Do not browse examples to learn APIs.

## Knowledge authority

```text
Skill       -> how to reason / operate
Material    -> reusable musical vocabulary
Project     -> concrete song decisions
Profile     -> declared implementation capability
Agent API   -> creative-safe execution contract
Source      -> original study evidence, explicit-study only
Renderer    -> derived execution
```

Keep those layers separate.

## Genre, instrumentation and energy

Treat these as separate dimensions.

```text
genre           -> compatibility / stylistic context
instrumentation -> which instruments are chosen
role            -> what each instrument does
energy          -> density, motion, weight, register and foreground pressure
```

Never assume:

```text
rock = loud
rock = distortion
rock = electric guitar only
pop-rock = one fixed band lineup
```

Genre tags may help rank already-compatible Materials, but they must not choose an instrument by themselves.

## Composition behavior

During composition:

```text
brief
-> choose required musical functions
-> choose instruments and section roles
-> establish harmony / tonal context as project decisions
-> compose foreground structure
-> retrieve compatible reusable Materials
-> combine / transform deliberately
-> render
-> listen / inspect
```

Do not browse unrelated completed projects as creative references.

## Melody execution neutrality

The composition Agent owns melodic decisions. The execution layer must not secretly compose them.

Canonical authored long-form mode:

```text
phrase_generation_mode: long_form_authored
```

Compatibility aliases `long_form_experimental` and `long_form` route to the same authored-only executor.

These labels are **semantic metadata, not executable musical instructions**:

```text
sequence
climax
resolution
variation
motif_operations
peak_bar
final_resolution_bar
delayed_target
```

They must not automatically transpose notes, create a rising contour, force a peak pitch, force the final tonic, move notes, lengthen endings or add vibrato.

Only concrete project data may change the melody. For long-form execution, use authored `motif_seed` content plus explicit `transform` / `note_overrides` when a transformation is desired. See `docs/agent_api/README.md`.

Pitch quantization and performance shaping are opt-in. The renderer must not silently repair a melody into its preferred scale or phrase arc.

## Validation neutrality

Validators may measure freely. Style-sensitive judgments must come from explicit project rules.

```text
missing rule -> measure, do not judge
explicit rule -> validate that declared intent
```

Do not make a composition conform to a hidden default merely to pass validation.

## Legacy boundary

The legacy Skill/reference/playbook architecture is removed from the current tree.
Do not search Git history or reconstruct it during normal work.

Only explicit user-requested legacy recovery may reopen old commits. Recover the smallest useful fact, translate it into V2 terminology, validate it, and promote it only when it still deserves to exist.

## Failure-driven growth

Prefer:

```text
make / render
-> hear or inspect a concrete failure
-> fix the smallest responsible layer
-> validate
-> promote reusable knowledge only after success
```

Do not grow the library with stereotyped or untested rules merely to make it look complete.
