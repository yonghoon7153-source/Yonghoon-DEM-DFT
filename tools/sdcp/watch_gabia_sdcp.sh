#!/bin/bash
# watch_gabia_sdcp.sh — gabia (kserver116-27) live status: p0 DFT barrier +
# SDCP Phase-B DFT+U (per-SCF detail + auto E_bind verdict). Phase-A dropped
# (done; ranking is in db/properties/sdcp_linio2_binding_phaseA.csv). p0 shown
# via the dft_p0 .out files. Install: overwrite /root/watch_li3n.sh, then
#   watch -n 30 /root/watch_li3n.sh
RY=13.605693
echo "════════ $(date '+%m-%d %H:%M:%S')  gabia — Phase-B DFT+U + p0 ════════"

# ── p0 DFT barrier ──
echo "■ P0 DFT barrier (Li3N, tmux:p0)  dft_p0/{min,saddle}"
D=/data/work/runs/li3n_pes_uma/dft_p0
Emin=""; Esad=""
for J in p0_min p0_saddle; do
    O=$D/$J.out
    if [ ! -f "$O" ]; then echo "   $J: 대기 (.out 없음)"; continue; fi
    E=$(grep '^!' "$O" 2>/dev/null | tail -1 | awk '{print $5}')
    if grep -q "JOB DONE" "$O" 2>/dev/null; then
        conv="?"; grep -q "bfgs converged" "$O" && conv="수렴"; grep -q "maximum number" "$O" && conv="MAXSTEP"
        echo "   $J: ✅ JOB DONE ($conv)  E=${E:-–} Ry"
    else
        st=$(grep "number of bfgs steps" "$O" 2>/dev/null | tail -1 | awk '{print $NF}')
        fo=$(grep "Total force" "$O" 2>/dev/null | tail -1 | awk '{print $4}')
        sc=$(grep "estimated scf accuracy" "$O" 2>/dev/null | tail -1 | awk '{print $(NF-1)}')
        age=$(( $(date +%s) - $(stat -c %Y "$O" 2>/dev/null || date +%s) ))
        echo "   $J: 진행  ionic≈${st:-0} | force ${fo:-–} | scf ${sc:-–} Ry (${age}s前)"
    fi
    [ "$J" = "p0_min" ] && Emin=$E || Esad=$E
done
if [ -n "$Emin" ] && [ -n "$Esad" ] && grep -q "JOB DONE" "$D/p0_min.out" 2>/dev/null \
   && grep -q "JOB DONE" "$D/p0_saddle.out" 2>/dev/null; then
    awk -v a="$Emin" -v b="$Esad" -v r=$RY 'BEGIN{printf "   ★ DFT BARRIER = %.3f eV\n",(b-a)*r}'
fi
tmux has-session -t p0 2>/dev/null && echo "   [tmux:p0 실행중]" || echo "   [tmux:p0 없음]"

# ── SDCP Phase-B DFT+U (per-SCF) ──
echo "■ SDCP Phase-B DFT+U (tmux:phaseB)  doped_chelation_r90 vs neutral_chelation_r0"
PB=/data/work/runs/sdcp_linio2_binding/phaseB_v7c
declare -A EN
done=0
now=$(date +%s)
for j in slab complex_doped complex_neutral mol_doped mol_neutral; do
    f=$PB/$j/scf.out
    if [ ! -f "$f" ]; then printf "   %-16s ⬚ 대기\n" "$j"; continue; fi
    if grep -q "JOB DONE" "$f" 2>/dev/null; then
        e=$(grep '^!' "$f" 2>/dev/null | tail -1 | awk '{print $5}')
        cv=""; grep -q "convergence has been achieved" "$f" && cv="✓수렴"
        printf "   %-16s ✅ DONE %s  E=%s Ry\n" "$j" "$cv" "${e:-–}"
        EN[$j]=$e; done=$((done+1))
    elif grep -qiE "out of memory|cuMemAlloc|%%%%%%" "$f" 2>/dev/null; then
        printf "   %-16s ✗ OOM/에러 (톱업 재실행 필요)\n" "$j"
    else
        it=$(grep -c "iteration #" "$f" 2>/dev/null)
        ac=$(grep "estimated scf accuracy" "$f" 2>/dev/null | tail -1 | awk '{print $(NF-1)}')
        age=$(( now - $(stat -c %Y "$f" 2>/dev/null || echo "$now") ))
        printf "   %-16s ⏳ scf-iter %s | acc %s Ry (%ds前)\n" "$j" "${it:-0}" "${ac:-–}" "$age"
    fi
done
echo "   ───  완료 $done/5  ───"
if [ "$done" -eq 5 ]; then
    awk -v s="${EN[slab]:-0}" -v cd="${EN[complex_doped]:-0}" -v cn="${EN[complex_neutral]:-0}" \
        -v md="${EN[mol_doped]:-0}" -v mn="${EN[mol_neutral]:-0}" -v r=$RY 'BEGIN{
        bd=(cd-s-md)*r; bn=(cn-s-mn)*r;
        printf "   ★ E_bind  doped %.3f  |  neutral %.3f  eV\n", bd, bn;
        printf "   ★ VERDICT  Δ(doped-neutral) = %.3f eV  (%s)\n", bd-bn, (bd-bn<0?"도핑이 결합 강화":"강화 아님")}'
fi
if [ -f "$PB/run.log" ]; then tail -2 "$PB/run.log" 2>/dev/null | sed 's/^/   · /'; fi

# ── GPU ──
echo "■ GPU"
nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader 2>/dev/null | sed 's/^/   /'
