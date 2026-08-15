# Music Agent V2 Checkpoint

Updated: 2026-08-15
Branch: `agent/skills-v2-clean-slate`

## Current architecture

The repository now uses one canonical knowledge path plus a hard creative-context firewall:

```text
config/creative_context.json
skills_v2/
materials_v2/
profiles/
docs/agent_api/
projects/<active-project>/
```

Implementation, tests, scripts and original-source evidence remain available for explicit non-composition modes but are excluded from ordinary creative context.

## Creative-context isolation

Ordinary `composition` mode is deny-by-default outside its allowlist.

Allowed by default:

```text
canonical root instructions and registries
skills_v2/
materials_v2/
profiles/
docs/agent_api/
projects/<active-project>/ only
```

Excluded by default:

```text
src/
scripts/
tests/
source_library/
projects/<non-active-project>/
other docs/
```

Explicit wider modes:

```text
implementation_debug
source_study
test_maintenance
```

The former policy of opening demo/build scripts for mechanics while trying to ignore their musical constants is retired. Stable mechanics are documented under `docs/agent_api/` instead.

## Concrete pollution cleanup

The current tree removes the concrete long-form melody teaching fixtures that could leak into creative context:

```text
scripts/build_melody_skeleton_v2.py
scripts/build_long_form_phrase_demos.py
tests/test_melody_skeleton_v2.py
tests/fixtures/lead_guitar_long_form_v2/
```

Long-form tests now use synthetic neutral data instead of a reusable example tune.

## Authored-only melody execution

Canonical mode:

```text
phrase_generation_mode: long_form_authored
```

Compatibility aliases `long_form_experimental` and `long_form` route to the same authored-only executor.

The executor no longer performs hidden composition from semantic labels. Removed implicit behavior includes:

- automatic transposition because a relationship is named `sequence` or `climax`;
- automatic ending-degree changes;
- automatic final tonic/root resolution;
- automatic rising contour toward `peak_bar`;
- automatic forcing of `delayed_target`;
- automatic post-peak descent;
- automatic peak/final note relocation or lengthening;
- automatic peak/final vibrato;
- automatic peak velocity boost;
- automatic bar-line clipping used as a phrase-style rule;
- default guitar gate-cycle rewriting.

Relationship labels and `motif_operations` are descriptive metadata only.

Musical changes must now be explicit project data. Supported authored operations include concrete `transform` fields and `note_overrides`. Exact mechanics are documented in `docs/agent_api/README.md`.

## Tonality / pitch neutrality

Long-form melody no longer silently falls back to E natural minor when tonal information is missing.

A project must provide either:

```text
tonality
```

or an explicit legacy compatibility `key_root`.

`pitch_quantization` is explicit and defaults to `none` for authored long-form material.

## Validation neutrality

The long-form validator still measures phrase behavior, but aesthetic warnings are activated only when the project explicitly declares corresponding `long_form_phrase_rules`.

Examples:

```text
require_delayed_peak
require_delayed_resolution
minimum_cross_bar_notes_per_8_bars
minimum_motif_developments_per_section
maximum_strong_cadences_per_8_bars
```

Missing rule means measure only, not judge.

This prevents validator targets from feeding a single house arc back into composition.

## Existing V2 knowledge policy

- `skills_v2/` contains reusable procedures and decision rules.
- `materials_v2/` contains reusable musical vocabulary promoted from evidence or validated experiments.
- `source_library/` contains original study sources and is explicit-study only.
- `profiles/` declares sound/performance implementation capabilities.
- `projects/` contains song-specific work and is not a default knowledge library.
- `instrumentation-role-planning` remains the default planning step for multi-instrument composition.
- Genre tags remain compatibility hints only; genre must not select instruments or imply energy.

## Agent rule

For ordinary composition:

```text
user request
-> creative-context allowlist
-> active project
-> skills_v2 registry
-> instrumentation / role / section-entry plan
-> materials_v2 registry by chosen instrument + role + behavior
-> Profiles
-> docs/agent_api contract
-> execute without reading scripts/src
-> render / validate / listen
```

Do not reverse this into `genre -> Material -> instrument`.
Do not use unrelated projects, tests, fixtures or demo builders as creative memory.

## Execution boundary

A successful compile means the pipeline accepted the data. It does not prove the music sounds good.
A validator proves only declared invariants and explicit project rules.
Listening feedback remains the final musical test.
