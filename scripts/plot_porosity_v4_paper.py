#!/usr/bin/env python3
"""Final 2D plot with v4 model — paper-quality 4-panel figure.

Panels:
  (a) ε(AM_wt, λ_eff) heatmap with measured points + outlier annotations
  (b) 1D slices at fixed λ values (showing sin-wave shape changes)
  (c) Decomposition stack at λ=8 (showing each term's contribution)
  (d) Outlier explanation — residual vs feature with group labels
"""
from __future__ import annotations
import csv, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch


# Load + features
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
                  thick_ratio, eps, r['campaign'], r['case_id']))

F_AM = np.array([d[0] for d in DATA]); LAM = np.array([d[1] for d in DATA])
LPS = np.array([d[2] for d in DATA]); FAMP = np.array([d[3] for d in DATA])
PHI = np.array([d[4] for d in DATA]); TR = np.array([d[5] for d in DATA])
EPS = np.array([d[6] for d in DATA]); CAMP = [d[7] for d in DATA]
CID  = [d[8] for d in DATA]

# v4 best-fit parameters (from previous run)
P4 = np.array([0.288, 0.494, 0.491, 92.392,
               12.102, 9.087, 0.296, 0.581, 0.119, 0.095, -0.389,
               27.830, 0.754, 2.543, 2.209,
               20.371, 2.292, 0.027,
               59.939, 4.207, -0.293,
               -11.495, -3.951])

def model_v4(f_AM, lam, lps, famp, phi, tr, p):
    (a,b,c,s, D_F,D_M,vc_F,vc_M,vw_F,vw_M,skew_F,
     H,eF,eM,H_l, K_t,lps_s,t_off, K_w,p_w,t_fl, K_phi,sp) = p
    f_SE = 1 - f_AM
    fc = a + b*(1 - np.exp(-c*(lam-1)))
    w_M = 1/(1 + np.exp(-s*(f_AM - fc))); w_F = 1 - w_M
    dF = D_F*(1-np.exp(-(lam-1)/8))
    z_F = (f_SE - vc_F)/vw_F
    vF = dF * np.exp(-0.5*z_F**2)*(1+skew_F*np.tanh(1.5*z_F))
    vF = np.maximum(0, vF)
    vM = (D_M/lam)*np.exp(-((f_SE-vc_M)**2)/(2*vw_M**2))
    dBin = w_F*vF + w_M*vM
    f_tri = famp*(1-famp)
    dTri = K_t*f_tri*(1-np.exp(-(lps-1)/lps_s)) + t_off*(famp-0.5)**2
    H_eff = H + H_l*np.log(np.maximum(lam,1.0))
    dPla = H_eff*f_SE*(w_F*eF + w_M*eM)
    dWall = K_w*np.maximum(0, tr - t_fl)**p_w
    dPhi = K_phi*(phi - 0.5)**2
    return 36.0 - dBin - dTri - dPla + sp + dWall + dPhi

# Per-case prediction
pred = np.array([model_v4(np.array([F_AM[i]]), np.array([LAM[i]]),
                            np.array([LPS[i]]), np.array([FAMP[i]]),
                            np.array([PHI[i]]), np.array([TR[i]]), P4)[0]
                 for i in range(len(DATA))])
resid = pred - EPS

# ── 4-panel figure ────────────────────────────────────────────────
fig = plt.figure(figsize=(20, 14))
gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.28)
camp_colors = {'particulate': '#d62728', '박막(1mAh)': '#1f77b4',
               '후막(6mAh)': '#ff7f0e', '후막(8mAh)': '#2ca02c'}
camp_lab = {'particulate':'particulate','박막(1mAh)':'thin 1mAh',
            '후막(6mAh)':'thick 6mAh','후막(8mAh)':'thick 8mAh'}

# Panel (a) — 2D heatmap with outlier annotations -----------------
ax = fig.add_subplot(gs[0, 0])
lam_grid = np.logspace(np.log10(1.3), np.log10(25), 120)
fam_grid = np.linspace(0.50, 0.99, 120)
LL, FF = np.meshgrid(lam_grid, fam_grid)
# Use a representative (PHI, TR, LPS, FAMP) for the surface
ZZ = np.zeros_like(LL)
for i in range(LL.shape[0]):
    for j in range(LL.shape[1]):
        f_a = FF[i,j]; lam = LL[i,j]
        v_AM = f_a*100/4.8; v_SE = (1-f_a)*100/2.0
        phi = v_SE/(v_AM+v_SE)
        ZZ[i,j] = model_v4(np.array([f_a]), np.array([lam]),
                             np.array([1.0]), np.array([0.0]),
                             np.array([phi]), np.array([0.05]), P4)[0]
levels = np.linspace(3, 35, 17)
im = ax.contourf(LL, FF*100, ZZ, levels=levels, cmap='viridis_r', extend='both')
cbar = plt.colorbar(im, ax=ax, label='Predicted ε (%)', pad=0.02)
# AM percolation curve
lam_curve = np.linspace(1.3, 25, 200)
fperc = P4[0] + P4[1]*(1 - np.exp(-P4[2]*(lam_curve-1)))
fperc = np.clip(fperc, 0, 1)
ax.plot(lam_curve, fperc*100, 'w--', lw=2.5, label='AM-percolation onset')
# Regime labels
ax.text(2.0, 65, 'Matrix\nregime', ha='center', va='center',
        fontsize=12, color='white', fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='black', alpha=0.4, edgecolor='none'))
ax.text(15, 85, 'Furnas\nregime', ha='center', va='center',
        fontsize=12, color='white', fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='black', alpha=0.4, edgecolor='none'))
# Data points
for c in sorted(set(CAMP)):
    idx = [i for i,cc in enumerate(CAMP) if cc==c]
    ax.scatter([LAM[i] for i in idx], [F_AM[i]*100 for i in idx],
                c=camp_colors[c], s=70, edgecolors='black', linewidths=0.9,
                label=f'{camp_lab[c]} (n={len(idx)})', zorder=10)
# Highlight outliers
OUTLIERS = {'input_1mAh_100_15': 'A1', 'input_1mAh_100_10': 'A2',
            'input_1mAh_5_AMP': 'B',  'input_8mAh_1': 'C',
            'input_particulate_9_E05': 'D', 'input_1mAh_100_3': 'E'}
for i, cid in enumerate(CID):
    if cid in OUTLIERS:
        ax.scatter(LAM[i], F_AM[i]*100, s=350, marker='o',
                    facecolors='none', edgecolors='red', linewidths=2.5, zorder=20)
        ax.annotate(OUTLIERS[cid], (LAM[i], F_AM[i]*100),
                     xytext=(7, 7), textcoords='offset points',
                     fontsize=10, color='red', fontweight='bold', zorder=21)
ax.set_xscale('log')
ax.set_xticks([2,3,5,7,10,15,20]); ax.set_xticklabels(['2','3','5','7','10','15','20'])
ax.set_xlabel('λ_eff = r_AM_eff / r_SE', fontsize=12)
ax.set_ylabel('AM weight fraction (%)', fontsize=12)
ax.set_title('(a)  2D porosity surface ε(AM_wt, λ_eff) — v4 fit\n'
              '            RMSE 2.27 %p (all 82) / 2.09 %p (trust 80)',
              fontsize=12, loc='left')
ax.legend(loc='lower right', framealpha=0.9, fontsize=9)
ax.set_xlim(1.3, 25); ax.set_ylim(50, 99)

# Panel (b) — 1D slices --------------------------------------------
ax = fig.add_subplot(gs[0, 1])
fam_curve = np.linspace(0.5, 0.98, 200)
slice_lams = [2, 3, 5, 7, 10, 13]
slice_colors = plt.cm.plasma(np.linspace(0.1, 0.85, len(slice_lams)))
for lam_s, col in zip(slice_lams, slice_colors):
    eps_c = np.array([model_v4(np.array([f]), np.array([lam_s]),
                                  np.array([1.0]), np.array([0.0]),
                                  np.array([(1-f)*100/2 / (f*100/4.8 + (1-f)*100/2)]),
                                  np.array([0.05]), P4)[0]
                       for f in fam_curve])
    ax.plot(fam_curve*100, eps_c, color=col, lw=2.5, label=f'λ={lam_s}')
# Overlay measurements at similar λ
for lam_show in slice_lams:
    idx = [i for i in range(len(DATA))
           if abs(LAM[i] - lam_show) < 0.6 and CID[i] not in OUTLIERS]
    if idx:
        col = slice_colors[slice_lams.index(lam_show)]
        ax.scatter([F_AM[i]*100 for i in idx], [EPS[i] for i in idx],
                    s=50, color=col, edgecolors='black', linewidths=0.5,
                    zorder=10)
ax.axhline(36, color='gray', ls=':', lw=1.0, label='ε_RCP = 36%')
ax.set_xlabel('AM weight fraction (%)', fontsize=12)
ax.set_ylabel('Porosity ε (%)', fontsize=12)
ax.set_title('(b)  1D slices ε(AM_wt) at fixed λ\n'
              '            sin-wave shape (high λ) → monotonic (low λ)',
              fontsize=12, loc='left')
ax.legend(loc='upper left', fontsize=10, ncol=2)
ax.grid(alpha=0.3)
ax.set_xlim(50, 99); ax.set_ylim(0, 40)

# Panel (c) — term decomposition at λ=7 ----------------------------
ax = fig.add_subplot(gs[1, 0])
lam_show = 7.0
fam_curve = np.linspace(0.5, 0.98, 200)
fse_curve = 1 - fam_curve
phi_curve = np.array([(1-f)*100/2 / (f*100/4.8 + (1-f)*100/2) for f in fam_curve])

# Per-point term computation
ws_F = np.zeros_like(fam_curve); ws_M = np.zeros_like(fam_curve)
vF_arr = np.zeros_like(fam_curve); vM_arr = np.zeros_like(fam_curve)
dPla_arr = np.zeros_like(fam_curve)
for i, fa in enumerate(fam_curve):
    fc = P4[0] + P4[1]*(1-np.exp(-P4[2]*(lam_show-1)))
    w_M = 1/(1+np.exp(-P4[3]*(fa-fc))); w_F = 1-w_M
    ws_F[i] = w_F; ws_M[i] = w_M
    f_se = 1-fa
    dF = P4[4]*(1-np.exp(-(lam_show-1)/8))
    z_F = (f_se-P4[6])/P4[8]
    vF = dF*np.exp(-0.5*z_F**2)*(1+P4[10]*np.tanh(1.5*z_F))
    vF_arr[i] = w_F * max(0, vF)
    vM = (P4[5]/lam_show)*np.exp(-((f_se-P4[7])**2)/(2*P4[9]**2))
    vM_arr[i] = w_M * vM
    H_eff = P4[11] + P4[14]*np.log(lam_show)
    dPla_arr[i] = H_eff * f_se * (w_F*P4[12] + w_M*P4[13])

dBin_total = vF_arr + vM_arr
eps_pred = 36 - dBin_total - dPla_arr + P4[22]
# Show stacked decomposition
ax.fill_between(fam_curve*100, 36, 36 - vF_arr,
                  color='#3b82f6', alpha=0.4, label='Δε Furnas binary')
ax.fill_between(fam_curve*100, 36 - vF_arr, 36 - vF_arr - vM_arr,
                  color='#a855f7', alpha=0.4, label='Δε Matrix binary')
ax.fill_between(fam_curve*100, 36 - dBin_total, eps_pred,
                  color='#f59e0b', alpha=0.4, label='Δε Plastic (Heckel)')
ax.plot(fam_curve*100, eps_pred, 'k-', lw=2.5, label='ε prediction')
ax.axhline(36, color='gray', ls=':', lw=1, label='ε_RCP = 36%')

# Regime weights inset
ax2 = ax.inset_axes([0.62, 0.62, 0.36, 0.35])
ax2.plot(fam_curve*100, ws_F, '#3b82f6', lw=2, label='w_F (Furnas)')
ax2.plot(fam_curve*100, ws_M, '#dc2626', lw=2, label='w_M (Matrix)')
ax2.set_xlabel('AM_wt%', fontsize=9); ax2.set_ylabel('weight', fontsize=9)
ax2.set_title('Regime weights', fontsize=9)
ax2.legend(fontsize=8, loc='center right'); ax2.grid(alpha=0.3)
ax2.set_xlim(50, 99); ax2.set_ylim(-0.05, 1.05)

ax.set_xlabel('AM weight fraction (%)', fontsize=12)
ax.set_ylabel('Porosity ε (%)', fontsize=12)
ax.set_title('(c)  Term-by-term decomposition at λ=7\n'
              '            sin-wave hump = Furnas valley × regime weight',
              fontsize=12, loc='left')
ax.legend(loc='lower left', fontsize=9)
ax.set_xlim(50, 99); ax.set_ylim(0, 40)

# Panel (d) — Outlier diagnostic -----------------------------------
ax = fig.add_subplot(gs[1, 1])
for c in sorted(set(CAMP)):
    idx = [i for i,cc in enumerate(CAMP) if cc==c]
    ax.scatter([F_AM[i]*100 for i in idx], [resid[i] for i in idx],
                c=camp_colors[c], s=55, edgecolors='black', linewidths=0.6,
                label=camp_lab[c], zorder=5)
# Outliers
for i, cid in enumerate(CID):
    if cid in OUTLIERS:
        ax.annotate(f' {OUTLIERS[cid]}: {cid.replace("input_","")}',
                     (F_AM[i]*100, resid[i]),
                     fontsize=9, color='red', zorder=20)
        ax.scatter(F_AM[i]*100, resid[i], s=200, marker='o',
                    facecolors='none', edgecolors='red', linewidths=2, zorder=15)
ax.axhline(0, color='k', lw=1.5)
ax.axhline(2, color='gray', lw=0.6, ls=':'); ax.axhline(-2, color='gray', lw=0.6, ls=':')
ax.axhspan(-2, 2, color='gray', alpha=0.1, zorder=0)
# Group annotation
ax.text(86, -9, 'Group A:\nsingle-layer AM_P\n(D_P > 0.5·thickness)',
        ha='center', fontsize=9, color='red',
        bbox=dict(boxstyle='round', facecolor='white', edgecolor='red'))
ax.text(78, 6, 'Groups B,E:\ntrimodal deep packing\n(model under-predicts ε)',
        ha='center', fontsize=9, color='red',
        bbox=dict(boxstyle='round', facecolor='white', edgecolor='red'))
ax.set_xlabel('AM weight fraction (%)', fontsize=12)
ax.set_ylabel('Residual (pred − meas) (%p)', fontsize=12)
ax.set_title('(d)  Residual diagnostic — outliers self-cluster\n'
              '            mostly within ±2 %p (ML noise floor band)',
              fontsize=12, loc='left')
ax.legend(loc='lower left', fontsize=9)
ax.grid(alpha=0.3); ax.set_ylim(-10, 9)

plt.suptitle('2D porosity surface ε(AM_wt, λ_eff) — v4 physics fit (82-case DEM corpus)',
              fontsize=14, fontweight='bold', y=0.995)
plt.savefig('docs/figures/porosity_v4_paper_figure.png', dpi=150,
             bbox_inches='tight')
print('Figure saved: docs/figures/porosity_v4_paper_figure.png')
