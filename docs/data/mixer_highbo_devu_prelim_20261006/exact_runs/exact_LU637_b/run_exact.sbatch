#!/bin/bash
#SBATCH --job-name=exact_b_LU637_ref_r2_s32452843
#SBATCH --output=/lustre/home/yonghoon/mixer_dev7_20260930_v26/exact_LU637_b/slurm_exact_%j.out
#SBATCH --qos=cpu-60
#SBATCH --partition=cpu
#SBATCH -n 1
#SBATCH --time=00:20:00
# 정확 좌표 프레임 (scripts/mixer_exact_frames.py deck 이 썼다 · 강성 축 사전등록 §12-4 (나)) — 고치지 말 것 (영수증이 sha256 을 적는다)
# ⛔ 원 런 폴더에는 쓰지 않는다: cwd = 이 작업 폴더 · 체크포인트는 read_restart 로 읽기만 · 형식 = 재개-위상 영수증 job 235118 과 같은 mpirun -np 1

source ~/.bashrc
conda activate myenv
cd /lustre/home/yonghoon/mixer_dev7_20260930_v26/exact_LU637_b || exit 3
mpirun --oversubscribe --bind-to none -np 1 /lustre/home/yonghoon/LIGGGHTS-PUBLIC/src/lmp_mpi -in in.exact > log.exact 2>&1
