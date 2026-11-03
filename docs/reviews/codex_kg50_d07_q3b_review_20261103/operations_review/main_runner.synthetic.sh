#!/bin/bash
#SBATCH --job-name=kg50_d07_b50_r56
#SBATCH --output=logs/output_kg50_d07_b50_r56_%j.out
#SBATCH -n 56
#SBATCH --time=5-00:00:00

cd "/synthetic/dem_test/kg50_d07_b50" || exit 1
ds=$(sha256sum 2>/dev/null < "/synthetic/dem_test/kg50_d07_b50/input_kg50_d07_b50_r56.liggghts" | cut -c1-64); ks=$(sha256sum 2>/dev/null < "/synthetic/dem_test/kg50_d07_b50/restart_kg50_d07_b50/restart_compress_1000000.bin" | cut -c1-64)
echo "LMP_IDENTITY (10-30 KG50R-F02): lmp_mpi=$(command -v lmp_mpi || echo none) sha256=$(sha256sum 2>/dev/null < "$(command -v lmp_mpi)" | cut -c1-64) deck=/synthetic/dem_test/kg50_d07_b50/input_kg50_d07_b50_r56.liggghts sha256=$ds checkpoint=/synthetic/dem_test/kg50_d07_b50/restart_kg50_d07_b50/restart_compress_1000000.bin sha256=$ks"
[ "$ds" = "322aeec7870695760c160bacef5c87ef3f55c6ae7b91e8721399eab1354fb5b1" ] && [ "$ks" = "d94f152912894b080bd7a377d2c1c1cc535bd5d1931b0082f3b668ab608a8a2e" ] || { echo "LMP_IDENTITY_MISMATCH (10-30 KG50R-F02): deck /synthetic/dem_test/kg50_d07_b50/input_kg50_d07_b50_r56.liggghts sha256 $ds (checked 322aeec7870695760c160bacef5c87ef3f55c6ae7b91e8721399eab1354fb5b1) checkpoint /synthetic/dem_test/kg50_d07_b50/restart_kg50_d07_b50/restart_compress_1000000.bin sha256 $ks (checked d94f152912894b080bd7a377d2c1c1cc535bd5d1931b0082f3b668ab608a8a2e) - mpirun not started"; exit 1; }
command mpirun --oversubscribe --bind-to none -np 56 lmp_mpi -in "/synthetic/dem_test/kg50_d07_b50/input_kg50_d07_b50_r56.liggghts"
