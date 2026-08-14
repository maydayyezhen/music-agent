from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


TAU_MS = 10
MAX_SHIFT_MS = 1000
MAX_DURATION_MS = 2000


class PMTError(ValueError):
    """Raised when a PMT stream or note cannot be represented safely."""


@dataclass(frozen=True)
class PMTNote:
    """One decoded performance note in absolute milliseconds."""

    track: int
    program: int
    pitch: int
    onset_ms: int
    duration_ms: int
    velocity: int

    def __post_init__(self) -> None:
        if not 0 <= self.track <= 15:
            raise PMTError(f"track must be in 0..15, got {self.track}")
        if not 0 <= self.program <= 128:
            raise PMTError(f"program must be in 0..128, got {self.program}")
        if not 0 <= self.pitch <= 127:
            raise PMTError(f"pitch must be in 0..127, got {self.pitch}")
        if self.onset_ms < 0:
            raise PMTError(f"onset_ms must be non-negative, got {self.onset_ms}")
        if self.duration_ms <= 0:
            raise PMTError(f"duration_ms must be positive, got {self.duration_ms}")
        if not 0 <= self.velocity <= 127:
            raise PMTError(f"velocity must be in 0..127, got {self.velocity}")


def _quantize_ms(value: int | float) -> int:
    return max(TAU_MS, int(round(float(value) / TAU_MS)) * TAU_MS)


def _parse_index(token: str, family: str, upper: int) -> int:
    prefix = f"{family}_"
    if not token.startswith(prefix):
        raise PMTError(f"expected {family} token, got {token!r}")
    try:
        value = int(token[len(prefix):])
    except ValueError as exc:
        raise PMTError(f"invalid {family} token: {token!r}") from exc
    if not 0 <= value <= upper:
        raise PMTError(f"{family} index must be in 0..{upper}, got {value}")
    return value


def _duration_tokens(duration_ms: int | float, *, tile_long_durations: bool) -> list[str]:
    """Encode duration using paper tokens, optionally tiled for notes over 2 s.

    Paper PMT allows one ``DURP`` token. The Agent extension repeats ``DURP_199``
    and ends with a remainder token, keeping a finite vocabulary while avoiding
    destructive truncation of held notes.
    """

    remaining = _quantize_ms(duration_ms)
    if not tile_long_durations:
        remaining = min(MAX_DURATION_MS, remaining)

    result: list[str] = []
    while remaining > MAX_DURATION_MS:
        result.append("DURP_199")
        remaining -= MAX_DURATION_MS
    result.append(f"DURP_{remaining // TAU_MS - 1}")
    return result


def encode_notes(
    notes: Iterable[PMTNote],
    *,
    tile_long_durations: bool = True,
) -> list[str]:
    """Encode notes using performance-timed PMT plus the optional duration tile.

    Notes are serialized deterministically by ``(onset, track, pitch)``.
    A true zero-millisecond onset gap emits no ``TSHIFT`` token.
    """

    ordered = sorted(
        list(notes),
        key=lambda note: (note.onset_ms, note.track, note.pitch),
    )
    tokens = ["<BOS>"]
    previous_onset_ms = 0
    active_track: int | None = None
    active_program: int | None = None

    for note in ordered:
        onset_ms = max(0, int(round(note.onset_ms / TAU_MS)) * TAU_MS)
        gap_ms = onset_ms - previous_onset_ms
        if gap_ms < 0:
            raise PMTError("notes must not move backwards after sorting")

        while gap_ms >= MAX_SHIFT_MS:
            tokens.append("TSHIFT_99")
            gap_ms -= MAX_SHIFT_MS
        if gap_ms > 0:
            tokens.append(f"TSHIFT_{gap_ms // TAU_MS - 1}")

        if note.track != active_track or note.program != active_program:
            tokens.extend((f"TRACK_{note.track}", f"PROG_{note.program}"))
            active_track = note.track
            active_program = note.program

        velocity_bin = max(0, min(31, note.velocity // 4))
        tokens.append(f"PITCH_{note.pitch}")
        tokens.extend(
            _duration_tokens(
                note.duration_ms,
                tile_long_durations=tile_long_durations,
            )
        )
        tokens.append(f"VEL_{velocity_bin}")
        previous_onset_ms = onset_ms

    tokens.append("<EOS>")
    return tokens


def decode_tokens(stream: Sequence[str] | str) -> list[PMTNote]:
    """Decode strict performance-timed PMT into absolute-millisecond notes.

    One or more consecutive ``DURP`` tokens are accepted. Multiple tokens are
    the Music Agent long-duration extension; a paper-compatible stream still
    uses exactly one.
    """

    tokens = stream.split() if isinstance(stream, str) else list(stream)
    if len(tokens) < 2 or tokens[0] != "<BOS>" or tokens[-1] != "<EOS>":
        raise PMTError("PMT stream must start with <BOS> and end with <EOS>")

    notes: list[PMTNote] = []
    current_time_ms = 0
    active_track: int | None = None
    active_program: int | None = None
    index = 1

    while index < len(tokens) - 1:
        token = tokens[index]
        if token == "<BAR>":
            raise PMTError("<BAR> is not valid in performance-timed PMT mode")
        if token.startswith("TSHIFT_"):
            shift = _parse_index(token, "TSHIFT", 99)
            current_time_ms += (shift + 1) * TAU_MS
            index += 1
            continue
        if token.startswith("TRACK_"):
            active_track = _parse_index(token, "TRACK", 15)
            index += 1
            continue
        if token.startswith("PROG_"):
            active_program = _parse_index(token, "PROG", 128)
            index += 1
            continue
        if token.startswith("PITCH_"):
            if active_track is None or active_program is None:
                raise PMTError("PITCH requires an active TRACK and PROG")
            pitch = _parse_index(token, "PITCH", 127)
            cursor = index + 1
            duration_ms = 0
            while cursor < len(tokens) - 1 and tokens[cursor].startswith("DURP_"):
                duration_bin = _parse_index(tokens[cursor], "DURP", 199)
                duration_ms += (duration_bin + 1) * TAU_MS
                cursor += 1
            if duration_ms <= 0:
                raise PMTError("PITCH must be followed by at least one DURP")
            if cursor >= len(tokens) - 1 or not tokens[cursor].startswith("VEL_"):
                raise PMTError("DURP sequence must be followed by VEL")
            velocity_bin = _parse_index(tokens[cursor], "VEL", 31)
            notes.append(
                PMTNote(
                    track=active_track,
                    program=active_program,
                    pitch=pitch,
                    onset_ms=current_time_ms,
                    duration_ms=duration_ms,
                    velocity=4 * velocity_bin + 2,
                )
            )
            index = cursor + 1
            continue
        raise PMTError(f"unexpected PMT token: {token!r}")

    return notes


def serialize_tokens(tokens: Sequence[str]) -> str:
    return " ".join(tokens) + "\n"
