# Groove Motif Bass

## Identity

- id: `groove-motif-bass`
- kind: `accompaniment_pattern`
- instruments: electric bass, synth bass
- roles: groove foundation, melodic rhythm-section voice, section drive
- character: syncopated, motif-led, stepwise, springy but controlled

## Use when

Use this Material when the bass should have a recognizable rhythmic/melodic identity of its own instead of merely following chord roots or copying the kick.

The main idea is:

```text
short attack syntax
+ recurring motif
+ stepwise contour
+ purposeful octave displacement
```

The part may be very short-gated and still feel continuous if the phrase identity is strong.

## Source observations

Promoted from a user-provided MIDI study of a funk/disco-oriented bass reference.

Observed in the studied bass track:

- 730 completed notes;
- GM program 38;
- pitch range MIDI 24-55;
- no CC64 sustain events;
- no pitch-wheel events;
- median note duration about 0.22 beat;
- median onset spacing 0.5 beat;
- median note-off to next-note-on gap about 0.28 beat;
- common onset gaps included 0.5 beat (312), 0.25 beat (169), 0.75 beat (92), 1.0 beat (52), and 2.0 beats (46);
- about 11.2% of adjacent notes repeated the same pitch;
- about 49.2% moved by one or two semitones, excluding repeats;
- about 66.5% stayed within five semitones;
- exactly one-octave adjacent moves occurred 111 times: 79 upward and 32 downward;
- velocity range was comparatively narrow at 98-110 with median 101.

These values describe this MIDI export. They are not universal quality targets.

## Musical behavior

### Build a motif before filling harmony

Give the bass a small recurring identity made from:

- a characteristic onset pattern;
- a short contour;
- a repeated anchor relationship;
- one or two connective notes;
- an optional register jump.

Repeat and transform this identity across several bars instead of generating each bar independently.

### Favor stepwise motion inside the motif

Use semitone and whole-tone motion to make the short attacks read as one phrase.

The line may move quickly, but adjacent notes should often remain locally related. This prevents dense rhythms from becoming random low-note confetti.

### Use octave displacement as punctuation

An octave jump can:

- lift a repeated pitch without changing harmonic function;
- reset register;
- emphasize a syncopated attack;
- create a short call/answer inside the bass part.

Do not use octave jumps on every cycle. In smoother styles, borrow this device sparingly.

### Let rhythm carry groove

The source had relatively stable velocity, so the groove cannot be explained by velocity randomization alone.

Prioritize:

```text
onset placement
+ rests
+ contour
+ motif recurrence
+ octave placement
```

before adding humanization noise.

## Articulation

Short gates are compatible with coherent musical motion when the motif is strong.

Do not infer that all melodic bass should use short gates. This Material is specifically the groove-motif family. For a rounded or creamy support line, combine only selected ideas with `smooth-melodic-support-bass`.

## Variation

Useful transformations include:

- keep the rhythm and change one approach pitch;
- keep the contour but move the motif to a new anchor;
- replace one local note with its octave;
- remove a dense tail under an active foreground phrase;
- extend the final anchor to create contrast against the short motif;
- answer the first bar with a simplified second bar.

## Compatible Materials

- `smooth-melodic-support-bass` for longer sustain and more relaxed phrase flow;
- `normal-pop-rock-bass` when a section needs a simpler, less foreground rhythm-section role;
- `section-linked-pop-rock-bass` when motif density should change with the arrangement.

## Failure modes

### Funk everywhere

The motif is applied to every section even when the arrangement needs calm support.

Reduce attack density or switch to a smoother Material for quieter sections.

### Octave trampoline

Frequent octave jumps become the main audible gimmick.

Keep octave displacement as punctuation, not a compulsory beat pattern.

### Random sixteenth notes

The line is busy but has no repeated identity.

Define a short motif and transform it rather than re-rolling every attack.

### Velocity-humanize placebo

The groove depends on random velocity variation while the actual note pattern remains flat.

Fix onset placement, rests and contour first.

### Lead competition

The bass motif becomes more memorable and active than the intended foreground melody.

Thin the tail, simplify octave gestures, or preserve only the motif's rhythmic skeleton.

## Listening checks

Solo the bass and ask:

- can a short motif be recognized after several bars?
- do stepwise moves connect the short attacks into a phrase?
- are octave jumps purposeful and memorable rather than constant?
- does the groove survive if velocity variation is reduced?
- in the full mix, does the bass add personality without becoming the lead?

## Provenance and boundary

Derived from measurements of a user-provided reference MIDI. Exact melody, harmony and complete rhythmic sequence are intentionally excluded. The source used a synth-bass GM program, but the reusable object here is the motif-led bass behavior rather than that exact sound.
