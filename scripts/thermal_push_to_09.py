#!/usr/bin/env python3
"""σ_thermal — push from 0.81 → 0.9+ with cross-products and feature interactions.

Physics Stage E target with structural-only greedy reached LOOCV 0.81.
Now try cross-products and ratios between top features to overcome
greedy plateau.
"""
from __future__ import annotations
import sys, json, glob
from pathlib import Path
import numpy as np
from numpy.linalg import solve
from collections import Counter

KAPPA_MAX = 50.0; KAPPA_MIN = 0.05


def load_corpus():
    cases = []
    for f in sorted(glob.glob('webapp/archive/**/full_metrics.json', recursive=True)):
        nm = Path(f).parent.name
        if not nm.startswith('input_'): continue
        try: d = json.load(open(f))
        except: continue
        kappa = d.get('thermal_sigma_full_mScm_stage_e_physics') or 0
        if not (KAPPA_MIN <= kappa <= KAPPA_MAX): continue
        flat = {'_name': nm, '_kappa': float(kappa)}
        for k, v in d.items():
            if isinstance(v, (int, float)) and np.isfinite(v):
                flat[k] = float(v)
            elif isinstance(v, dict):
                for sk, sv in v.items():
                    if isinstance(sv, (int, float)) and np.isfinite(sv):
                        flat[f'{k}.{sk}'] = float(sv)
        cases.append(flat)
    return cases


def fit_ridge_loocv(X, y, alpha=0.1):
    n = X.shape[1]
    X_ = np.column_stack([np.ones(len(y)), X])
    I = np.eye(n + 1); I[0, 0] = 0
    XtX = X_.T @ X_
    try:
        coef = solve(XtX + alpha * I, X_.T @ y)
    except: return 0, -np.inf, None
    pred = X_ @ coef
    sse_fit = float(np.sum((y - pred)**2))
    ss_tot = float(np.sum((y - y.mean())**2))
    r2 = 1 - sse_fit/ss_tot if ss_tot > 0 else 0
    sse_loo = 0.0
    for j in range(len(y)):
        m = np.ones(len(y), bool); m[j] = False
        Xm = X_[m]; ym = y[m]
        try:
            cm = solve(Xm.T @ Xm + alpha * I, Xm.T @ ym)
            sse_loo += (y[j] - X_[j] @ cm)**2
        except: pass
    loocv = 1 - sse_loo/ss_tot if ss_tot > 0 else 0
    return r2, loocv, coef


def main():
    cases = load_corpus()
    n = len(cases)
    print(f"\n  Loaded {n} cases (Physics Stage E target)\n")
    y = np.log(np.array([c['_kappa'] for c in cases]))

    EXCLUDE_PREFIXES = ('thermal_sigma', 'sigma_full_mScm',
                         'electronic_sigma_full_mScm', '_')
    EXCLUDE_EXACT = {
        'sigma_grain_factor_AM_P', 'sigma_grain_factor_AM_S', 'sigma_grain_factor_SE',
        'sigma_e_grain_factor_AM_P', 'sigma_e_grain_factor_AM_S',
        'kappa_grain_factor_AM_P', 'kappa_grain_factor_AM_S', 'kappa_grain_factor_SE',
    }
    def excluded(k):
        if k in EXCLUDE_EXACT: return True
        return any(k.startswith(p) for p in EXCLUDE_PREFIXES)

    counts = Counter()
    for c in cases:
        for k in c:
            if not excluded(k): counts[k] += 1
    common = [k for k, ct in counts.items() if ct / n >= 0.90]
    print(f"  Structural candidate features: {len(common)}")

    # Build feature data
    feature_data = {}
    for k in common:
        vals = np.array([c.get(k, np.nan) for c in cases])
        if not np.all(np.isfinite(vals)): continue
        if np.min(vals) > 0:
            feature_data[f'log({k})'] = np.log(vals)
        feature_data[k] = vals
    print(f"  Total candidate features: {len(feature_data)}")

    # ─── Start from previous best 7 features as baseline ───
    BASE_FEATURES = [
        'R_brug_over_full_physics',
        'log(overlap_pct_above_5)',
        'log(am_am_cn)',
        'R_bruggeman_over_full',
        'log(contact_pressure_mean)',
        'log(percolation_pct)',
    ]
    base_arrs = []
    for f in BASE_FEATURES:
        if f in feature_data:
            base_arrs.append(feature_data[f])
        else:
            print(f"  ⚠ missing: {f}")
    if len(base_arrs) < 4:
        print("[ABORT] base features missing"); return
    X_base = np.column_stack(base_arrs)
    r2_base, loo_base, _ = fit_ridge_loocv(X_base, y)
    print(f"\n  Base 6 features: R²={r2_base:.4f}  LOOCV={loo_base:.4f}\n")

    # ─── Try every other single feature as 7th addition ───
    print("=" * 90)
    print(f"  Step 7: try every remaining feature, find best to add")
    print("=" * 90)
    best_single = -np.inf; best_single_name = None
    for k, v in feature_data.items():
        if k in BASE_FEATURES: continue
        X_try = np.column_stack([X_base, v])
        try:
            _, loo, _ = fit_ridge_loocv(X_try, y)
            if loo > best_single:
                best_single = loo; best_single_name = k
        except: continue
    print(f"  Best 7th: {best_single_name}  LOOCV={best_single:.4f}")

    # ─── Try cross-products among base features ───
    print()
    print("=" * 90)
    print("  Cross-products: try every pairwise product of base features")
    print("=" * 90)
    cross_arrs = []
    cross_labels = []
    for i, fa in enumerate(BASE_FEATURES):
        if fa not in feature_data: continue
        for fb in BASE_FEATURES[i+1:]:
            if fb not in feature_data: continue
            cross_arrs.append(feature_data[fa] * feature_data[fb])
            cross_labels.append(f'({fa}) × ({fb})')
    print(f"  Generated {len(cross_arrs)} cross-products")

    best_cross = -np.inf; best_cross_label = None
    for lbl, arr in zip(cross_labels, cross_arrs):
        X_try = np.column_stack([X_base, arr])
        try:
            _, loo, _ = fit_ridge_loocv(X_try, y)
            if loo > best_cross:
                best_cross = loo; best_cross_label = lbl
        except: continue
    print(f"  Best cross: {best_cross_label}  LOOCV={best_cross:.4f}")

    # ─── Multi-add: base + best single + best cross ───
    print()
    print("=" * 90)
    print("  Combo: base + best_single + best_cross")
    print("=" * 90)
    extras = []
    if best_single_name and best_single_name in feature_data:
        extras.append(feature_data[best_single_name])
    if best_cross_label:
        idx = cross_labels.index(best_cross_label)
        extras.append(cross_arrs[idx])
    if extras:
        X_combo = np.column_stack([X_base] + extras)
        _, loo_combo, _ = fit_ridge_loocv(X_combo, y)
        print(f"  combo: LOOCV={loo_combo:.4f}")

    # ─── Round 2: greedy with cross-products ALLOWED ───
    print()
    print("=" * 90)
    print("  Round 2: greedy with cross-products allowed")
    print("=" * 90)
    # Add cross-products to feature pool
    all_features = dict(feature_data)
    for lbl, arr in zip(cross_labels, cross_arrs):
        all_features[lbl] = arr
    print(f"  Pool size: {len(all_features)}")

    selected = []; remaining = list(all_features.keys())
    best = -np.inf; history = []
    for step in range(15):
        best_step = -np.inf; best_k = None
        for k in remaining:
            try_keys = selected + [k]
            X = np.column_stack([all_features[kk] for kk in try_keys])
            try:
                _, loo, _ = fit_ridge_loocv(X, y, alpha=0.1)
                if loo > best_step:
                    best_step = loo; best_k = k
            except: continue
        if best_k is None: break
        selected.append(best_k); remaining.remove(best_k)
        flag = ' ⭐' if best_step >= 0.9 else (' ★' if best_step > 0.5 else '')
        print(f"  Step {step+1:2d}  add {best_k[:58]:58s}  LOOCV={best_step:.4f}{flag}")
        history.append((step+1, best_k, best_step))
        if best_step > best: best = best_step
        if step >= 3 and history[-1][2] - history[-2][2] < 0.001:
            print(f"           ── plateau, stopping")
            break

    print()
    print("=" * 90)
    print(f"  FINAL: best LOOCV = {best:.4f}")
    if best >= 0.9:
        print(f"  ⭐ MEETS 0.9 — adopt!")
    else:
        print(f"  ✗ Still {best:.4f} < 0.9.  Gap = {0.9 - best:.4f}")


if __name__ == '__main__':
    main()
