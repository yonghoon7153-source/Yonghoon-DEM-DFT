"""One P2G transfer and one pinned floor projection of a free, translating flat slab."""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path

import numpy as np


SOURCES = {
    "dem_suyoung_sf2d_dev.py": "6e8073230f14142f3f802e1fed316bea22610502a98292e2ef794a123ea7e5f4",
    "suyoung_u6_first_dev.py": "5db0f1bda90c824a23479401b7744cf8d31fc64f373441abca692dce6717bda5",
}
FLOOR, X0, WIDTH, THICKNESS = .15, .3, .4, .025
DT, SPEED = .0011231835082397789, .02
GRIDS = (80, 160)


def load_solver(root):
    scripts = root / "scripts"
    for filename, expected in SOURCES.items():
        if hashlib.sha256((scripts / filename).read_bytes()).hexdigest() != expected:
            raise ValueError("Pinned source differs: " + filename)
    spec = importlib.util.spec_from_file_location("gap_native", scripts / "suyoung_u6_first_dev.py")
    solver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(solver)
    if solver.LO != FLOOR or solver.model.RHO != 1.:
        raise ValueError("Floor or density differs")
    return solver


def slab(gap):
    # These common intervals contain the wall-weight spline breakpoints on both grids.
    edges = np.linspace(gap, gap + THICKNESS, 9)
    xi, weights = np.polynomial.legendre.leggauss(2)
    y = FLOOR + (edges[:-1, None] + .5 * np.diff(edges)[:, None] * (xi + 1))
    nx = 64
    x = X0 + (np.arange(nx) + .5) * WIDTH / nx
    xx, yy = np.meshgrid(x, y.ravel())
    area = np.repeat((.5 * np.diff(edges)[:, None] * weights).ravel(), nx) * WIDTH / nx
    return np.column_stack((xx.ravel(), yy.ravel())), area


def analytic_impulse(grid, gap, vy):
    # For t=z/h >= 1/2 only the wall's j=0 row overlaps, with weight
    # (1.5-t)^2/2 up to t=1.5. Horizontal partition of unity removes x.
    h = 1. / grid
    if gap / h < .5:
        raise ValueError("Grid and gap outside this analytic branch")
    lo = max(0., 1.5 - gap / h)
    hi = max(0., 1.5 - (gap + THICKNESS) / h)
    return max(0., -vy) * WIDTH * h * (lo**3 - hi**3) / 6.


def check_close(measured, expected, reason):
    if not math.isclose(measured, expected, rel_tol=1e-12, abs_tol=1e-16):
        raise ArithmeticError(f"{reason}: {measured} != {expected}")


def observe(solver, grid, points, volume, vy, gap):
    nodes, weights, _, _ = solver.model.stencil(points, grid)
    key, inverse = np.unique(nodes.ravel(), return_inverse=True)
    wm = volume[:, None] * weights
    mass = np.bincount(inverse.ravel(), weights=wm.ravel(), minlength=len(key))
    # Uniform velocity, zero affine velocity and zero stress leave this sole P2G term.
    normal_momentum = np.bincount(inverse.ravel(), weights=(wm * vy).ravel(), minlength=len(key))
    xy = np.column_stack(np.divmod(key, grid + 1)) / grid
    vel = np.zeros((len(key), 2))
    np.divide(normal_momentum, mass, out=vel[:, 1], where=mass > 0.)
    mass_total = float(np.sum(mass))
    momentum_before = float(mass @ vel[:, 1])
    impulse = solver.walls(mass, xy, vel, solver.LO + solver.WIDTH, 0.)
    momentum_after = float(mass @ vel[:, 1])
    analytic = analytic_impulse(grid, gap, vy)
    check_close(mass_total, WIDTH * THICKNESS, "mass conservation")
    check_close(momentum_before, WIDTH * THICKNESS * vy, "P2G momentum conservation")
    check_close(momentum_after - momentum_before, impulse, "wall impulse closure")
    check_close(impulse, analytic, "integrated spline wall weight")
    return dict(grid=grid, mass=mass_total, momentum_y_before=momentum_before,
                momentum_y_after=momentum_after, wall_impulse=impulse,
                integrated_spline_impulse=analytic,
                impulse_fraction_of_abs_incoming_momentum=impulse / abs(momentum_before))


def run(root):
    solver = load_solver(root)
    cases = []
    for name, gap, vy in (("down_near", .0125, -SPEED), ("up_near", .0125, SPEED),
                          ("down_far", .025, -SPEED)):
        final_gap = gap + vy * DT
        if min(gap, final_gap) <= 0.:
            raise ValueError("The free trajectory touches the wall")
        points, volume = slab(gap)
        rows = [observe(solver, grid, points, volume, vy, gap) for grid in GRIDS]
        cases.append(dict(case=name, initial_face_gap=gap, free_end_face_gap=final_gap,
                          velocity_y=vy, continuum_wall_impulse=0., grids=rows))
    measured = [r["wall_impulse"] for c in cases for r in c["grids"]]
    check_close(measured[0] / (WIDTH * THICKNESS * SPEED), 1/96, "near/coarse analytic fraction")
    if measured[0] <= 0. or any(value != 0. for value in measured[1:]):
        raise ArithmeticError("Mismatch in expected separating, far, or fine control")
    return dict(label="SYNTHETIC_SINGLE_FLOOR_PROJECTION", units="native box, time, mass and impulse units",
                floor=FLOOR, slab_x=[X0, X0 + WIDTH], thickness=THICKNESS, density=1.,
                points_per_slab=len(points), quadrature="64 horizontal midpoints; two Gauss nodes per depth interval, eight intervals",
                dt_for_free_gap_only=DT, normal_speed=SPEED, physics_sources_sha256=SOURCES,
                assumptions="Unstressed single slab, zero affine velocity, static frictionless floor and lid, no external forces.",
                cases=cases)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = json.dumps(run(args.source_root), indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(data, encoding="ascii")
    else:
        print(data, end="")
