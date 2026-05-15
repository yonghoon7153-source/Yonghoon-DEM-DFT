#!/usr/bin/env python
"""analyze_screening.py — Rank UMA screening results, produce Top-N report.

Reads uma_screening_results.json from run_uma_screening.py and produces a
ranked Top-N report of doped LPSCl candidates by composite score.

Scoring components (weights configurable):
  - Energy (lower is better, normalized): w_E
  - Volume change |ΔV/V0| (smaller is better): w_V
  - Site preference compatibility_score: w_S
  - Charge compensation penalty (imbalanced > 0): w_C

Usage:
  python3 analyze_screening.py \\
      --results data/doping_screening/uma_screening_results.json \\
      --top 20 \\
      --out data/doping_screening/top_candidates.json

  # Custom weights
  python3 analyze_screening.py --results ... --out ... \\
      --w_e 0.4 --w_v 0.3 --w_s 0.2 --w_c 0.1
"""
import argparse
import json
from pathlib import Path
import numpy as np


def normalize(values: list[float], invert: bool = False) -> list[float]:
    """Min-max normalize to [0, 1]. invert=True flips (lower=better)."""
    arr = np.array(values, dtype=float)
    lo, hi = arr.min(), arr.max()
    if hi - lo < 1e-12:
        return [0.5] * len(values)
    norm = (arr - lo) / (hi - lo)
    return (1.0 - norm if invert else norm).tolist()


def compute_composite_score(records: list[dict],
                           w_e: float = 0.4, w_v: float = 0.3,
                           w_s: float = 0.2, w_c: float = 0.1) -> list[dict]:
    """Composite score per record. Higher = better."""
    if not records:
        return records
    converged = [r for r in records if r.get('converged', False)]
    if not converged:
        print("⚠ No converged structures. Using all.")
        converged = records

    de = [r['uma_relaxed']['de_per_atom_vs_baseline'] for r in converged]
    dv = [abs(r['dV_over_V0']) for r in converged]
    sp = [r.get('compatibility_score', 0.0) for r in converged]
    cp = [1.0 if str(r.get('charge_compensation', '')).startswith('imbalanced')
          else 0.0 for r in converged]

    n_de = normalize(de, invert=True)   # lower energy → higher score
    n_dv = normalize(dv, invert=True)   # smaller |ΔV| → higher score
    n_sp = normalize(sp, invert=False)  # higher compatibility → higher score
    n_cp = normalize(cp, invert=True)   # lower penalty → higher score

    for r, ne, nv, ns, nc in zip(converged, n_de, n_dv, n_sp, n_cp):
        r['_score_components'] = {
            'energy': ne, 'volume': nv,
            'site_pref': ns, 'charge_comp': nc,
        }
        r['composite_score'] = (
            w_e * ne + w_v * nv + w_s * ns + w_c * nc
        )
    return converged


def print_top_table(ranked: list[dict], n: int = 20):
    """Print human-readable Top-N table."""
    print(f"\n{'='*100}")
    print(f"{'Rank':<5}{'Dopant':<8}{'Site':<10}{'x':<8}"
          f"{'ΔE/atom':<12}{'ΔV/V0':<10}{'CompScore':<12}{'Charge_comp':<20}")
    print('-' * 100)
    for i, r in enumerate(ranked[:n], 1):
        print(f"{i:<5}{r['dopant']:<8}{r['site']:<10}"
              f"{r['concentration']*100:>5.1f}% "
              f"{r['uma_relaxed']['de_per_atom_vs_baseline']:>+8.4f} eV  "
              f"{r['dV_over_V0']*100:>+6.2f}%  "
              f"{r['composite_score']:>8.4f}    "
              f"{r['charge_compensation']:<20}")
    print('=' * 100)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--results', required=True,
                       help='uma_screening_results.json')
    parser.add_argument('--out', required=True,
                       help='Top-N output JSON')
    parser.add_argument('--top', type=int, default=20,
                       help='Number of top candidates to report')
    parser.add_argument('--w_e', type=float, default=0.4,
                       help='Weight: energy')
    parser.add_argument('--w_v', type=float, default=0.3,
                       help='Weight: volume change')
    parser.add_argument('--w_s', type=float, default=0.2,
                       help='Weight: site preference')
    parser.add_argument('--w_c', type=float, default=0.1,
                       help='Weight: charge compensation penalty')
    parser.add_argument('--max_dv', type=float, default=0.10,
                       help='Filter: max |ΔV/V0| (default 10%%)')
    parser.add_argument('--max_de', type=float, default=None,
                       help='Filter: max ΔE/atom vs baseline (eV)')
    args = parser.parse_args()

    data = json.loads(Path(args.results).read_text())
    records = data.get('results', [])
    print(f"Loaded {len(records)} records from {args.results}")

    # Filter pre-screen
    pre = records
    if args.max_dv is not None:
        pre = [r for r in pre if abs(r.get('dV_over_V0', 1e9)) <= args.max_dv]
    if args.max_de is not None:
        pre = [r for r in pre
               if r['uma_relaxed']['de_per_atom_vs_baseline'] <= args.max_de]
    print(f"After filter (|ΔV/V0|≤{args.max_dv}, "
          f"ΔE≤{args.max_de}): {len(pre)} records")

    scored = compute_composite_score(pre, args.w_e, args.w_v, args.w_s, args.w_c)
    ranked = sorted(scored, key=lambda r: r['composite_score'], reverse=True)

    print_top_table(ranked, args.top)

    # Per-dopant best (across the full ranked list, so all dopants get a row)
    by_dopant = {}
    for r in ranked:
        d = r['dopant']
        if d not in by_dopant:
            by_dopant[d] = r

    # Unique dopants WITHIN top-N (the previous wording conflated this with
    # the per-dopant-best count over the full ranked list).
    top_slice = ranked[:args.top]
    unique_in_top = {r['dopant'] for r in top_slice}
    print(f"\nUnique dopants in Top-{args.top}: {len(unique_in_top)} "
          f"({', '.join(sorted(unique_in_top))})")
    print(f"Unique dopants across all {len(ranked)} ranked records: "
          f"{len(by_dopant)}")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({
        'baseline': data.get('baseline'),
        'weights': {'energy': args.w_e, 'volume': args.w_v,
                    'site_pref': args.w_s, 'charge_comp': args.w_c},
        'filters': {'max_dv': args.max_dv, 'max_de': args.max_de},
        'n_total': len(records),
        'n_after_filter': len(pre),
        'top_n': args.top,
        'top_candidates': ranked[:args.top],
        'best_per_dopant': list(by_dopant.values()),
    }, indent=2, default=str))
    print(f"\n✓ Top-{args.top}: {out_path}")


if __name__ == '__main__':
    main()
