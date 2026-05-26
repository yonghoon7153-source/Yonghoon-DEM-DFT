#!/usr/bin/env python
"""analyze_v0_ensemble.py — pick the EOS ensemble champion by BEST BM3 fit
quality (highest R^2, physical B0'), NOT lowest energy. Reports V0 + V0 cell.

Re-analyzes an existing uma_eos_results.json (no re-run):
  python3 analyze_v0_ensemble.py uma_eos_tight_both/uma_eos_results.json
"""
import argparse
import json
import numpy as np
from scipy.optimize import curve_fit


def bm(V, V0, B0, Bp, E0):
    e = (V0 / V) ** (2 / 3)
    return E0 + 9 * V0 * B0 / 16 * ((e - 1) ** 3 * Bp + (e - 1) ** 2 * (6 - 4 * e))


def fit_curve(curve):
    V = np.array([p['V'] for p in curve], float)
    E = np.array([p['E'] for p in curve], float)
    p, _ = curve_fit(bm, V, E, p0=[V[int(np.argmin(E))], 0.1, 4.0, E.min()], maxfev=200000)
    Ef = bm(V, *p)
    ssr = float(np.sum((E - Ef) ** 2))
    sst = float(np.sum((E - E.mean()) ** 2)) or 1e-30
    return {'V0': float(p[0]), 'B0': float(p[1] * 160.21766), 'Bp': float(p[2]),
            'E0': float(p[3]), 'R2': 1.0 - ssr / sst, 'rmse': float(np.sqrt(ssr / len(E)))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('json', help='uma_eos_results.json (has rank1_ensemble)')
    ap.add_argument('--bp_lo', type=float, default=2.0, help='min physical B0\'')
    ap.add_argument('--bp_hi', type=float, default=8.0, help='max physical B0\'')
    a = ap.parse_args()

    d = json.load(open(a.json))
    seeds = d.get('rank1_ensemble', d if isinstance(d, list) else [])
    rows = []
    for r in seeds:
        sc = r.get('eos_scan')
        if not sc:
            continue
        try:
            f = fit_curve(sc['curve'])
        except Exception:
            continue
        f.update(rank=r.get('rank', '?'), Vref=r['V_ref_relaxed'], cell=r['cell_relaxed'])
        rows.append(f)
    if not rows:
        print('no fittable seeds')
        return

    rows.sort(key=lambda x: -x['R2'])
    print(f"{len(rows)} seeds fit. Top 10 by R^2:")
    print(f"  {'rank':16s} {'R2':>10} {'rmse':>8} {'V0':>9} {'B0':>7} {'Bp':>7}")
    for x in rows[:10]:
        print(f"  {x['rank']:16s} {x['R2']:10.6f} {x['rmse']:8.4f} "
              f"{x['V0']:9.2f} {x['B0']:7.1f} {x['Bp']:7.2f}")

    good = [x for x in rows if a.bp_lo <= x['Bp'] <= a.bp_hi]
    champ = good[0] if good else rows[0]          # best R^2 with physical B0'
    sel = good if good else rows
    Vsel = np.array([x['V0'] for x in sel])
    B0sel = np.array([x['B0'] for x in sel])

    from ase.geometry import cell_to_cellpar
    scale = (champ['V0'] / champ['Vref']) ** (1 / 3)
    cp = cell_to_cellpar(np.array(champ['cell']) * scale)

    print(f"\n=== CHAMPION (best BM3 fit + physical B0') = {champ['rank']} ===")
    print(f"  V0 = {champ['V0']:.2f} Å³   B0 = {champ['B0']:.1f} GPa   "
          f"B0' = {champ['Bp']:.2f}   R2 = {champ['R2']:.6f}")
    print(f"  V0 cell: a={cp[0]:.4f}  b={cp[1]:.4f}  c={cp[2]:.4f} Å   "
          f"α={cp[3]:.2f} β={cp[4]:.2f} γ={cp[5]:.2f}°")
    print(f"\n=== GOOD-FIT ENSEMBLE ({a.bp_lo}<=B0'<={a.bp_hi}, n={len(good)}/{len(rows)}) ===")
    print(f"  V0 = {Vsel.mean():.2f} ± {Vsel.std():.2f} Å³  (median {np.median(Vsel):.2f})")
    print(f"  B0 = {B0sel.mean():.1f} ± {B0sel.std():.1f} GPa  (median {np.median(B0sel):.1f})")


if __name__ == '__main__':
    main()
