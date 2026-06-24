#!/usr/bin/env python3
"""Build a compact webapp 3D payload for the MPM result, in the SAME JSON schema
the DEM viewer (webapp/static/js/viewer3d.js) already renders — so the webapp can
show the MPM plastic continuum with the existing viewer (just a different data URL).

The heavy SE point cloud (tens of millions of pts) is voxelised + marching-cubed
into a DECIMATED surface here (on the compute server), so the served JSON is a few
MB, not the raw cloud.  Layout:
  • AM_P / AM_S  → `particles` (spheres, exactly like the DEM viewer)
  • SE           → `mesh_triangles` (the plastic continuum surface, decimated)
  • porosity / thickness / coverage / SE-fraction → `mpm_metrics` (for the table)

  python3 scripts/mpm_webapp_payload.py --se se384_dump.npy \
      --scaffold docs/data/real14_am_scaffold.csv \
      --target-porosity 0.159 --target-coverage 0.52 \
      --n-vox 192 --tri-step 3 --out results/<case>/mpm_payload.json

Coordinates are µm with the bed corner at the origin (lateral 0..50, z 0..thickness),
matching how the DEM viewer scales atoms.csv.
"""
import argparse
import json
import importlib.util
import numpy as np

_VC = None


def _vc():
    global _VC
    if _VC is None:
        import os
        p = os.path.join(os.path.dirname(__file__), 'viz_mpm_continuum.py')
        spec = importlib.util.spec_from_file_location('vc', p)
        _VC = importlib.util.module_from_spec(spec); spec.loader.exec_module(_VC)
    return _VC


def seed_se_mask(se_csv, am_shape, h, am_mask):
    """Voxel union of D1 SE spheres at the SEED (real DEM CSV) positions, on the SAME
    grid as the compacted voxelisation, minus AM cells → the loose pre-compaction SE
    (for the before/after view).  Mapping matches viz_mpm_continuum.voxelize exactly."""
    vc = _vc(); SW = vc.SW; FLOOR = vc.FLOOR
    scl = vc.SCL                                            # case µm/box scale (overridden for thick-film)
    raw = np.loadtxt(se_csv, delimiter=',')
    c = np.column_stack([SW[0] + raw[:, 1] * scl, SW[0] + raw[:, 2] * scl, FLOOR + raw[:, 3] * scl])
    rr = raw[:, 4] * scl
    nx, ny, nz = am_shape
    mask = np.zeros(am_shape, bool)
    for i in range(len(rr)):
        cx, cy, cz = c[i]; r = float(rr[i])
        ix0 = max(0, int((cx - r - SW[0]) / h)); ix1 = min(nx, int((cx + r - SW[0]) / h) + 1)
        iy0 = max(0, int((cy - r - SW[0]) / h)); iy1 = min(ny, int((cy + r - SW[0]) / h) + 1)
        iz0 = max(0, int((cz - r - FLOOR) / h)); iz1 = min(nz, int((cz + r - FLOOR) / h) + 1)
        if ix0 >= ix1 or iy0 >= iy1 or iz0 >= iz1:
            continue
        gx = (SW[0] + (np.arange(ix0, ix1) + 0.5) * h - cx)[:, None, None]
        gy = (SW[0] + (np.arange(iy0, iy1) + 0.5) * h - cy)[None, :, None]
        gz = (FLOOR + (np.arange(iz0, iz1) + 0.5) * h - cz)[None, None, :]
        mask[ix0:ix1, iy0:iy1, iz0:iz1] |= (gx * gx + gy * gy + gz * gz <= r * r)
    return mask & ~am_mask


def deformed_coverage(se_pts, t, c, r, bands_um, n_samp=400, sub=2_000_000, seed=0):
    """Continuous SE coverage of AM from the DEFORMED MPM SE points (KDTree to the real
    plastic SE — NOT a rigid-sphere / Tabor post-correction).  Coverage is a DISTANCE
    CURVE, so this returns, in ONE KDTree pass:
      • glob[name]      = per-type mean coverage % at EACH µm band
                          (bands_um[0] = Hertz/contact ≈0.13µm, [1] = Tabor spread ≈0.26µm)
      • per_particle[i] = each AM's own coverage % at bands_um[0]  (viewer heat map)
      • patches         = the SPATIAL map — covered AM-surface points [x_um,y_um,z_um,strength]
                          in viewer coords (strength 1.0 within Hertz, 0.5 within Tabor;
                          uncovered surface dropped) → the viewer colours ONLY the covered
                          parts of each AM ('partial' surface colouring).
    The voxel-adjacency 'coverage_AM_*_mpm_pct' is density-bound (doesn't converge); this
    grid-free curve is the value we report + the DEM Hertz/Tabor cross-comparison."""
    from scipy.spatial import cKDTree
    vc = _vc(); UM = vc.UM_BOX; SW0 = vc.SW[0]; FLOOR = vc.FLOOR
    rng = np.random.default_rng(seed)
    pts = se_pts if len(se_pts) <= sub else se_pts[rng.choice(len(se_pts), sub, replace=False)]
    tree = cKDTree(pts)
    # SUBSAMPLE-INVARIANT coverage.  Each SE point represents a sub-volume of radius ~r_pt, so the SE
    # SURFACE reaches r_pt beyond a point CENTRE.  "AM surface within `band` of the SE surface" ⟺
    # nearest SE point centre within (band + r_pt).  As the cloud sparsens r_pt grows AND the
    # nearest-point distance grows by the same r_pt → the two cancel, so the coverage is the SAME at
    # 2M / 30M / all points (the value no longer depends on --cov-sub).  r_pt = ½ the median
    # nearest-neighbour spacing of the points actually used.
    _smp = pts[rng.choice(len(pts), min(4000, len(pts)), replace=False)]
    _dnn, _ = tree.query(_smp, k=2)                         # k=2: self (0) + nearest neighbour
    r_pt = 0.5 * float(np.median(_dnn[:, 1]))               # effective SE-point radius (box units)
    bands = [b / UM + r_pt for b in bands_um]               # µm→box + SE-point radius (surface, not centre)
    bh, bt = bands[0], bands[-1]                            # Hertz, Tabor (box units)
    k = np.arange(n_samp); phi = np.pi * (3 - np.sqrt(5)); z = 1 - 2 * (k + 0.5) / n_samp
    rr = np.sqrt(1 - z * z); U = np.column_stack([rr * np.cos(phi * k), rr * np.sin(phi * k), z])
    glob = {}; per_particle = np.zeros(len(r)); patches = []
    for ty, nm in ((1, 'AM_P'), (2, 'AM_S')):
        idx = np.where(t == ty)[0]; acc = np.zeros(len(bands))
        for i in idx:
            S = c[i] + r[i] * U
            d, _ = tree.query(S)
            fr = np.array([float((d < b).mean()) for b in bands])
            acc += fr; per_particle[i] = round(100.0 * float(fr[0]), 1)
            cov = np.where(d < bt)[0]
            if len(cov):
                Pout = c[i] + r[i] * 1.02 * U               # just outside surface (no z-fight)
                for j in cov:
                    patches.append([round(float((Pout[j, 0] - SW0) * UM), 2),
                                    round(float((Pout[j, 1] - SW0) * UM), 2),
                                    round(float((Pout[j, 2] - FLOOR) * UM), 2),
                                    1.0 if d[j] < bh else 0.5])
        glob[nm] = (100.0 * acc / max(len(idx), 1)).round(1).tolist()
    return glob, per_particle, patches


def geometric_coverage(am_csv, se_csv, n_samp=2000, bands_um=(0.13, 0.26)):
    """RIGID-sphere SE coverage of AM — the resolution-INVARIANT reference (analytic spheres, no
    point cloud / subsample / n_vox; stable to 0.1%p over n_samp 800..10000).  Fraction of each AM
    surface within bands_um[0]/[1] (µm) of an SE SPHERE SURFACE (gap = d_centre − r_SE).  Compare to
    the DEFORMED-SE coverage (deformed_coverage at all points) at the SAME bands → the difference is
    the plastic conforming the MPM adds over rigid spheres."""
    from scipy.spatial import cKDTree
    am = np.loadtxt(am_csv, delimiter=','); se = np.loadtxt(se_csv, delimiter=',')
    tree = cKDTree(se[:, 1:4]); r_se = float(se[0, 4])
    b0, b1 = bands_um[0] / 1000.0, bands_um[1] / 1000.0     # µm → LIGGGHTS units (1 u = 1000 µm)
    k = np.arange(n_samp); phi = np.pi * (3 - np.sqrt(5)); z = 1 - 2 * (k + 0.5) / n_samp
    rr = np.sqrt(1 - z * z); U = np.column_stack([rr * np.cos(phi * k), rr * np.sin(phi * k), z])
    out = {}
    for ty, nm in ((1, 'AM_P'), (2, 'AM_S')):
        m = am[:, 0].astype(int) == ty
        C = am[m, 1:4]; R = am[m, 4]
        if not len(C):
            out[nm] = None; continue
        h = t = 0.0
        for i in range(len(C)):
            d, _ = tree.query(C[i] + R[i] * U); gap = d - r_se
            h += float((gap < b0).mean()); t += float((gap < b1).mean())
        out[nm] = {'hertz': round(100 * h / len(C), 1), 'tabor': round(100 * t / len(C), 1)}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scaffold', default='', help='AM scaffold CSV (type,x,y,z,r); omit for an SE-only '
                    'payload (loose→dense demo — no AM particles, just the SE continuum + strain)')
    ap.add_argument('--se', help='SE point cloud npy [n,3] box units (--save-se)')
    ap.add_argument('--se-proxy', action='store_true', help='no MPM run: cell-fill proxy (test)')
    ap.add_argument('--se-dump', default='', help='SE seed CSV (real DEM positions): adds the '
                    'loose PRE-compaction SE surface as seed_mesh_triangles for the before/after view')
    ap.add_argument('--se-frac', type=float, default=0.27)
    ap.add_argument('--n-vox', type=int, default=192, help='voxel resolution for the SE surface')
    ap.add_argument('--void-max', type=int, default=180000, help='max void (pore) voxel centres carried for '
                    'the XCT-like "기공만" viewer mode (0 = off). Pore = electrode-envelope cells not AM/SE.')
    ap.add_argument('--tri-step', type=int, default=3,
                    help='marching-cubes step for the SERVED mesh (3 ≈ browser-friendly tri count)')
    ap.add_argument('--target-porosity', type=float, default=None)
    ap.add_argument('--target-coverage', type=float, default=None)
    ap.add_argument('--se-min-count', type=int, default=1)
    ap.add_argument('--denoise', type=int, default=1)
    ap.add_argument('--smooth', type=float, default=1.0)
    ap.add_argument('--case', default='', help='case id (stored in payload meta)')
    ap.add_argument('--porosity', type=float, default=None,
                    help='AUTHORITATIVE porosity %% (from the sim, e.g. 15.93) — overrides the '
                         'mesh-resolution recompute, which is coarse-voxel biased')
    ap.add_argument('--thickness', type=float, default=None,
                    help='AUTHORITATIVE thickness µm (sim wall_z, e.g. 29.95) — the continuum box '
                         'height is NOT the compacted thickness')
    ap.add_argument('--cov-p', type=float, default=None, help='AUTHORITATIVE AM_P coverage %% (fine-res, e.g. 50)')
    ap.add_argument('--cov-s', type=float, default=None, help='AUTHORITATIVE AM_S coverage %% (fine-res, e.g. 53)')
    ap.add_argument('--metrics-json', default='',
                    help='RAW MPM metrics JSON from mpm3d_compaction --save-metrics: its authoritative '
                         'porosity/thickness/coverage/density are used instead of the coarse-mesh recompute')
    ap.add_argument('--coverage-um', type=float, default=0.13,
                    help='Hertz/contact band (µm) for the deformed-points coverage curve '
                         '(≈ DEM elastic ~0.13µm).  Also the per-AM-particle coverage band.')
    ap.add_argument('--cov-tabor-um', type=float, default=0.26,
                    help='Tabor plastic-spread band (µm) for the coverage curve (≈ DEM plastic ~0.26µm).')
    ap.add_argument('--cov-sub', type=int, default=0,
                    help='SE points in the PLASTIC (deformed) coverage KD-tree.  0 = ALL points (default) '
                         '= the CONVERGED value (subsample is the only knob that moves it: 6→45→70 as the '
                         'dense thick-film surface is under/fully-resolved).  Set e.g. 12000000 for a quick '
                         'preview.  The RIGID geometric reference is analytic and always exact.')
    ap.add_argument('--dg', default='', help='accumulated PLASTIC strain npy (mpm3d --save-dg) → SE strain points')
    ap.add_argument('--eps', default='', help='accumulated TOTAL strain npy (mpm3d --save-eps) — deformation vs the '
                    'seed sphere (incl elastic compression of the confined interior); PREFERRED over --dg')
    ap.add_argument('--strain-pts', type=int, default=200000, help='max SE strain points carried in the payload')
    ap.add_argument('--phase', default='', help='per-point phase npy (mpm3d --save-phase): 1 SE · 2 VGCF · '
                    '3 SuperP · 4 PTFE, SAME order as --se.  Splits the cloud → SE meshed as the continuum, '
                    'conductive additives carried as colored points (additive_points) for the 도전재 3D viewer.')
    ap.add_argument('--additive-pts', type=int, default=120000, help='max additive points carried in the payload')
    ap.add_argument('--fibre', default='', help='per-point fibre-id npy (mpm3d --save-fibre): group VGCF/PTFE '
                    'points into individual fibre polylines (additive_fibres) so the viewer can draw each fibre '
                    'as a line/rod instead of a point cloud.')
    ap.add_argument('--fibre-max', type=int, default=4000, help='max fibres carried as polylines (subsample)')
    ap.add_argument('--fibre-dia', default='', help='per-point relative fibre diameter npy (mpm3d '
                    '--save-fibre-dia): attach per-fibre median Ø to additive_fibres so the viewer renders '
                    'thickness (PTFE draw d∝√(V/L) — thin-long vs thick-short).')
    ap.add_argument('--out', default='mpm_payload.json')
    a = ap.parse_args()
    vc = _vc()
    sim_m = json.load(open(a.metrics_json)) if a.metrics_json else {}
    # thick-film / non-50µm-lateral: the viewer hardcodes a 50µm cube (vc.SCL / vc.UM_BOX).  Override
    # with the case's REAL µm-per-box so AM (LIGGGHTS units → box) aligns with the SE point cloud
    # (already box units) and the coverage distance bands are in true µm.  Prefer the sim's um_box_um;
    # else derive it EXACTLY from thickness/(wall_z − FLOOR) (both in the metrics) for older payloads.
    _umb = sim_m.get('um_box_um')
    if not _umb:
        _th, _wz = sim_m.get('thickness_um'), sim_m.get('wall_z')
        if _th and _wz and (_wz - vc.FLOOR) > 1e-9:
            _umb = _th / (_wz - vc.FLOOR)
    if _umb:
        vc.UM_BOX = float(_umb); vc.SCL = 1000.0 / float(_umb)
    UM = vc.UM_BOX; SW = vc.SW; FLOOR = vc.FLOOR

    if a.scaffold:
        t, c, r = vc.load_am(a.scaffold)
    else:                                                  # SE-only payload (loose→dense demo, no AM)
        t, c, r = np.zeros(0, int), np.zeros((0, 3)), np.zeros(0)
    if a.se_proxy or not a.se:
        top = float((c[:, 2] + r).max()) + 0.01            # proxy fill needs the AM skeleton
        v3p = importlib.util.spec_from_file_location(
            'v3', __file__.replace('mpm_webapp_payload', 'viz_mpm_morphology_3d'))
        v3 = importlib.util.module_from_spec(v3p); v3p.loader.exec_module(v3)
        se = v3.proxy_se(c, r, a.se_frac, top, max(96, a.n_vox), np.random.default_rng(0))
        print(f'proxy SE: {len(se):,} pts (test only)')
    else:
        se = np.load(a.se).astype(np.float64)
        print(f'loaded {len(se):,} SE pts from {a.se}')
        top = (float((c[:, 2] + r).max()) if len(r) else float(se[:, 2].max())) + 0.01

    # phase split: VGCF/PTFE/SuperP are EXTRA material points appended to the SE cloud (same order as
    # --save-se).  The SE continuum mesh + AM coverage must use the TRUE SE only (phase==1) — meshing the
    # additives would fuse the carbon into the SE surface.  Additives are carried separately as points.
    phase = None
    if a.phase:
        phase = np.load(a.phase)
        if len(phase) != len(se):
            print(f'  ⚠ phase length {len(phase)} != SE {len(se)} — ignoring --phase')
            phase = None
    se_se = se[phase == 1] if phase is not None else se        # true SE for continuum mesh + coverage

    am_p, am_s, se_mask, h = vc.voxelize(se_se, t, c, r, a.n_vox, top, a.se_min_count,
                                         a.denoise, a.target_porosity, a.target_coverage)
    am = am_p | am_s
    por = 100.0 * (~(am | se_mask)).mean()
    f_se = 100.0 * se_mask.mean()
    cov = vc.coverage(am_p, am_s, se_mask)
    s = h * UM                                             # voxel idx → µm

    # void (pore) phase → XCT-like "기공만" viewer mode: INTERNAL pore = complement of solid (AM ∪ SE)
    # BELOW the per-column electrode top surface, as a subsampled voxel-centre cloud (same µm frame as
    # the SE mesh / AM / additive_points).  Capping at each column's highest solid cell drops (a) the
    # empty HEADSPACE above the rough electrode top (the "SE 없는 위층") and (b) fully-empty periodic-edge
    # columns — so only real internal pores show, not the box void around/above the sample.  Additives
    # (~4 vol%, sub-grid, sit INSIDE the pores) are NOT subtracted → macro-pore network as XCT segments it.
    void_points = []
    if a.void_max > 0:
        solid = am | se_mask                               # (nx, ny, nz)
        nzc = solid.shape[2]
        has = solid.any(axis=2)                            # columns containing any solid
        ztop = np.where(has, nzc - 1 - np.argmax(solid[:, :, ::-1], axis=2), -1)   # highest solid z per column
        zz = np.arange(nzc)[None, None, :]
        void = (~solid) & (zz <= ztop[:, :, None])         # pore below the column top; headspace/empty cols dropped
        vi = np.argwhere(void)
        nvoid = len(vi)
        if nvoid > a.void_max:
            vi = vi[np.random.default_rng(3).choice(nvoid, a.void_max, replace=False)]
        void_points = ((vi + 0.5) * s).astype(np.float32).round(2).tolist()
        print(f'  void (pore) cloud: {len(void_points):,} of {nvoid:,} internal-pore voxels '
              f'(headspace + empty periodic-edge columns capped; raw void {int((~solid).sum()):,})')

    # SE continuum surface (decimated for the browser)
    mm = vc.mesh_of(se_mask, a.tri_step, a.smooth)
    tris = []
    if mm is not None:
        v, f = mm
        vu = (v * s).astype(np.float32)                    # µm, origin at bed corner
        tris = vu[f].round(3).tolist()                     # [[ [x,y,z]×3 ], ...]
    print(f'  SE surface: {len(tris):,} triangles (n_vox={a.n_vox}, step={a.tri_step})')

    # SE plastic-strain point cloud (subsampled) → the viewer's "SE Σdg" mode colours the
    # 3D SE by accumulated plastic strain (the field the 2D morphology shows, now in 3D).
    se_strain_points = []; strain_stats = {}
    strain_npy = a.eps or a.dg                             # TOTAL (vs seed) preferred over PLASTIC
    if strain_npy:
        sv = np.load(strain_npy).astype(np.float64)
        kind = 'total (vs seed)' if a.eps else 'plastic Σdg'
        if len(sv) == len(se):
            N = min(a.strain_pts, len(se))
            idx = (np.random.default_rng(0).choice(len(se), N, replace=False)
                   if len(se) > N else np.arange(len(se)))
            Ps = se[idx]
            xyzdg = np.column_stack([((Ps[:, 0] - SW[0]) * UM).round(2),
                                     ((Ps[:, 1] - SW[0]) * UM).round(2),
                                     ((Ps[:, 2] - FLOOR) * UM).round(2), sv[idx].round(4)])
            se_strain_points = xyzdg.tolist()
            pos = sv[sv > 0]
            strain_stats = {'dg_mean': round(float(sv.mean()), 4), 'dg_max': round(float(sv.max()), 3),
                            'dg_vmax98': round(float(np.percentile(pos, 98)), 4) if len(pos) else 0.0,
                            'dg_nonzero_pct': round(100.0 * float((sv > 0).mean()), 1),
                            'n_strain_pts': len(se_strain_points), 'strain_kind': kind}
            print(f'  SE strain points: {len(se_strain_points):,}  ({kind}: mean {strain_stats["dg_mean"]} '
                  f'max {strain_stats["dg_max"]} vmax98 {strain_stats["dg_vmax98"]})')
        else:
            print(f'  ⚠ strain npy length {len(sv)} != SE {len(se)} — skipping strain points')

    # seed (loose, pre-compaction) SE surface — the real DEM SE spheres on the same grid
    seed_tris = []
    seed_por = None
    if a.se_dump:
        seed_mask = seed_se_mask(a.se_dump, am_p.shape, h, am)
        seed_por = 100.0 * (~(am | seed_mask)).mean()
        smm = vc.mesh_of(seed_mask, a.tri_step, a.smooth)
        if smm is not None:
            sv, sf = smm
            seed_tris = (sv * s).astype(np.float32)[sf].round(3).tolist()
        print(f'  SEED SE surface: {len(seed_tris):,} triangles  (loose void {seed_por:.1f}%)')

    # AM particles (spheres) in µm, origin at bed corner — same schema as DEM viewer
    # per-particle coverage (each AM's own SE coverage, from the DEFORMED SE points) →
    # the viewer can colour each AM sphere by its coverage (a per-particle heat map).
    # PLASTIC coverage = the DEFORMED SE (the MPM result, SE conformed to the AM), measured at ALL
    # points (--cov-sub 0) so it's CONVERGED — the subsample was the only knob that moved it (6→45→70).
    # RIGID coverage = geometric SE SPHERES at the SAME bands (analytic, resolution-invariant reference).
    # Reporting BOTH makes the MPM's contribution explicit: plastic − rigid = the conforming the soft SE
    # adds over rigid spheres (the rigid leaves interface gaps the plastic SE fills).
    cov_bands, cov_per, cov_patches = deformed_coverage(se_se, t, c, r, [a.coverage_um, a.cov_tabor_um],
                                                        sub=(a.cov_sub or len(se_se)))
    geom_rigid = (geometric_coverage(a.scaffold, a.se_dump, bands_um=(a.coverage_um, a.cov_tabor_um))
                  if (a.scaffold and a.se_dump) else None)
    def _rigid(nm, which):                                 # geometric rigid-sphere reference (or None)
        if geom_rigid and geom_rigid.get(nm):
            return geom_rigid[nm]['hertz'] if which == 'h' else geom_rigid[nm]['tabor']
        return None
    name = {1: 'AM_P', 2: 'AM_S'}
    particles = [{'id': int(i), 'type': name.get(int(t[i]), 'AM'),
                  'x': round(float((c[i, 0] - SW[0]) * UM), 3),
                  'y': round(float((c[i, 1] - SW[0]) * UM), 3),
                  'z': round(float((c[i, 2] - FLOOR) * UM), 3),
                  'r': round(float(r[i] * UM), 3),
                  'coverage': float(cov_per[i])} for i in range(len(r))]

    # conductive additives (VGCF/SuperP/PTFE) → colored points for the 도전재 3D viewer.  Subsampled
    # proportionally to the budget; carried as [x,y,z,phase] µm (phase 2 VGCF · 3 SuperP · 4 PTFE).
    additive_points = []
    additive_counts = {}
    if phase is not None:
        rng_a = np.random.default_rng(1)
        add_tot = int((phase >= 2).sum())
        for code, nm in ((2, 'VGCF'), (3, 'SuperP'), (4, 'PTFE')):
            m = phase == code
            cnt = int(m.sum())
            if cnt == 0:
                continue
            additive_counts[nm] = cnt
            P = se[m]
            budget = max(1, int(a.additive_pts * cnt / max(add_tot, 1)))
            if len(P) > budget:
                P = P[rng_a.choice(len(P), budget, replace=False)]
            xyz = np.column_stack([((P[:, 0] - SW[0]) * UM).round(2), ((P[:, 1] - SW[0]) * UM).round(2),
                                   ((P[:, 2] - FLOOR) * UM).round(2), np.full(len(P), code, np.float64)])
            additive_points.extend(xyz.tolist())
        if additive_counts:
            print('  additives → ' + '  '.join(
                f'{nm} {c:,}pts→{min(c, max(1, int(a.additive_pts * c / max(add_tot, 1)))):,} shown'
                for nm, c in additive_counts.items()))

    # individual fibres (VGCF/PTFE) → polylines, so the viewer can draw each as a line/rod (SE = continuum,
    # but a fibre is a discrete object).  Group fibre points by id (stable sort keeps the along-axis order).
    additive_fibres = []
    if a.fibre and phase is not None:
        fid = np.load(a.fibre)
        dia = None
        if a.fibre_dia:                                      # per-point relative Ø (PTFE draw d∝√(V/L))
            dia = np.load(a.fibre_dia)
            if len(dia) != len(se):
                print(f'  ⚠ fibre-dia length {len(dia)} != SE {len(se)} — ignoring --fibre-dia')
                dia = None
        if len(fid) != len(se):
            print(f'  ⚠ fibre length {len(fid)} != SE {len(se)} — ignoring --fibre')
        else:
            fib_mask = (phase >= 2) & (fid >= 0)
            uniq = np.unique(fid[fib_mask])
            n_fib_total = len(uniq)
            if len(uniq) > a.fibre_max:
                uniq = np.random.default_rng(2).choice(uniq, a.fibre_max, replace=False)
            keep = fib_mask & np.isin(fid, uniq)
            idx = np.where(keep)[0]
            order = np.argsort(fid[idx], kind='stable')      # group by fibre, preserve along-axis order
            idx = idx[order]
            fsorted = fid[idx]
            splits = np.where(np.diff(fsorted) != 0)[0] + 1
            for grp in np.split(idx, splits):
                if len(grp) < 2:
                    continue
                coords = np.column_stack([((se[grp, 0] - SW[0]) * UM), ((se[grp, 1] - SW[0]) * UM),
                                          ((se[grp, 2] - FLOOR) * UM)]).round(2)
                rec = {'phase': int(phase[grp[0]]), 'pts': coords.tolist()}
                if dia is not None:                          # per-fibre relative thickness → viewer line width
                    rec['d'] = round(float(np.median(dia[grp])), 3)
                additive_fibres.append(rec)
            print(f'  additive_fibres: {len(additive_fibres)} fibres as polylines (of {n_fib_total} total)'
                  + ('' if dia is None else f'  Ø rel {min(f["d"] for f in additive_fibres):.2f}'
                     f'..{max(f["d"] for f in additive_fibres):.2f}'))

    lat = (SW[1] - SW[0]) * UM
    thick = (top - FLOOR) * UM

    # authoritative metrics: prefer the sim's --metrics-json (raw, computed at sim grid res),
    # then explicit overrides, then the (coarse-mesh-biased) recompute as a last resort.
    # (sim_m was already loaded above, where it set the µm/box scale for thick-film cases.)

    def pick(override, sim_key, computed):
        if override is not None:
            return override
        if sim_m.get(sim_key) is not None:
            return sim_m[sim_key]
        return computed
    mpm_metrics = {
        'porosity_mpm_pct': round(pick(a.porosity, 'porosity_settled_pct', por), 2),
        'thickness_mpm_um': round(pick(a.thickness, 'thickness_um', thick), 2),
        'coverage_AM_P_mpm_pct': round(pick(a.cov_p, 'coverage_AM_P_pct', cov['AM_P']), 1),
        'coverage_AM_S_mpm_pct': round(pick(a.cov_s, 'coverage_AM_S_pct', cov['AM_S']), 1),
        'se_fraction_pct': round(sim_m.get('SE_of_solid_pct', f_se), 2),
        'n_am': len(particles), 'se_surface_tris': len(tris), 'n_vox': a.n_vox,
        # coverage within Hertz/Tabor µm of the SE surface.  PLASTIC = deformed SE (MPM, all points);
        # RIGID = geometric SE spheres (reference).  plastic − rigid = the MPM plastic conforming.
        'coverage_AM_P_hertz_pct': cov_bands['AM_P'][0], 'coverage_AM_P_tabor_pct': cov_bands['AM_P'][1],
        'coverage_AM_S_hertz_pct': cov_bands['AM_S'][0], 'coverage_AM_S_tabor_pct': cov_bands['AM_S'][1],
        'coverage_AM_P_rigid_hertz_pct': _rigid('AM_P', 'h'), 'coverage_AM_P_rigid_tabor_pct': _rigid('AM_P', 't'),
        'coverage_AM_S_rigid_hertz_pct': _rigid('AM_S', 'h'), 'coverage_AM_S_rigid_tabor_pct': _rigid('AM_S', 't'),
        'cov_hertz_um': a.coverage_um, 'cov_tabor_um': a.cov_tabor_um,   # distance bands (0.13/0.26µm)
        'cov_method': 'plastic_deformed_vs_rigid_geometric' if geom_rigid else 'deformed_points',
    }
    # coverage_AM_*_mpm_pct = the sim's RAW value (the MPM DIRECTLY measures the plastic SE-AM
    # contact from the deformed SE — no Tabor/B3 post-correction, which would re-impose the DEM's
    # rigid-sphere fix on a model that already deformed plastically).  Compared in /group against
    # the DEM's Hertz (18) / Tabor (48); the disagreement is the quantified DEM↔MPM model gap.
    if seed_por is not None:
        sim_seed = None                                             # prefer the sim's authoritative seed void
        if sim_m.get('seed_AM_frac_pct') is not None and sim_m.get('seed_SE_frac_pct') is not None:
            sim_seed = 100.0 - sim_m['seed_AM_frac_pct'] - sim_m['seed_SE_frac_pct']
        mpm_metrics['seed_porosity_pct'] = round(sim_seed if sim_seed is not None else seed_por, 2)
        mpm_metrics['compacted_porosity_pct'] = mpm_metrics['porosity_mpm_pct']
    for k in ('E_SE_GPa', 'nu_SE', 'sigma_y_GPa', 'K_SE_GPa', 'final_stress_GPa', 'target_GPa',
              'bulk_density_g_cm3', 'seed_AM_frac_pct', 'seed_SE_frac_pct', 'n_grid', 'protocol'):
        if k in sim_m:
            mpm_metrics[k] = sim_m[k]                       # carry through raw sim fields
    mpm_metrics.update(strain_stats)                       # Σdg mean/max/vmax98/n_strain_pts (if --dg)
    if additive_counts:
        mpm_metrics['additive_counts'] = additive_counts   # {VGCF:n, SuperP:n, PTFE:n} total seeded

    payload = {
        'kind': 'mpm', 'case': a.case,
        'particles': particles,                            # AM_P / AM_S spheres (same both states)
        'am_coverage_patches': cov_patches,                # covered AM-surface points (spatial map)
        'se_strain_points': se_strain_points,              # [x,y,z,Σdg] µm — viewer "SE 소성변형" mode
        'mesh_triangles': tris,                            # COMPACTED SE plastic continuum (default)
        'seed_mesh_triangles': seed_tris,                  # loose SE before compaction (before/after)
        'additive_points': additive_points,                # [x,y,z,phase] µm — VGCF(2)/SuperP(3)/PTFE(4)
        'additive_fibres': additive_fibres,                # [{phase, pts:[[x,y,z],…]}] — VGCF/PTFE as polylines
        'void_points': void_points,                        # [x,y,z] µm — pore voxel centres (XCT "기공만" mode)
        'box': {'x_min': 0.0, 'x_max': round(lat, 2), 'y_min': 0.0, 'y_max': round(lat, 2),
                'z_min': 0.0, 'z_max': round(thick, 2)},
        'atoms_only': False,
        'mpm_metrics': mpm_metrics,
        'mpm_source': {'se': a.se or 'proxy', 'scaffold': a.scaffold, 'metrics_json': a.metrics_json,
                       'target_porosity': a.target_porosity, 'target_coverage': a.target_coverage,
                       'smooth': a.smooth},
    }
    with open(a.out, 'w') as fh:
        json.dump(payload, fh)
    import os
    _mp = mpm_metrics                                      # AUTHORITATIVE table values (sim porosity/
    #   thickness/SE-of-solid + converged plastic coverage vs rigid reference) — NOT the n_vox
    #   voxel-preview (por/f_se/cov), which re-discretise the point cloud and vary with --n-vox.
    rh, rt = _mp.get('coverage_AM_P_rigid_hertz_pct'), _mp.get('coverage_AM_P_rigid_tabor_pct')
    cov_str = f"AM_P plastic {_mp['coverage_AM_P_hertz_pct']:.0f}/{_mp['coverage_AM_P_tabor_pct']:.0f}%"
    if rh is not None:
        cov_str += (f" vs rigid {rh:.0f}/{rt:.0f}% (Δ +{_mp['coverage_AM_P_hertz_pct']-rh:.0f}/"
                    f"+{_mp['coverage_AM_P_tabor_pct']-rt:.0f} = plastic conforming)")
    print(f'saved {a.out}  ({os.path.getsize(a.out)/1e6:.1f} MB)  '
          f'porosity {_mp["porosity_mpm_pct"]:.1f}% · SE/solid {_mp["se_fraction_pct"]:.1f}% · '
          f'thickness {_mp["thickness_mpm_um"]:.1f}µm · coverage(@{a.coverage_um}/{a.cov_tabor_um}µm) {cov_str} · '
          f'{len(particles)} AM · {len(tris):,} SE tris (n_vox={a.n_vox})'
          f'  [voxel-preview por/SE/cov {por:.0f}/{f_se:.0f}/{cov["AM_P"]:.0f}% vary with n_vox — not reported]')


if __name__ == '__main__':
    main()
