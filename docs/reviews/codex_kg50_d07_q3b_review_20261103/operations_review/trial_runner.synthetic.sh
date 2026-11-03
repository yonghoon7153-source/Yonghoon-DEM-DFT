#!/bin/bash
#SBATCH --job-name=kg50_d07_b50_r56t
#SBATCH --output=logs/output_kg50_d07_b50_r56t_%j.out
#SBATCH -n 56
#SBATCH --time=01:00:00

cd "/synthetic/dem_test/kg50_d07_b50" || exit 1
ds=$(sha256sum 2>/dev/null < "/synthetic/dem_test/kg50_d07_b50/input_kg50_d07_b50_r56t.liggghts" | cut -c1-64); ks=$(sha256sum 2>/dev/null < "/synthetic/dem_test/kg50_d07_b50/restart_kg50_d07_b50/restart_compress_1000000.bin" | cut -c1-64)
echo "LMP_IDENTITY (10-30 KG50R-F02): lmp_mpi=$(command -v lmp_mpi || echo none) sha256=$(sha256sum 2>/dev/null < "$(command -v lmp_mpi)" | cut -c1-64) deck=/synthetic/dem_test/kg50_d07_b50/input_kg50_d07_b50_r56t.liggghts sha256=$ds checkpoint=/synthetic/dem_test/kg50_d07_b50/restart_kg50_d07_b50/restart_compress_1000000.bin sha256=$ks"
[ "$ds" = "862482e630403be5fd74dee8bc4d8f306342f3dfa7ab5c31cc9a6d735f8e2809" ] && [ "$ks" = "d94f152912894b080bd7a377d2c1c1cc535bd5d1931b0082f3b668ab608a8a2e" ] || { echo "LMP_IDENTITY_MISMATCH (10-30 KG50R-F02): deck /synthetic/dem_test/kg50_d07_b50/input_kg50_d07_b50_r56t.liggghts sha256 $ds (checked 862482e630403be5fd74dee8bc4d8f306342f3dfa7ab5c31cc9a6d735f8e2809) checkpoint /synthetic/dem_test/kg50_d07_b50/restart_kg50_d07_b50/restart_compress_1000000.bin sha256 $ks (checked d94f152912894b080bd7a377d2c1c1cc535bd5d1931b0082f3b668ab608a8a2e) - mpirun not started"; exit 1; }
command mpirun --oversubscribe --bind-to none -np 56 lmp_mpi -in "/synthetic/dem_test/kg50_d07_b50/input_kg50_d07_b50_r56t.liggghts"
