#!/bin/bash
# watch_li3n_kgy.sh v7 — kgy(RTX 3090) Li3N round-4 (min4 마무리런) watch.
#   watch -n 60 bash ~/watch_li3n_kgy.sh
# round-3 결산: p0_saddle3 bfgs 수렴 (확정 앵커). round-4 = p0_min4 단독 완주
# (min3 ion-20 승계) → barrier(saddle3−min4) 확정.
# v6 (17:08 중복발사 사고 대응): p0_min4.out 선두가 죽은 2호기의 OOM 텍스트 +
#     truncate로 생긴 NUL 구멍으로 오염 → 모든 grep에 -a(바이너리 무시),
#     판정 순서를 "JOB DONE → 프로세스 생존(pgrep) → 에러"로 재배열.
#     승계지문은 '첫 可視 !'(초반 유실로 ion 3-4부터)라 Δ −0.5 mRy까지 정상.
# v7: 최근 |F|(Total force) 4개 표시 — bfgs 종료조건이 forc_conv 1e-3이라
#     dE보다 직접적인 수렴 예고 지표.
D=$HOME/work/li3n_dft
now=$(date +%s)
echo "══════ kgy Li3N DFT (3090) round-4  $(date '+%m-%d %H:%M:%S') ══════"

es=$(grep -a '^!' $D/p0_saddle3.out 2>/dev/null | tail -1 | awk '{print $5}')
echo " p0_saddle3: ✅ 수렴 확정  E=${es:-–} Ry (앵커)"

J=p0_min4; O=$D/$J.out
alive=$(pgrep -f "pw\.x.*p0_min4\.in" | head -1)
MREF=$(grep -a '^!' $D/p0_min3.out 2>/dev/null | tail -1 | awk '{print $5}')
if [ ! -f "$O" ]; then
    echo " $J: ⬚ 대기 (kgy_li3n_round4_min.sh 실행 필요)"
elif grep -aq "JOB DONE" "$O"; then
    conv="MAXSTEP"; grep -aq "bfgs converged" "$O" && conv="수렴"
    echo " $J: ✅ JOB DONE ($conv)  E=$(grep -a '^!' "$O" | tail -1 | awk '{print $5}') Ry"
elif [ -n "$alive" ]; then
    et=$(ps -o etimes= -p "$alive" | tr -d ' ')
    ion=$(grep -ac '^!' "$O")
    age=$(( now - $(stat -c %Y "$O" 2>/dev/null || echo "$now") ))
    line=" $J: ⏳ RUN(pid $alive)  ion표시 $ion/300 (${age}s前"
    if [ -n "$et" ] && [ "$ion" -ge 1 ]; then
        r=$(awk -v e="$et" -v n="$ion" 'BEGIN{printf "%.1f", e/60/n}')
        line="$line | ~${r} min/ion"
    elif [ -n "$et" ]; then
        line="$line | 경과 $((et/60))m"
    fi
    echo "$line)"
    it=$(grep -a "iteration #" "$O" | tail -1 | sed 's/.*iteration #[ ]*\([0-9]*\).*/\1/')
    ac=$(grep -a "estimated scf accuracy" "$O" | tail -1 | awk '{print $(NF-1)}')
    em=$(grep -a "total energy" "$O" | grep -av '^!' | tail -1 | awk '{print $(NF-1)}')
    [ -n "$ac" ] && echo "    현재 SCF: iter ${it:--} | acc ${ac} | E중간 ${em:--} Ry"
    e1=$(grep -a '^!' "$O" | head -1 | awk '{print $5}')
    if [ -n "$e1" ] && [ -n "$MREF" ]; then
        awk -v a="$e1" -v b="$MREF" 'BEGIN{d=(a-b)*1000; ad=(d<0?-d:d);
            printf "    승계지문: 첫可視E %.8f vs min3최종 %.8f → Δ %+.2f mRy %s\n", a, b, d,
                   (ad<2 ? "✓ 승계정상" : "⚠ 확인필요")}'
    fi
    if [ "$ion" -ge 3 ]; then
        grep -a '^!' "$O" | tail -5 | awk '{e[NR]=$5} END{
            s="    최근 dE:"; for(i=2;i<=NR;i++) s=s sprintf(" %+.2f",(e[i]-e[i-1])*1000);
            last=(e[NR]-e[NR-1])*1000; prev=(NR>2)?(e[NR-1]-e[NR-2])*1000:last;
            v="등속"; if(last>prev+0.05) v="감속중"; if(last<prev-0.05) v="가속중";
            al=(last<0?-last:last);
            printf "%s mRy | %s%s\n", s, v, (al<0.2 ? " ✓<0.2(닫기가능권)" : "")}'
    fi
    fs=$(grep -a "Total force" "$O" | tail -4 | awk '{printf " %.4f", $4}')
    [ -n "$fs" ] && echo "    최근 |F|:$fs Ry/au (bfgs 종료 forc_conv 1e-3)"
    e_now=$(grep -a '^!' "$O" | tail -1 | awk '{print $5}')
    [ -n "$e_now" ] && [ -n "$es" ] && awk -v m="$e_now" -v s="$es" \
        'BEGIN{d=(m-s)*13605.7; printf "    saddle3 대비: min4 현재 %+.1f meV %s\n", d,
               (d>0 ? "(아직 역전 상태 — min이 saddle 위)" : "(정상 순서 복귀!)")}'
elif grep -aqiE "out of memory|cuMemAlloc|Error in routine" "$O"; then
    echo " $J: ✗ 에러/OOM (프로세스 없음) — tail -20 $O 확인"
else
    echo " $J: ✗ 중단(pw.x 없음) — chain.log 확인"
fi

for J2 in p0_min3 p0_min2 p0_saddle2 p0_saddle; do
    O2=$D/$J2.out; [ -f "$O2" ] || continue
    e=$(grep -a '^!' "$O2" 2>/dev/null | tail -1 | awk '{print $5}')
    echo " $J2: (히스토리)  E_last=${e:-–} Ry"
done

M=$D/p0_min4.out; { [ -s "$M" ] && grep -aq '!' "$M"; } || M=$D/p0_min3.out
em2=$(grep -a '^!' "$M" 2>/dev/null | tail -1 | awk '{print $5}')
if [ -n "$es" ] && [ -n "$em2" ]; then
    tag="잠정"; grep -aq "bfgs converged" "$M" 2>/dev/null && tag="확정"
    awk -v s="$es" -v m="$em2" -v t="$tag" -v mn="$(basename "$M" .out)" \
        'BEGIN{d=(s-m)*13605.7; printf " barrier(p0_saddle3−%s) = %+.2f mRy = %+.1f meV [%s]%s\n",
               mn,(s-m)*1000,d,t,(d<0?" ← UMA 위상 역전":"")}'
fi
tail -2 $D/chain.log 2>/dev/null | sed 's/^/ · /'
nvidia-smi --query-gpu=utilization.gpu,temperature.gpu,power.draw --format=csv,noheader 2>/dev/null | sed 's/^/ GPU util,temp,pwr: /'
echo " (완료 후: scp $D/p0_*.out gabia:/data/work/runs/li3n_pes_uma/dft_p0/)"
