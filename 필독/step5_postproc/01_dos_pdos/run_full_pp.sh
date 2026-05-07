#!/bin/bash
# DOS/PDOS post-processing pipeline (NSCF → DOS → projwfc)
# 사용: tight SCF (scf.in) 먼저 끝낸 후 실행
# 입력: tmp_v###/<prefix>.save (SCF 결과)
# 출력: <prefix>.dos, <prefix>.pdos_atm#N(El)_wfc#M(orb), <prefix>.pdos_tot

set -e
cd /scratch/x3430a02/kgy/manuscript_support/pipeline_v2/comp2_lpscbr/v2_postproc/

QE=/scratch/x3430a02/kgy/apps/qe-gpu/bin/pw.x
DOS=/scratch/x3430a02/kgy/apps/qe-gpu/bin/dos.x
PROJX=/scratch/x3430a02/kgy/apps/qe-gpu/bin/projwfc.x

# GPU 1 (GPU 0 has lammps_sevenn)
export CUDA_VISIBLE_DEVICES=1

echo "[NSCF] start $(date)"
$QE -input nscf.in > nscf.out 2>&1
grep -q "JOB DONE" nscf.out && echo "[NSCF] DONE $(date)" || { echo "[NSCF] FAILED"; exit 1; }

echo "[DOS] start $(date)"
$DOS -input dos.in > dos.out 2>&1
grep -q "JOB DONE" dos.out && echo "[DOS] DONE $(date)" || { echo "[DOS] FAILED"; exit 1; }

echo "[PROJWFC] start $(date)"
stdbuf -oL $PROJX -input projwfc.in > projwfc.out 2>&1
grep -q "JOB DONE" projwfc.out && echo "[PROJWFC] DONE $(date)" || echo "[PROJWFC] FAILED"

echo "[ALL DONE] $(date)"
