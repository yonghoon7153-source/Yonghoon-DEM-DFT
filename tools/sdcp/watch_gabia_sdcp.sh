#!/bin/bash
# watch_gabia_sdcp.sh — gabia (kserver116-27) live status: p0 DFT barrier +
# SDCP Phase-B DFT+U (per-SCF detail + auto E_bind verdict). Phase-A dropped
# (done; ranking is in db/properties/sdcp_linio2_binding_phaseA.csv). p0 shown
# via the dft_p0 .out files. Install: overwrite /root/watch_li3n.sh, then
#   watch -n 30 /root/watch_li3n.sh
RY=13.605693
echo "════════ $(date '+%m-%d %H:%M:%S')  gabia — Phase-B DFT+U + p0 ════════"

# ── p0 DFT barrier ──
# 계보: round1 gabia(p0_min MAXSTEP) → round2 kgy(saddle, min2 — 둘 다 MAXSTEP)
#       → round3 kgy(saddle2→min3, nstep300, 수렴 목표) 진행 중.
# kgy 완료 후 p0_*.out 전부를 이 폴더로 scp하면 아래 barrier가 최신 계보로 자동 갱신.
echo "■ P0 DFT barrier (Li3N)  round3:kgy(saddle2→min3, nstep300) 러닝"
D=/data/work/runs/li3n_pes_uma/dft_p0
ok() { [ -s "$1" ] && grep -q "JOB DONE" "$1" 2>/dev/null; }
for j in p0_min p0_min2 p0_min3 p0_saddle p0_saddle2; do
    f=$D/$j.out; [ -f "$f" ] || continue
    e=$(grep '^!' "$f" 2>/dev/null | tail -1 | awk '{print $5}')
    if ok "$f"; then
        st="MAXSTEP"; grep -q "bfgs converged" "$f" && st="수렴"
        echo "   $j: ✅ $st  E=${e:-–} Ry"
    else
        echo "   $j: (미완/구본 — barrier 계산에서 제외)  E=${e:-–}"
    fi
done
[ -f $D/p0_saddle2.out ] || echo "   (saddle2/min3 out 미도착 — kgy watch로 추적, 잠정 barrier ≤ +71 meV 상한)"
SB=""; for c in p0_saddle2 p0_saddle; do ok $D/$c.out && { SB=$D/$c.out; break; }; done
MB=""; for c in p0_min3 p0_min2 p0_min; do ok $D/$c.out && { MB=$D/$c.out; break; }; done
if [ -n "$SB" ] && [ -n "$MB" ]; then
    es=$(grep '^!' "$SB" | tail -1 | awk '{print $5}')
    em=$(grep '^!' "$MB" | tail -1 | awk '{print $5}')
    tag="잠정(MAXSTEP 포함)"
    grep -q "bfgs converged" "$SB" && grep -q "bfgs converged" "$MB" && tag="확정(양쪽 수렴)"
    [ -n "$es" ] && [ -n "$em" ] && awk -v s="$es" -v m="$em" -v t="$tag" \
        -v sb="$(basename "$SB" .out)" -v mb="$(basename "$MB" .out)" \
        'BEGIN{printf "   ★ barrier(%s−%s) = %+.1f meV  [%s]\n",sb,mb,(s-m)*13605.7,t}'
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
        # PLATEAU 종료 시 '!' 최종에너지 줄이 없음 -> 플레인 total energy 줄로 폴백
        e=$(grep -E "^(!)? *total energy *=" "$f" 2>/dev/null | tail -1 | awk '{print $(NF-1)}')
        if grep -q "convergence has been achieved" "$f"; then cv="✓수렴"; else cv="PLATEAU±0.004Ry"; fi
        printf "   %-16s ✅ DONE %s  E=%s Ry\n" "$j" "$cv" "${e:-–}"
        EN[$j]=$e; done=$((done+1))
    elif grep -qiE "out of memory|cuMemAlloc|%%%%%%" "$f" 2>/dev/null; then
        printf "   %-16s ✗ OOM/에러 (톱업 재실행 필요)\n" "$j"
    else
        it=$(grep -c "iteration #" "$f" 2>/dev/null)
        ac=$(grep "estimated scf accuracy" "$f" 2>/dev/null | tail -1 | awk '{print $(NF-1)}')
        age=$(( now - $(stat -c %Y "$f" 2>/dev/null || echo "$now") ))
        printf "   %-16s ⏳ scf-iter %s | acc %s Ry (%ds前)\n" "$j" "${it:-0}" "${ac:-–}" "$age"
        # 하강 vs 슬로싱 판별: 최근 4개 acc + 지금까지의 best.
        # best ≈ 현재값 → 아직 하강 중 / best ≪ 현재값 → 플래토 슬로싱 (gpu2: 2.7e-3에서 300iter 종료)
        tr4=$(grep "estimated scf accuracy" "$f" 2>/dev/null | tail -4 | awk '{printf " %s",$(NF-1)}')
        bst=$(grep "estimated scf accuracy" "$f" 2>/dev/null | awk '{print $(NF-1)}' | sort -g | head -1)
        [ -n "$tr4" ] && printf "        acc 최근4:%s | best %s\n" "$tr4" "${bst:-–}"
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
