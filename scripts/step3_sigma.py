#!/usr/bin/env python3
"""STEP3 v1 — electronic-conductivity voxel resistor network for MPM additive structures.

Solves ∇·(σ∇φ)=0 on a voxelized conductive skeleton (AM + VGCF/SuperP/SDCP; SE·PTFE = e-insulators)
between the collector plane (bottom, φ=1) and the top plane (φ=0), finite-volume with HARMONIC-mean
face conductances (phase boundaries handled naturally), and reports:
  · sigma_e_eff  — effective through-plane electronic conductivity (S/cm)
  · per-AM-particle current density (slide-20 colouring: which AM carry the current)
  · per-phase current shares (how much flows through carbon vs AM–AM necks)

DESIGN / TRUST (docs/step3_sigma_network.md):
  · FULL-resolution inputs (se_dump + phase + AM scaffold) — the payload's subsampled clouds would
    fragment bridges (unphysical).  Runs on kgy inside the payload step (mpm_webapp_payload --step3).
  · v1 trust unit = RELATIVE comparison at identical settings (voxel res + σ hooks fixed).  Absolute
    σ_e needs the DEM Stage-E contact-area cross-calibration (sub-voxel constriction NOT modelled —
    a 1-voxel neck's area is quantized to the face area; documented limit).
  · Boundary: lateral walls insulating (Neumann).  The MPM RVE is x,y-periodic; v1 keeps Neumann for
    solver simplicity — identical for all compared runs, so the relative Δσ is unaffected to first
    order (documented).
  · σ table (S/cm), every value overridable:
      AM_S 0.010 / AM_P 0.005   ✅ A1-locked (Trevisanello 10/5 mS/cm)
      VGCF 100 · SuperP 10      ⚠ literature order-of-magnitude hooks (graphitic fibre / CB compact)
      SDCP 0.010                ⚠ 'AM-grade conductor' default (= the econn classification; the
                                  pellet ×5.1 anchor is COMPOSITE-level — do not paste onto a phase σ.
                                  --sigma-sdcp overrides; doped/neutral split = future refinement)
      SE · PTFE 0               (electronic insulators)

Analytic self-tests (python3 scripts/step3_sigma.py --selftest):
  uniform block → σ exactly; series laminate → harmonic mean; parallel laminate → arithmetic mean;
  disconnected slab → σ ≈ 0.  These pin the assembly/BC signs.
"""
import argparse
import sys

import numpy as np
from scipy import ndimage, sparse
from scipy.sparse.linalg import cg

# σ defaults (S/cm) — see module docstring for anchor status
# SDCP 250 = USER-provided anchor UPDATE (2026-07-16; supersedes interim 150 of 2026-07-10,
# 진성호계 S-PEDOT 자릿수).  Still overridable per run.  ⚠ pre-2026-07-16 production outputs
# (DBE +45.4% 등) were solved at 150 — re-run needed for the 250-anchored numbers.
SIGMA_DEFAULT = {'AM_S': 0.010, 'AM_P': 0.005, 'VGCF': 100.0, 'SuperP': 10.0, 'SDCP': 250.0,
                 'SWCNT': 100.0}
SID_NAME = {1: 'AM_S', 2: 'AM_P', 3: 'VGCF', 4: 'SuperP', 5: 'SDCP', 6: 'SE', 7: 'PTFE',
            8: 'SWCNT'}                                    # voxel σ-id → name
#   sid 7 (PTFE) = SENSITIVITY-ONLY: production은 PTFE를 전도 격자에 아예 안 넣음(절연 = void와
#   동일 취급, bulk PTFE σ~1e-16 S/cm).  --sigma-ptfe > 0 민감도 런에서만 payload가 phase-4 점을
#   _apts에 포함시켜 여기로 스탬프됨.
#   sid 8 (SWCNT, A14 sheath) = 전자망 도체 (σ_e VGCF급 ⚠hook — koo2026 0.20 S/cm은 분말-복합체
#   값이지 상(phase) σ가 아님, 이식 금지) + 이온망 기본 = SE-투명(σ_i=σ_ion_se): 실제 skin은
#   2-10nm sub-voxel이라 1-voxel(≈0.4µm) 스탬프가 이온접촉을 끊으면 차단을 40-200× 과대표현
#   (trade-off 상한의 이중계상).  --swcnt-ion-block = 상한 시나리오 opt-in(σ_i=0 → BV면 소멸).

# Set True (mpm_webapp_payload --step3-gpu) to run the Kirchhoff CG on GPU (CuPy cuSPARSE) — a
# multi-M-dof fine-vox solve drops from ~1 h (CPU) to minutes.  Auto-falls back to scipy CPU if
# CuPy/CUDA is unavailable, so it is always safe to leave on.
GPU_SOLVE = False


def _solve_cg(L, b):
    """Jacobi-preconditioned CG for the SPD Kirchhoff system L·φ = b.  GPU (CuPy) when GPU_SOLVE and
    the import succeeds, else scipy CPU — SAME matrix + tol (1e-8) → SAME φ (backend swap only).
    Returns (phi: np.ndarray, info: int)."""
    diag = L.diagonal()
    if GPU_SOLVE:
        try:
            import cupy as cp
            import cupyx.scipy.sparse as cxs
            from cupyx.scipy.sparse.linalg import cg as cg_gpu
            Lg = cxs.csr_matrix(L.astype(np.float64))
            bg = cp.asarray(b, dtype=np.float64)
            Mg = cxs.diags(1.0 / cp.asarray(diag))
            try:
                xg, info = cg_gpu(Lg, bg, tol=1e-8, maxiter=30000, M=Mg)
            except TypeError:                              # newer CuPy renamed tol → rtol/atol
                xg, info = cg_gpu(Lg, bg, rtol=1e-8, atol=0.0, maxiter=30000, M=Mg)
            return cp.asnumpy(xg), int(info)
        except Exception as _e:
            print(f'    STEP3 GPU solve unavailable ({type(_e).__name__}: {_e}) → CPU fallback', flush=True)
    Minv = sparse.diags(1.0 / diag)
    try:
        return cg(L, b, rtol=1e-8, maxiter=30000, M=Minv)
    except TypeError:                                      # scipy < 1.12 has no rtol kwarg
        return cg(L, b, tol=1e-8, maxiter=30000, M=Minv)


def rasterize(am_c, am_r, am_t, add_pts, add_phase, box_lo, box_hi, vox, tol_am_um=0.10, se_pts=None):
    """Voxel σ-id grid: 0 = non-conductive, 1 = AM_S, 2 = AM_P, 3.. = additives (2,3,5 → 3,4,5).
    Also returns per-voxel AM particle index (-1 = not AM) for per-particle currents.
    am_t: 1 = AM_P, 2 = AM_S (LIGGGHTS type convention).  All coords in one frame (µm).

    AM-AM CONTACT BRIDGES: a DEM contact's Hertz neck (a ≈ √(Rδ) ~ 0.3-0.5µm) is at/below the
    voxel size, so plain rasterization randomly DROPS touching contacts (6-neighbour faces need
    shared/adjacent voxels) — the integration test showed a non-percolating AM skeleton from
    quantization alone.  Fix = stamp a 1-voxel-radius bridge at the contact midpoint of every
    AM pair with gap ≤ tol_am_um (the SAME contact rule econn uses), σ-id of the SOFTER particle
    (series-conservative).  Neck AREA is thereby quantized to ~vox² — a documented v1 limit,
    identical across compared runs (relative trust preserved)."""
    lo = np.asarray(box_lo, np.float64)
    n = np.maximum(1, np.ceil((np.asarray(box_hi) - lo) / vox).astype(int))
    sid = np.zeros(tuple(n), np.int8)
    pid = np.full(tuple(n), -1, np.int32)
    # SE (sid 6, optional): stamped FIRST = lowest priority — AM / contact bridges / additives
    # overwrite.  Enables the IONIC solve (SE+SDCP conduct; AM/carbon/PTFE ion-block) on the SAME
    # grid: the electronic table just sets σ(SE)=0.  Chunked (tens of millions of points).
    if se_pts is not None and len(se_pts):
        for c0 in range(0, len(se_pts), 8_000_000):
            ijk = np.floor((np.asarray(se_pts[c0:c0 + 8_000_000], np.float64) - lo) / vox).astype(int)
            ok = ((ijk >= 0) & (ijk < n)).all(1)
            ijk = ijk[ok]
            sid[ijk[:, 0], ijk[:, 1], ijk[:, 2]] = 6

    def _ball(centre_um, rad_um, s, particle):
        c = (centre_um - lo) / vox; rr = rad_um / vox
        i0 = np.maximum(0, np.floor(c - rr).astype(int)); i1 = np.minimum(n - 1, np.ceil(c + rr).astype(int))
        if (i1 < i0).any():
            return
        gx, gy, gz = np.ogrid[i0[0]:i1[0] + 1, i0[1]:i1[1] + 1, i0[2]:i1[2] + 1]
        m = ((gx + 0.5 - c[0]) ** 2 + (gy + 0.5 - c[1]) ** 2 + (gz + 0.5 - c[2]) ** 2) <= rr * rr
        sub = sid[i0[0]:i1[0] + 1, i0[1]:i1[1] + 1, i0[2]:i1[2] + 1]
        sub[m] = s
        if particle >= 0:
            psub = pid[i0[0]:i1[0] + 1, i0[1]:i1[1] + 1, i0[2]:i1[2] + 1]
            psub[m] = particle

    for i in range(len(am_c)):                             # AM spheres (few hundred): ball masks
        _ball(am_c[i], am_r[i], 2 if am_t[i] == 1 else 1, i)   # type 1 = AM_P → sid 2; 2 = AM_S → sid 1
    # AM-AM contact bridges (econn contact rule: gap ≤ tol) — NO blanket except here: silently
    # losing every bridge = the fragmented-skeleton σ-collapse the integration test exists to catch
    if len(am_c) >= 2:
        from scipy.spatial import cKDTree
        tree = cKDTree(am_c)
        for i, j in tree.query_pairs(2.0 * float(am_r.max()) + tol_am_um):
            d = float(np.linalg.norm(am_c[i] - am_c[j]))
            if d <= am_r[i] + am_r[j] + tol_am_um:
                mid = am_c[i] + (am_c[j] - am_c[i]) * (am_r[i] + 0.5 * (d - am_r[i] - am_r[j])) / max(d, 1e-12)
                soft = i if am_t[i] == 1 else j            # the LOWER-σ particle = AM_P (0.005 < AM_S 0.010)
                s = 2 if (am_t[i] == 1 or am_t[j] == 1) else 1   # mixed / P-P → AM_P id (series-conservative);
                _ball(mid, 1.2 * vox, s, soft)             #   S-S stays AM_S.  (Review M2: was inverted.)
    # additive points: cell-stamp (carbon overwrites AM at shared cells — the higher-σ phase wins,
    # which is the physical series-shortcut at an anchored contact)
    if add_pts is not None and len(add_pts):
        ijk = np.floor((add_pts - lo) / vox).astype(int)
        ok = ((ijk >= 0) & (ijk < n)).all(1)
        ijk, ph = ijk[ok], add_phase[ok]
        for code, s in ((2, 3), (3, 4), (5, 5), (4, 7), (6, 8)):   # phase → sid (4=PTFE: sensitivity-
            m = ph == code                                  #   only; 6=SWCNT sheath A14 → sid 8)
            if m.any():
                sid[ijk[m, 0], ijk[m, 1], ijk[m, 2]] = s
    return sid, pid


def solve_sigma_z(sid, sigma_of_sid, vox, return_field=False, z_top_um=None, plate_band_um=None,
                  z_bot_um=None, plate_band_bot_um=None, bot_allowed=None, periodic_xy=False):
    """Effective through-plane (z) σ of the voxel σ-id grid.  Finite volume, harmonic-mean face
    conductance g = (2σaσb/(σa+σb))·vox (cubic voxels: face area vox² / distance vox), collector
    plate φ=1 at the bed bottom, φ=0 plate at the bed top, lateral Neumann.

    PLATES = BAND-COUPLED CONTACT SETS (physics review F1): every conductive voxel whose centre
    lies within `band` of its plate PLANE couples with the distance-aware conductance
    g = σ·vox²/max(dist, vox/2).  A single-quantization-layer plate made σ swing ×7.7 under a
    ±0.2µm sub-voxel bed shift (2-4 AM crowns = the whole exit) — the band (default vox+0.1µm,
    capped 1.4·vox: the 0.1µm is the econn contact tol) makes the plate contact set the PHYSICAL
    crown-contact set, restoring cross-scaffold relative trust.  Top plane = z_top_um (bed
    thickness, production) else the top face of the highest AM layer; bottom plane = floor of the
    lowest occupied layer.  σ_eff uses the true plate gap L = z_plate − z_b.
    Returns dict(sigma_eff, n_dof, plate_z_um, n_plate_vox, cg_info, resid, unconverged
    [, phi, cond])."""
    nx, ny, nz = sid.shape
    sig = sigma_of_sid[sid]                                # per-voxel σ (S/cm)
    cond = sig > 0
    if not cond.any():
        return {'sigma_eff': 0.0, 'n_dof': 0, 'n_floating_dropped': 0, 'cg_info': 0, 'resid': 0.0,
                'unconverged': False, 'reason': 'no_conductive_voxels'}
    occ = np.where(cond.any((0, 1)))[0]
    k_bot = int(occ[0])
    am_occ = np.where((((sid == 1) | (sid == 2)) & cond).any((0, 1)))[0]
    k_top_ref = int(am_occ[-1]) if len(am_occ) else int(occ[-1])
    # plate PLANES in CONTINUOUS µm (not voxel-snapped): production passes z_bot=0 (collector)
    # and z_top=thickness — snapping to occupied layers re-introduced sub-voxel plate luck
    # (probe: ×2.8 residual swing) because the plane then hops with the rasterization phase.
    z_b = float(z_bot_um) if z_bot_um is not None else k_bot * vox
    z_plate = float(z_top_um) if z_top_um is not None else (k_top_ref + 1) * vox
    z_plate = min(z_plate, nz * vox)
    if z_plate - z_b <= 1.5 * vox:                         # degenerate (≈1-layer bed) → no through-path
        return {'sigma_eff': 0.0, 'n_dof': int(cond.sum()), 'n_floating_dropped': 0, 'cg_info': 0,
                'resid': 0.0, 'unconverged': False, 'reason': 'degenerate_thin_bed'}
    band = plate_band_um if plate_band_um is not None else (vox + 0.10)
    # BOTTOM band override (collector GEOMETRY axis): 'wetted/primer' = default band (vox+0.1 —
    # a conformal conductive film reaches ~0.2µm gaps, + quantization half-voxel); 'bare' passes a
    # TIGHTER band (0.5·vox+0.1 = true-contact crowns only) → fewer collector contacts → the exit
    # current funnels through crown contacts and the per-AM je map redistributes near the collector
    # (the primer-paper Fig-4d red-box story).  ±half-voxel quantization blur documented.
    band_bot = plate_band_bot_um if plate_band_bot_um is not None else band
    zc = (np.arange(nz) + 0.5) * vox                       # voxel-centre heights
    # PER-COLUMN SINGLE CONTACT (review F1, final form): each lateral column couples to a plate
    # through ONE voxel — its surface voxel — iff that surface is within `band` of the plane,
    # with distance-aware g.  A layer-band coupled a column through TWO layers whenever the band
    # edge crossed a voxel centre (probe: plate-voxel count 54→278 on a +0.1µm shift, σ ×2) —
    # per-column contact makes the plate set the physical crown patch and σ vary smoothly.
    any_c = cond.any(2)
    k_first = np.argmax(cond, axis=2)                      # column's lowest conductive voxel
    k_last = nz - 1 - np.argmax(cond[:, :, ::-1], axis=2)  # column's highest conductive voxel
    bot_m = any_c & (zc[k_first] - z_b <= band_bot)
    # ANALYTIC contact mask (v3, optional): [nx,ny] bool from EXACT sphere/point z (payload computes
    # it — gap ≤ 0.1µm bare / ≤ 0.3µm film-wetted).  Voxel-centre bands cannot resolve below
    # ~half-voxel; the analytic mask removes that blur — the SELECTION is exact, only the coupling
    # conductance stays voxel-scale.
    if bot_allowed is not None:
        bot_m &= np.asarray(bot_allowed, bool)
    top_m = any_c & (z_plate - zc[k_last] <= band)
    if not bot_m.any() or not top_m.any():
        return {'sigma_eff': 0.0, 'n_dof': int(cond.sum()), 'n_floating_dropped': 0, 'cg_info': 0,
                'resid': 0.0, 'unconverged': False,
                'reason': f'no_plate_contact(bot={int(bot_m.sum())},top={int(top_m.sum())},'
                          f'z_b={z_b:.2f},z_plate={z_plate:.2f},band={band:.2f})'}
    # FLOATING ISLANDS (components touching NEITHER plate contact) = singular blocks, zero current
    # by physics → dropped (their je reads 0).
    lab, _nl = ndimage.label(cond)                         # 6-connectivity = the face-coupling graph
    _ii, _jj = np.where(bot_m); _lb = lab[_ii, _jj, k_first[bot_m]]
    _ii, _jj = np.where(top_m); _lt = lab[_ii, _jj, k_last[top_m]]
    plate = np.unique(np.concatenate([_lb, _lt]))
    plate = plate[plate > 0]
    n_float = int(cond.sum())
    cond &= np.isin(lab, plate)
    n_float -= int(cond.sum())
    n_dof = int(cond.sum())
    if n_dof == 0:
        return {'sigma_eff': 0.0, 'n_dof': 0, 'n_floating_dropped': n_float, 'cg_info': 0,
                'resid': 0.0, 'unconverged': False, 'reason': 'all_floating_dropped'}
    sig = np.where(cond, sig, 0.0)
    idx = -np.ones(sid.shape, np.int64)
    idx[cond] = np.arange(n_dof)

    rows, cols, vals = [], [], []
    diag = np.zeros(n_dof, np.float64)
    b = np.zeros(n_dof, np.float64)

    def couple(sl_a, sl_b):
        A, B = idx[sl_a], idx[sl_b]
        sa, sb = sig[sl_a], sig[sl_b]
        m = (A >= 0) & (B >= 0)
        if not m.any():
            return
        g = (2.0 * sa[m] * sb[m] / (sa[m] + sb[m])) * vox   # σ[S/cm]·vox[µm] — unit cancels in σ_eff
        a2, b2 = A[m], B[m]
        rows.append(a2); cols.append(b2); vals.append(-g)
        rows.append(b2); cols.append(a2); vals.append(-g)
        np.add.at(diag, a2, g); np.add.at(diag, b2, g)

    couple(np.s_[:-1, :, :], np.s_[1:, :, :])
    couple(np.s_[:, :-1, :], np.s_[:, 1:, :])
    couple(np.s_[:, :, :-1], np.s_[:, :, 1:])
    if periodic_xy:                                        # ★x,y 주기 wrap (MPM RVE 'boundary p p f' 정합;
        if nx > 1:                                         #   z=plate 유지).  nx/ny=1이면 자기결합 방지 가드.
            couple(np.s_[-1:, :, :], np.s_[:1, :, :])      # x: nx-1 ↔ 0
        if ny > 1:
            couple(np.s_[:, -1:, :], np.s_[:, :1, :])      # y: ny-1 ↔ 0
    # per-column plate couplings, distance-aware: g = σ·vox²/max(dist, vox/2) (= 2σ·vox at half-cell)
    def _plate_couple(mask, ksurf, plane, phi_p):
        ii, jj = np.where(mask)
        kk2 = ksurf[mask]
        A = idx[ii, jj, kk2]; sa = sig[ii, jj, kk2]
        m = A >= 0
        if not m.any():
            return 0, None, None
        dist = np.maximum(np.abs(zc[kk2[m]] - plane), 0.5 * vox)
        g = sa[m] * vox * vox / dist
        np.add.at(diag, A[m], g)
        if phi_p != 0.0:
            np.add.at(b, A[m], g * phi_p)
        return int(m.sum()), A[m], g
    n_pb, _Ab, _gb = _plate_couple(bot_m, k_first, z_b, 1.0)
    n_pt, _At, _gt = _plate_couple(top_m, k_last, z_plate, 0.0)
    L = sparse.coo_matrix((np.concatenate(vals + [diag]),
                           (np.concatenate(rows + [np.arange(n_dof)]),
                            np.concatenate(cols + [np.arange(n_dof)]))),
                          shape=(n_dof, n_dof)).tocsr()
    print(f'    STEP3 solve: {n_dof:,} dof, plate contacts {n_pb:,}/{n_pt:,} — CG running '
          f'({"GPU" if GPU_SOLVE else "CPU"}, 수 분 소요 가능)…', flush=True)
    phi, info = _solve_cg(L, b)
    resid = float(np.linalg.norm(L @ phi - b) / max(np.linalg.norm(b), 1e-30))
    unconv = bool(info) or resid > 1e-6                    # review F2: NEVER ship a silent bad σ
    if unconv:
        print(f'  ⚠ STEP3 CG not converged (info={info}, resid={resid:.1e}) — σ UNRELIABLE')
    # total current through the bottom plate: I = Σ g_b·(1 − φ)
    I = float(np.sum(_gb * (1.0 - phi[_Ab]))) if _Ab is not None else 0.0
    # σ_eff = I·L/(A·ΔV): L = plate gap (µm), A = nx·ny·vox² → σ_eff in the σ-table unit (S/cm)
    sigma_eff = max(0.0, I * (z_plate - z_b) / (nx * ny * vox * vox))
    out = {'sigma_eff': float(sigma_eff), 'n_dof': n_dof, 'n_floating_dropped': n_float,
           'plate_z_um': (round(z_b, 3), round(z_plate, 3)), 'n_plate_vox': (n_pb, n_pt),
           'k_plates': (k_bot, k_top_ref), 'cg_info': int(info) if info else 0, 'resid': resid,
           'unconverged': unconv}
    if return_field:
        P = np.zeros(sid.shape, np.float64); P[cond] = phi
        out['phi'] = P; out['cond'] = cond
    return out


def per_particle_current(res, sid, pid, sigma_of_sid, n_am):
    """Mean |J_z| PROXY per AM particle (z-face current g·Δφ ∝ J_z·vox² — run-relative, the
    viewer percentile-normalizes; NOT vox-invariant across runs) — the slide-20 axis."""
    if 'phi' not in res:                                   # early-returned solve (see res['reason'])
        return np.zeros(n_am, np.float64)
    P, cond = res['phi'], res['cond']
    sig = sigma_of_sid[sid]
    jz = np.zeros(sid.shape, np.float64)
    sa, sb = sig[:, :, :-1], sig[:, :, 1:]
    both = cond[:, :, :-1] & cond[:, :, 1:]
    g = np.where(both, 2.0 * sa * sb / np.maximum(sa + sb, 1e-30), 0.0)
    dphi = P[:, :, :-1] - P[:, :, 1:]
    f = g * dphi                                           # face current ∝ σ·Δφ (per face area vox²)
    jz[:, :, :-1] += np.abs(f) * 0.5
    jz[:, :, 1:] += np.abs(f) * 0.5
    je = np.zeros(n_am, np.float64); nv = np.zeros(n_am, np.int64)
    m = pid >= 0
    np.add.at(je, pid[m], jz[m]); np.add.at(nv, pid[m], 1)
    return np.where(nv > 0, je / np.maximum(nv, 1), 0.0)


def phase_current_share(res, sid, sigma_of_sid):
    """Fraction of total dissipation per σ-id (where the current actually flows)."""
    if 'phi' not in res:
        return {}
    P, cond = res['phi'], res['cond']
    sig = sigma_of_sid[sid]
    diss = np.zeros(sid.shape, np.float64)
    for sl_a, sl_b in ((np.s_[:-1, :, :], np.s_[1:, :, :]), (np.s_[:, :-1, :], np.s_[:, 1:, :]),
                       (np.s_[:, :, :-1], np.s_[:, :, 1:])):
        both = cond[sl_a] & cond[sl_b]
        sa, sb = sig[sl_a], sig[sl_b]
        g = np.where(both, 2.0 * sa * sb / np.maximum(sa + sb, 1e-30), 0.0)
        d = g * (P[sl_a] - P[sl_b]) ** 2                   # per-face dissipation; split ∝ each side's
        wa = np.where(both, sb / np.maximum(sa + sb, 1e-30), 0.0)   # RESISTANCE (review F4 — the old
        diss[sl_a] += wa * d; diss[sl_b] += (1.0 - wa) * d          # half-half gave carbon 50% at a
        #   1e4-contrast face where it truly dissipates ~0.01%)
    tot = diss.sum()
    out = {}
    for s in np.unique(sid[sid > 0]):
        out[int(s)] = float(diss[sid == s].sum() / max(tot, 1e-30))
    return out


# ── STEP3 열전도 (σ_thermal) — 범용 Laplace 솔버(solve_sigma_z) 재사용, 多상 k 맵 ──────────────
# k 값 (W/cm·K; ×100 = W/m·K).  ★SE=문헌앵커(Ketter 2025 = LPSCl/SE 논문); AM=generic NCM 문헌-order
# (전용 인용 없음; network_conductivity.py의 uncited NCM 기본과 同값 — Ketter 아님[Ketter는 SE]),
# carbon/SDCP/PTFE/pore = ASSUMED order-of-mag (라벨 · 소체적분율이라 k_eff 영향 작음 · 스윕용).
K_AM_THERMAL = 4.0e-2    # NCM, ≈4 W/m·K  [generic NCM 문헌-order; 전용 인용 없음, NOT Ketter(=SE)]
K_SE_THERMAL = 0.7e-2    # LPSCl, ≈0.7 W/m·K  [lit: Ketter 2025 (LPSCl thermal)]
K_PTFE_THERMAL = 2.5e-3  # PTFE, ≈0.25 W/m·K  [polymer generic; 전용 인용 없음]
K_PORE_THERMAL = 0.0     # 압밀 ASSB 공극(Ar/진공, ~7% 고립) → 무시 [ASSUMED; 가스면 ~2.6e-4]


def thermal_k_table(k_am=K_AM_THERMAL, k_se=K_SE_THERMAL, k_carbon=None, k_sdcp=None,
                    k_ptfe=K_PTFE_THERMAL, k_pore=K_PORE_THERMAL):
    """sid-indexed 열전도 k 배열 (_sig3 電子표와 동일 레이아웃: 0=pore,1=AM_S,2=AM_P,3=VGCF,
    4=SuperP,5=SDCP,6=SE,7=PTFE,8=SWCNT).  ★열은 多상: σ_e(AM만)/σ_ion(SE만)과 달리 全상이 열
    통과 → SE(6)·PTFE(7)는 0 아님(pore는 기본 0=진공 가정).  carbon(VGCF/SuperP/SWCNT) 기본 =
    k_am(도체≥AM 보수적 ASSUMED, --k-carbon 상향 스윕 권장); SDCP 기본 = k_se.  반환 (k_array, prov)."""
    kc = k_am if k_carbon is None else float(k_carbon)
    ks = k_se if k_sdcp is None else float(k_sdcp)
    prov = {'AM(NCM)': f'{k_am*100:.1f} W/mK [generic NCM 문헌-order; 전용 인용 없음 — NOT Ketter(=LPSCl/SE); '
                       'network_conductivity.py uncited NCM 기본과 同값]',
            'SE(LPSCl)': f'{k_se*100:.2f} W/mK [lit Ketter2025 (LPSCl thermal)]',
            'carbon(VGCF/SuperP/SWCNT)': f'{kc * 100:.1f} W/mK [ASSUMED ~AM 하한; 소분율·--k-carbon 상향 스윕]',
            'SDCP': f'{ks * 100:.2f} W/mK [ASSUMED ~SE; ⚠전자적으론 최강도체 → k_carbon가 더 맞을 수(스윕)]',
            'PTFE': f'{k_ptfe * 100:.2f} W/mK [polymer generic; 전용 인용 없음]',
            'pore': f'{k_pore * 100:.3f} W/mK [ASSUMED 압밀ASSB≈0(진공/고립)]',
            'caveats': 'k_eff = 문헌/ASSUMED k 입력의 복셀-solve 전파값 — 열전도 실험 앵커 없음(Kapitza 계면 '
                       '열저항 무시 → 상한); network_conductivity thermal과 같은 k 앵커 공유 → 표현(복셀-field '
                       'vs 입자-graph)-일치만이지 입력·물리 검증 아님, 스케일도 다름(W/mK vs mScm-eq), 독립 아님'}
    return np.array([k_pore, k_am, k_am, kc, kc, ks, k_se, k_ptfe, kc], float), prov


def solve_thermal(sid, vox, z_top_um, z_bot_um=0.0, k_table=None, field_sids=None, field_max=90000):
    """복셀 through-plane 열전도 k_eff + 상별 ΔT/열저항(병목) 몫.  solve_sigma_z 재사용(∇·(k∇T)=0, 同 격자).
    ★多상이라 압밀 베드선 全상 연결 → 보통 항상 퍼콜(유한).  반환: k_eff_W_mK(=k_eff[W/cm·K]×100, ★Kapitza
    무시 상한), temp_drop_share(상별 through-plane 온도강하/열저항 몫 — 높을수록 열 병목; ★열류 아님 —
    직렬 flux는 상별 동일), n_dof, cg_resid, reason/unconverged.
    field_sids 주면 out['_field_pts']/['_field_j'] = 열류 |k∇T| 점군(電子/이온 필드와 동일 문법, 多상=全상
    solid; payload가 p99.8 정규화·직렬화 — '_' prefix = JSON 前 임시)."""
    if k_table is None:
        k_table, _ = thermal_k_table()
    res = solve_sigma_z(sid, k_table, vox, return_field=True, z_top_um=z_top_um, z_bot_um=z_bot_um)
    out = {'k_eff_W_mK': None, 'reason': res.get('reason'), 'n_dof': int(res.get('n_dof', 0)),
           'cg_resid': float(f"{res.get('resid', 0.0):.2g}"), 'unconverged': bool(res.get('unconverged'))}
    if not res.get('reason') and res.get('n_dof'):
        out['k_eff_W_mK'] = float(f"{res['sigma_eff'] * 100.0:.4g}")   # W/cm·K → W/m·K
        # phase_current_share = ∝ k(∇T)² 소산 functional의 상별 분담 = through-plane ΔT/열저항 몫(병목).
        # ★열류(∝ k∇T) 아님 — 정상 전도 ∇·(k∇T)=0 은 소산 0, 직렬 flux 상별 동일.
        share = phase_current_share(res, sid, k_table)
        out['temp_drop_share'] = {SID_NAME[k]: round(v, 4) for k, v in share.items()}
        if field_sids is not None:                             # 열류 |k∇T| 점군 (多상 = 全상 solid conduct)
            fp, fj = field_point_cloud(res, sid, k_table, vox, tuple(field_sids), max_points=field_max)
            if fp is not None:
                out['_field_pts'] = fp
                out['_field_j'] = fj
    return out


def field_point_cloud(res, sid, sigma_of_sid, vox, sel_sids, box_lo=(0.0, 0.0, 0.0),
                      max_points=40000, hot_budget_frac=0.35, seed=1):
    """Per-voxel current-density MAGNITUDE sampled at the selected conducting phase(s), as a
    subsampled point cloud for a paper-style field figure (Fig-2/Fig-4 grammar).

    Reuses the SAME validated (phi, cond) the solve returned (return_field=True) — this is a pure
    READOUT, it does not re-solve or change σ.  The cell-centred |J| proxy mirrors
    per_particle_current EXACTLY: for each of the 3 axes the two bounding face currents |g·Δφ| are
    half-split onto the cell (g = 2σaσb/(σa+σb) = the SAME harmonic-mean conductance the matrix
    used — so a high-σ phase such as SDCP actually lights up), then |J| = √(Jx²+Jy²+Jz²).
    Run-relative (∝ σ·Δφ; the viewer percentile-normalises); NOT vox-invariant across runs.

    sel_sids : iterable of σ-ids to KEEP (electronic field → AM+carbon {1,2,3,4,5};
               ionic field → SE+SDCP {5,6}).  Only voxels that are BOTH sel AND conductive (in the
               plate-connected component `cond`) are emitted — floating islands already dropped.
    Returns (pts_um [N,3] float32, jmag [N] float32) in the payload µm frame (voxel centres +
    box_lo), or (None, None) if the solve early-returned / nothing selected.

    Subsample keeps ALL of the hottest `hot_budget_frac` of the budget (so the conduction
    backbone survives at low point counts) + a uniform-random background for honest density."""
    if 'phi' not in res:
        return None, None
    P, cond = res['phi'], res['cond']
    sig = sigma_of_sid[sid]
    jmag = np.zeros(sid.shape, np.float64)
    for axis in (0, 1, 2):
        sa_sl = [slice(None)] * 3; sb_sl = [slice(None)] * 3
        sa_sl[axis] = slice(0, -1); sb_sl[axis] = slice(1, None)
        sa_sl, sb_sl = tuple(sa_sl), tuple(sb_sl)
        both = cond[sa_sl] & cond[sb_sl]
        sa, sb = sig[sa_sl], sig[sb_sl]
        g = np.where(both, 2.0 * sa * sb / np.maximum(sa + sb, 1e-30), 0.0)
        f = np.abs(g * (P[sa_sl] - P[sb_sl]))               # face current ∝ σ·Δφ (per face area)
        comp = np.zeros(sid.shape, np.float64)
        comp[sa_sl] += f * 0.5
        comp[sb_sl] += f * 0.5
        jmag += comp * comp
    jmag = np.sqrt(jmag)
    sel = np.isin(sid, np.asarray(list(sel_sids), np.int64)) & cond
    ii, jj, kk = np.where(sel)
    if not len(ii):
        return None, None
    vals = jmag[ii, jj, kk]
    if len(ii) > max_points:
        rng = np.random.default_rng(seed)
        order = np.argsort(vals)[::-1]
        n_hot = int(max_points * hot_budget_frac)
        hot = order[:n_hot]
        rest = rng.choice(order[n_hot:], size=max_points - n_hot, replace=False)
        pick = np.concatenate([hot, rest])
        ii, jj, kk, vals = ii[pick], jj[pick], kk[pick], vals[pick]
    pts = np.stack([(ii + 0.5) * vox + box_lo[0],
                    (jj + 0.5) * vox + box_lo[1],
                    (kk + 0.5) * vox + box_lo[2]], axis=1)
    return pts.astype(np.float32), vals.astype(np.float32)


def pore_tau(sid, vox, z_top_um, extra_solid_pts=None, box_lo=(0.0, 0.0, 0.0)):
    """A6 — PORE-phase effective-diffusion tortuosity (DiffuDict/TauFactor convention).

    Runs the SAME validated finite-volume machinery (solve_sigma_z, physics unchanged) on the
    VOID phase: σ(void)=1, σ(solid)=0, plates at z=0 / z_top → the returned sigma_eff IS the
    dimensionless D_eff/D0.  τ = ε_total / (D_eff/D0)   [tortuosity FACTOR: D_eff = D0·ε/τ].

    Conventions (honest):
      • PTFE is NOT rasterized into the e/ionic sid grid (insulator on both networks), so sid==0
        alone would read PTFE volume as open pore (ε over-count → τ under-count).  Its material
        points must be passed via extra_solid_pts (µm, grid frame) — stamped solid here, same
        single-voxel stamp convention rasterize() uses for additive points.
      • the grid is CROPPED to z ≤ z_top_um first (REQUIRED arg: without it the top plate would
        sit on the rasterization box's void padding cap and ε/D_rel measure the cap, not the
        bed).  Uncropped, every column's topmost pore voxel floats in that cap and the top
        plate loses/keeps contact by sub-voxel luck.
      • plate band = vox EXACTLY (review M1) — NOT the e-solve default vox+0.1: after the crop a
        true surface pore's centre is provably < vox from its plate plane while a pore ROOFED by
        one solid voxel is ≥ vox away, so band=vox separates open from sealed at both plates.
        The e-solve's +0.1 µm is crown-contact physics (a plate PRESSES onto crowns); for the
        pore there is no press — solid above a pore genuinely seals it.  With the default band,
        D_rel leaked through 1-voxel roofs whenever frac(z_top/vox) ∈ [0.5, 0.75) (τ<1 possible).
      • ε_total counts ALL void voxels of the cropped domain (isolated pores included —
        TauFactor convention: closed porosity RAISES τ); ε_connected (plate-reaching component)
        is reported alongside — None when the solve early-returns before the floating-island
        filter (its n_dof then counts ALL pore voxels, review m2).  D_rel below 1e-12
        (non-percolating pore) → tau=None.
      • known small biases (review m1/m4, documented not fixed): ε is measured over the cropped
        height nzc·vox while D_rel is normalised by L=z_top → one-sided τ over-read ≤ 0.5·vox/
        z_top (+0.67 % worst at 30 µm/vox 0.4, exact when frac(z_top/vox)<0.5); the AM-AM
        contact-bridge balls rasterize() stamps (1.2·vox Hertz-neck proxy) count as solid here
        (~2 % of the pore phase at ε≈15 % — a real neck does occupy that space).
      • STRUCTURAL descriptor (frame[4] cross-check / gas·liquid-infiltration axis).  ASSB Li⁺
        transport lives on the SE contact network (σ_ionic solves) — do NOT substitute this τ
        into the transport forms (CLAUDE.md audit #2 double-count trap).

    Returns dict(eps_total_pct, eps_connected_pct, D_rel, tau, n_dof, resid, unconverged
                 [, reason])."""
    if z_top_um is None or float(z_top_um) <= 0.0:
        raise ValueError('pore_tau requires z_top_um > 0 (bed thickness): without the crop the '
                         'void padding cap above the bed is measured instead of the pore network')
    s = np.asarray(sid)
    nzc = int(np.floor(float(z_top_um) / vox + 0.5))        # top-layer centre stays ≤ plate plane
    nzc = max(2, min(s.shape[2], nzc))
    s = s[:, :, :nzc].copy()
    if extra_solid_pts is not None and len(extra_solid_pts):
        ijk = np.floor((np.asarray(extra_solid_pts, np.float64) - np.asarray(box_lo, np.float64))
                       / vox).astype(int)
        ok = ((ijk >= 0) & (ijk < np.array(s.shape))).all(1)
        ijk = ijk[ok]
        s[ijk[:, 0], ijk[:, 1], ijk[:, 2]] = 7               # any non-zero id = solid to the pore solve
    pore = (s == 0)
    eps = float(pore.mean())
    if eps <= 0.0:
        return {'eps_total_pct': 0.0, 'eps_connected_pct': 0.0, 'D_rel': 0.0, 'tau': None,
                'n_dof': 0, 'resid': 0.0, 'unconverged': False, 'reason': 'no_void'}
    res = solve_sigma_z(pore.astype(np.int8), np.array([0.0, 1.0]), vox,
                        z_top_um=z_top_um, z_bot_um=0.0, plate_band_um=vox)
    d_rel = float(res['sigma_eff'])
    out = {'eps_total_pct': round(100.0 * eps, 2),
           # on early-return paths n_dof counts ALL pore voxels (floating filter never ran) —
           # connected fraction is then UNKNOWN, not "everything" (review m2)
           'eps_connected_pct': (None if res.get('reason')
                                 else round(100.0 * res['n_dof'] / s.size, 2)),
           'D_rel': float(f'{d_rel:.4g}'),
           'tau': (float(f'{eps / d_rel:.4g}') if d_rel > 1e-12 else None),
           'n_dof': res['n_dof'], 'resid': res['resid'], 'unconverged': res['unconverged']}
    if res.get('reason'):
        out['reason'] = res['reason']
    return out


def pore_pnm(sid, vox, z_top_um, extra_solid_pts=None, box_lo=(0.0, 0.0, 0.0)):
    """A13 — pore-network TOPOLOGY descriptors (nearest-seed pore-body partition; A6 확장).

    Same crop + PTFE-stamp preamble as pore_tau (conventions inherited), then:
      • EDT(pore) → plateau maxima (3³ max-filter, dist>1 voxel) = pore-body seeds →
        `ndimage.watershed_ift` basin partition (solid = background).
      • per-body: volume → equivalent radius r_eq = (3V/4π)^⅓ [µm].
      • throats: face-adjacent voxel pairs with different body labels → pore-CN (degree),
        n_throats, throat equivalent radius √(A_face/π) (voxel-resolution floor = vox).
      • closed_from_top_pct: pore volume in components NOT reaching the top layer
        (separator side = the open exterior; the bottom is the collector plate = sealed).
        This is the gas/liquid-infiltration closure axis (#286 yoo2026) — DIFFERENT from
        A6 eps_connected (both-plate percolation for the D_eff solve).

    Honest limits: EDT-plateau seeding over-segments long ridges (fine-grained bodies —
    distributions are the robust readout, single n_pores is marker-sensitive); throat area
    is a voxel face count (0.4 µm floor, sub-voxel constriction unresolved — same caveat
    as STEP3 σ).  Thin-pore fallback (no seed with dist>1): connected components become the
    bodies (n_throats=0, flagged).  STRUCTURAL descriptor only — NOT a transport input
    (same audit-#2 non-substitution rule as pore_tau)."""
    if z_top_um is None or float(z_top_um) <= 0.0:
        raise ValueError('pore_pnm requires z_top_um > 0 (same crop rule as pore_tau)')
    s = np.asarray(sid)
    nzc = int(np.floor(float(z_top_um) / vox + 0.5))
    nzc = max(2, min(s.shape[2], nzc))
    s = s[:, :, :nzc].copy()
    if extra_solid_pts is not None and len(extra_solid_pts):
        ijk = np.floor((np.asarray(extra_solid_pts, np.float64) - np.asarray(box_lo, np.float64))
                       / vox).astype(int)
        ok = ((ijk >= 0) & (ijk < np.array(s.shape))).all(1)
        ijk = ijk[ok]
        s[ijk[:, 0], ijk[:, 1], ijk[:, 2]] = 7
    pore = (s == 0)
    if not pore.any():
        return {'reason': 'no_void', 'n_pores': 0}

    # closed-from-top (component level — watershed 무관, 먼저 계산)
    lab_c, _n_c = ndimage.label(pore)                       # 6-conn = face graph
    top_ids = np.unique(lab_c[:, :, nzc - 1])
    top_ids = top_ids[top_ids > 0]
    v_all = float(pore.sum())
    v_open = float(np.isin(lab_c, top_ids).sum()) if len(top_ids) else 0.0
    closed_pct = 100.0 * (1.0 - v_open / max(v_all, 1.0))

    dist = ndimage.distance_transform_edt(pore)
    mx = ndimage.maximum_filter(dist, size=3)
    peaks = pore & (dist >= mx) & (dist > 1.0)              # >1 voxel: 1-voxel skin/line은 seed 아님
    mark, n_seed = ndimage.label(peaks)
    fallback = n_seed == 0
    if fallback:                                            # ultra-thin pore망: 성분=바디로
        lab = lab_c
        n_bodies = int(lab.max())
    else:
        # 최근접-seed 파티션 (SNOW-lite): pore 복셀을 유클리드-최근접 seed에 귀속.
        # ⚠ scipy watershed_ift는 이 용도에 부적합 확인(selftest dumbbell 734/7 오분할 —
        # IFT plateau/큐-순서 quirk) → 결정적 nearest-seed로 교체 (371/370, r_eq 2.23µm 정답).
        # 한계(정직): 직선-거리 metric이라 오목 기공에서 seed-Voronoi 경계가 벽을 가로질러
        # 그릴 수 있음 — throat 집계는 pore-내부 면만 세므로 가짜 인접은 제한적, 분포 판독 권장.
        _, idx = ndimage.distance_transform_edt(mark == 0, return_indices=True)
        lab = np.where(pore, mark[idx[0], idx[1], idx[2]], 0)
        n_bodies = int(len(np.unique(lab)) - (1 if (lab == 0).any() else 0))
    cnt = np.bincount(lab.ravel().astype(np.int64))
    if cnt.size:
        cnt[0] = 0
    ids = np.nonzero(cnt)[0]
    vol_um3 = cnt[ids] * (vox ** 3)
    r_eq = (3.0 * vol_um3 / (4.0 * np.pi)) ** (1.0 / 3.0)

    pairs = {}
    if not fallback:
        W = int(lab.max()) + 1
        for ax in range(3):
            sa = [slice(None)] * 3
            sb = [slice(None)] * 3
            sa[ax] = slice(0, -1)
            sb[ax] = slice(1, None)
            la = lab[tuple(sa)].ravel()
            lb = lab[tuple(sb)].ravel()
            m = (la > 0) & (lb > 0) & (la != lb)
            if m.any():
                lo = np.minimum(la[m], lb[m]).astype(np.int64)
                hi = np.maximum(la[m], lb[m]).astype(np.int64)
                key, c = np.unique(lo * W + hi, return_counts=True)
                for k, cc in zip(key, c):
                    pairs[int(k)] = pairs.get(int(k), 0) + int(cc)
        deg = np.zeros(W, np.int32)
        for k in pairs:
            deg[k // W] += 1
            deg[k % W] += 1
        cn = deg[ids]
    else:
        cn = np.zeros(len(ids), np.int32)
    throat_r = (np.sqrt(np.array(list(pairs.values()), float) * vox * vox / np.pi)
                if pairs else np.array([]))

    def _st(v, f=3):
        return {} if not len(v) else {
            'mean': float(f'{np.mean(v):.{f}g}'), 'med': float(f'{np.median(v):.{f}g}'),
            'p90': float(f'{np.percentile(v, 90):.{f}g}'), 'max': float(f'{np.max(v):.{f}g}')}
    out = {'n_pores': int(n_bodies), 'n_throats': int(len(pairs)),
           'r_eq_um': _st(r_eq), 'pore_cn': _st(cn.astype(float), 3),
           'closed_from_top_pct': round(closed_pct, 2),
           'trust': 'STRUCTURAL PNM (nearest-seed partition, EDT-plateau seed) — 분포가 robust 판독; '
                    'n_pores는 marker-민감, throat=face-count(vox 하한).  수송 폼 대입 금지(A6 동일)'}
    if len(throat_r):
        out['throat_r_eq_um'] = _st(throat_r)
    if fallback:
        out['fallback'] = 'components (no EDT>1 seed — ultra-thin pore)'
    return out


def solve_reaction_current(sid, sig_e_of_sid, sig_i_of_sid, pid, n_am, vox, gct_code,
                           z_top_um=None, z_bot_um=None):
    """STEP4-v1 — 저율·균일-SOC 갈바노스타틱 **반응전류 분포** (랩 slide-20 물리, 선형화 BV).

    같은 복셀 격자 위 TWO networks를 반응 계면에서만 결합한 단일 SPD Kirchhoff 시스템:
      · electronic net (σ_e table: AM+carbon+SDCP) ← 집전체 plate (bottom, φ_e=1 소스)
      · ionic net      (σ_i table: SE+SDCP)        ← 분리막 plate (top,   φ_i=0 싱크)
      · BV faces: AM(sid 1,2) ↔ ion-conductor(sid 5,6) 인접 면마다 선형화 Butler-Volmer
        컨덕턴스 g_ct = (i0·F/RT)·A_face.  Li는 이 면으로만 두 망을 건넌다 — 반응 면적이
        rasterized 접촉(=coverage)에서 자연히 나온다.
    가정(정직): 저율 선형화(과전압≪RT/F), 균일 SOC(OCV 상수 소거 — linear라 총전류로 스케일),
    충·방전은 부호만 반전.  SDCP는 혼성전도라 두 망 모두에 노드를 갖지만 자기-BV는 없음
    (인터칼레이션 전극이 아님) — 기여는 이온/전자 '배달'로만 (STEP3 서사와 연속).
    Returns dict(i_am[n_am] — 입자별 반응전류(code units, RELATIVE: caller가 정규화),
    I_tot, kcl_err, resid, unconverged, n_dof_e/i, n_bv_faces [, reason])."""
    nx, ny, nz = sid.shape
    sig_e = sig_e_of_sid[sid]
    sig_i = sig_i_of_sid[sid]
    cond_e = sig_e > 0
    cond_i = sig_i > 0
    out0 = {'i_am': np.zeros(n_am), 'I_tot': 0.0, 'kcl_err': 0.0, 'resid': 0.0,
            'unconverged': False, 'n_dof_e': int(cond_e.sum()), 'n_dof_i': int(cond_i.sum()),
            'n_bv_faces': 0}
    if not cond_e.any() or not cond_i.any():
        return {**out0, 'reason': 'missing_network'}
    z_b = float(z_bot_um) if z_bot_um is not None else 0.0
    z_plate = min(float(z_top_um) if z_top_um is not None else nz * vox, nz * vox)
    band = vox + 0.10
    zc = (np.arange(nz) + 0.5) * vox
    any_e = cond_e.any(2)
    k_first_e = np.argmax(cond_e, axis=2)
    bot_e = any_e & (zc[k_first_e] - z_b <= band)            # 집전체 접점 (전자망만)
    any_i = cond_i.any(2)
    k_last_i = nz - 1 - np.argmax(cond_i[:, :, ::-1], axis=2)
    top_i = any_i & (z_plate - zc[k_last_i] <= band)         # 분리막 접점 (이온망만)
    if not bot_e.any() or not top_i.any():
        return {**out0, 'reason': f'no_plate_contact(bot_e={int(bot_e.sum())},top_i={int(top_i.sum())})'}
    # anchored-component filter: 결합 그래프(전자·이온·BV 인접 = 모두 6-이웃 face)를 union 마스크
    # 라벨로 근사 — 어느 plate에도 안 닿는 섬은 전류 0이므로 제거 (특이 블록 방지).  union 인접이
    # 실제 엣지가 아닌 희귀 케이스(SE|carbon 면)는 아래 ε-diag 가드가 받친다.
    uni = cond_e | cond_i
    lab, _nl = ndimage.label(uni)
    _ii, _jj = np.where(bot_e)
    anch = set(lab[_ii, _jj, k_first_e[bot_e]].tolist())
    _ii, _jj = np.where(top_i)
    anch |= set(lab[_ii, _jj, k_last_i[top_i]].tolist())
    anch.discard(0)
    keep = np.isin(lab, list(anch))
    cond_e &= keep
    cond_i &= keep
    n_e = int(cond_e.sum())
    n_i = int(cond_i.sum())
    if n_e == 0 or n_i == 0:
        return {**out0, 'reason': 'all_floating_dropped'}
    idx_e = -np.ones(sid.shape, np.int64); idx_e[cond_e] = np.arange(n_e)
    idx_i = -np.ones(sid.shape, np.int64); idx_i[cond_i] = np.arange(n_i)
    sig_e = np.where(cond_e, sig_e, 0.0)
    sig_i = np.where(cond_i, sig_i, 0.0)
    N = n_e + n_i
    rows, cols, vals = [], [], []
    diag = np.zeros(N, np.float64)
    b = np.zeros(N, np.float64)

    def _net_couple(idxN, sigN, off, sl_a, sl_b):
        A, B = idxN[sl_a], idxN[sl_b]
        sa, sb = sigN[sl_a], sigN[sl_b]
        m = (A >= 0) & (B >= 0)
        if not m.any():
            return
        g = (2.0 * sa[m] * sb[m] / (sa[m] + sb[m])) * vox
        a2, b2 = A[m] + off, B[m] + off
        rows.append(a2); cols.append(b2); vals.append(-g)
        rows.append(b2); cols.append(a2); vals.append(-g)
        np.add.at(diag, a2, g); np.add.at(diag, b2, g)

    for sl_a, sl_b in ((np.s_[:-1, :, :], np.s_[1:, :, :]), (np.s_[:, :-1, :], np.s_[:, 1:, :]),
                       (np.s_[:, :, :-1], np.s_[:, :, 1:])):
        _net_couple(idx_e, sig_e, 0, sl_a, sl_b)
        _net_couple(idx_i, sig_i, n_e, sl_a, sl_b)
    # BV 계면 결합 + per-face 기록 (입자별 합산용)
    am_m = (sid == 1) | (sid == 2)
    ion_m = (sid == 5) | (sid == 6)
    bv_e, bv_i, bv_pid = [], [], []
    gct = float(gct_code)
    for sl_a, sl_b in ((np.s_[:-1, :, :], np.s_[1:, :, :]), (np.s_[:, :-1, :], np.s_[:, 1:, :]),
                       (np.s_[:, :, :-1], np.s_[:, :, 1:])):
        for am_first in (True, False):
            slA, slB = (sl_a, sl_b) if am_first else (sl_b, sl_a)
            m = am_m[slA] & ion_m[slB]
            Ae = idx_e[slA]; Bi = idx_i[slB]
            m &= (Ae >= 0) & (Bi >= 0)
            if not m.any():
                continue
            a2 = Ae[m]; b2 = Bi[m] + n_e
            g = np.full(len(a2), gct)
            rows.append(a2); cols.append(b2); vals.append(-g)
            rows.append(b2); cols.append(a2); vals.append(-g)
            np.add.at(diag, a2, g); np.add.at(diag, b2, g)
            bv_e.append(a2); bv_i.append(b2); bv_pid.append(pid[slA][m])
    n_bv = int(sum(len(x) for x in bv_e))
    if n_bv == 0:
        return {**out0, 'n_dof_e': n_e, 'n_dof_i': n_i, 'reason': 'no_reaction_interface'}
    # plates: 전자망 bottom(φ=1 소스), 이온망 top(φ=0)
    def _plate(idxN, sigN, off, mask, ksurf, plane, phi_p):
        ii, jj = np.where(mask)
        kk2 = ksurf[mask]
        A = idxN[ii, jj, kk2]
        sa = sigN[ii, jj, kk2]
        m = A >= 0
        dist = np.maximum(np.abs(zc[kk2[m]] - plane), 0.5 * vox)
        g = sa[m] * vox * vox / dist
        np.add.at(diag, A[m] + off, g)
        if phi_p != 0.0:
            np.add.at(b, A[m] + off, g * phi_p)
        return A[m] + off, g
    eb_nodes, eb_g = _plate(idx_e, sig_e, 0, bot_e, k_first_e, z_b, 1.0)
    _plate(idx_i, sig_i, n_e, top_i, k_last_i, z_plate, 0.0)
    # degree-0 노드(엣지 전무)만 ε-고정.  union-라벨이 false-adjacency로 남길 수 있는 "고립
    # 서브그래프"(예: SE에 싸인 carbon 섬)는 특이 블록이지만 b=0 + CG(x0=0)에서 φ≡0으로 정확히
    # 유지된다(구조적 블록대각 + Krylov가 0-블록을 못 건드림) — 리뷰 프로브로 ΔI ~1e-15 확인.
    # ⚠ 이 안전성은 CG+x0=0 전제: 직접분해(spsolve)나 블록혼합 preconditioner로 바꾸면
    # 컴포넌트-그래프 anchoring(BV 엣지 기반 union-find)으로 교체할 것.
    diag[diag == 0.0] = 1.0
    L = sparse.coo_matrix((np.concatenate(vals + [diag]),
                           (np.concatenate(rows + [np.arange(N)]),
                            np.concatenate(cols + [np.arange(N)]))), shape=(N, N)).tocsr()
    print(f'    STEP4 rxn solve: e {n_e:,} + i {n_i:,} dof, BV faces {n_bv:,} — CG '
          f'({"GPU" if GPU_SOLVE else "CPU"})…', flush=True)
    phi, info = _solve_cg(L, b)
    resid = float(np.linalg.norm(L @ phi - b) / max(np.linalg.norm(b), 1e-30))
    unconv = bool(info) or resid > 1e-6
    I_tot = float(np.sum(eb_g * (1.0 - phi[eb_nodes])))
    i_am = np.zeros(n_am, np.float64)
    I_bv = 0.0
    for a2, b2, pd in zip(bv_e, bv_i, bv_pid):
        f = gct * (phi[a2] - phi[b2])                        # +: e-net → i-net (한 방향, linear)
        I_bv += float(f.sum())
        mm2 = pd >= 0
        np.add.at(i_am, pd[mm2], f[mm2])
    kcl = abs(I_tot - I_bv) / max(abs(I_tot), 1e-30)         # KCL: plate 유입 = BV 총 통과
    return {'i_am': i_am, 'I_tot': I_tot, 'kcl_err': float(kcl), 'resid': resid,
            'unconverged': unconv, 'n_dof_e': n_e, 'n_dof_i': n_i, 'n_bv_faces': n_bv}


def _selftest_rxn():
    """STEP4 sandwich analytic: 하반 AM slab / 상반 SE slab, 계면 BV — 직렬저항 I와 균일 i_n."""
    vox = 0.5
    nxy, nz = 6, 12
    sid = np.zeros((nxy, nxy, nz), np.int8)
    sid[:, :, :6] = 1                                        # AM (전자망)
    sid[:, :, 6:] = 6                                        # SE (이온망)
    pid = np.full(sid.shape, -1, np.int32)
    pid[:, :, :6] = 0                                        # 입자 1개로 합산
    sig_e = np.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    sig_i = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0])
    gct = 0.05                                               # 면당 (code units)
    r = solve_reaction_current(sid, sig_e, sig_i, pid, 1, vox, gct,
                               z_top_um=nz * vox, z_bot_um=0.0)
    # 직렬 해석해 (µm-code 단위 일관, 코드 규약대로 직접 합산):
    #   per-column R = 1/g_plate,e + 5/(σe·vox) + 1/g_ct + 5/(σi·vox) + 1/g_plate,i
    ge_plate = 1.0 * vox * vox / (0.5 * vox)
    gi_plate = 2.0 * vox * vox / (0.5 * vox)
    R_col = 1.0 / ge_plate + 5 * (1.0 / (1.0 * vox)) + 1.0 / gct + 5 * (1.0 / (2.0 * vox)) + 1.0 / gi_plate
    I_exp = nxy * nxy / R_col
    okI = abs(r['I_tot'] - I_exp) / I_exp < 1e-3
    okK = r['kcl_err'] < 1e-6
    okU = abs(r['i_am'][0] - r['I_tot']) / r['I_tot'] < 1e-6   # 입자 1개 = 총전류 (CG rtol 1e-8 여유)
    print(f"rxn sandwich: I={r['I_tot']:.6f} (expect {I_exp:.6f})  {'OK' if okI else 'FAIL'}")
    print(f"rxn KCL: plate vs ΣBV err={r['kcl_err']:.2e}  {'OK' if okK else 'FAIL'}")
    print(f"rxn per-particle sum == I_tot  {'OK' if okU else 'FAIL'}")
    # 방향 대칭 — 좌/우 미러 배치가 같은 I·face 수 (am_first 양쪽 분기 고정; 물리 리뷰 프로브 영구화)
    sidL = np.zeros((6, 6, 12), np.int8); sidL[:3] = 1; sidL[3:] = 6
    sidR = np.zeros((6, 6, 12), np.int8); sidR[3:] = 1; sidR[:3] = 6
    pidL = np.where(sidL == 1, 0, -1).astype(np.int32)
    pidR = np.where(sidR == 1, 0, -1).astype(np.int32)
    rL = solve_reaction_current(sidL, sig_e, sig_i, pidL, 1, vox, gct, z_top_um=nz * vox, z_bot_um=0.0)
    rR = solve_reaction_current(sidR, sig_e, sig_i, pidR, 1, vox, gct, z_top_um=nz * vox, z_bot_um=0.0)
    okM = (rL['n_bv_faces'] == rR['n_bv_faces']
           and abs(rL['I_tot'] - rR['I_tot']) / max(abs(rL['I_tot']), 1e-30) < 1e-6)
    print(f"rxn mirror(lateral BV): I_L={rL['I_tot']:.6f} I_R={rR['I_tot']:.6f} "
          f"faces {rL['n_bv_faces']}/{rR['n_bv_faces']}  {'OK' if okM else 'FAIL'}")
    ok = okI and okK and okU and okM
    print('RXN SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def _selftest():
    """Analytic checks that pin assembly + BC signs."""
    ok = True
    sig_tab = np.array([0.0, 1.0, 4.0])
    # 1) uniform block σ=1 → σ_eff = 1
    sid = np.ones((6, 6, 10), np.int8)
    r = solve_sigma_z(sid, sig_tab, 0.5)
    ok &= abs(r['sigma_eff'] - 1.0) < 1e-6
    print(f"uniform:  σ_eff={r['sigma_eff']:.6f}  (expect 1.0)  {'OK' if ok else 'FAIL'}")
    # 2) series laminate (z-stacked σ=1 / σ=4, half-half) → harmonic mean 1.6
    sid = np.ones((6, 6, 10), np.int8); sid[:, :, 5:] = 2
    r = solve_sigma_z(sid, sig_tab, 0.5)
    e = abs(r['sigma_eff'] - 1.6) < 1e-3
    ok &= e; print(f"series:   σ_eff={r['sigma_eff']:.6f}  (expect 1.6 harmonic)  {'OK' if e else 'FAIL'}")
    # 3) parallel laminate (x-split) → arithmetic mean 2.5
    sid = np.ones((6, 6, 10), np.int8); sid[3:, :, :] = 2
    r = solve_sigma_z(sid, sig_tab, 0.5)
    e = abs(r['sigma_eff'] - 2.5) < 1e-3
    ok &= e; print(f"parallel: σ_eff={r['sigma_eff']:.6f}  (expect 2.5 arithmetic)  {'OK' if e else 'FAIL'}")
    # 4) disconnected (air gap layer) → σ_eff = 0
    sid = np.ones((6, 6, 10), np.int8); sid[:, :, 5] = 0
    r = solve_sigma_z(sid, sig_tab, 0.5)
    e = r['sigma_eff'] < 1e-12
    ok &= e; print(f"gap:      σ_eff={r['sigma_eff']:.2e}  (expect 0)  {'OK' if e else 'FAIL'}")
    # 5) thin conductive column (1/36 of area) → σ_eff = 1/36 of column σ
    sid = np.zeros((6, 6, 10), np.int8); sid[0, 0, :] = 1
    r = solve_sigma_z(sid, sig_tab, 0.5)
    e = abs(r['sigma_eff'] - 1.0 / 36.0) < 1e-6
    ok &= e; print(f"column:   σ_eff={r['sigma_eff']:.6f}  (expect {1/36:.6f})  {'OK' if e else 'FAIL'}")
    print('SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def _selftest_pore():
    """A6 pore-τ analytic checks — crop, PTFE stamping, TauFactor convention."""
    ok = True
    # 1) all-void box → ε=100%, D_rel=1, τ=1 exactly
    sid = np.zeros((6, 6, 10), np.int8)
    r = pore_tau(sid, 0.5, z_top_um=5.0)
    e = abs(r['tau'] - 1.0) < 1e-6 and abs(r['eps_total_pct'] - 100.0) < 1e-9
    ok &= e; print(f"all-void: τ={r['tau']}  ε={r['eps_total_pct']}%  (expect 1, 100)  {'OK' if e else 'FAIL'}")
    # 2) straight 2×2 channel through solid → D_rel = area share EXACT (plate half-cell convention),
    #    τ = 1 exactly (straight pore has no tortuosity)
    sid = np.ones((6, 6, 10), np.int8); sid[2:4, 2:4, :] = 0
    r = pore_tau(sid, 0.5, z_top_um=5.0)
    e = abs(r['tau'] - 1.0) < 1e-6 and abs(r['D_rel'] - 4.0 / 36.0) < 5e-4   # D_rel ships %.4g-rounded
    ok &= e; print(f"channel:  τ={r['tau']}  D_rel={r['D_rel']:.4f}  (expect 1, {4/36:.4f})  {'OK' if e else 'FAIL'}")
    # 3) void padding cap ABOVE the bed (raster box taller than the pressed thickness) — uncropped,
    #    every column's topmost pore voxel floats in the cap and the top plate decouples; the crop
    #    must restore the exact channel answer
    sid = np.ones((6, 6, 14), np.int8); sid[2:4, 2:4, :] = 0; sid[:, :, 10:] = 0
    r = pore_tau(sid, 0.5, z_top_um=5.0)
    e = abs(r['tau'] - 1.0) < 1e-6
    ok &= e; print(f"crop:     τ={r['tau']}  (expect 1 — padding cap cropped)  {'OK' if e else 'FAIL'}")
    # 4) extra_solid_pts stamping (the PTFE path): plug the channel with 4 stamped points → the pore
    #    no longer percolates → D_rel ~ 0, τ = None
    sid = np.ones((6, 6, 10), np.int8); sid[2:4, 2:4, :] = 0
    plug = np.array([[1.25, 1.25, 2.25], [1.75, 1.25, 2.25], [1.25, 1.75, 2.25], [1.75, 1.75, 2.25]])
    r = pore_tau(sid, 0.5, z_top_um=5.0, extra_solid_pts=plug)
    e = (r['tau'] is None) and r['D_rel'] < 1e-9
    ok &= e; print(f"stamp:    τ={r['tau']}  D_rel={r['D_rel']:.1e}  (expect None, ~0 — plugged)  {'OK' if e else 'FAIL'}")
    # 5) isolated-pore honesty: a sealed 2-voxel pocket raises ε_total but not ε_connected;
    #    τ uses ε_total (TauFactor) → closed porosity reads as τ > 1
    sid = np.ones((6, 6, 10), np.int8); sid[2:4, 2:4, :] = 0; sid[0, 0, 4:6] = 0
    r = pore_tau(sid, 0.5, z_top_um=5.0)
    e = r['eps_total_pct'] > r['eps_connected_pct'] and r['tau'] is not None and r['tau'] > 1.0
    ok &= e; print(f"isolated: ε_tot={r['eps_total_pct']}% > ε_conn={r['eps_connected_pct']}%  τ={r['tau']}"
                   f"  (expect τ>1: closed porosity penalised)  {'OK' if e else 'FAIL'}")
    # 6) review M1 — 1-voxel solid ROOF must SEAL the channel even when frac(z_top/vox) puts the
    #    roofed pore centre inside the e-solve's default band (vox+0.1): vox=0.4, z_top=2.68
    #    (frac 0.7) → roofed pore dist 0.48 < 0.5 leaked with the old band; band=vox seals it
    sid = np.ones((6, 6, 8), np.int8); sid[2:4, 2:4, 0:6] = 0    # channel k=0..5, solid roof k=6
    r = pore_tau(sid, 0.4, z_top_um=2.68)
    e = r['tau'] is None and r['D_rel'] < 1e-9 and bool(r.get('reason'))
    ok &= e; print(f"roof:     τ={r['tau']}  D_rel={r['D_rel']:.1e}  reason={r.get('reason')}"
                   f"  (expect sealed — old band read τ<1 through the roof)  {'OK' if e else 'FAIL'}")
    print('PORE SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def _selftest_swcnt():
    """A14 — phase-6(SWCNT sheath) rasterize 스탬프 + 전자-도체/이온-투명 배선 검증.
    리뷰 CRITICAL 재발 방지: phase→sid 맵 누락 시 점이 무음 drop되어 σ_e 효과가 0이 되는 버그."""
    ok = True
    am_c = np.array([[5.0, 5.0, 5.0]]); am_r = np.array([2.0]); am_t = np.array([1])
    pts = np.array([[5.0, 5.0, 7.3], [1.0, 1.0, 1.0]])       # sheath skin점 + 원거리 VGCF 대조점
    ph = np.array([6, 2], np.int8)
    se = np.array([[8.0, 8.0, 8.0]])
    sid, _ = rasterize(am_c, am_r, am_t, pts, ph, (0, 0, 0), (10.0, 10.0, 10.0), 0.4, se_pts=se)
    v6 = sid[int(5.0 / .4), int(5.0 / .4), int(7.3 / .4)]
    v2 = sid[int(1.0 / .4), int(1.0 / .4), int(1.0 / .4)]
    e = (v6 == 8) and (v2 == 3)
    ok &= e; print(f'stamp:     phase6→sid {v6} (expect 8), phase2→sid {v2} (expect 3)  {"OK" if e else "FAIL"}')
    # 전자 테이블: idx8 도체 / 이온 테이블: 기본 SE-투명(σ>0) vs 차단(0) — payload 테이블 모양 재현
    sig_e = np.array([0, .01, .005, 100, 10, 250, 0, 0, 100.0])
    sig_i_t = np.array([0, 0, 0, 0, 0, .0006, .003, 0, .003])
    sig_i_b = np.array([0, 0, 0, 0, 0, .0006, .003, 0, 0.0])
    e = sig_e[v6] > 0 and sig_i_t[v6] > 0 and sig_i_b[v6] == 0.0
    ok &= e; print(f'tables:    σ_e[8]={sig_e[8]} σ_i_transparent[8]={sig_i_t[8]} σ_i_blockUB[8]={sig_i_b[8]}  '
                   f'{"OK" if e else "FAIL"}')
    # SID_NAME 완결성 (phase_current_share KeyError 방지)
    e = SID_NAME.get(8) == 'SWCNT'
    ok &= e; print(f'sid-name:  SID_NAME[8]={SID_NAME.get(8)}  {"OK" if e else "FAIL"}')
    print('SWCNT-STAMP SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def _selftest_pnm():
    """A13 pore-PNM analytic checks — dumbbell 2-body/1-throat, sealed closure, thin fallback."""
    ok = True
    # 1) dumbbell: 두 구형 기공(r=4.4vox) + 1-voxel 목(neck) — 밀봉 박스 → n_pores=2, n_throats=1,
    #    CN mean=1, closed_from_top=100%
    n = (40, 20, 20)
    sid = np.ones(n, np.int8)
    zz = np.indices(n).astype(float)
    for cx in (10.0, 30.0):
        m = ((zz[0] - cx) ** 2 + (zz[1] - 10.0) ** 2 + (zz[2] - 10.0) ** 2) <= 4.4 ** 2
        sid[m] = 0
    sid[10:31, 10, 10] = 0                                   # 1-voxel neck (dist=1 → seed 아님)
    r = pore_pnm(sid, 0.5, z_top_um=10.0)
    e = (r['n_pores'] == 2 and r['n_throats'] == 1
         and abs(r['pore_cn']['mean'] - 1.0) < 1e-9 and r['closed_from_top_pct'] == 100.0)
    ok &= e
    print(f"dumbbell: n_pores={r['n_pores']} throats={r['n_throats']} CN={r['pore_cn'].get('mean')} "
          f"closed={r['closed_from_top_pct']}%  (expect 2/1/1.0/100)  {'OK' if e else 'FAIL'}")
    # r_eq sanity: 구 r=4.4vox=2.2µm에 목 절반씩 → 등가반경 ≈2.2µm ±20%
    e = abs(r['r_eq_um']['med'] - 2.2) / 2.2 < 0.2
    ok &= e
    print(f"r_eq:     med={r['r_eq_um']['med']}µm  (expect ≈2.2 ±20%)  {'OK' if e else 'FAIL'}")
    # 2) 위-열린 직선 채널 (2×2, 전체 관통) — ultra-thin → fallback=components, closed 0%
    sid = np.ones((6, 6, 10), np.int8)
    sid[2:4, 2:4, :] = 0
    r = pore_pnm(sid, 0.5, z_top_um=5.0)
    e = r['n_pores'] == 1 and r['closed_from_top_pct'] == 0.0 and 'fallback' in r
    ok &= e
    print(f"channel:  n_pores={r['n_pores']} closed={r['closed_from_top_pct']}% fallback={'Y' if 'fallback' in r else 'N'}"
          f"  (expect 1/0/Y)  {'OK' if e else 'FAIL'}")
    # 3) 열린 채널 + 밀봉 구 공존 → closed% = 구 부피 몫 (0<closed<100)
    sid = np.ones((20, 20, 12), np.int8)
    sid[2:4, 2:4, :] = 0
    m = ((zz[0][:20, :20, :12] - 12.0) ** 2 + (zz[1][:20, :20, :12] - 12.0) ** 2
         + (zz[2][:20, :20, :12] - 5.0) ** 2) <= 3.4 ** 2
    sid[m] = 0
    r = pore_pnm(sid, 0.5, z_top_um=6.0)
    e = 0.0 < r['closed_from_top_pct'] < 100.0
    ok &= e
    print(f"mixed:    closed={r['closed_from_top_pct']}%  (expect 0<x<100)  {'OK' if e else 'FAIL'}")
    # 4) no void → reason
    r = pore_pnm(np.ones((4, 4, 6), np.int8), 0.5, z_top_um=3.0)
    e = r.get('reason') == 'no_void'
    ok &= e
    print(f"no-void:  reason={r.get('reason')}  {'OK' if e else 'FAIL'}")
    print('PNM SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--selftest', action='store_true', help='run the analytic laminate/percolation checks')
    ap.add_argument('--selftest-rxn', action='store_true',
                    help='STEP4 sandwich analytic (series-R total current + uniform per-particle i + KCL)')
    ap.add_argument('--selftest-pore', action='store_true',
                    help='A6 pore-τ analytic checks (crop / PTFE stamp / TauFactor convention)')
    ap.add_argument('--selftest-pnm', action='store_true',
                    help='A13 pore-PNM checks (dumbbell 2-body/1-throat / closure / thin fallback)')
    ap.add_argument('--selftest-swcnt', action='store_true',
                    help='A14 SWCNT sheath 스탬프 검증 (phase6→sid8, 전자-도체/이온-투명 테이블)')
    ap.add_argument('--integration', action='store_true',
                    help='run the committed real14 integration probe (AM-only vs +300 synthetic VGCF, '
                         'seed 0, vox 0.4) — reproduces the review-anchored numbers + monotonicity')
    a = ap.parse_args()
    if a.selftest:
        sys.exit(_selftest())
    if a.selftest_rxn:
        sys.exit(_selftest_rxn())
    if a.selftest_pore:
        sys.exit(_selftest_pore())
    if a.selftest_pnm:
        sys.exit(_selftest_pnm())
    if a.selftest_swcnt:
        sys.exit(_selftest_swcnt())
    if a.integration:
        import os
        _csv = os.path.join(os.path.dirname(__file__), '..', 'docs/data/real14_am_scaffold.csv')
        am = np.loadtxt(_csv, delimiter=',', comments='#')
        t, c, r = am[:, 0].astype(int), am[:, 1:4] * 1000.0, am[:, 4] * 1000.0
        c[:, 2] -= (c[:, 2] - r).min()
        hi = (50.0, 50.0, float((c[:, 2] + r).max()))
        rng = np.random.default_rng(0)
        pts = []
        for _ in range(300):
            p0 = rng.uniform([0, 0, 0], hi); d = rng.normal(size=3); d /= np.linalg.norm(d)
            pts.append(p0 + np.outer(np.arange(0, 10, 0.2), d))
        pts = np.concatenate(pts); ph = np.full(len(pts), 2)
        inb = ((pts >= 0) & (pts < hi)).all(1); pts, ph = pts[inb], ph[inb]
        sig = np.array([0.0, 0.010, 0.005, 100.0, 10.0, 150.0, 0.0])
        out = {}
        for label, ap_, aph in (('AM-only', None, None), ('AM+VGCF', pts, ph)):
            sid, pid = rasterize(c, r, t, ap_, aph, (0, 0, 0), hi, 0.4)
            res = solve_sigma_z(sid, sig, 0.4, z_top_um=hi[2], z_bot_um=0.0)
            out[label] = res['sigma_eff']
            print(f"[{label:8s}] σ_eff={res['sigma_eff']:.4g} S/cm  dof={res['n_dof']:,} "
                  f"plate_vox={res['n_plate_vox']} resid={res['resid']:.1e}")
        boost = out['AM+VGCF'] / max(out['AM-only'], 1e-30)
        print(f"carbon boost ×{boost:.2f}  → {'PASS (monotone)' if boost > 1.0 else 'FAIL'}")
        sys.exit(0 if boost > 1.0 else 1)
    ap.print_help()
