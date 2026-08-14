from __future__ import annotations

from typing import Any

from .common import drum


def compile_phrase(phrase: dict[str, Any], beats_per_bar: int) -> list[dict[str, Any]]:
    phrase_type = phrase["phrase_type"]
    bars = int(phrase.get("bars", phrase.get("loop_bars", 8)))
    energy = float(phrase.get("energy", 0.5))
    base = int(70 + energy * 35)
    chorus = phrase_type in {"rock_chorus", "chorus_with_fill"}
    result: list[dict[str, Any]] = []
    for bar in range(bars):
        start = bar * beats_per_bar
        crash_on_downbeat = bar == 0 or (chorus and bar % 4 == 0)
        if crash_on_downbeat:
            result.append(drum("crash", start, base + 8, beats_per_bar, "right_hand", _gesture="section_crash"))
        hat_step = 0.5 if chorus else 1.0
        for step in range(round(beats_per_bar / hat_step)):
            local = step * hat_step
            if crash_on_downbeat and local == 0:
                continue
            hand = "right_hand"
            hat_name = "open_hat" if chorus and bar % 4 == 3 and step == round(beats_per_bar / hat_step) - 1 else "closed_hat"
            result.append(drum(hat_name, start + local, 58 + (step % 2 == 0) * 9 + int(energy * 9), beats_per_bar, hand, _gesture="timekeeping"))
        for beat in (1.0, 3.0):
            if beat < beats_per_bar:
                result.append(drum("snare", start + beat, base, beats_per_bar, "left_hand", _gesture="backbeat"))
        if chorus:
            kicks = [0.0, 2.0] + ([1.5, 3.5] if bar % 2 == 0 else [0.75, 2.75])
        else:
            verse_turn = bar % 4
            kicks = [0.0, 2.0]
            if verse_turn == 1:
                kicks.append(2.75)
            elif verse_turn == 2:
                kicks.append(1.5)
            elif verse_turn == 3:
                kicks.extend([0.75, 3.25])
        for local in sorted(set(kicks)):
            if local < beats_per_bar:
                result.append(drum("kick", start + local, base + (5 if local == 0 else 0), beats_per_bar, "right_foot", _gesture="groove"))
        if chorus and bar % 4 == 2:
            result.append(drum("snare", start + 2.75, 42, beats_per_bar, "left_hand", 0.08, _gesture="ghost"))
        if not chorus and bar % 2 == 1:
            result.append(drum("snare", start + 2.75, 39, beats_per_bar, "left_hand", 0.08, _gesture="ghost"))
    if phrase.get("transition_fill", chorus):
        start = (bars - 1) * beats_per_bar + max(0.0, beats_per_bar - 1.0)
        # The fill replaces hand timekeeping during its window; feet may continue.
        result = [event for event in result if not (
            event.get("_limb") in {"left_hand", "right_hand"}
            and (int(str(event["at"]).split(":", 1)[0]) - 1) * beats_per_bar
            + float(str(event["at"]).split(":", 1)[1]) - 1.0 >= start
        )]
        for index, name in enumerate(("low_tom", "mid_tom", "high_tom", "snare")):
            result.append(drum(name, start + index * 0.25, base - 7 + index * 3, beats_per_bar,
                               "left_hand" if index % 2 == 0 else "right_hand", 0.1, _gesture="transition_fill"))
    return sorted(result, key=lambda event: (event["at"], event["note"]))
