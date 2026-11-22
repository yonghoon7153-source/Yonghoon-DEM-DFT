"""Small, repeatable one-node conditioning cases. No physical time steps."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np


def exercise(project):
    rng = np.random.default_rng(173411)
    cases = []
    for bodies in (3, 4, 5):
        ids = np.arange(bodies)
        nodes = np.zeros(bodies, dtype=int)
        for log_mass_range in (0, 6, 12):
            for sample in range(40):
                mass = 10. ** -rng.uniform(0., log_mass_range, bodies)
                initial = rng.normal(size=(bodies, 2))
                centers = rng.normal(size=(bodies, 2))
                velocity = initial.copy()
                obs = dict(bodies=bodies, log_mass_range=log_mass_range, sample=sample)
                try:
                    project(ids, nodes, mass, mass[:, None]*centers, velocity, centers, .5)
                except ArithmeticError as exc:
                    if not np.array_equal(velocity, initial):
                        raise AssertionError("Failure modified input") from exc
                    obs.update(status="HALT_INPUT_PRESERVED", diagnostic=str(exc))
                else:
                    if not np.isfinite(velocity).all():
                        raise AssertionError("Nonfinite output")
                    relative = velocity[:, None] - velocity[None, :]
                    direction = centers[None, :] - centers[:, None]
                    i, j = np.triu_indices(bodies, k=1)
                    normal = direction[i, j] / np.linalg.norm(direction[i, j], axis=1)[:, None]
                    closing = np.sum(relative[i, j] * normal, axis=1).max()
                    scale = max(1., np.linalg.norm(initial, axis=1).max())
                    momentum_change = np.linalg.norm(mass @ (velocity-initial))
                    energy_change = np.sum(mass[:, None] * (velocity**2-initial**2)) / 2.
                    if (closing > 1e-9 * scale or momentum_change > 1e-10 * mass.sum() * scale
                            or energy_change > 1e-10 * mass.sum() * scale**2):
                        raise AssertionError("Output sanity check failed")
                    obs.update(status="SOLVED")
                if (bodies, log_mass_range, sample) == (5, 6, 14):
                    state = np.column_stack((mass, centers, initial)).astype("<f8")
                    obs.update(fixed_case_sha256=hashlib.sha256(state.tobytes()).hexdigest(),
                               mass=mass.tolist(), centers=centers.tolist(),
                               initial=initial.tolist(), returned=velocity.tolist())
                cases.append(obs)
    return cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subject", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("one_node_subject", args.subject)
    subject = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(subject)
    cases = exercise(subject.project_contacts)
    solved = sum(r["status"] == "SOLVED" for r in cases)
    report = {"scope": "single synthetic node; no time steps", "seed": 173411,
              "subject_sha256": hashlib.sha256(args.subject.read_bytes()).hexdigest(),
              "source_numpy_version": np.__version__, "solved": solved,
              "halts_with_input_preserved": len(cases)-solved, "cases": cases}
    with args.out.open("x", encoding="ascii", newline="\n") as f:
        json.dump(report, f, sort_keys=True, indent=2, allow_nan=False)
        f.write("\n")
    print(f"solved={solved}/{len(cases)}  atomic_halt={len(cases)-solved}")
    return int(solved != len(cases))


if __name__ == "__main__":
    raise SystemExit(main())
