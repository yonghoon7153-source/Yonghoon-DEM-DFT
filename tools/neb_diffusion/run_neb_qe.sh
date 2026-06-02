#!/bin/bash
# Full DFT NEB driver (gabia QE GPU).
#
# Sets up the NVHPC HPCX MPI env, picks pseudos by system, and launches
# the ASE NEB + Espresso driver. Always passes --restart so re-launching
# resumes from neb.traj instead of starting over.
#
# Usage:
#   bash run_neb_qe.sh <work_dir> <li3n|lic6> [warm_start_xyz]
# Example:
#   bash run_neb_qe.sh /data/work/runs/li_neb_diffusion/li3n_001/dft_neb li3n
set -e
WORK="${1:?usage: $0 <work_dir> <li3n|lic6> [warm_start_xyz]}"
SYSTEM="${2:?usage: $0 <work_dir> <li3n|lic6> [warm_start_xyz]}"
WARM_ARG="${3:-}"

# ---- NVHPC HPCX env (PREPENDED so conda env python with ASE/numpy survives) ----
export PATH=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi/bin:$PATH
export LD_LIBRARY_PATH=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi/lib:/data/apps/nvhpc/Linux_x86_64/24.11/compilers/lib:/usr/local/cuda-12.6/lib64:${LD_LIBRARY_PATH:-}
export OPAL_PREFIX=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi
export OMP_NUM_THREADS=1
export CUDA_VISIBLE_DEVICES=0
export OMPI_ALLOW_RUN_AS_ROOT=1
export OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

QE=/data/apps/qe-7.4.1-gpu/bin/pw.x
MPIRUN=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi/bin/mpirun

# Pick conda env python (the launching shell must have ASE+numpy)
PYTHON_BIN="${PYTHON_BIN:-$(command -v python3)}"
echo "Using python: $PYTHON_BIN"
$PYTHON_BIN -c "import numpy, ase; print('  numpy', numpy.__version__); print('  ase  ', ase.__version__)" \
    || { echo "ERROR: numpy/ase not importable by $PYTHON_BIN — activate uma env first"; exit 2; }

# ASE Espresso command (uses ASE_ESPRESSO_COMMAND in calculator)
export ASE_ESPRESSO_COMMAND="$MPIRUN -np 1 $QE -in PREFIX.pwi > PREFIX.pwo"

case "$SYSTEM" in
  li3n)
    PSEUDOS=(Li=li_pbe_v1.4.uspp.F.UPF N=N.pbe-n-radius_5.UPF)
    WARM_DEFAULT=/data/work/runs/li_neb_diffusion/li3n_001/neb_run1/neb_path_final.xyz
    ;;
  lic6)
    PSEUDOS=(Li=li_pbe_v1.4.uspp.F.UPF C=C.pbe-n-kjpaw_psl.1.0.0.UPF)
    WARM_DEFAULT=/data/work/runs/li_neb_diffusion/lic6_0001/neb_run1/neb_path_final.xyz
    ;;
  *)
    echo "Unknown system: $SYSTEM (use 'li3n' or 'lic6')"; exit 1 ;;
esac

WARM="${WARM_ARG:-$WARM_DEFAULT}"
mkdir -p "$WORK"

echo "[$(date)] full DFT NEB launch"
echo "  SYSTEM      = $SYSTEM"
echo "  WORK        = $WORK"
echo "  WARM_START  = $WARM"
echo "  PSEUDOS     = ${PSEUDOS[*]}"
nvidia-smi --query-gpu=index,name --format=csv,noheader

exec "$PYTHON_BIN" "$(dirname "$0")/run_neb_qe.py" \
    --warm_start "$WARM" \
    --work_dir   "$WORK" \
    --pseudos    "${PSEUDOS[@]}" \
    --pseudo_dir /data/work/pseudo \
    --qe_bin     "$QE" \
    --mpirun     "$MPIRUN" \
    --kgrid 2 2 1 \
    --fmax 0.05 \
    --max_steps_phase1 5 \
    --max_steps_phase2 30 \
    --optimizer bfgs \
    --restart
