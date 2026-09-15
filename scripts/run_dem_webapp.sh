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
#   bash scripts/run_dem_webapp.sh --stop       # 그 포트를 쥔 인스턴스만 멈춘다 (pid 파일 안 믿는다)
#   PORT=5050 bash scripts/run_dem_webapp.sh    # 포트 바꾸기
#
# 환경변수로 경로를 바꿀 수 있다 (기본값은 이 랩 WSL 규약):
#   DEM_WEB_DATA=~/Yonghoon-DEM-DFT   데이터(uploads/results/archive/mpm_lab)와 venv 가 있는 곳
#   DEM_WEB_VENV=<venv 경로>          비우면 DATA/venv → CODE/venv 순으로 찾는다
set -uo pipefail

PORT="${PORT:-5002}"
OPEN=0; BG=0; PULL=1; STOP=0
for a in "$@"; do
  case "$a" in
    --open) OPEN=1;;
    --bg) BG=1;;
    --no-pull) PULL=0;;
    --stop) STOP=1;;
    -h|--help) sed -n '1,23p' "$0"; exit 0;;
    *) echo "알 수 없는 인자: $a  (--open · --bg · --no-pull · --stop)"; exit 2;;
  esac
done

#  ★★ 2026-09-14 실사고 — **옛 인스턴스를 안 멈춰서 새 코드가 영영 안 떴다.**
#    옛 판은 포트를 확인하지 않고 그냥 `python3 app.py` 를 또 띄웠다.  포트가 물려 있으면
#    새 프로세스는 bind 실패로 죽는데, 준비 검사가 `connect_ex==0` 만 봐서 **옛 프로세스
#    덕분에 즉시 통과**하고 `✓ PID …` 를 찍었다 = 거짓 초록.  사용자는 "git pull 했고
#    런처가 ✓ 라는데 새 라우트가 404" 를 보게 된다 (worklog 페이지에서 실제로 겪음).
#    ⇒ 포트 기준으로 **먼저 멈추고** 띄운다.  pid 파일은 낡을 수 있어 믿지 않는다.
_port_pid() {                       # 그 포트를 LISTEN 중인 PID (없으면 빈 문자열)
  local p=''
  p="$(ss -ltnp 2>/dev/null | awk -v pat=":$PORT\$" 'NR>1 && $4 ~ pat' \
       | grep -oE 'pid=[0-9]+' | head -1 | cut -d= -f2)"
  [ -z "$p" ] && p="$(lsof -ti tcp:"$PORT" -sTCP:LISTEN 2>/dev/null | head -1)"
  printf '%s' "$p"
}
_stop_port() {                      # 그 포트를 비운다 (TERM → 안 죽으면 KILL)
  local pid; pid="$(_port_pid)"
  [ -z "$pid" ] && { echo "[dem] 포트 $PORT 비어 있음"; return 0; }
  echo "[dem] 포트 $PORT 를 PID $pid 가 쓰고 있다 — 옛 인스턴스를 멈춘다"
  kill "$pid" 2>/dev/null
  for _ in $(seq 1 20); do
    sleep 0.5; [ -z "$(_port_pid)" ] && { echo "[dem] 옛 인스턴스 종료 ✓"; return 0; }
  done
  pid="$(_port_pid)"
  [ -n "$pid" ] && { echo "[dem] TERM 무시 → KILL $pid"; kill -9 "$pid" 2>/dev/null; sleep 1; }
  [ -z "$(_port_pid)" ] && { echo "[dem] 옛 인스턴스 종료 ✓"; return 0; }
  echo "[dem] ⛔ 포트 $PORT 를 못 비웠다 (PID $(_port_pid)) — 직접 kill 후 다시"; return 1
}
if [ "$STOP" = 1 ]; then _stop_port; exit $?; fi

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
#  ★★ 2026-09-15 실사고 — **낡은 코드를 조용히 섬겼다.**  1저자가 새 페이지를 열었는데
#    커밋 다섯 개 전 화면이 떴고, 머리말의 SHA(`@ 9c5d6bfd8`)만이 그 사실을 말하고 있었다.
#    옛 판의 구멍 둘:
#      ⓐ detached HEAD (`BR == "HEAD"`) 면 pull 을 **아무 말 없이 건너뛴다** — 출력이 0줄이라
#         사용자는 최신인 줄 안다.
#      ⓑ pull 실패 경고가 `echo` 한 줄이라 `--bg` 로 띄우면 스크롤에 묻힌다.
#    ⇒ **무엇을 섬기는지 항상 말한다**: 기동 전 SHA 를 찍고, origin 과 다르면 배너를 띄운다.
#      ⛔ 그래도 **멈추지는 않는다** (오프라인에서도 웹앱은 떠야 한다) — 다만 **조용하지 않다**.
#    ⛔⛔ **그리고 그 둘 다 진짜 원인이 아니었다** (같은 날 저녁에 밝혀짐).  실제 원인은
#      **워크트리가 다른 브랜치에 있었던 것**이다 — `~/dem-web` 이
#      `claude/sdcp-dem-manuscript-si-pqwtv8` 에 있었고, 이 런처는 `git pull origin $BR` 로
#      **체크아웃된 브랜치 이름**을 그대로 쓴다.  그래서 *"엉뚱한 브랜치를 성공적으로"*
#      당겨 왔고, `@{upstream}` 대조도 그 브랜치 기준이라 **초록**이었다.
#      ⇒ 위 두 수리 중 어느 것도 이것을 못 잡는다.  **작업 브랜치와 다르면 배너를 띄운다.**
#      ⛔ 막지는 않는다 (다른 브랜치를 일부러 띄울 때가 있다) — 다만 조용하지 않다.
EXPECT_BR="${DEM_WEB_BRANCH:-claude/stoic-knuth-NObVQ}"
_SHA_BEFORE="$(git -C "$CODE" rev-parse --short=9 HEAD 2>/dev/null || echo '?')"
_CUR_BR="$(git -C "$CODE" rev-parse --abbrev-ref HEAD 2>/dev/null || echo '')"
if [ -n "$_CUR_BR" ] && [ "$_CUR_BR" != "HEAD" ] && [ "$_CUR_BR" != "$EXPECT_BR" ]; then
  echo "[dem] ╔══════════════════════════════════════════════════════════════════"
  echo "[dem] ║ ⚠⚠ 코드 워크트리가 **작업 브랜치가 아니다**"
  echo "[dem] ║    지금: $_CUR_BR"
  echo "[dem] ║    기대: $EXPECT_BR   (바꾸려면 DEM_WEB_BRANCH=…)"
  echo "[dem] ║    ⇒ 아래 pull 은 **그 브랜치**를 당긴다 = 새 코드가 안 온다."
  echo "[dem] ║       git -C \"$CODE\" switch $EXPECT_BR"
  echo "[dem] ╚══════════════════════════════════════════════════════════════════"
fi
if [ "$PULL" = 1 ]; then
  BR="$_CUR_BR"
  if [ -z "$BR" ]; then
    echo "[dem] ⚠ git 리포가 아니다 ($CODE) — 최신화를 건너뛴다"
  elif [ "$BR" = "HEAD" ]; then
    echo "[dem] ⚠⚠ detached HEAD ($_SHA_BEFORE) — **pull 을 건너뛴다**.  브랜치로 돌아가려면:"
    echo "        git -C \"$CODE\" checkout claude/stoic-knuth-NObVQ && git -C \"$CODE\" pull"
  else
    echo "[dem] git pull origin $BR   (지금 $_SHA_BEFORE)"
    #  ⚠ 실패해도 **멈추지 않는다** — 오프라인이어도 웹앱은 떠야 한다 (있는 코드로).
    if ! git -C "$CODE" pull --ff-only origin "$BR" 2>&1 | tail -3; then
      echo "[dem] ⚠ pull 실패 — 현재 체크아웃으로 계속한다 (--no-pull 로 건너뛸 수 있다)"
      git -C "$CODE" status --short | head -5 | sed 's/^/        /'
    fi
  fi
fi
#  ── 무엇을 섬기는지 말한다.  ⛔ "초록" 만 찍고 낡은 것을 섬기지 않는다.
_SHA_NOW="$(git -C "$CODE" rev-parse --short=9 HEAD 2>/dev/null || echo '?')"
_SHA_REMOTE="$(git -C "$CODE" rev-parse --short=9 "@{upstream}" 2>/dev/null || echo '')"
if [ -n "$_SHA_REMOTE" ] && [ "$_SHA_NOW" != "$_SHA_REMOTE" ]; then
  _BEHIND="$(git -C "$CODE" rev-list --count "HEAD..@{upstream}" 2>/dev/null || echo '?')"
  echo "[dem] ╔══════════════════════════════════════════════════════════════════"
  echo "[dem] ║ ⚠⚠ 낡은 코드를 섬긴다 — HEAD $_SHA_NOW · upstream $_SHA_REMOTE (뒤처짐 $_BEHIND 커밋)"
  echo "[dem] ║    페이지 머리말의 SHA 가 $_SHA_NOW 로 찍히면 그것이 이 이유다."
  echo "[dem] ╚══════════════════════════════════════════════════════════════════"
else
  echo "[dem] 코드 $_SHA_NOW${_SHA_REMOTE:+ (upstream 과 같다)}"
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
#  ★★ 2026-08-25 — **백업 나이를 매번 보여준다.**  윈도우 재설치로 WSL 안의 케이스 169건을
#    잃고 나서 붙였다.  백업은 조용히 안 도는 것이 기본값이므로 **침묵이 보이게** 만든다:
#    스탬프가 없거나 오래됐으면 여기서 눈에 띈다 (막지는 않는다 — 웹앱은 떠야 한다).
_BSTAMP="$DATA/webapp/.last_backup"
if [ -f "$_BSTAMP" ]; then
  _bage=$(( ( $(date +%s) - $(stat -c %Y "$_BSTAMP" 2>/dev/null || echo 0) ) / 86400 ))
  if [ "$_bage" -ge 7 ]; then
    echo "[dem] ⚠ 마지막 D 백업이 **${_bage}일 전** — bash $CODE/scripts/backup_webapp_data.sh"
  else
    echo "[dem] 백업 ✓ ${_bage}일 전"
  fi
elif [ "$_n" -gt 0 ]; then
  echo "[dem] ⚠⚠ **D 백업 기록이 없다** — 이 케이스 ${_n}건은 WSL 안에만 있다 (윈도우와 함께 사라진다)."
  echo "[dem]    bash $CODE/scripts/backup_webapp_data.sh    (대상: \${DEM_WEB_BACKUP:-/mnt/d/dem-backup/webapp})"
fi
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

#  ★ 띄우기 전에 포트를 비운다 — 이걸 빼면 위 지뢰(거짓 초록)가 그대로 재발한다
_stop_port || exit 1

cd "$CODE/webapp" || exit 1
if [ "$BG" = 1 ]; then
  LOG="$DATA/webapp/dem_webapp.log"
  echo "[dem] 백그라운드 실행 → $LOG"
  PORT="$PORT" nohup python3 app.py >"$LOG" 2>&1 &
  PID=$!
  echo "$PID" > "$DATA/webapp/dem_webapp.pid"
  #  뜰 때까지 잠깐 기다렸다가 연다 (바로 열면 연결 거부 화면이 뜬다)
  for _ in $(seq 1 40); do
    kill -0 "$PID" 2>/dev/null || break        # ★ 우리 프로세스가 죽었으면 즉시 탈출
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
