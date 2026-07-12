#!/bin/bash
# watch_li3n_kgy.sh v3 — kgy(RTX 3090) Li3N round-3 상세 watch.
#   watch -n 60 bash ~/watch_li3n_kgy.sh
# v3 추가:
#   - 첫-SCF 내부 진행(iter/acc/중간E) — '!'가 없는 초반에도 살아있음이 보임
#   - 승계지문 자동검사: 첫 '!' E를 round-2 최종 E와 비교 (|Δ|<2 mRy → ✓)
#   - ion 페이스(min/ion, pw.x 경과시간 기반) + nstep 300 소진 ETA
#   - dE 추이 5점 + 감속/등속/가속 판정 (<0.2 mRy = 닫기가능권 표시)
#   - barrier 최신 계보 자동 (saddle2>saddle vs min3>min2), 잠정/확정 태그
D=$HOME/work/li3n_dft
SR2=-2176.42469629   # round-2 최종 E (승계지문 기준): p0_saddle
MR2=-2176.42990687   #                                p0_min2
now=$(date +%s)
et=$(ps -C pw.x -o etimes= 2>/dev/null | head -1 | tr -d ' ')
echo "══════ kgy Li3N DFT (3090) round-3  $(date '+%m-%d %H:%M:%S') ══════"

for J in p0_saddle2 p0_min3; do
    O=$D/$J.out
    [ "$J" = p0_saddle2 ] && REF=$SR2 || REF=$MR2
    if [ ! -f "$O" ]; then echo " $J: ⬚ 대기 (선행 완료 시 자동 시작)"; continue; fi
    if grep -q "JOB DONE" "$O"; then
        conv="MAXSTEP"; grep -q "bfgs converged" "$O" && conv="수렴"
        echo " $J: ✅ JOB DONE ($conv)  E=$(grep '^!' "$O" | tail -1 | awk '{print $5}') Ry"
        continue
    fi
    if grep -qiE "out of memory|cuMemAlloc|Error in routine" "$O"; then
        echo " $J: ✗ 에러/OOM — tail -20 $O 확인"; continue
    fi
    ion=$(grep -c '^!' "$O")
    age=$(( now - $(stat -c %Y "$O" 2>/dev/null || echo "$now") ))
    st="⏳ RUN"; [ -z "$et" ] && st="✗ 중단(pw.x 없음) — chain.log 확인"
    line=" $J: $st  ion $ion/300 (${age}s前"
    if [ -n "$et" ] && [ "$ion" -ge 1 ]; then
        r=$(awk -v e="$et" -v n="$ion" 'BEGIN{printf "%.1f", e/60/n}')
        eta=$(awk -v e="$et" -v n="$ion" 'BEGIN{printf "%.1f",(300-n)*e/n/86400}')
        line="$line | ${r} min/ion | nstep소진ETA ${eta}d"
    elif [ -n "$et" ]; then
        line="$line | 경과 $((et/60))m, 첫 SCF 진행"
    fi
    echo "$line)"
    it=$(grep "iteration #" "$O" | tail -1 | sed 's/.*iteration #[ ]*\([0-9]*\).*/\1/')
    ac=$(grep "estimated scf accuracy" "$O" | tail -1 | awk '{print $(NF-1)}')
    em=$(grep "total energy" "$O" | grep -v '^!' | tail -1 | awk '{print $(NF-1)}')
    [ -n "$ac" ] && echo "    현재 SCF: iter ${it:--} | acc ${ac} | E중간 ${em:--} Ry"
    e1=$(grep '^!' "$O" | head -1 | awk '{print $5}')
    if [ -n "$e1" ]; then
        awk -v a="$e1" -v b="$REF" 'BEGIN{d=(a-b)*1000; ad=(d<0?-d:d);
            printf "    승계지문: 첫E %.8f vs round2 %.8f → Δ %+.2f mRy %s\n", a, b, d,
                   (ad<2 ? "✓ 승계정상" : "⚠ 확인필요")}'
    else
        echo "    승계지문: 첫 ! 대기 (round2 최종 ${REF} 근방이면 정상)"
    fi
    if [ "$ion" -ge 3 ]; then
        grep '^!' "$O" | tail -5 | awk '{e[NR]=$5} END{
            s="    최근 dE:"; for(i=2;i<=NR;i++) s=s sprintf(" %+.2f",(e[i]-e[i-1])*1000);
            last=(e[NR]-e[NR-1])*1000; prev=(NR>2)?(e[NR-1]-e[NR-2])*1000:last;
            v="등속"; if(last>prev+0.05) v="감속중"; if(last<prev-0.05) v="가속중";
            al=(last<0?-last:last);
            printf "%s mRy | %s%s\n", s, v, (al<0.2 ? " ✓<0.2(닫기가능권)" : "")}'
        grep '^!' "$O" | awk 'NR==1{f=$5} END{printf "    누적 하강: %+.2f mRy (round3 시작 대비)\n",($5-f)*1000}'
    fi
done

for J in p0_saddle p0_min2; do
    O=$D/$J.out; [ -f "$O" ] || continue
    echo " $J: ✅ round2 MAXSTEP  E=$(grep '^!' "$O" | tail -1 | awk '{print $5}') Ry"
done

S=$D/p0_saddle2.out; { [ -s "$S" ] && grep -q '^!' "$S"; } || S=$D/p0_saddle.out
M=$D/p0_min3.out;    { [ -s "$M" ] && grep -q '^!' "$M"; } || M=$D/p0_min2.out
es=$(grep '^!' "$S" 2>/dev/null | tail -1 | awk '{print $5}')
em2=$(grep '^!' "$M" 2>/dev/null | tail -1 | awk '{print $5}')
if [ -n "$es" ] && [ -n "$em2" ]; then
    tag="잠정"; grep -q "bfgs converged" "$S" && grep -q "bfgs converged" "$M" && tag="확정"
    awk -v s="$es" -v m="$em2" -v t="$tag" -v sn="$(basename "$S" .out)" -v mn="$(basename "$M" .out)" \
        'BEGIN{printf " barrier(%s−%s) = %+.2f mRy = %+.1f meV [%s]\n",sn,mn,(s-m)*1000,(s-m)*13605.7,t}'
fi
tail -2 $D/chain.log 2>/dev/null | sed 's/^/ · /'
nvidia-smi --query-gpu=utilization.gpu,temperature.gpu,power.draw --format=csv,noheader 2>/dev/null | sed 's/^/ GPU util,temp,pwr: /'
nvidia-smi --query-compute-apps=pid,used_memory --format=csv,noheader 2>/dev/null | sed 's/^/ GPU proc: /'
echo " (완료 후: scp $D/p0_*.out gabia:/data/work/runs/li3n_pes_uma/dft_p0/)"
