#!/usr/bin/env bash
# wallP conditional 다압력 검증 — 실측 f_AM 을 MPM 에 걸어 DEM 두께와 대조한다.
#
# 지금까지 --am-load-frac 은 단일압력 corner 런 검증 대기 상태였고, 넣는 f_AM 은
# 스캐폴드 기하 + Hertz 로 **추정**한 값이었다.  real_14 압력스윕(100/300/600 MPa)이
# contact 덤프와 함께 들어와 f_AM 을 **실측**했으므로(추정기는 1.3배 과대 —
# docs/mpm_wallP_conditional_troubleshooting.md), 그 실측값으로 첫 다압력 검증을 한다.
#
# ★ 같은 베드를 쓴다: f_AM 은 압력스윕 베드에서 쟀으므로 스캐폴드도 그 베드의 것을 쓴다
#   (production kit_real14 는 300 MPa 서 두께 30.28 vs 이 베드 27.72 µm = 다른 실현).
#
# ★ --target-gpa 에는 **전체 압력**을 넣는다.  --am-load-frac 이 내부에서
#   SE_target = target·(1−f_AM) 을 이미 적용하므로, 미리 곱해 넘기면 **이중 적용**된다.
#
# ★ --floor-porosity 는 **ε_union** 을 쓴다.  MPM porosity 는 기하(복셀 점유)라
#   기하 규약인 ε_union 과 짝이 맞다.  ε_sphere 는 DEM 겹침-프록시의 물질보존 규약이고
#   P600 에선 −5.01 % (D_sphere 1.05 = 과압축)라 애초에 쓸 수 없다.
#   docstring 이 "flat --am-load-frac alone over-corrects dense beds" 라 게이트는 필수.
#
# ⚠ P600 은 두 가지를 안고 간다: (a) DEM 자체가 과압축 영역이라 floor 0.7 % 가
#   사실상 게이트를 꺼버린다 (b) AM 이 436 → 412 로 24개 손실(AM_S 400→376).
#   → P100/P300 이 깨끗한 판정선이고 P600 은 참고로 읽는다.
#
# 사용:
#   nohup bash scripts/run_wallp_multiP.sh > ~/wallp.log 2>&1 &
#   bash scripts/run_wallp_multiP.sh --dry          # 계획만
set -uo pipefail

REPO="${REPO:-/home/ubuntu/dem-stoic}"
DATA="${DATA:-/home/ubuntu/Yonghoon-DEM-DFT}"
OUT="$DATA/se_curve"
NGRID=384; SUB=160; MACH=0.03; GPUMEM=20; DRY=0

# P : f_AM(실측) : floor(ε_union %) : DEM 두께(µm, 대조용)
RUNS=("100:0.517:24.72:33.024" "300:0.675:11.39:27.724" "600:0.620:0.69:23.474")

while [ $# -gt 0 ]; do
  case "$1" in
    --n-grid)  NGRID="$2"; shift 2 ;;
    --gpu-mem) GPUMEM="$2"; shift 2 ;;
    --sub)     SUB="$2"; shift 2 ;;
    --repo)    REPO="$2"; shift 2 ;;
    --data)    DATA="$2"; OUT="$2/se_curve"; shift 2 ;;
    --dry)     DRY=1; shift ;;
    -h|--help) sed -n '2,30p' "$0"; exit 0 ;;
    *) echo "알 수 없는 인자: $1" >&2; exit 2 ;;
  esac
done

# ── 프리플라이트 ①: numpy+taichi 되는 venv ────────────────────────────────
ACT=""
for A in "$REPO/venv/bin/activate" "$DATA/venv/bin/activate" "$HOME/.venv/bin/activate"; do
  [ -f "$A" ] || continue
  ( . "$A" >/dev/null 2>&1; python3 -c "import numpy,taichi" ) 2>/dev/null && { ACT="$A"; break; }
done
[ -n "$ACT" ] || { echo "★★ ABORT: numpy+taichi 되는 venv 없음" >&2; exit 1; }
# shellcheck disable=SC1090
. "$ACT" >/dev/null 2>&1
mkdir -p "$OUT"
echo "venv: $ACT · python: $(command -v python3)"
echo "설정: n_grid $NGRID · sub $SUB · mach $MACH · gpu-mem $GPUMEM"

rc_all=0
for R in "${RUNS[@]}"; do
  IFS=':' read -r P FAM FLOOR HDEM <<< "$R"
  AM="$REPO/docs/data/heckel_sweep_scaffolds/P${P}_am_scaffold.csv"
  SE="$REPO/docs/data/heckel_sweep_scaffolds/P${P}_se_scaffold.csv"
  # ── 프리플라이트 ②: 스캐폴드가 없으면 0회 돌고 성공처럼 보이는 게 최악 → 중단 ──
  for F in "$AM" "$SE"; do
    [ -f "$F" ] || { echo "★★ ABORT: $F 없음 (git pull 했는지 확인)"; exit 3; }
  done
  TGPA=$(python3 -c "print($P/1000.0)")
  SETG=$(python3 -c "print(round($P/1000.0*(1-$FAM),4))")
  NAME="wallp_P${P}"
  echo "=== $NAME  target ${TGPA} GPa · f_AM ${FAM} → SE목표 ${SETG} GPa · floor ${FLOOR}% · DEM두께 ${HDEM}µm  $(date +%H:%M:%S)"
  [ "$DRY" = 1 ] && { echo "  (dry-run)"; continue; }
  t0=$SECONDS
  python3 -u "$REPO/scripts/mpm3d_compaction.py" --arch cuda --gpu-mem "$GPUMEM" --am-scaffold "$AM" --se-dump "$SE" --n-grid "$NGRID" --sub "$SUB" --print-every 20 --protocol hold --periodic --platen-mach "$MACH" --target-gpa "$TGPA" --am-load-frac "$FAM" --floor-porosity "$FLOOR" --save-metrics "$OUT/${NAME}.json" > "$OUT/${NAME}.log" 2>&1
  rc=$?; echo "  EXIT=$rc  wall=$((SECONDS-t0))s"
  if [ "$rc" -ne 0 ]; then
    rc_all=$rc; echo "  ── 실패 꼬리 ──"; tail -8 "$OUT/${NAME}.log" | sed 's/^/  | /'
  else
    python3 - "$OUT/${NAME}.json" "$HDEM" <<'PY' || true
import json, sys
d = json.load(open(sys.argv[1])); h_dem = float(sys.argv[2])
h = d.get('thickness_um'); por = d.get('porosity_pct', d.get('porosity'))
if h: print(f"  → MPM 두께 {h:.3f} µm  vs DEM {h_dem:.3f}  Δ {100*(h-h_dem)/h_dem:+.1f} %   porosity {por}")
PY
  fi
done
n=$(ls "$OUT"/wallp_P*.json 2>/dev/null | wc -l)
echo "BATCH DONE $(date +%H:%M:%S)  (json $n/3, rc=$rc_all)"
exit $rc_all
