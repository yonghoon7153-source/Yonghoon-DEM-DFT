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
# =============================================================================
set -uo pipefail

IN=""; RUNNER_PAT=""; POLL=20; TIMEOUT=14400; EXIT_WAIT=7200; SELFTEST=0; PANE_PIDS_OVERRIDE=""; OUTF=""; NO_RUNNER=0
while [ $# -gt 0 ]; do
  case "$1" in
    --in) IN="$2"; shift ;;
    --runner) RUNNER_PAT="$2"; shift ;;
    --out) OUTF="$2"; shift ;;
    --no_runner) NO_RUNNER=1 ;;
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

main(){
  [ -n "$IN" ] && { [ -n "$RUNNER_PAT" ] || [ "$NO_RUNNER" = 1 ]; } || { echo "⛔ --in 과 (--runner 또는 --no_runner) 가 필요하다"; return 2; }
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
  rm -rf "$T"
  echo "  selftest: ⭕ $ok · ⛔ $bad"; [ "$bad" = 0 ] && exit 0 || exit 1
fi

main
