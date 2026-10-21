#!/usr/bin/env bash
# U2 — Codex source_audit.py 를 원래 놓인 꼴 (묶음 루트 R · 그 옆 앞 회차 폴더 OLD) 로 다시 세운다 (scratch · 리포에 쓰지 않는다).
#   R   = sa/dem_unloading_kit_fix_recheck_20261015 : probes/ (10-15 증거) · source_manifest.json (10-15 · 핀 eaecfba2a) · source/ = <commit> 의 그 252 경로
#         · submitted/request.md = 10-15 묶음이 받은 정정 요청서 (799459c85 의 10-14 재확인 요청서)
#   OLD = sa/dem_unloading_kit_reverify_20261014     : source_manifest.json (10-14 · 핀 a30fe150e) · source/ = a30fe150e 의 그 203 경로
# 사용: bash setup_source_audit.sh <commit>
set -euo pipefail
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a948397637bfe9a76
U=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_unload/u2
C=${1:?commit}
R=$U/sa/dem_unloading_kit_fix_recheck_20261015
O=$U/sa/dem_unloading_kit_reverify_20261014
rm -rf "$R" "$O"
mkdir -p "$R/source" "$R/evidence" "$R/submitted" "$O/source"
cp "$WT/docs/reviews/codex_dem_unloading_kit_fix_recheck_evidence_20261015/source_manifest.json" "$R/"
cp "$WT/docs/reviews/codex_dem_unloading_kit_reverify_evidence_20261014/source_manifest.json" "$O/"
mkdir -p "$R/probes"
cp "$WT/docs/reviews/codex_dem_unloading_kit_fix_recheck_evidence_20261015/probes/source_audit.py" "$R/probes/"
# 핀에 있는 경로만 (없는 경로는 목록에 남긴다)
: > "$U/sa/missing_at_commit.txt"
while read -r p; do
  if git -C "$WT" cat-file -e "$C:$p" 2>/dev/null; then echo "$p"; else echo "$p" >> "$U/sa/missing_at_commit.txt"; fi
done < "$U/sa/cur_paths.txt" > "$U/sa/cur_present.txt"
git -C "$WT" archive "$C" $(cat "$U/sa/cur_present.txt") | tar -x -C "$R/source"
git -C "$WT" archive a30fe150e $(cat "$U/sa/old_paths.txt") | tar -x -C "$O/source"
# 10-14 재확인 fix 증거 폴더 (audit 의 linux_suites) — <commit> 의 것
git -C "$WT" archive "$C" docs/reviews/dem_unloading_kit_reverify_fix_evidence_20261014 | tar -x -C "$R/source"
git -C "$WT" show 799459c85:docs/reviews/codex_dem_unloading_kit_reverify_fix_recheck_request_20261014.md > "$R/submitted/request.md"
echo "R=$R"; echo "missing at $C: $(wc -l < "$U/sa/missing_at_commit.txt")"
ls "$R" "$O"
