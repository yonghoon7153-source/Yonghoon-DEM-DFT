#!/usr/bin/env python3
"""Test whether the g₀₁₀-based φ_c blend (current production) is doing real work,
or whether dropping it / replacing it with an r_AM-dependent threshold is
physically cleaner AND empirically equivalent.

The g₀₁₀ blend (φ_c,P=0.200 vs φ_c,S=0.195, weighted by P:S sigmoid) is
suspect because the AM_P / AM_S distinction is a SIZE-LABEL CONVENTION,
not a material property: a monomodal system with a single AM size can be
labeled either way.  Three threshold-form variants are nested-CV compared:

    A.  current  — g₀₁₀-blend         (production; φ_c,P=0.200, φ_c,S=0.195)
    B.  simple   — single threshold   (φ_c = 0.195 frozen, δ always active)
    C.  r_AM-blend — φ_c(r_AM)        (physics-grounded: threshold depends on
                                       AM particle size, not on P/S label)

For C we scan the slope κ and use the best κ chosen per-fold by inner CV
(no selection bias).

Run from the repo root:  python3 scripts/test_threshold_form.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
from nested_cv_sat import (load_corpus, base_log_sat, base_no_phi, loocv_r2,
                           cblend_fit, cblend_pred, cronau_factor,
                           PHICP_F, PHICS_F, DELTA_F, K_PS, P_C)


PHI_C_SINGLE = 0.195         # B: simple single threshold (matches the φ_c,S-end)


def base_log_simple(a, phi_c=PHI_C_SINGLE, delta=DELTA_F):
    """B: single fixed threshold, no g₀₁₀ blend; δ always active."""
    phi = a[:, 0]
    pex = phi - phi_c
    return base_no_phi(a) + 0.5*np.log(np.sqrt(pex**2 + delta**2) + 1e-12)


def base_log_rAM(a, phi_c0=PHI_C_SINGLE, kappa=0.0, delta=DELTA_F):
    """C: physics-grounded — threshold modulates with composition-weighted
    AM particle size r_AM_um (column 13).  φ_c(r_AM) = phi_c0 + κ·log(r_AM/r_ref)
    with r_ref = 1.0 µm.  κ=0 reduces to form B."""
    phi = a[:, 0]
    ram = a[:, 13]
    # NaN r_AM → use median (neutral)
    if np.isfinite(ram).any():
        med = float(np.nanmedian(ram[np.isfinite(ram)]))
    else:
        med = 1.0
    ram_safe = np.where(np.isfinite(ram) & (ram > 0), ram, med)
    phi_c_eff = phi_c0 + kappa * np.log(ram_safe / 1.0)
    pex = phi - phi_c_eff
    return base_no_phi(a) + 0.5*np.log(np.sqrt(pex**2 + delta**2) + 1e-12)


KAPPA_GRID = np.round(np.linspace(-0.05, 0.05, 11), 4)


def nested_cv_kappa(a, logsf, taus, k_inner=5, seed=0):
    """Outer-LOO + inner-k-fold selection of κ for the r_AM-blend (form C)."""
    n = len(taus); ss = np.sum((logsf-logsf.mean())**2); sse = 0.0; picks = []
    rng = np.random.default_rng(seed)
    cf = cronau_factor(a[:, 8])
    for i in range(n):
        tr = np.array([j for j in range(n) if j != i])
        ls_tr, ta_tr = logsf[tr], taus[tr]
        order = rng.permutation(len(tr)); folds = [order[f::k_inner] for f in range(k_inner)]
        best, best_sse = None, np.inf
        for kappa in KAPPA_GRID:
            b = base_log_rAM(a[tr], kappa=float(kappa)) + np.log(cf[tr])
            fsse = 0.0
            for val in folds:
                m = np.ones(len(tr), bool); m[val] = False
                bv5, bp3 = cblend_fit(b[m], ls_tr[m], ta_tr[m])
                pv = cblend_pred(b[val], ta_tr[val], bv5, bp3)
                fsse += np.sum((ls_tr[val]-pv)**2)
            if fsse < best_sse:
                best_sse, best = fsse, float(kappa)
        picks.append(best)
        b = base_log_rAM(a, kappa=best) + np.log(cf)
        bv5, bp3 = cblend_fit(b[tr], ls_tr, ta_tr)
        pi = cblend_pred(b[i:i+1], taus[i:i+1], bv5, bp3)[0]
        sse += (logsf[i]-pi)**2
    return 1 - sse/ss, picks


def main():
    a = load_corpus()
    n = len(a)
    if n < 20:
        print(f"[ABORT] only {n} cases."); return
    logsf = np.log(a[:, 5]); taus = a[:, 4]
    ss = np.sum((logsf-logsf.mean())**2)
    se_loocv = np.sqrt(np.var((logsf-logsf.mean())**2)/n) / ss

    cf = cronau_factor(a[:, 8])

    # A. Current production: g₀₁₀ blend (frozen)
    base_A = base_log_sat(a, PHICP_F, PHICS_F, DELTA_F) + np.log(cf)
    lo_A = loocv_r2(base_A, logsf, taus)

    # B. Simple single threshold (no blend, δ always active)
    base_B = base_log_simple(a) + np.log(cf)
    lo_B = loocv_r2(base_B, logsf, taus)

    # C. r_AM-dependent threshold (nested-CV pick κ)
    lo_C, picks = nested_cv_kappa(a, logsf, taus)

    n_ram = int(np.isfinite(a[:, 13]).sum())

    print("=" * 78)
    print(f"Threshold-form comparison  (n={n}; r_AM available in {n_ram}/{n} cases)")
    print("=" * 78)
    print(f"  rough LOOCV noise SE  : {se_loocv:.4f}")
    print()
    print(f"  A. g₀₁₀ blend (production):    LOOCV = {lo_A:.4f}    "
          f"[φ_c,P=0.200, φ_c,S=0.195, δ·g₀₁₀]")
    print(f"  B. single threshold (no blend): LOOCV = {lo_B:.4f}    "
          f"Δ vs A = {lo_B-lo_A:+.4f}   [φ_c=0.195, δ always]")
    print(f"  C. r_AM-blend (κ inner-CV):     LOOCV = {lo_C:.4f}    "
          f"Δ vs A = {lo_C-lo_A:+.4f}   [φ_c(r_AM) = 0.195 + κ·ln(r_AM)]")
    print()
    # κ pick distribution
    vv, cc = np.unique(np.round(picks, 4), return_counts=True)
    top = sorted(zip(cc, vv), reverse=True)[:5]
    print(f"  inner-picked κ:  " + ", ".join(f"{v:+.3f}×{c}" for c, v in top))
    print(f"  mean κ across folds: {np.mean(picks):+.4f}   "
          f"std = {np.std(picks):.4f}")
    print()
    print("Verdict guide:")
    print("  • If |Δ_B − Δ_A| < noise SE  → blend is doing nothing;  DROP IT (form B)")
    print("    (simpler, removes the AM_P/AM_S convention dependence)")
    print("  • If C wins by > noise SE   → real r_AM dependence;  ADOPT C")
    print("    (physics-grounded: AM particle size affects SE percolation threshold)")
    print("  • If neither wins           → keep A but document that the blend")
    print("    is empirical and has tiny effect; possibly retire φ_c,P=0.200 anyway")
    print("    (87/91 inner folds already prefer 0.195)")

    # Effective-sigmoid sanity check: print how p distributes across the corpus
    print()
    print("Corpus composition snapshot (p = AM_P / (AM_P+AM_S)):")
    p_arr = a[:, 6]
    bins = [(0.0, 0.05, "0:10 (pure AM_S)"),
            (0.05, 0.30, "S-heavy mixed"),
            (0.30, 0.70, "balanced mixed"),
            (0.70, 0.95, "P-heavy mixed"),
            (0.95, 1.01, "10:0 (pure AM_P)")]
    for lo, hi, lab in bins:
        nn = int(((p_arr >= lo) & (p_arr < hi)).sum())
        print(f"   {lab:30s} : {nn:3d}/{n}")


if __name__ == "__main__":
    main()
