#!/usr/bin/env python3
"""σ_electronic residual diagnostic — find the missing predictor.

Stage 4 stuck at LOOCV ≈ 0.48 means current form can't explain ~50%
of σ_e variance.  Composition (p_amp), size (r̄_AM), thickness (T/d_AM)
all FAILED to provide a meaningful gain.

This script:
  1. Builds the Stage 4 form residuals (log σ_DEM − log σ_form)
  2. Sweeps EVERY numeric metric in full_metrics.json that has signal
     in the corpus
  3. Reports |Spearman ρ(residual, metric)| sorted descending
  4. Top correlations are candidate missing predictors

Also: prints top 5 outliers with their FULL metric dict side-by-side
so we can eyeball what's special about them.

Run on WSL:
    python3 scripts/electronic_resid_scan.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
from collections import defaultdict
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
import generate_comparison_plots as gcp
from electronic_nested_cv import (load_corpus_e, SIGMA_AM)
from scipy.stats import spearmanr


def main():
    a, names = load_corpus_e()
    n = len(a)
    if n < 10:
        print("[ABORT] need more cases on WSL.")
        return
    logsf = np.log(a[:, 5])
    phi_am = a[:, 0]; cn = a[:, 1]; cov = a[:, 2]; fp = a[:, 3]
    tau = a[:, 4]; p_amp = a[:, 6]
    r_AM_S = a[:, 8]; r_AM_P = a[:, 9]; T_um = a[:, 10]
    lt = np.log(tau)

    # Stage 4 form (best so far) ─ fit, get residuals
    r_eff = np.where(np.isfinite(r_AM_S), r_AM_S, 2.5)
    r_eff_P = np.where(np.isfinite(r_AM_P), r_AM_P, 5.5)
    r_eff = (1.0 - p_amp)*r_eff + p_amp*r_eff_P
    T_safe = np.where(np.isfinite(T_um) & (T_um > 0), T_um, 100.0)
    d_AM = 2.0 * r_eff
    log_r = np.log(np.maximum(r_eff, 0.5))
    log_Td = np.log(np.maximum(T_safe / d_AM, 0.1))
    X = np.column_stack([
        np.log(phi_am), np.log(fp), p_amp, log_r, log_Td,
        np.ones(n), lt, lt**2,
    ])
    y = logsf - np.log(SIGMA_AM)
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ coef
    resid = y - pred  # log-residual

    print("=" * 78)
    print(f" σ_electronic residual scan (n={n}, Stage 4 LOOCV ≈ 0.48 baseline)")
    print("=" * 78)
    print(f"  residual stats: mean={resid.mean():+.3f}  std={resid.std():.3f}")
    print(f"                  range=[{resid.min():+.2f}, {resid.max():+.2f}]")
    print()

    # ───── Scan ALL numeric metrics in raw full_metrics.json files ─────
    # Re-load raw dicts ALIGNED with the corpus (in same order as load_corpus_e).
    raw_dicts = []
    seen = set()
    for base in ('webapp/results', 'webapp/archive'):
        bp = Path(base)
        if not bp.is_dir(): continue
        for mp in bp.rglob('full_metrics.json'):
            try: d = json.load(open(mp))
            except Exception: continue
            from electronic_nested_cv import (_stage_e_electronic, _phi_am,
                                               _am_am_cn, _cov_am, _f_perc_e,
                                               _tau_e, _meta_name,
                                               _EXCLUDED_NAMES_EL, PHI_AM_MIN)
            sig = _stage_e_electronic(d)
            phi_amx = _phi_am(d); cnx = _am_am_cn(d)
            covx = _cov_am(d); fpx = _f_perc_e(d); taux = _tau_e(d)
            if not (sig and sig > 0 and phi_amx and phi_amx > PHI_AM_MIN
                    and cnx and cnx > 0 and covx and covx > 0
                    and fpx and fpx > 0 and taux and taux > 0):
                continue
            nm = _meta_name(mp.parent.name, mp.parent)
            if nm in _EXCLUDED_NAMES_EL: continue
            key = (round(phi_amx, 4), round(cnx, 3), round(float(sig), 5))
            if key in seen: continue
            seen.add(key); raw_dicts.append(d)
    assert len(raw_dicts) == n, f"{len(raw_dicts)} != {n} — alignment broken"

    # Collect all numeric metric names that have ≥80% non-null coverage
    metric_counts: dict[str, int] = defaultdict(int)
    for d in raw_dicts:
        for k, v in d.items():
            if isinstance(v, (int, float)) and not isinstance(v, bool) and np.isfinite(v):
                metric_counts[k] += 1
    candidate_keys = sorted([k for k, c in metric_counts.items() if c >= int(n * 0.8)])
    print(f"  Scanning {len(candidate_keys)} candidate metrics (≥80% coverage)")
    print()

    # Already in the form — skip these (no new info)
    in_form = {'phi_am', 'phi_se', 'am_am_cn', 'percolation_pct',
               'electronic_percolating_fraction', 'tortuosity_recommended',
               'tortuosity_mean'}
    in_form.update(_TARGET_KEYS_E := (
        'electronic_sigma_full_mScm', 'electronic_sigma_full_mScm_physics',
        'electronic_sigma_full_mScm_stage_e',
        'electronic_sigma_full_mScm_stage_e_physics',
        'sigma_full_mScm', 'sigma_full_mScm_physics',
        'sigma_full_mScm_stage_e', 'sigma_full_mScm_stage_e_physics',
    ))

    # Compute Spearman corr with residual for each metric
    sc = []
    for k in candidate_keys:
        if k in in_form: continue
        vals = np.array([d.get(k, np.nan) for d in raw_dicts], float)
        m = np.isfinite(vals)
        if m.sum() < 30: continue
        if np.std(vals[m]) < 1e-12: continue
        rho, p = spearmanr(vals[m], resid[m])
        if not np.isfinite(rho): continue
        sc.append((abs(rho), rho, k, m.sum(), p))
    sc.sort(reverse=True)

    print("─" * 78)
    print(" Top 30 metrics by |Spearman ρ(residual, metric)|")
    print(" Strong signals (|ρ|>0.4) = candidate missing predictors")
    print("─" * 78)
    print(f"  {'#':>3s}  {'metric':45s}  {'|ρ|':>5s}  {'ρ':>+6s}  {'p':>8s}  {'n':>4s}")
    for i, (absr, rho, k, cnt, pv) in enumerate(sc[:30], 1):
        flag = "  ★" if absr > 0.5 else ("  ←" if absr > 0.4 else "")
        print(f"  {i:>3d}  {k[:45]:45s}  {absr:5.3f}  {rho:+6.3f}  {pv:8.1e}  {cnt:>4d}{flag}")
    print()

    # ───── Top 5 outliers: full metric inspection ─────
    print("=" * 78)
    print(" Top-5 outlier cases — what's special about them?")
    print("=" * 78)
    order = np.argsort(-np.abs(resid))
    for i in order[:5]:
        nm = names[i] if i < len(names) else f"(idx{i})"
        sigma_dem = float(np.exp(logsf[i]))
        sigma_form = float(np.exp(pred[i] + np.log(SIGMA_AM)))
        err_pct = (sigma_form - sigma_dem) / sigma_dem * 100
        print(f"\n  {nm}  (residual={resid[i]:+.2f}, err {err_pct:+.0f}%)")
        print(f"    σ_DEM = {sigma_dem:.4f}  σ_form = {sigma_form:.4f}")
        # Show top-correlated metrics for this case
        d = raw_dicts[i]
        interesting = [k for _, _, k, _, _ in sc[:15]]
        for k in interesting:
            v = d.get(k)
            if isinstance(v, (int, float)) and np.isfinite(v):
                print(f"    {k:45s} = {v:>10.4f}")


if __name__ == '__main__':
    main()
