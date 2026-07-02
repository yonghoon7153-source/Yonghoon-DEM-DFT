#!/bin/bash
# icohp_paw_kisti.sh — b2o3 ICOHP with LOBSTER, redone with ALL-PAW pseudos.
# LOBSTER rejects USPP ("Wrong potential!"); the champion SCF used USPP (P/S/B).
# This does a fresh all-kjpaw(PAW) SCF -> nscf(nosym,nbnd,wf_collect) -> LOBSTER.
#
# PREREQ: 6 kjpaw pseudos in ./pseudo/  (Li/P/S/Cl/O from manuscript_support,
#         B.pbe-n-kjpaw_psl.1.0.0.UPF downloaded + sftp'd in).
#   ls pseudo/*kjpaw*   # must show all 6 incl. B
#
#   sbatch tools/electronic/icohp_paw_kisti.sh
#
#SBATCH -J llm_finetuning_pawic
#SBATCH -p amd_a100nv_8
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --time=08:00:00
#SBATCH --comment pytorch
#SBATCH -o logs/pawic_%j.out
#SBATCH -e logs/pawic_%j.err
set +H
cd "${SLURM_SUBMIT_DIR:-/scratch/x3430a02/kgy/b2o3_eos}"; mkdir -p logs
source /scratch/x3430a02/mjs0000/miniforge3/etc/profile.d/conda.sh 2>/dev/null || true
conda activate uma 2>/dev/null || true
GPU=/scratch/x3430a02/kgy/apps/qe-gpu/bin
LOBSTER=/scratch/x3430a02/kgy/apps/lobster-5.1.1/lobster-5.1.1
BASE=${1:-b2o3_scf.in.orig}                 # original champion SCF (USPP) as structure source
[ -f "$BASE" ] || BASE=b2o3_scf.in
echo ">> start $(date +%H:%M:%S)  base=$BASE"

# all-PAW pseudo names (must exist in ./pseudo/)
declare -A PAW=( [Li]="Li.pbe-sl-kjpaw_psl.1.0.0.UPF" [P]="P.pbe-n-kjpaw_psl.1.0.0.UPF"
                 [S]="S.pbe-nl-kjpaw_psl.1.0.0.UPF" [Cl]="Cl.pbe-nl-kjpaw_psl.1.0.0.UPF"
                 [O]="O.pbe-n-kjpaw_psl.0.1.UPF" [B]="B.pbe-n-kjpaw_psl.1.0.0.UPF" )
mkdir -p pseudo
# Li/P/S/Cl/O kjpaw already on KISTI — pull them in from the known pseudo dirs.
for d in "$SLURM_SUBMIT_DIR/pseudo" ../pseudo ../manuscript_support/pseudo \
         /scratch/x3430a02/kgy/pseudo "$HOME/pseudo"; do
  [ -d "$d" ] || continue
  for e in Li P S Cl O B; do
    [ -f "pseudo/${PAW[$e]}" ] || { [ -f "$d/${PAW[$e]}" ] && cp "$d/${PAW[$e]}" pseudo/; }
  done
done
# B kjpaw is NOT in the KISTI set — auto-fetch from QE pslibrary if still missing.
# Validate the payload is a real UPF (a 403/hotlink page must NOT masquerade as one).
Bp="${PAW[B]}"
if [ ! -f "pseudo/$Bp" ]; then
  echo ">> fetching $Bp ..."
  for url in "https://pseudopotentials.quantum-espresso.org/upf_files/$Bp" \
             "https://www.quantum-espresso.org/upf_files/$Bp"; do
    echo "   try $url"
    curl -fsSL -o "pseudo/$Bp.part" "$url" 2>/dev/null || wget -qO "pseudo/$Bp.part" "$url" 2>/dev/null || true
    if grep -qiE "PP_HEADER|UPF version" "pseudo/$Bp.part" 2>/dev/null; then
      mv "pseudo/$Bp.part" "pseudo/$Bp"; echo "   ok -> pseudo/$Bp ($(wc -c <"pseudo/$Bp") bytes)"; break
    fi
    rm -f "pseudo/$Bp.part"
  done
fi
if [ ! -f "pseudo/$Bp" ]; then
  echo "  !! B auto-fetch failed (compute node likely has no internet). Do ONE of these:"
  echo "     # (a) on the KISTI LOGIN node, which has internet:"
  echo "     cd '$PWD/pseudo' && wget https://pseudopotentials.quantum-espresso.org/upf_files/$Bp"
  echo "     # (b) or drop the copy you already have into: $PWD/pseudo/$Bp"
fi
for e in Li P S Cl O B; do
  test -f "pseudo/${PAW[$e]}" || { echo "ERROR: pseudo/${PAW[$e]} 없음 (B는 로그인노드에서 wget)"; exit 1; }
done

# 1) PAW SCF input: swap ATOMIC_SPECIES pseudo names, own outdir/prefix
python3 - "$BASE" <<'PY'
import re, sys
s = open(sys.argv[1]).read()
paw = {"Li":"Li.pbe-sl-kjpaw_psl.1.0.0.UPF","P":"P.pbe-n-kjpaw_psl.1.0.0.UPF",
       "S":"S.pbe-nl-kjpaw_psl.1.0.0.UPF","Cl":"Cl.pbe-nl-kjpaw_psl.1.0.0.UPF",
       "O":"O.pbe-n-kjpaw_psl.0.1.UPF","B":"B.pbe-n-kjpaw_psl.1.0.0.UPF"}
def swap(m):
    el = m.group(1); rest = m.group(2)
    base = re.sub(r"[0-9]+$", "", el)
    if base in paw:
        return re.sub(r"\S+\.UPF", paw[base], m.group(0))
    return m.group(0)
# ATOMIC_SPECIES lines: "  El  mass  file.UPF"
s = re.sub(r"(?m)^\s*([A-Za-z]{1,2}[0-9]?)\s+([\d.]+\s+\S+\.UPF)", swap, s)
s = re.sub(r"calculation\s*=\s*'[^']*'", "calculation='scf'", s)
s = re.sub(r"prefix\s*=\s*'[^']*'", "prefix='b2o3'", s)
s = re.sub(r"outdir\s*=\s*'[^']*'", "outdir='./tmp_paw'", s)
# robust SCF for a 128-atom insulator: local-TF + modest beta
for k,v in [("mixing_mode","'local-TF'"),("mixing_beta","0.2"),("electron_maxstep","300")]:
    s = re.sub(rf"{k}\s*=\s*[^\n,]+", f"{k}={v}", s) if re.search(rf"{k}\s*=", s) \
        else re.sub(r"(&electrons[^\n]*\n)", rf"\1  {k}={v},\n", s, count=1, flags=re.I)
open("b2o3_paw_scf.in","w").write(s); print("-> b2o3_paw_scf.in (all-PAW, local-TF)")
PY
grep -A8 ATOMIC_SPECIES b2o3_paw_scf.in | head -9

# 2) PAW SCF (GPU)
echo ">> PAW SCF $(date +%H:%M:%S)"
mpirun -np 1 "$GPU/pw.x" -npool 1 -in b2o3_paw_scf.in > b2o3_paw_scf.out 2>&1
grep -q "JOB DONE" b2o3_paw_scf.out || { echo "SCF FAIL:"; tail -25 b2o3_paw_scf.out; exit 1; }
grep -iE "highest occupied|convergence has been" b2o3_paw_scf.out | tail -2

# 3) nscf for LOBSTER (nosym, nbnd 460, wf_collect) reusing the PAW density
python3 - <<'PY'
import re
s = open("b2o3_paw_scf.in").read()
s = re.sub(r"calculation\s*=\s*'[^']*'", "calculation='nscf'", s)
for tag in ("nosym","noinv"):
    if not re.search(rf"{tag}\s*=", s, re.I): s = re.sub(r"(&SYSTEM[^\n]*\n)", rf"\1  {tag}=.true.\n", s, count=1, flags=re.I)
s = re.sub(r"nbnd\s*=\s*[0-9]+","nbnd=460",s) if re.search(r"nbnd\s*=",s) else re.sub(r"(&SYSTEM[^\n]*\n)",r"\1  nbnd=460\n",s,count=1,flags=re.I)
if not re.search(r"wf_collect",s,re.I): s=re.sub(r"(&(?:control|CONTROL)[^\n]*\n)",r"\1  wf_collect=.true.\n",s,count=1)
open("nscf_paw.in","w").write(s); print("-> nscf_paw.in")
PY
echo ">> nscf $(date +%H:%M:%S)"
mpirun -np 1 "$GPU/pw.x" -npool 1 -in nscf_paw.in > nscf_paw.out 2>&1
grep -q "JOB DONE" nscf_paw.out || { echo "nscf FAIL:"; tail -20 nscf_paw.out; exit 1; }

# 4) LOBSTER (reads b2o3_scf.in = the nscf; find ./b2o3.save)
cp nscf_paw.in b2o3_scf.in
ln -sfn tmp_paw/b2o3.save ./b2o3.save
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
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-8}
echo ">> LOBSTER $(date +%H:%M:%S)"
"$LOBSTER" > lobster_paw.out 2>&1
echo ">> done $(date +%H:%M:%S)"
echo "== charge spilling =="; grep -iE "charge spilling" lobster_paw.out | head
echo "== ICOHPLIST =="; head -25 ICOHPLIST.lobster 2>/dev/null || tail -25 lobster_paw.out
