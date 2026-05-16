#!/usr/bin/env bash
# watch_status.sh — comprehensive dashboard for long-running doping batch.
#
# Shows in one screen:
#   - Wall clock time + machine uptime
#   - GPU utilisation
#   - All UMA / anneal / postproc python processes
#   - Per-stage progress (lines parsed from logs/*.log)
#   - Disk space
#   - Latest 5 lines from each active log
#
# Usage:
#   watch -n 30 'bash tools/doping/watch_status.sh'

set -e
REPO="${REPO:-/data/work/v30u_ensemble/Yonghoon-DEM-DFT}"
cd "$REPO" 2>/dev/null || true

echo "================================================================"
echo "  Doping pipeline status  —  $(date +'%Y-%m-%d %H:%M:%S')"
echo "================================================================"

# --- System ---
echo ""
echo "▸ System"
uptime | awk '{print "  uptime:", $0}'
df -h "$REPO" 2>/dev/null | awk 'NR==2 {print "  disk:   " $5 " used of " $2 " (" $4 " free)"}'

# --- GPU ---
echo ""
echo "▸ GPU"
nvidia-smi --query-gpu=index,utilization.gpu,memory.used,memory.total,temperature.gpu \
           --format=csv,noheader 2>/dev/null \
  | awk -F, '{printf "  GPU%s: util=%s, mem=%sMB/%sMB, T=%s°C\n", $1, $2, $3, $4, $5}'

# --- Processes ---
echo ""
echo "▸ Active python processes (doping tools)"
ps -eo pid,etime,pcpu,pmem,cmd 2>/dev/null \
  | grep -E "(run_uma_screening|run_anneal|run_mlip_postproc|tier_cascade|preflight)" \
  | grep -v grep \
  | awk '{printf "  PID %s  elapsed=%s  CPU=%s%%  MEM=%s%%  %s\n", $1, $2, $3, $4, $5" "$6" "$7" "$8" "$9" "$10}' \
  | head -10
if ! ps -eo cmd 2>/dev/null | grep -qE "(run_uma_screening|run_anneal|run_mlip_postproc|preflight)" \
  | grep -v grep; then
    echo "  (none running)"
fi

# --- Progress per log ---
echo ""
echo "▸ Progress per log"
for log in logs/uma_*.log logs/anneal_*.log logs/postproc_*.log logs/v3_*.log logs/tier_*.log logs/cascade.log; do
    [ -f "$log" ] || continue
    # Latest count like '[N/Total]'
    latest=$(grep -oE '\[[0-9]+/[0-9]+\]' "$log" 2>/dev/null | tail -1)
    last_done=$(grep -E "✓|DONE" "$log" 2>/dev/null | tail -1 | cut -c-80)
    size=$(du -h "$log" 2>/dev/null | awk '{print $1}')
    mtime=$(stat -c '%y' "$log" 2>/dev/null | cut -d. -f1)
    echo "  $log ($size, last touched $mtime)"
    echo "    progress: ${latest:-N/A}"
    [ -n "$last_done" ] && echo "    last: $last_done"
done

# --- Results JSON sizes ---
echo ""
echo "▸ Result JSON sizes (so far)"
for j in runs/*/uma_results.json runs/*/anneal_results.json \
         runs/*/postproc_summary.json runs/*/winners.json 2>/dev/null; do
    [ -f "$j" ] || continue
    size=$(du -h "$j" 2>/dev/null | awk '{print $1}')
    nrec=$(python3 -c "
import json
try:
    d = json.load(open('$j'))
    if 'results' in d: print(len(d['results']))
    elif 'records' in d: print(len(d['records']))
    elif 'winners' in d: print(len(d['winners']))
    else: print('?')
except Exception: print('err')
" 2>/dev/null)
    echo "  $j ($size, $nrec records)"
done

# --- Bottom-line ---
echo ""
echo "================================================================"
