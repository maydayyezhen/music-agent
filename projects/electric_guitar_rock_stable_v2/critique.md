# V1 Critique and Revision Decisions

V1 was rendered through GeneralUser GS and FluidSynth before these decisions. It lasts 219.36
seconds and all six stems are non-silent. The findings below are about the actual generated MIDI,
critic reports and rendered WAV—not only the written brief.

1. **Intro target mismatch.** The complexity critic reported `target_mismatch_minimal`: measured
   density was 21.25 events/bar with six active tracks. The orchestration is intentionally layered,
   so V2 changes the declared Intro level to `simple` rather than pretending it is minimal.
2. **First chorus second pass was too literal.** Bars 9–16 reused the same odd-bar call layout as
   bars 1–8. V2 adds separate bar-12 and bar-14 answers with D–F–A and C–A–G contours, making the
   repeat conversational while retaining the hook.
3. **Final Chorus needed audible reprise evidence beyond register.** V1 raised the hook and changed
   harmony, but most material still arrived only in odd bars. V2 adds new answering cells in bars 4,
   8 and 12; bar 14 still reserves the E6 climax and bar 16 remains the only long final D landing.
4. **Bridge handoff needed a more explicit final launch.** V1 already had Lead Guitar at zero and
   two-stage organ/string density, but its last two bars did not clearly point into the return.
   V2 adds an organ D–F–A–C pickup and strings F–A–D rise into the final-chorus downbeat.
5. **Register collisions are contextual, not physical failures.** Instrument analysis reported four
   informational median-register overlaps (lead/strings or organ/strings), but 0 errors and 0
   warnings. V2 keeps the intentional bridge overlap because organ and strings alternate onsets;
   it does not “solve” the information notice by deleting the relay.
6. **Continuity already passed.** Point/Line/Plane analysis produced 0 warnings. V2 therefore does
   not lengthen notes or add overlap to manufacture continuity; the stable Lead remains ordinary
   picked monophony.
7. **Sound-source boundary remains honest.** The local result is a GeneralUser GS rendition. V2
   changes notes and arrangement only; it does not claim Ample, a VST, keyswitches or a vocal render.

## V3 selection

The final validation pass found that the bridge's bass and rhythm-guitar pitch material repeated
the first eight-bar harmony too literally even though organ and strings already intensified. V3
keeps the validated groove but changes bridge bars 9–16 to Gm–Bb–F–C–Dm–Bb–A–Dm. This gives the
bass/rhythm layer a distinct harmonic journey under the denser upper relay and makes the final Dm
arrival an earned launch point. V1 and V2 remain preserved.
