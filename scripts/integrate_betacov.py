#!/usr/bin/env python3
"""Test 3 physical integrations of the β_cov·Δcov term to bump it from
LOW-MED to HIGH confidence.

Current form uses Δcov = (cov_physics − cov_Hertz)/cov_Hertz · 100 — a
DERIVED percentage proxy.  β_cov = -0.016 is data-fit, physically
interpreted as "Tabor-amplification penalty" but lacks a clean literature
anchor.

3 integration candidates tested:

  T1.  REPLACE physics cov with Hertz cov
       σ ∝ cov_Hertz^½ instead of cov_physics^½·exp(β_cov·Δcov)
       → If LOOCV comparable, drop Δcov term entirely.  Physical:
         "Li+ conduction goes primarily through direct elastic contact;
          Tabor adhesion creates contact area but with reduced Li+ pathway."

  T2.  REPLACE Δcov with pct_tabor (binding-regime share)
       σ ∝ cov_physics^½ · exp(β_T · pct_tabor)
       → Direct physical proxy.  pct_tabor is the fraction of contacts in
         Tabor adhesion regime per Maugis-Dugdale classification (literature-
         grounded), not a derived percentage.
       β_T expected < 0 (more Tabor → less Li+ conduction).

  T3.  GEOMETRIC BLEND with FROZEN α from data
       σ ∝ (cov_h^α · cov_p^(1−α))^½, α frozen at corpus-fit value
       → If α is in [0,1], it's a physical convex combination.
         If α > 1, the blend interpretation fails (we already showed this:
         β_cov=-0.016 → α=3.2, NOT in [0,1] → T3 expected to FAIL).
         Included as a control to confirm.

For each: LOOCV, β value (if applicable), AIC, and per-outlier shifts on
the 8 |err|>20% outliers from current C5.

Run from the repo root:  python3 scripts/integrate_betacov.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
import generate_comparison_plots as gcp  # noqa
from nested_cv_sat import (load_corpus, base_log_sat, base_no_phi, cblend_fit,
                           cblend_pred, cronau_factor, p2_feature,
                           cov_delta_feature, _g_phys_smooth,
                           _meta_name, _EXCLUDED_NAMES,
                           PHICP_F, PHICS_F, DELTA_F, SG)


def _load_aligned_metrics(a):
    names, metrics, seen = [], [], set()
    for base in ('webapp/results', 'webapp/archive'):
        bp = Path(base)
        if not bp.is_dir(): continue
        for mp in bp.rglob('full_metrics.json'):
            try: d = json.load(open(mp))
            except Exception: continue
            sig = gcp._stage_e_sigma(d)
            phi = gcp._get(d, 'phi_se'); cn = gcp._get(d, 'se_se_cn')
            cov = gcp._cov_frac(d, physics=True) or gcp._cov_frac(d, physics=False)
            fp = gcp._get(d, 'percolation_pct') / 100.0
            tau = gcp._get(d, 'tortuosity_recommended', gcp._get(d, 'tortuosity_mean', 0))
            if not (sig and sig > 0 and phi > 0 and cn > 0 and cov and cov > 0
                    and fp > 0 and tau > 0):
                continue
            nm = _meta_name(mp.parent.name, mp.parent)
            if nm in _EXCLUDED_NAMES: continue
            key = (round(phi, 4), round(cn, 3), round(float(sig), 5))
            if key in seen: continue
            seen.add(key)
            names.append(nm); metrics.append(d)
    return names, metrics


def _find_tabor_field(metrics):
    """Discover which field holds the Tabor binding-regime share %."""
    candidates = [
        'pct_tabor_all', 'regime_share_tabor_all',
        'binding_share_tabor_all', 'tabor_fraction_all',
        'regime_share_all_tabor', 'pct_tabor', 'tabor_pct',
        'tabor_share_pct_all', 'binding_tabor_all_pct',
    ]
    found = {}
    for k in candidates:
        n_ok = sum(1 for d in metrics if isinstance(d.get(k), (int, float)))
        if n_ok >= 0.5 * len(metrics):
            found[k] = n_ok
    if found:
        return found
    # Discovery: scan all numeric fields for "tabor"
    discovered = {}
    for d in metrics:
        for k in d:
            if 'tabor' in k.lower() and isinstance(d.get(k), (int, float)):
                discovered[k] = discovered.get(k, 0) + 1
    return {k: v for k, v in discovered.items() if v >= 0.5 * len(metrics)}


def _find_hertz_cov_field(metrics):
    """Discover which field has the Hertz coverage (not physics)."""
    # _cov_frac(physics=False) reads coverage_AM_*_mean (not _physics suffixed)
    # Let's just compute cov_Hertz from cov_physics and Δcov:
    # Δcov = (cov_p − cov_h)/cov_h · 100  →  cov_h = cov_p / (1 + Δcov/100)
    return None  # we'll use the algebraic identity


def _loocv_with_extras(base, logsf, taus, extras):
    n = len(taus); ss = float(np.sum((logsf-logsf.mean())**2)); sse = 0.0
    lt = np.log(taus)
    if extras:
        X = np.column_stack([np.ones(n), lt, lt**2] + list(extras))
    else:
        X = np.column_stack([np.ones(n), lt, lt**2])
    for i in range(n):
        m = np.ones(n, bool); m[i] = False
        coef, *_ = np.linalg.lstsq(X[m], logsf[m] - base[m], rcond=None)
        pi = base[i] + X[i] @ coef
        sse += (logsf[i] - pi)**2
    coef_full, *_ = np.linalg.lstsq(X, logsf - base, rcond=None)
    pred_full = base + X @ coef_full
    sse_in = float(np.sum((logsf - pred_full)**2))
    aic = n*np.log(sse_in/n) + 2*X.shape[1]
    return 1 - sse/ss, coef_full, pred_full, aic


def main():
    a = load_corpus()
    n = len(a)
    if n < 20:
        print(f"[ABORT] only {n} cases."); return
    names, metrics = _load_aligned_metrics(a)
    logsf = np.log(a[:, 5]); taus = a[:, 4]
    cf = cronau_factor(a[:, 8])

    # Production base (SAT × Cronau with smooth g_phys)
    base = base_log_sat(a, PHICP_F, PHICS_F, DELTA_F) + np.log(cf)

    # Build features
    g_phys = _g_phys_smooth(a)
    p2 = p2_feature(a[:, 0], a[:, 8], g_gate=g_phys)
    dcov_centered, _ = cov_delta_feature(a[:, 12])
    f_log = a[:, 19] if a.shape[1] >= 20 else np.zeros(n)

    # Reference: current C5 form (P2 + Δcov + f_intact)
    lo_ref, coef_ref, pred_ref, aic_ref = _loocv_with_extras(
        base, logsf, taus, [p2, dcov_centered, f_log])
    err_ref = (np.exp(pred_ref) - np.exp(logsf)) / np.exp(logsf) * 100.0
    out_idx = np.where(np.abs(err_ref) > 20)[0]
    out_idx = out_idx[np.argsort(-np.abs(err_ref[out_idx]))][:8]

    print("=" * 95)
    print(f"  β_cov INTEGRATION TEST   n={n}")
    print("=" * 95)
    print(f"\n  REFERENCE (C5 production): cov_p^½·exp(β_cov·Δcov)+f_intact")
    print(f"    LOOCV = {lo_ref:.4f}   β_cov = {coef_ref[4]:+.4f}   k = 6")
    print(f"    AIC = {aic_ref:+.2f}   |err|>20% = {len(out_idx)}")

    # Discover Tabor field
    tabor_fields = _find_tabor_field(metrics)
    if tabor_fields:
        print(f"\n  Discovered Tabor-share fields: {list(tabor_fields.keys())}")
        tabor_key = max(tabor_fields, key=lambda k: tabor_fields[k])
        print(f"    Using: {tabor_key}  ({tabor_fields[tabor_key]}/{n} cases)")
    else:
        print(f"\n  ⚠ No Tabor-share field found in corpus — skipping T2")
        tabor_key = None

    # =========================================================================
    # T1: Use cov_Hertz instead of cov_physics (no Δcov term)
    # =========================================================================
    print("\n" + "█" * 95)
    print("T1: REPLACE cov_physics with cov_Hertz  (drop Δcov term)")
    print("█" * 95)
    # Build cov_Hertz from cov_physics and Δcov:
    #   Δcov = (cov_p − cov_h)/cov_h · 100  ⇒  cov_h = cov_p / (1 + Δcov/100)
    # But Δcov is in col 12 ALREADY centered? No — col 12 is the raw percentage
    # (cov_delta_pct_rough), not centered yet.
    # We use the raw values from metrics directly:
    cov_p_raw = np.array([float(gcp._cov_frac(d, physics=True) or
                                 gcp._cov_frac(d, physics=False) or 0.20)
                          for d in metrics])
    dcov_raw = np.array([(d.get('coverage_AM_delta_pct_rough')
                          or d.get('coverage_AM_S_delta_pct_rough') or 0.0)
                         for d in metrics], float)
    # cov_h = cov_p / (1 + Δcov/100)   ; clamp to avoid div issues
    factor = np.maximum(1.0 + dcov_raw/100.0, 0.1)
    cov_hertz = cov_p_raw / factor
    cov_hertz_safe = np.maximum(cov_hertz, 1e-4)

    # Replace cov^½ in base — subtract old (physics), add new (Hertz)
    # base currently includes 0.5·log(cov_physics).  Adjust:
    # Δlog = 0.5·log(cov_Hertz) − 0.5·log(cov_physics) = 0.5·log(cov_h/cov_p)
    base_T1 = base + 0.5*np.log(cov_hertz_safe / np.maximum(cov_p_raw, 1e-4))
    # T1 extras: P2 + f_intact only (no Δcov)
    lo_T1, coef_T1, pred_T1, aic_T1 = _loocv_with_extras(
        base_T1, logsf, taus, [p2, f_log])
    err_T1 = (np.exp(pred_T1) - np.exp(logsf)) / np.exp(logsf) * 100.0
    print(f"  LOOCV = {lo_T1:.4f}   Δ vs ref = {lo_T1 - lo_ref:+.4f}   k = 5")
    print(f"  AIC = {aic_T1:+.2f}   ΔAIC = {aic_T1 - aic_ref:+.2f}")
    print(f"  |err|>20% = {int((np.abs(err_T1)>20).sum())}   |err|>30% = {int((np.abs(err_T1)>30).sum())}")

    # =========================================================================
    # T2: Replace Δcov with pct_tabor
    # =========================================================================
    print("\n" + "█" * 95)
    print("T2: REPLACE Δcov with pct_tabor (Maugis-Dugdale binding-regime share)")
    print("█" * 95)
    if tabor_key:
        tabor_pct = np.array([(d.get(tabor_key) or 0.0) for d in metrics], float)
        # Center by median
        med = float(np.median(tabor_pct[np.isfinite(tabor_pct)]))
        tabor_c = np.where(np.isfinite(tabor_pct), tabor_pct - med, 0.0)
        print(f"  Tabor share range: {tabor_pct.min():.1f} – {tabor_pct.max():.1f} % "
              f"(median {med:.1f}%)")
        lo_T2, coef_T2, pred_T2, aic_T2 = _loocv_with_extras(
            base, logsf, taus, [p2, tabor_c, f_log])
        err_T2 = (np.exp(pred_T2) - np.exp(logsf)) / np.exp(logsf) * 100.0
        print(f"  LOOCV = {lo_T2:.4f}   Δ vs ref = {lo_T2 - lo_ref:+.4f}   k = 6")
        print(f"  β_T (pct_tabor coef) = {coef_T2[4]:+.4f}")
        print(f"  AIC = {aic_T2:+.2f}   ΔAIC = {aic_T2 - aic_ref:+.2f}")
        print(f"  |err|>20% = {int((np.abs(err_T2)>20).sum())}   |err|>30% = {int((np.abs(err_T2)>30).sum())}")
    else:
        print(f"  [skip — Tabor field not found in corpus]")

    # =========================================================================
    # T3: Geometric blend with FROZEN α (control — expected to fail)
    # =========================================================================
    print("\n" + "█" * 95)
    print("T3: GEOMETRIC BLEND  cov_eff = cov_h^α · cov_p^(1−α)  (control)")
    print("█" * 95)
    print(f"  Scanning α ∈ [0, 1] to find the data-optimal blend...")
    best_alpha, best_lo = None, -np.inf
    for alpha in np.linspace(0.0, 1.0, 21):
        cov_eff = cov_hertz_safe**alpha * cov_p_raw**(1.0 - alpha)
        # Adjust base: replace 0.5·log(cov_p) with 0.5·log(cov_eff)
        base_alpha = base + 0.5*np.log(np.maximum(cov_eff, 1e-4) / np.maximum(cov_p_raw, 1e-4))
        lo_a, _, _, _ = _loocv_with_extras(base_alpha, logsf, taus, [p2, f_log])
        if lo_a > best_lo:
            best_lo, best_alpha = lo_a, alpha
    print(f"  Best α = {best_alpha:.3f}   LOOCV = {best_lo:.4f}   "
          f"Δ vs ref = {best_lo - lo_ref:+.4f}")
    if best_alpha == 0.0:
        print(f"  → Data prefers PURE PHYSICS cov (α=0). Hertz weight unwanted in blend.")
    elif best_alpha == 1.0:
        print(f"  → Data prefers PURE HERTZ cov (α=1). Drop physics in favor of Hertz.")
    else:
        print(f"  → Blend with α={best_alpha:.3f} (Hertz weight {best_alpha*100:.0f}%)")

    # =========================================================================
    # SUMMARY
    # =========================================================================
    print("\n" + "=" * 95)
    print("SUMMARY — physical confidence rating after testing:")
    print("=" * 95)
    print(f"\n  REF C5 (Δcov + cov_p^½):  LOOCV={lo_ref:.4f}  k=6  β_cov={coef_ref[4]:+.4f}")
    print(f"     Confidence: LOW-MED (empirical proxy for Tabor effect)")
    print(f"\n  T1 (cov_Hertz only):     LOOCV={lo_T1:.4f}  k=5  ΔLOOCV={lo_T1-lo_ref:+.4f}")
    if lo_T1 >= lo_ref - 0.0016:
        print(f"     → ★ adopt: removes 1 param, cleaner physics, comparable LOOCV")
        print(f"     New confidence: MED-HIGH (Holm constriction with Hertz cov)")
    else:
        print(f"     → keep cov_physics + Δcov correction; Hertz alone misses Tabor info")
    if tabor_key:
        print(f"\n  T2 (pct_tabor proxy):    LOOCV={lo_T2:.4f}  k=6  β_T={coef_T2[4]:+.4f}")
        if lo_T2 >= lo_ref - 0.0016:
            print(f"     → ★ adopt: same k, but β has clean physical meaning")
            print(f"     New confidence: MED-HIGH (Maugis-Dugdale regime classification)")
        else:
            print(f"     → pct_tabor doesn't capture as much as Δcov; keep Δcov")
    print(f"\n  T3 (geometric blend):    best α={best_alpha:.3f}  LOOCV={best_lo:.4f}")
    if best_alpha in (0.0, 1.0):
        print(f"     → expected fail (boundary solution); pure blend doesn't fit data")


if __name__ == "__main__":
    main()
