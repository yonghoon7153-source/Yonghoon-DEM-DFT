#!/bin/bash
# LHS214 게이트 (763db8878) 가 끝나고 push 되면 → 본 가지를 세미나 반입 커밋 883cf90f5 로 fast-forward → 게이트 → push
cd /home/user/Yonghoon-DEM-DFT || exit 9
OUT=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/tasks/b2sun63m0.output
for i in $(seq 1 720); do grep -q "^origin \|GATE FAILED\|PUSH FAILED\|HEAD moved" "$OUT" 2>/dev/null && break; sleep 10; done
grep -q "PUSHED 763db8878" "$OUT" || { echo "LHS214 gate/push not OK — chain stopped"; tail -5 "$OUT"; exit 4; }
git merge -q --ff-only tmp-sem33-import || { echo "ff failed"; exit 5; }
[ "$(git rev-parse --short=9 HEAD)" = "883cf90f5" ] || { echo "HEAD not 883cf90f5"; exit 6; }
sed "s#gate_1cc5415e8.log#gate_883cf90f5.log#" /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/refaudit/gate_push_imp.sh > /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/refaudit/gate_push_s.sh
bash /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/refaudit/gate_push_s.sh
