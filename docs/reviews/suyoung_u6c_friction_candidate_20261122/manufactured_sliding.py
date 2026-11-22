"""Check prescribed three-body, sliding-contact solutions at one synthetic node."""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

import numpy as np


MU = 0.5
VELOCITY_TOL = 2e-8  # Native synthetic velocity units; unrelated to pressure criteria.
POSITIONS = np.array([[-0.8, -0.5], [1.2, -0.3], [0.1, 0.9]])
MASSES = np.array([1.0, 1.5, 0.75])
LOADS = np.array([0.26, 0.19, 0.11])


def manufactured(spin):
    # All three pairs touch at this node. A rigid rotation has zero relative
    # normal speed and nonzero tangential speed for each pair of centers.
    outgoing = spin * np.column_stack((-POSITIONS[:, 1], POSITIONS[:, 0]))
    outgoing += np.array([0.37, -0.41])
    normal_rows = []
    impulse_rows = []
    for i, j in itertools.combinations(range(3), 2):
        normal = POSITIONS[j] - POSITIONS[i]
        normal /= np.linalg.norm(normal)
        tangent = np.array([-normal[1], normal[0]])
        relative = outgoing[j] - outgoing[i]
        assert abs(relative @ normal) < 1e-14 and abs(relative @ tangent) > 0.4
        sliding_impulse = normal - MU * np.sign(relative @ tangent) * tangent
        nrow = np.zeros((3, 2))
        irow = np.zeros_like(nrow)
        nrow[i], nrow[j] = -normal, normal
        irow[i], irow[j] = -sliding_impulse, sliding_impulse
        normal_rows.append(nrow.ravel())
        impulse_rows.append(irow.ravel())
    normal_rows = np.array(normal_rows)
    impulse_rows = np.array(impulse_rows)
    mass = np.repeat(MASSES, 2)
    incoming = outgoing.ravel() - (LOADS @ impulse_rows) / mass
    # Solve the three normal-velocity equations on the prescribed sliding
    # branch independently. Positivity checks the sign assumed for each load.
    system = (normal_rows / mass) @ impulse_rows.T
    solved = np.linalg.solve(system, -(normal_rows @ incoming))
    if np.min(solved) <= 0 or np.max(np.abs(solved - LOADS)) > 1e-13:
        raise ArithmeticError("Manufactured sliding branch is inconsistent")
    return incoming.reshape(3, 2), outgoing, float(np.linalg.cond(system))


def evaluate(project, spin):
    incoming, exact, condition = manufactured(spin)
    results = []
    errors = []
    energy0 = 0.5 * np.sum(MASSES[:, None] * incoming**2)
    max_energy_change = float("-inf")
    max_momentum_error = 0.0
    for permutation in itertools.permutations(range(3)):
        ids = np.array(permutation)
        centers = np.empty_like(POSITIONS)
        centers[ids] = POSITIONS
        for rows in (np.array([0, 1, 2]), np.array([2, 1, 0])):
            v = incoming[rows].copy()
            project(ids[rows], np.zeros(3, dtype=int), MASSES[rows],
                    (POSITIONS * MASSES[:, None])[rows], v, centers, MU)
            physical = np.empty_like(v)
            physical[rows] = v
            if not np.isfinite(physical).all():
                raise ArithmeticError("Nonfinite result")
            results.append(physical)
            errors.append(float(np.max(np.linalg.norm(physical - exact, axis=1))))
            max_momentum_error = max(max_momentum_error, float(np.linalg.norm(MASSES @ (physical-incoming))))
            energy = 0.5 * np.sum(MASSES[:, None] * physical**2)
            max_energy_change = max(max_energy_change, float(energy - energy0))
    spread = max(float(np.max(np.linalg.norm(a-b, axis=1)))
                 for a, b in itertools.combinations(results, 2))
    return {"spin": spin, "label_and_storage_orders": len(results), "max_speed_error": max(errors),
            "max_order_spread": spread, "branch_condition_number": condition,
            "max_energy_change": max_energy_change, "max_momentum_error": max_momentum_error,
            "matches": max(errors) <= VELOCITY_TOL and spread <= VELOCITY_TOL and
                       max_momentum_error <= 1e-12 and max_energy_change <= 1e-12}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--kernel", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    spec = importlib.util.spec_from_file_location("tested_sliding_kernel", args.kernel)
    kernel = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kernel)
    records = [evaluate(kernel.project_contacts, spin) for spin in (0.70, -0.85)]
    matched = all(record["matches"] for record in records)
    summary = {"scope": "two manufactured all-sliding branches on a frozen synthetic node",
               "kernel_sha256": hashlib.sha256(args.kernel.read_bytes()).hexdigest(),
               "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "speed_tolerance": VELOCITY_TOL, "normal_impulses": LOADS.tolist(),
               "friction": MU, "matches": matched, "records": records}
    with args.out.open("x", encoding="ascii", newline="\n") as stream:
        stream.write(json.dumps(summary, sort_keys=True, indent=2, allow_nan=False) + "\n")
    print("MATCH" if matched else "MISMATCH", [record["max_speed_error"] for record in records])
    return 0 if matched else 1


if __name__ == "__main__":
    raise SystemExit(main())
