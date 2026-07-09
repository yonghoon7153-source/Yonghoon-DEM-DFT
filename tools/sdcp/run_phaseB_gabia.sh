#!/bin/bash
# run_phaseB_gabia.sh — run the 5 Phase-B SCFs on kserver116-27 (gabia GPU).
#   tmux new -s phaseB -d 'bash ~/work/Yonghoon-DEM-DFT/tools/sdcp/run_phaseB_gabia.sh \
#                          > /data/work/runs/sdcp_linio2_binding/phaseB_v7c/run.log 2>&1'
# Smallest-first + resume-safe (skip JOB DONE) + OOM-safe: each job waits until
# GPU 0 has enough FREE memory. On this ~48 GB card p0 holds ~41 GB, so EVERY
# job (molecules included -- a vacuum box at ecutrho 480 is not cheap) must wait
# for p0's min->saddle->barrier chain to free the card; the thresholds encode
# that. Failure-tolerant: an OOM/error job is logged and skipped; rerun to pick
# up whatever didn't finish (the OOM'd molecules re-run cleanly, no JOB DONE).
set -u
BASE=/data/work/runs/sdcp_linio2_binding/phaseB_v7c

# ---- gabia QE-GPU environment (identical to run_neb_qe.sh) ----
HPCX=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi
export PATH=$HPCX/bin:$PATH
export LD_LIBRARY_PATH=$HPCX/lib:/data/apps/nvhpc/Linux_x86_64/24.11/compilers/lib:/usr/local/cuda-12.6/lib64:${LD_LIBRARY_PATH:-}
export OPAL_PREFIX=$HPCX
export OMP_NUM_THREADS=1 CUDA_VISIBLE_DEVICES=0
export OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
QE=/data/apps/qe-7.4.1-gpu/bin/pw.x
MPIRUN=$HPCX/bin/mpirun

wait_gpu () {          # $1 = required free MiB on device 0
    local need=$1 free
    while :; do
        free=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits -i 0 2>/dev/null | head -1)
        [ -z "$free" ] && free=0
        [ "$free" -ge "$need" ] && break
        echo "[$(date +%H:%M:%S)] GPU0 free ${free} MiB < ${need} needed — waiting (p0 busy?)"
        sleep 60
    done
    echo "[$(date +%H:%M:%S)] GPU0 free ${free} MiB >= ${need} — go"
}

run_one () {           # $1 = job dir, $2 = required free MiB
    local j=$1 need=$2          # NOTE: keep on its own line -- under `set -u`, a single
    local d=$BASE/$j            # `local j=$1 d=$BASE/$j` expands $j (unset) before assigning
    if grep -q "JOB DONE" "$d/scf.out" 2>/dev/null; then echo "[$j] already done — skip"; return; fi
    wait_gpu "$need"
    echo "[$j] START $(date)"
    ( cd "$d" && $MPIRUN -np 1 $QE -in scf.in > scf.out 2>&1 )
    if grep -q "JOB DONE" "$d/scf.out"; then
        local e=$(grep '^!' "$d/scf.out" | tail -1 | awk '{print $5}')
        echo "[$j] DONE  E=${e} Ry  $(date)"
    else
        echo "[$j] NOT finished (OOM/error) — rerun script to retry  $(date)"
    fi
}

echo "===== Phase-B SCF chain (gabia)  $(date) ====="
# NOTE: this GPU is ~48 GB and p0 holds ~41 GB, so NOTHING (not even a molecule
# in a vacuum box at ecutrho 480) fits alongside p0 -- the first attempt OOM'd
# the molecules at 4 GB free. All thresholds now gate on "p0 has freed the card"
# (free jumps to ~47 GB when p0's min->saddle->barrier chain finishes).
# Thresholds gate on "p0 has freed the card" (~47 GB free after its chain).
# slab verified to run at 11.7 GB with 30 GB free, co-existing with p0_saddle,
# so heavies use the proven 30/32; molecules (big vacuum box, OOM'd at 6 GB free)
# wait for the same 30 GB before launching.
run_one mol_doped       30000    # 34 atoms, gamma, big vacuum box -> mem-heavy
run_one mol_neutral     30000    # 35 atoms
run_one slab            30000    # 96 atoms, 2x2x1, nspin2+U (ran at 11.7 GB)
run_one complex_doped   32000    # 130 atoms
run_one complex_neutral 32000    # 131 atoms
echo "===== chain end  $(date) ====="
n=$(grep -l "JOB DONE" $BASE/*/scf.out 2>/dev/null | wc -l)
echo "completed SCFs: $n / 5"
if [ "$n" -eq 5 ]; then
    echo "--- E_bind harvest (Ry) ---"
    for j in slab complex_doped complex_neutral mol_doped mol_neutral; do
        printf '%-16s ' $j; grep '^!' $BASE/$j/scf.out | tail -1
    done
fi
