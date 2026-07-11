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

run_heavy () {         # $1 = job dir, $2 = required free MiB
    # U DIRECT + robust smearing/mixing. Archaeology of reference_dft_v2 (07-11):
    # NO run of this slab ever truly converged -- U=0 sloshes at 1000s of Ry (AFM
    # collapse; our u0 retraced their failed trajectory digit-for-digit), while
    # U-on from scratch plateaus at ~2e-3 Ry after 300 iters (gpu2: beta 0.10,
    # degauss 0.02). +U stabilizes the AFM/gapped Ni-d state => run U directly,
    # and soften the classic sloshing knobs: degauss 0.03->0.05 (mv), beta 0.10,
    # ndim 8. Molecules (gapped, integer occupations) are smearing-insensitive,
    # so their 0.03-degauss energies remain consistent with the heavy set.
    local j=$1 need=$2
    local d=$BASE/$j
    grep -q "JOB DONE" "$d/scf.out" 2>/dev/null && { echo "[$j] already done — skip"; return; }
    rm -f "$d/scf_u0.in" "$d/scf_u0.out"              # retire the u0-ramp stage
    sed -i "/startingpot/d" "$d/scf.in"               # no u0 rho to read anymore
    sed -i "s/degauss.*/degauss         = 0.05/"      "$d/scf.in"
    sed -i "s/mixing_beta.*/mixing_beta     = 0.10/"  "$d/scf.in"
    sed -i "s/mixing_ndim.*/mixing_ndim     = 8/"     "$d/scf.in"
    rm -rf "$d/tmp" "$d/scf.out"
    wait_gpu "$need"
    echo "[$j] START (U direct; degauss 0.05 / beta 0.10 / ndim 8)  $(date)"
    ( cd "$d" && $MPIRUN -np 1 $QE -in scf.in > scf.out 2>&1 )
    if grep -q "JOB DONE" "$d/scf.out"; then
        local e=$(grep '^!' "$d/scf.out" | tail -1 | awk '{print $5}')
        if grep -q "convergence has been achieved" "$d/scf.out"; then
            echo "[$j] DONE (converged)  E=${e} Ry  $(date)"
        else
            echo "[$j] DONE (MAXSTEP PLATEAU — E는 오차막대와 함께만 사용)  E=${e} Ry  $(date)"
        fi
    else
        echo "[$j] NOT finished — rerun script to retry  $(date)"
    fi
}

echo "===== Phase-B SCF chain (gabia)  $(date) ====="
# 48 GB card: molecules need ~47 GB free (8 A boxes), heavies ~30-32 GB.
run_one   mol_doped       30000    # 34 atoms, gamma — DONE-skip if converged
run_one   mol_neutral     30000    # 35 atoms
run_heavy slab            30000    # 96 atoms, U-ramp (u0 -> u62)
run_heavy complex_doped   32000    # 130 atoms, U-ramp
run_heavy complex_neutral 32000    # 131 atoms, U-ramp
echo "===== chain end  $(date) ====="
n=$(grep -l "JOB DONE" $BASE/*/scf.out 2>/dev/null | wc -l)
echo "completed SCFs: $n / 5"
if [ "$n" -eq 5 ]; then
    echo "--- E_bind harvest (Ry) ---"
    for j in slab complex_doped complex_neutral mol_doped mol_neutral; do
        printf '%-16s ' $j; grep '^!' $BASE/$j/scf.out | tail -1
    done
fi
