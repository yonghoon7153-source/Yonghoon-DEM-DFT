#!/usr/bin/env bash
# 코드 체크아웃을 **안전하게** 최신으로 — detached HEAD 에서 `git pull` 이 조용히 no-op 이
# 되는 함정을 막는다.
#
# 실사고 (2026-08-11, V100): `cd ~/dem-sk && git pull` 이 fetch 는 성공해
# `5379a772..bea55376` 을 받아왔는데 "You are not currently on a branch" 로 merge 를 안 했다.
# 작업트리는 옛 커밋 그대로였고, 다음 줄에서 `python3 .../sr01_watch.py` 가
# "No such file or directory" 로 죽었다 — 원인이 **두 줄 위**에 있어 찾기 어렵다.
# git 은 이걸 오류로 안 친다 (exit 1 이지만 fetch 는 이미 됐고 사람은 성공으로 읽는다).
#
# ⚠ setup_v100.sh 로 갱신하지 말 것 — 그건 §④에서 킷 스캐폴드를 다시 풀어 **돌고 있는
#   런의 입력을 건드릴 수 있다**.  이 스크립트는 코드만 만진다.
#
# 사용:
#   bash scripts/dem_pull.sh                 # 이 스크립트가 있는 리포를 갱신
#   bash scripts/dem_pull.sh ~/dem-sk        # 경로 지정
#   BRANCH=claude/... bash scripts/dem_pull.sh
set -uo pipefail

REPO="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
BRANCH="${BRANCH:-claude/stoic-knuth-NObVQ}"
cd "$REPO" 2>/dev/null || { echo "★ ABORT — 리포 폴더 없음: $REPO"; exit 1; }
git rev-parse --git-dir >/dev/null 2>&1 || { echo "★ ABORT — git 리포가 아님: $REPO"; exit 1; }

echo "repo    $REPO"
WAS=$(git log -1 --format='%h %s' 2>/dev/null)
echo "was     $WAS"

# ① 로컬 수정이 있으면 **아무것도 하지 않는다** (덮어쓰기가 제일 나쁜 실패다)
DIRTY=$(git status --porcelain --untracked-files=no)
if [ -n "$DIRTY" ]; then
  echo "★ ABORT — 로컬 수정이 있습니다.  커밋하거나 stash 한 뒤 다시 도세요:"
  echo "$DIRTY" | head -10 | sed 's/^/          /'
  exit 1
fi

# ② fetch (네트워크 실패는 지수 백오프로 4회)
for i in 1 2 3 4; do
  git fetch origin "$BRANCH" && break
  [ "$i" = 4 ] && { echo "★ ABORT — fetch 4회 실패 (인증/네트워크)"; exit 1; }
  echo "  fetch 실패 → $((2 ** i))s 후 재시도"; sleep $((2 ** i))
done

TARGET=$(git rev-parse "origin/$BRANCH")

# ③ 현재 상태에 맞는 최소 이동.  detached 면 detached 로 옮긴다 (브랜치를 새로 만들지
#    않는다 — V100 은 읽기 전용 소비자이고, 브랜치를 만들면 다음 사람이 여기서 커밋한다).
CUR=$(git symbolic-ref --quiet --short HEAD || true)
if [ -z "$CUR" ]; then
  echo "head    detached → detached 로 이동 (읽기 전용 체크아웃 유지)"
  git checkout --detach "$TARGET" || { echo "★ ABORT — checkout 실패"; exit 1; }
elif [ "$CUR" = "$BRANCH" ]; then
  echo "head    $CUR → ff-only merge"
  git merge --ff-only "origin/$BRANCH" || {
    echo "★ ABORT — ff 불가 (로컬 커밋이 있습니다).  수동으로 확인하세요:"
    echo "          git -C $REPO log --oneline origin/$BRANCH..HEAD"; exit 1; }
else
  echo "★ ABORT — 다른 브랜치에 있습니다 ($CUR ≠ $BRANCH).  의도한 것이면:"
  echo "          BRANCH=$CUR bash $0 $REPO"
  exit 1
fi

NOW=$(git log -1 --format='%h %s')
echo "now     $NOW"
# ④ **실제로 옮겨졌는지** 확인한다 — 이 스크립트가 존재하는 이유가 "성공처럼 보이는 no-op"
#    이므로, 성공을 주장하기 전에 HEAD 가 목표와 같은지 본다.
if [ "$(git rev-parse HEAD)" != "$TARGET" ]; then
  echo "★ ABORT — HEAD 가 origin/$BRANCH 와 다릅니다.  갱신되지 않았습니다."
  exit 1
fi
echo "✓ 최신 ($BRANCH)"
