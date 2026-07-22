#!/usr/bin/env bash
# =============================================================================
# comp2 (Li6PS5Cl0.5Br0.5, 52-atom, DFT-confirmed champion) MD conductivity — 3-seed x 3-T 완전판
# -- md_conductivity_protocol 정확 미러 (lpsocl/b2o3/modelc와 동일 판정 조건):
#    UMA-s-1p1 (omat), Langevin NVT, dt 2 fs, friction 0.02, equilib 5 ps,
#    prod 200 ps, save_fs 100, MSD window 2-50 ps, Arrhenius 600/800/1000 K.
#    lpsocl 교훈 반영: 처음부터 seed 2/3/4 x 3T (ladder 단일시드 단계 생략 —
#    Ea 오차막대가 한 번에 완성, json 이중 갱신 불필요).
# n_Li = 2.3132e22 cm-3 (24 Li / 1037.54 A^3) — Nernst-Einstein 단계용.
#
# kgy (RTX3090) 또는 gabia (A6000), uma env 활성 셸에서. GPU 대기 내장:
# pw.x/neb.x/phonon 끝나면 자동 시작. SKIP_WAIT=1 로 우회 가능(CPU-only pw.x가 돌 때 —
# 예: gabia LPSOCl ELF는 CPU라 GPU 안 씀, nvidia-smi로 GPU 빈 것 확인 후 SKIP_WAIT=1).
#   cd ~/Yonghoon-DEM-DFT && git pull   # (or checkout)
#   PY=$(which python3)   # (uma) 셸
#   tmux new -s c2md -d "PY=$PY bash tools/ionic/run_comp2_md.sh > ~/work/comp2_md.log 2>&1"
# 예상: 9 x 205 ps, ~하루 (A6000/3090).
# =============================================================================
set -euo pipefail; set +H
REPO="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$REPO"
unset LD_LIBRARY_PATH OPAL_PREFIX 2>/dev/null || true   # QE env 잔재가 torch 오염
V0XYZ=${V0XYZ:-$REPO/db/structures/comp2_V0_v3_candidate.xyz}   # DFT-confirmed champion (UMA followmin, -508.7 meV/cell 2026-07-22). MD엔 UMA-relaxed 기하가 정답
OUTROOT=${OUTROOT:-$HOME/work/runs/comp2_md}
DEVICE=${DEVICE:-cuda}
PY=${PY:-python3}
DRIVER=$REPO/tools/modelc_v3/disorder_ensemble_diffusion.py
test -f "$V0XYZ" || { echo "MISSING $V0XYZ -- git pull first"; exit 1; }

# GPU 선점 대기 (QE relax/NEB/phonon 스크린). SKIP_WAIT=1 이면 건너뜀
# (GPU가 nvidia-smi로 비어있음을 확인했고, 도는 pw.x가 CPU-only일 때만 사용)
while [ "${SKIP_WAIT:-0}" != 1 ] && pgrep -f 'pw\.x|neb\.x|comp_phonon_uma' >/dev/null 2>&1; do
  echo "[$(date +%H:%M:%S)] GPU 사용중(pw.x/neb.x/phonon) — 5분 뒤 재확인 (GPU 비었으면 SKIP_WAIT=1로 재실행)"; sleep 300
done
echo "[$(date +%H:%M:%S)] GPU free — comp2 MD 시작"

# 구조 sanity gate (2026-07-17 double-transform 사고 방지 관례)
$PY - "$V0XYZ" <<'PYS'
import sys, re
import numpy as np
lines = open(sys.argv[1]).read().splitlines()
nat = int(lines[0])
A = np.array([float(x) for x in re.search(r'Lattice="([^"]+)"', lines[1]).group(1).split()]).reshape(3, 3)
pos = np.array([[float(x) for x in l.split()[1:4]] for l in lines[2:2 + nat]])
inv = np.linalg.inv(A)
mind = 9e9
for i in range(nat - 1):
    df = (pos[i + 1:] - pos[i]) @ inv
    df -= np.round(df)
    mind = min(mind, np.linalg.norm(df @ A, axis=1).min())
assert mind > 1.2, f"BROKEN STRUCTURE: min-dist {mind:.3f} A < 1.2"
print(f"structure sanity OK: min-dist {mind:.3f} A, nat {nat}")
PYS
mkdir -p "$OUTROOT"

# ---- 3 seed x 3 T (resume-safe: 완료 seed는 json 있으면 skip) ----
for S in 2 3 4; do
  if [ -f "$OUTROOT/s${S}/ensemble_results.json" ]; then
    echo "[s${S}] ensemble_results.json 있음 — skip"; continue
  fi
  echo "===== seed ${S} : 600/800/1000 K (prod 200 ps each) ====="
  $PY "$DRIVER" \
    --v0_xyz "$V0XYZ" --label comp2 \
    --out_root "$OUTROOT/s${S}" \
    --disorder_levels 0.0 --n_configs 1 \
    --temperatures 600 800 1000 \
    --equilib_ps 5 --prod_ps 200 \
    --timestep_fs 2.0 --friction 0.02 \
    --save_fs 100 --fit_window_ps 2 50 \
    --seed ${S} \
    --uma_model uma-s-1p1 --uma_task omat --device "$DEVICE"
done

echo ""; echo "===== collect D values ====="
$PY - "$OUTROOT" <<'PYC'
import json, os, sys
import numpy as np
root = sys.argv[1]
kB = 8.617333262e-5
x = 1.0 / np.array([600.0, 800.0, 1000.0])
ea = []
for s in (2, 3, 4):
    p = os.path.join(root, f"s{s}", "ensemble_results.json")
    if not os.path.exists(p):
        print(f"s{s}: 미완"); continue
    D = json.load(open(p))["levels"][0]["configs"][0]["D_per_T"]
    m, b = np.polyfit(x, np.log(D), 1)
    ea.append(-m * kB)
    print(f"s{s}: D(600/800/1000) = " + ", ".join(f"{d:.4e}" for d in D) + f"   Ea = {-m*kB:.4f} eV")
if len(ea) == 3:
    print(f"\ncomp2 Ea = {np.mean(ea):.3f} +/- {np.std(ea, ddof=1):.3f} eV (3-seed x 3-T)")
    print("anchors: modelc 0.197+/-0.032 / lpsocl 0.271+/-0.033 / b2o3 0.199+/-0.034")
PYC
echo ">> 붙여주면 db 등록 (comp2_md_arrhenius.json) + 4-시스템 Arrhenius 비교"
