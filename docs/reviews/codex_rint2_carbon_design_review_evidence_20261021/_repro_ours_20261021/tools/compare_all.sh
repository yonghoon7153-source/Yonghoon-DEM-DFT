#!/bin/bash
# Re-run all Codex-vs-ours JSON comparisons; print stats and up to 12 non-path rows per pair.
S=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad
X=$S/import_rint2rev/x; W=$S/rint2rev_repro; R=$W/_repro_ours_20261021; T=$S/rint2rev_tools
mkdir -p "$R/compare"
pair() {  # label codex ours [extra args]
  local lab=$1 a=$2 b=$3; shift 3
  if [ ! -f "$b" ]; then echo "$lab: OURS MISSING ($b)"; return; fi
  python3 -I -X utf8 -B "$T/compare_json.py" "$a" "$b" "$R/compare/$lab.cmp.json" --label "$lab" "$@" > "$R/compare/$lab.cmp.txt" 2>&1
  head -1 "$R/compare/$lab.cmp.txt"
  python3 -I -X utf8 -B -c "
import json,sys
d=json.load(open(sys.argv[1],encoding='utf-8'))
rows=[r for r in d['rows'] if r['class']!='path']
for r in rows[:12]: print('    ',json.dumps(r,ensure_ascii=False)[:420])
if len(rows)>12: print('     ... +%d more non-path rows'%(len(rows)-12))
" "$R/compare/$lab.cmp.json"
}
pair geometry_probe_results   "$X/geometry/geometry_probe_results.json"            "$R/geometry_probe_results.json"
pair registration_probe_results "$X/registration/registration_probe_results.json"  "$R/registration_probe_results.json"
pair convergence_probe_results "$X/geometry/convergence_probe_results.json"        "$R/convergence_probe_results.json"
pair search_cg_connected_results "$X/geometry/search_cg_connected_results.json"    "$R/search_cg_connected_results.json" --ignore-key phi
for f in independent_join_checks known_limit_and_mutant structure_results structure_fixture_manifest numeric_current numeric_overflow_replay_current; do
  pair "$f" "$X/part_b/evidence/$f.json" "$W/part_b/evidence/$f.json"
done
pair structure_minimal_replay "$X/part_b/evidence/probe_rint2_carbon_design_review_20261021_structure_minimal_replay.py.json" "$W/part_b/evidence/probe_rint2rev_repro_structure_minimal_replay.py.json" --ignore-key seconds --ignore-key command --ignore-key log_sha256 --ignore-key source --ignore-key test_source --ignore-key log
