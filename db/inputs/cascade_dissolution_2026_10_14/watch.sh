#!/bin/bash
# 녹는 에너지 실행 감시 (gabia · 읽기만) — run_gabia.sh 의 run.log · uma/relax.log · 이완 프로세스를 한 화면에.
#   watch -n 30 bash <이 파일> [worktree 경로 (기본 /data/work/wt_diss_1014)] [tmux 세션 (기본 diss1014)]
# 진행은 '끝난 것' 과 '시작한 것' 을 같이 본다 — 이완은 구조마다 '[i/N] 이름' (시작) 과 '✓ E/atom' (끝) 을 찍는다.
# 이완 프로세스는 pgrep 결과를 comm (python*) 으로 거른다 — 패턴이 들어간 감시 · 셸 자신을 세지 않는다 (CLAUDE.md).
# 이 스크립트가 못 하는 것: 끝난 뒤 결과 판독 (combine 출력 · result/combine_report.json 을 본다) · 다른 기계의 잡.
W=${1:-/data/work/wt_diss_1014}
S=${2:-diss1014}
D=$W/db/raw/cascade_dissolution_2026_10_14
R=$D/run.log
L=$D/uma/relax.log
NOW=$(date +%s)
echo "== 녹는 에너지 감시 · $(date '+%F %T') · 부하 $(cut -d' ' -f1-3 /proc/loadavg) · $(nproc) 코어"
if tmux has-session -t "$S" 2>/dev/null; then echo "tmux $S: 있음"; else echo "tmux $S: 없음"; fi
P=$(for x in $(pgrep -f run_uma_screening.py 2>/dev/null); do
        case "$(cat /proc/"$x"/comm 2>/dev/null)" in python*) echo "$x";; esac
    done | head -n 1)
if [ -n "$P" ]; then
    ps -o pcpu=,etime=,rss= -p "$P" | awk -v p="$P" '{printf "이완 프로세스 PID %s · CPU %s %% · 경과 %s · RSS %.1f GB\n", p, $1, $2, $3/1048576}'
else
    echo "이완 프로세스: 없음 (아직 ③ 전 · 끝남 · 멈춤 — 아래 단계 줄로 가른다)"
fi
if [ ! -f "$R" ]; then echo "run.log 없음 — 아직 시작 전 ($R)"; exit 0; fi
STEP=$(grep -a -o -E '\] (①|②|③|④) .*' "$R" | tail -n 1 | cut -c3-)   # 다중 바이트는 [..] 가 아니라 (..|..) — 로캘이 C 여도 잡힌다
echo "단계: ${STEP:-—}"
# 1단계 baseline 은 컴파운드 런마다 따로 이완돼 값이 수백 개다 (GPU 잡음 ~1e-7 eV/atom) — 개수 · 최소 · 최대로 줄인다
grep -a -E '^MP .* · formulas|^runs .* · records' "$R" | tail -n 2 | awk '{
    if (match($0, /baselines \[[^]]*\]/)) {
        s = substr($0, RSTART + 11, RLENGTH - 12); n = split(s, a, ", "); mn = a[1]; mx = a[1]
        for (i = 1; i <= n; i++) { if (a[i] + 0 < mn + 0) mn = a[i]; if (a[i] + 0 > mx + 0) mx = a[i] }
        $0 = substr($0, 1, RSTART - 1) "baselines " n "개 (" mn " … " mx ")" substr($0, RSTART + RLENGTH)
    }
    print "  " $0 }'   # cut -c 는 바이트로 잘라 한글을 깬다 — 안 자른다
if [ -f "$L" ]; then
    TOT=$(grep -a -o '^\[[0-9]*/[0-9]*\]' "$L" | tail -n 1 | sed 's/.*\///; s/\]//')
    CUR=$(grep -a '^\[[0-9]*/[0-9]*\]' "$L" | tail -n 1)
    OK=$(grep -a -c '✓ E/atom=' "$L")
    BAD=$(grep -a -c '❌ FAILED' "$L")
    BL=$(grep -a 'baseline E/atom' "$L" | tail -n 1 | sed 's/^ *//')
    echo "기준 (canonical 재이완 = 대조 잡): ${BL:-아직}"
    echo "이완: 끝 $OK · 실패 $BAD / ${TOT:-—} · 지금 ${CUR:-—}"
    T0=$(grep -a '③ UMA 이완' "$R" | tail -n 1 | grep -o '^\[[^]]*\]' | tr -d '[]')
    N=$((OK + BAD))
    if [ -n "$T0" ] && [ -n "$TOT" ] && [ "$N" -gt 0 ]; then
        EL=$((NOW - $(date -d "$T0" +%s)))
        PER=$((EL / N))
        echo "경과 $((EL / 60)) 분 · 구조당 평균 $PER 초 (모델 적재 · 기준 이완 포함) · 남은 어림 $(( (TOT - N) * PER / 60 )) 분"
    fi
    grep -a '✓ E/atom=' "$L" | tail -n 2 | sed 's/^ */  마지막: /'
fi
grep -a -E '⛔|끝 ✅|Traceback|Error|Killed' "$R" | tail -n 3
