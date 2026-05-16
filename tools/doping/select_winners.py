#!/usr/bin/env python
"""select_winners.py — extract the per-group winner from UMA screening
results so we can put MLIP post-processing (anneal, EOS, elastic, MD)
on the most-stable structure of every (compound, cation_site, anion_site)
combination.

User feedback: "각 조합에서의 1등들은 다 후처리를 해보자". This script
implements that grouping. Output is a JSON manifest with one entry per
winner that downstream tools can read.

Usage:
  python3 tools/doping/select_winners.py \\
      --results runs/.../uma_results.json \\
      --out runs/.../winners.json \\
      --group_by dopant cation_site anion_site_label
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from _provenance import get_provenance


def main():
    p = argparse.ArgumentParser(description=__doc__,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--results', required=True,
                  help='uma_results.json from run_uma_screening.py')
    p.add_argument('--out', required=True, help='Output winners.json')
    p.add_argument('--group_by', nargs='+',
                  default=['dopant', 'site', 'anion_site_label'],
                  help='Grouping keys (default: dopant + cation site + anion site)')
    p.add_argument('--metric', default='de_per_atom_vs_baseline',
                  help='Within-group metric to minimize')
    p.add_argument('--max_dv', type=float, default=0.30,
                  help='Skip records with |ΔV/V0| > this (default 30%%)')
    p.add_argument('--require_converged', action='store_true',
                  help='Drop non-converged records before selecting winners')
    args = p.parse_args()

    data = json.loads(Path(args.results).read_text())
    records = data.get('results', [])

    # Filter
    pre = records
    if args.max_dv is not None:
        pre = [r for r in pre if abs(r.get('dV_over_V0', 1e9)) <= args.max_dv]
    if args.require_converged:
        pre = [r for r in pre if r.get('converged', False)]
    # Skip explicit outliers
    pre = [r for r in pre if not r['uma_relaxed'].get('outlier_flag', False)]
    print(f"Filtered: {len(records)} → {len(pre)} records")

    # Group + pick winner per group
    groups = defaultdict(list)
    for r in pre:
        key = tuple(r.get(k, 'unknown') for k in args.group_by)
        groups[key].append(r)

    winners = []
    for key, group in groups.items():
        winner = min(group,
                    key=lambda r: r['uma_relaxed'][args.metric])
        winners.append({
            **winner,
            'group_key': dict(zip(args.group_by, key)),
            'n_in_group': len(group),
            'group_metric_min': winner['uma_relaxed'][args.metric],
            'group_metric_max': max(r['uma_relaxed'][args.metric] for r in group),
            'group_metric_spread': max(r['uma_relaxed'][args.metric] for r in group)
                                   - winner['uma_relaxed'][args.metric],
        })

    # Sort winners by metric (global ranking)
    winners.sort(key=lambda w: w['uma_relaxed'][args.metric])

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        'provenance': get_provenance(),
        'source': str(args.results),
        'group_by': args.group_by,
        'n_groups': len(groups),
        'metric': args.metric,
        'winners': winners,
    }, indent=2, default=str))

    print(f"\n{'Rank':<5}{'Group':<60}{'ΔE/atom':>10}{'Spread':>10}")
    print('-' * 90)
    for i, w in enumerate(winners[:30], 1):
        grp = '/'.join(str(v) for v in w['group_key'].values())[:58]
        print(f"{i:<5}{grp:<60}"
              f"{w['uma_relaxed'][args.metric]:>+9.4f} "
              f"{w['group_metric_spread']:>+8.4f}")
    print(f"\n✓ {len(winners)} winners → {out}")


if __name__ == '__main__':
    main()
