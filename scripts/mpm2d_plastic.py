#!/usr/bin/env python3
"""2D MPM confined compaction of soft ELASTO-PLASTIC disks — true-plastic ref.

Independent check of the DEM densification picture.  Our production DEM is
elastic-softened (hooke/hysteresis): particles only OVERLAP at contacts.  A
truly plastic material (von Mises / J2, volume-preserving) instead FLOWS into
the voids, conserving each particle's area.  This confined (oedometer) 2D MPM
shows it: soft disks with initial porosity are pressed by a descending rigid
wall between fixed side walls; the J2 disks plastically flow to fill voids, so
porosity drops toward ~0 while solid area is conserved, and the wall pressure
stays low until the voids are gone then rises sharply (Heckel-like).

Run:  python3 scripts/mpm2d_plastic.py
Out:  docs/figures/mpm2d_plastic.png + printed porosity/pressure series.
"""
import numpy as np
import taichi as ti

ti.init(arch=ti.cpu, default_fp=ti.f32, random_seed=1)

n_grid = 128
dx = 1.0 / n_grid
inv_dx = float(n_grid)
dt = 2.0e-4
p_vol = (dx * 0.5) ** 2
p_mass = p_vol * 1.0

E = 600.0; nu = 0.3
mu0 = E / (2 * (1 + nu))
lam0 = E * nu / ((1 + nu) * (1 - 2 * nu))
YIELD = 4.0                 # von Mises yield (Kirchhoff dev) — low → plastic flow

FLOOR = 0.08
SW_L, SW_R = 0.16, 0.84     # fixed side walls (confined / oedometer)
WIDTH = SW_R - SW_L
WALL_TOP0 = 0.62
WALL_MIN = 0.30
WALL_V = 0.20


def build_particles():
    pts = []; r = 0.026; pitch = 0.070
    y0, y1 = FLOOR + 0.02, 0.58
    x0, x1 = SW_L + 0.02, SW_R - 0.02
    nx = int((x1 - x0) / pitch); ny = int((y1 - y0) / pitch)
    for j in range(ny):
        for i in range(nx):
            cx = x0 + (i + 0.5 * (j % 2)) * pitch
            cy = y0 + j * pitch
            if cx < SW_L + r or cx > SW_R - r: continue
            k = int(r / (dx * 0.5)) + 1
            for a in range(-k, k + 1):
                for b in range(-k, k + 1):
                    px = cx + a * dx * 0.5; py = cy + b * dx * 0.5
                    if (px - cx) ** 2 + (py - cy) ** 2 <= r * r:
                        pts.append((px, py))
    return np.array(pts, dtype=np.float32)

init_xy = build_particles()
n_particles = len(init_xy)
SOLID_AREA = n_particles * p_vol

x = ti.Vector.field(2, ti.f32, n_particles)
v = ti.Vector.field(2, ti.f32, n_particles)
C = ti.Matrix.field(2, 2, ti.f32, n_particles)
F = ti.Matrix.field(2, 2, ti.f32, n_particles)
press = ti.field(ti.f32, n_particles)
grid_v = ti.Vector.field(2, ti.f32, (n_grid, n_grid))
grid_m = ti.field(ti.f32, (n_grid, n_grid))
wall_y = ti.field(ti.f32, ())


@ti.kernel
def init():
    for p in range(n_particles):
        F[p] = ti.Matrix.identity(ti.f32, 2)
        v[p] = ti.Vector([0.0, 0.0]); C[p] = ti.Matrix.zero(ti.f32, 2, 2)


@ti.kernel
def substep():
    for i, j in grid_m:
        grid_v[i, j] = ti.Vector([0.0, 0.0]); grid_m[i, j] = 0.0
    for p in range(n_particles):
        base = (x[p] * inv_dx - 0.5).cast(int)
        fx = x[p] * inv_dx - base.cast(ti.f32)
        w = [0.5 * (1.5 - fx) ** 2, 0.75 - (fx - 1.0) ** 2, 0.5 * (fx - 0.5) ** 2]
        U, sig, V = ti.svd(F[p])
        J = sig[0, 0] * sig[1, 1]
        stress = (2 * mu0 * (F[p] - U @ V.transpose()) @ F[p].transpose()
                  + ti.Matrix.identity(ti.f32, 2) * lam0 * J * (J - 1))
        press[p] = -0.5 * (stress[0, 0] + stress[1, 1])
        stress = (-dt * p_vol * 4 * inv_dx * inv_dx) * stress
        affine = stress + p_mass * C[p]
        for a, b in ti.static(ti.ndrange(3, 3)):
            off = ti.Vector([a, b]); dpos = (off.cast(ti.f32) - fx) * dx
            wt = w[a][0] * w[b][1]
            grid_v[base + off] += wt * (p_mass * v[p] + affine @ dpos)
            grid_m[base + off] += wt * p_mass
    for i, j in grid_m:
        if grid_m[i, j] > 0:
            grid_v[i, j] /= grid_m[i, j]
            if j * dx < FLOOR and grid_v[i, j][1] < 0: grid_v[i, j][1] = 0.0
            if j * dx > wall_y[None]: grid_v[i, j][1] = ti.min(grid_v[i, j][1], -WALL_V)
            if i * dx < SW_L and grid_v[i, j][0] < 0: grid_v[i, j][0] = 0.0
            if i * dx > SW_R and grid_v[i, j][0] > 0: grid_v[i, j][0] = 0.0
    for p in range(n_particles):
        base = (x[p] * inv_dx - 0.5).cast(int)
        fx = x[p] * inv_dx - base.cast(ti.f32)
        w = [0.5 * (1.5 - fx) ** 2, 0.75 - (fx - 1.0) ** 2, 0.5 * (fx - 0.5) ** 2]
        new_v = ti.Vector.zero(ti.f32, 2); new_C = ti.Matrix.zero(ti.f32, 2, 2)
        for a, b in ti.static(ti.ndrange(3, 3)):
            off = ti.Vector([a, b]); dpos = off.cast(ti.f32) - fx
            wt = w[a][0] * w[b][1]; gv = grid_v[base + off]
            new_v += wt * gv; new_C += 4 * inv_dx * wt * gv.outer_product(dpos)
        v[p] = new_v; C[p] = new_C
        F[p] = (ti.Matrix.identity(ti.f32, 2) + dt * new_C) @ F[p]
        U, sig, V = ti.svd(F[p])
        e0 = ti.log(ti.max(sig[0, 0], 1e-4)); e1 = ti.log(ti.max(sig[1, 1], 1e-4))
        tr = e0 + e1; d0 = e0 - 0.5 * tr; d1 = e1 - 0.5 * tr
        dn = ti.sqrt(d0 * d0 + d1 * d1) + 1e-9
        dg = dn - YIELD / (2 * mu0)
        if dg > 0:
            n0 = (d0 - dg * d0 / dn) + 0.5 * tr; n1 = (d1 - dg * d1 / dn) + 0.5 * tr
            F[p] = U @ ti.Matrix([[ti.exp(n0), 0.0], [0.0, ti.exp(n1)]]) @ V.transpose()
        x[p] += dt * v[p]


def porosity(top):
    return max(0.0, 1.0 - SOLID_AREA / (WIDTH * (top - FLOOR))) * 100.0


def main():
    x.from_numpy(init_xy); init()
    wall_y[None] = WALL_TOP0
    H0 = WALL_TOP0 - FLOOR
    sub = 80; nframe = 110
    series = []; snaps = []
    for frame in range(nframe):
        for _ in range(sub):
            substep()
        wall_y[None] = max(WALL_TOP0 - WALL_V * (frame + 1) * sub * dt, WALL_MIN)
        top = wall_y[None]
        strain = (H0 - (top - FLOOR)) / H0 * 100
        por = porosity(top)
        pr = float(np.mean(press.to_numpy()))
        series.append((strain, por, pr))
        if frame in (0, nframe // 2, nframe - 1):
            snaps.append((top, x.to_numpy().copy(), por))
        if frame % 15 == 0 or frame == nframe - 1:
            print(f"  frame {frame:3d}  strain={strain:5.1f}%  porosity={por:5.2f}%  ⟨p⟩={pr:8.3f}")

    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    s = np.array(series)
    fig, ax = plt.subplots(1, 4, figsize=(15.5, 3.9))
    for k, (top, xy, por) in enumerate(snaps):
        ax[k].scatter(xy[:, 0], xy[:, 1], s=0.6, c='#c08a0a')
        ax[k].axhline(FLOOR, color='k', lw=1); ax[k].axhline(top, color='r', lw=1.5)
        ax[k].axvline(SW_L, color='gray', lw=0.8); ax[k].axvline(SW_R, color='gray', lw=0.8)
        ax[k].set_xlim(0.1, 0.9); ax[k].set_ylim(0, 0.7); ax[k].set_aspect('equal')
        ax[k].set_title(['initial', 'mid', 'compacted'][k] + f"  ε={por:.1f}%", fontsize=10)
        ax[k].axis('off')
    ax[3].plot(s[:, 2], s[:, 1], '-o', ms=2.5, color='#2e8b57')
    ax[3].set_xlabel('wall pressure ⟨p⟩'); ax[3].set_ylabel('porosity ε (%)')
    ax[3].set_title('porosity vs pressure', fontsize=10); ax[3].grid(alpha=0.3)
    plt.tight_layout()
    import os; os.makedirs('docs/figures', exist_ok=True)
    plt.savefig('docs/figures/mpm2d_plastic.png', dpi=110)
    print("saved docs/figures/mpm2d_plastic.png")
    print(f"n_particles={n_particles}  solid_area={SOLID_AREA:.4f}  WIDTH={WIDTH:.3f}  "
          f"initial ε={series[0][1]:.1f}%  final ε={series[-1][1]:.1f}%")


if __name__ == '__main__':
    main()
