#!/bin/bash
# icohp_lobster_kisti.sh — b2o3 ICOHP via LOBSTER on KISTI (slide 15/16 for the champion).
# Reuses the existing SCF density (tmp/b2o3.save) -> nscf (nosym, more bands) -> LOBSTER.
#
# Prior LOBSTER run FAILED only because it was launched in apps/ (no QE files). LOBSTER
# must run in the dir holding the QE .save. Here we nscf into ./tmp then symlink ./b2o3.save
# so LOBSTER's QE detector finds data-file-schema.xml.
#
#   sbatch tools/electronic/icohp_lobster_kisti.sh
# -> ICOHPLIST.lobster (per-bond ICOHP: B-S, P-O, P-S, Li-S, Li-Cl, S-S), COHPCAR.lobster
#
#SBATCH -J llm_finetuning_icohp
#SBATCH -p amd_a100nv_8
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --time=03:00:00
#SBATCH --comment pytorch
#SBATCH -o logs/icohp_%j.out
#SBATCH -e logs/icohp_%j.err
set +H
cd "${SLURM_SUBMIT_DIR:-/scratch/x3430a02/kgy/b2o3_eos}"; mkdir -p logs
source /scratch/x3430a02/mjs0000/miniforge3/etc/profile.d/conda.sh 2>/dev/null || true
conda activate uma 2>/dev/null || true
GPU=/scratch/x3430a02/kgy/apps/qe-gpu/bin
LOBSTER=/scratch/x3430a02/kgy/apps/lobster-5.1.1/lobster-5.1.1
echo ">> start $(date +%H:%M:%S)"
test -d ./tmp/b2o3.save || { echo "ERROR: ./tmp/b2o3.save 없음"; exit 1; }
test -f b2o3_nscf_dos.in || { echo "ERROR: b2o3_nscf_dos.in 없음"; exit 1; }

# 1) nscf for LOBSTER: add nosym/noinv (full k-grid), bump nbnd (LOBSTER needs nbnd >= n_basis)
python3 - <<'PY'
import re
s = open("b2o3_nscf_dos.in").read()
for tag in ("nosym", "noinv"):
    if not re.search(rf"{tag}\s*=", s, re.I):
        s = re.sub(r"(&SYSTEM[^\n]*\n)", rf"\1  {tag}=.true.\n", s, count=1, flags=re.I)
# bump nbnd 388 -> 460 (occupied ~298 + margin so LOBSTER basis fits)
s = re.sub(r"nbnd\s*=\s*[0-9]+", "nbnd=460", s) if re.search(r"nbnd\s*=", s) \
    else re.sub(r"(&SYSTEM[^\n]*\n)", r"\1  nbnd=460\n", s, count=1, flags=re.I)
# LOBSTER 5.x requires the wf_collect keyword literally in the QE input it reads
if not re.search(r"wf_collect", s, re.I):
    s = re.sub(r"(&(?:control|CONTROL)[^\n]*\n)", r"\1  wf_collect=.true.\n", s, count=1)
open("nscf_lobster.in", "w").write(s); print("-> nscf_lobster.in (nosym, noinv, nbnd=460, wf_collect)")
PY
echo ">> nscf $(date +%H:%M:%S)"
if grep -q "JOB DONE" nscf_lobster.out 2>/dev/null; then
  echo "   nscf 재활용 (이미 JOB DONE — 재계산 안 함)"
else
  mpirun -np 1 "$GPU/pw.x" -npool 1 -in nscf_lobster.in > nscf_lobster.out 2>&1
  grep -q "JOB DONE" nscf_lobster.out || { echo "nscf FAIL:"; tail -20 nscf_lobster.out; exit 1; }
fi

# 2) let LOBSTER's QE detector find the save (it looks for ./<prefix>.save)
ln -sfn tmp/b2o3.save ./b2o3.save
# LOBSTER reads b2o3_scf.in as THE QE input -> make it match the nscf (+wf_collect)
[ -f b2o3_scf.in.orig ] || cp b2o3_scf.in b2o3_scf.in.orig
cp nscf_lobster.in b2o3_scf.in

# 3) lobsterin — champion bonds (matches slide 15/16 + new B-S, P-O)
cat > lobsterin <<'EOF'
COHPstartEnergy -12
COHPendEnergy 6
basisSet pbeVaspFit2015
gaussianSmearingWidth 0.05
cohpGenerator from 1.4 to 2.1 type B type S
cohpGenerator from 1.3 to 1.8 type P type O
cohpGenerator from 1.9 to 2.4 type P type S
cohpGenerator from 2.0 to 3.0 type Li type S
cohpGenerator from 2.2 to 3.2 type Li type Cl
cohpGenerator from 3.0 to 3.8 type S type S
EOF

# 4) run LOBSTER (multithread)
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-8}
echo ">> LOBSTER $(date +%H:%M:%S)  (OMP=$OMP_NUM_THREADS)"
"$LOBSTER" > lobster_run.out 2>&1
echo ">> done $(date +%H:%M:%S)"
echo "==== charge spilling (작을수록 좋음, <~5-10%) ===="
grep -iE "charge spilling|abs. charge spilling" lobster_run.out | head
echo "==== ICOHPLIST (per-bond ICOHP) ===="
if [ -f ICOHPLIST.lobster ]; then head -25 ICOHPLIST.lobster; else echo "ICOHPLIST 없음 — lobster_run.out tail:"; tail -25 lobster_run.out; fi
