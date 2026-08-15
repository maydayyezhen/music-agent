---
name: acoustic-guitar-continuous-strumming
description: Write and revise subdivision-based acoustic-guitar strumming with explicit hand motion, stroke coverage, sustain and renderer separation.
status: active
---

# Acoustic Guitar Continuous Strumming

## Purpose

Use this skill for repeated acoustic-guitar strumming built on a regular or swung subdivision grid, especially eighth-note, sixteenth-note and triplet-derived accompaniment.

This is a text knowledge and decision skill. It does not require a trained model and it does not define the final guitar timbre. Timbre, layering and production belong in `materials_v2/`.

## Density is a choice, not acoustic-guitar identity

Do **not** equate realistic acoustic strumming with deliberate gaps.

Keep these independent:

```text
hand-motion continuity
!=
audible attack density
!=
note sustain / ringing continuity
```

A convincing part may be:

```text
dense-continuous
-> nearly every eighth or sixteenth hand position creates some audible contact

selective-flow
-> the hand keeps moving while several positions become air strokes

breathing / sparse
-> larger intentional holes are part of the arrangement
```

All three are valid. Do not make `breathing / sparse` the default merely because air strokes are available.

For generic `continuous_strumming` with no explicit request for space, prefer an actually continuous audible pulse and create contrast through stroke width, register, dynamics, muting, ghost contact, single-string restrikes and sustain before inserting repeated silence.

Avoid the accidental house pattern:

```text
strum strum -> pause -> strum strum -> pause
```

unless that periodic gap is deliberately chosen for the current song.

## Source evidence

### Study 1: dense steel-string subdivision pulse

The first studied MIDI sample should **not** be treated as proof of a continuous-eighth pattern.

Directly observed in its main steel-string guitar track:

- GM program 25 was used for the main dense acoustic-guitar track;
- 2743 note events formed 921 exact onset groups;
- compact chord groups were common, with a median of about three notes per onset;
- the most common adjacent attack gaps were 0.25 and 0.50 quarter-note beats, so both sixteenth- and eighth-spaced attacks were present;
- notes inside the same chord group began on exactly the same MIDI tick;
- therefore the MIDI preserved attack timing, pitch, velocity, duration and overlap, but did not preserve string-by-string sweep order.

This sample supports the idea of a dense subdivision-based chord pulse. It does not justify inferring down/up direction, sweep timing, or an eighth-note-only technique.

### Study 2: warm flowing sixteenth-grid pop strum

A second user-provided MIDI study added a different acoustic-strumming behavior family.

Directly observed in its main acoustic-guitar track:

- GM program 24 was used;
- 2048 note events formed 684 exact onset groups;
- onset groups contained 1-5 notes, with a median of 3;
- 0.25- and 0.50-quarter-note-beat attack gaps dominated;
- most full 4/4 bars contained about 11-12 audible attacks on a sixteenth-note grid rather than sounding all 16 positions;
- quarter/eighth anchor positions were somewhat broader on average than inner-sixteenth connective attacks;
- common note durations were 0.25 and 0.50 quarter-note beats, with a median duration of 0.50 beat;
- adjacent attacks frequently retained only part of the previous pitch set instead of repeating an identical block chord;
- velocity was almost fixed at 100, so this sample was **not** treated as reliable evidence for expressive dynamic shaping;
- notes inside an onset group were simultaneous, so physical down/up direction and string sweep timing remained unknown.

This sample supports several reusable ideas:

- one sixteenth-note hand-clock family can produce a flowing part with deliberate silent slots;
- accompaniment density and chord width are separate controls;
- inner-sixteenth connective attacks can be narrower than structural anchors;
- repeated strumming can preserve common tones while changing the sounded subset;
- one recurring pattern family can remain stable over many bars without making every bar identical.

Its deliberate holes belong to that Material family. They are not a universal rule for acoustic guitar.

The exact source rhythm mask, pitches and harmonic sequence belong to the source library and must not be copied into this Skill.

### Study 3: rolling triplet / shuffle strum with recoverable sweep direction

A third user-provided MIDI study added a triplet-derived strumming family and, unlike the first two studies, preserved enough within-stroke timing to recover physical sweep direction.

Directly observed in the main steel-string guitar channel:

- the MIDI encoded 125 BPM at 192 ticks per beat;
- GM program 25 was used;
- 3074 note-ons were present;
- grouping adjacent note-ons within 12 ticks produced about 1015 strum groups with a median width of three notes;
- attack groups aligned overwhelmingly to two triplet locations within each beat: the beat start and the late-triplet position about 2/3 of a beat later;
- there was essentially no comparable middle-triplet attack family;
- beat-start groups with recoverable direction strongly moved low-to-high;
- late-triplet groups with recoverable direction were almost entirely high-to-low;
- within-stroke onset spread had a median around 20 ms and a 90th percentile around 47.5 ms;
- note duration had a median around 0.78 quarter-note beats;
- velocity varied meaningfully in the source, with a median around 86 and a broad range rather than one fixed export value.

This sample supports several reusable ideas:

- acoustic strumming may use a triplet or shuffle lattice rather than a straight eighth/sixteenth grid;
- a common rolling relationship is long-short spacing: about 2/3 beat from anchor to return, then about 1/3 beat to the next anchor;
- beat anchors can be broad low-to-high downstrokes;
- late-triplet returns can be substantial high-to-low upstrokes rather than tiny decorative flicks;
- explicit string-by-string spread is valid when the source actually preserves directional within-stroke timing;
- ringing duration can extend through the next attack so the groove rolls instead of becoming clipped.

The exact source harmony, pitches, arrangement and full MIDI rhythm sequence remain in the source library. Only the reusable triplet-strumming behavior is promoted here.

## General performance knowledge

The following rules are performance conventions, not facts recovered from every studied MIDI sample:

- choose a subdivision grid appropriate to the part; it may be straight eighths, straight sixteenths, triplet-derived or swung;
- continuous right-hand motion normally follows a stable physical clock appropriate to that subdivision;
- a grid position may produce a full stroke, partial stroke, ghost/muted contact, single-string restrike, or an air stroke depending on the selected density mode;
- air strokes are optional performance vocabulary, not a realism requirement;
- downstrokes often cover more low and middle strings and may carry stronger structural accents;
- upstrokes are often narrower and lighter, but some groove families intentionally use substantial upstroke returns;
- chord changes do not automatically reset right-hand direction;
- compatible strings or voices may continue ringing through later attacks;
- do not straighten a swing/triplet groove into equal eighths unless that is an intentional style change.

## Core representation

Treat strumming as three separate layers.

### 1. Hand-motion / subdivision clock

For eighth notes in 4/4:

```text
1 & 2 & 3 & 4 &
D U D U D U D U
```

For sixteenth notes in 4/4:

```text
1 e & a 2 e & a 3 e & a 4 e & a
D U D U D U D U D U D U D U D U
```

For a rolling triplet-derived pattern family:

```text
1 trip let  2 trip let  3 trip let  4 trip let
D   .   U   D   .   U   D   .   U   D   .   U
```

The triplet example is one useful pattern family, not a universal law for every triplet groove. The middle slot may be silent while the hand resets or travels.

The audible pattern may equal the physical clock or may be a subset of it. Do not restart the direction cycle merely because the bar, chord or phrase changed.

For flowing sixteenth-grid accompaniment, choose audible density from the role. Some families leave several positions as air strokes; dense-continuous families may instead make weak positions audible through ghost contacts, narrow partials or single-string restrikes.

### 2. Stroke action

A sounding slot may use:

- `full_strum`
- `low_partial`
- `middle_partial`
- `high_partial`
- `light_upstroke`
- `muted_strum`
- `ghost_strum`
- `single_string_restrike`

A non-sounding slot may use:

- `air_strum`

These are semantic actions, not fixed MIDI note lists.

### 3. Sound realization

The renderer decides:

- which chord tones realize the requested string group;
- whether the source needs explicit string-by-string onset spread;
- velocity and velocity gradient;
- duration and release behavior;
- retrigger and overlap handling;
- sampler articulations or synthesis details.

Do not hard-code sample-library keyswitches into the musical phrase.

## Decision procedure

1. Choose the subdivision and swing relationship from the musical task instead of assuming straight eighth notes.
2. Choose audible-density mode independently: dense-continuous, selective-flow, or breathing/sparse.
3. Build the appropriate hand-motion or triplet pulse clock.
4. Mark each grid position as sounding contact or air/reset motion according to the selected density mode. Do not insert gaps merely to prove that the hand is moving.
5. Assign stroke width and register coverage per sounding slot.
6. Treat structural anchors and connective/return attacks as different roles; their width and weight may differ by style.
7. Preserve long-short timing in triplet/shuffle grooves instead of quantizing it to equal eighths.
8. Establish meter-aware dynamics before adding any humanization.
9. Preserve compatible ringing voices rather than cutting every chord at every attack.
10. At chord changes, release conflicting voices without resetting the groove clock.
11. When a lead or vocal needs space, thin width, reduce register collision or soften weak contacts before automatically deleting repeated attacks.
12. Keep repeated bars related. Variation should transform a recognizable pattern rather than randomize every bar.

## Dynamics

Do not use one fixed velocity recipe for every style.

Useful relationships:

- structural downstrokes are often stronger than connective attacks;
- upstrokes are often lighter than nearby downstrokes, but this is style-dependent rather than mandatory;
- a rolling triplet return may have enough weight to function as a second rhythmic anchor;
- ghost or muted contacts are substantially lower;
- section energy, accompaniment role and the target instrument source determine the absolute velocity range.

When a reference MIDI is available, its velocity distribution may guide the current project only when that distribution contains meaningful variation. A nearly fixed-velocity export is evidence about encoding, not expressive performance.

Do not promote one song's exact velocities into a universal Skill default.

## Voicing and sustain

Continuous strumming should not be repeated copies of one full block chord.

Useful contrasts include:

- broad downstroke with bass support;
- narrow upper-string upstroke;
- substantial return upstroke in triplet/shuffle styles;
- low or middle partial connective stroke;
- ghost contact;
- single-tone refresh;
- longer compatible ringing voices under thinner re-attacks.

A partial stroke should retrigger only the selected voices when the renderer allows it. Shared tones may ring across chord changes when musically compatible.

A useful flowing-pop relationship is:

```text
broader structural anchors
+
narrower connective sixteenths
+
partial common-tone retention
```

A useful rolling-triplet relationship is:

```text
low-to-high anchor
+
late-triplet high-to-low return
+
ringing overlap across the beat
```

Do not hard-code one source's exact chord-width sequence. Generate a related family from the current harmony and phrase role.

## MIDI realization

A fully quantized block chord can be a valid MIDI representation.

Do **not** assume that guitar realism always requires visible inter-string MIDI staggering. A sampler may contain a recorded strum inside one articulation, and some reference MIDIs intentionally quantize chord tones to the same tick.

When ordinary single-note samples or synthesis require explicit sweep motion:

- downstroke: use a small low-to-high onset spread;
- upstroke: use a small high-to-low onset spread;
- scale the spread with tempo and stroke width;
- keep it short enough that the result remains a strum rather than an arpeggio.

Reference evidence can justify recoverable direction when within-stroke note timing trends consistently with pitch order. When source notes are simultaneous, label direction and sweep timing as unknown unless another source supplies them.

Do not promote one source's measured sweep spread into a universal constant. Treat measured values as evidence for that source and derive practical renderer settings from tempo, width and sample behavior.

## Common failure modes

Revise the part when:

- the subdivision was guessed incorrectly from a reference;
- a triplet/shuffle pattern has been straightened into equal eighths;
- every generated acoustic part defaults to the same `strum-strum-gap` breathing cadence;
- air strokes are inserted automatically without an arrangement reason;
- dense-continuous intent is weakened by periodic silence instead of by narrower/softer contacts;
- a sixteenth grid is treated as a requirement to sound all sixteen positions with equally broad attacks;
- every attack uses the same full voicing;
- connective sixteenths are as broad and heavy as every structural anchor without a style reason;
- every upstroke is forced to be tiny even when the groove needs a substantial return;
- the right hand restarts at every bar or chord;
- up/down labels are invented from fully simultaneous MIDI blocks;
- all notes are cut mechanically at every new attack;
- accidental same-pitch overlap creates doubled notes or stuck notes;
- humanization is random rather than tied to stroke role and meter;
- visible MIDI staggering is forced even when the sampler already supplies a strum articulation;
- explicit staggering is so wide that the result becomes an arpeggio;
- the guitar continuously duplicates a foreground melody or vocal rhythm.

## Validation checklist

Before accepting a generated part, verify:

- the declared subdivision matches the intended pattern;
- the selected density mode matches the arrangement instead of a global acoustic-guitar stereotype;
- swing/triplet long-short spacing is preserved when required;
- the hand or pulse clock is internally coherent;
- sounding and silent slots are intentional;
- dense-continuous mode is not silently converted into a repeating-gap pattern;
- selective-flow or breathing mode uses holes because the role calls for them, not because every acoustic pattern is expected to breathe the same way;
- stroke width varies meaningfully;
- structural and connective/return attacks have sensible width relationships;
- dynamics form a readable meter and phrase;
- partial strokes actually use fewer voices;
- note duration creates the intended amount of connection;
- chord changes do not leave incompatible sustained tones;
- renderer-specific sweep behavior is not confused with source MIDI evidence;
- recoverable direction is only claimed when within-stroke timing supports it;
- repeated bars are related but not mechanically identical.

## Current status

This skill documents reusable acoustic-guitar strumming behavior across straight eighth, straight sixteenth and triplet-derived groove families.

The first MIDI study contributed evidence for dense chord-pulse attacks, compact chord groups, strong velocity variation and note overlap.

The second strumming study added evidence for one warm flowing sixteenth-grid accompaniment family with deliberate holes, variable 1-5-note attack width, narrower connective sixteenths, common-tone retention and stable multi-bar pattern families. Its gaps are family-specific rather than a universal acoustic-guitar default.

The third strumming study added evidence for rolling long-short triplet timing, substantial late-triplet return strokes, ringing note lengths and recoverable low-to-high / high-to-low sweep direction when the MIDI actually preserves within-stroke onset order.

The first two studies did not provide recoverable physical sweep direction. The third one did, so the Skill now distinguishes simultaneous block evidence from genuinely directional strum evidence.
