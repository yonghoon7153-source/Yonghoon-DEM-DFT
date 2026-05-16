"""Bond length distribution across 5z×36xy ensemble for each comp.

For each (comp, z-shift, xy-shift) at fixed gap=1.4 A:
  - rigid stack SE on top of NCM
  - find ALL cross-interface atom pairs (SE side + NCM side)
  - extract bond lengths within cutoff per bond type
  - aggregate 180 configs into 1D array per (comp, bond_type)
  - plot histograms + report mean/std/quartiles

Cutoffs (per kb/papers/STRUCTURE_PATHS.md and refs):
  Li-O 2.8 Å (Li-O ionic, attractive)
  Li-S 3.0 Å
  Li-Cl 3.2 Å (Li 0.76 + Cl 1.81 = 2.57; cutoff at 3.2)
  Li-Br 3.4 Å (Li 0.76 + Br 1.96 = 2.72)
  Cl-O 3.4 Å (anion-anion repulsion proxy)
  Br-O 3.6 Å

Cross-interface = one atom from SE, other from NCM (z-distance > ~1 A apart).

Usage:
  python bond_length_ensemble.py [--comps comp1,comp2,...]
                                 [--gap 1.4]
                                 [--out_dir bond_length_ensemble]

Output:
  bond_length_ensemble/
    {comp}_{bond_type}.npy        raw bond lengths (1D array)
    bond_length_summary.csv       per-(comp,bond_type) stats
    bond_length_histograms.png    overlay histograms
    bond_length_violin.png        per-comp violin plots
"""
import sys, os, json, time
from pathlib import Path
from itertools import product
import argparse
import numpy as np
from ase.io import read
from ase.neighborlist import neighbor_list

CUTOFFS = {
    ('Li','O'):  2.8,
    ('Li','S'):  3.0,
    ('Li','Cl'): 3.2,
    ('Li','Br'): 3.4,
    ('Cl','O'):  3.4,
    ('Br','O'):  3.6,
}
# Maximum cutoff for ase neighbor_list (use largest)
MAX_CUTOFF = max(CUTOFFS.values())

COMPS = {
    'comp1':  {'src': 'comp1_slab_v2.xyz',                  'ncm': 'ncm_7x7x1_3Lconv.xyz'},
    'comp2':  {'src': 'comp2_slab_v2.xyz',                  'ncm': 'ncm_7x7x1_3Lconv.xyz'},
    'comp3':  {'src': 'comp3_slab_v1_PRESERVED.xyz',        'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'comp4':  {'src': 'comp4_slab_v2_PRESERVED.xyz',        'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'comp5':  {'src': 'comp5_slab_v1_PRESERVED.xyz',        'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'modelC': {'src': 'modelC_slab_v2_PRESERVED.xyz',       'ncm': 'ncm_5x5x1_3Lconv.xyz'},
}

VACUUM_TOP = 30.0
N_ZSHIFTS = 5
N_XY_GRID = 6


def zshift_variant(atoms, frac):
    a = atoms.copy()
    cz = a.cell.lengths()[2]
    pos = a.positions.copy()
    pos[:, 2] = (pos[:, 2] + frac * cz) % cz
    a.set_positions(pos)
    return a


def stack_rigid(se, ncm, gap, shift_frac=(0.0, 0.0)):
    """Same as ensemble script. Returns combined Atoms + index where NCM ends, SE begins."""
    se_a = se.copy(); ncm_a = ncm.copy()
    nc = se_a.cell.array.copy()
    nc[0] = ncm_a.cell.array[0]; nc[1] = ncm_a.cell.array[1]
    se_a.set_cell(nc, scale_atoms=True)
    dx, dy = shift_frac
    sc = dx * ncm_a.cell.array[0] + dy * ncm_a.cell.array[1]
    se_a.translate([sc[0], sc[1], 0.0])
    se_a.wrap()
    ncm_a.translate([0, 0, -ncm_a.positions[:, 2].min()])
    z_max_ncm = ncm_a.positions[:, 2].max()
    s_min = se_a.positions[:, 2].min()
    se_a.translate([0, 0, z_max_ncm - s_min + gap])
    n_ncm = len(ncm_a)
    combined = ncm_a + se_a
    new_cell = ncm_a.cell.array.copy()
    z_extent = combined.positions[:, 2].max() - combined.positions[:, 2].min()
    new_cell[2] = [0., 0., z_extent + VACUUM_TOP]
    combined.set_cell(new_cell, scale_atoms=False)
    combined.set_pbc([True, True, True])
    return combined, n_ncm


def get_cross_interface_bonds(atoms, n_ncm):
    """For each bond type, return list of bond lengths where one atom is in SE
    (idx >= n_ncm) and other in NCM (idx < n_ncm). Within cutoff."""
    i, j, d = neighbor_list('ijd', atoms, cutoff=MAX_CUTOFF)
    syms = atoms.get_chemical_symbols()
    bonds = {k: [] for k in CUTOFFS}
    for k in range(len(i)):
        ia, ja = i[k], j[k]
        if ia >= ja:
            continue   # avoid double count
        # cross-interface: one in NCM (< n_ncm), one in SE (>= n_ncm)
        is_cross = (ia < n_ncm) ^ (ja < n_ncm)
        if not is_cross:
            continue
        a, b = sorted([syms[ia], syms[ja]])
        pair = (a, b)
        # Try both orderings (Li,O) and (O,Li)
        if pair in CUTOFFS and d[k] <= CUTOFFS[pair]:
            bonds[pair].append(d[k])
        elif (b, a) in CUTOFFS and d[k] <= CUTOFFS[(b,a)]:
            bonds[(b, a)].append(d[k])
    return bonds


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--comps', default='comp1,comp2,comp3,comp4,comp5,modelC',
                   help='comma-sep list of comps to process')
    p.add_argument('--gap', type=float, default=1.4,
                   help='fixed interface gap (Å, default 1.4 = paper standard)')
    p.add_argument('--out_dir', default='bond_length_ensemble')
    args = p.parse_args()

    OUT = Path(args.out_dir); OUT.mkdir(exist_ok=True)
    comps = [c.strip() for c in args.comps.split(',')]

    xy_shifts = [(i/N_XY_GRID, j/N_XY_GRID)
                 for i in range(N_XY_GRID) for j in range(N_XY_GRID)]

    print(f"Bond length ensemble — {len(comps)} comps × {N_ZSHIFTS} z × {len(xy_shifts)} xy")
    print(f"Cutoffs: {CUTOFFS}")
    print(f"Gap: {args.gap} Å")

    all_data = {}   # comp → bond_pair → list of lengths
    t0 = time.time()

    for c in comps:
        if c not in COMPS:
            print(f"[skip] unknown comp: {c}"); continue
        cfg = COMPS[c]
        if not Path(cfg['src']).exists() or not Path(cfg['ncm']).exists():
            print(f"[skip] {c}: missing slab/ncm file"); continue

        se_base = read(cfg['src'])
        ncm = read(cfg['ncm'])
        comp_bonds = {pair: [] for pair in CUTOFFS}

        for iz in range(N_ZSHIFTS):
            se_z = zshift_variant(se_base, iz / N_ZSHIFTS)
            for ixy, (dx, dy) in enumerate(xy_shifts):
                stacked, n_ncm = stack_rigid(se_z, ncm, args.gap, shift_frac=(dx, dy))
                bonds = get_cross_interface_bonds(stacked, n_ncm)
                for pair, lengths in bonds.items():
                    comp_bonds[pair].extend(lengths)
        all_data[c] = comp_bonds
        print(f"  [{c}] done: " + " ".join(
            f"{a}-{b}={len(v):4d}" for (a,b), v in comp_bonds.items()))

        # Save raw arrays
        for (a,b), v in comp_bonds.items():
            np.save(OUT / f"{c}_{a}{b}.npy", np.array(v))

    print(f"\nTotal time: {time.time()-t0:.1f} s\n")

    # === Summary CSV ===
    csv_path = OUT / "bond_length_summary.csv"
    with open(csv_path, 'w') as f:
        f.write("comp,bond,n,mean_A,std_A,median_A,p25_A,p75_A,min_A,max_A\n")
        print(f"{'comp':<8} {'bond':<6} {'n':>4} {'mean':>6} {'std':>5} "
              f"{'median':>6} {'p25':>6} {'p75':>6} {'min':>5} {'max':>5}")
        for c in comps:
            if c not in all_data: continue
            for pair, lengths in all_data[c].items():
                arr = np.array(lengths)
                if len(arr) == 0:
                    line = f"{c},{pair[0]}-{pair[1]},0,,,,,,,\n"
                    print(f"{c:<8} {pair[0]}-{pair[1]:<4} {0:>4d}  (no bonds)")
                else:
                    s = (np.mean(arr), np.std(arr), np.median(arr),
                         np.percentile(arr, 25), np.percentile(arr, 75),
                         arr.min(), arr.max())
                    line = f"{c},{pair[0]}-{pair[1]},{len(arr)}," + ",".join(f"{x:.4f}" for x in s) + "\n"
                    print(f"{c:<8} {pair[0]}-{pair[1]:<4} {len(arr):>4d} "
                          f"{s[0]:>6.3f} {s[1]:>5.3f} {s[2]:>6.3f} "
                          f"{s[3]:>6.3f} {s[4]:>6.3f} {s[5]:>5.3f} {s[6]:>5.3f}")
                f.write(line)
    print(f"\nsaved {csv_path}")

    # === Histograms (subplot per bond type, overlay comps) ===
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    COLORS = {'comp1': '#1f77b4', 'comp2': '#17becf',
              'comp3': '#d62728', 'comp4': '#9467bd',
              'comp5': '#2ca02c', 'modelC': '#ff7f0e'}
    plt.rcParams.update({'font.size': 11})
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    pairs_list = list(CUTOFFS.keys())
    for ax, pair in zip(axes.flatten(), pairs_list):
        for c in comps:
            if c not in all_data: continue
            arr = np.array(all_data[c][pair])
            if len(arr) == 0: continue
            ax.hist(arr, bins=30, alpha=0.5, color=COLORS.get(c, 'gray'),
                    label=f"{c} (n={len(arr)})", density=True)
        ax.set_xlabel(f'{pair[0]}-{pair[1]} bond length (Å)')
        ax.set_ylabel('Density')
        ax.set_title(f'{pair[0]}-{pair[1]}  (cutoff {CUTOFFS[pair]} Å)')
        ax.axvline(CUTOFFS[pair], color='k', ls=':', alpha=0.4)
        ax.legend(fontsize=8)
        ax.grid(alpha=0.25)
    fig.suptitle(f'Bond length distributions — ensemble 5z × 36xy at gap={args.gap} Å', y=1.01)
    fig.tight_layout()
    fig.savefig(OUT / "bond_length_histograms.png", dpi=200, bbox_inches='tight')
    fig.savefig(OUT / "bond_length_histograms.pdf", bbox_inches='tight')
    plt.close()
    print(f"saved {OUT / 'bond_length_histograms.png'}")

    # === Violin plot (comps × bond type) ===
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    for ax, pair in zip(axes.flatten(), pairs_list):
        data = []; labels = []
        for c in comps:
            if c not in all_data: continue
            arr = np.array(all_data[c][pair])
            if len(arr) == 0: continue
            data.append(arr); labels.append(c)
        if data:
            vp = ax.violinplot(data, showmedians=True, showextrema=True)
            ax.set_xticks(range(1, len(labels)+1))
            ax.set_xticklabels(labels, rotation=30, ha='right')
        ax.set_ylabel(f'{pair[0]}-{pair[1]} bond length (Å)')
        ax.set_title(f'{pair[0]}-{pair[1]}')
        ax.axhline(CUTOFFS[pair], color='k', ls=':', alpha=0.4, label=f'cutoff {CUTOFFS[pair]}')
        ax.grid(alpha=0.25)
    fig.suptitle(f'Bond length distributions (violin) — gap={args.gap} Å', y=1.01)
    fig.tight_layout()
    fig.savefig(OUT / "bond_length_violin.png", dpi=200, bbox_inches='tight')
    plt.close()
    print(f"saved {OUT / 'bond_length_violin.png'}")


if __name__ == "__main__":
    main()
