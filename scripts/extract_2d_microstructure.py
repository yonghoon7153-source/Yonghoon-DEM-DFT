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


def synthesize_microstructure(case_dir: Path, n_pixels: int = 600,
                              grain_size_um: float = 0.8,
                              single_crystal_facets: bool = True,
                              seed: int = 0,
                              cov_off_p: float = 0.022, cov_off_s: float = 0.030,
                              bridge_dmax_um: float = 3.0):
    """Build a REPRESENTATIVE 2D microstructure from the 3D statistics
    (not a literal slice).

    A planar slice cannot show true particle D50 and the right area fractions
    at once (Wicksell).  Instead we synthesize: place AM particles whose size
    distribution has the analysis-summary D50 as its MEDIAN (variation kept)
    at the 3D-measured area fractions, fill a CONNECTED SE matrix, carve void
    pores to the porosity, and pin coverage to the 3D value.  AM_P = circular
    polycrystalline (grain boundaries), AM_S = faceted single crystal.  Result
    reproduces D50, φ_AM_P/φ_AM_S, porosity, coverage, and SE connectivity.
    """
    case_id = case_dir.name
    results_dir = ROOT / 'webapp' / 'results' / case_id
    meta_file = case_dir / 'meta.json'
    ip_file = results_dir / 'input_params.json'
    atoms_csv = results_dir / 'atoms.csv'
    fm_file = results_dir / 'full_metrics.json'
    if not meta_file.exists():
        return None
    meta = json.loads(meta_file.read_text())
    scale = meta.get('scale', 1000)
    type_map = {}
    for item in meta.get('type_map', '1:AM,2:SE').split(','):
        k, v = item.split(':')
        type_map[int(k)] = v.strip()
    ip = json.loads(ip_file.read_text()) if ip_file.exists() else {}
    fm = json.loads(fm_file.read_text()) if fm_file.exists() else {}

    box_x_um = (ip.get('box_x') or 0.05) * scale
    poro = float(fm.get('porosity') or 14.0) / 100.0
    phi_se = fm.get('phi_se')
    phi_se = float(phi_se) if phi_se is not None else 0.30
    def _cov(base):
        v = (fm.get(base + '_mean_physics_rough') or fm.get(base + '_mean_physics')
             or fm.get(base + '_mean'))
        return float(v) / 100.0 if v is not None else None
    cov_all = _cov('coverage_AM')
    cov_P = _cov('coverage_AM_P')                     # per-phase 3D coverage
    cov_S = _cov('coverage_AM_S')
    target_coverage_frac = cov_all                    # combined (reporting)
    thickness = float(fm.get('thickness_um') or box_x_um * 2)
    r_se_um = (ip.get('r_SE') or ip.get('r_SE_sim') or 0.0005) * scale

    # AM_P:AM_S split — use the DESIGN ps_ratio (7:3 is a VOLUME ratio, so
    # f_p = 7/(7+3) = 0.70); fall back to the atoms-measured volume split.
    def _parse_ps(s):
        try:
            a, b = str(s).split(':'); a = float(a); b = float(b)
            return a / (a + b) if (a + b) > 0 else None
        except Exception:
            return None
    f_p = _parse_ps(meta.get('ps_ratio')) or _parse_ps(fm.get('ps_ratio'))

    # AM radius distributions from the real atoms (kept for size variation)
    r_amp_arr = np.array([]); r_ams_arr = np.array([])
    if atoms_csv.exists():
        df = pd.read_csv(atoms_csv)
        for col in ('radius', 'type'):
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        rr = df['radius'].to_numpy() * scale
        ph = np.array([_type_to_phase(type_map.get(int(t), ''))
                       for t in df['type'].to_numpy()])
        r_amp_arr = rr[(ph == AM_P) & np.isfinite(rr)]
        r_ams_arr = rr[(ph == AM_S) & np.isfinite(rr)]
        if f_p is None:                              # fallback: measured split
            v_p = np.sum(r_amp_arr ** 3); v_s = np.sum(r_ams_arr ** 3)
            f_p = v_p / (v_p + v_s) if (v_p + v_s) > 0 else 0.7
    if f_p is None:
        f_p = 0.7

    def _d50_target(ip_key, arr):
        v = ip.get(ip_key) or ip.get(ip_key + '_sim')
        if v:
            return float(v) * scale
        return float(np.median(arr)) if arr.size else None
    r_amp_um = _d50_target('r_AM_P', r_amp_arr)
    r_ams_um = _d50_target('r_AM_S', r_ams_arr)

    # rescale the actual radius distribution so its median == analysis D50
    def _make_sampler(arr, target, rng):
        if arr.size and target:
            med = float(np.median(arr))
            scaled = arr * (target / med) if med > 0 else arr
            return lambda: float(rng.choice(scaled))
        if target:                                   # fallback: lognormal
            return lambda: float(target * np.exp(rng.normal(0, 0.22)))
        return None

    phi_am = max(0.0, 1.0 - poro - phi_se)
    phi_amp = phi_am * f_p
    phi_ams = phi_am * (1.0 - f_p)

    a_extent, b_extent = box_x_um, thickness
    nx = n_pixels
    ny = max(1, int(round(nx * b_extent / a_extent)))
    pa = a_extent / nx
    pb = b_extent / ny
    labels = np.zeros((ny, nx), dtype=np.int8)

    rng = np.random.default_rng(seed)
    sampler_p = _make_sampler(r_amp_arr, r_amp_um, rng)
    sampler_s = _make_sampler(r_ams_arr, r_ams_um, rng)

    # Random sequential addition, allowing modest overlap so AM particles
    # CONTACT (AM-AM boundaries → coverage < 100%, like a compacted electrode).
    # AM_P (large) placed first to its area target, then AM_S (small) nestles
    # into the gaps with a looser overlap budget so both phases hit target.
    pid = [0]
    particles = []                                   # (cx, cy, r_px) per particle
    def _place_phase(need_px, phase, sampler, faceted, gap_px, stale_max,
                     center_void=False, stratify_z=False):
        if not sampler or need_px <= 0:
            return
        placed = 0; stale = 0
        K = 8                                        # z-bands for stratified placement
        band_n = np.zeros(K)                         # particles placed per band
        band_stale = np.zeros(K, dtype=int)          # fails since last success per band
        BAND_SAT = 3000                              # band full once this many fails
        while placed < need_px and stale < stale_max:
            r_px = max(1.5, sampler() / pa)
            rem = need_px - placed                   # bound end-of-fill overshoot
            if rem > 0:
                rcap = (1.4 * rem / np.pi) ** 0.5
                if r_px > rcap:
                    r_px = max(1.5, rcap)
            if r_px > 0.48 * min(nx, ny):
                stale += 1; continue
            cx = rng.uniform(r_px, nx - r_px)
            band = -1
            if stratify_z:
                # fill the LEAST-occupied non-saturated z-band → even height
                # distribution without the round-robin trap (a full band can no
                # longer freeze the whole placement).
                avail = np.where(band_stale < BAND_SAT)[0]
                if avail.size == 0:
                    break
                mn = band_n[avail].min()
                band = int(rng.choice(avail[band_n[avail] == mn]))
                clo = max(r_px, band * ny / K)
                chi = min(ny - r_px, (band + 1) * ny / K)
                cy = rng.uniform(clo, chi) if chi > clo else rng.uniform(r_px, ny - r_px)
            else:
                cy = rng.uniform(r_px, ny - r_px)
            # NON-TOUCHING: require a thin SE gap around the particle so no two
            # AM share a boundary (electrons flow via the SE+additive matrix, so
            # AM-AM contact / AM percolation is not needed).  The footprint
            # dilated by `gap_px` must be entirely VOID.
            rg = r_px + gap_px
            x0 = max(0, int(np.floor(cx - rg))); x1 = min(nx, int(np.ceil(cx + rg)) + 1)
            y0 = max(0, int(np.floor(cy - rg))); y1 = min(ny, int(np.ceil(cy + rg)) + 1)
            ga = np.arange(x0, x1) + 0.5; gb = np.arange(y0, y1) + 0.5
            GA, GB = np.meshgrid(ga, gb)
            d2 = (GA - cx) ** 2 + (GB - cy) ** 2
            region = labels[y0:y1, x0:x1]
            ok = not (center_void and labels[int(cy), int(cx)] != VOID)
            if ok and np.any((region != VOID) & (d2 <= rg * rg)):   # would touch AM
                ok = False
            if ok:
                if faceted and single_crystal_facets:
                    pid[0] += 1
                    mask = _faceted_inside(GA, GB, cx, cy, r_px, seed=seed * 7919 + pid[0])
                else:
                    mask = d2 <= r_px ** 2
                new = mask & (region == VOID)
                ok = bool(new.any())
            if not ok:
                stale += 1
                if band >= 0:
                    band_stale[band] += 1
                continue
            region[new] = phase
            particles.append((cx, cy, r_px, float(phase)))
            placed += int(new.sum()); stale = 0
            if band >= 0:
                band_n[band] += 1; band_stale[band] = 0

    _place_phase(phi_amp * nx * ny, AM_P, sampler_p, False, 1.2, 60000,
                 stratify_z=True)
    _place_phase(phi_ams * nx * ny, AM_S, sampler_s, True, 1.0, 40000,
                 center_void=True)

    # ---- Coverage-driven porosity ---------------------------------------
    # The "uncovered" part of an AM surface is where it does NOT touch SE.  We
    # lay thin interfacial void patches on those parts so coverage is a real
    # geometric adjacency.  Each particle is treated INDIVIDUALLY (touching
    # particles are NOT merged), and its uncovered set is a multi-lobe angular
    # function + a per-particle bias — so coverage alternates SE/void around a
    # particle (초빨초빨), varies particle-to-particle, and some particles end
    # up fully isolated from SE (completely inactive).
    is_am0 = (labels == AM_P) | (labels == AM_S)
    na0 = ~is_am0
    nb0 = np.zeros_like(is_am0)
    nb0[:-1, :] |= na0[1:, :]; nb0[1:, :] |= na0[:-1, :]
    nb0[:, :-1] |= na0[:, 1:]; nb0[:, 1:] |= na0[:, :-1]
    am_bnd0 = is_am0 & nb0
    by, bx = np.where(am_bnd0)
    n_bnd0 = int(by.size)

    pore = np.zeros((ny, nx), dtype=bool)
    if (cov_all or cov_P or cov_S) is not None and n_bnd0 and particles:
        from scipy.spatial import cKDTree
        P = np.asarray(particles, dtype=float)        # (Np,4): cx, cy, r_px, phase
        Np = len(P)
        rngc = np.random.default_rng(seed + 999)
        bias = rngc.normal(0.0, 1.3, Np)              # per-particle activity
        ks = np.array([2.0, 3.0, 5.0])                # angular lobes
        amp = rngc.uniform(0.25, 0.75, (Np, 3))
        pha = rngc.uniform(0.0, 2 * np.pi, (Np, 3))
        idx = cKDTree(P[:, :2]).query(np.column_stack([bx, by]))[1]
        thb = np.arctan2(by - P[idx, 1], bx - P[idx, 0])
        g = bias[idx] + sum(amp[idx, k] * np.cos(ks[k] * thb + pha[idx, k])
                            for k in range(3))
        ph_px = labels[by, bx]                        # true phase at the pixel
        # per-phase threshold: AM_P and AM_S each hit their own 3D coverage
        # (+offset compensates for the 2-px shell widening the void contact)
        unc = np.zeros(len(g), dtype=bool)
        for phase_val, cov_t in ((AM_P, cov_P), (AM_S, cov_S)):
            cov_t = cov_t if cov_t is not None else cov_all
            if cov_t is None:
                continue
            sel = ph_px == phase_val
            if sel.any():
                off = cov_off_s if phase_val == AM_S else cov_off_p  # shell-widen comp.
                thr = np.quantile(g[sel], min(0.999, cov_t + off))
                unc[sel] = g[sel] > thr

        # Floating guard: every connected AM cluster must keep some SE contact
        # so it is anchored (not floating in void).  Cap each cluster's
        # uncovered rim — a lone particle therefore can't be 100% void-ringed,
        # while a particle wedged in a multi-particle cluster may still be fully
        # inactive (held by its neighbours).
        lab_am, _ = _ndi.label(is_am0)
        px_blob = lab_am[by, bx]
        BLOB_CAP = 0.90
        order = np.argsort(px_blob, kind='stable')
        blob_s = px_blob[order]; unc_o = unc[order]; g_o = g[order]
        ub = np.unique(blob_s)
        bnds = np.searchsorted(blob_s, np.append(ub, ub[-1] + 1))
        for i in range(len(ub)):
            a, b = bnds[i], bnds[i + 1]
            seg = unc_o[a:b]
            frac = seg.mean()
            if frac > BLOB_CAP:
                nflip = int(round((frac - BLOB_CAP) * (b - a)))
                loc = np.where(seg)[0]
                flip = loc[np.argsort(g_o[a:b][loc])[:nflip]]
                seg[flip] = False
                unc_o[a:b] = seg
        unc[order] = unc_o

        seed_mask = np.zeros((ny, nx), dtype=bool)
        seed_mask[by[unc], bx[unc]] = True
        shell = _ndi.binary_dilation(seed_mask, iterations=2) & na0
        pore |= shell                               # interfacial void

    need_void = int(round(poro * nx * ny))
    non_am = (labels == VOID)
    pr_max = max(2.0, r_se_um / pa * 2.0)
    dist_edge = _ndi.distance_transform_edt(non_am & ~pore)
    blocked = np.zeros_like(non_am)
    cy_, cx_ = np.where((non_am & ~pore) & (dist_edge > 1.5))
    if len(cy_):
        order = np.argsort(-dist_edge[cy_, cx_])
        for ci in order:
            if int(pore.sum()) >= need_void:
                break
            py, px = int(cy_[ci]), int(cx_[ci])
            if blocked[py, px]:
                continue
            room = float(dist_edge[py, px])
            r_target = 2.0 + (pr_max - 2.0) * rng.random() ** 1.6
            r_base = min(r_target, room - 0.5)
            if r_base < 1.5:
                continue
            a = rng.uniform(-1, 1, 3) * 0.12
            ph = rng.uniform(0, 2 * np.pi, 3)
            rmax = int(np.ceil(r_base * 1.4)) + 1
            yy0, yy1 = max(0, py - rmax), min(ny, py + rmax + 1)
            xx0, xx1 = max(0, px - rmax), min(nx, px + rmax + 1)
            gy, gx = np.ogrid[yy0 - py:yy1 - py, xx0 - px:xx1 - px]
            rr = np.hypot(gy, gx); th = np.arctan2(gy, gx)
            rb = r_base * (1 + a[0] * np.cos(th + ph[0]) + a[1] * np.cos(2 * th + ph[1])
                           + a[2] * np.cos(3 * th + ph[2]))
            m = ((rr <= rb) & non_am[yy0:yy1, xx0:xx1]
                 & (~pore[yy0:yy1, xx0:xx1]))
            if int(m.sum()) == 0:
                continue
            pore[yy0:yy1, xx0:xx1] |= m
            bm = int(rmax + 3)
            blocked[max(0, py-bm):min(ny, py+bm+1),
                    max(0, px-bm):min(nx, px+bm+1)] = True
    # non-AM, non-pore → SE matrix; pores stay VOID
    labels[(labels == VOID) & ~pore] = SE

    # Reconnect the SE network (ionic path).  In AM_S-dense cases the void
    # (interfacial shells + pores) chops SE into many local pockets that a
    # morphological closing alone cannot rejoin.  So: (1) light closing fills
    # thin AM necks, then (2) each remaining SE pocket within DMAX of the main
    # component is threaded to it with a short 2-px channel.  DMAX caps the
    # bridge length so this never draws the long cross-domain streaks the old
    # unconstrained threading did; pockets farther than DMAX (rare) are left.
    se = (labels == SE)
    labels[_ndi.binary_closing(se, iterations=2) & is_am0 & ~se] = SE
    se = (labels == SE)
    lab, ncomp = _ndi.label(se)
    if ncomp > 1:
        sizes = np.bincount(lab.ravel()); sizes[0] = 0
        main = int(sizes.argmax())
        dist_main, (iy, ix) = _ndi.distance_transform_edt(~(lab == main),
                                                          return_indices=True)
        DMAX = bridge_dmax_um / pa                   # bridge length cap (μm)
        for comp in range(1, ncomp + 1):
            if comp == main:
                continue
            ys, xs = np.where(lab == comp)
            k = int(np.argmin(dist_main[ys, xs]))    # pocket pixel nearest main
            if dist_main[ys[k], xs[k]] > DMAX:
                continue
            y0p, x0p = int(ys[k]), int(xs[k])
            y1p, x1p = int(iy[y0p, x0p]), int(ix[y0p, x0p])
            dy = abs(y1p - y0p); dx = abs(x1p - x0p)
            sy = 1 if y0p < y1p else -1
            sx = 1 if x0p < x1p else -1
            err = dx - dy; cy0, cx0 = y0p, x0p
            while True:
                for ddy in (0, 1):                   # 2-wide → 4-connected
                    for ddx in (0, 1):
                        labels[min(ny - 1, cy0 + ddy), min(nx - 1, cx0 + ddx)] = SE
                if cy0 == y1p and cx0 == x1p:
                    break
                e2 = 2 * err
                if e2 > -dy:
                    err -= dy; cx0 += sx
                if e2 < dx:
                    err += dx; cy0 += sy

    # AM_P polycrystalline grain boundaries (AM_S stays single crystal)
    grain_boundary = np.zeros_like(labels, dtype=bool)
    if grain_size_um and grain_size_um > 0:
        grain_boundary = _am_p_grain_boundaries(labels, pa, pb, grain_size_um)

    total = labels.size
    fracs = {PHASE_NAMES[p]: round(100 * np.sum(labels == p) / total, 2)
             for p in (VOID, AM_P, AM_S, SE)}

    # AM-SE coverage — GEOMETRIC: covered = AM perimeter touching SE,
    # uncovered = touching void/AM (the interfacial void shells above).
    # No pinning; the value falls out of the actual adjacency.
    is_am = (labels == AM_P) | (labels == AM_S)
    is_se = (labels == SE)
    se_n = np.zeros_like(is_se)
    se_n[:-1, :] |= is_se[1:, :]; se_n[1:, :] |= is_se[:-1, :]
    se_n[:, :-1] |= is_se[:, 1:]; se_n[:, 1:] |= is_se[:, :-1]
    not_am = ~is_am
    nb = np.zeros_like(not_am)
    nb[:-1, :] |= not_am[1:, :]; nb[1:, :] |= not_am[:-1, :]
    nb[:, :-1] |= not_am[:, 1:]; nb[:, 1:] |= not_am[:, :-1]
    am_boundary = is_am & nb
    am_covered = am_boundary & se_n
    am_uncov = am_boundary & ~se_n
    n_bnd = int(am_boundary.sum())
    coverage_pct = round(100 * int(am_covered.sum()) / n_bnd, 2) if n_bnd else 0.0
    coverage_inplane_pct = coverage_pct

    def _phase_cov(phase):
        pb = (labels == phase) & nb
        npb = int(pb.sum())
        return (round(100 * int((pb & se_n).sum()) / npb, 2) if npb else None)
    coverage_AM_P_pct = _phase_cov(AM_P)
    coverage_AM_S_pct = _phase_cov(AM_S)

    interface = np.zeros_like(labels)
    interface[am_covered] = 1
    interface[am_uncov] = 2

    return {
        'case_id': case_id, 'case_name': meta.get('name', case_id),
        'mode': meta.get('mode', ''),
        'ps_ratio': (meta.get('ps_ratio') or f"{round(f_p*10)}:{round((1-f_p)*10)}"),
        'labels': labels, 'interface': interface,
        'grain_boundary': grain_boundary, 'grain_size_um': grain_size_um,
        'axis': 'synth', 'se_continuum': True,
        'a_label': 'x (μm)', 'b_label': 'z (μm)',
        'a_extent': a_extent, 'b_extent': b_extent, 'b_origin': 0.0,
        'slice_at_um': 0.0, 'slice_frac': 0.0,
        'thickness_um': thickness,
        'n_pixels': nx, 'pa_um': pa, 'pb_um': pb,
        'phase_fracs': fracs,
        'coverage_2d_pct': coverage_pct,
        'coverage_2d_inplane_pct': coverage_inplane_pct,
        'coverage_3d_target_pct': (round(target_coverage_frac * 100, 2)
                                   if target_coverage_frac is not None else None),
        'coverage_AM_P_pct': coverage_AM_P_pct,
        'coverage_AM_S_pct': coverage_AM_S_pct,
        'coverage_AM_P_target_pct': (round(cov_P * 100, 2) if cov_P else None),
        'coverage_AM_S_target_pct': (round(cov_S * 100, 2) if cov_S else None),
        'n_am_boundary_px': n_bnd,
        'n_particles_hit': None,
        'r_AM_P_d50_um': (round(r_amp_um, 3) if r_amp_um else None),
        'r_AM_S_d50_um': (round(r_ams_um, 3) if r_ams_um else None),
        'r_AM_P_apparent_um': (round(r_amp_um, 3) if r_amp_um else None),
        'r_AM_S_apparent_um': (round(r_ams_um, 3) if r_ams_um else None),
        'synthetic': True,
    }


def _se_connectivity_pct(labels):
    """Largest SE connected component as % of all SE (ionic-network health)."""
    se = (labels == SE)
    n_se = int(se.sum())
    if n_se == 0:
        return 0.0
    lab, ncomp = _ndi.label(se)
    if ncomp <= 1:
        return 100.0
    sizes = np.bincount(lab.ravel()); sizes[0] = 0
    return round(100.0 * sizes.max() / n_se, 1)


def synthesize_calibrated(case_dir: Path, n_pixels: int = 600, seed: int = 0,
                          grain_size_um: float = 0.8, iters: int = 5,
                          cov_tol: float = 1.0, se_target: float = 95.0):
    """Closed-loop generate → measure → fine-tune.  Repeatedly synthesizes,
    measures per-phase AM-SE coverage and SE connectivity, and nudges the
    shell-widen offsets (toward the 3D coverage) and the SE bridge length
    (toward a connected network), keeping the best result.  Returns
    (best_data, report_rows)."""
    off_p, off_s, dmax = 0.022, 0.030, 3.0
    best, best_score, report = None, 1e18, []
    for it in range(max(1, iters)):
        d = synthesize_microstructure(case_dir, n_pixels=n_pixels, seed=seed,
                                      grain_size_um=grain_size_um,
                                      cov_off_p=off_p, cov_off_s=off_s,
                                      bridge_dmax_um=dmax)
        if d is None:
            return None, []
        cp, cs = d.get('coverage_AM_P_pct'), d.get('coverage_AM_S_pct')
        tp, ts = d.get('coverage_AM_P_target_pct'), d.get('coverage_AM_S_target_pct')
        se = _se_connectivity_pct(d['labels'])
        ep = (tp - cp) if (tp is not None and cp is not None) else 0.0
        es = (ts - cs) if (ts is not None and cs is not None) else 0.0
        report.append({'iter': it + 1, 'covP': cp, 'tgtP': tp, 'covS': cs,
                       'tgtS': ts, 'se_conn': se, 'off_p': round(off_p, 3),
                       'off_s': round(off_s, 3), 'dmax_um': round(dmax, 1)})
        score = abs(ep) + abs(es) + max(0.0, se_target - se)
        if score < best_score:
            best_score, best = score, d
        if abs(ep) <= cov_tol and abs(es) <= cov_tol and se >= se_target:
            break
        # nudge offsets toward target coverage; widen bridge if SE fragmented.
        # d(coverage%)/d(offset) ≈ 220, so Δoff = err/220 ≈ one-step correction
        # (gentle gain avoids the overshoot a /100 gain caused).
        off_p = float(min(0.2, max(0.0, off_p + ep / 220.0)))
        off_s = float(min(0.2, max(0.0, off_s + es / 220.0)))
        if se < se_target:
            dmax = min(8.0, dmax + 1.5)
    return best, report


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
                   cmap=ListedColormap(['#b6bac6']),   # clear gray GB lines
                   extent=extent, interpolation='nearest', aspect='equal',
                   alpha=1.0)
    ax.set_xlabel(data['a_label']); ax.set_ylabel(data['b_label'])
    se_tag = ' (continuum)' if data['se_continuum'] else ' (discrete)'
    gb_tag = (f', AM_P poly grain ~{gsz}μm / AM_S single-xtal'
              if gb is not None and gb.any() else '')
    rP = data.get('r_AM_P_d50_um'); rS = data.get('r_AM_S_d50_um')
    appP = data.get('r_AM_P_apparent_um'); appS = data.get('r_AM_S_apparent_um')
    is_syn = data.get('synthetic')
    d50_bits = []
    if rP:                                            # D50 = median diameter = 2·radius
        extra = f" (r={rP:.1f}μm)" if is_syn else (f" (slice~{appP:.1f})" if appP else "")
        d50_bits.append(f"AM_P D50 {2 * rP:.0f}μm{extra}")
    if rS:
        extra = f" (r={rS:.1f}μm)" if is_syn else (f" (slice~{appS:.1f})" if appS else "")
        d50_bits.append(f"AM_S D50 {2 * rS:.0f}μm{extra}")
    d50_line = ('\n' + '   '.join(d50_bits)) if d50_bits else ''
    ax.set_title(f"4-phase microstructure{se_tag}{gb_tag}\n"
                 f"void {fr['void']}% / AM_P {fr['AM_P']}% / "
                 f"AM_S {fr['AM_S']}% / SE {fr['SE']}%{d50_line}", fontsize=10)
    # legend labels carry the analysis-summary D50 (median DIAMETER) per AM phase
    r_by_phase = {AM_P: rP, AM_S: rS}
    def _lab(p):
        base = f'{PHASE_NAMES[p]} ({fr[PHASE_NAMES[p]]}%)'
        rr = r_by_phase.get(p)
        return base + (f', D50={2 * rr:.0f}μm' if rr else '')
    handles = [Patch(facecolor=PHASE_COLORS[p], edgecolor='gray', label=_lab(p))
               for p in (AM_P, AM_S, SE, VOID)]
    if gb is not None and gb.any():
        handles.append(Patch(facecolor='#b6bac6',
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
        ax.text(cxr, y_base, f'{name} D50 {2 * rr:.0f}μm', ha='center', va='top',
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
    if data.get('synthetic'):
        cp, cs = data.get('coverage_AM_P_pct'), data.get('coverage_AM_S_pct')
        cpt, cst = data.get('coverage_AM_P_target_pct'), data.get('coverage_AM_S_target_pct')
        # per-phase coverage is the matched quantity; headline it.  The combined
        # number is a length-weighted average and won't equal the 3D combined
        # (different weighting), so present it as an aside, not a "target".
        per = []
        if cp is not None:
            per.append(f"AM_P {cp}%" + (f" (→{cpt})" if cpt else ""))
        if cs is not None:
            per.append(f"AM_S {cs}%" + (f" (→{cst})" if cst else ""))
        cov_sub = " / ".join(per) + "   matched per-phase to 3D" if per else \
                  f"coverage = {data['coverage_2d_pct']}%"
        cov_note = (f"\ncombined (length-weighted) = {data['coverage_2d_pct']}%   ·   "
                    "uncovered = AM facing void/AM,  covered = AM facing SE")
    else:
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
    ap.add_argument('--procedural', action='store_true',
                    help='synthesize a representative microstructure from 3D '
                         'stats (AM D50-matched, area/porosity/coverage pinned) '
                         'instead of slicing')
    ap.add_argument('--seed', type=int, default=0, help='procedural RNG seed')
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
                if args.procedural:
                    data = synthesize_microstructure(
                        d, n_pixels=args.n_pixels, grain_size_um=args.grain_size,
                        single_crystal_facets=not args.no_facets, seed=args.seed)
                else:
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
