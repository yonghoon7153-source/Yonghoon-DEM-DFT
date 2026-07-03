#!/bin/bash
# interface_md_kisti.sh — SE|Li-metal interface: build -> relax -> NVT MD -> decomp
# analysis, all with UMA MLIP (NO DFT). GPU (A100). Tests whether Li dynamically
# decomposes the SE (P-S breaking, Li2S/Li3P, and for b2o3 metallic LiB) -> the
# kinetic reality behind the equilibrium "b2o3 worse at bare Li metal" flag.
#
#   sbatch tools/oxidation/interface_md_kisti.sh db/structures/b2o3_relaxV0.xyz  b2o3
#   sbatch tools/oxidation/interface_md_kisti.sh db/structures/modelc_V0_k663.xyz modelc
# knobs via env:  SC="2 2" T=600 PROD=50 EQ=2  sbatch ...
#
#SBATCH -J llm_finetuning_iface
#SBATCH -p amd_a100nv_8
#SBATCH -N 1
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH --time=12:00:00
#SBATCH --comment pytorch
#SBATCH -o logs/iface_%j.out
#SBATCH -e logs/iface_%j.err
set +H
source /scratch/x3430a02/mjs0000/miniforge3/etc/profile.d/conda.sh 2>/dev/null || true
conda activate uma 2>/dev/null || true
cd "${SLURM_SUBMIT_DIR:-$PWD}"; mkdir -p logs
echo ">> start $(date)  cwd=$(pwd)"

XYZ="${1:?usage: sbatch interface_md_kisti.sh <SE.xyz> <label>}"
LBL="${2:?need label}"
SC="${SC:-1 1}"; T="${T:-600}"; PROD="${PROD:-50}"; EQ="${EQ:-2}"
echo ">> SE=$XYZ label=$LBL supercell='$SC' T=${T}K prod=${PROD}ps"

# 0) preflight — fairchem/UMA present in this env? (else run on kgy instead)
python3 -c "from fairchem.core import pretrained_mlip; from fairchem.core.calculate.ase_calculator import FAIRChemCalculator; import ase; print('preflight: fairchem+ase OK')" \
  || { echo 'ERROR: fairchem/ase missing in this env -> run the same 3 python steps on kgy.'; exit 1; }

# 1) build interface  (report printed to log — eyeball SE/Li counts + Li density)
python3 tools/oxidation/build_li_interface.py \
  --electrolyte "$XYZ" --label "$LBL" --supercell $SC --out "interface_${LBL}_Li.xyz" || exit 1

# 2) UMA relax (FIRE) + Langevin NVT MD
python3 tools/oxidation/run_li_interface_md.py \
  --interface "interface_${LBL}_Li.xyz" --label "$LBL" \
  --temperature "$T" --equilib_ps "$EQ" --prod_ps "$PROD" --dt_fs 1.0 --device cuda || exit 1

# 3) decomposition metrics -> CSV
python3 tools/oxidation/analyze_interface_decomp.py "${LBL}_traj.xyz" --label "$LBL" \
  --dt_ps 0.2 --out "db/properties/interface_decomp_${LBL}.csv" || exit 1

echo ">> ALL DONE $(date)  ->  ${LBL}_relaxed.xyz  ${LBL}_traj.xyz  db/properties/interface_decomp_${LBL}.csv"
