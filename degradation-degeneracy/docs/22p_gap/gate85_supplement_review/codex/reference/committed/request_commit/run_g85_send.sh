#!/bin/bash
cd /home/user/Yonghoon-DEM-DFT/degradation-degeneracy
echo "START_HEAD=$(git rev-parse HEAD) status=$(git status --porcelain | wc -l) $(date -u +%FT%TZ)"
python -m pytest tests/ -q --no-header -p no:cacheprovider > /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad/g85_pytest_full.txt 2>&1
rc=$?
tail -40 /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad/g85_pytest_full.txt | grep -E "^FAILED|^ERROR|passed|failed"
echo "pytest rc=$rc $(date -u +%FT%TZ)"
python -m pytest tests/test_docs_lint.py -q --no-header -p no:cacheprovider --co 2>/dev/null | tail -1
t0=$(date +%s); ./scripts/smoke_e2e.sh > /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad/g85_smoke.txt 2>&1; src=$?
echo "smoke rc=$src $(( $(date +%s) - t0 ))s"
python -c "from src.io import source_digest; print('source_digest', source_digest())"
echo "END_HEAD=$(git rev-parse HEAD) status=$(git status --porcelain | wc -l) $(date -u +%FT%TZ)"
