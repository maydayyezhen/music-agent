# GPT第1练习曲

## Status

**Completed / archived**

Final accepted version: **v7**

Final artifact name:

```text
GPT第1练习曲_v7_取消中途淡出_Muted稍增.mid
```

Working subtitle used during iteration:

```text
《从“啪一下就停”到“终于像个乐队”》
```

This project is now considered finished. Do not keep revising it during normal Material development unless the project is explicitly reopened.

## Musical snapshot

```text
Tempo: 104 BPM
Meter: 4/4
Key center: G major
Length: 40 bars / about 92 seconds
Format: structured multi-track MIDI
```

## Final form

```text
1-4   Intro
5-12  Verse
13-20 Build
21-28 Chorus
29-32 Bridge
33-40 Final Chorus
```

## Final arrangement roles

### Acoustic guitars

The acoustic family carries the arrangement more strongly in the earlier part of the piece, then shifts toward support and color after the electric guitars enter.

The main steel-string part contains upper-string accents / top notes that can become perceptually melodic without becoming a separate lead track. In the later arrangement these notes remain audible as small highlights while the electric-guitar family assumes more of the foreground energy.

### Muted Guitar

Final behavior:

- fast eighth-note pulse family rather than a fixed quarter-note pulse;
- short detached gate, roughly 0.18-0.22 beat in this project;
- lighter per-hit velocity so the faster density does not become heavy hammering;
- phrase/block gaps remain important;
- slightly left of center rather than directly centered;
- slightly stronger than v6 so the texture is still audible in the mix.

Final CC7 section levels used in this project:

```text
Build:        92
Chorus:      100
Final Chorus:102
```

These numbers are project-specific mix choices, not reusable universal targets.

### Continuous Overdrive Rhythm Bed

Final role:

- continuous distorted rhythm bed;
- repeated re-articulation with sustain-supported audible continuity;
- lower direct level than foreground guitar roles;
- spatially separated and wetter than the sustained melodic Overdrive;
- no internally added fade-to-zero at ordinary section boundaries.

Project CC7 remains stable at 72 while active.

### Sustained Overdrive Guitar

Final role:

- sparse sustained melodic/support notes;
- phrase tails and long occupancy rather than repeated rhythm attacks;
- more direct and drier than the rhythm Overdrive bed;
- no default internal CC7 fade at section transitions;
- tail behavior should primarily come from note duration and natural renderer release unless a special effect is intended.

Project CC7 remains stable at 101 while active.

### Bass and drums

Bass uses the previously learned pop-rock accompaniment logic and section-linked behavior.

Drums remain intentionally simple. This project was not used as a drum-study benchmark.

## Final mix lessons preserved from this project

### 1. Role hierarchy matters as much as note writing

When several guitar families coexist, first decide which one is:

```text
foreground
support
continuous bed
```

Do not solve every masking problem by boosting the hidden track.

### 2. A support layer can stay active without becoming foreground

Direct level, pan, ambience and arrangement density can keep a rhythm bed present while leaving room for melodic or muted guitar detail.

### 3. Density and per-hit weight must be coupled

When a muted rhythm changes from quarter-note to eighth-note activity:

```text
attack density increases
→ per-hit velocity should usually decrease
→ gate should usually shorten
```

Do not simply duplicate a heavy quarter-note hit at twice the rate.

### 4. Reference-specific rhythm is evidence, not law

The studied reference contained many one-beat Muted Guitar onset gaps. That supports one valid implementation, but it does not mean `Muted Guitar = quarter notes` universally.

Reusable identity is closer to:

```text
short articulation
+ repeated compact harmonic bite
+ phrase/block organization
+ controlled dynamic contour
```

Pulse density remains an arrangement parameter.

### 5. Ordinary section changes should not automatically fade away

The earlier experiment with internal CC7 fade-outs made transitions feel as if the arrangement suddenly lost energy.

Final rule used here:

```text
ordinary verse / chorus / bridge transitions
→ prefer role handoff
→ part stop/start
→ phrase gap
→ note-duration tail
→ density change

volume/expression fade
→ reserve mainly for intro/outro
→ or an explicitly desired dissolve / energy-drop effect
```

A fade observed in a reference source remains valid source evidence, but is not promoted as a default section-transition rule.

### 6. Accompaniment top notes can create a secondary melodic thread

A guitar accompaniment does not need a dedicated lead line for every memorable high note.

A held chord plus a later upper-string accent can create a perceptible top-note motif:

```text
harmonic bed continues
+
upper note appears briefly
=
small melodic highlight inside accompaniment
```

This can help an accompaniment remain interesting early in the arrangement and later become a subtler color after foreground electric guitars enter.

## Materials exercised in this project

The project deliberately combined the currently learned guitar/bass vocabulary, including:

```text
dry-grainy-steel-string-strum
multi-take-acoustic-stack
warm-pop-sixteenth-strum
rolling-triplet-acoustic-strum
gentle-steel-strum-picking
normal-pop-rock-bass
section-linked-pop-rock-bass
muted-pop-rock-pulse
continuous-overdrive-rhythm-bed
sustained-overdrive-guitar
role-separated-midi-guitar-mix
```

The point of the piece was not to maximize musical complexity. It served as an integration benchmark for learned Materials and iterative listening-driven correction.

## Iteration history worth remembering

```text
v1  integrate learned Materials
v2  rhythm Overdrive re-articulation density increased
v3  rhythm Overdrive moved backward in level
v4  Muted Guitar made more audible; acoustic chorus ducking tested
v5  reference-derived MIDI guitar mix hierarchy tested
v6  Muted Guitar changed from slow/heavy pulse to fast/light eighth texture
v7  Muted slightly raised; internal section fade-outs removed
```

## Completion decision

v7 was accepted after listening. The project is archived as a successful integration exercise.

Future improvements to Materials should happen in their own studies or in **GPT第2练习曲**, rather than silently changing this finished benchmark.
