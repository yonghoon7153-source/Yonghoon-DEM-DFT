"""anneal_champion.py — pick overall champion from all 25 (rank, li) anneal results.
Reads rank{R}_li{L}_anneal.json files, finds MIN E_after, writes champion summary.

Usage: python anneal_champion.py [comp_name]
Output: anneal_champion.json + anneal_champion.xyz
"""
import sys, json, glob, shutil
from pathlib import Path

COMP = sys.argv[1] if len(sys.argv) > 1 else 'comp'

files = sorted(glob.glob('rank*_li*_anneal.json'))
if not files:
    print("No anneal results found."); sys.exit(1)

results = []
for f in files:
    d = json.load(open(f))
    results.append(d)

results.sort(key=lambda r: r['E_after'])

print(f"{'rank-li':<10} {'E_after':>12} {'E_post_quench':>14} {'E_pre_quench':>13}")
for r in results:
    print(f"  {r['rank']}-{r['li']:<5} {r['E_after']:>+12.4f} "
          f"{r['E_post_quench']:>+14.4f} {r['E_pre_quench']:>+13.4f}")

champ = results[0]
print(f"\n★ CHAMPION: rank{champ['rank']} li{champ['li']}  "
      f"E_after = {champ['E_after']:.4f}")

# Copy xyz to champion
src_xyz = Path(f"rank{champ['rank']}_li{champ['li']}_anneal.xyz")
dst_xyz = Path('anneal_champion.xyz')
if src_xyz.exists():
    shutil.copy(src_xyz, dst_xyz)
    print(f"saved {dst_xyz}")

# Save summary
champ['all_results'] = results
json.dump(champ, open('anneal_champion.json', 'w'), indent=2)
print(f"saved anneal_champion.json")
