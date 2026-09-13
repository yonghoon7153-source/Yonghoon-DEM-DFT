#!/usr/bin/env bash
#
# tools/vps-setup.sh 회귀 테스트.
#
# 이 파일이 지키는 규칙 하나: **파이프 뒤에 `grep -q` 를 쓰지 않는다.**
#
# 2026-09-13, Oracle Ubuntu 22.04 에서 이 설치본이 처음으로 실제 기계에 돌았고
# sshd 검사에서 멎었다 -- `sshd -T` 의 실효값은 `gatewayports no` 가 맞는데도.
# 원인은 도메인이 아니라 셸이다: `grep -q` 가 첫 일치에서 파이프를 닫고, 아직
# 쓸 것이 남은 `sshd` 가 SIGPIPE 로 죽고, `pipefail` 이 그 141 을 파이프라인의
# 값으로 삼는다.  찾았는데 못 찾은 것이 된다.
#
# 멎은 자리는 그나마 낫다 -- 사람이 본다.  같은 함정이 `--verify` 의 `nginx -T`
# 검사 넷과 `--check` 의 `ss` 검사에도 있었고, 그쪽은 **멈추지 않고 통과한
# 것을 실패로 적는다.**  세워 놓고 "안 섰다" 는 화면을 보며 원인을 찾게 된다.

set -uo pipefail

HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT="$HERE/../vps-setup.sh"

pass=0
fail=0

ok()   { pass=$((pass + 1)); printf '  ok   %s\n' "$1"; }
bad()  { fail=$((fail + 1)); printf '  FAIL %s\n' "$1"; }

echo "vps-setup.sh"

# --- 0. 그 함정이 실재하는지부터 보인다 ---------------------------------------
#
# 규칙만 적어 두면 다음 사람은 "왜 -q 를 못 쓰지" 로 읽고 되돌린다.  그래서
# 규칙을 재기 전에 **함정을 재현한다.**  이 단언이 언젠가 깨진다면 그때는
# 규칙이 필요 없어진 것이고, 그것도 알아야 할 일이다.
if bash -c 'set -euo pipefail; seq 1 200000 | grep -q "^5$"' 2>/dev/null; then
  bad "pipefail + grep -q 가 더 이상 거짓말하지 않는다 — 이 파일의 전제를 다시 보세요"
else
  ok "pipefail + grep -q 는 일치를 불일치로 읽는다 (그래서 아래 규칙이 있다)"
fi
if bash -c 'set -euo pipefail; seq 1 200000 | grep "^5$" >/dev/null' 2>/dev/null; then
  ok "grep ... >/dev/null 은 같은 자리에서 옳게 읽는다"
else
  bad "권장하는 형태마저 실패한다 — 이 환경의 grep 을 확인하세요"
fi

# --- 1. 설치본이 pipefail 을 켜 두는가 ----------------------------------------
#
# 켜 두는 것이 맞다 (파이프 중간의 실패를 삼키지 않는다).  다만 켜 둔 이상
# 아래 2번 규칙이 따라와야 한다 -- 이 둘은 한 짝이다.
if grep -E '^set -euo pipefail$' "$SCRIPT" >/dev/null; then
  ok "set -euo pipefail 이 켜져 있다"
else
  bad "set -euo pipefail 이 없다 — 2번 규칙의 전제가 사라졌다"
fi

# --- 2. 파이프 뒤의 grep -q 가 하나도 없는가 ----------------------------------
#
# 파일을 직접 읽는 `grep -q pattern file` 은 상류 프로세스가 없어 안전하다.
# 막는 것은 `... | grep -q` 뿐이다.
offenders="$(grep -nE '\|[[:space:]]*grep[[:space:]]+-[A-Za-z]*q' "$SCRIPT" || true)"
if [ -z "$offenders" ]; then
  ok "파이프 뒤에 grep -q 가 없다"
else
  bad "파이프 뒤에 grep -q 가 남아 있다:"
  printf '%s\n' "$offenders" | sed 's/^/         /'
fi

# --- 3. 문법 --------------------------------------------------------------
if bash -n "$SCRIPT" 2>/dev/null; then
  ok "bash -n 통과"
else
  bad "bash -n 실패"
fi

# --- 4. 줄바꿈은 LF (CLAUDE.md §0.5) ------------------------------------------
if grep -c $'\r' "$SCRIPT" >/dev/null 2>&1 && [ "$(grep -c $'\r' "$SCRIPT")" != "0" ]; then
  bad "CR 이 들어 있다 — WSL 의 bash 가 bad interpreter 로 죽는다"
else
  ok "LF 로만 저장돼 있다"
fi

printf '\n  %d 통과, %d 실패\n' "$pass" "$fail"
[ "$fail" -eq 0 ]
