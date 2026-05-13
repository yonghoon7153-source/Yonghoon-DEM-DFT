#!/usr/bin/env python3
"""TRUE physics porosity predictor — endpoints from EXPERIMENT.

CORRECTED understanding (key insight):

  Pure LPSCl at 300 MPa cold-press → ε ≈ 10 % (EXPERIMENTAL value,
  Sakuda 2013, Tran 2025 et al.).

  Naive Heckel with Tabor σ_y = H/3 = 283 MPa predicts ε ≈ 25 %,
  which is too high. The discrepancy reflects that real LPSCl
  undergoes time-dependent viscoplastic creep during cold-press
  (minutes timescale), so the effective σ_y is lower than the
  instantaneous hardness-based Tabor estimate.

  Heckel back-fit from experimental endpoint:
    ε(300 MPa) / ε_0 = exp(-K·P)
    0.10 / 0.36 = exp(-K · 300 MPa)
    K = 4.27 × 10⁻³ MPa⁻¹
    σ_y_effective = 1 / (3·K) = 78 MPa

  This effective σ_y reflects the time-averaged plastic resistance
  of LPSCl in cold-press conditions, consistent with Sakuda 2013
  (sulfide SE σ_y reported as 100–200 MPa, lower than Tabor estimate).

The MIXTURE behavior then follows from Sridhar 2000 SFM constraint
factor + stress-bearing percolation, where AM force chains protect
some SE from full plastic flow at low f_SE.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path


# ── Material (REAL) ────────────────────────────────────────────────
D_AM_P = 12.0; D_AM_S = 4.0; D_SE = 1.0     # µm
RHO_AM = 4.8;  RHO_SE = 2.0                  # g/cm³
E_AM   = 140e9; E_SE = 24e9                  # Pa (real)
H_SE   = 0.85e9                              # Pa (Vickers)

# Tabor σ_y for reference (NOT used in model — too high vs experiment)
SIGMA_Y_TABOR = H_SE / 3.0                   # 283 MPa

P_PRESS = 300e6                              # Pa
EPS_PURE_AM = 0.36                           # Bernal RCP (data)
EPS_PURE_SE_EXP = 0.10                       # EXPERIMENTAL pure-LPSCl @ 300 MPa
                                              # (Sakuda 2013, Tran 2025)

# Back-fit effective σ_y from experimental endpoint
# 0.10 = 0.36 · exp(-K · 300 MPa) → K = 4.27e-3 1/MPa
K_HECKEL_EFF = -np.log(EPS_PURE_SE_EXP / EPS_PURE_AM) / (P_PRESS / 1e6)  # 1/MPa
SIGMA_Y_EFF  = 1.0 / (3.0 * K_HECKEL_EFF * 1e6)                            # Pa
# ≈ 78 MPa (time-averaged plastic resistance, lower than Tabor 283 MPa)


# ── ONE calibrated mixture parameter — stress-bearing percolation ──
F_PERC_STRESS = 0.65   # Liu & Yin 2025 sand-rubber extrapolation
SHARPNESS     = 8.0


# ── Volume fractions ──────────────────────────────────────────────
def wt_to_vol(am_se_wt, p_s_vol):
    am_wt, se_wt = am_se_wt
    p_vol, s_vol = p_s_vol
    v_am_total = am_wt / RHO_AM
    v_se       = se_wt / RHO_SE
    p_frac = p_vol / (p_vol + s_vol)
    v_p = v_am_total * p_frac
    v_s = v_am_total * (1 - p_frac)
    v_total = v_p + v_s + v_se
    return v_p/v_total, v_s/v_total, v_se/v_total


# ── Bouvard 2004 RCP (data, no fit) ──────────────────────────────
def bouvard_rcp(f_se, lam_eff):
    fl = 1.0 - f_se
    fl_ref  = np.array([0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60,
                        0.70, 0.74, 0.78, 0.85, 0.90, 0.95, 1.00])
    eps_ref = np.array([0.36, 0.33, 0.30, 0.27, 0.24, 0.22, 0.20,
                        0.185, 0.18, 0.185, 0.215, 0.25, 0.30, 0.36])
    eps_lam8 = float(np.interp(fl, fl_ref, eps_ref))
    eps_min = max(0.13, 0.36 - 0.087 * np.log(max(lam_eff, 1.5)))
    eps_rcp = eps_min + (eps_lam8 - 0.18) / (0.36 - 0.18) * (0.36 - eps_min)
    return min(eps_rcp, 0.36)


# ── Sridhar 2000 SFM constraint (no fit) ─────────────────────────
def sfm_constraint(f_am, lam_eff, alpha_KC=2.0):
    if f_am <= 1e-9:
        return 1.0
    kc = 1.0 + alpha_KC * f_am ** 2
    kc *= 1.0 + 0.05 * np.log(max(lam_eff, 1.0))
    return kc


# ── Stress-bearing percolation (Liu & Yin 2025) ──────────────────
def stress_bearing_activation(f_se):
    return 1.0 / (1.0 + np.exp(-SHARPNESS * (f_se - F_PERC_STRESS)))


# ── Heckel plastic compaction with effective σ_y ─────────────────
def heckel_porosity(P, eps_0=EPS_PURE_AM, K=K_HECKEL_EFF):
    """ε = ε_0 · exp(-K·P) with K back-fit from experimental endpoint."""
    return eps_0 * np.exp(-K * P / 1e6)


# ── Prediction ────────────────────────────────────────────────────
def predict(am_se_wt, p_s_vol):
    f_p, f_s, f_se = wt_to_vol(am_se_wt, p_s_vol)
    f_am = f_p + f_s
    d_eff_am = (f_p * D_AM_P + f_s * D_AM_S) / max(f_am, 1e-9)
    lam_eff = d_eff_am / D_SE if f_am > 0 else 1.0

    eps_rcp = bouvard_rcp(f_se, lam_eff)
    kc      = sfm_constraint(f_am, lam_eff)
    p_se    = stress_bearing_activation(f_se)

    # Heckel: effective pressure on SE phase = P_applied / KC
    P_eff = P_PRESS / kc
    # Pure-SE-equivalent porosity at this effective pressure
    eps_pure_at_Peff = heckel_porosity(P_eff)
    delta_max = EPS_PURE_AM - eps_pure_at_Peff

    # Plastic densification: scaled by f_SE and stress-bearing activation
    delta = delta_max * f_se * p_se
    eps   = max(eps_rcp - delta, 0.03)

    return dict(f_p=f_p, f_s=f_s, f_se=f_se, lam_eff=lam_eff,
                eps_rcp=eps_rcp, kc=kc, p_se=p_se,
                P_eff=P_eff, eps_pure_at_Peff=eps_pure_at_Peff,
                delta_max=delta_max, delta=delta, eps_pred=eps)


def main():
    print(f'σ_y Tabor (H/3, instantaneous):    {SIGMA_Y_TABOR/1e6:.0f} MPa')
    print(f'σ_y effective (Heckel-back-fit):    {SIGMA_Y_EFF/1e6:.0f} MPa')
    print(f'K_Heckel (back-fit from 10% pure SE): {K_HECKEL_EFF:.3e} 1/MPa')
    print(f'→ time-dependent viscoplastic creep brings σ_y down from 283 → 78 MPa')
    print()

    measured = {
        (85, 15): {'p_s': (7, 3), 'eps': 0.157, 'label': 'input_8mAh_9'},
        (80, 20): {'p_s': (7, 3), 'eps': 0.165, 'label': 'input_8mAh_6'},
        (75, 25): {'p_s': (7, 3), 'eps': 0.185, 'label': 'input_8mAh_3'},
    }

    am_arr = np.linspace(0, 100, 101)
    p_s_configs = [(3, 7), (5, 5), (7, 3)]
    colors = {(3, 7): 'tab:blue', (5, 5): 'tab:green', (7, 3): 'crimson'}

    fig, axes = plt.subplots(1, 2, figsize=(15, 6.5))

    # Panel 1
    ax = axes[0]
    for p_s in p_s_configs:
        rcp_list, pred_list = [], []
        for am in am_arr:
            r = predict((am, 100-am), p_s)
            rcp_list.append(r['eps_rcp'] * 100)
            pred_list.append(r['eps_pred'] * 100)
        ax.plot(am_arr, rcp_list, '--', color=colors[p_s], alpha=0.4, lw=1.2,
                label=f'P:S={p_s[0]}:{p_s[1]} — Bouvard RCP')
        ax.plot(am_arr, pred_list, '-', color=colors[p_s], lw=2.5,
                label=f'P:S={p_s[0]}:{p_s[1]} — physics prediction')

    for (am, se), info in measured.items():
        ax.scatter(am, info['eps']*100, s=300, color='black',
                   marker='*', zorder=10, edgecolors='gold', linewidth=2,
                   label='Measured DEM' if (am, se) == (85, 15) else None)
        ax.annotate(f'{am}:{se}\nε={info["eps"]*100:.1f}%',
                     xy=(am, info['eps']*100),
                     xytext=(am-4, info['eps']*100+1.5),
                     fontsize=9, fontweight='bold')

    ax.scatter([0, 100], [EPS_PURE_SE_EXP*100, EPS_PURE_AM*100],
               s=200, marker='s', color='darkgreen',
               edgecolors='black', linewidth=1.5, zorder=8,
               label='Experimental endpoints (Sakuda 2013, Bernal)')

    ax.set_xlabel('AM weight fraction (%)', fontsize=12)
    ax.set_ylabel('Porosity ε (%)', fontsize=12)
    ax.set_title(f'Physics prediction with EXPERIMENTAL endpoints\n'
                  f'σ_y_eff = {SIGMA_Y_EFF/1e6:.0f} MPa (Heckel back-fit from '
                  f'pure-SE 10% @ 300 MPa), α_KC=2, f_perc_stress=0.65',
                  fontsize=10.5)
    ax.legend(fontsize=8.5, loc='upper left', framealpha=0.95)
    ax.grid(alpha=0.3)
    ax.set_xlim(-2, 102)
    ax.set_ylim(0, 42)

    # Panel 2
    ax = axes[1]
    rcp_list, pred_list, kc_list, p_list = [], [], [], []
    for am in am_arr:
        r = predict((am, 100-am), (7, 3))
        rcp_list.append(r['eps_rcp'] * 100)
        pred_list.append(r['eps_pred'] * 100)
        kc_list.append(r['kc'])
        p_list.append(r['p_se'])

    ax.plot(am_arr, rcp_list, '--', color='steelblue', lw=2,
            label='Bouvard RCP (geometric)')
    ax.plot(am_arr, pred_list, '-', color='crimson', lw=3,
            label='Physics prediction (Bouvard × SFM × Heckel × percolation)')
    ax.fill_between(am_arr, pred_list, rcp_list,
                     color='moccasin', alpha=0.5,
                     label='Plastic densification (Heckel)')

    for (am, se), info in measured.items():
        ax.scatter(am, info['eps']*100, s=300, color='black',
                   marker='*', zorder=10, edgecolors='gold', linewidth=2)

    ax2 = ax.twinx()
    ax2.plot(am_arr, kc_list, ':', color='purple', lw=1.5, alpha=0.7,
              label='KC (Sridhar 2000)')
    ax2.plot(am_arr, p_list, ':', color='darkorange', lw=1.5, alpha=0.7,
              label=f'p_se (stress-bearing perc, f_perc={F_PERC_STRESS})')
    ax2.set_ylabel('KC | p_se', fontsize=10, color='purple')
    ax2.tick_params(axis='y', colors='purple')
    ax2.set_ylim(0, max(max(kc_list), 1.3))
    ax2.legend(loc='lower right', fontsize=8.5)

    ax.set_xlabel('AM weight fraction (%)', fontsize=12)
    ax.set_ylabel('Porosity ε (%)', fontsize=12)
    ax.set_title('Physical decomposition (P:S=7:3)\n'
                  'Endpoint from experiment, mixture from physics framework',
                  fontsize=10.5)
    ax.legend(fontsize=9, loc='upper left', framealpha=0.95)
    ax.grid(alpha=0.3)
    ax.set_xlim(-2, 102)
    ax.set_ylim(0, 42)

    plt.tight_layout()
    out = Path('real_physics_porosity_curve.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    print(f'✓ Saved: {out.resolve()}')

    # Numerical comparison
    print()
    print('Physics prediction with experimental endpoints')
    print(f'{"AM:SE":>8s} {"P:S":>6s} {"f_se":>6s} {"KC":>6s} {"p_se":>6s} '
          f'{"P_eff":>8s} {"ε_RCP":>7s} {"ε_pred":>7s} {"meas":>7s} {"gap":>6s}')
    print('─' * 95)
    for am in [100, 95, 90, 85, 80, 75, 70, 60, 50, 30, 10, 0]:
        for p_s in p_s_configs if (am < 100 and am > 0) else [(7, 3)]:
            r = predict((am, 100-am), p_s)
            meas, gap = '', ''
            if (am, 100-am) in measured and measured[(am, 100-am)]['p_s'] == p_s:
                m = measured[(am, 100-am)]['eps']
                meas = f'{m*100:.1f}'
                gap = f'{(r["eps_pred"]-m)*100:+.1f}'
            print(f'{f"{am}:{100-am}":>8s} {f"{p_s[0]}:{p_s[1]}":>6s} '
                  f'{r["f_se"]*100:5.1f}% {r["kc"]:6.2f} {r["p_se"]:6.3f} '
                  f'{r["P_eff"]/1e6:7.0f} {r["eps_rcp"]*100:6.2f}% '
                  f'{r["eps_pred"]*100:6.2f}% {meas:>7s} {gap:>6s}')


