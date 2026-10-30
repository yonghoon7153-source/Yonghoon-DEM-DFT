#!/bin/bash
#SBATCH --job-name=kg50_d07_b50_r56t
#SBATCH --output=logs/output_kg50_d07_b50_r56t_%j.out
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

cd "/lustre/home/yonghoon/dem_test/kg50_d07_b50" || exit 1
ds=$(sha256sum 2>/dev/null < "/lustre/home/yonghoon/dem_test/kg50_d07_b50/input_kg50_d07_b50_r56t.liggghts" | cut -c1-64); ks=$(sha256sum 2>/dev/null < "/lustre/home/yonghoon/dem_test/kg50_d07_b50/restart_kg50_d07_b50/restart_settling_20001.bin" | cut -c1-64)
echo "LMP_IDENTITY (10-30 KG50R-F02): lmp_mpi=$(command -v lmp_mpi || echo none) sha256=$(sha256sum 2>/dev/null < "$(command -v lmp_mpi)" | cut -c1-64) deck=/lustre/home/yonghoon/dem_test/kg50_d07_b50/input_kg50_d07_b50_r56t.liggghts sha256=$ds checkpoint=/lustre/home/yonghoon/dem_test/kg50_d07_b50/restart_kg50_d07_b50/restart_settling_20001.bin sha256=$ks"
[ "$ds" = "94db4187093b417468ac7a2da6a0b43e5312e04507539251be45cbe2b8011ea1" ] && [ "$ks" = "aa833368651d9bf811c7b39331149ca939bfedf1bbe0511e2d66bf329fde15a8" ] || { echo "LMP_IDENTITY_MISMATCH (10-30 KG50R-F02): deck /lustre/home/yonghoon/dem_test/kg50_d07_b50/input_kg50_d07_b50_r56t.liggghts sha256 $ds (checked 94db4187093b417468ac7a2da6a0b43e5312e04507539251be45cbe2b8011ea1) checkpoint /lustre/home/yonghoon/dem_test/kg50_d07_b50/restart_kg50_d07_b50/restart_settling_20001.bin sha256 $ks (checked aa833368651d9bf811c7b39331149ca939bfedf1bbe0511e2d66bf329fde15a8) - mpirun not started"; exit 1; }
command mpirun --oversubscribe --bind-to none -np 56 lmp_mpi -in "/lustre/home/yonghoon/dem_test/kg50_d07_b50/input_kg50_d07_b50_r56t.liggghts"
