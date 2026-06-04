#!/usr/bin/env python3
"""σ_thermal Stage T1 form refinement on FINALIZED corpus (n=82).

Lock the finalization corpus: input_ cases with Physics Stage E κ in
[0.05, 50], minus σ_e EXCL, AS OF the n=82 finalize point.  To make this
reproducible regardless of later uploads, we reconstruct the exact 82 by
excluding the 8 post-finalize backfill additions.

Then refine the 16-feature Ridge:
  1. Backward elimination (drop weak, keep LOOCV ≥ 0.895)
  2. Forward re-selection from scratch (find true minimal)
  3. Mixed: lock physics-meaningful core, prune the rest
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

# 8 post-finalize backfill additions (entered after n=82 was locked).
# These are valid cases but excluded to reproduce the finalization corpus.
POST_FINALIZE = {
    'input_2mAh_real_6', 'input_2mAh_real_9', 'input_2mAh_real_11',
    'input_8mAh_real_6', 'input_8mAh_real_11',
    'input_1mAh_8_AMS_S1', 'input_1mAh_8_AMS_S2', 'input_1mAh_8_AMS_S3',
    'input_1mAh_8_AMS_S5',
}


def load(lock_finalize=True):
    cases = []; seen = set()
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
            if lock_finalize and nm in POST_FINALIZE: continue
            d['_name'] = nm; d['_kappa'] = float(kappa)
            cases.append(d)
    return cases


def _get_nested(d, key):
    if '.' not in key: return d.get(key)
    v = d
    for p in key.split('.'):
        if isinstance(v, dict): v = v.get(p)
        else: return None
    return v


def feat_arr(cases, key):
    out = []
    for c in cases:
        v = _get_nested(c, key)
        out.append(float(v) if isinstance(v, (int, float)) and np.isfinite(v) else np.nan)
    a = np.array(out)
    if np.any(~np.isfinite(a)):
        med = np.nanmedian(a)
        a = np.where(np.isfinite(a), a, med)
    return a


def fit_loocv(X, y, alpha=0.05):
    n = X.shape[1]
    X_ = np.column_stack([np.ones(len(y)), X])
    I = np.eye(n+1); I[0,0] = 0
    try: coef = solve(X_.T@X_ + alpha*I, X_.T@y)
    except: return None
    pred = X_@coef
    ss = float(np.sum((y-y.mean())**2))
    r2 = 1 - float(np.sum((y-pred)**2))/ss if ss>0 else 0
    sse = 0.0
    for j in range(len(y)):
        m = np.ones(len(y), bool); m[j]=False
        Xm = X_[m]
        try:
            cm = solve(Xm.T@Xm + alpha*I, Xm.T@y[m])
            sse += (y[j]-X_[j]@cm)**2
        except: pass
    return r2, (1-sse/ss if ss>0 else 0), coef


def build_X(cases, feat_list):
    cols = []
    for fk, do_log in feat_list:
        v = feat_arr(cases, fk)
        if do_log:
            v = np.where(v>0, v, np.nanmin(v[v>0]) if np.any(v>0) else 1e-6)
            cols.append(np.log(v))
        else:
            cols.append(v)
    return np.column_stack(cols)


def main():
    cases = load(lock_finalize=True)
    n = len(cases)
    print(f"\nFinalized corpus (n=82 target): {n}")
    y = np.log(np.array([c['_kappa'] for c in cases]))

    feats16 = [(f[0], f[1]) for f in gcp._THERMAL_T1_FEATURES]
    X = build_X(cases, feats16)
    base = fit_loocv(X, y)
    print(f"Full 16-feature: LOOCV={base[1]:.4f}  R²={base[0]:.4f}  n/k={n/17:.1f}\n")

    # ─── 1. Backward elimination (keep LOOCV ≥ baseline − 0.005) ───
    print("="*90)
    print("  1. Backward elimination (stop when LOOCV drops >0.005 below full)")
    print("="*90)
    keep = list(feats16); hist = []
    while len(keep) > 3:
        best_i, best_loo = None, -np.inf
        for i in range(len(keep)):
            sub = keep[:i]+keep[i+1:]
            r = fit_loocv(build_X(cases, sub), y)
            if r and r[1] > best_loo: best_loo = r[1]; best_i = i
        if best_i is None: break
        if best_loo < base[1] - 0.005:
            print(f"  STOP — dropping any more loses >0.005 (next would be {best_loo:.4f})")
            break
        dn = keep[best_i][0]; keep.pop(best_i)
        flag = ' ⭐' if best_loo >= 0.9 else ''
        print(f"  drop {dn[:42]:42s} → {len(keep):2d} feat  LOOCV={best_loo:.4f}{flag}")
        hist.append((len(keep), best_loo))
    print(f"\n  → Minimal-without-loss: {len(keep)} features, LOOCV={fit_loocv(build_X(cases,keep),y)[1]:.4f}")
    print(f"     kept: {[k[0] for k in keep]}\n")

    # ─── 2. Forward selection from scratch ───
    print("="*90)
    print("  2. Forward selection (greedy from scratch, all 16)")
    print("="*90)
    remaining = list(feats16); selected = []
    for step in range(16):
        best_i, best_loo = None, -np.inf
        for i, f in enumerate(remaining):
            r = fit_loocv(build_X(cases, selected+[f]), y)
            if r and r[1] > best_loo: best_loo = r[1]; best_i = i
        if best_i is None: break
        selected.append(remaining.pop(best_i))
        flag = ' ⭐' if best_loo >= 0.9 else ''
        mark = ''
        if len(selected) >= 2:
            prev = fit_loocv(build_X(cases, selected[:-1]), y)[1]
            if best_loo - prev < 0.003: mark = '  (plateau)'
        print(f"  +{selected[-1][0][:40]:40s} ({len(selected):2d}) LOOCV={best_loo:.4f}{flag}{mark}")
    print()

    # ─── 3. Physics-core lock + prune ───
    print("="*90)
    print("  3. Physics-core + structural prune")
    print("="*90)
    # Core: the 5 features that hurt most when dropped (porosity, se_se_cn,
    # bruggeman_fallback, gb_density, R_brug) + try adding back others
    CORE = [
        ('porosity', False), ('se_se_cn', True),
        ('validation_flags.bruggeman_fallback_fired_any', False),
        ('gb_density_mean', True), ('R_brug_over_full_physics', False),
    ]
    rc = fit_loocv(build_X(cases, CORE), y)
    print(f"  Physics core (5): LOOCV={rc[1]:.4f}  R²={rc[0]:.4f}")
    # Add remaining one at a time
    rest = [f for f in feats16 if f[0] not in [c[0] for c in CORE]]
    cur = list(CORE)
    for step in range(len(rest)):
        best_i, best_loo = None, -np.inf
        for i, f in enumerate(rest):
            if f in cur: continue
            r = fit_loocv(build_X(cases, cur+[f]), y)
            if r and r[1] > best_loo: best_loo = r[1]; best_i = i
        if best_i is None: break
        cur.append(rest[best_i])
        flag = ' ⭐' if best_loo >= 0.9 else ''
        print(f"  +{rest[best_i][0][:40]:40s} ({len(cur):2d}) LOOCV={best_loo:.4f}{flag}")
        if len(cur) >= 12: break
    print()

    print("="*90)
    print("  SUMMARY")
    print("="*90)
    print(f"  Full 16:        LOOCV {base[1]:.4f}  (current production)")
    print(f"  Backward-min:   {len(keep)} feat")
    print(f"  Goal: fewest features keeping LOOCV ≥ 0.895 (≈ finalized 0.90)")


if __name__ == '__main__':
    main()
