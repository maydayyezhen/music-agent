from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable


SUPPORTED_ACTIONS = {
    "pick",
    "hammer_on",
    "pull_off",
    "slide",
    "vibrato",
    "release",
}


class GestureIRError(ValueError):
    """Raised when instrument-specific performance intent is contradictory."""


@dataclass(frozen=True)
class GestureAction:
    """One instrument action in absolute milliseconds.

    PMT stores the resulting note performance. This sidecar stores the physical
    relationship that PMT cannot express, such as non-retriggered transitions.
    """

    action_id: str
    kind: str
    time_ms: int
    note_id: str | None = None
    pitch: int | None = None
    from_pitch: int | None = None
    to_pitch: int | None = None
    transition_ms: int | None = None
    retrigger: bool | None = None
    velocity: int | None = None
    parameters: dict[str, float] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.action_id:
            raise GestureIRError("action_id is required")
        if self.kind not in SUPPORTED_ACTIONS:
            raise GestureIRError(f"unsupported gesture action: {self.kind!r}")
        if self.time_ms < 0:
            raise GestureIRError("time_ms must be non-negative")
        for value, name in (
            (self.pitch, "pitch"),
            (self.from_pitch, "from_pitch"),
            (self.to_pitch, "to_pitch"),
        ):
            if value is not None and not 0 <= value <= 127:
                raise GestureIRError(f"{name} must be in 0..127")
        if self.velocity is not None and not 0 <= self.velocity <= 127:
            raise GestureIRError("velocity must be in 0..127")

        if self.kind == "pick":
            if self.pitch is None or self.velocity is None:
                raise GestureIRError("pick requires pitch and velocity")
            if self.retrigger is False:
                raise GestureIRError("pick is an attack and cannot disable retrigger")

        if self.kind in {"hammer_on", "pull_off", "slide"}:
            if self.from_pitch is None or self.to_pitch is None:
                raise GestureIRError(
                    f"{self.kind} requires from_pitch and to_pitch"
                )
            if self.transition_ms is None or self.transition_ms <= 0:
                raise GestureIRError(
                    f"{self.kind} requires a positive transition_ms"
                )
            if self.retrigger is not False:
                raise GestureIRError(
                    f"{self.kind} must explicitly set retrigger=False"
                )

        if self.kind == "vibrato":
            if self.pitch is None:
                raise GestureIRError("vibrato requires pitch")
            delay_ms = self.parameters.get("delay_ms")
            rate_hz = self.parameters.get("rate_hz")
            depth_cents = self.parameters.get("depth_cents")
            if delay_ms is None or delay_ms < 0:
                raise GestureIRError("vibrato requires non-negative delay_ms")
            if rate_hz is None or rate_hz <= 0:
                raise GestureIRError("vibrato requires positive rate_hz")
            if depth_cents is None or depth_cents <= 0:
                raise GestureIRError("vibrato requires positive depth_cents")

        if self.kind == "release" and self.pitch is None:
            raise GestureIRError("release requires pitch")

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "action_id": self.action_id,
            "kind": self.kind,
            "time_ms": self.time_ms,
        }
        for key in (
            "note_id",
            "pitch",
            "from_pitch",
            "to_pitch",
            "transition_ms",
            "retrigger",
            "velocity",
        ):
            value = getattr(self, key)
            if value is not None:
                result[key] = value
        if self.parameters:
            result["parameters"] = dict(self.parameters)
        return result


@dataclass(frozen=True)
class PerformanceGesture:
    gesture_id: str
    track: int
    program: int
    instrument: str
    string_index: int | None
    actions: tuple[GestureAction, ...]

    def validate(self) -> None:
        if not self.gesture_id:
            raise GestureIRError("gesture_id is required")
        if not 0 <= self.track <= 15:
            raise GestureIRError("track must be in 0..15")
        if not 0 <= self.program <= 128:
            raise GestureIRError("program must be in 0..128")
        if not self.instrument:
            raise GestureIRError("instrument is required")
        if self.string_index is not None and self.string_index < 0:
            raise GestureIRError("string_index must be non-negative")
        if not self.actions:
            raise GestureIRError("a gesture must contain at least one action")

        action_ids: set[str] = set()
        previous_time = -1
        for action in self.actions:
            action.validate()
            if action.action_id in action_ids:
                raise GestureIRError(
                    f"duplicate action_id in gesture: {action.action_id}"
                )
            if action.time_ms < previous_time:
                raise GestureIRError("gesture actions must be time-ordered")
            action_ids.add(action.action_id)
            previous_time = action.time_ms

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "gesture_id": self.gesture_id,
            "track": self.track,
            "program": self.program,
            "instrument": self.instrument,
            "actions": [action.to_dict() for action in self.actions],
        }
        if self.string_index is not None:
            result["string_index"] = self.string_index
        return result


def build_sidecar(
    gestures: Iterable[PerformanceGesture],
    *,
    source: str | None = None,
) -> dict[str, Any]:
    ordered = list(gestures)
    ids: set[str] = set()
    for gesture in ordered:
        gesture.validate()
        if gesture.gesture_id in ids:
            raise GestureIRError(
                f"duplicate gesture_id in sidecar: {gesture.gesture_id}"
            )
        ids.add(gesture.gesture_id)

    result: dict[str, Any] = {
        "schema": "music-agent-gesture-ir",
        "schema_version": 1,
        "gestures": [gesture.to_dict() for gesture in ordered],
    }
    if source is not None:
        result["source"] = source
    return result
