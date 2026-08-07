# kserver116-27 Server Setup (new lab server)

**Setup date:** 2026-04-23 | **Target host:** `121.78.116.27` | **OS:** Ubuntu 24.04.4 LTS

## Hardware

| Component | Spec |
|---|---|
| CPU | Intel Xeon Silver 4210R (10c/20t @ 2.4 GHz) |
| GPU | NVIDIA RTX A6000 48 GB (Ampere sm_86, driver 595.58.03) |
| RAM | 64 GB (2×32 GB DDR4-2933) |
| Storage | 480 GB SSD (`/`) + **3.6 TB HDD (`/data`)** |
| Network | Public IP, baremetal (not VM) |

## Installed Stack

### DFT / QM
| Tool | Version | Notes |
|---|---|---|
| QE CPU | 7.4.1 | `pw.x pp.x ph.x ev.x projwfc.x dos.x bands.x matdyn.x` (50+ binaries, apt libxc/fftw/blas) |
| QE GPU | 7.4.1 | Built with nvhpc 24.11, `cc86` + CUDA 12.6 + OpenACC + cuFFT/cuBLAS/cuSOLVER. Activate via `qegpu` function |
| ORCA | 6.1.1 | AVX non-AVX2 shared OpenMPI-4.1.8 build (runs fine on our OpenMPI 4.1.6). Serial + MPI PAL OK. Parallel requires full path `/data/apps/orca-6.1.1/orca` |
| thermo_pw | — | **SKIPPED** (gfortran 13 OpenMP-`collapse(4)` incompatibility; use manual `pw.x` finite-strain for Cij) |

### MD
| Tool | Version | Notes |
|---|---|---|
| LAMMPS | 30 Mar 2026 (release) | MANYBODY / GRANULAR / REAXFF / ML-SNAP / ML-PACE / KSPACE / RIGID / MOLECULE / MC / PYTHON / EXTRA-* |
| LIGGGHTS-PUBLIC | 3.8.0 | `lmp_mpi` (VTK flag stripped for Ubuntu 24.04 compat) |

### MLIP (3 conda envs)
| Env | torch | Model | Notes |
|---|---|---|---|
| `mace` | 2.5.1 + cu121 | MACE-MP-0 (small) | ~50 MB model, auto-download on first use |
| `uma` | 2.8.0 + cu128 | uma-s-1p1 (facebook/UMA, gated) | 1.1 GB, **manually placed in `~/.cache/fairchem/`**, `HF_HUB_OFFLINE=1` set. refs YAMLs auto-fetched |
| `sevennet` | 2.5.1 + cu121 | SevenNet-0 | Korean-dev MLIP (used by Choi2025 adhesion paper) |

### Analysis
| Tool | Version | Purpose |
|---|---|---|
| LOBSTER | 5.1.1 | COHP / COOP / ICOHP (20-thread auto) |
| CRITIC2 | latest git | Topology + Bader + NCI + ELF |
| Bader | 1.05 (Henkelman) | Charge analysis |
| Phono3py | 3.30.1 | Anharmonic phonon / thermal conductivity |

### Python
| Env | Purpose | Key packages |
|---|---|---|
| `base` | — | miniforge3 base |
| `dft` | DFT analysis | pymatgen 2026.3.23, ase 3.28, phonopy 3.5, phono3py 3.30, spglib 2.7, seekpath 2.2, chgnet 0.4, nglview 4.0, atomate2 0.1, jobflow, custodian, MDAnalysis 2.10 |
| `mace`, `uma`, `sevennet` | MLIP runtime | see above |

### Pseudopotentials
- `$PSEUDO_DIR = /data/work/pseudo` (SSSP 1.3.0 PBE efficiency, 103 elements)
- All 8 study elements confirmed: Li, P, S, Cl, Br, Ni, O, **Nd** (PAW f-electron Wentzcovitch)

### Utilities
`ncdu`, `parallel`, `iftop`, `tmux`, `rsync`, `unzip` — apt installed

## Key Paths

| Path | Content |
|---|---|
| `/data/apps/` | All binaries (QE / LAMMPS / LIGGGHTS / ORCA / LOBSTER / CRITIC2 / Bader / nvhpc / miniforge3) |
| `/data/apps/miniforge3/envs/` | 4 conda envs |
| `/data/work/pseudo/` | SSSP + Nd PPs (`$PSEUDO_DIR`) |
| `/data/work/bml/` | KISTI-synced structures (CIF, xyz) |
| `/data/work/repo/` | `Yonghoon-DEM-DFT` clone on branch `claude/argyrodite-ml-migration-kDtHW` |
| `~/.cache/fairchem/` | UMA checkpoint cache (HF gated) |

## Usage Cheatsheet

```bash
# DFT crystal (CPU)
mpirun -np 20 pw.x -in scf.in > scf.out

# DFT crystal (GPU) — 10× speedup for small cells
qegpu              # activation function (sets nvhpc + QE-GPU PATH)
mpirun -np 1 pw.x -in scf.in > scf.out

# DFT molecular
/data/apps/orca-6.1.1/orca input.inp > output.out    # full path for MPI!

# MD
mpirun -np 20 lmp -in input.lammps        # LAMMPS
mpirun -np 20 lmp_mpi -in input.liggghts  # LIGGGHTS (DEM)

# MLIP (Python)
conda activate uma        # or mace / sevennet
python script.py

# ★ 일상 python/ase/변환 작업도 'uma' env 사용 (사용자 표준, 2026-07-08)
#   ase는 uma env에 포함(fairchem 의존) — 'dft' env 말고 uma로 통일할 것
conda activate uma

# Analysis
conda activate dft
jupyter notebook          # with nglview viz
lobster                   # in QE output dir
bader charge.cube
critic2 input.cri

# Utility
ncdu /data                # disk usage TUI
```

## Environment Variables (`~/.bashrc`)

Critical globals:
```
CUDA_HOME=/usr/local/cuda-12.6
PSEUDO_DIR=/data/work/pseudo
HF_HUB_OFFLINE=1                     # UMA offline
OMPI_ALLOW_RUN_AS_ROOT=1             # OpenMPI allows root (dedicated server)
OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
```

`qegpu()` function switches to GPU QE with nvhpc toolchain (separate from CPU default).

## Gotchas

1. **ORCA parallel** requires **full binary path** (not symlink / alias) — ORCA checks this internally.
2. **UMA model** is gated on HuggingFace (`facebook/UMA`). Checkpoint `uma-s-1p1.pt` must be pre-placed at `~/.cache/fairchem/models--facebook--UMA/snapshots/be2896459a03fcde05e20d2fcefd11f450601fce/checkpoints/`. refs YAMLs auto-downloaded on first run (login needed once).
3. **thermo_pw** incompatible with gfortran 13 (OpenMP collapse bug). Use manual finite-strain protocol from `db/inputs/qe_templates/elastic_strain.in`.
4. **KISTI outbound SSH blocked** from login nodes. Data sync requires WSL relay (download to local → push to server).
5. **QE GPU build** is in `/data/apps/qe-7.4.1-gpu` (separate from CPU build `/data/apps/qe-7.4.1-cpu`). Do not mix PATHs.

## Comparison vs KISTI Neuron

| Property | KISTI Neuron | kserver116-27 |
|---|---|---|
| CPU | (login node varies) | Xeon 4210R 20t |
| GPU | A100 80 GB | A6000 48 GB |
| Shared / Dedicated | Shared, quota-limited | **Dedicated, no walltime** |
| Storage | `/scratch` shared | `/data` 3.4 TB dedicated |
| Network | KREN inside, SSH outbound blocked | Public IP |
| Walltime | ~hours, SIGKILL | Unlimited (no job manager) |
| QE GPU speed | A100 ~2× A6000 for DFT (FP64) | A6000 OK for ≤200 atoms |
| MLIP speed | similar (FP32 bound) | similar |

Expected usage: **MLIP + small/medium DFT** on new server, large DFT (adhesion 820-atom) continues on KISTI.

## ⚠ QE 추가 도구를 빌드할 때 — mpifort 가 gfortran 을 부른다 (2026-08-07 실측)

`neb.x` 를 만들려고 `make neb` 를 했더니 이렇게 죽었다:

```
gfortran: error: unrecognized command-line option '-fast'
gfortran: error: unrecognized command-line option '-cuda'
gfortran: error: unrecognized debug output level 'pu=cc86,cuda12.6'
```

원인은 **PATH**다. 기본 `which mpifort` 가 `/usr/bin/mpifort` = GNU Fortran 13.3.0 을
가리키는데, QE-GPU 는 NVHPC(`nvfortran`)로 빌드돼 있어 `make.inc` 의 플래그가
NVHPC 전용이다. gfortran 이 그걸 못 알아듣는다.

**빌드 전에 반드시 이 환경을 복원한다** (run_sei_dft.sh 가 실행 시 쓰는 것과 같은 것):

```bash
NVHPC=/data/apps/nvhpc/Linux_x86_64/24.11
export PATH=$NVHPC/comm_libs/12.6/hpcx/hpcx-2.20/ompi/bin:$NVHPC/compilers/bin:$PATH
export OPAL_PREFIX=$NVHPC/comm_libs/12.6/hpcx/hpcx-2.20/ompi
export LD_LIBRARY_PATH=$NVHPC/compilers/lib:/usr/local/cuda-12.6/lib64:$LD_LIBRARY_PATH

which mpifort                       # hpcx 경로여야 한다
mpifort --version | head -1         # nvfortran 이어야 한다
```

⚠ **QE-GPU 빌드에 `neb.x` 가 처음부터 없다.** `bin/` 은 `PW/src`·`PP/src` 로 가는
심볼릭 링크 모음인데 NEB 은 빌드 대상에 안 들어 있었다. `libpw.a` 는 이미 있으므로
`make neb` 는 NEB 모듈만 컴파일한다(2~5분).

⚠ 판정 기준: `make.inc` 의 `MPIF90` 이 원래 빌드에 쓴 컴파일러다. 그게 지금 PATH 에서
잡히는지가 전부다 —
```bash
grep -E "^(MPIF90|F90|CC|LD)\s*=" /data/apps/qe-7.4.1-gpu/make.inc
```
