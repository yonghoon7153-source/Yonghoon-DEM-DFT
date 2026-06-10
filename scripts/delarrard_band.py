#!/usr/bin/env python3
"""Physical de Larrard TREND + uncertainty BAND (NOT fit to DEM).

User: "DEM 절대값은 안 맞아도 돼 -- 트렌드랑 오차범위만 있으면 돼."  So we DROP the
DEM-calibrated absolute (the circular part) and use PHYSICAL parameter RANGES:
  beta_AM : 2D random-close-packing of polydisperse disks ~0.84   -> sweep 0.80-0.88
  beta_SE(P): from the Minnmann pure-SE Heckel (experiment anchor) -> tied to K
  K       : de Larrard compaction index, cold press ~9            -> sweep 6-15
  c_loosen: extreme-ratio fine-SE sub-ideal filling (form physical, magnitude the
            least-pinned)                                          -> sweep 0-1.5
Sweeping these PHYSICAL ranges gives a porosity BAND at each (P, composition, size);
the central is the physical default (0.84, 9, 0.7).  The TREND -- the Furnas dip +
the size + the pressure dependence -- comes from GEOMETRY (Furnas, self-validated)
and EXPERIMENT (Minnmann), independent of DEM.  DEM is used ONLY as a SANITY CHECK
(coverage: does the DEM porosity fall inside the physical band?), never as a fit.
Grid-free, instant.
"""
import csv
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from packing_dip_model import actual_phi, vol_fracs   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DP = os.path.join(HERE, '..', 'docs', 'data', 'dem_design_points.csv')

_ANCHOR = [(100.0, 13.9), (300.0, 10.0), (600.0, 8.3)]   # Minnmann 300->10 + cap shape
_Ps = np.array([a[0] for a in _ANCHOR]); _ys = np.array([a[1] for a in _ANCHOR])
_C = np.linalg.lstsq(np.vstack([np.ones_like(_Ps), np.log(_Ps)]).T, _ys, rcond=None)[0]


def phi_se(P):
    return float(max(3.0, _C[0] + _C[1] * np.log(P)))


def beta_se(P, K):
    return min(0.999, (1.0 - phi_se(P) / 100.0) * (K + 1.0) / K)


def poros(P, am_wt, ps, rP, rS, beta_am, K, c, r0=4.0):
    f = vol_fracs(am_wt, ps)
    diams = [rP, rS, 1.0]; betas = [beta_am, beta_am, beta_se(P, K)]; y = [f['AMP'], f['AMS'], f['SE']]
    nz = [k for k in range(3) if y[k] > 1e-9]
    if not nz:
        return float('nan')
    phi = actual_phi([diams[k] for k in nz], [betas[k] for k in nz], [y[k] for k in nz], K=K)
    base = (1.0 - phi) * 100.0
    fam = f['AMP'] + f['AMS']
    if fam > 1e-6 and f['SE'] > 1e-6:
        ratio_eff = (f['AMP'] * rP + f['AMS'] * rS) / fam
        base += c * max(0.0, ratio_eff - r0) * min(1.0, f['SE'] / 0.05)
    return base


# ── PHYSICAL parameter ranges (NOT fit to DEM) ──────────────────────────────
BETA_AM = [0.80, 0.84, 0.88]   # 2D-RCP polydisperse spread
K_RANGE = [6, 9, 15]           # de Larrard cold-press compaction index
C_RANGE = [0.0, 0.7, 1.5]      # extreme-ratio loosening (magnitude uncertainty)
CENTRAL = (0.84, 9, 0.7)


def band(P, am, ps, rP, rS):
    v = [poros(P, am, ps, rP, rS, ba, K, c) for ba in BETA_AM for K in K_RANGE for c in C_RANGE]
    v = [x for x in v if x == x]
    return (min(v), max(v)) if v else (float('nan'), float('nan'))


def central(P, am, ps, rP, rS):
    return poros(P, am, ps, rP, rS, CENTRAL[0], CENTRAL[1], CENTRAL[2])


# ── DEM coverage (SANITY CHECK only, not a fit) ─────────────────────────────
rows = []
with open(DP) as fh:
    for r in csv.DictReader(fh):
        try:
            p, s = (int(z) for z in r['PS'].split(':'))
            rows.append(dict(am=float(r['AM_wt']), rse=float(r['r_SE']), ps=(p, s),
                             rP=float(r['ratio_P']), rS=float(r['ratio_S']), dem=float(r['dem_porosity'])))
        except (ValueError, KeyError):
            continue
print(f"PHYSICAL de Larrard band (beta_AM {BETA_AM}, K {K_RANGE}, c {C_RANGE}); central {CENTRAL}")
print(f"  beta_SE(P) anchored to Minnmann pure-SE Heckel; NOT fit to DEM.\n")
ins = tot = 0
dwid = []
for r in rows:
    lo, hi = band(300.0, r['am'], r['ps'], r['rP'], r['rS'])
    if lo == lo:
        tot += 1; ins += (lo - 0.5 <= r['dem'] <= hi + 0.5); dwid.append(hi - lo)
print(f"DEM @300 coverage (sanity): {ins}/{tot} = {100*ins/tot:.0f}% inside the physical band")
print(f"  median band width = {np.median(dwid):.1f}%p  (the uncertainty range)\n")

# ── TREND: porosity vs AM (rSE=0.5, 7:3) -- central +/- band, DEM medians ────
print("== TREND: porosity vs AM%  (rSE=0.5, 12:4:1, 7:3, P=300) ==")
print(f"  {'AM%':>4s} {'central':>8s} {'band':>13s} {'DEM_med':>8s}")
rse = np.array([r['rse'] for r in rows]); am = np.array([r['am'] for r in rows]); dem = np.array([r['dem'] for r in rows])
for A in (55, 62, 70, 75, 80, 85, 90, 95):
    cen = central(300.0, float(A), (7, 3), 12.0, 4.0)
    lo, hi = band(300.0, float(A), (7, 3), 12.0, 4.0)
    mm = (rse <= 0.5) & (am >= A - 4) & (am < A + 4)
    dm = float(np.median(dem[mm])) if mm.sum() else float('nan')
    print(f"  {A:4d} {cen:8.1f}  [{lo:4.1f},{hi:4.1f}]  {('%.1f' % dm) if dm == dm else '   -':>8s}")
amg = np.arange(50, 101, 5)
cur = np.array([central(300.0, float(a), (7, 3), 12.0, 4.0) for a in amg])
i = int(np.argmin(cur))
print(f"  -> central dip @ AM{amg[i]} ({cur[i]:.1f}%)  [TREND from geometry, not DEM]")

# ── pressure dependence of the dip (central) ────────────────────────────────
print("\n== dip vs pressure (central, geometry+Minnmann) ==")
for P in (100.0, 300.0, 600.0):
    cur = np.array([central(P, float(a), (7, 3), 12.0, 4.0) for a in amg])
    i = int(np.argmin(cur))
    lo, hi = band(P, float(amg[i]), (7, 3), 12.0, 4.0)
    print(f"  P={P:4.0f}  dip @ AM{amg[i]}  central {cur[i]:.1f}%  band [{lo:.1f},{hi:.1f}]")
