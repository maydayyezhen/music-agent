$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root ".venv-vocals\Scripts\python.exe"
$ChineseModel = Join-Path $Root "assets\vocals\espnet-opencpop-visinger"
$JapaneseModel = Join-Path $Root "assets\vocals\espnet-kiritan-visinger"
$EnglishModel = Join-Path $Root "assets\vocals\soulx-singer"
$SoulXTools = Join-Path $Root "tools\soulx-singer"
$HfCommand = Get-Command hf -ErrorAction SilentlyContinue
$Hf = if ($HfCommand) { $HfCommand.Source } else { Join-Path $env:USERPROFILE "miniconda3\Scripts\hf.exe" }

if (-not (Test-Path $Python)) {
    py -3.11 -m venv (Join-Path $Root ".venv-vocals")
}

& $Python -m pip install --upgrade pip
& $Python -m pip install torch==2.7.1+cu128 torchaudio==2.7.1+cu128 --index-url https://download.pytorch.org/whl/cu128

# ESPnet declares several training-only packages that need a compiler on Windows.
# Install the runtime itself without dependency expansion, then the pinned inference set.
& $Python -m pip install --no-deps espnet==202310
& $Python -m pip install -r (Join-Path $Root "requirements-vocals.txt")

$NltkData = Join-Path $Root "assets\vocals\nltk_data"
New-Item -ItemType Directory -Force -Path $NltkData | Out-Null
& $Python -c "import nltk; nltk.download('averaged_perceptron_tagger', download_dir=r'$NltkData'); nltk.download('cmudict', download_dir=r'$NltkData')"

if (-not (Test-Path $Hf)) {
    throw "Hugging Face CLI not found at $Hf. Install it with: pip install huggingface_hub"
}
New-Item -ItemType Directory -Force -Path $ChineseModel | Out-Null
& $Hf download espnet/opencpop_visinger README.md meta.yaml `
    exp/svs_stats_raw_phn_None_zh/train/feats_stats.npz `
    exp/svs_stats_raw_phn_None_zh/train/pitch_stats.npz `
    exp/svs_visinger_normal/config.yaml `
    exp/svs_visinger_normal/500epoch.pth `
    --local-dir $ChineseModel

New-Item -ItemType Directory -Force -Path $JapaneseModel | Out-Null
& $Hf download espnet/kiritan_svs_visinger README.md meta.yaml `
    exp/svs_stats_raw_phn_pyopenjtalk_jp/train/feats_stats.npz `
    exp/svs_stats_raw_phn_pyopenjtalk_jp/train/pitch_stats.npz `
    exp/svs_train_visinger_24_raw_phn_pyopenjtalk_jp/config.yaml `
    exp/svs_train_visinger_24_raw_phn_pyopenjtalk_jp/200epoch.pth `
    --local-dir $JapaneseModel

New-Item -ItemType Directory -Force -Path $EnglishModel | Out-Null
& $Hf download Soul-AILab/SoulX-Singer model.pt config.yaml README.md --local-dir $EnglishModel

# Keep the minimal, pinned English inference runtime local and reproducible.
if (-not (Test-Path (Join-Path $SoulXTools "soulxsinger"))) {
    $Checkout = Join-Path $Root "work\setup-soulx"
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Checkout) | Out-Null
    git clone https://github.com/Soul-AILab/SoulX-Singer.git $Checkout
    git -C $Checkout checkout 81aeb3ae772c70093c3de74dc23c92d983801ae4
    New-Item -ItemType Directory -Force -Path $SoulXTools | Out-Null
    Copy-Item -LiteralPath (Join-Path $Checkout "cli") -Destination $SoulXTools -Recurse
    Copy-Item -LiteralPath (Join-Path $Checkout "soulxsinger") -Destination $SoulXTools -Recurse
    New-Item -ItemType Directory -Force -Path (Join-Path $SoulXTools "example\audio") | Out-Null
    Copy-Item -LiteralPath (Join-Path $Checkout "example\audio\en_prompt.mp3") -Destination (Join-Path $SoulXTools "example\audio")
    Copy-Item -LiteralPath (Join-Path $Checkout "example\audio\en_prompt.json") -Destination (Join-Path $SoulXTools "example\audio")
}

& $Python -c "import torch; from espnet2.bin.svs_inference import SingingGenerate; assert torch.cuda.is_available(); print(torch.__version__, torch.cuda.get_device_name(0))"
Write-Host "[OK] Optional Chinese, English, and Japanese vocal backends installed."
