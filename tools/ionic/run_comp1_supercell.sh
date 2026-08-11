#!/usr/bin/env bash
# =============================================================================
# run_comp1_supercell.sh — comp1 **셀 확대 사다리** (open_items #1 의 남은 수)
#
# 왜 (2026-08-06 판정, kb/open_items.md #1)
#   comp1 은 **시간으로 못 닫는다**가 실측으로 끝났다:
#     200 ps  6/6 케이지 (β 0.17–0.79)
#     1600 ps (8배, 같은 시드) → 600 K β **0.64 → 0.37 로 더 나빠짐**, 1000 K 만 통과
#     창 재적합·MTO 어느 쪽도 구제 아님
#   → 남은 가설은 하나다: **62원자 셀에 Li 24개라 평균낼 표본이 없다.**
#
# ⚠⚠ 그래서 이 실행은 "한 점 더 찍기" 가 아니라 **가설 검정**이다. 사다리로 돈다:
#
#     셀        원자   Li    비용(600 K 200 ps 기준)   기대
#     1×1×1      52    24    (이미 있음)               β 0.64
#     2×1×1     104    48    ~5 h                      ↑?
#     2×2×1     208    96    ~10 h                     ↑?
#     2×2×2     416   192    ~20 h                     ≥0.80 이면 가설 성립
#
#   · β 가 Li 개수에 따라 **단조 증가**하면 → 원인은 통계였다. 가설 성립.
#   · β 가 0.65 언저리에서 **평평하면** → 진짜 케이지다. 가설 기각, 셀 확대도 답이 아니다.
#   어느 쪽이든 결론이 난다. 2×2×2 한 점만 찍으면 "올랐다/안 올랐다" 밖에 못 말한다.
#
# ⚠ 타일링은 **물리를 안 바꾼다** — 같은 결정·같은 n_Li 다(드라이버가 밀도를 검산하고
#   어긋나면 즉사한다). 바뀌는 건 MSD 를 평균낼 이온 수뿐이다. 그게 이 검정의 전제다.
#
# ⚠ 600 K 만 먼저 돈다. 600 K 가 판정의 병목이고(800/1000 은 이미 통과하거나 근접),
#   여기서 가설이 기각되면 800/1000 은 돌 이유가 없다. 통과하면 TEMPS 로 확장한다.
#
#   cd ~/Yonghoon-DEM-DFT && conda activate uma
#   git fetch origin claude/friendly-meitner-lldvar && \
#     git checkout FETCH_HEAD -- tools/ionic/run_comp1_supercell.sh tools/modelc_v3/disorder_ensemble_diffusion.py
#   tmux new -s c1sc -d 'bash tools/ionic/run_comp1_supercell.sh 2>&1 | tee -a ~/logs/c1sc.log'
#
#   LADDER="2x1x1 2x2x1"  bash tools/ionic/run_comp1_supercell.sh   # 일부만
#   TEMPS="600 800 1000"  bash tools/ionic/run_comp1_supercell.sh   # 가설 성립 후 확장
# =============================================================================
set -euo pipefail; set +H
REPO="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$REPO"
unset LD_LIBRARY_PATH OPAL_PREFIX 2>/dev/null || true   # QE env 잔재가 torch 를 오염시킨다
DRIVER=$REPO/tools/modelc_v3/disorder_ensemble_diffusion.py
V0XYZ=${V0XYZ:-$REPO/db/structures/comp1_V0_k444.xyz}
OUTROOT=${OUTROOT:-$HOME/work/runs/comp1_supercell}
LADDER=${LADDER:-"2x1x1 2x2x1 2x2x2"}
TEMPS=${TEMPS:-600}
PRODPS=${PRODPS:-200}          # ⚠ 캠페인 표준. 시간을 늘리는 실험이 아니다 — 셀을 늘린다
SEED=${SEED:-2}                # 사다리 1단계는 시드 하나로 본다(경향만 보면 된다)
DEVICE=${DEVICE:-cuda}
PY=${PY:-python3}
test -f "$V0XYZ" || { echo "⛔ 없음: $V0XYZ — git pull 먼저"; exit 1; }
test -f "$DRIVER" || { echo "⛔ 없음: $DRIVER"; exit 1; }

# ── 중복 실행 가드 (flock 만 쓴다 — pgrep 은 tmux 래퍼까지 세서 자기 자신에 걸린다) ──
LOCK=${LOCK:-/tmp/comp1_supercell.lock}
exec 9>"$LOCK" || { echo "⛔ 락 파일을 못 연다"; exit 1; }
command -v flock >/dev/null 2>&1 && { flock -n 9 || { echo "⛔ 이미 돈다 — 중단"; exit 0; }; }

ts(){ echo "[$(date +%m-%d\ %H:%M:%S)] $*"; }
mkdir -p "$OUTROOT"

ts "comp1 셀 확대 사다리 — 사다리 [$LADDER] · T [$TEMPS] K · prod ${PRODPS} ps · seed $SEED"
ts "V0 $V0XYZ → $OUTROOT"

for SC in $LADDER; do
  NA=${SC%%x*}; REST=${SC#*x}; NB=${REST%%x*}; NC=${REST##*x}
  d="$OUTROOT/sc${SC}_s${SEED}"
  # 드라이버는 resume-safe 라 msd.json 이 있으면 건너뛴다 — 사다리 칸마다 폴더를 나눈다
  if [ -f "$d/ensemble_results.json" ] && grep -aq '"Ea_eV"\|"D_Li_cm2_s"' "$d/ensemble_results.json" 2>/dev/null; then
    ts "  ✓ $SC 이미 있음 — 건너뜀 ($d)"
    continue
  fi
  ts "═══ $SC  (${NA}×${NB}×${NC}) ═══"
  mkdir -p "$d"
  $PY "$DRIVER" \
      --v0_xyz "$V0XYZ" --supercell "$NA" "$NB" "$NC" \
      --label "comp1_sc${SC}" --out_root "$d" \
      --disorder_levels 0.0 --n_configs 1 \
      --temperatures $TEMPS \
      --equilib_ps 5 --prod_ps "$PRODPS" --timestep_fs 2 --friction 0.02 \
      --save_fs 100 --save_traj \
      --fit_window_ps 2 50 \
      --seed "$SEED" --device "$DEVICE" \
    || { ts "  ⛔ $SC 실패 — 사다리를 여기서 멈춘다 (뒤가 더 비싸다)"; break; }
  ts "  ✅ $SC 끝"
done

ts "═══ 사다리 판정 ═══"
# ⚠ β 는 **저장된 D 스칼라가 아니라 시계열**에서 다시 잰다 — 창 규약(2–50 ps) 고정.
$PY "$REPO/tools/ionic/msd_diffusive_check.py" \
    --glob "$OUTROOT/*/**/msd.json" 2>/dev/null || \
  ts "  (msd_diffusive_check 인자가 다르면 아래로: msd_refit_window.py --glob '$OUTROOT/*/**/msd.json')"
echo
ts "판정 규칙 — 여기서 눈으로 읽지 말고 규칙대로 읽을 것:"
echo "   · β 가 Li 24→48→96→192 에 따라 **단조 증가**하고 192 에서 ≥0.80 → 가설 성립."
echo "     그때만 comp1 Ea 를 셀 확대본으로 다시 낸다(800/1000 K 확장 후)."
echo "   · β 가 0.65 언저리에서 평평 → **가설 기각**. 셀 확대도 답이 아니다 —"
echo "     open_items #1 에 그렇게 적고 comp1 Ea 는 계속 인용 보류로 둔다."
echo "   ⛔ '192 만 통과' 는 애매하다 — 사다리 전체를 보고 말할 것."
