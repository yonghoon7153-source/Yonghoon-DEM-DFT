"""Relabel a synthetic nodal state and compare projected velocities in physical order."""
import argparse
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path
import platform

import numpy as np


SOURCES = {
    "suyoung_u6_first_dev.py": "5db0f1bda90c824a23479401b7744cf8d31fc64f373441abca692dce6717bda5",
    "dem_suyoung_sf2d_dev.py": "6e8073230f14142f3f802e1fed316bea22610502a98292e2ef794a123ea7e5f4",
}


def load_projection(folder):
    for name, digest in SOURCES.items():
        if hashlib.sha256((folder / name).read_bytes()).hexdigest() != digest:
            raise ValueError("source identity mismatch: " + name)
    spec = importlib.util.spec_from_file_location("fixed_node", folder / "suyoung_u6_first_dev.py")
    solver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(solver)
    return solver.project_contacts


def project(apply, centers, mass, velocity, ids, rows):
    # ids maps physical body -> numerical ID; rows maps stored row -> physical body.
    center_by_id = np.empty_like(centers)
    center_by_id[ids] = centers
    grad = mass[:, None] * centers
    out = velocity[rows].copy()
    apply(ids[rows], np.zeros(len(rows), dtype=int), mass[rows],
          grad[rows], out, center_by_id, 0.5)
    physical = np.empty_like(out)
    physical[rows] = out
    return physical


def measure(apply, positions, masses, velocities):
    centers, mass, velocity = [np.asarray(item, dtype=float)
                               for item in (positions, masses, velocities)]
    rows = np.arange(len(mass))
    incoming_p = np.sum(mass[:, None] * velocity, axis=0)
    energy = lambda v: float(np.sum(mass[:, None] * v**2) / 2)
    incoming_energy = energy(velocity)
    speed = max(float(np.linalg.norm(velocity[a] - velocity[b]))
                for a, b in itertools.combinations(rows, 2))
    records, results = [], []
    max_momentum_error = 0.
    max_row_change = 0.
    for labels in itertools.permutations(range(len(mass))):
        ids = np.array(labels)
        out = project(apply, centers, mass, velocity, ids, rows)
        reversed_rows = project(apply, centers, mass, velocity, ids, rows[::-1])
        max_row_change = max(max_row_change, float(np.max(np.abs(out-reversed_rows))))
        max_momentum_error = max(max_momentum_error, float(np.linalg.norm(
            np.sum(mass[:, None] * out, axis=0) - incoming_p)))
        records.append({"physical_to_id": list(labels), "velocity_by_physical_body": out.tolist(),
                        "outgoing_energy": energy(out)})
        results.append(out)
    distance, a, b, body = max(
        (float(np.linalg.norm(results[i][k]-results[j][k])), i, j, k)
        for i,j in itertools.combinations(range(len(results)), 2) for k in range(len(mass)))
    return {
        "positions_and_gradient_per_mass": centers.tolist(), "mass": mass.tolist(),
        "incoming_velocity": velocity.tolist(), "incoming_max_relative_speed": speed,
        "incoming_energy": incoming_energy, "id_results": records,
        "max_velocity_difference": distance, "max_difference_over_incoming_relative_speed": distance/speed,
        "worst_pair_ids": [records[i]["physical_to_id"] for i in (a,b)], "worst_physical_body": int(body),
        "max_row_reversal_component_difference": max_row_change,
        "max_linear_momentum_abs_error": max_momentum_error,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--scripts", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    apply = load_projection(args.scripts)
    triangle = [(1., 0.), (-.5, math.sqrt(3.)/2), (-.5, -math.sqrt(3.)/2)]
    cases = {
        "two_body_control": ([(-1,0),(1,0)], [1,1.5], [(1,.1),(-.8,.4)]),
        "symmetric_triangle": (triangle, [1,1,1], [(-x,-y) for x,y in triangle]),
        "asymmetric_triangle": ([(-.8,-.5),(1.2,-.3),(.1,.9)], [1,1.5,.75],
                                [(.9,.3),(-.6,.1),(.25,-.8)]),
    }
    data = {"scope": "synthetic single-node impulse projection only", "friction": .5,
            "multi_body_sweeps": 4, "source_sha256": SOURCES,
            "python": platform.python_version(), "numpy": np.__version__,
            "cases": {key: measure(apply,*case) for key,case in cases.items()}}
    for result in data["cases"].values():
        if result["max_row_reversal_component_difference"] != 0:
            raise ArithmeticError("storage-row control failed")
        if result["max_linear_momentum_abs_error"] > 1e-12:
            raise ArithmeticError("momentum sanity check")
        if max(row["outgoing_energy"] for row in result["id_results"]) > result["incoming_energy"] + 1e-12:
            raise ArithmeticError("energy sanity check")
    if data["cases"]["two_body_control"]["max_velocity_difference"] > 1e-12:
        raise ArithmeticError("two-body control failed")
    with args.out.open("x", encoding="ascii", newline="\n") as out:
        json.dump(data, out, indent=2, sort_keys=True, allow_nan=False)
        out.write("\n")


if __name__ == "__main__":
    main()
