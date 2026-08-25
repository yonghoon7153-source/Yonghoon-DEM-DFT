#!/usr/bin/env bash
#
# `bml install` 이 실제로 `bml` 을 쓸 수 있게 만드는가.
#
# 실제로 일어난 일: 노트북에서 clone → `./tools/bml install` 까지 했는데도
# 다음 줄이 `bml: command not found` 였다. install 이 심볼릭 링크만 만들고
# PATH 는 사람에게 미뤘기 때문이다. 명령의 이름이 install 인 이상 셸 설정
# 한 줄까지가 이 명령의 일이다.
#
# 사용: bash tools/tests/test_bml_install.sh     (실패 0 이면 exit 0)

set -uo pipefail

HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd -P "$HERE/../.." && pwd)"
BML_SOURCE_ONLY=1 source "$HERE/../bml"

pass=0
fail=0
ok_()  { pass=$((pass + 1)); printf '  ok   %s\n' "$1"; }
bad_() { fail=$((fail + 1)); printf '  FAIL %s\n' "$1"; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "bml install"

# --- 어느 파일에 적는가 -----------------------------------------------------

# 지금 돌고 있는 셸이 아니라 로그인 셸($SHELL)이 기준이어야 한다. `bash
# tools/bml install` 로 잠깐 bash 를 썼다고 zsh 사용자의 .bashrc 에 적으면
# 새 터미널에서 여전히 안 된다.
HOME="$TMP/home" ; mkdir -p "$HOME"
if [ "$(SHELL=/usr/bin/zsh shell_rc)" = "$HOME/.zshrc" ]; then
  ok_ "zsh 사용자는 .zshrc"
else
  bad_ "zsh 사용자인데 $(SHELL=/usr/bin/zsh shell_rc) 에 적으려 한다"
fi
if [ "$(SHELL=/bin/bash shell_rc)" = "$HOME/.bashrc" ]; then
  ok_ "bash 사용자는 .bashrc"
else
  bad_ "bash 사용자인데 $(SHELL=/bin/bash shell_rc) 에 적으려 한다"
fi

# --- 실제로 등록되는가 ------------------------------------------------------

export SHELL=/bin/bash
RC="$HOME/.bashrc"
: > "$RC"
TARGET="$TMP/bin"

out="$(cmd_install "$TARGET" 2>&1)"

for n in bml bmlin bmlout; do
  if [ -x "$TARGET/$n" ]; then ok_ "$n 을 만든다"
  else bad_ "$n 이 없거나 실행할 수 없다"; fi
done

# **생성 문자열이 아니라 동작을 본다.**  경로를 어떻게 인용하느냐는 구현이고,
# 이 시험이 지켜야 하는 것은 "그 실행기가 이 트리의 bml 을 부르는가" 다.
# 문자열로 못 박아 두면 인용을 고칠 때마다 애먼 시험이 깨지고, 정작 특수문자
# 경로에서 깨지는 것은 못 잡는다.
if REAL_SEEN="$(BML_PRINT_REAL=1 "$TARGET/bml" 2>/dev/null)" \
   && [ "$REAL_SEEN" = "$(cd -P "$HERE/.." && pwd)/bml" ]; then
  ok_ "이 트리의 bml 을 가리킨다"
else
  bad_ "엉뚱한 곳을 가리킨다: ${REAL_SEEN:-(못 읽음)}"
fi

# 껍데기를 통해서도 별칭이 살아 있어야 한다.  셔뱅을 거치면 커널이 argv[0] 을
# 스크립트 경로로 갈아치우므로 `$0` 로는 알 수 없다 -- 환경변수로 넘긴다.
for n in bmlin bmlout; do
  if [ "$(BML_PRINT_INVOKED_AS=1 "$TARGET/$n" 2>/dev/null)" = "$n" ]; then
    ok_ "$n 이 자기 이름을 넘긴다"
  else
    bad_ "$n 이 이름을 안 넘긴다 — bml 과 똑같이 동작한다"
  fi
done
if grep -q 'BML_INVOKED_AS' "$HERE/../bml"; then
  ok_ "bml 이 그 이름을 읽는다"
else
  bad_ "껍데기는 이름을 넘기는데 bml 이 안 읽는다"
fi

# --- 가리키는 파일이 사라졌을 때 ---------------------------------------------
#
# 실측: 한 폴더에서 브랜치를 바꾸면 워크벤치 파일이 통째로 사라지고(§0.7),
# 심볼릭 링크였던 시절에는 화면에 `No such file or directory` 한 줄만 남았다.
# 그 문장에는 **무엇이** 없는지가 없어서, 사람은 자기가 잘못 친 줄 안다.

GONE="$TMP/gone"; mkdir -p "$GONE/bin"
( SCRIPT="$GONE/repo/tools/bml" REPO="$GONE/repo"
  write_launcher "$GONE/bin/bml" bml )

out_missing="$("$GONE/bin/bml" 2>&1)"
if [ $? -ne 0 ]; then ok_ "없으면 0 을 돌려주지 않는다"
else bad_ "파일이 없는데 성공으로 끝났다"; fi
case "$out_missing" in
  *"저장소 폴더가 없습니다"*) ok_ "폴더가 통째로 없으면 그렇게 말한다" ;;
  *) bad_ "폴더가 없는데 다른 소리를 한다: $out_missing" ;;
esac
case "$out_missing" in
  *"tools/bml install"*) ok_ "그때 할 일을 준다" ;;
  *) bad_ "무엇을 하라는 말이 없다" ;;
esac

# 저장소는 있는데 그 파일만 없는 경우 — 브랜치를 바꾼 것이다.  대처가 정반대다.
mkdir -p "$GONE/repo"
git -C "$GONE/repo" init -q -b claude/friendly-meitner-lldvar 2>/dev/null
out_branch="$("$GONE/bin/bml" 2>&1)"
case "$out_branch" in
  *"저장소는 있는데"*) ok_ "저장소는 있고 파일만 없는 경우를 가른다" ;;
  *) bad_ "두 경우를 같은 말로 덮는다: $out_branch" ;;
esac
case "$out_branch" in
  *"switch claude/battery-charge-discharge-webapp"*) ok_ "돌아가는 명령을 준다" ;;
  *) bad_ "브랜치를 되돌리는 명령이 없다" ;;
esac
case "$out_branch" in
  *"worktree"*) ok_ "둘을 같이 쓰는 방법도 알려 준다" ;;
  *) bad_ "폴더를 나누는 방법을 안 알려 준다 — 또 바꾸게 된다" ;;
esac

# --- 옛 심볼릭 링크 위에 덮어써도 저장소를 안 망친다 -------------------------
#
# `cat >` 는 링크를 따라간다.  걷어내지 않으면 저장소의 tools/bml 이 껍데기로
# 덮여 사라진다 -- 이 명령이 고치려던 사고를 이 명령이 일으킨다.
LINKY="$TMP/linky"; mkdir -p "$LINKY"
REALCOPY="$TMP/realcopy"; cp "$HERE/../bml" "$REALCOPY"
BEFORE="$(md5sum < "$REALCOPY")"
ln -sf "$REALCOPY" "$LINKY/bml"
# 다른 HOME 으로 격리한다.  cmd_install 은 rc 에 PATH 한 줄을 넣는데, 아래
# 'command -v bml' 검사는 그 rc 를 읽는다 — 여기서 넣은 줄이 $TARGET 을 가려
# 멀쩡한 검사가 깨진다.
( HOME="$TMP/otherhome"; mkdir -p "$HOME"; cmd_install "$LINKY" ) >/dev/null 2>&1
if [ "$(md5sum < "$REALCOPY")" = "$BEFORE" ]; then
  ok_ "옛 링크를 덮어써도 원본이 안 바뀐다"
else
  bad_ "install 이 저장소의 bml 을 덮어썼다"
fi

if grep -qF "$TARGET" "$RC"; then ok_ "$RC 에 PATH 한 줄을 넣는다"
else bad_ "PATH 줄을 안 넣었다 — 새 터미널에서도 command not found 다"; fi

# 그 줄이 실제로 먹는지 — 새 셸이 rc 를 읽고 나면 bml 이 잡혀야 한다.
if env -i HOME="$HOME" bash -c ". '$RC' >/dev/null 2>&1; command -v bml" \
     | grep -qF "$TARGET/bml"; then
  ok_ "그 줄을 읽은 새 셸에서 bml 이 잡힌다"
else
  bad_ "줄은 넣었는데 새 셸에서 여전히 안 잡힌다"
fi

# 지금 이 터미널에 반영하는 법을 함께 준다. rc 는 **새** 터미널에서만 읽히므로,
# 이걸 안 주면 "넣었다는데 여전히 안 된다" 가 된다.
case "$out" in
  *"지금 이 터미널"*"export PATH"*) ok_ "지금 이 터미널에 반영하는 법을 준다" ;;
  *) bad_ "rc 에만 넣고 지금 터미널은 그대로 둔다 (여전히 command not found)" ;;
esac

# --- 두 번 불러도 한 줄만 ---------------------------------------------------
cmd_install "$TARGET" >/dev/null 2>&1
count="$(grep -cF "$TARGET" "$RC")"
if [ "$count" = "1" ]; then ok_ "두 번 불러도 줄이 하나다"
else bad_ "같은 줄이 ${count}개 쌓였다"; fi

# --- 설치 절차에 실제로 들어 있는가 -----------------------------------------

# make setup 에 없으면 반드시 빠진다 — 실제로 그렇게 빠졌다.
if grep -qE '^setup:.*install-bml' "$ROOT/Makefile"; then
  ok_ "make setup 이 install-bml 을 부른다"
else
  bad_ "make setup 을 끝까지 해도 bml 명령이 안 생긴다"
fi

# doctor 가 이것을 짚어야 한다. 안 짚으면 사람은 원인을 못 찾는다.
if grep -q 'bml 명령' "$HERE/../bml"; then
  ok_ "bml doctor 가 PATH 에 bml 이 있는지 짚는다"
else
  bad_ "doctor 가 command not found 의 원인을 안 짚는다"
fi

# 가이드도 같이 고쳐야 한다 — 사람이 실제로 붙여넣는 것은 문서 쪽이다.
# 코드만 고치고 문서에 옛 처방이 남아 있으면 피해는 똑같다.
for guide in wsl-setup bml-command; do
  g="$ROOT/docs/guides/$guide.md"
  if grep -q 'tools/bml install' "$g"; then
    ok_ "$guide 가 install 을 안내한다"
  else
    bad_ "$guide 에 install 단계가 없다"
  fi
  # rc 는 새 터미널에서만 읽힌다.  지금 터미널용 export 가 붙어 있지 않으면
  # 붙여넣은 사람은 바로 다음 줄에서 command not found 를 본다.
  if grep -qF 'export PATH="$HOME/.local/bin:$PATH"' "$g"; then
    ok_ "$guide 가 지금 터미널용 export 를 함께 준다"
  else
    bad_ "$guide 가 rc 만 고치고 지금 터미널을 그대로 둔다"
  fi
done

# 남의 컴퓨터에 깔 때 install 에서 멈추면 안 된다.  그냥 `bml` 을 치면 그
# 기계에 빈 서버가 뜨고, 주소까지 localhost:5003 로 같아서 데이터가 날아간
# 것처럼 보인다.  설치 안내에 `bml use` 가 붙어 있어야 한다.
if grep -q 'bml use' "$ROOT/docs/guides/bml-command.md"; then
  ok_ "설치 안내가 bml use 까지 데려간다"
else
  bad_ "설치만 안내하고 중추 서버에 붙이는 단계가 없다 (빈 화면을 보게 된다)"
fi

# --- 떠 있는 서버가 어느 코드인지 status 가 말하는가 -------------------------
#
# 실제로 막힌 자리: 새 기능을 push 하고 상대가 bml 을 쳤는데 화면에 안 보였다.
# 그때 확인할 방법이 "코드를 열어 본다" 뿐이었다.  저장소는 최신인데 서버가 옛
# 코드일 수도, 서버는 새 코드인데 브라우저가 옛 번들을 잡고 있을 수도 있고,
# 대처가 셋 다 다르다.

if grep -q '서비스 중' "$HERE/../bml"; then
  ok_ "bml status 가 서비스 중인 커밋을 말한다"
else
  bad_ "떠 있는 서버가 어느 코드인지 status 가 말하지 않는다"
fi

# server_state 는 값을 찍지 않고 종료 코드로 답한다.  $(...) 로 받으면 항상
# 빈 문자열이라 판정이 통째로 죽는데, 화면은 아무 말도 안 해서 안 보인다.
if grep -q 'if \[ -z "$SERVER" \] && server_state; then' "$HERE/../bml"; then
  ok_ "server_state 를 종료 코드로 받는다"
else
  bad_ "server_state 를 \$(...) 로 받으면 판정이 조용히 죽는다"
fi

# 세 갈래가 모두 있어야 한다 — 하나라도 빠지면 그 경우에 아무 안내가 없다.
missing_case=""
for phrase in '어느 커밋인지 알 수 없습니다' '옛 코드가 떠 있습니다' '화면 번들이 소스보다 낡았습니다'; do
  grep -qF -- "$phrase" "$HERE/../bml" || missing_case="$missing_case '$phrase'"
done
if [ -z "$missing_case" ]; then
  ok_ "옛 서버·옛 번들·알 수 없음을 각각 구분해 말한다"
else
  bad_ "이 경우에 안내가 없다:$missing_case"
fi

# --- 실패를 실패라고 말하는가 ------------------------------------------------
#
# 예전에는 cat 과 chmod 가 실패해도 "설치" 를 출력하고 rc 파일까지 고친 뒤 0 으로
# 끝났다.  PATH 는 잡혔는데 실행기가 없는, 가장 헷갈리는 상태다 -- 실제로
# 한 기계가 `bash: .../bml: No such file or directory` 로 막혔다.

echo
echo "쓸 수 없을 때"

HOME="$TMP/home2"; mkdir -p "$HOME"; export SHELL=/bin/bash
RC2="$HOME/.bashrc"; : > "$RC2"
BAD="$TMP/nowrite"
mkdir -p "$BAD"
# root 로도 도는 시험이라 권한 대신 mv 를 실패시킨다.
mv() { return 1; }
out="$(cmd_install "$BAD" 2>&1)"; rc=$?
unset -f mv
if [ "$rc" -ne 0 ]; then ok_ "실행기를 못 쓰면 0 으로 끝나지 않는다"
else bad_ "실행기를 못 썼는데 0 으로 끝났다"; fi
case "$out" in *"설치:"*) bad_ "설치했다고 말했다" ;; *) ok_ "설치했다고 말하지 않는다" ;; esac
if [ ! -s "$RC2" ]; then ok_ "PATH 를 건드리지 않는다"
else bad_ "실행기도 없는데 rc 파일을 고쳤다"; fi
if [ -z "$(find "$BAD" -maxdepth 1 -name 'bml*' 2>/dev/null)" ]; then
  ok_ "빈/잘린 실행기를 남기지 않는다"
else
  bad_ "쓰다 만 파일이 남았다: $(find "$BAD" -maxdepth 1 -name 'bml*')"
fi

# --- 특수문자가 든 경로 ------------------------------------------------------
#
# 실행기에 `REAL="/tmp/Battery $100/repo/tools/bml"` 이 적히면 다음 실행 때
# `$1` 이 다시 펼쳐져서, 실제 파일이 있어도 엉뚱한 경로를 찾는다.

echo
echo "특수문자가 든 경로"

ODD="$TMP/Battery \$100 'lab'"
mkdir -p "$ODD/tools" "$TMP/bin3"
cat > "$ODD/tools/bml" <<'FAKE'
#!/usr/bin/env bash
printf 'REACHED %s
' "${BML_INVOKED_AS:-?}"
FAKE
chmod +x "$ODD/tools/bml"

SAVED_SCRIPT="$SCRIPT"; SAVED_REPO="$REPO"
SCRIPT="$ODD/tools/bml"; REPO="$ODD"
write_launcher "$TMP/bin3/bmlin" bmlin && wrote=0 || wrote=1
SCRIPT="$SAVED_SCRIPT"; REPO="$SAVED_REPO"

if [ "$wrote" -eq 0 ]; then ok_ "특수문자 경로에도 실행기를 쓴다"
else bad_ "특수문자 경로에서 실행기를 못 썼다"; fi

# 문자열만 보지 않고 **실제로 실행한다.**  생성 문자열 검사는 이 결함을
# 그대로 통과시켰다.
got="$("$TMP/bin3/bmlin" 2>&1)"
if [ "$got" = "REACHED bmlin" ]; then
  ok_ "그 실행기가 실제로 원본을 부른다"
else
  bad_ "실행기가 원본을 못 찾았다: $got"
fi

# --- 실행기에 엉뚱한 것이 박히지 않는가 ----------------------------------------
#
# 실행기를 만드는 heredoc 은 값을 끼워 넣어야 해서 따옴표를 못 씌운다.  본문에
# 역따옴표나 $( ) 가 들어가면 쓰는 순간 실행되어 그 출력이 파일에 박히고,
# 실행기는 그 줄들을 명령으로 읽는다.  실제로 주석의 역따옴표 한 쌍 때문에
# bml 이 실행돼 커밋 목록이 통째로 들어갔다.
echo
echo "실행기 본문"
mkdir -p "$TMP/bin6"
write_launcher "$TMP/bin6/bml" bml
if LC_ALL=C grep -q "$(printf '\033')" "$TMP/bin6/bml"; then
  bad_ "실행기에 색 문자가 박혔다 — 만드는 중에 무언가가 실행됐다"
else
  ok_ "실행기에 다른 명령의 출력이 안 박힌다"
fi
if [ "$(wc -l < "$TMP/bin6/bml")" -lt 60 ]; then
  ok_ "실행기가 한 장을 넘지 않는다"
else
  bad_ "실행기가 $(wc -l < "$TMP/bin6/bml") 줄이다 — 뭔가 섞였다"
fi

# --- 브랜치를 오가도 죽지 않는가 ----------------------------------------------
#
# 이 저장소에는 프로젝트가 둘이고 각자 다른 브랜치에 산다.  한 폴더에서 브랜치를
# 바꾸면 상대 프로젝트 파일이 통째로 사라지고, 실행기가 가리키던 파일도 없어진다.
# 실제로 그렇게 `bash: .../bml: No such file or directory` 로 막혔다.

echo
echo "브랜치를 오가도"

if command -v git >/dev/null 2>&1; then
  GITREPO="$TMP/repo"
  mkdir -p "$GITREPO/tools"
  git -C "$GITREPO" init -q -b main 2>/dev/null
  git -C "$GITREPO" config user.email t@t; git -C "$GITREPO" config user.name t
  printf '#!/usr/bin/env bash\nprintf %%s "REACHED"\n' > "$GITREPO/tools/bml"
  chmod +x "$GITREPO/tools/bml"
  git -C "$GITREPO" add -A >/dev/null; git -C "$GITREPO" commit -qm work
  # 워크벤치는 이 브랜치에, 상대 프로젝트는 main 에.
  git -C "$GITREPO" branch -q bench
  git -C "$GITREPO" rm -q tools/bml >/dev/null
  git -C "$GITREPO" commit -qm "main 에는 워크벤치가 없다"

  # 실행기는 main 체크아웃을 가리키게 만든다 (사람이 브랜치를 바꾼 상황).
  SAVED_SCRIPT="$SCRIPT"; SAVED_REPO="$REPO"; SAVED_BRANCH="$WORKBENCH_BRANCH"
  SCRIPT="$GITREPO/tools/bml"; REPO="$GITREPO"; WORKBENCH_BRANCH=bench
  mkdir -p "$TMP/bin5"
  write_launcher "$TMP/bin5/bml" bml
  SCRIPT="$SAVED_SCRIPT"; REPO="$SAVED_REPO"; WORKBENCH_BRANCH="$SAVED_BRANCH"

  # 이 상태에서는 못 찾는 것이 맞다 -- 어디에도 워크벤치가 없다.
  if "$TMP/bin5/bml" >/dev/null 2>&1; then
    bad_ "워크벤치가 없는데 뭔가를 실행했다"
  else
    ok_ "어디에도 없으면 이유를 말하고 멈춘다"
  fi
  helped="$("$TMP/bin5/bml" 2>&1)"
  case "$helped" in
    *"worktree add"*) ok_ "폴더를 나누는 명령을 알려 준다" ;;
    *) bad_ "무엇을 하라는지 안 알려 준다" ;;
  esac

  # 이제 옆에 워크벤치 작업 폴더를 만든다 -- 실행기를 다시 설치하지 않아도
  # 살아나야 한다.  브랜치를 오갈 때마다 install 을 다시 하라고 할 수는 없다.
  git -C "$GITREPO" worktree add -q "$TMP/bench" bench 2>/dev/null
  got="$("$TMP/bin5/bml" 2>&1)"
  if [ "$got" = "REACHED" ]; then
    ok_ "옆 작업 폴더의 워크벤치를 찾아 간다"
  else
    bad_ "옆에 있는데도 못 찾았다: $got"
  fi
else
  printf '  skip 브랜치 시험 (git 이 없다)\n'
fi

# 그 폴더가 다른 브랜치가 되면 "거기서 stop 하세요" 는 통하지 않는 명령이다.
if sed -n '/다른 폴더의 워크벤치/,/둘 다 띄운다/p' "$HERE/../bml" | grep -q 'kill \$(port_owner'; then
  ok_ "옛 폴더에 tools/bml 이 없으면 kill 을 알려 준다"
else
  bad_ "통하지 않는 stop 명령만 알려 준다"
fi

# --- rc 의 주석은 '이미 있다' 가 아니다 ---------------------------------------

echo
echo "rc 파일 판정"

HOME="$TMP/home3"; mkdir -p "$HOME"
RC3="$HOME/.bashrc"
TARGET3="$TMP/bin4"
printf '# old %s\n' "$TARGET3" > "$RC3"
out="$(cmd_install "$TARGET3" 2>&1)"
if grep -q "^export PATH=\"$TARGET3:" "$RC3"; then
  ok_ "주석만 있으면 PATH 를 넣는다"
else
  bad_ "주석을 '이미 있다' 로 읽고 건너뛰었다 — 새 터미널에서 여전히 bml 이 없다"
fi

# 진짜로 있으면 두 번 넣지 않는다.
before="$(grep -c "^export PATH=" "$RC3")"
out="$(cmd_install "$TARGET3" 2>&1)"
after="$(grep -c "^export PATH=" "$RC3")"
if [ "$before" = "$after" ]; then ok_ "이미 있으면 다시 넣지 않는다"
else bad_ "같은 줄을 또 넣었다 ($before -> $after)"; fi

# `$HOME` 으로 적힌 형태도 같은 줄로 본다.
HOME="$TMP/home4"; mkdir -p "$HOME/.local/bin"
RC4="$HOME/.bashrc"
printf 'export PATH="$HOME/.local/bin:$PATH"\n' > "$RC4"
out="$(cmd_install "$HOME/.local/bin" 2>&1)"
if [ "$(grep -c 'export PATH=' "$RC4")" = "1" ]; then
  ok_ "\$HOME 으로 적힌 줄도 알아본다"
else
  bad_ "\$HOME 으로 적힌 줄을 못 알아보고 또 넣었다"
fi

echo "나중에 늘어난 이름은 스스로 채운다"
# 실제로 일어난 일: `bmlonly` 를 만들었는데, 이미 install 을 한 기계에서는
# 그 이름이 영영 안 생겼다.  화면은 그 명령을 쓰라고 안내하는데 셸은
# `command not found` 를 냈다 — 안내와 실물이 어긋나는 그 자리가 가장 오래
# 붙잡는다.  `bml` 이 도는 김에 옆을 보고 채운다.
HEAL="$TMP/heal"
mkdir -p "$HEAL"
write_launcher "$HEAL/bml" bml >/dev/null 2>&1
rm -f "$HEAL/bmlonly"
( PATH="$HEAL:$PATH"; heal_launchers >/dev/null 2>&1 )
[ -x "$HEAL/bmlonly" ] && ok_ "빠진 이름을 채운다" || bad_ "빠진 이름이 그대로다"
# 남의 `bml` 옆에 우리 이름을 뿌리지 않는다 -- PATH 어딘가의 동명이인이 있다.
OTHER="$TMP/other"
mkdir -p "$OTHER"
printf '#!/bin/sh\necho not ours\n' > "$OTHER/bml"; chmod +x "$OTHER/bml"
( PATH="$OTHER:$PATH"; heal_launchers >/dev/null 2>&1 )
[ -e "$OTHER/bmlonly" ] && bad_ "남의 bml 옆에 뿌렸다" || ok_ "남의 bml 옆에는 안 뿌린다"
# 이미 다 있으면 아무 말도 안 한다 -- 매번 "설치했습니다" 가 뜨면 소음이다.
( PATH="$HEAL:$PATH"; out="$(heal_launchers 2>&1)"; [ -z "$out" ]; ) \
  && ok_ "다 있으면 조용하다" || bad_ "다 있는데도 뭔가 출력했다"

echo
if [ "$fail" -eq 0 ]; then
  printf '결과: %d개 통과\n' "$pass"
  exit 0
fi
printf '결과: %d개 통과, %d개 실패\n' "$pass" "$fail"
exit 1
