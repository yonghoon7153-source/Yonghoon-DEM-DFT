#!/usr/bin/env python3
"""v5 — twin attack:
  (A) ML benchmark (gradient boosting) to measure the data-noise floor
  (B) Physics v5 with composition-dependent η_M(f_AM) — captures the
      "matrix-mode plastic flow drops as AM_wt → 1" behavior that
      hurt v4 on the 1mAh_100_* mono-AM_P high-AM_wt outliers.

If ML floor ≈ physics v5 RMSE → we've reached the data noise floor.
If ML << physics v5 → there's still extractable physics.
"""
from __future__ import annotations
import csv, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import KFold, cross_val_predict


# ── Load + features (same as v4) ──────────────────────────────────
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
    if am is None or eps is None or rse <= 0: continue
    if pv + sv > 0:
        r_eff = (pv*rp + sv*rs) / (pv + sv); f_AMP = pv / (pv + sv)
    elif rs > 0: r_eff = rs; f_AMP = 0.0
    else:        r_eff = rp; f_AMP = 1.0
    if r_eff <= 0: continue

    lam_eff = r_eff / rse
    lam_PS = (rp / rs) if (rp > 0 and rs > 0) else 1.0
    V_AM = am / 4.8; V_SE = (100-am) / 2.0
    phi_SE = V_SE / (V_AM + V_SE)
    thick_typ = {'박막(1mAh)': 25.0, '후막(6mAh)': 120.0,
                  '후막(8mAh)': 160.0, 'particulate': 100.0}.get(r['campaign'], 100.0)
    thick_ratio = (r_eff / 1000.0) / thick_typ
    DATA.append((am/100, lam_eff, lam_PS, f_AMP, phi_SE,
                  thick_ratio, r['campaign'], r['case_id'], eps,
                  rp/1000.0 if rp>0 else 0, rs/1000.0 if rs>0 else 0))

F_AM = np.array([d[0] for d in DATA]); LAM = np.array([d[1] for d in DATA])
LPS = np.array([d[2] for d in DATA]); FAMP = np.array([d[3] for d in DATA])
PHI = np.array([d[4] for d in DATA]); TR = np.array([d[5] for d in DATA])
EPS = np.array([d[8] for d in DATA])
R_P_UM = np.array([d[9] for d in DATA])
R_S_UM = np.array([d[10] for d in DATA])
CAMP = [d[6] for d in DATA]
OUT = {'input_1mAh_100_15', 'input_6mAh_real_10'}
mask = np.array([d[7] not in OUT for d in DATA])

# Numerical campaign label for ML
camp_id = np.array([{'particulate':0,'박막(1mAh)':1,'후막(6mAh)':2,
                      '후막(8mAh)':3}[c] for c in CAMP])


print('=' * 65)
print('A. ML BENCHMARK — Gradient Boosting (5-fold CV)')
print('=' * 65)
# Feature matrix
X = np.column_stack([F_AM, LAM, LPS, FAMP, PHI, TR, R_P_UM, R_S_UM, camp_id])
y = EPS
gbr = GradientBoostingRegressor(n_estimators=200, max_depth=4,
                                  learning_rate=0.05, random_state=42)
kf = KFold(n_splits=5, shuffle=True, random_state=42)
pred_cv = cross_val_predict(gbr, X, y, cv=kf)
rmse_gbr_all = np.sqrt(np.mean((pred_cv - y)**2))
rmse_gbr_trust = np.sqrt(np.mean((pred_cv[mask] - y[mask])**2))
print(f'GBR 5-fold CV RMSE (all 82):    {rmse_gbr_all:.3f} %p')
print(f'GBR 5-fold CV RMSE (trust 80):  {rmse_gbr_trust:.3f} %p')
print()

rfr = RandomForestRegressor(n_estimators=300, max_depth=6,
                              min_samples_split=3, random_state=42)
pred_rf = cross_val_predict(rfr, X, y, cv=kf)
rmse_rf_all = np.sqrt(np.mean((pred_rf - y)**2))
rmse_rf_trust = np.sqrt(np.mean((pred_rf[mask] - y[mask])**2))
print(f'RF  5-fold CV RMSE (all 82):    {rmse_rf_all:.3f} %p')
print(f'RF  5-fold CV RMSE (trust 80):  {rmse_rf_trust:.3f} %p')
print()
# Fit GBR on full data for feature importances + predictions
gbr.fit(X, y); rfr.fit(X, y)
print('Feature importances (GBR):')
feat_names = ['f_AM','λ_eff','λ_PS','f_AMP','φ_SE_vol','thick_ratio',
              'r_AM_P','r_AM_S','campaign_id']
for n, imp in sorted(zip(feat_names, gbr.feature_importances_),
                      key=lambda x: -x[1]):
    print(f'  {n:14s} {imp:.3f}  {"█"*int(imp*40)}')
print()


print('=' * 65)
print('B. PHYSICS v5 — composition-dependent η_M(f_AM)')
print('=' * 65)
def model_v5(f_AM, lam, lps, famp, phi, tr, p):
    """v5: η_M now peaks at optimal f_AM and declines toward 1 at f_AM→1."""
    (a_p, b_p, c_p, s_w,
     D_F, D_M, vc_F, vc_M, vw_F, vw_M, skew_F,
     H_max, eta_F, eta_M_max, eta_M_opt, eta_M_width,   # NEW: η_M is f_AM-dependent
     K_tri, lam_PS_sat, tri_offset,
     K_wall, p_wall, t_floor,
     K_phi, sp) = p
    f_SE = 1.0 - f_AM
    fc = a_p + b_p * (1.0 - np.exp(-c_p * (lam - 1.0)))
    w_M = 1.0 / (1.0 + np.exp(-s_w * (f_AM - fc)))
    w_F = 1.0 - w_M

    depth_F = D_F * (1.0 - np.exp(-(lam - 1.0) / 8.0))
    z_F = (f_SE - vc_F) / vw_F
    val_F = depth_F * np.exp(-0.5 * z_F**2) * (1.0 + skew_F * np.tanh(z_F * 1.5))
    val_F = np.maximum(0, val_F)
    depth_M = D_M / lam
    val_M = depth_M * np.exp(-((f_SE - vc_M) ** 2) / (2.0 * vw_M ** 2))
    dBin = w_F * val_F + w_M * val_M

    f_tri = famp * (1.0 - famp)
    tri_satur = 1.0 - np.exp(-(lps - 1.0) / lam_PS_sat)
    dTri = K_tri * f_tri * tri_satur + tri_offset * (famp - 0.5) ** 2

    # NEW: η_M(f_AM) — Gaussian bump at f_AM = eta_M_opt, declines to 1 elsewhere
    eta_M_local = 1.0 + (eta_M_max - 1.0) * np.exp(
        -((f_AM - eta_M_opt) ** 2) / (2.0 * eta_M_width ** 2))
    eta_eff = w_F * eta_F + w_M * eta_M_local
    dPla = H_max * f_SE * eta_eff

    dWall = K_wall * np.maximum(0, tr - t_floor) ** p_wall
    dPhi = K_phi * (phi - 0.5) ** 2
    return 36.0 - dBin - dTri - dPla + sp + dWall + dPhi

def loss_v5(p):
    return float(np.sum((model_v5(F_AM, LAM, LPS, FAMP, PHI, TR, p) - EPS) ** 2))

BD_v5 = [
    (0.20, 0.95),(0.05, 2.50),(0.005, 1.50),(3.0, 150.0),
    (1.0, 35.0),(1.0, 60.0),(0.05, 0.55),(0.10, 0.80),
    (0.03, 0.50),(0.03, 0.50),(-1.0, 1.0),
    (10.0, 40.0),(0.3, 2.0),
    (1.0, 5.0),    # eta_M_max (peak value)
    (0.50, 0.85),  # eta_M_opt (where peak occurs)
    (0.05, 0.40),  # eta_M_width
    (-25.0, 25.0),(0.3, 20.0),(-20.0, 20.0),
    (-10.0, 60.0),(0.3, 5.0),(-0.5, 0.5),
    (-15.0, 15.0),(-5.0, 5.0),
]
PNAMES_v5 = ['a_perc','b_perc','c_perc','s_w',
             'D_F','D_M','vc_F','vc_M','vw_F','vw_M','skew_F',
             'H_max','eta_F','eta_M_max','eta_M_opt','eta_M_width',
             'K_tri','lam_PS_sat','tri_offset',
             'K_wall','p_wall','t_floor',
             'K_phi','spring_back']

print('Running differential evolution (25 params)...')
res5 = differential_evolution(loss_v5, bounds=BD_v5, maxiter=600,
                                popsize=35, tol=1e-9, seed=42,
                                workers=-1, polish=True, init='sobol',
                                mutation=(0.5, 1.5), recombination=0.7)
P5 = res5.x
RMSE5 = math.sqrt(res5.fun / len(DATA))
pred5 = model_v5(F_AM, LAM, LPS, FAMP, PHI, TR, P5)
RMSE5_trust = math.sqrt(np.mean((pred5[mask] - EPS[mask]) ** 2))
print(f'v5 RMSE (all 82):    {RMSE5:.3f} %p')
print(f'v5 RMSE (trust 80):  {RMSE5_trust:.3f} %p')
print()

n_1 = 100*np.sum(np.abs(pred5 - EPS) < 1) / len(DATA)
n_2 = 100*np.sum(np.abs(pred5 - EPS) < 2) / len(DATA)
n_3 = 100*np.sum(np.abs(pred5 - EPS) < 3) / len(DATA)
print(f'Within ±1%p: {n_1:.0f}%   ±2%p: {n_2:.0f}%   ±3%p: {n_3:.0f}%')
print()

print('Worst v5 residuals:')
resid5 = pred5 - EPS
for i in np.argsort(-np.abs(resid5))[:8]:
    print(f'  {DATA[i][7]:25s}  meas={EPS[i]:5.2f}  pred={pred5[i]:5.2f}  '
          f'Δ={resid5[i]:+5.2f}  f_AMP={FAMP[i]:.2f}')

# ── Summary plot ──────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(20, 6))
camp_colors = {'particulate': '#d62728', '박막(1mAh)': '#1f77b4',
               '후막(6mAh)': '#ff7f0e', '후막(8mAh)': '#2ca02c'}

# Parity v5
ax = axes[0]
for c in sorted(set(CAMP)):
    idx = [i for i,cc in enumerate(CAMP) if cc==c]
    ax.scatter(EPS[idx], pred5[idx], c=camp_colors[c], s=55,
                edgecolors='black', linewidths=0.6, label=c)
ax.plot([3,35],[3,35], 'k-', lw=1.5)
ax.fill_between([3,35],[1,33],[5,37], color='gray', alpha=0.12, label='±2%p')
ax.fill_between([3,35],[2,34],[4,36], color='gray', alpha=0.20, label='±1%p')
ax.set_xlabel('Measured ε (%)'); ax.set_ylabel('Predicted ε (%)')
ax.set_title(f'v5 physics — {RMSE5:.2f}%p all / {RMSE5_trust:.2f}%p trust\n'
              f'±1%p:{n_1:.0f}%  ±2%p:{n_2:.0f}%')
ax.legend(fontsize=8); ax.grid(alpha=0.3); ax.set_xlim(3,35); ax.set_ylim(3,35)

# GBR parity
ax = axes[1]
for c in sorted(set(CAMP)):
    idx = [i for i,cc in enumerate(CAMP) if cc==c]
    ax.scatter(EPS[idx], pred_cv[idx], c=camp_colors[c], s=55,
                edgecolors='black', linewidths=0.6, label=c)
ax.plot([3,35],[3,35], 'k-', lw=1.5)
ax.fill_between([3,35],[1,33],[5,37], color='gray', alpha=0.12)
ax.fill_between([3,35],[2,34],[4,36], color='gray', alpha=0.20)
ax.set_xlabel('Measured ε (%)'); ax.set_ylabel('GBR predicted (5-fold CV)')
ax.set_title(f'ML benchmark (GBR 5-fold CV) — {rmse_gbr_all:.2f}%p all / {rmse_gbr_trust:.2f}%p trust\n'
              'data-noise floor estimate')
ax.legend(fontsize=8); ax.grid(alpha=0.3); ax.set_xlim(3,35); ax.set_ylim(3,35)

# RMSE progression
ax = axes[2]
versions = ['v0\nstrict', 'v1\nrefined', 'v2\nemp', 'v3\n+tri+wall',
            'v4\nglobal', 'v5\nη_M(f_AM)', 'GBR\nML floor']
all_rmse = [6.03, 3.11, 2.76, 2.21, 2.27, RMSE5, rmse_gbr_all]
trust_rmse = [5.85, 2.92, 2.15, 2.13, 2.09, RMSE5_trust, rmse_gbr_trust]
xpos = np.arange(len(versions))
ax.bar(xpos - 0.2, all_rmse, width=0.4, label='all 82', color='#3b82f6')
ax.bar(xpos + 0.2, trust_rmse, width=0.4, label='trust 80', color='#16a34a')
for i, (a, t) in enumerate(zip(all_rmse, trust_rmse)):
    ax.text(i - 0.2, a + 0.08, f'{a:.2f}', ha='center', fontsize=9)
    ax.text(i + 0.2, t + 0.08, f'{t:.2f}', ha='center', fontsize=9)
ax.set_xticks(xpos); ax.set_xticklabels(versions, fontsize=9)
ax.set_ylabel('RMSE (%p)'); ax.set_title('Model progression — RMSE')
ax.legend(); ax.grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('docs/figures/porosity_v5_ml_benchmark.png', dpi=140,
             bbox_inches='tight')
print('\nFigure saved: docs/figures/porosity_v5_ml_benchmark.png')
