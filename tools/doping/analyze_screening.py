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


def _dopant_atom_count(record: dict) -> int:
    """How many atoms of the dopant compound were introduced into the cell.

    Sums all 'n' fields across the placement steps (cation + anion in Type A,
    halide swaps in Type B). Used by ranking objectives that normalize by
    the number of foreign atoms added rather than total cell atoms.
    """
    n_dopant = 0
    for step in record.get('steps', []):
        for placement in step.get('placements', []):
            n_dopant += placement.get('n', 0)
        n_dopant += step.get('n_swap', 0)
    return max(1, n_dopant)  # floor 1 to avoid /0


def compute_score(records: list[dict],
                  objective: str = 'composite',
                  w_e: float = 0.4, w_v: float = 0.3,
                  w_s: float = 0.2, w_c: float = 0.1,
                  converged_penalty: float = 0.10,
                  precursor_mu: dict | None = None) -> list[dict]:
    """Annotate ``records`` with composite_score under the chosen objective.

    Objectives:
      'composite'    — weighted min-max heuristic (current default; arbitrary
                       but useful for first-pass ranking).
      'binding_E'    — sort by ΔE/atom directly. Sundar 2025-style "lower
                       binding energy = more stable doped phase". No
                       normalization, returns the raw absolute value as a
                       positive score (so higher = more negative ΔE).
      'binding_per_dopant' — ΔE × n_atoms / n_dopant_atoms. Removes the
                       systematic bias against high-vacancy compounds. Useful
                       for cross-compound comparison (Y₂O₃ vs Li₂O have
                       different dopant counts per cell).
      'formation_E'  — E_doped − E_LPSCl − Σ Δn_i × μ_i  where Δn_i is the
                       net atom count change for element i and μ_i is the
                       precursor chemical potential (precursor_mu dict; if
                       missing, falls back to ΔE/atom and warns).
      'disorder_sensitivity' — within-ensemble σ ΔE/atom (groups records by
                       (dopant, site, anion_site_label)). Per-record score
                       = group σ. High σ → Pustorino-style ordering
                       sensitivity, may correlate with disorder-enabled
                       conductivity but not stability.
    """
    if not records:
        return records
    if objective != 'composite':
        # Apply soft convergence penalty universally
        for r in records:
            r.setdefault('_score_components', {})

    if objective == 'binding_E':
        for r in records:
            de = r['uma_relaxed']['de_per_atom_vs_baseline']
            score = -de
            if not r.get('converged'):
                score -= converged_penalty
            r['composite_score'] = score
        print(f"  Score: binding_E (raw -ΔE/atom)")
        return records

    if objective == 'binding_per_dopant':
        for r in records:
            de = r['uma_relaxed']['de_per_atom_vs_baseline']
            n_at = r['uma_relaxed']['n_atoms']
            n_dop = _dopant_atom_count(r)
            score = -de * n_at / n_dop
            if not r.get('converged'):
                score -= converged_penalty
            r['composite_score'] = score
        print(f"  Score: binding_per_dopant (-ΔE × n_at / n_dopant_atoms)")
        return records

    if objective == 'formation_E':
        if precursor_mu is None:
            print("  ⚠ --objective formation_E without --precursor_mu, "
                  "falling back to binding_E.")
            return compute_score(records, 'binding_E', converged_penalty=converged_penalty)
        base_E = records[0].get('baseline_e_per_atom', 0)
        for r in records:
            E = r['uma_relaxed']['e_total']
            comp = r['uma_relaxed']['composition']
            base_n = sum(comp.values())  # rough — assumes Li6PS5Cl scale
            f = E - base_E * base_n
            for el, n in comp.items():
                f -= n * precursor_mu.get(el, 0)
            score = -f / base_n
            if not r.get('converged'):
                score -= converged_penalty
            r['composite_score'] = score
        print(f"  Score: formation_E (eV/atom)")
        return records

    if objective == 'disorder_sensitivity':
        from collections import defaultdict
        import statistics
        groups = defaultdict(list)
        for r in records:
            key = (r.get('dopant'), r.get('site'), r.get('anion_site_label'))
            groups[key].append(r)
        for key, rs in groups.items():
            if len(rs) > 1:
                des = [r['uma_relaxed']['de_per_atom_vs_baseline'] for r in rs]
                sigma = statistics.stdev(des)
            else:
                sigma = 0.0
            for r in rs:
                r['composite_score'] = sigma  # higher = more disorder
        print(f"  Score: disorder_sensitivity (σ ΔE within ensemble)")
        return records

    # Default — composite heuristic (kept for backward compat)
    return compute_composite_score(records, w_e, w_v, w_s, w_c,
                                  converged_penalty)


def compute_composite_score(records: list[dict],
                           w_e: float = 0.4, w_v: float = 0.3,
                           w_s: float = 0.2, w_c: float = 0.1,
                           converged_penalty: float = 0.10) -> list[dict]:
    """Composite score per record. Higher = better.

    Non-converged records are kept and ranked (a soft penalty is subtracted
    from the final score, default 0.10 ≈ ten percent of the normalized
    range). Compound-substitution structures often need >300 FIRE steps
    because foreign atoms and multiple Li vacancies create large initial
    strain; dropping them entirely loses real chemistry, while ignoring the
    convergence flag would over-credit them.
    """
    if not records:
        return records

    de = [r['uma_relaxed']['de_per_atom_vs_baseline'] for r in records]
    dv = [abs(r['dV_over_V0']) for r in records]
    sp = [r.get('compatibility_score', 0.0) for r in records]
    cp = [1.0 if str(r.get('charge_compensation', '')).startswith('imbalanced')
          else 0.0 for r in records]

    n_de = normalize(de, invert=True)   # lower energy → higher score
    n_dv = normalize(dv, invert=True)   # smaller |ΔV| → higher score
    n_sp = normalize(sp, invert=False)  # higher compatibility → higher score
    n_cp = normalize(cp, invert=True)   # lower penalty → higher score

    n_conv = sum(1 for r in records if r.get('converged'))
    print(f"  Score: converged {n_conv}/{len(records)}, "
          f"non-converged penalty = {converged_penalty:.2f}")

    for r, ne, nv, ns, nc in zip(records, n_de, n_dv, n_sp, n_cp):
        r['_score_components'] = {
            'energy': ne, 'volume': nv,
            'site_pref': ns, 'charge_comp': nc,
        }
        score = w_e * ne + w_v * nv + w_s * ns + w_c * nc
        if not r.get('converged', False):
            score -= converged_penalty
        r['composite_score'] = score
    return records


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
    parser.add_argument('--objective', default='composite',
                       choices=['composite', 'binding_E', 'formation_E',
                                'binding_per_dopant', 'disorder_sensitivity'],
                       help='Ranking metric (default composite — heuristic; '
                            'binding_E = raw ΔE/atom; '
                            'formation_E = E_doped − n_LPSCl×μ_LPSCl − Σ n_i × μ_i '
                            '(needs --precursor_mu JSON); '
                            'binding_per_dopant = ΔE normalized by number of '
                            'dopant atoms introduced (penalty-free per-atom); '
                            'disorder_sensitivity = σ ΔE across ensemble '
                            'seeds, higher = more Li-ordering sensitive '
                            '(Pustorino-style metric).')
    parser.add_argument('--precursor_mu',
                       help='JSON {element_or_compound: chemical_potential_eV} '
                            'for --objective formation_E. Without it falls '
                            'back to ΔE/atom of dopant-containing cell.')
    parser.add_argument('--max_dv', type=float, default=0.10,
                       help='Filter: max |ΔV/V0| (default 10%%). Compound '
                            'substitution often needs 0.20 because foreign '
                            'large cations + multiple Li vacancies expand the '
                            'lattice by 10-17%% (BaO, SrO, ZnO, Nd2O3, Y2O3).')
    parser.add_argument('--converged_penalty', type=float, default=0.10,
                       help='Composite-score penalty for non-converged FIRE '
                            'relaxations (default 0.10). Set 0 to ignore the '
                            'flag; set higher to be stricter.')
    parser.add_argument('--max_de', type=float, default=None,
                       help='Filter: max ΔE/atom vs baseline (eV)')
    parser.add_argument('--min_li_per_fu', type=float, default=4.0,
                       help='Filter: minimum Li atoms per formula unit '
                            '(default 4.0 = Li4PS5Cl floor; Sundar/Kraft '
                            'literature working range is Li5.4-6.0). Set to '
                            '0 to disable.')
    parser.add_argument('--n_fu', type=int, default=4,
                       help='Formula units per cell (default 4 for Li6PS5Cl '
                            'conventional cell)')
    parser.add_argument('--dedupe', action='store_true', default=True,
                       help='Drop duplicate records with identical composition '
                            'and ΔE within 1 meV/atom (default on)')
    args = parser.parse_args()

    data = json.loads(Path(args.results).read_text())
    records = data.get('results', [])
    print(f"Loaded {len(records)} records from {args.results}")

    # Filter pre-screen
    pre = records
    n_before = len(pre)
    if args.max_dv is not None:
        pre = [r for r in pre if abs(r.get('dV_over_V0', 1e9)) <= args.max_dv]
    if args.max_de is not None:
        pre = [r for r in pre
               if r['uma_relaxed']['de_per_atom_vs_baseline'] <= args.max_de]
    if args.min_li_per_fu > 0:
        before_li = len(pre)
        pre = [r for r in pre
               if r['uma_relaxed']['composition'].get('Li', 0) / args.n_fu
                  >= args.min_li_per_fu]
        print(f"  Li-retention filter (≥{args.min_li_per_fu} Li/f.u.): "
              f"{before_li} → {len(pre)} records")
    if args.dedupe:
        before_dd = len(pre)
        seen: set[tuple] = set()
        dedup = []
        for r in pre:
            comp = tuple(sorted(r['uma_relaxed']['composition'].items()))
            de = round(r['uma_relaxed']['de_per_atom_vs_baseline'] * 1000)
            key = (comp, de)
            if key not in seen:
                seen.add(key)
                dedup.append(r)
        pre = dedup
        print(f"  Dedup (composition + ΔE/atom 1 meV bucket): "
              f"{before_dd} → {len(pre)} records")
    print(f"  Total after all filters: {len(pre)}/{n_before}")

    precursor_mu = None
    if args.precursor_mu:
        precursor_mu = json.loads(Path(args.precursor_mu).read_text())
    scored = compute_score(pre, args.objective,
                          args.w_e, args.w_v, args.w_s, args.w_c,
                          args.converged_penalty, precursor_mu)
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
