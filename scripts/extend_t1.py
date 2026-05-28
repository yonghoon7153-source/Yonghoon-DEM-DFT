#!/usr/bin/env python3
"""Extend T1 (cov_Hertz adoption) — test more direct bottleneck statistics
and re-optimized exponents now that cov_Hertz is in the base.

T1 reference (current production): cov_Hertz^½ in base, 5 live params,
LOOCV ≈ 0.9731.  Key insight: σ_solver is bottleneck-dominated, and the
form's `cov^½` is a SIMPLIFIED proxy for the bottleneck-driven Holm
constriction.  cov_Hertz mean correlates better than cov_physics mean
because Tabor/Volume corrections inflate the LARGER contacts (not the
bottleneck-defining smallest ones).

Tests:
  E1.  path_hop_area_min_mean as direct bottleneck feature
       (literally: min contact area along the percolation path)
  E2.  cov_Hertz exponent scan — maybe Hertz cov benefits from
       different power than 0.5 (the Holm classical value applies to
       per-contact, not corpus-mean)
  E3.  cov heterogeneity (std/mean) as auxiliary feature
       (more uniform = closer to mean-Hertz = better predictor)
  E4.  Geometric mean cov_blend = cov_H^α · cov_P^(1−α) with frozen α
       (α=1 = pure Hertz = T1 ref; scan to confirm)
  E5.  Absolute contact area: replace cov with cov · r_SE²
       (dimensional: real A_contact ∝ cov · particle_radius²)
  E6.  CN exponent re-scan (was 2.0 with cov_physics; might shift now)

For each: LOOCV, AIC, |err|>20% count, β value (if added as feature).
Adoption rule: ★ if Δ_LOOCV > +0.0016 (noise SE) AND |err|>30% same/better.

Run from the repo root:  python3 scripts/extend_t1.py
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
                           _g_phys_smooth, _meta_name, _EXCLUDED_NAMES,
                           PHICP_F, PHICS_F, DELTA_F, K_PS, P_C, PHI_C0, SG,
                           CN_EXP, COV_EXP)


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
            cov = gcp._cov_frac(d, physics=False) or gcp._cov_frac(d, physics=True)
            fp = gcp._get(d, 'percolation_pct') / 100.0
            tau = gcp._get(d, 'tortuosity_recommended', gcp._get(d, 'tortuosity_mean', 0))
            if not (sig and sig > 0 and phi > PHI_C0 and cn > 0 and cov and cov > 0
                    and fp > 0 and tau > 0):
                continue
            nm = _meta_name(mp.parent.name, mp.parent)
            if nm in _EXCLUDED_NAMES: continue
            key = (round(phi, 4), round(cn, 3), round(float(sig), 5))
            if key in seen: continue
            seen.add(key)
            names.append(nm); metrics.append(d)
    return names, metrics


def _loocv_with_extras(base, logsf, taus, extras=None):
    n = len(taus); ss = float(np.sum((logsf-logsf.mean())**2)); sse = 0.0
    lt = np.log(taus)
    if extras:
        X = np.column_stack([np.ones(n), lt, lt**2] + list(extras))
    else:
        X = np.column_stack([np.ones(n), lt, lt**2])
    coef_full, *_ = np.linalg.lstsq(X, logsf - base, rcond=None)
    pred_full = base + X @ coef_full
    sse_in = float(np.sum((logsf - pred_full)**2))
    for i in range(n):
        m = np.ones(n, bool); m[i] = False
        coef, *_ = np.linalg.lstsq(X[m], logsf[m] - base[m], rcond=None)
        pi = base[i] + X[i] @ coef
        sse += (logsf[i] - pi)**2
    aic = n*np.log(sse_in/n) + 2*X.shape[1]
    return 1 - sse/ss, coef_full, pred_full, aic


def _err_bands(pred, logsf):
    err = (np.exp(pred) - np.exp(logsf)) / np.exp(logsf) * 100.0
    ae = np.abs(err)
    return int((ae > 20).sum()), int((ae > 30).sum()), float(np.median(ae))


def main():
    a = load_corpus()
    n = len(a)
    if n < 20:
        print(f"[ABORT] only {n} cases."); return
    names, metrics = _load_aligned_metrics(a)
    logsf = np.log(a[:, 5]); taus = a[:, 4]
    cf = cronau_factor(a[:, 8])

    # T1 REFERENCE: production base + P2 + f_intact (no Δcov)
    base_ref = base_log_sat(a, PHICP_F, PHICS_F, DELTA_F) + np.log(cf)
    g_phys = _g_phys_smooth(a)
    p2 = p2_feature(a[:, 0], a[:, 8], g_gate=g_phys)
    f_log = a[:, 19] if a.shape[1] >= 20 else np.zeros(n)
    lo_ref, coef_ref, pred_ref, aic_ref = _loocv_with_extras(
        base_ref, logsf, taus, [p2, f_log])
    n20, n30, med = _err_bands(pred_ref, logsf)
    se_loocv = 0.0016

    print("=" * 95)
    print(f"  T1 EXTENSION TESTS   n={n}   noise SE = {se_loocv:.4f}")
    print("=" * 95)
    print(f"\nREFERENCE (T1 production): cov_Hertz^0.5 + P2 + f_intact")
    print(f"    LOOCV = {lo_ref:.4f}   AIC = {aic_ref:+.2f}   k = 5")
    print(f"    |err|>20% = {n20}   |err|>30% = {n30}   median |err| = {med:.2f}%")

    # =========================================================================
    # E1. path_hop_area_min_mean as bottleneck feature
    # =========================================================================
    print("\n" + "█" * 95)
    print("E1. log(path_hop_area_min_mean) as direct bottleneck feature")
    print("█" * 95)
    pha_min = np.array([(d.get('path_hop_area_min_mean')
                         or d.get('path_hop_area_mean_physics')
                         or d.get('path_hop_area_mean') or np.nan)
                        for d in metrics], float)
    n_have = int(np.isfinite(pha_min).sum())
    if n_have < 0.5*n:
        print(f"  [skip — only {n_have}/{n} cases have path_hop_area_min]")
    else:
        med_pha = float(np.nanmedian(pha_min[np.isfinite(pha_min) & (pha_min > 0)]))
        pha_safe = np.where(np.isfinite(pha_min) & (pha_min > 0), pha_min, med_pha)
        pha_feat = np.log(pha_safe / med_pha)
        lo, coef, pred, aic = _loocv_with_extras(base_ref, logsf, taus,
                                                  [p2, f_log, pha_feat])
        n20_x, n30_x, med_x = _err_bands(pred, logsf)
        d = lo - lo_ref
        flag = "★" if d > se_loocv else (" " if abs(d) < se_loocv else "⚠")
        print(f"  LOOCV={lo:.4f}  Δ={d:+.4f}  β_pha={coef[-1]:+.3f}  k=6  {flag}")
        print(f"  |err|>20%={n20_x} (Δ{n20_x-n20:+d})  |err|>30%={n30_x} (Δ{n30_x-n30:+d})  med={med_x:.2f}%")

    # =========================================================================
    # E2. cov_Hertz exponent scan
    # =========================================================================
    print("\n" + "█" * 95)
    print("E2. cov_Hertz exponent scan (replace 0.5 with other powers)")
    print("█" * 95)
    cov = a[:, 2]  # current cov column (Hertz after T1 adoption)
    cn = a[:, 1]
    fp = a[:, 3]
    # build base WITHOUT cov term, then add cov^α
    g = _g_phys_smooth(a)
    phic = (1-g)*PHICP_F + g*PHICS_F
    pex = a[:, 0] - phic
    phi_eff = np.sqrt(pex**2 + (DELTA_F*g)**2 + 1e-12)
    bare_log = (np.log(SG) + 0.5*np.log(phi_eff) + CN_EXP*np.log(cn)
                + 3.0*np.log(fp) + np.log(cf))
    print(f"  {'cov exp':>10s} {'LOOCV':>7s} {'Δ vs ref':>9s}")
    for alpha in [0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 1.00]:
        base_a = bare_log + alpha*np.log(cov)
        lo, _, pred, _ = _loocv_with_extras(base_a, logsf, taus, [p2, f_log])
        d = lo - lo_ref
        mark = " ←current 0.5" if alpha == 0.50 else ""
        flag = "★" if d > se_loocv else ("  " if abs(d) < se_loocv else "⚠")
        print(f"  {alpha:>10.2f} {lo:7.4f} {d:+9.4f} {flag}{mark}")

    # =========================================================================
    # E3. cov heterogeneity as auxiliary feature
    # =========================================================================
    print("\n" + "█" * 95)
    print("E3. cov std/mean ratio (heterogeneity) as auxiliary feature")
    print("█" * 95)
    cov_std = np.array([(d.get('coverage_AM_S_std')
                         or d.get('coverage_AM_P_std') or np.nan)
                        for d in metrics], float)
    cov_mean = np.array([(d.get('coverage_AM_S_mean')
                          or d.get('coverage_AM_P_mean')
                          or d.get('coverage_AM_mean') or np.nan)
                         for d in metrics], float)
    n_have = int(np.isfinite(cov_std).sum())
    if n_have < 0.5*n:
        print(f"  [skip — only {n_have}/{n} cases have cov_std]")
    else:
        cv = np.where(np.isfinite(cov_std) & np.isfinite(cov_mean) & (cov_mean > 0),
                       cov_std / np.maximum(cov_mean, 1e-6), 0.0)
        med_cv = float(np.median(cv[np.isfinite(cv)]))
        cv_centered = np.where(np.isfinite(cv), cv - med_cv, 0.0)
        lo, coef, pred, aic = _loocv_with_extras(base_ref, logsf, taus,
                                                  [p2, f_log, cv_centered])
        d = lo - lo_ref
        n20_x, n30_x, _ = _err_bands(pred, logsf)
        flag = "★" if d > se_loocv else (" " if abs(d) < se_loocv else "⚠")
        print(f"  LOOCV={lo:.4f}  Δ={d:+.4f}  β_cv={coef[-1]:+.3f}  k=6  {flag}")
        print(f"  |err|>20%={n20_x} (Δ{n20_x-n20:+d})  |err|>30%={n30_x} (Δ{n30_x-n30:+d})")

    # =========================================================================
    # E4. Geometric blend cov_H^α · cov_P^(1−α) scan
    # =========================================================================
    print("\n" + "█" * 95)
    print("E4. Geometric blend cov_H^α · cov_P^(1−α) — fine scan around α=1")
    print("█" * 95)
    cov_h_raw = np.array([(gcp._cov_frac(d, physics=False)
                            or gcp._cov_frac(d, physics=True) or 0.20)
                           for d in metrics])
    cov_p_raw = np.array([(gcp._cov_frac(d, physics=True)
                            or gcp._cov_frac(d, physics=False) or 0.20)
                           for d in metrics])
    print(f"  {'α (Hertz weight)':>18s} {'LOOCV':>7s} {'Δ vs ref':>9s}")
    for alpha in [0.70, 0.80, 0.90, 0.95, 1.00, 1.05, 1.10]:
        # α=1 → pure Hertz (= T1 ref).  α>1 → over-weight Hertz beyond pure.
        cov_eff = np.maximum(cov_h_raw**alpha * cov_p_raw**(1.0-alpha), 1e-4)
        base_a = bare_log + 0.5*np.log(cov_eff) - 0.5*np.log(np.maximum(cov, 1e-4))
        # ↑ replaces 0.5·log(cov_Hertz) with 0.5·log(cov_eff)
        lo, _, pred, _ = _loocv_with_extras(base_a, logsf, taus, [p2, f_log])
        d = lo - lo_ref
        mark = " ←T1" if alpha == 1.00 else ""
        flag = "★" if d > se_loocv else ("  " if abs(d) < se_loocv else "⚠")
        print(f"  {alpha:>18.2f} {lo:7.4f} {d:+9.4f} {flag}{mark}")

    # =========================================================================
    # E5. Absolute contact area cov · r_SE²
    # =========================================================================
    print("\n" + "█" * 95)
    print("E5. Absolute contact area: cov · r_SE² (Holm dimensional)")
    print("█" * 95)
    rse = a[:, 8]
    rse_safe = np.where(np.isfinite(rse) & (rse > 0), rse, 0.5)
    cov_abs = cov * rse_safe**2
    base_E5 = bare_log + 0.5*np.log(np.maximum(cov_abs, 1e-6))
    lo, _, pred, _ = _loocv_with_extras(base_E5, logsf, taus, [p2, f_log])
    n20_x, n30_x, med_x = _err_bands(pred, logsf)
    d = lo - lo_ref
    flag = "★" if d > se_loocv else (" " if abs(d) < se_loocv else "⚠")
    print(f"  LOOCV={lo:.4f}  Δ={d:+.4f}  k=5  {flag}")
    print(f"  |err|>20%={n20_x} (Δ{n20_x-n20:+d})  |err|>30%={n30_x} (Δ{n30_x-n30:+d})")

    # =========================================================================
    # E6. CN exponent re-scan (post-T1)
    # =========================================================================
    print("\n" + "█" * 95)
    print("E6. CN exponent re-scan (cov changed to Hertz; CN^β may shift)")
    print("█" * 95)
    bare_log_no_cn = (np.log(SG) + 0.5*np.log(phi_eff) + 0.5*np.log(cov)
                      + 3.0*np.log(fp) + np.log(cf))
    print(f"  {'CN exp':>8s} {'LOOCV':>7s} {'Δ vs ref':>9s}")
    for beta in [1.50, 1.75, 2.00, 2.25, 2.50]:
        base_b = bare_log_no_cn + beta*np.log(cn)
        lo, _, pred, _ = _loocv_with_extras(base_b, logsf, taus, [p2, f_log])
        d = lo - lo_ref
        mark = " ←current 2.0" if beta == 2.00 else ""
        flag = "★" if d > se_loocv else ("  " if abs(d) < se_loocv else "⚠")
        print(f"  {beta:>8.2f} {lo:7.4f} {d:+9.4f} {flag}{mark}")

    print("\n" + "=" * 95)
    print("INTERPRETATION:")
    print("  • ★ candidate → LOOCV beats T1 by > noise SE")
    print("  • E1 ★ → adopt path_hop_area_min as direct bottleneck feature")
    print("  • E2 best exponent ≠ 0.5 → cov_Hertz wants different power")
    print("  • E4 best α ≠ 1.0 → some physics in cov_p NOT captured by Hertz alone")
    print("  • E5 ★ → dimensional contact area more physical than fraction")
    print("  • E6 best β ≠ 2.0 → CN exponent needs update with new cov")


if __name__ == "__main__":
    main()
