#!/usr/bin/env python3
"""σ_electronic Stage 15 shape-mismatch diagnostic.

Goal (per user 2026-05-29): 'R² 은 허상' — production form's shape vs
Stage E target shape needs to match BEFORE chasing R².  This script
identifies systematic per-family / per-region shape mismatches and
proposes what physics is missing.

For each case in the global Stage 15 fit corpus:
  1. Compute form prediction
  2. Compute residual (form − target) / target × 100  in %
  3. Group cases by family base (1mAh, 6mAh, 8mAh, particulate)
     and sub-series (1mAh_100, 6mAh_real, 8mAh_real, etc.)
  4. Report per-group mean residual + spread
  5. For each candidate missing feature (am_am_n_contacts,
     coverage_AM, r_SE, r_AM_eff, T, ...), compute Spearman
     correlation with the per-case residual

If a feature shows |ρ| > 0.4 globally, it's a candidate form-term
addition.  If a SUB-GROUP shows a large mismatch but feature ρ is weak,
the mismatch is form-structure (exponent / functional form), not a
missing scalar feature.

Run on WSL:
    python3 scripts/electronic_shape_audit.py
"""
from __future__ import annotations
import sys, json, re
from pathlib import Path
from collections import defaultdict
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(SCRIPTS.parent))   # in case we run from repo root


def _family_base(nm: str) -> tuple[str, str]:
    """Return (broad_family, sub_series).
    'input_1mAh_100_5'        -> ('1mAh', '1mAh_100')
    'input_1mAh_5'            -> ('1mAh', '1mAh_base')
    'input_1mAh_5_AMP'        -> ('1mAh', '1mAh_AMP')
    'input_6mAh_real_5'       -> ('6mAh', '6mAh_real')
    'input_6mAh_real40_2'     -> ('6mAh', '6mAh_real40')
    'input_8mAh_real_10'      -> ('8mAh', '8mAh_real')
    'input_particulate_5'     -> ('particulate', 'particulate_base')
    'input_particulate_S_*'   -> ('particulate', 'particulate_S')
    'input_S_2'               -> ('particulate', 'S')
    """
    n = re.sub(r'^input_', '', nm)
    # broad family
    if n.startswith('1mAh'):     broad = '1mAh'
    elif n.startswith('6mAh'):   broad = '6mAh'
    elif n.startswith('8mAh'):   broad = '8mAh'
    elif n.startswith('particulate') or n.startswith('S_') or n == 'S': broad = 'particulate'
    else: broad = 'other'
    # sub-series
    if '_100' in n:                 sub = broad + '_100'
    elif '_real40' in n:            sub = broad + '_real40'
    elif '_real' in n:              sub = broad + '_real'
    elif '_AMP' in n:               sub = broad + '_AMP'
    elif '_AMS' in n:               sub = broad + '_AMS'
    elif broad == 'particulate' and ('_E05' in n or '_E15' in n): sub = 'particulate_E'
    else:                           sub = broad + '_base'
    return broad, sub


def main():
    import matplotlib
    matplotlib.use('Agg')
    import generate_comparison_plots as gcp

    # ───── Walk corpus ─────
    data_list, names = [], []
    seen = set()
    for base in ('webapp/results', 'webapp/archive'):
        bp = Path(base)
        if not bp.is_dir(): continue
        for mp in bp.rglob('full_metrics.json'):
            meta_p = mp.parent / 'meta.json'
            nm = mp.parent.name
            if meta_p.exists():
                try: nm = json.load(open(meta_p)).get('name', nm) or nm
                except Exception: pass
            if nm in seen: continue
            seen.add(nm)
            try: d = json.load(open(mp))
            except Exception: continue
            data_list.append(d); names.append(nm)

    # ───── Global Stage 15 fit (using dashboard's helpers) ─────
    arr = gcp._electronic_form_arrays(data_list, names)
    if arr is None:
        print("[ABORT] corpus too small for Stage 15 form fit"); return
    fit_mask = ~arr['excluded']
    fit = gcp._electronic_fit(arr, fit_mask=fit_mask)
    coef = fit['coef']
    sig_act = arr['sig_act']
    sig_pred = np.exp(fit['pred_log'])
    err_pct = (sig_pred - sig_act) / sig_act * 100.0
    nfit = fit['n_fit']
    n = arr['n']

    sigma_S = float(np.exp(coef[0])); sigma_P = float(np.exp(coef[1]))
    print("=" * 100)
    print(f" σ_electronic Stage 15 — SHAPE MISMATCH AUDIT  (corpus n={n}, fit n={nfit})")
    print("=" * 100)
    print(f"  Global fit: σ_S={sigma_S:.2f}  σ_P={sigma_P:.2f}  "
          f"β_T={coef[2]:+.3f}  β_v={coef[3]:+.3f}  β_AC={coef[7]:+.3f}")
    print(f"              C(τ)={coef[4]:+.2f}{coef[5]:+.2f}·lnτ{coef[6]:+.2f}·ln²τ")
    print(f"  R²={fit['r2']:.3f}  LOOCV={fit['loocv']:.3f}")
    print()

    # ───── Group cases by family ─────
    by_broad = defaultdict(list)
    by_sub = defaultdict(list)
    for i, nm in enumerate(arr['names']):
        broad, sub = _family_base(nm)
        by_broad[broad].append(i)
        by_sub[sub].append(i)

    # ───── Per-family bias ─────
    print("─" * 100)
    print(" Per-BROAD-FAMILY shape bias  (mean form/target err%, + = form OVER, − = UNDER)")
    print("─" * 100)
    print(f"  {'family':14s}  {'n':>4s}  {'mean err%':>10s}  {'median':>8s}  {'spread (p25..p75)':>22s}  {'max |err|':>9s}")
    for fam in ('1mAh', '6mAh', '8mAh', 'particulate', 'other'):
        idx = by_broad.get(fam, [])
        if not idx: continue
        errs = np.array([err_pct[i] for i in idx])
        # Skip audit-excluded for averaging (their large err is intentional)
        excl_mask = np.array([arr['excluded'][i] for i in idx])
        clean = errs[~excl_mask]
        if len(clean) == 0: continue
        m = float(np.mean(clean)); md = float(np.median(clean))
        p25, p75 = float(np.percentile(clean, 25)), float(np.percentile(clean, 75))
        mx = float(np.max(np.abs(clean)))
        n_excl = int(excl_mask.sum())
        excl_tag = f" ({n_excl} excl)" if n_excl else ""
        print(f"  {fam:14s}  {len(clean):>4d}  {m:+10.1f}  {md:+8.1f}  "
              f"{p25:+7.1f}..{p75:+7.1f}  {mx:>9.1f}{excl_tag}")
    print()

    # ───── Per-sub-series bias ─────
    print("─" * 100)
    print(" Per-SUB-SERIES shape bias  (sorted by |mean err%|)")
    print("─" * 100)
    print(f"  {'sub-series':22s}  {'n':>4s}  {'mean err%':>10s}  {'flag':>10s}")
    sub_stats = []
    for sub, idx in by_sub.items():
        excl_mask = np.array([arr['excluded'][i] for i in idx])
        errs = np.array([err_pct[i] for i in idx])[~excl_mask]
        if len(errs) < 2: continue
        m = float(np.mean(errs))
        sub_stats.append((sub, len(errs), m))
    sub_stats.sort(key=lambda r: -abs(r[2]))
    for sub, nn, mean_err in sub_stats:
        flag = ""
        if abs(mean_err) > 25: flag = "★ SHAPE-MISS"
        elif abs(mean_err) > 15: flag = "◆ noticeable"
        print(f"  {sub:22s}  {nn:>4d}  {mean_err:+10.1f}  {flag:>10s}")
    print()

    # ───── Spearman correlation of residuals with structural features ─────
    print("─" * 100)
    print(" Residual ~ feature Spearman correlation  (sorted by |ρ|)")
    print(" (|ρ|>0.4 → real missing feature; |ρ|<0.2 → form-structure issue, not a missing scalar)")
    print("─" * 100)
    feat_keys = [
        ('phi_am', None), ('phi_se', None),
        ('am_am_cn', None), ('am_am_mean_area', None),
        ('am_am_n_contacts', None), ('am_am_mean_force', None),
        ('se_se_cn', None), ('coverage_AM_mean', None),
        ('coverage_AM_P_mean', None), ('coverage_AM_S_mean', None),
        ('thickness_um', None), ('r_AM_S', None), ('r_AM_P', None),
        ('AM_S_vulnerable_pct', 'am_vulnerable_pct'),
        ('bulk_resistance_fraction', None),
        ('contact_pressure_max', None), ('contact_pressure_mean', None),
        ('stress_cv', None),
        ('path_conductance_mean', None),
        ('tortuosity_recommended', 'tortuosity_mean'),
    ]
    feat_vals = {}
    for i_corp, idx in enumerate(arr['keep_idx']):
        if i_corp >= n: break
        d = data_list[idx]
        for k, fb in feat_keys:
            v = d.get(k)
            if v is None and fb: v = d.get(fb)
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                feat_vals.setdefault(k, []).append((i_corp, float(v)))

    from scipy.stats import spearmanr
    corr_results = []
    excl_mask = arr['excluded']
    resid_log = arr['logsf'] - fit['pred_log']  # log-space residual
    for k, _ in feat_keys:
        pairs = feat_vals.get(k, [])
        if len(pairs) < 8: continue
        ii = np.array([p[0] for p in pairs])
        vv = np.array([p[1] for p in pairs])
        # use non-excluded only for the correlation
        m = ~excl_mask[ii] & np.isfinite(vv)
        if m.sum() < 8: continue
        try:
            rho, _ = spearmanr(vv[m], resid_log[ii[m]])
            if np.isnan(rho): continue
            corr_results.append((k, float(rho), int(m.sum())))
        except Exception:
            continue
    corr_results.sort(key=lambda r: -abs(r[1]))
    print(f"  {'feature':28s}  {'ρ':>7s}  {'n':>4s}  status")
    for k, rho, nn in corr_results[:15]:
        flag = ""
        if abs(rho) > 0.4: flag = "★ STRONG — candidate form term"
        elif abs(rho) > 0.25: flag = "◆ moderate — re-fit consideration"
        print(f"  {k:28s}  {rho:+7.3f}  {nn:>4d}  {flag}")
    print()

    # ───── Verdict ─────
    print("=" * 100)
    print(" VERDICT — actionable next steps")
    print("=" * 100)
    bad_subs = [s for s in sub_stats if abs(s[2]) > 25]
    strong_feats = [r for r in corr_results if abs(r[1]) > 0.4]
    if bad_subs:
        print(f"  ★ {len(bad_subs)} sub-series with shape mismatch >±25%:")
        for sub, nn, m in bad_subs:
            direction = "OVER" if m > 0 else "UNDER"
            print(f"     {sub} ({nn} cases): form {direction}-predicts by {abs(m):.0f}%")
    if strong_feats:
        print(f"\n  ★ {len(strong_feats)} structural features with |ρ|>0.4 vs residual:")
        for k, rho, nn in strong_feats:
            print(f"     {k:28s} ρ={rho:+.2f}  → add to form?")
    if not strong_feats and bad_subs:
        print(f"\n  No |ρ|>0.4 feature → mismatched sub-series have FORM-STRUCTURE issue")
        print(f"  (wrong exponent, missing nonlinearity, not a missing scalar).")
        print(f"  → Inspect mismatched sub-series structurally (φ_AM range, CN range, T, r_AM).")
    if not bad_subs:
        print(f"  No sub-series >±25% mismatch — Stage 15 shape is acceptable.")
        print(f"  Remaining work: chase R² via finer tuning OR accept ceiling.")


if __name__ == '__main__':
    main()
