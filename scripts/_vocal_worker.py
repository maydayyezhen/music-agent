from __future__ import annotations

import argparse
import json
import os
import time
import warnings
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
import librosa

from _bootstrap import ROOT
os.environ.setdefault("NLTK_DATA", str(ROOT / "assets" / "vocals" / "nltk_data"))
warnings.filterwarnings("ignore", message=".*weight_norm.*deprecated.*", category=FutureWarning)
from espnet2.bin.svs_inference import SingingGenerate


def main() -> int:
    parser = argparse.ArgumentParser(description="Internal ESPnet OpenCpop vocal renderer.")
    parser.add_argument("job")
    args = parser.parse_args()
    job = json.loads(Path(args.job).read_text(encoding="utf-8"))
    model = ROOT / job["model"]
    config = model / job.get("config", "exp/svs_visinger_normal/config.yaml")
    checkpoint = model / job.get("checkpoint", "exp/svs_visinger_normal/500epoch.pth")
    device = job.get("device", "cuda")
    if device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is unavailable; set device to cpu")
    start = time.perf_counter()
    engine = SingingGenerate(str(config), str(checkpoint), device=device, seed=int(job.get("seed", 777)))
    loaded = time.perf_counter()
    output = engine(
        {
            "label": ([tuple(item) for item in job["phone_times"]], job["phones"]),
            "score": (float(job["tempo"]), job["notes"]),
        },
        decode_conf={
            "noise_scale": float(job.get("noise_scale", 0.667)),
            "noise_scale_dur": float(job.get("noise_scale_dur", 0.8)),
        },
    )
    rendered = time.perf_counter()
    wav = output["wav"].detach().cpu().numpy().astype(np.float32)
    target_rate = int(job.get("sample_rate", engine.fs))
    if engine.fs != target_rate:
        wav = librosa.resample(wav, orig_sr=engine.fs, target_sr=target_rate)
    destination = Path(job["output"])
    destination.parent.mkdir(parents=True, exist_ok=True)
    sf.write(destination, wav, target_rate, subtype="PCM_16")
    print(json.dumps({
        "sample_rate": target_rate,
        "samples": len(wav),
        "duration_seconds": len(wav) / target_rate,
        "peak": float(np.max(np.abs(wav))),
        "rms": float(np.sqrt(np.mean(wav ** 2))),
        "load_seconds": loaded - start,
        "render_seconds": rendered - loaded,
        "gpu_peak_mb": torch.cuda.max_memory_allocated() / 1024 ** 2 if device == "cuda" else 0.0,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
