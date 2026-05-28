#!/usr/bin/env python3
"""Current σ_ionic production form — final equation + error breakdown.

Prints the equation explicitly, layer-by-layer LOOCV improvements (so you
can see how each component contributes), per-case error distribution, and
the residual outlier list classified by type (corner-bulk, sub-µm, mixed,
etc.).  Use this as the canonical "where are we now" snapshot.

Run from the repo root:  python3 scripts/final_form_status.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
import generate_comparison_plots as gcp  # noqa
from nested_cv_sat import (load_corpus, base_log_sat, base_log_baseline, base_no_phi,
                           loocv_r2, cblend_fit, cblend_pred, cronau_factor,
                           _meta_name, _EXCLUDED_NAMES,
                           PHICP_F, PHICS_F, DELTA_F, K_PS, P_C, SG, PHI_C0)
from pathlib import Path as _P


EQUATION = r"""
σ_ionic = σ_grain · Cronau(r_SE) · (φ_eff)^½ · CN² · cov_physics^½ · f_p³
          · exp[a + b·ln τ + c·(ln τ)² + β_P2·P2 + β_cov·Δcov + β_F·log f_intact]

  ┌───────────────────────────────────────────────────────────────────────┐
  │ FROZEN (literature / physics-derived)                                  │
  ├───────────────────────────────────────────────────────────────────────┤
  │ σ_grain   = 3.0 mS/cm  Cronau 2022 Li6PS5Cl single-crystal     HIGH   │
  │ Cronau(r) = 0.33 + 0.32σ(50(r−0.10))                                  │
  │                + 0.25σ(50(r−0.30))                                    │
  │                + 0.10σ(50(r−0.50))     smooth 3-sigmoid        HIGH   │
  │ exponents (½, 2, ½, 3) for (φ_eff, CN, cov, f_p)   data-locked        │
  │ φc_P=0.200  φc_S=0.195  δ=0.040        joint screen on full corpus    │
  │ r_cut=3.5µm  α=2                       audit-midpoint AM_S/AM_P gap   │
  │                                        + Alt-C power scan optimum     │
  ├───────────────────────────────────────────────────────────────────────┤
  │ LIVE-fit (6 OLS params per corpus build)                              │
  ├───────────────────────────────────────────────────────────────────────┤
  │ a, b, c   tortuosity logpoly2: C(τ) = a + b·ln τ + c·(ln τ)²          │
  │ β_P2      bulk-grain corner enhancement amplitude                     │
  │ β_cov     Hertz→physics amplification gap (centered Δcov)             │
  │ β_F       fracture-aware partial-Holm exponent  (data → ≈ +0.19)      │
  └───────────────────────────────────────────────────────────────────────┘

Sub-definitions:
  φ_eff      = √[(φ − φc_eff)² + (δ · g_phys)²]
  φc_eff     = (1 − g_phys)·φc_P + g_phys·φc_S
  g_phys     = (min(r_cut / r̄_AM, 1))^α    ← power-law size gate (Alt-C)
  r̄_AM      = (1 − p)·r_AM,S + p·r_AM,P     ← composition-weighted AM radius
  P_2        = g_phys · (φ − φc_S)² · (r_SE − 0.5)+    ← Cronau super-µm arm
  Δcov       = coverage_AM_delta_pct_rough − median(…)  ← Tabor amplification gap
  f_intact   = 1 − fracture_aware_excluded_pct / 100   ← intact contact fraction

Per-term meaning:
  σ_grain · Cronau  — material baseline (Cronau 2022 literature)
  (φ_eff)^½         — mean-field 3D percolation, well-above-threshold
  CN²               — Kirchhoff #paths × bond-strength (Holm parallel paths)
  cov_physics^½     — Holm 1967 constriction at Tabor-corrected contact area
                       (T1 'cov_Hertz' base attempted 2026-05-28, REVERTED —
                       caused visible plot over-prediction & worse outliers)
  f_p³              — 3D isotropy: P(percolate-x ∧ y ∧ z) = f_p³
  C(τ)              — tortuosity path-length, logpoly2 (beats dual-branch by ΔAIC −10.6)
  β_P2·P2           — bulk-grain regime extension beyond Cronau's 0.5µm plateau
                       (catches 62:38 D1+ corner; PASSED leave-corner-out)
  β_cov·Δcov        — empirical correction for Hertz→physics inflation extremes
  β_F·log f_intact  — fracture-induced contact loss (β≈0.19 partial-Holm)
  g_phys (power)    — label-free 'small-AM dominance', inverse-square scaling

Other inputs:
  φ      = SE volume fraction (= phi_se)
  CN     = SE-SE coordination number (= se_se_cn)
  cov    = SE-SE covered area fraction (PHYSICS — Tabor-corrected)
  f_p    = percolation fraction (= percolation_pct/100)
  τ      = recommended tortuosity (= tortuosity_recommended)
  p      = AM_P / (AM_P + AM_S) volume fraction
  r_SE   = SE radius in µm (design input)
  r_AM_S, r_AM_P = smaller / larger AM radius in µm
"""


def main():
    a = load_corpus()
    n = len(a)
    if n < 20:
        print(f"[ABORT] only {n} cases."); return
    logsf = np.log(a[:, 5]); taus = a[:, 4]
    ss = np.sum((logsf-logsf.mean())**2)

    # ===== EQUATION ============================================================
    print("=" * 78)
    print(" CURRENT PRODUCTION FORM (Stage-E σ_ionic) — FROZEN HYPERPARAMS")
    print("=" * 78)
    print(EQUATION)
    if _EXCLUDED_NAMES:
        print(f" Excluded as per-seed anomalies ({len(_EXCLUDED_NAMES)}): "
              + ", ".join(sorted(_EXCLUDED_NAMES)))
        print(" (siblings at same design point cluster, this seed is half their median)")
    print(f" Corpus used here: n = {n}\n")

    # ===== LAYER-BY-LAYER LOOCV =================================================
    print("=" * 78)
    print(" Layer-by-layer LOOCV — what each component buys")
    print("=" * 78)
    # baseline (bare √, φc=0.19, no Cronau)
    base_b = base_log_baseline(a)
    lo_b = loocv_r2(base_b, logsf, taus)
    # SAT-blend (frozen φc/δ, no Cronau)
    base_s = base_log_sat(a, PHICP_F, PHICS_F, DELTA_F)
    lo_s = loocv_r2(base_s, logsf, taus)
    # SAT × Cronau (previous production = "C0")
    cf = cronau_factor(a[:, 8])
    base_sc = base_s + np.log(cf)
    lo_sc = loocv_r2(base_sc, logsf, taus)
    # C4 augmented (NEW PRODUCTION): + β_P2·P2 + β_cov·Δcov
    from nested_cv_sat import production_extras
    extras_c4, _med = production_extras(a)
    lo_c4 = loocv_r2(base_sc, logsf, taus, extras=extras_c4)
    # error in % bands at each layer
    def fit_and_err(base, extras=None):
        b = cblend_fit(base, logsf, taus, extras=extras)
        pred = cblend_pred(base, taus, b, extras=extras)
        err_pct = (np.exp(pred) - np.exp(logsf)) / np.exp(logsf) * 100.0
        return pred, err_pct
    pred_b, err_b = fit_and_err(base_b)
    pred_s, err_s = fit_and_err(base_s)
    pred_sc, err_sc = fit_and_err(base_sc)
    pred_c4, err_c4 = fit_and_err(base_sc, extras=extras_c4)

    def _bands(err):
        ae = np.abs(err)
        return {f"|err|≤10%": float((ae <= 10).mean()*100),
                f"|err|≤20%": float((ae <= 20).mean()*100),
                f"|err|≤30%": float((ae <= 30).mean()*100),
                f"|err|>50%": float((ae > 50).sum()),
                f"|err|>30%": float((ae > 30).sum())}

    print(f"  {'Layer':32s}{'LOOCV':>9s}{'Δ vs prev':>11s}    "
          f"{'≤10%':>5s} {'≤20%':>5s} {'≤30%':>5s} | "
          f"{'>30%':>4s} {'>50%':>4s}")
    for tag, lo, prev, err in (
            ("Baseline (bare √φ−0.19)", lo_b, None, err_b),
            ("+ SAT-blend (φc_eff, δ)", lo_s, lo_b, err_s),
            ("× Cronau(r_SE)", lo_sc, lo_s, err_sc),
            ("× C5 (P2 + Δcov + f_intact)   ← PRODUCTION", lo_c4, lo_sc, err_c4)):
        b = _bands(err)
        dv = f"{lo-prev:+.4f}" if prev is not None else "  —  "
        print(f"  {tag:32s}{lo:9.4f}{dv:>11s}    "
              f"{b['|err|≤10%']:>4.0f}% {b['|err|≤20%']:>4.0f}% {b['|err|≤30%']:>4.0f}% | "
              f"{int(b['|err|>30%']):>4d} {int(b['|err|>50%']):>4d}")
    print()

    # ===== TESTED EXTRA TERMS — what we ruled OUT =====================================
    print("=" * 78)
    print(" Extra terms TESTED on top of production (none adopted yet)")
    print("=" * 78)
    print("   ── failed nested-CV ──")
    print("     • am_se_cn (gated/ungated), coverage variants, r_SE/r_AM ratio")
    print("     • sub-µm GB penalty (Cronau-mirror), log r_SE size alone")
    print("     • CN exponent scan (locked 91/91 at CN^2.0)")
    print("     • cov exponent scan (locked at cov^0.5)")
    print("     • exp_S (0:10 percolation exponent — locked 91/91 at 0.5)")
    print("     • path_hop_area, se_se_cn_eff_area, stress_cv (corr signals diluted)")
    print("     • τ-exp variants, CN-exp variants, (1−exp(−α·(φ−φc)))")
    print("     • Q (CN^(2+κ·r_SE)), R (cov^(0.5+κ·r_SE)), O (φ_eff exponent)")
    print("   ── PROVISIONAL leads (nested-CV PASS, but [6] leave-corner-out FAIL)──")
    print("     • P2: (φ−φc)²·(r_SE−0.5)+      Δ=+0.0072  β=+4.07 (Cronau high-arm)")
    print("     • E:  (φ−φc)²·r_SE             Δ=+0.0060  β=+2.41 (bolt-on)")
    print("     • L:  g_hi·g_010·log(1+(φ−.3)·r_SE)  Δ=+0.0065  β=+1.43")
    print("   ↳ bulk-only β has OPPOSITE sign of full-fit → corner-driven; ")
    print("     deferred pending more 62:38 × large-grain data OR a SE-stratified test")
    print()

    # ===== PER-CASE ERROR LANDSCAPE ============================================
    print("=" * 78)
    print(f" Per-case |err%| landscape on PRODUCTION (C4 augmented, n={n})")
    print("=" * 78)
    err = err_c4
    ae = np.abs(err)
    print(f"   median |err|     : {np.median(ae):6.2f}%")
    print(f"   mean   |err|     : {np.mean(ae):6.2f}%")
    print(f"   90th pctile |err|: {np.quantile(ae, 0.90):6.2f}%")
    print(f"   max    |err|     : {np.max(ae):6.2f}%")
    print(f"   #cases |err|>30% : {int((ae>30).sum()):3d} / {n}")
    print(f"   #cases |err|>50% : {int((ae>50).sum()):3d} / {n}")
    print()

    # ===== OUTLIER LIST (top |err|) with case names + classification ==========
    print("─" * 78)
    print(f" Top outliers (|err|>20%, sorted by |err%|):")
    print(f"   {'name':32s} {'σ_act':>7s} {'σ_pred':>7s} {'err%':>7s}  "
          f"{'φ':>5s} {'CN':>5s} {'r_SE':>5s} {'p':>5s}   {'class':s}")
    print("─" * 78)
    # find names by re-walking the corpus (same order as load_corpus)
    names = []
    seen = set()
    for base in ('webapp/results', 'webapp/archive'):
        bp = _P(base)
        if not bp.is_dir(): continue
        for mp in bp.rglob('full_metrics.json'):
            try: d = __import__('json').load(open(mp))
            except Exception: continue
            sig = gcp._stage_e_sigma(d)
            phi = gcp._get(d, 'phi_se'); cn = gcp._get(d, 'se_se_cn')
            cov = gcp._cov_frac(d, physics=True) or gcp._cov_frac(d, physics=False)
            fp = gcp._get(d, 'percolation_pct') / 100.0
            tau = gcp._get(d, 'tortuosity_recommended', gcp._get(d, 'tortuosity_mean', 0))
            if not (sig and sig > 0 and phi > PHI_C0 and cn > 0 and cov and cov > 0
                    and fp > 0 and tau > 0):
                continue
            nm = _meta_name(mp.parent.name, mp.parent)
            if nm in _EXCLUDED_NAMES:
                continue
            key = (round(phi, 4), round(cn, 3), round(float(sig), 5))
            if key in seen: continue
            seen.add(key)
            names.append(nm)
    if len(names) != n:
        print(f"   [warn] name list n={len(names)} doesn't match arrays n={n}; "
              "showing best-effort.")
    p_arr, phi_arr, rse_arr = a[:, 6], a[:, 0], a[:, 8]

    def _classify(i):
        p, phi, rse = p_arr[i], phi_arr[i], rse_arr[i]
        flags = []
        if p < 0.05:        flags.append("0:10")
        elif p > 0.95:      flags.append("10:0")
        else:               flags.append(f"P:S~{int(round(p*10))}:{10-int(round(p*10))}")
        if phi > 0.30:      flags.append("SE-rich")
        if np.isfinite(rse) and rse >= 1.0:   flags.append("D1+")
        if np.isfinite(rse) and rse < 0.1:    flags.append("sub-100nm")
        if (p < 0.05) and (phi > 0.30) and np.isfinite(rse) and rse >= 1.0:
            flags = ["62:38 D1+ corner"]   # canonical D1/D1.5 family
        return ",".join(flags)

    idx_sorted = np.argsort(-np.abs(err))
    shown = 0
    for i in idx_sorted:
        if abs(err[i]) <= 20.0 or shown >= 25: break
        nm = names[i] if i < len(names) else f"(idx{i})"
        sa = float(np.exp(logsf[i])); sp = float(np.exp(pred_c4[i]))
        cls = _classify(i)
        rse_str = f"{rse_arr[i]:5.2f}" if np.isfinite(rse_arr[i]) else "  —  "
        print(f"   {nm[:32]:32s} {sa:7.3f} {sp:7.3f} {err[i]:+7.1f}  "
              f"{phi_arr[i]:5.3f} {a[i,1]:5.1f} {rse_str} {p_arr[i]:5.2f}   {cls}")
        shown += 1
    if shown == 0:
        print(f"   (no cases with |err|>20% — production catches everything within 20%)")
    print()

    # ===== ROADMAP =============================================================
    print("=" * 78)
    print(" WHAT'S LEFT — three honest options")
    print("=" * 78)
    print("  1. Adopt P2 as a CORNER calibration (Δ=+0.0072 LOOCV; corner")
    print("     RMSE 0.340→0.058) with explicit caveat: β=+4.07 calibrated on")
    print("     4 D1/D1.5 cases; bulk-β of opposite sign indicates this is a")
    print("     gated corner correction, not extrapolated bulk physics.")
    print("  2. Hold current form; document corner as known systematic (the")
    print("     leave-corner-out test says we can't safely extrapolate from")
    print("     n=4 cases without seed replication).")
    print("  3. Collect 62:38 × r_SE≥1µm multi-seed data (e.g. particulate_7_S1..S5,")
    print("     particulate_10_S1..S5).  Then re-run the stress tests:")
    print("       • if all seeds cluster near σ≈0.6-0.7 → real physics, ADOPT P2 ")
    print("       • if seeds scatter widely → 4 cases were per-seed noise; close out")
    print()


if __name__ == "__main__":
    main()
