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

DENS = {'AM': 4.80, 'SE': 2.00, 'VGCF': 2.00, 'SuperP': 1.90, 'PTFE': 2.20}  # g/cm³
#   SE=2.00 = PROJECT CONVENTION (matches porosity_physics_regression RHO_SE + grade_engine);
#   real Li6PS5Cl crystallographic ≈ 1.85–1.88 (2.0 is the project's slightly-high standard).
#   Aligned 2026-06-30 (was 1.64, an out-of-band low value) so the zip additive counts use the
#   SAME SE density as the closed porosity model. ⚠ grade_engine.py:1217 still uses 1.85 (separate
#   composite-density calc) — flagged for the user; not changed here.
PHASE = {'SE': 1, 'AM': 0, 'VGCF': 2, 'SuperP': 3, 'PTFE': 4}                 # save-phase codes
# default geometry (µm)
VGCF_D, VGCF_L = 0.15, 10.0      # VGCF fibre Ø, length (Showa Denko VGCF-H; aspect ~67)
SP_D           = 0.20            # Super P / Super C carbon-black aggregate (sphere, particulate)
PTFE_D, PTFE_L = 0.25, 40.0      # PTFE FIBRIL Ø, length — dry-process hot-roll fibrillation makes long
                                 # thin threads (branch to 10s nm) spanning tens of NMC; LONGER + HIGHER
                                 # aspect (AR≈160) than VGCF (AR≈67) → reads as the spanning binder web,
                                 # not a short rod.  Soft binder FIBRE (RSC D5EE03240G; Front. Energy 2023.1336344)


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
    return {k: float(wt[k]) for k in ('VGCF', 'SuperP', 'PTFE') if wt.get(k, 0) > 0}


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
             'PTFE': np.pi * (ptfe_d / 2) ** 2 * ptfe_l}
    for a, w in add_wt.items():
        V_a = (w / 100.0) * M_tot / DENS[a]                            # µm³ of additive a
        out[a] = {'wt_pct': w, 'vol_um3': V_a, 'n': int(round(V_a / v_obj[a])),
                  'vol_per_obj_um3': v_obj[a], 'vol_pct_of_solid': round(100.0 * V_a / solid_vol, 3)}
    return out


def seed_fibres(n, box_um, dx_um, rng, in_am=None, L=VGCF_L, L_cv=0.0,
                curl=0.0, vol_conserve=False, vol_cv=0.0, nucleate=None, nucleate_frac=0.0,
                branch_frac=0.0, branch_n=2, branch_vol=0.3, branch_len=0.5,
                bridge_frac=0.0, bridge_drift=0.15, buckle_lam=0.0, buckle_strain=0.0, am_frac_fn=None,
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
        d0 = d0 / (np.linalg.norm(d0) + 1e-12)
        line = _grow(c, d0, Li, k, drift_to)
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
    'VGCF': {    # 1D fibre — morph = intended fibre treatment (TBD A4/lit; not yet seeded per-mixing)
        'ballmill': dict(regime='bulk',       morph='gently wavy fibre, well dispersed'),
        'thinky':   dict(regime='coat_embed', morph='embedded in porous SE coat (Kim2025: σ_e recovers)'),
        'handmix':  dict(regime='bulk',       morph='long, clustered (gentle mix)'),
    },
    'PTFE': {    # binder fibril — morph = intended fibrillation degree (TBD A4/lit)
        'ballmill': dict(regime='bulk',       morph='fibrillated binder web'),
        'thinky':   dict(regime='bulk',       morph='dry-process fibrillation (TBD A4)'),
        'handmix':  dict(regime='bulk',       morph='less fibrillated, clumpy (TBD A4)'),
    },
}

# backward-compat: Super P carbon-black mixing presets consumed by seed_carbon_black.
# Derived from the matrix above (drop the non-CB keys) so there is ONE source of truth.
CB_MIX = {m: {k: v for k, v in cfg.items() if k in ('k', 'surface_frac', 'step', 'clump')}
          for m, cfg in ADDITIVE_PROCESS['SuperP'].items()}


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--recipe', default='', help="e.g. AM:SE:VGCF:PTFE=80:18:1:1")
    ap.add_argument('--rve-um', default='50,50,33', help='box Lx,Ly,Lz µm')
    ap.add_argument('--porosity', type=float, default=0.13)
    ap.add_argument('--dx-um', type=float, default=0.13)
    a = ap.parse_args()
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
