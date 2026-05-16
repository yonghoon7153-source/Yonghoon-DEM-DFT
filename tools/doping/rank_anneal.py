#!/usr/bin/env python
"""rank_anneal.py — Compare pre-anneal vs post-anneal rankings.

After ``run_anneal.py`` finishes, this script reads both the original UMA
screening JSON and the new anneal_results.json, joins them per structure
name, and reports candidates whose ranking changed (Pipeline Step 3 doc
notes Li6PS5Cl had a 4th→1st flip after anneal).

Usage:
  python3 tools/doping/rank_anneal.py \\
      --screening runs/.../uma_results.json \\
      --anneal    runs/.../anneal_results.json \\
      --out       runs/.../post_anneal_ranking.json \\
      --top 20
"""
import argparse
import json
from pathlib import Path
import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--screening', required=True,
                       help='Pre-anneal UMA screening JSON (run_uma_screening output)')
    parser.add_argument('--anneal', required=True,
                       help='Anneal results JSON (run_anneal output)')
    parser.add_argument('--out', required=True,
                       help='Output ranking JSON')
    parser.add_argument('--top', type=int, default=20)
    args = parser.parse_args()

    screen = json.loads(Path(args.screening).read_text())['results']
    anneal = json.loads(Path(args.anneal).read_text())['results']

    pre_by_name = {r['name']: r for r in screen if 'name' in r}
    post_by_name = {r['name']: r for r in anneal if 'name' in r and 'E_post_relax' in r}

    joined = []
    for name in sorted(set(pre_by_name) & set(post_by_name)):
        pre = pre_by_name[name]
        post = post_by_name[name]
        n_at = post['n_atoms']
        e_pre = post['E_pre_anneal'] / n_at
        e_post = post['E_post_relax'] / n_at
        de_anneal = (e_post - e_pre) * 1000  # meV/atom
        # Pre-anneal binding (from screening)
        de_screen = pre['uma_relaxed']['de_per_atom_vs_baseline']
        # Post-anneal binding (recompute against baseline)
        baseline_E_per_atom = pre['baseline_e_per_atom']
        de_screen_post = e_post - baseline_E_per_atom
        joined.append({
            'name': name,
            'dopant': pre.get('dopant', 'unknown'),
            'site': pre.get('site', '?'),
            'anion_site_label': pre.get('anion_site_label', '?'),
            'de_pre_anneal': de_screen,
            'de_post_anneal': de_screen_post,
            'delta_E_anneal_meV_per_atom': de_anneal,
            'volume_pre': post['volume_pre'],
            'volume_post': post['volume_post'],
            'dV_anneal_pct': (post['volume_post'] - post['volume_pre'])
                            / post['volume_pre'] * 100,
            'converged_post_anneal': post.get('converged', False),
        })

    # Rank by post-anneal ΔE
    ranked = sorted(joined, key=lambda r: r['de_post_anneal'])

    print(f"\n{'Rank':<5}{'Dopant':<22}{'sites':<24}"
          f"{'ΔE_pre':>10}{'ΔE_post':>10}{'ΔE_anneal':>12}"
          f"{'ΔV/V0':>9}")
    print('-' * 100)
    for i, r in enumerate(ranked[:args.top], 1):
        site_tag = f"{r['site'][:8]}+{r['anion_site_label'][:8]}"
        print(f"{i:<5}{r['dopant'][:22]:<22}{site_tag:<24}"
              f"{r['de_pre_anneal']:>+8.4f} "
              f"{r['de_post_anneal']:>+8.4f} "
              f"{r['delta_E_anneal_meV_per_atom']:>+8.1f} mV/at"
              f"{r['dV_anneal_pct']:>+8.2f}%")

    # Ranking flips
    print(f"\n=== Ranking shifts (pre-anneal rank → post-anneal rank) ===")
    pre_ranked = sorted(joined, key=lambda r: r['de_pre_anneal'])
    pre_rank = {r['name']: i for i, r in enumerate(pre_ranked, 1)}
    post_rank = {r['name']: i for i, r in enumerate(ranked, 1)}
    shifts = [(name, pre_rank[name], post_rank[name],
              post_rank[name] - pre_rank[name])
             for name in pre_rank if abs(pre_rank[name] - post_rank[name]) >= 3]
    for name, pre_r, post_r, delta in sorted(shifts, key=lambda x: abs(x[3]),
                                            reverse=True)[:15]:
        sign = '↑' if delta < 0 else '↓'
        print(f"  {name[:50]:<50}{sign} {pre_r:>3} → {post_r:>3}  (Δ{delta:+d})")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        'n_joined': len(joined),
        'ranked_by_post_anneal': ranked,
        'ranking_shifts': shifts,
    }, indent=2, default=str))
    print(f"\n✓ {len(joined)} structures joined → {out}")


if __name__ == '__main__':
    main()
