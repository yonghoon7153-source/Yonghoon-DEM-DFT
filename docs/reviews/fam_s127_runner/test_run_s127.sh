#!/bin/bash
# test_run_s127.sh — run_s127.sh 시험 (가짜 HOME · 가짜 $PY / git / nvidia-smi / pgrep / sleep / date)
# 쓰기:  bash test_run_s127.sh [RUNNER]        기본 RUNNER = 이 폴더의 run_s127.sh
# 가짜 시계: sleep 은 시계 파일만 앞당기고, 도는 가짜 python 이 그 시각을 처리할 때까지 기다린다 (결정적).
# 가짜 python: 봉인 코드(mpm3d_7f44.py)의 로그 문자열을 흉내 · 값 줄에 LEAKCANARY 를 심어 새는지 본다.
# 기대 argv = expected_argv.py 가 등록 문안(§12-7 · 970–986 행)과 건식 줄(19-1..19-4)을 따로 읽어 만든다.
set -u
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
R_IN=${1:-$HERE/run_s127.sh}
RUNNER=$(cd "$(dirname "$R_IN")" && pwd -P)/$(basename "$R_IN")
REPO=${REPO:-$(git -C "$HERE" rev-parse --show-toplevel)}
PREREG=$REPO/docs/reviews/fam_platen_prereg_20260812.md
BASE=${FAM_RUNNER_TEST_DIR:-$(mktemp -d)}  # 시험 자리 (리포 밖 · 기본 = 새 임시 폴더)
mkdir -p "$BASE"
SEALED_SRC=$BASE/mpm3d_7f44.py  # 봉인 코드 바이트 = git show 7f44d6534 (md5 아래에서 대조)
[ -f "$SEALED_SRC" ] || git -C "$REPO" show 7f44d6534d864f7be2f3310fa55d213b65cc707d:scripts/mpm3d_compaction.py > "$SEALED_SRC"
SEAL_FULL=7f44d6534d864f7be2f3310fa55d213b65cc707d
CSV_COMMIT=cf5103c948fffce69a1126331dc462fd9dd0a83c
RD=$(command -v date); RS=$(command -v sleep); PY3=$(command -v python3); REALGIT=$(command -v git)
DEADLINE=$("$RD" -u -d 2026-11-21T03:00:00Z +%s)
START=$(TZ=KST-9 "$RD" -d '2026-11-05 00:00:00' +%s)
WORK=$BASE/work; CACHE=$BASE/cache; ASSETS=$CACHE/assets
NV_ARGS='--query-gpu=memory.total,memory.free --format=csv,noheader,nounits'
PG_ARGS='-af [m]pm3d_compaction.py'
ARMS4=(confirm_fb corner_fb corner_fa corner_f0)
C15AM=docs/data/case15_corner_20261001/case15_am_scaffold.csv
C15SE=docs/data/case15_corner_20261001/case15_se_scaffold.csv
R14AM=docs/data/real14_am_scaffold.csv
R14SE=docs/data/real14_se_scaffold.csv

T_PASS=0; T_FAIL=0; FAILS=(); CUR=""
pass() { T_PASS=$((T_PASS + 1)); echo "  ok   [$CUR] $1"; }
fail() { T_FAIL=$((T_FAIL + 1)); FAILS+=("[$CUR] $1"); echo "  FAIL [$CUR] $1"; }
chk() { local d=$1; shift; if "$@" > /dev/null 2>&1; then pass "$d"; else fail "$d"; fi; }
nchk() { local d=$1; shift; if "$@" > /dev/null 2>&1; then fail "$d"; else pass "$d"; fi; }
cnt_eq() { [ "$(grep -cE -- "$2" "$1" 2>/dev/null)" = "$3" ]; }
all_lines_eq() { [ ! -f "$1" ] && return 0; [ "$(grep -cvxF -- "$2" "$1")" = 0 ]; }
order_ok() { local f=$1 prev=0 n re; shift; for re in "$@"; do n=$(grep -nE -m1 -- "$re" "$f" | cut -d: -f1); [ -n "$n" ] && [ "$n" -gt "$prev" ] || return 1; prev=$n; done; }
kst() { TZ=KST-9 "$RD" -d "@$1" '+%F %T %Z'; }

die() { echo "HARNESS ERROR: $*" >&2; exit 99; }
[ -f "$RUNNER" ] || die "runner missing: $RUNNER"
[ "$(md5sum < "$SEALED_SRC" | cut -c1-32)" = c31f0512021d416702e162709c6f4400 ] || die "sealed copy md5 mismatch"
[ "$DEADLINE" = 1795230000 ] || die "deadline epoch"

prep_assets() {
  mkdir -p "$ASSETS"
  local spec base
  for spec in "$CSV_COMMIT:$C15AM" "$CSV_COMMIT:$C15SE" "$SEAL_FULL:$R14AM" "$SEAL_FULL:$R14SE"; do
    base=${spec##*/}
    [ -s "$ASSETS/$base" ] || "$REALGIT" -C "$REPO" show "$spec" > "$ASSETS/$base" || die "git show $spec"
  done
  ( cd "$ASSETS" && sha256sum -c --quiet - ) <<EOF || die "asset sha256"
275c56e12fe11294fe6bf2cb304ce4187ee3fb3cb2f7ccdd8a5fc92d770383ba  case15_am_scaffold.csv
929a495e4599dc55f09b2348b5b8b7fe41ecda131bfdbfae08ca0597d1ae0d1f  case15_se_scaffold.csv
281ad86e0465a13b6ed96dbcf30c76acf4f372ff9d7c4a7e36fe55ecd44413fd  real14_am_scaffold.csv
159f4ac05973197e71019e9f541b6cb1517ef7a75c0790f935d1ccfb4c526640  real14_se_scaffold.csv
EOF
}

# ---------------------------------------------------------------- stubs (sed: @FAKE@ @RS@ @RD@ @PY3@ @GIT@)
stub_python() { cat <<'EOF'
#!/bin/bash
# fake $PY: emulates the sealed program's log strings; value lines carry LEAKCANARY
F='@FAKE@'; RS='@RS@'; PY3='@PY3@'
if [ "${1:-}" = "-c" ]; then
  echo version >> "$F/calls"
  printf '%s' "${2:-}" > "$F/version_code"
  if [ -e "$F/py_c_fail" ]; then echo "ModuleNotFoundError: No module named 'taichi'" >&2; exit 1; fi
  PYTHONPATH="$F/pymods" exec "$PY3" -c "${2:-}"
fi
json=""; prev=""
for a in "$@"; do [ "$prev" = "--save-metrics" ] && json=$a; prev=$a; done
arm=${json##*/}; arm=${arm%.json}; arm=${arm#fam_s127_}; [ -n "$arm" ] || arm=noarm
echo "arm $arm" >> "$F/calls"
printf '%s\0' "$0" "$@" > "$F/argv_$arm"
pwd -P > "$F/cwd_$arm"
if [ ! -f "${2:-/nonexistent}" ]; then echo "python3: can't open file '$PWD/${2:-}': [Errno 2] No such file or directory"; exit 2; fi
prev=""
for a in "$@"; do
  case $prev in --am-scaffold|--se-dump) [ -f "$a" ] || { echo "Traceback (most recent call last):"; echo "FileNotFoundError: $a"; exit 1; };; esac
  prev=$a
done
mode=converge; [ "$arm" = corner_f0 ] && mode=f0json
[ -f "$F/mode_$arm" ] && read -r mode < "$F/mode_$arm"
startup=0; line_s=10; lines_final=6; dur=60
[ -f "$F/time_$arm" ] && read -r startup line_s lines_final dur < "$F/time_$arm"
termmode=ok; [ -f "$F/term_$arm" ] && read -r termmode < "$F/term_$arm"
echo $$ > "$F/stub.pid.tmp"; mv -f "$F/stub.pid.tmp" "$F/stub.pid"
trap 'rm -f "$F/stub.pid"' EXIT
on_term() { cp "$F/clock" "$F/got_term_$arm"; [ "$termmode" = ignore ] && return 0; exit 143; }
trap on_term TERM
read -r t0 < "$F/clock"
grid=384; pts=45870816; case $arm in corner_*) grid=768; pts=94000000;; esac
echo "[Taichi] version 1.7.3, llvm 15.0.4, commit 5ec301be, linux, python 3.10.12 (arm log LEAKCANARY)"
echo "[Taichi] Starting on arch=cuda"
echo "  [platen] v=0.0123 box/t.u.  V/c_P=0.010  V/c_S=0.07  step=0.00049 box/frame  (--platen-mach)  LEAKCANARY"
echo "3D MPM  grid=$grid  pts=$pts  arch=cuda  scaffold (LEAKCANARY)  target=0.3 GPa  readout=wallP  xy=walls"
written=0
frame_line() { printf '  frame %3d [servo]  wallP= 0.0574 GPa (wallP=0.0574 σzz_vol=0.0450)  porosity= 14.21%%  wall_z=0.412  thickness=29.4917µm  LEAKCANARY\n' "$((5 * $1))"; }
want() { local c=0; if [ "$1" -ge "$startup" ]; then c=$((1 + ($1 - startup) / line_s)); fi; [ "$c" -gt "$lines_final" ] && c=$lines_final; echo "$c"; }
emit_to() { while [ "$written" -lt "$1" ]; do frame_line "$written"; written=$((written + 1)); done; }
marker() { echo "  ✓ converged: σzz equilibrated at target"; }
final_line() { echo "FINAL  wallP=0.0574 GPa  porosity(settled)=14.21%  porosity@target=14.21%  thickness=29.4917µm   [MPM, scaffold, LEAKCANARY]"; }
write_json() { printf '{\n  "thickness_um": 29.4917,\n  "porosity_at_target_pct": 14.21,\n  "note": "LEAKCANARY"\n}\n' > "$json"; echo "  saved metrics → $json  (57 fields)"; }
servo_exit() { printf '\n[servo] 평형이 밴드 안에서 수렴하지 않았습니다 — 결과를 내보내지 않고 중단합니다.\n  servo_status = %s   프로브 0회, 마지막 창 스프레드 n/a\n  wallP_end = 0.0574 GPa vs 목표 0.3000 (밴드 ±5%%), conv=0/12  LEAKCANARY\n' "$1" >&2; exit 1; }
tb() { printf 'Traceback (most recent call last):\n  File "scripts/mpm3d_compaction.py", line 3909, in <module>\n%s  LEAKCANARY\n' "$1"; }
finish() {
  emit_to "$lines_final"
  case $mode in
    converge)  marker; final_line; write_json; exit 0;;
    f0json|nomarker) final_line; write_json; exit 0;;
    budget)    final_line; servo_exit not_converged_frame_budget;;
    probe_not_at_rest) final_line; servo_exit not_converged_probe_not_at_rest;;
    traceback) marker; final_line; write_json; tb "RuntimeError: boom"; exit 0;;
    cuda)      marker; final_line; write_json; echo "[E 11/05/26 00:01:00.000 4242] [cuda_driver.h:operator()@92] CUDA Error CUDA_ERROR_ILLEGAL_ADDRESS: an illegal memory access was encountered  LEAKCANARY"; exit 0;;
    rc1)       marker; final_line; write_json; exit 1;;
    nojson)    marker; final_line; exit 0;;
    crash)     tb "ValueError: synthetic crash"; exit 1;;
    cuda_oom)  echo "[E 11/05/26 00:01:00.000 4242] [cuda_driver.h:operator()@92] CUDA Error CUDA_ERROR_OUT_OF_MEMORY: out of memory while calling mem_alloc (cuMemAlloc_v2)  LEAKCANARY"; tb "RuntimeError: [cuda_driver.h:operator()@92] CUDA Error CUDA_ERROR_OUT_OF_MEMORY"; exit 1;;
    *) echo "stub: unknown mode $mode" >> "$F/ERRORS"; exit 99;;
  esac
}
last=""
while :; do
  read -r c < "$F/clock"
  if [ "$c" != "$last" ]; then
    e=$((c - t0)); echo "$c" > "$F/last_seen_$arm"
    [ "$e" -ge "$dur" ] && finish
    emit_to "$(want "$e")"
    echo "$$ $c" > "$F/ack.tmp"; mv -f "$F/ack.tmp" "$F/ack"
    last=$c
  fi
  "$RS" 0.005
done
EOF
}

stub_sleep() { cat <<'EOF'
#!/bin/bash
# fake sleep: advances the clock file; waits until a running fake python has processed the old and new tick
F='@FAKE@'; RS='@RS@'
n=${1:-}
case $n in ''|*[!0-9]*) echo "fake sleep: bad arg '$*'" >> "$F/ERRORS"; exit 1;; esac
echo "$n" >> "$F/sleeps"
me=$$; parent=$PPID
alive_nz() { local st="" rest; { read -r st < "/proc/$1/stat"; } 2>/dev/null || return 1; rest=${st##*) }; set -- $rest; [ "${1:-Z}" != Z ]; }
find_child() { local d p st rest; for d in /proc/[0-9]*; do p=${d#/proc/}; [ "$p" = "$me" ] && continue; st=""; { read -r st < "$d/stat"; } 2>/dev/null || continue; rest=${st##*) }; set -- $rest; [ "${2:-}" = "$parent" ] || continue; [ "$1" = Z ] && continue; echo "$p"; return 0; done; return 1; }
wait_ack() { local i=0 a; while alive_nz "$1"; do a=""; { read -r a < "$F/ack"; } 2>/dev/null; [ "$a" = "$1 $2" ] && return 0; i=$((i + 1)); if [ "$i" -gt 10000 ]; then echo "fake sleep: ack timeout pid=$1 clock=$2" >> "$F/ERRORS"; return 1; fi; "$RS" 0.002; done; return 0; }
read -r c < "$F/clock"
ch=$(find_child) || ch=""
[ -n "$ch" ] && wait_ack "$ch" "$c"
c2=$((c + n))
echo "$c2" > "$F/clock.tmp"; mv -f "$F/clock.tmp" "$F/clock"
if [ -f "$F/events" ]; then
  k=0
  while read -r at verb path val; do
    k=$((k + 1)); [ -n "${at:-}" ] || continue
    [ "$c2" -ge "$at" ] || continue
    [ -e "$F/event_done_$k" ] && continue
    : > "$F/event_done_$k"
    case $verb in touch) : > "$path";; put) echo "$val" > "$path";; rm) rm -f "$path";; esac
  done < "$F/events"
fi
[ -n "$ch" ] && wait_ack "$ch" "$c2"
exit 0
EOF
}

stub_date() { cat <<'EOF'
#!/bin/bash
# fake date: "now" = clock file; -d/-r/-f conversions go to the real date
F='@FAKE@'; RD='@RD@'
for a in "$@"; do case $a in -d|-d?*|--date|--date=*|-r|-r?*|--reference*|-f|-f?*|--file*) exec "$RD" "$@";; esac; done
read -r c < "$F/clock"
exec "$RD" -d "@$c" "$@"
EOF
}

stub_nvidia() { cat <<'EOF'
#!/bin/bash
F='@FAKE@'
printf '%s\n' "$*" >> "$F/nv_args"
if [ -f "$F/nv_rc" ]; then read -r r < "$F/nv_rc"; echo "NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver."; exit "$r"; fi
if [ -f "$F/nv_raw" ]; then cat "$F/nv_raw"; exit 0; fi
read -r t < "$F/nv_total"; read -r f < "$F/nv_free"
echo "$t, $f"
EOF
}

stub_pgrep() { cat <<'EOF'
#!/bin/bash
F='@FAKE@'
printf '%s\n' "$*" >> "$F/pgrep_args"
if [ -f "$F/pgrep_busy" ]; then echo "4242 python3 -u scripts/mpm3d_compaction.py --other-run"; exit 0; fi
if [ -f "$F/stub.pid" ]; then
  read -r p < "$F/stub.pid"; st=""; { read -r st < "/proc/$p/stat"; } 2>/dev/null
  if [ -n "$st" ]; then rest=${st##*) }; set -- $rest
    if [ "$1" != Z ]; then echo "$p bash python -u scripts/mpm3d_compaction.py"; echo "fake pgrep: a live arm was running at a pre-check" >> "$F/ERRORS"; exit 0; fi
  fi
fi
exit 1
EOF
}

stub_git() { cat <<'EOF'
#!/bin/bash
F='@FAKE@'
printf '%s\n' "$*" >> "$F/git_args"
if [ "$#" -eq 4 ] && [ "$1" = -C ] && [ "$3" = rev-parse ] && [ "$4" = HEAD ]; then
  if [ -f "$F/git_real" ]; then exec '@GIT@' "$@"; fi
  cat "$F/git_head"; exit 0
fi
echo "fake git: unexpected args: $*" >> "$F/ERRORS"; exit 99
EOF
}

inst() { "stub_$1" | sed -e "s|@FAKE@|$F|g" -e "s|@RS@|$RS|g" -e "s|@RD@|$RD|g" -e "s|@PY3@|$PY3|g" -e "s|@GIT@|$REALGIT|g" > "$2"; chmod +x "$2"; }

# ---------------------------------------------------------------- environment per scenario
mk_env() {
  CUR=$1
  S=$WORK/$1; H=$S/home; F=$S/fake; B=$S/bin; OUTD=$H/fam_s127; BL=$OUTD/batch_s127.log
  rm -rf "$S"
  mkdir -p "$H/fam-wt/scripts" "$H/fam-wt/docs/data/case15_corner_20261001" "$H/fam-mpm310/bin" \
           "$F/pymods/numpy" "$F/pymods/scipy" "$F/pymods/taichi" "$B" "$S/cwd"
  cp "$SEALED_SRC" "$H/fam-wt/scripts/mpm3d_compaction.py"
  cp "$ASSETS/case15_am_scaffold.csv" "$ASSETS/case15_se_scaffold.csv" "$H/fam-wt/docs/data/case15_corner_20261001/"
  cp "$ASSETS/real14_am_scaffold.csv" "$ASSETS/real14_se_scaffold.csv" "$H/fam-wt/docs/data/"
  echo 7f44d6534 > "$H/fam-wt/SEAL_COMMIT"
  echo "$SEAL_FULL" > "$F/git_head"
  echo "$START" > "$F/clock"
  echo 49140 > "$F/nv_total"; echo 48539 > "$F/nv_free"
  echo '__version__ = "1.26.4"' > "$F/pymods/numpy/__init__.py"
  echo '__version__ = "1.11.4"' > "$F/pymods/scipy/__init__.py"
  printf 'print("[Taichi] version 1.7.3, llvm 15.0.4, commit 5ec301be, linux, python 3.10.12")\n__version__ = (1, 7, 3)\n' > "$F/pymods/taichi/__init__.py"
  inst python "$H/fam-mpm310/bin/python"
  inst sleep "$B/sleep"; inst date "$B/date"; inst nvidia "$B/nvidia-smi"; inst pgrep "$B/pgrep"; inst git "$B/git"
  : > "$S/precreated"
}

exp_argv() { "$PY3" -I "$HERE/expected_argv.py" "$PREREG" "$H/fam-mpm310/bin/python" "$OUTD" "$S/exp" > "$S/exp_table.txt" || fail "expected_argv.py failed"; }

run_r() {
  local to=${1:-120}
  ( cd "$S/cwd" && exec timeout -k 5 "$to" env -i HOME="$H" PATH="$B:/usr/local/bin:/usr/bin:/bin" TZ=UTC LANG=C.UTF-8 bash "$RUNNER" ) > "$S/stdout" 2> "$S/stderr"
  RC=$?
  if [ -f "$F/stub.pid" ]; then kill -KILL "$(cat "$F/stub.pid")" 2> /dev/null; fi
  [ "$RC" -ne 124 ] && [ "$RC" -ne 137 ] || fail "runner timed out (rc=$RC)"
}

leak_check() {
  local f lf line tok
  for tok in LEAKCANARY 29.4917 'thickness=' 'porosity=' 'wallP=' 'FINAL ' 'σzz' 'servo_status' 'saved metrics' '[platen]' '3D MPM' 'converged:' 'Traceback (most' 'ILLEGAL_ADDRESS' 'out of memory'; do
    for f in "$S/stdout" "$S/stderr" "$BL"; do
      [ -f "$f" ] && grep -qF -- "$tok" "$f" && { echo "    leak token '$tok' in ${f##*/}"; return 1; }
    done
  done
  for lf in "$OUTD"/fam_s127_*.log "$OUTD"/fam_s127_*.json; do
    [ -f "$lf" ] || continue
    while IFS= read -r line; do
      [ -n "${line//[[:space:]{\}]/}" ] || continue
      for f in "$S/stdout" "$S/stderr" "$BL"; do
        [ -f "$f" ] && grep -qF -- "$line" "$f" && { echo "    arm line leaked into ${f##*/}: ${line:0:50}"; return 1; }
      done
    done < "$lf"
  done
  return 0
}
stdout_in_batch() { local l; [ -f "$BL" ] || return 1; while IFS= read -r l; do [ -z "$l" ] && continue; grep -qxF -- "$l" "$BL" || return 1; done < "$S/stdout"; }
no_new_outputs() { local a x; for a in "${ARMS4[@]}"; do for x in log json; do [ -e "$OUTD/fam_s127_$a.$x" ] && ! grep -qxF "fam_s127_$a.$x" "$S/precreated" && return 1; done; done; return 0; }
corner_outputs_absent() { local a x; for a in corner_fb corner_fa corner_f0; do for x in log json; do [ -e "$OUTD/fam_s127_$a.$x" ] && ! grep -qxF "fam_s127_$a.$x" "$S/precreated" && return 1; done; done; return 0; }
calls_are() { cmp -s "$F/calls" <(printf '%s\n' "$@"); }

common_checks() {
  chk "no value / log line leaks (stdout · stderr · batch log)" leak_check
  chk "stubs reported no protocol error" test ! -s "$F/ERRORS"
  chk "nvidia-smi called only with the registered query" all_lines_eq "$F/nv_args" "$NV_ARGS"
  chk "pgrep called only as: pgrep $PG_ARGS" all_lines_eq "$F/pgrep_args" "$PG_ARGS"
  chk "git called only as: git -C WT rev-parse HEAD" all_lines_eq "$F/git_args" "-C $H/fam-wt rev-parse HEAD"
  chk "batch log exists and every stdout line is also in it" stdout_in_batch
}

# ================================================================ scenarios
sc_static() {
  CUR=static
  chk "bash -n runner" bash -n "$RUNNER"
  chk "bash -n harness" bash -n "$HERE/test_run_s127.sh"
  chk "runner has set -u" grep -qE '^set -u' "$RUNNER"
  chk "usage: tmux launch line in first 15 lines" bash -c "head -n 15 '$RUNNER' | grep -qF \"tmux new -d -s fam127 'bash ~/run_s127.sh'\""
  chk "usage: STOP line in first 15 lines" bash -c "head -n 15 '$RUNNER' | grep -qF 'touch ~/fam_s127/STOP'"
  chk "deadline epoch literal 1795230000 (= 2026-11-21T03:00:00Z)" grep -qE '(^|[^0-9])1795230000([^0-9]|$)' "$RUNNER"
}

sc_happy() {
  mk_env happy; exp_argv; run_r
  chk "exit 0" test "$RC" -eq 0
  chk "calls: version check, then confirm → corner b → a → 0" calls_are version "arm confirm_fb" "arm corner_fb" "arm corner_fa" "arm corner_f0"
  local a
  for a in "${ARMS4[@]}"; do
    chk "argv $a == registration text (+ 12-7-2 on corners)" cmp -s "$F/argv_$a" "$S/exp/$a.argv"
    chk "cwd $a == WT" test "$(cat "$F/cwd_$a" 2> /dev/null)" = "$(cd "$H/fam-wt" && pwd -P)"
  done
  chk "start line exactly once" cnt_eq "$S/stdout" '^§12-7 시작 ' 1
  chk "start line = clock at launch (KST)" grep -qxF "§12-7 시작 2026-11-05 00:00:00 KST" "$S/stdout"
  chk "start line in batch log" grep -qxF "§12-7 시작 2026-11-05 00:00:00 KST" "$BL"
  chk "order: VERSIONS < start line < RUN confirm_fb" order_ok "$BL" '^VERSIONS ' '^§12-7 시작 ' '^RUN confirm_fb '
  chk "END confirm_fb" grep -qxF "END confirm_fb rc=0 2026-11-05 00:00:00 KST → 2026-11-05 00:01:00 KST (60 s) frame_lines=6 json=yes (57 fields) status=converged" "$S/stdout"
  chk "END corner_fb" grep -qxF "END corner_fb rc=0 2026-11-05 00:01:10 KST → 2026-11-05 00:02:10 KST (60 s) frame_lines=6 json=yes (57 fields) status=converged" "$S/stdout"
  chk "END corner_fa" grep -qxF "END corner_fa rc=0 2026-11-05 00:02:20 KST → 2026-11-05 00:03:20 KST (60 s) frame_lines=6 json=yes (57 fields) status=converged" "$S/stdout"
  chk "END corner_f0 json=yes (57 fields)" grep -qxF "END corner_f0 rc=0 2026-11-05 00:03:30 KST → 2026-11-05 00:04:30 KST (60 s) frame_lines=6 json=yes (57 fields) status=no_converged_marker" "$S/stdout"
  chk "CONFIRM_GATE_PASS" grep -qxF CONFIRM_GATE_PASS "$S/stdout"
  chk "order: END confirm < GATE_PASS < RUN corner_fb" order_ok "$S/stdout" '^END confirm_fb ' '^CONFIRM_GATE_PASS$' '^RUN corner_fb '
  chk "batch end line" grep -q '^§12-7 끝 ' "$S/stdout"
  nchk "no REFUSED/SKIP/STOPPED/GATE_FAIL/KILL/HB/ETA" grep -qE '^(REFUSED|SKIP|STOPPED|CONFIRM_GATE_FAIL|KILL|HB|ETA) ' "$S/stdout"
  chk "VERSIONS recorded in batch log" grep -qE '^VERSIONS python=[0-9.]+ numpy=1\.26\.4 scipy=1\.11\.4 taichi=\(1, 7, 3\)$' "$BL"
  chk "version check = \$PY -c \"import sys,numpy,scipy,taichi; print(...)\"" grep -q '^import sys,numpy,scipy,taichi; print(' "$F/version_code"
  chk "runner md5 recorded in batch log" grep -qF "runner_md5=$(md5sum < "$RUNNER" | cut -c1-32)" "$BL"
  chk "PRE line with GPU total/free for each arm" cnt_eq "$S/stdout" '^PRE (confirm_fb|corner_fb|corner_fa|corner_f0) ok .*total=49140 free=48539' 4
  chk "ARGV line per arm, no trailing space" cnt_eq "$S/stdout" '^ARGV (confirm_fb|corner_fb|corner_fa|corner_f0) .*[^ ]$' 4
  for a in "${ARMS4[@]}"; do chk "outputs exist: $a .log/.json" test -f "$OUTD/fam_s127_$a.log" -a -s "$OUTD/fam_s127_$a.json"; done
  common_checks
}

hdr() { # name token pycalls(none|version) mutation [args]
  local name=$1 tok=$2 pyc=$3; shift 3
  mk_env "hdr_$name"; "$@"; run_r
  chk "exit 2 (REFUSED)" test "$RC" -eq 2
  chk "REFUSED $tok" grep -qE "^REFUSED ${tok}([^A-Za-z_]|\$)" "$S/stdout"
  chk "REFUSED in batch log" grep -qE "^REFUSED ${tok}([^A-Za-z_]|\$)" "$BL"
  nchk "no start line" grep -q '^§12-7 시작' "$S/stdout"
  if [ "$pyc" = none ]; then chk "python never called" test ! -e "$F/calls"
  else chk "python called only for the version check" calls_are version; fi
  chk "no arm output written" no_new_outputs
  common_checks
}
m_noop() { :; }
m_seal_wrong() { echo 7f44d6535 > "$H/fam-wt/SEAL_COMMIT"; }
m_seal_missing() { rm -f "$H/fam-wt/SEAL_COMMIT"; }
m_seal_crlf() { printf '7f44d6534\r\n' > "$H/fam-wt/SEAL_COMMIT"; }
m_head() { echo 0123456789012345678901234567890123456789 > "$F/git_head"; }
m_head_short() { echo 7f44d6534 > "$F/git_head"; }
m_md5() { printf '\n' >> "$H/fam-wt/scripts/mpm3d_compaction.py"; }
m_code_missing() { rm -f "$H/fam-wt/scripts/mpm3d_compaction.py"; }
m_sha() { printf 'x' >> "$H/fam-wt/$1"; }
m_csv_missing() { rm -f "$H/fam-wt/$1"; }
m_py_missing() { rm -f "$H/fam-mpm310/bin/python"; }
m_py_noexec() { chmod -x "$H/fam-mpm310/bin/python"; }
m_py_import() { : > "$F/py_c_fail"; }
m_nv_fail() { echo 9 > "$F/nv_rc"; }
m_nv_total() { echo 24576 > "$F/nv_total"; }
m_nv_garbage() { printf '[N/A], [N/A]\n' > "$F/nv_raw"; }
m_nv_two() { printf '49140, 48539\n49140, 48539\n' > "$F/nv_raw"; }
m_pgrep() { : > "$F/pgrep_busy"; }
m_out() { mkdir -p "$OUTD"; echo PREEXIST > "$OUTD/$1"; echo "$1" >> "$S/precreated"; }
m_deadline_eq() { echo "$DEADLINE" > "$F/clock"; }
m_deadline_after() { echo $((DEADLINE + 3600)) > "$F/clock"; }
m_stop() { mkdir -p "$OUTD"; : > "$OUTD/STOP"; }

sc_headers() {
  hdr seal_wrong SEAL_COMMIT none m_seal_wrong
  hdr seal_missing SEAL_COMMIT none m_seal_missing
  hdr seal_crlf SEAL_COMMIT none m_seal_crlf
  hdr head HEAD none m_head
  hdr head_short HEAD none m_head_short
  hdr md5 md5 none m_md5
  hdr code_missing md5 none m_code_missing
  hdr sha_c15am sha256 none m_sha "$C15AM"; chk "names the file" grep -qF "$C15AM" "$S/stdout"
  hdr sha_c15se sha256 none m_sha "$C15SE"; chk "names the file" grep -qF "$C15SE" "$S/stdout"
  hdr sha_r14am sha256 none m_sha "$R14AM"; chk "names the file" grep -qF "$R14AM" "$S/stdout"
  hdr sha_r14se sha256 none m_sha "$R14SE"; chk "names the file" grep -qF "$R14SE" "$S/stdout"
  hdr csv_missing sha256 none m_csv_missing "$C15SE"
  hdr py_missing PY none m_py_missing
  hdr py_noexec PY none m_py_noexec
  hdr nv_fail nvidia-smi none m_nv_fail
  hdr nv_total gpu_total none m_nv_total
  hdr nv_garbage nvidia-smi none m_nv_garbage
  hdr nv_two_gpus nvidia-smi none m_nv_two
  hdr pgrep_busy pgrep_busy none m_pgrep
  local a x
  for a in "${ARMS4[@]}"; do for x in log json; do
    hdr "out_${a}_$x" output_exists none m_out "fam_s127_$a.$x"
    chk "pre-existing fam_s127_$a.$x untouched" grep -qx PREEXIST "$OUTD/fam_s127_$a.$x"
  done; done
  hdr deadline_eq deadline none m_deadline_eq
  hdr deadline_after deadline none m_deadline_after
  hdr stop_present STOP none m_stop
  hdr py_import PY_import version m_py_import
}

gate() { # name mode reasons status [time]
  mk_env "gate_$1"; echo "$2" > "$F/mode_confirm_fb"; [ -n "${5:-}" ] && echo "$5" > "$F/time_confirm_fb"
  run_r
  chk "exit 5" test "$RC" -eq 5
  chk "CONFIRM_GATE_FAIL $3" grep -qxF "CONFIRM_GATE_FAIL $3 — corner 를 띄우지 않는다 · 1저자에게" "$S/stdout"
  chk "only the confirm arm ran" calls_are version "arm confirm_fb"
  chk "END confirm_fb status=$4" grep -qE "^END confirm_fb rc=[0-9]+ .* status=$4\$" "$S/stdout"
  nchk "no CONFIRM_GATE_PASS" grep -q '^CONFIRM_GATE_PASS' "$S/stdout"
  chk "no corner output files" corner_outputs_absent
  common_checks
}
sc_gates() {
  gate budget budget "rc=1,json_missing,no_converged_marker" not_converged_frame_budget "0 10 80 60"
  chk "END shows frame_lines=80 json=no" grep -qE '^END confirm_fb rc=1 .* frame_lines=80 json=no status=' "$S/stdout"
  gate probe probe_not_at_rest "rc=1,json_missing,no_converged_marker" not_converged_probe_not_at_rest
  gate nomarker nomarker "no_converged_marker" no_converged_marker
  gate traceback traceback "traceback" traceback
  gate cuda cuda "cuda_error" cuda_error
  gate cuda_oom cuda_oom "rc=1,json_missing,traceback,cuda_error,no_converged_marker" cuda_oom
  gate rc1 rc1 "rc=1" converged
  gate nojson nojson "json_missing" converged
}

sc_gpu_free() {
  mk_env free_31857; echo 31857 > "$F/nv_free"; run_r
  chk "exit 3 (SKIP)" test "$RC" -eq 3
  chk "SKIP corner_fb gpu_free=31857" grep -qE '^SKIP corner_fb gpu_free=31857([^0-9]|$)' "$S/stdout"
  chk "confirm ran, no corner arm" calls_are version "arm confirm_fb"
  chk "END confirm_fb present" grep -q '^END confirm_fb rc=0 ' "$S/stdout"
  chk "no corner output files" corner_outputs_absent
  common_checks

  mk_env free_31858; echo 31858 > "$F/nv_free"; run_r
  chk "free = 31858 (boundary) → all four arms, exit 0" test "$RC" -eq 0
  chk "calls: all four arms" calls_are version "arm confirm_fb" "arm corner_fb" "arm corner_fa" "arm corner_f0"
  common_checks

  mk_env free_drop_before_fa; echo "$((START + 100)) put $F/nv_free 31857" > "$F/events"; run_r
  chk "exit 3" test "$RC" -eq 3
  chk "SKIP corner_fa gpu_free" grep -qE '^SKIP corner_fa gpu_free=31857' "$S/stdout"
  chk "confirm + corner_fb ran, fa/f0 not" calls_are version "arm confirm_fb" "arm corner_fb"
  common_checks
}

sc_between_arms() {
  mk_env stop_between; echo "$((START + 65)) touch $OUTD/STOP" > "$F/events"; run_r
  chk "exit 3" test "$RC" -eq 3
  chk "SKIP corner_fb STOP" grep -qE '^SKIP corner_fb STOP' "$S/stdout"
  chk "only confirm ran" calls_are version "arm confirm_fb"
  common_checks

  mk_env deadline_between; echo $((DEADLINE - 100)) > "$F/clock"; echo "0 10 6 120" > "$F/time_confirm_fb"; run_r
  chk "exit 3" test "$RC" -eq 3
  chk "END confirm_fb normal (finished before the poll that saw the deadline)" grep -qE '^END confirm_fb rc=0 .* status=converged$' "$S/stdout"
  chk "SKIP corner_fb deadline" grep -qE '^SKIP corner_fb deadline' "$S/stdout"
  chk "only confirm ran" calls_are version "arm confirm_fb"
  common_checks

  mk_env pgrep_between; echo "$((START + 65)) touch $F/pgrep_busy" > "$F/events"; run_r
  chk "exit 3" test "$RC" -eq 3
  chk "SKIP corner_fb pgrep_busy" grep -qE '^SKIP corner_fb pgrep_busy' "$S/stdout"
  common_checks

  mk_env total_between; echo "$((START + 65)) put $F/nv_total 24576" > "$F/events"; run_r
  chk "exit 3" test "$RC" -eq 3
  chk "SKIP corner_fb gpu_total=24576" grep -qE '^SKIP corner_fb gpu_total=24576' "$S/stdout"
  common_checks

  mk_env nvfail_between; echo "$((START + 65)) put $F/nv_rc 9" > "$F/events"; run_r
  chk "exit 3" test "$RC" -eq 3
  chk "SKIP corner_fb nvidia-smi" grep -qE '^SKIP corner_fb nvidia-smi' "$S/stdout"
  common_checks

  mk_env output_appears; echo "$((START + 100)) touch $OUTD/fam_s127_corner_fa.json" > "$F/events"; echo fam_s127_corner_fa.json >> "$S/precreated"; run_r
  chk "exit 3" test "$RC" -eq 3
  chk "SKIP corner_fa output_exists" grep -qE '^SKIP corner_fa output_exists' "$S/stdout"
  chk "file that appeared is untouched (empty)" test -e "$OUTD/fam_s127_corner_fa.json" -a ! -s "$OUTD/fam_s127_corner_fa.json"
  common_checks
}

sc_deadline_mid() {
  mk_env deadline_mid_fb; echo $((DEADLINE - 3000)) > "$F/clock"
  echo budget > "$F/mode_corner_fb"; echo "0 50 1000 100000" > "$F/time_corner_fb"; run_r
  chk "exit 4 (STOPPED)" test "$RC" -eq 4
  chk "STOPPED corner_fb deadline" grep -qxF "STOPPED corner_fb deadline" "$S/stdout"
  chk "TERM at first poll past the deadline (12:00:10 KST)" grep -qxF "TERM corner_fb 2026-11-21 12:00:10 KST" "$S/stdout"
  chk "python received TERM (clock D+10..D+15)" bash -c "t=\$(cat '$F/got_term_corner_fb'); [ \$t -ge $((DEADLINE + 10)) ] && [ \$t -le $((DEADLINE + 15)) ]"
  nchk "no KILL needed" grep -q '^KILL ' "$S/stdout"
  chk "END corner_fb rc=143" grep -qE '^END corner_fb rc=143 ' "$S/stdout"
  chk "no further arm" calls_are version "arm confirm_fb" "arm corner_fb"
  chk "4 heartbeats with exact frame-line counts" bash -c "grep -E '^HB ' '$S/stdout' | grep -E ' corner_fb ' | sed 's/.*frame_lines=//' | tr '\n' ' ' | grep -qx '13 25 37 49 '"
  chk "HB format" grep -qxF "HB $(kst $((DEADLINE - 2930 + 600))) corner_fb frame_lines=13" "$S/stdout"
  nchk "no ETA (arm ran < 60 min)" grep -q '^ETA ' "$S/stdout"
  common_checks

  mk_env deadline_mid_fb_ignore; echo $((DEADLINE - 3000)) > "$F/clock"
  echo budget > "$F/mode_corner_fb"; echo "0 50 1000 100000" > "$F/time_corner_fb"; echo ignore > "$F/term_corner_fb"; run_r
  chk "exit 4" test "$RC" -eq 4
  chk "STOPPED corner_fb deadline" grep -qxF "STOPPED corner_fb deadline" "$S/stdout"
  chk "TERM line at 12:00:10" grep -qxF "TERM corner_fb 2026-11-21 12:00:10 KST" "$S/stdout"
  chk "KILL line 120 s after TERM (12:02:10)" grep -qE '^KILL corner_fb 2026-11-21 12:02:10 KST' "$S/stdout"
  chk "END corner_fb rc=137" grep -qE '^END corner_fb rc=137 ' "$S/stdout"
  chk "python kept running until KILL (last tick D+130)" test "$(cat "$F/last_seen_corner_fb" 2> /dev/null)" = $((DEADLINE + 130))
  chk "no further arm" calls_are version "arm confirm_fb" "arm corner_fb"
  common_checks

  mk_env deadline_mid_confirm; echo $((DEADLINE - 1)) > "$F/clock"; echo "0 10 6 120" > "$F/time_confirm_fb"; run_r
  chk "header passed at D-1 (start line)" grep -qxF "§12-7 시작 2026-11-21 11:59:59 KST" "$S/stdout"
  chk "exit 4" test "$RC" -eq 4
  chk "STOPPED confirm_fb deadline" grep -qxF "STOPPED confirm_fb deadline" "$S/stdout"
  nchk "gate not evaluated" grep -qE '^CONFIRM_GATE_(PASS|FAIL)' "$S/stdout"
  chk "no corner arm" calls_are version "arm confirm_fb"
  common_checks
}

sc_stop_mid() {
  mk_env stop_mid_fb; echo "$((START + 1000)) touch $OUTD/STOP" > "$F/events"
  echo budget > "$F/mode_corner_fb"; echo "0 50 1000 100000" > "$F/time_corner_fb"; run_r
  chk "exit 4" test "$RC" -eq 4
  chk "STOPPED corner_fb author" grep -qxF "STOPPED corner_fb author" "$S/stdout"
  chk "TERM at the first poll after STOP appeared (00:17:10)" grep -qxF "TERM corner_fb 2026-11-05 00:17:10 KST" "$S/stdout"
  chk "END corner_fb rc=143" grep -qE '^END corner_fb rc=143 ' "$S/stdout"
  chk "no further arm" calls_are version "arm confirm_fb" "arm corner_fb"
  common_checks

  mk_env stop_mid_confirm; echo "$((START + 30)) touch $OUTD/STOP" > "$F/events"; echo "0 10 6 600" > "$F/time_confirm_fb"; run_r
  chk "exit 4" test "$RC" -eq 4
  chk "STOPPED confirm_fb author" grep -qxF "STOPPED confirm_fb author" "$S/stdout"
  chk "no corner arm" calls_are version "arm confirm_fb"
  common_checks
}

sc_corner_fail() {
  mk_env corner_fb_rc1; echo budget > "$F/mode_corner_fb"; echo "0 10 600 60" > "$F/time_corner_fb"; run_r
  chk "exit 0 (batch continues past a failed corner arm)" test "$RC" -eq 0
  chk "END corner_fb rc=1 json=no status=not_converged_frame_budget" grep -qE '^END corner_fb rc=1 .* frame_lines=600 json=no status=not_converged_frame_budget$' "$S/stdout"
  chk "corner_fa and corner_f0 still ran" calls_are version "arm confirm_fb" "arm corner_fb" "arm corner_fa" "arm corner_f0"
  chk "END corner_fa rc=0" grep -qE '^END corner_fa rc=0 ' "$S/stdout"
  chk "END corner_f0 json=yes (57 fields)" grep -qE '^END corner_f0 rc=0 .* json=yes \(57 fields\) status=' "$S/stdout"
  nchk "no retry: corner_fb ran once" bash -c "[ \$(grep -c 'arm corner_fb' '$F/calls') -ne 1 ]"
  common_checks

  mk_env corner_crash_oom; echo crash > "$F/mode_corner_fb"; echo cuda_oom > "$F/mode_corner_fa"; echo converge > "$F/mode_corner_f0"; run_r
  chk "exit 0" test "$RC" -eq 0
  chk "END corner_fb status=traceback" grep -qE '^END corner_fb rc=1 .* json=no status=traceback$' "$S/stdout"
  chk "END corner_fa status=cuda_oom" grep -qE '^END corner_fa rc=1 .* json=no status=cuda_oom$' "$S/stdout"
  chk "END corner_f0 converged json=yes (57 fields)" grep -qE '^END corner_f0 rc=0 .* json=yes \(57 fields\) status=converged$' "$S/stdout"
  chk "no retry of any arm (each once)" calls_are version "arm confirm_fb" "arm corner_fb" "arm corner_fa" "arm corner_f0"
  common_checks
}

sc_heartbeat() {
  mk_env heartbeat; echo "0 40 100 1800" > "$F/time_confirm_fb"; run_r
  chk "exit 0" test "$RC" -eq 0
  chk "exactly 2 HB lines for confirm_fb" cnt_eq "$S/stdout" '^HB .* confirm_fb frame_lines=' 2
  chk "HB at +10 min with frame_lines=16" grep -qxF "HB 2026-11-05 00:10:00 KST confirm_fb frame_lines=16" "$S/stdout"
  chk "HB at +20 min with frame_lines=31" grep -qxF "HB 2026-11-05 00:20:00 KST confirm_fb frame_lines=31" "$S/stdout"
  chk "HB in batch log" grep -qxF "HB 2026-11-05 00:10:00 KST confirm_fb frame_lines=16" "$BL"
  chk "END confirm_fb (1800 s) frame_lines=100" grep -qE '^END confirm_fb rc=0 .* \(1800 s\) frame_lines=100 json=yes \(57 fields\) status=converged$' "$S/stdout"
  common_checks
}

sc_eta() {
  # corner_fb: first frame line at +300 s, then one line per 50 s (= 10 s/frame with 5 frames/line)
  mk_env eta_ok; echo "300 50 139 7200" > "$F/time_corner_fb"; run_r
  local p; p=$(kst $((START + 90360)))
  chk "exit 0" test "$RC" -eq 0
  chk "exactly one ETA line" cnt_eq "$S/stdout" '^ETA ' 1
  chk "ETA s_per_frame=10.000 projected=$p OK" grep -qE "^ETA corner_fb .* s_per_frame=10\.000 projected_end_if_all_use_3000=$p deadline=2026-11-21 12:00 KST OK\$" "$S/stdout"
  chk "ETA at the 60-min heartbeat (after HB +60 min of corner_fb)" order_ok "$S/stdout" "^HB $(kst $((START + 70 + 3600))) corner_fb frame_lines=67\$" '^ETA corner_fb '
  chk "11 corner_fb heartbeats" cnt_eq "$S/stdout" '^HB .* corner_fb ' 11
  common_checks

  mk_env eta_over; echo $((DEADLINE - 40000)) > "$F/clock"; echo "300 50 139 7200" > "$F/time_corner_fb"; run_r
  p=$(kst $((DEADLINE - 40000 + 90360)))
  chk "exit 0 (ETA is report-only)" test "$RC" -eq 0
  chk "ETA OVER with projected=$p" grep -qE "^ETA corner_fb .* s_per_frame=10\.000 projected_end_if_all_use_3000=$p deadline=2026-11-21 12:00 KST OVER\$" "$S/stdout"
  chk "all four arms still ran (no automatic change)" calls_are version "arm confirm_fb" "arm corner_fb" "arm corner_fa" "arm corner_f0"
  common_checks

  mk_env eta_na; echo "4000 50 5 4200" > "$F/time_corner_fb"; run_r
  chk "exit 0" test "$RC" -eq 0
  chk "ETA n/a when no frame-line interval in the first hour" grep -qE '^ETA corner_fb .* s_per_frame=n/a projected_end_if_all_use_3000=n/a deadline=2026-11-21 12:00 KST UNKNOWN' "$S/stdout"
  common_checks
}

sc_realgit() {
  local RG=$CACHE/realgit
  if [ ! -d "$RG/.git" ]; then
    git init -q "$RG" && ( cd "$RG" && "$REALGIT" -c protocol.file.allow=always -c uploadpack.allowAnySHA1InWant=true \
      fetch -q --depth=1 "file://$REPO" "$SEAL_FULL" 2> /dev/null && "$REALGIT" sparse-checkout set --no-cone \
      /scripts/mpm3d_compaction.py "/$R14AM" "/$R14SE" && "$REALGIT" checkout -q --detach FETCH_HEAD ) || { CUR=realgit; fail "could not build real-git cache"; return; }
  fi
  "$REALGIT" -C "$RG" checkout -q --detach "$SEAL_FULL"
  mkdir -p "$RG/docs/data/case15_corner_20261001"
  cp "$ASSETS/case15_am_scaffold.csv" "$ASSETS/case15_se_scaffold.csv" "$RG/docs/data/case15_corner_20261001/"
  echo 7f44d6534 > "$RG/SEAL_COMMIT"
  mk_env realgit_ok; rm -rf "$H/fam-wt"; ln -s "$RG" "$H/fam-wt"; : > "$F/git_real"; echo "$DEADLINE" > "$F/clock"; run_r
  chk "real git at sealed commit: passes HEAD check, refused later at deadline" grep -qE '^REFUSED deadline' "$S/stdout"
  chk "real git rev-parse was used" grep -qxF -- "-C $H/fam-wt rev-parse HEAD" "$F/git_args"
  chk "python never called" test ! -e "$F/calls"
  common_checks
  mk_env realgit_moved; rm -rf "$H/fam-wt"; ln -s "$RG" "$H/fam-wt"; : > "$F/git_real"
  "$REALGIT" -C "$RG" -c user.name=t -c user.email=t@t commit -q --allow-empty -m probe
  run_r
  chk "real git one commit past seal → REFUSED HEAD" grep -qE '^REFUSED HEAD' "$S/stdout"
  chk "python never called" test ! -e "$F/calls"
  common_checks
  "$REALGIT" -C "$RG" checkout -q --detach "$SEAL_FULL"
}

sc_realtools() {  # semantics the runner relies on, with the REAL tools (no fakes)
  CUR=realtools
  local out rc dpid
  out=$(pgrep -af '[m]pm3d_compaction.py' 2>&1); rc=$?
  chk "real pgrep, nothing running: rc=1 and empty output" test "$rc" -eq 1 -a -z "$out"
  ( exec -a "python3 -u scripts/mpm3d_compaction.py --dummy" "$RS" 30 ) &
  dpid=$!; "$RS" 0.3
  out=$(pgrep -af '[m]pm3d_compaction.py' 2>&1); rc=$?
  chk "real pgrep, one dummy running: rc=0 and one line" test "$rc" -eq 0 -a "$(printf '%s\n' "$out" | grep -c .)" -eq 1
  kill "$dpid" 2> /dev/null; wait "$dpid" 2> /dev/null
  chk "real date: TZ=KST-9 epoch 1795230000 → 2026-11-21 12:00:00 KST" test "$(TZ=KST-9 "$RD" -d @1795230000 '+%F %T %Z')" = "2026-11-21 12:00:00 KST"
}

# ================================================================ main
cleanup() { pkill -KILL -f "$WORK/" 2> /dev/null; }
trap cleanup EXIT
rm -rf "$WORK"; mkdir -p "$WORK"
prep_assets
echo "runner = ${RUNNER#"$HERE"/}"
echo "runner md5 = $(md5sum < "$RUNNER" | cut -c1-32)"
sc_static
sc_realtools
sc_happy
sc_headers
sc_gates
sc_gpu_free
sc_between_arms
sc_deadline_mid
sc_stop_mid
sc_corner_fail
sc_heartbeat
sc_eta
sc_realgit
echo
echo "== SUMMARY: pass $T_PASS · fail $T_FAIL =="
if [ "$T_FAIL" -gt 0 ]; then printf '  %s\n' "${FAILS[@]}"; exit 1; fi
exit 0
