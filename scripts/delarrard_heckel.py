#!/usr/bin/env python3
"""Complete fast Heckel + dip model: de Larrard mixing with a PRESSURE-dependent
plastic SE packing density beta_SE(P) anchored to the Minnmann pure-SE Heckel.

de Larrard alone (RIGID packing) floors at the single-species limit, so it cannot
reach the experimental pure-SE tail (that densification is PLASTICITY).  Here the
SE is plastic: its effective single-species packing density beta_SE(P) RISES with
pressure, calibrated so de Larrard pure-SE reproduces the Minnmann/cap pure-SE
Heckel (100->13.9 / 300->10 / 600->8.3 %).  The rigid AM keeps a constant beta_AM.
de Larrard's linear mixing then yields porosity(P, composition, size) = the Heckel
(via beta_SE(P)) AND the Furnas dip (via the packing geometry) -- one grid-free,
instant model.  (beta_AM, K) are fit to the 132-case DEM corpus @ 300 MPa.

Run: python3 scripts/delarrard_heckel.py
"""
import csv
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from packing_dip_model import actual_phi, vol_fracs   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DP = os.path.join(HERE, '..', 'docs', 'data', 'dem_design_points.csv')

# pure-SE Heckel anchor: Minnmann 300->10%; cap_compaction_heckel shape at 100/600
_ANCHOR = [(100.0, 13.9), (300.0, 10.0), (600.0, 8.3)]
_Ps = np.array([a[0] for a in _ANCHOR]); _ys = np.array([a[1] for a in _ANCHOR])
_C = np.linalg.lstsq(np.vstack([np.ones_like(_Ps), np.log(_Ps)]).T, _ys, rcond=None)[0]


def phi_se(P):
    """pure-SE porosity (%) vs pressure: log-P fit to the Minnmann/cap anchor, floored 3%."""
    return float(max(3.0, _C[0] + _C[1] * np.log(P)))


def beta_se(P, K):
    """effective plastic SE single-species packing density so de Larrard pure-SE at
    compaction index K reproduces phi_se(P).  (RISES with P = plastic densification.)"""
    return min(0.999, (1.0 - phi_se(P) / 100.0) * (K + 1.0) / K)


def poros(P, am_wt, ps, rP, rS, beta_am, K, c=0.0, r0=4.0):
    f = vol_fracs(am_wt, ps)
    diams = [rP, rS, 1.0]; betas = [beta_am, beta_am, beta_se(P, K)]; y = [f['AMP'], f['AMS'], f['SE']]
    nz = [k for k in range(3) if y[k] > 1e-9]
    if not nz:
        return float('nan')
    phi = actual_phi([diams[k] for k in nz], [betas[k] for k in nz], [y[k] for k in nz], K=K)
    base = (1.0 - phi) * 100.0
    # extreme size-ratio LOOSENING: real fine-SE filling of coarse-AM voids is sub-ideal
    # (bridging / wall friction), so de Larrard's IDEAL mixing over-densifies at big AM:SE
    # ratios.  ratio_eff = (p·rP+s·rS)/(p+s) is the AM:SE size disparity; add porosity above a
    # threshold r0, faded smoothly to 0 as SE->0 (pure-AM has no fine SE to over-fill).
    fam = f['AMP'] + f['AMS']
    if fam > 1e-6 and f['SE'] > 1e-6:
        ratio_eff = (f['AMP'] * rP + f['AMS'] * rS) / fam
        w = min(1.0, f['SE'] / 0.05)
        base += c * max(0.0, ratio_eff - r0) * w
    return base


rows = []
with open(DP) as fh:
    for r in csv.DictReader(fh):
        try:
            p, s = (int(z) for z in r['PS'].split(':'))
            rows.append(dict(am=float(r['AM_wt']), rse=float(r['r_SE']), ps=(p, s),
                             rP=float(r['ratio_P']), rS=float(r['ratio_S']), dem=float(r['dem_porosity'])))
        except (ValueError, KeyError):
            continue
dem = np.array([r['dem'] for r in rows]); rse = np.array([r['rse'] for r in rows])

# fit (beta_AM, K) to DEM @300 (K>=10 keeps beta_SE<=1 for the pure-SE anchor)
best = None
for c in np.arange(0.0, 2.01, 0.2):
    for beta_am in np.arange(0.78, 0.905, 0.01):
        for K in (10, 12, 15, 18, 22, 27, 33, 40, 50):
            pr = np.array([poros(300.0, r['am'], r['ps'], r['rP'], r['rS'], beta_am, K, c) for r in rows])
            mm = np.isfinite(pr)
            if mm.sum() < 10:
                continue
            mae = float(np.mean(np.abs(pr[mm] - dem[mm])))
            if best is None or mae < best[0]:
                best = (mae, float(beta_am), K, float(c), pr)
mae, beta_am, K, c, pr = best; m = np.isfinite(pr)
print(f"fit to DEM @300:  beta_AM={beta_am:.2f}, K={K}, c_loosen={c:.1f}, beta_SE(300)={beta_se(300,K):.3f}")
print(f"  -> mean|d|={mae:.1f}%p (n={m.sum()})   [uncorrected was 6.0; fixed-K de Larrard 3.5]")

print("\n== pure-SE Heckel: model vs Minnmann/cap anchor ==")
print(f"  {'P(MPa)':>7s} {'model':>6s} {'anchor':>7s}")
for P, a in sorted(_ANCHOR + [(200.0, None), (1000.0, None)]):
    mod = poros(P, 0.0, (7, 3), 12.0, 4.0, beta_am, K, c)
    print(f"  {P:7.0f} {mod:6.1f} {('%.1f' % a) if a else '   -':>7s}")

print("\n== composite Heckel + Furnas dip at 3 pressures (12:4:1, 7:3) ==")
print(f"  {'P(MPa)':>7s} {'AM82':>6s} {'dip@AM':>7s} {'dip_por':>8s}  (dip moves? depth?)")
ams = np.arange(50, 101, 5)
for P in (100.0, 300.0, 600.0):
    c82 = poros(P, 82.0, (7, 3), 12.0, 4.0, beta_am, K, c)
    cur = np.array([poros(P, a, (7, 3), 12.0, 4.0, beta_am, K, c) for a in ams])
    i = int(np.argmin(cur)); depth = 0.5 * (cur[0] + cur[-1]) - cur[i]
    print(f"  {P:7.0f} {c82:6.1f} {('AM%d' % ams[i]):>7s} {cur[i]:8.1f}  depth {depth:.1f}%p")

print("\n== validation vs DEM @300, per r_SE band ==")
for lo, hi, lab in [(0, 0.75, 'rSE<=0.5'), (0.75, 1.25, 'rSE~1.0'), (1.25, 9.9, 'rSE>=1.5')]:
    b = m & (rse >= lo) & (rse < hi)
    if b.sum() == 0:
        continue
    pe = np.corrcoef(dem[b], pr[b])[0, 1] if b.sum() >= 2 else float('nan')
    print(f"  {lab:9s} n={b.sum():3d}  meanD={np.mean(pr[b]-dem[b]):+5.1f}  "
          f"mean|D|={np.mean(np.abs(pr[b]-dem[b])):4.1f}  Pearson={pe:+.3f}")
