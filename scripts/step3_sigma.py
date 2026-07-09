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
SIGMA_DEFAULT = {'AM_S': 0.010, 'AM_P': 0.005, 'VGCF': 100.0, 'SuperP': 10.0, 'SDCP': 0.010}
PHASE_NAME = {2: 'VGCF', 3: 'SuperP', 5: 'SDCP'}          # additive phase codes (4 PTFE = insulator)


def rasterize(am_c, am_r, am_t, add_pts, add_phase, box_lo, box_hi, vox, tol_am_um=0.10):
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
    # AM-AM contact bridges (econn contact rule: gap ≤ tol)
    try:
        from scipy.spatial import cKDTree
        tree = cKDTree(am_c)
        for i, j in tree.query_pairs(2.0 * float(am_r.max()) + tol_am_um):
            d = float(np.linalg.norm(am_c[i] - am_c[j]))
            if d <= am_r[i] + am_r[j] + tol_am_um:
                mid = am_c[i] + (am_c[j] - am_c[i]) * (am_r[i] + 0.5 * (d - am_r[i] - am_r[j])) / max(d, 1e-12)
                soft = i if am_t[i] != 1 else j            # prefer the AM_S σ-id (lower σ, conservative);
                s = 2 if am_t[soft] == 1 else 1            #   AM_P-AM_P pairs stay AM_P
                _ball(mid, 1.2 * vox, s, soft)
    except Exception:
        pass
    # additive points: cell-stamp (carbon overwrites AM at shared cells — the higher-σ phase wins,
    # which is the physical series-shortcut at an anchored contact)
    if add_pts is not None and len(add_pts):
        ijk = np.floor((add_pts - lo) / vox).astype(int)
        ok = ((ijk >= 0) & (ijk < n)).all(1)
        ijk, ph = ijk[ok], add_phase[ok]
        for code, s in ((2, 3), (3, 4), (5, 5)):           # phase → sid
            m = ph == code
            if m.any():
                sid[ijk[m, 0], ijk[m, 1], ijk[m, 2]] = s
    return sid, pid


def solve_sigma_z(sid, sigma_of_sid, vox, return_field=False, z_top_um=None):
    """Effective through-plane (z) σ of the voxel σ-id grid.  Finite volume, harmonic-mean face
    conductance g = (2σaσb/(σa+σb))·vox (cubic voxels: face area vox² / distance vox), collector
    plate φ=1 at the bottom bed surface, φ=0 plate at the top, lateral Neumann.
    z_top_um: put the TOP plate at this height (the bed THICKNESS — production passes it).  Without
    it the top plate sits at the highest occupied layer, which is FRAGILE: one protruding fibre tip
    moves the plate up and the whole current funnels through those few voxels (integration test:
    adding VGCF *lowered* σ_eff ×24 — a plate artifact, since adding conductors is monotone).
    Returns dict(sigma_eff, n_dof, k_plates, cg_iters, resid [, phi, cond])."""
    sig = sigma_of_sid[sid]                                # per-voxel σ (S/cm)
    cond = sig > 0
    if not cond.any():
        return {'sigma_eff': 0.0, 'n_dof': 0, 'n_floating_dropped': 0, 'cg_iters': 0, 'resid': 0.0}
    # PLATE LAYERS: bottom = lowest OCCUPIED conductive layer (a sphere tangent to a plane never
    # reaches that layer's voxel CENTRES, so raw grid ends read empty → σ=0 for every run — caught
    # by the integration test).  Top = highest layer WITH AM (sid 1/2): the AM spheres ARE the bed
    # frame, so that layer is the bed surface a top plate can touch — a single protruding carbon
    # strand must NOT carry the plate (funnel artifact: adding VGCF *lowered* σ ×24 in the test).
    # z_top_um (bed thickness, production) additionally clips.  Falls back to occupancy top when
    # the grid has no AM (pure-carbon lab cases / selftests).
    occ = np.where(cond.any((0, 1)))[0]
    k_bot = int(occ[0])
    am_occ = np.where((((sid == 1) | (sid == 2)) & cond).any((0, 1)))[0]
    k_top = int(am_occ[-1]) if len(am_occ) else int(occ[-1])
    if z_top_um is not None:
        k_top = min(k_top, max(k_bot + 1, int(round(z_top_um / vox)) - 1))
    k_top = max(k_top, k_bot + 1)
    if k_top <= k_bot:
        return {'sigma_eff': 0.0, 'n_dof': int(cond.sum()), 'n_floating_dropped': 0, 'cg_iters': 0,
                'resid': 0.0}
    # FLOATING ISLANDS (components touching NEITHER plate layer) make the Laplacian singular
    # (zero-diag isolated voxels / zero-sum blocks → CG NaN — caught by the integration test).
    # They carry no current by physics → drop them (their je reads 0).
    lab, _nl = ndimage.label(cond)                         # 6-connectivity = the face-coupling graph
    plate = np.unique(np.concatenate([lab[:, :, k_bot].ravel(), lab[:, :, k_top].ravel()]))
    plate = plate[plate > 0]
    n_float = int(cond.sum())
    cond &= np.isin(lab, plate)
    n_float -= int(cond.sum())
    n_dof = int(cond.sum())
    if n_dof == 0:
        return {'sigma_eff': 0.0, 'n_dof': 0, 'n_floating_dropped': n_float, 'cg_iters': 0, 'resid': 0.0}
    sig = np.where(cond, sig, 0.0)
    idx = -np.ones(sid.shape, np.int64)
    idx[cond] = np.arange(n_dof)
    nx, ny, nz = sid.shape

    rows, cols, vals = [], [], []
    diag = np.zeros(n_dof, np.float64)
    b = np.zeros(n_dof, np.float64)

    def couple(sl_a, sl_b):
        A, B = idx[sl_a], idx[sl_b]
        sa, sb = sig[sl_a], sig[sl_b]
        m = (A >= 0) & (B >= 0)
        if not m.any():
            return
        g = (2.0 * sa[m] * sb[m] / (sa[m] + sb[m])) * vox   # S·cm... units: σ[S/cm]·vox[µm] — consistent
        a, bb = A[m], B[m]                                  #   throughout (cancels in σ_eff; see below)
        rows.append(a); cols.append(bb); vals.append(-g)
        rows.append(bb); cols.append(a); vals.append(-g)
        np.add.at(diag, a, g); np.add.at(diag, bb, g)

    couple(np.s_[:-1, :, :], np.s_[1:, :, :])
    couple(np.s_[:, :-1, :], np.s_[:, 1:, :])
    couple(np.s_[:, :, :-1], np.s_[:, :, 1:])
    # Dirichlet plates AT THE BED SURFACES: k_bot layer ↔ φ=1 collector, k_top layer ↔ φ=0
    # (half-cell distance → g = 2σ·vox)
    for k, phi_p in ((k_bot, 1.0), (k_top, 0.0)):
        A = idx[:, :, k]; sa = sig[:, :, k]
        m = A >= 0
        g = 2.0 * sa[m] * vox
        np.add.at(diag, A[m], g)
        if phi_p != 0.0:
            np.add.at(b, A[m], g * phi_p)
    L = sparse.coo_matrix((np.concatenate(vals + [diag]),
                           (np.concatenate(rows + [np.arange(n_dof)]),
                            np.concatenate(cols + [np.arange(n_dof)]))),
                          shape=(n_dof, n_dof)).tocsr()
    Minv = sparse.diags(1.0 / L.diagonal())
    phi, info = cg(L, b, rtol=1e-8, maxiter=12000, M=Minv)
    resid = float(np.linalg.norm(L @ phi - b) / max(np.linalg.norm(b), 1e-30))
    # total current through the bottom plate: I = Σ g_plate·(1 − φ_bottom)
    A0 = idx[:, :, k_bot]; s0 = sig[:, :, k_bot]; m0 = A0 >= 0
    I = float(np.sum(2.0 * s0[m0] * vox * (1.0 - phi[A0[m0]])))
    # σ_eff: I[σ·vox·V] over plate area (nx·ny·vox²) and plate gap L = (k_top−k_bot+1)·vox, ΔV=1
    #   σ_eff = I·L/(A·ΔV) = I·(k_top−k_bot+1)/(nx·ny·vox)   [same units as σ input]
    L_lay = k_top - k_bot + 1
    sigma_eff = I * L_lay / (nx * ny * vox)
    out = {'sigma_eff': float(sigma_eff), 'n_dof': n_dof, 'n_floating_dropped': n_float,
           'k_plates': (k_bot, k_top), 'cg_iters': int(info) if info else 0, 'resid': resid}
    if return_field:
        P = np.zeros(sid.shape, np.float64); P[cond] = phi
        out['phi'] = P; out['cond'] = cond
    return out


def per_particle_current(res, sid, pid, sigma_of_sid, vox, n_am):
    """Mean |J_z| (A per unit area, ∝ σ·∇φ) over each AM particle's voxels — the slide-20 axis.
    Uses the z-face currents so the number reads as through-plane current density."""
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
    P, cond = res['phi'], res['cond']
    sig = sigma_of_sid[sid]
    diss = np.zeros(sid.shape, np.float64)
    for sl_a, sl_b in ((np.s_[:-1, :, :], np.s_[1:, :, :]), (np.s_[:, :-1, :], np.s_[:, 1:, :]),
                       (np.s_[:, :, :-1], np.s_[:, :, 1:])):
        both = cond[sl_a] & cond[sl_b]
        sa, sb = sig[sl_a], sig[sl_b]
        g = np.where(both, 2.0 * sa * sb / np.maximum(sa + sb, 1e-30), 0.0)
        d = g * (P[sl_a] - P[sl_b]) ** 2                   # per-face dissipation, split half-half
        diss[sl_a] += 0.5 * d; diss[sl_b] += 0.5 * d
    tot = diss.sum()
    out = {}
    for s in np.unique(sid[sid > 0]):
        out[int(s)] = float(diss[sid == s].sum() / max(tot, 1e-30))
    return out


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


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--selftest', action='store_true', help='run the analytic laminate/percolation checks')
    a = ap.parse_args()
    if a.selftest:
        sys.exit(_selftest())
    ap.print_help()
