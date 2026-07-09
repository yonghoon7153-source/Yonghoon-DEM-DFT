#!/usr/bin/env python3
"""3D MPM compaction — production: soft plastic SE (shape-flow) + rigid AM.

True-plastic, large-deformation, GPU MPM.  Captures what the DEM cannot: the SE
material points plastically FLOW (change shape) into the voids, conserving volume,
so the COMPOSITE densifies correctly (the DEM's rigid spheres can't void-fill).
von Mises (J2) per phase: SE soft+low-yield → flows; AM stiff+high-yield → jams.

Confined (oedometer) compaction by a servo platen to a target axial stress.
Default readout = wallP (the platen REACTION stress, Σ m·Δv/(dt·area)): it is the
true boundary BC and resolution-invariant, whereas the volume-mean Cauchy σzz
(--readout sigzz) is diluted by the well-resolved soft SE and over-compresses (the
2D "512 blocker" lesson, CLAUDE.md).  Both are printed every frame for comparison.
Porosity = 1 − solid_volume/(box_area·height).  Units: length dimensionless [0,1],
modulus/stress in GPa, so σzz and --target-gpa are literal GPa.

3D pure-SE calibration (GPU, n_grid=256): E_SE=1.53, ν_SE=0.49 (K≈25.5 GPa, the
real LPSC bulk → no volumetric over-crush), σy=0.30 → porosity ≈ 10 % @ 0.30 GPa
(Minnmann).  These are the defaults.  Then --material mix --am-frac <vol AM> for
the composite.

Run:  python3 scripts/mpm3d_compaction.py --material SE --n-grid 96 --arch cpu
      python3 scripts/mpm3d_compaction.py --material SE --n-grid 256 --arch cuda
"""
import argparse
import sys

import numpy as np


def binder_cap(w_wt, w_opt):
    """A3 non-monotonic binder efficiency vs PTFE wt% (dimensionless, peak = 1 at
    w=w_opt).  cap(w) = (w/w*)·exp(1 - w/w*): 0 at w=0, rises to 1 at w=w_opt, then
    decays for over-application (over-crosslink / agglomeration — #264 X14, Cho 2024).
    Physical: too little binder → weak binding (delamination-prone); optimal →
    max fibril densification (Hong 2026 void -6.4%p); too much → inert agglomerate,
    declining mechanical benefit.  w_opt → ∞ recovers a flat ~constant near w≪w_opt."""
    if w_opt <= 0 or w_wt <= 0:
        return 0.0
    r = w_wt / w_opt
    return max(0.0, r * np.exp(1.0 - r))


def build_rod_topology(fibre_np, phase_np, xs, rod_phases=(2, 4)):
    """Tier-2 --fibre-rod connectivity (host-side, testable).  Fibre points of a given id are appended
    CONTIGUOUSLY in walk order (ids are globally unique, branches get their own id), so chain neighbours
    are just adjacent array indices that share the same fibre id AND a rod phase (2=VGCF, 4=PTFE).
    Returns per-point int32 prev/next (−1 = none), float32 rest length to NEXT (rl), float32 rest bending
    vector b0 = x_prev−2x+x_next (the seeded curvature the bending constraint restores; ≈0 for a straight
    VGCF seed), and an int32 is_rod flag.  SuperP (3) = breakable aggregate, handled separately (TODO)."""
    import numpy as _np
    n = len(xs)
    prev = _np.full(n, -1, _np.int32); nxt = _np.full(n, -1, _np.int32)
    rl = _np.zeros(n, _np.float32); b0 = _np.zeros((n, 3), _np.float32)
    is_rod = _np.zeros(n, _np.int32)
    rp = set(rod_phases)
    same = lambda a, b: (0 <= a < n and 0 <= b < n and fibre_np[a] >= 0
                         and fibre_np[a] == fibre_np[b] and phase_np[a] == phase_np[b])
    for p in range(n):
        if int(phase_np[p]) not in rp or fibre_np[p] < 0:
            continue
        is_rod[p] = 1
        if same(p, p - 1):
            prev[p] = p - 1
        if same(p, p + 1):
            nxt[p] = p + 1
            rl[p] = float(_np.linalg.norm(xs[p + 1] - xs[p]))
    for p in range(n):                                  # rest curvature once neighbours are known
        if is_rod[p] and prev[p] >= 0 and nxt[p] >= 0:
            b0[p] = (xs[prev[p]] - 2.0 * xs[p] + xs[nxt[p]]).astype(_np.float32)
    return prev, nxt, rl, b0, is_rod


def _press_curl(p_gpa, curl_sat=0.095, p_char=0.30):
    """VGCF waviness as a FUNCTION OF THE PRESS p_gpa (GPa) — pressure-dependent shape generation.
    Real VGCF is a slender column (L/r~267): Euler sigma_cr ~ tens of MPa << the 0.1-0.6 GPa press, so
    it BUCKLES under compaction — but embedded in the SE (elastic foundation) it wrinkles at SHORT
    wavelength, not one big arc.  Returns the per-step worm-like curl that PRESCRIBES that press-
    dependent wrinkle in the seeder.  (The continuum MPM can't resolve a sub-grid fibre's bending
    stiffness from the grid, so the buckling is prescribed here, not emergent — the emergent version
    needs an explicit sub-grid Cosserat/bonded-rod on the fibre points; see the additive-mechanics
    backlog.)  Saturating (post-buckling grows, then the densifying SE pins it): curl(P) = curl_sat·
    (1-exp(-P/p_char)); calibrated curl(0.30 GPa)=0.060.  P=0.1→0.027, 0.3→0.060, 0.6→0.082, 1.0→0.092."""
    return float(curl_sat * (1.0 - np.exp(-max(float(p_gpa), 0.0) / p_char)))


def _am_surface_pts(centres, radii, n, rng, box_hi, per=6):
    """`n` box-frame points on the AM sphere surfaces — for PTFE binder nucleation-draping (the fibril
    web wraps AM).  EVEN per-sphere spread (golden-angle Fibonacci directions + a per-sphere random
    roll), NOT random pin-pricks.  `per` seed points per sphere are generated, then sampled to exactly
    `n` (with replacement if n exceeds per·N_AM, so the caller can hit a target nucleation FRACTION
    regardless of the AM count).  Clipped inside the box.  Buried points (a nucleus inside another AM)
    are left to seed_fibres' `in_am` drop — a buried nucleus grows no fibril, so it self-corrects."""
    N = len(centres)
    if N == 0 or n <= 0:
        return np.zeros((0, 3), np.float32)
    k = np.arange(per) + 0.5
    z = 1.0 - 2.0 * k / per
    rr = np.sqrt(np.maximum(0.0, 1.0 - z * z))
    th = (np.pi * (1.0 + 5.0 ** 0.5)) * k                                  # golden-angle azimuth
    base = np.stack([rr * np.cos(th), rr * np.sin(th), z], axis=1)         # (per,3) even unit dirs
    roll = rng.uniform(0.0, 2.0 * np.pi, size=N)                           # per-sphere azimuth variety
    cs, sn = np.cos(roll)[:, None], np.sin(roll)[:, None]
    dx = base[None, :, 0] * cs - base[None, :, 1] * sn
    dy = base[None, :, 0] * sn + base[None, :, 1] * cs
    dz = np.broadcast_to(base[None, :, 2], (N, per))
    pts = (centres[:, None, :] + np.stack([dx, dy, dz], 2) * radii[:, None, None]).reshape(-1, 3)
    pts = np.clip(pts, 1e-4, np.asarray(box_hi, np.float64) - 1e-4)        # keep inside the box
    idx = rng.choice(len(pts), n, replace=(n > len(pts)))
    return pts[idx].astype(np.float32)


def parse_args(argv):
    ap = argparse.ArgumentParser(description="3D MPM compaction (servo to target σzz).")
    ap.add_argument('--arch', default='cpu', choices=['cpu', 'gpu', 'cuda', 'vulkan'])
    ap.add_argument('--n-grid', type=int, default=96)
    ap.add_argument('--material', default='SE', choices=['SE', 'mix'])
    ap.add_argument('--am-frac', type=float, default=0.0, help='AM volume fraction of SOLID (mix)')
    ap.add_argument('--preset', default='none', choices=['none', 'real14'],
                    help='real14 = production input_real_14 (3-comp AM_P6/AM_S2/SE0.5um = 12:4:1, '
                         'actual vol AM:SE 73:27, 50um RVE → cross-validate porosity vs LIGGGHTS 15.6%%)')
    ap.add_argument('--am-scaffold', default='',
                    help='CSV of fixed AM (type,x,y,z,r in LIGGGHTS 0..0.05 units): AM become a fixed '
                         'grid obstacle and only SE is the MPM filler (real skeleton, no RSA AM, light)')
    ap.add_argument('--save-se', default='', help='write final SE point positions (npy) for morphology')
    ap.add_argument('--save-dg', default='', help='write accumulated plastic strain Σdg per SE point '
                    '(npy, SAME order as --save-se) → colour the morphology slice by plastic strain')
    ap.add_argument('--save-eps', default='', help='write accumulated TOTAL equivalent strain per SE point '
                    '(vs the seed sphere, INCL elastic compression — shows the confined interior too; npy)')
    ap.add_argument('--save-phase', default='', help='write per-point phase (1=SE, 0=AM) npy, SAME order as '
                    '--save-se → composite viz can colour SE by strain and draw AM grey')
    ap.add_argument('--save-fibre', default='', help='write per-point fibre id npy (-1 = SE/SuperP, ≥0 = a '
                    'VGCF/PTFE fibre index), SAME order as --save-se → render each fibre as an individual line')
    ap.add_argument('--save-fibre-dia', default='', help='write per-point relative fibre diameter npy (0 = SE; '
                    '∝√(V_i/L_i) for the volume-conserving PTFE draw) → viewer renders fibre thickness')
    ap.add_argument('--save-se-id', default='', help='write per-point SE PARTICLE id npy (≥0 = the real DEM SE '
                    'sphere index it was seeded from via --se-dump, -1 = carbon/none), SAME order as --save-se → '
                    'lets the voxel solver recover SE-SE plastic CONTACT AREAS (per-particle Holm constriction)')
    ap.add_argument('--save-metrics', default='',
                    help='write ALL raw MPM outputs (porosity, thickness, coverage, seed density, '
                         'grid/material params, stress) to a JSON — the structured source for the '
                         'webapp compare table + payload (so nothing is recomputed at coarse mesh res)')
    ap.add_argument('--se-frac', type=float, default=0.27,
                    help='scaffold SE volume fraction of SOLID (default 0.27 = real_14 actual; vary to '
                         'see porosity respond — final porosity is a RESULT of plastic SE fill, not assumed)')
    ap.add_argument('--se-dump', default='',
                    help='CSV of REAL SE positions (type,x,y,z,r, same units as --am-scaffold): seed '
                         'D1 SE spheres at the actual DEM SE centres instead of uniform cell-fill, so '
                         'SE volume·distribution are REAL → porosity·coverage EMERGE (no se_frac/targeting)')
    ap.add_argument('--coh', type=float, default=0.0,
                    help='SE cohesion / adhesion (GPa, Cauchy): cold-weld + vdW of the soft sulfide — '
                         'an attractive stress that reduces the net contact repulsion → densifies. '
                         'Real physics (not a target fudge); LPSC ~0.01-0.05 GPa.  Acts in compression.')
    ap.add_argument('--coh-ptfe', type=float, default=0.10,
                    help='A3: PEAK PTFE binder cohesion (GPa) at the optimal loading.  The PTFE fibril web '
                         'binds + densifies (Hong 2026 void -6.4%%p).  The EFFECTIVE binder cohesion is '
                         'NON-MONOTONIC in PTFE wt%% (see --binder-opt-wt): too little → weak binding / '
                         'delamination-prone; too much → over-crosslink / agglomeration (#264 X14, Cho 2024 '
                         'over-binder harmful) → declining mechanical benefit.')
    ap.add_argument('--binder-opt-wt', type=float, default=1.5,
                    help='A3: PTFE wt%% at which the binder benefit peaks (Hong ~1 wt%% optimal + a small '
                         'over-margin).  coh_PTFE(w) = coh_ptfe · (w/w*)·exp(1-w/w*) — rises to coh_ptfe at '
                         'w=w*, then decays for over-application.  Set w* large to recover the old constant.')
    ap.add_argument('--e-se', type=float, default=1.53, help='SE modulus (GPa); champion 1.53 (softened)')
    ap.add_argument('--e-am', type=float, default=140.0, help='AM modulus (GPa)')
    ap.add_argument('--sigma-y', type=float, default=0.30,
                    help='SE von Mises yield (GPa); 3D calib 0.30 -> pure-SE ~0.10 porosity @ 0.30 GPa (Minnmann)')
    ap.add_argument('--nu-se', type=float, default=0.49,
                    help='SE Poisson ratio (default 0.49 = 3D calib: K~25.5 GPa, the real LPSC bulk; '
                         'soft shear -> incompressible granular flow; nu<=0.45 over-crushes to 0 porosity)')
    ap.add_argument('--target-gpa', type=float, default=0.30, help='servo platen target σzz (GPa)')
    ap.add_argument('--am-load-frac', type=float, default=0.0,
                    help='Tabor-style wallP CONDITIONAL (DEM-stress coupling, scaffold only).  Fraction '
                         '[0,1) of the target axial load borne by the FROZEN AM skeleton (from DEM, e.g. '
                         'von-Mises partition f_AM = phi_AM*sVM_AM / (phi_AM*sVM_AM + phi_SE*sVM_SE), '
                         'volume fractions of SOLID).  The SE servo then stops when '
                         'wallP_SE + f_AM*target >= target, i.e. SE bears only its share target*(1-f_AM) -- '
                         'the frozen AM cannot register on wallP, so without this the SE bears ALL the load '
                         'and over-compresses in SE-poor / AM-load-bearing corners (mono-large 10:0).  '
                         '0 = off (SE bears all = original validated behaviour).  Like Tabor caps contact '
                         'AREA by F/H, this caps SE densification by the AM load-balance -- a physics '
                         'condition, NOT a DEM-porosity clamp (the MPM still COMPUTES porosity under the '
                         'corrected BC).  ROBUST gating via --floor-porosity (recommended): then the AM '
                         'share engages ONLY below the DEM floor → dense/SE-rich beds unchanged.')
    ap.add_argument('--floor-porosity', type=float, default=0.0,
                    help='ROBUST wallP-conditional gate (%%, set = the case DEM porosity).  The AM skeleton '
                         '(--am-load-frac) bears its share ONLY once the bed compresses to this DEM rigid-'
                         'packing floor (where the AM jams).  ABOVE it the SE bears the full load → dense / '
                         'SE-rich beds that reach target above the floor are UNCHANGED (no over-correction); '
                         'BELOW it the AM share ramps in → SE-poor/mono-large over-compression stops near the '
                         'floor.  This is the all-regime-safe gate (flat --am-load-frac alone over-corrects '
                         'dense beds).  0 = off.')
    ap.add_argument('--floor-engage', type=float, default=1.5,
                    help='ramp width (%%) over which the AM-skeleton load engages below --floor-porosity '
                         '(numerical smoothness; smaller = stiffer jam).')
    ap.add_argument('--compact-to', type=float, default=0.0,
                    help='displacement-driven: descend the platen until bed porosity ≤ this %% then HOLD, '
                         'regardless of stress — for a target-density demo (e.g. 15).  0 = stress servo (default)')
    ap.add_argument('--am-jam', action='store_true',
                    help='OPTION C (geometric AM-jamming, scaffold only): the platen CANNOT penetrate the '
                         'PERCOLATING (floor-connected) frozen-AM skeleton — descent hard-stops at that '
                         'cluster top.  Makes the MPM jam at the AM-packing porosity GENUINELY (geometry '
                         'only — no f_AM / floor / DEM-porosity import); SE-poor AM-rich corners stop near '
                         'the DEM-anchored true porosity, SE-rich (no tall floor-connected cluster) keep '
                         'plastic void-fill unchanged (SE servo stops first).  Needs scipy.')
    ap.add_argument('--se-am-robust', type=float, default=6.0,
                    help='ROUND 4 (flexible PHYSICAL coef for --se-am-drag): drag turns OFF above this many AM '
                         'load-path layers (bed_depth / AM_diameter).  THICK beds (≥this) → AM multilayer bears '
                         'the platen load (§13 thickness-escape: 8mAh reliable w/o drag) → robust=0 → no drag.  '
                         'THIN beds → robust→1 → full drag.  Physically-derived (load-path depth), not target-tuned.')
    ap.add_argument('--se-am-robust-width', type=float, default=3.0,
                    help='ramp width (AM layers) over which the --se-am-robust factor goes 1→0.')
    ap.add_argument('--am-jam-tol', type=float, default=0.05,
                    help='AM-AM contact tolerance for --am-jam, as a fraction of median AM radius (near-contact).')
    ap.add_argument('--se-am-drag', type=float, default=0.0,
                    help='SE-AM CONFINEMENT (physical, scaffold only): damp SE grid velocity near the frozen AM, '
                         'scaled by the LOCAL AM fraction (3x3x3) — so SE conforms locally (Sakuda fusion) but is '
                         'resisted from long-range MIGRATION past the AM skeleton.  AM density modulates it → '
                         'SE-poor (dense AM, confined) stays ~DEM, SE-rich (sparse AM) keeps plastic void-fill — '
                         'regime auto, no DEM import / no forced jam.  v *= max(0, 1 − drag·AM_frac).  0 = off. Needs scipy.')
    ap.add_argument('--readout', default='wallP', choices=['wallP', 'sigzz'],
                    help='servo signal: wallP (platen reaction, resolution-invariant) or sigzz (volume-mean)')
    ap.add_argument('--protocol', default='servo', choices=['servo', 'hold'],
                    help='servo = bidirectional, equilibrate AT target; hold = LIGGGHTS protocol '
                         '(descend to target, FIX the platen, relax) — porosity = value at first 300 MPa')
    ap.add_argument('--init-solid', type=float, default=0.35,
                    help='initial solid fraction (loose; keep <=0.38 RSA saturation)')
    ap.add_argument('--r-am', type=float, default=0.045, help='AM radius (box units; raise n-grid for 12:4:1)')
    ap.add_argument('--r-se', type=float, default=0.018, help='SE radius (box units)')
    ap.add_argument('--frames', type=int, default=400)
    ap.add_argument('--print-every', type=int, default=5,
                    help='print a progress line every N frames (lower = watch a heavy 300M-pt run '
                         'advance, so it does not look frozen during the 20-frame silence)')
    ap.add_argument('--sub', type=int, default=40)
    ap.add_argument('--dt', type=float, default=2.0e-4)
    ap.add_argument('--seed', type=int, default=3)
    ap.add_argument('--gpu-mem', type=float, default=3.0)
    ap.add_argument('--lateral-box', type=float, default=0.05,
                    help='REAL LIGGGHTS lateral box size (the x,y RVE width in dump units; default 0.05 '
                         '= 50µm).  Scaffold scl = WIDTH/lateral_box; pass the case box_x so non-50µm '
                         'RVEs map correctly.  (mpm_input_from_case.py wires this from input_params box_x.)')
    ap.add_argument('--nz', type=int, default=0,
                    help='vertical grid cells (THICK films): 0 = auto (fit the electrode, ≥ n_grid).  '
                         'Non-cubic grid n_grid×n_grid×nz, uniform dx=1/n_grid → tall electrodes fit '
                         'without crushing SE resolution (a 158µm film no longer overflows the unit box).')
    ap.add_argument('--periodic', action='store_true',
                    help='x,y periodic RVE (match the DEM "boundary p p f"): no lateral walls, '
                         'particles + AM/SE masks wrap → boundary grains get bulk compaction + '
                         'coverage (default = rigid lateral walls, the validated production box)')
    ap.add_argument('--quiet', action='store_true')
    ap.add_argument('--add-recipe', default='',
                    help='seed conductive additives as extra MPM phases.  The ADDITIVE wt%% is its share of '
                         'the 100%% total electrode (AM+SE+additives); the AM:SE in the recipe is IGNORED — '
                         'AM:SE comes from the REAL scaffold (not hardcoded).  So "AM:SE:VGCF=80:18:1" → VGCF '
                         '1 wt%% (AM:SE fill the other 99%% at the scaffold ratio); "AM:SE:VGCF:PTFE=80:18:1:1" '
                         '→ VGCF 1 + PTFE 1 wt%% (AM:SE = 98%%).  "VGCF=1" works too.  VGCF & SuperP are separate. '
                         'fibres=point-chains, SuperP=blobs, avoid fixed AM.  Auto-enables SE cohesion '
                         '(--coh 0.02) unless --coh given.  Needs --am-scaffold.')
    ap.add_argument('--add-l-cv', type=float, default=0.4,
                    help='fibre length variation (coefficient of variation) for VGCF/PTFE — real fibres '
                         'have a length spread; lognormal mean-preserving so counts/volume unchanged. 0=fixed.')
    ap.add_argument('--vgcf-curl', type=float, default=-1.0,
                    help='VGCF path waviness (per-step worm-like kick, rad).  <0 (default) = AUTO from the '
                         'press: curl(P)=0.095·(1-exp(-P/0.30)) (buckling proxy — more press → more wrinkle, '
                         'calibrated 0.06 @ 0.30 GPa; real VGCF sigma_cr~tens of MPa < press, embedded → short-'
                         'wavelength waviness).  >=0 = fixed value (0 = perfectly straight).  See _press_curl.')
    ap.add_argument('--fibre-rod', action='store_true',
                    help='Tier-2: give VGCF/PTFE fibres an explicit sub-grid rod (XPBD distance+bending) so '
                         'they BUCKLE *emergently* under the press instead of the prescribed --vgcf-curl.  Real '
                         'fibre stiffness drives it (decoupled from the softened SE continuum E); VGCF is auto-'
                         'seeded straight when on.  Physics+solver verified in scripts/fibre_rod_reference.py '
                         '(P_cr==Euler).  OFF (default) = Tier-1 curl=f(P).  SuperP aggregate = TODO.')
    ap.add_argument('--rod-stiff', type=float, default=0.6,
                    help='--fibre-rod bending stiffness (PBD 0..1; VGCF uses this, PTFE 0.2× softer).  Higher = '
                         'longer buckling wavelength.  Calibrate on the single-fibre unit test to Euler σ_cr.')
    ap.add_argument('--rod-iters', type=int, default=15,
                    help='--fibre-rod constraint-projection iterations per substep (Jacobi, under-relaxed).')
    ap.add_argument('--fibre-buckle', action='store_true',
                    help='VGCF: seed the PHYSICS-PRESCRIBED buckle a real fibre would take at the press '
                         '(Winkler wavelength λ=2π(EI/E_SE)^¼≈1.5µm, amplitude from --buckle-strain, per-fibre '
                         'orientation-weighted cos²θ).  The honest MPM answer since the frozen-AM scaffold '
                         'cannot compress the fibre to buckle it emergently (fibre_rod_mpm_design §RESULT). '
                         'Replaces --vgcf-curl for VGCF.')
    ap.add_argument('--buckle-strain', type=float, default=0.42,
                    help='--fibre-buckle FULLY-AM-CONFINED axial strain (a fibre pinched on all sides sees the '
                         'macro bed strain ~0.42 for loose φ0~0.5→300 MPa).  Per-fibre effective strain = this '
                         '×cos²θ×(local AM fraction), so open-pore fibres buckle far less → mean straightness '
                         '≈0.96-0.97 (SEM-consistent band).  A SEM-match MORPHOLOGY KNOB, not a derived transport '
                         'result (the shape is sub-voxel → does not change σ_e at production resolution).')
    ap.add_argument('--fibre-stiff', action='store_true',
                    help='VGCF as a LOAD-BEARING rigid strut: pin the VGCF-occupied grid cells (v=0, like the '
                         'frozen AM), because real graphite VGCF (E~200 GPa, σ_y≫0.3 GPa press) does NOT compress '
                         'at 300 MPa — it RESISTS compaction.  Tests whether a compaction-resisting fibre network '
                         'moves porosity toward the Cho-2024 "conflicting roles" direction (porosity flat/up '
                         'instead of the passive volume-fill drop).  This is the STIFFNESS/load lever, orthogonal '
                         'to --vgcf-curl/--fibre-buckle (shape).  Scaffold-only.  It is the UPPER bound: fully '
                         'rigid = no buckling relief and (crucially) the frozen AM cannot rearrange, so the '
                         'AM-rearrangement half of the real prop-open is DEM co-compaction territory.')
    ap.add_argument('--mixing', default='ballmill', choices=['ballmill', 'thinky', 'handmix'],
                    help='Super P (carbon black) dispersion (lit morphology): ball-mill/Thinky = short '
                         'branched aggregates, uniform, intimately coating the AM; hand-mix = larger '
                         'clustered agglomerates, non-uniform.  (VGCF/PTFE fibres unaffected.)')
    ap.add_argument('--fibre-align', type=float, default=1.0,
                    help='PRESS-INDUCED IN-PLANE fibre alignment (affine): λ_z = axial stretch of the bed under '
                         'uniaxial compaction (loose→pressed).  1.0 = isotropic (default); <1 tilts fibres toward '
                         'the plane perpendicular to the press (tanθ = tanθ0/λ_z), as real 300-MPa-pressed VGCF '
                         'does.  Physically λ_z = (1−ε_loose)/(1−ε_pressed) ≈ 0.71 for 40%%→15%% porosity; the zip '
                         'generator bakes the case-specific value.  In-plane fibres also buckle less (smaller d0_z).')
    ap.add_argument('--ptfe-fibril', type=float, default=-1.0,
                    help='PTFE fibrillation degree ∈(0,1] set by the mixing SHEAR (dry-process): high-shear '
                         'ball-mill/Thinky unravel PTFE into a BRANCHED fibril web (1.0); low-shear hand-mix '
                         'leaves poorly-networked, clumpy fibrils (<1).  <0 = AUTO from --mixing (ball-mill/'
                         'Thinky 1.0, hand-mix 0.45).  Scales branch_frac (the web) only → shapes the σ_e-network '
                         'MORPHOLOGY + PTFE-on-AM coverage (pending a resolving-grid σ_e run); porosity is '
                         'UNAFFECTED (soft PTFE flows + volume-pinned, like SuperP).  DIRECTION lit-supported '
                         '(dry-fibrillation); MAGNITUDE a tunable estimate, NOT anchored (backlog §F1).')
    ap.add_argument('--ptfe-press-curl', action='store_true',
                    help='PTFE web tangle (curl) scales with the target press toward 0.40, for parity with '
                         "VGCF's press-curl.  OFF by default (opt-in) because the press MAGNITUDE for a SOFT "
                         'fibril is UNANCHORED — curl_sat=0.40/p_char=0.30 are BORROWED from VGCF\'s stiff-'
                         'column Euler-buckling calibration and have no PTFE basis (backlog §F1: unanchored → '
                         'keep out of the production number).  Provided for A/B comparison only.  (align, by '
                         "contrast, is auto-baked: its λ_z is DERIVED from the measured compaction ratio.)")
    ap.add_argument('--ptfe-am-bind', type=float, default=0.5,
                    help='PTFE binder AM-wrap strength = the target FRACTION of PTFE nucleations that DRAPE AM '
                         'surfaces (vs the CBD carbon).  PTFE is a binder that wraps/bridges AM (Lee 2025), not '
                         'only carbon; 0 = pure-CBD (no AM wrap), 1 = all on AM.  Held FIXED independent of the '
                         'carbon point count (else the wrap strength would swing with recipe).  In a PTFE-only '
                         'recipe (no carbon) AM is the whole pool.  MAGNITUDE (default 0.5) a conservative '
                         'tunable hook, NOT anchored (backlog §F1).')
    ap.add_argument('--coh-sdcp', type=float, default=0.10,
                    help='SDCP binder cohesion (GPa, Cauchy) among SDCP/SE points — BULK film integrity, '
                         'variant-independent + FLAT in wt% (no PTFE-style binder_cap arc: anchoring has no '
                         'fibrillation/over-crosslink peak mechanism).  The AM-interface anchoring '
                         '(γ≈0.93 J/m² doped / 0.42 neutral — INTERIM MLIP −4.8/−3.0 eV, DFT U-ramp pending; '
                         '~10× PTFE γ) is represented STRUCTURALLY (film seeded ON the AM, seed_coat) — a '
                         'boundary-adhesion energy term is future work; do NOT put the interface γ-ratio '
                         'into this bulk coh (wrong term, both directions).')
    ap.add_argument('--sdcp-neutral', action='store_true',
                    help='SDCP NEUTRAL (−SO₃H) variant — recorded as provenance for STEP3 σ-weighting.  '
                         'Anchoring γ 0.42 vs doped 0.93 J/m² (INTERIM MLIP −3.0/−4.8 eV, DFT pending) lives '
                         'in the AM-interface term (future), NOT the bulk coh; conductivity: undoped PEDOT '
                         '~1e-3..1e-1 S/cm ≈ AM-scale → still an AM-grade conductor in the binary econn '
                         '(NOT dropped — an insulator-drop would misclassify by ~13 orders vs ≤1).  '
                         'Default = doped (−SO₃⁻, the self-doped production state).')
    ap.add_argument('--sdcp-surface-frac', type=float, default=-1.0,
                    help='SDCP AM-ANCHORED share of the particles (sulfonate anchoring + ordered-mixing '
                         'decoration).  <0 = AUTO from the process row (ballmill/thinky 0.5; handmix 0.3 — '
                         'a ~3µm agglomerate decorates a 5µm host far more weakly than a 0.3µm single).  '
                         'MAGNITUDE a conservative tunable hook, NOT anchored (backlog §F1) — SEM/EDS anchor.')
    ap.add_argument('--sdcp-clump', type=int, default=-1,
                    help='SDCP anchored-cluster size at NCM surfaces (ordered-mixing decoration).  <=0 = AUTO '
                         'from the process row (all mixings 1 = S3-faithful singles).  >1 seeds clusters of '
                         'that size at AM surfaces — tests the NCM-cluster hypothesis (§3.7); MAGNITUDE '
                         'un-anchored §F1 hook (payload SDCP→AM proximity + SEM/EDS discriminate).')
    ap.add_argument('--sdcp-agg-d', type=float, default=-1.0,
                    help='SDCP surviving AS-MADE agglomerate Ø (µm) — hand-mix has no milling energy, so the '
                         'as-made ~3µm particles (manuscript Fig S2) survive un-milled and ALL SDCP seeds as '
                         '~agg_d clusters (anchored share draped on AM + bulk share in-pore).  <0 = AUTO from '
                         'the process row (handmix 3.0 = S2 anchor; ballmill/thinky 0 = milled S3 singles); '
                         '0 forces singles.  SIZE anchored (S2); survival-at-low-shear = physics direction.')
    ap.add_argument('--dilate-z', type=float, default=1.0,
                    help='STIFF-FIBRE BED DILATION: stretch the frozen scaffold (AM + SE seed) z-offsets by this '
                         'factor before compaction — the prop-open thickness response a frozen-AM MPM cannot '
                         'produce emergently (skeleton rearrangement = granular force-chain physics = DEM-class). '
                         'The VALUE is derived upstream (mpm_input_from_case) from λ_dz = (1+φ_VGCF)·(1−ε_DEM)/'
                         '(1−ε_real), ε_real = ε_DEM + 0.5pp/wt%(VGCF) — ONE empirical number (Cho 2024 LPSCl+VGCF '
                         'slope); Philipse rod-jamming φ_c≈5.4/(L/D)≈8vol% bounds the regime (our strut onset '
                         'reproduces it).  Thickness/porosity respond BY CONSTRUCTION; coverage/network/strain '
                         'respond EMERGENTLY on the dilated bed.  z-only affine = die-press global mode (lateral '
                         'fixed); local non-affine rearrangement stays DEM territory.  1.0 = off (soft additives: '
                         'PTFE/SuperP flow into pores, no dilation — their thickness pin is the physics).')
    return ap.parse_args(argv)


def main(argv):
    args = parse_args(argv)
    import taichi as ti
    arch = {'gpu': ti.gpu, 'cuda': ti.cuda, 'vulkan': ti.vulkan, 'cpu': ti.cpu}[args.arch]
    kw = dict(arch=arch, default_fp=ti.f32, random_seed=args.seed)
    if args.arch in ('gpu', 'cuda'):
        # cap --gpu-mem to the real USABLE VRAM so a zip baked for a big GPU (e.g. --gpu-mem 28) doesn't
        # OOM at ti.init on a smaller card (RTX 3090 = 24GB).  Taichi PRE-ALLOCATES device_memory_GB up
        # front, so it must fit in FREE VRAM (not just total) — a desktop card driving a display, or a
        # leftover run, has free < total → cuMemAlloc CUDA_ERROR_OUT_OF_MEMORY.  Cap to min(85% total,
        # 90% free); if nvidia-smi is unavailable/unparseable, fall back to a safe 20GB (never leave 28).
        _cap = 20.0
        _msg = 'nvidia-smi unavailable → safe default'
        try:
            import subprocess as _sp
            _q = _sp.run(['nvidia-smi', '--query-gpu=memory.total,memory.free',
                          '--format=csv,noheader,nounits'],
                         capture_output=True, text=True, timeout=10).stdout.strip().split('\n')[0]
            _tot_mb, _free_mb = (int(_x) for _x in _q.split(','))
            _cap = max(2.0, round(min(_tot_mb * 0.85, _free_mb * 0.90) / 1024.0, 1))
            _msg = f"total {_tot_mb/1024:.0f}GB, free {_free_mb/1024:.0f}GB"
        except Exception as _e:
            _msg = f"nvidia-smi query failed ({_e}) → safe default"
        if args.gpu_mem > _cap:
            print(f"  [mpm] --gpu-mem {args.gpu_mem} > usable VRAM ({_msg}) → capping to {_cap}GB")
            args.gpu_mem = _cap
        kw['device_memory_GB'] = args.gpu_mem
    ti.init(**kw)

    n_grid = args.n_grid
    dx = 1.0 / n_grid; inv_dx = float(n_grid)               # uniform cell size (lateral-based); z may exceed 1
    nz = n_grid                                             # vertical grid cells: = n_grid (cubic) unless a
    #   tall scaffold electrode needs more (set in the scaffold branch).  Fields are (n_grid,n_grid,nz).
    PERIODIC = bool(args.periodic)                          # x,y periodic RVE (opt-in); default lateral walls
    dt = args.dt                                           # per-point p_vol/p_mass (set in build):
    #   soft SE → fine voxelization (dx/2), rigid AM → coarse (dx) to cap memory at 12:1 ratio
    def lame(E, nu):
        return E / (2 * (1 + nu)), E * nu / ((1 + nu) * (1 - 2 * nu))
    MU_SE, LA_SE = lame(args.e_se, args.nu_se); MU_AM, LA_AM = lame(args.e_am, 0.30)
    K_SE = LA_SE + 2.0 * MU_SE / 3.0                        # SE bulk modulus (GPa) — stiff if ν→0.49
    YIELD_SE = args.sigma_y; YIELD_AM = 1.0e4               # AM ~rigid (no yield)
    COH = float(args.coh)                                   # SE cohesion/adhesion (GPa, Cauchy)
    if args.add_recipe and COH == 0.0:                      # additive regime: SE cold-weld/vdW ON (user
        COH = 0.02                                          # decision) — plain porosity runs stay coh=0
    # CFL-safe dt: cap by the stiffest material P-wave speed c=√((λ+2µ)/ρ), ρ=1.  With AM as a
    # MATERIAL (preset/mix, E_AM=140) the default dt blows up at high n_grid (CUDA illegal
    # address); the scaffold (AM = grid mask, only soft SE) keeps the default dt.
    _has_am_mat = (args.preset == 'real14') or (args.material == 'mix' and not args.am_scaffold)
    _M = LA_SE + 2.0 * MU_SE
    if _has_am_mat:
        _M = max(_M, LA_AM + 2.0 * MU_AM)
    if args.add_recipe:                                     # additive stiffness can EXCEED the SE stack
        _rc_up = args.add_recipe.upper()                    # (VGCF E=10 rode the old margin; SDCP E=23.6
        for _anm, _aE, _anu in (('VGCF', 10.0, 0.30), ('SDCP', 23.6, 0.35)):   # would blow the CFL) → cap dt
            if _anm in _rc_up:
                _mu_a, _la_a = lame(_aE, _anu)
                _M = max(_M, _la_a + 2.0 * _mu_a)
    dt = min(args.dt, 0.4 * dx / (_M ** 0.5))

    FLOOR = 0.10; SW = (0.18, 0.82)                         # confined box in x,y
    WIDTH = SW[1] - SW[0]
    WALL0 = 0.60; WALL_MIN = 0.105                          # just above FLOOR (servo stops earlier)
    am_frac = args.am_frac if args.material == 'mix' else 0.0

    # ── build material points: place spheres (two-tier RSA: big AM brute + small SE
    #    fine-grid, like the DEM — a uniform brute is O(N²) and stalls) ───────────
    rng = np.random.default_rng(args.seed)
    am_c = None; am_r = None; AM_vol = 0.0; am_top = 0.0; um_box = 0.0; am_jam_z = 0.0   # fixed-AM scaffold bookkeeping
    if args.am_scaffold:
        # DEM→MPM scaffold: real AM are FIXED (loaded from the LIGGGHTS dump) and become a grid
        # obstacle; only SE is the MPM material, RSA-packed into the interstices to a target volume
        # fraction.  The plate then plastically compacts the SE around the fixed real skeleton, so
        # the porosity is a RESULT of the SE plastic fill (drops from the rigid-RSA value), not assumed.
        SW = (0.04, 0.96); WIDTH = SW[1] - SW[0]; FLOOR = 0.05
        amraw = np.atleast_2d(np.loadtxt(args.am_scaffold, delimiter=','))  # 2D even for a 1-row CSV
        scl = WIDTH / args.lateral_box                         # box units per LIGGGHTS unit (lateral→WIDTH)
        DZ = max(float(args.dilate_z), 1.0)                    # stiff-fibre bed dilation (z-offsets only;
        if DZ > 1.0:                                           #  radii unchanged → particles move APART = prop-open)
            print(f'  [dilate-z] scaffold z-offsets ×{DZ:.4f} (stiff-fibre prop-open; thickness/porosity by '
                  f'construction, coverage/network EMERGENT on the dilated bed)')
            if args.am_jam or args.floor_porosity > 0 or args.se_am_drag > 0:
                print('  [dilate-z] ⚠ --am-jam / --floor-porosity / --se-am-drag are anchored to the UNDILATED '
                      'packing (contact tol, DEM-porosity clamp, layer count) — their gates are NOT dilation-'
                      'aware; verify or disable them on a dilated bed.')
        am_c = np.column_stack([SW[0] + amraw[:, 1] * scl, SW[0] + amraw[:, 2] * scl,
                                FLOOR + amraw[:, 3] * scl * DZ]).astype(np.float64)
        am_r = (amraw[:, 4] * scl).astype(np.float64)
        AM_vol = float(np.sum((4.0 / 3.0) * np.pi * am_r ** 3))
        am_top = float((am_c[:, 2] + am_r).max())
        WALL0 = am_top + 0.05; WALL_MIN = FLOOR + 0.01
        r_se3 = 0.0005 * scl                                  # SE 0.5µm → box units
        um_box = 1000.0 / scl                                 # µm per box unit (lateral_box LIGGGHTS u = WIDTH)
        if args.am_jam:                                       # ★ OPTION C: percolating-AM rigid jam height
            # The platen cannot penetrate the floor-connected (percolating) frozen-AM skeleton.  Compute
            # AM-AM near-contacts → connected components → keep components touching the FLOOR → jam height
            # = max(z+r) over those AM.  SE-poor AM-rich → AM percolate → jam_z ≈ am_top (platen stops near
            # the DEM bed top = true porosity, geometry-derived, no anchor import).  SE-rich → no tall
            # floor-connected cluster → jam_z stays low → SE servo stops the platen first → void-fill intact.
            try:
                from scipy.spatial import cKDTree
                from scipy.sparse import coo_matrix
                from scipy.sparse.csgraph import connected_components
                _rmed = float(np.median(am_r)); _tol = max(args.am_jam_tol, 0.0) * _rmed
                _pp = cKDTree(am_c).query_pairs(r=float(2.0 * am_r.max() + _tol), output_type='ndarray')
                if len(_pp):
                    _d = np.linalg.norm(am_c[_pp[:, 0]] - am_c[_pp[:, 1]], axis=1)
                    _pp = _pp[_d <= (am_r[_pp[:, 0]] + am_r[_pp[:, 1]] + _tol)]      # actual (near-)contacts
                _N = len(am_c)
                if len(_pp):
                    _g = coo_matrix((np.ones(len(_pp)), (_pp[:, 0], _pp[:, 1])), shape=(_N, _N))
                    _, _lab = connected_components(_g, directed=False)
                else:
                    _lab = np.arange(_N)
                _floor_am = (am_c[:, 2] - am_r) <= (FLOOR + 1.5 * _rmed)             # AM resting on/near the floor
                _perc = np.isin(_lab, np.unique(_lab[_floor_am])) if _floor_am.any() else np.zeros(_N, bool)
                if _perc.any():
                    am_jam_z = float((am_c[_perc, 2] + am_r[_perc]).max())
                print(f'  [am-jam] percolating AM skeleton: {int(_perc.sum())}/{_N} floor-connected, '
                      f'jam_z={am_jam_z:.3f} box = bed {(am_jam_z - FLOOR) * um_box:.1f}µm '
                      f'(am_top {am_top:.3f}) → platen hard-stops at the rigid AM top.')
            except Exception as _e:
                print(f'  [am-jam] DISABLED ({_e}) → no geometric jam'); am_jam_z = 0.0
        # THICK-FILM vertical grid: a tall electrode (z_extent > lateral) would overflow the cubic
        # unit box (158µm/30µm → z maps to ~5).  Size nz so the grid spans [0, WALL0] at the SAME
        # dx as the lateral cells → SE keeps its calibrated resolution.  nz = n_grid when it fits
        # (real_14 short film → cubic, unchanged); larger only for thick films.
        nz = args.nz if args.nz > 0 else max(n_grid, int(np.ceil((WALL0 + 0.02) * n_grid)))
        # periodic (x,y) RVE box in grid cells — matches the DEM 'boundary p p f': a boundary AM/SE
        # gets wrapped images so it compacts + is covered like the bulk (opt-in via --periodic).
        LO_m = int(round(SW[0] * n_grid)); WC_m = int(round((SW[1] - SW[0]) * n_grid))

        def _raster(mask, cx, cy, cz, rr, setval):
            """rasterise a sphere into the (n_grid³) mask; x,y wrap into [LO_m,LO_m+WC_m) when PERIODIC,
            else clamp to the grid (byte-identical to the old block-slice fill)."""
            iz0 = max(int(np.floor((cz - rr) * n_grid)), 0)
            iz1 = min(int(np.ceil((cz + rr) * n_grid)), nz)   # z spans nz cells (≥ n_grid for thick films)
            if iz1 <= iz0:
                return
            if PERIODIC:
                ix = np.arange(int(np.floor((cx - rr) * n_grid)), int(np.ceil((cx + rr) * n_grid)))
                iy = np.arange(int(np.floor((cy - rr) * n_grid)), int(np.ceil((cy + rr) * n_grid)))
            else:
                ix = np.arange(max(int(np.floor((cx - rr) * n_grid)), 0), min(int(np.ceil((cx + rr) * n_grid)), n_grid))
                iy = np.arange(max(int(np.floor((cy - rr) * n_grid)), 0), min(int(np.ceil((cy + rr) * n_grid)), n_grid))
            if len(ix) == 0 or len(iy) == 0:
                return
            iz = np.arange(iz0, iz1)
            X, Y, Z = np.meshgrid((ix + 0.5) / n_grid, (iy + 0.5) / n_grid, (iz + 0.5) / n_grid, indexing='ij')
            inside = (X - cx) ** 2 + (Y - cy) ** 2 + (Z - cz) ** 2 <= rr * rr
            if not inside.any():
                return
            ii, jj, kk = np.nonzero(inside)
            if PERIODIC:
                wx = LO_m + ((ix[ii] - LO_m) % WC_m + WC_m) % WC_m
                wy = LO_m + ((iy[jj] - LO_m) % WC_m + WC_m) % WC_m
            else:
                wx, wy = ix[ii], iy[jj]
            mask[wx, wy, iz[kk]] = setval

        pin_np = np.zeros((n_grid, n_grid, nz), np.int32)     # grid cells inside any fixed AM (z=nz cells)
        for _i in range(len(am_r)):
            cx, cy, cz = am_c[_i]; rr = float(am_r[_i])
            _raster(pin_np, cx, cy, cz, rr, int(amraw[_i, 0]))
        se_target = AM_vol * args.se_frac / (1.0 - args.se_frac)   # SE volume to RSA-fill
        plan = [(r_se3, 1.0, MU_SE, LA_SE, YIELD_SE)]
    elif args.preset == 'real14':
        # production input_real_14: 3-component AM_P 6µm + AM_S 2µm + SE 0.5µm (12:4:1),
        # 50×50µm RVE, ACTUAL voxel composition AM_P:AM_S:SE = 0.51:0.22:0.27 (AM:SE 73:27).
        # Map 50µm → the near-full lateral box; tall column for the loose bed.  SE material =
        # our MPM calibration (defaults E=1.53/ν=0.49/σy=0.30), AM ~rigid — NOT the LIGGGHTS
        # DEM contact params (frame [4]: each model calibrated to experiment independently).
        SW = (0.02, 0.98); WIDTH = SW[1] - SW[0]
        FLOOR = 0.05; WALL0 = 0.90; WALL_MIN = 0.055
        scl = WIDTH / 50.0                                  # box units per µm
        r_amp, r_ams, r_se3 = 6.0 * scl, 2.0 * scl, 0.5 * scl
        um_box = 1.0 / scl                                  # µm per box unit (preset scl = box/µm)
        plan = [(r_amp, 0.51, MU_AM, LA_AM, YIELD_AM),
                (r_ams, 0.22, MU_AM, LA_AM, YIELD_AM),
                (r_se3, 0.27, MU_SE, LA_SE, YIELD_SE)]
    else:
        plan = [(args.r_am, am_frac, MU_AM, LA_AM, YIELD_AM),
                (args.r_se, 1.0 - am_frac, MU_SE, LA_SE, YIELD_SE)]
    fill_h = (am_top if args.am_scaffold else WALL0 - 0.03)
    box_vol = WIDTH * WIDTH * (fill_h - FLOOR)
    target = (se_target if args.am_scaffold else args.init_solid * box_vol)
    vol = lambda r: (4.0 / 3.0) * np.pi * r ** 3           # noqa: E731
    plan = [pk for pk in plan if pk[1] > 1e-9]
    rmin = min(pk[0] for pk in plan)
    cell = 2.0 * rmin
    placed, big, grid = [], [], {}

    def in_am(p):                                          # O(1) fixed-AM rejection via grid mask
        if not args.am_scaffold:
            return False
        ii = min(int(p[0] * n_grid), n_grid - 1); jj = min(int(p[1] * n_grid), n_grid - 1)
        kk = min(int(p[2] * n_grid), nz - 1)
        return pin_np[ii, jj, kk] > 0

    def hits_big(p, r):
        for (qx, qy, qz, qr) in big:
            if (p[0] - qx) ** 2 + (p[1] - qy) ** 2 + (p[2] - qz) ** 2 < (r + qr + 0.004) ** 2:
                return True
        return False

    def hits_small(p, r):
        kx, ky, kz = int(p[0] / cell), int(p[1] / cell), int(p[2] / cell)
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                for c in (-1, 0, 1):
                    for (qx, qy, qz, qr) in grid.get((kx + a, ky + b, kz + c), ()):
                        if (p[0] - qx) ** 2 + (p[1] - qy) ** 2 + (p[2] - qz) ** 2 < (r + qr + 0.004) ** 2:
                            return True
        return False

    se_id_base = None                                       # per-base-point SE particle id (set under --se-dump)
    if args.am_scaffold:
        spc = dx * 0.5
        i0 = LO_m if PERIODIC else int(SW[0] * n_grid) + 1   # no wall inset when periodic
        i1 = LO_m + WC_m if PERIODIC else int(SW[1] * n_grid)
        k0 = int(FLOOR * n_grid) + 1; k1 = min(int(am_top * n_grid), nz)
        if args.se_dump:
            # ── seed SE at the REAL DEM SE centres: rasterise each D1 SE sphere into the grid
            #    (voxel union → no overlap double-count), keep only non-AM cells.  SE volume and
            #    spatial distribution are then REAL, so porosity·coverage EMERGE from the data
            #    (no se_frac, no --target-porosity). ──────────────────────────────────────────
            seraw = np.atleast_2d(np.loadtxt(args.se_dump, delimiter=','))  # 2D even for a 1-row CSV
            se_c = np.column_stack([SW[0] + seraw[:, 1] * scl, SW[0] + seraw[:, 2] * scl,
                                    FLOOR + seraw[:, 3] * scl * DZ])   # SE rides the dilated skeleton (z-affine)
            se_rr = (seraw[:, 4] * scl).astype(np.float64)
            se_pin = np.zeros((n_grid, n_grid, nz), bool)
            for _i in range(len(se_rr)):
                cx, cy, cz = se_c[_i]; rr = float(se_rr[_i])
                _raster(se_pin, cx, cy, cz, rr, True)        # x,y wrap when PERIODIC (boundary SE)
            se_pin &= (pin_np == 0)                          # SE only in non-AM cells
            sel = np.argwhere(se_pin)
            seed_str = f"{len(seraw)} real SE spheres → {len(sel):,} SE cells (REAL positions, no targeting)"
            # tag each SE cell with its NEAREST real SE sphere centre (Voronoi) so the original PARTICLE
            # id survives the union raster → the voxel solver can recover SE-SE plastic CONTACT AREAS
            # (per-particle Holm constriction) instead of fusing all SE into one blob.
            from scipy.spatial import cKDTree as _ckd
            _cid = _ckd(se_c).query((sel + 0.5) * dx, k=1)[1].astype(np.int32)   # cell → nearest SE sphere
            se_id_base = np.repeat(_cid, 8)                  # 8 sub-points/cell, SAME order as xs below
        else:
            # ── uniform cell-fill: a se_target/interstitial-vol fraction of the non-AM bed cells
            #    (porosity a RESULT of plastic fill, not RSA-limited). ──────────────────────────
            free = pin_np[i0:i1, i0:i1, k0:k1] == 0
            inter = np.argwhere(free) + np.array([i0, i0, k0])
            prob = min(1.0, se_target / max(len(inter) * dx ** 3, 1e-12))
            sel = inter[rng.random(len(inter)) < prob]
            seed_str = f"{len(sel):,} SE cells, interstitial fill {prob*100:.0f}% (se_frac {args.se_frac})"
        subo = np.array([[a, b, c] for a in (0.25, 0.75) for b in (0.25, 0.75)
                         for c in (0.25, 0.75)]) * dx       # 8 sub-positions per cell
        xs = ((sel[:, None, :] * dx) + subo[None]).reshape(-1, 3).astype(np.float32)
        n = len(xs)
        if n < 2:
            print("scaffold build failed (n<2) — check --am-scaffold / --se-frac / --se-dump"); return
        mus = np.full(n, MU_SE, np.float32); las = np.full(n, LA_SE, np.float32)
        ylds = np.full(n, YIELD_SE, np.float32); pvs = np.full(n, spc ** 3, np.float32)
        # ── density / volume-fraction watch (real ρ: AM 4800, SE 2000 kg/m³ from the LIGGGHTS deck) ──
        se_solid = len(sel) * dx ** 3
        am_solid = float((pin_np > 0).sum()) * dx ** 3
        bed_vol = WIDTH * WIDTH * (am_top - FLOOR)
        f_am = 100.0 * am_solid / bed_vol; f_se = 100.0 * se_solid / bed_vol
        bulk_rho = (am_solid * 4800.0 + se_solid * 2000.0) / bed_vol / 1000.0
        print(f"  scaffold: {len(am_r)} fixed AM + {seed_str} ({n:,} pts)")
        print(f"  seed density: AM {f_am:.1f}% / SE {f_se:.1f}% / void {max(0.0,100-f_am-f_se):.1f}%  "
              f"(SE/solid {100*se_solid/max(am_solid+se_solid,1e-12):.1f}%)  "
              f"ρ_bulk≈{bulk_rho:.2f} g/cm³  bed {(am_top-FLOOR)*um_box:.1f}µm")
    else:
        for (r, frac, mu, la, yld) in plan:
            goal = frac * target; acc = 0.0; fails = 0
            small = r <= 1.5 * rmin
            xlo = SW[0] if PERIODIC else SW[0] + r           # periodic → fill to the edge (wrap handles it)
            xhi = SW[1] if PERIODIC else SW[1] - r
            while acc < goal and fails < 60000:
                p = (rng.uniform(xlo, xhi), rng.uniform(xlo, xhi),
                     rng.uniform(FLOOR + r, fill_h - r))
                ok = (not in_am(p)) and (not hits_big(p, r)) and (not (small and hits_small(p, r)))
                if ok:
                    placed.append((p[0], p[1], p[2], r, mu, la, yld)); acc += vol(r); fails = 0
                    if small:
                        grid.setdefault((int(p[0] / cell), int(p[1] / cell), int(p[2] / cell)), []).append(
                            (p[0], p[1], p[2], r))
                    else:
                        big.append((p[0], p[1], p[2], r))
                else:
                    fails += 1
        # ── voxelize spheres into material points (numpy-vectorized: per-radius in-sphere
        #    offset template × particle centers, broadcast + chunked). ──────────────────
        placed_arr = np.asarray(placed, np.float64)        # [N,7] cx,cy,cz,r,mu,la,yld
        xs_list, mu_list, la_list, yld_list, pv_list = [], [], [], [], []
        for r in np.unique(placed_arr[:, 3]):
            grp = placed_arr[placed_arr[:, 3] == r]
            mu_v, la_v, yld_v = grp[0, 4], grp[0, 5], grp[0, 6]
            spc = dx if yld_v > 100.0 else dx * 0.5        # AM (rigid, high yld) coarse; SE fine
            pvg = spc ** 3                                 # per-point volume (= mass, ρ=1) for this group
            k = int(r / spc) + 1
            ax = np.arange(-k, k + 1) * spc
            ox, oy, oz = np.meshgrid(ax, ax, ax, indexing='ij')
            off = np.stack([ox.ravel(), oy.ravel(), oz.ravel()], 1)
            off = off[(off ** 2).sum(1) <= r * r]          # in-sphere offsets [Pin,3]
            centers = grp[:, :3]
            chunk = max(1, 16_000_000 // max(1, off.shape[0]))
            for s in range(0, len(centers), chunk):
                pts = (centers[s:s + chunk, None, :] + off[None]).reshape(-1, 3)
                m = pts.shape[0]
                xs_list.append(pts.astype(np.float32))
                mu_list.append(np.full(m, mu_v, np.float32))
                la_list.append(np.full(m, la_v, np.float32))
                yld_list.append(np.full(m, yld_v, np.float32))
                pv_list.append(np.full(m, pvg, np.float32))
        xs = np.concatenate(xs_list)
        n = len(xs)
        if n < 2:
            print("build failed (n<2) — raise --n-grid or --init-solid"); return
        mus = np.concatenate(mu_list); las = np.concatenate(la_list); ylds = np.concatenate(yld_list)
        pvs = np.concatenate(pv_list)
    # ── Stage 1: conductive additives (VGCF / Super P / PTFE) as extra MPM phases ──────
    #    recipe wt% → object counts (additives.py) → seed fibre/blob points (avoiding the fixed
    #    AM) → append with per-additive (µ,λ,σ_y).  Kernel uses only per-point material → no
    #    P2G/G2P change.  phase code: 1 SE · 2 VGCF · 3 SuperP · 4 PTFE (0 AM = scaffold mask).
    phase_np = np.where(ylds < 100.0, 1, 0).astype(np.int8)    # base points: 1 SE / 0 AM(mat, mix mode)
    coh_np = np.full(len(xs), COH, np.float32)                 # per-point cohesion: SE = COH (PTFE ≫ below)
    fibre_np = None                                            # set in the additive block if fibres seeded
    dia_np = None                                              # per-point relative fibre Ø (PTFE draw d∝√(V/L))
    if args.add_recipe:
        if not args.am_scaffold:
            print("  [additives] --add-recipe needs --am-scaffold; skipped")
        else:
            import sys as _sys, os as _os
            _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
            import additives as _ad
            wt = _ad.parse_recipe(args.add_recipe)
            add_wt = _ad.additive_wt(wt)                                # ONLY the additive wt% (AM:SE in
            #   the recipe is ignored — the additive enters as wt% of the REAL scaffold composition, not a
            #   hardcoded ratio).  AM/SE masses from the actual fixed-AM + seeded-SE volumes.
            se_um3 = float(pvs.sum()) * um_box ** 3                     # real SE volume (Σ per-point)
            am_um3 = AM_vol * um_box ** 3                               # real fixed-AM volume
            cnt = _ad.recipe_counts_real(add_wt, am_um3, se_um3)
            print(f"  [additives] realised electrode (from scaffold): AM {cnt['am_wt_pct']} / "
                  f"SE {cnt['se_wt_pct']} wt% + " + " ".join(f"{k} {add_wt[k]}wt%" for k in add_wt))
            bx = (WIDTH, WIDTH, max(am_top - FLOOR, 4 * dx))            # seed region (box units)
            off = np.array([SW[0], SW[0], FLOOR], np.float32)

            def _in_am_abs(p):                                          # p in ABSOLUTE box coords
                ii = int(p[0] * n_grid); jj = int(p[1] * n_grid); kk = int(p[2] * n_grid)
                return (0 <= ii < n_grid and 0 <= jj < n_grid and 0 <= kk < nz
                        and pin_np[ii, jj, kk] > 0)
            # VGCF waviness from the press (buckling proxy): --vgcf-curl <0 → AUTO curl=f(target P).
            # --fibre-rod → straight seed (rod buckles emergently); --fibre-buckle → straight seed + physics buckle.
            _vgcf_curl = (0.0 if (args.fibre_rod or args.fibre_buckle) else
                          args.vgcf_curl if args.vgcf_curl >= 0.0 else _press_curl(float(args.target_gpa)))
            # PTFE web tangle (curl).  Baseline 0.40 = the as-drawn/fibrillated tangle (a DRAWING/shear
            # property set by mixing, NOT press).  --ptfe-press-curl (OPT-IN) re-attributes it to a press
            # scaling for parity with VGCF — kept OPT-IN because the press MAGNITUDE for a soft fibril is
            # UNANCHORED (curl_sat/p_char are borrowed from VGCF's stiff-column Euler buckling, no PTFE
            # basis) → keep it out of the production number (backlog §F1).  (align is auto-baked instead
            # because its λ_z is DERIVED from the measured compaction ratio — an anchored quantity, not an
            # invented magnitude; that honest split — derived=auto, unanchored=opt-in — is the real reason.)
            _ptfe_curl = (_press_curl(float(args.target_gpa), curl_sat=0.40, p_char=0.30)
                          if args.ptfe_press_curl else 0.40)
            # physics buckle wavelength (Winkler): λ=2π(EI/E_SE)^¼, EI=E_fib·πr⁴/4 (real graphite 200 GPa, r=75nm)
            _buckle_lam = ((2 * np.pi * (200.0 * np.pi * 0.075 ** 4 / 4 / max(args.e_se, 1e-6)) ** 0.25) / um_box
                           if args.fibre_buckle else 0.0)
            # AM-POSITION-dependent buckle: local AM volume fraction at ~fibre-length scale → fibres in dense/
            # pinched AM regions buckle more (the real particle-pinching driver), fibres in open SE pores less.
            _amfrac_arr = None
            if args.fibre_buckle:
                try:
                    from scipy.ndimage import uniform_filter
                    _wn = max(3, int(round((_ad.VGCF_L / um_box) * n_grid)))   # window ≈ one fibre length (cells)
                    _amfrac_arr = uniform_filter((pin_np > 0).astype(np.float32), size=_wn, mode='nearest')
                except Exception as _e:
                    print(f'  [fibre-buckle] scipy.ndimage missing ({_e}) → uniform AM factor'); _amfrac_arr = None

            def _am_frac_abs(p):                                          # p ABSOLUTE box coords → local AM fraction
                if _amfrac_arr is None:
                    return 1.0
                ii = min(max(int(p[0] * n_grid), 0), n_grid - 1)
                jj = min(max(int(p[1] * n_grid), 0), n_grid - 1)
                kk2 = min(max(int(p[2] * n_grid), 0), nz - 1)
                return float(_amfrac_arr[ii, jj, kk2])
            print(f"  [additives] VGCF curl = {_vgcf_curl:.3f}  "
                  + (f'(--fibre-buckle: λ={_buckle_lam * um_box:.2f}µm, confined-strain {args.buckle_strain}, '
                     f'AM-position-dependent{"" if _amfrac_arr is not None else " OFF"})'
                     if args.fibre_buckle
                     else '(straight seed → --fibre-rod buckles it emergently)' if args.fibre_rod
                     else 'fixed --vgcf-curl' if args.vgcf_curl >= 0.0
                     else f'auto from press {args.target_gpa:.2f} GPa'))
            ADD = {  # phase: (E GPa, ν, σ_y GPa, code, kind, L_µm, curl, vol_cv, nuc_frac, branch_frac, bridge_frac).
                #   'fibre' = rod, 'cblack' = branched chain + AM-coating.  curl = path waviness (VGCF = press-dependent
                #   buckling proxy _vgcf_curl; PTFE 0.4 = tangled drawn web);
                #   vol_cv>0 → initial node-volume spread (drawn d∝√(V/L)); nuc_frac → fraction nucleating on carbon
                #   (CBD); branch_frac → ② spawn thinner secondary fibrils; bridge_frac → ④ steer toward a 2nd carbon.
                'VGCF':   (10.0, 0.30, 2.00, 2, 'fibre',  _ad.VGCF_L, _vgcf_curl, 0.0, 0.0, 0.0, 0.0),   # press-dependent buckling waviness (--vgcf-curl / _press_curl)
                'SuperP': (0.50, 0.30, 0.10, 3, 'cblack', 0.0,        0.0,  0.0, 0.0, 0.0, 0.0),   # carbon black
                'PTFE':   (0.30, 0.30, 0.05, 4, 'fibre',  _ad.PTFE_L, _ptfe_curl, 0.6, 0.6, 0.5, 0.5),   # drawn web + CBD + AM-wrap
                'SDCP':   (23.6, 0.35, 1.00, 5, 'particle', 0.0,      0.0,  0.0, 0.0, 0.0, 0.0),   # ★E=23.6 GPa MANUSCRIPT-ANCHORED (AFM S6; LPSCl급 강성) — 0.3µm particles (S3), σ_y=1.0 UN-anchored rigid-proxy §F1 (stiff conjugated polymer, no PTFE-like flow; ≫press → behaves rigid); ρ 1.3 still proxy (methods 대기)
            }
            am_box = ((am_c - off, am_r) if am_c is not None else None)   # AM in the seed-box frame (coating)
            fibre_np = np.full(len(xs), -1, np.int32)   # per-point fibre/aggregate id (-1 = SE; ≥0 = a fibre /
            dia_np = np.zeros(len(xs), np.float32)      # per-point relative fibre Ø (0 = SE/non-fibre; ∝√weight)
            carbon_seed = []                            # carbon (VGCF/SuperP) pts in seed-box frame → PTFE
            _gfib = 0                                   # nucleation attractors (binder nets carbon = CBD)
            _add_meta = {}                              # per-additive recipe+physics → mpm_metrics['additives']
            for nm, (E, nu, sy, code, kind, L_um, curl, vcv, nucf, brf, brgf) in ADD.items():
                if nm not in cnt:
                    continue
                # ★ A4 — placement regime from the process matrix.  IMPLEMENTED (97767ae+) for non-fibre
                # kinds: 'coat' (SDCP) and SuperP 'coat_block' (thinky) seed as an AM-surface film via
                # seed_coat — so SuperP thinky ≢ ballmill FROM NOW ON (pre-A4 campaign rows were merged).
                # VGCF 'coat_embed' is NOT yet coat-seeded (fibre branch wins) — still ≡ ballmill.
                _proc_regime = _ad.additive_regime(nm, args.mixing)
                nobj = cnt[nm]['n']                          # target PRIMARY-fibre count (VGCF/PTFE centreline
                #   skeleton; SuperP = aggregate count) — recipe wt%/vol% tracked in metrics + per-point pvs
                #   (branching adds children but the mean-1 weight normalisation preserves the recipe volume).
                # ★ PTFE fibrillation vs mixing SHEAR (dry-process): high-shear ball-mill/Thinky unravel PTFE
                # into a BRANCHED fibril web; low-shear hand-mix → poorly-networked, clumpy fibrils.  Scales
                # branch_frac (the web = the lit-supported fibrillation signature) ONLY, by a single knob → σ_e-
                # network morphology + PTFE-on-AM coverage; porosity UNAFFECTED (soft PTFE flows + add_pvs
                # volume-pin, mirror of SuperP).  DIRECTION lit-supported; MAGNITUDE a tunable hook, NOT anchored
                # (--ptfe-fibril; docs/digest_model_application_backlog.md §F1).
                _fibril = 1.0
                _coated = False
                if code == 4:
                    _fibril = float(args.ptfe_fibril) if args.ptfe_fibril >= 0.0 else _ad.PTFE_FIBRIL.get(args.mixing, 1.0)
                    brf = round(brf * _fibril, 3)            # fewer secondary fibrils = less-networked web at low shear
                if kind == 'fibre':
                    # nucleation attractors for the binder web: the already-seeded carbon (CBD co-location)
                    # PLUS, for PTFE (code 4), points on the AM SURFACES — PTFE is a binder that DRAPES/wraps
                    # AM particles (Lee 2025 bridging), not only the CBD carbon.  The AM share is a CONTROLLED
                    # FRACTION (--ptfe-am-bind) of the nucleations, held FIXED independent of the carbon point
                    # count (a raw concat would let the wrap strength swing wildly with recipe).  MAGNITUDE
                    # (default 0.5) is a conservative tunable hook, NOT anchored (backlog §F1).
                    _am_fired = False
                    _nuc_parts = [np.concatenate(carbon_seed)] if carbon_seed else []
                    if code == 4 and am_c is not None and (nucf > 0.0 or brgf > 0.0):
                        _f = float(np.clip(args.ptfe_am_bind, 0.0, 1.0))         # target AM share of nucleations
                        _ncarb = int(sum(len(c) for c in carbon_seed)) if carbon_seed else 0
                        if _f > 0.0:
                            _nam = (int(round(_f / (1.0 - _f) * _ncarb)) if (_ncarb > 0 and _f < 1.0)
                                    else 4 * len(am_c))                          # PTFE-only / f→1: AM = whole pool
                            _amsurf = _am_surface_pts(am_c - off, am_r, min(max(_nam, 0), 500000), rng, bx)
                            if len(_amsurf):
                                _nuc_parts.append(_amsurf); _am_fired = True
                    nuc = np.concatenate(_nuc_parts) if (_nuc_parts and (nucf > 0.0 or brgf > 0.0)) else None
                    _bk_lam = _buckle_lam if code == 2 else 0.0     # physics buckle = VGCF only (PTFE = drawn web)
                    _amfn = (lambda q: _am_frac_abs(q + off)) if (code == 2 and _bk_lam > 0.0) else None
                    pts, _fid, _w = _ad.seed_fibres(nobj, bx, dx, rng, L=L_um / um_box, L_cv=args.add_l_cv,
                                                    curl=curl, vol_conserve=(vcv > 0.0),   # Ø-spread = drawing (PTFE vcv>0) ONLY; VGCF gets waviness (curl>0) but keeps a uniform manufactured Ø
                                                    vol_cv=vcv, nucleate=nuc, nucleate_frac=nucf,
                                                    branch_frac=brf, bridge_frac=brgf,
                                                    buckle_lam=_bk_lam, buckle_strain=args.buckle_strain,
                                                    am_frac_fn=_amfn, align_lambda=float(args.fibre_align),
                                                    in_am=lambda q: _in_am_abs(q + off),
                                                    return_ids=True, return_vol=True)
                elif kind == 'particle':
                    # ★ SDCP manuscript morphology — MIXING-dependent dispersion state; single source of
                    # truth = additives.seed_sdcp (shared with scripts/preview_sdcp_mixing.py):
                    #   ball-mill/Thinky (high shear): milled 0.2-0.5µm SINGLES (Fig S3), surface_frac
                    #     AM-anchored (sulfonate + ordered-mixing decoration; §F1 hook) + rest in-pore;
                    #     --sdcp-clump>1 = NCM-decoration cluster hypothesis (anchored share only, §3.7).
                    #   hand-mix (low shear): NO milling energy → the as-made ~3µm agglomerates (Fig S2)
                    #     survive — ALL SDCP seeds as agg_d clusters (anchored draped on AM + bulk alike;
                    #     dispersion is a property of the POWDER, not of where a particle sits).
                    _row = _ad.additive_process(nm, args.mixing)
                    _sfrac = (float(args.sdcp_surface_frac) if (code == 5 and args.sdcp_surface_frac >= 0.0)
                              else float(_row.get('surface_frac', 0.5)))
                    _clump = max(1, int(args.sdcp_clump) if args.sdcp_clump > 0 else int(_row.get('clump', 1)))
                    _aggd = (float(args.sdcp_agg_d) if args.sdcp_agg_d >= 0.0
                             else float(_row.get('agg_d', 0.0)))               # µm; 0 = milled singles (S3)
                    pts, _fid = _ad.seed_sdcp(nobj, bx, dx, rng, am=am_box,
                                              in_am=lambda q: _in_am_abs(q + off),
                                              surface_frac=_sfrac, clump=_clump,
                                              agg_d=_aggd / um_box, d=_ad.SDCP_D / um_box,
                                              return_ids=True)
                    _w = np.ones(len(pts), np.float32)
                    _coated = True                            # metadata: coat dict records the anchored share
                elif kind == 'coat' or _proc_regime == 'coat_block':   # coat_embed RETIRED (fibres don't coat)
                    # A4 COAT REGIME: points seeded in a thin shell ON the AM surfaces — SDCP anchored film
                    # (default) or SuperP thinky dry-coat (coat_block: carbon film at the AM|SE interface;
                    # its σ_i-blocking emerges as an SE-coverage drop, Kim 2025 direction).  Film thickness
                    # is 1 voxel-ish (shell 0.2µm) vs real ~26-40nm — OVERSTATED sub-voxel reality, but the
                    # recipe VOLUME is add_pvs-pinned so porosity stays honest (same approximation class as
                    # Stage-E).  surface_frac: mixing-driven spread (handmix = patchy).
                    _row = _ad.additive_process(nm, args.mixing)          # single source: process matrix
                    _sfrac = (float(args.sdcp_surface_frac) if (code == 5 and args.sdcp_surface_frac >= 0.0)
                              else float(_row.get('surface_frac', 1.0)))    # SDCP rows 1.0/1.0/0.6; SuperP thinky 0.70
                    pts, _fid = _ad.seed_coat(nobj, bx, dx, rng, am=am_box, shell_um=_ad.SDCP_SHELL / um_box,
                                              surface_frac=_sfrac, in_am=lambda q: _in_am_abs(q + off),
                                              return_ids=True)              # µm shell → seed-frame units; buried/out-of-box DROPPED
                    _w = np.ones(len(pts), np.float32)
                    _coated = True
                else:                                        # carbon black: branched chains coating the AM
                    pts, _fid = _ad.seed_carbon_black(nobj, bx, dx, rng, in_am=lambda q: _in_am_abs(q + off),
                                                      am=am_box, mixing=args.mixing, return_ids=True)
                    _w = np.ones(len(pts), np.float32)
                if len(pts) == 0:
                    continue
                if code in (2, 3):                      # carbon → attractor for the PTFE binder (CBD co-location)
                    carbon_seed.append(pts.copy())
                if len(_fid):                           # make fibre/aggregate ids globally unique
                    _fid = _fid + _gfib; _gfib = int(_fid.max()) + 1
                pts = (pts + off).astype(np.float32)
                fibre_np = np.concatenate([fibre_np, _fid])
                dia_np = np.concatenate([dia_np, np.sqrt(np.maximum(_w, 1e-6)).astype(np.float32)])   # Ø∝√weight
                mu_a, la_a = lame(E, nu)
                xs = np.concatenate([xs, pts])
                mus = np.concatenate([mus, np.full(len(pts), mu_a, np.float32)])
                las = np.concatenate([las, np.full(len(pts), la_a, np.float32)])
                ylds = np.concatenate([ylds, np.full(len(pts), sy, np.float32)])
                # each additive point carries its SHARE of the additive's recipe volume (×per-point weight _w,
                # which is 1 for uniform VGCF and ∝V_i/L_i for the volume-conserving PTFE draw), so the MPM
                # additive volume == the recipe (lit-density) regardless of point count or fibre Ø spread.
                add_pvs = float(cnt[nm]['vol_um3'] / max(len(pts), 1)) / (um_box ** 3)   # box units
                pvs = np.concatenate([pvs, (add_pvs * _w).astype(np.float32)])
                phase_np = np.concatenate([phase_np, np.full(len(pts), code, np.int8)])
                # A3: VGCF/SuperP not sticky; PTFE binder cohesion is NON-MONOTONIC in PTFE wt%
                # (peak at --binder-opt-wt, decays for over-application — over-crosslink/agglomeration).
                if code == 4:                                      # PTFE binder
                    _cap = binder_cap(float(cnt[nm]['wt_pct']), args.binder_opt_wt)
                    _coh = round(args.coh_ptfe * _cap, 4)
                    _reg = ('under (delamination-prone)' if cnt[nm]['wt_pct'] < 0.6 * args.binder_opt_wt
                            else 'over (agglomeration↓)' if cnt[nm]['wt_pct'] > 1.6 * args.binder_opt_wt
                            else 'near-optimal')
                elif code == 5:                                    # SDCP conductive binder — BULK film-integrity coh,
                    _cap = 1.0                                     #   variant-INDEPENDENT (same PEDOT film both ways;
                    _coh = round(args.coh_sdcp, 4)                 #   doped/neutral γ 0.93/0.42 = AM-INTERFACE anchor →
                    _reg = 'neutral(−SO₃H)' if args.sdcp_neutral else 'doped(−SO₃⁻)'   # future boundary term + STEP3,
                    #   NOT this bulk coh — scaling bulk by the interface γ-ratio would be the same cross-
                    #   attribution the --coh-sdcp help forbids for the 10× inflation.
                else:
                    _coh, _cap, _reg = 0.0, 0.0, '—'
                coh_np = np.concatenate([coh_np, np.full(len(pts), _coh, np.float32)])
                _bind = (f" binder_cap={_cap:.2f} [{_reg}] (opt {args.binder_opt_wt}wt%)" if code == 4 else "")
                _bind += f" regime={_proc_regime}" + ("  (A4 coat-seeded)" if _coated else
                                                       "  (A4: coat seeding TBD → bulk)" if _proc_regime != 'bulk' else "")
                print(f"  [additives] {nm}: {nobj} objects ({cnt[nm]['wt_pct']}wt% = "
                      f"{cnt[nm]['vol_pct_of_solid']}vol% of solid) → {len(pts):,} pts "
                      f"(E={E} σ_y={sy} coh={_coh}, phase {code}){_bind}")
                _add_meta[nm] = {                            # → mpm_metrics['additives'][nm] → 요약
                    'wt_pct': float(cnt[nm]['wt_pct']), 'vol_pct_of_solid': float(cnt[nm]['vol_pct_of_solid']),
                    'vol_um3': round(float(cnt[nm]['vol_um3']), 2), 'n_objects': int(nobj), 'n_points': int(len(pts)),
                    'E_GPa': float(E), 'sigma_y_GPa': float(sy), 'phase_code': int(code),
                    'mixing': args.mixing, 'mixing_regime': _proc_regime,   # NAME + regime: ballmill & handmix BOTH regime='bulk' → the NAME is what tells them apart (regime alone can't)
                }
                if kind == 'cblack' and not _coated:         # CB_MIX params — only when seed_carbon_black RAN
                    _cbm = _ad.CB_MIX.get(args.mixing, {})   # (a coat-routed SuperP-thinky run must not claim
                    if _cbm:                                 # CB-chain morphology it didn't seed)
                        _add_meta[nm]['cb_mix'] = {_k: _cbm[_k] for _k in ('k', 'surface_frac', 'step', 'clump') if _k in _cbm}
                if _coated:                                  # A4 coat: record what ACTUALLY seeded
                    _add_meta[nm]['coat'] = {'shell_um': (_ad.SDCP_D / 2 if kind == 'particle' else _ad.SDCP_SHELL),
                                             'surface_frac': round(float(_sfrac), 3)}   # particle: anchored shell = particle radius
                if code == 2:                                # VGCF: waviness (Tier-1 curl / physics buckle / rod)
                    _add_meta[nm]['curl'] = round(float(_vgcf_curl), 3)
                    if args.fibre_buckle:
                        _add_meta[nm]['buckle_lam_um'] = round(float(_buckle_lam * um_box), 3)
                        _add_meta[nm]['buckle_strain_confined'] = float(args.buckle_strain)
                        _add_meta[nm]['buckle_am_position_dependent'] = bool(_amfrac_arr is not None)
                if kind == 'fibre' and float(args.fibre_align) != 1.0:   # press-induced in-plane alignment
                    _add_meta[nm]['align_lambda_z'] = round(float(args.fibre_align), 3)
                if code == 4:                                # PTFE: A3 binder cohesion + fibrillation-vs-shear
                    _add_meta[nm]['coh_ptfe'] = float(_coh); _add_meta[nm]['binder_cap'] = round(float(_cap), 3)
                    _add_meta[nm]['fibrillation'] = round(float(_fibril), 3)   # dry-shear web degree (mixing-driven)
                    _add_meta[nm]['branch_frac_effective'] = round(float(brf), 3)   # post-fibrillation secondary-fibril fraction (raw base = eff / fibrillation)
                    _add_meta[nm]['curl'] = round(float(_ptfe_curl), 3)        # web tangle (press-scaled iff --ptfe-press-curl)
                    _add_meta[nm]['press_curl'] = bool(args.ptfe_press_curl)   # prescribed press-curl on? (OFF = as-drawn 0.40)
                    _add_meta[nm]['am_bind'] = bool(_am_fired)                 # AM-surface draping attractors ACTUALLY added?
                    _add_meta[nm]['am_bind_frac'] = round(float(np.clip(args.ptfe_am_bind, 0.0, 1.0)), 3)   # target AM nucleation share
                if code == 5:                                # SDCP: dispersed anchored particles (manuscript)
                    _add_meta[nm]['morphology'] = (f'agglomerate_{_aggd:.1f}um_S2' if _aggd > 0.0
                                                   else 'particle_0.3um_S3')     # mixing-dependent dispersion state
                    _add_meta[nm]['E_anchor'] = 'AFM_S6_23.6GPa'
                    _add_meta[nm]['variant'] = 'neutral' if args.sdcp_neutral else 'doped'
                    _add_meta[nm]['coh_sdcp'] = float(_coh)
                    _add_meta[nm]['clump'] = int(_clump)
                    _add_meta[nm]['agg_d_um'] = round(float(_aggd), 2)           # 0 = milled S3 singles
                    if _aggd > 0.0:                                              # S2 as-made agglomerate: primaries per cluster
                        _add_meta[nm]['n_per_agglomerate'] = max(1, int(round(0.64 * (_aggd / _ad.SDCP_D) ** 3)))
                    _add_meta[nm]['anchor_status'] = 'INVALID_WRONG_MONOMER_recompute_pending'   # 2026-07-10: 이전 E_bind(−4.8/−3.0)는
                    #   곧은-pentyl C11H15O5S2로 계산됨 — 실제 SDCP는 ether-O 링커 + methyl-분지 2차 술폰산
                    #   (C11H16O6S2, Fig2a/S5).  ether-O의 Li 배위 채널 누락 → 값·기하 전면 재계산 필요.
    n = len(xs)                                               # final count (incl additives)
    xs[:, :2] = np.clip(xs[:, :2], 2.0 * dx, 1.0 - 2.0 * dx)   # lateral stencil inside [0,n_grid)
    xs[:, 2] = np.clip(xs[:, 2], 2.0 * dx, (nz - 2) * dx)      # z stencil inside [0,nz) (= 1-2dx when cubic)
    solid_vol = float(pvs.sum()) + AM_vol                  # voxelized SE vol (Σ per-point) + exact fixed-AM
    #   vol.  Σ per-point matches the old n·p_vol so the pure-SE 10% calibration is preserved.
    # periodic (x,y) box in grid cells, snapped so the particle wrap (LATW) == the grid wrap (WC·dx)
    # exactly → no seam drift.  Origin kept at SW[0] so it matches the mask rasterisation above.
    _LO = int(round(SW[0] * n_grid)); _WC = int(round((SW[1] - SW[0]) * n_grid))
    _SW0 = float(SW[0]); _LATW = _WC * dx                   # period (physical) = grid-aligned width

    x = ti.Vector.field(3, ti.f32, n); v = ti.Vector.field(3, ti.f32, n)
    C = ti.Matrix.field(3, 3, ti.f32, n); F = ti.Matrix.field(3, 3, ti.f32, n)
    mu_p = ti.field(ti.f32, n); la_p = ti.field(ti.f32, n); yld_p = ti.field(ti.f32, n)
    pvol_p = ti.field(ti.f32, n)                                # per-point volume (= mass, ρ=1)
    coh_p = ti.field(ti.f32, n)                                 # per-point cohesion (PTFE binder ≫ SE)
    dg_acc = ti.field(ti.f32, n)                                # accumulated plastic strain Σdg per point
    eps_acc = ti.field(ti.f32, n)                               # accumulated TOTAL strain (vs seed, incl elastic) per point
    grid_v = ti.Vector.field(3, ti.f32, (n_grid, n_grid, nz)); grid_m = ti.field(ti.f32, (n_grid, n_grid, nz))
    wall_z = ti.field(ti.f32, ()); wall_vel = ti.field(ti.f32, ()); szz = ti.field(ti.f32, ())
    wallf = ti.field(ti.f32, ())                                # platen reaction impulse Σ m·Δv (per substep)
    scaffold_on = bool(args.am_scaffold)                        # fixed-AM grid obstacle (real skeleton)
    SE_AM_DRAG = float(args.se_am_drag) if scaffold_on else 0.0   # ★ SE-AM confinement drag coef (compile-time const)
    am_mask = ti.field(ti.i32, (n_grid, n_grid, nz) if scaffold_on else (1, 1, 1))
    am_near = ti.field(ti.f32, (n_grid, n_grid, nz) if scaffold_on else (1, 1, 1))   # local AM fraction (confinement)
    if scaffold_on:
        rigid_np = pin_np                                       # rigid (v=0) obstacle mask = fixed AM …
        if args.fibre_stiff and 'phase_np' in locals():         # … ∪ load-bearing VGCF (stiff strut lever)
            _vg = (phase_np == 2)                               # VGCF points (phase code 2; σ_y=2 GPa ≫ press)
            if _vg.any():
                rigid_np = pin_np.copy()
                _vc = xs[_vg]
                _vi = np.clip((_vc[:, 0] * n_grid).astype(np.int64), 0, n_grid - 1)
                _vj = np.clip((_vc[:, 1] * n_grid).astype(np.int64), 0, n_grid - 1)
                _vk = np.clip((_vc[:, 2] * n_grid).astype(np.int64), 0, nz - 1)
                if PERIODIC:                                    # wrap x,y into the periodic cell (matches P2G node wrap)
                    _vi = _LO + ((_vi - _LO) % _WC + _WC) % _WC
                    _vj = _LO + ((_vj - _LO) % _WC + _WC) % _WC
                _free = rigid_np[_vi, _vj, _vk] == 0            # keep AM tags 1/2 intact (coverage/AM_vol untouched)
                rigid_np[_vi[_free], _vj[_free], _vk[_free]] = 3   # VGCF rigid tag (≠ AM 1/2; am_mask fires on >0)
                try:                                            # close the sub-voxel threads into connected struts
                    from scipy import ndimage as _ndi
                    _vm = _ndi.binary_closing(rigid_np == 3, iterations=1) & (rigid_np == 0)
                    rigid_np[_vm] = 3
                except Exception:
                    pass
                print(f"  [fibre-stiff] VGCF LOAD-BEARING: {int((rigid_np == 3).sum()):,} rigid cells "
                      f"(σ_y≫press → unbucklable strut) — tests compaction-resistance vs volume-fill")
        am_mask.from_numpy(rigid_np)                            # cells inside fixed AM (∪ stiff VGCF if --fibre-stiff)
        if SE_AM_DRAG > 0.0 and am_r is not None:
            # ★ ROUND 4 — GLOBAL load-path robustness (physical, not target-tuned): the drag is only PHYSICAL
            # where the AM skeleton does NOT robustly bear the platen load = THIN beds (few AM layers → marginal
            # floor→platen force path → SE over-flows).  THICK beds = AM multilayer geometrically blocks the
            # platen (§13 thickness-escape: 8mAh SE/sol 16% reliable WITHOUT drag) → robust→0 → drag OFF, so we
            # DON'T over-correct cases §13 says are already MPM-owned.  n_layers = bed depth / AM diameter.
            n_layers = (am_top - FLOOR) / (2.0 * float(np.median(am_r)))
            robust = max(0.0, min(1.0, (float(args.se_am_robust) - n_layers) / max(float(args.se_am_robust_width), 1e-6)))
            SE_AM_DRAG = SE_AM_DRAG * robust                    # effective coef: thin→full, thick→0
            print(f'  [se-am-drag] load-path: bed {(am_top - FLOOR) * um_box:.1f}µm = {n_layers:.1f} AM-layers → '
                  f'robustness {robust:.2f} (off ≥{float(args.se_am_robust):.0f}) → eff-coef {SE_AM_DRAG:.3f}')
        if SE_AM_DRAG > 0.0:
            try:
                from scipy.ndimage import uniform_filter
                _amnear = uniform_filter((pin_np > 0).astype(np.float32), size=3, mode='nearest')   # 3³ AM fraction ∈[0,1] (binary → fixes overlap double-count, was max 2.0)
            except Exception as _e:
                print(f'  [se-am-drag] scipy.ndimage missing ({_e}) → AM-cell-only proximity'); _amnear = (pin_np > 0).astype(np.float32)
            am_near.from_numpy(_amnear.astype(np.float32))
            print(f'  [se-am-drag] ON eff-coef={SE_AM_DRAG:.3f}; SE velocity damped by coef·AM_frac (∈[0,1], '
                  f'max {float(_amnear.max()):.2f}) near the frozen skeleton — local conform, migration suppressed.')

    # ── Tier-2 --fibre-rod: explicit sub-grid rod on VGCF/PTFE points (XPBD distance+bending) so they
    #    BUCKLE emergently under the press.  Verified physics+solver in scripts/fibre_rod_reference.py
    #    (P_cr==Euler; compressed rod bends, keeps contour length).  OFF → fields are size-1 dummies and
    #    none of the rod code runs (compile-time ti.static guard) → production path byte-identical.
    FIBRE_ROD = bool(args.fibre_rod) and ('fibre_np' in locals()) and ('phase_np' in locals())
    if bool(args.fibre_rod) and not FIBRE_ROD:
        print('  [fibre-rod] requested but no fibre additives present (need --add-recipe with VGCF/PTFE) → disabled')
    ROD_STIFF = float(args.rod_stiff); ROD_OMEGA = 0.25            # bending stiffness (PBD) + under-relax
    _rn = n if FIBRE_ROD else 1
    rod_prev = ti.field(ti.i32, _rn); rod_next = ti.field(ti.i32, _rn)
    rod_rl = ti.field(ti.f32, _rn); rod_kfac = ti.field(ti.f32, _rn); rod_is = ti.field(ti.i32, _rn)
    rod_b0 = ti.Vector.field(3, ti.f32, _rn); rod_dx = ti.Vector.field(3, ti.f32, _rn)
    x_pre = ti.Vector.field(3, ti.f32, _rn)                       # fibre position at substep start (for v)
    if FIBRE_ROD:
        _pv, _nx, _rl, _b0, _isr = build_rod_topology(fibre_np, phase_np, xs)
        _kf = np.where(phase_np == 2, 1.0, np.where(phase_np == 4, 0.2, 0.0)).astype(np.float32)  # VGCF stiff, PTFE 0.2×
        rod_prev.from_numpy(_pv); rod_next.from_numpy(_nx); rod_rl.from_numpy(_rl)
        rod_b0.from_numpy(_b0); rod_is.from_numpy(_isr); rod_kfac.from_numpy(_kf)
        print(f'  [fibre-rod] ON: {int(_isr.sum())} rod points (VGCF+PTFE) buckle emergently '
              f'(stiff={ROD_STIFF}, iters={args.rod_iters}); SuperP aggregate = TODO')

    @ti.kernel
    def load(xy: ti.types.ndarray(), ms: ti.types.ndarray(), ls: ti.types.ndarray(),
             ys: ti.types.ndarray(), pv: ti.types.ndarray(), cz: ti.types.ndarray()):
        for p in range(n):
            x[p] = ti.Vector([xy[p, 0], xy[p, 1], xy[p, 2]]); v[p] = ti.Vector([0.0, 0.0, 0.0])
            C[p] = ti.Matrix.zero(ti.f32, 3, 3); F[p] = ti.Matrix.identity(ti.f32, 3)
            mu_p[p] = ms[p]; la_p[p] = ls[p]; yld_p[p] = ys[p]; pvol_p[p] = pv[p]; coh_p[p] = cz[p]

    @ti.kernel
    def substep():
        for I in ti.grouped(grid_m):
            grid_v[I] = ti.Vector.zero(ti.f32, 3); grid_m[I] = 0.0
        szz[None] = 0.0; wallf[None] = 0.0
        for p in range(n):
            if ti.static(FIBRE_ROD):
                x_pre[p] = x[p]                                  # fibre position before advection (→ rod velocity)
            base = (x[p] * inv_dx - 0.5).cast(int); fx = x[p] * inv_dx - base.cast(ti.f32)
            w = [0.5 * (1.5 - fx) ** 2, 0.75 - (fx - 1.0) ** 2, 0.5 * (fx - 0.5) ** 2]
            U, sig, V = ti.svd(F[p])
            J = sig[0, 0] * sig[1, 1] * sig[2, 2]
            P = (2 * mu_p[p] * (F[p] - U @ V.transpose()) @ F[p].transpose()
                 + ti.Matrix.identity(ti.f32, 3) * la_p[p] * J * (J - 1))     # Kirchhoff τ = Jσ
            if ti.static(COH > 0.0):                                         # per-point cohesion (SE cold-weld/
                if coh_p[p] > 0.0 and J < 1.0:                               # vdW; PTFE binder ~5× stickier):
                    P += coh_p[p] * J * ti.Matrix.identity(ti.f32, 3)        # attractive σ in compression → binds
            szz[None] += -P[2, 2] / J                                         # -σzz = compressive axial pressure (GPa)
            pm = pvol_p[p]                                                    # per-point vol = mass (ρ=1)
            st = (-dt * pm * 4 * inv_dx * inv_dx) * P; affine = st + pm * C[p]
            for a, b, c in ti.static(ti.ndrange(3, 3, 3)):
                off = ti.Vector([a, b, c]); dpos = (off.cast(ti.f32) - fx) * dx
                wt = w[a][0] * w[b][1] * w[c][2]
                node = base + off
                if ti.static(PERIODIC):                                  # wrap x,y into the periodic box
                    node[0] = _LO + ((node[0] - _LO) % _WC + _WC) % _WC
                    node[1] = _LO + ((node[1] - _LO) % _WC + _WC) % _WC
                grid_v[node] += wt * (pm * v[p] + affine @ dpos)
                grid_m[node] += wt * pm
        for I in ti.grouped(grid_m):
            if grid_m[I] > 0:
                grid_v[I] /= grid_m[I]
                if ti.static(scaffold_on):                              # fixed AM = rigid obstacle (v=0)
                    if am_mask[I] > 0:
                        grid_v[I] = ti.Vector.zero(ti.f32, 3)
                    else:
                        if ti.static(SE_AM_DRAG > 0.0):                  # ★ SE-AM confinement: damp SE flow near AM
                            grid_v[I] *= ti.max(0.0, 1.0 - SE_AM_DRAG * am_near[I])  # local conform, suppress migration
                i, j, k = I[0], I[1], I[2]
                if k * dx < FLOOR and grid_v[I][2] < 0: grid_v[I][2] = 0.0
                if k * dx > wall_z[None]:                                    # servo platen (rigid)
                    wallf[None] += grid_m[I] * (grid_v[I][2] - wall_vel[None])  # reaction impulse Σ m·Δv
                    grid_v[I][2] = wall_vel[None]
                if ti.static(not PERIODIC):                                  # rigid lateral walls (else x,y wrap)
                    if i * dx < SW[0] and grid_v[I][0] < 0: grid_v[I][0] = 0.0
                    if i * dx > SW[1] and grid_v[I][0] > 0: grid_v[I][0] = 0.0
                    if j * dx < SW[0] and grid_v[I][1] < 0: grid_v[I][1] = 0.0
                    if j * dx > SW[1] and grid_v[I][1] > 0: grid_v[I][1] = 0.0
        for p in range(n):
            base = (x[p] * inv_dx - 0.5).cast(int); fx = x[p] * inv_dx - base.cast(ti.f32)
            w = [0.5 * (1.5 - fx) ** 2, 0.75 - (fx - 1.0) ** 2, 0.5 * (fx - 0.5) ** 2]
            nv = ti.Vector.zero(ti.f32, 3); nc = ti.Matrix.zero(ti.f32, 3, 3)
            for a, b, c in ti.static(ti.ndrange(3, 3, 3)):
                off = ti.Vector([a, b, c]); dpos = off.cast(ti.f32) - fx
                wt = w[a][0] * w[b][1] * w[c][2]
                node = base + off
                if ti.static(PERIODIC):                                  # gather from the wrapped node
                    node[0] = _LO + ((node[0] - _LO) % _WC + _WC) % _WC
                    node[1] = _LO + ((node[1] - _LO) % _WC + _WC) % _WC
                gv = grid_v[node]
                nv += wt * gv; nc += 4 * inv_dx * wt * gv.outer_product(dpos)
            v[p] = nv; C[p] = nc; F[p] = (ti.Matrix.identity(ti.f32, 3) + dt * nc) @ F[p]
            eps_acc[p] += (0.5 * (nc + nc.transpose())).norm() * dt   # total strain increment (vs seed, incl elastic)
            U, sig, V = ti.svd(F[p])
            e = ti.Vector([ti.log(ti.max(sig[0, 0], 1e-4)), ti.log(ti.max(sig[1, 1], 1e-4)),
                           ti.log(ti.max(sig[2, 2], 1e-4))])
            tr = (e[0] + e[1] + e[2]) / 3.0
            d = e - ti.Vector([tr, tr, tr]); dn = d.norm() + 1e-9
            dg = dn - yld_p[p] / (2 * mu_p[p])
            if dg > 0:
                dg_acc[p] += dg                                 # accumulate plastic strain (morphology colour)
                e = (d - dg * d / dn) + ti.Vector([tr, tr, tr])
                F[p] = U @ ti.Matrix([[ti.exp(e[0]), 0, 0], [0, ti.exp(e[1]), 0],
                                      [0, 0, ti.exp(e[2])]]) @ V.transpose()
            x[p] += dt * v[p]
            if ti.static(PERIODIC):                                      # wrap x,y into [SW0, SW0+LATW)
                x[p][0] -= _LATW * ti.floor((x[p][0] - _SW0) / _LATW)
                x[p][1] -= _LATW * ti.floor((x[p][1] - _SW0) / _LATW)

    @ti.kernel
    def rod_pass():                          # one PBD/XPBD Jacobi pass over the fibre rods (VGCF/PTFE)
        for p in range(n):
            rod_dx[p] = ti.Vector.zero(ti.f32, 3)
        for p in range(n):
            if rod_is[p] == 1:
                q = rod_next[p]
                if q >= 0:                   # distance (hard, inextensible): edge p→q back to rest length
                    d = x[q] - x[p]; Ln = d.norm() + 1e-9; nrm = d / Ln
                    dl = -0.5 * (Ln - rod_rl[p])
                    rod_dx[p] += -dl * nrm; rod_dx[q] += dl * nrm
                pr = rod_prev[p]
                if pr >= 0 and q >= 0:       # bending (soft): restore the seeded rest curvature b0
                    bvec = x[pr] - 2.0 * x[p] + x[q] - rod_b0[p]
                    Cb = bvec.norm() + 1e-9; nb = bvec / Cb
                    db = -(ROD_STIFF * rod_kfac[p]) * Cb / 6.0
                    rod_dx[pr] += db * nb; rod_dx[p] += -2.0 * db * nb; rod_dx[q] += db * nb
        for p in range(n):
            if rod_is[p] == 1:
                x[p] += ROD_OMEGA * rod_dx[p]            # under-relaxed Jacobi (a node sits in ≤5 constraints)

    @ti.kernel
    def rod_setv():                          # corrected positions → velocity (two-way rod↔SE coupling)
        for p in range(n):
            if rod_is[p] == 1:
                v[p] = (x[p] - x_pre[p]) / dt

    load(xs, mus, las, ylds, pvs, coh_np)
    area = (_LATW * _LATW if PERIODIC else WIDTH * WIDTH)   # periodic → grid-aligned cell area (self-consistent)
    target = args.target_gpa
    vmax = 0.008 * (WALL0 - FLOOR)                           # platen speed (slow = quasi-static)
    wall_z[None] = WALL0
    comp = (f"scaffold ({len(am_r)} fixed AM + SE "
            + ("se_dump REAL positions)" if args.se_dump else f"se_frac={args.se_frac})") if args.am_scaffold
            else "real14 (3-comp 12:4:1, AM:SE 73:27)" if args.preset == 'real14'
            else f"{args.material} (am_frac={am_frac})")
    if not args.quiet:
        gshape = f"{n_grid}" if nz == n_grid else f"{n_grid}×{n_grid}×{nz}"
        print(f"3D MPM  grid={gshape}  pts={n}  arch={args.arch}  {comp}  "
              f"E_SE={args.e_se} σy={args.sigma_y} ν_SE={args.nu_se} K_SE={K_SE:.2f}GPa  "
              f"target={target} GPa  readout={args.readout}  "
              + (f"am_load_frac={args.am_load_frac:.3f}" + (f" floor_porosity={args.floor_porosity:.1f}% (engage {args.floor_engage:.1f}%)" if args.floor_porosity > 0 else f" → SE_target={target*(1.0-args.am_load_frac):.4f} GPa") + "  " if args.am_load_frac > 0 else "")
              + f"xy={'periodic' if PERIODIC else 'walls'}")
    reached = False; conv = 0; por_end = 0.0; p_end = 0.0; por_at_target = -1.0; por0 = 100.0; relax = 0
    reach_cnt = 0; STOP_HOLD = 3            # loose→dense mix: need target SUSTAINED this many frames to stop
    for frame in range(args.frames):
        sacc = 0.0; wacc = 0.0
        for _ in range(args.sub):
            substep()
            if FIBRE_ROD:                                    # Tier-2: rods buckle emergently under the press
                for _r in range(args.rod_iters):
                    rod_pass()
                rod_setv()
            sacc += szz[None] / n                            # volume-mean Cauchy σzz (GPa)
            wacc += wallf[None] / (dt * area)                # platen reaction stress (GPa), resolution-invariant
        sig_mean = sacc / args.sub
        wallp = wacc / args.sub
        p = wallp if args.readout == 'wallP' else sig_mean   # servo signal
        height = wall_z[None] - FLOOR
        por = max(0.0, 1.0 - solid_vol / (area * height)) * 100.0
        if frame == 0:
            por0 = por
        # servo platen to target σzz (descend until target, then fine bidirectional).
        # arm-after-compaction guard: a big rigid AM (preset/mix, AM = MATERIAL) hitting the
        # platen on first contact spikes wallP transiently → refuse to stop until the bed has
        # actually compacted (por ≤ por0 − 5 %p).  The scaffold (AM = fixed grid mask) has NO
        # such transient, and the guard there forces a 5 %p over-descent regardless of stress,
        # which OVER-COMPRESSES dense (high se_frac) beds → disable it for the scaffold.
        if not reached:
            step = vmax
            if args.compact_to > 0:                          # displacement-driven → descend to a target porosity
                descend = por > args.compact_to
                if por < args.compact_to + 5.0:              # slow near the target → less overshoot
                    step = vmax * 0.25
            elif args.am_scaffold:
                # ROBUST wallP CONDITIONAL (skeleton-spring) — works across ALL regimes incl. SE-rich:
                # the rigid AM skeleton bears up to f_AM*target, but ONLY once the bed compresses to its
                # DEM rigid-packing floor (--floor-porosity), where the AM jams.  ABOVE the floor the SE
                # bears the FULL load → dense / SE-rich beds that reach `target` above the floor are
                # UNCHANGED (no over-correction — fixes the flaw where a flat f_AM broke real14/SE-rich).
                # BELOW the floor the AM share ramps in (over --floor-engage) → stops the SE-poor/mono-
                # large over-compression near the DEM floor, keeping a small plastic increment.
                # f_AM (=--am-load-frac) = AM-AM axial load share (scripts/dem_am_load_fraction.py).
                # floor<=0 OR f_AM=0 → legacy (SE bears all = original validated behaviour).
                if args.floor_porosity > 0.0 and args.am_load_frac > 0.0:
                    engage = min(1.0, max(0.0, (args.floor_porosity - por) / max(args.floor_engage, 1e-6)))
                    am_skel = args.am_load_frac * target * engage      # AM skeleton stress, engages below floor
                else:
                    am_skel = args.am_load_frac * target               # legacy flat (no floor)
                # ★ HARD AM-jamming stop (2026-06-27): the stress-share criterion alone lets a SOFT SE
                # SLIP PAST the floor (SE-poor corners: SE meets its (1-f_AM)·target share only ~5-7%p
                # below the floor → catastrophic over-compaction, e.g. 100_12 → 11.6 < floor 13.3).  The
                # frozen AM is fixed at its DEM-compacted (jammed) positions, so once the bed reaches the
                # floor the rigid AM-AM network has JAMMED and physically blocks further platen descent —
                # a porosity-based stop, NOT a stress-based one.  Gated on am_load_frac>0 (conditional
                # active = AM load-bearing); SE-rich (f_AM≈0) and legit void-fill (stop above floor) are
                # untouched.  This is physics (AM jam at DEM packing), not a DEM clamp.
                hard_floor = (args.am_load_frac > 0.0 and args.floor_porosity > 0.0
                              and por <= args.floor_porosity)
                am_jam = (am_jam_z > 0.0 and wall_z[None] <= am_jam_z)   # ★ OPTION C: platen reached percolating AM top → rigid jam
                descend = (p + am_skel < target) and not hard_floor and not am_jam
            else:
                # loose→dense mix: a big rigid AM hitting the platen spikes wallP for ~1 frame, which
                # froze the platen in the loose state (premature stop → slow crawl).  Keep descending
                # at full vmax until the bed SUSTAINS ≥ target for STOP_HOLD frames (after por≤por0−5);
                # if it never sustains, the continuum SE is over-flowing (no granular jam) and it
                # descends to WALL_MIN — itself an informative result (porosity→~0 = over-compaction).
                guard = (por > por0 - 5.0)
                reach_cnt = reach_cnt + 1 if (p >= target and not guard) else 0
                descend = reach_cnt < STOP_HOLD
            if descend:
                wall_vel[None] = -step / (args.sub * dt)
                wall_z[None] = max(WALL_MIN, wall_z[None] - step)
            else:
                reached = True; wall_vel[None] = 0.0
        elif args.protocol == 'hold' or args.compact_to > 0:
            # LIGGGHTS protocol: platen FIXED at the first-300-MPa position; relax (stress settles,
            # plate does not move → porosity stays at porosity@target).  No bidirectional over/under-shoot.
            wall_vel[None] = 0.0; relax += 1
            if relax >= 40 and frame > 20:
                if not args.quiet:
                    print("  ✓ held at target, relaxed (LIGGGHTS protocol)")
                break
        else:
            step = 0.12 * vmax                                   # bidirectional: equilibrate AT target
            if p > 1.02 * target:
                wall_z[None] = min(WALL0, wall_z[None] + step); wall_vel[None] = step / (args.sub * dt)
            elif p < 0.98 * target:
                wall_z[None] = max(WALL_MIN, wall_z[None] - step); wall_vel[None] = -step / (args.sub * dt)
            else:
                wall_vel[None] = 0.0
            conv = conv + 1 if abs(p - target) < 0.03 * target else 0
        por_end = por; p_end = p
        if reached and por_at_target < 0:
            por_at_target = por                              # porosity when target stress was FIRST reached
        if not args.quiet and (frame % args.print_every == 0 or conv >= 12):
            thick = f"  thickness={height*um_box:5.2f}µm" if um_box > 0 else ""
            print(f"  frame {frame:3d} [{'descend' if not reached else 'servo'}]  "
                  f"{args.readout}={p:7.4f} GPa (wallP={wallp:.4f} σzz_vol={sig_mean:.4f})  "
                  f"porosity={por:6.2f}%  wall_z={wall_z[None]:.3f}{thick}", flush=True)
        if conv >= 12 and frame > 20:
            if not args.quiet:
                print("  ✓ converged: σzz equilibrated at target")
            break
    por_target_str = f"{por_at_target:.2f}%" if por_at_target >= 0 else "n/a (target never reached)"
    scaf = (f"scaffold {len(am_r)}AM " + ("se_dump(real)" if args.se_dump else f"se_frac={args.se_frac}")
            if args.am_scaffold else f"am_frac={am_frac}")
    thick_str = (f"  thickness={(wall_z[None] - FLOOR) * um_box:.2f}µm" if um_box > 0 else "")
    print(f"FINAL  {args.readout}={p_end:.4f} GPa  porosity(settled)={por_end:.2f}%  "
          f"porosity@target={por_target_str}{thick_str}   "
          f"[MPM, {comp.split()[0]}, {scaf}, n_grid={n_grid}, pts={n}, "
          f"E_SE={args.e_se} ν_SE={args.nu_se} K_SE={K_SE:.1f}GPa, readout={args.readout}, "
          f"xy={'periodic' if PERIODIC else 'walls'}]")
    cov_out = {}
    if args.am_scaffold:
        # COVERAGE: fraction of each AM-type surface (AM↔non-AM voxel interfaces) that faces SE
        # (vs void).  The MPM SE plastically conforms to the AM, so this is the REAL coverage —
        # validates the DEM coverage post-corrections (Hertz / Tabor-physics / B3 shape-corr).
        xf = x.to_numpy()
        ci = (xf * n_grid).astype(int)
        ci[:, :2] = np.clip(ci[:, :2], 0, n_grid - 1); ci[:, 2] = np.clip(ci[:, 2], 0, nz - 1)
        try:
            from scipy import ndimage as _ndi
        except Exception:
            _ndi = None
        # close the discrete occupancy to fill point-sampling holes at the interface —
        # the raw 'point in the adjacent cell' measure UNDER-counts coverage otherwise
        # (geometric ground-truth is ~16 % touching / ~49 % within 0.14 µm; raw read ~26 %).
        def _occ_of(sel):                                     # boolean cell occupancy of a point-subset (+ hole-close)
            occ = np.zeros((n_grid, n_grid, nz), bool)
            if sel.any():
                cc = ci[sel]
                occ[cc[:, 0], cc[:, 1], cc[:, 2]] = True
                if _ndi is not None:
                    occ = _ndi.binary_closing(occ, iterations=1)
            return occ
        # ★ SE-only coverage (phase==1) = the TRUE SE coverage validating DEM Hertz/Tabor.  The additive
        # points (VGCF/SuperP/PTFE, phase>1) are ALSO material points in x, so lumping them here would
        # inflate "coverage by SE" (SuperP handmix's cov drop was 100 % the carbon component, mislabeled).
        # → count them SEPARATELY as additive-on-AM coverage (the σ_e-relevant contact).  Carbon-free runs
        # (real_14 validation) have no additive points → SE coverage byte-unchanged.
        _is_se = (phase_np == 1) if 'phase_np' in locals() else np.ones(len(ci), bool)
        se_occ = _occ_of(_is_se)
        add_occ = _occ_of(~_is_se) if (~_is_se).any() else None
        if PERIODIC:                                          # roll must wrap WITHIN the box, not the dead
            sl = slice(_LO, _LO + _WC)                        # margin → slice the periodic cell for x,y
            pin_c = pin_np[sl, sl, :]; se_c2 = se_occ[sl, sl, :]
            add_c = add_occ[sl, sl, :] if add_occ is not None else None
        else:
            pin_c, se_c2 = pin_np, se_occ
            add_c = add_occ
        def _cov_frac(occ_c, amt):                            # fraction of AM_t surface voxels facing occ_c
            tot = 0; cov = 0
            for ax in range(3):
                for s in (1, -1):
                    iface = amt & (np.roll(pin_c, s, ax) == 0)   # AM_t voxel with a non-AM neighbour
                    tot += int(iface.sum())
                    cov += int((iface & np.roll(occ_c, s, ax)).sum())
            return (100.0 * cov / tot if tot else 0.0), cov, tot
        for t, nm in ((1, 'AM_P'), (2, 'AM_S')):
            amt = (pin_c == t)
            pct, cov, tot = _cov_frac(se_c2, amt)
            cov_out[nm] = round(pct, 1)
            if tot:
                print(f"  coverage {nm} by SE = {pct:5.1f}%   ({cov:,}/{tot:,} surface voxels)")
            if add_c is not None:                             # additive (carbon/soft-fibre) coverage of AM = σ_e contact
                apct, acov, _ = _cov_frac(add_c, amt)
                cov_out[nm + '_add'] = round(apct, 1)
                if tot:
                    print(f"  coverage {nm} by additive = {apct:5.1f}%   ({acov:,}/{tot:,})")
    if args.save_metrics:
        # ── ALL raw MPM outputs → one structured JSON (the webapp's MPM source) ──────────────
        import json as _json
        m = {
            'porosity_settled_pct': round(float(por_end), 3),
            'porosity_at_target_pct': round(float(por_at_target), 3) if por_at_target >= 0 else None,
            'thickness_um': round(float((wall_z[None] - FLOOR) * um_box), 3) if um_box > 0 else None,
            'wall_z': round(float(wall_z[None]), 4),
            'um_box_um': round(float(um_box), 4) if um_box > 0 else None,   # µm per box unit (payload scale)
            'final_stress_GPa': round(float(p_end), 4), 'target_GPa': float(target),
            'am_load_frac': float(args.am_load_frac),
            'floor_porosity_pct': float(args.floor_porosity) if args.floor_porosity > 0 else None,
            'se_target_GPa': round(float(target * (1.0 - args.am_load_frac)), 4) if (args.am_load_frac > 0 and args.floor_porosity <= 0) else None,
            'coverage_AM_P_pct': cov_out.get('AM_P'), 'coverage_AM_S_pct': cov_out.get('AM_S'),
            # additive(carbon/soft-fibre)-on-AM coverage (σ_e contact), SEPARATE from SE coverage above;
            # None for carbon-free runs.  SE keys are now SE-ONLY (were SE+additive conflated pre-2026-07-03).
            'coverage_AM_P_add_pct': cov_out.get('AM_P_add'), 'coverage_AM_S_add_pct': cov_out.get('AM_S_add'),
            'n_grid': int(n_grid), 'nz': int(nz), 'n_pts': int(n),
            'E_SE_GPa': float(args.e_se), 'nu_SE': float(args.nu_se),
            'sigma_y_GPa': float(args.sigma_y), 'K_SE_GPa': round(float(K_SE), 3),
            'protocol': args.protocol, 'readout': args.readout,
            'se_dump': bool(args.se_dump), 'se_frac': float(args.se_frac),
            'periodic': bool(PERIODIC),
            'dilate_z': round(float(args.dilate_z), 4) if (args.am_scaffold and float(args.dilate_z) > 1.0) else None,   # stiff-fibre prop-open stretch (None = off / no-op without a scaffold)
        }
        if args.am_scaffold:
            m.update({
                'seed_AM_frac_pct': round(float(f_am), 2), 'seed_SE_frac_pct': round(float(f_se), 2),
                'SE_of_solid_pct': round(100.0 * se_solid / max(am_solid + se_solid, 1e-12), 2),
                'bulk_density_g_cm3': round(float(bulk_rho), 3), 'n_AM': int(len(am_r)),
            })
        _add_meta = locals().get('_add_meta') or {}          # per-additive recipe+physics (if additives seeded)
        if _add_meta:
            m['additives'] = _add_meta                       # {VGCF:{wt_pct,vol%,n_obj,n_pts,E,σ_y,curl}, …} → 요약
            m['fibre_rod'] = bool(FIBRE_ROD)                 # Tier-2 emergent buckling on?
            m['fibre_stiff'] = bool(args.fibre_stiff)        # VGCF load-bearing rigid strut (compaction-resistance)?
            if FIBRE_ROD:                                    # record the rod knobs so runs are distinguishable
                m['rod_stiff'] = float(args.rod_stiff); m['rod_iters'] = int(args.rod_iters)
        _json.dump(m, open(args.save_metrics, 'w'), indent=2)
        print(f"  saved metrics → {args.save_metrics}  ({len(m)} fields)")
    if args.save_se:
        np.save(args.save_se, x.to_numpy())                # final SE point cloud (morphology)
        print(f"  saved SE morphology → {args.save_se} ({n} pts)")
    if args.save_dg:
        dgn = dg_acc.to_numpy()
        np.save(args.save_dg, dgn)                          # accumulated plastic strain (same order)
        print(f"  saved plastic strain Σdg → {args.save_dg} ({n} pts, "
              f"mean {float(dgn.mean()):.3f} max {float(dgn.max()):.3f})")
    if args.save_eps:
        en = eps_acc.to_numpy()
        np.save(args.save_eps, en)                          # accumulated TOTAL strain vs seed (same order)
        print(f"  saved total strain (vs seed) → {args.save_eps} ({n} pts, "
              f"mean {float(en.mean()):.3f} max {float(en.max()):.3f})")
    if args.save_phase:
        np.save(args.save_phase, phase_np)                  # 1 SE · 2 VGCF · 3 SuperP · 4 PTFE (0 AM)
        _u, _c = np.unique(phase_np, return_counts=True)
        print(f"  saved phase → {args.save_phase} ({n} pts, "
              + " ".join(f"{int(u)}:{c}" for u, c in zip(_u, _c)) + ")")
    if args.save_fibre and fibre_np is not None:
        np.save(args.save_fibre, fibre_np)                  # -1 = SE/SuperP, ≥0 = fibre index (VGCF/PTFE)
        print(f"  saved fibre ids → {args.save_fibre} ({n} pts, {int(fibre_np.max()) + 1} fibres)")
    if args.save_fibre_dia and dia_np is not None:
        np.save(args.save_fibre_dia, dia_np)                # per-point relative Ø (∝√weight; PTFE draw d∝√(V/L))
        _fd = dia_np[dia_np > 0]
        print(f"  saved fibre Ø → {args.save_fibre_dia} ({n} pts, "
              f"Ø rel {(_fd.min() if len(_fd) else 0):.2f}..{(_fd.max() if len(_fd) else 0):.2f})")
    if args.save_se_id:
        se_id_full = np.full(n, -1, np.int32)               # carbon / non-SE = -1; base SE pts = particle id
        if se_id_base is not None:
            se_id_full[:len(se_id_base)] = se_id_base       # base SE pts are points 0..len-1 (carbon appended)
        else:
            print("  ⚠ --save-se-id without --se-dump → all -1 (per-particle ids need real SE centres). "
                  "The voxel contact-network (--se-id) will return None.")
        np.save(args.save_se_id, se_id_full)
        _nid = len(np.unique(se_id_full[se_id_full >= 0]))
        print(f"  saved SE particle ids → {args.save_se_id} ({n} pts, {_nid} SE particles)")


if __name__ == '__main__':
    main(sys.argv[1:])
