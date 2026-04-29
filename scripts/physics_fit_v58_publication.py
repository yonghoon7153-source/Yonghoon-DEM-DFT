#!/usr/bin/env python3
"""Physics-mode v58 — publication analysis pipeline.

Combines four deliverables:
  E. σ_constr_net extraction from per-case network_conductivity.json
     → 3-way decomposition: σ_P / σ_bulk_H = (σ_P/σ_constr_H) × (σ_constr_H/σ_bulk_H)
  F. γ universal scaling visualisation (γ vs (φ-φc)·CN per batch)
  G. Multi-mode joint fit predicted-vs-actual scatter plots
  H. (Paper draft saved separately as PAPER_DRAFT.md)

Outputs four publication-grade PNG figures:
  fig1_v29_predicted_vs_actual.png       (main scaling law performance)
  fig2_gamma_universal.png               (γ vs <(φ-φc)·CN> per batch + fitted curve)
  fig3_three_way_decomposition.png       (σ_P/σ_bulk_H decomposed into two factors)
  fig4_multimode_joint.png               (3 modes scatter + per-mode R²)

All figures publication-grade (300 dpi, vector-friendly fonts).
"""
from __future__ import annotations
import sys, json, warnings
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
from physics_fit_v33_binding import load_phys_rows  # noqa: E402
from v32_exhaustive_refit import load_cases  # noqa: E402
from physics_fit_v53_lasso import enrich_full        # noqa: E402

WEBAPP = SCRIPTS.parent / 'webapp'
warnings.filterwarnings('ignore')
plt.rcParams.update({'font.size': 11, 'figure.dpi': 100,
                     'savefig.dpi': 300, 'savefig.bbox': 'tight'})


def extract_sigma_constr(df):
    """Extract sigma_constr_net_mScm per case from network_conductivity*.json."""
    print('\n— E1: Extracting σ_constr_net per case —', flush=True)
    sigma_constr = []
    for cid in df['case_id'].values:
        nc_path = None
        for base in ('webapp/results', 'webapp/archive'):
            for p in Path(base).rglob(f'{cid}/network_conductivity*.json'):
                nc_path = p; break
            if nc_path: break
        v = None
        if nc_path:
            try:
                m = json.load(open(nc_path))
                # Prefer the dict structure from dual or direct mScm key
                if 'hertzian' in m and isinstance(m['hertzian'], dict):
                    v = m['hertzian'].get('sigma_constr_net_mScm') or \
                        m['hertzian'].get('sigma_constr_mScm')
                if v is None:
                    v = m.get('sigma_constr_net_mScm') or m.get('sigma_constr_mScm')
            except Exception:
                pass
        sigma_constr.append(float(v) if v else np.nan)
    df['sigma_constr_H'] = sigma_constr
    n_have = int(np.sum(~np.isnan(sigma_constr)))
    print(f'  Got σ_constr_net for {n_have}/{len(df)} cases', flush=True)
    if n_have > 0:
        valid = np.array([v for v in sigma_constr if not np.isnan(v)])
        print(f'  range: {valid.min():.4f} – {valid.max():.4f} mS/cm', flush=True)
    return df


# ─────────────────────────────────────────────────────────────────────
# Figure 1: v29 predicted-vs-actual (main scaling-law figure)
# ─────────────────────────────────────────────────────────────────────
def make_fig1_v29_scatter(df, out_path):
    """Use v29's well-known LOOCV R²=0.90 numbers; here we visualise
    σ_P (actual) vs σ_v29-style prediction. We use a simplified
    canonical Bruggeman form for visualisation since v29's full form
    requires extra C_blend/C_corr coefs not loaded here.
    """
    print('\n— F: Figure 1 (v29 predicted vs actual) —', flush=True)
    SIGMA_GRAIN = 3.0; PHI_C = 0.20
    excess = np.maximum(df['phi'].values - PHI_C, 1e-6)
    canonical = (SIGMA_GRAIN
                 * (excess ** 0.5)
                 * (df['cn'].values ** 1.5)
                 * (df['cov_phys'].values ** 0.4)
                 * (df['f_perc'].values ** 3)
                 / (df['tau'].values ** 2))
    log_sigma = np.log(np.maximum(df['sigma'].values, 1e-12))
    log_canon = np.log(np.maximum(canonical, 1e-12))
    log_C = float(np.mean(log_sigma - log_canon))
    pred = np.exp(log_C) * canonical
    actual = df['sigma'].values

    fig, ax = plt.subplots(figsize=(6.5, 6))
    ax.loglog([1e-3, 2], [1e-3, 2], 'k--', alpha=0.4, label='1:1')
    band20 = np.array([1e-3, 2])
    ax.fill_between(band20, band20 * 0.8, band20 * 1.2, color='green',
                    alpha=0.15, label='±20% band')
    name = df['name'].astype(str)
    colors = {'1mAh': '#1f77b4', '6mAh': '#2ca02c', '8mAh': '#d62728',
              'particulate': '#ff7f0e', 'other': 'gray'}
    for label, color in colors.items():
        mask = name.str.contains(label, case=False, na=False).values \
            if label != 'other' else \
            ~np.any([name.str.contains(b, case=False, na=False).values
                     for b in ['1mAh', '6mAh', '8mAh', 'particulate']], axis=0)
        if mask.sum():
            ax.scatter(actual[mask], pred[mask], c=color, s=60,
                       alpha=0.7, edgecolor='k', linewidth=0.5,
                       label=f'{label} (n={mask.sum()})')
    ax.set_xlabel('σ_P actual (mS/cm)')
    ax.set_ylabel('σ_P predicted (canonical v29 form, mS/cm)')
    err = np.abs(actual - pred) / np.maximum(actual, 1e-12)
    w20 = int(np.sum(err <= 0.20))
    ss_res = np.sum((log_sigma - log_canon - log_C) ** 2)
    ss_tot = np.sum((log_sigma - log_sigma.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot
    ax.set_title(
        f'v29 canonical form on physics-mode data\n'
        f'C={np.exp(log_C):.4f}, R²={r2:.3f}, ±20%: {w20}/{len(df)}',
        fontsize=11)
    ax.legend(loc='lower right', fontsize=9)
    ax.set_xlim(1e-3, 2); ax.set_ylim(1e-3, 2)
    ax.grid(alpha=0.3)
    plt.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f'  → {out_path}', flush=True)


# ─────────────────────────────────────────────────────────────────────
# Figure 2: γ universal scaling
# ─────────────────────────────────────────────────────────────────────
def make_fig2_gamma_universal(df, out_path):
    print('\n— F: Figure 2 (γ universal scaling) —', flush=True)
    log_P = np.log(np.maximum(df['sigma'].values, 1e-12))
    log_H = np.log(np.maximum(df['sigma_H'].values, 1e-6))
    name = df['name'].astype(str)
    PHI_C = 0.20

    fig, ax = plt.subplots(figsize=(7, 5.5))
    batches = [('1mAh', '#1f77b4'), ('6mAh', '#2ca02c'),
               ('8mAh', '#d62728'), ('particulate', '#ff7f0e')]
    points_x, points_y = [], []
    for b, c in batches:
        m = name.str.contains(b, case=False, na=False).values
        if m.sum() < 3: continue
        x = log_H[m]; y = log_P[m]
        gam = float(np.sum((x - x.mean()) * (y - y.mean())) /
                    np.sum((x - x.mean()) ** 2))
        sub = df[m]
        excess = np.maximum(sub['phi'].values - PHI_C, 1e-6)
        feat = np.log(excess) * np.log(np.maximum(sub['cn'].values, 1e-3))
        feat_mean = float(np.mean(feat))
        ax.scatter(feat_mean, gam, c=c, s=200, edgecolor='k',
                   linewidth=1.2, label=f'{b} (n={m.sum()})')
        points_x.append(feat_mean); points_y.append(gam)
        ax.annotate(f'  γ={gam:.3f}', (feat_mean, gam),
                    fontsize=9, va='center')

    px = np.array(points_x); py = np.array(points_y)
    if len(px) >= 3:
        slope = float(np.sum((px - px.mean()) * (py - py.mean())) /
                       np.sum((px - px.mean()) ** 2))
        intc = float(py.mean() - slope * px.mean())
        xs = np.linspace(px.min() - 0.3, px.max() + 0.3, 100)
        ax.plot(xs, slope * xs + intc, 'k--', alpha=0.6,
                label=f'γ = {slope:+.3f}·⟨(φ-φc)·CN⟩ + {intc:+.3f}')
        pred = slope * px + intc
        r2 = 1 - np.sum((py - pred) ** 2) / np.sum((py - py.mean()) ** 2)
        ax.text(0.02, 0.97,
                f'σ_P = C · σ_H^γ\nR² = {r2:.3f} (per-batch γ regression)',
                transform=ax.transAxes, va='top', fontsize=10,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))

    ax.axhline(1.0, color='gray', linestyle=':', alpha=0.5,
               label='γ=1 (linear σ_P=σ_H)')
    ax.set_xlabel('Batch-mean ⟨log(φ-φc) · log(CN)⟩')
    ax.set_ylabel('Fitted γ in σ_P = C · σ_H^γ')
    ax.set_title('Cross-mode scaling exponent γ varies with regime feature')
    ax.legend(loc='lower right', fontsize=9)
    ax.grid(alpha=0.3)
    plt.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f'  → {out_path}', flush=True)


# ─────────────────────────────────────────────────────────────────────
# Figure 3: 3-way decomposition
# ─────────────────────────────────────────────────────────────────────
def make_fig3_three_way(df, out_path):
    print('\n— E: Figure 3 (3-way decomposition) —', flush=True)
    if 'sigma_constr_H' not in df.columns or df['sigma_constr_H'].isna().all():
        print('  ⚠ sigma_constr_H not extracted, skip', flush=True)
        return
    valid = df.dropna(subset=['sigma_constr_H']).copy()
    valid = valid[valid['sigma_constr_H'] > 0]
    valid = valid[valid['sigma_bulk_H'] > 0]
    valid['ratio_total'] = valid['sigma'] / valid['sigma_bulk_H']
    valid['ratio_PvC']   = valid['sigma'] / valid['sigma_constr_H']
    valid['ratio_CvB']   = valid['sigma_constr_H'] / valid['sigma_bulk_H']
    print(f'  n={len(valid)} cases with all three σ values', flush=True)
    print(f'  σ_P/σ_bulk_H:     median {valid["ratio_total"].median():.4f}', flush=True)
    print(f'  σ_P/σ_constr_H:   median {valid["ratio_PvC"].median():.4f}', flush=True)
    print(f'  σ_constr/σ_bulk_H: median {valid["ratio_CvB"].median():.4f}', flush=True)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    name = valid['name'].astype(str)
    colors = {'1mAh': '#1f77b4', '6mAh': '#2ca02c', '8mAh': '#d62728',
              'particulate': '#ff7f0e'}
    for ax, col, title, xlabel in [
        (axes[0], 'ratio_total', 'σ_P / σ_bulk_H\n(total constriction loss)',
         'σ_P / σ_bulk_H'),
        (axes[1], 'ratio_PvC',   'σ_P / σ_constr_H\n(plastic vs Hertzian constr.)',
         'σ_P / σ_constr_H'),
        (axes[2], 'ratio_CvB',   'σ_constr_H / σ_bulk_H\n(pure Hertzian constr. loss)',
         'σ_constr_H / σ_bulk_H'),
    ]:
        for b, c in colors.items():
            m = name.str.contains(b, case=False, na=False).values
            if m.sum() == 0: continue
            ax.hist(valid[col].values[m], bins=15, alpha=0.5, color=c,
                    label=b, edgecolor='k', linewidth=0.3)
        med = valid[col].median()
        ax.axvline(med, color='red', linestyle='--',
                   label=f'median {med:.3f}')
        ax.set_xlabel(xlabel); ax.set_ylabel('count')
        ax.set_title(title)
        ax.legend(fontsize=8); ax.grid(alpha=0.3)
    fig.suptitle('Three-way decomposition of plastic constriction penalty',
                  fontsize=13, y=1.02)
    plt.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f'  → {out_path}', flush=True)


# ─────────────────────────────────────────────────────────────────────
# Figure 4: Multi-mode joint fit
# ─────────────────────────────────────────────────────────────────────
def make_fig4_multimode(df, out_path):
    print('\n— G: Figure 4 (multi-mode joint fit) —', flush=True)
    log_P  = np.log(np.maximum(df['sigma'].values, 1e-12))
    log_H  = np.log(np.maximum(df['sigma_H'].values, 1e-6))
    log_bH = np.log(np.maximum(df['sigma_bulk_H'].values, 1e-6))
    PHI_C = 0.20
    excess = np.maximum(df['phi'].values - PHI_C, 1e-6)
    log_excess = np.log(excess)
    log_CN = np.log(np.maximum(df['cn'].values, 1e-3))
    log_cov = np.log(np.maximum(df['cov_phys'].values, 1e-3))
    log_f_p = np.log(np.maximum(df['f_perc'].values, 1e-3))
    log_tau = np.log(np.maximum(df['tau'].values, 1e-3))
    log_thick = np.log(np.maximum(df['thickness'].values, 1.0))
    porosity = df['porosity'].values / 100.0

    feats = np.column_stack([log_excess, log_CN, log_cov, log_f_p, log_tau,
                              log_thick, porosity,
                              log_excess * log_CN, log_tau * log_thick, log_tau ** 2])
    n = len(df)
    Xs = []; ys = []; mids = []
    for mid, target in [(0, log_P), (1, log_H), (2, log_bH)]:
        dummies = np.zeros((n, 3)); dummies[:, mid] = 1.0
        Xs.append(np.column_stack([feats, dummies]))
        ys.append(target)
        mids.extend([mid] * n)
    X = np.vstack(Xs); y = np.concatenate(ys); mids = np.array(mids)
    Xstd = (X - X.mean(0)) / (X.std(0) + 1e-9)

    from sklearn.linear_model import LassoCV
    lcv = LassoCV(cv=5, max_iter=20000, n_alphas=80, fit_intercept=True,
                  random_state=42)
    lcv.fit(Xstd, y); pred = Xstd @ lcv.coef_ + lcv.intercept_

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    titles = ['σ_P (Physics)', 'σ_H (Hertzian)', 'σ_bulk_H (no constr.)']
    for mid, ax, title in zip([0, 1, 2], axes, titles):
        m = (mids == mid)
        a = np.exp(y[m]); p = np.exp(pred[m])
        ss_r = np.sum((y[m] - pred[m]) ** 2)
        ss_t = np.sum((y[m] - y[m].mean()) ** 2)
        r2 = 1 - ss_r / ss_t
        ax.loglog([1e-3, 2], [1e-3, 2], 'k--', alpha=0.4)
        band = np.array([1e-3, 2])
        ax.fill_between(band, band * 0.8, band * 1.2,
                        color='green', alpha=0.15)
        ax.scatter(a, p, c='steelblue', s=40, alpha=0.7,
                   edgecolor='k', linewidth=0.4)
        ax.set_xlabel(f'{title} actual (mS/cm)')
        ax.set_ylabel(f'{title} predicted (joint fit, mS/cm)')
        ax.set_title(f'{title}\nR² = {r2:.3f}')
        ax.set_xlim(1e-3, 2); ax.set_ylim(1e-3, 2); ax.grid(alpha=0.3)
    fig.suptitle('Multi-mode joint Lasso fit (shared structural backbone)',
                  fontsize=13, y=1.02)
    plt.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f'  → {out_path}', flush=True)


def main():
    cases = load_cases()
    rows = enrich_full(load_phys_rows(cases))
    df = pd.DataFrame(rows)
    print(f'Loaded {len(df)} cases.', flush=True)

    df = extract_sigma_constr(df)

    out = Path('docs/figures/physics_regime')
    out.mkdir(parents=True, exist_ok=True)

    make_fig1_v29_scatter(df, out / 'fig1_v29_predicted_vs_actual.png')
    make_fig2_gamma_universal(df, out / 'fig2_gamma_universal.png')
    make_fig3_three_way(df, out / 'fig3_three_way_decomposition.png')
    make_fig4_multimode(df, out / 'fig4_multimode_joint.png')

    # Save extracted data
    save_df = df[['case_id', 'name', 'sigma', 'sigma_H', 'sigma_bulk_H',
                   'sigma_constr_H']].copy()
    save_df.to_csv(out / 'sigma_three_modes.csv', index=False)
    print(f'\n→ {out}/sigma_three_modes.csv', flush=True)
    print(f'\n=== All four publication figures generated ===', flush=True)
    print(f'Output dir: {out}', flush=True)


if __name__ == '__main__':
    main()
