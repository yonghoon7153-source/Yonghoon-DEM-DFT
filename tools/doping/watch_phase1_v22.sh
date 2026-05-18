#!/usr/bin/env bash
# watch_phase1_v22.sh — 22-compound multi-category batch dashboard
#
# Usage:
#   watch -n 30 'bash tools/doping/watch_phase1_v22.sh'
#
# Shows:
#   ▸ Overall progress (X/22 compounds done, Y/12 Phase 1A, Z/10 Phase 1B)
#   ▸ Current compound + stage
#   ▸ Per-compound status (Phase 1A 12 + Phase 1B 10)
#   ▸ Recent log tail
#   ▸ GPU utilization
#   ▸ ETA estimation
#
# Env: BATCH_DIR can override default path
BATCH_DIR="${BATCH_DIR:-/data/work/runs/multi_category_2026_05_19_v22}"

# 22-compound ordered list (Phase 1A oxide → 1B halide)
PHASE_1A=(Li2O MgO CaO ZnO Al2O3 Y2O3 La2O3 Nd2O3 Sm2O3 SiO2 ZrO2 TiO2)
PHASE_1B=(LiF MgF2 AlF3 AlCl3 ZrCl4 LiBr Li2S Li3N LiCl_rich LiBr_rich)
ALL_COMPOUNDS=("${PHASE_1A[@]}" "${PHASE_1B[@]}")

# Stage labels (18+ stages)
STAGES=(00_preflight 01_substitute 02_screen 03_winners 04_anneal 05_bvse
        06_rerank 07_eos 08_elastic 09a_combine 09b_collect 09c_train_predictor
        09d_dft_inputs 09e_ehull 09f_esw 10_md_sigma 11_cathode_interface
        12_collect_final 12b_train_final)
N_STAGES=${#STAGES[@]}

# Color helpers (terminal-safe)
GRN=$'\e[32m'
YLW=$'\e[33m'
RED=$'\e[31m'
CYA=$'\e[36m'
DIM=$'\e[2m'
RST=$'\e[0m'
BLD=$'\e[1m'

clear_line() { printf "%-70s" "$1"; }

# Header
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║  ${BLD}Multi-Category Batch v22 — Phase 1 dashboard${RST}                          ║"
echo "║  ${DIM}$(date +'%Y-%m-%d %H:%M:%S')  ($BATCH_DIR)${RST}      ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"

# ───── Section 1: Overall progress ───────────────────────────────────────
declare -i n_done_1a=0 n_done_1b=0 n_running=0
current_cmp=""
current_stage=""

for cmp in "${PHASE_1A[@]}"; do
    cmp_dir="$BATCH_DIR/$cmp"
    if [ -f "$cmp_dir/STAGE_12b.DONE" ] || [ -f "$cmp_dir/STAGE_12.DONE" ]; then
        n_done_1a=$((n_done_1a + 1))
    elif [ -d "$cmp_dir" ]; then
        # 진행 중 — 마지막 STAGE_*.DONE 찾기
        last=$(ls -t "$cmp_dir"/STAGE_*.DONE 2>/dev/null | head -1 | xargs basename 2>/dev/null | cut -d. -f1)
        [ -n "$last" ] && current_cmp="$cmp" && current_stage="$last" && n_running=1
    fi
done

for cmp in "${PHASE_1B[@]}"; do
    cmp_dir="$BATCH_DIR/$cmp"
    if [ -f "$cmp_dir/STAGE_12b.DONE" ] || [ -f "$cmp_dir/STAGE_12.DONE" ]; then
        n_done_1b=$((n_done_1b + 1))
    elif [ -d "$cmp_dir" ]; then
        last=$(ls -t "$cmp_dir"/STAGE_*.DONE 2>/dev/null | head -1 | xargs basename 2>/dev/null | cut -d. -f1)
        [ -n "$last" ] && current_cmp="$cmp" && current_stage="$last" && n_running=1
    fi
done

n_done_total=$((n_done_1a + n_done_1b))
pct_total=$((n_done_total * 100 / 22))

echo ""
echo "▸ Overall progress"
printf "  Phase 1A (oxides):     %s%d/12%s  " "$GRN" "$n_done_1a" "$RST"
# Mini progress bar
bar_1a=""
for i in $(seq 1 12); do
    [ $i -le $n_done_1a ] && bar_1a+="█" || bar_1a+="·"
done
printf "[%s]\n" "$bar_1a"

printf "  Phase 1B (halide+):    %s%d/10%s  " "$GRN" "$n_done_1b" "$RST"
bar_1b=""
for i in $(seq 1 10); do
    [ $i -le $n_done_1b ] && bar_1b+="█" || bar_1b+="·"
done
printf "[%s]\n" "$bar_1b"

printf "  ${BLD}Total:                 %s%d/22%s (%d%%)${RST}\n\n" "$GRN" "$n_done_total" "$RST" "$pct_total"

# ───── Section 2: Current cascade (if running) ───────────────────────────
if [ -n "$current_cmp" ]; then
    echo "▸ Currently active: ${CYA}${BLD}$current_cmp${RST} → last DONE = $current_stage"

    # Determine which stage is in progress (the NEXT one after last DONE)
    last_idx=-1
    for i in "${!STAGES[@]}"; do
        if [ "STAGE_${STAGES[$i]}" = "STAGE_${current_stage}" ] || \
           [ "STAGE_${STAGES[$i]%%_*}" = "STAGE_${current_stage}" ]; then
            last_idx=$i; break
        fi
    done

    # Per-stage marker for active compound
    cmp_dir="$BATCH_DIR/$current_cmp"
    printf "  Stage chain: "
    for s in "${STAGES[@]}"; do
        marker_name="STAGE_${s%%_*}.DONE"
        # try both label patterns
        if ls "$cmp_dir/$marker_name" >/dev/null 2>&1 || \
           ls "$cmp_dir"/STAGE_*"${s%%_*}"*.DONE >/dev/null 2>&1; then
            printf "${GRN}●${RST}"
        else
            printf "${DIM}○${RST}"
        fi
    done
    echo ""
    echo ""
else
    if [ "$n_done_total" -eq 22 ]; then
        echo "${GRN}▸ ALL 22 COMPOUNDS COMPLETE ✓${RST}"
        echo ""
    else
        echo "${YLW}▸ No active cascade detected${RST}"
        echo ""
    fi
fi

# ───── Section 3: Per-compound status table ──────────────────────────────
echo "▸ Per-compound status"
echo ""
echo "  ${BLD}Phase 1A — Oxides${RST}"
for i in "${!PHASE_1A[@]}"; do
    cmp="${PHASE_1A[$i]}"
    step_num=$((i + 1))
    cmp_dir="$BATCH_DIR/$cmp"
    if [ -f "$cmp_dir/STAGE_12b.DONE" ] || [ -f "$cmp_dir/STAGE_12.DONE" ]; then
        status="${GRN}✓ DONE${RST}"
        last=""
        # σ_Li 결과 1줄 (3 winners 평균)
        sig_file="$cmp_dir/10_md_sigma/sigma_md_summary.json"
        if [ -f "$sig_file" ]; then
            sig_info=$(python3 -c "
import json
d = json.load(open('$sig_file'))
recs = d.get('records', [])
if recs:
    sigmas = [r.get('arrhenius', {}).get('sigma_300K_S_cm_NE', 0) * 1000 for r in recs]
    sigmas = [s for s in sigmas if s > 0]
    if sigmas:
        print(f'σ={max(sigmas):.2f}/{min(sigmas):.2f} mS/cm (n={len(sigmas)})')
" 2>/dev/null)
            [ -n "$sig_info" ] && last="$sig_info"
        fi
    elif [ -d "$cmp_dir" ]; then
        last_stage=$(ls -t "$cmp_dir"/STAGE_*.DONE 2>/dev/null | head -1 | xargs basename 2>/dev/null | cut -d. -f1)
        if [ -n "$last_stage" ]; then
            status="${YLW}⟲ $last_stage${RST}"
        else
            status="${YLW}⟲ starting${RST}"
        fi
        last=""
    else
        status="${DIM}─ pending${RST}"
        last=""
    fi
    printf "    %2d. %-12s %-25s %s\n" "$step_num" "$cmp" "$status" "$last"
done

echo ""
echo "  ${BLD}Phase 1B — Halide/Sulfide/Nitride/Halide-rich${RST}"
for i in "${!PHASE_1B[@]}"; do
    cmp="${PHASE_1B[$i]}"
    step_num=$((i + 13))
    cmp_dir="$BATCH_DIR/$cmp"
    if [ -f "$cmp_dir/STAGE_12b.DONE" ] || [ -f "$cmp_dir/STAGE_12.DONE" ]; then
        status="${GRN}✓ DONE${RST}"
        last=""
        sig_file="$cmp_dir/10_md_sigma/sigma_md_summary.json"
        if [ -f "$sig_file" ]; then
            sig_info=$(python3 -c "
import json
d = json.load(open('$sig_file'))
recs = d.get('records', [])
if recs:
    sigmas = [r.get('arrhenius', {}).get('sigma_300K_S_cm_NE', 0) * 1000 for r in recs]
    sigmas = [s for s in sigmas if s > 0]
    if sigmas:
        print(f'σ={max(sigmas):.2f}/{min(sigmas):.2f} mS/cm (n={len(sigmas)})')
" 2>/dev/null)
            [ -n "$sig_info" ] && last="$sig_info"
        fi
    elif [ -d "$cmp_dir" ]; then
        last_stage=$(ls -t "$cmp_dir"/STAGE_*.DONE 2>/dev/null | head -1 | xargs basename 2>/dev/null | cut -d. -f1)
        if [ -n "$last_stage" ]; then
            status="${YLW}⟲ $last_stage${RST}"
        else
            status="${YLW}⟲ starting${RST}"
        fi
        last=""
    else
        status="${DIM}─ pending${RST}"
        last=""
    fi
    chem_watch=""
    case "$cmp" in
        AlCl3|ZrCl4|Li3N) chem_watch="${RED}⚠${RST}" ;;
    esac
    printf "    %2d. %-12s %-25s %s %s\n" "$step_num" "$cmp" "$status" "$last" "$chem_watch"
done
echo ""

# ───── Section 4: GPU status ─────────────────────────────────────────────
echo "▸ GPU"
nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total,temperature.gpu \
           --format=csv,noheader 2>/dev/null \
  | awk -F, '{printf "  GPU%s%s: util=%-4s mem=%-12s T=%-4s\n", $1, $2, $3, $4"/"$5, $6}'
echo ""

# ───── Section 5: Active python processes ────────────────────────────────
echo "▸ Active processes (doping)"
ps -eo pid,etime,pcpu,pmem,cmd 2>/dev/null \
  | grep -E "(run_uma_screening|run_anneal|run_mlip_postproc|run_md_sigma|run_cathode_interface|tier_cascade|preflight|substitute_compound)" \
  | grep -v grep \
  | head -5 \
  | awk '{printf "  %s  etime=%-12s cpu=%5s%%  %s\n", $1, $2, $3, $5}'
echo ""

# ───── Section 6: Recent log tail (current compound) ─────────────────────
if [ -n "$current_cmp" ]; then
    log_file="$BATCH_DIR/$current_cmp.log"
    if [ -f "$log_file" ]; then
        echo "▸ Recent log ($current_cmp.log, last 6 lines)"
        tail -6 "$log_file" 2>/dev/null | sed 's/^/  /' | head -6
        echo ""
    fi
fi

# ───── Section 7: ETA estimation ─────────────────────────────────────────
if [ "$n_done_total" -gt 0 ] && [ "$n_done_total" -lt 22 ]; then
    # 첫 compound 시작 시간 추정 (가장 오래된 STAGE_00.DONE)
    first_start=$(find "$BATCH_DIR" -name "STAGE_00.DONE" -printf "%T@\n" 2>/dev/null | sort -n | head -1)
    if [ -n "$first_start" ]; then
        now=$(date +%s)
        elapsed=$(awk "BEGIN {print $now - $first_start}")
        elapsed_h=$(awk "BEGIN {printf \"%.1f\", $elapsed / 3600}")
        per_cmp_h=$(awk "BEGIN {printf \"%.1f\", $elapsed / 3600 / $n_done_total}")
        remaining_cmp=$((22 - n_done_total))
        eta_h=$(awk "BEGIN {printf \"%.1f\", $per_cmp_h * $remaining_cmp}")
        eta_d=$(awk "BEGIN {printf \"%.1f\", $eta_h / 24}")
        echo "▸ ETA"
        echo "  Elapsed:     ${elapsed_h}h ($n_done_total compounds done)"
        echo "  Per-cmp avg: ${per_cmp_h}h"
        echo "  Remaining:   $remaining_cmp compounds × ${per_cmp_h}h = ${eta_h}h (~${eta_d} days)"
    fi
    echo ""
fi

# ───── Section 8: Disk usage ─────────────────────────────────────────────
if [ -d "$BATCH_DIR" ]; then
    size=$(du -sh "$BATCH_DIR" 2>/dev/null | cut -f1)
    echo "▸ Disk: $BATCH_DIR  ($size)"
fi

echo ""
echo "${DIM}  Refresh: watch -n 30 'bash tools/doping/watch_phase1_v22.sh'${RST}"
echo "${DIM}  Stop: Ctrl+C${RST}"
