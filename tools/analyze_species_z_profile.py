"""analyze_species_z_profile.py -- z-axis composition profile per slab/stack.

For each composition (anneal champion, NO migration assumed):
  For each species (Li, P, S, Cl, Br, O, Ni, ...):
    histogram its z position
    -> "Who sits where in the z direction?"

Two modes:
  1) SE slab only:   tools/analyze_species_z_profile.py slab
  2) Stacked SE+NCM: tools/analyze_species_z_profile.py stacked

Each comp on its own subplot; species color-coded; interface region
highlighted (in stacked mode).

Output:
  species_z_profile_{slab|stacked}.png/pdf
  species_z_profile_{slab|stacked}.json

Usage on gabia:
  cd /data/work/v30u_ensemble
  wget -O analyze_species_z_profile.py \
    "https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/claude/debug-api-500-error-iukkt/tools/analyze_species_z_profile.py?$(date +%s)"
  python3 analyze_species_z_profile.py slab
  python3 analyze_species_z_profile.py stacked
"""
import json
import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ase.io import read

WORK = Path('/data/work/v30u_ensemble')

SLAB_FILES = {
    'comp1':    'comp1_slab_v2.xyz',
    'comp2':    'comp2_slab_v2.xyz',
    'comp4_v1': 'comp4_slab_v1_PRESERVED.xyz',
    'comp4_v2': 'comp4_slab_v2_PRESERVED.xyz',
    'comp5':    'comp5_slab_v1_PRESERVED.xyz',
    'modelC':   'modelC_slab_v2_PRESERVED.xyz',
}

STACK_FILES = {
    'comp1':    'comp1_R1_origin_d1.2_orthogonal.xyz',
    'comp2':    'comp2_R1_origin_d1.2_orthogonal.xyz',
    'comp4_v2': 'comp4_v2_R1_origin_d1.4_orthogonal.xyz',
}

SPECIES_COLOR = {
    'Li': '#9971D9',  # purple
    'P':  '#A8A8A8',  # gray
    'S':  '#FCC830',  # yellow
    'Cl': '#1FE61F',  # green
    'Br': '#A52A2A',  # wine
    'O':  '#FF1C00',  # red (NCM)
    'Ni': '#5078D2',  # blue (NCM)
    'Co': '#3E66BB',
    'Mn': '#9C2DAB',
}

# Atomic radius for "where on z-axis" markers
ATOMIC_R = {
    'Li': 0.70, 'P': 0.95, 'S': 1.00, 'Cl': 0.95, 'Br': 1.10,
    'O': 0.55, 'Ni': 0.80, 'Co': 0.80, 'Mn': 0.80,
}


def analyze_one(atoms):
    """Return {species: z_array} dict."""
    syms = np.array(atoms.get_chemical_symbols())
    z = atoms.positions[:, 2]
    out = {}
    for sp in np.unique(syms):
        out[sp] = z[syms == sp]
    return out


def detect_interface_z(atoms, ncm_species=('Ni', 'Co', 'Mn')):
    """If NCM transition metals present, return top-of-NCM z (interface)."""
    syms = np.array(atoms.get_chemical_symbols())
    z = atoms.positions[:, 2]
    ncm_mask = np.isin(syms, list(ncm_species))
    if ncm_mask.sum() == 0:
        return None
    return float(z[ncm_mask].max())


def plot_profile(per_comp, files, title_suffix, out_stem):
    n = len(per_comp)
    fig, axes = plt.subplots(n, 1, figsize=(12, 2.2 * n), sharex=False)
    if n == 1:
        axes = [axes]

    for ax, (cname, data) in zip(axes, per_comp.items()):
        atoms_z = data['z_per_species']
        n_atoms = data['n_atoms']
        z_iface = data.get('z_iface')
        z_min = data['z_min']
        z_max = data['z_max']

        # combined histogram
        sp_order = ['Ni', 'Co', 'Mn', 'O', 'Li', 'P', 'S', 'Cl', 'Br']
        for sp in sp_order:
            if sp not in atoms_z:
                continue
            zs = atoms_z[sp]
            if len(zs) == 0:
                continue
            ax.hist(zs, bins=40, range=(z_min - 0.5, z_max + 0.5),
                    color=SPECIES_COLOR.get(sp, '#888'),
                    alpha=0.75, edgecolor='k', lw=0.3,
                    label=f"{sp} (n={len(zs)})")

        if z_iface is not None:
            ax.axvline(z_iface, color='red', ls='--', lw=1.3, alpha=0.85,
                       label='NCM top (interface)')

        ax.set_title(f"{cname}  ({files[cname]}, total {n_atoms} atoms)", fontsize=10)
        ax.set_xlabel("z (Å)")
        ax.set_ylabel("count")
        ax.legend(loc='upper right', fontsize=7, framealpha=0.92, ncol=3)
        ax.grid(alpha=0.25)

    fig.suptitle(f"Species z-profile per composition ({title_suffix})  —  champion structures",
                 fontsize=13)
    fig.tight_layout()
    fig.savefig(WORK / f"{out_stem}.png", dpi=150, bbox_inches='tight')
    fig.savefig(WORK / f"{out_stem}.pdf", bbox_inches='tight')
    print(f"Saved: {out_stem}.png/.pdf")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'slab'
    files = SLAB_FILES if mode == 'slab' else STACK_FILES
    out_stem = f"species_z_profile_{mode}"

    per_comp = {}
    print("=" * 90)
    print(f"Mode: {mode}    (champion structures, no migration assumed)")
    print("=" * 90)
    for cname, fn in files.items():
        path = WORK / fn
        if not path.exists():
            print(f"  [{cname}] SKIP — file missing: {fn}")
            continue
        atoms = read(path)
        z = atoms.positions[:, 2]
        z_per_species = analyze_one(atoms)
        z_iface = detect_interface_z(atoms)

        per_comp[cname] = {
            'n_atoms':         len(atoms),
            'z_min':           float(z.min()),
            'z_max':           float(z.max()),
            'z_per_species':   {k: v.tolist() for k, v in z_per_species.items()},
            'z_iface':         z_iface,
        }

        print(f"\n{cname}  ({fn})")
        print(f"  z range: {z.min():.2f} .. {z.max():.2f} Å, total {len(atoms)} atoms")
        if z_iface is not None:
            print(f"  NCM top (interface): z = {z_iface:.2f} Å")
        for sp in sorted(z_per_species.keys()):
            zs = z_per_species[sp]
            if len(zs) == 0: continue
            label = ""
            if z_iface is not None:
                # how many are above NCM (= in SE region)
                n_above = int((zs > z_iface).sum())
                n_below = len(zs) - n_above
                # interface-near = within 3 Å of z_iface
                near = ((zs > z_iface - 0.5) & (zs < z_iface + 3.0)).sum()
                label = f"  | above NCM: {n_above:>3d}  near interface (<3A above): {int(near):>3d}"
            print(f"    {sp:<3} n={len(zs):>3d}  <z>={zs.mean():.2f}  z range=[{zs.min():.2f}, {zs.max():.2f}]{label}")

    # save JSON
    json.dump(per_comp, open(WORK / f"{out_stem}.json", 'w'), indent=2)

    # plot
    plot_profile(per_comp, files, mode, out_stem)


if __name__ == "__main__":
    main()
