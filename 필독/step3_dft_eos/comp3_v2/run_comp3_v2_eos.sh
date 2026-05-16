#!/bin/bash
export PATH=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi/bin:/usr/local/bin:/usr/bin:/bin
export LD_LIBRARY_PATH=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi/lib:/data/apps/nvhpc/Linux_x86_64/24.11/compilers/lib:/usr/local/cuda-12.6/lib64
export OPAL_PREFIX=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi
export OMP_NUM_THREADS=1
export CUDA_VISIBLE_DEVICES=0

QE=/data/apps/qe-7.4.1-gpu/bin/pw.x
cd /data/work/comp3_v2_eos

for v in 098 099 100 101 102 103 104 105 106 107 108; do
    IN="comp3_v2_eos_v${v}.in"
    OUT="comp3_v2_eos_v${v}.out"
    if [ -f "$OUT" ] && grep -q "JOB DONE" "$OUT"; then
        echo "[v${v}] already DONE, skip"; continue
    fi
    echo "[$(date +%H:%M:%S)] === v${v} ==="
    rm -rf tmp_v${v}/
    mpirun -np 1 $QE -in "$IN" > "$OUT" 2>&1
    JD=$(grep -c "JOB DONE" "$OUT")
    E=$(grep "!" "$OUT" | tail -1 | awk '{print $5}')
    P=$(grep "total   stress" "$OUT" | tail -1 | awk '{print $6}')
    echo "  JOB_DONE=$JD  E=$E Ry  P=$P kbar"
done
echo "[$(date +%H:%M:%S)] ===== ALL DONE ====="
