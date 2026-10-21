#!/bin/bash
# 세미나 반입 (883cf90f5) 게이트 · push 가 끝나면 → 본 가지를 Rint 반입 커밋 5bd2e53a9 로 fast-forward → 게이트 → push
cd /home/user/Yonghoon-DEM-DFT || exit 9
OUT=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/tasks/bgzcb6398.output
for i in $(seq 1 720); do grep -q "^origin \|GATE FAILED\|PUSH FAILED\|HEAD moved\|chain stopped\|ff failed\|HEAD not" "$OUT" 2>/dev/null && break; sleep 10; done
grep -q "PUSHED 883cf90f5" "$OUT" || { echo "seminar gate/push not OK — chain stopped"; tail -5 "$OUT"; exit 4; }
git merge -q --ff-only tmp-rimpr-import || { echo "ff failed"; exit 5; }
[ "$(git rev-parse --short=9 HEAD)" = "5bd2e53a9" ] || { echo "HEAD not 5bd2e53a9"; exit 6; }
sed "s#gate_1cc5415e8.log#gate_5bd2e53a9.log#" /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/refaudit/gate_push_imp.sh > /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/refaudit/gate_push_t.sh
bash /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/refaudit/gate_push_t.sh
