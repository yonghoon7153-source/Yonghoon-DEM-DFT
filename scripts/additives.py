#!/usr/bin/env python3
"""Seed conductive additives (VGCF fibres, Super P / Super C carbon black, PTFE
binder) as EXTRA MPM material phases — counts derived from the electrode recipe,
never hard-coded.

Why this works cheaply where LIGGGHTS can't: the discrete DEM would need millions
of nano objects (Super P ~40 nm, VGCF Ø~0.15 µm) → impossible.  The MPM is a
grid/continuum whose cost is resolution-bound, and it already carries a PER-POINT
material (µ, λ, σ_y) — so an additive is just "more material points with different
constants", no kernel change.  Nano features stay sub-grid → they enter as a
HOMOGENISED phase (a fibre = a chain of points along its axis; carbon black = a
small blob), evenly distributed through the box (optionally avoiding the fixed AM).

Recipe → count chain (densities g/cm³, literature):
  AM(NMC811) 4.80 · SE(Li6PS5Cl) 2.00 · VGCF 2.00 · SuperP 1.90 · PTFE 2.20
  wt%  --(/ρ)-->  vol%  --(× solid_vol)-->  phase volume  --(/ vol-per-object)-->  N
VGCF Ø≈0.15 µm, L≈10 µm (aspect ≈67);  SuperP aggregate ≈0.2 µm.

  python3 scripts/additives.py            # demo: the two production recipes
"""
from __future__ import annotations
import argparse
import numpy as np

DENS = {'AM': 4.80, 'SE': 2.00, 'VGCF': 2.00, 'SuperP': 1.90, 'PTFE': 2.20, 'SDCP': 1.30,  # g/cm³ (SDCP 1.3 = ⚠PROXY from generic PEDOT web-lit — REPLACE with the user's manuscript value)
        'SWCNT': 1.35}  # theoretical (10,10)-class SWCNT ≈1.33; bundles 1.3–1.5 (geometry-derived lit
#   range) → 1.35 mid-proxy.  At the koo2026 loading (0.2 wt%) the volume is <0.1 vol% and add_pvs
#   volume-pinning makes porosity insensitive to this value — count-scale only.
#   SE=2.00 = PROJECT CONVENTION (matches porosity_physics_regression RHO_SE + grade_engine);
#   real Li6PS5Cl crystallographic ≈ 1.85–1.88 (2.0 is the project's slightly-high standard).
#   Aligned 2026-06-30 (was 1.64, an out-of-band low value) so the zip additive counts use the
#   SAME SE density as the closed porosity model. ⚠ grade_engine.py:1217 still uses 1.85 (separate
#   composite-density calc) — flagged for the user; not changed here.
PHASE = {'SE': 1, 'AM': 0, 'VGCF': 2, 'SuperP': 3, 'PTFE': 4, 'SDCP': 5, 'SWCNT': 6}   # save-phase codes
# default geometry (µm)
VGCF_D, VGCF_L = 0.15, 10.0      # VGCF fibre Ø, length (Showa Denko VGCF-H; aspect ~67)
SP_D           = 0.20            # Super P / Super C carbon-black aggregate (sphere, particulate)
PTFE_D, PTFE_L = 0.25, 40.0      # PTFE FIBRIL Ø, length — dry-process hot-roll fibrillation makes long
                                 # thin threads (branch to 10s nm) spanning tens of NMC; LONGER + HIGHER
                                 # aspect (AR≈160) than VGCF (AR≈67) → reads as the spanning binder web,
                                 # not a short rod.  Soft binder FIBRE (RSC D5EE03240G; Front. Energy 2023.1336344)
SDCP_D = 0.30                    # SDCP in-electrode particle Ø (µm) — manuscript Fig S3 (0.2-0.5µm dispersed;
                                 # as-made ~3µm S2, milled down by the dry process)
SDCP_AGG_D = 3.0                 # SDCP AS-MADE agglomerate Ø (µm) — manuscript Fig S2 (~3µm particles before
                                 # milling).  Low-shear mixing (hand-mix) has no milling energy → these survive
                                 # (seeded via seed_sdcp agg_d); high-shear (ball-mill/Thinky) mills → S3 singles.
SDCP_AGG_PACK = 0.64             # ASSUMED internal packing of the as-made agglomerate (RCP-like) — §F1 hook,
                                 # NOT anchored: S2 anchors the ~3µm SIZE only; a denser (even fully solid,
                                 # 1.0) precipitation-grown particle is not excluded.  Sets n_agg = pack·
                                 # (agg_d/d)³ and the member-ball radius in seed_sdcp.
SDCP_SHELL = 0.20                # legacy coat-shell (µm) — coat-variant option only; manuscript default = PARTICLE
# ── A14 SWCNT surface-conformal sheath (#275 koo2026, Joule 10:102392) ─────────────────
SWCNT_D = 0.002                  # single-tube outer Ø ≈ 2 nm (koo2026, OCSiAl SWCNT) — DEEPLY sub-voxel;
                                 # the tube Ø is a MATERIAL datum, the bundle scale below is representation.
SWCNT_BUND_D = 0.05              # vein/bundle Ø used for OBJECT COUNTING + viewer scale (µm).  §F1: koo2026
                                 # Fig 1D shows "vein-like" SWCNT bundles wrapping NCMA but publishes no
                                 # bundle-Ø number → 50 nm is an UN-ANCHORED representation scale.  The
                                 # recipe volume is add_pvs-pinned downstream, so this sets point counts
                                 # only — NEVER porosity.
SWCNT_SEG_L = 1.0                # µm of vein per counted object (same representation-budget role).
SWCNT_SHELL = 0.08               # seeded sheath skin thickness (µm).  Real few-layer sheath ~2–10 nm =
                                 # OUR INFERENCE from the published tube Ø 2 nm (koo2026 publishes NO
                                 # sheath-thickness number — §F1: do not cite "2-10nm (Koo)").  Sub-voxel;
                                 # same 1-voxel-overstatement class as seed_coat, volume-pinned → honest.


def vol_fracs(wt: dict) -> dict:
    """wt% (any subset of AM/SE/VGCF/SuperP/PTFE) → volume fractions (sum 1)."""
    v = {k: wt[k] / DENS[k] for k in wt if wt.get(k, 0) > 0}
    tot = sum(v.values())
    return {k: vv / tot for k, vv in v.items()}


def recipe_counts(wt: dict, solid_vol_um3: float, vgcf_d=VGCF_D, vgcf_l=VGCF_L,
                  sp_d=SP_D, ptfe_d=PTFE_D, ptfe_l=PTFE_L) -> dict:
    """Number of VGCF fibres / SuperP spheres / PTFE fibrils for a recipe + solid volume."""
    vf = vol_fracs(wt)
    out = {'vol_fracs': vf}
    v_fib = np.pi * (vgcf_d / 2) ** 2 * vgcf_l                      # µm³ per VGCF fibre
    v_sp = np.pi / 6 * sp_d ** 3                                    # Super P sphere
    v_pt = np.pi * (ptfe_d / 2) ** 2 * ptfe_l                       # PTFE fibril (fibre, not sphere)
    for ph, vobj in (('VGCF', v_fib), ('SuperP', v_sp), ('PTFE', v_pt)):
        if vf.get(ph, 0) > 0:
            out[ph] = {'vol_um3': vf[ph] * solid_vol_um3,
                       'n': int(round(vf[ph] * solid_vol_um3 / vobj)),
                       'vol_per_obj_um3': vobj}
    return out


def additive_wt(wt: dict) -> dict:
    """Pull just the conductive-additive wt% from a recipe dict, ignoring AM/SE.  So
    'AM:SE:VGCF=72:27:1' and 'VGCF=1' both give {'VGCF': 1.0} — the AM:SE in the recipe is
    NOT used (the real scaffold sets it; see recipe_counts_real)."""
    return {k: float(wt[k]) for k in ('VGCF', 'SuperP', 'PTFE', 'SDCP', 'SWCNT') if wt.get(k, 0) > 0}


def recipe_counts_real(add_wt: dict, am_vol_um3: float, se_vol_um3: float, vgcf_d=VGCF_D,
                       vgcf_l=VGCF_L, sp_d=SP_D, ptfe_d=PTFE_D, ptfe_l=PTFE_L) -> dict:
    """Additive counts where each additive is `wt%` of the REAL electrode — AM/SE masses come
    from the actual scaffold (am_vol·ρ_AM + se_vol·ρ_SE), NOT a hardcoded recipe ratio.

    Each additive a is wt_a% of the TOTAL (AM+SE+additives):
        M_tot = M_solid / (1 − Σwt/100),   M_a = wt_a/100 · M_tot,   V_a = M_a / ρ_a.
    (ρ cancels into consistent units, so masses ∝ vol·ρ are fine to mix with µm³ volumes.)
    Returns the realised electrode wt%/vol% so the run can report the true composition."""
    M_AM = am_vol_um3 * DENS['AM']
    M_SE = se_vol_um3 * DENS['SE']
    M_solid = M_AM + M_SE
    sw = sum(add_wt.values())
    M_tot = M_solid / max(1.0 - sw / 100.0, 1e-6)
    solid_vol = am_vol_um3 + se_vol_um3
    out = {'mode': 'real_scaffold_wt',
           'am_wt_pct': round(100.0 * M_AM / M_tot, 2), 'se_wt_pct': round(100.0 * M_SE / M_tot, 2)}
    v_obj = {'VGCF': np.pi * (vgcf_d / 2) ** 2 * vgcf_l, 'SuperP': np.pi / 6 * sp_d ** 3,
             'PTFE': np.pi * (ptfe_d / 2) ** 2 * ptfe_l,
             'SDCP': np.pi / 6 * SDCP_D ** 3,  # SDCP particle (manuscript S3) — n = particle count; volume add_pvs-pinned
             'SWCNT': np.pi / 4 * SWCNT_BUND_D ** 2 * SWCNT_SEG_L}  # A14: 1µm vein-bundle segment (representation
    #   budget — real single tubes at Ø2nm would give billions of objects; volume add_pvs-pinned either way)
    for a, w in add_wt.items():
        V_a = (w / 100.0) * M_tot / DENS[a]                            # µm³ of additive a
        out[a] = {'wt_pct': w, 'vol_um3': V_a, 'n': int(round(V_a / v_obj[a])),
                  'vol_per_obj_um3': v_obj[a], 'vol_pct_of_solid': round(100.0 * V_a / solid_vol, 3)}
    return out


def seed_coat(n, box_um, dx_um, rng, am=None, shell_um=0.20, surface_frac=1.0,
              in_am=None, return_ids=False):
    """CONFORMAL COAT seeding (A4 coat regime): n points in a thin shell ON the AM sphere
    surfaces — the anchored film morphology (SDCP self-doped binder: sulfonate chemisorbs
    into the Li-O layer; E_bind ⚠INVALID(wrong-monomer 2026-07-10, DFT recompute pending — do NOT cite −4.8 eV); also SuperP thinky
    dry-coat coat_block).  Area-weighted across AM (big spheres get ∝R² points);
    UNIFORM-on-sphere dirs + per-sphere random cap axis (contiguous patch when
    surface_frac<1).
    surface_frac < 1 → each sphere coated only on a random spherical CAP of that fractional
    area (patchy/partial coating).  Radial offset uniform in [0, shell_um] OUTSIDE the
    surface (film thickness ≈ shell; sub-voxel reality documented — 1-voxel overstatement,
    volume-pinned by add_pvs downstream so porosity stays honest).  Points buried inside a
    NEIGHBOURING AM (scaffold contact overlaps, ~6%%) or outside the box are DROPPED — the
    fibre-seeding convention; add_pvs renormalises the recipe volume over the survivors.
    am = (centres, radii) in the SEED-BOX frame (same convention as seed_carbon_black)."""
    if am is None or len(am[0]) == 0:                        # no AM → uniform fallback (degenerate)
        (Lx, Ly, Lz) = box_um
        P = np.column_stack([rng.uniform(0, Lx, n), rng.uniform(0, Ly, n), rng.uniform(0, Lz, n)])
        return (P.astype(np.float32), np.zeros(n, np.int32)) if return_ids else P.astype(np.float32)
    C, R = np.asarray(am[0], np.float64), np.asarray(am[1], np.float64)
    w = R ** 2; w /= w.sum()                                 # per-sphere share ∝ surface area
    sph = rng.choice(len(C), n, p=w)                         # sphere index per point
    # even unit dirs: golden-angle sequence per point + per-sphere random axis for the cap
    k = rng.uniform(0, 1, n)
    z = 1.0 - 2.0 * k                                        # uniform in cos → uniform on sphere
    if surface_frac < 1.0:                                   # spherical cap of fractional area f:
        z = 1.0 - 2.0 * surface_frac * k                     #   cos(θ) ∈ [1−2f, 1] about the cap axis
    phi = rng.uniform(0, 2 * np.pi, n)
    rr = np.sqrt(np.maximum(0.0, 1.0 - z * z))
    d_loc = np.column_stack([rr * np.cos(phi), rr * np.sin(phi), z])
    # rotate each sphere's cap axis to a random direction (per-sphere fixed → contiguous patch)
    ax = rng.normal(size=(len(C), 3)); ax /= np.linalg.norm(ax, axis=1, keepdims=True) + 1e-12
    a = ax[sph]
    # rotate local +z to a: use Rodrigues via orthonormal frame
    t = np.cross(np.broadcast_to([0.0, 0.0, 1.0], a.shape), a)
    tn = np.linalg.norm(t, axis=1, keepdims=True)
    ok = tn[:, 0] > 1e-9
    t = np.where(ok[:, None], t / np.where(tn > 1e-9, tn, 1.0), [1.0, 0.0, 0.0])
    cosang = a[:, 2:3]
    d = d_loc * cosang + np.cross(t, d_loc) * np.sqrt(np.maximum(1 - cosang ** 2, 0)) \
        + t * (t * d_loc).sum(1, keepdims=True) * (1 - cosang)
    d[~ok] = d_loc[~ok] * np.sign(a[~ok, 2:3] + 1e-12)       # a ≈ ±z: no rotation needed
    d /= np.linalg.norm(d, axis=1, keepdims=True) + 1e-12
    off = rng.uniform(0.0, shell_um, n)
    P = C[sph] + d * (R[sph] + off)[:, None]
    (Lx, Ly, Lz) = box_um
    keep = ((P[:, 0] >= 0) & (P[:, 0] < Lx) & (P[:, 1] >= 0) & (P[:, 1] < Ly)
            & (P[:, 2] >= 0) & (P[:, 2] < Lz))                # DROP out-of-box (fibre convention,
    P = P[keep]; sph = sph[keep]                              #  no wall 'curtains'; periodic images
    if in_am is not None and len(P):                          #  re-enter via the volume renorm)
        P_keep = ~np.array([in_am(q) for q in P])             # drop points buried in a NEIGHBOUR AM
        P = P[P_keep]; sph = sph[P_keep]                      #  (own sphere: offset ≥ R → never inside)
    P = P.astype(np.float32)
    return (P, sph.astype(np.int32)) if return_ids else P


def _rot_z_to(d_loc, a):
    """Rodrigues rotation of local-frame unit vectors d_loc[(n,3)] so local +z maps onto the
    per-row axis a[(n,3)] (unit).  Shared by sheath cap sampling; mirrors seed_coat's inline
    block (kept separate — seed_coat is validated production code, not refactored here)."""
    t = np.cross(np.broadcast_to([0.0, 0.0, 1.0], a.shape), a)
    tn = np.linalg.norm(t, axis=1, keepdims=True)
    ok = tn[:, 0] > 1e-9
    t = np.where(ok[:, None], t / np.where(tn > 1e-9, tn, 1.0), [1.0, 0.0, 0.0])
    cosang = a[:, 2:3]
    d = d_loc * cosang + np.cross(t, d_loc) * np.sqrt(np.maximum(1 - cosang ** 2, 0)) \
        + t * (t * d_loc).sum(1, keepdims=True) * (1 - cosang)
    d[~ok] = d_loc[~ok] * np.sign(a[~ok, 2:3] + 1e-12)
    return d / (np.linalg.norm(d, axis=1, keepdims=True) + 1e-12)


def seed_sheath(n_seg, box_um, dx_um, rng, am=None, in_am=None, wrap_frac=1.0,
                shell_um=SWCNT_SHELL, seg_len_um=SWCNT_SEG_L, step_um=None, persist=0.85,
                return_ids=False, return_host=False, max_pts=400000):
    """A14 SURFACE-CONFORMAL SHEATH seeding (#275 koo2026, Joule 10:102392): continuous
    vein-like conductive filaments marching ON the AM sphere surfaces — geodesic random
    walks at a thin radial skin.  The THIRD carbon morphology, distinct from both existing
    ones (SuperP = discrete interstitial chains; VGCF = bulk-spanning stiff fibres) and from
    A4 coat_block (isolated blocking-film POINTS): every chain is CONTIGUOUS along itself
    (step ≈ voxel), i.e. a per-chain vein net (koo2026 Fig 1D "vein-like" wrapping; ζ≈−1.9 mV
    = near-complete coverage anchor).  ⚠ per-AM skin CONNECTIVITY across chains at production
    point budgets is representation-density-limited (µm inter-chain gaps at ~0.2 wt% + max_pts
    — same caveat class as the coverage metric; honest direction: the voxel stamp UNDER-states
    the real continuous skin, never fakes a gain).

    Walk: per chain, host AM chosen ∝ surface area; start uniform on the sphere (inside a
    per-sphere random CAP of fractional area `wrap_frac` when <1); each step advances the
    surface point by arc `step_um` along a parallel-transported tangent with curvature noise
    (1−persist) → wavy vein.  Cap containment steers the tangent back toward the cap axis.
    Points sit at radius R+U(0,shell_um) (thin skin; sub-voxel reality documented at the
    SWCNT_* constants — volume add_pvs-pinned downstream so porosity stays honest).

    Drops out-of-box points and points buried in a NEIGHBOURING AM — ANALYTIC sphere test
    vs `am` (scipy KDTree; own host never — offset ≥ 0).  The caller's voxel-mask `in_am` is
    used only as a scipy-less fallback: a voxel mask cannot exclude the own host (cell-center
    -inside test drops ~20% of the skin at dx > shell), so the analytic path is authoritative.
    If n_seg·steps would exceed `max_pts`, chains are subsampled (n_seg floors at 1, so
    max_pts < n_steps still emits one chain; visible in the dispatch's "objects → pts" print
    — not a silent cap).
    Returns P[(n,3) float32] (+ per-chain fid if return_ids; + host AM index if return_host).
    """
    (Lx, Ly, Lz) = box_um
    if am is None or len(am[0]) == 0 or n_seg <= 0:            # no AM → nothing to wrap
        z = (np.zeros((0, 3), np.float32), np.zeros(0, np.int32), np.zeros(0, np.int32))
        if return_ids and return_host:
            return z
        return (z[0], z[1]) if return_ids else (z[0], z[2]) if return_host else z[0]
    C, R = np.asarray(am[0], np.float64), np.asarray(am[1], np.float64)
    step = float(step_um) if step_um else 0.9 * float(dx_um)   # arc per step ≈ voxel → contiguous skin
    n_steps = max(4, int(round(float(seg_len_um) / step)))
    if n_seg * n_steps > max_pts:                              # representation budget (dispatch prints counts)
        n_seg = max(1, max_pts // n_steps)
    w = R ** 2; w = w / w.sum()
    sph = rng.choice(len(C), n_seg, p=w)                       # host AM per chain (area-weighted)
    ax = rng.normal(size=(len(C), 3)); ax /= np.linalg.norm(ax, axis=1, keepdims=True) + 1e-12
    a = ax[sph]                                                # per-sphere fixed cap axis (contiguous patch)
    wf = float(np.clip(wrap_frac, 1e-3, 1.0))
    zmin = 1.0 - 2.0 * wf                                      # cap cos threshold (wf=1 → whole sphere)
    # start: uniform inside the cap (local frame), rotate +z→axis
    k = rng.uniform(0, 1, n_seg)
    z0 = 1.0 - 2.0 * wf * k
    phi = rng.uniform(0, 2 * np.pi, n_seg)
    rr = np.sqrt(np.maximum(0.0, 1.0 - z0 * z0))
    u = _rot_z_to(np.column_stack([rr * np.cos(phi), rr * np.sin(phi), z0]), a)
    v = rng.normal(size=(n_seg, 3))
    t = v - (v * u).sum(1, keepdims=True) * u
    t /= np.linalg.norm(t, axis=1, keepdims=True) + 1e-12      # tangent ⊥ u
    th = np.clip(step / R[sph], 1e-4, 0.5)[:, None]            # per-chain arc angle (rad)
    cth, sth = np.cos(th), np.sin(th)
    sig_w = (1.0 - float(np.clip(persist, 0.0, 1.0))) * 1.2    # curvature noise (rad/step) → vein waviness
    P_steps, host = [], sph.astype(np.int32)
    for kst in range(n_steps):
        off = rng.uniform(0.0, shell_um, n_seg)
        P_steps.append(C[sph] + u * (R[sph] + off)[:, None])
        un = u * cth + t * sth                                 # geodesic advance
        tn = -u * sth + t * cth                                # parallel transport (stays ⊥ un)
        if sig_w > 0:
            eps = rng.normal(0.0, sig_w, (n_seg, 1))
            tn = tn * np.cos(eps) + np.cross(un, tn) * np.sin(eps)   # wobble about the normal
        un /= np.linalg.norm(un, axis=1, keepdims=True) + 1e-12      # re-normalize each step: tiny-cap
        if wf < 1.0:                                           # steering (below) otherwise degrades the
            # cap containment: steer back toward axis.  Threshold clamped < 1: at wf ≤ 0.025 the raw
            # zmin+0.05 ≥ 1 fired EVERY step and broke (u,t) orthonormality (‖u‖ drifted to 3× →
            # points 3.5 µm off-surface / inside the host — adversarial-review finding).
            out = (un * a).sum(1) < min(zmin + 0.05, 0.999)
            if out.any():
                g = a[out] - (a[out] * un[out]).sum(1, keepdims=True) * un[out]
                g /= np.linalg.norm(g, axis=1, keepdims=True) + 1e-12
                tn[out] = g                                    # tangent → toward cap centre
        tn -= (tn * un).sum(1, keepdims=True) * un             # Gram-Schmidt: keep t ⊥ u exactly
        u, t = un, tn / (np.linalg.norm(tn, axis=1, keepdims=True) + 1e-12)
    # stack step-major: stable sort by fid downstream restores along-chain order within each fid
    P = np.concatenate(P_steps, 0)
    fid = np.tile(np.arange(n_seg, dtype=np.int32), n_steps)
    hst = np.tile(host, n_steps)
    keep = ((P[:, 0] >= 0) & (P[:, 0] < Lx) & (P[:, 1] >= 0) & (P[:, 1] < Ly)
            & (P[:, 2] >= 0) & (P[:, 2] < Lz))
    P, fid, hst = P[keep], fid[keep], hst[keep]
    dropped_analytic = False
    if len(P) and len(C) > 1:                                  # ANALYTIC neighbour-burial (authoritative):
        try:                                                   #   a voxel in_am can't exclude the own host
            from scipy.spatial import cKDTree                  #   (drops ~20% of the skin at dx > shell)
            kq = min(len(C), 8)
            dnb, jnb = cKDTree(C).query(P, k=kq)
            if kq == 1:
                dnb, jnb = dnb[:, None], jnb[:, None]
            buried = ((dnb < R[jnb] - 1e-9) & (jnb != hst[:, None])).any(1)
            P, fid, hst = P[~buried], fid[~buried], hst[~buried]
            dropped_analytic = True
        except ImportError:
            pass
    if (not dropped_analytic) and in_am is not None and len(P):   # scipy-less fallback (voxel mask —
        kp = ~np.array([in_am(q) for q in P])                     #   over-drops own-host skin, documented)
        P, fid, hst = P[kp], fid[kp], hst[kp]
    P = P.astype(np.float32)
    if return_ids and return_host:
        return P, fid, hst
    if return_ids:
        return P, fid
    if return_host:
        return P, hst
    return P


def _fib_sphere_samples(am_c, am_r, n_samp, seed=0):
    """Area-weighted Fibonacci samples on AM sphere surfaces → (pts[(n,3)], sphere_idx[(n,)]).
    Same ground-truth convention as the SE-dump coverage check (CLAUDE.md 2026-06-17)."""
    C, R = np.asarray(am_c, np.float64), np.asarray(am_r, np.float64)
    w = R ** 2; w = w / w.sum()
    per = np.maximum(8, np.round(w * n_samp).astype(int))
    ga = np.pi * (3.0 - np.sqrt(5.0))                          # golden angle
    pts, idx = [], []
    for j in range(len(C)):
        m = per[j]
        i = np.arange(m, dtype=np.float64)
        z = 1.0 - 2.0 * (i + 0.5) / m
        rr = np.sqrt(np.maximum(0.0, 1.0 - z * z))
        th = ga * i
        d = np.column_stack([rr * np.cos(th), rr * np.sin(th), z])
        pts.append(C[j] + d * R[j])
        idx.append(np.full(m, j, np.int32))
    return np.concatenate(pts, 0), np.concatenate(idx)


def sheath_ion_tradeoff(sheath_pts_um, am_c_um, am_r_um, se_pts_um,
                        bands_um=(0.13, 0.26), n_samp=6000, seed=0, wrap_frac=None,
                        se_cloud_label='pre-compaction seed positions (moves during compaction)'):
    """A14 — sheath electronic-coverage vs LPSCl ionic-contact TRADE-OFF (geometry only).

    TWO layers, deliberately separate (they answer different questions):

    • physical_bound — ANALYTIC, from `wrap_frac` alone: the real sheath is a CONTINUOUS
      sub-voxel skin (few-layer ~2-10 nm = OUR inference from the published tube Ø 2 nm;
      koo2026 publishes no sheath thickness.  ζ≈−1.9 = near-complete coverage anchor), so
      wherever the wrapped cap covers the AM surface the skin interposes at every AM|SE
      contact there.  blocked = 100·wrap_frac is the EXPECTATION under random cap
      orientation (exact, SE-clustering-independent: P(point ∈ random cap) = cap area
      fraction) — a true bound only at wrap=1; for wrap<1 individual AMs can block up to
      100% of their SE contacts when contacts cluster inside the cap (dead-AM hotspot
      risk the case-mean hides).  "Upper bound" refers to the ION-BLOCKING-SKIN assumption
      axis, not to cap-orientation realizations.  This is the number to reason with.

    • cloud_at_representation_density (per_band) — the SEEDED point cloud vs area-weighted
      Fibonacci AM-surface samples at each band b (Hertz 0.13 / Tabor 0.26 µm project
      convention): sheathed = nearest sheath pt ≤ b; se_contact = nearest SE pt ≤ b.
      ⚠ REPRESENTATION-LIMITED on BOTH clouds: the sheath cloud undersamples the continuous
      skin (~0.2 wt% + max_pts → spacing > band), and the SE side is whatever subsample the
      caller passes (production: 300k of tens of millions → se_contact_pct GROSSLY
      understates the real AM|SE contact).  Diagnostics only (where veins sit vs SE
      contacts); NEVER read as physical coverage.  n_se_used/se_nn_spacing_um are recorded
      so the density limit is self-describing.

    ⚠ §F1 semantics of "blocked": assumes an ion-blocking skin.  Taken literally at wrap=1
    the bound is 100% = an electrochemically DEAD cathode — yet koo2026's cells deliver
    11.4 mAh/cm², proving Li⁺ passes the skin in their LIQUID system (our inference:
    electrolyte wets the nm-scale inter-tube mesh; their PUBLISHED transport claim is
    pore-CHANNEL vacating — D_eff 2.5× — not trans-skin porosity).  For our SOLID LPSCl
    contact the nearest same-SE anchor is kim2025 SP@CAM (interposed carbon: active surface
    area −49%, σ_ion −31% at 2.9 wt%) = measured PARTIAL blocking → expected real loss well
    below the bound.  Read as bracket, never a loss prediction; blocked_eff maps to
    R_ct ∝ 1/(1−blocked_eff) in the R_int(N) reference frame.
    Returns None when scipy is unavailable or <2 sheath points (no silent fallback math;
    a 1-point cloud would emit spacing=inf → non-RFC JSON)."""
    try:
        from scipy.spatial import cKDTree
    except ImportError:
        return None
    surf, _ = _fib_sphere_samples(am_c_um, am_r_um, n_samp, seed)
    sh = np.asarray(sheath_pts_um, np.float64)
    se = np.asarray(se_pts_um, np.float64)
    if len(sh) < 2 or len(surf) == 0:
        return None
    d_sh = cKDTree(sh).query(surf, k=1)[0]
    d_se = cKDTree(se).query(surf, k=1)[0] if len(se) else np.full(len(surf), np.inf)
    # representation-density scales (BOTH clouds) — recorded so readers can judge the bands
    nn = cKDTree(sh).query(sh[:min(len(sh), 4000)], k=2)[0][:, 1]
    se_nn = (cKDTree(se).query(se[:min(len(se), 4000)], k=2)[0][:, 1] if len(se) > 1
             else np.array([0.0]))
    out = {'bands_um': [float(b) for b in bands_um], 'n_surf_samples': int(len(surf)),
           'cloud_nn_spacing_um': round(float(np.median(nn)), 4),
           'n_se_used': int(len(se)), 'se_nn_spacing_um': round(float(np.median(se_nn)), 4),
           'se_cloud': se_cloud_label, 'per_band': {}}
    if wrap_frac is not None:
        wf = float(np.clip(wrap_frac, 0.0, 1.0))
        out['physical_bound'] = {
            'blocked_of_se_contact_pct_upper_bound': round(100.0 * wf, 1),
            'basis': 'ANALYTIC: expectation = 100·wrap_frac under random cap orientation '
                     '(exact, clustering-independent; per-AM tail can reach 100% at wrap<1). '
                     '"Upper bound" = the ion-blocking-skin ASSUMPTION axis: taken literally '
                     'at wrap=1 it means a dead cathode, while koo2026 cells deliver 11.4 '
                     'mAh/cm2 (liquid wets the nm inter-tube mesh — our inference; their '
                     'published claim is pore-channel vacating, not trans-skin porosity). '
                     'Solid-LPSCl nearest anchor kim2025 SP@CAM: ASA −49%, σ_ion −31% at '
                     '2.9wt% = measured PARTIAL blocking → expected real loss ≪ bound. '
                     'Bracket, not prediction; maps to R_ct ∝ 1/(1−blocked_eff).'}
    for b in bands_um:
        s = d_sh <= b
        c = d_se <= b
        n_c = int(c.sum())
        blocked = 100.0 * float((s & c).sum()) / n_c if n_c else 0.0
        out['per_band'][f'{b:g}'] = {
            'sheath_cov_pct': round(100.0 * float(s.mean()), 2),
            'se_contact_pct': round(100.0 * float(c.mean()), 2),
            'blocked_of_se_contact_pct': round(blocked, 2),
            'open_of_se_contact_pct': round(100.0 - blocked, 2) if n_c else 0.0}
    out['trust'] = ('physical_bound = the trade-off number (analytic, wrap_frac); per_band '
                    'cloud values are REPRESENTATION-DENSITY-limited diagnostics on BOTH '
                    f'sides (sheath spacing {out["cloud_nn_spacing_um"]}µm, SE subsample '
                    f'spacing {out["se_nn_spacing_um"]}µm vs bands {list(bands_um)}µm) — '
                    'they understate the continuous skin AND the real AM|SE contact; never '
                    'read as physical coverage.  Seed-time RIGID geometry; bands = '
                    'Hertz/Tabor convention.')
    return out


def seed_sdcp(n, box, dx, rng, am=None, in_am=None, surface_frac=0.5, clump=1,
              agg_d=0.0, d=SDCP_D, return_ids=False, return_info=False):
    """SDCP particle seeding — the MIXING-dependent dispersion states (manuscript S2/S3).
    Single source of truth shared by mpm3d_compaction (seed-box units) and
    scripts/preview_sdcp_mixing.py (µm units): box/dx/d/agg_d must be in ONE frame.

    Two dispersion modes (agg_d wins):
      agg_d == 0 — HIGH SHEAR (ball-mill / Thinky; manuscript electrode): the dry process
        mills the powder to 0.2-0.5µm SINGLES (Fig S3).  `surface_frac` of them are
        anchored ON the AM surfaces (seed_coat shell = d/2 — sulfonate chemisorption +
        ordered-mixing decoration of the coarse host); the rest disperse in-pore via
        seed_blobs rejection sampling (count-preserving — a 0D particle sits in the pore
        space by definition; keeps the bulk population consistent with the agg-mode bulk).
        clump > 1 = the NCM-decoration CLUSTER hypothesis (§3.7): the anchored share seeds
        as `clump`-member clusters scattered ~1 particle Ø (gaussian σ = d) around
        AM-surface centres; the bulk share STAYS singles (the powder itself is dispersed).
      agg_d > 0 — LOW SHEAR (hand-mix): no milling energy → the AS-MADE ~agg_d
        agglomerates (Fig S2) survive.  BOUNDING ENDPOINT (full survival; partial
        breakage / fines mixtures not modelled).  ALL SDCP seeds as agglomerates: the
        EXACT n members are distributed over n_cl ≈ n/n_agg clusters (n_agg =
        SDCP_AGG_PACK·(agg_d/d)³), each uniform-in-sphere with radius
        (agg_d/2)·(m_i/n_agg)^⅓ so the SEEDED internal packing is SDCP_AGG_PACK for full
        and partial agglomerates alike.  Centres split surface_frac : rest between AM
        surfaces (members poking into the host DROP → a cap DRAPED on the NCM, the
        soft-agglomerate adhesion contact) and the bulk pore space.
    ⚠ HONESTY (§F1):
      • SDCP_AGG_PACK=0.64 is an ASSUMED as-made internal packing (RCP-like) — S2 anchors
        the ~3µm SIZE only; a denser/solid particle is not excluded.  Tunable hook.
      • surface_frac is the SEED-TIME split, NOT the realized share: in-AM/out-of-box
        drops are population-asymmetric (draped caps lose ~half their members; bulk
        rejection sampling loses none).  Read the REALIZED split from `info`
        (realized_anchor_frac) / run metadata, not from surface_frac.
      • Volume: drops are re-pinned GLOBALLY downstream (add_pvs = recipe/len(pts)), so
        total volume is exact but the dropped (draped) anchored volume migrates into ALL
        survivors — realized agglomerate internal density ≈ SDCP_AGG_PACK/survival (can
        exceed 1).  Porosity is volume-pinned and unaffected.
    Returns pts float32 (m,3) [+ ids int32: cluster/agglomerate group index — anchored
    singles carry their AM-sphere index, bulk singles a unique id (fibre-id ledger)]
    [+ info dict: realized per-population counts / shares / survival]."""
    box_arr = np.asarray(box, np.float64)
    agg = bool(agg_d and agg_d > 0.0)
    info = {'n_target': int(n), 'mode': 'agglomerate_S2' if agg else 'singles_S3',
            'surface_frac_nominal': round(float(surface_frac), 4)}
    parts, idparts, tags, base = [], [], [], 0

    def _filt(P, ids):
        if len(P) == 0:
            return np.zeros((0, 3), np.float64), np.zeros(0, np.int64)
        keep = ((P >= 0) & (P < box_arr)).all(1)
        P, ids = P[keep], ids[keep]
        if in_am is not None and len(P):
            k2 = ~np.array([in_am(q) for q in P])
            P, ids = P[k2], ids[k2]
        return P, ids

    def _push(P, ids, n_groups, tag):
        nonlocal base
        P, ids = _filt(np.asarray(P, np.float64), np.asarray(ids, np.int64))
        if len(P):
            parts.append(P.astype(np.float32))
            idparts.append((ids + base).astype(np.int32))
            tags.append((tag, len(P)))
        base += int(n_groups)

    def _ball(centres, m_per, radius):
        """m_per[i] pts uniform-in-sphere(radius[i]) around centre i → (P, group ids)."""
        rep = np.repeat(np.arange(len(centres)), m_per)
        v = rng.normal(size=(len(rep), 3))
        v /= np.linalg.norm(v, axis=1, keepdims=True) + 1e-12
        rr = np.repeat(radius, m_per) * rng.uniform(0.0, 1.0, len(rep)) ** (1.0 / 3.0)
        return np.asarray(centres, np.float64)[rep] + v * rr[:, None], rep

    have_am = am is not None and len(am[0]) > 0
    if agg:
        n_agg = max(1, int(round(SDCP_AGG_PACK * (agg_d / d) ** 3)))   # design primaries per FULL agglomerate
        n_cl = max(1, int(round(n / n_agg)))                    # agglomerate count from the recipe
        n_cl_am = int(round(n_cl * surface_frac)) if have_am else 0
        n_cl_bulk = max(n_cl - n_cl_am, 0)
        n_m_am = int(round(n * (n_cl_am / n_cl)))               # EXACT member split (Σ = n, no quantization)
        info.update(n_agg_design=int(n_agg), agg_pack_assumed=SDCP_AGG_PACK,
                    n_clusters_target=int(n_cl))
        for cnt_c, cnt_m, tag in ((n_cl_am, n_m_am, 'am'), (n_cl_bulk, n - n_m_am, 'bulk')):
            if cnt_c <= 0 or cnt_m <= 0:
                continue
            ctr = (seed_coat(cnt_c, box, dx, rng, am=am, shell_um=d / 2, surface_frac=1.0,
                             in_am=in_am) if tag == 'am'
                   else seed_blobs(cnt_c, box, rng, in_am=in_am))
            if not len(ctr):
                base += cnt_c
                continue
            m = np.full(len(ctr), cnt_m // len(ctr), np.int64)  # exact member distribution over the
            m[:cnt_m % len(ctr)] += 1                           #   REALIZED centres (mass-conserving)
            rad = (agg_d / 2.0) * (m / float(n_agg)) ** (1.0 / 3.0)   # partial/over-full → radius scaled;
            P, gid = _ball(ctr, m, rad)                               #   SEEDED packing = SDCP_AGG_PACK always
            _push(P, gid, len(ctr), tag)
            info['n_clusters_' + tag] = int(len(ctr))
    else:
        n_am = int(round(n * surface_frac)) if have_am else 0
        n_bulk = max(n - n_am, 0)
        clump = max(1, int(clump))
        if n_am > 0 and clump > 1:
            n_ctr = max(1, n_am // clump)
            ctr = seed_coat(n_ctr, box, dx, rng, am=am, shell_um=d / 2, surface_frac=1.0,
                            in_am=in_am)
            if len(ctr):
                rep = np.repeat(np.arange(len(ctr)), clump)[:n_am]
                P = np.asarray(ctr, np.float64)[rep] + rng.normal(scale=d, size=(len(rep), 3))
                _push(P, rep, len(ctr), 'am')
            else:
                base += n_ctr
            info['n_clusters_am'] = int(len(ctr))
        elif n_am > 0:
            P, sph = seed_coat(n_am, box, dx, rng, am=am, shell_um=d / 2, surface_frac=1.0,
                               in_am=in_am, return_ids=True)
            if len(P):
                parts.append(P.astype(np.float32))
                idparts.append((sph.astype(np.int64) + base).astype(np.int32))
                tags.append(('am', len(P)))
            base += int(len(am[0]))
        if n_bulk > 0:
            P = seed_blobs(n_bulk, box, rng, in_am=in_am)       # count-preserving (rejection sampling)
            if len(P):
                _push(P, np.arange(len(P)), len(P), 'bulk')
    if parts:
        pts, ids = np.concatenate(parts, 0).astype(np.float32), np.concatenate(idparts, 0)
    else:
        pts, ids = np.zeros((0, 3), np.float32), np.zeros(0, np.int32)
    n_a = sum(c for t, c in tags if t == 'am'); n_b = sum(c for t, c in tags if t == 'bulk')
    info.update(n_seeded=int(len(pts)), n_anchored_seeded=int(n_a), n_bulk_seeded=int(n_b),
                survival=round(len(pts) / max(n, 1), 4),
                realized_anchor_frac=round(n_a / len(pts), 4) if len(pts) else 0.0)
    out = [pts]
    if return_ids:
        out.append(ids)
    if return_info:
        out.append(info)
    return out[0] if len(out) == 1 else tuple(out)


def seed_fibres(n, box_um, dx_um, rng, in_am=None, L=VGCF_L, L_cv=0.0,
                curl=0.0, vol_conserve=False, vol_cv=0.0, nucleate=None, nucleate_frac=0.0,
                branch_frac=0.0, branch_n=2, branch_vol=0.3, branch_len=0.5,
                bridge_frac=0.0, bridge_drift=0.15, buckle_lam=0.0, buckle_strain=0.0, am_frac_fn=None,
                align_lambda=1.0,
                return_lengths=False, return_ids=False, return_vol=False):
    """n random fibres (SEM-like: thin rods/fibrils threading the interstices), each a chain of
    points spaced ~dx along its path.  Even distribution = uniform random centres.  Points falling
    in AM (in_am) are dropped (fibre bends around).

    L_cv>0 → per-fibre length is lognormal (mean L, CV L_cv), mean-preserving: the recipe
    count/volume is unchanged, only the lengths spread (real VGCF: 5-20µm from milling).

    curl>0 → the path is a persistent random walk (worm-like chain) with a per-step direction kick
    ~curl rad, instead of a straight rod.  curl=0 → perfectly straight.  VGCF uses a SMALL curl
    (~0.06) for as-grown graphite-fibre waviness — real VGCF is wavy, not laser-straight (axially
    stiff, so it doesn't bend much MORE under load, but it isn't a ruler either; perfectly straight
    rods read as an artifact).  PTFE fibrils are roll-shear-DRAWN into a tangled, curved web → curl≈0.4.
    NOTE: the per-step kick is in grid steps, so total waviness ∝ curl·√(L/step) — mildly resolution-
    sensitive; tune curl per n_grid if a run looks too straight/too coiled.

    vol_conserve → CONSTANT-VOLUME DRAWING (PTFE fibrillation): each fibril starts as a PTFE node of
    volume V_i (varied by vol_cv — real PTFE has a particle/agglomerate SIZE distribution) and is drawn
    to length L_i, conserving ITS OWN V_i, so cross-section A_i = V_i/L_i → diameter d_i ∝ √(V_i/L_i).
    TWO independent spreads (initial volume V_i × draw length L_i) ⇒ a diverse fibre population: a big
    node drawn short = very thick stub, a small node drawn long = very thin strand — exactly PTFE roll-
    fibrillation.  The per-point volume weight is V_i/k_i ∝ V_i/L_i (a thin-long fibril carries LESS
    material per point).  return_vol returns that per-point weight, normalised to mean 1 (Σ = n_points),
    so multiplying by the uniform add_pvs preserves the recipe volume exactly while redistributing it.
    The diameter stays sub-grid (a fibre is ~1 cell thick); d_i ∝ √weight, so the viewer reconstructs
    each fibre's thickness from the per-point weight (carried via --save-fibre-dia → payload 'd').
    vol_conserve=False (VGCF) → uniform weight (a manufactured fibre has constant Ø).

    nucleate (Nx3 attractor points, e.g. the already-seeded carbon) + nucleate_frac → a fraction of
    fibrils START on a random attractor (small jitter) instead of in free void, so the PTFE binder web
    co-locates with and NETS the carbon → forms the Carbon-Binder Domain (CBD) rather than floating.

    branch_frac → ② HIERARCHY: a primary fibril spawns up to branch_n thinner secondary fibrils from
    points along it (child volume = branch_vol·V_parent, length = branch_len·L_parent → child d is
    smaller → finer fibril), reproducing the lit primary→secondary→tertiary branched web.

    bridge_frac + bridge_drift → ④ DIRECTED BRIDGE: a fibril nucleated on one carbon point also picks a
    NEARBY second attractor and STEERS its walk toward it (drift term), so the fibril CONNECTS two
    carbon clusters instead of wandering isotropically — the actual binding action (Lee 2025 SEM: binder
    fibrils stretched & fibrillated ACROSS the interface, bridging particles)."""
    (Lx, Ly, Lz) = box_um
    sigma = np.sqrt(np.log(1.0 + L_cv ** 2)) if L_cv > 0 else 0.0   # length lognormal, mean-preserving
    sigma_v = np.sqrt(np.log(1.0 + vol_cv ** 2)) if vol_cv > 0 else 0.0   # INITIAL node-volume spread
    step = 0.7 * dx_um                                              # point spacing along the fibre path
    nuc = np.asarray(nucleate, np.float32) if (nucleate is not None and len(nucleate)) else None
    hi = np.array([Lx - 1e-3, Ly - 1e-3, Lz - 1e-3])

    def _grow(c, d0, Li, kk, drift_to):
        """one fibre path from c along d0 (length Li, kk pts).  curl>0 → worm-like walk; drift_to (a
        target point) biases the walk toward it (④ directed bridge).  Returns the clipped, AM-dropped line."""
        if curl <= 0.0 and drift_to is None:                        # straight rod (VGCF)
            t = np.linspace(-Li / 2, Li / 2, kk)
            ln = c[None, :] + t[:, None] * d0[None, :]
            if buckle_lam > 0.0 and buckle_strain > 0.0 and kk >= 3:
                # ★ PRESCRIBED SEM-CONSISTENT BUCKLE (morphology knob, NOT a derived transport result — the
                # scaffold MPM can't compress the fibre to buckle it emergently, fibre_rod_mpm_design §RESULT;
                # real VGCF waviness is part as-grown + part discrete AM-pinching = DEM).  Winkler wavelength
                # buckle_lam = 2π(EI/E_SE)^¼ (~1.5µm, ~13 half-waves / 10µm fibre).  Amplitude A = (λ/π)√ε_ax.
                # ε_ax = buckle_strain · cos²θ · amf, where cos²θ (θ=fibre angle from press-z) makes z-aligned
                # fibres buckle most, and amf = LOCAL AM volume fraction around the fibre (am_frac_fn) makes
                # fibres in dense/pinched AM regions buckle more than those in open SE pores — the actual
                # particle-pinching driver, so the waviness is AM-POSITION-dependent (not spatially uniform).
                amf = float(am_frac_fn(c)) if am_frac_fn is not None else 1.0
                eps_ax = buckle_strain * float(d0[2]) ** 2 * max(0.0, min(amf, 1.0))
                A = (buckle_lam / np.pi) * np.sqrt(max(eps_ax, 0.0))
                if A > 0.0:
                    rp = rng.normal(size=3); rp -= rp.dot(d0) * d0    # a perpendicular buckling direction
                    rp /= np.linalg.norm(rp) + 1e-12
                    s = t + Li / 2.0                                  # arc position 0..Li
                    win = np.sin(np.pi * s / Li)                      # end-taper → deflection vanishes at the pins
                    disp = A * win * np.sin(2.0 * np.pi * s / buckle_lam + rng.uniform(0, 2 * np.pi))
                    ln = ln + disp[:, None] * rp[None, :]
        else:                                                       # persistent random walk (PTFE fibril)
            d = d0.copy(); pos = c.copy(); seq = [pos.copy()]
            for _s in range(kk - 1):
                d = d + rng.normal(size=3) * curl                   # turn ~curl rad, persist
                if drift_to is not None:                            # steer toward the bridge target
                    to = drift_to - pos; d = d + bridge_drift * to / (np.linalg.norm(to) + 1e-9)
                d /= np.linalg.norm(d) + 1e-12
                pos = pos + step * d; seq.append(pos.copy())
            ln = np.asarray(seq)
        ln = ln[(ln[:, 0] >= 0) & (ln[:, 0] < Lx) & (ln[:, 1] >= 0)
                & (ln[:, 1] < Ly) & (ln[:, 2] >= 0) & (ln[:, 2] < Lz)]
        if in_am is not None and len(ln):
            ln = ln[~np.array([in_am(p) for p in ln])]
        return ln

    pts, lens, ids, wts = [], [], [], []
    fid = 0                                                          # fibre index (so points can be re-grouped
    for _ in range(n):                                             # into individual fibres for line rendering)
        Li = L if sigma == 0 else float(np.clip(L * np.exp(rng.normal(-0.5 * sigma ** 2, sigma)),
                                                0.3 * L, 3.0 * L))   # draw LENGTH: mean L, clipped 0.3L..3L
        Vi = 1.0 if sigma_v == 0 else float(np.clip(np.exp(rng.normal(-0.5 * sigma_v ** 2, sigma_v)),
                                                    0.2, 5.0))      # INITIAL node VOLUME (mean 1): size spread
        k = max(2, int(round(Li / step)))                           # points per fibre (∝ length)
        drift_to = None
        if nuc is not None and rng.random() < nucleate_frac:        # CBD: nucleate on a carbon attractor →
            a = nuc[rng.integers(len(nuc))]
            c = np.clip(a + rng.normal(size=3) * (1.5 * step), 0, hi)   # binder STARTS on carbon (nets it)
            if bridge_frac > 0.0 and rng.random() < bridge_frac:    # ④ pick a NEARBY 2nd carbon → bridge to it
                b = nuc[rng.integers(len(nuc))]
                if step < np.linalg.norm(b - a) < 1.3 * Li:         # reachable within ~one fibre length
                    drift_to = b
        else:
            c = np.array([rng.uniform(0, Lx), rng.uniform(0, Ly), rng.uniform(0, Lz)])
        d0 = (drift_to - c) if drift_to is not None else rng.normal(size=3)   # head toward the bridge target
        if align_lambda != 1.0:                                # PRESS-INDUCED IN-PLANE ALIGNMENT (affine):
            d0 = d0 * np.array([1.0, 1.0, align_lambda])       # uniaxial-z compaction (λ_z<1) tilts fibres in-
        d0 = d0 / (np.linalg.norm(d0) + 1e-12)                 # plane (tanθ_new = tanθ0/λ_z).  buckle then sees
        line = _grow(c, d0, Li, k, drift_to)                   # a smaller d0[2] → in-plane fibres buckle less (physical)
        if not len(line):
            continue
        pts.append(line); lens.append(Li); ids.append(np.full(len(line), fid, np.int32))
        wts.append(np.full(len(line), Vi / len(line), np.float32)); fid += 1   # fibre = node-vol Vi → d∝√(Vi/Li)
        # ② HIERARCHY: the primary spawns thinner secondary fibrils (1차→2차 branched web)
        if branch_frac > 0.0 and len(line) > 3 and rng.random() < branch_frac:
            for _b in range(int(rng.integers(1, branch_n + 1))):
                bp = line[rng.integers(len(line))]                  # branch point along the primary
                Vc = Vi * branch_vol * (0.5 + rng.random())         # child thinner (fraction of parent V) →
                Lc = Li * branch_len * (0.4 + 0.8 * rng.random())   #   shorter; both → smaller child d
                dc = rng.normal(size=3); dc /= np.linalg.norm(dc) + 1e-12
                cl = _grow(bp, dc, Lc, max(2, int(round(Lc / step))), None)
                if len(cl):
                    pts.append(cl); lens.append(Lc); ids.append(np.full(len(cl), fid, np.int32))
                    wts.append(np.full(len(cl), Vc / len(cl), np.float32)); fid += 1
    P = np.concatenate(pts, 0).astype(np.float32) if pts else np.zeros((0, 3), np.float32)
    out = [P]
    if return_lengths:
        out.append(np.array(lens, np.float32))
    if return_ids:                                                  # per-point fibre index (0..n_fibre-1)
        out.append(np.concatenate(ids).astype(np.int32) if ids else np.zeros(0, np.int32))
    if return_vol:                                                  # per-point volume weight (mean 1)
        if vol_conserve and pts:
            w = np.concatenate(wts).astype(np.float32); w *= len(w) / w.sum()   # ∝1/L_i, Σ=n_points
        else:
            w = np.ones(len(P), np.float32)                         # uniform Ø (VGCF)
        out.append(w)
    return out[0] if len(out) == 1 else tuple(out)


def seed_blobs(n, box_um, rng, in_am=None):
    """n carbon-black / PTFE points, uniform-random (even) through the box, non-AM."""
    (Lx, Ly, Lz) = box_um
    out, tries = [], 0
    while len(out) < n and tries < 50 * n + 100:
        p = np.array([rng.uniform(0, Lx), rng.uniform(0, Ly), rng.uniform(0, Lz)])
        tries += 1
        if in_am is None or not in_am(p):
            out.append(p)
    return np.array(out, np.float32) if out else np.zeros((0, 3), np.float32)


SP_AGG = 0.18         # Super P aggregate size µm (40nm primaries → 150-200nm branched aggregate; lit)

# ── ADDITIVE × MIXING process matrix (the A4 plug-board) ─────────────────────────
# Every (additive, mixing) combination is an INDEPENDENT, explicit slot so each can
# carry its own process physics.  `regime` says WHERE the additive ends up:
#   'bulk'       — in the particle interstices (current default; W2 σ_e BOOST).
#   'coat_block' — carbon inside the SE-coating-on-CAM layer, blocking CAM–CAM
#                  contact → W2 σ_e COLLAPSE (Super P dry-coat; Kim2025 SE–SP@CAM 1.0e-5).
#   'coat_embed' — carbon embedded in a porous SE coating, still conductive → W2 σ_e
#                  ~RECOVERS (VGCF dry-coat; Kim2025 SE–VGCF@CAM 1.4e-2 ≈ no-CA).
# ★ A4 HOOK: the *structural seeding* for the 'coat_*' regimes (placing carbon in the
#   SE-coating layer rather than bulk interstices) is NOT yet implemented in the MPM
#   (mpm3d_compaction seeds every regime as bulk today).  These cells are pre-wired so
#   that when the A4 se_coating GPU results land you only fill (i) the coating seeding
#   in mpm3d_compaction and (ii) the embed/block σ magnitudes in grade_engine — no
#   plumbing.  Morphology fields beyond Super P's CB params are descriptive intent
#   (TBD A4/lit) and are NOT yet read by the fibre seeder, so behaviour is unchanged.
#   mixing energy (lit): ball-mill/Thinky = high shear → short, uniform, AM-coating;
#   hand-mix = gentle → long, clustered agglomerates (less dispersion).
ADDITIVE_PROCESS = {
    'SuperP': {  # 0D carbon black — k/surface_frac/step/clump consumed by seed_carbon_black
        'ballmill': dict(regime='bulk',       k=3, surface_frac=0.70, step=0.7, clump=1),
        'thinky':   dict(regime='coat_block', k=3, surface_frac=0.70, step=0.7, clump=1),  # dry-coat → blocks CAM–CAM
        'handmix':  dict(regime='bulk',       k=8, surface_frac=0.30, step=0.9, clump=4),
    },
    'VGCF': {    # 1D fibre — ★ 'coat_embed' label RETIRED (2026-07-10, A4 closure): a 10µm stiff fibre
        # cannot 'coat' a 5µm NCM — the label never matched fibre physics (placement = bulk interstices
        # + buckle/align), and the Kim2025 coating concern is CARBON-BLACK's (coat_block), not fibres'.
        # → VGCF thinky ≡ ballmill by physics, not by TODO.
        'ballmill': dict(regime='bulk', morph='gently wavy fibre, well dispersed'),
        'thinky':   dict(regime='bulk', morph='gently wavy fibre (coat_embed retired — fibres do not coat)'),
        'handmix':  dict(regime='bulk', morph='long, clustered (gentle mix)'),
    },
    'SDCP': {    # self-doped conductive binder — MANUSCRIPT morphology, MIXING-dependent dispersion state.
        # The manuscript anchors BOTH endpoints of the shear axis:
        #   S3 = IN-ELECTRODE 0.2-0.5µm dispersed singles (their high-shear dry process mills the powder),
        #   S2 = AS-MADE ~3µm particles (what a mixer that CANNOT mill inherits — hand-mix has no milling
        #        energy → full-survival BOUNDING ENDPOINT: the SIZE is the S2 anchor, survival-at-low-shear
        #        is inference, partial breakage / fines mixtures not modelled.  Dispersion is a property of
        #        the POWDER after mixing, so it applies to the anchored AND the bulk share alike).
        # surface_frac = AM-anchored share (sulfonate anchoring + ordered-mixing decoration of the coarse
        # NCM host by the fine guest; MAGNITUDE un-anchored §F1 hook — S3 shows both populations.  hand-mix
        # lower: a ~3µm guest on a 5µm host has adhesion/weight ~100× weaker than a 0.3µm guest → ordered
        # mixing fades toward random).  clump = NCM-decoration cluster size (user §3.7 hypothesis; default
        # 1 = S3-faithful singles; SBE/DBE payload proximity + SEM/EDS discriminate).  agg_d = surviving
        # as-made agglomerate Ø (µm; 0 = milled to singles).  Consumed by seed_sdcp (single source shared
        # by mpm3d_compaction and preview_sdcp_mixing).
        'ballmill': dict(regime='particle', surface_frac=0.5, clump=1, agg_d=0.0,
                         morph='milled 0.2-0.5µm singles, NCM-anchor bias (S3)'),
        'thinky':   dict(regime='particle', surface_frac=0.5, clump=1, agg_d=0.0,
                         morph='milled 0.2-0.5µm singles, NCM-anchor bias (S3; ≡ballmill — both high-shear)'),
        'handmix':  dict(regime='particle', surface_frac=0.3, clump=1, agg_d=SDCP_AGG_D,
                         morph='as-made ~3µm agglomerates (size=S2 anchor; low-shear survival=inference); weaker NCM decoration'),
    },
    'PTFE': {    # binder fibril — fibril = fibrillation degree vs mixing SHEAR (dry-process; ∈(0,1], 1=full web)
        'ballmill': dict(regime='bulk', fibril=1.0,  morph='fibrillated binder web (high shear)'),
        'thinky':   dict(regime='bulk', fibril=1.0,  morph='dry-process fibrillation (high shear)'),
        'handmix':  dict(regime='bulk', fibril=0.45, morph='less fibrillated, clumpy (low shear)'),
    },
    'SWCNT': {   # ★ A14 surface-conformal sheath (#275 koo2026, Joule 10:102392) — THIRD carbon morphology.
        # The sheath is PRE-FORMED on the CAM powder by zeta-potential self-assembly (PDDA reverses NCMA to
        # +14.2 mV → f-SWCNT −35 mV wraps it; composite ζ≈−1.9 = near-complete coverage) BEFORE electrode
        # mixing.  Raman Fig 1F shows the attachment SURVIVES high-shear SLURRY mixing (>2000 rpm, wet);
        # koo2026's own dry route is kneading/fibrillation/calendering → thinky/handmix are covered by the
        # anchor.  ⚠ dry BALL-MILLING WITH MEDIA is NOT covered (§F1): abrasive media impact on a nm-scale
        # electrostatically physisorbed skin is outside the anchor's scope (the same media this matrix
        # credits with milling 3µm SDCP → 0.3µm singles) — wrap_frac=1.0 kept as the lit-supported
        # DIRECTION, survival-under-media = assumption; `--swcnt-wrap <1` is the degraded-wrap knob.
        'ballmill': dict(regime='surface_conformal', wrap_frac=1.0,
                         morph='vein-like conformal SWCNT sheath (pre-assembled; media-milling survival un-anchored §F1)'),
        'thinky':   dict(regime='surface_conformal', wrap_frac=1.0,
                         morph='vein-like conformal SWCNT sheath (pre-assembled, anchor-covered: kneading/calendering-robust)'),
        'handmix':  dict(regime='surface_conformal', wrap_frac=1.0,
                         morph='vein-like conformal SWCNT sheath (pre-assembled — low shear cannot undo self-assembly)'),
    },
}

# backward-compat: Super P carbon-black mixing presets consumed by seed_carbon_black.
# Derived from the matrix above (drop the non-CB keys) so there is ONE source of truth.
CB_MIX = {m: {k: v for k, v in cfg.items() if k in ('k', 'surface_frac', 'step', 'clump')}
          for m, cfg in ADDITIVE_PROCESS['SuperP'].items()}

# PTFE fibrillation degree vs mixing SHEAR (dry-process).  PTFE binder fibrillates — mechanically
# unravels into a BRANCHED fibril WEB — in proportion to the applied shear: high-shear ball-mill /
# Thinky give a good binder network; low-shear hand-mix leaves poorly-networked, clumpy fibrils.
# fibril ∈(0,1], 1 = full web.  DIRECTION is lit-supported (dry-electrode fibrillation); the MAGNITUDE
# (the 0.45 low-shear value) is NOT anchored — a demonstrative, tunable estimate (mpm3d_compaction
# --ptfe-fibril overrides).  Rule: docs/digest_model_application_backlog.md §F1 ("conservative tunable
# hook, 날조 금지").  Consumed ONLY for PTFE (fibre code 4); scales branch_frac (the web) → σ_e-network
# MORPHOLOGY + PTFE-on-AM coverage (pending a resolving-grid σ_e run), NOT porosity (soft PTFE flows +
# recipe-volume-pinned, mirror of SuperP).  DERIVED from ADDITIVE_PROCESS → ONE source of truth (cf CB_MIX).
PTFE_FIBRIL = {m: cfg.get('fibril', 1.0) for m, cfg in ADDITIVE_PROCESS['PTFE'].items()}


def additive_process(name, mixing):
    """Process cell for an (additive, mixing) pair; falls back to ball-mill / bulk."""
    a = ADDITIVE_PROCESS.get(name, {})
    return a.get(mixing) or a.get('ballmill') or {'regime': 'bulk'}


def additive_regime(name, mixing):
    """Placement regime for (additive, mixing): 'bulk' | 'coat_block' | 'coat_embed'.
    The single source of truth shared by the W2 σ estimate and (future A4) MPM seeding."""
    return additive_process(name, mixing).get('regime', 'bulk')


def seed_carbon_black(n, box_um, dx_um, rng, in_am=None, am=None, mixing='ballmill', return_ids=False):
    """Carbon black (Super P) — NOT isolated spheres.  Lit: 40nm primaries fuse into 150-200nm BRANCHED
    (fractal) aggregates that disperse AROUND the active material as a MULTI-CHAIN conductive network,
    loosely grouping into µm agglomerates.  Each aggregate is seeded as a short random-walk CHAIN (the
    branched structure); a `surface_frac` fraction nucleate in a thin shell on an AM surface (coating),
    the rest in the pore space.  `mixing` (ball-mill/Thinky vs hand-mix) sets chain length, surface
    fraction and agglomerate clustering (CB_MIX).  am=(centres[m,3], radii[m]) in box_um's frame for the
    coating bias (None → pore-only).  n = target point count → n_agg = n/k aggregates.  Returns the
    point cloud (+ per-aggregate ids if return_ids) so the viewer draws the chains as short lines."""
    if n <= 0:                                          # 0-wt% carbon → emit nothing (else max(1,…) below
        z = (np.zeros((0, 3), np.float32), np.zeros(0, np.int32))   # would inject a stray ~k-point chain)
        return z if return_ids else z[0]
    (Lx, Ly, Lz) = box_um
    cfg = CB_MIX.get(mixing, CB_MIX['ballmill'])
    k, sfrac, step, clump = cfg['k'], cfg['surface_frac'], cfg['step'] * dx_um, cfg['clump']
    have_am = am is not None and len(am[0]) > 0
    amc, amr = (am if have_am else (None, None))
    n_agg = max(1, int(round(n / k)))
    pts_list, ids_list, fid = [], [], 0
    anchor = None                                              # agglomerate nucleus (hand-mix clusters)
    for i in range(n_agg):
        if have_am and rng.random() < sfrac:                  # COAT an AM surface (just outside it)
            j = int(rng.integers(len(amc)))
            u = rng.normal(size=3); u /= np.linalg.norm(u) + 1e-12
            start = amc[j] + u * (amr[j] + (0.3 + 0.9 * rng.random()) * dx_um)
        elif clump > 1 and anchor is not None and (i % clump):  # cluster near the last nucleus (agglomerate)
            start = anchor + rng.normal(size=3) * (1.5 * step)
        else:
            start = np.array([rng.uniform(0, Lx), rng.uniform(0, Ly), rng.uniform(0, Lz)])
            anchor = start.copy()
        p = start.astype(np.float64).copy(); chain = [p.copy()]
        for _ in range(k - 1):                                # random-walk = branched aggregate
            u = rng.normal(size=3); u /= np.linalg.norm(u) + 1e-12
            p = p + u * step; chain.append(p.copy())
        chain = np.array(chain)
        chain = chain[(chain[:, 0] >= 0) & (chain[:, 0] < Lx) & (chain[:, 1] >= 0)
                      & (chain[:, 1] < Ly) & (chain[:, 2] >= 0) & (chain[:, 2] < Lz)]
        if in_am is not None and len(chain):
            chain = chain[~np.array([in_am(q) for q in chain])]
        if len(chain):
            pts_list.append(chain); ids_list.append(np.full(len(chain), fid, np.int32)); fid += 1
    P = np.concatenate(pts_list, 0).astype(np.float32) if pts_list else np.zeros((0, 3), np.float32)
    if return_ids:
        return P, (np.concatenate(ids_list).astype(np.int32) if ids_list else np.zeros(0, np.int32))
    return P


def parse_recipe(s: str) -> dict:
    """'AM:SE:VGCF:PTFE=80:18:1:1' or 'AM:SE:VGCF=72:27:1' → wt dict."""
    keys, vals = s.split('=')
    keys = keys.split(':'); vals = [float(v) for v in vals.split(':')]
    return dict(zip(keys, vals))


def dispersion_metrics(pts_um, box_xy_um, z_top_um, cell_um=2.0, matrix_pts_um=None,
                       nn_sample=20000, seed=0, am_c_um=None, am_r_um=None):
    """A5/E2 (#284 SSRM-analog) — additive DISPERSION uniformity.  Pure geometry, run-relative.

    Two axes, deliberately separate (they answer different questions):
      • index_of_dispersion — variance-to-mean of per-cell point counts on a cell_um lattice
        over the electrode volume (z ≤ z_top_um; only FULL cells binned, a partial top layer is
        dropped).  CSR/Poisson-random = 1.0; >1 clustered/agglomerated; <1 hyper-uniform.
        Density-corrected (raw CoV is NOT: a sparser phase has CoV_Poisson = 1/√mean even when
        perfectly random — both are reported).  ⚠ CAVEAT 1 (chain/blob phases): VGCF/PTFE
        fibres = ~dozens of collinear points per object, SuperP = small blobs — within-object
        correlation inflates D by construction, so D is a SAME-PHASE run-to-run comparator;
        cross-phase "who is better dispersed" must use the nn_* axis below.  ⚠ CAVEAT 2
        (review M2 — AM exclusion): additives are seeded in the MATRIX (never inside AM), so
        full-box cells inside AM are zero BY CONSTRUCTION → zero-inflation makes full-box D
        scale with point count (measured: CSR-in-matrix reads D 2.3→22 for 25k→400k pts at 33 %
        AM), swamping real agglomeration.  Pass am_c_um/am_r_um (AM sphere centres+radii, µm)
        to EXCLUDE cells whose centre lies inside an AM sphere: CSR-in-matrix then reads near 1
        again, with a RESIDUAL partial-cell inflation (boundary cells have less matrix volume) —
        so even masked-D comparisons should hold recipe + AM scaffold statistics fixed.
      • nn_med_um / nn_p90_um — nearest-additive distance from MATRIX sample points (SE), i.e.
        "how far is a matrix location from the network" (the SSRM mechanism analog).  This is
        the cross-phase axis and it INCLUDES morphology by design — a fibre network at the same
        point budget genuinely leaves farther matrix voids than dispersed dots, which is the
        transport-relevant fact.  nn_clustering = nn_med / nn_med_random, where the random
        reference is a Poisson field of the same count in the MATRIX volume (review M3):
        r_med = (3·ln2 / 4πn)^⅓ with n = N/(V_box·matrix_vol_frac), matrix_vol_frac = 1 − ΣV_AM/
        V_box from am_c_um/am_r_um (falls back to the full box without them — then CSR-in-matrix
        reads (V_matrix/V_box)^⅓ ≈ 0.73–0.95 < 1, documented offset).  >1 = matrix sees farther
        voids than same-count random-in-matrix, ≈1 = random, <1 = hyper-uniform coverage.

    No literature ABSOLUTE anchor is claimed (#284 SSRM is a different modality — §F1: relative
    comparisons between our runs only).
    Returns dict; {'reason': 'too_few_points'} below 50 pts."""
    pts = np.asarray(pts_um, np.float64)
    out = {'n_pts': int(len(pts)), 'cell_um': float(cell_um)}
    if len(pts) < 50:
        out['reason'] = 'too_few_points'
        return out
    lx, ly, lz = float(box_xy_um[0]), float(box_xy_um[1]), float(z_top_um)
    ncx, ncy, ncz = max(1, int(lx / cell_um)), max(1, int(ly / cell_um)), max(1, int(lz / cell_um))
    m = ((pts[:, 0] >= 0) & (pts[:, 0] < ncx * cell_um)
         & (pts[:, 1] >= 0) & (pts[:, 1] < ncy * cell_um)
         & (pts[:, 2] >= 0) & (pts[:, 2] < ncz * cell_um))
    ijk = np.floor(pts[m] / cell_um).astype(int)
    counts = np.bincount((ijk[:, 0] * ncy + ijk[:, 1]) * ncz + ijk[:, 2],
                         minlength=ncx * ncy * ncz).astype(np.float64)
    mat_frac = 1.0                                           # matrix volume fraction (M3 reference)
    if am_c_um is not None and am_r_um is not None and len(am_r_um):
        amc = np.asarray(am_c_um, np.float64); amr = np.asarray(am_r_um, np.float64)
        mat_frac = float(np.clip(1.0 - (4.0 / 3.0) * np.pi * float((amr ** 3).sum())
                                 / max(lx * ly * lz, 1e-12), 0.05, 1.0))   # overlaps ignored (slight
        out['matrix_vol_frac'] = round(mat_frac, 3)          #   under-count of matrix — conservative)
        # M2 mask: drop cells whose CENTRE is inside an AM sphere (structural zeros, not physics)
        cx = (np.arange(ncx) + 0.5) * cell_um
        cy = (np.arange(ncy) + 0.5) * cell_um
        cz = (np.arange(ncz) + 0.5) * cell_um
        inside = np.zeros((ncx, ncy, ncz), bool)
        for k in range(len(amr)):                            # few hundred AM spheres — cheap
            dx2 = (cx - amc[k, 0]) ** 2; dy2 = (cy - amc[k, 1]) ** 2; dz2 = (cz - amc[k, 2]) ** 2
            inside |= (dx2[:, None, None] + dy2[None, :, None] + dz2[None, None, :]) <= amr[k] ** 2
        keep = ~inside.reshape(-1)
        out['n_cells_masked_am'] = int((~keep).sum())
        counts = counts[keep]
    if counts.size >= 2:                                     # review m5: 1 cell → var(ddof=1)=NaN
        mu = float(counts.mean())
        out.update({'n_cells': int(counts.size), 'mean_per_cell': round(mu, 2),
                    'cov': round(float(counts.std(ddof=1)) / max(mu, 1e-12), 3),
                    'cov_poisson_floor': round(float(1.0 / np.sqrt(max(mu, 1e-12))), 3),   # plain float — np.float64 kills json.dump
                    'index_of_dispersion': round(float(counts.var(ddof=1)) / max(mu, 1e-12), 2)})
    else:
        out['reason'] = 'degenerate_lattice'
    if matrix_pts_um is not None and len(matrix_pts_um):
        from scipy.spatial import cKDTree
        mp = np.asarray(matrix_pts_um, np.float64)
        if len(mp) > nn_sample:
            mp = mp[np.random.default_rng(seed).choice(len(mp), nn_sample, replace=False)]
        d, _ = cKDTree(pts).query(mp, k=1)
        n_dens = len(pts) / max(lx * ly * lz * mat_frac, 1e-12)   # density in the MATRIX volume (M3)
        r_rand = (3.0 * np.log(2.0) / (4.0 * np.pi * n_dens)) ** (1.0 / 3.0)
        out.update({'nn_med_um': round(float(np.median(d)), 3),
                    'nn_p90_um': round(float(np.percentile(d, 90)), 3),
                    'nn_med_random_um': round(float(r_rand), 3),
                    'nn_clustering': round(float(np.median(d)) / max(float(r_rand), 1e-12), 2)})
    return out


def _selftest_dispersion():
    """A5 dispersion-metric checks: CSR calibration (D≈1, nn_clustering≈1), clustered detection,
    chain-phase caveat direction."""
    rng = np.random.default_rng(0)
    box, zt = (50.0, 50.0), 20.0
    mx = rng.uniform([0, 0, 0], [box[0], box[1], zt], size=(30000, 3))     # matrix sample
    ok = True
    # 1) CSR uniform points → D ≈ 1, nn_clustering ≈ 1  (calibrates both "random = 1" scales)
    pts = rng.uniform([0, 0, 0], [box[0], box[1], zt], size=(20000, 3))
    r = dispersion_metrics(pts, box, zt, matrix_pts_um=mx)
    e = 0.9 < r['index_of_dispersion'] < 1.1 and 0.9 < r['nn_clustering'] < 1.1
    ok &= e; print(f"CSR:       D={r['index_of_dispersion']}  nn×={r['nn_clustering']}  (expect ≈1, ≈1)  {'OK' if e else 'FAIL'}")
    # 2) clustered blobs (200 × 100 pts, σ=0.5µm) → D ≫ 1, nn_clustering > 1
    cent = rng.uniform([2, 2, 2], [box[0] - 2, box[1] - 2, zt - 2], size=(200, 3))
    pts = (cent[:, None, :] + rng.normal(0.0, 0.5, size=(200, 100, 3))).reshape(-1, 3)
    r = dispersion_metrics(pts, box, zt, matrix_pts_um=mx)
    e = r['index_of_dispersion'] > 5.0 and r['nn_clustering'] > 1.2
    ok &= e; print(f"clustered: D={r['index_of_dispersion']}  nn×={r['nn_clustering']}  (expect ≫1, >1.2)  {'OK' if e else 'FAIL'}")
    # 3) chain phase (randomly PLACED straight fibres): D inflated by within-object correlation
    #    even though placement is random — the documented cross-phase caveat (direction check only)
    p0 = rng.uniform([0, 0, 0], [box[0], box[1], zt], size=(500, 3))
    dirs = rng.normal(size=(500, 3)); dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
    pts = (p0[:, None, :] + dirs[:, None, :] * np.linspace(0, 10, 40)[None, :, None]).reshape(-1, 3)
    r = dispersion_metrics(pts, box, zt, matrix_pts_um=mx)
    e = r['index_of_dispersion'] > 1.5
    ok &= e; print(f"chains:    D={r['index_of_dispersion']}  nn×={r['nn_clustering']}  (expect D>1.5 — "
                   f"morphology confound, hence nn_* for cross-phase)  {'OK' if e else 'FAIL'}")
    # 4) review M2/M3 — AM-exclusion calibration: CSR-in-MATRIX points around 18 AM spheres
    #    (r=5µm, ~19 vol%).  Full-box D reads ≫1 by structural zero-inflation; the AM-masked D
    #    must fall back near 1.  nn_clustering with the matrix-volume reference reads ≈1 where
    #    the full-box reference reads <1 (matrix is denser than the box average).
    amc = np.array([[x, y, z] for x in (12.5, 25.0, 37.5) for y in (12.5, 25.0, 37.5)
                    for z in (6.0, 14.0)])
    amr = np.full(len(amc), 5.0)
    def _in_matrix(n):
        got, tot = [], 0
        while tot < n:
            cand = rng.uniform([0, 0, 0], [box[0], box[1], zt], size=(2 * n, 3))
            d2 = ((cand[:, None, :] - amc[None, :, :]) ** 2).sum(-1)
            keep = cand[(d2 > amr[None, :] ** 2).all(1)]
            got.append(keep); tot += len(keep)
        return np.concatenate(got)[:n]
    pmat, mmat = _in_matrix(20000), _in_matrix(30000)
    rf = dispersion_metrics(pmat, box, zt, matrix_pts_um=mmat)
    rm = dispersion_metrics(pmat, box, zt, matrix_pts_um=mmat, am_c_um=amc, am_r_um=amr)
    e = (rf['index_of_dispersion'] > 1.5 and rm['index_of_dispersion'] < rf['index_of_dispersion']
         and rm['index_of_dispersion'] < 1.5
         and 0.9 < rm['nn_clustering'] < 1.12 and rf['nn_clustering'] < rm['nn_clustering'])
    ok &= e; print(f"AM-excl:   D full-box={rf['index_of_dispersion']} → masked={rm['index_of_dispersion']}"
                   f" (cells−{rm.get('n_cells_masked_am')})  nn× full-box={rf['nn_clustering']} → "
                   f"matrix-ref={rm['nn_clustering']} (mat_frac={rm.get('matrix_vol_frac')})"
                   f"  (expect masked≈1, matrix-ref≈1)  {'OK' if e else 'FAIL'}")
    print('DISPERSION SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def _selftest_sheath():
    """A14 seed_sheath + sheath_ion_tradeoff checks (synthetic AM/SE — no MPM needed)."""
    ok = True
    box, dx = (10.0, 10.0, 10.0), 0.13
    C = np.array([[5.0, 5.0, 5.0]]); R = np.array([2.0])
    rng = np.random.default_rng(7)
    P, fid, hst = seed_sheath(300, box, dx, rng, am=(C, R), wrap_frac=1.0,
                              return_ids=True, return_host=True)
    # 1) thin radial skin: every point within [R, R+shell] of its host sphere
    rad = np.linalg.norm(P.astype(np.float64) - C[hst], axis=1) - R[hst]
    e = len(P) > 1000 and float(rad.min()) > -1e-4 and float(rad.max()) < SWCNT_SHELL + 1e-4
    ok &= e; print(f'skin:      n={len(P)} radial∈[{rad.min():.4f},{rad.max():.4f}]µm '
                   f'(shell {SWCNT_SHELL})  {"OK" if e else "FAIL"}')
    # 2) chain contiguity: consecutive same-chain gap ≈ step (continuous vein, not dust)
    o = np.lexsort((np.arange(len(P)), fid))                    # stable: within fid = along-chain
    Ps, fs = P[o].astype(np.float64), fid[o]
    gap = np.linalg.norm(np.diff(Ps, axis=0), axis=1)[np.diff(fs) == 0]
    step = 0.9 * dx
    e = len(gap) > 0 and float(np.median(gap)) < 1.6 * step and float(gap.max()) < 3.0 * step
    ok &= e; print(f'contig:    gap med={np.median(gap):.3f} max={gap.max():.3f}µm '
                   f'(step {step:.3f})  {"OK" if e else "FAIL"}')
    # 3) full-wrap coverage high / 4) partial wrap lower (band = Tabor 0.26)
    surf, _ = _fib_sphere_samples(C, R, 2000)
    try:
        from scipy.spatial import cKDTree
    except ImportError:
        print('scipy 없음 → coverage/trade-off 체크 스킵 (seed 체크만)')
        print('SHEATH SELFTEST', 'PASS' if ok else 'FAIL')
        return 0 if ok else 1
    cov_full = float((cKDTree(P).query(surf, k=1)[0] <= 0.26).mean())
    P35 = seed_sheath(300, box, dx, np.random.default_rng(7), am=(C, R), wrap_frac=0.35)
    cov_part = float((cKDTree(P35).query(surf, k=1)[0] <= 0.26).mean())
    e = cov_full >= 0.85 and cov_part <= 0.60 and cov_part < cov_full - 0.25
    ok &= e; print(f'coverage:  wrap1.0={100*cov_full:.1f}%  wrap0.35={100*cov_part:.1f}%  '
                   f'(expect ≥85 / ≤60)  {"OK" if e else "FAIL"}')
    # 5) trade-off: SE shell hugging the LOWER hemisphere at contact distance
    ns = 4000
    d = np.random.default_rng(1).normal(size=(ns, 3)); d /= np.linalg.norm(d, axis=1, keepdims=True)
    d[:, 2] = -np.abs(d[:, 2]); d /= np.linalg.norm(d, axis=1, keepdims=True)
    se = (C[0] + d * (R[0] + 0.05)).astype(np.float32)          # gap 0.05 < Hertz band
    tr = sheath_ion_tradeoff(P, C, R, se, n_samp=4000, wrap_frac=1.0)
    b = tr['per_band']['0.26']
    pb = tr['physical_bound']['blocked_of_se_contact_pct_upper_bound']
    # dense synthetic case: cloud spacing ≪ band → cloud blocked CONVERGES to the analytic bound
    e = (30.0 < b['se_contact_pct'] < 70.0 and b['blocked_of_se_contact_pct'] >= 70.0
         and abs(b['blocked_of_se_contact_pct'] + b['open_of_se_contact_pct'] - 100.0) < 1e-6
         and pb == 100.0 and abs(b['blocked_of_se_contact_pct'] - pb) < 15.0
         and tr['cloud_nn_spacing_um'] < 0.26)
    ok &= e; print(f"tradeoff:  se_contact={b['se_contact_pct']}% cloud-blocked={b['blocked_of_se_contact_pct']}% "
                   f"physical-bound={pb}% nn={tr['cloud_nn_spacing_um']}µm "
                   f"(dense → cloud≈analytic 수렴 확인)  {'OK' if e else 'FAIL'}")
    # 6) neighbour-AM burial drop: two touching spheres + in_am on the second
    C2 = np.array([[3.5, 5.0, 5.0], [6.5, 5.0, 5.0]]); R2 = np.array([2.0, 2.0])
    in2 = lambda q: np.linalg.norm(np.asarray(q, np.float64) - C2[1]) < R2[1]
    Pn, _f, hn = seed_sheath(300, box, dx, np.random.default_rng(3), am=(C2, R2),
                             in_am=in2, return_ids=True, return_host=True)
    m0 = hn == 0
    dmin = float(np.linalg.norm(Pn[m0].astype(np.float64) - C2[1], axis=1).min()) if m0.any() else np.inf
    e = dmin >= R2[1] - 1e-4
    ok &= e; print(f'burial:    host-0 min dist to AM-1 = {dmin:.3f}µm (R=2.0, ≥R expected)  '
                   f'{"OK" if e else "FAIL"}')
    # 7) representation budget cap visible (not silent): huge n_seg → ≤ max_pts
    Pc = seed_sheath(200000, box, dx, np.random.default_rng(5), am=(C, R), max_pts=5000)
    e = len(Pc) <= 5000
    ok &= e; print(f'budget:    n_seg=200k max_pts=5k → {len(Pc)} pts  {"OK" if e else "FAIL"}')
    # 8) tiny-cap 안정성 (리뷰 finding: wf≤0.025에서 (u,t) 직교성 붕괴 → skin 계약 위반이었음):
    #    wf=0.01에서도 모든 점이 [R, R+shell] 스킨 안에 있어야 함
    for wf_t in (0.001, 0.01, 0.02):
        Pt, _ft, ht = seed_sheath(80, box, dx, np.random.default_rng(11), am=(C, R),
                                  wrap_frac=wf_t, return_ids=True, return_host=True)
        rd = np.linalg.norm(Pt.astype(np.float64) - C[ht], axis=1) - R[ht]
        e = len(Pt) > 0 and float(rd.min()) > -1e-4 and float(rd.max()) < SWCNT_SHELL + 1e-4
        ok &= e
        print(f'tiny-cap:  wf={wf_t} radial∈[{rd.min():.4f},{rd.max():.4f}]µm (계약 [0,{SWCNT_SHELL}])'
              f'  {"OK" if e else "FAIL"}')
    print('SHEATH SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--recipe', default='', help="e.g. AM:SE:VGCF:PTFE=80:18:1:1")
    ap.add_argument('--rve-um', default='50,50,33', help='box Lx,Ly,Lz µm')
    ap.add_argument('--porosity', type=float, default=0.13)
    ap.add_argument('--dx-um', type=float, default=0.13)
    ap.add_argument('--selftest-dispersion', action='store_true',
                    help='A5/E2 dispersion-metric checks (CSR calibration / clustered / chain caveat)')
    ap.add_argument('--selftest-sheath', action='store_true',
                    help='A14 seed_sheath + sheath_ion_tradeoff checks (skin/contiguity/coverage/trade-off)')
    a = ap.parse_args()
    if a.selftest_dispersion:
        import sys
        sys.exit(_selftest_dispersion())
    if a.selftest_sheath:
        import sys
        sys.exit(_selftest_sheath())
    Lx, Ly, Lz = (float(v) for v in a.rve_um.split(','))
    solid = Lx * Ly * Lz * (1 - a.porosity)
    recipes = [a.recipe] if a.recipe else ['AM:SE:VGCF=72:27:1', 'AM:SE:VGCF:PTFE=80:18:1:1']
    rng = np.random.default_rng(0)
    for r in recipes:
        wt = parse_recipe(r)
        c = recipe_counts(wt, solid)
        print(f'\n=== {r}   (RVE {Lx:g}×{Ly:g}×{Lz:g}µm, solid {solid:,.0f}µm³) ===')
        print('  vol%: ' + '  '.join(f'{k} {100*v:.1f}' for k, v in c['vol_fracs'].items()))
        for ph in ('VGCF', 'SuperP', 'PTFE'):
            if ph in c:
                print(f'  {ph:7s} {c[ph]["n"]:>8,} objects  (vol {c[ph]["vol_um3"]:.0f}µm³)')
        if 'VGCF' in c:
            fib = seed_fibres(c['VGCF']['n'], (Lx, Ly, Lz), a.dx_um, rng)
            print(f'  → VGCF seeded {len(fib):,} material points '
                  f'({len(fib)/max(c["VGCF"]["n"],1):.0f} pts/fibre)')


if __name__ == '__main__':
    main()
