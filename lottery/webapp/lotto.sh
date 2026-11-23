#!/usr/bin/env bash
# lotto — 복권 번호 연구소 웹앱 한 줄 실행 (본체 webapp/bms.sh 를 본떴다)
#
#   venv 확인 → 의존성 동기화 → 빈 포트 찾기 → 서버 기동
#
# 쓰기:
#   lottery/webapp/lotto.sh              # 이 기계에서만 (127.0.0.1)
#   lottery/webapp/lotto.sh --share      # 같은 망의 다른 사람도 (0.0.0.0) — 인증이 없다, 사설망에서만
#   lottery/webapp/lotto.sh --port 5123  # 포트 지정
#   lottery/webapp/lotto.sh --stop       # 떠 있는 것을 내린다
#
# git 은 건드리지 않는다 (bms.sh 와 다른 점) — 이 앱은 results/analysis.json 을 읽을 뿐이고,
# 데이터 갱신은 fetch_data.py → build_results.py 를 사람이 돌린다.
set -uo pipefail

HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
VENV="$HERE/../.venv-webapp"
PIDF="$VENV/.lotto.pid"
PORT=""
SHARE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --port)  # 값이 없으면 shift 2 가 실패해 같은 인자를 영원히 돌았다 (자체 리뷰 소)
      [[ $# -ge 2 && -n "$2" ]] || { echo "--port 에 포트 번호가 필요하다 (예: --port 5071)" >&2; exit 2; }
      PORT="$2"; shift 2 ;;
    --share) SHARE=1; shift ;;
    --stop)
      if [[ -f "$PIDF" ]] && kill -0 "$(cat "$PIDF")" 2>/dev/null; then
        kill "$(cat "$PIDF")" && rm -f "$PIDF" && echo "내렸다."
      else
        echo "떠 있는 서버가 없다."
      fi
      exit 0 ;;
    -h|--help) sed -n '2,13p' "$0"; exit 0 ;;
    *) echo "모르는 옵션: $1 (--help)"; exit 2 ;;
  esac
done

if [[ ! -f "$HERE/../results/analysis.json" ]]; then
  echo "lottery/results/analysis.json 이 없다 — 먼저 python lottery/build_results.py 를 돌린다."
  exit 1
fi

if [[ ! -x "$VENV/bin/python" ]]; then
  echo "venv 만드는 중: $VENV"
  python3 -m venv "$VENV" || { echo "venv 를 만들지 못했다 (python3-venv 패키지?)"; exit 1; }
fi
"$VENV/bin/pip" install --quiet -r "$HERE/requirements.txt" || { echo "의존성 설치 실패"; exit 1; }

if [[ -z "$PORT" ]]; then
  PORT=5070
  while (echo > "/dev/tcp/127.0.0.1/$PORT") 2>/dev/null; do PORT=$((PORT + 1)); done
fi
HOST=127.0.0.1
[[ "$SHARE" == 1 ]] && HOST=0.0.0.0

echo "복권 번호 연구소 → http://127.0.0.1:$PORT"
if [[ "$SHARE" == 1 ]]; then
  IP="$(hostname -I 2>/dev/null | awk '{print $1}')"
  [[ -n "$IP" ]] && echo "같은 망에서는 → http://$IP:$PORT  (인증 없음 — 공인 IP·포트포워딩에 걸지 않는다)"
fi
cd "$HERE" || exit 1
WEBAPP_HOST="$HOST" WEBAPP_PORT="$PORT" "$VENV/bin/python" app.py &
echo $! > "$PIDF"
wait
