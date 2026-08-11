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
# ★★ 2026-08-11 설계 변경 (Codex 재리뷰 + 자체검토) — **1시드 사다리는 판정을 못 한다.**
#   실측: 이 캠페인의 3시드 그룹 7개에서 pooled within-condition SD(β) = **0.1065** 인데
#   사다리가 기대하는 신호는 0.64 → 0.80 = **0.16** 이다. 같은 크기다.
#   → 4칸 × 1시드로는 신호와 시드 잡음을 못 가른다. **양 끝 셀 × 여러 시드**가 맞다.
#     SE(Δβ) ≈ 0.1065·√(2/k).  k=3 → 0.087 (95% 반폭 0.17, 여전히 파일럿)
#                              k=7 → 0.057 (0.16 신호를 80% 검정력으로 잡는다)
#   ⚠ 기준선 β=0.64 는 **다른 런**에서 왔다 — 같은 파이프라인으로 1×1×1 을 다시 재야 한다.
LADDER=${LADDER:-"1x1x1 2x2x2"}      # 기본 = 양 끝. 중간 칸은 끝이 갈린 뒤 채운다
TEMPS=${TEMPS:-600}
PRODPS=${PRODPS:-200}          # ⚠ 캠페인 표준. 시간을 늘리는 실험이 아니다 — 셀을 늘린다
SEEDS=${SEEDS:-"2 3 4"}        # 600 K 오차막대와 같은 시드 집합
DEVICE=${DEVICE:-cuda}
PY=${PY:-python3}
test -f "$V0XYZ" || { echo "⛔ 없음: $V0XYZ — git pull 먼저"; exit 1; }
test -f "$DRIVER" || { echo "⛔ 없음: $DRIVER"; exit 1; }
# ⛔ 2026-08-11 사고 방지 — 러너만 최신이고 드라이버가 옛 판이면 MTO 없이 돌고,
#   프레임이 없으면 소급 복구가 안 된다 (arrhenius_6pt 21 런이 그렇게 날아갔다).
#   --supercell 도 같은 커밋에 들어 있으므로 이 검사가 그것까지 겸한다.
grep -q "msd_multi_origin" "$DRIVER" || { echo "⛔ 드라이버에 MTO 가 없다 — 옛 판이다: $DRIVER"; exit 1; }
grep -q '"--supercell"' "$DRIVER" || { echo "⛔ 드라이버에 --supercell 이 없다 — 옛 판이다: $DRIVER"; exit 1; }

# ── 중복 실행 가드 (flock 만 쓴다 — pgrep 은 tmux 래퍼까지 세서 자기 자신에 걸린다) ──
LOCK=${LOCK:-/tmp/comp1_supercell.lock}
exec 9>"$LOCK" || { echo "⛔ 락 파일을 못 연다"; exit 1; }
command -v flock >/dev/null 2>&1 && { flock -n 9 || { echo "⛔ 이미 돈다 — 중단"; exit 0; }; }

ts(){ echo "[$(date +%m-%d\ %H:%M:%S)] $*"; }
mkdir -p "$OUTROOT"

ts "comp1 셀 확대 사다리 — 사다리 [$LADDER] · T [$TEMPS] K · prod ${PRODPS} ps · seed $SEED"
ts "V0 $V0XYZ → $OUTROOT"

# ⚠ 싼 칸부터 · 시드 안쪽 루프 — 한 셀의 3시드가 먼저 모여야 그 칸을 판정할 수 있다
for SC in $LADDER; do
  NA=${SC%%x*}; REST=${SC#*x}; NB=${REST%%x*}; NC=${REST##*x}
  for SEED in $SEEDS; do
    d="$OUTROOT/sc${SC}_s${SEED}"
    # 드라이버는 resume-safe 라 msd.json 이 있으면 건너뛴다 — 칸·시드마다 폴더를 나눈다
    if [ -f "$d/ensemble_results.json" ] && grep -aq '"Ea_eV"\|"D_Li_cm2_s"' "$d/ensemble_results.json" 2>/dev/null; then
      ts "  ✓ $SC s$SEED 이미 있음 — 건너뜀"
      continue
    fi
    ts "═══ $SC  (${NA}×${NB}×${NC})  seed $SEED ═══"
    mkdir -p "$d"
    # ⚠ 타일링 뒤 속도는 드라이버가 **원자별로 새로 뽑는다**(MaxwellBoltzmannDistribution
    #   이 슈퍼셀에 적용됨) — 복제본이 한 덩어리로 움직이는 copy symmetry 는 없다. 확인함.
    $PY "$DRIVER" \
        --v0_xyz "$V0XYZ" --supercell "$NA" "$NB" "$NC" \
        --label "comp1_sc${SC}" --out_root "$d" \
        --disorder_levels 0.0 --n_configs 1 \
        --temperatures $TEMPS \
        --equilib_ps 5 --prod_ps "$PRODPS" --timestep_fs 2 --friction 0.02 \
        --save_fs 100 --save_traj \
        --fit_window_ps 2 50 \
        --seed "$SEED" --device "$DEVICE" \
      || { ts "  ⛔ $SC s$SEED 실패 — 여기서 멈춘다 (뒤가 더 비싸다)"; break 2; }
    ts "  ✅ $SC s$SEED 끝"
  done
done

ts "═══ 사다리 판정 ═══"
# ⚠ β 는 **저장된 D 스칼라가 아니라 시계열**에서 다시 잰다 — 창 규약(2–50 ps) 고정.
$PY "$REPO/tools/ionic/msd_diffusive_check.py" \
    --glob "$OUTROOT/*/**/msd.json" 2>/dev/null || \
  ts "  (msd_diffusive_check 인자가 다르면 아래로: msd_refit_window.py --glob '$OUTROOT/*/**/msd.json')"
echo
ts "판정 규칙 (2026-08-11 개정) — **단조성이 아니라 양 끝 비교 + 산포**로 읽는다:"
echo "   시드 SD ≈ 0.107 이므로 시드 하나짜리 차이는 아무 뜻이 없다. 칸별 3시드 평균을 본다."
echo
echo "   ① 큰 셀 중앙값 β → 1 에 접근 **AND** 시드 산포 감소"
echo "      → finite-sampling/finite-size 효과 지지. comp1 Ea 를 확대본으로 재산출."
echo "   ② 중앙값은 <0.8 에 머물고 **산포만** 감소"
echo "      → ⛔ 가설 기각이 아니다. **non-Fickian 동역학을 더 정밀하게 잰 것**이다."
echo "        MSD 경로를 접고 홉 통계·van Hove 로 기구를 분해한다:"
echo "          python3 tools/ionic/hops_per_ion.py --glob '$OUTROOT/*/**/traj.xyz'"
echo "   ③ 중앙값이 불확실도를 넘어 이동 → 진짜 유한크기/형상 물리 (또는 추정기 편향)"
echo "   ④ 중앙값도 산포도 불안정 → 집단 상관·비정상성·프로토콜 감사"
echo
echo "   ⚠ 이상적 독립 Li 라면 Li 24→192 에서 SD 가 1/√8 = 0.354배로 줄어야 한다."
echo "     덜 줄면 **유효 독립 Li 수가 명목보다 작다**는 뜻이다 — 그 자체가 결과다."
echo "   ⚠ 2x1x1→2x2x1→2x2x2 는 크기뿐 아니라 **형상비**도 바꾼다 — 크기 단독 실험이 아니다."
