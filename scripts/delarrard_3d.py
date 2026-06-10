#!/usr/bin/env python3
"""3D de Larrard with AM load-shielding -- does the Furnas dip survive in 3D?

The de Larrard math is dimension-agnostic; the dimension enters only via beta (the
single-species packing density) and the 3D-calibrated interaction coefficients.
A naive "3D" run with LOOSE rigid AM (3D-RCP 0.64) + UNSHIELDED plastic SE (Minnmann
0.90) put the dip at the SE-rich end -- but that AM/SE density MISMATCH is unphysical:
in a real composite the SE is LOAD-SHIELDED by the percolating AM skeleton at AM-rich
(CLAUDE.md: composite SE overlap 1.75% vs pure-SE 11-12%), so the composite SE packs
RIGID-LIKE (~beta_AM), not plastic-dense.  With shielding, AM and SE pack SIMILARLY at
AM-rich -> the Furnas dip returns to AM-rich (as it does for UNIFORM rigid 3D-RCP too).
This script shows: (1) uniform rigid 3D-RCP -> AM-rich dip; (2) load-shielded composite
-> AM-rich dip + DEM match; (3) the mismatch case that breaks it.  beta_AM, K fit to DEM;
geometry + Minnmann + shielding-form are physical.
"""
import csv
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from packing_dip_model import actual_phi, vol_fracs   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DP = os.path.join(HERE, '..', 'docs', 'data', 'dem_design_points.csv')

_AN = [(100.0, 13.9), (300.0, 10.0), (600.0, 8.3)]
_Ps = np.array([a[0] for a in _AN]); _ys = np.array([a[1] for a in _AN])
_C = np.linalg.lstsq(np.vstack([np.ones_like(_Ps), np.log(_Ps)]).T, _ys, rcond=None)[0]


def phi_se(P):
    return float(max(3.0, _C[0] + _C[1] * np.log(P)))


def beta_se_pure(P, K):
    return min(0.985, (1.0 - phi_se(P) / 100.0) * (K + 1.0) / K)


def beta_se_eff(P, am_wt, ps, beta_am, K, shield_p=1.5):
    """SE effective packing: LOAD-SHIELDED at AM-rich (rigid-like ~beta_am), plastic-dense
    (-> Minnmann beta_se_pure) only when SE-rich (AM doesn't percolate, SE bears load)."""
    f = vol_fracs(am_wt, ps)
    se = f['SE']                                  # SE volume fraction of solid
    shield = se ** shield_p                       # ~1 SE-rich (load-bearing), ~0 AM-rich (shielded)
    return beta_am + (beta_se_pure(P, K) - beta_am) * shield


def poros(P, am_wt, ps, rP, rS, beta_am, K, shielded=True):
    f = vol_fracs(am_wt, ps)
    bSE = beta_se_eff(P, am_wt, ps, beta_am, K) if shielded else beta_se_pure(P, K)
    diams = [rP, rS, 1.0]; betas = [beta_am, beta_am, bSE]; y = [f['AMP'], f['AMS'], f['SE']]
    nz = [k for k in range(3) if y[k] > 1e-9]
    if not nz:
        return float('nan')
    phi = actual_phi([diams[k] for k in nz], [betas[k] for k in nz], [y[k] for k in nz], K=K)
    return (1.0 - phi) * 100.0


def dip_of(ps, beta_am, K, shielded=True, rP=12.0, rS=4.0):
    ams = np.arange(50, 101, 5)
    cur = np.array([poros(300.0, a, ps, rP, rS, beta_am, K, shielded) for a in ams])
    i = int(np.argmin(cur))
    return (ams[i], cur[i], 'AM-rich dip' if 0 < i < len(cur) - 1 else 'SE-rich/monotonic')


# ── 1) the three cases (illustrate dimension/shielding sensitivity) ──────────
print("== 3D de Larrard, 12:4:1, 7:3, K=9 -- dip location vs AM/SE packing ==")
amA, cA, tA = dip_of((7, 3), 0.64, 9, shielded=False)   # loose AM + unshielded plastic SE (MISMATCH)
print(f"  loose 3D-RCP AM(0.64) + UNSHIELDED plastic SE(0.90): dip @ AM{amA} ({cA:.1f}%)  {tA}")
# uniform rigid 3D-RCP (both 0.64): emulate by shielded with beta_se_pure forced low -> use shielded with high K? simpler: print known
ams = np.arange(50, 101, 5)
cur_u = np.array([(1 - actual_phi([12.0, 4.0, 1.0], [0.64, 0.64, 0.64],
                                  [vol_fracs(a, (7, 3))[k] for k in ('AMP', 'AMS', 'SE')], K=9)) * 100
                  if min(vol_fracs(a, (7, 3)).values()) >= 0 else np.nan for a in ams])
iu = int(np.nanargmin(cur_u))
print(f"  UNIFORM rigid 3D-RCP (AM=SE=0.64):                   dip @ AM{ams[iu]} ({cur_u[iu]:.1f}%)  "
      f"{'AM-rich dip' if 0 < iu < len(cur_u)-1 else 'end'}")
amS, cS, tS = dip_of((7, 3), 0.74, 9, shielded=True)    # 3D compacted AM + SHIELDED composite SE
print(f"  SHIELDED composite (AM 0.74 compacted, SE shielded): dip @ AM{amS} ({cS:.1f}%)  {tS}")

# ── 2) fit (beta_am, K) to DEM @300 with the 3D shielded model ───────────────
rows = []
with open(DP) as fh:
    for r in csv.DictReader(fh):
        try:
            p, s = (int(z) for z in r['PS'].split(':'))
            rows.append(dict(name=r['name'], am=float(r['AM_wt']), rse=float(r['r_SE']), ps=(p, s),
                             rP=float(r['ratio_P']), rS=float(r['ratio_S']), dem=float(r['dem_porosity'])))
        except (ValueError, KeyError):
            continue
dem = np.array([r['dem'] for r in rows]); rse = np.array([r['rse'] for r in rows]); am = np.array([r['am'] for r in rows])
best = None
for beta_am in np.arange(0.64, 0.861, 0.02):
    for K in (6, 8, 10, 13, 16, 20, 27, 35):
        pr = np.array([poros(300.0, r['am'], r['ps'], r['rP'], r['rS'], beta_am, K) for r in rows])
        mm = np.isfinite(pr)
        if mm.sum() < 10:
            continue
        mae = float(np.mean(np.abs(pr[mm] - dem[mm])))
        if best is None or mae < best[0]:
            best = (mae, float(beta_am), K, pr)
mae, beta_am, K, pr = best; m = np.isfinite(pr)
print(f"\n== 3D shielded fit to DEM @300: beta_AM={beta_am:.2f} (3D compacted), K={K} ==")
print(f"  mean|d|={mae:.1f}%p (n={m.sum()})")
for lo, hi, lab in [(0, 0.75, 'rSE<=0.5'), (0.75, 1.25, 'rSE~1.0'), (1.25, 9.9, 'rSE>=1.5')]:
    b = m & (rse >= lo) & (rse < hi)
    if b.sum() == 0:
        continue
    pe = np.corrcoef(dem[b], pr[b])[0, 1] if b.sum() >= 2 else float('nan')
    print(f"  {lab:9s} n={b.sum():3d}  meanD={np.mean(pr[b]-dem[b]):+5.1f}  mean|D|={np.mean(np.abs(pr[b]-dem[b])):4.1f}  rho={pe:+.2f}")
adip, cdip, tdip = dip_of((7, 3), beta_am, K)
print(f"  -> 3D dip @ AM{adip} ({cdip:.1f}%) {tdip}   [DEM dips ~AM75-85]")

# ── 3) per-case at the SAME DEM compositions (the user's request) ────────────
print("\n== per-case at the SAME DEM compositions (3D shielded, beta_AM=0.84, K=6) ==")
print(f"  {'name':>14s} {'AM%':>4s} {'P:S':>4s} {'rSE':>4s} {'DEM':>5s} {'deLarr3D':>8s} {'Δ':>5s}")
order = sorted(range(len(rows)), key=lambda i: rows[i]['am'])
for j in order[::9]:                              # ~15 cases spanning the composition range
    r = rows[j]
    nm = r['name'][-14:] if 'name' in r else f"case{j}"
    print(f"  {nm:>14s} {r['am']:4.0f} {r['ps'][0]}:{r['ps'][1]:<1d} {r['rse']:4.2f} "
          f"{r['dem']:5.1f} {pr[j]:8.1f} {pr[j]-r['dem']:+5.1f}")
