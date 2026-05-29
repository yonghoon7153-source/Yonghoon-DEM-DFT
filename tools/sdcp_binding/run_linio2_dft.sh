#!/bin/bash
# Run LiNiO2 (104) slab DFT+U+AFM relax on gabia (single A100 GPU).
#
# Usage:
#   bash run_linio2_dft.sh <work_dir>
# where <work_dir> contains relax.in (from build_linio2_dft_input.py).
#
# Restart-aware: tmp/<prefix>.save 있으면 'restart' 모드, 없으면 fresh.
# 96 atom + DFT+U + ISPIN=2 → 단일 SCF ~5-15 분, nstep=30 → 5-25h.
# 무너지는지 확인이 목적이라 nstep 10 만 돼도 충분 — 5~10 step 후 visualize.

set -e
WORK="${1:?usage: $0 <work_dir>}"
QE=/data/apps/qe-7.4.1-gpu/bin/pw.x
PREFIX=$(grep "^\s*prefix" "$WORK/relax.in" | head -1 | sed -E "s/.*'(.+)'.*/\1/")

cd "$WORK"
mkdir -p tmp logs

# GPU QE 7.4.1 (NVHPC build) requires mpirun for MPI_Init to succeed.
# Single rank is fine for a 1-GPU job.
export OMPI_ALLOW_RUN_AS_ROOT=1
export OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
# Pick whichever mpirun the QE GPU build expects (try NVHPC path first)
if [ -x /data/apps/qe-7.4.1-gpu/mpi/bin/mpirun ]; then
    MPIRUN=/data/apps/qe-7.4.1-gpu/mpi/bin/mpirun
elif command -v mpirun >/dev/null 2>&1; then
    MPIRUN=$(command -v mpirun)
else
    echo "[$(date)] ERROR: no mpirun found" >&2
    exit 1
fi

echo "[$(date)] LiNiO2 DFT+U slab relax: $WORK"
echo "[$(date)] host=$(hostname)  prefix=$PREFIX"
echo "[$(date)] mpirun=$MPIRUN  pw=$QE"
nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used --format=csv,noheader

# Already converged?
if [ -f relax.out ] && grep -qE "bfgs converged in|End of BFGS Geometry" relax.out 2>/dev/null; then
    echo "[$(date)] already BFGS converged — nothing to do"
    grep '!' relax.out | tail -1
    exit 0
fi

# Restart from checkpoint if present, else fresh start.
SAVE="tmp/${PREFIX}.save"
sed -i "/restart_mode/d" relax.in 2>/dev/null || true
if [ -f "$SAVE/charge-density.dat" ] || [ -f "$SAVE/charge-density.hdf5" ]; then
    sed -i "/calculation/a\\    restart_mode = 'restart'" relax.in
    echo "[$(date)] restart from $SAVE"
else
    echo "[$(date)] fresh start"
fi

T0=$(date +%s)
$MPIRUN -np 1 $QE -input relax.in > relax.out 2>&1 || echo "[$(date)] pw.x exited with non-zero (may still have output)"
DT=$(( $(date +%s) - T0 ))

echo "[$(date)] elapsed ${DT}s"
if grep -qE "bfgs converged in|End of BFGS Geometry" relax.out 2>/dev/null; then
    echo "[$(date)] ✓ BFGS CONVERGED"
    grep '!' relax.out | tail -1
elif grep -qE "convergence NOT achieved" relax.out 2>/dev/null; then
    echo "[$(date)] ⚠ SCF non-converged — check mixing"
    tail -15 relax.out
else
    echo "[$(date)] INCOMPLETE — re-run to resume from .save"
    tail -8 relax.out
fi
