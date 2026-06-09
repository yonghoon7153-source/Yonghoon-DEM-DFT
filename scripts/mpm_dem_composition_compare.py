#!/usr/bin/env python3
"""Overlay champion MPM porosity-vs-AM (mpm2d_composition.py sweep) on the DEM
corpus — the DEM↔MPM behaviour cross-check (frame [4]).

Champion sweep numbers are baked in from a run of scripts/mpm2d_composition.py
(n_grid=128, plastic SE = LPSCl-like, rigid SE = DEM-overlap-like).  DEM
porosity-vs-AM is read live from docs/case_summary.csv (weight fraction from
phi_am/phi_se via ρ_AM=4.8, ρ_SE=2.0).

Run:  python3 scripts/mpm_dem_composition_compare.py
Out:  docs/figures/mpm_dem_composition_compare.png
"""
import csv
import os

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
SUMMARY = os.path.join(HERE, '..', 'docs', 'case_summary.csv')
OUT = os.path.join(HERE, '..', 'docs', 'figures', 'mpm_dem_composition_compare.png')
RHO_AM, RHO_SE = 4.8, 2.0

# champion MPM sweep (scripts/mpm2d_composition.py, AM wt% : ε_plastic, ε_rigid)
CHAMP_AM = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
CHAMP_PLASTIC = [6.5, 7.2, 8.2, 8.9, 10.0, 11.2, 11.4, 13.5, 16.4, 20.2, 28.2]
CHAMP_RIGID = [8.1, 9.1, 11.5, 12.7, 15.4, 17.0, 17.5, 18.4, 21.2, 24.0, 28.7]


def dem_points():
    pts = []
    with open(SUMMARY) as fh:
        for r in csv.DictReader(fh):
            try:
                pa = float(r['fm__phi_am']); ps = float(r['fm__phi_se'])
                po = float(r['fm__porosity'])
            except (KeyError, ValueError):
                continue
            if pa + ps <= 0:
                continue
            wam = pa * RHO_AM; wse = ps * RHO_SE
            pts.append((100.0 * wam / (wam + wse), po))
    return np.array(pts)


def main():
    dem = dem_points()
    # DEM binned median
    bins = {}
    for amwt, po in dem:
        b = int(round(amwt / 5) * 5); bins.setdefault(b, []).append(po)
    bx = sorted(bins); bmed = [float(np.median(bins[b])) for b in bx]

    fig, ax = plt.subplots(figsize=(8.4, 5.6))
    ax.plot(CHAMP_AM, CHAMP_PLASTIC, '-o', color='#2e8b57', lw=2.2, ms=6,
            label='champion MPM — SE PLASTIC (LPSCl-like)')
    ax.plot(CHAMP_AM, CHAMP_RIGID, '-s', color='#c0392b', lw=2.0, ms=6, alpha=0.85,
            label='champion MPM — SE RIGID (DEM-overlap-like)')
    ax.scatter(dem[:, 0], dem[:, 1], s=16, c='#2453b8', alpha=0.45,
               label=f'DEM cases (n={len(dem)})')
    ax.plot(bx, bmed, '-D', color='#10246b', lw=2.4, ms=7, label='DEM binned median')
    ax.axvspan(70, 90, color='#ffe9a8', alpha=0.35, zorder=0,
               label='production regime (AM-rich): DEM ≈ MPM-plastic')
    ax.set_xlabel('AM weight fraction (%)')
    ax.set_ylabel('porosity ε at common pressure (%)')
    ax.set_title('DEM ↔ champion MPM porosity-vs-composition cross-check\n'
                 'AM-rich: DEM tracks plastic MPM (cross-validated) · '
                 'SE-rich: DEM jumps toward rigid (model-dependent regime)',
                 fontsize=10)
    ax.set_xlim(-3, 103); ax.grid(alpha=0.3); ax.legend(fontsize=8, loc='upper left')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    plt.tight_layout(); plt.savefig(OUT, dpi=140)
    print(f"saved {OUT}")
    # text verdict
    print("\n  AM%   DEM_med   MPM_plastic   MPM_rigid")
    for b, m in zip(bx, bmed):
        pp = float(np.interp(b, CHAMP_AM, CHAMP_PLASTIC))
        pr = float(np.interp(b, CHAMP_AM, CHAMP_RIGID))
        tag = '  DEM≈plastic' if abs(m - pp) < abs(m - pr) else '  DEM≈rigid'
        print(f"  {b:3d}   {m:6.1f}     {pp:6.1f}      {pr:6.1f}{tag}")


if __name__ == '__main__':
    main()
