"""Evaluate only the first upper-wall velocity projection on the frozen, undeformed seed."""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path

import numpy as np


SOURCE = {
    "scripts/dem_suyoung_sf2d_dev.py": "6e8073230f14142f3f802e1fed316bea22610502a98292e2ef794a123ea7e5f4",
    "scripts/suyoung_u6_first_dev.py": "5db0f1bda90c824a23479401b7744cf8d31fc64f373441abca692dce6717bda5",
    "scripts/suyoung_u6b_dev.py": "50f1a3aec71b750105852dfec281fc7ca9b84f5d4a594ee8fcc10073d4dba762",
    "docs/reviews/suyoung_floor_contact_20261123/material_floor.py": "4b64bcfe6d0975e3bb18d450cfab77c8c3db750dc06f17965c21c5057f3dd72b",
}


def load(root, name):
    path = root / name
    spec = importlib.util.spec_from_file_location("static_" + path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def evaluate(solver, driver, candidate, cells):
    points, ids, volume = solver.seed(cells)
    grid = round(cells / solver.DIAMETER)
    dt = driver.step_size(solver, cells)
    top_surface = solver.LO + 6.5 * solver.WIDTH / 7 + solver.DIAMETER / 2
    lid = solver.LO + (solver.WIDTH - dt * solver.WALL_SPEED)
    gap = lid - top_surface
    if gap <= 0:
        raise ValueError("the prescribed first lid position intersects the physical seed")
    nodes, weights, _, _ = solver.model.stencil(points, grid)
    nn = (grid + 1) ** 2
    key, slots = np.unique((nodes + ids[:, None] * nn).ravel(), return_inverse=True)
    mass = np.bincount(slots.ravel(), weights=(volume[:, None] * weights).ravel(), minlength=len(key))
    xy = np.column_stack(np.divmod(key % nn, grid + 1)) / grid

    def downward_impulse(where, initial_v):
        gv = np.zeros((len(key), 2))
        gv[:, 1] = initial_v
        candidate._other_walls(solver, xy, gv, where)
        return float(mass @ (initial_v - gv[:, 1]))

    observed = downward_impulse(lid, 0.)
    # Direct particle-weight sum on the eligible vertical support is an independent
    # accumulation of the same nodal mass, prior to any nodal/contact operation.
    w = weights * ((nodes % (grid + 1))/grid >= lid)
    supported_mass = float(np.sum(volume[:, None] * w))
    expected = supported_mass * solver.WALL_SPEED
    far = downward_impulse(lid + 3/grid, 0.)
    separating = downward_impulse(lid, -2*solver.WALL_SPEED)
    if not math.isclose(observed, expected, rel_tol=1e-11, abs_tol=1e-19) or far != 0. or separating != 0.:
        raise ArithmeticError("upper-wall projection controls disagree")
    return dict(cells=cells, native_material_points=len(points), first_step_end_geometric_gap_diameters=gap/solver.DIAMETER,
                initial_gap_diameters=(solver.LO+solver.WIDTH-top_surface)/solver.DIAMETER,
                downward_impulse_code=observed, affected_mass_fraction=supported_mass/float(volume.sum()),
                reconstructed_impulse_code=expected, far_wall_impulse_code=far, separating_impulse_code=separating)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    repo = parser.parse_args().repo.resolve()
    for name, sha in SOURCE.items():
        if hashlib.sha256((repo/name).read_bytes()).hexdigest() != sha:
            raise ValueError("source identity changed: " + name)
    solver = load(repo, "scripts/suyoung_u6_first_dev.py")
    driver = load(repo, "scripts/suyoung_u6b_dev.py")
    material = load(repo, "docs/reviews/suyoung_floor_contact_20261123/material_floor.py")
    print(json.dumps(dict(kind="static_first_projection_only", sources=SOURCE,
                          rows=[evaluate(solver, driver, material, n) for n in (8,12,16,24)]),
                     indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
