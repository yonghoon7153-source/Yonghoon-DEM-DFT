"""Compare two bottom-wall operators on the same periodic, pre-stressed flat strip.

No time stepping. A physical material surface sits at z=0, with a uniform
row of markers on material points at that surface. Mass and normal momentum
are scattered from the same positive reference quadrature on each grid.
"""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
import math
from pathlib import Path

import numpy as np


FLOOR, WIDTH, DT = 0.15, 0.4, .0011231835082397789
SOURCE = {
    "suyoung_u6_first_dev.py": "5db0f1bda90c824a23479401b7744cf8d31fc64f373441abca692dce6717bda5",
    "dem_suyoung_sf2d_dev.py": "6e8073230f14142f3f802e1fed316bea22610502a98292e2ef794a123ea7e5f4",
}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def equal(a, b):
    if not math.isclose(a, b, rel_tol=2e-9, abs_tol=2e-11):
        raise ValueError(f"Flat-patch mismatch: {a} vs {b}")


def slab():
    # Gauss–Lobatto of degree five, including the physical lower face. The
    # quadrature pieces split at every spline break of either tested grid.
    nodes = (1. + np.array([-1., -1./math.sqrt(5), 1./math.sqrt(5), 1.])) / 2
    weights = np.array([1., 5., 5., 1.])/12
    dz = 1./320
    zz = ((np.arange(16)[:,None] + nodes[None,:])*dz).ravel()
    unique, inverse = np.unique(zz,return_inverse=True)
    vertical = np.bincount(inverse.ravel(),weights=np.tile(weights*dz,16))
    axis = .30 + np.arange(128)*WIDTH/128
    xx, z = np.meshgrid(axis,unique)
    x = np.column_stack((xx.ravel(), FLOOR+z.ravel()))
    area = np.repeat(vertical, len(axis))*WIDTH/len(axis)
    # Every fine-grid vertex is a surface marker. The same locations are
    # used at both resolutions (not retuned to reduce spread).
    owners = np.arange(0,len(axis),2)
    return x, area, z.ravel(), owners


def exact(grid, slope):
    # I, L, Q are respectively integrals from 0 to infinity of
    # B(j-t), (j-t)B(j-t), t(j-t)B(j-t) for j=-1,0,1. Each is a
    # polynomial integral of the centered quadratic B-spline. Its trace
    # at a surface marker uses N=[1/8,3/4,1/8]. The plane is periodic
    # and invariant in x, so the mass-metric wall solve reduces to one
    # row: -N*v_free / sum(N^2/M). These are impulse/dt/width in MPa.
    F = Fraction
    moments = ((F(1,48),-F(3,128),-F(1,320)),
               (F(1,2),-F(13,64),-F(1,8)),
               (F(47,48),-F(3,128),-F(79,320)))
    weights = (F(1,8),F(3,4),F(1,8))
    inv = sum(n*n/row[0] for n,row in zip(weights,moments))
    coeff = [-4*sum(n*row[k]/row[0] for n,row in zip(weights,moments))/inv for k in (1,2)]
    return float(10*(coeff[0]+coeff[1]*slope/grid))


def sample(solver, candidate, grid, slope):
    x, area, depth, owners = slab()
    ids, weights, _, offsets = solver.model.stencil(x,grid)
    period = round(WIDTH*grid)
    ix, iy = np.divmod(ids,grid+1)
    field_key = ((ix - round(.30*grid)) % period)*(grid+1)+iy
    keys, inv = np.unique(field_key.ravel(),return_inverse=True)
    slots = inv.reshape(weights.shape)
    def scatter(values):
        return np.bincount(slots.ravel(),weights=values.ravel(),minlength=len(keys))
    mass = scatter(area[:,None]*weights)
    # yy = -(1+slope*z); only the stress part of vertical momentum is nonzero.
    dm = 4*grid*grid*DT*area[:,None]*(1+slope*depth[:,None])*weights*offsets[:,:,1]
    mom = scatter(dm)
    v = np.zeros((len(keys),2))
    np.divide(mom,mass,out=v[:,1],where=mass>0)
    ix, iy = np.divmod(keys,grid+1)
    coords = np.column_stack((.30+ix/grid,iy/grid))
    baseline = solver.walls(mass, coords, v.copy(), .9, 0.)/(DT*WIDTH)*10
    equal(baseline,10*(29/32+slope*41/(80*grid)))
    boundary = candidate.MaterialBoundary(owners,x[owners].copy())
    step = boundary.bind(x,weights,offsets,slots,grid,FLOOR,DT)
    old = v.copy()
    impulse = step.project(mass,v)
    measured = impulse/(DT*WIDTH)*10
    equal(measured,exact(grid,slope))
    equal(float(mass @ (v[:,1]-old[:,1])),impulse)
    # Particle and grid impulses agree even when the constrained marker
    # operator spreads impulse across multiple tangential nodes.
    dp = np.sum(area*np.sum(weights*(v[slots,1]-old[slots,1]),axis=1))
    equal(float(dp),impulse)
    return dict(grid=grid,old_wall_MPa=baseline,candidate_wall_MPa=measured,
                analytical_discrete_candidate_MPa=exact(grid,slope),continuum_surface_stress_MPa=10.,
                impulse=impulse,particle_momentum_change=float(dp))


def run(root, candidate_path):
    for name,sha in SOURCE.items():
        if hashlib.sha256((root/"scripts"/name).read_bytes()).hexdigest() != sha:
            raise ValueError("Source mismatch: "+name)
    solver = load("pinned_wall_solver",root/"scripts/suyoung_u6_first_dev.py")
    candidate = load("manufactured_wall_candidate",candidate_path)
    profiles = []
    for name,slope in (("constant",0),("linear_depth",8)):
        rows = [sample(solver,candidate,g,slope) for g in (80,160)]
        profiles.append(dict(name=name,slope=slope,rows=rows,
                             old_grid_gap_MPa=rows[0]["old_wall_MPa"]-rows[1]["old_wall_MPa"],
                             candidate_grid_gap_MPa=rows[0]["candidate_wall_MPa"]-rows[1]["candidate_wall_MPa"]))
    return dict(scope="Synthetic instantaneous static surface; no dense compression arm",profiles=profiles)


if __name__ == "__main__":
    par = argparse.ArgumentParser(description=__doc__)
    par.add_argument("--source-root",required=True,type=Path)
    par.add_argument("--candidate",type=Path,default=Path(__file__).with_name("material_floor.py"))
    a = par.parse_args()
    print(json.dumps(run(a.source_root,a.candidate),indent=2,allow_nan=False))
