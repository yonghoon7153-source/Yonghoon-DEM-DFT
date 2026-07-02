#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Server setup for Yonghoon-DEM-DFT — MPM (Taichi/CUDA) + Python post-processing
# + webapp.  DEM (LIGGGHTS) is built separately: scripts/build_liggghts.sh.
#
# Run INSIDE the target conda env:
#     conda activate uma
#     bash scripts/setup_server.sh
# ─────────────────────────────────────────────────────────────────────────────
set -uo pipefail
echo "[setup] python : $(command -v python)  ($(python --version 2>&1))"
echo "[setup] conda  : ${CONDA_DEFAULT_ENV:-<none>}   (expected: uma)"
if [ "${CONDA_DEFAULT_ENV:-}" != "uma" ]; then
  echo "[setup] ⚠ not in the 'uma' env — run 'conda activate uma' first (or continue if intentional)."
fi

# ── 1) Python deps: MPM + post-processing + webapp ───────────────────────────
python -m pip install --upgrade pip
python -m pip install numpy scipy pandas matplotlib flask python-pptx scikit-image
# MPM engine — Taichi (bundles its own CUDA runtime; only the NVIDIA *driver* is needed
# on the host, not the full CUDA toolkit).  Try the production 1.7.4; if its wheel needs
# a newer glibc than this host has (ImportError: GLIBC_2.32 not found), fall back to
# 1.6.0 (manylinux_2_27 → glibc 2.27, works on older servers; same MPM API + results).
python -m pip install "taichi==1.7.4"
if ! python -c "import taichi" >/dev/null 2>&1; then
  echo "[setup] taichi 1.7.4 import failed (likely host glibc < 2.32) → falling back to 1.6.0"
  python -m pip install "taichi==1.6.0"
fi
# optional: ML predictor training (Phase 3).  Safe to skip if it fails.
python -m pip install scikit-learn || echo "[setup] scikit-learn optional → skipped"

# ── 2) GPU / Taichi-CUDA check ───────────────────────────────────────────────
echo "[setup] --- GPU check ---"
if command -v nvidia-smi >/dev/null 2>&1; then nvidia-smi -L; else
  echo "[setup] ⚠ nvidia-smi missing → install the NVIDIA driver for GPU MPM (CPU --arch cpu still works)"; fi
python - <<'PY' 2>/dev/null || echo "[setup] ⚠ Taichi CUDA init failed — check the NVIDIA driver; MPM can fall back to --arch cpu"
import taichi as ti
ti.init(arch=ti.cuda)
print("[setup] Taichi CUDA OK  (version", ti.__version__, ")")
PY

# ── 3) sanity: core imports ──────────────────────────────────────────────────
python - <<'PY'
import numpy, scipy, pandas, matplotlib, flask
print("[setup] core imports OK")
PY

echo "[setup] ------------------------------------------------------------------"
echo "[setup] DONE — Python + MPM (Taichi) ready."
echo "[setup] NEXT:"
echo "[setup]   • DEM (LIGGGHTS):   bash scripts/build_liggghts.sh   (see docs/server_setup.md §2)"
echo "[setup]   • MPM smoke test:   python scripts/mpm3d_compaction.py --help"
echo "[setup]   • webapp:           cd webapp && python app.py"
