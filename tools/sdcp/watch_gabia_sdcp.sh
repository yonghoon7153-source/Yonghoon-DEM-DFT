#!/bin/bash
# watch_gabia_sdcp.sh — gabia (kserver116-27) live status for the CURRENT work:
#   p0 DFT barrier + SDCP clean-slab rebuild (Phase-A re-rank -> Phase-B DFT+U).
# Finished items (Li3N UMA RC, LiC6) intentionally dropped. p0 shown via
# tmux capture-pane (no path guessing). Install: overwrite /root/watch_li3n.sh
# with this, then  watch -n 30 /root/watch_li3n.sh
echo "════════ $(date '+%m-%d %H:%M:%S')  gabia — SDCP clean rebuild + p0 ════════"

echo "■ P0 DFT barrier (Li3N, tmux:p0)  dft_p0/{min,saddle}"
D=/data/work/runs/li3n_pes_uma/dft_p0
Emin=""; Esad=""
for J in p0_min p0_saddle; do
    O=$D/$J.out
    if [ ! -f "$O" ]; then echo "   $J: 대기 (.out 없음)"; continue; fi
    E=$(grep '^!' "$O" 2>/dev/null | tail -1 | awk '{print $5}')
    if grep -q "JOB DONE" "$O" 2>/dev/null; then
        conv="?"; grep -q "bfgs converged" "$O" && conv="수렴"
        grep -q "maximum number" "$O" && conv="MAXSTEP"
        echo "   $J: ✅ JOB DONE ($conv)  E=${E:-–} Ry"
    else
        st=$(grep "number of bfgs steps" "$O" 2>/dev/null | tail -1 | awk '{print $NF}')
        fo=$(grep "Total force" "$O" 2>/dev/null | tail -1 | awk '{print $4}')
        sc=$(grep "estimated scf accuracy" "$O" 2>/dev/null | tail -1 | awk '{print $(NF-1)}')
        age=$(( $(date +%s) - $(stat -c %Y "$O" 2>/dev/null || date +%s) ))
        echo "   $J: 진행  ionic≈${st:-0} | force ${fo:-–} | scf ${sc:-–} Ry | E ${E:-–} Ry (${age}s前)"
    fi
    [ "$J" = "p0_min" ] && Emin=$E || Esad=$E
done
if [ -n "$Emin" ] && [ -n "$Esad" ] && grep -q "JOB DONE" "$D/p0_min.out" 2>/dev/null \
   && grep -q "JOB DONE" "$D/p0_saddle.out" 2>/dev/null; then
    awk -v a="$Emin" -v b="$Esad" 'BEGIN{printf "   ★ DFT BARRIER = (E_saddle-E_min) = %.3f eV\n",(b-a)*13.605693}'
fi
tmux has-session -t p0 2>/dev/null && echo "   [tmux:p0 실행중]" || echo "   [tmux:p0 없음]"

echo "■ SDCP Phase-A CLEAN 재랭킹 (tmux:phaseAc)  슬랩 전체 고정, v7c"
PA=/data/work/runs/sdcp_linio2_binding/phaseA_v7c_clean.log
if [ -f "$PA" ]; then
    grep -E "eV|ranking|saved" "$PA" 2>/dev/null | tail -12 | sed 's/^/   /'
else
    echo "   로그 대기 (phaseAc 미시작)"
fi
if tmux has-session -t phaseAc 2>/dev/null; then
    echo "   [phaseAc 실행중]"
else
    echo "   [phaseAc 종료 — 위에 ranking 있으면 완료]"
fi

echo "■ SDCP Phase-B DFT+U (tmux:phaseB)"
PB=/data/work/runs/sdcp_linio2_binding/phaseB_v7c
if [ -f "$PB/run.log" ]; then
    tail -3 "$PB/run.log" 2>/dev/null | sed 's/^/   /'
    n=$(grep -l "JOB DONE" $PB/*/scf.out 2>/dev/null | wc -l)
    echo "   완료 SCF: ${n:-0}/5"
else
    echo "   미시작 (phaseAc 챔피언 확정 후 발사)"
fi

echo "■ GPU"
nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader 2>/dev/null \
    | sed 's/^/   /'
