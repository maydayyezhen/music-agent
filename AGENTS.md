# Music Agent Clean-Slate Instructions

Read the root `SKILL.md` and `docs/clean_slate_bootstrap.md`.

## Active context

Only these sources are active by default:

- the user's current request;
- the current project being edited;
- `manifest.json` and registered native artifacts;
- implementation code and schemas required to run the task;
- explicitly selected skills under `skills_v2/`.

The previous knowledge library, prior instrument playbooks and complete example projects are cold
storage. Do not search, summarize or imitate them unless the user explicitly requests recovery of
a named capability.

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
3. Create or edit a structured source artifact.
4. Preserve a prior version for material changes.
5. Compile and render through the registered adapter.
6. Run data-integrity and round-trip checks relevant to that adapter.
7. Describe concrete audible or structural failures.
8. Fix the smallest responsible layer.

Do not require a universal form, motif process, harmony system, density curve, climax location or
instrument hierarchy.

## Rebuilding `skills_v2/`

Create a new skill only after a concrete task exposes reusable knowledge.

Every skill must define:

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

## Legacy recovery

Legacy recovery is opt-in. When explicitly requested:

1. identify one narrow question;
2. inspect the smallest relevant legacy passage;
3. extract the implementation fact;
4. rewrite it in style-neutral language;
5. add a test or inspectable validation rule;
6. place the cleaned result in `skills_v2/`;
7. do not import the original musical example.

## Honesty boundary

A successful compile proves that the pipeline accepted the data. It does not prove that the music
sounds good. A validator passing proves only the invariants it actually checks.
