"""Repeat the native projection on frozen nodal degrees of freedom. No time steps."""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

import numpy as np


FIXTURES = Path("docs/reviews/suyoung_u6c_seed_return_20261122")
SOURCE_SHA = "5fd72069e8627d2fb4af2b4e74db194077a310503035c27f0bee6c1840aee619"
FIXTURE_SHA = "d8eccd805f0a51a66b33b95ad7b12ae8480378c6cf8e98e93fecdf7eba6e0cc6"
CHECKPOINTS = (1, 2, 4, 16)


def verified(path, digest):
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != digest:
        raise ValueError("Unexpected input: " + path.name)
    return data


def measure(prior, native_project, case, mu):
    mass = np.array(case["mass"])
    centers = np.array(case["positions_and_gradient_per_mass"])
    initial = np.array(case["incoming_velocity"])
    rows = np.arange(len(mass))
    pairs = list(itertools.combinations(rows, 2))
    normals = [centers[j] - centers[i] for i, j in pairs]
    normals = [n / np.linalg.norm(n) for n in normals]
    initial_p = mass @ initial
    labels = list(itertools.permutations(rows))
    saved = {n: [] for n in CHECKPOINTS}
    stats = {n: dict(max_residual_closing_speed=0., max_change_from_previous_batch=0.,
                     max_momentum_error=0., min_kinetic_energy=None, max_kinetic_energy=None)
             for n in CHECKPOINTS}

    def project(ids, nodes, masses, gradients, vel, by_id, fixture_mu):
        # The prior fixture supplies exactly the same physical->ID mapping,
        # gradients, storage order and centres. Set friction for this series.
        native_project(ids, nodes, masses, gradients, vel, by_id, mu)

    for permutation in labels:
        ids = np.array(permutation)
        v = initial.copy()
        e = .5 * np.sum(mass[:, None] * v**2)
        for n in range(1, max(CHECKPOINTS) + 1):
            before = v
            v = prior.project(project, centers, mass, before, ids, rows)
            energy = float(.5 * np.sum(mass[:, None] * v**2))
            if energy > e + 1e-12 or np.linalg.norm(mass @ v - initial_p) > 1e-12:
                raise ArithmeticError("Node balance control failed")
            e = energy
            if n == 1 and mu == .5:
                expected = next(r for r in case["id_results"] if r["physical_to_id"] == ids.tolist())
                np.testing.assert_allclose(v, expected["velocity_by_physical_body"], atol=1e-14, rtol=1e-14)
            if n in saved:
                saved[n].append(v.copy())
                s = stats[n]
                residual = max(0., *(float((v[i]-v[j]) @ normal) for (i,j),normal in zip(pairs,normals)))
                s["max_residual_closing_speed"] = max(s["max_residual_closing_speed"],residual)
                change = float(np.max(np.linalg.norm(v-before, axis=1)))
                s["max_change_from_previous_batch"] = max(s["max_change_from_previous_batch"],change)
                s["max_momentum_error"] = max(s["max_momentum_error"],float(np.linalg.norm(mass@v-initial_p)))
                low, high = s["min_kinetic_energy"], s["max_kinetic_energy"]
                s["min_kinetic_energy"] = energy if low is None else min(energy,low)
                s["max_kinetic_energy"] = energy if high is None else max(energy,high)

    for n, outcomes in saved.items():
        stats[n]["max_same_body_velocity_difference"] = max(
            float(np.max(np.linalg.norm(a-b,axis=1))) for a,b in itertools.combinations(outcomes,2))
        if len(mass)==2 and stats[n]["max_same_body_velocity_difference"] > 1e-12:
            raise ArithmeticError("Two-body ID control failed")
    return {"permutations":len(labels), "batches":stats}


def run(repo):
    folder = repo / FIXTURES
    src = folder / "node_permutation.py"
    verified(src,SOURCE_SHA)
    spec = importlib.util.spec_from_file_location("original_node_fixture", src)
    prior = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prior)
    fixed = json.loads(verified(folder/"node_permutation.json",FIXTURE_SHA))
    native = prior.load_projection(repo/"scripts")
    results = {}
    for mu in (.5,0.):
        results[str(mu)] = {case:measure(prior,native,data,mu) for case,data in fixed["cases"].items()}
    return {"scope":"frozen single synthetic node; zero time advancement",
            "fixture_source_sha256":SOURCE_SHA,"fixture_data_sha256":FIXTURE_SHA,
            "native_sources_sha256":prior.SOURCES, "sweeps_per_triple_batch":4,
            "pair_update_per_two_body_batch":1, "by_friction":results}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    args = ap.parse_args()
    report=run(args.repo)
    with args.out.open("x",encoding="ascii",newline="\n") as out:
        json.dump(report,out,sort_keys=True,indent=2,allow_nan=False)
        out.write("\n")
