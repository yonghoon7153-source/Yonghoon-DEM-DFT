#!/bin/bash
cd /scratch/x3430a02/kgy/manuscript_support
export CUDA_VISIBLE_DEVICES=1
QE=/scratch/x3430a02/kgy/apps/qe-gpu/bin/pw.x

for strain in e1 e2 e3 e6 e5 e4; do
  for sign in pos neg; do
    inp="comp5_basinA/elastic_basinA/comp5_bA_v101_${strain}_${sign}.in"
    out="comp5_basinA/elastic_basinA/comp5_bA_v101_${strain}_${sign}.out"
    echo "=== $strain $sign ==="
    mpirun -np 1 $QE -in $inp > $out 2>&1
    stress=$(grep "total   stress" $out | awk '{print $6}')
    echo "  stress(kbar): $stress"
  done
done
echo "===== ELASTIC DONE ====="
