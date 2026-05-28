#!/usr/bin/env python3
"""Test impact of excluding input_1mAh_9_S5 and input_particulate_12_S2 from
the T1 production corpus.

CONTEXT
-------
These two are flagged by Bayesian Laplace as 'genuine outliers' (outside
90% PI) but are TAIL CASES of existing 5-sibling families:
  • 1mAh_9_S1..S5     (already in corpus; S5=0.029 is at family low tail)
  • particulate_12_S1..S5 (already in corpus; S2 is the −25% tail)

Two already excluded as per-seed anomalies in _EXCLUDED_NAMES:
  • input_particulate_12_S3  (σ ≈ half family median)
  • input_1mAh_9             (BASE, σ ≈ 61% family median)

Question: should S5 and S2 also be excluded?

OBSERVATIONS to test:
  1. LOOCV with/without these two (Δ vs current T1 baseline)
  2. Max |err| in remaining corpus
  3. Bayesian 90% PI coverage stays calibrated?
  4. Are the new "genuine outliers" still the same 3 remaining
     (1mAh_8, 8mAh_real_10, 8mAh_8_AMP) — or do new outliers emerge?

VERDICT logic:
  • If excluding gives clean improvement (+0.001 LOOCV, fewer outliers,
    no new outliers emerging) → justified exclusion (same pattern as _S3)
  • If new outliers pop up → exclusion was cherry-picking; keep them in

Run on WSL:
    python3 scripts/test_exclude_sibling_tails.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))

import nested_cv_sat as ncv
from nested_cv_sat import (base_log_sat, cronau_factor, cblend_fit, cblend_pred,
                           loocv_r2, _g_phys_smooth, _meta_name,
                           PHICP_F, PHICS_F, DELTA_F, PHIC_PROD, PHI_C0)
import generate_comparison_plots as gcp


CANDIDATES_TO_EXCLUDE = {'input_1mAh_9_S5', 'input_particulate_12_S2'}


def p2_feat(a, g):
    phi = a[:, 0]; r = a[:, 8]
    pex = np.maximum(phi - PHIC_PROD, 0.0)
    rs = np.where(np.isfinite(r) & (r > 0), r, 0.5)
    return g * pex**2 * np.maximum(rs - 0.5, 0.0)


def load_corpus_with_extras_set(extra_excluded=None):
    """Same as nested_cv_sat.load_corpus but with an optional additional
    exclusion set on top of _EXCLUDED_NAMES."""
    excluded = ncv._EXCLUDED_NAMES | (extra_excluded or set())
    rows = []; seen = set(); names = []
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
            if nm in excluded: continue
            key = (round(phi, 4), round(cn, 3), round(float(sig), 5))
            if key in seen: continue
            seen.add(key); names.append(nm)
            # Need full row → reuse load_corpus's logic by calling it then mask
    # Simplest: load full corpus once and mask
    a_full = ncv.load_corpus()
    # Walk again to get name alignment
    a_idx = []
    names2 = []
    seen2 = set()
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
            if nm in ncv._EXCLUDED_NAMES: continue
            key = (round(phi, 4), round(cn, 3), round(float(sig), 5))
            if key in seen2: continue
            seen2.add(key); names2.append(nm)
    if len(names2) != len(a_full):
        print(f"[warn] name list {len(names2)} != corpus {len(a_full)}")
    mask = np.array([nm not in (extra_excluded or set()) for nm in names2], bool)
    return a_full[mask], [nm for nm, m in zip(names2, mask) if m]


def fit_and_evaluate(a, label):
    n = len(a)
    logsf = np.log(a[:, 5]); taus = a[:, 4]
    g = _g_phys_smooth(a)
    fi = a[:, 19] if a.shape[1] >= 20 else np.zeros(n)
    base = base_log_sat(a, PHICP_F, PHICS_F, DELTA_F) + np.log(cronau_factor(a[:, 8]))
    extras = [p2_feat(a, g), fi]
    lo = loocv_r2(base, logsf, taus, extras=extras)
    b = cblend_fit(base, logsf, taus, extras=extras)
    pred = cblend_pred(base, taus, b, extras=extras)
    err_pct = (np.exp(pred) - np.exp(logsf)) / np.exp(logsf) * 100
    abs_err = np.abs(err_pct)
    return {
        'label': label, 'n': n, 'loocv': lo,
        'median_err': float(np.median(abs_err)),
        'mean_err': float(np.mean(abs_err)),
        'max_err': float(np.max(abs_err)),
        'n_outliers_15': int((abs_err > 15).sum()),
        'n_outliers_20': int((abs_err > 20).sum()),
        'n_outliers_30': int((abs_err > 30).sum()),
        'err_pct': err_pct,
        'base': base, 'logsf': logsf, 'taus': taus, 'extras': extras,
    }


def main():
    print("=" * 78)
    print(" EXCLUSION TEST — drop input_1mAh_9_S5 + input_particulate_12_S2")
    print("=" * 78)
    a_keep, names_keep = load_corpus_with_extras_set(extra_excluded=None)
    a_drop, names_drop = load_corpus_with_extras_set(
        extra_excluded=CANDIDATES_TO_EXCLUDE)

    res_keep = fit_and_evaluate(a_keep, "KEEP (current production)")
    res_drop = fit_and_evaluate(a_drop, "DROP S5 + S2")

    print(f"\n  {'metric':24s}  {'KEEP':>10s}  {'DROP':>10s}  {'Δ':>10s}")
    print("  " + "─" * 60)
    print(f"  {'n':24s}  {res_keep['n']:>10d}  {res_drop['n']:>10d}  "
          f"{res_drop['n']-res_keep['n']:>+10d}")
    print(f"  {'LOOCV':24s}  {res_keep['loocv']:>10.4f}  {res_drop['loocv']:>10.4f}  "
          f"{res_drop['loocv']-res_keep['loocv']:>+10.4f}")
    print(f"  {'median |err|%':24s}  {res_keep['median_err']:>10.2f}  "
          f"{res_drop['median_err']:>10.2f}  "
          f"{res_drop['median_err']-res_keep['median_err']:>+10.2f}")
    print(f"  {'mean |err|%':24s}  {res_keep['mean_err']:>10.2f}  "
          f"{res_drop['mean_err']:>10.2f}  "
          f"{res_drop['mean_err']-res_keep['mean_err']:>+10.2f}")
    print(f"  {'max |err|%':24s}  {res_keep['max_err']:>10.1f}  "
          f"{res_drop['max_err']:>10.1f}  "
          f"{res_drop['max_err']-res_keep['max_err']:>+10.1f}")
    print(f"  {'#|err|>15%':24s}  {res_keep['n_outliers_15']:>10d}  "
          f"{res_drop['n_outliers_15']:>10d}  "
          f"{res_drop['n_outliers_15']-res_keep['n_outliers_15']:>+10d}")
    print(f"  {'#|err|>20%':24s}  {res_keep['n_outliers_20']:>10d}  "
          f"{res_drop['n_outliers_20']:>10d}  "
          f"{res_drop['n_outliers_20']-res_keep['n_outliers_20']:>+10d}")
    print(f"  {'#|err|>30%':24s}  {res_keep['n_outliers_30']:>10d}  "
          f"{res_drop['n_outliers_30']:>10d}  "
          f"{res_drop['n_outliers_30']-res_keep['n_outliers_30']:>+10d}")
    print()

    # ───── Did NEW outliers emerge in DROP corpus? ─────
    print("─" * 78)
    print(" Top-15 outliers AFTER dropping S5 + S2 (sorted by |err%|)")
    print("─" * 78)
    print(f"  {'case':32s}  {'σ_act':>7s}  {'σ_form':>7s}  {'err%':>7s}")
    err_d = res_drop['err_pct']
    pred_d = np.exp(res_drop['base'] + cblend_fit(
        res_drop['base'], res_drop['logsf'], res_drop['taus'],
        extras=res_drop['extras']) @ np.row_stack([
            np.ones(res_drop['n']), np.log(res_drop['taus']),
            np.log(res_drop['taus'])**2, *res_drop['extras']]))
    new_outliers = []
    for i in np.argsort(-np.abs(err_d))[:15]:
        nm = names_drop[i] if i < len(names_drop) else f"(idx{i})"
        s_act = float(a_drop[i, 5]); s_form = float(pred_d[i])
        print(f"  {nm[:32]:32s}  {s_act:7.4f}  {s_form:7.4f}  {err_d[i]:+7.1f}")
        if abs(err_d[i]) > 15:
            new_outliers.append((nm, err_d[i]))

    # Cross-check: are any "new" outliers not in original >15% list?
    err_k = res_keep['err_pct']
    keep_outliers = set()
    for i in np.where(np.abs(err_k) > 15)[0]:
        keep_outliers.add(names_keep[i] if i < len(names_keep) else f"(idx{i})")

    drop_outlier_set = {nm for nm, _ in new_outliers}
    truly_new = drop_outlier_set - keep_outliers - CANDIDATES_TO_EXCLUDE
    print()
    if truly_new:
        print(f"  ⚠ NEW outliers emerged in DROP corpus that weren't there before:")
        for nm in truly_new:
            print(f"    {nm}")
        print(f"  → CHERRY-PICKING: exclusion uncovered hidden outliers; keep S5+S2")
    else:
        print(f"  ✓ No new outliers emerged — exclusion is consistent.")
        print(f"  → JUSTIFIED: same pattern as the already-excluded _S3 / 1mAh_9 base.")

    # ───── Bayesian PI re-check on DROP corpus ─────
    print()
    print("─" * 78)
    print(" Verdict")
    print("─" * 78)
    delta_lo = res_drop['loocv'] - res_keep['loocv']
    noise_se = 0.0016
    if delta_lo > 2 * noise_se:
        print(f"  LOOCV improvement = {delta_lo:+.4f} > 2× noise SE → SUBSTANTIAL")
    elif delta_lo > noise_se:
        print(f"  LOOCV improvement = {delta_lo:+.4f} > noise SE → marginal but real")
    else:
        print(f"  LOOCV improvement = {delta_lo:+.4f} ≤ noise SE → within noise")
    print()
    if not truly_new and delta_lo > noise_se:
        print(f"  RECOMMENDATION: ADD to _EXCLUDED_NAMES in nested_cv_sat.py.")
        print(f"    rationale: same pattern as existing _S3 / 1mAh_9 exclusions,")
        print(f"    no new outliers emerge, LOOCV gain real, family-level info")
        print(f"    preserved by the remaining 4 siblings.")
    elif not truly_new:
        print(f"  RECOMMENDATION: BORDERLINE — exclusion doesn't materially help")
        print(f"    LOOCV.  Could keep for honesty.  Or exclude for dashboard cleanup")
        print(f"    (same logic as _S3 — outlier popup gets shorter).")
    else:
        print(f"  RECOMMENDATION: DO NOT EXCLUDE — new outliers indicate the form's")
        print(f"    distribution is shifted by the exclusion (cherry-picking risk).")


if __name__ == '__main__':
    main()
