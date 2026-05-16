#!/bin/bash
# modelC v2 0K Cij — 12 strain SCF on gabia GPU0
# Same env as comp2 v2: hpcx mpirun, no conda, single-thread OMP
export PATH=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi/bin:/usr/local/bin:/usr/bin:/bin
export LD_LIBRARY_PATH=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi/lib:/data/apps/nvhpc/Linux_x86_64/24.11/compilers/lib:/usr/local/cuda-12.6/lib64
export OPAL_PREFIX=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi
export OMP_NUM_THREADS=1
export CUDA_VISIBLE_DEVICES=0

QE=/data/apps/qe-7.4.1-gpu/bin/pw.x
cd /data/work/modelc_v2_elastic/1_dft_0K

for strain in e1 e2 e3 e6 e5 e4; do
  for sign in p m; do
    DIR="${strain}_${sign}"
    OUT="${DIR}/scf.out"
    if [ -f "$OUT" ] && grep -q "JOB DONE" "$OUT"; then
        echo "[$(date +%H:%M:%S)] === $DIR — already DONE, skip ==="; continue
    fi
    echo "[$(date +%H:%M:%S)] === $DIR ==="
    cd "$DIR"; rm -rf tmp/
    mpirun -np 1 $QE -in scf.in > scf.out 2>&1
    stress=$(grep "total   stress" scf.out | tail -1 | awk '{print $6}')
    JD=$(grep -c "JOB DONE" scf.out)
    echo "  stress(kbar): $stress  | JOB DONE count: $JD"
    cd ..
  done
done
echo "[$(date +%H:%M:%S)] ===== modelC v2 0K ELASTIC DONE ====="
