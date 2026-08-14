---
id: overdriven-power-chord-pulse
name: Overdriven Power-Chord Pulse Guitar
kind: accompaniment_pattern
status: active
---

# Overdriven Power-Chord Pulse Guitar

## Identity

A basic open overdriven rhythm-guitar role built from repeated power-chord dyads on a stable pulse. It is broader and more exposed than a muted rhythm layer, but still functions as accompaniment rather than lead guitar.

Useful tags:

```text
overdriven-guitar
power-chord
pop-rock
rhythm-guitar
steady-pulse
strong-soft-alternation
short-gate
section-lift
```

This is a distinct role from muted rhythm guitar and from melodic/lead overdrive guitar.

## Core behavior

Use a stable repeated pulse with compact power-chord shapes:

```text
STRONG  soft  STRONG  soft
X       x     X       x
```

The pulse may continue for many beats without changing rhythm. Harmony changes underneath while the attack identity remains stable.

Do not invent a new rhythm every bar merely because the guitar is distorted.

## Chord shape

Prefer two-note root/fifth power shapes for the basic family.

A three-note root/fifth/octave shape can appear occasionally for a stronger arrival, but the default should remain compact.

The main abstraction is:

```text
power dyad
+
repeated pulse
+
accent hierarchy
```

not a full triad played like piano chords.

## Accent hierarchy

A useful four-beat relationship is:

```text
beat 1  stronger / longer
beat 2  lighter / shorter
beat 3  stronger / longer
beat 4  lighter / shorter
```

This gives the rhythm internal motion even when pitch and onset spacing are highly repetitive.

Use meter-aware repetition before random humanization.

## Gate and articulation

Open overdrive rhythm does not need to sustain continuously to the next attack.

The studied source used a one-beat pulse while many notes occupied only roughly 0.25-0.50 beat, leaving attack definition and air between hits.

Useful relationship:

```text
strong pulse attack
→ somewhat longer gate

lighter connective pulse
→ somewhat shorter gate
```

Do not make every repeated power chord a full-beat slab unless the section specifically wants sustained guitar walls.

## Repetition and harmony

Repeated attacks on the same power shape are desirable.

A typical harmonic region may keep one dyad for several consecutive pulse attacks before moving to the next chord.

Change harmony when the song changes harmony, not simply to create guitar activity.

## Section role

This material is useful for:

- chorus lift;
- stronger intro or post-chorus rhythm;
- open rock accompaniment after a muted verse;
- doubling the main groove with a broad midrange attack layer.

A common arrangement contrast is:

```text
muted-pop-rock-pulse
→ restrained motion

overdriven-power-chord-pulse
→ open section lift
```

The contrast comes from articulation and spectral openness as much as from velocity.

## Failure modes

Revise when:

- full major/minor triads replace compact power shapes by default;
- every hit has identical gate and velocity;
- repeated chords sustain so long that the pulse disappears;
- the rhythm changes randomly from bar to bar;
- the part is confused with a melodic lead-guitar phrase;
- the only difference from muted guitar is MIDI program number.

## Study provenance

This material was abstracted from a user-provided pop-rock MIDI with a dedicated GM program 29 Overdriven Guitar rhythm track.

Observed in the studied rhythm track:

- 766 note attacks formed 388 exact onset groups;
- 374 of 388 groups were two-note dyads;
- those two-note groups were overwhelmingly separated by seven semitones, supporting a root/fifth power-chord interpretation;
- 384 adjacent onset gaps were exactly one beat on the MIDI pulse grid;
- the repeated pulse was therefore far more stable than varied;
- strong pulse positions were commonly louder and longer, while alternating positions were commonly softer and shorter;
- median note duration was about 0.38 beat, with stronger positions often near 0.5 beat and lighter positions near 0.3 beat;
- the rhythm remained in a narrow low/mid guitar register and repeated the same dyad across extended harmonic regions.

These observations support a reusable overdriven power-chord pulse family. The source's exact pitches, chord progression, complete attack sequence and section order are intentionally omitted.
