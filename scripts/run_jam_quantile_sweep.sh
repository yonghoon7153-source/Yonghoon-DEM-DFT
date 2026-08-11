#!/usr/bin/env bash
# --am-jam quantile 재시험 러너 — **사전등록판** (2026-08-11, Codex Q1 수용 후).
#
# 묻는 것 하나: "퍼콜 AM 상위 q% 가 만드는 지지평면이 실제 플래튼 정지 높이인가."
# 판정은 scripts/summarize_jam_sweep.py 가 한다 (여기서는 돌리기만 한다).
#
# ★★ 사전등록 (돌리기 전에 고정, Codex 6회차 리뷰 반영) ★★
#   ① 압력 제외는 **q 와 무관한 사전 정보**로만: P600 은 DEM ε_union 0.69 % 축퇴라
#      **사전 제외**.  판정 압력은 P100/P200/P300.
#   ② q ∈ {90, 95, 100} × P 3개 = **9 런 전부** 요구.  하나라도 없으면 스윕 incomplete.
#   ③ jam 미발화(`stop_mode != am_jam`)·축퇴(porosity < 2 %)는 **제외가 아니라 FAIL**.
#      — 그것은 "그 q 가 그 압력에서 정지 기준으로 작동하지 않았다" 는 **결과**다.
#      옛 시험이 P100-q90 을 사후 제외한 것이 post-treatment selection 이었다.
#   ④ 지표는 **두께 고정**.  porosity 는 관찰만 (결과를 보고 지표를 바꾸지 않는다).
#   ⑤ 통과해도 주장은 "압력-독립" 까지 — 세 q 를 같은 3 압력에서 고른 것이므로
#      후보군 내 screening 이다.  일반화에는 holdout 이 하나 더 필요하다.
#
# ⚠ 두께는 **예측 대상이 아니다** (얼린-AM 스캐폴드).  jam 기준의 검증 지표일 뿐이다.
#
# 사용:
#   bash scripts/run_jam_quantile_sweep.sh                    # 9 런
#   bash scripts/run_jam_quantile_sweep.sh --dry              # 계획만
#   bash scripts/run_jam_quantile_sweep.sh --p 100,200 --q 95 # 부분 (판정은 incomplete)
set -uo pipefail
REPO="${REPO:-/home/ubuntu/dem-stoic}"
DATA="${DATA:-/home/ubuntu/Yonghoon-DEM-DFT}"
OUT="$DATA/se_curve"
PS="100,200,300"; QS="90,95,100"; NGRID=192; SUB=160; MACH=0.03; GPUMEM=8; DRY=0
while [ $# -gt 0 ]; do
  case "$1" in
    --p)       PS="$2"; shift 2 ;;
    --q)       QS="$2"; shift 2 ;;
    --n-grid)  NGRID="$2"; shift 2 ;;
    --sub)     SUB="$2"; shift 2 ;;
    --mach)    MACH="$2"; shift 2 ;;
    --gpu-mem) GPUMEM="$2"; shift 2 ;;
    --repo)    REPO="$2"; shift 2 ;;
    --data)    DATA="$2"; OUT="$2/se_curve"; shift 2 ;;
    --dry)     DRY=1; shift ;;
    -h|--help) sed -n '2,28p' "$0"; exit 0 ;;
    *) echo "알 수 없는 인자: $1" >&2; exit 2 ;;
  esac
done

# ── 프리플라이트 ①: numpy+scipy+taichi 되는 venv (scipy 는 --se-dump 필수) ──
#   ★ --dry 는 **계획만** 보는 것이 목적이라 런타임을 요구하지 않는다.  요구하면
#     GPU 머신 밖에서 사전등록 계획을 검토할 수 없어 --dry 자체가 무용해진다.
ACT=""
if [ "$DRY" = 1 ]; then
  echo "(dry-run: venv 프리플라이트 생략 — 계획만 출력한다)"
else
for A in "$REPO/scripts/activate_dem.sh" "$REPO/venv/bin/activate" \
         "$DATA/venv/bin/activate" "$HOME/.venv/bin/activate"; do
  [ -f "$A" ] || continue
  ( . "$A" >/dev/null 2>&1; python3 -c "import numpy,scipy,taichi" ) 2>/dev/null && { ACT="$A"; break; }
done
  [ -n "$ACT" ] || { echo "★★ ABORT: numpy+scipy+taichi 되는 venv 없음.
  설치는 **venv 파이썬으로**: $DATA/venv/bin/python3 -m pip install scipy" >&2; exit 1; }
  # shellcheck disable=SC1090
  . "$ACT" >/dev/null 2>&1
  mkdir -p "$OUT"
  echo "venv: $ACT · python: $(command -v python3)"
fi
echo "설정: n_grid $NGRID · sub $SUB · mach $MACH · gpu-mem $GPUMEM"
echo "사전등록: P{$PS} × q{$QS} 전부 · P600 사전제외(ε_union 0.69 % 축퇴)"
echo "         jam 미발화/축퇴 = FAIL(제외 아님) · 지표는 두께 고정"

IFS=',' read -r -a P_ARR <<< "$PS"
IFS=',' read -r -a Q_ARR <<< "$QS"
rc_all=0; n_done=0; n_tot=$(( ${#P_ARR[@]} * ${#Q_ARR[@]} ))
for P in "${P_ARR[@]}"; do
  AM="$REPO/docs/data/heckel_sweep_scaffolds/P${P}_am_scaffold.csv"
  SE="$REPO/docs/data/heckel_sweep_scaffolds/P${P}_se_scaffold.csv"
  # ── 프리플라이트 ②: 스캐폴드가 없으면 0회 돌고 성공처럼 보이는 게 최악 → 중단 ──
  for F in "$AM" "$SE"; do
    if [ ! -f "$F" ]; then
      [ "$DRY" = 1 ] && { echo "  ⚠ (dry) 스캐폴드 없음: $F"; continue; }
      echo "★★ ABORT: $F 없음 (git pull 했는지 확인)"; exit 3
    fi
  done
  TGPA=$(python3 -c "print($P/1000.0)")
  for Q in "${Q_ARR[@]}"; do
    NAME="jam_P${P}_q${Q}"
    # 낡은 산출물 먼저 제거 — 안 지우면 시작조차 못 했을 때 watch 가 이전 런을
    # 현재 상태로 보여준다 (2026-08-07 실제 발생).
    rm -f "$OUT/${NAME}.json" "$OUT/${NAME}.log"
    echo "=== $NAME  target ${TGPA} GPa · q=${Q}  $(date +%H:%M:%S)"
    [ "$DRY" = 1 ] && { echo "  (dry-run)"; continue; }
    t0=$SECONDS
    python3 -u "$REPO/scripts/mpm3d_compaction.py" --arch cuda --gpu-mem "$GPUMEM" \
      --am-scaffold "$AM" --se-dump "$SE" --n-grid "$NGRID" --sub "$SUB" \
      --print-every 20 --protocol hold --periodic --platen-mach "$MACH" \
      --target-gpa "$TGPA" --am-jam --am-jam-quantile "$Q" \
      --save-metrics "$OUT/${NAME}.json" > "$OUT/${NAME}.log" 2>&1
    rc=$?; echo "  EXIT=$rc  wall=$((SECONDS-t0))s"
    if [ "$rc" -ne 0 ]; then
      rc_all=$rc; echo "  ── 실패 꼬리 ──"; tail -8 "$OUT/${NAME}.log" | sed 's/^/  | /'
    else
      n_done=$((n_done+1))
      python3 - "$OUT/${NAME}.json" <<'PY' || true
import json, sys
d = json.load(open(sys.argv[1]))
print(f"  두께 {d.get('thickness_um')} µm · porosity {d.get('porosity_settled_pct')} %"
      f" · stop_mode {d.get('stop_mode')}")
PY
    fi
  done
done

echo
echo "SWEEP DONE $(date +%H:%M:%S)  ($n_done/$n_tot 성공)"
echo "판정:  python3 $REPO/scripts/summarize_jam_sweep.py --dir $OUT"
echo "  ⚠ 9 런이 다 있어야 판정한다 — 부분 결과로 q 를 고르면 그것이 selection bias 다."
exit $rc_all
