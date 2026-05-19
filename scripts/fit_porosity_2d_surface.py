#!/usr/bin/env python3
"""2D porosity surface fit: ε(AM_wt, λ) for mono-AM particulate sweep.

Two-regime model with AM-percolation-based mixing:
  ε(f_AM, λ) = w(f_AM, λ) · ε_Furnas(f_AM, λ)
             + (1 − w(f_AM, λ)) · ε_matrix(f_AM, λ)

  w(f_AM, λ) = 1 − sigmoid(s · (f_AM − f_AM_perc(λ)))
  f_AM_perc(λ) = a_perc + b_perc · (1 − exp(−c_perc · (λ−1)))

The Furnas regime curve is a smoothed Bouvard binary-RCP form;
the matrix regime curve is quadratic in f_AM with λ-dependent
slope.  Total free parameters: 10, total data points: 10 — tight
but well-posed because the regime split is physics-anchored.

Inputs are 10 DEM measurements from the particulate corpus:
  D0.5 (λ≈13): 1 point  (62:38)
  D1   (λ≈7):  3 points (62:38, 72:28, 82:18)
  D2   (λ≈3):  3 points (62:38, 72:28, 82:18)
  D3   (λ≈2):  3 points (62:38, 72:28, 82:18)
"""
from __future__ import annotations
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# ── Data (10 points) ──────────────────────────────────────────────
#  (lam,  f_AM, eps_meas, am_perc, sigma_e)   AM_wt% / 100 = f_AM
DATA = [
    (13.0, 0.62, 16.82, 0.000, 0.00),   # D0.5 particulate_1
    ( 7.0, 0.62, 21.23, 0.000, 0.00),   # D1   particulate_4
    ( 7.0, 0.72, 17.22, 0.809, 0.80),   # D1   particulate_5
    ( 7.0, 0.82, 16.07, 0.993, 5.90),   # D1   particulate_6
    ( 3.0, 0.62,  6.61, 0.932, 1.57),   # D2   particulate_7
    ( 3.0, 0.72, 10.43, 0.993, 4.21),   # D2   particulate_8
    ( 3.0, 0.82, 17.06, 0.998, 7.15),   # D2   particulate_9
    ( 2.0, 0.62,  5.66, 0.964, 1.83),   # D3   particulate_10
    ( 2.0, 0.72, 11.39, 0.998, 4.46),   # D3   particulate_11
    ( 2.0, 0.82, 20.12, 1.000, 7.27),   # D3   particulate_12
]
LAM   = np.array([d[0] for d in DATA])
F_AM  = np.array([d[1] for d in DATA])
EPS   = np.array([d[2] for d in DATA])
APERC = np.array([d[3] for d in DATA])


# ── Model ──────────────────────────────────────────────────────────
def f_AM_perc(lam, a, b, c):
    """AM-percolation threshold f_AM as a function of λ.
    Monotonically increases with λ (high λ = harder for AM to
    percolate because SE separates AM particles)."""
    return a + b * (1.0 - np.exp(-c * (lam - 1.0)))


def w_Furnas(f_AM, lam, a, b, c, s):
    """Furnas-regime weight (0 = pure matrix mode, 1 = pure Furnas).
    Sigmoid centered at f_AM_perc(λ)."""
    fc = f_AM_perc(lam, a, b, c)
    return 1.0 / (1.0 + np.exp(s * (f_AM - fc)))


def eps_Furnas(f_AM, lam, eps_pure_am=36.0, eps_pure_se=10.0,
               valley_center=0.80, valley_depth_max=18.0,
               valley_width=0.20, lam_sat=8.0):
    """Smoothed Bouvard binary-RCP curve.  Valley depth grows with λ
    (saturating at λ ≈ lam_sat).  At f_AM extremes, returns the
    monodisperse RCP / pure-SE plastic limits."""
    # Linear interpolation between pure anchors
    linear = eps_pure_am * f_AM + eps_pure_se * (1.0 - f_AM)
    # Gaussian-shaped valley centered at valley_center
    valley_strength = valley_depth_max * (1.0 - np.exp(-(lam - 1.0) / lam_sat))
    valley = valley_strength * np.exp(
        -((f_AM - valley_center) ** 2) / (2.0 * valley_width ** 2))
    return linear - valley


def eps_matrix(f_AM, lam, e0, k1, k2):
    """Matrix-regime porosity (quadratic in f_AM, λ-dependent slope).
    At low f_AM (SE-rich), ε is low (~5-7%); at high f_AM (AM-rich),
    rises toward mono-AM RCP.  Slope steepens for smaller λ."""
    # Slope: D3 (λ=2) is steeper than D2 (λ=3); k2/λ captures this
    slope = k1 + k2 / lam
    # f_AM_ref = 0.62 anchor: low SE limit of our particulate corpus
    return e0 + slope * (f_AM - 0.62) + 50.0 * np.maximum(0, f_AM - 0.62) ** 2 * (1.0 / lam)


def model_eps(f_AM, lam, params):
    """Full 2-regime model with smooth mixing."""
    a_p, b_p, c_p, s_w, vd_max, e0_m, k1_m, k2_m = params
    w = w_Furnas(f_AM, lam, a_p, b_p, c_p, s_w)
    ef = eps_Furnas(f_AM, lam, valley_depth_max=vd_max)
    em = eps_matrix(f_AM, lam, e0_m, k1_m, k2_m)
    return w * ef + (1.0 - w) * em


def loss(params):
    """Squared-error loss on porosity (%)."""
    pred = model_eps(F_AM, LAM, params)
    return float(np.sum((pred - EPS) ** 2))


# ── Fit ────────────────────────────────────────────────────────────
# Parameter order: [a_perc, b_perc, c_perc, s_w, vd_max, e0_m, k1_m, k2_m]
P0 = [0.40, 0.50, 0.30, 25.0, 18.0, 6.0, 40.0, 30.0]
BOUNDS = [(0.30, 0.70), (0.05, 0.90), (0.05, 1.0), (5.0, 100.0),
          (5.0, 30.0), (3.0, 12.0), (5.0, 100.0), (0.0, 100.0)]

res = minimize(loss, P0, method='L-BFGS-B', bounds=BOUNDS)
PARAMS = res.x
PARAM_NAMES = ['a_perc', 'b_perc', 'c_perc', 's_w',
               'valley_depth_max', 'eps_matrix_0', 'k1_matrix', 'k2_matrix']

print('=' * 60)
print('FIT RESULTS')
print('=' * 60)
print(f'Loss (RMSE): {np.sqrt(res.fun / len(DATA)):.3f} %p')
print()
print('Fitted parameters:')
for name, val in zip(PARAM_NAMES, PARAMS):
    print(f'  {name:20s} = {val:8.3f}')
print()

# ── Verify per-point ───────────────────────────────────────────────
pred = model_eps(F_AM, LAM, PARAMS)
print(f'{"λ":>5s} {"f_AM":>6s} {"meas":>7s} {"pred":>7s} {"err":>7s}  AM_perc  Case')
print('-' * 70)
case_names = ['p_1 D0.5', 'p_4 D1', 'p_5 D1', 'p_6 D1',
              'p_7 D2', 'p_8 D2', 'p_9 D2', 'p_10 D3', 'p_11 D3', 'p_12 D3']
for i, (lam, fam, eps, ap, _) in enumerate(DATA):
    print(f'{lam:5.0f} {fam:6.2f} {eps:6.2f}% {pred[i]:6.2f}% '
          f'{pred[i]-eps:+6.2f}%  {ap*100:5.1f}%  {case_names[i]}')

# Show AM-percolation threshold curve
print()
print('AM-percolation threshold f_AM_perc(λ):')
for lam in [2, 3, 5, 7, 10, 13, 20]:
    fc = f_AM_perc(lam, PARAMS[0], PARAMS[1], PARAMS[2])
    print(f'  λ = {lam:2d}  →  f_AM_perc = {fc:.3f}  '
          f'(AM가 {fc*100:.0f}%일 때 percolation onset)')

# ── Plot ───────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

# --- LEFT: 2D heat map ---
ax = axes[0]
lam_grid = np.logspace(np.log10(1.5), np.log10(20), 80)
fam_grid = np.linspace(0.50, 0.95, 80)
LL, FF = np.meshgrid(lam_grid, fam_grid)
ZZ = np.zeros_like(LL)
for i in range(LL.shape[0]):
    for j in range(LL.shape[1]):
        ZZ[i, j] = model_eps(np.array([FF[i, j]]),
                              np.array([LL[i, j]]), PARAMS)[0]
im = ax.contourf(LL, FF * 100, ZZ, levels=20, cmap='viridis_r')
plt.colorbar(im, ax=ax, label='ε (%)')

# AM-percolation onset curve
lam_curve = np.linspace(1.5, 20, 100)
fperc_curve = f_AM_perc(lam_curve, PARAMS[0], PARAMS[1], PARAMS[2])
ax.plot(lam_curve, fperc_curve * 100, 'w--', lw=2,
        label='AM percolation onset\nf_AM_perc(λ)')

# Data points
for i, (lam, fam, eps, ap, _) in enumerate(DATA):
    ax.scatter(lam, fam * 100, s=120, c=[eps], cmap='viridis_r',
                vmin=ZZ.min(), vmax=ZZ.max(),
                edgecolors='red', linewidths=2, zorder=10)
    ax.annotate(f'{eps:.1f}%', (lam, fam * 100),
                 xytext=(8, 0), textcoords='offset points',
                 fontsize=9, color='red', fontweight='bold')

ax.set_xscale('log')
ax.set_xlabel('λ = r_AM / r_SE')
ax.set_ylabel('AM weight fraction (%)')
ax.set_title('2D porosity surface ε(AM_wt, λ)\n'
              'fitted to 10 mono-AM particulate cases')
ax.legend(loc='lower left', framealpha=0.85)
ax.set_xticks([2, 3, 5, 7, 10, 13, 20])
ax.set_xticklabels(['2', '3', '5', '7', '10', '13', '20'])

# --- RIGHT: 1D slices per λ ---
ax = axes[1]
fam_smooth = np.linspace(0.50, 0.95, 200)
colors = {2: '#d62728', 3: '#ff7f0e', 7: '#2ca02c', 13: '#1f77b4'}
labels = {2: 'D3 (λ=2)', 3: 'D2 (λ=3)', 7: 'D1 (λ=7)', 13: 'D0.5 (λ=13)'}
for lam in [13, 7, 3, 2]:
    eps_curve = model_eps(fam_smooth, lam * np.ones_like(fam_smooth), PARAMS)
    ax.plot(fam_smooth * 100, eps_curve, '-', color=colors[lam],
             label=labels[lam], lw=2)
    # Data points
    pts_x = [d[1] * 100 for d in DATA if abs(d[0] - lam) < 0.1]
    pts_y = [d[2] for d in DATA if abs(d[0] - lam) < 0.1]
    ax.scatter(pts_x, pts_y, s=80, c=colors[lam], edgecolors='black',
                linewidths=1.5, zorder=10)

ax.set_xlabel('AM weight fraction (%)')
ax.set_ylabel('Porosity ε (%)')
ax.set_title('ε(AM_wt) slices per λ\n'
              '— Furnas vs matrix regime trends')
ax.legend(loc='upper left', framealpha=0.95)
ax.grid(alpha=0.3)
ax.set_xlim(50, 95)
ax.set_ylim(0, 25)

plt.tight_layout()
out_png = 'docs/figures/porosity_2d_fit.png'
import os
os.makedirs('docs/figures', exist_ok=True)
plt.savefig(out_png, dpi=150, bbox_inches='tight')
print(f'\nFigure saved: {out_png}')
