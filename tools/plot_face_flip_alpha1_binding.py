"""plot_face_flip_alpha1_binding.py — binding curves from face-flip + α=1 strain.

For each comp in face_flip_results/, choose a face (A, B, or best/canonical):
  • Compute 36-reg mean Wad curve (face A or B)
  • Apply α=1 strain correction: Wad(α=1) = Wad - ΔW_strain
    where ΔW_strain = delta_Wad_J_per_m2 from eiso_fix JSON (per comp)
  • Plot E_adh = -Wad(α=1) vs gap

Outputs three figures:
  (1) face A + α=1   — original-bottom termination
  (2) face B + α=1   — flipped (other face) termination
  (3) face A vs B    — side-by-side

Absolute values won't match the OLD figure (scale different) but the
family ordering and curve shape should appear canonical.
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
EISO = WORK / 'v30u_1L_correct_results_eiso_fix'

# Map face-flip comp → eiso_fix comp (for ΔW_strain lookup)
COMP_KEYS = {
    'comp1':    'comp1',
    'comp2':    'comp2',
    'comp4_v1': 'comp4',
    'comp4_v2': 'comp4',
    'modelC':   'modelC',
}

# Per-comp ΔW_strain (from eiso_fix data)
# comp4_v1 and comp4_v2 use same NCM 5x5 but DIFFERENT SE cells.
# We use comp4_v1's value as proxy for comp4_v2 (close enough for narrative).

PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp4': 298, 'modelC': None}

COLORS = {
    'comp1':    '#1f77b4',
    'comp2':    '#17becf',
    'comp4_v1': '#9467bd',
    'comp4_v2': '#9467bd',
    'modelC':   '#2ca02c',
}
MARKERS = {'comp1':'s', 'comp2':'o', 'comp4_v1':'D', 'comp4_v2':'D', 'modelC':'v'}
LABELS = {
    'comp1':    r'comp1: Li$_6$PS$_5$Cl',
    'comp2':    r'comp2: Li$_6$PS$_5$Cl$_{0.5}$Br$_{0.5}$',
    'comp4_v1': r'comp4 (v1): Li$_{5.4}$PS$_{4.4}$Cl$_{0.8}$Br$_{0.8}$',
    'comp4_v2': r'comp4 (v2): Li$_{5.4}$PS$_{4.4}$Cl$_{0.8}$Br$_{0.8}$',
    'modelC':   r'modelC: Li$_{5.4}$PS$_{4.4}$Cl$_{1.6}$',
}


def morse(d, D, a, d_eq, offset):
    return D * (1 - np.exp(-a * (d - d_eq)))**2 - D + offset


def smooth(g, e):
    g, e = np.asarray(g, float), np.asarray(e, float)
    valid = ~np.isnan(e)
    g, e = g[valid], e[valid]
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


def load_face_data():
    """Returns {comp: {face: (gaps, Wad_corrected_mean)}}.
    Applies α=1 strain correction using comp's eiso_fix ΔW_strain."""
    data = {}
    for c_face, c_eiso in COMP_KEYS.items():
        ff_path = FACE / f"{c_face}_done.json"
        eiso_path = EISO / f"{c_eiso}_done.json"
        if not ff_path.exists(): continue
        ff = json.load(open(ff_path))
        if not eiso_path.exists():
            print(f"  [WARN] no eiso JSON for {c_eiso}, skip strain correction")
            dW = 0.0
        else:
            dW = json.load(open(eiso_path))['delta_Wad_J_per_m2']
        gaps = np.array(ff['gaps'])
        comp_d = {'dW_strain': dW, 'faces': {}}
        for face_name in ['A', 'B']:
            face = ff['faces'].get(face_name)
            if not face: continue
            wad_mean = np.array(face['Wad_mean'], dtype=float)
            # α=1 correction: subtract ΔW_strain
            wad_corr = wad_mean - dW
            comp_d['faces'][face_name] = {
                'gaps':       gaps,
                'wad_raw':    wad_mean,
                'wad_corr':   wad_corr,
                'eadh_corr':  -wad_corr,
                'wad_well':   float(np.nanmax(wad_corr)),
                'wad_asymp':  float(wad_corr[-1]),
            }
        data[c_face] = comp_d
    return data


def compute_R(data, face):
    """R(Wad_well, paper_aJ) for paper comps."""
    paper, wmax, names = [], [], []
    for c, info in data.items():
        if c not in PAPER_EXP or PAPER_EXP[c] is None: continue
        f = info['faces'].get(face)
        if f is None: continue
        paper.append(PAPER_EXP[c])
        wmax.append(f['wad_well'])
        names.append(c)
    if len(paper) < 2: return None, names
    return float(np.corrcoef(paper, wmax)[0, 1]), names


def plot_one(data, face_name, out_path, title_suffix=""):
    R, names = compute_R(data, face_name)
    plt.rcParams.update({'font.size': 13, 'legend.fontsize': 10})
    fig, ax = plt.subplots(figsize=(11, 7))
    plot_order = ['comp1', 'comp2', 'comp4_v1', 'comp4_v2', 'modelC']
    for c in plot_order:
        if c not in data: continue
        if face_name not in data[c]['faces']: continue
        d = data[c]['faces'][face_name]
        g = d['gaps']; e = d['eadh_corr']
        ax.plot(g, e, MARKERS[c], color=COLORS[c], ms=8, mec='k', mew=0.5,
                alpha=0.92, zorder=5)
        gd, ed = smooth(g, e)
        ax.plot(gd, ed, '-', color=COLORS[c], lw=2.4, zorder=4,
                label=LABELS.get(c, c))
    ax.axhline(0, color='k', lw=0.7, zorder=1)
    ax.axvspan(1.2, 1.6, alpha=0.10, color='grey', zorder=0)
    ax.set_xlabel(r'Interface gap, $d$ (Å)', fontsize=14)
    ax.set_ylabel(r'Adhesion energy, $E_{adh}=-W_{ad}$  (J m$^{-2}$)', fontsize=14)
    title = f"UMA binding curves — face {face_name} + α=1 strain correction"
    if R is not None: title += f"   R={R:+.3f} (n={len(names)})"
    if title_suffix: title += "   " + title_suffix
    ax.set_title(title, fontsize=12)
    ax.legend(loc='upper right', fontsize=10, framealpha=0.95)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches='tight')
    fig.savefig(out_path.with_suffix('.pdf'), bbox_inches='tight')
    plt.close()
    print(f"  saved {out_path}")
    return R, names


def plot_compare(data, out_path):
    """2-panel A vs B side by side."""
    plt.rcParams.update({'font.size': 12, 'legend.fontsize': 9})
    fig, axes = plt.subplots(1, 2, figsize=(15, 6.5), sharey=True)
    plot_order = ['comp1', 'comp2', 'comp4_v1', 'comp4_v2', 'modelC']
    for ax, face_name in zip(axes, ['A', 'B']):
        R, names = compute_R(data, face_name)
        for c in plot_order:
            if c not in data: continue
            if face_name not in data[c]['faces']: continue
            d = data[c]['faces'][face_name]
            g, e = d['gaps'], d['eadh_corr']
            ax.plot(g, e, MARKERS[c], color=COLORS[c], ms=7, mec='k', mew=0.5, zorder=5)
            gd, ed = smooth(g, e)
            ax.plot(gd, ed, '-', color=COLORS[c], lw=2.2,
                    label=LABELS.get(c, c) if face_name == 'B' else None)
        ax.axhline(0, color='k', lw=0.6)
        ax.axvspan(1.2, 1.6, alpha=0.10, color='grey')
        ax.set_xlabel(r'$d$ (Å)', fontsize=12)
        ax.set_title(f"face {face_name} + α=1   R={R:+.3f} (n={len(names)})" if R else f"face {face_name}",
                     fontsize=11)
        ax.grid(alpha=0.3)
    axes[0].set_ylabel(r'$E_{adh}$ (J m$^{-2}$)', fontsize=12)
    axes[1].legend(loc='upper right', fontsize=9)
    plt.suptitle('Face A (original-bottom) vs Face B (flipped) — α=1 strain corrected', fontsize=12)
    fig.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches='tight')
    fig.savefig(out_path.with_suffix('.pdf'), bbox_inches='tight')
    plt.close()
    print(f"  saved {out_path}")


def print_summary(data):
    print("\n── Summary (α=1 corrected, 36-reg mean) ──")
    print(f"{'comp':<10} {'dW_str':>8} | {'A_well':>8} {'A_asymp':>8} | {'B_well':>8} {'B_asymp':>8}")
    for c in ['comp1', 'comp2', 'comp4_v1', 'comp4_v2', 'modelC']:
        if c not in data: continue
        d = data[c]
        a = d['faces'].get('A', {}); b = d['faces'].get('B', {})
        aw = a.get('wad_well', np.nan); aa = a.get('wad_asymp', np.nan)
        bw = b.get('wad_well', np.nan); ba = b.get('wad_asymp', np.nan)
        print(f"{c:<10} {d['dW_strain']:>+8.3f} | {aw:>+8.3f} {aa:>+8.3f} | {bw:>+8.3f} {ba:>+8.3f}")


def main():
    print("Loading face-flip data + applying α=1 strain correction...\n")
    data = load_face_data()
    print_summary(data)
    print()
    R_A, _ = plot_one(data, 'A', WORK / 'binding_curves_alpha1_faceA.png',
                      title_suffix='(face A = original bottom)')
    R_B, _ = plot_one(data, 'B', WORK / 'binding_curves_alpha1_faceB.png',
                      title_suffix='(face B = flipped)')
    plot_compare(data, WORK / 'binding_curves_alpha1_AvsB.png')
    print()
    print(f"R(face A, paper) = {R_A:+.3f}")
    print(f"R(face B, paper) = {R_B:+.3f}")


if __name__ == "__main__":
    main()
