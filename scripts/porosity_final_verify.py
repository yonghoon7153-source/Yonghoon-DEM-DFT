#!/usr/bin/env python3
"""Adversarial re-check: is the 9-term gated form really FINAL?

(A) ablation  : drop each term -> LOOCV.  If LOOCV doesn't drop (Delta >= -0.005)
                the term is DEAD WEIGHT -> remove for parsimony.
(B) additions : forward-add new physics candidates -> keep only if Delta > +0.005.
(C) target    : gated-best vs pure-MPM vs pure-DEM (which target generalizes?).
(D) overfit   : full-R2 vs LOOCV gap; Ridge vs OLS (is k=9 on n=109 safe?).
"""
import math
import numpy as np
from porosity_physics_regression import features, FEAT_KEYS, loocv_r2, se_of_solid, sat
from porosity_plastic_vs_rigid import load_pairs

GATE = 4.0
rows = load_pairs()
for r in rows:
    g = r["dem"] - r["mpm"]
    r["best"] = r["dem"] if g > GATE else r["mpm"]

def Xy(keys, ykey="best"):
    X = np.array([[features(r)[k] for k in keys] for r in rows])
    y = np.array([r[ykey] for r in rows])
    return X, y

X, y = Xy(FEAT_KEYS)
base_lo, _ = loocv_r2(X, y)
beta, *_ = np.linalg.lstsq(X, y, rcond=None)
full_r2 = 1 - np.sum((y - X@beta)**2)/np.sum((y-y.mean())**2)
print(f"BASE: 9 terms, n={len(y)}  full-R2={full_r2:.3f}  LOOCV={base_lo:.3f}  "
      f"gap={full_r2-base_lo:.3f}")

# (A) ablation
print("\n(A) ABLATION  (drop one term):")
for drop in FEAT_KEYS:
    if drop == "const": continue
    keys = [k for k in FEAT_KEYS if k != drop]
    lo, _ = loocv_r2(*Xy(keys))
    d = lo - base_lo
    verdict = "DEAD (drop)" if d >= -0.005 else ("marginal" if d >= -0.015 else "NEEDED")
    print(f"    -{drop:13s} LOOCV {lo:.3f}  Delta {d:+.4f}  {verdict}")

# (B) additions
def extra(r, name):
    P, amwt = r["P"], r["amwt"]
    ses = se_of_solid(amwt)
    rAMP, rAMS, rSE = r["rAMP"], r["rAMS"], r["rSE"]
    rAM_eff = (P*rAMP+(1-P)*rAMS) if (rAMP>0 and rAMS>0) else (rAMP or rAMS)
    lamSE = rAM_eff/rSE if rSE>0 else 0
    B = features(r)["bimodal"]
    return {
        "se_solid_sq":  ses**2,
        "bim_x_se":     B*ses,
        "P_lin":        P,
        "P_sq":         P*P,
        "rSE_lin":      rSE,
        "ses_x_amwt":   ses*(amwt/100),
        "lamAM_sat":    sat(rAMP/rAMS) if (rAMP>0 and rAMS>0) else (1/7),
        "inv_lamSE":    1.0/lamSE if lamSE>0 else 0,
        "bim_sq":       B*B,
    }[name]

cands = ["se_solid_sq","bim_x_se","P_lin","P_sq","rSE_lin","ses_x_amwt",
         "lamAM_sat","inv_lamSE","bim_sq"]
print("\n(B) ADD candidate (on top of 9-term base):")
res = []
for c in cands:
    ex = np.array([[extra(r, c)] for r in rows])
    lo, _ = loocv_r2(np.hstack([X, ex]), y)
    res.append((c, lo-base_lo))
for c, d in sorted(res, key=lambda kv:-kv[1]):
    mark = "  <-- HELPS (add)" if d > 0.005 else ("" if d>-0.003 else " (hurts)")
    print(f"    +{c:13s} LOOCV {base_lo+d:.3f}  Delta {d:+.4f}{mark}")

# (C) target choice
print("\n(C) TARGET CHOICE (same 9-term form):")
for ykey, lbl in [("best","gated best (production)"),("mpm","pure MPM/plastic"),
                  ("dem","pure DEM/rigid")]:
    lo, _ = loocv_r2(*Xy(FEAT_KEYS, ykey))
    print(f"    {lbl:28s} LOOCV {lo:.3f}")

# (D) overfit / Ridge
print("\n(D) OVERFIT CHECK (Ridge alpha sweep, gated target):")
def ridge_loocv(X, y, alpha):
    n = len(y); preds = np.zeros(n)
    Xa = np.hstack([np.ones((n,1)), X[:,1:]])  # keep const col
    for i in range(n):
        m = np.ones(n, bool); m[i]=False
        A = Xa[m]; b = y[m]
        reg = alpha*np.eye(A.shape[1]); reg[0,0]=0
        beta = np.linalg.solve(A.T@A + reg, A.T@b)
        preds[i] = Xa[i]@beta
    return 1 - np.sum((y-preds)**2)/np.sum((y-y.mean())**2)
for a in (0.0, 0.5, 1.0, 3.0, 10.0):
    print(f"    alpha={a:5.1f}  LOOCV {ridge_loocv(X, y, a):.3f}")
print(f"\nVERDICT: gap {full_r2-base_lo:.3f} (small=not overfit); "
      f"see ablation/additions above for FINAL term set.")
