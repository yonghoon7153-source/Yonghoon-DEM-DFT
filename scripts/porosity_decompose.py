#!/usr/bin/env python3
"""Per-term DECOMPOSITION of the final production porosity.

For each grid condition, porosity = sum of (coef_k * feature_k).  Print each
term's CONTRIBUTION in %p (so the components literally add up to the porosity),
and save a full CSV.  Reuses the same fit as porosity_final_production.py.
"""
import csv
import numpy as np
from porosity_physics_regression import features, FEAT_KEYS, se_of_solid
from porosity_plastic_vs_rigid import load_pairs

# refit the final (regime-gated best) form -> same beta as production
rows = load_pairs()
for r in rows:
    g = r["dem"] - r["mpm"]
    r["best"] = r["dem"] if g > 4 else r["mpm"]
X = np.array([[features(r)[k] for k in FEAT_KEYS] for r in rows])
y = np.array([r["best"] for r in rows])
beta, *_ = np.linalg.lstsq(X, y, rcond=None)
B = dict(zip(FEAT_KEYS, beta))

# physical grouping for readability
GROUPS = [
    ("const",         ["const"]),
    ("McGeary dip",   ["bimodal", "bimodal_sym"]),
    ("Bazzoun SE",    ["se_fill", "lam_SE_sat", "se_solid"]),
    ("size",          ["rAM_eff"]),
    ("couplings",     ["lamSE_x_amwt", "sefill_x_bim"]),
]

print("coefficients (porosity %p per unit feature):")
for k in FEAT_KEYS:
    print(f"    {k:13s} = {B[k]:+8.2f}")

def contribs(P, amwt, rAMP, rAMS, rSE, ps):
    rr = dict(P=P, amwt=amwt, rAMP=rAMP, rAMS=rAMS, rSE=rSE, por=np.nan, ps=ps)
    fv = features(rr)
    return {k: B[k] * fv[k] for k in FEAT_KEYS}

ps_grid = [("0:10",0.0),("1:9",0.1),("2:8",0.2),("3:7",0.3),("4:6",0.4),
           ("5:5",0.5),("6:4",0.6),("7:3",0.7),("8:2",0.8),("9:1",0.9),("10:0",1.0)]

# full CSV: every (P:S, AM_wt) with per-term contribution
out = []
for ps, P in ps_grid:
    for amwt in (75, 78, 80, 82, 85, 88, 90):
        rAMP, rAMS = 6.0, 2.0
        if P == 0.0: rAMP = 0.0
        if P == 1.0: rAMS = 0.0
        c = contribs(P, amwt, rAMP, rAMS, rSE=0.5, ps=ps)
        row = dict(ps=ps, am_wt=amwt)
        for k in FEAT_KEYS:
            row[f"c_{k}"] = round(c[k], 2)
        row["porosity_pct"] = round(sum(c.values()), 1)
        out.append(row)
outp = "docs/data/porosity_decomposition.csv"
with open(outp, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
    w.writeheader(); w.writerows(out)

# pretty print: AM_wt=82 column, all P:S, grouped contributions
print(f"\n=== component breakdown @ AM_wt=82, r=6/2/0.5 (values add to porosity) ===")
hdr = f"  {'P:S':>5} | " + " ".join(f"{g[0]:>11}" for g in GROUPS) + f" | {'porosity':>8}"
print(hdr)
for ps, P in ps_grid:
    rAMP, rAMS = 6.0, 2.0
    if P == 0.0: rAMP = 0.0
    if P == 1.0: rAMS = 0.0
    c = contribs(P, 82, rAMP, rAMS, rSE=0.5, ps=ps)
    gvals = [sum(c[k] for k in keys) for _, keys in GROUPS]
    tot = sum(c.values())
    print(f"  {ps:>5} | " + " ".join(f"{v:>+11.1f}" for v in gvals) +
          f" | {tot:>8.1f}")
print(f"\n  -> full 77-row per-term CSV: {outp}")
