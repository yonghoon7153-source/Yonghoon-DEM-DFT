#!/bin/bash
#SBATCH --job-name=pse_r075_a
#SBATCH --output=logs/output_pse_r075_a_%j.out
#SBATCH --qos=cpu-60
#SBATCH --partition=cpu
#SBATCH -n 15
#SBATCH --time=5-00:00:00

source ~/.bashrc
conda activate myenv
export PATH=/home/yonghoon/LIGGGHTS-PUBLIC/src:/home/yonghoon/.conda/envs/myenv/bin:$PATH

cd ~/dem_test/lhs/pse_r075_a
mpirun --oversubscribe --bind-to none -np 15 lmp_mpi -in input_pse_r075_a.liggghts
