#!/usr/bin/env python3
"""DEM ↔ MPM 1:1 porosity cross-validation at 300 MPa (frame [4]).

For every DEM design point in docs/data/dem_design_points.csv, build the SAME
geometry (AM_P:AM_S:SE size ratios) and composition (phi_am, phi_se, P:S) in the
champion MPM (E_SE=1.53/σ_y=0.15 plastic + work-hardening, AM rigid), compress a
servo wall to the SAME pressure (300 MPa via mean particle pressure), and read
MPM porosity.  Output: per-case DEM vs MPM porosity → parity check.

SE radius is fixed at R_SE=0.006 (resolution-consistent ~2-3 cells at 320); AM
radii scale by the case's measured size ratios (r_AM/r_SE), so each case keeps
its own bimodal geometry.  Composition taken directly from the DEM phi fractions.

Run (uma GPU):
  python3 scripts/mpm_dem_match.py [--n-grid 320] [--seeds 2] [--real-only]
                                   [--max-n 12] [--p-read 0.30]
  python3 scripts/mpm_dem_match.py --plot      # parity plot from the CSV (matplotlib)
Out: docs/data/mpm_dem_match.csv  (+ docs/figures/mpm_dem_match_parity.png with --plot)
"""
import argparse
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DP = os.path.join(HERE, '..', 'docs', 'data', 'dem_design_points.csv')
OUT = os.path.join(HERE, '..', 'docs', 'data', 'mpm_dem_match.csv')

# ---- fixed MPM material / geometry (champion) -----------------------------
R_SE_MPM = 0.006                      # fixed smallest radius (sets resolution)
INIT_SOLID = 0.50
FLOOR = 0.08; SW_L, SW_R = 0.08, 0.92; WIDTH = SW_R - SW_L
WALL0 = 0.66; WALL_MIN = 0.05; WALL_V = 0.18
P_STOP = 0.70
F50_POR_FLOOR = 5.0   # stop the f50 sweep once clearly over-compressed (≈ jamming POR_FLOOR 0.05)


def _f50_porosity(por, p):
    """Self-normalised f50 readout (port of mpm2d_jamming.jam_porosity, f=0.50):
    porosity (%) where the bed's mean pressure first reaches 50% of its OWN max.

    The absolute mean-pressure amplitude is RESOLUTION-SCALED, so reading porosity
    at a COMMON absolute pressure (e.g. 300 MPa) is grid-biased — pure-SE collapsed
    11%@320 → 0.8%@512.  At f50 the resolution amplitude factor cancels
    (mpm2d_jamming 320≡512≡768, Pearson 0.94) and the champion's f50 already lands
    at the experimental ~10-15%.  This is an INTERNAL MPM readout-consistency fix
    (reads the MPM's own P-φ curve at a resolution-invariant point) — it uses NO DEM
    data, so it is NOT a DEM↔MPM cross-fit (frame [4] safe)."""
    import numpy as np
    por = np.asarray(por, float); p = np.maximum(np.asarray(p, float), 0.0)
    if len(por) == 0:
        return float('nan')
    p_ref = float(np.max(p[-5:])) if len(p) >= 5 else float(np.max(p))
    if p_ref <= 0:
        return float(por[-1])
    order = np.argsort(por)[::-1]            # loose → compressed (porosity descending)
    pp, qq = por[order], p[order]
    idx = np.where(qq >= 0.50 * p_ref)[0]
    return float(pp[idx[0]]) if len(idx) else float(pp[-1])


def _is_particulate(nm):
    n = nm.lower()
    return ('particulate' in n) or n.startswith('input_s_') or n == 'input_s'


def load_design(names=None, real_only=False, particulate=False, max_n=None):
    with open(DP) as fh:
        rows = list(csv.DictReader(fh))
    out = []
    for r in rows:
        nm = r['name']
        if real_only and 'real' not in nm:
            continue
        if particulate and not _is_particulate(nm):
            continue
        if names and nm not in names:
            continue
        out.append(dict(
            name=nm,
            ratio_P=float(r['ratio_P']), ratio_S=float(r['ratio_S']),
            phi_am=float(r['phi_am']), phi_se=float(r['phi_se']),
            PS=r['PS'], dem=float(r['dem_porosity']),
            r_SE=float(r['r_SE']), AM_wt=float(r['AM_wt']),
            e_se_gpa=float(r.get('e_se_gpa') or 1.35)))
    if max_n:
        out = out[:max_n]
    return out


def _strain_png(outdir, p10, amwt, por, xy, epl):
    """Save a 2D plastic-strain (Σdg per particle) map PNG for one (P:S, AM%) composition."""
    import os as _o
    import numpy as _np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as _plt
    _o.makedirs(outdir, exist_ok=True)
    vmax = (float(_np.percentile(epl, 98)) + 1e-6) if len(epl) else 1.0
    fig, ax = _plt.subplots(figsize=(4.2, 4.2))
    sc = ax.scatter(xy[:, 0], xy[:, 1], c=epl, s=2, cmap='inferno', vmin=0.0, vmax=vmax)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(f"P:S {p10}:{10 - p10}  AM {int(amwt)}wt%  por={por:.1f}%", fontsize=9)
    fig.colorbar(sc, ax=ax, label='plastic strain Σdg', shrink=0.8)
    fig.tight_layout()
    fig.savefig(_o.path.join(outdir, f"strain_PS{p10}-{10 - p10}_AM{int(amwt)}.png"), dpi=110)
    _plt.close(fig)


def run_match(args):
    import numpy as np
    import taichi as ti
    ng = args.n_grid
    try:
        ti.init(arch=ti.gpu, default_fp=ti.f32, random_seed=7); print('  [taichi] GPU')
    except Exception as e:
        print(f'  [taichi] GPU failed ({e}); CPU'); ti.init(arch=ti.cpu, default_fp=ti.f32, random_seed=7)
    dx = 1.0 / ng; inv_dx = float(ng); dt = 8.0e-5 * 320.0 / ng; p_vol = (dx * 0.5) ** 2
    def lame(E, nu): return E / (2 * (1 + nu)), E * nu / ((1 + nu) * (1 - 2 * nu))
    # Champion MPM SE modulus 1.53 GPa ↔ DEM effective 1.35 GPa: each is its
    # OWN experiment-calibrated baseline (frame [4]).  For the E-sweep cases
    # (particulate_9_E05/E15 = DEM E ×0.5/×1.5) we apply the SAME relative
    # perturbation to the MPM baseline → MPM_E = 1.53·(DEM_E/1.35).  This tests
    # whether the porosity RESPONSE to E matches, without cross-fitting absolute E.
    MPM_E_CHAMPION = 1.53; DEM_E_BASE = 1.35
    MODEL = args.model                      # 'vonmises' (champion, default) | 'dpc'
    # --e-se overrides the SE base modulus (e.g. real E=24 for the cap cross-check;
    # the cap, not a softened E, then supplies the realistic residual porosity).
    E_se_base = float(args.e_se) if args.e_se else MPM_E_CHAMPION
    MU_SE, LA_SE = lame(E_se_base, args.nu_se); MU_AM, LA_AM = lame(140.0, 0.25)
    YIELD_SE = float(args.yield_se); YIELD_AM = 1.0e4; HARD_SE = float(args.hard_se); RHO_AM, RHO_SE = 4.8, 2.0
    MAXP = 2_500_000
    x = ti.Vector.field(2, ti.f32, MAXP); v = ti.Vector.field(2, ti.f32, MAXP)
    C = ti.Matrix.field(2, 2, ti.f32, MAXP); F = ti.Matrix.field(2, 2, ti.f32, MAXP)
    mu_p = ti.field(ti.f32, MAXP); la_p = ti.field(ti.f32, MAXP); yld_p = ti.field(ti.f32, MAXP)
    m_p = ti.field(ti.f32, MAXP); prs = ti.field(ti.f32, MAXP); epl = ti.field(ti.f32, MAXP)
    avp = ti.field(ti.f32, MAXP)   # accumulated volumetric plastic compaction (hardens the cap)
    grid_v = ti.Vector.field(2, ti.f32, (ng, ng)); grid_m = ti.field(ti.f32, (ng, ng))
    wall_y = ti.field(ti.f32, ()); N = ti.field(ti.i32, ())
    wall_vf = ti.field(ti.f32, ())   # servo wall speed — slows as Pcur→p_read (no overshoot)
    wall_imp = ti.field(ti.f32, ())  # accumulated wall reaction impulse (Σ m·(v+wall_vf)) → boundary stress
    # DPC cap params (runtime so --heckel can sweep): pressure-dependent shear
    # (cap_fric) + DIVERGENT hardening cap  p_b(avp) = cap_pb0·(avpmax/(avpmax-avp))^cap_h
    # → p_b → ∞ as avp → cap_avpmax (residual floor φ_min), so densification
    # stops at a physical residual instead of collapsing to 0 (DPC/Cam-Clay).
    cap_pb0 = ti.field(ti.f32, ()); cap_h = ti.field(ti.f32, ())
    cap_fric = ti.field(ti.f32, ()); cap_avpmax = ti.field(ti.f32, ())
    # JAM model params: deviatoric (shear) yield diverges as the GLOBAL porosity
    # → jam_phimin (local packing → φ_max), σ_y_eff = σ_y/frac^jam_k with
    # frac=(poro-phimin)/(poro0-phimin).  Isochoric — NO particle shrinkage; the
    # physically-correct way to stop rearrangement at the residual (jamming).
    jam_poro = ti.field(ti.f32, ()); jam_poro0 = ti.field(ti.f32, ())
    jam_phimin = ti.field(ti.f32, ()); jam_k = ti.field(ti.f32, ())

    @ti.kernel
    def load(xy: ti.types.ndarray(), mu: ti.types.ndarray(), la: ti.types.ndarray(),
             yl: ti.types.ndarray(), ms: ti.types.ndarray(), n: ti.i32):
        N[None] = n
        for p in range(n):
            x[p] = ti.Vector([xy[p, 0], xy[p, 1]]); v[p] = ti.Vector([0.0, 0.0])
            C[p] = ti.Matrix.zero(ti.f32, 2, 2); F[p] = ti.Matrix.identity(ti.f32, 2)
            mu_p[p] = mu[p]; la_p[p] = la[p]; yld_p[p] = yl[p]; m_p[p] = ms[p]
            epl[p] = 0.0; avp[p] = 0.0

    @ti.kernel
    def substep():
        for I in ti.grouped(grid_m):
            grid_v[I] = ti.Vector.zero(ti.f32, 2); grid_m[I] = 0.0
        for p in range(N[None]):
            base = (x[p] * inv_dx - 0.5).cast(int); fx = x[p] * inv_dx - base.cast(ti.f32)
            w = [0.5 * (1.5 - fx) ** 2, 0.75 - (fx - 1.0) ** 2, 0.5 * (fx - 0.5) ** 2]
            U, sig, V = ti.svd(F[p]); J = sig[0, 0] * sig[1, 1]
            la_e = la_p[p]
            if ti.static(MODEL == 'jam'):
                # ── volumetric jamming: the bed's effective BULK modulus diverges
                # as global porosity → jam_phimin (packing → φ_max).  Loose powder
                # is compliant (la=softened base → compacts by rearrangement);
                # jammed powder is incompressible (la→∞ → resists the wall) — this
                # resists the volumetric wall load, unlike a shear yield, and is
                # NOT particle shrinkage (it's the packing stiffness).
                if yld_p[p] < 1.0:
                    fr = ti.max((jam_poro[None] - jam_phimin[None]) /
                                ti.max(jam_poro0[None] - jam_phimin[None], 1e-3), 1e-3)
                    la_e = la_p[p] / ti.pow(fr, jam_k[None])
            st = (2 * mu_p[p] * (F[p] - U @ V.transpose()) @ F[p].transpose()
                  + ti.Matrix.identity(ti.f32, 2) * la_e * J * (J - 1))
            prs[p] = -0.5 * (st[0, 0] + st[1, 1]) / ti.max(J, 1e-4)
            st = (-dt * p_vol * 4 * inv_dx * inv_dx) * st; aff = st + m_p[p] * C[p]
            for a, b in ti.static(ti.ndrange(3, 3)):
                off = ti.Vector([a, b]); dpos = (off.cast(ti.f32) - fx) * dx; wt = w[a][0] * w[b][1]
                grid_v[base + off] += wt * (m_p[p] * v[p] + aff @ dpos); grid_m[base + off] += wt * m_p[p]
        for I in ti.grouped(grid_m):
            if grid_m[I] > 0:
                grid_v[I] /= grid_m[I]; i, j = I[0], I[1]
                if j * dx < FLOOR and grid_v[I][1] < 0: grid_v[I][1] = 0.0
                if j * dx > wall_y[None]:
                    vb = grid_v[I][1]
                    if vb > -wall_vf[None]:                    # bed stress resists the descending wall
                        wall_imp[None] += grid_m[I] * (vb + wall_vf[None])   # reaction impulse → boundary load
                        grid_v[I][1] = -wall_vf[None]          # (= ti.min(vb,-wall_vf) for vb>-wall_vf)
                if i * dx < SW_L and grid_v[I][0] < 0: grid_v[I][0] = 0.0
                if i * dx > SW_R and grid_v[I][0] > 0: grid_v[I][0] = 0.0
        for p in range(N[None]):
            base = (x[p] * inv_dx - 0.5).cast(int); fx = x[p] * inv_dx - base.cast(ti.f32)
            w = [0.5 * (1.5 - fx) ** 2, 0.75 - (fx - 1.0) ** 2, 0.5 * (fx - 0.5) ** 2]
            nv = ti.Vector.zero(ti.f32, 2); nc = ti.Matrix.zero(ti.f32, 2, 2)
            for a, b in ti.static(ti.ndrange(3, 3)):
                off = ti.Vector([a, b]); dpos = off.cast(ti.f32) - fx; wt = w[a][0] * w[b][1]; gv = grid_v[base + off]
                nv += wt * gv; nc += 4 * inv_dx * wt * gv.outer_product(dpos)
            v[p] = nv; C[p] = nc; F[p] = (ti.Matrix.identity(ti.f32, 2) + dt * nc) @ F[p]
            U, sig, V = ti.svd(F[p])
            e0 = ti.log(ti.max(sig[0, 0], 1e-4)); e1 = ti.log(ti.max(sig[1, 1], 1e-4))
            tr = e0 + e1; d0 = e0 - 0.5 * tr; d1 = e1 - 0.5 * tr; dn = ti.sqrt(d0 * d0 + d1 * d1) + 1e-9
            if ti.static(MODEL == 'vonmises' or MODEL == 'jam'):
                # champion von Mises deviatoric clamp, ISOCHORIC.  For 'jam' the
                # jamming is supplied by the density-dependent BULK modulus in the
                # P2G stress above (volumetric), NOT by the shear yield.
                dg = dn - (yld_p[p] * (1.0 + HARD_SE * epl[p])) / (2 * mu_p[p])
                if dg > 0:
                    epl[p] += dg
                    m0 = (d0 - dg * d0 / dn) + 0.5 * tr; m1 = (d1 - dg * d1 / dn) + 0.5 * tr
                    F[p] = U @ ti.Matrix([[ti.exp(m0), 0.0], [0.0, ti.exp(m1)]]) @ V.transpose()
            else:
                # ── Drucker-Prager + Cap (DPC) on the SE phase only (AM stays elastic) ──
                # (1) deviatoric: pressure-dependent shear yield  τ_y = σ_y + μ_fric·p
                #     (Klár 2016 friction → granular grains resist shear/rearrangement
                #      more as confining pressure rises = jamming the continuum lacks).
                # (2) volumetric cap: hydrostatic yield p_b(avp)=pb0·exp(h·avp) hardens
                #     with accumulated plastic compaction → densification stops at a
                #     physical residual porosity (DPC powder-compaction standard).
                if yld_p[p] < 1.0:   # SE
                    Kb = la_p[p]                           # vol stiffness, matches P2G la·J·(J-1)
                    pmean = -Kb * tr                       # pressure (compression tr<0 → p>0)
                    y_dev = yld_p[p] * (1.0 + HARD_SE * epl[p]) + cap_fric[None] * ti.max(pmean, 0.0)
                    dg = dn - y_dev / (2 * mu_p[p])
                    if dg > 0:                             # shear return (project deviatoric)
                        epl[p] += dg
                        d0 = d0 - dg * d0 / dn; d1 = d1 - dg * d1 / dn
                    amax = cap_avpmax[None]                # divergent cap: p_b → ∞ at avp→amax
                    pb = cap_pb0[None] * ti.pow(amax / ti.max(amax - avp[p], 1e-3), cap_h[None])
                    if pmean > pb:                         # cap return → permanent densification
                        tr_new = -pb / Kb                  # relax elastic compression to the cap
                        avp[p] = ti.min(avp[p] + (tr_new - tr), amax - 1e-3)   # +ve, floored at amax
                        tr = tr_new
                    g0 = d0 + 0.5 * tr; g1 = d1 + 0.5 * tr
                    F[p] = U @ ti.Matrix([[ti.exp(g0), 0.0], [0.0, ti.exp(g1)]]) @ V.transpose()
            x[p] += dt * v[p]

    def build(R_AMP, R_AMS, fAP, fAS, fSE, rng, mu_se=MU_SE, la_se=LA_SE):
        fill_h = WALL0 - 0.02; box = WIDTH * (fill_h - FLOOR); target = INIT_SOLID * box
        placed = []; cell = max(R_AMP, R_SE_MPM) * 1.05; Hm = {}
        def clash(cx, cy, r):
            ci, cj = int(cx / cell), int(cy / cell)
            for di in (-2, -1, 0, 1, 2):
                for dj in (-2, -1, 0, 1, 2):
                    for (px, py, pr) in Hm.get((ci + di, cj + dj), []):
                        if (cx - px) ** 2 + (cy - py) ** 2 < (r + pr + 0.2 * R_SE_MPM) ** 2: return True
            return False
        def add(cx, cy, r):
            placed.append((cx, cy, r)); Hm.setdefault((int(cx / cell), int(cy / cell)), []).append((cx, cy, r))
        plan = [(R_AMP, fAP, MU_AM, LA_AM, YIELD_AM, RHO_AM),
                (R_AMS, fAS, MU_AM, LA_AM, YIELD_AM, RHO_AM),
                (R_SE_MPM, fSE, mu_se, la_se, YIELD_SE, RHO_SE)]
        xs = []; mu = []; la = []; yl = []; ms = []
        for (r, frac, mm, ll, yy, rho) in plan:
            if frac <= 1e-6: continue
            goal = frac * target; acc = 0.0; t = 0
            while acc < goal and t < 1_500_000:
                t += 1; cx = rng.uniform(SW_L + r, SW_R - r); cy = rng.uniform(FLOOR + r, fill_h - r)
                if clash(cx, cy, r): continue
                add(cx, cy, r)
                k = int(r / (dx * 0.5)) + 1
                for a in range(-k, k + 1):
                    for b in range(-k, k + 1):
                        px, py = cx + a * dx * 0.5, cy + b * dx * 0.5
                        if (px - cx) ** 2 + (py - cy) ** 2 <= r * r:
                            xs.append((px, py)); mu.append(mm); la.append(ll); yl.append(yy); ms.append(p_vol * rho)
                acc += np.pi * r * r
        return (np.array(xs, np.float32), np.array(mu, np.float32), np.array(la, np.float32),
                np.array(yl, np.float32), np.array(ms, np.float32))

    def run_once(R_AMP, R_AMS, fAP, fAS, fSE, seed, e_se_mpm=None, p_read=None,
                 readout='f50'):
        cap_pb0[None] = args.cap_pb0; cap_h[None] = args.cap_h; cap_fric[None] = args.cap_fric
        cap_avpmax[None] = args.cap_avpmax
        jam_phimin[None] = args.jam_phimin; jam_k[None] = args.jam_k
        if e_se_mpm is None: e_se_mpm = E_se_base
        pr = p_read if p_read else args.p_read
        rng = np.random.default_rng(seed)
        mu_se, la_se = lame(e_se_mpm, args.nu_se)
        xy, mu, la, yl, ms = build(R_AMP, R_AMS, fAP, fAS, fSE, rng,
                                   mu_se=mu_se, la_se=la_se); n = len(xy)
        if n == 0: return float('nan')
        sa = n * p_vol; load(xy, mu, la, yl, ms, n); wall_y[None] = WALL0; wall_vf[None] = WALL_V
        top_full = FLOOR + sa / WIDTH; wall_floor = top_full + 0.002
        por0 = max(0.0, 1.0 - sa / (WIDTH * (WALL0 - FLOOR))) * 100   # initial porosity %
        jam_poro0[None] = por0; jam_poro[None] = por0
        if readout == 'f50':
            # ── self-normalised f50 readout (resolution-invariant) ──────────────
            # FIXED slow-velocity sweep → record the full P(porosity) curve → read
            # porosity where the bed's pressure first hits 50% of its OWN max.  The
            # resolution-scaled amplitude cancels (320≡512), unlike the absolute
            # 300-MPa readout below which collapses pure-SE 11%@320 → 0.8%@512.
            por_s = []; p_s = []
            for fr in range(int(8000 * ng / 320)):
                for _ in range(25): substep()
                top = wall_y[None]
                por = max(0.0, 1.0 - sa / (WIDTH * (top - FLOOR))) * 100
                jam_poro[None] = por                       # feed jam model (no-op for vonmises)
                por_s.append(por); p_s.append(float(np.mean(prs.to_numpy()[:n])))
                if top <= wall_floor + 1e-4 or por <= F50_POR_FLOOR:
                    break
                wall_y[None] = max(top - WALL_V * 25 * dt, wall_floor)   # fixed v, NO servo
            return _f50_porosity(por_s, p_s)
        if readout == 'wallP':
            # ── resolution-INVARIANT *absolute* readout: servo to the WALL REACTION stress ──
            # mean(prs) is a VOLUME average → the well-resolved soft SE dilutes it (512 over-
            # compresses to 0.8% before the mean hits 300 MPa).  The wall reaction
            # Σ grid_m·(v+wall_vf)/(n_sub·dt·WIDTH) = boundary force / area is a force balance →
            # ≈ constitutive stress (GPa), dx/n_sub/ρ cancelling.  The TRUE experimental BC.
            # ARM-after-compaction guard (the ONLY robustness add — a median/window stop instead
            # over-compresses universally and inverts the good rSE=1.0 band): a big rigid-AM bed
            # (rSE=0.5) is NOT geometrically jammed at its initial ~56% porosity (AM area ~37% <<
            # 2D jamming ~67%), so the first-contact wall spike there is a TRANSIENT.  Disarm the
            # stop until the bed has actually compacted (por ≤ por0−2) so that transient can't
            # freeze the wall at the initial porosity; the instantaneous stop (which already
            # gives Δ≈−2~−3 in the resolved rSE=1.0 band) is otherwise UNCHANGED.
            got = float('nan'); armed = False
            for fr in range(int(8000 * ng / 320)):
                wall_imp[None] = 0.0
                for _ in range(25): substep()
                top = wall_y[None]
                por = max(0.0, 1.0 - sa / (WIDTH * (top - FLOOR))) * 100
                ws = wall_imp[None] / (25.0 * dt * WIDTH)          # GPa, resolution-invariant
                jam_poro[None] = por
                if por <= por0 - 2.0: armed = True                 # real compaction has begun
                if armed and ws >= pr:
                    got = por; break
                if top <= wall_floor + 1e-4:
                    got = por; break
                if top > wall_floor:
                    servo = min(1.0, max(0.04, (pr - ws) / pr))
                    wall_vf[None] = WALL_V * servo
                    wall_y[None] = max(top - wall_vf[None] * 25 * dt, wall_floor)
            return got
        # ── legacy ABSOLUTE-pressure readout (servo wall) — --heckel diagnostic only.
        #    KEPT to demonstrate the resolution bias; NOT used for the per-case match.
        got = float('nan')
        for fr in range(int(8000 * ng / 320)):
            for _ in range(25): substep()
            Pcur = float(np.mean(prs.to_numpy()[:n])); top = wall_y[None]
            por = max(0.0, 1.0 - sa / (WIDTH * (top - FLOOR))) * 100
            jam_poro[None] = por                          # feed global packing back to jamming yield
            if Pcur >= pr:
                got = por; break
            if Pcur >= P_STOP or top <= wall_floor + 1e-4:
                got = por; break
            if top > wall_floor:
                # servo: full speed while far from target pressure, ramp to a slow
                # crawl as Pcur→pr so the wall settles at equilibrium instead of
                # overshooting to geometric full-pack (the 600-MPa collapse).
                servo = min(1.0, max(0.04, (pr - Pcur) / pr))
                wall_vf[None] = WALL_V * servo
                wall_y[None] = max(top - wall_vf[None] * 25 * dt, wall_floor)
        return got

    # ── Heckel calibration: pure-SE at several pressures → residual porosity ──
    # Verifies the DPC cap BEFORE composites: a correct cap densifies and the
    # porosity drops with pressure toward a residual (target ~Minnmann 10% @ 300).
    if args.heckel:
        _pp = (f"jam_phimin={args.jam_phimin} jam_k={args.jam_k}" if MODEL == 'jam'
               else f"cap_pb0={args.cap_pb0} cap_h={args.cap_h} "
                    f"cap_avpmax={args.cap_avpmax} cap_fric={args.cap_fric}")
        print(f"Heckel (pure-SE) — model={MODEL}, E_se={E_se_base}, {_pp}, n_grid={ng}")
        print(f"  {'P(MPa)':>7s} {'absP%':>8s} {'wallP%':>8s}   "
              f"(absP=mean-prs RESOLUTION-BIASED; wallP=boundary load, resolution-INVARIANT)")

        def _avg(readout, pmpa):
            vals = [run_once(0.006, 0.006, 0.0, 0.0, 1.0, 7000 + i, p_read=pmpa / 1000.0,
                             readout=readout) for i in range(args.seeds)]
            vals = [x for x in vals if x == x]
            return float(np.mean(vals)) if vals else float('nan')

        for pmpa in (100.0, 300.0, 600.0):
            print(f"  {pmpa:7.0f} {_avg('absP', pmpa):8.1f} {_avg('wallP', pmpa):8.1f}", flush=True)
        # self-normalised f50 anchor — resolution-INVARIANT TREND readout (offset cancels)
        fvals = [run_once(0.006, 0.006, 0.0, 0.0, 1.0, 7000 + i, readout='f50')
                 for i in range(args.seeds)]
        fvals = [x for x in fvals if x == x]
        f50 = float(np.mean(fvals)) if fvals else float('nan')
        print(f"  f50 (self-normalised TREND): {f50:5.1f}%", flush=True)
        print(f"  → wallP@300 = ABSOLUTE re-anchor candidate; want 320≈512 ~10-15% "
              f"(Minnmann 300→10%)", flush=True)
        return

    if args.ps_am_grid:
        # ── REAL-value (P:S × AM wt%) porosity grid via the wallP servo (300 MPa, champion SE) ──
        import os as _os
        R_AMP, R_AMS = R_SE_MPM * 12.0, R_SE_MPM * 4.0          # real 12:4:1 size ratio

        def _pf(s):
            if ':' in s:
                pp, qq = s.split(':'); return float(pp) / (float(pp) + float(qq))
            return float(s)
        p_fracs = [_pf(s) for s in args.ps_list]; am_wts = [float(x) for x in args.am_list]
        rho_am, rho_se = 4.8, 2.0
        print(f"REAL (P:S × AM wt%) grid — wallP servo @ {args.p_read} GPa, E_se={E_se_base} "
              f"sigma_y={args.yield_se} nu={args.nu_se}, sizes 12:4:1, n_grid={ng}, seeds={args.seeds}")
        print(f"  {'P:S':>5s} {'AM%':>4s} {'porosity%':>10s} {'±std':>6s}")
        grows = []
        for pf in p_fracs:
            for amwt in am_wts:
                wA = amwt / 100.0
                vA = (wA / rho_am) / ((wA / rho_am) + ((1 - wA) / rho_se)) if 0 < wA < 1 else float(wA >= 1)
                phi_am = INIT_SOLID * vA; phi_se = INIT_SOLID * (1 - vA)
                fAP, fAS, fSE = phi_am * pf, phi_am * (1 - pf), phi_se
                vals = [run_once(R_AMP, R_AMS, fAP, fAS, fSE, 7000 + i, E_se_base, readout='wallP')
                        for i in range(args.seeds)]
                vals = [vv for vv in vals if vv == vv]
                por = float(np.mean(vals)) if vals else float('nan')
                std = float(np.std(vals)) if len(vals) > 1 else 0.0
                p10 = int(round(pf * 10))
                print(f"  {p10:2d}:{10 - p10:<2d} {amwt:4.0f} {por:10.2f} {std:6.2f}", flush=True)
                grows.append((pf, p10, amwt, por, std, len(vals)))
                if args.strain_png_dir:                              # per-point plastic-strain map (last seed)
                    nn = N[None]
                    _strain_png(args.strain_png_dir, p10, amwt, por,
                                x.to_numpy()[:nn], epl.to_numpy()[:nn])
        _os.makedirs(_os.path.dirname(args.grid_csv) or '.', exist_ok=True)
        with open(args.grid_csv, 'w') as f:
            f.write(f"# REAL 2D MPM porosity vs (P:S, AM wt%).  wallP@{args.p_read}GPa E_se={E_se_base} "
                    f"sigma_y={args.yield_se} nu_se={args.nu_se} sizes 12:4:1 n_grid={ng}\n")
            f.write("p_frac,ps_label,am_wt,porosity_pct,porosity_std,n_seed\n")
            for pf, p10, amwt, por, std, ns in grows:
                f.write(f"{pf:.3f},{p10}:{10 - p10},{amwt:.0f},{por:.3f},{std:.3f},{ns}\n")
        print(f"\nwrote {args.grid_csv} ({len(grows)} pts) → plot/fit:\n"
              f"  python3 scripts/mpm2d_ps_am_sweep.py --analyze-only {args.grid_csv}")
        return

    dps = load_design(names=set(args.names) if args.names else None,
                      real_only=args.real_only, particulate=args.particulate,
                      max_n=args.max_n)
    if args.sweep:
        # ── synthetic composition sweep (AM 0→100 at rSE=0.5, P:S=7:3) ──────────
        # Map the Furnas dip vs SE MATERIAL params, to find what SE properties best
        # reproduce the DEM dip — NOT the morphology champion, a best-fit-to-DEM SE
        # model.  Target = DEM corpus medians (rSE≤0.5) binned by AM%.  The dip is a
        # LOCAL MINIMUM; champion soft-plastic SE is monotonic (fills it), stiff/high-
        # yield SE (toward rigid) should restore it — this sweep finds where.
        dem_bins = {}
        for d in dps:
            if d['r_SE'] > 0.5:
                continue
            dem_bins.setdefault(int(d['AM_wt'] // 5) * 5, []).append(d['dem'])
        print(f"composition sweep — rSE=0.5 (12:4:1), P:S=7:3, readout={args.readout}, n_grid={ng}\n"
              f"  SE: E={E_se_base}  sigma_y={args.yield_se}  nu={args.nu_se}  HARD={args.hard_se}")
        print(f"  {'AM%':>4s} {'DEM':>6s} {'MPM':>7s}   (DEM = corpus median rSE<=0.5)")
        R_AMP, R_AMS = R_SE_MPM * 12.0, R_SE_MPM * 4.0
        rho_am, rho_se = 4.8, 2.0
        sweep_rows = []
        for amwt in [0, 20, 40, 55, 62, 70, 75, 80, 85, 90, 95, 100]:
            wA = amwt / 100.0
            vA = (wA / rho_am) / ((wA / rho_am) + ((1 - wA) / rho_se)) if 0 < wA < 1 else float(wA >= 1)
            phi_am = INIT_SOLID * vA; phi_se = INIT_SOLID * (1 - vA)
            fAP, fAS, fSE = phi_am * 0.7, phi_am * 0.3, phi_se
            vals = [run_once(R_AMP, R_AMS, fAP, fAS, fSE, 7000 + i, E_se_base, readout=args.readout)
                    for i in range(args.seeds)]
            vals = [x for x in vals if x == x]
            mpm = float(np.mean(vals)) if vals else float('nan')
            cand = [v for k in dem_bins if abs(k - amwt) <= 5 for v in dem_bins[k]]
            dm = float(np.median(cand)) if cand else float('nan')
            print(f"  {amwt:4.0f} {dm:6.1f} {mpm:7.1f}", flush=True)
            sweep_rows.append((amwt, mpm))
        body = [(a, m) for a, m in sweep_rows if a >= 55 and m == m]
        if len(body) >= 3:
            ams = [b[0] for b in body]; mps = [b[1] for b in body]
            imin = int(np.argmin(mps)); is_dip = 0 < imin < len(mps) - 1
            tag = (f'DIP at AM{ams[imin]} ({mps[imin]:.1f})' if is_dip else 'MONOTONIC (no dip)')
            print(f"  -> MPM {tag};  DEM dips at AM~75", flush=True)
        return
    print(f"matching {len(dps)} DEM design points @ {args.p_read*1000:.0f} MPa, "
          f"n_grid={ng}, seeds={args.seeds}")
    rows = []
    for d in dps:
        R_AMP = R_SE_MPM * d['ratio_P']; R_AMS = R_SE_MPM * d['ratio_S']
        p, s = (int(z) for z in d['PS'].split(':')); tot = p + s
        fAP = d['phi_am'] * p / tot; fAS = d['phi_am'] * s / tot; fSE = d['phi_se']
        # per-case MPM SE modulus.  Default (champion, no cap): same relative
        # perturbation as the DEM E-variant → 1.53·(DEM_E/1.35).  With --e-se
        # (cap cross-check) use the fixed base E for every case instead.
        e_se_mpm = E_se_base if args.e_se else (MPM_E_CHAMPION * d['e_se_gpa'] / DEM_E_BASE)
        vals = [run_once(R_AMP, R_AMS, fAP, fAS, fSE, 7000 + i, e_se_mpm, readout=args.readout)
                for i in range(args.seeds)]
        vals = [x for x in vals if x == x]  # drop nan
        mpm = float(np.mean(vals)) if vals else float('nan')
        std = float(np.std(vals)) if len(vals) > 1 else 0.0
        rows.append((d['name'], d['dem'], mpm, std, d['r_SE'], d['AM_wt'],
                     d['e_se_gpa'], round(e_se_mpm, 3)))
        print(f"  {d['name'][:30]:30s} rSE={d['r_SE']:.2f} AMwt={d['AM_wt']:4.0f} "
              f"E_dem={d['e_se_gpa']:.3f}→E_mpm={e_se_mpm:.2f}  "
              f"DEM={d['dem']:5.1f}%  MPM={mpm:5.1f}±{std:.1f}%  Δ={mpm-d['dem']:+5.1f}",
              flush=True)
    with open(OUT, 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['name', 'dem_porosity', 'mpm_porosity', 'mpm_std', 'r_SE', 'AM_wt',
                    'e_se_gpa', 'e_se_mpm'])
        for r in rows: w.writerow(r)
    import numpy as np  # noqa (already imported above; keep for clarity)
    dems = np.array([r[1] for r in rows]); mpms = np.array([r[2] for r in rows])
    ok = np.isfinite(mpms)
    if ok.sum() >= 2:
        r2 = 1 - np.sum((dems[ok]-mpms[ok])**2)/np.sum((dems[ok]-dems[ok].mean())**2)
        print(f"\n  saved {OUT}  |  DEM↔MPM parity R²(1:1)={r2:.3f}, "
              f"mean|Δ|={np.mean(np.abs(dems[ok]-mpms[ok])):.1f}%p, "
              f"Pearson={np.corrcoef(dems[ok],mpms[ok])[0,1]:.3f}")
        # per-r_SE-band breakdown — the single 1:1 R² is dominated by the big-AM/small-SE
        # (rSE≤0.5) rigid force-chain divergence; partition by SE size to show WHERE the
        # continuum agrees with DEM (rSE≈1.0, pure-SE) vs diverges at the extremes (frame [4]).
        rse = np.array([r[4] for r in rows])
        print(f"  {'band':10s} {'n':>3s} {'meanΔ':>6s} {'mean|Δ|':>7s} {'Pearson':>8s}")
        for lo, hi, lab in [(0.0, 0.75, 'rSE≤0.5'), (0.75, 1.25, 'rSE≈1.0'), (1.25, 9.9, 'rSE≥1.5')]:
            m = ok & (rse >= lo) & (rse < hi)
            if m.sum() == 0:
                continue
            dd, mm = dems[m], mpms[m]
            pear = np.corrcoef(dd, mm)[0, 1] if m.sum() >= 2 else float('nan')
            print(f"  {lab:10s} {m.sum():3d} {np.mean(mm-dd):+6.1f} {np.mean(np.abs(mm-dd)):7.1f} {pear:+8.3f}")


def plot():
    import numpy as np
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    with open(OUT) as fh:
        r = list(csv.DictReader(fh))
    dem = np.array([float(x['dem_porosity']) for x in r])
    mpm = np.array([float(x['mpm_porosity']) for x in r])
    ok = np.isfinite(mpm)
    dem, mpm = dem[ok], mpm[ok]
    fig, ax = plt.subplots(figsize=(5.6, 5.4))
    lo = min(dem.min(), mpm.min()) - 2; hi = max(dem.max(), mpm.max()) + 2
    ax.plot([lo, hi], [lo, hi], 'k--', lw=1, label='1:1')
    ax.scatter(dem, mpm, s=28, c='#c0392b', alpha=0.8)
    r2 = 1 - np.sum((dem-mpm)**2)/np.sum((dem-dem.mean())**2)
    ax.set_xlabel('DEM porosity (%)'); ax.set_ylabel('MPM porosity (%) — champion 1.53/0.15')
    ax.set_title(f'DEM ↔ MPM 1:1 porosity @ 300 MPa\nR²(1:1)={r2:.3f}, '
                 f'Pearson={np.corrcoef(dem,mpm)[0,1]:.3f}, n={len(dem)}', fontsize=10)
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi); ax.set_aspect('equal'); ax.grid(alpha=0.3); ax.legend()
    plt.tight_layout(); os.makedirs(os.path.join(HERE, '..', 'docs', 'figures'), exist_ok=True)
    out = os.path.join(HERE, '..', 'docs', 'figures', 'mpm_dem_match_parity.png')
    plt.savefig(out, dpi=130); print(f"saved {out}")


def group_plot():
    """Trend plot: porosity vs AM wt%, grouped by SE radius, DEM (solid) vs MPM
    (dashed).  Shows whether the DEM size-dependent crossover (small-SE
    descending / large-SE ascending) survives under true-plastic MPM."""
    import numpy as np
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    with open(OUT) as fh:
        r = list(csv.DictReader(fh))
    if not r or 'r_SE' not in r[0]:
        print("CSV has no r_SE/AM_wt columns — re-run the match first (not --plot)."); return
    # group rows by SE radius (size sweep).  Skip non-base-E variants
    # (e_se ≠ 1.35) so the size trend stays clean — the E-sensitivity is a
    # separate axis, read it from the run's printed E_dem→E_mpm lines.
    groups = {}
    for x in r:
        try:
            rse = float(x['r_SE']); amw = float(x['AM_wt'])
            dem = float(x['dem_porosity']); mpm = float(x['mpm_porosity'])
            ese = float(x.get('e_se_gpa') or 1.35)
        except (KeyError, ValueError):
            continue
        if not np.isfinite(mpm) or abs(ese - 1.35) > 1e-3:
            continue
        groups.setdefault(round(rse, 3), []).append((amw, dem, mpm))
    fig, ax = plt.subplots(figsize=(7.6, 5.4))
    cmap = plt.get_cmap('viridis')
    rkeys = sorted(groups)
    for i, rse in enumerate(rkeys):
        pts = sorted(groups[rse])
        amw = [p[0] for p in pts]; dem = [p[1] for p in pts]; mpm = [p[2] for p in pts]
        c = cmap(i / max(len(rkeys) - 1, 1))
        ax.plot(amw, dem, '-o', color=c, lw=2, ms=6, label=f'DEM  r_SE={rse}')
        ax.plot(amw, mpm, '--s', color=c, lw=1.6, ms=6, mfc='none', alpha=0.9,
                label=f'MPM r_SE={rse}')
    ax.set_xlabel('AM wt%'); ax.set_ylabel('Porosity (%)')
    ax.set_title('DEM (solid) vs true-plastic MPM (dashed) porosity\n'
                 'per SE radius — does the size-dependent crossover survive plasticity?',
                 fontsize=10)
    ax.grid(alpha=0.3); ax.legend(fontsize=7, ncol=2)
    plt.tight_layout(); os.makedirs(os.path.join(HERE, '..', 'docs', 'figures'), exist_ok=True)
    out = os.path.join(HERE, '..', 'docs', 'figures', 'mpm_dem_match_trend.png')
    plt.savefig(out, dpi=130); print(f"saved {out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n-grid', type=int, default=320)
    ap.add_argument('--seeds', type=int, default=2)
    ap.add_argument('--real-only', action='store_true')
    ap.add_argument('--particulate', action='store_true',
                    help='only input_particulate_* / input_S_* (monomodal SE-size sweep)')
    ap.add_argument('--max-n', type=int, default=None)
    ap.add_argument('--names', nargs='*', default=None)
    ap.add_argument('--p-read', type=float, default=0.30, help='read pressure GPa (0.30 = 300 MPa)')
    ap.add_argument('--hard-se', type=float, default=10.0,
                    help="SE work-hardening: sigma_y_eff = sigma_y*(1+HARD*eps_pl).  Higher -> SE "
                         "flow stops sooner (floors void-fill) -> raises the SE-rich flank that the "
                         "Furnas dip needs.  Lever for fitting the dip (with --yield-se).")
    ap.add_argument('--sweep', action='store_true',
                    help="synthetic AM 0->100 composition sweep (rSE=0.5, P:S=7:3) vs the DEM dip "
                         "medians -- find SE material params that reproduce the Furnas dip (use with "
                         "--e-se/--yield-se/--nu-se/--hard-se; champion is soft+monotonic).")
    ap.add_argument('--nu-se', type=float, default=0.30,
                    help="SE Poisson ratio.  0.30 = champion (softened E softens BULK too -> "
                         "volumetric over-compaction at SE-rich).  Raise toward ~0.49 to stiffen "
                         "the BULK back to real (volume-preserving granular flow) while keeping "
                         "shear soft -> kills the over-compaction.  >0.47 is near-incompressible "
                         "and may need a smaller dt (watch for NaN/blow-up).")
    ap.add_argument('--readout', choices=['f50', 'wallP', 'absP'], default='f50',
                    help="porosity readout: f50=self-normalised TREND (resolution-invariant, "
                         "reads ~22%% absolute); wallP=boundary-load ABSOLUTE (resolution-invariant, "
                         "servo to wall reaction = p_read); absP=legacy mean-prs (resolution-BIASED)")
    ap.add_argument('--plot', action='store_true', help='parity scatter (DEM vs MPM)')
    ap.add_argument('--group-plot', action='store_true',
                    help='trend: porosity vs AM wt%% per SE radius, DEM vs MPM')
    # ── constitutive model (champion vs cap) ──────────────────────────────
    ap.add_argument('--model', choices=['vonmises', 'dpc', 'jam'], default='vonmises',
                    help="SE plasticity: 'vonmises' (champion J2, no cap) | 'dpc' "
                         "(Drucker-Prager+cap, wrong for resolved grain — see "
                         "docs/mpm_dpc_cap_crosscheck.md) | 'jam' (isochoric "
                         "density-dependent shear yield = correct jamming)")
    ap.add_argument('--e-se', type=float, default=None,
                    help='fixed SE Young modulus GPa (e.g. 24 real bulk); with cap this '
                         'replaces the softened champion. Omit = champion 1.53 + E-variant scaling')
    ap.add_argument('--yield-se', type=float, default=0.15,
                    help='SE von Mises yield GPa (0.15 = champion plastic; 1e4 = RIGID '
                         'bound for the [rigid, plastic] DEM bracket)')
    ap.add_argument('--cap-pb0', type=float, default=0.05,
                    help='DPC initial hydrostatic cap yield p_b0 (GPa) — low → powder '
                         'compacts easily, then hardens')
    ap.add_argument('--cap-h', type=float, default=1.0,
                    help='DPC cap divergence exponent: p_b = p_b0·(avpmax/(avpmax-avp))^cap_h')
    ap.add_argument('--cap-avpmax', type=float, default=0.9,
                    help='DPC residual floor: plastic compaction avp at which p_b diverges '
                         '(≙ φ_min). LOWER → higher residual porosity (main Heckel knob)')
    ap.add_argument('--cap-fric', type=float, default=0.5,
                    help='DPC Drucker-Prager friction: τ_y = σ_y + cap_fric·p')
    ap.add_argument('--jam-phimin', type=float, default=8.0,
                    help='JAM residual porosity floor %% (φ_min) where shear yield diverges')
    ap.add_argument('--jam-k', type=float, default=2.0,
                    help='JAM divergence exponent: σ_y_eff = σ_y/frac^jam_k')
    ap.add_argument('--heckel', action='store_true',
                    help='pure-SE pressure sweep (100/300/600 MPa) to calibrate/verify')
    ap.add_argument('--ps-am-grid', action='store_true',
                    help='REAL-value sweep over the (P:S × AM wt%%) grid via the wallP servo @ --p-read '
                         '(300 MPa) with champion SE → --grid-csv.  Pass --nu-se 0.49 for the stiff-bulk '
                         'champion.  Then plot/fit:  mpm2d_ps_am_sweep.py --analyze-only <csv>.')
    ap.add_argument('--ps-list', nargs='*',
                    default=['0:10', '1:9', '2:8', '3:7', '4:6', '5:5', '6:4', '7:3', '8:2', '9:1', '10:0'])
    ap.add_argument('--am-list', nargs='*', default=['75', '80', '85', '90', '95'])
    ap.add_argument('--grid-csv', default='docs/data/mpm2d_ps_am_porosity.csv')
    ap.add_argument('--strain-png-dir', default='',
                    help='if set, save a per-point plastic-strain map PNG (last seed) for every (P:S, AM%%) '
                         'grid cell into this dir = the "grid of strain images" (negligible extra compute).')
    a = ap.parse_args()
    if a.plot:
        plot(); return
    if a.group_plot:
        group_plot(); return
    run_match(a)


if __name__ == '__main__':
    main()
