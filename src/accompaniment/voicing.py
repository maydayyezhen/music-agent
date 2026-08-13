from __future__ import annotations

import itertools
from typing import Any

from src.midi.pitches import note_number


def _pitch_classes(pitches: list[str | int]) -> list[int]:
    result: list[int] = []
    for pitch in pitches:
        pc = note_number(pitch) % 12
        if pc not in result:
            result.append(pc)
    return result


def _candidates(pitches: list[str | int], low: int, high: int, voices: int) -> list[tuple[int, ...]]:
    pitch_classes = _pitch_classes(pitches)
    if not pitch_classes:
        return []
    pools = [[midi for midi in range(low, high + 1) if midi % 12 == pc] for pc in pitch_classes]
    candidates: set[tuple[int, ...]] = set()
    # Include each chord tone, then optionally double a stable tone until the
    # requested voice count is met. Sorting preserves inner-voice order.
    for choice in itertools.product(*pools):
        base = sorted(choice)
        if len(set(base)) != len(base):
            continue
        if voices <= len(base):
            for subset in itertools.combinations(base, voices):
                candidates.add(tuple(subset))
        else:
            extras = [midi for midi in range(low, high + 1) if midi % 12 in pitch_classes]
            for extra_choice in itertools.combinations(extras, voices - len(base)):
                candidate = tuple(sorted(base + list(extra_choice)))
                if len(set(candidate)) == voices:
                    candidates.add(candidate)
    return sorted(candidates)


def voicing_cost(
    previous: tuple[int, ...] | None,
    candidate: tuple[int, ...],
    register: tuple[int, int],
    common_tone_weight: float = 5.0,
    movement_weight: float = 1.0,
) -> float:
    """Small deterministic voicing cost: movement + leaps + register - common tones."""
    low, high = register
    center = (low + high) / 2
    register_penalty = abs(sum(candidate) / len(candidate) - center) * 0.12
    spacing_penalty = sum(max(0, 3 - (b - a)) * 1.5 + max(0, (b - a) - 12) * 0.35 for a, b in zip(candidate, candidate[1:]))
    if previous is None:
        return register_penalty + spacing_penalty
    count = min(len(previous), len(candidate))
    movements = [abs(candidate[index] - previous[index]) for index in range(count)]
    movement_cost = sum(movements)
    leap_penalty = sum(max(0, movement - 7) ** 2 * 0.4 for movement in movements)
    common_tones = len(set(previous) & set(candidate))
    return (movement_cost + leap_penalty) * movement_weight + register_penalty + spacing_penalty - common_tones * common_tone_weight


def plan_smooth_voicings(
    harmony_spans: list[dict[str, Any]],
    register: tuple[int, int] = (55, 76),
    voices: int = 3,
    common_tone_retention: float = 0.8,
    voice_leading_strength: float = 0.8,
) -> list[tuple[int, ...]]:
    previous: tuple[int, ...] | None = None
    result: list[tuple[int, ...]] = []
    common_weight = 2.0 + common_tone_retention * 6.0
    movement_weight = 0.5 + voice_leading_strength
    for span in harmony_spans:
        candidates = _candidates(span["pitches"], register[0], register[1], voices)
        if not candidates:
            raise ValueError(f"no legal voicing in register {register} for {span['pitches']}")
        chosen = min(candidates, key=lambda candidate: voicing_cost(previous, candidate, register, common_weight, movement_weight))
        result.append(chosen)
        previous = chosen
    return result


NOTE_NAMES = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")


def midi_to_note(value: int) -> str:
    return f"{NOTE_NAMES[value % 12]}{value // 12 - 1}"
