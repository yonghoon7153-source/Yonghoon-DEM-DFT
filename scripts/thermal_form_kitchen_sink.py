#!/usr/bin/env python3
"""σ_thermal — KITCHEN SINK approach: throw 50+ features at it.

After Approaches A/B/C failed (max LOOCV 0.05), try ALL available metrics
+ transforms + cross-terms + ratios.  Use Ridge regression to handle
overparameterization.  Greedy forward selection finds the optimal subset.

Strategy:
  1. Auto-discover ALL numeric fields per case
  2. Build base + log transforms for everything plausible
  3. Add cross-products and ratios of key pairs
  4. Forward-selection: add features one at a time, track LOOCV
  5. Report top features by Δ LOOCV contribution

Hope: discover a feature combination that breaks 0.9 LOOCV barrier.
"""
from __future__ import annotations
import sys, json, glob
from pathlib import Path
from collections import defaultdict
import numpy as np
from numpy.linalg import lstsq

KAPPA_MAX = 50.0; KAPPA_MIN = 0.05


def safe_log(v, floor=1e-6):
    return np.log(max(float(v), floor))


def safe_log_arr(arr, floor=1e-6):
    return np.log(np.maximum(arr.astype(float), floor))


def load_full_corpus():
    """Load every case with valid κ, extract ALL numeric fields."""
    cases = []
    for f in sorted(glob.glob('webapp/archive/**/full_metrics.json', recursive=True)):
        nm = Path(f).parent.name
        if not nm.startswith('input_'): continue
        try: d = json.load(open(f))
        except: continue
        kappa = (d.get('thermal_sigma_full_mScm_stage_e') or
                 d.get('thermal_sigma_full_mScm') or 0)
        if not (kappa and KAPPA_MIN <= kappa <= KAPPA_MAX): continue
        # Auto-extract all numeric scalar fields
        flat = {}
        for k, v in d.items():
            if isinstance(v, (int, float)) and np.isfinite(v):
                flat[k] = float(v)
            elif isinstance(v, dict):
                # Some metrics are nested dicts (e.g. coverage)
                for sk, sv in v.items():
                    if isinstance(sv, (int, float)) and np.isfinite(sv):
                        flat[f'{k}.{sk}'] = float(sv)
        flat['_name'] = nm
        flat['_kappa'] = float(kappa)
        cases.append(flat)
    return cases


def build_feature_matrix(cases, candidate_keys):
    """Build X for given feature keys.  Returns X, mask of cases with all valid."""
    n = len(cases)
    rows_valid = np.ones(n, bool)
    X_cols = []
    for key in candidate_keys:
        vals = np.zeros(n)
        for i, c in enumerate(cases):
            v = c.get(key)
            if v is None or not np.isfinite(v):
                rows_valid[i] = False
                vals[i] = 0
            else:
                vals[i] = v
        X_cols.append(vals)
    X = np.column_stack(X_cols) if X_cols else np.zeros((n, 0))
    return X, rows_valid


def fit_ridge_loocv(X, y, alpha=1.0):
    """Ridge regression + LOOCV.  Returns R², LOOCV, coef."""
    n, k = X.shape
    # Add intercept column
    X_ = np.column_stack([np.ones(n), X])
    # Ridge: (X^T X + alpha I) coef = X^T y, no penalty on intercept
    XtX = X_.T @ X_
    I = np.eye(k + 1); I[0, 0] = 0  # no penalty on intercept
    coef = np.linalg.solve(XtX + alpha * I, X_.T @ y)
    pred = X_ @ coef
    sse_fit = float(np.sum((y - pred)**2))
    ss_tot = float(np.sum((y - y.mean())**2))
    r2 = 1 - sse_fit/ss_tot if ss_tot > 0 else 0
    # LOOCV via leave-one-out
    sse_loo = 0.0
    for j in range(n):
        m = np.ones(n, bool); m[j] = False
        try:
            Xm = X_[m]; ym = y[m]
            cm = np.linalg.solve(Xm.T @ Xm + alpha * I, Xm.T @ ym)
            sse_loo += (y[j] - X_[j] @ cm)**2
        except: pass
    loocv = 1 - sse_loo/ss_tot if ss_tot > 0 else 0
    return r2, loocv, coef


def discover_common_keys(cases, min_coverage=0.95):
    """Find numeric keys present in ≥ min_coverage fraction of cases."""
    counts = defaultdict(int)
    for c in cases:
        for k in c:
            if not k.startswith('_'):
                counts[k] += 1
    n = len(cases)
    common = sorted(k for k, c in counts.items() if c / n >= min_coverage)
    return common


def main():
    print("\n  ── Loading corpus ──")
    cases = load_full_corpus()
    n = len(cases)
    if n < 20:
        print(f"[ABORT] n={n} too few"); return
    print(f"  Loaded {n} valid thermal cases")

    common_keys = discover_common_keys(cases, min_coverage=0.90)
    print(f"  Common numeric keys (≥90% coverage): {len(common_keys)}")

    # Target
    y_kappa = np.array([c['_kappa'] for c in cases])
    y_log = np.log(y_kappa)

    # ─── Round 1: All log-transformed common keys ───
    print()
    print("=" * 90)
    print("  Round 1: Ridge fit on ALL log-transformed common features")
    print("=" * 90)
    # Skip keys that are already log-scale (avoid double log) or non-positive ranges
    skip_keys = {'_name', '_kappa'}
    use_keys = [k for k in common_keys if k not in skip_keys]
    # Make log-features; keep only those with all positive values
    feature_data = []  # (label, values_array)
    for k in use_keys:
        vals = np.array([c.get(k, np.nan) for c in cases])
        if not np.all(np.isfinite(vals)): continue
        # Only log-transform positive metrics
        if np.min(vals) > 0:
            feature_data.append((f'log({k})', np.log(vals)))
        # Linear feature too
        feature_data.append((k, vals))

    print(f"  Total candidate features (linear + log): {len(feature_data)}")

    # Try Ridge fit with ALL features
    if len(feature_data) > 0:
        X_all = np.column_stack([v for _, v in feature_data])
        for alpha in [0.01, 0.1, 1.0, 10.0]:
            try:
                r2, loocv, coef = fit_ridge_loocv(X_all, y_log, alpha=alpha)
                flag = ' ⭐' if loocv >= 0.9 else (' ★' if loocv > 0.5 else '')
                print(f"  All {len(feature_data)} features, α={alpha:>5.2f}:  R²={r2:.3f}  LOOCV={loocv:.3f}{flag}")
            except Exception as e:
                print(f"  All features, α={alpha}: FAIL ({e})")

    # ─── Round 2: GREEDY FORWARD SELECTION ───
    print()
    print("=" * 90)
    print("  Round 2: Greedy forward selection (add best single feature per step)")
    print("=" * 90)
    selected_idx = []
    selected_labels = []
    remaining_idx = list(range(len(feature_data)))
    history = []
    best_loocv_overall = -np.inf
    for step in range(min(20, len(feature_data))):
        best_step_loo = -np.inf
        best_step_idx = None
        for idx in remaining_idx:
            try_idx = selected_idx + [idx]
            X = np.column_stack([feature_data[i][1] for i in try_idx])
            try:
                r2, loocv, _ = fit_ridge_loocv(X, y_log, alpha=0.1)
                if loocv > best_step_loo:
                    best_step_loo = loocv; best_step_idx = idx
            except: continue
        if best_step_idx is None: break
        selected_idx.append(best_step_idx)
        selected_labels.append(feature_data[best_step_idx][0])
        remaining_idx.remove(best_step_idx)
        history.append((step + 1, feature_data[best_step_idx][0], best_step_loo))
        if best_step_loo > best_loocv_overall:
            best_loocv_overall = best_step_loo
        flag = ' ⭐' if best_step_loo >= 0.9 else (' ★' if best_step_loo > 0.5 else '')
        print(f"  Step {step+1:2d}  add {feature_data[best_step_idx][0][:45]:45s}  "
              f"LOOCV={best_step_loo:.4f}{flag}")
        # stop if not improving by > 0.001
        if step >= 2 and history[-1][2] - history[-2][2] < 0.001:
            print(f"           ── plateau (Δ<0.001), stopping")
            break

    # ─── Round 3: Cross-terms and ratios ───
    print()
    print("=" * 90)
    print("  Round 3: Cross-products / ratios of selected features")
    print("=" * 90)
    if len(selected_idx) >= 2:
        cross_features = []
        # All pairwise log products and ratios from top 6 selected
        top6 = selected_idx[:6]
        for i_a, ia in enumerate(top6):
            for ib in top6[i_a+1:]:
                la, va = feature_data[ia]
                lb, vb = feature_data[ib]
                # product
                cross_features.append((f'({la}) × ({lb})', va * vb))
                # ratio (skip if either has zeros)
                if np.all(vb != 0):
                    cross_features.append((f'({la}) / ({lb})', va / np.where(vb == 0, 1e-6, vb)))
        print(f"  Generated {len(cross_features)} cross-features from top-{len(top6)} selected")

        # Best individual cross-feature added to selected baseline
        X_base = np.column_stack([feature_data[i][1] for i in selected_idx[:8]])
        r2_base, loo_base, _ = fit_ridge_loocv(X_base, y_log, alpha=0.1)
        print(f"  Base (top 8 selected): LOOCV={loo_base:.4f}")
        for label, vals in cross_features[:30]:
            X_try = np.column_stack([X_base, vals])
            try:
                r2, loocv, _ = fit_ridge_loocv(X_try, y_log, alpha=0.1)
                if loocv > loo_base + 0.005:
                    flag = ' ⭐' if loocv >= 0.9 else (' ★' if loocv > 0.5 else '')
                    print(f"    + {label[:55]:55s} → LOOCV={loocv:.4f}{flag}")
            except: pass

    print()
    print("=" * 90)
    print("  FINAL VERDICT")
    print("=" * 90)
    print(f"  Best LOOCV achieved by greedy selection: {best_loocv_overall:.4f}")
    if best_loocv_overall >= 0.9:
        print(f"  ⭐ MET user threshold (≥0.9) — adopt selected feature set!")
        print(f"  Selected features (in order):")
        for s, lbl, loo in history:
            print(f"    {s:>2d}. {lbl:50s}  LOOCV={loo:.4f}")
    elif best_loocv_overall >= 0.5:
        print(f"  ★ Above 0.5 but below 0.9 — still doesn't meet user requirement")
    else:
        print(f"  ✗ Below 0.5 — σ_thermal genuinely has weak signal in this corpus")
        print(f"  Recommendation: production = solver direct, no form")


if __name__ == '__main__':
    main()
