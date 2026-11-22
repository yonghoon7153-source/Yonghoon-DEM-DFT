"""Report physical-body spreads and residual closing speeds for historical nodes."""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

import numpy as np


def load(path):
    spec = importlib.util.spec_from_file_location("nodal_subject", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.project_contacts


def measure(project, case, mu):
    x, m, vel = [np.asarray(case[key], dtype=float) for key in
                 ("positions_and_gradient_per_mass", "mass", "incoming_velocity")]
    pairs = list(itertools.combinations(range(len(m)), 2))
    max_speed = max(np.linalg.norm(vel[i]-vel[j]) for i, j in pairs)
    normal = [(x[j]-x[i])/np.linalg.norm(x[j]-x[i]) for i, j in pairs]
    out = []
    closing = 0.
    for perm in itertools.permutations(range(len(m))):
        ids = np.asarray(perm)
        centers = np.empty_like(x)
        centers[ids] = x
        trial = vel.copy()
        project(ids, np.full(len(m), 17), m, m[:, None]*x, trial, centers, mu)
        out.append(trial)
        closing = max(closing, *(float((trial[i]-trial[j]) @ n)
                                 for (i, j), n in zip(pairs, normal)))
    spread = max(float(np.linalg.norm(a-b, axis=1).max())
                 for a, b in itertools.combinations(out, 2))
    return {"permutations": len(out), "same_body_max_speed_difference": spread,
            "incoming_max_relative_speed": float(max_speed),
            "max_residual_closing_speed": closing,
            "max_residual_closing_over_incoming_max_relative_speed": float(closing/max_speed)}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--subject", type=Path, required=True)
    p.add_argument("--fixtures", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    raw = a.fixtures.read_bytes()
    if hashlib.sha256(raw).hexdigest() != "d8eccd805f0a51a66b33b95ad7b12ae8480378c6cf8e98e93fecdf7eba6e0cc6":
        raise ValueError("Unexpected fixture identity")
    cases = json.loads(raw)["cases"]
    project = load(a.subject)
    report = {"subject_sha256": hashlib.sha256(a.subject.read_bytes()).hexdigest(),
              "by_friction": {str(mu): {name: measure(project, case, mu) for name, case in cases.items()}
                              for mu in (.5, 0.)}}
    with a.out.open("x", encoding="ascii", newline="\n") as f:
        json.dump(report, f, sort_keys=True, indent=2, allow_nan=False)
        f.write("\n")
