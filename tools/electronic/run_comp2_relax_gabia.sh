#!/usr/bin/env bash
# =============================================================================
# run_comp2_relax_gabia.sh — comp2 champion(v3 followmin) 고정셀 DFT relax on gabia.
#
# 목적: UMA followmin을 DFT 최소로 완화 -> gap/DOS용 정식 champion 기하.
# ⚠ argyrodite 골격 유지 필수 (전례: db/structures/lpscl_..._BROKEN_PS4_dissociated).
#    보호책: ① 고정셀(vc-relax 금지 — B0/부피 EOS 확정 25.8 GPa와 자기일관)
#            ② 보수적 BFGS (trust_radius_max 0.3 bohr) — 큰 점프로 basin 이탈 방지
#            ③ relax 후 PS4 4배위 골격 검증 (깨지면 저장 보류).
# 세팅 = saddle-check와 동일 (kjpaw PAW 60/480, k222, mv 0.01) -> -508.7 확인과 일관.
#
#   gabia(root): bash tools/electronic/run_comp2_relax_gabia.sh
#   GPU 대기 내장(SKIP_WAIT=1로 우회). ⚠ 먼저 nvidia-smi로 GPU 비었는지 확인
#   (SDCP 잔재 프로세스 있으면 kill 후). 완료 -> comp2_V0_v3_relaxed.xyz + 골격판정.
# =============================================================================
set -u; set +H
REPO=${REPO:-$HOME/Yonghoon-DEM-DFT}; [ -d "$REPO" ] || REPO=$HOME/work/Yonghoon-DEM-DFT
WORK=${WORK:-/data/work/runs/comp2_relax}; mkdir -p "$WORK"
IN_XYZ=${IN_XYZ:-$REPO/db/structures/comp2_V0_v3_candidate.xyz}
UMA_PY=$(ls /data/apps/miniforge3/envs/uma/bin/python3 2>/dev/null || which python3)
test -f "$IN_XYZ" || { echo "MISSING $IN_XYZ — git pull 먼저"; exit 1; }
[ "$(pgrep -fc run_comp2_relax_gabia)" -le 2 ] || { echo "이미 실행중"; exit 1; }
echo "REPO=$REPO  UMA_PY=$UMA_PY  IN=$IN_XYZ"

# ---- pseudos (saddle-check와 동일 kjpaw + Br) ----
PSE=$WORK/pseudo; mkdir -p "$PSE"
NEED="Li.pbe-s-kjpaw_psl.1.0.0.UPF P.pbe-n-kjpaw_psl.1.0.0.UPF S.pbe-n-kjpaw_psl.1.0.0.UPF Cl.pbe-n-kjpaw_psl.1.0.0.UPF Br.pbe-n-kjpaw_psl.1.0.0.UPF"
BASE="https://pseudopotentials.quantum-espresso.org/upf_files"
for p in $NEED; do
  [ -s "$PSE/$p" ] && continue
  f=$(find "$HOME" /data -name "$p" 2>/dev/null | head -1)
  if [ -n "$f" ]; then cp "$f" "$PSE/"; echo "[pseudo] $p <- $f"
  else echo "[pseudo] wget $p"; wget -q "$BASE/$p" -O "$PSE/$p" || true
    [ -s "$PSE/$p" ] || { echo "!! $p 확보 실패 — UPF 목록 붙여줘"; exit 1; }
  fi
done

# ---- relax 입력 생성 (고정셀, 좌표만) ----
"$UMA_PY" - "$IN_XYZ" "$WORK" "$PSE" <<'PY'
import sys
from ase.io import read
xyz, work, pse = sys.argv[1:4]
mass = {"Li":6.94,"P":30.97,"S":32.06,"Cl":35.45,"Br":79.904}
ups = {"Li":"Li.pbe-s-kjpaw_psl.1.0.0.UPF","P":"P.pbe-n-kjpaw_psl.1.0.0.UPF",
       "S":"S.pbe-n-kjpaw_psl.1.0.0.UPF","Cl":"Cl.pbe-n-kjpaw_psl.1.0.0.UPF",
       "Br":"Br.pbe-n-kjpaw_psl.1.0.0.UPF"}
a = read(xyz)
syms = a.get_chemical_symbols()
order = [e for e in ("Li","P","S","Cl","Br") if e in syms]
spec = "\n".join(f"  {e:2s} {mass[e]:7.3f}  {ups[e]}" for e in order)
cell = "\n".join("  " + " ".join(f"{x:14.8f}" for x in r) for r in a.cell.array)
pos = "\n".join(f"  {s:2s} {p[0]:14.8f} {p[1]:14.8f} {p[2]:14.8f}"
                for s,p in zip(syms, a.get_positions()))
inp = f"""&CONTROL
  calculation='relax', prefix='c2relax', outdir='./tmp_relax',
  pseudo_dir='{pse}', tprnfor=.true., tstress=.true., disk_io='low',
  forc_conv_thr=1d-3, nstep=100
/
&SYSTEM
  ibrav=0, nat={len(a)}, ntyp={len(order)}, ecutwfc=60, ecutrho=480,
  occupations='smearing', smearing='mv', degauss=0.01
/
&ELECTRONS
  conv_thr=1d-8, mixing_beta=0.3, electron_maxstep=200
/
&IONS
  ion_dynamics='bfgs', trust_radius_ini=0.2, trust_radius_max=0.3
/
ATOMIC_SPECIES
{spec}
CELL_PARAMETERS angstrom
{cell}
ATOMIC_POSITIONS angstrom
{pos}
K_POINTS automatic
  2 2 2 0 0 0
"""
open(f"{work}/relax.in","w").write(inp)
print(f"[in] relax.in nat={len(a)} ntyp={len(order)} (고정셀 relax, trust_radius_max 0.3)")
PY
[ $? -eq 0 ] || exit 1

# ---- gabia qegpu env + GPU 대기 ----
while [ "${SKIP_WAIT:-0}" != 1 ] && pgrep -f 'pw\.x|neb\.x|comp_phonon_uma|disorder_ensemble' >/dev/null 2>&1; do
  echo "[$(date +%H:%M:%S)] GPU 사용중 — 5분 뒤 재확인 (GPU 비었으면 SKIP_WAIT=1로 재실행)"; sleep 300
done
HPCX=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi
export PATH=$HPCX/bin:$PATH
export LD_LIBRARY_PATH=$HPCX/lib:/data/apps/nvhpc/Linux_x86_64/24.11/compilers/lib:/usr/local/cuda-12.6/lib64:${LD_LIBRARY_PATH:-}
export OPAL_PREFIX=$HPCX OMP_NUM_THREADS=1 CUDA_VISIBLE_DEVICES=0
export OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
QE=/data/apps/qe-7.4.1-gpu/bin/pw.x
MPIRUN=$HPCX/bin/mpirun
[ -x "$QE" ] || { echo "ERROR: $QE 없음"; exit 1; }

cd "$WORK"
if ! grep -aq "JOB DONE" relax.out 2>/dev/null; then
  echo "[$(date +%H:%M:%S)] pw.x relax 시작 (nstep 100, forc_conv 1d-3, 고정셀)"
  "$MPIRUN" -np 1 "$QE" -in relax.in > relax.out 2>&1
fi
grep -aq "JOB DONE" relax.out && echo "[relax] JOB DONE" || { echo "[relax] 미완/에러 — tail:"; tail -15 relax.out; }

# ---- 최종 구조 추출 + argyrodite 골격 검증 ----
"$UMA_PY" - "$WORK" "$IN_XYZ" <<'PY'
import sys, numpy as np
from ase.io import read, write
work, in_xyz = sys.argv[1:3]
def ps4_report(atoms, label):
    sym = np.array(atoms.get_chemical_symbols())
    P = np.where(sym=="P")[0]; S = np.where(sym=="S")[0]
    cell = atoms.cell.array; inv = np.linalg.inv(cell); pos = atoms.get_positions()
    coord=[]; bonds=[]
    for p in P:
        d = pos[S]-pos[p]; f=d@inv; f-=np.round(f); dd=np.linalg.norm(f@cell,axis=1)
        coord.append(int((dd<2.7).sum())); bonds += list(dd[dd<2.7])
    bonds=np.array(bonds)
    print(f"  [{label}] P-S4 배위(각 P의 S이웃<2.7A) = {coord}  (정상=모두 4)")
    if len(bonds): print(f"           P-S bond: mean {bonds.mean():.3f} / min {bonds.min():.3f} / max {bonds.max():.3f} A  (n={len(bonds)})")
    return all(c==4 for c in coord)
start = read(in_xyz)
try:
    final = read(f"{work}/relax.out", format="espresso-out", index=-1)
except Exception as e:
    print("최종프레임 읽기 실패 (relax.out 붙여줘):", e); sys.exit(0)
print("── argyrodite 골격 검증 ──")
ps4_report(start, "START  ")
okf = ps4_report(final, "RELAXED")
disp = np.linalg.norm(final.get_positions()-start.get_positions(), axis=1)
print(f"  max 원자변위(START->RELAXED) = {disp.max():.3f} A, mean {disp.mean():.3f} A")
pos=final.get_positions(); cell=final.cell.array; inv=np.linalg.inv(cell); mind=9e9
for i in range(len(final)-1):
    f=(pos[i+1:]-pos[i])@inv; f-=np.round(f); mind=min(mind, np.linalg.norm(f@cell,axis=1).min())
print(f"  min 원자간거리 = {mind:.3f} A")
if okf and mind>1.5:
    outp=f"{work}/comp2_V0_v3_relaxed.xyz"
    final.info['comment']="comp2 champion v3 DFT-RELAXED (fixed-cell kjpaw 60/480 k222). argyrodite PS4 intact. B0=25.8 GPa carried(EOS V0)."
    write(outp, final)
    print(f"\n  ✅ argyrodite 유지(PS4 전부 4배위) + min-dist OK -> 저장 {outp}")
    print("     >> 이 구조로 gap(fixed-occ nscf)/DOS. B0=25.8 carry.")
else:
    print(f"\n  ⚠ 골격 이상 (PS4 intact={okf}, min-dist={mind:.2f}) — 저장 보류. BROKEN_PS4 재발? relax.out 확인 필요.")
PY
echo ""; echo ">> relax.out 마지막 '!' 에너지 + 위 골격판정 붙여줘 — 이상없으면 gap/DOS 후속, comp2_V0_v3_relaxed.xyz 회수해서 db 등록."
