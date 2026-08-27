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
# ⛔ 2026-08-28 (리뷰 L4) — 1차 sweep 은 **nbins 고정 + rmax 적응형**이라 bin 폭이
#   런마다 0.05–0.12 Å 로 달랐다. 그런데 우리가 주장한 차이(modelc 600→800 K 0.09 Å)가
#   딱 그 규모다 ⇒ 격자 인공물인지 안 갈랐다. 이제 **폭을 고정**하고, 매 궤적에서
#   dr 사다리를 같이 돌려 "이 궤적에서 인용 가능한 최소 차이" 를 숫자로 남긴다.
DR="${DR:-0.05}"                     # Å. 런간 비교를 하려면 전 궤적이 같은 폭이어야 한다
DR_SWEEP="${DR_SWEEP:-0.025 0.05 0.10}"   # 빈 문자열이면 사다리를 건너뛴다

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
  # ④ 배선: --dr / --dr_sweep 를 도구가 실제로 받는가 (없는 플래그면 rc=2 로 죽는다)
  "$PY" "$TOOL" --help 2>/dev/null | grep -q -- "--dr_sweep" \
    && say "✓" "④ 도구가 --dr_sweep 를 받는다" || say "✗" "④ --dr_sweep 가 도구에 없다"
  "$PY" "$TOOL" --help 2>/dev/null | grep -q -- "--dr " \
    && say "✓" "⑤ 도구가 --dr 을 받는다" || say "✗" "⑤ --dr 이 도구에 없다"
  # ⑥ 음성: DR_SWEEP 를 비우면 사다리 인자를 **안 붙여야** 한다 (빈 배열 전개)
  ( DR_SWEEP=""; _SW=(); [ -n "$DR_SWEEP" ] && _SW=(--dr_sweep $DR_SWEEP)
    [ "${#_SW[@]}" = 0 ] ) && say "✓" "⑥ DR_SWEEP 를 비우면 사다리를 건너뛴다" \
                           || say "✗" "⑥ 빈 DR_SWEEP 인데 인자가 붙는다"
  rm -rf "$T"
  [ "$ok" = 1 ] && { echo "  ✅ selftest 통과"; exit 0; } || { echo "  ⛔ selftest 실패"; exit 1; }
fi

[ $# -ge 1 ] || { echo "사용: $0 <궤적루트> [...]"; exit 2; }
mkdir -p "$OUTROOT"
SUM="$OUTROOT/summary_$(date +%m%d_%H%M).txt"
# ⛔ 2026-08-28 (리뷰 L4) — 1차 33궤적 sweep 은 **어느 파일을 읽었는지 기록이 없다.**
#   요약 텍스트에 라벨만 남아서, 나중에 "그 표의 그 줄이 어느 궤적이냐" 를 못 되짚는다.
#   ⇒ 궤적마다 경로·SHA256·프레임수·명령줄·종료코드를 JSONL 한 줄로 남긴다.
MAN="$OUTROOT/manifest_$(date +%m%d_%H%M).jsonl"
echo "# van Hove sweep $(date)" | tee "$SUM"
echo "# manifest: $MAN" | tee -a "$SUM"

n_ok=0; n_fail=0; n_skip=0
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
    # ⛔ 2026-08-28 (리뷰 L · P0-1) — 첫 판은 출력을 grep 으로 거르고 **무조건 n_ok++** 했다.
    #   분석기가 traceback 으로 죽어도 "완료" 로 세어졌다 (실제로 `edges` NameError 가 있었다).
    #   ⇒ 전체 출력을 파일로 받고, **종료코드로** 성공을 센다. traceback 은 요약에 남긴다.
    _RAW="$OUTROOT/$LBL.stdout"; mkdir -p "$OUTROOT"
    _SW=(); [ -n "$DR_SWEEP" ] && _SW=(--dr_sweep $DR_SWEEP)
    "$PY" "$TOOL" --traj "$TJ" --label "$LBL" --out_dir "$OUTROOT/$LBL" \
        --lags_ps $LAGS --dr "$DR" "${_SW[@]}" > "$_RAW" 2>&1
    _RC=$?
    grep -aE "frames=|vanHove|불변식|dr 사다리|⇒|!" "$_RAW" | tee -a "$SUM"
    # ★ 되짚을 수 있게 남긴다. sha256 은 큰 궤적에서 몇 초 걸리지만 분석보다 훨씬 싸다.
    _SHA=$(sha256sum "$TJ" 2>/dev/null | cut -c1-64); _SHA="${_SHA:-unknown}"
    _NFR=$(grep -ac "^Lattice\|^ *[0-9]\+ *$" "$TJ" 2>/dev/null || echo 0)
    printf '{"label":"%s","traj":"%s","sha256":"%s","bytes":%s,"frames_hint":%s,' \
           "$LBL" "$TJ" "$_SHA" "${SZ:-0}" "${_NFR:-0}" >> "$MAN"
    printf '"lags_ps":"%s","dr_A":"%s","dr_sweep":"%s","rc":%s,"at":"%s"}\n' \
           "$LAGS" "$DR" "$DR_SWEEP" "$_RC" "$(date -Is)" >> "$MAN"
    if [ "$_RC" -ne 0 ]; then
      echo "  ⛔ 분석기 실패 (rc=$_RC) — 꼬리:" | tee -a "$SUM"
      tail -6 "$_RAW" | sed 's/^/     /' | tee -a "$SUM"
      n_fail=$((n_fail+1))
    else
      n_ok=$((n_ok+1))
    fi
  done < <(find "$ROOT" -name traj.xyz | sort)
done
echo "" | tee -a "$SUM"
echo "완료 $n_ok · **실패 $n_fail** · 건너뜀 $n_skip · 요약: $SUM" | tee -a "$SUM"
echo "⛔ 판정은 사람이 한다 — 같은 계·다른 시드를 **나란히** 놓고 봐야 시드 산포가 보인다." | tee -a "$SUM"
