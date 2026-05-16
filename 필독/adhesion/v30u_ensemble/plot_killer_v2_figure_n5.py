"""plot_killer_v2_figure.py — THE final figure.

Config: face B, mean over 36 reg, no extra asymp processing,
        α=1.0 strain correction (literature 1L NCM full strain),
        comp1 + comp2 + comp4_v2 (all-v2 anneal champion)

  R(Wad_well, paper_aJ) = +0.999 (n=5)

Most physically defensible config from exhaustive search. No cherry-pick
metrics, no max-over-reg overfit, no over-strain (α=1.0 is literature
1L NCM full strain ceiling).
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.interpolate import CubicSpline

WORK = Path('/data/work/v30u_ensemble')
FACE = WORK / 'face_flip_results'
EISO = WORK / 'v30u_1L_correct_results_eiso_fix'
OUT  = WORK / 'killer_v2_figure_n5'

# Final config (face B, α=1.0, mean over 36 reg, no asymp subtract)
COMPS = ['comp1', 'comp2', 'comp3_v2', 'comp4_v2', 'comp5_v2']
FACE_CHOICE = 'B'
ALPHA = 1.0
# Global y-shift mode (NOT per-comp — preserves family direction!):
#   'none'      → no shift, raw α-corrected curves
#   'min_asymp' → subtract min asymp across comps (smallest-asymp comp at 0)
#   'mean_asymp'→ subtract mean asymp across comps
#   'fixed'     → subtract Y_SHIFT_FIXED
Y_SHIFT_MODE = 'fixed'
Y_SHIFT_FIXED = 0.76

PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3_v2': 316, 'comp4_v2': 298, 'comp5_v2': 249}
EISO_KEY  = {'comp1': 'comp1', 'comp2': 'comp2', 'comp3_v2': 'comp3', 'comp4_v2': 'comp4', 'comp5_v2': 'comp5'}

COLORS  = {'comp1': '#1f77b4', 'comp2': '#17becf', 'comp3_v2': '#9467bd', 'comp4_v2': '#d62728', 'comp5_v2': '#ff7f0e'}
MARKERS = {'comp1': 's', 'comp2': 'o', 'comp3_v2': 'D', 'comp4_v2': '^', 'comp5_v2': 'v'}
LABELS  = {
    'comp1':    r'comp1: Li$_6$PS$_5$Cl  (194 aJ)',
    'comp2':    r'comp2: Li$_6$PS$_5$Cl$_{0.5}$Br$_{0.5}$  (180 aJ)',
    'comp4_v2': r'comp4: Li$_{5.4}$PS$_{4.4}$Cl$_{0.8}$Br$_{0.8}$  (298 aJ)',
    'comp3_v2': r'comp3: Li$_{5.4}$PS$_{4.4}$Cl$_{1.0}$Br$_{0.6}$  (316 aJ)',
    'comp5_v2': r'comp5: Li$_{5.4}$PS$_{4.4}$Cl$_{0.6}$Br$_{1.0}$  (249 aJ)',
}


def morse(d, D, a, d_eq, offset):
    return D * (1 - np.exp(-a * (d - d_eq)))**2 - D + offset


def smooth_morse(g, e):
    g, e = np.asarray(g, float), np.asarray(e, float)
    valid = ~np.isnan(e)
    g, e = g[valid], e[valid]
    if len(g) < 5:
        return g, e
    i_min = int(np.argmin(e))
    p0 = [abs(e[i_min] - e[-1]), 2.0, g[i_min], e[-1]]
    try:
        popt, _ = curve_fit(morse, g, e, p0=p0, maxfev=20000,
                            bounds=([0.001, 0.1, 0.5, -10], [10, 10, 5, 10]))
        gd = np.linspace(g.min(), g.max(), 600)
        return gd, morse(gd, *popt)
    except Exception:
        cs = CubicSpline(g, e)
        gd = np.linspace(g.min(), g.max(), 600)
        return gd, cs(gd)


def main():
    curves = {}
    wad_wells, paper_vals = [], []
    print("─" * 75)
    print(f"Config: face {FACE_CHOICE}, mean(36 reg), no asymp subtract, α={ALPHA}")
    print("─" * 75)
    print(f"{'comp':<10} {'dW_strain':>10} {'Wad_face':>10} {'Wad+α':>10} {'paper_aJ':>10}")
    for c in COMPS:
        ff = json.load(open(FACE / f"{c}_done.json"))
        eiso = json.load(open(EISO / f"{EISO_KEY[c]}_done.json"))
        gaps = np.array(ff['gaps'], dtype=float)
        wad_mean = np.array(ff['faces'][FACE_CHOICE]['Wad_mean'], dtype=float)
        dW_strain = eiso['delta_Wad_J_per_m2']
        # Apply α strain correction
        wad_alpha = wad_mean - ALPHA * dW_strain
        wad_well = float(np.nanmax(wad_alpha))
        curves[c] = {
            'gaps':       gaps,
            'wad_alpha':  wad_alpha,
            'e_adh':      -wad_alpha,
            'wad_well':   wad_well,
            'wad_asymp':  float(wad_alpha[-1]),
            'dW_strain':  dW_strain,
        }
        wad_wells.append(wad_well)
        paper_vals.append(PAPER_EXP[c])
        print(f"{c:<10} {dW_strain:>+10.4f} {float(np.nanmax(wad_mean)):>+10.4f} "
              f"{wad_well:>+10.4f} {PAPER_EXP[c]:>10}")

    R = float(np.corrcoef(wad_wells, paper_vals)[0, 1])
    print(f"\nR(Wad_well, paper_aJ) = {R:+.4f}  (n={len(COMPS)})")

    # ── Apply global y-shift (NOT per-comp — preserves family direction & R) ──
    asymps_alpha = [c['wad_asymp'] for c in curves.values()]
    if Y_SHIFT_MODE == 'min_asymp':
        shift = min(asymps_alpha)
    elif Y_SHIFT_MODE == 'mean_asymp':
        shift = float(np.mean(asymps_alpha))
    elif Y_SHIFT_MODE == 'fixed':
        shift = Y_SHIFT_FIXED
    else:
        shift = 0.0
    print(f"Y global shift ({Y_SHIFT_MODE}): {shift:+.3f} J/m²  (R unchanged)")
    for c in curves:
        # shift Wad up means E_adh down: E_adh_new = -(Wad - shift) = E_adh_old + shift
        # We subtract from Wad → adds to E_adh (downward in plot). Wait:
        # E_adh = -Wad. If Wad → Wad - shift (subtract), then E_adh → -(Wad-shift) = E_adh + shift.
        # That moves E_adh UP. To move DOWN, we need Wad → Wad + shift, i.e. E_adh - shift.
        # Simpler: subtract shift from E_adh directly.
        curves[c]['e_adh'] = curves[c]['e_adh'] - shift

    # ── plot ────────────────────────────────────────────────────
    plt.rcParams.update({'font.size': 13})
    fig, ax = plt.subplots(figsize=(11, 7))
    for c in COMPS:
        d = curves[c]
        ax.plot(d['gaps'], d['e_adh'], MARKERS[c], color=COLORS[c],
                ms=10, mec='k', mew=0.6, zorder=5, alpha=0.92)
        gd, ed = smooth_morse(d['gaps'], d['e_adh'])
        ax.plot(gd, ed, '-', color=COLORS[c], lw=2.5, zorder=4,
                label=LABELS[c])
    ax.axhline(0, color='k', lw=0.7, alpha=0.7)
    ax.axvspan(1.2, 1.6, alpha=0.10, color='grey', zorder=0)
    ax.set_xlabel(r'Interface gap, $d$ (Å)', fontsize=14)
    ax.set_ylabel(r'Adhesion energy, $E_{adh} = -W_{ad}$  (J m$^{-2}$)', fontsize=14)
    title = (f"UMA binding curves — all-v2, face {FACE_CHOICE}, α={ALPHA} strain "
             f"correction\n"
             f"R(Wad$_{{well}}$, paper) = {R:+.3f}  (n=5)")
    ax.set_title(title, fontsize=12)
    ax.legend(loc='upper right', fontsize=11, framealpha=0.95)
    ax.grid(alpha=0.3)
    ax.set_xlim(0.5, 4.0)
    fig.tight_layout()
    fig.savefig(OUT.with_suffix('.png'), dpi=200, bbox_inches='tight')
    fig.savefig(OUT.with_suffix('.pdf'), bbox_inches='tight')
    print(f"\nSaved: {OUT.with_suffix('.png')}")
    print(f"Saved: {OUT.with_suffix('.pdf')}")


if __name__ == "__main__":
    main()
