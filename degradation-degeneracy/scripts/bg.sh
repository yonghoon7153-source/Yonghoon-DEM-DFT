#!/usr/bin/env bash
# =============================================================================
#  bg.sh — 어떤 명령이든 SSH가 끊겨도 살아남게 실행한다
#
#  사용:
#    ./scripts/bg.sh wsweep ./run.sh --mode wsweep --in results/grid_fine_v2 --nproc 32
#    ./scripts/bg.sh hc     ./run.sh --mode fit --in results/halfcell_v1 --reference halfcell --nproc 32
#             └ 로그 이름   └ 실행할 명령 그대로
#
#  왜 필요한가
#  ───────────
#  포그라운드 프로세스는 SSH가 끊기면 SIGHUP으로 함께 죽는다. 그것도 로그도
#  traceback도 없이 조용히 사라져서, 코드 버그로 오인하기 쉽다 (2026-08-06에
#  30조건 스모크가 이렇게 없어져 원인 추적에 시간을 썼다).
#
#  setsid  새 세션을 만들어 터미널에서 떼어낸다
#  nohup   SIGHUP을 무시한다
#  disown  셸의 자식 목록에서 빼서 셸 종료 시 신호가 안 가게 한다
#  </dev/null  표준입력을 끊어 백그라운드에서 입력 대기로 멈추지 않게 한다
#
#  셋을 다 쓰는 이유는 어느 하나만으로는 새는 경로가 있기 때문이다.
#  tmux 안에서 써도 무해하다 (tmux가 죽어도 살아남는다).
# =============================================================================
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

if [[ $# -lt 2 ]]; then
  echo "사용: ./scripts/bg.sh <로그이름> <명령...>" >&2
  echo "예:   ./scripts/bg.sh wsweep ./run.sh --mode wsweep --in results/grid_fine_v2 --nproc 32" >&2
  exit 1
fi

NAME="$1"; shift
LOG="${NAME%.log}.log"

# 같은 로그로 이미 뭔가 돌고 있으면 막는다 (동시 실행은 CPU를 반씩 나눠 쓴다)
if pgrep -f 'src\.(fitting|grid|weight_sweep)' >/dev/null 2>&1; then
  echo "[경고] 이미 계산 프로세스가 돌고 있습니다:" >&2
  pgrep -af 'src\.(fitting|grid|weight_sweep)' | cut -c1-80 >&2
  echo "물리 16코어를 나눠 쓰면 둘 다 느려집니다. 끝난 뒤 실행하거나," >&2
  echo "정말 동시에 돌리려면 이 스크립트 없이 직접 실행하세요." >&2
  exit 2
fi

setsid nohup "$@" > "$LOG" 2>&1 < /dev/null &
PID=$!
disown 2>/dev/null || true

sleep 3
if kill -0 "$PID" 2>/dev/null; then
  printf '실행 시작  PID %s  →  %s\n\n' "$PID" "$LOG"
else
  printf '[실패] 3초 안에 죽었습니다. 로그:\n\n' >&2
  tail -20 "$LOG" >&2
  exit 1
fi

printf '진행 확인:\n  ./scripts/watch_fit.sh <결과디렉터리> %s\n' "$LOG"
printf '로그 보기:\n  tail -f %s\n' "$LOG"
