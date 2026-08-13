from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOULX = ROOT / "tools" / "soulx-singer"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(SOULX))

from cli.inference import build_model, process
from soulxsinger.utils.file_utils import load_config
from src.vocals.english import build_soulx_metadata

import librosa
import numpy as np
import soundfile as sf


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("job")
    args = parser.parse_args()
    job = json.loads(Path(args.job).read_text(encoding="utf-8"))
    config_path = SOULX / "soulxsinger" / "config" / "soulxsinger.yaml"
    config = load_config(str(config_path))
    metadata = []
    for index, phrase in enumerate(job["phrases"], 1):
        item = build_soulx_metadata(phrase, float(job["tempo"]), index)
        start_ms = round(float(phrase["start_beat"]) * 60.0 / float(job["tempo"]) * 1000)
        duration_ms = item["time"][1]
        item["time"] = [start_ms, start_ms + duration_ms]
        metadata.append(item)
    metadata_path = Path(job["metadata"])
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    namespace = argparse.Namespace(
        control="score",
        prompt_metadata_path=str(SOULX / "example" / "audio" / "en_prompt.json"),
        prompt_wav_path=str(SOULX / "example" / "audio" / "en_prompt.mp3"),
        target_metadata_path=job["metadata"],
        phoneset_path=str(SOULX / "soulxsinger" / "utils" / "phoneme" / "phone_set.json"),
        save_dir=job["save_dir"],
        device=job.get("device", "cuda"),
        auto_shift=False,
        pitch_shift=int(job.get("pitch_shift", 0)),
        use_fp16=True,
    )
    model = build_model(
        str(ROOT / "assets" / "vocals" / "soulx-singer" / "model.pt"),
        config,
        device=namespace.device,
        use_fp16=True,
    )
    process(namespace, config, model)
    generated = Path(namespace.save_dir) / "generated.wav"
    audio, rate = sf.read(generated, dtype="float32")
    target_rate = int(job["sample_rate"])
    if rate != target_rate:
        audio = librosa.resample(audio, orig_sr=rate, target_sr=target_rate)
    expected_frames = round(float(job["song_seconds"]) * target_rate)
    if len(audio) < expected_frames:
        audio = np.pad(audio, (0, expected_frames - len(audio)))
    else:
        audio = audio[:expected_frames]
    sf.write(job["output"], audio, target_rate, subtype="PCM_16")
    print(json.dumps({
        "sample_rate": target_rate,
        "duration_seconds": len(audio) / target_rate,
        "peak": float(np.max(np.abs(audio))),
        "rms": float(np.sqrt(np.mean(audio ** 2))),
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
