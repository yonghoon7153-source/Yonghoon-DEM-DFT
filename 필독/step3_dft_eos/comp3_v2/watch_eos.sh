#!/bin/bash
B="\033[1m"; G="\033[1;32m"; Y="\033[1;33m"; R="\033[1;31m"; C="\033[1;36m"; D="\033[2m"; N="\033[0m"

cd /data/work/comp3_v2_eos

echo -e "${B}════════════════════════════════════════════════════════════════"
echo -e "  comp3 v2 DFT EOS monitor — $(date '+%Y-%m-%d %H:%M:%S')"
echo -e "════════════════════════════════════════════════════════════════${N}"

# Process
echo -e "\n${C}── Process ──${N}"
PID=$(pgrep -f "run_comp3_v2_eos" | head -1)
QPID=$(pgrep -f "pw.x.*comp3" | head -1)
if [ -n "$PID" ]; then
    ps -p $PID -o pid,etime,pcpu,pmem,cmd --no-headers | awk '{ printf "  runner PID=%s  elapsed=%s  CPU=%s%%\n", $1,$2,$3 }'
fi
if [ -n "$QPID" ]; then
    ps -p $QPID -o pid,etime,pcpu,pmem,cmd --no-headers | awk '{ cmd=""; for(i=5;i<=NF;i++) cmd=cmd" "$i;
        printf "  pw.x   PID=%s  elapsed=%s  CPU=%s%%  Mem=%s%%\n", $1,$2,$3,$4 }'
else
    echo -e "  ${Y}no pw.x running${N}"
fi

# GPU
echo -e "\n${C}── GPU ──${N}"
nvidia-smi --query-gpu=index,name,temperature.gpu,utilization.gpu,memory.used,memory.total --format=csv,noheader,nounits 2>/dev/null | \
  awk -F', ' '{ printf "  GPU%s %s  T=%s°C  Util=%3s%%  Mem=%5s/%5s MB\n", $1,$2,$3,$4,$5,$6 }'

# Volume progress
echo -e "\n${C}── Volume progress (11 vols) ──${N}"
N_DONE=0; N_RUNNING=0
for v in 098 099 100 101 102 103 104 105 106 107 108; do
    OUT="comp3_v2_eos_v${v}.out"
    if [ -f "$OUT" ]; then
        JD=$(grep -c "JOB DONE" "$OUT")
        if [ "$JD" -gt 0 ]; then
            E=$(grep "!" "$OUT" | tail -1 | awk '{print $5}')
            P=$(grep "total   stress" "$OUT" | tail -1 | awk '{print $6}')
            BFGS=$(grep -c "bfgs converged" "$OUT")
            echo -e "  ${G}[✓ v${v}]${N}  E=$E Ry  P=$P kbar  bfgs=$BFGS"
            N_DONE=$((N_DONE+1))
        else
            ITER=$(grep -c "iteration #" "$OUT")
            BFGS=$(grep -c "BFGS Geometry Optimization" "$OUT")
            LAST_E=$(grep "total energy" "$OUT" | tail -1 | awk '{print $5}')
            SIZE=$(du -k "$OUT" | cut -f1)
            echo -e "  ${Y}[▶ v${v}]${N}  iter=$ITER  bfgs=$BFGS  E_last=$LAST_E  ${SIZE}K"
            N_RUNNING=1
        fi
    else
        echo "  [ ] v${v}"
    fi
done
echo -e "  ${B}Done: $N_DONE / 11${N}"

# Estimate ETA
if [ $N_DONE -gt 0 ] && [ -n "$PID" ]; then
    ELAPSED_SEC=$(ps -p $PID -o etimes --no-headers | tr -d ' ')
    if [ -n "$ELAPSED_SEC" ] && [ "$ELAPSED_SEC" -gt 0 ]; then
        AVG=$((ELAPSED_SEC / N_DONE))
        REMAIN=$((11 - N_DONE))
        ETA_SEC=$((REMAIN * AVG))
        ETA_H=$(echo "scale=1; $ETA_SEC / 3600" | bc 2>/dev/null || echo "?")
        echo -e "  avg ${AVG}s/vol  →  remaining $REMAIN vols ≈ ${ETA_H} h"
    fi
fi

# Current volume detail
CURRENT=$(grep -lE "^[^A].*PWSCF v\.7\.4\.1" /data/work/comp3_v2_eos/comp3_v2_eos_v*.out 2>/dev/null | \
  xargs -I{} sh -c 'JD=$(grep -c "JOB DONE" "{}"); if [ "$JD" -eq 0 ]; then echo "{}"; fi' 2>/dev/null | tail -1)
if [ -n "$CURRENT" ]; then
    echo -e "\n${C}── Current volume detail (${CURRENT##*/}) ──${N}"
    tail -10 "$CURRENT" | sed 's/^/    /'
fi

echo -e "\n${B}════════════════════════════════════════════════════════════════${N}"
