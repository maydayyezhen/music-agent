---
name: acoustic-guitar-continuous-eighth-strumming
description: Write and revise general-purpose continuous eighth-note acoustic-guitar strumming without relying on a trained model or a finished-song template.
status: active
---

# Acoustic Guitar Continuous Eighth Strumming

## Purpose

Use this skill when an acoustic guitar should provide a continuous eighth-note accompaniment pulse.

This is a text knowledge and decision skill. It does not require a trained model, feature extractor, learned fingerprint, or source-song transcription.

The target behavior is:

```text
one bar of 4/4
1 & 2 & 3 & 4 &
D U D U D U D U
```

The hand may continue through every eighth-note slot even when some slots are silent or only lightly touch part of the chord.

Do not use this skill for:

- fingerpicking;
- isolated sustained chord hits;
- sixteenth-note funk strumming;
- electric-guitar palm-muted rhythm;
- flamenco techniques;
- percussive body hits;
- complete song composition.

## Evidence boundary

### Direct observations from the first studied MIDI sample

The studied acoustic-guitar track supported these observations:

- attacks occurred on all eight eighth-note positions in the bar;
- attacks commonly used compact chord groups of about three simultaneous notes;
- the chord voices began on exactly the same MIDI tick;
- the source therefore preserved attack rhythm, pitch content, velocity, duration, and overlap;
- the source did not preserve string-by-string sweep order.

These observations support a continuous eighth-note chord-pulse technique. They do not prove downstroke or upstroke direction.

### General guitar-performance knowledge used by this skill

The following rules are performance conventions, not facts recovered from that MIDI sample:

- continuous eighth-note motion normally alternates down and up;
- downstrokes can cover more low and middle strings and can carry stronger accents;
- upstrokes are often lighter and can favor middle or high strings;
- silent positions may still contain an air stroke;
- the right hand should not restart its direction cycle at every chord or bar boundary;
- strings not struck again may continue ringing when the voicing and articulation allow it.

Keep this distinction visible when documenting a project.

## Core representation

Think in three independent layers.

### 1. Hand motion

The default physical clock is:

```text
slot:       0 1 2 3 4 5 6 7
direction:  D U D U D U D U
```

Direction continues across barlines. A missing audible attack does not remove the hand-motion slot.

### 2. Stroke action

Each slot chooses one action:

- `full_strum`: broad chord attack;
- `low_partial`: bass and lower-middle strings;
- `middle_partial`: middle-string support;
- `high_partial`: upper-string answer;
- `light_upstroke`: light upper or middle-upper response;
- `muted_strum`: short non-pitched or weakly pitched attack when supported by the renderer;
- `ghost_strum`: very soft contact;
- `air_strum`: hand passes without a sounding note;
- `single_string_restrike`: one important chord tone is refreshed.

These are action categories, not fixed MIDI note lists.

### 3. Sound realization

The renderer or compiler decides:

- which chord tones fit the requested string group;
- the small onset spread among sounded strings;
- velocity and velocity gradient;
- duration and release behavior;
- retrigger and overlap handling;
- articulation fallback when the sound library lacks a dedicated sample.

Do not place library-specific keyswitch numbers in the musical phrase.

## Default musical behavior

### Pulse

For the fully active subtype, sound all eight eighth-note positions.

This does not mean every slot should be equally loud or use the same voicing. A convincing full-pulse bar normally varies:

- chord width;
- low-versus-high register emphasis;
- accent strength;
- duration;
- attack openness.

### Downstrokes

Downstrokes usually work well for:

- bar openings;
- strong beats;
- low-string reinforcement;
- wider voicings;
- structural accents.

Do not make every downstroke a six-note maximum-velocity chord.

### Upstrokes

Upstrokes usually work well for:

- offbeat motion;
- lighter answers;
- high or middle-high partial voicings;
- short connective attacks;
- keeping the pulse alive without masking a foreground melody.

Do not make every upstroke identical or mechanically quiet.

### Accent hierarchy

Start with a meter-aware hierarchy rather than random velocity:

```text
beat 1: strongest structural anchor
beat 3: secondary anchor
beats 2 and 4: supportive attacks
upbeats: usually lighter connective motion
```

This hierarchy is a starting point. Genre, phrase direction, syncopation, and section energy may override it.

Normalize dynamics to the current section. Do not copy exact velocities from a reference MIDI.

## Voicing and string-group behavior

Continuous strumming should not be eight repetitions of one block chord.

Useful contrast:

- strong downstroke: broad voicing including a bass note;
- light upstroke: two or three upper chord tones;
- connective downstroke: low or middle partial;
- weak response: high partial or ghost contact;
- foreground-active moment: thinner voicing and reduced velocity;
- foreground rest: temporarily allow a wider chord.

Chord identity and stroke width are separate decisions.

A chord may remain harmonically unchanged while its sounded subset changes from slot to slot.

## Sustain and retrigger rules

Treat sounded strings or voices independently when the renderer supports it.

- A partial stroke should retrigger only the selected voices.
- Unselected compatible voices may continue ringing.
- Do not create overlapping duplicates of the same pitch without an intentional retrigger policy.
- At a chord change, stop or replace voices that conflict with the new harmony.
- Shared or compatible tones may continue when this sounds natural.
- A new attack does not require cutting every previous note.
- Short muting is an articulation decision, not the default for every slot.

The goal is a connected harmonic fabric rather than a row of detached piano chords.

## Chord-change behavior

A chord change affects the fretting hand and sounded pitches. It does not reset the right-hand clock.

For each boundary:

1. preserve the next expected down/up direction;
2. identify which sounding voices remain compatible;
3. release conflicting voices before or at the new attack;
4. choose a stroke width appropriate to the boundary;
5. avoid forcing every change to begin with a maximum full downstroke.

A light pickup or partial stroke can introduce a new chord before a stronger later attack.

## Interaction with a lead or vocal

When another part is foreground:

- keep the eighth-note hand motion conceptually active;
- reduce audible attack density only when the arrangement needs space;
- prefer partial high or middle strokes over repeated full chords;
- reduce velocity and chord width;
- avoid duplicating the foreground rhythm;
- allow longer ringing voices to carry harmony through busy lead passages.

When the foreground rests, the guitar may briefly become wider or more rhythmically explicit.

## Variation without copying a song

Build variation from transformations, not from a stored reference pattern.

Safe operations include:

- replace one full stroke with a partial stroke;
- thin one or two upstrokes;
- convert a sounding slot to an air stroke;
- strengthen a structural downstroke;
- refresh a single upper chord tone;
- lengthen compatible ringing voices;
- shorten one muted or transitional attack;
- alter chord width over a two-bar or four-bar phrase;
- reduce activity under a foreground phrase;
- open the voicing near a section arrival.

Preserve enough repetition that the right-hand identity remains audible.

Do not randomize every bar independently.

## MIDI realization guidance

When generating ordinary MIDI:

- represent each audible stroke with the selected chord tones;
- use a small low-to-high onset spread for downstrokes;
- use a small high-to-low onset spread for upstrokes;
- scale the spread with tempo so very fast songs do not produce slow arpeggios;
- keep main metric anchors close to the grid;
- vary velocity by meter, direction, stroke width, and phrase role;
- manage note-offs per pitch or per string-like voice;
- avoid stuck notes and same-pitch overlap;
- retain an explicit semantic action grid when air strokes matter, because MIDI cannot encode silent hand motion directly.

A fully quantized block chord is a valid simplified rendering, but it loses sweep direction and should not be described as evidence of a physical downstroke or upstroke.

## Minimal decision procedure

For every bar:

1. Establish eight alternating hand-motion slots.
2. Decide which slots sound and which remain air strokes.
3. Assign stronger structural downstrokes.
4. Choose narrower and usually lighter upstrokes.
5. Vary chord coverage rather than repeating one voicing eight times.
6. Preserve compatible ringing tones.
7. Handle the next chord without resetting hand direction.
8. Thin the guitar when a lead or vocal needs room.
9. Check that the bar belongs to a repeating phrase, not an unrelated random pattern.

## Common failure modes

Reject or revise the part when:

- every chord tone starts together on every slot with identical velocity and duration;
- every stroke uses the same full voicing;
- the right hand restarts with a downstroke at every bar or chord;
- upstrokes are absent without an intentional style reason;
- chord changes cut every ringing note mechanically;
- same-pitch notes overlap accidentally;
- humanization is random rather than meter- and action-based;
- the guitar duplicates the lead rhythm continuously;
- a source MIDI's exact pitches, velocities, form, or bar sequence are copied into the skill;
- air strokes are claimed as MIDI facts even though they were not encoded.

## Validation checklist

Before accepting a generated part, verify:

- the declared subdivision is eighth-note;
- the down/up hand sequence remains continuous across bars;
- sounding and silent slots are intentional;
- chord width varies meaningfully;
- strong and weak attacks form a readable meter;
- partial strokes actually use fewer voices;
- chord changes do not create conflicting sustained tones;
- note durations produce connection without stuck notes;
- the accompaniment leaves space for foreground material;
- repeated bars are related but not mechanically identical;
- no source-specific melody, chord progression, title, or exact velocity sequence entered the reusable skill.

## Current status

This skill currently documents one broad technique family: continuous eighth-note acoustic-guitar accompaniment.

The first MIDI study strengthened the knowledge of continuous eighth-note attack density, compact partial chord attacks, and sustained overlap. It did not provide down/up sweep evidence.

Future studies should refine this text only when they reveal reusable behavior such as:

- sparse eighth-note variants;
- different partial-stroke distributions;
- reliable sweep timing ranges;
- muted and ghost-stroke behavior;
- chord-change release strategies;
- interaction with vocals or lead instruments.

Add reusable principles and decision rules. Do not add a finished song's exact pattern.
