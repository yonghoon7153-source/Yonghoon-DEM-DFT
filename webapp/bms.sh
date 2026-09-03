#!/usr/bin/env bash
# bms — Battery Materials Lab 위키 뷰어 한 줄 실행
#
#   git 갱신 → venv 확인 → 의존성 동기화 → 빈 포트 찾기 → 서버 기동
#
# 설치 (한 번만) — 경로는 **이 저장소를 받아 둔 자리**다. 이름이 꼭
# Yonghoon-DEM-DFT 일 필요는 없다 (~/bms 로 받아 둔 기계도 있다):
#   echo "alias bms='<저장소>/webapp/bms.sh'" >> ~/.bashrc && . ~/.bashrc
#   예)  echo "alias bms='~/bms/webapp/bms.sh'" >> ~/.bashrc && . ~/.bashrc
#
# 쓰기:
#   bms              # 갱신하고 띄운다 (이 기계에서만 보인다)
#   bms --share      # 같은 망의 다른 사람도 볼 수 있게 (0.0.0.0 바인딩)
#   bms --no-pull    # 갱신 없이 띄운다 (오프라인·작업 중)
#   bms --port 5123  # 포트 지정
#   bms --stop       # 떠 있는 것을 내린다
#
# 설계 메모
#   · **브랜치를 하드코딩하지 않는다.** 현재 체크아웃된 브랜치를 따라간다 —
#     작업 브랜치 이름의 정본은 저장소 루트 `CLAUDE.md` 하드룰 1 하나이고,
#     사본을 만들면 이름이 바뀔 때 갈라진다 (2026-08-20 에 8곳이 그랬다).
#   · **git 이 갈라져 있으면 멈추지 않고 알린 뒤 그대로 띄운다.** 뷰어를 못
#     여는 것보다 "지금 보고 있는 것이 최신이 아니다" 를 아는 편이 낫다.
#     자동 merge·reset 은 하지 않는다 — 남의 커밋을 조용히 버릴 수 있다.
set -uo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="$ROOT/.venv"
PIDF="$ROOT/.venv/.bms.pid"
DO_PULL=1
PORT=""
SHARE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-pull) DO_PULL=0; shift ;;
    --port)    PORT="${2:-}"; shift 2 ;;
    --share)   SHARE=1; shift ;;
    --stop)
      if [[ -f "$PIDF" ]] && kill -0 "$(cat "$PIDF")" 2>/dev/null; then
        kill "$(cat "$PIDF")" && rm -f "$PIDF"
        echo "· 내렸다"
      else
        echo "· 떠 있는 bms 가 없다"
      fi
      exit 0 ;;
    -h|--help) sed -n '2,25p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "모르는 인자: $1 (--help)" >&2; exit 2 ;;
  esac
done

cd "$ROOT" || exit 1

# ── 1. 이미 떠 있으면 그것을 알린다 (두 벌 띄우지 않는다) ──────────────────
if [[ -f "$PIDF" ]] && kill -0 "$(cat "$PIDF")" 2>/dev/null; then
  echo "· 이미 떠 있다 (pid $(cat "$PIDF")). 내리려면: bms --stop"
  [[ -f "$ROOT/.venv/.bms.url" ]] && echo "  → $(cat "$ROOT/.venv/.bms.url")"
  exit 0
fi

# ── 2. git 갱신 — 갈라져 있으면 손대지 않고 알리기만 ──────────────────────
# `.git` 은 **파일일 수도 있다** — worktree 에서는 `gitdir: …` 한 줄이 든 파일이다.
# `-d` 로 물으면 worktree 에서 이 블록이 통째로 건너뛰어지고, 뷰어가 조용히 옛
# 커밋을 계속 띄운다 (2026-09-03 에 실측: `· 브랜치:` 줄이 아예 안 찍혔다).
if [[ $DO_PULL -eq 1 ]] && [[ -e "$ROOT/.git" ]]; then
  BR="$(git rev-parse --abbrev-ref HEAD 2>/dev/null)"
  echo "· 브랜치: $BR"
  if git fetch --quiet origin "$BR" 2>/dev/null; then
    AHEAD=$(git rev-list --count "origin/$BR..HEAD" 2>/dev/null || echo 0)
    BEHIND=$(git rev-list --count "HEAD..origin/$BR" 2>/dev/null || echo 0)
    if   [[ "$AHEAD" == "0" && "$BEHIND" == "0" ]]; then echo "· 최신"
    elif [[ "$AHEAD" == "0" ]]; then
      git merge --ff-only "origin/$BR" --quiet && echo "· $BEHIND 커밋 당겼다"
    else
      echo "⚠ 로컬에 push 안 된 커밋 $AHEAD 개가 있어 자동 갱신을 건너뛴다"
      echo "  (원격에는 $BEHIND 개 더 있다). 확인:"
      echo "    git log --oneline origin/$BR..HEAD"
      echo "  합치려면: git pull --rebase origin $BR"
    fi
  else
    echo "⚠ fetch 실패 — 네트워크? 지금 트리 그대로 띄운다"
  fi
fi

# ── 3. venv + 의존성 (requirements 가 바뀐 때만 설치) ─────────────────────
REQ="$ROOT/webapp/requirements.txt"
[[ -f "$REQ" ]] || { echo "✗ $REQ 가 없다" >&2; exit 1; }
if [[ ! -x "$VENV/bin/python" ]]; then
  echo "· venv 를 만든다"
  python3 -m venv "$VENV" || { echo "✗ venv 생성 실패 (python3-venv 설치 필요?)" >&2; exit 1; }
fi
STAMP="$VENV/.bms.reqs.sha256"
NOW="$(sha256sum "$REQ" | cut -d' ' -f1)"
if [[ ! -f "$STAMP" ]] || [[ "$(cat "$STAMP")" != "$NOW" ]]; then
  echo "· 의존성 동기화"
  "$VENV/bin/pip" install --quiet --upgrade pip >/dev/null 2>&1
  if "$VENV/bin/pip" install --quiet -r "$REQ"; then
    echo "$NOW" > "$STAMP"
  else
    echo "✗ pip install 실패" >&2; exit 1
  fi
fi

# ── 4. 빈 포트 ────────────────────────────────────────────────────────────
if [[ -z "$PORT" ]]; then
  PORT="$("$VENV/bin/python" - <<'PY'
import socket
for p in range(5100, 5200):          # 저쪽 브랜치 webapp(5001·5057)과 안 겹치게
    s = socket.socket()
    try:
        s.bind(("127.0.0.1", p)); print(p); break
    except OSError:
        continue
    finally:
        s.close()
else:
    s = socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1]); s.close()
PY
)"
fi

URL="http://127.0.0.1:$PORT"
echo "$URL" > "$ROOT/.venv/.bms.url"

# ── 5. 같은 망의 다른 사람에게 보여 줄 때 (--share) ───────────────────────
# 기본은 `127.0.0.1` 이다 — 이 기계 밖에서는 아예 닿지 않는다. `--share` 는 그
# 경계를 **의도적으로** 연다. 앱이 읽기 전용이라 남이 저장소를 고칠 수는 없지만,
# 위키·게이트 원장·결과 수치가 **같은 망의 누구에게나 그대로 보인다.** 인증이
# 없고, 앞에 리버스 프록시도 없다. 사내망·연구실망에서 잠깐 같이 보는 용도이며
# 공개망(공유기 포트포워딩, 클라우드 공인 IP)에 걸어 두지 않는다.
if [[ "$SHARE" == "1" ]]; then
  BIND="0.0.0.0"
  # 상대가 칠 주소를 **우리가 찾아서 찍어 준다** — `ip addr` 를 읽게 시키지 않는다
  LANIP="$(ip -4 -o addr show scope global 2>/dev/null | awk '{split($4,a,"/"); print a[1]; exit}')"
  [[ -z "$LANIP" ]] && LANIP="$(hostname -I 2>/dev/null | awk '{print $1}')"
  echo "· 기동 → $URL"
  if [[ -n "$LANIP" ]]; then
    echo "· 같은 망에서는 →  http://$LANIP:$PORT"
    echo "$LANIP" > "$ROOT/.venv/.bms.lanip"
  else
    echo "· ⚠ 이 기계의 망 주소를 못 찾았다 — 'ip -4 addr' 로 직접 확인할 것"
  fi
  echo "· ⚠ 인증이 없다. 같은 망의 누구나 열람한다 (읽기 전용). 공개망에 걸지 말 것"
  echo "·   WSL 에서 돌린다면 Windows 쪽 방화벽·포트프록시가 한 겹 더 있다 (README 참고)"
else
  BIND="127.0.0.1"
  echo "· 기동 → $URL   (이 기계에서만 보인다 — 남에게 보여주려면: bms --share)"
fi
echo "·   끄기: Ctrl-C · 뒤에서 끄기: bms --stop"

# ── 6. 기동 (foreground — Ctrl-C 로 끈다) ─────────────────────────────────
echo $$ > "$PIDF"
trap 'rm -f "$PIDF"' EXIT
exec "$VENV/bin/python" - "$PORT" "$BIND" <<'PY'
import sys, pathlib
root = pathlib.Path(__file__).resolve().parent if "__file__" in dir() else pathlib.Path.cwd()
sys.path.insert(0, str(pathlib.Path.cwd() / "webapp"))
from app import app
app.run(host=sys.argv[2], port=int(sys.argv[1]), debug=False)
PY
