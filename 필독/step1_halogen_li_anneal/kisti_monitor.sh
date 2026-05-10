#!/bin/bash
# kisti_monitor.sh — 엄청 자세한 watch 용 status snapshot.
#
# Usage:
#   ./kisti_monitor.sh                    # one-shot detailed status
#   watch -n 30 ./kisti_monitor.sh        # auto-refresh every 30s
#   watch -c -n 30 ./kisti_monitor.sh     # with color (if supported)
#
# Hard-codes KISTI pipeline_v2 paths. Edit BASE if elsewhere.

BASE=/scratch/x3430a02/kgy/manuscript_support/pipeline_v2
COMP3_DIR=$BASE/comp3_lpscbr/1_step1to3
COMP5_DIR=$BASE/comp5_lpscbr/1_step1to3

# Color helpers
B="\033[1m"; G="\033[1;32m"; Y="\033[1;33m"; R="\033[1;31m"; C="\033[1;36m"; N="\033[0m"

echo -e "${B}=========================================="
echo -e "  KISTI comp3/comp5 v2 monitor"
echo -e "  $(date '+%Y-%m-%d %H:%M:%S')"
echo -e "==========================================${N}"

echo -e "\n${C}── GPU usage ──${N}"
nvidia-smi --query-gpu=index,name,temperature.gpu,utilization.gpu,memory.used,memory.total \
           --format=csv,noheader,nounits | \
  awk -F', ' '{
    printf "  GPU%s %s  T=%s°C  Util=%3s%%  Mem=%5s/%5s MB\n", $1,$2,$3,$4,$5,$6
  }'

echo -e "\n${C}── Processes ──${N}"
PS_OUT=$(ps -ef | grep -E "watchdog_comp[35]|comp[35]_v2_step1to3|anneal_rank.py" | grep -v grep)
if [ -z "$PS_OUT" ]; then
  echo -e "  ${R}(no watchdog or python process running)${N}"
else
  echo "$PS_OUT" | awk '{
    cmd=""; for(i=8;i<=NF;i++) cmd=cmd" "$i;
    printf "  PID %s  start=%s  CPU=%s  %s\n", $2,$5,$7,cmd
  }'
fi

# Per-comp detail
for label in comp3 comp5; do
  if [ "$label" = "comp3" ]; then DIR=$COMP3_DIR; GPU=0; else DIR=$COMP5_DIR; GPU=1; fi

  echo -e "\n${B}── $label  (GPU$GPU,  $DIR) ──${N}"

  if [ ! -d "$DIR" ]; then
    echo -e "  ${R}directory not found${N}"; continue
  fi

  # Output files
  CHAMP="$DIR/${label}_v2_champion.xyz"
  RES="$DIR/${label}_v2_results.json"
  if [ -f "$CHAMP" ] && [ -f "$RES" ]; then
    echo -e "  ${G}DONE${N}  champion + results.json present"
    # quick summary
    python3 -c "
import json
r = json.load(open('$RES'))
print(f\"  best_cl={r['best_cl']}  best_br={r['best_br']}\")
print(f\"  Li spread = {r['li_spread_meV']:.1f} meV\")
ch = r['champion']
print(f\"  champion rank{ch['rank']} Li{ch['li_trial']} E_after = {ch['e_after']:.4f} eV\")
print(f\"  total = {r['total_h']:.2f} h\")
" 2>/dev/null || echo "  (could not parse $RES)"
    continue
  fi

  RUN_LOG="$DIR/run.log"
  WD_LOG="$DIR/watchdog.log"

  # Watchdog log: retry count + last line
  if [ -f "$WD_LOG" ]; then
    RETRY=$(grep -c "retry" "$WD_LOG" 2>/dev/null)
    DIED=$(grep -c "died exit=" "$WD_LOG" 2>/dev/null)
    LAST_WD=$(tail -1 "$WD_LOG" 2>/dev/null)
    if [ "$DIED" -gt 0 ]; then
      echo -e "  ${Y}watchdog: ${DIED} crashes / ${RETRY} retries${N}"
    else
      echo -e "  watchdog: ${RETRY} entries (no crashes)"
    fi
    echo "    last: $LAST_WD"
  else
    echo -e "  ${R}no watchdog.log yet (script not started?)${N}"
  fi

  # Run log: parse stage progress
  if [ -f "$RUN_LOG" ]; then
    SIZE=$(stat -c%s "$RUN_LOG" 2>/dev/null)
    LASTMOD=$(stat -c%y "$RUN_LOG" 2>/dev/null | cut -d. -f1)
    AGE_S=$(( $(date +%s) - $(stat -c%Y "$RUN_LOG") ))
    echo -e "  run.log: ${SIZE} bytes  modified=$LASTMOD  (${AGE_S}s ago)"

    # Stage progress
    S1A=$(grep -c "Stage1a " "$RUN_LOG" 2>/dev/null)
    S1B=$(grep -c "Stage1b " "$RUN_LOG" 2>/dev/null)
    S2=$(grep -c "Stage2 Li" "$RUN_LOG" 2>/dev/null)
    S3_500K=$(grep -c "500K 100ps" "$RUN_LOG" 2>/dev/null)
    S3_300K=$(grep -c "300K 10ps quench" "$RUN_LOG" 2>/dev/null)
    S3_LBFGS=$(grep -c "LBFGS relax" "$RUN_LOG" 2>/dev/null)
    CHAMP_LINE=$(grep "CHAMPION:" "$RUN_LOG" 2>/dev/null | tail -1)
    LAST_T=$(grep -o "\[[0-9.]*h\]" "$RUN_LOG" 2>/dev/null | tail -1)

    # Total Stage 1b expected: comp4=350 / comp3,5=280
    if [ "$label" = "comp4" ]; then S1B_TOTAL=350; else S1B_TOTAL=280; fi

    echo "  progress:"
    printf "    Stage1a (45 S placements):  %d / 45\n" "$S1A"
    printf "    Stage1b (Cl/Br configs):    %d / %d\n" "$S1B" "$S1B_TOTAL"
    printf "    Stage2  (20 Li):            %d / 20\n" "$S2"
    printf "    Stage3  (5 anneal MD):      500K=%d  300K=%d  LBFGS=%d  / 5\n" "$S3_500K" "$S3_300K" "$S3_LBFGS"
    [ -n "$LAST_T" ]      && echo "    elapsed (script): $LAST_T"
    [ -n "$CHAMP_LINE" ]  && echo -e "    ${G}$CHAMP_LINE${N}"

    # Last 3 actual log lines
    echo "  last 3 lines of run.log:"
    tail -3 "$RUN_LOG" 2>/dev/null | sed 's/^/    /'
  else
    echo -e "  ${R}no run.log yet${N}"
  fi
done

echo -e "\n${B}==========================================${N}"
