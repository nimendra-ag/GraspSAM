# GraspSAM — Windows Setup Guide

> The original `requirements.txt` was generated from a Linux conda environment and does not work as-is on Windows. Follow this guide **exactly in order** using the cleaned `requirements.txt` included in this repo.

---

## Prerequisites

Before starting, make sure you have all of these:

1. **[Anaconda or Miniconda](https://docs.conda.io/en/latest/miniconda.html)** — installed and working from your terminal
2. **[Git](https://git-scm.com/download/win)** — installed and available in PATH (run `git --version` to check)
3. **[Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)** — install with the **"Desktop development with C++"** workload selected. Required for compiling GroundingDINO's C++/CUDA extensions. Run `where cl` to verify — if it returns a path, you're good.
4. **NVIDIA GPU with CUDA support** and up-to-date drivers

---

## Step 1 — Create the conda environment

```bash
conda create -n GraspSAM python=3.10 -y
conda activate GraspSAM
```

> **Why Python 3.10?** The original env used Python 3.8, which is too old — many pinned packages (contourpy, pandas, etc.) require ≥3.9.

---

## Step 2 — Install PyTorch with CUDA

This **must** be done before everything else. PyPI's default torch is CPU-only on Windows.

```bash
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118
```

Verify:

```bash
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
```

Expected: `2.0.1+cu118 True`. **Do not proceed if this says False.**

---

## Step 3 — Downgrade setuptools and install build helpers

CLIP's `setup.py` uses `pkg_resources` (removed in recent setuptools), and lang-sam uses Poetry as its build backend.

```bash
pip install "setuptools<70" poetry-core
```

---

## Step 4 — Install CLIP

```bash
pip install --no-build-isolation git+https://github.com/openai/CLIP.git@dcba3cb2e2827b402d2701e7e1c7d9fed8a20ef1
```

**If that fails**, clone and install directly:

```bash
git clone https://github.com/openai/CLIP.git
cd CLIP
git checkout dcba3cb2e2827b402d2701e7e1c7d9fed8a20ef1
python setup.py install
cd ..
```

Verify:

```bash
python -c "import clip; print('clip: OK')"
```

---

## Step 5 — Install GroundingDINO

GroundingDINO's `setup.py` has a hardcoded subprocess call that tries to `pip install torch` inside pip's build isolation, which always breaks. Use `--no-build-isolation` so it sees your existing torch:

```bash
pip install --no-build-isolation git+https://github.com/IDEA-Research/GroundingDINO.git
```

**If that fails**, clone and install directly:

```bash
git clone https://github.com/IDEA-Research/GroundingDINO.git
cd GroundingDINO
python setup.py install
cd ..
```

Verify:

```bash
pip show groundingdino
```

---

## Step 6 — Install segment-anything

```bash
pip install --no-build-isolation git+https://github.com/facebookresearch/segment-anything.git@6fdee8f2727f4506cfbbe553e23b895e27956588
```

Verify:

```bash
python -c "import segment_anything; print('segment_anything: OK')"
```

---

## Step 7 — Install lang-sam (skip its dependencies)

`lang-sam` declares `groundingdino` as a git dependency in its `pyproject.toml`, which triggers the broken GroundingDINO build again. Since GroundingDINO and segment-anything are already installed, skip dependency resolution with `--no-deps`.

```bash
pip install --no-build-isolation --no-deps "lang-sam @ git+https://github.com/luca-medeiros/lang-segment-anything.git@05c386ee95b26a8ec8398bebddf70ffb8ddd3faf"
```

Verify:

```bash
python -c "import lang_sam; print('lang_sam: OK')"
```

---

## Step 8 — Navigate to the GraspSAM project directory

Make sure you are in the GraspSAM repo root where the cleaned `requirements.txt` lives:

```bash
cd E:\GraspSAM
```

(Replace with your actual path.)

---

## Step 9 — Install remaining dependencies

Use `--no-deps` to prevent pip's resolver from pulling in newer transitive dependencies that overwrite the pinned versions (this is the single biggest source of problems with this repo).

```bash
pip install --no-deps -r requirements.txt
```

> **Why `--no-deps`?** Without it, pip resolves transitive dependencies and silently upgrades numpy to 2.x, transformers to 5.x, Pillow to 12.x, etc. — breaking everything. Since the requirements file already lists every package the environment needs, `--no-deps` installs exactly what's listed.

---

## Step 10 — Re-pin critical packages

Even with `--no-deps`, some packages may have been overwritten by earlier steps. Force the correct versions:

```bash
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118
pip install "numpy>=1.24.4,<1.26" transformers==4.44.0 huggingface-hub==0.23.5 opencv-python==4.9.0.80 Pillow==9.4.0
```

---

## Step 11 — Final verification

Run all checks at once:

```bash
python -c "import torch; print('torch:', torch.__version__, '| CUDA:', torch.cuda.is_available())"
python -c "import clip; print('clip: OK')"
python -c "import groundingdino; print('groundingdino: OK')"
python -c "import lang_sam; print('lang_sam: OK')"
python -c "import segment_anything; print('segment_anything: OK')"
python -c "import transformers; print('transformers:', transformers.__version__)"
python -c "import lightning; print('lightning: OK')"
python -c "import numpy; print('numpy:', numpy.__version__)"
```

**Expected output:**

```
torch: 2.0.1+cu118 | CUDA: True
clip: OK
groundingdino: OK
lang_sam: OK
segment_anything: OK
transformers: 4.44.0
lightning: OK
numpy: 1.25.x
```

If `CUDA: False`, repeat Step 10's torch install.

---

## Expected warnings (harmless)

These warnings will appear during imports but do **not** indicate a broken environment:

| Warning | Meaning |
|---|---|
| `FutureWarning: Importing from timm.models.layers is deprecated` | timm deprecation notice — cosmetic only |
| `Failed to load custom C++ ops. Running on CPU mode Only!` | GroundingDINO's CUDA C++ extensions didn't compile on Windows. It falls back to a Python/CPU implementation — slower but functional |

---

## What was cleaned from the original requirements.txt

The original `requirements.txt` was exported from a Linux conda environment with `pip freeze` and contained paths and packages that don't work on Windows. The cleaned version has these changes:

| Removed / Changed | Reason |
|---|---|
| All `@ file:///...` local paths | Pointed to the original author's Linux filesystem |
| `torch`, `torchvision`, `torchaudio` | Installed separately with CUDA in Step 2 |
| `clip`, `lang-sam`, `segment-anything` | Installed manually in Steps 4–7 to work around build issues |
| All `nvidia-*` packages (cu11 and cu12) | PyTorch bundles the correct CUDA runtime libraries automatically |
| `triton==2.0.0` | Linux-only; not available on Windows |
| `pickle5==0.0.11` | Only needed for Python < 3.8; fails on modern Python |
| `mkl-fft`, `mkl-random`, `mkl-service` | Conda-internal packages; not installable via pip |
| `gmpy2` | Conda-internal package; not installable via pip on Windows |
| `MultiScaleDeformableAttention==1.0` | Requires separate source build from Deformable-DETR repo |
| `numpy==1.23.1` → `numpy>=1.24.4,<1.26` | `albumentations==1.4.2` requires numpy ≥1.24.4 |

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'pkg_resources'` | `pip install "setuptools<70"` |
| `Cannot import 'poetry.core.masonry.api'` | `pip install poetry-core` |
| GroundingDINO build fails with "No module named 'torch'" | Use `--no-build-isolation` or clone repo and run `python setup.py install` |
| `torch.cuda.is_available()` returns `False` | `pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118` |
| numpy conflict with albumentations | Use `numpy>=1.24.4,<1.26` |
| `where cl` returns nothing | Install Visual Studio Build Tools with "Desktop development with C++" |
| pip rebuilds groundingdino during `requirements.txt` | Make sure `lang-sam`, `clip`, and `segment-anything` lines are removed from requirements.txt |
| NumPy 2.x crash (`_ARRAY_API not found`) | `pip install "numpy>=1.24.4,<1.26"` |
| `transformers` says "PyTorch >= 2.5 is required" | `pip install transformers==4.44.0` |
| `huggingface-hub` version incompatible | `pip install huggingface-hub==0.23.5` |
| Pillow version incompatible | `pip install Pillow==9.4.0` |
| opencv-python version incompatible | `pip install opencv-python==4.9.0.80` |
