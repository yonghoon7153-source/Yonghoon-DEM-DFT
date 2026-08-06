#!/usr/bin/env bash
# SE 응답곡선 배치 러너 — 여러 킷을 같은 φ 격자·같은 재하율로 돌린다.
#
# ★ 왜 스크립트인가: 긴 명령을 터미널에 붙여넣으면 `\` 줄바꿈이 깨져
#   "--compact-to: command not found" (EXIT=127) 로 조용히 실패하는 일이 반복됐다
#   (2026-08-06 세 번).  러너를 리포에 두면 붙여넣기가 관여하지 않는다.
#
# ★ 재하율은 --mach 로 **반드시 고정**한다.  mpm3d 의 기본 기하 규칙
#   vmax = 0.008·(WALL0−FLOOR) 은 플래튼 속도를 베드 높이에 비례시켜, 두께가 다른
#   베드끼리는 재하율이 달라지고 σ(φ) 비교가 통째로 교란된다
#   (실측 real_14 V/c_P 0.031 vs kit_ps_7_3 0.105 = 3.4배 — docs/se_curve_transfer_verdict_20260806.md).
#
# 사용:
#   bash scripts/run_se_curve_batch.sh --kits kit_ps_0_10,kit_ps_3_7 --phi 0.66,0.72,0.81
#   bash scripts/run_se_curve_batch.sh --kits kit_real14 --phi 0.60,0.70 --n-grid 384 --tag ref
#   bash scripts/run_se_curve_batch.sh --dry           # 실행 없이 계획만
set -uo pipefail

REPO="${REPO:-/home/ubuntu/dem-stoic}"          # 코드 (worktree)
DATA="${DATA:-/home/ubuntu/Yonghoon-DEM-DFT}"   # 킷 데이터 + 산출 디렉토리
OUT="$DATA/se_curve"
KITS=""; PHI="0.66,0.72,0.81"; NGRID=192; SUB=160; MACH=0.03; GPUMEM=8; TAG=""; DRY=0

while [ $# -gt 0 ]; do
  case "$1" in
    --kits)    KITS="$2"; shift 2 ;;
    --phi)     PHI="$2"; shift 2 ;;
    --n-grid)  NGRID="$2"; shift 2 ;;
    --sub)     SUB="$2"; shift 2 ;;
    --mach)    MACH="$2"; shift 2 ;;
    --gpu-mem) GPUMEM="$2"; shift 2 ;;
    --tag)     TAG="$2"; shift 2 ;;
    --repo)    REPO="$2"; shift 2 ;;
    --data)    DATA="$2"; OUT="$2/se_curve"; shift 2 ;;
    --dry)     DRY=1; shift ;;
    -h|--help) sed -n '2,22p' "$0"; exit 0 ;;
    *) echo "알 수 없는 인자: $1" >&2; exit 2 ;;
  esac
done
[ -n "$KITS" ] || { echo "--kits 필요 (쉼표 구분).  --help 참조" >&2; exit 2; }

# ── 프리플라이트 ①: numpy+taichi 되는 venv (worktree 는 venv 심링크가 필요하다) ──
ACT=""
for A in "$REPO/scripts/activate_dem.sh" "$DATA/scripts/activate_dem.sh" \
         "$DATA/venv/bin/activate" "$HOME/.venv/bin/activate"; do
  [ -f "$A" ] || continue
  ( . "$A" >/dev/null 2>&1; python3 -c "import numpy,taichi" ) 2>/dev/null && { ACT="$A"; break; }
done
[ -n "$ACT" ] || { echo "★★ ABORT: numpy+taichi 되는 venv 없음 (심링크: ln -sfn $DATA/venv $REPO/venv)" >&2; exit 1; }
# shellcheck disable=SC1090
. "$ACT" >/dev/null 2>&1
mkdir -p "$OUT"; cd "$OUT" || exit 1
echo "venv: $ACT  ·  python: $(command -v python3)"
echo "설정: n_grid $NGRID · sub $SUB · mach $MACH · gpu-mem $GPUMEM · φ $PHI"

rc_all=0
IFS=',' read -r -a KIT_ARR <<< "$KITS"
for K in "${KIT_ARR[@]}"; do
  KDIR="$DATA/$K"; [ -d "$KDIR" ] || KDIR="$OUT/$K"      # 킷은 데이터루트 또는 se_curve 밑
  if [ ! -f "$KDIR/am_scaffold.csv" ] || [ ! -f "$KDIR/se_scaffold.csv" ]; then
    echo "SKIP $K — am/se_scaffold.csv 없음 ($KDIR)"; continue
  fi
  EPS=$(python3 "$REPO/scripts/plan_se_curve_targets.py" --kit "$KDIR" --phi "$PHI" --eps-only)
  # ── 프리플라이트 ②: 빈 EPS 로 0회 돌고 "DONE" 찍는 게 최악 (성공처럼 보인다) → 중단 ──
  [ -n "$EPS" ] || { echo "★★ ABORT: $K 의 ε 목표가 비었음 (planner 실패)"; exit 3; }
  echo "### $K  ε: $EPS  ($(echo "$EPS" | wc -w) 점)  $(date +%H:%M:%S)"
  for E in $EPS; do
    T=$(echo "$E" | tr -d .)
    NAME="${TAG:+${TAG}_}${K}_g${NGRID}_e${T}"
    echo "=== $NAME  $(date +%H:%M:%S)"
    if [ "$DRY" = 1 ]; then echo "  (dry-run)"; continue; fi
    t0=$SECONDS
    python3 -u "$REPO/scripts/mpm3d_compaction.py" --arch cuda --gpu-mem "$GPUMEM" --am-scaffold "$KDIR/am_scaffold.csv" --se-dump "$KDIR/se_scaffold.csv" --n-grid "$NGRID" --sub "$SUB" --print-every 20 --protocol hold --periodic --platen-mach "$MACH" --compact-to "$E" --save-metrics "xfer_${NAME}.json" > "xfer_${NAME}.log" 2>&1
    rc=$?; echo "  EXIT=$rc  wall=$((SECONDS-t0))s"
    if [ "$rc" -ne 0 ]; then
      rc_all=$rc; echo "  ── 실패 꼬리 ──"; tail -5 "xfer_${NAME}.log" | sed 's/^/  | /'
    fi
  done
done
n=$(ls xfer_*_g${NGRID}_e*.json 2>/dev/null | wc -l)
echo "BATCH DONE $(date +%H:%M:%S)  (이 n_grid 의 json 총 $n 개, rc=$rc_all)"
exit $rc_all
