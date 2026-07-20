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


def seed_se_mask(se_csv, am_shape, h, am_mask, dz=1.0):
    """Voxel union of D1 SE spheres at the SEED (real DEM CSV) positions, on the SAME
    grid as the compacted voxelisation, minus AM cells → the loose pre-compaction SE
    (for the before/after view).  Mapping matches viz_mpm_continuum.voxelize exactly.
    dz = the MPM's --dilate-z scaffold stretch (payload must live on the same frame)."""
    vc = _vc(); SW = vc.SW; FLOOR = vc.FLOOR
    scl = vc.SCL                                            # case µm/box scale (overridden for thick-film)
    raw = np.loadtxt(se_csv, delimiter=',')
    c = np.column_stack([SW[0] + raw[:, 1] * scl, SW[0] + raw[:, 2] * scl, FLOOR + raw[:, 3] * scl * dz])
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


def electronic_connectivity(t, c, r, se, phase, floor_z, um,
                            tol_am_um=0.10, band_um=0.15, vox_um=0.30, cond_phases=(2, 3, 5)):
    """Per-AM ELECTRONIC connectivity to the current collector (floor) — the slide-19 quantity
    (연결/고립 입자).  Zeroth-order electron-transport physics = PERCOLATION on the conductive
    phases only:
      nodes  = AM spheres ∪ conductive-carbon clusters (phase 2 VGCF / 3 SuperP / 5 SDCP)
      edges  = AM–AM mechanical contact (surface gap ≤ tol_am — Holm: contact spot = conduction
               spot, mirrors the DEM σ_e network criterion)
             ∪ AM–carbon contact (carbon point within band of the AM surface = the add-cov
               contact we measure; carbon σ_e ≫ σ_AM so the bridge is never the bottleneck
               at connectivity level)
      carbon clusters: full-res material points voxel-labeled at vox_um (26-conn) — one
               continuous fibre/web/aggregate = one conductor; touching carbon conducts.
      connected := component reaches the collector (AM bottom or carbon within tol of z=floor).
    EXCLUDED (physics): SE = electronic insulator (~1e-9 S/cm, by design); PTFE (phase 4) =
    insulating binder (~1e-16 S/cm).  BINARY percolation only — NO σ numbers (that is STEP3
    Kirchhoff with contact resistances); an AM with no electron path is electrochemically DEAD
    regardless of its ionic wiring (= the DEM dead-AM concept, extended to carbon-mediated paths).
    MUST run on FULL-RES arrays (se+phase before subsampling): the served 120k-point subsample
    stretches fibre point spacing ~0.14→~4µm and would falsely fragment conductors."""
    from scipy import ndimage
    from scipy.spatial import cKDTree
    n = len(r)
    parent = np.arange(n + 1, dtype=np.int64)               # node n = the current collector

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = int(parent[i])
        return i

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    tol = tol_am_um / um; band = band_um / um
    if n:
        tree = cKDTree(c)
        for i, j in tree.query_pairs(2.0 * float(r.max()) + tol):
            if np.linalg.norm(c[i] - c[j]) <= r[i] + r[j] + tol:
                union(int(i), int(j))                        # (a) AM–AM contact
        for i in np.where(c[:, 2] - r <= floor_z + tol)[0]:
            union(int(i), n)                                 # AM on the collector
    n_cl = 0
    if phase is not None and n:
        cond = se[np.isin(phase, cond_phases)]               # conductive phases only (NOT PTFE 4; SDCP 5 KEPT even
        #   when neutral — AM-grade weak conductor; insulator-drop would misclassify ~13 orders (see caller 419+)
        if len(cond):
            vox = vox_um / um                                # ≥2× the 0.7·dx point spacing → one
            lo = cond.min(0) - vox                           #   continuous fibre labels as one cluster
            ijk = np.floor((cond - lo) / vox).astype(np.int64)
            grid = np.zeros(ijk.max(0) + 2, bool)
            grid[ijk[:, 0], ijk[:, 1], ijk[:, 2]] = True
            lab, n_cl = ndimage.label(grid, structure=np.ones((3, 3, 3), bool))
            plab = lab[ijk[:, 0], ijk[:, 1], ijk[:, 2]]      # per-point cluster id 1..n_cl
            parent = np.concatenate([parent, n + 1 + np.arange(n_cl, dtype=np.int64)])
            ct = cKDTree(cond)
            for i in range(n):                               # (b) AM–carbon attach
                idx = ct.query_ball_point(c[i], float(r[i]) + band)
                if idx:
                    for lb in np.unique(plab[idx]):
                        union(int(i), n + int(lb))
            fl = np.where(cond[:, 2] <= floor_z + band)[0]   # carbon on the collector
            if len(fl):
                for lb in np.unique(plab[fl]):
                    union(n, n + int(lb))
    root_cc = find(n)
    econn = np.array([find(i) == root_cc for i in range(n)], bool)
    return econn, int(n_cl)


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
    ap.add_argument('--dilate-z', type=float, default=1.0,
                    help='scaffold z-stretch the MPM ran with (--dilate-z there): rebuild AM + seed-SE on the '
                         'SAME dilated frame — else coverage/viewer compare the dilated se_dump.npy against '
                         'un-dilated spheres (up-to-µm z mismatch at the bed top).')
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
    # ★ STEP3 v1 — electronic voxel resistor network (σ_e_eff + per-AM current density).  RELATIVE
    # trust unit; σ table: AM = A1-locked (Trevisanello 10/5 mS/cm), carbon/SDCP = §F1 order-of-
    # magnitude hooks (record travels in metrics.step3.sigma_table so runs are comparable).
    ap.add_argument('--no-step3', action='store_true', help='skip the STEP3 σ_e network solve')
    ap.add_argument('--step3-vox', type=float, default=0.4,
                    help='STEP3 voxel size (µm).  0.4 default: AM-carbon bridges (band 0.15µm) land in '
                         'same/adjacent voxels; smaller = finer necks but ∝1/vox³ dof.')
    ap.add_argument('--sigma-am-s', type=float, default=0.010, help='σ_e AM_S (S/cm) — A1-locked 10 mS/cm')
    ap.add_argument('--sigma-am-p', type=float, default=0.005, help='σ_e AM_P (S/cm) — A1-locked 5 mS/cm')
    ap.add_argument('--sigma-vgcf', type=float, default=100.0, help='σ_e VGCF (S/cm) — lit order ⚠hook')
    ap.add_argument('--sigma-superp', type=float, default=10.0, help='σ_e SuperP (S/cm) — lit order ⚠hook')
    ap.add_argument('--sigma-sdcp', type=float, default=250.0,
                    help='σ_e SDCP material (S/cm) — 250 = USER-provided anchor UPDATE (2026-07-16, '
                         'supersedes interim 150 of 2026-07-10, S-PEDOT-class); pellet ×5.1 stays '
                         'COMPOSITE-level.  Doped/neutral split = future.')
    ap.add_argument('--sigma-ptfe', type=float, default=0.0,
                    help='σ_e PTFE (S/cm) — SENSITIVITY hook (default 0 = production: PTFE는 전도 격자에 '
                         '아예 미스탬프, bulk PTFE ~1e-16 S/cm 절연체).  >0이면 PTFE phase-4 점을 sid7로 '
                         '스탬프해 전자망에 참여시킴 — "절연 가정이 결과를 만들었나" 반론 검증용 '
                         '(랩 논의 2026-07-14, 0.58 S/cm 제안값의 출처는 미확인 ⚠).  이온은 항상 절연.')
    ap.add_argument('--sigma-ion-se', type=float, default=0.003,
                    help='σ_ion SE (S/cm) = 3.0 mS/cm LPSCl grain (Cronau — production σ_grain anchor)')
    ap.add_argument('--collector-rint', type=float, default=-1.0,
                    help='SELECTED collector R_int (Ω·cm², manuscript Fig6e cycled anchors: bare-Al SBE '
                         '110 / DBE 46 / C-SUS primer 30; 0 = ideal).  <0 = no selection (presets still '
                         'reported).  Applied as a uniform areal series term (post-processing).')
    ap.add_argument('--collector-name', default='', help='label for the selected collector preset')
    ap.add_argument('--sigma-ion-sdcp', type=float, default=0.001,
                    help='σ_ion SDCP (S/cm) — NOT an ion-insulator (user principle: Li-hopping keeps it '
                         'conducting; pellet ×0.80 vs PTFE ×0.27).  1 mS/cm ⚠F1 hook; Li⁺ DFT 패키지가 앵커 예정.')
    ap.add_argument('--field-max-points', type=int, default=90000,
                    help='max points per current-density FIELD cloud (electronic=AM+carbon, ionic=SE+SDCP). '
                         'High for paper figures; ~90k/field ≈ a few MB JSON.  Hottest 35%% always kept.')
    ap.add_argument('--no-field', action='store_true',
                    help='skip the STEP3 current-density FIELD export (electronic_field / ionic_field)')
    ap.add_argument('--step3-gpu', action='store_true',
                    help='run the STEP3 Kirchhoff CG on GPU (CuPy cuSPARSE) — ~10-50× faster, esp. fine '
                         'vox; auto-falls back to scipy CPU if CuPy/CUDA missing (same σ either way).')
    ap.add_argument('--i0-a-m2', type=float, default=2.0,
                    help='STEP4 exchange current density i0 (A/m², NCM|LPSCl 계면) — ⚠F1 literature hook '
                         '(Newman-typical 1-5 A/m²).  Sets the linearised BV conductance g=i0·F/RT.')
    ap.add_argument('--no-step4', action='store_true',
                    help='skip the STEP4 reaction-current solve (저율 충전 반응전류 분포, slide-20 물리)')
    ap.add_argument('--save-step4-grid', default='',
                    help='STEP4-v2(시간전개) 입력 격자 npz 저장: sid/pid/σ_e·σ_i테이블/vox/z_top/AM반경 '
                         '— scripts/step4_dyn.py --grid 로 로드 (payload 재실행 없이 rate 스윕)')
    a = ap.parse_args()
    if a.save_step4_grid and not a.save_step4_grid.endswith('.npz'):
        a.save_step4_grid += '.npz'                      # savez 자동 append와 소비자(--grid) 일관화
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
        t, c, r = vc.load_am(a.scaffold, dz=a.dilate_z)
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
    # BELOW the GLOBAL electrode top surface, as a subsampled voxel-centre cloud (same µm frame as the SE
    # mesh / AM / additive_points).  Cap at the GLOBAL top (a high percentile of the per-column solid tops,
    # robust to one tall AM) — this drops the empty HEADSPACE above the bed (the "SE 없는 위층") and fully-
    # empty periodic-edge columns, while KEEPING surface-valley + inter-particle pore (a per-COLUMN cap was
    # too aggressive: it deleted real pore wherever a column happened to be short).  ⚠ the cloud is a COARSE
    # n_vox preview — its void fraction under-counts the authoritative sim porosity (mpm_metrics); it shows
    # WHERE the pores are, not the exact amount.  Additives (~4 vol%, in-pore) are NOT subtracted.
    void_points = []
    if a.void_max > 0:
        solid = am | se_mask                               # (nx, ny, nz)
        nzc = solid.shape[2]
        has = solid.any(axis=2)                            # columns containing any solid
        ztop = np.where(has, nzc - 1 - np.argmax(solid[:, :, ::-1], axis=2), -1)   # highest solid z per column
        gtop = int(np.percentile(ztop[has], 98)) if has.any() else nzc - 1         # GLOBAL bed top (spike-robust)
        _th = sim_m.get('thickness_um') or sim_m.get('thickness_mpm_um')           # never above the plate position
        if _th and s > 0:                                  # (a few tall AM poke above the mean bed → headspace)
            gtop = min(gtop, int(_th / s))
        zz = np.arange(nzc)[None, None, :]
        void = (~solid) & (zz <= gtop) & has[:, :, None]   # pore below the global top, in solid-bearing columns
        vi = np.argwhere(void)
        nvoid = len(vi)
        if nvoid > a.void_max:
            vi = vi[np.random.default_rng(3).choice(nvoid, a.void_max, replace=False)]
        void_points = ((vi + 0.5) * s).astype(np.float32).round(2).tolist()
        print(f'  void (pore) cloud: {len(void_points):,} of {nvoid:,} internal-pore voxels '
              f'(below global top z={gtop}/{nzc}; headspace+empty cols dropped; raw void {int((~solid).sum()):,})')

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
        seed_mask = seed_se_mask(a.se_dump, am_p.shape, h, am, dz=a.dilate_z)
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
    # electronic connectivity (연결/고립, slide-19 quantity) — FULL-RES se+phase, before subsampling
    econn = None; econn_summary = None
    if len(r):
        try:
            _sdcp = (sim_m.get('additives') or {}).get('SDCP') or {}
            # neutral SDCP (~1e-3..1e-1 S/cm) ≈ AM-grade conductor → KEPT in the binary graph (AM itself
            # is a node at similar σ; an insulator-drop would misclassify by ~13 orders vs ≤1).  The
            # doped/neutral quantitative split = STEP3 Kirchhoff σ-weights, not a percolation boolean.
            econn, _ncl = electronic_connectivity(t, c, r, se, phase, FLOOR, UM)
            econn_summary = {'connected_pct': round(100.0 * float(econn.mean()), 1),
                             'n_isolated': int((~econn).sum()), 'n_carbon_clusters': _ncl,
                             'tol_am_um': 0.10, 'band_um': 0.15, 'vox_um': 0.30,
                             'conductive_phases': ('AM + VGCF/SuperP + neutral-SDCP as AM-grade weak conductor '
                                                   '(SE·PTFE excluded; doped/neutral split = STEP3 σ-weights)'
                                                   if _sdcp.get('variant') == 'neutral'
                                                   else 'AM + VGCF/SuperP/SDCP (SE·PTFE excluded = e-insulators)')}
            for ty, nm in ((1, 'AM_P'), (2, 'AM_S')):
                m = (t == ty)
                if m.any():
                    econn_summary[f'connected_pct_{nm}'] = round(100.0 * float(econn[m].mean()), 1)
            print(f"  econn: {econn_summary['connected_pct']}% AM connected to the collector "
                  f"({econn_summary['n_isolated']} isolated; {_ncl} carbon clusters)")
        except Exception as _e:
            print(f'  ⚠ econn skipped ({_e})')
    # ★ STEP3 v1 — electronic voxel resistor network (FULL-RES, like econn): σ_e_eff + per-AM
    # current density (slide-20 axis) + per-phase current share.  ∇·(σ∇φ)=0, harmonic-mean faces,
    # collector plate below / φ=0 above, lateral Neumann.  TRUST = RELATIVE comparison at identical
    # settings (σ hooks + vox recorded in metrics); absolute σ_e needs the DEM Stage-E contact-area
    # cross-calibration (sub-voxel constriction not modelled).  scripts/step3_sigma.py has the
    # analytic laminate/percolation self-tests that pin the assembly.
    step3 = None; je_am = None; jb_am = None; elec_field = None; ion_field = None; jrxn_am = None
    if len(r) and not a.no_step3:                       # phase=None → AM-skeleton-only σ (SBE baseline)
        try:
            import time as _time
            import step3_sigma as _s3
            _s3.GPU_SOLVE = a.step3_gpu                     # CuPy CG backend (auto CPU fallback)
            _t0 = _time.time()
            _off = np.array([SW[0], SW[0], FLOOR])
            _am_c = (c - _off) * UM
            _am_r = r * UM
            _cond_ph = (2, 3, 5, 4) if a.sigma_ptfe > 0 else (2, 3, 5)   # PTFE(4)는 민감도 런에서만 스탬프
            _m = (np.isin(phase, _cond_ph) if phase is not None
                  else np.zeros(len(se), bool))            # conductive additives (PTFE 4 = insulator, default)
            _apts = (se[_m] - _off) * UM if _m.any() else None
            _aph = phase[_m] if _m.any() else None
            _hi = ((SW[1] - SW[0]) * UM, (SW[1] - SW[0]) * UM, max((top - FLOOR) * UM, a.step3_vox))
            print('  STEP3: voxelizing conductive+SE grid (풀해상도 — 이후 전자/이온 CG 솔브, 침묵 수 분 정상)…', flush=True)
            _septs = (se[phase == 1] - _off) * UM if phase is not None else (se - _off) * UM
            sid3, pid3 = _s3.rasterize(_am_c, _am_r, t, _apts, _aph, (0.0, 0.0, 0.0), _hi, a.step3_vox,
                                       se_pts=_septs)      # SE stamped (sid 6) → ionic solve on the same grid
            _sig3 = np.array([0.0, a.sigma_am_s, a.sigma_am_p, a.sigma_vgcf, a.sigma_superp, a.sigma_sdcp,
                              0.0, a.sigma_ptfe])          # ELECTRONIC table: SE = e-insulator; idx7 =
            #                                                PTFE sensitivity hook (default 0 → sid7 미존재)
            _ztop = float(sim_m.get('thickness_um') or ((top - FLOOR) * UM))   # PRESS PLANE (wall_z) —
            #   `top` has a +0.01-box (~0.4µm) void-cap padding that floats the plate off the bed
            #   crowns (kgy first run: no_plate_contact); the sim thickness is the physical plate.
            _res3 = _s3.solve_sigma_z(sid3, _sig3, a.step3_vox, return_field=True,
                                      z_top_um=_ztop, z_bot_um=0.0)
            if _res3.get('reason'):
                print(f"  ⚠ STEP3 σ_e not solvable: {_res3['reason']}")
                step3 = {'sigma_e_eff_S_cm': 0.0, 'reason': _res3['reason'], 'vox_um': a.step3_vox}
            elif _res3['n_dof']:
                je_am = np.nan_to_num(_s3.per_particle_current(_res3, sid3, pid3, _sig3, len(r)),
                                      nan=0.0, posinf=0.0, neginf=0.0)   # a bare NaN token kills JSON.parse
                _p998e = None                               # 필드 정량 스케일용 (아래 step3에 기록)
                if not a.no_field:                          # ELECTRONIC field (AM+carbon {1,2,3,4,5}) — the
                    _ep, _ej = _s3.field_point_cloud(       # paper Fig-4 grammar: |J_e| cloud, hot backbone
                        _res3, sid3, _sig3, a.step3_vox, (1, 2, 3, 4, 5, 7), max_points=a.field_max_points)
                    if _ep is not None:
                        _ej = np.nan_to_num(_ej, nan=0.0, posinf=0.0, neginf=0.0)  # bare NaN kills JSON.parse
                        _p998e = max(float(np.percentile(_ej, 99.8)), 1e-30)
                        _ejn = _ej / _p998e                                        # p99.8-norm (top 0.2%>1,
                        elec_field = [[round(float(_ep[i, 0]), 2), round(float(_ep[i, 1]), 2),   # viewer clamps;
                                       round(float(_ep[i, 2]), 2), round(float(_ejn[i]), 4)]     # keeps dim-end
                                      for i in range(len(_ep))]                                  # range vs max-norm)
                        print(f"  STEP3 electronic FIELD: {len(elec_field):,} pts (AM+carbon |J| cloud)")
                _share = _s3.phase_current_share(_res3, sid3, _sig3)
                _sname = _s3.SID_NAME
                step3 = {'sigma_e_eff_S_cm': float(f"{_res3['sigma_eff']:.4g}"),
                         'vox_um': a.step3_vox, 'n_dof': _res3['n_dof'],
                         'k_plates': list(_res3.get('k_plates', ())),
                         'n_floating_dropped': _res3.get('n_floating_dropped', 0),
                         'cg_resid': float(f"{_res3['resid']:.2g}"),
                         'dissipation_share': {_sname[k]: round(v, 4) for k, v in _share.items()},
                         'sigma_table_S_cm': {'AM_S': a.sigma_am_s, 'AM_P': a.sigma_am_p,
                                              'VGCF': a.sigma_vgcf, 'SuperP': a.sigma_superp,
                                              'SDCP': a.sigma_sdcp,
                                              **({'PTFE': a.sigma_ptfe} if a.sigma_ptfe > 0 else {})},
                         'trust': ('RELATIVE_v1 (same settings between runs; pressed-to-plate beds — '
                                   'plate contacts abundant; carbon/SDCP σ = F1 hooks; AM_S/P = A1-locked '
                                   '10/5 mS/cm; lateral Neumann; sub-voxel constriction not modelled)'
                                   + (' ⚠UNCONVERGED' if _res3.get('unconverged') else ''))}
                if _p998e is not None:                      # 정량 컬러바 스케일 (뷰어 라벨용): 내부
                    # jmag=σ_hm·Δφ_face=J·vox_cm → J[A/cm²]=jmag/vox_cm (ΔV=1V 선형해).
                    # ⟨J_z⟩=σ_eff·ΔV/L.  focus=J/⟨J_z⟩=바이어스-무관 집중계수 (균일도체=1 검산).
                    _voxcm = a.step3_vox * 1e-4
                    _Lcm = max(_ztop, 1e-9) * 1e-4
                    _jm_e = _res3['sigma_eff'] / _Lcm
                    # 면적용량 자동산출 → mA/cm² 절대 라벨: Q_vol = F·c_max·|x100−x0|/3600
                    # (Chen2020 NMC811 기계추출 창 — step4_pybamm_anchor와 동일 §F1 앵커)
                    # ≈ 998 mAh/cm³ (교차확인 ~200 mAh/g × 4.8 g/cm³ = 960).  운전 ⟨J⟩ @1C
                    # = 면적용량 × 1 h⁻¹ [mA/cm²]; 국소 = (|J|/⟨J⟩) × ⟨J⟩ — 선형해라 정확.
                    _QVOL_mAh_cm3 = 96485.0 * 63104.0 * abs(0.853974674630047
                                                            - 0.2638452245913298) / 3600.0 / 1000.0
                    _n_amvox = int(np.count_nonzero((sid3 == 1) | (sid3 == 2)))
                    _A_um2 = sid3.shape[0] * sid3.shape[1] * (a.step3_vox ** 2)
                    _areal_mAh_cm2 = _QVOL_mAh_cm3 * (_n_amvox * a.step3_vox ** 3 / _A_um2) * 1e-4
                    step3['field_scale_e'] = {
                        'j_top_A_cm2_per_V': float(f"{_p998e / _voxcm:.4g}"),
                        'j_mean_z_A_cm2_per_V': float(f"{_jm_e:.4g}"),
                        'focus_top': float(f"{(_p998e / _voxcm) / max(_jm_e, 1e-30):.4g}"),
                        'dV_V': 1.0,
                        'areal_capacity_mAh_cm2': float(f"{_areal_mAh_cm2:.4g}"),
                        'j_1C_mA_cm2': float(f"{_areal_mAh_cm2:.4g}"),
                        'note': ('v(0..1): ×j_top→A/cm²@ΔV=1V; ×focus_top→|J|/⟨J_z⟩(바이어스 무관); '
                                 '국소 mA/cm²@C-rate = focus×j_1C×C (j_1C=면적용량, Chen2020 창)')}
                # COLLECTOR-INTERFACE post-processing (C-SUS/primer axis, manuscript-anchored):
                # the solve's bottom plate is a PERFECT contact (R_int=0) → σ_e_eff is the BULK
                # network value.  A real collector adds an AREAL series term: σ_apparent =
                # L/(L/σ_bulk + R_int) — exact series composition for uniform areal R_int, no
                # re-solve.  Anchors = manuscript Fig6e post-cycling R_int (Ω·cm²): bare-Al SBE
                # 110 / DBE 46 / SDCP-graphene-primer C-SUS 30 (S14: primer σ 1.3e4 S/cm, 200nm).
                # Bulk R (~0.002 Ω·cm²) ≪ R_int → the INTERFACE is the bottleneck the primer
                # fixes — the model states that quantitatively.
                _Lcm = _ztop * 1e-4
                _Rbulk = _Lcm / max(step3['sigma_e_eff_S_cm'], 1e-30)
                step3['collector'] = {'kind': 'SCENARIO series load — measured R_int applied '
                                              'externally (NOT a model prediction; the model\'s own '
                                              'interface OUTPUT is collector_geometric.R_geom)',
                                      'R_bulk_ohm_cm2': float(f'{_Rbulk:.3g}'),
                                      'anchors': 'Fig6e post-cycling R_int; S14 primer 1.3e4 S/cm 200nm',
                                      'sigma_apparent_S_cm': {
                                          nm2: float(f'{_Lcm / (_Rbulk + _R):.3g}')
                                          # ★ 사용자 확정 시나리오 트리플 (2026-07-10): SBE / DBE / SBE+C-SUS.
                                          #   SBE+C-SUS는 manuscript 미측정 → DBE-앵커(30) proxy 라벨.
                                          for nm2, _R in (('ideal_R0', 0.0), ('SBE_bare_110', 110.0),
                                                          ('DBE_bare_46', 46.0),
                                                          ('SBE_CSUS_30_proxy_DBE_anchored', 30.0))}}
                print(f"  STEP3 σ_e_eff = {step3['sigma_e_eff_S_cm']:.4g} S/cm  (vox {a.step3_vox}µm, "
                      f"{_res3['n_dof']:,} dof, resid {_res3['resid']:.1e}, {_time.time()-_t0:.0f}s)  "
                      f"share: " + " ".join(f"{k} {100*v:.0f}%" for k, v in step3['dissipation_share'].items()))
                if a.collector_rint >= 0.0:                # UI-selected preset → highlighted entry
                    step3['collector']['selected'] = {
                        'name': a.collector_name or f'R{a.collector_rint:g}',
                        'R_int_ohm_cm2': a.collector_rint,
                        'sigma_apparent_S_cm': float(f'{_Lcm / (_Rbulk + a.collector_rint):.3g}')}
                _ca = step3['collector']['sigma_apparent_S_cm']
                # carbon-free/희박 배선 케이스는 R_bulk가 계면(30-110)과 동급까지 올라옴 — "≪" 고정
                # 문구가 그 regime에서 거짓이 되던 것을 조건화 (260714 carbon-free: R_bulk 12 Ωcm²)
                _rel = ('≪ 계면' if _Rbulk < 3.0 else
                        '≈ 계면과 동급 — carbon-free/희박 배선 regime' if _Rbulk < 100.0 else '≫ 계면(!)')
                print(f"  STEP3 collector scenarios: bulk {_ca['ideal_R0']:.3g} → SBE(110Ωcm²) "
                      f"{_ca['SBE_bare_110']:.3g} / DBE(46) {_ca['DBE_bare_46']:.3g} / SBE+C-SUS(30 proxy) "
                      f"{_ca['SBE_CSUS_30_proxy_DBE_anchored']:.3g} S/cm  (R_bulk {_Rbulk:.2g} Ωcm² {_rel})")
                # ★ ANALYTIC-GAP GEOMETRIC pair (v3, user: "지금 하자"): the contact SELECTION now
                # comes from EXACT sphere/point z (no voxel blur — the DEM positions are known
                # exactly): bare = surface within 0.10µm of the collector (econn contact tol),
                # wetted = within 0.30µm (0.10 + 200nm primer film reach).  Per-sphere contact
                # patch on the plane: ρ² = r² − (z_c − tol)² (surface-within-tol footprint);
                # conductive additive points (2/3/5) with z ≤ tol mark their columns too.
                # The voxel solve then couples ONLY those columns (selection analytic; coupling
                # conductance stays voxel-scale).  je = canonical plate, jb = analytic-bare.
                def _bot_mask(_tol):
                    _nx2, _ny2 = sid3.shape[0], sid3.shape[1]
                    _mm2 = np.zeros((_nx2, _ny2), bool)
                    _gz = _am_c[:, 2] - _am_r
                    for _i2 in np.where(_gz <= _tol)[0]:
                        _rho2 = _am_r[_i2] ** 2 - max(_am_c[_i2, 2] - _tol, 0.0) ** 2
                        if _rho2 <= 0:
                            continue
                        _rho = float(np.sqrt(_rho2))
                        _x0 = max(0, int((_am_c[_i2, 0] - _rho) / a.step3_vox))
                        _x1 = min(_nx2 - 1, int((_am_c[_i2, 0] + _rho) / a.step3_vox))
                        _y0 = max(0, int((_am_c[_i2, 1] - _rho) / a.step3_vox))
                        _y1 = min(_ny2 - 1, int((_am_c[_i2, 1] + _rho) / a.step3_vox))
                        if _x1 < _x0 or _y1 < _y0:
                            continue
                        _gxx, _gyy = np.ogrid[_x0:_x1 + 1, _y0:_y1 + 1]
                        _mm2[_x0:_x1 + 1, _y0:_y1 + 1] |= (
                            ((_gxx + 0.5) * a.step3_vox - _am_c[_i2, 0]) ** 2
                            + ((_gyy + 0.5) * a.step3_vox - _am_c[_i2, 1]) ** 2) <= _rho2
                    if _apts is not None and len(_apts):
                        _lw = _apts[:, 2] <= _tol
                        if _lw.any():
                            _ij = np.floor(_apts[_lw, :2] / a.step3_vox).astype(int)
                            _ok3 = (_ij[:, 0] >= 0) & (_ij[:, 0] < _nx2) & (_ij[:, 1] >= 0) & (_ij[:, 1] < _ny2)
                            _mm2[_ij[_ok3, 0], _ij[_ok3, 1]] = True
                    return _mm2
                _mw, _mb = _bot_mask(0.30), _bot_mask(0.10)
                _res3w = _s3.solve_sigma_z(sid3, _sig3, a.step3_vox, return_field=False,
                                           z_top_um=_ztop, z_bot_um=0.0, bot_allowed=_mw)
                _res3b = _s3.solve_sigma_z(sid3, _sig3, a.step3_vox, return_field=True,
                                           z_top_um=_ztop, z_bot_um=0.0, bot_allowed=_mb)
                jb_am = None
                if 'phi' in _res3b:
                    jb_am = np.nan_to_num(_s3.per_particle_current(_res3b, sid3, pid3, _sig3, len(r)),
                                          nan=0.0, posinf=0.0, neginf=0.0)
                # R_geom = the interface resistance the GEOMETRY itself creates (bare contact
                # starving vs film-wetted) — the MODEL'S OWN emergent interface number (an OUTPUT;
                # 측정 R_int는 결과값이지 설정값이 아님).  measured R_int − R_geom = the chemistry/
                # degradation share the structure model does NOT contain (quantified limit).
                _swR = float(_res3w['sigma_eff']); _sbR = float(_res3b['sigma_eff'])
                # 가드(#9 code-review): 축퇴/실패 solve(σ≤0 or reason)면 R_geom을 계산하지 말 것 —
                # 1e-30 클램프가 _Lcm/σ ≈ 1e27 Ω·cm² 를 만들어 'MODEL OUTPUT'으로 뱉는 걸 막는다.
                if _res3b.get('reason') or _res3w.get('reason') or _swR <= 0.0 or _sbR <= 0.0:
                    _rgeom = None
                else:
                    _sw = max(_swR, 1e-30); _sb = max(_sbR, 1e-30)
                    _rgeom = max(0.0, _Lcm / _sb - _Lcm / _sw)
                step3['collector_geometric'] = {
                    'mode': 'analytic_gap_v3 (bare gap≤0.10µm / wetted gap≤0.30µm — exact sphere/point z)',
                    'wetted_sigma_S_cm': float(f'{_sw:.4g}'),
                    'bare_sigma_S_cm': float(f'{_sb:.4g}'),
                    'R_geom_ohm_cm2': (None if _rgeom is None else float(f'{_rgeom:.3g}')),
                    'n_bottom_contacts': {'wetted': (_res3w.get('n_plate_vox') or (None,))[0],
                                          'bare': (_res3b.get('n_plate_vox') or (None,))[0],
                                          'canonical_plate': (_res3.get('n_plate_vox') or (None,))[0]},
                    **({'bare_reason': _res3b['reason']} if _res3b.get('reason') else {}),
                    **({'wetted_reason': _res3w['reason']} if _res3w.get('reason') else {}),
                    'note': 'MODEL OUTPUT (emergent): contact SELECTION analytic (no voxel blur); '
                            'coupling conductance voxel-scale.  R_geom = L(1/σ_bare − 1/σ_wetted); '
                            'measured R_int − R_geom = chemistry/degradation share'}
                _cgm = step3['collector_geometric']
                _rgs = 'n/a (solve degenerate)' if _cgm['R_geom_ohm_cm2'] is None else f"{_cgm['R_geom_ohm_cm2']:.3g}"
                print(f"  STEP3 collector geometry (MODEL output): wetted {_cgm['wetted_sigma_S_cm']:.3g} "
                      f"({_cgm['n_bottom_contacts']['wetted']} contacts) vs bare "
                      f"{_cgm['bare_sigma_S_cm']:.3g} S/cm ({_cgm['n_bottom_contacts']['bare']}) → "
                      f"R_geom {_rgs} Ωcm² (측정 R_int와의 갭 = 화학/열화 몫)")
                # IONIC network on the SAME grid (paper Fig-2d/f axis): SE + SDCP conduct Li⁺
                # (user principle — SDCP is NOT an ion insulator), AM/carbon/PTFE block.
                _t1 = _time.time()
                _sig3i = np.array([0.0, 0.0, 0.0, 0.0, 0.0, a.sigma_ion_sdcp, a.sigma_ion_se, 0.0])
                _res3i = _s3.solve_sigma_z(sid3, _sig3i, a.step3_vox, return_field=True,
                                           z_top_um=_ztop, z_bot_um=0.0)
                if _res3i['n_dof']:
                    _sharei = _s3.phase_current_share(_res3i, sid3, _sig3i)
                    if not a.no_field:                      # IONIC field (SE+SDCP {5,6}) — Li⁺ |J| cloud,
                        _ip, _ij = _s3.field_point_cloud(   # the partner panel to the electronic field
                            _res3i, sid3, _sig3i, a.step3_vox, (5, 6), max_points=a.field_max_points)
                        if _ip is not None:
                            _ij = np.nan_to_num(_ij, nan=0.0, posinf=0.0, neginf=0.0)  # bare NaN kills JSON.parse
                            _p998i = max(float(np.percentile(_ij, 99.8)), 1e-30)
                            _ijn = _ij / _p998i                                        # p99.8-norm (top 0.2%>1,
                            ion_field = [[round(float(_ip[i, 0]), 2), round(float(_ip[i, 1]), 2),   # viewer clamps)
                                          round(float(_ip[i, 2]), 2), round(float(_ijn[i]), 4)]
                                         for i in range(len(_ip))]
                            print(f"  STEP3 ionic FIELD: {len(ion_field):,} pts (SE+SDCP |J| cloud)")
                            # 정량 컬러바 스케일 (뷰어 라벨용): 내부 jmag=σ_hm·Δφ_face=J·vox_cm
                            # → J[A/cm²]=jmag/vox_cm (ΔV=1V 선형해).  ⟨J_z⟩=σ_eff·ΔV/L.
                            # focus=J/⟨J_z⟩=바이어스-무관 집중계수 (균일도체=1 검산).
                            _voxcm = a.step3_vox * 1e-4
                            _Lcm = max(_ztop, 1e-9) * 1e-4
                            _jm_i = _res3i['sigma_eff'] / _Lcm
                            _fse = step3.get('field_scale_e') or {}
                            step3['field_scale_ion'] = {
                                'j_top_A_cm2_per_V': float(f"{_p998i / _voxcm:.4g}"),
                                'j_mean_z_A_cm2_per_V': float(f"{_jm_i:.4g}"),
                                'focus_top': float(f"{(_p998i / _voxcm) / max(_jm_i, 1e-30):.4g}"),
                                'dV_V': 1.0,
                                # 정상상태 단일-이온 SE: 이온 관통 ⟨J⟩ = 전자 ⟨J⟩ = 면적전류 (직렬)
                                'areal_capacity_mAh_cm2': _fse.get('areal_capacity_mAh_cm2'),
                                'j_1C_mA_cm2': _fse.get('j_1C_mA_cm2'),
                                'note': ('v(0..1): ×j_top→A/cm²@ΔV=1V; ×focus_top→|J|/⟨J_z⟩(바이어스 무관); '
                                         '국소 mA/cm²@C-rate = focus×j_1C×C (j_1C=면적용량, Chen2020 창)')}
                    # ★ φ(z) 프로파일 (Oh 2025 primer 논문 Fig 4e 문법 = ΔV=1V 전도 솔브의
                    # 두께방향 전위) — 층별 전도-복셀 평균.  전자(정본) + 전자(bare 집전체:
                    # 계면 강하 그림) + 이온 3곡선.  solve 규약: 바닥판 φ=1, 꼭대기 φ=0.
                    def _phi_prof(_resX):
                        if 'phi' not in _resX:
                            return None
                        _P, _C = _resX['phi'], _resX['cond']
                        _pz, _zz = [], []
                        for _k in range(sid3.shape[2]):
                            _m3 = _C[:, :, _k]
                            if _m3.any():
                                _pz.append(float(_P[:, :, _k][_m3].mean()))
                                _zz.append(round((_k + 0.5) * a.step3_vox, 3))
                        return {'z_um': _zz, 'phi': [float(f'{v:.5g}') for v in _pz]}
                    step3['phi_profile'] = {k: v for k, v in {
                        'electronic': _phi_prof(_res3), 'electronic_bare': _phi_prof(_res3b),
                        'ionic': _phi_prof(_res3i)}.items() if v}
                    step3['phi_profile']['note'] = ('ΔV=1V 전도 솔브 층별 전도-복셀 평균 φ '
                                                    '(바닥판 φ=1, 꼭대기 φ=0; Oh2025 Fig4e 문법)')
                    step3['sigma_ion_eff_S_cm'] = float(f"{_res3i['sigma_eff']:.4g}")
                    step3['ion_dissipation_share'] = {_s3.SID_NAME.get(k, str(k)): round(v, 4)
                                                      for k, v in _sharei.items()}
                    step3['sigma_ion_table_S_cm'] = {'SE': a.sigma_ion_se, 'SDCP': a.sigma_ion_sdcp}
                    step3['ion_resid'] = float(f"{_res3i['resid']:.2g}")
                    print(f"  STEP3 σ_ion_eff = {step3['sigma_ion_eff_S_cm']:.4g} S/cm  "
                          f"({_res3i['n_dof']:,} dof, resid {_res3i['resid']:.1e}, {_time.time()-_t1:.0f}s)  "
                          f"share: " + " ".join(f"{k} {100*v:.0f}%"
                                                for k, v in step3['ion_dissipation_share'].items()))
                # ★ A6 — PORE-phase effective-diffusion τ (DiffuDict/TauFactor 규약, #281/#286 축):
                # 같은 격자에서 void상 σ=1 Laplace → D_eff/D0, τ = ε_total/D_rel.  STRUCTURAL
                # descriptor (frame[4] cross-check) — ASSB Li⁺ 수송은 SE 접촉망(σ_ion 위)이 담당,
                # 이 τ를 수송 폼/PyBaMM τ에 대입 금지 (audit #2 이중계산 함정).  PTFE는 e/ion
                # 격자에 미스탬프(양쪽 절연) → 여기서 solid로 스탬프해 기공 과대계상 방지.
                try:
                    _t6 = _time.time()
                    _ppts = ((se[phase == 4] - _off) * UM
                             if (phase is not None and (phase == 4).any()) else None)
                    _rp = _s3.pore_tau(sid3, a.step3_vox, z_top_um=_ztop, extra_solid_pts=_ppts)
                    step3['pore'] = {k: _rp[k] for k in ('eps_total_pct', 'eps_connected_pct',
                                                         'D_rel', 'tau', 'n_dof') if k in _rp}
                    if _rp.get('reason'):
                        step3['pore']['reason'] = _rp['reason']
                    step3['pore']['resid'] = float(f"{_rp['resid']:.2g}")
                    step3['pore']['trust'] = ('STRUCTURAL pore-diffusion τ (D_eff/D0 = ε/τ, TauFactor '
                                              '규약, ε_total 기준; 닫힌 기공은 τ를 올림) — SE-망 '
                                              'σ_ionic과 별개 축, 수송 폼 대입 금지; PTFE solid-stamped; '
                                              'grid cropped to z ≤ thickness'
                                              + (' ⚠UNCONVERGED' if _rp.get('unconverged') else ''))
                    print(f"  STEP3 pore-τ: ε_tot {step3['pore'].get('eps_total_pct')}% (conn "
                          f"{step3['pore'].get('eps_connected_pct')}%) · D_rel {step3['pore'].get('D_rel')}"
                          f" · τ {step3['pore'].get('tau')}"
                          + (f"  ⚠{_rp['reason']}" if _rp.get('reason') else '')
                          + f"  ({_time.time()-_t6:.0f}s)")
                except Exception as _e6:                     # pore-τ 실패가 STEP3 결과를 못 물귀신하게 격리
                    print(f'  ⚠ pore-τ skipped ({type(_e6).__name__}: {_e6}) — STEP3 결과는 유지')
                # ★ STEP4-v1 — 저율 충전 **반응전류 분포** (랩 slide-20 물리): 전자망(집전체 급전)과
                # 이온망(분리막 급전)을 AM|SE·AM|SDCP 접촉면의 선형화 Butler-Volmer 컨덕턴스로 결합한
                # 단일 Kirchhoff 시스템 → 입자별 i_n.  분포는 RELATIVE(i/ī, linear라 C-rate 스케일 무관);
                # 절대화(A/m²·SOC 의존)는 STEP4-v2.  analytic sandwich selftest: --selftest-rxn.
                if not a.no_step4:
                  try:                                       # STEP4 실패가 STEP3 결과를 못 물귀신하게 격리
                    _t4 = _time.time()
                    _gpp = a.i0_a_m2 * 1e-4 * 38.92          # i0[A/m²→A/cm²] × F/RT[V⁻¹] = g″ [S/cm²]
                    _gct = _gpp * (a.step3_vox ** 2) * 1e-4  # face-conductance (σ·vox_µm 코드 규약 정합)
                    _r4 = _s3.solve_reaction_current(sid3, _sig3, _sig3i, pid3, len(r), a.step3_vox,
                                                     _gct, z_top_um=_ztop, z_bot_um=0.0)
                    if _r4.get('reason'):
                        print(f"  ⚠ STEP4 rxn skipped: {_r4['reason']}")
                    else:
                        _ia = np.nan_to_num(_r4['i_am'], nan=0.0, posinf=0.0, neginf=0.0)
                        _pos = _ia[_ia > 0]
                        jrxn_am = _ia / max(float(_pos.mean()) if len(_pos) else 0.0, 1e-30)   # i/ī
                        step3['rxn'] = {
                            'i0_A_m2': a.i0_a_m2,
                            'gct_S_cm2': float(f'{_gpp:.4g}'),
                            'n_bv_faces': _r4['n_bv_faces'],
                            'active_am_pct': round(100.0 * float((_ia > 0).mean()), 1),
                            'kcl_err': float(f"{_r4['kcl_err']:.2g}"),
                            'resid': float(f"{_r4['resid']:.2g}"),
                            'trust': ('RELATIVE i/mean map — linearised BV, uniform SOC, low-rate '
                                      '(charge↔discharge = sign only); i0 ⚠F1 hook; reaction area = '
                                      'rasterized AM|SE·AM|SDCP faces (coverage-native)'
                                      + (' ⚠UNCONVERGED' if _r4['unconverged'] else ''))}
                        print(f"  STEP4 rxn: BV faces {_r4['n_bv_faces']:,} · active AM "
                              f"{step3['rxn']['active_am_pct']}% · i/ī p95 "
                              f"{float(np.percentile(jrxn_am, 95)):.2f} · KCL {_r4['kcl_err']:.1e} · "
                              f"resid {_r4['resid']:.1e} ({_time.time()-_t4:.0f}s)")
                  except Exception as _e4:
                    jrxn_am = None
                    print(f'  ⚠ STEP4 rxn failed ({type(_e4).__name__}: {_e4}) — STEP3 결과는 유지')
                if a.save_step4_grid:                        # STEP4-v2 동역학 입력 (step4_dyn.py --grid)
                    np.savez_compressed(a.save_step4_grid, sid=sid3.astype(np.int8),
                                        pid=pid3.astype(np.int32), vox_um=a.step3_vox,
                                        z_top_um=_ztop, sig_e_S_cm=_sig3, sig_i_S_cm=_sig3i,
                                        am_r_um=np.asarray(r, np.float64) * UM)
                    a._s4grid_saved = True           # end-of-main 알림용 (stale 파일 오탐 방지, 리뷰 R2#6)
                    print(f'  STEP4-v2 grid → {a.save_step4_grid}  (sid {sid3.shape}, '
                          f'n_am {len(r)}, vox {a.step3_vox}µm)')
        except Exception as _e:
            import traceback as _tb
            print(f'  ⚠ STEP3 skipped ({type(_e).__name__}: {_e})')
            print('    ' + _tb.format_exc(limit=2).strip().replace(chr(10), chr(10) + '    '))
    particles = [{'id': int(i), 'type': name.get(int(t[i]), 'AM'),
                  'x': round(float((c[i, 0] - SW[0]) * UM), 3),
                  'y': round(float((c[i, 1] - SW[0]) * UM), 3),
                  'z': round(float((c[i, 2] - FLOOR) * UM), 3),
                  'r': round(float(r[i] * UM), 3),
                  'coverage': float(cov_per[i]),
                  **({'econn': int(econn[i])} if econn is not None else {}),
                  **({'je': float(f'{je_am[i]:.4g}')} if je_am is not None else {}),
                  **({'jb': float(f'{jb_am[i]:.4g}')} if jb_am is not None else {}),
                  **({'jrxn': float(f'{jrxn_am[i]:.4g}')} if jrxn_am is not None else {})} for i in range(len(r))]

    # conductive additives (VGCF/SuperP/PTFE) → colored points for the 도전재 3D viewer.  Subsampled
    # proportionally to the budget; carried as [x,y,z,phase] µm (phase 2 VGCF · 3 SuperP · 4 PTFE).
    additive_points = []
    additive_counts = {}
    if phase is not None:
        rng_a = np.random.default_rng(1)
        add_tot = int((phase >= 2).sum())
        for code, nm in ((2, 'VGCF'), (3, 'SuperP'), (4, 'PTFE'), (5, 'SDCP')):
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
            fib_mask = np.isin(phase, (2, 4)) & (fid >= 0)   # rod phases only — coat ids (SuperP-thinky/SDCP shells) are NOT polylines
            n_fib_total = len(np.unique(fid[fib_mask]))
            # subsample fibres PER PHASE so a high-count phase (SuperP — ~40k carbon-black chains) doesn't
            # crowd out the low-count binder web (PTFE — ~300 fibres).  Fewest-fibre phase first gets its
            # fair share (kept whole if small); its surplus rolls to the larger phases → the PTFE web always
            # renders (uniform sampling left only ~45/320 PTFE when SuperP dominated the budget).
            _rng2 = np.random.default_rng(2)
            _phs = np.unique(phase[fib_mask])
            _ids_by_ph = {int(ph): np.unique(fid[fib_mask & (phase == ph)]) for ph in _phs}
            _budget = a.fibre_max; _rem = len(_phs); _keep = []
            for ph in sorted(_phs, key=lambda p: len(_ids_by_ph[int(p)])):
                ids_ph = _ids_by_ph[int(ph)]; share = max(1, _budget // max(_rem, 1))
                _keep.append(ids_ph if len(ids_ph) <= share else _rng2.choice(ids_ph, share, replace=False))
                _budget -= len(_keep[-1]); _rem -= 1
            uniq = np.concatenate(_keep) if _keep else np.array([], int)
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
                  + ('' if (dia is None or not additive_fibres)   # rod phases (2,4) can be ABSENT (e.g.
                     else f'  Ø rel {min(f["d"] for f in additive_fibres):.2f}'   # SuperP-only run: fibre.npy
                     f'..{max(f["d"] for f in additive_fibres):.2f}'))            # exists but 0 polylines) — min() on empty crashed A4 run

    lat = (SW[1] - SW[0]) * UM
    thick = (top - FLOOR) * UM

    # ★ A5/E2 — additive DISPERSION uniformity (#284 SSRM-analog, additives.dispersion_metrics):
    # per-phase index-of-dispersion (2µm cell lattice, CSR=1; SAME-PHASE run-to-run comparator —
    # chain phases carry within-object correlation) + SE-matrix→nearest-additive distances (µm,
    # cross-phase axis: "매트릭스가 네트워크에서 얼마나 먼가").  Pure geometry on the FULL-res
    # point cloud; §F1 — relative comparisons between our runs only, no SSRM absolute claimed.
    additive_dispersion = None
    if phase is not None and np.isin(phase, (2, 3, 4, 5)).any():
        try:
            from additives import dispersion_metrics as _dm
            _offd = np.array([SW[0], SW[0], FLOOR])
            _ztd = float(sim_m.get('thickness_um') or thick)
            _mse = np.where(phase == 1)[0]                   # SE matrix: subsample BEFORE the µm
            if len(_mse) > 20000:                            # copy (full SE = tens of millions pts)
                _mse = np.random.default_rng(0).choice(_mse, 20000, replace=False)
            _mx = (se[_mse] - _offd) * UM
            _amck = {'am_c_um': (c - _offd) * UM, 'am_r_um': r * UM}   # review M2/M3: AM-masked D
            additive_dispersion = {}                                   # cells + matrix-volume nn ref
            for _ph, _nm in ((2, 'VGCF'), (3, 'SuperP'), (4, 'PTFE'), (5, 'SDCP')):
                if (phase == _ph).any():
                    additive_dispersion[_nm] = _dm((se[phase == _ph] - _offd) * UM, (lat, lat),
                                                   _ztd, matrix_pts_um=_mx, **_amck)
            _mc = np.isin(phase, (2, 3, 5))                  # conductive network union (PTFE 제외)
            if _mc.any():
                additive_dispersion['conductive_all'] = _dm((se[_mc] - _offd) * UM, (lat, lat),
                                                            _ztd, matrix_pts_um=_mx, **_amck)
            print('  additive dispersion (A5/E2): ' + '  '.join(
                f"{_nm} D={_v.get('index_of_dispersion')} nn_med={_v.get('nn_med_um')}µm"
                f"(×{_v.get('nn_clustering')})"
                for _nm, _v in additive_dispersion.items() if 'reason' not in _v))
        except Exception as _e5:
            additive_dispersion = None
            print(f'  ⚠ dispersion metrics skipped ({type(_e5).__name__}: {_e5})')

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
        # additive(carbon/soft-fibre)-on-AM coverage (σ_e contact), SEPARATE from the SE coverage above
        # (which is now SE-ONLY as of the 2026-07-03 metric fix); None for carbon-free runs.
        'coverage_AM_P_add_mpm_pct': sim_m.get('coverage_AM_P_add_pct'),
        'coverage_AM_S_add_mpm_pct': sim_m.get('coverage_AM_S_add_pct'),
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
    if step3 is not None:
        mpm_metrics['step3'] = step3                       # σ_e_eff + σ-table + shares (RELATIVE trust)
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
              'bulk_density_g_cm3', 'seed_AM_frac_pct', 'seed_SE_frac_pct', 'n_grid', 'protocol',
              'additives', 'fibre_rod'):                    # per-additive recipe+physics + Tier-2 rod flag → 요약
        if k in sim_m:
            mpm_metrics[k] = sim_m[k]                       # carry through raw sim fields
    mpm_metrics.update(strain_stats)                       # Σdg mean/max/vmax98/n_strain_pts (if --dg)
    if additive_counts:
        mpm_metrics['additive_counts'] = additive_counts   # {VGCF:n, SuperP:n, PTFE:n} total seeded
    if additive_dispersion:
        mpm_metrics['additive_dispersion'] = additive_dispersion   # A5/E2: D(CSR=1)+nn_*(µm) per phase
    # fibre polyline count (VGCF/PTFE) — a morphology descriptor the summary can show without the sim JSON
    if additive_fibres:
        mpm_metrics['n_fibres'] = len(additive_fibres)
        # ★ buckling metric (the Tier-2 --fibre-rod check): per-fibre end-to-end / contour length.
        #   1.00 = perfectly straight; <1 = bent/wavy/buckled.  A straight seed → ~1.0; if the rod truly
        #   buckles the fibres, mean drops and a fraction go clearly bent.  Quantitative = settles the
        #   "did it buckle?" question the cluttered 3D view can't.  Computed straight from the polylines.
        _st = []
        for _f in additive_fibres:
            _p = np.asarray(_f.get('pts') or [], float)
            if len(_p) >= 2:
                _contour = float(np.sum(np.linalg.norm(np.diff(_p, axis=0), axis=1)))
                if _contour > 1e-9:
                    _st.append(float(np.linalg.norm(_p[-1] - _p[0])) / _contour)
        if _st:
            _st = np.asarray(_st)
            mpm_metrics['fibre_straightness_mean'] = round(float(_st.mean()), 4)        # 1=straight
            mpm_metrics['fibre_straightness_p10'] = round(float(np.percentile(_st, 10)), 4)  # most-buckled decile
            mpm_metrics['fibre_buckled_frac_pct'] = round(float((_st < 0.9).mean()) * 100.0, 1)  # % clearly bent

    payload = {
        'kind': 'mpm', 'case': a.case,
        'particles': particles,                            # AM_P / AM_S spheres (same both states)
        'econn_summary': econn_summary,                    # 전기적 연결성 (slide-19): % connected + graph params
        'am_coverage_patches': cov_patches,                # covered AM-surface points (spatial map)
        'se_strain_points': se_strain_points,              # [x,y,z,Σdg] µm — viewer "SE 소성변형" mode
        'mesh_triangles': tris,                            # COMPACTED SE plastic continuum (default)
        'seed_mesh_triangles': seed_tris,                  # loose SE before compaction (before/after)
        'additive_points': additive_points,                # [x,y,z,phase] µm — VGCF(2)/SuperP(3)/PTFE(4)
        'additive_fibres': additive_fibres,                # [{phase, pts:[[x,y,z],…]}] — VGCF/PTFE as polylines
        'electronic_field': elec_field,                    # [x,y,z,|J|₀₋₁] µm — STEP3 e⁻ current-density cloud (AM+carbon)
        'ionic_field': ion_field,                          # [x,y,z,|J|₀₋₁] µm — STEP3 Li⁺ current-density cloud (SE+SDCP)
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
    if a.save_step4_grid and not getattr(a, '_s4grid_saved', False):
        print(f'⚠ --save-step4-grid 요청됐지만 미저장 — STEP3 미도달/실패 경로 (step4-v2 입력 없음)')


if __name__ == '__main__':
    main()
