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
import os as _os
import sys as _sys
import numpy as np

_THIS_DIR = _os.path.dirname(_os.path.abspath(__file__))
if _THIS_DIR not in _sys.path:
    _sys.path.insert(0, _THIS_DIR)
import se_material  # single source of truth for σ_ion(SE) + its temperature convention

_VC = None


class _SkipRequested(Exception):
    """사용자가 명시 플래그로 **끈** 것.  실패(`failed`)와 구분해서 잡는다 —
    `except Exception` 이 삼켜 "skipped (…)" 로 찍히면 원장에 거짓 진단이 남는다."""

# ── T1-e ─ 이온상 혼합-온도 판정 (SE 만 스케일하면 상 분율이 왜곡된다) ─────────────
# --temp-c 는 σ_ion(SE) 하나만 Kraft-2017 Arrhenius 로 올린다.  이온을 나르는 상이 SE 뿐이면
# 그것으로 충분하지만, SDCP(σ_ion>0, Li-hopping 폴리머)가 베드에 있으면 그 σ 는 T_ref 에 남아
# **σ_SDCP/σ_SE 비율 자체가 T-인자만큼 뒤틀린다** (45 °C → ÷2.56).  SDCP 에 LPSCl 의 Eₐ 를
# 이식하는 것은 §F1 날조이고, 그대로 두는 것은 왜곡 → 기본은 **차단**, 해제는 명시 플래그.
_T1E_SCALED_IONIC = ('SE (sid6)',
                     'SWCNT sheath (sid8 — SE-투명 규약이므로 SE 와 같은 σ·같은 T)')


def mixed_ionic_verdict(temp_c, sdcp_present, sigma_ion_sdcp, allow_mixed, ea_ev=None):
    """SE-만-스케일이 이온상 분율을 왜곡하는지 판정한다.

    반환 ``(blocked, note)``:
      blocked — True 면 호출부가 하드 차단해야 한다 (조용한 왜곡 금지, §F1).
      note    — provenance 에 실을 기록.  temp_c=None(기본) 이면 None → 기존 JSON 바이트 불변.
    """
    if temp_c is None:
        return False, None                                   # 기능 OFF = 기존 경로 그대로
    f = se_material.arrhenius_sigma_factor(temp_c, ea_ev)
    if not (sdcp_present and float(sigma_ion_sdcp) > 0.0):
        return False, {
            'status': 'CLEAN',
            'reason': ('이 런에서 σ_ion>0 로 이온망에 참여하는 상이 SE 계열뿐이다 (SDCP 미스탬프 / '
                       '--sigma-ion-sdcp 0 / 이온 솔브 미실행 중 하나) → 모든 이온상이 같은 T 에 있다'),
            'scaled_at_T': list(_T1E_SCALED_IONIC),
            'held_at_T_ref': [],
            'sigma_ion_T_factor': float(f),
        }
    return (not allow_mixed), {
        'status': 'DISTORTED',
        'reason': ('SE 만 Arrhenius 스케일되고 SDCP σ_ion 은 T_ref 에 남음 — SDCP 는 Li-hopping '
                   '폴리머라 LPSCl Eₐ 를 이식할 앵커가 없다 (§F1).  같이 올리면 날조, 안 올리면 왜곡.'),
        'scaled_at_T': list(_T1E_SCALED_IONIC),
        'held_at_T_ref': ['SDCP (sid5)'],
        'sigma_ion_T_factor': float(f),
        'sigma_sdcp_over_se_ratio_distortion_x': float(1.0 / f),
        'consequence': ('σ_ion_eff · ion_dissipation_share · STEP4 이온망이 전부 이 왜곡된 비율 위에서 '
                        '풀린다 — SDCP 원고(σ_SDCP 스윕)와 직접 비교 금지'),
        'released_by': '--allow-mixed-t-ionic (사용자 명시)' if allow_mixed else None,
    }


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
                            tol_am_um=0.10, band_um=0.15, vox_um=0.30, cond_phases=(2, 3, 5, 6)):
    """Per-AM ELECTRONIC connectivity to the current collector (floor) — the slide-19 quantity
    (연결/고립 입자).  Zeroth-order electron-transport physics = PERCOLATION on the conductive
    phases only:
      nodes  = AM spheres ∪ conductive-carbon clusters (phase 2 VGCF / 3 SuperP / 5 SDCP / 6 SWCNT sheath)
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


def _selftest_temperature():
    """T1-e (혼합-온도 이온상) + T1-a (npz 온도 계약) 회귀 테스트.

      python3 scripts/mpm_webapp_payload.py --selftest-temperature
    """
    ok = True

    def chk(name, cond, extra=''):
        nonlocal ok
        ok &= bool(cond)
        print(f"  {'PASS' if cond else 'FAIL'}  {name}{(' — ' + extra) if extra else ''}")

    # 1. 기본(--temp-c 미지정) = 판정 자체가 없음 → provenance 바이트 불변
    for _sd in (False, True):
        b, n = mixed_ionic_verdict(None, _sd, 0.001, False)
        chk(f'temp_c=None (sdcp={_sd}) → 차단 없음 + note None', (not b) and n is None)

    # 2. SDCP 가 없으면(또는 σ_ion_sdcp=0) 온도를 켜도 왜곡 없음 = CLEAN
    b, n = mixed_ionic_verdict(45.0, False, 0.001, False)
    chk('45 °C + SDCP 미스탬프 → CLEAN, 통과', (not b) and n['status'] == 'CLEAN')
    b, n = mixed_ionic_verdict(45.0, True, 0.0, False)
    chk('45 °C + SDCP 있으나 σ_ion_sdcp=0 → CLEAN, 통과', (not b) and n['status'] == 'CLEAN')

    # 3. ★핵심: SDCP 가 이온 전도상으로 있으면 기본 차단
    b, n = mixed_ionic_verdict(45.0, True, 0.001, False)
    chk('45 °C + SDCP 이온상 → 기본 BLOCKED', b and n['status'] == 'DISTORTED')
    f45 = se_material.arrhenius_sigma_factor(45.0)
    chk('왜곡 배수 = 1/f (SE 만 올라간 만큼 비율이 내려감)',
        abs(n['sigma_sdcp_over_se_ratio_distortion_x'] - 1.0 / f45) < 1e-12,
        f"1/f={1.0 / f45:.4f}")
    chk('차단 사유가 §F1 앵커 부재를 명시', 'F1' in n['reason'])

    # 4. 명시 해제 → 통과하되 DISTORTED 가 provenance 에 남는다 (라벨만 붙이는 것 아님)
    b, n = mixed_ionic_verdict(45.0, True, 0.001, True)
    chk('--allow-mixed-t-ionic → 통과 + DISTORTED 기록',
        (not b) and n['status'] == 'DISTORTED' and n['released_by'])

    # 5. Eₐ 밴드가 판정에 반영된다 (단일값 고정 아님)
    _, n_lo = mixed_ionic_verdict(45.0, True, 0.001, True, se_material.EA_ION_EV_MIN)
    _, n_hi = mixed_ionic_verdict(45.0, True, 0.001, True, se_material.EA_ION_EV_MAX)
    chk('Eₐ 밴드로 왜곡 배수가 달라짐 (0.29 < 0.41 < 0.46)',
        n_lo['sigma_ion_T_factor'] < f45 < n_hi['sigma_ion_T_factor'],
        f"x{n_lo['sigma_ion_T_factor']:.3f} < x{f45:.3f} < x{n_hi['sigma_ion_T_factor']:.3f}")

    # 6. npz 온도 계약 왕복 — payload 가 쓰는 형식 그대로 굽고 step4_dyn 이 읽는다
    import tempfile
    import step4_dyn as _s4
    with tempfile.TemporaryDirectory() as td:
        for t_c in (None, 45.0):
            p = _os.path.join(td, f'g_{t_c}.npz')
            prov = se_material.provenance(t_c)
            _tkw = {} if t_c is None else {'grid_temp_c': np.float64(t_c)}   # 실제 writer 와 동일
            np.savez_compressed(
                p, sid=np.zeros((2, 2, 2), np.int8),
                temperature_provenance=np.array(json.dumps(prov)), **_tkw)
            gt = _s4._grid_temperature(p)
            chk(f'npz 왕복 T_C={t_c} → step4_dyn 이 동일하게 읽음',
                gt['present'] and gt['T_C'] == t_c, str(gt['T_C']))
            chk(f'  └ T_C={t_c} 기본키 집합 유지 (grid_temp_c 는 온도 선언시에만)',
                ('grid_temp_c' in np.load(p, allow_pickle=False).files) == (t_c is not None))
        p0 = _os.path.join(td, 'legacy.npz')                 # 옛 그리드 = provenance 없음
        np.savez_compressed(p0, sid=np.zeros((2, 2, 2), np.int8))
        chk('옛 그리드(계약 없음) → present=False (조용한 25 °C 단정 금지 신호)',
            _s4._grid_temperature(p0)['present'] is False)

    #  ★★ 2026-08-19 — **기록 필드가 계산을 죽이면 안 된다**.
    #    실사고: 매니페스트에 `float(a.temp_c)` 를 넣었는데 `--temp-c` 의 기본이 None 이라
    #    TypeError 로 죽었다.  하필 죽는 자리가 **σ_e 솔브(2,474 s)가 끝난 뒤**여서 GPU
    #    시간을 통째로 버렸다.  ⇒ 새로 넣은 기록 필드 전부를 **None 입력**으로 건다.
    _NONE_SAFE = ('sigma_ion_se', '_sigma_ion_se_ref', 'sigma_ion_sdcp',
                  'sigma_am_s', 'sigma_am_p', 'temp_c', 'ea_ion_ev')
    try:
        _rec = {k: _mflt(None) for k in _NONE_SAFE}
        _rec['cam'] = None if None is None else str(None)
        _rec['mpm_seed'] = _mint(None)
        _rec['se_E_GPa'] = _mflt(None)
        import json as _js
        _js.dumps(_rec)                       # 직렬화까지 되어야 payload 가 저장된다
        _n_ok = all(v is None for v in _rec.values())
    except Exception as _e:                                        # noqa: BLE001
        print(f'  FAIL  기록 필드가 None 에서 터진다: {_e}')
        ok = False
        _n_ok = False
    print(('  PASS  ' if _n_ok else '  FAIL  ')
          + '기록 필드 전부 None-안전 + JSON 직렬화 가능 (계산을 죽이지 않는다)')
    ok = ok and _n_ok
    #  ★ 0.0 을 None 으로 접지 않는지도 건다 (`or` 로 쓰면 0 이 사라진다).
    _z_ok = (_mflt(0.0) == 0.0) and (_mint(0) == 0)
    print(('  PASS  ' if _z_ok else '  FAIL  ')
          + f'0 은 0 으로 남는다 (_mflt(0.0)={_mflt(0.0)!r} · _mint(0)={_mint(0)!r})')
    ok = ok and _z_ok
    #  ── ★★ PTFE 스탬프 규약 (CDXR2-2 / CDXR2-6) ──────────────────────────────────────
    def _p(label, cond):
        nonlocal ok
        print(('  PASS  ' if cond else '  FAIL  ') + label)
        ok = ok and bool(cond)

    _p('ptfe-legacy-on  옛 규약: 요청 없음 + σ>0 → centerline (CL-49 재현성 보존)',
       resolve_ptfe_stamp('', 1e-16) == ('centerline', True))
    _p('ptfe-legacy-off 옛 규약: 요청 없음 + σ=0 → off (생산 기본 불변)',
       resolve_ptfe_stamp('', 0.0) == ('off', True))
    _p('ptfe-explicit   ★ 명시 요청은 σ 를 **보지 않는다** — centerline+σ=0 = exact-zero DOF',
       resolve_ptfe_stamp('centerline', 0.0) == ('centerline', False)
       and resolve_ptfe_stamp('off', 250.0) == ('off', False))
    _p('ptfe-reserved   ★ capsule 은 예약값이다 (centerline 별칭 금지)',
       'capsule' in PTFE_STAMPS_RESERVED and 'capsule' in PTFE_STAMPS)
    #  ★ 이 검사가 요점이다 — 누가 capsule 을 구현하면서 직경 배선을 잊으면 여기서 걸린다.
    _p('ptfe-dia-gate   ★★ 예약 해제된 규약은 전부 직경 배선을 갖춰야 한다',
       all(r in PTFE_STAMP_NEEDS_DIA for r in PTFE_STAMPS_RESERVED))
    import os as _os_mod
    _txt = open(_os_mod.path.abspath(__file__), encoding='utf-8').read()
    #  ⚠ needle 을 **쪼개서** 만든다 — 통짜로 적으면 이 줄 자신이 파일에 들어가
    #    검사가 스스로를 잡는다 (자기참조).  실제로 초판이 그렇게 실패했다.
    _old_gate = 'if a.sigma_ptfe > 0 else ' + '(2, 3, 5, 6)'
    _p('ptfe-gate-split ★ _cond_ph 가 σ 가 아니라 규약으로 갈린다 (옛 결함 회귀)',
       "_ptfe_stamp != 'off'" in _txt and _old_gate not in _txt)
    _p('ptfe-dia-early  ★ --fibre-dia 를 solve **전에** 읽는다 (뷰어 블록은 재사용)',
       '_dia_all = np.load(a.fibre_dia)' in _txt and 'dia = _dia_all' in _txt)

    print('PAYLOAD TEMPERATURE SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1




def _sha256_file(path, _chunk=1 << 22):
    """파일 내용의 sha256 (앞 16 hex).  없거나 못 읽으면 None.

    ★ 2026-08-20 (Codex CDX-IJ-02 → CDXIJ-10 ③) — "pair 간 σ_ion 만 바뀌었다" 를 기계가
      확인하려면 **입력이 같다** 는 증거가 있어야 한다.  경로·크기·mtime 은 증거가 아니다
      (같은 이름으로 다른 침대를 놓을 수 있다) — 내용 해시여야 한다.
    ⚠ 비용: se_dump.npy 가 1~2 GB 라 팔당 수 초.  8팔이면 수십 초 — 솔브(수천 초) 앞에서
      무시 가능하고, 그 대가로 침대 바뀜이 **조용히** 지나가지 않는다.
    """
    import hashlib as _hl
    if not path or not _os.path.exists(path):
        return None
    try:
        h = _hl.sha256()
        with open(path, 'rb') as f:
            for blk in iter(lambda: f.read(_chunk), b''):
                h.update(blk)
        return h.hexdigest()[:16]
    except OSError:
        return None


def _code_sha(script_dir):
    """이 코드가 어느 커밋인가 (+ dirty 여부).  git 이 없으면 None.

    ⚠ dirty 면 `<sha>+dirty` — 커밋 안 된 수정으로 돈 런은 재현 불가임을 **드러낸다**.
    """
    import subprocess as _sp
    try:
        sha = _sp.run(['git', '-C', script_dir, 'rev-parse', '--short', 'HEAD'],
                      capture_output=True, text=True, timeout=10)
        if sha.returncode != 0:
            return None
        st = _sp.run(['git', '-C', script_dir, 'status', '--porcelain'],
                     capture_output=True, text=True, timeout=20)
        dirty = bool((st.stdout or '').strip())
        return sha.stdout.strip() + ('+dirty' if dirty else '')
    except Exception:                                          # noqa: BLE001
        return None


def _mflt(v):
    """metrics 값 → float, 없으면 None.  ★ 0.0 을 None 으로 만들면 안 되므로 `or` 금지."""
    return None if v is None else float(v)


def _mint(v):
    """metrics 값 → int, 없으면 None (seed 0 이 유효값이라 `or` 금지)."""
    return None if v is None else int(v)


def finite_belt(obj, path='$', found=None):
    """payload 안의 NaN/Inf 를 None 으로 바꾸고 **바꾼 경로를 돌려준다** → (clean, paths).

    ★ RC7-01 (Codex 7회차): `json.dump` 기본값 allow_nan=True 는 RFC 8259 에 없는
      `NaN` / `Infinity` **토큰**을 그대로 쓴다 → 브라우저 `JSON.parse` 가 payload 전체를
      거부한다 (수 분짜리 STEP3 결과가 통째로 못 읽히는 형태의 실패).  이 파일은 곳곳에서
      ad-hoc `np.nan_to_num` 을 걸어왔지만 한 군데만 빠져도 같은 일이 난다 ⇒ 쓰기 직전에
      **한 번** 전수 검사한다.  조용히 고치지 않고 경로를 기록하는 것이 요점이다.
    ⚠ np.float32 는 파이썬 float 의 서브클래스가 **아니다** — np.floating 도 함께 본다.
    """
    if found is None:
        found = []
    if isinstance(obj, (float, np.floating)):
        v = float(obj)
        if v != v or v in (float('inf'), float('-inf')):
            found.append(path)
            return None, found
        return v, found
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            out[k], found = finite_belt(v, f'{path}.{k}', found)
        return out, found
    if isinstance(obj, (list, tuple)):
        out = []
        for i, v in enumerate(obj):
            w, found = finite_belt(v, f'{path}[{i}]', found)
            out.append(w)
        return out, found
    return obj, found

#: ★ 직경 인식 PTFE 스탬프 규약 (CDXR2-2).  여기 있는 규약은 per-fibril 직경 없이
#  돌면 **안 된다** — 직경 없이 돌면 요청과 다른 규약(1-셀 선분)을 재게 된다.
#  ⚠ `capsule` 은 아직 예약값이라 parse 직후 중단되므로 그 게이트는 아직 발화하지 않는다.
#    구현이 들어올 때 이 목록이 fail-open 을 막는 자리다.
PTFE_STAMP_NEEDS_DIA = ('capsule',)

#: ★★★ **물리 규약 정체성** (CDXR3-3, 종료조건 ③④).  `schema_version` 은 **파일 구조**,
#   이것은 **물리 의미**다 — 둘 중 하나가 다른 하나를 대신하지 못한다 (Codex).
#   여기 적힌 인자가 하나라도 다르면 **다른 규약**이고, 그 결과는 섞으면 안 된다.
#   ⚠ 값은 **적용된 것**(applied)이지 요청값이 아니다.  요청↔적용 불일치는 별 필드로 남긴다.
#  ★★ 2026-08-25 (Codex 재리뷰 조건 4) — 둘을 **더 넣는다**.
#    · `periodic_xy` : x·y 경계 규약.  seam 면이 회로에 들어가는지가 달라진다 (Codex #7)
#      — 물리 인자인데 규약 해시에 없어서 주기 팔과 비주기 팔이 섞여도 안 걸렸다.
#    · `plate_rule`  : 플레이트 결합 규약 판 (`step3_sigma.PLATE_RULE_VERSION`).
#      CDXR3-6 이 이 규칙을 바꿔 **σ_e 절대값이 바뀌었다** — 옛 판 산출물과 새 판
#      산출물은 같은 침대·같은 vox 라도 다른 수를 낸다.  섞이면 안 되므로 해시에 넣는다.
#  ⚠ 축을 늘리면 **모든 id 가 바뀐다**.  그것이 의도다 — 규약이 실제로 달라졌으므로
#    옛 팔과 새 팔은 다른 실험이고, 판정기가 그것을 섞지 못하게 해야 한다.
PROTOCOL_FIELDS = ('vox_um', 'bridge_um', 'fibre_stamp', 'sdcp_stamp', 'sdcp_sphere_d_um',
                   'sdcp_yield_to_vgcf', 'ptfe_stamp', 'ptfe_zero_dof',
                   'sigma_vgcf_S_cm', 'sigma_sdcp_S_cm', 'sigma_ptfe_S_cm',
                   'sigma_ion_se_S_cm', 'sigma_ion_sdcp_S_cm',
                   'sigma_am_s_S_cm', 'sigma_am_p_S_cm', 'cam', 'temp_c',
                   'periodic_xy', 'plate_rule')


def physics_protocol_id(man):
    """적용된 규약 dict → 안정 해시 문자열.  **선언이 아니라 결과**다.

    ★ 왜 (Codex CDXR3-3): 러너가 요청한 규약과 payload 가 실제로 적용한 규약을
      **end-to-end 로 대조할 방법이 없었다**.  `_ptscenterline` OUTDIR 에서 모든 팔이
      조용히 `off` 로 돌아도 서로만 같으면 초록이었다.
    ⚠ 값이 하나라도 **없으면** 규약을 확정할 수 없다 → `unknown:<빠진 필드>` 를 낸다
      (임의 기본값으로 채우지 않는다 — 그것이 fail-open 이다)."""
    import hashlib as _hl
    #  ★★ 2026-08-25 (M-R3-02, Codex 재리뷰) — **`None` 이 곧 missing 은 아니다.**
    #    `temp_c=None` 은 "온도 기능 OFF" 라는 **유효값**이고 생산 기본이다 (러너가
    #    `--temp-c` 를 안 준다).  옛 판은 그것을 missing 으로 읽어 정상 16팔이 전부
    #    `unknown:temp_c` 가 됐고, 내가 넣은 게이트가 그것을 HOLD 로 잡았다 =
    #    **내가 만든 생산 과잉차단**.  ⇒ OFF 가 정당한 축은 sentinel 로 정규화한다.
    _OFF_OK = ('temp_c',)          # None = 명시적 OFF 인 축
    _v = {}
    for k in PROTOCOL_FIELDS:
        if man.get(k) is None and k in _OFF_OK:
            _v[k] = '__OFF__'      # 값이 없는 것과 **끈 것**을 구분해 해시에 넣는다
        else:
            _v[k] = man.get(k)
    _miss = [k for k in PROTOCOL_FIELDS if _v[k] is None]
    if _miss:
        return 'unknown:' + ','.join(sorted(_miss))
    _canon = json.dumps(_v, sort_keys=True,
                        ensure_ascii=False, separators=(',', ':'))
    return 'p1-' + _hl.sha256(_canon.encode('utf-8')).hexdigest()[:16]

#: PTFE 스탬프 규약 이름들.  '' = 옛 규약 유도 (매니페스트에 legacy-unversioned).
PTFE_STAMPS = ('off', 'centerline', 'capsule')
#: 아직 구현되지 않은 예약값 — 고르면 **중단**한다 (centerline 별칭 금지, Codex Q3).
PTFE_STAMPS_RESERVED = ('capsule',)


def resolve_ptfe_stamp(requested, sigma_ptfe):
    """(요청, σ_PTFE) → (적용 규약, 옛 규약 유도인가).

    ★ **스탬프 여부와 전도도는 다른 축이다** (CDXR2-6).  옛 게이트는 둘을 묶어
    `sigma_ptfe > 0` 일 때만 찍었고, 그래서 "격자에 그리되 절연으로" 를 표현할 방법이
    없었다 — CL-49 가 `1e-16` 우회로를 쓴 이유다 (σ 대비 1e18 = 조건수 파괴).
    솔버는 이미 `cond = sig > 0` 이라 σ=0 셀을 dof 에서 빼므로, 게이트만 떼면
    `centerline + σ=0` 이 **exact-zero DOF** 가 된다.

    ⚠ 옛 호출부 호환: 요청이 비면 σ 로 유도하고 `legacy=True` 를 돌려준다.
      그 팔은 매니페스트에 `legacy-unversioned` 로 적혀 새 세대와 섞이지 않는다."""
    if requested:
        return requested, False
    return ('centerline' if float(sigma_ptfe or 0.0) > 0 else 'off'), True


def _payload_reject_reason(a, step3):
    """의미적으로 실패한 payload 인가 → 사유 문자열 (없으면 None).

    ★ 2026-08-25 (R3-F2): 이 판정은 **최종 파일명에 게시하기 전에** 나야 한다.
      게시 뒤에 죽으면 실패 산출물이 성공 이름으로 남고 러너 캐시가 그것을 재사용한다."""
    #  ★★★ 2026-08-25 (CDXR3-2) — **required component 실패를 process exit 로 전파한다.**
    #    이것이 R-1 의 원래 요구다.  러너의 `check_arm` 은 2차 방어이지 대체가 아니다 —
    #    Codex 가 partial/missing·backend 위장 mutant 로 8팔 최종 봉인까지 통과시켰다.
    #    ⚠ STEP3 를 **요청하지 않은** 런(`--no-step3`)은 대상이 아니다 (disabled 는 실패가 아니다).
    #  ⚠⚠ **aggregate `partial` 로 판단하면 안 된다** — `--no-ion` 처럼 **의도적으로 끈**
    #    component 도 `disabled` 라서 aggregate 가 `partial` 이 된다.  초판이 그렇게 짜서
    #    규칙 J 스모크(그리고 실제 LEAN=2 생산 스윕 팔 전부)를 거부했다.
    #    ⇒ Codex 가 말한 대로 **required 를 run mode 에서 파생**하고 그것만 본다.
    #      required = electronic(항상) + ionic(--no-ion 이 아닐 때).
    _m = (step3 or {}).get('manifest') if isinstance(step3, dict) else None
    if not isinstance(_m, dict):
        return None
    if getattr(a, '_protocol_expect', ''):
        _got = _m.get('physics_protocol_id')
        if _got != a._protocol_expect:
            return (f'PROTOCOL_MISMATCH: 물리 규약 불일치 — 기대 `{a._protocol_expect}` · '
                    f'적용 `{_got}`.  러너가 요청한 규약과 payload 가 실제로 한 것이 갈렸다')
    #  ★★ 조건 4 — 러너가 **자기 설정으로** 선언한 물리 인자와 적용값을 필드별로 맞춘다.
    #    문자열로 비교한다 (선언은 CLI 텍스트다): `0.15` ↔ `0.15`, `True` ↔ `True`.
    #    ⚠ 부동소수 표기 차이(`0.15` vs `0.150`)는 float 로도 한 번 더 본다.
    _pe = getattr(a, '_physics_expect', None) or {}
    for _k, _want in _pe.items():
        _got = _m.get(_k)
        if str(_got) == _want:
            continue
        try:
            if abs(float(_got) - float(_want)) <= 1e-12 * max(1.0, abs(float(_want))):
                continue
        except (TypeError, ValueError):
            pass
        return (f'PROTOCOL_MISMATCH: 러너가 선언한 `{_k}` = {_want!r} 인데 적용된 것은 '
                f'{_got!r} — 요청↔적용이 갈렸다.  ⚠ 이 대조는 **첫 팔이 아니라 러너 자신의 '
                f'설정**을 기준으로 한다 (첫 팔을 베끼면 첫 팔이 진리가 된다)')
    if _m.get('status') == 'disabled':
        return None
    _req = ['electronic'] + ([] if a.no_ion else ['ionic'])
    _cmp = _m.get('components') or {}
    #  ★ 2026-08-25 (Codex 재리뷰 조건 7) — **required 만 센다.**  초판은 `failed`/`missing`
    #    목록을 통째로 붙여, `--no-ion --no-thermal` 런에서 사유가
    #    `['electronic', 'ionic(missing)', 'pnm(missing)', 'pore(missing)', 'thermal(missing)']`
    #    처럼 나왔다 — **원인 하나가 잡음 넷에 묻힌다**.  required 밖은 애초에 요구가 아니다.
    _bad = [f'{c}({(_cmp.get(c) or {}).get("status") or "absent"})' for c in _req
            if not isinstance(_cmp.get(c), dict) or _cmp[c].get('status') != 'complete']
    _bad += [f'{c}(failed)' for c in (_m.get('failed') or []) if c in _req]
    _bad += [f'{c}(missing)' for c in (_m.get('missing') or []) if c in _req]
    if _bad and not a.allow_partial_step3:
        #  ★ 인과 코드 — 러너·규칙 J 가 문자열이 아니라 **코드**로 짝지을 수 있게 (조건 7).
        return (f'STEP3_REQUIRED_INCOMPLETE: required component 가 완료되지 않았다: '
                f'{sorted(set(_bad))} (required={_req}).  `--allow-partial-step3` 로만 연다')
    return None


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
    ap.add_argument('--step3-fibre-stamp', choices=('point', 'segment'), default='point',
                    help='★SR-01: STEP3 에서 섬유 첨가제를 굽는 방식.  point(기본) = 현행 1-복셀 점 '
                         '스탬프 — 실침대에서 섬유의 68.5-86.4%% 가 2.6-3.4 조각으로 **끊긴다** '
                         '(6-face 솔버에서 전기적으로 분리).  segment = 같은 fid 점열을 경로로 보고 '
                         '선분 순회 → 연결 구성상 보장 (--fibre npy 필요).  ⚠ 기본을 바꾸지 않은 것은 '
                         'Δσ_e 크기를 아직 안 쟀기 때문 (docs/data/sr01_realbed_ab.csv)')
    ap.add_argument('--fibre-dia', default='', help='per-point relative fibre diameter npy (mpm3d '
                    '--save-fibre-dia): attach per-fibre median Ø to additive_fibres so the viewer renders '
                    'thickness (PTFE draw d∝√(V/L) — thin-long vs thick-short).')
    ap.add_argument('--out', default='mpm_payload.json')
    # ★ STEP3 v1 — electronic voxel resistor network (σ_e_eff + per-AM current density).  RELATIVE
    # trust unit; σ table: AM = A1-locked (Trevisanello 10/5 mS/cm), carbon/SDCP = §F1 order-of-
    # magnitude hooks (record travels in metrics.step3.sigma_table so runs are comparable).
    ap.add_argument('--no-step3', action='store_true', help='skip the STEP3 σ_e network solve')
    ap.add_argument('--step3-bridge-um', type=float, default=0.0,
                    help='AM 접촉 브리지 반경을 **물리 단위**로 고정 (µm).  0 = 현행 1.2·vox (격자에 묶임). 격자 수렴 시험에서 탄소 효과와 브리지 효과를 분리하려면 고정할 것 (CL-21)')
    ap.add_argument('--step3-rasterize-only', default='', metavar='OUT_JSON',
                    help='래스터까지만 하고 **상별 셀 수 원장**을 JSON 으로 쓰고 종료한다 '
                         '(솔브 없음 = 순수 CPU 수 분).  구 스탬프와 함께 주면 점 스탬프 대비 '
                         '추가 셀의 **원래 상**까지 diff — CL-34 우선순위 결함 크기를 '
                         'GPU 대조 팔 없이 잰다 (심층 리뷰 ③ 제안)')
    ap.add_argument('--step3-sdcp-sphere-d', type=float, default=0.0, metavar='D_UM',
                    help='SDCP 를 **참 직경 D_UM 의 구**로 스탬프한다 (기본 0 = 현행 점 스탬프). '
                         '점 스탬프는 입자당 셀 하나라 부피가 격자에 19 배 흔들린다 '
                         '(0.24× @0.15 ~ 4.53× @0.4).  구 스탬프는 2.4 %% 안이다.  '
                         '⚠ d/vox ≥ 2 필요 — 그 아래는 fail-closed 로 거부한다.  '
                         'prereg v2 판정(h1) 의 대응, CL-33')
    ap.add_argument('--step3-sdcp-yield-to-vgcf', action='store_true',
                    help='★ **진단 전용** (CL-43, prereg v3 STEP 5) — SDCP 가 이미 VGCF 인 셀에는 '
                         '안 찍고 **양보**한다.  상별 원장이 SDCP 셀의 39.8 %% (vox 0.4) ~ 7.2 %% '
                         '(0.15) 가 원래 VGCF 셀임을 보였다: 그 셀은 도체 셀 수(dof)가 안 변하고 '
                         'σ 만 11.0 → 250 으로 올라간다 = **새 도체 부피가 아니라 기존 도체의 '
                         'σ 업그레이드**.  이 플래그로 그 채널만 끈다 (양보해도 그 셀은 VGCF 라 '
                         '여전히 도체 = 연결성은 안 끊긴다).  ⚠ 생산 규약은 바꾸지 않는다 — '
                         '기본값은 옛 거동과 셀 단위 동일 (selftest sdcp-yield-default)')
    ap.add_argument('--step3-origin-shift', type=float, nargs=3, default=None,
                    metavar=('SX', 'SY', 'SZ'),
                    help='STEP3 격자 origin 을 축마다 [0, vox) 만큼 민다 (µm).  격자 **위상**만 '
                         '바뀌고 침대는 안 잃는다.  origin 앙상블용 — 단일 origin σ 는 위상에 '
                         '2.4~5.8 %% 흔들린다 (CL-30).  prereg sdcp_gain_prereg_20260816 §4')
    ap.add_argument('--step3-vox', type=float, default=0.4,
                    help='STEP3 voxel size (µm).  0.4 default: AM-carbon bridges (band 0.15µm) land in '
                         'same/adjacent voxels; smaller = finer necks but ∝1/vox³ dof.')
    ap.add_argument('--cam', choices=('nmc811', 'nca'), default='nmc811',
                    help='★A8 CAM 재료 프리셋 — σ_e(AM) 기본값 결정 (docs/nca_material_preset.md 검증표). '
                         'nmc811: S/P = 10/5 mS/cm (A1 corpus-fit).  nca: S=P = 10 mS/cm 단일값 — '
                         'Amin/Chiang JES 2015 소결펠릿 "충전-상태 상단"(리튬화는 1e-4 S/cm, SOC 2자리 스윙; '
                         'NCA 단결정/다결정 분리 데이터 부재라 S=P).  ⚠ E_AM은 프리셋이 안 바꿈 — '
                         'Kang의 175 GPa는 assumed(Koerver umbrella 인용)라 140 유지(가짜 25%% 대비 차단).')
    ap.add_argument('--sigma-am-s', type=float, default=None,
                    help='σ_e AM_S (S/cm) — 미지정 시 --cam 프리셋 (nmc811: 0.010 / nca: 0.010)')
    ap.add_argument('--sigma-am-p', type=float, default=None,
                    help='σ_e AM_P (S/cm) — 미지정 시 --cam 프리셋 (nmc811: 0.005 / nca: 0.010)')
    ap.add_argument('--sigma-vgcf', type=float, default=100.0,
                    help='σ_e VGCF (S/cm).  ⚠ NOT a material property — this is an EFFECTIVE '
                         'NETWORK constant (CL-47): voxel fusion deletes fibre-fibre contact '
                         'resistance, so 100 lumps that missing loss (powder 83, single fibre '
                         '1e4 S/cm).  Same epistemology as the DEM E_eff 18x softening.')
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
    #  ★★ 2026-08-24 (CDXR2-2/CDXR2-6) — **스탬프 여부와 전도도를 분리한다.**
    #    옛 게이트 `_cond_ph = (...) if a.sigma_ptfe > 0 else (...)` 는 둘을 묶어 놓아
    #    "PTFE 를 격자에 그리되 절연으로" 를 표현할 방법이 **없었다**.  그래서 CL-49 는
    #    `--sigma-ptfe 1e-16` 이라는 우회로를 썼고, 그것은 σ 대비 1e18 로 조건수를 무너뜨린다
    #    (prereg v3 STEP 3 이 대비 25,000 배에서 이미 CG 미수렴 HOLD).
    #    ★ 솔버는 이미 `cond = sig > 0` (step3_sigma.py:447) 이라 **σ=0 셀은 dof 에서 빠진다**.
    #      ⇒ 게이트만 분리하면 `--ptfe-stamp centerline --sigma-ptfe 0` = **exact-zero DOF** 다.
    #  ★★ 2026-08-25 (CDXR3-2) — **required component 실패는 nonzero 로 끝난다.**
    #    옛 판은 STEP3 예외를 `status: failed` 로 적고 payload 를 쓴 뒤 **exit 0** 이었다.
    #    러너의 `check_arm` 이 2차 방어를 하지만 그것으로 **대체할 수 없다** — Codex 가
    #    partial/missing·backend 위장 mutant 로 8팔 최종 봉인까지 통과시켰다.
    #    ⇒ 기본 fail-closed.  부분 payload 가 필요한 소비자(웹앱 미리보기 등)는 명시로 연다.
    ap.add_argument('--allow-partial-step3', action='store_true',
                    help='STEP3 가 실패/부분이어도 exit 0 으로 끝낸다 (기본은 nonzero).  '
                         '⚠ 과학 산출물에는 쓰지 말 것 — 부분 결과가 성공으로 캐시된다')
    #  ★★ 2026-08-25 (CDXR3-3) — 러너가 **기대하는 규약 id** 를 넘긴다.  payload 가
    #    적용한 것과 다르면 nonzero 로 죽는다 (요청↔적용 end-to-end 봉인).
    ap.add_argument('--expect-protocol', default='',
                    help='기대하는 physics_protocol_id.  적용된 것과 다르면 **중단**한다. '
                         '러너가 넘긴다 — 규약이 조용히 바뀌는 것을 막는 유일한 자리다')
    #  ★★★ 2026-08-25 (Codex 재리뷰 조건 4) — **기대값을 첫 팔에서 읽지 않는다.**
    #    `--expect-protocol` 의 표준 용법은 "첫 팔이 찍은 id 를 나머지 팔에 넘기기" 였는데,
    #    그러면 **첫 팔이 진리를 정의한다** — 첫 팔이 조용히 잘못된 규약으로 돌면 나머지
    #    일곱이 그것에 일치해 전부 통과한다 (팔간 일치는 옳음이 아니다).
    #    ⇒ 러너가 **자기가 설정한 값**을 그대로 선언하고, payload 가 **적용값**과 필드별로
    #      대조한다.  해시가 아니라 필드라서 어느 축이 갈렸는지도 말해 준다.
    ap.add_argument('--expect-physics', default='',
                    help='러너가 설정한 물리 인자 선언 `KEY=VAL,KEY=VAL…` (KEY 는 '
                         'PROTOCOL_FIELDS).  적용값과 다르면 **중단**한다 (exit 4).  '
                         '⚠ 첫 팔의 id 를 베끼는 것과 다르다 — 그것은 첫 팔을 진리로 삼는다')
    ap.add_argument('--ptfe-stamp', default='', choices=('', 'off', 'centerline', 'capsule'),
                    help="PTFE 를 전도 격자에 어떻게 그릴지.  off = 안 그린다 · centerline = "
                         "1-셀 선분(현행) · capsule = 직경 인식(**예약값, 미구현 — 고르면 중단**).  "
                         "빈 값 = 옛 규약 유도(sigma_ptfe > 0 이면 centerline, 아니면 off) 이고 "
                         "매니페스트에 legacy-unversioned 로 적힌다.  ⚠ σ 와 무관하다 — "
                         "`--ptfe-stamp centerline --sigma-ptfe 0` 이 exact-zero DOF 다")
    ap.add_argument('--sigma-swcnt', type=float, default=100.0,
                    help='σ_e SWCNT sheath (S/cm) — A14.  VGCF급 lit order ⚠hook: 개별 SWCNT 축방향은 '
                         '1e4-1e5 S/cm급이나 vein-번들 film 유효값은 미앵커.  ⚠ koo2026의 0.20 S/cm은 '
                         '분말-복합체(powder-composite) 측정값이지 상(phase) σ가 아님 — 이식 금지.')
    ap.add_argument('--swcnt-ion-block', action='store_true',
                    help='A14 상한 시나리오 opt-in: sheath 복셀 σ_i=0 (이온 dof·BV면 소멸) = ion-blocking '
                         'skin 가정의 기하 상한을 수송모델로 구현.  기본 OFF = SE-투명(σ_i=σ_ion_se): '
                         '실제 skin 2-10nm sub-voxel이라 1-voxel 차단은 40-200× 과대표현(이중계상).')
    ap.add_argument('--sigma-ion-se', type=float, default=se_material.SIGMA_GRAIN_S_CM_25C,
                    help='σ_ion SE (S/cm) = 3.0 mS/cm LPSCl grain (Cronau — production σ_grain anchor). '
                         f'★ declared AT T_ref = {se_material.T_REF_C:.0f} °C (se_material convention); '
                         '--temp-c multiplies THIS value by the Arrhenius factor.')
    ap.add_argument('--collector-rint', type=float, default=-1.0,
                    help='SELECTED collector R_int (Ω·cm², manuscript Fig6e cycled anchors: bare-Al SBE '
                         '110 / DBE 46 / C-SUS primer 30; 0 = ideal).  <0 = no selection (presets still '
                         'reported).  Applied as a uniform areal series term (post-processing).')
    ap.add_argument('--collector-name', default='', help='label for the selected collector preset')
    ap.add_argument('--collector-scenario', default='', choices=('', 'sbe', 'dbe', 'csus', 'sus'),
                    help='anchors-CSV scenario key of the selected collector (webapp이 전달) — selected '
                         '항목에 pristine 짝값(시간-일관 BOL)을 병기하기 위한 단일-출처 키')
    ap.add_argument('--sigma-ion-sdcp', type=float, default=0.001,
                    help='σ_ion SDCP (S/cm) — NOT an ion-insulator (user principle: Li-hopping keeps it '
                         'conducting; pellet ×0.80 vs PTFE ×0.27).  1 mS/cm ⚠F1 hook; Li⁺ DFT 패키지가 앵커 예정.')
    ap.add_argument('--field-max-points', type=int, default=90000,
                    help='max points per current-density FIELD cloud (electronic=AM+carbon, ionic=SE+SDCP). '
                         'High for paper figures; ~90k/field ≈ a few MB JSON.  Hottest 35%% always kept.')
    ap.add_argument('--no-field', action='store_true',
                    help='skip the STEP3 current-density FIELD export (electronic_field / ionic_field)')
    ap.add_argument('--no-thermal', action='store_true',
                    help='skip STEP3 열전도 (σ_thermal 多상 k_eff) 솔브')
    ap.add_argument('--no-trackb', action='store_true',
                    help='Track-B(COMSOL 하이브리드) 파라미터 계산 생략 — τ_geo 추가 솔브 1회 + '
                         'AM face walk 를 끈다')
    ap.add_argument('--periodic', action='store_true',
                    help='STEP3 σ-solve(전자/이온/열/pore-τ/반응)에 x,y 주기 BC 적용 (MPM RVE '
                         "'boundary p p f' 정합 — 측면 wrap, z=plate 유지).  기본 OFF = 절연 측벽(기존).")
    ap.add_argument('--joule-heat', action='store_true',
                    help='#29 — 전자망 Joule 발열밀도 q∝|J|²/σ hot-spot 맵 산출 (어디서 발열 몰리는지; '
                         'step3.joule + joule_field).  기본 OFF.  ★절대 ΔT(K)·STEP5 R(N) Arrhenius 연동은 '
                         'LPSCl 분해 Eₐ 앵커 미보유 → v2(이 플래그는 발열 생성분포까지만).')
    ap.add_argument('--k-carbon', type=float, default=None,
                    help='열전도 carbon(VGCF/SuperP/SWCNT) k [W/cm·K] override (기본 =k_AM 보수적 ASSUMED; 스윕용)')
    ap.add_argument('--step3-gpu', action='store_true',
                    help='run the STEP3 Kirchhoff CG on GPU (CuPy cuSPARSE) — ~10-50× faster, esp. fine '
                         'vox; auto-falls back to scipy CPU if CuPy/CUDA missing (same σ either way).')
    ap.add_argument('--step3-maxiter', type=int, default=0,
                    help='STEP3 CG 최대 반복 (기본 0 = 코드 기본 30000 유지).  조건수가 나쁜 '
                         '진단 팔(예: --sigma-vgcf 7854 → σ 대비 785,400x)이 rtol 1e-8 에 '
                         '못 닿아 info=30000 으로 끝날 때 올린다.  ⚠ 규약을 바꾸는 것이 아니라 '
                         '수렴에 도달시키는 것이다 — 수렴한 값끼리만 비교할 수 있다.')
    ap.add_argument('--step3-amg', action='store_true',
                    help='STEP3 CPU CG 전처리를 Jacobi → AMG (pyamg smoothed-aggregation).  '
                         '값은 반복수 절벽 회피: 합성 침대 실측(61.6k→487k dof)에서 Jacobi 는 '
                         '3,374→7,088 it 로 자라고 AMG 는 218→261 로 평평하다 — 2.7M dof 어림 '
                         'Jacobi ≈1.3만 it = maxiter 30,000 의 절반.  속도 이득은 작다(1.4–1.5×, '
                         '2.7M 외삽 ≈2.4×) — 벽시계의 진짜 치료는 --step3-gpu 다.  σ_eff 는 '
                         '전처리에 불변(rtol 1e-8 서 ≤0.014 %%).  ⚠ A/B 두 팔은 **같은 전처리**여야 '
                         '한다 — manifest backend.precond 에 남고 비교기가 검사한다.  '
                         'pyamg 부재 시 Jacobi 폴백.')
    ap.add_argument('--i0-a-m2', type=float, default=2.0,
                    help='STEP4 exchange current density i0 (A/m², NCM|LPSCl 계면) — ⚠F1 literature hook '
                         '(Newman-typical 1-5 A/m²).  Sets the linearised BV conductance g=i0·F/RT.')
    ap.add_argument('--no-ion', action='store_true',
                    help='STEP3 **이온 솔브를 건너뛴다** (σ_e 전용 스윕용).  2026-08-18 신설 — '
                         'vox 0.125 격자 스윕이 여기서 OOM 으로 죽었고(36.7 M dof 이온계가 45.1 M '
                         'dof 전자계 위에 얹힌다), DR3-07 로 vox ≤ 0.125 의 σ_ion 은 **어차피 인용 '
                         '금지**다 (SE 점 스탬프 미충전).  Track-B 도 같이 없어진다.  '
                         '⚠ 상태는 `disabled` 로 남는다 — `not_solvable`(SE 미퍼콜)과 구분된다')
    ap.add_argument('--no-collector', action='store_true',
                    help='STEP3 **집전체 기하 솔브(wetted/bare) 2회를 건너뛴다** (σ_e 전용 스윕용). '
                         '2026-08-18 신설 — vox 0.125 스윕이 `--no-ion --no-pore` 로도 **여기서** '
                         'OOM 으로 죽었다 (전자 솔브는 수렴 완료 후 사망).  ⚠ shift 팔에서는 '
                         '`_bot_mask` 가 origin 이동을 안 더해 이 값이 **어차피 무효**다 → 스윕에서 '
                         '끄면 손실 0, 시간 ~3배 절약.  ⚠ 상태는 `disabled` 로 남는다')
    ap.add_argument('--no-pore', action='store_true',
                    help='STEP3 **pore-τ·PNM 을 건너뛴다** (σ_e 전용 스윕용).  vox 0.125 에서 '
                         'τ 가 1,415 → 4.97e9 로 터졌고(closed-from-top 28.5 → 99.2 %%) DR3-07 이 '
                         '예언한 그대로다 — 인용 금지 값에 300 s·10 GB 를 쓰지 않는다')
    ap.add_argument('--no-step4', action='store_true',
                    help='skip the STEP4 reaction-current solve (저율 충전 반응전류 분포, slide-20 물리)')
    ap.add_argument('--save-step4-grid', default='',
                    help='STEP4-v2(시간전개) 입력 격자 npz 저장: sid/pid/σ_e·σ_i테이블/vox/z_top/AM반경 '
                         '— scripts/step4_dyn.py --grid 로 로드 (payload 재실행 없이 rate 스윕)')
    se_material.temperature_argparse(ap)   # --temp-c / --ea-ion-ev (both default None)
    ap.add_argument('--allow-mixed-t-ionic', action='store_true',
                    help='T1-e 해제: --temp-c 가 SE 이온 σ만 올리고 SDCP σ_ion 은 T_ref 에 남는 '
                         '**혼합-온도 이온상**을 명시 허용한다.  기본은 차단 — SDCP 는 Li-hopping '
                         '폴리머라 LPSCl Eₐ 를 이식할 앵커가 없고(§F1) 그대로 두면 σ_SDCP/σ_SE 비율이 '
                         'T-인자만큼 왜곡된다.  허용 시 provenance 에 mixed_ionic_temperature='
                         'DISTORTED 가 기록된다.')
    ap.add_argument('--selftest-temperature', action='store_true',
                    help='T1-e/T1-a 온도 계약 회귀 테스트만 실행하고 종료 (입력 파일 불필요)')
    a = ap.parse_args()
    #  ★★ PTFE 스탬프 규약 해석 (CDXR2-6).  **어떤 작업보다 먼저** — 예약값을 고르면
    #    GPU 를 잡기 전에 죽어야 한다.
    a._ptfe_stamp, a._ptfe_stamp_legacy = resolve_ptfe_stamp(a.ptfe_stamp, a.sigma_ptfe)
    a._protocol_expect = (a.expect_protocol or '').strip()
    a._physics_expect = {}
    for _kv in (a.expect_physics or '').split(','):
        _kv = _kv.strip()
        if not _kv:
            continue
        if '=' not in _kv:
            raise SystemExit(f'--expect-physics 항목이 `KEY=VAL` 이 아니다: {_kv!r}')
        _k, _v = _kv.split('=', 1)
        _k = _k.strip()
        if _k not in PROTOCOL_FIELDS:
            raise SystemExit(f'--expect-physics 의 `{_k}` 는 PROTOCOL_FIELDS 가 아니다 '
                             f'(가능: {", ".join(PROTOCOL_FIELDS)})')
        a._physics_expect[_k] = _v.strip()
    if a._ptfe_stamp in PTFE_STAMPS_RESERVED:
        #  ⚠ 예약값이다 — centerline 으로 별칭하거나 매니페스트에 'capsule applied' 라고
        #    적으면 **안 된다** (Codex Q3).  구현될 때까지 명시적으로 죽는다.
        raise SystemExit(
            'unsupported_protocol: --ptfe-stamp capsule 은 **예약값이고 미구현**이다.\n'
            '  PTFE 는 정부피 인발로 시딩돼 직경이 **분포**다 (additives.seed_fibres '
            'vol_conserve, d_i ∝ √(V_i/L_i)) — 단일 Ø0.25 캡슐로는 표현되지 않는다.\n'
            '  게다가 per-fibril 직경이 아직 raster 에 배선돼 있지 않다 (CDXR2-2: '
            '--fibre-dia 는 뷰어 전용이고 로드가 solve 뒤다).\n'
            '  ⇒ D-1 source census 를 먼저 돌려 표현법을 정한 뒤 구현한다.  '
            '지금은 `--ptfe-stamp {off,centerline}` 만 쓸 것.')
    if a.selftest_temperature:
        _sys.exit(_selftest_temperature())
    # ── σ_ion(T) ────────────────────────────────────────────────────────────────
    # --temp-c unset (default) → scale_sigma_ion is the identity, so --sigma-ion-se keeps its
    # bare 0.003 value and EVERY legacy run is bitwise unchanged.  When set, the Kraft-2017
    # σ·T Arrhenius factor multiplies the (T_ref = 25 °C) SE ionic σ — including a user-supplied
    # --sigma-ion-se override, which is likewise declared at T_ref.  σ_e / κ / i0 stay
    # T-independent: for σ_e that is the literature-consistent choice (Reisacher — ohmic regime
    # is T-independent) AND matches the DEM solver; for κ / i0 / D_s there is no anchor (§F1).
    # ⚠ SDCP (σ_ion_sdcp) is deliberately NOT scaled: it is a Li-hopping POLYMER, its Eₐ is not
    # LPSCl's 0.41 eV and no SDCP Eₐ anchor exists (§F1).  Applying the SE band to it would be
    # fabrication, so it stays at its T_ref value and the provenance says so.
    a._sigma_ion_se_ref = a.sigma_ion_se
    a.sigma_ion_se = se_material.scale_sigma_ion(a.sigma_ion_se, a.temp_c, a.ea_ion_ev)
    _temp_prov = se_material.provenance(a.temp_c, a.ea_ion_ev)
    _temp_prov['scaled_phases'] = ['SE']
    _temp_prov['unscaled_phases'] = {
        'SDCP': 'no Ea anchor for the Li-hopping polymer (§F1) — held at T_ref',
        'AM/carbon (sigma_e)': 'ohmic regime is T-independent (Reisacher, qualitative)',
        'thermal k': 'no anchor (§F1)',
        'i0 / D_s / OCP dU/dT': 'no anchor (§F1) — STEP4 kinetics are NOT temperature-scaled',
    }
    se_material.warn_band(a.temp_c, a.ea_ion_ev)
    # ★A8 CAM 프리셋 → σ_e(AM) 기본값 해석 (명시 --sigma-am-s/-p가 항상 우선; nmc811 기본은
    #   기존 10/5와 byte-동일 = 하위호환).  근거·캐비엇: docs/nca_material_preset.md
    if a.sigma_am_s is None:
        a.sigma_am_s = 0.010
    if a.sigma_am_p is None:
        a.sigma_am_p = 0.010 if a.cam == 'nca' else 0.005
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

    # ── T1-e 혼합-온도 이온상 차단 (SDCP 가 실제로 베드에 있을 때만 발화) ─────────────
    #    여기가 SDCP(phase 5) 존재를 아는 가장 이른 지점 = STEP3 수 분 태우기 전에 fail-fast.
    _sdcp_here = bool(phase is not None and (phase == 5).any())
    _t1e_blocked, _t1e_note = mixed_ionic_verdict(
        a.temp_c, _sdcp_here and not a.no_step3, a.sigma_ion_sdcp, a.allow_mixed_t_ionic, a.ea_ion_ev)
    if _t1e_note is not None:                       # --temp-c 미지정이면 None → JSON 바이트 불변
        _temp_prov['mixed_ionic_temperature'] = _t1e_note
        if _t1e_note['status'] == 'DISTORTED':
            _temp_prov['unscaled_phases']['SDCP'] += (
                '  ⚠ 이 런은 SDCP 가 실제로 스탬프돼 있어 σ_SDCP/σ_SE 비율이 '
                f"÷{_t1e_note['sigma_ion_T_factor']:.3f} 왜곡됨 (--allow-mixed-t-ionic)")
    if _t1e_blocked:
        _f = _t1e_note['sigma_ion_T_factor']
        print(f'\n⛔ T1-e 차단: --temp-c {a.temp_c:g} °C 는 σ_ion(SE) 만 ×{_f:.3f} 올리는데, 이 베드에는\n'
              f'   SDCP 이온상(phase 5, {int((phase == 5).sum()):,} pts, --sigma-ion-sdcp '
              f'{a.sigma_ion_sdcp:g} S/cm)이 스탬프돼 있고 그 σ_ion 은 T_ref '
              f'{se_material.T_REF_C:.0f} °C 에 그대로 남습니다.\n'
              f'   → σ_SDCP/σ_SE 비율이 ÷{_f:.3f} 왜곡된 채 STEP3 이온 솔브·STEP4 격자가 만들어집니다.\n'
              '   SDCP 는 Li-hopping 폴리머라 LPSCl 의 Eₐ 를 이식할 앵커가 없습니다 (§F1):\n'
              '   같이 올리면 날조, 안 올리면 왜곡 → 조용히 통과시키지 않고 **차단**합니다.\n'
              '   ▶ SDCP 레시피의 정본 경로: --temp-c 를 빼고 25 °C 로 돌린다\n'
              '   ▶ 온도축만 보고 싶다면: --sigma-ion-sdcp 0 (SDCP 를 이온 절연으로 명시)\n'
              '   ▶ 왜곡을 알고 감수: --allow-mixed-t-ionic (provenance 에 DISTORTED 기록)\n'
              '   ▶ 상세: docs/temp_pressure_capability.md §3 / se_material.py 헤더\n', flush=True)
        _sys.exit(2)

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

    # ── #4b: SE morphology 점군 (뷰어 "2D 단면 morphology" 모드용) — 다운샘플 SE 물질점 (µm) ──
    #   [x,y,z] µm (AM 구·SE 메쉬와 동일 (pt−off)·UM 규약).  뷰어가 클릭 평면서 슬라이스 → 그레인색
    #   (위치-해시 golden-ratio hue) + AM + void 로 canvas 렌더 → SE void-filling 실시간 확인.
    se_morph_points = []
    if len(se_se):
        _Nm = min(a.strain_pts, len(se_se))
        _idxm = (np.random.default_rng(2).choice(len(se_se), _Nm, replace=False)
                 if len(se_se) > _Nm else np.arange(len(se_se)))
        _Pm = se_se[_idxm]
        se_morph_points = np.column_stack([((_Pm[:, 0] - SW[0]) * UM).round(2),
                                           ((_Pm[:, 1] - SW[0]) * UM).round(2),
                                           ((_Pm[:, 2] - FLOOR) * UM).round(2)]).tolist()
        print(f'  SE morphology points: {len(se_morph_points):,} (#4b 2D 단면 morphology)')

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
                                                   else 'AM + VGCF/SuperP/SDCP/SWCNT-sheath (SE·PTFE excluded = e-insulators)')}
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
    # ★★ RC6-06 (Codex 6회차) — STEP3 **component manifest** ★★
    #   지금까지 thermal 만 상태를 남겼고 electronic/ionic/pore/pnm/reaction 은 무상태였다.
    #   그래서 키 부재가 disabled / not_applicable / not_solvable / failed 중 무엇인지
    #   downstream 이 알 수 없었다 — DEM 접촉망 솔버에서 고친 것과 **같은 결함**이다.
    #   (그 결함이 양쪽 파이프라인에 따로 있었던 것이 CLAUDE.md frame[5] 경고의 실례다.)
    _s3st = {}                       # component → {'status': …, 'reason': …}
    #: ★ RC7-01 (Codex 7회차): manifest 가 **표시된 component 들만** 보고 상태를 정했다.
    #:   그래서 어떤 component 가 아예 실행되지 않아 `_s3st` 에 **없으면**, 남은 것들이
    #:   전부 complete 인 한 top='complete' 가 나왔다 — "안 돈 것" 이 "다 됐다" 로 보였다.
    #:   결손을 조용히 두지 않겠다는 manifest 자신의 목적과 정반대다.
    #:   ⇒ **기대 집합을 선언**하고, 표시되지 않은 것은 `missing` 으로 채운다.
    STEP3_EXPECTED = ('electronic', 'ionic', 'thermal', 'pore', 'pnm')

    def _s3mark(comp, status, reason=''):
        """STEP3 component 의 상태를 남긴다.  **결손을 조용히 두지 않는다.**

        status ∈ complete | unconverged(솔브는 돌았으나 CG 가 수렴 안 함 — 값을 쓰면 안 된다)
                 | not_solvable(물리적으로 정의 안 됨=정상) | failed(예외)
                 | disabled(사용자가 끔) | skipped(선행 부재) | missing(표시 자체가 없음)

        ★ RC7-05 (Codex 7회차): backend 는 모듈 전역 `LAST_BACKEND` 하나뿐이라 manifest 가
          **마지막 solve 의 backend** 만 담았다 (electronic 은 GPU, ionic 은 CPU 로 떨어져도
          하나만 보임).  → 표시 시점에 **component 별로 스냅샷**한다.
        """
        rec = {'status': status, **({'reason': reason} if reason else {})}
        _mod = _sys.modules.get('step3_sigma')
        _bk = getattr(_mod, 'LAST_BACKEND', None) if _mod is not None else None
        if status == 'complete' and isinstance(_bk, dict) and _bk.get('used'):
            rec['backend'] = dict(_bk)
        _s3st[comp] = rec
        return rec

    # ★ SR-01: 섬유 id 를 STEP3 **전에** 읽는다 (뷰어용 로드는 훨씬 뒤라 그때는 늦다).
    #   킷 run_mpm.sh 가 이미 --save-fibre 로 저장하므로 배선만 하면 된다.
    #  ★ CDXIJ-10 ③ — 입력 digest 는 **읽기 직후** 계산한다 (솔브 실패해도 남게).
    _in_files = {}
    for _k, _v in (('scaffold', a.scaffold), ('se', a.se), ('phase', a.phase),
                   ('fibre', getattr(a, 'fibre', '')), ('metrics_json', a.metrics_json),
                   ('fibre_dia', getattr(a, 'fibre_dia', ''))):
        _h = _sha256_file(_v) if _v else None
        if _h:
            _in_files[_k] = _h
    _in_dig = None
    if _in_files:
        import hashlib as _hl2
        _in_dig = _hl2.sha256(
            '|'.join(f'{k}={_in_files[k]}' for k in sorted(_in_files)).encode()
        ).hexdigest()[:16]
        print(f'  입력 digest {_in_dig} ({len(_in_files)} 파일) — CDXIJ-10 ③', flush=True)

    _fid_all = None
    _afid = None          # STEP3 가 안 돌아도 manifest 가 참조하므로 바깥에서 초기화
    # ⚠⚠ `_kind_all` 도 **반드시 여기서** 초기화한다 (2026-08-20 실사고, 규칙 J).
    #   옛 코드는 아래 `if getattr(a,'fibre',…)` **안에서만** 대입해 놓고 rasterize 호출
    #   (`add_kind=(_kind_all …)`)에서는 무조건 읽었다.  `--fibre` 없는 런 —
    #   즉 `mpm_input_from_case.py` 가 `--add-recipe` 없는 킷에 만드는 **모든 plain 침대** —
    #   에서 UnboundLocalError 가 나고, STEP3 를 감싼 blanket except 가 그것을 삼켜
    #   `⚠ STEP3 skipped` 한 줄만 남긴 채 **payload 가 exit 0 으로 완주**했다.
    #   ⇒ σ_e·σ_ion·k·pore-τ·collector·step4_grid 가 통째로 **소실**되는데 런은 성공으로 보인다.
    #   (2026-08-12 `60bd849e` 이후 활성.  pyflakes(check_undefined_names)는 조건부 바인딩을
    #    원리적으로 못 본다 — 그래서 규칙 J 스모크가 필요하다.)
    #  ★★ 2026-08-24 (CDXR2-2) — `_dia_all` 도 **같은 부류**다.  per-fibril 직경을
    #    solve 전에 읽는데(옛 판은 뷰어 블록에서만, 솔브 **뒤**), 그것을 읽는 게이트
    #    (`PTFE_STAMP_NEEDS_DIA`)가 아래 `if a.fibre` 블록 **밖**에 있다 — 즉 hoist 가
    #    없으면 `--fibre` 없는 plain 침대에서 정확히 위와 같은 UnboundLocalError 다.
    #    ⇒ 두 hoist 를 **붙여 둔다**.  규칙 J 의 음성 대조(`_J_NEEDLE`)가 이 두 줄을
    #      한 덩어리로 지키므로, 어느 쪽을 지워도 스모크가 잡는다.
    _dia_all = None
    _kind_all = None
    if getattr(a, 'fibre', '') and phase is not None:
        try:
            _fid_all = np.load(a.fibre)
            # ★ fid 의미(경로/그룹) 동반 파일 — 있으면 그것이 이긴다 (SR-01 후속).
            #   없으면 STEP3 가 phase 화이트리스트로 폴백한다 (옛 산출물 호환).
            _kp = (a.fibre[:-4] if a.fibre.endswith('.npy') else a.fibre) + '_kind.npy'
            # ⚠ 반드시 `_os` — 이 함수 안에 `import os` 가 있어 `os` 는 **지역명**이고,
            #   그 대입은 여기보다 뒤라 `os.path` 는 UnboundLocalError 다.  2026-08-12 실사고:
            #   그 예외를 아래 `except Exception` 이 삼켜 **선분 스탬프가 조용히 꺼졌다**.
            if _os.path.exists(_kp):
                try:
                    _kind_all = np.load(_kp)
                    print(f'  STEP3: fid 의미 파일 로드 ({_kp}) — 경로 '
                          f'{int((_kind_all == 1).sum()):,} / 그룹 {int((_kind_all == 0).sum()):,} 점', flush=True)
                except Exception as _e:
                    print(f'  ⚠ fid 의미 파일 읽기 실패 ({_e}) → phase 폴백', flush=True)
            if len(_fid_all) != len(se):
                print(f'  ⚠ --fibre 길이 {len(_fid_all):,} ≠ SE 점 {len(se):,} → 선분 스탬프 비활성',
                      flush=True)
                _fid_all = None
            #  ★ per-fibril 상대 직경 (PTFE 정부피 인발: d ∝ √(V/L) 이라 **분포**다).
            #    길이가 안 맞으면 **여기서** 버린다 — 뷰어 뒤가 아니라.
            if getattr(a, 'fibre_dia', ''):
                try:
                    _dia_all = np.load(a.fibre_dia)
                    if len(_dia_all) != len(se):
                        print(f'  ⚠ --fibre-dia 길이 {len(_dia_all):,} ≠ SE 점 {len(se):,} '
                              f'→ 직경 비활성', flush=True)
                        _dia_all = None
                    else:
                        print(f'  STEP3: per-fibril 직경 로드 ({a.fibre_dia}) — '
                              f'{len(_dia_all):,} 점', flush=True)
                except Exception as _e2:                       # noqa: BLE001
                    print(f'  ⚠ --fibre-dia 로드 실패 ({type(_e2).__name__}: {_e2})', flush=True)
                    _dia_all = None
        except SystemExit:
            raise
        except Exception as _e:                                # noqa: BLE001
            # ★ 2026-08-12 fail-closed: `--step3-fibre-stamp segment` 를 **명시적으로** 요청했으면
            #   조용히 점으로 내려앉으면 안 된다.  런은 성공한 것처럼 끝나고 **다른 규약을 잰다**
            #   (실사고: UnboundLocalError 를 여기서 삼켜 선분 팔이 점 팔이 됐다).
            print(f'  ⚠ --fibre 로드 실패 ({type(_e).__name__}: {_e}) → 선분 스탬프 비활성', flush=True)
            _fid_all = None
            if getattr(a, 'step3_fibre_stamp', 'point') == 'segment':
                raise SystemExit(
                    f'ABORT — --step3-fibre-stamp segment 인데 --fibre 로드가 실패했다 '
                    f'({type(_e).__name__}: {_e}).  점-스탬프로 진행하면 요청과 **다른 규약**을 '
                    f'재게 된다.  --fibre 를 고치거나 --step3-fibre-stamp point 를 명시할 것.')

    #  ★ 방어 기본값 — 아래 try 가 이들을 대입하기 **전에** 죽으면 매니페스트 조립(:1690~)이
    #    NameError 를 낸다 (2026-08-16 에 `_zt3` 로 실제로 겪었다).  매니페스트가 읽는 이름은
    #    전부 여기서 먼저 정의한다.
    #  ★★ 2026-08-24 (CDXR2-2) — **직경 인식 스탬프는 직경 없이 돌면 안 된다.**
    #    지금은 `capsule` 하나뿐이고 그것은 parse 직후 예약값으로 중단되므로 이 게이트는
    #    아직 발화하지 않는다.  그래도 **여기 있어야** 한다 — 구현이 들어오는 순간
    #    fail-open 이 되는 것을 막는 자리이고, 규약 목록에 이름을 올려 두면 다음 사람이
    #    직경 배선을 잊지 않는다.  (`_selftest` 의 `ptfe-dia-gate` 가 이 목록을 지킨다.)
    if a._ptfe_stamp in PTFE_STAMP_NEEDS_DIA and _dia_all is None:
        raise SystemExit(
            f'ABORT — --ptfe-stamp {a._ptfe_stamp} 는 per-fibril 직경이 필요한데 '
            f'--fibre-dia 가 없거나 길이가 SE 점과 다르다.  직경 없이 돌면 요청과 '
            f'**다른 규약**(1-셀 선분)을 재게 된다.')
    _bru = None; _osh = np.zeros(3); _zt3 = _zb3 = None; _afid = None
    step3 = None; je_am = None; jb_am = None; elec_field = None; ion_field = None; jrxn_am = None
    thermal_field = None                                     # STEP3 열류 |k∇T| 점군 (전자/이온 필드처럼)
    joule_field = None                                       # #29 STEP3 Joule 발열밀도 q∝|J|²/σ hot-spot 점군
    if len(r) and not a.no_step3:                       # phase=None → AM-skeleton-only σ (SBE baseline)
        try:
            import time as _time
            import step3_sigma as _s3
            _s3.GPU_SOLVE = a.step3_gpu                     # CuPy CG backend (auto CPU fallback)
            _s3.AMG_SOLVE = a.step3_amg                     # SR-03: CPU 전처리 (기본 OFF=Jacobi)
            _t0 = _time.time()
            _off = np.array([SW[0], SW[0], FLOOR])
            _am_c = (c - _off) * UM
            _am_r = r * UM
            #  ★★ 2026-08-24 (CDXR2-6) — 스탬프 여부는 **규약**이 정한다 (σ 가 아니라).
            #    `--ptfe-stamp centerline --sigma-ptfe 0` 이면 sid 7 이 찍히되 σ=0 이라
            #    솔버의 `cond = sig > 0` 이 그 셀을 **dof 에서 제외**한다 = exact-zero DOF.
            #    1e-16 우회로(σ 대비 1e18)와 달리 조건수를 건드리지 않는다.
            _cond_ph = ((2, 3, 5, 6, 4) if a._ptfe_stamp != 'off'
                        else (2, 3, 5, 6))   # 6=SWCNT sheath(A14, 도체)
            _m = (np.isin(phase, _cond_ph) if phase is not None
                  else np.zeros(len(se), bool))            # conductive additives (PTFE 4 = insulator, default)
            _apts = (se[_m] - _off) * UM if _m.any() else None
            _aph = phase[_m] if _m.any() else None
            # ── ★ SR-01: 섬유 첨가제를 **선분**으로 굽는 opt-in (기본 = 현행 점 스탬프) ──────
            #   점-스탬프는 6-face 연결을 깬다 (실침대 실측: 섬유의 68.5–86.4 % 가 2.6–3.4 조각).
            #   `--fibre` npy(킷이 --save-fibre 로 이미 저장) 를 주고 `--step3-fibre-stamp segment`
            #   이면 같은 fid 의 점열을 경로로 보고 선분 순회로 굽는다 → 연결이 구성상 보장.
            #   ⚠ **기본은 point** — Δσ_e 크기를 실측하기 전에 default 를 바꾸지 않는다.
            _afid = None
            if a.step3_fibre_stamp == 'segment':
                if _fid_all is None:
                    raise SystemExit(
                        'ABORT — --step3-fibre-stamp segment 인데 --fibre npy 가 없다.  '
                        '점-스탬프로 진행하면 요청과 **다른 규약**을 재게 되고, 그 런은 성공한 '
                        '것처럼 끝난다 (2026-08-12 실사고).  킷의 --save-fibre 산출물을 --fibre 로 '
                        '주거나, 점 규약을 원하면 --step3-fibre-stamp point 를 명시할 것.')
                elif _m.any():
                    _afid = _fid_all[_m]
                    print(f'  STEP3: 섬유 **선분 스탬프** ON — 도체점 {int(_m.sum()):,} · '
                          f'섬유 {int(np.unique(_afid[_afid >= 0]).size):,}개', flush=True)
            _hi = ((SW[1] - SW[0]) * UM, (SW[1] - SW[0]) * UM, max((top - FLOOR) * UM, a.step3_vox))
            print('  STEP3: voxelizing conductive+SE grid (풀해상도 — 이후 전자/이온 CG 솔브, 침묵 수 분 정상)…', flush=True)
            _septs = (se[phase == 1] - _off) * UM if phase is not None else (se - _off) * UM
            _bru = (float(a.step3_bridge_um) if getattr(a, 'step3_bridge_um', 0) > 0 else None)
            if _bru is not None:
                print(f'  STEP3: AM 접촉 브리지 반경 **고정** {_bru} µm '
                      f'(기본은 1.2·vox = {1.2 * a.step3_vox:.3f}) — 격자 수렴 시험용', flush=True)
            # ── ★ origin 앙상블 (2026-08-16, prereg sdcp_gain_prereg_20260816 §4) ──────────
            #   격자 **위상**만 바꾼다: lo 를 −s 로 내리면 셀 경계가 s 만큼 밀리고 침대는
            #   하나도 안 잃는다 (n = ceil((hi−lo)/vox) 라 축마다 셀이 하나 늘 뿐).
            #   ⚠ z 를 밀면 플레이트 평면도 같이 밀어야 한다 — 솔버는 셀 중심을
            #     (k+0.5)·vox 로 보므로 z_top/z_bot 에 **같은 s_z 를 더한다**.  그러면
            #     L = z_plate − z_b 가 불변이라 σ_eff 규약이 유지된다.
            #   왜 필요: 단일 origin 의 σ 는 위상에 2.4~5.8 % 흔들린다 (CL-30) — 그 잡음을
            #     물리로 오독하지 않으려면 앙상블 평균이 필요하다.
            _osh = np.array([float(x) for x in (a.step3_origin_shift or (0.0, 0.0, 0.0))],
                            np.float64)
            if (_osh < 0).any() or (_osh >= a.step3_vox).any():
                raise SystemExit(f'ABORT — --step3-origin-shift 는 축마다 [0, vox) 여야 한다 '
                                 f'(받은 {_osh.tolist()}, vox {a.step3_vox}).  그 밖이면 '
                                 f'위상 이동이 아니라 격자 자체가 달라진다')
            #  ⚠ periodic × origin-shift 는 **미검증 조합** — 리뷰 ② 픽스처에서 여분층이
            #    seam 을 조용히 끊었다 (σ 9.08e-4 → 6.0e-4 = 정확히 3e-3/5).  현행 캠페인은
            #    비주기라 불활성이지만, 조합이 켜지면 소리 없이 틀리므로 fail-closed.
            if getattr(a, 'periodic', False) and _osh.any():
                raise SystemExit('ABORT — --periodic 과 --step3-origin-shift 병용은 미검증 '
                                 '(여분층이 seam 을 끊는다, 리뷰 ② 재현).  둘 중 하나만 쓸 것')
            _lo3 = tuple(-_osh)
            #  방어적 초기화 — STEP3 가 예외로 건너뛰어도 매니페스트 조립이 죽지 않게.
            #  (실사고: STEP3 를 try 가 삼킨 뒤 매니페스트에서 NameError 로 다시 터졌다.)
            _zt3 = _zb3 = None
            _hi = tuple(np.asarray(_hi, np.float64) + _osh)
            if _osh.any():
                print(f'  STEP3: ★ origin 이동 {_osh.tolist()} µm (위상만; 침대 손실 없음)',
                      flush=True)
            if getattr(a, 'step3_sdcp_sphere_d', 0) > 0:
                print(f'  STEP3: ★ SDCP **부피-보존 구 스탬프** Ø{a.step3_sdcp_sphere_d} µm '
                      f'(d/vox = {a.step3_sdcp_sphere_d / a.step3_vox:.2f}) — 점 스탬프는 '
                      f'참부피의 {a.step3_vox ** 3 / (3.14159265 / 6 * a.step3_sdcp_sphere_d ** 3):.2f}배', flush=True)
            if int(getattr(a, 'step3_maxiter', 0) or 0) > 0:
                _s3.CG_MAXITER = int(a.step3_maxiter)
                print(f'  STEP3: CG maxiter {_s3.CG_MAXITER:,} (기본 30,000) — 조건수가 나쁜 '
                      f'팔을 수렴시키기 위한 것이지 규약 변경이 아니다', flush=True)
            _yv3 = bool(getattr(a, 'step3_sdcp_yield_to_vgcf', False))
            if _yv3:
                print('  STEP3: ★ **진단 팔** — SDCP 가 VGCF 셀에 양보한다 (σ-치환 채널 OFF, '
                      'CL-43).  ⚠ 생산 규약 아님', flush=True)
            sid3, pid3 = _s3.rasterize(_am_c, _am_r, t, _apts, _aph, _lo3, _hi, a.step3_vox,
                                       se_pts=_septs, add_fid=_afid, bridge_um=_bru,
                                       sdcp_sphere_d_um=getattr(a, 'step3_sdcp_sphere_d', 0.0),
                                       sdcp_yield_to_vgcf=_yv3,
                                       # ⚠ 도메인은 `se` 다 — `_m` 은 se 위의 마스크라
                                       #   `_kind_all[_m]` 이 성립하려면 len(_kind_all)==len(se).
                                       #   옛 코드는 `len(_fid_all)` 과 비교해 ⓐ 길이 불일치로
                                       #   `_fid_all=None` 이 된 뒤에는 TypeError 였고 ⓑ 애초에
                                       #   비교 대상이 틀렸다 (2026-08-20).
                                       add_kind=(_kind_all[_m] if _kind_all is not None
                                                 and len(_kind_all) == len(se) else None))   # SE stamped (sid 6) → ionic solve
            # ── ★ rasterize-only 원장 (2026-08-16, 심층 리뷰 ③ 제안) ─────────────────────
            #   왜: CL-34 의 "우선순위 결함이 σ_e 를 얼마나 부풀렸나" 를 **솔브 없이** 잰다.
            #   두 스탬프 순서(제자리 vs 루프-뒤)로 각각 구워 상별 셀 수를 diff 하면
            #   SDCP 가 PTFE/SWCNT 에서 뺏은 셀이 **직접** 나온다 — 대조 팔(GPU 1.5 h) 불요.
            #   ⇒ 순수 CPU 수 분.  돌고 있는 GPU 런과 자원 충돌 없음.
            if getattr(a, 'step3_rasterize_only', False):
                import json as _rj
                _led = {'vox_um': a.step3_vox, 'origin_shift_um': [float(x) for x in _osh],
                        'bridge_um': _bru, 'sdcp_yield_to_vgcf': _yv3,
                        'sdcp_sphere_d_um': float(
                            getattr(a, 'step3_sdcp_sphere_d', 0.0) or 0.0),
                        'grid_shape': [int(x) for x in sid3.shape],
                        'cells_by_sid': {int(k): int(v) for k, v in
                                         zip(*np.unique(sid3, return_counts=True))},
                        'vol_by_sid_um3': {}}
                for _k, _v in _led['cells_by_sid'].items():
                    _led['vol_by_sid_um3'][int(_k)] = float(_v) * a.step3_vox ** 3
                #  ★ 같은 입력으로 **반대 순서** 도 구워 diff 한다 (결함판 재현 = 규약 비교)
                if _led['sdcp_sphere_d_um'] > 0:
                    _alt, _ = _s3.rasterize(
                        _am_c, _am_r, t, _apts, _aph, _lo3, _hi, a.step3_vox, se_pts=_septs,
                        add_fid=_afid, bridge_um=_bru, sdcp_sphere_d_um=0.0,
                        sdcp_yield_to_vgcf=_yv3,          # 양쪽을 같은 규약으로 (like-for-like diff)
                        add_kind=(_kind_all[_m] if _kind_all is not None
                                  and len(_kind_all) == len(se) else None))   # 도메인 = se (위 주석)
                    #  결함판 재현: 구 셀을 **나중에** 덮어쓴다 (SDCP 가 PTFE/SWCNT 를 먹는다)
                    _sph_only = (sid3 == 5) & (_alt != 5)
                    _stolen = {}
                    for _k in np.unique(_alt[_sph_only]):
                        _stolen[int(_k)] = int((_alt[_sph_only] == _k).sum())
                    _led['sphere_extra_cells'] = int(_sph_only.sum())
                    _led['sphere_extra_from_sid'] = _stolen
                    _led['defect_would_steal'] = {
                        int(k): int(v) for k, v in _stolen.items() if k in (7, 8)}
                    _led['_note'] = ('sphere_extra_from_sid = 구 스탬프가 점 스탬프 대비 '
                                     '**추가로** 차지한 셀의 원래 상.  그 중 sid 7(PTFE)·'
                                     '8(SWCNT) 이 결함판에서 SDCP 가 **덮었을** 셀이다 — '
                                     '수정판은 그 둘을 양보하므로 diff 가 곧 결함의 크기다.')
                _rj.dump(_led, open(a.step3_rasterize_only, 'w'), ensure_ascii=False, indent=1)
                print(f'  STEP3 rasterize-only 원장 → {a.step3_rasterize_only}', flush=True)
                for _k in sorted(_led['cells_by_sid']):
                    print(f'    sid {_k} ({_s3.SID_NAME.get(_k, "pore" if _k == 0 else "?")}): '
                          f'{_led["cells_by_sid"][_k]:,} 셀 = '
                          f'{_led["vol_by_sid_um3"][_k]:,.1f} µm³', flush=True)
                if 'defect_would_steal' in _led:
                    print(f'    ★ 구 추가 셀 {_led["sphere_extra_cells"]:,} · '
                          f'그 중 결함판이 뺏었을 PTFE/SWCNT = {_led["defect_would_steal"]}',
                          flush=True)
                raise SystemExit(0)
            _sig3 = np.array([0.0, a.sigma_am_s, a.sigma_am_p, a.sigma_vgcf, a.sigma_superp, a.sigma_sdcp,
                              0.0, a.sigma_ptfe, a.sigma_swcnt])   # ELECTRONIC table: SE = e-insulator;
            #   idx7 = PTFE sensitivity hook (default 0 → sid7 미존재); idx8 = SWCNT sheath (A14, 도체)
            _ztop = float(sim_m.get('thickness_um') or ((top - FLOOR) * UM))   # PRESS PLANE (wall_z) —
            #   `top` has a +0.01-box (~0.4µm) void-cap padding that floats the plate off the bed
            #   crowns (kgy first run: no_plate_contact); the sim thickness is the physical plate.
            #  ★★ 격자 좌표계의 플레이트 평면 — **모든** 솔브가 이 두 값을 쓴다.
            #     origin 을 −s 로 내렸으므로 침대는 격자좌표 [s_z, s_z+두께] 에 놓인다.
            #     둘 다 s_z 를 더하므로 L = z_plate − z_b 는 **불변**이고 σ_eff 규약이 유지된다.
            #     ⚠ 2026-08-16 실사고: 정의를 위로 옮긴다면서 **주석만 넣고 대입을 빠뜨려**
            #       `NameError: _zt3` 로 판별 런이 죽었다 (STEP3 는 try 가 삼켜 "skipped" 로
            #       찍혔고, 매니페스트 조립에서 다시 터졌다).  ⇒ `_ztop` 직후에 못 박는다.
            _zt3, _zb3 = _ztop + float(_osh[2]), 0.0 + float(_osh[2])
            _res3 = _s3.solve_sigma_z(sid3, _sig3, a.step3_vox, return_field=True,
                                      z_top_um=_zt3, z_bot_um=_zb3, periodic_xy=a.periodic)
            if _res3.get('reason'):
                print(f"  ⚠ STEP3 σ_e not solvable: {_res3['reason']}")
                _s3mark('electronic', 'not_solvable', _res3['reason'])
                step3 = {'sigma_e_eff_S_cm': 0.0, 'reason': _res3['reason'], 'vox_um': a.step3_vox}
            elif _res3['n_dof']:
                je_am = np.nan_to_num(_s3.per_particle_current(_res3, sid3, pid3, _sig3, len(r)),
                                      nan=0.0, posinf=0.0, neginf=0.0)   # a bare NaN token kills JSON.parse
                _p998e = None                               # 필드 정량 스케일용 (아래 step3에 기록)
                if not a.no_field:                          # ELECTRONIC field (AM+carbon {1,2,3,4,5}) — the
                    _ep, _ej = _s3.field_point_cloud(       # paper Fig-4 grammar: |J_e| cloud, hot backbone
                        _res3, sid3, _sig3, a.step3_vox, (1, 2, 3, 4, 5, 7, 8), max_points=a.field_max_points)
                    if _ep is not None:
                        _ej = np.nan_to_num(_ej, nan=0.0, posinf=0.0, neginf=0.0)  # bare NaN kills JSON.parse
                        _p998e = max(float(np.percentile(_ej, 99.8)), 1e-30)
                        _ejn = _ej / _p998e                                        # p99.8-norm (top 0.2%>1,
                        elec_field = [[round(float(_ep[i, 0]), 2), round(float(_ep[i, 1]), 2),   # viewer clamps;
                                       round(float(_ep[i, 2]), 2), round(float(_ejn[i]), 4)]     # keeps dim-end
                                      for i in range(len(_ep))]                                  # range vs max-norm)
                        print(f"  STEP3 electronic FIELD: {len(elec_field):,} pts (AM+carbon |J| cloud)")
                _jhs = None                                 # #29 Joule 발열 hot-spot (전자망 q∝|J|²/σ; --joule-heat)
                if a.joule_heat:
                    _jhs = _s3.joule_hotspot(_res3, sid3, _sig3, a.step3_vox, (1, 2, 3, 4, 5, 7, 8),
                                             max_points=a.field_max_points)
                    if _jhs is not None:
                        _jq = np.nan_to_num(_jhs['q'], nan=0.0, posinf=0.0, neginf=0.0)
                        _p998j = max(float(np.percentile(_jq, 99.8)), 1e-30)
                        _jqn = _jq / _p998j                                        # p99.8-norm (전자/이온 필드 동일)
                        joule_field = [[round(float(_jhs['pts'][i, 0]), 2), round(float(_jhs['pts'][i, 1]), 2),
                                        round(float(_jhs['pts'][i, 2]), 2), round(float(_jqn[i]), 4)]
                                       for i in range(len(_jhs['pts']))]
                        print(f"  STEP3 Joule hot-spot: {len(joule_field):,} pts · 집중 hot_frac_50 "
                              f"{_jhs['hot_frac_50']:.3f} (작을수록 집중) · conc {_jhs['conc_ratio']:.1f}× — 어디서 발열 몰리나")
                _share = _s3.phase_current_share(_res3, sid3, _sig3)
                _sname = _s3.SID_NAME
                #  ★ 2026-08-20 (전수 감사 코드 하위 γ) — **미수렴을 `complete` 로 적지 않는다.**
                #    판정기(`sdcp_gain_verdict`)는 `cg_info`/`unconverged` 를 직접 보므로
                #    prereg 는 안전했지만, manifest 의 component status 만 읽는 소비자는
                #    "완료" 로 오독한다 (선언과 실행이 갈라지는 바로 그 자리).
                _s3mark('electronic',
                        'unconverged' if _res3.get('unconverged') else 'complete',
                        (f"cg_info={_res3.get('cg_info')} resid={_res3.get('cg_resid')}"
                         if _res3.get('unconverged') else ''))
                #  ★★ 2026-08-20 (Codex 재검증 §D-2-가) — **저장 정밀도를 깎지 않는다.**
                #    옛 판은 σ 를 `.4g`, residual 을 `.2g` 로 **저장**했다.  화면 서식이 아니라
                #    **파일에 들어가는 값**이라, 판정기가 "raw solver precision 으로 1 % 게이트를
                #    건다" 고 선언해도 실행이 불가능했다 (원값이 이미 없다).
                #    실증: vox 0.115 DBE 8팔 중 4팔이 4자리 반올림으로 **같은 값(0.05272)** 이 됐다.
                #    ⇒ 원값을 그대로 싣는다.  화면 출력은 아래 print 가 따로 `.4g` 로 줄인다.
                step3 = {'sigma_e_eff_S_cm': float(_res3['sigma_eff']),
                         'vox_um': a.step3_vox, 'n_dof': _res3['n_dof'],
                         'k_plates': list(_res3.get('k_plates', ())),
                         'n_floating_dropped': _res3.get('n_floating_dropped', 0),
                         'cg_resid': float(_res3['resid']),
                         #  ★ 수렴 판정을 **기계가 읽을 수 있게** 남긴다 (사전등록 §5-1).
                         #    실사고 2026-08-16: 판정기가 없는 필드를 읽어 미수렴 게이트가
                         #    fail-open 이었다 (resid 는 로그에만 있었다).
                         'cg_info': int(_res3.get('cg_info', 0) or 0),
                         'unconverged': bool(_res3.get('unconverged', False)),
                         'dissipation_share': {_sname[k]: round(v, 4) for k, v in _share.items()},
                         'sigma_table_S_cm': {'AM_S': a.sigma_am_s, 'AM_P': a.sigma_am_p,
                                              'VGCF': a.sigma_vgcf, 'SuperP': a.sigma_superp,
                                              'SDCP': a.sigma_sdcp, 'SWCNT': a.sigma_swcnt,
                                              'SWCNT_ion_mode': ('blocked_UB_scenario' if a.swcnt_ion_block
                                                                 else 'SE_transparent_default'),
                                              **({'PTFE': a.sigma_ptfe} if a.sigma_ptfe > 0 else {})},
                         # ★A8: CAM 프리셋 provenance (nca σ = Amin 2015 충전-상단 1e-2 S/cm,
                         #   리튬화 1e-4 캐비엇; E_AM은 프리셋 불변 — nca_material_preset.md)
                         'cam_preset': {'cam': a.cam,
                                        **({'sigma_note': 'NCA: Amin/Chiang JES 2015 sintered-pellet '
                                                          'charged-state upper end 1e-2 S/cm (lithiated '
                                                          '1e-4, 2-decade SOC swing); S=P (no SC/PC split '
                                                          'data for NCA); E_AM kept 140 GPa (Kang 175 = '
                                                          'assumed, see docs/nca_material_preset.md)'}
                                           if a.cam == 'nca' else {})},
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
                # ★ 단일 출처 (2026-07-21): 시나리오 R_int 값은 정본 docs/data/rint_eis_anchors.csv에서
                #   읽음(rint_cycle_traj.load_scenario 재사용) — payload/app.py/CSV 3중 하드코딩이
                #   정밀-digitize 업데이트 시 어긋나는 미래 위험 제거.  ⚠ load_scenario는 키 부재 시
                #   SystemExit(BaseException) → Exception만 잡으면 payload가 죽음.
                try:
                    from rint_cycle_traj import load_scenario as _ls_rint
                    # (r0, rc, ntot, prec) 전체 유지 — precision 라벨도 CSV 단일 출처 (정밀 digitize가
                    # CSV precision 컬럼을 바꾸면 라벨까지 일괄 반영; 하드코딩 'panel_e_approx' 금지)
                    _scn_vals = {k: tuple(_ls_rint(k)) for k in ('sbe', 'dbe', 'csus', 'sus')}
                    _scn_src = 'docs/data/rint_eis_anchors.csv (정본, scenario keys)'
                except (Exception, SystemExit) as _e_rs:
                    _scn_vals = {'sbe': (18.0, 110.0, 1000, 'panel_e_approx'),
                                 'dbe': (12.0, 46.0, 1000, 'panel_e_approx'),
                                 'csus': (10.0, 30.0, 1000, 'panel_e_approx'),
                                 'sus': (50.0, 150.0, 1000, 'measured_projected')}   # 이종기술 SUS 실측50/투영150
                    _scn_src = f'fallback snapshot 2026-07-21 (anchors CSV unreadable: {_e_rs})'
                _pri_prec = '/'.join(sorted({str(v[3]) for v in _scn_vals.values()}))
                _nm_fmt = {'sbe': 'SBE_bare_{:g}', 'dbe': 'DBE_bare_{:g}',
                           'csus': 'SBE_CSUS_{:g}_proxy_DBE_anchored',   # SBE+C-SUS 미측정 → DBE-앵커 proxy
                           'sus': 'isotech_SUS_{:g}'}                    # 이종기술 SUS 실측50/투영150
                _cyc_pairs = ([('ideal_R0', 0.0)]
                              + [(_nm_fmt[k].format(_scn_vals[k][1]), _scn_vals[k][1])
                                 for k in ('sbe', 'dbe', 'csus', 'sus')])
                _pri_pairs = ([('ideal_R0', 0.0)]
                              + [(_nm_fmt[k].format(_scn_vals[k][0]), _scn_vals[k][0])
                                 for k in ('sbe', 'dbe', 'csus', 'sus')])
                step3['collector'] = {'kind': 'SCENARIO series load — measured R_int applied '
                                              'externally (NOT a model prediction; the model\'s own '
                                              'interface OUTPUT is collector_geometric.R_geom)',
                                      'R_bulk_ohm_cm2': float(f'{_Rbulk:.3g}'),
                                      'anchors': 'Fig6e R_int (cycled=1000cyc@2C, pristine=panel-e≈); '
                                                 'S14 primer 1.3e4 S/cm 200nm',
                                      'anchors_source': _scn_src,
                                      'sigma_apparent_S_cm': {
                                          nm2: float(f'{_Lcm / (_Rbulk + _R):.3g}')
                                          for nm2, _R in _cyc_pairs},
                                      # ★ A11-③ (§6.1 시간축 분리): pristine 세트 병기 — BOL(fresh) 벌크와
                                      #   시간-일관인 fresh+fresh 조합.  cycled 세트는 "fresh 전극 + aged
                                      #   접촉" 민감도 시나리오로 라벨 (혼합 금지·병기).
                                      'sigma_apparent_pristine_S_cm': {
                                          nm2: float(f'{_Lcm / (_Rbulk + _R):.3g}')
                                          for nm2, _R in _pri_pairs},
                                      'time_axis': 'sigma_apparent_S_cm = aged R_int(1000cyc@2C) × BOL 벌크 '
                                                   '= 민감도 시나리오; sigma_apparent_pristine_S_cm = '
                                                   'pristine R_int × BOL 벌크 = 시간-일관(물리적 BOL 풀셀)',
                                      'pristine_precision': f'{_pri_prec} — CSV precision 컬럼에서 유도'
                                                            '(정밀 디지타이즈 시 CSV만 갱신하면 일괄 반영); '
                                                            'docs/data/rint_eis_anchors.csv scenario keys'}
                print(f"  STEP3 σ_e_eff = {step3['sigma_e_eff_S_cm']:.4g} S/cm  (vox {a.step3_vox}µm, "
                      f"{_res3['n_dof']:,} dof, resid {_res3['resid']:.1e}, {_time.time()-_t0:.0f}s)  "
                      f"share: " + " ".join(f"{k} {100*v:.0f}%" for k, v in step3['dissipation_share'].items()))
                if _jhs is not None:                        # #29 Joule 발열 hot-spot 요약 (joule_field는 별도 export)
                    step3['joule'] = {'hot_frac_50': _jhs['hot_frac_50'], 'conc_ratio': round(_jhs['conc_ratio'], 2),
                                      'n_pts': _jhs['n'],
                                      'note': 'Joule 발열밀도 q∝|J|²/σ (전자망, run-relative) — 어디서 발열 몰리나. '
                                              'hot_frac_50=q 총합 50% 담는 상위복셀 분율(작을수록 집중).  ★절대 ΔT(K)·'
                                              'STEP5 R(N) Arrhenius 연동 = LPSCl 분해 Eₐ 앵커 대기(v2).'}
                if a.collector_rint >= 0.0:                # UI-selected preset → highlighted entry
                    _sel = {
                        'name': a.collector_name or f'R{a.collector_rint:g}',
                        'R_int_ohm_cm2': a.collector_rint,
                        'sigma_apparent_S_cm': float(f'{_Lcm / (_Rbulk + a.collector_rint):.3g}')}
                    if a.collector_scenario in _scn_vals:  # 시간축 짝값 병기 (선택=cycled, pristine 함께)
                        _r0s = _scn_vals[a.collector_scenario][0]
                        _sel.update({'scenario_key': a.collector_scenario,
                                     'time_axis': 'R_int_ohm_cm2 = cycled(aged-접촉 민감도); '
                                                  'pristine 짝 = 시간-일관 BOL 풀셀',
                                     'R_int_pristine_ohm_cm2': float(_r0s),
                                     'sigma_apparent_pristine_S_cm':
                                         float(f'{_Lcm / (_Rbulk + _r0s):.3g}'),
                                     'pristine_precision': str(_scn_vals[a.collector_scenario][3])})
                    step3['collector']['selected'] = _sel
                _ca = step3['collector']['sigma_apparent_S_cm']
                # carbon-free/희박 배선 케이스는 R_bulk가 계면(30-110)과 동급까지 올라옴 — "≪" 고정
                # 문구가 그 regime에서 거짓이 되던 것을 조건화 (260714 carbon-free: R_bulk 12 Ωcm²)
                _rel = ('≪ 계면' if _Rbulk < 3.0 else
                        '≈ 계면과 동급 — carbon-free/희박 배선 regime' if _Rbulk < 100.0 else '≫ 계면(!)')
                print(f"  STEP3 collector scenarios(cycled): bulk {_ca['ideal_R0']:.3g} → "
                      + " / ".join(f"{nm2}({_R:g}Ωcm²) {_ca[nm2]:.3g}" for nm2, _R in _cyc_pairs[1:])
                      + f" S/cm  (R_bulk {_Rbulk:.2g} Ωcm² {_rel})")
                _cp = step3['collector']['sigma_apparent_pristine_S_cm']
                print("  STEP3 collector PRISTINE(시간-일관, panel-e≈): "
                      + " / ".join(f"{nm2}({_R:g}) {_cp[nm2]:.3g}" for nm2, _R in _pri_pairs[1:])
                      + " S/cm  (위 cycled 세트=aged-접촉 민감도)")
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
                # ★★ 2026-08-18 — `--no-collector`.  이 블록은 σ_e 솔브를 **2회 더** 돈다
                #   (wetted/bare 집전체 기하).  LEAN 플래그로 못 껐고, vox 0.125 스윕이 **여기서**
                #   OOM 으로 죽었다 (`p2_DBE_sph_a3`: 전자 솔브는 0.06071 로 수렴 완료 후 사망).
                #   ⚠ 게다가 shift 팔에서는 `_bot_mask` 가 origin 이동을 안 더해 **어차피 틀린 값**이다
                #   (러너 주석이 이미 그렇게 적고 있었다).  ⇒ 스윕에서는 끈다: 시간 3배 절약 + OOM 해소.
                if a.no_collector:
                    _s3mark('collector_geom', 'disabled',
                            '--no-collector (σ_e 전용 스윕; shift 팔에서는 _bot_mask 가 origin 을 안 더해 값 자체가 무효)')
                    print('  STEP3: --no-collector — 집전체 기하 솔브 2회 건너뜀 (wetted/bare)', flush=True)
                    _res3w = _res3b = None
                    jb_am = None
                else:
                    _mw, _mb = _bot_mask(0.30), _bot_mask(0.10)
                    _res3w = _s3.solve_sigma_z(sid3, _sig3, a.step3_vox, return_field=False,
                                               z_top_um=_zt3, z_bot_um=_zb3, bot_allowed=_mw, periodic_xy=a.periodic)
                    _res3b = _s3.solve_sigma_z(sid3, _sig3, a.step3_vox, return_field=True,
                                               z_top_um=_zt3, z_bot_um=_zb3, bot_allowed=_mb, periodic_xy=a.periodic)
                    jb_am = None
                    if 'phi' in _res3b:
                        jb_am = np.nan_to_num(_s3.per_particle_current(_res3b, sid3, pid3, _sig3, len(r)),
                                              nan=0.0, posinf=0.0, neginf=0.0)
                    # R_geom = the interface resistance the GEOMETRY itself creates (bare contact
                    # starving vs film-wetted) — the MODEL'S OWN emergent interface number (an OUTPUT;
                    # 측정 R_int는 결과값이지 설정값이 아님).  measured R_int − R_geom = the chemistry/
                    # degradation share the structure model does NOT contain (quantified limit).
                    _swR = float(_res3w['sigma_eff']); _sbR = float(_res3b['sigma_eff'])
                    # _sw/_sb MUST be defined on BOTH paths — the dict below (:wetted/bare_sigma)
                    # reads them unconditionally.  Hoist the clamp above the guard so the
                    # degenerate branch (_rgeom=None) does NOT raise NameError and drop the
                    # whole STEP3/STEP4 output via the broad except.  (fix: guard was crashing
                    # in exactly the corner it targets.)
                    _sw = max(_swR, 1e-30); _sb = max(_sbR, 1e-30)
                    # 가드(#9 code-review): 축퇴/실패 solve(σ≤0 or reason)면 R_geom을 계산하지 말 것 —
                    # 1e-30 클램프가 _Lcm/σ ≈ 1e27 Ω·cm² 를 만들어 'MODEL OUTPUT'으로 뱉는 걸 막는다.
                    if _res3b.get('reason') or _res3w.get('reason') or _swR <= 0.0 or _sbR <= 0.0:
                        _rgeom = None
                    else:
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
                # ★ φ(z)/T(z) 프로파일 헬퍼 (Oh 2025 primer 논문 Fig 4e 문법 = ΔV=1V 전도 솔브의
                # 두께방향 전위) — 층별 전도-복셀 평균.  solve 규약: 바닥판 φ=1, 꼭대기 φ=0.
                # ★ 여기(이온 solve 前)에 두는 이유: 예전엔 `if _res3i['n_dof']:` 안에서 정의돼
                #   SE 미퍼콜(n_dof=0) 케이스에서 이름 자체가 없었다 — 아래 thermal 블록이 이걸
                #   부르는 순간 좋은 압밀 뒤에 NameError 로 payload 가 죽는다 (2026-06-21 `geom`
                #   사고와 같은 형태).  호출부보다 얕은 스코프에서 무조건 정의한다.
                def _phi_prof(_resX):
                    if not _resX or 'phi' not in _resX:
                        return None
                    _P, _C = _resX['phi'], _resX['cond']
                    _pz, _zz = [], []
                    for _k in range(sid3.shape[2]):
                        _m3 = _C[:, :, _k]
                        if _m3.any():
                            _pz.append(float(_P[:, :, _k][_m3].mean()))
                            _zz.append(round((_k + 0.5) * a.step3_vox, 3))
                    return {'z_um': _zz, 'phi': [float(f'{v:.5g}') for v in _pz]}
                # IONIC network on the SAME grid (paper Fig-2d/f axis): SE + SDCP conduct Li⁺
                # (user principle — SDCP is NOT an ion insulator), AM/carbon/PTFE block.
                # ★★ 2026-08-18 — `--no-ion`.  두 가지를 동시에 푼다:
                #   ① **OOM** — vox 0.125 스윕이 여기서 죽었다 (`Killed`, 36.7 M dof 이온계를 조립하는
                #      중).  전자계(45.1 M dof)가 이미 잡고 있는 메모리 위에 얹히고, 호스트 RAM 62 GB
                #      중 가용이 22 GB 까지 내려간 상태였다.  전자 σ_e 만 필요한 스윕에서 이온계는
                #      **순수 낭비**다.
                #   ② **DR3-07 이 예언한 대로** vox ≤ 0.125 의 σ_ion·τ_pore 는 인용 금지다 — 실제로
                #      pore-τ 가 1,415 (0.15) → **4.97e9** (0.125), closed-from-top 28.5 % → 99.2 % 로
                #      터졌다.  쓸 수 없는 값을 위해 죽을 이유가 없다.
                #   ⚠ 기본은 끄지 않는다 (생산 payload 는 이온망이 있어야 한다).
                _t1 = _time.time()
                # idx8 SWCNT = 기본 SE-투명(σ_i=σ_ion_se): 실제 skin 2-10nm sub-voxel → 1-voxel
                # 스탬프가 이온망을 끊으면 차단 40-200× 과대표현(trade-off 상한 이중계상).
                # --swcnt-ion-block = 상한 시나리오 opt-in (σ_i=0 → 해당 복셀 이온 dof·BV면 소멸).
                _sig3i = np.array([0.0, 0.0, 0.0, 0.0, 0.0, a.sigma_ion_sdcp, a.sigma_ion_se, 0.0,
                                   0.0 if a.swcnt_ion_block else a.sigma_ion_se])
                #  ⚠ **끈 것과 못 푼 것을 구분한다** — n_dof=0 스텁으로 아래 분기를 건너뛰되
                #    상태는 `disabled` 로 남긴다.  `not_solvable`(SE 미퍼콜) 로 적으면 거짓말이다.
                if a.no_ion:
                    _s3mark('ionic', 'disabled', '--no-ion (σ_e 전용 스윕; DR3-07 로 vox ≤ 0.125 '
                                                 'σ_ion 은 어차피 인용 금지)')
                    print('  STEP3: --no-ion — 이온 솔브 건너뜀 (σ_e 전용).  '
                          'σ_ion·τ_full·Track-B 는 이 payload 에 **없다**', flush=True)
                    _res3i = {'n_dof': 0}
                else:
                    _res3i = _s3.solve_sigma_z(sid3, _sig3i, a.step3_vox, return_field=True,
                                               z_top_um=_zt3, z_bot_um=_zb3, periodic_xy=a.periodic)
                if _res3i['n_dof']:
                    _sharei = _s3.phase_current_share(_res3i, sid3, _sig3i)
                    if not a.no_field:                      # IONIC field (SE+SDCP {5,6}) — Li⁺ |J| cloud,
                        _ip, _ij = _s3.field_point_cloud(   # the partner panel to the electronic field
                            _res3i, sid3, _sig3i, a.step3_vox, (5, 6, 8), max_points=a.field_max_points)
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
                    # 전자(정본) + 전자(bare 집전체: 계면 강하 그림) + 이온 3곡선 (헬퍼는 위에서 정의).
                    step3['phi_profile'] = {k: v for k, v in {
                        'electronic': _phi_prof(_res3), 'electronic_bare': _phi_prof(_res3b),
                        'ionic': _phi_prof(_res3i)}.items() if v}
                    step3['phi_profile']['note'] = ('ΔV=1V 전도 솔브 층별 전도-복셀 평균 φ '
                                                    '(바닥판 φ=1, 꼭대기 φ=0; Oh2025 Fig4e 문법)')
                    #  ★★ 2026-08-24 (CDXR2-4) — **이온도 미수렴을 `complete` 로 적지 않는다.**
                    #    2026-08-20 감사 γ 가 **전자 경로만** 고쳤고(:1198) 이온 쌍둥이는 그대로
                    #    무조건 'complete' 였다 = 같은 결함의 3회차 (웹앱↔킷 쌍둥이 결함과 같은
                    #    뿌리 — CLAUDE.md frame[5] ⚠).  게다가 이쪽은 전자와 달리 `cg_info`·
                    #    `unconverged` 를 **payload 에 싣지도 않아** 판정기가 볼 것 자체가 없었다
                    #    (`--require-ionic` 은 양의 σ_ion 존재만 본다) = fail-open.
                    _ion_unconv = bool(_res3i.get('unconverged', False))
                    _s3mark('ionic', 'unconverged' if _ion_unconv else 'complete',
                            (f"cg_info={_res3i.get('cg_info')} resid={_res3i.get('resid')}"
                             if _ion_unconv else ''))
                    step3['sigma_ion_eff_S_cm'] = float(_res3i['sigma_eff'])
                    #  ★ 판정기가 **기계로** 읽는 이온 수렴 봉인 (전자의 cg_info/unconverged 와 대칭)
                    step3['ion_cg_info'] = int(_res3i.get('cg_info', 0) or 0)
                    step3['ion_unconverged'] = _ion_unconv
                    step3['ion_dissipation_share'] = {_s3.SID_NAME.get(k, str(k)): round(v, 4)
                                                      for k, v in _sharei.items()}
                    step3['sigma_ion_table_S_cm'] = {'SE': a.sigma_ion_se, 'SDCP': a.sigma_ion_sdcp}
                    # T1-a provenance: which temperature convention produced this σ_ion?
                    step3['temperature_provenance'] = dict(_temp_prov)
                    step3['sigma_ion_se_at_T_ref_S_cm'] = a._sigma_ion_se_ref
                    step3['ion_resid'] = float(_res3i['resid'])
                    print(f"  STEP3 σ_ion_eff = {step3['sigma_ion_eff_S_cm']:.4g} S/cm  "
                          f"({_res3i['n_dof']:,} dof, resid {_res3i['resid']:.1e}, {_time.time()-_t1:.0f}s)  "
                          f"share: " + " ".join(f"{k} {100*v:.0f}%"
                                                for k, v in step3['ion_dissipation_share'].items()))
                    # ★ Track-B — COMSOL 하이브리드(AM 해상구 + SE 연속체) 파라미터: τ_full/τ_geo/
                    #   κ_dom + AM 표면 face-walk 패치 분율.  κ_dom 이중계상 가드: 하이브리드는 AM
                    #   구를 기하로 해상하므로 AM-장애물 굴곡도는 모델이 스스로 만든다 → SE 연속체에
                    #   줄 전도도는 σ_bulk·(φ_full/τ_full)/(φ_geo/τ_geo) 여야 한다 (τ_geo = "AM
                    #   여집합을 꽉 찬 SE 로 이상화"한 같은 복셀 Laplace 해 — kdom_calibration).
                    if not a.no_trackb:
                        _tb = {}
                        try:
                            _t7 = _time.time()
                            # 구세대 체크아웃 가드 (리뷰 minor): 헬퍼 부재 시 τ_geo 대형 솔브를
                            # 돌기 전에 저비용으로 error 경로로 — V100 등에서 git pull 누락 대비
                            if not hasattr(_s3, 'tau_from_solve'):
                                raise AttributeError('step3_sigma 에 Track-B 헬퍼 부재 '
                                                     '(tau_from_solve 등) — git pull 필요')
                            # 크롭: pore_tau 와 같은 규약 — rasterize 박스 상단의 void 패딩 캡을
                            # 빼고 z ≤ 두께만 잰다 (pore_tau docstring 의 크롭 근거 참조)
                            _nzc = max(2, min(sid3.shape[2],
                                              int(np.floor(float(_ztop) / a.step3_vox + 0.5))))
                            _sidc = sid3[:, :, :_nzc]
                            _cnt = np.bincount(_sidc.ravel().astype(np.int64), minlength=len(_sig3i))
                            _tb.update({'tau_convention': 'linear: sigma_eff = sigma_bulk*phi/tau',
                                        'crop_nz': int(_nzc),
                                        'phi_denominator': 'cropped_total_voxels',
                                        # 심화리뷰 physics: pkg 가 자기 BC·해상도·온도를 말해야
                                        # B1 비교조건이 판별된다 (periodic↔절연벽 D_geo +5.1% /
                                        # vox 계단 → κ_dom +13~16% @0.4 / σ 는 T-스케일 후 solve)
                                        'periodic_xy': bool(a.periodic),
                                        'vox_um': float(a.step3_vox),
                                        'sigma_declared_at_T_C': (
                                            float(a.temp_c) if getattr(a, 'temp_c', None)
                                            is not None else None)})
                            # φ_full = 이온 전도상 복셀 분율.  전도집합 = σ_i>0 이고 격자에 실재하는
                            # sid — 테이블에 σ>0 이어도 복셀 0개면 solve 에 없다 (부재상으로
                            # mixed_phase 오탐하지 않기 위해 실재만 센다)
                            _csid = [s for s in range(len(_sig3i)) if _sig3i[s] > 0.0 and _cnt[s] > 0]
                            _phi_full = float(sum(int(_cnt[s]) for s in _csid)) / float(_sidc.size)
                            _tb['phi_full'] = float(f'{_phi_full:.6g}')
                            # 균일성 가드: 전도상 σ 가 서로 다르면 (예: SDCP 1e-3 ≠ SE) 단일 σ_bulk
                            # 기반 τ 가 정의 불가 → tau_full=None + reason (§F1: 날조 금지)
                            _sigs = sorted({float(_sig3i[s]) for s in _csid})
                            if len(_sigs) == 1:
                                _tb['mixed_phase'] = None
                                _tb['sigma_bulk_ion_S_cm'] = _sigs[0]
                                _tau_full = _s3.tau_from_solve(_phi_full, _sigs[0],
                                                               float(_res3i['sigma_eff']))
                            else:
                                # TODO(trackb): mixed 이온상(예: SDCP+SE) 의 단일 σ_bulk 환원 규약
                                # 미결 — 지금은 None+reason 이 정직(§F1), 하이브리드는 sigma_ion_eff
                                # 를 직접 쓰거나 SE-only 재솔브 필요
                                _tau_full = None
                                _tb['sigma_bulk_ion_S_cm'] = None
                                _tb['mixed_phase'] = {
                                    'sigma_by_sid_S_cm': {_s3.SID_NAME.get(s, str(s)): float(_sig3i[s])
                                                          for s in _csid},
                                    'reason': ('conducting phases carry unequal sigma_ion → single-'
                                               'sigma_bulk tau undefined; use sigma_ion_eff_S_cm')}
                            _tb['tau_full'] = None if _tau_full is None else float(f'{_tau_full:.4g}')
                            # τ_geo: AM(sid 1,2)=0.0 / 나머지(void 포함) 전부 1.0 — 순수 AM-장애물
                            # 기하 굴곡도.  σ_bulk=1 이므로 sigma_eff 가 곧 D_rel.
                            # ★ 크롭 그리드로 푼다 (리뷰 major, 합성 실측 +1~12% 편향): geo 테이블은
                            #   void 도 σ=1 이라 rasterize 상단 패딩 캡이 도전층으로 남아 plate 가
                            #   캡을 잰다 — pore_tau docstring 이 명시한 바로 그 실패 모드.  이온
                            #   τ_full 솔브(_res3i)는 void σ=0 이라 무영향이므로 그대로 둔다.
                            _sig_geo = np.array([1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
                            _res_geo = _s3.solve_sigma_z(_sidc, _sig_geo, a.step3_vox, z_top_um=_zt3,
                                                         z_bot_um=_zb3, periodic_xy=a.periodic)
                            _D_geo = float(_res_geo['sigma_eff'])
                            _phi_geo = 1.0 - float(int(_cnt[1]) + int(_cnt[2])) / float(_sidc.size)
                            _tau_geo = _s3.tau_from_solve(_phi_geo, 1.0, _D_geo)
                            _tb['phi_geo'] = float(f'{_phi_geo:.6g}')
                            _tb['tau_geo'] = None if _tau_geo is None else float(f'{_tau_geo:.4g}')
                            _tb['D_rel_geo'] = float(f'{_D_geo:.4g}')
                            if _res_geo.get('reason'):
                                _tb['geo_reason'] = _res_geo['reason']
                            _kdom = _s3.kdom_calibration(_phi_full, _tau_full, _phi_geo, _tau_geo)
                            _tb['kdom_ratio'] = None if _kdom is None else float(f'{_kdom:.4g}')
                            _tb['kappa_dom_S_cm'] = (
                                None if (_kdom is None or _tb['sigma_bulk_ion_S_cm'] is None)
                                else float(f"{_kdom * _tb['sigma_bulk_ion_S_cm']:.4g}"))
                            if _kdom is not None and _kdom > 1.0:
                                print(f'  ⚠ Track-B κ_dom/σ_bulk = {_kdom:.3g} > 1 — 규약/입력 '
                                      '불일치 신호 (AM-장애물 굴곡도보다 좋은 유효전도?)')
                            # per-particle AM 표면 패치 (COMSOL 구면 f_cov 경계조건용).  n_am 은
                            # rasterize 입력 배열 길이를 명시 — pid.max()+1 추정 금지 (SuperP
                            # _fid.max()+1 전역오프셋 버그의 회귀 방지)
                            _pp = _s3.am_surface_patches(sid3, pid3, len(_am_c),
                                                         periodic_xy=bool(a.periodic))
                            # isfinite 벨트 (리뷰 minor): 헬퍼가 den=max(n_face,1) 로 NaN 을 막지만
                            # ('bare NaN kills JSON.parse' — 이 파일의 확립 규약) 계약 변경에도
                            # payload JSON 이 죽지 않게 한 겹 더
                            _tb['per_particle'] = {
                                'n_face': [int(v) for v in _pp['n_face']],
                                **{_k: [round(float(v), 4) if np.isfinite(v) else 0.0
                                        for v in _pp[_k]]
                                   for _k in ('f_reaction', 'f_carbon', 'f_void', 'f_block')}}
                            # face-walk 클래스 평균 vs 기존 coverage — 교차확인 print 만 (저장 안 함;
                            # 잣대가 다름: face-walk=복셀 면 인접, coverage=Hertz 0.13µm 밴드)
                            _fr = np.asarray(_pp['f_reaction'], float)
                            _cchk = ' · '.join(
                                f"{_nm} face-walk {100.0 * float(_fr[t == _ty].mean()):.1f}% "
                                f"vs cov(Hertz) {cov_bands[_nm][0]}%"
                                for _ty, _nm in ((1, 'AM_P'), (2, 'AM_S')) if (t == _ty).any())
                            if _cchk:
                                print('  Track-B f_reaction ' + _cchk)
                            step3['trackb'] = _tb
                            print(f"  Track-B: τ_full {_tb['tau_full']} · τ_geo {_tb['tau_geo']} · "
                                  f"κ_dom/σ_bulk {_tb['kdom_ratio']} "
                                  f"({'mixed' if _tb['mixed_phase'] else 'uniform'}) · "
                                  f"crop_nz {_nzc} ({_time.time()-_t7:.0f}s)")
                        except Exception as _e_tb:
                            # 조용히 삼키지 않는다 — 2026-06-21 geom NameError 사고(정상 압밀 뒤
                            # payload 통째 사망)의 재발 방지: 부분결과 + error 키를 남기고 STEP3 유지
                            step3['trackb'] = {**_tb, 'error': f'{type(_e_tb).__name__}: {_e_tb}'}
                            print(f'  ⚠ Track-B failed ({type(_e_tb).__name__}: {_e_tb}) — '
                                  'step3.trackb.error 기록, STEP3 결과는 유지')
                elif not a.no_trackb and not a.no_ion:
                    #  ⚠ `and not a.no_ion` — 끈 것을 "SE 미퍼콜" 로 적으면 거짓 진단이 원장에 남는다.
                    # 심화리뷰 minor: 이온 n_dof=0 (SE 미퍼콜 퇴화) — trackb 키가 아예 없으면
                    # exporter 가 "구세대 trackb 부재 → 재실행" 으로 오진한다.  재실행해도 같으니
                    # 원인을 스텁으로 명시 (§F1 정직 null 관례)
                    _s3mark('ionic', 'not_solvable',
                            'n_dof=0 (SE non-percolating)')     # ★ RC6-06: 채널 상태를 남긴다
                    step3['trackb'] = {'reason': 'ionic solve n_dof=0 (SE non-percolating) — '
                                                 'trackb undefined; 재실행으로 해소되지 않음'}
                # ── STEP3 열전도 (σ_thermal, 多상 k) — 同 sid3 격자 재사용, ∇·(k∇T)=0 (σ_e/σ_ion과 동일 솔버) ──
                if a.no_thermal:
                    #  ★★ 2026-08-25 (M-R3-03, Codex 재리뷰) — **끈 것을 disabled 로 적는다.**
                    #    옛 판은 `--no-thermal` 에서 아무 기록도 안 남겨 thermal 이
                    #    `missing` 으로 채워졌고, 내가 오늘 넣은 required 게이트가 그것을
                    #    실패로 세어 **LEAN=1/2 생산 스윕 팔 전부가 exit 3** 이 됐다.
                    #    (ion·pore 는 이미 disabled 를 적고 있었다 — thermal 만 빠져 있었다.)
                    _s3mark('thermal', 'disabled', '--no-thermal (σ_e 전용 스윕)')
                if not a.no_thermal:
                    try:
                        _kt, _kprov = _s3.thermal_k_table(k_carbon=a.k_carbon)
                        _th = _s3.solve_thermal(sid3, a.step3_vox, _zt3, _zb3, _kt,
                                                field_sids=(None if a.no_field else (1, 2, 3, 4, 5, 6, 7, 8)),
                                                field_max=a.field_max_points, periodic_xy=a.periodic)
                        _tfp = _th.pop('_field_pts', None)
                        _tfj = _th.pop('_field_j', None)
                        _tres = _th.pop('_res', None)          # T(z) 프로파일용 (JSON 前 pop 필수)
                        step3['thermal'] = {
                            'k_eff_W_mK': _th['k_eff_W_mK'], 'n_dof': _th['n_dof'],
                            'cg_resid': _th['cg_resid'], 'temp_drop_share': _th.get('temp_drop_share'),
                            'status': _s3mark('thermal', 'complete')['status'],
                            'k_table_provenance': _kprov,
                            'trust': ('k_eff = 문헌/ASSUMED k 입력의 복셀-solve 전파값 — 열전도 실험 앵커 없음(Kapitza '
                                      '무시 상한); 多상 k(全상 열통과, σ_e[AM만]/σ_ion[SE만] 단상과 다름); SE=Ketter2025'
                                      '(LPSCl) 문헌앵커, AM=generic NCM 문헌-order(전용 인용 없음, NOT Ketter), '
                                      'carbon/SDCP/PTFE/pore=ASSUMED(소분율·--k-carbon 스윕); network_conductivity '
                                      'thermal과 같은 k 앵커 공유 → 표현-일치만, 스케일 다름(W/mK vs mScm-eq), 독립검증 아님'
                                      + (' ⚠UNCONVERGED' if _th.get('unconverged') else ''))}
                        # ★ T(z)@ΔT=1 프로파일 — 전자 φ(z)/이온 φ(z) 와 같은 층평균 문법(_phi_prof).
                        #   열전도는 多상(全상 열통과)이라 마스크가 전자/이온보다 넓다 = 자기 solve 의 것.
                        if _tres is not None:
                            _tprof = _phi_prof(_tres)
                            if _tprof:
                                step3.setdefault('phi_profile', {})['thermal'] = _tprof
                        if _tfp is not None and _tfj is not None:   # 열류 |k∇T| 필드 (전자/이온 필드 문법)
                            _tfj = np.nan_to_num(_tfj, nan=0.0, posinf=0.0, neginf=0.0)
                            _p998t = max(float(np.percentile(_tfj, 99.8)), 1e-30)
                            _tfjn = _tfj / _p998t                   # p99.8 정규화 (상위 0.2%>1 = 열 hot-spot)
                            thermal_field = [[round(float(_tfp[i, 0]), 2), round(float(_tfp[i, 1]), 2),
                                              round(float(_tfp[i, 2]), 2), round(float(_tfjn[i]), 4)]
                                             for i in range(len(_tfp))]
                            print(f"  STEP3 thermal FIELD: {len(thermal_field):,} pts (|k∇T| cloud)")
                        if _th['k_eff_W_mK'] is not None:
                            print(f"  STEP3 κ_eff = {_th['k_eff_W_mK']} W/m·K  (多상 열전도, vox {a.step3_vox}µm, "
                                  f"resid {_th['cg_resid']})")
                        elif _th.get('reason'):
                            # 물리적으로 풀 수 없는 것 = **정상 결과**.  실패와 구분되게 기록한다.
                            print(f"  ⚠ STEP3 thermal not solvable: {_th['reason']}")
                            step3['thermal'] = {
                                'k_eff_W_mK': None,
                                'status': _s3mark('thermal', 'not_solvable',
                                                  _th['reason'])['status'],
                                'reason': _th['reason'],
                                'trust': '열망이 형성되지 않아 k_eff 가 정의되지 않는다 — '
                                         '솔버 실패가 아니라 **구조의 답**이다.'}
                    except (Exception, SystemExit) as _e_th:
                        # ★ 2026-08-11: 옛 코드는 print 만 하고 `step3['thermal']` 을 **아예
                        #   안 남겼다**.  그러면 downstream 에서 "열망이 안 풀리는 구조"(정상)와
                        #   "솔버가 죽었다"(실패)가 **똑같이 키 없음**으로 보인다 — DEM 접촉망
                        #   솔버에서 같은 결함(RC5-03)을 고치다가 여기도 같은 모양인 것을 찾았다.
                        #   §F1 정직 null 관례대로 **이유를 남긴 스텁**을 쓴다.
                        print(f"  ⚠ STEP3 thermal skip: {type(_e_th).__name__}: {_e_th}")
                        step3['thermal'] = {
                            'k_eff_W_mK': None,
                            'status': _s3mark('thermal', 'failed',
                                              f'{type(_e_th).__name__}: {_e_th}')['status'],
                            'reason': f'{type(_e_th).__name__}: {_e_th}',
                            'trust': 'solver 예외로 미산출 — 열망 미형성(정상)과 구분되는 **실패**다. '
                                     '재실행으로 해소될 수 있다.'}
                # ★#30 — carbon(VGCF3/SuperP4/SWCNT8)↔SE(6) 3상 계면 면적 (kim2024 Fig3b: SE 분해 촉매면).
                #   STEP5 VGCF-촉매 화학열화(b1_chem_fade carbon_se_area)의 구조 입력.  carbon 있을 때만 기록.
                try:
                    _csa = _s3.carbon_se_contact_area(sid3, a.step3_vox, periodic_xy=bool(a.periodic))
                    if _csa > 0:
                        step3['carbon_se_area_um2'] = float(f"{_csa:.4g}")
                        print(f"  STEP3 carbon–SE 계면 {step3['carbon_se_area_um2']} µm² "
                              f"(VGCF-촉매 SE분해 화학열화 STEP5 입력)")
                except Exception as _e_csa:
                    print(f"  ⚠ carbon–SE area skip: {type(_e_csa).__name__}")
                # ★ A6 — PORE-phase effective-diffusion τ (DiffuDict/TauFactor 규약, #281/#286 축):
                # 같은 격자에서 void상 σ=1 Laplace → D_eff/D0, τ = ε_total/D_rel.  STRUCTURAL
                # descriptor (frame[4] cross-check) — ASSB Li⁺ 수송은 SE 접촉망(σ_ion 위)이 담당,
                # 이 τ를 수송 폼/PyBaMM τ에 대입 금지 (audit #2 이중계산 함정).  PTFE는 e/ion
                # 격자에 미스탬프(양쪽 절연) → 여기서 solid로 스탬프해 기공 과대계상 방지.
                if a.no_pore:
                    #  ★ 2026-08-18 — vox ≤ 0.125 에서 pore-τ 는 **인용 금지**(DR3-07)이고 실제로
                    #    터졌다 (τ 1,415 @0.15 → 4.97e9 @0.125, closed-from-top 28.5 → 99.2 %).
                    #    쓸 수 없는 값을 위해 300 s 와 10 GB 를 쓸 이유가 없다.  상태는 남긴다.
                    _s3mark('pore', 'disabled', '--no-pore (σ_e 전용 스윕; DR3-07 로 vox ≤ 0.125 '
                                                'pore-τ 는 어차피 인용 금지)')
                    _s3mark('pnm', 'disabled', '--no-pore (σ_e 전용 스윕)')
                    print('  STEP3: --no-pore — pore-τ·PNM 건너뜀 (σ_e 전용)', flush=True)
                try:
                    if a.no_pore:
                        raise _SkipRequested('--no-pore')
                    _t6 = _time.time()
                    _ppts = ((se[phase == 4] - _off) * UM
                             if (phase is not None and (phase == 4).any()) else None)
                    _rp = _s3.pore_tau(sid3, a.step3_vox, z_top_um=_zt3, extra_solid_pts=_ppts,
                                       periodic_xy=a.periodic)
                    # ⚠ eps_connected_pct 는 either-plate 규약이다 (Codex #2) — 관통 공극률로
                    #   읽히지 않도록 basis 와 eps_through_pct 를 **함께** 실어 보낸다.
                    step3['pore'] = {k: _rp[k] for k in ('eps_total_pct', 'eps_connected_pct',
                                                         'eps_connected_basis', 'eps_through_pct',
                                                         'D_rel', 'tau', 'n_dof',
                                                         'n_plate_reachable_dof', 'n_through_dof')
                                     if k in _rp}
                    _s3mark('pore', 'not_solvable' if _rp.get('reason') else 'complete',
                            _rp.get('reason', ''))
                    if _rp.get('reason'):
                        step3['pore']['reason'] = _rp['reason']
                    step3['pore']['resid'] = float(f"{_rp['resid']:.2g}")
                    step3['pore']['trust'] = ('STRUCTURAL pore-diffusion τ (D_eff/D0 = ε/τ, TauFactor '
                                              '규약, ε_total 기준; 닫힌 기공은 τ를 올림) — SE-망 '
                                              'σ_ionic과 별개 축, 수송 폼 대입 금지; PTFE solid-stamped; '
                                              'grid cropped to z ≤ thickness'
                                              + (' ⚠UNCONVERGED' if _rp.get('unconverged') else ''))
                    # ★ A13 — pore-PNM 위상지표 (nearest-seed 분할; τ와 같은 crop/PTFE-stamp 규약).
                    #   실패해도 pore-τ 결과는 유지 (내부 try).
                    try:
                        _pnm = _s3.pore_pnm(sid3, a.step3_vox, z_top_um=_zt3, extra_solid_pts=_ppts,
                                        periodic_xy=bool(a.periodic))
                        _s3mark('pnm', 'complete')
                        step3['pore']['pnm'] = _pnm
                        if not _pnm.get('reason'):
                            print(f"  STEP3 pore-PNM: {_pnm['n_pores']} bodies · r_eq med "
                                  f"{(_pnm.get('r_eq_um') or {}).get('med')}µm · CN med "
                                  f"{(_pnm.get('pore_cn') or {}).get('med')} · throats {_pnm['n_throats']}"
                                  f" · closed-from-top {_pnm['closed_from_top_pct']}%")
                    except Exception as _e7:
                        print(f'  ⚠ pore-PNM skipped ({type(_e7).__name__}: {_e7}) — pore-τ 결과는 유지')
                    print(f"  STEP3 pore-τ: ε_tot {step3['pore'].get('eps_total_pct')}% (conn "
                          f"{step3['pore'].get('eps_connected_pct')}%) · D_rel {step3['pore'].get('D_rel')}"
                          f" · τ {step3['pore'].get('tau')}"
                          + (f"  ⚠{_rp['reason']}" if _rp.get('reason') else '')
                          + f"  ({_time.time()-_t6:.0f}s)")
                except _SkipRequested:                       # 사용자가 끈 것 — 실패로 적지 않는다
                    pass
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
                                                     _gct, z_top_um=_zt3, z_bot_um=_zb3, periodic_xy=a.periodic)
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
                    # ★ T1-a CONTRACT 기계 필드 — **온도를 선언한 런에만** 실어 기본 그리드의 키
                    #   집합을 이전과 동일하게 유지한다 (없으면 소비자가 provenance.T_C 로 폴백).
                    _tkw = ({} if a.temp_c is None
                            else {'grid_temp_c': np.float64(float(a.temp_c))})
                    # ★periodic_xy 를 계약에 포함 (2026-07-27 감사 C1): STEP3 는 --periodic 시
                    #   x,y wrap 을 전도·BV 에 함께 걸지만 STEP4-v2 는 npz 에 이 정보가 없어
                    #   **항상 절연벽**으로 풀었다 (실격자서 i-망 wrap 면 30,895 · seam BV 11,543 누락).
                    np.savez_compressed(a.save_step4_grid, sid=sid3.astype(np.int8),
                                        pid=pid3.astype(np.int32), vox_um=a.step3_vox,
                                        z_top_um=_zt3, sig_e_S_cm=_sig3, sig_i_S_cm=_sig3i,
                                        # ★ 격자 좌표계 값 — origin 이동 시 sid3 와 같은 계다.
                                        origin_shift_um=np.asarray(_osh, np.float64),
                                        am_r_um=np.asarray(r, np.float64) * UM,
                                        periodic_xy=np.array(bool(getattr(a, 'periodic', False))),
                                        # ★ T1-a CONTRACT: STEP4-v2 reads sig_i from THIS npz, so the
                                        # grid MUST carry the temperature its σ were built at.
                                        #   temperature_provenance = the full se_material record (JSON;
                                        #     plain unicode array → allow_pickle=False safe).  ALWAYS
                                        #     written; T_C=None ⇒ σ_ion is the T_ref 25 °C value.
                                        #   grid_temp_c (**_tkw) = redundant machine field, present only
                                        #     when --temp-c was given (keeps the default key set intact).
                                        # step4_dyn CROSS-CHECKS this against its own --temp-k and
                                        # hard-blocks a mixed-temperature run (T1-d/G-1) — dropping this
                                        # provenance is what let σ@45 °C meet kinetics@25 °C silently.
                                        temperature_provenance=np.array(json.dumps(_temp_prov)),
                                        **_tkw)
                    a._s4grid_saved = True           # end-of-main 알림용 (stale 파일 오탐 방지, 리뷰 R2#6)
                    print(f'  STEP4-v2 grid → {a.save_step4_grid}  (sid {sid3.shape}, '
                          f'n_am {len(r)}, vox {a.step3_vox}µm)')
        except Exception as _e:
            import traceback as _tb
            print(f'  ⚠ STEP3 skipped ({type(_e).__name__}: {_e})')
            print('    ' + _tb.format_exc(limit=2).strip().replace(chr(10), chr(10) + '    '))
            # ★ RC6-06: 옛 코드는 print 만 하고 payload 에 아무 흔적도 남기지 않아,
            #   step3 가 통째로 없는 것이 "안 돌렸다" 인지 "죽었다" 인지 구분 불가였다.
            _s3mark('_step3', 'failed', f'{type(_e).__name__}: {_e}')
            if not isinstance(step3, dict):
                step3 = {}
            step3['status'] = 'failed'
            step3['reason'] = f'{type(_e).__name__}: {_e}'
    # ── ★ RC6-06: STEP3 manifest 를 payload 에 박는다 (배선 — 구현만으론 안 된다) ──
    #    component 가 하나도 없으면 STEP3 를 아예 안 돌린 것(disabled)이고, 있으면
    #    complete/partial/failed 를 상태들로 판정한다.  키 부재가 무엇을 뜻하는지
    #    downstream 이 **추측하지 않아도** 되게 만드는 것이 이 manifest 의 목적이다.
    if isinstance(step3, dict):
        # ★ RC7-01: 표시되지 않은 기대 component 를 **missing 으로 채운 뒤** 판정한다.
        #   (STEP3 를 아예 안 돌린 경우 = _s3st 가 비어 있음 → disabled 로 남긴다.
        #    STEP3 는 돌았는데 일부가 표시조차 안 된 경우만 missing 이다.)
        if _s3st:
            for _c in STEP3_EXPECTED:
                _s3st.setdefault(_c, {'status': 'missing',
                                      'reason': '이 실행에서 상태 표시가 없었다 '
                                                '(코드 경로가 건너뛰었거나 표시 누락)'})
        _sts = {c: v['status'] for c, v in _s3st.items()}
        if not _sts:
            _top = 'disabled'
        elif _sts.get('_step3') == 'failed':
            _top = 'failed'
        elif 'failed' in _sts.values() or 'missing' in _sts.values():
            _top = 'partial'
        elif all(v == 'complete' for v in _sts.values()):
            _top = 'complete'
        else:
            _top = 'partial'
        step3['manifest'] = {
            'schema_version': 2,          # 1→2: missing 채움 + component 별 backend
            'status': _top, 'components': dict(_s3st),
            'expected': list(STEP3_EXPECTED),
            'missing': sorted(c for c, v in _sts.items() if v == 'missing'),
            'failed': sorted(c for c, v in _sts.items() if v == 'failed'),
            # ★ RC6-08: 요청한 backend 와 **실제로 쓴** backend.  CuPy 부재로
            #   CPU 로 떨어져도 결과는 정상 수치라 로그 없이는 구분 불가였다.
            # ★ RC7-05: 이 전역 필드는 **마지막 solve** 만 담는다 → component 별
            #   `components[c]['backend']` 가 정본이고 여기는 하위호환 요약이다.
            # ★ 2026-08-12: 이 필드는 **실제로 적용된** 규약이다 (요청값이 아니다).
            #   실사고 — amonly 런이 --fibre 로드 실패로 점-스탬프로 내려앉았는데도 도장은
            #   `segment` 였다 (요청값을 적고 있었다).  `sr01_stamp_compare --check-arm` 이
            #   이 필드로 팔을 검증하므로, 조용히 강등된 런이 검사를 통과했다.
            #   ⇒ 기록은 **일어난 일**을 적는다.  요청값은 별 필드로 보존.
            'fibre_stamp': ('segment' if _afid is not None else 'point'),
            'fibre_stamp_requested': a.step3_fibre_stamp,
            'fibre_stamp_applied': bool(_afid is not None),
            # ★ origin 앙상블 (prereg sdcp_gain_prereg_20260816 §4) — **일어난 일**을 적는다.
            #   앙상블 팔을 나중에 대조하려면 각 payload 가 자기 위상을 알고 있어야 한다.
            'origin_shift_um': [float(x) for x in _osh],
            #  ★★ 2026-08-24 (CDXR2-6) — PTFE 규약을 **고정 인자로** 기록한다.  안 적으면
            #    exact-zero 팔과 1e-16 팔과 미스탬프 팔이 섞여도 게이트가 못 잡는다 (H5 와 같은 실수).
            'ptfe_stamp': a._ptfe_stamp,
            'ptfe_stamp_requested': (a.ptfe_stamp or 'legacy-unversioned'),
            #  σ=0 으로 찍혔나 = 그 셀이 dof 에서 빠졌나 (1e-16 = 극저-σ dof 와 **다른 규약**)
            'ptfe_zero_dof': bool(a._ptfe_stamp != 'off' and float(a.sigma_ptfe or 0.0) == 0.0),
            'sdcp_stamp': ('sphere' if getattr(a, 'step3_sdcp_sphere_d', 0) > 0 else 'point'),
            'sdcp_sphere_d_um': float(getattr(a, 'step3_sdcp_sphere_d', 0.0)),
            # ★ 2026-08-18 (CL-43) — 진단 팔은 **매니페스트에 남아야** 한다.  안 그러면
            #   σ-치환 OFF 팔과 생산 팔이 섞여도 고정-인자 게이트가 못 잡는다 (H5 와 같은 실수).
            'sdcp_yield_to_vgcf': bool(getattr(a, 'step3_sdcp_yield_to_vgcf', False)),
            # ★★ 2026-08-18 (심층 리뷰 ① H5) — `bridge_um` 이 **매니페스트에 없었다**.
            #   그래서 `sdcp_gain_verdict.py:107` 의 고정-인자 게이트가 이 필드에 대해
            #   항상 None 을 보고 **한 번도 발화하지 않았다** = 가짜 보증.  prereg §5 가
            #   명시적으로 "브리지를 물리 단위로 못 박는다" 고 선언한 바로 그 인자다.
            #   (`_bru` 는 rasterize-only 원장(:944)에만 실려 있었다.)
            #  ★ 2026-08-20 — **실효값**을 적는다.  옛 판은 `--step3-bridge-um` 을 안 주면
            #    `None` 을 적었는데, 판정기의 missing 게이트는 "기록 없음 = 고정 확인 불가"로
            #    읽어 **기본 브리지로 돈 런이 전부 거짓 HOLD** 가 된다 ("기본값" 과 "미기록" 을
            #    구분 못 하는 것 = `backend` 사고와 같은 범주 혼동).
            #    rasterize 의 기본은 `1.2·vox` (`step3_sigma.py` `_ball(... 1.2*vox if bridge_um is None ...)`)
            #    이므로 그 값을 적으면 매니페스트가 **실제로 쓴 반경**을 말하게 된다.
            #  ★★ CDXIJ-10 ③ (2026-08-20) — **입력 artifact digest + code SHA**.
            #    "pair 간 σ_ion 만 바꿨다" 를 기계가 확인하려면 입력이 같다는 증거가 필요하다.
            #    경로·크기·mtime 은 증거가 아니다 (같은 이름으로 다른 침대를 놓을 수 있다).
            #    ⇒ 실제로 읽은 파일들의 내용 해시를 정렬해 하나로 접는다.
            'input_digest': _in_dig,
            'input_files': _in_files,
            'code_sha': _code_sha(_os.path.dirname(_os.path.abspath(__file__))),
            #  ★★★ 2026-08-25 (자체발견, R3-F2 검증 중) — **`vox_um` 이 매니페스트에 없었다.**
            #    `PROTOCOL_FIELDS` 는 그것을 요구하는데 producer 가 안 써서 `physics_protocol_id`
            #    가 **모든 런에서 `unknown:vox_um`** 이 됐다.  팔끼리는 그 상수로 일치하므로
            #    게이트는 초록이고, 규약이 실제로 갈려도 못 잡는다 = H5·backend 와 같은 부류의
            #    **가짜 보증**.  ⇒ 값을 적고, 규칙 J 가 `unknown:` 접두사를 **거부**하게 한다
            #    (그것이 이 부류의 유일한 실물 증인이다 — 손수 만든 매니페스트는 증명 못 한다).
            'vox_um': float(a.step3_vox),
            #  ★★ 2026-08-25 (Codex 재리뷰 조건 4) — 규약 축 둘 + 감사 축 둘.
            'periodic_xy': bool(a.periodic),
            'plate_rule': str(getattr(_s3, 'PLATE_RULE_VERSION', 'unknown')),
            #  ★ **component 계획** — 무엇을 돌리기로 했는가 (요청).  이것이 없으면
            #    `disabled` 가 "의도적으로 껐다" 인지 "조용히 죽었다" 인지 구분할 근거가
            #    매니페스트 안에 없다 (M-R3-03 이 정확히 그 혼동이었다).
            'component_plan': {'electronic': True,
                               'ionic': not bool(a.no_ion),
                               'thermal': not bool(a.no_thermal),
                               'pore': not bool(a.no_pore),
                               'collector': not bool(a.no_collector)},
            #  ★ **관측 sid7 수** — PTFE 가 격자에 **실제로 몇 셀** 찍혔는가.
            #    `ptfe_stamp='centerline'` 이라고 적혀 있어도 0 셀이면 아무 일도 안 났다
            #    (스탬프 도장과 실제 효과를 가르는 유일한 증거).
            'ptfe_cells_observed': int((sid3 == 7).sum()) if sid3 is not None else None,
            'bridge_um': float(_bru) if _bru is not None else 1.2 * float(a.step3_vox),
            'bridge_um_explicit': _bru is not None,   # 고정 지시였나 vs 기본값이었나 (구분 보존)
            'sigma_vgcf_S_cm': float(getattr(a, 'sigma_vgcf', 0.0) or 0.0),
            'sigma_sdcp_S_cm': float(getattr(a, 'sigma_sdcp', 0.0) or 0.0),
            # ★ 2026-08-18 (CL-49) — PTFE 스탬프 팔도 고정 인자다.  0 = 생산(미스탬프),
            #   > 0 = 진단 팔(phase-4 를 격자에 찍어 탄소망을 끊는다).  기록 없으면 게이트가
            #   못 잡는다 (H5 와 같은 실수 방지).
            'sigma_ptfe_S_cm': float(getattr(a, 'sigma_ptfe', 0.0) or 0.0),
            # ★★ 2026-08-19 (코팅·도핑 리뷰 A5) — **σ_ion 축과 침대 세대가 게이트 밖에 있었다.**
            #   ⓐ `sigma_ion_table_S_cm`(:1397) 은 매니페스트 **밖**이라 `sdcp_gain_verdict._read`
            #      가 못 보고, 게다가 `if _res3i['n_dof']:` 안이라 **`--no-ion`(LEAN=2 = 현행
            #      스윕의 기본 모드)에서는 아예 기록되지 않는다**.  ⇒ 도핑 팔과 생산 팔이 한
            #      디렉터리에 섞여도 고정-인자 게이트가 통과시킨다 (CL-43/CL-49 에서 두 번 고친
            #      no-op 이 σ_ion 축에 그대로 남아 있었다).
            #   ⓑ `sigma_table_S_cm`(:1084)·`cam_preset`(:1092) 도 매니페스트 **밖** = 미게이트인데
            #      σ_AM 은 σ_e 솔브에 **직접** 들어간다.
            #   ⓒ SE 본체의 압밀 물성(E/ν/σ_y)과 seed 는 어디에도 안 찍혔다.  도펀트가 이걸
            #      바꾼다고 판단해 건드리면 **침대가 새 세대**가 되는데 탐지 장치가 없다
            #      (= CL-42 ADD_E_SET 사고의 SE 축 재현 경로).
            #   ⇒ 셋 다 **일어난 일**로 여기 남긴다.  `--no-ion` 여부와 **무관하게** 기록한다
            #     (기록 비용은 0 이고, 안 찍히는 것이 바로 위 ⓐ 의 원인이었다).
            #  ⚠⚠ 2026-08-19 실사고 — 여기를 `float(a.temp_c)` 로 썼다가 **런이 죽었다**.
            #    `--temp-c` 의 기본은 **None 이고 그것이 의미 있는 값**이다 (온도 기능 OFF =
            #    과거 출력과 비트 동일, `se_material.scale_sigma_ion:123`).  None 을 float 로
            #    감싸면 TypeError 다.  더 나쁜 것은 죽는 **자리**였다 — σ_e 솔브(2,474 s)가
            #    끝난 **뒤** 매니페스트를 쓰다가 죽어서 GPU 시간을 통째로 버렸다.
            #    ⇒ 기록 필드는 **절대 계산을 죽이면 안 된다**.  전부 None-안전으로.
            'sigma_ion_se_S_cm': _mflt(a.sigma_ion_se),          # T-스케일링 **적용 후** = 실제 쓴 값
            'sigma_ion_se_ref_S_cm': _mflt(getattr(a, '_sigma_ion_se_ref', a.sigma_ion_se)),
            'sigma_ion_sdcp_S_cm': _mflt(a.sigma_ion_sdcp),
            'sigma_am_s_S_cm': _mflt(a.sigma_am_s),
            'sigma_am_p_S_cm': _mflt(a.sigma_am_p),
            'cam': (None if a.cam is None else str(a.cam)),
            'temp_c': _mflt(a.temp_c),                            # ★ None = 온도 기능 OFF (유효값)
            'ea_ion_ev': _mflt(a.ea_ion_ev),
            'mpm_seed': _mint(sim_m.get('seed')),
            'se_E_GPa': _mflt(sim_m.get('E_SE_GPa')),
            'se_nu': _mflt(sim_m.get('nu_SE')),
            'se_sigma_y_GPa': _mflt(sim_m.get('sigma_y_GPa')),
            #  ★ 2026-08-19 (fable 리뷰 ② F4) — **첨가제 E 세대**.  CL-56 이 확인한 축
            #    (SDCP E 23.6 → 9.0, ADD_E_SET)이 매니페스트·게이트 어디에도 없어서
            #    E=9.0 팔과 23.6 팔이 섞여도 판정기가 원리적으로 못 잡았다.
            #    mpm_metrics['additives'] = {이름: {'E_GPa':…, 'E_anchor':…}, …} 를
            #    {이름: E} 평탄 dict 로 요약해 싣는다 (None-안전 — 계산을 죽이지 않는다).
            'additive_E_GPa': ({k: _mflt((v or {}).get('E_GPa'))
                                for k, v in sim_m['additives'].items()}
                               if isinstance(sim_m.get('additives'), dict) else None),
            'plate_z_grid_um': ([float(_zb3), float(_zt3)]
                                if (_zb3 is not None and _zt3 is not None) else None),
            # ★ 시각화 의존성이 없어 메쉬가 빠졌으면 **기록**한다 (조용한 강등 금지).
            'mesh_unavailable': getattr(_vc(), 'MESH_UNAVAILABLE_REASON', None),
            'backend_last_solve': dict(getattr(_s3, 'LAST_BACKEND', {}) or {}),
            'backend': dict(getattr(_s3, 'LAST_BACKEND', {}) or {}),   # 하위호환 별칭
        }
        #  ★★★ 2026-08-25 (CDXR3-3, 종료조건 ③④) — **물리 규약 정체성**.
        #    `schema_version` 은 파일 **구조**, 이것은 **물리 의미**다.  적용된 값에서
        #    파생하므로 자유 입력 라벨이 아니라 **결과**다 (Codex: "디렉터리 태그와 선언
        #    enum 은 검증 근거가 아니라 결과여야 한다").
        step3['manifest']['physics_protocol_id'] = physics_protocol_id(step3['manifest'])
        #  ★ 요청↔적용 불일치를 **기계가 읽게** 남긴다.  러너가 `--ptfe-stamp centerline`
        #    을 줬는데 payload 가 `off` 로 돌아도, 팔끼리만 같으면 옛 게이트는 통과했다.
        if getattr(a, '_protocol_expect', ''):
            step3['manifest']['physics_protocol_expected'] = a._protocol_expect
            step3['manifest']['physics_protocol_match'] = bool(
                a._protocol_expect == step3['manifest']['physics_protocol_id'])
    elif _s3st:
        step3 = {'manifest': {'schema_version': 2, 'status': 'failed',
                              'components': dict(_s3st),
                              'expected': list(STEP3_EXPECTED)}}

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
        for code, nm in ((2, 'VGCF'), (3, 'SuperP'), (4, 'PTFE'), (5, 'SDCP'), (6, 'SWCNT')):
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
        #  ★ 2026-08-24 (CDXR2-2) — 위에서 **이미 읽고 검증한** 배열을 쓴다.  옛 판은
        #    여기서 다시 `np.load` 하고 길이 불일치를 여기서만 잡았다 (솔브 뒤라 늦었다).
        dia = _dia_all
        if len(fid) != len(se):
            print(f'  ⚠ fibre length {len(fid)} != SE {len(se)} — ignoring --fibre')
        else:
            fib_mask = np.isin(phase, _s3.POLYLINE_PHASES) & (fid >= 0)   # ★ step3 와 **단일 소스**
        #   (2026-08-12: 같은 판별이 step3 `_fibre_segment_ijk` 에 없어 SDCP/SuperP-thinky 의
        #    coat id 가 폴리라인으로 구워질 뻔했다 — 셀 ×12.9, 87 % 가 AM 내부.)
        #   rod/chain phases — coat ids (SuperP-thinky/SDCP shells) are
            #   NOT polylines; SWCNT(6) sheath chains ARE (fid=chain, along-chain order preserved by the stable sort below)
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
    if phase is not None and np.isin(phase, (2, 3, 4, 5, 6)).any():
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
            for _ph, _nm in ((2, 'VGCF'), (3, 'SuperP'), (4, 'PTFE'), (5, 'SDCP'), (6, 'SWCNT')):
                if (phase == _ph).any():
                    additive_dispersion[_nm] = _dm((se[phase == _ph] - _offd) * UM, (lat, lat),
                                                   _ztd, matrix_pts_um=_mx, **_amck)
            # ★SWCNT(6) 포함 — σ_e 100 S/cm(VGCF급) 도체다 (A14 sheath).  PTFE(4)만 절연으로 제외.
            #   2026-07-27 감사: 6 이 빠져 SWCNT 베드의 conductive_all 이 과소계상됐음.
            _mc = np.isin(phase, (2, 3, 5, 6))               # conductive network union (PTFE 제외)
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
        'se_morph_points': se_morph_points,                # [x,y,z] µm — viewer "2D 단면 morphology" mode (#4b, SE void-filling)
        'mesh_triangles': tris,                            # COMPACTED SE plastic continuum (default)
        'seed_mesh_triangles': seed_tris,                  # loose SE before compaction (before/after)
        'additive_points': additive_points,                # [x,y,z,phase] µm — VGCF(2)/SuperP(3)/PTFE(4)
        'additive_fibres': additive_fibres,                # [{phase, pts:[[x,y,z],…]}] — VGCF/PTFE as polylines
        'electronic_field': elec_field,                    # [x,y,z,|J|₀₋₁] µm — STEP3 e⁻ current-density cloud (AM+carbon)
        'ionic_field': ion_field,                          # [x,y,z,|J|₀₋₁] µm — STEP3 Li⁺ current-density cloud (SE+SDCP)
        'thermal_field': thermal_field,                    # [x,y,z,|k∇T|₀₋₁] µm — STEP3 열류 cloud (多상, 열 hot-spot)
        'joule_field': joule_field,                        # [x,y,z,q₀₋₁] µm — #29 STEP3 Joule 발열밀도 hot-spot (--joule-heat)
        'void_points': void_points,                        # [x,y,z] µm — pore voxel centres (XCT "기공만" mode)
        'box': {'x_min': 0.0, 'x_max': round(lat, 2), 'y_min': 0.0, 'y_max': round(lat, 2),
                'z_min': 0.0, 'z_max': round(thick, 2)},
        'atoms_only': False,
        # ★ T1-a — top-level so ANY consumer of this payload (viewer, kit zip, STEP4 grid,
        # ML feature builder) can tell what temperature convention the σ inside were solved at.
        # On a legacy run this reads T_dependence=NOT_MODELLED, i.e. "σ is the 25 °C value".
        'temperature_provenance': dict(_temp_prov),
        'mpm_metrics': mpm_metrics,
        'mpm_source': {'se': a.se or 'proxy', 'scaffold': a.scaffold, 'metrics_json': a.metrics_json,
                       'target_porosity': a.target_porosity, 'target_coverage': a.target_coverage,
                       'smooth': a.smooth},
    }
    # ── ★ RC7-01 (Codex 7회차): bare NaN 벨트 ─────────────────────────────────
    #   이 파일은 곳곳에서 `np.nan_to_num(...)` 으로 NaN 을 막아왔지만 그것은 **ad-hoc**
    #   이고, 한 군데라도 빠지면 `json.dump` 의 기본 allow_nan=True 가 RFC 8259 에 없는
    #   `NaN` / `Infinity` **토큰을 그대로 쓴다** → 브라우저 `JSON.parse` 가 payload 전체를
    #   거부한다 (수 분짜리 STEP3 결과가 통째로 못 읽히는 형태의 실패).
    #   ⇒ 쓰기 직전에 **한 번** 전수 검사한다.  단 조용히 고치면 안 되므로 (그것이 이
    #     리뷰가 계속 잡아온 실패 양식이다) 바꾼 자리를 **경로째 payload 에 기록**한다.
    payload, _nonfinite = finite_belt(payload)
    if _nonfinite:
        payload['nonfinite_sanitized'] = {'count': len(_nonfinite),
                                          'paths': _nonfinite[:50],
                                          'note': 'NaN/Inf → null 로 치환 (bare NaN 은 JSON 이 아님). '
                                                  '값이 null 인 자리는 계산이 안 된 것으로 읽을 것.'}
        print(f'  ⚠ 비유한값 {len(_nonfinite)}개를 null 로 치환했다 (payload.nonfinite_sanitized 참조): '
              + ', '.join(_nonfinite[:5]) + (' …' if len(_nonfinite) > 5 else ''), flush=True)
    #  ★★ 2026-08-25 (CDXR3-2) — **원자적 쓰기**.  옛 판은 최종 파일명에 직접 썼다.
    #    중간에 죽으면 **반쯤 쓰인 JSON 이 성공 경로의 이름**으로 남고, 러너의
    #    `[ -s "$OUT" ]` 캐시가 그것을 재사용한다.  `.part` → fsync → rename 으로 막는다.
    _part = a.out + '.part'
    with open(_part, 'w') as fh:
        json.dump(payload, fh, allow_nan=False)   # 벨트 뒤이므로 남아 있으면 **터뜨린다**
        fh.flush()
        import os as _os_w
        _os_w.fsync(fh.fileno())
    import os as _os_w2
    #  ★★★ 2026-08-25 (R3-F2, Codex 재리뷰) — **semantic validation 을 게시보다 먼저.**
    #    초판은 `.part → fsync → replace` 를 했지만 replace 가 exit-3/exit-4 검사보다
    #    **앞**이라, 의미적으로 실패한 payload 가 성공 파일명에 먼저 나타났다 (러너의
    #    `[ -s "$OUT" ]` 캐시가 그것을 재사용한다).  ⇒ 판정을 여기서 끝내고, 실패면
    #    **최종 이름을 쓰지 않고** `.failed` 로 남긴다 (진단은 보존, 캐시는 오염 안 됨).
    _fail_reason = _payload_reject_reason(a, step3)
    if _fail_reason:
        _bad = a.out + '.failed'
        _os_w2.replace(_part, _bad)
        print(f'\n✗ {_fail_reason}', flush=True)
        print(f'  최종 파일명을 쓰지 않는다 — 진단본: {_bad}', flush=True)
        #  exit 3 = STEP3 required component · exit 4 = 물리 규약 불일치.
        #  ⚠ 사유 문자열이 아니라 **코드 접두사**로 가른다 (조건 7 — 러너가 짝짓는 축).
        raise SystemExit(3 if _fail_reason.startswith('STEP3_REQUIRED_INCOMPLETE') else 4)
    _os_w2.replace(_part, a.out)
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
