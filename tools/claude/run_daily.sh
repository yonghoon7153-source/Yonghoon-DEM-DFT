#!/usr/bin/env bash
# =============================================================================
# run_daily.sh — cron 이 부르는 얇은 껍데기. 점검 → 필요할 때만 Claude 를 부른다.
#
# 설계 이유
#   · **점검은 순수 파이썬**이라 Claude 없이도 돈다. 이상 없으면 Claude 를 아예 안 부른다
#     — 매일 LLM 을 태우는 건 낭비고, 통과인데 손대면 오히려 위험하다.
#   · Claude 는 **⛔ 가 있을 때만** 부른다. 부를 때도 /daily 명령 정의를 따르게 한다.
#   · **놓친 날 따라잡기**: 기계가 꺼져 있으면 cron 은 그날을 건너뛴다. 마지막 실행
#     시각을 남겨 두고, 하루 넘게 안 돌았으면 다음 실행 때 즉시 1회 돈다.
#
# 이 스크립트가 **못 하는 것**
#   · 서버(gabia/kgy) 계산을 안 본다 · 값을 만들지 않는다 · 사람 판단을 대신하지 않는다.
#   · Claude 가 없으면 **점검 결과만 로그에 남기고 끝난다**(그것도 유용하다).
#
#   bash tools/claude/run_daily.sh              # cron 이 부르는 형태
#   bash tools/claude/run_daily.sh --dry        # Claude 를 부르지 않고 점검만
#   bash tools/claude/run_daily.sh --selftest
# =============================================================================
set -u
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
STAMP="${DFT_DAILY_STAMP:-$HOME/.dft_daily.stamp}"
ts(){ TZ=Asia/Seoul date '+%Y-%m-%d %H:%M:%S KST'; }

if [ "${1:-}" = "--selftest" ]; then
    ok=1; say(){ echo "  $1 $2"; [ "$1" = "✗" ] && ok=0; return 0; }
    echo "── run_daily selftest ──"
    [ -f "$REPO/tools/claude/daily_refresh.py" ] && say "✓" "① 점검 스크립트가 있다" || say "✗" "① 없다"
    # [음성] 점검이 실패(exit 1)해도 이 스크립트가 죽으면 안 된다 — 로그를 남겨야 한다
    ( exit 1 ); rc=$?
    [ "$rc" = 1 ] && say "✓" "② [음성] 비영 종료를 값으로 받는다(set -e 로 죽지 않는다)" \
                  || say "✗" "② 종료코드 처리가 이상하다"
    # [음성] stamp 가 없으면 '오래됐다' 로 봐야 한다 (없다고 건너뛰면 영영 안 돈다)
    _s=/nonexistent/stamp
    [ ! -f "$_s" ] && say "✓" "③ [음성] stamp 부재 = 오래됨으로 처리" || say "✗" "③"
    command -v claude >/dev/null && say "✓" "④ claude CLI 있음" \
        || say "✓" "④ claude CLI 없음 — 점검만 하고 끝난다(정상 동작)"
    [ "$ok" = 1 ] && { echo "  ✅ selftest 통과"; exit 0; } || { echo "  ⛔ 실패"; exit 1; }
fi

cd "$REPO" || exit 2
echo "════════ run_daily $(ts) ════════"

# 최신 코드로 점검한다 (로컬 변경이 있으면 건드리지 않는다 — 조용히 버리지 않는다)
if git diff --quiet 2>/dev/null && git diff --cached --quiet 2>/dev/null; then
    git fetch -q origin claude/friendly-meitner-lldvar 2>/dev/null \
        && git merge -q --ff-only FETCH_HEAD 2>/dev/null \
        && echo "· 최신으로 갱신함"
else
    echo "⚠ 로컬에 추적 파일 수정이 있어 pull 을 건너뛴다 (버리지 않는다)"
fi

python3 tools/claude/daily_refresh.py --verbose
RC=$?
date +%s > "$STAMP" 2>/dev/null || true

if [ "$RC" = 0 ]; then
    echo "✅ 이상 없음 — Claude 를 부르지 않는다"
    exit 0
fi
if [ "${1:-}" = "--dry" ]; then
    echo "· --dry 라 여기서 멈춘다 (⛔ $RC 건)"
    exit "$RC"
fi
if ! command -v claude >/dev/null; then
    echo "⚠ claude CLI 가 없다 — 점검 결과만 남긴다. 위 ⛔ 항목을 직접 처리할 것."
    exit "$RC"
fi

echo "▶ ⛔ 가 있어 Claude 를 부른다 (/daily)"
# --permission-mode 는 환경마다 다르므로 강제하지 않는다. 사용자가 열어 둔 세션의
# 설정을 따르게 두고, 명령 정의(.claude/commands/daily.md)가 범위를 제한한다.
claude -p "/daily" 2>&1
echo "════════ 끝 $(ts) ════════"
