#!/usr/bin/env python3
"""FINAL production electrode-porosity relation (rigid + plastic combined).

Target = regime-gated BEST porosity, i.e. the value that INCLUDES SE plastic
deformation everywhere it is trustworthy and only falls back to the rigid DEM
where the plastic continuum over-compresses:

    gap = dem_eps_sphere - mpm_plastic
    if gap > +4 (mono-large corner: MPM over-compresses) -> use DEM
    else                                                  -> use MPM (plastic)

  -> normal + SE-rich  : MPM (true plastic void-fill = the physical value;
                         also rescues the DEM eps_sphere over-compression)
  -> mono-large corner : DEM (loose-truth; MPM continuum lacks the rigid
                         contact network that holds the bed open)

Fit the literature-grounded physics form (McGeary bimodal dip + Bazzoun
SE-fill crossover + the two LOOCV-validated couplings) on this target.
Report R2/LOOCV, the dip coefficient (between rigid -15.7 and plastic +1.7),
the regime error bands, and a production grid at AM D=12/4um, SE D=1um.
"""
import csv, math
import numpy as np
from porosity_physics_regression import (features, FEAT_KEYS, loocv_r2,
                                          se_of_solid)
from porosity_plastic_vs_rigid import load_pairs

GATE = 4.0   # %p; gap > GATE => mono-large corner => DEM

rows = load_pairs()
for r in rows:
    gap = r["dem"] - r["mpm"]
    if gap > GATE:
        r["best"] = r["dem"];  r["src"] = "DEM(corner)"
    else:
        r["best"] = r["mpm"];  r["src"] = "MPM(plastic)"

n_mpm = sum(1 for r in rows if r["src"].startswith("MPM"))
print(f"FINAL target: regime-gated BEST porosity  (n={len(rows)})")
print(f"  MPM(plastic) used: {n_mpm}   DEM(corner) used: {len(rows)-n_mpm}")
print(f"  mean best = {np.mean([r['best'] for r in rows]):.1f}%  "
      f"(rigid {np.mean([r['dem'] for r in rows]):.1f}, "
      f"plastic {np.mean([r['mpm'] for r in rows]):.1f})")

X = np.array([[features(r)[k] for k in FEAT_KEYS] for r in rows])
y = np.array([r["best"] for r in rows])
beta, *_ = np.linalg.lstsq(X, y, rcond=None)
pred = X @ beta
r2 = 1 - np.sum((y-pred)**2)/np.sum((y-y.mean())**2)
lo, lpred = loocv_r2(X, y)
rmse = math.sqrt(np.mean((y-pred)**2))
print(f"\n=== FINAL FORM (rigid+plastic combined) ===")
print(f"  R2={r2:.3f}  LOOCV={lo:.3f}  RMSE={rmse:.2f}%p")
for k, b in zip(FEAT_KEYS, beta):
    print(f"    {k:13s}={b:+8.2f}")

# DATA-LEVEL Furnas-dip check (robust; the single bimodal coef is collinear).
# The production MPM is the SCAFFOLD MPM (frozen real DEM AM) -> it INHERITS the
# DEM packing dip (NOT the standalone-2D-MPM which erases it).
print(f"\n=== Furnas dip in the PLASTIC (scaffold-MPM) target, AM~82 ===")
for mah in (6, 8):
    seq = sorted([(r["P"], r["mpm"]) for r in rows
                  if abs(r["amwt"]-82) <= 1.5 and r.get("ps")], key=lambda t: t[0])
    # filter by mAh via case name
    seq = [(r["P"], r["mpm"]) for r in rows
           if abs(r["amwt"]-82) <= 1.5 and f"{mah}mAh" in r["case"]]
    seq.sort(key=lambda t: t[0])
    if seq:
        s = "  ".join(f"P{p:.1f}={m:.1f}" for p, m in seq)
        print(f"  {mah}mAh: {s}   (dip retained = plastic keeps geometric packing)")

# regime error bands (the user's regime-mixing-as-error)
resid = y - lpred
print(f"\n=== REGIME ERROR BANDS (LOOCV residual) ===")
buckets = {}
for r, e in zip(rows, resid):
    ses = r["se_solid"]
    if r["src"].startswith("DEM"):     reg = "mono-large corner (DEM)"
    elif ses > 0.55:                   reg = "SE-rich (MPM)"
    else:                              reg = "normal (MPM/plastic)"
    buckets.setdefault(reg, []).append(e)
band = {}
for reg, es in sorted(buckets.items(), key=lambda kv:-len(kv[1])):
    es = np.array(es); b = math.sqrt(np.mean(es**2)); band[reg] = b
    print(f"  {reg:26s} n={len(es):3d}  bias={es.mean():+.2f}  RMSE=±{b:.2f}%p")
norm_band = band.get("normal (MPM/plastic)", rmse)

# production grid at user sizes (AM D12/4 r6/2, SE D1 r0.5)
print(f"\n=== PRODUCTION GRID (final rigid+plastic form, @300 MPa) ===")
print(f"  AM_P D12(r6) / AM_S D4(r2) / SE D1(r0.5)\n")
print(f"  {'P:S':>5} {'AM_wt%':>6} | {'porosity%':>9}  {'±band':>6}  src")
out = []
ps_grid = [("0:10",0.0),("1:9",0.1),("2:8",0.2),("3:7",0.3),("4:6",0.4),
           ("5:5",0.5),("6:4",0.6),("7:3",0.7),("8:2",0.8),("9:1",0.9),("10:0",1.0)]
for ps_label, P in ps_grid:
    for amwt in (70, 72.5, 75, 77.5, 80, 82.5, 85, 87.5, 90):
        rAMP, rAMS = (6.0, 2.0)
        if P == 0.0: rAMP = 0.0
        if P == 1.0: rAMS = 0.0
        rr = dict(P=P, amwt=amwt, rAMP=rAMP, rAMS=rAMS, rSE=0.5, por=np.nan, ps=ps_label)
        fv = features(rr)
        p = sum(beta[i]*fv[k] for i, k in enumerate(FEAT_KEYS))
        # which regime/band: mono-large hi-AM = corner, low-AM = SE-rich
        ses = se_of_solid(amwt)
        if P >= 1.0 and amwt >= 85:  reg, src = "mono-large corner (DEM)", "DEM"
        elif ses > 0.55:             reg, src = "SE-rich (MPM)", "MPM"
        else:                        reg, src = "normal (MPM/plastic)", "MPM"
        b = band.get(reg, norm_band)
        print(f"  {ps_label:>5} {amwt:>6} | {p:>8.1f}  ±{b:>4.1f}  {src}")
        out.append(dict(ps=ps_label, P=P, am_wt=amwt, r_AM_P=rAMP, r_AM_S=rAMS,
                        r_SE=0.5, se_of_solid_pct=round(ses*100,1),
                        porosity_pct=round(p,1), err_band_pct=round(b,1),
                        source=src))
outp = "docs/data/porosity_production_final.csv"
with open(outp, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
    w.writeheader(); w.writerows(out)
print(f"\n  -> saved {len(out)} predictions to {outp}")
