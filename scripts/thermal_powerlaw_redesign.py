#!/usr/bin/env python3
"""σ_thermal 2-phase EMT power-law redesign.

Current production: 16-feature Ridge (mix of log + raw features) → hybrid
form, reviewer-objectionable ("not multiplicative").

This script tests pure-multiplicative alternatives:
  A. ALL-LOG Ridge: force every feature to log → κ = ∏ feature^coef
     (pure power-law, same 16 features but multiplicative)
  B. 2-phase EMT backbone: κ = κ_AM^a · κ_SE^b · structural^...
     physically-grounded, fewer params
  C. Compact power-law: greedy on log-only features, stop at ~6-8

Goal: multiplicative form (reviewer-proof) + ≤8 params + LOOCV ≥ 0.85
(ideally ≥0.90).  Compare to current Ridge 0.901.
"""
import sys, json, glob
from pathlib import Path
from collections import Counter
import numpy as np
from numpy.linalg import solve

sys.path.insert(0, 'scripts')
import generate_comparison_plots as gcp

KAPPA_MAX = 50.0; KAPPA_MIN = 0.05
EXCL = gcp._EXCLUDED_NAMES_EL


def load():
    cases = []
    seen = set()
    for base in ('webapp/archive', 'webapp/results'):
        for f in sorted(glob.glob(f'{base}/**/full_metrics.json', recursive=True)):
            nm = Path(f).parent.name
            if not nm.startswith('input_') or nm in seen: continue
            seen.add(nm)
            try: d = json.load(open(f))
            except: continue
            kappa = d.get('thermal_sigma_full_mScm_stage_e_physics') or 0
            if not (KAPPA_MIN <= kappa <= KAPPA_MAX): continue
            if nm in EXCL: continue
            d['_name'] = nm; d['_kappa'] = float(kappa)
            cases.append(d)
    return cases


# Features that leak the target (solver direct outputs) — NEVER use as predictor
TARGET_LEAK = (
    'thermal_sigma', 'sigma_full_mScm', 'electronic_sigma_full_mScm',
    'stage_e_le_baseline_kappa',  # = κ baseline, direct leak
)
def is_leak(k):
    return any(p in k for p in TARGET_LEAK)


def safe_log_feature(vals):
    """Transform any real-valued feature into a log-space predictor.
    - all-positive: log(v)
    - has non-positive: signed symlog = sign(v)·log(1+|v|)
    Returns (transformed_array, mode) or None if constant."""
    vals = np.asarray(vals, dtype=float)
    if not np.all(np.isfinite(vals)): return None
    if np.std(vals) < 1e-12: return None
    if np.min(vals) > 0:
        return np.log(vals), 'log'
    # signed symlog for features with zeros/negatives (R_brug ratios etc.)
    return np.sign(vals) * np.log1p(np.abs(vals)), 'symlog'


def _get_nested(d, key):
    if '.' not in key: return d.get(key)
    v = d
    for p in key.split('.'):
        if isinstance(v, dict): v = v.get(p)
        else: return None
    return v


def fit_loocv(X, y, alpha=0.05):
    n = X.shape[1]
    X_ = np.column_stack([np.ones(len(y)), X])
    I = np.eye(n + 1); I[0, 0] = 0
    try:
        coef = solve(X_.T @ X_ + alpha * I, X_.T @ y)
    except: return None
    pred = X_ @ coef
    ss_tot = float(np.sum((y - y.mean())**2))
    r2 = 1 - float(np.sum((y - pred)**2))/ss_tot if ss_tot > 0 else 0
    sse_loo = 0.0
    for j in range(len(y)):
        m = np.ones(len(y), bool); m[j] = False
        Xm = X_[m]
        try:
            cm = solve(Xm.T @ Xm + alpha*I, Xm.T @ y[m])
            sse_loo += (y[j] - X_[j] @ cm)**2
        except: pass
    loo = 1 - sse_loo/ss_tot if ss_tot > 0 else 0
    return r2, loo, coef


def main():
    cases = load()
    n = len(cases)
    print(f"\nCorpus (post-EXCL): {n}\n")
    y = np.log(np.array([c['_kappa'] for c in cases]))

    # ─── A. Current 16 features but SYMLOG (pure power-law, signed) ───
    print("=" * 90)
    print("  A. Current 16 features → SYMLOG (pure multiplicative, signed for ratios)")
    print("=" * 90)
    feats_16 = [f[0] for f in gcp._THERMAL_T1_FEATURES]
    cols = []; labels = []; dropped = []
    for fk in feats_16:
        vals = np.array([_get_nested(c, fk) if _get_nested(c, fk) is not None else np.nan
                         for c in cases], dtype=float)
        tr = safe_log_feature(vals)
        if tr is None: dropped.append(fk); continue
        cols.append(tr[0]); labels.append(f'{tr[1]}({fk})')
    if dropped:
        print(f"  dropped (constant/nan): {dropped}")
    X = np.column_stack(cols)
    res = fit_loocv(X, y)
    print(f"  SYMLOG ({len(labels)} feat): R²={res[0]:.4f}  LOOCV={res[1]:.4f}")
    print(f"  → κ = exp(c0) · ∏ feature_i^c_i  (signed-log for ratio features)")
    print()

    # ─── B. 2-phase EMT backbone ───
    print("=" * 90)
    print("  B. 2-phase EMT power-law backbone")
    print("=" * 90)
    # κ ≈ κ_AM_eff^w_AM · κ_SE_eff^w_SE · structural corrections
    # Use literature κ: κ_AM=4 W/mK, κ_SE=0.7 W/mK (in mScm-equiv after norm)
    # Backbone features (all log):
    def feat(c, k, default=None):
        v = _get_nested(c, k)
        return float(v) if isinstance(v, (int, float)) and np.isfinite(v) else default

    backbone_sets = [
        ("B1: φ_AM + φ_SE only",
         ['phi_am', 'phi_se']),
        ("B2: + se_se_cn (SE backbone)",
         ['phi_am', 'phi_se', 'se_se_cn']),
        ("B3: + porosity",
         ['phi_am', 'phi_se', 'se_se_cn', 'porosity']),
        ("B4: + tortuosity_median",
         ['phi_am', 'phi_se', 'se_se_cn', 'porosity', 'tortuosity_median']),
        ("B5: + R_brug_over_full_physics (EMT ratio)",
         ['phi_am', 'phi_se', 'se_se_cn', 'porosity', 'tortuosity_median', 'R_brug_over_full_physics']),
        ("B6: + gb_density_mean",
         ['phi_am', 'phi_se', 'se_se_cn', 'porosity', 'tortuosity_median', 'R_brug_over_full_physics', 'gb_density_mean']),
        ("B7: + area_SE_SE_total_physics (Holm)",
         ['phi_am', 'phi_se', 'se_se_cn', 'porosity', 'tortuosity_median', 'R_brug_over_full_physics', 'gb_density_mean', 'area_SE_SE_total_physics']),
    ]
    print(f"  {'variant':50s} {'k':>3s} {'n/k':>6s} {'R²':>7s} {'LOOCV':>7s}")
    for label, fks in backbone_sets:
        cols = []; ok = True
        for fk in fks:
            vals = np.array([feat(c, fk, np.nan) for c in cases])
            tr = safe_log_feature(vals)
            if tr is None: ok = False; break
            cols.append(tr[0])
        if not ok:
            print(f"  {label:50s}  (skip — constant/nan feature)")
            continue
        X = np.column_stack(cols)
        res = fit_loocv(X, y)
        k = X.shape[1] + 1
        flag = ' ⭐' if res[1] >= 0.9 else (' ★' if res[1] > 0.85 else '')
        print(f"  {label:50s} {k:>3d} {n/k:>6.1f} {res[0]:>6.3f} {res[1]:>6.3f}{flag}")
    print()

    # ─── C. Compact greedy on symlog features (target-leak excluded) ───
    print("=" * 90)
    print("  C. Compact greedy (symlog features, NO target-leak, stop at plateau)")
    print("=" * 90)
    candidates = {}
    common = Counter()
    for c in cases:
        for k, v in c.items():
            if k.startswith('_'): continue
            if isinstance(v, (int, float)): common[k] += 1
            elif isinstance(v, dict):
                for sk, sv in v.items():
                    if isinstance(sv, (int, float)): common[f'{k}.{sk}'] += 1
    for k, ct in common.items():
        if ct/n < 0.9: continue
        if is_leak(k): continue   # exclude solver direct outputs (target leak)
        vals = np.array([_get_nested(c, k) if _get_nested(c, k) is not None else np.nan
                         for c in cases], dtype=float)
        tr = safe_log_feature(vals)
        if tr is not None:
            candidates[f'{tr[1]}({k})'] = tr[0]
    print(f"  symlog candidates (leak-free): {len(candidates)}")
    cand_items = list(candidates.items())
    selected = []; sel_arrs = []; best = -np.inf
    hist = []
    for step in range(12):
        best_step = -np.inf; best_i = None
        for i, (lbl, arr) in enumerate(cand_items):
            if i in [s[0] for s in selected]: continue
            X = np.column_stack(sel_arrs + [arr])
            r = fit_loocv(X, y)
            if r and r[1] > best_step:
                best_step = r[1]; best_i = i
        if best_i is None: break
        selected.append((best_i, cand_items[best_i][0]))
        sel_arrs.append(cand_items[best_i][1])
        flag = ' ⭐' if best_step >= 0.9 else (' ★' if best_step > 0.85 else '')
        print(f"  Step {step+1:2d}  {cand_items[best_i][0][:50]:50s} LOOCV={best_step:.4f}{flag}")
        hist.append(best_step)
        if best_step > best: best = best_step
        if step >= 3 and hist[-1] - hist[-2] < 0.002:
            print(f"           plateau, stop"); break

    print()
    print("=" * 90)
    print(f"  SUMMARY (current production Ridge: LOOCV 0.901, 16 mixed features)")
    print("=" * 90)
    print(f"  A. ALL-LOG 16-feat:  pure power-law, same complexity")
    print(f"  B. 2-phase EMT:      physically grounded, {len(backbone_sets)} sizes tested")
    print(f"  C. Compact greedy:   best {best:.4f} at {len(selected)} log-features")
    print()
    print("  Target: multiplicative + ≤8 params + LOOCV ≥ 0.85 (ideally 0.90)")


if __name__ == '__main__':
    main()
