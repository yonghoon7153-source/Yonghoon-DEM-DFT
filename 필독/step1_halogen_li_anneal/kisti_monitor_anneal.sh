#!/bin/bash
# kisti_monitor_anneal.sh — detailed monitor for new anneal_chain.sh.
# Shows per-comp 5×5 progress matrix (rank × li) + MD steps + crash count.

BASE=/scratch/x3430a02/kgy/manuscript_support/pipeline_v2
COMP3_DIR=$BASE/comp3_lpscbr/1_step1to3
COMP5_DIR=$BASE/comp5_lpscbr/1_step1to3

B="\033[1m"; G="\033[1;32m"; Y="\033[1;33m"; R="\033[1;31m"; C="\033[1;36m"; D="\033[2m"; M="\033[35m"; N="\033[0m"

echo -e "${B}════════════════════════════════════════════════════════════════════════"
echo -e "  comp3 / comp5 v2 anneal_chain monitor"
echo -e "  $(date '+%Y-%m-%d %H:%M:%S')"
echo -e "════════════════════════════════════════════════════════════════════════${N}"

echo -e "\n${C}── GPU ──${N}"
nvidia-smi --query-gpu=index,name,temperature.gpu,utilization.gpu,memory.used,memory.total \
           --format=csv,noheader,nounits 2>/dev/null | \
  awk -F', ' '{ printf "  GPU%s %s  T=%s°C  Util=%3s%%  Mem=%5s/%5s MB\n", $1,$2,$3,$4,$5,$6 }'

echo -e "\n${C}── Processes ──${N}"
PS_OUT=$(ps -ef | grep -E "watchdog_comp[35]|anneal_chain|anneal_(stage2|md|finish|champion)" | grep -v grep)
if [ -z "$PS_OUT" ]; then
    echo -e "  ${R}NO process running${N}"
else
    echo "$PS_OUT" | awk '{
        cmd=""; for(i=8;i<=NF;i++) cmd=cmd" "$i;
        if (length(cmd) > 70) cmd = substr(cmd, 1, 67) "...";
        printf "  PID %7s start=%-5s CPU=%-9s %s\n", $2,$5,$7,cmd
    }'
fi

for label in comp3 comp5; do
    if [ "$label" = "comp3" ]; then DIR=$COMP3_DIR; GPU=0; else DIR=$COMP5_DIR; GPU=1; fi
    echo -e "\n${B}══ $label (GPU$GPU) ══${N}"

    if [ ! -d "$DIR" ]; then
        echo -e "  ${R}directory not found${N}"; continue
    fi

    # Stage 2 completion (5 ranks)
    echo "  Stage 2 (one per rank):"
    S2_DONE=0
    S2_ROW="    "
    for RANK in 0 1 2 3 4; do
        if [ -f "$DIR/cache_stage2_rank${RANK}.json" ]; then
            S2_ROW="$S2_ROW ${G}[r$RANK ✓]${N}"
            S2_DONE=$((S2_DONE+1))
        else
            S2_ROW="$S2_ROW [r$RANK  ]"
        fi
    done
    echo -e "$S2_ROW   ($S2_DONE/5)"

    # 5×5 (rank, li) matrix
    echo "  Anneal matrix (rows=rank, cols=li):"
    echo -e "          li=0       li=1       li=2       li=3       li=4"
    TOTAL_DONE=0
    for RANK in 0 1 2 3 4; do
        ROW="    r$RANK:"
        for LI in 0 1 2 3 4; do
            ANN_JSON="$DIR/rank${RANK}_li${LI}_anneal.json"
            MD_JSON="$DIR/rank${RANK}_li${LI}_md.json"
            if [ -f "$ANN_JSON" ]; then
                # Both MD and finish done — extract E_after
                E=$(python3 -c "import json; r=json.load(open('$ANN_JSON')); print(f'{r[\"E_after\"]:.3f}')" 2>/dev/null)
                ROW="$ROW  ${G}[✓ $E]${N}"
                TOTAL_DONE=$((TOTAL_DONE+1))
            elif [ -f "$MD_JSON" ]; then
                # MD partial / done; finish not yet
                MD_INFO=$(python3 -c "
import json
d = json.load(open('$MD_JSON'))
done = d.get('done', False)
n = d.get('steps_done', 0)
print(f'{n}|{done}')
" 2>/dev/null)
                STEPS=$(echo $MD_INFO | cut -d'|' -f1)
                MD_DONE=$(echo $MD_INFO | cut -d'|' -f2)
                if [ "$MD_DONE" = "True" ]; then
                    ROW="$ROW  ${Y}[Q wait ]${N}"
                else
                    PCT=$((STEPS * 100 / 100000))
                    ROW="$ROW  ${M}[MD ${PCT}%]${N}"
                fi
            else
                ROW="$ROW  [        ]"
            fi
        done
        echo -e "$ROW"
    done
    echo -e "  ${B}Progress: $TOTAL_DONE / 25 (rank,li) pairs DONE${N}"

    # Watchdog crash count
    WD_LOG="$DIR/watchdog.log"
    if [ -f "$WD_LOG" ]; then
        N_RETRY=$(grep -c retry "$WD_LOG" 2>/dev/null)
        N_CRASH=$(grep -c "died exit=" "$WD_LOG" 2>/dev/null)
        if [ "$N_CRASH" -gt 0 ]; then
            echo -e "  ${Y}watchdog: $N_CRASH crashes / $N_RETRY retries${N}"
            tail -1 "$WD_LOG" | sed 's/^/    last: /'
        else
            echo -e "  watchdog: $N_RETRY entries  ${D}(no crashes)${N}"
        fi
    fi

    # anneal_chain.log: last STARTED / DONE / FAILED
    AC_LOG="$DIR/anneal_chain.log"
    if [ -f "$AC_LOG" ]; then
        AGE_S=$(( $(date +%s) - $(stat -c%Y "$AC_LOG") ))
        if [ $AGE_S -gt 600 ]; then AGE_C=$Y; else AGE_C=$G; fi
        echo -e "  anneal_chain.log: ${AGE_C}updated ${AGE_S}s ago${N}"
        LAST_START=$(grep -E "▶" "$AC_LOG" | tail -1 | sed 's/.*▶ //')
        LAST_FAIL=$(grep -E "✗ FAILED" "$AC_LOG" | tail -1 | sed 's/.*FAILED.*: //')
        [ -n "$LAST_START" ] && echo "    last ▶ : $LAST_START"
        [ -n "$LAST_FAIL"  ] && echo -e "    ${R}last ✗ : $LAST_FAIL${N}"
        echo "    last 3 lines:"
        tail -3 "$AC_LOG" | sed 's/^/      /'
    fi
done

echo -e "\n${B}════════════════════════════════════════════════════════════════════════${N}"
echo -e "${D}Legend: [r✓]=stage2 done  [MD x%]=MD running  [Q wait]=MD done, quench pending  [✓ E]=full done${N}"
