# New-server setup — DEM (LIGGGHTS) + MPM (Taichi) + Python + webapp

Setup for a fresh GPU server (e.g. `kgy@59.12.161.91`) to run this repo's DEM/MPM
pipeline.  Assumes a conda env named **uma** (`conda activate uma`).

## What runs where
| piece | engine | needs |
|---|---|---|
| **DEM** compaction (`dem_scripts/*.liggghts` → atoms.csv/contacts.csv) | **LIGGGHTS-PUBLIC** (C++ build) | g++, MPI, make |
| **MPM** compaction (`scripts/mpm3d_compaction.py`) | **Taichi 1.7.4**, `arch=cuda` | NVIDIA **driver** (CUDA bundled in the wheel) |
| post-processing (network σ, fits, plots) | Python | numpy/scipy/pandas/matplotlib |
| **webapp** (case browser + 3D viewer) | Flask | flask |

⚠ DEM here is **LIGGGHTS, not vanilla LAMMPS** — the inputs use `soft_particles yes`
and LIGGGHTS granular models (`fix property/global youngsModulus`, `pair gran`), which
LAMMPS does not have.

---

## 0) Clone the repo + branch
```bash
git clone https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT.git
cd Yonghoon-DEM-DFT
git checkout claude/stoic-knuth-NObVQ          # (or your working branch)
```

## 1) Python + MPM (Taichi)  — reliable, do this first
```bash
conda activate uma
bash scripts/setup_server.sh
```
This installs `numpy scipy pandas matplotlib flask python-pptx taichi==1.7.4`
(+ optional scikit-learn), checks `nvidia-smi`, and inits Taichi on CUDA.
- Taichi's wheel bundles its own CUDA runtime → you only need the **NVIDIA driver**
  (`nvidia-smi` must work), not the full CUDA toolkit.
- If Taichi CUDA init fails: the driver is missing/mismatched; MPM still runs on
  `--arch cpu` (slow) meanwhile.

Smoke-test MPM:
```bash
python scripts/mpm3d_compaction.py --help
# a real (small) run needs an am/se scaffold — generate one from a case via the webapp
# 첨가제 zip, or scripts/mpm_input_from_case.py, then: bash run_mpm.sh
```

## 2) DEM (LIGGGHTS)  — the C++ build
Toolchain first (conda-forge is the most portable):
```bash
conda install -c conda-forge gxx_linux-64 gcc_linux-64 openmpi make
# or system: sudo apt install build-essential openmpi-bin libopenmpi-dev
```
Then:
```bash
bash scripts/build_liggghts.sh                 # clones CFDEMproject/LIGGGHTS-PUBLIC + builds
```
Produces `LIGGGHTS-PUBLIC/src/lmp_auto` (or `lmp_mpi`).  Run a case from the repo root:
```bash
mpirun -np 4 LIGGGHTS-PUBLIC/src/lmp_auto -in dem_scripts/case09_E15x.liggghts
export LIGGGHTS_BIN="$PWD/LIGGGHTS-PUBLIC/src/lmp_auto"     # so scripts can find it
```
**Common build gotchas**
- `mpicxx not found` → install openmpi (above) and re-run.
- Newer g++ (≥11) can trip on old LIGGGHTS sources → `make serial` (no MPI) as a
  fallback, or pin `gxx_linux-64=10` in conda.
- **`fatal error: vtkSmartPointer.h: No such file or directory`** (very common): LIGGGHTS
  is trying to build the optional ParaView **VTK** output but VTK isn't installed. We don't
  need VTK (the pipeline reads atoms.csv/contacts.csv). Disable it:
  ```bash
  cd LIGGGHTS-PUBLIC/src && make clean-all
  mkdir -p ../_vtk_off && mv dump_*vtk*.cpp dump_*vtk*.h dump_vtk.* ../_vtk_off/ 2>/dev/null
  for f in MAKE/Makefile.mpi Makefile.package Makefile.package.settings; do
    [ -f "$f" ] && sed -i -E 's/-DLAMMPS_VTK//g; s#-I[[:space:]]*[^[:space:]]*vtk[^[:space:]]*##g; s/-lvtk[^[:space:]]*//g' "$f"
  done
  make -j$(nproc) mpi
  ```
  If another `*vtk*` source errors, move it into `../_vtk_off/` too and rebuild.

## 3) webapp (optional, for the viewer/zip generator)
```bash
cd webapp && python app.py          # then browse http://<server>:5000  (or PORT=5050 python app.py)
```

## 4) Verify the pipeline end-to-end
```bash
# DEM → post-processing
mpirun -np 4 LIGGGHTS-PUBLIC/src/lmp_auto -in dem_scripts/case09_E15x.liggghts
python scripts/network_conductivity.py --help          # Kirchhoff σ solver
# MPM
python scripts/mpm3d_compaction.py --help
```

## Notes
- **GPU**: MPM (`--arch cuda`) needs the NVIDIA driver only.  LIGGGHTS here is CPU/MPI
  (the `.liggghts` inputs don't request the GPU package).
- **sklearn** is only for the ML predictor (Phase 3); the DEM/MPM/network core doesn't
  need it.
- If any script raises `ModuleNotFoundError`, `pip install <module>` into `uma` — the
  repo has no pinned requirements file, so this guide's list is the working set.
- Data dirs: the webapp reads `results/<id>/` and `webapp/archive/<campaign>/`; MPM
  runs write `mpm_metrics.json` / `mpm_payload.json` to upload back.
