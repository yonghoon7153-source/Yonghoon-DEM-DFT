#!/usr/bin/env python3
"""UNIFIED porosity form — production (bimodal) + particulate/S (mono-small
separator) in ONE equation.

The production form (porosity_final_production.py) excludes particulate because
(a) the collection CSV reconstructs AM radii (6/2) which is wrong for the
particulate r_AM_S=3/4, and (b) the SE-size effect is a COMPOSITION-DEPENDENT
U-shape (SE-rich: U with min at lambda=r_AM/r_SE~3 -- too-small SE wastes into
SE-SE voids; SE-poor: monotonic small-better -- Bazzoun fill of sparse voids)
that the linear rSE term cannot span.

Unification fixes both:
  - use the ACTUAL r_AM_S for particulate/S (from the sweep tracking CSV),
  - add a COMPOSITION-GATED lambda-U term: penalty for deviating from lambda~3
    that is active only when SE-rich (se_of_solid > ~0.4), 0 for SE-poor.

Tradeoff: one form for the whole design space is LESS accurate on production
than the specialised production-only form (it spends DOF spanning particulate).
As more particulate / E-variant samples land, the gated-U + (future) E_SE term
sharpen and the unified LOOCV rises.  Run to refit on the current corpus.
"""
import csv, math
import numpy as np
from porosity_physics_regression import features, FEAT_KEYS, loocv_r2, se_of_solid
from porosity_plastic_vs_rigid import load_pairs

LAM_OPT = 3.0          # de Larrard/McGeary-like SE-fill optimum size ratio
SE_GATE = 0.40         # se_of_solid above which the SE-rich U-penalty turns on

def real_rAMS():
    """actual r_AM_S for particulate/S mono-small cases (collection reconstructs 6/2)."""
    t = {}
    with open("docs/data/particulate_se_size_sweep.csv") as f:
        for l in f:
            if l.startswith(("#", "case")):
                continue
            p = l.split(","); t[p[0]] = float(p[2])
    return t

def build():
    track = real_rAMS()
    rows = load_pairs(exclude_particulate=False)          # FULL corpus
    for r in rows:
        g = r["dem"] - r["mpm"]; r["best"] = r["dem"] if g > 4 else r["mpm"]
        r["ses"] = se_of_solid(r["amwt"])
        if r["case"] in track and r["P"] == 0.0:          # fix mono-small geometry
            r["rAMS"] = track[r["case"]]; r["rAMP"] = 0.0
        rAM = (r["P"]*r["rAMP"] + (1-r["P"])*r["rAMS"]) if (r["rAMP"] > 0 and r["rAMS"] > 0) \
              else (r["rAMP"] or r["rAMS"])
        r["lnlam"] = math.log(rAM / r["rSE"]) if r["rSE"] > 0 else 0.0
        r["is_part"] = ("particulate" in r["case"]) or r["case"].startswith("input_S_")
    return rows

def feat_unified(r):
    """base 9-term + composition-gated lambda-U (SE-rich only)."""
    v = [features(r)[k] for k in FEAT_KEYS]
    v.append(max(r["ses"] - SE_GATE, 0.0) * (r["lnlam"] - math.log(LAM_OPT))**2)
    return v

def loocv(rows, fn):
    y = np.array([r["best"] for r in rows]); n = len(rows)
    X = np.array([fn(r) for r in rows]); pr = np.zeros(n)
    for i in range(n):
        m = np.ones(n, bool); m[i] = False
        b, *_ = np.linalg.lstsq(X[m], y[m], rcond=None); pr[i] = X[i] @ b
    r2 = 1 - np.sum((y-pr)**2)/np.sum((y-y.mean())**2)
    return r2, pr, y

if __name__ == "__main__":
    rows = build()
    part = np.array([r["is_part"] for r in rows])
    base = lambda r: [features(r)[k] for k in FEAT_KEYS]
    r2b, _, _ = loocv(rows, base)
    r2u, pr, y = loocv(rows, feat_unified)
    print(f"UNIFIED porosity form — full corpus n={len(rows)} "
          f"(production {(~part).sum()} + particulate/S {part.sum()})")
    print(f"  base 9-term (no U):           LOOCV={r2b:.3f}")
    print(f"  + composition-gated lambda-U: LOOCV={r2u:.3f}")
    for lbl, msk in [("production", ~part), ("particulate/S", part)]:
        rmse = math.sqrt(np.mean((y[msk]-pr[msk])**2))
        print(f"  per-regime RMSE {lbl:14s} ={rmse:.2f} %p (n={msk.sum()})")
    # report the fitted unified coefficients
    X = np.array([feat_unified(r) for r in rows]); y = np.array([r["best"] for r in rows])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    print("  coefficients (base9 + gatedU):")
    for k, b in zip(FEAT_KEYS + ["gatedU(se>0.4)*(lnλ-ln3)^2"], beta):
        print(f"    {k:28s}={b:+8.2f}")
    print(f"\n  NOTE: unified LOOCV < production-only (~0.6) -- one form for the whole "
          f"space costs production accuracy.  More particulate/E samples sharpen it.")
