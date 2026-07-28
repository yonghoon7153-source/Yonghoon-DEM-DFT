#!/usr/bin/env bash
# =============================================================================
# run_lpsocl_bader_gabia.sh — LPSOCl(V0, 62-atom) **AE Bader** on gabia CPU build.
#
# ⚠ 왜 ELF 의 rho_scf 를 재사용하지 않는가
#   ELF 런은 **NC ONCV + plot_num=0(가전자)** 이다. 그런데 기존
#   db/properties/bader_b2o3_vs_lpscl16.csv 는 **PAW(kjpaw) + plot_num=17(AE)** 로 계산됐다
#   (B +3.0, P +4.691 같은 준-형식전하가 그 서명). 두 값을 같은 표에 넣으면
#   **도핑 효과가 아니라 방법 차이를 보게 된다.** 그래서 SCF 를 kjpaw 로 다시 돈다.
#   비용은 SCF 한 번 — ELF 와 비슷하다.
#
#   pseudo 세트는 tools/comp1_v3/build_lobster_paw_inputs.py 의 kjpaw_psl 목록과 동일하게
#   맞춘다(그 파일이 O 까지 lpsocl 용으로 등록해 뒀다, 2026-07-17).
#
#   ELF 뒤에 체인:
#     tmux new -s lpsoclbader -d 'bash tools/electronic/run_lpsocl_bader_gabia.sh \
#       > /data/work/runs/lpsocl_bader/run.log 2>&1'
#   (스크립트가 ELF pw.x/pp.x 종료를 스스로 기다린다 — CPU 경합 회피)
# =============================================================================
set -u; set +H
REPO=${REPO:-$HOME/Yonghoon-DEM-DFT}; [ -d "$REPO" ] || REPO=$HOME/work/Yonghoon-DEM-DFT
OUT=/data/work/runs/lpsocl_bader; mkdir -p "$OUT"
ELFDIR=${ELFDIR:-/data/work/runs/lpsocl_elf}
V0=$REPO/db/structures/lpsocl_relaxV0.xyz
CPU=/data/apps/qe-7.4.1-cpu/bin
MPIRUN=${MPIRUN:-/usr/bin/mpirun}; [ -x "$MPIRUN" ] || MPIRUN=mpirun
PHYS=$(lscpu -p=Core,Socket 2>/dev/null | grep -v '^#' | sort -u | wc -l)
[ "${PHYS:-0}" -ge 1 ] || PHYS=$(nproc 2>/dev/null || echo 4)
NP=${NP:-$(( PHYS < 16 ? PHYS : 16 ))}
MPIFLAGS="--oversubscribe"
ts() { date '+%H:%M:%S'; }

[ -x "$CPU/pw.x" ] && [ -x "$CPU/pp.x" ] || { echo "ERROR: CPU 빌드 없음 ($CPU)"; exit 1; }
[ -f "$V0" ] || { echo "ERROR: $V0 없음 — git pull"; exit 1; }
cd "$OUT"

# ---- 0) ELF 런이 끝날 때까지 대기 (CPU 경합 회피) --------------------------
# ⚠ `pgrep -x pw.x` 로 기다리면 **무관한 GPU pw.x 까지 문다**. 실제로 gabia 에서
#   SDCP relax(QE-GPU, /data/apps/qe-7.4.1-gpu, 1.5일 실행 중)가 잡혀서 이 체인이
#   영원히 대기할 뻔했다. CPU 빌드 경로로 좁힌다 — 우리가 피하려는 경합은 CPU 경합이다.
CPUPAT=${CPUPAT:-qe-7.4.1-cpu}
cpu_qe_running() { pgrep -f "$CPUPAT/(pw|pp)\.x" >/dev/null; }
if [ "${WAIT_ELF:-1}" = "1" ]; then
  while cpu_qe_running; do
    echo "[$(ts)] CPU QE($CPUPAT) 진행 중 — 3분 뒤 재확인 "\
"(GPU pw.x 는 무시: $(pgrep -f 'qe-.*-gpu/bin/pw\.x' | tr '\n' ' '))"
    sleep 180
  done
  echo "[$(ts)] CPU 해방 — Bader SCF 착수"
fi

# ---- 1) kjpaw pseudo 수집 (로컬 수색 → PSLibrary 폴백) --------------------
# ⚠ 파일명은 build_lobster_paw_inputs.py 와 **정확히 동일**하게. 다르면 기존 Bader 표와
#   pseudo 세대가 갈려 비교가 또 깨진다.
declare -A PS=( [Li]=Li.pbe-sl-kjpaw_psl.1.0.0.UPF [P]=P.pbe-n-kjpaw_psl.1.0.0.UPF
                [S]=S.pbe-nl-kjpaw_psl.1.0.0.UPF  [Cl]=Cl.pbe-nl-kjpaw_psl.1.0.0.UPF
                [O]=O.pbe-n-kjpaw_psl.0.1.UPF )
PSE=$OUT/pseudo; mkdir -p "$PSE"
PSL="https://pseudopotentials.quantum-espresso.org/upf_files"
for E in Li P S Cl O; do
  F=${PS[$E]}
  if [ -s "$PSE/$F" ]; then echo "[pseudo] $E <- $PSE/$F (있음)"; continue; fi
  HIT=$(find "$HOME" /data /opt -name "$F" -size +1k 2>/dev/null | head -1)
  if [ -n "$HIT" ]; then cp -n "$HIT" "$PSE/$F" 2>/dev/null; echo "[pseudo] $E <- $HIT"
  else
    echo "[pseudo] $E 다운로드 시도: $PSL/$F"
    wget -q -O "$PSE/$F" "$PSL/$F" || curl -sSL -o "$PSE/$F" "$PSL/$F" || true
  fi
  [ -s "$PSE/$F" ] || { echo "ERROR: $E pseudo ($F) 확보 실패 — 수동으로 $PSE 에 두고 재실행"; exit 1; }
done
echo "[pseudo] OK: $(ls "$PSE")"

# ---- 2) SCF 입력 (kjpaw → ecut 70/560, ELF 의 80/320 과 다르다) ------------
python3 - "$V0" "$OUT" <<'PYC'
import sys, os
v0, out = sys.argv[1], sys.argv[2]
L = open(v0).read().splitlines()
nat = int(L[0].split()[0])
# extended-xyz Lattice="..." 우선, 없으면 두 번째 줄 9수
import re
m = re.search(r'Lattice="([^"]+)"', L[1])
cell = [float(x) for x in (m.group(1).split() if m else L[1].split()[:9])]
sym, pos = [], []
for ln in L[2:2+nat]:
    t = ln.split(); sym.append(t[0]); pos.append(t[1:4])
els = sorted(set(sym), key=sym.index)
PS = {"Li":"Li.pbe-sl-kjpaw_psl.1.0.0.UPF","P":"P.pbe-n-kjpaw_psl.1.0.0.UPF",
      "S":"S.pbe-nl-kjpaw_psl.1.0.0.UPF","Cl":"Cl.pbe-nl-kjpaw_psl.1.0.0.UPF",
      "O":"O.pbe-n-kjpaw_psl.0.1.UPF"}
MASS = {"Li":6.94,"P":30.974,"S":32.06,"Cl":35.45,"O":15.999}
s = f"""&CONTROL
  calculation='scf', prefix='lpsocl_paw', outdir='./out_paw',
  pseudo_dir='./pseudo', tprnfor=.true., tstress=.true., disk_io='low',
/
&SYSTEM
  ibrav=0, nat={nat}, ntyp={len(els)}, ecutwfc=70, ecutrho=560,
  occupations='fixed',
/
&ELECTRONS
  conv_thr=1.0d-10, electron_maxstep=200, mixing_beta=0.3,
/
ATOMIC_SPECIES
"""
for e in els: s += f"  {e} {MASS[e]} {PS[e]}\n"
s += "CELL_PARAMETERS angstrom\n"
for i in range(3): s += "  " + " ".join(f"{cell[3*i+j]:.10f}" for j in range(3)) + "\n"
s += "ATOMIC_POSITIONS angstrom\n"
for e, p in zip(sym, pos): s += f"  {e} {p[0]} {p[1]} {p[2]}\n"
s += "K_POINTS automatic\n  4 4 4 0 0 0\n"
open(os.path.join(out, "scf_paw.in"), "w").write(s)
print(f"[scf_paw.in] nat={nat} ntyp={len(els)} kjpaw ecut70/560 k444 fixed-occ")
PYC

# ---- 3) SCF ---------------------------------------------------------------
if [ ! -s scf_paw.out ] || ! grep -qa "convergence has been achieved" scf_paw.out; then
  echo "[$(ts)] pw.x scf_paw.in (CPU -np $NP)"
  "$MPIRUN" $MPIFLAGS -np "$NP" "$CPU/pw.x" -in scf_paw.in > scf_paw.out 2>&1
fi
# ⚠ 가짜 수렴 검사 — electron_maxstep 도달 시 QE 도 'achieved' 를 찍는 설정이 있다
NIT=$(grep -ao "convergence has been achieved in *[0-9]*" scf_paw.out | tail -1 | grep -o '[0-9]*$')
echo "[$(ts)] SCF 수렴 반복수 = ${NIT:-?} (electron_maxstep=200 과 같으면 **가짜 수렴**)"
grep -qa "convergence has been achieved" scf_paw.out || { echo "ERROR: SCF 미수렴 — scf_paw.out 확인"; exit 1; }

# ---- 4) pp.x plot_num=17 (AE valence+core reconstruction) -----------------
# ⚠ **17 이어야 기존 표와 같은 양**이다. 0(가전자)로 바꾸면 비교가 깨진다.
if [ ! -s lpsocl_rho_ae.cube ]; then
cat > pp_ae.in <<'EOF'
&INPUTPP
  prefix='lpsocl_paw', outdir='./out_paw', plot_num=17, filplot='lpsocl_ae'
/
&PLOT
  iflag=3, output_format=6, fileout='lpsocl_rho_ae.cube'
/
EOF
  echo "[$(ts)] pp.x plot_num=17 (AE)"
  "$MPIRUN" $MPIFLAGS -np "$NP" "$CPU/pp.x" -in pp_ae.in > pp_ae.out 2>&1
fi
[ -s lpsocl_rho_ae.cube ] || { echo "ERROR: AE cube 생성 실패 — pp_ae.out 확인"; exit 1; }

# ---- 5) Bader ------------------------------------------------------------
BADER=$(command -v bader || ls /data/apps/bader/bader /data/apps/bader 2>/dev/null | head -1)
if [ -z "$BADER" ] || [ ! -x "$BADER" ]; then
  echo "ERROR: bader 실행파일 없음. 설치:"
  echo "  mkdir -p /data/apps/bader && cd /data/apps/bader && \\"
  echo "  wget http://theory.cm.utexas.edu/henkelman/code/bader/download/bader_lnx_64.tar.gz && \\"
  echo "  tar xzf bader_lnx_64.tar.gz && chmod +x bader"
  exit 1
fi
echo "[$(ts)] bader -p all_atom (AE cube)"
"$BADER" -p all_atom lpsocl_rho_ae.cube > bader_run.out 2>&1
[ -s ACF.dat ] || { echo "ERROR: ACF.dat 없음 — bader_run.out 확인"; exit 1; }

# ---- 6) 요약 (원소별 net charge) ------------------------------------------
python3 - "$OUT" "$V0" <<'PYC'
import sys, os, re, json
from collections import defaultdict
out, v0 = sys.argv[1], sys.argv[2]
L = open(v0).read().splitlines(); nat = int(L[0].split()[0])
sym = [ln.split()[0] for ln in L[2:2+nat]]
# ZVAL: kjpaw 세트의 가전자 수 (AE plot_num=17 은 core 를 복원하므로 총 Z 를 쓴다)
Z = {"Li":3,"P":15,"S":16,"Cl":17,"O":8}
rows = [l.split() for l in open(os.path.join(out,"ACF.dat"))
        if re.match(r"^\s*\d+\s", l)]
per = defaultdict(list)
for s, r in zip(sym, rows):
    per[s].append(Z[s] - float(r[4]))          # net = Z - Bader charge
res = {"method": "AE density plot_num=17, PAW kjpaw_psl, ecut 70/560, k444, fixed-occ",
       "note": "기존 bader_b2o3_vs_lpscl16.csv 와 **같은 방법** — 비교 가능",
       "per_species": {k: {"n": len(v), "mean": round(sum(v)/len(v), 3),
                           "min": round(min(v), 3), "max": round(max(v), 3)}
                       for k, v in sorted(per.items())}}
open(os.path.join(out, "lpsocl_bader_summary.json"), "w").write(
    json.dumps(res, ensure_ascii=False, indent=2) + "\n")
print("\n원소별 net charge (Z − Bader):")
for k, v in res["per_species"].items():
    print(f"  {k:3s} n={v['n']:3d}  {v['mean']:+.3f}  [{v['min']:+.3f}, {v['max']:+.3f}]")
print(f"\n→ {out}/lpsocl_bader_summary.json  ·  ACF.dat")
PYC
echo "[$(ts)] DONE"
