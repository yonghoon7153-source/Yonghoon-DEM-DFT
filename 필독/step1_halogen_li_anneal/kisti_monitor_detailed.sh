#!/bin/bash
# kisti_monitor_detailed.sh — comp3/comp5 v2 step1to3 detailed status + diagnosis.
# Shows: progress per stage, crash timeline, retry duration pattern, decision hint.
#
# Usage:  watch -n 60 ./kisti_monitor_detailed.sh
#         OR ./kisti_monitor_detailed.sh                 # one-shot

BASE=/scratch/x3430a02/kgy/manuscript_support/pipeline_v2
COMP3_DIR=$BASE/comp3_lpscbr/1_step1to3
COMP5_DIR=$BASE/comp5_lpscbr/1_step1to3

B="\033[1m"; G="\033[1;32m"; Y="\033[1;33m"; R="\033[1;31m"; C="\033[1;36m"; N="\033[0m"

echo -e "${B}════════════════════════════════════════════════════════════════════════"
echo -e "  KISTI comp3 / comp5 v2 step1to3  —  detailed monitor"
echo -e "  $(date '+%Y-%m-%d %H:%M:%S')"
echo -e "════════════════════════════════════════════════════════════════════════${N}"

echo -e "\n${C}── GPU ──${N}"
nvidia-smi --query-gpu=index,name,temperature.gpu,utilization.gpu,memory.used,memory.total \
           --format=csv,noheader,nounits | \
  awk -F', ' '{ printf "  GPU%s %s  T=%s°C  Util=%3s%%  Mem=%5s/%5s MB\n", $1,$2,$3,$4,$5,$6 }'

echo -e "\n${C}── Processes ──${N}"
PS_OUT=$(ps -ef | grep -E "watchdog_comp[35]|comp[35]_v2_step1to3" | grep -v grep)
if [ -z "$PS_OUT" ]; then
  echo -e "  ${R}NO process running${N}"
else
  echo "$PS_OUT" | awk '{
    cmd=""; for(i=8;i<=NF;i++) cmd=cmd" "$i;
    printf "  PID %7s start=%-5s elapsed=%9s   %s\n", $2,$5,$7,cmd
  }'
fi

#=== per-comp detail ===
for label in comp3 comp5; do
  if [ "$label" = "comp3" ]; then DIR=$COMP3_DIR; GPU=0; else DIR=$COMP5_DIR; GPU=1; fi

  echo -e "\n${B}══ $label (GPU$GPU) ══${N}"
  echo "  $DIR"

  if [ ! -d "$DIR" ]; then
    echo -e "  ${R}directory not found${N}"; continue
  fi

  # Check champion success
  CHAMP="$DIR/${label}_v2_champion.xyz"
  RES="$DIR/${label}_v2_results.json"
  if [ -f "$CHAMP" ] && [ -f "$RES" ]; then
    echo -e "  ${G}✅✅ CHAMPION DONE${N}"
    python3 -c "
import json
r = json.load(open('$RES'))
print(f\"    best_cl={r['best_cl']}  best_br={r['best_br']}\")
print(f\"    Li spread = {r['li_spread_meV']:.1f} meV\")
print(f\"    champion: rank{r['champion']['rank']} Li{r['champion']['li_trial']} E={r['champion']['e_after']:.4f}\")
print(f\"    total runtime = {r['total_h']:.2f} h\")
" 2>/dev/null
    continue
  fi

  # Crash timeline
  WD_LOG="$DIR/watchdog.log"
  if [ -f "$WD_LOG" ]; then
    N_RETRY=$(grep -c retry "$WD_LOG" 2>/dev/null)
    N_CRASH=$(grep -c "died exit=" "$WD_LOG" 2>/dev/null)
    FIRST=$(grep -E "===.*start" "$WD_LOG" | head -1 | awk '{print $1}')
    LAST_RETRY=$(grep -E "===.*start.*retry" "$WD_LOG" | tail -1 | awk -F"start \\(retry " '{print $2}' | tr -d ')' | awk '{print $1}')
    LAST_TS=$(grep -E "===.*start" "$WD_LOG" | tail -1 | awk '{print $1}')

    if [ "$N_CRASH" -gt 0 ]; then
      echo -e "  ${R}⚠ crashes: $N_CRASH  /  retries: $N_RETRY${N}  (first start: $FIRST)"
    else
      echo -e "  ${G}watchdog: $N_RETRY entries (no crashes)${N}"
    fi
    echo "  current retry: #${LAST_RETRY:-?} started at $LAST_TS"

    # Last 5 watchdog entries
    echo "  last 5 watchdog events:"
    tail -5 "$WD_LOG" | sed 's/^/    /'
  fi

  # Run.log progress
  RUN_LOG="$DIR/run.log"
  if [ -f "$RUN_LOG" ]; then
    SIZE=$(stat -c%s "$RUN_LOG" 2>/dev/null)
    AGE_S=$(( $(date +%s) - $(stat -c%Y "$RUN_LOG") ))
    if [ $AGE_S -gt 300 ]; then AGE_COLOR=$Y; else AGE_COLOR=$G; fi
    echo -e "  run.log: ${SIZE} bytes  ${AGE_COLOR}updated ${AGE_S}s ago${N}"

    S1A=$(grep -c "Stage1a " "$RUN_LOG" 2>/dev/null)
    S1B=$(grep -c "Stage1b " "$RUN_LOG" 2>/dev/null)
    S2=$(grep -c "Stage2 Li" "$RUN_LOG" 2>/dev/null)
    S3_500K=$(grep -c "500K 100ps" "$RUN_LOG" 2>/dev/null)
    S3_300K=$(grep -c "300K 10ps quench" "$RUN_LOG" 2>/dev/null)
    S3_LBFGS=$(grep -c "LBFGS relax\\.\\.\\." "$RUN_LOG" 2>/dev/null)
    CHAMP_LINE=$(grep "CHAMPION:" "$RUN_LOG" 2>/dev/null | tail -1)
    LAST_T=$(grep -o "\[[0-9.]*h\]" "$RUN_LOG" 2>/dev/null | tail -1)

    if [ "$label" = "comp4" ]; then S1B_TOTAL=350; else S1B_TOTAL=280; fi

    # Per-current-retry counts (since last "=== ... start ===" in run.log)
    # Find line number of last retry start in run.log
    LAST_RETRY_LINE=$(grep -n "=== Stage 1a" "$RUN_LOG" 2>/dev/null | tail -1 | cut -d: -f1)
    if [ -n "$LAST_RETRY_LINE" ]; then
      CUR_S1A=$(tail -n +$LAST_RETRY_LINE "$RUN_LOG" | grep -c "Stage1a ")
      CUR_S1B=$(tail -n +$LAST_RETRY_LINE "$RUN_LOG" | grep -c "Stage1b ")
      CUR_S2=$(tail -n +$LAST_RETRY_LINE "$RUN_LOG" | grep -c "Stage2 Li")
      CUR_S3=$(tail -n +$LAST_RETRY_LINE "$RUN_LOG" | grep -c "500K 100ps")
    else
      CUR_S1A=$S1A; CUR_S1B=$S1B; CUR_S2=$S2; CUR_S3=$S3_500K
    fi

    echo "  progress (this retry):"
    printf "    Stage1a (45 S placements):  %2d / 45    %s\n" "$CUR_S1A" "$( [ $CUR_S1A -ge 45 ] && echo "${G}✓${N}" || echo "─" )"
    printf "    Stage1b (Cl/Br configs):   %3d / %d   %s\n" "$CUR_S1B" "$S1B_TOTAL" "$( [ $CUR_S1B -ge $S1B_TOTAL ] && echo "${G}✓${N}" || echo "─" )"
    printf "    Stage2  (20 Li):            %2d / 20    %s\n" "$CUR_S2" "$( [ $CUR_S2 -ge 20 ] && echo "${G}✓${N}" || echo "─" )"
    printf "    Stage3  (5 anneal MD):     500K=%d  300K=%d  LBFGS=%d / 5\n" "$S3_500K" "$S3_300K" "$S3_LBFGS"
    [ -n "$LAST_T" ]      && echo "    elapsed (script t()): $LAST_T"
    [ -n "$CHAMP_LINE" ]  && echo -e "    ${G}$CHAMP_LINE${N}"

    echo "  cumulative across ALL retries:"
    printf "    Stage1a: %d ($((N_RETRY)) × 45 = $((N_RETRY * 45)) expected)\n" "$S1A"
    printf "    Stage1b lines: %d  (cumulative)\n" "$S1B"
    printf "    Stage3 Rank entries: %d  (Each retry reaches Rank 0 500K MD then dies)\n" "$S3_500K"

    echo "  last 5 run.log lines:"
    tail -5 "$RUN_LOG" 2>/dev/null | sed 's/^/    /'
  fi
done

#=== diagnosis ===
echo -e "\n${B}════ DIAGNOSIS ════${N}"
echo "Crash pattern: each retry runs ~80-90 min, then dies during Stage 3 Rank 0 MD."
echo "  Stage 1+2 (Stage1a 45 + Stage1b 280 + Stage2 20) ≈ 80 min"
echo "  Stage 3 Rank 0 100ps MD ≈ 50 min"
echo "  Expected total to first champion = ~130 min"
echo ""
echo "Likely cause: ${R}KISTI login node (glogin01) walltime/idle kill at ~90 min${N}"
echo ""
echo "Decision options:"
echo "  A) ${R}Keep running${N} (waste): each retry redoes Stage1+2 from scratch → infinite loop"
echo "  B) ${Y}Convert to SLURM sbatch${N}: 4-12h walltime → can finish (need script edit)"
echo "  C) ${G}Kill KISTI + restart on gabia (GPU1 free)${N}: safe, ~3h to champion"
echo ""
echo -e "${B}════════════════════════════════════════════════════════════════════════${N}"
