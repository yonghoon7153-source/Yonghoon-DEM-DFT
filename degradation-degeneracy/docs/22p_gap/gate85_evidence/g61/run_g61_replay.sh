#!/bin/bash
cd /home/user/Yonghoon-DEM-DFT/degradation-degeneracy
echo "START_HEAD=$(git rev-parse HEAD) status=$(git status --porcelain | wc -l) $(date -u +%FT%TZ)"
python docs/22p_gap/mutation_replay.py -k incomplete_receipt_is_refused-g61 2>&1 | grep -v "^$" | tail -5
echo "replay rc=${PIPESTATUS[0]}"
echo "END_HEAD=$(git rev-parse HEAD) $(date -u +%FT%TZ)"
