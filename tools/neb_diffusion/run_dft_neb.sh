#!/bin/bash
# Run DFT SCF on 7 NEB images sequentially (gabia QE GPU).
# Uses NVHPC HPCX MPI environment (same as other DFT runs).
#
# Usage:
#   bash run_dft_neb.sh <dft_verify_dir>
# where dft_verify_dir contains img0.in ... img6.in
set -e
WORK="${1:?usage: $0 <dft_verify_dir>}"
cd "$WORK"

# NVHPC HPCX env (matches other gabia QE GPU runs)
export PATH=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi/bin:/usr/local/bin:/usr/bin:/bin
export LD_LIBRARY_PATH=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi/lib:/data/apps/nvhpc/Linux_x86_64/24.11/compilers/lib:/usr/local/cuda-12.6/lib64
export OPAL_PREFIX=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi
export OMP_NUM_THREADS=1
export CUDA_VISIBLE_DEVICES=0
export OMPI_ALLOW_RUN_AS_ROOT=1
export OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

QE=/data/apps/qe-7.4.1-gpu/bin/pw.x
MPIRUN=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi/bin/mpirun

echo "[$(date)] DFT NEB verification — sequential 7-image SCF"
echo "[$(date)] WORK=$WORK"
nvidia-smi --query-gpu=index,name --format=csv,noheader

for i in 0 1 2 3 4 5 6; do
    INF=img${i}.in
    OUT=img${i}.out
    if [ ! -f "$INF" ]; then
        echo "[$(date +%H:%M:%S)] img${i}: no input — skip"; continue
    fi
    if [ -f "$OUT" ] && grep -q "JOB DONE" "$OUT" 2>/dev/null; then
        echo "[$(date +%H:%M:%S)] img${i}: already DONE — skip"
        grep '^!' "$OUT" | tail -1
        continue
    fi

    echo "[$(date +%H:%M:%S)] img${i}: START"
    T0=$(date +%s)
    $MPIRUN -np 1 $QE -in "$INF" > "$OUT" 2>&1 || echo "[$(date +%H:%M:%S)] img${i}: pw.x non-zero exit"
    DT=$(( $(date +%s) - T0 ))

    if grep -q "JOB DONE" "$OUT" 2>/dev/null; then
        echo "[$(date +%H:%M:%S)] img${i}: DONE (${DT}s)"
        grep '^!' "$OUT" | tail -1
    else
        echo "[$(date +%H:%M:%S)] img${i}: INCOMPLETE (${DT}s) — last 8 lines:"
        tail -8 "$OUT"
    fi
done

echo ""
echo "[$(date)] === ALL 7 DONE — Parsing energies ==="

python3 <<'PY'
import re
energies_eV = []
for i in range(7):
    try:
        txt = open(f"img{i}.out").read()
    except FileNotFoundError:
        energies_eV.append(None); continue
    matches = re.findall(r"!.*total energy\s+=\s+(-?\d+\.\d+)\s+Ry", txt)
    if matches:
        energies_eV.append(float(matches[-1]) * 13.6057)
    else:
        energies_eV.append(None)

if all(e is not None for e in energies_eV):
    E0 = energies_eV[0]
    rel = [e - E0 for e in energies_eV]
    barrier = max(rel)
    ts_idx = rel.index(barrier)
    print()
    print(f"{'image':<8} {'E (eV)':>14}  {'E_rel (eV)':>12}")
    print("=" * 42)
    for i, (e, r) in enumerate(zip(energies_eV, rel)):
        mark = "  ← TS" if i == ts_idx else ""
        print(f"  {i:<6} {e:>14.4f}  {r:>+12.4f}{mark}")
    print(f"\nDFT barrier: {barrier:.4f} eV  (at image {ts_idx})")

    import json
    json.dump({
        "energies_eV": energies_eV,
        "rel_energies_eV": rel,
        "barrier_eV": barrier,
        "barrier_image_idx": ts_idx,
        "n_images": 7,
        "method": "QE pw.x SCF on UMA-NEB-relaxed geometries",
    }, open("dft_neb_results.json", "w"), indent=2)
    print(f"\n→ dft_neb_results.json")
else:
    print("Some images did not finish — check img*.out")
    for i, e in enumerate(energies_eV):
        print(f"  img{i}: {'OK ' + str(e) if e is not None else 'FAILED'}")
PY
