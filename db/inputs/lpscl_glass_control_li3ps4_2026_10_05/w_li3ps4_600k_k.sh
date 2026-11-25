#!/bin/bash
# li2s 대조 B 600 K · kgy 몫 (seed1·3) 감시 — 읽기만 · 결과값 (D · β · MSD) 은 안 찍는다
#   쓰는 법: bash <이 파일>            (한 번 찍고 끝)
#            bash <이 파일> --loop 300  (300 s 마다 화면을 지우고 다시 찍는다 · Ctrl-C 로 끝)
#   다른 온도·루트 (2026-10-14 B 측정 가능 조건 카드): TT=650 TS=li3ps4_650k R=~/work/runs/lpscl_glass_bmeas_650K_2026_10_14 bash <이 파일> --loop 300
show(){
  R=${R:-$HOME/work/runs/lpscl_glass_control_li3ps4_600K_2026_10_13}; Q=$R/queue_kgy.log
  TT=${TT:-600}; TS=${TS:-li3ps4_600k}
  echo "== $(date '+%F %T') · kgy · li2s B ${TT} K (seed1·3 · 405 ps 씩 · cascade 와 GPU 공유) =="
  tmux has-session -t "$TS" 2>/dev/null && echo "tmux $TS 살아 있음" || echo "tmux $TS 없음"
  tmux capture-pane -pt "$TS" 2>/dev/null | grep -aE '문지기|판 — ' | tail -n 2 | cut -c1-320
  if [ ! -f "$Q" ]; then echo "큐 로그 없음 ($Q)"; else
    echo "끝난 런 $(grep -ac "✅ T${TT} seed" "$Q") / 2"
    for S in $(grep -a "✅ T${TT} seed" "$Q" | sed -E "s/.*✅ T${TT} seed([0-9]+) .*/\1/"); do
      a=$(grep -a "▶ T${TT} seed$S " "$Q" | tail -n 1 | sed -E 's/^\[([^]]+)\].*/\1/'); b=$(grep -a "✅ T${TT} seed$S " "$Q" | tail -n 1 | sed -E 's/^\[([^]]+)\].*/\1/')
      echo "  seed$S $(grep -a "✅ T${TT} seed$S " "$Q" | tail -n 1 | sed -E 's/.*끝 (\(rc [0-9]+\)).*/\1/') · 벽시계 $(awk -v x=$(( $(date -d "$b" +%s) - $(date -d "$a" +%s) )) 'BEGIN{printf "%.1f h", x/3600}')"
    done
    grep -aE '⛔|■ 큐 끝' "$Q" | tail -n 2
    L=$(grep -a "▶ T${TT} seed" "$Q" | tail -n 1)
    if [ -z "$L" ]; then echo "아직 런 시작 전"; else
      S=$(echo "$L" | sed -E "s/.*▶ T${TT} seed([0-9]+) .*/\1/"); P=$(echo "$L" | sed -E 's/.* PID ([0-9]+) .*/\1/')
      T0=$(echo "$L" | sed -E 's/^\[([^]]+)\].*/\1/'); MD=$R/seed$S/T$TT/d0.00_cfg0/T$TT/md.log
      t=$(tail -n 1 "$MD" 2>/dev/null | awk '$1+0==$1 {print $1+0}'); el=$(( $(date +%s) - $(date -d "$T0" +%s) ))
      if grep -aq "✅ T${TT} seed$S " "$Q"; then st="끝남"; elif kill -0 "$P" 2>/dev/null; then st="돌고 있음 PID $P"; else st="PID $P 없음 — 큐 로그 끝을 본다"; fi
      echo "지금 seed$S · $st · 시작 $T0 · md.log ${t:-0} / 405 ps · 경과 $(awk -v e=$el 'BEGIN{printf "%.2f h", e/3600}')$(awk -v t=${t:-0} -v e=$el 'BEGIN{ if (t > 5) printf " · 남은 어림 %.1f h", (405-t)*e/t/3600 }')"
      grep -aE "run_meta = |dt = " "$Q" | tail -n 2 | cut -c1-160
    fi
  fi
  echo "GPU $(nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu --format=csv,noheader 2>/dev/null) (프로세스별은 kgy 에서 막혀 있다)"
  tmux has-session -t cv7main 2>/dev/null && echo "곁의 cascade v7 (tmux cv7main) 살아 있음 — 진행·비용은 cv7_watch 로" || echo "cascade tmux cv7main 없음"
}
if [ "${1:-}" = "--loop" ]; then
  while :; do clear; show; echo "(${2:-300} s 마다 갱신 · Ctrl-C 로 끝)"; sleep "${2:-300}"; done
else show; fi
