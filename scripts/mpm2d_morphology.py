#!/usr/bin/env python3
"""(가) champion 2D MPM — MORPHOLOGY snapshots of LPSCl compaction.

Self-contained depiction of "real LPSCl 2D compaction behaviour": resolved
grains (AM_P 12 : AM_S 4 : SE 1) compressed by a servo wall, SE = champion
softened-J2 plastic (E=1.53/σ_y=0.15, work-hardening), AM rigid.  Saves three
snapshots (loose → mid → compacted) with particles coloured by accumulated
plastic strain Σdg → shows core-preserved + boundary-flattening (the SEM match).

Run (uma GPU):  python3 mpm2d_morphology.py [n_grid=320] [arch=gpu] [AM=82] [P:S=7:3]
  e.g. sharp:   python3 mpm2d_morphology.py 512 gpu 82 7:3
Out: mpm2d_morphology_AM<am>_n<grid>.png

Companion to scripts/mpm2d_PS_pressure.py (porosity) and the dip tools.
"""
import sys
import numpy as np
import taichi as ti

n_grid = int(sys.argv[1]) if len(sys.argv) > 1 else 320
ARCH   = sys.argv[2] if len(sys.argv) > 2 else 'gpu'
AM_WT  = float(sys.argv[3]) if len(sys.argv) > 3 else 82.0
PS     = sys.argv[4] if len(sys.argv) > 4 else '7:3'
PP, SS = (int(z) for z in PS.split(':'))
ti.init(arch=getattr(ti, ARCH), default_fp=ti.f32, random_seed=7)

dx = 1.0 / n_grid; inv_dx = float(n_grid); dt = 8.0e-5 * 320.0 / n_grid
p_vol = (dx * 0.5) ** 2
NU_SE = float(sys.argv[5]) if len(sys.argv) > 5 else 0.30   # 0.30 champion; ~0.49 stiff-bulk porosity-fit (does SEM morphology still hold?)
def lame(E, nu): return E / (2 * (1 + nu)), E * nu / ((1 + nu) * (1 - 2 * nu))
MU_SE, LA_SE = lame(1.53, NU_SE); MU_AM, LA_AM = lame(140.0, 0.25)
YIELD_SE = 0.15; YIELD_AM = 1.0e4; HARD_SE = 10.0; RHO_AM, RHO_SE = 4.8, 2.0
FLOOR = 0.08; SW_L, SW_R = 0.08, 0.92; WIDTH = SW_R - SW_L
WALL0 = 0.66; WALL_MIN = 0.05; WALL_V = 0.18
R_AMP, R_AMS, R_SE = 0.072, 0.024, 0.006; INIT_SOLID = 0.50

MAXP = 2_000_000
x = ti.Vector.field(2, ti.f32, MAXP); v = ti.Vector.field(2, ti.f32, MAXP)
C = ti.Matrix.field(2, 2, ti.f32, MAXP); F = ti.Matrix.field(2, 2, ti.f32, MAXP)
mu_p = ti.field(ti.f32, MAXP); la_p = ti.field(ti.f32, MAXP); yld_p = ti.field(ti.f32, MAXP)
m_p = ti.field(ti.f32, MAXP); epl = ti.field(ti.f32, MAXP)
grid_v = ti.Vector.field(2, ti.f32, (n_grid, n_grid)); grid_m = ti.field(ti.f32, (n_grid, n_grid))
wall_y = ti.field(ti.f32, ()); N = ti.field(ti.i32, ())


def fracs(am_wt, pp, ss):
    w = am_wt / 100.0
    if w <= 0: vam = 0.0
    elif w >= 1: vam = 1.0
    else:
        a = w / RHO_AM; b = (1 - w) / RHO_SE; vam = a / (a + b)
    tot = pp + ss
    return (pp / tot) * vam, (ss / tot) * vam, 1.0 - vam


def build(am, pp, ss, rng):
    fAP, fAS, fSE = fracs(am, pp, ss)
    fill_h = WALL0 - 0.02; box = WIDTH * (fill_h - FLOOR); target = INIT_SOLID * box
    placed = []; cell = R_AMP * 1.05; H = {}
    def clash(cx, cy, r):
        ci, cj = int(cx / cell), int(cy / cell)
        for di in (-2, -1, 0, 1, 2):
            for dj in (-2, -1, 0, 1, 2):
                for (px, py, pr) in H.get((ci + di, cj + dj), []):
                    if (cx - px) ** 2 + (cy - py) ** 2 < (r + pr + 0.0015) ** 2: return True
        return False
    def add(cx, cy, r, mu, la, yld, rho, ph):
        placed.append((cx, cy, r, mu, la, yld, rho, ph))
        H.setdefault((int(cx / cell), int(cy / cell)), []).append((cx, cy, r))
    plan = [(R_AMP, fAP, MU_AM, LA_AM, YIELD_AM, RHO_AM, 0),
            (R_AMS, fAS, MU_AM, LA_AM, YIELD_AM, RHO_AM, 1),
            (R_SE,  fSE, MU_SE, LA_SE, YIELD_SE, RHO_SE, 2)]
    for (r, frac, mu, la, yld, rho, ph) in plan:
        if frac <= 1e-6: continue
        goal = frac * target; acc = 0.0; t = 0
        while acc < goal and t < 800000:
            t += 1; cx = rng.uniform(SW_L + r, SW_R - r); cy = rng.uniform(FLOOR + r, fill_h - r)
            if not clash(cx, cy, r): add(cx, cy, r, mu, la, yld, rho, ph); acc += np.pi * r * r
    xs = []; mu = []; la = []; yl = []; ms = []; phs = []
    for (cx, cy, r, mm, ll, yy, rho, ph) in placed:
        k = int(r / (dx * 0.5)) + 1
        for a in range(-k, k + 1):
            for b in range(-k, k + 1):
                px, py = cx + a * dx * 0.5, cy + b * dx * 0.5
                if (px - cx) ** 2 + (py - cy) ** 2 <= r * r:
                    xs.append((px, py)); mu.append(mm); la.append(ll); yl.append(yy)
                    ms.append(p_vol * rho); phs.append(ph)
    return (np.array(xs, np.float32), np.array(mu, np.float32), np.array(la, np.float32),
            np.array(yl, np.float32), np.array(ms, np.float32), np.array(phs, np.int32))


@ti.kernel
def load(xy: ti.types.ndarray(), mu: ti.types.ndarray(), la: ti.types.ndarray(),
         yl: ti.types.ndarray(), ms: ti.types.ndarray(), n: ti.i32):
    N[None] = n
    for p in range(n):
        x[p] = ti.Vector([xy[p, 0], xy[p, 1]]); v[p] = ti.Vector([0.0, 0.0])
        C[p] = ti.Matrix.zero(ti.f32, 2, 2); F[p] = ti.Matrix.identity(ti.f32, 2)
        mu_p[p] = mu[p]; la_p[p] = la[p]; yld_p[p] = yl[p]; m_p[p] = ms[p]; epl[p] = 0.0


@ti.kernel
def substep():
    for I in ti.grouped(grid_m):
        grid_v[I] = ti.Vector.zero(ti.f32, 2); grid_m[I] = 0.0
    for p in range(N[None]):
        base = (x[p] * inv_dx - 0.5).cast(int); fx = x[p] * inv_dx - base.cast(ti.f32)
        w = [0.5 * (1.5 - fx) ** 2, 0.75 - (fx - 1.0) ** 2, 0.5 * (fx - 0.5) ** 2]
        U, sig, V = ti.svd(F[p]); J = sig[0, 0] * sig[1, 1]
        st = (2 * mu_p[p] * (F[p] - U @ V.transpose()) @ F[p].transpose()
              + ti.Matrix.identity(ti.f32, 2) * la_p[p] * J * (J - 1))
        st = (-dt * p_vol * 4 * inv_dx * inv_dx) * st; aff = st + m_p[p] * C[p]
        for a, b in ti.static(ti.ndrange(3, 3)):
            off = ti.Vector([a, b]); dpos = (off.cast(ti.f32) - fx) * dx; wt = w[a][0] * w[b][1]
            grid_v[base + off] += wt * (m_p[p] * v[p] + aff @ dpos); grid_m[base + off] += wt * m_p[p]
    for I in ti.grouped(grid_m):
        if grid_m[I] > 0:
            grid_v[I] /= grid_m[I]; i, j = I[0], I[1]
            if j * dx < FLOOR and grid_v[I][1] < 0: grid_v[I][1] = 0.0
            if j * dx > wall_y[None]: grid_v[I][1] = ti.min(grid_v[I][1], -WALL_V)
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
        dg = dn - (yld_p[p] * (1.0 + HARD_SE * epl[p])) / (2 * mu_p[p])
        if dg > 0:
            epl[p] += dg
            m0 = (d0 - dg * d0 / dn) + 0.5 * tr; m1 = (d1 - dg * d1 / dn) + 0.5 * tr
            F[p] = U @ ti.Matrix([[ti.exp(m0), 0.0], [0.0, ti.exp(m1)]]) @ V.transpose()
        x[p] += dt * v[p]


def main():
    rng = np.random.default_rng(7)
    xy, mu, la, yl, ms, ph = build(AM_WT, PP, SS, rng); n = len(xy); sa = n * p_vol
    print(f"n_grid={n_grid} AM={AM_WT}wt% P:S={PP}:{SS}  material_pts={n}", flush=True)
    load(xy, mu, la, yl, ms, n); wall_y[None] = WALL0
    top_full = FLOOR + sa / WIDTH; wall_floor = top_full + 0.002
    snaps = []; snap_por = [0.40, 0.22]; taken = [False, False]
    for fr in range(int(9000 * n_grid / 320)):
        for _ in range(25): substep()
        top = wall_y[None]; por = max(0.0, 1.0 - sa / (WIDTH * (top - FLOOR)))
        for si, tp in enumerate(snap_por):
            if not taken[si] and por <= tp:
                snaps.append((por, x.to_numpy()[:n].copy(), epl.to_numpy()[:n].copy())); taken[si] = True
        if top <= wall_floor + 1e-4: break
        if top > wall_floor: wall_y[None] = max(top - WALL_V * 25 * dt, wall_floor)
    snaps.insert(0, (INIT_SOLID, None, None))  # placeholder for initial
    snaps[0] = (1.0 - INIT_SOLID, xy.copy(), np.zeros(n))   # initial (loose)
    snaps.append((por, x.to_numpy()[:n].copy(), epl.to_numpy()[:n].copy()))  # final

    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, len(snaps), figsize=(4.6 * len(snaps), 4.4))
    axs = np.atleast_1d(axs)
    se_all = ph == 2
    vmax = max(1e-3, float(np.percentile(snaps[-1][2][se_all], 98)))
    labels = ['loose', 'mid', 'dense', 'final']
    for k, (por, xpos, ep) in enumerate(snaps):
        ax = axs[k]
        am_m = ph == 0; ams_m = ph == 1; se_m = ph == 2
        # AM grey skeleton, SE coloured by plastic strain
        ax.scatter(xpos[am_m, 0], xpos[am_m, 1], s=0.5, c='#888888')
        ax.scatter(xpos[ams_m, 0], xpos[ams_m, 1], s=0.5, c='#bbbbbb')
        sc = ax.scatter(xpos[se_m, 0], xpos[se_m, 1], s=0.5, c=ep[se_m], cmap='hot', vmin=0, vmax=vmax)
        ax.set_xlim(SW_L - 0.02, SW_R + 0.02); ax.set_ylim(FLOOR - 0.02, WALL0)
        ax.set_aspect('equal'); ax.axis('off')
        lab = labels[k] if k < len(labels) else f'snap{k}'
        ax.set_title(f'{lab}\nporosity {por*100:.0f}%', fontsize=10)
    fig.colorbar(sc, ax=axs.tolist(), shrink=0.7, label='SE accumulated plastic strain Σdg')
    fig.suptitle(f'champion MPM morphology (line-ga) — AM {AM_WT:.0f}wt% P:S {PP}:{SS}, '
                 f'E=1.53/sy=0.15/nu={NU_SE} (n_grid={n_grid})\n'
                 'AM rigid (grey) - SE plastic (hot=more flow) -> core-preserved + boundary-flattening',
                 fontsize=11)
    out = f'mpm2d_morphology_AM{int(AM_WT)}_n{n_grid}_nu{NU_SE:.2f}.png'
    plt.savefig(out, dpi=130, bbox_inches='tight'); print(f"saved {out}", flush=True)


if __name__ == '__main__':
    main()
