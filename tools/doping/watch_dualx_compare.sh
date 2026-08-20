#!/usr/bin/env bash
# dual-x 농도 비교 watch: x=0.0625 (lowx) vs x=0.25 (highx).
# 도펀트별로 양쪽 stage 진행 + blocking_fraction(있으면)을 나란히 표시.
# 사용: bash tools/doping/watch_dualx_compare.sh   (watch -n 60 으로 반복 가능)
set +H
DX=/data/work/runs/dualx_v23
DOPANTS=(Sc2O3 Gd2O3 Cr2O3 Y2O3 La2O3 HfO2 Ta2O5 Nb2O5 V2O5 TiF4)

stat_of(){  # $1=dir -> DONE / 최종stage짧게 / -
  if [ -f "$1/STAGE_04.DONE" ]; then echo "DONE"
  elif [ -d "$1" ]; then ls -d "$1"/[0-9]*_* 2>/dev/null | sed 's#.*/##' | tail -1 | cut -c1-9
  else echo "-"; fi; }
block_of(){  # $1=dir -> blocking_fraction 값(첫 매치) 또는 빈값
  grep -rhoE '"[a-z_]*blocking_fraction"[ :]+[-0-9.]+' "$1" 2>/dev/null \
    | grep -oE '[-0-9.]+' | head -1; }

echo "════════ $(date '+%m-%d %H:%M')  dual-x 농도 비교 (low x=0.0625  vs  high x=0.25) ════════"
printf "  %-7s | %-20s | %-20s\n" "도펀트" "x=0.0625 (low)" "x=0.25 (high)"
echo "  --------+----------------------+----------------------"
ld=0; hd=0
for c in "${DOPANTS[@]}"; do
  ls_=$(stat_of "$DX/${c}_lowx");  lb=$(block_of "$DX/${c}_lowx")
  hs=$(stat_of "$DX/${c}_highx"); hb=$(block_of "$DX/${c}_highx")
  [ "$ls_" = DONE ] && ld=$((ld+1)); [ "$hs" = DONE ] && hd=$((hd+1))
  printf "  %-7s | %-9s blk %-6s | %-9s blk %-6s\n" "$c" "$ls_" "${lb:-—}" "$hs" "${hb:-—}"
done
echo "  --------+----------------------+----------------------"
printf "  %-7s | low %2d/10 완료        | high %2d/10 완료\n" "합계" "$ld" "$hd"

# highx driver/진행 상태
p=$(pgrep -f run_dualx_highx.sh | head -1)
if [ -n "$p" ]; then echo "  highx driver ✅ 실행중 PID=$p ($(ps -o etime= -p "$p" 2>/dev/null|tr -d ' '))"
else echo "  highx driver ⛔ 없음 (멈춤/완료 — 재개: setsid bash tools/doping/run_dualx_highx.sh ...)"; fi
R=$(find "$DX" -path "*_highx*" -name "*.log" -newermt "-5 min" 2>/dev/null | head -1)
[ -n "$R" ] && echo "  🟢 highx 진행중 (5분내 갱신)" || echo "  🔴 highx 5분내 갱신 없음"
nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv,noheader 2>/dev/null | sed 's/^/  GPU(공유): /'
echo "  ※ blk=— 이면 그 stage에 blocking_fraction이 아직/별도 저장 — 둘 다 끝나면 분석으로 최종 비교"
