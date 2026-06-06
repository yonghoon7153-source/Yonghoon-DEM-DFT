#!/usr/bin/env python3
"""3D MPM compaction (GPU-ready) — soft plastic SE + rigid AM.

True-plastic, large-deformation, GPU-native reference for cathode compaction.
Captures what DEM cannot: particles plastically FLOW into voids (non-spherical),
volume change, conserving material.  von Mises (J2) plasticity per phase:
  • SE : soft (E=24 GPa scaled), low yield  → flows, fills voids.
  • AM : rigid (E=140 GPa scaled), ~no yield → jams.
Confined (oedometer) compaction by a descending rigid wall; porosity measured
as 1 - solid_volume / (box_area · height).

GPU:  edit ARCH='gpu' (Taichi picks CUDA/Vulkan/Metal).  CPU is the safe
fallback for a small smoke test.  Run on a real GPU for full size ratios.

Run:  python3 scripts/mpm3d_compaction.py [n_grid] [arch]
"""
import sys
import numpy as np
import taichi as ti

ARCH = sys.argv[2] if len(sys.argv) > 2 else 'cpu'
ti.init(arch=getattr(ti, ARCH), default_fp=ti.f32, random_seed=1)

n_grid = int(sys.argv[1]) if len(sys.argv) > 1 else 48
dx = 1.0 / n_grid; inv_dx = float(n_grid)
dt = 2.0e-4
p_vol = (dx * 0.5) ** 3; p_mass = p_vol * 1.0
nu = 0.3
def lame(E): return E / (2 * (1 + nu)), E * nu / ((1 + nu) * (1 - 2 * nu))
MU_SE, LA_SE = lame(24.0); MU_AM, LA_AM = lame(140.0)
YIELD_SE = 0.6; YIELD_AM = 1.0e4

FLOOR = 0.10; SW = (0.18, 0.82)        # confined box in x and y
WALL0 = 0.60; WALL_MIN = 0.24; WALL_V = 0.25
R_AM, R_SE = 0.045, 0.022              # qualitative (smoke); raise grid for real 12:4:1
AM_AREA = 0.45                         # fraction of solid that is AM (composition knob)
INIT_SOLID = 0.45

MAXP = 4_000_000
x = ti.Vector.field(3, ti.f32, MAXP); v = ti.Vector.field(3, ti.f32, MAXP)
C = ti.Matrix.field(3, 3, ti.f32, MAXP); F = ti.Matrix.field(3, 3, ti.f32, MAXP)
mu_p = ti.field(ti.f32, MAXP); la_p = ti.field(ti.f32, MAXP); yld_p = ti.field(ti.f32, MAXP)
grid_v = ti.Vector.field(3, ti.f32, (n_grid,) * 3); grid_m = ti.field(ti.f32, (n_grid,) * 3)
wall_z = ti.field(ti.f32, ()); N = ti.field(ti.i32, ())


def build(rng):
    placed = []
    fill_h = WALL0 - 0.03
    box_vol = (SW[1] - SW[0]) ** 2 * (fill_h - FLOOR)
    target = INIT_SOLID * box_vol
    plan = [(R_AM, AM_AREA, MU_AM, LA_AM, YIELD_AM),
            (R_SE, 1 - AM_AREA, MU_SE, LA_SE, YIELD_SE)]
    for (r, frac, mu, la, yld) in plan:
        if frac <= 0: continue
        goal = frac * target; acc = 0.0; tries = 0
        while acc < goal and tries < 200000:
            tries += 1
            c = (rng.uniform(SW[0] + r, SW[1] - r), rng.uniform(SW[0] + r, SW[1] - r),
                 rng.uniform(FLOOR + r, fill_h - r))
            ok = True
            for (px, py, pz, pr, *_ ) in placed:
                if (c[0]-px)**2 + (c[1]-py)**2 + (c[2]-pz)**2 < (r+pr+0.006)**2:
                    ok = False; break
            if ok:
                placed.append((c[0], c[1], c[2], r, mu, la, yld))
                acc += (4/3)*np.pi*r**3
    xs = []; mus = []; las = []; ylds = []
    for (cx, cy, cz, r, mu, la, yld) in placed:
        k = int(r / (dx * 0.5)) + 1
        for a in range(-k, k+1):
            for b in range(-k, k+1):
                for cc in range(-k, k+1):
                    px, py, pz = cx+a*dx*0.5, cy+b*dx*0.5, cz+cc*dx*0.5
                    if (px-cx)**2+(py-cy)**2+(pz-cz)**2 <= r*r:
                        xs.append((px, py, pz)); mus.append(mu); las.append(la); ylds.append(yld)
    return (np.array(xs, np.float32), np.array(mus, np.float32),
            np.array(las, np.float32), np.array(ylds, np.float32))


@ti.kernel
def load(xy: ti.types.ndarray(), mus: ti.types.ndarray(),
         las: ti.types.ndarray(), ylds: ti.types.ndarray(), n: ti.i32):
    N[None] = n
    for p in range(n):
        x[p] = ti.Vector([xy[p, 0], xy[p, 1], xy[p, 2]]); v[p] = ti.Vector([0.0, 0.0, 0.0])
        C[p] = ti.Matrix.zero(ti.f32, 3, 3); F[p] = ti.Matrix.identity(ti.f32, 3)
        mu_p[p] = mus[p]; la_p[p] = las[p]; yld_p[p] = ylds[p]


@ti.kernel
def substep():
    for I in ti.grouped(grid_m):
        grid_v[I] = ti.Vector.zero(ti.f32, 3); grid_m[I] = 0.0
    for p in range(N[None]):
        base = (x[p] * inv_dx - 0.5).cast(int); fx = x[p] * inv_dx - base.cast(ti.f32)
        w = [0.5*(1.5-fx)**2, 0.75-(fx-1.0)**2, 0.5*(fx-0.5)**2]
        U, sig, V = ti.svd(F[p])
        J = sig[0,0]*sig[1,1]*sig[2,2]
        st = (2*mu_p[p]*(F[p]-U@V.transpose())@F[p].transpose()
              + ti.Matrix.identity(ti.f32, 3)*la_p[p]*J*(J-1))
        st = (-dt*p_vol*4*inv_dx*inv_dx)*st; affine = st + p_mass*C[p]
        for a, b, c in ti.static(ti.ndrange(3, 3, 3)):
            off = ti.Vector([a, b, c]); dpos = (off.cast(ti.f32)-fx)*dx
            wt = w[a][0]*w[b][1]*w[c][2]
            grid_v[base+off] += wt*(p_mass*v[p] + affine@dpos)
            grid_m[base+off] += wt*p_mass
    for I in ti.grouped(grid_m):
        if grid_m[I] > 0:
            grid_v[I] /= grid_m[I]
            i, j, k = I[0], I[1], I[2]
            if k*dx < FLOOR and grid_v[I][2] < 0: grid_v[I][2] = 0.0
            if k*dx > wall_z[None]: grid_v[I][2] = ti.min(grid_v[I][2], -WALL_V)
            if i*dx < SW[0] and grid_v[I][0] < 0: grid_v[I][0] = 0.0
            if i*dx > SW[1] and grid_v[I][0] > 0: grid_v[I][0] = 0.0
            if j*dx < SW[0] and grid_v[I][1] < 0: grid_v[I][1] = 0.0
            if j*dx > SW[1] and grid_v[I][1] > 0: grid_v[I][1] = 0.0
    for p in range(N[None]):
        base = (x[p] * inv_dx - 0.5).cast(int); fx = x[p] * inv_dx - base.cast(ti.f32)
        w = [0.5*(1.5-fx)**2, 0.75-(fx-1.0)**2, 0.5*(fx-0.5)**2]
        nv = ti.Vector.zero(ti.f32, 3); nc = ti.Matrix.zero(ti.f32, 3, 3)
        for a, b, c in ti.static(ti.ndrange(3, 3, 3)):
            off = ti.Vector([a, b, c]); dpos = off.cast(ti.f32)-fx
            wt = w[a][0]*w[b][1]*w[c][2]; gv = grid_v[base+off]
            nv += wt*gv; nc += 4*inv_dx*wt*gv.outer_product(dpos)
        v[p] = nv; C[p] = nc; F[p] = (ti.Matrix.identity(ti.f32, 3) + dt*nc) @ F[p]
        U, sig, V = ti.svd(F[p])
        e = ti.Vector([ti.log(ti.max(sig[0,0],1e-4)), ti.log(ti.max(sig[1,1],1e-4)),
                       ti.log(ti.max(sig[2,2],1e-4))])
        tr = (e[0]+e[1]+e[2])/3.0
        d = e - ti.Vector([tr, tr, tr]); dn = d.norm() + 1e-9
        dg = dn - yld_p[p]/(2*mu_p[p])
        if dg > 0:
            e = (d - dg*d/dn) + ti.Vector([tr, tr, tr])
            F[p] = U @ ti.Matrix([[ti.exp(e[0]),0,0],[0,ti.exp(e[1]),0],[0,0,ti.exp(e[2])]]) @ V.transpose()
        x[p] += dt*v[p]


def main():
    rng = np.random.default_rng(3)
    xy, mus, las, ylds = build(rng); n = len(xy)
    print(f"n_grid={n_grid} arch={ARCH} particles(material pts)={n}")
    load(xy, mus, las, ylds, n)
    solid_vol = n * p_vol; area = (SW[1]-SW[0])**2
    wall_z[None] = WALL0
    for frame in range(60):
        for _ in range(40): substep()
        wall_z[None] = max(WALL0 - WALL_V*(frame+1)*40*dt, WALL_MIN)
        top = wall_z[None]
        por = max(0.0, 1.0 - solid_vol/(area*(top-FLOOR)))*100
        if frame % 12 == 0 or frame == 59:
            print(f"  frame {frame:2d}  wall_z={top:.3f}  porosity={por:5.2f}%", flush=True)
    print("3D MPM smoke test OK — extend grid + size ratio on GPU for full runs.")


if __name__ == '__main__':
    main()
