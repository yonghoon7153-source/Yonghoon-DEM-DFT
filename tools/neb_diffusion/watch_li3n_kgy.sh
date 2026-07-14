#!/bin/bash
# watch_li3n_kgy.sh v5 — kgy(RTX 3090) Li3N round-4 (min4 마무리런) watch.
#   watch -n 60 bash ~/watch_li3n_kgy.sh
# round-3 결산: p0_saddle3 bfgs 수렴 (확정 앵커). round-4 = p0_min4 단독 완주
# (min3 ion-20 승계) → barrier(saddle3−min4) 확정.
# v5: 승계지문 기준을 하드코딩 상수 대신 min3 마지막 '!'에서 동적으로 취득,
#     saddle3 대비 min4 현재 위치(역전 감시) 표시.
D=$HOME/work/li3n_dft
now=$(date +%s)
et=$(ps -C pw.x -o etimes= 2>/dev/null | head -1 | tr -d ' ')
echo "══════ kgy Li3N DFT (3090) round-4  $(date '+%m-%d %H:%M:%S') ══════"

# ---- 확정 앵커 ----
es=$(grep '^!' $D/p0_saddle3.out 2>/dev/null | tail -1 | awk '{print $5}')
echo " p0_saddle3: ✅ 수렴 확정  E=${es:-–} Ry (앵커)"

# ---- round-4 활성 잡 ----
J=p0_min4; O=$D/$J.out
MREF=$(grep '^!' $D/p0_min3.out 2>/dev/null | tail -1 | awk '{print $5}')
if [ ! -f "$O" ]; then
    echo " $J: ⬚ 대기 (kgy_li3n_round4_min.sh 실행 필요)"
elif grep -q "JOB DONE" "$O"; then
    conv="MAXSTEP"; grep -q "bfgs converged" "$O" && conv="수렴"
    echo " $J: ✅ JOB DONE ($conv)  E=$(grep '^!' "$O" | tail -1 | awk '{print $5}') Ry"
elif grep -qiE "out of memory|cuMemAlloc|Error in routine" "$O"; then
    echo " $J: ✗ 에러/OOM — tail -20 $O 확인"
else
    ion=$(grep -c '^!' "$O")
    age=$(( now - $(stat -c %Y "$O" 2>/dev/null || echo "$now") ))
    st="⏳ RUN"; [ -z "$et" ] && st="✗ 중단(pw.x 없음) — chain.log 확인"
    line=" $J: $st  ion $ion/300 (${age}s前"
    if [ -n "$et" ] && [ "$ion" -ge 1 ]; then
        r=$(awk -v e="$et" -v n="$ion" 'BEGIN{printf "%.1f", e/60/n}')
        line="$line | ${r} min/ion"
    elif [ -n "$et" ]; then
        line="$line | 경과 $((et/60))m, 첫 SCF 진행"
    fi
    echo "$line)"
    it=$(grep "iteration #" "$O" | tail -1 | sed 's/.*iteration #[ ]*\([0-9]*\).*/\1/')
    ac=$(grep "estimated scf accuracy" "$O" | tail -1 | awk '{print $(NF-1)}')
    em=$(grep "total energy" "$O" | grep -v '^!' | tail -1 | awk '{print $(NF-1)}')
    [ -n "$ac" ] && echo "    현재 SCF: iter ${it:--} | acc ${ac} | E중간 ${em:--} Ry"
    e1=$(grep '^!' "$O" | head -1 | awk '{print $5}')
    if [ -n "$e1" ] && [ -n "$MREF" ]; then
        awk -v a="$e1" -v b="$MREF" 'BEGIN{d=(a-b)*1000; ad=(d<0?-d:d);
            printf "    승계지문: 첫E %.8f vs min3최종 %.8f → Δ %+.2f mRy %s\n", a, b, d,
                   (ad<2 ? "✓ 승계정상" : "⚠ 확인필요")}'
    fi
    if [ "$ion" -ge 3 ]; then
        grep '^!' "$O" | tail -5 | awk '{e[NR]=$5} END{
            s="    최근 dE:"; for(i=2;i<=NR;i++) s=s sprintf(" %+.2f",(e[i]-e[i-1])*1000);
            last=(e[NR]-e[NR-1])*1000; prev=(NR>2)?(e[NR-1]-e[NR-2])*1000:last;
            v="등속"; if(last>prev+0.05) v="감속중"; if(last<prev-0.05) v="가속중";
            al=(last<0?-last:last);
            printf "%s mRy | %s%s\n", s, v, (al<0.2 ? " ✓<0.2(닫기가능권)" : "")}'
    fi
    e_now=$(grep '^!' "$O" | tail -1 | awk '{print $5}')
    [ -n "$e_now" ] && [ -n "$es" ] && awk -v m="$e_now" -v s="$es" \
        'BEGIN{d=(m-s)*13605.7; printf "    saddle3 대비: min4 현재 %+.1f meV %s\n", d,
               (d>0 ? "(아직 역전 상태 — min이 saddle 위)" : "(정상 순서 복귀!)")}'
fi

# ---- 히스토리 ----
for J in p0_min3 p0_min2 p0_saddle2 p0_saddle; do
    O=$D/$J.out; [ -f "$O" ] || continue
    e=$(grep '^!' "$O" 2>/dev/null | tail -1 | awk '{print $5}')
    echo " $J: (히스토리)  E_last=${e:-–} Ry"
done

# ---- barrier 최신 계보 ----
M=$D/p0_min4.out; { [ -s "$M" ] && grep -q '^!' "$M"; } || M=$D/p0_min3.out
em2=$(grep '^!' "$M" 2>/dev/null | tail -1 | awk '{print $5}')
if [ -n "$es" ] && [ -n "$em2" ]; then
    tag="잠정"; grep -q "bfgs converged" "$M" 2>/dev/null && tag="확정"
    awk -v s="$es" -v m="$em2" -v t="$tag" -v mn="$(basename "$M" .out)" \
        'BEGIN{d=(s-m)*13605.7; printf " barrier(p0_saddle3−%s) = %+.2f mRy = %+.1f meV [%s]%s\n",
               mn,(s-m)*1000,d,t,(d<0?" ← UMA 위상 역전":"")}'
fi
tail -2 $D/chain.log 2>/dev/null | sed 's/^/ · /'
nvidia-smi --query-gpu=utilization.gpu,temperature.gpu,power.draw --format=csv,noheader 2>/dev/null | sed 's/^/ GPU util,temp,pwr: /'
echo " (완료 후: scp $D/p0_*.out gabia:/data/work/runs/li3n_pes_uma/dft_p0/)"
