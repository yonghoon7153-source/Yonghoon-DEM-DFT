#!/usr/bin/env bash
# run_phaseB_vertical_gabia.sh — run the 2 vertical single-points on gabia.
# Env set INSIDE the script (not before tmux) -- a `tmux new -d` inherits the
# tmux server's env (uma), so exports done before it are lost -> GNU libgomp
# wins -> "libgomp: TODO" crash. Here the NVHPC/HPC-X env (proven by
# run_phaseB_gabia.sh, which ran the day-long relax fine) is set in-script.
#
#   tmux new -s pbvert -d 'bash ~/work/Yonghoon-DEM-DFT/tools/sdcp/run_phaseB_vertical_gabia.sh > /data/work/runs/sdcp_linio2_binding/phaseB_v7c/pbvert.log 2>&1'
set -u; set +H
BASE=/data/work/runs/sdcp_linio2_binding/phaseB_v7c

# ---- gabia QE-GPU env (verbatim from run_phaseB_gabia.sh) ----
HPCX=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi
export PATH=$HPCX/bin:$PATH
export LD_LIBRARY_PATH=$HPCX/lib:/data/apps/nvhpc/Linux_x86_64/24.11/compilers/lib:/usr/local/cuda-12.6/lib64:${LD_LIBRARY_PATH:-}
export OPAL_PREFIX=$HPCX
export OMP_NUM_THREADS=1 CUDA_VISIBLE_DEVICES=0
export OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
QE=/data/apps/qe-7.4.1-gpu/bin/pw.x
MPIRUN=$HPCX/bin/mpirun

run_one() {   # $1 = job dir
    local d=$BASE/$1
    if grep -aq "JOB DONE" "$d/scf.out" 2>/dev/null; then echo "[$1] already done — skip"; return; fi
    echo "[$(date +%H:%M:%S)] pw.x $1"
    cd "$d" && "$MPIRUN" -np 1 "$QE" -npool 1 -in scf.in > scf.out 2>&1
    if grep -aq "JOB DONE" "$d/scf.out"; then
        echo "[$1] OK  E=$(grep -a '^!' "$d/scf.out"|tail -1|awk '{print $(NF-1)}') Ry"
    else
        echo "[$1] FAIL — tail:"; tail -15 "$d/scf.out"
    fi
}

run_one mol_doped_v2       # gamma gas box (fast, ~tens of min) -- confirms env
run_one complex_doped_v2   # 221 single-point (slow, ~1 day)

echo ""
python3 - <<PY
import re
Ry=13.605693; slab=-10563.22819091
def E(p):
    try:
        es=re.findall(r"^!\s+total energy\s+=\s+(-\d+\.\d+)", open(f"$BASE/{p}/scf.out").read(), re.M)
        return float(es[-1]) if es else None
    except FileNotFoundError: return None
c=E("complex_doped_v2"); m=E("mol_doped_v2")
if c and m:
    eb=(c-slab-m)*Ry
    print(f"E_bind(doped, vertical) = {eb:+.4f} eV | neutral -2.213 | Delta = {eb-(-2.213):+.4f} eV (neg=doping strengthens)")
else:
    print(f"complex={c} mol={m} (one not done yet)")
PY
