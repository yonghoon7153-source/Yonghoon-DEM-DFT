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
# uid/gid 를 빼면 root 소유로 붙어서 DB 를 못 쓴다 (실측 2026-08-30).
check "소유자 옵션까지 준다"            "$(has "uid=$(id -u),gid=$(id -g)" "$out")" "yes"
check "재부팅 후에도 유지하는 줄을 준다" "$(has '/etc/fstab' "$out")"           "yes"
# 이 시험이 이 파일의 이유다.  `mkdir` 라는 글자는 나온다 — "하지 마세요" 로.
# 못 박는 것은 **그것을 하라고 내놓는 줄**이 없다는 것이다.
check "만들라는 줄이 없다"              "$(has '이 자리가 맞다면' "$out")"      "no"
check "오히려 하지 말라고 말한다"       "$(has '는 하지 마세요' "$out")"        "yes"
check "왜 안 되는지도 말한다"           "$(has '빈 폴더를 만듭니다' "$out")"    "yes"
check "지금 붙어 있는 것을 보여 준다"   "$(has '/mnt/c' "$out")"                "yes"

echo
echo "마운트 줄은 남았는데 그 마운트가 죽었을 때"
# 실측 2026-08-30 (DESKTOP-IK8J81H): 외장하드를 뽑았다 끼우니 /proc/mounts 에
# `/mnt/d` 줄이 셋 남아 있는데 `[ -d /mnt/d ]` 는 거짓이었다.  `path_is_mounted`
# 만 보던 예전 코드는 그것을 "붙어 있다" 로 세고 **"경로를 다시 보세요"** 라고
# 했다 — 경로는 멀쩡한데.  그 자리를 여기서 못 박는다.
is_wsl() { return 0; }
path_is_mounted() { return 0; }   # 줄은 남아 있다
wsl_mounted_drives() { printf '/mnt/c'; }
# /mnt/d 는 이 컨테이너에 없다 → [ -d ] 가 거짓 = 죽은 마운트.
check "죽은 마운트는 살아 있는 것이 아니다" \
      "$(drive_is_live /mnt/d && printf yes || printf no)" "no"
out="$(data_dir_help /mnt/d/bml-data 2>&1)"
check "죽었다고 말한다"                 "$(has '마운트가 죽어 있습니다' "$out")"   "yes"
check "경로를 의심하라고 하지 않는다"   "$(has '경로를 다시 보세요' "$out")"       "no"
# 떼는 것이 먼저다.  mount 만 다시 하면 죽은 것 위에 얹히고, 그러면 소유자가
# root 로 보여 DB 를 못 쓴다 (실측: 그렇게 세 겹이 쌓였다).
check "umount 를 먼저 시킨다"           "$(has 'sudo umount /mnt/d' "$out")"       "yes"
check "떨어졌는지 확인까지 시킨다"      "$(has 'grep /mnt/d /proc/mounts' "$out")" "yes"
check "여러 겹일 수 있다고 말한다"      "$(has '여러 겹' "$out")"                  "yes"
check "그 다음에 붙인다"                "$(has 'mount -t drvfs D: /mnt/d' "$out")" "yes"
check "소유자 옵션을 빠뜨리지 않는다"   "$(has "uid=$(id -u),gid=$(id -g)" "$out")" "yes"
# 돌던 서버는 죽은 손잡이를 계속 쥔다 — 이 말이 없으면 드라이브만 고치고
# 화면은 그대로 500 이라 "안 고쳐졌다" 가 된다.
check "서버도 다시 띄우라고 한다"       "$(has '다시 띄워야' "$out")"              "yes"
check "DB 를 지우라고 하지 않는다"      "$(has 'rm ' "$out")"                      "no"
check "만들라는 줄이 없다"              "$(has '이 자리가 맞다면' "$out")"         "no"

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
check "원본 개수를 말한다"              "$(has '원본 2개' "$out")"              "yes"

# 세는 것은 충방전만이 아니다.  EIS 의 .mpr/.mps 와 GITT 파일이 같은
# uploads/ 에 들어오는데 `-name '*.wrd'` 로 세던 시절에는 임피던스만 담긴
# 외장하드가 "0개" 로 나왔다 — 백업이 안 됐다는 뜻으로 읽히는 화면이고,
# 실제로는 `tools/backup.py` 가 처음부터 전부 복사하고 있었다.
mkdir -p "$TMP/eisdrive/uploads"
: > "$TMP/eisdrive/uploads/spec.mpr"
: > "$TMP/eisdrive/uploads/spec.mps"
: > "$TMP/eisdrive/uploads/other.mpt"
out="$(cmd_data "$TMP/eisdrive" 2>&1)"
check "임피던스 원본도 센다"            "$(has '원본 3개' "$out")"              "yes"
check "0개라고 하지 않는다"             "$(has '원본 0개' "$out")"              "no"
cmd_data "$TMP/drive" >/dev/null 2>&1

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
