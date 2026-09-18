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
#
# ── 모드 B (러너의 RUNS 모드를 본다, 2026-09-10) ──────────────────────────
#   run_gap_nscf_gabia.sh 가 RUNS 모드로 돌면 산출이 $OUT/<계>/ 가 아니라
#   **런 디렉터리 안**($RUNS/<계>/nscf_gap.out)에 떨어지고, 계 이름도 comp1/modelc
#   가 아니다. 그래서 RUNS·SYSTEMS·LOG 를 받는다. 정본 irr k / 재현 목표가 없는
#   계는 그 대조를 **건너뛴다** — 없는 기준을 맞다고 하지 않는다.
#
#   RUNS=$HOME/work/runs/nd_scf_2026_09_08 \
#   SYSTEMS="ndo_lpscl16_n4fu_O-distributed ndo_lpscl16_n5fu_O-distributed" \
#   LOG=/tmp/gap_nscf_nd.log \
#   watch -n 60 bash tools/electronic/watch_gap_nscf.sh
#
# ── 모드 C: LOBSTER/ICOHP (MODE=lobster, 2026-09-10) ────────────────────────
#   build_lobster_paw_inputs.py 가 낸 run_lobster.sh 는 **같은 pw.x 를 두 번**
#   (lobster_scf → lobster_nscf) 돌리고 lobster 를 붙인다. 단계 이름만 다르지
#   봐야 하는 것(수렴 궤적·밴드 대각화 진행·생사 판정·VRAM)은 모드 B 와 같다.
#   ⇒ 새 watch 를 만들지 않고 **단계 목록과 마무리 블록만** 갈아 끼운다.
#   갭·G5 판정은 하지 않는다 (여긴 갭을 재는 계산이 아니다).
#
#   MODE=lobster RUNS=/data/work/runs SYSTEMS=icohp_n5fu \
#   watch -n 60 bash tools/electronic/watch_gap_nscf.sh
# =============================================================================
set -u

OUT=${OUT:-/data/work/runs/gap_nscf}
RUNS=${RUNS:-}
EXT=0; [ -n "$RUNS" ] && EXT=1
# gap = fixed-occ 갭 nscf (기본) · lobster = LOBSTER/ICOHP 단계열
MODE=${MODE:-gap}
case "$MODE" in
    gap)     STAGELIST=${STAGELIST:-"scf nscf_gap nscf_dos"} ;;
    lobster) STAGELIST=${STAGELIST:-"lobster_scf lobster_nscf"}; EXT=1 ;;
    *) echo "⛔ MODE 는 gap 또는 lobster 다 (받은 값: $MODE) — 시작하지 않는다"; exit 2 ;;
esac
# 계 목록·로그 위치. 모드 B 는 런 디렉터리가 곧 계 디렉터리다.
if [ "$EXT" = 1 ]; then
    SYSLIST=${SYSTEMS:-$(ls -1 "$RUNS" 2>/dev/null | grep -v '^_' | tr '\n' ' ')}
    if [ "$MODE" = lobster ]; then
        # 러너가 런 디렉터리 안에 run.log 를 쓴다. 계가 하나뿐인 게 보통이다.
        _S1=$(echo ${SYSTEMS:-} | awk '{print $1}')
        LOG=${LOG:-$RUNS/${_S1:-.}/run.log}
    else
        LOG=${LOG:-/tmp/gap_nscf_nd.log}
    fi
    PWPAT=${PWPAT:-'qe-.*-gpu/bin/pw\.x'}
else
    SYSLIST=${SYSTEMS:-"comp1 modelc"}
    LOG=${LOG:-$OUT/run.log}
    PWPAT=${PWPAT:-'qe-.*-cpu/bin/pw\.x'}
fi
REPO=${REPO:-/data/work/repo}
[ -d "$REPO/tools/electronic" ] || REPO=$PWD
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

# ── LOBSTER 판독 헬퍼 ────────────────────────────────────────────────────────
#   ⚠ 본문과 selftest 가 **같은 함수**를 쓴다. 시험이 본문 코드를 베끼면
#     본문만 고쳐도 시험은 계속 통과한다 (그건 시험이 아니다).
lobster_spill() {    # $1 = lobsterout → spilling 줄 + 5% 판정
    local sp
    sp=$(grep -aiE 'spilling' "$1" 2>/dev/null | grep -avi 'spillings:' | tail -3)
    [ -n "$sp" ] || return 0
    echo "$sp" | sed 's/^ *//;s/^/        /'
    # 5 % 는 build_lobster_paw_inputs.py docstring 의 기준이다.
    echo "$sp" | grep -aoE '[0-9]+\.[0-9]+ *%' | tr -d ' %' | awk '{
        if ($1+0 > 5) bad=1 } END {
        if (bad) print "        ⚠ 5 % 초과 — 기저가 유사포텐셜과 어긋났을 수 있다 (ICOHP 정량 인용 보류)"
        else if (NR>0) print "        ✅ 5 % 미만 — 기저 적합" }'
}

# ⛔ 2026-09-18 교정 — 아래 둘은 **조용히** 틀렸었다. 6월 실물
#   (db/raw/nd_lobster/ICOHPLIST.lobster) 로 재보고 잡았다.
#   ① 헤더가 **두 줄**이다 (`COHP# atomMU …` + `for spin 1  for spin 2`).
#      `NR>1` 은 한 줄만 건너뛰어 둘째 줄이 데이터로 들어가고
#      `-spin 1쌍 Σ 2.000` 이라는 없는 원소쌍이 생겼다.
#   ② 스핀분극 파일은 ICOHP 열이 **둘**(spin1·spin2)이고 총 ICOHP 는 그 **합**이다.
#      `$(NF)` 는 spin 2 만 집어 전부 **약 절반**으로 나왔다
#      (Nd–S −0.218 vs 원장 −0.436 · P–S −2.836 vs −5.672).
#      우리 frozen-4f 런은 **비분극**이라 열이 하나 → `$(NF)` 가 맞는다.
#      ⇒ 고치지 않으면 6월(반값)과 9월/우리(온값)를 **2배 어긋난 채** 나란히 놓게 된다.
#      바로 이 비교가 이 캠페인의 전부다.
#   ⚠ 스핀 유무는 **헤더에서 읽는다**. `$(NF)+$(NF-1)` 은 비분극 파일에서
#      transZ(=0)를 더해 우연히 맞을 뿐이고, 우연히 맞는 것은 규칙이 아니다.
icohp_spin_cols() {  # $1 = ICOHPLIST → ICOHP 열 수 (1 또는 2). 못 읽으면 0.
    head -3 "$1" 2>/dev/null | grep -aqi 'for spin 2' && { echo 2; return; }
    head -3 "$1" 2>/dev/null | grep -aqi 'ICOHP'      && { echo 1; return; }
    echo 0
}

icohp_pairs() {      # $1 = ICOHPLIST.lobster → 원소쌍별 쌍수·ΣICOHP(총합)
    local nsp; nsp=$(icohp_spin_cols "$1")
    [ "$nsp" = 0 ] && { echo "        ⚠ ICOHPLIST 헤더를 못 읽었다 — 집계하지 않는다"; return; }
    echo "        (ICOHP 열 ${nsp}개 → $([ "$nsp" = 2 ] && echo '스핀 둘을 **합**해서' || echo '비분극, 그대로') 집계)"
    awk -v nsp="$nsp" '$1+0>0 && NF>=5 {
              a=$2;b=$3;gsub(/[0-9]/,"",a);gsub(/[0-9]/,"",b);
              if(a>b){t=a;a=b;b=t}; k=a"-"b; n[k]++;
              s[k] += (nsp==2 ? $(NF)+$(NF-1) : $(NF))}
         END{for(k in n) printf "        %-8s %3d쌍  ΣICOHP %8.3f eV (평균 %6.3f)\n", k, n[k], s[k], s[k]/n[k]}' \
        "$1" 2>/dev/null | sort
}

# ★ 카드 §2 의 게이트는 **원자 하나**(`Nd79`)에 걸려 있지 원소쌍 평균이 아니다.
#   6월에 Nd2(=NdO₂S₃Cl)가 평균을 끌어내린 게 밝혀졌기 때문이다 — 평균으로 판정하면
#   그 교훈이 지워진다. 그래서 자리별로 쪼갠다.
icohp_nd_sites() {   # $1 = ICOHPLIST → Nd 자리별 Nd–S 평균
    local nsp; nsp=$(icohp_spin_cols "$1"); [ "$nsp" = 0 ] && return
    awk -v nsp="$nsp" '$1+0>0 && NF>=5 {
              a=$2;b=$3; A=a;B=b; gsub(/[0-9]/,"",A); gsub(/[0-9]/,"",B);
              v = (nsp==2 ? $(NF)+$(NF-1) : $(NF));
              if(A=="Nd"&&B=="S"){n[a]++; s[a]+=v} else if(B=="Nd"&&A=="S"){n[b]++; s[b]+=v}}
         END{for(k in n) printf "        %-6s Nd–S %d쌍  평균 %7.3f eV\n", k, n[k], s[k]/n[k]}' \
        "$1" 2>/dev/null | sort
}

# 카드의 C1/C2/C3 판정. ⛔ 문턱을 **여기 박지 않는다** — 카드에서 읽는다.
#   못 읽으면 판정을 **생략한다**. 확인 안 된 문턱으로 판정을 찍지 않는다.
CARD_ICOHP=${CARD_ICOHP:-/data/work/repo/db/properties/nd_icohp_pp_swap_card_2026_09_16.json}
icohp_nd79_verdict() {   # $1 = ICOHPLIST, $2 = 자리 이름(기본 Nd79)
    local site=${2:-Nd79} nsp val th
    nsp=$(icohp_spin_cols "$1"); [ "$nsp" = 0 ] && return
    val=$(awk -v nsp="$nsp" -v site="$site" '$1+0>0 && NF>=5 {
              a=$2;b=$3; A=a;B=b; gsub(/[0-9]/,"",A); gsub(/[0-9]/,"",B);
              v = (nsp==2 ? $(NF)+$(NF-1) : $(NF));
              if((a==site&&B=="S")||(b==site&&A=="S")){n++; s+=v}}
         END{if(n>0) printf "%.4f %d", s/n, n}' "$1" 2>/dev/null)
    [ -n "$val" ] || { echo "        ★ $site 의 Nd–S 쌍이 없다 — 판정 불가 (자리 이름이 바뀌었나)"; return; }
    th=$(python3 -c "
import json,re,sys
d=json.load(open('$CARD_ICOHP'))['2_결과_보기_전에_고정하는_판정']
c1=re.search(r'([0-9.]+)', d['C1_PP_가_원인이다'].split('−')[1]).group(1)
c2=re.search(r'([0-9.]+)', d['C2_PP_가_원인이_아니다'].split('−')[1]).group(1)
print(c1, c2)" 2>/dev/null)
    if [ -z "$th" ]; then
        echo "        ★ $site Nd–S 평균 $(echo $val|awk '{print $1}') eV ($(echo $val|awk '{print $2}')쌍)"
        echo "        ⚠ 카드에서 문턱을 **못 읽었다**($CARD_ICOHP) — C1/C2/C3 판정을 생략한다"
        return
    fi
    echo "$val $th" | awk '{v=$1; n=$2; c1=$3; c2=$4; a=(v<0?-v:v);
        printf "        ★ %s Nd–S 평균 %.3f eV (%d쌍)  · 문턱 C1 |ICOHP|>%.1f · C2 <%.1f\n", "'"$site"'", v, n, c1, c2;
        if (a > c1) print "           ⇒ **C1** PP 가 원인. 6월 Nd–S(−0.436·−0.481) 영구 비인용 확정";
        else if (a < c2) print "           ⇒ **C2** PP 가 원인 아님. 9월 −4.080 쪽을 의심 (그 값도 비인용으로)";
        else print "           ⇒ **C3 미판정.** 어느 쪽도 선언하지 않는다 (⛔ 5%만 넘었다고 C1 로 읽지 않는다)"}'
    echo "        ⚠ 한계: 6월↔우리 k 일치는 **미상**이다 (D-2026-09-18-nd-icohp-kmesh)"
}

icohp_has_pair() {   # $1 = ICOHPLIST, $2/$3 = 원소 → 그 쌍이 있으면 0
    awk -v x="$2" -v y="$3" 'NR>1 && NF>=5 {a=$2;b=$3;gsub(/[0-9]/,"",a);gsub(/[0-9]/,"",b);
        if ((a==x&&b==y)||(a==y&&b==x)) {found=1}} END{exit found?0:1}' "$1" 2>/dev/null
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

    # ── LOBSTER 판독 (모드 C) ────────────────────────────────────────────
    cat > "$T/lo_good" <<'EOF'
spillings:
      abs. charge spilling: 1.82 %
      abs. total spilling: 3.44 %
finished in 421 s
EOF
    cat > "$T/lo_bad" <<'EOF'
spillings:
      abs. charge spilling: 11.70 %
      abs. total spilling: 18.02 %
EOF
    O=$(lobster_spill "$T/lo_good")
    echo "$O" | grep -q '✅ 5 % 미만' && say "✓" "spilling 1.82 % 를 적합으로 읽는다" \
        || say "✗" "spilling 1.82 % 판정 실패: $O"
    O=$(lobster_spill "$T/lo_bad")
    echo "$O" | grep -q '⚠ 5 % 초과' && say "✓" "[음성] spilling 11.7 % 를 통과시키지 않는다" \
        || say "✗" "[음성] spilling 11.7 % 를 놓쳤다: $O"
    : > "$T/lo_empty"
    [ -z "$(lobster_spill "$T/lo_empty")" ] && say "✓" "[음성] spilling 줄이 없으면 판정하지 않는다" \
        || say "✗" "[음성] 없는 spilling 을 판정했다"

    # ICOHPLIST — Nd 는 있고 Nd–P 는 **없는** 실제 예상 형태
    cat > "$T/ic_noNdP" <<'EOF'
COHP#  atomMU  atomNU  distance  transX  transY  transZ  ICOHP
1  Nd57  S12  2.681  0 0 0  -1.204
2  Nd57  S13  2.744  0 0 0  -1.150
3  Nd57  Cl4  2.889  0 0 0  -0.702
4  P3    S20  2.045  0 0 0  -4.310
EOF
    cat > "$T/ic_NdP" <<'EOF'
COHP#  atomMU  atomNU  distance  transX  transY  transZ  ICOHP
1  Nd57  P3   3.120  0 0 0  -0.081
2  P3    S20  2.045  0 0 0  -4.310
EOF
    icohp_has_pair "$T/ic_noNdP" Nd P && say "✗" "[음성] 없는 Nd–P 쌍을 있다고 했다" \
        || say "✓" "[음성] Nd–P 가 없으면 없다고 한다"
    icohp_has_pair "$T/ic_NdP" Nd P && say "✓" "Nd–P 쌍이 있으면 잡는다" \
        || say "✗" "있는 Nd–P 쌍을 놓쳤다"
    icohp_has_pair "$T/ic_noNdP" Nd Cl && say "✓" "Nd–Cl 쌍을 순서 무관하게 잡는다" \
        || say "✗" "Nd–Cl 쌍을 놓쳤다"
    O=$(icohp_pairs "$T/ic_noNdP")
    echo "$O" | grep -q 'Nd-S *2쌍' && say "✓" "원소쌍 집계 (Nd-S 2쌍)" \
        || say "✗" "원소쌍 집계 실패: $O"
    echo "$O" | awk '/Nd-S/{exit ($4+2.354<0.001 && $4+2.354>-0.001)?0:1}' \
        && say "✓" "ΣICOHP 합산 (Nd-S −2.354 eV)" || say "✗" "ΣICOHP 합산 실패: $O"
    # ⛔ 헤더를 데이터로 세면 **없는 원소쌍 하나**(atomMU-atomNU)가 더 생긴다.
    #   ⚠ 2026-09-18: 이 시험이 **출력 줄 수**를 세고 있었다 — 쌍이 아니라 줄이다.
    #     집계 줄을 하나 추가하자마자 빨간불이 났다. 세야 하는 건 `ΣICOHP` 를 가진 줄이다.
    NK=$(echo "$O" | grep -c 'ΣICOHP')
    [ "$NK" = 3 ] && say "✓" "[음성] 헤더 줄을 쌍으로 세지 않는다 (원소쌍 3종)" \
        || say "✗" "[음성] 원소쌍이 3종이 아니다 (${NK}종) — 헤더가 섞였나: $O"

    # ── 스핀분극 ICOHPLIST (6월 실물 형태) — 여기가 비어 있어서 2배 오차가 살아남았다 ──
    #   헤더 **두 줄** + ICOHP 열 **둘**. 값은 db/raw/nd_lobster/ICOHPLIST.lobster 에서 땄다.
    cat > "$T/ic_spin" <<'EOF'
  COHP#    atomMU    atomNU   distance   translation   ICOHP (at) eF    ICOHP (at) eF
                                                          for spin 1       for spin 2
      1       P25       S40    2.06950     0   0   0        -3.07238         -3.07509
    443      Nd2       O35    2.60866     0   0   0        -0.23638         -0.24008
    445      Nd2       S45    3.17786     0   0   0        -0.10074         -0.10246
    446      Nd2       S46    2.97362    -1   0   0        -0.23627         -0.23921
    500     Nd79       S60    2.70000     0   0   0        -0.24000         -0.24100
EOF
    [ "$(icohp_spin_cols "$T/ic_spin")" = 2 ] && say "✓" "스핀분극 파일의 ICOHP 열을 2로 읽는다" \
        || say "✗" "스핀 열 수 오독: $(icohp_spin_cols "$T/ic_spin")"
    [ "$(icohp_spin_cols "$T/ic_noNdP")" = 1 ] && say "✓" "비분극 파일은 1로 읽는다" \
        || say "✗" "비분극 열 수 오독: $(icohp_spin_cols "$T/ic_noNdP")"
    OS=$(icohp_pairs "$T/ic_spin")
    # ⛔음성 — 헤더 **둘째 줄**('for spin 1 …')이 쌍으로 세어지면 안 된다
    echo "$OS" | grep -q -- '-spin' && say "✗" "[음성] 헤더 둘째 줄을 원소쌍으로 셌다: $OS" \
        || say "✓" "[음성] 헤더가 **두 줄**이어도 쌍으로 세지 않는다"
    # ⛔음성 — spin 2 만 집으면 P–S 가 −3.075. 합이면 −6.147.
    echo "$OS" | awk '/P-S/{d=$4+6.147; exit (d<0.01 && d>-0.01)?0:1}' \
        && say "✓" "스핀 둘을 **합**한다 (P–S Σ −6.147, spin2 만이면 −3.075)" \
        || say "✗" "스핀 합산 실패: $(echo "$OS" | grep P-S)"
    # 자리별 — Nd2 와 Nd79 가 **갈라져야** 한다 (평균으로 뭉치면 카드 게이트가 무의미)
    ON=$(icohp_nd_sites "$T/ic_spin")
    echo "$ON" | grep -q 'Nd2 .*2쌍' && echo "$ON" | grep -q 'Nd79 .*1쌍' \
        && say "✓" "Nd 자리별로 갈라 센다 (Nd2 2쌍 · Nd79 1쌍)" \
        || say "✗" "자리별 분리 실패: $ON"
    # ⛔음성 — Nd–O 는 Nd–S 집계에 섞이면 안 된다 (Nd2 는 O35 도 있다)
    # 섞였으면 3쌍이 되고 평균이 −0.305 로 끌려온다. 안 섞이면 2쌍 −0.339.
    echo "$ON" | awk '/Nd2 /{d=$5+0.339; exit (d<0.005&&d>-0.005)?0:1}' \
        && say "✓" "[음성] Nd–O 를 Nd–S 에 섞지 않는다 (Nd2 2쌍 평균 −0.339)" \
        || say "✗" "[음성] Nd–O 가 섞였다: $(echo "$ON" | grep Nd2)"
    # ⛔음성 — 카드를 못 읽으면 **판정을 찍지 않는다**
    OV=$(CARD_ICOHP=/nonexistent/card.json icohp_nd79_verdict "$T/ic_spin" Nd79)
    # ⚠ 문구('C1/C2/C3 판정을 생략한다')에 C1 이 들어 있다 — **판정 줄**만 봐야 한다.
    echo "$OV" | grep -q '판정을 생략한다' && ! echo "$OV" | grep -qE '⇒ \*\*C[12]\*\*|⇒ \*\*C3 미판정' \
        && say "✓" "[음성] 카드를 못 읽으면 C1/C2/C3 를 **찍지 않는다**" \
        || say "✗" "[음성] 문턱 없이 판정을 찍었다: $OV"
    # ⛔음성 — 없는 자리를 물으면 판정 불가라고 한다
    echo "$(icohp_nd79_verdict "$T/ic_spin" Nd999)" | grep -q '판정 불가' \
        && say "✓" "[음성] 없는 Nd 자리는 **판정 불가**라고 한다" \
        || say "✗" "[음성] 없는 자리에 판정을 찍었다"

    rm -rf "$T"
    [ "$ok" = 1 ] && { echo "selftest PASS"; exit 0; } || { echo "selftest FAIL"; exit 1; }
fi

hhmm() { date '+%m-%d %H:%M:%S'; }
if [ "$MODE" = lobster ]; then
    echo "════════ $(hhmm)  LOBSTER/ICOHP (모드 C) — $RUNS ════════"
elif [ "$EXT" = 1 ]; then
    echo "════════ $(hhmm)  fixed-occ gap nscf (모드 B) — $RUNS ════════"
else
    echo "════════ $(hhmm)  gabia — comp1·modelc fixed-occ gap nscf ════════"
fi

# ① 프로세스
# 러너 이름은 모드마다 다르다 — 모드 C 에서 gap 러너를 찾으면 **영원히 '없음'** 이다.
RUNPAT=${RUNPAT:-$([ "$MODE" = lobster ] && echo 'run_lobster\.sh|/lobster' || echo 'run_gap_nscf_gabia')}
PIDS=$(pgrep -f "$RUNPAT|$PWPAT" 2>/dev/null | tr '\n' ' ')
if [ -n "${PIDS// /}" ]; then
    # ⛔ 런처를 랭크로 세지 않는다 (2026-08-31 오경보) — comm 이 pw.x 인 것만
    NR=$(rank_pids "$PWPAT" | wc -l); NR=${NR:-0}
    echo "■ 프로세스 ✅ 살아있음  (pw.x rank ${NR}개)"
else
    echo "■ 프로세스 ⛔ 없음 — 끝났거나 죽었다"
fi

# 최근 상태 줄
if [ -s "$LOG" ]; then
    echo "■ 로그 최근 ($LOG)"
    # ⛔ 거부·오류 줄을 반드시 포함한다. 필터가 진행 로그만 보면 **러너가
    #   시작조차 안 한 것을 '도는 중' 으로 보여준다** — 2026-09-10 실측:
    #   b2o3 가 VRAM 가드에 걸려 즉시 거부됐는데 화면에는 그 줄이 안 올라와,
    #   옆에서 도는 다른 잡의 pw.x 를 보고 "살아있음" 으로 읽혔다.
    grep -a '^\[\|^   ★\|^   ⚠\|^!!\|^   VBM\|^   CBM\|^   GAP\|재현 목표\|^⛔\|^ *ERROR\|던지지 않는다\|시작하지 않는다' "$LOG" \
        | tail -6 | sed 's/^/   /'
    # 마지막 줄이 거부면 크게 띄운다 — 아래 "프로세스 살아있음" 은 남의 잡일 수 있다.
    if tail -3 "$LOG" | grep -aq '⛔\|ERROR\|던지지 않는다\|시작하지 않는다'; then
        echo "   ══ 이 런은 시작하지 못했다 (위 줄) — 아래 '프로세스' 는 다른 잡일 수 있다 ══"
    fi
fi

# GPU 를 쓰는 판이면 VRAM 도 본다 — kgy 는 공유고, 여기서 죽은 전례가 있다.
if [ "$EXT" = 1 ] && command -v nvidia-smi >/dev/null 2>&1; then
    echo "■ GPU $(nvidia-smi --query-gpu=memory.used,memory.free --format=csv,noheader | head -1)"
    # ⛔⛔ 2026-09-10 실측 — "MD 없음" 인데 VRAM 40 GB 가 잡혀 있었다. 남은 것이
    #   pw.x 인지 죽다 만 UMA python 인지 **used/free 두 숫자로는 알 수 없다.**
    #   CLAUDE.md 의 gabia 규칙(pw.x 와 UMA 동시 실행 금지)은 이걸 봐야 지킬 수 있다.
    nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader 2>/dev/null \
        | sed 's/^/     /' | head -6
    nvidia-smi --query-compute-apps=pid --format=csv,noheader 2>/dev/null | grep -q . \
        || echo "     (점유 프로세스 없음 — VRAM 이 잡혀 있다면 드라이버가 아직 회수 중이다)"
fi

for S in $SYSLIST; do
    if [ "$EXT" = 1 ]; then D=$RUNS/$S; else D=$OUT/$S; fi
    [ -d "$D" ] || continue
    echo "■ $S"

    _FIRST=$(echo $STAGELIST | awk '{print $1}')
    for STAGE in $STAGELIST; do
        F=$D/$STAGE.out
        [ -s "$F" ] || { [ "$STAGE" = "$_FIRST" ] && echo "   $STAGE: 아직 출력 없음"; continue; }

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
        # ⚠ 종전엔 $OUT/run.log 고정이라 **모드 B/C 에서 이 판별이 통째로 죽어 있었다**
        #   (모드 A 에선 LOG 기본값이 바로 그 파일이라 동작이 같다).
        if [ -z "${RUNSTART_EPOCH:-}" ] && [ -s "$LOG" ]; then
            _t=$(grep -aom1 '^\[[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]\]' "$LOG" | tr -d '[]')
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
        if [ "$STAGE" != "$_FIRST" ] && [ -n "$NK" ]; then
            if [ -z "${KIRR[$S]:-}" ]; then
                # 없는 기준과 다르다고 경고하면 그건 오경보다.
                echo "        irr k-point $NK (정본 기록 없는 계 — 대조 건너뜀)"
            elif [ "$NK" = "${KIRR[$S]}" ]; then
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
                if [ -n "${TGAP[$S]:-}" ]; then
                    echo "     ── 재현 목표: VBM ${TVBM[$S]}  CBM ${TCBM[$S]}  gap ${TGAP[$S]} ──"
                else
                    echo "     ── 재현 목표 없는 계 — 이 절대값은 인용 대상이 아니다 ──"
                fi
            fi
            continue
        fi

        CPUT=$(grep -a 'total cpu time' "$F" | tail -1 | awk '{print $(NF-1)}')
        # ⛔ nscf 는 SCF 반복이 아니라 **밴드 대각화**다 — 'iteration #' 이 영원히 0 이다.
        #   첫 판은 그걸 "초기화 중" 으로 찍다가 15분 뒤 "초기화가 너무 길다" 고 오경보할
        #   상태였다 (실측: 3.4시간째 도는데 화면은 '반복 전, 6분 경과').
        #   nscf 진행은 계산된 k-point 수로 본다.
        if [ "$STAGE" != "$_FIRST" ]; then
            # ⛔ 판본·설정에 따라 QE 가 찍는 진행 표시가 다르다. 하나만 보면
            #   **도는 잡을 0/N 으로 읽는다** (2026-09-10 실측: n5fu nscf_dos 가
            #   5/10 인데 화면은 0/10 이었다 — 'Computing kpt #' 가 안 찍히는 판이었다).
            #   ⇒ 여러 표시를 보고 **가장 큰 값**을 쓴다. 못 세는 쪽이 0 을 내도
            #     세는 쪽이 이긴다.
            KD=0
            for _pat in 'Computing kpt #' 'c_bands: ' 'ethr =' 'total cpu time spent up to now'; do
                _n=$(grep -ac "$_pat" "$F"); [ "${_n:-0}" -gt "$KD" ] && KD=$_n
            done
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
                # ⛔ 인자를 안 넘기면 기본값이 **CPU 패턴**이라 GPU 런에서
                #   "랭크 없음" 오경보가 난다 — 바로 위 줄은 $PWPAT 로 제대로
                #   세고 있어서 한 화면 안에서 두 줄이 서로 모순됐다 (2026-09-10 실측).
                ADV=$(cpu_advancing "$PWPAT")
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

    # ── DOS 후처리 (dos.x -> projwfc.x -> pdos 파일) ─────────────────────
    if [ "$MODE" = gap ]; then
    #   nscf_dos 가 끝났는데 여기가 비어 있으면 후처리에서 멈춘 것이다.
    #   "nscf 끝났다" 만 보고 끝난 줄 알면 pdos 가 없는 걸 몇 시간 뒤에 안다.
    if grep -aq 'JOB DONE' "$D/nscf_dos.out" 2>/dev/null; then
        EF=$(grep -a 'Fermi energy' "$D/nscf_dos.out" | tail -1 | awk '{print $(NF-1)}')
        [ -n "$EF" ] && echo "   nscf_dos: E_F = $EF eV (tetrahedra — 갭은 이 값이 아니라 nscf_gap 의 VBM/CBM 이다)"
        for X in dos projwfc; do
            if [ ! -s "$D/$X.out" ]; then
                echo "   $X.x: 아직 안 돌았다"
            elif grep -aq 'JOB DONE' "$D/$X.out"; then
                echo "   $X.x: OK 완료"
            else
                echo "   $X.x: 실패 — $(grep -a . "$D/$X.out" | tail -2 | tr '\n' ' ')"
            fi
        done
        PFX=$(grep -a "prefix" "$D/scf.in" 2>/dev/null | head -1 | sed "s/.*=[[:space:]]*'\([^']*\)'.*/\1/")
        if [ -n "$PFX" ]; then
            NPD=$(ls "$D/$PFX".pdos* 2>/dev/null | wc -l)
            if [ -s "$D/$PFX.dos" ]; then DOSSZ=$(du -h "$D/$PFX.dos" | cut -f1); else DOSSZ="없음"; fi
            echo "   산출: pdos 파일 ${NPD}개 · ${PFX}.dos ${DOSSZ}"
        fi
    fi
    fi

    # ── LOBSTER 단계 (모드 C) ─────────────────────────────────────────────
    #   ⛔ nscf 가 JOB DONE 이라고 끝난 게 아니다. LOBSTER 는 그 뒤에 따로 돌고,
    #     **charge spilling 이 나쁘면 조용히 나쁜 ICOHP 를 낸다** (에러가 아니다).
    if [ "$MODE" = lobster ]; then
        LO=$D/lobsterout
        if [ ! -s "$LO" ]; then
            grep -aq 'JOB DONE' "$D/lobster_nscf.out" 2>/dev/null \
                && echo "   lobster: ⏳ nscf 는 끝났는데 아직 시작 안 했다 (후처리 대기)" \
                || echo "   lobster: 아직 (nscf 먼저)"
        else
            LAGE=$(( ( $(date +%s) - $(stat -c %Y "$LO") ) / 60 ))
            if grep -aq 'finished in' "$LO"; then
                echo "   lobster: ✅ 완료 ($(grep -a 'finished in' "$LO" | tail -1 | sed 's/^ *//'))"
            else
                echo "   lobster: ⏳ 진행 중 (로그 갱신 ${LAGE}분 전)"
            fi
            lobster_spill "$LO"
            IC=$D/ICOHPLIST.lobster
            if [ -s "$IC" ]; then
                echo "        ICOHPLIST $(( $(wc -l < "$IC") - 1 )) 쌍"
                icohp_pairs "$IC"
                icohp_nd_sites "$IC"
                icohp_nd79_verdict "$IC" "${ND_SITE:-Nd79}"
                # ★ 이 계의 물음: Nd 가 P 자리에 있는데 **Nd–P 결합이 있나**.
                #   lobsterin 에 Nd–P 생성자를 일부러 넣었다 — 비어 있으면 그게 답이다.
                if icohp_has_pair "$IC" Nd P; then
                    echo "        ★ Nd–P 쌍이 **있다**"
                else
                    echo "        ★ Nd–P 쌍이 **비어 있다** — 생성자를 넣었는데 없으면 그게 결론이다"
                fi
            fi
        fi
    fi
done

# ── 모드 B: 두 셀이 다 끝났으면 G5(셀 선택)를 계산한다 ──────────────────────
#   ⛔ 문턱을 여기 박지 않는다 — **카드에서 읽는다.** 문턱이 두 곳에 있으면
#     결과를 보고 한쪽을 고치는 길이 열린다 (mlip_committee.py _card_thresholds 선례).
#     카드를 못 읽으면 갭만 나열하고 **판정하지 않는다.**
if [ "$EXT" = 1 ] && [ "$MODE" = gap ]; then
    GAPS=""
    for S in $SYSLIST; do
        F=$RUNS/$S/nscf_gap.out
        grep -aq 'JOB DONE' "$F" 2>/dev/null || continue
        G=$(python3 "$SRC/extract_gap.py" "$F" 2>/dev/null | awk '/GAP =/{print $3}')
        [ -n "$G" ] && GAPS="$GAPS $S=$G"
    done
    N=$(echo $GAPS | wc -w)
    echo "■ G5 (셀 선택)"
    if [ "$N" -lt 2 ]; then
        echo "   아직 $N/2 — 두 셀이 다 끝나야 판정한다"
    else
        CARD=${CARD:-$REPO/db/properties/ndo_lpscl16_o_motif_estimand_2026_09_09.json}
        python3 - "$CARD" $GAPS <<'PY'
import json, re, sys
card, pairs = sys.argv[1], sys.argv[2:]
vals = {}
for p in pairs:
    k, v = p.rsplit("=", 1); vals[k] = float(v)
ks = sorted(vals)
d = abs(vals[ks[0]] - vals[ks[1]])
for k in ks:
    print(f"   {k}: gap {vals[k]:.4f} eV")
print(f"   |Δgap| = {d:.4f} eV")
try:
    c = json.load(open(card, encoding="utf-8"))
    g5 = c["4_검증_게이트_결과_보기_전에"]["G5_셀선택"]
except Exception as e:
    print(f"   ⛔ 카드를 못 읽었다 ({e.__class__.__name__}) — 판정하지 않는다.")
    print(f"      CARD=<경로> 로 지정해라: {card}")
    raise SystemExit(0)
m = re.search(r"<\s*([\d.]+)\s*eV", g5)
if not m:
    print("   ⛔ 카드 G5 에서 문턱을 못 읽었다 — 판정하지 않는다.")
    raise SystemExit(0)
th = float(m.group(1))
small = [k for k in ks if "n4" in k] or [ks[0]]
print(f"   카드 문턱: |Δgap| < {th} eV → 싼 셀")
if d < th:
    print(f"   ⇒ **{small[0]}** 에서 ICOHP·DOS·PDOS (|Δgap| {d:.4f} < {th})")
else:
    big = [k for k in ks if k not in small]
    print(f"   ⇒ **{big[0] if big else ks[-1]}** 에서 ICOHP·DOS·PDOS (|Δgap| {d:.4f} ≥ {th})")
print("   ⚠ 이 갭 절대값은 셀 선택 통계다 — 인용 대상이 아니다 (카드 §5)")
PY
    fi
fi
