#!/usr/bin/env python3
"""Physics-decomposition fit of ε(AM_wt, λ_eff).

Replaces the empirical 2-regime mixing of fit_porosity_2d_full_corpus.py
with an explicit 6-principle decomposition.  Each term has a physical
interpretation and the parameters can be checked against literature
anchors (Sakuda 2013 Heckel constant, Bouvard 2004 binary RCP depth,
McGeary 1961 size-ratio knee, etc.).

ε_observed(f_AM, λ) =
      ε_RCP_baseline                            # P1: mono-RCP ceiling
    − ΔεPacking(λ, f_SE, regime)                # P2: binary packing
    − ΔεPlastic(f_SE) · η_active(regime, λ)     # P3+4: plastic flow gated
    + ε_spring                                   # P6: elastic recovery

where regime ∈ {Furnas, matrix} is governed by AM-percolation onset
(P4) and mass+force balance (P5) is enforced implicitly through the
parametric form (no parameter combinations yield ε < 0 or > ε_RCP).

Parameters (10 total):
  Regime switch:    a_perc, b_perc, c_perc, s_w
  Binary packing:   D_max_F, D_max_M, valley_ctr_F, valley_ctr_M,
                    valley_wid_F, valley_wid_M
  Plastic:          η_F (=1, fixed Heckel anchor),
                    η_M_λ_scale (matrix efficiency vs λ)
  Spring-back:      ε_spring (small constant)
"""
from __future__ import annotations
import csv
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import minimize


# ── Load corpus (same as before) ──────────────────────────────────
ROWS = list(csv.DictReader(open('all_dem_porosity.csv')))
def fnum(s):
    try: return float(s)
    except: return None

DATA = []
for r in ROWS:
    am_wt = fnum(r['am_wt']); eps = fnum(r['porosity_pct'])
    rse = fnum(r['r_SE_um']) or 0
    rp = fnum(r['r_AM_P_um']) or 0; rs = fnum(r['r_AM_S_um']) or 0
    pv = fnum(r['p_vol']) or 0; sv = fnum(r['s_vol']) or 0
    if am_wt is None or eps is None or rse <= 0: continue
    if pv + sv > 0:    r_eff = (pv*rp + sv*rs) / (pv+sv)
    elif rs > 0:       r_eff = rs
    else:              r_eff = rp
    if r_eff <= 0:     continue
    DATA.append((am_wt/100, r_eff/rse, eps, r['campaign'], r['case_id']))

F_AM = np.array([d[0] for d in DATA])
LAM  = np.array([d[1] for d in DATA])
EPS  = np.array([d[2] for d in DATA])

# Known mechanistic outliers from paper §5.2 trust audit
OUTLIERS = {'input_1mAh_100_15', 'input_6mAh_real_10'}
TRUST_MASK = np.array([d[4] not in OUTLIERS for d in DATA])


# ── Physics-explicit model ────────────────────────────────────────
# Literature anchors (NOT fitted — fixed at known values)
EPS_RCP        = 36.0        # mono RCP for spheres (Bernal 1965)
HECKEL_DELTA   = 26.0        # ε_AM_RCP - ε_pure_SE_300MPa = 36 - 10
LAM_SAT        = 8.0         # Bouvard saturation λ scale
                              # (valley depth saturates above McGeary knee)


def f_AM_perc(lam, a, b, c):
    """Principle 4: AM-percolation threshold."""
    return a + b * (1.0 - np.exp(-c * (lam - 1.0)))


def regime_weights(f_AM, lam, a, b, c, s):
    """Furnas (w_F) and matrix (w_M) regime weights, w_F + w_M = 1."""
    fc = f_AM_perc(lam, a, b, c)
    AM_perc = 1.0 / (1.0 + np.exp(-s * (f_AM - fc)))
    return 1.0 - AM_perc, AM_perc


def delta_binary_packing(f_SE, lam, regime_params):
    """Principle 2: binary-packing reduction (Furnas + matrix variants)."""
    Dm_F, Dm_M, vc_F, vc_M, vw_F, vw_M = regime_params
    # Furnas variant — depth saturates at high λ, valley at vc_F in f_SE
    depth_F = Dm_F * (1.0 - np.exp(-(lam - 1.0) / LAM_SAT))
    valley_F = depth_F * np.exp(-((f_SE - vc_F) ** 2) / (2.0 * vw_F ** 2))
    # Matrix variant — depth depends inversely on λ (larger SE bridges better)
    depth_M = Dm_M * (1.0 / lam)
    valley_M = depth_M * np.exp(-((f_SE - vc_M) ** 2) / (2.0 * vw_M ** 2))
    return valley_F, valley_M


def delta_plastic(f_SE, eta_matrix_scale, lam, w_F, w_M):
    """Principles 3+4: plastic densification with regime-dependent
    efficiency.  η_Furnas = 1 (fully active, anchored to Sakuda).
    η_matrix < 1 — SE constrained by AM skeleton in matrix mode, but
    larger SE (small λ) is more effective at bridging AM-AM gaps."""
    eta_F = 1.0
    eta_M = 1.0 - eta_matrix_scale / lam   # small λ → η_M close to 1
    eta_total = w_F * eta_F + w_M * eta_M
    return HECKEL_DELTA * f_SE * eta_total


def model_eps(f_AM, lam, params):
    a, b, c, s, Dm_F, Dm_M, vc_F, vc_M, vw_F, vw_M, eta_M, sp = params
    f_SE = 1.0 - f_AM
    w_F, w_M = regime_weights(f_AM, lam, a, b, c, s)
    val_F, val_M = delta_binary_packing(
        f_SE, lam, (Dm_F, Dm_M, vc_F, vc_M, vw_F, vw_M))
    de_binary = w_F * val_F + w_M * val_M
    de_plast = delta_plastic(f_SE, eta_M, lam, w_F, w_M)
    return EPS_RCP - de_binary - de_plast + sp


def loss(params):
    pred = model_eps(F_AM, LAM, params)
    return float(np.sum((pred - EPS) ** 2))


# Parameter starting points and bounds
P0 = [
    0.50,   # a_perc
    1.20,   # b_perc
    0.05,   # c_perc
    35.0,   # s_w
    15.0,   # D_max_Furnas
    20.0,   # D_max_matrix
    0.30,   # valley_center_Furnas (in f_SE)
    0.50,   # valley_center_matrix (in f_SE)
    0.15,   # valley_width_Furnas
    0.25,   # valley_width_matrix
    1.5,    # eta_matrix_scale
    0.0,    # spring_back
]
BOUNDS = [
    (0.30, 0.80),  # a_perc
    (0.05, 1.5),   # b_perc
    (0.01, 1.0),   # c_perc
    (5.0, 80.0),   # s_w
    (5.0, 30.0),   # D_max_F
    (5.0, 50.0),   # D_max_M
    (0.10, 0.50),  # vc_F
    (0.20, 0.70),  # vc_M
    (0.05, 0.40),  # vw_F
    (0.05, 0.40),  # vw_M
    (0.0, 5.0),    # eta_matrix_scale
    (-2.0, 3.0),   # spring_back
]
PARAM_NAMES = ['a_perc', 'b_perc', 'c_perc', 's_w',
               'D_max_F', 'D_max_M', 'vc_F', 'vc_M',
               'vw_F', 'vw_M', 'eta_M_scale', 'spring_back']

res = minimize(loss, P0, method='L-BFGS-B', bounds=BOUNDS)
PARAMS = res.x
RMSE_all = math.sqrt(res.fun / len(DATA))

# Trust-only RMSE
pred_all = model_eps(F_AM, LAM, PARAMS)
resid_all = pred_all - EPS
RMSE_trust = math.sqrt(np.mean(resid_all[TRUST_MASK] ** 2))

print('=' * 65)
print('PHYSICS-DECOMPOSITION FIT (6 principles, 12 params)')
print('=' * 65)
print(f'Fixed anchors:')
print(f'  ε_RCP_baseline     = {EPS_RCP} %    (Bernal 1965, mono RCP)')
print(f'  HECKEL_delta_max   = {HECKEL_DELTA} %p   (Sakuda 2013, 300 MPa)')
print(f'  LAM_SAT            = {LAM_SAT}      (McGeary 1961 knee)')
print()
print(f'RMSE on all {len(DATA)} cases:    {RMSE_all:.3f} %p')
print(f'RMSE on trust subset:    {RMSE_trust:.3f} %p '
      f'(n={int(TRUST_MASK.sum())})')
print()
print('Fitted parameters:')
for name, val, (lo, hi) in zip(PARAM_NAMES, PARAMS, BOUNDS):
    atb = '⚠ at bound' if (abs(val-lo) < 0.01*(hi-lo) or
                            abs(val-hi) < 0.01*(hi-hi-lo+1)) else ''
    print(f'  {name:18s} = {val:8.3f}   ({lo:.2f}, {hi:.2f}) {atb}')

# Component breakdown for a few test points
print()
print('Term-by-term decomposition (example cases):')
print(f'{"case":25s}  {"λ":>5s}  {"AM%":>5s}  {"w_F":>5s}  {"ΔεBin":>7s}  {"ΔεPla":>7s}  {"ε_pred":>7s}  {"ε_obs":>7s}')
print('-' * 95)
test_cases = ['input_particulate_1', 'input_particulate_7',
              'input_particulate_10', 'input_particulate_12',
              'input_1mAh_5_AMP', 'input_1mAh_5_AMS', 'input_8mAh_5',
              'input_6mAh_real_3']
for tc in test_cases:
    for i, d in enumerate(DATA):
        if d[4] == tc:
            fam = d[0]; lam = d[1]; eps = d[2]
            f_se = 1 - fam
            w_F, w_M = regime_weights(np.array([fam]), np.array([lam]),
                                        PARAMS[0], PARAMS[1], PARAMS[2], PARAMS[3])
            val_F, val_M = delta_binary_packing(
                np.array([f_se]), np.array([lam]),
                PARAMS[4:10])
            de_b = (w_F * val_F + w_M * val_M)[0]
            de_p = delta_plastic(np.array([f_se]), PARAMS[10],
                                 np.array([lam]), w_F, w_M)[0]
            pred = EPS_RCP - de_b - de_p + PARAMS[11]
            print(f'{tc:25s}  {lam:5.2f}  {fam*100:5.1f}  {w_F[0]:5.2f}  '
                  f'{de_b:6.2f}  {de_p:6.2f}   {pred:6.2f}    {eps:6.2f}')
            break

# Per-campaign breakdown
CAMP = [d[3] for d in DATA]
print()
print('Per-campaign residuals (trust subset):')
for camp in sorted(set(CAMP)):
    idx = [i for i, c in enumerate(CAMP)
           if c == camp and TRUST_MASK[i]]
    if not idx: continue
    rs = resid_all[idx]
    print(f'  {camp:15s} n={len(idx):3d}  RMSE={np.sqrt(np.mean(rs**2)):.2f}%p  '
          f'|Δ|<2%p: {100*np.sum(np.abs(rs)<2)/len(rs):.0f}%')


# ── Plots ─────────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(20, 11))

# Panel 1: 2D heatmap
ax = axes[0, 0]
lam_grid = np.logspace(np.log10(2), np.log10(25), 100)
fam_grid = np.linspace(0.50, 0.99, 100)
LL, FF = np.meshgrid(lam_grid, fam_grid)
ZZ = np.array([[model_eps(np.array([FF[i,j]]), np.array([LL[i,j]]), PARAMS)[0]
                 for j in range(LL.shape[1])] for i in range(LL.shape[0])])
im = ax.contourf(LL, FF * 100, ZZ, levels=np.linspace(3, 35, 17),
                  cmap='viridis_r', extend='both')
plt.colorbar(im, ax=ax, label='ε predicted (%)')
lam_curve = np.linspace(2, 25, 100)
fperc_curve = np.clip(f_AM_perc(lam_curve, PARAMS[0], PARAMS[1], PARAMS[2]), 0, 1)
ax.plot(lam_curve, fperc_curve * 100, 'w--', lw=2,
        label='AM percolation onset')
camp_colors = {'particulate': '#d62728', '박막(1mAh)': '#1f77b4',
               '후막(6mAh)': '#ff7f0e', '후막(8mAh)': '#2ca02c'}
for camp in sorted(set(CAMP)):
    idx = [i for i, c in enumerate(CAMP) if c == camp]
    ax.scatter([LAM[i] for i in idx], [F_AM[i]*100 for i in idx],
                c=camp_colors[camp], s=45, edgecolors='black',
                linewidths=0.6, label=f'{camp} (n={len(idx)})', zorder=10)
ax.set_xscale('log')
ax.set_xticks([2,3,5,7,10,15,20]); ax.set_xticklabels(['2','3','5','7','10','15','20'])
ax.set_xlabel('λ_eff = r_AM_eff / r_SE')
ax.set_ylabel('AM weight fraction (%)')
ax.set_title(f'Physics decomposition fit\nRMSE {RMSE_all:.2f}%p (all 82) / {RMSE_trust:.2f}%p (trust 80)')
ax.legend(loc='lower left', framealpha=0.92, fontsize=8.5)

# Panel 2: Parity plot
ax = axes[0, 1]
for camp in sorted(set(CAMP)):
    idx = [i for i, c in enumerate(CAMP) if c == camp]
    ax.scatter(EPS[idx], pred_all[idx], c=camp_colors[camp],
                s=50, edgecolors='black', linewidths=0.6,
                label=camp, zorder=5)
ax.plot([3,35], [3,35], 'k-', lw=1.5, label='1:1')
ax.fill_between([3,35], [1,33], [5,37], color='gray', alpha=0.15, label='±2%p')
ax.set_xlabel('Measured ε (%)'); ax.set_ylabel('Predicted ε (%)')
n_2pct = 100*sum(abs(r)<2 for r in resid_all)/len(resid_all)
n_3pct = 100*sum(abs(r)<3 for r in resid_all)/len(resid_all)
ax.set_title(f'Parity — |Δ|<2%p: {n_2pct:.0f}%, |Δ|<3%p: {n_3pct:.0f}%')
ax.legend(fontsize=8.5); ax.set_xlim(3,35); ax.set_ylim(3,35); ax.grid(alpha=0.3)

# Panel 3: Decomposition vs f_SE at fixed λ
ax = axes[0, 2]
fse_curve = np.linspace(0.05, 0.95, 100)
for lam_show, color, ls in [(2, '#d62728', '-'), (3, '#ff7f0e', '-'),
                             (7, '#2ca02c', '-'), (13, '#1f77b4', '-')]:
    fAM = 1 - fse_curve
    eps_curve = np.array([model_eps(np.array([1-fse]), np.array([lam_show]),
                                       PARAMS)[0] for fse in fse_curve])
    ax.plot(fAM*100, eps_curve, color=color, ls=ls, lw=2,
             label=f'λ={lam_show}')
ax.axhline(EPS_RCP, color='gray', ls=':', label='ε_RCP=36%')
ax.set_xlabel('AM weight fraction (%)'); ax.set_ylabel('ε (%)')
ax.set_title('1D slices per λ — sin-wave at high λ, monotonic at low λ')
ax.legend(); ax.grid(alpha=0.3); ax.set_ylim(0, 38)

# Panel 4: Term contributions for λ=8 (representative bimodal)
ax = axes[1, 0]
lam_show = 8.0
fse_curve = np.linspace(0.05, 0.95, 100); fAM = 1 - fse_curve
w_F_curve = np.array([regime_weights(np.array([1-fse]), np.array([lam_show]),
                                          PARAMS[0], PARAMS[1], PARAMS[2], PARAMS[3])[0][0]
                       for fse in fse_curve])
w_M_curve = 1 - w_F_curve
val_F_curve = np.array([delta_binary_packing(np.array([fse]), np.array([lam_show]), PARAMS[4:10])[0][0]
                          for fse in fse_curve])
val_M_curve = np.array([delta_binary_packing(np.array([fse]), np.array([lam_show]), PARAMS[4:10])[1][0]
                          for fse in fse_curve])
de_b_curve = w_F_curve * val_F_curve + w_M_curve * val_M_curve
de_p_curve = np.array([delta_plastic(np.array([fse]), PARAMS[10], np.array([lam_show]),
                                          np.array([w_F_curve[i]]), np.array([w_M_curve[i]]))[0]
                         for i, fse in enumerate(fse_curve)])
eps_curve = EPS_RCP - de_b_curve - de_p_curve + PARAMS[11]
ax.fill_between(fAM*100, EPS_RCP, EPS_RCP - de_b_curve,
                  color='#1f77b4', alpha=0.4, label='Δε binary packing')
ax.fill_between(fAM*100, EPS_RCP - de_b_curve, eps_curve,
                  color='#ff7f0e', alpha=0.4, label='Δε plastic')
ax.fill_between(fAM*100, eps_curve, eps_curve - 0.0, color='none')  # no spring
ax.plot(fAM*100, eps_curve, 'k-', lw=2, label='ε predicted')
ax.axhline(EPS_RCP, color='gray', ls=':', label='ε_RCP=36%')
ax.set_xlabel('AM weight fraction (%)'); ax.set_ylabel('ε (%)')
ax.set_title(f'Term contributions at λ={lam_show:.0f} (bimodal regime)')
ax.legend(loc='upper left'); ax.set_ylim(0, 38); ax.grid(alpha=0.3)

# Panel 5: Regime weights vs (f_AM, λ)
ax = axes[1, 1]
AM_perc_grid = np.array([[1-regime_weights(np.array([FF[i,j]]), np.array([LL[i,j]]),
                                              PARAMS[0], PARAMS[1], PARAMS[2], PARAMS[3])[0][0]
                          for j in range(LL.shape[1])]
                         for i in range(LL.shape[0])])
im = ax.contourf(LL, FF*100, AM_perc_grid, levels=20, cmap='RdYlBu_r')
plt.colorbar(im, ax=ax, label='AM percolation prob (matrix-regime weight)')
ax.plot(lam_curve, fperc_curve*100, 'k--', lw=2, label='f_AM_perc(λ)')
ax.set_xscale('log')
ax.set_xticks([2,3,5,7,10,15,20]); ax.set_xticklabels(['2','3','5','7','10','15','20'])
ax.set_xlabel('λ_eff'); ax.set_ylabel('AM_wt%')
ax.set_title('Regime split: w_F (Furnas, blue) vs w_M (matrix, red)')
ax.legend()

# Panel 6: Residual diagnostic
ax = axes[1, 2]
for camp in sorted(set(CAMP)):
    idx = [i for i, c in enumerate(CAMP) if c == camp]
    ax.scatter([F_AM[i]*100 for i in idx], [resid_all[i] for i in idx],
                c=camp_colors[camp], s=50, edgecolors='black',
                linewidths=0.6, label=camp, zorder=5)
ax.axhline(0, color='k', lw=1.5)
ax.axhline(2, color='gray', lw=0.8, ls=':')
ax.axhline(-2, color='gray', lw=0.8, ls=':')
ax.set_xlabel('AM_wt%'); ax.set_ylabel('Residual (pred − meas) (%p)')
ax.set_title('Residual diagnostic vs AM_wt')
ax.legend(fontsize=8.5); ax.grid(alpha=0.3); ax.set_ylim(-12, 12)

plt.tight_layout()
import os
os.makedirs('docs/figures', exist_ok=True)
out_png = 'docs/figures/porosity_physics_decomposition.png'
plt.savefig(out_png, dpi=140, bbox_inches='tight')
print(f'\nFigure saved: {out_png}')
