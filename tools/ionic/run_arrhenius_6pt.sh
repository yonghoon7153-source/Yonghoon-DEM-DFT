#!/usr/bin/env bash
# =============================================================================
# run_arrhenius_6pt.sh — 6점 아레니우스(500-1000 K)를 **세 계 전부 처음부터** 다시
#
# 왜 (1저자 요청 2026-08-03, kb/reports/paper_first_author_requests_2026_08.md §1)
#   지금은 600/800/1000 3점이라 **직선인지 아닌지를 따질 수가 없다**. 6점이면 직선성
#   자체가 증거가 되고 figure 도 산다.
#
# ⚠⚠ **세 계를 같은 온도 집합으로 맞춰야 한다.** 한 계만 6점이고 다른 계가 3점이면
#   Ea 비교(LPSOCl 이 modelc 보다 +90 meV 등)가 **다른 적합끼리의 비교**가 되어 깨진다.
#   B2O3 실증: 고온 3점 Ea 0.207 vs 5점(400-1000) 0.214 — 적합 집합이 값을 바꾼다.
#
# ⚠⚠ **기존 점을 재사용하지 않고 전부 다시 돈다 (2026-08-03 결정).**
#   modelc·b2o3 는 400/500 K 를 이미 갖고 있지만 **단일 시드**다. 그걸 3시드 점들과 섞으면
#   오차막대가 점마다 달라져서, 6점 적합의 가중치를 정할 근거가 사라진다.
#   → 6온도 x 3계 x 3시드 = **54 런**. 모든 점이 같은 3시드 오차막대를 갖는다.
#
# ⚠ 400 K 는 뺀다. 필요 prod 가 323-1279 ps 로(md_temperature_feasibility.py) 200 ps 표준을
#   넘고, 계마다 필요량이 4배 차이 나서 프로토콜 통일이 깨진다. 6점(500-1000)이면 충분하다.
#
# ⚠ prod: 500 K 만 400 ps, 나머지 200 ps. 500 K 필요량이 modelc 103 / b2o3 104 /
#   LPSOCl 242 ps 라 200 ps 로는 LPSOCl 이 모자란다. 계별로 다르게 주면 프로토콜이
#   지저분해지므로 **온도 단위로** 통일한다.
#
#   cd ~/Yonghoon-DEM-DFT && git pull && conda activate uma
#   tmux new -s arr6 -d 'bash tools/ionic/run_arrhenius_6pt.sh 2>&1 | tee -a ~/logs/arr6.log'
#   bash tools/ionic/run_arrhenius_6pt.sh modelc      # 한 계만
#
# 비용(A6000): 54 런. 200 ps ~1.5-2 h, 500 K(400 ps) ~3-4 h → 전체 대략 **4일**.
# =============================================================================
set -euo pipefail; set +H
REPO="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$REPO"
# ⚠ QE 환경변수가 남아 있으면 torch 가 죽는다 (기존 러너와 동일한 처리)
unset LD_LIBRARY_PATH OPAL_PREFIX 2>/dev/null || true
DRIVER=$REPO/tools/modelc_v3/disorder_ensemble_diffusion.py
OUTROOT=${OUTROOT:-$HOME/work/runs/arrhenius_6pt}
DEVICE=${DEVICE:-cuda}
SEEDS=${SEEDS:-"2 3 4"}          # 600 K 오차막대와 같은 시드 집합
ONLY=${1:-all}
mkdir -p "$OUTROOT"

# ── 중복 실행 가드 ──────────────────────────────────────────────────────────
# ⚠ pgrep 으로 세면 tmux 래퍼까지 세서 자기 자신에 걸린다(실측 재발 2회). flock 만 쓴다.
LOCK=${LOCK:-/tmp/arr6.lock}
exec 9>"$LOCK" || { echo "⛔ 락 파일을 못 연다"; exit 1; }
command -v flock >/dev/null 2>&1 && { flock -n 9 || { echo "⛔ 이미 돈다 — 중단"; exit 0; }; }

# ── 계 정의: label · V0 구조 · 500 K 에 필요한 prod(ps) ─────────────────────
#   prod500 은 md_temperature_feasibility.py 의 '실무 필요' 값을 올림한 것.
#   modelc 103 / b2o3 104 → 200 ps 로 충분. LPSOCl 242 → 400 ps.
sys_list() {
  cat <<'EOF'
modelc|db/structures/modelc_V0_k663.xyz
lpsocl|db/structures/lpsocl_relaxV0.xyz
b2o3|db/structures/b2o3_relaxV0.xyz
EOF
}
# 온도:prod(ps). 500 K 만 길다 — 위 주석 참조.
TEMP_PROD="500:400 600:200 700:200 800:200 900:200 1000:200"

ts(){ echo "[$(date +%m-%d\ %H:%M:%S)] $*"; }

# ── 구조 건전성 게이트 (2026-07-17 이중변환 사고 재발 방지) ─────────────────
#   깨진 xyz 로 MD 를 돌리면 폭발해서 D~1e-2 같은 값이 나온다. 최소 원자간 거리로 막는다.
sanity() {
  python3 - "$1" <<'PY'
import sys, re
import numpy as np
L = open(sys.argv[1]).read().splitlines()
nat = int(L[0])
A = np.array([float(x) for x in re.search(r'Lattice="([^"]+)"', L[1]).group(1).split()]).reshape(3, 3)
pos = np.array([[float(x) for x in l.split()[1:4]] for l in L[2:2 + nat]])
inv = np.linalg.inv(A); mind = 9e9
for i in range(nat - 1):
    df = (pos[i + 1:] - pos[i]) @ inv; df -= np.round(df)
    mind = min(mind, np.linalg.norm(df @ A, axis=1).min())
assert mind > 1.2, f"⛔ BROKEN STRUCTURE: 최단 원자간 {mind:.3f} A < 1.2 — 실행 거부"
print(f"   구조 게이트 OK (최단 {mind:.3f} A, nat {nat})")
PY
}

ts "6점 아레니우스 — 500/600/700/800/900/1000 K · 시드 ${SEEDS} · 3계 = 54 런"
ts "⚠ 기존 점을 재사용하지 않는다. 전부 같은 3시드 오차막대를 갖게 처음부터 돈다."

while IFS='|' read -r LABEL XYZ; do
  [ "$ONLY" = all ] || [ "$ONLY" = "$LABEL" ] || continue
  test -f "$REPO/$XYZ" || { ts "⛔ $LABEL: $XYZ 없음 — 건너뜀"; continue; }
  ts "═══ $LABEL ($XYZ) ═══"
  sanity "$REPO/$XYZ"
  for S in $SEEDS; do
    for TP in $TEMP_PROD; do
      T=${TP%%:*}; P=${TP##*:}
      OUT="$OUTROOT/$LABEL/T${T}_s${S}"
      if [ -s "$OUT/msd.json" ]; then ts "  ✓ $LABEL T${T} s${S} 이미 있음 — 건너뜀"; continue; fi
      ts "  ▶ $LABEL  T=${T} K  seed=${S}  prod=${P} ps"
      python3 "$DRIVER" \
        --v0_xyz "$REPO/$XYZ" --label "$LABEL" \
        --out_root "$OUT" \
        --disorder_levels 0.0 --n_configs 1 \
        --temperatures "$T" \
        --equilib_ps 5 --prod_ps "$P" \
        --timestep_fs 2.0 --friction 0.02 \
        --save_fs 100 --fit_window_ps 2 50 \
        --seed "$S" \
        --uma_model uma-s-1p1 --uma_task omat --device "$DEVICE" \
        || ts "  ⚠ $LABEL T${T} s${S} 실패 — 나머지는 계속 간다"
    done
  done
done < <(sys_list)

ts "═══ 완료. 다음: 확산영역 게이트를 **전 점에** 돌린다 ═══"
ts "  python3 tools/ionic/msd_diffusive_check.py --glob '$OUTROOT/*/T*_s*/**/msd.json' --scan"
ts "  ⚠⚠ 게이트를 통과한 점만 아레니우스에 넣는다. 통과 못 한 점을 넣으면"
ts "     그 점이 기울기를 끌어당겨 Ea 가 통째로 틀어진다."
ts "  ⚠ 그리고 **세 계 전부 같은 온도 집합**으로 다시 적합해야 Ea 비교가 산다."
