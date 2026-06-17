#!/usr/bin/env python3
"""Visualise the MPM scaffold SE morphology: a 2D (x-z) slice of the compacted
composite showing the fixed AM skeleton + the plastically-conformed SE + void.

The MPM SE actually deforms/flows around the real AM (the rigid-sphere DEM
cannot), so this slice is the SE plastic morphology — the MPM's unique output.

Usage:
  python3 scripts/viz_mpm_morphology.py --se se_real14.npy \
      --scaffold docs/data/real14_am_scaffold.csv --y 0.5 --out morph.png
"""
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt                       # noqa: E402
from matplotlib.colors import ListedColormap, BoundaryNorm  # noqa: E402

# scaffold box geometry (must match mpm3d_compaction.py --am-scaffold)
SW = (0.04, 0.96); FLOOR = 0.05
WIDTH = SW[1] - SW[0]; SCL = WIDTH / 0.05              # box units per LIGGGHTS unit
UM_BOX = 1000.0 / SCL                                  # µm per box unit

# phase colours (void / AM_P / AM_S / SE) — match the 2D microstructure viewer
COLORS = ['#ffffff', '#2b2f3a', '#9aa0ad', '#f4d35e']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--se', required=True, help='SE point cloud npy ([n,3], box units) from --save-se')
    ap.add_argument('--scaffold', required=True, help='AM scaffold CSV (type,x,y,z,r LIGGGHTS units)')
    ap.add_argument('--y', type=float, default=0.5, help='slab centre (box units, 0.04..0.96)')
    ap.add_argument('--slab', type=float, default=0.0, help='slab half-thickness (box units; 0=auto)')
    ap.add_argument('--nx', type=int, default=220, help='image columns (≈ SE point density; '
                    'too high → SE undersampled/sparse, too low → blocky)')
    ap.add_argument('--se-min-count', type=int, default=1,
                    help='pixel is SE only if ≥N SE points land in it (1=any point; '
                         '>1 removes the thin-slab salt-and-pepper false void)')
    ap.add_argument('--denoise', type=int, default=0,
                    help='morphological close+open iterations on the SE mask so only '
                         'COHERENT pores remain (0=off; 1-2 typical, needs scipy)')
    ap.add_argument('--out', default='mpm_morphology.png')
    a = ap.parse_args()

    se = np.load(a.se).astype(np.float64)                       # [n,3] box units
    am = np.loadtxt(a.scaffold, delimiter=',')                 # type,x,y,z,r (LIGGGHTS)
    am_t = am[:, 0].astype(int)
    am_c = np.column_stack([SW[0] + am[:, 1] * SCL, SW[0] + am[:, 2] * SCL, FLOOR + am[:, 3] * SCL])
    am_r = am[:, 4] * SCL
    r_se = 0.0005 * SCL
    half = a.slab if a.slab > 0 else 1.5 * r_se                # auto slab ≈ 1.5 SE radii

    # view box: lateral SW, vertical FLOOR..(AM top + margin)
    z_top = float((am_c[:, 2] + am_r).max()) + 0.01
    x0, x1, z0, z1 = SW[0], SW[1], FLOOR, z_top
    nx = a.nx; nz = int(nx * (z1 - z0) / (x1 - x0))
    xs = np.linspace(x0, x1, nx); zs = np.linspace(z0, z1, nz)
    X, Z = np.meshgrid(xs, zs)                                  # [nz,nx]
    lab = np.zeros((nz, nx), np.int8)                          # 0 void

    # SE: bin slab points into the (x,z) image.  Default = SE where any point
    # lands; with --se-min-count, SE only where ≥N points hit a pixel (removes
    # the salt-and-pepper false-void of a thin subsampled slab); --denoise then
    # runs a morphological close+open so only COHERENT pores survive.
    m = np.abs(se[:, 1] - a.y) < half
    sx, sz = se[m, 0], se[m, 2]
    ix = np.clip(((sx - x0) / (x1 - x0) * (nx - 1)).astype(int), 0, nx - 1)
    iz = np.clip(((sz - z0) / (z1 - z0) * (nz - 1)).astype(int), 0, nz - 1)
    cnt = np.zeros((nz, nx), np.int32)
    np.add.at(cnt, (iz, ix), 1)
    se_mask = cnt >= a.se_min_count
    if a.denoise > 0:
        from scipy import ndimage as ndi
        se_mask = ndi.binary_closing(se_mask, iterations=a.denoise)   # fill void specks in SE
        se_mask = ndi.binary_opening(se_mask, iterations=a.denoise)   # drop SE specks in void
    lab[se_mask] = 3                                           # SE

    # AM cross-section at the slab (overwrites SE/void): circle radius √(r²-(cy-y)²)
    for i in range(len(am_r)):
        cx, cy, cz = am_c[i]; rr = am_r[i]
        d = a.y - cy
        if abs(d) >= rr:
            continue
        reff = np.sqrt(rr * rr - d * d)
        lab[(X - cx) ** 2 + (Z - cz) ** 2 <= reff * reff] = am_t[i]   # 1 AM_P / 2 AM_S

    por = 100.0 * (lab == 0).mean()
    se_f = 100.0 * (lab == 3).mean()
    am_f = 100.0 * ((lab == 1) | (lab == 2)).mean()

    fig, ax = plt.subplots(figsize=(9, 9 * (z1 - z0) / (x1 - x0) + 0.6))
    cmap = ListedColormap(COLORS); norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], cmap.N)
    ax.imshow(lab, origin='lower', cmap=cmap, norm=norm, interpolation='nearest',
              extent=[0, (x1 - x0) * UM_BOX, 0, (z1 - z0) * UM_BOX], aspect='equal')
    ax.set_xlabel('x (µm)'); ax.set_ylabel('z (µm, compaction ↓)')
    ax.set_title(f'MPM SE plastic morphology — x-z slice @ y={a.y:.2f}\n'
                 f'AM {am_f:.0f}% (dark=AM_P / gray=AM_S) · SE {se_f:.0f}% (yellow) · '
                 f'void {por:.0f}% (white)', fontsize=10)
    plt.tight_layout(); plt.savefig(a.out, dpi=140)
    print(f'saved {a.out}   slice: AM {am_f:.1f}% / SE {se_f:.1f}% / void {por:.1f}%  '
          f'(SE pts in slab: {m.sum():,})')


if __name__ == '__main__':
    main()
