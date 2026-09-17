#!/usr/bin/env bash
# =============================================================================
# watch_elastic.sh — run_elastic_relaxedion_gabia.sh 라이브 상태 (계 여러 개).
#
# 왜 독립 파일인가 (코드 규율 사다리)
#   watch_gap_nscf.sh 에 모드로 넣어 봤다가 되돌렸다. 그 도구는 scf/nscf **한두
#   단계**를 깊게 보는 모양인데, 여기는 **13잡 × 계 여러 개**를 얕게 훑고 마지막에
#   Cij 판독을 붙이는 모양이다. 한 파일에 넣으면 STAGELIST 가 13개로 불어나
#   출력 규율(기본은 요약)과 충돌한다. 1저자 결정 2026-09-10.
#
# 무엇을 보나
#   ① 계별 V0 relax + strain n/12
#   ② 지금 도는 점의 반복·BFGS 스텝·accuracy·경과
#   ③ ⛔ **JOB DONE 과 BFGS 완료를 구분한다** — relax 가 최대 스텝에 걸려도
#      JOB DONE 은 찍힌다 (힘대조에서 같은 함정을 겪었다)
#   ④ fit 결과를 **참조점 두 개와 나란히** — 판정은 하지 않는다
#   ⑤ GPU 점유 프로세스 (gabia 는 SEI 잡과 공유 중이다)
#
# 이 도구가 **못 하는 것**
#   · Cij 를 판정하지 않는다. 카드가 '두 참조점 중 어느 쪽에 가까운가' 로 읽으라
#     했고 문턱을 숫자로 박지 않기로 했다 — 새 수를 지어내면 그게 사후 조정이다.
#   · 왜 느린지 못 짚는다 (경과와 갱신 시각만 보인다).
#   · 계 간 설정이 같은지 확인하지 않는다 — 그건 러너의 DRY_RUN 이 할 일이다.
#
# 사용
#   watch -n 120 bash tools/elastic/watch_elastic.sh
#   ALL=1 bash tools/elastic/watch_elastic.sh      # 12점 전체 목록
#   bash tools/elastic/watch_elastic.sh --selftest
# =============================================================================
set -u
ROOT=${ROOT:-/data/work/runs}
TAGS="strain_11_p strain_11_m strain_22_p strain_22_m strain_33_p strain_33_m \
      strain_23_p strain_23_m strain_13_p strain_13_m strain_12_p strain_12_m"

# ── 점 하나의 상태 (한 곳에만 둔다 — selftest 가 이 함수를 그대로 부른다) ────
el_state() {   # $1 = .out 경로 → "상태|비고"
    local f=$1
    [ -s "$f" ] || { echo "대기|"; return; }
    if grep -aqE "Error in routine|%%%%%%%" "$f"; then
        echo "☠ 오류|$(grep -a -A1 'Error in routine' "$f" | tail -1 | cut -c1-46)"; return
    fi
    if grep -aq "JOB DONE" "$f"; then
        # ⛔⛔ 2026-09-17 정정 — 앞판은 `End of BFGS Geometry Optimization` 을 완료 표지로
        #   썼는데 **QE 는 nstep 소진에도 그 줄을 찍는다**. 그래서 strain_23_p 가
        #   `✓ 완료` 로 보고됐다 (실제: 50 스텝 소진, max|f| 0.001107 > 0.001,
        #   ΔE 4.4e-5 > 1e-5). 선언은 "BFGS 종료를 따로 본다" 였는데 실행이 안 그랬다.
        #   ⛔ 그리고 당시 음성 시험의 fixture 는 `End of BFGS` 가 **없는** 파일이라
        #     실제 실패 모드를 한 번도 안 쟀다. 아래에 진짜 fixture 를 넣었다.
        #   판정은 **`bfgs converged` 선언 하나**로 한다 — 그것만이 두 기준
        #   (ΔE < etot_conv_thr **그리고** max|f| < forc_conv_thr)을 다 통과했다는 뜻이다.
        if grep -aq "bfgs converged" "$f"; then
            echo "✓ 완료|$(grep -a 'number of scf cycles' "$f" | tail -1 | tr -s ' ' | cut -c1-40)"
        elif grep -aqi "maximum number of steps has been reached" "$f"; then
            echo "⛔ 스텝소진|nstep 에 걸렸다 — 수렴 아님. 이 점의 응력을 Cij 에 쓰면 안 된다"
        else
            echo "⚠ 완료(BFGS 미완)|JOB DONE 은 있는데 수렴 선언이 없다 — 힘이 안 내려갔다"
        fi
        return
    fi
    local nit; nit=$(grep -ac 'iteration #' "$f")
    [ "${nit:-0}" -gt 0 ] && echo "… 진행|반복 ${nit}회" || echo "… 초기화|"
}

if [ "${1:-}" = "--selftest" ]; then
    ok=0; bad=0; t=$(mktemp -d)
    chk(){ if [ "$2" = "$3" ]; then echo "  ⭕ $1"; ok=$((ok+1));
           else echo "  ⛔ $1 — 얻음 '$2' 기대 '$3'"; bad=$((bad+1)); fi; }
    chk "없는 파일은 대기" "$(el_state "$t/nope" | cut -d'|' -f1)" "대기"
    printf 'starting\n' > "$t/a";            chk "갓 시작은 초기화"      "$(el_state "$t/a" | cut -d'|' -f1)" "… 초기화"
    printf '     iteration #  3\n' > "$t/b"; chk "반복이 있으면 진행"    "$(el_state "$t/b" | cut -d'|' -f1)" "… 진행"
    # ⚠ 앞판 fixture 는 `End of BFGS` 만 있고 `bfgs converged` 가 없었다 — QE 가 그렇게
    #   찍는 경우는 **수렴이 아니라 스텝소진**이다. 실제 수렴 출력으로 고친다.
    printf '     bfgs converged in 31 scf cycles and 7 bfgs steps\n     number of scf cycles = 31\n     End of BFGS Geometry Optimization\nJOB DONE.\n' > "$t/c"
    chk "수렴 선언 + JOB DONE 이면 완료" "$(el_state "$t/c" | cut -d'|' -f1)" "✓ 완료"
    # ⛔음성 — 이 한 줄이 이 도구의 존재 이유다
    printf '     iteration #  99\nJOB DONE.\n' > "$t/d"
    chk "[음성] JOB DONE 만으로 완료 아님 (BFGS 미완)" "$(el_state "$t/d" | cut -d'|' -f1)" "⚠ 완료(BFGS 미완)"
    printf 'Error in routine electrons (1):\n     charge is wrong\n' > "$t/e"
    chk "[음성] QE 오류를 진행으로 읽지 않음" "$(el_state "$t/e" | cut -d'|' -f1)" "☠ 오류"
    printf 'End of BFGS Geometry Optimization\n' > "$t/f"     # JOB DONE 없음
    chk "[음성] BFGS 만 있고 JOB DONE 이 없으면 완료 아님" "$(el_state "$t/f" | cut -d'|' -f1)" "… 초기화"
    printf 'JOB DONE.\0\0garbage\n' > "$t/g"
    chk "[음성] NUL 오염 출력도 읽는다" "$(el_state "$t/g" | cut -d'|' -f1)" "⚠ 완료(BFGS 미완)"
    # ⛔⛔ 2026-09-17 — **진짜 실패 모드**. QE 는 nstep 소진에도 End of BFGS 를 찍는다.
    #   앞판 fixture(/d)는 그 줄이 없어서 이 경우를 한 번도 안 쟀고, 그래서 시험이
    #   초록인 채로 strain_23_p 가 `✓ 완료` 로 보고됐다.
    printf '     number of bfgs steps    =  49\n     The maximum number of steps has been reached.\n\n     End of BFGS Geometry Optimization\nJOB DONE.\n' > "$t/h"
    chk "[음성] nstep 소진은 완료가 아니다 (End of BFGS 가 찍혀도)" \
        "$(el_state "$t/h" | cut -d'|' -f1)" "⛔ 스텝소진"
    printf '     number of bfgs steps    =  11\n     bfgs converged in 42 scf cycles and 11 bfgs steps\n     number of scf cycles = 42\n     End of BFGS Geometry Optimization\nJOB DONE.\n' > "$t/i"
    chk "진짜 수렴만 완료다 (bfgs converged 선언)" "$(el_state "$t/i" | cut -d'|' -f1)" "✓ 완료"
    # ── 집계 배선 (el_state 만 시험하면 case 문의 구멍을 못 본다) ──────────────
    #   ⛔ 2026-09-17: `⛔ 스텝소진` 을 case 에 안 넣었더니 `*)` 로 떨어져 **진행 중**
    #     으로 잡혔다. el_state 시험은 10/0 초록이었다 — 시험이 집계를 안 쟀다.
    R=$t/tree; mkdir -p "$R/elastic_zz"
    CONV='     bfgs converged in 31 scf cycles and 7 bfgs steps\n     number of scf cycles = 31\n     End of BFGS Geometry Optimization\nJOB DONE.\n'
    MAXS='     number of bfgs steps    =  49\n     The maximum number of steps has been reached.\n\n     End of BFGS Geometry Optimization\nJOB DONE.\n'
    printf "$CONV" > "$R/elastic_zz/V0_relax.out"
    for tag in strain_11_p strain_11_m strain_22_p strain_22_m strain_33_p strain_33_m; do
        printf "$CONV" > "$R/elastic_zz/$tag.out"
    done
    printf "$MAXS" > "$R/elastic_zz/strain_23_p.out"      # ← 거짓 초록이 났던 그 경우
    SUM=$(ROOT=$R bash "$0" 2>/dev/null | grep -a "strain .*완료")
    case "$SUM" in
        *"6/12 완료"*"문제 1"*) echo "  ⭕ [음성] 집계: 스텝소진은 완료가 아니라 **문제**로 센다"; ok=$((ok+1)) ;;
        *) echo "  ⛔ [음성] 집계가 스텝소진을 잘못 센다 — 얻음 '$SUM'"; bad=$((bad+1)) ;;
    esac
    case "$SUM" in
        *"진행 strain_23_p"*) echo "  ⛔ [음성] 스텝소진을 '진행 중' 으로 읽는다 (case 구멍)"; bad=$((bad+1)) ;;
        *) echo "  ⭕ [음성] 끝난 점을 '진행 중' 으로 읽지 않는다"; ok=$((ok+1)) ;;
    esac
    rm -rf "$t"; echo "  selftest: ⭕ $ok · ⛔ $bad"; [ "$bad" = 0 ] || exit 1; exit 0
fi

echo "════════ $(date '+%m-%d %H:%M:%S')  relaxed-ion Cij — $ROOT ════════"
if command -v nvidia-smi >/dev/null 2>&1; then
PW=$(pgrep -af "pw.x" | grep -v "pgrep\|watch_" | head -1); if [ -z "$PW" ]; then echo "■ ⏸ pw.x 없음 — 정지/대기 (아래 '진행' 은 파일 상태일 뿐이다)"; fi
    echo "■ GPU $(nvidia-smi --query-gpu=memory.used,memory.free --format=csv,noheader | head -1)"
    nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader 2>/dev/null \
        | sed 's/^/     /' | head -5
fi

DIRS=${SYSTEMS:-$(ls -d "$ROOT"/elastic_* 2>/dev/null)}
[ -n "${DIRS// /}" ] || { echo "■ $ROOT 에 elastic_* 작업방이 없다 — 아직 안 던졌거나 ROOT 가 다르다"; exit 0; }

for D in $DIRS; do
    [ -d "$D" ] || D=$ROOT/$D
    [ -d "$D" ] || continue
    echo "■ $(basename "$D")"
    V=$D/V0_relax.out
    if [ -s "$V" ]; then
        IFS='|' read -r st note <<< "$(el_state "$V")"
        E=$(grep -a '^!' "$V" | tail -1 | awk '{print $5}')
        printf "   V0_relax: %s%s%s\n" "$st" "${E:+  E=$E Ry}" "${note:+  · $note}"
    else
        echo "   V0_relax: 대기 (아직 시작 안 함)"
    fi

    NOK=0; NBAD=0; CUR=""; NPEND=0
    for t in $TAGS; do
        IFS='|' read -r st note <<< "$(el_state "$D/$t.out")"
        case "$st" in
            "✓ 완료")            NOK=$((NOK+1)) ;;
            "⚠ 완료(BFGS 미완)"|"⛔ 스텝소진"|"☠ 오류") NBAD=$((NBAD+1)) ;;
            "대기")              NPEND=$((NPEND+1)) ;;
            *)                   CUR=$t ;;
        esac
        [ -n "${ALL:-}" ] && printf "     %-14s %-18s %s\n" "$t" "$st" "${note:0:44}"
    done
    printf "   strain %s/12 완료" "$NOK"
    [ "$NBAD"  -gt 0 ] && printf " · ⛔ 문제 %s" "$NBAD"
    [ -n "$CUR" ]      && printf " · 진행 %s" "$CUR"
    [ "$NPEND" -gt 0 ] && printf " · 대기 %s" "$NPEND"
    echo
    if [ -n "$CUR" ]; then
        F=$D/$CUR.out
        NIT=$(grep -ac 'iteration #' "$F"); BFG=$(grep -ac 'number of scf cycles' "$F")
        ACC=$(grep -a 'estimated scf accuracy' "$F" | tail -1 | awk '{print $(NF-1)}')
        CPUT=$(grep -a 'total cpu time' "$F" | tail -1 | awk '{print $(NF-1)}')
        AGE=$(( ( $(date +%s) - $(stat -c %Y "$F") ) / 60 ))
        printf "      반복 %s · BFGS %s스텝 · accuracy %s → 1e-10" "$NIT" "$BFG" "${ACC:-–}"
        [ -n "$CPUT" ] && awk -v t="$CPUT" 'BEGIN{printf "  · cpu %.0f분", t/60}'
        printf "  · 로그 %s분 전%s\n" "$AGE" "$([ "$AGE" -gt 60 ] && echo '  ⚠ 60분 무갱신')"
    fi
    [ -z "${ALL:-}" ] && [ "$NOK" -lt 12 ] && echo "      (12점 전체는 ALL=1)"

    if [ -s "$D/elastic_fit.txt" ]; then
        echo "   ── fit 결과 ── ⛔ 판정은 사람이 한다 (카드: 두 참조점 중 어느 쪽에 가까운가)"
        grep -aiE "eigenvalue|E_VRH|G_VRH|B_VRH|C44|C55|C66|positive|not pos" "$D/elastic_fit.txt" \
            | head -8 | sed 's/^/      /'
        echo "      참조 깨끗  modelc(62)         최소고유값  4.45 · 금지커플링 3.55 GPa · E_VRH 27.66"
        echo "      참조 깨짐  b2o3(2026-07-03)   최소고유값 −2.87 · 금지커플링 ~30  GPa · C66 5.15"
    elif [ "$NOK" = 12 ]; then
        echo "   ⏳ 12점 다 찼는데 fit 이 아직 없다 (러너가 곧 돌린다)"
    fi
done
