#!/usr/bin/env bash
#
# 데이터가 어느 폴더에 있는지.
#
# 실제로 일어난 일: 외장 SSD(T7, D:)를 WSL 이 뜬 뒤에 꽂았더니 Windows 탐색기
# 에는 D: 가 보이는데 WSL 에는 `/mnt/d` 가 없었다.  `bml` 은 데이터 폴더가
# 없다며 멈췄고 — 거기까지는 맞다 — 그러면서 이렇게 안내했다:
#
#     그 드라이브가 맞다면   mkdir -p "/mnt/d/bml-data"
#
# `/mnt/d` 가 마운트가 아니므로 그 명령은 **드라이브가 아니라 리눅스 루트에
# 같은 이름의 빈 폴더**를 만든다.  그 뒤로는 이 가드가 통과하고, 워크벤치는
# 셀 0개로 멀쩡히 뜨고, 거기 올린 .wrd 는 드라이브를 꽂아도 안 보이는 곳에
# 쌓인다.  가드가 막으려던 사고를 가드의 안내문이 시켰다.
#
# 그리고 두 번째 안내 `rm .bml/env` — 되돌리기처럼 보이지만, 외장하드를 쓰던
# 중추 서버에서는 **데이터를 통째로 갈아타는 명령**이다.  같은 파일에 적어 둔
# WORKBENCH_HOST 도 같이 날아가서, 노트북들이 그 서버에 못 닿게 된다.
#
# 사용: bash tools/tests/test_bml_data.sh     (실패 0 이면 exit 0)

set -uo pipefail

HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BML="$HERE/../bml"

pass=0
fail=0
check() {
  local what="$1" got="$2" want="$3"
  if [ "$got" = "$want" ]; then
    pass=$((pass + 1)); printf '  ok   %s\n' "$what"
  else
    fail=$((fail + 1)); printf '  FAIL %s\n           얻음: %s\n           기대: %s\n' "$what" "$got" "$want"
  fi
}
has()  { case "$2" in *"$1"*) printf 'yes' ;; *) printf 'no' ;; esac; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

BML_SOURCE_ONLY=1 . "$BML"
# 진짜 저장소의 .bml/env 를 건드리지 않는다.
REPO="$TMP/repo"; RUN_DIR="$REPO/.bml"; mkdir -p "$RUN_DIR"

echo "경로에서 드라이브 마운트 지점 뽑기"
check "/mnt/d/bml-data → /mnt/d"  "$(wsl_drive_mount_of /mnt/d/bml-data)" "/mnt/d"
check "/mnt/d 자체도 /mnt/d"      "$(wsl_drive_mount_of /mnt/d)"          "/mnt/d"
check "깊은 경로도 첫 칸만"       "$(wsl_drive_mount_of /mnt/e/a/b/c)"    "/mnt/e"
check "대문자도 받는다"           "$(wsl_drive_mount_of /mnt/D/x)"        "/mnt/D"
# /mnt/wslg 와 /mnt/wsl 은 드라이브가 아니다.  한 글자만 드라이브로 본다.
check "두 글자 이상은 드라이브가 아니다" "$(wsl_drive_mount_of /mnt/wslg/x; printf '(%s)' $?)" "(1)"
check "홈 아래는 드라이브가 아니다"      "$(wsl_drive_mount_of /home/me/data; printf '(%s)' $?)" "(1)"
check "빈 값"                            "$(wsl_drive_mount_of ''; printf '(%s)' $?)"            "(1)"

echo
echo "마운트인지 폴더인지"
check "/ 는 마운트다"          "$(path_is_mounted / && printf yes || printf no)"          "yes"
mkdir -p "$TMP/notamount"
check "그냥 만든 폴더는 아니다" "$(path_is_mounted "$TMP/notamount" && printf yes || printf no)" "no"
# 여기가 사고의 핵심이다.  `mkdir -p /mnt/d` 는 폴더를 만들지 드라이브를 붙이지
# 않는다 — [ -d ] 로는 둘이 똑같이 보인다.
check "[ -d ] 는 둘을 구분하지 못한다" "$([ -d "$TMP/notamount" ] && printf yes || printf no)" "yes"

echo
echo "드라이브가 안 붙었을 때의 안내"
# is_wsl 과 path_is_mounted 를 이 시험 안에서 갈아 끼운다.  진짜 WSL 이 아니어도
# (CI 는 리눅스다) 그 화면을 볼 수 있어야 한다.
is_wsl() { return 0; }
path_is_mounted() { return 1; }
wsl_mounted_drives() { printf '/mnt/c'; }
out="$(data_dir_help /mnt/d/bml-data 2>&1)"
check "드라이브가 없다고 말한다"        "$(has 'D: 가 WSL 에 안 붙어' "$out")"  "yes"
check "붙이는 명령을 준다"              "$(has 'mount -t drvfs D: /mnt/d' "$out")" "yes"
check "재부팅 후에도 유지하는 줄을 준다" "$(has '/etc/fstab' "$out")"           "yes"
# 이 시험이 이 파일의 이유다.  `mkdir` 라는 글자는 나온다 — "하지 마세요" 로.
# 못 박는 것은 **그것을 하라고 내놓는 줄**이 없다는 것이다.
check "만들라는 줄이 없다"              "$(has '이 자리가 맞다면' "$out")"      "no"
check "오히려 하지 말라고 말한다"       "$(has '는 하지 마세요' "$out")"        "yes"
check "왜 안 되는지도 말한다"           "$(has '빈 폴더를 만듭니다' "$out")"    "yes"
check "지금 붙어 있는 것을 보여 준다"   "$(has '/mnt/c' "$out")"                "yes"

echo
echo "드라이브는 붙어 있고 폴더만 없을 때"
path_is_mounted() { return 0; }
mkdir -p "$TMP/mounted"
out="$(data_dir_help "$TMP/mounted/bml-data" 2>&1)"
check "그때는 mkdir 가 맞다"            "$(has "mkdir -p \"$TMP/mounted/bml-data\"" "$out")" "yes"
check "drvfs 안내는 안 나온다"          "$(has 'drvfs' "$out")"                 "no"

echo
echo "윗 폴더부터 없을 때"
is_wsl() { return 1; }
out="$(data_dir_help "$TMP/nope/nope/data" 2>&1)"
check "경로를 다시 보라고 한다"         "$(has '윗 폴더부터 없습니다' "$out")"  "yes"
check "mkdir 로 덮으라고 하지 않는다"   "$(has 'mkdir -p' "$out")"              "no"

echo
echo "rm .bml/env 를 시키지 않는다"
# 되돌리기처럼 보이지만 중추 서버에서는 데이터를 갈아타는 명령이고, 같은 파일에
# 적어 둔 WORKBENCH_HOST 까지 함께 지운다 (실측: 그래서 노트북 두 대가 서버에
# 못 닿았다).  `bml data off` 는 그 한 줄만 지운다.
out="$(data_dir_help /mnt/d/bml-data 2>&1)"
check "rm 을 안내하지 않는다"           "$(has 'rm ' "$out")"                   "no"
check "bml data off 를 안내한다"        "$(has 'bml data off' "$out")"          "yes"

echo
echo "설정 파일의 다른 줄을 지키기"
printf 'WORKBENCH_HOST=0.0.0.0\nWORKBENCH_DATA=/mnt/d/bml-data\nWORKBENCH_SERVER_LAN=http://192.168.0.40:5003\n' > "$RUN_DIR/env"
need_run_dir() { :; }
WORKBENCH_DATA="/mnt/d/bml-data"; DATA_DIR="$TMP/here"; mkdir -p "$DATA_DIR"
cmd_data off >/dev/null 2>&1
check "off 는 WORKBENCH_DATA 만 지운다" "$(grep -c WORKBENCH_DATA "$RUN_DIR/env")" "0"
check "WORKBENCH_HOST 는 남는다"        "$(grep -c 'WORKBENCH_HOST=0.0.0.0' "$RUN_DIR/env")" "1"
check "LAN 주소도 남는다"               "$(grep -c 'WORKBENCH_SERVER_LAN' "$RUN_DIR/env")"   "1"

mkdir -p "$TMP/drive/uploads"
: > "$TMP/drive/uploads/a.wrd"
: > "$TMP/drive/uploads/b.wrd"
out="$(cmd_data "$TMP/drive" 2>&1)"
check "새 경로를 적는다"                "$(grep -c "WORKBENCH_DATA=$TMP/drive" "$RUN_DIR/env")" "1"
check "다른 줄은 그대로"                "$(grep -c 'WORKBENCH_HOST=0.0.0.0' "$RUN_DIR/env")"    "1"
# 몇 개가 보이는지 말한다.  0개면 그 자리가 아니라는 뜻이고, 그것을 지금
# 알아야 한다 — 띄운 다음에 빈 화면을 보고 알면 데이터가 날아간 것으로 읽힌다.
check ".wrd 개수를 말한다"              "$(has '.wrd 2개' "$out")"              "yes"

check "없는 폴더는 적지 않는다"         "$(cmd_data "$TMP/nowhere" >/dev/null 2>&1; printf '%s' $?)" "1"
check "실패했으면 값이 안 바뀐다"       "$(grep -c "WORKBENCH_DATA=$TMP/drive" "$RUN_DIR/env")" "1"

echo
echo "네트워크에 열지 말지도 같은 파일의 한 줄이다"
# 여기가 오늘 두 번째로 샌 자리다.  `.bml/env` 에 WORKBENCH_HOST=0.0.0.0 을
# 손으로 넣으라고 안내했는데, 한 줄을 넣는 가장 쉬운 방법이 `> .bml/env` 라
# WORKBENCH_DATA 가 함께 날아갔다.  한 줄만 건드린다.
HOST="127.0.0.1"
cmd_host open >/dev/null 2>&1
check "open 은 0.0.0.0 을 적는다"       "$(grep -c 'WORKBENCH_HOST=0.0.0.0' "$RUN_DIR/env")" "1"
check "데이터 줄은 그대로"              "$(grep -c "WORKBENCH_DATA=$TMP/drive" "$RUN_DIR/env")" "1"
check "LAN 주소도 그대로"               "$(grep -c 'WORKBENCH_SERVER_LAN' "$RUN_DIR/env")"   "1"
cmd_host local >/dev/null 2>&1
check "local 은 그 줄만 지운다"         "$(grep -c 'WORKBENCH_HOST' "$RUN_DIR/env")"        "0"
check "데이터 줄은 여전히 그대로"       "$(grep -c "WORKBENCH_DATA=$TMP/drive" "$RUN_DIR/env")" "1"
# 암호가 없으면 그 사실을 여는 순간에 말한다 — status 를 따로 볼 이유가 없다.
WORKBENCH_PASSWORD=""
check "암호가 없으면 그 자리에서 말한다" "$(has '암호 없이 전부 보고 고칩니다' "$(cmd_host open 2>&1)")" "yes"
WORKBENCH_PASSWORD="sekrit"
check "암호가 있으면 그 줄은 안 나온다"  "$(has '암호 없이' "$(cmd_host open 2>&1)")"        "no"

echo
printf '%s개 통과, %s개 실패\n' "$pass" "$fail"
[ "$fail" -eq 0 ]
