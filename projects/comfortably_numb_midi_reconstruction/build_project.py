from __future__ import annotations

import base64
import json
import struct
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TPB = 480
TEMPO_US_PER_BEAT = 923076
LEAD_B85 = 'c-m!<K~4iP3`L!pO6^f*iP)e~(kM!)fC>#>vP5bZJwlcoB}ZV<1I!UPLXMClV1H5u#OBFL?C<}*-p~-41{(I@L1@avs}D+nDN&l3DpfGaZ!+b;-3_tSOj(#IKPfN53pvqoRAsiBb6|6(<YlU#Jv6Oq{@X}-g3dy0dH<uI_h3*SMe{^%`zX7P7PZwnZ_zX2CCG~@J6^p}j>~NI>dHm+>B5iOYhI6xp1aTX>pW<ex^+fOMf68Dg(_b7RxdN$X|6UkDf7#(jL+bAx(9HF)E+txH@AAjV!3-I=N1oj<n=~x+t1B;^QnaMdvYVLVXxQ7{XFs)U5SDN'
RHYTHM_B85 = 'c-rk)Q3``F3~kOchBAaAY7xCakI^IKxIKbLm_7#!Oggq%om+n%lBCZhO$<>fHC(J3u>=}mXVst>a)z8C=TXi{{+^uNBqvt_4Y0H1cJp(sdtZ&`jI)JcYk)1-pyfiGg_c`zex>#YBRa^p;vjyKpR!H90OHHw8(?e6N35USDl^0LoDD6q(SN8VpNmXtU@bD4i+FK%s71WF@Ofsgh0j6lA(>C$K|XJtqD80l;D^nV8%Z|X*hJH&zDOMx+vcxhf1I=CUQsV=tKf{Tf>XHKefpEju=UJ)kQRGTKkY#a-DiT`XM){lf_=Rf^M<v(>ATWDf%x((=re^e'
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def unpack(blob: str) -> list[tuple[int, int, int, int]]:
    raw = zlib.decompress(base64.b85decode(blob.encode()))
    if len(raw) % 6:
        raise ValueError("embedded MIDI table is corrupt")
    return [
        struct.unpack(">HHBB", raw[offset:offset + 6])
        for offset in range(0, len(raw), 6)
    ]


def note_name(value: int) -> str:
    return f"{NAMES[value % 12]}{value // 12 - 1}"


def number_text(value: float) -> str:
    return f"{value:.6f}".rstrip("0").rstrip(".")


def decode(blob: str) -> list[dict[str, object]]:
    start_tick = 0
    events: list[dict[str, object]] = []
    for delta_tick, duration_tick, pitch, velocity in unpack(blob):
        start_tick += delta_tick
        total_beats = start_tick / TPB
        bar = int(total_beats // 4) + 1
        beat = total_beats % 4 + 1
        events.append({
            "type": "note",
            "pitch": note_name(pitch),
            "at": f"{bar}:{number_text(beat)}",
            "duration": float(number_text(duration_tick / TPB)),
            "velocity": velocity,
        })
    return events


def main() -> None:
    lead = decode(LEAD_B85)
    rhythm = decode(RHYTHM_B85)
    composition = {
        "metadata": {
            "title": "Comfortably Numb MIDI Reconstruction Test",
            "tempo": 60_000_000 / TEMPO_US_PER_BEAT,
            "time_signature": "4/4",
            "key": "D major / source MIDI",
            "description": (
                "Exact event-level reconstruction of the user-supplied MIDI "
                "using the existing explicit-event schema."
            ),
        },
        "sections": [{"name": "solo", "bars": 12}],
        "tracks": {
            "lead_guitar": {
                "role": "source Guitar 1",
                "sections": {
                    "solo": {"loop_bars": 12, "events": lead}
                },
            },
            "rhythm_guitar": {
                "role": "source Guitar 2",
                "sections": {
                    "solo": {"loop_bars": 12, "events": rhythm}
                },
            },
        },
    }
    path = ROOT / "composition.json"
    path.write_text(
        json.dumps(composition, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"[OK] wrote {path}")
    print(f"[OK] lead notes={len(lead)}, rhythm notes={len(rhythm)}")
    print("[OK] no melody generator or engine modification was used")


if __name__ == "__main__":
    main()
