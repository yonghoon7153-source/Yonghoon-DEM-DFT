#!/usr/bin/env python
"""
THE final figure with TIGHT MORSE FIT — R=+0.9888, rho=+1.0000.

Multi-start global optimization for each binding curve. Reports per-comp
fit RMSE and outputs dense (600-point) CSV of fitted curves.

Outputs:
  killer_v2_figure_R0988_TIGHT.png
  killer_v2_figure_R0988_TIGHT.pdf
  killer_v2_figure_R0988_TIGHT_dense.csv     (600-point Morse curves)
  killer_v2_figure_R0988_TIGHT_data.csv      (16 raw data points)
  killer_v2_figure_R0988_TIGHT_fit_params.csv (Morse parameters per comp)

Run anywhere:
  python3 plot_R0988_TIGHT_FIT.py
"""
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit, differential_evolution
from scipy.stats import spearmanr

# ── Data (E_adh, identical to standalone script) ──────────────────────
GAP = np.array([0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.5, 2.8, 3.0, 3.5, 4.0, 5.0, 7.0])

E = {
    'comp1':    np.array([10.051626718, 2.338847112, -0.355997310, -0.835399377, -0.481271372,
                          0.113328109, 0.700706531, 1.192675296, 1.552903315, 1.865112734,
                          2.032106948, 2.104469976, 2.200599072, 2.241651505, 2.296908398, 2.299680218]),
    'comp2':    np.array([6.581441348, 1.151681305, -0.563040840, -0.696082393, -0.258767783,
                          0.318141483, 0.851300085, 1.272484390, 1.561331833, 1.807491585,
                          1.950161316, 2.009957649, 2.085695499, 2.117914454, 2.150181251, 2.154495055]),
    'comp3_v2': np.array([9.114794261, 2.489477230, -0.623653673, -1.709084988, -1.933346420,
                          -1.814649249, -1.591695432, -1.397127866, -1.262662015, -1.078891537,
                          -0.950454908, -0.893642024, -0.790796558, -0.699070367, -0.466459646, -0.277229324]),
    'comp4_v2': np.array([10.857377160, 2.855317495, -0.403541060, -1.440978694, -1.629803822,
                          -1.503944688, -1.289345167, -1.114682112, -0.992010956, -0.829145053,
                          -0.722228567, -0.675174228, -0.581152987, -0.492434715, -0.270200047, -0.115563511]),
    'comp5_v2': np.array([5.119999966, 0.403840842, -1.157819723, -1.418882408, -1.275231579,
                          -1.016717738, -0.797384874, -0.648697707, -0.549360752, -0.453108742,
                          -0.404006507, -0.385237557, -0.354356993, -0.329261136, -0.313085036, -0.331754886]),
}

PAPER  = {'comp1': 194, 'comp2': 180, 'comp3_v2': 316, 'comp4_v2': 298, 'comp5_v2': 249}
COLORS = {'comp1': '#1f77b4', 'comp2': '#17becf',
          'comp3_v2': '#d62728', 'comp4_v2': '#9467bd', 'comp5_v2': '#2ca02c'}
MARKERS = {'comp1': 's', 'comp2': 'o', 'comp3_v2': '^', 'comp4_v2': 'D', 'comp5_v2': 'v'}
LABELS = {
    'comp1':    r'comp1: Li$_6$PS$_5$Cl  (194 aJ)',
    'comp2':    r'comp2: Li$_6$PS$_5$Cl$_{0.5}$Br$_{0.5}$  (180 aJ)',
    'comp3_v2': r'comp3: Li$_{5.4}$PS$_{4.4}$Cl$_{1.0}$Br$_{0.6}$  (316 aJ)',
    'comp4_v2': r'comp4: Li$_{5.4}$PS$_{4.4}$Cl$_{0.8}$Br$_{0.8}$  (298 aJ)',
    'comp5_v2': r'comp5: Li$_{5.4}$PS$_{4.4}$Cl$_{0.6}$Br$_{1.0}$  (249 aJ)',
}


# ── Morse function ──
def morse(d, D, a, d_eq, off):
    return D * (1 - np.exp(-a * (d - d_eq)))**2 - D + off


def fit_residuals(params, g, e):
    D, a, d_eq, off = params
    pred = morse(g, D, a, d_eq, off)
    # Weight: give 2x weight to points within 1 Å of well, normal elsewhere
    i_min = int(np.argmin(e))
    g_well = g[i_min]
    w = np.where(np.abs(g - g_well) < 1.0, 2.0, 1.0)
    return float(np.sum(w * (pred - e)**2))


def tight_fit(g, e, label=''):
    """Multi-start Morse fit with global optimization fallback."""
    g, e = np.asarray(g, float), np.asarray(e, float)
    m = ~np.isnan(e)
    g, e = g[m], e[m]
    i_min = int(np.argmin(e))
    g_min = g[i_min]
    e_min = e[i_min]
    e_asymp = e[-1]

    # Multi-start initial guesses
    starts = [
        [abs(e_min - e_asymp), 2.0, g_min, e_asymp],
        [abs(e_min - e_asymp), 1.5, g_min, e_asymp],
        [abs(e_min - e_asymp), 3.0, g_min, e_asymp],
        [abs(e_min - e_asymp) * 1.5, 2.0, g_min - 0.1, e_asymp],
        [abs(e_min - e_asymp) * 0.8, 2.5, g_min + 0.1, e_asymp],
        [3.0, 2.0, 1.4, 0.0],
        [1.0, 2.5, 1.3, e_asymp],
    ]
    best_popt, best_rmse = None, np.inf
    bounds_lo = [0.001, 0.1, 0.5, -10]
    bounds_hi = [50.0, 10.0, 5.0, 10.0]

    # Try curve_fit with each start
    for p0 in starts:
        try:
            popt, _ = curve_fit(morse, g, e, p0=p0, maxfev=50000,
                                bounds=(bounds_lo, bounds_hi))
            pred = morse(g, *popt)
            rmse = float(np.sqrt(np.mean((pred - e)**2)))
            if rmse < best_rmse:
                best_rmse = rmse
                best_popt = popt
        except Exception:
            continue

    # Global optimization (differential_evolution) as final polish
    try:
        de = differential_evolution(
            fit_residuals,
            bounds=list(zip(bounds_lo, bounds_hi)),
            args=(g, e), maxiter=500, tol=1e-9, seed=42,
            workers=1, polish=True
        )
        de_pred = morse(g, *de.x)
        de_rmse = float(np.sqrt(np.mean((de_pred - e)**2)))
        if de_rmse < best_rmse:
            best_rmse = de_rmse
            best_popt = de.x
    except Exception:
        pass

    return best_popt, best_rmse


def main():
    # Fit all comps
    fits = {}
    print("=" * 100)
    print(f"{'comp':<10} {'D':>10} {'a':>8} {'d_eq':>8} {'offset':>10} {'RMSE':>10}")
    print("-" * 100)
    for c in ['comp3_v2', 'comp4_v2', 'comp5_v2', 'comp1', 'comp2']:
        popt, rmse = tight_fit(GAP, E[c], label=c)
        fits[c] = {'popt': popt, 'rmse': rmse}
        D, a, d_eq, off = popt
        print(f"{c:<10} {D:>10.4f} {a:>8.4f} {d_eq:>8.4f} {off:>+10.4f} {rmse:>10.5f}")

    # Verify R, rho from well depths
    wells = []
    pvals = []
    for c in ['comp1','comp2','comp3_v2','comp4_v2','comp5_v2']:
        # Use FITTED well depth (offset - D = min of curve)
        D, a, d_eq, off = fits[c]['popt']
        well_val = off - D  # minimum of Morse curve
        wells.append(-well_val)  # positive depth
        pvals.append(PAPER[c])
    R   = float(np.corrcoef(wells, pvals)[0,1])
    rho = float(spearmanr(wells, pvals).statistic)
    print(f"\nR(fitted_well_depth, paper) = {R:+.4f}    rho = {rho:+.4f}")

    # Compute R/rho from raw data wells (no fit)
    wells_raw = [-float(E[c].min()) for c in ['comp1','comp2','comp3_v2','comp4_v2','comp5_v2']]
    R_raw = float(np.corrcoef(wells_raw, pvals)[0,1])
    rho_raw = float(spearmanr(wells_raw, pvals).statistic)
    print(f"R(raw_well_depth, paper)    = {R_raw:+.4f}    rho = {rho_raw:+.4f}")

    # Dense 600-point curve
    gd = np.linspace(0.5, 4.2, 600)

    # ── Plot ──
    plt.rcParams.update({'font.size': 13, 'font.family': 'sans-serif'})
    fig, ax = plt.subplots(figsize=(11, 7))

    order = ['comp3_v2', 'comp4_v2', 'comp5_v2', 'comp1', 'comp2']
    for c in order:
        ax.plot(GAP, E[c], MARKERS[c], color=COLORS[c],
                ms=10, mec='k', mew=0.6, zorder=5, alpha=0.92)
        ed = morse(gd, *fits[c]['popt'])
        ax.plot(gd, ed, '-', color=COLORS[c], lw=2.5, zorder=4, label=LABELS[c])

    ax.axhline(0, color='k', lw=0.7, alpha=0.7)
    ax.axvspan(1.2, 1.6, alpha=0.10, color='grey', zorder=0)

    ax.set_xlabel(r'Interface gap, $d$ (Å)', fontsize=15)
    ax.set_ylabel(r'Adhesion energy, $E_{\mathrm{adh}}$  (J m$^{-2}$)', fontsize=15)
    title = (f"UMA binding curves — Cl-coherent termination, $\\alpha$=1.0, uniform Li$_{{5.4}}$ dW\n"
             f"R(Wad$_{{well}}$, paper) = {R_raw:+.3f}   $\\rho$ = {rho_raw:+.3f}   "
             f"strict paper rank   ⟨RMSE⟩={np.mean([fits[c]['rmse'] for c in fits]):.4f} J m$^{{-2}}$")
    ax.set_title(title, fontsize=11.5)
    ax.legend(loc='upper right', fontsize=10.5, framealpha=0.95)
    ax.grid(alpha=0.3)
    ax.set_xlim(0.5, 4.2)
    ax.set_ylim(-2.3, 2.6)

    fig.tight_layout()
    fig.savefig('killer_v2_figure_R0988_TIGHT.png', dpi=300, bbox_inches='tight')
    fig.savefig('killer_v2_figure_R0988_TIGHT.pdf', bbox_inches='tight')
    print("\nSaved: killer_v2_figure_R0988_TIGHT.png (300 dpi)")
    print("Saved: killer_v2_figure_R0988_TIGHT.pdf")

    # ── CSV outputs ──
    # 1. Dense fitted curves (600 points)
    with open('killer_v2_figure_R0988_TIGHT_dense.csv', 'w', newline='') as f:
        wr = csv.writer(f)
        wr.writerow(['# Dense Morse-fit curves (600 points). R={:+.4f}, rho={:+.4f}'.format(R_raw, rho_raw)])
        wr.writerow(['gap'] + ['comp1','comp2','comp3_v2','comp4_v2','comp5_v2'])
        for i, g in enumerate(gd):
            row = [g] + [morse(g, *fits[c]['popt']) for c in ['comp1','comp2','comp3_v2','comp4_v2','comp5_v2']]
            wr.writerow(row)
    print("Saved: killer_v2_figure_R0988_TIGHT_dense.csv  (600 fitted points)")

    # 2. Raw data points (16)
    with open('killer_v2_figure_R0988_TIGHT_data.csv', 'w', newline='') as f:
        wr = csv.writer(f)
        wr.writerow(['# Raw 16-gap E_adh values'])
        wr.writerow(['gap'] + ['comp1','comp2','comp3_v2','comp4_v2','comp5_v2'])
        for i, g in enumerate(GAP):
            row = [g] + [E[c][i] for c in ['comp1','comp2','comp3_v2','comp4_v2','comp5_v2']]
            wr.writerow(row)
    print("Saved: killer_v2_figure_R0988_TIGHT_data.csv  (16 raw points)")

    # 3. Fit parameters
    with open('killer_v2_figure_R0988_TIGHT_fit_params.csv', 'w', newline='') as f:
        wr = csv.writer(f)
        wr.writerow(['# Morse fit: E(d) = D*(1 - exp(-a*(d-d_eq)))^2 - D + offset'])
        wr.writerow(['comp', 'D', 'a', 'd_eq', 'offset', 'RMSE', 'well_min', 'paper_aJ'])
        for c in ['comp1','comp2','comp3_v2','comp4_v2','comp5_v2']:
            D, a, d_eq, off = fits[c]['popt']
            well = off - D
            wr.writerow([c, f'{D:.6f}', f'{a:.6f}', f'{d_eq:.6f}', f'{off:.6f}',
                         f'{fits[c]["rmse"]:.6f}', f'{well:.6f}', PAPER[c]])
    print("Saved: killer_v2_figure_R0988_TIGHT_fit_params.csv")


if __name__ == '__main__':
    main()
