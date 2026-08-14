# Creative Context Isolation Policy

This repository contains implementation research, validators, demos and complete proof songs.
Those materials have different purposes and must not be loaded into a composition context as if
they were one undifferentiated style library.

The goal is to preserve technical reliability without turning validated examples into musical
templates.

## Context classes

### 1. Method documents

Method documents explain capabilities, constraints and decision tools. They may be read during
normal composition work.

Examples:

- instrument ranges and physical constraints;
- MIDI/rendering architecture;
- articulation realization rules;
- harmony and voice-leading concepts;
- validation criteria;
- generic transformation operations.

A method document should avoid prescribing one key, chord loop, section length, motif, density
curve or climax location as the normal answer.

### 2. Primitive libraries

Primitive libraries provide reusable operations rather than finished musical identities.
They may be read during normal work.

Examples:

- strumming action vocabularies;
- chord-voicing search procedures;
- motif transformations;
- groove and articulation operators;
- instrument capability tables;
- renderer profiles.

A primitive is a tool such as `sequence_up`, `partial_strum`, `retain_common_tone` or
`delayed_vibrato`. A complete four-chord song, exact solo, fixed 16-bar arc or copied pitch list
is not a primitive.

### 3. Proof and demo projects

Files under `projects/` are executable evidence. They are not default composition references.
This includes their:

- `composition*.json` files;
- `build_song.py` scripts;
- core motifs;
- exact harmony and form;
- MIDI files;
- density curves;
- validation reports containing exact musical statistics.

Do not inspect a proof/demo project's musical content before writing a new piece merely because
it uses the same instrument or compiler path.

A proof project may be inspected only after a concrete implementation question exists, for
example:

- authored fingering disappeared during compilation;
- a slide produced no pitch curve;
- continuous strumming reset at a barline;
- a profile emitted an unsafe pitch bend;
- the renderer failed on a known supported feature.

When consulting a proof project, load only the smallest relevant file or passage and extract the
implementation fact. Do not copy its notes, harmony, form, register path, energy contour or
section proportions.

## Blank-slate order for new compositions

For a new song or substantial rewrite, use this order:

1. Read the user brief.
2. Create `musical-brief.md` and `creative-seed.md` before opening any complete example song.
3. In `creative-seed.md`, independently define:
   - the central audible idea;
   - rhythmic identity;
   - harmonic behavior;
   - formal behavior;
   - instrument roles;
   - silence and density behavior;
   - at least two possible development paths.
4. Read method documents and primitive libraries needed to make the idea playable.
5. Build and render the first draft with the current stable system.
6. Inspect proof/demo material only when a specific downstream failure requires it.
7. Record any consulted proof file and the narrow implementation fact taken from it.

The creative seed is not required to be conventional. It may be minimal, noisy, repetitive,
through-composed, asymmetrical, modal, non-functional, metrically unstable or deliberately
mechanical when the brief supports that choice.

## No canonical song arc

The following are optional compositional strategies, never universal requirements:

- motif statement followed by sequence;
- delayed climax;
- late high note;
- thematic return;
- 4/8/16-bar phrasing;
- verse/chorus energy growth;
- one strong cadence per eight bars;
- continuous lead activity;
- minor-pentatonic guitar vocabulary;
- open-chord acoustic accompaniment.

Validators may measure these when a project declares them, but they must not silently make every
song adopt them.

## Reference divergence check

Before accepting a new composition, compare it conceptually with every proof/demo project that
was consulted. At least two of the following must differ for musical reasons, not cosmetic
renaming:

- form or section proportions;
- meter or tempo behavior;
- harmonic rhythm or chord-function plan;
- motif rhythm;
- pitch/interval identity;
- register and fretboard path;
- density/energy contour;
- accompaniment texture;
- climax/arrival strategy;
- instrument hierarchy.

Changing only key, tempo, program number or a few pitches does not constitute a new composition.

## Documentation rule

New method documents must mark concrete examples as one possibility among several. Exact song
statistics belong in project-local reports, not in default skill instructions.

The default composition context should contain principles and tools. Finished songs stay outside
that context until a concrete debugging need opens the door.
