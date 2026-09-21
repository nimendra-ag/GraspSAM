# GraspSAM — Windows Setup Guide

> The original `requirements.txt` was generated from a Linux conda environment and does not work as-is on Windows. Follow this guide **exactly in order** using the cleaned `requirements.txt` included in this repo.

---

## Prerequisites

Before starting, make sure you have all of these:

1. **[Anaconda or Miniconda](https://docs.conda.io/en/latest/miniconda.html)** — installed and working from your terminal
2. **[Git](https://git-scm.com/download/win)** — installed and available in PATH (run `git --version` to check)
3. **[Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)** — install with the **"Desktop development with C++"** workload selected. This is required for compiling GroundingDINO's C++/CUDA extensions. Run `where cl` to verify — if it returns a path, you're good.
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

## Step 3 — Downgrade setuptools

CLIP's `setup.py` uses `pkg_resources`, which was removed in recent setuptools versions.

```bash
pip install "setuptools<70"
```

---

## Step 4 — Install CLIP

```bash
pip install --no-build-isolation git+https://github.com/openai/CLIP.git@dcba3cb2e2827b402d2701e7e1c7d9fed8a20ef1
```

**If that fails**, clone and install directly:

```bash
cd %USERPROFILE%\Desktop
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

GroundingDINO's `setup.py` has a hardcoded `subprocess` call that tries to `pip install torch` inside pip's build isolation, which always breaks. Clone and install directly:

```bash
cd %USERPROFILE%\Desktop
git clone https://github.com/IDEA-Research/GroundingDINO.git
cd GroundingDINO
pip install --no-build-isolation .
cd ..
```

**If that fails**, fall back to:

```bash
cd GroundingDINO
python setup.py install
cd ..
```

> **Note:** Do NOT use `-e .` (editable install). That ties the package to the cloned folder — deleting the folder later breaks your environment.

Verify:

```bash
pip show groundingdino
```

---

## Step 6 — Install lang-sam (skip its dependencies)

`lang-sam` declares `groundingdino` as a git dependency in its `pyproject.toml`. Since GroundingDINO is already installed, we skip dependency resolution entirely with `--no-deps`. We also need `poetry-core` because lang-sam uses Poetry as its build backend.

```bash
pip install poetry-core
pip install --no-build-isolation --no-deps "lang-sam @ git+https://github.com/luca-medeiros/lang-segment-anything.git@05c386ee95b26a8ec8398bebddf70ffb8ddd3faf"
```

Verify:

```bash
python -c "import lang_sam; print('lang_sam: OK')"
```

---

## Step 7 — Install segment-anything

```bash
pip install --no-build-isolation git+https://github.com/facebookresearch/segment-anything.git@6fdee8f2727f4506cfbbe553e23b895e27956588
```

Verify:

```bash
python -c "import segment_anything; print('segment_anything: OK')"
```

---

## Step 8 — Navigate back to the GraspSAM project directory

Make sure you are in the GraspSAM repo root where the cleaned `requirements.txt` lives:

```bash
cd C:\Users\ASUS\OneDrive\Desktop\UoM\GraspSAM
```

(Replace with your actual path.)

---

## Step 9 — Install remaining dependencies

```bash
pip install -r requirements.txt
```

This uses the **cleaned** `requirements.txt` — NOT the original. See [What was cleaned](#what-was-cleaned-from-the-original-requirementstxt) below.

---

## Step 10 — Reinstall PyTorch with CUDA (critical)

Step 9 can silently downgrade or replace torch with a CPU-only version pulled from PyPI as a transitive dependency. **Always re-pin torch after installing requirements:**

```bash
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118
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
python -c "import transformers; print('transformers: OK')"
python -c "import lightning; print('lightning: OK')"
```

**Expected output:**

```
torch: 2.0.1+cu118 | CUDA: True
clip: OK
groundingdino: OK
lang_sam: OK
segment_anything: OK
transformers: OK
lightning: OK
```

If `CUDA: False`, repeat Step 10.

---

## What was cleaned from the original requirements.txt

The original `requirements.txt` was exported from a Linux conda environment with `pip freeze` and contained paths and packages that don't work on Windows. The cleaned version has these changes:

| Removed / Changed | Reason |
|---|---|
| All `@ file:///...` local paths | These pointed to the original author's Linux filesystem |
| `torch`, `torchvision`, `torchaudio` | Installed separately with CUDA in Step 2 (and re-pinned in Step 10) |
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
| `ModuleNotFoundError: No module named 'pkg_resources'` | Run `pip install "setuptools<70"` |
| `Cannot import 'poetry.core.masonry.api'` | Run `pip install poetry-core` |
| GroundingDINO build fails with "No module named 'torch'" | Clone the repo and run `python setup.py install` directly |
| `torch.cuda.is_available()` returns `False` | Reinstall torch: `pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118` |
| numpy conflict with albumentations | Use `numpy>=1.24.4,<1.26` instead of `==1.23.1` in requirements.txt |
| `where cl` returns nothing | Install Visual Studio Build Tools with "Desktop development with C++" |
| pip tries to rebuild groundingdino when installing requirements | Make sure `lang-sam` and `clip` lines are removed from requirements.txt |
