"""
export_comsol_2d.py — Phase D4.

3D DEM case → COMSOL 2D FEM 입력을 두 갈래로 분리 export:

  (1) 수치적 입력 (numerical) — COMSOL Global Parameters / Material로 직접
      타이핑할 3D-측정 유효 물성 스칼라:
        σ_ionic, σ_e, κ, τ_Laplace_eff, τ_Dijkstra, φ_SE, coverage,
        specific surface area, ASR, σ_grain(bulk) ...
      → parameters.csv  +  parameters.json

  (2) Geometry 입력 (geometric) — 2D microstructure 형상 (phase 경계):
        DXF (LWPOLYLINE, layer = phase) + SVG preview
      → geometry.dxf  +  geometry.svg  +  microstructure.npy

철학:
  • 형상(domain)은 geometry로, 물성은 수치로 — COMSOL 표준 workflow.
  • 2D-FEM이 3D 결과를 재현하려면, geometry는 2D인데 물성(τ, σ)은
    3D-network-solver에서 측정한 값을 그대로 입력 → 차원 보정이 물성에
    내포됨 (2D 단면 + 3D 유효 τ).

CLI:
  python3 scripts/export_comsol_2d.py input_6mAh_real_4
  python3 scripts/export_comsol_2d.py input_6mAh_real_4 --axis y --n-pixels 600
"""
from __future__ import annotations
import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import ndimage as _ndi

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from extract_2d_microstructure import (   # noqa: E402
    slice_microstructure, render_png as render_microstructure_png,
    VOID, AM_P, AM_S, SE, PHASE_NAMES,
)

SIGMA_GRAIN_MS = 3.0   # bulk LPSCl ionic conductivity (mS/cm)


def _fnum(d, *keys):
    for k in keys:
        v = d.get(k)
        if v is not None:
            try:
                return float(v)
            except (TypeError, ValueError):
                continue
    return None


def numerical_parameters(case_dir: Path, slice_data: dict) -> list[dict]:
    """Pull 3D-measured effective properties for COMSOL parameter input."""
    case_id = case_dir.name
    fm_file = ROOT / 'webapp' / 'results' / case_id / 'full_metrics.json'
    fm = json.loads(fm_file.read_text()) if fm_file.exists() else {}

    phi_se   = _fnum(fm, 'phi_se')
    sig_full = _fnum(fm, 'sigma_full_mScm_stage_e_physics',
                     'sigma_full_mScm_physics', 'sigma_full_mScm')
    sig_bulk = _fnum(fm, 'sigma_bulk_net_mScm')
    # τ_Laplace,eff = √(φ_SE × σ_grain / σ_full)  — COMSOL/EIS input
    tau_lap_eff = None
    if phi_se and sig_full and sig_full > 0:
        tau_lap_eff = (phi_se * SIGMA_GRAIN_MS / sig_full) ** 0.5
    tau_lap_bulk = None
    if phi_se and sig_bulk and sig_bulk > 0:
        tau_lap_bulk = (phi_se * SIGMA_GRAIN_MS / sig_bulk) ** 0.5

    fr = slice_data['phase_fracs']

    # ASR_ionic — full_metrics에 저장 안 됨 (on-the-fly).  L × 0.1 / σ_ionic.
    L_um = _fnum(fm, 'thickness_um')
    asr_ionic = None
    if L_um and sig_full and sig_full > 0:
        asr_ionic = L_um * 0.1 / sig_full   # Ω·cm²

    rows = [
        # name, value, unit, COMSOL parameter suggestion, source
        ('phi_SE',         phi_se,                                   '1',
         'phiSE', '3D SE volume fraction (ρ-weighted)'),
        ('phi_void',       _fnum(fm, 'porosity') and _fnum(fm, 'porosity')/100,
         '1', 'eps', '3D porosity (full_metrics)'),
        ('sigma_grain',    SIGMA_GRAIN_MS,                           'mS/cm',
         'sigma_grain', 'LPSCl bulk grain σ (constant)'),
        ('sigma_ionic_eff', sig_full,                                'mS/cm',
         'sigma_i', '★ 3D effective ionic σ (Stage E / network solver)'),
        ('sigma_e_eff',    _fnum(fm, 'electronic_sigma_full_mScm_stage_e_physics',
                                  'electronic_sigma_full_mScm_physics'), 'mS/cm',
         'sigma_e', '3D effective electronic σ'),
        ('kappa_eff',      _fnum(fm, 'thermal_sigma_full_mScm_stage_e_physics',
                                  'thermal_sigma_full_mScm_physics'), 'mS/cm-eq',
         'kappa', '3D effective thermal conductivity'),
        ('tau_Laplace_eff', tau_lap_eff,                             '1',
         'tau_eff', '★ 3D tortuosity (COMSOL/EIS input) = √(φ·σ_grain/σ_full)'),
        ('tau_Laplace_bulk', tau_lap_bulk,                           '1',
         'tau_bulk', '3D geometric tortuosity (no constriction)'),
        ('tau_Dijkstra',   _fnum(fm, 'tortuosity_recommended', 'tortuosity_mean'),
         '1', 'tau_geo', '3D geodesic tortuosity'),
        ('coverage_AM',    _fnum(fm, 'coverage_AM_mean_physics_rough',
                                  'coverage_AM_mean_physics'),        '%',
         'cov_AM', '★ 3D AM-SE coverage (Tabor shape-corrected)'),
        ('A_AM_SE_total',  _fnum(fm, 'area_AM_P_SE_total') or 0,      'um2',
         'A_AMSE', '3D total AM-SE interfacial area'),
        ('ASR_ionic',      asr_ionic,                                 'Ohm*cm2',
         'ASR_i', '3D cell-level ASR = L_cat × 0.1 / σ_ionic (Ohm slab)'),
        ('thickness',      _fnum(fm, 'thickness_um'),                 'um',
         'L_cat', 'cathode thickness (z extent)'),
        ('SE_SE_cn',       _fnum(fm, 'se_se_cn'),                     '1',
         'z_SESE', 'SE-SE coordination number'),
        ('percolation',    _fnum(fm, 'percolation_pct'),             '%',
         'perc', '3D SE percolation top↔bottom'),
        # 2D-slice geometry stats (for reference / sanity vs 3D)
        ('phi_SE_2Dslice',  fr['SE']/100,                            '1',
         '—', '2D slice SE area fraction (NOT for input — compare vs phi_SE)'),
        ('phi_void_2Dslice', fr['void']/100,                         '1',
         '—', '2D slice void area fraction'),
        ('coverage_2Dslice', slice_data['coverage_2d_pct'],          '%',
         '—', '2D figure AM-SE coverage (pinned to 3D coverage_AM)'),
        ('coverage_2Dslice_inplane', slice_data.get('coverage_2d_inplane_pct'), '%',
         '—', '2D raw in-plane coverage (pre-calibration; underestimates 3D)'),
    ]
    out = []
    for name, val, unit, comsol, src in rows:
        out.append({
            'parameter': name,
            'value': (round(val, 6) if isinstance(val, (int, float)) else ''),
            'unit': unit,
            'comsol_name': comsol,
            'source': src,
        })
    return out


def _clean_mask(mask: np.ndarray, min_area_px: int,
                fill_holes: bool = False) -> np.ndarray:
    """Drop connected components smaller than min_area_px (unmeshable specks
    that break a COMSOL import) and optionally fill small interior holes.

    fill_holes=True → solid domains (AM particles).
    fill_holes=False → keep interior pores (SE matrix porosity).
    """
    lbl, n = _ndi.label(mask)
    if n == 0:
        return mask
    sizes = np.bincount(lbl.ravel()); sizes[0] = 0
    out = (sizes >= min_area_px)[lbl]
    if fill_holes:
        out = _ndi.binary_fill_holes(out)
    return out


def _rdp(pts: np.ndarray, eps: float) -> np.ndarray:
    """Ramer–Douglas–Peucker polyline simplification (iterative, no recursion
    limit).  Removes the dense voxel-staircase vertices COMSOL chokes on."""
    n = len(pts)
    if n < 3:
        return pts
    keep = np.zeros(n, dtype=bool); keep[0] = keep[-1] = True
    stack = [(0, n - 1)]
    while stack:
        i0, i1 = stack.pop()
        if i1 <= i0 + 1:
            continue
        a = pts[i0]; ab = pts[i1] - a
        L2 = float(ab[0] ** 2 + ab[1] ** 2)
        seg = pts[i0 + 1:i1] - a
        if L2 == 0.0:
            d = np.hypot(seg[:, 0], seg[:, 1])
        else:
            t = (seg[:, 0] * ab[0] + seg[:, 1] * ab[1]) / L2
            d = np.hypot(seg[:, 0] - t * ab[0], seg[:, 1] - t * ab[1])
        if d.size == 0:
            continue
        k = int(np.argmax(d))
        if d[k] > eps:
            idx = i0 + 1 + k
            keep[idx] = True
            stack.append((i0, idx)); stack.append((idx, i1))
    return pts[keep]


def _chaikin(pts: np.ndarray, iters: int, closed: bool) -> np.ndarray:
    """Chaikin corner-cutting → smooth, rounded polyline (smears voxel steps)."""
    p = pts
    for _ in range(iters):
        if closed:
            a = p; b = np.roll(p, -1, axis=0)
        else:
            a = p[:-1]; b = p[1:]
        q = a + 0.25 * (b - a)
        r = a + 0.75 * (b - a)
        new = np.empty((len(q) + len(r), 2))
        new[0::2] = q; new[1::2] = r
        p = new if closed else np.vstack([pts[0], new, pts[-1]])
    return p


def _contours(mask: np.ndarray, pa: float, pb: float, b0: float,
              smooth: bool = True, min_area_px: int = 15,
              fill_holes: bool = False):
    """Extract SMOOTH iso-0.5 contours of a boolean mask as Nx2 arrays in μm.

    Voxel staircases are smeared into clean curves so the result is usable as
    a COMSOL geometry boundary: (1) prune unmeshable specks, (2) Gaussian
    sub-pixel iso-contour, (3) RDP vertex reduction, (4) Chaikin rounding.
    """
    m = _clean_mask(mask, min_area_px, fill_holes=fill_holes)
    if m.sum() == 0:
        return []
    work = _ndi.gaussian_filter(m.astype(float), sigma=1.0) if smooth \
        else m.astype(float)
    fig = plt.figure(); ax = fig.add_subplot(111)
    cs = ax.contour(work, levels=[0.5])
    segs = []
    allsegs = getattr(cs, 'allsegs', None)
    if allsegs:
        for level_segs in allsegs:
            for seg in level_segs:
                if len(seg) < 4:
                    continue
                xy = np.asarray(seg, dtype=float)
                closed = bool(np.allclose(xy[0], xy[-1]))
                if smooth:
                    xy = _rdp(xy, eps=0.6)
                    if len(xy) >= 4:
                        xy = _chaikin(xy, iters=2, closed=closed)
                xs = xy[:, 0] * pa
                ys = xy[:, 1] * pb + b0
                segs.append(np.column_stack([xs, ys]))
    plt.close(fig)
    return segs


def _classify_am_interface(labels, interface, pa, pb, b0):
    """Split AM particle outlines into SE-covered vs uncovered arc segments.

    Returns {'AM_SE_interface': [Nx2 …], 'AM_inactive': [Nx2 …]} as μm
    line-segment polylines.  COMSOL은 covered arc에만 Li+ flux BC를 줄 수
    있음 (active interface), uncovered는 insulated.

    Method: AM mask contour를 추출하고, 각 segment 중점의 interface label
    (1=covered / 2=uncovered)로 분류 → 같은 class 연속 segment를 묶음.
    """
    is_am = (labels == AM_P) | (labels == AM_S)
    am_contours = _contours(is_am, pa, pb, b0)
    covered_segs, inactive_segs = [], []

    ny, nx = labels.shape
    for cont in am_contours:
        # cont vertices in μm; convert back to pixel idx to read interface
        cur_class = None
        run = []
        for k in range(len(cont)):
            x_um, y_um = cont[k]
            ix = int(np.clip((x_um / pa), 0, nx - 1))
            iy = int(np.clip((y_um - b0) / pb, 0, ny - 1))
            lab = interface[iy, ix]
            # nearest interface class: search small window if 0
            if lab == 0:
                y0, y1 = max(0, iy-1), min(ny, iy+2)
                x0, x1 = max(0, ix-1), min(nx, ix+2)
                win = interface[y0:y1, x0:x1]
                nz = win[win > 0]
                lab = int(nz[0]) if nz.size else 1   # default covered
            cls = 'cov' if lab == 1 else 'inact'
            if cls != cur_class and run:
                (covered_segs if cur_class == 'cov' else inactive_segs).append(
                    np.array(run))
                run = [run[-1]] if run else []
            run.append((x_um, y_um))
            cur_class = cls
        if run and len(run) >= 2:
            (covered_segs if cur_class == 'cov' else inactive_segs).append(
                np.array(run))
    return {'AM_SE_interface': covered_segs, 'AM_inactive': inactive_segs}


def write_dxf(phase_contours: dict, interface_segs: dict, out_path: Path):
    """Write minimal ASCII DXF R12 with POLYLINE per contour, layered by
    phase + AM-SE interface (covered) + AM-inactive (uncovered).
    Hand-written (no ezdxf dependency)."""
    lines = []
    def w(code, val): lines.append(str(code)); lines.append(str(val))

    w(0, 'SECTION'); w(2, 'HEADER'); w(0, 'ENDSEC')
    w(0, 'SECTION'); w(2, 'TABLES'); w(0, 'TABLE'); w(2, 'LAYER')
    layer_color = {'AM_P': 1, 'AM_S': 3, 'SE': 2, 'void': 8,
                   'AM_SE_interface': 3, 'AM_inactive': 1}  # green / red
    for ph, color in layer_color.items():
        w(0, 'LAYER'); w(2, ph); w(70, 0); w(62, color); w(6, 'CONTINUOUS')
    w(0, 'ENDTAB'); w(0, 'ENDSEC')

    w(0, 'SECTION'); w(2, 'ENTITIES')
    # closed phase boundaries
    for ph, contours in phase_contours.items():
        for seg in contours:
            w(0, 'POLYLINE'); w(8, ph); w(66, 1); w(70, 1)   # closed
            for (x, y) in seg:
                w(0, 'VERTEX'); w(8, ph)
                w(10, f'{x:.4f}'); w(20, f'{y:.4f}'); w(30, '0.0')
            w(0, 'SEQEND')
    # open interface arcs (covered / inactive)
    for layer, segs in interface_segs.items():
        for seg in segs:
            if len(seg) < 2:
                continue
            w(0, 'POLYLINE'); w(8, layer); w(66, 1); w(70, 0)  # open
            for (x, y) in seg:
                w(0, 'VERTEX'); w(8, layer)
                w(10, f'{x:.4f}'); w(20, f'{y:.4f}'); w(30, '0.0')
            w(0, 'SEQEND')
    w(0, 'ENDSEC'); w(0, 'EOF')
    out_path.write_text('\n'.join(lines))


def write_svg(phase_contours: dict, interface_segs: dict,
              a_ext, b_ext, b0, out_path: Path):
    fill = {'AM_P': '#1a1a2e', 'AM_S': '#8d99ae', 'SE': '#f4d35e', 'void': 'none'}
    W, H = 800, max(1, int(800 * b_ext / a_ext))
    sx, sy = W / a_ext, H / b_ext
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}">',
             f'<rect width="{W}" height="{H}" fill="white"/>']
    # filled phase polygons
    for ph, contours in phase_contours.items():
        if ph == 'void':
            continue
        for seg in contours:
            pts = ' '.join(f'{x*sx:.2f},{H-(y-b0)*sy:.2f}' for (x, y) in seg)
            parts.append(f'<polygon points="{pts}" fill="{fill[ph]}" '
                         f'stroke="none" fill-opacity="0.85"/>')
    # interface arcs over the top: covered green, inactive red
    arc_color = {'AM_SE_interface': '#10b981', 'AM_inactive': '#ef4444'}
    for layer, segs in interface_segs.items():
        for seg in segs:
            if len(seg) < 2:
                continue
            pts = ' '.join(f'{x*sx:.2f},{H-(y-b0)*sy:.2f}' for (x, y) in seg)
            parts.append(f'<polyline points="{pts}" fill="none" '
                         f'stroke="{arc_color[layer]}" stroke-width="2"/>')
    parts.append('</svg>')
    out_path.write_text('\n'.join(parts))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('case')
    ap.add_argument('--axis', choices=['z', 'y', 'x'], default='y')
    ap.add_argument('--slice-frac', type=float, default=0.5)
    ap.add_argument('--n-pixels', type=int, default=600)
    ap.add_argument('--no-continuum', action='store_true')
    ap.add_argument('--grain-size', type=float, default=0.8,
                    help='AM_P poly grain μm (Trevisanello 2021); 0=off')
    ap.add_argument('--no-facets', action='store_true',
                    help='draw AM_S as plain circles (default: faceted single-crystal)')
    ap.add_argument('--out', default='docs/data/comsol_export')
    args = ap.parse_args()

    uploads = ROOT / 'webapp' / 'uploads'
    case_dir = None
    for d in uploads.iterdir():
        if not d.is_dir(): continue
        mf = d / 'meta.json'
        if mf.exists():
            try:
                if json.loads(mf.read_text()).get('name') == args.case:
                    case_dir = d; break
            except Exception:
                pass
    if case_dir is None:
        print(f'Case "{args.case}" not found', file=sys.stderr); sys.exit(1)

    print(f'Slicing {args.case} (axis={args.axis}, continuum={not args.no_continuum})...')
    sd = slice_microstructure(case_dir, slice_frac=args.slice_frac,
                              n_pixels=args.n_pixels, axis=args.axis,
                              se_continuum=not args.no_continuum,
                              grain_size_um=args.grain_size,
                              single_crystal_facets=not args.no_facets)
    if sd is None:
        print('slice failed (missing data)', file=sys.stderr); sys.exit(1)

    out_dir = ROOT / args.out / args.case
    out_dir.mkdir(parents=True, exist_ok=True)

    # ── (1) Numerical parameters ──────────────────────────────────────
    params = numerical_parameters(case_dir, sd)
    with open(out_dir / 'parameters.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['parameter', 'value', 'unit',
                                            'comsol_name', 'source'])
        w.writeheader(); w.writerows(params)
    (out_dir / 'parameters.json').write_text(
        json.dumps({p['parameter']: p for p in params}, indent=2))
    print(f'  수치 파라미터 → parameters.csv ({len(params)} rows)')

    # ── (2) Geometry — smooth phase contours (COMSOL-meshable) ─────────
    labels = sd['labels']
    pa, pb, b0 = sd['pa_um'], sd['pb_um'], sd['b_origin']
    # specks below this area can't be meshed cleanly → pruned
    min_area_px = max(12, int((sd['n_pixels'] / 110) ** 2))
    phase_contours = {}
    # AM particles = solid domains (fill interior holes); SE keeps its pores;
    # void = isolated pores exported as their own layer (for SE = Rect − AM −
    # void Boolean subtraction → watertight interfaces).
    for ph_id, ph_name, fill in [(AM_P, 'AM_P', True),
                                 (AM_S, 'AM_S', True),
                                 (SE,   'SE',   False),
                                 (VOID, 'void', False)]:
        mask = (labels == ph_id)
        if mask.sum() == 0:
            continue
        phase_contours[ph_name] = _contours(mask, pa, pb, b0,
                                            min_area_px=min_area_px,
                                            fill_holes=fill)
    n_seg = sum(len(v) for v in phase_contours.values())

    # coverage as geometry — split AM outline into covered / inactive arcs
    interface_segs = _classify_am_interface(labels, sd['interface'], pa, pb, b0)
    n_cov = len(interface_segs['AM_SE_interface'])
    n_ina = len(interface_segs['AM_inactive'])

    np.save(out_dir / 'microstructure.npy', labels)
    write_dxf(phase_contours, interface_segs, out_dir / 'geometry.dxf')
    write_svg(phase_contours, interface_segs, sd['a_extent'], sd['b_extent'],
              b0, out_dir / 'geometry.svg')
    # PNG preview — 2-panel (phase domain + AM-SE coverage interface)
    render_microstructure_png(sd, out_dir / 'geometry.png')
    print(f'  geometry → geometry.dxf + geometry.svg + geometry.png + microstructure.npy')
    print(f'    phase boundaries: {n_seg} polylines')
    print(f'    AM-SE coverage as geometry: {n_cov} covered arcs + '
          f'{n_ina} inactive arcs (2D coverage {sd["coverage_2d_pct"]}%)')

    # ── README ─────────────────────────────────────────────────────────
    readme = f"""COMSOL 2D import — {args.case}
=================================================================
COMSOL 모델은 (A) DOMAIN, (B) MATERIAL(수치), (C) BOUNDARY 로 구성.
이 export는 그 3가지에 각각 매핑되도록 분리:

  [A] DOMAIN (형상)      → geometry.dxf  (phase 영역)
  [B] MATERIAL (수치)    → parameters.csv (3D 유효 물성)
  [C] BOUNDARY (계면)    → geometry.dxf 의 AM_SE_interface / AM_inactive layer

─────────────────────────────────────────────────────────────────
[A] DOMAIN — Geometry → Import → geometry.dxf
─────────────────────────────────────────────────────────────────
  Layer AM_P  = 대입자 활물질 domain  (다결정, 원형, closed polyline)
  Layer AM_S  = 소입자 활물질 domain  (단결정, faceted+둥근 모서리)
  Layer SE    = 고체전해질 CONNECTED continuum domain (단일 연결망)
  void        = SE 내부의 고립 pore (closed polyline, SE 안의 구멍)

  ★ 경계는 모두 smoothing 처리됨 (Gaussian iso-contour + RDP + Chaikin)
    → voxel 계단 제거, COMSOL meshing 가능한 매끈한 polyline.
    작은 speck(메시 불가)은 자동 prune.

  ★ SE 연결성 보장: SE는 단일 percolating network로 만들어짐 (3D 99.5%
    percolation 반영).  단면이 끊어 보이는 건 slice artifact이므로 closing
    으로 복원함 — 끊긴 SE면 COMSOL 이온 도메인이 안 풀림.

  ★ 권장 SE 구성 (watertight 계면):
    COMSOL에서 SE domain = (외곽 Rectangle) − (AM_P ∪ AM_S ∪ void pores)
    의 Boolean Difference로 만들면 AM-SE 계면이 정확히 공유됨.
    (geometry.dxf의 SE layer는 시각/검산용; 위 방식이 mesh가 더 깨끗)

  축: {sd['a_label']} (가로) × {sd['b_label']} (세로)
  {'※ b축 = z = through-thickness (이온 전달 방향)' if args.axis in ('x','y') else '※ XY 수평 단면'}

─────────────────────────────────────────────────────────────────
[B] MATERIAL — Global Definitions → Parameters (parameters.csv)
─────────────────────────────────────────────────────────────────
  각 domain에 부여할 3D-측정 EFFECTIVE 물성.  2D 형상 위에 3D 유효
  물성을 올려서 2D-FEM이 3D 결과를 재현하게 함.

  SE domain:
    sigma_i  = σ_ionic effective (mS/cm)
    tau_eff  = τ_Laplace,eff   ← σ_eff = σ_grain / (φ·tau_eff²) 검산용
  AM domain:
    sigma_e  = σ_electronic (mS/cm),  kappa = thermal
  cell-level (post-processing 검증):
    ASR_i = L_cat / σ_ionic,  perc = percolation %

─────────────────────────────────────────────────────────────────
[C] BOUNDARY — coverage를 geometry로 (★ 사용자 요청)
─────────────────────────────────────────────────────────────────
  AM 입자 둘레가 두 layer로 분리됨:
    Layer AM_SE_interface  (green)  = SE에 닿은 활성 계면
        → Li+ flux / charge-transfer BC 부여 (electrode reaction)
    Layer AM_inactive      (red)    = void/AM에 닿은 비활성 둘레
        → insulated (no-flux) BC

  2D coverage = {sd['coverage_2d_pct']}%  (이 비율이 active 계면 길이 분율)
  → COMSOL에서 AM_SE_interface edge만 선택해 반응 경계조건 적용 가능.

─────────────────────────────────────────────────────────────────
설정: axis={args.axis} @ {sd['slice_at_um']:.1f}μm ({args.slice_frac:.0%}),
      {sd['n_pixels']}px / {pa:.3f} μm·px⁻¹,
      SE = {'continuum (입자 병합)' if not args.no_continuum else 'discrete particles'}

주의 (2D vs 3D): geometry는 2D, 물성은 3D-effective.  순수 2D-geometric
tortuosity가 필요하면 COMSOL이 형상에서 직접 계산하고, 3D 비교는
parameters.csv의 tau_eff(=3D 측정값)와 대조.
"""
    (out_dir / 'README.txt').write_text(readme)
    print(f'  README.txt 작성')
    print(f'\nDone → {out_dir}')


if __name__ == '__main__':
    main()
