#!/usr/bin/env python3
"""Rigorous overfitting stress-tests for a candidate 62:38 term.

Used after nested_cv_sat.py + sat_exp_62_38_search.py pick a finalist
feature.  This script runs FOUR independent overfitting checks on that
feature against the SAT × Cronau base:

  1. PERMUTATION NULL  — shuffle log σ 1000× and recompute LOOCV β and
     Δ_LOOCV.  If the real Δ is in the top 1% of the null distribution
     (p<0.01) the signal can't be explained by chance.
  2. BOOTSTRAP β CI    — resample cases with replacement N times, refit
     β each draw.  95% CI excluding 0 = β is statistically real.
  3. PER-FOLD STABILITY — mean / std / CV% of β across LOO folds.
     CV% < 30% = β isn't whip-sawing case-by-case (no leverage points).
  4. HALF-SPLIT GENERALIZATION — fit β on a random 50% subset, predict
     the held-out 50%.  Repeat 200× with different splits; the train→test
     R² shift should be small AND the held-out β consistent.

Plus:
  5. AIC / BIC      — does adding β actually improve the information
     criterion (penalizing the extra parameter)?

Default candidate = E:  (φ−φc)²·r_SE  (the ungated power-coupling winner).
Run with another feature:  python3 scripts/stress_test_62_38_term.py <NAME>
where <NAME> is one of: E, D, L, M2, F, O, O2, P, P2, Q, Q2, R
(matching the tags in sat_exp_62_38_search.py).
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
from nested_cv_sat import (load_corpus, base_log_sat, cblend_fit, cblend_pred,
                           loocv_with_feat, cronau_factor,
                           PHICP_F, PHICS_F, DELTA_F, K_PS, P_C)
from sat_exp_62_38_search import _make_features


# Optional readable tags → feature dict (built by _make_features) lookup.
TAG_MAP = {
    "E":  "E_(φ-φc)²·r_SE",
    "D":  "D_(φ-φc)·r_SE",
    "L":  "L_g_hi·g_010·log(1+1·(φ-0.30)·r_SE)",
    "M2": "M2_g_hi·g_010·(φ-φc)·r_SE",
    "F":  "F_exp(3.0·φ·r_SE)-1",
    "O":  "O_r_SE·log(φ_eff)  [φ_eff exponent ~ r_SE]",
    "O2": "O2_(r_SE-0.5)·log(φ_eff)  [centered at Cronau ref]",
    "P":  "P_(φ-φc)·(r_SE-0.5)+  [Cronau high-r_SE arm]",
    "P2": "P2_(φ-φc)²·(r_SE-0.5)+ [Cronau, quadratic-φ]",
    "Q":  "Q_r_SE·log(CN)  [CN exponent ~ r_SE]",
    "Q2": "Q2_(r_SE-0.5)·log(CN)  [centered]",
    "R":  "R_r_SE·log(cov)  [cov exponent ~ r_SE]",
}


def _beta_of(base, logsf, taus, sf):
    """Single-shot OLS β on the post-C_blend residual (matches loocv_with_feat
    inner step but without the leave-one-out)."""
    b = cblend_fit(base, logsf, taus)
    resid = logsf - cblend_pred(base, taus, b)
    sm = sf.mean(); sc = sf - sm
    d = float(np.dot(sc, sc))
    return float(np.dot(sc, resid)/d) if d > 1e-12 else 0.0


def _loocv_r2_const(base, logsf, taus):
    """LOOCV R² of the C_blend-only base (no extra term) — comparison reference."""
    n = len(taus); ss = np.sum((logsf-logsf.mean())**2); sse = 0.0
    for i in range(n):
        m = np.ones(n, bool); m[i] = False
        b = cblend_fit(base[m], logsf[m], taus[m])
        pi = cblend_pred(base[i:i+1], taus[i:i+1], b)[0]
        sse += (logsf[i]-pi)**2
    return 1 - sse/ss


def _per_fold_betas(base, logsf, taus, sf):
    """The β fit inside each LOO fold (the per-fold OLS coefficients)."""
    n = len(taus); betas = []
    for i in range(n):
        m = np.ones(n, bool); m[i] = False
        b = cblend_fit(base[m], logsf[m], taus[m])
        resid_tr = logsf[m] - cblend_pred(base[m], taus[m], b)
        sm = sf[m].mean(); sc = sf[m] - sm
        d = float(np.dot(sc, sc))
        b = float(np.dot(sc, resid_tr)/d) if d > 1e-12 else 0.0
        betas.append(b)
    return np.array(betas)


def run(name="E", n_perm=1000, n_boot=2000, n_half=200, seed=0):
    a = load_corpus()
    n = len(a)
    if n < 20:
        print(f"[ABORT] only {n} cases."); return
    logsf = np.log(a[:, 5]); taus = a[:, 4]
    rng = np.random.default_rng(seed)

    base = base_log_sat(a, PHICP_F, PHICS_F, DELTA_F) + np.log(cronau_factor(a[:, 8]))
    lo_ref = _loocv_r2_const(base, logsf, taus)

    feats = _make_features(a)
    if name not in TAG_MAP:
        print(f"[ABORT] unknown candidate '{name}'. Choices: {list(TAG_MAP)}"); return
    tag = TAG_MAP[name]; sf = feats[tag]
    if not np.all(np.isfinite(sf)) or np.std(sf) < 1e-12:
        print(f"[ABORT] feature '{tag}' degenerate."); return

    # OBSERVED values
    lo_obs, beta_obs_mean = loocv_with_feat(base, logsf, taus, sf)
    delta_obs = lo_obs - lo_ref
    beta_obs_ss = _beta_of(base, logsf, taus, sf)
    fold_betas = _per_fold_betas(base, logsf, taus, sf)

    print("=" * 78)
    print(f"Overfitting stress-tests for candidate {name}: {tag}")
    print(f"  n={n}  base (SAT×Cronau) LOOCV = {lo_ref:.4f}")
    print("=" * 78)
    print(f"OBSERVED:  LOOCV+β = {lo_obs:.4f}   Δ = {delta_obs:+.4f}   "
          f"single-shot β = {beta_obs_ss:+.3f}   LOO-mean β = {beta_obs_mean:+.3f}")
    print()

    # 1) PERMUTATION NULL — shuffle the FEATURE, not the target.
    # FIX: shuffling y breaks alignment with base; C_blend then fits noise →
    # huge null Δ artifact (NOT what we want).  Correct test = permute sf only,
    # keep y/base/taus aligned; C_blend fit is unaffected; β refits on shuffled sf.
    print(f"[1] PERMUTATION NULL  (n_perm={n_perm}, shuffle FEATURE, β refit)")
    b_ref = cblend_fit(base, logsf, taus)
    resid_ref = logsf - cblend_pred(base, taus, b_ref)
    sse_ref_const = float(np.sum(resid_ref**2))
    null_betas = np.empty(n_perm); null_deltas = np.empty(n_perm)
    for k in range(n_perm):
        sf_perm = sf[rng.permutation(n)]
        sm = sf_perm.mean(); sc = sf_perm - sm
        d = float(np.dot(sc, sc))
        b_k = float(np.dot(sc, resid_ref)/d) if d > 1e-12 else 0.0
        # in-sample SSE reduction → LOOCV-comparable Δ (since C_blend doesn't
        # change under feature-only permutation)
        pred_perm_resid = b_k * (sf_perm - sm)
        sse_with = float(np.sum((resid_ref - pred_perm_resid)**2))
        null_betas[k] = b_k
        null_deltas[k] = (sse_ref_const - sse_with) / float(np.sum((logsf - logsf.mean())**2))
    # observed in-sample equivalent (same metric)
    sm0 = sf.mean(); sc0 = sf - sm0
    d0 = float(np.dot(sc0, sc0))
    b0 = float(np.dot(sc0, resid_ref)/d0) if d0 > 1e-12 else 0.0
    sse_with_obs = float(np.sum((resid_ref - b0*(sf - sm0))**2))
    delta_obs_inS = (sse_ref_const - sse_with_obs) / float(np.sum((logsf - logsf.mean())**2))
    p_beta = float((np.abs(null_betas) >= abs(b0)).mean())
    p_delta = float((null_deltas >= delta_obs_inS).mean())
    print(f"    null |β| 99th pctile = {np.quantile(np.abs(null_betas), 0.99):.3f}   "
          f"|observed β| = {abs(b0):.3f}")
    print(f"    p(|β_null| ≥ |β_obs|) = {p_beta:.4f}")
    print(f"    null Δ_R² 99th pctile = {np.quantile(null_deltas, 0.99):+.4f}   "
          f"observed (in-sample) Δ_R² = {delta_obs_inS:+.4f}")
    print(f"    p(Δ_null ≥ Δ_obs)    = {p_delta:.4f}")
    v1 = "PASS — feature/target association not explained by chance" if (p_beta < 0.01 and p_delta < 0.01) else "FAIL"
    print(f"    VERDICT: {v1}")

    # 2) BOOTSTRAP β CI — vanilla AND stratified (so corner cases aren't dropped).
    # Plain bootstrap is unfair for a corner-driven β: with n_corner=4 in n=91,
    # ~16% of bootstrap samples have ZERO corner cases → β collapses → CI very
    # wide.  Stratified bootstrap protects the corner subset (always sampled).
    print(f"\n[2] BOOTSTRAP 95% CI for β  (n_boot={n_boot})")
    rse_arr = a[:, 8]; p_arr = a[:, 6]; phi_arr = a[:, 0]
    idx_corner = np.where((p_arr < 0.05) & (phi_arr > 0.30) &
                          np.isfinite(rse_arr) & (rse_arr >= 1.0))[0]
    idx_bulk = np.array([i for i in range(n) if i not in set(idx_corner)])
    n_c, n_b = len(idx_corner), len(idx_bulk)
    boot_v = np.empty(n_boot); boot_s = np.empty(n_boot)
    for k in range(n_boot):
        # vanilla
        idx_v = rng.integers(0, n, n)
        # stratified: resample within each stratum to preserve corner presence
        idx_s = np.concatenate([
            idx_corner[rng.integers(0, n_c, n_c)] if n_c > 0 else np.array([], int),
            idx_bulk[rng.integers(0, n_b, n_b)],
        ])
        try: boot_v[k] = _beta_of(base[idx_v], logsf[idx_v], taus[idx_v], sf[idx_v])
        except Exception: boot_v[k] = np.nan
        try: boot_s[k] = _beta_of(base[idx_s], logsf[idx_s], taus[idx_s], sf[idx_s])
        except Exception: boot_s[k] = np.nan
    for label, arr in (("vanilla   ", boot_v), ("stratified", boot_s)):
        ok = arr[np.isfinite(arr)]
        lo_ci, hi_ci = np.quantile(ok, [0.025, 0.975])
        excl = (lo_ci > 0) or (hi_ci < 0)
        n_corner_in_sample = "n/a"
        print(f"    {label}: mean = {np.mean(ok):+.3f}   median = {np.median(ok):+.3f}   "
              f"95% CI = [{lo_ci:+.3f}, {hi_ci:+.3f}]   excludes 0: {'YES' if excl else 'NO'}")
    # verdict: stratified must exclude 0 (vanilla informational only — corner sparsity makes it unreliable)
    s_ok = boot_s[np.isfinite(boot_s)]
    lo_s, hi_s = np.quantile(s_ok, [0.025, 0.975])
    excl_s = (lo_s > 0) or (hi_s < 0)
    print(f"    (corner cases n={n_c}/{n}; vanilla bootstrap drops them ~"
          f"{(1-n_c/n)**n*100:.0f}% of samples — that's why stratified is fairer here)")
    v2 = "PASS — stratified β CI excludes 0" if excl_s else "FAIL — stratified CI crosses 0"
    print(f"    VERDICT: {v2}")

    # 3) PER-FOLD STABILITY
    print(f"\n[3] PER-FOLD β STABILITY  (n_fold={n})")
    fb = fold_betas
    mean_b, std_b = float(np.mean(fb)), float(np.std(fb))
    cv_pct = abs(std_b/mean_b)*100.0 if abs(mean_b) > 1e-9 else float('inf')
    n_sign_consistent = int(np.sum(np.sign(fb) == np.sign(mean_b)))
    print(f"    β over folds: mean = {mean_b:+.3f}   std = {std_b:.3f}   "
          f"CV = {cv_pct:.1f}%")
    print(f"    sign consistent with mean: {n_sign_consistent}/{n} folds")
    v3 = ("PASS — β is stable (CV<30% AND >90% sign consistent)"
          if (cv_pct < 30.0 and n_sign_consistent/n > 0.9) else
          "FAIL — β unstable across folds")
    print(f"    VERDICT: {v3}")

    # 4) HALF-SPLIT GENERALIZATION
    print(f"\n[4] HALF-SPLIT (50/50) GENERALIZATION  (n_split={n_half})")
    train_R2 = np.empty(n_half); test_R2 = np.empty(n_half); split_betas = np.empty(n_half)
    for k in range(n_half):
        idx = rng.permutation(n)
        tr = idx[:n//2]; te = idx[n//2:]
        # fit C_blend + β on train half
        b_tr = base[tr]; y_tr = logsf[tr]; t_tr = taus[tr]; sf_tr = sf[tr]
        b = cblend_fit(b_tr, y_tr, t_tr)
        resid_tr = y_tr - cblend_pred(b_tr, t_tr, b)
        sm = sf_tr.mean(); sc = sf_tr - sm
        d = float(np.dot(sc, sc)); beta_k = float(np.dot(sc, resid_tr)/d) if d>1e-12 else 0.0
        # predict on each half
        for which, idxs, store in (("train", tr, train_R2), ("test", te, test_R2)):
            b_s = base[idxs]; y_s = logsf[idxs]; t_s = taus[idxs]; sf_s = sf[idxs]
            pred = cblend_pred(b_s, t_s, b) + beta_k*(sf_s - sm)
            ss_s = float(np.sum((y_s - y_s.mean())**2)) + 1e-12
            store[k] = 1.0 - float(np.sum((y_s - pred)**2))/ss_s
        split_betas[k] = beta_k
    drop = float(np.mean(train_R2) - np.mean(test_R2))
    print(f"    R²(train half) = {np.mean(train_R2):.3f} ± {np.std(train_R2):.3f}")
    print(f"    R²(test  half) = {np.mean(test_R2):.3f} ± {np.std(test_R2):.3f}")
    print(f"    train − test gap = {drop:+.3f}    "
          f"(large gap ⇒ overfit; small ⇒ generalizes)")
    print(f"    β over half-splits: mean = {np.mean(split_betas):+.3f}   "
          f"std = {np.std(split_betas):.3f}   CV = {abs(np.std(split_betas)/np.mean(split_betas))*100 if abs(np.mean(split_betas))>1e-9 else float('inf'):.1f}%")
    v4 = ("PASS — train→test R² gap < 0.05" if drop < 0.05 else
          "FAIL — large train→test gap suggests overfit")
    print(f"    VERDICT: {v4}")

    # 5) AIC / BIC comparison
    print(f"\n[5] INFORMATION CRITERION")
    b = cblend_fit(base, logsf, taus)
    pred_ref = cblend_pred(base, taus, b)
    sse_ref = float(np.sum((logsf - pred_ref)**2))
    sm = sf.mean(); sc = sf - sm
    d = float(np.dot(sc, sc))
    beta_full = float(np.dot(sc, logsf - pred_ref)/d) if d>1e-12 else 0.0
    pred_full = pred_ref + beta_full*(sf - sm)
    sse_full = float(np.sum((logsf - pred_full)**2))
    # AIC ≈ n·log(SSE/n) + 2k ;  ΔAIC = +2·1 − n·log(sse_ref/sse_full)
    daic = 2*1 - n*np.log(sse_ref/sse_full)
    dbic = np.log(n)*1 - n*np.log(sse_ref/sse_full)
    print(f"    SSE base   = {sse_ref:.4f}    SSE base+β = {sse_full:.4f}")
    print(f"    ΔAIC = AIC(base+β) − AIC(base) = {daic:+.2f}   "
          f"(negative = candidate wins)")
    print(f"    ΔBIC = BIC(base+β) − BIC(base) = {dbic:+.2f}")
    v5 = ("PASS — improves AIC AND BIC (param earns its keep)"
          if (daic < -2 and dbic < 0) else
          ("WEAK — AIC ok, BIC marginal" if daic < -2 else "FAIL — does not improve AIC"))
    print(f"    VERDICT: {v5}")

    # 6) LEAVE-CORNER-OUT — the cleanest fairness test for a corner-targeting term.
    # Fit β ONLY on the bulk (no 62:38 corner cases).  Then predict the held-out
    # corner with that β.  If the term GENERALIZES from bulk physics to the corner,
    # bulk-only β should still significantly improve corner RMSE.  If it doesn't,
    # the term was an over-fit to the 4 corner cases.
    print(f"\n[6] LEAVE-CORNER-OUT GENERALIZATION (n_corner={n_c}, n_bulk={n_b})")
    if n_c < 1:
        print("    (no corner cases — test n/a)")
    else:
        # baseline: predict the corner with C_blend only (no β)
        b_b = cblend_fit(base[idx_bulk], logsf[idx_bulk], taus[idx_bulk])
        pred_corner_noβ = cblend_pred(base[idx_corner], taus[idx_corner], b_b)
        rmse_noβ = float(np.sqrt(np.mean((logsf[idx_corner] - pred_corner_noβ)**2)))
        # fit β on bulk only
        resid_bulk = logsf[idx_bulk] - cblend_pred(base[idx_bulk], taus[idx_bulk], b_b)
        sm_b = sf[idx_bulk].mean(); sc_b = sf[idx_bulk] - sm_b
        d_b = float(np.dot(sc_b, sc_b))
        beta_bulk = float(np.dot(sc_b, resid_bulk)/d_b) if d_b > 1e-12 else 0.0
        pred_corner_β = pred_corner_noβ + beta_bulk*(sf[idx_corner] - sm_b)
        rmse_β = float(np.sqrt(np.mean((logsf[idx_corner] - pred_corner_β)**2)))
        # for reference: β fit on FULL data (corner included)
        beta_full = _beta_of(base, logsf, taus, sf)
        print(f"    β (bulk-only fit)       = {beta_bulk:+.3f}")
        print(f"    β (full-data fit)       = {beta_full:+.3f}   "
              f"(ratio bulk/full = {beta_bulk/beta_full if abs(beta_full)>1e-9 else float('inf'):+.2f})")
        print(f"    corner RMSE (no β)      = {rmse_noβ:.3f}")
        print(f"    corner RMSE (bulk-β)    = {rmse_β:.3f}    "
              f"improvement = {rmse_noβ - rmse_β:+.3f}")
        # Same-sign β AND substantial improvement = real bulk→corner physics
        same_sign = (np.sign(beta_bulk) == np.sign(beta_full)) and abs(beta_bulk) > 0.3*abs(beta_full)
        improved = (rmse_noβ - rmse_β) > 0.1
        v6 = ("PASS — bulk-fit β generalizes to the corner (real physics, not corner over-fit)"
              if (same_sign and improved) else
              "WEAK/FAIL — bulk-only β doesn't carry over to the corner")
        print(f"    VERDICT: {v6}")

    print("\n" + "=" * 78)
    print("OVERALL — verdicts above; the most informative ones for a corner-driven")
    print("          term are [3] per-fold stability, [4] half-split gap, [5] AIC,")
    print("          [6] leave-corner-out generalization, and [1] permutation null.")
    print("          ([2] stratified bootstrap is fairer for n_corner=4.)")


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "E"
    run(name)
