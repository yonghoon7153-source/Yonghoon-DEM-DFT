#!/usr/bin/env bash
#  독립 재현 가능한 리뷰 패키지를 만든다 (A5, R4-CX-08).
#
#  ★★ 왜 필요한가 — 지난 패키지는 **incremental bundle** 이었다.  받는 쪽 빈 저장소에서
#     `Repository lacks these prerequisite commits` 로 clone 이 실패해, Codex 가 일부
#     결함을 **소스 없이** 판정해야 했다 (그리고 그 상태로도 P1 을 찾았다).
#  ⇒ `--all` 로 **전 ref** 를 싣는다.  받는 쪽은 `git clone <bundle> repo` 한 줄이면 된다.
#
#  쓰는 법:  bash scripts/make_review_bundle.sh [출력경로]
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
cd "$ROOT"
OUT="${1:-$ROOT/../sdcp_review_$(git rev-parse --short HEAD).bundle}"

#  ⚠ 커밋 안 된 변경이 있으면 번들에 **안 들어간다** — 그것이 곧 "리뷰 대상과 다른 코드" 다.
#  ★★ 2026-08-25 첫 실사용에서 **과잉차단**이 났다 (내 게이트가 낸 7번째).  옛 판은
#    `git status --porcelain` 을 썼는데 그것은 **추적 안 되는 파일까지** 더럽다고 센다.
#    kgy 의 `tmp/`·`db/`·출력 zip 처럼 애초에 번들에 들어갈 일이 없는 지역 산출물이
#    번들 생성을 막았다.  ⇒ 두 경우를 **가른다**:
#      · 추적 파일의 수정/스테이징 = **중단**.  리뷰어가 볼 코드와 다르다.
#      · 추적 안 되는 파일 = **사람이 판단**.  대개 지역 산출물이지만, 커밋 안 한 **새 소스
#        파일**이면 번들에서 빠져 리뷰가 반쪽이 된다 (지난 R4 가 정확히 그 상태였다).
#        이름으로 짐작하지 않는다 — 목록을 보여 주고 `ALLOW_UNTRACKED=1` 로 명시하게 한다.
_DIRTY="$(git status --porcelain --untracked-files=no)"
if [ -n "$_DIRTY" ]; then
  echo "⛔ 추적 파일에 커밋 안 된 변경이 있다 — 번들은 커밋된 것만 싣는다.  먼저 커밋할 것:" >&2
  printf '%s\n' "$_DIRTY" >&2
  exit 2
fi
_UNTRACKED="$(git ls-files --others --exclude-standard)"
if [ -n "$_UNTRACKED" ]; then
  _N="$(printf '%s\n' "$_UNTRACKED" | wc -l)"
  echo "⚠ 추적 안 되는 파일 $_N 개 (번들에 **안 들어간다**):" >&2
  #  ★★ 2026-08-25 두 번째 실사용 교훈 — **목록이 길면 사람은 안 본다.**  첫 판은 kgy 에서
  #    300줄을 그대로 찍었고 (거의 전부 Quantum ESPRESSO scratch), 정작 판단해야 할 세
  #    항목이 그 안에 묻혔다.  "사람이 보고 판단하라" 는 게이트가 목록 길이 때문에
  #    형식만 남는다 = 내가 막으려던 것(안 보고 통과)의 재발.
  #  ⇒ 30개를 넘으면 **디렉터리별 집계**로 접는다.  숨기는 것이 아니다 — 최상위 경로는
  #    전부 나오고 개수가 붙으므로, 큰 덩어리가 무엇인지 한눈에 보이고 그 다음 판단이 선다.
  if [ "$_N" -le 30 ]; then
    printf '  %s\n' $_UNTRACKED >&2
  else
    echo "  (30개 초과 — 최상위 경로별로 접는다.  전체는 \`git status -u\`)" >&2
    printf '%s\n' "$_UNTRACKED" | awk -F/ '{print (NF>1 ? $1"/" : $1)}' \
      | sort | uniq -c | sort -rn | awk '{printf "  %6d  %s\n", $1, $2}' >&2
  fi
  if [ "${ALLOW_UNTRACKED:-0}" != "1" ]; then
    echo "" >&2
    echo "이 중 **커밋해야 할 새 소스**가 있으면 지금 커밋할 것.  전부 지역 산출물이면:" >&2
    echo "    ALLOW_UNTRACKED=1 bash scripts/make_review_bundle.sh" >&2
    exit 2
  fi
  echo "  → ALLOW_UNTRACKED=1 이므로 지역 산출물로 보고 계속한다." >&2
fi

git bundle create "$OUT" --all
echo "번들 → $OUT"

#  ★ **받는 쪽 검증까지 여기서 한다** (번들이 정말 단독으로 열리는가).
#    지난번 실패는 만들 때가 아니라 **열 때** 드러났다.
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
if git clone --quiet "$OUT" "$TMP/repo" 2>"$TMP/err"; then
  _n="$(git -C "$TMP/repo" rev-list --count HEAD)"
  _h="$(git -C "$TMP/repo" rev-parse --short HEAD)"
  echo "✓ 빈 저장소에서 clone 성공 — HEAD $_h · 커밋 $_n 개"
else
  echo "⛔ 단독 clone 실패 (이것이 R4-CX-08 의 증상이다):" >&2
  cat "$TMP/err" >&2
  exit 3
fi

#  ★ 리뷰어가 첫 줄부터 돌릴 수 있는 명령을 같이 적는다.
cat <<TXT

받는 쪽:
  git clone $(basename "$OUT") repo && cd repo
  git checkout $(git rev-parse --abbrev-ref HEAD)
  bash scripts/check_all.sh            # 검사기 selftest + 리포 실물
  python3 scripts/mutation_sweep_20260825.py   # 돌연변이 배터리 (수 분)
TXT
