#!/usr/bin/env python3
"""Voxelize DEM atoms.csv into a 3D phase-labeled grid for FFT-based
micromechanics or transport homogenization.

Input
─────
  case_dir/atoms.csv         (id, type, x, y, z, radius — sim units)
  case_dir/meta.json         (type_map, scale, [box_x, box_y, box_z])
  case_dir/input_params.json (box_x, box_y, box_z, r_AM_P, r_AM_S, r_SE)

Output
──────
  case_dir/voxel_grid.npy    — 3D uint8 array
                                  0 = void
                                  1 = AM_P
                                  2 = AM_S
                                  3 = SE
  case_dir/voxel_meta.json   — grid dims, voxel size (μm), type_map

Resolution
──────────
  Default: voxel size = r_SE / 5 → smallest particle has ~10³ ≈ 1000 voxels.
  For r_SE = 0.5 μm and box 50×50×95 μm:
    voxel = 0.1 μm → 500 × 500 × 950 = 237 M voxels (uint8 → 240 MB).
  Use --voxels-per-r-min N to adjust (smaller N = coarser, faster FFT).

Phase priority
──────────────
  When multiple particles overlap a voxel, the phase with highest priority
  wins (default SE > AM_S > AM_P, matching plastic-flow infiltration).
  Use --phase-priority "SE,AM_S,AM_P" to change.

Usage
─────
  python3 scripts/voxelize_microstructure.py CASE_ID
  python3 scripts/voxelize_microstructure.py CASE_ID --voxels-per-r-min 3
  python3 scripts/voxelize_microstructure.py --all
"""
from __future__ import annotations
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
WEBAPP = ROOT / 'webapp'

PHASE_VOID = 0
PHASE_AM_P = 1
PHASE_AM_S = 2
PHASE_SE   = 3
DEFAULT_PHASE_PRIORITY = ('SE', 'AM_S', 'AM_P')   # later overwrites earlier


def discover_case(case_id: str) -> Path | None:
    """Find a case anywhere under webapp/results/ or webapp/archive/ (any depth)."""
    for base in ('results', 'archive'):
        root = WEBAPP / base
        if not root.exists():
            continue
        for atoms_p in root.rglob('atoms.csv'):
            if atoms_p.parent.name == case_id:
                return atoms_p.parent
    return None


def discover_all_cases() -> list[Path]:
    seen = set()
    out = []
    for base in ('results', 'archive'):
        root = WEBAPP / base
        if not root.exists():
            continue
        for atoms_p in root.rglob('atoms.csv'):
            d = atoms_p.parent
            if d not in seen:
                seen.add(d)
                out.append(d)
    return sorted(out)


def _read_meta(case_dir: Path) -> dict:
    for path in (case_dir / 'meta.json',
                 WEBAPP / 'uploads' / case_dir.name / 'meta.json'):
        if path.exists():
            try:
                return json.load(open(path))
            except Exception:
                pass
    return {}


def _parse_type_map(s: str) -> dict[int, str]:
    out = {}
    for tok in (s or '').split(','):
        if ':' in tok:
            k, v = tok.split(':', 1)
            try:
                out[int(k.strip())] = v.strip()
            except Exception:
                pass
    return out


def _phase_id_for_label(label: str) -> int:
    if label == 'AM_P':  return PHASE_AM_P
    if label == 'AM_S':  return PHASE_AM_S
    if label == 'SE':    return PHASE_SE
    return PHASE_VOID


def voxelize(case_dir: Path, voxels_per_r_min: int = 5,
              priority: tuple[str, ...] = DEFAULT_PHASE_PRIORITY,
              quiet: bool = False) -> dict | None:
    """Voxelize one case. Returns metadata dict on success, None on failure."""
    meta = _read_meta(case_dir)
    type_map = _parse_type_map(meta.get('type_map', '1:AM_P,2:AM_S,3:SE'))
    if not type_map:
        type_map = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
    scale = float(meta.get('scale', 1000))

    # Read input_params for box
    ip_path = case_dir / 'input_params.json'
    if not ip_path.exists():
        if not quiet:
            print(f'  ✗ {case_dir.name}: no input_params.json')
        return None
    ip = json.load(open(ip_path))
    box_x_sim = float(ip.get('box_x', 0.05))
    box_y_sim = float(ip.get('box_y', 0.05))
    box_z_sim = float(ip.get('box_z', 0.095))

    # Real-μm extent
    box_x_um = box_x_sim * 1e6 / scale
    box_y_um = box_y_sim * 1e6 / scale
    box_z_um = box_z_sim * 1e6 / scale

    # Determine voxel size from smallest particle radius
    atoms = pd.read_csv(case_dir / 'atoms.csv',
                         usecols=['id', 'type', 'x', 'y', 'z', 'radius'])
    r_min_sim = float(atoms['radius'].min())
    r_min_um = r_min_sim * 1e6 / scale
    voxel_um = r_min_um / voxels_per_r_min

    nx = int(np.ceil(box_x_um / voxel_um))
    ny = int(np.ceil(box_y_um / voxel_um))
    nz = int(np.ceil(box_z_um / voxel_um))
    n_total = nx * ny * nz

    if not quiet:
        print(f'  {case_dir.name}:')
        print(f'    box       : {box_x_um:.1f} × {box_y_um:.1f} × {box_z_um:.1f} μm')
        print(f'    r_min     : {r_min_um:.3f} μm')
        print(f'    voxel     : {voxel_um:.4f} μm  '
              f'({voxels_per_r_min} per r_min)')
        print(f'    grid      : {nx} × {ny} × {nz} = {n_total/1e6:.1f} M voxels')
        print(f'    memory    : {n_total/1024**2:.0f} MB (uint8)')

    if n_total > 5e8:
        if not quiet:
            print(f'    ⚠ grid large — consider --voxels-per-r-min smaller')
    if n_total > 2e9:
        print(f'    ✗ grid too large ({n_total/1e9:.1f} G voxels)')
        return None

    # Initialize void grid
    grid = np.zeros((nx, ny, nz), dtype=np.uint8)

    # Convert atom coords/radii to real μm
    x_um = atoms['x'].values * 1e6 / scale
    y_um = atoms['y'].values * 1e6 / scale
    z_um = atoms['z'].values * 1e6 / scale
    r_um = atoms['radius'].values * 1e6 / scale
    types = atoms['type'].values.astype(int)

    # Map atom type → phase label → priority order
    pri_idx = {lbl: i for i, lbl in enumerate(priority)}
    # Lower idx = higher priority (drawn last → wins)
    # Sort atoms so that highest-priority drawn LAST (overwrites)
    type_to_label = {tid: type_map.get(tid, '') for tid in np.unique(types)}
    type_priority = np.array([pri_idx.get(type_to_label.get(t, ''), 99)
                               for t in types])
    # Higher pri_idx (= lower priority) drawn first; lower pri_idx drawn last
    order = np.argsort(-type_priority)  # descending → low-pri first

    t0 = time.time()
    for i_atom_idx, atom_idx in enumerate(order):
        cx, cy, cz = x_um[atom_idx], y_um[atom_idx], z_um[atom_idx]
        r = r_um[atom_idx]
        phase = _phase_id_for_label(type_to_label.get(types[atom_idx], ''))
        if phase == PHASE_VOID:
            continue

        # Voxel index range covering the sphere bounding box
        ix0 = max(0, int((cx - r) / voxel_um))
        ix1 = min(nx, int((cx + r) / voxel_um) + 1)
        iy0 = max(0, int((cy - r) / voxel_um))
        iy1 = min(ny, int((cy + r) / voxel_um) + 1)
        iz0 = max(0, int((cz - r) / voxel_um))
        iz1 = min(nz, int((cz + r) / voxel_um) + 1)

        if ix1 <= ix0 or iy1 <= iy0 or iz1 <= iz0:
            continue

        # Voxel center coords in this slice
        xv = (np.arange(ix0, ix1) + 0.5) * voxel_um
        yv = (np.arange(iy0, iy1) + 0.5) * voxel_um
        zv = (np.arange(iz0, iz1) + 0.5) * voxel_um

        # Distance²-from-center field for the slice
        Xv, Yv, Zv = np.meshgrid(xv, yv, zv, indexing='ij')
        d2 = (Xv - cx)**2 + (Yv - cy)**2 + (Zv - cz)**2
        mask = d2 <= r * r

        sub = grid[ix0:ix1, iy0:iy1, iz0:iz1]
        sub[mask] = phase

        if not quiet and (i_atom_idx + 1) % max(1, len(order)//10) == 0:
            elapsed = time.time() - t0
            pct = (i_atom_idx + 1) / len(order) * 100
            print(f'    voxelizing  {pct:5.1f}%   ({elapsed:.1f}s)', flush=True)

    # Phase volume fractions
    n_void = int((grid == PHASE_VOID).sum())
    n_amp  = int((grid == PHASE_AM_P).sum())
    n_ams  = int((grid == PHASE_AM_S).sum())
    n_se   = int((grid == PHASE_SE).sum())
    if not quiet:
        print(f'    phase φ   : void {n_void/n_total*100:.1f}%  '
              f'AM_P {n_amp/n_total*100:.1f}%  '
              f'AM_S {n_ams/n_total*100:.1f}%  '
              f'SE {n_se/n_total*100:.1f}%')

    # Save
    grid_p = case_dir / 'voxel_grid.npy'
    np.save(grid_p, grid)
    meta_out = {
        'shape':           [nx, ny, nz],
        'voxel_um':        voxel_um,
        'box_um':          [box_x_um, box_y_um, box_z_um],
        'voxels_per_r_min': voxels_per_r_min,
        'phase_id_map':    {'void': PHASE_VOID, 'AM_P': PHASE_AM_P,
                            'AM_S': PHASE_AM_S, 'SE': PHASE_SE},
        'phase_priority':  list(priority),
        'phi':             {'void': n_void/n_total, 'AM_P': n_amp/n_total,
                            'AM_S': n_ams/n_total, 'SE': n_se/n_total},
        'n_atoms':         len(atoms),
        'r_min_um':        r_min_um,
    }
    with open(case_dir / 'voxel_meta.json', 'w') as f:
        json.dump(meta_out, f, indent=2)
    if not quiet:
        print(f'    ✓ saved   : voxel_grid.npy + voxel_meta.json')
    return meta_out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('case_id', nargs='?',
                    help='Single case to voxelize (default: --all required)')
    ap.add_argument('--all', action='store_true',
                    help='Voxelize all cases under results/ + archive/')
    ap.add_argument('--voxels-per-r-min', type=int, default=5,
                    help='Voxels per smallest particle radius (default 5)')
    ap.add_argument('--phase-priority', default=','.join(DEFAULT_PHASE_PRIORITY),
                    help='Comma list, last overwrites '
                         '(default "SE,AM_S,AM_P")')
    ap.add_argument('--quiet', action='store_true')
    args = ap.parse_args()

    priority = tuple(s.strip() for s in args.phase_priority.split(','))

    if args.case_id:
        case_dir = discover_case(args.case_id)
        if not case_dir:
            ap.error(f'Case {args.case_id!r} not found in webapp/results or archive')
        voxelize(case_dir, voxels_per_r_min=args.voxels_per_r_min,
                  priority=priority, quiet=args.quiet)
    elif args.all:
        cases = discover_all_cases()
        print(f'Voxelizing {len(cases)} cases  '
              f'(voxels_per_r_min={args.voxels_per_r_min}) …')
        n_ok = n_fail = 0
        for d in cases:
            try:
                ok = voxelize(d, voxels_per_r_min=args.voxels_per_r_min,
                                priority=priority, quiet=args.quiet)
                if ok: n_ok += 1
                else:  n_fail += 1
            except Exception as e:
                print(f'  ✗ {d.name}: {type(e).__name__}: {e}')
                n_fail += 1
        print(f'\nDone — {n_ok} ok, {n_fail} failed.')
    else:
        ap.error('Pass a case_id or use --all')


if __name__ == '__main__':
    main()
