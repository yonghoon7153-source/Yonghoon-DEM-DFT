# esp-Z590-AORUS-MASTER Server Setup (new home/lab server)

**Setup date:** 2026-07-01 | **Target host:** `59.12.161.91` (ssh `kgy@59.12.161.91`) | **OS:** Ubuntu 20.04.6 LTS (focal), kernel 5.15

> Companion install script: `setup/new_server_esp_setup.sh` (labeled Phase 1–9 blocks a human pastes one at a time). This doc is the canonical record; the script is the paste source.

## Hardware

| Component | Spec |
|---|---|
| CPU | Intel Core i9-11900K (8c/16t, Rocket Lake) |
| GPU | NVIDIA GeForce RTX 3090 24 GB (Ampere **sm_86 / cc86**, driver 560.35.03, CUDA 12.6) |
| RAM | ~32 GB (build with `-j8`, not `-j16`, to avoid OOM on C++ compiles) |
| Storage | **916 GB single SSD on `/` (823 G free). NO `/data` partition** |
| Network | Home/lab IP, baremetal |

**Consequence of no `/data`:** everything installs under `$HOME` (`/home/kgy`):
- apps/binaries -> `~/apps`
- work/data/inputs -> `~/work`
- model/pseudo caches -> `~/.cache`, `~/work/pseudo`

**Permissions:** user `kgy`, **sudo REQUIRES A PASSWORD** (not root, not passwordless). Only Phase 1 (apt) needs sudo; everything else is pure `$HOME`.

## Installed Stack

### DFT / QM
| Tool | Version | Path | Notes |
|---|---|---|---|
| QE CPU | 7.4.1 | `~/apps/qe-7.4.1-cpu/bin` | gfortran-9 + apt OpenMPI 4.0.3 + apt ScaLAPACK. **`--without-libxc`** (20.04 apt libxc 4.x too old); internal PBE. Six programs: `pw.x pp.x ph.x epsilon.x dos.x projwfc.x` |
| QE GPU | 7.4.1 | `~/apps/qe-7.4.1-gpu/bin` | nvhpc 24.11, `cc86` + CUDA 12.6 (SDK-bundled) + OpenACC + cuFFT/cuBLAS/cuSOLVER. Activate via `qegpu`. **`pw.x`/`pp.x` only — no `ph.x`** |
| ORCA | 6.1.1 | `~/apps/orca-6.1.1` | Precompiled tree **rsync'd from gabia**. Linked to OpenMPI 4.1.x -> needs source-built OpenMPI 4.1.6 (below). Parallel requires **full path** `~/apps/orca-6.1.1/orca` |
| OpenMPI (for ORCA) | 4.1.6 | `~/apps/openmpi-4.1.6` | **Built from source** into `$HOME` (apt 4.0.3 is the wrong minor series for ORCA) |

### MLIP
| Env | torch | Model | Notes |
|---|---|---|---|
| `uma` | 2.8.0 + cu128 | uma-s-1p1 (facebook/UMA, gated) | 1.1 GB, **rsync'd from gabia into `~/.cache/fairchem/`**, `HF_HUB_OFFLINE=1`. Import is `fairchem.core` (NOT `fairchem_core`). fairchem-core pins `torch~=2.8.0` (matches installed) |

### Python (conda / miniforge3 at `~/apps/miniforge3`)
| Env | Purpose | Key packages |
|---|---|---|
| `base` | — | miniforge3 base |
| `dft` | DFT analysis | pymatgen, ase, mp_api (python 3.11) |
| `uma` | MLIP runtime | torch 2.8.0+cu128, fairchem-core, pymatgen, ase, mp_api (python 3.11) |

### Pseudopotentials
- `$PSEUDO_DIR = ~/work/pseudo` — SSSP 1.3.0 PBE + Nd PP, **rsync'd from gabia** `/data/work/pseudo`.

## Key Paths (all under HOME — no `/data`)

| Path | Content |
|---|---|
| `~/apps/qe-7.4.1-cpu/bin` | QE CPU binaries (`pw.x pp.x ph.x epsilon.x dos.x projwfc.x`) |
| `~/apps/qe-7.4.1-gpu/bin` | QE GPU binaries (`pw.x pp.x` — SCF/nscf/relax/NEB only) |
| `~/apps/nvhpc/Linux_x86_64/24.11` | NVIDIA HPC SDK (compilers, bundled CUDA 12.6, HPC-X OpenMPI, math_libs) |
| `~/apps/orca-6.1.1` | ORCA 6.1.1 precompiled tree + `orca_env.sh` |
| `~/apps/openmpi-4.1.6` | Source-built OpenMPI 4.1.6 (for ORCA) |
| `~/apps/miniforge3/envs/` | conda envs `dft`, `uma` |
| `~/work/pseudo` | SSSP 1.3.0 PBE + Nd PP (`$PSEUDO_DIR`) |
| `~/work/bml` | structures (CIF, xyz) synced from gabia |
| `~/work/Yonghoon-DEM-DFT` | repo clone (branch `claude/friendly-meitner-lldvar`) |
| `~/.cache/fairchem/` | UMA checkpoint cache (gated, offline) |

## Environment Variables (`~/.bashrc`)

```
PATH             += ~/apps/qe-7.4.1-cpu/bin      # CPU pw.x etc.
PSEUDO_DIR        = ~/work/pseudo
ESPRESSO_PSEUDO   = ~/work/pseudo                # alt name some QE tools read
HF_HUB_OFFLINE    = 1                            # UMA offline (never hit HF)
MP_API_KEY        = <paste your own, NOT committed>
NVVER             = 24.11
NV                = ~/apps/nvhpc/Linux_x86_64/24.11
CUDA_HOME         = $NV/cuda/12.6                # nvhpc-bundled CUDA 12.6
```

- `~/apps/orca-6.1.1/orca_env.sh` is sourced from `~/.bashrc`: puts **OpenMPI 4.1.6 first** on `PATH`/`LD_LIBRARY_PATH`, then the ORCA tree.
- `qegpu()` function switches THIS shell to the GPU-QE toolchain: sets `OPAL_PREFIX` (HPC-X ompi), `MPIRUN` (HPC-X mpirun), `QEGPU` bin, and puts `$NV/compilers/lib` **first** on `LD_LIBRARY_PATH` (kills `libgomp: TODO`). Run `conda deactivate` before calling it.

## Usage Cheatsheet

```bash
# DFT crystal (CPU) — MPI + OpenMP
mpirun -np 4 pw.x -in scf.in > scf.out

# Phonons / DFPT / epsilon — CPU BUILD ONLY (GPU ph.x crashes 'libgomp: TODO')
mpirun -np 4 ~/apps/qe-7.4.1-cpu/bin/ph.x      -in ph.in      > ph.out
mpirun -np 4 ~/apps/qe-7.4.1-cpu/bin/epsilon.x -in eps.in     > eps.out

# DFT crystal (GPU) — scf/nscf/relax/vc-relax/NEB only, 1 rank = 1 GPU
conda deactivate            # FIRST — avoid conda libgomp shadowing NVHPC's
qegpu                       # sets HPC-X mpirun + NVHPC libs + QE-GPU PATH
$MPIRUN -np 1 $QEGPU/pw.x -npool 1 -in scf.in > scf.out 2>&1

# DFT molecular (ORCA) — FULL PATH for parallel, cores set INSIDE the .inp
~/apps/orca-6.1.1/orca input.inp > output.out     # '%pal nprocs N end' in .inp; do NOT use mpirun

# MLIP (UMA)
conda activate uma
export HF_HUB_OFFLINE=1
python tools/modelc_v3/uma_smoke.py db/structures/b2o3_relaxV0.xyz cuda

# Pull fresh artifacts from gabia
rsync -a --info=progress2 --partial root@121.78.116.27:/data/work/pseudo/ ~/work/pseudo/
```

## Gotchas

1. **No external libxc (both QE builds).** Ubuntu 20.04 apt libxc is 4.x — too old for QE 7.4.1 `--with-libxc`. Build with `--without-libxc`; QE's internal PBE matches the SSSP-PBE pseudos, so results are unaffected.
2. **ORCA needs OpenMPI 4.1.x, not apt 4.0.3.** ORCA 6.1.1 is linked against OpenMPI 4.1.8 and requires the 4.1.x series (PMIx/launcher ABI differs from 4.0.3). Build OpenMPI **4.1.6** from source into `$HOME` (proven-good on gabia) and keep it first on `PATH`/`LD_LIBRARY_PATH`. Never let apt OpenMPI shadow it.
3. **Parallel ORCA = FULL ABSOLUTE PATH, never `mpirun`.** `~/apps/orca-6.1.1/orca job.inp`. ORCA spawns MPI itself and needs the full path to find its worker sub-executables (`orca_scf`, `orca_gtoint`, …). Set cores with `%pal nprocs N end` inside the `.inp`. Wrapping ORCA in `mpirun` double-launches MPI and fails.
4. **`ph.x` / DFPT is NOT in the GPU build.** GPU `pw.x` is fine for scf/nscf/relax/vc-relax/NEB, but `ph.x` / `epsilon.x` (DFPT path) crash with `libgomp: TODO` or hang (this is exactly the KISTI epsil hang). Do all phonons / `ph.x` / `epsilon.x` on the **CPU build** with the system `mpirun`.
5. **`libgomp: TODO` abort = wrong OpenMP runtime loaded.** Two triggers: (a) a conda env is active (its GNU libgomp shadows NVHPC's) — `conda deactivate` before GPU runs; (b) `LD_LIBRARY_PATH` order — `$NV/compilers/lib` must come first. `qegpu()` handles (b); you do (a).
6. **GPU launcher must be NVHPC's HPC-X mpirun**, not `/usr/bin/mpirun` (apt 4.0.3). The GPU `pw.x` is linked to the SDK's HPC-X OpenMPI. `qegpu()` sets `$MPIRUN` and `OPAL_PREFIX` (or HPC-X can't find its runtime help files).
7. **cc86, not cc80.** RTX 3090 is Ampere sm_86. Do NOT copy KISTI/A100 `cc80` settings. gabia's A6000 is also sm_86, so its build settings port directly.
8. **After rsync'ing nvhpc from gabia, re-run `makelocalrc`** against THIS box's gcc/gfortran-9, or nvfortran picks up gabia's gcc-13 paths and fails. (A fresh tarball install writes localrc automatically; re-running is harmless.)
9. **UMA is gated + offline.** `HF_HUB_OFFLINE=1` fetches nothing from HuggingFace, so rsync the **ENTIRE** `~/.cache/fairchem/models--facebook--UMA` tree (blobs/ + snapshots/ + refs/), not just `checkpoints/`. Use `rsync -a` (preserves the snapshots→blobs symlinks); do NOT use `-L`/`--copy-links`. Snapshot hash on gabia: `be2896459a03fcde05e20d2fcefd11f450601fce` — ls the dir after copy and use whatever hash is present.
10. **fairchem import is `fairchem.core`** (NOT `fairchem_core`). Repo scripts import `FAIRChemCalculator` from `fairchem.core.calculate.ase_calculator`; keep that path. `task_name='omat'` for inorganic solids (wrong task silently gives wrong energies, not an error).
11. **RTX 3090 24 GB vs gabia A6000 48 GB.** Single-point / relax fit easily, but large UMA MD supercells (>~1500 atoms) that fit on gabia may OOM here — shrink the cell or batch.
12. **Build with `-j8`, not `-j16`.** i9-11900K has 8 physical cores; QE builds can race on `.mod` deps and OpenMPI's C++ compiles can OOM the ~32 GB RAM at `-j16`. If a parallel QE build races, just re-run `make pw pp ph` serially.
13. **`--with-cuda` = the CUDA TOOLKIT path**, which for nvhpc is the SDK-bundled `$NV/cuda/12.6` (`NVHPC_CUDA_HOME`), NOT `/usr/local/cuda` (there is no standalone CUDA on this box). This keeps cuFFT/cuBLAS/cuSOLVER matched to nvfortran 24.11.
14. **No secrets in the repo.** `~/.bashrc` ships an `MP_API_KEY` placeholder; paste your real key locally. It is read via `os.environ['MP_API_KEY']` and never printed.
15. **Don't mix QE PATHs / MPIs in one shell.** CPU-QE (apt OpenMPI 4.0.3), GPU-QE (`qegpu`, HPC-X), and ORCA (source OpenMPI 4.1.6) each want their own MPI first on PATH. Use a fresh shell (or re-source the relevant env) when switching.

## Comparison vs gabia (kserver116-27)

| Property | gabia / kserver116 | esp-Z590-AORUS-MASTER |
|---|---|---|
| OS | Ubuntu 24.04.4 LTS | Ubuntu 20.04.6 LTS (focal) |
| CPU | Xeon 4210R (10c/20t) | i9-11900K (8c/16t) |
| GPU | RTX A6000 48 GB (sm_86) | RTX 3090 24 GB (sm_86) |
| CUDA / driver | 12.6 / 595.58.03 | 12.6 / 560.35.03 |
| Storage | 480 GB SSD + 3.6 TB `/data` | 916 GB SSD only (all under `$HOME`) |
| Install root | `/data/apps`, `/data/work` | `~/apps`, `~/work` |
| sudo | root | `kgy`, **password required** |
| libxc | apt libxc (24.04, usable) | apt libxc 4.x **too old -> `--without-libxc`** |
| ORCA MPI | OpenMPI 4.1.6 (present) | **source-built** OpenMPI 4.1.6 (apt is 4.0.3) |
| nvhpc | 24.11 native | 24.11 (rsync'd from gabia, `makelocalrc` re-run) |
| Role of artifacts | canonical source | **rsync consumer** (ORCA/UMA/pseudos/structures pulled from gabia) |

Expected usage: **MLIP + small/medium DFT (GPU pw.x) + molecular ORCA** on esp. Phonons/DFPT/epsilon on the esp CPU build; large DFT continues on gabia/KISTI.
