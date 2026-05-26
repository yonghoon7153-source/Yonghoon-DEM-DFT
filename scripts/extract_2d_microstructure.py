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
from scipy import ndimage as _ndi


def _disk(radius_px: int) -> np.ndarray:
    """Boolean disk structuring element of given pixel radius."""
    r = max(1, int(radius_px))
    yy, xx = np.ogrid[-r:r+1, -r:r+1]
    return (xx*xx + yy*yy) <= r*r


def _se_to_continuum(labels: np.ndarray, r_se_px: float,
                      target_void_frac: float | None = None) -> np.ndarray:
    """Convert discrete SE particles → a single CONNECTED SE matrix, then
    re-insert porosity as isolated interior pores.

    SE percolates ~99.5% top↔bottom in 3D, so the ionic FEM domain must be
    connected — a thin 2D slice that severs out-of-plane SE bridges would
    wrongly show isolated SE islands, and COMSOL cannot solve a disconnected
    electrolyte.  We therefore:

      (1) close the discrete SE into ONE connected continuum (bridges the
          sub-slice gaps that 3D SE fills just above/below the cut), then
      (2) carve the 3D-measured porosity back in as ISOLATED interior pores
          — holes placed fully inside thick SE.  A hole strictly interior to
          a connected 2D region never disconnects it, so SE stays a single
          percolating network while void fraction is pinned to the 3D value.

    target_void_frac : 3D porosity (0-1).  None → fully filled (no pores).
    """
    se = (labels == SE)
    is_am = (labels == AM_P) | (labels == AM_S)
    rad = max(1, int(round(r_se_px)))
    se_closed = _ndi.binary_closing(se, structure=_disk(rad))
    out = labels.copy()
    out[se_closed & (~is_am) & (labels == VOID)] = SE      # connected SE matrix

    if target_void_frac is None:
        return out

    total = out.size
    need = int(round(target_void_frac * total)) - int(np.sum(out == VOID))
    if need <= 0:
        return out

    # Irregular, size-varied isolated pores.  Each pore is carved only where
    # it is fully INTERIOR to the connected SE (a hole strictly inside a
    # connected 2D region never disconnects it), and a blocked margin keeps
    # pores from touching → SE stays one percolating network.  Pore size is
    # capped by the local SE thickness, so wide SE channels get larger pores
    # and tight gaps get small ones (realistic porosity), and each pore is a
    # wobbly blob (low-order radial harmonics), not a perfect disc.
    ny, nx = out.shape
    rng = np.random.default_rng(0)
    blocked = np.zeros((ny, nx), dtype=bool)
    se_now = (out == SE)
    dist_edge = _ndi.distance_transform_edt(se_now)        # interior room map
    pr_min = 2.0
    pr_max = max(3.0, r_se_px * 1.6)
    AMP = 0.35                                             # max radial wobble
    cy, cx = np.where(se_now & (dist_edge > pr_min + 1.5))
    if len(cy) == 0:
        return out
    order = np.argsort(-dist_edge[cy, cx])                 # thickest SE first
    for ci in order:
        if need <= 0:
            break
        py, px = int(cy[ci]), int(cx[ci])
        if blocked[py, px]:
            continue
        room = float(dist_edge[py, px])
        # sample a target radius (skewed small), capped so the wobbly blob
        # stays fully interior to the original SE
        r_target = pr_min + (pr_max - pr_min) * rng.random() ** 1.7
        r_base = min(r_target, (room - 1.5) / (1.0 + AMP))
        if r_base < pr_min:
            continue
        a = rng.uniform(-1, 1, 3) * (AMP / 3.0)            # 3 harmonics
        ph = rng.uniform(0, 2 * np.pi, 3)
        rmax = int(np.ceil(r_base * (1.0 + AMP))) + 1
        y0, y1 = max(0, py - rmax), min(ny, py + rmax + 1)
        x0, x1 = max(0, px - rmax), min(nx, px + rmax + 1)
        gy, gx = np.ogrid[y0 - py:y1 - py, x0 - px:x1 - px]
        rr = np.hypot(gy, gx)
        th = np.arctan2(gy, gx)
        r_blob = r_base * (1.0 + a[0] * np.cos(th + ph[0])
                                + a[1] * np.cos(2 * th + ph[1])
                                + a[2] * np.cos(3 * th + ph[2]))
        region = out[y0:y1, x0:x1]
        m = (rr <= r_blob) & (region == SE)
        c = int(m.sum())
        if c == 0:
            continue
        region[m] = VOID
        need -= c
        bm = int(rmax + pr_max + 2)                        # keep pores apart
        by0, by1 = max(0, py - bm), min(ny, py + bm + 1)
        bx0, bx1 = max(0, px - bm), min(nx, px + bm + 1)
        blocked[by0:by1, bx0:bx1] = True
    return out

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


def _am_p_grain_boundaries(labels, pa, pb, grain_size_um):
    """Generate polycrystalline grain-boundary mask inside AM_P regions.

    Each AM_P secondary particle is internally tessellated into primary
    grains (~grain_size_um) via nearest-seed (Voronoi) assignment;
    grain boundaries = AM_P pixels whose 4-neighbour belongs to a
    different grain.  AM_S (single-crystal) gets NO internal GB.

    Literature: Trevisanello 2021 — poly primary grain ~0.1-1 μm.
    """
    is_amp = (labels == AM_P)
    if is_amp.sum() == 0:
        return np.zeros_like(labels, dtype=bool)
    ny, nx = labels.shape
    # seed density: 1 seed per grain area (πr²) → grain "radius" = grain_size/2
    g_px = max(2.0, grain_size_um / pa)
    area_per_grain = np.pi * (g_px / 2) ** 2
    n_seed = max(4, int(is_amp.sum() / area_per_grain))
    rng = np.random.default_rng(42)
    ys, xs = np.where(is_amp)
    pick = rng.choice(len(xs), size=min(n_seed, len(xs)), replace=False)
    seed_xy = np.column_stack([xs[pick], ys[pick]])
    try:
        from scipy.spatial import cKDTree
        tree = cKDTree(seed_xy)
        gy, gx = np.where(is_amp)
        _, grain_id_flat = tree.query(np.column_stack([gx, gy]))
        grain_id = np.full((ny, nx), -1, dtype=np.int32)
        grain_id[gy, gx] = grain_id_flat
    except Exception:
        return np.zeros_like(labels, dtype=bool)
    # boundary = AM_P pixel whose right or down neighbour is a different grain
    gb = np.zeros((ny, nx), dtype=bool)
    gid = grain_id
    valid = gid >= 0
    # right neighbour
    diff_r = valid[:, :-1] & valid[:, 1:] & (gid[:, :-1] != gid[:, 1:])
    gb[:, :-1] |= diff_r
    gb[:, 1:]  |= diff_r
    # down neighbour
    diff_d = valid[:-1, :] & valid[1:, :] & (gid[:-1, :] != gid[1:, :])
    gb[:-1, :] |= diff_d
    gb[1:, :]  |= diff_d
    return gb & is_amp


def _faceted_inside(GA, GB, ac, bc, r, seed):
    """Sharp, irregular polygon footprint for a single-crystal (AM_S) particle.

    Single-crystal NCM grows as faceted rhombohedral/hexagonal habit —
    angular polyhedra with flat faces, NOT spheres (Bi 2020 Science; Kim
    2019 ACS Energy Lett).  Each particle gets 5–7 straight facets at
    INDEPENDENT inradii (per-facet irregularity), so every crystal is a
    unique convex polygon — realistic SEM habit, unlike idealised regular
    Voronoi cells.  Polycrystalline secondary particles (AM_P) stay circular
    (spheroidal agglomerate).  Base inradius is area-preserving (≈πr²); the
    facet ORIENTATION/shape is a literature-based habit, not measured.
    """
    rng = np.random.default_rng(int(seed) & 0xFFFFFFFF)
    n = int(rng.integers(5, 8))                          # 5–7 facets
    theta0 = rng.uniform(0, 2 * np.pi)
    r_in = r * np.sqrt(np.pi / (n * np.tan(np.pi / n)))  # area-preserving base
    jit = 1.0 + rng.uniform(-0.16, 0.16, n)              # per-facet irregularity

    # Build the sharp polygon radial profile R(θ), then circularly smooth it:
    # this ROUNDS the sharp corners (cusps in R) while leaving the flat faces
    # — single-crystal NCM shows faceted faces with smoothly rounded edges.
    M = 720
    tt = np.arange(M) * (2 * np.pi / M)
    rel = (tt - theta0) % (2 * np.pi)
    k = (np.floor(rel / (2 * np.pi / n)).astype(int)) % n
    local = rel - (k + 0.5) * (2 * np.pi / n)            # -π/n … π/n within facet
    R_sharp = (r_in * jit[k]) / np.cos(local)
    R_round = _ndi.gaussian_filter1d(R_sharp, sigma=M / (n * 7.0), mode='wrap')

    dx = GA - ac; dy = GB - bc
    rad = np.hypot(dx, dy)
    tha = np.arctan2(dy, dx) % (2 * np.pi)
    xp = np.concatenate([tt, [2 * np.pi]])
    fp = np.concatenate([R_round, [R_round[0]]])
    Rb = np.interp(tha.ravel(), xp, fp).reshape(tha.shape)
    return rad <= Rb


def slice_microstructure(case_dir: Path, slice_frac: float = 0.5,
                          n_pixels: int = 500, axis: str = 'y',
                          se_continuum: bool = True,
                          grain_size_um: float = 0.8,
                          single_crystal_facets: bool = True):
    """Rasterise one planar slice of a case into a 4-phase label grid.

    axis = slice-NORMAL direction:
      'z' → XY plane (horizontal cut, lateral view)
      'y' → XZ plane (vertical cross-section: x lateral, z through-thickness) ★
      'x' → YZ plane (vertical cross-section: y lateral, z through-thickness)
    For 'y'/'x' the vertical axis spans the full electrode thickness — the
    SEM-cross-section view most relevant for through-plane ionic transport.

    se_continuum=True merges discrete SE particles into a connected SE
    matrix (morphological closing) so void = genuine porosity only.

    Returns a dict, or None if data missing.
    """
    case_id = case_dir.name
    results_dir = ROOT / 'webapp' / 'results' / case_id
    atoms_csv = results_dir / 'atoms.csv'
    meta_file = case_dir / 'meta.json'
    ip_file = results_dir / 'input_params.json'
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

    # 3D-measured properties (full_metrics, %) → fractions.  Used to pin the
    # 2D figure to the 3D ground truth: void → porosity, coverage → coverage_AM.
    fm_file = results_dir / 'full_metrics.json'
    fm = json.loads(fm_file.read_text()) if fm_file.exists() else {}
    poro_3d = fm.get('porosity')
    target_void_frac = (float(poro_3d) / 100.0) if poro_3d is not None else None
    cov_3d = (fm.get('coverage_AM_mean_physics_rough')
              or fm.get('coverage_AM_mean_physics'))
    target_coverage_frac = (float(cov_3d) / 100.0) if cov_3d is not None else None

    df = pd.read_csv(atoms_csv)
    for col in ('x', 'y', 'z', 'radius', 'type', 'id'):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    xs = df['x'].to_numpy() * scale
    ys = df['y'].to_numpy() * scale
    zs = df['z'].to_numpy() * scale
    rs = df['radius'].to_numpy() * scale
    phases = np.array([_type_to_phase(type_map.get(int(t), ''))
                       for t in df['type'].to_numpy()])
    r_se_um = (ip.get('r_SE') or ip.get('r_SE_sim') or 0.0005) * scale

    # AM characteristic radii (D50) — use the analysis-summary value per case
    # (input_params r_AM_P/r_AM_S × scale), dynamic per case.  Fall back to the
    # median of the actual per-particle radii of that phase if not present.
    def _phase_d50(phase_id, ip_key):
        v = ip.get(ip_key) or ip.get(ip_key + '_sim')
        if v:
            return float(v) * scale
        rp = rs[phases == phase_id]
        return float(np.median(rp)) if rp.size else None
    r_amp_um = _phase_d50(AM_P, 'r_AM_P')
    r_ams_um = _phase_d50(AM_S, 'r_AM_S')

    z_min, z_max = float(np.nanmin(zs - rs)), float(np.nanmax(zs + rs))
    thickness = z_max - z_min

    # ── Assign in-plane axes (a horizontal, b vertical) + normal c ──────
    if axis == 'z':
        ca, cb, cc = xs, ys, zs                    # plot x-y, cut at z
        a_label, b_label = 'x (μm)', 'y (μm)'
        a_extent, b_extent = box_x_um, box_y_um
        c_min, c_max = z_min, z_max
    elif axis == 'x':
        ca, cb, cc = ys, zs, xs                    # plot y-z, cut at x
        a_label, b_label = 'y (μm)', 'z (μm)'
        a_extent, b_extent = box_y_um, thickness
        c_min, c_max = 0.0, box_x_um
    else:  # 'y' (default) — XZ vertical cross-section
        ca, cb, cc = xs, zs, ys                    # plot x-z, cut at y
        a_label, b_label = 'x (μm)', 'z (μm)'
        a_extent, b_extent = box_x_um, thickness
        c_min, c_max = 0.0, box_y_um

    c0 = c_min + slice_frac * (c_max - c_min)
    # For z-plot the b-axis origin is z_min; for x/y-plot it's also z_min.
    b_origin = z_min if axis in ('x', 'y') else 0.0

    # Pixel grid: a horizontal, b vertical
    nx = n_pixels
    ny = max(1, int(round(n_pixels * b_extent / a_extent)))
    pa = a_extent / nx
    pb = b_extent / ny

    labels   = np.zeros((ny, nx), dtype=np.int8)
    owner_dc = np.full((ny, nx), np.inf, dtype=np.float32)

    dc = np.abs(cc - c0)
    hit = dc < rs
    idx_hit = np.where(hit)[0]
    order = idx_hit[np.argsort(-dc[idx_hit])]

    # raw in-slice chord radii (for reporting the apparent vs D50 size)
    with np.errstate(invalid='ignore'):
        r_chord0 = np.sqrt(np.maximum(0.0, rs ** 2 - dc ** 2))

    for i in order:
        r_slice = float(np.sqrt(max(0.0, rs[i]**2 - (cc[i] - c0)**2)))
        if r_slice <= 0:
            continue
        ac, bc = ca[i], cb[i] - b_origin   # b coordinate relative to grid origin
        ix0 = max(0, int(np.floor((ac - r_slice) / pa)))
        ix1 = min(nx - 1, int(np.ceil((ac + r_slice) / pa)))
        iy0 = max(0, int(np.floor((bc - r_slice) / pb)))
        iy1 = min(ny - 1, int(np.ceil((bc + r_slice) / pb)))
        if ix1 < ix0 or iy1 < iy0:
            continue
        ga = (np.arange(ix0, ix1 + 1) + 0.5) * pa
        gb = (np.arange(iy0, iy1 + 1) + 0.5) * pb
        GA, GB = np.meshgrid(ga, gb)
        if single_crystal_facets and phases[i] == AM_S:
            inside = _faceted_inside(GA, GB, ac, bc, r_slice, seed=i)
        else:
            inside = (GA - ac) ** 2 + (GB - bc) ** 2 <= r_slice ** 2
        sub_dc = owner_dc[iy0:iy1+1, ix0:ix1+1]
        sub_lab = labels[iy0:iy1+1, ix0:ix1+1]
        win = inside & (dc[i] < sub_dc)
        sub_lab[win] = phases[i]
        sub_dc[win] = dc[i]

    # ── SE continuum: merge discrete SE → connected matrix ─────────────
    if se_continuum:
        r_se_px = max(1.0, r_se_um / pa)
        labels = _se_to_continuum(labels, r_se_px,
                                  target_void_frac=target_void_frac)

    # ── Morphology: AM_P polycrystalline grains, AM_S single-crystal ───
    # Trevisanello 2021 (Adv Energy Mater): polycrystalline NCM secondary
    # particle = many ~0.1–1 μm primary grains w/ grain boundaries;
    # single-crystal NCM = monolithic, no internal GB.
    # → grain_boundary mask drawn ONLY inside AM_P (AM_S stays solid).
    grain_boundary = np.zeros_like(labels, dtype=bool)
    if grain_size_um and grain_size_um > 0:
        grain_boundary = _am_p_grain_boundaries(labels, pa, pb, grain_size_um)

    # Phase fractions
    total = labels.size
    fracs = {PHASE_NAMES[p]: round(100 * np.sum(labels == p) / total, 2)
             for p in (VOID, AM_P, AM_S, SE)}

    # ── AM-SE interface (coverage) detection ──────────────────────────
    # An AM pixel on the boundary is "SE-covered" (active ionic interface)
    # if any 4-neighbour is SE; "uncovered" if it borders void/AM only.
    # Per-slice coverage % = covered AM-boundary / total AM-boundary —
    # the 2D analogue of the dashboard's cov_AM (SE-touching surface).
    is_am = (labels == AM_P) | (labels == AM_S)
    is_se = (labels == SE)
    # shifted neighbour SE presence
    se_up    = np.zeros_like(is_se); se_up[:-1, :]   = is_se[1:, :]
    se_down  = np.zeros_like(is_se); se_down[1:, :]  = is_se[:-1, :]
    se_left  = np.zeros_like(is_se); se_left[:, :-1] = is_se[:, 1:]
    se_right = np.zeros_like(is_se); se_right[:, 1:] = is_se[:, :-1]
    se_neighbour = se_up | se_down | se_left | se_right
    # AM boundary = AM pixel adjacent to a non-AM pixel (any direction)
    not_am = ~is_am
    nb_up    = np.zeros_like(not_am); nb_up[:-1, :]   = not_am[1:, :]
    nb_down  = np.zeros_like(not_am); nb_down[1:, :]  = not_am[:-1, :]
    nb_left  = np.zeros_like(not_am); nb_left[:, :-1] = not_am[:, 1:]
    nb_right = np.zeros_like(not_am); nb_right[:, 1:] = not_am[:, :-1]
    am_boundary = is_am & (nb_up | nb_down | nb_left | nb_right)
    am_covered  = am_boundary & se_neighbour     # AM perimeter touching SE
    am_uncov    = am_boundary & ~se_neighbour
    n_bnd = int(am_boundary.sum())
    coverage_inplane_pct = (round(100 * int(am_covered.sum()) / n_bnd, 2)
                            if n_bnd else 0.0)

    # ── Calibrate covered fraction to the 3D-measured coverage_AM ──────
    # In-plane adjacency underestimates 3D coverage: a 1-D perimeter samples
    # a 2-D surface, so SE lying just out-of-plane is missed.  We promote the
    # uncovered AM-boundary pixels CLOSEST to SE — the locations most likely
    # SE-covered out-of-plane (SE is a connected continuum) — until the
    # covered fraction equals coverage_AM (3D).  This pins the figure's
    # active-interface boundary condition to the same number COMSOL receives.
    if target_coverage_frac is not None and n_bnd:
        n_target = int(round(target_coverage_frac * n_bnd))
        n_promote = n_target - int(am_covered.sum())
        if n_promote > 0:
            uy, ux = np.where(am_uncov)
            if len(uy):
                dist_se = _ndi.distance_transform_edt(~is_se)
                order = np.argsort(dist_se[uy, ux])  # nearest-SE perimeter first
                sel = order[:min(n_promote, len(order))]
                am_covered[uy[sel], ux[sel]] = True
                am_uncov[uy[sel], ux[sel]]   = False
    coverage_pct = round(100 * int(am_covered.sum()) / n_bnd, 2) if n_bnd else 0.0

    # Interface label grid (for visualization): 0 none / 1 covered / 2 uncovered
    interface = np.zeros_like(labels)
    interface[am_covered] = 1
    interface[am_uncov]   = 2

    # Raw (pre-scale) in-slice median radius per AM phase — the chord-reduced
    # size before D50 calibration, reported so the slice effect is transparent
    # (raw ≤ D50 because a plane cuts spheres off-centre; we then scale ×D50/raw).
    def _app_med(pid):
        sel = (phases == pid) & hit & (r_chord0 > 0)
        return round(float(np.median(r_chord0[sel])), 3) if np.any(sel) else None
    r_amp_app = _app_med(AM_P)
    r_ams_app = _app_med(AM_S)

    return {
        'case_id': case_id, 'case_name': meta.get('name', case_id),
        'mode': meta.get('mode', ''), 'ps_ratio': meta.get('ps_ratio', ''),
        'labels': labels, 'interface': interface,
        'grain_boundary': grain_boundary, 'grain_size_um': grain_size_um,
        'axis': axis, 'se_continuum': se_continuum,
        'a_label': a_label, 'b_label': b_label,
        'a_extent': a_extent, 'b_extent': b_extent, 'b_origin': b_origin,
        'slice_at_um': c0, 'slice_frac': slice_frac,
        'thickness_um': thickness,
        'n_pixels': nx, 'pa_um': pa, 'pb_um': pb,
        'phase_fracs': fracs,
        'coverage_2d_pct': coverage_pct,                 # calibrated to 3D
        'coverage_2d_inplane_pct': coverage_inplane_pct, # raw in-plane only
        'coverage_3d_target_pct': (round(target_coverage_frac * 100, 2)
                                   if target_coverage_frac is not None else None),
        'n_am_boundary_px': n_bnd,
        'n_particles_hit': int(hit.sum()),
        # AM characteristic size (analysis-summary D50, per case) + apparent
        'r_AM_P_d50_um': (round(r_amp_um, 3) if r_amp_um else None),
        'r_AM_S_d50_um': (round(r_ams_um, 3) if r_ams_um else None),
        'r_AM_P_apparent_um': r_amp_app,
        'r_AM_S_apparent_um': r_ams_app,
    }


def render_png(data, out_path: Path):
    from matplotlib.patches import Patch
    labels = data['labels']
    interface = data['interface']
    fr = data['phase_fracs']
    a_ext, b_ext = data['a_extent'], data['b_extent']
    b0 = data['b_origin']
    # extent: a horizontal (0..a_ext), b vertical (b0..b0+b_ext)
    extent = [0, a_ext, b0, b0 + b_ext]
    aspect_h = b_ext / a_ext

    fig, axes = plt.subplots(1, 2, figsize=(15, 7 * max(0.4, aspect_h) + 1.5))

    # ── Panel 1: 4-phase microstructure ───────────────────────────────
    ax = axes[0]
    cmap = ListedColormap([PHASE_COLORS[p] for p in (VOID, AM_P, AM_S, SE)])
    norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], cmap.N)
    ax.imshow(labels, origin='lower', cmap=cmap, norm=norm,
               extent=extent, interpolation='nearest', aspect='equal')
    # AM_P polycrystalline grain boundaries overlay (Trevisanello 2021)
    gb = data.get('grain_boundary')
    gsz = data.get('grain_size_um', 0)
    if gb is not None and gb.any():
        gb_overlay = np.ma.masked_where(~gb, np.ones_like(labels))
        ax.imshow(gb_overlay, origin='lower',
                   cmap=ListedColormap(['#5b5b78']),   # subtle GB lines
                   extent=extent, interpolation='nearest', aspect='equal',
                   alpha=0.9)
    ax.set_xlabel(data['a_label']); ax.set_ylabel(data['b_label'])
    se_tag = ' (continuum)' if data['se_continuum'] else ' (discrete)'
    gb_tag = (f', AM_P poly grain ~{gsz}μm / AM_S single-xtal'
              if gb is not None and gb.any() else '')
    rP = data.get('r_AM_P_d50_um'); rS = data.get('r_AM_S_d50_um')
    appP = data.get('r_AM_P_apparent_um'); appS = data.get('r_AM_S_apparent_um')
    d50_bits = []
    if rP:
        d50_bits.append(f"AM_P D50 r={rP:.1f}μm" +
                        (f" (slice~{appP:.1f})" if appP else ""))
    if rS:
        d50_bits.append(f"AM_S D50 r={rS:.1f}μm" +
                        (f" (slice~{appS:.1f})" if appS else ""))
    d50_line = ('\n' + '   '.join(d50_bits)) if d50_bits else ''
    ax.set_title(f"4-phase microstructure{se_tag}{gb_tag}\n"
                 f"void {fr['void']}% / AM_P {fr['AM_P']}% / "
                 f"AM_S {fr['AM_S']}% / SE {fr['SE']}%{d50_line}", fontsize=10)
    # legend labels carry the analysis-summary D50 radius per AM phase
    r_by_phase = {AM_P: rP, AM_S: rS}
    def _lab(p):
        base = f'{PHASE_NAMES[p]} ({fr[PHASE_NAMES[p]]}%)'
        rr = r_by_phase.get(p)
        return base + (f', r={rr:.1f}μm' if rr else '')
    handles = [Patch(facecolor=PHASE_COLORS[p], edgecolor='gray', label=_lab(p))
               for p in (AM_P, AM_S, SE, VOID)]
    if gb is not None and gb.any():
        handles.append(Patch(facecolor='#5b5b78',
                              label='AM_P grain boundary'))
    ax.legend(handles=handles, loc='upper right', fontsize=8.5, framealpha=0.9)

    # D50 reference circles (analysis-summary radius, dashed) — true AM size,
    # for comparison against the chord-reduced particles in the slice.
    from matplotlib.patches import Circle
    x_cursor = 0.04 * a_ext
    y_base = b0 + 0.035 * b_ext
    for rr, col, name in [(rP, '#1a1a2e', 'AM_P'), (rS, '#8d99ae', 'AM_S')]:
        if not rr:
            continue
        cxr = x_cursor + rr
        ax.add_patch(Circle((cxr, y_base + rr), rr, fill=False, ec=col,
                            lw=1.8, ls='--', alpha=0.95, zorder=5))
        ax.text(cxr, y_base, f'{name} D50', ha='center', va='top',
                fontsize=7.5, color=col, weight='bold', zorder=5)
        x_cursor = cxr + rr + 0.05 * a_ext

    # ── Panel 2: AM-SE coverage (interface) map ───────────────────────
    ax = axes[1]
    cmap_b = ListedColormap(['#ffffff', '#e8e8ee', '#e8e8ee', '#faf3d0'])
    ax.imshow(labels, origin='lower', cmap=cmap_b,
               norm=BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], 4),
               extent=extent, interpolation='nearest', aspect='equal')
    cov_overlay = np.ma.masked_where(interface == 0, interface)
    cmap_ov = ListedColormap(['#10b981', '#ef4444'])
    ax.imshow(cov_overlay, origin='lower', cmap=cmap_ov,
               norm=BoundaryNorm([0.5, 1.5, 2.5], 2),
               extent=extent, interpolation='nearest', aspect='equal')
    ax.set_xlabel(data['a_label']); ax.set_ylabel(data['b_label'])
    tgt = data.get('coverage_3d_target_pct')
    inp = data.get('coverage_2d_inplane_pct')
    cov_sub = (f"coverage = {data['coverage_2d_pct']}%  (pinned to 3D {tgt}%)"
               if tgt is not None else f"2D coverage = {data['coverage_2d_pct']}%")
    cov_note = (f"\nin-plane only = {inp}%  →  +out-of-plane (nearest-SE)"
                if tgt is not None and inp is not None else "")
    ax.set_title(f"AM–SE interface (coverage)\n{cov_sub}  "
                 f"({data['n_am_boundary_px']} AM-boundary px){cov_note}",
                 fontsize=9.5)
    handles2 = [Patch(facecolor='#10b981', label=f"SE-covered ({data['coverage_2d_pct']}%)"),
                Patch(facecolor='#ef4444', label=f"uncovered ({round(100-data['coverage_2d_pct'],1)}%)"),
                Patch(facecolor='#faf3d0', edgecolor='gray', label='SE bulk'),
                Patch(facecolor='#e8e8ee', edgecolor='gray', label='AM bulk')]
    ax.legend(handles=handles2, loc='upper right', fontsize=8.5, framealpha=0.9)

    axis_desc = {'z': 'XY horizontal', 'y': 'XZ cross-section',
                 'x': 'YZ cross-section'}.get(data['axis'], data['axis'])
    fig.suptitle(
        f"{data['case_name']} — 2D microstructure ({axis_desc})  "
        f"(mode: {data['mode']}, ps: {data['ps_ratio'] or '—'}, "
        f"slice@{data['slice_at_um']:.1f}μm {data['slice_frac']:.0%}, "
        f"{data['n_pixels']}px / {data['pa_um']:.3f}μm·px⁻¹)",
        fontsize=11, y=1.0)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=130, bbox_inches='tight')
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cases', nargs='*', help='case names or "--all"')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--tier')
    ap.add_argument('--axis', choices=['z', 'y', 'x'], default='y',
                    help="slice-normal axis: 'y'=XZ cross-section (default, "
                         "through-thickness view), 'x'=YZ, 'z'=XY horizontal")
    ap.add_argument('--slice-frac', type=float, default=0.5,
                    help='slice position fraction along the normal axis (0-1, default 0.5)')
    ap.add_argument('--n-pixels', type=int, default=500)
    ap.add_argument('--slices', type=int, default=1,
                    help='# slices evenly spaced (overrides --slice-frac if >1)')
    ap.add_argument('--no-continuum', action='store_true',
                    help='keep SE as discrete particles (default: merge to continuum)')
    ap.add_argument('--grain-size', type=float, default=0.8,
                    help='AM_P polycrystalline primary grain size μm '
                         '(Trevisanello 2021 ~0.1-1μm; 0=off, AM_S always single-xtal)')
    ap.add_argument('--no-facets', action='store_true',
                    help='draw AM_S as plain circles (default: faceted '
                         'single-crystal habit; AM_P stays spheroidal)')
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

    fracs_list = ([args.slice_frac] if args.slices <= 1
                  else list(np.linspace(0.25, 0.75, args.slices)))

    print(f'Processing {len(candidates)} case(s), {len(fracs_list)} slice(s) '
          f'each, axis={args.axis}, continuum={not args.no_continuum}...')
    n_ok = 0
    for name, d in candidates:
        for zf in fracs_list:
            try:
                data = slice_microstructure(d, slice_frac=zf,
                                            n_pixels=args.n_pixels,
                                            axis=args.axis,
                                            se_continuum=not args.no_continuum,
                                            grain_size_um=args.grain_size,
                                            single_crystal_facets=not args.no_facets)
            except Exception as e:
                print(f'  [{name} z={zf:.2f}] FAILED: {type(e).__name__}: {e}')
                continue
            if not data:
                print(f'  [{name}] skip (missing data)')
                break
            tag = (f'{name}_{args.axis}' if len(fracs_list) == 1
                   else f'{name}_{args.axis}{zf:.2f}')
            np.save(out_npy_dir / f'{tag}.npy', data['labels'])
            render_png(data, out_png_dir / f'{tag}.png')
            fr = data['phase_fracs']
            print(f'  [{tag}] void {fr["void"]}% AM_P {fr["AM_P"]}% '
                  f'AM_S {fr["AM_S"]}% SE {fr["SE"]}%  '
                  f'| AM-SE coverage {data["coverage_2d_pct"]}%  '
                  f'({data["n_particles_hit"]} particles)')
            n_ok += 1

    print(f'\nDone — {n_ok} slices.')
    print(f'  PNG → {out_png_dir}')
    print(f'  NPY → {out_npy_dir}')


if __name__ == '__main__':
    main()
