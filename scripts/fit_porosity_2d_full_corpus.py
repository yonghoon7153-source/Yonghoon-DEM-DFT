#!/usr/bin/env python3
"""Full-corpus 2D porosity surface fit ε(AM_wt, λ_eff).

Extends the 10-point particulate fit to the full 82-case ensemble
(particulate + 박막 1mAh + 후막 6mAh + 후막 8mAh) by reducing the
4-particle-class system to a 2D (AM_wt, λ_eff) input:

    r_AM_eff  =  (V_P · r_AM_P + V_S · r_AM_S) / (V_P + V_S)
    λ_eff     =  r_AM_eff / r_SE

The 2-regime model is the same as fit_porosity_2d_surface.py:

    ε(f_AM, λ) = w(f_AM, λ) · ε_Furnas(f_AM, λ)
               + (1 - w(f_AM, λ)) · ε_matrix(f_AM, λ)
    w(f_AM, λ) = 1 - sigmoid(s · (f_AM - f_AM_perc(λ)))
    f_AM_perc(λ) = a + b · (1 - exp(-c · (λ-1)))

After fit, residuals are plotted vs P:S ratio + campaign to see if
the 2D reduction misses any P:S-specific physics.
"""
from __future__ import annotations
import csv
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import minimize


# ── Load all 82 cases ─────────────────────────────────────────────
ROWS = list(csv.DictReader(open('all_dem_porosity.csv')))

def fnum(s):
    try: return float(s)
    except: return None

DATA = []   # list of (f_AM, lam_eff, eps, campaign, ps_ratio, case_id)
for r in ROWS:
    am_wt = fnum(r['am_wt'])
    eps   = fnum(r['porosity_pct'])
    rse   = fnum(r['r_SE_um']) or 0
    rp    = fnum(r['r_AM_P_um']) or 0
    rs    = fnum(r['r_AM_S_um']) or 0
    pv    = fnum(r['p_vol']) or 0
    sv    = fnum(r['s_vol']) or 0
    if am_wt is None or eps is None or rse <= 0:
        continue
    # Volume-weighted effective AM radius
    if pv + sv > 0:
        # P:S given as volume ratio
        v_total = pv + sv
        r_am_eff = (pv * rp + sv * rs) / v_total
    elif rs > 0:
        r_am_eff = rs                                # particulate, AM_S only
    else:
        r_am_eff = rp                                # AM_P only
    if r_am_eff <= 0:
        continue
    lam_eff = r_am_eff / rse
    DATA.append((am_wt / 100.0, lam_eff, eps,
                  r['campaign'], pv, sv, r['case_id']))

print(f'Loaded {len(DATA)} cases')
print()
print('λ_eff distribution:')
lams = sorted(set(round(d[1], 2) for d in DATA))
from collections import Counter
lam_counts = Counter(round(d[1], 1) for d in DATA)
for lam in sorted(lam_counts):
    print(f'  λ_eff = {lam:5.1f}  →  {lam_counts[lam]:3d} cases')
print()

F_AM   = np.array([d[0] for d in DATA])
LAM    = np.array([d[1] for d in DATA])
EPS    = np.array([d[2] for d in DATA])
CAMP   = [d[3] for d in DATA]
PS_P   = np.array([d[4] for d in DATA])
PS_S   = np.array([d[5] for d in DATA])


# ── Model (same as 10-point version) ──────────────────────────────
def f_AM_perc(lam, a, b, c):
    return a + b * (1.0 - np.exp(-c * (lam - 1.0)))


def w_Furnas(f_AM, lam, a, b, c, s):
    fc = f_AM_perc(lam, a, b, c)
    return 1.0 / (1.0 + np.exp(s * (f_AM - fc)))


def eps_Furnas(f_AM, lam,
                eps_pure_am=36.0, eps_pure_se=10.0,
                valley_center=0.80, valley_depth_max=18.0,
                valley_width=0.20, lam_sat=8.0):
    linear = eps_pure_am * f_AM + eps_pure_se * (1.0 - f_AM)
    valley_strength = valley_depth_max * (1.0 - np.exp(-(lam - 1.0) / lam_sat))
    valley = valley_strength * np.exp(
        -((f_AM - valley_center) ** 2) / (2.0 * valley_width ** 2))
    return linear - valley


def eps_matrix(f_AM, lam, e0, k1, k2):
    slope = k1 + k2 / lam
    return (e0
            + slope * (f_AM - 0.62)
            + 50.0 * np.maximum(0, f_AM - 0.62) ** 2 * (1.0 / lam))


def model_eps(f_AM, lam, params):
    a_p, b_p, c_p, s_w, vd_max, vc, vw, e0_m, k1_m, k2_m = params
    w = w_Furnas(f_AM, lam, a_p, b_p, c_p, s_w)
    ef = eps_Furnas(f_AM, lam,
                     valley_center=vc, valley_depth_max=vd_max,
                     valley_width=vw)
    em = eps_matrix(f_AM, lam, e0_m, k1_m, k2_m)
    return w * ef + (1.0 - w) * em


def loss(params):
    pred = model_eps(F_AM, LAM, params)
    return float(np.sum((pred - EPS) ** 2))


P0 = [0.40, 0.50, 0.30, 25.0, 18.0, 0.80, 0.20, 6.0, 40.0, 30.0]
BOUNDS = [(0.30, 0.80), (0.05, 1.20), (0.02, 1.0), (3.0, 100.0),
          (5.0, 35.0), (0.50, 0.95), (0.05, 0.40),
          (3.0, 15.0), (5.0, 150.0), (-50.0, 100.0)]

res = minimize(loss, P0, method='L-BFGS-B', bounds=BOUNDS)
PARAMS = res.x
RMSE = math.sqrt(res.fun / len(DATA))

PARAM_NAMES = ['a_perc', 'b_perc', 'c_perc', 's_w',
               'valley_depth_max', 'valley_center', 'valley_width',
               'eps_matrix_0', 'k1_matrix', 'k2_matrix']

print('=' * 60)
print(f'82-CASE FULL ENSEMBLE FIT')
print('=' * 60)
print(f'RMSE: {RMSE:.3f} %p across {len(DATA)} cases')
print()
print('Fitted parameters:')
for name, val in zip(PARAM_NAMES, PARAMS):
    print(f'  {name:20s} = {val:8.3f}')

# Per-case prediction
pred = model_eps(F_AM, LAM, PARAMS)
resid = pred - EPS

print()
print('Residuals by campaign:')
for camp in sorted(set(CAMP)):
    idx = [i for i, c in enumerate(CAMP) if c == camp]
    rs = resid[idx]
    print(f'  {camp:15s}  n={len(idx):3d}  '
          f'RMSE={np.sqrt(np.mean(rs**2)):.2f} %p   '
          f'mean Δ={rs.mean():+.2f}%   '
          f'max |Δ|={np.max(np.abs(rs)):.2f}%')

# ── Plots ─────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(20, 5.5))

# --- LEFT: 2D heatmap ---
ax = axes[0]
lam_grid = np.logspace(np.log10(2), np.log10(25), 100)
fam_grid = np.linspace(0.50, 0.99, 100)
LL, FF = np.meshgrid(lam_grid, fam_grid)
ZZ = np.zeros_like(LL)
for i in range(LL.shape[0]):
    for j in range(LL.shape[1]):
        ZZ[i, j] = model_eps(np.array([FF[i, j]]),
                              np.array([LL[i, j]]), PARAMS)[0]
im = ax.contourf(LL, FF * 100, ZZ, levels=np.linspace(3, 35, 17),
                  cmap='viridis_r', extend='both')
plt.colorbar(im, ax=ax, label='ε predicted (%)')

# AM percolation onset curve
lam_curve = np.linspace(2, 25, 100)
fperc_curve = f_AM_perc(lam_curve, PARAMS[0], PARAMS[1], PARAMS[2])
fperc_curve = np.clip(fperc_curve, 0, 1)
ax.plot(lam_curve, fperc_curve * 100, 'w--', lw=2,
        label='AM percolation onset')

# Data points colored by campaign
camp_colors = {'particulate': '#d62728',
               '박막(1mAh)':  '#1f77b4',
               '후막(6mAh)':  '#ff7f0e',
               '후막(8mAh)':  '#2ca02c'}
camp_labels = {'particulate': 'particulate',
                '박막(1mAh)':  'thin film 1mAh',
                '후막(6mAh)':  'thick 6mAh',
                '후막(8mAh)':  'thick 8mAh'}
for camp in sorted(set(CAMP)):
    idx = [i for i, c in enumerate(CAMP) if c == camp]
    ax.scatter([LAM[i] for i in idx], [F_AM[i] * 100 for i in idx],
                c=camp_colors[camp], s=50, edgecolors='black',
                linewidths=0.7, label=f'{camp_labels[camp]} (n={len(idx)})',
                zorder=10)
ax.set_xscale('log')
ax.set_xticks([2, 3, 5, 7, 10, 15, 20])
ax.set_xticklabels(['2', '3', '5', '7', '10', '15', '20'])
ax.set_xlabel('λ_eff = r_AM_eff / r_SE')
ax.set_ylabel('AM weight fraction (%)')
ax.set_title(f'2D porosity surface ε(AM_wt, λ_eff)\n'
              f'fit to 82 DEM cases — RMSE {RMSE:.2f} %p')
ax.legend(loc='lower left', framealpha=0.92, fontsize=8.5)

# --- MIDDLE: parity plot ---
ax = axes[1]
for camp in sorted(set(CAMP)):
    idx = [i for i, c in enumerate(CAMP) if c == camp]
    ax.scatter(EPS[idx], pred[idx], c=camp_colors[camp],
                s=60, edgecolors='black', linewidths=0.7,
                label=f'{camp_labels[camp]}', zorder=5)
emin, emax = 3, 35
ax.plot([emin, emax], [emin, emax], 'k-', lw=1.5, label='1:1', zorder=1)
ax.fill_between([emin, emax], [emin-2, emax-2], [emin+2, emax+2],
                  color='gray', alpha=0.15, label='±2 %p')
ax.set_xlabel('Measured ε (DEM, %)')
ax.set_ylabel('Predicted ε (model, %)')
ax.set_title(f'Parity plot — 82 cases\n'
              f'|Δ|<2%p: {100*sum(abs(r)<2 for r in resid)/len(resid):.0f}%, '
              f'|Δ|<3%p: {100*sum(abs(r)<3 for r in resid)/len(resid):.0f}%')
ax.legend(loc='lower right', fontsize=8.5)
ax.set_xlim(emin, emax); ax.set_ylim(emin, emax)
ax.grid(alpha=0.3)

# --- RIGHT: residuals vs P:S ratio ---
ax = axes[2]
# P-fraction within AM = pv/(pv+sv)
ps_frac = np.array([
    PS_P[i] / (PS_P[i] + PS_S[i]) if (PS_P[i] + PS_S[i]) > 0 else 0
    for i in range(len(DATA))])
for camp in sorted(set(CAMP)):
    idx = [i for i, c in enumerate(CAMP) if c == camp]
    ax.scatter([ps_frac[i] for i in idx], [resid[i] for i in idx],
                c=camp_colors[camp], s=50, edgecolors='black',
                linewidths=0.7, label=f'{camp_labels[camp]}', zorder=5)
ax.axhline(0, color='k', lw=1.5)
ax.axhline(2, color='gray', lw=0.8, ls=':')
ax.axhline(-2, color='gray', lw=0.8, ls=':')
ax.set_xlabel('AM_P / (AM_P + AM_S) volume fraction within AM')
ax.set_ylabel('Residual (pred - meas) (%p)')
ax.set_title('Residual diagnostic — does 2D reduction miss P:S physics?\n'
              '(flat scatter = no P:S bias → 2D reduction OK)')
ax.legend(loc='lower right', fontsize=8.5)
ax.grid(alpha=0.3)

plt.tight_layout()
import os
os.makedirs('docs/figures', exist_ok=True)
out_png = 'docs/figures/porosity_2d_fit_full_corpus.png'
plt.savefig(out_png, dpi=140, bbox_inches='tight')
print(f'\nFigure saved: {out_png}')
print()
print('Top 10 worst predictions (by |Δ|):')
order = np.argsort(-np.abs(resid))[:10]
for i in order:
    print(f'  {DATA[i][6]:25s}  λ_eff={LAM[i]:5.2f}  '
          f'AM={F_AM[i]*100:5.1f}%  meas={EPS[i]:5.2f}%  '
          f'pred={pred[i]:5.2f}%  Δ={resid[i]:+5.2f}%p')
