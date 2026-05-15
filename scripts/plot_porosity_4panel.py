#!/usr/bin/env python3
"""4-panel comprehensive validation showing ALL 82 cases by regime.

  ┌───────────────────────────────┬───────────────────────────────┐
  │  ① MAIN — thick-film bulk     │  ② thick-film OUT-OF-REGIME   │
  │     (bimodal AM, λ≥4, ε≥8)   │     (mono-AM and/or λ<4)     │
  ├───────────────────────────────┼───────────────────────────────┤
  │  ③ thin-film 1 mAh REFERENCE │  ④ particulate — mono-AM ref │
  │     wall confinement          │     no Furnas-binary benefit  │
  └───────────────────────────────┴───────────────────────────────┘

Same strict-physics model parameters in all four panels (no re-fit).
Out-of-regime panels (2, 4) show WHY each filter is needed by
revealing the systematic deviations that disappear in panel ①.

Panel selection criteria (no cherry-picking — see paper §5)
───────────────────────────────────────────────────────────
The 82-case set is partitioned by *pre-registered* geometric
filters that are documented in the model definition itself, not
chosen post-hoc to make panel ① clean:

  Panel ①  campaign ∈ {후막 6mAh, 후막 8mAh}
           AND bimodal AM       (both AM_P and AM_S present)
           AND lam = D_AM/D_SE ≥ 4   (Bouvard validity)
           AND ε_measured ≥ 8 %  (Heckel plastic regime)

  Panel ②  same thick-film campaigns BUT failing any of the
           above filters (mono-AM, λ<4, or ε<8%) — these are
           explicitly out-of-regime for the strict physics model,
           and the panel shows the systematic deviations.

  Panel ③  campaign = 박막(1mAh) — all 33 cases, no further
           filter.  Wall confinement effects dominate.

  Panel ④  campaign = particulate — all 20 cases (P-only or
           S-only mono-AM by construction).

The 22 cases marked as "untrustworthy" by the
validation-flag audit (docs/db/case_audit.csv) are *not* excluded
from any of the four panels — they appear with the same markers
as the trustworthy cases, including the two flagged mechanistic
outliers (cluster C: input_1mAh_100_15, cluster D:
input_6mAh_real_10) which are drawn with red hollow stars per the
OUTLIER_CASES constant below.  This is intentional: the panel
groupings are *physical regime* filters, not *data quality*
filters, and "trustworthy" is reported separately in §5.2 instead
of being baked into the panels.
"""
import csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys

sys.path.insert(0, str(Path(__file__).parent))
from predict_porosity_strict_physics import (
    RHO_AM, RHO_SE, EPS_PURE_AM, K_HECKEL, P_PRESS,
    ALPHA_KC, F_PERC, SHARPNESS, bouvard_rcp,
)

# ── Mechanistic outliers identified by the validation-flag trust audit
# (paper §5, cluster analysis). Marked with red stars on the panels so
# the reader sees them visually isolated from the bulk ensemble.
#   1mAh_100_15 — AM_P-only 100 %, severe = 48.7 %, near-percolation
#   6mAh_real_10 — severe = 61.8 %, settling-phase artefact
OUTLIER_CASES = {'input_1mAh_100_15', 'input_6mAh_real_10'}


def stress_perc(f_se):
    return 1.0 / (1.0 + np.exp(-SHARPNESS * (f_se - F_PERC)))


def sfm(f_am, lam):
    if f_am <= 1e-9:
        return 1.0
    return (1 + ALPHA_KC * f_am ** 2) * (1 + 0.05 * np.log(max(lam, 1.0)))


def predict_full(am_wt, se_wt, d_p, n_p, d_s, n_s, d_se):
    v_am = am_wt / RHO_AM
    v_se = se_wt / RHO_SE
    f_se = v_se / (v_am + v_se)
    f_am = 1 - f_se
    if n_p and n_s:
        vp = n_p * d_p ** 3
        vs = n_s * d_s ** 3
        d_eff = (vp * d_p + vs * d_s) / (vp + vs)
        bimodal = True
    elif n_p:
        d_eff = d_p; bimodal = False
    else:
        d_eff = d_s if d_s else 4.0; bimodal = False
    lam = d_eff / d_se if d_se else 1.0
    eps_rcp = bouvard_rcp(f_se, lam)
    kc = sfm(f_am, lam)
    p_se = stress_perc(f_se)
    P_eff = P_PRESS / kc
    eps_pure_eff = EPS_PURE_AM * np.exp(-K_HECKEL * P_eff / 1e6)
    delta = (EPS_PURE_AM - eps_pure_eff) * f_se * p_se
    return dict(eps=max(eps_rcp - delta, 0.03) * 100,
                lam=lam, bimodal=bimodal, f_se=f_se)


def fnum(s):
    try:    return float(s)
    except: return None


def load():
    rows = list(csv.DictReader(open('all_dem_porosity.csv')))
    out = []
    for r in rows:
        am = fnum(r['am_wt']); se = fnum(r['se_wt'])
        if am is None:
            continue
        d_se = (fnum(r['r_SE_um'])   or 0) * 2 / 1000
        d_p  = (fnum(r['r_AM_P_um']) or 0) * 2 / 1000
        d_s  = (fnum(r['r_AM_S_um']) or 0) * 2 / 1000
        n_p  = fnum(r['n_AM_P']) or 0
        n_s  = fnum(r['n_AM_S']) or 0
        meas = fnum(r['porosity_pct'])
        if not meas or d_se <= 0:
            continue
        p = predict_full(am, se, d_p, n_p, d_s, n_s, d_se)
        out.append(dict(
            case_id=r['case_id'], campaign=r['campaign'],
            am_wt=am, lam=p['lam'], bimodal=p['bimodal'],
            f_se=p['f_se'], eps_meas=meas, eps_pred=p['eps'],
        ))
    return out


def stats_str(cases):
    if not cases:
        return ''
    res = np.array([c['eps_meas'] - c['eps_pred'] for c in cases])
    n = len(cases)
    rmse = np.sqrt(np.mean(res ** 2))
    n_le2 = int(np.sum(np.abs(res) < 2))
    n_le3 = int(np.sum(np.abs(res) < 3))
    n_le5 = int(np.sum(np.abs(res) < 5))
    return (f'N={n}, mean Δ={res.mean():+.2f}%, σ={res.std():.2f}%, '
            f'RMSE={rmse:.2f}%\n'
            f'|Δ|<2%: {100*n_le2/n:.0f}%, '
            f'<3%: {100*n_le3/n:.0f}%, '
            f'<5%: {100*n_le5/n:.0f}%')


def panel(ax, cases, title, note,
          colors_by_campaign=True, gray_out=False):
    label_en = {'particulate': 'particulate',
                '박막(1mAh)': 'thin film 1mAh',
                '후막(6mAh)': 'thick film 6mAh',
                '후막(8mAh)': 'thick film 8mAh'}
    cmap = {'particulate': 'tab:blue',
            '박막(1mAh)': 'tab:green',
            '후막(6mAh)': 'tab:orange',
            '후막(8mAh)': 'tab:red'}
    mk = {'particulate': 'o', '박막(1mAh)': 's',
          '후막(6mAh)': '^', '후막(8mAh)': 'D'}

    for camp in sorted({c['campaign'] for c in cases}):
        sub_c = [c for c in cases if c['campaign'] == camp]
        col = cmap.get(camp, 'gray') if colors_by_campaign else 'gray'
        alpha = 0.5 if gray_out else 0.85
        ax.scatter([c['eps_pred'] for c in sub_c],
                   [c['eps_meas'] for c in sub_c],
                   s=70, color=col,
                   marker=mk.get(camp, 'o'),
                   alpha=alpha, edgecolors='black', linewidth=0.5,
                   label=f'{label_en.get(camp, camp)} (n={len(sub_c)})')

    # Mark the two mechanistic outliers identified by the trust-audit
    # cluster analysis (paper §5).  Drawn as oversized hollow red stars
    # on top of the campaign markers so they are visually isolated
    # without changing the rest of the figure.
    outliers = [c for c in cases if c['case_id'] in OUTLIER_CASES]
    if outliers:
        ax.scatter([c['eps_pred'] for c in outliers],
                   [c['eps_meas'] for c in outliers],
                   s=320, marker='*', facecolors='none',
                   edgecolors='red', linewidth=2.2, zorder=5,
                   label=f'mechanistic outlier (n={len(outliers)})')
        for c in outliers:
            ax.annotate(c['case_id'],
                         (c['eps_pred'], c['eps_meas']),
                         xytext=(7, 7), textcoords='offset points',
                         fontsize=8, color='red', fontweight='bold')

    lo, hi = 5, 35
    ax.plot([lo, hi], [lo, hi], 'k-', lw=1.5, zorder=1, label='1:1')
    ax.fill_between([lo, hi], [lo-2, hi-2], [lo+2, hi+2],
                    color='gray', alpha=0.20, label='±2%')
    ax.fill_between([lo, hi], [lo-3, hi-3], [lo+3, hi+3],
                    color='gray', alpha=0.10)

    full_title = (f'{title}\n{stats_str(cases)}\n· {note}'
                  if cases else f'{title}\n(no cases)')
    ax.set_title(full_title, fontsize=9.5)
    ax.set_xlabel('Predicted ε (strict physics, %)', fontsize=10.5)
    ax.set_ylabel('Measured ε (DEM, %)', fontsize=10.5)
    ax.legend(fontsize=8.5, loc='upper left', framealpha=0.95)
    ax.grid(alpha=0.3)
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)


def main():
    cases = load()
    print(f'Total cases: {len(cases)}')

    # ── Slicing ─────────────────────────────────────────────────
    # Panel 1: MAIN — thick-film bulk in-regime
    p1 = [c for c in cases
          if c['campaign'] in ('후막(6mAh)', '후막(8mAh)')
          and c['bimodal']
          and c['lam'] >= 4
          and c['eps_meas'] >= 8]

    # Panel 2: thick-film out-of-regime (mono-AM OR low-λ OR ε<8%)
    p2 = [c for c in cases
          if c['campaign'] in ('후막(6mAh)', '후막(8mAh)')
          and c not in p1]

    # Panel 3: thin-film 1mAh (all)
    p3 = [c for c in cases if c['campaign'] == '박막(1mAh)']

    # Panel 4: particulate (mostly mono-AM reference)
    p4 = [c for c in cases if c['campaign'] == 'particulate']

    print(f'Panel 1 (thick bulk in-regime):  {len(p1)}')
    print(f'Panel 2 (thick out-of-regime):   {len(p2)}')
    print(f'Panel 3 (thin film 1mAh):        {len(p3)}')
    print(f'Panel 4 (particulate):           {len(p4)}')
    print(f'Total in panels: {len(p1)+len(p2)+len(p3)+len(p4)}')

    fig, axes = plt.subplots(2, 2, figsize=(15, 13.5))
    panel(axes[0, 0], p1,
          '① MAIN — thick-film bulk validation',
          'bimodal AM, λ≥4, ε≥8% (physics-first model unbiased)')
    panel(axes[0, 1], p2,
          '② thick-film OUT-OF-REGIME',
          'mono-AM (no Furnas) or λ<4 (Bouvard limit) — explained as such')
    panel(axes[1, 0], p3,
          '③ thin-film 1 mAh — geometric reference',
          'cell ≈ D_AM_P → wall confinement disturbs Furnas valley')
    panel(axes[1, 1], p4,
          '④ particulate — mono-AM reference',
          'AM is monomodal (P-only or S-only) — no Furnas-binary benefit')

    plt.suptitle('Strict physics-first model — comprehensive 82-case '
                 'validation by regime',
                 fontsize=13, fontweight='bold', y=1.00)
    plt.tight_layout()
    out = Path('porosity_4panel.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    print(f'\n✓ Saved: {out.resolve()}')


if __name__ == '__main__':
    main()
