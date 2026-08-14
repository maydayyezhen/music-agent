---
id: rolling-triplet-acoustic-strum
kind: accompaniment_pattern
status: active
---

# Rolling Triplet Acoustic Strum

## Purpose

Use this material for a loose, rolling acoustic-guitar groove built from triplet timing rather than straight eighths or sixteenths. It works well for folk, western-adjacent, country-adjacent and acoustic-rock accompaniment when the guitar should feel like it is rocking forward instead of marching on an even grid.

This card describes a reusable rhythm family. Do not copy the source song's pitches, harmony, arrangement or full MIDI sequence.

## Core rhythmic idea

Divide each quarter-note beat into three equal triplet positions.

A common family emphasizes the first and late-triplet positions:

```text
1 trip let  2 trip let  3 trip let  4 trip let
X   .   x   X   .   x   X   .   x   X   .   x
```

The important relationship is the long-short spacing:

```text
anchor -> late-triplet = about 2/3 beat
late-triplet -> next anchor = about 1/3 beat
```

Do not flatten this into equal eighth notes. The uneven spacing is the groove.

The exact sounding mask may vary by bar. Omit or thin some late-triplet attacks, especially around vocals, phrase endings or chord changes.

## Stroke direction family

When the performance source or renderer supports directional sweep:

- beat anchors may use a low-to-high downstroke;
- late-triplet returns may use a high-to-low upstroke;
- the middle triplet slot may remain silent while the hand resets or travels;
- the upstroke does not have to be a tiny upper-string flick. It can carry two to five strings and have real rhythmic weight.

Do not apply these directions blindly to reference MIDI with simultaneous block onsets. Direction is only recoverable when the source preserves within-stroke string timing or another source supplies the articulation.

## Stroke width

Use a mix of medium and broad attacks rather than repeating one identical block chord.

Useful relationships:

- anchor downstroke: medium to broad;
- late-triplet upstroke: medium, sometimes nearly as broad as the anchor;
- phrase transition: temporarily narrow one attack or omit it;
- chord change: favor the voices that make the new harmony legible while allowing compatible tones to ring.

This groove loses its rolling body when every upstroke is reduced to a brittle two-string tick.

## Sustain and connection

Let compatible voices continue ringing across the next attack when possible. Re-trigger only the strings that the current stroke needs.

A practical feel is:

```text
broad ringing anchor
+
late-triplet return stroke
+
continued resonance under the next beat
```

Avoid making every note gate exactly at the next attack unless the intended style is deliberately dry or muted.

## Sweep realization

A user-provided MIDI study that motivated this card preserved explicit within-stroke timing. In the studied main steel-string guitar part:

- 125 BPM and 192 ticks per beat were encoded;
- grouping adjacent note-ons within 12 ticks produced about 1015 strum groups from 3074 note-ons;
- the median group contained three notes;
- attack groups aligned overwhelmingly to beat starts and the late triplet position, with essentially no middle-triplet attack family;
- on beat-start groups with recoverable direction, low-to-high motion strongly dominated;
- on late-triplet groups with recoverable direction, high-to-low motion almost completely dominated;
- within-stroke spread had a median around 20 ms and a 90th percentile around 47.5 ms;
- note duration had a median around 0.78 quarter-note beats;
- velocity varied meaningfully, with a median around 86 and a broad practical range in the source.

These measurements are source-study evidence, not universal defaults.

For a new renderer, a reasonable starting family is a compact sweep that remains clearly a strum rather than an arpeggio. Scale spread with stroke width and tempo, and use the source-library profile when an instrument already contains recorded strum articulations.

## Variation controls

Vary the groove without destroying its identity by changing one or two of these at a time:

- omit an occasional late-triplet return;
- make one anchor broader or narrower;
- change which common tones are re-triggered;
- slightly alter velocity between anchor and return;
- let phrase-ending notes ring longer;
- thin the groove under a foreground vocal or lead;
- restore a broader return stroke when the arrangement opens up.

Keep the long-short triplet relationship recognizable across related bars.

## Failure modes

Revise when:

- the groove has been quantized into equal eighths;
- every beat uses an identical full block chord;
- every upstroke is forced to be tiny and brittle;
- explicit sweep spread is so large that the chord becomes an arpeggio;
- random timing noise obscures the stable triplet lattice;
- middle-triplet attacks are added everywhere and erase the long-short rocking feel;
- source-specific chord progressions or exact MIDI sequences are copied instead of abstracting the pattern family.

## Provenance boundary

This material was abstracted from a user-provided MIDI source studied specifically for acoustic-guitar strumming. The source supplied evidence for triplet placement, within-stroke direction, sweep spread, note duration and velocity behavior. It does not establish the commercial recording's exact guitar, microphone, room, EQ, compression or production chain.
