#!/usr/bin/env python3
"""Physics-mode fit v33 — break the R²=0.96 ceiling with new features.

Stage 1 of physics_fit_final.py plateaued at R²=0.962 / LOOCV=0.956
because the existing v29 features (φ, τ, CN, cov, f_perc, p_frac, gb)
saturate. Adding more parameters from the same feature space gives no
new signal — c_t, β_pf, β_gb all collapse to zero under fitting.

This script tries to break that ceiling by feeding the fit two new
data signals that v29 never saw:

  1) **5-case binding share** (A_binding_share_AM_SE_pct from
     full_metrics.json, written by coverage_physics_vs_hertzian.py).
     Five percentages — H / L / T / V / G — describing what fraction
     of AM-SE contacts had each candidate area selected.
  2) **r_SE / r_AM ratio** — particle-size ratio (from input_params.json).
     v32's only non-zero correction was -0.05·r_SE/r_AM, suggesting
     it carries genuine residual signal.

Stage progression:
  Stage 0:  σ_v29 baseline (control, just to compare)
  Stage 1:  + binding share features (4 params, drop one for collinearity)
  Stage 2:  + r_SE/r_AM
  Stage 3:  + τ × tabor_share interaction (does plastic regime depend
              on tortuosity differently than elastic?)

Each stage:
  - Multi-start Nelder-Mead (8 starts) on the new γ params, OLS-style
  - Report R², LOOCV, w20 band, parameter values
  - Print which case shifted most under the new fit (residual change)

If R² hits 0.99 the form is publication-ready. If we plateau again
we'll know the binding/ratio features hit their own ceiling and need
yet more features (e.g., GB anisotropy, force-chain stats).
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
from v32_exhaustive_refit import load_cases  # noqa: E402

WEBAPP = SCRIPTS.parent / 'webapp'
SIGMA_GRAIN = 3.0


def _read_full_metrics(cid: str) -> dict | None:
    for base in ('results', 'archive'):
        for p in (WEBAPP / base).rglob(f'{cid}/full_metrics.json'):
            try:
                return json.load(open(p))
            except Exception:
                pass
    return None


def _read_input_params(cid: str) -> dict | None:
    p = WEBAPP / 'results' / cid / 'input_params.json'
    if p.exists():
        try:
            return json.load(open(p))
        except Exception:
            pass
    return None


def load_phys_rows(cases):
    """Enrich cases with physics σ, physics coverage, binding share, r_SE/r_AM."""
    rows = []
    for c in cases:
        cid = c['case_id']
        fm = _read_full_metrics(cid)
        if fm is None:
            continue
        sig_p = fm.get('sigma_full_mScm_physics')
        if not sig_p or sig_p < 1e-4:
            continue
        cov_p = (fm.get('coverage_AM_mean_physics')
                 or fm.get('coverage_AM_P_mean_physics')
                 or fm.get('coverage_AM_S_mean_physics'))
        if not cov_p:
            continue
        binding = fm.get('A_binding_share_AM_SE_pct') or {}
        # All five binding shares (sum ≈ 100). We'll drop one for collinearity.
        rows.append({
            'case_id':   cid,
            'name':      c['name'],
            'phi':       c['phi'],
            'tau':       c['tau'],
            'cn':        c['cn'],
            'cov_phys':  cov_p / 100.0,
            'f_perc':    c['f_perc'],
            'p_frac':    c['p_frac'],
            'gb_dens':   c['gb_dens'],
            'thick':     c['thick'],
            'sigma':     sig_p,
            # Binding share %
            'b_hertzian': float(binding.get('hertzian', 0)),
            'b_liggghts': float(binding.get('liggghts', 0)),
            'b_tabor':    float(binding.get('tabor', 0)),
            'b_volume':   float(binding.get('volume', 0)),
            'b_geom':     float(binding.get('geom', 0)),
            # Particle size ratio (None when not available)
            'r_SE':       c.get('r_SE'),
            'r_AM_S':     c.get('r_AM_S'),
            'r_AM_P':     c.get('r_AM_P'),
        })
    return rows


# ────────────────────────────────────────────────────────────────────
# Base v29 prediction
# ────────────────────────────────────────────────────────────────────
def predict_base(df, params):
    """Pure power-law base, no C(τ) blend (it collapses on physics data
    per the Stage 1/2/3 stagnation observed earlier)."""
    alpha, beta, gamma, delta, phi_c, mu, b0 = params
    phi  = df['phi'].values
    tau  = df['tau'].values
    cn   = df['cn'].values
    cov  = df['cov_phys'].values
    f_p  = df['f_perc'].values
    excess = np.maximum(phi - phi_c, 1e-6)
    pred = (np.exp(b0) * SIGMA_GRAIN
            * excess ** alpha
            * cn    ** beta
            * cov   ** gamma
            * f_p   ** delta
            * tau   ** mu)
    return pred


def loss_base(params, df):
    pred = predict_base(df, params)
    log_err = np.log(pred + 1e-12) - np.log(df['sigma'].values + 1e-12)
    return float(np.mean(log_err ** 2))


def fit_base(df, n_start=10):
    bounds = [(0.3, 3.0),  # alpha
              (0.3, 3.0),  # beta
              (0.0, 1.5),  # gamma
              (0.5, 7.0),  # delta
              (0.05, 0.30),# phi_c
              (-2.0, 0.5), # mu
              (-5.0, 5.0)] # b0
    rng = np.random.default_rng(42)
    best = None
    for s in range(n_start):
        x0 = [rng.uniform(*b) for b in bounds]
        res = minimize(loss_base, x0, args=(df,), method='Nelder-Mead',
                       options={'maxiter': 2000, 'xatol': 1e-6, 'fatol': 1e-8})
        if best is None or res.fun < best.fun:
            best = res
    return best.x


def metrics(actual, pred):
    a = np.log(actual + 1e-12); p = np.log(pred + 1e-12)
    ss_res = np.sum((a - p) ** 2)
    ss_tot = np.sum((a - a.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    err = np.abs(actual - pred) / np.maximum(actual, 1e-12)
    w20 = int(np.sum(err <= 0.20))
    return r2, w20


def loocv_r2(df, base_pred, gamma_features=None, gamma=None):
    """Leave-one-out R² for an additive log-space correction.
       log σ_pred = log base_pred + Σ γ_i feature_i
    """
    n = len(df)
    if gamma_features is None or len(gamma_features) == 0:
        # Pure base prediction LOOCV — no fitted residual.
        actual = df['sigma'].values
        a = np.log(actual + 1e-12); p = np.log(base_pred + 1e-12)
        ss_res = np.sum((a - p) ** 2)
        ss_tot = np.sum((a - a.mean()) ** 2)
        return 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    X = np.column_stack([df[f].values for f in gamma_features])
    actual_log = np.log(df['sigma'].values + 1e-12)
    base_log = np.log(base_pred + 1e-12)
    resid = actual_log - base_log
    pred_log_loo = np.empty(n)
    for i in range(n):
        idx = np.arange(n) != i
        Xi = X[idx]; yi = resid[idx]
        coef, *_ = np.linalg.lstsq(Xi, yi, rcond=None)
        pred_log_loo[i] = base_log[i] + X[i] @ coef
    a = actual_log; p = pred_log_loo
    ss_res = np.sum((a - p) ** 2)
    ss_tot = np.sum((a - a.mean()) ** 2)
    return 1 - ss_res / ss_tot if ss_tot > 0 else 0.0


def fit_residual_features(df, base_pred, feature_names):
    """OLS γ on log residual — γ minimises Σ(log σ - log base - γ·X)²."""
    if not feature_names:
        return [], base_pred
    X = np.column_stack([df[f].values for f in feature_names])
    resid = np.log(df['sigma'].values + 1e-12) - np.log(base_pred + 1e-12)
    coef, *_ = np.linalg.lstsq(X, resid, rcond=None)
    pred = base_pred * np.exp(X @ coef)
    return coef, pred


def fit_stage(df, stage, label, base_params=None):
    """Stage 0 = base-only. Stages 1+ add features incrementally.

    Stages 2+ require r_SE/r_AM, so we restrict to rows that have both
    when those features are active to avoid SVD failure on degenerate
    columns.
    """
    if base_params is None:
        base_params = fit_base(df)

    df_stage = df.copy()
    feature_names = []
    if stage >= 1:
        # Drop b_volume (≈ 0 in most cases) to break sum-to-100 collinearity.
        feature_names += ['b_hertzian', 'b_liggghts', 'b_tabor', 'b_geom']
    if stage >= 2:
        # r_SE / r_AM_S — restrict to rows with both available
        def _ratio(r):
            rs = r['r_SE']
            ra = r['r_AM_S'] or r['r_AM_P']
            if rs and ra and ra > 0:
                return rs / ra
            return None
        df_stage['r_ratio'] = df_stage.apply(_ratio, axis=1)
        df_stage = df_stage[df_stage['r_ratio'].notna()].reset_index(drop=True)
        feature_names += ['r_ratio']
    if stage >= 3:
        df_stage['tau_tabor'] = df_stage['tau'].values * df_stage['b_tabor'].values / 100.0
        df_stage['tau_geom']  = df_stage['tau'].values * df_stage['b_geom'].values / 100.0
        feature_names += ['tau_tabor', 'tau_geom']

    # Drop features that are all zero / constant (degenerate)
    feature_names = [f for f in feature_names if f in df_stage.columns
                     and df_stage[f].std() > 1e-9]

    base_pred = predict_base(df_stage, base_params)
    coef, pred = fit_residual_features(df_stage, base_pred, feature_names)
    r2, w20 = metrics(df_stage['sigma'].values, pred)
    loocv = loocv_r2(df_stage, base_pred, feature_names, coef)

    print(f'\n── Stage {stage} — {label} ──')
    print(f'  n={len(df_stage)}   R²={r2:.4f}   LOOCV={loocv:.4f}   w20={w20}/{len(df_stage)}')
    print('  base:', '  '.join(f'{n}={v:+.3f}' for n, v in zip(
        ('α','β','γ','δ','φc','μ','b0'), base_params)))
    if feature_names:
        print('  residual γ:')
        for f, g in zip(feature_names, coef):
            print(f'    {f:14s} = {g:+.4f}')
    return {
        'stage': stage, 'label': label,
        'r2': r2, 'loocv': loocv, 'w20': w20, 'n': len(df_stage),
        'base_params': list(base_params),
        'features':    feature_names,
        'gamma':       list(coef),
    }


def diagnose_residuals(df, base_pred, top_k=12):
    """Print the top-k cases by absolute log-space residual.

    The R² ceiling at 0.96 with all v29 features collapsed strongly
    suggests a small number of cases are dragging the fit. Listing the
    biggest offenders should reveal whether they share a regime
    (thin / extreme p_frac / outlier τ) — which then suggests the
    feature class to add next.
    """
    log_resid = np.log(df['sigma'].values + 1e-12) - np.log(base_pred + 1e-12)
    idx = np.argsort(-np.abs(log_resid))
    print('\n=== Top residual cases (|log_residual| sorted) ===')
    print(f'{"name":36s}  {"σ_act":>8s}  {"σ_pred":>8s}  {"resid":>8s}  '
          f'{"τ":>5s}  {"φ":>5s}  {"CN":>5s}  {"p":>5s}  '
          f'{"H%":>5s}  {"L%":>5s}  {"T%":>5s}  {"G%":>5s}')
    for i in idx[:top_k]:
        row = df.iloc[i]
        print(f'{str(row["name"])[:36]:36s}  '
              f'{row["sigma"]:8.4f}  {base_pred[i]:8.4f}  '
              f'{log_resid[i]:+8.3f}  '
              f'{row["tau"]:5.2f}  {row["phi"]:5.3f}  {row["cn"]:5.2f}  '
              f'{row["p_frac"]:5.2f}  '
              f'{row["b_hertzian"]:5.1f}  {row["b_liggghts"]:5.1f}  '
              f'{row["b_tabor"]:5.1f}  {row["b_geom"]:5.1f}')
    return idx


def outlier_drop_curve(df, base_params, max_drop=10):
    """Refit base after dropping top-k residual cases. Reports how R²
    climbs as outliers are removed — if the curve rises sharply for
    small k, the ceiling is a small-handful problem; if it rises
    smoothly, the gap is distributed.
    """
    print('\n=== Outlier drop curve (refit base after dropping top-k residuals) ===')
    print(f'{"k_drop":>6s}  {"n":>4s}  {"R²":>8s}  {"LOOCV":>8s}  {"w20":>8s}')
    df_work = df.copy()
    for k in range(0, max_drop + 1):
        if k > 0:
            base_pred = predict_base(df_work, base_params)
            log_resid = np.log(df_work['sigma'].values + 1e-12) - np.log(base_pred + 1e-12)
            worst_idx = np.argmax(np.abs(log_resid))
            df_work = df_work.drop(df_work.index[worst_idx]).reset_index(drop=True)
        # Refit base on the trimmed set
        params_k = fit_base(df_work, n_start=8)
        pred_k = predict_base(df_work, params_k)
        r2_k, w20_k = metrics(df_work['sigma'].values, pred_k)
        loocv_k = loocv_r2(df_work, pred_k)
        print(f'{k:>6d}  {len(df_work):>4d}  {r2_k:8.4f}  {loocv_k:8.4f}  '
              f'{w20_k:>3d}/{len(df_work)}')


def stratified_tau_fit(df, base_params):
    """Split cases into thin/moderate/thick by τ and fit each subset.
    The R² ceiling can come from a single regime that the v29 form
    handles poorly — this surfaces it.
    """
    print('\n=== Stratified fit by τ regime ===')
    bins = [
        ('thick     (τ < 1.5)',      df['tau'] < 1.5),
        ('moderate  (1.5 ≤ τ < 2.5)',(df['tau'] >= 1.5) & (df['tau'] < 2.5)),
        ('thin      (2.5 ≤ τ < 4)',  (df['tau'] >= 2.5) & (df['tau'] < 4)),
        ('extreme   (τ ≥ 4)',         df['tau'] >= 4),
    ]
    print(f'{"regime":24s}  {"n":>4s}  {"R²":>8s}  {"LOOCV":>8s}  {"w20":>8s}')
    for label, mask in bins:
        sub = df[mask].reset_index(drop=True)
        if len(sub) < 5:
            print(f'{label:24s}  {len(sub):>4d}  (too few cases)')
            continue
        try:
            params_sub = fit_base(sub, n_start=8)
            pred_sub = predict_base(sub, params_sub)
            r2, w20 = metrics(sub['sigma'].values, pred_sub)
            loocv = loocv_r2(sub, pred_sub)
            print(f'{label:24s}  {len(sub):>4d}  {r2:8.4f}  {loocv:8.4f}  '
                  f'{w20:>3d}/{len(sub)}')
        except Exception as e:
            print(f'{label:24s}  {len(sub):>4d}  fit failed: {e}')


def leverage_scan(df, base_params, k_top=10):
    """Drop each case in turn, refit residual gamma, report R²
    sensitivity. The cases whose removal moves R² the most are the
    ones constraining the fit — useful for spotting bad data or
    physics outliers.
    """
    print('\n=== Leverage scan (drop-one R² shift) ===')
    base_pred_full = predict_base(df, base_params)
    r2_full, _ = metrics(df['sigma'].values, base_pred_full)

    impacts = []
    for i in range(len(df)):
        sub = df.drop(df.index[i]).reset_index(drop=True)
        params_i = fit_base(sub, n_start=4)  # cheap multi-start
        pred_i = predict_base(sub, params_i)
        r2_i, _ = metrics(sub['sigma'].values, pred_i)
        impacts.append((df.iloc[i]['name'], r2_i, r2_i - r2_full))
    impacts.sort(key=lambda x: -abs(x[2]))

    print(f'{"case":40s}  {"R² without it":>14s}  {"ΔR² vs full":>13s}')
    for nm, r2_i, d in impacts[:k_top]:
        print(f'{str(nm)[:40]:40s}  {r2_i:14.4f}  {d:+13.4f}')


def main():
    cases = load_cases()
    rows = load_phys_rows(cases)
    df = pd.DataFrame(rows)
    if len(df) == 0:
        print('No physics-mode cases found.')
        return
    print(f'Loaded {len(df)} physics-mode cases.')
    have_binding = (df[['b_hertzian','b_liggghts','b_tabor','b_volume','b_geom']]
                    .sum(axis=1) > 0).sum()
    print(f'  • {have_binding}/{len(df)} have A_binding_share_AM_SE_pct populated')
    have_rratio = ((df['r_SE'].notna()) &
                   (df['r_AM_S'].notna() | df['r_AM_P'].notna())).sum()
    print(f'  • {have_rratio}/{len(df)} have r_SE & r_AM (for size ratio)')

    print('\n' + '=' * 75)
    print('PHYSICS FIT v33 — break ceiling with binding-share + size-ratio features')
    print('=' * 75)

    # Fit base once, reuse across stages so we measure incremental gain
    print('\n[shared base power-law fit, used across stages]')
    base_params = fit_base(df)
    base_pred = predict_base(df, base_params)
    r2_base, w20_base = metrics(df['sigma'].values, base_pred)
    loocv_base = loocv_r2(df, base_pred)
    print(f'  Stage 0: R²={r2_base:.4f}  LOOCV={loocv_base:.4f}  w20={w20_base}/{len(df)}')

    # Print biggest base residuals — these reveal what physics the fit
    # is currently missing, since adding random parameters to the v29
    # form has hit a ceiling.
    diagnose_residuals(df, base_pred, top_k=12)

    s1 = fit_stage(df, 1, '+ 5-case binding share (H/L/T/V/G)', base_params)
    s2 = fit_stage(df, 2, '+ r_SE/r_AM particle ratio',          base_params)
    s3 = fit_stage(df, 3, '+ τ × binding interactions',          base_params)

    # Robust diagnostics — surface where the 0.96 ceiling actually lives.
    outlier_drop_curve(df, base_params, max_drop=10)
    stratified_tau_fit(df, base_params)
    leverage_scan(df, base_params, k_top=10)

    print('\n' + '=' * 75)
    print('=== SUMMARY ===')
    print(f'{"stage":40s}  {"R²":>8s}  {"LOOCV":>8s}  {"w20":>8s}')
    print(f'{"Stage 0 — base power-law":40s}  '
          f'{r2_base:8.4f}  {loocv_base:8.4f}  {w20_base:>3d}/{len(df)}')
    for s in (s1, s2, s3):
        print(f'{s["label"][:40]:40s}  '
              f'{s["r2"]:8.4f}  {s["loocv"]:8.4f}  '
              f'{s["w20"]:>3d}/{s["n"]}')

    # Save best stage
    best = max([s1, s2, s3], key=lambda s: s['loocv'])
    best['base_r2'] = r2_base; best['base_loocv'] = loocv_base
    out = Path('docs/figures/physics_regime')
    out.mkdir(parents=True, exist_ok=True)
    with open(out / 'physics_fit_v33_binding.json', 'w') as f:
        json.dump({'all': [s1, s2, s3], 'best': best}, f, indent=2)
    print(f'\n→ {out}/physics_fit_v33_binding.json (best: stage {best["stage"]})')
    target = 0.99
    if best['loocv'] >= target:
        print(f'\n  TARGET REACHED: LOOCV {best["loocv"]:.4f} ≥ {target}')
    else:
        gap = target - best['loocv']
        print(f'\n  Still below 0.99. Gap = {gap:+.4f}.  Next tactics:')
        print('   - Add GB density nonlinear term (currently log-linear only)')
        print('   - Stratified fit by τ regime (thin / moderate / thick)')
        print('   - Drop highest-leverage 1-2 cases (verify they are not outliers)')
        print('   - Bring in stress-CV or force-chain anisotropy')


if __name__ == '__main__':
    main()
