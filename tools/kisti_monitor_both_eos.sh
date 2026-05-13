#!/bin/bash
# kisti_monitor_both_eos.sh — detailed monitor for:
#   GPU0: comp3 v2 DFT EOS (priority v103 → v102 → v104 → ...)
#   GPU1: comp5 v2 DFT EOS (priority v104 → v103 → v105 → ...)
#
# Usage: while true; do clear; ./kisti_monitor_both_eos.sh; sleep 30; done

COMP3=/scratch/x3430a02/kgy/manuscript_support/pipeline_v2/comp3_lpscbr
COMP5=/scratch/x3430a02/kgy/manuscript_support/pipeline_v2/comp5_lpscbr

B="\033[1m"; G="\033[1;32m"; Y="\033[1;33m"; R="\033[1;31m"; C="\033[1;36m"; D="\033[2m"; M="\033[35m"; N="\033[0m"

echo -e "${B}════════════════════════════════════════════════════════════════════════"
echo -e "  KISTI: comp3 v2 EOS (GPU0) + comp5 v2 EOS (GPU1) — priority 3-vol"
echo -e "  $(date '+%Y-%m-%d %H:%M:%S')"
echo -e "════════════════════════════════════════════════════════════════════════${N}"

# ============================================================
#  GPU + Process
# ============================================================
echo -e "\n${C}── GPU ──${N}"
nvidia-smi --query-gpu=index,name,temperature.gpu,utilization.gpu,memory.used,memory.total \
           --format=csv,noheader,nounits 2>/dev/null | \
  awk -F', ' '{ printf "  GPU%s %s  T=%s°C  Util=%3s%%  Mem=%5s/%5s MB\n", $1,$2,$3,$4,$5,$6 }'

echo -e "\n${C}── Processes ──${N}"
PS_OUT=$(ps -ef | grep -E "auto_restart|run_dft_eos|pw\.x|watchdog" | grep -v grep | grep -v monitor)
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
#  Per-comp EOS detail (function)
# ============================================================
show_comp_eos() {
    local LABEL=$1
    local BASE=$2
    local GPU=$3
    local PRIORITY=$4    # space-separated vol priority order

    echo -e "\n${B}══ $LABEL v2 DFT EOS (GPU$GPU) ══${N}"

    if [ ! -d "$BASE/dft_eos" ]; then
        echo -e "  ${R}dft_eos directory not found at $BASE${N}"
        return
    fi

    # Process priority order
    echo -e "  ${D}Priority order: $PRIORITY${N}"
    echo "  Vol status (in priority order):"

    local N_DONE=0
    local N_RUNNING_VOL=""
    local PRIORITY_DONE=0
    local PRIORITY_3_VOLS=$(echo $PRIORITY | awk '{print $1, $2, $3}')

    for v in $PRIORITY; do
        OUT="$BASE/dft_eos/v${v}/relax.out"
        IS_PRIORITY_3=0
        for p3 in $PRIORITY_3_VOLS; do
            [ "$v" = "$p3" ] && IS_PRIORITY_3=1
        done

        if [ -f "$OUT" ]; then
            if grep -qE "bfgs converged in|End of BFGS Geometry" "$OUT" 2>/dev/null; then
                E_RY=$(grep "!" "$OUT" | tail -1 | awk '{print $5}')
                E_EV=$(python3 -c "print(f'{float(\"$E_RY\")*13.6057:.4f}')" 2>/dev/null)
                WALL=$(grep "PWSCF.*WALL" "$OUT" | tail -1 | awk '{print $5}')
                MARK=""
                [ "$IS_PRIORITY_3" = "1" ] && { MARK=" ⭐"; PRIORITY_DONE=$((PRIORITY_DONE+1)); }
                echo -e "    ${G}[✓ v${v}]${N}  E=$E_RY Ry ($E_EV eV)  WALL=$WALL${MARK}"
                N_DONE=$((N_DONE+1))
            else
                ITER=$(grep -c "^     iteration #" "$OUT" 2>/dev/null)
                BFGS=$(grep -c "new energy" "$OUT" 2>/dev/null)
                LAST_ACC=$(grep "estimated scf accuracy" "$OUT" | tail -1 | awk '{print $NF}')
                LAST_FORCE=$(grep "Total force" "$OUT" | tail -1 | awk '{print $4}')
                SIZE=$(du -k "$OUT" | cut -f1)
                AGE_S=$(( $(date +%s) - $(stat -c%Y "$OUT") ))
                MARK=""
                [ "$IS_PRIORITY_3" = "1" ] && MARK=" ⭐"
                echo -e "    ${Y}[▶ v${v}]${N}  iter=$ITER bfgs=$BFGS acc=$LAST_ACC force=$LAST_FORCE  age=${AGE_S}s${MARK}"
                N_RUNNING_VOL="v${v}"
            fi
        else
            MARK=""
            [ "$IS_PRIORITY_3" = "1" ] && MARK=" ⭐"
            echo "    [ ] v${v}${MARK}"
        fi
    done

    echo -e "  ${B}Done: $N_DONE / 11${N}  (priority 3: ${G}${PRIORITY_DONE}/3${N})"

    # auto_restart.log
    AR_LOG="$BASE/auto_restart.log"
    if [ -f "$AR_LOG" ]; then
        AGE_S=$(( $(date +%s) - $(stat -c%Y "$AR_LOG") ))
        if [ $AGE_S -gt 600 ]; then AGE_C=$Y; else AGE_C=$G; fi
        echo -e "  auto_restart.log: ${AGE_C}${AGE_S}s ago${N}"
        echo "    last 2 lines:"
        tail -2 "$AR_LOG" | sed 's/^/      /'
    fi

    # run_dft_eos.log
    RDFT_LOG="$BASE/run_dft_eos.log"
    if [ -f "$RDFT_LOG" ]; then
        echo "    run_dft_eos.log last 3 lines:"
        tail -3 "$RDFT_LOG" | sed 's/^/      /'
    fi

    # Current running vol detail
    if [ -n "$N_RUNNING_VOL" ]; then
        OUT="$BASE/dft_eos/${N_RUNNING_VOL}/relax.out"
        echo -e "  ${C}Current ${N_RUNNING_VOL} detail:${N}"
        # Last SCF iter
        LAST_ITER_LINE=$(grep "^     iteration #" "$OUT" | tail -1 | tr -s ' ' | sed 's/^ //')
        [ -n "$LAST_ITER_LINE" ] && echo "    $LAST_ITER_LINE"
        # Current total energy + force
        LAST_TOTE=$(grep "total energy" "$OUT" | tail -1 | awk '{print $5}')
        LAST_FORCE=$(grep "Total force" "$OUT" | tail -1 | awk '{print $4}')
        [ -n "$LAST_TOTE" ] && echo "    E=$LAST_TOTE Ry,  Total force=$LAST_FORCE"
        # SCF accuracy progression (last 5)
        echo "    SCF accuracy (last 5):"
        grep "estimated scf accuracy" "$OUT" | tail -5 | awk '{print "      " $NF}'
        # Negative rho warning count
        NEG_RHO=$(grep -c "negative rho" "$OUT" 2>/dev/null)
        [ "$NEG_RHO" -gt 0 ] && echo -e "    ${Y}negative rho warnings: $NEG_RHO${N}"
    fi
}

# ============================================================
#  comp3
# ============================================================
show_comp_eos "comp3" "$COMP3" "0" "103 102 104 101 105 100 106 99 107 98 108"

# ============================================================
#  comp5
# ============================================================
show_comp_eos "comp5" "$COMP5" "1" "104 103 105 102 106 101 107 100 108 99 98"

# ============================================================
#  Summary / next steps
# ============================================================
echo -e "\n${B}════════════════════════════════════════════════════════════════════════${N}"
echo -e "${D}Priority 3 vols (⭐) center the EOS curve minimum (parabolic fit V0,B0)"
echo -e "After priority 3 done, remaining 8 vols complete the full BM3 fit"
echo -e "auto_restart.sh handles KISTI walltime kills (5-min watchdog, restart_mode='restart')${N}"
