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

#  ★★ 대조 **두 개**를 먼저, 정해진 순서로 돌린다 (2×2):
#     ① orig_1type (새 빌드, 원본 1-type) vs 옛 기록  → **빌드 효과**
#     ② base (2-type)         vs orig_1type          → **type 리팩터 효과**
#     둘 다 0 이어야 OAT 를 믿는다.  하나만 돌리면 두 원인이 섞인다.
CONTROLS=("in.orig_1type.liggghts" "in.base.liggghts")
for c in "${CONTROLS[@]}"; do
  [ -f "$c" ] || { echo "⛔ $c 가 없다 — 생성기를 다시 돌릴 것"; exit 1; }
done

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

for c in "${CONTROLS[@]}"; do
  run_one "$c" || { echo; echo "⛔⛔ 대조 런이 실패했다.  나머지를 돌리지 않는다."; exit 1; }
done
echo
echo "★★ 대조 2건 완료.  **계속하기 전에 두 비교를 확인할 것**:"
echo "   ① post_oat_orig_1type/ 최종 porosity  vs  옛 기록(docs/data/heckel_pure_se_dem.csv)"
echo "      → 다르면 **빌드가 다르다**.  그 차이를 먼저 기록하고, OAT 는 새 빌드 안에서만 해석."
echo "   ② post_oat_base/ (2-type)  vs  post_oat_orig_1type/ (1-type)"
echo "      → 다르면 **type 리팩터가 무언가를 바꿨다**.  OAT 결과는 무효다."
echo "   ⚠ ①만 보고 ②를 건너뛰면 두 원인이 섞인다.  둘 다 볼 것."
echo
for f in in.*.liggghts; do
  skip=0
  for c in "${CONTROLS[@]}"; do [ "$f" = "$c" ] && skip=1; done
  [ "$skip" = 1 ] && continue
  run_one "$f"
done
echo "완료."
