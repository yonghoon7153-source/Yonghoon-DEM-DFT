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
#   · 생사는 **판정**하지만 원인은 못 짚는다 (MPI 전송 실패인지 OOM 인지는 사람이).
#   · CPU 전진 표본은 기본 5초다 — 그 순간 I/O 대기 중인 랭크는 정지로 보일 수 있다.
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

# ⛔⛔ 2026-08-31 사고 — modelc nscf 가 **31시간 죽어 있었는데 이 도구는
#   "확인 필요" 라고만 찍었다.** 무갱신 문턱이 pool0 기준이라 pool0 이 끝난 뒤에는
#   의미가 없고, 로그의 MPI 오류를 아예 안 읽었기 때문이다.
#   죽음은 추정하지 말고 **두 가지 실물**로 판정한다:
#     ⓐ 로그에 MPI 전송 실패가 있나 (OpenMPI TCP BTL 이 끊기면 랭크가 죽은 소켓의
#        블로킹 recv 에 걸려 CPU 0 인 채 영원히 산다 — 죽지도 끝나지도 않는다)
#     ⓑ 누적 CPU 가 지금 늘고 있나 (`ps -o pcpu` 는 **생애 평균**이라 못 쓴다.
#        두 번 재서 차를 봐야 한다)
MPI_DEAD_RE='mca_btl_tcp_recv_blocking|Connection reset by peer|MPI_ABORT|ORTE has lost communication'

mpi_dead_lines() {   # $1 = .out  → 최근 200줄 중 MPI 전송 실패 줄 수
    # ⚠ `grep -c` 는 0건이어도 "0" 을 찍고 **exit 1** 이다. `|| echo 0` 을 붙이면
    #   "0\n0" 이 나와 숫자 비교가 깨진다 (2026-08-31 selftest 가 잡았다).
    local n
    n=$(tail -200 "$1" 2>/dev/null | grep -acE "$MPI_DEAD_RE")
    echo "${n:-0}"
}

# ⛔ 2026-08-31 실측 — `pgrep -f '…/pw\.x'` 는 **mpirun 런처까지** 잡는다
#   (런처의 명령줄에 pw.x 경로가 들어 있으니까). 런처는 자식을 기다리는 게 일이라
#   CPU 를 안 먹는다 ⇒ "10 랭크 + 런처 1 = 11 중 1개 정지" 라는 **오경보**가 났다.
#   늑대 안 왔는데 외치는 탐지기는 이번 사고(31시간 무지)의 원인 그 자체다.
#   ⇒ 프로세스 **이름**(`/proc/<pid>/comm`)이 실제로 pw.x 인 것만 랭크로 센다.
rank_pids() {        # $1 = pgrep -f 패턴 → 진짜 pw.x 랭크 pid 만
    local q
    for q in $(pgrep -f "${1:-qe-.*-cpu/bin/pw\.x}" 2>/dev/null); do
        [ "$(cat /proc/$q/comm 2>/dev/null)" = "pw.x" ] && echo "$q"
    done
}

cpu_advancing() {    # → "늘어난랭크수/전체랭크수" (표본 ${CPU_SAMPLE_S:-5}초)
    local pat=${1:-'qe-.*-cpu/bin/pw\.x'} n=${CPU_SAMPLE_S:-5}
    local a b adv=0 tot=0
    a=$(rank_pids "$pat" | while read -r q; do
            printf '%s %s\n' "$q" "$(awk '{print $14+$15}' /proc/$q/stat 2>/dev/null)"; done)
    [ -z "$a" ] && { echo "0/0"; return; }
    sleep "$n"
    b=$(rank_pids "$pat" | while read -r q; do
            printf '%s %s\n' "$q" "$(awk '{print $14+$15}' /proc/$q/stat 2>/dev/null)"; done)
    while read -r pid t0; do
        t1=$(echo "$b" | awk -v p="$pid" '$1==p{print $2}')
        [ -n "$t1" ] || continue
        tot=$((tot+1)); [ "$t1" -gt "$t0" ] 2>/dev/null && adv=$((adv+1))
    done <<< "$a"
    echo "$adv/$tot"
}

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

    # ⛔ 2026-08-31 사고 회귀시험 — MPI 전송 실패를 **죽음으로** 읽는가
    printf 'Computing kpt #  1\n     total cpu time  100.0 secs\n' > "$T/live.out"
    [ "$(mpi_dead_lines "$T/live.out")" = "0" ] \
        && say "✓" "[음성] 정상 로그를 죽음으로 오판하지 않는다" \
        || say "✗" "정상 로그를 죽음으로 오판했다"
    cat >> "$T/live.out" <<'EOF2'
[kserver][[51384,1],7][../../opal/mca/btl/tcp/btl_tcp.c:559:mca_btl_tcp_recv_blocking] recv(25) failed: Connection reset by peer (104)
EOF2
    [ "$(mpi_dead_lines "$T/live.out")" -ge 1 ] \
        && say "✓" "MPI 전송 실패 줄을 잡아낸다 (2026-08-31 사고 회귀)" \
        || say "✗" "MPI 전송 실패를 못 잡는다"
    printf 'ORTE has lost communication with a remote daemon\n' > "$T/lost.out"
    [ "$(mpi_dead_lines "$T/lost.out")" -ge 1 ] \
        && say "✓" "daemon 통신 상실도 잡아낸다" || say "✗" "daemon 상실 미검출"
    # CPU 전진 표본: 있을 리 없는 패턴이면 0/0 이어야 한다 (없는 것을 돈다고 하지 않기)
    # ⛔ 이 selftest 프로세스(bash)는 명령줄에 스크립트 경로가 들어 있어 패턴에
    #   걸리지만 comm 이 pw.x 가 아니다 — 랭크로 세면 안 된다 (런처 오경보 회귀)
    [ -z "$(rank_pids 'watch_gap_nscf')" ] \
        && say "✓" "[음성] pw.x 가 아닌 프로세스(런처·셸)를 랭크로 세지 않는다" \
        || say "✗" "런처/셸을 랭크로 셌다 — 2026-08-31 오경보 회귀"
    CPU_SAMPLE_S=1
    [ "$(cpu_advancing 'zzz_no_such_process_zzz')" = "0/0" ] \
        && say "✓" "[음성] 없는 프로세스를 '돌고 있다' 고 하지 않는다" \
        || say "✗" "없는 프로세스를 돈다고 했다"

    rm -rf "$T"
    [ "$ok" = 1 ] && { echo "selftest PASS"; exit 0; } || { echo "selftest FAIL"; exit 1; }
fi

hhmm() { date '+%m-%d %H:%M:%S'; }
echo "════════ $(hhmm)  gabia — comp1·modelc fixed-occ gap nscf ════════"

# ① 프로세스
PIDS=$(pgrep -f 'run_gap_nscf_gabia|qe-.*-cpu/bin/pw\.x' 2>/dev/null | tr '\n' ' ')
if [ -n "${PIDS// /}" ]; then
    # ⛔ 런처를 랭크로 세지 않는다 (2026-08-31 오경보) — comm 이 pw.x 인 것만
    NR=$(rank_pids 'qe-.*-cpu/bin/pw\.x' | wc -l); NR=${NR:-0}
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
        # ⛔ 이 판별을 **네 번** 고쳤다. 매번 "이번 실행" 의 경계를 간접 지표로 잡아서다:
        #     ① .in 이 .out 보다 새로운가 → 지난 판에서 곧바로 실행돼 죽은 modelc 를 못 걸렀다
        #     ② 모든 .in 중 최신 → comp1 이 nscf 로 넘어가자 끝난 scf 까지 '지난 판' 이 됐다
        #     ③ 그 단계 자신의 .in → modelc 의 지난 판 오류가 다시 살아났다
        #   ⇒ 경계는 **run.log 의 첫 타임스탬프**다. 러너가 실행 때마다 run.log 를 새로 쓴다.
        #     그보다 오래된 .out 은 무조건 지난 판이다. 간접 지표를 그만 쓴다.
        if [ -z "${RUNSTART_EPOCH:-}" ] && [ -s "$OUT/run.log" ]; then
            _t=$(grep -aom1 '^\[[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]\]' "$OUT/run.log" | tr -d '[]')
            [ -n "$_t" ] && RUNSTART_EPOCH=$(date -d "$(date +%Y)-${_t/ / }" +%s 2>/dev/null)
        fi
        # ⭐ 다섯 번째 판 — 시각 비교를 **완료 여부 뒤로** 뺐다. 규칙 방향이 틀렸었다.
        #   실측: 러너가 "comp1 scf: 이미 완료 — 건너뜀" 으로 넘어갔는데, scf.out 이
        #   이번 run.log 보다 오래됐다는 이유로 화면은 '아직 시작 안 함' 이라 찍었다.
        #   **완료된 단계는 언제 끝났든 완료다.** 시각은 *미완/실패* 출력에만 의미가 있다
        #   — 그게 지난 판 것인지 이번 판 것인지가 그때만 갈리기 때문이다.
        _OLD=0
        if [ -n "${RUNSTART_EPOCH:-}" ] && [ "$(stat -c %Y "$F")" -lt "$RUNSTART_EPOCH" ]; then
            _OLD=1
        fi
        if ! grep -aq 'JOB DONE' "$F" && [ "$_OLD" = 1 ]; then
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
            echo "   $STAGE: ✅ JOB DONE ($CONV)${E:+  E=$E Ry}$([ "$_OLD" = 1 ] && echo '  · 지난 실행에서 완료, 이번엔 건너뜀')"
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
            # ⛔⛔ 2026-08-21 — **QE 는 pool 0 의 진행만 찍는다.**
            #   -nk 10 이면 pool 0 은 170 중 17개만 맡는데, 화면은 그 17개를 170 에
            #   대고 재던 것이다. 그래서 진행률도 ETA 도 **npool 배 비관적**이었다.
            #   (이 착시가 "112 h" 추정을 만들었다 — 실제 처리량은 그 절반이었다.)
            NPOOLS=$(grep -a 'npool' "$F" | head -1 | sed 's/.*npool[^0-9]*//' | awk '{print $1}')
            [ -n "$NPOOLS" ] && [ "$NPOOLS" -gt 0 ] 2>/dev/null || NPOOLS=1
            KTOT=$(( KD * NPOOLS ))
            KPOOL=$(( ( ${NK:-0} + NPOOLS - 1 ) / NPOOLS ))
            printf "   %s: 밴드 대각화 — pool0 %s/%s · 전체 ≈ %s/%s (npool %s)" \
                   "$STAGE" "$KD" "$KPOOL" "$KTOT" "${NK:-?}" "$NPOOLS"
            [ -n "$CPUT" ] && awk -v t="$CPUT" 'BEGIN{printf "  · cpu %.1f h", t/3600}'
            echo
            if [ -n "$NK" ] && [ "${KD:-0}" -gt 0 ] && [ -n "$CPUT" ]; then
                # 처리량은 **전체 기준**으로 잰다 (pool0 개수 × npool).
                awk -v kt="$KTOT" -v n="$NK" -v t="$CPUT" 'BEGIN{
                    if (kt>0 && n>kt) printf "        전체 %.0f s/kpt · 남은 %d개 ≈ %.1f h  (초기화 포함이라 낙관 쪽으로 개선된다)\n", t/kt, n-kt, (n-kt)*(t/kt)/3600
                }'
            fi
            # ⚠ 무갱신 문턱을 60분 고정으로 뒀더니 **정상 작동을 경고로 찍었다** (2026-08-23).
            #   pool 당 k-point 하나가 4시간 넘게 걸리는 작업이라 2.3시간 침묵이 정상이다.
            #   문턱은 **실측 per-pool-kpt 시간의 1.5배**로 잡는다 — 그보다 오래 조용하면
            #   그때가 진짜 이상이다. (실측이 없으면 판정을 보류하지 경고하지 않는다.)
            printf "        로그 갱신 %s분 전" "$AGE"
            if [ "${KTOT:-0}" -gt 0 ] && [ -n "$CPUT" ]; then
                # ⛔⛔ 2026-09-02 실측 — 문턱이 **npool 배(10×) 헐거웠다.**
                #   종전: per = t/KD/60 — `t` 는 **전 랭크 누적 CPU 시간**인데
                #   `KD` 는 **pool0 하나의** kpt 수다. 단위가 섞여 npool 배 커진다.
                #   실측(modelc, npool 10): 바로 윗줄이 `2484 s/kpt`(=41.4분) 를 찍는데
                #   같은 블록에서 `414분/kpt` 이 나왔다 — 정확히 10배다.
                #   그래서 문턱이 621분이 되어, **84분 침묵을 '정상' 으로 찍었다**
                #   (자기 규칙대로면 62분 초과이므로 경고했어야 한다). fail-open 이다.
                #   ⇒ 바로 윗줄과 **같은 기준**(전체 kpt)을 쓴다. 두 수가 갈라지면
                #     둘 중 하나는 반드시 틀린 것이다.
                awk -v age="$AGE" -v kt="$KTOT" -v t="$CPUT" 'BEGIN{
                    per = t/kt/60                      # kpt 하나당 분 (전체 기준)
                    if (age > 1.5*per) printf "  (정상 주기 %.0f분/kpt 초과 — 아래 생사 판정을 본다)", per
                    else                printf "  (정상 — kpt 하나에 %.0f분 걸린다)", per
                }'
            fi
            echo
            # ── 생사 판정 (추정 아님) ──────────────────────────────────────
            DEADL=$(mpi_dead_lines "$F")
            if [ "${DEADL:-0}" -gt 0 ]; then
                echo "        ⛔⛔ MPI 전송 실패 ${DEADL}줄 — **이 잡은 죽었다**"
                echo "           OpenMPI 가 단일 노드인데 TCP BTL 을 골랐고 소켓이 끊겼다."
                echo "           랭크는 죽은 소켓의 블로킹 recv 에 걸려 CPU 0 인 채 살아 있다."
                echo "           조치: 죽이고 \`MPI_MCA='--mca btl self,vader'\` 로 재실행"
                echo "           (run_gap_nscf_gabia.sh 는 2026-08-31 부터 그게 기본값)"
            fi
            if [ -n "${PIDS// /}" ]; then
                ADV=$(cpu_advancing)
                printf "        CPU 전진 %s 랭크 (%s초 표본)" "$ADV" "${CPU_SAMPLE_S:-5}"
                case "$ADV" in
                    0/0) printf "  — 랭크 없음" ;;
                    */0) ;;
                    *) awk -v a="${ADV%%/*}" -v t="${ADV##*/}" 'BEGIN{
                           if (t>0 && a==0) printf "  ⛔ 아무도 안 돈다 — 죽었다"
                           else if (t>0 && a < t/2) printf "  ⛔ 과반이 멈췄다 — 죽었거나 갈라졌다"
                           else if (t>0 && a < t)   printf "  ⚠ 일부만 돈다 (%d개 정지)", t-a
                           else printf "  ✅ 전부 돈다" }' ;;
                esac
                echo
            fi
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
