#!/bin/bash
cd /home/user/Yonghoon-DEM-DFT/degradation-degeneracy
echo "START_HEAD=$(git rev-parse HEAD) status=$(git status --porcelain | wc -l) $(date -u +%FT%TZ)"
python -m pytest tests/ -q --no-header -p no:cacheprovider -rfEx > /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad/g86_pytest_full.txt 2>&1
rc=$?
tail -40 /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad/g86_pytest_full.txt | grep -E "^FAILED|^ERROR|^XFAIL|passed|failed"
echo "pytest rc=$rc $(date -u +%FT%TZ) status=$(git status --porcelain | wc -l)"
t0=$(date +%s); ./scripts/smoke_e2e.sh > /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad/g86_smoke.txt 2>&1; src=$?
echo "smoke rc=$src $(( $(date +%s) - t0 ))s $(date -u +%FT%TZ) status=$(git status --porcelain | wc -l)"
python docs/22p_gap/mutation_replay.py > /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad/g86_replay_all.txt 2>&1
echo "replay rc=$? $(date -u +%FT%TZ)"
python docs/22p_gap/mutation_replay.py --check-preimages 2>&1 | tail -1
python -c "from src.io import source_digest; print('source_digest', source_digest())"
echo "END_HEAD=$(git rev-parse HEAD) status=$(git status --porcelain | wc -l) $(date -u +%FT%TZ)"
