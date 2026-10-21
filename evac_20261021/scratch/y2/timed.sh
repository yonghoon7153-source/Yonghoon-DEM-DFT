#!/usr/bin/env bash
# usage: timed.sh LOG cmd args...   — runs cmd, writes combined output + elapsed seconds + rc to LOG
log="$1"; shift
t0=$(date +%s.%N)
"$@" > "$log" 2>&1
rc=$?
t1=$(date +%s.%N)
echo "ELAPSED_S=$(python3 -c "print(round($t1-$t0,1))") RC=$rc" >> "$log"
exit $rc
