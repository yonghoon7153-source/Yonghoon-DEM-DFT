#!/bin/bash
#SBATCH --job-name=kg50_d2_b50_r56t
#SBATCH --output=logs/output_kg50_d2_b50_r56t_%j.out
#SBATCH --qos=cpu-60
#SBATCH --partition=cpu
#SBATCH -n 56
#SBATCH --time=01:00:00

source ~/.bashrc
conda activate myenv

export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

cd /lustre/home/yonghoon/dem_test/kg50_d2_b50
mpirun --oversubscribe --bind-to none -np 56 lmp_mpi -in input_kg50_d2_b50_r56t.liggghts.bak
