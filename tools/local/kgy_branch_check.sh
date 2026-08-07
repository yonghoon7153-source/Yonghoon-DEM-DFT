#!/usr/bin/env bash
# kgy_check.sh — 브랜치 전환 전에 **덮어써도 되는지** 파일 단위로 확인한다.
#   kgy 는 HEAD 가 claude/stoic-knuth-NObVQ 인데 작업트리에 우리 DFT 트리(db/kb/tools)가
#   **추적 안 된 채** 들어 있다. checkout 이 "덮어쓰게 된다"며 거부하는 게 그것 때문이다.
#   내용이 브랜치와 같으면 덮어써도 잃을 게 없고, 다르면 그건 kgy 에만 있는 작업이다.
set -u
cd ~/Yonghoon-DEM-DFT
B=origin/claude/friendly-meitner-lldvar
git fetch -q origin claude/friendly-meitner-lldvar
OUT=/tmp/kgy_check
mkdir -p $OUT

git ls-tree -r --name-only $B -- db kb tools | sort > $OUT/in_branch.txt
find db kb tools -type f 2>/dev/null | sed 's|^\./||' | sort > $OUT/in_worktree.txt

: > $OUT/differ.txt
while read -r f; do
  [ -f "$f" ] || continue
  a=$(git hash-object "$f" 2>/dev/null)
  b=$(git rev-parse "$B:$f" 2>/dev/null)
  [ "$a" = "$b" ] || echo "$f" >> $OUT/differ.txt
done < $OUT/in_branch.txt

comm -13 $OUT/in_branch.txt $OUT/in_worktree.txt > $OUT/only_here.txt

echo "════════════════════════════════════════════════════════"
echo " 브랜치에 있는 파일          : $(wc -l < $OUT/in_branch.txt)"
echo " 그중 내용이 **다른** 것     : $(wc -l < $OUT/differ.txt)   ← 0 이면 덮어써도 안전"
echo " 작업트리에만 있는 것        : $(wc -l < $OUT/only_here.txt)  ← 이건 checkout 해도 살아남는다"
echo "════════════════════════════════════════════════════════"
if [ -s $OUT/differ.txt ]; then
  echo; echo "⚠ 내용이 다른 파일 (덮어쓰면 잃는다):"; sed 's/^/   /' $OUT/differ.txt | head -40
  echo; echo "   → 먼저 보관:  mkdir -p ~/kgy_keep && rsync -R \$(cat $OUT/differ.txt | tr '\n' ' ') ~/kgy_keep/"
else
  echo; echo "✅ 다른 파일 없음 — 아래를 그대로 실행하면 된다:"
  echo "     git checkout -f claude/friendly-meitner-lldvar"
  echo "     git pull origin claude/friendly-meitner-lldvar"
fi
echo; echo "작업트리에만 있는 것 (checkout 후에도 남는다):"; sed 's/^/   /' $OUT/only_here.txt | head -20
