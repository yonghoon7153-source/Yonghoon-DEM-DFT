#!/usr/bin/env python3
"""Consolidated MPM LPSCl-compaction summary figure (3 panels).

Reads the committed rigid-jamming + grid-free geometric CSVs; the plastic
(champion E=1.53/σ_y=0.15) jamming numbers are embedded from the uma run
(2026-06-08).  Narrative: docs/mpm_lpscl_compaction_summary.md.

  Panel A  RIGID dip is resolution-invariant (320≈512≈geometry).
  Panel B  PLASTIC dip — early(f05) vs deep(f50): attenuated + grid-sensitive.
  Panel C  porosity into the experimental window only with plasticity.

Run (machine with matplotlib):  python3 scripts/plot_mpm_compaction_summary.py
Out: docs/figures/mpm_compaction_summary.png
"""
import os
import csv
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'docs', 'data')
AM = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 85, 90, 95, 100], float)


def col(path, key):
    with open(path) as fh:
        r = list(csv.DictReader(fh))
    am = np.array([float(x['AM_wt%']) for x in r])
    y = np.array([float(x[key]) for x in r])
    return am, y


# ---- committed data (rigid 7:3 + grid-free geometry) ----------------------
ra, rig320 = col(os.path.join(DATA, 'jam_320.csv'), 'eps_f05')
_,  rig512 = col(os.path.join(DATA, 'jam_512.csv'), 'eps_f05')
ga, geom = col(os.path.join(DATA, 'packing_dip_model_ps73.csv'), 'poros_beta0.84')

# ---- plastic champion (E=1.53/σ_y=0.15) — embedded from the uma run --------
plas = {
    'f05_320': [42.99, 37.89, 37.62, 33.50, 33.23, 31.39, 29.58, 29.64, 28.52, 27.40, 30.05, 29.70, 33.24],
    'f05_512': [36.56, 31.15, 31.05, 28.72, 28.52, 27.55, 26.81, 28.29, 27.88, 28.67, 28.95, 27.33, 30.75],
    'f50_320': [23.27, 18.48, 18.12, 15.18, 14.97, 13.99, 12.87, 12.09, 11.87, 11.29, 11.40, 13.52, 15.84],
    'f50_512': [16.07, 11.64, 11.56, 10.86, 10.87, 10.09, 9.51, 9.08, 9.71, 10.28, 10.59, 11.79, 14.46],
}
plas = {k: np.array(v) for k, v in plas.items()}


def main():
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except Exception as e:
        print(f"matplotlib needed: {e}"); return

    fig, ax = plt.subplots(1, 3, figsize=(15, 4.4))

    # Panel A — rigid resolution-invariance
    ax[0].plot(ra, rig320, '-o', color='#c0392b', ms=4, label='rigid MPM 320')
    ax[0].plot(ra, rig512, '-s', color='#2980b9', ms=4, label='rigid MPM 512')
    ax[0].plot(ga, geom, '--', color='#2e8b57', lw=2, label='grid-free geometry')
    ax[0].set_title('A. RIGID dip — resolution-INVARIANT\n(Pearson 320↔512 = 0.99)', fontsize=10)
    ax[0].set_xlabel('AM wt%'); ax[0].set_ylabel('jamming porosity (%)')
    ax[0].legend(fontsize=8); ax[0].grid(alpha=0.3)

    # Panel B — plastic dip early vs deep
    ax[1].plot(AM, plas['f05_320'], '-o', color='#e67e22', ms=4, label='plastic f05 (early) 320')
    ax[1].plot(AM, plas['f05_512'], '--o', color='#e67e22', ms=3, alpha=0.6, label='plastic f05 512')
    ax[1].plot(AM, plas['f50_320'], '-s', color='#8e44ad', ms=4, label='plastic f50 (deep) 320')
    ax[1].plot(AM, plas['f50_512'], '--s', color='#8e44ad', ms=3, alpha=0.6, label='plastic f50 512')
    ax[1].set_title('B. PLASTIC dip (champion 1.53/0.15)\nattenuated + grid-sensitive (Pearson 0.80–0.89)', fontsize=10)
    ax[1].set_xlabel('AM wt%'); ax[1].set_ylabel('porosity (%)')
    ax[1].legend(fontsize=7); ax[1].grid(alpha=0.3)

    # Panel C — porosity into the experimental window only with plasticity
    ax[2].axhspan(10, 16, color='gray', alpha=0.18, label='experiment ~10–16%')
    ax[2].plot(ra, rig320, '-o', color='#c0392b', ms=4, label='rigid (geometry) 320')
    ax[2].plot(AM, plas['f50_512'], '-s', color='#8e44ad', ms=4, label='plastic f50 512')
    ax[2].plot(ga, geom, '--', color='#2e8b57', lw=2, label='grid-free geometry')
    ax[2].axhline(11.4, color='k', ls=':', lw=1)
    ax[2].annotate('Minnmann pure-SE 300→~10%', (2, 11.4), fontsize=7, va='bottom')
    ax[2].set_title('C. Only PLASTIC reaches the experimental porosity\n(rigid 30–50% too high)', fontsize=10)
    ax[2].set_xlabel('AM wt%'); ax[2].set_ylabel('porosity (%)')
    ax[2].legend(fontsize=8); ax[2].grid(alpha=0.3)

    fig.suptitle('MPM LPSCl 2D compaction — RIGID dip is resolution-invariant; '
                 'PLASTIC makes porosity realistic but attenuates/grid-sensitises the dip',
                 fontsize=11)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    os.makedirs(os.path.join(HERE, '..', 'docs', 'figures'), exist_ok=True)
    out = os.path.join(HERE, '..', 'docs', 'figures', 'mpm_compaction_summary.png')
    plt.savefig(out, dpi=130)
    print(f"saved {out}")


if __name__ == '__main__':
    main()
