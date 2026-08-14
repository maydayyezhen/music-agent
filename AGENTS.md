# Music Agent Clean-Slate Instructions

Read the root `SKILL.md` and `docs/clean_slate_bootstrap.md`.

## Active context

These sources are active by default:

- the user's current request;
- the current project being edited;
- `manifest.json` and registered native artifacts;
- implementation code and schemas required to run the task;
- relevant Skills under `skills_v2/`;
- `materials_v2/registry.json`;
- multiple relevant material cards under `materials_v2/`.

The previous knowledge library, prior instrument playbooks and complete example projects are cold storage. Do not search or imitate them unless the user explicitly requests recovery of a named capability.

The V2 materials library is not cold storage. It is active external musical memory. Browse its registry during composition, retrieve several plausible cards, and use them as vocabulary for harmony, voicing, accompaniment, instrument behavior, texture and production.

Large material retrieval is acceptable when it improves the result. Prefer a coherent shortlist over arbitrary context limits.

## Preserve the new architecture

The facade is thin:

```text
skills + retrieved materials
-> manifest/index
-> native artifact
-> adapter/compiler
-> renderer
-> derived output and report
```

Do not move notes, automation, plugin state or other rich native data into the manifest merely to make one schema appear universal.

Prefer existing mature standards and project-native files. Add custom data only as a clearly named extension or sidecar when no mature representation fits.

## Task workflow

1. Resolve the user's requested artifact and constraints.
2. Inspect the active project and necessary code path.
3. Select relevant `skills_v2/` Skills for operations and constraints.
4. Read `materials_v2/registry.json`.
5. Retrieve material cards across all relevant dimensions, including harmony, voicing, accompaniment, phrasing, timbre and production.
6. Compare candidate materials and decide which ideas can coexist.
7. Adapt materials through transposition, revoicing, rhythmic variation, density changes, orchestration changes and section-aware development.
8. Create or edit the structured source artifact.
9. Preserve a prior version for material changes.
10. Compile and render through the registered adapter.
11. Run relevant data-integrity checks.
12. Describe concrete audible or structural failures.
13. Fix the smallest responsible layer or retrieve additional material when the vocabulary is insufficient.

Do not require a universal form, motif process, harmony system, density curve, climax location or instrument hierarchy.

## Rebuilding `skills_v2/`

Create a Skill when a concrete task exposes a reusable operation or decision procedure.

Every Skill should define:

- trigger and scope;
- capability boundary;
- inputs and outputs;
- decision procedure;
- failure modes;
- validation method;
- provenance.

Skills teach how to work. Materials provide concrete things worth trying.

## Growing `materials_v2/`

Create or extend material cards whenever a listening, MIDI, score or production study exposes reusable musical vocabulary.

The library may contain:

- chord voicing families;
- harmonic colors and chord-motion tendencies;
- accompaniment and rhythm-pattern families;
- instrument gestures and articulation combinations;
- phrase shapes, pickups, fills, transitions and cadence devices;
- orchestration and register combinations;
- texture and production recipes;
- renderer-specific mappings;
- small synthetic examples and parameterized fragments.

Each material card should define searchable tags, applicability, transformation options, incompatibilities, failure modes and provenance.

Materials may be stylistic. Multiple overlapping cards are welcome because comparison and accumulation improve the Agent's choices.

Do not convert one complete copyrighted song into a default reusable template. Do not copy a source's full melody, chord progression, form, exact rhythm sequence or production automation wholesale. Extract, label, transform and recombine the useful parts.

## Retrieval behavior

During composition:

1. search by instrument, role, texture, energy, genre and musical problem;
2. retrieve several cards, not necessarily only one;
3. include contrasting candidates when the direction is uncertain;
4. prefer cards with concrete examples and listening checks;
5. explain which cards informed the result when that matters;
6. add a new card after a successful experiment reveals a reusable result.

Do not avoid the material library merely to keep context small. Context is a resource to manage, not an enemy to starve.

## Legacy recovery

Legacy recovery is opt-in. When explicitly requested:

1. identify the useful capability or material;
2. inspect the smallest relevant legacy source;
3. extract the reusable fact or pattern;
4. rewrite it into V2 terminology;
5. place it in `skills_v2/` or `materials_v2/` according to whether it describes an operation or musical material;
6. retain provenance and uncertainty;
7. do not import a complete finished composition as the reusable object.

## Honesty boundary

A successful compile proves that the pipeline accepted the data. It does not prove that the music sounds good. A validator passing proves only the invariants it checks. A material card is a candidate vocabulary item, not a guarantee that every arrangement, sample library or mix will respond the same way.
