#!/bin/bash
cd /home/user/Yonghoon-DEM-DFT/degradation-degeneracy
echo "START_HEAD=$(git rev-parse HEAD) status=$(git status --porcelain | wc -l) $(date -u +%FT%TZ)"
python -m pytest tests/ -q --no-header -p no:cacheprovider > /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad/g84_pytest_full.txt 2>&1
rc=$?
tail -40 /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad/g84_pytest_full.txt | grep -E "^FAILED|^ERROR|passed|failed"
echo "pytest rc=$rc $(date -u +%FT%TZ)"
t0=$(date +%s); ./scripts/smoke_e2e.sh > /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad/g84_smoke.txt 2>&1; src=$?
tail -3 /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad/g84_smoke.txt
echo "smoke rc=$src $(( $(date +%s) - t0 ))s"
python docs/22p_gap/mutation_replay.py > /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad/g84_replay_full.txt 2>&1
echo "replay rc=$?"; tail -3 /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad/g84_replay_full.txt
python docs/22p_gap/mutation_replay.py --check-preimages 2>&1 | tail -1
echo "END_HEAD=$(git rev-parse HEAD) status=$(git status --porcelain | wc -l) $(date -u +%FT%TZ)"
