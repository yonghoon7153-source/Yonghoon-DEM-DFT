#!/usr/bin/env bash
# =============================================================================
# run_comp2_saddle_check_kgy.sh — comp2 champion V0 vs UMA followmin, DFT 판정.
#
# UMA 판정: V0는 Li-부격자 안장점, followmin이 -535 meV/cell 낮음 (2026-07-21).
# DFT(같은 셀·같은 세팅 단일점 페어)로 방향 확인 — ΔE_DFT < 0 이면 champion
# 교체 안건 확정. 세팅: PSlibrary kjpaw PAW, ecut 60/480, k 2x2x2, mv 0.01
# (두 점 동일 조건이라 ΔE에서 상쇄; 절대값 인용용 아님).
#
# kgy:  bash tools/electronic/run_comp2_saddle_check_kgy.sh
#   (GPU 대기 내장; followmin은 ~/work/comp2_phonon/comp2_followmin_best.xyz)
# =============================================================================
set -u; set +H
REPO=${REPO:-$HOME/Yonghoon-DEM-DFT}
WORK=${WORK:-$HOME/work/comp2_saddle_check}; mkdir -p "$WORK"
FMIN=${FMIN:-$HOME/work/comp2_phonon/comp2_followmin_best.xyz}
[ -f "$FMIN" ] || { echo "ERROR: $FMIN 없음 — phonon 재실행(followmin 저장)부터"; exit 1; }

# ---- pseudos (vgcf 러너와 같은 PSlibrary kjpaw 계열 + Br) ----
PSE=$WORK/pseudo; mkdir -p "$PSE"
NEED="Li.pbe-s-kjpaw_psl.1.0.0.UPF P.pbe-n-kjpaw_psl.1.0.0.UPF S.pbe-n-kjpaw_psl.1.0.0.UPF Cl.pbe-n-kjpaw_psl.1.0.0.UPF Br.pbe-n-kjpaw_psl.1.0.0.UPF"
BASE="https://pseudopotentials.quantum-espresso.org/upf_files"
for p in $NEED; do
  [ -s "$PSE/$p" ] && continue
  f=$(find "$HOME" -name "$p" 2>/dev/null | head -1)
  if [ -n "$f" ]; then cp "$f" "$PSE/"; echo "[pseudo] $p <- $f"
  else echo "[pseudo] wget $p"; wget -q "$BASE/$p" -O "$PSE/$p" || true
    [ -s "$PSE/$p" ] || { echo "!! $p 확보 실패 — kgy UPF 목록 붙여줘"; exit 1; }
  fi
done

# ---- 입력 생성 (V0 cif + followmin xyz -> 동일 세팅 scf 페어) ----
python3 - "$REPO/db/structures/comp2_V0.cif" "$FMIN" "$WORK" "$PSE" <<'PY'
import sys
import numpy as np
from ase.io import read
v0p, fmp, work, pse = sys.argv[1:5]
mass = {"Li": 6.94, "P": 30.97, "S": 32.06, "Cl": 35.45, "Br": 79.904}
ups = {"Li": "Li.pbe-s-kjpaw_psl.1.0.0.UPF", "P": "P.pbe-n-kjpaw_psl.1.0.0.UPF",
       "S": "S.pbe-n-kjpaw_psl.1.0.0.UPF", "Cl": "Cl.pbe-n-kjpaw_psl.1.0.0.UPF",
       "Br": "Br.pbe-n-kjpaw_psl.1.0.0.UPF"}
for tag, path in (("V0", v0p), ("followmin", fmp)):
    a = read(path)
    syms = a.get_chemical_symbols()
    order = [e for e in ("Li", "P", "S", "Cl", "Br") if e in syms]
    spec = "\n".join(f"  {e:2s} {mass[e]:7.3f}  {ups[e]}" for e in order)
    cell = "\n".join("  " + " ".join(f"{x:14.8f}" for x in r) for r in a.cell.array)
    pos = "\n".join(f"  {s:2s} {p[0]:14.8f} {p[1]:14.8f} {p[2]:14.8f}"
                    for s, p in zip(syms, a.get_positions()))
    inp = f"""&CONTROL
  calculation='scf', prefix='c2_{tag}', outdir='./tmp_{tag}',
  pseudo_dir='{pse}', tprnfor=.true., disk_io='low'
/
&SYSTEM
  ibrav=0, nat={len(a)}, ntyp={len(order)}, ecutwfc=60, ecutrho=480,
  occupations='smearing', smearing='mv', degauss=0.01
/
&ELECTRONS
  conv_thr=1d-8, mixing_beta=0.3, electron_maxstep=200
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
    open(f"{work}/scf_{tag}.in", "w").write(inp)
    print(f"[in] scf_{tag}.in  nat={len(a)}")
PY
[ $? -eq 0 ] || exit 1

# ---- qegpu env (vgcf 러너와 동일) + GPU 대기 ----
while pgrep -f 'pw\.x|neb\.x|comp_phonon_uma' >/dev/null 2>&1; do
  echo "[$(date +%H:%M:%S)] GPU 사용중 — 3분 뒤 재확인"; sleep 180
done
PW=${PW:-$(find "$HOME/apps" -maxdepth 4 -name pw.x -path "*qe*gpu*bin*" 2>/dev/null | head -1)}
[ -n "$PW" ] || { echo "ERROR: pw.x 못찾음"; exit 1; }
NV="$HOME/apps/nvhpc/Linux_x86_64/24.11"
HPCX="$(ls -d "$NV"/comm_libs/*/hpcx/hpcx-*/ompi 2>/dev/null | sort | tail -1)"
export OPAL_PREFIX="$HPCX" OMP_NUM_THREADS=1
export LD_LIBRARY_PATH="$NV/compilers/lib:$NV/cuda/12.6/lib64:$NV/math_libs/lib64:$HPCX/lib:${LD_LIBRARY_PATH:-}"
MPIRUN="$HPCX/bin/mpirun"

cd "$WORK"
for tag in V0 followmin; do
  grep -aq "JOB DONE" "scf_${tag}.out" 2>/dev/null && { echo "[$tag] done skip"; continue; }
  echo "[$(date +%H:%M:%S)] pw.x scf_${tag}"
  "$MPIRUN" -np 1 "$PW" -in "scf_${tag}.in" > "scf_${tag}.out" 2>&1
  grep -aq "JOB DONE" "scf_${tag}.out" || { echo "[$tag] FAIL:"; tail -12 "scf_${tag}.out"; exit 1; }
done

echo; echo "===== DFT VERDICT ====="
python3 - "$WORK" <<'PY'
import re, sys
Ry = 13.605693
W = sys.argv[1]
E = {}
for tag in ("V0", "followmin"):
    t = open(f"{W}/scf_{tag}.out").read()
    E[tag] = float(re.findall(r"^!\s+total energy\s+=\s+(-\d+\.\d+)", t, re.M)[-1])
    print(f"  E({tag}) = {E[tag]:.6f} Ry")
d = (E["followmin"] - E["V0"]) * Ry
print(f"  ΔE(DFT) = E(followmin) − E(V0) = {d*1000:+.1f} meV/cell ({d*1000/52:+.2f} meV/atom)")
print("  →", "DFT도 followmin이 낮음 — champion 교체 안건 확정 (UMA −535와 방향 일치)" if d < -0.01
      else "DFT는 V0 유지 — UMA 편향 사례로 기록")
PY
echo ">> 출력 붙여주면 판정 등록 + (확정 시) followmin DFT-relax 후속"
