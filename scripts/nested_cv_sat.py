#!/usr/bin/env python3
"""Nested-CV validation of the SAT-blend σ_ionic form vs the bare-√ baseline.

The 6-panel test selects (φc_P, φc_S, δ) on the FULL corpus by LOOCV, so its
+0.009 LOOCV gain may carry optimistic selection bias.  This script removes
that bias with NESTED cross-validation:

    OUTER  : leave-one-out over all cases (unbiased generalization estimate)
    INNER  : for each outer-train set, re-select (φc_P, φc_S, δ) by inner
             K-fold CV — the held-out case never touches hyperparameter choice.

It reports, on the SAME cases:
    • baseline LOOCV       (bare √(φ−0.19) + C_blend, no hyperparameters)
    • SAT naive LOOCV      (hyperparams chosen on full data → biased, = the panel)
    • SAT NESTED-CV        (hyperparams re-chosen inside each fold → unbiased)

VERDICT: the SAT form is real iff  SAT-nested  >  baseline  by a margin above
the LOOCV noise SE.  If SAT-nested collapses toward baseline while SAT-naive
stayed high, the panel gain was selection bias.

Run from the repo root (needs webapp/results + webapp/archive):
    python3 scripts/nested_cv_sat.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
import generate_comparison_plots as gcp  # noqa: E402  (reuse exact helpers)

SG = 3.0; PHI_C0 = 0.19; CN_EXP = 2.0; COV_EXP = 0.5      # base fixed form
# C_blend(τ) is now logpoly2 (3 OLS params: a, b, c) — dual-branch retired
# after scripts/screen_form_simplifications.py confirmed +0.0020 LOOCV
# and -10.6 ΔAIC at half the parameters (2026-05-28).
K_PS = 10.0; P_C = 0.5                                    # P:S sigmoid (g_010)

# Joint screen grids (match the plot)
PHICP_GRID = np.round(np.linspace(0.18, 0.215, 8), 4)
PHICS_GRID = np.round(np.linspace(0.15, 0.215, 14), 4)
DELTA_GRID = np.round(np.linspace(0.0, 0.10, 6), 4)


# Per-seed simulation anomalies — actual σ inconsistent with same-design
# siblings.  Justified case-by-case in CLAUDE.md (2026-05-28 audit):
#   input_particulate_12_S3: σ_act=0.020 vs 5 siblings 0.030–0.045 at same
#       (φ,CN,r_SE) → σ_act ≈ half of sibling median, isolated anomaly.
#   input_1mAh_9: σ_act=0.020 vs 5 _Sn siblings 0.029–0.035 (median 0.033)
#       at same (φ≈0.23, CN≈4.5, r_SE=0.5µm) → σ_act = 61% of sibling
#       median, same pattern as particulate_12_S3.  Excluded 2026-05-28.
_EXCLUDED_NAMES = {'input_particulate_12_S3', 'input_1mAh_9'}


def _meta_name(cid, mp_parent):
    """Look up the human-readable name from meta.json (matches dashboard names)."""
    for meta_p in (Path('webapp/uploads') / cid / 'meta.json',
                   mp_parent / 'meta.json'):
        if meta_p.exists():
            try:
                return __import__('json').load(open(meta_p)).get('name') or cid
            except Exception:
                pass
    return cid


def load_corpus():
    """Scan webapp/results + webapp/archive for full_metrics.json and build the
    Stage-E/physics arrays used by the fixed form."""
    rows = []
    seen = set()
    for base in ('webapp/results', 'webapp/archive'):
        bp = Path(base)
        if not bp.is_dir():
            continue
        for mp in bp.rglob('full_metrics.json'):
            try:
                d = __import__('json').load(open(mp))
            except Exception:
                continue
            sig = gcp._stage_e_sigma(d)
            phi = gcp._get(d, 'phi_se'); cn = gcp._get(d, 'se_se_cn')
            cov = gcp._cov_frac(d, physics=True) or gcp._cov_frac(d, physics=False)
            fp = gcp._get(d, 'percolation_pct') / 100.0
            tau = gcp._get(d, 'tortuosity_recommended', gcp._get(d, 'tortuosity_mean', 0))
            p = gcp._ps_fraction(d)
            if not (sig and sig > 0 and phi > PHI_C0 and cn > 0 and cov and cov > 0
                    and fp > 0 and tau > 0):
                continue
            if _meta_name(mp.parent.name, mp.parent) in _EXCLUDED_NAMES:
                continue
            key = (round(phi, 4), round(cn, 3), round(float(sig), 5))
            if key in seen:
                continue
            seen.add(key)
            sz = _size_proxy(d)
            # composition-aware AM-SE contact quality (handles 0:10 AM_S-only
            # AND mixed P:S where both AM_P & AM_S coverage exist):
            amcn = (d.get('am_se_cn_surface_weighted') or d.get('am_se_cn_mean')
                    or d.get('AM_S_se_cn_mean'))
            cov_h = (d.get('coverage_AM_mean') or d.get('coverage_AM_S_mean'))
            cov_p = (d.get('coverage_AM_mean_physics')
                     or d.get('coverage_AM_S_mean_physics'))
            cov_dlt = (d.get('coverage_AM_delta_pct_rough')
                       or d.get('coverage_AM_S_delta_pct_rough'))
            # POST-Cronau diagnostic flagged these (62:38 corr +0.80~+0.82) —
            # geometric (non-circular) constriction-area family, captures the
            # "few but large contacts" physics for D1/D1.5 that CN² misses.
            pha = d.get('path_hop_area_mean_physics') or d.get('path_hop_area_mean')
            cnea = d.get('se_se_cn_eff_area') or d.get('se_se_cn_eff_area_perc')
            scv = d.get('stress_cv')   # particle-stress non-uniformity (mech.)
            # Extract individual r_AM_S, r_AM_P for label-free physical form
            # (needed by the smooth two-sigmoid f_small formulation that
            # replaces g010's label dependence with actual size inputs).
            def _one_ram(keys):
                for k in keys:
                    v = d.get(k)
                    if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0:
                        return v*1000.0 if v < 0.01 else float(v)
                return np.nan
            r_AM_S_val = _one_ram(('_input_r_AM_S_um', '_input_r_AM_S', 'r_AM_S_um', 'r_AM_S'))
            r_AM_P_val = _one_ram(('_input_r_AM_P_um', '_input_r_AM_P', 'r_AM_P_um', 'r_AM_P'))
            rows.append((phi, cn, cov, fp, tau, float(sig), p,
                         float(sz) if sz else np.nan, _direct_rse_um(d),
                         float(amcn) if amcn and amcn > 0 else np.nan,
                         float(cov_h)/100.0 if cov_h and cov_h > 0 else np.nan,
                         float(cov_p)/100.0 if cov_p and cov_p > 0 else np.nan,
                         float(cov_dlt) if cov_dlt is not None else np.nan,
                         _direct_ram_um(d, p),
                         float(pha) if pha and pha > 0 else np.nan,
                         float(cnea) if cnea and cnea > 0 else np.nan,
                         float(scv) if scv and scv > 0 else np.nan,
                         r_AM_S_val, r_AM_P_val))
    a = np.array(rows, float)
    # cols: phi cn cov fp tau sigma p se_size r_SE_um amcn covAM_h covAM_p covAM_dpct r_AM_um path_hop_area se_cn_eff_area stress_cv r_AM_S r_AM_P
    return a


def _direct_ram_um(d, p):
    """Composition-weighted AM radius in µm: (1−p)·r_AM_S + p·r_AM_P (NaN if none)."""
    def one(keys):
        for k in keys:
            v = d.get(k)
            if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0:
                return v*1000.0 if v < 0.01 else float(v)
        return np.nan
    rs = one(('_input_r_AM_S_um', '_input_r_AM_S', 'r_AM_S_um', 'r_AM_S'))
    rp = one(('_input_r_AM_P_um', '_input_r_AM_P', 'r_AM_P_um', 'r_AM_P'))
    if np.isfinite(rs) and np.isfinite(rp):
        return (1.0 - p)*rs + p*rp
    return rs if np.isfinite(rs) else rp


def _direct_rse_um(d):
    """Direct SE radius in µm from the design inputs (NaN if unavailable)."""
    for k in ('_input_r_SE_um', '_input_r_SE', 'r_SE_um', 'r_SE'):
        v = d.get(k)
        if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0:
            return v*1000.0 if v < 0.01 else float(v)
    return np.nan


def _size_proxy(d):
    """SE grain-size proxy (µm): direct r_SE if present, else 1/gb_density."""
    r = _direct_rse_um(d)
    if np.isfinite(r):
        return r
    gb = d.get('gb_density_mean')
    if isinstance(gb, (int, float)) and not isinstance(gb, bool) and gb > 0:
        return 1.0/gb
    return np.nan


def base_no_phi(a):
    """Base log without the φ term (so φc can be re-screened)."""
    phi, cn, cov, fp = a[:, 0], a[:, 1], a[:, 2], a[:, 3]
    return np.log(SG) + CN_EXP*np.log(cn) + COV_EXP*np.log(cov) + 3.0*np.log(fp)


def base_log_baseline(a):
    return base_no_phi(a) + 0.5*np.log(np.maximum(a[:, 0] - PHI_C0, 1e-9))


def cronau_factor(rse_um, smooth=True):
    """Stage-E σ_ionic SE-size factor (Cronau 2022 piecewise).

    smooth=True (default) — three-sigmoid approximation, fully differentiable:
        Cronau(r) = 0.33 + 0.32·σ(K(r−0.10)) + 0.25·σ(K(r−0.30)) + 0.10·σ(K(r−0.50))
        with K = 50/µm.  Plateau values match the literature within <1% at
        interior points (r ∈ {0.05, 0.20, 0.40, 1.0µm}); transitions are
        softened over ~0.04µm windows at the literature breakpoints.

    smooth=False — original piecewise literature curve:
        r≥0.5µm→1.00, 0.3–0.5→0.90, 0.1–0.3→0.65, 0.03–0.1→linear interp,
        <0.03→0.33.  Kept for back-compat / diagnostic.

    Adopted 2026-05-28: smooth replaces piecewise to make the form fully
    differentiable (consistent with the smooth f_small g_phys adoption).
    LOOCV impact negligible (the corpus has only 1 sub-µm case).  NaN r_SE → 1.0.
    """
    r = np.asarray(rse_um, float)
    if smooth:
        K = 50.0  # 1/µm; transition width ~0.04µm
        f = (0.33
             + 0.32 / (1.0 + np.exp(-K*(r - 0.10)))
             + 0.25 / (1.0 + np.exp(-K*(r - 0.30)))
             + 0.10 / (1.0 + np.exp(-K*(r - 0.50))))
    else:
        f = np.select([r >= 0.5, r >= 0.3, r >= 0.1, r >= 0.03],
                      [1.00, 0.90, 0.65, 0.33 + 0.32*(np.clip(r, 0.03, 0.1)-0.03)/0.07],
                      default=0.33)
    return np.where(np.isfinite(r) & (r > 0), f, 1.0)


# ── Production augmentation (C4 adopted 2026-05-28) ────────────────────────
# Two extra OLS coefficients fitted alongside C_blend:
#   β_P2  · (φ−φc)² · (r_SE − 0.5)+        — Cronau high-r_SE extension arm
#   β_cov · (Δcov  − median(Δcov))         — Hertz→physics amplification gap
# Justification: bidir_62_38_test.py confirmed leave-corner-out PASS for the
# joint model (sign-consistent bulk vs full β AND corner RMSE -0.119 below
# threshold).  Each term separately failed the cross-validation generalization
# test, but jointly they regularize each other.  Catches 3 of 4 corner cases
# within ±10% (input_S_2 r_SE=0.5 partial — bidirectional bias).

PHIC_PROD = 0.195  # composition-neutral φc for the P2 term


def p2_feature(phi, r_SE_um, p_amp=None):
    """P2 augmentation feature: g_010 · (φ−φc_S)² · (r_SE − 0.5)+.

    Zero at r_SE ≤ 0.5µm (Cronau's reference threshold); grows quadratically
    in SE-volume excess above φc and linearly in grain-size excess above
    Cronau's plateau.  Physical reading: 'bulk-grain enhancement' at large
    grain × high SE fraction — natural extension of Cronau curve.

    GATING (added 2026-05-28 after C4 spillover diagnosis): the term is
    g_010-gated by default — fires only at 0:10 (pure AM_S) where the
    62:38 corner physics lives.  Without gating, P2 activates for ANY
    composition with r_SE>0.5 AND φ>φc, causing positive-direction spillover
    into non-0:10 D1+ cases (1mAh_5_AMP +22→+29%, 6mAh_real_10 NEW +26%,
    8mAh_real40_9 NEW +22%) — those were ALREADY over-predicted, so P2
    pushed them further out.  Gating restricts the correction to 0:10
    where it's physically motivated AND data-validated.

    p_amp = AM_P/(AM_P+AM_S); if None, ungated (legacy C4 behavior)."""
    pex = np.maximum(np.asarray(phi, float) - PHIC_PROD, 0.0)
    r = np.asarray(r_SE_um, float)
    r_safe = np.where(np.isfinite(r) & (r > 0), r, 0.5)  # neutral if missing
    rse_hi = np.maximum(r_safe - 0.5, 0.0)
    p2 = pex**2 * rse_hi
    if p_amp is not None:
        g_010 = 1.0 / (1.0 + np.exp(K_PS * (np.asarray(p_amp, float) - P_C)))
        p2 = g_010 * p2
    return p2


def cov_delta_feature(cov_delta_pct, center=None):
    """Δcov augmentation: coverage_AM_S_delta_pct_rough − median.  This is
    the Hertz→physics amplification % — how much Tabor adhesion + volume
    corrections inflate the bare elastic Hertz contact area.  Centered so
    that 0 = 'average corpus amplification'; β_cov < 0 in fit means the
    form's physics-cov over-uses inflation when amplification is large.

    Returns (centered_array, median_used)."""
    v = np.asarray(cov_delta_pct, float)
    if center is None:
        med = float(np.nanmedian(v[np.isfinite(v)])) if np.isfinite(v).any() else 0.0
    else:
        med = float(center)
    return np.where(np.isfinite(v), v - med, 0.0), med


def production_extras(a, cov_delta_center=None):
    """Compute the production augmentation extras for the C4 form
    (g_010-gated P2 + Δcov, 2026-05-28).

    Returns (extras_list, cov_delta_median) where:
        extras_list[0] = g_010-gated P2 feature (n-vector)
        extras_list[1] = centered Δcov feature (n-vector)
    Pass extras_list to cblend_fit/pred via the `extras=` argument."""
    p2 = p2_feature(a[:, 0], a[:, 8], p_amp=a[:, 6])   # g_010-gated
    cdc, med = cov_delta_feature(a[:, 12], center=cov_delta_center)
    return [p2, cdc], med


def base_log_sat(a, phicP, phicS, delta):
    phi, p = a[:, 0], a[:, 6]
    g010 = 1.0/(1.0+np.exp(K_PS*(p - P_C)))
    phic = (1.0-g010)*phicP + g010*phicS
    pex = phi - phic
    return base_no_phi(a) + 0.5*np.log(np.sqrt(pex**2 + (delta*g010)**2) + 1e-12)


# Frozen SAT-blend optimum (from the joint screen) — fixed while testing exp_S
PHICP_F, PHICS_F, DELTA_F = 0.200, 0.195, 0.040


def base_log_sat_exp(a, exp_s, phicP=PHICP_F, phicS=PHICS_F, delta=DELTA_F, exp_p=0.5):
    """SAT-blend base with a COMPOSITION-DEPENDENT percolation exponent:
    exp_eff = (1−g010)·exp_p + g010·exp_s  → 0:10 gets the (steeper?) exp_s,
    P-heavy keeps mean-field 0.5.  Tests whether σ rises sharper above φc in 0:10."""
    phi, p = a[:, 0], a[:, 6]
    g010 = 1.0/(1.0+np.exp(K_PS*(p - P_C)))
    phic = (1.0-g010)*phicP + g010*phicS
    pex = phi - phic
    exp_eff = (1.0-g010)*exp_p + g010*exp_s
    return base_no_phi(a) + exp_eff*np.log(np.sqrt(pex**2 + (delta*g010)**2) + 1e-12)


def base_log_sat_cnexp(a, cn_exp):
    """SAT-blend base with the CN exponent replaced (production = 2.0).
    Tests whether the data prefers a different CN scaling — audit shows D1/D1.5
    have CN² z≈+1.5 but the form still under-predicts, suggesting the exponent
    may not be optimal."""
    # base = log(SG·Cronau) + 0.5·log(φ_eff) + cn_exp·log(cn) + 0.5·log(cov) + 3·log(fp)
    cn = a[:, 1]
    base = base_log_sat(a, PHICP_F, PHICS_F, DELTA_F) + np.log(cronau_factor(a[:, 8]))
    # subtract the production CN² and add cn_exp·log(cn)
    return base - CN_EXP*np.log(cn) + cn_exp*np.log(cn)


def base_log_sat_covexp(a, cov_exp):
    """SAT-blend base with the cov exponent replaced (production = 0.5).
    cov^½ z is +1.46 in D1/D1.5 — maybe linear (cov^1) catches them better."""
    cov = a[:, 2]
    base = base_log_sat(a, PHICP_F, PHICS_F, DELTA_F) + np.log(cronau_factor(a[:, 8]))
    return base - COV_EXP*np.log(cov) + cov_exp*np.log(cov)


def cblend_fit(base, logsf, taus, extras=None):
    """OLS joint fit of C_blend(τ) = a + b·ln τ + c·(ln τ)²  plus optional
    extras (each an n-length feature vector, fitted with its own β).

    extras=None → 3-param logpoly2 (legacy/bare form).
    extras=[P2, Δcov_centered] → 5-param C4 augmented form (production).
    Returns b = [a, b, c, β_extra1, β_extra2, ...] (length 3+len(extras))."""
    lt = np.log(taus)
    X_cols = [np.ones(len(taus)), lt, lt**2]
    if extras is not None:
        X_cols.extend(extras)
    X = np.column_stack(X_cols)
    b, *_ = np.linalg.lstsq(X, logsf - base, rcond=None)
    return b


def cblend_pred(base, taus, b, extras=None):
    """Apply C_blend(τ) + optional extras with coefficients b.
    b must have length 3 + (len(extras) if extras else 0)."""
    lt = np.log(taus)
    out = base + b[0] + b[1]*lt + b[2]*lt**2
    if extras is not None:
        for j, e in enumerate(extras):
            out = out + b[3+j] * e
    return out


def loocv_r2(base, logsf, taus, extras=None):
    """Plain LOOCV R² for a FIXED base (no hyperparameter selection).
    extras=None → 3-param logpoly2; extras=[arrays] → augmented form."""
    n = len(taus); ss = np.sum((logsf-logsf.mean())**2); sse = 0.0
    for i in range(n):
        m = np.ones(n, bool); m[i] = False
        extras_tr = [e[m] for e in extras] if extras is not None else None
        extras_te = [e[i:i+1] for e in extras] if extras is not None else None
        b = cblend_fit(base[m], logsf[m], taus[m], extras=extras_tr)
        pi = cblend_pred(base[i:i+1], taus[i:i+1], b, extras=extras_te)[0]
        sse += (logsf[i]-pi)**2
    return 1 - sse/ss


def production_aug_fit(base, logsf, taus, a):
    """Convenience: fit the C4 augmented form (logpoly2 + P2 + Δcov).
    Returns (b, cov_delta_median) where b = [a_blend, b_blend, c_blend, β_P2, β_cov]."""
    extras, med = production_extras(a)
    b = cblend_fit(base, logsf, taus, extras=extras)
    return b, med


def production_aug_pred(base, taus, a, b, cov_delta_center):
    """Apply the C4 augmented prediction.  cov_delta_center MUST match
    the median used at fit time (returned by production_aug_fit)."""
    extras, _ = production_extras(a, cov_delta_center=cov_delta_center)
    return cblend_pred(base, taus, b, extras=extras)


def _kfold_sse_sat(a, logsf, taus, phicP, phicS, delta, folds):
    """Inner K-fold validation SSE for one SAT hyperparameter combo."""
    sse = 0.0
    for val in folds:
        tr = np.ones(len(taus), bool); tr[val] = False
        bl = base_log_sat(a, phicP, phicS, delta)
        b_lp = cblend_fit(bl[tr], logsf[tr], taus[tr])
        pv = cblend_pred(bl[val], taus[val], b_lp)
        sse += np.sum((logsf[val]-pv)**2)
    return sse


def nested_cv_sat(a, logsf, taus, k_inner=5, seed=0):
    """OUTER LOO; INNER k-fold re-selects (φc_P, φc_S, δ) on the outer-train set.
    Returns the unbiased outer-CV R² and how often each hyperparam was picked."""
    n = len(taus); ss = np.sum((logsf-logsf.mean())**2); sse = 0.0
    picks = []
    rng = np.random.default_rng(seed)
    for i in range(n):
        tr_idx = np.array([j for j in range(n) if j != i])
        a_tr, ls_tr, ta_tr = a[tr_idx], logsf[tr_idx], taus[tr_idx]
        # inner k-fold partition of the outer-train set
        order = rng.permutation(len(tr_idx))
        folds = [order[f::k_inner] for f in range(k_inner)]
        best, best_sse = None, np.inf
        for pP in PHICP_GRID:
            for pS in PHICS_GRID:
                for dl in DELTA_GRID:
                    s = _kfold_sse_sat(a_tr, ls_tr, ta_tr, pP, pS, dl, folds)
                    if s < best_sse:
                        best_sse, best = s, (pP, pS, dl)
        pP, pS, dl = best; picks.append(best)
        # refit on the full outer-train set with the inner-selected combo, predict i
        bl = base_log_sat(a, pP, pS, dl)
        b_lp = cblend_fit(bl[tr_idx], ls_tr, ta_tr)
        pi = cblend_pred(bl[i:i+1], taus[i:i+1], b_lp)[0]
        sse += (logsf[i]-pi)**2
    picks = np.array(picks)
    return 1 - sse/ss, picks


# ── SAT + extra term (does catching 62:38 add REAL gain?) ───────────────────
SIZE_K_PHI = 12.0; SIZE_PHI_GATE = 0.30   # near-threshold gate for the size term
GB_R_C = 0.5; GB_K = 12.0                 # Cronau sub-µm GB threshold (µm) + sharpness


def size_feat(a):
    """Near-threshold-gated, log SE-size feature (raw, un-centered)."""
    phi, sz = a[:, 0], a[:, 7]
    g = 1.0/(1.0+np.exp(SIZE_K_PHI*(phi - SIZE_PHI_GATE)))
    ls = np.log(np.where(np.isfinite(sz) & (sz > 0), sz, np.nan))
    ls = np.where(np.isfinite(ls), ls, np.nanmedian(ls[np.isfinite(ls)]) if np.isfinite(ls).any() else 0.0)
    return g * ls


def gb_feat(a):
    """Sub-µm grain-boundary indicator (mirrors the Stage-E Cronau correction):
    sigmoid ON (→1) when r_SE < GB_R_C, OFF for coarse SE.  NaN r_SE → 0 (neutral)."""
    rse = a[:, 8]
    f = 1.0/(1.0+np.exp(-GB_K*(GB_R_C - rse)))   # r_SE < 0.5µm → ~1
    return np.where(np.isfinite(rse), f, 0.0)


def _logcol(a, col):
    v = a[:, col]
    ls = np.log(np.where(np.isfinite(v) & (v > 0), v, np.nan))
    med = np.nanmedian(ls[np.isfinite(ls)]) if np.isfinite(ls).any() else 0.0
    return np.where(np.isfinite(ls), ls, med)


def _g010(a):
    """P:S sigmoid: ~1 toward 0:10 (p→0), ~0 toward 10:0 (p→1)."""
    return 1.0/(1.0+np.exp(K_PS*(a[:, 6] - P_C)))


def amcn_feat(a):
    """log AM-SE coordination (surface-weighted, composition-aware → handles
    0:10 AM_S-only AND mixed P:S). Diagnostic's top geometric signal in 62:38
    (corr −0.81): high am_se_cn (small SE / many tiny contacts) ⇒ lower σ."""
    return _logcol(a, 9)


def amcn_g010_feat(a):
    """am_se_cn gated to 0:10 (signal is 0:10-localized: corr −0.81 in 62:38 but
    only ~−0.2 globally) — apply the correction where it actually lives."""
    f = _logcol(a, 9)
    return _g010(a) * (f - np.mean(f))


def covAM_hertz_feat(a):
    """log AM coverage (total, Hertzian) — contact-AREA side, composition-aware."""
    return _logcol(a, 10)


def covAM_phys_feat(a):
    """log AM coverage (total, physics) — model's cov already uses this (control)."""
    return _logcol(a, 11)


def covAM_dpct_feat(a):
    """AM coverage Hertz→physics amplification % (plastic-flow proxy)."""
    v = a[:, 12]
    med = np.nanmedian(v[np.isfinite(v)]) if np.isfinite(v).any() else 0.0
    return np.where(np.isfinite(v), v, med)


def sizeratio_feat(a):
    """log(r_SE / r_AM) design size ratio (composition-weighted r_AM). The
    geometric CAUSE behind am_se_cn — small SE relative to AM ⇒ many contacts."""
    rse, ram = a[:, 8], a[:, 13]
    lr = np.log(rse) - np.log(ram)
    med = np.nanmedian(lr[np.isfinite(lr)]) if np.isfinite(lr).any() else 0.0
    return np.where(np.isfinite(lr), lr, med)


# ── POST-Cronau candidates (62:38 D1/D1.5 high-σ residual; diag corr ~+0.8) ──
def pha_feat(a):
    """log path_hop_area (physics) — Holm constriction cross-section along the
    percolation path.  Large SE ⇒ few but wide contacts ⇒ low Holm loss ⇒
    higher σ.  Diag corr +0.82 in 62:38 (post-Cronau)."""
    return _logcol(a, 14)


def cnea_feat(a):
    """log se_se_cn_eff_area — SE-SE coordination weighted by contact AREA, the
    'count×size' combo. Diag corr +0.80 in 62:38 (post-Cronau)."""
    return _logcol(a, 15)


def scv_feat(a):
    """log stress_cv (von-Mises CV%) — particle-stress non-uniformity. Uniform
    stress ⇔ well-formed network ⇔ high σ; expect NEGATIVE β. Diag corr −0.82."""
    return _logcol(a, 16)


# Pinpoint gates for the D1/D1.5 62:38 corner (high-φ SE-rich, optionally 0:10).
PHI_HIGH = 0.30; K_PHI_HIGH = 15.0


def _g_high(a):
    """SE-rich gate: ~1 for φ>0.30, ~0 below.  Isolates the corner where
    path_hop_area / area-weighted-CN signal lives (62:38 → φ_se~0.35)."""
    return 1.0/(1.0+np.exp(-K_PHI_HIGH*(a[:, 0] - PHI_HIGH)))


def pha_ghi_feat(a):
    """g_high × log(path_hop_area) — concentrates the constriction-area signal
    where it lives (SE-rich corner)."""
    return _g_high(a) * _logcol(a, 14)


def pha_ghi010_feat(a):
    """g_high × g_010 × log(path_hop_area) — pinpoint D1/D1.5 (SE-rich 0:10)."""
    g010 = 1.0/(1.0+np.exp(K_PS*(a[:, 6] - P_C)))
    return _g_high(a) * g010 * _logcol(a, 14)


# ── 62:38 EXP/SATURATION/COUPLED candidates ──────────────────────────────────
# Origin: scripts/sat_exp_62_38_search.py scan; rationale = at extreme SE
# fraction (φ>0.30) with large SE grains the response is exponential / coupled
# in (φ×r_SE) — bulk-grain dominance.  Top ★ candidates from the search:
#   L  +0.0065  β=+1.43  ↓RMSE_62=+0.289   (gated D1/D1.5 corner pinpoint)
#   E  +0.0060  β=+2.41  ↓RMSE_62=+0.282   (ungated power coupling, cleanest)
#   M2 +0.0057  β=+0.82  ↓RMSE_62=+0.266   (gated LINEAR, control vs L)
#   D  +0.0019  β=+0.62  ↓RMSE_62=+0.191   (ungated LINEAR, control vs E)
#   F  +0.0020  β=+0.034 ↓RMSE_62=+0.184   (pure exp(φ·r_SE)−1, γ=3)
# pure φ-saturation (A) and pure CN/τ exp (J/K) all FAILED → the lever is the
# φ×r_SE COUPLING (bulk-grain × extreme SE), exactly the user's intuition.

PHIC_NEUTRAL = 0.195   # composition-neutral threshold for the (φ−φc) base


def _rse_safe(a):
    """r_SE in µm with NaN → median fallback (neutral for cases lacking input)."""
    rse = a[:, 8]
    if np.isfinite(rse).any():
        med = float(np.nanmedian(rse[np.isfinite(rse)]))
    else:
        med = 1.0
    return np.where(np.isfinite(rse) & (rse > 0), rse, med)


def bulk_couple_feat(a):
    """E:  (φ−φc)² · r_SE  — ungated power coupling.  Captures bulk-grain
    dominance at extreme SE: σ rises faster than (φ_eff)^0.5 once φ−φc is large
    AND the grains are big (fewer GBs per volume).  Top ungated candidate."""
    pex = np.maximum(a[:, 0] - PHIC_NEUTRAL, 0.0)
    return pex**2 * _rse_safe(a)


def bulk_couple_lin_feat(a):
    """D:  (φ−φc) · r_SE  — linear control for E (does quadratic actually win?)."""
    pex = np.maximum(a[:, 0] - PHIC_NEUTRAL, 0.0)
    return pex * _rse_safe(a)


def corner_log_couple_feat(a):
    """L:  g_high · g_010 · log(1 + (φ−0.30)·r_SE)  — D1/D1.5 pinpoint with a
    saturating log-coupled exp form.  Gates: φ>0.30 (SE-rich) AND p<0.5 (0:10).
    The α=1 variant wins the search (β=+1.43)."""
    pex_h = np.maximum(a[:, 0] - PHI_HIGH, 0.0)
    return _g_high(a) * _g010(a) * np.log1p(pex_h * _rse_safe(a))


def corner_lin_couple_feat(a):
    """M2:  g_high · g_010 · (φ−φc) · r_SE  — linear control for L."""
    pex = np.maximum(a[:, 0] - PHIC_NEUTRAL, 0.0)
    return _g_high(a) * _g010(a) * pex * _rse_safe(a)


def exp_phi_rse_feat(a):
    """F:  exp(3·φ·r_SE) − 1  — pure-exp form (no gates, no (φ−φc) shift).
    Sanity check that the lever lives at (φ·r_SE) coupling regardless of form."""
    return np.exp(3.0 * a[:, 0] * _rse_safe(a)) - 1.0


def loocv_with_feat(base, logsf, taus, sfeat):
    """LOOCV with C_blend + β·sfeat fit jointly per fold (β is an OLS coefficient,
    no selection → unbiased). Returns (r2, mean β).
    Uses the adopted logpoly2 C_blend: a + b·ln τ + c·(ln τ)² (3 params)."""
    n = len(taus); ss = np.sum((logsf-logsf.mean())**2); sse = 0.0; betas = []
    lt = np.log(taus)
    X = np.column_stack([np.ones(n), lt, lt**2])
    for i in range(n):
        mk = np.ones(n, bool); mk[i] = False
        resid = logsf[mk] - base[mk]
        bX, *_ = np.linalg.lstsq(X[mk], resid, rcond=None)
        cb = X[mk] @ bX
        sm = sfeat[mk].mean(); sc = sfeat[mk] - sm
        rr = resid - cb
        d = float(np.dot(sc, sc))
        beta = float(np.dot(sc, rr)/d) if d > 1e-12 else 0.0
        betas.append(beta)
        cbi = X[i] @ bX
        pi = base[i] + cbi + beta*(sfeat[i] - sm)
        sse += (logsf[i] - pi)**2
    return 1 - sse/ss, float(np.mean(betas))


def cblend_feat_fit(base, logsf, taus, sf):
    """C_blend fit + one extra coefficient β on the post-C_blend residual
    (feature sf centered here).  Returns (b, beta, smean) — b is the 3-vec
    logpoly2 coefficients."""
    b = cblend_fit(base, logsf, taus)
    resid = logsf - cblend_pred(base, taus, b)
    smean = sf.mean(); sc = sf - smean
    beta = float(np.dot(sc, resid)/np.dot(sc, sc)) if np.dot(sc, sc) > 1e-12 else 0.0
    return b, beta, smean


def cblend_feat_pred(base, taus, sf, b, beta, smean):
    return cblend_pred(base, taus, b) + beta*(sf - smean)


EXP_S_GRID = np.round(np.linspace(0.3, 1.4, 12), 3)   # 0:10 percolation exponent
CN_EXP_GRID = np.round(np.linspace(1.0, 3.0, 11), 3)  # CN exponent (production = 2.0)
COV_EXP_GRID = np.round(np.linspace(0.2, 1.2, 11), 3) # cov exponent (production = 0.5)


def _nested_cv_exp_scan(a, logsf, taus, grid, build_base, k_inner=5, seed=0):
    """Generic outer-LOO + inner k-fold scan of a single exponent that enters
    the base directly. `build_base(a_subset, exp_val)` must return base_log."""
    n = len(taus); ss = np.sum((logsf-logsf.mean())**2); sse = 0.0; picks = []
    rng = np.random.default_rng(seed)
    for i in range(n):
        tr = np.array([j for j in range(n) if j != i])
        ls_tr, ta_tr = logsf[tr], taus[tr]
        order = rng.permutation(len(tr)); folds = [order[f::k_inner] for f in range(k_inner)]
        best, best_sse = None, np.inf
        for ev in grid:
            bl = build_base(a[tr], float(ev))
            fsse = 0.0
            for val in folds:
                m = np.ones(len(tr), bool); m[val] = False
                b_lp = cblend_fit(bl[m], ls_tr[m], ta_tr[m])
                pv = cblend_pred(bl[val], ta_tr[val], b_lp)
                fsse += np.sum((ls_tr[val]-pv)**2)
            if fsse < best_sse:
                best_sse, best = fsse, float(ev)
        picks.append(best)
        bl = build_base(a, best)
        b_lp = cblend_fit(bl[tr], ls_tr, ta_tr)
        pi = cblend_pred(bl[i:i+1], taus[i:i+1], b_lp)[0]
        sse += (logsf[i]-pi)**2
    return 1 - sse/ss, float(np.mean(picks)), picks


def nested_cv_exp(a, logsf, taus, k_inner=5, seed=0):
    """Outer LOO; inner k-fold selects the 0:10 percolation exponent exp_S
    (φc/δ frozen at the joint optimum, P-heavy exp fixed 0.5). Returns
    (r2, mean exp_S, picks)."""
    n = len(taus); ss = np.sum((logsf-logsf.mean())**2); sse = 0.0; picks = []
    rng = np.random.default_rng(seed)
    for i in range(n):
        tr = np.array([j for j in range(n) if j != i])
        ls_tr, ta_tr = logsf[tr], taus[tr]
        order = rng.permutation(len(tr)); folds = [order[f::k_inner] for f in range(k_inner)]
        best, best_sse = None, np.inf
        for es in EXP_S_GRID:
            bl = base_log_sat_exp(a[tr], float(es))
            fsse = 0.0
            for val in folds:
                m = np.ones(len(tr), bool); m[val] = False
                b_lp = cblend_fit(bl[m], ls_tr[m], ta_tr[m])
                pv = cblend_pred(bl[val], ta_tr[val], b_lp)
                fsse += np.sum((ls_tr[val]-pv)**2)
            if fsse < best_sse:
                best_sse, best = fsse, float(es)
        picks.append(best)
        bl = base_log_sat_exp(a, best)
        b_lp = cblend_fit(bl[tr], ls_tr, ta_tr)
        pi = cblend_pred(bl[i:i+1], taus[i:i+1], b_lp)[0]
        sse += (logsf[i]-pi)**2
    return 1 - sse/ss, float(np.mean(picks)), picks


def nested_cv_sat_feat(a, logsf, taus, featfn, k_inner=5, seed=0):
    """As nested_cv_sat but the per-fold model is SAT-blend + β·featfn(a)
    (β fit inside each fold; (φc_P,φc_S,δ) re-selected by inner k-fold)."""
    n = len(taus); ss = np.sum((logsf-logsf.mean())**2); sse = 0.0
    sf_all = featfn(a); betas = []
    rng = np.random.default_rng(seed)
    for i in range(n):
        tr = np.array([j for j in range(n) if j != i])
        a_tr, ls_tr, ta_tr = a[tr], logsf[tr], taus[tr]
        order = rng.permutation(len(tr)); folds = [order[f::k_inner] for f in range(k_inner)]
        s_tr_all = featfn(a_tr)
        best, best_sse = None, np.inf
        for pP in PHICP_GRID:
            for pS in PHICS_GRID:
                for dl in DELTA_GRID:
                    b = base_log_sat(a_tr, pP, pS, dl)
                    fsse = 0.0
                    for val in folds:
                        m = np.ones(len(tr), bool); m[val] = False
                        b_lp, beta, sm = cblend_feat_fit(b[m], ls_tr[m], ta_tr[m], s_tr_all[m])
                        pv = cblend_feat_pred(b[val], ta_tr[val], s_tr_all[val], b_lp, beta, sm)
                        fsse += np.sum((ls_tr[val]-pv)**2)
                    if fsse < best_sse:
                        best_sse, best = fsse, (pP, pS, dl)
        pP, pS, dl = best
        b = base_log_sat(a, pP, pS, dl)
        b_lp, beta, sm = cblend_feat_fit(b[tr], ls_tr, ta_tr, sf_all[tr])
        betas.append(beta)
        pi = cblend_feat_pred(b[i:i+1], taus[i:i+1], sf_all[i:i+1], b_lp, beta, sm)[0]
        sse += (logsf[i]-pi)**2
    return 1 - sse/ss, float(np.mean(betas))


def main():
    a = load_corpus()
    n = len(a)
    if n < 20:
        print(f"[ABORT] only {n} usable cases found (need the WSL corpus).")
        return
    logsf = np.log(a[:, 5]); taus = a[:, 4]
    ss = np.sum((logsf-logsf.mean())**2)

    # 1) baseline (bare √, φc=0.19) — no hyperparameters → LOOCV is unbiased
    base_b = base_log_baseline(a)
    lo_base = loocv_r2(base_b, logsf, taus)

    # 2) SAT naive: pick (φc_P,φc_S,δ) on FULL data by LOOCV, then report LOOCV
    best, best_lo = None, -np.inf
    for pP in PHICP_GRID:
        for pS in PHICS_GRID:
            for dl in DELTA_GRID:
                lo = loocv_r2(base_log_sat(a, pP, pS, dl), logsf, taus)
                if lo > best_lo:
                    best_lo, best = lo, (pP, pS, dl)
    lo_sat_naive = best_lo

    # 3) SAT nested CV (unbiased)
    lo_sat_nested, picks = nested_cv_sat(a, logsf, taus)

    se = np.sqrt(np.var((logsf - logsf.mean())**2) / n) / ss  # rough LOOCV noise SE
    print("=" * 64)
    print(f"Nested-CV validation of SAT-blend  (n={n})")
    print("=" * 64)
    print(f"  baseline  LOOCV (bare √, φc=0.19) : {lo_base:.4f}")
    print(f"  SAT naive LOOCV (full-selected)   : {lo_sat_naive:.4f}   "
          f"[φc_P*={best[0]:.3f} φc_S*={best[1]:.3f} δ*={best[2]:.3f}]")
    print(f"  SAT NESTED-CV (unbiased)          : {lo_sat_nested:.4f}")
    print("-" * 64)
    print(f"  naive − nested (selection bias)   : {lo_sat_naive - lo_sat_nested:+.4f}")
    print(f"  nested − baseline (real gain)     : {lo_sat_nested - lo_base:+.4f}")
    print(f"  ~noise SE on LOOCV                : {se:.4f}")
    verdict = ("PASS — SAT generalizes (real gain > noise SE)"
               if lo_sat_nested - lo_base > se else
               "FAIL — gain is within noise / selection bias; keep bare √")
    print(f"  VERDICT: {verdict}")
    print("-" * 64)
    for j, name in enumerate(('φc_P', 'φc_S', 'δ')):
        vals, cnts = np.unique(picks[:, j], return_counts=True)
        top = sorted(zip(cnts, vals), reverse=True)[:3]
        print(f"  inner-picked {name:5s}: " + ", ".join(f"{v:.3f}×{c}" for c, v in top))

    # 4) extra terms targeting 62:38 — do they add REAL gain OVER SAT-blend?
    print("=" * 64)
    print("Extra terms targeting 62:38 (nested-CV gain OVER SAT-blend):")
    for tag, featfn, col, why in (
            ("sub-µm GB penalty (Cronau, r_SE<0.5µm)", gb_feat, 8,
             "FAIL before — kept for record"),
            ("log am_se_cn surf-wt (count, ungated)", amcn_feat, 9,
             "composition-aware; top signal but 0:10-localized"),
            ("log am_se_cn surf-wt × g_010 (gated)", amcn_g010_feat, 9,
             "PRIMARY: applies the −0.81 signal only where it lives (0:10)"),
            ("log coverage_AM total (Hertzian)", covAM_hertz_feat, 10,
             "contact-AREA side, composition-aware"),
            ("log coverage_AM total (physics)", covAM_phys_feat, 11,
             "model's cov already uses this (control)"),
            ("coverage_AM Hertz→phys Δ% (plastic amp)", covAM_dpct_feat, 12,
             "amplification axis"),
            ("log(r_SE/r_AM) size ratio", sizeratio_feat, 13,
             "design-input cause behind am_se_cn")):
        n_ok = int(np.isfinite(a[:, col]).sum())
        if n_ok < 0.4*n:
            print(f"  [skip {tag}: only {n_ok}/{n} expose the input]")
            continue
        lo_x, beta_x = nested_cv_sat_feat(a, logsf, taus, featfn)
        d = lo_x - lo_sat_nested
        v = "PASS — real gain → catches 62:38" if d > se else "FAIL — within noise"
        print(f"  + {tag}  [{n_ok}/{n}]")
        print(f"      nested-CV={lo_x:.4f}  Δover SAT={d:+.4f}  β={beta_x:+.3f}  ({why})")
        print(f"      VERDICT: {v}")
    print("-" * 64)
    print("  NOTE: am_se_cn (count) & coverage (area) are the SAME contact-quality")
    print("  axis (anti-correlated) — adopt only ONE. Testing several arms = mild")
    print("  multiple-comparison; trust a PASS only if Δ clearly exceeds the SE.")

    # Apples-to-apples baseline for sections 5–6: SAT with frozen φc/δ (no inner
    # scanning), so the Δ reflects ONLY the added effect — not the difference
    # between scanning vs not scanning.
    base_fix = base_log_sat(a, PHICP_F, PHICS_F, DELTA_F)
    lo_fix = loocv_r2(base_fix, logsf, taus)

    # 5) composition-dependent φ exponent for 0:10 (a NEW core-physics lever:
    #    the percolation exponent was frozen at 0.5 — never scanned).
    print("=" * 64)
    lo_exp, exps_mean, exps_picks = nested_cv_exp(a, logsf, taus)
    print("Composition-dependent φ exponent — 0:10 exp_S (φc/δ frozen, P-heavy 0.5):")
    print(f"  SAT (frozen φc/δ) LOOCV  : {lo_fix:.4f}")
    print(f"  SAT+exp_S NESTED-CV      : {lo_exp:.4f}   Δover SAT(frozen)={lo_exp - lo_fix:+.4f}   "
          f"mean exp_S={exps_mean:.2f}")
    vv, cc = np.unique(np.round(exps_picks, 2), return_counts=True)
    top = sorted(zip(cc, vv), reverse=True)[:4]
    print("  inner-picked exp_S: " + ", ".join(f"{v:.2f}×{c}" for c, v in top))
    print(f"  VERDICT: {'PASS — 0:10 wants a different exponent' if lo_exp - lo_fix > se else 'FAIL — exp_S=0.5 is best (no change)'}")

    # 5b) CN-exponent scan (production=2.0) — apples-to-apples vs the SAT×Cronau
    #     base at the SAME exponent (production), so the Δ reflects only the
    #     scan, not the (separately measured) Cronau gain.
    print("=" * 64)
    lo_cn, cn_mean, cn_picks = _nested_cv_exp_scan(a, logsf, taus, CN_EXP_GRID, base_log_sat_cnexp)
    lo_cn_ref = loocv_r2(base_log_sat_cnexp(a, CN_EXP), logsf, taus)   # CN^2 reference
    print(f"CN exponent scan (production = {CN_EXP}):")
    print(f"  SAT×Cronau, CN^{CN_EXP} (ref) LOOCV : {lo_cn_ref:.4f}")
    print(f"  SAT+scanned CN_exp NESTED-CV     : {lo_cn:.4f}   "
          f"Δ vs ref = {lo_cn - lo_cn_ref:+.4f}   mean CN_exp = {cn_mean:.2f}")
    vv, cc = np.unique(np.round(cn_picks, 2), return_counts=True)
    top = sorted(zip(cc, vv), reverse=True)[:4]
    print("  inner-picked CN_exp: " + ", ".join(f"{v:.2f}×{c}" for c, v in top))
    print(f"  VERDICT: {'PASS — data wants CN^' + f'{cn_mean:.2f}' if lo_cn - lo_cn_ref > se else f'FAIL — CN^{CN_EXP} is best (no change)'}")

    # 5c) cov-exponent scan (production=0.5) — same apples-to-apples comparison.
    print("=" * 64)
    lo_cv, cv_mean, cv_picks = _nested_cv_exp_scan(a, logsf, taus, COV_EXP_GRID, base_log_sat_covexp)
    lo_cv_ref = loocv_r2(base_log_sat_covexp(a, COV_EXP), logsf, taus)
    print(f"cov exponent scan (production = {COV_EXP}):")
    print(f"  SAT×Cronau, cov^{COV_EXP} (ref) LOOCV: {lo_cv_ref:.4f}")
    print(f"  SAT+scanned cov_exp NESTED-CV     : {lo_cv:.4f}   "
          f"Δ vs ref = {lo_cv - lo_cv_ref:+.4f}   mean cov_exp = {cv_mean:.2f}")
    vv, cc = np.unique(np.round(cv_picks, 2), return_counts=True)
    top = sorted(zip(cc, vv), reverse=True)[:4]
    print("  inner-picked cov_exp: " + ", ".join(f"{v:.2f}×{c}" for c, v in top))
    print(f"  VERDICT: {'PASS — data wants cov^' + f'{cv_mean:.2f}' if lo_cv - lo_cv_ref > se else f'FAIL — cov^{COV_EXP} is best (no change)'}")

    # 6) Stage-E Cronau SE-size factor — APPLIED (fixed literature, NOT fitted),
    #    so no DoF / no selection bias: does mirroring the target's own grain
    #    correction in σ_grain improve the fit?
    cf = cronau_factor(a[:, 8])
    lo_cron = loocv_r2(base_fix + np.log(cf), logsf, taus)
    n_sub = int(np.sum(np.isfinite(a[:, 8]) & (a[:, 8] < 0.5)))
    print("=" * 64)
    print("Stage-E Cronau SE-size factor — APPLIED to σ_grain (fixed, not fitted):")
    print(f"  SAT (frozen φc/δ) LOOCV     : {lo_fix:.4f}")
    print(f"  SAT × Cronau(r_SE) LOOCV    : {lo_cron:.4f}   Δ={lo_cron - lo_fix:+.4f}   "
          f"[{n_sub}/{n} cases r_SE<0.5µm get a penalty]")
    print(f"  VERDICT: {'ADOPT — literature factor improves the fit' if lo_cron - lo_fix > 0 else 'no gain — target σ apparently already reflects it (or none sub-0.5µm)'}")

    # 7) POST-Cronau candidates — does anything ADD on top of SAT × Cronau?
    #    (β fit by OLS each fold, no inner selection → unbiased LOOCV.)
    base_cron = base_fix + np.log(cf)
    print("=" * 64)
    print(f"POST-Cronau extras  (base = SAT × Cronau, LOOCV = {lo_cron:.4f}):")
    for tag, featfn, col, why in (
            ("log path_hop_area (physics, constriction)", pha_feat, 14,
             "Holm cross-section; diag corr +0.82 in 62:38"),
            ("log se_se_cn_eff_area (area-weighted CN)", cnea_feat, 15,
             "'count×size' that CN² misses; diag +0.80"),
            ("log stress_cv (mech. non-uniformity)", scv_feat, 16,
             "uniform stress ⇔ good network; diag −0.82"),
            ("path_hop_area × g_high (SE-rich gate)", pha_ghi_feat, 14,
             "gate concentrates signal where it lives (φ>0.30)"),
            ("path_hop_area × g_high × g_010 (D1/D1.5 pinpoint)", pha_ghi010_feat, 14,
             "SE-rich AND 0:10 — the actual D1/D1.5 62:38 corner")):
        n_ok = int(np.isfinite(a[:, col]).sum())
        if n_ok < 0.5*n:
            print(f"  [skip {tag}: only {n_ok}/{n} expose the input]")
            continue
        lo_x, beta_x = loocv_with_feat(base_cron, logsf, taus, featfn(a))
        d = lo_x - lo_cron
        v = "ADOPT — real gain → catches D1/D1.5" if d > se else "FAIL — within noise"
        print(f"  + {tag}  [{n_ok}/{n}]")
        print(f"      LOOCV={lo_x:.4f}  Δover (SAT×Cronau)={d:+.4f}  β={beta_x:+.3f}  ({why})")
        print(f"      VERDICT: {v}")

    # 7b) 62:38 EXP/SAT/COUPLED candidates (sat_exp_62_38_search.py finalists).
    #     LOOCV unbiased β; ALSO report subset RMSE so we can see if it actually
    #     catches the D1/D1.5 corner (which is the whole point).
    p_arr, phi_arr, rse_arr = a[:, 6], a[:, 0], a[:, 8]
    idx_corner = np.where((p_arr < 0.05) & (phi_arr > PHI_HIGH) &
                          np.isfinite(rse_arr) & (rse_arr >= 1.0))[0]
    idx_serich = np.where((p_arr < 0.05) & (phi_arr > PHI_HIGH))[0]
    # baseline (SAT × Cronau) single-shot prediction for subset RMSE deltas
    bb = cblend_fit(base_cron, logsf, taus)
    pred_b = cblend_pred(base_cron, taus, bb)
    def _rmse(idx, pred):
        return float('nan') if len(idx) == 0 else float(np.sqrt(np.mean((logsf[idx]-pred[idx])**2)))
    rmse62_b = _rmse(idx_corner, pred_b); rmseSE_b = _rmse(idx_serich, pred_b)
    print("=" * 64)
    print(f"62:38 EXP/SAT/COUPLED extras  (base = SAT × Cronau, LOOCV = {lo_cron:.4f}):")
    print(f"  baseline subset RMSE — 62:38 corner [n={len(idx_corner)}]: {rmse62_b:.3f}  "
          f"|  SE-rich 0:10 [n={len(idx_serich)}]: {rmseSE_b:.3f}")
    for tag, featfn, why in (
            ("E:  (φ−φc)²·r_SE  (ungated power coupling)", bulk_couple_feat,
             "cleanest — no gates; natural nonlinearity of (φ_eff)^0.5"),
            ("D:  (φ−φc)·r_SE  (LINEAR control for E)", bulk_couple_lin_feat,
             "tests whether the QUADRATIC really wins over linear"),
            ("L:  g_hi·g_010·log(1+(φ−0.30)·r_SE)  (D1/D1.5 pinpoint)", corner_log_couple_feat,
             "gated to SE-rich 0:10; β=+1.43 in the search"),
            ("M2: g_hi·g_010·(φ−φc)·r_SE  (LINEAR control for L)", corner_lin_couple_feat,
             "gated linear — tests if the log-saturation form matters"),
            ("F:  exp(3·φ·r_SE)−1  (pure exp; ungated)", exp_phi_rse_feat,
             "sanity: lever is at (φ·r_SE) coupling regardless of form")):
        sf = featfn(a)
        if not np.all(np.isfinite(sf)) or np.std(sf) < 1e-12:
            print(f"  [skip {tag}: degenerate]"); continue
        lo_x, beta_x = loocv_with_feat(base_cron, logsf, taus, sf)
        # single-shot pred to measure subset RMSE improvement
        b = cblend_fit(base_cron, logsf, taus)
        resid = logsf - cblend_pred(base_cron, taus, b)
        sm = sf.mean(); sc = sf - sm
        beta_ss = float(np.dot(sc, resid)/np.dot(sc, sc)) if np.dot(sc, sc) > 1e-12 else 0.0
        pred = cblend_pred(base_cron, taus, b) + beta_ss*(sf - sm)
        drc = rmse62_b - _rmse(idx_corner, pred)
        drs = rmseSE_b - _rmse(idx_serich, pred)
        d = lo_x - lo_cron
        v = ("ADOPT — global gain > noise AND catches 62:38" if (d > se and drc > 0) else
             "FAIL — within noise / no 62:38 gain")
        print(f"  + {tag}")
        print(f"      LOOCV={lo_x:.4f}  Δ={d:+.4f}  β={beta_x:+.3f}  "
              f"↓rmse_62={drc:+.3f}  ↓rmse_SE={drs:+.3f}  ({why})")
        print(f"      VERDICT: {v}")

    # 7c) Top candidates — FULL nested CV (re-select φc_P/φc_S/δ inside each
    # outer fold WITH the candidate β fit jointly).  This is the rigorous
    # verdict: gain that survives BOTH hyper re-selection AND single-coef LOO.
    print("=" * 64)
    print("Nested-CV verdict on TOP candidates (re-selects φc/δ + β per fold):")
    for tag, featfn in (("E:  (φ−φc)²·r_SE", bulk_couple_feat),
                        ("L:  g_hi·g_010·log(1+(φ−0.30)·r_SE)", corner_log_couple_feat)):
        lo_nx, beta_nx = nested_cv_sat_feat(a, logsf, taus, featfn)
        d = lo_nx - lo_sat_nested
        v = ("ADOPT — survives full nested re-selection"
             if d > se else "FAIL — nested gain within noise")
        print(f"  + {tag}")
        print(f"      nested-CV={lo_nx:.4f}  Δover SAT-nested={d:+.4f}  β={beta_nx:+.3f}")
        print(f"      VERDICT: {v}")

    # 8) Ablation — remove each base term and report LOOCV drop (C_blend refit
    #    every time, so it captures only what THAT term contributes uniquely).
    phi, cn_a, cov_a, fp_a = a[:, 0], a[:, 1], a[:, 2], a[:, 3]
    g010 = 1.0/(1.0+np.exp(K_PS*(a[:, 6] - P_C)))
    phic = (1.0-g010)*PHICP_F + g010*PHICS_F
    pex = phi - phic
    phi_eff = np.sqrt(pex**2 + (DELTA_F*g010)**2 + 1e-12)
    term_sg   = np.log(SG) * np.ones(n)
    term_cron = np.log(cronau_factor(a[:, 8]))
    term_phi  = 0.5 * np.log(phi_eff)
    term_cn   = 2.0 * np.log(cn_a)
    term_cov  = 0.5 * np.log(cov_a)
    term_fp   = 3.0 * np.log(fp_a)
    full = term_sg + term_cron + term_phi + term_cn + term_cov + term_fp
    lo_all = loocv_r2(full, logsf, taus)
    # "No C_blend": replace C_blend(τ) with a single constant fit (intercept only)
    sse_const = 0.0; ssn = ss
    for i in range(n):
        mk = np.ones(n, bool); mk[i] = False
        c = float(np.mean(logsf[mk] - full[mk]))
        sse_const += (logsf[i] - full[i] - c)**2
    lo_noblend = 1 - sse_const/ssn
    print("=" * 64)
    print(f"Ablation — LOOCV drop when each term is removed (full={lo_all:.4f}):")
    print(f"  remove C_blend(τ) → constant C : LOOCV={lo_noblend:.4f}   drop={lo_all - lo_noblend:+.4f}")
    for tag, term in (("Cronau(r_SE)",      term_cron),
                      ("(φ_eff)^0.5",       term_phi),
                      ("CN^2",              term_cn),
                      ("cov^0.5",           term_cov),
                      ("f_p^3",             term_fp)):
        lo_ab = loocv_r2(full - term, logsf, taus)
        var = float(np.std(term))
        print(f"  remove {tag:18s}  LOOCV={lo_ab:.4f}   drop={lo_all - lo_ab:+.4f}   "
              f"(σ(log-term)={var:.2f})")


if __name__ == "__main__":
    main()
