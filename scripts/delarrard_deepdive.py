#!/usr/bin/env python3
"""de Larrard deep-dive vs DEM: size dependence, P:S dip, and the K(P) Heckel axis.

Follows scripts/delarrard_vs_dem.py (de Larrard fits DEM porosity ~3.5%p AND HAS
the dip, where the plastic MPM is monotonic).  Digs into whether de Larrard also
captures the GEOMETRIC structure the MPM could NOT: (1) the size dependence /
crossover (porosity vs r_SE at fixed composition), (2) how the dip moves with P:S,
(3) the pressure axis via the de Larrard compaction index K(P) -> Heckel.
Grid-free, instant, reads docs/data/dem_design_points.csv (all 300 MPa).
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
            rows.append(dict(am=float(r['AM_wt']), rse=float(r['r_SE']), ps=(p, s),
                             rP=float(r['ratio_P']), rS=float(r['ratio_S']), dem=float(r['dem_porosity'])))
        except (ValueError, KeyError):
            continue
dem = np.array([r['dem'] for r in rows]); rse = np.array([r['rse'] for r in rows]); am = np.array([r['am'] for r in rows])

# calibrate (beta, K) to DEM
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
mae, beta, K, dl = best; m = np.isfinite(dl)
print(f"calibrated de Larrard: beta={beta:.2f} K={K}  mean|d|={mae:.1f}%p (n={m.sum()})\n")

# ── (1) SIZE dependence: porosity vs r_SE at AM bins (the MPM size-crossover failure) ──
print("== (1) SIZE: porosity vs r_SE at fixed AM (DEM | deLarrard) — MPM could NOT do this ==")
for alo, ahi, alab in [(58, 68, 'AM~62 (SE-rich)'), (72, 80, 'AM~76 (dip)'), (80, 90, 'AM~85 (AM-rich)')]:
    ab = m & (am >= alo) & (am < ahi)
    if ab.sum() == 0:
        continue
    print(f"  [{alab}]  n={ab.sum()}")
    for lo, hi, lab in [(0, 0.4, 'rSE0.25'), (0.4, 0.75, 'rSE0.5'), (0.75, 1.25, 'rSE1.0'), (1.25, 9.9, 'rSE1.5')]:
        b = ab & (rse >= lo) & (rse < hi)
        if b.sum() == 0:
            continue
        print(f"    {lab:8s} n={b.sum():2d}  DEM={np.median(dem[b]):5.1f}  deLarrard={np.median(dl[b]):5.1f}  Δ={np.median(dl[b]-dem[b]):+4.1f}")

# ── (2) dip vs P:S (clean de Larrard sweep, canonical 12:4:1) ──
print("\n== (2) DIP vs P:S (clean de Larrard sweep, 12:4:1) ==")
ams = np.arange(50, 101, 5)
for ps in sorted(set(r['ps'] for r in rows)):
    cur = np.array([dl_poros(a, ps, 12.0, 4.0, beta, K) for a in ams])
    i = int(np.argmin(cur))
    if 0 < i < len(cur) - 1:
        print(f"  P:S {ps[0]}:{ps[1]}  dip @ AM{ams[i]} ({cur[i]:.1f}%)  depth {0.5*(cur[0]+cur[-1])-cur[i]:.1f}%p")
    else:
        print(f"  P:S {ps[0]}:{ps[1]}  monotonic (min at AM{ams[i]})")

# ── (3) K(P) Heckel: the pressure axis ──
print("\n== (3) K(P) Heckel — de Larrard pressure axis (K rises with P) ==")
print(f"  {'P(MPa)':>7s} {'K':>4s} {'comp_AM82_7:3':>13s} {'pure_SE':>8s}   (12:4:1)")
for P, Kp in [(100, 4), (200, 5), (300, 6), (450, 8), (600, 11), (1000, 18)]:
    comp = dl_poros(82.0, (7, 3), 12.0, 4.0, beta, Kp)
    pse = dl_poros(0.0, (7, 3), 12.0, 4.0, beta, Kp)
    print(f"  {P:7d} {Kp:4d} {comp:13.1f} {pse:8.1f}")
print(f"  pure-SE FLOORS at the rigid single-species limit 1-beta = {(1-beta)*100:.0f}% "
      f"(needs PLASTICITY for the experimental ~8%@600 tail);")
print("  the COMPOSITE densifies geometrically (small SE fills big-AM voids) -> reaches the dip.")
print("  ⇒ K(P) gives the Heckel SHAPE + dip for composites; the pure-SE tail is the")
print("     rigid-packing floor where the plastic MPM (or DPC) is still needed.")
