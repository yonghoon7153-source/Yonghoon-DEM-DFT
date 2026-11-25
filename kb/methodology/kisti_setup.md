# KISTI Neuron — Software Installation & Environment Guide

**Source:** extracted from `/scratch/x3430a02/kgy/setup_neuron.sh` (2026-04-06)
Working environment for argyrodite DFT/MLIP workflow on KISTI Neuron.

---

## 1. Host specification

| Item | Value |
|------|-------|
| **Login node** | `glogin01.neuron.ksc.re.kr` |
| **GPU** | NVIDIA **A100 80GB PCIe** (compute capability 8.0, sm_80) |
| **Default GPU** | `CUDA_VISIBLE_DEVICES=1` (GPU 0 reserved by other users) |
| **Work dir** | `/scratch/x3430a02/kgy/` |
| **Home dir** | `/home01/x3430a02/` |

## 2. Module toolchain

```bash
module load gcc/11.5.0
module load cuda/12.5                   # auto-redirects to 12.4.1
module load cudampi/openmpi-4.1.8
module load cmake/4.1.3                 # auto-redirects to 4.2.1
module load fftw3/3.3.10
module load libxc/7.0.0
module load hdf5/1.12.0                 # auto-redirects to 2.0.0
module load mkl/2025.3
```

**For GPU QE build only:**
```bash
module load nvhpc/25.11_cuda12
module load cuda/12.5
```

## 3. Installed applications

### QE 7.4.1

| Variant | Path | Status | Notes |
|---------|------|--------|-------|
| **GPU** | `/scratch/x3430a02/kgy/apps/qe-gpu/bin/pw.x` | ✅ built | nvfortran / cc80 / nvhpc |
| CPU | `/scratch/x3430a02/kgy/apps/qe-cpu/bin/pw.x` | ⚠️ built with issues | libxc linkage trouble (see setup.log) |

Build commands (GPU):
```bash
cd $WORK/apps/qe-gpu
./configure \
    --with-cuda=$CUDA_HOME \
    --with-cuda-runtime=12.5 \
    --with-cuda-cc=80 \
    --enable-openmp \
    FC=nvfortran F90=nvfortran CC=nvc MPIF90=mpifort
make -j8 pw pp
```

### LIGGGHTS-PUBLIC (DEM simulations)

```
/scratch/x3430a02/kgy/apps/LIGGGHTS-PUBLIC/src/lmp_mpi
```
Built without VTK (flags stripped from Makefile.mpi).

### Conda environments

Shared miniforge at `/scratch/x3430a02/mjs0000/miniforge3/`.

```bash
source /scratch/x3430a02/mjs0000/miniforge3/etc/profile.d/conda.sh
conda env list
```

| Env | Purpose | Key packages |
|-----|---------|-------------|
| `base` | default | - |
| `mace` | MACE-MP-0 | torch (cu121), mace-torch, ase, pymatgen |
| `uma` | UMA MLIP | torch (cu121), fairchem-core, ase, pymatgen |

Create (if missing):
```bash
# MACE
conda create -n mace python=3.11 -y
conda activate mace
pip install torch --index-url https://download.pytorch.org/whl/cu121
pip install mace-torch ase numpy scipy matplotlib pandas pymatgen

# UMA
conda create -n uma python=3.11 -y
conda activate uma
pip install torch --index-url https://download.pytorch.org/whl/cu121
pip install fairchem-core ase pymatgen numpy scipy matplotlib pandas huggingface-hub
```

## 4. Environment (bashrc block)

Appended to `~/.bashrc` by setup script:

```bash
# ===== Neuron Custom Environment =====
export CUDA_VISIBLE_DEVICES=1

module purge 2>/dev/null
module load gcc/11.5.0
module load cuda/12.5
module load cudampi/openmpi-4.1.8
module load cmake/4.1.3
module load fftw3/3.3.10
module load libxc/7.0.0
module load hdf5/1.12.0
module load mkl/2025.3

export WORK=/scratch/x3430a02/kgy
export PATH=$WORK/apps/qe-cpu/bin:$PATH
export PATH=$WORK/apps/qe-gpu/bin:$PATH
export PATH=$WORK/apps/LIGGGHTS-PUBLIC/src:$PATH
export PSEUDO_DIR=$WORK/pseudo

alias cds='cd /scratch/x3430a02/kgy'
alias cdp='cd /scratch/x3430a02/kgy/projects'

run_bg() { nohup "$@" > "${1##*/}.log" 2>&1 & echo "PID: $!"; }
# ===== End Custom Environment =====
```

Also symlinks:
```
~/apps     -> /scratch/x3430a02/kgy/apps
~/pseudo   -> /scratch/x3430a02/kgy/pseudo
~/projects -> /scratch/x3430a02/kgy/projects
```

## 5. Project directory layout

```
/scratch/x3430a02/kgy/
├── apps/
│   ├── qe-gpu/bin/pw.x
│   ├── qe-cpu/bin/pw.x
│   └── LIGGGHTS-PUBLIC/src/lmp_mpi
├── pseudo/                            # SSSP efficiency PBE UPFs
├── lpscl16_site_pref/                 # Model C site preference study
├── manuscript_support/                # main paper calculations
│   ├── pipeline_v2/                   # v2 (annealing) pipeline
│   │   ├── comp1_v2/                  # DFT done
│   │   └── modelC_lpsc16/             # DFT EOS (basin B redo in progress)
│   ├── adhesion/                      # v5 xy-shift interfaces
│   ├── *.xyz                          # structure files
│   └── mlip_*_log.txt                 # MLIP calculation logs
├── md_results/                        # LAMMPS/LIGGGHTS MD outputs
├── projects/
│   ├── manuscript_support/  -> symlink
│   ├── SEI/
│   └── simulation/
├── SEI/                               # SEI-related calcs
├── root_scripts/
├── setup_neuron.sh                    # this setup script
└── setup.log                          # setup execution log
```

## 6. Standard run patterns

### QE GPU (single-point or relax)
```bash
QE=/scratch/x3430a02/kgy/apps/qe-gpu/bin/pw.x
export CUDA_VISIBLE_DEVICES=1
$QE -input relax.in > relax.out 2>&1
```
**Note:** no `mpirun -np 1` needed; pw.x-gpu is single-process by design for single GPU.

### QE CPU (parallel)
```bash
mpirun -np 8 pw.x -in input.in > output.out
```

### LIGGGHTS (DEM)
```bash
mpirun -np 8 lmp_mpi -in input.liggghts
```

### MLIP (MACE or UMA)
```bash
conda activate mace     # or uma
python script.py
```

### Background job (nohup)
```bash
nohup ./run.sh > run.log 2>&1 &
# or using the helper alias:
run_bg pw.x -in input.in
```

## 7. Login node limitations (observed)

- **Walltime limit ~several hours** then SIGKILL
- **Shared GPU** (A100); GPU 0 reserved for other users
- For long DFT jobs: use restart-safe wrapper scripts (`run_gpu*_redo.sh` with `restart_mode='restart'` when `tmp/<prefix>.save/` exists)
- Loop pattern (for walltime workaround): run → kill → restart → repeat until JOB DONE

## 8. SLURM batch (if used)

```bash
#!/bin/bash
#SBATCH -J modelC
#SBATCH -p amd_a100_8          # verify with: sinfo -s
#SBATCH --gres=gpu:2
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=2
#SBATCH -t 24:00:00
#SBATCH -o %x_%j.out
#SBATCH -e %x_%j.err

source /scratch/x3430a02/mjs0000/miniforge3/etc/profile.d/conda.sh
conda activate uma

QE=/scratch/x3430a02/kgy/apps/qe-gpu/bin/pw.x
# ... run logic identical to login-node scripts
```

Check queue:
```bash
sinfo -s
squeue -u $USER
scontrol show partitions
```

## 9. Pseudopotentials

Location:
```
/scratch/x3430a02/kgy/pseudo/
    li_pbe_v1_4_uspp_F.UPF
    P_pbe-n-rrkjus_psl_1_0_0.UPF
    s_pbe_v1_4_uspp_F.UPF
    cl_pbe_v1_4_uspp_F.UPF
    br_pbe_v1_4_uspp_F.UPF
    Ni.pbe-spn-rrkjus_psl_1_0_0.UPF
    O.pbe-n-rrkjus_psl_1_0_0.UPF
```

QE input reference:
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

## 10. Common tasks quick-reference

| Task | Command |
|------|---------|
| Activate UMA env | `conda activate uma` |
| Start QE relax (GPU1) | `CUDA_VISIBLE_DEVICES=1 pw.x -input relax.in > relax.out 2>&1` |
| Check QE progress | `grep "iteration\|Total force\|JOB DONE" relax.out \| tail` |
| GPU memory | `nvidia-smi --query-gpu=memory.used,memory.free --format=csv` |
| Kill all pw.x | `pkill -9 -f pw.x` |
| Continue after kill | `./run_gpu0_redo.sh` (auto restart from tmp) |
| Quick dir nav | `cds` (work root) / `cdp` (projects) |

## 11. Troubleshooting

**`command not found` in shell script**
→ pw.x not absolute path; use `QE=/scratch/x3430a02/kgy/apps/qe-gpu/bin/pw.x`

**`ModuleNotFoundError: numpy` on `python3`**
→ running outside conda env; `conda activate uma` first

**ASE reader `IndexError` on restart-merged relax.out**
→ multiple ATOMIC_POSITIONS blocks from restart_mode; use regex extraction of final `Begin final coordinates ... End final coordinates` block

**QE BM3 fit B₀ 4× too high**
→ wrong Birch-Murnaghan formula; correct form:
```python
eta = (V0/V)**(2/3)
E = E0 + 9*V0*B0/16 * ((eta-1)**2 * (6-4*eta) + Bp * (eta-1)**3)
```

**Volume-induced basin transitions during EOS scan**
→ compare `get_scaled_positions()` between adjacent volumes; if any atom Δfrac > 0.05 = basin change; re-run from reference basin champion coords using `v101_champion_frac.txt` + regex-rewritten relax.in (see `run_gpu*_redo.sh` pattern)

**Login-node job killed (walltime)**
→ tmp/ preserved; relaunch with `restart_mode='restart'` (scripts auto-detect); loop until converged

**libxc not found during QE CPU build**
→ known issue in this environment; use GPU QE instead, which links nvhpc's own math libs
