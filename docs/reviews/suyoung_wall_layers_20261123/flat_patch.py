"""Manufactured lower-wall stress transfer on a flat slab, without a time step.

The same points and reference volumes are supplied at both resolutions.  With
z the physical distance above a grid-aligned floor and t=z/h, summing the
quadratic spline over all horizontal nodes removes the horizontal coordinate.
At floor nodes j<=0 the normalized first moment is

    K(t) = 4 sum_j (t-j) N(t-j)
         = 1/2 + 3t/2 - 2t^3             for 0<=t<=1/2
         = 2t (3/2-t)^2                  for 1/2<=t<=3/2
         = 0                             for t>=3/2.

Direct polynomial integration gives integral K dt = 29/32 and integral t K dt
= 41/80. Thus a prescribed yy stress -(a+bz) gives the signed pressure
component 10*(a*29/32 + b*h*41/80) MPa under this geometric mask. These are
the MLS stress-term moments. No velocity or unilateral state is evolved.
"""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path

import numpy as np


SOURCES = {
    "scripts/dem_suyoung_sf2d_dev.py": "6e8073230f14142f3f802e1fed316bea22610502a98292e2ef794a123ea7e5f4",
    "docs/reviews/suyoung_wall_cross_projection_20261122/cross.py":
        "d587f32a9e74cfdefcccc97f1c81281168fd26bfdbb74b04ae3b0df5009d57ab",
}
FLOOR = 0.15
WIDTH = 0.4


def load_pinned_sources(source_root):
    modules = []
    for rel, expected in SOURCES.items():
        path = Path(source_root) / rel
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError("source identity differs: " + rel)
        spec = importlib.util.spec_from_file_location(path.stem, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        modules.append(mod)
    return modules


def common_slab():
    # Three-point Gauss quadrature exactly samples the polynomial of degree
    # four in each depth subinterval. All spline breakpoints for g=80 and
    # g=160 are interval boundaries. The 0.025 slab covers both stencils.
    xi, weights = np.polynomial.legendre.leggauss(3)
    dz = 1. / 640.
    depth = (np.arange(16)[:, None] + (xi[None, :] + 1.) / 2.) * dz
    wy = np.broadcast_to(weights * dz / 2., depth.shape).ravel()
    nx = 64
    x = .3 + (np.arange(nx) + .5) * WIDTH / nx
    xx, zz = np.meshgrid(x, depth.ravel())
    pts = np.column_stack((xx.ravel(), FLOOR + zz.ravel()))
    volume = np.repeat(wy, nx) * WIDTH / nx
    return pts, volume, zz.ravel()


def analytic(grid, amplitude, slope):
    return 10. * (amplitude * 29. / 32. + slope * 41. / (80. * grid))


def sample(model, cross, slab, grid, amplitude, slope):
    points, volume, depth = slab
    ids = np.zeros(depth.size, dtype=np.int64)
    state = dict(x=points, ids=ids, volume=volume, yy=-(amplitude + slope * depth),
                 yx=np.zeros_like(depth))
    floor_row = 3 * grid // 20
    # Every geometric floor node, including ones with zero support, field 0.
    keys = [i*(grid+1) + j for i in range(grid+1) for j in range(floor_row+1)]
    observed = cross.totals(cross.project_state(model, state, grid, WIDTH, keys))["stress_MPa"]
    target = analytic(grid, amplitude, slope)
    if not math.isclose(observed, target, rel_tol=1e-12, abs_tol=1e-12):
        raise ValueError(f"flat stress component {observed} differs from analytic {target}")
    return dict(grid=grid, cells_per_diameter=grid//10, h=1./grid,
                measured_MPa=observed, analytic_MPa=target)


def run(source_root):
    model, cross = load_pinned_sources(source_root)
    slab = common_slab()
    rows = []
    for name, slope in (("constant", 0.), ("linear_inward", 8.)):
        pair = [sample(model, cross, slab, g, 1., slope) for g in (80, 160)]
        rows.append(dict(field=name, amplitude=1., slope_per_box_length=slope, samples=pair,
                         measured_delta_MPa=pair[0]["measured_MPa"]-pair[1]["measured_MPa"],
                         analytic_delta_MPa=pair[0]["analytic_MPa"]-pair[1]["analytic_MPa"]))
    return dict(label="SYNTHETIC_GEOMETRIC_MASK_STRESS_TRANSFER", width=WIDTH, floor=FLOOR,
                slab_depth=.025, common_points=len(slab[0]), geometric_mask="all nodes y<=floor",
                moment_zero=29./32., moment_one=41./80., rows=rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parents[3])
    print(json.dumps(run(parser.parse_args().source_root), indent=2, allow_nan=False))
