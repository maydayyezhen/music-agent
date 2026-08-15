# Music Agent

一个面向通用 Agent 的结构化音乐工作区。当前知识体系只认 V2，并对**创作上下文**与**实现/测试上下文**做硬隔离。

## Canonical architecture

```text
user intent
-> config/creative_context.json   context firewall
-> skills_v2/                     reusable decision procedures
-> instrumentation / roles        choose musical functions before patterns
-> materials_v2/                  reusable musical vocabulary for chosen roles
-> projects/<active-project>/     song-specific structured source
-> profiles/                      renderer / instrument capability mapping
-> docs/agent_api/                creative-safe execution contract
-> compiler / renderer            execution, normally not read by composer
-> MIDI / audio / reports         derived outputs
```

Original reference sources are separate:

```text
source_library/
-> explicit source_study mode only
-> reusable abstraction
-> skills_v2/ or materials_v2/
```

## Creative context firewall

Ordinary composition uses an allowlist. The Agent may read:

```text
skills_v2/
materials_v2/
profiles/
docs/agent_api/
projects/<active-project>/ only
canonical root instructions / registries
```

It must not open or repo-wide search these by default:

```text
src/
scripts/
tests/
source_library/
unrelated projects/
arbitrary docs/
```

Why so strict? A demo builder or fixture can contain a perfectly concrete melody, chord progression or phrase arc even when it was intended only as test data. Once loaded into an LLM context, that data can bias composition. The repository therefore uses structural exclusion rather than asking the model to "look but not imitate".

Machine-readable policy:

```text
config/creative_context.json
```

## Context modes

```text
composition          default creative work
implementation_debug explicit implementation inspection; adds src/
source_study         explicit original-source study; adds source_library/
test_maintenance     explicit tests/scripts maintenance
```

Running a command documented under `docs/agent_api/` does not require reading its script source.

## Agent read order

1. `config/creative_context.json`
2. `AGENTS.md`
3. root `SKILL.md`
4. the active project explicitly named by the user
5. `skills_v2/registry.json` and relevant Skills
6. resolve instrumentation + role + section entry/exit for multi-instrument work
7. `materials_v2/registry.json` and relevant Materials
8. required Profiles
9. `docs/agent_api/` for execution mechanics

## Retrieval principle

Do not use genre as a hidden instrument selector.

```text
genre != instrumentation
genre != energy
rock != distortion
rock != electric-guitar-only
```

Genre tags are compatibility hints. Instrument choice comes from musical functions and the active brief; Material choice comes after instrument/role planning.

## Melody authorship principle

The LLM/project owns the melody. The deterministic layer must not secretly compose it.

Canonical long-form mode:

```text
phrase_generation_mode: long_form_authored
```

Compatibility aliases `long_form_experimental` and `long_form` use the same authored-only executor.

Semantic labels do not execute musical changes:

```text
sequence   != auto-transpose
climax     != auto-rise
resolution != auto-tonic
peak_bar   != forced highest pitch
```

Concrete changes require explicit project data such as `transform` or `note_overrides`. Pitch quantization, articulation, bend, velocity shaping and gate shaping are explicit/opt-in.

## Validation principle

Validators measure freely but do not carry a hidden house style.

```text
missing aesthetic rule -> measure only
explicit project rule   -> validate it
```

## Hard boundaries

- `skills_v2/` is the only active Skill library.
- `materials_v2/` is the only active reusable musical-material library.
- Complete projects are not style templates or composition memory.
- Tests, fixtures and demo builders are not creative references.
- `source_library/` is explicit-study only.
- Profiles are capability declarations, not permission to invent unsupported behavior.
- Stable mechanical contracts belong in `docs/agent_api/`, not in musical examples.

## Repository roles

```text
skills_v2/       how to reason
materials_v2/    reusable musical vocabulary
source_library/  original evidence, explicit-study only
profiles/        sound/performance capability mappings
projects/        active or archived song-specific work
docs/agent_api/  neutral execution contract
src/             implementation, debug context only
scripts/         execution/maintenance, not creative context
tests/           regression, not creative context
```
