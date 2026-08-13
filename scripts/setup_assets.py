from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
import urllib.request
import zipfile
import subprocess
from pathlib import Path

from _bootstrap import ROOT

FLUIDSYNTH_VERSION = "2.5.7"
FLUIDSYNTH_URL = (
    "https://github.com/FluidSynth/fluidsynth/releases/download/"
    "v2.5.7/fluidsynth-v2.5.7-win10-x64-cpp11.zip"
)
SOUNDFONT_URL = (
    "https://raw.githubusercontent.com/mrbumpy409/GeneralUser-GS/main/GeneralUser-GS.sf2"
)
SOUNDFONT_LICENSE_URL = (
    "https://raw.githubusercontent.com/mrbumpy409/GeneralUser-GS/main/documentation/LICENSE.txt"
)


def _download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "music-agent-setup/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response, destination.open("wb") as output:
        total = int(response.headers.get("Content-Length", 0))
        downloaded = 0
        while block := response.read(1024 * 1024):
            output.write(block)
            downloaded += len(block)
            if total:
                print(f"  {destination.name}: {downloaded / total:6.1%}", end="\r", flush=True)
    if total:
        print()


def install_fluidsynth(force: bool = False) -> Path:
    destination = ROOT / "tools" / "fluidsynth"
    expected = destination / "bin" / "fluidsynth.exe"
    alternate = destination / "fluidsynth.exe"
    if not force and (expected.is_file() or alternate.is_file()):
        path = expected if expected.is_file() else alternate
        print(f"[OK] FluidSynth already present: {path}")
        return path
    with tempfile.TemporaryDirectory(prefix="music-agent-fluid-") as temporary:
        archive = Path(temporary) / "fluidsynth.zip"
        unpacked = Path(temporary) / "unpacked"
        print(f"Downloading FluidSynth {FLUIDSYNTH_VERSION} official Windows x64 build...")
        _download(FLUIDSYNTH_URL, archive)
        with zipfile.ZipFile(archive) as handle:
            handle.extractall(unpacked)
        roots = [entry for entry in unpacked.iterdir() if entry.is_dir()]
        source = roots[0] if len(roots) == 1 else unpacked
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(source, destination)
    candidates = [destination / "bin" / "fluidsynth.exe", destination / "fluidsynth.exe"]
    path = next((candidate for candidate in candidates if candidate.is_file()), None)
    if path is None:
        raise RuntimeError("FluidSynth archive layout was not recognized")
    print(f"[OK] FluidSynth installed: {path}")
    return path


def install_soundfont(force: bool = False) -> Path:
    destination = ROOT / "assets" / "soundfonts" / "GeneralUser-GS.sf2"
    license_path = ROOT / "licenses" / "GeneralUser-GS-LICENSE.txt"
    if force or not destination.is_file():
        print("Downloading GeneralUser GS from its official repository...")
        _download(SOUNDFONT_URL, destination)
    else:
        print(f"[OK] SoundFont already present: {destination}")
    if force or not license_path.is_file():
        _download(SOUNDFONT_LICENSE_URL, license_path)
    if destination.stat().st_size < 20_000_000:
        raise RuntimeError(f"downloaded SoundFont is unexpectedly small: {destination}")
    print(f"[OK] GeneralUser GS ready ({destination.stat().st_size / 1_048_576:.1f} MiB)")
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description="Download the local renderer and free GM SoundFont.")
    parser.add_argument("--force", action="store_true", help="download clean copies")
    args = parser.parse_args()
    try:
        install_fluidsynth(args.force)
        install_soundfont(args.force)
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build_soundfont_catalog.py")],
            cwd=ROOT,
            check=True,
        )
    except Exception as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        return 1
    print("\nAssets ready. Run: python scripts/doctor.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
