#!/bin/bash
# 85차 증거 — g61 정정 뒤 단독 재생을 clean HEAD 에서 **필터 없이** (원 16:24Z 실행은 dirty tree status 1 · tail -5 였다)
cd /home/user/Yonghoon-DEM-DFT/degradation-degeneracy
echo "START_HEAD=$(git rev-parse HEAD) status=$(git status --porcelain | wc -l) $(date -u +%FT%TZ)"
python docs/22p_gap/mutation_replay.py -k incomplete_receipt_is_refused-g61
echo "replay rc=$?"
python docs/22p_gap/mutation_replay.py --emit-expect -k incomplete_receipt_is_refused-g61
echo "emit-expect rc=$?"
echo "END_HEAD=$(git rev-parse HEAD) status=$(git status --porcelain | wc -l) $(date -u +%FT%TZ)"
