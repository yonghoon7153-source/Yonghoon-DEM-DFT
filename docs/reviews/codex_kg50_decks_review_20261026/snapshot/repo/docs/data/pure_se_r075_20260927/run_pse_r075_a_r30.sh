#!/bin/bash
#SBATCH --job-name=pse_r075_a_r30
#SBATCH --output=logs/output_pse_r075_a_r30_%j.out
#SBATCH --qos=cpu-60
#SBATCH --partition=cpu
#SBATCH -n 30
#SBATCH --time=5-00:00:00

source ~/.bashrc
conda activate myenv

export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

cd /lustre/home/yonghoon/dem_test/lhs/pse_r075_a
mpirun --oversubscribe --bind-to none -np 30 lmp_mpi -in input_pse_r075_a_r30.liggghts
