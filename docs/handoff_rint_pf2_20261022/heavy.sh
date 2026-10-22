#!/bin/bash
# Machine-wide limit for runs over ~60 s (10-21 after container restart).
# v2 (10-21 07:5x UTC): at most TWO heavy runs at once (4 CPUs) instead of one.
#   slot 1 = the original heavy.lock (jobs already waiting on it keep their place) · slot 2 = heavy2.lock.
# v3 (10-21 08:0x UTC): HEAVY_EXCLUSIVE=1 = take BOTH slots (whole machine) — for runs that start
#   several threads (e.g. 4-thread OpenBLAS path probes); thread variables are then left to the caller.
# Usage: bash heavy.sh <command...>                     (one slot · 1 thread · waits up to 6 h)
#        HEAVY_EXCLUSIVE=1 bash heavy.sh <command...>   (both slots · waits up to 6 h)
# Exit code = the command's.
D=${HEAVY_LOCK_DIR:-${TMPDIR:-/tmp}/rint_heavy_locks}; mkdir -p "$D"
L1=$D/heavy.lock
L2=$D/heavy2.lock
if [ "${HEAVY_EXCLUSIVE:-0}" = "1" ]; then
  # Same order as everyone else (slot 1 first) — single-slot jobs never hold two locks, so no deadlock.
  exec flock -w 21600 "$L1" flock -w 21600 "$L2" nice -n 19 "$@"
fi
BUSY=199                      # flock's own "slot busy" code (-E) — not a code our commands use
deadline=$(( $(date +%s) + 21600 ))
while :; do
  for L in "$L1" "$L2"; do
    flock -n -E $BUSY "$L" env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 nice -n 19 "$@"
    rc=$?
    [ "$rc" -ne "$BUSY" ] && exit "$rc"
  done
  if [ "$(date +%s)" -ge "$deadline" ]; then
    echo "heavy.sh: no free slot within 6 h" >&2
    exit 1
  fi
  sleep 3
done
