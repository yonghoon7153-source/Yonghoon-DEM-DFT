# R 사다리 런마다 걸린 시간 (읽기만 · σ 를 열지 않는다 — 파일 시각만) · 쓰는 법: bash ~/rtimes.sh <P0|P1>
# 시작 = 런 폴더 안 가장 이른 파일 · 끝 = 팔 JSON (p2_*.json) · 근사 (분 단위)
# 비교 (3 판 어림 × 1.5 · 1저자 11-18): 저장본 짓는 첫 보통 점 런 = kgy 9,067 → 13,600 s · gabia 10,817 → 16,226 s · 나머지 점 = kgy 4,932 → 7,398 s · gabia 6,682 → 10,023 s
D=$HOME/sdcp/ca1_ladder_$1
for d in $(find "$D" -mindepth 1 -maxdepth 3 -type d -name 'L[0-9]*' 2>/dev/null | sort); do
  s=$(find "$d" -type f -printf '%T@\n' 2>/dev/null | sort -n | head -1); j=$(find "$d" -maxdepth 2 -name 'p2_*.json' -printf '%T@\n' 2>/dev/null | sort -n | head -1)
  if [ -z "$s" ]; then echo "$(basename "$d") 아직 파일 없음"
  elif [ -n "$j" ]; then echo "$(basename "$d") $(awk -v a="$j" -v b="$s" 'BEGIN{printf "%d", a-b}') s (끝 $(date -d @"${j%.*}" '+%m-%d %H:%M'))"
  else echo "$(basename "$d") 도는 중 · 시작 $(date -d @"${s%.*}" '+%m-%d %H:%M') · 지금까지 $(awk -v a="$(date +%s)" -v b="$s" 'BEGIN{printf "%d", a-b}') s"; fi
done
