#!/usr/bin/env bash
# =============================================================================
# pause_relax_at_bfgs.sh — 러너가 돌리는 pw.x relax 를 **BFGS 스텝 직후** EXIT 로 세우고,
#   러너가 다음 점을 띄우지 못하게 막는다. 재개는 러너를 새로 띄우면 BFGS 이력째 이어진다.
#
# 왜 (2026-10-11 · 사용자 '13m bfgs 뜨면 잠정 stop하고 li3nd 로 넘어가자' · '대신 resume 잘 걸려야돼')
#   10-01 에 탄성 strain_23_m 을 같은 방식으로 세웠다 (감시 스크립트 stop23m.sh 는 gabia 에만 있었고
#   레포에 없었다). 두 번째라 시험 붙은 도구로 둔다.
#
# 순서 (하나라도 어긋나면 손대지 않고 멈춘다 — 그때까지 바꾼 것은 되돌린다)
#   ① pw.x 를 **입력 파일 이름**으로 찾는다 (comm = pw.x 인 것 하나만 · 이름으로 죽이지 않는다)
#   ② pw.x 의 조상에서 러너 bash 를 찾는다 (--runner 패턴). **tmux 창 셸(pane pid)이면 거부** —
#      tmux 가 STOP 을 곧바로 풀어 버린다 (CLAUDE.md 2026-09-26).
#   ③ 러너만 kill -STOP · 상태 T 확인 (아니면 CONT 로 되돌리고 거부)
#   ④ .out 의 'number of bfgs steps' 줄 수가 늘면 (= BFGS 갱신 · .bfgs 저장 직후) <cwd>/<prefix>.EXIT 생성
#      — pw.x 가 그 전에 스스로 끝나면 EXIT 를 만들지 않는다 (수렴·nstep 소진도 재개 가능한 상태다)
#   ⑤ pw.x 가 끝날 때까지 기다린다 → .out 마커 · .bfgs · 남은 EXIT 파일 확인
#      ⚠ QE 가 EXIT 를 못 먹고 끝났으면 (스스로 끝난 직후 생성 등) **파일을 지운다** — 남겨 두면
#        재개한 pw.x 가 첫 점검에서 바로 선다.
#   ⑥ 그 다음에만 얼린 러너를 kill -9 (pw.x 가 살아 있을 때 러너를 죽이면 SIGHUP 이 pw.x 로 갈 수 있다)
#   시간 초과 (BFGS 줄이 --timeout 안에 안 늘면) → 러너를 CONT 로 되돌리고 EXIT 를 만들지 않고 끝낸다.
#
# 재개 (이 도구 밖): 러너를 새로 띄운다 — 탄성 러너 `_out_state` 가 'stopped' + .bfgs 를 보고
#   restart_mode='restart' 로 잇는다 (09-27 · selftest). 새 .out 에서 확인할 것:
#   'Atomic positions and unit cell read from directory' · 'initial density is read from file' ·
#   첫 SCF 뒤 'number of bfgs steps' 가 멈춘 번호 다음부터.
#
# ⛔ 이 도구가 못 하는 것
#   · 재개를 하지 않는다 (러너를 새로 띄우는 것은 사람 몫 · 결정 기록과 같이)
#   · 러너가 pw.x 를 mpirun 으로 띄웠는지 몰라도 되지만, 러너가 pw.x 의 **조상이 아니면** 못 찾는다 (거부)
#   · 한 기계의 pw.x 하나만 다룬다 · 같은 입력 이름의 pw.x 가 둘이면 거부한다
#   · 물리를 판정하지 않는다 — '세웠다' 는 미수렴이라는 뜻이다
#
#   bash tools/elastic/pause_relax_at_bfgs.sh --in strain_13_m.in --runner run_elastic_relaxedion_gabia.sh
#   bash tools/elastic/pause_relax_at_bfgs.sh --selftest
#
# 2026-10-19 보탬 (Nd ELF 를 위해 Li₃Nd r2 를 잠깐 세운다 · 사용자 '안되면 잠깐 li3Nd stop하고 해도 되잖아')
#   --out FILE   pw.x 의 출력 파일 (pw.x cwd 기준 · 기본 <입력>.out). restart_qe_relax.sh 는 'X.restart.in' 으로 돌리고
#                'X.out' 에 쓴다 — 기본 규칙으로는 '파일이 없다' 로 거부된다 (그 경우를 selftest 가 잡는다).
#   --no_runner  러너를 얼리지도 죽이지도 않는다 (②③⑥ 생략). pw.x 가 끝난 뒤 **다음 잡을 안 띄우는** 드라이버일 때만 쓴다
#                (restart_qe_relax.sh 는 끝난 잡을 판정·출력만 하고 다시 걸지 않는다 — '▶ … mode=' 다음 줄들).
#   bash tools/elastic/pause_relax_at_bfgs.sh --in 00_control_relax.restart.in --out 00_control_relax.out --no_runner
#
# 2026-10-27 보탬 (Li₂S 4×4×4 를 탄성 13_m 과 12_p 사이에 끼운다 · 사용자 '권고대로 하자 · li2S 진행' ·
#   결정 D-2026-10-09-li2s-neb-cellconv active)
#   --hold FILE     러너만 얼리고 (①②③ 그대로) **EXIT 를 만들지 않는다** — 지금 점 (13_m) 은 끝까지 돌게 두고,
#                   그 pw.x 가 끝나면 러너를 얼린 채 FILE 에 러너 PID · 시작 시각 · 명령줄 · 끝난 점의 상태를 적고 끝난다 (0).
#                   기다리는 동안 누가 러너를 풀면 (T 아님) 10 · --hold_timeout 을 넘으면 러너를 풀고 6.
#                   러너를 죽이지 않는다 — 풀면 러너가 끝난 점을 판정하고 다음 점 (12_p) 을 이어 띄운다.
#   --release FILE  FILE 의 러너를 kill -CONT 로 푼다. PID · 시작 시각 · 명령줄이 FILE 과 다르면 **안 건드린다** (11 · PID 재사용 방지).
#                   이미 풀려 있으면 0 (기록만) · CONT 뒤에도 T 면 12.
#   bash tools/elastic/pause_relax_at_bfgs.sh --in strain_13_m.in --runner run_elastic_relaxedion_gabia.sh --hold /data/work/runs/x/elastic_hold.txt
#   bash tools/elastic/pause_relax_at_bfgs.sh --release /data/work/runs/x/elastic_hold.txt
#   ⛔ 못 하는 것: 붙든 동안 탄성 점을 바꾸거나 판정하지 않는다 · 러너가 얼어 있는 사이 그 자식 pw.x 가 끝나면 좀비가 되지만
#     GPU 는 놓는다 (좀비는 메모리를 안 잡는다) · 이 도구가 SIGKILL 로 죽으면 러너는 언 채 남는다 — 그때는 --release 로 푼다.
# =============================================================================
set -uo pipefail

IN=""; RUNNER_PAT=""; POLL=20; TIMEOUT=14400; EXIT_WAIT=7200; SELFTEST=0; PANE_PIDS_OVERRIDE=""; OUTF=""; NO_RUNNER=0
HOLD=""; RELEASE=""; HOLD_TIMEOUT=1209600
while [ $# -gt 0 ]; do
  case "$1" in
    --in) IN="$2"; shift ;;
    --runner) RUNNER_PAT="$2"; shift ;;
    --out) OUTF="$2"; shift ;;
    --no_runner) NO_RUNNER=1 ;;
    --hold) HOLD="$2"; shift ;;
    --release) RELEASE="$2"; shift ;;
    --hold_timeout) HOLD_TIMEOUT="$2"; shift ;;
    --poll) POLL="$2"; shift ;;
    --timeout) TIMEOUT="$2"; shift ;;
    --exit_wait) EXIT_WAIT="$2"; shift ;;
    --pane_pids) PANE_PIDS_OVERRIDE="$2"; shift ;;   # 시험용 (tmux 없이 pane pid 를 흉내)
    --selftest) SELFTEST=1 ;;
    -h|--help) sed -n '2,40p' "$0"; exit 0 ;;
    *) echo "⛔ 모르는 인자: $1"; exit 2 ;;
  esac; shift
done
ts(){ date '+%F %T'; }
say(){ echo "[$(ts)] $*"; }

find_pw(){   # $1 = 입력 이름 → pw.x PID 들 (comm 으로 거른다 — pgrep 은 자기·래퍼를 센다)
  local x
  for x in $(pgrep -f -- "$1" 2>/dev/null); do
    [ "$(cat /proc/$x/comm 2>/dev/null)" = pw.x ] && echo "$x"
  done
}
find_runner(){   # $1 = pw.x PID · $2 = 러너 패턴 → 조상 중 첫 매치
  local q; q=$(awk '{print $4}' /proc/$1/stat 2>/dev/null)
  while [ -n "$q" ] && [ "$q" != 0 ] && [ "$q" != 1 ]; do
    if tr '\0' ' ' < /proc/$q/cmdline 2>/dev/null | grep -q -- "$2"; then echo "$q"; return 0; fi
    q=$(awk '{print $4}' /proc/$q/stat 2>/dev/null)
  done
  return 1
}
pane_pids(){
  if [ -n "$PANE_PIDS_OVERRIDE" ]; then echo "$PANE_PIDS_OVERRIDE" | tr ',' ' '; return; fi
  command -v tmux >/dev/null && tmux list-panes -a -F '#{pane_pid}' 2>/dev/null | tr '\n' ' '
}
pstat(){ ps -o stat= -p "$1" 2>/dev/null | tr -d ' '; }
alive(){   # 좀비는 끝난 것이다 — 얼린 러너의 직접 자식이면 pw.x 가 끝나도 회수가 안 돼 kill -0 이 계속 참이다
  local s; s=$(pstat "$1"); [ -n "$s" ] && [ "${s#Z}" = "$s" ]; }
inkey(){   # $1 = .in · $2 = 키 → 값 (따옴표 제거)
  grep -aiE "^[[:space:]]*$2[[:space:]]*=" "$1" | head -1 | sed -E "s/^[^=]*=[[:space:]]*//; s/[\"',]//g; s/[[:space:]]+$//"
}
nbfgs(){ grep -ac "number of bfgs steps" "$1" 2>/dev/null || true; }
starttime(){   # /proc/PID/stat 22 번째 칸 — comm 에 빈칸이 있어도 ') ' 뒤에서 센다 (tmux: server 같은 이름에 칸이 밀렸다)
  sed -E 's/^.*\) //' "/proc/$1/stat" 2>/dev/null | awk '{print $20}'; }
cmdline(){ tr '\0' ' ' < "/proc/$1/cmdline" 2>/dev/null | sed 's/ $//'; }
out_state(){   # 끝난 relax 의 상태 — 아래 EXIT 경로와 같은 낱말
  if grep -aq "bfgs converged" "$1"; then echo done
  elif grep -aqi "maximum number of steps has been reached" "$1"; then echo exhausted
  elif grep -aqE "Program stopped by user request|Maximum CPU time exceeded" "$1"; then echo stopped
  else echo other; fi; }

hold_wait(){   # main 의 P · R · C · OUT · IN 을 쓴다 — 러너는 이미 T
  local t0 st; t0=$(date +%s)
  say "붙듦: 러너 $R 얼린 채 pw.x $P 가 스스로 끝나기를 기다린다 (최대 ${HOLD_TIMEOUT} s · EXIT 안 만듦) — 다음 점을 못 띄운다"
  while alive "$P"; do
    case "$(pstat "$R")" in
      T*) ;;
      *) say "⛔ 러너 $R 가 붙든 사이 풀렸다 ($(pstat "$R")) — 누가 CONT 했다. 붙듦을 그만둔다 (아무것도 안 바꿈)"; return 10 ;;
    esac
    if [ $(( $(date +%s) - t0 )) -gt "$HOLD_TIMEOUT" ]; then
      kill -CONT "$R" 2>/dev/null
      say "⛔ ${HOLD_TIMEOUT} s 가 지나도 pw.x 가 안 끝났다 — 러너를 풀고 끝낸다 (상태 $(pstat "$R"))"; return 6
    fi
    sleep "$POLL"
  done
  st=$(out_state "$OUT")
  { echo "runner_pid=$R"; echo "runner_start=$(starttime "$R")"; echo "runner_cmd=$(cmdline "$R")"
    echo "pw_pid=$P"; echo "pw_in=$C/$IN"; echo "pw_out=$OUT"; echo "pw_state=$st"
    echo "pw_bfgs_lines=$(nbfgs "$OUT")"; echo "held_at=$(ts)"; } > "$HOLD"
  say "✅ 붙듦 — pw.x 끝 (상태 $st · BFGS 줄 $(nbfgs "$OUT") · 마지막 $(grep -a 'Total force' "$OUT" | tail -1 | tr -s ' ')) · 러너 $R 얼린 채"
  say "   풀기: bash $0 --release $HOLD"
  return 0
}

release_main(){
  local R ST0 CM0 s
  [ -f "$RELEASE" ] || { say "⛔ 붙듦 파일이 없다: $RELEASE"; return 2; }
  R=$(sed -n 's/^runner_pid=//p' "$RELEASE" | head -1); ST0=$(sed -n 's/^runner_start=//p' "$RELEASE" | head -1)
  CM0=$(sed -n 's/^runner_cmd=//p' "$RELEASE" | head -1)
  [ -n "$R" ] && [ -n "$ST0" ] || { say "⛔ 붙듦 파일에 runner_pid · runner_start 가 없다 — 안 건드린다"; return 2; }
  if grep -q '^released_at=' "$RELEASE"; then say "이미 푼 기록이 있다 ($(sed -n 's/^released_at=//p' "$RELEASE" | tail -1)) — 상태만 본다: $(pstat "$R")"; fi
  kill -0 "$R" 2>/dev/null || { say "⛔ 러너 $R 가 없다 — 풀 것이 없다 (사람이 본다)"; return 11; }
  if [ "$(starttime "$R")" != "$ST0" ] || [ "$(cmdline "$R")" != "$CM0" ]; then
    say "⛔ PID $R 는 붙든 러너가 아니다 (시작 시각 $ST0 → $(starttime "$R") · 명령줄 '$(cmdline "$R" | cut -c1-60)') — 안 건드린다"; return 11
  fi
  s=$(pstat "$R")
  case "$s" in
    T*) kill -CONT "$R"; sleep 1; s=$(pstat "$R")
        case "$s" in T*) say "⛔ CONT 뒤에도 러너 $R 가 T 다"; return 12 ;; esac
        echo "released_at=$(ts)" >> "$RELEASE"; say "✅ 러너 $R 풀림 ($s) — 끝난 점을 판정하고 다음 점을 띄운다" ;;
    *)  echo "released_at=$(ts) (이미 풀려 있었다 · $s)" >> "$RELEASE"; say "러너 $R 는 이미 풀려 있다 ($s) — 기록만 했다" ;;
  esac
  return 0
}

main(){
  [ -n "$RELEASE" ] && { release_main; return $?; }
  [ -n "$IN" ] && { [ -n "$RUNNER_PAT" ] || [ "$NO_RUNNER" = 1 ]; } || { echo "⛔ --in 과 (--runner 또는 --no_runner) 가 필요하다"; return 2; }
  if [ -n "$HOLD" ]; then
    [ "$NO_RUNNER" = 1 ] && { echo "⛔ --hold 는 러너를 얼려야 뜻이 있다 — --no_runner 와 같이 못 쓴다"; return 2; }
    if [ -f "$HOLD" ] && ! grep -q '^released_at=' "$HOLD"; then
      echo "⛔ 붙듦 파일 $HOLD 가 이미 있고 아직 안 풀렸다 — 그 러너부터 --release 로 풀거나 파일을 치운다"; return 2; fi
  fi
  local pids n P C OUT PFX ODIR BFGS R n0 t0 tE ended=0
  pids=$(find_pw "$IN"); n=$(echo "$pids" | grep -c . || true)
  [ "$n" = 1 ] || { say "⛔ '$IN' 을 돌리는 pw.x 가 ${n} 개다 (하나여야 한다) — 아무것도 안 했다"; return 3; }
  P=$pids; C=$(readlink "/proc/$P/cwd")
  if [ -n "$OUTF" ]; then case "$OUTF" in /*) OUT=$OUTF ;; *) OUT="$C/$OUTF" ;; esac; else OUT="$C/${IN%.in}.out"; fi
  [ -f "$C/$IN" ] && [ -f "$OUT" ] || { say "⛔ $C 에 $IN · $(basename "$OUT") 가 없다 — 아무것도 안 했다"; return 3; }
  PFX=$(inkey "$C/$IN" prefix); PFX=${PFX:-pwscf}
  ODIR=$(inkey "$C/$IN" outdir); ODIR=${ODIR:-./}; case "$ODIR" in /*) ;; *) ODIR="$C/$ODIR" ;; esac
  BFGS="$ODIR/$PFX.bfgs"
  if [ "$NO_RUNNER" = 1 ]; then
    R=""
    say "pw.x $P · cwd $C · prefix $PFX · bfgs $BFGS · 출력 $(basename "$OUT") · 러너 안 얼림 (--no_runner)"
  else
    R=$(find_runner "$P" "$RUNNER_PAT") || { say "⛔ pw.x $P 의 조상에 '$RUNNER_PAT' 가 없다 — 아무것도 안 했다"; return 3; }
    for x in $(pane_pids); do
      [ "$x" = "$R" ] && { say "⛔ 러너 $R 가 tmux 창 셸 자체다 — STOP 을 tmux 가 풀어 버린다. 아무것도 안 했다"; return 4; }
    done
    say "pw.x $P · cwd $C · prefix $PFX · bfgs $BFGS · 러너 $R"
    kill -STOP "$R"; sleep 1
    case "$(pstat "$R")" in
      T*) say "러너 $R 얼림 (T) — 13_m 같은 이 점이 끝나도 다음 점을 못 띄운다" ;;
      *)  kill -CONT "$R" 2>/dev/null; say "⛔ 러너 상태가 T 가 아니다 ($(pstat "$R")) — CONT 로 되돌리고 멈춘다"; return 5 ;;
    esac
  fi
  if [ -n "$HOLD" ]; then hold_wait; return $?; fi
  n0=$(nbfgs "$OUT"); t0=$(date +%s); say "BFGS 줄 ${n0} 개에서 다음 줄을 기다린다 (최대 ${TIMEOUT} s)"
  while :; do
    if ! alive "$P"; then ended=1; say "pw.x 가 스스로 끝났다 — EXIT 를 만들지 않는다"; break; fi
    if [ "$(nbfgs "$OUT")" -gt "$n0" ]; then
      : > "$C/$PFX.EXIT"; tE=$(date +%s); say "BFGS 줄 $(nbfgs "$OUT") — $C/$PFX.EXIT 생성"; break
    fi
    if [ $(( $(date +%s) - t0 )) -gt "$TIMEOUT" ]; then
      [ -n "$R" ] && kill -CONT "$R" 2>/dev/null
      say "⛔ ${TIMEOUT} s 안에 BFGS 줄이 안 늘었다 — EXIT 없이 끝낸다$([ -n "$R" ] && echo " · 러너를 CONT 로 되돌림 (상태 $(pstat "$R"))")"; return 6
    fi
    sleep "$POLL"
  done
  if [ "$ended" = 0 ]; then
    local tw; tw=$(date +%s)
    while alive "$P"; do
      [ $(( $(date +%s) - tw )) -gt "$EXIT_WAIT" ] && { say "⛔ EXIT 뒤 ${EXIT_WAIT} s 가 지나도 pw.x 가 안 끝났다 — 러너는 얼린 채 둔다 (사람이 본다)"; return 7; }
      sleep "$POLL"
    done
    say "pw.x 끝 ($(( $(date +%s) - tE )) s 뒤)"
  fi
  local st="?"
  if grep -aq "bfgs converged" "$OUT"; then st=done
  elif grep -aqi "maximum number of steps has been reached" "$OUT"; then st=exhausted
  elif grep -aqE "Program stopped by user request|Maximum CPU time exceeded" "$OUT"; then st=stopped
  fi
  if [ -e "$C/$PFX.EXIT" ]; then rm -f "$C/$PFX.EXIT"; say "⚠ QE 가 EXIT 파일을 안 먹었다 — 지웠다 (남기면 재개한 pw.x 가 바로 선다)"; fi
  if [ -f "$BFGS" ]; then say ".bfgs $(sha256sum "$BFGS" | cut -c1-8) · $(date -r "$BFGS" '+%F %T')"; else say "⚠ .bfgs 없음 ($BFGS) — 재개는 처음부터가 된다"; fi
  say "상태 = $st · BFGS 줄 $(nbfgs "$OUT") · 마지막 $(grep -a 'Total force' "$OUT" | tail -1 | tr -s ' ')"
  case "$st" in done|exhausted|stopped) ;; *) say "⛔ 재개 가능한 상태가 아니다 ($st) — 러너는 얼린 채 둔다 (사람이 본다)"; return 8 ;; esac
  if [ -z "$R" ]; then
    say "✅ 세움 (러너 안 얼림 · --no_runner) · 재개 = 드라이버를 새로 띄운다 (stopped/exhausted + .bfgs → restart)"
    return 0
  fi
  kill -9 "$R" 2>/dev/null; sleep 1
  kill -0 "$R" 2>/dev/null && { say "⛔ 러너 $R 가 아직 있다"; return 9; }
  say "✅ 러너 $R 종료 · 다음 점 안 띄움 · 재개 = 러너를 새로 띄운다 (stopped/exhausted + .bfgs → restart)"
  return 0
}

if [ "$SELFTEST" = 1 ]; then
  T=$(mktemp -d); ok=0; bad=0; XN="st$$_x"   # 입력 이름을 실행마다 다르게 — 병렬 selftest 가 서로의 가짜 pw.x 를 세지 않게
  ck(){ if [ "$2" = "$3" ]; then echo "  ⭕ $1"; ok=$((ok+1)); else echo "  ⛔ $1 — 얻음 '$2' · 기대 '$3'"; bad=$((bad+1)); fi; }
  mkdir -p "$T/bin"
  # 가짜 pw.x: BFGS 줄을 STEP 초마다 쓰고, <prefix>.EXIT 가 보이면 QE 처럼 멈춘다 (파일을 지운다)
  cat > "$T/bin/pw.x" <<'EOF'
#!/bin/bash
in=$2; out=${OUTNAME:-${in%.in}.out}; k=0; : > "$out"; mkdir -p tmp
while :; do
  sleep "${STEP:-1}"; k=$((k+1)); echo "     number of bfgs steps    = $k" >> "$out"; echo "$k" > tmp/fk.bfgs
  echo "     Total force =     0.0$k" >> "$out"
  if [ -e fk.EXIT ] && [ "${IGNORE_EXIT:-0}" != 1 ]; then rm -f fk.EXIT; printf '\n     Program stopped by user request\nJOB DONE.\n' >> "$out"; exit 0; fi
  if [ "$k" -ge "${CONV_AT:-999}" ]; then printf '     bfgs converged in  %s scf cycles and  %s bfgs steps\nJOB DONE.\n' "$k" "$k" >> "$out"; exit 0; fi
  if [ "$k" -ge "${MAXK:-999}" ]; then printf '     The maximum number of steps has been reached.\nJOB DONE.\n' >> "$out"; exit 0; fi
done
EOF
  # 가짜 러너: pw.x 를 자식으로 돌리고, 끝나면 '다음 점' 을 띄운다 (얼려 두면 못 띄워야 한다)
  cat > "$T/bin/fake_elastic_runner.sh" <<'EOF'
#!/bin/bash
cd "$1" && "$2/pw.x" -in "$3.in"; echo started > "$1/next_point_started"; sleep 30
EOF
  chmod +x "$T/bin/pw.x" "$T/bin/fake_elastic_runner.sh"
  mkjob(){ mkdir -p "$T/$1"; printf "&CONTROL\n  calculation = 'relax'\n  prefix = 'fk'\n  outdir = './tmp'\n/\n&IONS\n/\n" > "$T/$1/$XN.in"; }
  cleanup(){ local x; for x in $(pgrep -f "$T/bin/"); do kill -9 "$x" 2>/dev/null; done; sleep 0.3; }
  run_case(){  # $1 = 폴더 · 나머지 = 환경 → rc
    local d=$1; shift
    env "$@" "$T/bin/fake_elastic_runner.sh" "$T/$d" "$T/bin" "$XN" & local rp=$!; disown $rp
    sleep 1.5
    ( cd "$T/$d" && IN=$XN.in RUNNER_PAT=fake_elastic_runner.sh POLL=0.3 TIMEOUT=20 EXIT_WAIT=20 PANE_PIDS_OVERRIDE="${PANES:-}" main ) > "$T/$d.log" 2>&1
    local rc=$?; cleanup; echo $rc
  }
  mkjob a; rc=$(run_case a STEP=1)
  ck "양성: BFGS 줄 뒤 EXIT → 세움 · rc 0" "$rc" 0
  ck "양성: .out 에 'Program stopped by user request'" "$(grep -c 'Program stopped by user request' "$T/a/$XN.out")" 1
  ck "⛔음성: 러너가 다음 점을 못 띄웠다 (얼림이 먹었다)" "$([ -e "$T/a/next_point_started" ] && echo yes || echo no)" no
  ck "양성: EXIT 파일이 남지 않았다" "$([ -e "$T/a/fk.EXIT" ] && echo yes || echo no)" no
  ck "양성: 로그에 '상태 = stopped' 한 줄" "$(grep -c '상태 = stopped' "$T/a.log")" 1
  ck "양성: 로그에 .bfgs 해시 한 줄" "$(grep -cE '\] \.bfgs [0-9a-f]{8} ' "$T/a.log")" 1
  # ⛔ 러너가 tmux 창 셸 자체면 거부하고 아무것도 안 바꾼다
  mkjob b; STEP=1 "$T/bin/fake_elastic_runner.sh" "$T/b" "$T/bin" "$XN" & rpb=$!; disown $rpb; sleep 1.5
  ( cd "$T/b" && IN=$XN.in RUNNER_PAT=fake_elastic_runner.sh POLL=0.3 TIMEOUT=5 EXIT_WAIT=5 PANE_PIDS_OVERRIDE="$rpb" main ) > "$T/b.log" 2>&1; rcb=$?
  ck "⛔음성: 러너 = tmux 창 셸 → 거부 rc 4" "$rcb" 4
  ck "⛔음성: 거부했으면 러너를 얼리지 않았다" "$(ps -o stat= -p $rpb | tr -d ' ' | cut -c1)" S
  ck "⛔음성: 거부했으면 EXIT 를 만들지 않았다" "$([ -e "$T/b/fk.EXIT" ] && echo yes || echo no)" no
  cleanup
  # ⛔ 맞는 pw.x 가 없으면 아무것도 안 한다
  ( IN=nothing_here.in RUNNER_PAT=fake_elastic_runner.sh main ) > "$T/c.log" 2>&1
  ck "⛔음성: 대상 pw.x 없음 → rc 3" "$?" 3
  # 스스로 수렴해 끝나면 EXIT 를 만들지 않고 러너만 막는다 (BFGS 줄이 늘기 전 끝나도록 CONV_AT=1)
  mkjob d; rcd=$(run_case d STEP=2 CONV_AT=1)
  ck "경계: 첫 BFGS 줄과 함께 수렴 → done · rc 0" "$rcd" 0
  ck "⛔음성: 수렴으로 끝나도 다음 점은 못 띄웠다" "$([ -e "$T/d/next_point_started" ] && echo yes || echo no)" no
  # QE 가 EXIT 를 안 먹고 다른 이유로 끝나면 남은 EXIT 파일을 지운다 (재개 즉시 정지 방지)
  mkjob e; rce=$(run_case e STEP=1 IGNORE_EXIT=1 MAXK=5)
  ck "경계 전제: EXIT 를 실제로 만들었다 (안 만들었으면 아래 두 시험은 헛것이다)" "$(grep -c 'EXIT 생성' "$T/e.log")" 1
  ck "경계: EXIT 무시·nstep 소진 → exhausted · rc 0" "$rce" 0
  ck "⛔음성: 남은 EXIT 파일을 지웠다" "$([ -e "$T/e/fk.EXIT" ] && echo yes || echo no)" no
  ck "경계: 로그에 'EXIT 파일을 안 먹었다'" "$(grep -c 'EXIT 파일을 안 먹었다' "$T/e.log")" 1
  # 시간 초과 → 러너를 되돌리고 EXIT 없음 (러너 상태를 직접 본다 — 로그만 보지 않는다)
  mkjob f; STEP=30 "$T/bin/fake_elastic_runner.sh" "$T/f" "$T/bin" "$XN" & rpf=$!; disown $rpf; sleep 1.5
  ( cd "$T/f" && IN=$XN.in RUNNER_PAT=fake_elastic_runner.sh POLL=0.3 TIMEOUT=2 EXIT_WAIT=5 main ) > "$T/f.log" 2>&1; rcf=$?
  ck "⛔음성: BFGS 줄이 시간 안에 안 늘면 rc 6" "$rcf" 6
  ck "⛔음성: 시간 초과면 EXIT 를 만들지 않았다" "$([ -e "$T/f/fk.EXIT" ] && echo yes || echo no)" no
  ck "⛔음성: 시간 초과면 러너를 되돌렸다 (상태 T 아님)" "$(ps -o stat= -p $rpf | tr -d ' ' | cut -c1)" S
  cleanup
  # ── 2026-10-19 보탬: --out · --no_runner (restart_qe_relax.sh 꼴 — 'X.restart.in' 으로 돌리고 'X.out' 에 쓴다) ──
  cat > "$T/bin/fake_relax_driver.sh" <<'EOF'
#!/bin/bash
cd "$1" && OUTNAME="$3.out" "$2/pw.x" -in "$3.restart.in"; echo judged > "$1/driver_done"
EOF
  chmod +x "$T/bin/fake_relax_driver.sh"
  mkr(){ mkjob "$1"; cp "$T/$1/$XN.in" "$T/$1/$XN.restart.in"; }
  mkr g; env STEP=1 "$T/bin/fake_relax_driver.sh" "$T/g" "$T/bin" "$XN" & rpg=$!; disown $rpg; sleep 1.5
  ( cd "$T/g" && IN=$XN.restart.in POLL=0.3 TIMEOUT=20 EXIT_WAIT=20 main ) > "$T/g0.log" 2>&1; rcg0=$?
  ck "⛔음성: --runner 도 --no_runner 도 없으면 rc 2" "$rcg0" 2
  ( cd "$T/g" && IN=$XN.restart.in NO_RUNNER=1 POLL=0.3 TIMEOUT=20 EXIT_WAIT=20 main ) > "$T/g1.log" 2>&1; rcg1=$?
  ck "⛔음성: --out 없이 restart.in 잡 → '<입력>.out 없음' 으로 거부 rc 3" "$rcg1" 3
  ck "⛔음성: 거부했으면 EXIT 를 만들지 않았다" "$([ -e "$T/g/fk.EXIT" ] && echo yes || echo no)" no
  ( cd "$T/g" && IN=$XN.restart.in OUTF=$XN.out NO_RUNNER=1 POLL=0.3 TIMEOUT=20 EXIT_WAIT=20 main ) > "$T/g.log" 2>&1; rcg=$?
  sleep 1
  ck "양성: --out + --no_runner → BFGS 줄 뒤 EXIT → 세움 · rc 0" "$rcg" 0
  ck "양성: X.out 에 'Program stopped by user request'" "$(grep -c 'Program stopped by user request' "$T/g/$XN.out")" 1
  ck "양성: 러너를 얼리지 않았다 — 드라이버가 판정 단계까지 갔다" "$([ -e "$T/g/driver_done" ] && echo yes || echo no)" yes
  ck "양성: EXIT 파일이 남지 않았다" "$([ -e "$T/g/fk.EXIT" ] && echo yes || echo no)" no
  ck "양성: 로그에 '러너 안 얼림' 두 줄 (시작 · 끝)" "$(grep -c '러너 안 얼림' "$T/g.log")" 2
  cleanup
  mkr h; env STEP=1 "$T/bin/fake_relax_driver.sh" "$T/h" "$T/bin" "$XN" & rph=$!; disown $rph; sleep 1.5
  ( cd "$T/h" && IN=$XN.restart.in OUTF=no_such.out NO_RUNNER=1 POLL=0.3 TIMEOUT=5 EXIT_WAIT=5 main ) > "$T/h.log" 2>&1; rch=$?
  ck "⛔음성: --out 이 없는 파일이면 rc 3 · EXIT 안 만듦" "$rch:$([ -e "$T/h/fk.EXIT" ] && echo yes || echo no)" "3:no"
  cleanup
  mkr i; env STEP=30 "$T/bin/fake_relax_driver.sh" "$T/i" "$T/bin" "$XN" & rpi=$!; disown $rpi; sleep 1.5
  ( cd "$T/i" && IN=$XN.restart.in OUTF=$XN.out NO_RUNNER=1 POLL=0.3 TIMEOUT=2 EXIT_WAIT=5 main ) > "$T/i.log" 2>&1; rci=$?
  ck "⛔음성: --no_runner 시간 초과 → rc 6 · EXIT 안 만듦" "$rci:$([ -e "$T/i/fk.EXIT" ] && echo yes || echo no)" "6:no"
  cleanup
  # ── 2026-10-27 보탬: --hold · --release (지금 점은 끝까지 · 다음 점만 막는다 · 풀면 다음 점) ──
  yn(){ [ -e "$1" ] && echo yes || echo no; }
  st1(){ pstat "$1" | cut -c1; }
  mkjob ha; env STEP=1 CONV_AT=3 "$T/bin/fake_elastic_runner.sh" "$T/ha" "$T/bin" "$XN" & rpa=$!; disown $rpa; sleep 1.5
  ( cd "$T/ha" && IN=$XN.in RUNNER_PAT=fake_elastic_runner.sh POLL=0.3 HOLD="$T/ha/hold.txt" HOLD_TIMEOUT=30 main ) > "$T/ha.log" 2>&1; rca=$?
  ck "양성(hold): 지금 점이 스스로 끝날 때까지 붙듦 → rc 0" "$rca" 0
  ck "양성(hold): EXIT 를 안 만들었다 — 점이 스스로 수렴했다" "$(grep -c 'bfgs converged' "$T/ha/$XN.out"):$(grep -c 'Program stopped' "$T/ha/$XN.out")" "1:0"
  ck "⛔음성(hold): 붙든 동안 다음 점을 못 띄웠다" "$(yn "$T/ha/next_point_started")" no
  ck "양성(hold): 러너는 언 채 (T) · 죽이지 않았다" "$(st1 $rpa)" T
  ck "양성(hold): 붙듦 파일 runner_pid · pw_state" "$(sed -n 's/^runner_pid=//p' "$T/ha/hold.txt"):$(sed -n 's/^pw_state=//p' "$T/ha/hold.txt")" "$rpa:done"
  ( RELEASE="$T/ha/hold.txt" main ) > "$T/ha_rel.log" 2>&1; rcr=$?; sleep 1.5
  ck "양성(release): rc 0 · 풀린 러너가 다음 점을 띄웠다" "$rcr:$(yn "$T/ha/next_point_started")" "0:yes"
  ck "양성(release): 붙듦 파일에 released_at 한 줄" "$(grep -c '^released_at=' "$T/ha/hold.txt")" 1
  cleanup
  mkjob hb; env STEP=1 CONV_AT=40 "$T/bin/fake_elastic_runner.sh" "$T/hb" "$T/bin" "$XN" & rpb2=$!; disown $rpb2; sleep 1.5
  ( cd "$T/hb" && IN=$XN.in RUNNER_PAT=fake_elastic_runner.sh POLL=0.3 HOLD="$T/hb/hold.txt" HOLD_TIMEOUT=30 main ) > "$T/hb.log" 2>&1 & hp=$!
  sleep 2; kill -CONT $rpb2; wait $hp; rchb=$?
  ck "⛔음성(hold): 붙든 사이 누가 풀면 rc 10 · 붙듦 파일 안 씀" "$rchb:$(yn "$T/hb/hold.txt")" "10:no"
  cleanup
  mkjob hc; env STEP=30 "$T/bin/fake_elastic_runner.sh" "$T/hc" "$T/bin" "$XN" & rpc=$!; disown $rpc; sleep 1.5
  ( cd "$T/hc" && IN=$XN.in RUNNER_PAT=fake_elastic_runner.sh POLL=0.3 HOLD="$T/hc/hold.txt" HOLD_TIMEOUT=2 main ) > "$T/hc.log" 2>&1; rchc=$?
  ck "⛔음성(hold): 시간 초과면 rc 6 · 러너를 풀었다 (T 아님)" "$rchc:$(st1 $rpc)" "6:S"
  ck "⛔음성(hold): 시간 초과면 EXIT 도 붙듦 파일도 없다" "$(yn "$T/hc/fk.EXIT"):$(yn "$T/hc/hold.txt")" "no:no"
  cleanup
  mkjob hd; env STEP=1 CONV_AT=2 "$T/bin/fake_elastic_runner.sh" "$T/hd" "$T/bin" "$XN" & rpd=$!; disown $rpd; sleep 1.5
  ( cd "$T/hd" && IN=$XN.in RUNNER_PAT=fake_elastic_runner.sh POLL=0.3 HOLD="$T/hd/hold.txt" HOLD_TIMEOUT=30 main ) > "$T/hd.log" 2>&1
  sed -i 's/^runner_start=.*/runner_start=1/' "$T/hd/hold.txt"
  ( RELEASE="$T/hd/hold.txt" main ) > "$T/hd_rel.log" 2>&1; rcd=$?
  ck "⛔음성(release): 시작 시각이 다르면 안 건드린다 rc 11 · 러너 언 채" "$rcd:$(st1 $rpd)" "11:T"
  kill -CONT $rpd 2>/dev/null; cleanup
  ( IN=x.in NO_RUNNER=1 HOLD="$T/x_hold.txt" main ) > /dev/null 2>&1
  ck "⛔음성(hold): --hold + --no_runner → rc 2" "$?" 2
  mkjob he; env STEP=1 CONV_AT=40 "$T/bin/fake_elastic_runner.sh" "$T/he" "$T/bin" "$XN" & rpe=$!; disown $rpe; sleep 1.5
  echo "runner_pid=1" > "$T/he/hold.txt"
  ( cd "$T/he" && IN=$XN.in RUNNER_PAT=fake_elastic_runner.sh POLL=0.3 HOLD="$T/he/hold.txt" main ) > "$T/he.log" 2>&1; rce=$?
  ck "⛔음성(hold): 안 푼 붙듦 파일이 있으면 rc 2 · 러너 안 얼림" "$rce:$(st1 $rpe)" "2:S"
  cleanup
  printf "runner_pid=999999\nrunner_start=1\nrunner_cmd=x\n" > "$T/gone.txt"
  ( RELEASE="$T/gone.txt" main ) > /dev/null 2>&1
  ck "⛔음성(release): 러너가 없으면 rc 11" "$?" 11
  rm -rf "$T"
  echo "  selftest: ⭕ $ok · ⛔ $bad"; [ "$bad" = 0 ] && exit 0 || exit 1
fi

main
