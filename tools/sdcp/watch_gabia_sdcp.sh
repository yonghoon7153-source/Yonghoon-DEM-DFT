#!/bin/bash
# watch_gabia_sdcp.sh — gabia (kserver116-27) live status: p0 DFT barrier +
# SDCP Phase-B DFT+U (per-SCF detail + auto E_bind verdict). Phase-A dropped
# (done; ranking is in db/properties/sdcp_linio2_binding_phaseA.csv). p0 shown
# via the dft_p0 .out files. Install: overwrite /root/watch_li3n.sh, then
#   watch -n 30 /root/watch_li3n.sh
RY=13.605693
echo "════════ $(date '+%m-%d %H:%M:%S')  gabia — Phase-B DFT+U + p0 ════════"

# ── p0 DFT barrier ──
echo "■ P0 DFT barrier (Li3N)  min:gabia 완료 / min2→saddle:kgy(3090) 이관"
D=/data/work/runs/li3n_pes_uma/dft_p0
Emin=""; Emin2=""; Esad=""
Emin=$(grep '^!' $D/p0_min.out 2>/dev/null | tail -1 | awk '{print $5}')
[ -n "$Emin" ] && echo "   p0_min  : ✅ MAXSTEP 종료  E=$Emin Ry (미수렴 — min2로 연장 중, 참조용)"
if [ -f $D/p0_min2.out ]; then
    Emin2=$(grep '^!' $D/p0_min2.out | tail -1 | awk '{print $5}')
    if grep -q "JOB DONE" $D/p0_min2.out; then
        conv="?"; grep -q "bfgs converged" $D/p0_min2.out && conv="수렴"
        grep -q "maximum number" $D/p0_min2.out && conv="MAXSTEP"
        echo "   p0_min2 : ✅ JOB DONE ($conv)  E=$Emin2 Ry"
    else
        echo "   p0_min2 : (kgy 복사본 도착, 파싱)  E=${Emin2:-–}"
    fi
else
    echo "   p0_min2 : ⏳ kgy에서 진행 — 완료 out을 이 폴더로 복사하면 barrier 자동"
fi
if grep -q "JOB DONE" $D/p0_saddle.out 2>/dev/null; then
    Esad=$(grep '^!' $D/p0_saddle.out | tail -1 | awk '{print $5}')
    echo "   p0_saddle: ✅ JOB DONE  E=$Esad Ry"
else
    echo "   p0_saddle: ⏳ kgy에서 min2 뒤 자동 체인 (로컬 구 out 무시)"
fi
REF=${Emin2:-$Emin}
if [ -n "$REF" ] && [ -n "$Esad" ]; then
    awk -v a="$REF" -v b="$Esad" -v r=$RY -v m2="$Emin2" \
      'BEGIN{printf "   ★ DFT BARRIER = %.3f eV%s\n",(b-a)*r,(m2==""?" (min 미수렴 참조 — min2 대기)":"")}'
fi

# ── SDCP Phase-B DFT+U (per-SCF) ──
echo "■ SDCP Phase-B DFT+U (tmux:phaseB)  doped_chelation_r90 vs neutral_chelation_r0"
PB=/data/work/runs/sdcp_linio2_binding/phaseB_v7c
declare -A EN
done=0
now=$(date +%s)
for j in slab complex_doped complex_neutral mol_doped mol_neutral; do
    f=$PB/$j/scf.out
    u0=$PB/$j/scf_u0.out
    if [ ! -f "$f" ] && [ -f "$u0" ] && ! grep -q "JOB DONE" "$u0" 2>/dev/null; then
        it0=$(grep -c "iteration #" "$u0" 2>/dev/null)
        ac0=$(grep "estimated scf accuracy" "$u0" 2>/dev/null | tail -1 | awk '{print $(NF-1)}')
        printf "   %-16s ⏳ U0 워밍업 scf-iter %s | acc %s Ry\n" "$j" "${it0:-0}" "${ac0:-–}"
        continue
    fi
    if [ ! -f "$f" ]; then
        [ -f "$u0" ] && grep -q "JOB DONE" "$u0" 2>/dev/null \
            && printf "   %-16s ⬚ U0 완료 — U6.2 대기\n" "$j" \
            || printf "   %-16s ⬚ 대기\n" "$j"
        continue
    fi
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
