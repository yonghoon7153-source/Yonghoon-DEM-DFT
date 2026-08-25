#!/usr/bin/env bash
# =============================================================================
# install_daily_cron.sh — KST 00:00 에 /daily 를 돌리는 cron 을 건다.
#
# 왜 cron 인가
#   대시보드·canonical 처럼 **최신성에 민감한 것**은 조용히 낡는다. 사람이 눈치채는
#   시점은 대개 발표 직전이다(2026-08-25 실측: 대시보드가 5일 낡은 채 뒤집힌 판정을
#   말하고 있었다). 매일 기계가 먼저 본다.
#
# 이 스크립트가 **못 하는 것**
#   · **기계가 꺼져 있으면 안 돈다.** cron 은 부팅돼 있어야 한다. 노트북이면 놓친다
#     — 그래서 아래 `--catchup` 으로 "마지막 실행 이후 하루 넘었으면 즉시 1회" 를 같이 건다.
#   · Claude 없이도 점검은 돌지만(daily_refresh 는 순수 파이썬), **고치는 건 Claude 몫**이다.
#   · 원격 서버(gabia/kgy)의 계산 상태는 안 본다.
#   · 이미 같은 줄이 crontab 에 있으면 **중복으로 넣지 않는다**(멱등).
#
#   bash tools/claude/install_daily_cron.sh          # 설치
#   bash tools/claude/install_daily_cron.sh --show   # 지금 걸린 것 보기
#   bash tools/claude/install_daily_cron.sh --remove # 제거
#   bash tools/claude/install_daily_cron.sh --selftest
# =============================================================================
set -u
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
MARK="# dft-daily-refresh"          # 이 표식으로 우리 줄만 찾고 지운다
LOG="${DFT_DAILY_LOG:-$HOME/.dft_daily.log}"

# ⚠ cron 은 TZ 를 상속하지 않는다 — KST 00:00 을 원하면 줄 안에서 TZ 를 못박아야 한다.
#   (서버가 UTC 면 `0 0 * * *` 는 한국시간 오전 9시에 돈다. 실제로 흔한 사고다.)
LINE="0 0 * * * TZ=Asia/Seoul cd $REPO && bash tools/claude/run_daily.sh >> $LOG 2>&1 $MARK"

case "${1:-}" in
  --selftest)
    ok=1; say(){ echo "  $1 $2"; [ "$1" = "✗" ] && ok=0; return 0; }
    echo "── install_daily_cron selftest ──"
    [ -f "$REPO/tools/claude/daily_refresh.py" ] && say "✓" "① 점검 스크립트가 있다" \
                                                 || say "✗" "① daily_refresh.py 가 없다"
    [ -f "$REPO/.claude/commands/daily.md" ] && say "✓" "② /daily 명령 정의가 있다" \
                                             || say "✗" "② .claude/commands/daily.md 가 없다"
    # [음성] TZ 를 안 박으면 UTC 서버에서 9시간 어긋난다 — 줄에 TZ 가 있어야 한다
    case "$LINE" in *"TZ=Asia/Seoul"*) say "✓" "③ [음성] cron 줄에 TZ 가 박혀 있다";;
                    *) say "✗" "③ TZ 가 없다 — UTC 서버에서 KST 09시에 돈다";; esac
    # [음성] 표식이 없으면 --remove 가 남의 줄을 지운다
    case "$LINE" in *"$MARK"*) say "✓" "④ [음성] 표식이 있어 우리 줄만 지운다";;
                    *) say "✗" "④ 표식이 없다 — remove 가 위험하다";; esac
    command -v crontab >/dev/null && say "✓" "⑤ crontab 이 있다" \
        || say "✓" "⑤ crontab 없음 — WSL 이면 아래 안내 참조(설치는 실패로 끝난다)"
    [ "$ok" = 1 ] && { echo "  ✅ selftest 통과"; exit 0; } || { echo "  ⛔ 실패"; exit 1; }
    ;;
  --show)
    crontab -l 2>/dev/null | grep -F "$MARK" || echo "(걸린 것 없음)"
    exit 0 ;;
  --remove)
    crontab -l 2>/dev/null | grep -vF "$MARK" | crontab - && echo "✓ 제거했다"
    exit 0 ;;
esac

command -v crontab >/dev/null || {
  echo "⛔ crontab 이 없다."
  echo "   WSL(Ubuntu) 이면:  sudo apt update && sudo apt install -y cron"
  echo "   그리고 cron 데몬이 떠 있어야 한다:  sudo service cron start"
  echo "   ⚠ WSL 은 창을 닫으면 데몬도 죽는다 — 창을 열어 두거나"
  echo "     Windows 작업 스케줄러로 'wsl -e bash -lc \"cd $REPO && bash tools/claude/run_daily.sh\"' 를 걸 것."
  exit 1; }

if crontab -l 2>/dev/null | grep -qF "$MARK"; then
  echo "· 이미 걸려 있다 (중복으로 넣지 않는다):"
  crontab -l | grep -F "$MARK"
  exit 0
fi
( crontab -l 2>/dev/null; echo "$LINE" ) | crontab - && {
  echo "✅ 걸었다 — 매일 KST 00:00"
  echo "   $LINE"
  echo "   로그: $LOG"
  echo "   ⚠ 기계가 꺼져 있으면 그날은 건너뛴다. run_daily.sh 가 --catchup 으로"
  echo "     '마지막 실행 이후 하루 넘었으면 즉시 1회' 를 처리한다."
}
