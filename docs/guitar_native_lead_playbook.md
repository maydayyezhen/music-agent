# Guitar-Native Lead Writing

This document is a capability and playability guide. It is not a song template, lick library or
required dramatic arc.

Read `docs/creative_context_policy.md` first. Write the new piece's `creative-seed.md` before
opening any complete guitar demo or proof project.

## What must survive

A convincing guitar part needs its musical identity and physical logic to survive the pipeline:

```text
musical role
-> pitch/rhythm skeleton
-> playable hand path
-> performance actions
-> neutral events
-> profile/controller realization
-> rendered audio
```

The plain pitch/rhythm skeleton should already make sense. Bends, slides and vibrato cannot turn
an unrelated collection of phrases into one coherent performance.

## Universal physical considerations

These are constraints and questions, not stylistic prescriptions:

- Is the written range playable for the chosen tuning?
- Can adjacent notes be reached with a plausible string/fret path?
- Are hammer-ons and pull-offs assigned to reachable same-string movements?
- Does a slide connect an actual source and destination?
- Does a bend have a target and enough time to be perceived?
- Is pitch-bend realization channel-safe?
- Are intentional double-stops or chords declared rather than accidental overlaps?
- Does repeated picking have a feasible rhythmic engine?
- Are position changes audible musical decisions rather than random teleportation?

A piece may intentionally violate normal guitar technique, but that choice should be explicit.

## Choose a lead archetype from the brief

Do not default every electric-guitar part to a long ascending rock solo. Possible roles include:

- sparse answering phrases;
- repeated-note rhythmic hook;
- low-register riff;
- lyrical sustained theme;
- angular intervallic line;
- modal drone improvisation;
- tremolo-picked texture;
- octave melody;
- double-stop response;
- noise/feedback gesture;
- through-composed solo;
- deliberately static motif;
- fragmented interjections;
- cyclic pattern with gradual timbral change.

The user brief determines whether the part develops, repeats, dissolves, interrupts, resolves or
remains suspended.

## Build an original creative seed

Before consulting complete examples, define:

1. rhythmic identity;
2. interval or pitch identity;
3. register and physical region;
4. phrase/rest behavior;
5. harmonic relationship;
6. development options appropriate to this piece;
7. what the guitar must avoid.

The seed may be one note, a chordal gesture, a rhythm, a noise envelope or a conventional motif.
Do not force a melodic motif when texture is the real idea.

## Development operations

Use these as independent primitives. No fixed order is required.

### Pitch and contour

- sequence up or down;
- invert or mirror selected intervals;
- retain contour while changing interval size;
- pedal around one pitch;
- displace selected notes by octave;
- narrow or widen the range;
- approach a target chromatically;
- avoid resolution deliberately.

### Rhythm

- repeat a picking cell;
- compress or expand durations;
- shift accents;
- add/remove pickups;
- fragment the tail;
- sustain across a barline;
- interrupt with silence;
- alternate dense and sparse responses;
- preserve mechanical timing intentionally.

### Guitar mechanics

- remain inside one position;
- connect positions by slide;
- change strings while retaining fret shape;
- use same-string legato groups;
- move from picked to legato articulation;
- introduce repeated-string retriggers;
- add double-stops or octave shapes;
- move from fretted notes to harmonics/noise when supported.

### Form

- statement and variation;
- accumulation;
- erosion/dissolution;
- call and response;
- cyclic return;
- interrupted development;
- multiple independent episodes;
- flat hypnotic repetition;
- late arrival;
- early climax followed by decay;
- no climax at all.

A delayed high target and thematic return are only two possible strategies.

## Fingering fields

When physical placement matters, motif notes may declare:

```json
{
  "pitch": "G4",
  "at": "3:2.5",
  "duration": 0.5,
  "velocity": 92,
  "planned_position": "custom_region_a",
  "planned_string": 3,
  "planned_fret": 12,
  "articulations": ["slide"],
  "slide_from_semitones": -2.0
}
```

`planned_string` is zero-based against the configured tuning. The compiler verifies that the
string/fret pair produces the authored pitch.

Use explicit fingering only when it affects the music or realization. Do not annotate every note
merely to satisfy a template.

## Articulation as causal action

Articulation should explain a physical transition:

- `hammer_on`: source note and reachable higher fret;
- `pull_off`: source note and reachable lower fret;
- `slide`: connected source/destination and transition direction;
- `bend`: target interval and curve;
- `bend_release`: return or continuation behavior;
- `vibrato`: delayed start, rate and depth when supported;
- `palm_mute`: right-hand damping state;
- `accent`: intentional attack emphasis;
- `sustain`: intentional held target.

Do not stamp an articulation periodically because a prior example used it.

## Arrangement interaction

The other tracks should support the current lead role, not a generic rock blueprint.

Ask:

- Which register must remain open?
- Which rhythm belongs to the foreground?
- Should accompaniment continue, thin out, answer or disappear?
- Does the harmony need to clarify the lead or remain ambiguous?
- Is the guitar the line, point, plane or noise layer in this section?

Acoustic strumming, bass roots, rock drums and organ pads are not mandatory companions.

## Render-first diagnostic loop

For important guitar work:

```text
compose from the current brief
-> render MIDI/WAV
-> identify a concrete audible failure
-> inspect the smallest relevant compiler/profile/proof passage
-> fix only the failing layer
-> regenerate with musical data held constant when testing the system
```

Useful diagnostics include:

- note/phrase continuity;
- unintended resets;
- impossible fingering;
- excessive or accidental overlap;
- missing authored position data;
- unsafe bends;
- slide/vibrato realization;
- repeated exact phrase windows;
- register collisions;
- whether articulation changed the intended rhythm;
- whether accompaniment obscures the chosen lead role.

Diagnostics describe the current piece. They do not prescribe the statistics of another song.

## Use of proof projects

Complete proof projects under `projects/` exist to demonstrate implementation behavior. Do not
read their exact musical content during blank-slate composition.

After a specific failure, a proof project may answer a narrow question such as:

- how `planned_string` survives normalization;
- how a profile maps `slide_from_semitones`;
- how pitch-wheel safety is checked;
- how a validator reports overlap.

Record the file consulted and the implementation fact extracted. Do not reuse its notes,
harmony, form, density curve, climax location or register path.

## Anti-patterns

- changing only key and tempo from a proof song;
- using the same section lengths and density arc as the nearest demo;
- treating minor pentatonic as the default guitar language;
- forcing every solo upward toward a late bend;
- making every phrase four bars;
- adding vibrato to every long note;
- using articulation to disguise a weak skeleton;
- copying a validated build script and replacing pitch lists;
- reading full project examples before establishing the new creative seed;
- allowing validators to invent the composition's style.

The target is not one ideal guitar solo. The target is an authored musical idea that remains
playable, editable and faithfully realizable.
