#!/usr/bin/env bash
set -uo pipefail
# 끝난 STEP4 스텝만 골라 tar.gz 로 묶는다.  체인 전체를 기다릴 필요 없음 —
# 각 스텝은 종료 즉시 자기 npz/viz/state 를 쓴다.
#   bash harvest.sh                       # latest_run 의 모든 step4 산출물 (뷰어용)
#   bash harvest.sh '*chg_c0.2*'          # 0.2C 충전 것만
#   bash harvest.sh '*chg_c0.2*' --resume # + step4_grid.npz·s4state (재개용, 큼)
#   HARVEST_RUN=/path/to/run_dir bash harvest.sh …
KIT="$(cd "$(dirname "$0")" && pwd)"
RUN="${HARVEST_RUN:-$KIT/latest_run}"
[ -d "$RUN" ] || { echo "run 폴더 없음: $RUN  (HARVEST_RUN=... 로 지정)"; exit 1; }
RUN="$(cd "$RUN" && pwd)"
PAT="${1:-step4_*}"
RESUME=0; for x in "$@"; do [ "$x" = "--resume" ] && RESUME=1; done
cd "$RUN"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
LIST="$TMP/files"; : > "$LIST"
# ── geometry / provenance (STEP2 산출 — 뷰어와 감사에 필수, 작음) ──
for f in mpm_payload.json mpm_metrics.json mpm_input.json mpm_run.log; do
  [ -f "$f" ] && echo "$f" >> "$LIST"
done
ls -1 step4_run_*.log 2>/dev/null >> "$LIST"
# ── 지정 패턴의 STEP4 산출물 (npz + viz json) ──
N=0
for f in $PAT; do
  [ -e "$f" ] || continue
  case "$f" in step4_grid.npz|s4state_*) continue;; esac   # 아래 --resume 에서만
  echo "$f" >> "$LIST"; N=$((N+1))
done
[ "$N" -gt 0 ] || { echo "패턴에 맞는 산출물 0개: $PAT   (여기 있는 것:)"; ls -1 step4_*.npz step4_*.json 2>/dev/null | head -20; exit 1; }
if [ "$RESUME" = 1 ]; then
  for f in step4_grid.npz s4state_*.npz; do [ -e "$f" ] && echo "$f" >> "$LIST"; done
fi
sort -u "$LIST" -o "$LIST"
# ★모드를 파일명에 박는다 — 안 그러면 같은 초에 두 모드를 돌렸을 때 뒤엣것이
#   앞엣것을 조용히 덮어쓴다 (실측).  타임스탬프는 초 해상도라 충분치 않다.
MODE="view"; [ "$RESUME" = 1 ] && MODE="resume"
OUT="$KIT/harvest_$(basename "$RUN")_${MODE}_$(date +%Y%m%d_%H%M%S).tar.gz"
[ -e "$OUT" ] && OUT="${OUT%.tar.gz}_$$.tar.gz"   # 같은 초 재실행도 안 덮어씀
echo "── 묶는 파일 ──"; while read -r f; do printf "  %10s  %s\n" "$(du -h "$f" | cut -f1)" "$f"; done < "$LIST"
tar -czf "$OUT" -T "$LIST" || { echo "tar 실패"; exit 1; }
echo ""
echo "✓ $OUT   ($(du -h "$OUT" | cut -f1))"
[ "$RESUME" = 1 ] || echo "  (grid·state 제외 = 뷰어/분석용.  재개하려면 --resume)"
echo "  받기: scp <user>@<host>:$OUT ."
