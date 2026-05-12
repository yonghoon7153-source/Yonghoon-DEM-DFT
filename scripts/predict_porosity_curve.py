#!/usr/bin/env python3
"""Predict ε vs SE fraction curve by combining Furnas-Westman (geometric)
and Storakers-Fleck-McMeeking (plastic) for our DEM ASSB cathodes.

Reference: Bouvard 2004 Int. J. Mech. Sci. 46:907 (geometric RCP)
           Sridhar & Fleck 2000 Acta Mater. 48:3341 (SFM composite)
           Storakers, Fleck, McMeeking 1999 J. Mech. Phys. Solids 47:785

Material parameters (per user input):
  E_NCM (AM):  140 GPa
  E_SE:        24 GPa
  H_SE:        0.85 GPa  →  Tabor σ_y_SE = H/3 ≈ 283 MPa
  Size ratio:  D_AM/D_SE ≈ 10  (D10/D1)
  P_press:     300 MPa  (cold-press nominal)
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ── Material parameters ─────────────────────────────────────────
E_AM        = 140.0e9       # Pa
E_SE        = 24.0e9        # Pa
H_SE        = 0.85e9        # Pa (hardness)
SIGMA_Y_SE  = H_SE / 3.0    # Pa (Tabor: H ≈ 3 σ_y)  → 283 MPa
P_PRESS     = 300.0e6       # Pa
SIZE_RATIO  = 10.0          # D_AM / D_SE


# ── Furnas-Westman geometric RCP (Bouvard 2004 fit) ─────────────
def furnas_porosity(f_se, lambda_ratio=10):
    """Initial RCP porosity for binary rigid mixture.

    Based on Bouvard 2004 Fig 2: maximum density at f_l ≈ 74 % large
    particles, monomodal RCP = 36 % at both extremes (f_l = 0 and f_l = 1).
    We use an asymmetric parabolic interpolation that hits 36 % at both
    ends and ~17 % at the optimum.
    """
    f_large = 1.0 - f_se
    fl_opt = 0.74
    eps_min = 0.17 if lambda_ratio >= 8 else 0.20
    eps_max = 0.36
    # Asymmetric scaling: distance to nearest extreme normalized separately
    # so that delta = ±1 at the extremes (f_large = 0 or 1) and 0 at optimum
    if f_large <= fl_opt:
        delta = (f_large - fl_opt) / fl_opt
    else:
        delta = (f_large - fl_opt) / (1.0 - fl_opt)
    eps = eps_min + (eps_max - eps_min) * delta * delta
    return min(eps, eps_max)


# ── SFM plastic contribution ────────────────────────────────────
def plastic_contribution(f_se, P=P_PRESS, sigma_y=SIGMA_Y_SE,
                          eps_rcp_pure=0.36, eps_pure_se_target=0.10):
    """Linear approximation of Storakers-Fleck-McMeeking plastic densification.

    At pure SE (f_se=1), the cold-press achieves the calibrated 10 %
    porosity (reducing 36 % → 10 % = 26 % absolute reduction). For
    composites, this densification scales linearly with SE volume
    fraction in the first-order SFM-affine approximation.
    """
    delta_max = eps_rcp_pure - eps_pure_se_target  # 0.26
    # Scale with P/σ_y if these parameters change
    p_norm = (P / sigma_y) / (300e6 / 283e6)  # = 1.0 at reference
    return delta_max * f_se * min(p_norm, 1.5)


# ── Main calculation ────────────────────────────────────────────
def main():
    f_se = np.linspace(0.0, 1.0, 101)
    eps_rcp = np.array([furnas_porosity(f, SIZE_RATIO) for f in f_se])
    delta_p = np.array([plastic_contribution(f) for f in f_se])
    eps_pred = np.maximum(eps_rcp - delta_p, 0.05)

    # Measured DEM data (from user)
    f_se_meas = np.array([0.30, 0.38, 0.45])
    eps_meas = np.array([0.157, 0.165, 0.185])
    case_labels = ['85:15\n(input_8mAh_9)', '80:20\n(input_8mAh_6)',
                   '75:25\n(input_8mAh_3)']

    # Calibrated endpoints
    endpoints_x = [0.0, 1.0]
    endpoints_y = [0.36, 0.10]

    # ── Plot ────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(11, 7))

    ax.plot(f_se * 100, eps_rcp * 100, '--', color='steelblue', lw=2.5,
            label='Furnas RCP only (geometric, Bouvard 2004)')
    ax.plot(f_se * 100, eps_pred * 100, '-', color='crimson', lw=3,
            label='Predicted (Furnas + SFM plastic, σ_y=283 MPa)')

    # Plastic contribution as shaded area
    ax.fill_between(f_se * 100, eps_rcp * 100, eps_pred * 100,
                     color='moccasin', alpha=0.4,
                     label='Plastic densification (SFM)')

    # Measured DEM
    ax.scatter(f_se_meas * 100, eps_meas * 100, s=200, color='black',
                marker='*', zorder=5,
                label='Measured (our DEM, 165 cases)')
    for x, y, lbl in zip(f_se_meas, eps_meas, case_labels):
        ax.annotate(lbl, xy=(x*100, y*100), xytext=(x*100+3, y*100+1.5),
                     fontsize=9, ha='left')

    # Calibrated endpoints
    ax.scatter(endpoints_x, [e*100 for e in endpoints_y], s=180,
                marker='s', color='darkgreen', zorder=5,
                label='Calibrated endpoints (E_SE tuned)')
    ax.annotate('Pure AM\n(rigid, RCP)', xy=(0, 36),
                 xytext=(5, 37), fontsize=9, color='darkgreen')
    ax.annotate('Pure SE\n(plastic, cold-press)', xy=(100, 10),
                 xytext=(80, 4), fontsize=9, color='darkgreen')

    # Annotations
    ax.axvline(26, color='gray', linestyle=':', alpha=0.6, lw=1)
    ax.text(26, 38.5, 'Furnas\noptimum', ha='center', fontsize=10,
             color='gray', style='italic')

    # Gap arrows
    for x, y_meas in zip(f_se_meas, eps_meas):
        idx = int(x * 100)
        y_pred = eps_pred[idx]
        ax.annotate('', xy=(x*100, y_meas*100), xytext=(x*100, y_pred*100),
                     arrowprops=dict(arrowstyle='<->', color='purple', lw=1.5))
    ax.text(50, 13.5, 'Δ = force chain\nshadow effect', fontsize=10,
             color='purple', style='italic', ha='center')

    ax.set_xlabel('SE volume fraction (%)', fontsize=13)
    ax.set_ylabel('Porosity ε (%)', fontsize=13)
    ax.set_title(f'Predicted porosity curve\n'
                  f'E_AM={E_AM/1e9:.0f} GPa, E_SE={E_SE/1e9:.0f} GPa, '
                  f'H_SE={H_SE/1e9:.2f} GPa → σ_y=283 MPa (Tabor), '
                  f'P={P_PRESS/1e6:.0f} MPa, λ={SIZE_RATIO:.0f}',
                  fontsize=11)
    ax.legend(fontsize=10, loc='upper right', framealpha=0.95)
    ax.grid(alpha=0.3)
    ax.set_xlim(-3, 105)
    ax.set_ylim(0, 42)

    plt.tight_layout()
    out = Path('predicted_porosity_curve.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    print(f'✓ Saved: {out.resolve()}')

    # Print numerical comparison
    print(f'\n{"f_SE (%)":>10s} {"ε_RCP (%)":>10s} {"Δε_plastic":>12s} '
          f'{"ε_pred (%)":>11s}')
    print('─' * 50)
    for fs in [0, 0.10, 0.20, 0.26, 0.30, 0.38, 0.45, 0.50, 0.70, 1.0]:
        idx = int(fs * 100)
        print(f'{fs*100:10.1f} {eps_rcp[idx]*100:10.2f} '
              f'{delta_p[idx]*100:12.2f} {eps_pred[idx]*100:11.2f}')

    print(f'\nParameters: σ_y_SE (Tabor) = {SIGMA_Y_SE/1e6:.1f} MPa, '
          f'P/σ_y = {P_PRESS/SIGMA_Y_SE:.2f}')


if __name__ == '__main__':
    main()
