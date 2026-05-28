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

# ── F / G: SMOOTH two-sigmoid form (no inequalities anywhere) ──────────────
# User's deeper critique 1: don't use the ps_ratio LABEL to determine which
# mode is "small" — use the actual r_AM_S / r_AM_P SIZES.
# User's deeper critique 2: indicator [r_AM < cutoff] in the form is inelegant;
# replace by a sigmoid for full differentiability.
# User's deeper critique 3: extend with the dimensionless r_AM/r_SE ratio for
# scale-invariance (form G).
#
# Math (no inequalities anywhere):
#
#   f_small  =  (1−p)·σ(K_1·(r_cut − r_AM,S))  +  p·σ(K_1·(r_cut − r_AM,P))     (F)
#   f_small  =  (1−p)·σ(K_1·(ρ_cut − r_AM,S/r_SE))  +  p·σ(K_1·(ρ_cut − r_AM,P/r_SE))  (G)
#   g_phys   =  σ(K_2·(f_small − 0.5))            ← replaces g010 in form A
#
# Both forms use the SAME outer sigmoid K_2 = 10 (matching g010), differing
# only in whether the inner sigmoid is on absolute size (F) or dimensionless
# size ratio (G).  All other base-form structure identical to form A.

CUTOFF_GRID    = np.array([3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0])           # F
RATIO_CUT_GRID = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0])     # G
K1_GRID        = np.array([2.0, 5.0, 10.0, 20.0])                       # inner sharpness


def _f_small_abs(a, cutoff, K1):
    """Form F smooth f_small: σ on absolute r_AM."""
    p = a[:, 6]
    r_AM_S = a[:, 17]; r_AM_P = a[:, 18]
    r_AM_eff = a[:, 13]
    # NaN backup using composition-weighted r_AM (rare in this corpus)
    rs = np.where(np.isfinite(r_AM_S), r_AM_S, r_AM_eff)
    rp = np.where(np.isfinite(r_AM_P), r_AM_P, r_AM_eff)
    sig_S = 1.0/(1.0+np.exp(-K1*(cutoff - rs)))
    sig_P = 1.0/(1.0+np.exp(-K1*(cutoff - rp)))
    return (1-p)*sig_S + p*sig_P


def _f_small_ratio(a, ratio_cut, K1):
    """Form G smooth f_small: σ on dimensionless r_AM / r_SE ratio."""
    p = a[:, 6]
    r_AM_S = a[:, 17]; r_AM_P = a[:, 18]; r_SE = a[:, 8]; r_AM_eff = a[:, 13]
    rs = np.where(np.isfinite(r_AM_S), r_AM_S, r_AM_eff)
    rp = np.where(np.isfinite(r_AM_P), r_AM_P, r_AM_eff)
    rse_med = float(np.nanmedian(r_SE[np.isfinite(r_SE)])) if np.isfinite(r_SE).any() else 0.5
    rse = np.where(np.isfinite(r_SE) & (r_SE > 0), r_SE, rse_med)
    sig_S = 1.0/(1.0+np.exp(-K1*(ratio_cut - rs/rse)))
    sig_P = 1.0/(1.0+np.exp(-K1*(ratio_cut - rp/rse)))
    return (1-p)*sig_S + p*sig_P


def base_log_smooth(a, f_small_fn, cutoff_or_ratio, K1, K2=10.0,
                    phicP=PHICP_F, phicS=PHICS_F, delta=DELTA_F):
    """Form A's structure with g010 replaced by σ(K_2·(f_small − 0.5))."""
    phi = a[:, 0]
    f = f_small_fn(a, cutoff_or_ratio, K1)
    g = 1.0/(1.0+np.exp(-K2*(f - 0.5)))
    phic = (1.0 - g)*phicP + g*phicS
    pex = phi - phic
    return base_no_phi(a) + 0.5*np.log(np.sqrt(pex**2 + (delta*g)**2) + 1e-12)


def nested_cv_smooth(a, logsf, taus, f_small_fn, cut_grid, label, k_inner=5, seed=0):
    """Outer-LOO + inner-k-fold scan of (cutoff/ratio, K1) jointly."""
    n = len(taus); ss = np.sum((logsf-logsf.mean())**2); sse = 0.0; picks = []
    rng = np.random.default_rng(seed)
    cf = cronau_factor(a[:, 8])
    for i in range(n):
        tr = np.array([j for j in range(n) if j != i])
        ls_tr, ta_tr = logsf[tr], taus[tr]
        order = rng.permutation(len(tr)); folds = [order[f::k_inner] for f in range(k_inner)]
        best, best_sse = None, np.inf
        for ct in cut_grid:
            for K1 in K1_GRID:
                b = base_log_smooth(a[tr], f_small_fn, float(ct), float(K1)) + np.log(cf[tr])
                fsse = 0.0
                for val in folds:
                    m = np.ones(len(tr), bool); m[val] = False
                    bv5, bp3 = cblend_fit(b[m], ls_tr[m], ta_tr[m])
                    pv = cblend_pred(b[val], ta_tr[val], bv5, bp3)
                    fsse += np.sum((ls_tr[val]-pv)**2)
                if fsse < best_sse:
                    best_sse, best = fsse, (float(ct), float(K1))
        picks.append(best)
        ct, K1 = best
        b = base_log_smooth(a, f_small_fn, ct, K1) + np.log(cf)
        bv5, bp3 = cblend_fit(b[tr], ls_tr, ta_tr)
        pi = cblend_pred(b[i:i+1], taus[i:i+1], bv5, bp3)[0]
        sse += (logsf[i]-pi)**2
    return 1 - sse/ss, picks


# ── D / E: r_AM-bundled gating (replace g010 entirely) ─────────────────────
# Physical hypothesis: g010 in form A bundles "AM particle is small AND
# polydisperse" via the P:S label.  The real variable is the AM particle
# size (or the SE/AM size ratio).  D and E replace g010 with a sigmoid
# gate over that physical variable, keeping the rest of form A intact.

R_AM_REF_GRID = np.round(np.linspace(0.4, 1.4, 11), 2)   # crossover AM size (µm)
K_R_GRID      = np.array([5.0, 10.0, 20.0])              # sigmoid sharpness
RATIO_REF_GRID = np.round(np.linspace(0.3, 1.5, 7), 2)   # crossover r_SE/r_AM


def _g_size_rAM(a, r_ref, K_r):
    """g_size = σ(K_r·(r_ref − r_AM_eff))  →  ≈1 for small AM, ≈0 for large.
    NaN r_AM → returns 0.5 (neutral, no preference)."""
    ram = a[:, 13]
    ram_med = float(np.nanmedian(ram[np.isfinite(ram)])) if np.isfinite(ram).any() else 1.0
    ram_safe = np.where(np.isfinite(ram) & (ram > 0), ram, ram_med)
    return 1.0/(1.0+np.exp(-K_r*(r_ref - ram_safe)))


def _g_size_ratio(a, ratio_ref, K_r):
    """g_size based on r_SE/r_AM size ratio (geometric packing efficiency).
    σ(K_r·(ratio_ref − ratio))  →  ≈1 for small ratio (small SE / big AM),
    ≈0 for large ratio (SE comparable to AM).  Matches g010 phenomenology
    because pure AM_S (small AM) → high ratio; but NO P/S label dependence."""
    rse = a[:, 8]; ram = a[:, 13]
    rse_med = float(np.nanmedian(rse[np.isfinite(rse)])) if np.isfinite(rse).any() else 0.5
    ram_med = float(np.nanmedian(ram[np.isfinite(ram)])) if np.isfinite(ram).any() else 1.0
    rse_s = np.where(np.isfinite(rse) & (rse > 0), rse, rse_med)
    ram_s = np.where(np.isfinite(ram) & (ram > 0), ram, ram_med)
    ratio = rse_s / ram_s
    return 1.0/(1.0+np.exp(-K_r*(ratio_ref - ratio)))


def base_log_bundle(a, phicP, phicS, delta, gate_fn, **gate_kw):
    """Form A's structure with g010 replaced by a custom `gate_fn(a, **gate_kw)`."""
    phi = a[:, 0]
    g = gate_fn(a, **gate_kw)
    phic = (1.0 - g)*phicP + g*phicS
    pex = phi - phic
    return base_no_phi(a) + 0.5*np.log(np.sqrt(pex**2 + (delta*g)**2) + 1e-12)


def nested_cv_bundle(a, logsf, taus, gate_fn, gate_grid, k_inner=5, seed=0):
    """Outer-LOO + inner-k-fold scan of bundle hyperparam (r_ref, K_r);
    φc_P / φc_S / δ are frozen at A's production values to make the comparison
    apples-to-apples (only the GATE differs vs form A)."""
    n = len(taus); ss = np.sum((logsf-logsf.mean())**2); sse = 0.0; picks = []
    rng = np.random.default_rng(seed)
    cf = cronau_factor(a[:, 8])
    for i in range(n):
        tr = np.array([j for j in range(n) if j != i])
        ls_tr, ta_tr = logsf[tr], taus[tr]
        order = rng.permutation(len(tr)); folds = [order[f::k_inner] for f in range(k_inner)]
        best, best_sse = None, np.inf
        for gp in gate_grid:
            b = base_log_bundle(a[tr], PHICP_F, PHICS_F, DELTA_F, gate_fn, **gp) + np.log(cf[tr])
            fsse = 0.0
            for val in folds:
                m = np.ones(len(tr), bool); m[val] = False
                bv5, bp3 = cblend_fit(b[m], ls_tr[m], ta_tr[m])
                pv = cblend_pred(b[val], ta_tr[val], bv5, bp3)
                fsse += np.sum((ls_tr[val]-pv)**2)
            if fsse < best_sse:
                best_sse, best = fsse, dict(gp)
        picks.append(best)
        b = base_log_bundle(a, PHICP_F, PHICS_F, DELTA_F, gate_fn, **best) + np.log(cf)
        bv5, bp3 = cblend_fit(b[tr], ls_tr, ta_tr)
        pi = cblend_pred(b[i:i+1], taus[i:i+1], bv5, bp3)[0]
        sse += (logsf[i]-pi)**2
    return 1 - sse/ss, picks


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

    # D. A's structure but g010 replaced by g_size(r_AM) — physical bundling
    gate_grid_D = [{'r_ref': r, 'K_r': k} for r in R_AM_REF_GRID for k in K_R_GRID]
    lo_D, picks_D = nested_cv_bundle(a, logsf, taus, _g_size_rAM, gate_grid_D)

    # E. g_size(r_SE/r_AM) — size ratio bundling (geometric packing variable)
    gate_grid_E = [{'ratio_ref': r, 'K_r': k} for r in RATIO_REF_GRID for k in K_R_GRID]
    lo_E, picks_E = nested_cv_bundle(a, logsf, taus, _g_size_ratio, gate_grid_E)

    # F. SMOOTH two-sigmoid with absolute r_AM cutoff (label-free, differentiable)
    lo_F, picks_F = nested_cv_smooth(a, logsf, taus, _f_small_abs, CUTOFF_GRID, "F")
    # G. SMOOTH two-sigmoid with r_AM/r_SE ratio (scale-invariant)
    lo_G, picks_G = nested_cv_smooth(a, logsf, taus, _f_small_ratio, RATIO_CUT_GRID, "G")

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
    print(f"  D. r_AM-gated BUNDLE:           LOOCV = {lo_D:.4f}    "
          f"Δ vs A = {lo_D-lo_A:+.4f}   [g010 → g_size(r_AM)]")
    print(f"  E. r_SE/r_AM ratio BUNDLE:      LOOCV = {lo_E:.4f}    "
          f"Δ vs A = {lo_E-lo_A:+.4f}   [g010 → g_size(r_SE/r_AM)]")
    print(f"  F. SMOOTH abs cutoff (label-free): LOOCV = {lo_F:.4f}    "
          f"Δ vs A = {lo_F-lo_A:+.4f}   [f=(1-p)·σ(K(c-rS))+p·σ(K(c-rP))]")
    print(f"  G. SMOOTH ratio cutoff (scale-inv): LOOCV = {lo_G:.4f}    "
          f"Δ vs A = {lo_G-lo_A:+.4f}   [f using r_AM/r_SE]")
    print()
    # (cutoff, K1) pick distributions for F, G
    def _summ(label, picks):
        cts = [p[0] for p in picks]; k1s = [p[1] for p in picks]
        vv_c, cc_c = np.unique(np.round(cts, 2), return_counts=True)
        vv_k, cc_k = np.unique(np.round(k1s, 1), return_counts=True)
        top_c = sorted(zip(cc_c, vv_c), reverse=True)[:4]
        top_k = sorted(zip(cc_k, vv_k), reverse=True)[:3]
        print(f"  inner-picked ({label}) cutoff: " + ", ".join(f"{v}×{c}" for c, v in top_c))
        print(f"  inner-picked ({label}) K_1:    " + ", ".join(f"{v}×{c}" for c, v in top_k))
    _summ("F", picks_F)
    _summ("G", picks_G)
    print()

    def _summarize_picks(label, picks, keys):
        for k in keys:
            vals = [p[k] for p in picks]
            vv, cc = np.unique(np.round(vals, 3), return_counts=True)
            top = sorted(zip(cc, vv), reverse=True)[:4]
            print(f"  {label}  {k:>9s}: " + ", ".join(f"{v}×{c}" for c, v in top))

    # κ pick distribution for C
    vv, cc = np.unique(np.round(picks, 4), return_counts=True)
    top = sorted(zip(cc, vv), reverse=True)[:5]
    print(f"  inner-picked κ (C):  " + ", ".join(f"{v:+.3f}×{c}" for c, v in top))
    _summarize_picks("inner-picked (D)", picks_D, ['r_ref', 'K_r'])
    _summarize_picks("inner-picked (E)", picks_E, ['ratio_ref', 'K_r'])
    print()
    print("Verdict guide:")
    print("  • D or E within noise SE of A → BUNDLED form preserves performance")
    print("    AND removes AM_P/AM_S convention dependence → ADOPT (more physical)")
    print("  • D or E exceeds A by > SE   → bundling gives genuine improvement")
    print("  • B/C significantly worse    → confirms blend does real work (already known)")
    print("  • If all of B, C, D, E lose  → A is the right form; document that g010")
    print("    is a CONVENIENT PROXY for AM size disorder, not a P/S label dependence")

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
