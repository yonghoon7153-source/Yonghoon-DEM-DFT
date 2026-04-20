"""
Defense (b): Dijkstra vs Laplace tortuosity comparison.

From each case's full_metrics.json we extract three quantities:
  * tortuosity_mean     → Dijkstra geometric τ (geodesic shortest-path)
  * sigma_bulk_net      → CONTACT_FREE (bulk-only) σ/σ_grain — gives τ_Laplace_geom
  * sigma_full          → FULL (bulk+constriction)  σ/σ_grain — gives τ_Laplace_eff
  * phi_se              → SE volume fraction

Relation: σ_ratio = ε_SE / τ² (Bruggeman-like, ε = φ_SE for SE-network)
  → τ²  = ε_SE / σ_ratio
  → τ   = √(ε_SE / σ_ratio)

Three τ's per case:
  τ_Dijkstra       = tortuosity_mean
  τ_Laplace_geom   = √(φ_se / sigma_bulk_net)    ← Laplace, pure bulk, NO constriction
  τ_Laplace_eff    = √(φ_se / sigma_full)        ← Laplace, FULL = geom + constriction

Key ratios:
  R_Lg/D  = τ_Laplace_geom / τ_Dijkstra          ← narrative decider
                                                     2–3×  → current narrative OK
                                                     5–10× → narrative needs revision
                                                     ≲1.5× → Dijkstra ≈ Laplace, even better
  R_Le/Lg = τ_Laplace_eff  / τ_Laplace_geom      ← GB/constriction amplification
                                                   (should match our framework's GB contribution)
"""
from __future__ import annotations
import argparse
import glob
import json
import math
import os
import sys
from typing import Optional


def safe_sqrt(x: Optional[float]) -> Optional[float]:
    if x is None:
        return None
    try:
        v = float(x)
        return math.sqrt(v) if v > 0 else None
    except Exception:
        return None


def compute_tau(metrics: dict) -> dict:
    """Extract Dijkstra τ + derive two Laplace τ's from stored σ ratios."""
    phi = metrics.get('phi_se') or metrics.get('SE_vol_frac')
    sigma_full       = metrics.get('sigma_full')        # = σ_eff / σ_grain (full network)
    sigma_bulk_net   = metrics.get('sigma_bulk_net')    # = σ_eff / σ_grain (CONTACT_FREE)
    tau_dijkstra     = metrics.get('tortuosity_mean')
    tau_dij_median   = metrics.get('tortuosity_median')

    def tau_from_sigma(s):
        if s is None or phi is None:
            return None
        try:
            s = float(s); phi_v = float(phi)
            if s <= 0 or phi_v <= 0:
                return None
            return math.sqrt(phi_v / s)
        except Exception:
            return None

    tau_L_geom = tau_from_sigma(sigma_bulk_net)
    tau_L_eff  = tau_from_sigma(sigma_full)

    def div(a, b):
        try:
            return a / b if (a is not None and b is not None and b > 0) else None
        except Exception:
            return None

    return {
        'phi_se':          phi,
        'sigma_full':      sigma_full,
        'sigma_bulk_net':  sigma_bulk_net,
        'tau_dijkstra':    tau_dijkstra,
        'tau_dij_median':  tau_dij_median,
        'tau_Laplace_geom': tau_L_geom,
        'tau_Laplace_eff':  tau_L_eff,
        'ratio_Lg_over_D':  div(tau_L_geom, tau_dijkstra),
        'ratio_Le_over_Lg': div(tau_L_eff,  tau_L_geom),
        'ratio_Le_over_D':  div(tau_L_eff,  tau_dijkstra),
    }


def find_full_metrics(roots: list[str]) -> list[str]:
    paths = []
    for r in roots:
        if os.path.isfile(r) and r.endswith('full_metrics.json'):
            paths.append(r)
            continue
        for p in glob.glob(os.path.join(r, '**', 'full_metrics.json'), recursive=True):
            paths.append(p)
    return sorted(set(paths))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('roots', nargs='*',
                    default=['webapp/archive', 'webapp/results'],
                    help='Directories (or json files) to scan for full_metrics.json')
    ap.add_argument('--csv-out', default='/tmp/tau_compare.csv',
                    help='Write per-case CSV to this path')
    ap.add_argument('--min-phi', type=float, default=0.0,
                    help='Only include cases with phi_se ≥ this')
    ap.add_argument('--min-perc', type=float, default=50.0,
                    help='Only include cases with percolation_pct ≥ this '
                         '(default 50%%). Non-percolating cases produce garbage '
                         'τ_Dijkstra via fallback path; filter them out.')
    args = ap.parse_args()

    paths = find_full_metrics(args.roots)
    print(f"Found {len(paths)} full_metrics.json files", file=sys.stderr)

    rows = []
    excluded_perc = []
    for p in paths:
        try:
            with open(p) as f:
                m = json.load(f)
        except Exception as e:
            print(f"  SKIP {p}: {e}", file=sys.stderr)
            continue
        case = os.path.basename(os.path.dirname(p))
        t = compute_tau(m)
        t['case'] = case
        t['path'] = p
        t['percolation_pct'] = m.get('percolation_pct', 100.0)
        if t['phi_se'] is not None and t['phi_se'] < args.min_phi:
            continue
        # Percolation filter: non-percolating cases produce garbage τ_Dijkstra
        # via dem_analysis_core.py's fallback path (uses isolated component
        # lowest-z as source → partial paths → inflated τ).
        if t['percolation_pct'] is not None and t['percolation_pct'] < args.min_perc:
            excluded_perc.append((case, t['percolation_pct']))
            continue
        rows.append(t)

    if excluded_perc:
        print(f"\n[EXCLUDED] {len(excluded_perc)} cases with percolation < {args.min_perc}%:",
              file=sys.stderr)
        for c, pct in excluded_perc[:20]:
            print(f"  {c:35s}  perc = {pct:.1f}%", file=sys.stderr)
        if len(excluded_perc) > 20:
            print(f"  ... and {len(excluded_perc)-20} more", file=sys.stderr)

    # Filter cases where we can compute the key ratio
    good = [r for r in rows if r['ratio_Lg_over_D'] is not None]
    print(f"\n=== Laplace-vs-Dijkstra τ comparison: {len(good)}/{len(rows)} cases with complete data ===\n")

    # Column order for printing
    hdr = ('case', 'φ_SE', 'τ_Dij', 'τ_Lap_geom', 'τ_Lap_eff',
           'Lg/D', 'Le/Lg', 'Le/D')
    print(f"{hdr[0]:30s} {hdr[1]:>6s} {hdr[2]:>7s} {hdr[3]:>11s} {hdr[4]:>10s} "
          f"{hdr[5]:>6s} {hdr[6]:>6s} {hdr[7]:>6s}")
    print('-' * 92)

    def fmt(v, w, prec=2):
        if v is None:
            return f"{'—':>{w}s}"
        try:
            return f"{float(v):>{w}.{prec}f}"
        except Exception:
            return f"{'?':>{w}s}"

    for r in sorted(good, key=lambda x: x.get('phi_se') or 0):
        print(f"{r['case'][:30]:30s} "
              f"{fmt(r['phi_se'], 6, 3)} "
              f"{fmt(r['tau_dijkstra'], 7)} "
              f"{fmt(r['tau_Laplace_geom'], 11)} "
              f"{fmt(r['tau_Laplace_eff'], 10)} "
              f"{fmt(r['ratio_Lg_over_D'], 6)} "
              f"{fmt(r['ratio_Le_over_Lg'], 6)} "
              f"{fmt(r['ratio_Le_over_D'], 6)}")

    # Summary stats — the headline number
    ratios_Lg_D = [r['ratio_Lg_over_D'] for r in good if r['ratio_Lg_over_D']]
    ratios_Le_Lg = [r['ratio_Le_over_Lg'] for r in good if r['ratio_Le_over_Lg']]
    ratios_Le_D = [r['ratio_Le_over_D'] for r in good if r['ratio_Le_over_D']]

    def stats(vals):
        if not vals:
            return {'n': 0}
        import statistics as S
        return {
            'n': len(vals),
            'min': min(vals),
            'p25': S.quantiles(vals, n=4)[0] if len(vals) >= 4 else min(vals),
            'median': S.median(vals),
            'mean': S.mean(vals),
            'p75': S.quantiles(vals, n=4)[2] if len(vals) >= 4 else max(vals),
            'max': max(vals),
        }

    print('\n=== Summary ===')
    print('\nτ_Laplace_geom / τ_Dijkstra  (NARRATIVE DECIDER):')
    s = stats(ratios_Lg_D)
    if s['n']:
        print(f"  n={s['n']}  min={s['min']:.2f}  p25={s['p25']:.2f}  median={s['median']:.2f}  "
              f"mean={s['mean']:.2f}  p75={s['p75']:.2f}  max={s['max']:.2f}")
        m = s['median']
        if 0.7 <= m <= 1.3:
            verdict = (f"≈1× ({m:.2f}) : Dijkstra ≈ Laplace geometric τ. "
                       f"STRONGER than 'lower bound' — use as surrogate.")
        elif 1.3 < m <= 3.5:
            verdict = (f"{m:.2f}× : CURRENT NARRATIVE CONFIRMED "
                       f"(Dijkstra = lower bound, GB separate).")
        elif 3.5 < m <= 10:
            verdict = (f"{m:.2f}× : Narrative NEEDS REVISION "
                       f"(Dijkstra not a simple lower bound).")
        elif m < 0.7:
            verdict = (f"{m:.2f}× < 0.7 : Dijkstra OVER-estimates τ vs Laplace. "
                       f"Unusual — check sample size / sampling bias.")
        else:
            verdict = f"Ratio {m:.1f}× — unusual; investigate."
        print(f"  VERDICT: {verdict}")

    print('\nτ_Laplace_eff / τ_Laplace_geom  (GB/constriction amplification — series-limit check):')
    s = stats(ratios_Le_Lg)
    if s['n']:
        print(f"  n={s['n']}  median={s['median']:.2f}  mean={s['mean']:.2f}  max={s['max']:.2f}")
        print(f"  (Our framework predicts (1+R_GB/R_bulk)^½. If constriction 70–80%, "
              f"R_GB/R_bulk ≈ 3 → ratio ≈ 2.0. Compare with above.)")

    print('\nτ_Laplace_eff / τ_Dijkstra  (Minnmann-comparable τ_eff vs Dijkstra τ):')
    s = stats(ratios_Le_D)
    if s['n']:
        print(f"  n={s['n']}  median={s['median']:.2f}  mean={s['mean']:.2f}  max={s['max']:.2f}")

    # CSV dump
    if rows:
        import csv as _csv
        fieldnames = ['case', 'phi_se', 'sigma_full', 'sigma_bulk_net',
                      'tau_dijkstra', 'tau_dij_median',
                      'tau_Laplace_geom', 'tau_Laplace_eff',
                      'ratio_Lg_over_D', 'ratio_Le_over_Lg', 'ratio_Le_over_D',
                      'path']
        with open(args.csv_out, 'w', newline='') as f:
            w = _csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            w.writeheader()
            for r in rows:
                w.writerow(r)
        print(f"\nWrote {args.csv_out} ({len(rows)} rows)")


if __name__ == '__main__':
    main()
