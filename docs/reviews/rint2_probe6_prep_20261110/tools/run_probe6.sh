#!/usr/bin/env bash
# run_probe6.sh - watcher for the Rint 2 development probe 6 (SBE numeric probe, sigma sealed).  ASCII only.
#
# usage: bash run_probe6.sh <W> <O> <L> <PIN> <MAXITER> [ROOT]
#   W        pinned worktree (git HEAD must equal PIN; tree clean, untracked files included)
#   O        runner output folder: must not exist or be empty; name ca1_probe6_a<N>_<...>_arm1
#   L        log folder: must exist and hold nothing but nohup.out; directly in $HOME; name p6log_a<N>_<...> (N = attempt,
#            1 to 4, same as O)
#   PIN      expected commit (40 hex)
#   MAXITER  CG iteration limit (digits) -> P2_EXTRA="--step3-maxiter MAXITER"; the registered pair: attempt 1 -> 30000,
#            attempt 2 -> 1500000, attempts 3 and 4 -> 1500000 (any other pair is a STOP)
#   ROOT     kit root (default $HOME/sdcp) - the runner is started there
#
# Rules: docs/reviews/rint2_dev_probe_ledger_20261026.md section 2 (seven boxes) and section 3 (attempt lines); command =
#   registration R docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md section 10-1 (2).
# What it does:
#   umask 022, job control off -> checks (nothing is written outside L and the lock, and the runner is not started, unless
#   all pass): arguments, folders, attempt number and its limit, one-watcher lock ($HOME/.probe6.lock), earlier attempts
#   in $HOME/p6log_* (every one has an end marker; this attempt number has not run to the end yet; an attempt does not
#   run after a higher-numbered attempt that ran to the end; attempt N >= 2 needs exactly one attempt-(N-1) folder with
#   DONE and solve_started=1, whose pin is this pin or an earlier commit of it (history not grafted, not shallow);
#   attempts 2 and 4 also need the same solve code CODE_PATHS as attempt 1 and 3; "ran to the end" = DONE with
#   solve_started=1, or WATCHER_FAILED after the runner-start line), the store folder (attempts 3 and 4, below), no runner
#   or payload of this account already running, pin, clean tree, venv, kit, S0 plan, kit payload line, GPU, cupy, the
#   runner's own pre-run gates
#   -> environment fingerprint (versions only, no host name)
#   -> removes PYTHONPATH and every runner-axis variable from the environment and sets exactly the registered ones
#      (+ PYTHONUNBUFFERED=1); the runner gets no BASH_ENV and no SHELLOPTS (env -u)
#   -> starts the runner in its own session / process group with ALL of its output going to L/runner.log and checks that
#      the runner leads that session (WATCHER_FAILED when it does not)
#   -> samples host RSS, GPU memory and the log line count while it runs
#   -> after the runner ends: stops whatever is left in its process group, records, probe6_read.py (closed allowlist),
#      bundle of the allowlisted report, fingerprint and numeric diagnostics.
# End markers in L: DONE = the runner ran and the record is complete (also when the runner failed or hit the
#   iteration limit - that is a normal end); STOPPED = stopped before the runner started (nothing was solved);
#   WATCHER_FAILED = the watcher itself failed after the runner started (runner group stopped, lock kept, record
#   incomplete).  No marker = still running, or the watcher was killed (look at status.log first).
# It never prints runner output, never deletes or overwrites a result, and never copies the arm JSON, the run
# receipt or the raw runner log into the bundle (they stay where they are; the report carries their sha256).
# The runner itself writes into the kit run folder (generated arm script, time -v record, and on failure the
# rejected arm JSON) and would overwrite same-named files of an earlier attempt, so the watcher copies such files
# into the log folder: kit_run_before/ (present before the start) and kit_run_new/ (written by this attempt).
# Attempts 3 and 4 (ledger section 3, 2026-11-13 - carbon-junction registry store of the Rint 2 code package): the same probe
#   with the store on, CJUNC_STORE = the fixed folder ~/p6_cjstore.  Attempt 3: the store folder is absent or empty
#   (the watcher makes it, umask 022, after every check) -> the payload builds the registry and writes it (arm audit status
#   built_written).  Attempt 4: the store folder holds exactly what attempt 3 left (names and sha256 from attempt 3's meta)
#   -> the payload reads it (status hit).  The arm audit side file cjstore_audit_<arm>.json (next to the arm in O, the runner
#   moves it) carries the status; the reader checks it.  meta: store, store_listing_before, store_listing_after.
# git reads of this watcher (pin, clean tree, ancestry, solve-code diff) are sealing reads (Codex rebuttal 1/2 section 3): the
#   repository-selecting GIT_* names are unset (same text as run_contract.GIT_DROP_SH) and replacement objects are off
#   (GIT_NO_REPLACE_OBJECTS=1, exported - the runner inherits it).
# Knobs for testing (both recorded in meta.txt): PROBE6_SAMPLE_S = sampling interval in s (default 10),
#   PROBE6_CAP_GB = host RSS cap in GB (default min(46, MemAvailable - 6)).
set -u
umask 022
set +m   # job control off (SHELLOPTS / BASH_ENV may turn it on): with it on, setsid forks and the runner leaves the watched group
for _gv in $(compgen -e); do case "$_gv" in (GIT_DIR|GIT_WORK_TREE|GIT_INDEX_FILE|GIT_OBJECT_DIRECTORY|GIT_ALTERNATE_OBJECT_DIRECTORIES|GIT_COMMON_DIR|GIT_NAMESPACE|GIT_PREFIX|GIT_CONFIG_PARAMETERS|GIT_CONFIG_COUNT|GIT_CONFIG_KEY_*|GIT_CONFIG_VALUE_*) unset "$_gv";; esac; done
export GIT_NO_REPLACE_OBJECTS=1

KIT=kit_SBE_vgcf100
TOL_FF=0.07381254285530132
RUNNER_REL=scripts/sdcp_gain_vox015_8arm.sh
TOOLS_REL=docs/reviews/rint2_probe6_prep_20261110/tools
S0PLAN_REL=docs/data/rint2_s0_sbe_20261108/files/sdcp/ca1_s0_sbe_20261106_memfix/cjunc_plan.json
LOCK="$HOME/.probe6.lock"
# solve code: the repository paths the runner and the payload read or import (traced with strace on the real runner and
# payload, 2026-11-10; outside scripts/ = the prereg file the runner checks and the EIS anchor table the payload reads),
# this tool folder and the S0 stage-1 data.  Attempt 2 runs only when these are the same at attempt 1's pin and this pin.
CODE_PATHS=(scripts/ docs/reviews/rint2_probe6_prep_20261110/tools/ docs/data/rint2_s0_sbe_20261108/ docs/data/rint_eis_anchors.csv docs/reviews/sdcp_gain_prereg_v2_20260816.md)
# the runner and the pre-run gates run without BASH_ENV (a startup file of every non-interactive bash) and SHELLOPTS
RENV=(env -u BASH_ENV -u SHELLOPTS)
# Registered axes (registration R section 10-1 (2)).  Values that the registration writes as <plan ...>:
#   CJUNC_LEN_LAW = scripts/carbon_junction.py CJUNC_LEN_LAW, CJUNC_S_MIN_UM = 0 (author 2026-11-09, section 2-1b),
#   CJUNC_TOL_FF_UM = S0 stage-1 plan values_um.tol_ff, STEP3_RTOL = scripts/step3_conv_cert.py CERT_RTOL_MAX.
AXES=(
  VOX=0.15 SDCP_SPHERE_D=0.30 PTFE_STAMP=face_alpha BRIDGE_UM=0.48
  SIGMA_AM_S_OVERRIDE=0.0041 SIGMA_SDCP_OVERRIDE=256.6 SIGMA_FIBRE_BULK=1e4
  CJUNC=1 CJUNC_RJ=1e6 CJUNC_LEN_LAW=len_scaled_v0 CJUNC_UNREG_LAW=cut CJUNC_S_MIN_UM=0.0
  "CJUNC_TOL_FF_UM=$TOL_FF" CJUNC_PTFE_JLAW=P0 SDCP_MOD_C=0 STEP3_RTOL=1e-12
  EXPECT_BACKEND=gpu "KITS=$KIT" ARMS=1 LEAN=2
)
EXP_RTOL=""; EXP_BACKEND=""; EXP_RJ=""
for a in "${AXES[@]}"; do
  case "$a" in STEP3_RTOL=*) EXP_RTOL="${a#*=}";; EXPECT_BACKEND=*) EXP_BACKEND="${a#*=}";; CJUNC_RJ=*) EXP_RJ="${a#*=}";; esac
done
# names of the environment that change how the runner and payload run (recorded as unset / empty / set / short value)
ENV_NAMES="CUDA_VISIBLE_DEVICES OMP_NUM_THREADS OPENBLAS_NUM_THREADS OPENBLAS_CORETYPE PYTHONUNBUFFERED BASH_ENV"

LOGF=""; L=""; LOCKED=0; FINISHED=0; RUNNER_STARTED=0; RPID=""; ABORTED=0; CAPTERM=0; LATE_SIG=0; WF_REASON=""; P1=""; PPR=0
say() {
  local m
  m="[probe6] $(date -u +%Y-%m-%dT%H:%M:%SZ) $*"
  echo "$m"
  if [ -n "$LOGF" ]; then echo "$m" >> "$LOGF"; fi
  return 0
}
homerel() {
  case "$1" in
    "$HOME"/*) printf '~%s' "${1#"$HOME"}";;
    *) printf '%s' "$1";;
  esac
}
release_lock() {
  if [ "$LOCKED" = 1 ]; then
    rm -f "$LOCK/owner" 2>/dev/null
    rmdir "$LOCK" 2>/dev/null
    LOCKED=0
  fi
  return 0
}
stop() {   # stop before the runner starts: STOPPED marker (written before the STOP line), lock released, rc 2
  FINISHED=1
  release_lock
  if [ -n "$LOGF" ]; then
    printf 'reason=%s\nrunner_started=0\n' "$*" > "$L/STOPPED"
    rm -f "$L/watcher.pid"
  fi
  say "STOP: $* (runner not started)"
  exit 2
}
okpath() {
  local LC_ALL=C
  case "$1" in /*) ;; *) return 1;; esac
  case "$1" in *[!A-Za-z0-9._/+-]*) return 1;; esac
  return 0
}
digits() {   # digits only, no leading zero unless the value is 0, at most $2 characters
  local LC_ALL=C
  case "$1" in ""|*[!0-9]*) return 1;; esac
  [ "${#1}" -le "$2" ] || return 1
  case "$1" in 0?*) return 1;; esac
  return 0
}
envrec() {   # unset | empty | set | value:<v> (the value itself only when short: letters, digits . , _ -)
  local LC_ALL=C v
  if [ -z "${!1+x}" ]; then echo unset; return 0; fi
  v="${!1}"
  if [ -z "$v" ]; then echo empty; return 0; fi
  case "$v" in
    *[!A-Za-z0-9,._-]*) echo set;;
    [!A-Za-z0-9]*) echo set;;
    *) if [ "${#v}" -le 32 ]; then echo "value:$v"; else echo set; fi;;
  esac
  return 0
}
group_pids() {   # live processes whose process group is RPID (read from /proc - works without ps)
  local d s rest
  [ -n "$RPID" ] || return 0
  for d in /proc/[0-9]*; do
    s=""
    read -r s < "$d/stat" 2>/dev/null || continue
    rest="${s##*) }"
    set -- $rest
    [ "${1:-}" = Z ] && continue
    [ "${3:-}" = "$RPID" ] && printf '%s ' "${d#/proc/}"
  done
  return 0
}
group_count() { local p; p="$(group_pids)"; set -- $p; echo "$#"; }
runner_leads_session() {   # 0 = the runner (RPID) leads its own session (setsid did not fork), 1 = it does not or it is gone
  local i=0 s rest
  while [ "$i" -lt 300 ]; do
    s=""
    read -r s < "/proc/$RPID/stat" 2>/dev/null || return 1
    rest="${s##*) }"
    set -- $rest
    [ "${4:-}" = "$RPID" ] && return 0
    [ "${1:-}" = Z ] && return 1
    if [ "$i" -ge 50 ]; then sleep 0.01; fi
    i=$((i + 1))
  done
  return 1
}
history_problem() {   # prints a reason when the pinned worktree's history is grafted or shallow (ancestry / diff untrustworthy)
  local s gp
  if [ -n "${GIT_GRAFT_FILE+x}" ] || [ -n "${GIT_SHALLOW_FILE+x}" ]; then
    echo "GIT_GRAFT_FILE / GIT_SHALLOW_FILE is set (graft / shallow history) - unset it before the watcher"; return 0
  fi
  s="$(git -C "$W" rev-parse --is-shallow-repository 2>/dev/null)" || { echo "cannot tell whether the pinned worktree is a shallow clone (git rev-parse failed)"; return 0; }
  [ "$s" = false ] || { echo "the pinned worktree is a shallow clone (history cut) - run git fetch --unshallow first"; return 0; }
  gp="$(git -C "$W" rev-parse --git-path info/grafts 2>/dev/null)" || { echo "cannot read the git path info/grafts of the pinned worktree"; return 0; }
  case "$gp" in /*) ;; *) gp="$W/$gp";; esac
  if [ -e "$gp" ] || [ -L "$gp" ]; then echo "the pinned worktree's repository has info/grafts (grafted history) - remove it first"; fi
  return 0
}
store_listing() {   # name:sha256 of every entry of the store folder (C order, comma separated; a non-regular entry = name:other)
  local LC_ALL=C f n out=""
  for f in "$STORE"/* "$STORE"/.[!.]* "$STORE"/..?*; do
    [ -e "$f" ] || [ -L "$f" ] || continue
    n="$(basename "$f")"
    if [ -f "$f" ] && [ ! -L "$f" ]; then out="$out,$n:$(sha256sum "$f" | awk '{print $1}')"; else out="$out,$n:other"; fi
  done
  printf '%s' "${out#,}"
  return 0
}
finished() {   # $1 = an earlier log folder: 0 when that attempt counts as run to the end (ledger section 3)
  if [ -f "$1/DONE" ] && grep -qx 'solve_started=1' "$1/meta.txt" 2>/dev/null; then return 0; fi
  if [ -f "$1/WATCHER_FAILED" ] && grep -q ' runner started - maxiter ' "$1/status.log" 2>/dev/null; then return 0; fi
  return 1
}
group_stop() {   # TERM to the whole runner process group, wait up to 10 s, then KILL whatever is left
  local i=0
  [ -n "$RPID" ] || return 0
  kill -TERM -- "-$RPID" 2>/dev/null
  while [ "$i" -lt 10 ] && [ "$(group_count)" -gt 0 ]; do sleep 1; i=$((i + 1)); done
  if [ "$(group_count)" -gt 0 ]; then kill -KILL -- "-$RPID" 2>/dev/null; sleep 1; fi
  return 0
}
on_signal() {
  if [ "$RUNNER_STARTED" = 1 ]; then
    [ -n "$RPID" ] || RPID="$(jobs -p 2>/dev/null | head -n 1)"
    if [ -z "$RPID" ]; then stop "signal received before the runner started"; fi
    if [ "$ABORTED" = 0 ]; then
      ABORTED=1
      say "signal received - stopping the runner group"
      group_stop
    fi
  else
    stop "signal received before the runner started"
  fi
}
on_exit() {   # a watcher that ends any other way than STOP / DONE
  local rc=$?
  [ "$FINISHED" = 1 ] && return 0
  FINISHED=1
  [ -n "$LOGF" ] || return 0
  if [ "$RUNNER_STARTED" = 1 ]; then
    say "WATCHER FAILED (rc $rc) after the runner started - stopping the runner group; the record is incomplete; the lock $(homerel "$LOCK") is kept"
    group_stop
    { printf 'rc=%s\nrunner_started=1\n' "$rc"; [ -z "$WF_REASON" ] || printf 'reason=%s\n' "$WF_REASON"; } > "$L/WATCHER_FAILED"
  else
    release_lock
    printf 'reason=the watcher ended unexpectedly (rc %s)\nrunner_started=0\n' "$rc" > "$L/STOPPED"
    say "STOP: the watcher ended unexpectedly (rc $rc) (runner not started)"
  fi
  rm -f "$L/watcher.pid"
}
trap on_exit EXIT

# ---- arguments (nothing is written yet) ----
if [ "$#" -lt 5 ] || [ "$#" -gt 6 ]; then
  echo "[probe6] STOP: usage: bash run_probe6.sh <W> <O> <L> <PIN> <MAXITER> [ROOT] (runner not started)"
  exit 2
fi
W=$1; O=$2; L=$3; PIN=$4; MAXITER=$5; ROOT=${6:-$HOME/sdcp}
# the log folder is checked first: every STOP after it leaves a STOPPED marker there
okpath "$L" || { echo "[probe6] STOP: path must be absolute and use only A-Za-z0-9._/+- : $(homerel "$L") (runner not started)"; exit 2; }
[ -d "$L" ] && [ ! -L "$L" ] || { echo "[probe6] STOP: log folder does not exist: $(homerel "$L") (runner not started)"; exit 2; }
for f in "$L"/* "$L"/.[!.]* "$L"/..?*; do
  [ -e "$f" ] || [ -L "$f" ] || continue
  if [ "$(basename "$f")" != nohup.out ]; then
    echo "[probe6] STOP: log folder is not new (found $(basename "$f")): $(homerel "$L") (runner not started)"
    exit 2
  fi
done
exec 2>> "$L/watcher.err"
LOGF="$L/status.log"
echo "$$" > "$L/watcher.pid"
trap on_signal TERM INT HUP
say "start - watcher for probe 6 (runner output goes to the log folder only)"

# ---- checks ----
for p in "$W" "$O" "$ROOT"; do
  okpath "$p" || stop "path must be absolute and use only A-Za-z0-9._/+- : $(homerel "$p")"
done
# the earlier attempts are read from $HOME/p6log_* - a log folder elsewhere would not see them
LP="$(cd "$(dirname "$L")" 2>/dev/null && pwd -P)" || LP=""
HP="$(cd "$HOME" 2>/dev/null && pwd -P)" || HP=""
[ -n "$LP" ] && [ "$LP" = "$HP" ] || stop "log folder must be directly in the home folder (~/p6log_a<N>_<...>) so that the earlier attempts are seen"
case "$(basename "$L")" in
  p6log_a1_*) ATTEMPT=1;;
  p6log_a2_*) ATTEMPT=2;;
  p6log_a3_*) ATTEMPT=3;;
  p6log_a4_*) ATTEMPT=4;;
  *) stop "log folder name must start with p6log_a1_, p6log_a2_, p6log_a3_ or p6log_a4_ (the attempt number)";;
esac
case "$(basename "$O")" in
  "ca1_probe6_a${ATTEMPT}_"*_arm1) ;;
  *) stop "output folder name must be ca1_probe6_a${ATTEMPT}_<...>_arm1 (same attempt number as the log folder; the runner appends _arm1 otherwise)";;
esac
( LC_ALL=C; case "$PIN" in ""|*[!0-9a-f]*) exit 1;; esac; [ "${#PIN}" -eq 40 ] ) || stop "PIN is not a 40-hex commit"
digits "$MAXITER" 9 && [ "$MAXITER" -ge 1 ] || stop "MAXITER must be a positive integer (digits only)"
# the registered pair of attempt number and iteration limit (ledger section 3)
case "$ATTEMPT" in
  1) WANT_MAX=30000;;
  2) WANT_MAX=1500000;;
  3) WANT_MAX=1500000;;
  4) WANT_MAX=1500000;;
esac
[ "$MAXITER" = "$WANT_MAX" ] || stop "attempt $ATTEMPT runs with maxiter $WANT_MAX (registered pairs 1 -> 30000, 2 -> 1500000, 3 -> 1500000, 4 -> 1500000), not $MAXITER"
if mkdir "$LOCK" 2>/dev/null; then
  LOCKED=1
  printf 'pid=%s\nlogdir=%s\n' "$$" "$(homerel "$L")" > "$LOCK/owner"
else
  stop "another probe 6 watcher holds the lock $(homerel "$LOCK") (or one that died left it) - look at $(homerel "$LOCK")/owner; if no watcher runs, remove that folder by hand"
fi
# ---- earlier attempts (one ledger line per attempt; ledger section 3) ----
for d in "$HOME"/p6log_*; do
  [ -d "$d" ] && [ "$(basename "$d")" != "$(basename "$L")" ] || continue
  if [ -e "$d/DONE" ] || [ -e "$d/STOPPED" ] || [ -e "$d/WATCHER_FAILED" ]; then continue; fi
  stop "earlier log folder $(homerel "$d") has no end marker (DONE / STOPPED / WATCHER_FAILED): a watcher still runs there or died - look at its status.log"
done
for d in "$HOME"/p6log_a"$ATTEMPT"_*; do
  [ -d "$d" ] && [ "$(basename "$d")" != "$(basename "$L")" ] || continue
  if finished "$d"; then
    stop "attempt $ATTEMPT already ran to the end in $(homerel "$d") (DONE with solve_started=1, or WATCHER_FAILED after the runner-start line) - one ledger line per attempt"
  fi
done
for M in 2 3 4; do   # a higher-numbered attempt that ran to the end closes this number
  [ "$M" -gt "$ATTEMPT" ] || continue
  for d in "$HOME"/p6log_a"$M"_*; do
    if [ -d "$d" ] && finished "$d"; then stop "attempt $M already ran to the end in $(homerel "$d") - attempt $ATTEMPT does not run after attempt $M"; fi
  done
done
PREV=0; PD=""
if [ "$ATTEMPT" -ge 2 ]; then
  PREV=$((ATTEMPT - 1))
  N1=0
  for d in "$HOME"/p6log_a"$PREV"_*; do
    [ -d "$d" ] || continue
    if [ -f "$d/DONE" ] && grep -qx 'solve_started=1' "$d/meta.txt" 2>/dev/null; then
      N1=$((N1 + 1))
      P1="$(sed -n 's/^pin=//p' "$d/meta.txt" | head -n 1)"
      PD="$d"
    fi
  done
  [ "$N1" = 1 ] || stop "attempt $ATTEMPT needs exactly one attempt-$PREV log folder with DONE and solve_started=1 (found $N1)"
  ( LC_ALL=C; case "$P1" in ""|*[!0-9a-f]*) exit 1;; esac; [ "${#P1}" -eq 40 ] ) || stop "the attempt-$PREV meta pin is not a 40-hex commit"
fi
PSL="$(ps -u "$(id -u)" -o pid=,args= 2>/dev/null)" || stop "cannot list the processes of this account (ps failed)"
BUSY="$(printf '%s\n' "$PSL" | awk -v me="$$" '$1 != me && (index($0, "sdcp_gain_vox015_8arm.sh") || index($0, "mpm_webapp_payload.py")) { n++ } END { print n + 0 }')"
[ "$BUSY" = 0 ] || stop "a runner (sdcp_gain_vox015_8arm.sh) or payload (mpm_webapp_payload.py) already runs under this account ($BUSY process(es)) - one solve at a time"
if [ -e "$O" ] || [ -L "$O" ]; then
  { [ -d "$O" ] && [ ! -L "$O" ] && [ -z "$(ls -A "$O" 2>/dev/null)" ]; } || stop "output folder exists and is not empty: $(homerel "$O")"
fi
# store folder (attempts 3 and 4): fixed ~/p6_cjstore; attempt 3 = absent or empty, attempt 4 = what attempt 3 left
STORE=""; STORE_BEFORE=""; STORE_AFTER=""
if [ "$ATTEMPT" -ge 3 ]; then
  STORE="${HOME%/}/p6_cjstore"
  ( LC_ALL=C; case "$STORE" in *[!A-Za-z0-9._/-]*) exit 1;; esac ) || stop "the store folder path has a character the runner refuses (only A-Za-z0-9._/-): $(homerel "$STORE")"
  case "$STORE/" in *//*|*/./*|*/../*) stop "the store folder path is not in normal form (no //, . or .. parts): $(homerel "$STORE")";; esac
  if [ -L "$STORE" ]; then stop "the store folder is a symbolic link: $(homerel "$STORE")"; fi
  if [ "$ATTEMPT" = 3 ]; then
    if [ -e "$STORE" ]; then
      { [ -d "$STORE" ] && [ -z "$(ls -A "$STORE" 2>/dev/null)" ]; } || stop "attempt 3 needs an absent or empty store folder (it builds and writes the registry): $(homerel "$STORE")"
    fi
  else
    [ -d "$STORE" ] || stop "attempt 4 needs the store folder attempt 3 wrote: $(homerel "$STORE")"
    WANT_LIST="$(sed -n 's/^store_listing_after=//p' "$PD/meta.txt" | head -n 1)"
    [ -n "$WANT_LIST" ] || stop "the attempt-3 meta has no store listing (store_listing_after)"
    STORE_BEFORE="$(store_listing)"
    [ "$STORE_BEFORE" = "$WANT_LIST" ] || stop "the store folder differs from what attempt 3 left (names / sha256) - attempt 4 reads exactly that registry"
  fi
fi
T="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
TW="$(cd "$W/$TOOLS_REL" 2>/dev/null && pwd -P)" || TW=""
[ -n "$TW" ] && [ "$T" = "$TW" ] || stop "this watcher is not the copy inside the pinned worktree"
READER="$T/probe6_read.py"; RUNNER="$W/$RUNNER_REL"; S0PLAN="$W/$S0PLAN_REL"
for f in "$READER" "$RUNNER" "$S0PLAN"; do
  [ -f "$f" ] || stop "missing in the pinned worktree: $(homerel "$f")"
done
HEAD_NOW="$(git -C "$W" rev-parse HEAD 2>/dev/null)" || stop "git rev-parse failed in the pinned worktree"
[ "$HEAD_NOW" = "$PIN" ] || stop "worktree HEAD differs from PIN"
DIRTY="$(git -C "$W" status --porcelain --untracked-files=all 2>/dev/null)" || stop "git status failed in the pinned worktree"
GIT_BEFORE="$(printf '%s' "$DIRTY" | grep -c .)"
[ -z "$DIRTY" ] || stop "pinned worktree is not clean ($GIT_BEFORE line(s) in git status)"
# attempt N >= 2: the attempt-(N-1) pin is this pin or an earlier commit of it (history neither grafted nor shallow); attempt 2
# runs the solve code of attempt 1 (author 2026-11-10 Q2 (a)) and attempt 4 the solve code of attempt 3 (CODE_PATHS equal)
if [ "$ATTEMPT" -ge 2 ]; then
  HPB="$(history_problem)"
  [ -z "$HPB" ] || stop "$HPB"
  { [ "$P1" = "$PIN" ] || git -C "$W" merge-base --is-ancestor "$P1" "$PIN" 2>/dev/null; } \
    || stop "the attempt-$PREV pin is not this PIN or an earlier commit of it"
fi
if [ "$ATTEMPT" = 2 ] || [ "$ATTEMPT" = 4 ]; then
  git -C "$W" diff --quiet "$P1" "$PIN" -- "${CODE_PATHS[@]}" 2>/dev/null
  case $? in
    0) ;;
    1) stop "the solve code changed between the attempt-$PREV pin and this PIN: $(git -C "$W" diff --name-only "$P1" "$PIN" -- "${CODE_PATHS[@]}" 2>/dev/null | head -n 5 | tr '\n' ' ')- attempt $ATTEMPT runs the code of attempt $PREV";;
    *) stop "cannot compare the solve code of the attempt-$PREV pin and this PIN (git diff failed)";;
  esac
fi
VENV="$HOME/dem-venv"
[ -f "$VENV/bin/activate" ] || stop "venv not found: $(homerel "$VENV")"
set +u
. "$VENV/bin/activate"
set -u
# PYTHONPATH would put other modules in front of the pinned code: removed before any python of the watcher, the gates,
# the runner and the payload runs (recorded as pythonpath_removed; pythonpath_set = still there at the runner start)
if [ -n "${PYTHONPATH+x}" ]; then PPR=1; unset PYTHONPATH; fi
command -v python3 >/dev/null 2>&1 || stop "python3 not found after activating the venv"
command -v setsid >/dev/null 2>&1 || stop "setsid not found (the runner gets its own process group)"
K="$ROOT/$KIT"
[ -d "$K" ] && [ -f "$K/run_mpm.sh" ] || stop "kit not found: $(homerel "$K")"
RUNP=""
if [ -e "$K/latest_run" ]; then
  RUNP="$(cd "$K/latest_run" 2>/dev/null && pwd -P)" || RUNP=""
else
  for d in "$K"/run_*; do
    if [ -f "$d/se_dump.npy" ]; then RUNP="$(cd "$d" && pwd -P)"; fi
  done
fi
[ -n "$RUNP" ] && [ -d "$RUNP" ] || stop "no compaction run folder in the kit"
S0INFO="$(python3 -I -B - "$S0PLAN" <<'PYS0'
import json
import sys
try:
    with open(sys.argv[1], encoding='utf-8') as f:
        p = json.load(f)
    print('%s %r' % (p['source']['run_dir_name'], p['values_um']['tol_ff']))
except Exception as e:
    print('ERR %s' % type(e).__name__)
PYS0
)" || stop "cannot read the S0 stage-1 plan"
S0RUN="${S0INFO%% *}"; S0TOL="${S0INFO#* }"
[ "$S0RUN" != ERR ] && [ -n "$S0RUN" ] || stop "cannot read the S0 stage-1 plan ($S0TOL)"
[ "$S0TOL" = "$TOL_FF" ] || stop "S0 stage-1 plan tol_ff differs from the registered command value"
[ "$(basename "$RUNP")" = "$S0RUN" ] || stop "kit run folder is not the S0 stage-1 bed (run folder name differs from the S0 plan)"
# kit payload line (the runner builds the arm command from it): conditions that are certain to waste the attempt
#   --joule-heat / --save-step4-grid: the payload refuses them at entry when face_alpha or the junction block is on
#   (scripts/mpm_webapp_payload.py, S1_FACE_ALPHA_REFUSED / S2_CJUNC_REFUSED; scripts/test_rint_r_chain_e2e.py E6)
#   --show-results: the runner keeps the kit base command, so the payload would print sigma into the runner log
for flag in --joule-heat --save-step4-grid --show-results; do
  if grep -q -e "$flag" "$K/run_mpm.sh" 2>/dev/null; then
    stop "the kit run_mpm.sh has $flag (refused at payload entry or unseals the results)"
  fi
done
# the registered command expects the GPU backend: without --step3-gpu in the kit payload line the payload would
# solve on the CPU and the runner would then refuse the arm (same test as scripts/sr01_stamp_ab.sh)
grep -q -e '--step3-gpu' "$K/run_mpm.sh" 2>/dev/null \
  || stop "the kit run_mpm.sh has no --step3-gpu (the payload would solve on the CPU and the runner would refuse the arm)"
command -v nvidia-smi >/dev/null 2>&1 || stop "nvidia-smi not found (the registered command expects the GPU backend)"
TMO=()
if command -v timeout >/dev/null 2>&1; then TMO=(timeout -k 5 30); fi
GPUQ="$(${TMO[@]+"${TMO[@]}"} nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader,nounits 2>/dev/null | head -1)"
[ -n "$GPUQ" ] || stop "nvidia-smi query failed (the registered command expects the GPU backend)"
GN="$(printf '%s' "$GPUQ" | awk -F, '{gsub(/^ +| +$/, "", $1); print $1}')"
GD="$(printf '%s' "$GPUQ" | awk -F, '{gsub(/^ +| +$/, "", $2); print $2}')"
GM="$(printf '%s' "$GPUQ" | awk -F, '{gsub(/^ +| +$/, "", $3); print $3}')"

# ---- environment fingerprint (versions only) ----
{
  python3 - <<'PYENV'
import platform
print('python=' + platform.python_version())
print('python_impl=' + platform.python_implementation())
for n in ('numpy', 'scipy', 'cupy'):
    try:
        m = __import__(n)
        print('%s=%s' % (n, getattr(m, '__version__', 'unknown')))
    except Exception:
        print('%s=ABSENT' % n)
try:
    import cupy
    print('cupy_cuda_runtime=%s' % cupy.cuda.runtime.runtimeGetVersion())
except Exception:
    print('cupy_cuda_runtime=unknown')
try:
    import numpy
    try:
        libs = numpy.__config__.blas_opt_info.get('libraries')
    except Exception:
        libs = numpy.show_config(mode='dicts')['Build Dependencies']['blas']['name']
    print('numpy_blas=%s' % (','.join(libs) if isinstance(libs, (list, tuple)) else libs))
except Exception:
    print('numpy_blas=unknown')
PYENV
  echo "blas_core=$(OPENBLAS_VERBOSE=2 python3 -c 'import numpy' 2>&1 | sed -n 's/^Core: *\([A-Za-z0-9_]*\).*$/\1/p' | head -1)"
  echo "gpu_name=$GN"
  echo "gpu_driver=$GD"
  echo "gpu_mem_total_mib=$GM"
  echo "cuda_version=$(${TMO[@]+"${TMO[@]}"} nvidia-smi 2>/dev/null | sed -n 's/.*CUDA Version: *\([0-9.]*\).*/\1/p' | head -1)"
  echo "kernel=$(uname -sr)"
  echo "os=$(sed -n 's/^PRETTY_NAME="\(.*\)"$/\1/p' /etc/os-release 2>/dev/null | head -1)"
  echo "cpu_model=$(sed -n 's/^model name[^:]*: *//p' /proc/cpuinfo 2>/dev/null | head -1)"
  echo "nproc=$(nproc 2>/dev/null)"
  echo "mem_total_kb=$(awk '/^MemTotal/{print $2}' /proc/meminfo 2>/dev/null)"
  echo "git=$(git --version 2>/dev/null | awk '{print $3}')"
  echo "bash=${BASH_VERSION%%(*}"
} > "$L/env.txt" 2> "$L/env.err"
if grep -q '^cupy=ABSENT' "$L/env.txt"; then
  stop "cupy cannot be imported in this venv (the registered command expects the GPU backend)"
fi

# ---- sampling interval and host memory cap ----
SAMPLE_S="${PROBE6_SAMPLE_S:-10}"
digits "$SAMPLE_S" 4 && [ "$SAMPLE_S" -ge 1 ] || stop "PROBE6_SAMPLE_S must be a positive integer"
if [ -n "${PROBE6_CAP_GB+x}" ]; then
  CAP="$PROBE6_CAP_GB"
  digits "$CAP" 4 || stop "PROBE6_CAP_GB must be digits"
else
  AV="$(awk '/^MemAvailable/{print int($2/1048576)}' /proc/meminfo 2>/dev/null)"
  CAP=$(( ${AV:-0} - 6 ))
  if [ "$CAP" -gt 46 ]; then CAP=46; fi
  [ "$CAP" -ge 1 ] || stop "not enough free host memory (MemAvailable ${AV:-0} GB)"
fi

# ---- environment: drop every runner-axis variable, then set exactly the registered ones ----
SCRUBBED=""
for n in $(compgen -e); do
  case "$n" in
    SIGMA_*|SDCP_*|PTFE_*|CJUNC*|STEP3_*|MPM_*|P2_*|LEAN|VOX|ARMS|ARM_LIST|KITS|FIBRE_STAMP|BRIDGE_UM|OUTDIR|EXPECT_PROTOCOL|EXPECT_BACKEND)
      unset "$n"
      SCRUBBED="$SCRUBBED $n";;
  esac
done
SCRUBBED="${SCRUBBED# }"
PP=0
if [ -n "${PYTHONPATH+x}" ]; then PP=1; fi
# PYTHONUNBUFFERED=1 is not a physics axis: the payload prints "CG not converged" without a flush, and a buffered
# line is lost when the run is stopped early (README section 4)
CMD=("${AXES[@]}" "P2_EXTRA=--step3-maxiter $MAXITER" "OUTDIR=$O" PYTHONUNBUFFERED=1)
if [ -n "$STORE" ]; then CMD=("${AXES[@]}" "P2_EXTRA=--step3-maxiter $MAXITER" "CJUNC_STORE=$STORE" "OUTDIR=$O" PYTHONUNBUFFERED=1); fi
cd "$ROOT" || stop "cannot enter the kit root"

# ---- the runner's own pre-run gates (read from the runner text, run the same way, before the runner starts) ----
GATES="$(python3 -I -B - "$RUNNER" <<'PYG'
import re
import sys
src = open(sys.argv[1], encoding='utf-8').read()
ok1 = re.search(r'python3 "\$SCR/check_method_discipline\.py"', src)
m2 = re.search(r'python3 "\$SCR/check_undefined_names\.py"(.*?)>/dev/null', src, re.S)
files = re.findall(r'"\$SCR/([A-Za-z0-9_]+\.py)"', m2.group(1)) if m2 else []
print('OK ' + ' '.join(files) if (ok1 and files) else 'ERR')
PYG
)"
case "$GATES" in
  "OK "?*) ;;
  *) stop "cannot read the runner's pre-run gate commands from $(homerel "$RUNNER")";;
esac
UFILES=()
for f in ${GATES#OK }; do UFILES+=("$W/scripts/$f"); done
"${RENV[@]}" "${CMD[@]}" PYTHONUTF8=1 python3 "$W/scripts/check_method_discipline.py" > "$L/pregate_discipline.log" 2>&1 < /dev/null \
  || stop "the runner's own pre-run gate fails: discipline check (log $(homerel "$L")/pregate_discipline.log)"
"${RENV[@]}" "${CMD[@]}" PYTHONUTF8=1 python3 "$W/scripts/check_undefined_names.py" "${UFILES[@]}" > "$L/pregate_undefined.log" 2>&1 < /dev/null \
  || stop "the runner's own pre-run gate fails: undefined-name check (log $(homerel "$L")/pregate_undefined.log)"

# earlier probe files in the kit run folder (same names would be overwritten by this attempt) -> byte copies
NBEFORE=0
for f in "$RUNP"/p2_SBE_vgcf100_*.json "$RUNP"/p2_SBE_vgcf100_*.json.failed "$RUNP"/p2_SBE_vgcf100_*.json.part "$RUNP"/.peak_rss_p2_SBE_vgcf100_*; do
  if [ -f "$f" ] && [ ! -L "$f" ]; then
    mkdir -p "$L/kit_run_before" && cp "$f" "$L/kit_run_before/" || stop "cannot preserve an earlier probe file of the kit run folder"
    NBEFORE=$((NBEFORE + 1))
  fi
done
# attempt 3: the store folder is made only now (every check passed); umask 022 -> 0755 (the payload checks owner and mode)
if [ "$ATTEMPT" = 3 ] && [ ! -d "$STORE" ]; then
  mkdir "$STORE" || stop "cannot make the store folder $(homerel "$STORE")"
fi
{
  echo "# cwd: $(homerel "$ROOT")"
  printf '%s' "${RENV[*]}"
  for a in "${CMD[@]}"; do
    case "$a" in
      OUTDIR=*) printf ' OUTDIR=%s' "$(homerel "${a#*=}")";;
      CJUNC_STORE=*) printf ' CJUNC_STORE=%s' "$(homerel "${a#*=}")";;
      *" "*) printf ' %s="%s"' "${a%%=*}" "${a#*=}";;
      *) printf ' %s' "$a";;
    esac
  done
  printf ' bash %s\n' "$(homerel "$RUNNER")"
} > "$L/command.txt"
ENVREC="$( export PYTHONUNBUFFERED=1; for n in $ENV_NAMES; do printf 'env_%s=%s\n' "$n" "$(envrec "$n")"; done )"
G0="$(${TMO[@]+"${TMO[@]}"} nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader,nounits 2>/dev/null | head -1 | tr -d ' ')"
GU0="${G0%%,*}"; digits "${GU0:-x}" 7 || GU0=NA
DFK="$(df -Pk "$ROOT" 2>/dev/null | awk 'NR == 2 { printf "%d", $4 / 1048576 }')"; digits "${DFK:-x}" 9 || DFK=NA
DFL="$(df -Pk "$L" 2>/dev/null | awk 'NR == 2 { printf "%d", $4 / 1048576 }')"; digits "${DFL:-x}" 9 || DFL=NA
say "pre-launch: attempt $ATTEMPT, GPU memory in use $GU0 MiB of $GM MiB, disk free $DFK GB (kit root) and $DFL GB (log folder)"
printf '#epoch\telapsed_s\tlog_lines\trss_sum_kb\trss_proc_kb\tgpu_used_mib\tgpu_ours_mib\tgpu_util\n' > "$L/samples.tsv"

# ---- start the runner in its own session / process group (all of its output -> runner.log) ----
START="$(date +%s)"
START_KST="$(TZ=Asia/Seoul date +%Y-%m-%dT%H:%M:%S%z)"
TV=0
TIMEV=()
if [ -x /usr/bin/time ]; then
  TV=1
  TIMEV=(/usr/bin/time -v -o "$L/time_v.txt")
fi
RUNNER_STARTED=1
setsid ${TIMEV[@]+"${TIMEV[@]}"} "${RENV[@]}" "${CMD[@]}" bash "$RUNNER" > "$L/runner.log" 2>&1 < /dev/null &
RPID=$!
say "runner started - maxiter $MAXITER, host RSS cap $CAP GB, sampling every $SAMPLE_S s"
# the runner must lead its own session: otherwise setsid forked (job control on) and the watched group is not the runner's
if ! runner_leads_session; then
  WF_REASON="the runner (pid $RPID) does not lead its own session - setsid forked (job control on?); its processes may run outside the watched group - look at ps"
  say "$WF_REASON"
  exit 1
fi

stage() {
  if grep -q '^saved ' "$L/runner.log" 2>/dev/null; then echo saved
  elif grep -q 'STEP3 solve:' "$L/runner.log" 2>/dev/null; then echo cg
  elif grep -q 'STEP3: voxelizing' "$L/runner.log" 2>/dev/null; then echo raster
  else echo before_step3
  fi
}
RS=0
sample() {
  local now el nl line rp pids g gu gut a ours
  now="$(date +%s)"
  el=$((now - START))
  nl="$(wc -l < "$L/runner.log" 2>/dev/null)"
  nl=$(( ${nl:-0} + 0 ))
  line="$(ps -e -o pid=,pgid=,rss= 2>/dev/null | awk -v g="$RPID" '
    $2 == g { s += $3; if ($3 > m) m = $3; l = l $1 "," }
    END { printf "%d %d ,%s\n", s, m, l }')"
  RS="${line%% *}"; line="${line#* }"; rp="${line%% *}"; pids="${line#* }"
  digits "${RS:-x}" 12 || RS=0
  digits "${rp:-x}" 12 || rp=0
  gu=NA; gut=NA; ours=NA
  g="$(${TMO[@]+"${TMO[@]}"} nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader,nounits 2>/dev/null | head -1 | tr -d ' ')"
  if digits "${g%%,*}" 7 && digits "${g#*,}" 3; then gu="${g%%,*}"; gut="${g#*,}"; fi
  if a="$(${TMO[@]+"${TMO[@]}"} nvidia-smi --query-compute-apps=pid,used_memory --format=csv,noheader,nounits 2>/dev/null)"; then
    ours="$(printf '%s\n' "$a" | tr -d ' ' | awk -F, -v set="$pids" '{ if ($1 != "" && index(set, "," $1 ",")) s += $2 } END { printf "%d", s + 0 }')"
    digits "${ours:-x}" 7 || ours=NA
  fi
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$now" "$el" "$nl" "$RS" "$rp" "$gu" "$ours" "$gut" >> "$L/samples.tsv"
  if [ $((el - LAST_HB)) -ge 600 ]; then
    LAST_HB="$el"
    say "running - elapsed ${el} s, stage $(stage), log lines $nl, host RSS $((RS / 1048576)) GB, GPU used ${gu} MiB"
  fi
}
LAST_HB=-600   # the first sample prints a status line at once (GPU memory already in use at the start is visible)
while kill -0 "$RPID" 2>/dev/null; do
  sample
  if [ "$CAPTERM" = 0 ] && [ "$ABORTED" = 0 ] && [ $((RS / 1048576)) -ge "$CAP" ]; then
    CAPTERM=1
    say "host RSS cap reached ($((RS / 1048576)) GB >= $CAP GB) - stopping the runner group"
    group_stop
  fi
  sleep "$SAMPLE_S"
done
# from here on a TERM / INT / HUP is held until the record is complete (the runner is over; nothing left to stop)
trap 'LATE_SIG=$((LATE_SIG + 1))' TERM INT HUP
wait "$RPID" 2>/dev/null
RC=$?
LAST_HB=999999999
sample
END="$(date +%s)"
END_KST="$(TZ=Asia/Seoul date +%Y-%m-%dT%H:%M:%S%z)"
say "runner ended - rc $RC, wall $((END - START)) s"
ORPH="$(group_count)"
if [ "$ORPH" -gt 0 ]; then
  say "the runner group still has $ORPH process(es) after the runner ended - stopping them"
  group_stop
fi
LEFT="$(group_count)"

# ---- record (no value of the solve is read here) ----
MODEBAD="$(find "$O" "$L" ! -type l -perm /022 2>/dev/null | wc -l)"
if [ -n "$STORE" ]; then STORE_AFTER="$(store_listing)"; fi
GIT_AFTER="$(git -C "$W" status --porcelain --untracked-files=all 2>/dev/null | grep -c .)"
SOLVE=0
if grep -q 'STEP3 solve:' "$L/runner.log" 2>/dev/null; then SOLVE=1; fi
NNEW=0
for f in "$RUNP"/p2_SBE_vgcf100_* "$RUNP"/.peak_rss_p2_SBE_vgcf100_*; do
  if [ -f "$f" ] && [ ! -L "$f" ] && [ "$f" -nt "$L/command.txt" ]; then
    mkdir -p "$L/kit_run_new" && cp "$f" "$L/kit_run_new/" && NNEW=$((NNEW + 1))
    case "$(basename "$f")" in .peak_rss_*) cp "$f" "$L/arm_time_v.txt";; esac
  fi
done
sha() { sha256sum "$1" 2>/dev/null | awk '{print $1}'; }
{
  echo "probe6_meta_version=2"
  echo "attempt=$ATTEMPT"
  echo "pin=$PIN"
  if [ "$ATTEMPT" = 2 ]; then
    echo "attempt1_pin=$P1"
    echo "code_same_as_attempt1=1"
  fi
  if [ "$ATTEMPT" = 3 ]; then
    echo "attempt2_pin=$P1"
  fi
  if [ "$ATTEMPT" = 4 ]; then
    echo "attempt3_pin=$P1"
    echo "code_same_as_attempt3=1"
  fi
  if [ -n "$STORE" ]; then
    echo "store=$(homerel "$STORE")"
    echo "store_listing_before=$STORE_BEFORE"
    echo "store_listing_after=$STORE_AFTER"
  fi
  echo "maxiter=$MAXITER"
  echo "expect_rtol=$EXP_RTOL"
  echo "expect_backend=$EXP_BACKEND"
  echo "expect_rj=$EXP_RJ"
  echo "kit=$KIT"
  echo "kit_run=$(basename "$RUNP")"
  echo "kit_run_matches_s0=1"
  echo "outdir=$(homerel "$O")"
  echo "logdir=$(homerel "$L")"
  echo "start_epoch=$START"
  echo "start_kst=$START_KST"
  echo "end_epoch=$END"
  echo "end_kst=$END_KST"
  echo "wall_s=$((END - START))"
  echo "runner_rc=$RC"
  echo "solve_started=$SOLVE"
  echo "orphans=$((ORPH + 0))"
  echo "orphans_left=$((LEFT + 0))"
  echo "cap_gb=$CAP"
  echo "cap_term=$CAPTERM"
  echo "aborted=$ABORTED"
  echo "sample_s=$SAMPLE_S"
  echo "time_v=$TV"
  echo "umask=$(umask)"
  echo "mode_bad=$((MODEBAD + 0))"
  echo "git_lines_before=$((GIT_BEFORE + 0))"
  echo "git_lines_after=$((GIT_AFTER + 0))"
  echo "pregate=1"
  echo "scrubbed=$SCRUBBED"
  echo "pythonpath_set=$PP"
  echo "pythonpath_removed=$PPR"
  printf '%s\n' "$ENVREC"
  echo "gpu_used_start_mib=$GU0"
  echo "disk_free_gb_kit=$DFK"
  echo "disk_free_gb_log=$DFL"
  echo "tool_sha256_wrapper=$(sha "$T/run_probe6.sh")"
  echo "tool_sha256_reader=$(sha "$READER")"
  echo "runner_sha256=$(sha "$RUNNER")"
  echo "runner_log_sha256=$(sha "$L/runner.log")"
  echo "s0_plan_sha256=$(sha "$S0PLAN")"
  echo "kit_run_before=$NBEFORE"
  echo "kit_run_new=$NNEW"
} > "$L/meta.txt"

# ---- value-blind report (closed allowlist) ----
python3 -I -B "$READER" --outdir "$O" --logdir "$L" --kit-run "$RUNP" --s0-plan "$S0PLAN" > "$L/probe6_screen.txt" 2> "$L/probe6_reader.err"
RRC=$?
cat "$L/probe6_screen.txt"
say "report rc $RRC (0 PROBE_OK, 3 not converged, 4 incomplete, 5 rejected)"

# ---- bundle: allowlisted report + fingerprint + numeric diagnostics only (copies taken now, in bundle_files/) ----
#   status.log is copied before this line and the DONE line; time -v records keep only three lines (no command line)
STG="$L/bundle_files"
MEMBERS=""
BSHA=none
if mkdir "$STG" 2>/dev/null; then
  for f in probe6_report.json probe6_screen.txt runner_filtered.log env.txt meta.txt command.txt samples.tsv status.log probe6_reader.err; do
    if [ -f "$L/$f" ] && cp "$L/$f" "$STG/$f"; then MEMBERS="$MEMBERS $f"; fi
  done
  for f in time_v.txt arm_time_v.txt; do
    if [ -f "$L/$f" ]; then
      grep -E '^[[:space:]]*(Maximum resident set size \(kbytes\)|Elapsed \(wall clock\) time \(h:mm:ss or m:ss\)|Exit status): ' "$L/$f" > "$STG/$f"
      MEMBERS="$MEMBERS $f"
    fi
  done
  if ( cd "$STG" && sha256sum $MEMBERS > SHA256SUMS && tar -czf "$L/probe6_bundle.tgz" $MEMBERS SHA256SUMS ); then
    BSHA="$(sha "$L/probe6_bundle.tgz")"
    echo "$BSHA  probe6_bundle.tgz" > "$L/probe6_bundle.sha256"
  fi
fi
say "bundle $(homerel "$L/probe6_bundle.tgz") sha256 $BSHA"
# DONE only after the runner group is empty (a process stuck in the GPU driver keeps the record open)
W_LEFT=0
while [ "$(group_count)" -gt 0 ]; do
  if [ $((W_LEFT % 600)) -eq 0 ]; then say "waiting for $(group_count) process(es) of the runner group to end before DONE"; fi
  kill -KILL -- "-$RPID" 2>/dev/null
  sleep 10
  W_LEFT=$((W_LEFT + 10))
done
if [ "$LATE_SIG" -gt 0 ]; then say "$LATE_SIG signal(s) during the final record were held until the record was complete"; fi
release_lock
rm -f "$L/watcher.pid"
FINISHED=1
say "DONE runner_rc=$RC report_rc=$RRC attempt=$ATTEMPT"
echo "runner_rc=$RC report_rc=$RRC attempt=$ATTEMPT orphans=$((ORPH + 0))" > "$L/DONE"
if [ "$RC" -eq 0 ] && [ "$RRC" -eq 0 ]; then exit 0; fi
exit 1
