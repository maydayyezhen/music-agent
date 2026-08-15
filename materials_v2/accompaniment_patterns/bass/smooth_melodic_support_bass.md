# Smooth Melodic Support Bass

## Identity

- id: `smooth-melodic-support-bass`
- kind: `accompaniment_pattern`
- instruments: electric bass, finger bass, fretless-style bass
- roles: bass foundation, melodic support, connective low line
- character: connected, rounded, supportive, lightly melodic

## Use when

Use this Material when the bass should feel like one continuous musical sentence rather than a sequence of isolated roots, while remaining clearly subordinate to the lead.

The main idea is:

```text
harmonic anchor
+ nearby connective motion
+ rhythmic breathing
+ recognizable contour
```

The line should be interesting enough to hear when soloed, but simple enough to disappear naturally into the arrangement.

## Source observations

Promoted from a user-provided MIDI study of a smooth pop/soul bass reference.

Observed in the studied bass channel:

- 516 completed notes;
- GM program 35;
- pitch range MIDI 26-48;
- no CC64 sustain events;
- no pitch-wheel events;
- median note duration about 0.70 beat;
- median onset spacing 1.0 beat;
- median note-off to next-note-on gap about 0.22 beat;
- common onset gaps included 0.5 beat (217), 1.5 beats (164), and 1.0 beat (58);
- about 36.1% of adjacent notes repeated the same pitch;
- about 25.2% moved by one or two semitones, excluding repeats;
- about 95.7% of adjacent moves stayed within five semitones;
- velocity range was 109-124 with median 115 in this particular export.

These measurements describe the MIDI source, not universal target values.

## Musical behavior

### Anchor first

Keep a small number of strong harmonic anchors. Roots are useful, but chord tones and stable pedal tones may also carry the floor.

Do not turn every beat into a new root announcement.

### Connect locally

Between anchors, prefer compact motion such as:

- same-note re-articulation with changed duration;
- semitone approach;
- whole-tone approach;
- neighboring tone;
- small chord-tone movement;
- one- or two-note pickup into the next anchor.

Large jumps should be occasional structural gestures, not the default connector.

### Mix hold and motion

The source suggests a useful family in which shorter movements alternate with longer spaces or holds. A half-beat move followed by a longer interval before the next attack can create forward motion without making the line busy.

Do not copy one exact onset mask. Preserve the relationship:

```text
move briefly
-> let the line breathe
-> arrive clearly
```

### Preserve a contour

Across two or more beats, the bass should have a direction: rising, falling, circling a local anchor, or approaching a new register.

A useful bass line can contain many repeated pitches and still be melodic if the rhythm, duration and neighboring motion create a phrase.

## Articulation

Smooth does not require full MIDI legato.

Start with moderately long gates that leave small natural gaps or renderer release between many notes. Use overlap only when the actual sound source benefits from it and does not create unwanted polyphony.

For this Material, phrase continuity is more important than forcing every note to touch the next note.

## Variation

Keep one phrase identity across a section, then vary one dimension at a time:

- replace one repeated anchor with a nearby approach note;
- lengthen a stable tone;
- add a short pickup before a section arrival;
- shift a connector by one scale/chord tone;
- remove a connector under a busy vocal or lead;
- move one phrase ending into a nearby register.

## Compatible Materials

- `normal-pop-rock-bass` for a simpler foundation underneath or in alternate sections;
- `section-linked-pop-rock-bass` when the bass must change density with guitar arrangement roles;
- `groove-motif-bass` when a smooth line needs a little more rhythmic identity or an occasional octave lift.

When combining with `groove-motif-bass`, borrow motif identity selectively. Do not automatically import its short-gate density or frequent octave movement.

## Failure modes

### Root-only line

The part is harmonically correct but has no contour.

Add one or two purposeful connectors instead of rewriting every note.

### Too many passing notes

The bass begins behaving like a lead instrument.

Restore anchors and silence. Remove connectors that do not clearly approach, leave or decorate an anchor.

### Mechanical quarter pulses

Every attack is equally spaced and equally weighted.

Mix holds, short pickups and small rhythmic displacements.

### Fake smoothness by overlap

Notes overlap heavily but the contour still feels disconnected.

Fix the pitch and phrase logic first, then revisit gate/release.

### Register wandering

The line drifts because every connection chooses a new direction.

Keep most motion local and reserve larger jumps for phrase resets or deliberate arrivals.

## Listening checks

Solo the bass and ask:

- can the phrase be followed as a line rather than a list of chord roots?
- are the anchors still obvious?
- do the connectors point somewhere?
- does the bass leave enough room for the foreground melody?
- when placed back in the mix, does it feel continuous without demanding attention?

## Provenance and boundary

Derived from measurements of a user-provided reference MIDI. Exact melody, harmony and complete rhythmic sequence are intentionally excluded. The source used a fretless-bass GM program, but this Material describes the **musical line behavior**, not a required timbre. A dedicated creamy/fretless sound Profile should be created only after separate timbre/rendering study.
