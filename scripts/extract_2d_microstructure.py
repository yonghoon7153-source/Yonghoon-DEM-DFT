"""
extract_2d_microstructure.py — Phase D1.

3D DEM packing → 2D 4-phase voxel mask (AM_P / AM_S / SE / void).

세미나 피드백 #4 (microstructure 따서 어디서 어떤 형상) + Phase D
(2D microstructure transfer → FEM 입력)의 첫 단계.

방법:
  • z = z_frac × thickness 평면에서 slice (default 중앙 0.5).
  • 평면을 통과하는 입자 i (|z0 − zc| < r): 평면상 반경
    r_slice = √(r² − (z0 − zc)²) 의 원을 (xc, yc)에 그림.
  • 픽셀의 phase = 그 점을 포함하는 입자 중 center가 평면에 가장 가까운
    입자 (overlap 해소).  없으면 void.
  • 출력: numpy int array (0=void / 1=AM_P / 2=AM_S / 3=SE).

출력 (per case):
  docs/data/microstructure_2d/<case>.npy    (H×W int label)
  docs/figures/microstructure_2d/<case>.png  (4-color + phase fraction)

CLI:
  python3 scripts/extract_2d_microstructure.py input_6mAh_real_4
  python3 scripts/extract_2d_microstructure.py --all
  python3 scripts/extract_2d_microstructure.py input_6mAh_real_4 \
      --z-frac 0.5 --n-pixels 500 --slices 3
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

ROOT = Path(__file__).resolve().parent.parent

# Phase labels
VOID, AM_P, AM_S, SE = 0, 1, 2, 3
PHASE_NAMES  = {VOID: 'void', AM_P: 'AM_P', AM_S: 'AM_S', SE: 'SE'}
PHASE_COLORS = {VOID: '#ffffff', AM_P: '#1a1a2e', AM_S: '#8d99ae', SE: '#f4d35e'}


def _type_to_phase(type_name: str) -> int:
    t = (type_name or '').upper()
    if 'AM_P' in t: return AM_P
    if 'AM_S' in t: return AM_S
    if t == 'AM':   return AM_P   # standard mono → treat as AM_P
    if 'SE' in t:   return SE
    return VOID


def slice_microstructure(case_dir: Path, z_frac: float = 0.5,
                          n_pixels: int = 500):
    """Rasterise one z-slice of a case into a 4-phase label grid.

    Returns dict {labels (H×W int), box_x_um, box_y_um, z0_um, ...} or None.
    """
    case_id = case_dir.name
    results_dir = ROOT / 'webapp' / 'results' / case_id
    atoms_csv = results_dir / 'atoms.csv'
    meta_file = case_dir / 'meta.json'
    ip_file = results_dir / 'input_params.json'
    fm_file = results_dir / 'full_metrics.json'
    if not (atoms_csv.exists() and meta_file.exists()):
        return None

    meta = json.loads(meta_file.read_text())
    scale = meta.get('scale', 1000)
    type_map = {}
    for item in meta.get('type_map', '1:AM,2:SE').split(','):
        k, v = item.split(':')
        type_map[int(k)] = v.strip()

    ip = json.loads(ip_file.read_text()) if ip_file.exists() else {}
    box_x_um = (ip.get('box_x') or 0.05) * scale
    box_y_um = (ip.get('box_y') or 0.05) * scale
    if box_x_um <= 0 or box_y_um <= 0:
        return None

    df = pd.read_csv(atoms_csv)
    for col in ('x', 'y', 'z', 'radius', 'type', 'id'):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # All in μm
    xs = df['x'].to_numpy() * scale
    ys = df['y'].to_numpy() * scale
    zs = df['z'].to_numpy() * scale
    rs = df['radius'].to_numpy() * scale
    phases = np.array([_type_to_phase(type_map.get(int(t), ''))
                       for t in df['type'].to_numpy()])

    z_min, z_max = float(np.nanmin(zs - rs)), float(np.nanmax(zs + rs))
    z0 = z_min + z_frac * (z_max - z_min)

    # Pixel grid
    nx = n_pixels
    ny = max(1, int(round(n_pixels * box_y_um / box_x_um)))
    px = box_x_um / nx   # μm per pixel
    py = box_y_um / ny

    labels   = np.zeros((ny, nx), dtype=np.int8)
    # Track |z0 - zc| of the particle currently owning each pixel — smaller
    # (closer center) wins so the slice shows the nearest particle's phase.
    owner_dz = np.full((ny, nx), np.inf, dtype=np.float32)

    # Particles intersecting the plane
    dz = np.abs(zs - z0)
    hit = dz < rs
    idx_hit = np.where(hit)[0]
    # Draw farthest-first so closest overwrites
    order = idx_hit[np.argsort(-dz[idx_hit])]

    for i in order:
        r_slice = float(np.sqrt(max(0.0, rs[i]**2 - (zs[i] - z0)**2)))
        if r_slice <= 0:
            continue
        xc, yc = xs[i], ys[i]
        # bounding box in pixel coords
        ix0 = max(0, int(np.floor((xc - r_slice) / px)))
        ix1 = min(nx - 1, int(np.ceil((xc + r_slice) / px)))
        iy0 = max(0, int(np.floor((yc - r_slice) / py)))
        iy1 = min(ny - 1, int(np.ceil((yc + r_slice) / py)))
        if ix1 < ix0 or iy1 < iy0:
            continue
        # pixel centers
        gx = (np.arange(ix0, ix1 + 1) + 0.5) * px
        gy = (np.arange(iy0, iy1 + 1) + 0.5) * py
        GX, GY = np.meshgrid(gx, gy)
        inside = (GX - xc) ** 2 + (GY - yc) ** 2 <= r_slice ** 2
        sub_dz = owner_dz[iy0:iy1+1, ix0:ix1+1]
        sub_lab = labels[iy0:iy1+1, ix0:ix1+1]
        # this particle wins where inside AND closer than current owner
        win = inside & (dz[i] < sub_dz)
        sub_lab[win] = phases[i]
        sub_dz[win] = dz[i]

    # Phase fractions
    total = labels.size
    fracs = {PHASE_NAMES[p]: round(100 * np.sum(labels == p) / total, 2)
             for p in (VOID, AM_P, AM_S, SE)}

    return {
        'case_id': case_id, 'case_name': meta.get('name', case_id),
        'mode': meta.get('mode', ''), 'ps_ratio': meta.get('ps_ratio', ''),
        'labels': labels, 'box_x_um': box_x_um, 'box_y_um': box_y_um,
        'z0_um': z0, 'z_frac': z_frac, 'z_range_um': (z_min, z_max),
        'n_pixels': nx, 'px_um': px,
        'phase_fracs': fracs,
        'n_particles_hit': int(hit.sum()),
    }


def render_png(data, out_path: Path):
    labels = data['labels']
    cmap = ListedColormap([PHASE_COLORS[p] for p in (VOID, AM_P, AM_S, SE)])
    norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], cmap.N)

    fig, ax = plt.subplots(figsize=(8, 8 * data['box_y_um'] / data['box_x_um'] + 1))
    ax.imshow(labels, origin='lower', cmap=cmap, norm=norm,
               extent=[0, data['box_x_um'], 0, data['box_y_um']],
               interpolation='nearest', aspect='equal')
    ax.set_xlabel('x (μm)'); ax.set_ylabel('y (μm)')
    fr = data['phase_fracs']
    ax.set_title(
        f"{data['case_name']} — 2D microstructure slice\n"
        f"z = {data['z0_um']:.1f} μm ({data['z_frac']:.0%} of {data['z_range_um'][1]:.0f} μm), "
        f"{data['n_pixels']} px ({data['px_um']:.3f} μm/px)\n"
        f"void {fr['void']}% / AM_P {fr['AM_P']}% / AM_S {fr['AM_S']}% / SE {fr['SE']}%",
        fontsize=10)
    # legend
    from matplotlib.patches import Patch
    handles = [Patch(facecolor=PHASE_COLORS[p], edgecolor='gray',
                      label=f'{PHASE_NAMES[p]} ({fr[PHASE_NAMES[p]]}%)')
               for p in (AM_P, AM_S, SE, VOID)]
    ax.legend(handles=handles, loc='upper right', fontsize=9,
              framealpha=0.9)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=130, bbox_inches='tight')
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cases', nargs='*', help='case names or "--all"')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--tier')
    ap.add_argument('--z-frac', type=float, default=0.5,
                    help='slice height fraction (0=bottom, 1=top, default 0.5)')
    ap.add_argument('--n-pixels', type=int, default=500)
    ap.add_argument('--slices', type=int, default=1,
                    help='# slices evenly spaced (overrides --z-frac if >1)')
    ap.add_argument('--out-png', default='docs/figures/microstructure_2d')
    ap.add_argument('--out-npy', default='docs/data/microstructure_2d')
    args = ap.parse_args()

    uploads = ROOT / 'webapp' / 'uploads'
    candidates = []
    if args.all or args.tier:
        for d in sorted(uploads.iterdir()):
            if not d.is_dir(): continue
            mf = d / 'meta.json'
            if not mf.exists(): continue
            try:
                name = json.loads(mf.read_text()).get('name', d.name)
            except Exception:
                continue
            if args.tier and args.tier not in name:
                continue
            candidates.append((name, d))
    elif args.cases:
        for cn in args.cases:
            for d in uploads.iterdir():
                if not d.is_dir(): continue
                mf = d / 'meta.json'
                if mf.exists():
                    try:
                        if json.loads(mf.read_text()).get('name') == cn:
                            candidates.append((cn, d)); break
                    except Exception:
                        pass
    else:
        ap.print_help(); return

    out_png_dir = ROOT / args.out_png
    out_npy_dir = ROOT / args.out_npy
    out_png_dir.mkdir(parents=True, exist_ok=True)
    out_npy_dir.mkdir(parents=True, exist_ok=True)

    z_fracs = ([args.z_frac] if args.slices <= 1
               else list(np.linspace(0.25, 0.75, args.slices)))

    print(f'Processing {len(candidates)} case(s), {len(z_fracs)} slice(s) each...')
    n_ok = 0
    for name, d in candidates:
        for zf in z_fracs:
            try:
                data = slice_microstructure(d, z_frac=zf, n_pixels=args.n_pixels)
            except Exception as e:
                print(f'  [{name} z={zf:.2f}] FAILED: {type(e).__name__}: {e}')
                continue
            if not data:
                print(f'  [{name}] skip (missing data)')
                break
            tag = f'{name}' if len(z_fracs) == 1 else f'{name}_z{zf:.2f}'
            np.save(out_npy_dir / f'{tag}.npy', data['labels'])
            render_png(data, out_png_dir / f'{tag}.png')
            fr = data['phase_fracs']
            print(f'  [{tag}] void {fr["void"]}% AM_P {fr["AM_P"]}% '
                  f'AM_S {fr["AM_S"]}% SE {fr["SE"]}%  '
                  f'({data["n_particles_hit"]} particles in slice)')
            n_ok += 1

    print(f'\nDone — {n_ok} slices.')
    print(f'  PNG → {out_png_dir}')
    print(f'  NPY → {out_npy_dir}')


if __name__ == '__main__':
    main()
