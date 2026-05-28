#!/usr/bin/env python3
"""Deep parameter scan + ablation of the smooth f_small (S1) gate.

The production smooth gate (adopted 2026-05-28) uses:
  f_small = (1−p)·σ(K_S·(r_cut − r_AM_S)) + p·σ(K_S·(r_cut − r_AM_P))
  g_phys  = σ(K_K·(f_small − 0.5))
with r_cut=3.5µm, K_S=5/µm, K_K=10.  These three constants are heuristic
(picked from the audit-confirmed corpus gap mid-point).  This script:

  PART 1 — PARAMETER SCAN
    Joint scan over (r_cut, K_S, K_K) with production C5 form
    (P2 + Δcov + f_intact extras).  Identify global LOOCV optimum and
    its sensitivity to each parameter.

  PART 2 — PER-CASE BORDERLINE ANALYSIS
    For each corpus case, compute g_phys at the production constants
    AND at neighbouring (r_cut ±0.5µm).  Identify cases where g_phys
    is most "swingable" — these are the cases that the smooth-form
    treatment affects.  input_S_2 (r_AM_S=4µm) is the obvious one;
    are there other borderline cases lurking?

  PART 3 — ALTERNATE FUNCTIONAL FORM TESTS
    • Linear ramp instead of sigmoid (hard cutoff with linear window)
    • r_SE-aware: include SE size as third factor in f_small
    • Continuous power: f_small = (r_AM/r_cut)^α  (no sigmoid)
    Compare LOOCV for each alternative form vs the production sigmoid.

Run from the repo root:  python3 scripts/scan_smooth_f_small.py
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
                           cov_delta_feature, _meta_name, _EXCLUDED_NAMES,
                           PHICP_F, PHICS_F, DELTA_F, K_PS, P_C, PHI_C0, SG)


def _load_names_and_metrics(a):
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
            if not (sig and sig > 0 and phi > PHI_C0 and cn > 0 and cov and cov > 0
                    and fp > 0 and tau > 0):
                continue
            nm = _meta_name(mp.parent.name, mp.parent)
            if nm in _EXCLUDED_NAMES: continue
            key = (round(phi, 4), round(cn, 3), round(float(sig), 5))
            if key in seen: continue
            seen.add(key)
            names.append(nm)
            metrics.append(d)
    return names, metrics


def _g_phys_smooth_custom(a, r_cut, K_S, K_K):
    """Smooth size-based g_phys with custom (r_cut, K_S, K_K)."""
    p = a[:, 6]
    ras = a[:, 17]; rap = a[:, 18]
    rs_med = float(np.nanmedian(ras[np.isfinite(ras)])) if np.isfinite(ras).any() else 2.5
    rp_med = float(np.nanmedian(rap[np.isfinite(rap)])) if np.isfinite(rap).any() else 5.5
    ras_s = np.where(np.isfinite(ras) & (ras > 0), ras, rs_med)
    rap_s = np.where(np.isfinite(rap) & (rap > 0), rap, rp_med)
    sig_S = 1.0/(1.0+np.exp(-K_S*(r_cut - ras_s)))
    sig_P = 1.0/(1.0+np.exp(-K_S*(r_cut - rap_s)))
    f_small = (1.0 - p)*sig_S + p*sig_P
    return 1.0/(1.0+np.exp(-K_K*(f_small - 0.5)))


def _base_log_sat_custom(a, r_cut, K_S, K_K, phicP=PHICP_F, phicS=PHICS_F,
                          delta=DELTA_F):
    """SAT-blend base with custom smooth g_phys."""
    phi = a[:, 0]
    g = _g_phys_smooth_custom(a, r_cut, K_S, K_K)
    phic = (1.0-g)*phicP + g*phicS
    pex = phi - phic
    return base_no_phi(a) + 0.5*np.log(np.sqrt(pex**2 + (delta*g)**2) + 1e-12)


def _loocv_with_extras(base, logsf, taus, extras):
    n = len(taus); ss = float(np.sum((logsf-logsf.mean())**2)); sse = 0.0
    lt = np.log(taus)
    X = np.column_stack([np.ones(n), lt, lt**2] + list(extras))
    for i in range(n):
        m = np.ones(n, bool); m[i] = False
        coef, *_ = np.linalg.lstsq(X[m], logsf[m] - base[m], rcond=None)
        pi = base[i] + X[i] @ coef
        sse += (logsf[i] - pi)**2
    return 1 - sse/ss


def _build_extras_for_grid(a, metrics, r_cut, K_S, K_K, cov_med=None):
    """Build C5 extras list with custom smooth gate parameters."""
    g = _g_phys_smooth_custom(a, r_cut, K_S, K_K)
    p2 = p2_feature(a[:, 0], a[:, 8], g_gate=g)
    cdc, med = cov_delta_feature(a[:, 12], center=cov_med)
    f_log = a[:, 19] if a.shape[1] >= 20 else np.zeros(a.shape[0])
    return [p2, cdc, f_log], med


def main():
    a = load_corpus()
    n = len(a)
    if n < 20:
        print(f"[ABORT] only {n} cases (need WSL corpus)."); return
    names, metrics = _load_names_and_metrics(a)
    logsf = np.log(a[:, 5]); taus = a[:, 4]
    cf = cronau_factor(a[:, 8])
    se_loocv = np.sqrt(np.var((logsf-logsf.mean())**2)/n) / np.sum((logsf-logsf.mean())**2)

    # =========================================================================
    print("=" * 95)
    print(f"SMOOTH f_small (S1) DEEP SCAN   n={n}   noise SE ≈ {se_loocv:.4f}")
    print("=" * 95)

    # Reference: production (r_cut=3.5, K_S=5, K_K=10)
    base_ref = _base_log_sat_custom(a, 3.5, 5.0, 10.0) + np.log(cf)
    extras_ref, _ = _build_extras_for_grid(a, metrics, 3.5, 5.0, 10.0)
    lo_ref = _loocv_with_extras(base_ref, logsf, taus, extras_ref)
    print(f"\nREFERENCE (production):  r_cut=3.5µm, K_S=5, K_K=10   LOOCV = {lo_ref:.4f}")

    # PART 1 — PARAMETER SCAN
    print("\n" + "█" * 95)
    print("PART 1 — JOINT (r_cut, K_S, K_K) parameter scan")
    print("█" * 95)
    rcut_grid = [2.5, 3.0, 3.25, 3.5, 3.75, 4.0, 4.5]
    KS_grid   = [2.0, 5.0, 10.0, 20.0]
    KK_grid   = [5.0, 10.0, 20.0]
    print(f"  Scanning {len(rcut_grid)} × {len(KS_grid)} × {len(KK_grid)} = "
          f"{len(rcut_grid)*len(KS_grid)*len(KK_grid)} combinations...")

    results = []
    for rc in rcut_grid:
        for ks in KS_grid:
            for kk in KK_grid:
                base_x = _base_log_sat_custom(a, rc, ks, kk) + np.log(cf)
                extras_x, _ = _build_extras_for_grid(a, metrics, rc, ks, kk)
                lo = _loocv_with_extras(base_x, logsf, taus, extras_x)
                results.append((rc, ks, kk, lo))
    results.sort(key=lambda x: -x[3])

    print(f"\n  TOP 8 combinations:")
    print(f"  {'rank':>4s} {'r_cut':>6s} {'K_S':>5s} {'K_K':>5s} {'LOOCV':>7s} {'Δ vs prod':>10s}")
    for i, (rc, ks, kk, lo) in enumerate(results[:8]):
        flag = "★" if lo > lo_ref + se_loocv else ("·" if abs(lo - lo_ref) <= se_loocv else " ")
        print(f"  {i+1:>4d} {rc:>6.2f} {ks:>5.1f} {kk:>5.1f} {lo:7.4f} {lo - lo_ref:+10.4f} {flag}")

    print(f"\n  Sensitivity to each parameter (at production K_S=5, K_K=10):")
    for rc in rcut_grid:
        base_x = _base_log_sat_custom(a, rc, 5.0, 10.0) + np.log(cf)
        extras_x, _ = _build_extras_for_grid(a, metrics, rc, 5.0, 10.0)
        lo = _loocv_with_extras(base_x, logsf, taus, extras_x)
        marker = " ←PROD" if rc == 3.5 else ""
        print(f"    r_cut = {rc:4.2f} µm   LOOCV = {lo:.4f}   Δ = {lo - lo_ref:+.4f}{marker}")

    print(f"\n  Sensitivity to K_S (sharpness of inner sigmoid; at r_cut=3.5, K_K=10):")
    for ks in KS_grid:
        base_x = _base_log_sat_custom(a, 3.5, ks, 10.0) + np.log(cf)
        extras_x, _ = _build_extras_for_grid(a, metrics, 3.5, ks, 10.0)
        lo = _loocv_with_extras(base_x, logsf, taus, extras_x)
        marker = " ←PROD" if ks == 5.0 else ""
        print(f"    K_S = {ks:5.1f}/µm   LOOCV = {lo:.4f}   Δ = {lo - lo_ref:+.4f}{marker}")

    print(f"\n  Sensitivity to K_K (sharpness of outer sigmoid; at r_cut=3.5, K_S=5):")
    for kk in KK_grid:
        base_x = _base_log_sat_custom(a, 3.5, 5.0, kk) + np.log(cf)
        extras_x, _ = _build_extras_for_grid(a, metrics, 3.5, 5.0, kk)
        lo = _loocv_with_extras(base_x, logsf, taus, extras_x)
        marker = " ←PROD" if kk == 10.0 else ""
        print(f"    K_K = {kk:5.1f}     LOOCV = {lo:.4f}   Δ = {lo - lo_ref:+.4f}{marker}")

    # PART 2 — PER-CASE BORDERLINE ANALYSIS
    print("\n" + "█" * 95)
    print("PART 2 — PER-CASE g_phys swingability (borderline cases)")
    print("█" * 95)
    g_prod = _g_phys_smooth_custom(a, 3.5, 5.0, 10.0)
    g_low  = _g_phys_smooth_custom(a, 3.0, 5.0, 10.0)   # r_cut shift down 0.5
    g_high = _g_phys_smooth_custom(a, 4.0, 5.0, 10.0)   # r_cut shift up 0.5
    # also g_010 for comparison
    p = a[:, 6]
    g_010 = 1.0/(1.0+np.exp(K_PS*(p - P_C)))
    # swing = (g_high - g_low) — how much does g_phys change with r_cut?
    swing = g_high - g_low
    swing_abs = np.abs(swing)
    # also: difference smooth vs label
    diff_smooth_label = g_prod - g_010

    print(f"\n  Cases where smooth g DIFFERS most from label g_010 (|smooth−label| > 0.05):")
    print(f"  {'rank':>4s} {'name':30s} {'r_AM_S':>6s} {'r_AM_P':>6s} {'p':>5s} "
          f"{'g_010':>6s} {'g_prod':>7s} {'diff':>6s} {'swing':>6s}")
    idx_diff = np.argsort(-np.abs(diff_smooth_label))
    shown = 0
    for i in idx_diff:
        if abs(diff_smooth_label[i]) < 0.05:
            break
        ras = a[i, 17] if np.isfinite(a[i, 17]) else 0
        rap = a[i, 18] if np.isfinite(a[i, 18]) else 0
        print(f"  {shown+1:>4d} {names[i][:30]:30s} {ras:>6.2f} {rap:>6.2f} {p[i]:>5.2f} "
              f"{g_010[i]:>6.3f} {g_prod[i]:>7.3f} {diff_smooth_label[i]:+6.3f} {swing_abs[i]:>6.3f}")
        shown += 1
    if shown == 0:
        print("    (none — corpus convention strictly followed; smooth ≡ g_010 numerically)")
    print(f"\n  Total swingable cases (|swing| > 0.05 w.r.t. r_cut±0.5µm): "
          f"{int((swing_abs > 0.05).sum())}/{n}")

    # PART 3 — ALTERNATE FUNCTIONAL FORMS
    print("\n" + "█" * 95)
    print("PART 3 — ALTERNATE functional forms for f_small")
    print("█" * 95)
    print(f"\n  Reference: σ(K_S·(r_cut−r_AM)) sigmoid  ←PRODUCTION  LOOCV = {lo_ref:.4f}")

    # Alt 1: Linear ramp (hard cutoff with linear window)
    def _g_phys_linear(a, r_cut, window=0.5):
        p = a[:, 6]
        ras = a[:, 17]; rap = a[:, 18]
        ras_s = np.where(np.isfinite(ras) & (ras > 0), ras, 2.5)
        rap_s = np.where(np.isfinite(rap) & (rap > 0), rap, 5.5)
        # linear ramp from 1 (r ≤ rcut-w/2) to 0 (r ≥ rcut+w/2)
        def _ramp(r):
            return np.clip((r_cut + window/2 - r) / window, 0.0, 1.0)
        f_small = (1.0 - p)*_ramp(ras_s) + p*_ramp(rap_s)
        return 1.0/(1.0+np.exp(-10.0*(f_small - 0.5)))

    print(f"\n  Alternate forms (production extras unchanged; only gate replaced):")
    print(f"  {'form':50s} {'LOOCV':>7s} {'Δ vs prod':>10s}")
    for window in [0.5, 1.0, 1.5]:
        g = _g_phys_linear(a, 3.5, window)
        phic = (1-g)*PHICP_F + g*PHICS_F
        pex = a[:, 0] - phic
        bl = (base_no_phi(a) + 0.5*np.log(np.sqrt(pex**2 + (DELTA_F*g)**2) + 1e-12)
              + np.log(cf))
        p2 = p2_feature(a[:, 0], a[:, 8], g_gate=g)
        cdc, _ = cov_delta_feature(a[:, 12])
        f_log = a[:, 19] if a.shape[1] >= 20 else np.zeros(a.shape[0])
        lo = _loocv_with_extras(bl, logsf, taus, [p2, cdc, f_log])
        tag = f"Alt-A linear ramp (r_cut=3.5, window={window:.1f}µm)"
        flag = "★" if lo > lo_ref + se_loocv else (" " if abs(lo - lo_ref) <= se_loocv else "⚠")
        print(f"  {tag:50s} {lo:7.4f} {lo - lo_ref:+10.4f}   {flag}")

    # Alt 2: r_SE-aware (include r_SE in f_small)
    def _g_phys_with_rSE(a, r_cut_am, K_S=5.0, K_K=10.0):
        """Include r_SE in the gate — borderline cases might depend on r_SE too."""
        p = a[:, 6]
        ras = a[:, 17]; rap = a[:, 18]; rse = a[:, 8]
        ras_s = np.where(np.isfinite(ras) & (ras > 0), ras, 2.5)
        rap_s = np.where(np.isfinite(rap) & (rap > 0), rap, 5.5)
        rse_s = np.where(np.isfinite(rse) & (rse > 0), rse, 0.5)
        # f_small includes r_AM/r_SE ratio
        ratio_S = ras_s / np.maximum(rse_s, 0.1)
        ratio_P = rap_s / np.maximum(rse_s, 0.1)
        sig_S = 1.0/(1.0+np.exp(-K_S*(r_cut_am/0.5 - ratio_S)))  # scale ratio by 0.5
        sig_P = 1.0/(1.0+np.exp(-K_S*(r_cut_am/0.5 - ratio_P)))
        f_small = (1.0 - p)*sig_S + p*sig_P
        return 1.0/(1.0+np.exp(-K_K*(f_small - 0.5)))

    for rc in [3.5, 4.0]:
        g = _g_phys_with_rSE(a, rc)
        phic = (1-g)*PHICP_F + g*PHICS_F
        pex = a[:, 0] - phic
        bl = (base_no_phi(a) + 0.5*np.log(np.sqrt(pex**2 + (DELTA_F*g)**2) + 1e-12)
              + np.log(cf))
        p2 = p2_feature(a[:, 0], a[:, 8], g_gate=g)
        cdc, _ = cov_delta_feature(a[:, 12])
        f_log = a[:, 19] if a.shape[1] >= 20 else np.zeros(a.shape[0])
        lo = _loocv_with_extras(bl, logsf, taus, [p2, cdc, f_log])
        tag = f"Alt-B r_SE-aware (ratio cutoff at r_AM/r_SE = {rc/0.5:.1f})"
        flag = "★" if lo > lo_ref + se_loocv else (" " if abs(lo - lo_ref) <= se_loocv else "⚠")
        print(f"  {tag:50s} {lo:7.4f} {lo - lo_ref:+10.4f}   {flag}")

    # Alt 3: Continuous power (no sigmoid)
    def _g_phys_power(a, r_cut, alpha):
        """f_small = (r_cut / r_AM_eff)^α, no sigmoid."""
        p = a[:, 6]
        ras = a[:, 17]; rap = a[:, 18]
        ras_s = np.where(np.isfinite(ras) & (ras > 0), ras, 2.5)
        rap_s = np.where(np.isfinite(rap) & (rap > 0), rap, 5.5)
        # composition-weighted r_AM
        r_eff = (1.0 - p)*ras_s + p*rap_s
        ratio = np.minimum(r_cut/np.maximum(r_eff, 0.5), 1.0)
        f_small = ratio**alpha
        return f_small   # already in [0, 1]

    for rc in [3.5, 4.5]:
        for alpha in [1.0, 2.0, 4.0]:
            g = _g_phys_power(a, rc, alpha)
            phic = (1-g)*PHICP_F + g*PHICS_F
            pex = a[:, 0] - phic
            bl = (base_no_phi(a) + 0.5*np.log(np.sqrt(pex**2 + (DELTA_F*g)**2) + 1e-12)
                  + np.log(cf))
            p2 = p2_feature(a[:, 0], a[:, 8], g_gate=g)
            cdc, _ = cov_delta_feature(a[:, 12])
            f_log = a[:, 19] if a.shape[1] >= 20 else np.zeros(a.shape[0])
            lo = _loocv_with_extras(bl, logsf, taus, [p2, cdc, f_log])
            tag = f"Alt-C power (r_cut={rc}, α={alpha:.1f})"
            flag = "★" if lo > lo_ref + se_loocv else (" " if abs(lo - lo_ref) <= se_loocv else "⚠")
            print(f"  {tag:50s} {lo:7.4f} {lo - lo_ref:+10.4f}   {flag}")

    print("\n" + "=" * 95)
    print("INTERPRETATION:")
    print("  • PART 1 best LOOCV → suggests refined (r_cut, K_S, K_K)")
    print("  • PART 2 swingable cases → which case the smooth treatment actually changes")
    print("  • PART 3 alternates → whether sigmoid is necessary or simpler form works")
    print("  • If alt-form ★ → simpler/more-physical form found")
    print("  • If r_SE-aware ★ → SE size matters too, not just AM")


if __name__ == "__main__":
    main()
