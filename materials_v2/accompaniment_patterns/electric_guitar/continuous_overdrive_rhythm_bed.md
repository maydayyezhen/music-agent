---
id: continuous-overdrive-rhythm-bed
name: Continuous Overdrive Rhythm Bed
kind: accompaniment_pattern
status: active
---

# Continuous Overdrive Rhythm Bed

## Identity

A pop-rock overdriven rhythm-guitar family with repeated chord re-articulation but a continuously occupied distorted guitar bed underneath. The attack grid may be simple and repetitive while the audible guitar body remains connected across attacks.

Useful tags:

```text
overdriven-guitar
rhythm-guitar
continuous-bed
re-articulation
power-dyad
sustain-pedal
section-layer
pop-rock
```

This replaces the earlier mistaken abstraction that treated short MIDI note gates as literal audible silence between overdrive attacks.

## Core principle

Separate **attack timing** from **audible continuity**.

A useful basic shape is:

```text
attacks:
X       X       X       X

sounding bed:
━━━━━━━━━━━━━━━━━━━━━━━━━━
```

The guitar may re-articulate once per beat while the distorted body continues ringing underneath.

Do not translate a short notated MIDI gate directly into:

```text
啪___  啪___  啪___  啪___
```

when sustain, overlap, release behavior, or controller state keeps the sound alive.

## Attack structure

A stable quarter-note re-articulation is a useful starting family:

```text
1       2       3       4
X       X       X       X
```

Compact root/fifth dyads are a strong default for pop-rock rhythm support. Repeating the same dyad for several attacks is desirable when harmony is stable.

The attack pattern does not need rhythmic novelty every bar. The role gains mass from continuity and arrangement placement rather than constant syncopation.

## Audible continuity

The central requirement is that the guitar body should remain present between attacks.

Possible realizations include:

- MIDI CC64 sustain when the target sound source responds musically;
- overlapping note releases;
- longer sampler or amp-envelope release;
- renderer-specific sustain/release controls;
- audio-level sustain or amp behavior after rendering.

The implementation may differ, but the perceptual result should be:

```text
new pick attack
+
existing distorted tail
→ connected guitar wall
```

rather than a sequence of isolated stabs.

## Nominal gate versus effective sounding duration

Always distinguish:

```text
notated note gate
!=
effective sounding duration
```

A source MIDI may contain note-offs well before the next attack while sustain controller state keeps released notes sounding. Therefore note-duration statistics alone are insufficient for articulation inference.

When studying or generating this role, inspect:

- note-on spacing;
- note-off timing;
- CC64 sustain state;
- retrigger overlap;
- release-tail behavior of the renderer;
- section-level sounding occupancy.

## Accent hierarchy

Repeated attacks may still have meter-aware accents, for example stronger odd beats and lighter connective beats. However, accent differences should sit on top of a continuous bed.

Do not create accent contrast by cutting the weak beats into dead air unless the arrangement intentionally wants staccato rhythm guitar.

## Section role

This role is usually a **section layer**, not a decorative one-shot.

Useful behavior:

```text
section enters
→ continuous overdrive rhythm bed turns on
→ stable re-articulation continues through the section
→ section ends
→ the whole layer drops out or releases
```

Use it to make an open or heavy section feel physically larger. Do not automatically add it to every chorus merely because the song is rock-adjacent.

## Relationship to bass and drums

High attack alignment with bass is allowed when the whole rhythm section shares the same pulse.

A useful relationship is:

```text
continuous overdrive attacks
↕
full bass pulse
↕
kick / backbeat framework
```

The overdrive guitar contributes sustained midrange mass, while bass and drums define low-frequency weight and impact.

## Contrast with muted guitar

Keep the distinction explicit:

```text
muted-pop-rock-pulse
→ genuinely clipped
→ short audible occupancy
→ intentional air between attacks

continuous-overdrive-rhythm-bed
→ repeated attacks
→ continuous audible occupancy
→ distortion body remains present
```

The two roles can therefore create a strong section transition without relying only on velocity.

## Contrast with sustained melodic overdrive

`continuous-overdrive-rhythm-bed` is rhythm-section material. Its identity comes from repeated re-articulation plus continuous body.

`sustained-overdrive-guitar` is a separate melodic/support gesture. Its identity comes from sparse one-to-several-beat notes, phrase shapes, tails, dyads and occasional pedal tones.

Do not merge them into one generic "Overdrive Guitar" behavior.

## Failure modes

Revise when:

- the generator infers audible gaps from MIDI note-off timing without checking sustain state;
- every beat becomes an isolated short stab;
- the guitar sounds like piano-style block chords with silence between attacks;
- sustain is held blindly across harmonic changes and creates clashes;
- the role is sprinkled as random decoration instead of treated as a section layer;
- the generator confuses this role with genuinely muted rhythm guitar;
- the generator confuses this role with sparse melodic sustained overdrive.

## Study provenance

This material was abstracted from the dedicated short-note GM program 29 Overdriven Guitar rhythm track in a user-provided pop-rock MIDI.

Observed in the studied source track:

- 766 note attacks formed 388 exact onset groups;
- 374 of 388 onset groups were two-note dyads;
- the dyads were overwhelmingly fifth-related compact power shapes;
- 384 adjacent onset-group gaps were exactly one beat, showing extremely stable re-articulation;
- the nominal MIDI note duration had a median around 0.38 beat;
- crucially, the same track contained 96 CC64 sustain events forming 48 pedal-down blocks;
- every observed pedal-down block lasted about 7.99 beats, approximately two 4/4 bars;
- therefore the short note gates did **not** imply repeated audible silence between attacks;
- the source behavior is better understood as repeated pick attacks over a sustained, connected overdrive bed.

These observations support a reusable continuous overdrive rhythm family. The source's exact pitches, harmony, section order, controller event sequence and complete rhythm are intentionally omitted.
