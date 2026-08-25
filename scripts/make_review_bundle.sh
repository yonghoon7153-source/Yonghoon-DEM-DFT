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
if [ -n "$(git status --porcelain)" ]; then
  echo "⛔ 작업 트리가 더럽다 — 번들은 커밋된 것만 싣는다.  먼저 커밋할 것:" >&2
  git status --short >&2
  exit 2
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
