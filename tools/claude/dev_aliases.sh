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
#   · 파이썬 환경(conda/venv)을 만들지 않는다.
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
_dft_tree_clean() {          # $1 = repo 경로.  0 = 깨끗함, 1 = 변경 있음, 2 = repo 아님
  local r="${1:-$DFT_REPO}"
  git -C "$r" rev-parse --git-dir >/dev/null 2>&1 || return 2
  [ -z "$(git -C "$r" status --porcelain 2>/dev/null)" ]
}

# ── 명령 ─────────────────────────────────────────────────────────────────────
dft()     { cd "$DFT_REPO" || return 1; git -C "$DFT_REPO" status -sb | head -3; }

dftpull() {                  # 최신 받기. -f 를 줘야만 로컬 변경을 버린다.
  local force=0
  [ "${1:-}" = "-f" ] && force=1
  git -C "$DFT_REPO" fetch origin "$DFT_BRANCH" || return 1
  if ! _dft_tree_clean "$DFT_REPO"; then
    if [ "$force" = 0 ]; then
      echo "⛔ 로컬에 변경이 있다 — 그냥 덮으면 사라진다. 먼저 보라:"
      git -C "$DFT_REPO" status --short
      echo "   버려도 되면:  dftpull -f"
      return 1
    fi
    echo "⚠ -f — 아래 변경을 버린다:"; git -C "$DFT_REPO" status --short
  fi
  git -C "$DFT_REPO" reset --hard FETCH_HEAD && \
    git -C "$DFT_REPO" log --oneline -1
}

dftweb()  {                  # webapp 띄우기 (Ctrl-C 로 끈다)
  echo "▶ http://127.0.0.1:${DFT_PORT}   (Ctrl-C 로 종료)"
  PORT="$DFT_PORT" python3 "$DFT_REPO/webapp/app.py"
}

dftwebbg() {                 # 백그라운드로 띄우고 살아있는지 확인
  pgrep -f "webapp/app.py" >/dev/null && { echo "⚠ 이미 떠 있다 (pgrep -f webapp/app.py)"; return 1; }
  PORT="$DFT_PORT" nohup python3 "$DFT_REPO/webapp/app.py" \
    > "${TMPDIR:-/tmp}/dftweb.log" 2>&1 &
  sleep 3
  if curl -fsS "http://127.0.0.1:${DFT_PORT}/health" >/dev/null 2>&1; then
    echo "✅ http://127.0.0.1:${DFT_PORT}   로그: ${TMPDIR:-/tmp}/dftweb.log"
  else
    echo "⛔ 안 떴다 — 로그 꼬리:"; tail -15 "${TMPDIR:-/tmp}/dftweb.log"; return 1
  fi
}
dftwebstop() { pkill -f "webapp/app.py" && echo "✓ webapp 종료" || echo "· 떠 있지 않다"; }

dfttest() { python3 -m pytest "$DFT_REPO/webapp/tests" -q; }
dftlint() { python3 "$DFT_REPO/tools/kb_wiki.py" lint; python3 "$DFT_REPO/tools/convention_check.py" | tail -2; }

# 서버 — ssh 키를 먼저 심어야 무비번이 된다 (위 '못 하는 것' 참조)
gabia()  { ssh root@121.78.116.27 "$@"; }
kgy()    { ssh kgy@59.12.161.91 "$@"; }
# 붙자마자 "지금 걸어도 되나" 를 본다
gabiast() { ssh root@121.78.116.27 'cd /data/work/repo && bash tools/claude/server_status.sh'; }
kgyst()   { ssh kgy@59.12.161.91 'cd ~/work/Yonghoon-DEM-DFT && bash tools/claude/server_status.sh'; }

dfthelp() {
  cat <<'EOT'
  dft         repo 로 이동 + 상태 3줄
  dftpull     최신 받기 (로컬 변경이 있으면 멈춘다 · 버리려면 dftpull -f)
  dftweb      webapp 앞단 실행        dftwebbg  백그라운드 + 건강검진
  dftwebstop  webapp 종료             dfttest   webapp 테스트
  dftlint     kb lint + 물리규약 검사
  gabia/kgy   ssh 접속                gabiast/kgyst  서버 현황 한 화면
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

  T=$(mktemp -d)
  # [음성] git repo 가 아니면 2 를 돌려줘야 한다 (0 이면 더러운 트리를 깨끗하다고 본다)
  _dft_tree_clean "$T"; [ "$?" = 2 ] && say "✓" "③ git repo 아님 → 2" || say "✗" "③ repo 아닌데 판정을 했다"
  git -C "$T" init -q 2>/dev/null; git -C "$T" -c user.email=a@b -c user.name=a commit -q --allow-empty -m x 2>/dev/null
  _dft_tree_clean "$T" && say "✓" "④ 깨끗한 트리 → 0" || say "✗" "④ 깨끗한데 더럽다고 했다"
  # [음성] ★ 이 한 줄이 이 파일의 존재 이유다 — 더러운 트리를 깨끗하다고 하면
  #   dftpull 이 손댄 것을 말없이 버린다
  echo dirty > "$T/dirty.txt"
  _dft_tree_clean "$T" && say "✗" "⑤ **더러운 트리를 깨끗하다고 했다** — dftpull 이 변경을 버린다" \
                       || say "✓" "⑤ 더러운 트리 → 1 (dftpull 이 멈춘다)"
  # [음성] 추적 중인 파일을 고친 경우도 잡아야 한다 (untracked 만 보면 놓친다)
  rm -f "$T/dirty.txt"; echo v1 > "$T/f.txt"
  git -C "$T" add f.txt 2>/dev/null; git -C "$T" -c user.email=a@b -c user.name=a commit -q -m f 2>/dev/null
  echo v2 > "$T/f.txt"
  _dft_tree_clean "$T" && say "✗" "⑥ 추적 파일 수정을 못 잡았다" || say "✓" "⑥ 추적 파일 수정 → 1"
  rm -rf "$T"
  [ "$ok" = 1 ] && { echo "  ✅ selftest 통과"; exit 0; } || { echo "  ⛔ selftest 실패"; exit 1; }
fi
