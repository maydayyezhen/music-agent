# V1 Critique and Revision Decisions

V1 was rendered to `output/v1.wav` before revision. The findings below come from the actual MIDI/WAV build artifacts and all four critics, not from the brief alone.

1. Long-form narrative warnings occurred in Chorus 1, Verse 2 and Final Chorus because the realized motif contains two consecutive full-rest bars at a few relationship transitions. The relationship graph is intact, but the section-specific validator target was stricter than the intended dramatic breath. V2 explicitly allows at most two consecutive rest bars while retaining zero resets, one strong cadence and cross-bar connections.
2. Final Chorus was too close to Chorus 1 in measurable construction: both peaked in bar 12, used the same open-chord omission grid, and occupied nearly the same string register. V2 moves the final lead target to E6/bar 14, adds an altered climax ending, reduces guitar omissions after the midpoint and lifts strings to MIDI 60–86.
3. The organ was classified as a melodic track because its role includes “countermelody,” and sustained semantic chord tracks in every section produced six `melody_no_breath` warnings. V2 changes Verse 1, Verse 2 and Outro organ material into a two-voice sustained plane in a lower register; it remains a line only when it actually takes over in Bridge.
4. Declared role budgets exceeded the target in seven sections (for example simple Intro 13 versus guide 8). V2 reallocates rather than adding/removing arbitrary notes: simple sections spend 8 or fewer points, standard sections 10, rich sections at most 15, and Final Chorus remains within the dense guide.
5. Both Bridge organ counterlines triggered `line_is_disconnected`. Their positive gaps were too large for a role that must carry narrative after Lead Guitar exits. V2 lengthens both the generated counterline notes and authored bridge answers while preserving distinct onsets and register rise.
6. Instrument critic reported 11 same-register observations in V1. They were informational rather than errors, but the lead/organ/strings overlap reduced hierarchy in Intro, Pre and Outro. V2 lowers the supporting organ plane in reflective sections and raises only the final strings, making the foreground assignment clearer.
7. Bridge Build was busy but did not accelerate enough between its early and late halves: the V1 rhythm-guitar omission pattern removed the same two last eighths every bar after its opening. V2 retains the sparse first two bars, then removes only one terminal step per two-bar unit, producing a quantifiable density climb into the impact.

The revision intentionally does not add more bends or random humanization. It changes phrase continuity targets, role allocation, return transformation, register hierarchy and bridge propulsion.

