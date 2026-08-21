#!/usr/bin/env bash
# =============================================================================
# watch_gap_nscf.sh — run_gap_nscf_gabia.sh (comp1·modelc fixed-occ gap) 라이브 상태.
#
# 왜 이 파일인가 (코드 규율 사다리 확인)
#   watch_gabia_sdcp.sh / watch_li3n_*.sh 는 QE .out 을 읽지만 **relax/`^!` 총에너지**
#   기준이고 job 목록이 그 캠페인에 박혀 있다. 여기서 봐야 하는 건 다르다:
#   scf 반복별 `estimated scf accuracy` 수렴 궤적 · nscf 의 **irr k-point 계보 대조** ·
#   fixed-occ gap 재현 목표와의 거리. 그래서 신설한다.
#
# 무엇을 보나
#   ① 프로세스 생존 + 단계 (scf / nscf / 끝)
#   ② scf 반복 수 · 최신 accuracy vs conv_thr · **자릿수 진척**(제자리인지)
#   ③ 초기화 구간을 "진행 없음" 으로 오독하지 않는다 (반복 0 = 아직 준비 중)
#   ④ ★ nscf 의 irr k-point 를 정본 기록(comp1 170 / modelc 68)과 대조
#   ⑤ 끝나면 VBM/CBM/GAP 을 재현 목표와 나란히
#
# 이 도구가 **못 하는 것**
#   · gap 이 맞는지 판정하지 않는다. 재현 목표와의 거리만 보인다.
#   · ETA 는 지난 반복 속도의 산술 외삽이다. QE 는 후반 반복이 대개 빨라져 비관적이다.
#   · nscf 는 반복이 없어(밴드 대각화) 진행률을 못 준다 — 경과 시간과 로그 갱신만 본다.
#
# 사용
#   watch -n 60 bash tools/electronic/watch_gap_nscf.sh
#   bash tools/electronic/watch_gap_nscf.sh --selftest
# =============================================================================
set -u

OUT=${OUT:-/data/work/runs/gap_nscf}
REPO=${REPO:-/data/work/repo}
[ -d "$REPO/tools/electronic" ] || REPO=$HOME/Yonghoon-DEM-DFT
SRC=$REPO/tools/electronic/standard_dos
declare -A KIRR=( [comp1]=170     [modelc]=68 )
declare -A TGAP=( [comp1]=2.066   [modelc]=2.099 )
declare -A TVBM=( [comp1]=2.128   [modelc]=2.445 )
declare -A TCBM=( [comp1]=4.194   [modelc]=4.544 )
INIT_GRACE_MIN=${INIT_GRACE_MIN:-15}   # 이 시간까지 반복 0 은 정상(초기화)

# ── 셀프테스트 (음성 경로 포함) ─────────────────────────────────────────────
if [ "${1:-}" = "--selftest" ]; then
    T=$(mktemp -d); ok=1
    say() { echo "  $1 $2"; if [ "$1" = "✗" ]; then ok=0; fi; return 0; }

    cat > "$T/scf.out" <<'EOF'
     iteration #  1     ecut=    60.00 Ry     beta= 0.30
     total cpu time spent up to now is      120.5 secs
     estimated scf accuracy    <       1.23456789 Ry
     iteration #  2     ecut=    60.00 Ry     beta= 0.30
     total cpu time spent up to now is      240.9 secs
     estimated scf accuracy    <       0.00456789 Ry
EOF
    n=$(grep -ac 'iteration #' "$T/scf.out")
    [ "$n" = "2" ] && say "✓" "반복 수 2" || say "✗" "반복 수 파싱 실패: $n"
    a=$(grep -a 'estimated scf accuracy' "$T/scf.out" | tail -1 | awk '{print $(NF-1)}')
    [ "$a" = "0.00456789" ] && say "✓" "최신 accuracy 추출" || say "✗" "accuracy 추출 실패: $a"
    t=$(grep -a 'total cpu time' "$T/scf.out" | tail -1 | awk '{print $(NF-1)}')
    [ "$t" = "240.9" ] && say "✓" "경과 cpu time 추출" || say "✗" "time 추출 실패: $t"

    # [음성] 반복이 0 인 파일을 "정체" 로 부르면 안 된다 — 초기화 중일 수 있다
    printf '     Reading input from scf.in\n     Parallel version\n' > "$T/init.out"
    n0=$(grep -ac 'iteration #' "$T/init.out")
    [ "$n0" = "0" ] && say "✓" "[음성] 반복 0 을 0 으로 정확히 센다 (초기화 구간)" \
        || say "✗" "반복 0 판정 실패: $n0"

    # [음성] QE 오류 블록을 진행으로 읽으면 안 된다
    cat > "$T/err.out" <<'EOF'
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
     Error in routine read_cards (1):
     wrong number of columns in ATOMIC_POSITIONS
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
EOF
    grep -aq 'Error in routine' "$T/err.out" && say "✓" "[음성] QE 오류 블록을 검출한다" \
        || say "✗" "오류 블록 미검출"
    grep -aq 'JOB DONE' "$T/err.out" && say "✗" "죽은 출력을 완료로 읽는다" \
        || say "✓" "[음성] 죽은 출력을 완료로 읽지 않는다"

    # ★ irr k-point 계보 대조 (양성 + 음성)
    printf '     number of k points=   170\n' > "$T/k.out"
    k=$(grep -a 'number of k points' "$T/k.out" | head -1 | sed 's/.*number of k points=[[:space:]]*//' | awk '{print $1}')
    [ "$k" = "170" ] && say "✓" "irr k-point 170 파싱" || say "✗" "k 파싱 실패: $k"
    printf '     number of k points=   260 Marzari-Vanderbilt\n' > "$T/k2.out"
    k2=$(grep -a 'number of k points' "$T/k2.out" | head -1 | sed 's/.*number of k points=[[:space:]]*//' | awk '{print $1}')
    [ "$k2" = "260" ] && say "✓" "[음성] 뒤에 글자가 붙어도 수만 뽑는다" || say "✗" "k 파싱 오염: $k2"
    [ "$k2" != "170" ] && say "✓" "[음성] 다른 k 수를 계보 일치로 오판하지 않는다" || say "✗" "계보 오판"

    # [음성] NUL 오염 출력도 grep -a 로 읽힌다
    printf '     iteration #  7\n' > "$T/nul.out"; printf '\0\0' >> "$T/nul.out"
    [ "$(grep -ac 'iteration #' "$T/nul.out")" = "1" ] \
        && say "✓" "[음성] NUL 오염 출력도 읽힌다" || say "✗" "NUL 처리 실패"

    # [음성] ★ 옛 실행의 .out 을 현재 상태로 읽으면 안 된다 (2026-08-20 실측 오보고)
    touch -d '2026-08-20 10:00' "$T/old.out"
    touch -d '2026-08-20 12:00' "$T/new.in"
    [ "$T/new.in" -nt "$T/old.out" ] \
        && say "✓" "[음성] .in 이 .out 보다 새로우면 '아직 시작 안 함' 으로 읽는다" \
        || say "✗" "옛 .out 을 현재 상태로 읽는다 (오보고 재발)"
    touch -d '2026-08-20 13:00' "$T/old.out"
    [ "$T/new.in" -nt "$T/old.out" ] \
        && say "✗" "실행된 .out 을 '시작 안 함' 으로 오판한다" \
        || say "✓" "[음성] 실제로 실행된 .out 은 정상 판독한다"

    # [음성] accuracy 가 안 줄면 잡아내야 한다
    x=$(printf '0.005\n0.005\n' | tail -2 | head -1); y=0.005
    awk -v a="$x" -v b="$y" 'BEGIN{exit !(a<=b)}' \
        && say "✓" "[음성] accuracy 정체를 검출한다" || say "✗" "정체 미검출"

    rm -rf "$T"
    [ "$ok" = 1 ] && { echo "selftest PASS"; exit 0; } || { echo "selftest FAIL"; exit 1; }
fi

hhmm() { date '+%m-%d %H:%M:%S'; }
echo "════════ $(hhmm)  gabia — comp1·modelc fixed-occ gap nscf ════════"

# ① 프로세스
PIDS=$(pgrep -f 'run_gap_nscf_gabia|qe-.*-cpu/bin/pw\.x' 2>/dev/null | tr '\n' ' ')
if [ -n "${PIDS// /}" ]; then
    NR=$(pgrep -fc 'qe-.*-cpu/bin/pw\.x' 2>/dev/null | tail -1); NR=${NR:-0}
    echo "■ 프로세스 ✅ 살아있음  (CPU pw.x rank ${NR}개)"
else
    echo "■ 프로세스 ⛔ 없음 — 끝났거나 죽었다"
fi

# 최근 상태 줄
if [ -s "$OUT/run.log" ]; then
    echo "■ run.log 최근"
    grep -a '^\[\|^   ★\|^   ⚠\|^!!\|^   VBM\|^   CBM\|^   GAP\|재현 목표' "$OUT/run.log" \
        | tail -6 | sed 's/^/   /'
fi

for S in comp1 modelc; do
    D=$OUT/$S
    [ -d "$D" ] || continue
    echo "■ $S"

    for STAGE in scf nscf_gap; do
        F=$D/$STAGE.out
        [ -s "$F" ] || { [ "$STAGE" = scf ] && echo "   $STAGE: 아직 출력 없음"; continue; }

        AGE=$(( ( $(date +%s) - $(stat -c %Y "$F") ) / 60 ))

        # ⛔ 2026-08-20 실측 (2차). 옛 실행의 .out 을 현재 상태로 보고하는 문제를
        #   "`.in` 이 `.out` 보다 새로우면 옛 판" 으로 고쳤는데 **그것도 틀렸다.**
        #   지난 판에서 modelc 는 .in 을 쓰고 **곧바로 실행해서 죽었다** — 그래서
        #   .out 이 .in 보다 새롭다. 이번 실행은 아직 modelc 차례가 오지도 않았는데
        #   화면은 여전히 지난 판의 오류를 지금 난 것처럼 찍었다.
        #   ⇒ 옳은 기준은 **이번 실행이 시작한 시각**이다. 러너는 계마다 실행 직전에
        #     .in 을 새로 만드니, 모든 .in 중 **가장 새로운 것**이 이번 실행의 진행선이다.
        #     그보다 오래된 .out 은 무조건 지난 판이다.
        # ⚠ 2026-08-21 실측 — 첫 판이 "모든 .in 중 가장 새로운 것" 을 진행선으로 썼는데,
        #   comp1 이 nscf 로 넘어가 nscf_gap.in 이 쓰이자 **끝난 scf.out 까지 '지난 판'** 이 됐다.
        #   ("comp1 scf 완료 E=-1022.9 Ry" 가 로그에 있는데 화면은 '아직 시작 안 함')
        #   ⇒ 진행선은 **그 단계 자신의 .in** 이어야 한다. 다른 단계의 .in 은 무관하다.
        IN=$D/$STAGE.in
        if [ -f "$IN" ] && [ "$IN" -nt "$F" ]; then
            echo "   $STAGE: ⏸ 이번 실행에서 아직 시작 안 함 (남은 .out 은 **지난 판**이라 안 읽는다)"
            continue
        fi

        if grep -aq 'Error in routine' "$F"; then
            echo "   $STAGE: ⛔ QE 오류"
            grep -a -A2 'Error in routine' "$F" | head -3 | sed 's/^/        /'
            continue
        fi

        # ★ irr k-point 계보 (nscf 에서 의미가 있다)
        NK=$(grep -a 'number of k points' "$F" | head -1 \
             | sed 's/.*number of k points=[[:space:]]*//' | awk '{print $1}')
        if [ "$STAGE" = "nscf_gap" ] && [ -n "$NK" ]; then
            if [ "$NK" = "${KIRR[$S]}" ]; then
                echo "        ★ irr k-point $NK = 정본 기록과 일치 — 셋업 계보 확인"
            else
                echo "        ⚠ irr k-point $NK ≠ 정본 ${KIRR[$S]} — 셋업이 정본과 다르다"
            fi
        fi

        if grep -aq 'JOB DONE' "$F"; then
            CONV=$(grep -aq 'convergence has been achieved' "$F" && echo "수렴" || echo "종료")
            E=$(grep -a '^!' "$F" | tail -1 | awk '{print $5}')
            echo "   $STAGE: ✅ JOB DONE ($CONV)${E:+  E=$E Ry}"
            if [ "$STAGE" = "nscf_gap" ]; then
                python3 "$SRC/extract_gap.py" "$F" 2>/dev/null | sed 's/^/     /'
                echo "     ── 재현 목표: VBM ${TVBM[$S]}  CBM ${TCBM[$S]}  gap ${TGAP[$S]} ──"
            fi
            continue
        fi

        CPUT=$(grep -a 'total cpu time' "$F" | tail -1 | awk '{print $(NF-1)}')
        # ⛔ nscf 는 SCF 반복이 아니라 **밴드 대각화**다 — 'iteration #' 이 영원히 0 이다.
        #   첫 판은 그걸 "초기화 중" 으로 찍다가 15분 뒤 "초기화가 너무 길다" 고 오경보할
        #   상태였다 (실측: 3.4시간째 도는데 화면은 '반복 전, 6분 경과').
        #   nscf 진행은 계산된 k-point 수로 본다.
        if [ "$STAGE" = "nscf_gap" ]; then
            KD=$(grep -ac 'Computing kpt #' "$F")
            [ "$KD" = "0" ] && KD=$(grep -ac 'ethr =' "$F")
            printf "   %s: 밴드 대각화 진행 — k-point %s/%s" "$STAGE" "$KD" "${NK:-?}"
            [ -n "$CPUT" ] && awk -v t="$CPUT" 'BEGIN{printf "  · cpu %.1f h", t/3600}'
            echo
            if [ -n "$NK" ] && [ "${KD:-0}" -gt 0 ] && [ -n "$CPUT" ]; then
                awk -v k="$KD" -v n="$NK" -v t="$CPUT" 'BEGIN{
                    if (k>0 && n>k) printf "        %.0f s/kpt · 남은 %d개 ≈ %.1f h\n", t/k, n-k, (n-k)*(t/k)/3600
                }'
            fi
            printf "        로그 갱신 %s분 전" "$AGE"
            [ "$AGE" -gt 60 ] && printf "  ⚠ 60분 무갱신"
            echo
            continue
        fi
        NIT=$(grep -ac 'iteration #' "$F")
        if [ "$NIT" -eq 0 ]; then
            # ⚠ 초기화 구간을 "진행 없음" 으로 부르지 않는다 — 52원자 USPP 는 준비만 몇 분 간다.
            if [ "$AGE" -gt "$INIT_GRACE_MIN" ]; then
                echo "   $STAGE: ⚠ 반복 0 인 채 ${AGE}분 — 초기화가 너무 길다 (확인 필요)"
            else
                echo "   $STAGE: ⏳ 초기화 중 (반복 전, ${AGE}분 경과)${CPUT:+  cpu ${CPUT}s}"
            fi
            continue
        fi

        ACC=$(grep -a 'estimated scf accuracy' "$F" | tail -1 | awk '{print $(NF-1)}')
        PREV=$(grep -a 'estimated scf accuracy' "$F" | tail -2 | head -1 | awk '{print $(NF-1)}')
        printf "   %s: 반복 %s · accuracy %s → 목표 1e-9" "$STAGE" "$NIT" "${ACC:-–}"
        [ -n "$ACC" ] && awk -v a="$ACC" 'BEGIN{if(a+0<=1e-9) printf "  ✅ 도달"}'
        echo
        # ⚠ 초반 SCF 는 원래 출렁인다 (mixing_beta 0.3). 반복 2회에서 "제자리 의심" 을
        #   찍었더니 멀쩡히 도는 계산을 문제처럼 보이게 했다 — 정직하지 않은 경고다.
        #   4회 이상 쌓였고 **최근 3회 내내** 안 줄 때만 말한다.
        if [ -n "$PREV" ] && [ -n "$ACC" ]; then
            if [ "$NIT" -lt 4 ]; then
                printf "        직전 %s → 지금 %s  (반복 %s회 — 초반은 출렁인다, 판정 보류)\n" \
                       "$PREV" "$ACC" "$NIT"
            else
                A3=$(grep -a 'estimated scf accuracy' "$F" | tail -3 | awk '{print $(NF-1)}' | tr '\n' ' ')
                awk -v s="$A3" -v p="$PREV" -v a="$ACC" 'BEGIN{
                    n=split(s,v," "); mono=1
                    for(i=2;i<=n;i++) if (v[i]+0 < v[i-1]+0) mono=0
                    if (n>=3 && mono) print "        ⚠ 최근 3회 내내 안 줄었다 (제자리 — 확인 필요)";
                    else printf "        직전 %s → 지금 %s (%.1f 자릿수 진척)\n", p, a, log(p/a)/log(10)
                }'
            fi
        fi
        if [ -n "$CPUT" ] && [ "$NIT" -gt 1 ]; then
            awk -v t="$CPUT" -v n="$NIT" 'BEGIN{printf "        %.0f s/반복 · cpu 누적 %.1f 분\n", t/n, t/60}'
        fi
        printf "        로그 갱신 %s분 전" "$AGE"
        [ "$AGE" -gt 30 ] && printf "  ⚠ 30분 무갱신"
        echo
    done
done
