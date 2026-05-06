#!/bin/bash
# Bader charge analysis pipeline (pp.x → bader_lnx_64)
# 입력: V0 SCF 결과 (tmp_v###/<prefix>.save) + pp.in
# 출력: charge.cube (Gaussian cube), ACF.dat (Bader atomic charges)

cd /scratch/x3430a02/kgy/manuscript_support/pipeline_v2/comp2_lpscbr
QE=/scratch/x3430a02/kgy/apps/qe-gpu/bin
export CUDA_VISIBLE_DEVICES=0

echo "=== Bader: pp.x ==="
mpirun -np 1 $QE/pp.x -in comp2_v2_pp.in > comp2_v2_pp.out 2>&1
echo "pp.x done"

if [ -f comp2_v2_charge.cube ]; then
    echo "=== Bader analysis ==="
    bader comp2_v2_charge.cube
    echo "Bader done!"
    head -5 ACF.dat
fi
echo "===== BADER COMPLETE ====="
