#!/usr/bin/env bash
# =============================================================================
# run_lpsocl_elf_gabia.sh — LPSOCl(V0, 62-atom) ELF(+CDD) on gabia **CPU build**.
#
# 여경 진행표의 마지막 칸: LPSOCl ELF. b2o3 ELF는 KISTI에서 뽑았지만 그 save는
# 소멸(2026-07-20 KISTI 정리) — 새 SCF부터. 프로토콜 = comp1/modelc 전자구조 계열
# (gabia_cdd_phx.md): NC ONCV pseudo, ecut 80/320, occupations='fixed'(gap 2.23
# 절연체), k444, conv 1e-10. CPU pw.x/pp.x라 GPU(pbrefine pw.x)와 동시 실행 안전.
#
#   cd ~/Yonghoon-DEM-DFT && git pull   # (or checkout tools/electronic/)
#   tmux new -s lpsoclelf -d 'bash tools/electronic/run_lpsocl_elf_gabia.sh > /data/work/runs/lpsocl_elf/run.log 2>&1'
# 산출: lpsocl_elf.cube (+ CDD용 rho_scf/rho_atomic cube — cube_diff는 repo에서)
# =============================================================================
set -u; set +H
REPO=${REPO:-$HOME/Yonghoon-DEM-DFT}; [ -d "$REPO" ] || REPO=$HOME/work/Yonghoon-DEM-DFT
OUT=/data/work/runs/lpsocl_elf; mkdir -p "$OUT"
V0=$REPO/db/structures/lpsocl_relaxV0.xyz
CPU=/data/apps/qe-7.4.1-cpu/bin
CORES=$(nproc 2>/dev/null || echo 8)
NP=${NP:-$(( CORES < 16 ? CORES : 16 ))}
echo "[mpi] cores=$CORES -> np=$NP"
[ -x "$CPU/pw.x" ] && [ -x "$CPU/pp.x" ] || { echo "ERROR: CPU 빌드 pw.x/pp.x 없음 ($CPU) — ls /data/apps 붙여줘"; exit 1; }
[ -f "$V0" ] || { echo "ERROR: $V0 없음 — git pull"; exit 1; }

# ---- 0) NC(ONCV/SG15) pseudo 5종 수집 (Li P S Cl O) — 로컬 수색 -> SG15 wget 폴백 ----
PSE=$OUT/pseudo; mkdir -p "$PSE"
SG15="http://www.quantum-simulation.org/potentials/sg15_oncv/upf"
for e in Li P S Cl O; do
  ls "$PSE/${e}"_*.upf "$PSE/${e}"_*.UPF >/dev/null 2>&1 && continue
  f=$(find /data/work /data/apps /root -maxdepth 5 \( -iname "${e}_*.upf" -o -iname "${e}.*upf" \) 2>/dev/null \
        | grep -iE "oncv|sg15" | head -1)
  if [ -n "$f" ]; then cp "$f" "$PSE/"; echo "[pseudo] $e <- $f"; continue; fi
  ok=""
  for v in 1.2 1.1 1.0; do
    wget -q "$SG15/${e}_ONCV_PBE-${v}.upf" -O "$PSE/${e}_ONCV_PBE-${v}.upf" 2>/dev/null \
      && [ -s "$PSE/${e}_ONCV_PBE-${v}.upf" ] \
      && grep -aq "UPF" "$PSE/${e}_ONCV_PBE-${v}.upf" \
      && { ok=$v; break; }
    rm -f "$PSE/${e}_ONCV_PBE-${v}.upf"
  done
  if [ -n "$ok" ]; then echo "[pseudo] $e <- SG15 wget (v$ok)"
  else
    echo "!! $e NC pseudo 확보 실패 (로컬 없음 + SG15 wget 실패) — 네트워크/URL 확인 필요"
    exit 1
  fi
done
echo "[pseudo] OK: $(ls "$PSE" | tr '\n' ' ')"

# ---- 1) scf.in 생성 (V0 xyz -> QE, fixed occ, k444) ----
python3 - "$V0" "$OUT" "$PSE" <<'PY'
import re, sys, os
v0, out, pse = sys.argv[1:4]
lines = open(v0).read().splitlines()
nat = int(lines[0])
A = re.search(r'Lattice="([^"]+)"', lines[1]).group(1).split()
cell = [A[0:3], A[3:6], A[6:9]]
at = [l.split()[:4] for l in lines[2:2 + nat]]
elems = []
for a in at:
    if a[0] not in elems: elems.append(a[0])
assert set(elems) == {"Li", "P", "S", "Cl", "O"}, f"unexpected species {elems}"
ups = {e: [f for f in os.listdir(pse) if f.lower().startswith(e.lower() + "_") or f.lower().startswith(e.lower() + ".")][0] for e in elems}
mass = {"Li": 6.94, "P": 30.97, "S": 32.06, "Cl": 35.45, "O": 16.00}
spec = "\n".join(f"  {e:2s} {mass[e]:7.2f}  {ups[e]}" for e in elems)
pos = "\n".join(f"  {a[0]:2s} {float(a[1]):14.8f} {float(a[2]):14.8f} {float(a[3]):14.8f}" for a in at)
cl = "\n".join("  " + " ".join(f"{float(x):14.8f}" for x in r) for r in cell)
scf = f"""&CONTROL
  calculation='scf', prefix='lpsocl', outdir='./out',
  pseudo_dir='{pse}', tprnfor=.true.
/
&SYSTEM
  ibrav=0, nat={nat}, ntyp={len(elems)}, ecutwfc=80, ecutrho=320,
  occupations='fixed'
/
&ELECTRONS
  conv_thr=1d-10, mixing_beta=0.3, electron_maxstep=200
/
ATOMIC_SPECIES
{spec}
CELL_PARAMETERS angstrom
{cl}
ATOMIC_POSITIONS angstrom
{pos}
K_POINTS automatic
  4 4 4 0 0 0
"""
open(f"{out}/scf.in", "w").write(scf)
# atomic-superposition ref (CDD): density frozen at atomic guess
sat = scf.replace("prefix='lpsocl'", "prefix='lpsocl_at'").replace("outdir='./out'", "outdir='./out_at'")
sat = sat.replace("conv_thr=1d-10, mixing_beta=0.3, electron_maxstep=200",
                  "conv_thr=1d20, mixing_beta=0.0, electron_maxstep=1, startingpot='atomic'")
open(f"{out}/scf_atomic.in", "w").write(sat)
print(f"[scf.in] nat={nat} ntyp={len(elems)} k444 fixed-occ -> {out}/scf.in (+scf_atomic.in)")
PY

cd "$OUT"
run_pw() {  # $1=in $2=out
  grep -aq "JOB DONE" "$2" 2>/dev/null && { echo "[$1] done skip"; return 0; }
  echo "[$(date +%H:%M:%S)] pw.x $1 (CPU -np $NP)"
  mpirun -np "$NP" "$CPU/pw.x" -in "$1" > "$2" 2>&1
  grep -aq "JOB DONE" "$2" || { echo "[$1] FAIL — tail:"; tail -12 "$2"; return 1; }
  echo "[$1] OK  E=$(grep -a '^!' "$2" | tail -1 | awk '{print $(NF-1)}') Ry"
}

# ---- 2) SCF -> ELF (plot_num=8) ----
run_pw scf.in scf.out || exit 1
if [ ! -s lpsocl_elf.cube ]; then
  cat > pp_elf.in <<'EOF'
&INPUTPP
  prefix='lpsocl', outdir='./out', plot_num=8, filplot='lpsocl_elf'
/
&PLOT
  iflag=3, output_format=6, fileout='lpsocl_elf.cube'
/
EOF
  echo "[$(date +%H:%M:%S)] pp.x ELF"
  mpirun -np "$NP" "$CPU/pp.x" -in pp_elf.in > pp_elf.out 2>&1
fi
echo "ELF: $(ls -la lpsocl_elf.cube 2>/dev/null || echo FAIL)"

# ---- 3) CDD densities (rho_scf, rho_atomic) — b2o3 그림 계열 패리티 ----
if [ ! -s lpsocl_rho_scf.cube ]; then
  cat > pp_rho.in <<'EOF'
&INPUTPP
  prefix='lpsocl', outdir='./out', plot_num=0, filplot='lpsocl_rho'
/
&PLOT
  iflag=3, output_format=6, fileout='lpsocl_rho_scf.cube'
/
EOF
  mpirun -np "$NP" "$CPU/pp.x" -in pp_rho.in > pp_rho.out 2>&1
fi
run_pw scf_atomic.in scf_atomic.out || true   # maxstep=1이라 'convergence NOT achieved'로 끝나도 정상
if [ ! -s lpsocl_rho_atomic.cube ]; then
  cat > pp_rho_at.in <<'EOF'
&INPUTPP
  prefix='lpsocl_at', outdir='./out_at', plot_num=0, filplot='lpsocl_rho_at'
/
&PLOT
  iflag=3, output_format=6, fileout='lpsocl_rho_atomic.cube'
/
EOF
  mpirun -np "$NP" "$CPU/pp.x" -in pp_rho_at.in > pp_rho_at.out 2>&1
fi

echo ""; echo "===== 산출물 ====="
ls -la lpsocl_elf.cube lpsocl_rho_scf.cube lpsocl_rho_atomic.cube 2>/dev/null
echo ">> gap 체크(fixed-occ): $(grep -a 'highest occupied' scf.out | tail -1)"
echo ">> 3개 cube를 repo/로컬로 가져오면 CDD(cube_diff) + VESTA 페어(.vesta ASCII CRLF) 만들어줄게"
