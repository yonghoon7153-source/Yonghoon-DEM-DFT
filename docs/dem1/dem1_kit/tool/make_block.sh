#!/bin/bash
# make_block.sh — 스크립트를 DEM1 붙여넣기 블록으로 (cat > ~/X.sh <<'X_EOF' … + md5 게이트 줄)
#   bash make_block.sh path/X.sh ["게이트 통과 뒤 실행할 명령"]   → path/X_block.txt
#   기본 명령 = "bash ~/X.sh" (사용법만 출력) · th_grid 는 "bash ~/th_grid.sh gen"
S=$1; [ -s "$S" ] || { echo "사용법: bash make_block.sh path/X.sh [명령]"; exit 1; }
N=$(basename "$S"); M=$(echo "${N%.*}" | tr 'a-z' 'A-Z' | tr -c 'A-Z0-9\n' '_'); M=${M%_}; [ "$N" = th_grid.sh ] && M=TH; M=${M}_EOF
CMD=${2:-bash ~/$N}; OUT=${S%.*}_block.txt; BAD=0
bash -n "$S" || { echo "⛔ bash -n 실패"; BAD=1; }
[ "$(tr -cd '\041' < "$S" | wc -c)" = 0 ] || { echo "⛔ 느낌표 $(tr -cd '\041' < "$S" | wc -c)개 (인터랙티브 붙여넣기에서 history 확장됨)"; grep -n "$(printf '\041')" "$S" | head -5; BAD=1; }
[ "$(tr -cd '\t' < "$S" | wc -c)" = 0 ] || { echo "⛔ 탭 문자 있음"; BAD=1; }
[ "$(tr -cd '\r' < "$S" | wc -c)" = 0 ] || { echo "⛔ CR(윈도 줄바꿈) 있음"; BAD=1; }
grep -qx "$M" "$S" && { echo "⛔ 본문에 구분자 줄 $M 이 있음"; BAD=1; }
[ $BAD = 0 ] || exit 1
H=$(md5sum < "$S" | cut -c1-32)
{ echo "cat > ~/$N <<'$M'"; cat "$S"; echo "$M"
  echo "if [ \"\$(md5sum < ~/$N | cut -c1-32)\" = $H ]; then $CMD; else echo \"⛔ 붙여넣기가 깨짐 (md5 다름) — 아무것도 안 함\"; fi"; } > "$OUT"
echo "✅ $OUT · md5 $H · $(wc -l < "$OUT")줄 $(wc -c < "$OUT")바이트 · 최장 줄 $(awk '{ if (length($0) > m) m = length($0) } END { print m }' "$S")"
