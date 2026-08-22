#!/usr/bin/env bash
#
# 커밋마다 `docs/log.md` 에 한 줄이 남는가.
#
# 왜: 두 사람이 같은 브랜치를 쓰고 각자 **다른 Claude Code 세션**에서 일한다.
# 세션은 서로의 대화를 볼 수 없다. `git log` 는 무엇을 고쳤는지만 말하고,
# 왜 그렇게 고쳤는지 — 어떤 증상이었고 무엇을 재현했고 무엇을 일부러 안
# 했는지 — 는 대화에만 남고 그 대화는 사라진다.
#
# 그래서 커밋 제목과 log.md 항목 제목을 **같게** 쓴다. 그래야 기계가 둘을
# 짝지을 수 있고, 빠진 것이 드러난다. 이 파일이 그 짝짓기를 고정한다.
#
# 사용: bash tools/tests/test_worklog.sh     (실패 0 이면 exit 0)

set -uo pipefail

HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd -P "$HERE/../.." && pwd)"
BML_SOURCE_ONLY=1 source "$HERE/../bml"

pass=0
fail=0
ok_()   { pass=$((pass + 1)); printf '  ok   %s\n' "$1"; }
bad_()  { fail=$((fail + 1)); printf '  FAIL %s\n' "$1"; }
yes_()  { if "$@" >/dev/null 2>&1; then return 0; else return 1; fi }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
LOG="$TMP/log.md"
cat > "$LOG" <<'EOF'
# 작업 로그

## [2026-08-22] fix | 000 이 어느 층에서 끊긴 것인지까지 짚는다
본문에서 "터널을 둘로 — 망을 보고 고른다" 를 언급만 한다.

## [2026-08-21] feat | 터널을 둘로 — 망을 보고 고른다
본문.
EOF

echo "커밋 <-> docs/log.md 짝짓기"

# --- 제목에서 접두사 떼기 ---------------------------------------------------
check_body() {
  local got; got="$(commit_subject_body "$1")"
  if [ "$got" = "$2" ]; then ok_ "접두사를 뗀다: $1"
  else bad_ "접두사를 못 뗐다: $1
           얻음: $got
           기대: $2"; fi
}
check_body "fix: 터널이 안 붙는다"            "터널이 안 붙는다"
check_body "feat: 터널을 둘로 — 망을 보고 고른다" "터널을 둘로 — 망을 보고 고른다"
# 제목 안에 콜론이 또 있어도 첫 접두사만 뗀다.
check_body "docs: ADR 0014: 왜 문을 다는가"    "ADR 0014: 왜 문을 다는가"

# --- 있는 것은 있다고, 없는 것은 없다고 -------------------------------------
if yes_ log_has_entry "fix: 000 이 어느 층에서 끊긴 것인지까지 짚는다" "$LOG"; then
  ok_ "기록이 있는 커밋을 찾는다"
else
  bad_ "기록이 있는데 없다고 했다 (훅이 매번 헛경고한다)"
fi

if yes_ log_has_entry "fix: 아무도 적지 않은 커밋" "$LOG"; then
  bad_ "기록이 없는데 있다고 했다 (검사가 있으나 마나 해진다)"
else
  ok_ "기록이 없는 커밋을 잡아낸다"
fi

# 접두사가 달라도 제목이 같으면 같은 항목이다 — log.md 의 어휘(SCHEMA.md)와
# 커밋 prefix(CLAUDE.md §2)가 완전히 같지는 않기 때문이다.
if yes_ log_has_entry "update: 터널을 둘로 — 망을 보고 고른다" "$LOG"; then
  ok_ "접두사가 달라도 제목이 같으면 같은 항목으로 본다"
else
  bad_ "접두사가 다르다고 다른 항목으로 봤다"
fi

# 본문에 같은 문장이 있어도 **항목 제목**이 아니면 기록이 아니다.  이걸
# 놓치면 "언급만 해도 통과" 가 되어 검사가 무의미해진다.
cat > "$TMP/only-body.md" <<'EOF'
# 작업 로그

## [2026-08-22] fix | 다른 제목
본문에서 아무도 적지 않은 커밋 을 언급만 한다.
EOF
if yes_ log_has_entry "fix: 아무도 적지 않은 커밋" "$TMP/only-body.md"; then
  bad_ "본문에 언급만 있는데 기록으로 쳤다"
else
  ok_ "본문 언급은 기록으로 치지 않는다"
fi

# 파일이 없으면 없다고 한다 (있다고 하면 훅이 통째로 잠잔다).
if yes_ log_has_entry "fix: 무엇" "$TMP/없는파일.md"; then
  bad_ "log.md 가 없는데 기록이 있다고 했다"
else
  ok_ "log.md 가 없으면 없다고 한다"
fi

# --- 훅이 실제로 붙어 있고 같은 판정을 쓰는가 -------------------------------
HOOK="$ROOT/.githooks/commit-msg"
if [ -x "$HOOK" ]; then ok_ "commit-msg 훅이 실행 가능하다"
else bad_ "commit-msg 훅이 없거나 실행 권한이 없다"; fi

# 훅이 자기 판정을 따로 구현하면 feed 와 어긋난다 — 훅이 통과시킨 커밋을
# feed 가 빠졌다고 말하는 상태가 가장 나쁘다.
if grep -q 'log_has_entry' "$HOOK" && grep -q 'BML_SOURCE_ONLY=1' "$HOOK"; then
  ok_ "훅이 bml 의 판정을 그대로 쓴다 (구현이 하나다)"
else
  bad_ "훅이 판정을 따로 구현했다 — feed 와 어긋난다"
fi

# 기본은 막지 않는다.  막으면 상대는 --no-verify 를 습관으로 만든다.
if grep -q 'WORKBENCH_LOG_STRICT' "$HOOK" && grep -q '^exit 0$' "$HOOK"; then
  ok_ "기본은 경고, WORKBENCH_LOG_STRICT=1 일 때만 막는다"
else
  bad_ "훅이 기본으로 커밋을 막는다"
fi

# 머지·리버트·rebase 는 새 기록을 요구하지 않는다.
missing_skip=""
for word in 'Merge\ *' 'Revert\ *' 'fixup!\ *' 'rebase-merge'; do
  grep -qF -- "$word" "$HOOK" || missing_skip="$missing_skip $word"
done
if [ -z "$missing_skip" ]; then
  ok_ "머지·리버트·fixup·rebase 는 넘어간다"
else
  bad_ "이런 커밋에서도 경고한다:$missing_skip"
fi

# --- 설정이 실제로 물리는가 -------------------------------------------------
if grep -q 'core.hooksPath .githooks' "$ROOT/Makefile" \
   && grep -q 'ensure_hooks_path' "$HERE/../bml"; then
  ok_ "make setup-git 과 bml 이 훅 경로를 물린다"
else
  bad_ "훅을 만들어 두고 아무도 물리지 않는다"
fi

# 남의 설정은 덮지 않는다.
if grep -q 'current="$(git -C "$REPO" config --local core.hooksPath' "$HERE/../bml" \
   && grep -q '\[ -n "$current" \] && return 0' "$HERE/../bml"; then
  ok_ "이미 잡힌 hooksPath 는 덮지 않는다"
else
  bad_ "남이 잡아 둔 hooksPath 를 덮어쓴다"
fi

# --- 규칙이 두 미러에 모두 있는가 (CLAUDE.md == AGENTS.md) ------------------
for doc in CLAUDE.md AGENTS.md; do
  if grep -q 'bml feed' "$ROOT/$doc" 2>/dev/null; then
    ok_ "$doc 에 규칙이 있다"
  else
    bad_ "$doc 에 규칙이 없다 — 다른 세션은 이 규칙을 모른다"
  fi
done

echo
if [ "$fail" -eq 0 ]; then
  printf '결과: %d개 통과\n' "$pass"
  exit 0
fi
printf '결과: %d개 통과, %d개 실패\n' "$pass" "$fail"
exit 1
