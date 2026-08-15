# Scripts

`scripts/` is an execution and maintenance surface, not a creative knowledge library.

## Preferred use

For current work, prefer narrow generic entry points such as render, validate, import, audit and project-facade utilities when they fit the task.

Some older files remain here with names such as:

```text
build_*demo.py
build_*full_song.py
build_*demos.py
```

They may still be useful for regression, API discovery or implementation archaeology, but their musical constants are **not** active composition guidance.

## Hard boundary

When opening a demo/full-song builder to learn implementation:

```text
extract:
- current function signatures
- schema / JSON field usage
- compiler calls
- renderer calls
- file layout
- validation mechanics

ignore:
- instrument selection
- genre assumptions
- chord loops
- song form
- section lengths
- layer entry / exit
- rhythmic density
- melody
- dynamics
- mix balance
```

Do not copy a demo builder and then merely change tempo/key/title to create a new piece.

For a new composition, derive creative decisions from the active brief, relevant V2 Skills, the instrumentation/role plan, and role-matched Materials.
