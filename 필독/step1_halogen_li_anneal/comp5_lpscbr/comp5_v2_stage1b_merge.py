"""comp3 v2 — Stage 1b merge: combine 3 chunk caches, sort by E, save cache_stage1b.json.
Trivial (~1 sec). Required by stage2.py and anneal_rank.py."""
import sys, json
from pathlib import Path
from comp5_v2_lib import jx, COMP_NAME

OUT = Path('cache_stage1b.json')
if OUT.exists():
    print(f"[{COMP_NAME}] {OUT} exists — exit 0."); sys.exit(0)

chunks = []
for ci in range(3):
    p = Path(f'cache_stage1b_c{ci}.json')
    if not p.exists():
        print(f"ERROR: {p} not found. Run stage1b chunk {ci} first."); sys.exit(2)
    chunks.append(json.load(open(p)))

merged = [r for c in chunks for r in c]
merged.sort(key=lambda r: r['E'])
json.dump(merged, open(OUT, 'w'), default=jx)
print(f"[{COMP_NAME}] merged {sum(len(c) for c in chunks)} entries → {OUT}")
print(f"[{COMP_NAME}] Top 5 halogen:")
for i, r in enumerate(merged[:5]):
    print(f"  rank{i}: S{r['s_rank']}={r['s_idx']} Cl={r['cl']} Br={r['br']} E={r['E']:.4f}")
