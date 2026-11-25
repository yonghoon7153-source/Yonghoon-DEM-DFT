#!/usr/bin/env bash
# kgy_which_is_newer.sh — 내용이 다른 파일이 **어느 쪽이 최신인지** 판정한다.
#
# 왜 필요한가 (2026-08-07)
#   kgy 작업트리는 추적 안 되는 잔존물이라 두 가능성이 있다.
#     ① kgy 것이 **낡았다** — origin 이 그 뒤로 고쳤다 → 덮어써도 잃을 게 없다
#     ② kgy 것이 **새롭다** — 여기서 고치고 안 올렸다 → 덮어쓰면 작업이 날아간다
#   특히 tools/modelc_v3/disorder_ensemble_diffusion.py 는 **arr6 가 지금 쓰는 드라이버**다.
#   ①이면 "돌고 있는 게 낡은 드라이버"라는 뜻이라 그것대로 판정이 필요하다.
#
#   판정 근거 두 개를 나란히 놓는다:
#     · origin 이 그 파일을 마지막으로 고친 커밋 시각
#     · kgy 작업트리 파일의 mtime
#   그리고 실제 diff 를 보여 준다 — 시각만으로는 못 정한다(복사·rsync 가 mtime 을 바꾼다).
#
#   bash /tmp/newer.sh              # 요약
#   bash /tmp/newer.sh --full       # 전체 diff 까지
set -u
cd ~/Yonghoon-DEM-DFT
B=origin/claude/friendly-meitner-lldvar
LIST=${LIST:-/tmp/kgy_check/differ.txt}
FULL=${1:-}
[ -s "$LIST" ] || { echo "⛔ $LIST 가 없다 — kgy_branch_check.sh 를 먼저 돌릴 것"; exit 1; }

# ① 잃지 않게 먼저 보관 — 판정 전에 무조건 한다
mkdir -p ~/kgy_keep
rsync -Rq $(tr '\n' ' ' < "$LIST") ~/kgy_keep/ 2>/dev/null
echo "✅ 10개 원본을 ~/kgy_keep/ 에 보관했다 (판정과 무관하게 안전)"
echo

printf "%-52s %-12s %-12s %s\n" "파일" "origin수정" "kgy mtime" "줄 차이(+origin/-kgy)"
echo "──────────────────────────────────────────────────────────────────────────────────────"
while read -r f; do
  [ -n "$f" ] || continue
  oc=$(git log -1 --format='%ad' --date=short "$B" -- "$f" 2>/dev/null)
  km=$(date -r "$f" +%Y-%m-%d 2>/dev/null)
  st=$(git diff --numstat "$B" -- "$f" 2>/dev/null | awk '{print "-"$1" +"$2}')
  #   ⚠ git diff <commit> -- f 는 **commit → 작업트리** 방향이다.
  #     즉 numstat 의 added 는 "작업트리에만 있는 줄", deleted 는 "origin 에만 있는 줄".
  printf "%-52s %-12s %-12s %s\n" "$f" "${oc:-?}" "${km:-?}" "${st:-동일?}"
done < "$LIST"

echo
echo "══ 핵심 두 개의 실제 차이 (arr6 가 쓰는 드라이버 + 모든 그림이 import 하는 스타일) ══"
for f in tools/modelc_v3/disorder_ensemble_diffusion.py tools/figures/house_style.py; do
  grep -qx "$f" "$LIST" || continue
  echo; echo "───── $f ─────"
  echo "   (< = origin 에만 · > = kgy 작업트리에만)"
  git diff --no-color "$B" -- "$f" | sed -n '1,60p'
done

if [ "$FULL" = "--full" ]; then
  echo; echo "══ 나머지 전체 diff ══"
  git diff --no-color "$B" -- $(tr '\n' ' ' < "$LIST")
fi

echo
echo "판정 요령"
echo "  · diff 에 **우리가 origin 에 올린 최근 변경**(예: 계 표시명 DISP 통일, 다중 시간원점)이"
echo "    '+' 로 보이면 = kgy 것이 낡았다 → git checkout -f 로 덮어쓰면 된다."
echo "  · 반대로 kgy 에만 있는 새 기능이 보이면 그건 ~/kgy_keep/ 에 있으니 그 파일만 되살린다."