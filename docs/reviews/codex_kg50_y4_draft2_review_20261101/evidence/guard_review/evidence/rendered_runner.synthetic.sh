#!/bin/bash
#SBATCH --job-name=synthetic_case_r56
#SBATCH --output=logs/output_synthetic_case_r56_%j.out
#SBATCH -n 56
#SBATCH --time=5-00:00:00

cd "/synthetic/unavailable/work" || exit 1
ds=$(sha256sum 2>/dev/null < "/synthetic/unavailable/work/input.liggghts" | cut -c1-64); ks=$(sha256sum 2>/dev/null < "/synthetic/unavailable/work/restart.bin" | cut -c1-64)
echo "LMP_IDENTITY (10-30 KG50R-F02): lmp_mpi=$(command -v lmp_mpi || echo none) sha256=$(sha256sum 2>/dev/null < "$(command -v lmp_mpi)" | cut -c1-64) deck=/synthetic/unavailable/work/input.liggghts sha256=$ds checkpoint=/synthetic/unavailable/work/restart.bin sha256=$ks"
[ "$ds" = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" ] && [ "$ks" = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb" ] || { echo "LMP_IDENTITY_MISMATCH (10-30 KG50R-F02): deck /synthetic/unavailable/work/input.liggghts sha256 $ds (checked aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa) checkpoint /synthetic/unavailable/work/restart.bin sha256 $ks (checked bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb) - mpirun not started"; exit 1; }
command mpirun --oversubscribe --bind-to none -np 56 lmp_mpi -in "/synthetic/unavailable/work/input.liggghts"
