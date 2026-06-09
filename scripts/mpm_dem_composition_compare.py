#!/usr/bin/env python3
"""DEM ↔ champion MPM porosity-vs-composition cross-check (frame [4]).

Two panels, self-contained (no data files needed):
  A) porosity vs AM weight %        — champion plastic/rigid lines + DEM cases
  B) porosity vs SE-fraction-of-SOLID — density-independent design axis, DEM
     points coloured by AM_P:AM_S split (monomodal AM_S → bimodal → AM_P).

Champion sweep: scripts/mpm2d_composition.py (P:S=7:3, fixed sizes), plastic
SE = LPSCl-like, rigid SE = DEM-overlap-like.  DEM: 132 webapp cases baked in
as (AM_P_vol%, AM_S_vol%, SE_vol%, porosity%) (vol = fraction of total cell, so
the four sum to ~100).

Verdict (both axes): DEM median tracks the PLASTIC MPM through the production
core (AM 70-85 % ≡ SE 30-50 % of solid) and only leans rigid at the extremes
(SE-rich / AM-rich).  Spread at fixed composition = size (Furnas) effect, which
the single-size champion slice does not span but the DEM corpus does.

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

# champion MPM sweep (scripts/mpm2d_composition.py): AM wt% -> ε_plastic, ε_rigid
CHAMP_AM = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
CHAMP_PLASTIC = [6.5, 7.2, 8.2, 8.9, 10.0, 11.2, 11.4, 13.5, 16.4, 20.2, 28.2]
CHAMP_RIGID = [8.1, 9.1, 11.5, 12.7, 15.4, 17.0, 17.5, 18.4, 21.2, 24.0, 28.7]

# DEM corpus: (AM_P_vol%, AM_S_vol%, SE_vol%, porosity%), 132 webapp cases
DEM = [(0.0,31.9,46.9,21.2),(0.0,32.6,47.7,19.7),(0.0,34.0,49.2,16.8),(0.0,37.9,55.4,6.6),(0.0,38.3,56.0,5.7),(0.0,42.9,39.9,17.2),(0.0,43.6,40.1,16.4),(0.0,45.9,42.7,11.4),(0.0,46.4,43.2,10.4),(0.0,49.5,36.4,14.1),(0.0,49.8,36.7,13.5),(0.0,50.7,30.4,18.9),(0.0,51.3,27.8,20.9),(0.0,52.4,27.5,20.1),(0.0,52.4,31.3,16.3),(0.0,52.6,27.6,19.8),(0.0,52.6,28.5,18.9),(0.0,52.7,27.5,19.8),(0.0,52.7,27.7,19.7),(0.0,52.8,28.6,18.6),(0.0,52.9,28.6,18.4),(0.0,53.1,27.9,18.9),(0.0,54.1,29.2,16.7),(0.0,54.4,28.6,17.1),(0.0,55.1,28.9,16.1),(0.0,55.3,23.4,21.4),(0.0,55.5,23.5,21.1),(0.0,55.6,20.5,23.9),(0.0,55.8,23.6,20.6),(0.0,55.8,29.1,15.1),(0.0,56.0,23.7,20.4),(0.0,56.3,23.8,19.8),(0.0,56.4,29.6,14.0),(0.0,56.9,20.9,22.2),(0.0,57.2,21.0,21.8),(0.0,59.2,12.6,28.1),(0.0,59.9,12.8,27.4),(13.6,31.8,35.7,18.9),(14.8,34.6,38.1,12.4),(15.4,35.8,37.6,11.2),(15.5,36.1,37.4,11.1),(15.5,36.3,30.4,17.8),(15.8,36.9,30.6,16.7),(16.0,37.4,28.7,17.8),(16.1,37.5,28.9,17.6),(16.1,37.7,28.7,17.5),(16.2,37.7,29.0,17.1),(16.2,37.8,28.8,17.2),(16.4,38.4,29.3,15.9),(16.5,38.6,29.1,15.8),(16.9,39.5,22.6,20.9),(17.0,39.6,30.4,13.1),(17.0,39.6,30.5,12.9),(17.4,40.7,24.4,17.5),(17.9,41.8,22.0,18.3),(18.0,42.0,21.8,18.2),(18.4,42.9,22.3,16.5),(19.1,44.7,13.4,22.7),(19.2,44.7,13.4,22.8),(23.0,23.0,35.7,18.2),(24.4,24.4,37.9,13.4),(25.9,25.9,37.8,10.5),(26.0,26.0,37.9,10.1),(26.3,26.3,30.8,16.6),(26.5,26.5,31.0,16.0),(27.2,27.2,29.4,16.1),(27.4,27.4,29.3,15.9),(27.8,27.8,29.5,15.0),(28.4,28.4,30.3,13.0),(28.4,28.4,30.8,12.4),(29.2,29.2,24.4,17.2),(29.3,29.3,24.6,16.8),(29.3,29.3,24.7,16.8),(29.4,29.4,24.6,16.6),(29.8,29.8,24.9,15.5),(30.5,30.5,22.4,16.7),(30.7,30.7,22.5,16.2),(31.1,31.1,22.7,15.1),(32.2,13.8,36.1,18.0),(32.6,32.6,13.8,21.0),(32.9,32.9,13.9,20.2),(33.9,14.5,36.5,15.2),(36.0,15.4,30.4,18.1),(36.5,15.6,31.4,16.5),(36.6,15.7,31.4,16.3),(36.9,15.8,31.7,15.5),(37.0,15.8,31.2,16.0),(37.0,15.9,30.8,16.3),(37.5,16.1,22.6,23.8),(38.2,16.4,23.1,22.3),(38.5,16.5,29.5,15.5),(38.6,16.5,23.3,21.6),(38.6,16.5,29.6,15.2),(38.6,16.5,29.9,15.0),(38.7,16.6,29.8,15.0),(38.7,16.6,40.6,4.1),(38.9,16.7,29.9,14.5),(39.0,16.7,30.0,14.3),(39.2,16.8,40.6,3.3),(39.3,16.8,23.7,20.1),(39.4,16.9,30.3,13.5),(39.5,16.9,29.3,14.3),(39.5,16.9,29.7,13.9),(39.5,16.9,30.4,13.2),(39.6,17.0,30.5,12.9),(39.7,17.0,30.6,12.6),(39.8,17.1,30.6,12.5),(41.5,17.8,25.0,15.7),(41.9,18.0,22.0,18.2),(43.2,18.5,22.7,15.6),(43.6,18.7,22.7,15.0),(46.0,19.7,14.0,20.4),(46.6,0.0,25.1,28.3),(46.9,20.1,14.0,19.1),(49.1,0.0,18.0,32.8),(49.6,0.0,29.3,21.1),(50.0,0.0,29.6,20.4),(50.1,0.0,29.6,20.2),(50.1,0.0,29.7,20.2),(50.8,0.0,30.1,19.1),(51.7,0.0,38.1,10.2),(52.3,0.0,31.3,16.4),(53.5,0.0,28.7,17.7),(53.6,0.0,22.8,23.6),(54.8,0.0,23.3,21.9),(54.9,0.0,28.8,16.3),(55.0,0.0,28.8,16.2),(55.2,0.0,20.2,24.6),(57.9,0.0,24.5,17.7),(58.4,0.0,12.3,29.3),(59.4,0.0,21.6,19.0),(60.0,0.0,12.7,27.3)]
RHO_AM, RHO_SE = 4.8, 2.0


def champ_se_of_solid(am_wt):
    w = am_wt / 100.0
    if w <= 0: return 100.0
    if w >= 1: return 0.0
    a = w / RHO_AM; b = (1 - w) / RHO_SE
    return 100.0 * (1 - a / (a + b))


def main():
    d = np.array(DEM)
    amp, ams, se, po = d[:, 0], d[:, 1], d[:, 2], d[:, 3]
    am_vol = amp + ams
    # weight fraction AM (vol→wt) and SE fraction of solid
    am_wt = 100.0 * (am_vol * RHO_AM) / (am_vol * RHO_AM + se * RHO_SE)
    se_solid = 100.0 * se / (am_vol + se)
    p_of_am = np.where(am_vol > 0, 100.0 * amp / np.maximum(am_vol, 1e-9), 0.0)  # AM_P % of AM

    champ_ss = np.array([champ_se_of_solid(a) for a in CHAMP_AM])
    order = np.argsort(champ_ss)

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(13.6, 5.6))

    # ── Panel A: porosity vs AM wt% ──
    axA.plot(CHAMP_AM, CHAMP_PLASTIC, '-o', color='#2e8b57', lw=2.2, ms=5,
             label='champion MPM — SE PLASTIC')
    axA.plot(CHAMP_AM, CHAMP_RIGID, '-s', color='#c0392b', lw=2.0, ms=5, alpha=0.85,
             label='champion MPM — SE RIGID')
    axA.scatter(am_wt, po, s=15, c='#2453b8', alpha=0.4, label=f'DEM (n={len(d)})')
    bx = sorted(set((am_wt / 5).round() * 5))
    bmed = [np.median(po[np.abs(am_wt - b) <= 2.5]) for b in bx]
    axA.plot(bx, bmed, '-D', color='#10246b', lw=2.2, ms=6, label='DEM binned median')
    axA.axvspan(70, 85, color='#ffe9a8', alpha=0.35, zorder=0)
    axA.set_xlabel('AM weight fraction (%)'); axA.set_ylabel('porosity (%)')
    axA.set_title('A) porosity vs AM wt%', fontsize=10)
    axA.grid(alpha=0.3); axA.legend(fontsize=7.5, loc='upper left')

    # ── Panel B: porosity vs SE-fraction-of-solid, DEM coloured by P:S ──
    axB.plot(champ_ss[order], np.array(CHAMP_PLASTIC)[order], '-o', color='#2e8b57',
             lw=2.2, ms=5, label='champion MPM — SE PLASTIC (P:S=7:3)')
    axB.plot(champ_ss[order], np.array(CHAMP_RIGID)[order], '-s', color='#c0392b',
             lw=2.0, ms=5, alpha=0.85, label='champion MPM — SE RIGID')
    sc = axB.scatter(se_solid, po, s=18, c=p_of_am, cmap='coolwarm', vmin=0, vmax=100,
                     alpha=0.8, edgecolor='none')
    axB.axvspan(30, 50, color='#ffe9a8', alpha=0.35, zorder=0)
    axB.set_xlabel('SE fraction of solid (%)  [density-independent]')
    axB.set_ylabel('porosity (%)')
    axB.set_title('B) porosity vs SE/solid — DEM coloured by AM_P share '
                  '(blue=AM_S only → red=AM_P)', fontsize=9.5)
    axB.grid(alpha=0.3); axB.legend(fontsize=7.5, loc='upper right')
    fig.colorbar(sc, ax=axB, shrink=0.8, label='AM_P % of AM (bimodal split)')

    fig.suptitle('DEM ↔ champion MPM porosity-vs-composition — DEM median tracks '
                 'PLASTIC MPM through the production core\n(AM 70-85% ≡ SE 30-50% '
                 'of solid); spread at fixed composition = size (Furnas) effect',
                 fontsize=11)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    plt.tight_layout(rect=[0, 0, 1, 0.95]); plt.savefig(OUT, dpi=140)
    print(f"saved {OUT}")

    # text verdict on the SE-of-solid axis
    cx = champ_ss[order]; cpp = np.array(CHAMP_PLASTIC)[order]; cpr = np.array(CHAMP_RIGID)[order]
    print("\n  SE/solid%  n   DEMmed  MPMplas  MPMrig   verdict")
    for b in range(20, 70, 10):
        sel = np.abs(se_solid - b) <= 5
        if sel.sum() == 0: continue
        m = float(np.median(po[sel])); pp = float(np.interp(b, cx, cpp)); pr = float(np.interp(b, cx, cpr))
        tag = 'DEM≈plastic' if abs(m - pp) < abs(m - pr) else 'DEM≈rigid'
        print(f"  {b:7d}  {int(sel.sum()):3d}  {m:6.1f}  {pp:6.1f}  {pr:6.1f}   {tag}")


if __name__ == '__main__':
    main()
