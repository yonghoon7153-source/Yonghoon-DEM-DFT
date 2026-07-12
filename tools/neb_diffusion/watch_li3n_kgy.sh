#!/bin/bash
# watch_li3n_kgy.sh — kgy(RTX 3090) Li3N DFT: round3 체인 p0_saddle2 → p0_min3 (nstep 300).
#   watch -n 60 bash ~/watch_li3n_kgy.sh
# round1/2(p0_min, p0_saddle, p0_min2)는 MAXSTEP 종료 — 최종 기하가 round3의 시작점.
# 닫는 기준: bfgs converged, 또는 dE 감속 <0.2 mRy/step에서 오차막대와 함께 닫기.
# barrier 줄은 최신 계보(saddle2>saddle, min3>min2)의 마지막 E로 자동 계산.
D=$HOME/work/li3n_dft
echo "══════ kgy Li3N DFT (3090)  $(date '+%m-%d %H:%M:%S') ══════"
for J in p0_saddle2 p0_min3 p0_saddle p0_min2; do
    O=$D/$J.out
    if [ ! -f "$O" ]; then echo " $J: ⬚ 대기"; continue; fi
    if grep -q "JOB DONE" "$O"; then
        conv="?"; grep -q "bfgs converged" "$O" && conv="수렴"
        grep -q "maximum number" "$O" && conv="MAXSTEP"
        echo " $J: ✅ JOB DONE ($conv)  E=$(grep '^!' "$O" | tail -1 | awk '{print $5}') Ry"
    elif grep -qiE "out of memory|cuMemAlloc|Error in routine" "$O"; then
        echo " $J: ✗ 에러/OOM — tail -20 $O 확인 (3090 초과면 KISTI 백업)"
    else
        st=$(grep -c "number of bfgs steps" "$O")
        fo=$(grep "Total force" "$O" | tail -1 | awk '{print $4}')
        age=$(( $(date +%s) - $(stat -c %Y "$O") ))
        echo " $J: ⏳ ionic≈${st:-0}/300 | force ${fo:--} (${age}s前)"
        # 최근 스텝 dE(mRy) — 닫기 판정용 (감속 & <0.2 = 닫기 가능)
        grep '^!' "$O" | tail -4 | awk '{e[NR]=$5} END{s="   "; for(i=2;i<=NR;i++) s=s sprintf(" dE %+.2f",(e[i]-e[i-1])*1000); if(NR>1) print s " mRy"}'
    fi
done
# ---- barrier (최신 계보 우선) ----
S=$D/p0_saddle2.out; [ -s "$S" ] || S=$D/p0_saddle.out
M=$D/p0_min3.out;    [ -s "$M" ] || M=$D/p0_min2.out
es=$(grep '^!' "$S" 2>/dev/null | tail -1 | awk '{print $5}')
em=$(grep '^!' "$M" 2>/dev/null | tail -1 | awk '{print $5}')
if [ -n "$es" ] && [ -n "$em" ]; then
    tag="잠정(미수렴)"
    grep -q "bfgs converged" "$S" && grep -q "bfgs converged" "$M" && tag="확정(양쪽 수렴)"
    awk -v s="$es" -v m="$em" -v t="$tag" \
        'BEGIN{printf " barrier(saddle-min) = %+.2f mRy = %+.1f meV  [%s]\n",(s-m)*1000,(s-m)*13605.7,t}'
fi
tail -2 $D/chain.log 2>/dev/null | sed 's/^/ · /'
nvidia-smi --query-compute-apps=pid,used_memory --format=csv,noheader 2>/dev/null | sed 's/^/ GPU: /'
echo " (완료 후: scp $D/p0_*.out gabia:/data/work/runs/li3n_pes_uma/dft_p0/ → gabia watch가 barrier 자동)"
