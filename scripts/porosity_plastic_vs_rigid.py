#!/usr/bin/env python3
"""What does PLASTIC deformation add to the porosity regression?

The base regression targets DEM eps_sphere = RIGID sphere + elastic overlap.
MPM adds TRUE plastic void-fill.  Fit the SAME physics form on:
  (R) rigid target  = dem_porosity_pct
  (P) plastic target= mpm_porosity_pct  (production SCAFFOLD MPM)
  (D) densification = dem - mpm  (how much extra the plastic flow densifies)
on the paired corpus (case_3d_collection.csv has both).

NOTE on the Furnas dip: the single `bimodal` coefficient is COLLINEAR with
bimodal_sym / sefill_x_bim, so reading it alone is misleading.  At the DATA
level the production MPM is the SCAFFOLD MPM (frozen real DEM AM positions),
so it INHERITS the DEM packing dip (6/8mAh AM82 MPM dips to a 7:3 bottom) --
plastic does NOT erase the dip here.  Only the standalone-2D free-AM MPM
erases it (frame[3]).  The ROBUST comparison is the regime-gap, not the coef.
"""
import csv, math
import numpy as np
from porosity_physics_regression import features, FEAT_KEYS, loocv_r2, se_of_solid

SRC = "docs/data/case_3d_collection.csv"

def reconstruct(d):
    """Build a design row (features() input) from the collection record.
    AM radii reconstructed from ps_label (production 6/2; mono drops one)."""
    ps = d["ps_label"].strip()
    P  = float(d["p_frac"])
    rSE = float(d["r_se"] or 0.5)
    rAMP, rAMS = 6.0, 2.0
    if ps == "10:0": rAMS = 0.0          # mono-large
    if ps == "0:10": rAMP = 0.0          # mono-small
    return dict(P=P, amwt=float(d["am_wt"]), rAMP=rAMP, rAMS=rAMS, rSE=rSE,
                por=np.nan, ps=ps)

def load_pairs(exclude_particulate=True):
    rows = []
    with open(SRC) as f:
        for d in csv.DictReader(f):
            try:
                dem = float(d["dem_porosity_pct"]); mpm = float(d["mpm_porosity_pct"])
            except (ValueError, KeyError):
                continue
            if dem <= 0 or mpm <= 0:
                continue
            # particulate cases = a SEPARATE REGIME (mono-AM_S r3, separator-like,
            # SE-rich, SE-size U-shape).  They have NO bimodal AM (P=0) so they wash
            # out the Furnas-dip term and degrade the PRODUCTION form.  Tracked
            # separately in docs/data/particulate_se_size_sweep.csv.  Exclude from
            # the production-form fit (set exclude_particulate=False to include).
            if exclude_particulate and ("particulate" in d["case"] or d["case"].startswith("input_S_")):
                continue
            # broken-sim series (CLAUDE.md: input_1mAh_100_* plate_z metadata bug ->
            # bad/negative porosity).  Excluded from the closed production form.
            if exclude_particulate and "1mAh_100" in d["case"]:
                continue
            r = reconstruct(d)
            r["dem"] = dem; r["mpm"] = mpm; r["case"] = d["case"]
            r["se_solid"] = se_of_solid(r["amwt"])
            rows.append(r)
    return rows

def fit(rows, ykey):
    X = np.array([[features(r)[k] for k in FEAT_KEYS] for r in rows])
    y = np.array([r[ykey] for r in rows])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ beta
    r2 = 1 - np.sum((y-pred)**2)/np.sum((y-y.mean())**2)
    lo, lpred = loocv_r2(X, y)
    rmse = math.sqrt(np.mean((y-pred)**2))
    return beta, r2, lo, rmse, y, lpred

rows = load_pairs()
print(f"paired corpus (DEM & MPM both): n={len(rows)} from {SRC}")
print(f"  mean DEM(rigid)={np.mean([r['dem'] for r in rows]):.1f}%  "
      f"mean MPM(plastic)={np.mean([r['mpm'] for r in rows]):.1f}%  "
      f"mean densification={np.mean([r['dem']-r['mpm'] for r in rows]):+.1f}%p")

for label, key in [("(R) RIGID  dem_eps_sphere", "dem"),
                   ("(P) PLASTIC mpm_porosity", "mpm")]:
    for r in rows: r["_y"] = r[key]
    beta, r2, lo, rmse, y, lpred = fit(rows, "_y")
    print(f"\n=== {label} ===  R2={r2:.3f}  LOOCV={lo:.3f}  RMSE={rmse:.2f}%p")
    for k, b in zip(FEAT_KEYS, beta):
        tag = " <-- Furnas dip" if k == "bimodal" else ""
        print(f"    {k:13s}={b:+8.2f}{tag}")

# --- densification target: what drives plastic void-fill? ---
for r in rows: r["_y"] = r["dem"] - r["mpm"]
beta, r2, lo, rmse, y, lpred = fit(rows, "_y")
print(f"\n=== (D) DENSIFICATION  (dem_rigid - mpm_plastic) ===")
print(f"  R2={r2:.3f}  LOOCV={lo:.3f}  RMSE={rmse:.2f}%p")
print(f"  mean +{y.mean():.2f}%p  (positive = plastic densifies below rigid)")
for k, b in zip(FEAT_KEYS, beta):
    print(f"    {k:13s}={b:+8.2f}")

# --- regime split of the rigid-vs-plastic gap (the user's regime-error) ---
print(f"\n=== rigid->plastic gap by regime ===")
buckets = {}
for r in rows:
    g = r["dem"] - r["mpm"]
    ses = r["se_solid"]
    if ses > 0.55:           reg = "SE-rich (DEM eps over-compress)"
    elif r["P"] >= 1.0:      reg = "mono-large corner"
    else:                    reg = "normal bimodal/mono-small"
    buckets.setdefault(reg, []).append(g)
for reg, gs in sorted(buckets.items(), key=lambda kv:-len(kv[1])):
    gs = np.array(gs)
    print(f"  {reg:34s} n={len(gs):3d}  mean gap={gs.mean():+5.1f}  sd={gs.std():.1f} %p")
