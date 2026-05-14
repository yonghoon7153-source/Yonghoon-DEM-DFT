#!/bin/bash
# kisti_monitor_v0_relax.sh -- detailed monitor for comp3 + comp5 V0 tight relax
#   GPU0: comp3 v2 V0 relax  (pipeline_v2/comp3_lpscbr/dft_eos/v0_fit/relax_v0/)
#   GPU1: comp5 v2 V0 relax  (pipeline_v2/comp5_lpscbr/dft_eos/v0_fit/relax_v0/)
#
# Usage:  watch -n 30 -c ./kisti_monitor_v0_relax.sh

C3=/scratch/x3430a02/kgy/manuscript_support/pipeline_v2/comp3_lpscbr/dft_eos/v0_fit
C5=/scratch/x3430a02/kgy/manuscript_support/pipeline_v2/comp5_lpscbr/dft_eos/v0_fit

B="\033[1m"; G="\033[1;32m"; Y="\033[1;33m"; R="\033[1;31m"
C="\033[1;36m"; D="\033[2m"; N="\033[0m"

echo -e "${B}════════════════════════════════════════════════════════════════════════"
echo -e "  KISTI: comp3 v2 V0 tight relax (GPU0) + comp5 v2 V0 (GPU1)"
echo -e "  $(date '+%Y-%m-%d %H:%M:%S')"
echo -e "════════════════════════════════════════════════════════════════════════${N}"

# ─── GPU ───
echo -e "\n${C}── GPU ──${N}"
nvidia-smi --query-gpu=index,temperature.gpu,utilization.gpu,memory.used,memory.total \
           --format=csv,noheader,nounits 2>/dev/null | \
  awk -F', ' '{ printf "  GPU%s  T=%s°C  Util=%3s%%  Mem=%6s/%6s MB\n", $1,$2,$3,$4,$5 }'

# ─── Processes ───
echo -e "\n${C}── pw.x processes ──${N}"
PS_OUT=$(ps -ef | grep -E "run_v0_relax|pw\.x" | grep -v grep | grep -v monitor)
if [ -z "$PS_OUT" ]; then
    echo -e "  ${R}NO V0 relax processes running${N}"
else
    echo "$PS_OUT" | awk '{
        cmd=""; for(i=8;i<=NF;i++) cmd=cmd" "$i;
        if (length(cmd) > 70) cmd = substr(cmd, 1, 67) "...";
        printf "  PID %7s start=%-5s CPU=%-9s %s\n", $2,$5,$7,cmd
    }'
fi

# ─── Function: detail per comp ───
show_v0() {
    local LABEL=$1
    local DIR=$2
    local GPU=$3

    echo -e "\n${B}══ $LABEL V0 tight relax (GPU$GPU) ══${N}"

    if [ ! -d "$DIR/relax_v0" ]; then
        echo -e "  ${R}relax_v0/ not found at $DIR${N}"
        return
    fi

    local OUT="$DIR/relax_v0/relax.out"
    local LOG="$DIR/v0_relax.log"

    if [ ! -f "$OUT" ]; then
        echo -e "  ${R}relax.out not found${N}"
        return
    fi

    # file age
    local AGE=$(($(date +%s) - $(stat -c %Y "$OUT")))
    local AGE_LBL="${AGE}s ago"
    if [ $AGE -lt 60 ];   then COLOR=$G
    elif [ $AGE -lt 600 ]; then COLOR=$Y
    else                       COLOR=$R; fi
    echo -e "  relax.out last update: ${COLOR}${AGE_LBL}${N}"

    # JOB DONE?
    if grep -qa "JOB DONE" "$OUT" 2>/dev/null; then
        echo -e "  ${G}✓ JOB DONE${N}"
        local EN=$(grep -a "!.*total energy" "$OUT" | tail -1 | awk '{print $5,$6}')
        echo -e "  ${G}final E = $EN${N}"
    fi

    # BFGS converged?
    if grep -qa "bfgs converged" "$OUT" 2>/dev/null; then
        echo -e "  ${G}✓ BFGS CONVERGED${N}"
    fi

    # iter count
    local N_SCF=$(grep -ca "^     iteration #" "$OUT" 2>/dev/null)
    # BFGS step count - QE prints "number of bfgs steps    =  N"
    local N_BFGS=$(grep -a "number of bfgs steps" "$OUT" 2>/dev/null | tail -1 | awk '{print $NF}')
    [ -z "$N_BFGS" ] && N_BFGS=0
    # ATOMIC_POSITIONS blocks = actual atom moves since restart
    local N_MOVES=$(grep -ca "^ATOMIC_POSITIONS" "$OUT" 2>/dev/null)
    # Total force evaluations (= one per SCF cycle = one per BFGS step)
    local N_FORCE=$(grep -ca "Total force" "$OUT" 2>/dev/null)
    echo -e "  SCF iter total   : $N_SCF"
    echo -e "  ${C}BFGS step (cumulative): $N_BFGS${N}    (atom moves this run: $N_MOVES,  SCF cycles: $N_FORCE)"

    # latest force
    local FORCE=$(grep -a "Total force" "$OUT" | tail -1 | awk '{print $4}')
    [ -n "$FORCE" ] && echo -e "  latest Total force = $FORCE  (target 1e-4)"

    # latest few ! total energy values (energy trajectory across BFGS steps)
    echo -e "  ${D}Last 5 ! total energy:${N}"
    grep -a "^!" "$OUT" 2>/dev/null | tail -5 | awk '{print "    " $0}'

    # latest BFGS energy
    local NEW_E=$(grep -aE "energy.*new" "$OUT" | tail -1)
    [ -n "$NEW_E" ] && echo -e "  $NEW_E"

    # latest 5 SCF accuracy
    echo -e "  ${D}Last 5 SCF accuracy:${N}"
    grep -a "estimated scf accuracy" "$OUT" 2>/dev/null | tail -5 | awk '{print "    " $0}'

    # latest log line
    if [ -f "$LOG" ]; then
        echo -e "  v0_relax.log last 2 lines:"
        tail -2 "$LOG" | awk '{print "    " $0}'
    fi

    # CRASH file?
    [ -f "$DIR/../../CRASH" ] && echo -e "  ${R}⚠ CRASH file present${N}"
}

show_v0 "comp3" "$C3" "0"
show_v0 "comp5" "$C5" "1"

echo ""
