#!/usr/bin/env bash
# =============================================================================
# T12 — 갖고 있는 궤적 전부에 van Hove `G_s(r,t)` 를 돌린다 (CPU 전용).
#
# 왜: 우리는 "이게 확산 구간이 맞나" 를 한 달 내내 **MSD 기울기 하나로** 갈랐다
#   (β 문턱 → D_inc → 창 스캔 → 200 ps 판정불가). van Hove 는 **창을 안 고르고**
#   분포 모양으로 답한다 — 짧은 dt 는 진동 봉우리 하나, 긴 dt 에서 자리 간격(~3 Å)에
#   두 번째 봉우리가 자라면 진짜 홉이다.
#
# ⛔ 이 스크립트가 **못 하는 것**
#   · D 를 안 준다. "확산 중인가" 만 본다 — 정본 D 는 MSD 쪽 소관이다.
#   · 시드 간 오차막대를 안 준다. 시드별로 따로 돌려 **나란히 놓는 것**까지가 여기 몫이다.
#   · 궤적의 save_fs 를 모르면 **거부한다** (옆 aimd_results.json 에서 읽거나 --save_fs).
#     시간축이 어긋나면 lag 이 통째로 틀리는데 화면에는 정상으로 보인다.
#
# 사용:
#   bash tools/ionic/run_vanhove_sweep.sh <root> [<root2> ...]
#   bash tools/ionic/run_vanhove_sweep.sh --selftest
# =============================================================================
set -uo pipefail
PY="${PY:-python3}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOL="$HERE/aimd_jump_stats.py"
OUTROOT="${OUTROOT:-$HOME/work/vanhove}"
LAGS="${LAGS:-0.5 2 10 50}"          # ps. 200 ps 궤적이면 50 까지가 안전한 상한이다

if [ "${1:-}" = "--selftest" ]; then
  ok=1; say(){ echo "  $1 $2"; [ "$1" = "✗" ] && ok=0; return 0; }
  echo "── run_vanhove_sweep selftest ──"
  [ -f "$TOOL" ] && say "✓" "① 도구 경로가 맞다" || say "✗" "① 도구가 없다: $TOOL"
  "$PY" "$TOOL" --selftest >/dev/null 2>&1 \
    && say "✓" "② 도구 자체 selftest 통과" || say "✗" "② 도구 selftest 실패"
  T=$(mktemp -d); mkdir -p "$T/r/a" "$T/r/b"
  : > "$T/r/a/traj.xyz"; : > "$T/r/b/other.xyz"
  n=$(find "$T/r" -name traj.xyz | wc -l)
  [ "$n" = 1 ] && say "✓" "③ traj.xyz 만 고른다 (다른 xyz 는 안 건드린다)" \
                || say "✗" "③ 엉뚱한 파일을 골랐다 ($n)"
  rm -rf "$T"
  [ "$ok" = 1 ] && { echo "  ✅ selftest 통과"; exit 0; } || { echo "  ⛔ selftest 실패"; exit 1; }
fi

[ $# -ge 1 ] || { echo "사용: $0 <궤적루트> [...]"; exit 2; }
mkdir -p "$OUTROOT"
SUM="$OUTROOT/summary_$(date +%m%d_%H%M).txt"
echo "# van Hove sweep $(date)" | tee "$SUM"

n_ok=0; n_skip=0
for ROOT in "$@"; do
  ROOT="${ROOT/#\~/$HOME}"
  [ -d "$ROOT" ] || { echo "· 없음: $ROOT" | tee -a "$SUM"; continue; }
  while IFS= read -r TJ; do
    D="$(dirname "$TJ")"
    LBL="$(echo "${D#$HOME/}" | tr '/' '_')"
    # save_fs 를 모르면 건너뛴다 — 추측하면 시간축이 통째로 틀린다
    if [ ! -f "$D/aimd_results.json" ]; then
      echo "· save_fs 불명 → 건너뜀: $D" | tee -a "$SUM"; n_skip=$((n_skip+1)); continue; fi
    SZ=$(stat -c%s "$TJ" 2>/dev/null || echo 0)
    [ "$SZ" -gt 1000 ] || { echo "· 빈 궤적 → 건너뜀: $D" | tee -a "$SUM"; n_skip=$((n_skip+1)); continue; }
    echo "▶ $LBL" | tee -a "$SUM"
    "$PY" "$TOOL" --traj "$TJ" --label "$LBL" --out_dir "$OUTROOT/$LBL" \
        --lags_ps $LAGS 2>&1 | grep -aE "frames=|vanHove|⇒|!" | tee -a "$SUM"
    n_ok=$((n_ok+1))
  done < <(find "$ROOT" -name traj.xyz | sort)
done
echo "" | tee -a "$SUM"
echo "완료 $n_ok · 건너뜀 $n_skip · 요약: $SUM" | tee -a "$SUM"
echo "⛔ 판정은 사람이 한다 — 같은 계·다른 시드를 **나란히** 놓고 봐야 시드 산포가 보인다." | tee -a "$SUM"
