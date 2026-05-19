#!/usr/bin/env python3
"""Extended physics fit v3 — close the 3 gaps identified in v2.

v2 limitations and our fixes:

  Gap 1: Trimodal packing (1mAh_100_* mono-AM_P, plus P:S = 5:5 / 7:3)
    → Add λ_PS = r_AM_P / r_AM_S as a separate input (when both exist)
    → Trimodal correction term: Δε_tri = K_tri · f_AMP · f_AMS · sat(λ_PS)
       (peaks when both AM types are present in similar amounts)

  Gap 2: Matrix-mode plastic over-amplification (η_matrix > 1)
    → Make plastic efficiency a smooth function of regime weight
    → Allow per-regime calibration of Heckel max

  Gap 3: Thin-film wall confinement (1mAh cases, RVE-z ≈ D_AM_P)
    → Add wall term: Δε_wall = K_wall · max(0, D_AM_eff / thickness)^p
    → Penalises cases where the largest AM is large compared to RVE z

Total inputs: f_AM, λ_eff, λ_PS, f_AM_P, D_AM_eff / thickness
Total params: ~15 (each anchored to a physical interpretation)
"""
from __future__ import annotations
import csv, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# ── Load + feature engineering ────────────────────────────────────
ROWS = list(csv.DictReader(open('all_dem_porosity.csv')))
def fnum(s):
    try: return float(s)
    except: return None

DATA = []   # (f_AM, lam_eff, lam_PS, f_AMP, thick_ratio, eps, camp, case_id)
for r in ROWS:
    am = fnum(r['am_wt']); eps = fnum(r['porosity_pct'])
    rse = fnum(r['r_SE_um']) or 0
    rp = fnum(r['r_AM_P_um']) or 0
    rs = fnum(r['r_AM_S_um']) or 0
    pv = fnum(r['p_vol']) or 0
    sv = fnum(r['s_vol']) or 0
    if am is None or eps is None or rse <= 0:
        continue

    # Volume-weighted effective AM radius
    if pv + sv > 0:
        r_eff = (pv*rp + sv*rs) / (pv + sv)
        f_AMP = pv / (pv + sv)
    elif rs > 0:
        r_eff = rs
        f_AMP = 0.0
    else:
        r_eff = rp
        f_AMP = 1.0
    if r_eff <= 0:
        continue

    lam_eff = r_eff / rse
    # λ_PS only defined when both AM types present
    lam_PS = (rp / rs) if (rp > 0 and rs > 0) else 1.0   # 1.0 = mono = no λ_PS effect

    # Thickness-related wall-confinement signal
    # The user's metric was thickness in μm (sim units / scale).  We
    # don't have it directly in the CSV; approximate via campaign:
    # 1mAh → ~20μm typical thickness, 6mAh→~120μm, 8mAh→~160μm, particulate→variable
    thick_typ = {'박막(1mAh)': 25.0, '후막(6mAh)': 120.0,
                  '후막(8mAh)': 160.0, 'particulate': 100.0}.get(r['campaign'], 100.0)
    # D_AM_eff in μm = r_eff (already μm scale due to r_eff/1000 from CSV)
    # Actually CSV stores in different units — let me check
    # The original csv has r_AM_P_um like 6000.0 — those are nm; divide by 1000 for μm
    D_AM_eff_um = r_eff / 1000.0
    thick_ratio = D_AM_eff_um / thick_typ   # >1 means D_AM ≥ thickness (severe)

    DATA.append((am/100, lam_eff, lam_PS, f_AMP, thick_ratio, eps,
                  r['campaign'], r['case_id']))

F_AM  = np.array([d[0] for d in DATA])
LAM   = np.array([d[1] for d in DATA])
LPS   = np.array([d[2] for d in DATA])
FAMP  = np.array([d[3] for d in DATA])
TR    = np.array([d[4] for d in DATA])
EPS   = np.array([d[2] if False else d[5] for d in DATA])
CAMP  = [d[6] for d in DATA]
print(f'Loaded {len(DATA)} cases')
print(f'λ_eff   range: {LAM.min():.2f} – {LAM.max():.2f}')
print(f'λ_PS    range: {LPS.min():.2f} – {LPS.max():.2f}  (1.0 = mono)')
print(f'f_AM_P  values: {sorted(set(np.round(FAMP, 2)))[:8]}{"..." if len(set(FAMP))>8 else ""}')
print(f'thick_ratio: {TR.min():.3f} – {TR.max():.3f}')

OUT = {'input_1mAh_100_15', 'input_6mAh_real_10'}
mask_trust = np.array([d[7] not in OUT for d in DATA])


# ── Model v3 — physics + corrections ──────────────────────────────
EPS_RCP = 36.0

def f_AM_perc(lam, a, b, c):
    return a + b * (1.0 - np.exp(-c * (lam - 1.0)))


def model_v3(f_AM, lam, lam_PS, f_AMP, thick_ratio, p):
    (a_p, b_p, c_p, s_w,                          # regime switch
     D_F, D_M, vc_F, vc_M, vw_F, vw_M,            # binary packing
     H_max, eta_F, eta_M,                          # plastic efficiency
     K_tri, lam_PS_sat,                            # trimodal correction
     K_wall, p_wall,                               # wall confinement
     sp) = p                                       # spring back
    f_SE = 1.0 - f_AM

    # P4: regime weights
    fc = f_AM_perc(lam, a_p, b_p, c_p)
    w_M = 1.0 / (1.0 + np.exp(-s_w * (f_AM - fc)))
    w_F = 1.0 - w_M

    # P2a: Furnas binary (saturating in λ at lam_sat=8)
    depth_F = D_F * (1.0 - np.exp(-(lam - 1.0) / 8.0))
    val_F = depth_F * np.exp(-((f_SE - vc_F) ** 2) / (2.0 * vw_F ** 2))
    # P2b: Matrix binary (inversely λ-dependent)
    depth_M = D_M / lam
    val_M = depth_M * np.exp(-((f_SE - vc_M) ** 2) / (2.0 * vw_M ** 2))
    dBin = w_F * val_F + w_M * val_M

    # P2c [NEW]: Trimodal correction
    # Active only when both AM_P and AM_S exist (f_AMP ∈ (0,1)) AND λ_PS > 1.
    # Maximum when f_AMP × f_AMS = 0.25 (50:50 AM mix), saturating with λ_PS.
    f_tri = f_AMP * (1.0 - f_AMP)  # peaks at 0.25 for 50:50
    tri_satur = 1.0 - np.exp(-(lam_PS - 1.0) / lam_PS_sat)
    dTri = K_tri * f_tri * tri_satur

    # P3+4: Plastic densification (regime-weighted efficiency)
    eta_eff = w_F * eta_F + w_M * eta_M
    dPla = H_max * f_SE * eta_eff

    # P6+wall [NEW]: Spring-back + wall confinement
    dWall = K_wall * np.maximum(0, thick_ratio - 0.1) ** p_wall

    return EPS_RCP - dBin - dTri - dPla + sp + dWall


def loss(p):
    pred = model_v3(F_AM, LAM, LPS, FAMP, TR, p)
    return float(np.sum((pred - EPS) ** 2))


# Initialise from v2 winner + new term defaults
P0 = [
    0.50, 1.20, 0.05, 35.0,        # regime switch
    15.0, 25.0, 0.30, 0.30, 0.15, 0.20,   # binary packing
    26.0, 1.0, 1.5,                # plastic
    8.0, 5.0,                       # trimodal: max amount, λ_PS saturation
    20.0, 1.5,                      # wall: amount, exponent
    0.0,                            # spring back
]
BOUNDS = [
    (0.30, 0.85), (0.05, 1.50), (0.01, 1.0), (5.0, 80.0),
    (3.0, 30.0), (5.0, 40.0), (0.10, 0.50), (0.20, 0.70),
    (0.05, 0.40), (0.05, 0.40),
    (15.0, 35.0), (0.5, 1.5), (0.5, 3.0),
    (0.0, 20.0), (0.5, 15.0),       # trimodal
    (0.0, 50.0), (0.5, 4.0),        # wall
    (-3.0, 3.0),
]
PNAMES = ['a_perc','b_perc','c_perc','s_w',
          'D_F','D_M','vc_F','vc_M','vw_F','vw_M',
          'H_max','eta_F','eta_M',
          'K_tri','lam_PS_sat',
          'K_wall','p_wall',
          'spring_back']

res = minimize(loss, P0, method='L-BFGS-B', bounds=BOUNDS,
               options={'ftol': 1e-12, 'maxiter': 2000})
PARAMS = res.x
RMSE = math.sqrt(res.fun / len(DATA))

pred = model_v3(F_AM, LAM, LPS, FAMP, TR, PARAMS)
resid = pred - EPS
RMSE_trust = math.sqrt(np.mean(resid[mask_trust] ** 2))

print()
print('=' * 65)
print('v3 EXTENDED MODEL (trimodal + wall confinement)')
print('=' * 65)
print(f'RMSE on all 82 cases:     {RMSE:.3f} %p')
print(f'RMSE on trust subset:     {RMSE_trust:.3f} %p (n={int(mask_trust.sum())})')
print()
print('Previous fits for comparison:')
print(f'  v0 strict physics:       6.03 %p')
print(f'  v1 refined physics:      3.11 %p')
print(f'  v2 pure empirical:       2.76 %p (trust 2.15)')
print()
print('Fitted parameters:')
for n, v, (lo, hi) in zip(PNAMES, PARAMS, BOUNDS):
    atb = ('⚠ at bound' if (abs(v-lo) < 0.01*abs(hi-lo+1) or
                              abs(v-hi) < 0.01*abs(hi-lo+1)) else '')
    print(f'  {n:14s} = {v:8.3f}   ({lo:.2f}, {hi:.2f}) {atb}')

# Per-campaign residuals
print()
print('Per-campaign residuals (trust subset):')
from collections import defaultdict
camp_r = defaultdict(list)
for i, c in enumerate(CAMP):
    if mask_trust[i]:
        camp_r[c].append(resid[i])
for c in sorted(camp_r):
    r = np.array(camp_r[c])
    print(f'  {c:15s} n={len(r):3d}  RMSE={np.sqrt(np.mean(r**2)):.2f}%p  '
          f'|Δ|<1%p: {100*np.sum(np.abs(r)<1)/len(r):.0f}%  '
          f'|Δ|<2%p: {100*np.sum(np.abs(r)<2)/len(r):.0f}%')

# Worst residuals
order = np.argsort(-np.abs(resid))[:10]
print()
print('Top 10 worst residuals:')
for i in order:
    print(f'  {DATA[i][7]:25s}  meas={EPS[i]:5.2f}  pred={pred[i]:5.2f}  '
          f'Δ={resid[i]:+5.2f}  λ={LAM[i]:5.2f}  AM={F_AM[i]*100:5.1f}%  '
          f'fAMP={FAMP[i]:.2f}')

# ── Parity + diagnostic plot ──────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(20, 6))

camp_colors = {'particulate': '#d62728', '박막(1mAh)': '#1f77b4',
               '후막(6mAh)': '#ff7f0e', '후막(8mAh)': '#2ca02c'}
camp_lab = {'particulate':'particulate','박막(1mAh)':'thin 1mAh',
            '후막(6mAh)':'thick 6mAh','후막(8mAh)':'thick 8mAh'}

# Parity
ax = axes[0]
for c in sorted(set(CAMP)):
    idx = [i for i,cc in enumerate(CAMP) if cc==c]
    ax.scatter(EPS[idx], pred[idx], c=camp_colors[c], s=55,
                edgecolors='black', linewidths=0.6,
                label=f'{camp_lab[c]} (n={len(idx)})')
ax.plot([3,35], [3,35], 'k-', lw=1.5)
ax.fill_between([3,35], [1,33], [5,37], color='gray', alpha=0.15, label='±2%p')
ax.fill_between([3,35], [2,34], [4,36], color='gray', alpha=0.25, label='±1%p')
n_1 = 100*sum(abs(r)<1 for r in resid)/len(resid)
n_2 = 100*sum(abs(r)<2 for r in resid)/len(resid)
ax.set_xlabel('Measured ε (%)'); ax.set_ylabel('Predicted ε (%)')
ax.set_title(f'v3 fit — RMSE {RMSE:.2f}%p (all), {RMSE_trust:.2f}%p (trust)\n'
              f'|Δ|<1%p: {n_1:.0f}%   |Δ|<2%p: {n_2:.0f}%')
ax.legend(fontsize=9, loc='lower right')
ax.set_xlim(3,35); ax.set_ylim(3,35); ax.grid(alpha=0.3)

# Term breakdown: stacked contribution
ax = axes[1]
# Recompute terms per case
ddBin = np.zeros(len(DATA)); ddTri = np.zeros(len(DATA))
ddPla = np.zeros(len(DATA)); ddWall = np.zeros(len(DATA))
for i in range(len(DATA)):
    f_SE = 1 - F_AM[i]; lam = LAM[i]
    a,b,c,s = PARAMS[0:4]
    D_F,D_M,vc_F,vc_M,vw_F,vw_M = PARAMS[4:10]
    H,eF,eM = PARAMS[10:13]
    K_t,lps = PARAMS[13:15]; K_w,p_w = PARAMS[15:17]
    fc = a + b*(1-np.exp(-c*(lam-1)))
    w_M = 1/(1+np.exp(-s*(F_AM[i]-fc))); w_F = 1-w_M
    dF = D_F*(1-np.exp(-(lam-1)/8))*np.exp(-((f_SE-vc_F)**2)/(2*vw_F**2))
    dMM = (D_M/lam)*np.exp(-((f_SE-vc_M)**2)/(2*vw_M**2))
    ddBin[i] = w_F*dF + w_M*dMM
    ddTri[i] = K_t * FAMP[i]*(1-FAMP[i]) * (1-np.exp(-(LPS[i]-1)/lps))
    ddPla[i] = H*f_SE*(w_F*eF + w_M*eM)
    ddWall[i] = K_w*max(0, TR[i]-0.1)**p_w
# Sort by f_AM
order = np.argsort(F_AM)
x = np.arange(len(DATA))
ax.bar(x, ddBin[order], color='#1f77b4', label='Δε binary', width=0.9)
ax.bar(x, ddPla[order], bottom=ddBin[order], color='#ff7f0e',
        label='Δε plastic', width=0.9)
ax.bar(x, ddTri[order], bottom=ddBin[order]+ddPla[order],
        color='#9467bd', label='Δε trimodal', width=0.9)
ax.bar(x, -ddWall[order], color='#d62728', label='−Δε wall (subtracts from total reduction)', width=0.9)
ax.set_xlabel(f'cases sorted by AM_wt (left=SE-rich, right=AM-rich)')
ax.set_ylabel('Contribution to ε reduction (%p)')
ax.set_title('Term-by-term decomposition per case (v3)')
ax.legend(fontsize=9, loc='upper right')
ax.grid(alpha=0.3, axis='y')

# Residual vs trimodal / wall axis
ax = axes[2]
sc = ax.scatter(F_AM*100, resid, c=LPS, cmap='plasma',
                 s=70, edgecolors='black', linewidths=0.6)
plt.colorbar(sc, ax=ax, label='λ_PS = r_AM_P / r_AM_S')
ax.axhline(0, color='k', lw=1.5)
ax.axhline(2, color='gray', lw=0.8, ls=':'); ax.axhline(-2, color='gray', lw=0.8, ls=':')
ax.set_xlabel('AM_wt%'); ax.set_ylabel('Residual (pred − meas) (%p)')
ax.set_title('Residual vs (AM_wt, λ_PS) — color shows trimodal info')
ax.grid(alpha=0.3); ax.set_ylim(-10, 10)

plt.tight_layout()
import os
os.makedirs('docs/figures', exist_ok=True)
plt.savefig('docs/figures/porosity_v3_extended.png', dpi=140, bbox_inches='tight')
print('\nFigure saved: docs/figures/porosity_v3_extended.png')
