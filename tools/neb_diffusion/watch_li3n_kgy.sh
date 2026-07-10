#!/bin/bash
# watch_li3n_kgy.sh — kgy(RTX 3090) Li3N DFT chain: p0_min2(연장) → p0_saddle.
#   watch -n 60 bash ~/watch_li3n_kgy.sh
# 닫는 기준(min2): 마지막 스텝들 dE가 감속하며 <0.2 mRy/step 또는 bfgs converged.
D=$HOME/work/li3n_dft
echo "══════ kgy Li3N DFT (3090)  $(date '+%m-%d %H:%M:%S') ══════"
for J in p0_min2 p0_saddle; do
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
        sc=$(grep "estimated scf accuracy" "$O" | tail -1 | awk '{print $(NF-1)}')
        age=$(( $(date +%s) - $(stat -c %Y "$O") ))
        echo " $J: ⏳ ionic≈${st:-0} | force ${fo:--} | scf ${sc:--} Ry (${age}s前)"
        # 최근 이온스텝 에너지 3개 + 스텝당 dE(mRy) — min2 '닫기 판정'용
        grep '^!' "$O" | tail -3 | awk '{e[NR]=$5} END{for(i=1;i<=NR;i++){printf "    E%d: %s",i,e[i]; if(i>1) printf "  (dE %+.2f mRy)",(e[i]-e[i-1])*1000; print ""}}'
    fi
done
tail -2 $D/chain.log 2>/dev/null | sed 's/^/ · /'
nvidia-smi --query-compute-apps=pid,used_memory --format=csv,noheader 2>/dev/null | sed 's/^/ GPU: /'
echo " (완료 후: scp $D/p0_*.out gabia:/data/work/runs/li3n_pes_uma/dft_p0/ → gabia watch가 barrier 자동)"
