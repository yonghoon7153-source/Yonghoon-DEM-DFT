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


# ─────────────────────────────────────────────────────────────────────────────────────────────
#  PLASTIC-HISTORY RESTART  (--save-state / --load-state)   [docs/temp_pressure_capability.md §6-B P1.5]
#
#  WHY.  A real cell is FABRICATED at ~300 MPa, then UNLOADED, then cycled while a ~90 MPa
#  operating stack pressure is held.  Every run of this script used to re-seed PRISTINE SE and
#  reset the plastic history (F[p]=I in `load`), so `--target-gpa 0.09` produced a VIRGIN electrode
#  compacted at 90 MPa — NOT a 300-MPa-fabricated electrode re-equilibrated at 90 MPa.  Saving and
#  restoring the deformation gradient F (which carries BOTH the elastic stress state and the
#  accumulated plastic shape change) makes the 2-stage protocol expressible:
#      ① --protocol hold --target-gpa 0.30  --save-state s.npz          (fabrication)
#      ② --load-state s.npz --protocol servo --target-gpa 0.09 --cycle-deform   (operation)
#
#  v AND C ARE SAVED BUT ZEROED ON LOAD — deliberate.  The restart is QUASI-STATIC: stage ① ends
#  with the bed relaxed under the platen, so the physical state is "stress stored in F, motion ≈ 0".
#  Re-injecting a stale velocity/affine field would inject spurious kinetic energy across a protocol
#  change (the platen BC and the target stress differ between the two stages), and MPM's APIC C is a
#  per-step reconstruction, not a state variable.  They are written to the npz for auditability only.
#  This choice is recorded in the npz meta as `restart_velocity_convention`.
STATE_SCHEMA = 'mpm3d_state_v1'

# arrays that MUST be present and finite in a state file (per-point, len == n_pts)
_STATE_REQUIRED = ('x', 'F', 'mu_p', 'la_p', 'yld_p', 'pvol_p', 'coh_p', 'dg_acc', 'eps_acc')
# meta keys that MUST match bit-for-bit between the saved run and the restarting run
_STATE_HARD_META = ('n_grid', 'nz', 'lateral_box', 'periodic')


def state_fingerprint(am_pos, am_r_pristine):
    """Stable short fingerprint of the FROZEN AM scaffold GEOMETRY in BOX-frame coordinates.

    Uses the PRISTINE radii (the raw CSV radii × scl, captured before --cycle-deform /
    --fracture-scaffold rescale them) precisely so that a cycle-breathing restart — which is the
    whole point of this feature — does NOT trip the guard: the AM radii are SUPPOSED to change
    between stages, the AM CENTRES and COUNT are not.  A different electrode / a different
    --lateral-box / a different --dilate-z all move the centres → different fingerprint → refused."""
    import hashlib
    h = hashlib.sha256()
    p = np.ascontiguousarray(np.asarray(am_pos, np.float64).reshape(-1, 3))
    r = np.ascontiguousarray(np.asarray(am_r_pristine, np.float64).ravel())
    h.update(np.int64(len(r)).tobytes()); h.update(p.tobytes()); h.update(r.tobytes())
    return h.hexdigest()[:16]


def state_guard_errors(saved_meta, cur_meta, saved_am_pos, saved_am_r0,
                       cur_am_pos, cur_am_r0, atol=1e-9):
    """Pure-numpy compatibility check for --load-state.  Returns a list of human-readable errors
    (empty = compatible).  HARD: schema version · n_grid · nz · lateral_box · periodic · AM count ·
    AM centres · AM PRISTINE radii.  DELIBERATELY NOT CHECKED: the APPLIED (deformed) AM radii —
    --cycle-deform / --fracture-scaffold change them by design."""
    errs = []
    sv = str(saved_meta.get('schema', ''))
    if sv != STATE_SCHEMA:
        errs.append(f"schema mismatch: state file is '{sv}', this build expects '{STATE_SCHEMA}'")
    for k in _STATE_HARD_META:
        a, b = saved_meta.get(k), cur_meta.get(k)
        if isinstance(a, float) or isinstance(b, float):
            same = (a is not None and b is not None and abs(float(a) - float(b)) <= 1e-12)
        else:
            same = (a == b)
        if not same:
            errs.append(f"{k} mismatch: state={a!r} run={b!r}")
    sp = np.asarray(saved_am_pos, np.float64).reshape(-1, 3)
    cp = np.asarray(cur_am_pos, np.float64).reshape(-1, 3)
    sr = np.asarray(saved_am_r0, np.float64).ravel()
    cr = np.asarray(cur_am_r0, np.float64).ravel()
    if len(sp) != len(cp):
        errs.append(f"AM scaffold COUNT mismatch: state={len(sp)} run={len(cp)}")
    else:
        if len(sp) and not np.allclose(sp, cp, rtol=0.0, atol=atol):
            nbad = int((np.abs(sp - cp).max(1) > atol).sum())
            errs.append(f"AM scaffold CENTRES differ in {nbad}/{len(sp)} spheres "
                        f"(max |Δ|={float(np.abs(sp - cp).max()):.3e} box) — different electrode/geometry")
        if len(sr) == len(cr) and len(sr) and not np.allclose(sr, cr, rtol=0.0, atol=atol):
            nbad = int((np.abs(sr - cr) > atol).sum())
            errs.append(f"AM scaffold PRISTINE radii differ in {nbad}/{len(sr)} spheres — different "
                        f"scaffold CSV (note: --cycle-deform/--fracture-scaffold radii are NOT compared)")
    return errs


def state_finite_errors(arrays):
    """Reject a corrupt / diverged state file: any non-finite (NaN/Inf) entry is fatal."""
    errs = []
    for k, a in arrays.items():
        a = np.asarray(a)
        if a.dtype.kind in 'fc' and not np.isfinite(a).all():
            errs.append(f"array '{k}' has {int((~np.isfinite(a)).sum())} non-finite (NaN/Inf) entries")
    return errs


# ─────────────────────────────────────────────────────────────────────────────────────────────
#  RESTART PLATEN LOGIC — pure helpers (no taichi), so the unload/guard/provenance rules that the
#  2026-07-28 review found broken are covered by --selftest instead of only by a GPU run.
# ─────────────────────────────────────────────────────────────────────────────────────────────
def restart_unload_needed(p_settle, target, band=0.10):
    """Decide, from the settle-window readings, whether the restart must UNLOAD (platen rises).

    Uses the MAX of the window on purpose: the reaction rebuilds from F over the window (v and C were
    zeroed), and the two possible mistakes are not symmetric — an unnecessary RISE is elastic and the
    servo band undoes it, an unnecessary DESCENT is plastic and irreversible.  An EMPTY window returns
    False (no unload); that case must never be reachable in a real run, which is why main() refuses
    --restart-settle < 1 rather than silently taking the frame-0 reading.

    ★ 2026-07-28: the trigger is the SAME band the acceptance test uses, not a bare `> target`.  A bed
    whose settled reading is already inside the band is AT the requested pressure — there is nothing
    to unload, and disturbing it only injects the transient the search then has to fight.  Observed
    directly: a restart that settled at 0.0947 GPa against a 0.0900 target (5 % over = in band) was
    sent unloading by the old bare comparison, rose 0.022 box, and ended at 0.0607 GPa having gained
    3.6 %p of porosity — strictly worse than doing nothing."""
    if not p_settle:
        return False
    return bool(max(p_settle) > (1.0 + float(band)) * float(target))


def settle_is_quasistatic(p_window, rel_tol=0.15, abs_floor=1e-4):
    """Is a frozen-platen window actually AT REST, or still ringing?

    The unload search assumes the probe reading is the quasi-static contact stress.  It is not, if the
    window is too short: v and C are zeroed on --load-state, so the reaction has to rebuild from F, and
    a 3-frame window on a stiff bed returns numbers that swing by more than the signal — a real trace
    read 0.1371 → 0.1785 → 0.2642 → 0.3028 GPa while the platen was RISING (p should fall), and other
    frames read NEGATIVE.  Bisecting on that cannot converge, and the failure looks like a search bug
    rather than what it is: the reading was never a pressure.

    ★ 2026-07-29 적대리뷰 수정 3건 (S-3 · S-5):
      (a) 샘플 < 3 은 이제 **정지 미증명**(False, inf)이다.  옛 코드는 (True, 0.0) 을 돌려줘
          `--restart-settle 1|2` 면 적응형 정착 전체가 no-op 이 되면서 provenance 에
          `settle_quasistatic: true, spread 0.0` = **측정한 적 없는 사실을 검증했다고 기록**했다.
          실제로 `settle_is_quasistatic([0.1371, 0.3028])` (121% 튀는 창)이 통과했다.
      (b) 창 **전체**의 max−min 을 본다.  옛 코드는 창을 아무리 늘려도 마지막 3점만 봐서,
          주기적 링잉이 **마루 위상**에서 통과했다(1.899/2.000/1.899 → spread 0.052 인데
          실제 진폭은 ±100%).  이것이 "p 를 2× 과소독"(0.0947 vs 실제 0.1781)의 직접 기전이다.
      (c) **추세 항** 추가.  [0.100, 0.093, 0.087] 처럼 단조 붕괴 중인 창이 스프레드만으로는
          통과했다(0.93^i 로 1.0→0.113 붕괴하는 창도 통과).  잔여 드리프트가 밴드를 넘으면 거부.
    rel_tol 기본은 호출부가 수용 밴드의 1/3 이하로 넘기는 것을 권장한다 (±15% 판독으로 ±10%
    밴드를 판정하던 비대칭이 S-5 지적사항이었다).

    Returns (ok, spread_rel).  ≥3 샘플 필요; 창 전체 진폭 + 꼬리 추세를 함께 본다."""
    if p_window is None or len(p_window) < 3:
        return False, float('inf')             # 정지를 **증명하지 못했다** (조용한 통과 금지)
    w = [float(v) for v in p_window]
    scale = max(abs(sum(w) / len(w)), float(abs_floor))
    spread = (max(w) - min(w)) / scale          # ★ 창 전체 (마지막 3점 아님)
    # 추세: 마지막 3점의 평균 기울기가 남은 창만큼 더 가면 얼마나 움직이나
    slope = (w[-1] - w[-3]) / 2.0
    drift = abs(slope * 3.0) / scale            # 3프레임 앞 외삽
    return bool(spread <= float(rel_tol) and drift <= float(rel_tol)), float(max(spread, drift))


def arm_guard_active(por, por0, is_restart):
    """arm-after-compaction guard for the non-scaffold descend branch.

    por0 is the FRAME-0 porosity.  On a fresh loose bed that is the loose packing, and the guard
    ('refuse to stop until the bed has compacted 5 %p') protects against a first-contact wallP spike.
    On a --load-state restart por0 is the ALREADY-COMPACTED porosity, so the same rule mandates another
    5 %p of plastic compaction with no stress justification — including when the restart target is
    LOWER (an unload request).  Hence: never active on a restart."""
    return bool(por > por0 - 5.0) and not bool(is_restart)


def rearm_cohesion(coh_cmdline, coh_state_max):
    """--load-state cohesion gate.  substep()'s cohesion term is behind a compile-time ti.static(COH>0)
    built from THIS run's --coh, while the per-point coh_p comes from the state → a restart without
    --coh silently drops the restored binder/cold-weld.  Returns (COH_effective, rearmed_value|None)."""
    coh = float(coh_cmdline)
    if float(coh_state_max) > 0.0 and coh <= 0.0:
        return float(coh_state_max), float(coh_state_max)
    return coh, None


def pick_rod_rest(state_arrays, n, rl_derived, b0_derived):
    """Rod rest length/curvature for a restart.  build_rod_topology derives them from the positions it is
    handed; on a restart those are the COMPRESSED positions, so a fibre that buckled under the press would
    take its buckled shape as stress-free.  Prefer the arrays saved by stage ①.
    Returns (rl, b0, source)."""
    if state_arrays is None:
        return rl_derived, b0_derived, 'seeded_this_run'
    ok = ('rod_rl' in state_arrays and 'rod_b0' in state_arrays
          and len(state_arrays['rod_rl']) == n and len(state_arrays['rod_b0']) == n)
    if ok:
        return (np.ascontiguousarray(state_arrays['rod_rl'], np.float32),
                np.ascontiguousarray(state_arrays['rod_b0'], np.float32).reshape(n, 3),
                'restored_from_state')
    return rl_derived, b0_derived, 'REDERIVED_from_compressed_positions'


def unload_verdict(p, target, band=0.10):
    """TWO-SIDED acceptance for the restart unload: 'above' | 'in_band' | 'below'.

    ★ 2026-07-28 (re-verify HIGH-a).  The previous test was one-sided — `p <= 1.02*target` — so a
    platen that rose clear of the bed and read p ≈ 0 PASSED it.  Combined with the coarse rise step
    (full vmax for as long as p > 1.5*target, i.e. the whole way down from ~1.2 GPa to 0.135 GPa)
    the platen routinely blew past the target in a single step and then "converged" on an
    out-of-contact state: porosity inflated, reaction ≈ 0, and the run still labelled itself
    `operating_stack_pressure`.  Unloading has a target, not a ceiling — under-shooting it by 100 %
    is exactly as wrong as over-shooting it, and the accept test has to say so."""
    t = float(target)
    if float(p) > (1.0 + float(band)) * t:
        return 'above'
    if float(p) < (1.0 - float(band)) * t:
        return 'below'
    return 'in_band'


def unload_next_z(z_now, z_lo, z_hi, wall0, step, floor_z=None):
    """Next platen height for the unload search, and the move kind.  Returns (z_next, kind).

    z_lo = highest height known to read ABOVE the band (still too compressed; starts at the restart
    height).  z_hi = lowest height known to read BELOW the band (overshot), or None while the target
    is not yet bracketed.

      • not yet bracketed → RISE by `step`, capped at wall0 (out of travel).      kind='rise'
      • bracketed         → BISECT the interval.                                  kind='bisect'

    ★ Why descending inside the bracket is legitimate here, even though the initial unload-vs-compact
      decision is deliberately biased against descending (see restart_unload_needed): that asymmetry
      is about NEW plastic compaction beyond the fabrication state.  Inside the bracket the platen
      only ever returns toward a stress ≤ (1+band)·target, which for an operating-pressure restart
      (90 MPa vs a 300 MPa fabrication) is far inside the yield surface the bed already carries — so
      it is elastic re-loading along the path it just came up, and it adds no plastic strain.  The
      `floor_z` guard makes that explicit: the search may never go below the height the restart
      started at, which is the height that carries the fabrication pressure."""
    if z_hi is None:
        return min(float(wall0), float(z_now) + float(step)), 'rise'
    mid = 0.5 * (float(z_lo) + float(z_hi))
    if floor_z is not None:
        mid = max(float(floor_z), mid)
    return mid, 'bisect'


def stage_pressure_role(is_restart, p_achieved, target, tol=1.25, tol_lo=0.75):
    """Provenance role string.  P_this_stage_MPa is the REQUEST; if the platen never brought the bed to
    it (silent no-op, out of travel, runaway unload, …) the role must say so, because the webapp badge
    renders the requested number next to this string.

    ★ 2026-07-28 (re-verify HIGH-a-provenance): the check used to be one-sided (`> tol*target`), which
    is precisely blind to the failure the unload fix is about.  A runaway unload lands at p ≈ 0, i.e.
    FAR BELOW target — and the old audit trail stamped that `operating_stack_pressure`, certifying the
    runaway as a good operating-pressure geometry.  Both directions are now tagged, with distinct
    suffixes so the JSON says which way it failed."""
    role = 'operating_stack_pressure' if is_restart else 'fabrication_pressure'
    if not (is_restart and target > 0):
        return role
    r = float(p_achieved) / float(target)
    if r > float(tol):
        return role + '_NOT_REACHED'          # still compressed — platen never unloaded
    if r < float(tol_lo):
        return role + '_OVER_UNLOADED'        # platen went past the target (often clear of the bed)
    return role


def write_state_npz(path, arrays, meta, compress=None, compress_max_bytes=1_500_000_000):
    """Write the restart state.  `meta` is JSON-serialised into a 0-d array so the npz stays a
    single self-describing file (np.savez cannot store dicts).

    compress=None → AUTO: deflate below `compress_max_bytes`, store uncompressed above it.  A
    production bed is tens of millions of material points (x+F+v+C+7 scalars ≈ 125 B/pt → multi-GB);
    those arrays are float noise that deflate barely shrinks, so paying minutes of zlib on them is a
    bad trade.  Both forms are read identically by np.load.  Returns (path, n_bytes, compressed)."""
    import json as _json
    out = {k: np.asarray(v) for k, v in arrays.items()}
    nbytes = int(sum(a.nbytes for a in out.values()))
    if compress is None:
        compress = nbytes <= compress_max_bytes
    out['meta_json'] = np.array(_json.dumps(meta, sort_keys=True))
    (np.savez_compressed if compress else np.savez)(path, **out)
    return path, nbytes, bool(compress)


def read_state_npz(path):
    """Read a state npz → (arrays dict, meta dict).  Raises on a missing/undecodable meta."""
    import json as _json
    z = np.load(path, allow_pickle=False)
    if 'meta_json' not in z.files:
        raise SystemExit(f"[load-state] {path}: no meta_json — not an mpm3d state file")
    meta = _json.loads(str(z['meta_json']))
    arrays = {k: z[k] for k in z.files if k != 'meta_json'}
    return arrays, meta


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
                         'variant-independent + FLAT in wt%% (no PTFE-style binder_cap arc: anchoring has no '
                         'fibrillation/over-crosslink peak mechanism).  The AM-interface anchoring '
                         '(γ ⚠INVALID: wrong-monomer 2026-07-10, DFT recompute pending — do NOT cite 0.93/0.42 J/m² '
                         'or −4.8/−3.0 eV, direction only) is represented STRUCTURALLY (film seeded ON the AM, seed_coat) — a '
                         'boundary-adhesion energy term is future work; do NOT put the interface γ-ratio '
                         'into this bulk coh (wrong term, both directions).')
    ap.add_argument('--sdcp-neutral', action='store_true',
                    help='SDCP NEUTRAL (−SO₃H) variant — recorded as provenance for STEP3 σ-weighting.  '
                         'Anchoring γ (⚠INVALID: wrong-monomer 2026-07-10, DFT recompute pending — 0.42/0.93 J/m²·−3.0/−4.8 eV 인용 금지) lives '
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
    ap.add_argument('--swcnt-wrap', type=float, default=-1.0,
                    help='A14 SWCNT sheath coverage fraction of each AM surface (surface_conformal).  <0 = '
                         'AUTO from the process row (1.0 all mixings — koo2026 ζ≈−1.9 near-complete pre-'
                         'assembled coverage, mixing-robust per Raman).  <1 seeds a contiguous partial CAP '
                         'per AM = degraded-wrapping what-if (un-anchored §F1 knob).')
    ap.add_argument('--dilate-z', type=float, default=1.0,
                    help='STIFF-FIBRE BED DILATION: stretch the frozen scaffold (AM + SE seed) z-offsets by this '
                         'factor before compaction — the prop-open thickness response a frozen-AM MPM cannot '
                         'produce emergently (skeleton rearrangement = granular force-chain physics = DEM-class). '
                         'The VALUE is derived upstream (mpm_input_from_case) from λ_dz = (1+φ_VGCF)·(1−ε_DEM)/'
                         '(1−ε_real), ε_real = ε_DEM + 0.5pp/wt%%(VGCF) — ONE empirical number (Cho 2024 LPSCl+VGCF '
                         'slope); Philipse rod-jamming φ_c≈5.4/(L/D)≈8vol%% bounds the regime (our strut onset '
                         'reproduces it).  Thickness/porosity respond BY CONSTRUCTION; coverage/network/strain '
                         'respond EMERGENTLY on the dilated bed.  z-only affine = die-press global mode (lateral '
                         'fixed); local non-affine rearrangement stays DEM territory.  1.0 = off (soft additives: '
                         'PTFE/SuperP flow into pores, no dilation — their thickness pin is the physics).')
    # ── A-1 cycle-deform (real_degrading_electrode_design §3 A-1) ────────────────────────────
    ap.add_argument('--cycle-deform', action='store_true',
                    help='A-1 (v1 ASSUMED-FORM): re-deform the frozen AM scaffold by the CHARGE-STATE lattice '
                         'ΔV (SC shrink / poly expand) BEFORE compaction, then let the SE MPM re-equilibrate '
                         'around the deformed skeleton → se_dump\' re-deformed geometry + EMERGENT porosity/'
                         'coverage/thickness at that state.  frame[5]=MPM (mechanics/void-fill re-flow); the '
                         'N→ΔV mapping and anchor-to-anchor trajectory belong to the ledger (A-3), NOT here — '
                         'this produces ONE deformed anchor at the ΔV you pass.  Centres & grid (dx/origin/'
                         'nz/FLOOR/lateral_box) + the bed reference-frame am_top stay PRISTINE across N so '
                         'porosity is measured in a FIXED box (N4 grid-invariance); only the AM radii (→ pin '
                         'mask, SE eviction, AM_vol) change.  Scaffold-only.')
    ap.add_argument('--cycle-dv-sc', type=float, default=-0.051,
                    help='SC (AM_S, single-crystal, scaffold type=2 in this file) whole-particle lattice volume-change fraction, '
                         'SIGNED (−=charge/contraction).  Default −0.051 = Kondrakov NMC811 c-axis collapse; '
                         'sweep to −0.059 (Yun/Kang).  Radius ×(1+ΔV)^(1/3).  ISOTROPIC approximation '
                         '(Kondrakov c-axis anisotropy ignored — for the c-aligned worst case pass the larger '
                         '|ΔV|).  ASSUMED-FORM: this is a charge-STATE deformation, not a per-cycle law.')
    ap.add_argument('--cycle-dv-poly', type=float, default=0.059,
                    help='poly (AM_P, polycrystalline, scaffold type=1 in this file) OUTER-SHELL reference ΔV magnitude, SIGNED '
                         '(+=microcrack grain-separation envelope EXPANSION — OPPOSITE sign to SC per the '
                         'anisotropic intergranular fracture; Parks/Yun).  Scaled by --dv-pct-poly before '
                         'use — do NOT put the full lattice ΔV/3 on the outer radius (the crack absorbs most '
                         'internally).  radius ×(1+ΔV_poly·dv_pct_poly)^(1/3).')
    ap.add_argument('--dv-pct-poly', type=float, default=0.30,
                    help='fraction of --cycle-dv-poly that reaches the poly OUTER radius (default 0.30: A9 '
                         'intergranular crack absorbs ~70%% internally as void; Kang&Shin size-weighting). '
                         'The rest is internal void (not resolved by the rigid-obstacle AM mask at this '
                         'grid → v1 reports it as a discount, not an explicit inner cavity).  Sweep axis.')
    ap.add_argument('--cycle-n', type=int, default=0,
                    help='anchor LABEL: which cycle N this deformed geometry represents (metadata only — the '
                         'physics is driven by ΔV, not N).  Lets A-3 map anchor→N.  0 = pristine/unlabelled.')
    # ── 취성 파괴 → MPM crack-void 게이트 (frame[5]: DEM=WHERE 균열 개시, MPM=morphology 결과) ──────────
    ap.add_argument('--fracture-scaffold', default='',
                    help='per-AM Auerbach 심각도 CSV (am_scaffold와 행-정렬; 마지막 두 열 = worst_stage_rank '
                         '(0 intact..4 pulv), f_over_pc).  scripts/dem_fracture_scaffold.py로 생성.  게이트 '
                         '통과 AM에 crack-void 반경감소 → SE ingress.  기본 미사용 = bitwise 동일(기본값 없음).')
    ap.add_argument('--fracture-min-stage', default='fragmentation',
                    choices=['fragmentation', 'pulverization'],
                    help='이 단계 이상만 crack-void 주입 (기본 fragmentation).  micro/multi crack은 열린 '
                         '부피≈0이라 MPM morphology에 기여 안 함(near-null) → crack-void 맵에서 제외 = '
                         '게이트 선택지도 frag/pulv만.  DEM 취성의 전-스펙트럼은 수송 f_intact가 담당.')
    ap.add_argument('--fracture-void-frag', type=float, default=0.15,
                    help='fragmentation AM의 crack-void 부피분율 (ASSUMED-FORM; r×(1−v)^⅓ → 유효반경 감소 → '
                         'SE가 균열공간 채움).  --dv-pct-poly와 같은 스윕-축 성격(문헌앵커 대기).')
    ap.add_argument('--fracture-void-pulv', type=float, default=0.35,
                    help='pulverization AM의 crack-void 부피분율 (ASSUMED-FORM; 분쇄 = 더 큰 열린 부피).')
    # ── 소성이력 restart (P1.5: 제작압 압밀 → 제하 → 구동압 유지) ────────────────────────────
    ap.add_argument('--save-state', default='',
                    help='런 종료 시 충실한 재시작 상태를 npz 로 저장: per-point x·F(변형구배=탄성응력+소성형상 '
                         '이력)·mu/la/yld/pvol/coh·Σdg·ε + phase/fibre/Ø/se_id + AM 스캐폴드 지문 + meta '
                         '(n_grid/nz/lateral_box/periodic/wall_z/target/protocol/E·ν·σ_y).  v(속도)·C(affine)도 '
                         '기록하지만 --load-state 는 0 으로 둔다(준정적 재시작).  기본 미지정 = 기존 동작 불변.')
    ap.add_argument('--load-state', default='',
                    help='--save-state 로 만든 npz 에서 SE 를 복원 — 시딩을 건너뛰고 소성이력(F)을 그대로 이어받는다. '
                         '★ 이것이 "300 MPa 로 제작된 전극을 90 MPa 구동압에서 재평형" 을 가능하게 하는 조각: '
                         '--load-state s.npz --protocol servo --target-gpa 0.09 [--cycle-deform].  AM 반경은 이 런의 '
                         '--cycle-deform/--fracture-scaffold 가 정한 대로 재구성되며(지문은 위치·개수·PRISTINE 반경만 '
                         '비교 → 사이클 호흡 허용), 스키마/n_grid/nz/lateral-box/periodic/AM 위치가 다르면 중단한다.')
    ap.add_argument('--restart-settle', type=int, default=3,
                    help='--load-state 전용 (다른 런에서는 완전 무시): 재시작 직후 플래튼을 이 프레임 수만큼 '
                         'FREEZE 하고 응력이 F 로부터 재구축되기를 기다린 뒤 "제하(platen 상승)냐 추가 압밀'
                         '(하강)이냐" 를 판정한다.  v·C 가 0 으로 초기화되므로 frame 0 의 wallP 는 아직 0 에 '
                         '가깝다 — 그 값으로 판정하면 이미 제작된 베드를 아래로 밀어버린다(수치 파라미터, '
                         '물리 앵커 아님).  판정은 창 안 p 의 MAX 로 한다(제하 쪽으로 편향 = 불필요한 상승은 '
                         '탄성이라 servo 밴드가 되돌리지만, 불필요한 하강은 소성=비가역).')
    ap.add_argument('--restart-settle-max', type=int, default=200,
                    help='--load-state 제하 전용: 정지-프로브 창의 **최대** 프레임 (--restart-settle 은 이제 '
                         '최소값).  창이 닫힐 때 정지 여부를 실제로 재고, 아직 울리면 최대치까지 더 기다린다. '
                         '★ 실측(n_grid 64): 3 프레임 → 꼬리 스프레드 ~100%%, p(z) 비단조(플래튼이 올라가는데 '
                         'p 가 커짐), p 가 2× 과소독(0.0947 vs 실제 0.1781); 30 프레임 → 스프레드 4%%, '
                         'p(z) 단조 0.1364→0.0830.  정착시간은 파동 통과시간(∝ n_grid)에 비례하므로 고정 '
                         '프레임 수는 해상도마다 틀린다 — 숫자가 아니라 **조건**을 기다린다.')
    ap.add_argument('--servo-band', type=float, default=0.02,
                    help='servo 평형 수용 밴드 (기본 ±2%% = 옛 데드밴드와 동일).  ★2026-07-29 S-1: '
                         'servo 는 이제 **정지 상태에서만** 판독한다 (이동→동결→판독).  옛 동작은 '
                         '움직이는 플래튼에서 읽어 limit cycle 로 발진했다 — 실측 685프레임 무감쇠 '
                         '(목표 0.09 에 −0.019↔+0.206).  --servo-legacy 로 옛 동작 복원 가능.')
    ap.add_argument('--servo-legacy', action='store_true',
                    help='옛 servo(움직이는 플래튼에서 판독) 복원 — **옛 코퍼스 바이트 재현 전용**. '
                         '이 경로는 limit cycle 로 발진하며 final_stress_GPa 와 provenance 도장이 '
                         '--frames 절단 위상에 좌우된다는 것이 확인된 상태다(적대리뷰 S-1).')
    ap.add_argument('--allow-unconverged-servo', action='store_true',
                    help='servo 가 밴드 안에서 수렴하지 못해도 계속 진행 (기본=중단).  실험 전용 — '
                         '산출물 state_provenance.servo_status 에 not_converged 가 박힌다.')
    ap.add_argument('--unload-band', type=float, default=0.10,
                    help='--load-state 제하 전용: 목표압 수용 밴드 (기본 ±10%%).  ★ 2026-07-28 이전에는 '
                         '수용조건이 한쪽(p ≤ 1.02·target)뿐이라 플래튼이 베드에서 완전히 떨어져 p≈0 이 된 '
                         '상태도 "제하 완료" 로 통과했다(=과제하 폭주).  제하는 천장이 아니라 목표이므로 '
                         '양쪽으로 판정한다 (수치 파라미터, 물리 앵커 아님).')
    ap.add_argument('--unload-max-probes', type=int, default=40,
                    help='--load-state 제하 전용: 정지-프로브 최대 횟수.  소진되면 값을 내놓지 않고 '
                         'not_converged 로 **중단**한다 (--allow-unconverged-unload 로만 완화).')
    ap.add_argument('--allow-unconverged-unload', action='store_true',
                    help='제하가 밴드 안에 수렴하지 못했을 때도 계속 진행 (기본=중단).  ★ 실험/디버그 전용 — '
                         '수렴하지 않은 제하의 porosity·두께·coverage 는 프로덕션 숫자가 아니며, 산출물은 '
                         'state_provenance.unload_status 와 P_this_stage_role 에 그 사실이 박힌다.')
    ap.add_argument('--selftest', action='store_true',
                    help='restart-state 계층 자체검증 (numpy 전용, taichi/GPU 불필요) 후 종료')
    return ap.parse_args(argv)


def _selftest():
    """--selftest: pure-numpy checks of the restart state layer (no taichi / no GPU needed)."""
    import json as _json
    import tempfile, os as _os
    ok = 0; fail = []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)

    rng = np.random.default_rng(0)
    n_am = 7
    am_pos = rng.uniform(0.1, 0.9, (n_am, 3))
    am_r0 = rng.uniform(0.01, 0.03, n_am)
    meta = {'schema': STATE_SCHEMA, 'n_grid': 64, 'nz': 64, 'lateral_box': 0.05, 'periodic': False}

    # 1. fingerprint: deterministic, and sensitive to geometry / count
    fp = state_fingerprint(am_pos, am_r0)
    chk('fingerprint deterministic', fp == state_fingerprint(am_pos.copy(), am_r0.copy()))
    _p2 = am_pos.copy(); _p2[3, 1] += 1e-6
    chk('fingerprint sees a moved AM', fp != state_fingerprint(_p2, am_r0))
    chk('fingerprint sees a dropped AM', fp != state_fingerprint(am_pos[:-1], am_r0[:-1]))
    chk('fingerprint sees a resized AM', fp != state_fingerprint(am_pos, am_r0 * 1.001))

    # 2. guards — the compatible case must be clean
    chk('compatible state passes', state_guard_errors(meta, dict(meta), am_pos, am_r0, am_pos, am_r0) == [])
    # each hard field individually caught
    for k, bad in (('schema', 'mpm3d_state_v0'), ('n_grid', 96), ('nz', 80),
                   ('lateral_box', 0.03), ('periodic', True)):
        m2 = dict(meta); m2[k] = bad
        errs = state_guard_errors(m2, dict(meta), am_pos, am_r0, am_pos, am_r0)
        chk(f'guard catches {k}', any(k.split("_")[0] in e or 'schema' in e for e in errs) and errs != [])
    chk('guard catches AM count',
        any('COUNT' in e for e in state_guard_errors(meta, dict(meta), am_pos, am_r0,
                                                     am_pos[:-1], am_r0[:-1])))
    chk('guard catches moved AM',
        any('CENTRES' in e for e in state_guard_errors(meta, dict(meta), am_pos, am_r0, _p2, am_r0)))
    chk('guard catches different pristine radii',
        any('PRISTINE' in e for e in state_guard_errors(meta, dict(meta), am_pos, am_r0,
                                                        am_pos, am_r0 * 1.02)))
    # ★ THE POINT OF THE FEATURE: a --cycle-deform run rescales the APPLIED radii; the guard must NOT
    #   fire, because only the PRISTINE radii (unchanged) are compared.
    am_r_deformed = am_r0 * (1.0 + (-0.051)) ** (1.0 / 3.0)
    chk('cycle-deform (applied radii change) does NOT trip the guard',
        state_guard_errors(meta, dict(meta), am_pos, am_r0, am_pos, am_r0) == []
        and not np.allclose(am_r_deformed, am_r0))

    # 3. non-finite rejection
    good = {'x': np.zeros((5, 3), np.float32), 'F': np.zeros((5, 3, 3), np.float32)}
    chk('finite arrays accepted', state_finite_errors(good) == [])
    badf = {k: v.copy() for k, v in good.items()}; badf['F'][2, 1, 1] = np.nan
    chk('NaN rejected', any('non-finite' in e for e in state_finite_errors(badf)))
    badi = {k: v.copy() for k, v in good.items()}; badi['x'][0, 0] = np.inf
    chk('Inf rejected', any('non-finite' in e for e in state_finite_errors(badi)))

    # 4. npz round-trip is bit-exact and carries the meta (incl. the v/C convention)
    npts = 11
    arrs = {'x': rng.random((npts, 3)).astype(np.float32),
            'F': rng.random((npts, 3, 3)).astype(np.float32),
            'v': rng.random((npts, 3)).astype(np.float32),
            'C': rng.random((npts, 3, 3)).astype(np.float32),
            'mu_p': rng.random(npts).astype(np.float32),
            'la_p': rng.random(npts).astype(np.float32),
            'yld_p': rng.random(npts).astype(np.float32),
            'pvol_p': rng.random(npts).astype(np.float32),
            'coh_p': rng.random(npts).astype(np.float32),
            'dg_acc': rng.random(npts).astype(np.float32),
            'eps_acc': rng.random(npts).astype(np.float32),
            'phase': np.ones(npts, np.int8),
            'am_pos': am_pos, 'am_r_pristine': am_r0, 'am_r_applied': am_r_deformed}
    m = dict(meta); m.update({'n_pts': npts, 'wall_z': 0.6157, 'target_gpa': 0.30,
                              'protocol': 'hold', 'am_fingerprint': fp, 'n_am': n_am,
                              'restart_velocity_convention': 'v_and_C_zeroed_on_load'})
    with tempfile.TemporaryDirectory() as td:
        for _cmp in (True, False):                       # both the deflate and the store path
            p = _os.path.join(td, f's{int(_cmp)}.npz')
            _, _nb, _got = write_state_npz(p, arrs, m, compress=_cmp)
            a2, m2 = read_state_npz(p)
            chk(f'round-trip all arrays present (compress={_cmp})', set(a2) == set(arrs))
            chk(f'round-trip bit-exact (compress={_cmp})',
                all(np.array_equal(a2[k], arrs[k]) for k in arrs))
            chk(f'round-trip meta (compress={_cmp})', m2 == _json.loads(_json.dumps(m, sort_keys=True)))
            chk(f'compress flag honoured ({_cmp})', _got is _cmp)
        chk('meta records the v/C zeroing convention',
            m2.get('restart_velocity_convention') == 'v_and_C_zeroed_on_load')
        chk('required arrays all present in a written state',
            all(k in a2 for k in _STATE_REQUIRED))
        # AUTO size rule: small state → deflate, oversized budget → store
        p = _os.path.join(td, 'auto.npz')
        chk('auto picks deflate under budget', write_state_npz(p, arrs, m)[2] is True)
        chk('auto picks store over budget',
            write_state_npz(p, arrs, m, compress_max_bytes=1)[2] is False)

    # ── 5. RESTART PLATEN LOGIC (2026-07-28 review: the unload arm was a silent no-op) ───────────
    #    A. UNLOAD decision.  The bug: a restart at a LOWER target could only push the platen DOWN.
    chk('unload: settled reaction ABOVE the new target → unload',
        restart_unload_needed([0.28, 0.30, 0.31], 0.09) is True)
    chk('unload: restart at a HIGHER target → no unload, normal descend',
        restart_unload_needed([0.05, 0.07, 0.08], 0.30) is False)
    chk('unload: frame-0 transient must NOT veto the unload (window MAX, not last/first)',
        restart_unload_needed([0.00, 0.02, 0.19], 0.09) is True
        and restart_unload_needed([0.19, 0.02, 0.00], 0.09) is True)
    chk('unload: empty settle window is refused (never silently "no unload")',
        restart_unload_needed([], 0.09) is False)     # main() raises on --restart-settle < 1

    #    B. arm-after-compaction guard must not re-arm on the restart porosity (forced 5 %p descent).
    chk('guard: fresh loose bed still guarded (unchanged behaviour)',
        arm_guard_active(75.0, 75.0, False) is True and arm_guard_active(69.0, 75.0, False) is False)
    chk('guard: DISABLED on a restart (would have forced 5 %p of extra plastic compaction)',
        arm_guard_active(17.6, 17.6, True) is False and arm_guard_active(68.3, 68.3, True) is False)

    #    C. cohesion gate re-armed from the state (else the restored binder is compiled out).
    chk('coh: restart without --coh re-arms the gate from the state',
        rearm_cohesion(0.0, 0.02) == (0.02, 0.02))
    chk('coh: explicit --coh wins and is not overwritten',
        rearm_cohesion(0.05, 0.02) == (0.05, None))
    chk('coh: cohesion-free state stays cohesion-free (no invented cohesion)',
        rearm_cohesion(0.0, 0.0) == (0.0, None))

    #    D. rod rest state: restored, or honestly reported as re-derived from the compressed bed.
    _n5 = 4
    _rl_d = np.array([0.9, 0.8, 0.7, 0.0], np.float32)          # derived from the COMPRESSED positions
    _b0_d = np.zeros((_n5, 3), np.float32)
    _rl_s = np.array([1.0, 1.0, 1.0, 0.0], np.float32)          # the true as-seeded rest length
    _b0_s = np.ones((_n5, 3), np.float32) * 0.01
    _rl_o, _b0_o, _src = pick_rod_rest({'rod_rl': _rl_s, 'rod_b0': _b0_s}, _n5, _rl_d, _b0_d)
    chk('rod: rest length/curvature restored from the state (buckled shape NOT taken as stress-free)',
        _src == 'restored_from_state' and np.array_equal(_rl_o, _rl_s) and np.array_equal(_b0_o, _b0_s))
    _rl_o2, _, _src2 = pick_rod_rest({}, _n5, _rl_d, _b0_d)
    chk('rod: state without rod arrays → re-derived AND flagged (not silently wrong)',
        _src2 == 'REDERIVED_from_compressed_positions' and np.array_equal(_rl_o2, _rl_d))
    chk('rod: length mismatch also falls back to the flagged path',
        pick_rod_rest({'rod_rl': _rl_s[:2], 'rod_b0': _b0_s[:2]}, _n5, _rl_d, _b0_d)[2]
        == 'REDERIVED_from_compressed_positions')
    chk('rod: a pristine (non-restart) run reports the seeded source',
        pick_rod_rest(None, _n5, _rl_d, _b0_d)[2] == 'seeded_this_run')

    #    E. provenance role must not claim an operating pressure the platen never reached.
    chk('provenance: a no-op restart (still at the fabrication pressure) is tagged NOT_REACHED',
        stage_pressure_role(True, 0.4169, 0.09) == 'operating_stack_pressure_NOT_REACHED')
    chk('provenance: a genuine unload keeps the plain role',
        stage_pressure_role(True, 0.088, 0.09) == 'operating_stack_pressure')
    # ★ 2026-07-28 정정: 이 자리에 있던 "0.054 vs 0.09(=60 %) 도 정상" 단언이 바로 과제하 폭주를
    #   승인하던 사각지대였다.  runaway 는 p→0, 즉 목표를 한참 밑도는 쪽으로 실패한다 —
    #   위쪽만 보던 tol 은 그것을 절대 못 잡고 'operating_stack_pressure' 도장을 찍어줬다.
    chk('provenance: mild relaxation below target (hold arm) is still fine',
        stage_pressure_role(True, 0.085, 0.09) == 'operating_stack_pressure')
    chk('provenance: a RUNAWAY unload (platen off the bed, p≈0) is tagged OVER_UNLOADED',
        stage_pressure_role(True, 0.001, 0.09) == 'operating_stack_pressure_OVER_UNLOADED'
        and stage_pressure_role(True, 0.054, 0.09) == 'operating_stack_pressure_OVER_UNLOADED')
    chk('provenance: fabrication runs are never tagged',
        stage_pressure_role(False, 0.31, 0.30) == 'fabrication_pressure'
        and stage_pressure_role(False, 0.001, 0.30) == 'fabrication_pressure')

    #    E2. UNLOAD acceptance is TWO-SIDED and the search can recover from an overshoot.
    chk('unload: p far ABOVE target → keep unloading',
        unload_verdict(1.18, 0.09) == 'above')
    chk('unload: p inside ±10 % → accept',
        unload_verdict(0.09, 0.09) == 'in_band' and unload_verdict(0.0955, 0.09) == 'in_band'
        and unload_verdict(0.0845, 0.09) == 'in_band')
    chk('unload: ★ platen clear of the bed (p≈0) is REJECTED (the old test accepted it)',
        unload_verdict(0.0, 0.09) == 'below' and unload_verdict(0.001, 0.09) == 'below')
    chk('unload: the old one-sided rule would have accepted p=0 — regression pin',
        (0.0 <= 1.02 * 0.09) and unload_verdict(0.0, 0.09) != 'in_band')
    chk('unload: band is configurable', unload_verdict(0.08, 0.09, band=0.30) == 'in_band')
    # search geometry: rise while unbracketed, bisect once bracketed, never below the restart height
    _zn, _k = unload_next_z(0.60, 0.60, None, 0.90, 0.01)
    chk('unload: unbracketed → rise by the step', _k == 'rise' and abs(_zn - 0.61) < 1e-12)
    chk('unload: rise is capped at WALL0 (out of travel)',
        unload_next_z(0.895, 0.60, None, 0.90, 0.01)[0] == 0.90)
    _zn2, _k2 = unload_next_z(0.70, 0.60, 0.70, 0.90, 0.01)
    chk('unload: bracketed → BISECT back DOWN toward the target (old loop could only rise)',
        _k2 == 'bisect' and abs(_zn2 - 0.65) < 1e-12 and _zn2 < 0.70)
    chk('unload: bisection never descends below the restart height (no new plastic compaction)',
        unload_next_z(0.62, 0.60, 0.62, 0.90, 0.01, floor_z=0.615)[0] == 0.615)
    # ── STIFFNESS SWEEP: the real defect only appears when the elastic unload branch is stiff
    #    relative to the platen step, which is exactly the production geometry (fabrication 1.2 GPa,
    #    operating 0.09 GPa, vmax-sized steps).  p(z) = p_fab·exp(−k·Δz) with k from gentle to stiff.
    #    NEW search must stay in band at EVERY stiffness; the OLD rise-only loop must fall apart as k
    #    grows — that divergence IS the bug, so it is pinned rather than described.
    _TGT, _VMAX, _Z0 = 0.09, 0.002, 0.600

    def _mk_branch(k):
        return lambda z: max(0.0, 1.20 * float(np.exp(-k * (z - _Z0))))

    def _run_new(pz):
        lo, hi, z = _Z0, None, _Z0
        for i in range(40):
            z, _ = unload_next_z(z, lo, hi, 0.90, 0.05 * _VMAX * (1.6 ** min(i, 8)), floor_z=_Z0)
            v = unload_verdict(pz(z), _TGT)
            if v == 'in_band':
                return pz(z)
            if v == 'above':
                lo = max(lo, z)
            else:
                hi = z if hi is None else min(hi, z)
        return None

    def _run_old(pz):                       # the pre-2026-07-28 loop, verbatim in behaviour
        z = _Z0
        for _ in range(40):
            p = pz(z)
            if p <= 1.02 * _TGT:            # one-sided accept: fires wherever it happens to land
                return p
            z += _VMAX if p > 1.5 * _TGT else 0.12 * _VMAX
        return None

    _new_ok, _old_worst = True, 1.0
    for _k in (260.0, 800.0, 2000.0, 4000.0):
        _pz = _mk_branch(_k)
        _pn = _run_new(_pz)
        _new_ok &= (_pn is not None and unload_verdict(_pn, _TGT) == 'in_band')
        _po = _run_old(_pz)
        _old_worst = min(_old_worst, (_po / _TGT) if _po is not None else 1.0)
    chk('unload: bracketing search stays in band across the whole stiffness sweep (k=260…4000)',
        _new_ok)
    chk('unload: ★ the OLD rise-only loop collapses to <5 % of target on a stiff branch '
        '(platen clear of the bed) — the documented runaway',
        _old_worst < 0.05)

    #    E3. the unload TRIGGER uses the same band as the acceptance test.
    chk('unload trigger: a bed already inside the band is left alone (nothing to unload)',
        restart_unload_needed([0.0947], 0.09) is False          # 5 % over = in band  ← real trace
        and restart_unload_needed([0.099], 0.09) is False)
    chk('unload trigger: genuinely over-pressure still unloads',
        restart_unload_needed([0.30], 0.09) is True
        and restart_unload_needed([0.101], 0.09) is True)       # >10 % over
    chk('unload trigger: ★ the old bare `> target` disturbed an in-band bed — regression pin',
        (0.0947 > 0.09) and restart_unload_needed([0.0947], 0.09) is False)

    #    E4. a settle window that is still ringing must be REFUSED, not searched.
    chk('settle: a flat at-rest window is quasi-static',
        settle_is_quasistatic([0.0900, 0.0902, 0.0899])[0] is True)
    chk('settle: ★ the real ringing trace is caught (p ROSE while the platen rose)',
        settle_is_quasistatic([0.1371, 0.1785, 0.2642, 0.3028])[0] is False)
    chk('settle: a sign-flipping (negative reaction) window is caught',
        settle_is_quasistatic([0.1960, -0.0541, 0.1037])[0] is False)
    # ★ 2026-07-29 정정: 이 자리의 옛 단언("샘플 부족 → 실패 아님, CLI 가드가 <1 담당")이
    #   바로 S-3 구멍을 못박고 있었다 — --restart-settle 1|2 면 창 길이가 2 라 적응형 정착
    #   전체가 no-op 인데 provenance 는 'settle_quasistatic: true, spread 0.0' 을 적었다.
    chk('settle: ★ 샘플 부족은 "정지 미증명"이다 (옛 단언이 이 구멍을 고정하고 있었다)',
        settle_is_quasistatic([0.09])[0] is False and settle_is_quasistatic([])[0] is False
        and settle_is_quasistatic([0.1371, 0.3028])[0] is False)   # 121% 튀는 2점 창
    chk('settle: 창 전체 진폭을 본다 — 링잉의 마루 위상이 통과하지 못한다',
        settle_is_quasistatic([1.0, 2.0, 1.0, 2.0, 1.899, 2.000, 1.899])[0] is False)
    chk('settle: 단조 붕괴 중인 창은 스프레드가 작아도 거부 (추세 항)',
        settle_is_quasistatic([0.100, 0.093, 0.087])[0] is False
        and settle_is_quasistatic([1.0 * 0.93 ** i for i in range(30)])[0] is False)
    chk('settle: near-zero windows use the absolute floor, not a blown-up relative spread',
        settle_is_quasistatic([1e-9, 2e-9, 1.5e-9])[0] is True)

    #    F. CLI guard: --restart-settle < 1 with --load-state must be refused, not clamped.
    for _bad_settle in (0, -1):
        try:
            main(['--load-state', 'x.npz', '--restart-settle', str(_bad_settle)])
            _ok = False
        except SystemExit as _e:
            _ok = 'restart-settle' in str(_e)
        except Exception:
            _ok = False
        chk(f'--restart-settle {_bad_settle} with --load-state is refused', _ok)

    print(f"selftest: {ok}/{ok + len(fail)} PASS" + (f"   FAILED: {fail}" if fail else ""))
    return 1 if fail else 0


def main(argv):
    args = parse_args(argv)
    if args.selftest:                                          # numpy-only; must run without taichi
        raise SystemExit(_selftest())
    if args.load_state and args.restart_settle < 3:
        # Hard refusal, not a clamp: with no settle window the unload/compact decision is taken on frame 0,
        # where v and C have just been zeroed and the platen reaction still reads ≈0 — so an UNLOAD request
        # would be read as "not in contact yet" and the platen would be driven DOWN into an already-
        # fabricated bed (plastic, irreversible).  That is precisely the failure this window removes.
        raise SystemExit('[load-state] --restart-settle must be ≥ 3 (given '
                         f'{args.restart_settle}).  The restart zeroes v/C, so the platen reaction needs a '
                         'few frozen frames to rebuild from F; deciding "unload or compact?" on frame 0 '
                         'silently compacts an already-fabricated bed.  ★2026-07-29 (S-3): the floor is '
                         'now 3, not 1 — settle_is_quasistatic needs ≥3 samples to judge at-rest, so a '
                         'window of 1-2 made the whole adaptive-settle layer a no-op while still writing '
                         '"settle_quasistatic: true, spread 0.0" into the provenance.')
    if args.load_state and args.compact_to <= 0:
        # ★ FRAME BUDGET.  Each unload probe costs a full frozen settle window plus the move frame, so
        #   the search needs roughly settle × probes frames.  A real run hit exactly this: --frames 400
        #   with --restart-settle 30 bought only 11 of the 40 probes, and the search — which was
        #   converging cleanly (0.1364→0.0830 monotone, final 1.01× target) — ran out of frames rather
        #   than out of ideas.  That is now a not_converged failure, so warn BEFORE spending the run.
        _np = max(1, args.unload_max_probes)
        _need = (args.restart_settle + 1) * _np + args.restart_settle          # every probe settles in the MINIMUM
        _need_max = (max(args.restart_settle_max, args.restart_settle) + 1) * _np + args.restart_settle
        if args.frames < _need_max:
            # Report the WORST case, not just the best.  --restart-settle is a minimum and the probe
            # window extends adaptively until the bed is at rest, so quoting only the minimum-window
            # figure would give false comfort: a bed that needs the full --restart-settle-max per probe
            # costs ~{_need_max} frames, and the run then dies as not_converged_frame_budget with no
            # numbers emitted.  (Observed: --frames 400 / settle 30 bought 11 of 40 probes.)
            _verdict = ('too small' if args.frames < _need else 'enough only if every probe settles '
                        'in the MINIMUM window')
            print(f"  ⚠ [load-state] --frames {args.frames} is {_verdict} for this search: "
                  f"{_np} probes × (settle + 1 move) + {args.restart_settle} initial = "
                  f"{_need} frames at the {args.restart_settle}-frame minimum, up to {_need_max} if the "
                  f"probe window extends to --restart-settle-max {args.restart_settle_max}.  Running out "
                  f"of FRAMES mid-search ends the run as not_converged_frame_budget (no numbers emitted). "
                  f"Raise --frames toward {_need_max}, or lower --unload-max-probes.")
    if args.load_state and args.protocol == 'hold' and args.compact_to <= 0:
        print("  [load-state] --protocol hold on a restart = RIGID-FIXTURE arm: the platen first UNLOADS to "
              "--target-gpa, then is FIXED and the stress relaxes below it (constant gap).  --protocol servo "
              "= COMPLIANT-FIXTURE arm (constant stress, thickness free).  The two bracket the real jig.")
    if args.load_state and not args.save_state and args.protocol == 'servo' and args.target_gpa >= 0.25:
        print(f"  [load-state] note: --protocol servo --target-gpa {args.target_gpa} ≈ the usual FABRICATION "
              f"pressure.  For the '제작 → 제하 → 구동압' protocol pass the OPERATING stack pressure "
              f"(e.g. --target-gpa 0.09).")
    if args.fracture_scaffold and not args.am_scaffold:       # ★L1(리뷰): crack-void는 스캐폴드 경로 전용
        raise SystemExit('[fracture] --fracture-scaffold 는 --am-scaffold 필요 (crack-void는 '
                         'DEM→MPM 스캐폴드 경로에서만 동작 — 다른 경로에선 무시되므로 침묵 no-op 차단).')
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
    am_c = None; am_r = None; am_r_pristine = None                                       # (pristine radii = restart fingerprint)
    AM_vol = 0.0; am_top = 0.0; um_box = 0.0; am_jam_z = 0.0   # fixed-AM scaffold bookkeeping
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
        am_r_pristine = am_r.copy()                             # kept for the cycle-deform eviction DELTA (m2)
        am_top = float((am_c[:, 2] + am_r).max())              # ★ PRISTINE bed top → grid sizing (WALL0/nz) is
        #   N-INVARIANT (N4).  ★ NOTE (physics#2): porosity is integrated to the SETTLED platen wall_z (which
        #   physically descends = the thickness output), NOT to am_top — so what is pinned across N is the
        #   FLOOR / lateral area / grid dx·nz / initial WALL0 (discretization frame), and the moving wall_z is
        #   the real press response, not an artefact.  am_top is the grid-sizing envelope, not a porosity box.
        if args.cycle_deform:
            # ── A-1 (v1 ASSUMED-FORM): charge-state radius re-deformation.  ★ THIS FILE'S type convention is
            #    1=AM_P (poly), 2=AM_S (SC) — see the coverage loop ((1,'AM_P'),(2,'AM_S')) and the scaffold
            #    CSV header — the OPPOSITE of step3_sigma's SID_NAME.  ⚠ HANDOFF (electrochem#4): if se_dump'/
            #    the sid-tagged deformed geometry is ever routed to STEP3, REMAP sid (1↔2) — step3 reads the
            #    OPPOSITE SID_NAME, so a naive handoff SWAPS poly↔SC material (σ_e, GB, D_s).  (B-1/step4 is
            #    immune: it splits poly/SC by RADIUS ≥3.5µm, not sid.)  SC (sid=2) contracts on charge; poly
            #    (sid=1) expands its envelope via anisotropic intergranular microcracking (opposite sign),
            #    discounted by --dv-pct-poly (crack absorbs most internally).  Isotropic approx (c-axis
            #    anisotropy folded into the |ΔV| sweep-axis).  Centres FIXED → only radii (→ pin mask / SE
            #    eviction / AM_vol) change.  frame[5]=MPM re-flow; the N→ΔV law is the ledger's (A-3). ──────
            if args.cycle_dv_sc <= -1.0 or args.cycle_dv_poly * args.dv_pct_poly <= -1.0:   # (m8) guard nan radii
                raise SystemExit(f"[cycle-deform] ΔV ≤ -1 unphysical (dv_sc={args.cycle_dv_sc}, "
                                 f"dv_poly·pct={args.cycle_dv_poly * args.dv_pct_poly}) → radius (1+ΔV)^⅓ = nan")
            _sid = amraw[:, 0].astype(int)
            _fac = np.ones(len(am_r), np.float64)
            _fac[_sid == 2] = (1.0 + args.cycle_dv_sc) ** (1.0 / 3.0)                       # AM_S=SC shrink
            _fac[_sid == 1] = (1.0 + args.cycle_dv_poly * args.dv_pct_poly) ** (1.0 / 3.0)  # AM_P=poly expand (discounted)
            am_r = am_r * _fac
            _dr_sc = (1.0 + args.cycle_dv_sc) ** (1.0 / 3.0) - 1.0
            _dr_po = (1.0 + args.cycle_dv_poly * args.dv_pct_poly) ** (1.0 / 3.0) - 1.0
            print(f"  [cycle-deform] N={args.cycle_n} (v1 ASSUMED-FORM, isotropic, grid/bed-frame N-invariant):  "
                  f"AM_S/SC ΔV={args.cycle_dv_sc:+.3f} → r×{1+_dr_sc:.4f} ({_dr_sc*100:+.2f}%, {int((_sid==2).sum())} AM_S)  ·  "
                  f"AM_P/poly ΔV={args.cycle_dv_poly:+.3f}×{args.dv_pct_poly:.2f} → r×{1+_dr_po:.4f} ({_dr_po*100:+.2f}%, "
                  f"{int((_sid==1).sum())} AM_P)")
        if args.fracture_scaffold:
            # ── 취성 파괴 → MPM crack-void 게이트.  DEM Auerbach가 '어디서' 균열이 개시하는지(WHERE)를 주고,
            #    MPM이 그 형태적 결과(SE가 열린 균열공간으로 흘러듦)를 보여줌 = frame[5] 분업.  fragmentation+
            #    심각도만 게이트(microcrack=열린 부피≈0, near-null).  crack-void를 유효반경 감소로 근사
            #    (--cycle-deform과 동일한 radius-factor 규약; 정확한 fragment-split은 v2 후보).  기본 OFF. ──
            fr = np.atleast_2d(np.loadtxt(args.fracture_scaffold, delimiter=','))
            if len(fr) != len(am_r):
                raise SystemExit(f"[fracture] fracture-scaffold 행수 {len(fr)} != am_scaffold {len(am_r)} — "
                                 "행-정렬 CSV 필요 (scripts/dem_fracture_scaffold.py로 동일 순서 생성).")
            # ★M1(리뷰): 행수만으론 순서-불일치/다른-전극 CSV를 못 잡음.  fracture CSV는 cols 0-4에
            #   type,x,y,z,r 을 재수록하므로 좌표로 실제 정렬 검증 (생성기의 .6f 반올림 허용).
            if fr.shape[1] >= 5 and not np.allclose(fr[:, 1:4], amraw[:, 1:4], atol=1e-4):
                _nbad = int((np.abs(fr[:, 1:4] - amraw[:, 1:4]).max(1) > 1e-4).sum())
                raise SystemExit(f"[fracture] fracture-scaffold 좌표가 am_scaffold와 불일치 ({_nbad}행) — "
                                 "다른 전극/순서의 CSV.  같은 am_scaffold로 dem_fracture_scaffold.py 재생성.")
            _rank = fr[:, -2].astype(int)                          # worst_stage_rank 0..4
            _RANKMIN = {'microcrack': 1, 'multicrack': 2, 'fragmentation': 3, 'pulverization': 4}[args.fracture_min_stage]
            _void = np.zeros(len(am_r), np.float64)
            _void[_rank == 3] = args.fracture_void_frag           # 단계별 crack-void 부피분율 (ASSUMED-FORM)
            _void[_rank >= 4] = args.fracture_void_pulv
            _void[_rank < _RANKMIN] = 0.0                         # 심각도 게이트 (문턱 미만 무시)
            _gate = _void > 0
            if _gate.any():
                am_r = am_r * (1.0 - _void) ** (1.0 / 3.0)         # crack-void → 유효반경↓ → pin-mask↓ → SE ingress
                print(f"  [fracture-gate] {int(_gate.sum())}/{len(am_r)} AM에 crack-void 주입 "
                      f"(min-stage={args.fracture_min_stage}, ASSUMED-FORM): frag {int((_rank==3).sum())} "
                      f"pulv {int((_rank>=4).sum())} → r×(1−v)^⅓ (v_frag={args.fracture_void_frag}, "
                      f"v_pulv={args.fracture_void_pulv}).  frame[5]: DEM=WHERE, MPM=morphology.  "
                      f"⚠ 이중계산 주의 — DEM f_intact(σ 수송보정)와 별개 축(형태/공극); 두 보정 동시 적용 시 doc §guard 참조")
            else:
                print(f"  [fracture-gate] {args.fracture_min_stage}+ AM 없음 (micro/multi만 존재 = 열린 부피≈0) "
                      f"→ crack-void 미적용, near-null.  DEM 취성은 수송(f_intact)에만 반영됨.")
        AM_vol = float(np.sum((4.0 / 3.0) * np.pi * am_r ** 3))  # DEFORMED solid (density/report)
        WALL0 = am_top + 0.05; WALL_MIN = FLOOR + 0.01          # WALL0 from PRISTINE am_top → nz N-invariant
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
        pin_pristine = None                                   # (m2) PRISTINE AM mask → exact eviction DELTA
        if args.cycle_deform:                                 #   (excludes the static contact-boundary overlap
            pin_pristine = np.zeros((n_grid, n_grid, nz), bool)  #   present even in the undeformed bed)
            for _i in range(len(am_r_pristine)):
                _raster(pin_pristine, am_c[_i, 0], am_c[_i, 1], am_c[_i, 2], float(am_r_pristine[_i]), True)
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
    _cyc_evict_pct = None                                    # A-1 cycle-deform SE eviction % (honesty; None = off)
    _state_in = None                                         # restored restart state (--load-state); None = seed fresh
    _state_meta = {}                                         # its meta (fabrication provenance for the outputs)
    if args.load_state:
        # ── PLASTIC-HISTORY RESTART: skip SE seeding entirely and restore the saved material points
        #    (positions + F + the per-point material/history arrays).  The AM scaffold above was
        #    rebuilt normally, so --cycle-deform / --fracture-scaffold radii for THIS stage are already
        #    applied to am_r / pin_np — that is exactly the intent: SE keeps its 300-MPa memory while
        #    the AM breathes.  The guard therefore compares centres/count/PRISTINE radii only. ────────
        _sa, _sm = read_state_npz(args.load_state)
        _cur_meta = {'n_grid': int(n_grid), 'nz': int(nz),
                     'lateral_box': float(args.lateral_box), 'periodic': bool(PERIODIC)}
        _cur_pos = am_c if am_c is not None else np.zeros((0, 3))
        _cur_r0 = am_r_pristine if am_r_pristine is not None else np.zeros(0)
        _errs = state_guard_errors(_sm, _cur_meta, _sa.get('am_pos', np.zeros((0, 3))),
                                   _sa.get('am_r_pristine', np.zeros(0)), _cur_pos, _cur_r0)
        _miss = [k for k in _STATE_REQUIRED if k not in _sa]
        if _miss:
            _errs.append(f"state file is missing required arrays: {_miss}")
        else:
            _npts = len(_sa['x'])
            _bad = [k for k in _STATE_REQUIRED if len(_sa[k]) != _npts]
            if _bad:
                _errs.append(f"per-point arrays disagree on length (x has {_npts}): {_bad}")
            _errs += state_finite_errors({k: _sa[k] for k in _STATE_REQUIRED})
        if _errs:
            raise SystemExit("[load-state] INCOMPATIBLE state file '" + args.load_state + "':\n  - "
                             + "\n  - ".join(_errs)
                             + "\n  A restart must reuse the SAME grid + the SAME AM scaffold geometry "
                               "(only the AM RADII may change, via --cycle-deform/--fracture-scaffold).")
        _state_in = _sa; _state_meta = _sm
        n = len(_sa['x'])
        xs = np.ascontiguousarray(_sa['x'], np.float32)
        mus = np.ascontiguousarray(_sa['mu_p'], np.float32)
        las = np.ascontiguousarray(_sa['la_p'], np.float32)
        ylds = np.ascontiguousarray(_sa['yld_p'], np.float32)
        pvs = np.ascontiguousarray(_sa['pvol_p'], np.float32)
        coh_np = np.ascontiguousarray(_sa['coh_p'], np.float32)
        phase_np = (np.ascontiguousarray(_sa['phase'], np.int8) if 'phase' in _sa
                    else np.where(ylds < 100.0, 1, 0).astype(np.int8))
        fibre_np = np.ascontiguousarray(_sa['fibre'], np.int32) if 'fibre' in _sa else None
        dia_np = np.ascontiguousarray(_sa['fibre_dia'], np.float32) if 'fibre_dia' in _sa else None
        se_id_base = np.ascontiguousarray(_sa['se_id'], np.int32) if 'se_id' in _sa else None
        if am_c is not None and am_r_pristine is not None:   # fingerprint = human-readable scaffold identity
            _fp_now = state_fingerprint(am_c, am_r_pristine)   # (the AUTHORITATIVE check is the array compare
            print(f"  [load-state] AM scaffold fingerprint {_fp_now} "  # in state_guard_errors above)
                  f"(state {_sm.get('am_fingerprint')}) · {len(am_r)} AM"
                  + (f" · radii re-deformed this stage (cycle-deform/fracture) — excluded from the guard "
                     f"by design" if (args.cycle_deform or args.fracture_scaffold) else ""))
        if args.am_scaffold:                                 # seed-density bookkeeping (metrics parity)
            se_solid = float(pvs.sum())
            am_solid = float((pin_np > 0).sum()) * dx ** 3
            bed_vol = WIDTH * WIDTH * (am_top - FLOOR)
            f_am = 100.0 * am_solid / bed_vol; f_se = 100.0 * se_solid / bed_vol
            bulk_rho = (am_solid * 4800.0 + se_solid * 2000.0) / bed_vol / 1000.0
        print(f"  [load-state] restored {n:,} material points from {args.load_state}  "
              f"(fab target={_sm.get('target_gpa')} GPa protocol={_sm.get('protocol')} "
              f"wall_z={_sm.get('wall_z')} · plastic history F/Σdg/ε KEPT · v,C zeroed = quasi-static restart)")
        print(f"  [load-state] Σdg(saved) mean={float(np.mean(_sa['dg_acc'])):.4f} "
              f"max={float(np.max(_sa['dg_acc'])):.4f}   ‖F−I‖ mean="
              f"{float(np.mean(np.linalg.norm(_sa['F'].reshape(-1, 3, 3) - np.eye(3), axis=(1, 2)))):.5f} "
              f"(0 ⇒ pristine/no memory)")
        if args.se_dump or args.add_recipe:
            print("  [load-state] note: --se-dump / --se-frac / --add-recipe are IGNORED here — the SE (and any "
                  "additive) points come from the state file.  They still matter for stage ①.")
        # ★ SILENT-WRONGNESS GUARD: the per-point µ/λ/σ_y/cohesion are RESTORED FROM THE STATE, so a
        #   --e-se / --nu-se / --sigma-y / --coh given on the restart command line does NOT reach the
        #   material.  Without this warning a "temperature-softened σ_y" restart would run at the ORIGINAL
        #   σ_y and look like it worked.  (Changing the material mid-restart is not supported: the per-point
        #   values also carry the additive phases, which have their own moduli.)
        _mat_mismatch = [f"{k}: state={_sm.get(k)} cmdline={c}"
                         for k, c in (('e_se', float(args.e_se)), ('nu_se', float(args.nu_se)),
                                      ('sigma_y', float(args.sigma_y)), ('coh', float(COH)))
                         if _sm.get(k) is not None and abs(float(_sm[k]) - c) > 1e-9]
        if _mat_mismatch:
            print("  [load-state] ⚠ MATERIAL ARGS IGNORED — per-point µ/λ/σ_y/coh come from the state file, "
                  "not from this command line:\n      " + "\n      ".join(_mat_mismatch)
                  + "\n      → to change the SE material you must re-run stage ① (fabrication) with the new "
                    "values.  This run continues with the SAVED material.")
        # ★ CFL RE-CHECK against the RESTORED material.  dt was capped from the command-line --e-se/--nu-se
        #   (they are what this run's `lame()` saw), but the per-point µ/λ come from the state.  A state
        #   stiffer than this run's args ⇒ the P-wave speed exceeds what dt was sized for ⇒ silent blow-up.
        #   Only ever SHRINKS dt (never relaxes it), so a matching restart is bit-identical.
        _M_state = float(np.max(np.asarray(las, np.float64) + 2.0 * np.asarray(mus, np.float64))) if n else 0.0
        if _M_state > 0.0:
            _dt_state = 0.4 * dx / (_M_state ** 0.5)
            if _dt_state < dt:
                print(f"  [load-state] dt tightened for CFL: {dt:.3e} → {_dt_state:.3e} s — the restored "
                      f"per-point material (max λ+2µ = {_M_state:.2f} GPa) is stiffer than this run's "
                      f"--e-se/--nu-se implied.  (dt is sized from the args, the material comes from the "
                      f"state; without this the run can go unstable.)")
                dt = _dt_state
        # ★ COHESION RE-ARM (review A-4 — silent loss).  The cohesion term inside `substep` sits behind a
        #   COMPILE-TIME `ti.static(COH > 0.0)` gate built from THIS run's --coh.  coh_p IS restored from the
        #   state, but a restart that does not repeat --coh (COH=0) compiles the whole branch OUT, so a bed
        #   fabricated WITH cold-weld / PTFE-binder cohesion silently runs stage ② with NO cohesion at all —
        #   and nothing in the output says so.  Re-arm the gate from the state's own per-point values (the
        #   per-point magnitudes are unchanged; only the compile-time gate is opened).
        _coh_state_max = float(np.max(coh_np)) if len(coh_np) else 0.0
        COH, _coh_rearmed = rearm_cohesion(COH, _coh_state_max)
        if _coh_rearmed is not None:
            _coh_rearmed = round(_coh_rearmed, 6)
            print(f"  [load-state] cohesion RE-ARMED from the state (max coh_p = {_coh_state_max:.4f} GPa). "
                  f"This run passed no --coh, which would have compiled the cohesion term OUT and silently "
                  f"dropped the restored binder/cold-weld.")
        if args.am_scaffold:
            # HONESTY: the seeding path filters SE out of AM cells ONCE, at seed time.  On a restart there is
            # no re-seed, so points that the (possibly EXPANDED) AM mask now covers are NOT evicted — they are
            # pinned by am_mask instead.  We deliberately do NOT delete them: deletion would (a) destroy the
            # plastic history this feature exists to preserve and (b) break the no-change round-trip, and the
            # pristine path has the same overlap anyway once points advect during compaction (it only filters
            # at seed time).  Instead the overlap is MEASURED and reported — it is the part of solid_vol that
            # is counted both as SE (Σpvol) and as AM (AM_vol), i.e. a small porosity under-estimate.
            _ii = np.clip((xs[:, 0] * n_grid).astype(np.int64), 0, n_grid - 1)
            _jj = np.clip((xs[:, 1] * n_grid).astype(np.int64), 0, n_grid - 1)
            _kk = np.clip((xs[:, 2] * n_grid).astype(np.int64), 0, nz - 1)
            _in_am = pin_np[_ii, _jj, _kk] > 0
            _se_in_am_pct = round(100.0 * float(_in_am.sum()) / max(n, 1), 3)
            print(f"  [load-state] {int(_in_am.sum()):,}/{n:,} restored points ({_se_in_am_pct:.2f}%) lie inside "
                  f"the CURRENT AM mask → pinned, NOT evicted (plastic history preserved; that volume is "
                  f"double-counted in solid_vol ⇒ porosity biased low by ≲ this share of the SE volume).")
    elif args.am_scaffold:
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
            _se_raw_cells = int(se_pin.sum())                # SE cells before AM eviction
            _se_raw_bool = se_pin.copy() if args.cycle_deform else None   # (m2) raw SE raster for the delta
            se_pin &= (pin_np == 0)                          # SE only in non-AM cells
            sel = np.argwhere(se_pin)
            seed_str = f"{len(seraw)} real SE spheres → {len(sel):,} SE cells (REAL positions, no targeting)"
            if args.cycle_deform:
                # HONESTY (N4-F5a): a poly EXPANSION grows the AM mask into cells that held SE → those SE cells
                # are EVICTED (v1 = eviction-DELETION, not volume-conserving advection).  ★ (m2/physics#3,#4)
                # report the DEFORMATION-INDUCED delta ONLY = SE cells now inside AM that were NOT inside the
                # PRISTINE AM (pin_pristine) — this EXCLUDES the static contact-boundary overlap present even in
                # the undeformed bed (which is NOT eviction), so the flag no longer false-triggers on baseline
                # overlap.  SC shrink cannot evict (deformed AM ⊂ pristine); only poly expansion can, so the
                # value is nonzero whenever --cycle-dv-poly>0 (NOT "≈0 on charge" — the old claim was wrong).
                _evict = int((_se_raw_bool & (pin_np > 0) & (~pin_pristine)).sum())
                _evict_pct = 100.0 * _evict / max(_se_raw_cells, 1)
                _cyc_evict_pct = round(float(_evict_pct), 3)
                print(f"  [cycle-deform] SE eviction (poly-expansion, deformation-induced Δ vs pristine, excl "
                      f"static contact overlap): {_evict:,}/{_se_raw_cells:,} cells ({_evict_pct:.2f}%) DELETED — "
                      f"v1 not volume-conserving; read Δvoid with this caveat (0 only if --cycle-dv-poly=0).")
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
    if _state_in is None:                                      # (--load-state restored these already)
        phase_np = np.where(ylds < 100.0, 1, 0).astype(np.int8)  # base points: 1 SE / 0 AM(mat, mix mode)
        coh_np = np.full(len(xs), COH, np.float32)             # per-point cohesion: SE = COH (PTFE ≫ below)
        fibre_np = None                                        # set in the additive block if fibres seeded
        dia_np = None                                          # per-point relative fibre Ø (PTFE draw d∝√(V/L))
    if args.add_recipe and _state_in is not None:
        # the saved state ALREADY contains the seeded additive points (with their own µ/λ/σ_y/coh/phase) —
        # re-seeding them here would DOUBLE the additive loading and desync phase/fibre bookkeeping.
        print("  [additives] --add-recipe IGNORED under --load-state: the restored state already carries "
              "its additive points (re-seeding would double the loading).  Re-run stage ① to change the recipe.")
    elif args.add_recipe:
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
                'SWCNT':  (0.50, 0.30, 0.10, 6, 'sheath',  0.0,       0.0,  0.0, 0.0, 0.0, 0.0),   # ★A14 (#275 koo2026) conformal sheath — E/σ_y = SuperP-class SOFT PROXY §F1: the film-effective
                #   transverse modulus of a few-layer CNT skin (~2-10nm = OUR inference from tube Ø 2nm;
                #   koo2026 publishes no sheath thickness) is UN-anchored (single-tube AXIAL ~1 TPa is the
                #   wrong axis for a wrapped skin under radial press); ≤0.5wt% + add_pvs volume-pin → compaction
                #   impact negligible either way.  Role is STRUCTURAL (conductive-skin morphology → STEP3/viewer).
            }
            am_box = ((am_c - off, am_r) if am_c is not None else None)   # AM in the seed-box frame (coating)
            _se0_box = ((xs[phase_np == 1] - off) if 'SWCNT' in cnt
                        else np.zeros((0, 3), np.float32))   # ★A14: pre-additive SE cloud (seed-box frame)
            #   for the seed-time sheath↔SE trade-off — built ONLY when SWCNT is in the recipe (the
            #   boolean-index copy is ~0.5 GB at 384³; don't pay it for every additive run)
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
                    pts, _fid, _seedinfo = _ad.seed_sdcp(nobj, bx, dx, rng, am=am_box,
                                                         in_am=lambda q: _in_am_abs(q + off),
                                                         surface_frac=_sfrac, clump=_clump,
                                                         agg_d=_aggd / um_box, d=_ad.SDCP_D / um_box,
                                                         return_ids=True, return_info=True)
                    _w = np.ones(len(pts), np.float32)
                    _coated = True                            # metadata: coat dict records the anchored share
                elif kind == 'sheath':
                    # ★ A14 SURFACE_CONFORMAL (#275 koo2026): continuous vein-like SWCNT skin ON the AM
                    # surfaces (geodesic walks — additives.seed_sheath).  Distinct from A4 coat_block
                    # (isolated blocking-film points): chains are CONTIGUOUS → a connected conductive skin
                    # per AM.  Coverage wrap_frac from the process row (1.0, ζ≈−1.9 anchor) or --swcnt-wrap.
                    # Seed-time RIGID trade-off vs the pre-additive SE cloud → meta (GEOMETRIC UPPER BOUND
                    # of ionic-contact loss — additives.sheath_ion_tradeoff trust label; deformed-cloud
                    # version = payload-side future).
                    _row = _ad.additive_process(nm, args.mixing)
                    _wrap = (float(args.swcnt_wrap) if args.swcnt_wrap >= 0.0
                             else float(_row.get('wrap_frac', 1.0)))
                    pts, _fid = _ad.seed_sheath(nobj, bx, dx, rng, am=am_box,
                                                in_am=lambda q: _in_am_abs(q + off),
                                                wrap_frac=_wrap,
                                                shell_um=_ad.SWCNT_SHELL / um_box,
                                                seg_len_um=_ad.SWCNT_SEG_L / um_box,
                                                return_ids=True)
                    _w = np.ones(len(pts), np.float32)
                    _sfrac = _wrap                       # coat-meta coverage share = the wrap fraction
                    _coated = True
                    _nch = int(np.unique(_fid).size)     # TRUE chain count — must be read BEFORE the
                    #   global _gfib offset below (review finding: max()+1 after offset inflated it by
                    #   every earlier additive's object count)
                    _tro = None
                    if len(pts) and am_box is not None and len(_se0_box):
                        _sub = (_se0_box if len(_se0_box) <= 300000
                                else _se0_box[rng.choice(len(_se0_box), 300000, replace=False)])
                        #   300k subsample → SE NN spacing ~0.19µm (Tabor 0.26 band 근해상, Hertz 0.13
                        #   미해상) — 밀도 한계는 tradeoff의 n_se_used/se_nn_spacing_um/trust에 자기기술
                        _tro = _ad.sheath_ion_tradeoff(pts.astype(np.float64) * um_box,
                                                       np.asarray(am_box[0], np.float64) * um_box,
                                                       np.asarray(am_box[1], np.float64) * um_box,
                                                       _sub.astype(np.float64) * um_box,
                                                       wrap_frac=_wrap)
                elif kind == 'coat' or _proc_regime == 'coat_block':   # coat_embed RETIRED (fibres don't coat)
                    # A4 COAT REGIME: points seeded in a thin shell ON the AM surfaces — SDCP anchored film
                    # (default) or SuperP thinky dry-coat (coat_block: carbon film at the AM|SE interface;
                    # its σ_i-blocking emerges as an SE-coverage drop, Kim 2025 direction).  Film thickness
                    # is 1 voxel-ish (shell 0.2µm) vs real ~26-40nm — OVERSTATED sub-voxel reality, but the
                    # recipe VOLUME is add_pvs-pinned so porosity stays honest (same approximation class as
                    # Stage-E).  surface_frac: mixing-driven spread (handmix = patchy).
                    _row = _ad.additive_process(nm, args.mixing)          # single source: process matrix
                    _sfrac = (float(args.sdcp_surface_frac) if (code == 5 and args.sdcp_surface_frac >= 0.0)
                              else float(_row.get('surface_frac', 1.0)))    # SuperP thinky 0.70 (SDCP never routes here — kind='particle')
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
                    _coh = round(args.coh_sdcp, 4)                 #   doped/neutral γ (⚠INVALID wrong-monomer, recompute) = AM-INTERFACE →
                    _reg = 'neutral(−SO₃H)' if args.sdcp_neutral else 'doped(−SO₃⁻)'   # future boundary term + STEP3,
                    #   NOT this bulk coh — scaling bulk by the interface γ-ratio would be the same cross-
                    #   attribution the --coh-sdcp help forbids for the 10× inflation.
                else:
                    _coh, _cap, _reg = 0.0, 0.0, '—'
                coh_np = np.concatenate([coh_np, np.full(len(pts), _coh, np.float32)])
                _bind = (f" binder_cap={_cap:.2f} [{_reg}] (opt {args.binder_opt_wt}wt%)" if code == 4 else "")
                _bind += f" regime={_proc_regime}" + ("  (A4 coat-seeded)" if _coated else
                                                       "  (A4: coat seeding TBD → bulk)" if _proc_regime != 'bulk' else "")
                # ★MED-1(감사 정직수정): SuperP recipe n = 응집체(aggregate)수이나 seed_carbon_black은 k개
                #   응집체를 하나의 agglomerate-chain으로 뭉쳐 ~n/k chain 시딩(docstring "loosely grouping into
                #   µm agglomerates" = 물리적).  n_objects=recipe n 보고는 chain 수를 k× 과대 → 실제 시딩 chain
                #   수(_fid 고유수)로 정직 보고.  seeding·부피·σ 전부 불변(라벨만 정정, VGCF는 nobj 그대로).
                _cb = (kind == 'cblack' and not _coated)
                # ⚠ _fid 는 line 1059 에서 전역 오프셋(_gfib) 됨 → max()+1 은 이전 첨가제 개수만큼 부풀음
                #   (VGCF+SuperP 조합서 오작동, 코드리뷰 HIGH).  unique().size 는 오프셋-불변 = 실제 chain 수.
                _n_obj_rep = int(np.unique(_fid).size) if (_cb and len(_fid)) else int(nobj)
                print(f"  [additives] {nm}: {_n_obj_rep} {'agglom-chains' if _cb else 'objects'} "
                      f"({cnt[nm]['wt_pct']}wt% = {cnt[nm]['vol_pct_of_solid']}vol% of solid) → {len(pts):,} pts "
                      f"(E={E} σ_y={sy} coh={_coh}, phase {code}){_bind}")
                _add_meta[nm] = {                            # → mpm_metrics['additives'][nm] → 요약
                    'wt_pct': float(cnt[nm]['wt_pct']), 'vol_pct_of_solid': float(cnt[nm]['vol_pct_of_solid']),
                    'vol_um3': round(float(cnt[nm]['vol_um3']), 2), 'n_objects': int(_n_obj_rep), 'n_points': int(len(pts)),
                    'E_GPa': float(E), 'sigma_y_GPa': float(sy), 'phase_code': int(code),
                    'mixing': args.mixing, 'mixing_regime': _proc_regime,   # NAME + regime: ballmill & handmix BOTH regime='bulk' → the NAME is what tells them apart (regime alone can't)
                }
                if kind == 'cblack' and not _coated:         # CB_MIX params — only when seed_carbon_black RAN
                    _cbm = _ad.CB_MIX.get(args.mixing, {})   # (a coat-routed SuperP-thinky run must not claim
                    _add_meta[nm]['n_recipe_aggregates'] = int(nobj)   # ★MED-1: recipe 0.2µm 응집체수 (n_objects는
                    _add_meta[nm]['obj_kind'] = 'agglom_chain'         #   그 k개가 뭉친 실제 chain 수 = 정직 대표값)
                    if _cbm:                                 # CB-chain morphology it didn't seed)
                        _add_meta[nm]['cb_mix'] = {_k: _cbm[_k] for _k in ('k', 'surface_frac', 'step', 'clump') if _k in _cbm}
                if _coated:                                  # A4 coat: record what ACTUALLY seeded
                    _add_meta[nm]['coat'] = {'shell_um': (_ad.SDCP_D / 2 if kind == 'particle'
                                                          else _ad.SWCNT_SHELL if kind == 'sheath'
                                                          else _ad.SDCP_SHELL),
                                             'surface_frac': round(float(_sfrac), 3)}   # particle: anchored shell = particle radius
                if kind == 'sheath':                         # ★ A14 sheath meta (+ trade-off if computed)
                    _add_meta[nm]['sheath'] = {'wrap_frac': round(float(_wrap), 3),
                                               'shell_um': _ad.SWCNT_SHELL,
                                               'n_chains': _nch,
                                               'morph': _row.get('morph', '')}
                    if _tro:
                        _add_meta[nm]['sheath_tradeoff'] = _tro
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
                    _add_meta[nm]['agg_d_um'] = round(float(_aggd), 2)           # 0 = milled S3 singles
                    _add_meta[nm]['seeding'] = _seedinfo                         # REALIZED counts/shares — read
                    #   realized_anchor_frac (NOT surface_frac: drops are population-asymmetric) + survival
                    #   (add_pvs re-pins volume over survivors → realized agg density = pack/survival).
                    if _aggd > 0.0:                                              # S2 as-made agglomerate mode
                        _add_meta[nm]['n_per_agglomerate'] = int(_seedinfo.get('n_agg_design', 0))
                        _add_meta[nm]['agg_pack_assumed'] = float(_ad.SDCP_AGG_PACK)   # §F1 hook — S2 anchors SIZE only
                        _add_meta[nm]['agg_mechanics'] = 'primary_E_anchor_assembly_uncalibrated'
                        #   E=23.6 GPa is the PRIMARY's AFM anchor; agglomerate-scale inter-primary bonding
                        #   is represented only by the un-calibrated bulk coh_sdcp hook (§F1)
                    else:                                                        # clump active only in singles mode
                        _add_meta[nm]['clump'] = int(_clump)                     # (agg_d wins over clump by design)
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
    _rod_rest_source = None
    if FIBRE_ROD:
        _pv, _nx, _rl, _b0, _isr = build_rod_topology(fibre_np, phase_np, xs)
        _kf = np.where(phase_np == 2, 1.0, np.where(phase_np == 4, 0.2, 0.0)).astype(np.float32)  # VGCF stiff, PTFE 0.2×
        _rod_rest_source = 'seeded_this_run'
        if _state_in is not None:
            # ★ ROD REST-STATE (review A-7).  build_rod_topology derives the rest length rl and the rest
            #   curvature b0 FROM THE POSITIONS IT IS GIVEN.  On a restart `xs` is the COMPRESSED bed, so a
            #   fibre that buckled during fabrication would adopt its buckled shape as its stress-free rest
            #   shape — the elastic energy stored by the press would be erased and the rod would never push
            #   back.  The state carries the ORIGINAL (as-seeded) rest arrays; restore them.  Topology
            #   (prev/next/is_rod) is index-based and the points are restored in the same order, so the
            #   rebuilt connectivity is identical — only rl/b0 must come from the state.
            _rl, _b0, _rod_rest_source = pick_rod_rest(_state_in, n, _rl, _b0)
            if _rod_rest_source == 'restored_from_state':
                print('  [fibre-rod] rest length/curvature RESTORED from the state (not re-derived from the '
                      'compressed positions) — the fabrication buckling stays elastic, not stress-free.')
            else:
                print('  ⚠ [fibre-rod] the state file carries NO rod rest arrays (written by an older run, or '
                      'stage ① ran without --fibre-rod): rest length/curvature are RE-DERIVED from the '
                      'COMPRESSED positions, i.e. the buckled shape becomes the stress-free shape and the '
                      'stored bending energy is LOST.  Re-run stage ① with --fibre-rod to fix; recorded as '
                      'rod_rest_source in the metrics.')
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
    _state_wall_z = None
    if _state_in is not None:
        # ── restore the PLASTIC + ELASTIC history.  `load` has just set F=I / v=0 / C=0; F, Σdg and ε are
        #    overwritten from the state file.  v and C are LEFT AT ZERO on purpose (see the STATE_SCHEMA
        #    note at the top): stage ① ends relaxed under the platen, and re-injecting a stale velocity /
        #    APIC-affine field across a protocol + target-stress change would add spurious kinetic energy.
        #    All of the stress that matters is already encoded in F. ─────────────────────────────────────
        F.from_numpy(np.ascontiguousarray(_state_in['F'], np.float32).reshape(n, 3, 3))
        dg_acc.from_numpy(np.ascontiguousarray(_state_in['dg_acc'], np.float32))
        eps_acc.from_numpy(np.ascontiguousarray(_state_in['eps_acc'], np.float32))
        _sm_wall = _state_meta.get('wall_z')
        if _sm_wall is not None:
            # continue from the SAVED platen height, not WALL0 — otherwise the platen would be lifted back
            # to the loose-bed start and the run would re-compact from scratch (= the very thing this
            # feature exists to avoid).  Clamped into this run's legal travel.
            _state_wall_z = float(min(WALL0, max(WALL_MIN, float(_sm_wall))))
            wall_z[None] = _state_wall_z
            print(f"  [load-state] platen resumed at wall_z={_state_wall_z:.4f} "
                  f"(saved {float(_sm_wall):.4f}; travel [{WALL_MIN:.3f}, {WALL0:.3f}])")
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
    # ★ conv 의 **단위**가 servo 경로에 따라 다르다 (2026-07-29 S-1 후속):
    #   legacy = 프레임당 1 (밴드 안 프레임 12개) / 정지-판독 = **프로브당 1** (각 프로브가
    #   최소 --restart-settle 프레임 + 이동을 먹는다).  같은 12 를 쓰면 프레임 기준으로 4배
    #   이상 엄격해져 멀쩡히 수렴한 런이 예산 초과로 죽는다 — 임계값을 단위에 맞춘다.
    SERVO_HOLD = 3                     # 정지-판독 경로: 밴드 안 프로브 3연속 (UNLOAD_HOLD 와 대칭)
    reach_cnt = 0; STOP_HOLD = 3            # loose→dense mix: need target SUSTAINED this many frames to stop
    # ── RESTART UNLOAD (제하) — the missing half of "fabricate at 300 MPa → unload → cycle at 90 MPa".
    #    Before this, a --load-state run at a LOWER target could only ever push the platen DOWN:
    #      • scaffold path   : descend=(p+am_skel<target) is False on frame 0 → 'reached' immediately at the
    #                          FABRICATION height → --protocol hold then froze the platen there and reported
    #                          the fabrication geometry under an "operating pressure" label (silent no-op);
    #      • non-scaffold    : the arm-after-compaction guard (por>por0−5) is re-armed on the RESTART
    #                          porosity, so it forced a further 5 %p descent regardless of the stress —
    #                          an UNLOAD request produced EXTRA plastic compaction.
    #    Now a restart first freezes the platen for --restart-settle frames (v,C are zeroed on load, so the
    #    platen reaction has to rebuild from F; frame 0 reads ≈0 and would be mistaken for "not yet in
    #    contact"), then decides ONCE: p_settle > target → UNLOAD (platen rises until the reaction drops to
    #    the target); otherwise the normal descend logic runs.  servo then equilibrates AT the target
    #    (compliant fixture: constant stress, thickness free); hold FIXES the platen at the unloaded height
    #    and lets the stress relax (rigid fixture: constant gap, stress free) — the two-arm bracket.
    _RESTART = bool(args.load_state) and args.compact_to <= 0    # --compact-to is displacement-driven by design
    _settle = max(0, int(args.restart_settle)) if _RESTART else 0
    _unload = False
    _unload_status = ('not_a_restart' if not args.load_state
                      else ('disabled_by_compact_to' if args.compact_to > 0 else 'pending'))
    _p_settle = []; _p_tail = []
    _probe_left = 0; _unload_cnt = 0
    UNLOAD_HOLD = 3          # at-rest probes IN BAND required to call the unload done (cf. STOP_HOLD)
    _wall_z_start = float(wall_z[None])
    # ── unload bracketing search state (2026-07-28 HIGH-a) ────────────────────────────────────
    # z_lo = highest platen height that still read ABOVE the band (starts at the restart height,
    # which by construction carries the fabrication pressure); z_hi = lowest height that read BELOW
    # it (None until the target is bracketed).  The old loop kept neither and could only rise.
    _z_lo = float(wall_z[None]); _z_hi = None
    _settle_quasistatic = None; _settle_spread_rel = None
    _probe_win = []; _probe_extended = False; _probe_win_max = 0
    _restart_floor_hit = False
    # ── S-1 servo 정지-판독 상태 (제하 프로브와 같은 구조) ──────────────────────────────
    _srv_left = 0; _srv_win = []; _srv_probes = 0; _srv_spread = None
    _srv_settle = max(1, int(args.restart_settle))       # 최소 창 = 제하와 같은 노브
    _settle_max_srv = max(int(args.restart_settle_max), _srv_settle)
    # --restart-settle is the MINIMUM window; _settle_max caps the adaptive extension so a bed that
    # never settles fails loudly instead of burning the whole frame budget in one probe.
    _settle_max = max(int(args.restart_settle_max), int(args.restart_settle)) if _RESTART else 0
    _unload_probes = 0
    _UNLOAD_GROW = 1.6                       # geometric rise growth while hunting for the bracket
    _UNLOAD_DZ_MIN = 0.02 / max(n_grid, 1)   # bracket narrower than 1/50 cell → refining is meaningless
    _unload_step0 = 0.05 * vmax              # START SMALL — the elastic unload branch is stiff
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
        _p_tail.append(p)
        if len(_p_tail) > 5:
            _p_tail.pop(0)
        # servo platen to target σzz (descend until target, then fine bidirectional).
        # arm-after-compaction guard: a big rigid AM (preset/mix, AM = MATERIAL) hitting the
        # platen on first contact spikes wallP transiently → refuse to stop until the bed has
        # actually compacted (por ≤ por0 − 5 %p).  The scaffold (AM = fixed grid mask) has NO
        # such transient, and the guard there forces a 5 %p over-descent regardless of stress,
        # which OVER-COMPRESSES dense (high se_frac) beds → disable it for the scaffold.
        if _RESTART and frame < _settle:
            # restart settle window: platen FROZEN while the stress rebuilds from F (v,C were zeroed).
            _p_settle.append(p); wall_vel[None] = 0.0
        elif not reached:
            step = vmax
            if _RESTART and _unload_status == 'pending':
                # ONE-TIME decision, taken on the MAX of the settle window.  Biased toward unloading on
                # purpose: an unnecessary rise is elastic and the servo band puts it back, an unnecessary
                # descent is PLASTIC and irreversible (that asymmetry is the whole bug being fixed).
                _p0 = max(_p_settle) if _p_settle else p
                _unload = restart_unload_needed(_p_settle or [p], target, args.unload_band)
                _unload_status = 'unloading' if _unload else 'not_needed_p_within_band'
                # ★ Is the window actually at rest?  If not, EVERY later probe reading is transient
                #   too, so the search is bisecting on noise — refuse up front and name the real cause
                #   instead of failing 15 probes later as "bracket collapsed".
                _qs_ok, _qs_spread = settle_is_quasistatic(_p_settle, rel_tol=args.unload_band / 3.0)
                _settle_quasistatic = bool(_qs_ok)
                _settle_spread_rel = float(_qs_spread)
                if not args.quiet:
                    print(f"  [restart] settle({_settle} frames): p={_p0:.4f} GPa vs target={target:.4f} "
                          f"(band ±{args.unload_band:.0%}), tail spread {_qs_spread * 100:.0f}% → "
                          + ("UNLOAD (제하): platen RISES until the reaction drops into the band"
                             if _unload else
                             "no unload needed (already inside the band) → normal descend logic"))
                if _unload and not _qs_ok and not args.allow_unconverged_unload:
                    raise SystemExit(
                        f"\n[restart] SETTLE WINDOW IS NOT QUASI-STATIC — 제하를 시작하지 않고 중단합니다.\n"
                        f"  --restart-settle {args.restart_settle} 프레임 창의 마지막 3점이 "
                        f"{_qs_spread * 100:.0f}% 로 흔들립니다 (허용 15%).  최근 값: "
                        f"{', '.join(f'{v:.4f}' for v in _p_settle[-5:])} GPa\n"
                        f"  --load-state 는 v·C 를 0 으로 두므로 응력이 F 로부터 재구축돼야 하는데, 창이 "
                        f"짧으면 그 값은 접촉응력이 아니라 **탄성파 과도응답**입니다.\n"
                        f"  그 위에서 제하 탐색을 돌리면 p(z) 가 단조롭지 않아(플래튼이 올라가는데 p 가 "
                        f"커지는 구간이 생김) 어떤 알고리즘도 수렴할 수 없습니다.\n"
                        f"  → --restart-settle 을 크게(예: 20–50) 주어 창이 정지 상태에 도달하게 하세요.\n"
                        f"  → 의도적인 실험이면 --allow-unconverged-unload 로 강행할 수 있습니다.")
            if _unload:
                # ── UNLOAD = rise · PROBE · rise · PROBE …  The stop test MUST be read on a frozen
                #    platen: wallf = Σ m·(v_grid − v_wall), so while the platen rises the v_wall term
                #    biases the reaction LOW by ~the same order as the signal (measured: a mid-rise frame
                #    read −0.23 GPa on a bed that was really at +0.19).  Testing on a moving frame ends
                #    the unload after a single step and leaves the bed at the fabrication pressure with
                #    an "unloaded" label — the exact class of silent no-op this fix exists to remove.
                #    UNLOAD_HOLD consecutive at-rest probes below the target are required (mirror of the
                #    descend side's STOP_HOLD sustained criterion, which exists for the same noise reason).
                if _probe_left > 0:
                    # PROBE window: platen frozen so the post-move rebound transient decays; the LAST
                    # frame of the window is the reading (same convention as the initial settle
                    # decision).  One frozen frame is not enough — the material still carries the
                    # velocity it picked up from the move.
                    #
                    # ★ ADAPTIVE (2026-07-28).  --restart-settle is now a MINIMUM, not the whole window:
                    #   when it closes we ask settle_is_quasistatic() whether the bed is actually at rest
                    #   and keep waiting if it is not, up to --restart-settle-max.  Measured at n_grid=64:
                    #   3 frames → tail spread ~100 %, p(z) NON-monotone (the reaction rose while the
                    #   platen rose) and p under-read by ~2× (0.0947 vs the true 0.1781); 30 frames →
                    #   spread 4 % and p(z) cleanly monotone 0.1364→0.0830.  A fixed frame count cannot
                    #   be right for both, because the settling time scales with the wave transit time
                    #   (∝ n_grid) — so we wait for the CONDITION, not a guessed count.
                    wall_vel[None] = 0.0
                    _probe_left -= 1
                    _probe_win.append(float(p))
                    descend = None                                       # platen stays put during the probe
                    if _probe_left == 0:
                        _qs_ok, _qs_spread = settle_is_quasistatic(_probe_win, rel_tol=args.unload_band / 3.0)
                        if not _qs_ok and len(_probe_win) < _settle_max:
                            _probe_left = max(1, _settle // 2)           # not at rest yet → keep waiting
                            _probe_extended = True
                        elif not _qs_ok:
                            _unload_status = 'not_converged_probe_not_at_rest'
                            _settle_quasistatic = False
                            _settle_spread_rel = float(_qs_spread)
                            descend = False
                    if _probe_left == 0 and _unload_status == 'unloading':  # window closed AND at rest
                        _probe_win_max = max(_probe_win_max, len(_probe_win))
                        _probe_win = []
                        _verdict = unload_verdict(p, target, args.unload_band)
                        _unload_probes += 1
                        # BRACKET update.  z_lo = highest height still reading ABOVE the band;
                        # z_hi = lowest height reading BELOW it.  Once both exist the target height is
                        # bracketed and the search bisects instead of only rising (the old loop could
                        # only rise, so a single overshoot was unrecoverable and it "converged" there).
                        if _verdict == 'above':
                            _z_lo = max(_z_lo, float(wall_z[None])); _unload_cnt = 0
                        elif _verdict == 'below':
                            _z_hi = (float(wall_z[None]) if _z_hi is None
                                     else min(_z_hi, float(wall_z[None]))); _unload_cnt = 0
                        else:
                            _unload_cnt += 1
                        if not args.quiet:
                            print(f"    [unload probe {_unload_probes}/{args.unload_max_probes}] "
                                  f"wall_z={wall_z[None]:.5f} {args.readout}={p:.4f} vs {target:.4f} GPa "
                                  f"→ {_verdict}  bracket=[{_z_lo:.5f},"
                                  f"{'None' if _z_hi is None else f'{_z_hi:.5f}'}]  in_band×{_unload_cnt}")
                        if _unload_cnt >= UNLOAD_HOLD:
                            _unload_status = 'completed'; descend = False   # tail below sets reached=True
                            if not args.quiet:
                                print(f"  ✓ [restart] unloaded: {UNLOAD_HOLD} consecutive at-rest probes "
                                      f"(each after {_settle} frozen frames) inside ±{args.unload_band:.0%} "
                                      f"of target, {args.readout}={p:.4f} vs {target:.4f} GPa, "
                                      f"wall_z={wall_z[None]:.4f} (from {_wall_z_start:.4f}), "
                                      f"porosity={por:.2f}%")
                        elif _unload_probes >= args.unload_max_probes:
                            _unload_status = 'not_converged_probe_budget'; descend = False
                        elif _z_hi is not None and (_z_hi - _z_lo) <= _UNLOAD_DZ_MIN:
                            # The bracket collapsed without ever landing in the band → p(wall_z) steps
                            # across the band discontinuously at this resolution.  Refining further is
                            # meaningless; say so rather than accepting whichever side we are on.
                            _unload_status = 'not_converged_bracket_collapsed'; descend = False
                elif wall_z[None] >= WALL0 - 1e-9 and _z_hi is None:
                    _unload_status = 'out_of_travel'; descend = False
                    print(f"  ⚠ [restart] unload ran out of platen travel at WALL0={WALL0:.4f} with "
                          f"{args.readout}={p:.4f} GPa still above target {target:.4f} — the bed did NOT "
                          f"reach the requested pressure (recorded in state_provenance.unload_status).")
                else:
                    # RISE (not yet bracketed) or BISECT (bracketed).  The rise step is now geometric and
                    # starts SMALL: the unload branch is elastic and therefore stiff, so the old
                    # `vmax while p > 1.5*target` took the bed from the fabrication pressure to zero
                    # contact in one move and never saw the target on the way past.
                    _step = _unload_step0 * (_UNLOAD_GROW ** min(_unload_probes, 8))
                    _z_next, _kind = unload_next_z(float(wall_z[None]), _z_lo, _z_hi, WALL0, _step,
                                                   floor_z=_wall_z_start)
                    _dz = _z_next - float(wall_z[None])
                    wall_z[None] = _z_next
                    wall_vel[None] = _dz / (args.sub * dt)
                    _probe_left = max(1, _settle)                        # then freeze and read it at rest
                    descend = None                                       # platen already moved
            elif args.compact_to > 0:                        # displacement-driven → descend to a target porosity
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
                # ★ 2026-08-04 — 지속-요구(STOP_HOLD)를 scaffold 분기에도 건다.  여기는 `p >= target` 의
                #   **순간** 비교라 첫-접촉 동적 스파이크 1프레임이면 플래튼이 그 자리에서 얼어붙었다.
                #   아래 non-scaffold 분기는 정확히 같은 이유로 이미 STOP_HOLD 연속 프레임을 요구한다
                #   ("a big rigid AM hitting the platen spikes wallP for ~1 frame") — scaffold 만 무방비였다.
                #   실측 (P:S 5킷, 2026-08-04): 하강이 **정확히 4·4·4·4·3 프레임**에서 멎어
                #   스트로크/초기두께 = N×0.008 (0.03198/0.03204/0.03203/0.03200/0.02405) — 정수 프레임 =
                #   운동학적 정지이지 응력 평형이 아니다.  정지 후 wallP 는 목표의 1/20~1/100 로 이완했고
                #   (프레임5 에 −0.049 GPa = 플래튼 인장 = 반동), porosity 서열은 frame 0 것이 그대로 남아
                #   소성이 서열을 시험하지 못했다.  hard_floor/am_jam 은 기하학적 정지라 즉시 적용 유지.
                reach_cnt = reach_cnt + 1 if (p + am_skel >= target) else 0
                descend = (reach_cnt < STOP_HOLD) and not hard_floor and not am_jam
            else:
                # loose→dense mix: a big rigid AM hitting the platen spikes wallP for ~1 frame, which
                # froze the platen in the loose state (premature stop → slow crawl).  Keep descending
                # at full vmax until the bed SUSTAINS ≥ target for STOP_HOLD frames (after por≤por0−5);
                # if it never sustains, the continuum SE is over-flowing (no granular jam) and it
                # descends to WALL_MIN — itself an informative result (porosity→~0 = over-compaction).
                # ★ NOT on a restart (review A-2/A-3): por0 is then the ALREADY-COMPACTED porosity, so the
                #   guard would demand another 5 %p of descent with no stress justification — turning an
                #   unload request into extra plastic compaction.  A restarted bed is in contact with the
                #   platen from frame 0 and has no loose-bed first-contact transient to guard against.
                guard = arm_guard_active(por, por0, args.load_state)
                reach_cnt = reach_cnt + 1 if (p >= target and not guard) else 0
                descend = reach_cnt < STOP_HOLD
            if descend is None:
                pass                                         # --load-state unload: platen already moved UP
            elif descend:
                # ★ S-2 (2026-07-29 적대리뷰 CONFIRMED — 이번 라운드가 만든 회귀): 밴드 확대가
                #   (1.00, 1.10]×target 구간을 제하(상승)에서 **이 하강 분기로** 옮겼다.  정착값이
                #   0.0947 vs 목표 0.0900(=+5%, 밴드 안)이면 restart_unload_needed 는 이제 False 를
                #   주고, non-scaffold 런은 여기로 떨어져 `reach_cnt` 램프 동안 2프레임을 **하강**한다
                #   (0.016 box — 실측 제하 총 스트로크 0.0091 보다 크다).  이미 제작된 베드에 붙는
                #   **신규 소성 압축**이고, 산출은 'descended_compacted' + 깨끗한 도장이 된다.
                #   restart_unload_needed docstring 자신이 경계한 바로 그 방향이다.
                #   → 재시작에서는 제작 높이(_wall_z_start) 아래로 내려가지 못하게 바닥을 건다.
                _floor_z = max(WALL_MIN, _wall_z_start) if _RESTART else WALL_MIN
                _z_next = max(_floor_z, wall_z[None] - step)
                if _z_next >= wall_z[None] - 1e-12 and _RESTART:
                    reached = True; wall_vel[None] = 0.0      # 이미 바닥 = 더 압축할 수 없음
                    if not _restart_floor_hit:
                        _restart_floor_hit = True
                        print(f'  ℹ [restart] 하강 요청이 제작 높이 바닥({_wall_z_start:.5f})에 막힘 — '
                              f'재시작은 제작 상태보다 더 압축하지 않는다 (S-2 가드)', flush=True)
                else:
                    wall_vel[None] = -step / (args.sub * dt)
                    wall_z[None] = _z_next
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
        elif args.servo_legacy:
            # ── LEGACY servo (S-1 이전 동작) — 옛 코퍼스를 바이트 재현할 때만.  ⚠ 아래 결함을
            #    알고도 쓰는 경로다: 움직이는 플래튼에서 반력을 읽어 limit cycle 로 발진한다.
            step = 0.12 * vmax                                   # bidirectional: equilibrate AT target
            if p > 1.02 * target:
                wall_z[None] = min(WALL0, wall_z[None] + step); wall_vel[None] = step / (args.sub * dt)
            elif p < 0.98 * target:
                wall_z[None] = max(WALL_MIN, wall_z[None] - step); wall_vel[None] = -step / (args.sub * dt)
            else:
                wall_vel[None] = 0.0
            conv = conv + 1 if abs(p - target) < 0.03 * target else 0
        else:
            # ── ★ S-1 (2026-07-29 적대리뷰, 3렌즈 동시 CONFIRMED) — servo 를 정지-판독으로 ────────
            #    결함: 반력은 wallf += grid_m·(grid_v[2] − wall_vel) 로 적분된다(:2056).  옛 servo 는
            #    **자기가 방금 움직인 플래튼 위에서** p 를 읽었고, 그 편향의 부호가 제어동작과 같아
            #    **양의 되먹임**이 된다 → 상승하면 음(−) 판독 → 하강 → 양(+) 판독 → 상승 … 무한.
            #    실측: 목표 0.09 인데 −0.019 ↔ +0.206 을 685 프레임 무감쇠 왕복(진폭 감소 7%).
            #    독립 재현은 제하 경로 없이도 됨(pristine `--material SE --n-grid 32 --target-gpa 0.05`
            #    → −0.37 ↔ +0.72) ⇒ 이 결함은 369e9d5d(2026-06-16) 부터의 **기존 결함**이다.
            #    영향: porosity 는 인접 두 위치만 왕복해 진폭 0.04–0.08 %p 로 작지만,
            #    final_stress_GPa 와 **provenance 도장**은 --frames 절단 위상이 결정한다
            #    (3음2양 → 0.80× = 깨끗한 operating_stack_pressure / 2음3양 → 1.30× = _NOT_REACHED).
            #    코드는 이 편향을 이미 알고 있었다 — 제하 프로브가 wall_vel=0 으로 동결하고 읽는
            #    이유가 그것이고("mid-rise frame read −0.23 on a bed really at +0.19"), servo 팔에만
            #    그 처리가 빠져 있었다.  → 같은 구조(이동 → 동결 → 판독)를 그대로 쓴다.
            if _srv_left > 0:                                    # PROBE: 플래튼 동결, 과도응답 감쇠
                wall_vel[None] = 0.0
                _srv_left -= 1
                _srv_win.append(float(p))
                if _srv_left == 0:
                    _qs, _sp = settle_is_quasistatic(_srv_win, rel_tol=args.servo_band / 3.0)
                    # ★ 판정-안정성 (2026-07-29, 첫 실검증에서 발견): "완전 정지"를 요구하면
                    #   **이완 중인 베드에서는 영영 충족되지 않는다** — 실측에서 servo 가 150프레임
                    #   동안 프로브 0회로 아무 결정도 못 했다(wall_z 고정).  하지만 목표의 3배 위에
                    #   있다는 걸 알기 위해 정지까지 기다릴 필요는 없다.  드리프트를 외삽해도
                    #   **판정이 안 바뀌면** 그 판독은 행동하기에 충분하다.  반대로 "밴드 안"이라는
                    #   주장은 수렴 선언이므로 진짜 정지를 요구한다.
                    _v_now = unload_verdict(p, target, args.servo_band)
                    _slope = (_srv_win[-1] - _srv_win[-3]) / 2.0 if len(_srv_win) >= 3 else 0.0
                    _v_ext = unload_verdict(p + 3.0 * _slope, target, args.servo_band)
                    _stable = (_v_now == _v_ext) and _v_now != 'in_band'
                    if not (_qs or _stable) and len(_srv_win) < _settle_max_srv:
                        _srv_left = 1                            # 아직 울림 → 더 기다린다
                    else:                                        # ★ 이 프레임이 THE 판독
                        _srv_spread = float(_sp)
                        _srv_probes += 1
                        _v = unload_verdict(p, target, args.servo_band)
                        if _v == 'in_band':
                            conv += 1
                        else:
                            conv = 0
                            step = 0.12 * vmax
                            _fl = max(WALL_MIN, _wall_z_start) if _RESTART else WALL_MIN
                            if _v == 'above':
                                wall_z[None] = min(WALL0, wall_z[None] + step)
                            else:
                                wall_z[None] = max(_fl, wall_z[None] - step)   # S-2 바닥 공유
                            _srv_left = max(1, _srv_settle)      # 이동 후 다시 동결·판독
                        _srv_win = []
            else:
                _srv_left = max(1, _srv_settle)                  # 첫 진입 → 바로 프로브 창
                wall_vel[None] = 0.0
        por_end = por; p_end = p
        if reached and por_at_target < 0:
            por_at_target = por                              # porosity when target stress was FIRST reached
        _conv_need = 12 if args.servo_legacy else SERVO_HOLD
        if not args.quiet and (frame % args.print_every == 0 or conv >= _conv_need):
            thick = f"  thickness={height*um_box:5.2f}µm" if um_box > 0 else ""
            # phase label — 'settle'/'unload' only ever appear on a --load-state run, so a production
            # (no-restart) log line is byte-identical to before.
            _phase = ('settle' if (_RESTART and frame < _settle)
                      else 'unload' if (_unload and not reached)
                      else 'descend' if not reached else 'servo')
            print(f"  frame {frame:3d} [{_phase}]  "
                  f"{args.readout}={p:7.4f} GPa (wallP={wallp:.4f} σzz_vol={sig_mean:.4f})  "
                  f"porosity={por:6.2f}%  wall_z={wall_z[None]:.3f}{thick}", flush=True)
        if conv >= _conv_need and frame > 20:
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
    # ── MATERIAL SOURCE (review A-6).  Under --load-state the per-point µ/λ/σ_y come from the STATE, not
    #    from --e-se/--nu-se/--sigma-y, so printing/reporting the args described a material the run never
    #    used.  Report the state's values when the state governs, and always say which.  Pristine runs take
    #    the 'args' branch → identical values, byte-identical JSON, unchanged FINAL line.
    _mat_src = 'state_file' if (args.load_state and _state_meta.get('e_se') is not None) else 'args'
    _E_rep = float(_state_meta['e_se']) if _mat_src == 'state_file' else float(args.e_se)
    _nu_rep = float(_state_meta.get('nu_se', args.nu_se)) if _mat_src == 'state_file' else float(args.nu_se)
    _sy_rep = float(_state_meta.get('sigma_y', args.sigma_y)) if _mat_src == 'state_file' else float(args.sigma_y)
    _mu_rep, _la_rep = lame(_E_rep, _nu_rep)
    _K_rep = round(_la_rep + 2.0 * _mu_rep / 3.0, 3) if _mat_src == 'state_file' else round(float(K_SE), 3)
    if _mat_src == 'state_file':
        print(f"MATERIAL  from the STATE FILE (not this command line): E_SE={_E_rep} ν_SE={_nu_rep} "
              f"σ_y={_sy_rep} K_SE={_K_rep} GPa  [the FINAL line above prints this run's --e-se/--nu-se, "
              f"which the restart does NOT apply — metrics JSON reports these state values]")
    # ── ACHIEVED (not requested) end-state — review A-5.  `target` is what was ASKED for; the platen may
    #    have run out of travel, jammed, or (protocol hold) relaxed below it.  Everything the provenance
    #    reports as "this stage's pressure" is derived from these measured numbers.
    _p_ach = float(sum(_p_tail) / len(_p_tail)) if _p_tail else float(p_end)   # mean of the last ≤5 frames
    _wall_z_end = float(wall_z[None])
    _dz_box = _wall_z_end - _wall_z_start
    if args.load_state:
        _dir = 'ROSE (제하)' if _dz_box > 1e-9 else ('DESCENDED (further compaction)' if _dz_box < -1e-9
                                                    else 'DID NOT MOVE')
        print(f"RESTART  unload_status={_unload_status}  platen {_dir}  "
              f"wall_z {_wall_z_start:.4f} → {_wall_z_end:.4f} (Δ={_dz_box:+.4f} box"
              + (f" = {_dz_box * um_box:+.3f} µm" if um_box > 0 else "") + ")  "
              f"{args.readout}_achieved(last≤5 mean)={_p_ach:.4f} GPa vs requested {target:.4f}  "
              f"porosity {float(_state_meta.get('porosity_settled_pct') or float('nan')):.2f}% → {por_end:.2f}%")
        if _p_ach > 1.25 * target:
            print(f"  ⚠ [restart] the bed is STILL at {_p_ach*1000:.1f} MPa, not the requested "
                  f"{target*1000:.1f} MPa — this geometry is NOT an operating-pressure geometry.  "
                  f"state_provenance.P_this_stage_role is tagged NOT_REACHED.")
        # ★ 2026-07-28 HIGH-a GATE.  A non-converged / runaway unload must not leak a porosity,
        #   thickness or coverage number into the pipeline.  The failure mode this closes is not
        #   "the run crashed" but "the run finished and the numbers look plausible" — the platen ends
        #   up clear of the bed, porosity is inflated by the gap, and every downstream consumer reads
        #   it as an operating-pressure geometry.  Refuse by default; the override exists for
        #   deliberate experiments and stamps itself into the provenance.
        # 'unloading' still set at the end = the frame budget ran out MID-SEARCH.  That is a
        # non-convergence too, and it is the easiest one to miss: the loop simply stops, the last
        # probe's geometry is whatever it happened to be, and nothing else in the run says so.
        if _unload_status == 'unloading':
            _unload_status = 'not_converged_frame_budget'
        _bad_unload = _unload_status.startswith('not_converged') or _unload_status == 'out_of_travel'
        _over_unloaded = target > 0 and _p_ach < 0.75 * target and _unload
        if (_bad_unload or _over_unloaded) and not args.allow_unconverged_unload:
            raise SystemExit(
                f"\n[restart] UNLOAD DID NOT CONVERGE — 결과를 내보내지 않고 중단합니다.\n"
                f"  unload_status = {_unload_status}\n"
                f"  {args.readout}_achieved = {_p_ach:.4f} GPa  vs  requested {target:.4f} GPa "
                f"({(_p_ach/target if target > 0 else float('nan')):.2f}×)\n"
                f"  platen wall_z {_wall_z_start:.5f} → {_wall_z_end:.5f} (Δ={_dz_box:+.5f} box), "
                f"porosity {por_end:.2f}%\n"
                f"  이 상태의 porosity/두께/coverage 는 구동압 형상이 아닙니다 — 플래튼이 베드에서 "
                f"떨어졌거나 목표압을 지나쳤습니다.\n"
                f"  → --unload-band 를 넓히거나(현재 ±{args.unload_band:.0%}), --unload-max-probes 를 "
                f"늘리거나(현재 {args.unload_max_probes}), --restart-settle 을 키워 프로브를 안정화하세요.\n"
                f"  → 의도적인 실험이면 --allow-unconverged-unload 로 진행할 수 있습니다 "
                f"(산출물에 not_converged 가 박힙니다).")
    # ── ★ S-1 게이트: servo 가 밴드 안에서 수렴했는가 ────────────────────────────────────
    #    ⚠ 제하 게이트는 `if args.load_state:` 안이라 **pristine 런에는 존재조차 않았다**(적대리뷰
    #    지적).  servo 발진은 제하와 무관하게 일어나므로(독립 재현 확인) 이 게이트는 밖에 둔다.
    if args.protocol == 'servo' and args.compact_to <= 0 and not args.servo_legacy:
        _srv_ok = (conv >= SERVO_HOLD
                   or unload_verdict(p_end, target, args.servo_band) == 'in_band')
        _servo_status = ('converged' if _srv_ok else
                         ('not_converged_probe_not_at_rest'
                          if (_srv_spread is not None and _srv_spread > 0.15)
                          else 'not_converged_frame_budget'))
        if not _srv_ok and not args.allow_unconverged_servo:
            raise SystemExit(
                f"\n[servo] 평형이 밴드 안에서 수렴하지 않았습니다 — 결과를 내보내지 않고 중단합니다.\n"
                f"  servo_status = {_servo_status}   프로브 {_srv_probes}회, "
                f"마지막 창 스프레드 {('%.0f%%' % (_srv_spread*100)) if _srv_spread is not None else 'n/a'}\n"
                f"  {args.readout}_end = {p_end:.4f} GPa vs 목표 {target:.4f} "
                f"(밴드 ±{args.servo_band:.0%}), conv={conv}/12\n"
                f"  이 상태의 final_stress_GPa · porosity · provenance 도장은 수렴한 값이 아닙니다.\n"
                f"  → --frames 를 늘리거나 --servo-band 를 넓히세요 (현재 ±{args.servo_band:.0%}).\n"
                f"  → 의도적 실험이면 --allow-unconverged-servo 로 진행할 수 있습니다.")
    else:
        _servo_status = ('legacy_moving_platen_readout' if args.servo_legacy else 'n/a_not_servo')
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
            'E_SE_GPa': _E_rep, 'nu_SE': _nu_rep,
            'sigma_y_GPa': _sy_rep, 'K_SE_GPa': _K_rep,
            'protocol': args.protocol, 'readout': args.readout,
            'se_dump': bool(args.se_dump), 'se_frac': float(args.se_frac),
            'periodic': bool(PERIODIC),
            'dilate_z': round(float(args.dilate_z), 4) if (args.am_scaffold and float(args.dilate_z) > 1.0) else None,   # stiff-fibre prop-open stretch (None = off / no-op without a scaffold)
        }
        if args.am_scaffold and args.cycle_deform:
            # A-1 cycle-deform (charge-state re-deformation anchor).  ASSUMED-FORM v1 — a single deformed
            # geometry at this ΔV, NOT an N-trajectory (that is the A-3 ledger's job).  (m6) key added ONLY
            # when the flag is on → production/pristine JSON schema stays byte-identical.  ⚠ charge-STATE
            # (reversible SOC breathing), NOT permanent fade — see cycle_geom_debond.py docstring.
            m['cycle_deform'] = {
                'N': int(args.cycle_n), 'dv_sc': round(float(args.cycle_dv_sc), 4),
                'dv_poly': round(float(args.cycle_dv_poly), 4), 'dv_pct_poly': round(float(args.dv_pct_poly), 3),
                'se_evict_pct': _cyc_evict_pct,   # DEFORMATION-INDUCED SE deletion Δ (excl static overlap); v1 non-conserving
                'reversible_charge_state': True,  # this is a charge-state snapshot, not permanent degradation
                'assumed_form': True, 'isotropic': True,
            }
        if args.am_scaffold:
            m.update({
                'seed_AM_frac_pct': round(float(f_am), 2), 'seed_SE_frac_pct': round(float(f_se), 2),
                'SE_of_solid_pct': round(100.0 * se_solid / max(am_solid + se_solid, 1e-12), 2),
                'bulk_density_g_cm3': round(float(bulk_rho), 3), 'n_AM': int(len(am_r)),
            })
        if args.load_state or args.save_state:
            # ── PRESSURE / PLASTIC-HISTORY PROVENANCE (docs/temp_pressure_capability.md §P1-a, §P1.5).
            #    Downstream (payload → STEP3 σ → STEP5 ledger) must be able to tell a 300-MPa press-peak
            #    geometry from a 300-MPa-fabricated bed re-equilibrated at the OPERATING stack pressure.
            #    Key added ONLY when a restart flag is used → the pristine production JSON schema is
            #    byte-identical (same convention as the `cycle_deform` key above). ─────────────────────
            _chain = list(_state_meta.get('fab_chain') or ([_state_meta['target_gpa']]
                                                          if 'target_gpa' in _state_meta else []))
            _fab = (_chain[0] if _chain else float(target))   # ORIGINAL fabrication pressure of the chain
            # ★ ACHIEVED vs REQUESTED (review A-5).  P_this_stage_MPa is the REQUEST; the badge that renders
            #   it must not be able to claim "90 MPa" for a bed the platen never unloaded.  The role string
            #   (rendered next to it in webapp/templates/single.html) is tagged NOT_REACHED whenever the
            #   measured end-state stress is still >25 % above the request, and the measured numbers are
            #   published alongside so a reader can check the claim instead of trusting the label.
            _p_ach_mpa = round(float(_p_ach) * 1000.0, 3)
            _role = stage_pressure_role(bool(args.load_state), _p_ach, target)
            _not_reached = _role.endswith('_NOT_REACHED')
            m['state_provenance'] = {
                'schema': STATE_SCHEMA,
                'pressure_chain_GPa': _chain + [float(target)] if args.load_state else [float(target)],
                'plastic_history_restored': bool(args.load_state),
                'P_fab_MPa': (round(float(_fab) * 1000.0, 3) if _fab is not None else None),
                'P_this_stage_MPa': round(float(target) * 1000.0, 3),
                'P_this_stage_is': 'REQUESTED_target',                      # ← not the achieved value
                'P_achieved_MPa': _p_ach_mpa,                               # measured, mean of the last ≤5 frames
                'P_achieved_readout': args.readout,
                'P_achieved_over_requested': (round(float(_p_ach) / float(target), 4) if target > 0 else None),
                'P_this_stage_role': _role,
                # what the platen actually did this stage (box units + µm) — the audit trail for the above
                'unload_status': _unload_status,
                'unload_probe_hold_frames': int(UNLOAD_HOLD),
                # ★ 2026-07-28 HIGH-a: 제하 탐색이 실제로 어떤 조건에서 멈췄는지 — 밴드·프로브 예산·
                #   사용한 프로브 수·최종 브래킷.  "완료" 라는 한 단어 대신 수렴 근거를 남긴다.
                'unload_band': float(args.unload_band),
                'unload_probes_used': int(_unload_probes),
                'unload_max_probes': int(args.unload_max_probes),
                'unload_bracket_box': [round(float(_z_lo), 6),
                                       (round(float(_z_hi), 6) if _z_hi is not None else None)],
                'unload_unconverged_override': bool(args.allow_unconverged_unload),
                # ★ the ACTIONABLE number: how many frozen frames a probe actually needed at this
                #   resolution before the bed was at rest.  --restart-settle is only the minimum, so
                #   this is what a future run at the same n_grid should budget for (settling time
                #   scales with the wave transit time, so it is resolution-specific by nature).
                'probe_window_frames_max': int(_probe_win_max),
                'probe_window_extended': bool(_probe_extended),
                'restart_settle_min': int(args.restart_settle),
                'restart_settle_max': int(args.restart_settle_max),
                'settle_quasistatic': _settle_quasistatic,
                'settle_tail_spread_rel': (round(float(_settle_spread_rel), 4)
                                          if _settle_spread_rel is not None else None),
                # ★ S-1: servo 평형이 수렴했는지 — 옛 산출물에는 이 정보가 **한 필드도** 없어서
                #   limit cycle 위상이 그대로 도장이 됐다 (적대리뷰 3렌즈 CONFIRMED).
                'servo_status': _servo_status,
                'servo_band': float(args.servo_band),
                'servo_probes': int(_srv_probes),
                'servo_tail_spread_rel': (round(float(_srv_spread), 4)
                                          if _srv_spread is not None else None),
                'servo_readout': ('legacy_moving_platen (limit-cycle prone)' if args.servo_legacy
                                  else 'at_rest_probe (move → freeze → read)'),
                'unload_search': 'bracket_then_bisect (rise until p<band, then bisect; floor = restart '
                                 'height so the search never adds plastic compaction)',
                'wall_z_start': round(float(_wall_z_start), 6),
                'wall_z_end': round(float(_wall_z_end), 6),
                'platen_delta_box': round(float(_dz_box), 6),
                'platen_delta_um': (round(float(_dz_box) * um_box, 4) if um_box > 0 else None),
                'platen_direction': ('rose_unloaded' if _dz_box > 1e-9 else
                                     'descended_compacted' if _dz_box < -1e-9 else 'did_not_move'),
                'porosity_fab_pct': _state_meta.get('porosity_settled_pct'),
                'porosity_end_pct': round(float(por_end), 3),
                'thickness_fab_um': _state_meta.get('thickness_um'),
                'restart_settle_frames': int(_settle),
                'protocol_this_stage': args.protocol,
                # what `protocol` MEANS for a restart, so the two-arm bracket is not read as one number:
                #   servo = compliant fixture (stress held AT the target, thickness free to creep)
                #   hold  = rigid fixture (platen FIXED after the unload, stress free to relax below it)
                'protocol_semantics': (('servo = constant-stress fixture (unload to target, then hold that '
                                        'stress; thickness is the free variable)') if args.protocol == 'servo'
                                       else ('hold = constant-gap fixture (unload to target, then FIX the '
                                             'platen; stress relaxes below the target — that relaxation is '
                                             'the rigid-jig arm, not a failure)')) if args.load_state else None,
                'fab_protocol': (_state_meta.get('protocol') if args.load_state else args.protocol),
                'fab_wall_z': (_state_meta.get('wall_z') if args.load_state else None),
                'wall_z_resumed': (round(float(_state_wall_z), 4) if _state_wall_z is not None else None),
                'restart_velocity_convention': 'v_and_C_zeroed_on_load',
                'loaded_from': (args.load_state or None), 'saved_to': (args.save_state or None),
                # share of restored points sitting inside the CURRENT (possibly cycle-deformed) AM mask:
                # pinned rather than evicted, so that volume is counted in BOTH Σpvol and AM_vol
                'se_points_inside_AM_pct': locals().get('_se_in_am_pct'),
                'se_evicted_on_load': False,   # restart NEVER deletes points (seed-time eviction only)
                # per-point material (µ/λ/σ_y/coh) comes from the state, NOT from this run's --e-se etc.
                'material_from_state': bool(args.load_state),
                'material_args_ignored': (locals().get('_mat_mismatch') or None),
                # which numbers the E_SE_GPa / nu_SE / sigma_y_GPa / K_SE_GPa fields above describe
                'material_source': _mat_src,
                # cohesion: the compile-time gate is re-armed from the state when the restart omits --coh
                # (otherwise the restored binder/cold-weld would be silently compiled out)
                'coh_GPa_effective': round(float(COH), 6),
                'coh_rearmed_from_state_GPa': locals().get('_coh_rearmed'),
                # fibre rods: were the rest length/curvature restored, or re-derived from the COMPRESSED
                # positions (= the buckled shape becomes stress-free and the stored bending energy is lost)?
                'rod_rest_source': locals().get('_rod_rest_source'),
                # honest limits: the constitutive model has NO rate/creep term, so a "held at 90 MPa for
                # hundreds of hours" state is NOT represented — only the stress-equilibrated geometry is.
                'rate_dependence': 'NOT_MODELLED_rate_independent_J2',
                'T_C': None, 'T_dependence': 'NOT_MODELLED',   # this solver has no temperature axis at all
            }
        _add_meta = locals().get('_add_meta') or {}          # per-additive recipe+physics (if additives seeded)
        if not _add_meta and _state_in is not None and _state_meta.get('additives'):
            _add_meta = dict(_state_meta['additives'])       # inherited through --load-state (points travel in
            m['additives_inherited_from_state'] = True       # the arrays; the recipe meta travels in the meta)
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
    if args.save_state:
        # ── FULL restart state (see the STATE_SCHEMA note at the top of this file).  Everything the
        #    next stage needs to continue THIS bed instead of re-seeding a virgin one: positions,
        #    the deformation gradient F (elastic stress + plastic shape memory), the per-point material
        #    constants, the two accumulated-strain histories, the additive bookkeeping arrays, and the
        #    AM-scaffold fingerprint that the loader validates against. ────────────────────────────────
        _arr = {'x': x.to_numpy(), 'F': F.to_numpy(),
                'v': v.to_numpy(), 'C': C.to_numpy(),      # written for auditability; ZEROED on load
                'mu_p': mu_p.to_numpy(), 'la_p': la_p.to_numpy(), 'yld_p': yld_p.to_numpy(),
                'pvol_p': pvol_p.to_numpy(), 'coh_p': coh_p.to_numpy(),
                'dg_acc': dg_acc.to_numpy(), 'eps_acc': eps_acc.to_numpy(),
                'phase': np.asarray(phase_np, np.int8),
                'am_pos': (np.asarray(am_c, np.float64) if am_c is not None else np.zeros((0, 3))),
                'am_r_pristine': (np.asarray(am_r_pristine, np.float64) if am_r_pristine is not None
                                  else np.zeros(0)),
                'am_r_applied': (np.asarray(am_r, np.float64) if am_r is not None else np.zeros(0))}
        if fibre_np is not None:
            _arr['fibre'] = np.asarray(fibre_np, np.int32)
        if dia_np is not None:
            _arr['fibre_dia'] = np.asarray(dia_np, np.float32)
        if se_id_base is not None:
            _sid = np.full(n, -1, np.int32); _sid[:len(se_id_base)] = se_id_base
            _arr['se_id'] = _sid
        if FIBRE_ROD:
            # ★ rod REST state (review A-7): rl/b0 are the stress-free length/curvature the XPBD rod
            #   restores toward.  build_rod_topology derives them from whatever positions it is handed, so
            #   a restart that re-derived them from the COMPRESSED bed would make the buckled shape the new
            #   rest shape (fabrication bending energy erased).  Carry the originals in the state instead.
            _arr['rod_rl'] = rod_rl.to_numpy().astype(np.float32)
            _arr['rod_b0'] = rod_b0.to_numpy().astype(np.float32)
        _bad = state_finite_errors({k: _arr[k] for k in _STATE_REQUIRED})
        if _bad:
            raise SystemExit("[save-state] refusing to write a diverged state:\n  - " + "\n  - ".join(_bad))
        _state_add_meta = locals().get('_add_meta') or (_state_meta.get('additives') if _state_in else None)
        try:                                                 # never let un-serialisable recipe meta kill the save
            import json as _js0; _js0.dumps(_state_add_meta)
        except Exception as _e:
            print(f"  [save-state] additive meta not JSON-serialisable ({_e}) → omitted from the state")
            _state_add_meta = None
        _meta = {
            'schema': STATE_SCHEMA, 'n_pts': int(n),
            'n_grid': int(n_grid), 'nz': int(nz), 'lateral_box': float(args.lateral_box),
            'periodic': bool(PERIODIC),
            'wall_z': float(wall_z[None]),   # FULL precision — a rounded platen height would make the
            #                                  no-change round-trip start at a slightly different porosity
            'FLOOR': float(FLOOR), 'WALL0': float(WALL0),
            'WALL_MIN': float(WALL_MIN), 'um_box_um': (float(um_box) if um_box > 0 else None),
            'target_gpa': float(target), 'protocol': args.protocol, 'readout': args.readout,
            'final_stress_GPa': round(float(p_end), 6),
            # achieved (measured) end-state, so a 3rd stage restarting from THIS file knows what pressure
            # the geometry is really at — `target_gpa` above is only what was requested.
            'p_achieved_GPa': round(float(_p_ach), 6),
            'unload_status': _unload_status,
            'platen_delta_box': round(float(_dz_box), 6),
            'rod_rest_source': locals().get('_rod_rest_source'),
            'porosity_settled_pct': round(float(por_end), 4),
            'thickness_um': (round(float((wall_z[None] - FLOOR) * um_box), 4) if um_box > 0 else None),
            'e_se': float(args.e_se), 'nu_se': float(args.nu_se), 'sigma_y': float(args.sigma_y),
            'coh': float(COH), 'am_scaffold': bool(args.am_scaffold), 'se_dump': bool(args.se_dump),
            'se_frac': float(args.se_frac), 'dilate_z': float(args.dilate_z),
            'n_am': int(len(am_r)) if am_r is not None else 0,
            'am_fingerprint': (state_fingerprint(am_c, am_r_pristine)
                               if (am_c is not None and am_r_pristine is not None) else None),
            'am_radii_deformed': bool(args.cycle_deform or args.fracture_scaffold),
            # carry the additive RECIPE provenance through the restart: the additive POINTS travel in the
            # arrays, but `_add_meta` is only built by the seeder, so without this a stage-② metrics JSON
            # would silently lose "this bed is 1 wt% VGCF + 1 wt% PTFE" (which STEP3/the payload read).
            'additives': _state_add_meta,
            'cycle_deform': ({'N': int(args.cycle_n), 'dv_sc': float(args.cycle_dv_sc),
                              'dv_poly': float(args.cycle_dv_poly),
                              'dv_pct_poly': float(args.dv_pct_poly)} if args.cycle_deform else None),
            'loaded_from': (args.load_state or None),
            # full pressure chain across an N-stage restart chain (fab → op → op' → …), so a 3rd-stage
            # state still knows the ORIGINAL fabrication pressure
            'fab_chain': list(_state_meta.get('fab_chain') or []) + [float(target)],
            # ★ the deliberate restart convention — the loader ZEROES v and C (quasi-static restart from
            #   the relaxed state); all stress that matters lives in F.  Recorded so a reader of this file
            #   never has to guess whether the velocities were meaningful.
            'restart_velocity_convention': 'v_and_C_zeroed_on_load',
            'rate_dependence': 'NOT_MODELLED_rate_independent_J2',
            'T_C': None, 'T_dependence': 'NOT_MODELLED',
        }
        _, _nb, _cz = write_state_npz(args.save_state, _arr, _meta)
        _dgv = _arr['dg_acc']
        print(f"  saved restart state → {args.save_state}  ({n:,} pts, {len(_arr)} arrays, "
              f"{_nb / 1e9:.2f} GB raw, {'deflate' if _cz else 'store'}; "
              f"wall_z={_meta['wall_z']} target={_meta['target_gpa']} GPa protocol={args.protocol}; "
              f"Σdg mean={float(_dgv.mean()):.4f}; AM fp={_meta['am_fingerprint']})")
        print(f"  → resume with:  --load-state {args.save_state} --protocol servo --target-gpa <operating> "
              f"[--cycle-deform ...]   (v,C are zeroed = quasi-static restart)")


if __name__ == '__main__':
    main(sys.argv[1:])
