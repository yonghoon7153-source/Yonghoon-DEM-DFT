#!/bin/bash
# SHA256SUMS (폴더 안 모든 파일 · 상대 경로 · 이름 순 · SHA256SUMS 자신 뺌) — preattack14/ · pa14_fix/ · 그 뒤 sha256sum -c 로 다시 대조
set -eu
E=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a271b07eec3fe5332/docs/reviews/rint2_rr2_fix_evidence_20261105
for d in preattack14 pa14_fix; do
  cd "$E/$d"
  find . -type f ! -name SHA256SUMS -printf '%P\n' | LC_ALL=C sort | xargs -d '\n' sha256sum > SHA256SUMS
  echo "$d: $(wc -l < SHA256SUMS) 파일"
  sha256sum -c --quiet SHA256SUMS && echo "$d: sha256sum -c 통과"
done
