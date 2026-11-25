#!/usr/bin/env bash
##############################################################################
# setup/new_server_esp_setup.sh
#
# Setup record + PASTE-BY-PHASE install script for the NEW lab server
#   host  : esp-Z590-AORUS-MASTER
#   ssh   : kgy@59.12.161.91   (user 'kgy', HOME=/home/kgy)
#   OS    : Ubuntu 20.04.6 LTS (focal), kernel 5.15
#   CPU   : Intel i9-11900K (8c/16t)
#   GPU   : NVIDIA RTX 3090 24GB, Ampere sm_86 / cc86, driver 560.35.03, CUDA 12.6
#   disk  : 916GB on /  (823G free). NO /data partition -> EVERYTHING under $HOME
#           apps  -> ~/apps      work/data -> ~/work
#
# Reference/donor box "gabia / kserver116":
#   ssh   : root@121.78.116.27  (password/key auth; passwordless key from esp set)
#   holds : QE-CPU+GPU, ORCA 6.1.1 (/data/apps/orca-6.1.1), nvhpc 24.11
#           (/data/apps/nvhpc/Linux_x86_64/24.11), UMA checkpoint
#           (/root/.cache/fairchem), SSSP+Nd pseudos (/data/work/pseudo),
#           structures (/data/work/bml).
#
# HOW TO USE THIS FILE:
#   This is NOT a run-it-all script. It is a set of clearly labeled PHASES.
#   A human pastes ONE phase (or ONE sub-block) at a time into a shell on esp,
#   waits for it to finish, eyeballs the output, then moves on. Blocks are
#   tolerant of sudo-with-password (they will prompt), and contain no secrets
#   (MP_API_KEY is a placeholder you edit locally).
#
#   Phase 1  apt base .......................... DONE (recorded for the record)
#   Phase 2  miniforge3 + conda envs dft/uma ... DONE
#   Phase 3  repo clone ........................ DONE
#   Phase 4  QE 7.4.1 CPU build ................ paste
#   Phase 5  QE 7.4.1 GPU build (nvhpc 24.11) .. paste
#   Phase 6  ORCA 6.1.1 + OpenMPI 4.1.6 ........ paste
#   Phase 7  rsync portable artifacts from gabia paste
#   Phase 8  ~/.bashrc environment block ....... paste
#   Phase 9  end-to-end verification (V0..V6) .. paste
#
# KEY CONSTRAINTS (read once):
#   * Ubuntu 20.04 apt libxc is 4.x -> TOO OLD for QE 7.4.1 --with-libxc.
#     Build QE (CPU and GPU) with --without-libxc; QE internal PBE matches SSSP-PBE.
#   * ORCA 6.1.1 is linked to OpenMPI 4.1.x. apt OpenMPI here is 4.0.3 (WRONG minor
#     series) -> build OpenMPI 4.1.6 from source into $HOME for ORCA.
#   * ph.x / DFPT / epsilon(DFPT) is NOT reliable in the QE GPU build ('libgomp: TODO').
#     Do phonons / ph.x / epsilon.x on the CPU build. GPU pw.x = scf/nscf/relax/NEB only.
#   * 'libgomp: TODO' abort = GNU libgomp shadowed NVHPC's OpenMP. Fix: conda deactivate
#     before GPU runs AND put $NV/compilers/lib FIRST on LD_LIBRARY_PATH (qegpu() does this).
#   * Parallel ORCA MUST be launched by its FULL ABSOLUTE PATH, never via mpirun,
#     and core count is set INSIDE the .inp via '%pal nprocs N end'.
##############################################################################


##############################################################################
# PHASE 1 — apt base packages                                    [ALREADY DONE]
##############################################################################
# Recorded for reproducibility. sudo on this box REQUIRES A PASSWORD (user is
# not root, not passwordless) — the apt line will prompt. Do NOT re-run unless
# rebuilding the box.
#
#   sudo apt update
#   sudo apt install -y \
#     build-essential gfortran gcc g++ make cmake git \
#     libfftw3-dev libblas-dev liblapack-dev \
#     libopenmpi-dev openmpi-bin libscalapack-openmpi-dev \
#     tmux rsync wget curl bzip2 ca-certificates
#
# Resulting toolchain: gfortran-9, apt OpenMPI 4.0.3, apt ScaLAPACK.
# (apt OpenMPI 4.0.3 is fine for QE-CPU; it is NOT usable for ORCA — see Phase 6.)


##############################################################################
# PHASE 2 — miniforge3 + conda envs                              [ALREADY DONE]
##############################################################################
# Recorded for reproducibility.
#   miniforge3 installed at ~/apps/miniforge3
#   env 'dft' (python 3.11): pymatgen / ase / mp_api  (DFT analysis)
#   env 'uma' (python 3.11): torch 2.8.0+cu128 (cuda True, sees RTX 3090),
#                            pymatgen / ase / mp_api, fairchem-core (import 'fairchem.core')
#
# Activation for later phases:
#   source ~/apps/miniforge3/etc/profile.d/conda.sh
#   conda activate uma
#   python -c "import torch;print(torch.__version__,torch.cuda.is_available(),torch.cuda.get_device_name(0))"
#   # expect: 2.8.0+cu128 True NVIDIA GeForce RTX 3090


##############################################################################
# PHASE 3 — repo clone                                           [ALREADY DONE]
##############################################################################
# Recorded for reproducibility.
#   ~/work/Yonghoon-DEM-DFT   (branch claude/friendly-meitner-lldvar)
#   Passwordless SSH key esp -> gabia (root@121.78.116.27) is configured.


##############################################################################
# PHASE 4 — QE 7.4.1 CPU build (gfortran-9 + apt OpenMPI 4.0.3 + apt ScaLAPACK)
#   internal PBE functionals (NO external libxc); install -> ~/apps/qe-7.4.1-cpu
#   Builds the six required programs: pw.x pp.x ph.x epsilon.x dos.x projwfc.x
#   Paste block-by-block.
##############################################################################

# --- 4.0 Sanity: confirm apt deps already present (Phase 1 installed them)
which mpif90 mpicc gfortran make cmake
dpkg -l | grep -E 'libscalapack-openmpi-dev|libfftw3-dev|libblas-dev|liblapack-dev|libopenmpi-dev' | awk '{print $2, $3}'
# Expect mpif90 -> /usr/bin/mpif90 (OpenMPI 4.0.3) and all 5 packages listed.

# --- 4.1 Fetch + unpack QE 7.4.1 source (extracts to q-e-qe-7.4.1/  <- double 'qe')
mkdir -p ~/apps/src && cd ~/apps/src
wget -c "https://gitlab.com/QEF/q-e/-/archive/qe-7.4.1/q-e-qe-7.4.1.tar.gz" -O q-e-qe-7.4.1.tar.gz
tar xzf q-e-qe-7.4.1.tar.gz
cd ~/apps/src/q-e-qe-7.4.1

# --- 4.2 Configure: MPI + OpenMP + apt ScaLAPACK, internal PBE (no libxc)
#     Make sure NO conda env is active (conda libgomp/mpi can shadow apt's).
conda deactivate 2>/dev/null; conda deactivate 2>/dev/null
export OMPI_FC=gfortran OMPI_CC=gcc
./configure \
  --enable-parallel \
  --enable-openmp \
  --with-scalapack=yes \
  --without-libxc \
  MPIF90=mpif90 CC=mpicc F77=mpif90 \
  --prefix=$HOME/apps/qe-7.4.1-cpu \
  2>&1 | tee ~/apps/src/qe-cpu-configure.log

# --- 4.3 VERIFY configure picked the right libs BEFORE building (read make.inc)
grep -E '^(DFLAGS|BLAS_LIBS|LAPACK_LIBS|SCALAPACK_LIBS|FFT_LIBS|MPIF90|F90FLAGS)' make.inc
#   MUST show:  -D__MPI  -D__SCALAPACK  and OpenMP (-D__OPENMP or -fopenmp in F90FLAGS).
#   SCALAPACK_LIBS must be non-empty (-lscalapack-openmpi ... from apt).
#   If -D__SCALAPACK is MISSING, stop and re-check the apt scalapack dev pkg.

# --- 4.4 Build the six required programs. Targets:
#         pw -> pw.x ;  pp -> pp.x,dos.x,projwfc.x,epsilon.x ;  ph -> ph.x
#     Use -j8 (i9-11900K = 8 physical cores; higher -j can race on .mod deps).
make -j8 pw pp ph 2>&1 | tee ~/apps/src/qe-cpu-make.log

# --- 4.5 Install into the prefix (populates ~/apps/qe-7.4.1-cpu/bin)
make install 2>&1 | tee ~/apps/src/qe-cpu-install.log
#   FALLBACK if `make install` misbehaves on this QE version — the .x files
#   already exist in the source bin/:
#     mkdir -p ~/apps/qe-7.4.1-cpu/bin && cp ~/apps/src/q-e-qe-7.4.1/bin/*.x ~/apps/qe-7.4.1-cpu/bin/

# --- 4.6 VERIFY: all six binaries exist and pw.x is MPI+OpenMP
ls -la ~/apps/qe-7.4.1-cpu/bin/{pw.x,pp.x,ph.x,epsilon.x,dos.x,projwfc.x}
~/apps/qe-7.4.1-cpu/bin/pw.x --version 2>&1 | head -3     # "Program PWSCF v.7.4.1"
mpirun -np 2 ~/apps/qe-7.4.1-cpu/bin/pw.x -in /dev/null 2>&1 | grep -Ei 'MPI process|Threads|Parallel version'
#   Expect: "Parallel version (MPI & OpenMP), running on 2 processor cores".
ldd ~/apps/qe-7.4.1-cpu/bin/pw.x | grep -Ei 'gomp|scalapack|fftw3|blas|lapack|mpi'
# NOTE: PATH for pw.x is wired in Phase 8 (~/.bashrc). PSEUDO_DIR comes in Phase 7/8.


##############################################################################
# PHASE 5 — QE 7.4.1 GPU build (nvhpc 24.11 SDK, RTX 3090 cc86, CUDA 12.6)
#   nvhpc SDK -> ~/apps/nvhpc ; QE -> ~/apps/qe-7.4.1-gpu . NO sudo needed.
#   GPU pw.x = scf/nscf/relax/vc-relax/NEB ONLY. Do ph.x/epsilon.x on the CPU build.
#   Paste block-by-block.
##############################################################################

# --- 5.0 Prep dirs + GPU sanity
mkdir -p ~/apps ~/work/src
nvidia-smi --query-gpu=name,driver_version,compute_cap --format=csv,noheader
# expect: NVIDIA GeForce RTX 3090, 560.35.03, 8.6   -> cc86 confirmed

# --- 5.1a OPTION A (preferred): rsync the already-working nvhpc SDK from gabia
#          (skips the ~11 GB download; gabia's SDK is proven on the same sm_86 class).
mkdir -p ~/apps/nvhpc
rsync -aP --info=progress2 \
  root@121.78.116.27:/data/apps/nvhpc/Linux_x86_64 \
  ~/apps/nvhpc/
# Result: ~/apps/nvhpc/Linux_x86_64/24.11/{compilers,cuda,math_libs,comm_libs,...}
# nvhpc is relocatable BUT its localrc bakes the old prefix -> re-run makelocalrc in 5.3.

# --- 5.1b OPTION B (only if you do NOT want the gabia rsync): fresh NVIDIA download.
#          NOTE: NVIDIA's CDN 403s through datacenter proxies; a home/lab IP is usually fine.
# cd ~/work/src
# wget https://developer.download.nvidia.com/hpc-sdk/24.11/nvhpc_2024_2411_Linux_x86_64_cuda_12.6.tar.gz
# tar xpzf nvhpc_2024_2411_Linux_x86_64_cuda_12.6.tar.gz
# NVHPC_SILENT=true NVHPC_INSTALL_DIR="$HOME/apps/nvhpc" NVHPC_INSTALL_TYPE=single \
#   ./nvhpc_2024_2411_Linux_x86_64_cuda_12.6/install
# # -> installs to ~/apps/nvhpc/Linux_x86_64/24.11 (no sudo; 'single' = local install)

# --- 5.2 Pin the nvhpc prefix and load its env for THIS build shell
export NV=$HOME/apps/nvhpc/Linux_x86_64/24.11
export NVHPC_CUDA_HOME=$NV/cuda/12.6          # SDK-bundled CUDA 12.6 toolkit
export PATH=$NV/compilers/bin:$NV/cuda/12.6/bin:$PATH
export MANPATH=$NV/compilers/man:$MANPATH
export LD_LIBRARY_PATH=$NV/compilers/lib:$NV/cuda/12.6/lib64:$NV/math_libs/lib64:$LD_LIBRARY_PATH
nvfortran --version    # expect: nvfortran 24.11-0 ...  (>= 21.7 required by QE)
nvcc --version         # expect: Cuda compilation tools, release 12.6

# --- 5.3 Regenerate the SDK localrc for THIS machine's gcc + THIS GPU (cc86).
#         MANDATORY after an rsync move (otherwise nvfortran picks up gabia's gcc-13 paths).
$NV/compilers/bin/makelocalrc $NV/compilers/bin \
    -x -gcc $(which gcc) -gpp $(which g++) -g77 $(which gfortran)
# self-test that the toolchain sees the GPU:
echo 'program p; print *,"nvfortran ok"; end program' > /tmp/t.f90
nvfortran -acc -gpu=cc86,cuda12.6 /tmp/t.f90 -o /tmp/t && /tmp/t

# --- 5.4 Fetch QE 7.4.1 source (separate tree from the CPU build)
cd ~/work/src
wget -O qe-7.4.1.tar.gz \
  https://gitlab.com/QEF/q-e/-/archive/qe-7.4.1/q-e-qe-7.4.1.tar.gz
tar xzf qe-7.4.1.tar.gz
mv q-e-qe-7.4.1 qe-7.4.1-gpu-src
cd qe-7.4.1-gpu-src

# --- 5.5 Configure QE for GPU. SDK compilers + HPC-X mpifort; SDK-bundled CUDA 12.6.
#         cc86 = RTX 3090 Ampere. --with-cuda-mpi=no because HPC-X here isn't CUDA-aware.
export MPIF90=$NV/comm_libs/12.6/hpcx/hpcx-2.20/ompi/bin/mpifort
./configure \
    --with-cuda=$NVHPC_CUDA_HOME \
    --with-cuda-cc=86 \
    --with-cuda-runtime=12.6 \
    --with-cuda-mpi=no \
    --enable-openmp \
    --prefix=$HOME/apps/qe-7.4.1-gpu \
    FC=nvfortran F90=nvfortran CC=nvc MPIF90=$MPIF90 \
    2>&1 | tee ~/work/src/qe-gpu-configure.log
# sanity: confirm GPU flags landed in make.inc
grep -E 'GPU_ARCH|CUDA_RUNTIME|DGPU|-acc|-cuda' make.inc | head

# --- 5.6 Build pw.x (+ pp.x). If a parallel .mod race hits, re-run serially.
make -j8 pw pp 2>&1 | tee ~/work/src/qe_gpu_build.log
#   on a .mod dependency race:  make pw pp 2>&1 | tee -a ~/work/src/qe_gpu_build.log

# --- 5.7 Install into ~/apps/qe-7.4.1-gpu
make install
ls -l ~/apps/qe-7.4.1-gpu/bin/pw.x ~/apps/qe-7.4.1-gpu/bin/pp.x

# --- 5.8 The qegpu() runtime activation function is added to ~/.bashrc in PHASE 8.
#         (It fixes the 4 known GPU-run bugs: conda-libgomp shadow, HPC-X mpirun,
#          OPAL_PREFIX, and compilers/lib-first LD_LIBRARY_PATH.)

# --- 5.9 VERIFY (after Phase 8 is in place). Minimal 2-atom Si scf against an SSSP UPF:
#   source ~/.bashrc; conda deactivate 2>/dev/null; qegpu
#   $MPIRUN -np 1 $QEGPU/pw.x -in /tmp/qe_smoke_scf.in > /tmp/qe_smoke_scf.out 2>&1
#   grep -E "GPU acceleration is ACTIVE|JOB DONE|^!.*total energy" /tmp/qe_smoke_scf.out
#   nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader  # nonzero while running


##############################################################################
# PHASE 6 — ORCA 6.1.1 (parallel) + OpenMPI 4.1.6 from source
#   ORCA tree: rsync the portable precompiled binaries from gabia (no rebuild).
#   OpenMPI 4.1.6: build from source into $HOME (apt 4.0.3 is the WRONG series).
#   Paste block-by-block as user 'kgy'.
##############################################################################

# --- 6a. rsync the precompiled ORCA 6.1.1 binary tree from gabia -> ~/apps
#         (trailing slashes on BOTH sides avoid a nested orca-6.1.1/orca-6.1.1)
mkdir -p ~/apps
rsync -aHvz --info=progress2 \
  root@121.78.116.27:/data/apps/orca-6.1.1/ \
  ~/apps/orca-6.1.1/
ls -la ~/apps/orca-6.1.1/orca
ls    ~/apps/orca-6.1.1/ | head -40
# Confirm ORCA expects OpenMPI 4.x SONAMEs (libmpi.so.40):
ldd ~/apps/orca-6.1.1/orca_scf 2>/dev/null | grep -i -E 'mpi|not found' || \
  ldd ~/apps/orca-6.1.1/orca | grep -i -E 'mpi|not found'

# --- 6b. Build OpenMPI 4.1.6 from source into ~/apps (NO sudo). gcc-9/gfortran-9.
mkdir -p ~/apps/src && cd ~/apps/src
wget -c https://download.open-mpi.org/release/open-mpi/v4.1/openmpi-4.1.6.tar.bz2
## FALLBACK if wget is blocked by the proxy:
##   rsync -avz root@121.78.116.27:/data/apps/src/openmpi-4.1.6.tar.bz2 ~/apps/src/
## or (fastest) rsync gabia's relocatable OpenMPI 4.1.x install tree directly and
## SKIP the configure/make below, then jump to 6c:
##   rsync -aHvz root@121.78.116.27:/data/apps/openmpi-4.1.6/ ~/apps/openmpi-4.1.6/
tar xjf openmpi-4.1.6.tar.bz2
cd openmpi-4.1.6
./configure --prefix=$HOME/apps/openmpi-4.1.6 \
            CC=gcc CXX=g++ FC=gfortran \
            --enable-mpi-fortran=all
make -j8          # -j8 not -j16: OpenMPI's C++ compiles can OOM at high -j
make install

# --- 6c. ORCA env file (OpenMPI 4.1.6 FIRST on PATH/LD_LIBRARY_PATH, then ORCA tree)
cat > ~/apps/orca-6.1.1/orca_env.sh <<'EOF'
# --- ORCA 6.1.1 + OpenMPI 4.1.6 environment (esp-Z590) ---
export OMPI_HOME="$HOME/apps/openmpi-4.1.6"
export ORCA_HOME="$HOME/apps/orca-6.1.1"
# OpenMPI 4.1.6 MUST come before any system MPI (apt 4.0.3):
export PATH="$OMPI_HOME/bin:$ORCA_HOME:$PATH"
export LD_LIBRARY_PATH="$OMPI_HOME/lib:$ORCA_HOME:$LD_LIBRARY_PATH"
export ORCA_EXE="$ORCA_HOME/orca"
EOF
grep -q 'orca-6.1.1/orca_env.sh' ~/.bashrc || \
  echo 'source ~/apps/orca-6.1.1/orca_env.sh' >> ~/.bashrc
source ~/apps/orca-6.1.1/orca_env.sh

# --- 6d. Verify MPI is your 4.1.6 and ORCA resolves ALL its libs
which mpirun && mpirun --version | head -1        # must report 4.1.6, from ~/apps
ldd ~/apps/orca-6.1.1/orca_scf 2>/dev/null | grep -i -E 'mpi|not found'
#   -> libmpi.so.40 => ~/apps/openmpi-4.1.6/lib/... , NO "not found".

# --- 6e. Parallel smoke test. CRITICAL ORCA RULES:
#     * Do NOT prepend mpirun — ORCA spawns MPI itself.
#     * Call ORCA by its FULL ABSOLUTE PATH for parallel runs.
#     * Request cores INSIDE the input via '%pal nprocs N end', NOT -np.
mkdir -p ~/work/orca_test && cd ~/work/orca_test
cat > h2o_par.inp <<'EOF'
! BP86 def2-SVP
%pal nprocs 4 end
* xyz 0 1
O  0.0000  0.0000  0.0000
H  0.0000  0.7570  0.5860
H  0.0000 -0.7570  0.5860
*
EOF
$HOME/apps/orca-6.1.1/orca ~/work/orca_test/h2o_par.inp > ~/work/orca_test/h2o_par.out
grep -E "FINAL SINGLE POINT ENERGY|TOTAL RUN TIME|ORCA finished" ~/work/orca_test/h2o_par.out


##############################################################################
# PHASE 7 — rsync portable artifacts from gabia (root@121.78.116.27)
#   Passwordless SSH key esp -> gabia is already set. Run as 'kgy'. No sudo.
#   Trailing slash on SOURCE so contents land directly (no nested dir).
#   --partial lets you re-run to resume a dropped transfer.
##############################################################################

mkdir -p ~/work ~/apps ~/.cache

# 7.0 sanity: reach gabia passwordlessly
ssh -o BatchMode=yes -o ConnectTimeout=10 root@121.78.116.27 'echo GABIA_OK; hostname' \
  || echo "SSH to gabia failed — fix the key before rsyncing"

# 7.1 Pseudopotentials  (SSSP 1.3.0 PBE + Nd PP)  -> ~/work/pseudo
rsync -a --info=progress2 --partial \
  root@121.78.116.27:/data/work/pseudo/  ~/work/pseudo/

# 7.2 UMA checkpoint (facebook/UMA, uma-s-1p1) -> ~/.cache/fairchem
#     Copy the ENTIRE models--facebook--UMA tree (blobs/ + snapshots/ + refs/),
#     NOT just checkpoints/: HF_HUB_OFFLINE=1 needs the refs/config YAMLs locally.
#     rsync -a preserves the snapshots/<hash>/ symlinks into blobs/ — do NOT use -L.
rsync -a --info=progress2 --partial \
  root@121.78.116.27:/root/.cache/fairchem/  ~/.cache/fairchem/

# 7.3 ORCA 6.1.1 binary tree (if not already pulled in Phase 6a) -> ~/apps/orca-6.1.1
rsync -a --info=progress2 --partial \
  root@121.78.116.27:/data/apps/orca-6.1.1/  ~/apps/orca-6.1.1/

# 7.4 Structures -> ~/work/bml
rsync -a --info=progress2 --partial \
  root@121.78.116.27:/data/work/bml/  ~/work/bml/

# 7.5 landing check
echo "--- pseudo ---"; ls ~/work/pseudo | head; echo "count: $(ls ~/work/pseudo | wc -l)"
echo "--- fairchem ---"; find ~/.cache/fairchem -name '*.pt' 2>/dev/null | head
echo "--- fairchem snapshot ---"; ls -la ~/.cache/fairchem/models--facebook--UMA/snapshots/*/checkpoints/ 2>/dev/null
readlink -f ~/.cache/fairchem/models--facebook--UMA/snapshots/*/checkpoints/uma-s-1p1.pt 2>/dev/null
echo "--- orca ---"; ls ~/apps/orca-6.1.1/orca ~/apps/orca-6.1.1/orca_scf 2>/dev/null
echo "--- bml ---";  ls ~/work/bml | head


##############################################################################
# PHASE 8 — ~/.bashrc environment block  (append once, then `source ~/.bashrc`)
#   NO secrets committed. Edit MP_API_KEY placeholder locally after pasting.
#   Assumes nvhpc at ~/apps/nvhpc/Linux_x86_64/24.11 (matches Phase 5 / gabia).
##############################################################################

cat >> ~/.bashrc <<'BASHRC'

# ===== esp-Z590-AORUS-MASTER DFT/ML environment =====

# --- conda (miniforge3 under HOME) ---
__conda="$HOME/apps/miniforge3/etc/profile.d/conda.sh"
[ -f "$__conda" ] && . "$__conda"       # enables `conda activate dft|uma`

# --- QE 7.4.1 CPU build (locally built) ---
export PATH="$HOME/apps/qe-7.4.1-cpu/bin:$PATH"

# --- pseudopotentials (SSSP 1.3.0 PBE + Nd) ---
export PSEUDO_DIR="$HOME/work/pseudo"
export ESPRESSO_PSEUDO="$PSEUDO_DIR"    # some QE tools read this name instead

# --- UMA / fairchem: use the local rsynced checkpoint, never hit the network ---
export HF_HUB_OFFLINE=1

# --- Materials Project API key (PASTE YOUR OWN — do not commit) ---
export MP_API_KEY="PASTE_YOUR_MP_API_KEY_HERE"

# --- ORCA 6.1.1 + OpenMPI 4.1.6 (sourced from its own env file) ---
[ -f "$HOME/apps/orca-6.1.1/orca_env.sh" ] && . "$HOME/apps/orca-6.1.1/orca_env.sh"

# --- NVHPC (bundles CUDA 12.6) — used by the GPU QE build ---
export NVVER="24.11"
export NV="$HOME/apps/nvhpc/Linux_x86_64/$NVVER"
export CUDA_HOME="$NV/cuda/12.6"        # nvhpc-bundled CUDA 12.6
[ -d "$CUDA_HOME" ] || export CUDA_HOME="$NV/cuda"   # fallback if unversioned

# qegpu : GPU-QE runtime env for THIS shell only. Reason (proven on gabia):
#   GPU pw.x is linked to NVHPC HPC-X OpenMPI, and NVHPC libgomp/CUDA/math libs
#   MUST come FIRST or you hit "libgomp: TODO". Run `conda deactivate` first.
qegpu() {
  local NV="${NV:-$HOME/apps/nvhpc/Linux_x86_64/$NVVER}"
  local HPCX; HPCX="$(ls -d "$NV"/comm_libs/*/hpcx/hpcx-*/ompi 2>/dev/null | sort | tail -1)"
  [ -z "$HPCX" ] && HPCX="$(ls -d "$NV"/comm_libs/hpcx/latest/ompi 2>/dev/null | tail -1)"
  export OPAL_PREFIX="$HPCX"
  export MPIRUN="$OPAL_PREFIX/bin/mpirun"
  export QEGPU="$HOME/apps/qe-7.4.1-gpu/bin"
  export LD_LIBRARY_PATH="$NV/compilers/lib:$NV/cuda/12.6/lib64:$NV/math_libs/lib64:$OPAL_PREFIX/lib:$LD_LIBRARY_PATH"
  export PATH="$QEGPU:$OPAL_PREFIX/bin:$NV/compilers/bin:$PATH"
  export OMP_NUM_THREADS=1
  echo "GPU-QE env active. bin=$QEGPU  mpirun=$MPIRUN"
  echo "  run:  \$MPIRUN -np 1 \$QEGPU/pw.x -npool 1 -in scf.in > scf.out 2>&1"
  echo "  (did you 'conda deactivate' first?)"
}
# ===== end DFT/ML environment =====
BASHRC

source ~/.bashrc
echo "MP_API_KEY set? -> $([ "$MP_API_KEY" = 'PASTE_YOUR_MP_API_KEY_HERE' ] && echo 'NO — edit ~/.bashrc' || echo yes)"


##############################################################################
# PHASE 9 — end-to-end verification (V0..V6). Fresh shell, run top-to-bottom.
#   Stop and fix at the first FAIL.
##############################################################################

# --- V0. torch sees the RTX 3090 (in the 'uma' env) ---
conda activate uma
python -c "import torch; print('torch', torch.__version__, 'cuda?', torch.cuda.is_available(), '|', (torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NO-GPU'))"
#   EXPECT: cuda? True | NVIDIA GeForce RTX 3090

# --- V1. CPU pw.x tiny SCF using a real pseudo (bulk Al, PBE) ---
conda deactivate 2>/dev/null
command -v pw.x && echo "pw.x on PATH: $(which pw.x)"
AL_UPF=$(ls ~/work/pseudo | grep -iE '^Al[._].*\.upf$' | head -1)
echo "Using Al pseudo: ${AL_UPF:?no Al UPF found in ~/work/pseudo}"
mkdir -p ~/work/_verify && cd ~/work/_verify
cat > al_scf.in <<EOF
&control
  calculation='scf', prefix='al', outdir='./tmp', pseudo_dir='$PSEUDO_DIR', verbosity='low'
/
&system
  ibrav=2, celldm(1)=7.65, nat=1, ntyp=1, ecutwfc=30, ecutrho=240,
  occupations='smearing', smearing='mp', degauss=0.02
/
&electrons
  conv_thr=1.0d-6, mixing_beta=0.7
/
ATOMIC_SPECIES
  Al 26.98 $AL_UPF
ATOMIC_POSITIONS (alat)
  Al 0.0 0.0 0.0
K_POINTS automatic
  6 6 6 1 1 1
EOF
mpirun -np 4 pw.x -in al_scf.in > al_scf.out 2>&1 || pw.x -in al_scf.in > al_scf.out 2>&1
grep -q "JOB DONE" al_scf.out && grep "^!" al_scf.out && echo "V1 PASS: CPU pw.x SCF converged" \
  || { echo "V1 FAIL — tail:"; tail -25 al_scf.out; }

# --- V2. epsilon.x present in the CPU build ---
command -v epsilon.x >/dev/null && echo "V2 PASS: epsilon.x -> $(which epsilon.x)" \
  || echo "V2 FAIL: epsilon.x missing (rebuild CPU QE 'make pp')"

# --- V3. UMA single-point on the GPU (loads local checkpoint, offline) ---
conda activate uma
python - <<'PY'
import os, numpy as np
from ase.build import bulk
from fairchem.core import pretrained_mlip
from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
import fairchem.core as fc
print("fairchem", getattr(fc,"__version__","?"), "| HF_HUB_OFFLINE", os.environ.get("HF_HUB_OFFLINE"))
pred = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
calc = FAIRChemCalculator(pred, task_name="omat")
a = bulk("Cu","fcc", a=3.61); a.calc = calc
e = a.get_potential_energy(); f = a.get_forces()
print(f"V3 PASS: UMA/GPU  E={e:.4f} eV  |F|max={np.abs(f).max():.4f} eV/A")
PY

# --- V4. mp_api query (needs MP_API_KEY exported) ---
python - <<'PY'
import os
k = os.environ.get("MP_API_KEY","")
assert k and k!="PASTE_YOUR_MP_API_KEY_HERE", "MP_API_KEY not set — edit ~/.bashrc"
from mp_api.client import MPRester
with MPRester(k) as m:
    d = m.materials.summary.search(material_ids=["mp-149"], fields=["material_id","formula_pretty","band_gap"])
    print("V4 PASS: mp_api ->", d[0].material_id, d[0].formula_pretty, "Eg=", d[0].band_gap)
PY
conda deactivate 2>/dev/null

# --- V5. ORCA serial on a 1-atom input (no MPI needed) ---
cd ~/work/_verify
cat > h_atom.inp <<'EOF'
! UHF def2-SVP
* xyz 0 2
H 0.0 0.0 0.0
*
EOF
$HOME/apps/orca-6.1.1/orca h_atom.inp > h_atom.out 2>&1
grep -q "FINAL SINGLE POINT ENERGY" h_atom.out \
  && { echo "V5 PASS: ORCA serial ->"; grep "FINAL SINGLE POINT ENERGY" h_atom.out; } \
  || { echo "V5 FAIL — tail:"; tail -20 h_atom.out; }

# --- V6 (optional). GPU pw.x smoke test, IF qe-7.4.1-gpu is built ---
if [ -x "$HOME/apps/qe-7.4.1-gpu/bin/pw.x" ]; then
  conda deactivate 2>/dev/null; qegpu
  cd ~/work/_verify
  $MPIRUN -np 1 $QEGPU/pw.x -npool 1 -in al_scf.in > al_scf_gpu.out 2>&1
  grep -q "JOB DONE" al_scf_gpu.out && echo "V6 PASS: GPU pw.x SCF converged" \
    || { echo "V6 FAIL — tail:"; tail -25 al_scf_gpu.out; }
else
  echo "V6 SKIP: qe-7.4.1-gpu not built yet"
fi

echo "==== VERIFICATION COMPLETE — review V0..V6 lines above ===="
##############################################################################
# END setup/new_server_esp_setup.sh
##############################################################################