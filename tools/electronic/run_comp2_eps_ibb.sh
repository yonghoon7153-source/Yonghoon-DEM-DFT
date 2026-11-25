#!/usr/bin/env bash
# =============================================================================
# run_comp2_eps_ibb.sh — comp2 ε∞ (전자 유전율/분극률) via ph.x epsil on ibb-master(48c).
#   Route A: fixed-occ SCF (PAW 재활용) + ph.x epsil (E-field DFPT, 3섭동) -> ε∞ 텐서 (+옵션 Born Z*).
#   comp2 insulator(gap 2.04) -> fixed-occ OK. gabia와 완전 독립(다 CPU).
#   ⚠ ph.x hang이 b2o3 실패원인 -> timeout으로 감지. hang이면 Route B(epsilon.x)로 전환.
#
#   ibb-master: conda activate myenv; export OMPI_FC=$(which gfortran)  # (ph.x 빌드 셸과 동일)
#   bash run_comp2_eps_ibb.sh [champion.xyz]   (기본 ~/comp2_eps/comp2_V0_v3_relaxed.xyz)
#   BORN=1 이면 Born Z*+ε0도 (trans=.true., 비쌈).  NP/OMP 조절 가능 (기본 8×6=48).
# =============================================================================
set -u; set +H
WORK=${WORK:-$HOME/comp2_eps}; mkdir -p "$WORK"
XYZ=${1:-$WORK/comp2_V0_v3_relaxed.xyz}
QEBIN=${QEBIN:-$HOME/qe-7.4.1/bin}; PWX=$QEBIN/pw.x; PHX=$QEBIN/ph.x
NP=${NP:-8}; export OMP_NUM_THREADS=${OMP:-6}
BORN=${BORN:-0}
cd "$WORK"
test -f "$XYZ" || { echo "champion xyz 없음: $XYZ  (gabia에서 scp 먼저)"; exit 1; }
test -x "$PHX" || { echo "ph.x 없음: $PHX"; exit 1; }
export OMPI_FC=$(command -v gfortran) OMPI_CC=$(command -v gcc) 2>/dev/null || true
MPIRUN=$(command -v mpirun); echo "pw.x=$PWX  ph.x=$PHX  mpirun=$MPIRUN  np=$NP omp=$OMP_NUM_THREADS"

# ---- pseudos (comp2 kjpaw PAW; find-or-wget) ----
PSE=$WORK/pseudo; mkdir -p "$PSE"
NEED="Li.pbe-s-kjpaw_psl.1.0.0.UPF P.pbe-n-kjpaw_psl.1.0.0.UPF S.pbe-n-kjpaw_psl.1.0.0.UPF Cl.pbe-n-kjpaw_psl.1.0.0.UPF Br.pbe-n-kjpaw_psl.1.0.0.UPF"
BASE="https://pseudopotentials.quantum-espresso.org/upf_files"
for p in $NEED; do
  [ -s "$PSE/$p" ] && continue
  f=$(find "$HOME" -name "$p" 2>/dev/null | head -1)
  if [ -n "$f" ]; then cp "$f" "$PSE/"; else wget -q "$BASE/$p" -O "$PSE/$p" || true; fi
  [ -s "$PSE/$p" ] || { echo "pseudo $p 확보 실패 (인터넷 확인)"; exit 1; }
done

# ---- 1) fixed-occ SCF 입력 (champion xyz -> PAW, occupations=fixed, k222) ----
python3 - "$XYZ" "$PSE" > scf_eps.in <<'PY'
import sys, re, numpy as np
xyz, pse = sys.argv[1], sys.argv[2]
mass={"Li":6.94,"P":30.97,"S":32.06,"Cl":35.45,"Br":79.904}
ups={"Li":"Li.pbe-s-kjpaw_psl.1.0.0.UPF","P":"P.pbe-n-kjpaw_psl.1.0.0.UPF","S":"S.pbe-n-kjpaw_psl.1.0.0.UPF","Cl":"Cl.pbe-n-kjpaw_psl.1.0.0.UPF","Br":"Br.pbe-n-kjpaw_psl.1.0.0.UPF"}
L=open(xyz).read().splitlines(); nat=int(L[0])
A=np.array([float(x) for x in re.search(r'Lattice="([^"]+)"',L[1]).group(1).split()]).reshape(3,3)
sym=[l.split()[0] for l in L[2:2+nat]]
pos=[[float(x) for x in l.split()[1:4]] for l in L[2:2+nat]]
order=[e for e in ("Li","P","S","Cl","Br") if e in sym]
spec="\n".join(f"  {e:2s} {mass[e]:8.3f}  {ups[e]}" for e in order)
cell="\n".join("  "+" ".join(f"{x:14.8f}" for x in r) for r in A)
posc="\n".join(f"  {s:2s} {p[0]:14.8f} {p[1]:14.8f} {p[2]:14.8f}" for s,p in zip(sym,pos))
print(f"""&CONTROL
  calculation='scf', prefix='comp2', outdir='./out_eps',
  pseudo_dir='{pse}', verbosity='high'
/
&SYSTEM
  ibrav=0, nat={nat}, ntyp={len(order)}, ecutwfc=60, ecutrho=480,
  occupations='fixed'
/
&ELECTRONS
  conv_thr=1d-10, mixing_beta=0.3, electron_maxstep=200
/
ATOMIC_SPECIES
{spec}
CELL_PARAMETERS angstrom
{cell}
ATOMIC_POSITIONS angstrom
{posc}
K_POINTS automatic
  2 2 2 0 0 0
""")
PY
echo "[$(date +%H:%M:%S)] fixed-occ SCF 입력 생성 (occupations=fixed, conv_thr 1d-10)"

# ---- 2) SCF ----
if ! grep -q "JOB DONE" scf_eps.out 2>/dev/null; then
  echo "[$(date +%H:%M:%S)] pw.x SCF ..."
  "$MPIRUN" -np "$NP" "$PWX" -in scf_eps.in > scf_eps.out 2>&1
fi
grep -q "JOB DONE" scf_eps.out || { echo "SCF FAIL (fixed-occ가 metal 보면 여기서 죽음):"; tail -20 scf_eps.out; exit 1; }
echo "  SCF OK — insulator 확인:"; grep -iE "highest occupied.*lowest|highest occupied level" scf_eps.out | tail -2

# ---- 3) ph.x epsil 입력 (q 0 0 0 줄 필수) ----
TRANS=".false."; [ "$BORN" = 1 ] && TRANS=".true."
cat > eps.in <<EOF
comp2 eps_inf (electronic dielectric tensor; E-field perturbations)
&inputph
  prefix='comp2', outdir='./out_eps',
  epsil=.true., trans=$TRANS, tr2_ph=1.0d-14, fildyn='comp2.dyn',
/
0 0 0
EOF

# ---- 4) ph.x epsil (HANG 감지 timeout — b2o3 실패대비) ----
echo "[$(date +%H:%M:%S)] ph.x epsil (timeout 60m; hang이면 kill→Route B)"
timeout 60m "$MPIRUN" -np "$NP" "$PHX" -in eps.in > eps.out 2>&1; rc=$?
if [ "$rc" = 124 ]; then
  echo "!! ph.x TIMEOUT(hang 60분) — b2o3 재현. Route B(epsilon.x)로 전환 권장."; tail -15 eps.out; exit 124
fi
grep -qiE "JOB DONE|Dielectric constant" eps.out || { echo "ph.x FAIL (PAW 거부면 Route B):"; tail -20 eps.out; exit 1; }

# ---- 5) ε∞ 추출 ----
echo ""; echo "===== ε∞ (electronic dielectric tensor, cartesian) ====="
grep -iA4 "Dielectric constant in cartesian axis" eps.out | tail -5
[ "$BORN" = 1 ] && { echo "===== Born effective charges Z* ====="; grep -iA5 "Effective charges" eps.out | head -40; }
echo ""; echo ">> 위 3×3 텐서 (대각 평균 = ε∞) 붙여줘 — comp1도 같은 방법으로 → 비교. 성공 시 comp2.json 등록."
