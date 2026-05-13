#!/usr/bin/env python3
"""REAL physics porosity predictor — no endpoint calibration trick.

Uses bare material parameters directly. No "E_SE = 1.35 GPa effective"
trick to force pure SE = 10 %. Pure SE prediction comes from real
Heckel + Tabor with experimental σ_y.

KEY REALIZATION:
  Real LPSCl pure pellet at 300 MPa cold-press has porosity ε ≈ 20-25 %
  (Sakuda 2013: ~25 % at 360 MPa; Tran 2025: ~15 % at 350 MPa).
  Our DEM's "pure SE = 10 %" endpoint was artificially achieved by
  calibrating E_SE = 1.35 GPa (1/18 of real 24 GPa), which is
  NOT a physical Young's modulus. For pure SE, real physics says
  ε ≈ 25 %, not 10 %.

For MIXTURES, however, real physics predicts ε values that closely
match our DEM measurements. The DEM result is actually MORE
realistic for mixed composites than for the (artificially calibrated)
pure SE endpoint.

ALL PARAMETERS FROM PUBLISHED PHYSICS (no fit):
  - σ_y_SE = H/3 = 283 MPa     (Tabor 1948, H = 0.85 GPa McGrogan 2017)
  - K_Heckel = 1/(3 σ_y)        (Heckel 1961)
  - eps_pure_SE @ 300 MPa = 25.3 %  (Heckel prediction, no fit)
  - eps_pure_AM = 0.36          (Bernal RCP, no fit)
  - α_KC = 2                    (Sridhar 2000 typical)
  - Bouvard 2004 RCP curve      (data interpolation)
  - Geometric percolation = 0.30 (Scher-Zallen 1970 classical)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path


# ── Material (REAL, no tuning) ─────────────────────────────────────
D_AM_P  = 12.0; D_AM_S = 4.0; D_SE = 1.0   # µm
RHO_AM  = 4.8;  RHO_SE = 2.0               # g/cm³
E_AM    = 140e9; E_SE  = 24e9              # Pa  ← real LPSCl modulus
H_SE    = 0.85e9                            # Pa  Vickers hardness
SIGMA_Y_SE = H_SE / 3.0                     # 283 MPa via Tabor 1948

P_PRESS = 300e6                             # Pa

EPS_PURE_AM = 0.36                          # Bernal RCP


# ── Heckel 1961: real pure-SE porosity at given P ─────────────────
def heckel_pure_se(P=P_PRESS, sigma_y=SIGMA_Y_SE, eps_0=EPS_PURE_AM):
    """Pure-SE cold-press porosity from Heckel equation.

    ε = ε_0 · exp(-K · P),   K = 1/(3·σ_y)

    For σ_y = 283 MPa, P = 300 MPa:
      K·P = 0.353  →  ε ≈ 0.36 · 0.703 ≈ 25.3 %
    """
    K = 1.0 / (3.0 * sigma_y)
    return eps_0 * np.exp(-K * P)

EPS_PURE_SE_real = heckel_pure_se()           # ≈ 0.253 at 300 MPa


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


# ── Geometric SE percolation (Scher-Zallen 1970) ─────────────────
def geometric_percolation(f_se, f_perc=0.30, sharpness=8.0):
    return 1.0 / (1.0 + np.exp(-sharpness * (f_se - f_perc)))


# ── REAL physics prediction ──────────────────────────────────────
def predict_real(am_se_wt, p_s_vol):
    f_p, f_s, f_se = wt_to_vol(am_se_wt, p_s_vol)
    f_am = f_p + f_s
    d_eff_am = (f_p * D_AM_P + f_s * D_AM_S) / max(f_am, 1e-9)
    lam_eff = d_eff_am / D_SE if f_am > 0 else 1.0

    eps_rcp = bouvard_rcp(f_se, lam_eff)
    kc      = sfm_constraint(f_am, lam_eff)
    p_se    = geometric_percolation(f_se)

    # Heckel plastic contribution (real σ_y)
    delta_max = EPS_PURE_AM - EPS_PURE_SE_real   # ≈ 0.107
    delta = delta_max * f_se * p_se / kc
    eps   = max(eps_rcp - delta, 0.03)

    return dict(f_p=f_p, f_s=f_s, f_se=f_se, lam_eff=lam_eff,
                eps_rcp=eps_rcp, kc=kc, p_se=p_se,
                delta=delta, eps_pred=eps)


def main():
    print(f'Real Heckel pure-SE porosity at P={P_PRESS/1e6:.0f} MPa, '
          f'σ_y={SIGMA_Y_SE/1e6:.0f} MPa: {EPS_PURE_SE_real*100:.1f}%')
    print(f'  (= 36 % × exp(-K·P), K = 1/(3·σ_y) = '
          f'{1/(3*SIGMA_Y_SE)*1e9:.3f} 1/GPa)')
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

    # Panel 1: full sweep
    ax = axes[0]
    for p_s in p_s_configs:
        rcp_list, pred_list = [], []
        for am in am_arr:
            r = predict_real((am, 100-am), p_s)
            rcp_list.append(r['eps_rcp'] * 100)
            pred_list.append(r['eps_pred'] * 100)
        ax.plot(am_arr, rcp_list, '--', color=colors[p_s], alpha=0.4, lw=1.2,
                label=f'P:S={p_s[0]}:{p_s[1]} — Bouvard RCP')
        ax.plot(am_arr, pred_list, '-', color=colors[p_s], lw=2.5,
                label=f'P:S={p_s[0]}:{p_s[1]} — real-physics prediction')

    for (am, se), info in measured.items():
        ax.scatter(am, info['eps']*100, s=300, color='black',
                   marker='*', zorder=10,
                   edgecolors='gold', linewidth=2,
                   label='Measured DEM (P:S=7:3)' if (am, se) == (85, 15) else None)
        ax.annotate(f'{am}:{se}\nε={info["eps"]*100:.1f}%',
                     xy=(am, info['eps']*100),
                     xytext=(am-4, info['eps']*100+1.5),
                     fontsize=9, fontweight='bold')

    # Mark real pure-SE endpoint (NOT 10 %)
    ax.scatter([0, 100], [EPS_PURE_SE_real*100, EPS_PURE_AM*100],
               s=200, marker='s', color='darkgreen',
               edgecolors='black', linewidth=1.5, zorder=8,
               label=f'Heckel real endpoints (pure-SE={EPS_PURE_SE_real*100:.1f}%, '
                     f'pure-AM={EPS_PURE_AM*100:.0f}%)')

    ax.set_xlabel('AM weight fraction (%)', fontsize=12)
    ax.set_ylabel('Porosity ε (%)', fontsize=12)
    ax.set_title('REAL physics — no parameter tuning, real material values\n'
                  f'σ_y_SE=283 MPa (Tabor), E_SE=24 GPa, α_KC=2, '
                  f'f_perc=0.30 (geometric)', fontsize=10.5)
    ax.legend(fontsize=8.5, loc='upper left', framealpha=0.95)
    ax.grid(alpha=0.3)
    ax.set_xlim(-2, 102)
    ax.set_ylim(0, 42)

    # Panel 2: physics decomposition with KC, p_se
    ax = axes[1]
    rcp_list, pred_list, kc_list, p_list = [], [], [], []
    for am in am_arr:
        r = predict_real((am, 100-am), (7, 3))
        rcp_list.append(r['eps_rcp'] * 100)
        pred_list.append(r['eps_pred'] * 100)
        kc_list.append(r['kc'])
        p_list.append(r['p_se'])

    ax.plot(am_arr, rcp_list, '--', color='steelblue', lw=2,
            label='Bouvard RCP (geometric)')
    ax.plot(am_arr, pred_list, '-', color='crimson', lw=3,
            label='REAL prediction (RCP × SFM × Heckel × percolation)')
    ax.fill_between(am_arr, pred_list, rcp_list,
                     color='moccasin', alpha=0.5,
                     label='Plastic densification Δε (Heckel)')

    for (am, se), info in measured.items():
        ax.scatter(am, info['eps']*100, s=300, color='black',
                   marker='*', zorder=10,
                   edgecolors='gold', linewidth=2)
        ax.annotate(f'{am}:{se}\n{info["label"]}\nε={info["eps"]*100:.1f}%',
                     xy=(am, info['eps']*100),
                     xytext=(am-2.5, info['eps']*100+2),
                     fontsize=9, fontweight='bold')

    ax2 = ax.twinx()
    ax2.plot(am_arr, kc_list, ':', color='purple', lw=1.5, alpha=0.7,
              label='KC (SFM Sridhar 2000)')
    ax2.plot(am_arr, p_list, ':', color='darkorange', lw=1.5, alpha=0.7,
              label='p_se (geometric percolation 0.30)')
    ax2.set_ylabel('KC (purple) | p_se (orange)', fontsize=10, color='purple')
    ax2.tick_params(axis='y', colors='purple')
    ax2.set_ylim(0, max(max(kc_list), 1.3))
    ax2.legend(loc='lower right', fontsize=8.5)

    ax.set_xlabel('AM weight fraction (%)', fontsize=12)
    ax.set_ylabel('Porosity ε (%)', fontsize=12)
    ax.set_title('Real-physics decomposition (P:S=7:3)\n'
                  'Pure-SE endpoint from real Heckel (25 %, not 10 %)',
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
    print('REAL physics prediction (no calibration of mixture parameters)')
    print(f'{"AM:SE":>8s} {"P:S":>6s} {"f_se":>6s} {"λ_eff":>7s} '
          f'{"KC":>6s} {"p_se":>6s} {"ε_RCP":>7s} {"ε_pred":>7s} '
          f'{"meas":>7s} {"gap":>6s}')
    print('─' * 90)
    for am in [100, 95, 90, 85, 80, 75, 70, 60, 50, 30, 10, 0]:
        for p_s in p_s_configs if am < 100 and am > 0 else [(7, 3)]:
            r = predict_real((am, 100-am), p_s)
            meas, gap = '', ''
            if (am, 100-am) in measured and measured[(am, 100-am)]['p_s'] == p_s:
                m = measured[(am, 100-am)]['eps']
                meas = f'{m*100:.1f}'
                gap = f'{(r["eps_pred"]-m)*100:+.1f}'
            print(f'{f"{am}:{100-am}":>8s} {f"{p_s[0]}:{p_s[1]}":>6s} '
                  f'{r["f_se"]*100:5.1f}% {r["lam_eff"]:7.2f} '
                  f'{r["kc"]:6.2f} {r["p_se"]:6.3f} '
                  f'{r["eps_rcp"]*100:6.2f}% {r["eps_pred"]*100:6.2f}% '
                  f'{meas:>7s} {gap:>6s}')


if __name__ == '__main__':
    main()
