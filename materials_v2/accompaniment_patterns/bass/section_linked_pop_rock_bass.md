---
id: section-linked-pop-rock-bass
name: Section-Linked Pop-Rock Bass
kind: accompaniment_pattern
status: active
---

# Section-Linked Pop-Rock Bass

## Identity

A pop-rock bass family whose groove changes together with the current rhythm-section role. Instead of treating bass as one fixed pattern across the whole song, let the low end switch behavior when the arrangement moves between restrained muted-guitar sections and more open, stronger sections.

Useful tags:

```text
pop-rock
section-linked
rhythm-section
guitar-linked
muted-section
open-section
root-pulse
low-variation
phrase-fill
```

This is not a replacement for `normal-pop-rock-bass`. Use `normal-pop-rock-bass` when the bass should broadly inherit a main accompaniment groove. Use this card when the arrangement contains clearly different section roles and the bass should change with them.

## Core principle

Treat bass, rhythm guitar and drums as one groove system.

A useful arrangement relationship is:

```text
muted rhythm guitar
→ bass becomes sparser and leaves more internal space

open / stronger rhythm section
→ bass opens into a fuller repeated pulse
```

Do not express a section change only by increasing bass velocity. Change the rhythmic behavior when the surrounding rhythm section changes.

## Muted-section behavior

When the main electric-guitar role is short and muted, a useful bass pattern is a sparse four-beat frame such as:

```text
1   2   3   4
X   X   .   X
```

The second attack may ring significantly longer so the missing third-beat attack feels intentional rather than empty.

A useful articulation relationship is:

```text
beat 1: medium-short anchor
beat 2: longer sustain
beat 3: no new attack
beat 4: medium-short pickup / return
```

This produces motion without competing with a clipped muted-guitar layer.

Do not force this exact mask into every muted section. Preserve the larger principle: fewer bass attacks, intentional sustain, and strong agreement with the muted rhythm-guitar pulse.

## Open-section behavior

When the arrangement opens into a stronger section, the bass may switch to a full quarter-note pulse:

```text
1   2   3   4
X   X   X   X
```

Keep pitch movement restrained. Repeated root or harmonic-anchor notes are useful because the section lift comes primarily from rhythmic fullness and the wider arrangement, not from a suddenly busy bass line.

A meter-aware accent hierarchy can keep repeated notes alive:

```text
beat 1: strong
beat 2: lighter
beat 3: strongest or equally strong
beat 4: medium-strong
```

The exact velocity values should come from the current project and sound source, not from one reference MIDI.

## Two-bar color-note variation

A useful low-cost variation is:

```text
bar A:
root  root  root   root

bar B:
root  root  color  root
```

The color note may be a nearby chord tone or scale tone that briefly lifts the line on beat 3 before returning home.

This gives the bass a small melodic identity without turning it into a walking or riff-heavy part.

Use this sparingly and keep the anchor recognizable.

## Relationship to rhythm guitar

This material intentionally allows very high attack alignment between bass and the active rhythm-guitar layer when that layer defines the section pulse.

Think in roles:

```text
muted guitar block
↔ sparse bass pulse

open rhythm-section pulse
↔ full bass pulse
```

The bass does not need to duplicate guitar pitches. It shares attack structure and section energy while remaining in its own register and harmonic role.

A sustained melodic guitar layer such as `sustained-overdrive-guitar` may sit above this rhythm section without controlling every bass attack.

## Relationship to drums

Bass may reinforce important kick attacks, but kick is not the only controller.

Use the whole rhythm section:

```text
rhythm-guitar role
+
kick/backbeat structure
+
section energy
→ bass pattern choice
```

This prevents the bass from becoming a literal copy of the kick while still allowing the low end to lock tightly with the band.

## Phrase development

Keep early repetitions simple. Add extra movement later rather than filling every bar from the beginning.

Useful later-stage changes include:

- one eighth-note pickup near beat 4;
- one short approach into the next harmonic anchor;
- a compact phrase-end descent or ascent;
- one extra attack in a later chorus;
- returning immediately to the stable section pattern after the fill.

The order matters:

```text
establish groove
→ repeat
→ change section role
→ repeat
→ introduce a small late fill
```

## Failure modes

Revise when:

- the bass uses the same rhythm through restrained and open sections;
- section lift is created only by higher velocity;
- the muted section fills every beat and loses internal space;
- the open section becomes melodically busy when a repeated pulse would support the arrangement better;
- every two-bar unit contains a fill;
- color notes stop returning to the harmonic anchor;
- the bass copies every kick mechanically while ignoring the rhythm-guitar role;
- fills appear before the basic groove identity has been established.

## Pairing

This material pairs naturally with:

- `muted-pop-rock-pulse` for restrained sections;
- a fuller drum/accompaniment groove for open sections;
- `sustained-overdrive-guitar` as a separate long-note electric layer above the bass groove when the arrangement needs more electric-guitar body without another short pulse pattern.

A useful basic transformation is:

```text
Verse:
muted-pop-rock-pulse
+
section-linked-pop-rock-bass sparse mode

Stronger section:
fuller rhythm section
+
section-linked-pop-rock-bass full-pulse mode
+
optional sustained-overdrive-guitar above it
```

## Study provenance

This material was abstracted from the bass track of a user-provided pop-rock MIDI that also contained dedicated muted and overdriven guitar tracks.

Observed in the studied bass track:

- GM program 33, Electric Bass (finger), was used;
- 745 bass note attacks were present;
- the pitch range was narrow, spanning only six distinct MIDI pitches across the studied track;
- across the whole file, the two dominant full-bar attack masks were a four-hit quarter-note pulse and a three-hit `1, 2, 4` pattern;
- 78 bars used the `1, 2, 4` bass pattern, while 96 bars used the full `1, 2, 3, 4` quarter-note pulse;
- among bars where the dedicated muted-guitar track was active, 62 of 64 bass bars used the `1, 2, 4` pattern, and about 91.8% of bass attacks aligned exactly with muted-guitar attacks;
- in those three-hit bars, median bass note durations were about 0.73 beat on beat 1, 1.55 beats on beat 2, and 0.71 beat on beat 4, supporting an intentional sustained middle space;
- among bars where the source's dedicated short overdriven rhythm-guitar track was active, 84 of 100 bass bars used the full four-hit quarter-note pulse, and about 96.9% of bass attacks aligned exactly with that source track;
- in common four-hit bars, median velocity by beat showed a clear meter-aware hierarchy, with beat 2 lighter than beats 1, 3 and 4;
- 51 of the common four-hit bars repeated one pitch on all four beats, while 38 used a `root, root, color, root` shape; 36 consecutive two-bar pairs specifically used a stable-root bar followed by a third-beat color-note bar;
- later parts of the source added occasional extra pickups and fills after the basic groove had already been strongly established.

The short overdriven rhythm-guitar source remains useful as evidence for this bass relationship, but its previously promoted standalone guitar Material has been removed. The source's exact pitches, chord progression, section order and complete rhythmic sequence are intentionally omitted.
