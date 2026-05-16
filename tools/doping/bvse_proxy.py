#!/usr/bin/env python
"""bvse_proxy.py — Bond Valence Site Energy proxy (pure Python, no UMA).

Computes per-Li bond valence sums from final relaxed geometry and reports
distribution statistics that correlate with Li migration barrier.

Theory:
  BVS_Li = Σ exp((R0 - R_ij) / b)
  where the sum is over neighboring anions j (S, Cl, Br, I, O, N, F).
  R0 (single-bond reference length) and b (universal soft-cutoff) are
  tabulated per cation-anion pair (Brown 2002 + Adams 2003 BVS database).

  An ideal Li⁺ site has BVS ≈ 1.0 (full nominal valence). σ-fast ionic
  conductors exhibit BROAD BVS distributions across Li sites (Adams 2003
  / Mo 2014), indicating energetically near-equivalent positions and
  thus low migration barriers — the Li atom essentially sees a flat
  potential energy landscape.

Output per structure:
  bvs_li_mean, bvs_li_std, bvs_li_min, bvs_li_max
  n_li_undervalent (BVS < 0.7), n_li_overvalent (BVS > 1.3)
  bvs_li_proxy_score = std × (1 - |mean − 1.0|)  — higher = more sigma-favorable

Higher proxy score → flatter PES → expected faster σ.

Usage:
  python3 tools/doping/bvse_proxy.py \\
      --xyz_dir runs/.../structures \\
      --out runs/.../bvs_report.json

  # Or single file
  python3 tools/doping/bvse_proxy.py --xyz foo.xyz
"""
import argparse
import json
import math
from pathlib import Path
import sys
import numpy as np
from ase.io import read

sys.path.insert(0, str(Path(__file__).parent))
from _provenance import get_provenance


# Bond valence parameters R0 (Å), b (Å) for Li-anion pairs.
# Sources: Brown & Altermatt 1985 (oxides), Adams 2003 (sulfides/halides),
# Mo et al. 2014 (BVSE refinement for Li ion conductors).
BVS_PARAMS = {
    'O':  {'R0': 1.466, 'b': 0.37},
    'S':  {'R0': 1.94,  'b': 0.40},   # Adams 2003 Li-S
    'Se': {'R0': 2.10,  'b': 0.40},
    'Te': {'R0': 2.32,  'b': 0.40},
    'F':  {'R0': 1.36,  'b': 0.37},
    'Cl': {'R0': 1.91,  'b': 0.37},
    'Br': {'R0': 2.07,  'b': 0.37},
    'I':  {'R0': 2.29,  'b': 0.37},
    'N':  {'R0': 1.61,  'b': 0.37},
}
NEIGHBOR_CUTOFF_A = 5.0  # neighbors within this distance contribute


def compute_migration_volume(atoms, bvs_lo: float = 0.8,
                            bvs_hi: float = 1.2,
                            n_grid: int = 20,
                            cutoff: float = 5.0) -> dict:
    """Quantitative Li-migration accessible volume.

    Samples an n_grid³ uniform fractional grid throughout the unit cell,
    treats each grid point as a virtual Li site, computes the bond
    valence sum from neighboring anions, and counts the fraction of
    grid points falling within [bvs_lo, bvs_hi] — the energetically
    acceptable range for a Li⁺ ion (Adams 2010 / Mo 2014).

    Higher migration_volume_fraction → larger accessible region → faster
    Li transport (BVSE-style cheap proxy for AIMD σ). Not a substitute
    for full AIMD, but provides an O(seconds) screening filter for the
    "Top-N to invest in AIMD" decision.

    Output:
      migration_volume_fraction: ratio of acceptable grid points
      accessible_volume_A3: that fraction × cell volume
      grid_bvs_mean / grid_bvs_std: bulk BVS landscape statistics
      bvs_threshold_used: (lo, hi)
    """
    syms = atoms.get_chemical_symbols()
    anion_idx = [i for i, s in enumerate(syms) if s in BVS_PARAMS]
    if not anion_idx:
        return {'migration_volume_fraction': 0.0,
               'accessible_volume_A3': 0.0,
               'error': 'no anions'}

    cell = atoms.cell.array
    pos = atoms.get_positions()
    anion_pos = pos[anion_idx]
    anion_syms = [syms[i] for i in anion_idx]

    # Fractional grid
    one = np.linspace(0, 1, n_grid, endpoint=False)
    frac = np.array(np.meshgrid(one, one, one, indexing='ij')).reshape(3, -1).T
    cart = frac @ cell  # (n_grid³, 3)

    # PBC-replicated anions for fast tree lookup
    from scipy.spatial import cKDTree
    shifts = np.array([[i, j, k] for i in (-1, 0, 1)
                       for j in (-1, 0, 1) for k in (-1, 0, 1)])
    anion_pbc = np.concatenate([anion_pos + s @ cell for s in shifts])
    anion_pbc_syms = anion_syms * 27

    tree = cKDTree(anion_pbc)
    distances, indices = tree.query(cart, k=25,
                                   distance_upper_bound=cutoff)

    # Vectorized BVS accumulation: pre-compute per-symbol R0, b arrays
    R0_arr = np.array([BVS_PARAMS[s]['R0'] for s in anion_pbc_syms])
    b_arr = np.array([BVS_PARAMS[s]['b'] for s in anion_pbc_syms])
    # For each grid point, accumulate exp((R0 - d)/b) over its neighbors
    bvs_grid = np.zeros(cart.shape[0])
    for k in range(distances.shape[1]):
        col_d = distances[:, k]
        col_i = indices[:, k]
        valid = (col_d < np.inf) & (col_i < len(anion_pbc))
        if not valid.any():
            continue
        idx = col_i[valid]
        bvs_grid[valid] += np.exp((R0_arr[idx] - col_d[valid]) / b_arr[idx])

    n_total = len(bvs_grid)
    accessible_mask = (bvs_grid >= bvs_lo) & (bvs_grid <= bvs_hi)
    n_accessible = int(accessible_mask.sum())
    vol_cell = atoms.get_volume()

    return {
        'migration_volume_fraction': n_accessible / n_total,
        'accessible_volume_A3': (n_accessible / n_total) * vol_cell,
        'grid_resolution': n_grid,
        'grid_bvs_mean': float(bvs_grid.mean()),
        'grid_bvs_std': float(bvs_grid.std()),
        'bvs_threshold_used': [bvs_lo, bvs_hi],
        'cutoff_A': cutoff,
    }


def compute_bvs_per_li(atoms) -> dict:
    """Bond valence sum per Li atom + distribution stats."""
    syms = atoms.get_chemical_symbols()
    li_idx = [i for i, s in enumerate(syms) if s == 'Li']
    anion_idx = [i for i, s in enumerate(syms) if s in BVS_PARAMS]
    if not li_idx or not anion_idx:
        return {'error': 'no Li or no anions'}

    D = atoms.get_all_distances(mic=True)
    bvs_values = []
    for li in li_idx:
        bvs = 0.0
        for j in anion_idx:
            r = D[li, j]
            if r > NEIGHBOR_CUTOFF_A:
                continue
            sym = syms[j]
            p = BVS_PARAMS[sym]
            bvs += math.exp((p['R0'] - r) / p['b'])
        bvs_values.append(bvs)
    arr = np.array(bvs_values)

    mean = float(arr.mean())
    std = float(arr.std())
    # Proxy: σ-fast Li conductors have FLAT PES across Li sites, i.e. BVS≈1.0
    # consistently with SMALL std (Adams 2003 / Mo 2014 BVSE landscape). Fixed
    # sign convention vs earlier version (which inverted the chemistry):
    # high std means some deep-trap + some over-coordinated sites that block
    # percolation. Score combines (closeness of mean to 1) × (1 - std).
    deviation_from_1 = abs(mean - 1.0)
    proxy = max(0.0, 1.0 - deviation_from_1) * max(0.0, 1.0 - std)

    return {
        'bvs_li_mean': mean,
        'bvs_li_std': std,
        'bvs_li_min': float(arr.min()),
        'bvs_li_max': float(arr.max()),
        'n_li_undervalent_lt_0p7': int(np.sum(arr < 0.7)),
        'n_li_overvalent_gt_1p3': int(np.sum(arr > 1.3)),
        'n_li_ideal_0p8_to_1p2': int(np.sum((arr > 0.8) & (arr < 1.2))),
        'bvs_li_proxy_score': float(proxy),
        'bvs_values': arr.tolist(),
    }


def main():
    p = argparse.ArgumentParser(description=__doc__,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--xyz', nargs='+', help='Individual xyz files')
    p.add_argument('--xyz_dir', help='Directory to scan recursively')
    p.add_argument('--out', required=True, help='Output JSON')
    p.add_argument('--grid_resolution', type=int, default=20,
                  help='Migration volume grid (default 20³ = 8000 points; '
                       'increase to 30 for finer scan at ~3× cost)')
    args = p.parse_args()

    paths = []
    if args.xyz:
        paths.extend(Path(p) for p in args.xyz)
    if args.xyz_dir:
        paths.extend(sorted(Path(args.xyz_dir).rglob('*.xyz')))
    paths = [p for p in paths if p.name not in ('post_md.xyz', 'post_relax.xyz')]
    print(f"Processing {len(paths)} structures")

    # Resume — load existing records if present
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    existing = {}
    if out.exists():
        try:
            prev = json.loads(out.read_text())
            for r in prev.get('records', []):
                if 'name' in r:
                    existing[r['name']] = r
            print(f"  Resume: {len(existing)} records already computed")
        except Exception:
            existing = {}

    records = list(existing.values())
    todo = [p for p in paths if p.stem not in existing]
    print(f"  To compute: {len(todo)}/{len(paths)}")

    for i, xpath in enumerate(todo):
        try:
            atoms = read(str(xpath))
            bvs = compute_bvs_per_li(atoms)
            mig = compute_migration_volume(atoms,
                                          n_grid=args.grid_resolution)
            records.append({'name': xpath.stem, 'xyz': str(xpath),
                          **bvs, **mig})
        except Exception as e:
            records.append({'name': xpath.stem, 'error': str(e)})
        if (i + 1) % 50 == 0 or (i + 1) == len(todo):
            # Periodic save for crash resilience
            out.write_text(json.dumps({
                'provenance': get_provenance(),
                'n_records': len(records),
                'records': records,
            }, indent=2, default=str))
            print(f"  {i+1}/{len(todo)}")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        'provenance': get_provenance(),
        'n_records': len(records),
        'records': records,
    }, indent=2, default=str))

    # Rank by migration volume × proxy score (combined Li mobility metric)
    ok = [r for r in records if 'bvs_li_proxy_score' in r
          and 'migration_volume_fraction' in r]
    for r in ok:
        # Combined: weight migration volume (most direct conductivity proxy)
        # 3x, BVS proxy score 1x
        r['li_mobility_score'] = (3 * r['migration_volume_fraction']
                                  + r['bvs_li_proxy_score'])
    ok.sort(key=lambda r: -r['li_mobility_score'])
    print(f"\n{'Rank':<5}{'Name':<45}{'⟨BVS⟩':>8}{'σ BVS':>8}{'V_mig%':>9}"
          f"{'mob_score':>11}")
    for i, r in enumerate(ok[:20], 1):
        print(f"{i:<5}{r['name'][:43]:<45}"
              f"{r['bvs_li_mean']:>7.3f} "
              f"{r['bvs_li_std']:>7.3f} "
              f"{r['migration_volume_fraction']*100:>7.2f}% "
              f"{r['li_mobility_score']:>10.4f}")
    print(f"\n✓ {len(records)} BVS records → {out}")


if __name__ == '__main__':
    main()
