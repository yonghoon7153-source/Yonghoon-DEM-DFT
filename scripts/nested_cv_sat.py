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
KV5 = 5.0; CV5 = 2.1; KBL = 20.0; CBL = 1.92              # C_blend(τ) shape
K_PS = 10.0; P_C = 0.5                                    # P:S sigmoid (g_010)

# Joint screen grids (match the plot)
PHICP_GRID = np.round(np.linspace(0.18, 0.215, 8), 4)
PHICS_GRID = np.round(np.linspace(0.15, 0.215, 14), 4)
DELTA_GRID = np.round(np.linspace(0.0, 0.10, 6), 4)


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
            key = (round(phi, 4), round(cn, 3), round(float(sig), 5))
            if key in seen:
                continue
            seen.add(key)
            rows.append((phi, cn, cov, fp, tau, float(sig), p))
    a = np.array(rows, float)
    return a  # columns: phi, cn, cov, fp, tau, sigma, p


def base_no_phi(a):
    """Base log without the φ term (so φc can be re-screened)."""
    phi, cn, cov, fp = a[:, 0], a[:, 1], a[:, 2], a[:, 3]
    return np.log(SG) + CN_EXP*np.log(cn) + COV_EXP*np.log(cov) + 3.0*np.log(fp)


def base_log_baseline(a):
    return base_no_phi(a) + 0.5*np.log(np.maximum(a[:, 0] - PHI_C0, 1e-9))


def base_log_sat(a, phicP, phicS, delta):
    phi, p = a[:, 0], a[:, 6]
    g010 = 1.0/(1.0+np.exp(K_PS*(p - P_C)))
    phic = (1.0-g010)*phicP + g010*phicS
    pex = phi - phic
    return base_no_phi(a) + 0.5*np.log(np.sqrt(pex**2 + (delta*g010)**2) + 1e-12)


def cblend_fit(base, logsf, taus):
    """OLS fit of the two C_blend branches on the residual; returns (bv5, bp3)."""
    n = len(taus)
    w_v5 = 1.0/(1.0+np.exp(-KV5*(taus-CV5))); lt = np.log(taus)
    Xv5 = np.column_stack([np.ones(n), w_v5])
    Xp3 = np.column_stack([np.ones(n), lt, lt**2, lt**3])
    resid = logsf - base
    bv5, *_ = np.linalg.lstsq(Xv5, resid, rcond=None)
    bp3, *_ = np.linalg.lstsq(Xp3, resid, rcond=None)
    return bv5, bp3


def cblend_pred(base, taus, bv5, bp3):
    n = len(taus)
    w_v5 = 1.0/(1.0+np.exp(-KV5*(taus-CV5))); lt = np.log(taus)
    w_bl = 1.0/(1.0+np.exp(-KBL*(taus-CBL)))
    Xv5 = np.column_stack([np.ones(n), w_v5])
    Xp3 = np.column_stack([np.ones(n), lt, lt**2, lt**3])
    return base + (1-w_bl)*(Xv5@bv5) + w_bl*(Xp3@bp3)


def loocv_r2(base, logsf, taus):
    """Plain LOOCV R² for a FIXED base (no hyperparameter selection)."""
    n = len(taus); ss = np.sum((logsf-logsf.mean())**2); sse = 0.0
    for i in range(n):
        m = np.ones(n, bool); m[i] = False
        bv5, bp3 = cblend_fit(base[m], logsf[m], taus[m])
        pi = cblend_pred(base[i:i+1], taus[i:i+1], bv5, bp3)[0]
        sse += (logsf[i]-pi)**2
    return 1 - sse/ss


def _kfold_sse_sat(a, logsf, taus, phicP, phicS, delta, folds):
    """Inner K-fold validation SSE for one SAT hyperparameter combo."""
    sse = 0.0
    for val in folds:
        tr = np.ones(len(taus), bool); tr[val] = False
        b = base_log_sat(a, phicP, phicS, delta)
        bv5, bp3 = cblend_fit(b[tr], logsf[tr], taus[tr])
        pv = cblend_pred(b[val], taus[val], bv5, bp3)
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
        b = base_log_sat(a, pP, pS, dl)
        bv5, bp3 = cblend_fit(b[tr_idx], ls_tr, ta_tr)
        pi = cblend_pred(b[i:i+1], taus[i:i+1], bv5, bp3)[0]
        sse += (logsf[i]-pi)**2
    picks = np.array(picks)
    return 1 - sse/ss, picks


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


if __name__ == "__main__":
    main()
