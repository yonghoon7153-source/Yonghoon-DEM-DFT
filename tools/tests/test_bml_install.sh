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

if [ -L "$TARGET/bml" ]; then ok_ "링크를 만든다"
else bad_ "링크가 없다"; fi

if [ "$(readlink -f "$TARGET/bml")" = "$(readlink -f "$HERE/../bml")" ]; then
  ok_ "링크가 이 트리의 bml 을 가리킨다"
else
  bad_ "링크가 엉뚱한 곳을 가리킨다: $(readlink -f "$TARGET/bml")"
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

# 가이드도 같이 고쳐야 한다 — 사람이 붙여넣는 것은 문서 쪽이다.
if grep -q 'tools/bml install' "$ROOT/docs/guides/wsl-setup.md"; then
  ok_ "wsl-setup 가이드가 install 을 안내한다"
else
  bad_ "가이드에 install 단계가 없다"
fi

echo
if [ "$fail" -eq 0 ]; then
  printf '결과: %d개 통과\n' "$pass"
  exit 0
fi
printf '결과: %d개 통과, %d개 실패\n' "$pass" "$fail"
exit 1
