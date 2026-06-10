#!/usr/bin/env python3
"""Figures for the DEM<->MPM wallP@512 cross-validation (reads the matcher CSV).

  docs/figures/mpm_dem_parity.png    DEM vs MPM scatter, colored by r_SE band,
                                     1:1 line, force-chain corner ringed.
  docs/figures/mpm_dem_dip.png       Furnas dip: median porosity vs AM% (rSE<=0.5),
                                     DEM vs MPM (+ MPM with force-chain excluded),
                                     dip minimum + force-chain region marked.
  docs/figures/mpm_dem_band_bias.png per-r_SE-band mean Delta (MPM-DEM) bars.

Frame [4]: agreement = cross-validation, divergence = quantified continuum limit.
Tunes nothing -- pure visualisation of the already-computed parity.
"""
import csv
import os
import sys

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt   # noqa: E402

CSV = sys.argv[1] if len(sys.argv) > 1 else 'docs/data/mpm_dem_match.csv'
FCT = 15.0                                   # MPM-DEM %p = force-chain flag
OUT = 'docs/figures'
os.makedirs(OUT, exist_ok=True)

rows = []
with open(CSV) as fh:
    for d in csv.DictReader(fh):
        try:
            rows.append((d['name'], float(d['dem_porosity']), float(d['mpm_porosity']),
                         float(d.get('mpm_std', 0) or 0), float(d['r_SE']), float(d['AM_wt'])))
        except (ValueError, KeyError):
            continue
rows = [r for r in rows if np.isfinite(r[2])]
if not rows:
    sys.exit("no usable rows in " + CSV)
dem = np.array([r[1] for r in rows]); mpm = np.array([r[2] for r in rows])
rse = np.array([r[4] for r in rows]); amwt = np.array([r[5] for r in rows])
print(f"loaded {len(rows)} cases from {CSV}")

BANDS = [(0, 0.75, 'rSE<=0.5', '#2980b9'), (0.75, 1.25, 'rSE~1.0', '#27ae60'),
         (1.25, 9.9, 'rSE>=1.5', '#e67e22')]
fc = (rse <= 0.5) & (mpm - dem > FCT)


def _band_stat(mask):
    d, p = dem[mask], mpm[mask]
    pe = np.corrcoef(d, p)[0, 1] if mask.sum() >= 2 else float('nan')
    return np.mean(p - d), np.mean(np.abs(p - d)), pe


# ── fig1: parity ───────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6.0, 5.9))
lim = max(dem.max(), mpm.max()) * 1.08
ax.plot([0, lim], [0, lim], 'k--', lw=1, alpha=0.6, label='1:1')
for lo, hi, lab, c in BANDS:
    m = (rse >= lo) & (rse < hi) & ~fc
    if m.sum():
        b, a, pe = _band_stat((rse >= lo) & (rse < hi))
        ax.scatter(dem[m], mpm[m], s=30, c=c, alpha=0.82, edgecolors='none',
                   label=f'{lab} n={((rse>=lo)&(rse<hi)).sum()}  d{b:+.1f} r{pe:.2f}')
if fc.sum():
    ax.scatter(dem[fc], mpm[fc], s=48, facecolors='none', edgecolors='#c0392b',
               linewidths=1.5, label=f'force-chain n={fc.sum()}')
r2 = 1 - np.sum((dem - mpm) ** 2) / np.sum((dem - dem.mean()) ** 2)
ax.set_xlabel('DEM porosity (%)'); ax.set_ylabel('MPM porosity (%)')
ax.set_title(f'DEM<->MPM parity  (champion wallP @512, n={len(rows)})\n'
             f'overall mean|d|={np.mean(np.abs(dem-mpm)):.1f}%p  Pearson={np.corrcoef(dem,mpm)[0,1]:.2f}')
ax.legend(fontsize=7.5, loc='upper left'); ax.set_xlim(0, lim); ax.set_ylim(0, lim)
ax.grid(alpha=0.25); plt.tight_layout()
plt.savefig(f'{OUT}/mpm_dem_parity.png', dpi=140); print('saved mpm_dem_parity.png')
plt.close()

# ── fig2: Furnas dip ───────────────────────────────────────────────────────
band = rse <= 0.5
bins = [(55, 65), (65, 72), (72, 78), (78, 83), (83, 88), (88, 95), (95, 101)]
xc, dM, mM, mMc = [], [], [], []
for lo, hi in bins:
    m = band & (amwt >= lo) & (amwt < hi)
    if m.sum() == 0:
        continue
    xc.append((lo + hi) / 2.0); dM.append(np.median(dem[m])); mM.append(np.median(mpm[m]))
    mc = m & ~fc
    mMc.append(np.median(mpm[mc]) if mc.sum() else np.nan)
fig, ax = plt.subplots(figsize=(7.2, 5.2))
ax.axvspan(80, 101, color='#c0392b', alpha=0.07, label='force-chain region (AM>=80)')
ax.plot(xc, dM, 'o-', c='#2c3e50', lw=2.2, ms=7, label='DEM (contact network)')
ax.plot(xc, mM, 's-', c='#c0392b', lw=2.0, ms=6, label='MPM champion (all)')
ax.plot(xc, mMc, 's--', c='#e67e22', lw=1.7, ms=5, alpha=0.95, label='MPM (force-chain excl.)')
imin = int(np.nanargmin(dM))
ax.annotate('dip minimum\nAM72-78', xy=(xc[imin], dM[imin]), xytext=(xc[imin] - 2, dM[imin] - 5),
            fontsize=9, ha='center', arrowprops=dict(arrowstyle='->', color='#2c3e50'))
ax.set_xlabel('AM content (wt%)'); ax.set_ylabel('median porosity (%)')
ax.set_title('Furnas dip co-located: DEM vs independent plastic MPM (rSE<=0.5)')
ax.legend(fontsize=8.5); ax.grid(alpha=0.25); plt.tight_layout()
plt.savefig(f'{OUT}/mpm_dem_dip.png', dpi=140); print('saved mpm_dem_dip.png')
plt.close()

# ── fig3: per-band bias ────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6.0, 4.4))
labs, biases, cs = [], [], []
for lo, hi, lab, c in BANDS:
    m = (rse >= lo) & (rse < hi)
    if m.sum() == 0:
        continue
    b, a, pe = _band_stat(m)
    labs.append(f'{lab}\nn={m.sum()}\nr={pe:.2f}'); biases.append(b); cs.append(c)
ax.bar(range(len(labs)), biases, color=cs, alpha=0.85)
ax.axhline(0, c='k', lw=0.8)
for i, b in enumerate(biases):
    ax.text(i, b + (0.2 if b >= 0 else -0.5), f'{b:+.1f}', ha='center', fontsize=9)
ax.set_xticks(range(len(labs))); ax.set_xticklabels(labs, fontsize=9)
ax.set_ylabel('mean d = MPM - DEM (%p)')
ax.set_title('Per-r_SE-band bias (wallP @512)')
ax.grid(axis='y', alpha=0.25); plt.tight_layout()
plt.savefig(f'{OUT}/mpm_dem_band_bias.png', dpi=140); print('saved mpm_dem_band_bias.png')
plt.close()
print('done -> docs/figures/')
