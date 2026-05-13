"""analyze_halogen_slab_positions.py — quantify halogen positions in SE slabs.

For each SE slab (comp1, comp2, comp4_v1, comp4_v2, modelC):
  • z-distribution of each halogen (Cl, Br)
  • Distance to top face (= NCM-facing surface in stack)
  • Distance to bottom face
  • Nearest Li distance per halogen (≈ Li-X d_eq)
  • Nearest S distance per halogen
  • "Interface-facing halogen" count: those within 3 Å of either face

Output:
  • Per-comp summary table (n_halogen total, n at top, n at bottom, mean z, ...)
  • Comparison comp4_v1 vs comp4_v2 (Δ mean_z per element, Δ n_at_top)
  • Histograms in halogen_slab_positions.png

Usage on gabia:
  cd /data/work/v30u_ensemble
  wget -O analyze_halogen_slab_positions.py "https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/claude/debug-api-500-error-iukkt/tools/analyze_halogen_slab_positions.py?$(date +%s)"
  python3 analyze_halogen_slab_positions.py
"""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ase.io import read

WORK = Path('/data/work/v30u_ensemble')

SLABS = {
    'comp1':    'comp1_slab_v2.xyz',
    'comp2':    'comp2_slab_v2.xyz',
    'comp4_v1': 'comp4_slab_v1_PRESERVED.xyz',
    'comp4_v2': 'comp4_slab_v2_PRESERVED.xyz',
    'comp5':    'comp5_slab_v1_PRESERVED.xyz',
    'modelC':   'modelC_slab_v2_PRESERVED.xyz',
}

NEAR_FACE = 3.0   # Å within face -> "interface-facing"


def analyze(atoms):
    syms = np.array(atoms.get_chemical_symbols())
    pos = atoms.positions
    z = pos[:, 2]
    z_min, z_max = z.min(), z.max()
    thickness = z_max - z_min

    Li_idx = np.where(syms == 'Li')[0]
    S_idx = np.where(syms == 'S')[0]
    Li_pos = pos[Li_idx]
    S_pos = pos[S_idx]

    info = {
        'n_atoms': len(atoms),
        'z_min': float(z_min),
        'z_max': float(z_max),
        'thickness': float(thickness),
        'halogen': {},
    }

    for el in ('Cl', 'Br'):
        idx = np.where(syms == el)[0]
        if len(idx) == 0:
            info['halogen'][el] = None
            continue
        pos_h = pos[idx]
        z_h = pos_h[:, 2]

        d_top = z_max - z_h        # distance from top face (NCM-facing in stack)
        d_bot = z_h - z_min        # distance from bottom face

        # nearest Li
        d_to_Li = np.full(len(idx), np.inf)
        d_to_S = np.full(len(idx), np.inf)
        for ih, p in enumerate(pos_h):
            if len(Li_pos):
                d = np.linalg.norm(Li_pos - p, axis=1)
                d_to_Li[ih] = float(np.min(d))
            if len(S_pos):
                d = np.linalg.norm(S_pos - p, axis=1)
                d_to_S[ih] = float(np.min(d))

        info['halogen'][el] = {
            'n': int(len(idx)),
            'z_values': z_h.tolist(),
            'z_mean': float(z_h.mean()),
            'z_std': float(z_h.std()),
            'z_min': float(z_h.min()),
            'z_max': float(z_h.max()),
            'd_top_mean': float(d_top.mean()),
            'd_bot_mean': float(d_bot.mean()),
            'n_near_top': int((d_top <= NEAR_FACE).sum()),
            'n_near_bot': int((d_bot <= NEAR_FACE).sum()),
            'frac_near_face': float(((d_top <= NEAR_FACE) | (d_bot <= NEAR_FACE)).sum() / len(idx)),
            'd_to_Li_mean': float(d_to_Li.mean()),
            'd_to_Li_min': float(d_to_Li.min()),
            'd_to_S_mean': float(d_to_S.mean()),
            'd_to_S_min': float(d_to_S.min()),
        }
    return info


def main():
    results = {}
    print(f"{'comp':<10} {'Δslab':<6} | {'el':<3} {'n':<3} {'<z>':<6} {'<d_top>':<8} {'<d_bot>':<8} "
          f"{'near_top':<8} {'near_bot':<8} {'frac_face':<9} {'<Li>':<6} {'min(Li)':<7} {'<S>':<6}")
    print("=" * 110)

    for c, fn in SLABS.items():
        path = WORK / fn
        if not path.exists():
            print(f"  [{c}] SKIP — file not found: {fn}")
            continue
        atoms = read(path)
        info = analyze(atoms)
        results[c] = info

        for el in ('Cl', 'Br'):
            h = info['halogen'][el]
            if h is None:
                continue
            print(f"{c:<10} {info['thickness']:<6.1f} | "
                  f"{el:<3} {h['n']:<3} {h['z_mean']:<6.2f} "
                  f"{h['d_top_mean']:<8.2f} {h['d_bot_mean']:<8.2f} "
                  f"{h['n_near_top']:<8d} {h['n_near_bot']:<8d} "
                  f"{h['frac_near_face']:<9.2f} "
                  f"{h['d_to_Li_mean']:<6.2f} {h['d_to_Li_min']:<7.2f} "
                  f"{h['d_to_S_mean']:<6.2f}")
        print()

    # ── comp4 v1 vs v2 comparison ──
    print("=" * 110)
    print("comp4 v1 → v2 anneal transition (same composition, different anneal champion)")
    print("=" * 110)
    if 'comp4_v1' in results and 'comp4_v2' in results:
        v1 = results['comp4_v1']
        v2 = results['comp4_v2']
        for el in ('Cl', 'Br'):
            h1 = v1['halogen'][el]
            h2 = v2['halogen'][el]
            if h1 is None or h2 is None:
                continue
            print(f"\n  [{el}]")
            print(f"    <z>            : v1 = {h1['z_mean']:.2f}  v2 = {h2['z_mean']:.2f}  Δ = {h2['z_mean']-h1['z_mean']:+.2f} Å")
            print(f"    <d_to_top>     : v1 = {h1['d_top_mean']:.2f}  v2 = {h2['d_top_mean']:.2f}  Δ = {h2['d_top_mean']-h1['d_top_mean']:+.2f} Å")
            print(f"    <d_to_bot>     : v1 = {h1['d_bot_mean']:.2f}  v2 = {h2['d_bot_mean']:.2f}  Δ = {h2['d_bot_mean']-h1['d_bot_mean']:+.2f} Å")
            print(f"    n near top face: v1 = {h1['n_near_top']:>2d}     v2 = {h2['n_near_top']:>2d}     Δ = {h2['n_near_top']-h1['n_near_top']:+d}")
            print(f"    n near bot face: v1 = {h1['n_near_bot']:>2d}     v2 = {h2['n_near_bot']:>2d}     Δ = {h2['n_near_bot']-h1['n_near_bot']:+d}")
            print(f"    <Li-X> bond    : v1 = {h1['d_to_Li_mean']:.3f} Å  v2 = {h2['d_to_Li_mean']:.3f} Å  Δ = {h2['d_to_Li_mean']-h1['d_to_Li_mean']:+.3f}")
            print(f"    min(Li-X)      : v1 = {h1['d_to_Li_min']:.3f} Å  v2 = {h2['d_to_Li_min']:.3f} Å  Δ = {h2['d_to_Li_min']-h1['d_to_Li_min']:+.3f}")

    # save JSON
    out_json = WORK / 'halogen_slab_positions_summary.json'
    json.dump(results, open(out_json, 'w'), indent=2)
    print(f"\nSaved: {out_json}")

    # ── histogram ──
    fig, axes = plt.subplots(2, 3, figsize=(15, 8), sharey=False)
    plot_comps = ['comp1', 'comp2', 'comp4_v1', 'comp4_v2', 'comp5', 'modelC']
    for ax, c in zip(axes.flat, plot_comps):
        if c not in results:
            ax.set_visible(False)
            continue
        info = results[c]
        # plot z of all halogens, color by element
        for el, color in [('Cl', 'green'), ('Br', 'firebrick')]:
            h = info['halogen'][el]
            if h is None:
                continue
            zs = h['z_values']
            ax.hist(zs, bins=20, range=(info['z_min']-1, info['z_max']+1),
                    color=color, alpha=0.6, label=f"{el} (n={h['n']})", edgecolor='k', lw=0.4)
        ax.axvline(info['z_min'], color='k', ls='--', lw=0.6, alpha=0.5)
        ax.axvline(info['z_max'], color='k', ls='--', lw=0.6, alpha=0.5)
        ax.axvspan(info['z_max']-NEAR_FACE, info['z_max'], color='red', alpha=0.10, label='top face zone')
        ax.axvspan(info['z_min'], info['z_min']+NEAR_FACE, color='blue', alpha=0.10, label='bot face zone')
        ax.set_title(f"{c}  (thickness={info['thickness']:.1f} Å)")
        ax.set_xlabel("z (Å)")
        ax.set_ylabel("halogen count")
        ax.legend(fontsize=8, loc='upper left')
        ax.grid(alpha=0.3)

    fig.suptitle("Halogen z-distribution per slab (top face = NCM-facing in stack)", fontsize=13)
    fig.tight_layout()
    fig.savefig(WORK / 'halogen_slab_positions.png', dpi=150, bbox_inches='tight')
    fig.savefig(WORK / 'halogen_slab_positions.pdf', bbox_inches='tight')
    print(f"Saved: {WORK / 'halogen_slab_positions.png'}")


if __name__ == "__main__":
    main()
