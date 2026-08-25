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
#   bash tools/claude/run_daily.sh --catchup    # 하루 넘게 안 돌았을 때만 실행 (셸 시작용)
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
    # [음성] --catchup 이 **최근에 돌았으면 조용히 끝나야** 한다 (매번 돌면 무의미)
    _t=$(mktemp -d); date +%s > "$_t/s"
    DFT_DAILY_STAMP="$_t/s" bash "$0" --catchup >/dev/null 2>&1
    [ "$?" = 0 ] && say "✓" "⑤ [음성] 최근 실행이면 catchup 이 조용히 끝난다" \
                 || say "✗" "⑤ catchup 이 최근 실행인데도 돌았다"
    # [음성] 오래됐으면 실제로 돌아야 한다 (조용히 넘기면 안전망이 아니다)
    echo 0 > "$_t/s"
    _o=$(DFT_DAILY_STAMP="$_t/s" bash "$0" --catchup --dry 2>&1)
    case "$_o" in *"밀린 만큼 지금 돈다"*|*"run_daily"*) say "✓" "⑤ [음성] 오래되면 실제로 돈다";;
                  *) say "✗" "⑤ 오래됐는데 안 돈다 — 안전망이 아니다";; esac
    rm -rf "$_t"
    command -v claude >/dev/null && say "✓" "④ claude CLI 있음" \
        || say "✓" "④ claude CLI 없음 — 점검만 하고 끝난다(정상 동작)"
    [ "$ok" = 1 ] && { echo "  ✅ selftest 통과"; exit 0; } || { echo "  ⛔ 실패"; exit 1; }
fi

# ── --catchup: 밀린 경우에만 돈다 ──────────────────────────────────────────
#   ⛔ 2026-08-25 — install_daily_cron.sh 가 "--catchup 으로 놓친 날을 따라잡는다" 고
#     안내하면서 정작 **구현이 없었다**(stamp 를 쓰기만 하고 읽지 않았다).
#     WSL 은 창을 닫으면 cron 데몬이 죽어 그날을 통째로 건너뛴다 — 그래서 이 경로가
#     장식이 아니라 실제 안전망이다. ~/.bashrc 에 걸어 두면 터미널 열 때 따라잡는다.
CATCHUP_AFTER=${DFT_CATCHUP_AFTER:-72000}      # 20 h. 24 h 로 두면 매일 조금씩 밀린다.
if [ "${1:-}" = "--catchup" ]; then
    if [ -f "$STAMP" ]; then
        _last=$(cat "$STAMP" 2>/dev/null || echo 0)
        _age=$(( $(date +%s) - ${_last:-0} ))
        if [ "$_age" -lt "$CATCHUP_AFTER" ]; then
            exit 0                              # 최근에 돌았다 — 조용히 끝낸다
        fi
        echo "· 마지막 실행 이후 $((_age/3600))시간 — 밀린 만큼 지금 돈다"
    else
        echo "· 실행 기록이 없다 — 처음 1회 돈다"
    fi
    # ⚠ `set -- ""` 로 쓰면 **뒤따르는 인자가 날아간다** — `--catchup --dry` 를 줘도
    #   --dry 가 사라져 Claude 를 부르게 된다. --catchup 하나만 떼어낸다.
    shift
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
