#!/usr/bin/env python3
"""Extract 3D pore mesh from DEM packing for XCT-style visualization.

Voxelizes particles from atoms.csv, computes the complementary pore network,
filters small noise components, and exports:
  - pores.glb    (Three.js / web viewer)
  - pores.stl    (ParaView / Blender / Meshlab)
  - pore_metrics.json (porosity, pore D10/D50/D90, connectivity, surface area)

Usage
─────
  python3 scripts/extract_pore_mesh.py CASE_DIR
  python3 scripts/extract_pore_mesh.py CASE_DIR --voxel-res 256 --pore-min 100
  python3 scripts/extract_pore_mesh.py --all
  python3 scripts/extract_pore_mesh.py --all --jobs 4

Dependencies
────────────
  pip install scipy scikit-image trimesh
"""
from __future__ import annotations
import argparse
import json
import sys
import traceback
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
WEBAPP = ROOT / 'webapp'


# ── voxel stamping ────────────────────────────────────────────────────────

def _stamp_spheres(solid: np.ndarray, atoms_arr: np.ndarray,
                    xmin: float, ymin: float, zmin: float, dx: float) -> None:
    """Mark voxels inside each sphere as solid (in-place).

    atoms_arr columns: x, y, z, r (SI units, e.g. meters).
    Uses vectorized bounding-box per particle rather than triple nested loop.
    """
    nx, ny, nz = solid.shape
    for x, y, z, r in atoms_arr:
        ix0 = (x - xmin) / dx
        iy0 = (y - ymin) / dx
        iz0 = (z - zmin) / dx
        ir = r / dx
        ir_ceil = int(np.ceil(ir)) + 1

        ilo = max(0, int(ix0 - ir_ceil))
        ihi = min(nx, int(ix0 + ir_ceil) + 1)
        jlo = max(0, int(iy0 - ir_ceil))
        jhi = min(ny, int(iy0 + ir_ceil) + 1)
        klo = max(0, int(iz0 - ir_ceil))
        khi = min(nz, int(iz0 + ir_ceil) + 1)
        if ihi <= ilo or jhi <= jlo or khi <= klo:
            continue

        I, J, K = np.ogrid[ilo:ihi, jlo:jhi, klo:khi]
        d2 = (I - ix0) ** 2 + (J - iy0) ** 2 + (K - iz0) ** 2
        mask = d2 <= ir * ir
        solid[ilo:ihi, jlo:jhi, klo:khi] |= mask


# ── main extraction ───────────────────────────────────────────────────────

def extract_pore_mesh(case_dir: Path, voxel_res: int = 200,
                      pore_min_voxels: int = 50,
                      save_mesh: bool = True) -> dict:
    """Run full pipeline. Returns metrics dict."""
    case_dir = Path(case_dir)
    atoms_path = case_dir / 'atoms.csv'
    if not atoms_path.exists():
        raise FileNotFoundError(atoms_path)

    atoms = pd.read_csv(atoms_path)
    cols_lc = {c.lower(): c for c in atoms.columns}
    x_col = cols_lc.get('x', 'x')
    y_col = cols_lc.get('y', 'y')
    z_col = cols_lc.get('z', 'z')
    r_col = (cols_lc.get('r') or cols_lc.get('radius')
             or cols_lc.get('rad') or 'r')

    xs = atoms[x_col].to_numpy()
    ys = atoms[y_col].to_numpy()
    zs = atoms[z_col].to_numpy()
    rs = atoms[r_col].to_numpy()

    # Domain bounding box (tight, no extra margin → preserves true porosity)
    xmin, xmax = (xs - rs).min(), (xs + rs).max()
    ymin, ymax = (ys - rs).min(), (ys + rs).max()
    zmin, zmax = (zs - rs).min(), (zs + rs).max()

    L = max(xmax - xmin, ymax - ymin, zmax - zmin)
    dx = L / voxel_res
    nx = int(np.ceil((xmax - xmin) / dx))
    ny = int(np.ceil((ymax - ymin) / dx))
    nz = int(np.ceil((zmax - zmin) / dx))
    print(f'  Voxel grid: {nx}×{ny}×{nz}  (dx = {dx*1e6:.3f} µm)')
    print(f'  Particles: {len(atoms)}')

    solid = np.zeros((nx, ny, nz), dtype=bool)
    _stamp_spheres(solid, np.column_stack([xs, ys, zs, rs]),
                   xmin, ymin, zmin, dx)

    pore = ~solid

    # ── filter small isolated pores ──────────────────────────────────────
    from scipy.ndimage import label, distance_transform_edt
    labeled, _ = label(pore)
    sizes = np.bincount(labeled.ravel())
    sizes[0] = 0  # background label
    keep_labels = np.where(sizes >= pore_min_voxels)[0]
    pore_clean = np.isin(labeled, keep_labels)

    porosity = float(pore_clean.sum()) / pore.size

    # ── pore size distribution (Euclidean distance transform) ────────────
    dist_vox = distance_transform_edt(pore_clean)
    diameters_um = 2.0 * dist_vox[pore_clean] * dx * 1e6
    if diameters_um.size > 0:
        d10 = float(np.percentile(diameters_um, 10))
        d50 = float(np.percentile(diameters_um, 50))
        d90 = float(np.percentile(diameters_um, 90))
        dmax = float(diameters_um.max())
        dmean = float(diameters_um.mean())
    else:
        d10 = d50 = d90 = dmax = dmean = 0.0

    # ── connectivity ──────────────────────────────────────────────────────
    labeled2, _ = label(pore_clean)
    comp_sizes = np.bincount(labeled2.ravel())[1:]  # skip background
    if comp_sizes.size > 0:
        largest_frac = float(comp_sizes.max() / comp_sizes.sum())
        n_components = int(comp_sizes.size)
    else:
        largest_frac = 0.0
        n_components = 0

    metrics = {
        'voxel_resolution': int(voxel_res),
        'voxel_size_um': float(dx * 1e6),
        'porosity_voxel': porosity,
        'n_particles': int(len(atoms)),
        'n_pore_components': n_components,
        'largest_pore_fraction': largest_frac,
        'pore_diameter_mean_um': dmean,
        'pore_diameter_d10_um': d10,
        'pore_diameter_d50_um': d50,
        'pore_diameter_d90_um': d90,
        'pore_diameter_max_um': dmax,
    }

    # ── mesh export ───────────────────────────────────────────────────────
    if save_mesh:
        try:
            from skimage.measure import marching_cubes
            from scipy.ndimage import gaussian_filter
            import trimesh
        except ImportError as e:
            print(f'  [warn] mesh export skipped — install: pip install scikit-image trimesh ({e})',
                  file=sys.stderr)
        else:
            # Slight smoothing to remove voxel staircase
            field = gaussian_filter(pore_clean.astype(np.float32), sigma=0.8)
            verts, faces, _, _ = marching_cubes(field, level=0.5,
                                                 spacing=(dx, dx, dx))
            verts += np.array([xmin, ymin, zmin])
            mesh = trimesh.Trimesh(vertices=verts, faces=faces, process=True)

            # Surface area (in m²)
            try:
                sa_m2 = float(mesh.area)
                vol_m3 = pore.size * dx ** 3
                metrics['pore_surface_area_um2'] = sa_m2 * 1e12
                metrics['specific_surface_per_volume_um2_per_um3'] = (
                    sa_m2 * 1e12) / (vol_m3 * 1e18)
            except Exception:
                pass

            mesh.export(case_dir / 'pores.glb')
            mesh.export(case_dir / 'pores.stl')
            print(f'  Saved: pores.glb, pores.stl')

    # ── write metrics ────────────────────────────────────────────────────
    with open(case_dir / 'pore_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)

    print(f'  Porosity (voxel): {porosity*100:.2f}%  |  '
          f'D50 pore: {d50:.2f} µm  |  components: {n_components}')
    return metrics


# ── discovery + CLI ──────────────────────────────────────────────────────

def discover_cases() -> list[Path]:
    out = []
    for base in ('results', 'archive'):
        root = WEBAPP / base
        if not root.exists():
            continue
        for atoms_p in root.rglob('atoms.csv'):
            out.append(atoms_p.parent)
    return sorted(set(out))


def _worker(args):
    case_dir, voxel_res, pore_min = args
    try:
        m = extract_pore_mesh(case_dir, voxel_res, pore_min)
        return (case_dir.name, True, f"ε={m['porosity_voxel']*100:.2f}%")
    except Exception as e:
        return (case_dir.name, False, f'{type(e).__name__}: {e}')


def main():
    ap = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__)
    ap.add_argument('case_dir', nargs='?', help='Single case directory')
    ap.add_argument('--all', action='store_true',
                    help='Process every case under webapp/results + webapp/archive')
    ap.add_argument('--voxel-res', type=int, default=200,
                    help='Voxel grid resolution along longest axis (default 200)')
    ap.add_argument('--pore-min', type=int, default=50,
                    help='Minimum voxels for a pore component (smaller = noise)')
    ap.add_argument('--jobs', '-j', type=int, default=1,
                    help='Parallel workers when using --all')
    args = ap.parse_args()

    if args.all:
        cases = discover_cases()
        if not cases:
            ap.error('No cases found under webapp/results or webapp/archive')
        print(f'Processing {len(cases)} cases (jobs={args.jobs})...')
        n_ok = n_fail = 0
        if args.jobs > 1:
            from concurrent.futures import ProcessPoolExecutor, as_completed
            tasks = [(c, args.voxel_res, args.pore_min) for c in cases]
            with ProcessPoolExecutor(max_workers=args.jobs) as ex:
                futs = {ex.submit(_worker, t): t for t in tasks}
                for i, f in enumerate(as_completed(futs), 1):
                    cid, ok, msg = f.result()
                    tag = '✓' if ok else '✗'
                    print(f'  [{i:3d}/{len(cases)}] {tag} {cid:35s} {msg}')
                    n_ok += int(ok)
                    n_fail += int(not ok)
        else:
            for i, c in enumerate(cases, 1):
                print(f'[{i}/{len(cases)}] {c.name}')
                try:
                    extract_pore_mesh(c, args.voxel_res, args.pore_min)
                    n_ok += 1
                except Exception:
                    traceback.print_exc()
                    n_fail += 1
        print(f'\nDone — {n_ok} ok, {n_fail} failed.')
        sys.exit(0 if n_fail == 0 else 1)

    elif args.case_dir:
        extract_pore_mesh(Path(args.case_dir), args.voxel_res, args.pore_min)
    else:
        ap.error('Provide CASE_DIR or use --all')


if __name__ == '__main__':
    main()
