#!/usr/bin/env bash
# pure-SE OAT 민감도 + E 스윕 — 로컬(WSL/kgy) 실행용.  ⚠ 클라우드 보드에서 돌리지 말 것.
#
#   bash dem_scripts/oat_sweep/run_all.sh                     # 순차
#   LIGGGHTS=~/src/LIGGGHTS-PUBLIC/src/lmp_auto NP=8 bash …    # mpirun -np 8
#   MPI=no bash …                                             # serial 빌드일 때
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
LIGGGHTS="${LIGGGHTS:-liggghts}"
NP="${NP:-1}"
MPI="${MPI:-auto}"          # auto | yes | no
command -v "$LIGGGHTS" >/dev/null 2>&1 || {
  echo "⛔ '$LIGGGHTS' 를 못 찾았다.  LIGGGHTS=<실행파일> 로 지정하거나 PATH 에 넣을 것."
  exit 1; }

#  ⚠⚠ 2026-08-25 실측 — MPI 빌드를 `mpirun` **없이** 직접 실행하면 `MPI_Init` 에서 **무한 대기**한다.
#    증상: 배너도 안 나오고 · CPU 0 % · RSS 12 MB 고정 · `/proc/<pid>/wchan` = `wait_woken` ·
#    fd 에 socket/eventpoll/eventfd (= OpenMPI ORTE 기계).  39분을 그렇게 서 있었다.
#    ⇒ `mpirun` 이 있으면 **np=1 이라도 반드시 거친다**.  옛 판은 NP>1 일 때만 썼다.
USE_MPI=0
case "$MPI" in
  yes) USE_MPI=1;;
  no)  USE_MPI=0;;
  *)   command -v mpirun >/dev/null 2>&1 && USE_MPI=1;;
esac
[ "$USE_MPI" = 1 ] && echo "[실행] mpirun -np $NP" || echo "[실행] 직접 (mpirun 없음/MPI=no)"
[ "$USE_MPI" = 0 ] && [ "$NP" -gt 1 ] && { echo "⛔ NP=$NP 인데 mpirun 이 없다"; exit 1; }

#  ⚠ 로그가 파일로 나가면 stdio 가 **4 KB 블록 버퍼**를 써서, 살아 있어도 로그가 비어 보인다
#    (님이 실제로 그것 때문에 죽은 줄 알았다).  줄 단위로 흘려 `tail -f` 가 되게 한다.
STDBUF=""
command -v stdbuf >/dev/null 2>&1 && STDBUF="stdbuf -oL -eL"

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
  echo "   진행 보기:  tail -f $(pwd)/log.$n.txt"
  if [ "$USE_MPI" = 1 ]; then
    $STDBUF mpirun -np "$NP" "$LIGGGHTS" -in "$f" > "log.$n.txt" 2>&1
  else
    $STDBUF "$LIGGGHTS" -in "$f" > "log.$n.txt" 2>&1
  fi
  local rc=$?
  echo "   exit=$rc · $((SECONDS-t0))s · log.$n.txt"
  #  ★ exit 0 이어도 **아무것도 안 만들었으면 실패다** (MPI 행처럼 조용히 죽는 경우)
  if [ $rc -eq 0 ] && [ ! -d "post_oat_$n" ]; then
    echo "   ⛔ exit=0 인데 post_oat_$n/ 이 없다 — 실행이 시작조차 못 했을 수 있다."
    echo "      로그 크기: $(stat -c %s "log.$n.txt" 2>/dev/null || echo 0) 바이트"
    rc=1
  fi
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
