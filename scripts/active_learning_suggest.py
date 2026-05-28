#!/usr/bin/env python3
"""Active-learning suggester — find the design points where the σ_ionic form
has highest predictive uncertainty.  Running a sim at those points has the
highest expected information gain for the form's refinement.

METHOD
------
1. Build a candidate grid over the design space:
     P:S        ∈ {0:10, 3:7, 5:5, 7:3, 10:0}
     r_SE_um    ∈ {0.25, 0.5, 0.75, 1.0, 1.5}
     r_AM_S/P   ∈ {2, 3, 4, 5, 6} µm  (with composition-coherent pairing)
     φ_SE       ∈ {0.20, 0.25, 0.30, 0.35, 0.40}
   For each grid point, derive proxy values for CN, cov, τ, f_p from
   neighbour-interpolation on the existing corpus (since these aren't free
   design knobs — they emerge from DEM).
2. For each candidate, estimate σ_form ± PI via the Laplace posterior from
   bayesian_laplace.py (or via bootstrap from generate_comparison_plots).
3. Compute distance to the nearest corpus point (avoid suggesting points
   already in the data).
4. Rank by (PI_width × novelty_distance) — prefer high-uncertainty AND novel.

OUTPUT
------
Top 10 candidate (P:S, r_SE, r_AM, φ) cells with their predicted σ ± PI,
distance to nearest existing case, and an info-gain ranking score.

CAVEAT
------
This is a HEURISTIC — true information gain requires running each candidate
through the full LIGGGHTS pipeline.  Use it as a planner ("which next sim
gives the most form-improvement bang for the compute buck") not as a hard
ranking.

Run on WSL:
    python3 scripts/active_learning_suggest.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))

from nested_cv_sat import (load_corpus, base_log_sat, cronau_factor,
                           cblend_fit, cblend_pred, _g_phys_smooth,
                           PHIC_PROD, PHICP_F, PHICS_F, DELTA_F, PHI_C0,
                           R_CUT_AM, ALPHA_AM)
from bayesian_laplace import (p2_feat, build_design_matrix, map_and_laplace,
                              PRIOR_MEAN, PRIOR_STD)


def p2_feat_scalar(phi, r_SE, g_phys):
    pex = max(phi - PHIC_PROD, 0.0)
    return g_phys * pex**2 * max(r_SE - 0.5, 0.0)


def g_phys_scalar(p, r_AM_S, r_AM_P):
    r_AM_eff = (1.0 - p) * r_AM_S + p * r_AM_P
    return min(R_CUT_AM / max(r_AM_eff, 0.5), 1.0)**ALPHA_AM


def predict_with_PI(b_map, S_post, sigma_res, base, taus, extras):
    """Return (median_pred_sigma, PI_log_width_at_90pct) per candidate."""
    samples = np.random.default_rng(0).multivariate_normal(b_map, S_post, size=1000)
    n_cand = len(taus)
    pred_log_b = np.empty((1000, n_cand))
    for j in range(1000):
        b = samples[j]
        lt = np.log(taus)
        out = base + b[0] + b[1]*lt + b[2]*lt**2 + b[3]*extras[0] + b[4]*extras[1]
        pred_log_b[j] = out
    med = np.median(pred_log_b, axis=0)
    se = np.std(pred_log_b, axis=0, ddof=1)
    se_total = np.sqrt(se**2 + sigma_res**2)
    pi_width_log = 2 * 1.645 * se_total
    return np.exp(med), pi_width_log


def _interp_metric(metric_arr, key_arrs, target):
    """Inverse-distance-weighted interpolation of a corpus metric at a target
    design point.  Robust against sparse data; returns NaN if no neighbours."""
    n = len(metric_arr)
    if n == 0: return np.nan
    dists = np.zeros(n)
    for ka, t in zip(key_arrs, target):
        d = (ka - t)
        # Normalize roughly by range
        rng = np.nanmax(ka) - np.nanmin(ka) + 1e-9
        dists += (d / rng)**2
    dists = np.sqrt(dists)
    # k-NN avg with k=3
    order = np.argsort(dists)[:3]
    w = 1.0 / (dists[order] + 1e-6)
    return np.average(metric_arr[order], weights=w)


def main():
    print("=" * 78)
    print(" ACTIVE LEARNING — suggest next sim design points for max info-gain")
    print("=" * 78)
    a = load_corpus()
    n = len(a)
    if n < 8 or a.ndim < 2:
        print("[ABORT] corpus too small."); return
    logsf = np.log(a[:, 5]); taus = a[:, 4]
    g = _g_phys_smooth(a); fi = a[:, 19] if a.shape[1] >= 20 else np.zeros(n)
    base = base_log_sat(a, PHICP_F, PHICS_F, DELTA_F) + np.log(cronau_factor(a[:, 8]))
    extras = [p2_feat(a, g), fi]

    # MAP + posterior covariance (Laplace) — for predictive uncertainty
    b_ols = cblend_fit(base, logsf, taus, extras=extras)
    pred_ols = cblend_pred(base, taus, b_ols, extras=extras)
    sigma_res = float(np.sqrt(np.sum((logsf-pred_ols)**2)/(n-5)))
    X = build_design_matrix(base, taus, extras)
    b_map, S_post = map_and_laplace(base, logsf, X, PRIOR_MEAN, PRIOR_STD, sigma_res)
    print(f"  Posterior from n={n} cases.  Residual SE = {sigma_res:.4f} (log-space)")
    print()

    # ───── Candidate grid ─────
    PS_grid    = [0.0, 0.3, 0.5, 0.7, 1.0]     # AM_P fraction
    rSE_grid   = [0.25, 0.5, 0.75, 1.0, 1.5]    # µm
    rAM_S_grid = [2.0, 3.0, 4.0]
    rAM_P_grid = [4.0, 5.0, 6.0]
    phi_grid   = [0.22, 0.28, 0.32, 0.38]

    candidates = []
    for p_amp in PS_grid:
        for rse in rSE_grid:
            for ras in rAM_S_grid:
                for rap in rAM_P_grid:
                    for phi in phi_grid:
                        if phi <= PHI_C0: continue
                        candidates.append((p_amp, rse, ras, rap, phi))
    candidates = np.array(candidates, float)
    nc = len(candidates)
    print(f"  Candidate grid: {nc} design points")

    # ───── Interpolate emergent metrics (CN, cov, τ, f_p) from neighbours ─────
    # Corpus arrays for k-NN
    keys = [a[:, 0], a[:, 8], a[:, 17], a[:, 18], a[:, 6]]  # phi, r_SE, r_AM_S, r_AM_P, p
    cn_arr   = a[:, 1]
    cov_arr  = a[:, 2]
    tau_arr  = a[:, 4]
    fp_arr   = a[:, 3]

    cn_c, cov_c, tau_c, fp_c = [], [], [], []
    for p_amp, rse, ras, rap, phi in candidates:
        target = (phi, rse, ras, rap, p_amp)
        cn_c.append(_interp_metric(cn_arr,  keys, target))
        cov_c.append(_interp_metric(cov_arr, keys, target))
        tau_c.append(_interp_metric(tau_arr, keys, target))
        fp_c.append(_interp_metric(fp_arr,  keys, target))
    cn_c = np.array(cn_c); cov_c = np.array(cov_c)
    tau_c = np.array(tau_c); fp_c = np.array(fp_c)

    # Filter: valid + above-threshold
    valid = (cn_c > 0) & (cov_c > 0) & (tau_c > 0) & (fp_c > 0) & np.all(np.isfinite([cn_c,cov_c,tau_c,fp_c]), axis=0)
    print(f"  Candidates with valid neighbour-interp: {valid.sum()}")
    candidates = candidates[valid]
    cn_c = cn_c[valid]; cov_c = cov_c[valid]
    tau_c = tau_c[valid]; fp_c = fp_c[valid]

    # ───── Build candidate base_log + extras ─────
    base_c, p2_c, fi_c = [], [], []
    for (p_amp, rse, ras, rap, phi), cn, cov, fp in zip(candidates, cn_c, cov_c, fp_c):
        g_p = g_phys_scalar(p_amp, ras, rap)
        phic_eff = (1-g_p)*PHICP_F + g_p*PHICS_F
        pex = phi - phic_eff
        phi_eff = np.sqrt(pex**2 + (DELTA_F*g_p)**2 + 1e-12)
        # Use literal Cronau
        cron = float(cronau_factor(np.array([rse]))[0])
        bl = (np.log(3.0 * cron) + 0.5*np.log(phi_eff) + 2.0*np.log(cn)
              + 0.5*np.log(cov) + 3.0*np.log(fp))
        base_c.append(bl)
        p2_c.append(p2_feat_scalar(phi, rse, g_p))
        fi_c.append(0.0)  # assume f_intact = 1 for new sims (no fracture)
    base_c = np.array(base_c); p2_c = np.array(p2_c); fi_c = np.array(fi_c)
    extras_c = [p2_c, fi_c]

    # ───── Predict + uncertainty ─────
    med_sig, pi_width = predict_with_PI(b_map, S_post, sigma_res, base_c, tau_c, extras_c)
    pi_width_pct = (np.exp(pi_width/2) - 1) * 200  # rough ± %

    # Novelty: min distance to existing corpus (normalized)
    novelty = np.zeros(len(candidates))
    for j, (p_amp, rse, ras, rap, phi) in enumerate(candidates):
        d = np.sqrt(
            ((a[:, 0] - phi)/0.2)**2
            + ((a[:, 8] - rse)/1.5)**2
            + ((a[:, 17] - ras)/3.0)**2
            + ((a[:, 18] - rap)/3.0)**2
            + ((a[:, 6] - p_amp))**2
        )
        novelty[j] = np.nanmin(d)

    # Score: prefer high PI × high novelty
    score = pi_width * (novelty + 0.1)

    print()
    print("─" * 78)
    print(" Top 10 suggested next-sim design points")
    print(" (ranked by predictive uncertainty × novelty)")
    print("─" * 78)
    print(f"  {'rk':>3s}  {'P:S':>4s}  {'r_SE':>5s}  {'r_AM_S':>6s}  {'r_AM_P':>6s}  "
          f"{'φ':>5s}    {'σ_pred':>7s}  {'±%':>5s}  {'novelty':>7s}  {'score':>6s}")
    top = np.argsort(-score)[:10]
    for rk, j in enumerate(top, 1):
        p_amp, rse, ras, rap, phi = candidates[j]
        ps_label = f"{int(round(p_amp*10))}:{10-int(round(p_amp*10))}"
        print(f"  {rk:>3d}  {ps_label:>4s}  {rse:5.2f}  {ras:6.1f}  {rap:6.1f}  "
              f"{phi:5.3f}    {med_sig[j]:7.4f}  {pi_width_pct[j]:5.0f}  "
              f"{novelty[j]:7.3f}  {score[j]:6.3f}")
    print()
    print(f"  Interpretation: 'σ_pred ±%' = approx 90% PI half-width as a percentage.")
    print(f"  Higher novelty = farther from any existing corpus case.")
    print(f"  Run the top-ranked design first; each new sim shrinks the posterior")
    print(f"  most along the axis of highest uncertainty.")


if __name__ == '__main__':
    main()
