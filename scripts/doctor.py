from __future__ import annotations

import importlib.util
import math
import shutil
import sys
import tempfile
import wave
from pathlib import Path

from _bootstrap import ROOT


class Doctor:
    def __init__(self) -> None:
        self.failed = False

    def ok(self, label: str, detail: str = "") -> None:
        print(f"[OK] {label}{': ' + detail if detail else ''}")

    def warn(self, label: str, detail: str) -> None:
        print(f"[WARN] {label}: {detail}")

    def fail(self, label: str, detail: str) -> None:
        self.failed = True
        print(f"[FAIL] {label}: {detail}")


def _test_midi(path: Path, mido: object) -> None:
    midi = mido.MidiFile(type=1, ticks_per_beat=480)
    conductor = mido.MidiTrack()
    conductor.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(120), time=0))
    midi.tracks.append(conductor)
    music = mido.MidiTrack()
    music.append(mido.Message("program_change", program=0, channel=0, time=0))
    music.append(mido.Message("note_on", note=69, velocity=90, channel=0, time=0))
    music.append(mido.Message("note_off", note=69, velocity=0, channel=0, time=240))
    midi.tracks.append(music)
    midi.save(path)


def _write_test_wav(path: Path, sample_rate: int, np: object) -> None:
    time = np.arange(sample_rate // 4) / sample_rate
    mono = 0.1 * np.sin(2 * np.pi * 440 * time)
    stereo = np.column_stack((mono, mono))
    pcm = (stereo * 32767).astype("<i2")
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(2)
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        handle.writeframes(pcm.tobytes())


def main() -> int:
    doctor = Doctor()
    print("Music Agent environment check\n")
    doctor.ok("Python", sys.version.split()[0])
    missing = [name for name in ("mido", "numpy") if importlib.util.find_spec(name) is None]
    if missing:
        doctor.fail("Python dependencies", ", ".join(missing))
        print("\nMusic rendering environment is not ready.")
        return 1
    doctor.ok("Python dependencies", "mido, numpy")

    import mido
    import numpy as np

    from src.mixer import mix_stems
    from src.render.fluidsynth import find_fluidsynth, render_midi
    from src.render.sfizz import find_sfizz
    from src.utils import load_json

    executable = find_fluidsynth()
    if executable:
        doctor.ok("FluidSynth", str(executable))
    else:
        doctor.fail("FluidSynth", "run: python scripts/setup_assets.py")

    config = load_json(ROOT / "config" / "render.json")
    soundfont = ROOT / config["soundfont"]
    if soundfont.is_file() and soundfont.stat().st_size > 20_000_000:
        doctor.ok("SoundFont", f"{soundfont.name}, {soundfont.stat().st_size / 1_048_576:.1f} MiB")
    else:
        doctor.fail("SoundFont", "run: python scripts/setup_assets.py")

    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        doctor.ok("ffmpeg", ffmpeg)
    else:
        doctor.warn("ffmpeg", "not found; the built-in PCM mixer does not require it")

    sfizz = find_sfizz()
    if sfizz:
        doctor.ok("SFZ backend", str(sfizz))
    else:
        doctor.warn("SFZ backend", "optional; install sfizz when an instrument mapping uses engine=sfizz")

    vocal_python = ROOT / ".venv-vocals" / "Scripts" / "python.exe"
    vocal_model = (
        ROOT
        / "assets"
        / "vocals"
        / "espnet-opencpop-visinger"
        / "exp"
        / "svs_visinger_normal"
        / "500epoch.pth"
    )
    if vocal_python.is_file() and vocal_model.is_file() and vocal_model.stat().st_size > 400_000_000:
        probe = __import__("subprocess").run(
            [
                str(vocal_python),
                "-c",
                "import torch; from espnet2.bin.svs_inference import SingingGenerate; "
                "assert torch.cuda.is_available(); x=torch.ones(1,device='cuda'); "
                "print(torch.__version__, torch.cuda.get_device_name(0))",
            ],
            capture_output=True,
            text=True,
        )
        if probe.returncode == 0:
            doctor.ok("Optional vocal backend", probe.stdout.strip())
        else:
            doctor.warn("Optional vocal backend", probe.stderr.strip().splitlines()[-1])
    else:
        doctor.warn("Optional vocal backend", "not installed; instrumental rendering is unaffected")

    for relative in ("projects/demo_song/tracks", "projects/demo_song/stems", "projects/demo_song/output"):
        path = ROOT / relative
        try:
            path.mkdir(parents=True, exist_ok=True)
            probe = path / ".doctor-write-test"
            probe.write_text("ok", encoding="ascii")
            probe.unlink()
        except OSError as error:
            doctor.fail("Output directories", f"{path}: {error}")
            break
    else:
        doctor.ok("Output directories")

    if executable and soundfont.is_file():
        try:
            with tempfile.TemporaryDirectory(prefix="music-agent-doctor-") as temporary:
                directory = Path(temporary)
                midi_path = directory / "test.mid"
                wav_path = directory / "test.wav"
                _test_midi(midi_path, mido)
                render_midi(midi_path, soundfont, wav_path, int(config["sample_rate"]), 0.5)
                with wave.open(str(wav_path), "rb") as handle:
                    samples = np.frombuffer(handle.readframes(handle.getnframes()), dtype="<i2")
                    duration = handle.getnframes() / handle.getframerate()
                if duration <= 0 or int(np.max(np.abs(samples.astype(np.int32)))) == 0:
                    raise RuntimeError("rendered WAV is silent")
                doctor.ok("MIDI render", f"real A4 test tone, {duration:.2f}s")
        except Exception as error:
            doctor.fail("MIDI render", str(error))

    try:
        with tempfile.TemporaryDirectory(prefix="music-agent-mixer-") as temporary:
            directory = Path(temporary)
            _write_test_wav(directory / "left.wav", int(config["sample_rate"]), np)
            _write_test_wav(directory / "right.wav", int(config["sample_rate"]), np)
            output = directory / "mix.wav"
            stats = mix_stems(
                directory,
                output,
                {
                    "left": {"volume_db": -3, "pan": -0.5, "mute": False},
                    "right": {"volume_db": -3, "pan": 0.5, "mute": False},
                },
                int(config["sample_rate"]),
            )
            if not output.is_file() or stats["duration_seconds"] <= 0:
                raise RuntimeError("mixer did not produce a valid WAV")
            doctor.ok("Mixer", "stereo volume/pan test")
    except Exception as error:
        doctor.fail("Mixer", str(error))

    print()
    if doctor.failed:
        print("Music rendering environment is not ready.")
        return 1
    print("Music rendering environment ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
