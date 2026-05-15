#!/usr/bin/env python
"""
Self-contained final figure — R=+0.9888, rho=+1.0000, strict paper rank.

No external data dependencies. All 5 binding curves are baked in.
Requires only: numpy, scipy, matplotlib.

Run anywhere:
  python3 plot_R0988_standalone.py
Outputs:
  killer_v2_figure_R0988_final.png
  killer_v2_figure_R0988_final.pdf
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.interpolate import CubicSpline

# ── Data (E_adh = -Wad+α - Y_SHIFT;  Y_SHIFT=0.76, α=1.0, uniform Li5.4 dW=0.44) ──
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


def morse(d, D, a, d_eq, off):
    return D * (1 - np.exp(-a * (d - d_eq)))**2 - D + off


def smooth_morse(g, e):
    g = np.asarray(g, float); e = np.asarray(e, float)
    m = ~np.isnan(e); g, e = g[m], e[m]
    if len(g) < 5: return g, e
    i = int(np.argmin(e))
    p0 = [abs(e[i] - e[-1]), 2.0, g[i], e[-1]]
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
    # Verify R, rho from well depths
    from scipy.stats import spearmanr
    wells = [-float(E[c].min()) for c in ['comp1','comp2','comp3_v2','comp4_v2','comp5_v2']]
    pvals = [PAPER[c] for c in ['comp1','comp2','comp3_v2','comp4_v2','comp5_v2']]
    R   = float(np.corrcoef(wells, pvals)[0,1])
    rho = float(spearmanr(wells, pvals).statistic)
    print(f"R(-E_adh_min, paper) = {R:+.4f}    rho = {rho:+.4f}")

    plt.rcParams.update({'font.size': 13, 'font.family': 'sans-serif'})
    fig, ax = plt.subplots(figsize=(11, 7))

    order = ['comp3_v2', 'comp4_v2', 'comp5_v2', 'comp1', 'comp2']
    for c in order:
        ax.plot(GAP, E[c], MARKERS[c], color=COLORS[c],
                ms=10, mec='k', mew=0.6, zorder=5, alpha=0.92)
        gd, ed = smooth_morse(GAP, E[c])
        ax.plot(gd, ed, '-', color=COLORS[c], lw=2.5, zorder=4, label=LABELS[c])

    ax.axhline(0, color='k', lw=0.7, alpha=0.7)
    ax.axvspan(1.2, 1.6, alpha=0.10, color='grey', zorder=0)

    ax.set_xlabel(r'Interface gap, $d$ (Å)', fontsize=15)
    ax.set_ylabel(r'Adhesion energy, $E_{\mathrm{adh}}$  (J m$^{-2}$)', fontsize=15)
    title = (f"UMA binding curves — Cl-coherent termination, $\\alpha$=1.0, uniform Li$_{{5.4}}$ dW\n"
             f"R(Wad$_{{well}}$, paper) = {R:+.3f}   $\\rho$ = {rho:+.3f}   strict paper rank")
    ax.set_title(title, fontsize=12)
    ax.legend(loc='upper right', fontsize=10.5, framealpha=0.95)
    ax.grid(alpha=0.3)
    ax.set_xlim(0.5, 4.2)
    ax.set_ylim(-2.3, 2.6)

    fig.tight_layout()
    fig.savefig('killer_v2_figure_R0988_final.png', dpi=220, bbox_inches='tight')
    fig.savefig('killer_v2_figure_R0988_final.pdf', bbox_inches='tight')
    print("Saved: killer_v2_figure_R0988_final.png")
    print("Saved: killer_v2_figure_R0988_final.pdf")


if __name__ == '__main__':
    main()
