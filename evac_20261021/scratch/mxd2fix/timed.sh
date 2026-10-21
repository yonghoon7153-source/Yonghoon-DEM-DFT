#!/bin/bash
# usage: bash timed.sh <log> <command...>   — runs the command (cwd unchanged), writes stdout+stderr to <log>,
# appends "rc=<rc> elapsed=<s>s" to the log and prints the last 3 lines.
log="$1"; shift
t0=$(date +%s.%N)
"$@" > "$log" 2>&1
rc=$?
t1=$(date +%s.%N)
echo "rc=$rc elapsed=$(python3 -c "print(round($t1-$t0,1))")s" >> "$log"
tail -n 3 "$log"
exit $rc
