#!/bin/bash
# G2c′ 샌드박스 실행기 (2026-11-10 · 등록 = 메모 docs/reviews/p1_g2c_compare_definition_20261105.md §0 · §5-2 · 결과 0 건 상태에서 씀)
#   사용:  LMP=<LIGGGHTS 3d5c00f 직렬 실행 파일> bash run_g2cp.sh N OUT      (OUT = 없거나 빈 폴더 · 덮어쓰지 않는다 · 자리 = 아래 'OUT 자리')
#   대조:  python3 -I compare_g2cp.py OUT N                               (따로 · 실행기는 대조하지 않는다)
#   팔 (이 차례 · 직렬 · 한 번에 하나 · nice -n 19):
#     A  A2  B  B2  C  = 11-04 run_arms.sh 와 같은 덱 · 같은 인자
#     BW = BW.liggghts (R 덱 include + write_restart) · 입력 = A 의 주기 파일      → BR = R 덱 · 입력 = BW 가 쓴 restart_rt.bin
#     CW = BW.liggghts · 입력 = A2 의 명령 파일 (restart_cmd.bin)                 → CR = R 덱 · 입력 = CW 가 쓴 restart_rt.bin
#   실행 전 멈춤 (rc 3 · OUT 을 만들지 않는다 · 이유 = 화면 stderr):
#     인자 · N 꼴 (200 이상 · 100 의 배수 — R 덱 덤프 주기 100) · 도구 · LMP 없음 · 파일 아님 · 실행 권한 없음 · `-h` 첫 머리 줄에
#     "LIGGGHTS (" 없음 (빈 임시 폴더 · -log none) · OUT 비지 않음 · 11-04 덱 일곱 md5 ≠ run_40000/inputs.md5 · BW 덱 꼴 ·
#     git 작업 트리 안이면 이 폴더에 커밋 안 된 변경 · 새 파일 (등록 커밋 뒤에만 돈다) · OUT 자리
#   OUT 자리 (G2CPR2-05 · 실제 경로 = readlink -m 으로 본다 · 대조기 out_guard 와 같은 자리 규칙 (dry/ 는 대조기에도 · G2CPR3-02) + 기존 런 폴더 안): 샌드박스 (이) 폴더 · 그 조상 ·
#     11-04 기록 폴더 (run_40000/ · dry/) 와 그 안 · 기존 런 폴더 안 (OUT 의 조상 폴더에 런 표지 lmp_identity.txt · inputs.md5 —
#     이 실행기 · 11-04 run_arms.sh 가 OUT 에 맨 먼저 쓰는 파일) = 실행 전 멈춤.  샌드박스 폴더 안의 새 폴더는 받는다 (대조기도 읽는다).
#   실행 중 멈춤 (rc 4 · OUT/STOP.txt · 남은 팔 안 돎): 팔 rc ≠ 0 (시간 한도 = 124) · 로그 · 화면에 ERROR 줄 · 로그에 "Loop time of" 없음 ·
#     기대 출력 없음 · 빈 파일
#   시간 한도 (초): A · A2 = G2CP_TLONG (기본 1800 · 11-04 실측 20 s) · 나머지 = G2CP_TSHORT (기본 600 · 11-04 ≤ 1 s) — 넘으면 timeout 이
#     TERM → 30 s 뒤 KILL.  끊기면 다시 돌리지 말고 보고 (새 빈 폴더 · 1저자 승인 뒤 · 이 묶음은 재개 도구가 아니다).
#   사람이 멈추기 (G2CPR-08): Ctrl-C (INT) · kill -TERM <이 실행기 pid> · 터미널 닫힘 (HUP) → 도는 팔의 timeout (이 셸이 띄운 직접 자식) 에만
#     TERM → timeout 이 LIGGGHTS 에 넘김 (30 s 뒤 KILL) → 거둔 뒤 rc.txt "<팔> 신호 <INT|TERM|HUP>" · STOP.txt · rc 4 (실행 전이면 rc 3 ·
#     OUT 안 만듦).  팔 = 배경 + wait (wait 중에 신호가 바로 듣는다) · 실행기는 그 밖의 어떤 프로세스에도 신호를 보내지 않는다.
#   쓰는 것 = OUT 안뿐: lmp_identity.txt (경로 · 실제 경로 · md5 · sha256 · 크기 (stat -L) · -h 배너 · glibc · uname · git HEAD) ·
#     lmp_ldd.txt · lmp_libs.md5 (공유 라이브러리 · 기록만 · 판정 조건 아님 · G2CPR-07) · inputs.md5 · rc.txt · <팔>/{log,out}.txt ·
#     <팔>/post · <팔>/rst · outputs.md5 · (멈추면) STOP.txt.  이 폴더 (덱) 에는 아무것도 쓰지 않는다.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
TPID=''; HT=''; O=''; PHASE=pre; CUR='(팔 밖)'
die0() { [ -n "$HT" ] && rm -rf "$HT"; echo "⛔ 실행 전 멈춤 (rc 3 · 아무 팔도 안 돎): $*" >&2; exit 3; }
ischild() {   # $1 = 이 셸이 띄운 직접 자식인가 (숫자 · > 1 · 자기 · 부모 아님 · /proc 있으면 PPid = 이 셸)
  local p=$1
  [[ "$p" =~ ^[0-9]+$ ]] && [ "$p" -gt 1 ] && [ "$p" != "$$" ] && [ "$p" != "$PPID" ] || return 1
  if [ -r "/proc/$p/status" ]; then
    [ "$(awk '$1 == "PPid:" {print $2}' "/proc/$p/status" 2>/dev/null)" = "$$" ] || return 1
  fi
  return 0
}
reap() {      # 도는 자식 (timeout) 에만 TERM → 거둠 (timeout 이 LIGGGHTS 묶음에 TERM · 30 s 뒤 KILL)
  if [ -n "$TPID" ] && ischild "$TPID"; then
    kill -TERM "$TPID" 2>/dev/null
    wait "$TPID" 2>/dev/null
  fi
  TPID=''
}
onsig() {
  trap '' INT TERM HUP
  reap
  [ "$PHASE" = pre ] && die0 "신호 $1 — 사람이 멈춤 (팔 시작 전)"
  echo "$CUR 신호 $1" >> "$O/rc.txt"
  stop "신호 $1 ($CUR 중) — 사람이 멈춤 · 도는 LIGGGHTS 에 TERM (30 s 뒤 KILL) · 다시 돌리지 말고 보고 (새 빈 폴더 · 1저자 승인 뒤)"
}
trap 'onsig INT' INT
trap 'onsig TERM' TERM
trap 'onsig HUP' HUP

[ $# -eq 2 ] || die0 "인자 = N OUT (둘) — 받은 수 $#"
N=$1; O=$2
[[ "$N" =~ ^[1-9][0-9]{0,8}$ ]] || die0 "N='$N' — 양의 정수 (ASCII 숫자 · 9 자리 안) 가 아니다"
(( N >= 200 && N % 100 == 0 )) || die0 "N=$N — 200 이상 · 100 의 배수여야 한다 (R 덱 덤프 주기 100 → setup 덤프가 step N 에 나와야 한다)"
for t in nice timeout md5sum sha256sum mktemp stat find sort xargs grep awk cut head tr date ls readlink dirname; do
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
( cd "$HT" && exec timeout -k 5 60 "$LMPABS" -log none -h ) > "$HT/h.txt" 2>&1 &
TPID=$!
wait "$TPID"
HRC=$?
TPID=''
BANNER=$(grep -m1 '^LIGGGHTS (' "$HT/h.txt")
HHEAD=$(head -c 300 "$HT/h.txt" | head -3 | tr '\n' ' ')
rm -rf "$HT"
HT=''
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

# OUT 자리 (G2CPR2-05) — 실제 경로로 본다 (없는 끝 조각 · 심볼릭 링크 · .. 를 푼다) · 대조기 out_guard 와 같은 자리 규칙 (run_40000/ · dry/) + 기존 런 폴더 안
inside() { [ "$1" = "$2" ] || [ "${1#"${2%/}"/}" != "$1" ]; }    # $1 이 $2 이거나 $2 안 (실제 경로 둘)
RO=$(readlink -m -- "$O" 2>/dev/null)
RH=$(readlink -m -- "$HERE" 2>/dev/null)
[[ "$RO" == /* && "$RH" == /* ]] || die0 "OUT='$O' — 실제 경로를 알 수 없다 (readlink -m) — 자리를 확인하지 못하면 돌지 않는다"
inside "$RH" "$RO" && die0 "OUT='$O' — 샌드박스 (덱) 폴더이거나 그 조상이다 — 덱 · 기록 폴더에 쓰지 않는다"
for rec in run_40000 dry; do
  RR=$(readlink -m -- "$HERE/$rec" 2>/dev/null)
  [[ "$RR" == /* ]] || die0 "11-04 기록 폴더 $rec 의 실제 경로를 알 수 없다 (readlink -m)"
  inside "$RO" "$RR" && die0 "OUT='$O' — 11-04 기록 폴더 ($rec/) 이거나 그 안이다 — 기록 폴더에 쓰지 않는다"
done
RP=$(dirname "$RO")
while :; do
  for m in lmp_identity.txt inputs.md5; do
    [ -e "$RP/$m" ] && die0 "OUT='$O' — 기존 런 폴더 안이다 ($RP 에 런 표지 $m) — 다른 런의 출력 폴더 안에 새 런을 쓰지 않는다"
  done
  [ "$RP" = / ] && break
  RP=$(dirname "$RP")
done

# OUT — 없거나 빈 폴더
if [ -e "$O" ]; then
  [ -d "$O" ] || die0 "OUT='$O' — 폴더가 아니다"
  [ -z "$(ls -A "$O")" ] || die0 "OUT='$O' — 비어 있지 않다 (덮어쓰지 않는다)"
fi
stop() { echo "$*" > "$O/STOP.txt"; echo "⛔ 실행 중 멈춤 (rc 4 · 남은 팔 안 돎): $*" >&2; exit 4; }
mkdir -p "$O" || die0 "OUT='$O' — 만들 수 없다"
O=$(cd "$O" && pwd) || die0 "OUT='$O' — 들어갈 수 없다"
PHASE=run
{
  echo "lmp_path $LMPABS"
  echo "lmp_realpath $(readlink -f "$LMPABS" 2>/dev/null || echo '알 수 없음')"
  echo "lmp_md5 $(md5sum < "$LMPABS" | cut -d' ' -f1)"
  echo "lmp_sha256 $(sha256sum < "$LMPABS" | cut -d' ' -f1)"
  echo "lmp_bytes $(stat -L -c %s "$LMPABS")"
  echo "lmp_banner $BANNER"
  echo "lmp_h_rc $HRC"
  echo "glibc $(getconf GNU_LIBC_VERSION 2>/dev/null || echo '알 수 없음')"
  echo "uname $(uname -srm 2>/dev/null || echo '알 수 없음')"
  echo "git_head $GH"
  echo "N $N"
  echo "timeouts long=$TL short=$TS"
  echo "date_utc $(date -u +%FT%TZ)"
} > "$O/lmp_identity.txt"
# 공유 라이브러리 (G2CPR-07 — 같은 md5 실행 파일이 다른 기계에서 다른 출력을 낼 때 가릴 자료 · 기록만 · 대조기의 판정 조건 아님 — 11-04 기록에는 없다)
if command -v ldd > /dev/null 2>&1; then
  timeout 60 ldd "$LMPABS" > "$O/lmp_ldd.txt" 2>&1
  echo "ldd_rc $?" >> "$O/lmp_ldd.txt"
  awk '{for (i = 1; i <= NF; i++) if ($i ~ /^\//) print $i}' "$O/lmp_ldd.txt" | sort -u | while IFS= read -r lib; do
    [ -f "$lib" ] && md5sum "$lib"
  done > "$O/lmp_libs.md5"
else
  echo "ldd 없음" > "$O/lmp_ldd.txt"
  : > "$O/lmp_libs.md5"
fi
cd "$HERE" || stop "cd $HERE 실패"
{ ( cd "$(dirname "$LMPABS")" && md5sum "$(basename "$LMPABS")" ); md5sum *.inc *.liggghts run_arms.sh run_g2cp.sh compare.py compare_g2cp.py test_g2cp.py; } > "$O/inputs.md5" 2>/dev/null \
  || stop "inputs.md5 쓰기 실패"
for a in A A2 B B2 C BW BR CW CR; do mkdir -p "$O/$a/post" "$O/$a/rst" || stop "mkdir $a"; done

go() {   # go 팔 한도 lmp-인자… — 배경 + wait (사람 멈춤 신호가 wait 를 바로 깨우고 onsig 가 이 timeout 에만 TERM · G2CPR-08)
  local arm=$1 lim=$2; shift 2
  local t0 rc; t0=$(date +%s)
  CUR=$arm
  nice -n 19 timeout -k 30 "$lim" "$LMPABS" -log "$O/$arm/log.txt" "$@" > "$O/$arm/out.txt" 2>&1 &
  TPID=$!
  wait "$TPID"
  rc=$?
  TPID=''
  CUR='(팔 밖)'
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
