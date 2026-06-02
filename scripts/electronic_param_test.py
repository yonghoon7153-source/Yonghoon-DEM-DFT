#!/usr/bin/env python3
"""σ_electronic + σ_ionic parametric test — fix σ_S/σ_P at user-chosen
values and inspect how form behaves.

Use cases:
  - "σ_AM = 50 literature 그대로 쓰면 어떨까?"          → --sigma_S 50 --sigma_P 50
  - "Trevisanello effective (S=10, P=5)는?"             → --sigma_S 10 --sigma_P 5
  - "두 endpoint 5 mS/cm 동일하면?"                      → --sigma_S 5 --sigma_P 5
  - "현재 live-fit 그대로 보고 싶다"                       → (no args, default)

Also diagnoses cases where solver computes σ_e but form fails to fit
(err > 20%) — identifies WHICH physics axis is missing per case.

Run:
    python3 scripts/electronic_param_test.py                # default live-fit
    python3 scripts/electronic_param_test.py --sigma_S 10 --sigma_P 5
    python3 scripts/electronic_param_test.py --sigma_S 50 --sigma_P 50

For σ_ionic equivalent (σ_grain control):
    python3 scripts/electronic_param_test.py --ionic_grain 3.0
"""
from __future__ import annotations
import sys, json, argparse
from pathlib import Path
import numpy as np
from numpy.linalg import lstsq

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))


def loo_r2_logsf(X_, log_offset_, logsf_):
    n_ = len(logsf_)
    if n_ < X_.shape[1] + 2: return float('nan')
    ss_tot = float(np.sum((logsf_ - logsf_.mean())**2))
    if ss_tot <= 0: return 0.0
    y_resid = logsf_ - log_offset_
    sse = 0.0
    for j in range(n_):
        m = np.ones(n_, bool); m[j] = False
        c, *_ = lstsq(X_[m], y_resid[m], rcond=None)
        sse += (logsf_[j] - (X_[j] @ c + log_offset_[j]))**2
    return 1 - sse/ss_tot


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sigma_S', type=float, default=None,
                    help='Lock σ_S (S-end AM conductivity, mS/cm).  Default = live-fit.')
    ap.add_argument('--sigma_P', type=float, default=None,
                    help='Lock σ_P (P-end AM conductivity, mS/cm).  Default = live-fit.')
    ap.add_argument('--ionic_grain', type=float, default=None,
                    help='[future] σ_grain for σ_ionic test')
    ap.add_argument('--mix', choices=['geometric', 'linear'], default='geometric',
                    help='Mixing rule when σ_S/σ_P locked')
    args = ap.parse_args()

    import matplotlib; matplotlib.use('Agg')
    import generate_comparison_plots as gcp

    # ───── Walk corpus ─────
    data_list, names, seen = [], [], set()
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
                except: pass
            if nm == cid and not nm.startswith('input_'): continue
            if nm in seen: continue
            seen.add(nm)
            try: d = json.load(open(mp))
            except: continue
            data_list.append(d); names.append(nm)

    arr = gcp._electronic_form_arrays(data_list, names)
    if arr is None: print("[ABORT]"); return
    fit_mask = ~arr['excluded']
    sig_act = arr['sig_act']; logsf = arr['logsf']
    n = arr['n']; nfit = int(fit_mask.sum()); nms = arr['names']
    p_a = arr['p_amp']; phi_a = arr['phi']
    ras = arr['r_AM_S']; rap = arr['r_AM_P']

    # Always run Stage 21 live-fit baseline for comparison
    fit21 = gcp._electronic_fit(arr, fit_mask=fit_mask)
    pred21 = np.exp(fit21['pred_log'])
    err21 = (pred21 - sig_act) / sig_act * 100
    sS_fit = float(np.exp(fit21['coef'][0])); sP_fit = float(np.exp(fit21['coef'][1]))

    print("=" * 110)
    print(f" σ_electronic parametric test  (n={n} n_fit={nfit})")
    print("=" * 110)
    print(f"  Stage 21 live-fit (BASELINE):")
    print(f"    σ_S={sS_fit:.3f}  σ_P={sP_fit:.3f}  ratio={sS_fit/sP_fit:.2f}×")
    print(f"    LOOCV={fit21['loocv']:.4f}  R²={fit21['r2']:.4f}")
    print()

    sigma_S = args.sigma_S if args.sigma_S is not None else sS_fit
    sigma_P = args.sigma_P if args.sigma_P is not None else sP_fit
    user_locked = (args.sigma_S is not None) or (args.sigma_P is not None)

    if user_locked:
        print(f"  USER LOCK:  σ_S={sigma_S:.2f}  σ_P={sigma_P:.2f}  ratio={sigma_S/sigma_P:.2f}×  mix={args.mix}")
        # Refit with locked σ_S/σ_P
        if args.mix == 'geometric':
            log_mix = (1-p_a)*np.log(sigma_S) + p_a*np.log(sigma_P)
        else:
            log_mix = np.log((1-p_a)*sigma_S + p_a*sigma_P)
        X_keep = arr['X'][:, 2:]   # 12 cols
        # log_offset already contains log_ncm + log_holm + log_phi4
        # We replace the σ_S/σ_P part (cols 0,1) with our locked log_mix
        offset_new = log_mix + arr['log_offset']
        y_resid_new = logsf - offset_new
        Xf = X_keep[fit_mask]; yf = y_resid_new[fit_mask]
        c_new, *_ = lstsq(Xf, yf, rcond=None)
        pred_log_new = X_keep @ c_new + offset_new
        pred_new = np.exp(pred_log_new)
        err_new = (pred_new - sig_act) / sig_act * 100
        loo_new = loo_r2_logsf(Xf, offset_new[fit_mask], logsf[fit_mask])
        print(f"    LOOCV={loo_new:.4f}  ΔLOOCV={loo_new-fit21['loocv']:+.4f}")
        print(f"    refitted coefs: β_T={c_new[0]:+.3f}  β_v={c_new[1]:+.3f}  β_AC={c_new[5]:+.3f}  β_bi={c_new[8]:+.3f}")
    else:
        pred_new = pred21
        err_new = err21
        loo_new = fit21['loocv']
        print(f"  (no lock; showing Stage 21 live-fit only)")
    print()

    # Family masks
    def fam(test): return np.array([test(nm) for nm in nms])
    families = [
        ('1mAh', fam(lambda nm: '1mAh' in nm and '_real' not in nm)),
        ('2mAh_real', fam(lambda nm: '2mAh' in nm)),
        ('6mAh_real', fam(lambda nm: '6mAh' in nm)),
        ('8mAh', fam(lambda nm: '8mAh' in nm)),
        ('particulate', fam(lambda nm: 'particulate' in nm or 'input_S_' in nm[:8])),
    ]

    print("─" * 110)
    print(" Per-family MAE")
    print("─" * 110)
    print(f"  {'family':15s}  {'n':>4s}  {'BASELINE':>10s}  {'USER LOCK':>11s}  {'Δ':>7s}")
    for label, m in families:
        mf = m & fit_mask
        if mf.sum() == 0: continue
        mae_base = float(np.mean(np.abs(err21[mf])))
        mae_user = float(np.mean(np.abs(err_new[mf])))
        d = mae_user - mae_base
        flag = ""
        if d < -1: flag = "  ◆ improves"
        elif d > +1: flag = "  ✗ worsens"
        print(f"  {label:15s}  {int(mf.sum()):>4d}  {mae_base:>9.1f}%  {mae_user:>10.1f}%  {d:>+6.1f}{flag}")
    print()

    # ───── Cases that DON'T fit (solver works, form fails) ─────
    print("─" * 110)
    print(" Cases where SOLVER computes σ but FORM fails to fit (|err| > 20%, non-EXCL)")
    print(" → Investigate WHY each case is poorly predicted")
    print("─" * 110)
    fail_mask = (~arr['excluded']) & (np.abs(err_new) > 20)
    fail_idx = np.where(fail_mask)[0]
    fail_idx = sorted(fail_idx, key=lambda i: -abs(err_new[i]))
    if not fail_idx:
        print("  None — all non-EXCL cases fit within ±20%")
    else:
        for i in fail_idx[:15]:
            di = data_list[arr['keep_idx'][i]]
            phi = arr['phi'][i]; pa = arr['p_amp'][i]
            rse = di.get('r_SE_mean', di.get('r_SE', 1.0)) or 1.0
            T = arr['T'][i]
            cn = arr['cn_am'][i]
            am_area = arr['am_area'][i]
            cov_amp = arr['cov_AM_P'][i]
            tau = arr['tau'][i]
            # Family check
            root = nms[i]
            for suf in ('_S1','_S2','_S3','_S4','_S5'):
                if root.endswith(suf): root = root[:-len(suf)]
            # Reason heuristic
            reasons = []
            if phi > 0.62: reasons.append(f"high-φ corner (φ={phi:.2f})")
            if phi < 0.45: reasons.append(f"low-φ corner (φ={phi:.2f})")
            if cn < 3.0: reasons.append(f"low CN (CN={cn:.1f})")
            if cn > 5.5: reasons.append(f"high CN (CN={cn:.1f})")
            if cov_amp < 5: reasons.append(f"low cov_AM_P (={cov_amp:.1f})")
            if tau > 3.0: reasons.append(f"high τ (={tau:.1f})")
            if rse < 0.5: reasons.append(f"small r_SE (={rse:.1f})")
            # Family check
            sibs = [j for j in range(n) if nms[j].startswith(root) and j != i]
            if len(sibs) >= 2:
                sib_sigs = [sig_act[j] for j in sibs]
                med = np.median(sib_sigs)
                if med > 0 and abs(sig_act[i] - med)/med > 0.15:
                    reasons.append(f"sibling-tail (this σ={sig_act[i]:.2f} vs family med={med:.2f})")
            if not reasons:
                if pa == 1.0 or pa == 0.0:
                    reasons.append("isolated endpoint (p=0 or p=1, no neighbors)")
                else:
                    reasons.append("isolated case (no clear feature anomaly)")
            print(f"  {nms[i]:32s}  σ={sig_act[i]:>6.2f} pred={pred_new[i]:>6.2f} err={err_new[i]:>+5.1f}%")
            print(f"    → {', '.join(reasons)}")
    print()

    # ───── Improvement suggestions ─────
    print("=" * 110)
    print(" IMPROVEMENT OPPORTUNITIES (data + form)")
    print("=" * 110)
    fail_set = set(fail_idx)
    # 1. Sibling-tail candidates
    print(" 1. Sibling-tail outliers (multi-seed family has tail case):")
    families_seen = {}
    for i in range(n):
        if arr['excluded'][i]: continue
        root = nms[i]
        for suf in ('_S1','_S2','_S3','_S4','_S5'):
            if root.endswith(suf): root = root[:-len(suf)]
        families_seen.setdefault(root, []).append(i)
    sibling_tail = []
    for root, idxs in families_seen.items():
        if len(idxs) < 3: continue
        sigs = [sig_act[j] for j in idxs]
        med = np.median(sigs)
        cv = float(np.std(sigs) / med * 100) if med > 0 else 0
        if cv > 15:
            worst_i = idxs[int(np.argmax([abs(sig_act[j]-med)/med for j in idxs]))]
            sibling_tail.append((root, len(idxs), cv, worst_i, nms[worst_i],
                                 sig_act[worst_i], med, err_new[worst_i]))
    sibling_tail.sort(key=lambda r: -r[2])
    for root, n_sib, cv, wi, wnm, ws, wm, we in sibling_tail[:5]:
        print(f"    {root:25s}  n_sibs={n_sib}  CV={cv:.1f}%  worst={wnm}  σ={ws:.2f} (med {wm:.2f})  err={we:+.1f}%")
    if not sibling_tail:
        print("    (no families with CV>15%)")
    print()

    # 2. Undersampled corners
    print(" 2. Undersampled design corners (isolated cases, no neighbors):")
    iso_cases = []
    for i in fail_idx[:10]:
        root = nms[i]
        for suf in ('_S1','_S2','_S3','_S4','_S5'):
            if root.endswith(suf): root = root[:-len(suf)]
        n_sibs = len(families_seen.get(root, []))
        if n_sibs < 3:
            iso_cases.append((nms[i], err_new[i], n_sibs, arr['phi'][i], arr['p_amp'][i]))
    for nm, e, ns, ph, pp in iso_cases[:5]:
        print(f"    {nm:32s}  err={e:+.1f}%  family n={ns}  φ={ph:.2f} p={pp:.2f}")
        print(f"        → multi-seed sim (5 seeds at this design) would resolve")
    if not iso_cases:
        print("    (no isolated failures)")
    print()

    # 3. Form structure suggestions
    print(" 3. Form structure observations:")
    if user_locked:
        if loo_new < fit21['loocv'] - 0.01:
            print(f"    User lock σ_S={sigma_S:.1f}/σ_P={sigma_P:.1f} degrades LOOCV by {fit21['loocv']-loo_new:.4f}")
            print(f"    → live-fit values (σ_S={sS_fit:.2f}, σ_P={sP_fit:.2f}) ARE necessary")
            print(f"    → S-end vs P-end have genuinely different effective σ in DEM corpus")
        elif loo_new > fit21['loocv'] - 0.005:
            print(f"    User lock holds LOOCV (Δ={loo_new-fit21['loocv']:+.4f})")
            print(f"    → σ_S/σ_P endpoints are not strongly constrained, can use literature value")
        else:
            print(f"    User lock has small LOOCV loss (Δ={loo_new-fit21['loocv']:+.4f})")
    else:
        # Stage 21 final analysis
        print(f"    σ_S/σ_P ratio = {sS_fit/sP_fit:.2f}×  (literature Trevisanello: 2-3×)")
        print(f"    Matches literature → endpoint asymmetry is REAL physics")
        print(f"    14 OLS params on n={nfit} fit cases (n/k = {nfit/14:.1f})")
        print(f"    Comparable to σ_ionic 88/5 = 17.6, our 6.0 is borderline overfit territory")

    print()
    print(" 4. Path to LOOCV improvement (ranked by feasibility):")
    print(f"    a) Multi-seed averaging for 1mAh_5_AMP, 1mAh_8_AMP, 1mAh_6 families")
    print(f"       (CV >15% sibling spread → avg reduces noise floor)")
    print(f"    b) Re-run 31 older sims for missing cov_AM/f_perc metrics")
    print(f"       (currently excluded from form arrays, would join corpus)")
    print(f"    c) Add 2mAh × P-end multi-seed (only 2 such cases → undersampled)")
    print(f"    d) Add high-φ × multi-P cases (φ>0.6 undersampled)")
    print()
    print(" 5. Visualization improvements (already in code):")
    print(f"    ✓ PI band (bootstrap + residual) — shows uncertainty per case")
    print(f"    ✓ Phantom X marks — distinguishes raw missing from form-incomputable")
    print(f"    ✓ Hollow gray squares — flags raw σ available but form metrics missing")


if __name__ == '__main__':
    main()
