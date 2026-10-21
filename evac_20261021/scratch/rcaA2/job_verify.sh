#!/bin/bash
# verification after the fix commits: probes + off-path bit identity, mutation sweep, regressions (one at a time)
D=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2
date > $D/logs/verify_start.txt
bash $D/job_probes.sh
python3 $D/mutsweep.py $D/impl $D/logs/mutsweep.json > $D/logs/mutsweep.log 2>&1; echo "rc=$?" >> $D/logs/mutsweep.log
bash $D/job_reg.sh r1
date > $D/logs/verify_done.txt
