#!/usr/bin/env python3
"""de Larrard geometric packing model vs the DEM corpus (132 design points).

(b) of "MPM = morphology, DEM/de Larrard = dip": the resolved-grain plastic MPM
CANNOT reproduce the Furnas dip (material-independent, proven by mpm_dem_match
--sweep) because the dip lives in the INITIAL rigid-sphere packing.  de Larrard's
linear packing model IS that geometry -- grid-free, instant, and it HAS the dip.
This calibrates de Larrard (beta, K) to the DEM porosity corpus and reports
whether the geometric dip CO-LOCATES with DEM -- i.e. whether de Larrard is the
fast porosity+dip model to use in DEM's place where the plastic MPM fails.

Reads docs/data/dem_design_points.csv (all 300 MPa); per case uses the case's
own size ratios.  No grid, no GPU.  K is the de Larrard compaction index (~9 cold
press); higher P -> higher K -> lower porosity (the pressure/Heckel axis).
"""
import csv
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from packing_dip_model import actual_phi, vol_fracs   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DP = os.path.join(HERE, '..', 'docs', 'data', 'dem_design_points.csv')


def dl_poros(am_wt, ps, rP, rS, beta, K):
    """de Larrard porosity (%) for one composition at its own size ratios (SE=1)."""
    f = vol_fracs(am_wt, ps)
    diams = [rP, rS, 1.0]; y = [f['AMP'], f['AMS'], f['SE']]
    nz = [k for k in range(3) if y[k] > 1e-9]
    if not nz:
        return float('nan')
    phi = actual_phi([diams[k] for k in nz], [beta] * len(nz), [y[k] for k in nz], K=K)
    return (1.0 - phi) * 100.0


rows = []
with open(DP) as fh:
    for r in csv.DictReader(fh):
        try:
            p, s = (int(z) for z in r['PS'].split(':'))
            rows.append(dict(name=r['name'], am=float(r['AM_wt']), rse=float(r['r_SE']),
                             ps=(p, s), rP=float(r['ratio_P']), rS=float(r['ratio_S']),
                             dem=float(r['dem_porosity'])))
        except (ValueError, KeyError):
            continue
print(f"loaded {len(rows)} DEM design points (all 300 MPa)")
dem = np.array([r['dem'] for r in rows])
rse = np.array([r['rse'] for r in rows]); am = np.array([r['am'] for r in rows])

# ── calibrate (beta, K) to best-fit DEM porosity (grid search) ──────────────
best = None
for beta in np.arange(0.72, 0.905, 0.02):
    for K in (4, 6, 8, 10, 13, 16, 20, 25, 30, 40, 60):
        dl = np.array([dl_poros(r['am'], r['ps'], r['rP'], r['rS'], beta, K) for r in rows])
        mm = np.isfinite(dl)
        if mm.sum() < 10:
            continue
        mae = float(np.mean(np.abs(dl[mm] - dem[mm])))
        if best is None or mae < best[0]:
            best = (mae, float(beta), K, dl)
mae, beta, K, dl = best
m = np.isfinite(dl)
r2 = 1 - np.sum((dem[m] - dl[m]) ** 2) / np.sum((dem[m] - dem[m].mean()) ** 2)
pear = float(np.corrcoef(dem[m], dl[m])[0, 1])
print(f"\nbest-fit de Larrard: beta={beta:.2f}, K={K}  ->  mean|d|={mae:.1f}%p, "
      f"R2={r2:.3f}, Pearson={pear:.3f}  (n={m.sum()})  [MPM nu0.49 was mean|d|~5.3, no dip]")

# ── per-r_SE band parity (compare to the MPM bands) ─────────────────────────
print("\n-- per-r_SE band (de Larrard vs DEM) --")
for lo, hi, lab in [(0, 0.75, 'rSE<=0.5'), (0.75, 1.25, 'rSE~1.0'), (1.25, 9.9, 'rSE>=1.5')]:
    b = m & (rse >= lo) & (rse < hi)
    if b.sum() == 0:
        continue
    pe = np.corrcoef(dem[b], dl[b])[0, 1] if b.sum() >= 2 else float('nan')
    print(f"  {lab:9s} n={b.sum():3d}  meanD={np.mean(dl[b]-dem[b]):+5.1f}  "
          f"mean|D|={np.mean(np.abs(dl[b]-dem[b])):4.1f}  Pearson={pe:+.3f}")

# ── Furnas dip co-location (rSE<=0.5, binned by AM) ─────────────────────────
print("\n-- Furnas dip: porosity vs AM_wt (rSE<=0.5), DEM | de Larrard medians --")
band = rse <= 0.5
xs, dem_b, dl_b = [], [], []
for lo, hi in [(0, 65), (65, 72), (72, 78), (78, 83), (83, 88), (88, 95), (95, 101)]:
    mm = band & (am >= lo) & (am < hi) & m
    if mm.sum() == 0:
        continue
    xs.append((lo + hi) / 2.0); dem_b.append(float(np.median(dem[mm]))); dl_b.append(float(np.median(dl[mm])))
    print(f"  AM {lo:3d}-{hi:3d}  n={mm.sum():3d}  DEM={np.median(dem[mm]):5.1f}  deLarrard={np.median(dl[mm]):5.1f}")


def dip_of(x, y):
    if len(y) < 3:
        return "n/a"
    i = int(np.argmin(y))
    return f"DIP at AM{int(x[i])} ({y[i]:.1f})" if 0 < i < len(y) - 1 else "MONOTONIC (min at end)"


print(f"  DEM        -> {dip_of(xs, dem_b)}")
print(f"  de Larrard -> {dip_of(xs, dl_b)}    (MPM champion: MONOTONIC / no dip)")
