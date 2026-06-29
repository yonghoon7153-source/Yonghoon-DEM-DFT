#!/usr/bin/env python3
"""
Literature-grounded multi-dimensional porosity regression.

Connects the design parameters (P:S bimodal AM, AM:SE, radii) to porosity
through the established granular-packing physics, instead of bare linear terms:

  porosity = 1 - packing_fraction(skeleton, bimodal-fill, SE-fill)

Physics features (each tied to a reference):
  (1) Furnas/McGeary bimodal AM packing  -- McGeary 1961, de Larrard CPM
      Large AM (P) forms a skeleton (void ~0.36); small AM (S) fills the void.
      Densest at large-fraction P ~ 0.64-0.72 (small ~ void/skeleton ratio).
      Filling efficiency saturates at the critical size ratio lambda_AM = 7:1
      (small must be <= 1/7 of large to seat in the void; McGeary 0.154*d_c).
  (2) SE inter-AM filling  -- Bazzoun 2025 (small SE fills CAM voids -> eps down)
      SE seats in the AM interstices; efficiency rises with lambda_SE = r_AM/r_SE
      and with available SE volume phi_se.
  (3) skeleton baseline (RCP) + composition/size cross terms.

Regime-mixing is reported as an ERROR BAND (residual RMSE per regime), NOT by
filtering -- per user instruction "regime 섞인거 관련해서는 오차값으로 넣어줘".

Pure cloud-side OLS + LOOCV (numpy only). No GPU, no sklearn.
"""
import csv, math, sys
import numpy as np

SRC = "docs/data/dem_design_points.csv"

# --- McGeary/Furnas constants (literature, FROZEN) ---
PHI_RCP   = 0.64     # random close packing of monodisperse spheres
VOID_RCP  = 1.0 - PHI_RCP            # 0.36 skeleton void available to be filled
P_OPT     = PHI_RCP                  # optimal large-fraction ~ skeleton solid frac
LAMBDA_C  = 7.0      # McGeary critical size ratio (1/7 rule, 0.154*d_c)

# --- material densities (g/cm3) for weight->volume of the SOLID (design input,
#     POROSITY-INDEPENDENT -- never use the DEM phi_am/phi_se which leak porosity)
RHO_AM = 4.8         # single-crystal NCM811 (project convention)
RHO_SE = 2.0         # Li6PS5Cl (LPSCl) (project convention)


def se_of_solid(am_wt):
    """SE volume fraction of the SOLID from the design weight ratio + densities.
    Independent of porosity (uses input weights, not DEM box volume fractions)."""
    v_am = am_wt / RHO_AM
    v_se = (100.0 - am_wt) / RHO_SE
    return v_se / (v_am + v_se)


def sat(lmbda):
    """Size-ratio filling efficiency, 0..1, saturating at the 7:1 McGeary rule."""
    return min(max(lmbda, 0.0) / LAMBDA_C, 1.0)


def load():
    rows = []
    with open(SRC) as f:
        for d in csv.DictReader(f):
            try:
                por = float(d["dem_porosity"])
            except (ValueError, KeyError):
                continue
            rAMP = float(d["r_AM_P"] or 0)
            rAMS = float(d["r_AM_S"] or 0)
            rSE  = float(d["r_SE"]  or 0)
            amwt = float(d["AM_wt"])
            ps   = d["PS"].strip()
            # P = fraction of AM that is the LARGE (P) component, by the P:S label
            pmap = {"0:10": 0.0, "3:7": 0.3, "5:5": 0.5, "7:3": 0.7, "10:0": 1.0}
            P = pmap.get(ps, np.nan)
            if math.isnan(P):
                continue
            rows.append(dict(name=d["name"], por=por, rAMP=rAMP, rAMS=rAMS,
                             rSE=rSE, amwt=amwt, P=P, ps=ps,
                             phi_am=float(d["phi_am"]), phi_se=float(d["phi_se"])))
    return rows


def features(r):
    """Physics-motivated feature vector (literature-connected)."""
    P, amwt = r["P"], r["amwt"]
    rAMP, rAMS, rSE = r["rAMP"], r["rAMS"], r["rSE"]

    # effective AM radius (composition-weighted; mono handled by zero radius)
    if rAMP > 0 and rAMS > 0:
        rAM_eff = P * rAMP + (1 - P) * rAMS
        lam_AM  = rAMP / rAMS                 # bimodal AM size disparity
    else:
        rAM_eff = rAMP if rAMP > 0 else rAMS  # mono
        lam_AM  = 1.0                         # no disparity -> no bimodal fill

    # (1) Furnas/McGeary bimodal dip: peak fill at P_OPT, width set by mixing,
    #     amplitude gated by how far lam_AM clears the 7:1 critical ratio.
    #     Use an asymmetric skeleton-fill: f = 4*P*(1-P) reaches 1 at P=0.5;
    #     skew toward P_OPT via a parabola centered at P_OPT.
    bimodal_sym  = 4.0 * P * (1 - P)                       # symmetric mix amount
    bimodal_skew = 1.0 - ((P - P_OPT) / max(P_OPT, 1 - P_OPT))**2  # peak at P_OPT
    bimodal_fill = max(bimodal_skew, 0.0) * sat(lam_AM)    # McGeary-gated dip

    # (2) Bazzoun SE-fill: SE seats in AM interstices; rises with lam_SE & SE vol.
    #     The project DEM data shows the SE-size effect FLIPS sign with
    #     composition (CLAUDE.md size-effect note): SE-rich -> bigger SE packs
    #     denser (load-bearing, less jamming); AM-rich -> smaller SE fills the
    #     skeleton voids better (Bazzoun).  The pair {se_fill, lam_SE_sat}
    #     reproduces the crossover: net size term = sat*(b1*se_solid + b2),
    #     which changes sign with se_solid when b1,b2 have opposite signs.
    #     se_solid is DESIGN-derived (weights+densities) -> porosity-independent.
    se_solid = se_of_solid(amwt)
    lam_SE   = rAM_eff / rSE if rSE > 0 else 0.0
    se_fill  = se_solid * sat(lam_SE)                      # Bazzoun void-filling

    # (3) multi-dimensional couplings (literature: the packing mechanisms are
    #     NOT independent -- LOOCV-validated cross terms):
    #   lamSE_x_amwt  : SE-fill efficiency scales with the AM skeleton it fills
    #                   around (Bazzoun lambda x composition)
    #   sefill_x_bim  : SE seats into the voids the McGeary/Furnas bimodal AM
    #                   packing creates (de Larrard two-class coupling)
    lamSE_x_amwt = sat(lam_SE) * (amwt / 100.0)
    sefill_x_bim = se_fill * bimodal_fill

    return dict(
        const      = 1.0,
        bimodal    = bimodal_fill,        # -> lowers porosity (McGeary/Furnas)
        bimodal_sym= bimodal_sym,         # secondary symmetric mix term
        se_fill    = se_fill,             # SE vol x size-ratio (Bazzoun)
        lam_SE_sat = sat(lam_SE),         # size-ratio eff -> crossover partner
        se_solid   = se_solid,            # raw SE-of-solid (composition)
        rAM_eff    = rAM_eff,             # absolute AM size (wall/skeleton scale)
        lamSE_x_amwt = lamSE_x_amwt,      # SE-size x composition coupling
        sefill_x_bim = sefill_x_bim,      # SE-fill x bimodal-dip coupling
    )


FEAT_KEYS = ["const", "bimodal", "bimodal_sym", "se_fill", "lam_SE_sat",
             "se_solid", "rAM_eff", "lamSE_x_amwt", "sefill_x_bim"]


def design_matrix(rows, keys=FEAT_KEYS):
    X = np.array([[features(r)[k] for k in keys] for r in rows])
    y = np.array([r["por"] for r in rows])
    return X, y


def loocv_r2(X, y):
    n = len(y)
    preds = np.zeros(n)
    for i in range(n):
        m = np.ones(n, bool); m[i] = False
        beta, *_ = np.linalg.lstsq(X[m], y[m], rcond=None)
        preds[i] = X[i] @ beta
    ss_res = np.sum((y - preds)**2)
    ss_tot = np.sum((y - y.mean())**2)
    return 1 - ss_res / ss_tot, preds


def fit_report(rows, keys, label):
    X, y = design_matrix(rows, keys)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ beta
    ss_res = np.sum((y - pred)**2); ss_tot = np.sum((y - y.mean())**2)
    r2 = 1 - ss_res / ss_tot
    rmse = math.sqrt(np.mean((y - pred)**2))
    lo_r2, lo_pred = loocv_r2(X, y)
    print(f"\n=== {label} (n={len(y)}, k={len(keys)}) ===")
    print(f"  R2(full)={r2:.3f}  LOOCV R2={lo_r2:.3f}  RMSE={rmse:.2f} %p")
    for k, b in zip(keys, beta):
        print(f"    {k:12s} = {b:+.3f}")
    return beta, lo_pred, y, rows


def regime_of(r):
    """Classify each design point's porosity regime (for the error band)."""
    se_of_solid = (1 - r["amwt"] / 100.0)  # crude SE-of-solid proxy by weight
    if r["por"] < 8.0 and r["P"] <= 0.4:
        return "SE-rich over-compressed (DEM eps artifact -> use MPM)"
    if r["P"] >= 1.0 and r["amwt"] >= 85:
        return "mono-large SE-poor corner (use DEM/bracket)"
    return "normal cross-validated"


def main():
    rows = load()
    print(f"loaded {len(rows)} DEM design points from {SRC}")

    # physics-informed form
    beta, lo_pred, y, rows = fit_report(rows, FEAT_KEYS, "PHYSICS-INFORMED")

    # baseline: bare linear (P(1-P) dip + amwt + SE/sol) for comparison
    def lin_feat(r):
        se_sol = 1 - r["amwt"]/100.0
        return [1.0, r["P"], r["P"]*(1-r["P"]), r["amwt"]/100.0, se_sol, r["rSE"]]
    Xl = np.array([lin_feat(r) for r in rows]);
    lo_lin, _ = loocv_r2(Xl, y)
    print(f"\n[baseline bare-linear P+P(1-P)+amwt+SE/sol+rSE]  LOOCV R2={lo_lin:.3f}")

    # ---- regime error decomposition (the user's error band) ----
    resid = y - lo_pred
    print("\n=== REGIME ERROR BANDS (LOOCV residual RMSE per regime) ===")
    buckets = {}
    for r, e in zip(rows, resid):
        buckets.setdefault(regime_of(r), []).append(e)
    for name, errs in sorted(buckets.items(), key=lambda kv: -len(kv[1])):
        errs = np.array(errs)
        print(f"  {name:55s} n={len(errs):3d}  "
              f"bias={errs.mean():+.2f}  RMSE=±{math.sqrt(np.mean(errs**2)):.2f} %p")

    # ---- prediction grid (the "저 값들에 대한 데이터" deliverable) ----
    print("\n=== PREDICTED POROSITY GRID (physics-informed form, @300 MPa) ===")
    print("    production radii r_AM_P=6 r_AM_S=2 r_SE=1.5 um (bimodal);")
    print("    mono uses r=6 (P) or r=2 (S); error band = regime RMSE above.\n")
    band = {n: math.sqrt(np.mean(np.array(e)**2)) for n, e in buckets.items()}
    norm_band = band.get("normal cross-validated", 3.0)
    # production sizes (user spec): AM_P D=12um (r=6), AM_S D=4um (r=2),
    # SE D=1um (r=0.5).  Single size set -> sweep P:S x AM_wt only.
    rSE = 0.5
    print(f"  sizes: AM_P D12 (r6) / AM_S D4 (r2) / SE D1 (r{2*rSE:.0f}... r_SE={rSE})")
    print(f"  {'P:S':>5} {'AM_wt%':>6} | {'porosity%':>9}  {'±band':>6}  regime")
    grid_ps = [("0:10",0.0),("3:7",0.3),("5:5",0.5),("7:3",0.7),("10:0",1.0)]
    out_rows = []
    for ps_label, P in grid_ps:
        for amwt in (75, 78, 80, 82, 85, 88, 90):
            rAMP, rAMS = (6.0, 2.0)
            if P == 0.0: rAMP = 0.0          # mono small
            if P == 1.0: rAMS = 0.0          # mono large
            rr = dict(P=P, amwt=amwt, rAMP=rAMP, rAMS=rAMS, rSE=rSE,
                      por=np.nan, ps=ps_label)
            fv = features(rr)
            pred = sum(beta[i]*fv[k] for i,k in enumerate(FEAT_KEYS))
            reg = regime_of(dict(por=pred, P=P, amwt=amwt))
            short = ("over-comp" if "over" in reg else
                     "corner" if "corner" in reg else "normal")
            b = band.get(reg, norm_band)
            print(f"  {ps_label:>5} {amwt:>6} | {pred:>8.1f}  ±{b:>4.1f}  {short}")
            out_rows.append(dict(ps=ps_label, P=P, am_wt=amwt, r_AM_P=rAMP,
                                 r_AM_S=rAMS, r_SE=rSE,
                                 se_of_solid_pct=round(se_of_solid(amwt)*100,1),
                                 porosity_pred_pct=round(pred,1),
                                 err_band_pct=round(b,1), regime=short))
    # save the deliverable CSV
    outp = "docs/data/porosity_regression_predictions.csv"
    with open(outp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader(); w.writerows(out_rows)
    print(f"\n  -> saved {len(out_rows)} predictions to {outp}")
    return beta


if __name__ == "__main__":
    main()
