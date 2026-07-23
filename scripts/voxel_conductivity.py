#!/usr/bin/env python3
"""Image-based effective conductivity on the MPM voxel grid — the FEM/continuum
cross-check for the DEM network (Kirchhoff/Holm) solver.

Take the MPM phase grid (each voxel = void / SE / AM / VGCF / SuperP …), assign a
per-voxel conductivity for the channel of interest, hold the TOP face at 1 V and
the BOTTOM at 0 V, and solve ∇·(σ∇φ)=0 (finite-volume, harmonic-mean face
conductances, insulating side walls).  σ_eff = I·L / (A·ΔV) — the homogenised
conductivity a blocking-electrode EIS / 4-probe would read.

Channels:
  ionic      : SE conducts (σ_SE), AM + carbon + void block  → σ_eff,ion
  electronic : AM + VGCF + SuperP conduct, SE + void block   → σ_eff,e
               (carbon σ ≫ AM → fibres BRIDGE dead AM: the 도전재 payoff, quantified)

This gives the MPM a TRANSPORT readout (it had only mechanics) → a SECOND,
independent σ to validate the DEM network solver (frame[4]); and it ingests the
VGCF/SuperP phases from additives.py natively.

  python3 scripts/voxel_conductivity.py            # self-test (slab / series / parallel)
"""
from __future__ import annotations
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import cg

_USE_GPU = False   # set by --gpu: run the CG on the GPU (CuPy) when available — big speedup for the
#                    thick-electrode grids (256×256×700+ ≈ 46M cells); falls back to CPU automatically.

_SIGMA_AM_E = None  # set by --sigma-am-e: override the AM electronic σ (mS/cm).  0 → AM is a NON-conducting
#                     obstacle so CARBON is the sole e-path → isolates the carbon-only percolation regime
#                     (the literature 1D-VGCF vs 0D-SuperP comparison, where the AM is not the conductor).


def _cg_solve(A, b, tol=1e-6, label=''):
    """Jacobi-preconditioned CG for A·x=b.  GPU (CuPy) when --gpu and CuPy import OK (the solve, not
    just the MPM, then runs on the GPU), else CPU (scipy).  Returns x (numpy).
    label: print a residual-based % progress every ~1.5 s (both GPU & CPU) so a long solve is never
    a silent '…' — keeps the output flowing so a remote SSH session doesn't time out / broken-pipe."""
    import sys as _sys, time as _time
    N = A.shape[0]
    Ad = A.diagonal(); minv = 1.0 / np.where(Ad > 0, Ad, 1.0)
    bnorm = float(np.linalg.norm(b)) or 1.0
    denom = -np.log10(tol) or 6.0                       # residual must drop this many decades → 100%
    cnt = [0]; t0 = _time.time(); last = [t0]

    def _mk_cb(Amat, bvec, xp):
        def cb(xk):                                     # CG callback gets the current solution xk
            cnt[0] += 1
            now = _time.time()
            if label and now - last[0] > 1.5:           # throttle to ~1.5 s (cheap: 1 matvec per print)
                last[0] = now
                r = float(xp.linalg.norm(bvec - Amat.dot(xk)))
                pct = min(100.0, max(0.0, 100.0 * np.log10(bnorm / max(r, 1e-30)) / denom))
                print(f'\r      [{label}] CG ~{pct:5.1f}%  (iter {cnt[0]}, {now - t0:.0f}s)',
                      end='', flush=True)
        return cb
    if _USE_GPU:
        try:
            import cupy as cp
            import cupyx.scipy.sparse as _csp
            import cupyx.scipy.sparse.linalg as _csl
            Ag = _csp.csr_matrix(A.astype(np.float64)); bg = cp.asarray(b); Mg = _csp.diags(cp.asarray(minv))
            cb = _mk_cb(Ag, bg, cp)
            try:
                x = _csl.cg(Ag, bg, tol=tol, maxiter=20000, M=Mg, callback=cb)[0]
            except TypeError:                              # newer CuPy: rtol instead of tol
                x = _csl.cg(Ag, bg, rtol=tol, maxiter=20000, M=Mg, callback=cb)[0]
            if label:
                print(f'\r      [{label}] CG done: {cnt[0]} iters, {_time.time()-t0:.0f}s' + '\033[K', flush=True)
            return cp.asnumpy(x)
        except Exception as e:
            print(f'    (GPU CG unavailable: {type(e).__name__}: {e} → CPU for the rest of this run)',
                  file=_sys.stderr)
            globals()['_USE_GPU'] = False            # latch off → don't retry the failed GPU path every solve
            cnt[0] = 0; t0 = _time.time(); last[0] = t0
    M = csr_matrix((minv, (np.arange(N), np.arange(N))), shape=(N, N))
    x = cg(A, b, rtol=tol, maxiter=20000, M=M, callback=_mk_cb(A, b, np))[0]
    if label:
        print(f'\r      [{label}] CG done: {cnt[0]} iters, {_time.time()-t0:.0f}s\033[K', flush=True)
    return x

# Per-phase conductivity for the FV solve.  void = 0 always.  Units: ionic/electronic mS/cm, thermal W/m·K.
# PROVENANCE (so these aren't magic numbers) — keep as-is; tighten citations for the manuscript later:
#   • SE 3.0 (ionic)        = Cronau 2022 Li6PS5Cl single-crystal σ_grain (the DEM σ_grain).  ✅ literature.
#   • AM 50 (electronic)    = project σ_AM (NCM811, Trevisanello 2021 — same value the DEM σ_e form uses). ✅
#   • SuperP 1e5 / VGCF 5e5 (electronic) = 100 / 500 S/cm — carbon-black (~10–100 S/cm) & VGCF
#       (~100–1000 S/cm) MATERIAL-conductivity literature BALLPARK, rounded O(magnitude) (⚠ not a single
#       cited digit).  The exact value barely matters: the 200× contrast cap in effective_sigma clamps any
#       carbon ≥200×AM to ~1e4 mS/cm (that conductive = already a perfect bridge), so SuperP vs VGCF differ
#       ONLY by MORPHOLOGY (fibre reach vs aggregate), NOT by 1e5 vs 5e5.
#   • thermal SE 0.7 / AM 4.0 (LPSCl / NMC lit); carbon VGCF 20 / SuperP 5 / PTFE 0.25 (graphitic / binder
#       ballpark).  All thermal numbers are representative, not single-source-cited.
# ⚠ LEGACY/STANDALONE 솔버 — 생산 파이프라인은 이 파일을 import 안 함(step3_sigma.py 가 정본).
#   전자 σ 자릿수 hook 이 정본과 다름: 여기 VGCF 5.0e5/SuperP 1.0e5 mS/cm(=500/100 S/cm) vs
#   step3_sigma.SIGMA_DEFAULT VGCF 100/SuperP 10 S/cm.  둘 다 "문헌 자릿수 hook" 라벨이나 미정합 —
#   ★생산 값은 step3_sigma 를 쓸 것(이 파일 값 인용/복사 금지).  contrast 는 200×AM 로 clamp(:139).
PHASE_SIGMA = {  # per channel; void always 0.  ionic/electronic mS/cm, thermal W/m·K
    'ionic':      {'SE': 3.0, 'AM': 0.0, 'VGCF': 0.0, 'SuperP': 0.0, 'PTFE': 0.0},
    'electronic': {'SE': 0.0, 'AM': 50.0, 'VGCF': 5.0e5, 'SuperP': 1.0e5, 'PTFE': 0.0},
    'thermal':    {'SE': 0.7, 'AM': 4.0, 'VGCF': 20.0, 'SuperP': 5.0, 'PTFE': 0.25},  # all solid conducts
}
PHASE_CODE = {'void': 0, 'AM': 0 - 9, 'SE': 1, 'VGCF': 2, 'SuperP': 3, 'PTFE': 4}  # AM handled separately


def sigma_from_phase(phase, channel, code2name, sigma_map=None):
    """phase: int 3D array of phase codes; code2name: {code: 'SE'/'AM'/...}.
    Returns per-voxel σ (float 3D), 0 where insulating for this channel."""
    sig = (sigma_map or PHASE_SIGMA[channel])
    out = np.zeros(phase.shape, np.float64)
    for code, name in code2name.items():
        out[phase == code] = sig.get(name, 0.0)
    return out


def effective_sigma(sigma, axis=2, dx=1.0, tol=1e-6, return_field=False, label=''):
    """Finite-volume solve of div(σ ∇φ)=0 with φ=1 on the high-`axis` face, φ=0 on
    the low face, no-flux side walls.  σ: 3D float (0 = insulator).  Returns σ_eff
    in the SAME units as σ (geometry cancels)."""
    sigma = np.moveaxis(sigma, axis, 2)            # solve along z
    # Trim leading/trailing z-slices that hold NO conducting cell so the Dirichlet faces sit on
    # the conducting phase's OWN envelope.  Without this, an interstitial phase that never reaches
    # the box floor/ceiling — e.g. SE packed under a rigid AM scaffold that rests on the floor —
    # reads σ_eff=0 even though it percolates internally (its cells touch the top face but not the
    # bottom k=0 face, which the AM occupies).  Internal all-insulator gaps are NOT trimmed, so a
    # genuinely disconnected phase still yields σ_eff=0.  L in σ_eff=I·L/A becomes the conducting
    # span → the slab's true conductivity, undiluted by headspace.
    zmask = (sigma > 0).any(axis=(0, 1))
    if not zmask.any():
        return (0.0, None) if return_field else 0.0
    z0 = int(np.argmax(zmask)); z1 = int(len(zmask) - np.argmax(zmask[::-1]))
    sigma = sigma[:, :, z0:z1]
    if z1 - z0 < 2:                                 # 1-layer-thick conductor → NO top↔bottom z-path:
        return (0.0, None) if return_field else 0.0   #   top & bottom Dirichlet hit the SAME cell → false σ≠0
    cond = sigma > 0
    N = int(cond.sum())
    if N == 0:
        return (0.0, None) if return_field else 0.0
    # Bound the conductivity contrast: electronic mixes carbon (SuperP 1e5 / VGCF 5e5 mS/cm) with
    # AM (50) — a 2000–10000× ratio that makes the FV Laplacian ill-conditioned, so unpreconditioned
    # CG crawls toward maxiter.  A phase already ≥200× its neighbour is a near-perfect bridge, so
    # clamping the max to 200×(smallest nonzero σ) leaves σ_eff unchanged (<0.2%) and the solve fast.
    sigma = np.minimum(sigma, float(sigma[cond].min()) * 200.0)
    nx, ny, nz = sigma.shape
    if label:
        print(f'\r      [{label}] assembling {N:,} nodes…', end='', flush=True)
    gid = -np.ones(sigma.shape, np.int64)
    gid[cond] = np.arange(N)
    s = sigma
    diag = np.zeros(N)
    rows, cols, data = [], [], []

    def harm(a, c):                                 # harmonic-mean face conductance (vectorised)
        out = np.zeros(a.shape)
        m = (a > 0) & (c > 0)
        out[m] = 2.0 * a[m] * c[m] / (a[m] + c[m])
        return out

    # internal edges along each axis (x,y side walls are no-flux ⇒ just the interior pairs)
    for ax in (0, 1, 2):
        sa = [slice(None)] * 3; sa[ax] = slice(0, sigma.shape[ax] - 1)
        sb = [slice(None)] * 3; sb[ax] = slice(1, sigma.shape[ax])
        ga = gid[tuple(sa)].ravel(); gb = gid[tuple(sb)].ravel()
        g = harm(s[tuple(sa)], s[tuple(sb)]).ravel()
        m = (ga >= 0) & (gb >= 0) & (g > 0)
        ga, gb, g = ga[m], gb[m], g[m]
        rows += [ga, gb]; cols += [gb, ga]; data += [-g, -g]
        diag += np.bincount(ga, weights=g, minlength=N) + np.bincount(gb, weights=g, minlength=N)
        #   ↑ bincount is a C-level scatter-add — ~50-100× faster than np.add.at over the ~10⁸ edges of
        #     a thick-electrode grid (np.add.at was the real bottleneck, NOT the GPU/CPU CG solve).

    # z Dirichlet faces (½-cell ⇒ g=2σ): bottom k=0 → φ=0, top k=nz-1 → φ=1
    b = np.zeros(N)
    g0 = gid[:, :, 0].ravel(); s0 = s[:, :, 0].ravel(); m0 = g0 >= 0
    diag += np.bincount(g0[m0], weights=2.0 * s0[m0], minlength=N)
    g1 = gid[:, :, nz - 1].ravel(); s1 = s[:, :, nz - 1].ravel(); m1 = g1 >= 0
    diag += np.bincount(g1[m1], weights=2.0 * s1[m1], minlength=N)
    b += np.bincount(g1[m1], weights=2.0 * s1[m1], minlength=N)

    rows.append(np.arange(N)); cols.append(np.arange(N)); data.append(np.where(diag > 0, diag, 1.0))
    A = csr_matrix((np.concatenate(data), (np.concatenate(rows), np.concatenate(cols))), shape=(N, N))
    if label:
        print(f'\r      [{label}] {N:,} nodes assembled — CG solving on '
              f'{"GPU" if _USE_GPU else "CPU"}…', end='', flush=True)
    phi = _cg_solve(A, b, tol, label=label)        # Jacobi-preconditioned CG (GPU via CuPy if --gpu)

    I = float((2.0 * s0[m0] * phi[g0[m0]]).sum())  # current through the bottom Dirichlet face
    sigma_eff = I * nz / (nx * ny * 1.0)           # σ_eff = I·L/(A·ΔV), ΔV=1, L=nz, A=nx·ny
    if return_field:
        f = np.zeros(sigma.shape); f[cond] = phi
        return sigma_eff, f
    return sigma_eff


def _selftest():
    print('=== voxel effective-conductivity self-test ===')
    n = 24
    # 1) homogeneous slab σ=3 → σ_eff = 3
    hom = np.full((n, n, n), 3.0)
    print(f'  homogeneous σ=3.0           → σ_eff = {effective_sigma(hom):.4f}  (expect 3.000)')
    # 2) two layers in SERIES along z (σ1=2 bottom half, σ2=6 top) → harmonic mean = 3
    ser = np.empty((n, n, n)); ser[:, :, :n // 2] = 2.0; ser[:, :, n // 2:] = 6.0
    print(f'  series 2|6 (⊥ current)      → σ_eff = {effective_sigma(ser):.4f}  (expect 3.000 harmonic)')
    # 3) two columns in PARALLEL (σ1=2, σ2=6 split in x) → arithmetic mean = 4
    par = np.empty((n, n, n)); par[:n // 2] = 2.0; par[n // 2:] = 6.0
    print(f'  parallel 2|6 (∥ current)    → σ_eff = {effective_sigma(par):.4f}  (expect 4.000 arithmetic)')
    # 4) insulating slab blocking the path → σ_eff = 0 (no percolation)
    blk = np.full((n, n, n), 3.0); blk[:, :, n // 2] = 0.0
    print(f'  blocked layer (no percol.)  → σ_eff = {effective_sigma(blk):.4f}  (expect 0.000)')


# ── real-data path: voxelise the MPM phase cloud (+ AM scaffold) and run all channels ──
def _vc():
    import importlib.util, os
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'viz_mpm_continuum.py')
    spec = importlib.util.spec_from_file_location('viz_mpm_continuum', p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def _densify_fibres(p, fid, h):
    """Fill the gaps between consecutive points of each fibre (same id, kept in centreline order) with
    interpolated points spaced ≤ h, so a thin sub-voxel fibre rasterises to a CONNECTED voxel thread
    instead of a dotted line (the VGCF/PTFE centrelines are seeded ~1.5 µm apart ≫ a 0.5 µm cell, so
    the bare point cloud breaks into disconnected dots and the fibre stops conducting).
    PRECONDITION: each fibre's points are CONSECUTIVE in array order along the centreline (true for
    mpm3d --save-fibre — seed_fibres emits one ordered line per id).  Do NOT pass a reshuffled cloud or
    a Voronoi-style id (e.g. se_id); stable-sort only groups by id, it does NOT re-order within a fibre."""
    if len(p) < 2:
        return p
    o = np.argsort(fid, kind='stable'); p, fid = p[o], fid[o]
    same = fid[1:] == fid[:-1]
    a, b = p[:-1][same], p[1:][same]
    if len(a) == 0:
        return p
    seg = b - a
    nfill = np.ceil(np.linalg.norm(seg, axis=1) / max(h, 1e-9)).astype(np.int64)
    out = [p]
    for k in range(1, int(nfill.max()) if len(nfill) else 0):     # interior fill points along each segment
        msk = nfill > k
        if not msk.any():
            break
        out.append(a[msk] + (k / nfill[msk].astype(np.float64))[:, None] * seg[msk])
    return np.vstack(out)


def voxelize_phase(se_pts, phase, scaffold, n_vox, top=None, porosity=None, se_close=False, fibre=None):
    """Per-phase presence grids on the vc grid: AM from the scaffold spheres, SE/VGCF/SuperP/PTFE
    from the MPM point cloud (phase 1/2/3/4).  Returns ({name: bool grid}, h).
    porosity (the MPM void fraction, e.g. 0.174): if given, SE fills its TRUE fraction as the
    densest CONTIGUOUS region (target_porosity) instead of "≥1 point/cell".  Essential for the
    ionic channel — the SE point cloud is NOT space-filling, so "≥1 point/cell" thins out and
    DISCONNECTS as n_vox rises (σ_ionic → 0 spuriously), while AM (spheres) and the AM-carried
    electronic/thermal channels stay fine.  porosity → resolution-stable, percolating SE.
    se_close (default OFF — opt-in): morphological-close the SE mask by the point spacing s_MPM (in
    voxels), restricted to free space, to bridge fragile near-percolation necks.  NOT needed for a
    DENSE cloud: with --porosity alone the dense-synthetic σ_ionic is 1.894/1.900/1.904 across
    128/192/256 = the analytic space-filling ground truth (1.90), and closing slightly OVER-fills
    (1.80, noisier).  Use it only as a rescue when the real near-threshold SE still scatters."""
    vc = _vc()
    t, c, r = vc.load_am(scaffold)                         # AM spheres (box units)
    se1 = se_pts[phase == 1]                               # true SE points → SE occupancy
    if top is None:
        top = float(se_pts[:, 2].max()) + 0.01
    am_p, am_s, se_mask, h = vc.voxelize(se1, t, c, r, n_vox, top, 1, False, target_porosity=porosity)
    nx, ny, nz = se_mask.shape
    SW0, FLOOR = vc.SW[0], vc.FLOOR
    if se_close and len(se1) > 1000:                       # reconnect SE necks (res-stable)
        from scipy import ndimage as ndi
        s_mpm = (float(np.prod(se1.max(0) - se1.min(0))) / len(se1)) ** (1.0 / 3.0)
        r_vox = max(1, int(round(s_mpm / h)))
        se_mask = ndi.binary_closing(se_mask, iterations=r_vox) & ~(am_p | am_s)
    pres = {'AM': am_p | am_s, 'SE': se_mask}
    for code, name in ((2, 'VGCF'), (3, 'SuperP'), (4, 'PTFE')):
        g = np.zeros((nx, ny, nz), bool)
        m = phase == code
        if m.any():
            p = se_pts[m]
            if fibre is not None and code in (2, 4):     # VGCF/PTFE are 1-D fibres → fill to a thread
                p = _densify_fibres(p, np.asarray(fibre)[m], h)
            ix = np.clip(((p[:, 0] - SW0) / h).astype(np.int64), 0, nx - 1)
            iy = np.clip(((p[:, 1] - SW0) / h).astype(np.int64), 0, ny - 1)
            iz = np.clip(((p[:, 2] - FLOOR) / h).astype(np.int64), 0, nz - 1)
            g[ix, iy, iz] = True
        pres[name] = g
    return pres, h


def se_contact_network(se_pts, se_id, n_vox, thickness_um, sigma_grain=3.0, top=None):
    """MPM SE-SE PLASTIC contact-network σ_ionic — the per-particle (NOT fused) ionic solve that
    recovers the constriction the merged-voxel FV misses (which read σ_contact-free).

    Each SE point carries its originating DEM-SE-particle id (mpm3d --save-se-id, Voronoi-tagged).
    Voxelise SE keeping the id (majority per cell), then between every pair of TOUCHING particles
    accumulate the real plastic CONTACT AREA a = (#adjacent cell-faces with different ids)·h_um².
    Build a Holm resistor network — constriction R = 1/(2·σ·r_c), r_c = √(a/π) (Holm 1967, the same
    law as the DEM Kirchhoff solver) — and solve top↔bottom.

    ⚠ EXPERIMENTAL — currently OVER-COUNTS the contact area.  The space-filling Voronoi partition makes
    every pair of neighbouring particles share their FULL mutual facet, so `a` is the Voronoi facet area,
    NOT the small plastic contact disk → r_c too large → constriction too small → σ_ionic comes out ABOVE
    even σ_contact-free (≈0.88 vs the fused-FV 0.25 and the DEM full 0.044 on AMS_S1-class cases).  A fix
    needs interpenetration/overlap-based contact area (DEM-style δ/R* plastic film), and even then the SE
    neck (⟨A_hop⟩≈0.065 µm², bottleneck 0.0025) is SUB-VOXEL at any practical n_vox → not DEM-grade.
    → Production σ_ionic stays the DEM network (frame[5]: the contact network owns the constriction); this
    mode is at best a coarse UPPER bound + a contact-area diagnostic, not an independent σ_ionic.

    Returns dict: σ_ionic (mS/cm, Voronoi-contact, OVER-COUNTED), n_particles, n_contacts, A_SE-SE total &
    mean contact area (µm²; also over-counted = Voronoi facets, not plastic contacts)."""
    from scipy.sparse import csr_matrix as _csr
    vc = _vc()
    SW0, FLOOR, WIDTH = vc.SW[0], vc.FLOOR, vc.SW[1] - vc.SW[0]
    keep = se_id >= 0
    P, sid = se_pts[keep], se_id[keep].astype(np.int64)
    if len(P) < 2:
        return None
    if top is None:
        top = float(P[:, 2].max()) + 1e-9
    h = WIDTH / n_vox
    nz = max(int(np.ceil((top - FLOOR) / h)), 2)
    um_box = thickness_um / max(float(P[:, 2].max()) - FLOOR, 1e-9)   # µm per box unit (from known T)
    h_um = h * um_box
    from scipy import ndimage as _ndi
    from scipy.spatial import cKDTree as _ckd
    ix = np.clip(((P[:, 0] - SW0) / h).astype(np.int64), 0, n_vox - 1)
    iy = np.clip(((P[:, 1] - SW0) / h).astype(np.int64), 0, n_vox - 1)
    iz = np.clip(((P[:, 2] - FLOOR) / h).astype(np.int64), 0, nz - 1)
    # SE particle centroids (deformed-particle centre = mean of its points).
    mx = int(sid.max()) + 1
    csum = np.zeros((mx, 3)); ccnt = np.zeros(mx)
    np.add.at(csum, sid, P); np.add.at(ccnt, sid, 1.0)
    cid = np.nonzero(ccnt > 0)[0]; cen = csum[cid] / ccnt[cid, None]
    # SE occupancy (all points) → CLOSE the sub-(point-spacing) gaps so the SE region is space-filling,
    # then assign every SE cell to its NEAREST centroid (Voronoi).  This gives a COMPLETE, resolution-
    # stable particle partition: the boundary between two particles' territories = their plastic contact
    # face (vs the bare point cloud, whose patchy interfaces shrink the contact area as n_vox rises).
    occ = np.zeros((n_vox, n_vox, nz), bool); occ[ix, iy, iz] = True
    s_mpm = (float(np.prod(P.max(0) - P.min(0))) / len(P)) ** (1.0 / 3.0)   # SE point spacing (box)
    rec_nvox = int(WIDTH / s_mpm)                                    # the critically-sampled resolution
    occ = _ndi.binary_closing(occ, iterations=max(1, int(np.ceil(s_mpm / h))))
    sx, sy, sz = np.nonzero(occ)
    cc = np.column_stack([(sx + 0.5) * h + SW0, (sy + 0.5) * h + SW0, (sz + 0.5) * h + FLOOR])
    idg = np.full((n_vox, n_vox, nz), -1, np.int64)
    idg[sx, sy, sz] = cid[_ckd(cen).query(cc, k=1)[1]]
    # contact faces: adjacent occupied cells with DIFFERENT ids → one h_um² face for that particle pair
    K = int(sid.max()) + 1
    keys = []
    for ax in (0, 1, 2):
        a = np.moveaxis(idg, ax, 0)
        m = (a[:-1] >= 0) & (a[1:] >= 0) & (a[:-1] != a[1:])
        u, v = a[:-1][m], a[1:][m]
        keys.append(np.minimum(u, v) * K + np.maximum(u, v))
    keys = np.concatenate(keys) if keys else np.array([], np.int64)
    parts = np.unique(idg[idg >= 0]); npart = len(parts)
    if keys.size == 0 or npart < 2:
        return {'sigma_ionic_mScm': 0.0, 'n_particles': int(npart), 'n_contacts': 0,
                'A_SE_SE_total_um2': 0.0, 'A_hop_mean_um2': 0.0, 'note': 'no SE-SE contacts'}
    uk, ck = np.unique(keys, return_counts=True)                     # uk = lo·K+hi, ck = #faces
    pa, pb = uk // K, uk % K
    a_um2 = ck * (h_um * h_um)                                       # plastic contact area per pair (µm²)
    rmap = np.full(int(parts.max()) + 1, -1, np.int64); rmap[parts] = np.arange(npart)
    pai, pbi = rmap[pa], rmap[pb]
    # particle z-extent → top/bottom electrode membership (vectorised)
    occ = idg >= 0
    pv = rmap[idg[occ]]
    pz = np.broadcast_to(np.arange(nz)[None, None, :], idg.shape)[occ]
    zmn = np.full(npart, nz); zmx = np.full(npart, -1)
    np.minimum.at(zmn, pv, pz); np.maximum.at(zmx, pv, pz)
    z_lo, z_hi = int(pz.min()), int(pz.max())                        # electrodes = the actual SE extent,
    bottom, top_m = zmn <= z_lo, zmx >= z_hi                         # not the grid bounds (robust)
    base = {'n_particles': int(npart), 'n_contacts': int(len(uk)),
            'A_SE_SE_total_um2': float(a_um2.sum()), 'A_hop_mean_um2': float(a_um2.mean()),
            'recommended_n_vox': rec_nvox}
    if z_hi - z_lo < 1 or not bottom.any() or not top_m.any():       # 1-layer SE → rails short / no z-path
        return {**base, 'sigma_ionic_mScm': 0.0,
                'note': 'SE single z-layer' if z_hi - z_lo < 1 else 'no top↔bottom percolation'}
    # Holm constriction conductance g = 2·r_c (σ=1 normalised; µm), r_c = √(a/π).  Rail: top→V=1,
    # bottom→V=0 with a stiff g_big.  σ_eff[mS/cm] = σ_grain · G_norm[µm] · L[µm] / A[µm²].
    g = 2.0 * np.sqrt(a_um2 / np.pi)
    diag = np.zeros(npart)
    np.add.at(diag, pai, g); np.add.at(diag, pbi, g)
    g_big = 1.0e3 * float(g.max())
    diag[bottom] += g_big; diag[top_m] += g_big
    rows = np.concatenate([pai, pbi, np.arange(npart)])
    cols = np.concatenate([pbi, pai, np.arange(npart)])
    data = np.concatenate([-g, -g, np.where(diag > 0, diag, 1.0)])
    A = _csr((data, (rows, cols)), shape=(npart, npart))
    b = np.zeros(npart); b[top_m] += g_big * 1.0
    V = _cg_solve(A, b, 1e-8)                                        # GPU (CuPy) if --gpu, else CPU
    I = g_big * float(V[bottom].sum())                               # current into the V=0 rail (ΔV=1)
    sigma = sigma_grain * I * thickness_um / (n_vox * h_um) ** 2
    return {**base, 'sigma_ionic_mScm': float(sigma)}


def sigma_grid(pres, channel, drop_carbon=False):
    """Per-cell σ = MAX σ over the phases present (a sub-grid carbon thread makes its cells
    conduct; for ionic the SE wins; void = 0).
    drop_carbon = the WITHOUT-CBD baseline:
      • electronic / thermal: carbon stops conducting (σ_VGCF/SuperP → 0) → reveals the dead AM
        the carbon was BRIDGING → gain = σ_with/σ_without > 1 is the CBD payoff.
      • ionic: NO-OP (with == without, gain 1.0×).  Carbon never conducts ions, and the carbon/
        PTFE cells block SE percolation EQUALLY in both columns, so a single-structure σ-toggle
        cannot isolate the blocking.  (A carbon→SE "unblock" was tried and removed: the patchy
        carbon cloud extends/distorts the conduction envelope → spurious gains, e.g. 7.6× with
        σ_without < σ_with, which is physically impossible.)  Measure the CBD ionic blocking via
        the STRUCTURAL comparison instead — voxel a no-CBD run and a +CBD run and compare."""
    sig = dict(PHASE_SIGMA[channel])
    if channel == 'electronic' and _SIGMA_AM_E is not None:
        sig['AM'] = _SIGMA_AM_E                                 # --sigma-am-e: AM e-σ override (0 → carbon-only)
    if drop_carbon and channel != 'ionic':
        sig['VGCF'] = 0.0; sig['SuperP'] = 0.0                  # carbon stops conducting (e/thermal)
    out = np.zeros(next(iter(pres.values())).shape, np.float64)
    for name, g in pres.items():
        s = sig.get(name, 0.0)
        if s > 0:
            np.maximum(out, np.where(g, s, 0.0), out=out)
    return out


def _main():
    import argparse
    ap = argparse.ArgumentParser(description='Stage-2 voxel σ on the MPM phase grid (σ_e/σ_i/κ, ±CBD)')
    ap.add_argument('--se', required=True, help='se_carbon.npy — all MPM points (box units)')
    ap.add_argument('--phase', default=None,
                    help='phase_carbon.npy — per-point phase (1 SE/2 VGCF/3 SuperP/4 PTFE).  '
                         'OMIT for an SE+AM-only (no-CBD) dump → all points treated as SE, so you '
                         'can voxel the plain run and compare σ to the CBD run (rigorous CBD effect).')
    ap.add_argument('--scaffold', default=None, help='am_scaffold.csv — AM spheres (FV mode only)')
    ap.add_argument('--n-vox', type=int, default=128)
    ap.add_argument('--porosity', type=float, default=None,
                    help='MPM void fraction (e.g. 0.174 from metrics_carbon.json).  STRONGLY '
                         'recommended: fills SE to its true fraction as a CONTIGUOUS region so the '
                         'ionic channel is resolution-stable (without it the SE point cloud thins '
                         'out and σ_ionic spuriously → 0 as n_vox rises).')
    ap.add_argument('--channel', default='all', choices=['ionic', 'electronic', 'thermal', 'all'])
    ap.add_argument('--fibre', default=None,
                    help='fibre_carbon.npy (mpm3d --save-fibre): per-point fibre id.  When given, VGCF/PTFE '
                         'fibres are filled along their centreline into CONNECTED voxel threads (the bare '
                         'point cloud is ~1.5µm-spaced ≫ cell → a dotted line that stops conducting).  '
                         'Use for a FAIR electronic SuperP-vs-VGCF comparison.')
    ap.add_argument('--se-close', action='store_true',
                    help='OPT-IN: morphologically close the SE necks (default off).  --porosity '
                         'alone is already resolution-stable for a dense cloud (= ground truth); '
                         'use --se-close only as a rescue if the near-threshold SE still scatters.')
    ap.add_argument('--se-id', default=None,
                    help='se_id.npy (mpm3d --save-se-id): per-point SE PARTICLE id → run the SE-SE '
                         'PLASTIC CONTACT-NETWORK σ_ionic (per-particle Holm constriction, the value '
                         'the fused-voxel FV misses) instead of the FV.  Needs --thickness-um.')
    ap.add_argument('--thickness-um', type=float, default=None,
                    help='electrode thickness in µm (DEM/MPM, e.g. 170.4) — sets the box→µm scale for '
                         'the --se-id contact-network absolute σ_ionic + contact areas.')
    ap.add_argument('--gpu', action='store_true',
                    help='run the CG solve on the GPU via CuPy (big speedup for thick-electrode grids, '
                         'e.g. 256×256×700; the solver is CPU/scipy by default).  Auto-falls back to CPU '
                         'if CuPy is not installed.')
    ap.add_argument('--sigma-am-e', type=float, default=None,
                    help='override the AM electronic σ (mS/cm; default 50 = NCM811, Trevisanello).  Set 0 to '
                         'make AM a NON-conducting obstacle so CARBON is the SOLE e-path → isolates the '
                         'carbon-only percolation (the literature 1D-VGCF vs 0D-SuperP regime: which carbon '
                         'morphology percolates at a given loading when the AM is not the conductor).')
    a = ap.parse_args()
    global _USE_GPU; _USE_GPU = a.gpu
    global _SIGMA_AM_E; _SIGMA_AM_E = a.sigma_am_e
    if a.se_id:                                                      # ── SE plastic contact-network mode ──
        if a.thickness_um is None:
            raise SystemExit('--se-id needs --thickness-um (electrode thickness, e.g. 170.4)')
        pts = np.load(a.se).astype(np.float64); se_id = np.load(a.se_id)
        if len(pts) != len(se_id):
            raise SystemExit(f'se {len(pts)} != se_id {len(se_id)} — mismatched run')
        o = se_contact_network(pts, se_id, a.n_vox, a.thickness_um, sigma_grain=PHASE_SIGMA['ionic']['SE'])
        if o is None:
            raise SystemExit('too few SE particle points')
        print(f'\n  SE-SE PLASTIC contact-network σ_ionic (per-particle Holm constriction, MPM deformed contacts)')
        print(f'  particles {o["n_particles"]:,}  contacts {o["n_contacts"]:,}  '
              f'(recommended n_vox ≈ {o["recommended_n_vox"]}, you used {a.n_vox})')
        print(f'  A_SE-SE total = {o["A_SE_SE_total_um2"]:.0f} µm²   ⟨A_hop⟩ = {o["A_hop_mean_um2"]:.4f} µm²'
              f'   (compare to DEM dashboard A_SE-SE / ⟨A_hop⟩)')
        if o.get('note'):
            print(f'  ⚠ {o["note"]} → σ_ionic = 0')
        print(f'  σ_ionic (Voronoi-contact, mS/cm) = {o["sigma_ionic_mScm"]:.4f}   '
              f'⚠ OVER-COUNTS (Voronoi facet ≠ plastic contact → > σ_contact-free, ≫ DEM σ_full).')
        print(f'    ⇒ production σ_ionic = DEM network (Holm); this mode = upper-bound + contact-area '
              f'diagnostic only.  A_SE-SE/⟨A_hop⟩ above are likewise Voronoi facets, not plastic contacts.')
        return
    if not a.scaffold:
        raise SystemExit('FV mode needs --scaffold am_scaffold.csv (or pass --se-id for contact-network mode)')
    pts = np.load(a.se).astype(np.float64)
    phase = np.load(a.phase) if a.phase else np.ones(len(pts), dtype=np.int64)  # no --phase → all SE
    if len(pts) != len(phase):
        raise SystemExit(f'se {len(pts)} != phase {len(phase)} — mismatched run (se_dump overwritten?)')
    u, cc = np.unique(phase, return_counts=True)
    print('phase counts:', {int(p): int(n) for p, n in zip(u, cc)})
    if a.porosity is None:
        print('  ⚠ no --porosity → SE = "≥1 point/cell" (NOT space-filling); σ_ionic disconnects'
              ' as n_vox rises.  Pass --porosity <MPM void frac> for a resolution-stable ionic σ.')
    import time as _t
    _tv = _t.time(); print('  voxelising…', end='', flush=True)
    _fib = np.load(a.fibre) if a.fibre else None
    pres, h = voxelize_phase(pts, phase, a.scaffold, a.n_vox, porosity=a.porosity,
                             se_close=a.se_close, fibre=_fib)
    print(f'\r  voxelised {next(iter(pres.values())).shape} in {_t.time()-_tv:.0f}s — '
          f'cells/phase: {{{", ".join(f"{k}:{int(v.sum())}" for k, v in pres.items())}}}', flush=True)
    chans = ['electronic', 'ionic', 'thermal'] if a.channel == 'all' else [a.channel]
    units = {'electronic': 'mS/cm', 'ionic': 'mS/cm', 'thermal': 'W/m·K'}
    print(f'\n  {"channel":<11}{"WITHOUT CBD":>14}{"WITH CBD":>14}{"gain":>9}'
          f"   (solving on {'GPU' if _USE_GPU else 'CPU'})", flush=True)
    for ch in chans:
        _tc = _t.time()
        # 2 FV solves per channel (±CBD), each with live [assemble → CG iter] progress on stderr/line.
        s_wout = effective_sigma(sigma_grid(pres, ch, drop_carbon=True), label=f'{ch} WITHOUT-CBD')
        s_with = effective_sigma(sigma_grid(pres, ch, drop_carbon=False), label=f'{ch} WITH-CBD')
        gain = f'{s_with / s_wout:>6.1f}x' if s_wout > 1e-9 else '  None→'   # σ_e=None revived
        print(f'\r  {ch:<11}{s_wout:>13.4g} {s_with:>13.4g}  {gain:>8}  ({units[ch]})  '
              f'[{_t.time()-_tc:.0f}s]' + ' ' * 16, flush=True)
    print('\n  electronic: WITHOUT = carbon σ off (dead AM exposed), WITH = carbon bridges →')
    print('              gain = σ_with/σ_without > 1 is the CBD electronic payoff.')
    print('  ionic: WITHOUT == WITH (gain 1.0×) BY DESIGN — carbon blocks SE equally in both, a')
    print('         single-structure toggle cannot isolate it.  The printed σ_ionic IS the real')
    print('         (carbon-blocked) value; use --porosity + n_vox≥192 for a stable reading.')
    print('  ⇒ CBD ionic BLOCKING = voxel a no-CBD run vs the +CBD run and compare σ_ionic')
    print('    (that also captures the SE/AM packing rearrangement a σ-toggle never could).')


if __name__ == '__main__':
    import sys
    (_main() if '--se' in sys.argv else _selftest())
