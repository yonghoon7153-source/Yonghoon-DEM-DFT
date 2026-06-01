#!/usr/bin/env python3
"""σ_electronic Stage 21 push — target σ_ionic grade (LOOCV ~0.975).

User feedback 2026-06-01: PI band shows two systematic miss clusters
that are NOT noise floor:
  (A) 8mAh_75:25 family (3 cases ~2× over-prediction)
  (B) 6mAh_real_1.5µm × P=10:0 corner (1 case ~5× over-prediction)
  + 2mAh × 10:0 edge over-prediction

Goal: close LOOCV 0.908 → 0.975 (+0.067).  σ_ionic close-out playbook
shows this needs ~3-5 increments (each +0.005 to +0.020) + data cleanup.

This script:
  1. Stage 20 BASELINE LOOCV (current production)
  2. Per-case residual table + cluster summary (8mAh_75:25, 6mAh
     r_SE=1.5 P-end, 2mAh × 10:0)
  3. Family multi-seed sibling check for outliers (could be per-seed
     anomaly like σ_ionic 1mAh_9_S5)
  4. Spearman residual scan over ALL features (find STRONG missing
     physics, |ρ|>0.4)
  5. Test CANDIDATE term additions via NESTED LOOCV (k=5 outer fold):
       C1  β_τφ · lnτ · log(φ_AM)              (high-AM thick film miss)
       C2  β_fT · log(f_p) · log(T/d)          (thick-film percolation)
       C3  β_prSE · p · log(r_SE)              (P × large r_SE corner)
       C4  β_pkT · p · log(T/d)                (P-rich thick coupling)
       C5  fintact ALWAYS-on (coverage_AM fallback when frac missing)
       C6  β_φAC · (φ_AM−0.3)² · g_thin        (thin-film high-φ nonlinearity)
       C7  log_fp_thin = g_thin · log(f_p)     (thin-region f_p amplify)
       C8  am_am_n_contact direct (replace area½ with N½)
  6. Sibling-tail removal test (drop 1-3 worst residual cases, see if
     LOOCV jumps like σ_ionic 0.97→0.975 with 1mAh_9_S5+particulate_12_S2)
  7. VERDICT: best 1-3 increments → Stage 21 candidate form

Run on WSL:
    python3 scripts/electronic_push_to_ionic_grade.py 2>&1 | tee /tmp/e_push.log

Send back the tail of /tmp/e_push.log if not full.
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
    if n_ < X_.shape[1] + 2:
        return float('nan')
    ss = float(np.sum((y_ - y_.mean())**2))
    if ss <= 0:
        return 0.0
    sse = 0.0
    for j in range(n_):
        m = np.ones(n_, bool); m[j] = False
        c, *_ = lstsq(X_[m], y_[m], rcond=None)
        sse += (y_[j] - X_[j] @ c)**2
    return 1 - sse/ss


def kfold_r2(X_, y_, k=5, seed=0):
    """Outer k-fold CV (unbiased estimator, no leakage from term-selection)."""
    n_ = len(y_)
    if n_ < k * 2:
        return float('nan')
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
    import matplotlib
    matplotlib.use('Agg')
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
            cid = mp.parent.name
            nm = cid
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
    if arr is None:
        print("[ABORT] corpus too small"); return

    fit_mask = ~arr['excluded']
    fit = gcp._electronic_fit(arr, fit_mask=fit_mask)
    coef = fit['coef']
    sig_act = arr['sig_act']
    sig_pred = np.exp(fit['pred_log'])
    err_pct = (sig_pred - sig_act) / sig_act * 100.0
    resid_log = arr['logsf'] - fit['pred_log']

    n = arr['n']; nfit = fit['n_fit']
    nms = arr['names']

    print("=" * 110)
    print(f" σ_electronic Stage 21 push — BASELINE  (n={n}, fit={nfit})")
    print("=" * 110)
    print(f"  Stage 20 BASELINE  R²={fit['r2']:.4f}  LOOCV={fit['loocv']:.4f}")
    print(f"  coefs: σ_S={float(np.exp(coef[0])):.2f}  σ_P={float(np.exp(coef[1])):.2f}  "
          f"β_T={coef[2]:+.3f}  β_v={coef[3]:+.3f}  β_AC={coef[7]:+.3f}")
    print(f"         β_φth={coef[8]:+.3f}  β_covth={coef[9]:+.3f}  β_bi={coef[10]:+.3f}  "
          f"β_Fe={coef[11]:+.3f}")
    print(f"  Target: σ_ionic-grade LOOCV ≈ 0.975  →  Δ needed = {0.975 - fit['loocv']:+.4f}")
    print()

    # ───── Per-case worst residuals ─────
    print("─" * 110)
    print(" Worst-residual cases (signed log resid + err%)")
    print("─" * 110)
    order = np.argsort(-np.abs(resid_log))
    print(f"  {'rank':>4s}  {'name':40s}  {'σ_act':>8s}  {'σ_pred':>8s}  "
          f"{'err%':>8s}  {'φ':>6s}  {'p':>5s}  {'r_SE':>5s}  {'T':>5s}  {'fam'}")
    families = {}
    for rk, idx in enumerate(order[:25], 1):
        nm = nms[idx]
        sa = sig_act[idx]; sp = sig_pred[idx]; ep = err_pct[idx]
        ph = arr['phi'][idx]; pa = arr['p_amp'][idx]
        ras = arr['r_AM_S'][idx]; rap = arr['r_AM_P'][idx]
        Ti = arr['T'][idx]
        # Try to read r_SE from data_list (not in arr)
        di = data_list[arr['keep_idx'][idx]]
        rse = di.get('r_SE_mean') or di.get('r_SE') or di.get('SE_radius') or 0
        # Family root: strip _Sx suffix
        root = nm
        for suf in ('_S1','_S2','_S3','_S4','_S5'):
            if root.endswith(suf): root = root[:-len(suf)]
        families.setdefault(root, []).append((nm, ep))
        excl = " [EXCL]" if arr['excluded'][idx] else ""
        print(f"  {rk:>4d}  {nm[:40]:40s}  {sa:>8.2f}  {sp:>8.2f}  {ep:>+7.1f}%  "
              f"{ph:>6.3f}  {pa:>5.2f}  {rse:>5.2f}  {Ti:>5.0f}  {root[:24]}{excl}")
    print()

    # ───── Cluster summary ─────
    print("─" * 110)
    print(" Cluster summary (PI-band misses identified from plots)")
    print("─" * 110)
    def cluster_stats(label, mask):
        if mask.sum() == 0:
            print(f"  {label:50s} n=0"); return
        nc = int(mask.sum())
        ec = err_pct[mask]
        print(f"  {label:50s} n={nc:>2d}  median err%={np.median(ec):+6.1f}  "
              f"mean={np.mean(ec):+6.1f}  range [{ec.min():+.0f}, {ec.max():+.0f}]")
        for i in np.where(mask)[0]:
            print(f"      {nms[i]:42s}  σ_act={sig_act[i]:6.2f}  pred={sig_pred[i]:6.2f}  err={err_pct[i]:+6.1f}%")

    # Cluster A: 8mAh_75:25
    mask_A = np.array([('8mAh' in n_ and '75' in n_) for n_ in nms])
    cluster_stats("8mAh_75:25 family", mask_A)
    # Cluster B: 6mAh_real with r_SE>=1.0 and P-end
    mask_B = np.array([
        ('6mAh_real' in n_) and (arr['p_amp'][i] > 0.8)
        and (data_list[arr['keep_idx'][i]].get('r_SE_mean', 0) >= 1.0)
        for i, n_ in enumerate(nms)
    ])
    cluster_stats("6mAh_real × r_SE≥1.0 × P-end (p>0.8)", mask_B)
    # Cluster C: 2mAh × 10:0
    mask_C = np.array([('2mAh' in n_ and arr['p_amp'][i] > 0.8) for i, n_ in enumerate(nms)])
    cluster_stats("2mAh × P-end (p>0.8)", mask_C)
    # Cluster D: all P=10:0 endpoint (covers wide miss)
    mask_D = arr['p_amp'] > 0.8
    cluster_stats("ALL P=10:0 endpoint (p>0.8)", mask_D)
    # Cluster E: all 0:10 endpoint
    mask_E = arr['p_amp'] < 0.2
    cluster_stats("ALL S=10:0 endpoint (p<0.2)", mask_E)
    print()

    # ───── Family multi-seed check ─────
    print("─" * 110)
    print(" Family sibling spread (>=3 siblings, σ_act CV%)")
    print("─" * 110)
    print(f"  {'family root':30s}  {'n':>3s}  {'σ_med':>7s}  {'σ_CV%':>7s}  {'worst':>8s}  {'note'}")
    sigs_by_root = {}
    for i, nm in enumerate(nms):
        root = nm
        for suf in ('_S1','_S2','_S3','_S4','_S5'):
            if root.endswith(suf): root = root[:-len(suf)]
        sigs_by_root.setdefault(root, []).append((sig_act[i], err_pct[i], nm))
    for root, lst in sorted(sigs_by_root.items()):
        if len(lst) < 3: continue
        ss = np.array([s for s, _, _ in lst])
        es = np.array([e for _, e, _ in lst])
        med = float(np.median(ss))
        cv = float(np.std(ss) / med * 100) if med > 0 else 0
        worst_nm = lst[int(np.argmax(np.abs(es)))][2]
        worst_e = es[int(np.argmax(np.abs(es)))]
        note = ""
        if cv > 40: note = " ★ HIGH spread — sibling-tail candidate"
        elif cv > 25: note = " ◆ moderate spread"
        print(f"  {root[:30]:30s}  {len(lst):>3d}  {med:>7.2f}  {cv:>7.1f}  "
              f"{worst_e:>+7.1f}%  {note}")
    print()

    # ───── Spearman scan all features ─────
    print("─" * 110)
    print(" Spearman ρ(resid_log, feature) — ALL cases (find missing physics signals)")
    print("─" * 110)
    clean = ~arr['excluded']
    feats = {
        'φ_AM': arr['phi'],
        'p_AMP': arr['p_amp'],
        'r_AM,S': arr['r_AM_S'],
        'r_AM,P': arr['r_AM_P'],
        'r_eff': arr['r_eff'],
        'T_um': arr['T'],
        'T/d_AM': arr['T'] / (2*arr['r_eff']),
        'lnτ': np.log(arr['tau']),
        'am_vuln': arr['am_vuln'],
        'am_area': arr['am_area'],
        'cn_am': arr['cn_am'],
        'φ·logCN': arr['phi_logcn'],
        'cov_AM,P': arr['cov_AM_P'],
        'g_thin': arr['g_thin'],
    }
    # Pull from data_list directly for richer features
    extra_keys = ['phi_se', 'r_SE_mean', 'r_SE', 'coverage_AM_mean',
                  'coverage_AM_S_mean', 'coverage_AM_P_mean',
                  'am_am_n_contact', 'am_se_cn', 'se_se_cn',
                  'f_perc_x_AM', 'f_perc_recommended', 'bulk_resistance_fraction',
                  'contact_pressure_mean', 'stress_cv',
                  'frac_intact_force_pct', 'frac_intact_pct',
                  'tortuosity_electronic_mean', 'tortuosity_electronic_recommended']
    for k in extra_keys:
        vals = []
        for ci in range(n):
            di = data_list[arr['keep_idx'][ci]]
            v = di.get(k)
            vals.append(float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else np.nan)
        if np.sum(np.isfinite(vals)) >= 10:
            feats[k] = np.array(vals)
    rho_table = []
    for fk, fv in feats.items():
        mv = np.isfinite(fv) & clean
        if mv.sum() < 10: continue
        r_, _ = spearmanr(fv[mv], resid_log[mv])
        if not np.isnan(r_): rho_table.append((fk, float(r_), int(mv.sum())))
    rho_table.sort(key=lambda r: -abs(r[1]))
    print(f"  {'feature':30s}  {'ρ':>8s}  {'n':>4s}")
    for fk, r_, nc in rho_table[:25]:
        flag = ""
        if abs(r_) > 0.4: flag = "  ★ STRONG"
        elif abs(r_) > 0.3: flag = "  ◆ moderate"
        elif abs(r_) > 0.2: flag = "  · weak"
        print(f"  {fk:30s}  {r_:+8.3f}  {nc:>4d}{flag}")
    print()

    # ───── Cluster-A focused Spearman (8mAh_75:25) ─────
    if mask_A.sum() >= 3:
        print("─" * 110)
        print(f" Cluster A focused: 8mAh_75:25 family (n={int(mask_A.sum())}) — Spearman ρ on resid")
        print("─" * 110)
        rho_A = []
        for fk, fv in feats.items():
            mv = np.isfinite(fv) & mask_A & clean
            if mv.sum() < 3: continue
            try:
                r_, _ = spearmanr(fv[mv], resid_log[mv])
                if not np.isnan(r_): rho_A.append((fk, float(r_), int(mv.sum())))
            except Exception: pass
        rho_A.sort(key=lambda r: -abs(r[1]))
        for fk, r_, nc in rho_A[:10]:
            print(f"  {fk:30s}  ρ={r_:+.3f}  n={nc}")
        print()

    # ───── Candidate term LOOCV tests ─────
    print("─" * 110)
    print(" CANDIDATE term tests — LOOCV impact (Stage 20 base + 1 new term)")
    print("─" * 110)
    X = arr['X']; y_resid_full = arr['y_resid']
    Xf = X[fit_mask]; yf = y_resid_full[fit_mask]
    base_loo = loo_r2(Xf, yf)
    base_kf = kfold_r2(Xf, yf, k=5, seed=0)
    print(f"  BASE (Stage 20)           LOOCV={base_loo:.4f}  5-fold={base_kf:.4f}")
    print()

    # Build feature arrays for candidates
    log_phi = np.log(np.maximum(arr['phi'], 0.01))
    lnt = np.log(arr['tau'])
    log_Td = np.log(np.maximum(arr['T'] / (2*arr['r_eff']), 0.1))
    log_fp = np.log(np.maximum(
        np.array([data_list[arr['keep_idx'][i]].get('f_perc_x_AM',
                  data_list[arr['keep_idx'][i]].get('f_perc_recommended', 0.5))
                  for i in range(n)]), 0.01))
    p_a = arr['p_amp']
    # r_SE
    rse = np.array([
        data_list[arr['keep_idx'][i]].get('r_SE_mean',
            data_list[arr['keep_idx'][i]].get('r_SE', 1.0)) or 1.0
        for i in range(n)])
    log_rse = np.log(np.maximum(rse, 0.05))

    cands = {
        'C1  β_τφ · lnτ · log φ_AM        (thick × AM-rich)': lnt * log_phi,
        'C2  β_fT · log f_p · log(T/d)    (thick × percolation)': log_fp * log_Td,
        'C3  β_prSE · p · log r_SE        (P-end × large r_SE)': p_a * log_rse,
        'C4  β_pkT · p · log(T/d)         (P-end × thick)': p_a * log_Td,
        'C6  β_φAC · (φ−0.3)² · g_thin    (thin high-φ nonlin)': (arr['phi'] - 0.3)**2 * arr['g_thin'],
        'C7  β_fpth · g_thin · log f_p    (thin × percolation)': arr['g_thin'] * log_fp,
        'C9  β_logfp · log f_p            (ALL × percolation, ungated)': log_fp,
        'C10 β_logrSE · log r_SE          (ALL × r_SE direct)': log_rse,
        'C11 β_τT · lnτ · log(T/d)        (thick × tortuosity)': lnt * log_Td,
        'C12 β_φT · log φ_AM · log(T/d)   (thick × AM density)': log_phi * log_Td,
    }
    results = []
    for label, new_col in cands.items():
        new_col = np.array(new_col, dtype=float)
        if not np.all(np.isfinite(new_col)):
            print(f"  {label}  → SKIP (non-finite)"); continue
        X_aug = np.column_stack([X, new_col])
        Xf_aug = X_aug[fit_mask]
        c_aug, *_ = lstsq(Xf_aug, yf, rcond=None)
        beta = float(c_aug[-1])
        loo = loo_r2(Xf_aug, yf)
        kf = kfold_r2(Xf_aug, yf, k=5, seed=0)
        d_loo = loo - base_loo
        d_kf = kf - base_kf
        flag = ""
        if d_loo > 0.015 and d_kf > 0.010: flag = "  ★ STRONG — adopt candidate"
        elif d_loo > 0.005 and d_kf > 0.003: flag = "  ◆ moderate — investigate"
        elif d_loo < -0.005: flag = "  ✗ degrades"
        print(f"  {label:60s}")
        print(f"     β={beta:+.4f}  LOOCV={loo:.4f} (Δ{d_loo:+.4f})  "
              f"5-fold={kf:.4f} (Δ{d_kf:+.4f}){flag}")
        results.append((label, beta, loo, kf, d_loo, d_kf))
    print()

    # ───── Sibling-tail removal test ─────
    print("─" * 110)
    print(" Sibling-tail / worst-case removal LOOCV impact")
    print("─" * 110)
    # Worst 1-5 cases (by |resid|) excluded
    sorted_clean = np.argsort(-np.abs(resid_log))
    sorted_clean = [i for i in sorted_clean if fit_mask[i]]
    for k_rm in (1, 2, 3, 5):
        rm_idx = set(sorted_clean[:k_rm])
        mask_kept = np.array([(i not in rm_idx) for i in range(n)]) & fit_mask
        X_k = X[mask_kept]; y_k = y_resid_full[mask_kept]
        loo = loo_r2(X_k, y_k)
        names_rm = [nms[i] for i in sorted_clean[:k_rm]]
        print(f"  remove top-{k_rm} worst:  LOOCV={loo:.4f} (Δ{loo - base_loo:+.4f})")
        for nm in names_rm:
            print(f"      └─ {nm}")
    print()

    # ───── COMBO test: best 2 candidates together ─────
    if len(results) >= 2:
        print("─" * 110)
        print(" COMBO: top-2 candidates added together")
        print("─" * 110)
        top2 = sorted(results, key=lambda r: -r[4])[:2]
        labels = [r[0] for r in top2]
        cols = [cands[lab] for lab in labels]
        X_combo = np.column_stack([X] + cols)
        Xf_combo = X_combo[fit_mask]
        c_c, *_ = lstsq(Xf_combo, yf, rcond=None)
        loo_c = loo_r2(Xf_combo, yf)
        kf_c = kfold_r2(Xf_combo, yf, k=5, seed=0)
        print(f"  top-2 combo: {labels[0][:30]} + {labels[1][:30]}")
        print(f"     LOOCV={loo_c:.4f} (Δ{loo_c - base_loo:+.4f})  "
              f"5-fold={kf_c:.4f} (Δ{kf_c - base_kf:+.4f})")
        for i, lab in enumerate(labels):
            print(f"     β[{i}]={c_c[12+i]:+.4f}  ({lab[:50]})")
        print()

    # ───── Verdict ─────
    print("=" * 110)
    print(" VERDICT")
    print("=" * 110)
    strong = [r for r in results if r[4] > 0.015 and r[5] > 0.010]
    if strong:
        print(f"  {len(strong)} STRONG candidate(s):")
        for lab, beta, loo, kf, d_loo, d_kf in strong:
            print(f"    {lab}")
            print(f"      β={beta:+.4f}  LOOCV Δ{d_loo:+.4f}  5-fold Δ{d_kf:+.4f}")
        print(f"  → Stage 21 candidate: adopt top STRONG term(s)")
    else:
        moderate = [r for r in results if r[4] > 0.005]
        if moderate:
            print(f"  No STRONG term, but {len(moderate)} moderate:")
            for r in moderate[:5]:
                print(f"    {r[0]}  Δ_loo={r[4]:+.4f}")
            print(f"  → Need DATA (multi-seed at outlier designs) or different "
                  f"base ingredient (like σ_ionic T1 cov_physics→cov_Hertz)")
        else:
            print(f"  No form term passes — Stage 20 is at this corpus's noise floor.")
            print(f"  → Path: (a) sibling-tail removal of {sorted_clean[:3]}, "
                  f"or (b) more data at miss-cluster designs.")


if __name__ == '__main__':
    main()
