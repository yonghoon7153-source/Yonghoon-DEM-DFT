#!/usr/bin/env bash
# =============================================================================
# run_arrhenius_6pt.sh — 6점 아레니우스(500-1000 K) 완성용 **30 런** (신규 27 + lpsocl 600 재실행 3)
#
# 왜 (1저자 요청 2026-08-03, kb/reports/paper_first_author_requests_2026_08.md §1)
#   지금은 600/800/1000 3점이라 **직선인지 아닌지를 따질 수가 없다**. 6점이면 직선성
#   자체가 증거가 되고 figure 도 산다.
#
# ⚠⚠ **세 계를 같은 온도 집합으로 맞춰야 한다.** 한 계만 6점이고 다른 계가 3점이면
#   Ea 비교(LPSOCl 이 modelc 보다 +90 meV 등)가 **다른 적합끼리의 비교**가 되어 깨진다.
#   B2O3 실증: 고온 3점 Ea 0.207 vs 5점(400-1000) 0.214 — 적합 집합이 값을 바꾼다.
#
# ~~⚠⚠ 기존 점을 재사용하지 않고 전부 다시 돈다 (2026-08-03 결정) → 54 런~~
# **[개정 2026-08-04 — 사용자 결정: 30 런]** 54 의 근거("기존 400/500 이 단일시드")는
#   맞았지만, v2 게이트 검사(msd_3sys_200ps 작업)로 **기존 600/800/1000 멀티시드 점이
#   9칸 중 8칸 게이트 통과**임이 확인됐다 (modelc 0.87/0.93/0.92 · b2o3 0.81/0.83/0.97 ·
#   lpsocl 0.61⛔/0.86/1.02). 멀쩡한 칸을 다시 돌 이유가 없다.
#   → **신규 온도 27 런 (500/700/900 x 3계 x 3시드) + lpsocl 600 K 재실행 3 런 = 30 런.**
#   기존 점 위치(최종 적합 때 합친다):
#     modelc 600  = kgy  ~/work/runs/modelc_600_reseed        (3시드 200 ps)
#     modelc hiT  = kgy  ~/work/runs/highT_reseed/modelc      (3시드 100 ps)
#     b2o3  600   = gabia /data/work/b2o3md/runs/b2o3_600_reseed (3시드 200 ps)
#     b2o3  hiT   = kgy  ~/work/runs/highT_reseed/b2o3        (3시드 100 ps)
#     lpsocl 800/1000 = kgy ~/work/runs/lpsocl_md             (4시드 200 ps)
#   ⚠ 각주 의무: 기존 hiT 는 100 ps(창 2-50 완전 포함이라 D 동일)·MTO 없음.
#     신규 30 런만 MTO 를 갖는다 — 재적합 감사에서 섞어 볼 때 명시할 것.
#
# ⚠ 400 K 는 뺀다. 필요 prod 가 323-1279 ps 로(md_temperature_feasibility.py) 200 ps 표준을
#   넘고, 계마다 필요량이 4배 차이 나서 프로토콜 통일이 깨진다. 6점(500-1000)이면 충분하다.
#
# ⚠ prod: 500 K 만 400 ps, 나머지 200 ps. 500 K 필요량이 modelc 103 / b2o3 104 /
#   LPSOCl 242 ps 라 200 ps 로는 LPSOCl 이 모자란다. 계별로 다르게 주면 프로토콜이
#   지저분해지므로 **온도 단위로** 통일한다.
#
# ── 적합 창에 대하여 (1저자 질문 2026-08-03: "fit 을 2-50 까지만 하는 게 맞아?") ──
#   창은 이 실행을 **붙잡지 않는다.** msd.json 이 times_ps/msd_Li_A2 **시계열 전체**를
#   저장하므로 창은 나중에 재계산 없이 바꿀 수 있다:
#     python3 tools/ionic/msd_refit_window.py --glob '<OUTROOT>/*/T*_s*/**/msd.json'
#   실측 근거로 2-50 을 유지한다 — LPSOCl 200 ps 는 창을 2-50 에서 100-200 으로 옮겨도
#   기울기가 2 % 만 변하고(beta 0.98→1.02) Ea 가 안 움직인다. 반대로 창을 늦춰 '구제'
#   하려 들면 modelc 100 ps 에서 Ea 0.223(R^2 0.992) → 0.155(R^2 0.875) 로 **나빠진다**.
#   창이 아니라 **통계**가 문제이기 때문이다(62원자 셀에 Li 27개, 시간원점 1개).
#
# ★ 그래서 이번 신규 30 런부터는 msd.json 에 **다중 시간원점 MSD**(msd_Li_A2_mto)가 같이
#   쓰인다 — 같은 MD 에서 산포가 ~2.9배 줄어든다(추가 비용·디스크 0, 합성시험 검증).
#   기존 런은 프레임을 안 남겨서 소급 적용이 안 된다. 재적합 감사는 --mto 로 본다.
#
#   cd ~/Yonghoon-DEM-DFT && git pull && conda activate uma
#   tmux new -s arr6 -d 'bash tools/ionic/run_arrhenius_6pt.sh 2>&1 | tee -a ~/logs/arr6.log'
#   bash tools/ionic/run_arrhenius_6pt.sh modelc      # 한 계만
#
# 비용: 30 런. 200 ps ~1.5-2 h, 500 K(400 ps) ~3-4 h → 전체 대략 **2일** (구 54런 4일).
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
#   기본 = 신규 온도만 (30런 계획). 전면 재실행(구 54런)을 원하면:
#     TEMP_PROD="500:400 600:200 700:200 800:200 900:200 1000:200" LPSOCL_EXTRA="" bash ...
TEMP_PROD=${TEMP_PROD:-"500:400 700:200 900:200"}
# lpsocl 만 600 K 재실행 — 4시드 200 ps 앙상블 beta 0.61 게이트 탈락(2026-08-04 v2)의 재판정.
#   신규 런은 MTO(다중 시간원점)가 있어 beta 추정 산포가 ~2.9배 작다.
LPSOCL_EXTRA=${LPSOCL_EXTRA:-"600:200"}

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

ts "6점 아레니우스 30런 계획 — 신규 ${TEMP_PROD} x 3계 x 시드(${SEEDS}) + lpsocl [${LPSOCL_EXTRA}]"
ts "기존 600/800/1000 멀티시드 점은 게이트 통과 확인(2026-08-04 v2) — 재사용. lpsocl 600 만 재실행."

while IFS='|' read -r LABEL XYZ; do
  [ "$ONLY" = all ] || [ "$ONLY" = "$LABEL" ] || continue
  test -f "$REPO/$XYZ" || { ts "⛔ $LABEL: $XYZ 없음 — 건너뜀"; continue; }
  ts "═══ $LABEL ($XYZ) ═══"
  sanity "$REPO/$XYZ"
  TP_LIST="$TEMP_PROD"
  [ "$LABEL" = "lpsocl" ] && [ -n "$LPSOCL_EXTRA" ] && TP_LIST="$TEMP_PROD $LPSOCL_EXTRA"
  for S in $SEEDS; do
    for TP in $TP_LIST; do
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
ts "  ⚠ 최종 6점 적합 = 신규(이 OUTROOT) + 기존 멀티시드 점(헤더의 위치 목록) 결합."
ts "     lpsocl 600 K 는 **신규 MTO-beta ≥ 0.8 일 때만** 넣는다 — 아니면 5점 + 1600 ps 프로브."
ts ""
ts "═══ 그리고 창 민감도를 SI 용으로 남긴다 (1저자 질문 §3) ═══"
ts "  python3 tools/ionic/msd_refit_window.py --glob '$OUTROOT/*/T*_s*/**/msd.json' \\"
ts "      --csv db/properties/msd_window_sensitivity.csv"
ts "  python3 tools/ionic/msd_refit_window.py --glob '$OUTROOT/*/T*_s*/**/msd.json' --mto"
ts "  ⚠ 2-50 창 D 와 MTO D 가 크게 다른 점은 **그 점의 통계가 모자란 것**이지"
ts "    창을 바꿔서 해결할 문제가 아니다. 시드/시간을 늘려야 한다."
