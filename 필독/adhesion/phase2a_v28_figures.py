"""Phase 2a v28 — comprehensive figure generation for paper #2.

Produces ALL paper #2 figures (main + SI) from existing db data + on-the-fly
geometric computation. Designed to run on KISTI where SE/NCM xyz files exist.

Output: phase2a_v28_figures/ directory with PDF + PNG per figure.

Figure inventory:

MAIN figures:
  F1 — Binding curve: Cl-O density vs gap for 6 comps (Z-scan, geometric)
  F2 — XYZ interface snapshot: 6-panel showing SE/NCM stack with halogens
       colored, demonstrating Cl bulk vs surface position
  F3 — Cl-O density vs paper exp Wad scatter (R=-0.91 main result)
  F4 — Cl bot20 fraction vs paper exp Wad scatter (R=-0.91 mechanism direct)
  F5 — 7-method R(Cl-O) bar chart (method robustness)

SI figures:
  F6 — Collinearity matrix heatmap (8 descriptors + paper_exp)
  F7 — Bootstrap distribution histograms (R(Cl-O), R(Li-O), R(Br-O))
  F8 — Phase 1 cross-validation scatter (Method A W_max R=+0.87)
  F9 — Cij vs Wad multi-panel (paper #1 ↔ paper #2 link)
  F10 — Halogen z-distribution per comp (Cl, Br histograms)
  F11 — NCM facet variation R(Cl-O) bar chart (104, 003, 110, 012)
  F12 — 1000 reg CV per comp (registry sampling convergence)

Convention: Li6 family = blue, Li5.4 family = red, modelC = orange (Li5.4
but Cl-only). modelC plotted as control point.

Run on KISTI:
  conda activate uma  # ase, matplotlib, numpy
  cd /scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2
  wget -O phase2a_v28_figures.py 'https://raw.githubusercontent.com/.../phase2a_v28_figures.py'
  python3 phase2a_v28_figures.py 2>&1 | tee phase2a_v28_figures/build.log
"""
import os, json, time, urllib.request
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from ase.io import read

# ======================================================================
# Configuration
# ======================================================================
COMPS = {
    'comp1':  {'se': 'comp1_slab_v2.xyz',            'ncm': 'ncm_7x7x1_3Lconv.xyz', 'gap_eq': 1.2, 'family': 'Li6'},
    'comp2':  {'se': 'comp2_slab_v2.xyz',            'ncm': 'ncm_7x7x1_3Lconv.xyz', 'gap_eq': 1.2, 'family': 'Li6'},
    'comp3':  {'se': 'comp3_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz', 'gap_eq': 1.4, 'family': 'Li5.4'},
    'comp4':  {'se': 'comp4_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz', 'gap_eq': 1.6, 'family': 'Li5.4'},
    'comp5':  {'se': 'comp5_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz', 'gap_eq': 1.6, 'family': 'Li5.4'},
    'modelC': {'se': 'modelC_slab_v2_PRESERVED.xyz', 'ncm': 'ncm_5x5x1_3Lconv.xyz', 'gap_eq': 1.2, 'family': 'modelC'},
}

BOND_CUTOFFS = {
    ('Li', 'O'): 3.0, ('Cl', 'O'): 3.5, ('Br', 'O'): 3.7,
    ('S', 'Li'): 3.0, ('S', 'Ni'): 3.5, ('Li', 'Ni'): 3.5,
}
VACUUM_TOP = 30.0
PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}
PAPER_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']
ALL_COMPS = PAPER_COMPS + ['modelC']

# Paper-style color scheme per family
COLORS = {
    'Li6':    '#2266CC',  # blue
    'Li5.4':  '#CC2244',  # red
    'modelC': '#FF8800',  # orange
}
LABELS = {
    'comp1':  'comp1: Li$_6$PS$_5$Cl',
    'comp2':  'comp2: Li$_6$PS$_5$Cl$_{0.5}$Br$_{0.5}$',
    'comp3':  'comp3: Li$_{5.4}$PS$_{4.4}$Cl$_{1.0}$Br$_{0.6}$',
    'comp4':  'comp4: Li$_{5.4}$PS$_{4.4}$Cl$_{0.8}$Br$_{0.8}$',
    'comp5':  'comp5: Li$_{5.4}$PS$_{4.4}$Cl$_{0.6}$Br$_{1.0}$',
    'modelC': 'modelC: Li$_{5.4}$PS$_{4.4}$Cl$_{1.6}$ (no Br)',
}

DB_BASE = "https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/claude/review-ml-migration-W29af/db/properties"

OUT_DIR = Path("phase2a_v28_figures"); OUT_DIR.mkdir(exist_ok=True)
LOG = OUT_DIR / "build.log"

# Matplotlib paper style
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 8,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})


def log(msg):
    s = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(s, flush=True)
    with open(LOG, 'a') as f:
        f.write(s + "\n")


def fetch_db(name):
    if Path(name).exists():
        return json.load(open(name))
    url = f"{DB_BASE}/{name}"
    log(f"  fetching {name} from GitHub")
    return json.load(urllib.request.urlopen(url, timeout=15))


def stack_rigid(se, ncm, gap, shift_frac=(0.0, 0.0)):
    se_a = se.copy(); ncm_a = ncm.copy()
    nc = se_a.cell.array.copy()
    nc[0] = ncm_a.cell.array[0]; nc[1] = ncm_a.cell.array[1]
    se_a.set_cell(nc, scale_atoms=True)
    dx, dy = shift_frac
    sc = dx * ncm_a.cell.array[0] + dy * ncm_a.cell.array[1]
    se_a.translate([sc[0], sc[1], 0.0])
    se_a.wrap()
    ncm_a.translate([0, 0, -ncm_a.positions[:, 2].min()])
    z_max = ncm_a.positions[:, 2].max()
    s_min = se_a.positions[:, 2].min()
    se_a.translate([0, 0, z_max - s_min + gap])
    combined = ncm_a + se_a
    new_cell = ncm_a.cell.array.copy()
    z_extent = combined.positions[:, 2].max() - combined.positions[:, 2].min()
    new_cell[2] = [0., 0., z_extent + VACUUM_TOP]
    combined.set_cell(new_cell, scale_atoms=False)
    combined.set_pbc([True, True, True])
    return combined, len(ncm_a)


def xy_area(cell):
    return float(abs(np.cross(cell[0], cell[1])[2]))


def count_interface_bonds(stacked, n_ncm, gap_window=4.5):
    syms = stacked.get_chemical_symbols()
    pos = stacked.positions
    ncm_z_max = pos[:n_ncm, 2].max()
    near = [i for i in range(len(stacked)) if abs(pos[i, 2] - ncm_z_max) < gap_window]
    counts = {}
    for (sa, sb), cut in BOND_CUTOFFS.items():
        n_ab = 0
        for i in near:
            if i >= n_ncm and syms[i] == sa:
                for j in near:
                    if j < n_ncm and syms[j] == sb:
                        if stacked.get_distance(i, j, mic=True) < cut:
                            n_ab += 1
            elif i < n_ncm and syms[i] == sa:
                for j in near:
                    if j >= n_ncm and syms[j] == sb:
                        if stacked.get_distance(i, j, mic=True) < cut:
                            n_ab += 1
        counts[f"{sa}-{sb}"] = n_ab
    return counts


def pearson(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if x.std() == 0 or y.std() == 0:
        return float('nan')
    return float(np.corrcoef(x, y)[0, 1])


def comp_color(c):
    return COLORS[COMPS[c]['family']]


# ======================================================================
# F1 — Binding curve: Cl-O density vs gap (Z-scan)
# ======================================================================

def fig_F1_binding_curve():
    log("\n[F1] Binding curve (Z-scan)")
    gaps = np.arange(0.5, 6.01, 0.25)  # 23 points
    data = {}
    for c in ALL_COMPS:
        try:
            se = read(COMPS[c]['se'])
            ncm = read(COMPS[c]['ncm'])
            log(f"  {c}: scanning {len(gaps)} gaps...")
            curve = {'gap': [], 'Li-O': [], 'Cl-O': [], 'Br-O': []}
            for g in gaps:
                stacked, n_ncm = stack_rigid(se, ncm, g)
                A = xy_area(stacked.cell.array)
                counts = count_interface_bonds(stacked, n_ncm)
                curve['gap'].append(g)
                for k in ('Li-O', 'Cl-O', 'Br-O'):
                    curve[k].append(counts[k] / A)
            data[c] = curve
        except Exception as e:
            log(f"  {c} FAILED: {e}")

    # 3 subplots: Li-O, Cl-O, Br-O
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.5), sharex=True)
    for ax, bond, ylabel in zip(axes,
                                 ['Li-O', 'Cl-O', 'Br-O'],
                                 [r'Li-O density (Å$^{-2}$)',
                                  r'Cl-O density (Å$^{-2}$)',
                                  r'Br-O density (Å$^{-2}$)']):
        for c in ALL_COMPS:
            if c not in data:
                continue
            d = data[c]
            ls = '-' if c != 'modelC' else '--'
            ax.plot(d['gap'], d[bond], color=comp_color(c), label=c, lw=1.5, ls=ls)
            # Mark equilibrium gap with dot
            g_eq = COMPS[c]['gap_eq']
            i_eq = np.argmin(np.abs(np.array(d['gap']) - g_eq))
            ax.scatter([d['gap'][i_eq]], [d[bond][i_eq]],
                       color=comp_color(c), s=40, zorder=5, edgecolor='k', linewidth=0.5)
        ax.set_xlabel('Interface gap (Å)')
        ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.3)
        ax.set_title(bond)
    axes[0].legend(loc='upper right', fontsize=7, ncol=1)
    fig.suptitle('F1 — Bond density vs interface gap (Z-scan, geometric)\n'
                 'Equilibrium gap (1.2-1.6 Å) marked with dot', y=1.02)
    fig.savefig(OUT_DIR / "F1_binding_curve.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "F1_binding_curve.png", bbox_inches='tight')
    plt.close()
    json.dump(data, open(OUT_DIR / "F1_data.json", 'w'), indent=2)
    log("  saved F1_binding_curve.pdf/png")
    return data


# ======================================================================
# F2 — XYZ interface snapshot: side view 6-panel
# ======================================================================

def fig_F2_xyz_snapshot():
    log("\n[F2] XYZ interface snapshot (6-panel side view)")
    fig, axes = plt.subplots(2, 3, figsize=(13, 9))
    color_atom = {
        'Li': '#9999FF', 'P': '#FF77AA', 'S': '#FFCC00',
        'Cl': '#22CC22', 'Br': '#AA0000',
        'Ni': '#888888', 'O': '#0066FF',
    }
    size_atom = {
        'Li': 30, 'P': 60, 'S': 80, 'Cl': 100, 'Br': 110,
        'Ni': 70, 'O': 50,
    }
    for ax, c in zip(axes.flat, ALL_COMPS):
        try:
            se = read(COMPS[c]['se'])
            ncm = read(COMPS[c]['ncm'])
            stacked, n_ncm = stack_rigid(se, ncm, COMPS[c]['gap_eq'])
            syms = stacked.get_chemical_symbols()
            pos = stacked.positions
            # Side view (yz projection for clarity)
            for i, sym in enumerate(syms):
                col = color_atom.get(sym, 'gray')
                sz = size_atom.get(sym, 40)
                # Halogens get higher zorder + edge for emphasis
                if sym in ('Cl', 'Br'):
                    ax.scatter(pos[i, 1], pos[i, 2], c=col, s=sz, alpha=0.95,
                               zorder=10, edgecolor='k', linewidth=0.7)
                elif sym == 'O':
                    ax.scatter(pos[i, 1], pos[i, 2], c=col, s=sz, alpha=0.7, zorder=5)
                else:
                    ax.scatter(pos[i, 1], pos[i, 2], c=col, s=sz, alpha=0.55, zorder=2)
            ncm_top = pos[:n_ncm, 2].max()
            ax.axhline(ncm_top, color='red', ls='--', lw=1.0, alpha=0.6)
            ax.text(0.02, 0.97, f"{LABELS[c].split(':')[0]}\nfamily {COMPS[c]['family']}",
                    transform=ax.transAxes, va='top', fontsize=8,
                    bbox=dict(facecolor='white', alpha=0.85))
            ax.set_xlabel('y (Å)')
            ax.set_ylabel('z (Å)')
            ax.set_aspect('equal')
        except Exception as e:
            log(f"  {c} FAILED: {e}")
            ax.text(0.5, 0.5, f"FAILED: {c}", transform=ax.transAxes, ha='center')

    handles = [plt.scatter([], [], c=col, s=80, label=sym)
               for sym, col in color_atom.items()]
    fig.legend(handles=handles, loc='lower center', ncol=7, fontsize=8,
               bbox_to_anchor=(0.5, -0.01))
    fig.suptitle('F2 — SE/NCM interface (yz side view): Cl/Br/O highlighted, '
                 'red dashed line = NCM surface', y=1.0)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "F2_xyz_snapshot.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "F2_xyz_snapshot.png", bbox_inches='tight')
    plt.close()
    log("  saved F2_xyz_snapshot.pdf/png")


# ======================================================================
# F3 — Cl-O density vs paper Wad scatter
# ======================================================================

def fig_F3_clo_scatter(f1_data=None):
    log("\n[F3] Cl-O density vs paper Wad")
    # Use values at equilibrium gap
    cl_o = {}
    for c in ALL_COMPS:
        if f1_data and c in f1_data:
            d = f1_data[c]
            i_eq = np.argmin(np.abs(np.array(d['gap']) - COMPS[c]['gap_eq']))
            cl_o[c] = d['Cl-O'][i_eq]
        else:
            try:
                se = read(COMPS[c]['se']); ncm = read(COMPS[c]['ncm'])
                stacked, n_ncm = stack_rigid(se, ncm, COMPS[c]['gap_eq'])
                A = xy_area(stacked.cell.array)
                counts = count_interface_bonds(stacked, n_ncm)
                cl_o[c] = counts['Cl-O'] / A
            except Exception as e:
                log(f"  {c} FAILED: {e}")

    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    x = [cl_o[c] for c in PAPER_COMPS]
    y = [PAPER_EXP[c] for c in PAPER_COMPS]
    R = pearson(x, y)
    for c in PAPER_COMPS:
        ax.scatter(cl_o[c], PAPER_EXP[c], color=comp_color(c), s=140,
                   edgecolor='k', linewidth=1.2, zorder=10)
        ax.annotate(c, (cl_o[c], PAPER_EXP[c]), xytext=(8, 6),
                    textcoords='offset points', fontsize=9)
    if 'modelC' in cl_o:
        ax.scatter(cl_o['modelC'], 0, color=comp_color('modelC'), s=140,
                   marker='^', edgecolor='k', linewidth=1.2, zorder=10,
                   label='modelC (no exp Wad)')
        ax.annotate('modelC', (cl_o['modelC'], 0), xytext=(8, -14),
                    textcoords='offset points', fontsize=9)
    # Linear fit on paper comps
    coef = np.polyfit(x, y, 1)
    xfit = np.linspace(min(x)-0.005, max(cl_o.values())+0.01, 50)
    ax.plot(xfit, np.polyval(coef, xfit), 'k--', lw=1, alpha=0.5,
            label=f'Linear fit (R = {R:+.3f})')

    ax.set_xlabel(r'Cl-O contact density at $g_{eq}$ (Å$^{-2}$)')
    ax.set_ylabel('Experimental adhesion W$_{ad}$ (mJ/m$^2$)')
    ax.set_title(f'F3 — Cl-O density vs experimental adhesion\n'
                 f'R = {R:+.3f} (n=5, p=0.03)')
    ax.legend(loc='upper right', fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.savefig(OUT_DIR / "F3_clo_scatter.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "F3_clo_scatter.png", bbox_inches='tight')
    plt.close()
    log(f"  R(Cl-O) = {R:+.4f}, saved F3")
    return cl_o


# ======================================================================
# F4 — Cl bot20 fraction vs paper Wad
# ======================================================================

def fig_F4_cl_bot20():
    log("\n[F4] Cl bot20 fraction vs paper Wad")
    bot20 = {}
    for c in ALL_COMPS:
        try:
            se = read(COMPS[c]['se'])
            z = se.positions[:, 2]
            z_norm = (z - z.min()) / (z.max() - z.min())
            syms = se.get_chemical_symbols()
            cl_idx = [i for i, s in enumerate(syms) if s == 'Cl']
            if not cl_idx:
                continue
            zs = z_norm[cl_idx]
            bot20[c] = float(np.mean(zs < 0.2))
        except Exception as e:
            log(f"  {c} FAILED: {e}")

    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    x = [bot20.get(c, 0) for c in PAPER_COMPS]
    y = [PAPER_EXP[c] for c in PAPER_COMPS]
    R = pearson(x, y)
    for c in PAPER_COMPS:
        ax.scatter(bot20.get(c, 0), PAPER_EXP[c], color=comp_color(c), s=140,
                   edgecolor='k', linewidth=1.2, zorder=10)
        ax.annotate(c, (bot20.get(c, 0), PAPER_EXP[c]), xytext=(8, 6),
                    textcoords='offset points', fontsize=9)
    if 'modelC' in bot20:
        ax.scatter(bot20['modelC'], 0, color=comp_color('modelC'), s=140,
                   marker='^', edgecolor='k', linewidth=1.2, zorder=10)
        ax.annotate('modelC', (bot20['modelC'], 0), xytext=(8, -14),
                    textcoords='offset points', fontsize=9)
    coef = np.polyfit(x, y, 1)
    xfit = np.linspace(0, max(0.5, max(bot20.values())), 50)
    ax.plot(xfit, np.polyval(coef, xfit), 'k--', lw=1, alpha=0.5,
            label=f'Linear fit (R = {R:+.3f})')

    ax.set_xlabel('Cl fraction in bottom 20% of SE slab (interface side)')
    ax.set_ylabel('Experimental adhesion W$_{ad}$ (mJ/m$^2$)')
    ax.set_title(f'F4 — Direct mechanism: Cl at interface vs adhesion\n'
                 f'R = {R:+.3f} (independent geometric descriptor)')
    ax.legend(loc='upper right', fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.savefig(OUT_DIR / "F4_cl_bot20.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "F4_cl_bot20.png", bbox_inches='tight')
    plt.close()
    log(f"  R(Cl bot20) = {R:+.4f}, saved F4")


# ======================================================================
# F5 — 7-method R(Cl-O) bar chart
# ======================================================================

def fig_F5_method_robustness():
    log("\n[F5] 7-method R(Cl-O) bar chart")
    methods = [
        ('v15 baseline\nNCM (104)', -0.9136),
        ('NCM (003)', -0.9141),
        ('NCM (110)', -0.9107),
        ('NCM (012)', -0.9121),
        ('Constrained\nrelax (M2)', -0.9131),
        ('2x2 supercell\n(M6)', -0.9131),
        ('Li shake ±0.2Å\n(mean 5 seeds)', -0.8863),
        ('1000 reg', -0.9142),
    ]
    fig, ax = plt.subplots(figsize=(8.5, 4))
    labels = [m[0] for m in methods]
    vals = [m[1] for m in methods]
    colors = ['#3366BB' if 'baseline' in m[0] else '#888888' for m in methods]
    bars = ax.bar(range(len(methods)), vals, color=colors, edgecolor='k', linewidth=0.8)
    ax.axhline(-0.9136, color='red', ls='--', lw=1, alpha=0.5, label='v15 baseline')
    ax.axhspan(-1.0, -0.7, color='green', alpha=0.1, label='|R| > 0.7 region')
    for i, (label, v) in enumerate(methods):
        ax.text(i, v - 0.03, f'{v:+.3f}', ha='center', fontsize=8)
    ax.set_xticks(range(len(methods)))
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel('R(Cl-O density vs paper Wad)')
    ax.set_ylim(-1.05, 0.0)
    ax.set_title('F5 — Method robustness: R(Cl-O) across 8 perturbations\n'
                 'all stay in [-0.914, -0.886]')
    ax.legend(loc='lower right', fontsize=8)
    ax.grid(axis='y', alpha=0.3)
    fig.savefig(OUT_DIR / "F5_method_robustness.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "F5_method_robustness.png", bbox_inches='tight')
    plt.close()
    log("  saved F5")


# ======================================================================
# F6 — Collinearity matrix heatmap
# ======================================================================

def fig_F6_collinearity():
    log("\n[F6] Collinearity matrix heatmap")
    # From v25 Y4 results
    descriptors = ['Cl-O dens', 'Li-O dens', 'Br-O dens', 'Li/fu',
                   'Cl/fu', 'Br/fu', 'vacancy', 'Cl+Br', 'paper_exp']
    mat = np.array([
        [+1.000, -0.843, -0.663, +0.994, -0.202, -0.745, -0.994, -0.994, -0.914],
        [-0.843, +1.000, +0.367, -0.785, +0.653, +0.290, +0.785, +0.785, +0.818],
        [-0.663, +0.367, +1.000, -0.667, -0.319, +0.775, +0.667, +0.667, +0.394],
        [+0.994, -0.785, -0.667, +1.000, -0.120, -0.799, -1.000, -1.000, -0.911],
        [-0.202, +0.653, -0.319, -0.120, +1.000, -0.500, +0.120, +0.120, +0.415],
        [-0.745, +0.290, +0.775, -0.799, -0.500, +1.000, +0.799, +0.799, +0.543],
        [-0.994, +0.785, +0.667, -1.000, +0.120, +0.799, +1.000, +1.000, +0.911],
        [-0.994, +0.785, +0.667, -1.000, +0.120, +0.799, +1.000, +1.000, +0.911],
        [-0.914, +0.818, +0.394, -0.911, +0.415, +0.543, +0.911, +0.911, +1.000],
    ])
    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(mat, cmap='RdBu_r', vmin=-1, vmax=1, aspect='equal')
    ax.set_xticks(range(len(descriptors)))
    ax.set_yticks(range(len(descriptors)))
    ax.set_xticklabels(descriptors, rotation=45, ha='right')
    ax.set_yticklabels(descriptors)
    for i in range(len(descriptors)):
        for j in range(len(descriptors)):
            ax.text(j, i, f'{mat[i,j]:+.2f}',
                    ha='center', va='center', fontsize=7,
                    color='white' if abs(mat[i,j]) > 0.6 else 'black')
    plt.colorbar(im, ax=ax, label='Pearson R')
    ax.set_title('F6 — Cross-correlation matrix\n'
                 '6 pairs |R|>0.95: descriptors collapse to 2 effective dims')
    fig.savefig(OUT_DIR / "F6_collinearity.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "F6_collinearity.png", bbox_inches='tight')
    plt.close()
    log("  saved F6")


# ======================================================================
# F7 — Bootstrap distribution histograms
# ======================================================================

def fig_F7_bootstrap():
    log("\n[F7] Bootstrap distribution histograms")
    # Re-run bootstrap on Cl-O, Li-O, Br-O, S-Li using equilibrium-gap densities
    densities = {}
    for c in ALL_COMPS:
        try:
            se = read(COMPS[c]['se']); ncm = read(COMPS[c]['ncm'])
            stacked, n_ncm = stack_rigid(se, ncm, COMPS[c]['gap_eq'])
            A = xy_area(stacked.cell.array)
            counts = count_interface_bonds(stacked, n_ncm)
            densities[c] = {k: v / A for k, v in counts.items()}
        except Exception as e:
            log(f"  {c} FAILED: {e}")

    paper = np.array([PAPER_EXP[c] for c in PAPER_COMPS], float)
    rng = np.random.default_rng(42)
    N_BOOT = 2000

    fig, axes = plt.subplots(2, 2, figsize=(9, 7))
    bonds = ['Li-O', 'Cl-O', 'Br-O', 'S-Li']
    for ax, bond in zip(axes.flat, bonds):
        x = np.array([densities[c].get(bond, 0) for c in PAPER_COMPS], float)
        if x.std() == 0:
            ax.text(0.5, 0.5, f"{bond}: zero variance", ha='center', transform=ax.transAxes)
            continue
        R_point = pearson(x, paper)
        Rs = []
        for _ in range(N_BOOT):
            idx = rng.integers(0, 5, 5)
            xb, yb = x[idx], paper[idx]
            if xb.std() == 0 or yb.std() == 0:
                continue
            Rs.append(pearson(xb, yb))
        Rs = np.array(Rs)
        ax.hist(Rs, bins=40, color='#5577AA', edgecolor='k', linewidth=0.5, alpha=0.85)
        ax.axvline(R_point, color='red', ls='--', lw=2, label=f'point R = {R_point:+.3f}')
        lo, hi = np.percentile(Rs, [2.5, 97.5])
        ax.axvspan(lo, hi, color='green', alpha=0.2, label=f'95% CI [{lo:+.2f}, {hi:+.2f}]')
        ax.set_xlabel('Pearson R')
        ax.set_ylabel('Count')
        ax.set_title(f'{bond}')
        ax.legend(loc='upper left', fontsize=8)
        ax.set_xlim(-1.05, 1.05)
        ax.grid(True, alpha=0.3)
    fig.suptitle(f'F7 — Bootstrap distribution of R (n=5, N_boot={N_BOOT})', y=1.0)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "F7_bootstrap.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "F7_bootstrap.png", bbox_inches='tight')
    plt.close()
    log("  saved F7")


# ======================================================================
# F8 — Phase 1 cross-validation
# ======================================================================

def fig_F8_phase1_crossval():
    log("\n[F8] Phase 1 cross-validation")
    try:
        adhesion = fetch_db("adhesion.json")
        p1 = adhesion['phase1_rigid_binding_2026_05_06']
    except Exception as e:
        log(f"  FAILED: {e}")
        return

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    for ax, mkey, mlabel in zip(axes,
                                 ['method_A_isolated_slab', 'method_B_self_reference'],
                                 ['Method A (isolated slab)',
                                  'Method B (self-reference)']):
        results = p1[mkey]['results']
        x = [results[c]['W_max_J_per_m2'] for c in PAPER_COMPS]
        y = [PAPER_EXP[c] for c in PAPER_COMPS]
        R = pearson(x, y)
        for c in PAPER_COMPS:
            ax.scatter(results[c]['W_max_J_per_m2'], PAPER_EXP[c],
                       color=comp_color(c), s=140, edgecolor='k', linewidth=1.2, zorder=10)
            ax.errorbar(results[c]['W_max_J_per_m2'], PAPER_EXP[c],
                        xerr=results[c]['W_max_std'], color=comp_color(c),
                        alpha=0.5, capsize=3, zorder=5)
            ax.annotate(c, (results[c]['W_max_J_per_m2'], PAPER_EXP[c]),
                        xytext=(8, 6), textcoords='offset points', fontsize=9)
        coef = np.polyfit(x, y, 1)
        xfit = np.linspace(min(x)-0.1, max(x)+0.1, 50)
        ax.plot(xfit, np.polyval(coef, xfit), 'k--', lw=1, alpha=0.5)
        ax.set_xlabel(r'Phase 1 W$_{max}$ (J/m$^2$)')
        ax.set_ylabel('Experimental W$_{ad}$ (mJ/m$^2$)')
        ax.set_title(f'{mlabel}\nR = {R:+.3f}')
        ax.grid(True, alpha=0.3)
    fig.suptitle('F8 — Phase 1 cross-validation (independent UMA energy method)', y=1.02)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "F8_phase1_crossval.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "F8_phase1_crossval.png", bbox_inches='tight')
    plt.close()
    log("  saved F8")


# ======================================================================
# F9 — Cij vs Wad multi-panel (paper #1 ↔ paper #2)
# ======================================================================

def fig_F9_cij_vs_adhesion():
    log("\n[F9] Cij vs adhesion multi-panel")
    try:
        elastic = fetch_db("elastic.json")
        sec = elastic.get('mlip_600K_snapshot', {}).get('results', [])
        by_comp = {}
        for row in sec:
            rid = row.get('id', '')
            if rid in ('comp1', 'comp2', 'comp3', 'comp4'):
                by_comp[rid] = row
            elif rid == 'comp5_B':
                by_comp['comp5'] = row
            elif rid == 'modelc':
                by_comp['modelC'] = row
    except Exception as e:
        log(f"  FAILED: {e}")
        return

    fields = [('C44', 'C$_{44}$ (GPa)'), ('G', 'G (GPa)'),
              ('E', 'E (GPa)'), ('K', 'K (GPa)')]
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.5))
    for ax, (f, label) in zip(axes, fields):
        x = [by_comp.get(c, {}).get(f) for c in PAPER_COMPS]
        if any(v is None for v in x):
            ax.text(0.5, 0.5, f"{f}: missing data", ha='center', transform=ax.transAxes)
            continue
        y = [PAPER_EXP[c] for c in PAPER_COMPS]
        R = pearson(x, y)
        for c in PAPER_COMPS:
            ax.scatter(by_comp[c][f], PAPER_EXP[c], color=comp_color(c),
                       s=110, edgecolor='k', linewidth=1.0, zorder=10)
            ax.annotate(c, (by_comp[c][f], PAPER_EXP[c]),
                        xytext=(7, 5), textcoords='offset points', fontsize=8)
        coef = np.polyfit(x, y, 1)
        xfit = np.linspace(min(x)-1, max(x)+1, 50)
        ax.plot(xfit, np.polyval(coef, xfit), 'k--', lw=1, alpha=0.5)
        ax.set_xlabel(label)
        ax.set_ylabel('Wad (mJ/m$^2$)')
        ax.set_title(f'R = {R:+.3f}')
        ax.grid(True, alpha=0.3)
    fig.suptitle('F9 — Mechanical Cij (paper #1) vs adhesion Wad (paper #2): '
                 'all same direction', y=1.02)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "F9_cij_vs_adhesion.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "F9_cij_vs_adhesion.png", bbox_inches='tight')
    plt.close()
    log("  saved F9")


# ======================================================================
# F10 — Halogen z-distribution histograms
# ======================================================================

def fig_F10_halogen_z_hist():
    log("\n[F10] Halogen z-distribution histograms")
    fig, axes = plt.subplots(2, 3, figsize=(11, 7))
    for ax, c in zip(axes.flat, ALL_COMPS):
        try:
            se = read(COMPS[c]['se'])
            z = se.positions[:, 2]
            z_norm = (z - z.min()) / (z.max() - z.min())
            syms = se.get_chemical_symbols()
            for X, color, label in [('Cl', '#22CC22', 'Cl'), ('Br', '#AA0000', 'Br')]:
                idxs = [i for i, s in enumerate(syms) if s == X]
                if not idxs:
                    continue
                zs = z_norm[idxs]
                ax.hist(zs, bins=np.linspace(0, 1, 21), color=color,
                        alpha=0.7, edgecolor='k', linewidth=0.5,
                        label=f'{X} (n={len(zs)})')
            ax.axvspan(0, 0.2, color='gray', alpha=0.2, label='bottom 20%')
            ax.axvspan(0.8, 1.0, color='lightblue', alpha=0.2, label='top 20%')
            ax.set_title(f"{c} (family {COMPS[c]['family']})")
            ax.set_xlabel('z (normalized)')
            ax.set_ylabel('count')
            ax.legend(loc='upper right', fontsize=7)
            ax.set_xlim(0, 1)
        except Exception as e:
            log(f"  {c} FAILED: {e}")
    fig.suptitle('F10 — Halogen z-distribution per comp (Li5.4 + Cl/Br mix → Cl out of bottom 20%)',
                 y=1.0)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "F10_halogen_z_hist.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "F10_halogen_z_hist.png", bbox_inches='tight')
    plt.close()
    log("  saved F10")


# ======================================================================
# F11 — NCM facet variation R(Cl-O) bar chart
# ======================================================================

def fig_F11_ncm_facet():
    log("\n[F11] NCM facet variation")
    facets = [('(104)\nbaseline', -0.9136),
              ('(003)', -0.9141),
              ('(110)', -0.9107),
              ('(012)', -0.9121),
              ('5L (104)', -0.9131)]
    fig, ax = plt.subplots(figsize=(6, 3.5))
    labels = [f[0] for f in facets]
    vals = [f[1] for f in facets]
    bars = ax.bar(range(len(facets)), vals, color='#3366BB',
                   edgecolor='k', linewidth=0.8)
    bars[0].set_color('#CC4444')
    for i, (lbl, v) in enumerate(facets):
        ax.text(i, v - 0.03, f'{v:+.3f}', ha='center', fontsize=9)
    ax.set_xticks(range(len(facets)))
    ax.set_xticklabels(labels)
    ax.set_ylabel('R(Cl-O vs paper Wad)')
    ax.set_ylim(-1.0, 0.0)
    ax.axhline(-0.9136, color='red', ls='--', lw=1, alpha=0.5)
    ax.set_title('F11 — Cl-O R is NCM-facet-independent (and depth-converged)')
    ax.grid(axis='y', alpha=0.3)
    fig.savefig(OUT_DIR / "F11_ncm_facet.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "F11_ncm_facet.png", bbox_inches='tight')
    plt.close()
    log("  saved F11")


# ======================================================================
# F12 — 1000 reg CV per comp
# ======================================================================

def fig_F12_1000reg_cv():
    log("\n[F12] 1000 reg CV per comp")
    cv_data = {
        'comp1': {'Li-O': 4.3, 'Cl-O': 11.5, 'Br-O': 0.0},
        'comp2': {'Li-O': 5.7, 'Cl-O': 10.9, 'Br-O': 0.0},
        'comp3': {'Li-O': 3.1, 'Cl-O': 0.0, 'Br-O': 0.0},
        'comp4': {'Li-O': 6.3, 'Cl-O': 0.0, 'Br-O': 3.8},
        'comp5': {'Li-O': 5.6, 'Cl-O': 0.0, 'Br-O': 3.7},
        'modelC': {'Li-O': 10.6, 'Cl-O': 7.9, 'Br-O': 0.0},
    }
    bonds = ['Li-O', 'Cl-O', 'Br-O']
    bond_colors = ['#5577AA', '#22CC22', '#AA0000']
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.arange(len(ALL_COMPS))
    width = 0.27
    for i, (bond, color) in enumerate(zip(bonds, bond_colors)):
        vals = [cv_data[c][bond] for c in ALL_COMPS]
        ax.bar(x + (i-1)*width, vals, width, label=bond, color=color,
                edgecolor='k', linewidth=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(ALL_COMPS)
    ax.set_ylabel('Coefficient of Variation (%)')
    ax.set_title('F12 — Registry sampling CV (1000 random xy-shifts)\n'
                 'Cl-O CV 0% for comp3-5 (no contacts at any registry)')
    ax.legend(fontsize=9)
    ax.grid(axis='y', alpha=0.3)
    ax.axhline(15, color='red', ls=':', lw=1, alpha=0.5, label='15% threshold')
    fig.savefig(OUT_DIR / "F12_1000reg_cv.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "F12_1000reg_cv.png", bbox_inches='tight')
    plt.close()
    log("  saved F12")


# ======================================================================
# F13 — UMA vs MACE Wad scatter (key MLIP-dependence figure)
# ======================================================================

def fig_F13_uma_vs_mace():
    log("\n[F13] UMA vs MACE Wad comparison")
    # MACE Wad from v26c
    wad_mace = {'comp1': -23.8520, 'comp2': -24.8346, 'comp3': +3.7469,
                'comp4': -6.3623, 'comp5': -6.5192, 'modelC': +0.7016}
    # UMA Wad from earlier rigid (v12-style)
    # use Phase 1 Method A as UMA representative (R=+0.87, but different scale)
    try:
        adhesion = fetch_db("adhesion.json")
        p1 = adhesion['phase1_rigid_binding_2026_05_06']
        wad_uma = {c: p1['method_A_isolated_slab']['results'][c]['W_max_J_per_m2']
                   for c in PAPER_COMPS}
    except Exception as e:
        log(f"  UMA fetch failed: {e}")
        return

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    # (a) MACE Wad vs paper
    ax = axes[0]
    x = [wad_mace[c] for c in PAPER_COMPS]; y = [PAPER_EXP[c] for c in PAPER_COMPS]
    R = pearson(x, y)
    for c in PAPER_COMPS:
        ax.scatter(wad_mace[c], PAPER_EXP[c], color=comp_color(c), s=140,
                   edgecolor='k', linewidth=1.2, zorder=10)
        ax.annotate(c, (wad_mace[c], PAPER_EXP[c]), xytext=(8, 6),
                    textcoords='offset points', fontsize=9)
    if 'modelC' in wad_mace:
        ax.scatter(wad_mace['modelC'], 0, color=comp_color('modelC'), s=140,
                   marker='^', edgecolor='k', linewidth=1.2)
        ax.annotate('modelC', (wad_mace['modelC'], 0), xytext=(8, -14),
                    textcoords='offset points', fontsize=9)
    coef = np.polyfit(x, y, 1)
    xfit = np.linspace(min(x)-2, max(x)+2, 50)
    ax.plot(xfit, np.polyval(coef, xfit), 'k--', lw=1, alpha=0.5)
    ax.set_xlabel(r'MACE Wad (J/m$^2$)')
    ax.set_ylabel('Experimental Wad (mJ/m$^2$)')
    ax.set_title(f'(a) MACE-MP-0\nR = {R:+.3f} ⭐')
    ax.grid(True, alpha=0.3)

    # (b) UMA Phase 1 Method A
    ax = axes[1]
    x = [wad_uma[c] for c in PAPER_COMPS]; y = [PAPER_EXP[c] for c in PAPER_COMPS]
    R_uma = pearson(x, y)
    for c in PAPER_COMPS:
        ax.scatter(wad_uma[c], PAPER_EXP[c], color=comp_color(c), s=140,
                   edgecolor='k', linewidth=1.2, zorder=10)
        ax.annotate(c, (wad_uma[c], PAPER_EXP[c]), xytext=(8, 6),
                    textcoords='offset points', fontsize=9)
    coef = np.polyfit(x, y, 1)
    xfit = np.linspace(min(x)-0.1, max(x)+0.1, 50)
    ax.plot(xfit, np.polyval(coef, xfit), 'k--', lw=1, alpha=0.5)
    ax.set_xlabel(r'UMA Phase 1 W$_{max}$ (J/m$^2$)')
    ax.set_ylabel('Experimental Wad (mJ/m$^2$)')
    ax.set_title(f'(b) UMA Phase 1\nR = {R_uma:+.3f}')
    ax.grid(True, alpha=0.3)

    fig.suptitle('F13 — Energy descriptor is MLIP-dependent: '
                 'MACE recovers correct ranking, UMA inverted in v9-v22 (rigid Wad)', y=1.02)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "F13_uma_vs_mace.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "F13_uma_vs_mace.png", bbox_inches='tight')
    plt.close()
    log(f"  R(MACE) = {R:+.3f}, R(UMA Phase1 A) = {R_uma:+.3f}, saved F13")


# ======================================================================
# Master summary panel
# ======================================================================

def fig_master_summary(f1_data, cl_o):
    log("\n[F0] Master summary 4-panel")
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))

    # (a) binding curve summary (Cl-O only)
    ax = axes[0, 0]
    for c in ALL_COMPS:
        if c not in f1_data: continue
        d = f1_data[c]
        ls = '-' if c != 'modelC' else '--'
        ax.plot(d['gap'], d['Cl-O'], color=comp_color(c), label=c, lw=1.5, ls=ls)
        g_eq = COMPS[c]['gap_eq']
        i_eq = np.argmin(np.abs(np.array(d['gap']) - g_eq))
        ax.scatter([d['gap'][i_eq]], [d['Cl-O'][i_eq]],
                   color=comp_color(c), s=40, zorder=5, edgecolor='k', linewidth=0.5)
    ax.set_xlabel('Interface gap (Å)'); ax.set_ylabel('Cl-O density (Å$^{-2}$)')
    ax.set_title('(a) Binding curve'); ax.grid(True, alpha=0.3)
    ax.legend(fontsize=7, loc='upper right')

    # (b) main scatter
    ax = axes[0, 1]
    x = [cl_o[c] for c in PAPER_COMPS]; y = [PAPER_EXP[c] for c in PAPER_COMPS]
    R = pearson(x, y)
    for c in PAPER_COMPS:
        ax.scatter(cl_o[c], PAPER_EXP[c], color=comp_color(c), s=100,
                   edgecolor='k', linewidth=1.0, zorder=10)
    if 'modelC' in cl_o:
        ax.scatter(cl_o['modelC'], 0, color=comp_color('modelC'), s=100,
                   marker='^', edgecolor='k', linewidth=1.0)
    coef = np.polyfit(x, y, 1)
    xfit = np.linspace(min(x)-0.005, max(cl_o.values())+0.01, 50)
    ax.plot(xfit, np.polyval(coef, xfit), 'k--', lw=1, alpha=0.5)
    ax.set_xlabel('Cl-O density (Å$^{-2}$)'); ax.set_ylabel('Wad (mJ/m$^2$)')
    ax.set_title(f'(b) Main result: R = {R:+.3f}'); ax.grid(True, alpha=0.3)

    # (c) method robustness (mini bar)
    ax = axes[1, 0]
    methods = ['v15', '(003)', '(110)', '(012)', 'M2', '2x2', 'shake', '1000reg']
    vals = [-0.9136, -0.9141, -0.9107, -0.9121, -0.9131, -0.9131, -0.8863, -0.9142]
    ax.bar(range(len(methods)), vals, color='#3366BB', edgecolor='k', linewidth=0.5)
    ax.set_xticks(range(len(methods)))
    ax.set_xticklabels(methods, rotation=30, fontsize=8)
    ax.set_ylim(-1.0, 0.0)
    ax.axhline(-0.9136, color='red', ls='--', lw=1, alpha=0.5)
    ax.set_ylabel('R(Cl-O)')
    ax.set_title('(c) Method robustness (8 perturbations)')
    ax.grid(axis='y', alpha=0.3)

    # (d) Cl bot20 mechanism
    ax = axes[1, 1]
    bot20 = {}
    for c in ALL_COMPS:
        try:
            se = read(COMPS[c]['se']); z = se.positions[:, 2]
            zn = (z - z.min())/(z.max() - z.min())
            syms = se.get_chemical_symbols()
            cl = [i for i, s in enumerate(syms) if s == 'Cl']
            if cl:
                bot20[c] = float(np.mean(zn[cl] < 0.2))
        except Exception:
            pass
    x = [bot20.get(c, 0) for c in PAPER_COMPS]; y = [PAPER_EXP[c] for c in PAPER_COMPS]
    R = pearson(x, y)
    for c in PAPER_COMPS:
        ax.scatter(bot20.get(c, 0), PAPER_EXP[c], color=comp_color(c), s=100,
                   edgecolor='k', linewidth=1.0)
    if 'modelC' in bot20:
        ax.scatter(bot20['modelC'], 0, color=comp_color('modelC'), s=100,
                   marker='^', edgecolor='k', linewidth=1.0)
    ax.set_xlabel('Cl in bottom 20% (interface)')
    ax.set_ylabel('Wad (mJ/m$^2$)')
    ax.set_title(f'(d) Mechanism: Cl@interface, R = {R:+.3f}')
    ax.grid(True, alpha=0.3)

    fig.suptitle('Paper #2 master summary — Cl-O contact density at SE/NCM interface',
                 fontsize=13, y=1.01)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "F0_master_summary.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "F0_master_summary.png", bbox_inches='tight')
    plt.close()
    log("  saved F0 master summary")


# ======================================================================
# Main
# ======================================================================

def main():
    t0 = time.time()
    log("=" * 70)
    log("v28 — paper #2 figure assembly (12 figures + 1 master)")
    log("=" * 70)

    f1_data = fig_F1_binding_curve()
    cl_o = fig_F3_clo_scatter(f1_data)
    fig_F2_xyz_snapshot()
    fig_F4_cl_bot20()
    fig_F5_method_robustness()
    fig_F6_collinearity()
    fig_F7_bootstrap()
    fig_F8_phase1_crossval()
    fig_F9_cij_vs_adhesion()
    fig_F10_halogen_z_hist()
    fig_F11_ncm_facet()
    fig_F12_1000reg_cv()
    fig_F13_uma_vs_mace()
    fig_master_summary(f1_data, cl_o)

    log(f"\n=== v28 DONE: {(time.time()-t0)/60:.1f} min ===")
    log(f"Outputs in: {OUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
