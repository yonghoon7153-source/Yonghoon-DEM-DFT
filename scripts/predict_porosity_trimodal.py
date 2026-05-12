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
    """Asymmetric Bouvard 2004 Fig 2 parabolic fit.

    eps_min depends on size ratio:
      λ = 4  →  eps_min ≈ 0.22
      λ = 8  →  eps_min ≈ 0.18
      λ = 12 →  eps_min ≈ 0.16
      λ→∞   →  eps_min →  0.15 (McGeary asymptote)
    """
    fl = 1.0 - f_se
    fl_opt = 0.74
    # Interpolate eps_min with size ratio (Bouvard data)
    eps_min = max(0.15, 0.36 - 0.04 * np.log(lambda_ratio))
    eps_max = 0.36

    if fl <= fl_opt:
        delta = (fl - fl_opt) / fl_opt
    else:
        delta = (fl - fl_opt) / (1.0 - fl_opt)
    eps = eps_min + (eps_max - eps_min) * delta * delta
    return min(eps, eps_max)


# ── SFM plastic contribution (linear in plastic-phase fraction) ──
def plastic_delta(f_se, P=P_PRESS, sigma_y=SIGMA_Y_SE,
                   eps_pure_se_target=0.10, eps_rcp_pure=0.36):
    """Linear SFM approximation. Pure SE compaction at P/σ_y ≈ 1.06
    achieves Δε = 0.26 (36 → 10 %). For mixtures, scaled by f_SE.
    """
    delta_max = eps_rcp_pure - eps_pure_se_target  # 0.26
    p_norm = (P / sigma_y) / (300e6 / 283e6)
    return delta_max * f_se * min(p_norm, 1.5)


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

    am_se_sweep = [(95, 5), (90, 10), (85, 15), (80, 20), (75, 25), (70, 30),
                    (60, 40), (50, 50), (30, 70), (10, 90), (0, 100)]
    p_s_configs = [(3, 7), (5, 5), (7, 3)]

    colors = {(3, 7): 'tab:blue', (5, 5): 'tab:green', (7, 3): 'tab:red'}

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # ── Panel 1: porosity curves for different P:S ──
    ax = axes[0]
    for p_s in p_s_configs:
        f_se_list, eps_rcp_list, eps_pred_list = [], [], []
        for am_se in am_se_sweep:
            f_se, lam, eps_rcp, eps_pred = predict_porosity(am_se, p_s)
            f_se_list.append(f_se * 100)
            eps_rcp_list.append(eps_rcp * 100)
            eps_pred_list.append(eps_pred * 100)

        ax.plot(f_se_list, eps_rcp_list, '--', color=colors[p_s], alpha=0.5,
                label=f'P:S={p_s[0]}:{p_s[1]} (Furnas RCP)')
        ax.plot(f_se_list, eps_pred_list, '-', color=colors[p_s], lw=2.5,
                label=f'P:S={p_s[0]}:{p_s[1]} (with plastic)')

    # Measured points
    for (am, se), info in measured.items():
        f_se, lam, eps_rcp, eps_pred = predict_porosity((am, se), info['p_s'])
        ax.scatter(f_se * 100, info['eps'] * 100, s=250, color='black',
                    marker='*', zorder=10,
                    label='Measured (DEM)' if (am, se) == (85, 15) else None)
        ax.annotate(f'{am}:{se}\n(λ_eff={lam:.1f})',
                     xy=(f_se*100, info['eps']*100),
                     xytext=(f_se*100 + 2, info['eps']*100 - 2),
                     fontsize=9, fontweight='bold')

    ax.set_xlabel('SE volume fraction (%)', fontsize=12)
    ax.set_ylabel('Porosity ε (%)', fontsize=12)
    ax.set_title('Trimodal D12/D4/D1 porosity prediction\n'
                  'AM_P:AM_S:SE = 12:4:1 µm, ρ_AM=4.8, ρ_SE=2', fontsize=11)
    ax.axvline(26, color='gray', linestyle=':', alpha=0.4)
    ax.text(26, 38, 'Furnas\nopt', ha='center', fontsize=8, color='gray')
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8, loc='upper right')
    ax.set_xlim(-3, 105)
    ax.set_ylim(0, 42)

    # ── Panel 2: same data, focus on measured range ──
    ax = axes[1]
    for p_s in p_s_configs:
        f_se_list, eps_rcp_list, eps_pred_list, lam_list = [], [], [], []
        # Dense sweep for smooth curves
        for am in np.linspace(60, 95, 50):
            am_se = (am, 100 - am)
            f_se, lam, eps_rcp, eps_pred = predict_porosity(am_se, p_s)
            f_se_list.append(f_se * 100)
            eps_rcp_list.append(eps_rcp * 100)
            eps_pred_list.append(eps_pred * 100)
            lam_list.append(lam)

        ax.plot(f_se_list, eps_rcp_list, '--', color=colors[p_s], alpha=0.6,
                label=f'P:S={p_s[0]}:{p_s[1]} (RCP λ_eff={lam_list[len(lam_list)//2]:.1f})')
        ax.plot(f_se_list, eps_pred_list, '-', color=colors[p_s], lw=2.5)

    # Measured points
    for (am, se), info in measured.items():
        f_se, lam, eps_rcp, eps_pred = predict_porosity((am, se), info['p_s'])
        ax.scatter(f_se * 100, info['eps'] * 100, s=250, color='black',
                    marker='*', zorder=10)
        ax.annotate(f'{am}:{se}\n{info["label"]}\nε={info["eps"]*100:.1f}%',
                     xy=(f_se*100, info['eps']*100),
                     xytext=(f_se*100 + 2, info['eps']*100 - 4),
                     fontsize=9)

    ax.set_xlabel('SE volume fraction (%)', fontsize=12)
    ax.set_ylabel('Porosity ε (%)', fontsize=12)
    ax.set_title('Zoom: measured range (AM:SE 75:25 — 95:5)\n'
                  'P:S effect via effective size ratio λ_eff', fontsize=11)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=9, loc='upper right')
    ax.set_xlim(15, 50)
    ax.set_ylim(0, 30)

    plt.tight_layout()
    out = Path('trimodal_porosity_curve.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    print(f'✓ Saved: {out.resolve()}')

    # ── Print numerical table ──
    print()
    print(f'{"AM:SE":>8s} {"P:S":>6s} {"f_AM_P":>8s} {"f_AM_S":>8s} '
          f'{"f_SE":>8s} {"λ_eff":>7s} {"ε_RCP":>8s} {"ε_pred":>8s} {"meas":>8s}')
    print('─' * 90)
    for am_se in [(95, 5), (90, 10), (85, 15), (80, 20), (75, 25), (70, 30)]:
        for p_s in p_s_configs:
            f_am_p, f_am_s, f_se = wt_to_vol(am_se, p_s)
            lam = effective_size_ratio(f_am_p, f_am_s, f_se)
            eps_rcp = bouvard_porosity(f_se, lam)
            eps_pred = max(eps_rcp - plastic_delta(f_se), 0.05)
            meas = ''
            if am_se in measured and measured[am_se]['p_s'] == p_s:
                meas = f'{measured[am_se]["eps"]*100:.1f}'
            print(f'{f"{am_se[0]}:{am_se[1]}":>8s} '
                  f'{f"{p_s[0]}:{p_s[1]}":>6s} '
                  f'{f_am_p*100:7.2f}% {f_am_s*100:7.2f}% '
                  f'{f_se*100:7.2f}% {lam:7.2f} '
                  f'{eps_rcp*100:7.2f}% {eps_pred*100:7.2f}% {meas:>8s}')


if __name__ == '__main__':
    main()
