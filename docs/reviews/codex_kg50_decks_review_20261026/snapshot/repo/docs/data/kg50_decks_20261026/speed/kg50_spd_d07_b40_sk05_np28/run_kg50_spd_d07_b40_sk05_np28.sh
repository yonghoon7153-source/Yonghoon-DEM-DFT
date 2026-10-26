#!/bin/bash
#SBATCH --job-name=kg50_spd_d07_b40_sk05_np28
#SBATCH --output=logs/output_kg50_spd_d07_b40_sk05_np28_%j.out
#SBATCH --qos=cpu-60
#SBATCH --partition=cpu
#SBATCH -n 28
#SBATCH --time=5-00:00:00

source ~/.bashrc
conda activate myenv

export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

cd $HOME/dem_test/kg50_spd_d07_b40_sk05_np28
mpirun --oversubscribe --bind-to none -np 28 lmp_mpi -in input_kg50_spd_d07_b40_sk05_np28.liggghts
