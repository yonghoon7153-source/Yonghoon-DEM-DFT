#!/usr/bin/env python3
"""2D MPM compaction of soft ELASTO-PLASTIC disks — true-plastic reference.

Why: our production DEM uses an elastic-softened (hooke/hysteresis) contact
law where particles only OVERLAP at contacts.  A truly plastic material
(von Mises / J2, volume-preserving) instead FLOWS into the voids while
conserving each particle's area.  This 2D MPM shows that mechanism directly:
soft disks arranged with gaps (high porosity) are compressed by a descending
rigid wall; the J2 plastic disks deform and fill the voids, so porosity drops
toward ~0 (limited only by what plasticity allows), conserving total solid area.

Tunable material: E, nu, yield_tau (σ_y).  Two phases supported (soft SE +
rigid AM) via per-particle yield.  Measures porosity vs wall strain and a
pressure proxy (mean particle pressure) → Heckel-style curve.

Run:  python3 scripts/mpm2d_plastic.py
Out:  docs/figures/mpm2d_plastic.png  + printed porosity/pressure series.
"""
import numpy as np
import taichi as ti

ti.init(arch=ti.cpu, default_fp=ti.f32, random_seed=1)

# ── grid / particles ──
n_grid = 128
dx = 1.0 / n_grid
inv_dx = float(n_grid)
dt = 2.0e-4
p_vol = (dx * 0.5) ** 2
p_rho = 1.0
p_mass = p_vol * p_rho

# ── material (soft SE-like) ──
E = 400.0           # Young (arbitrary soft units)
nu = 0.3
mu0 = E / (2 * (1 + nu))
lam0 = E * nu / ((1 + nu) * (1 - 2 * nu))
YIELD = 1.2         # von Mises yield (Hencky deviatoric stress) — low → flows

FLOOR = 0.08        # rigid bottom
WALL_V = 0.18       # wall descent speed (domain/s)

# ── build porous initial config: disks on a lattice with gaps ──
def build_particles():
    pts = []
    r = 0.026
    pitch = 0.072                       # > 2r → gaps → initial porosity
    y0, y1 = FLOOR + 0.02, 0.62
    x0, x1 = 0.16, 0.84
    nx = int((x1 - x0) / pitch)
    ny = int((y1 - y0) / pitch)
    for j in range(ny):
        for i in range(nx):
            cx = x0 + (i + 0.5 * (j % 2)) * pitch
            cy = y0 + j * pitch
            # fill disk with material points
            k = int(r / (dx * 0.5)) + 1
            for a in range(-k, k + 1):
                for b in range(-k, k + 1):
                    px = cx + a * dx * 0.5
                    py = cy + b * dx * 0.5
                    if (px - cx) ** 2 + (py - cy) ** 2 <= r * r:
                        pts.append((px, py))
    return np.array(pts, dtype=np.float32), r, x0, x1

init_xy, R0, XL, XR = build_particles()
n_particles = len(init_xy)
SOLID_AREA = n_particles * p_vol        # conserved (J2 volume-preserving)
WIDTH = XR - XL

x = ti.Vector.field(2, ti.f32, n_particles)
v = ti.Vector.field(2, ti.f32, n_particles)
C = ti.Matrix.field(2, 2, ti.f32, n_particles)
F = ti.Matrix.field(2, 2, ti.f32, n_particles)
Jp = ti.field(ti.f32, n_particles)
press = ti.field(ti.f32, n_particles)     # particle pressure (−trace σ /2)
grid_v = ti.Vector.field(2, ti.f32, (n_grid, n_grid))
grid_m = ti.field(ti.f32, (n_grid, n_grid))
wall_y = ti.field(ti.f32, ())


@ti.kernel
def init():
    for p in range(n_particles):
        F[p] = ti.Matrix.identity(ti.f32, 2)
        v[p] = ti.Vector([0.0, 0.0])
        C[p] = ti.Matrix.zero(ti.f32, 2, 2)
        Jp[p] = 1.0


@ti.kernel
def substep():
    for i, j in grid_m:
        grid_v[i, j] = ti.Vector([0.0, 0.0]); grid_m[i, j] = 0.0
    for p in range(n_particles):
        base = (x[p] * inv_dx - 0.5).cast(int)
        fx = x[p] * inv_dx - base.cast(ti.f32)
        w = [0.5 * (1.5 - fx) ** 2, 0.75 - (fx - 1.0) ** 2, 0.5 * (fx - 0.5) ** 2]
        # elastic stress from F (fixed corotated), J2 plasticity applied in G2P
        U, sig, V = ti.svd(F[p])
        J = sig[0, 0] * sig[1, 1]
        mu = mu0; la = lam0
        stress = (2 * mu * (F[p] - U @ V.transpose()) @ F[p].transpose()
                  + ti.Matrix.identity(ti.f32, 2) * la * J * (J - 1))
        press[p] = -0.5 * (stress[0, 0] + stress[1, 1])
        stress = (-dt * p_vol * 4 * inv_dx * inv_dx) * stress
        affine = stress + p_mass * C[p]
        for a, b in ti.static(ti.ndrange(3, 3)):
            off = ti.Vector([a, b])
            dpos = (off.cast(ti.f32) - fx) * dx
            wt = w[a][0] * w[b][1]
            grid_v[base + off] += wt * (p_mass * v[p] + affine @ dpos)
            grid_m[base + off] += wt * p_mass
    for i, j in grid_m:
        if grid_m[i, j] > 0:
            grid_v[i, j] /= grid_m[i, j]
            # rigid floor (sticky)
            if j * dx < FLOOR and grid_v[i, j][1] < 0:
                grid_v[i, j][1] = 0.0
            # descending rigid wall (pushes down, no penetration above)
            if j * dx > wall_y[None]:
                grid_v[i, j][1] = ti.min(grid_v[i, j][1], -WALL_V)
            # side walls (slip)
            if i * dx < 0.06 and grid_v[i, j][0] < 0: grid_v[i, j][0] = 0.0
            if i * dx > 0.94 and grid_v[i, j][0] > 0: grid_v[i, j][0] = 0.0
    for p in range(n_particles):
        base = (x[p] * inv_dx - 0.5).cast(int)
        fx = x[p] * inv_dx - base.cast(ti.f32)
        w = [0.5 * (1.5 - fx) ** 2, 0.75 - (fx - 1.0) ** 2, 0.5 * (fx - 0.5) ** 2]
        new_v = ti.Vector.zero(ti.f32, 2); new_C = ti.Matrix.zero(ti.f32, 2, 2)
        for a, b in ti.static(ti.ndrange(3, 3)):
            off = ti.Vector([a, b])
            dpos = off.cast(ti.f32) - fx
            wt = w[a][0] * w[b][1]
            gv = grid_v[base + off]
            new_v += wt * gv
            new_C += 4 * inv_dx * wt * gv.outer_product(dpos)
        v[p] = new_v; C[p] = new_C
        F[p] = (ti.Matrix.identity(ti.f32, 2) + dt * new_C) @ F[p]
        # ── von Mises (J2) return mapping in Hencky strain (volume-preserving) ──
        U, sig, V = ti.svd(F[p])
        eps0 = ti.log(ti.max(sig[0, 0], 1e-4))
        eps1 = ti.log(ti.max(sig[1, 1], 1e-4))
        tr = eps0 + eps1
        d0 = eps0 - 0.5 * tr; d1 = eps1 - 0.5 * tr        # deviatoric Hencky
        dnorm = ti.sqrt(d0 * d0 + d1 * d1) + 1e-9
        dgamma = dnorm - YIELD / (2 * mu0)                # yield: 2μ‖dev ε‖ ≤ σ_y
        if dgamma > 0:                                    # plastic flow: scale back
            eps0 = (d0 - dgamma * d0 / dnorm) + 0.5 * tr
            eps1 = (d1 - dgamma * d1 / dnorm) + 0.5 * tr
            F[p] = U @ ti.Matrix([[ti.exp(eps0), 0.0], [0.0, ti.exp(eps1)]]) @ V.transpose()
        x[p] += dt * v[p]


def porosity(top):
    h = top - FLOOR
    return max(0.0, 1.0 - SOLID_AREA / (WIDTH * h)) * 100.0


def main():
    x.from_numpy(init_xy)
    init()
    wall_y[None] = 0.66
    series = []   # (strain%, porosity%, mean_pressure)
    H0 = wall_y[None] - FLOOR
    frames = []
    for frame in range(60):
        for _ in range(60):
            substep()
        wall_y[None] = max(0.66 - WALL_V * (frame + 1) * 60 * dt, FLOOR + 0.12)
        top = wall_y[None]
        strain = (H0 - (top - FLOOR)) / H0 * 100
        por = porosity(top)
        mp = float(np.mean(press.to_numpy()))
        series.append((strain, por, mp))
        if frame % 10 == 0 or frame == 59:
            print(f"  frame {frame:2d}  strain={strain:5.1f}%  porosity={por:5.2f}%  ⟨p⟩={mp:7.2f}")
            frames.append((top, x.to_numpy().copy()))

    # ── plot ──
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    s = np.array(series)
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))
    # initial vs final config
    for k, (lbl, idx) in enumerate([('initial (porous)', 0), ('compacted', -1)]):
        top, xy = frames[0] if k == 0 else frames[-1]
        ax[k].scatter(xy[:, 0], xy[:, 1], s=1.0, c='#c08a0a')
        ax[k].axhline(FLOOR, color='k'); ax[k].axhline(top, color='r')
        ax[k].set_xlim(0, 1); ax[k].set_ylim(0, 0.8); ax[k].set_aspect('equal')
        ax[k].set_title(f"{lbl}  (ε={porosity(top):.1f}%)"); ax[k].axis('off')
    ax[2].plot(s[:, 2], s[:, 1], '-o', ms=3, color='#2e8b57')
    ax[2].set_xlabel('mean particle pressure ⟨p⟩'); ax[2].set_ylabel('porosity ε (%)')
    ax[2].set_title('porosity vs pressure (true-plastic 2D)'); ax[2].grid(alpha=0.3)
    plt.tight_layout()
    import os; os.makedirs('docs/figures', exist_ok=True)
    plt.savefig('docs/figures/mpm2d_plastic.png', dpi=140)
    print("saved docs/figures/mpm2d_plastic.png")
    print(f"n_particles={n_particles}  solid_area={SOLID_AREA:.4f}  "
          f"initial ε={series[0][1]:.1f}%  final ε={series[-1][1]:.1f}%")


if __name__ == '__main__':
    main()
