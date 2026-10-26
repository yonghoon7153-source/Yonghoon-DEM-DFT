#!/bin/bash
#SBATCH --job-name=kg50_d07_b40
#SBATCH --output=logs/output_kg50_d07_b40_%j.out
#SBATCH --qos=cpu-60
#SBATCH --partition=cpu
#SBATCH -n 56
#SBATCH --time=5-00:00:00

source ~/.bashrc
conda activate myenv

export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

cd $HOME/dem_test/kg50_d07_b40
mpirun --oversubscribe --bind-to none -np 56 lmp_mpi -in input_kg50_d07_b40.liggghts
