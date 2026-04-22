# KISTI Neuron — Software Installation & Environment Guide

Observed setup for argyrodite DFT/MLIP workflow on KISTI Neuron (glogin01).
Paths reflect user x3430a02 but pattern is identical for others.

---

## 1. Host & Access
- **Login node:** `glogin01.neuron.ksc.re.kr`
- **Shell:** zsh (prompt shows `(uma) N% [x3430a02@glogin01 ...]`)
- **Storage root:** `/scratch/x3430a02/kgy/` (personal scratch)
- **Shared miniforge:** `/scratch/x3430a02/mjs0000/miniforge3/` (lab member Minseok Jo's install)

## 2. Conda environments (already set up)

Shared base — activate on login:
```bash
source /scratch/x3430a02/mjs0000/miniforge3/etc/profile.d/conda.sh
conda env list
# base  /scratch/x3430a02/mjs0000/miniforge3
# mace  /scratch/x3430a02/mjs0000/miniforge3/envs/mace
# uma   /scratch/x3430a02/mjs0000/miniforge3/envs/uma
```

### `uma` env (adhesion calculations, UMA MLIP)
```bash
conda activate uma
# contains: ase, numpy, scipy, fairchem (uma-s-1p1)
pip list | grep -iE "ase|fairchem|torch|pymatgen"
```
Used for v5 xy-shift adhesion, Li annealing, MLIP EOS screening.

### `mace` env (MACE-MP-0 screening)
```bash
conda activate mace
# contains: mace-torch (MACE-MP-0), ase, numpy
```
Used for halogen enumeration screening + 600K snapshot elastic.

### Python 3.10, CUDA 12.9

---

## 3. Quantum ESPRESSO (pre-compiled GPU build)

```
/scratch/x3430a02/kgy/apps/qe-gpu/bin/pw.x   # GPU-accelerated PWscf
/scratch/x3430a02/kgy/apps/qe-cpu/bin/pw.x   # CPU fallback
```
Both in `$PATH`. Built with OpenMPI 4.1.8 + CUDA 12.9.1 + MKL 2025.3.

Test:
```bash
which pw.x
pw.x -version
```

### Compile notes (reference only, if re-building needed)
- Modules loaded at build time (from `module list` at user's PATH):
  - `openmpi/4.1.8/gcc/11.5.0/cuda/12.9.1`
  - `cuda/12.9.1`
  - `mkl/2025.3`
  - `hdf5/2.0.0`
  - `libxc/7.0.0`
  - `fftw3/3.3.10`
  - `cmake/4.2.1`
  - `ucx/1.20.0`
- QE configure with:
  ```bash
  ./configure \
      CC=mpicc CXX=mpic++ FC=mpif90 \
      --with-cuda=$CUDA_HOME \
      --with-cuda-runtime=12.9 \
      --with-cuda-cc=80 \
      --enable-openmp \
      --enable-parallel \
      --with-scalapack=yes
  ```

---

## 4. Pseudopotentials

```
/scratch/x3430a02/kgy/manuscript_support/pseudo/
```
All SSSP-efficiency PBE UPF files (Li, P, S, Cl, Br, Ni, O).

Referenced in QE input as:
```
ATOMIC_SPECIES
  Li   6.9410   li_pbe_v1_4_uspp_F.UPF
  P   30.9740   P_pbe-n-rrkjus_psl_1_0_0.UPF
  S   32.0650   s_pbe_v1_4_uspp_F.UPF
  Cl  35.4530   cl_pbe_v1_4_uspp_F.UPF
  Br  79.9040   br_pbe_v1_4_uspp_F.UPF
  Ni  58.6934   Ni.pbe-spn-rrkjus_psl_1_0_0.UPF
  O   15.9994   O.pbe-n-rrkjus_psl_1_0_0.UPF
```

---

## 5. Running jobs on login node (current workflow)

### GPU visibility
```bash
# On login node with attached GPUs (2 × H200 or A100 typical)
nvidia-smi
export CUDA_VISIBLE_DEVICES=0   # or 1
```

### Direct run pattern (as used in run_gpu*.sh)
```bash
QE=/scratch/x3430a02/kgy/apps/qe-gpu/bin/pw.x
cd <working_dir>
$QE -input relax.in > relax.out 2>&1
```
Note: **no mpirun** for single-GPU runs. `pw.x` picks up GPU directly.

### Multi-GPU: split volumes
```bash
# GPU0: one subset
export CUDA_VISIBLE_DEVICES=0; $QE -input v096/relax.in > v096/relax.out &
# GPU1: another subset
export CUDA_VISIBLE_DEVICES=1; $QE -input v102/relax.in > v102/relax.out &
wait
```

### Restart-safe wrapper (for walltime kills)
See `run_gpu0_redo.sh`, `run_gpu1_redo.sh`:
- Check `JOB DONE` → skip
- If `tmp/<prefix>.save/` exists → prepend `restart_mode='restart'`
- Otherwise fresh
- Re-run on next invocation if killed

---

## 6. Login-node limitations (observed)

- Walltime limit **~several hours** then SIGKILL
- No guaranteed GPU reservation (shared)
- Use pattern: `while incomplete; do ./run.sh; done` (loop until done)
- **Proper solution:** SLURM batch submission (below), but login-node repeats also work

---

## 7. SLURM batch template (if/when used)

```bash
#!/bin/bash
#SBATCH -J modelC
#SBATCH -p amd_a100_8         # check: sinfo -s
#SBATCH --gres=gpu:2
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=2
#SBATCH -t 24:00:00
#SBATCH -o %x_%j.out
#SBATCH -e %x_%j.err

source /scratch/x3430a02/mjs0000/miniforge3/etc/profile.d/conda.sh
conda activate uma

QE=/scratch/x3430a02/kgy/apps/qe-gpu/bin/pw.x
# ... (run logic identical to login-node scripts)
```

Check queue:
```bash
sinfo -s              # partitions
squeue -u $USER       # your jobs
scontrol show partitions
```

---

## 8. Common tasks quick-reference

| Task | Command |
|------|---------|
| Activate UMA env | `conda activate uma` |
| Start QE relax (GPU0) | `CUDA_VISIBLE_DEVICES=0 pw.x -input relax.in > relax.out 2>&1` |
| Check QE progress | `grep "iteration\|Total force\|JOB DONE" relax.out \| tail` |
| GPU memory | `nvidia-smi --query-gpu=memory.used,memory.free --format=csv` |
| Kill all pw.x | `pkill -9 -f pw.x` |
| Continue after kill | `./run_gpu0_redo.sh` (auto-detects `tmp/<prefix>.save`) |

---

## 9. Project directories

```
/scratch/x3430a02/kgy/manuscript_support/
├── pseudo/                         # All PBE USPPs
├── pipeline_v1/                    # v1 (Rietveld Li) data
│   ├── comp1/ comp2/ comp3/ comp4/ comp5/
│   └── modelc_lpsc16/
├── pipeline_v2/                    # v2 (annealing champion) data
│   ├── comp1_v2/                   # DFT done
│   └── modelC_lpsc16/              # DFT EOS in progress
├── adhesion/                       # v5 xy-shift interfaces
│   ├── structures/*.xyz
│   └── results/*.json
└── post_processing/                # Bader, DOS, bonds, elastic
```

---

## 10. Troubleshooting

**`command not found` in shell script**
- Cause: `pw.x` not absolute path inside script
- Fix: use `$QE=/scratch/x3430a02/kgy/apps/qe-gpu/bin/pw.x` variable

**`ModuleNotFoundError: numpy`** on `python3`
- Cause: running outside conda env
- Fix: `conda activate uma` first

**ASE reader `IndexError` on restart-merged relax.out**
- Cause: multiple ATOMIC_POSITIONS blocks from restart_mode confuse parser
- Fix: regex extraction of final `Begin final coordinates ... End final coordinates` block

**QE BM3 fit B₀ 4× too high**
- Cause: wrong Birch-Murnaghan formula using `f = (V0/V)^(2/3) - 1` without factor ½
- Fix: `f = 0.5 * ((V0/V)^(2/3) - 1)` OR use standard form:
  ```python
  eta = (V0/V)**(2/3)
  E = E0 + 9*V0*B0/16 * ((eta-1)**2 * (6-4*eta) + Bp * (eta-1)**3)
  ```

**Volume-induced basin transitions during EOS scan**
- Detect: compare `get_scaled_positions()` between adjacent volumes
- If any atom Δfrac > 0.05 → basin change
- Fix: re-run from reference basin champion coords (see `tools/` scripts or `run_gpu*_redo.sh` pattern)
