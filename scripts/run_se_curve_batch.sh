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
  # ★ scipy 도 본다.  빼면 mpm3d 가 --se-dump 의 cKDTree 에서 **16초 만에** 죽고,
  #   러너는 그것을 점마다 반복한다 (실제로 3점 × 16s 를 두 번 태웠다).
  #   ⚠ `pip install` 을 venv 밖에서 하면 ~/.local 에 깔리는데 venv 는 user-site 를
  #     경로에 넣지 않는다 → 시스템 python 에선 import 되고 여기선 안 되는 상태가 된다.
  #     그래서 검사는 반드시 **활성화한 그 python** 으로 한다 (아래가 그렇다).
  ( . "$A" >/dev/null 2>&1; python3 -c "import numpy,scipy,taichi" ) 2>/dev/null && { ACT="$A"; break; }
done
[ -n "$ACT" ] || { echo "★★ ABORT: numpy+scipy+taichi 되는 venv 없음 (scipy 는 --se-dump 필수).
  설치는 **venv 파이썬으로**: ~/Yonghoon-DEM-DFT/venv/bin/python3 -m pip install scipy (심링크: ln -sfn $DATA/venv $REPO/venv)" >&2; exit 1; }
# shellcheck disable=SC1090
. "$ACT" >/dev/null 2>&1
# ── 준정적 게이트 (2026-08-11) ─────────────────────────────────────────────────
#   mpm3d 는 이제 V/c_P > 0.01 이면 **거부**한다 (옛 코드는 print 경고만 했다).
#   이 러너는 **상대 비교**가 목적이라 (같은 마하로 통일 → 공통모드 상쇄 = 등급 B)
#   승인 플래그를 붙이되, 그 사실을 화면에 크게 알리고 결과 JSON 에도 기록되게 한다.
#   ⚠ 절대값이 필요하면 --mach 0.01 로 다시 재야 한다 (실측 0.0306→0.01 에서 σ +4.8 %).
QSFLAG=()
if python3 -c "import sys; sys.exit(0 if float('$MACH') > 0.01 else 1)" 2>/dev/null; then
  QSFLAG=(--allow-fast-platen)
  echo "★ 준정적 한계 초과 (mach $MACH > 0.01) — --allow-fast-platen 으로 승인하고 진행한다."
  echo "  이 배치의 결과는 **상대 비교 전용**이다 (결과 JSON 의 quasistatic_violation=true)."
  echo "  절대값이 필요하면: --mach 0.01 (런타임 ~3x)"
fi
mkdir -p "$OUT"; cd "$OUT" || exit 1
echo "venv: $ACT  ·  python: $(command -v python3)"
echo "설정: n_grid $NGRID · sub $SUB · mach $MACH · gpu-mem $GPUMEM · φ $PHI"

# ── 실행 이력 (2026-08-11 사고 후 추가) ───────────────────────────────────────
#   ★ 이 배치는 **시작 시점에 한 번** QSFLAG 를 계산하는데, mpm3d 는 **매 런마다 새로
#     읽힌다**.  그래서 배치 중간에 `git pull` 하면 둘이 어긋난다.
#     실측 사고(2026-08-11, kit_ps_7_3 g288): 13:19 에 게이트 없던 코드로 시작 →
#     1·2번(ε 14.97·11.73) 통과 → 중간에 pull → mpm3d 가 준정적 게이트를 얻음 →
#     3번(ε 7.42)만 144초 만에 거부(EXIT=1).  화면 어디에도 "코드가 바뀌었다" 는
#     신호가 없어 원인 파악에 왕복이 필요했다.  ⇒ **첫 줄에 박고, 바뀌면 그때도 알린다.**
_MPM="$REPO/scripts/mpm3d_compaction.py"
_sha()  { git -C "$REPO" rev-parse --short HEAD 2>/dev/null || echo "no-git"; }
_mpmh() { md5sum "$_MPM" 2>/dev/null | cut -c1-8 || echo "????????"; }
HEAD0=$(_sha); MPM0=$(_mpmh)
_gate=$(grep -c 'allow_fast_platen' "$_MPM" 2>/dev/null || true); _gate=${_gate:-0}
echo "── 실행 이력 ────────────────────────────────────────────────"
echo "   repo HEAD : $HEAD0"
echo "   mpm3d     : md5 $MPM0  ·  준정적 게이트 $([ "$_gate" -gt 0 ] && echo 있음 || echo 없음)"
echo "   QSFLAG    : ${QSFLAG[*]:-(없음)}   ← ★ 배치 시작 시점에 고정 (중간 pull 시 어긋남)"
if [ "$_gate" -gt 0 ] && [ ${#QSFLAG[@]} -eq 0 ]; then
  echo "   ★★ 경고: mpm3d 에 게이트가 있는데 QSFLAG 가 비어 있다."
  echo "      mach $MACH 가 준정적 한계(0.01)를 넘으면 **모든 런이 거부**된다."
fi
echo "─────────────────────────────────────────────────────────────"

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
    python3 -u "$REPO/scripts/mpm3d_compaction.py" --arch cuda --gpu-mem "$GPUMEM" --am-scaffold "$KDIR/am_scaffold.csv" --se-dump "$KDIR/se_scaffold.csv" --n-grid "$NGRID" --sub "$SUB" --print-every 20 --protocol hold --periodic --platen-mach "$MACH" "${QSFLAG[@]}" --compact-to "$E" --save-metrics "xfer_${NAME}.json" > "xfer_${NAME}.log" 2>&1
    rc=$?; echo "  EXIT=$rc  wall=$((SECONDS-t0))s"
    # 배치 도중 코드가 바뀌었으면 **그 자리에서** 알린다 (위 사고의 조기 신호).
    _now=$(_mpmh)
    if [ "$_now" != "$MPM0" ]; then
      echo "  ★★ mpm3d 가 배치 도중 바뀌었다: md5 $MPM0 → $_now  (HEAD $HEAD0 → $(_sha))"
      echo "     QSFLAG 는 시작 시점 값(${QSFLAG[*]:-없음})으로 **고정**돼 있어 새 코드와"
      echo "     어긋날 수 있다.  실패가 나면 배치를 다시 띄우세요 (2026-08-11 사고)."
      MPM0="$_now"; HEAD0=$(_sha)
    fi
    if [ "$rc" -ne 0 ]; then
      rc_all=$rc; echo "  ── 실패 꼬리 ──"; tail -5 "xfer_${NAME}.log" | sed 's/^/  | /'
    fi
  done
done
n=$(ls xfer_*_g${NGRID}_e*.json 2>/dev/null | wc -l)
echo "BATCH DONE $(date +%H:%M:%S)  (이 n_grid 의 json 총 $n 개, rc=$rc_all)"
exit $rc_all
