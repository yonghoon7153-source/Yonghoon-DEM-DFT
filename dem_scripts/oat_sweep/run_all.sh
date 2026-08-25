#!/usr/bin/env bash
# pure-SE OAT 민감도 + E 스윕 — 로컬(WSL/kgy) 실행용.  ⚠ 클라우드 보드에서 돌리지 말 것.
#
#   bash dem_scripts/oat_sweep/run_all.sh            # 순차 (안전)
#   LIGGGHTS=lmp_auto bash dem_scripts/oat_sweep/run_all.sh
#   NP=4 bash dem_scripts/oat_sweep/run_all.sh       # mpirun -np 4
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
LIGGGHTS="${LIGGGHTS:-liggghts}"
NP="${NP:-1}"
command -v "$LIGGGHTS" >/dev/null 2>&1 || {
  echo "⛔ '$LIGGGHTS' 를 못 찾았다.  LIGGGHTS=<실행파일> 로 지정하거나 PATH 에 넣을 것."
  exit 1; }

#  ★ 기준선을 **먼저** 돌린다 — 원본을 재현 못 하면 나머지는 볼 필요가 없다.
ORDER=$(ls in.*.liggghts | sed 's/^/ /' | tr -d '\n')
FIRST="in.base.liggghts"
[ -f "$FIRST" ] || { echo "⛔ $FIRST 가 없다"; exit 1; }

run_one() {
  local f="$1"; local n="${f#in.}"; n="${n%.liggghts}"
  echo "── $n ─────────────────────────────"
  local t0=$SECONDS
  if [ "$NP" -gt 1 ]; then mpirun -np "$NP" "$LIGGGHTS" -in "$f" > "log.$n.txt" 2>&1
  else "$LIGGGHTS" -in "$f" > "log.$n.txt" 2>&1; fi
  local rc=$?
  echo "   exit=$rc · $((SECONDS-t0))s · log.$n.txt"
  [ $rc -ne 0 ] && { echo "   ⛔ 실패 — 로그 마지막:"; tail -12 "log.$n.txt"; }
  return $rc
}

run_one "$FIRST" || { echo; echo "⛔⛔ 기준선이 실패했다.  나머지를 돌리지 않는다."; exit 1; }
echo
echo "★★ 기준선 완료.  **다음을 계속하기 전에 확인할 것**:"
echo "   post_oat_base/ 의 최종 porosity 가 원본(1-type) 결과와 같은가?"
echo "   다르면 type 리팩터가 무언가를 바꾼 것이고 OAT 결과는 무효다."
echo
for f in in.*.liggghts; do
  [ "$f" = "$FIRST" ] && continue
  run_one "$f"
done
echo "완료.  결과 수집:  python3 ../../scripts/collect_oat_sweep.py"
