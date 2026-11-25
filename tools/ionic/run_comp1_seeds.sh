#!/usr/bin/env bash
# =============================================================================
# comp1 (Li6PS5Cl, 52-atom ordered) MD conductivity — 멀티시드 보강 (open_items #1)
#
# 목적: modelc Ea 정본 충돌(0.2235 단일 deck vs 0.197±0.032 3-seed)을 닫기 위한
#   comp1 시드 보강. 기존 deck 궤적(driver 기본 seed 1234; Ea 0.2532, D600 3.09e-06 /
#   D800 1.03e-05 / D1000 2.20e-05, li_transport.json headline_PAPER_GRADE)에
#   seed 2/3 x 3T를 추가 → 3-seed 완성 → 전 조성 멀티시드 통일 후
#   modelc 0.197±0.032 를 정본 확정 (AIMD 불필요 판정 근거는 kb/open_items.md).
#
# 프로토콜 = md_conductivity_protocol 정확 미러 (run_comp2_md.sh 와 동일):
#   UMA-s-1p1 (omat), Langevin NVT, dt 2 fs, friction 0.02, equilib 5 ps,
#   prod 200 ps, save_fs 100, MSD window 2-50 ps, Arrhenius 600/800/1000 K.
# n_Li = 2.3608e22 cm-3 (24 Li / 1016.62 A^3, a=10.0551) — NE 단계용.
#
# ★ CHAIN 모드: gabia에서 comp2 disorder ensemble(LEVELS=0.5)이 도는 동안 걸어두면
#   그게 끝난 뒤 자동 시작한다. SDCP pw.x(k221, VRAM ~46 GB)와의 공존은 VRAM 게이트로
#   판단 — disorder 슬롯(~1.2 GB)이 비면 free ~2.3 GB라 UMA 52at(~1.2 GB)가 들어간다.
#   (pw.x 종료를 기다리지 않는다: disorder MD가 이미 같은 조건에서 공존했음.)
#
# 실행 (gabia, uma env 셸):
#   cd ~/Yonghoon-DEM-DFT && git fetch origin claude/friendly-meitner-lldvar \
#     && git checkout FETCH_HEAD -- tools/ionic/run_comp1_seeds.sh
#   PY=$(which python3)
#   tmux new -s c1md -d "PY=$PY bash tools/ionic/run_comp1_seeds.sh > ~/work/comp1_seeds.log 2>&1"
# 예상: 6 x 205 ps, ~15 h (A6000).
# =============================================================================
set -euo pipefail; set +H
REPO="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$REPO"
unset LD_LIBRARY_PATH OPAL_PREFIX 2>/dev/null || true   # QE env 잔재가 torch 오염
V0XYZ=${V0XYZ:-$REPO/db/structures/comp1_V0_k444.xyz}   # deck 궤적과 동일 구조 (52at, a=10.0551)
OUTROOT=${OUTROOT:-$HOME/work/runs/comp1_seeds}
# ⚠⚠ **확산영역 게이트 대응 (2026-08-01).** prod 200 ps 로는 저이동도 계에서 MSD 가
#   확산 영역에 못 간다 — comp1 seeds 6/6 케이지(β 0.17–0.79), 창 변경·시드 평균 어느
#   쪽으로도 구제 안 됨(kb/results/mlip_md_diffusive_gate_2026_08_01.md).
#   PRODPS 로 시간을 늘려 재시도한다. ⚠ **OUTROOT 를 반드시 바꿔라** — 드라이버가
#   resume-safe 라 기존 msd.json 이 있으면 **그냥 건너뛴다**(200 ps 결과가 남아버린다).
PRODPS=${PRODPS:-200}
SEEDS=${SEEDS:-"2 3"}
DEVICE=${DEVICE:-cuda}
PY=${PY:-python3}
DRIVER=$REPO/tools/modelc_v3/disorder_ensemble_diffusion.py
test -f "$V0XYZ" || { echo "MISSING $V0XYZ -- git pull first"; exit 1; }

# 중복실행 가드
[ "$(pgrep -fc run_comp1_seeds.sh)" -le 3 ] || { echo "이미 실행중 — 종료"; exit 1; }

# ---- CHAIN 대기 ①: comp2 disorder ensemble (disorder_levels 0.5) 종료까지 ----
# 우리 자신은 --disorder_levels 0.0 으로 돌므로 패턴이 자기 자신을 잡지 않는다.
while [ "${SKIP_WAIT:-0}" != 1 ] && pgrep -f 'run_comp2_disorder|disorder_levels 0.5' >/dev/null 2>&1; do
  echo "[$(date +%H:%M:%S)] comp2 disorder ensemble 진행중 — 10분 뒤 재확인"; sleep 600
done
# ---- CHAIN 대기 ②: VRAM 게이트 (SDCP pw.x 공존 대비, free >= 2000 MiB) ----
while [ "${SKIP_WAIT:-0}" != 1 ]; do
  FREE=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits 2>/dev/null | head -1)
  [ -z "$FREE" ] && { echo "nvidia-smi 실패 — 60s 뒤 재시도"; sleep 60; continue; }
  [ "$FREE" -ge 2000 ] && { echo "[$(date +%H:%M:%S)] VRAM free ${FREE} MiB — 시작"; break; }
  echo "[$(date +%H:%M:%S)] VRAM free ${FREE} MiB < 2000 — 5분 뒤 재확인 (pw.x 점유 중일 수 있음)"; sleep 300
done
echo "[$(date +%H:%M:%S)] chain 조건 충족 — comp1 seed(s) '$SEEDS' 시작 (prod ${PRODPS} ps)"
echo "[$(date +%H:%M:%S)]   OUTROOT=$OUTROOT"
if [ "$PRODPS" != 200 ] && [ "$OUTROOT" = "$HOME/work/runs/comp1_seeds" ]; then
  echo "⛔ PRODPS 를 바꿨는데 OUTROOT 가 기본값이다 — 기존 msd.json 때문에 전부 skip 된다."
  echo "   OUTROOT=$HOME/work/runs/comp1_seeds_p${PRODPS} 처럼 따로 줘라."; exit 1
fi

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

# ---- 2 seed x 3 T (resume-safe: 완료 seed는 json 있으면 skip) ----
# deck 궤적(seed 1234)이 1번 시드 역할 — 여기선 2, 3만 돌린다.
for S in $SEEDS; do
  if [ -f "$OUTROOT/s${S}/ensemble_results.json" ]; then
    echo "[s${S}] ensemble_results.json 있음 — skip"; continue
  fi
  echo "===== seed ${S} : 600/800/1000 K (prod 200 ps each) ====="
  $PY "$DRIVER" \
    --v0_xyz "$V0XYZ" --label comp1 \
    --out_root "$OUTROOT/s${S}" \
    --disorder_levels 0.0 --n_configs 1 \
    --temperatures 600 800 1000 \
    --equilib_ps 5 --prod_ps "$PRODPS" \
    --timestep_fs 2.0 --friction 0.02 \
    --save_fs 100 --fit_window_ps 2 50 \
    --seed ${S} \
    --uma_model uma-s-1p1 --uma_task omat --device "$DEVICE"
done

echo ""; echo "===== collect: deck(1234) + s2 + s3 → 3-seed Ea ====="
$PY - "$OUTROOT" <<'PYC'
import json, os, sys
import numpy as np
root = sys.argv[1]
kB = 8.617333262e-5
x = 1.0 / np.array([600.0, 800.0, 1000.0])
# deck 궤적 (driver 기본 seed 1234) — li_transport.json headline_PAPER_GRADE 등록값
runs = {"deck(1234)": [3.09e-06, 1.03e-05, 2.20e-05]}
for s in (2, 3):
    p = os.path.join(root, f"s{s}", "ensemble_results.json")
    if not os.path.exists(p):
        print(f"s{s}: 미완"); continue
    runs[f"s{s}"] = json.load(open(p))["levels"][0]["configs"][0]["D_per_T"]
ea = []
for tag, D in runs.items():
    m, b = np.polyfit(x, np.log(D), 1)
    ea.append(-m * kB)
    print(f"{tag}: D(600/800/1000) = " + ", ".join(f"{d:.4e}" for d in D) + f"   Ea = {-m*kB:.4f} eV")
if len(ea) == 3:
    print(f"\ncomp1 Ea = {np.mean(ea):.3f} +/- {np.std(ea, ddof=1):.3f} eV (3-seed x 3-T)")
    print("멀티시드 앵커 완성: modelc 0.197+/-0.032 / b2o3 0.199+/-0.034 / lpsocl 0.271+/-0.033")
    print(">> 다음: modelc 0.197+/-0.032 정본 확정 + 단일 deck 앵커 SUPERSEDED 처리 (kb/open_items.md #1)")
PYC
echo ">> 붙여주면 db 등록 + open_items #1 닫기"
