#!/bin/bash
# gabia_monitor_full_ensemble.sh — detailed monitor for run_v30u_full_ensemble.py.
# Shows: per-comp progress (configs done / 180), ETA, GPU usage, checkpoint
# files, last log lines, process status.
#
# Usage: watch -c -n 30 ./gabia_monitor_full_ensemble.sh
#        while true; do clear; ./gabia_monitor_full_ensemble.sh; sleep 30; done

WORK=/data/work/v30u_ensemble
RESULTS=$WORK/v30u_full_ensemble_results
LOG=$RESULTS/run.log

# Activate uma env (silent, fast)
for base in /data/apps/miniforge3 /scratch/x3430a02/mjs0000/miniforge3 \
            /opt/conda /root/miniforge3 $HOME/miniforge3; do
    if [ -f "$base/etc/profile.d/conda.sh" ]; then
        source "$base/etc/profile.d/conda.sh"
        conda activate uma 2>/dev/null
        break
    fi
done
PY=python

B="\033[1m"; G="\033[1;32m"; Y="\033[1;33m"; R="\033[1;31m"; C="\033[1;36m"; D="\033[2m"; N="\033[0m"

echo -e "${B}════════════════════════════════════════════════════════════════════════"
echo -e "  gabia v30u FULL ensemble monitor (5 z × 36 xy × 6 comps = 1080 configs)"
echo -e "  $(date '+%Y-%m-%d %H:%M:%S')"
echo -e "════════════════════════════════════════════════════════════════════════${N}"

# Process
echo -e "\n${C}── Process ──${N}"
PID=$(pgrep -f "run_v30u_full_ensemble.py" | head -1)
if [ -z "$PID" ]; then
    echo -e "  ${R}NO process running${N}"
else
    ps -p $PID -o pid,etime,pcpu,pmem,cmd --no-headers | \
      awk '{ cmd=""; for(i=5;i<=NF;i++) cmd=cmd" "$i;
             printf "  PID=%s  elapsed=%s  CPU=%s%%  Mem=%s%%  %s\n", $1,$2,$3,$4,cmd }'
fi

# GPU
echo -e "\n${C}── GPU ──${N}"
nvidia-smi --query-gpu=index,name,temperature.gpu,utilization.gpu,memory.used,memory.total \
           --format=csv,noheader,nounits 2>/dev/null | \
  awk -F', ' '{ printf "  GPU%s %s  T=%s°C  Util=%3s%%  Mem=%5s/%5s MB\n", $1,$2,$3,$4,$5,$6 }'

# Checkpoint files
echo -e "\n${C}── Checkpoint files (per-comp) ──${N}"
N_DONE=0
for C in comp1 comp2 comp3 comp4 comp5 modelC; do
    F=$RESULTS/${C}_done.json
    if [ -f "$F" ]; then
        SIZE=$(du -h "$F" | cut -f1)
        # Robust python: handles both keys + index lookup; prints "Wmax±std at d=X.XX"
        INFO=$($PY << PYEOF 2>&1
try:
    import json
    d = json.load(open('$F'))
    m = d.get('Wad_mean', [])
    s = d.get('Wad_std', [])
    g = d.get('gaps', [])
    if m and s and g:
        i = max(range(len(m)), key=lambda k: m[k])
        print(f"Wmax={m[i]:+.3f}±{s[i]:.3f}  d={g[i]:.2f}A  n={d.get('n_samples','?')}")
    else:
        print("(no Wad_mean in json)")
except Exception as e:
    print(f"(parse err: {e})")
PYEOF
)
        echo -e "    ${G}[✓]${N} ${C}_done.json  ($SIZE)  $INFO"
        N_DONE=$((N_DONE+1))
    else
        echo -e "    [ ] ${C}_done.json"
    fi
done
echo -e "  ${B}Done: $N_DONE / 6 comps${N}"

# Current progress (from run.log)
if [ -f "$LOG" ]; then
    AGE_S=$(( $(date +%s) - $(stat -c%Y "$LOG") ))
    if [ $AGE_S -gt 120 ]; then AGE_C=$Y; else AGE_C=$G; fi

    # Last "========= compN =========" → current comp
    CUR_COMP=$(grep -E "========= comp" "$LOG" | tail -1 | sed 's/.*= //' | sed 's/ =.*//')

    # Last "config X/Y" line for that comp
    LAST_PROG=$(grep -E "config [0-9]+/" "$LOG" | tail -1)
    DONE=$(echo "$LAST_PROG" | grep -oE "config [0-9]+" | head -1 | awk '{print $2}')
    TOT=$(echo "$LAST_PROG" | grep -oE "/[0-9]+" | head -1 | tr -d '/')
    ELAPSED=$(echo "$LAST_PROG" | grep -oE "elapsed=[0-9.]+min" | head -1)
    ETA=$(echo "$LAST_PROG" | grep -oE "ETA=[0-9.]+min" | head -1)

    echo -e "\n${C}── Current progress ──${N}"
    echo -e "  log age: ${AGE_C}${AGE_S}s ago${N}"
    if [ -n "$CUR_COMP" ]; then
        echo "  current comp: $CUR_COMP"
        if [ -n "$DONE" ] && [ -n "$TOT" ]; then
            PCT=$((DONE * 100 / TOT))
            BAR_LEN=$((PCT / 5))
            BAR=$(printf '█%.0s' $(seq 1 $BAR_LEN))$(printf '─%.0s' $(seq 1 $((20-BAR_LEN))))
            echo "  configs: $DONE / $TOT  [$BAR] ${PCT}%"
            echo "  $ELAPSED  $ETA"
        fi
    fi

    echo "  last 6 log lines:"
    tail -6 "$LOG" | sed 's/^/    /'
fi

# Overall ETA estimate
echo -e "\n${C}── Overall ETA ──${N}"
if [ $N_DONE -ge 1 ]; then
    # Estimate from elapsed and done comps
    if [ -n "$PID" ]; then
        ELAPSED_SEC=$(ps -p $PID -o etimes --no-headers | tr -d ' ')
        if [ -n "$ELAPSED_SEC" ] && [ "$ELAPSED_SEC" -gt 0 ]; then
            AVG_PER_COMP=$((ELAPSED_SEC / N_DONE))
            REMAINING=$((6 - N_DONE))
            ETA_SEC=$((REMAINING * AVG_PER_COMP))
            ETA_HR=$(echo "scale=1; $ETA_SEC / 3600" | bc 2>/dev/null || echo "?")
            echo "  $N_DONE comps done in $((ELAPSED_SEC/60)) min  →  avg $((AVG_PER_COMP/60)) min/comp"
            echo "  Remaining $REMAINING comps ≈ ${ETA_HR} h"
        fi
    fi
else
    echo "  Need ≥1 comp done for ETA. Initial estimate: ~7 hours total."
fi

# Per-comp summary if done
if [ $N_DONE -ge 1 ]; then
    echo -e "\n${C}── Per-comp W_max_mean (so far) ──${N}"
    $PY << PYEOF 2>&1
import json, os, glob, math
PAPER = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}
print(f"  {'comp':<8} {'W_max_mean':>14} {'std':>8} {'d_min':>8} {'n_samp':>8} {'paper':>7}")
results_dir = '$RESULTS'
files = sorted(glob.glob(os.path.join(results_dir, '*_done.json')))
xs, ys = [], []
for f in files:
    c = os.path.basename(f).replace('_done.json','')
    try:
        d = json.load(open(f))
        m = d.get('Wad_mean', [])
        s = d.get('Wad_std', [])
        g = d.get('gaps', [])
        n = d.get('n_samples', '?')
        if m and s and g:
            i = max(range(len(m)), key=lambda k: m[k])
            paper = PAPER.get(c, '—')
            print(f"  {c:<8} {m[i]:>+14.3f} {s[i]:>8.3f} {g[i]:>8.2f} {str(n):>8} {str(paper):>7}")
            if c in PAPER:
                xs.append(m[i]); ys.append(PAPER[c])
    except Exception as e:
        print(f"  {c}: parse error: {e}")
# Pearson R (pure Python, no numpy)
if len(xs) >= 3:
    n = len(xs)
    mx = sum(xs)/n; my = sum(ys)/n
    num = sum((xs[i]-mx)*(ys[i]-my) for i in range(n))
    dx2 = sum((xs[i]-mx)**2 for i in range(n))
    dy2 = sum((ys[i]-my)**2 for i in range(n))
    denom = math.sqrt(dx2*dy2)
    R = num/denom if denom > 0 else float('nan')
    print(f"\n  R(W_max_mean vs paper exp) = {R:+.4f}  (n={n})")
PYEOF
fi

echo -e "\n${B}════════════════════════════════════════════════════════════════════════${N}"
