#!/usr/bin/env bash
# b2o3 RELAXED-ION elastic constants -> Young's modulus on KISTI.
# Reuses build_elastic_strain_inputs.py --relaxed_ion (12 strain relaxes, ions
# relax at fixed strained cell) + fit_elastic_cij_stress.py (Cij -> B,G,E,nu).
# Run on the KISTI login node: it generates inputs and submits a 12-task array.
#
#   bash tools/elastic/run_b2o3_elastic_kisti.sh
set -euo pipefail
set +H
BASE=/scratch/x3430a02/kgy/b2o3_eos                 # has relax_v0.in/.out + pseudo
REPO=/scratch/x3430a02/kgy/Yonghoon-DEM-DFT          # repo clone (tools)
WORK=$BASE/elastic_relaxedion
STRAIN=0.005
BIN=/scratch/x3430a02/kgy/apps/qe-gpu/bin
mkdir -p "$WORK/logs"

# 1) generate the 12 relaxed-ion strain inputs (calculation='relax', cell fixed)
python3 "$REPO/tools/comp1_v3/build_elastic_strain_inputs.py" \
  --relaxed_ion --src_in "$BASE/relax_v0.in" --src_out "$BASE/relax_v0.out" \
  --strain "$STRAIN" --workdir "$WORK" --prefix_base strain

# 2) make each strain use a UNIQUE outdir + a shared pseudo symlink, so the 12
#    jobs can run in parallel without clobbering ./tmp or the prefix.
[ -e "$WORK/pseudo" ] || ln -sf "$BASE/pseudo" "$WORK/pseudo" 2>/dev/null || true
for t in strain_11_p strain_11_m strain_22_p strain_22_m strain_33_p strain_33_m \
         strain_23_p strain_23_m strain_13_p strain_13_m strain_12_p strain_12_m; do
  sed -i "s|outdir *=.*|outdir = './tmp_$t'|" "$WORK/$t.in"
  sed -i "s|prefix *=.*|prefix = '$t'|"        "$WORK/$t.in"
done

# 3) job-array sbatch: one relaxed-ion relax per task
cat > "$WORK/sbatch_elastic.sh" <<EOF
#!/bin/bash
#SBATCH -J llm_finetuning_v08
#SBATCH -p amd_a100nv_8
#SBATCH -N 1
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:2
#SBATCH --time=12:00:00
#SBATCH -o logs/el_%A_%a.out
#SBATCH -e logs/el_%A_%a.err
#SBATCH --comment pytorch
#SBATCH --array=0-11
source /scratch/x3430a02/mjs0000/miniforge3/etc/profile.d/conda.sh 2>/dev/null || true
conda activate uma 2>/dev/null || true
cd "\$SLURM_SUBMIT_DIR"
TAGS=(strain_11_p strain_11_m strain_22_p strain_22_m strain_33_p strain_33_m strain_23_p strain_23_m strain_13_p strain_13_m strain_12_p strain_12_m)
t=\${TAGS[\$SLURM_ARRAY_TASK_ID]}
if [ -f \$t.out ] && grep -q "JOB DONE" \$t.out; then echo "\$t already done"; exit 0; fi
mpirun -np 1 $BIN/pw.x -npool 1 -inp \$t.in > \$t.out 2>&1
grep -q "JOB DONE" \$t.out && echo "\$t OK" || { echo "\$t FAIL"; tail -15 \$t.out; }
EOF

cd "$WORK" && sbatch sbatch_elastic.sh
echo
echo "submitted 12-task array in $WORK"
echo "watch:  squeue -u x3430a02 | grep llm   |  ls $WORK/strain_*.out"
echo "when all 12 say JOB DONE, FIT (Cij -> B,G,E,nu):"
echo "  python3 $REPO/tools/modelc_v3/fit_elastic_cij_stress.py --workdir $WORK --strain $STRAIN"
