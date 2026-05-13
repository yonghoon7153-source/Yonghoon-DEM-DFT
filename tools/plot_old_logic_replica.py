"""plot_old_logic_replica.py — apply OLD figure logic to our face-flip data.

OLD figure logic (from plot_binding_curves_v2.py):
  1. For each gap, take MAX Wad over registries (not mean)
  2. Compute per-comp asymptote = mean of Wad at gap >= 3.0
  3. Subtract per-comp asymptote → Wad' = Wad - asymp_per_comp
  4. Plot E_adh = -Wad'  (so canonical: wells negative, asymp at 0)

Apply this to our face-flip data (z=0, 36 registries × 16 gaps) for face A
and face B separately.

Question: does the OLD-logic processing (max + per-comp asymp subtract)
give paper-direction R or paper-inverted R when applied to our UMA data?
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import curve_fit

WORK = Path('/data/work/v30u_ensemble')
FACE = WORK / 'face_flip_results'

COMPS = ['comp1', 'comp2', 'comp4_v1', 'comp4_v2', 'modelC']
PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp4_v1': 298, 'comp4_v2': 298,
             'modelC': None}

COLORS  = {'comp1':'#1f77b4', 'comp2':'#17becf', 'comp4_v1':'#9467bd',
           'comp4_v2':'#d62728', 'modelC':'#2ca02c'}
MARKERS = {'comp1':'s', 'comp2':'o', 'comp4_v1':'D', 'comp4_v2':'X', 'modelC':'v'}
LABELS  = {
    'comp1':    r'comp1: Li$_6$PS$_5$Cl',
    'comp2':    r'comp2: Li$_6$PS$_5$Cl$_{0.5}$Br$_{0.5}$',
    'comp4_v1': r'comp4 (v1): Li$_{5.4}$PS$_{4.4}$Cl$_{0.8}$Br$_{0.8}$',
    'comp4_v2': r'comp4 (v2): Li$_{5.4}$PS$_{4.4}$Cl$_{0.8}$Br$_{0.8}$',
    'modelC':   r'modelC: Li$_{5.4}$PS$_{4.4}$Cl$_{1.6}$',
}

ASYMP_GAP_MIN = 3.0   # gap >= this = asymptote region


def morse(d, D, a, d_eq, offset):
    return D * (1 - np.exp(-a * (d - d_eq)))**2 - D + offset


def smooth(g, e):
    g, e = np.asarray(g, float), np.asarray(e, float)
    v = ~np.isnan(e); g, e = g[v], e[v]
    if len(g) < 5: return g, e
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


def extract_max_per_gap(face_data, gaps):
    """For each gap, return MAX Wad over 36 registries (not mean)."""
    wad_max = []
    for g in gaps:
        gk = f"{g:.3f}"
        vals = [reg['curve'][gk]['Wad_J_per_m2']
                for reg in face_data['per_reg'].values()
                if reg['curve'].get(gk, {}).get('Wad_J_per_m2') is not None]
        wad_max.append(float(np.max(vals)) if vals else np.nan)
    return np.array(wad_max)


def extract_mean_per_gap(face_data, gaps):
    """For each gap, return MEAN Wad over 36 registries."""
    return np.array(face_data['Wad_mean'], dtype=float)


def process_old_logic(wad_per_gap, gaps):
    """OLD logic: subtract per-comp asymptote (mean of gap >= 3.0 region)."""
    asymp_mask = gaps >= ASYMP_GAP_MIN
    asymp = float(np.nanmean(wad_per_gap[asymp_mask])) if asymp_mask.any() else 0.0
    wad_corr = wad_per_gap - asymp
    return wad_corr, asymp


def plot_panel(ax, data_dict, gaps, title):
    """data_dict: {comp: e_adh_curve}"""
    paper, wmax, names = [], [], []
    for c, e in data_dict.items():
        ax.plot(gaps, e, MARKERS[c], color=COLORS[c], ms=7, mec='k', mew=0.5, zorder=5)
        gd, ed = smooth(gaps, e)
        ax.plot(gd, ed, '-', color=COLORS[c], lw=2.2, label=LABELS[c], zorder=4)
        if PAPER_EXP[c] is not None:
            wmax.append(-np.nanmin(e))   # Wad_well = -min(E_adh) = max(Wad)
            paper.append(PAPER_EXP[c])
            names.append(c)
    R = None
    if len(paper) >= 2:
        R = float(np.corrcoef(paper, wmax)[0, 1])
    ax.axhline(0, color='k', lw=0.6)
    ax.axvspan(1.2, 1.6, alpha=0.10, color='grey', zorder=0)
    ax.set_xlabel(r'$d$ (Å)', fontsize=11)
    title_with_R = f"{title}   R={R:+.3f}" if R is not None else title
    ax.set_title(title_with_R, fontsize=10)
    ax.grid(alpha=0.3)
    return R


def main():
    out_data = {'logic': 'OLD: max over reg + per-comp asymp subtract'}

    # ── 4-panel figure ──────────────────────────────────────
    fig, axes = plt.subplots(2, 2, figsize=(15, 11), sharey='row', sharex=True)

    for col, face in enumerate(['A', 'B']):
        for row, mode in enumerate(['max', 'mean']):
            ax = axes[row, col]
            data_dict = {}
            gaps_arr = None
            for c in COMPS:
                f_path = FACE / f"{c}_done.json"
                if not f_path.exists(): continue
                ff = json.load(open(f_path))
                if face not in ff['faces']: continue
                gaps_arr = np.array(ff['gaps'])
                face_d = ff['faces'][face]
                if mode == 'max':
                    wad_per_gap = extract_max_per_gap(face_d, gaps_arr)
                else:
                    wad_per_gap = extract_mean_per_gap(face_d, gaps_arr)
                wad_corr, asymp = process_old_logic(wad_per_gap, gaps_arr)
                e_adh = -wad_corr
                data_dict[c] = e_adh
                out_data.setdefault(f"face{face}_{mode}", {})[c] = {
                    'asymp_raw': asymp,
                    'wad_well':  float(np.nanmax(wad_corr)),
                    'e_adh_well': float(np.nanmin(e_adh)),
                }
            R = plot_panel(ax, data_dict, gaps_arr,
                           f"face {face} — {mode} over 36 reg")
            out_data.setdefault(f"face{face}_{mode}", {})['R'] = R

        axes[row, col].set_xlabel(r'$d$ (Å)', fontsize=11)
    axes[0, 0].set_ylabel(r'$E_{adh}$ (J m$^{-2}$),  asymp-subtracted', fontsize=11)
    axes[1, 0].set_ylabel(r'$E_{adh}$ (J m$^{-2}$),  asymp-subtracted', fontsize=11)
    axes[0, 1].legend(loc='upper right', fontsize=8, framealpha=0.95)
    plt.suptitle('OLD-logic replica: per-comp asymp subtract, '
                 'MAX (top) vs MEAN (bottom) over 36 registries', fontsize=12)
    fig.tight_layout()
    fig.savefig(WORK / 'old_logic_replica.png', dpi=200, bbox_inches='tight')
    fig.savefig(WORK / 'old_logic_replica.pdf', bbox_inches='tight')
    plt.close()
    print(f"saved old_logic_replica.png/pdf")

    # ── summary print ────────────────────────────────────────
    print("\n── Summary ──")
    for key in sorted([k for k in out_data if k.startswith('face')]):
        info = out_data[key]
        R = info.pop('R', None)
        print(f"\n  {key}:  R(paper) = {R:+.3f}" if R is not None else f"\n  {key}:")
        for c, v in info.items():
            tag = f"(paper {PAPER_EXP[c]})" if PAPER_EXP[c] else ""
            print(f"    {c:<10} asymp={v['asymp_raw']:>+6.3f}  "
                  f"well_Wad={v['wad_well']:>+6.3f}  E_adh_well={v['e_adh_well']:>+6.3f}  {tag}")

    json.dump(out_data, open(WORK / 'old_logic_replica.json', 'w'), indent=2)


if __name__ == "__main__":
    main()
