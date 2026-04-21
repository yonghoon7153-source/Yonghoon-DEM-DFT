#!/usr/bin/env python3
"""
v30 exhaustive refit — systematic search for the best SINGLE-FORMULA
extension of v29 FORM X that closes the remaining outlier gaps
(thin-electrode bimodal, real-PSD overshoot).

Strategy: start from v29 core
  σ_v29 = C_blend(τ) × σ_grain × (φ-0.2)^0.5 × CN^1.5 × cov^0.4 × f_p^3
        × exp(β_pf·w_pf + β_lin·p·w_win + β_gb·w_gb)

Add a multiplicative correction
  σ_v30 = σ_v29 × exp(Σ_i  γ_i · feature_i(thick, PSD, phi, ...))

Features tried (every single, pair, and triple combination):
  1) THIN_WIDE     = σ_thin × (phi_SE − phi_ref)           captures A/B direction flip
  2) THIN_TIGHT    = exp(−T/T_c)                            boundary boost
  3) THIN_PHI      = σ_thin × phi_SE                        thin × SE content
  4) THIN_INV_T    = 1/T                                    boundary fraction proxy
  5) PSD_CV_R      = CV(r_AM) = std/mean                    real-PSD dispersity
  6) PSD_RATIO     = r_SE/r_AM_avg                          size-ratio proxy
  7) LOG_POR       = log(porosity/porosity_ref)             porosity spread
  8) TAU_DIJ       = τ_Dij − τ_ref                          direct τ term beyond C_blend
  9) CN_DEV        = CN − CN_ref                            CN deviation
 10) REAL_FLAG     = 1 if 'real' in name else 0            catch-all PSD indicator

For each candidate set, Nelder-Mead jointly optimises (γ_i).
Reports R², LOOCV, ±20% band, AIC, and parameter values.
Greedy forward selection: pick best single → best 2 → best 3 (bound by
LOOCV plateau).

Usage:
  python3 scripts/v30_exhaustive_refit.py
  python3 scripts/v30_exhaustive_refit.py --max-terms 4 --verbose
"""
from __future__ import annotations
import os, json, sys, itertools, argparse
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize

SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))
from generate_comparison_plots import _formx_v29_predict, _formx_v29_params, _ps_fraction  # noqa: E402

WEBAPP = Path(__file__).parent.parent / 'webapp'
OUT = Path('docs/figures/physics_regime')
OUT.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────────────────────────────
# Data loading
# ─────────────────────────────────────────────────────────────────────
def load_cases():
    # Optionally merge physics-regime cap % from dataset_summary.csv
    reg_csv = OUT / 'dataset_summary.csv'
    reg_map = {}
    if reg_csv.exists():
        reg_df = pd.read_csv(reg_csv)
        for _, r in reg_df.iterrows():
            reg_map[r['case_id']] = r.to_dict()

    rows = []
    for base in (WEBAPP / 'results', WEBAPP / 'archive'):
        if not base.is_dir():
            continue
        for mp in base.rglob('full_metrics.json'):
            try:
                m = json.load(open(mp))
            except Exception:
                continue
            s_act = m.get('sigma_full_mScm')
            if not s_act or s_act < 1e-4:
                continue

            phi = m.get('phi_se')
            tau = (m.get('tortuosity_recommended') or m.get('tortuosity_mean')
                   or m.get('tau_dij'))
            cn = m.get('se_se_cn')
            cov_vals = [v for v in (m.get('coverage_AM_P_mean'),
                                     m.get('coverage_AM_S_mean'),
                                     m.get('coverage_AM_mean')) if v and v > 0]
            cov = (sum(cov_vals) / len(cov_vals) / 100) if cov_vals else 0.20
            fp = m.get('percolation_pct')
            fp = (fp / 100.0) if fp else 0.5
            gb = m.get('gb_density_mean', 1e-6) or 1e-6
            thick = m.get('thickness_um') or 0
            porosity = m.get('porosity') or 0

            cid = mp.parent.name
            meta_p = WEBAPP / 'uploads' / cid / 'meta.json'
            ip_p = WEBAPP / 'results' / cid / 'input_params.json'
            nm = cid; ps_ratio = ''
            r_AM_P = r_AM_S = r_SE = None
            if meta_p.exists():
                try:
                    mj = json.load(open(meta_p))
                    nm = mj.get('name', cid)
                    ps_ratio = mj.get('ps_ratio', '')
                except Exception:
                    pass
            if ip_p.exists():
                try:
                    ip = json.load(open(ip_p))
                    r_AM_P = ip.get('r_AM_P'); r_AM_S = ip.get('r_AM_S')
                    r_SE = ip.get('r_SE')
                except Exception:
                    pass

            if any(x is None for x in (phi, tau, cn)) or tau <= 0 or phi <= 0.20 or cn <= 0:
                continue

            p_frac = _ps_fraction({'ps_ratio': ps_ratio})

            # Physics-regime cap percentages (from dataset_summary.csv)
            reg = reg_map.get(cid, {})
            rows.append({
                'case_id': cid, 'name': nm,
                'sigma_actual': s_act,
                'phi': phi, 'tau': tau, 'cn': cn, 'cov': cov,
                'f_perc': max(fp, 0.01), 'p_frac': p_frac, 'gb_dens': gb,
                'thick': thick, 'porosity': porosity,
                'r_AM_P': r_AM_P, 'r_AM_S': r_AM_S, 'r_SE': r_SE,
                'is_real': int('real' in nm.lower()),
                'is_thin': int('thin' in nm.lower() or thick < 25),
                # Physics-regime cap activation (from physics_regime_histogram --all)
                'geom_pct':    reg.get('geom', 0) or 0,
                'tabor_pct':   reg.get('tabor', 0) or 0,
                'liggghts_lb_pct': reg.get('liggghts_lb', 0) or 0,
                'p50_dr':      reg.get('p50_dr', 0) or 0,
                'p90_dr':      reg.get('p90_dr', 0) or 0,
            })

    seen = {}
    for r in rows:
        k = (r['name'], round(r['phi'], 3))
        if k not in seen:
            seen[k] = r
    return list(seen.values())


# ─────────────────────────────────────────────────────────────────────
# Feature engineering
# ─────────────────────────────────────────────────────────────────────
def build_features(df: pd.DataFrame) -> dict:
    """Compute candidate correction features for every case.
    Each feature is a vector of length n — multiplicative correction
    σ_v30 = σ_v29 × exp(Σ γ_i · feature_i)
    """
    T = df['thick'].values
    phi = df['phi'].values
    tau = df['tau'].values
    cn = df['cn'].values
    por = df['porosity'].values
    fp = df['f_perc'].values

    # Thin regime indicator
    T_c = 30.0  # μm characteristic thin length
    sigma_T = 15.0
    w_thin = np.exp(-T / T_c)                       # 1 at T→0, 0 at T→∞

    # AM size dispersity proxy
    r_p = df['r_AM_P'].fillna(np.nan).values
    r_s = df['r_AM_S'].fillna(np.nan).values
    r_se = df['r_SE'].fillna(0.0005).values
    # CV of AM radii if bimodal, else 0
    cv_r = np.zeros(len(df))
    for i, (p, s) in enumerate(zip(r_p, r_s)):
        if p and s and not np.isnan(p) and not np.isnan(s):
            mean = (p + s) / 2
            std  = abs(p - s) / 2
            cv_r[i] = std / mean
        else:
            cv_r[i] = 0.0

    # Size ratio: r_SE / r_AM_avg  (bigger means SE relatively large)
    r_am_avg = np.zeros(len(df))
    for i, (p, s) in enumerate(zip(r_p, r_s)):
        if p and not np.isnan(p) and s and not np.isnan(s):
            r_am_avg[i] = (p + s) / 2
        elif p and not np.isnan(p):
            r_am_avg[i] = p
        elif s and not np.isnan(s):
            r_am_avg[i] = s
        else:
            r_am_avg[i] = 0.003  # default
    size_ratio = r_se / np.where(r_am_avg > 0, r_am_avg, 0.003)

    # Porosity log deviation from reference
    por_ref = 17.0
    log_por = np.log(np.maximum(por, 1.0) / por_ref)

    # τ deviation from reference
    tau_ref = 1.5
    tau_dev = tau - tau_ref

    # CN deviation
    cn_ref = 5.0
    cn_dev = cn - cn_ref

    features = {
        # Thin-regime direction-flip family
        'THIN_WIDE':  w_thin * (phi - 0.25),
        'THIN_TIGHT': w_thin,
        'THIN_PHI':   w_thin * phi,
        'THIN_INV_T': 1.0 / np.maximum(T, 1.0),
        'THIN_TAU':   w_thin * (tau - 1.5),
        # PSD / size-ratio family
        'PSD_CV_R':   cv_r,
        'PSD_RATIO':  size_ratio,
        'REAL_FLAG':  df['is_real'].values.astype(float),
        # Porosity / τ / CN deviation family
        'LOG_POR':    log_por,
        'TAU_DIJ':    tau_dev,
        'CN_DEV':     cn_dev,
        # NEW — Physics-regime cap percentages (from dataset_summary.csv)
        # Normalised to 0–1 for numerical stability
        'GEOM_PCT':      df['geom_pct'].values / 20.0,    # 0–17% → ~0–0.85
        'TABOR_PCT':     (df['tabor_pct'].values - 85.0) / 15.0,  # centred around 85%
        'LIGG_LB_PCT':   df['liggghts_lb_pct'].values / 35.0,     # 0–34%
        'P50_DR':        df['p50_dr'].values,              # 0.07–0.36
        'P50_DR_DEV':    df['p50_dr'].values - 0.20,       # deviation from full-plastic threshold
        # Thin × cap interactions (likely useful — thin regime × packing signature)
        'THIN_X_GEOM':   w_thin * (df['geom_pct'].values / 20.0),
        'THIN_X_LIGG':   w_thin * (df['liggghts_lb_pct'].values / 35.0),
    }
    return features


# ─────────────────────────────────────────────────────────────────────
# Fit machinery
# ─────────────────────────────────────────────────────────────────────
def v29_predict_vec(df, params):
    preds = []
    for _, r in df.iterrows():
        p = _formx_v29_predict(
            r['phi'], r['cn'], r['tau'], r['cov'], r['f_perc'],
            r['p_frac'], r['gb_dens'], params=params)
        preds.append(max(p, 1e-8))
    return np.array(preds)


def r2_log(actual, predicted):
    la, lp = np.log(actual), np.log(predicted)
    return 1 - np.sum((la - lp) ** 2) / np.sum((la - np.mean(la)) ** 2)


def loocv_r2(actual, predicted_fn, n):
    la = np.log(actual)
    ss_tot = np.sum((la - np.mean(la)) ** 2)
    sse = 0.0
    for i in range(n):
        mask = np.ones(n, bool); mask[i] = False
        pred_i = predicted_fn(mask, i)
        sse += (la[i] - np.log(max(pred_i, 1e-8))) ** 2
    return 1 - sse / ss_tot


def fit_candidate(df, feature_names, features, base_pred):
    """Fit σ_v30 = base_pred × exp(X @ γ) where X = stacked features.
    Returns dict with r2, loocv, aic, gammas, pred.
    """
    actual = df['sigma_actual'].values
    log_actual = np.log(actual)
    log_base = np.log(base_pred)

    X = np.column_stack([features[f] for f in feature_names]) if feature_names else np.zeros((len(df), 0))

    def fit_gammas(X_sub, log_y, log_b):
        # OLS: log_y = log_b + X @ γ → γ = (X'X)^-1 X' (log_y - log_b)
        if X_sub.shape[1] == 0:
            return np.array([]), log_b
        residual = log_y - log_b
        gammas, *_ = np.linalg.lstsq(X_sub, residual, rcond=None)
        return gammas, log_b + X_sub @ gammas

    gammas, log_pred = fit_gammas(X, log_actual, log_base)
    pred = np.exp(log_pred)

    r2 = r2_log(actual, pred)

    # LOOCV — refit γ on each fold
    n = len(df)
    ss_tot = np.sum((log_actual - np.mean(log_actual)) ** 2)
    sse_loo = 0.0
    for i in range(n):
        mask = np.ones(n, bool); mask[i] = False
        g_fold, _ = fit_gammas(X[mask] if X.shape[1] > 0 else np.zeros((n-1, 0)),
                                log_actual[mask], log_base[mask])
        pred_i = log_base[i] + (X[i] @ g_fold if X.shape[1] > 0 else 0)
        sse_loo += (log_actual[i] - pred_i) ** 2
    loocv = 1 - sse_loo / ss_tot

    k = len(feature_names)  # number of free params added on top of v29
    aic = n * np.log(np.sum((log_actual - log_pred) ** 2) / n) + 2 * k
    w20 = int(np.sum(np.abs(pred - actual) / actual < 0.20))

    return {
        'features': feature_names,
        'r2': r2, 'loocv': loocv, 'aic': aic, 'w20': w20, 'n': n,
        'gammas': gammas, 'pred': pred,
    }


# ─────────────────────────────────────────────────────────────────────
# Main driver
# ─────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--max-terms', type=int, default=4,
                    help='Max number of correction terms to try combining')
    ap.add_argument('--verbose', action='store_true')
    args = ap.parse_args()

    rows = load_cases()
    df = pd.DataFrame(rows)
    print(f"Loaded {len(df)} cases")

    params = _formx_v29_params()
    base_pred = v29_predict_vec(df, params)
    r2_base = r2_log(df['sigma_actual'].values, base_pred)
    print(f"\nBaseline v29 (no correction):")
    print(f"  R² = {r2_base:.4f}")

    features = build_features(df)
    feature_names = list(features.keys())
    print(f"\nFeatures: {feature_names}")

    # ─── Single-term search ────────────────────────────────────────
    print("\n" + "=" * 60)
    print("ROUND 1: Single-term additions (each feature alone)")
    print("=" * 60)
    single_results = []
    for fname in feature_names:
        res = fit_candidate(df, [fname], features, base_pred)
        single_results.append(res)
        if args.verbose or True:
            print(f"  {fname:12s}  R²={res['r2']:.4f}  LOOCV={res['loocv']:.4f}  "
                  f"AIC={res['aic']:+.2f}  ±20%={res['w20']:2d}/{res['n']}  "
                  f"γ={res['gammas'][0]:+.4f}")
    single_results.sort(key=lambda x: -x['loocv'])
    best_single = single_results[0]
    print(f"\n  ★ Best single: {best_single['features']}  LOOCV={best_single['loocv']:.4f}")

    # ─── Multi-term search (greedy forward) ────────────────────────
    combo_results = list(single_results)
    for k in range(2, args.max_terms + 1):
        print("\n" + "=" * 60)
        print(f"ROUND {k}: {k}-term combinations")
        print("=" * 60)
        round_results = []
        # Greedy: start from best (k-1), add each remaining feature
        prev_best = max([r for r in combo_results if len(r['features']) == k - 1],
                        key=lambda x: x['loocv'])
        for fname in feature_names:
            if fname in prev_best['features']:
                continue
            new_features = prev_best['features'] + [fname]
            res = fit_candidate(df, new_features, features, base_pred)
            round_results.append(res)
            if args.verbose:
                print(f"  {'+'+fname:13s}  LOOCV={res['loocv']:.4f}  "
                      f"R²={res['r2']:.4f}  ±20%={res['w20']:2d}")
        round_results.sort(key=lambda x: -x['loocv'])
        if not round_results:
            break
        best_k = round_results[0]
        print(f"  ★ Best {k}-term: {best_k['features']}")
        print(f"    LOOCV={best_k['loocv']:.4f}  R²={best_k['r2']:.4f}  "
              f"AIC={best_k['aic']:+.2f}  ±20%={best_k['w20']}/{best_k['n']}")
        for f, g in zip(best_k['features'], best_k['gammas']):
            print(f"      γ({f}) = {g:+.4f}")
        combo_results.extend(round_results)
        # Also do exhaustive combinations at this level (not just greedy)
        if k <= 3:
            exhaustive = []
            for combo in itertools.combinations(feature_names, k):
                res = fit_candidate(df, list(combo), features, base_pred)
                exhaustive.append(res)
            exhaustive.sort(key=lambda x: -x['loocv'])
            print(f"\n  Top 5 EXHAUSTIVE {k}-term combos:")
            for i, r in enumerate(exhaustive[:5]):
                marker = '★' if r['features'] == best_k['features'] else ' '
                print(f"    {marker} #{i+1} {'+'.join(r['features']):55s}  "
                      f"LOOCV={r['loocv']:.4f}  R²={r['r2']:.4f}")
            combo_results.extend(exhaustive[:20])

    # ─── Final summary ─────────────────────────────────────────────
    combo_results.sort(key=lambda x: -x['loocv'])
    print("\n" + "=" * 60)
    print("FINAL RANKING (by LOOCV, top 15)")
    print("=" * 60)
    for i, r in enumerate(combo_results[:15]):
        flabel = '+'.join(r['features']) if r['features'] else '(v29 only)'
        print(f"  #{i+1:2d}  LOOCV={r['loocv']:.4f}  R²={r['r2']:.4f}  "
              f"AIC={r['aic']:+7.2f}  ±20%={r['w20']:2d}/{r['n']}  "
              f"k={len(r['features'])}  {flabel}")

    # Dump to CSV
    rows_out = []
    for r in combo_results:
        row = {'n_terms': len(r['features']),
               'features': '+'.join(r['features']),
               'r2': r['r2'], 'loocv': r['loocv'],
               'aic': r['aic'], 'w20': r['w20']}
        for f, g in zip(r['features'], r['gammas']):
            row[f'gamma_{f}'] = g
        rows_out.append(row)
    out_csv = OUT / 'v30_refit_candidates.csv'
    pd.DataFrame(rows_out).sort_values('loocv', ascending=False).to_csv(out_csv, index=False)
    print(f"\n→ {out_csv}")

    # Save best prediction per-case
    best = combo_results[0]
    df['sigma_pred_v30'] = best['pred']
    df['err_pct'] = 100 * (df['sigma_pred_v30'] - df['sigma_actual']) / df['sigma_actual']
    df['abs_err_pct'] = df['err_pct'].abs()
    out_pc = OUT / 'v30_best_per_case.csv'
    df.sort_values('abs_err_pct', ascending=False).to_csv(out_pc, index=False)
    print(f"→ {out_pc}")


if __name__ == '__main__':
    main()
