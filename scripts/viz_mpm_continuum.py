#!/usr/bin/env python3
"""3D CONTINUUM view of the MPM scaffold result — the composite cathode as a
solid electrode, not a point cloud.

Voxelise the SE material-point cloud + the fixed AM scaffold into a 3D
occupancy grid (void / AM_P / AM_S / SE), denoise the SE (count threshold +
3D morphological open/close → kills sub-sample salt-and-pepper), optionally
cut a corner away to see inside, then marching-cubes each phase into a surface
mesh and render it as a solid continuum:
  • AM_P (dark) + AM_S (gray) = the rigid skeleton, opaque,
  • SE (yellow) = the plastically-flowed electrolyte matrix, semi-opaque,
  • void = the residual pores (the gaps left in the SE).

The voxel occupancy also reports the TRUE 3D porosity at this resolution
(void voxels / total) — a cross-check on the 2D-slice number.

Engines:
  • plotly (default) — interactive rotatable HTML (Mesh3d). Best.
  • mpl              — static PNG (Poly3DCollection), multi-angle. Offline.

  # real result (run mpm3d_compaction --save-se se384.npy first):
  python3 scripts/viz_mpm_continuum.py --se se384.npy \
      --scaffold docs/data/real14_am_scaffold.csv --n-vox 256 --cut corner \
      --denoise 1 --out electrode3d.html

  # geometry proxy (no MPM run — cell-fill):
  python3 scripts/viz_mpm_continuum.py --se-proxy --se-frac 0.27 \
      --scaffold docs/data/real14_am_scaffold.csv --n-vox 200 --out proxy3d.html

Needs: numpy, scikit-image (marching cubes), scipy (denoise); plotly for HTML.
"""
import argparse
import numpy as np

# scaffold box geometry (must match mpm3d_compaction.py --am-scaffold)
SW = (0.04, 0.96); FLOOR = 0.05
WIDTH = SW[1] - SW[0]; SCL = WIDTH / 0.05               # box units per LIGGGHTS unit
UM_BOX = 1000.0 / SCL                                   # µm per box unit
COL = {1: '#2b2f3a', 2: '#9aa0ad', 3: '#f4d35e'}       # AM_P / AM_S / SE


def load_am(path):
    am = np.loadtxt(path, delimiter=',')
    t = am[:, 0].astype(int)
    c = np.column_stack([SW[0] + am[:, 1] * SCL,
                         SW[0] + am[:, 2] * SCL,
                         FLOOR + am[:, 3] * SCL])
    r = am[:, 4] * SCL
    return t, c, r


def voxelize(se, t, c, r, n_vox, top, se_min_count, denoise):
    """→ (am_p, am_s, se_mask) boolean grids [nx,ny,nz] (x,y,z order) + h."""
    h = WIDTH / n_vox
    nx = ny = n_vox
    nz = int(np.ceil((top - FLOOR) / h))
    am_p = np.zeros((nx, ny, nz), bool)
    am_s = np.zeros((nx, ny, nz), bool)
    for i in range(len(r)):
        cx, cy, cz = c[i]; rr = r[i]
        ix0 = max(0, int((cx - rr - SW[0]) / h)); ix1 = min(nx, int((cx + rr - SW[0]) / h) + 1)
        iy0 = max(0, int((cy - rr - SW[0]) / h)); iy1 = min(ny, int((cy + rr - SW[0]) / h) + 1)
        iz0 = max(0, int((cz - rr - FLOOR) / h)); iz1 = min(nz, int((cz + rr - FLOOR) / h) + 1)
        if ix0 >= ix1 or iy0 >= iy1 or iz0 >= iz1:
            continue
        gx = (SW[0] + (np.arange(ix0, ix1) + 0.5) * h - cx)[:, None, None]
        gy = (SW[0] + (np.arange(iy0, iy1) + 0.5) * h - cy)[None, :, None]
        gz = (FLOOR + (np.arange(iz0, iz1) + 0.5) * h - cz)[None, None, :]
        inside = gx * gx + gy * gy + gz * gz <= rr * rr
        (am_p if t[i] == 1 else am_s)[ix0:ix1, iy0:iy1, iz0:iz1] |= inside
    am = am_p | am_s

    # SE occupancy by per-voxel point count
    ix = np.clip(((se[:, 0] - SW[0]) / h).astype(np.int64), 0, nx - 1)
    iy = np.clip(((se[:, 1] - SW[0]) / h).astype(np.int64), 0, ny - 1)
    iz = np.clip(((se[:, 2] - FLOOR) / h).astype(np.int64), 0, nz - 1)
    cnt = np.zeros((nx, ny, nz), np.int32)
    np.add.at(cnt, (ix, iy, iz), 1)
    se_mask = (cnt >= se_min_count) & (~am)
    if denoise > 0:
        from scipy import ndimage as ndi
        se_mask = ndi.binary_closing(se_mask, iterations=denoise) & (~am)  # fill void specks
        se_mask = ndi.binary_opening(se_mask, iterations=denoise)          # drop SE specks
    return am_p, am_s, se_mask, h


def apply_cut(mask, cut):
    if cut == 'none':
        return mask
    nx, ny, nz = mask.shape
    m = mask.copy()
    if cut == 'half':
        m[nx // 2:, :, :] = False                       # remove +x half
    elif cut == 'corner':
        m[nx // 2:, ny // 2:, :] = False                # remove +x,+y octant
    return m


def mesh_of(mask, step):
    from skimage.measure import marching_cubes
    if mask.sum() < 8:
        return None
    # pad so surfaces at the array border close into solids
    p = np.pad(mask.astype(np.float32), 1)
    v, f, _, _ = marching_cubes(p, level=0.5, step_size=step)
    return v - 1.0, f                                    # undo pad offset (voxel idx)


def render_plotly(meshes, h, out):
    import plotly.graph_objects as go
    s = h * UM_BOX                                       # voxel-idx → µm
    data = []
    for (v, f), col, name, op in meshes:
        data.append(go.Mesh3d(x=v[:, 0] * s, y=v[:, 1] * s, z=v[:, 2] * s,
                              i=f[:, 0], j=f[:, 1], k=f[:, 2], color=col,
                              opacity=op, name=name, showscale=False,
                              flatshading=True, lighting=dict(ambient=0.45, diffuse=0.8)))
    fig = go.Figure(data=data)
    fig.update_layout(title='MPM composite cathode — 3D continuum '
                      '(AM skeleton + plastic SE matrix + pores)',
                      scene=dict(xaxis_title='x (µm)', yaxis_title='y (µm)',
                                 zaxis_title='z (µm)', aspectmode='data'))
    fig.write_html(out)
    print(f'saved {out}   (plotly interactive)')


def render_mpl(meshes, h, out):
    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    s = h * UM_BOX
    fig = plt.figure(figsize=(11, 10)); ax = fig.add_subplot(111, projection='3d')
    for (v, f), col, name, op in meshes:
        tri = v[f] * s                                  # (ntri,3,3) µm
        pc = Poly3DCollection(tri, alpha=op, facecolor=col, linewidths=0)
        ax.add_collection3d(pc)
    allv = np.vstack([v for (v, f), *_ in meshes]) * s
    ax.set_xlim(allv[:, 0].min(), allv[:, 0].max())
    ax.set_ylim(allv[:, 1].min(), allv[:, 1].max())
    ax.set_zlim(allv[:, 2].min(), allv[:, 2].max())
    ax.set_box_aspect((np.ptp(allv[:, 0]), np.ptp(allv[:, 1]), np.ptp(allv[:, 2])))
    ax.view_init(elev=18, azim=-65)
    ax.set_xlabel('x (µm)'); ax.set_ylabel('y (µm)'); ax.set_zlabel('z (µm)')
    plt.tight_layout(); plt.savefig(out, dpi=140)
    print(f'saved {out}   (mpl static)')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scaffold', required=True)
    ap.add_argument('--se', help='SE point cloud npy [n,3] box units (--save-se)')
    ap.add_argument('--se-proxy', action='store_true', help='no MPM: cell-fill proxy')
    ap.add_argument('--se-frac', type=float, default=0.27)
    ap.add_argument('--n-vox', type=int, default=220, help='lateral voxels (higher = finer; '
                    'plotly HTML grows with surface area — 256 is a good interactive ceiling)')
    ap.add_argument('--se-min-count', type=int, default=1, help='voxel is SE if ≥N points')
    ap.add_argument('--denoise', type=int, default=1, help='3D close+open iters (speckle removal)')
    ap.add_argument('--cut', choices=['none', 'half', 'corner'], default='corner')
    ap.add_argument('--step', type=int, default=2, help='marching-cubes step (2 = coarser/fewer tris)')
    ap.add_argument('--se-opacity', type=float, default=0.55, help='SE matrix transparency')
    ap.add_argument('--engine', choices=['plotly', 'mpl'], default='plotly')
    ap.add_argument('--measure-only', action='store_true',
                    help='voxelise + print AM/SE/VOID %% then stop (no mesh/render) — '
                         'fast sweep to find the --se-min-count that hits true porosity')
    ap.add_argument('--out', default='mpm_continuum_3d.html')
    a = ap.parse_args()

    t, c, r = load_am(a.scaffold)
    top = float((c[:, 2] + r).max()) + 0.01
    if a.se_proxy or not a.se:
        import importlib.util
        spec = importlib.util.spec_from_file_location('v3', __file__.replace('continuum', 'morphology_3d'))
        v3 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v3)
        se = v3.proxy_se(c, r, a.se_frac, top, max(96, a.n_vox), np.random.default_rng(0))
        print(f'proxy SE: {len(se):,} cell-fill pts (GEOMETRY only)')
    else:
        se = np.load(a.se).astype(np.float64)
        print(f'loaded {len(se):,} SE pts from {a.se}')

    am_p, am_s, se_mask, h = voxelize(se, t, c, r, a.n_vox, top, a.se_min_count, a.denoise)
    tot = am_p.size
    am = am_p | am_s
    void = ~(am | se_mask)
    print(f'voxel grid {am_p.shape}  (h={h*UM_BOX:.3f} µm)')
    print(f'  AM {100*am.mean():.1f}%  SE {100*se_mask.mean():.1f}%  '
          f'VOID {100*void.mean():.1f}%   ← 3D porosity at this resolution')
    if a.measure_only:                                  # fast --se-min-count sweep
        return

    meshes = []
    for mask, col, name, op in ((am_p, COL[1], 'AM_P', 1.0),
                                (am_s, COL[2], 'AM_S', 1.0),
                                (se_mask, COL[3], 'SE', a.se_opacity)):
        mm = mesh_of(apply_cut(mask, a.cut), a.step)
        if mm is not None:
            meshes.append((mm, col, name, op))
            print(f'  {name}: {len(mm[1]):,} triangles')
    ntri = sum(len(f) for (v, f), *_ in meshes)
    print(f'  total {ntri:,} triangles')
    if a.engine == 'plotly' and ntri > 1_500_000:
        print('  ⚠ >1.5M triangles — HTML may be heavy; lower --n-vox or raise --step')

    (render_plotly if a.engine == 'plotly' else render_mpl)(meshes, h, a.out)


if __name__ == '__main__':
    main()
