# Scripts

`scripts/` is an execution, regression and maintenance surface. It is **not creative context**.

## Hard context boundary

During ordinary composition, an Agent must not open or search files under `scripts/`.

Running a documented command is different from reading its source:

```text
allowed during composition:
use a command documented in docs/agent_api/

not allowed during composition:
open the script to discover how it works
search build_* files for examples
copy constants from a regression/demo builder
```

If the creative-safe contract is missing a mechanical fact, switch explicitly to an implementation/debug task, inspect the smallest required implementation surface, then document the neutral API under `docs/agent_api/` before returning to composition.

## Why this is strict

A script can contain technically convenient test data such as concrete notes, chord progressions, section shapes or instrument choices. Even when those values were never intended as musical advice, putting them into an LLM's composition context can bias the result.

The former rule of "read a demo for mechanics but ignore its musical constants" is retired. The default is now structural isolation, not prompt-level self-restraint.

## Preferred use

Use scripts for:

```text
rendering
conversion
validation
maintenance
regression generation
explicit implementation debugging
```

Keep reusable creative knowledge in `skills_v2/` and `materials_v2/`. Keep stable creative-safe execution contracts in `docs/agent_api/`.
