"""Small developer-only nodal exercises for conditioning. No solver time steps."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np


def run(solver):
    rng = np.random.default_rng(61807)
    groups = {}
    for n in (3, 4):
        for lo in (0., 2., 6.):
            label = f"body{n}_log10_mass_range{lo:g}"
            counts = {"ok": 0, "halt": 0, "unchanged_on_halt": 0, "example": None}
            for k in range(12):
                x = rng.uniform(-1., 1., (n, 2))
                m = 10**(-rng.uniform(0., lo, n))
                vin = rng.normal(size=(n, 2))
                vel = vin.copy()
                try:
                    solver.project_contacts(np.arange(n), np.zeros(n, dtype=int),
                                            m, m[:, None]*x, vel, x, .5)
                except ArithmeticError as exc:
                    counts["halt"] += 1
                    counts["unchanged_on_halt"] += bool(np.array_equal(vel, vin))
                    if not counts["example"]:
                        counts["example"] = {
                            "case": k, "cause": str(exc), "x": x.tolist(),
                            "m": m.tolist(), "vin": vin.tolist(),
                        }
                else:
                    counts["ok"] += 1
            groups[label] = counts
    return groups


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--subject", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    spec = importlib.util.spec_from_file_location("candidate", a.subject)
    solver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(solver)
    obs = {"sha256": hashlib.sha256(a.subject.read_bytes()).hexdigest(),
           "seed": 61807, "purpose": "bounded synthetic exercises; arbitrary directions, masses, velocities",
           "groups": run(solver)}
    with a.out.open("x", encoding="ascii", newline="\n") as f:
        json.dump(obs, f, indent=2, sort_keys=True, allow_nan=False)
        f.write("\n")
