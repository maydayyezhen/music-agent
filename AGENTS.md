# Music Agent V2 Instructions

This file is the coding/composition Agent entry point for the current repository.

## First rule: choose a context mode

Read `config/creative_context.json` first.

For ordinary music creation use `composition` mode. It is deny-by-default outside this allowlist:

```text
skills_v2/
materials_v2/
profiles/
docs/agent_api/
projects/<active-project>/ only
canonical root instructions / registries
```

Do not open or repo-wide search `src/`, `scripts/`, `tests/`, `source_library/`, unrelated projects or arbitrary docs during ordinary composition.

The separation is structural. Do not rely on a prompt such as "ignore the example melody" after loading a demo into context.

## Explicit mode changes

Use a wider surface only when the task itself requires it:

```text
composition          creative work, default
implementation_debug add src/ only for a concrete implementation problem
source_study         add source_library/ only for explicit source study
test_maintenance     add tests/ and scripts/ for explicit maintenance/regression work
```

After implementation investigation, prefer documenting the neutral execution contract in `docs/agent_api/` so future composition Agents do not need the implementation source.

Running a documented command does not mean reading the script that implements it.

## Canonical creative context

Use these knowledge surfaces by default:

```text
skills_v2/       reusable procedures and decision rules
materials_v2/    reusable musical vocabulary
profiles/        declared sound/performance capabilities
docs/agent_api/  neutral execution contract
projects/        only the project explicitly being edited
```

`source_library/` is evidence and explicit-study only.

## Required composition read order

1. `config/creative_context.json`
2. root `SKILL.md`
3. the user's request and active project
4. `skills_v2/registry.json`
5. relevant Skill files only
6. for multi-instrument composition, resolve instrumentation + role + section entry/exit before Material retrieval
7. `materials_v2/registry.json`
8. relevant Material cards for chosen instruments/roles
9. required Profiles
10. `docs/agent_api/` when execution mechanics are needed

Do not browse examples to discover schemas or APIs.

## Arrangement routing rule

For multi-instrument composition, use the thin `instrumentation-role-planning` Skill before selecting detailed Materials.

The order is:

```text
brief
-> required musical functions
-> instrument palette
-> per-section roles / entry / exit
-> Material retrieval by instrument + role + behavior
```

Do **not** reverse this into `genre -> Material -> instrument`.

Keep these dimensions separate:

```text
genre           stylistic compatibility
instrumentation chosen sound sources
role            musical function
energy          density / motion / register / weight / foreground pressure
texture         articulation / sustain / rhythmic surface / timbre
```

Never use shortcuts such as `rock = loud`, `rock = distortion`, or `rock = electric guitar only`.

## Melody authorship boundary

The Agent composes; the executor executes.

Canonical semantic mode:

```text
phrase_generation_mode: long_form_authored
```

The old names `long_form_experimental` and `long_form` remain compatibility aliases but use the same authored-only semantics.

The execution layer must not infer musical content from semantic labels. In particular:

```text
relationship = sequence    != transpose automatically
relationship = climax      != move upward automatically
relationship = resolution  != force tonic automatically
peak_bar                   != force highest note there
delayed_target             != rewrite a note into that pitch
motif_operations           != executable transform
```

A desired musical change must be represented concretely in project data. For long-form motifs use explicit `transform` / `note_overrides`, or author the resulting material directly.

Do not silently quantize authored melody. `pitch_quantization` is explicit. Do not silently add guitar expression or alter note gates; realization shaping is opt-in.

## Validator boundary

Validators may compute measurements, but aesthetic requirements are not defaults.

Only enforce a style-sensitive condition when the active project declares the corresponding `long_form_phrase_rules` entry.

```text
undeclared aesthetic -> no warning
explicit project rule -> validate it
```

This prevents validation targets from becoming a hidden house melody style.

## Hard no-example rule for composition

`tests/`, fixtures, demo builders, regression songs and unrelated finished projects are not composition memory.

Do not:

- open a builder to learn the API;
- search for a working melody schema across projects;
- use a fixture as a seed;
- retrieve an unrelated project because it has a similar genre;
- inspect implementation source just to get creative ideas.

Use `docs/agent_api/` for mechanics. If that contract is incomplete, fix the contract in an explicit implementation task.

## Skill policy

Create or revise a Skill only for a reusable operation, decision procedure, capability boundary, failure mode or validation method.

Do not put complete songs, fixed chord progressions, signature riffs or renderer presets into a Skill.

## Material policy

Materials may be numerous and stylistic. They should contain reusable musical vocabulary learned from evidence or controlled experiments.

Genre words in a Material id or tag describe provenance or compatible context, not a claim that the Material is the standard answer for that genre.

Do not promote exact source melody, full rhythm sequence, full harmony or complete arrangement.

## Project policy

A project is song-specific state, not reusable knowledge.

- Open only the active project named by the user.
- `_templates/` is structural scaffolding only.
- Archived/completed projects remain closed unless explicitly reopened.
- Never load all projects to "learn the house style".

## Source-library policy

`source_library/` contains original evidence. It is not composition memory.

Open it only for requests such as study, compare, verify, analyze or revisit an original source. Promote only abstract reusable results to V2.

## Profile policy

Profiles declare available implementation capabilities. Never invent unsupported keyswitches, CC mappings, chip modes, plugin behavior or hardware limits.

## Execution honesty

A successful compile means the pipeline accepted the data. It does not prove the music sounds good.
A validator proves only its declared invariants.
Listening feedback may override a technically valid but musically poor result.
