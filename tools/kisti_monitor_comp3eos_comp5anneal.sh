#!/bin/bash
# kisti_monitor_comp3eos_comp5anneal.sh — combined monitor for:
#   GPU0: comp3 v2 DFT EOS (paper protocol, 11 vols)
#   GPU1: comp5 anneal_chain (5×5 rank×li matrix)

COMP3=/scratch/x3430a02/kgy/manuscript_support/pipeline_v2/comp3_lpscbr
COMP5=/scratch/x3430a02/kgy/manuscript_support/pipeline_v2/comp5_lpscbr/1_step1to3

B="\033[1m"; G="\033[1;32m"; Y="\033[1;33m"; R="\033[1;31m"; C="\033[1;36m"; D="\033[2m"; M="\033[35m"; N="\033[0m"

echo -e "${B}════════════════════════════════════════════════════════════════════════"
echo -e "  KISTI: comp3 v2 DFT EOS (GPU0) + comp5 anneal (GPU1)"
echo -e "  $(date '+%Y-%m-%d %H:%M:%S')"
echo -e "════════════════════════════════════════════════════════════════════════${N}"

# GPU
echo -e "\n${C}── GPU ──${N}"
nvidia-smi --query-gpu=index,name,temperature.gpu,utilization.gpu,memory.used,memory.total \
           --format=csv,noheader,nounits 2>/dev/null | \
  awk -F', ' '{ printf "  GPU%s %s  T=%s°C  Util=%3s%%  Mem=%5s/%5s MB\n", $1,$2,$3,$4,$5,$6 }'

# Processes
echo -e "\n${C}── Processes ──${N}"
PS_OUT=$(ps -ef | grep -E "watchdog_comp|anneal_chain|anneal_md|anneal_finish|pw\.x|run_dft_eos|auto_restart" | grep -v grep)
if [ -z "$PS_OUT" ]; then
    echo -e "  ${R}NO processes running${N}"
else
    echo "$PS_OUT" | awk '{
        cmd=""; for(i=8;i<=NF;i++) cmd=cmd" "$i;
        if (length(cmd) > 70) cmd = substr(cmd, 1, 67) "...";
        printf "  PID %7s start=%-5s CPU=%-9s %s\n", $2,$5,$7,cmd
    }'
fi

# ============================================================
#  comp3 v2 DFT EOS (GPU0)
# ============================================================
echo -e "\n${B}══ comp3 v2 DFT EOS (GPU0) ══${N}"

if [ ! -d "$COMP3/dft_eos" ]; then
    echo -e "  ${R}dft_eos directory not found${N}"
else
    N_DONE=0
    N_RUNNING=0
    N_TOTAL=11
    echo "  Vol progress:"
    for v in 098 099 100 101 102 103 104 105 106 107 108; do
        OUT="$COMP3/dft_eos/v${v}/relax.out"
        if [ -f "$OUT" ]; then
            if grep -qE "bfgs converged in|End of BFGS Geometry" "$OUT" 2>/dev/null; then
                E=$(grep "!" "$OUT" | tail -1 | awk '{print $5}')
                echo -e "    ${G}[✓ v${v}]${N}  E=$E Ry"
                N_DONE=$((N_DONE+1))
            else
                ITER=$(grep -c "^     iteration #" "$OUT" 2>/dev/null)
                BFGS=$(grep -c "new energy" "$OUT" 2>/dev/null)
                LAST_ACC=$(grep "estimated scf accuracy" "$OUT" | tail -1 | awk '{print $NF}')
                SIZE=$(du -k "$OUT" | cut -f1)
                echo -e "    ${Y}[▶ v${v}]${N}  iter=$ITER bfgs=$BFGS acc=$LAST_ACC ${SIZE}K"
                N_RUNNING=1
            fi
        else
            echo "    [ ] v${v}"
        fi
    done
    echo -e "  ${B}Done: $N_DONE / $N_TOTAL${N}"

    # auto_restart.log
    AR_LOG="$COMP3/auto_restart.log"
    if [ -f "$AR_LOG" ]; then
        AGE_S=$(( $(date +%s) - $(stat -c%Y "$AR_LOG") ))
        if [ $AGE_S -gt 600 ]; then AGE_C=$Y; else AGE_C=$G; fi
        echo -e "  auto_restart.log: ${AGE_C}${AGE_S}s ago${N}"
        echo "  last 3 lines:"
        tail -3 "$AR_LOG" | sed 's/^/    /'
    fi

    # Currently running vol detail
    CUR_VOL=""
    for v in 098 099 100 101 102 103 104 105 106 107 108; do
        OUT="$COMP3/dft_eos/v${v}/relax.out"
        if [ -f "$OUT" ] && ! grep -qE "bfgs converged in|End of BFGS Geometry" "$OUT" 2>/dev/null; then
            CUR_VOL="v${v}"
            break
        fi
    done
    if [ -n "$CUR_VOL" ]; then
        OUT="$COMP3/dft_eos/${CUR_VOL}/relax.out"
        AGE_S=$(( $(date +%s) - $(stat -c%Y "$OUT") ))
        echo -e "  Current ${CUR_VOL} (log ${AGE_S}s ago):"
        # Last SCF iter + accuracy
        LAST_ITER=$(grep "^     iteration #" "$OUT" | tail -1 | tr -s ' ' | sed 's/^ //')
        LAST_TOTE=$(grep "total energy" "$OUT" | tail -1 | awk '{print $5}')
        LAST_FORCE=$(grep "Total force" "$OUT" | tail -1 | awk '{print $4}')
        [ -n "$LAST_ITER" ] && echo "    $LAST_ITER"
        [ -n "$LAST_TOTE" ] && echo "    E=$LAST_TOTE Ry,  Total force=$LAST_FORCE"
    fi
fi

# ============================================================
#  comp5 anneal_chain (GPU1)
# ============================================================
echo -e "\n${B}══ comp5 anneal_chain (GPU1) ══${N}"

if [ ! -d "$COMP5" ]; then
    echo -e "  ${R}comp5 directory not found${N}"
else
    # Stage 2
    echo "  Stage 2 (one per rank):"
    S2_DONE=0
    S2_ROW="    "
    for RANK in 0 1 2 3 4; do
        if [ -f "$COMP5/cache_stage2_rank${RANK}.json" ]; then
            S2_ROW="$S2_ROW ${G}[r$RANK ✓]${N}"
            S2_DONE=$((S2_DONE+1))
        else
            S2_ROW="$S2_ROW [r$RANK  ]"
        fi
    done
    echo -e "$S2_ROW   ($S2_DONE/5)"

    # 5×5 matrix
    echo "  Anneal matrix (rows=rank, cols=li):"
    echo -e "          li=0       li=1       li=2       li=3       li=4"
    TOTAL_DONE=0
    for RANK in 0 1 2 3 4; do
        ROW="    r$RANK:"
        for LI in 0 1 2 3 4; do
            ANN_JSON="$COMP5/rank${RANK}_li${LI}_anneal.json"
            MD_JSON="$COMP5/rank${RANK}_li${LI}_md.json"
            if [ -f "$ANN_JSON" ]; then
                E=$(python3 -c "import json; r=json.load(open('$ANN_JSON')); print(f'{r[\"E_after\"]:.3f}')" 2>/dev/null)
                ROW="$ROW  ${G}[✓ $E]${N}"
                TOTAL_DONE=$((TOTAL_DONE+1))
            elif [ -f "$MD_JSON" ]; then
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

    # anneal_chain.log
    AC_LOG="$COMP5/anneal_chain.log"
    if [ -f "$AC_LOG" ]; then
        AGE_S=$(( $(date +%s) - $(stat -c%Y "$AC_LOG") ))
        if [ $AGE_S -gt 600 ]; then AGE_C=$Y; else AGE_C=$G; fi
        echo -e "  anneal_chain.log: ${AGE_C}${AGE_S}s ago${N}"
        echo "    last 3 lines:"
        tail -3 "$AC_LOG" | sed 's/^/      /'
    fi
fi

echo -e "\n${B}════════════════════════════════════════════════════════════════════════${N}"
echo -e "${D}comp3 EOS: paper protocol K=2x2x1 (gen_dft_eos_comp4.py mirror)${N}"
echo -e "${D}comp5 anneal: champion = lowest E_after across all (rank,li) pairs${N}"
