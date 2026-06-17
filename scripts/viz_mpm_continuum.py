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
# phase palettes — 'phase' = the 2D-viewer convention; 'dem' = the DEM
# particle-render look (grey AM skeleton + khaki SE matrix) so the MPM
# continuum and the DEM render read with the same colours side by side.
PALETTES = {
    'phase': {1: '#2b2f3a', 2: '#9aa0ad', 3: '#f4d35e'},
    'dem':   {1: '#5b5b5b', 2: '#8f8f8f', 3: '#c9b88a'},
}
COL = PALETTES['phase']                                 # default; --palette overrides


def _hex_rgb(h):
    return tuple(int(h[k:k + 2], 16) for k in (1, 3, 5))


def _dilate6(mask):                                     # 6-neighbour dilation
    out = mask.copy()
    for ax in range(3):
        out |= np.roll(mask, 1, ax); out |= np.roll(mask, -1, ax)
    return out


def coverage(am_p, am_s, se_mask):
    """% of each AM type's SURFACE voxels that face SE (vs void) — the voxel
    analogue of the DEM/MPM mechanical coverage."""
    adj_non_am = _dilate6(~(am_p | am_s))
    adj_se = _dilate6(se_mask)
    res = {}
    for nm, m in (('AM_P', am_p), ('AM_S', am_s)):
        surf = m & adj_non_am
        n = int(surf.sum())
        res[nm] = 100.0 * int((surf & adj_se).sum()) / max(1, n)
    return res


def load_am(path):
    am = np.loadtxt(path, delimiter=',')
    t = am[:, 0].astype(int)
    c = np.column_stack([SW[0] + am[:, 1] * SCL,
                         SW[0] + am[:, 2] * SCL,
                         FLOOR + am[:, 3] * SCL])
    r = am[:, 4] * SCL
    return t, c, r


def voxelize(se, t, c, r, n_vox, top, se_min_count, denoise,
             target_porosity=None, target_coverage=None):
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
    free = ~am
    if target_porosity is not None:
        # The integer point-count threshold is too coarse to hit a given porosity
        # (the per-voxel counts cluster, so min_count±1 jumps the void several %p).
        # Instead pick the threshold on a lightly-smoothed (continuous) density so
        # SE = the densest free voxels and VOID = the known target EXACTLY.  The
        # smoothing also removes the salt-and-pepper, so no morphological denoise.
        from scipy import ndimage as ndi
        dens = ndi.gaussian_filter(cnt.astype(np.float32), 0.8)
        N = am.size
        n_se = int(free.sum()) - int(round(target_porosity * N))
        if n_se <= 0:
            return am_p, am_s, np.zeros_like(am), h

        def se_from_film(film):
            """SE = film ∪ densest-of-the-rest, total PINNED to n_se → porosity (and
            every volume fraction) stays fixed; the film only redistributes SE."""
            rest = free & ~film
            n_extra = n_se - int(film.sum())
            if n_extra <= 0:
                return film.copy()
            dr = dens[rest]
            thr = np.partition(dr, -n_extra)[-n_extra] if n_extra < dr.size else dr.min()
            return film | (rest & (dens >= thr))

        # interfacial candidates = non-AM voxels that touch AM and hold SE points
        cand = free & (cnt >= 1) & _dilate6(am)
        if target_coverage is not None and cand.any():
            # CALIBRATE the amount of interfacial film so AM-SE coverage matches the
            # KNOWN data value (52%) — the voxel threshold otherwise distorts it.
            # Porosity stays pinned (se_from_film holds the SE total); only the
            # bulk↔interface split moves.  Binary-search the film density cutoff.
            tgt = target_coverage * 100.0
            lo, hi = float(dens[cand].min()), float(dens[cand].max())
            se_mask = se_from_film(cand)
            for _ in range(24):
                q = 0.5 * (lo + hi)
                sm = se_from_film(cand & (dens >= q))
                cv = coverage(am_p, am_s, sm)
                if 0.5 * (cv['AM_P'] + cv['AM_S']) > tgt:
                    lo = q                            # too much film → raise cutoff
                else:
                    hi = q
                se_mask = sm
            return am_p, am_s, se_mask, h
        # default (no coverage target): keep only the film that BRIDGES AM to bulk SE
        thr0 = np.partition(dens[free], -n_se)[-n_se]
        bulk0 = (dens >= thr0) & free
        return am_p, am_s, se_from_film(cand & _dilate6(bulk0)), h
    se_mask = (cnt >= se_min_count) & free
    if denoise > 0:
        from scipy import ndimage as ndi
        se_mask = ndi.binary_closing(se_mask, iterations=denoise) & free      # fill void specks
        se_mask = ndi.binary_opening(se_mask, iterations=denoise)             # drop SE specks
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


def render_plotly(meshes, h, out, subtitle=''):
    import plotly.graph_objects as go
    s = h * UM_BOX                                       # voxel-idx → µm
    data = []
    for (v, f), col, name, op in meshes:
        data.append(go.Mesh3d(x=v[:, 0] * s, y=v[:, 1] * s, z=v[:, 2] * s,
                              i=f[:, 0], j=f[:, 1], k=f[:, 2], color=col,
                              opacity=op, name=name, showscale=False, flatshading=True,
                              # flat, near-specular-free lighting so each phase shows
                              # its TRUE colour (no blue specular sky-tint / tan wash)
                              lighting=dict(ambient=0.72, diffuse=0.6, specular=0.04,
                                            roughness=0.95, fresnel=0.0),
                              lightposition=dict(x=120, y=200, z=400)))
    fig = go.Figure(data=data)
    ttl = 'MPM composite cathode — 3D continuum'
    if subtitle:
        ttl += '<br><sub>' + subtitle + '</sub>'
    fig.update_layout(title=ttl, paper_bgcolor='white',
                      scene=dict(xaxis_title='x (µm)', yaxis_title='y (µm)',
                                 zaxis_title='z (µm)', bgcolor='white', aspectmode='data'))
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


def write_stl(path, v, f, s):
    """Per-phase binary STL (µm) — for MeshLab/Blender/CAD/3D-print."""
    tri = (v[f] * s).astype(np.float32)                 # (n,3,3)
    n = len(tri)
    e1 = tri[:, 1] - tri[:, 0]; e2 = tri[:, 2] - tri[:, 0]
    nrm = np.cross(e1, e2); ln = np.linalg.norm(nrm, axis=1, keepdims=True)
    nrm = (nrm / np.where(ln == 0, 1.0, ln)).astype(np.float32)
    blk = np.concatenate([nrm, tri.reshape(n, 9)], axis=1).astype('<f4')   # (n,12)
    rec = np.zeros((n, 50), np.uint8)
    rec[:, :48] = np.ascontiguousarray(blk).view(np.uint8).reshape(n, 48)
    with open(path, 'wb') as fh:
        fh.write(b'\0' * 80); fh.write(np.uint32(n).tobytes()); fh.write(rec.tobytes())


def write_ply(path, meshes, s):
    """Combined binary-LE PLY with per-vertex RGB (µm) — single coloured mesh
    that ParaView/MeshLab/Blender open with SE/AM in their phase colours."""
    Vs, Fs, Cs, off = [], [], [], 0
    for (v, f), col, name, op in meshes:
        Vs.append((v * s).astype('<f4')); Fs.append((f + off).astype('<i4'))
        Cs.append(np.tile(_hex_rgb(col), (len(v), 1)).astype(np.uint8)); off += len(v)
    V = np.vstack(Vs); C = np.vstack(Cs); F = np.vstack(Fs)
    vbuf = np.zeros(len(V), [('p', '<f4', 3), ('c', 'u1', 3)]); vbuf['p'] = V; vbuf['c'] = C
    fbuf = np.zeros(len(F), [('n', 'u1'), ('v', '<i4', 3)]); fbuf['n'] = 3; fbuf['v'] = F
    hdr = ("ply\nformat binary_little_endian 1.0\n"
           f"element vertex {len(V)}\nproperty float x\nproperty float y\nproperty float z\n"
           "property uchar red\nproperty uchar green\nproperty uchar blue\n"
           f"element face {len(F)}\nproperty list uchar int vertex_indices\nend_header\n")
    with open(path, 'wb') as fh:
        fh.write(hdr.encode()); fh.write(vbuf.tobytes()); fh.write(fbuf.tobytes())


def write_obj(path, meshes, s):
    """Single OBJ with one named object (`o`) per phase → COMSOL (and Blender /
    MeshLab) import each phase as a SEPARATE object/domain, so the AM_P / AM_S /
    SE groups stay split for per-domain material assignment."""
    import io
    buf = io.StringIO(); off = 0
    for (v, f), col, name, op in meshes:
        buf.write(f'o {name}\n')
        np.savetxt(buf, v * s, fmt='v %.5f %.5f %.5f')
        np.savetxt(buf, (f + 1 + off).astype(np.int64), fmt='f %d %d %d')
        off += len(v)
    with open(path, 'w') as fh:
        fh.write(buf.getvalue())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scaffold', required=True)
    ap.add_argument('--se', help='SE point cloud npy [n,3] box units (--save-se)')
    ap.add_argument('--se-proxy', action='store_true', help='no MPM: cell-fill proxy')
    ap.add_argument('--se-frac', type=float, default=0.27)
    ap.add_argument('--n-vox', type=int, default=220, help='lateral voxels (higher = finer; '
                    'plotly HTML grows with surface area — 256 is a good interactive ceiling)')
    ap.add_argument('--se-min-count', type=int, default=1, help='voxel is SE if ≥N points')
    ap.add_argument('--target-porosity', type=float, default=None,
                    help='pin VOID to this fraction EXACTLY (e.g. 0.167) via a smoothed-'
                         'density quantile — use this instead of --se-min-count, which is '
                         'too coarse to hit a given porosity (counts cluster). Also denoises.')
    ap.add_argument('--target-coverage', type=float, default=None,
                    help='also calibrate AM-SE coverage to this KNOWN value (e.g. 0.52) by '
                         'tuning how much interfacial SE film to keep — porosity stays '
                         'pinned (only the bulk↔interface SE split moves). Needs --target-porosity.')
    ap.add_argument('--denoise', type=int, default=1, help='3D close+open iters (speckle removal)')
    ap.add_argument('--cut', choices=['none', 'half', 'corner'], default='corner')
    ap.add_argument('--step', type=int, default=2, help='marching-cubes step (2 = coarser/fewer tris)')
    ap.add_argument('--se-opacity', type=float, default=0.55, help='SE matrix transparency')
    ap.add_argument('--palette', choices=['phase', 'dem'], default='phase',
                    help="'phase' = 2D-viewer colours; 'dem' = DEM-render look "
                         "(grey AM + khaki SE) for side-by-side comparison")
    ap.add_argument('--engine', choices=['plotly', 'mpl'], default='plotly')
    ap.add_argument('--mesh-out', help='also export the continuum as a mesh: '
                    'PREFIX.ply (combined, vertex-coloured) + PREFIX_{AM_P,AM_S,SE}.stl '
                    '+ PREFIX.json (phase types, coverage, porosity description)')
    ap.add_argument('--measure-only', action='store_true',
                    help='voxelise + print AM/SE/VOID %% then stop (no mesh/render) — '
                         'fast sweep to find the --se-min-count that hits true porosity')
    ap.add_argument('--out', default='mpm_continuum_3d.html')
    a = ap.parse_args()
    col_map = PALETTES[a.palette]

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

    am_p, am_s, se_mask, h = voxelize(se, t, c, r, a.n_vox, top, a.se_min_count,
                                      a.denoise, a.target_porosity, a.target_coverage)
    am = am_p | am_s
    void = ~(am | se_mask)
    por = 100.0 * void.mean()
    f_amp, f_ams, f_se = 100 * am_p.mean(), 100 * am_s.mean(), 100 * se_mask.mean()
    print(f'voxel grid {am_p.shape}  (h={h*UM_BOX:.3f} µm)')
    print(f'  AM_P {f_amp:.1f}%  AM_S {f_ams:.1f}%  SE {f_se:.1f}%  '
          f'VOID {por:.1f}%   ← 3D porosity at this resolution')
    cov = coverage(am_p, am_s, se_mask)
    print(f'  coverage by SE:  AM_P {cov["AM_P"]:.1f}%   AM_S {cov["AM_S"]:.1f}%')
    if a.measure_only:                                  # fast --se-min-count sweep
        return

    meshes = []
    for mask, col, name, op in ((am_p, col_map[1], 'AM_P', 1.0),
                                (am_s, col_map[2], 'AM_S', 1.0),
                                (se_mask, col_map[3], 'SE', a.se_opacity)):
        mm = mesh_of(apply_cut(mask, a.cut), a.step)
        if mm is not None:
            meshes.append((mm, col, name, op))
            print(f'  {name}: {len(mm[1]):,} triangles')
    ntri = sum(len(f) for (v, f), *_ in meshes)
    print(f'  total {ntri:,} triangles')
    if a.engine == 'plotly' and ntri > 1_500_000:
        print('  ⚠ >1.5M triangles — HTML may be heavy; lower --n-vox or raise --step')

    if a.mesh_out:                                       # export mesh + description
        import json
        s = h * UM_BOX
        write_ply(a.mesh_out + '.ply', meshes, s)
        print(f'  saved {a.mesh_out}.ply  (combined, vertex-coloured)')
        write_obj(a.mesh_out + '.obj', meshes, s)
        print(f'  saved {a.mesh_out}.obj  (grouped: o AM_P / o AM_S / o SE → COMSOL domains)')
        for (v, f), col, name, op in meshes:
            write_stl(f'{a.mesh_out}_{name}.stl', v, f, s)
            print(f'  saved {a.mesh_out}_{name}.stl  ({len(f):,} tris)  ← import as a domain')
        desc = {
            'source': a.se if a.se and not a.se_proxy else 'proxy(cell-fill)',
            'n_vox': a.n_vox, 'voxel_um': round(h * UM_BOX, 4),
            'se_min_count': a.se_min_count, 'denoise': a.denoise, 'cut': a.cut,
            'units': 'micrometre', 'palette': a.palette,
            'phases': {
                'AM_P': {'type': 'active material (polycrystal, dark)',
                         'volume_pct': round(f_amp, 2), 'color': col_map[1]},
                'AM_S': {'type': 'active material (single-crystal, grey)',
                         'volume_pct': round(f_ams, 2), 'color': col_map[2]},
                'SE':   {'type': 'solid electrolyte (plastic matrix, yellow/khaki)',
                         'volume_pct': round(f_se, 2), 'color': col_map[3]},
                'void': {'type': 'pore', 'volume_pct': round(por, 2)},
            },
            'porosity_pct': round(por, 2),
            'coverage_by_SE_pct': {'AM_P': round(cov['AM_P'], 2),
                                   'AM_S': round(cov['AM_S'], 2)},
            'triangles': {nm: int(len(f)) for (v, f), col, nm, op in meshes},
            'comsol': {
                'separate_domains': ['AM_P', 'AM_S', 'SE'],
                'files': {'grouped_single': a.mesh_out + '.obj (o-groups)',
                          'per_domain_stl': [f'{a.mesh_out}_{nm}.stl' for nm in
                                             ('AM_P', 'AM_S', 'SE')],
                          'coloured_combined': a.mesh_out + '.ply'},
                'import': 'OBJ keeps the 3 objects split; or import the 3 STLs and '
                          'Form Assembly + Imprint to share the AM-SE interfaces. '
                          'MC iso-surfaces are coincident at shared voxel faces.',
            },
        }
        with open(a.mesh_out + '.json', 'w') as fh:
            json.dump(desc, fh, indent=2, ensure_ascii=False)
        print(f'  saved {a.mesh_out}.json  (phase types · coverage · porosity)')

    subtitle = (f'porosity {por:.1f}%  ·  SE {f_se:.0f}%  ·  '
                f'coverage AM_P {cov["AM_P"]:.0f}% / AM_S {cov["AM_S"]:.0f}%  ·  '
                f'n_vox {a.n_vox} ({h*UM_BOX:.2f} µm/vox)')
    if a.engine == 'plotly':
        render_plotly(meshes, h, a.out, subtitle)
    else:
        render_mpl(meshes, h, a.out)


if __name__ == '__main__':
    main()
