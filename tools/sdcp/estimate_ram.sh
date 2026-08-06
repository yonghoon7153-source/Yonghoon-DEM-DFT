#!/usr/bin/env bash
# =============================================================================
# estimate_ram.sh — 설정 조합별 **QE 자체 메모리 견적만** 뽑는다. 완주시키지 않는다.
#
# 왜 필요한가 (2026-08-06)
#   Phase-B 를 48 GB 한 장에 넣으려고 조합을 바꿔 가며 탐침을 돌렸는데, 조합 하나에
#   20-30분씩 태우고 OOM 으로 죽는 걸 반복했다. 그런데 QE 는 SCF 를 시작하기 **전에**
#     Estimated max dynamical RAM per process >  NN.NN GB
#   를 찍는다. 그 한 줄만 보면 되는데 끝까지 기다릴 이유가 없다.
#   → 견적 줄이 나오는 즉시 pw.x 를 죽이고 다음 조합으로 간다. 조합당 2-3분.
#
# ⚠ 견적은 상한 추정이지 실측 peak 이 아니다. 하지만 **조합 간 비교**에는 정확하고,
#   가용 메모리를 넘는지 아닌지의 1차 판정에는 충분하다 (실측: 견적 57.16 > 49.14 → OOM,
#   견적 69.30 > 49.14 → OOM). 최종 확정은 여전히 탐침(SCF 반복 완주)으로 한다.
#
#   bash tools/sdcp/estimate_ram.sh                       # 기본 조합표
#   bash tools/sdcp/estimate_ram.sh "GAP=15 ECUTWFC=50 ECUTRHO=400" "GAP=12 ECUTWFC=50 ECUTRHO=360"
#
# ⚠ 다른 pw.x 가 돌고 있으면 실행하지 말 것 — 이 스크립트는 자기가 띄운 것만 죽이지만
#   GPU 를 나눠 쓰면 견적이 아니라 실행이 실패한다.
# =============================================================================
set -uo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$REPO"
OUT=${OUT:-/data/work/runs/sdcp_v2/phaseB_v3}
F="$OUT/complex_doped_extr/scf.out"
AVAIL=${AVAIL:-49140}          # MiB — nvidia-smi memory.total
WAITS=${WAITS:-90}             # 견적 줄을 기다리는 최대 폴링 횟수 (×2초)

DEFAULT=(
  "DIAG=ppcg GAP=15 ECUTWFC=60 ECUTRHO=480"
  "DIAG=ppcg GAP=15 ECUTWFC=50 ECUTRHO=400"
  "DIAG=ppcg GAP=15 ECUTWFC=50 ECUTRHO=360"
  "DIAG=ppcg GAP=12 ECUTWFC=50 ECUTRHO=400"
  "DIAG=ppcg GAP=12 ECUTWFC=50 ECUTRHO=360"
  "DIAG=ppcg GAP=12 ECUTWFC=45 ECUTRHO=360"
)
[ $# -gt 0 ] && COMBOS=("$@") || COMBOS=("${DEFAULT[@]}")

if pgrep -f "pw.x" >/dev/null; then
  echo "⛔ pw.x 가 이미 돌고 있다 — 끝나고 실행할 것"; exit 1
fi

printf "%-46s %10s %10s %s\n" "조합" "견적(GB)" "가용(GB)" "판정"
printf '%.0s─' {1..86}; echo

for combo in "${COMBOS[@]}"; do
  rm -f "$F"
  # 러너의 probe 단계를 띄우되, 견적 줄이 나오면 즉시 죽인다.
  ( eval "$combo" MAXSTEP=1 bash tools/sdcp/run_phaseB_sdcp_v3.sh probe ) >/dev/null 2>&1 &
  runner=$!
  est=""
  for _ in $(seq 1 "$WAITS"); do
    [ -s "$F" ] && est=$(grep -a "Estimated max dynamical RAM" "$F" 2>/dev/null | tail -1 \
                          | grep -ao "[0-9.]* GB" | head -1)
    [ -n "$est" ] && break
    kill -0 "$runner" 2>/dev/null || break     # 러너가 죽었으면 더 기다리지 않는다
    sleep 2
  done
  pkill -f "pw.x" 2>/dev/null
  kill "$runner" 2>/dev/null
  wait "$runner" 2>/dev/null

  if [ -z "$est" ]; then
    printf "%-46s %10s %10s %s\n" "$combo" "—" "$(awk -v a=$AVAIL 'BEGIN{printf "%.2f", a/1024}')" \
      "⛔ 견적 줄을 못 얻음 (입력 생성 실패? 로그 확인)"
    continue
  fi
  g=${est% GB}
  verdict=$(awk -v g="$g" -v a="$AVAIL" 'BEGIN{
      av=a/1024; if (g < av-2) print "✅ 여유 " sprintf("%.1f", av-g) " GB";
      else if (g < av) print "⚠ 빠듯 " sprintf("%.1f", av-g) " GB";
      else print "⛔ 초과 " sprintf("%.1f", g-av) " GB"}')
  printf "%-46s %10s %10s %s\n" "$combo" "$g" \
    "$(awk -v a=$AVAIL 'BEGIN{printf "%.2f", a/1024}')" "$verdict"
done

echo
echo "⚠ 견적은 상한 추정이다. ✅ 가 나와도 최종 확정은 탐침(SCF 반복 완주)으로 한다:"
echo "   <조합> MAXSTEP=5 bash tools/sdcp/run_phaseB_sdcp_v3.sh probe"
echo "⚠ pseudo 하한: ecutwfc ≥ 47 (O) · ecutrho ≥ 326 (C). 그 아래는 규격 위반이다."
