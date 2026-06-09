#!/usr/bin/env python3
"""Overlay champion MPM porosity-vs-AM (mpm2d_composition.py sweep) on the DEM
corpus — the DEM↔MPM behaviour cross-check (frame [4]).

Champion sweep numbers are baked in from a run of scripts/mpm2d_composition.py
(n_grid=128, plastic SE = LPSCl-like, rigid SE = DEM-overlap-like).  DEM
porosity-vs-AM (weight fraction from phi_am/phi_se via ρ_AM=4.8, ρ_SE=2.0) is
baked in too (85 cases from docs/case_summary.csv) so the script is
self-contained — runs anywhere with matplotlib, no data files needed.

Run:  python3 scripts/mpm_dem_composition_compare.py
Out:  docs/figures/mpm_dem_composition_compare.png
"""
import os

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'docs', 'figures', 'mpm_dem_composition_compare.png')

# champion MPM sweep (scripts/mpm2d_composition.py, AM wt% : ε_plastic, ε_rigid)
CHAMP_AM = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
CHAMP_PLASTIC = [6.5, 7.2, 8.2, 8.9, 10.0, 11.2, 11.4, 13.5, 16.4, 20.2, 28.2]
CHAMP_RIGID = [8.1, 9.1, 11.5, 12.7, 15.4, 17.0, 17.5, 18.4, 21.2, 24.0, 28.7]

# DEM corpus (AM wt%, porosity %) — 85 cases, baked from docs/case_summary.csv
DEM_PTS = [(62.0, 21.2), (62.1, 19.7), (62.2, 5.7), (62.2, 6.6), (62.4, 16.8),
           (72.1, 10.4), (72.1, 11.4), (72.1, 17.2), (72.3, 16.4), (75.3, 18.9),
           (75.4, 18.0), (75.5, 13.4), (75.6, 18.2), (75.7, 12.4), (76.1, 15.2),
           (76.5, 14.1), (76.7, 10.1), (76.8, 11.1), (80.0, 15.5), (80.0, 16.3),
           (80.0, 16.5), (80.0, 18.9), (80.1, 16.3), (80.1, 16.4), (80.2, 14.4),
           (80.3, 16.0), (80.3, 18.1), (80.4, 16.0), (80.4, 16.6), (80.4, 17.8),
           (80.5, 16.3), (80.5, 16.7), (81.6, 12.4), (81.6, 18.4), (81.6, 18.6),
           (81.6, 18.9), (81.6, 20.9), (81.7, 12.9), (81.7, 13.1), (81.7, 14.3),
           (81.7, 14.5), (81.7, 15.2), (81.7, 15.5), (81.7, 17.1), (81.7, 17.8),
           (81.7, 28.3), (81.8, 15.9), (81.8, 15.9), (81.8, 17.2), (81.8, 17.5),
           (81.9, 15.0), (82.0, 13.9), (82.0, 14.0), (82.0, 15.8), (82.0, 17.1),
           (82.0, 18.9), (82.0, 19.7), (82.0, 19.8), (82.0, 20.1), (82.0, 20.4),
           (82.1, 15.1), (82.1, 16.1), (82.1, 16.2), (82.1, 16.3), (82.1, 19.8),
           (82.2, 14.3), (85.0, 16.8), (85.0, 17.7), (85.0, 19.8), (85.0, 20.1),
           (85.0, 21.6), (85.0, 22.3), (85.0, 23.8), (85.1, 15.7), (85.1, 17.5),
           (85.1, 22.1), (85.2, 24.5), (85.6, 20.5), (85.7, 20.9), (85.7, 22.1),
           (86.7, 16.7), (86.7, 18.2), (86.7, 18.3), (86.7, 23.9), (86.8, 32.8)]


def main():
    dem = np.array(DEM_PTS)
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
