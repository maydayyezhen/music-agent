# Composition Decision Guide

Read `docs/creative_context_policy.md` before creating a new piece.

This document offers decisions and checks for the repository's structured music workflow. It is
not a universal music grammar and does not define one preferred form, genre or development arc.
The user brief wins.

## Start with an audible identity

A piece needs a perceivable reason to exist, but that identity does not have to be a conventional
melodic motif.

Possible starting points include:

- a rhythm or groove;
- a pitch/interval cell;
- a chord color or harmonic process;
- a texture or register relationship;
- an instrument gesture;
- a timbral transformation;
- a drone or repeated note;
- silence and interruption;
- a formal process;
- a lyric/prosodic shape;
- deliberate noise or instability.

Choose the starting point that matches the brief. Do not automatically apply
`motif -> repetition -> variation -> contrast -> return` unless that process serves the piece.
Other valid processes include accumulation, erosion, looping, abrupt replacement, gradual
transformation, stasis, call-and-response, fragmentation, collage and unresolved continuation.

Record the independent idea in `creative-seed.md` before reading complete example projects.

## Brief, form and attention

Record genre or non-genre intent, mood, tonal behavior, tempo behavior, length, instruments,
production character and exclusions in `musical-brief.md`.

Translate adjectives into musical decisions, but allow more than one translation. For example,
“urgent” might use a tight pulse, unstable harmony, clipped releases, register pressure, abrupt
silence or accelerated timbral change. It does not simply mean higher velocity.

Form may be:

- verse/chorus;
- through-composed;
- cyclic;
- additive;
- subtractive;
- episodic;
- A/B or ternary;
- variation form;
- ambient process;
- loop with evolving production;
- asymmetrical or intentionally ambiguous.

An energy map is optional. A piece may rise, fall, wave, remain flat, reset, fracture or avoid a
single climax.

## Melody and foreground material

When pitch-based foreground material is used:

- Give it a recognizable identity through rhythm, interval, contour, register, articulation or
  timbre.
- Decide whether the listener should remember, follow, inhabit or merely notice it.
- Repetition may establish identity, hypnosis, insistence or stability.
- Variation may affect one or many dimensions; it is not mandatory in every return.
- Rests can create phrasing, but continuous motion is valid when intentional.
- A phrase may resolve, evade, loop, dissolve or be interrupted.
- Highest pitch is not automatically the climax. Rhythm, harmony, timbre, density and silence can
  carry the arrival.
- A hook is required only when the brief calls for hook-centered writing.
- Avoid scale-safe wandering without rhythmic, intervallic or textural purpose.

For guitar, strings, winds and other player-like parts, make the foreground compatible with a
plausible physical or declared experimental technique.

## Harmony

Choose harmony for the piece's behavior rather than for compliance with a default pop function.
Possible approaches include:

- functional motion and cadences;
- modal centers;
- pedal tones and drones;
- planing;
- chromatic voice-leading;
- static sonority;
- polymodal or polytonal layers;
- ambiguous roots;
- non-tertian structures;
- deliberate dissonance or noise spectra.

When voice-leading matters, retain common tones and control register/spacing. When discontinuity
is intentional, large shifts and unrelated blocks may be the point.

Extensions, inversions and suspensions are functional/color tools, not decorations to add by
quota. Dense low voicings should be used consciously because they can obscure bass and attack.

## Rhythm and time

Give each active role a temporal identity. That identity may be steady, syncopated, rubato,
polyrhythmic, sparse, mechanical, elastic or non-metric.

Avoid making every instrument share the same onset grid unless unison/mechanical behavior is the
idea. Silence is a first-class structural event, but continuous texture is also valid.

Tempo, meter and quantization may be stable or changing. Preserve the chosen anchors when adding
performance timing.

## Instrument-specific writing

### Bass

Bass may provide foundation, counterline, pedal, rhythmic hook, texture or silence. Do not reduce
it automatically to repeated roots. Roots, fifths, approaches, inversions, passing tones,
register shifts and rests are available choices. Relationship with kick may be tight, partial or
independent according to the style.

### Guitar

Guitar is not piano MIDI with another program number. Choose a physical/textural role such as
strum, fingerpicking, riff, muted pulse, arpeggio, octave line, double-stop response, sustained
feedback, harmonic/noise gesture or lead phrase. Respect tuning and reachable shapes when normal
playability is intended.

### Piano and keyboards

Separate hand/register functions when physical piano writing matters. Other keyboard roles may be
single-line synth, repeated chord machine, cluster texture, arpeggiator, organ plane or sound
design layer. Chord tones need not attack simultaneously or share duration.

### Strings

Strings may sustain harmony, move as independent lines, create texture/noise, reinforce a motif or
remain silent until a structural event. Do not automatically duplicate keyboard chord blocks.

### Pad and sustained textures

A pad may provide atmosphere, glue, tension, movement or spectral change. It need not play every
section or retrigger every beat. Keep register and masking intentional.

### Drums and percussion

Establish the desired pulse language, not a mandatory rock backbeat. Consider limb feasibility
when modeling a conventional player. Accents, ghost notes, open sounds, fills and crashes should
have structural or gestural reasons rather than fixed bar quotas.

Electronic or impossible percussion is valid when explicitly intended.

## Arrangement and Point/Line/Plane

Use Point/Line/Plane as an observation tool:

- **Point:** isolated attack or accent;
- **Line:** connected motion;
- **Plane:** sustained or continuous field.

No fixed balance is universally correct. Pointillist, drone-based, monophonic and dense
counterpoint pieces are all valid. Ensure the chosen hierarchy is audible and roles do not
accidentally mask one another.

Introduce, remove or transform layers for musical reasons. Do not assume every piece needs a
pre-chorus build and chorus payoff.

## Performance and humanization

Performance detail follows the intended style:

- velocity may follow meter, phrase, gesture, timbre or deliberate machine consistency;
- durations distinguish connected, muted, sustained and percussive behavior;
- timing offsets should preserve important anchors;
- chord tones should move together unless a roll/strum is intended;
- kick and snare need not always be tighter than other parts outside conventional groove music;
- humanization is not mandatory for intentionally mechanical music.

Check overlaps, stuck notes, tiny accidental events, impossible ranges and controller conflicts.
Random timing/velocity cannot rescue weak musical identity.

## Render, critique and revise

The first successful WAV is evidence, not completion.

Save `composition_v1.json`, render, and describe concrete audible results in `critique.md`.
Revise the smallest layer responsible for the issue. Preserve prior versions.

Critique the current piece against its brief, not against the statistics or form of a proof song.
Useful observations include:

- the intended identity is or is not perceivable;
- hierarchy is unclear;
- a texture masks the foreground;
- the rhythm lacks the intended weight;
- the renderer lost an authored articulation;
- a repeated section changes too much or too little for the declared process.

Before acceptance, perform the reference-divergence check from
`docs/creative_context_policy.md` for every complete example consulted.
