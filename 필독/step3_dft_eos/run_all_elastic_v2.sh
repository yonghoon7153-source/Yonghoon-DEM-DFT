#!/bin/bash
# DFT 0K Elastic — all 5 compositions
export CUDA_VISIBLE_DEVICES=0
PW=/scratch/x3430a02/kgy/apps/qe-gpu/bin/pw.x

echo '========== comp1 =========='
echo '[1/12] comp1_el_xx_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_xx_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_xx_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_xx_p.out | head -1
echo ''
echo '[2/12] comp1_el_xx_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_xx_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_xx_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_xx_m.out | head -1
echo ''
echo '[3/12] comp1_el_yy_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_yy_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_yy_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_yy_p.out | head -1
echo ''
echo '[4/12] comp1_el_yy_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_yy_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_yy_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_yy_m.out | head -1
echo ''
echo '[5/12] comp1_el_zz_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_zz_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_zz_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_zz_p.out | head -1
echo ''
echo '[6/12] comp1_el_zz_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_zz_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_zz_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_zz_m.out | head -1
echo ''
echo '[7/12] comp1_el_yz_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_yz_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_yz_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_yz_p.out | head -1
echo ''
echo '[8/12] comp1_el_yz_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_yz_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_yz_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_yz_m.out | head -1
echo ''
echo '[9/12] comp1_el_xz_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_xz_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_xz_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_xz_p.out | head -1
echo ''
echo '[10/12] comp1_el_xz_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_xz_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_xz_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_xz_m.out | head -1
echo ''
echo '[11/12] comp1_el_xy_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_xy_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_xy_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_xy_p.out | head -1
echo ''
echo '[12/12] comp1_el_xy_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_xy_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_xy_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp1/comp1_el_xy_m.out | head -1
echo ''
echo 'comp1 elastic done!'
echo ''

echo '========== comp2B =========='
echo '[1/12] comp2B_el_xx_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_xx_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_xx_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_xx_p.out | head -1
echo ''
echo '[2/12] comp2B_el_xx_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_xx_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_xx_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_xx_m.out | head -1
echo ''
echo '[3/12] comp2B_el_yy_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_yy_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_yy_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_yy_p.out | head -1
echo ''
echo '[4/12] comp2B_el_yy_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_yy_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_yy_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_yy_m.out | head -1
echo ''
echo '[5/12] comp2B_el_zz_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_zz_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_zz_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_zz_p.out | head -1
echo ''
echo '[6/12] comp2B_el_zz_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_zz_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_zz_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_zz_m.out | head -1
echo ''
echo '[7/12] comp2B_el_yz_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_yz_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_yz_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_yz_p.out | head -1
echo ''
echo '[8/12] comp2B_el_yz_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_yz_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_yz_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_yz_m.out | head -1
echo ''
echo '[9/12] comp2B_el_xz_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_xz_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_xz_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_xz_p.out | head -1
echo ''
echo '[10/12] comp2B_el_xz_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_xz_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_xz_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_xz_m.out | head -1
echo ''
echo '[11/12] comp2B_el_xy_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_xy_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_xy_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_xy_p.out | head -1
echo ''
echo '[12/12] comp2B_el_xy_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_xy_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_xy_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp2B/comp2B_el_xy_m.out | head -1
echo ''
echo 'comp2B elastic done!'
echo ''

echo '========== comp3 =========='
echo '[1/12] comp3_el_xx_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_xx_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_xx_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_xx_p.out | head -1
echo ''
echo '[2/12] comp3_el_xx_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_xx_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_xx_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_xx_m.out | head -1
echo ''
echo '[3/12] comp3_el_yy_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_yy_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_yy_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_yy_p.out | head -1
echo ''
echo '[4/12] comp3_el_yy_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_yy_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_yy_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_yy_m.out | head -1
echo ''
echo '[5/12] comp3_el_zz_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_zz_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_zz_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_zz_p.out | head -1
echo ''
echo '[6/12] comp3_el_zz_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_zz_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_zz_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_zz_m.out | head -1
echo ''
echo '[7/12] comp3_el_yz_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_yz_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_yz_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_yz_p.out | head -1
echo ''
echo '[8/12] comp3_el_yz_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_yz_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_yz_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_yz_m.out | head -1
echo ''
echo '[9/12] comp3_el_xz_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_xz_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_xz_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_xz_p.out | head -1
echo ''
echo '[10/12] comp3_el_xz_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_xz_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_xz_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_xz_m.out | head -1
echo ''
echo '[11/12] comp3_el_xy_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_xy_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_xy_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_xy_p.out | head -1
echo ''
echo '[12/12] comp3_el_xy_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_xy_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_xy_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp3/comp3_el_xy_m.out | head -1
echo ''
echo 'comp3 elastic done!'
echo ''

echo '========== comp4 =========='
echo '[1/12] comp4_el_xx_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_xx_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_xx_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_xx_p.out | head -1
echo ''
echo '[2/12] comp4_el_xx_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_xx_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_xx_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_xx_m.out | head -1
echo ''
echo '[3/12] comp4_el_yy_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_yy_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_yy_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_yy_p.out | head -1
echo ''
echo '[4/12] comp4_el_yy_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_yy_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_yy_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_yy_m.out | head -1
echo ''
echo '[5/12] comp4_el_zz_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_zz_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_zz_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_zz_p.out | head -1
echo ''
echo '[6/12] comp4_el_zz_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_zz_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_zz_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_zz_m.out | head -1
echo ''
echo '[7/12] comp4_el_yz_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_yz_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_yz_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_yz_p.out | head -1
echo ''
echo '[8/12] comp4_el_yz_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_yz_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_yz_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_yz_m.out | head -1
echo ''
echo '[9/12] comp4_el_xz_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_xz_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_xz_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_xz_p.out | head -1
echo ''
echo '[10/12] comp4_el_xz_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_xz_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_xz_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_xz_m.out | head -1
echo ''
echo '[11/12] comp4_el_xy_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_xy_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_xy_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_xy_p.out | head -1
echo ''
echo '[12/12] comp4_el_xy_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_xy_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_xy_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp4/comp4_el_xy_m.out | head -1
echo ''
echo 'comp4 elastic done!'
echo ''

echo '========== comp5 =========='
echo '[1/12] comp5_el_xx_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_xx_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_xx_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_xx_p.out | head -1
echo ''
echo '[2/12] comp5_el_xx_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_xx_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_xx_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_xx_m.out | head -1
echo ''
echo '[3/12] comp5_el_yy_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_yy_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_yy_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_yy_p.out | head -1
echo ''
echo '[4/12] comp5_el_yy_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_yy_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_yy_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_yy_m.out | head -1
echo ''
echo '[5/12] comp5_el_zz_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_zz_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_zz_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_zz_p.out | head -1
echo ''
echo '[6/12] comp5_el_zz_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_zz_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_zz_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_zz_m.out | head -1
echo ''
echo '[7/12] comp5_el_yz_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_yz_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_yz_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_yz_p.out | head -1
echo ''
echo '[8/12] comp5_el_yz_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_yz_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_yz_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_yz_m.out | head -1
echo ''
echo '[9/12] comp5_el_xz_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_xz_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_xz_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_xz_p.out | head -1
echo ''
echo '[10/12] comp5_el_xz_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_xz_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_xz_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_xz_m.out | head -1
echo ''
echo '[11/12] comp5_el_xy_p'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_xy_p.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_xy_p.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_xy_p.out | head -1
echo ''
echo '[12/12] comp5_el_xy_m'
mpirun -np 1 $PW -in /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_xy_m.in > /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_xy_m.out 2>&1
grep 'total   stress' /scratch/x3430a02/kgy/manuscript_support/elastic/comp5/comp5_el_xy_m.out | head -1
echo ''
echo 'comp5 elastic done!'
echo ''

echo '===== ALL DONE ====='
