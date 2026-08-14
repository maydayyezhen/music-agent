# Music Agent Clean-Slate Instructions

Read the root `SKILL.md` and `docs/clean_slate_bootstrap.md`.

## Active context

Only these sources are active by default:

- the user's current request;
- the current project being edited;
- `manifest.json` and registered native artifacts;
- implementation code and schemas required to run the task;
- explicitly selected Skills under `skills_v2/`;
- one explicitly selected material recipe under `materials_v2/` when timbre, texture or production is part of the request.

The previous knowledge library, prior instrument playbooks and complete example projects are cold
storage. Do not search, summarize or imitate them unless the user explicitly requests recovery of
a named capability.

Do not browse the entire material library. Resolve the requested instrument and texture, then read
the smallest matching recipe.

## Preserve the new architecture

The facade is thin:

```text
manifest/index
-> native artifact
-> adapter/compiler
-> renderer
-> derived output and report
```

Do not move notes, automation, plugin state or other rich native data into the manifest merely to
make one schema appear universal.

Prefer existing mature standards and project-native files. Add custom data only as a clearly
named extension or sidecar when no mature representation fits.

## Task workflow

1. Resolve the user's requested artifact and constraints.
2. Inspect the active project and the smallest necessary code path.
3. Select the narrowest matching `skills_v2/` Skill when behavior guidance is needed.
4. Select one `materials_v2/` recipe only when the user asks for a sound texture or production target.
5. Create or edit a structured source artifact.
6. Preserve a prior version for material changes.
7. Compile and render through the registered adapter.
8. Run data-integrity and round-trip checks relevant to that adapter.
9. Describe concrete audible or structural failures.
10. Fix the smallest responsible layer.

Do not require a universal form, motif process, harmony system, density curve, climax location or
instrument hierarchy.

## Rebuilding `skills_v2/`

Create a new Skill only after a concrete task exposes reusable knowledge.

Every Skill must define:

- trigger and scope;
- capability boundary;
- inputs and outputs;
- decision procedure;
- failure modes;
- validation method;
- provenance.

Skills should teach operations and constraints. They must not contain finished songs, copied
builders, signature progressions, full melodic phrases or validator statistics promoted from one
project.

## Rebuilding `materials_v2/`

Create a material recipe when a concrete listening task exposes a reusable relationship between an
instrument/source and a named texture.

Every material recipe should define:

- texture identity and searchable tags;
- suitable instrument or source prerequisites;
- performance prerequisites that processing cannot repair;
- practical starting ranges for source controls and processing;
- renderer or synthesis mappings where useful;
- failure modes;
- listening checks;
- provenance and uncertainty.

Materials decide how a performance should feel and sound. They do not decide melody, harmony, form
or a finished rhythm pattern.

A material recipe must not preserve a source song's exact notes, chord progression, form, velocity
sequence or full production chain as a template. Approximate settings must be labeled as starting
points rather than measured facts unless they were actually measured.

## Legacy recovery

Legacy recovery is opt-in. When explicitly requested:

1. identify one narrow question;
2. inspect the smallest relevant legacy passage;
3. extract the implementation fact;
4. rewrite it in style-neutral language;
5. add a test or inspectable validation rule;
6. place the cleaned result in `skills_v2/` or `materials_v2/` according to whether it describes behavior or sound;
7. do not import the original musical example.

## Honesty boundary

A successful compile proves that the pipeline accepted the data. It does not prove that the music
sounds good. A validator passing proves only the invariants it actually checks. A material recipe
provides a starting point, not a guarantee that every sample library or recording will respond the
same way.
