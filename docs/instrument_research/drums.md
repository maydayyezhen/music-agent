# Drum Kit

## Band responsibility

- Establish pulse, backbeat/subdivision and sectional energy.
- Signal transitions with fills, crashes, openings and temporary subtraction.
- Converse with bass and riffs while preserving a coherent groove hierarchy.

## Physical model

- Default kit uses two hands and two feet. A simultaneous onset must be assignable to
  available limbs: kick foot, hi-hat foot, and two hand voices.
- Closed/open hat, ride, crash, snare and toms normally consume hand capacity. A single
  hand cannot strike two ordinary surfaces at exactly the same instant.
- Hi-hat openness is a state; open hat should close intentionally before/at a closed hit.
- Rolls/flams are gesture types, not stacks of duplicate notes at one tick.

## Phrase vocabulary by section

- Verse: restrained backbeat, lower hat density, sparse kick variation and ghost notes.
- Chorus: stronger backbeat, denser hat/ride, crash at structural entry, extra kick.
- Bridge: half-time, tom ostinato, ride-bell shift, subtraction or displaced backbeat.
- Fill: one- or two-beat hand path through snare/toms, optionally supported by kick,
  ending at a section boundary rather than every bar.

## Interaction

- Kick shares selected structural accents with bass and rhythm guitar.
- Snare defines backbeat and may answer melodic syncopation with restrained ghosts.
- Cymbal changes should correspond to arrangement energy, not random decoration.

## MIDI expression

- Drum hits remain GM-compatible semantic drum names until a profile maps note numbers.
- Velocity derives from limb/accent role: backbeat, ghost, hat pattern and fill contour
  have distinct ranges.
- Flam/drag/roll store gesture parameters and compile to ordered hits. Timing deviation is
  correlated within a groove and keeps structural anchors stable.

## Piano-roll anti-patterns

- Three cymbals, snare and two toms strike simultaneously with one kick.
- Every hat hit has identical velocity; every section uses the same groove.
- Fills are random drum names without a hand path or landing crash.
- Crash occurs on every bar; ghost notes are as loud as backbeats.

## Code-convertible rules

- Classify kit pieces by limb and run simultaneous-onset allocation.
- Detect mutually exclusive hat states and excessive same-limb collisions.
- Generate groove from kick/snare/hat roles, then add bounded ghost/fill gestures.
- Measure section groove signatures, transition coverage and repeated-bar identity.
- Tie deterministic variation to bar role (opening, middle, turnaround, fill).

## Preferences, not hard laws

- Double-kick pedals, open-handed playing, auxiliary percussion and advanced sticking can
  expand limb capacity. Profiles/phrases must declare these capabilities.
- Perfect quantisation can be stylistically correct; humanization is optional intent.

