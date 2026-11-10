#!/bin/bash
# G2c′ 샌드박스 실행기 (2026-11-10 · 등록 = 메모 docs/reviews/p1_g2c_compare_definition_20261105.md §0 · §5-2 · 결과 0 건 상태에서 씀)
#   사용:  LMP=<LIGGGHTS 3d5c00f 직렬 실행 파일> bash run_g2cp.sh N OUT      (OUT = 없거나 빈 폴더 · 덮어쓰지 않는다)
#   대조:  python3 -I compare_g2cp.py OUT N                               (따로 · 실행기는 대조하지 않는다)
#   팔 (이 차례 · 직렬 · 한 번에 하나 · nice -n 19):
#     A  A2  B  B2  C  = 11-04 run_arms.sh 와 같은 덱 · 같은 인자
#     BW = BW.liggghts (R 덱 include + write_restart) · 입력 = A 의 주기 파일      → BR = R 덱 · 입력 = BW 가 쓴 restart_rt.bin
#     CW = BW.liggghts · 입력 = A2 의 명령 파일 (restart_cmd.bin)                 → CR = R 덱 · 입력 = CW 가 쓴 restart_rt.bin
#   실행 전 멈춤 (rc 3 · OUT 을 만들지 않는다 · 이유 = 화면 stderr):
#     인자 · N 꼴 (200 이상 · 100 의 배수 — R 덱 덤프 주기 100) · 도구 · LMP 없음 · 파일 아님 · 실행 권한 없음 · `-h` 첫 머리 줄에
#     "LIGGGHTS (" 없음 (빈 임시 폴더 · -log none) · OUT 비지 않음 · 11-04 덱 일곱 md5 ≠ run_40000/inputs.md5 · BW 덱 꼴 ·
#     git 작업 트리 안이면 이 폴더에 커밋 안 된 변경 · 새 파일 (등록 커밋 뒤에만 돈다)
#   실행 중 멈춤 (rc 4 · OUT/STOP.txt · 남은 팔 안 돎): 팔 rc ≠ 0 (시간 한도 = 124) · 로그 · 화면에 ERROR 줄 · 로그에 "Loop time of" 없음 ·
#     기대 출력 없음 · 빈 파일
#   시간 한도 (초): A · A2 = G2CP_TLONG (기본 1800 · 11-04 실측 20 s) · 나머지 = G2CP_TSHORT (기본 600 · 11-04 ≤ 1 s) — 넘으면 timeout 이
#     TERM → 30 s 뒤 KILL.  끊기면 다시 돌리지 말고 보고 (새 빈 폴더 · 1저자 승인 뒤 · 이 묶음은 재개 도구가 아니다).
#   쓰는 것 = OUT 안뿐: lmp_identity.txt (경로 · md5 · sha256 · 크기 · -h 배너 · git HEAD) · inputs.md5 · rc.txt · <팔>/{log,out}.txt ·
#     <팔>/post · <팔>/rst · outputs.md5 · (멈추면) STOP.txt.  이 폴더 (덱) 에는 아무것도 쓰지 않는다.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
die0() { echo "⛔ 실행 전 멈춤 (rc 3 · 아무 팔도 안 돎): $*" >&2; exit 3; }

[ $# -eq 2 ] || die0 "인자 = N OUT (둘) — 받은 수 $#"
N=$1; O=$2
[[ "$N" =~ ^[1-9][0-9]{0,8}$ ]] || die0 "N='$N' — 양의 정수 (ASCII 숫자 · 9 자리 안) 가 아니다"
(( N >= 200 && N % 100 == 0 )) || die0 "N=$N — 200 이상 · 100 의 배수여야 한다 (R 덱 덤프 주기 100 → setup 덤프가 step N 에 나와야 한다)"
for t in nice timeout md5sum sha256sum mktemp stat find sort xargs grep awk cut head tr date ls; do
  command -v "$t" > /dev/null 2>&1 || die0 "도구 없음: $t"
done
[ -n "${LMP:-}" ] || die0 "LMP 없음 — LIGGGHTS 3d5c00f 직렬 실행 파일 경로를 LMP 로 준다 (11-10 이 컨테이너: 실행 파일 없음 · 빌드 = 1저자 GO 뒤)"
[ -f "$LMP" ] || die0 "LMP='$LMP' — 파일이 아니다"
[ -x "$LMP" ] || die0 "LMP='$LMP' — 실행 권한 없음"
LMPABS="$(cd "$(dirname "$LMP")" && pwd)/$(basename "$LMP")"
TL=${G2CP_TLONG:-1800}; TS=${G2CP_TSHORT:-600}
[[ "$TL" =~ ^[1-9][0-9]*$ && "$TS" =~ ^[1-9][0-9]*$ ]] || die0 "시간 한도 G2CP_TLONG='$TL' · G2CP_TSHORT='$TS' — 양의 정수 (초)"

# -h 머리 줄 — 빈 임시 폴더에서 · -log none (log.liggghts 를 만들지 않는다 · lammps.cpp 310–319) · 배너 = lammps.cpp 359–361
HT=$(mktemp -d) || die0 "mktemp 실패"
( cd "$HT" && timeout -k 5 60 "$LMPABS" -log none -h ) > "$HT/h.txt" 2>&1
HRC=$?
BANNER=$(grep -m1 '^LIGGGHTS (' "$HT/h.txt")
HHEAD=$(head -c 300 "$HT/h.txt" | head -3 | tr '\n' ' ')
rm -rf "$HT"
[ "$HRC" -eq 0 ] || die0 "LMP -h rc $HRC — 실행이 안 된다 (머리: ${HHEAD:-없음})"
[ -n "$BANNER" ] || die0 "LMP -h 머리 줄에 'LIGGGHTS (' 가 없다 — LIGGGHTS 실행 파일이 아니다 (머리: ${HHEAD:-없음})"

# 덱 — 11-04 그대로 (일곱 md5 = run_40000/inputs.md5) · BW 꼴 = include R + write_restart 한 줄
REF="$HERE/run_40000/inputs.md5"
[ -f "$REF" ] || die0 "11-04 입력 기록 없음: $REF"
for f in head.inc mat.inc fresh.inc outA.inc A.liggghts A2.liggghts R.liggghts; do
  [ -f "$HERE/$f" ] || die0 "덱 없음: $f"
  want=$(awk -v f="$f" '$2 == f {print $1}' "$REF")
  have=$(md5sum < "$HERE/$f" | cut -d' ' -f1)
  [ -n "$want" ] && [ "$want" = "$have" ] || die0 "$f md5 $have ≠ 11-04 기록 ${want:-없음} — 11-04 덱이 바뀌었다"
done
[ -f "$HERE/BW.liggghts" ] || die0 "BW.liggghts 없음"
BWL=$(grep -v -e '^[[:space:]]*#' -e '^[[:space:]]*$' "$HERE/BW.liggghts")
[ "$BWL" = $'include R.liggghts\nwrite_restart ${RST}/restart_rt.bin' ] || die0 "BW.liggghts 꼴 ≠ 'include R.liggghts' + 'write_restart \${RST}/restart_rt.bin' (주석 · 빈 줄 빼고 두 줄)"
for f in compare_g2cp.py; do [ -f "$HERE/$f" ] || die0 "없음: $f"; done

# git — 리포 작업 트리 안이면 이 폴더가 깨끗해야 한다 (등록 커밋 뒤에만) · 밖이면 '리포 밖' 으로 적는다
if ! command -v git > /dev/null 2>&1; then
  GH="git 없음"
elif git -C "$HERE" rev-parse --is-inside-work-tree > /dev/null 2>&1; then
  D=$(git -C "$HERE" status --porcelain -- . 2>/dev/null)
  [ -z "$D" ] || die0 "이 폴더에 커밋 안 된 변경 · 새 파일이 있다 (등록 커밋 뒤에만 돈다): $(echo "$D" | head -3 | tr '\n' ' ')"
  GH=$(git -C "$HERE" rev-parse HEAD 2>/dev/null)
else
  GH="리포 밖"
fi

# OUT — 없거나 빈 폴더
if [ -e "$O" ]; then
  [ -d "$O" ] || die0 "OUT='$O' — 폴더가 아니다"
  [ -z "$(ls -A "$O")" ] || die0 "OUT='$O' — 비어 있지 않다 (덮어쓰지 않는다)"
fi
mkdir -p "$O" || die0 "OUT='$O' — 만들 수 없다"
O=$(cd "$O" && pwd)

stop() { echo "$*" > "$O/STOP.txt"; echo "⛔ 실행 중 멈춤 (rc 4 · 남은 팔 안 돎): $*" >&2; exit 4; }
{
  echo "lmp_path $LMPABS"
  echo "lmp_md5 $(md5sum < "$LMPABS" | cut -d' ' -f1)"
  echo "lmp_sha256 $(sha256sum < "$LMPABS" | cut -d' ' -f1)"
  echo "lmp_bytes $(stat -c %s "$LMPABS")"
  echo "lmp_banner $BANNER"
  echo "lmp_h_rc $HRC"
  echo "git_head $GH"
  echo "N $N"
  echo "timeouts long=$TL short=$TS"
  echo "date_utc $(date -u +%FT%TZ)"
} > "$O/lmp_identity.txt"
cd "$HERE" || stop "cd $HERE 실패"
{ ( cd "$(dirname "$LMPABS")" && md5sum "$(basename "$LMPABS")" ); md5sum *.inc *.liggghts run_arms.sh run_g2cp.sh compare.py compare_g2cp.py test_g2cp.py; } > "$O/inputs.md5" 2>/dev/null \
  || stop "inputs.md5 쓰기 실패"
for a in A A2 B B2 C BW BR CW CR; do mkdir -p "$O/$a/post" "$O/$a/rst" || stop "mkdir $a"; done

go() {   # go 팔 한도 lmp-인자…
  local arm=$1 lim=$2; shift 2
  local t0; t0=$(date +%s)
  nice -n 19 timeout -k 30 "$lim" "$LMPABS" -log "$O/$arm/log.txt" "$@" > "$O/$arm/out.txt" 2>&1
  local rc=$?
  echo "$arm rc $rc sec $(( $(date +%s) - t0 ))" >> "$O/rc.txt"
  if [ "$rc" -eq 124 ]; then stop "$arm rc 124 (시간 한도 $lim s 넘음)"; fi
  [ "$rc" -eq 0 ] || stop "$arm rc $rc"
  if grep -q '^ERROR' "$O/$arm/log.txt" "$O/$arm/out.txt" 2> /dev/null; then stop "$arm 로그 · 화면에 ERROR 줄"; fi
  grep -q 'Loop time of' "$O/$arm/log.txt" 2> /dev/null || stop "$arm 로그에 'Loop time of' 없음 (run 이 끝나지 않았다)"
}
need() {   # need 팔 파일…
  local arm=$1; shift
  local f
  for f in "$@"; do [ -s "$O/$arm/$f" ] || stop "$arm 기대 출력 없음 (또는 빈 파일): $f"; done
}

M1=$((N - 1))
go A  "$TL" -in A.liggghts  -var N "$N" -var NM1 "$M1" -var RA $((N + 999)) -var RST "$O/A/rst"  -var POST "$O/A/post"
need A  "rst/restart_$N.bin" "post/c_$N.txt" "post/cpre_$M1.txt" "post/atom_$N.txt"
go A2 "$TL" -in A2.liggghts -var N "$N" -var NM1 "$M1" -var R2 "$M1"         -var RST "$O/A2/rst" -var POST "$O/A2/post"
need A2 "rst/restart_$N.bin" rst/restart_cmd.bin "post/c_$N.txt" "post/cpre_$M1.txt" "post/atom_$N.txt"
go B  "$TS" -in R.liggghts  -var RFILE "$O/A/rst/restart_$N.bin"  -var POST "$O/B/post"
need B  "post/c_$N.txt" "post/atom_$N.txt"
go B2 "$TS" -in R.liggghts  -var RFILE "$O/A2/rst/restart_$N.bin" -var POST "$O/B2/post"
need B2 "post/c_$N.txt" "post/atom_$N.txt"
go C  "$TS" -in R.liggghts  -var RFILE "$O/A2/rst/restart_cmd.bin" -var POST "$O/C/post"
need C  "post/c_$N.txt" "post/atom_$N.txt"
go BW "$TS" -in BW.liggghts -var RFILE "$O/A/rst/restart_$N.bin"  -var POST "$O/BW/post" -var RST "$O/BW/rst"
need BW "post/c_$N.txt" "post/atom_$N.txt" rst/restart_rt.bin
go BR "$TS" -in R.liggghts  -var RFILE "$O/BW/rst/restart_rt.bin" -var POST "$O/BR/post"
need BR "post/c_$N.txt" "post/atom_$N.txt"
go CW "$TS" -in BW.liggghts -var RFILE "$O/A2/rst/restart_cmd.bin" -var POST "$O/CW/post" -var RST "$O/CW/rst"
need CW "post/c_$N.txt" "post/atom_$N.txt" rst/restart_rt.bin
go CR "$TS" -in R.liggghts  -var RFILE "$O/CW/rst/restart_rt.bin" -var POST "$O/CR/post"
need CR "post/c_$N.txt" "post/atom_$N.txt"

( cd "$O" && find . -mindepth 3 -maxdepth 3 -type f \( -path './*/post/*' -o -path './*/rst/*' \) -printf '%P\0' | sort -z | xargs -0 md5sum ) \
  > "$O/outputs.md5" || stop "outputs.md5 쓰기 실패"
echo "✓ 팔 아홉 끝 — 대조: python3 -I $HERE/compare_g2cp.py $O $N"
