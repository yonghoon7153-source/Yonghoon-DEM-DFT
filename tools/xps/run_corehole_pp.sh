#!/bin/bash
# Generate P ground + P-1s-core-hole pseudopotentials. Run from the repo root on gabia:
#   bash tools/xps/run_corehole_pp.sh
# Copies the (git-clean) .in files into the QE work dir and runs ld1.x with a 120s timeout.
set +H
SELF=$(cd "$(dirname "$0")" && pwd)
WORK=/data/work/runs/xps_qe
LD1=/data/apps/qe-7.4.1-cpu/bin/ld1.x
pkill -9 -f ld1.x 2>/dev/null; sleep 1
cd "$WORK" || { echo "no $WORK"; exit 1; }
cp "$SELF/P_gs.in" "$SELF/P_ch.in" .
for p in P_gs P_ch; do
  echo "=========== ld1.x $p (in=$(wc -l < $p.in) lines) ==========="
  timeout 120 $LD1 < ${p}.in > ${p}.ld1out 2>&1
  rc=$?
  if [ -f ${p}.UPF ]; then echo "  UPF OK ($(wc -c < ${p}.UPF) bytes)"
  elif [ $rc -eq 124 ]; then echo "  *** TIMEOUT(120s) — likely rel=2 core-hole not converging"
  else echo "  *** NO UPF (rc=$rc):"; grep -iE "error|waiting for input" ${p}.ld1out | head -3; tail -3 ${p}.ld1out; fi
done
echo "=== DONE ==="
