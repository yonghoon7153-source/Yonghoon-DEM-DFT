#!/bin/bash
# Machine-wide limit for runs over ~60 s (10-21 after container restart).
# v2 (10-21 07:5x UTC): at most TWO heavy runs at once (4 CPUs) instead of one.
#   slot 1 = the original heavy.lock (jobs already waiting on it keep their place) · slot 2 = heavy2.lock.
# Usage: bash heavy.sh <command...>   (waits up to 6 h for a free slot; exit code = the command's)
D=${HEAVY_LOCK_DIR:-/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad}
L1=$D/heavy.lock
L2=$D/heavy2.lock
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
