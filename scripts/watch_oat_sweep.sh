#!/usr/bin/env bash
# OAT 스윕 진행 감시 — 어느 런이 · 몇 스텝 · 얼마나 남았나.
#
# ★ 왜: 이 스윕은 런당 5시간 이상, 13런이면 며칠이다.  `tail -f` 는 지금 이 순간만
#   보여 주고, 로그가 조용하면 살았는지 죽었는지 구분이 안 된다 (오늘 39분을 그렇게 썼다).
#   ⇒ **살았나 · 어디까지 갔나 · 언제 끝나나** 를 한 화면에.
#
#   bash scripts/watch_oat_sweep.sh          # 1회 출력
#   bash scripts/watch_oat_sweep.sh -w       # 20초마다 갱신 (Ctrl-C 로 종료)
set -uo pipefail
D="$(cd "$(dirname "${BASH_SOURCE[0]}")/../dem_scripts/oat_sweep" && pwd)"

#: 입력의 총 스텝 (settling 200k + stabilize 200k + 이완 100k + 압축 루프).
#: ⚠ 압축 루프는 300 MPa 도달까지라 **가변**이다 → ETA 는 **하한**으로 읽을 것.
TOTAL=500000

_one() {
  local n_done n_all cur run pid step rate eta
  n_all=$(ls "$D"/in.*.liggghts 2>/dev/null | wc -l)
  #  ⚠⚠ 완료 = **디렉터리 존재가 아니다**.  `post_oat_*/` 은 LIGGGHTS 가 압축 시작 **전에**
  #     만든다 (입력 §shell mkdir).  존재를 완료로 세면 도는 런을 끝났다고 보고한다 —
  #     실제로 그렇게 오보했다.  ⇒ 로그의 **종료 문구**로 센다.
  n_done=$(grep -l 'Finished!' "$D"/log.*.txt 2>/dev/null | wc -l)
  echo "═══ OAT 스윕  ($(date '+%H:%M:%S')) ═══"

  #  ★ 프로세스가 있나 — 없으면 끝났거나 죽은 것이고, 그 둘은 다르다
  pid=$(pgrep -f 'lmp_(serial|auto|mpi)' | head -1)
  if [ -n "$pid" ]; then
    read -r et cpu rss < <(ps -o etime=,%cpu=,rss= -p "$pid" | tr -s ' ')
    echo "  프로세스 PID $pid · 경과 $et · CPU ${cpu}% · RSS $((rss/1024)) MB"
    #  ⚠ CPU 0 이면 계산 중이 아니다 (오늘의 MPI 행이 그랬다)
    case "$cpu" in 0.0|0) echo "  ⚠ CPU 0 % — 계산 중이 아니다.  기동 중이거나 막혔다";; esac
  else
    echo "  ⚠ 실행 중인 LIGGGHTS 프로세스 **없음** (완료 또는 중단)"
  fi

  #  ★ 가장 최근에 쓰인 로그 = 지금 도는 런
  cur=$(ls -t "$D"/log.*.txt 2>/dev/null | head -1)
  if [ -z "$cur" ]; then echo "  로그 없음 — 아직 시작 안 함"; return; fi
  run=$(basename "$cur" .txt); run=${run#log.}

  #  ⚠ thermo 줄만 고른다: 4열 이상 · 1·2열이 정수 · 마지막 열이 CPU 초.
  #    (옛 판은 grep -oE 로 잡으려다 실패해 "아직 설정 단계" 라고 오보했다 — 실제 109,000 스텝)
  read -r step cpus < <(awk '$1 ~ /^[0-9]+$/ && $2 ~ /^[0-9]+$/ && NF>=4 {s=$1; c=$NF}
                             END{print s, c}' "$cur")
  echo "  현재 런 : $run     ($n_done / $n_all 완료)"
  if [ -n "${step:-}" ]; then
    #  진행률·속도·ETA — CPU 열(4번째)이 LIGGGHTS 가 찍는 경과초다
    printf "  스텝    : %s / ~%s  (%.1f %%)\n" "$step" "$TOTAL" \
           "$(awk -v a="$step" -v b="$TOTAL" 'BEGIN{print a*100/b}')"
    if [ -n "${cpus:-}" ] && [ "$(awk -v c="$cpus" 'BEGIN{print (c>0)}')" = 1 ]; then
      rate=$(awk -v s="$step" -v c="$cpus" 'BEGIN{printf "%.1f", s/c}')
      eta=$(awk -v s="$step" -v t="$TOTAL" -v c="$cpus" \
            'BEGIN{r=s/c; if(r>0) printf "%.1f", (t-s)/r/3600; else print "?"}')
      echo "  속도    : ${rate} step/s     남은 시간 ≈ ${eta} h  (⚠ 압축 루프 가변 → **하한**)"
    fi
  else
    echo "  스텝    : 아직 (삽입/설정 단계) — 마지막 줄:"
    tail -1 "$cur" | sed 's/^/            /'
  fi

  #  ★★ 대조 2건은 특별히 따로 본다 — 이게 어긋나면 나머지는 의미가 없다
  echo "  ── 대조 ──"
  for c in orig_1type base; do
    if [ -f "$D/log.$c.txt" ] && grep -q 'Finished!' "$D/log.$c.txt" 2>/dev/null; then
      echo "    ✓ $c **완료** (덤프 $(ls "$D/post_oat_$c" 2>/dev/null | wc -l)개)"
    elif [ -f "$D/log.$c.txt" ]; then
      echo "    … $c 진행 중 (덤프 $(ls "$D/post_oat_$c" 2>/dev/null | wc -l)개)"
    else
      echo "    · $c 대기"
    fi
  done
}

if [ "${1:-}" = "-w" ]; then
  while true; do clear; _one; echo; echo "(20초마다 갱신 · Ctrl-C 종료)"; sleep 20; done
else
  _one
fi
