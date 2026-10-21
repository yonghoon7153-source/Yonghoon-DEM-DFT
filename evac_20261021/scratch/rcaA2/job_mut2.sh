#!/bin/bash
D=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2
python3 $D/mutsweep2.py > $D/logs/mutsweep2.log 2>&1
echo "rc=$?" >> $D/logs/mutsweep2.log
