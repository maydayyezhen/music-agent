---
id: muted-pop-rock-pulse
name: Muted Pop-Rock Pulse Guitar
kind: accompaniment_pattern
status: active
---

# Muted Pop-Rock Pulse Guitar

## Identity

A muted electric-guitar rhythm family built from short repeated compact dyads. Its job is to create dry, articulated forward motion without opening into a sustained overdriven wall.

Useful tags:

```text
muted-guitar
palm-muted
pop-rock
rhythm-guitar
short-gate
repeated-pulse
crescendo-block
compact-dyad
variable-density
```

This is a distinct accompaniment role, not merely an overdrive guitar with lower velocity.

## Core behavior

Build the part from short pulse blocks:

```text
x x x x x x
          rest / reset
x x x x x x
```

The important invariant is not one fixed subdivision. Preserve:

```text
short articulated attacks
+
repetition
+
block-level dynamic shape
+
phrase-level gaps
```

Choose pulse density from tempo, section energy and the desired motion.

## Pulse-density modes

### Quarter-pulse mode

A slower, steadier family may use one compact attack per beat:

```text
1   2   3   4
X   X   X   X
```

Use this when the muted guitar should feel restrained, deliberate or heavy enough to mark the meter clearly.

Do not make quarter-pulse mode the automatic default. At moderate tempos it can become slow and hammer-like when attacks are too loud or too central.

### Eighth-pulse mode

For lighter, faster forward motion, use an eighth-note grid:

```text
1 & 2 & 3 & 4 &
x x x x x x x x
```

The denser mode should usually reduce the weight of each individual hit:

```text
pulse density up
→ per-hit velocity down
→ gate shorter
→ less low-mid impact per attack
```

The perceptual target is a dry moving texture rather than repeated heavy knocks.

The exact sounding mask does not need all eight positions. Omit selected late attacks or create a phrase gap so the block still breathes.

## Chord shape

Prefer compact two-note shapes in a narrow low-to-mid guitar register.

Useful interval families include fourth/fifth-related dyads and other compact shapes derived from the current harmony.

Do not realize every muted attack as a full six-string chord.

The role is:

```text
compact harmonic bite
+
short articulation
+
repetition
```

## Gate and articulation

Keep attacks clearly detached.

A useful relationship is:

```text
pulse interval
>
actual note gate
```

For quarter-pulse mode, the studied source commonly used nominal note lengths around roughly 0.35-0.50 beat against one-beat attack spacing.

For denser eighth-pulse adaptations, shorten the gate with the subdivision rather than reusing the same long gate. A practical starting family is roughly 0.18-0.28 quarter-note beats when the pulse interval is 0.5 beat, then tune by renderer.

Do not let muted notes ring through the whole pulse unless a specific sound source requires it.

## Weight and accent

Do not equate prominence with a large velocity on every attack.

Prefer a readable hierarchy such as:

```text
structural anchor: medium
connective eighth: lighter
phrase arrival: slightly firmer
```

When the part feels like slow heavy knocking, revise in this order:

1. increase pulse density when the arrangement wants more motion;
2. reduce per-hit velocity;
3. shorten gate;
4. move the part away from dead-center if mix space allows;
5. reduce competing accompaniment before making the muted guitar louder again.

## Dynamic blocks

A major reusable behavior is block-level crescendo.

Instead of giving every attack unrelated velocity, let a run rise progressively:

```text
soft
→ medium
→ firm
→ stronger
```

Then reset after a phrase gap or harmony/section change.

In eighth-pulse mode, keep the crescendo shallower than a slow quarter-pulse version because twice as many attacks already increase perceived energy.

The crescendo belongs to the phrase block, not to random per-note humanization.

## Phrase construction

Useful block shapes include:

- short run of repeated attacks, then a gap;
- another run at a new harmony, then a gap;
- a longer uninterrupted run as the arrangement builds;
- a denser eighth-note block for faster motion;
- a crescendo that resets when a new block begins.

Keep the rhythmic identity simple. Variation should come mainly from block length, pulse density, gaps, harmony and dynamic contour.

Do not add random syncopation merely to avoid simplicity.

## Arrangement role

This material works well when the arrangement needs guitar motion without the spectral width or sustain of open overdrive rhythm guitar.

Typical uses:

- verse drive;
- pre-chorus build;
- low-energy rock accompaniment;
- under a vocal or lead where a broad guitar layer would be too large;
- as a setup before an overdriven rhythm guitar enters;
- as a faster dry texture when a quarter-note pulse feels too slow or heavy.

When `continuous-overdrive-rhythm-bed` is also active, distinguish them by articulation and depth:

```text
muted-pop-rock-pulse
→ dry / clipped / granular motion

continuous-overdrive-rhythm-bed
→ sustained / connected / background body
```

They may share a subdivision, but should not share the same perceptual weight.

## Failure modes

Revise when:

- every hit is a full chord;
- muted attacks ring almost to the next pulse and lose their clipped character;
- the part has no phrase gaps or block structure;
- velocity is random instead of forming readable phrase contours;
- every block has a new rhythm;
- the part is treated as merely a quieter copy of overdriven rhythm guitar;
- quarter-note attacks sound slow, heavy and hammer-like in a section that needs faster motion;
- eighth-note mode keeps quarter-mode velocity and becomes an aggressive machine gun;
- the generator treats one-beat spacing from a reference MIDI as a universal rule.

## Study provenance

This material was first abstracted from a user-provided pop-rock MIDI with a dedicated GM program 28 Muted Guitar track.

Observed in that studied track:

- 440 note attacks formed 224 exact onset groups;
- 216 of 224 onset groups were two-note attacks;
- compact fourth/fifth-related dyads dominated;
- 205 adjacent onset gaps were exactly one beat in the MIDI pulse grid;
- 16 larger three-beat onset gaps created repeated phrase spaces rather than a fully continuous stream;
- median nominal note duration was about 0.41 beat, clearly shorter than the one-beat attack spacing;
- repeated blocks showed deliberate velocity ramps, including six-hit and longer crescendo sequences;
- the pitch range stayed very narrow, supporting a compact low/mid-register rhythm role.

Those measurements support the quarter-pulse realization, short articulation, compact dyads, phrase gaps and block crescendo. They do **not** prove that one-beat spacing is the only valid density for the broader reusable role.

The eighth-pulse mode is a later project adaptation motivated by listening tests in which a moderate-tempo quarter pulse sounded too slow and heavy. Treat it as a reusable controllable variation, not as a claim about the original reference MIDI.

The source's exact pitches, chord progression, full rhythmic sequence and section order are intentionally omitted.
