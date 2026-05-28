#!/usr/bin/env python3
"""Test the CLEAN integrated σ_ionic form vs the C4+F4 form.

User direction: "수식을 전체적으로 정갈하게 만들어봐 묶을건 묶고 수정할건
수정하고 중복된건 빼고" (make the equation clean overall, group, remove
duplicates).

Hypothesis: β_cov·Δcov (β ≈ -0.005, very small) is essentially noise
that can be DROPPED without LOOCV loss once f_intact is included (β_F
≈ +0.193 absorbs the relevant 'effective contact area' physics more
strongly).  The clean integrated form:

  σ = σ_grain · Cronau(r_SE) · (φ_eff)^½ · CN² · (cov · f_intact^γ)^½ · f_p³
      · exp[C(τ) + β_P2·P2]

where γ = 2β_F (data-fit ≈ 0.39).  This INTEGRATES the fracture-aware
correction into the existing Holm cov^½ term (multiplicative effective
cov), removes the redundant β_cov·Δcov, and reduces to 5 live params:
  a, b, c, β_P2, β_F   (n/k = 90/5 = 18:1)

Tests 4 forms:
  L4.  C_blend logpoly2 alone               (3 params)   — bare
  C4.  + β_P2·P2 + β_cov·Δcov               (5 params)   — current production
  C5.  + β_F·log f_intact (kept Δcov)       (6 params)   — F4 ADD, redundant
  C6.  C4 − Δcov + β_F·log f_intact         (5 params)   — CLEAN (proposed)
  C6b. (5 params)  same as C6 (sanity)

For each: LOOCV, AIC, BIC, |err|>30%, |err|>20%, max err.

Run from the repo root:  python3 scripts/test_clean_form.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
import generate_comparison_plots as gcp  # noqa
from nested_cv_sat import (load_corpus, base_log_sat, cblend_fit, cblend_pred,
                           cronau_factor, p2_feature, cov_delta_feature,
                           _meta_name, _EXCLUDED_NAMES,
                           PHICP_F, PHICS_F, DELTA_F, K_PS, P_C, PHI_C0)


def _f_intact_log_from_metrics(metrics):
    """log(1 − fracture_aware_excluded_pct/100), clipped at f_intact≥0.05."""
    out = []
    for d in metrics:
        frx = d.get('fracture_aware_excluded_pct')
        if frx is not None and isinstance(frx, (int, float)):
            out.append(float(np.log(max(1.0 - float(frx)/100.0, 0.05))))
        else:
            out.append(0.0)
    return np.array(out)


def _load_aligned_metrics(a):
    """Re-walk corpus aligned with `a` row order; return metrics dict list + names."""
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
            if nm in _EXCLUDED_NAMES:
                continue
            key = (round(phi, 4), round(cn, 3), round(float(sig), 5))
            if key in seen: continue
            seen.add(key)
            names.append(nm)
            metrics.append(d)
    return names, metrics


def _loocv_with_extras(base, logsf, taus, extras):
    """LOOCV with joint OLS for [logpoly2, *extras]."""
    n = len(taus); ss = float(np.sum((logsf-logsf.mean())**2)); sse = 0.0
    lt = np.log(taus)
    X = np.column_stack([np.ones(n), lt, lt**2] + list(extras)) if extras \
        else np.column_stack([np.ones(n), lt, lt**2])
    coef_full, *_ = np.linalg.lstsq(X, logsf - base, rcond=None)
    pred_full = base + X @ coef_full
    sse_in = float(np.sum((logsf - pred_full)**2))
    for i in range(n):
        m = np.ones(n, bool); m[i] = False
        coef, *_ = np.linalg.lstsq(X[m], logsf[m] - base[m], rcond=None)
        pi = base[i] + X[i] @ coef
        sse += (logsf[i] - pi)**2
    return 1 - sse/ss, sse_in, coef_full, pred_full


def _aic_bic(sse, n, k):
    """k = number of free OLS params."""
    return n*np.log(sse/n) + 2*k, n*np.log(sse/n) + np.log(n)*k


def _bands_summary(err_pct):
    ae = np.abs(err_pct)
    return {'≤10%': float((ae <= 10).mean()*100),
            '≤20%': float((ae <= 20).mean()*100),
            '≤30%': float((ae <= 30).mean()*100),
            '>30%': int((ae > 30).sum()),
            '>50%': int((ae > 50).sum()),
            'max': float(np.max(ae)),
            'median': float(np.median(ae)),
            'mean': float(np.mean(ae))}


def main():
    a = load_corpus()
    n = len(a)
    if n < 20:
        print(f"[ABORT] only {n} cases."); return
    names, metrics = _load_aligned_metrics(a)
    logsf = np.log(a[:, 5]); taus = a[:, 4]

    # Base (geometric, SAT × Cronau)
    cf = cronau_factor(a[:, 8])
    base = base_log_sat(a, PHICP_F, PHICS_F, DELTA_F) + np.log(cf)

    # Build all candidate features
    p2 = p2_feature(a[:, 0], a[:, 8], p_amp=a[:, 6])
    dcov, _med = cov_delta_feature(a[:, 12])
    f_log = _f_intact_log_from_metrics(metrics)

    forms = [
        ('L4. logpoly2 bare (3 params)',           [],                       3),
        ('C4. + P2 + Δcov (5 params, current prod)', [p2, dcov],              5),
        ('C5. + P2 + Δcov + f_intact (6 params)',  [p2, dcov, f_log],        6),
        ('C6. + P2 + f_intact (5 params, CLEAN)',  [p2, f_log],              5),
        ('   D1. f_intact alone (4 params)',       [f_log],                  4),
        ('   D2. P2 + f_intact + Δcov (6 same as C5)', [p2, f_log, dcov],    6),
    ]

    print("=" * 95)
    print(f"  CLEAN FORM COMPARISON   n={n}   "
          f"(noise SE on LOOCV ≈ {np.sqrt(np.var((logsf-logsf.mean())**2)/n)/np.sum((logsf-logsf.mean())**2):.4f})")
    print("=" * 95)
    print(f"  {'form':50s} {'LOOCV':>7s} {'AIC':>8s} {'BIC':>8s}  {'≤10%':>5s} {'≤20%':>5s} {'≤30%':>5s} {'>30%':>4s} {'>50%':>4s}")
    print("  " + "-" * 93)

    results = {}
    for tag, extras, k in forms:
        lo, sse_in, coef, pred = _loocv_with_extras(base, logsf, taus, extras)
        aic, bic = _aic_bic(sse_in, n, k)
        err_pct = (np.exp(pred) - np.exp(logsf)) / np.exp(logsf) * 100.0
        b = _bands_summary(err_pct)
        results[tag] = (lo, aic, bic, k, coef, b, err_pct)
        print(f"  {tag:50s} {lo:7.4f} {aic:+8.2f} {bic:+8.2f}  "
              f"{b['≤10%']:>4.0f}% {b['≤20%']:>4.0f}% {b['≤30%']:>4.0f}% {b['>30%']:>4d} {b['>50%']:>4d}")
        # show coefficients
        coef_str = ", ".join(f"{c:+.3f}" for c in coef)
        print(f"      coef [a,b,c, β...] = [{coef_str}]")

    # Pairwise comparison: which has best LOOCV per parameter?
    print("\n" + "=" * 95)
    print("  Pairwise comparisons:")
    print("=" * 95)
    pairs = [
        ('C5 vs C4', 'C5. + P2 + Δcov + f_intact (6 params)', 'C4. + P2 + Δcov (5 params, current prod)'),
        ('C6 vs C5', 'C6. + P2 + f_intact (5 params, CLEAN)', 'C5. + P2 + Δcov + f_intact (6 params)'),
        ('C6 vs C4', 'C6. + P2 + f_intact (5 params, CLEAN)', 'C4. + P2 + Δcov (5 params, current prod)'),
        ('D1 vs C6', '   D1. f_intact alone (4 params)', 'C6. + P2 + f_intact (5 params, CLEAN)'),
    ]
    for tag, na, nb in pairs:
        la, aica, bica, ka, _, _, _ = results[na]
        lb, aicb, bicb, kb, _, _, _ = results[nb]
        d_lo = la - lb; d_aic = aica - aicb; d_bic = bica - bicb
        print(f"   {tag:15s}: ΔLOOCV={d_lo:+.4f}  ΔAIC={d_aic:+.2f}  ΔBIC={d_bic:+.2f}  Δk={ka-kb:+d}")

    # Per-outlier shift table for top 10 outliers in C4 reference
    print("\n" + "=" * 95)
    print("  Per-outlier shift across forms (top 10 |err|>20% in C4)")
    print("=" * 95)
    _, _, _, _, _, _, err_c4 = results['C4. + P2 + Δcov (5 params, current prod)']
    out_idx = np.where(np.abs(err_c4) > 20)[0]
    out_idx = out_idx[np.argsort(-np.abs(err_c4[out_idx]))][:10]
    header = f"  {'case':30s} | " + " | ".join(f"{t[:15]:>8s}" for t in ['L4', 'C4', 'C5', 'C6', 'D1', 'D2'])
    print(header)
    print("  " + "-" * (len(header) - 2))
    short = ['L4', 'C4', 'C5', 'C6', 'D1', 'D2']
    all_errs = {}
    for tag, _, _ in forms:
        sn = tag.strip().split('.')[0].strip()
        all_errs[sn] = results[tag][6]
    for i in out_idx:
        row = f"  {names[i][:30]:30s} | "
        row += " | ".join(f"{all_errs[s][i]:+7.1f}%" for s in short)
        print(row)

    print("\n" + "=" * 95)
    print("INTERPRETATION:")
    print("  • C6 is the CLEAN form (5 params, no Δcov, integrated f_intact in Holm cov^½)")
    print("    If C6 LOOCV/AIC ≈ C5 within noise → Δcov was redundant; ADOPT C6")
    print("  • D1 is bare f_intact only — tests if P2 still adds value after F4")
    print("  • C5 = C4 + F4 added; D2 = C5 re-ordered (sanity, should match C5)")
    print()
    print("Decision rule for the FINAL production form:")
    print("  C6 LOOCV ≥ C5 within noise SE → CLEAN form wins, fewer params")
    print("  C6 LOOCV < C5 − noise SE      → Δcov adds real value, keep it (use C5)")


if __name__ == "__main__":
    main()
