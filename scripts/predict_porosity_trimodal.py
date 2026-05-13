#!/usr/bin/env python3
"""Trimodal porosity predictor for AM_P (D12) / AM_S (D4) / SE (D1).

Material parameters (user-provided):
  AM_P: D=12 µm, elastic, ρ_real = 4.8 g/cm³
  AM_S: D=4  µm, elastic, ρ_real = 4.8 g/cm³
  SE:   D=1  µm, plastic, ρ_real = 2.0 g/cm³

Composition sweep:
  AM:SE wt%   = 75:25, 80:20, 85:15, 90:10, 95:5
  P:S ratio   = 3:7, 5:5, 7:3   (within AM, by volume)

Output:
  ε vs SE-volume-fraction for each P:S configuration
  (compares Furnas-Westman geometric + SFM plastic)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path


# ── Material parameters ─────────────────────────────────────────
D_AM_P  = 12.0           # µm
D_AM_S  = 4.0            # µm
D_SE    = 1.0            # µm
RHO_AM  = 4.8            # g/cm³
RHO_SE  = 2.0            # g/cm³

E_AM    = 140e9          # Pa (elastic)
E_SE    = 24e9           # Pa
H_SE    = 0.85e9         # Pa  (hardness)
SIGMA_Y_SE = H_SE / 3.0  # Tabor → 283 MPa

P_PRESS = 300e6          # Pa


# ── Wt% → vol% conversion (trimodal) ────────────────────────────
def wt_to_vol(am_se_wt_ratio, p_s_vol_ratio):
    """Convert (AM:SE) wt% + (P:S) vol ratio to (f_AM_P, f_AM_S, f_SE).

    Note: P:S is _within AM_, by VOLUME (per user spec — both AM
    types share the same density ρ_AM, so P:S vol == P:S wt within AM).
    """
    am_wt, se_wt = am_se_wt_ratio  # e.g., (85, 15)
    p_vol, s_vol = p_s_vol_ratio   # e.g., (7, 3)

    # Volumes per unit total mass (e.g., per 100 g)
    v_am_total = am_wt / RHO_AM
    v_se = se_wt / RHO_SE

    # Split AM into P and S by their volume ratio
    p_frac = p_vol / (p_vol + s_vol)
    v_am_p = v_am_total * p_frac
    v_am_s = v_am_total * (1 - p_frac)

    v_total = v_am_p + v_am_s + v_se
    return v_am_p/v_total, v_am_s/v_total, v_se/v_total


# ── Effective size ratio (volume-weighted AM diameter / SE diameter) ─
def effective_size_ratio(f_am_p, f_am_s, f_se):
    """Volume-weighted effective AM diameter / SE diameter."""
    f_am = f_am_p + f_am_s
    if f_am <= 0:
        return 1.0
    d_eff_am = (f_am_p * D_AM_P + f_am_s * D_AM_S) / f_am
    return d_eff_am / D_SE


# ── Furnas-Westman binary Bouvard 2004 fit ──────────────────────
def bouvard_porosity(f_se, lambda_ratio):
    """Bouvard 2004 Fig 2 — interpolated from digitized data points.

    For size ratio λ = 8, the porosity ε vs f_large data approximately
    follows (digitized from Bouvard Fig 2):
      f_large = 0.00 → ε = 0.36
      f_large = 0.20 → ε = 0.30
      f_large = 0.40 → ε = 0.24
      f_large = 0.60 → ε = 0.20
      f_large = 0.74 → ε = 0.18   (optimum)
      f_large = 0.80 → ε = 0.19
      f_large = 0.90 → ε = 0.25
      f_large = 1.00 → ε = 0.36
    For larger λ, the minimum porosity decreases (McGeary λ=11.3 gives
    ε_min ≈ 0.15). We scale eps_min and use the same shape.
    """
    fl = 1.0 - f_se

    # Reference curve at λ = 8 (Bouvard Fig 2 data)
    fl_ref  = np.array([0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60,
                        0.70, 0.74, 0.78, 0.85, 0.90, 0.95, 1.00])
    eps_ref = np.array([0.36, 0.33, 0.30, 0.27, 0.24, 0.22, 0.20,
                        0.185, 0.18, 0.185, 0.215, 0.25, 0.30, 0.36])

    eps_lambda8 = np.interp(fl, fl_ref, eps_ref)

    # Scale eps_min with size ratio (Bouvard λ=4 → eps_min≈0.22, λ=8 → 0.18, λ=12 → 0.16)
    eps_min_scale = 0.18 + (8 - lambda_ratio) * 0.005   # rough fit
    eps_min_scale = max(0.14, min(0.22, eps_min_scale))
    # Affine adjust: shift the curve toward its new minimum
    eps_min_ref = 0.18
    eps_max_ref = 0.36
    eps_adjusted = eps_min_scale + (eps_lambda8 - eps_min_ref) / \
                   (eps_max_ref - eps_min_ref) * (eps_max_ref - eps_min_scale)
    return min(float(eps_adjusted), 0.36)


# ── SFM plastic contribution with FORCE-CHAIN SHADOW correction ──
SHADOW_EXPONENT = 2.0   # f_AM^β  (β=2: percolation-aware; β=1: linear)

def plastic_delta(f_se, P=P_PRESS, sigma_y=SIGMA_Y_SE,
                   eps_pure_se_target=0.10, eps_rcp_pure=0.36,
                   shadow_beta=SHADOW_EXPONENT):
    """Heterogeneity-corrected SFM plastic densification.

    Naive SFM (linear in f_SE) assumes mean-field plastic flow, which
    overpredicts plastic contribution in mixtures because AM force
    chains shadow a portion of SE particles from compaction stress.

    Physical model — force-chain percolation shadow:
        α_effective(f_AM) = α_pure × (1 − f_AM^β)

    where β controls how rapidly the shadow grows with rigid fraction:
      β = 1: linear (mean-field-like)
      β = 2: quadratic — force chains require AM-AM percolation
             (force chain density ∝ AM coordination number)²
      β > 2: even sharper percolation threshold

    For typical granular mixtures with size ratio ~10, β ≈ 2 reflects
    the experimentally observed sand-rubber stress-shadow effect
    (Liu & Yin 2025) and our DEM force-chain quantification.

    Calibration: at pure SE (f_AM=0), shadow=0 → α_eff = α_pure,
    recovering the 0.26 endpoint reduction (36 % → 10 %).
    """
    f_am = 1.0 - f_se
    alpha_pure = eps_rcp_pure - eps_pure_se_target  # 0.26 at pure SE
    shadow = f_am ** shadow_beta
    alpha_eff = alpha_pure * (1.0 - shadow)
    p_norm = (P / sigma_y) / (300e6 / 283e6)
    return alpha_eff * f_se * min(p_norm, 1.5)


# ── Effective porosity prediction ───────────────────────────────
def predict_porosity(am_se_wt, p_s_vol):
    """Return (f_se_vol, eps_rcp, eps_plastic_corrected)."""
    f_am_p, f_am_s, f_se = wt_to_vol(am_se_wt, p_s_vol)
    lam = effective_size_ratio(f_am_p, f_am_s, f_se)
    eps_rcp = bouvard_porosity(f_se, lam)
    delta = plastic_delta(f_se)
    eps_pred = max(eps_rcp - delta, 0.05)
    return f_se, lam, eps_rcp, eps_pred


# ── Main: sweep + plot ──────────────────────────────────────────
def main():
    # Measured data (input_8mAh_3, _6, _9) — all P:S = 7:3
    measured = {
        (85, 15): {'p_s': (7, 3), 'eps': 0.157, 'label': 'input_8mAh_9'},
        (80, 20): {'p_s': (7, 3), 'eps': 0.165, 'label': 'input_8mAh_6'},
        (75, 25): {'p_s': (7, 3), 'eps': 0.185, 'label': 'input_8mAh_3'},
    }

    # AM:SE sweep (X-axis): use AM wt% as the axis
    am_wt_arr = np.linspace(50, 100, 51)  # AM wt% from 50% to 100%
    p_s_configs = [(3, 7), (5, 5), (7, 3)]

    colors = {(3, 7): 'tab:blue', (5, 5): 'tab:green', (7, 3): 'tab:red'}
    markers = {(3, 7): 's', (5, 5): 'o', (7, 3): '^'}

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # ── Panel 1: full AM:SE sweep, X = AM wt% ──
    ax = axes[0]
    for p_s in p_s_configs:
        eps_rcp_list, eps_pred_list, lam_list = [], [], []
        for am_wt in am_wt_arr:
            am_se = (am_wt, 100 - am_wt)
            f_se, lam, eps_rcp, eps_pred = predict_porosity(am_se, p_s)
            eps_rcp_list.append(eps_rcp * 100)
            eps_pred_list.append(eps_pred * 100)
            lam_list.append(lam)

        ax.plot(am_wt_arr, eps_rcp_list, '--', color=colors[p_s], alpha=0.45,
                lw=1.5,
                label=f'P:S={p_s[0]}:{p_s[1]} — Furnas RCP (geometric)')
        ax.plot(am_wt_arr, eps_pred_list, '-', color=colors[p_s], lw=2.5,
                label=f'P:S={p_s[0]}:{p_s[1]} — with SFM plastic')

    # Measured points (P:S = 7:3)
    for (am, se), info in measured.items():
        f_se, lam, eps_rcp, eps_pred = predict_porosity((am, se), info['p_s'])
        ax.scatter(am, info['eps'] * 100, s=280, color='black', marker='*',
                    zorder=10, edgecolors='gold', linewidth=1.5,
                    label='Measured (DEM, P:S=7:3)' if (am, se) == (85, 15) else None)
        ax.annotate(f'{am}:{se}\nε={info["eps"]*100:.1f}%',
                     xy=(am, info['eps']*100),
                     xytext=(am-3.5, info['eps']*100+1.5), fontsize=9,
                     fontweight='bold',
                     arrowprops=dict(arrowstyle='-', color='gray', alpha=0.5))

    ax.set_xlabel('AM weight fraction (%)', fontsize=12)
    ax.set_ylabel('Porosity ε (%)', fontsize=12)
    ax.set_title('Trimodal D12/D4/D1 prediction\n'
                  '(ρ_AM=4.8, ρ_SE=2.0, H_SE=0.85 GPa, P=300 MPa)',
                  fontsize=11)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8.5, loc='upper left', framealpha=0.95)
    ax.set_xlim(48, 102)
    ax.set_ylim(0, 42)
    # Add SE wt% as a secondary x-axis on top
    ax2 = ax.twiny()
    ax2.set_xlim(ax.get_xlim())
    ax2.set_xticks([50, 60, 70, 80, 90, 100])
    ax2.set_xticklabels(['50', '40', '30', '20', '10', '0'])
    ax2.set_xlabel('SE weight fraction (%)', fontsize=11, color='gray')

    # ── Panel 2: zoom to measured range, also show effective λ ──
    ax = axes[1]
    am_wt_zoom = np.linspace(65, 95, 100)
    for p_s in p_s_configs:
        eps_pred_list, lam_list = [], []
        for am_wt in am_wt_zoom:
            am_se = (am_wt, 100 - am_wt)
            f_se, lam, eps_rcp, eps_pred = predict_porosity(am_se, p_s)
            eps_pred_list.append(eps_pred * 100)
            lam_list.append(lam)
        ax.plot(am_wt_zoom, eps_pred_list, '-', color=colors[p_s], lw=2.5,
                marker=markers[p_s], markevery=12, markersize=8,
                label=f'P:S={p_s[0]}:{p_s[1]} (λ_eff={lam_list[50]:.1f})')

    # Measured
    for (am, se), info in measured.items():
        ax.scatter(am, info['eps'] * 100, s=300, color='black', marker='*',
                    zorder=10, edgecolors='gold', linewidth=2)
        ax.annotate(f'{am}:{se}\n{info["label"]}\nε={info["eps"]*100:.1f}%',
                     xy=(am, info['eps']*100),
                     xytext=(am-2, info['eps']*100+2.5), fontsize=10)

    ax.set_xlabel('AM weight fraction (%)', fontsize=12)
    ax.set_ylabel('Porosity ε (%)', fontsize=12)
    ax.set_title('Zoom: measured range (AM:SE = 75:25 to 95:5)\n'
                  'Effect of P:S on porosity at fixed AM:SE',
                  fontsize=11)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=10, loc='upper left', framealpha=0.95)
    ax.set_xlim(65, 96)
    ax.set_ylim(2, 22)

    plt.tight_layout()
    out = Path('trimodal_porosity_curve.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    print(f'✓ Saved: {out.resolve()}')

    # ── Print numerical table ──
    print()
    print(f'{"AM:SE":>8s} {"P:S":>6s} {"f_AM_P":>8s} {"f_AM_S":>8s} '
          f'{"f_SE":>8s} {"λ_eff":>7s} {"ε_RCP":>8s} {"ε_pred":>8s} {"meas":>8s}')
    print('─' * 90)
    for am in [95, 90, 85, 80, 75, 70]:
        for p_s in p_s_configs:
            am_se = (am, 100 - am)
            f_am_p, f_am_s, f_se = wt_to_vol(am_se, p_s)
            lam = effective_size_ratio(f_am_p, f_am_s, f_se)
            eps_rcp = bouvard_porosity(f_se, lam)
            eps_pred = max(eps_rcp - plastic_delta(f_se), 0.05)
            meas = ''
            if am_se in measured and measured[am_se]['p_s'] == p_s:
                meas = f'{measured[am_se]["eps"]*100:.1f}'
            print(f'{f"{am}:{100-am}":>8s} '
                  f'{f"{p_s[0]}:{p_s[1]}":>6s} '
                  f'{f_am_p*100:7.2f}% {f_am_s*100:7.2f}% '
                  f'{f_se*100:7.2f}% {lam:7.2f} '
                  f'{eps_rcp*100:7.2f}% {eps_pred*100:7.2f}% {meas:>8s}')


if __name__ == '__main__':
    main()
