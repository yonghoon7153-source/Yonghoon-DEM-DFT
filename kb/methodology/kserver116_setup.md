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
