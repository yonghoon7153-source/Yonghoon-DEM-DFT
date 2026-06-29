#!/usr/bin/env python3
"""Explore honest levers to raise the porosity-regression R2.

(1) seed-noise FLOOR: average sibling seeds (identical design) -> refit.  The
    gap between raw-LOOCV and sibling-averaged-R2 is the irreducible DEM
    stochastic packing noise (a form ceiling, not a form deficiency).
(2) physics INTERACTION terms (multi-dimensional couplings): test each
    addition's LOOCV gain on top of the leak-free base form.
"""
import csv, math
import numpy as np
from porosity_physics_regression import (load, features, FEAT_KEYS,
                                          design_matrix, loocv_r2, se_of_solid, sat)

rows = load()
X, y = design_matrix(rows, FEAT_KEYS)
base_lo, _ = loocv_r2(X, y)
print(f"base leak-free form: n={len(y)} k={len(FEAT_KEYS)} LOOCV={base_lo:.3f}")

# ---------- (1) seed-noise floor ----------
groups = {}
for r in rows:
    key = (r["rAMP"], r["rAMS"], r["rSE"], round(r["amwt"]), r["ps"])
    groups.setdefault(key, []).append(r["por"])
multi = {k: v for k, v in groups.items() if len(v) >= 2}
within = []
for k, v in multi.items():
    v = np.array(v); within.append(v.std(ddof=1))
print(f"\n[seed-noise floor] {len(multi)} designs w/ >=2 seeds "
      f"({sum(len(v) for v in multi.values())} cases)")
print(f"  median within-design sigma = {np.median(within):.2f} %p  "
      f"mean = {np.mean(within):.2f} %p")
print(f"  -> a form predicting the design MEAN perfectly still has "
      f"RMSE ~ {np.mean(within):.2f} %p from per-seed scatter")

# sibling-averaged fit: collapse each design to its mean, refit
agg = {}
for r in rows:
    key = (r["rAMP"], r["rAMS"], r["rSE"], round(r["amwt"], 1), r["ps"])
    agg.setdefault(key, []).append(r)
arows = []
for k, rs in agg.items():
    rr = dict(rs[0]); rr["por"] = float(np.mean([x["por"] for x in rs]))
    arows.append(rr)
Xa, ya = design_matrix(arows, FEAT_KEYS)
alo, _ = loocv_r2(Xa, ya)
print(f"  sibling-AVERAGED LOOCV (n={len(ya)} designs) = {alo:.3f}  "
      f"(<- ceiling at this corpus once seed noise removed)")

# ---------- (2) physics interaction terms ----------
def fx(r):
    f = features(r)
    P = r["P"]; amwt = r["amwt"]
    ses = se_of_solid(amwt)
    rAMP, rAMS, rSE = r["rAMP"], r["rAMS"], r["rSE"]
    rAM_eff = (P*rAMP + (1-P)*rAMS) if (rAMP>0 and rAMS>0) else (rAMP or rAMS)
    lamSE = rAM_eff/rSE if rSE>0 else 0.0
    return dict(
        # --- candidate multi-dimensional couplings (each physics-motivated) ---
        bim_x_se   = f["bimodal"] * ses,        # dip locked by SE void-fill
        bim_x_amwt = f["bimodal"] * (amwt/100), # dip deepens with AM skeleton
        sefill_x_bim = f["se_fill"] * f["bimodal"],   # SE fills bimodal voids
        se_solid_sq = ses**2,                   # nonlinear SE content
        P_lin      = P,                         # asymmetry beyond parabola
        P_sq       = P*P,
        lamSE_x_amwt = sat(lamSE) * (amwt/100), # SE-size x composition (alt form)
        rSE_lin    = rSE,                       # raw SE size
        rAMeff_sq  = rAM_eff**2,
    )

cands = list(fx(rows[0]).keys())
print(f"\n[interaction screen] base LOOCV {base_lo:.3f}; "
      f"Delta from adding each single term:")
results = []
for c in cands:
    extra = np.array([[fx(r)[c]] for r in rows])
    Xc = np.hstack([X, extra])
    lo, _ = loocv_r2(Xc, y)
    results.append((c, lo - base_lo))
for c, d in sorted(results, key=lambda kv: -kv[1]):
    mark = "  <-- helps" if d > 0.003 else ("" if d > -0.003 else "  (hurts)")
    print(f"    +{c:16s} LOOCV {base_lo+d:.3f}  Delta {d:+.4f}{mark}")

# greedy forward add of the helpful ones
helpful = [c for c, d in sorted(results, key=lambda kv: -kv[1]) if d > 0.003]
print(f"\n[greedy forward] adding helpful terms in order:")
Xg = X.copy(); curr = base_lo; added = []
for c in helpful:
    extra = np.array([[fx(r)[c]] for r in rows])
    Xt = np.hstack([Xg, extra])
    lo, _ = loocv_r2(Xt, y)
    if lo > curr + 0.001:
        Xg = Xt; curr = lo; added.append(c)
        print(f"    + {c:16s} -> LOOCV {curr:.3f}")
    else:
        print(f"    x {c:16s} (no marginal gain, skip)")
print(f"\nFINAL augmented: base7 + {added}")
print(f"  LOOCV {curr:.3f}  (base {base_lo:.3f}, +{curr-base_lo:.3f})")
print(f"  sibling-averaged ceiling was {alo:.3f}")
