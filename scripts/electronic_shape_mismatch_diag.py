#!/usr/bin/env python3
"""σ_electronic Stage 21 — within-panel SHAPE mismatch diagnostic.

User feedback (2026-06-01): "다른것들도 안맞는거 같은데"  →  several within-panel
shape inversions / trend mismatches are NOT captured by aggregate LOOCV:
  • 8mAh_real_1.5µm trio (data ASCEND, form DESCEND — full inversion)
  • 1mAh_80:20 hump (form peak where data dips)
  • 1mAh_100_80:20 4-point cluster (form flat, data spikes)
  • 2mAh × 10:0 endpoints (over-pred)
  • 6mAh_real_1.5µm non-EXCL (consistent +5~10% over)

This script:
  1. Print Stage 21 LOOCV / R² / coefs (exact numbers)
  2. Identify each suspect cluster, dump σ_act / σ_form / per-case features
  3. For each cluster, compute residual gradient (which feature varies +/−
     correlating with the data trend that form gets wrong)
  4. Test 5 SHAPE-targeted candidate terms via LOOCV+5-fold:
       S1  log(am_am_n_contacts)      (Holm count, not area — Tabor)
       S2  log(am_se_cn)              (AM-SE contact count - hidden TPB)
       S3  log(coverage_AM_S)         (vs current coverage_AM_P only)
       S4  log(contact_pressure_mean) (pressure → Hertz area amplification)
       S5  log(am_am_mean_force)      (force per contact, not area sum)
       S6  log(bulk_resistance_fraction)  (top Spearman ρ=+0.22)
       S7  φ_se × log(r_SE)           (SE-side packing × size coupling)
  5. PER-CLUSTER candidate: which term flips the shape for the inversion case?
  6. Verdict: STRONG term that fixes shape AND passes LOOCV

Run on WSL:
    python3 scripts/electronic_shape_mismatch_diag.py 2>&1 | tee /tmp/e_shape.log
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np
from numpy.linalg import lstsq

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))


def loo_r2(X_, y_):
    n_ = len(y_)
    if n_ < X_.shape[1] + 2: return float('nan')
    ss = float(np.sum((y_ - y_.mean())**2))
    if ss <= 0: return 0.0
    sse = 0.0
    for j in range(n_):
        m = np.ones(n_, bool); m[j] = False
        c, *_ = lstsq(X_[m], y_[m], rcond=None)
        sse += (y_[j] - X_[j] @ c)**2
    return 1 - sse/ss


def kfold_r2(X_, y_, k=5, seed=0):
    n_ = len(y_)
    if n_ < k*2: return float('nan')
    rng = np.random.default_rng(seed)
    idx = rng.permutation(n_)
    folds = np.array_split(idx, k)
    ss = float(np.sum((y_ - y_.mean())**2))
    sse = 0.0
    for fi in range(k):
        test = folds[fi]
        train = np.array([i for j, ff in enumerate(folds) if j != fi for i in ff])
        c, *_ = lstsq(X_[train], y_[train], rcond=None)
        sse += float(np.sum((y_[test] - X_[test] @ c)**2))
    return 1 - sse/ss


def main():
    import matplotlib; matplotlib.use('Agg')
    import generate_comparison_plots as gcp
    from scipy.stats import spearmanr

    # ───── Walk corpus ─────
    data_list, names = [], []
    seen = set()
    for base in ('webapp/archive', 'webapp/results'):
        bp = Path(base)
        if not bp.is_dir(): continue
        for mp in bp.rglob('full_metrics.json'):
            meta_p = mp.parent / 'meta.json'
            cid = mp.parent.name; nm = cid
            if meta_p.exists():
                try:
                    mn = json.load(open(meta_p)).get('name', '') or ''
                    if mn: nm = mn
                except Exception: pass
            if nm == cid and not nm.startswith('input_'): continue
            if nm in seen: continue
            seen.add(nm)
            try: d = json.load(open(mp))
            except Exception: continue
            data_list.append(d); names.append(nm)

    arr = gcp._electronic_form_arrays(data_list, names)
    if arr is None: print("[ABORT] corpus too small"); return
    fit_mask = ~arr['excluded']
    fit = gcp._electronic_fit(arr, fit_mask=fit_mask)
    coef = fit['coef']
    sig_act = arr['sig_act']; sig_pred = np.exp(fit['pred_log'])
    err_pct = (sig_pred - sig_act) / sig_act * 100.0
    resid_log = arr['logsf'] - fit['pred_log']
    n = arr['n']; nfit = fit['n_fit']; nms = arr['names']

    print("=" * 110)
    print(f" Stage 21 BASELINE (post 4-EXCL + β_fpth + β_logrSE)")
    print("=" * 110)
    print(f"  n={n}  n_fit={nfit}  R²={fit['r2']:.4f}  LOOCV={fit['loocv']:.4f}")
    print(f"  σ_S={float(np.exp(coef[0])):.3f}  σ_P={float(np.exp(coef[1])):.3f}  "
          f"β_T={coef[2]:+.3f}  β_v={coef[3]:+.3f}")
    print(f"  β_AC={coef[7]:+.3f}  β_φth={coef[8]:+.3f}  β_covth={coef[9]:+.3f}")
    print(f"  β_bi={coef[10]:+.3f}  β_Fe={coef[11]:+.3f}")
    print(f"  β_fpth={coef[12]:+.3f}  β_logrSE={coef[13]:+.3f}  ← Stage 21 new")
    print()

    # ───── Helper: dump a cluster's per-case features ─────
    feat_keys = ['phi_am', 'phi_se', 'am_am_cn', 'am_am_mean_area',
                 'am_am_mean_force', 'am_am_n_contacts', 'am_se_cn',
                 'coverage_AM_mean', 'coverage_AM_S_mean', 'coverage_AM_P_mean',
                 'thickness_um', 'r_SE_mean', 'r_AM_S_mean', 'r_AM_P_mean',
                 'AM_S_vulnerable_pct', 'AM_P_vulnerable_pct',
                 'bulk_resistance_fraction', 'contact_pressure_mean',
                 'stress_cv', 'tortuosity_electronic_recommended',
                 'frac_intact_force_pct',
                 'f_perc_x_AM', 'f_perc_recommended']

    def dump_cluster(label, mask):
        idxs = np.where(mask)[0]
        if len(idxs) == 0:
            print(f"  [{label}] EMPTY")
            return
        print(f"  [{label}]  n={len(idxs)}")
        print(f"  {'name':35s}  {'σ_act':>7s}  {'σ_form':>7s}  {'err%':>7s}  {'EXCL':>5s}")
        for i in idxs:
            ex = "EXCL" if arr['excluded'][i] else ""
            print(f"  {nms[i][:35]:35s}  {sig_act[i]:>7.2f}  {sig_pred[i]:>7.2f}  "
                  f"{err_pct[i]:>+6.1f}%  {ex:>5s}")
        # Feature table
        print()
        hdr = f"  {'name':35s}"
        for fk in feat_keys: hdr += f"  {fk[:14]:>14s}"
        print(hdr)
        for i in idxs:
            di = data_list[arr['keep_idx'][i]]
            row = f"  {nms[i][:35]:35s}"
            for fk in feat_keys:
                v = di.get(fk)
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    row += f"  {v:>14.3f}"
                else:
                    row += f"  {'—':>14s}"
            print(row)
        # Per-feature trend correlation within cluster
        print()
        print(f"  → Within-cluster Spearman: feature vs σ_act, feature vs resid_log")
        print(f"    (★ feature where σ_act trend and form trend disagree)")
        if len(idxs) >= 3:
            sa = sig_act[idxs]; rl = resid_log[idxs]
            for fk in feat_keys:
                vals = []
                for i in idxs:
                    v = data_list[arr['keep_idx'][i]].get(fk)
                    vals.append(float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else np.nan)
                v = np.array(vals)
                m = np.isfinite(v)
                if m.sum() < 3 or len(set(v[m])) < 2: continue
                r_sa, _ = spearmanr(v[m], sa[m])
                r_rl, _ = spearmanr(v[m], rl[m])
                flag = ""
                if not np.isnan(r_sa) and not np.isnan(r_rl):
                    if abs(r_rl) > 0.7: flag = "  ★ STRONG resid corr"
                    elif abs(r_rl) > 0.5: flag = "  ◆ moderate"
                if abs(r_rl) > 0.3 or abs(r_sa) > 0.7:
                    print(f"    {fk:35s}  ρ(σ_act)={r_sa:+.2f}  ρ(resid)={r_rl:+.2f}{flag}")
        print()
        print("─" * 110)

    print("=" * 110)
    print(" SHAPE-mismatch cluster dumps")
    print("=" * 110)

    # Cluster 1: 8mAh_real with r_SE=1.5 (the ASCENDING data, DESCENDING form trio)
    mask = np.array([
        ('8mAh_real' in nm)
        and (data_list[arr['keep_idx'][i]].get('r_SE_mean', 0) >= 1.0)
        for i, nm in enumerate(nms)
    ])
    dump_cluster("8mAh_real × r_SE≥1.0 (ASCENDING data vs DESCENDING form)", mask)

    # Cluster 2: 1mAh_80:20 group
    mask = np.array([('1mAh' in nm and '80' in nm and '20' in nm) for nm in nms])
    dump_cluster("1mAh_80:20 (hump shape)", mask)

    # Cluster 3: 1mAh_100 (4-point cluster, mostly _80:20 variants)
    mask = np.array([('1mAh_100' in nm) for nm in nms])
    dump_cluster("1mAh_100 family (within-group spikes)", mask)

    # Cluster 4: 2mAh family
    mask = np.array([('2mAh' in nm) for nm in nms])
    dump_cluster("2mAh family (P-end endpoint misses)", mask)

    # Cluster 5: 6mAh_real with r_SE=1.5
    mask = np.array([
        ('6mAh_real' in nm)
        and (data_list[arr['keep_idx'][i]].get('r_SE_mean', 0) >= 1.0)
        for i, nm in enumerate(nms)
    ])
    dump_cluster("6mAh_real × r_SE≥1.0 (consistent +5~10% over)", mask)

    # ───── Candidate term tests ─────
    print("=" * 110)
    print(" SHAPE-targeted candidate term LOOCV+5-fold test")
    print("=" * 110)
    X = arr['X']; y_resid_full = arr['y_resid']
    Xf = X[fit_mask]; yf = y_resid_full[fit_mask]
    base_loo = loo_r2(Xf, yf); base_kf = kfold_r2(Xf, yf, k=5, seed=0)
    print(f"  BASE (Stage 21)         LOOCV={base_loo:.4f}  5-fold={base_kf:.4f}")
    print()

    # Build candidate features (per-case)
    def pull(key, default=1.0):
        out = []
        for i in range(n):
            v = data_list[arr['keep_idx'][i]].get(key)
            out.append(float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0 else default)
        return np.array(out)

    cands = {
        'S1  log(am_am_n_contacts)        (Holm count vs area)': np.log(np.maximum(pull('am_am_n_contacts'), 1.0)),
        'S2  log(am_se_cn)                (AM-SE TPB count)':    np.log(np.maximum(pull('am_se_cn', 0.1), 0.01)),
        'S3  log(coverage_AM_S)           (S-side coverage)':    np.log(np.maximum(pull('coverage_AM_S_mean', 0.01), 0.01)),
        'S4  log(contact_pressure_mean)   (pressure→Hertz)':     np.log(np.maximum(pull('contact_pressure_mean'), 1e-3)),
        'S5  log(am_am_mean_force)        (force/contact)':      np.log(np.maximum(pull('am_am_mean_force', 1e-6), 1e-9)),
        'S6  log(bulk_resistance_fraction)(top Spearman 0.22)':  np.log(np.maximum(pull('bulk_resistance_fraction', 0.01), 0.001)),
        'S7  φ_se · log r_SE              (SE pack×size)':       pull('phi_se', 0.3) * np.log(np.maximum(pull('r_SE_mean'), 0.05)),
        'S8  log(1 - AM_S_vuln)           (S-side intact)':      np.log(np.maximum(1.0 - pull('AM_S_vulnerable_pct', 0)/100, 0.05)),
        'S9  log(stress_cv)               (heterogeneity)':      np.log(np.maximum(pull('stress_cv', 0.1), 0.01)),
        'S10 r_SE/r_AM_eff ratio          (size disparity)':     pull('r_SE_mean') / np.maximum(arr['r_eff'], 0.1),
    }

    results = []
    for label, new_col in cands.items():
        if not np.all(np.isfinite(new_col)):
            print(f"  {label}  → SKIP (non-finite)"); continue
        X_aug = np.column_stack([X, new_col])
        Xf_aug = X_aug[fit_mask]
        c_aug, *_ = lstsq(Xf_aug, yf, rcond=None)
        beta = float(c_aug[-1])
        loo = loo_r2(Xf_aug, yf); kf = kfold_r2(Xf_aug, yf, k=5, seed=0)
        d_loo = loo - base_loo; d_kf = kf - base_kf
        flag = ""
        if d_loo > 0.015 and d_kf > 0.010: flag = "  ★ STRONG"
        elif d_loo > 0.005 and d_kf > 0.003: flag = "  ◆ moderate"
        elif d_loo < -0.005: flag = "  ✗ degrades"
        print(f"  {label:60s}")
        print(f"     β={beta:+.4f}  LOOCV={loo:.4f} (Δ{d_loo:+.4f})  "
              f"5-fold={kf:.4f} (Δ{d_kf:+.4f}){flag}")
        results.append((label, beta, loo, kf, d_loo, d_kf, new_col))
    print()

    # ───── For each suspect cluster: does any candidate flip the shape? ─────
    print("=" * 110)
    print(" PER-CLUSTER: which candidate REDUCES |err| on the inversion case?")
    print("=" * 110)
    clusters = [
        ('8mAh_real × r_SE≥1.0', np.array([
            ('8mAh_real' in nm)
            and (data_list[arr['keep_idx'][i]].get('r_SE_mean', 0) >= 1.0)
            for i, nm in enumerate(nms)
        ])),
        ('1mAh_100', np.array([('1mAh_100' in nm) for nm in nms])),
        ('2mAh', np.array([('2mAh' in nm) for nm in nms])),
        ('6mAh_real × r_SE≥1.0', np.array([
            ('6mAh_real' in nm)
            and (data_list[arr['keep_idx'][i]].get('r_SE_mean', 0) >= 1.0)
            for i, nm in enumerate(nms)
        ])),
    ]
    for clab, cmask in clusters:
        clean = cmask & fit_mask
        if clean.sum() == 0:
            print(f"  [{clab}] no fit cases"); continue
        base_mae = float(np.mean(np.abs(err_pct[clean])))
        print(f"  [{clab}]  n={int(clean.sum())}  BASE MAE%={base_mae:.1f}")
        for label, beta, loo, kf, d_loo, d_kf, new_col in results:
            X_aug = np.column_stack([X, new_col])
            Xf_aug = X_aug[fit_mask]
            c_aug, *_ = lstsq(Xf_aug, yf, rcond=None)
            pred_log = X_aug @ c_aug + arr['log_offset']
            new_pred = np.exp(pred_log)
            new_err = (new_pred - sig_act) / sig_act * 100.0
            new_mae = float(np.mean(np.abs(new_err[clean])))
            d_mae = new_mae - base_mae
            mark = ""
            if d_mae < -3: mark = "  ★ shape-fix"
            elif d_mae < -1: mark = "  ◆ improves"
            elif d_mae > +3: mark = "  ✗ makes worse"
            print(f"    {label[:30]:30s}  MAE%={new_mae:>5.1f} (Δ{d_mae:+.1f}){mark}")
        print()

    print("=" * 110)
    print(" VERDICT")
    print("=" * 110)
    strong_global = [r for r in results if r[4] > 0.015 and r[5] > 0.010]
    if strong_global:
        print(f"  {len(strong_global)} STRONG global candidate(s):")
        for r in strong_global:
            print(f"    {r[0]}  Δ_loo={r[4]:+.4f}  Δ_5fold={r[5]:+.4f}")
        print("  → Stage 22 candidate. Verify it ALSO fixes cluster shape above.")
    else:
        print("  No STRONG global term → shape inversions are LOCAL physics")
        print("  not captured by any single feature.  Path: per-regime form")
        print("  OR multi-seed data at suspect cluster designs.")


if __name__ == '__main__':
    main()
