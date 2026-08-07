# DEM 웹앱 (WSL) 갱신·재시작 셸 함수 — `source` 해서 쓴다.
#
#   설치:  echo 'source /home/yonghoon/dem-web/scripts/dem_shell.sh' >> ~/.bashrc
#          exec bash
#
# ★ 왜 .bashrc 에 직접 붙여넣지 않는가: 긴 heredoc 을 터미널에 붙이면 줄이 섞여
#   .bashrc 가 깨진다 (2026-08-06 실제 발생 — 'syntax error near dem() {').
#   리포에 파일로 두고 한 줄로 source 하면 붙여넣기가 관여하지 않는다.
#
# ★ 왜 alias 가 아니라 함수인가: 절차 중간에 조건 분기가 있다 —
#   재생성 산출물만 되돌리고, **그 외 수정이 남아 있으면 멈춘다**.
#   alias 로 이어붙이면 그 안전장치가 사라져 손댄 파일이 조용히 날아간다.
#
# ═══════════════════ DEM 웹앱 (WSL) — 갱신 + 재시작 ═══════════════════
# 사용:  dem            갱신 → 재생성 → 재시작 (기본)
#        dem status     현재 상태만 보기
#        dem -f         "모르는 수정" 경고를 무시하고 강행 (검토 후에만)
#        dem norun      갱신·재생성까지만 하고 서버는 안 건드림
export DEM_WEB="${DEM_WEB:-/home/yonghoon/dem-web}"
export DEM_BRANCH="${DEM_BRANCH:-claude/stoic-knuth-NObVQ}"
export DEM_RUN="${DEM_RUN:-$HOME/run_dem5002.sh}"

# 매 fit 마다 다시 만들어지는 산출물 — pull 을 막으면 버려도 된다 (데이터 아님).
# ★ 이 목록에 없는 파일은 절대 자동으로 버리지 않는다.
DEM_REGEN_PATHS=('이종기술/eis/' '.gitignore')

# ★ 반드시 함수 정의 **앞**에 있어야 한다.  대화형 셸은 alias 를 함수 정의보다 먼저
#   전개하므로, 같은 이름의 alias 가 남아 있으면  alias dem='cd ~/dem-web'  →
#   `cd ~/dem-web() {` 가 되어  "syntax error near unexpected token `('" 로 죽는다
#   (2026-08-06 실제 발생 — 파일·인코딩 문제가 아니었다).
unalias dem 2>/dev/null || true

dem() {
  local force=0 run=1 arg
  for arg in "$@"; do
    case "$arg" in
      -f|--force) force=1 ;;
      norun|--no-run) run=0 ;;
      status|-s)
        ( cd "$DEM_WEB" 2>/dev/null || { echo "★ $DEM_WEB 없음"; exit 1; }
          echo "── HEAD ──"; git log --oneline -1
          echo "── 변경 ──"; git status --short || true )
        return ;;
      -h|--help) sed -n '2,7p' <(declare -f dem >/dev/null; cat "${BASH_SOURCE[0]:-$HOME/.bashrc}") 2>/dev/null
        echo "dem [status|norun|-f]"; return ;;
    esac
  done

  ( set -o pipefail
    cd "$DEM_WEB" || { echo "★ $DEM_WEB 이 없습니다"; exit 1; }
    git rev-parse --git-dir >/dev/null 2>&1 || { echo "★ git 저장소가 아닙니다: $DEM_WEB"; exit 1; }
    echo "▶ $DEM_WEB  ($(git log --oneline -1))"

    # ── ① 재생성 산출물만 되돌린다 (실제로 더러운 것만) ──────────────
    local p tossed=0
    for p in "${DEM_REGEN_PATHS[@]}"; do
      if [ -n "$(git status --porcelain -- "$p" 2>/dev/null)" ]; then
        git checkout -- "$p" 2>/dev/null && { echo "  ↩ 되돌림: $p"; tossed=1; }
      fi
    done
    [ "$tossed" = 0 ] && echo "  · 되돌릴 재생성 파일 없음"

    # ── ② 그래도 남은 수정이 있으면 멈춘다 (모르는 파일은 안 지운다) ──
    local rest; rest="$(git status --porcelain | grep -v '^??' || true)"
    if [ -n "$rest" ] && [ "$force" = 0 ]; then
      echo; echo "★ 예상 못 한 수정이 남아 있어 중단합니다 — 내용을 확인하세요:"
      echo "$rest" | sed 's/^/    /'
      echo "    (diff 보기:  cd $DEM_WEB && git diff)"
      echo "    검토 후 강행하려면:  dem -f"
      exit 2
    fi
    [ -n "$rest" ] && { echo "  ⚠ --force: 위 수정을 남긴 채 진행합니다"; }

    # ── ③ pull (네트워크 실패만 재시도) ───────────────────────────
    local i out
    for i in 1 2 3; do
      if out="$(git pull origin "$DEM_BRANCH" 2>&1)"; then
        echo "$out" | tail -3 | sed 's/^/  /'; break
      fi
      if [ "$i" = 3 ]; then
        echo "★ pull 실패:"; echo "$out" | tail -8 | sed 's/^/    /'; exit 3
      fi
      echo "  · pull 재시도 $i/3 …"; sleep $((i*3))
    done

    # ── ④ EIS 카탈로그·피팅 재생성 (pull 이 옛 사본을 지웠으므로) ────
    echo "▶ EIS 재생성"
    python3 scripts/eis_archive.py || { echo "★ eis_archive 실패 — 서버는 재시작하지 않습니다"; exit 4; }
    python3 scripts/eis_fit.py     || { echo "★ eis_fit 실패 — 서버는 재시작하지 않습니다"; exit 5; }
  ) || return $?

  # ── ⑤ 재시작 (위 단계가 전부 성공했을 때만) ──────────────────────
  if [ "$run" = 1 ]; then
    [ -f "$DEM_RUN" ] || { echo "★ $DEM_RUN 없음 — 재시작 건너뜀"; return 6; }
    echo "▶ 재시작: $DEM_RUN"
    bash "$DEM_RUN"
  else
    echo "▶ norun — 서버는 그대로 둡니다"
  fi
}
