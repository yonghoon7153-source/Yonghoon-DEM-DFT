#!/usr/bin/env python3
"""σ_thermal — switch target to Physics Stage E + structural-only kitchen sink.

Audit revealed:
  - Hertz Stage E (current target): LOOCV 0.111, factor range 0.83-1.0 (pass-through)
  - Physics Stage E (alternative):  LOOCV 0.518 with minimal form (8 features)

Physics Stage E uses Tabor + volume plastic contact areas — larger, less
sensitive to point-contact noise.  Form fits ~5× better.

This script: Run greedy forward selection on Physics Stage E target with
structural-only features (no solver direct outputs).  Can we reach 0.9?
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
        # TARGET = Physics Stage E (new)
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
    print(f"\n  Loaded {n} cases (target = Physics Stage E)\n")
    if n < 20:
        print(f"[ABORT] n<20"); return
    y_log = np.log(np.array([c['_kappa'] for c in cases]))

    # EXCLUDE solver-direct outputs (cheating sources)
    EXCLUDE_PREFIXES = (
        'thermal_sigma', 'sigma_full_mScm',
        'electronic_sigma_full_mScm', '_',
    )
    EXCLUDE_EXACT = {
        'sigma_grain_factor_AM_P', 'sigma_grain_factor_AM_S', 'sigma_grain_factor_SE',
        'sigma_e_grain_factor_AM_P', 'sigma_e_grain_factor_AM_S',
        'kappa_grain_factor_AM_P', 'kappa_grain_factor_AM_S', 'kappa_grain_factor_SE',
    }
    def excluded(k):
        if k in EXCLUDE_EXACT: return True
        return any(k.startswith(p) for p in EXCLUDE_PREFIXES)

    # Discover features
    counts = Counter()
    for c in cases:
        for k in c:
            if not excluded(k): counts[k] += 1
    common = [k for k, c in counts.items() if c / n >= 0.90]
    print(f"  Structural candidate features: {len(common)}")

    feature_data = []
    for k in common:
        vals = np.array([c.get(k, np.nan) for c in cases])
        if not np.all(np.isfinite(vals)): continue
        if np.min(vals) > 0:
            feature_data.append((f'log({k})', np.log(vals)))
        feature_data.append((k, vals))
    print(f"  Total (linear + log): {len(feature_data)}")

    # Round 1: All Ridge
    print()
    print("=" * 90)
    print("  Round 1: All Ridge (Physics Stage E target, structural-only)")
    print("=" * 90)
    X_all = np.column_stack([v for _, v in feature_data])
    for alpha in [0.01, 0.1, 1.0, 10.0]:
        r2, loocv, _ = fit_ridge_loocv(X_all, y_log, alpha=alpha)
        flag = ' ⭐' if loocv >= 0.9 else (' ★' if loocv > 0.5 else '')
        print(f"  α={alpha:>5.2f}:  R²={r2:.4f}  LOOCV={loocv:.4f}{flag}")

    # Round 2: Greedy
    print()
    print("=" * 90)
    print("  Round 2: Greedy forward selection (Physics Stage E target)")
    print("=" * 90)
    selected = []; remaining = list(range(len(feature_data)))
    best = -np.inf; history = []
    for step in range(25):
        best_step = -np.inf; best_idx = None
        for idx in remaining:
            try_idx = selected + [idx]
            X = np.column_stack([feature_data[i][1] for i in try_idx])
            _, loocv, _ = fit_ridge_loocv(X, y_log, alpha=0.1)
            if loocv > best_step:
                best_step = loocv; best_idx = idx
        if best_idx is None: break
        selected.append(best_idx)
        remaining.remove(best_idx)
        flag = ' ⭐' if best_step >= 0.9 else (' ★' if best_step > 0.5 else '')
        print(f"  Step {step+1:2d}  add {feature_data[best_idx][0][:58]:58s}  LOOCV={best_step:.4f}{flag}")
        history.append((step+1, feature_data[best_idx][0], best_step))
        if best_step > best: best = best_step
        if step >= 3 and history[-1][2] - history[-2][2] < 0.001:
            print(f"           ── plateau (Δ<0.001), stopping")
            break

    print()
    print("=" * 90)
    print(f"  VERDICT: Physics Stage E target, structural-only")
    print("=" * 90)
    print(f"  Best LOOCV: {best:.4f}")
    print(f"  Previous Hertz Stage E target best (structural-only): 0.4409")
    print(f"  Improvement: +{best - 0.4409:.4f}")
    if best >= 0.9:
        print(f"  ⭐ Switch production target to Physics Stage E + adopt this form!")
    elif best >= 0.5:
        print(f"  ★ Significant improvement but still below 0.9")
    else:
        print(f"  Below 0.5 — still genuine signal limitation")


if __name__ == '__main__':
    main()
