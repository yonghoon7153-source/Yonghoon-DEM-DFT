#!/usr/bin/env bash
# Dual-x HIGH-x companion to run_dualx.sh: SAME 10 dopants, SAME 2,2,1 supercell,
# SAME tier_cascade pipeline (mobility-only, killed at STAGE_04) — only the
# concentration differs: X_COMPOUND=0.25 (vs 0.0625 in the lowx run).
# Output dirs: ${cmp}_highx (so it never clobbers the *_lowx results).
# Purpose: apples-to-apples blocking_fraction comparison at x=0.25 vs x=0.0625
# in an identical cell (the lowx run already used 2,2,1).
# NOTE: the typeA_cluster structure-gen bug is left AS-IS on purpose, so both
# concentrations sample structures identically (consistency > completeness here).
# Launch DETACHED under the uma env (survives SSH/WSL drops):
#   conda activate uma
#   setsid bash tools/doping/run_dualx_highx.sh > /data/work/runs/dualx_v23/_driver_highx.log 2>&1 < /dev/null &
cd /data/work/repo
run_highx(){ cmp=$1; OUT=/data/work/runs/dualx_v23/${cmp}_highx
  env COMPOUND_FILTER="$cmp" X_COMPOUND=0.25 bash tools/doping/tier_cascade.sh \
    db/structures/lpscl_F43m_24G_canonical.cif "$OUT" 5 2,2,1 0 >> /data/work/runs/dualx_v23/${cmp}_highx.log 2>&1 & pid=$!
  while kill -0 $pid 2>/dev/null; do [ -f "$OUT/STAGE_04.DONE" ] && { kill -TERM $pid; break; }; sleep 30; done
  wait $pid 2>/dev/null; echo "$cmp stage04 $(date +%H:%M)"; }
for c in Sc2O3 Gd2O3 Cr2O3 Y2O3 La2O3 HfO2 Ta2O5 Nb2O5 V2O5 TiF4; do echo "== $c =="; run_highx $c; done
echo "ALL DUALX HIGHX DONE"
