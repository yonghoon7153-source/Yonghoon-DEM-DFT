#!/usr/bin/env python3
"""Test if σ_electronic LOOCV ≈ 0.48 ceiling is outlier-driven OR form-limited.

resid_scan revealed NO single predictor with |ρ|>0.3 — all 211 candidate
metrics had weak diffuse signals.  Two possible interpretations:

  (i)  The ceiling is driven by 2-3 wild outliers (σ_e=55-68 cases like
       1mAh_100_2, _3) — removing them would jump LOOCV substantially,
       revealing the rest of the data has cleaner structure.

  (ii) The σ_e data is fundamentally noisier than σ_ionic (Stage E
       pipeline issues, AM-AM physics intrinsically more complex).
       Removing outliers doesn't help — LOOCV stays ~0.5.

This script tries 4 removal strategies and reports LOOCV at each:
  • Strategy A: σ_e cap at 30 mS/cm  (2× literature poly-NCM composite max)
  • Strategy B: σ_e cap at 20 mS/cm  (tighter)
  • Strategy C: drop top-K |residual| outliers, K ∈ {3, 5, 10}
  • Strategy D: drop both σ_e>30 AND high-resid (combined)

If strategy A or B gives LOOCV > 0.7 → ceiling was outlier-driven.
If all strategies leave LOOCV < 0.6 → form is genuinely at limit.

Run on WSL:
    python3 scripts/electronic_outlier_impact.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
from electronic_nested_cv import load_corpus_e, SIGMA_AM


def stage4_fit(a, logsf):
    """Stage 4 form: log σ_e = log σ_AM + a·log φ + d·log f_p + β_P·p_amp
                              + β_r·log r̄_AM + β_T·log T/d + p + q·ln τ + r·ln²τ.
    Returns (coef, pred_log, r2, loocv, ae)."""
    n = len(a)
    phi_am = a[:, 0]; cn = a[:, 1]; fp = a[:, 3]
    tau = a[:, 4]; p_amp = a[:, 6]
    r_AM_S = a[:, 8]; r_AM_P = a[:, 9]; T_um = a[:, 10]
    r_eff = np.where(np.isfinite(r_AM_S), r_AM_S, 2.5)
    r_eff_P = np.where(np.isfinite(r_AM_P), r_AM_P, 5.5)
    r_eff = (1.0 - p_amp)*r_eff + p_amp*r_eff_P
    T_safe = np.where(np.isfinite(T_um) & (T_um > 0), T_um, 100.0)
    d_AM = 2.0 * r_eff
    log_r = np.log(np.maximum(r_eff, 0.5))
    log_Td = np.log(np.maximum(T_safe / d_AM, 0.1))
    lt = np.log(tau)
    X = np.column_stack([
        np.log(phi_am), np.log(fp), p_amp, log_r, log_Td,
        np.ones(n), lt, lt**2,
    ])
    y = logsf - np.log(SIGMA_AM)
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ coef
    ss_tot = np.sum((y - y.mean())**2)
    ss_res = np.sum((y - pred)**2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    sse_loo = 0.0
    for i in range(n):
        m = np.ones(n, bool); m[i] = False
        c_loo, *_ = np.linalg.lstsq(X[m], y[m], rcond=None)
        sse_loo += (y[i] - X[i] @ c_loo)**2
    lo = 1 - sse_loo / ss_tot if ss_tot > 0 else 0
    pred_log = pred + np.log(SIGMA_AM)
    err = (np.exp(pred_log) - np.exp(logsf)) / np.exp(logsf) * 100
    return coef, pred_log, r2, lo, err


def main():
    print("=" * 78)
    print(" σ_electronic — is the 0.48 LOOCV ceiling outlier-driven?")
    print("=" * 78)
    a_full, names_full = load_corpus_e()
    n_full = len(a_full)
    logsf_full = np.log(a_full[:, 5])
    sig_full = a_full[:, 5]
    print(f"  Baseline corpus n = {n_full}")
    print(f"  σ_e range : {sig_full.min():.4f} ~ {sig_full.max():.1f} mS/cm")
    print()

    # ───── Baseline: full corpus, Stage 4 form ─────
    _coef0, _pred0, r2_0, lo_0, err_0 = stage4_fit(a_full, logsf_full)
    print(f"  Baseline (full n={n_full}):  R² = {r2_0:.4f}  LOOCV = {lo_0:.4f}")
    print()

    # ───── Strategy A: σ_e cap ─────
    print("─" * 78)
    print(" Strategy A: σ_e cap (drop cases above threshold)")
    print("─" * 78)
    for cap in [50, 30, 25, 20, 15]:
        m = sig_full <= cap
        a_c = a_full[m]; logsf_c = logsf_full[m]
        if len(a_c) < 10:
            print(f"  σ_e ≤ {cap:>3.0f}  n={len(a_c):>3d}  [too small]")
            continue
        _c, _p, r2, lo, _e = stage4_fit(a_c, logsf_c)
        drop_n = n_full - len(a_c)
        flag = "  ★ outlier-driven" if lo > 0.7 else ("  ←" if lo > 0.6 else "")
        print(f"  σ_e ≤ {cap:>3.0f}  n={len(a_c):>3d} (-{drop_n})  "
              f"R² = {r2:6.4f}  LOOCV = {lo:7.4f}{flag}")
    print()

    # ───── Strategy C: drop top-K |residual| outliers ─────
    print("─" * 78)
    print(" Strategy C: drop top-K largest-|residual| cases on the BASELINE fit")
    print("─" * 78)
    abs_err = np.abs(err_0)
    abs_resid_log = np.abs(logsf_full - _pred0)
    for K in [3, 5, 10, 15, 20]:
        order = np.argsort(-abs_resid_log)
        drop_idx = set(order[:K].tolist())
        keep = np.array([i not in drop_idx for i in range(n_full)])
        a_k = a_full[keep]; logsf_k = logsf_full[keep]
        _c, _p, r2, lo, _e = stage4_fit(a_k, logsf_k)
        flag = "  ★ outlier-driven" if lo > 0.7 else ("  ←" if lo > 0.6 else "")
        print(f"  drop K={K:>2d}  n={n_full-K:>3d}  "
              f"R² = {r2:6.4f}  LOOCV = {lo:7.4f}{flag}")
    print()

    # ───── Strategy D: combined σ_e ≤ 30 AND drop top-5 residuals ─────
    print("─" * 78)
    print(" Strategy D: combined — σ_e ≤ 30 AND drop top-5 |residual| within that")
    print("─" * 78)
    m1 = sig_full <= 30
    a_d = a_full[m1]; logsf_d = logsf_full[m1]
    if len(a_d) > 10:
        _c, _p, r2d, lod, errd = stage4_fit(a_d, logsf_d)
        abs_rd = np.abs(logsf_d - _p)
        order = np.argsort(-abs_rd)
        keep2 = np.array([i not in set(order[:5].tolist()) for i in range(len(a_d))])
        a_d2 = a_d[keep2]; logsf_d2 = logsf_d[keep2]
        _c2, _p2, r2d2, lod2, _ = stage4_fit(a_d2, logsf_d2)
        print(f"  σ_e ≤ 30           n={len(a_d):>3d}  R² = {r2d:6.4f}  LOOCV = {lod:7.4f}")
        print(f"  σ_e ≤ 30 + drop 5  n={len(a_d2):>3d}  R² = {r2d2:6.4f}  LOOCV = {lod2:7.4f}")
    print()

    # ───── Show top dropped cases ─────
    print("─" * 78)
    print(" Cases that would be excluded (showing the 10 with largest |residual|)")
    print("─" * 78)
    abs_resid_log = np.abs(logsf_full - _pred0)
    order = np.argsort(-abs_resid_log)[:10]
    print(f"  {'case':32s}  {'σ_DEM':>7s}  {'σ_form':>7s}  {'err%':>8s}  {'|resid log|':>10s}")
    for i in order:
        nm = names_full[i] if i < len(names_full) else f"(idx{i})"
        sigma_form = float(np.exp(_pred0[i]))
        print(f"  {nm[:32]:32s}  {sig_full[i]:7.3f}  {sigma_form:7.3f}  "
              f"{err_0[i]:+8.1f}  {abs_resid_log[i]:10.2f}")
    print()

    # ───── Verdict ─────
    print("=" * 78)
    print(" VERDICT")
    print("=" * 78)
    # Find best LOOCV across all strategies
    # Quick re-run to get the best
    best_lo = lo_0; best_strat = "baseline"
    for cap in [50, 30, 25, 20, 15]:
        m = sig_full <= cap
        if m.sum() >= 10:
            _, _, _, lo, _ = stage4_fit(a_full[m], logsf_full[m])
            if lo > best_lo:
                best_lo = lo; best_strat = f"σ_e cap {cap}"
    for K in [3, 5, 10, 15, 20]:
        order = np.argsort(-np.abs(logsf_full - _pred0))
        keep = np.array([i not in set(order[:K].tolist()) for i in range(n_full)])
        _, _, _, lo, _ = stage4_fit(a_full[keep], logsf_full[keep])
        if lo > best_lo:
            best_lo = lo; best_strat = f"drop top-{K}"
    print(f"  Baseline LOOCV:    {lo_0:.4f}")
    print(f"  Best strategy:     {best_strat} → LOOCV = {best_lo:.4f}")
    print(f"  Improvement:       Δ = {best_lo - lo_0:+.4f}")
    print()
    if best_lo > 0.75:
        print("  → CEILING WAS OUTLIER-DRIVEN.  Remove flagged cases (with audit",
              "trail in _EXCLUDED_NAMES_EL) and proceed to σ_ionic-style finalization.")
    elif best_lo > 0.65:
        print("  → PARTIALLY outlier-driven.  Outlier removal helps but form still")
        print("    has structural limit.  Worth excluding the worst few, then accept")
        print("    moderate LOOCV ceiling.")
    elif best_lo - lo_0 > 0.10:
        print("  → Outliers contribute but ceiling is form-limited.  Document the")
        print("    σ_e form as 'noisier than σ_ionic; LOOCV ~0.5-0.6 is expected'.")
    else:
        print("  → CEILING IS FORM-LIMITED, not outlier-driven.  σ_e data has")
        print("    intrinsic structure the current feature set can't capture.")
        print("    Path forward: upstream Stage E electronic pipeline audit, or")
        print("    accept σ_e at LOOCV ~0.48 and use Bayesian PI for honest reporting.")


if __name__ == '__main__':
    main()
