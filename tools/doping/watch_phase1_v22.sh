#!/usr/bin/env bash
# watch_phase1_v22.sh — 95-compound multi-category batch dashboard
#
# Usage (self-looping, scrollable):
#   bash tools/doping/watch_phase1_v22.sh             # 30s interval, infinite loop
#   bash tools/doping/watch_phase1_v22.sh --once      # single snapshot
#   INTERVAL=60 bash tools/doping/watch_phase1_v22.sh # 60s interval
#
# Stop: Ctrl+C
# Note: Terminal output is preserved (scrollable). Use `tmux` or `screen`
#       for long-running monitoring sessions.

BATCH_DIR="${BATCH_DIR:-/data/work/runs/multi_category_2026_05_19_v22}"
INTERVAL="${INTERVAL:-30}"
MODE="loop"
[ "${1:-}" = "--once" ] && MODE="once"

# ============================================================
# Display function (called once per iteration)
# ============================================================
render_dashboard() {

# Phase 1A — 37 oxides
PHASE_1A=(
    Li2O Na2O Cu2O Ag2O
    MgO ZnO CaO SrO BaO MnO CoO NiO
    Al2O3 Sc2O3 Y2O3 La2O3 Nd2O3 Sm2O3 Gd2O3 Ga2O3 In2O3 Cr2O3 Fe2O3 B2O3
    SiO2 GeO2 SnO2 TiO2 ZrO2 HfO2
    V2O5 Nb2O5 Ta2O5 Sb2O5
    CrO3 MoO3 WO3
)

# Phase 1B — 64 non-oxides
PHASE_1B=(
    LiF MgF2 CaF2 AlF3 YF3 LaF3 NdF3 ZrF4 TiF4 ScF3
    LiCl MgCl2 CaCl2 SrCl2 BaCl2 AlCl3 GaCl3 FeCl3 CrCl3
    YCl3 LaCl3 NdCl3 SmCl3 ScCl3 ZrCl4 HfCl4 TiCl4 NbCl5 TaCl5
    LiBr MgBr2 CaBr2 AlBr3 ZrBr4
    LiI NaI MgI2 AlI3
    Li3N Mg3N2 Ca3N2 AlN GaN
    Li2S Na2S MgS CaS Al2S3 Ga2S3 SiS2 GeS2 SnS2 As2S3 Sb2S3
)

# Tier D
TIER_D=(Cl_rich Br_rich I_rich F_rich)

N_1A=${#PHASE_1A[@]}
N_1B=${#PHASE_1B[@]}
N_D=${#TIER_D[@]}
N_TOTAL=$((N_1A + N_1B + N_D))

# Colors
GRN=$'\e[32m'
YLW=$'\e[33m'
RED=$'\e[31m'
CYA=$'\e[36m'
DIM=$'\e[2m'
RST=$'\e[0m'
BLD=$'\e[1m'

# Header
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║  ${BLD}Multi-Category Batch v105 — Phase 1 dashboard${RST}                         ║"
echo "║  ${DIM}$(date +'%Y-%m-%d %H:%M:%S')  ($BATCH_DIR)${RST}     ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"

# ───── Section 1: Overall progress ────────────────────────────────────
declare -i n_1a=0 n_1b=0 n_d=0
current_cmp=""

for cmp in "${PHASE_1A[@]}"; do
    cmp_dir="$BATCH_DIR/$cmp"
    if [ -f "$cmp_dir/STAGE_12b.DONE" ] || [ -f "$cmp_dir/STAGE_12.DONE" ]; then
        n_1a=$((n_1a + 1))
    elif [ -d "$cmp_dir" ]; then
        last=$(ls -t "$cmp_dir"/STAGE_*.DONE 2>/dev/null | head -1 | xargs basename 2>/dev/null | cut -d. -f1)
        [ -n "$last" ] && current_cmp="$cmp:$last"
    fi
done
for cmp in "${PHASE_1B[@]}"; do
    cmp_dir="$BATCH_DIR/$cmp"
    if [ -f "$cmp_dir/STAGE_12b.DONE" ] || [ -f "$cmp_dir/STAGE_12.DONE" ]; then
        n_1b=$((n_1b + 1))
    elif [ -d "$cmp_dir" ]; then
        last=$(ls -t "$cmp_dir"/STAGE_*.DONE 2>/dev/null | head -1 | xargs basename 2>/dev/null | cut -d. -f1)
        [ -n "$last" ] && current_cmp="$cmp:$last"
    fi
done
for hal in "${TIER_D[@]}"; do
    if [ -f "$BATCH_DIR/$hal/STAGE_12b.DONE" ] || [ -f "$BATCH_DIR/$hal/STAGE_12.DONE" ]; then
        n_d=$((n_d + 1))
    fi
done

n_done=$((n_1a + n_1b + n_d))
pct=$((n_done * 100 / N_TOTAL))

echo ""
echo "▸ Overall progress (105-compound v22 batch)"
printf "  Phase 1A (oxides):           %s%3d/%-3d%s  " "$GRN" "$n_1a" "$N_1A" "$RST"
bar=""; max_show=37
for i in $(seq 1 $max_show); do
    [ $i -le $n_1a ] && bar+="█" || bar+="·"
done
printf "[%s]\n" "$bar"

printf "  Phase 1B (halide+non-oxide): %s%3d/%-3d%s  " "$GRN" "$n_1b" "$N_1B" "$RST"
bar=""
for i in $(seq 1 64); do
    [ $i -le $n_1b ] && bar+="█" || bar+="·"
done
printf "[%s]\n" "$bar"

printf "  Tier D (halide-rich):        %s%3d/%-3d%s  [%s%s]\n" "$GRN" "$n_d" "$N_D" "$RST" \
    "$(printf '█%.0s' $(seq 1 $n_d))" "$(printf '·%.0s' $(seq 1 $((N_D - n_d))))"

printf "\n  ${BLD}Total: %s%d/%d%s (%d%%)${RST}\n\n" "$GRN" "$n_done" "$N_TOTAL" "$RST" "$pct"

# ───── Section 2: Currently active ────────────────────────────────────
if [ -n "$current_cmp" ]; then
    cmp_name="${current_cmp%%:*}"
    last_stage="${current_cmp##*:}"
    echo "▸ Currently active: ${CYA}${BLD}$cmp_name${RST} → last DONE = $last_stage"
fi
echo ""

# ───── Section 3: Recent activity (last 5 compounds with action) ──────
echo "▸ Recent activity (top 5 most recent)"
ls -t "$BATCH_DIR"/*/STAGE_*.DONE 2>/dev/null | head -5 | while read f; do
    cmp=$(basename $(dirname "$f"))
    stage=$(basename "$f" | sed 's/STAGE_//; s/.DONE//')
    mtime=$(stat -c "%y" "$f" 2>/dev/null | cut -d. -f1)
    echo "  $cmp / $stage  ($mtime)"
done
echo ""

# ───── Section 4: Per-tier progress ───────────────────────────────────
echo "▸ Phase 1A — Oxides (37)"
for i in "${!PHASE_1A[@]}"; do
    cmp="${PHASE_1A[$i]}"
    step=$((i + 1))
    cmp_dir="$BATCH_DIR/$cmp"
    if [ -f "$cmp_dir/STAGE_12b.DONE" ] || [ -f "$cmp_dir/STAGE_12.DONE" ]; then
        status="${GRN}✓${RST}"
    elif [ -d "$cmp_dir" ]; then
        last_stage=$(ls -t "$cmp_dir"/STAGE_*.DONE 2>/dev/null | head -1 | xargs basename 2>/dev/null | cut -d. -f1 | sed 's/STAGE_//')
        status="${YLW}⟲${last_stage}${RST}"
    else
        status="${DIM}·${RST}"
    fi
    # 6 columns per row
    if [ $((step % 6)) -eq 1 ]; then printf "  "; fi
    printf "%-3d.%-7s %-15s " "$step" "$cmp" "$status"
    if [ $((step % 6)) -eq 0 ]; then echo ""; fi
done
echo ""

echo "▸ Phase 1B — Halides+Sulfide+Nitride (64)"
for i in "${!PHASE_1B[@]}"; do
    cmp="${PHASE_1B[$i]}"
    step=$((i + N_1A + 1))
    cmp_dir="$BATCH_DIR/$cmp"
    if [ -f "$cmp_dir/STAGE_12b.DONE" ] || [ -f "$cmp_dir/STAGE_12.DONE" ]; then
        status="${GRN}✓${RST}"
    elif [ -d "$cmp_dir" ]; then
        last_stage=$(ls -t "$cmp_dir"/STAGE_*.DONE 2>/dev/null | head -1 | xargs basename 2>/dev/null | cut -d. -f1 | sed 's/STAGE_//')
        status="${YLW}⟲${last_stage}${RST}"
    else
        status="${DIM}·${RST}"
    fi
    if [ $((step % 6)) -eq $((N_1A % 6 + 1)) ]; then printf "  "; fi
    printf "%-3d.%-7s %-15s " "$step" "$cmp" "$status"
    if [ $((step % 6)) -eq $((N_1A % 6)) ]; then echo ""; fi
done
echo ""
echo ""

# ───── Section 5: GPU status ──────────────────────────────────────────
echo "▸ GPU"
nvidia-smi --query-gpu=index,utilization.gpu,memory.used,memory.total,temperature.gpu \
           --format=csv,noheader 2>/dev/null \
  | awk -F, '{printf "  GPU%s: util=%-5s mem=%-15s T=%-4s\n", $1, $2, $3"/"$4, $5}'
echo ""

# ───── Section 6: Active processes ────────────────────────────────────
echo "▸ Active python processes"
ps -eo pid,etime,pcpu,cmd 2>/dev/null \
  | grep -E "(run_uma|run_anneal|run_mlip|run_md_sigma|run_cathode|tier_cascade|substitute_compound)" \
  | grep -v grep \
  | head -5 \
  | awk '{printf "  PID %s  etime=%-10s CPU=%5s%%  %s\n", $1, $2, $3, $5}'
echo ""

# ───── Section 7: Current compound log ────────────────────────────────
if [ -n "$current_cmp" ]; then
    cmp_name="${current_cmp%%:*}"
    log_file="$BATCH_DIR/$cmp_name.log"
    if [ -f "$log_file" ]; then
        echo "▸ Recent log ($cmp_name.log, last 5 lines)"
        tail -5 "$log_file" 2>/dev/null | sed 's/^/  /'
        echo ""
    fi
fi

# ───── Section 8: ETA ──────────────────────────────────────────────────
if [ "$n_done" -gt 0 ] && [ "$n_done" -lt "$N_TOTAL" ]; then
    first_done_marker=$(find "$BATCH_DIR" -name "STAGE_12*.DONE" -printf "%T@\n" 2>/dev/null | sort -n | head -1)
    if [ -z "$first_done_marker" ]; then
        # 아직 1개도 완료 안 된 경우 — 첫 STAGE_00 사용
        first_done_marker=$(find "$BATCH_DIR" -name "STAGE_00.DONE" -printf "%T@\n" 2>/dev/null | sort -n | head -1)
    fi
    if [ -n "$first_done_marker" ]; then
        now=$(date +%s)
        elapsed=$(awk "BEGIN {print $now - $first_done_marker}")
        elapsed_h=$(awk "BEGIN {printf \"%.1f\", $elapsed / 3600}")
        if [ "$n_done" -gt 0 ]; then
            per_cmp_h=$(awk "BEGIN {printf \"%.1f\", $elapsed / 3600 / $n_done}")
            remaining=$((N_TOTAL - n_done))
            eta_h=$(awk "BEGIN {printf \"%.0f\", $per_cmp_h * $remaining}")
            eta_d=$(awk "BEGIN {printf \"%.1f\", $eta_h / 24}")
            echo "▸ ETA"
            echo "  Elapsed: ${elapsed_h}h ($n_done/$N_TOTAL done)"
            echo "  Avg per cmp: ${per_cmp_h}h"
            echo "  Remaining: $remaining cmps × ${per_cmp_h}h = ${eta_h}h (~${eta_d} days)"
        fi
        echo ""
    fi
fi

# ───── Section 9: Disk ────────────────────────────────────────────────
if [ -d "$BATCH_DIR" ]; then
    size=$(du -sh "$BATCH_DIR" 2>/dev/null | cut -f1)
    free=$(df -h "$BATCH_DIR" 2>/dev/null | awk 'NR==2 {print $4}')
    echo "▸ Disk: $BATCH_DIR  ($size used; $free free on volume)"
fi
echo "${DIM}  ── next refresh in ${INTERVAL}s (Ctrl+C to stop) ──${RST}"

}  # ← end of render_dashboard()

# ============================================================
# Main: either single snapshot or infinite loop
# ============================================================
if [ "$MODE" = "once" ]; then
    render_dashboard
else
    trap 'echo ""; echo "${DIM}Stopped at $(date +%T)${RST}"; exit 0' INT TERM
    iter=0
    while true; do
        iter=$((iter + 1))
        echo ""
        echo "════════════════════════════════════════════════════════════════════════════"
        echo "  Iteration #$iter  ($(date +'%Y-%m-%d %H:%M:%S'))"
        echo "════════════════════════════════════════════════════════════════════════════"
        render_dashboard
        sleep "$INTERVAL"
    done
fi
