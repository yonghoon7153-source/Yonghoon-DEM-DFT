#!/bin/bash
# watch_li3n_drag.sh — KISTI Li3N DFT drag 체인 (drag_p0..p8, 잡명 llm2) 상세 watch.
#   cp → /home01/x3430a02/watch_drag.sh ;  watch -n 60 bash /home01/x3430a02/watch_drag.sh
# lpsocl watch와 동일 문법: 벽킬/정체 구분, carry ↻, 잠정 프로파일 곡선, ALL_DONE 시 결과 표시.
WB=/scratch/x3430a02/kgy/li3n_drag_dft
now=$(date +%s)

echo "══════ KISTI Li3N DFT drag (9점, Kim&Cui법)  $(date '+%m-%d %H:%M:%S') ══════"
echo "── 체인 (squeue, llm2) ──"
q=$(squeue -u x3430a02 -h -n llm2 -o "  %.9i %.9T %.8M %.9L %R" 2>/dev/null | sort -k1)
if [ -n "$q" ]; then echo "$q"; else echo "  (큐에 llm2 없음)"; fi
nr=$(squeue -u x3430a02 -h -n llm2 -t RUNNING 2>/dev/null | wc -l)
[ -f "$WB/ALL_DONE" ] && echo "  ★★ ALL_DONE — 9/9 완료 → drag_result.json ★★"

last=$(ls -t $WB/logs/li3n_drag_*.out 2>/dev/null | head -1)
if [ -n "$last" ]; then
    c=$(grep -E "CARRY:" "$last" 2>/dev/null | sed 's/^/  /')
    [ -n "$c" ] && { echo "── carry 이벤트 ($(basename "$last")) ──"; echo "$c"; }
fi

echo "── 점별 진행 (GPU0: 짝수점 / GPU1: 홀수점) ──"
done=0
for k in 0 1 2 3 4 5 6 7 8; do
    f=$WB/drag_p${k}.out
    g=$((k % 2))
    cm=""
    [ -n "$last" ] && grep -q "\[p$k\] CARRY: spliced" "$last" 2>/dev/null && cm="↻"
    if [ ! -f "$f" ]; then
        printf "  p%-2s [G%s] ⬚ 대기\n" "$k" "$g"; continue
    fi
    if grep -q "JOB DONE" "$f" 2>/dev/null; then
        e=$(grep '^!' "$f" 2>/dev/null | tail -1 | awk '{print $5}')
        conv="MAXSTEP"; grep -q "bfgs converged" "$f" && conv="수렴"
        printf "  p%-2s%s [G%s] ✅ DONE(%-7s) E=%s Ry\n" "$k" "$cm" "$g" "$conv" "${e:-–}"
        done=$((done+1))
    else
        st=$(grep -c "Self-consistent Calculation" "$f" 2>/dev/null)
        en=$(grep '^!' "$f" 2>/dev/null | tail -1 | awk '{print $5}')
        fo=$(grep "Total force" "$f" 2>/dev/null | tail -1 | awk '{print $4}')
        age=$(( now - $(stat -c %Y "$f" 2>/dev/null || echo "$now") ))
        if [ "$nr" -eq 0 ]; then tag="⏸ 벽킬-carry대기"
        elif [ $age -gt 300 ]; then tag="⚠정체${age}s"
        else tag="진행"; fi
        printf "  p%-2s%s [G%s] %s  ion≈%s  E=%s  |F|=%s (%ds前)\n" \
               "$k" "$cm" "$g" "$tag" "${st:-0}" "${en:-–}" "${fo:-–}" "$age"
    fi
done
echo "  ─────  완료 $done / 9  ─────"

# 잠정 프로파일 (p0 대비 상대에너지; drag 곡선이 서서히 드러남)
e0=$(grep '^!' $WB/drag_p0.out 2>/dev/null | tail -1 | awk '{print $5}')
if [ -n "$e0" ]; then
    out="  "
    for k in 0 1 2 3 4 5 6 7 8; do
        f=$WB/drag_p${k}.out
        e=$(grep '^!' "$f" 2>/dev/null | tail -1 | awk '{print $5}')
        [ -z "$e" ] && continue
        s=""; grep -q "JOB DONE" "$f" 2>/dev/null || s="*"
        d=$(awk -v a="$e" -v b="$e0" 'BEGIN{printf "%+d",(a-b)*13605.7}')
        out="${out}p$k ${d}${s}  "
    done
    echo "── 프로파일 잠정 (p0 대비 meV, *=미완) ──"
    echo "$out"
fi

echo "── 최신 세그먼트 로그 ──"
if [ -n "$last" ]; then
    echo "  ($(basename "$last"))"
    tail -6 "$last" 2>/dev/null | sed 's/^/  /'
else
    echo "  (로그 없음 — 세그먼트 아직 시작 안 함)"
fi
if [ -f "$WB/drag_result.json" ]; then
    echo "── 최종 결과 ──"
    python3 -c "import json; d=json.load(open('$WB/drag_result.json')); print('  barrier = %.4f eV = %.1f meV' % (d['barrier_eV'], d['barrier_eV']*1000))" 2>/dev/null
fi
