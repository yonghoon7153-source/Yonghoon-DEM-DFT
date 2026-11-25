#!/bin/bash
# icohp_ext_kisti.sh — b2o3 ICOHP with EXTENDED LOBSTER basis (Li 1s2s2p,
# P/S/Cl 3s3p3d, B/O 2s2p) = modelc apples-to-apples, correct Li-X.
# Extended basis needs ~895 projection functions > the nbnd=460 of the first
# nscf, so this re-runs nscf at nbnd=960 REUSING the SCF charge density in
# tmp_paw/b2o3.save (NO SCF redo) then LOBSTER. If LOBSTER still says "too few
# bands", bump NBND.  Then plot with tools/modelc_v3/plot_lobster_4panel.py.
#SBATCH -J llm_finetuning_extlob
#SBATCH -p amd_a100nv_8
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --time=05:00:00
#SBATCH --comment pytorch
#SBATCH -o logs/extlob_%j.out
#SBATCH -e logs/extlob_%j.err
set +H
cd "${SLURM_SUBMIT_DIR:-/scratch/x3430a02/kgy/b2o3_eos}"; mkdir -p logs
source /scratch/x3430a02/mjs0000/miniforge3/etc/profile.d/conda.sh 2>/dev/null || true
conda activate uma 2>/dev/null || true
GPU=/scratch/x3430a02/kgy/apps/qe-gpu/bin
LOBSTER=/scratch/x3430a02/kgy/apps/lobster-5.1.1/lobster-5.1.1
NBND=960
echo ">> start $(date +%H:%M:%S)  nbnd=$NBND"
test -d tmp_paw/b2o3.save || { echo "ERROR: tmp_paw/b2o3.save 없음 (SCF 결과 필요)"; exit 1; }

# 1) nscf @ high nbnd (reuse SCF density in tmp_paw) — extended basis needs bands >= basis funcs
python3 - "$NBND" <<'PY'
import re, sys
nb = sys.argv[1]; s = open("b2o3_paw_scf.in").read()
s = re.sub(r"calculation\s*=\s*'[^']*'", "calculation='nscf'", s)
for t in ("nosym", "noinv"):
    if not re.search(rf"{t}\s*=", s, re.I):
        s = re.sub(r"(&SYSTEM[^\n]*\n)", rf"\1  {t}=.true.\n", s, 1, re.I)
s = re.sub(r"nbnd\s*=\s*[0-9]+", f"nbnd={nb}", s) if re.search(r"nbnd\s*=", s) \
    else re.sub(r"(&SYSTEM[^\n]*\n)", rf"\1  nbnd={nb}\n", s, 1, re.I)
if not re.search(r"wf_collect", s, re.I):
    s = re.sub(r"(&(?:control|CONTROL)[^\n]*\n)", r"\1  wf_collect=.true.\n", s, 1)
open("nscf_ext.in", "w").write(s); print("-> nscf_ext.in nbnd=" + nb)
PY
echo ">> nscf(ext) $(date +%H:%M:%S)"
mpirun -np 1 "$GPU/pw.x" -npool 1 -in nscf_ext.in > nscf_ext.out 2>&1
grep -q "JOB DONE" nscf_ext.out || { echo "nscf FAIL:"; tail -20 nscf_ext.out; exit 1; }

# 2) extended-basis LOBSTER (reads b2o3_paw_scf.in [has wf_collect] + ./b2o3.save[nbnd960])
ln -sfn tmp_paw/b2o3.save ./b2o3.save
cat > lobsterin <<'EOF'
COHPstartEnergy -12
COHPendEnergy 6
basisSet pbeVaspFit2015
gaussianSmearingWidth 0.05
basisfunctions Li 1s 2s 2p
basisfunctions B 2s 2p
basisfunctions O 2s 2p
basisfunctions P 3s 3p 3d
basisfunctions S 3s 3p 3d
basisfunctions Cl 3s 3p 3d
cohpGenerator from 1.4 to 2.1 type B type S
cohpGenerator from 1.3 to 1.8 type P type O
cohpGenerator from 1.9 to 2.4 type P type S
cohpGenerator from 1.8 to 4.0 type Li type S
cohpGenerator from 2.0 to 4.0 type Li type Cl
cohpGenerator from 3.0 to 3.9 type S type S
EOF
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-8}
echo ">> LOBSTER(ext) $(date +%H:%M:%S)"
"$LOBSTER" > lobster_ext.out 2>&1
echo ">> done $(date +%H:%M:%S)"
echo "== charge spilling (확장 basis라 더 낮아야) =="; grep -iE "charge spilling" lobster_ext.out | head
echo "== bands/basis 경고 =="; grep -iE "basis functions|will be ignored|too few|more.*bands" lobster_ext.out | head
echo "== ICOHPLIST =="; head -30 ICOHPLIST.lobster 2>/dev/null || tail -30 lobster_ext.out
