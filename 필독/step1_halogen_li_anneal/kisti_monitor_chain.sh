#!/bin/bash
# kisti_monitor_chain.sh — detailed status for stage-split chain.sh runs.
# Shows: each comp's stage completion checklist + current stage progress +
# crash count + ETA + GPU. Watchdog re-runs chain.sh; cache resume skips done.
#
# Usage: watch -c -n 30 ./kisti_monitor_chain.sh    (live, 30s refresh)
#        while true; do clear; ./kisti_monitor_chain.sh; sleep 30; done

BASE=/scratch/x3430a02/kgy/manuscript_support/pipeline_v2
COMP3_DIR=$BASE/comp3_lpscbr/1_step1to3
COMP5_DIR=$BASE/comp5_lpscbr/1_step1to3

B="\033[1m"; G="\033[1;32m"; Y="\033[1;33m"; R="\033[1;31m"; C="\033[1;36m"; D="\033[2m"; N="\033[0m"

echo -e "${B}════════════════════════════════════════════════════════════════════════"
echo -e "  comp3 / comp5 v2 chain.sh — stage progress monitor"
echo -e "  $(date '+%Y-%m-%d %H:%M:%S')"
echo -e "════════════════════════════════════════════════════════════════════════${N}"

echo -e "\n${C}── GPU ──${N}"
nvidia-smi --query-gpu=index,name,temperature.gpu,utilization.gpu,memory.used,memory.total \
           --format=csv,noheader,nounits 2>/dev/null | \
  awk -F', ' '{ printf "  GPU%s %s  T=%s°C  Util=%3s%%  Mem=%5s/%5s MB\n", $1,$2,$3,$4,$5,$6 }'

echo -e "\n${C}── Processes ──${N}"
PS_OUT=$(ps -ef | grep -E "watchdog_comp[35]|chain.sh|comp[35]_v2_stage|anneal_rank" | grep -v grep)
if [ -z "$PS_OUT" ]; then
  echo -e "  ${R}NO chain/stage process running${N}"
else
  echo "$PS_OUT" | awk '{
    cmd=""; for(i=8;i<=NF;i++) cmd=cmd" "$i;
    if (length(cmd) > 80) cmd = substr(cmd, 1, 77) "...";
    printf "  PID %7s start=%-5s CPU=%-9s %s\n", $2,$5,$7,cmd
  }'
fi


# Stage names + expected cache filenames + approx duration
# (comp3 and comp5 same pattern)
STAGES=(
  "stage1a       cache_stage1a.json         5min"
  "stage1b_c0    cache_stage1b_c0.json     25min"
  "stage1b_c1    cache_stage1b_c1.json     25min"
  "stage1b_c2    cache_stage1b_c2.json     20min"
  "stage1b_merge cache_stage1b.json         <1s"
  "stage2        cache_stage2.json          5min"
  "rank0_anneal  comp_v2_rank0_results.json 50min"
  "rank1_anneal  comp_v2_rank1_results.json 50min"
  "rank2_anneal  comp_v2_rank2_results.json 50min"
  "rank3_anneal  comp_v2_rank3_results.json 50min"
  "rank4_anneal  comp_v2_rank4_results.json 50min"
)

for label in comp3 comp5; do
  if [ "$label" = "comp3" ]; then DIR=$COMP3_DIR; GPU=0; else DIR=$COMP5_DIR; GPU=1; fi
  echo -e "\n${B}══ $label (GPU$GPU) ══${N}"
  echo -e "${D}  $DIR${N}"

  if [ ! -d "$DIR" ]; then
    echo -e "  ${R}directory not found${N}"; continue
  fi

  # Champion = all done?
  CHAMP="$DIR/${label}_v2_champion.xyz"
  if [ -f "$CHAMP" ]; then
    echo -e "  ${G}✅✅ FINAL CHAMPION DONE${N}"
    [ -f "$DIR/${label}_v2_results.json" ] && python3 -c "
import json
r = json.load(open('$DIR/${label}_v2_results.json'))
print(f\"    champion: rank{r['champion']['rank']} Li{r['champion']['li_trial']} E={r['champion']['e_after']:.4f}\")
" 2>/dev/null
  fi

  # Per-stage checkbox
  echo "  Stage completion:"
  N_DONE=0; N_TOTAL=0
  for s in "${STAGES[@]}"; do
    sname=$(echo "$s" | awk '{print $1}')
    cache=$(echo "$s" | awk '{print $2}')
    dur=$(echo "$s" | awk '{print $3}')
    # Replace comp_ in rank cache with actual comp name
    cache_real=${cache//comp_/${label}_}
    cache_path="$DIR/$cache_real"
    N_TOTAL=$((N_TOTAL+1))
    if [ -f "$cache_path" ]; then
      printf "    ${G}[✓]${N} %-14s ${D}(%5s, %s)${N}\n" "$sname" "$dur" "$cache_real"
      N_DONE=$((N_DONE+1))
    else
      printf "    [ ] %-14s ${D}(%5s, %s)${N}\n" "$sname" "$dur" "$cache_real"
    fi
  done
  echo -e "  ${B}Progress: $N_DONE / $N_TOTAL stages done${N}"

  # Watchdog crash count
  WD_LOG="$DIR/watchdog.log"
  if [ -f "$WD_LOG" ]; then
    N_RETRY=$(grep -c retry "$WD_LOG" 2>/dev/null)
    N_CRASH=$(grep -c "died exit=" "$WD_LOG" 2>/dev/null)
    if [ "$N_CRASH" -gt 0 ]; then
      echo -e "  ${Y}watchdog crashes: $N_CRASH / retries: $N_RETRY${N}"
    else
      echo -e "  watchdog: $N_RETRY entries"
    fi
    LAST_CRASH=$(grep "died exit=" "$WD_LOG" | tail -1)
    [ -n "$LAST_CRASH" ] && echo -e "    ${D}last: $LAST_CRASH${N}"
  fi

  # chain.log: which stage running, last few lines
  CHAIN_LOG="$DIR/chain.log"
  if [ -f "$CHAIN_LOG" ]; then
    AGE_S=$(( $(date +%s) - $(stat -c%Y "$CHAIN_LOG" 2>/dev/null || date +%s) ))
    if [ $AGE_S -gt 300 ]; then AGE_C=$Y; else AGE_C=$G; fi

    # Find last "START" without matching DONE/FAILED → currently running
    LAST_START=$(grep -E "▶ START:" "$CHAIN_LOG" | tail -1 | sed 's/.*START: //' | head -c 40)
    LAST_DONE=$(grep -E "✓ DONE:" "$CHAIN_LOG" | tail -1 | sed 's/.*DONE: //' | head -c 40)
    LAST_FAIL=$(grep -E "✗ FAILED" "$CHAIN_LOG" | tail -1 | sed 's/.*FAILED.*: //' | head -c 40)
    ALL_DONE=$(grep -E "🎉 ALL STAGES DONE" "$CHAIN_LOG")

    echo -e "  chain.log: ${AGE_C}updated ${AGE_S}s ago${N}"
    [ -n "$LAST_START" ] && echo "    last START : $LAST_START"
    [ -n "$LAST_DONE"  ] && echo "    last DONE  : $LAST_DONE"
    [ -n "$LAST_FAIL"  ] && echo -e "    ${R}last FAILED: $LAST_FAIL${N}"
    [ -n "$ALL_DONE"   ] && echo -e "    ${G}🎉 ALL STAGES DONE${N}"

    echo "  last 4 chain.log lines:"
    tail -4 "$CHAIN_LOG" 2>/dev/null | sed 's/^/    /'
  fi
done

# ETA estimate based on done stages
echo -e "\n${B}══ ETA (sum of remaining stage durations) ══${N}"
echo "  Each stage independent; if walltime SIGKILL → re-run chain.sh, cache resume."
echo "  Total successful runtime ≈ 5 + 3×25 + 5 + 5×50 = 335 min ≈ 5.6 h cumulative"
echo "  With ~2h SIGKILL retries on KISTI: expect ~3-4 retries to finish."
echo -e "${B}════════════════════════════════════════════════════════════════════════${N}"
