# Projects

Projects are song-specific workspaces, not reusable Agent knowledge.

## Default rule

Open only the project explicitly named by the user or created for the current task.

Do not scan sibling projects to learn style, arrangement, harmony, density, melody, instrumentation or mix targets.

## Special directories

- `_templates/` contains structural scaffolding only.
- completed/archived projects stay closed unless the user explicitly reopens them.
- benchmark, reconstruction and reference-demo projects may be inspected only for a concrete implementation, schema, conversion or verification question.

## Implementation-example boundary

Sometimes a project build script is the easiest way to understand a current API. That permission is mechanical, not creative.

When inspecting an existing project for implementation details:

```text
may reuse:
schema shape
API calls
manifest conventions
compiler / renderer wiring
validation mechanics

must not inherit:
instrument lineup
section form
chord progression
melody
rhythmic density
entry / exit plan
energy map
mix hierarchy
```

A filename containing a genre such as `pop_rock`, `british_rock` or `jpop` does not turn that project into a style template.

Reusable lessons belong in `skills_v2/`, `materials_v2/` or `profiles/`, not in cross-project imitation.
