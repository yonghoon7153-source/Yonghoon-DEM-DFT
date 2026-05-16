"""alpha_strain_fit.py — fit strain mixing α to recover paper trend.

Theory:
  After eiso_fix:  Wad_fixed   = (E_se + E_ncm_SE_cell - E_int) / A
                  → strain in NCM cancels (NCM at same strain in iso and in int)
                  → pure chemistry Wad

  Before fix:     Wad_unfixed = (E_se + E_ncm_NCM_cell - E_int) / A
                  → strain in NCM only in E_int, not in reference
                  → Wad = chemistry - W_strain  (W_strain > 0)

  Per-comp:       Wad_fixed - Wad_unfixed = ΔWad_strain   (saved as delta_Wad_J_per_m2)

  α-parametrized: Wad(α) = Wad_fixed - α × ΔWad_strain
                  α = 0  → pure chemistry (Wad_fixed)            paper-inverted
                  α = 1  → full strain   (Wad_unfixed = OLD)     paper-matching
                  0<α<1  → realistic mix (literature: 1L NCM ~0.5-1.0
                                          due to little dislocation room)

Procedure:
  • Sweep α ∈ [0, 1] in 21 steps
  • For each α, compute Wad_well_max per comp
  • R(Wad_well, paper_aJ) across n=3 (comp1, comp2, comp4) at each α
  • Find α* that maximizes R(α)
  • Plot:
      (left)  R(α) curve and α*
      (right) binding curves at α=0, α*, α=1 side-by-side

Output:
  /data/work/v30u_ensemble/alpha_strain_fit.{png,pdf,csv,json}

Run on gabia:
  cd /data/work/v30u_ensemble
  python3 alpha_strain_fit.py
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
FIXED = WORK / 'v30u_1L_correct_results_eiso_fix'
OUT_PNG = WORK / 'alpha_strain_fit.png'
OUT_PDF = WORK / 'alpha_strain_fit.pdf'
OUT_CSV = WORK / 'alpha_strain_fit.csv'
OUT_JSON= WORK / 'alpha_strain_fit.json'

COMPS = ['comp1', 'comp2', 'comp4', 'modelC']
PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp4': 298}   # aJ

COLORS  = {'comp1': '#1f77b4', 'comp2': '#17becf',
           'comp4': '#9467bd', 'modelC': '#888888'}
MARKERS = {'comp1': 's', 'comp2': 'o', 'comp4': 'D', 'modelC': 'P'}
LABELS  = {
    'comp1':  r'comp1: Li$_6$PS$_5$Cl',
    'comp2':  r'comp2: Li$_6$PS$_5$Cl$_{0.5}$Br$_{0.5}$',
    'comp4':  r'comp4: Li$_{5.4}$PS$_{4.4}$Cl$_{0.8}$Br$_{0.8}$',
    'modelC': r'modelC: Li$_{5.4}$PS$_{4.4}$Cl$_{1.6}$',
}


def morse(d, D, a, d_eq, offset):
    return D * (1 - np.exp(-a * (d - d_eq)))**2 - D + offset


def smooth_curve(g, e):
    g, e = np.asarray(g, float), np.asarray(e, float)
    valid = ~np.isnan(e)
    g, e = g[valid], e[valid]
    if len(g) < 5:
        return g, e
    i_min = int(np.argmin(e))
    p0 = [abs(e[i_min] - e[-1]), 2.0, g[i_min], e[-1]]
    try:
        popt, _ = curve_fit(morse, g, e, p0=p0, maxfev=20000,
                            bounds=([0.001, 0.1, 0.5, -5.0],
                                    [10.0, 10.0, 5.0, 5.0]))
        gd = np.linspace(g.min(), g.max(), 600)
        return gd, morse(gd, *popt)
    except Exception:
        cs = CubicSpline(g, e)
        gd = np.linspace(g.min(), g.max(), 600)
        return gd, cs(gd)


def main():
    # ─── 1. Load fixed data, extract per-comp Wad_curve and ΔWad ────────────
    data = {}
    for c in COMPS:
        f = FIXED / f"{c}_done.json"
        if not f.exists():
            print(f"[SKIP] {c}: no JSON")
            continue
        d = json.load(open(f))
        data[c] = {
            'gaps':      np.array(d['gaps'], dtype=float),
            'wad_fixed': np.array(d['Wad_mean'], dtype=float),  # 5z×36 mean
            'dWad':      d['delta_Wad_J_per_m2'],   # per-comp strain correction
        }
        i_min = int(np.nanargmin(-data[c]['wad_fixed']))  # wait, we want MAX of Wad
        # Wad_max = strongest binding (most positive Wad). E_adh_min = -Wad_max.
        i_max = int(np.nanargmax(data[c]['wad_fixed']))
        print(f"[{c}]  ΔWad_strain = {data[c]['dWad']:+.4f}  "
              f"Wad_max_fixed = {data[c]['wad_fixed'][i_max]:+.4f}  "
              f"asymp_fixed = {data[c]['wad_fixed'][-1]:+.4f}")

    # ─── 2. Sweep α, compute R(α) ───────────────────────────────────────────
    alphas = np.linspace(0.0, 1.5, 31)  # extend past 1.0 to see beyond OLD
    paper_comps = [c for c in COMPS if c in PAPER_EXP]
    paper_vals = np.array([PAPER_EXP[c] for c in paper_comps], dtype=float)

    R_curve = []
    for a in alphas:
        wm = []
        for c in paper_comps:
            wad_a = data[c]['wad_fixed'] - a * data[c]['dWad']
            wm.append(np.nanmax(wad_a))
        wm = np.array(wm)
        if wm.std() < 1e-9:
            R_curve.append(np.nan)
        else:
            R_curve.append(float(np.corrcoef(wm, paper_vals)[0, 1]))
    R_curve = np.array(R_curve)

    # Optimal α (maximize R)
    i_opt = int(np.nanargmax(R_curve))
    alpha_opt = float(alphas[i_opt])
    R_opt = float(R_curve[i_opt])
    print(f"\nα sweep result:")
    print(f"  α = 0.00 (eiso_fix, pure chem) → R = {R_curve[0]:+.3f}")
    print(f"  α = 1.00 (full strain = OLD)   → R = {R_curve[np.argmin(np.abs(alphas-1.0))]:+.3f}")
    print(f"  α = {alpha_opt:.2f} (optimal)         → R = {R_opt:+.3f}")

    # ─── 3. CSV: Wad_well per comp at α ∈ {0, opt, 1} ────────────────────────
    with open(OUT_CSV, 'w') as f:
        f.write("# α = strain fraction kept in Wad\n")
        f.write("# Wad(α) = Wad_fixed - α × ΔWad_strain\n")
        f.write(f"# Optimal α = {alpha_opt:.3f}  R = {R_opt:+.3f}\n")
        f.write("alpha,R," + ",".join([f"{c}_wad_max" for c in paper_comps]) + "\n")
        for a, R in zip(alphas, R_curve):
            wm = [np.nanmax(data[c]['wad_fixed'] - a * data[c]['dWad']) for c in paper_comps]
            f.write(f"{a:.3f},{R:+.4f}," + ",".join(f"{v:+.4f}" for v in wm) + "\n")

    json.dump({
        'alphas':         alphas.tolist(),
        'R_curve':        R_curve.tolist(),
        'alpha_optimal':  alpha_opt,
        'R_optimal':      R_opt,
        'paper_comps':    paper_comps,
        'paper_aJ':       paper_vals.tolist(),
        'per_comp_dWad':  {c: data[c]['dWad'] for c in COMPS if c in data},
    }, open(OUT_JSON, 'w'), indent=2)

    # ─── 4. Plot: 2-panel (R(α) | curves at 3 α values) ──────────────────────
    fig = plt.figure(figsize=(15, 6))
    gs = fig.add_gridspec(1, 4)
    ax_R = fig.add_subplot(gs[0, 0])

    # (a) R(α) curve
    ax_R.plot(alphas, R_curve, 'k-', lw=2)
    ax_R.axhline(0, color='gray', lw=0.6)
    ax_R.axvline(alpha_opt, color='red', lw=1.2, linestyle='--',
                 label=f'α* = {alpha_opt:.2f},  R = {R_opt:+.3f}')
    ax_R.axvline(0, color='blue', lw=0.8, alpha=0.5, linestyle=':')
    ax_R.axvline(1, color='blue', lw=0.8, alpha=0.5, linestyle=':')
    ax_R.text(0, ax_R.get_ylim()[1] * 0.92, 'eiso_fix\n(pure chem)',
              ha='center', fontsize=8, color='blue')
    ax_R.text(1, ax_R.get_ylim()[1] * 0.92, 'OLD\n(full strain)',
              ha='center', fontsize=8, color='blue')
    ax_R.set_xlabel(r'strain fraction $\alpha$')
    ax_R.set_ylabel(r'R(W$_{ad}$ at well, paper aJ)')
    ax_R.set_title('Family signal vs α', fontsize=11)
    ax_R.grid(alpha=0.3)
    ax_R.legend(loc='lower right', fontsize=9)

    # (b–d) binding curves at α = 0, opt, 1
    for k, (a, label) in enumerate([(0.0,         'α = 0  (chem only)'),
                                    (alpha_opt,   f'α* = {alpha_opt:.2f}  (best fit)'),
                                    (1.0,         'α = 1  (full strain / OLD)')]):
        ax = fig.add_subplot(gs[0, 1 + k])
        for c in COMPS:
            if c not in data: continue
            g = data[c]['gaps']
            wad = data[c]['wad_fixed'] - a * data[c]['dWad']
            e_adh = -wad
            ax.plot(g, e_adh, MARKERS[c], color=COLORS[c],
                    markersize=6, alpha=0.85, zorder=3)
            gd, ed = smooth_curve(g, e_adh)
            ax.plot(gd, ed, '-', color=COLORS[c], lw=2.0, zorder=2,
                    label=LABELS.get(c, c))
        ax.axhline(0, color='k', lw=0.6)
        ax.axvspan(1.2, 1.6, alpha=0.10, color='grey', zorder=0)
        # R at this α
        wm = [np.nanmax(data[c]['wad_fixed'] - a * data[c]['dWad'])
              for c in paper_comps]
        if np.std(wm) > 1e-9:
            R_a = float(np.corrcoef(wm, paper_vals)[0, 1])
        else:
            R_a = np.nan
        ax.set_title(f"{label}   R={R_a:+.3f}", fontsize=10)
        ax.set_xlabel(r'$d$ (Å)', fontsize=10)
        if k == 0:
            ax.set_ylabel(r'E$_{adh}$ = $-W_{ad}$  (J m$^{-2}$)', fontsize=10)
        if k == 2:
            ax.legend(loc='upper right', fontsize=7, framealpha=0.95)
        ax.grid(alpha=0.3)

    plt.suptitle('Strain-mixing fit: how much of the cell-mismatch '
                 'strain to keep for paper-trend recovery', fontsize=11, y=1.02)
    plt.tight_layout()
    plt.savefig(OUT_PNG, dpi=200, bbox_inches='tight')
    plt.savefig(OUT_PDF, bbox_inches='tight')
    print(f"\nSaved: {OUT_PNG}")
    print(f"Saved: {OUT_PDF}")
    print(f"Saved: {OUT_CSV}")
    print(f"Saved: {OUT_JSON}")
    print("\nInterpretation:")
    print(f"  α* = {alpha_opt:.2f} means {alpha_opt*100:.0f}% of theoretical strain")
    print(f"  needs to remain in the binding curve to recover paper-trend.")
    print(f"  Literature for 1L NCM: α ∈ [0.5, 1.0]. Check α* vs this range.")


if __name__ == "__main__":
    main()
