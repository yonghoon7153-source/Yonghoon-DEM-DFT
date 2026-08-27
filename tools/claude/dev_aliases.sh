#!/usr/bin/env bash
# =============================================================================
# dev_aliases.sh — 로컬 작업 머신용 명령 모음. `source` 해서 쓴다.
#
# 왜 repo 안에 두나
#   로컬 머신을 다시 깔면 ~/.bashrc 는 사라진다. **repo 는 남는다.**
#   재설치 후 복구는 두 줄이면 끝난다:
#       git clone <repo> && cd Yonghoon-DEM-DFT
#       echo 'source ~/Yonghoon-DEM-DFT/tools/claude/dev_aliases.sh' >> ~/.bashrc
#   (2026-08-25 윈도우 재설정 때 신설 — 그때까지 alias 는 어디에도 안 적혀 있었다)
#
# 이 파일이 **못 하는 것**
#   · ssh 키를 만들지 않는다. 무비번 접속은 한 번은 손으로 해야 한다:
#       ssh-keygen -t ed25519          (이미 있으면 건너뛴다)
#       ssh-copy-id root@121.78.116.27 ; ssh-copy-id kgy@59.12.161.91
#   · conda 를 다루지 않는다. webapp 용 venv 는 dftsetup 이 만들지만, 계산용
#     환경(uma / QE)은 서버 쪽 것이라 여기서 안 건드린다.
#   · **PowerShell 에서는 안 된다** — bash 전용이다 (WSL 또는 Git Bash).
#   · 서버 쪽 작업을 대신 판정하지 않는다. 붙여주기만 한다.
#
#   source tools/claude/dev_aliases.sh
#   bash tools/claude/dev_aliases.sh --selftest
# =============================================================================

# 스크립트 자기 위치에서 repo 루트를 구한다 (경로를 손으로 안 적어도 되게).
if [ -n "${BASH_SOURCE[0]:-}" ]; then
  DFT_REPO="${DFT_REPO:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." 2>/dev/null && pwd)}"
fi
DFT_REPO="${DFT_REPO:-$HOME/Yonghoon-DEM-DFT}"
DFT_BRANCH="${DFT_BRANCH:-claude/friendly-meitner-lldvar}"
DFT_PORT="${DFT_PORT:-5001}"
export DFT_REPO DFT_BRANCH DFT_PORT

# ── 안전 가드 ────────────────────────────────────────────────────────────────
# ⚠ 서버에서는 `git reset --hard` 를 쓴다(읽기 전용 소비자라 잃을 게 없다). 로컬은
#   다르다 — 여기서 같은 걸 하면 **손댄 것이 말없이 사라진다.** 더러우면 멈춘다.
# ⛔ 2026-08-25 실측 — 첫 판은 **untracked 까지 막았다.** `git reset --hard` 는
#   추적 중인 파일만 되돌린다 — untracked 는 손도 안 댄다. 그런데 가드가 둘을 안 갈라서,
#   다른 브랜치가 남긴 .bml/ · apps/ · data/ · packages/ 때문에 dftpull 이 영영 막혔다.
#   (그 상태로는 "이걸 무시하게 해주는 .gitignore" 조차 못 받는다 — 자기가 자기를 막는다.)
#   위험한 건 **추적 파일의 수정**뿐이다. 그것만 막고 untracked 는 알려만 준다.
_dft_tree_clean() {          # $1 = repo.  0 깨끗 · 1 추적파일 수정(위험) · 2 repo 아님 · 3 untracked만(안전)
  local r="${1:-$DFT_REPO}" st
  git -C "$r" rev-parse --git-dir >/dev/null 2>&1 || return 2
  st="$(git -C "$r" status --porcelain 2>/dev/null)"
  [ -z "$st" ] && return 0
  # '??' 로 시작하지 않는 줄 = 추적 파일의 수정/스테이지 → reset --hard 가 지운다
  printf '%s\n' "$st" | grep -qv '^??' && return 1
  return 3
}

# ── 명령 ─────────────────────────────────────────────────────────────────────
# ⭐ 한 번에 다 한다 — 받고, 띄우고, 주소를 준다. 예전엔 상태 한 줄만 찍어
#   "그래서 뭘 하라는 거지" 가 됐다. 매번 dftpull → dftwebbg 를 손으로 이어 붙였다.
#   ⚠ 로컬 수정이 있으면 pull 을 건너뛴다 (dftpull 의 가드를 그대로 탄다 — 안 버린다).
dft() {
  cd "$DFT_REPO" || return 1
  dftpull || echo "· pull 을 건너뛰었다 (위 사유) — 있는 코드로 띄운다"
  if _dft_web_alive; then
    echo "✅ 이미 떠 있다 → http://127.0.0.1:${DFT_PORT}"
  else
    dftwebbg || return 1
  fi
  git -C "$DFT_REPO" log --oneline -1
}
dftst()   { cd "$DFT_REPO" || return 1; git -C "$DFT_REPO" status -sb | head -3; }  # 예전 dft

dftpull() {                  # 최신 받기. -f 를 줘야만 로컬 변경을 버린다.
  local force=0
  [ "${1:-}" = "-f" ] && force=1
  git -C "$DFT_REPO" fetch origin "$DFT_BRANCH" || return 1
  _dft_tree_clean "$DFT_REPO"; local st=$?
  if [ "$st" = 2 ]; then echo "⛔ git repo 가 아니다: $DFT_REPO"; return 1; fi
  if [ "$st" = 1 ] && [ "$force" = 0 ]; then
    echo "⛔ **추적 파일에 수정이 있다** — reset 하면 사라진다. 먼저 보라:"
    git -C "$DFT_REPO" status --short | grep -v '^??'
    echo "   버려도 되면:  dftpull -f"
    return 1
  fi
  [ "$st" = 1 ] && { echo "⚠ -f — 아래 수정을 버린다:"; git -C "$DFT_REPO" status --short | grep -v '^??'; }
  # untracked 는 reset --hard 가 건드리지 않는다. 막지 않고 알려만 준다.
  if [ "$st" = 3 ] || [ "$force" = 1 ]; then
    local n; n=$(git -C "$DFT_REPO" status --porcelain | grep -c '^??')
    [ "${n:-0}" -gt 0 ] && echo "· untracked ${n}건은 그대로 둔다 (reset 대상 아님)"
  fi
  # ⛔ 2026-08-25 — 이 파일 자체가 바뀌면 **셸에는 옛 함수가 그대로 남는다.**
  #   dftpull 의 버그를 고쳐 올려도, 그걸 받으려면 옛 dftpull 을 써야 하는 자물쇠가
  #   두 번 걸렸다. 당긴 뒤 파일이 바뀌었으면 스스로 다시 읽는다.
  local _self="$DFT_REPO/tools/claude/dev_aliases.sh"
  local _before=""; [ -f "$_self" ] && _before=$(git -C "$DFT_REPO" hash-object "$_self" 2>/dev/null)
  git -C "$DFT_REPO" reset --hard FETCH_HEAD || return 1
  git -C "$DFT_REPO" log --oneline -1
  local _after=""; [ -f "$_self" ] && _after=$(git -C "$DFT_REPO" hash-object "$_self" 2>/dev/null)
  if [ -n "$_before" ] && [ "$_before" != "$_after" ]; then
    # shellcheck disable=SC1090
    . "$_self" && echo "↻ dev_aliases.sh 가 바뀌어 다시 읽었다 (dfthelp 로 확인)"
  fi
}

# ⛔ 2026-08-25 실측 — 첫 판은 **실패하고도 아무 말을 안 했다.** 새로 깐 WSL 에서
#   Flask 가 없어 python3 가 즉사했는데 화면에는 `[1]+ Exit 1` 만 남았다. 원인을
#   보려면 로그 파일을 손으로 열어야 했다 — 진단이 안 나오는 게 실패보다 나쁘다.
#   ⇒ 띄우기 **전에** 전제(python3 · Flask)를 확인하고, 없으면 고치는 법을 찍는다.
# ⛔ 2026-08-25 실측 — Ubuntu 24.04(python 3.12) 는 PEP 668 로 시스템 pip 을 막는다
#   ("externally-managed-environment"). `--break-system-packages` 는 OS 파이썬을
#   건드리는 거라 쓰지 않는다. **venv 가 정답**이고, .venv/ 는 이미 gitignore 에 있다.
DFT_VENV="${DFT_VENV:-$DFT_REPO/.venv}"

_dft_py() {                  # 쓸 파이썬 경로. venv 가 있으면 그것을, 없으면 시스템.
  if [ -x "$DFT_VENV/bin/python" ]; then echo "$DFT_VENV/bin/python"
  else command -v python3; fi
}

dftsetup() {                 # venv 만들고 webapp 의존성 설치 (한 번만)
  command -v python3 >/dev/null || {
    echo "⛔ python3 가 없다.  sudo apt update && sudo apt install -y python3"; return 1; }
  if [ ! -x "$DFT_VENV/bin/python" ]; then
    echo "▶ venv 생성: $DFT_VENV"
    if ! python3 -m venv "$DFT_VENV" 2>/dev/null; then
      echo "⛔ venv 를 못 만들었다. 데비안 계열은 별도 패키지가 필요하다:"
      echo "     sudo apt update && sudo apt install -y python3-venv"
      return 1
    fi
  fi
  "$DFT_VENV/bin/python" -m pip install -q --upgrade pip
  "$DFT_VENV/bin/python" -m pip install -q -r "$DFT_REPO/webapp/requirements.txt" || return 1
  echo "✅ 준비 완료 — 이제 dftweb / dftwebbg"
  "$DFT_VENV/bin/python" -c "import flask, markdown; print('   flask', flask.__version__)"
}

_dft_web_ready() {           # 0 = 띄울 수 있다, 1 = 전제가 빠졌다 (이유를 찍는다)
  local py; py="$(_dft_py)"
  if [ -z "$py" ]; then
    echo "⛔ python3 가 없다.   sudo apt update && sudo apt install -y python3"
    return 1
  fi
  if ! "$py" -c "import flask, markdown" 2>/dev/null; then
    echo "⛔ Flask/markdown 이 없다 (새로 깐 WSL 이면 정상이다). 한 줄이면 끝난다:"
    echo "     dftsetup"
    echo "   (venv 를 만들어서 넣는다. Ubuntu 24.04 는 시스템 pip 이 PEP 668 로 막혀 있다)"
    return 1
  fi
  [ -f "$DFT_REPO/webapp/app.py" ] || { echo "⛔ webapp/app.py 가 없다: $DFT_REPO"; return 1; }
  return 0
}

# 건강검진. curl 이 없는 WSL 이 있어서 python 으로 되돌아간다.
_dft_web_alive() {
  if command -v curl >/dev/null; then
    curl -fsS "http://127.0.0.1:${DFT_PORT}/health" >/dev/null 2>&1
  else
    python3 -c "import urllib.request,sys
try: urllib.request.urlopen('http://127.0.0.1:${DFT_PORT}/health',timeout=3)
except Exception: sys.exit(1)" 2>/dev/null
  fi
}

dftweb()  {                  # webapp 띄우기 (Ctrl-C 로 끈다)
  _dft_web_ready || return 1
  echo "▶ http://127.0.0.1:${DFT_PORT}   (Ctrl-C 로 종료)"
  PORT="$DFT_PORT" "$(_dft_py)" "$DFT_REPO/webapp/app.py"
}

dftwebbg() {                 # 백그라운드로 띄우고 살아있는지 확인
  _dft_web_ready || return 1
  # ⛔⛔ 2026-08-27 — 옛 판은 `pgrep -f webapp/app.py` 로 중복을 막았다. 그런데
  #   `pkill` 직후에는 프로세스가 **종료 중(좀비 포함)** 으로 몇 초 남는다.
  #   실측: `pkill …; sleep 2; dft` 라는 **가장 자연스러운 순서**가 그대로 막혔고,
  #   `return 1` 이라 `dft` 가 조용히 끝나서 "왜 안 뜨지" 로 갔다.
  #   → 중복 판정은 **포트가 실제로 응답하는가**로 한다. 살아 있으면 그렇다고 말하고
  #     성공으로 끝낸다(막지 않는다). 죽어가는 프로세스는 포트를 이미 놨다.
  if _dft_web_alive; then
    echo "✅ 이미 떠 있다 → http://127.0.0.1:${DFT_PORT}"
    return 0
  fi
  # 포트는 안 열렸는데 프로세스가 남아 있으면 — 정리하고 진행한다(사람 손 안 빌린다)
  if pgrep -f "webapp/app.py" >/dev/null; then
    echo "· 응답 없는 옛 프로세스가 남아 있다 — 정리하고 띄운다"
    pkill -f "webapp/app.py" 2>/dev/null
    sleep 2
  fi
  local log="${TMPDIR:-/tmp}/dftweb.log"
  PORT="$DFT_PORT" nohup "$(_dft_py)" "$DFT_REPO/webapp/app.py" > "$log" 2>&1 &
  local i
  for i in 1 2 3 4 5 6 7 8 9 10; do        # 느린 기계에서 3초는 모자랐다
    sleep 1
    _dft_web_alive && { echo "✅ http://127.0.0.1:${DFT_PORT}   로그: $log"; return 0; }
  done
  echo "⛔ ${DFT_PORT} 포트가 10초 안에 안 열렸다 — 로그 꼬리:"
  tail -15 "$log" 2>/dev/null || echo "   (로그 파일도 없다: $log)"
  return 1
}
dftwebstop() { pkill -f "webapp/app.py" && echo "✓ webapp 종료" || echo "· 떠 있지 않다"; }

dfttest() { "$(_dft_py)" -m pytest "$DFT_REPO/webapp/tests" -q; }
dftlint() { python3 "$DFT_REPO/tools/kb_wiki.py" lint; python3 "$DFT_REPO/tools/convention_check.py" | tail -2; }

# 서버 — ssh 키를 먼저 심어야 무비번이 된다 (위 '못 하는 것' 참조)
gabia()  { ssh root@121.78.116.27 "$@"; }
kgy()    { ssh kgy@59.12.161.91 "$@"; }
# 붙자마자 "지금 걸어도 되나" 를 본다
gabiast() { ssh root@121.78.116.27 "cd /data/work/repo && bash tools/claude/server_status.sh ${1:-}"; }
gabiajobs(){ gabiast --jobs; }        # 진행률까지
kgyst()   { ssh kgy@59.12.161.91 "cd ~/work/Yonghoon-DEM-DFT && bash tools/claude/server_status.sh ${1:-}"; }
kgyjobs() { kgyst --jobs; }

dfthelp() {
  cat <<'EOT'
  dft         ★ 받고 + webapp 띄우고 + 주소 (한 번에)
  dftst       repo 로 이동 + 상태 3줄 (예전 dft)
  dftpull     최신 받기 (로컬 변경이 있으면 멈춘다 · 버리려면 dftpull -f)
  dftsetup    ★ 처음 한 번 — venv + 의존성 설치
  dftweb      webapp 앞단 실행        dftwebbg  백그라운드 + 건강검진
  dftwebstop  webapp 종료             dfttest   webapp 테스트
  dftlint     kb lint + 물리규약 검사
  gabia/kgy   ssh 접속                gabiast/kgyst  서버 현황 한 화면
  gabiajobs/kgyjobs   + 작업별 진행률
EOT
}

# ── selftest ────────────────────────────────────────────────────────────────
if [ "${1:-}" = "--selftest" ]; then
  ok=1
  say(){ echo "  $1 $2"; if [ "$1" = "✗" ]; then ok=0; fi; return 0; }
  echo "── dev_aliases selftest ──"
  [ -d "$DFT_REPO/webapp" ] && say "✓" "① repo 자동 인식: $DFT_REPO" \
                            || say "✗" "① repo 를 못 찾았다: $DFT_REPO"
  [ -f "$DFT_REPO/webapp/app.py" ] && say "✓" "② webapp/app.py 있다" || say "✗" "② app.py 없다"
  # ★ dft 는 "받고 + 띄우고 + 주소" 를 다 해야 한다 — 셋 중 하나라도 빠지면 손으로 잇게 된다
  _b=$(declare -f dft 2>/dev/null)
  case "$_b" in *dftpull*) say "✓" "②' dft 가 pull 을 한다";; *) say "✗" "②' dft 에 pull 이 없다";; esac
  case "$_b" in *dftwebbg*|*_dft_web_alive*) say "✓" "②' dft 가 webapp 을 띄운다";;
                *) say "✗" "②' dft 가 webapp 을 안 띄운다";; esac
  case "$_b" in *127.0.0.1*) say "✓" "②' dft 가 주소를 찍는다";; *) say "✗" "②' 주소를 안 찍는다";; esac

  T=$(mktemp -d)
  # [음성] git repo 가 아니면 2 를 돌려줘야 한다 (0 이면 더러운 트리를 깨끗하다고 본다)
  _dft_tree_clean "$T"; [ "$?" = 2 ] && say "✓" "③ git repo 아님 → 2" || say "✗" "③ repo 아닌데 판정을 했다"
  git -C "$T" init -q 2>/dev/null; git -C "$T" -c user.email=a@b -c user.name=a commit -q --allow-empty -m x 2>/dev/null
  _dft_tree_clean "$T" && say "✓" "④ 깨끗한 트리 → 0" || say "✗" "④ 깨끗한데 더럽다고 했다"
  # [음성] ★ 이 한 줄이 이 파일의 존재 이유다 — 더러운 트리를 깨끗하다고 하면
  #   dftpull 이 손댄 것을 말없이 버린다
  # ★ untracked 만 있는 경우는 **막으면 안 된다** — reset --hard 가 안 건드리기 때문이다.
  #   (첫 판이 여기서 막혀, 그 막힘을 푸는 .gitignore 조차 못 받는 자물쇠가 됐다)
  echo dirty > "$T/dirty.txt"
  _dft_tree_clean "$T"; [ "$?" = 3 ] && say "✓" "⑤ untracked 만 → 3 (통과시킨다)" \
                                     || say "✗" "⑤ untracked 를 위험으로 오판 — dftpull 이 영영 막힌다"
  # [음성] 추적 중인 파일의 수정은 **반드시** 막아야 한다 (이건 reset 이 지운다)
  rm -f "$T/dirty.txt"; echo v1 > "$T/f.txt"
  git -C "$T" add f.txt 2>/dev/null; git -C "$T" -c user.email=a@b -c user.name=a commit -q -m f 2>/dev/null
  echo v2 > "$T/f.txt"
  _dft_tree_clean "$T"; [ "$?" = 1 ] && say "✓" "⑥ 추적 파일 수정 → 1 (막는다)" \
                                     || say "✗" "⑥ **추적 파일 수정을 못 잡았다** — 수정이 사라진다"
  # [음성] 추적 수정 + untracked 가 섞이면 **위험 쪽**으로 판정해야 한다
  echo also > "$T/untracked2.txt"
  _dft_tree_clean "$T"; [ "$?" = 1 ] && say "✓" "⑦ 수정+untracked 혼재 → 1 (안전측)" \
                                     || say "✗" "⑦ 혼재인데 통과시켰다 — 수정이 사라진다"
  rm -rf "$T"
  [ "$ok" = 1 ] && { echo "  ✅ selftest 통과"; exit 0; } || { echo "  ⛔ selftest 실패"; exit 1; }
fi
