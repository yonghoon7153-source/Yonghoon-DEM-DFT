#!/usr/bin/env bash
# OAT 스윕 진행판 — 13런을 한 화면에.
#
# ★ 왜: 런당 3~5시간, 13런이면 며칠이다.  `tail -f` 는 지금 이 순간만 보여 주고,
#   로그가 조용하면 살았는지 죽었는지 구분이 안 된다 (2026-08-25 에 39분을 그렇게 썼다).
#
#   bash scripts/watch_oat_sweep.sh                             # 1회
#   watch -n 300 'bash ~/dem-web/scripts/watch_oat_sweep.sh'    # 5분마다
#
# ⚠⚠ 이 스크립트가 세 번 오보한 이력 — 전부 "열의 뜻을 확인 않고 위치만 봤다":
#   ① `post_oat_*/` 존재를 완료로 셌다 → 압축 **시작 전에** 만들어진다.  ⇒ `Finished!` 로 판정.
#   ② `$NF` 를 CPU 로 봤다 → stabilize 는 `v_pressMPa` 가 붙어 마지막이 **압력**.  ⇒ 4열 고정.
#   ③ CPU 열을 누적으로 봤다 → `run` 마다 **0 으로 리셋**.  ⇒ 프로세스 `etimes` 로 나눈다.
set -uo pipefail
D="$(cd "$(dirname "${BASH_SOURCE[0]}")/../dem_scripts/oat_sweep" && pwd)"

TARGET=0.300          # 입력의 target_press (스케일계)
TOTAL=500000          # settling 200k + stabilize 200k + 이완 100k (+ 압축 루프 가변)

echo "══════════════════════════════════════════════════════════════════════════"
echo "  OAT 민감도 + E 스윕 — pure-SE 300 MPa   ($(date '+%m-%d %H:%M:%S'))"
echo "══════════════════════════════════════════════════════════════════════════"

n_all=$(ls "$D"/in.*.liggghts 2>/dev/null | wc -l)
n_fin=$(grep -al 'Finished!' "$D"/log.*.txt 2>/dev/null | wc -l)
n_err=$(grep -alE 'ERROR|MPI_ABORT' "$D"/log.*.txt 2>/dev/null | wc -l)
pid=$(pgrep -f 'lmp_(serial|auto|mpi)' | head -1)
esec=""
if [ -n "$pid" ]; then
  read -r et cpu rss < <(ps -o etime=,%cpu=,rss= -p "$pid" | tr -s ' ')
  esec=$(ps -o etimes= -p "$pid" 2>/dev/null | tr -d ' ')
  st="PID $pid · $et · CPU ${cpu}% · $((rss/1024)) MB"
  case "$cpu" in 0.0|0) st="$st  ⚠ CPU 0 % (계산 중 아님)";; esac
else
  st="⚠ 실행 프로세스 **없음** (완료 또는 중단)"
fi
echo "  완료 $n_fin/$n_all   오류 $n_err   $st"
echo ""
printf "  %-16s %-11s %-7s %-8s %-6s %-9s %s\n" \
       "런" "단계" "atoms" "압력" "목표%" "step" "비고"
echo "  ──────────────────────────────────────────────────────────────────────"

for f in "$D"/in.*.liggghts; do
  n=$(basename "$f" .liggghts); n=${n#in.}
  L="$D/log.$n.txt"
  if [ ! -f "$L" ]; then
    printf "  %-16s %-11s\n" "$n" "· 대기"; continue
  fi
  PH=$(grep -ahoE 'INSERTING|SETTLING|STABILIZE|COMPRESSION|RELAXATION|Finished' "$L" 2>/dev/null | tail -1)
  read -r S A < <(awk '$1 ~ /^[0-9]+$/ && $2 ~ /^[0-9]+$/ && NF>=4 {s=$1; a=$2} END{print s, a}' "$L")
  #  압력 — 입력이 압축 루프마다 찍는 print 를 쓴다 (thermo 열 위치에 안 기댄다)
  P=$(grep -aoE 'Current Pressure: [0-9.eE+-]+' "$L" 2>/dev/null | tail -1 | awk '{print $3}')
  PCT=""; [ -n "${P:-}" ] && PCT=$(awk -v p="$P" -v t="$TARGET" 'BEGIN{printf "%.0f%%", p/t*100}')
  NOTE=""
  if grep -aq 'Finished!' "$L" 2>/dev/null; then
    NOTE="✓ 완료 (덤프 $(ls "$D/post_oat_$n" 2>/dev/null | wc -l))"
  elif grep -aqE 'ERROR|MPI_ABORT' "$L" 2>/dev/null; then
    NOTE="⛔ $(grep -ahoE 'ERROR[^(]*' "$L" | tail -1 | cut -c1-34)"
  elif [ -n "$esec" ] && [ -n "${S:-}" ] && [ "$esec" -gt 0 ] 2>/dev/null; then
    NOTE=$(awk -v s="$S" -v e="$esec" -v t="$TOTAL" \
      'BEGIN{r=s/e; if(r>0) printf "%.0f st/s · 남은 ~%.1f h", r, (t-s)/r/3600}')
  fi
  printf "  %-16s %-11s %-7s %-8s %-6s %-9s %s\n" \
         "$n" "${PH:-시작}" "${A:-?}" "${P:-—}" "${PCT:-—}" "${S:-?}" "$NOTE"
done

echo ""
echo "  ★ 대조 2건이 먼저다 — 어긋나면 나머지 11런은 의미가 없다"
for c in orig_1type base; do
  if grep -aq 'Finished!' "$D/log.$c.txt" 2>/dev/null; then
    echo "     ✓ $c 완료  → docs/data/heckel_pure_se_dem.csv 300 MPa 행과 대조할 것"
  elif [ -f "$D/log.$c.txt" ]; then echo "     … $c 진행 중"
  else echo "     · $c 대기"; fi
done
echo "  ⚠ '남은 시간' 은 **하한** — 압축 루프가 300 MPa 도달까지라 스텝이 가변이다"
echo "══════════════════════════════════════════════════════════════════════════"
