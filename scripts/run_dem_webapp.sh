#!/usr/bin/env bash
# DEM webapp 런처 — **리포 안에 있다** (홈 디렉터리가 아니라).
#
# ★★ 왜 리포로 옮겼나 (2026-08-25): 옛 런처가 `~/run_dem5002.sh` 라 홈에만 있었고,
#   윈도우 재설치로 WSL 이 통째로 날아가면서 **같이 사라졌다**.  리포에 두면 `git clone`
#   한 번으로 돌아온다.  alias 도 이 파일을 가리키게 한다.
#
#   bash scripts/run_dem_webapp.sh              # git pull → 5002 포트로 실행
#   bash scripts/run_dem_webapp.sh --open       # 실행 + 브라우저 열기
#   bash scripts/run_dem_webapp.sh --bg --open  # 백그라운드 + 브라우저 (셸을 안 잡는다)
#   bash scripts/run_dem_webapp.sh --no-pull    # 오프라인/작업 중일 때
#   PORT=5050 bash scripts/run_dem_webapp.sh    # 포트 바꾸기
#
# 환경변수로 경로를 바꿀 수 있다 (기본값은 이 랩 WSL 규약):
#   DEM_WEB_DATA=~/Yonghoon-DEM-DFT   데이터(uploads/results/archive/mpm_lab)와 venv 가 있는 곳
#   DEM_WEB_VENV=<venv 경로>          비우면 DATA/venv → CODE/venv 순으로 찾는다
set -uo pipefail

PORT="${PORT:-5002}"
OPEN=0; BG=0; PULL=1
for a in "$@"; do
  case "$a" in
    --open) OPEN=1;;
    --bg) BG=1;;
    --no-pull) PULL=0;;
    -h|--help) sed -n '1,22p' "$0"; exit 0;;
    *) echo "알 수 없는 인자: $a  (--open · --bg · --no-pull)"; exit 2;;
  esac
done

#  코드 = 이 스크립트가 있는 리포 (자기 위치로 찾는다 — 경로를 적어 두면 또 틀린다)
CODE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)"
#  데이터 = 코드와 **다른 곳**일 수 있다 (이 랩 규약: 코드는 worktree `~/dem-web`,
#  데이터는 `~/Yonghoon-DEM-DFT/webapp/*`).  같은 곳이면 그냥 같은 곳이다.
DATA="${DEM_WEB_DATA:-$HOME/Yonghoon-DEM-DFT}"
[ -d "$DATA" ] || DATA="$CODE"

echo "[dem] 코드 $CODE"
echo "[dem] 데이터 $DATA"

[ -f "$CODE/webapp/app.py" ] || {
  echo "[dem] ⛔ $CODE/webapp/app.py 가 없다 — 리포 루트가 맞나?"; exit 1; }

# ── ① 최신화 ────────────────────────────────────────────────────────────────────
if [ "$PULL" = 1 ]; then
  BR="$(git -C "$CODE" rev-parse --abbrev-ref HEAD 2>/dev/null || echo '')"
  if [ -n "$BR" ] && [ "$BR" != "HEAD" ]; then
    echo "[dem] git pull origin $BR"
    #  ⚠ 실패해도 **멈추지 않는다** — 오프라인이어도 웹앱은 떠야 한다 (있는 코드로).
    git -C "$CODE" pull --ff-only origin "$BR" 2>&1 | tail -3 \
      || echo "[dem] ⚠ pull 실패 — 현재 체크아웃으로 계속한다 (--no-pull 로 건너뛸 수 있다)"
  fi
fi

# ── ② 파이썬 환경 ───────────────────────────────────────────────────────────────
VENV="${DEM_WEB_VENV:-}"
if [ -z "$VENV" ]; then
  for c in "$DATA/venv" "$CODE/venv" "$HOME/Yonghoon-DEM-DFT/venv"; do
    [ -f "$c/bin/activate" ] && { VENV="$c"; break; }
  done
fi
if [ -n "$VENV" ] && [ -f "$VENV/bin/activate" ]; then
  # shellcheck disable=SC1091
  source "$VENV/bin/activate"
  echo "[dem] venv $VENV"
elif [ -n "${CONDA_DEFAULT_ENV:-}" ] && [ "${CONDA_DEFAULT_ENV}" != "base" ]; then
  echo "[dem] conda env $CONDA_DEFAULT_ENV (venv 없음 — 그대로 쓴다)"
else
  echo "[dem] ⚠ venv 를 못 찾았다 — 시스템 파이썬으로 시도한다"
  echo "      만들려면:  python3 -m venv \"$DATA/venv\" && \"$DATA/venv/bin/pip\" install -q flask numpy scipy"
fi

#  ⚠⚠ 2026-08-25 — 옛 판은 `('flask','numpy')` **두 개만** 확인하고 통과시켰다.  그런데
#    webapp 의 외부 의존은 13개고 `storage_sync` 가 최상위에서 `requests` 를 import 한다.
#    → 검사는 초록인데 **앱이 곧바로 ModuleNotFoundError 로 죽었다** = 검사가 실물을 안 봤다.
#    ⇒ 목록을 **추측하지 않는다**.  진짜 `app.py` 를 import 해 보고, 죽으면 없는 모듈 이름을
#      그대로 뽑아 **설치 명령까지 만들어** 준다 (규칙 J 와 같은 원리: 실제 진입점을 돌린다).
_DEP_ERR="$( (cd "$CODE/webapp" && python3 -c 'import app') 2>&1 >/dev/null )"
if [ -n "$_DEP_ERR" ]; then
  _MISS="$(printf '%s' "$_DEP_ERR" | sed -n "s/.*No module named '\([^']*\)'.*/\1/p" | sort -u | tr '\n' ' ')"
  if [ -n "${_MISS// /}" ]; then
    _PIP="$(printf '%s' "$_MISS" | sed 's/\bPIL\b/pillow/g; s/\bsklearn\b/scikit-learn/g')"
    echo "[dem] ⛔ 없는 모듈: $_MISS"
    echo "[dem]    설치:  ${VIRTUAL_ENV:+$VIRTUAL_ENV/bin/}pip install $_PIP"
    echo "[dem]    핵심 한 벌:  pip install flask requests numpy scipy pandas matplotlib pillow markdown"
    echo "[dem]    선택(없으면 그 기능만 꺼진다):  scikit-learn pybamm weasyprint anthropic"
  else
    echo "[dem] ⛔ app.py import 실패:"; printf '%s\n' "$_DEP_ERR" | tail -12
  fi
  exit 1
fi

# ── ③ 데이터 폴더 배선 (코드와 데이터가 갈려 있으므로 **명시로 잇는다**) ──────────────
#  이걸 안 하면 웹앱이 코드 worktree 안의 빈 폴더를 보고 "케이스 0건" 으로 뜬다.
for pair in "UPLOAD:uploads" "RESULTS:results" "ARCHIVE:archive" "MPM_LAB:mpm_lab"; do
  key="${pair%%:*}"; dir="${pair##*:}"
  mkdir -p "$DATA/webapp/$dir"
  export "WEBAPP_${key}_FOLDER=$DATA/webapp/$dir"
done
_n=$(find "$DATA/webapp/results" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l)
echo "[dem] 데이터 배선 완료 — results 케이스 ${_n}건"
[ "$_n" = 0 ] && echo "      ⚠ 0건이면 데이터 경로가 틀렸을 수 있다:  DEM_WEB_DATA=<경로> 로 지정"

# ── ④ 실행 ──────────────────────────────────────────────────────────────────────
URL="http://localhost:$PORT"
_open() {
  #  WSL → 윈도우 브라우저.  셋 중 되는 것으로 (환경마다 다르다).
  for c in wslview "explorer.exe" xdg-open open; do
    command -v "$c" >/dev/null 2>&1 && { "$c" "$URL" >/dev/null 2>&1 & return 0; }
  done
  echo "[dem] 브라우저를 못 열었다 — 직접 여세요: $URL"
}

cd "$CODE/webapp" || exit 1
if [ "$BG" = 1 ]; then
  LOG="$DATA/webapp/dem_webapp.log"
  echo "[dem] 백그라운드 실행 → $LOG"
  PORT="$PORT" nohup python3 app.py >"$LOG" 2>&1 &
  PID=$!
  echo "$PID" > "$DATA/webapp/dem_webapp.pid"
  #  뜰 때까지 잠깐 기다렸다가 연다 (바로 열면 연결 거부 화면이 뜬다)
  for _ in $(seq 1 40); do
    if python3 -c "import socket,sys; s=socket.socket(); s.settimeout(.3); sys.exit(0 if s.connect_ex(('127.0.0.1',$PORT))==0 else 1)"; then break; fi
    sleep 0.5
  done
  if kill -0 "$PID" 2>/dev/null; then
    echo "[dem] ✓ PID $PID · $URL"
    [ "$OPEN" = 1 ] && _open
    echo "[dem] 끄기:  kill \$(cat $DATA/webapp/dem_webapp.pid)"
    echo "[dem] 로그:  tail -f $LOG"
  else
    echo "[dem] ⛔ 떠오르지 못했다 — 로그 마지막:"; tail -20 "$LOG"; exit 1
  fi
else
  echo "[dem] ✓ $URL   (Ctrl-C 로 종료)"
  [ "$OPEN" = 1 ] && ( sleep 2; _open ) &
  PORT="$PORT" exec python3 app.py
fi
