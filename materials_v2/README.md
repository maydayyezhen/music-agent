# Materials V2

`materials_v2/` is an opt-in library of reusable sound and production recipes.

It is not a composition skill library and it is not a collection of finished-song templates.

Use it to answer questions such as:

- what kind of instrument source fits a requested texture;
- how to shape attack, body, grain, width and room;
- which processing chain is a sensible starting point;
- which audible failures indicate the wrong source or wrong settings.

## Library boundary

A material recipe may contain:

- a texture name and searchable tags;
- suitable instrument and playing prerequisites;
- source/sample-selection guidance;
- relative performance and rendering guidance;
- suggested EQ, dynamics, saturation, stereo and ambience ranges;
- code-synthesis equivalents when useful;
- failure modes and listening checks.

A material recipe must not contain:

- a complete copyrighted source file;
- a finished song's chord progression, melody or exact rhythm sequence;
- a source MIDI note list or velocity sequence;
- a claim that approximate settings were objectively measured when they were not;
- mandatory brand-specific plugins when a generic processing description is enough.

## Context policy

Materials are never loaded by default. Select one recipe explicitly by texture, instrument or production goal.

Composition skills decide what the instrument plays. Material recipes decide how that performance should feel and sound. Renderers and profiles translate the recipe into available controls.

## Recipe status

Each recipe should distinguish:

- `identity`: the intended audible result;
- `requirements`: what the source and performance must already provide;
- `starting_ranges`: practical starting points, not universal truths;
- `renderer_mapping`: how to approximate the texture with samples, synthesis or effects;
- `failure_modes`: signs that the result has drifted away from the target.
