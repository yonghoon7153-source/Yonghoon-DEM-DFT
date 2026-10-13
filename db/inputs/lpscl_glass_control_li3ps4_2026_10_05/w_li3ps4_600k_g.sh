#!/bin/bash
# li2s 대조 B 600 K · gabia 몫 (seed2·4·5) 감시 — 읽기만 · 결과값 (D · β · MSD) 은 안 찍는다
R=${R:-/data/work/runs/lpscl_glass_control_li3ps4_600K_2026_10_13}; Q=$R/queue_gabia.log
R2=${R2:-/data/work/runs/sei_control/li3nd_mp-976264_p333_r2}
echo "== $(date '+%F %T') · gabia · li2s B 600 K (seed2·4·5 · 405 ps 씩) =="
tmux has-session -t li3ps4_600k 2>/dev/null && echo "tmux li3ps4_600k 살아 있음" || echo "tmux li3ps4_600k 없음"
if [ ! -f "$Q" ]; then echo "큐 로그 없음 ($Q)"; else
  echo "끝난 런 $(grep -ac '✅ T600 seed' "$Q") / 3 — $(grep -a '✅ T600 seed' "$Q" | sed -E 's/.*✅ T600 (seed[0-9]+) 끝 · ([0-9]+) s.*/\1 \2 s/' | awk '{printf "%s %.1f h  ", $1, $2/3600}')"
  grep -a '판 — ' "$Q" | tail -n 1 | cut -c1-200
  grep -aE '⛔|■ 큐 끝' "$Q" | tail -n 2
  L=$(grep -a '▶ T600 seed' "$Q" | tail -n 1)
  if [ -z "$L" ]; then echo "아직 런 시작 전"; else
    S=$(echo "$L" | sed -E 's/.*▶ T600 seed([0-9]+) .*/\1/'); P=$(echo "$L" | sed -E 's/.* PID ([0-9]+) .*/\1/')
    T0=$(echo "$L" | sed -E 's/^\[([^]]+)\].*/\1/'); MD=$R/seed$S/T600/d0.00_cfg0/T600/md.log
    t=$(tail -n 1 "$MD" 2>/dev/null | awk '$1+0==$1 {print $1+0}'); el=$(( $(date +%s) - $(date -d "$T0" +%s) ))
    if grep -aq "✅ T600 seed$S 끝" "$Q"; then st="끝남"; elif kill -0 "$P" 2>/dev/null; then st="돌고 있음 PID $P"; else st="PID $P 없음 — 큐 로그 끝을 본다"; fi
    echo "지금 seed$S · $st · 시작 $T0 · md.log ${t:-0} / 405 ps · 경과 $(awk -v e=$el 'BEGIN{printf "%.2f h", e/3600}')$(awk -v t=${t:-0} -v e=$el 'BEGIN{ if (t > 5) printf " · 남은 어림 %.1f h", (405-t)*e/t/3600 }')"
    grep -aE "run_meta = |dt = " "$Q" | tail -n 2 | cut -c1-160
  fi
  [ -f "$R/queue_coexist.tsv" ] && awk -F'\t' 'NR>1 {printf "  표 T%s seed%s rc %s done %s · %.1f h · 피크 합계 %s · 우리 %s MiB · 가드 %s\n", $1, $2, $3, $4, $5/3600, $6, $7, ($8==""?"없음":$8)}' "$R/queue_coexist.tsv"
  PM=$(ls -t "$R"/queue_logs/*_pmon.tsv 2>/dev/null | head -1)
  [ -n "$PM" ] && awk -F'\t' 'NR>1 && $2 != "NA" {n++; s += ($3 > 0 ? $2/$3 : 1); last=$0} END { if (n) printf "점유 표본 %d 개 · 우리/합 평균 %.3f · 마지막 [%s]\n", n, s/n, last }' "$PM"
fi
echo "GPU $(nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu --format=csv,noheader 2>/dev/null) · host MemAvailable $(awk '/MemAvailable/{printf "%d MiB", $2/1024}' /proc/meminfo)"
nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader 2>/dev/null | sed 's/^/  /'
O=$(ls -t "$R2"/*.out 2>/dev/null | head -1)
[ -n "$O" ] && echo "곁의 Li₃Nd r2 · $(basename "$O") · bfgs 스텝 $(grep -a 'number of bfgs steps' "$O" | tail -n 1 | awk -F'=' '{gsub(/ /,"",$2); print $2}') · Total force $(grep -a 'Total force' "$O" | tail -n 1 | awk '{print $4}') · 갱신 $(date -r "$O" '+%m-%d %H:%M')"
