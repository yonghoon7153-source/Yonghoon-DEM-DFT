#!/usr/bin/env python3
"""v4 — push RMSE down via global optimization + wider feature set.

Strategy vs v3:
  • Differential-evolution global search (escapes local minima v3 fell into)
  • Wider parameter bounds (8 of 18 v3 params were at bounds)
  • Trimodal correction can SIGN both ways (sometimes 3-stage packing
    densifies, sometimes disrupts — let data decide)
  • Add φ_SE-volume direct dependence (separate from f_AM mass)
  • Add λ_P-specific term for mono-AM_P configurations
  • More expressive Furnas valley (asymmetric Gaussian)
"""
from __future__ import annotations
import csv, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution, minimize


ROWS = list(csv.DictReader(open('all_dem_porosity.csv')))
def fnum(s):
    try: return float(s)
    except: return None

DATA = []
for r in ROWS:
    am = fnum(r['am_wt']); eps = fnum(r['porosity_pct'])
    rse = fnum(r['r_SE_um']) or 0
    rp = fnum(r['r_AM_P_um']) or 0
    rs = fnum(r['r_AM_S_um']) or 0
    pv = fnum(r['p_vol']) or 0
    sv = fnum(r['s_vol']) or 0
    if am is None or eps is None or rse <= 0:
        continue

    if pv + sv > 0:
        r_eff = (pv*rp + sv*rs) / (pv + sv)
        f_AMP = pv / (pv + sv)
    elif rs > 0:
        r_eff = rs; f_AMP = 0.0
    else:
        r_eff = rp; f_AMP = 1.0
    if r_eff <= 0: continue

    lam_eff = r_eff / rse
    lam_PS  = (rp / rs) if (rp > 0 and rs > 0) else 1.0
    lam_P_only = (rp / rse) if rp > 0 else 0.0
    # Volume fraction estimate (ρ_AM=4.8, ρ_SE=2.0)
    V_AM = am / 4.8; V_SE = (100-am) / 2.0
    phi_SE_vol = V_SE / (V_AM + V_SE)

    thick_typ = {'박막(1mAh)': 25.0, '후막(6mAh)': 120.0,
                  '후막(8mAh)': 160.0, 'particulate': 100.0}.get(r['campaign'], 100.0)
    D_AM_um = r_eff / 1000.0
    thick_ratio = D_AM_um / thick_typ

    DATA.append((am/100, lam_eff, lam_PS, f_AMP, phi_SE_vol,
                  thick_ratio, lam_P_only, eps, r['campaign'], r['case_id']))

F_AM = np.array([d[0] for d in DATA])
LAM  = np.array([d[1] for d in DATA])
LPS  = np.array([d[2] for d in DATA])
FAMP = np.array([d[3] for d in DATA])
PHI  = np.array([d[4] for d in DATA])
TR   = np.array([d[5] for d in DATA])
LP   = np.array([d[6] for d in DATA])
EPS  = np.array([d[7] for d in DATA])
CAMP = [d[8] for d in DATA]
print(f'Loaded {len(DATA)} cases')

OUT = {'input_1mAh_100_15', 'input_6mAh_real_10'}
mask_trust = np.array([d[9] not in OUT for d in DATA])


def model(f_AM, lam, lps, famp, phi, tr, lp, p):
    """v4 model with 23 parameters."""
    (a_p, b_p, c_p, s_w,                          # 0-3: regime
     D_F, D_M, vc_F, vc_M, vw_F, vw_M, skew_F,    # 4-10: binary packing
     H_max, eta_F, eta_M, H_lambda,                # 11-14: plastic
     K_tri, lam_PS_sat, tri_offset,                # 15-17: trimodal
     K_wall, p_wall, t_floor,                      # 18-20: wall
     K_phi, sp) = p                                # 21-22: phi correction + spring
    f_SE = 1.0 - f_AM

    # P4: regime
    fc = a_p + b_p * (1.0 - np.exp(-c_p * (lam - 1.0)))
    w_M = 1.0 / (1.0 + np.exp(-s_w * (f_AM - fc)))
    w_F = 1.0 - w_M

    # P2a: Furnas binary (skewed Gaussian valley)
    depth_F = D_F * (1.0 - np.exp(-(lam - 1.0) / 8.0))
    # skew: makes valley asymmetric (wider on one side)
    z_F = (f_SE - vc_F) / vw_F
    val_F = depth_F * np.exp(-0.5 * z_F**2) * (1.0 + skew_F * np.tanh(z_F * 1.5))
    val_F = np.maximum(0, val_F)

    # P2b: Matrix binary
    depth_M = D_M / lam
    val_M = depth_M * np.exp(-((f_SE - vc_M) ** 2) / (2.0 * vw_M ** 2))
    dBin = w_F * val_F + w_M * val_M

    # P2c: Trimodal correction (now signed — can be ±)
    f_tri = famp * (1.0 - famp)
    tri_satur = 1.0 - np.exp(-(lps - 1.0) / lam_PS_sat)
    dTri = K_tri * f_tri * tri_satur + tri_offset * (famp - 0.5) ** 2

    # P3: Plastic densification (Heckel max can be λ-dependent)
    H_eff_max = H_max + H_lambda * np.log(np.maximum(lam, 1.0))
    eta_eff = w_F * eta_F + w_M * eta_M
    dPla = H_eff_max * f_SE * eta_eff

    # P6+wall: wall confinement (active only above floor threshold)
    dWall = K_wall * np.maximum(0, tr - t_floor) ** p_wall

    # NEW: phi_SE_vol correction — captures density-driven effects
    # beyond f_AM mass fraction (e.g., wt vs vol asymmetry)
    dPhi = K_phi * (phi - 0.5) ** 2

    return 36.0 - dBin - dTri - dPla + sp + dWall + dPhi


def loss(p):
    pred = model(F_AM, LAM, LPS, FAMP, PHI, TR, LP, p)
    return float(np.sum((pred - EPS) ** 2))


# Bounds — wider than v3
BOUNDS = [
    (0.20, 0.95),      # 0  a_perc
    (0.05, 2.50),      # 1  b_perc
    (0.005, 1.50),     # 2  c_perc
    (3.0, 150.0),      # 3  s_w
    (1.0, 35.0),       # 4  D_F
    (1.0, 60.0),       # 5  D_M
    (0.05, 0.55),      # 6  vc_F
    (0.10, 0.80),      # 7  vc_M
    (0.03, 0.50),      # 8  vw_F
    (0.03, 0.50),      # 9  vw_M
    (-1.0, 1.0),       # 10 skew_F
    (10.0, 40.0),      # 11 H_max
    (0.3, 2.0),        # 12 eta_F
    (0.3, 4.0),        # 13 eta_M
    (-5.0, 5.0),       # 14 H_lambda
    (-25.0, 25.0),     # 15 K_tri
    (0.3, 20.0),       # 16 lam_PS_sat
    (-20.0, 20.0),     # 17 tri_offset
    (-10.0, 60.0),     # 18 K_wall
    (0.3, 5.0),        # 19 p_wall
    (-0.5, 0.5),       # 20 t_floor
    (-15.0, 15.0),     # 21 K_phi
    (-5.0, 5.0),       # 22 spring_back
]
PNAMES = ['a_perc','b_perc','c_perc','s_w',
          'D_F','D_M','vc_F','vc_M','vw_F','vw_M','skew_F',
          'H_max','eta_F','eta_M','H_lambda',
          'K_tri','lam_PS_sat','tri_offset',
          'K_wall','p_wall','t_floor',
          'K_phi','spring_back']

print('Running differential evolution global search ...')
res = differential_evolution(
    loss, bounds=BOUNDS, maxiter=500, popsize=30,
    tol=1e-9, seed=42, workers=-1, polish=True,
    mutation=(0.5, 1.5), recombination=0.7,
    init='sobol')
PARAMS = res.x
RMSE = math.sqrt(res.fun / len(DATA))

pred = model(F_AM, LAM, LPS, FAMP, PHI, TR, LP, PARAMS)
resid = pred - EPS
RMSE_trust = math.sqrt(np.mean(resid[mask_trust] ** 2))

print()
print('=' * 65)
print('v4 GLOBAL FIT (differential evolution, 23 params)')
print('=' * 65)
print(f'RMSE on all 82 cases:   {RMSE:.3f} %p')
print(f'RMSE on trust subset:   {RMSE_trust:.3f} %p (n={int(mask_trust.sum())})')
print()
print('Progression: v0(6.0) → v1(3.1) → v2(2.76) → v3(2.21) → v4')
print()
n_1pct = 100*sum(abs(r)<1 for r in resid)/len(resid)
n_2pct = 100*sum(abs(r)<2 for r in resid)/len(resid)
n_3pct = 100*sum(abs(r)<3 for r in resid)/len(resid)
print(f'Within ±1%p: {n_1pct:.0f}%   ±2%p: {n_2pct:.0f}%   ±3%p: {n_3pct:.0f}%')

print()
print('Fitted parameters:')
for n, v, (lo, hi) in zip(PNAMES, PARAMS, BOUNDS):
    width = max(abs(hi-lo), 0.01)
    atb = '⚠ at bound' if (abs(v-lo) < 0.02*width or abs(v-hi) < 0.02*width) else ''
    print(f'  {n:14s} = {v:9.3f}   ({lo:+7.2f}, {hi:+7.2f}) {atb}')

print()
print('Per-campaign residuals (trust subset):')
from collections import defaultdict
camp_r = defaultdict(list)
for i, c in enumerate(CAMP):
    if mask_trust[i]: camp_r[c].append(resid[i])
for c in sorted(camp_r):
    r = np.array(camp_r[c])
    print(f'  {c:15s} n={len(r):3d}  RMSE={np.sqrt(np.mean(r**2)):5.2f}%p  '
          f'|Δ|<1%p:{100*np.sum(np.abs(r)<1)/len(r):3.0f}%  '
          f'|Δ|<2%p:{100*np.sum(np.abs(r)<2)/len(r):3.0f}%  '
          f'|Δ|<3%p:{100*np.sum(np.abs(r)<3)/len(r):3.0f}%')

print()
print('Top 10 worst residuals:')
order = np.argsort(-np.abs(resid))[:10]
for i in order:
    print(f'  {DATA[i][9]:25s}  meas={EPS[i]:5.2f}  pred={pred[i]:5.2f}  '
          f'Δ={resid[i]:+5.2f}  λ={LAM[i]:5.2f}  AM={F_AM[i]*100:5.1f}%  '
          f'f_AMP={FAMP[i]:.2f}  λ_PS={LPS[i]:.2f}')

# ── 3-panel diagnostic plot ───────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(20, 6))
camp_colors = {'particulate': '#d62728', '박막(1mAh)': '#1f77b4',
               '후막(6mAh)': '#ff7f0e', '후막(8mAh)': '#2ca02c'}
camp_lab = {'particulate':'particulate','박막(1mAh)':'thin 1mAh',
            '후막(6mAh)':'thick 6mAh','후막(8mAh)':'thick 8mAh'}

ax = axes[0]
for c in sorted(set(CAMP)):
    idx = [i for i,cc in enumerate(CAMP) if cc==c]
    ax.scatter(EPS[idx], pred[idx], c=camp_colors[c], s=55,
                edgecolors='black', linewidths=0.6,
                label=f'{camp_lab[c]} (n={len(idx)})')
ax.plot([3,35],[3,35], 'k-', lw=1.5)
ax.fill_between([3,35],[1,33],[5,37], color='gray', alpha=0.12, label='±2%p')
ax.fill_between([3,35],[2,34],[4,36], color='gray', alpha=0.20, label='±1%p')
ax.set_xlabel('Measured ε (%)'); ax.set_ylabel('Predicted ε (%)')
ax.set_title(f'v4 — all={RMSE:.2f}%p, trust={RMSE_trust:.2f}%p\n'
              f'±1%p:{n_1pct:.0f}%  ±2%p:{n_2pct:.0f}%  ±3%p:{n_3pct:.0f}%')
ax.legend(fontsize=9, loc='lower right')
ax.set_xlim(3,35); ax.set_ylim(3,35); ax.grid(alpha=0.3)

ax = axes[1]
versions = ['v0\nstrict', 'v1\nrefined', 'v2\nempirical', 'v3\n+tri+wall', 'v4\nglobal']
all_rmse = [6.03, 3.11, 2.76, 2.21, RMSE]
trust_rmse = [5.85, 2.92, 2.15, 2.13, RMSE_trust]
xpos = np.arange(len(versions))
ax.bar(xpos - 0.20, all_rmse, width=0.4, label='all 82 cases', color='#3b82f6')
ax.bar(xpos + 0.20, trust_rmse, width=0.4, label='trust (80)', color='#16a34a')
for i, (a, t) in enumerate(zip(all_rmse, trust_rmse)):
    ax.text(i - 0.20, a + 0.1, f'{a:.2f}', ha='center', fontsize=10)
    ax.text(i + 0.20, t + 0.1, f'{t:.2f}', ha='center', fontsize=10)
ax.set_xticks(xpos); ax.set_xticklabels(versions)
ax.set_ylabel('RMSE (%p)'); ax.legend()
ax.set_title('Model progression — RMSE reduction')
ax.grid(alpha=0.3, axis='y')

ax = axes[2]
sc = ax.scatter(F_AM*100, resid, c=LAM, cmap='viridis', s=60,
                 edgecolors='black', linewidths=0.6)
plt.colorbar(sc, ax=ax, label='λ_eff')
ax.axhline(0, color='k', lw=1.5)
ax.axhline(1, color='gray', lw=0.6, ls=':'); ax.axhline(-1, color='gray', lw=0.6, ls=':')
ax.axhline(2, color='gray', lw=0.6, ls=':'); ax.axhline(-2, color='gray', lw=0.6, ls=':')
ax.set_xlabel('AM_wt%'); ax.set_ylabel('Residual (%p)')
ax.set_title('v4 residuals vs (AM_wt, λ_eff)')
ax.grid(alpha=0.3); ax.set_ylim(-8, 8)

plt.tight_layout()
plt.savefig('docs/figures/porosity_v4_global.png', dpi=140, bbox_inches='tight')
print('\nFigure saved: docs/figures/porosity_v4_global.png')
