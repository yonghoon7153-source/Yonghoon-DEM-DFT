"""Small frictionless, perfectly inelastic simultaneous normal projection at one node."""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

import numpy as np


SOURCES = {
    "suyoung_u6_first_dev.py": "5db0f1bda90c824a23479401b7744cf8d31fc64f373441abca692dce6717bda5",
    "dem_suyoung_sf2d_dev.py": "6e8073230f14142f3f802e1fed316bea22610502a98292e2ef794a123ea7e5f4",
}
FIXTURE = "d8eccd805f0a51a66b33b95ad7b12ae8480378c6cf8e98e93fecdf7eba6e0cc6"


def constraint_matrix(positions):
    """G v >= 0: normal relative velocity is separating or zero for every pair."""
    n = len(positions)
    pairs = list(itertools.combinations(range(n), 2))
    g = np.zeros((len(pairs), 2*n))
    for i, (a, b) in enumerate(pairs):
        normal = positions[b] - positions[a]
        magnitude = np.linalg.norm(normal)
        if magnitude == 0.:
            raise ValueError("Coincident centers")
        g[i, 2*a:2*a+2] = -normal / magnitude
        g[i, 2*b:2*b+2] = normal / magnitude
    return g


def solve(positions, masses, velocities):
    """Minimize 1/2 ||v-v0||_M^2 subject to G v >= 0 (2 or 3 bodies)."""
    x, mass, v0 = (np.asarray(a, dtype=float) for a in (positions, masses, velocities))
    n = len(mass)
    if n not in (2, 3) or x.shape != (n, 2) or v0.shape != x.shape or mass.shape != (n,):
        raise ValueError("Expected 2 or 3 two-dimensional bodies")
    if not (np.all(mass > 0) and all(np.isfinite(a).all() for a in (x,mass,v0))):
        raise ValueError("Non-finite inputs or invalid mass")
    g = constraint_matrix(x)
    m = np.repeat(mass, 2)
    inv_mass = 1. / m
    speed0 = g @ v0.ravel()
    w = (g * inv_mass) @ g.T
    accepted = []
    # Enumeration covers each candidate active set. Positive masses give a
    # strictly convex velocity objective. Dual impulses need not be unique.
    for k in range(len(g)+1):
        for subset in itertools.combinations(range(len(g)), k):
            active = list(subset)
            impulses = np.zeros(len(g))
            if active:
                block = w[np.ix_(active, active)]
                if np.linalg.matrix_rank(block) < k:
                    continue
                impulses[active] = np.linalg.solve(block, -speed0[active])
            delta = inv_mass * (g.T @ impulses)
            v = v0.ravel() + delta
            slack = g @ v
            # Absolute tolerances below apply only to these O(1) synthetic fixtures.
            if min(impulses) < -1e-12 or min(slack) < -1e-12:
                continue
            if max(np.abs(impulses * slack)) > 1e-12:
                continue
            if max(np.abs(m*(v-v0.ravel()) - g.T@impulses)) > 1e-12:
                raise ValueError("Stationarity failed")
            objective = .5 * np.dot(m*delta, delta)
            accepted.append((objective, v.reshape(n,2), impulses, slack))
    if not accepted:
        raise ValueError("No feasible KKT solution")
    obj, v, impulse, slack = min(accepted, key=lambda item: item[0])
    if any(not np.allclose(item[1],v,rtol=0,atol=1e-12) for item in accepted):
        raise ValueError("Inconsistent velocity solutions")
    return v, {"objective":float(obj), "pair_impulses":impulse.tolist(),
               "final_separating_speed":slack.tolist(), "feasible_kkt_sets":len(accepted)}


def measure(solver, state):
    x, m, vel = (np.asarray(state[k], dtype=float) for k in
                 ("positions_and_gradient_per_mass","mass","incoming_velocity"))
    n = len(m)
    vstar, constraints = solve(x,m,vel)
    rows = np.arange(n)
    grad = m[:,None] * x
    runs = []
    for labels in itertools.permutations(rows):
        ids = np.asarray(labels)
        centers = np.empty_like(x)
        centers[ids] = x
        projected = vel.copy()
        solver.project_contacts(ids, np.zeros(n,dtype=int), m, grad, projected, centers, 0.)
        # Independently reorder the reference solve by numerical ID; undo that
        # ordering before comparing the individual physical bodies.
        idx = np.argsort(ids)
        other, _ = solve(x[idx],m[idx],vel[idx])
        if not np.allclose(vstar[idx],other,rtol=0,atol=1e-12):
            raise ValueError("Reference relabel failed")
        runs.append(projected)
    native_error = [float(np.max(np.linalg.norm(v-vstar,axis=1))) for v in runs]
    native_objectives = [float(.5*np.sum(m[:,None]*(v-vel)**2)) for v in runs]
    g = constraint_matrix(x)
    native_closing = max(0., *[-float(np.min(g@v.ravel())) for v in runs])
    return {"reference_outgoing_velocity":vstar.tolist(),"KKT":constraints,
            "native_label_orders":len(runs),"native_max_final_closing_speed":native_closing,
            "native_min_max_single_body_velocity_error":[min(native_error), max(native_error)],
            "native_min_max_objective":[min(native_objectives),max(native_objectives)],
            "native_max_order_spread":max(float(np.max(np.linalg.norm(a-b,axis=1)))
                                          for a,b in itertools.combinations(runs,2))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scripts",type=Path,required=True)
    parser.add_argument("--fixtures",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    args = parser.parse_args()
    for name, expected in SOURCES.items():
        if hashlib.sha256((args.scripts/name).read_bytes()).hexdigest() != expected:
            raise ValueError("Source mismatch: "+name)
    raw = args.fixtures.read_bytes()
    if hashlib.sha256(raw).hexdigest() != FIXTURE:
        raise ValueError("Fixture mismatch")
    spec = importlib.util.spec_from_file_location("pinned_nodal",args.scripts/"suyoung_u6_first_dev.py")
    solver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(solver)
    records = {name:measure(solver,state) for name,state in json.loads(raw)["cases"].items()}
    report = {"model":"synthetic one-step normal-only mass metric projection, all pairs imposed",
              "mu":0., "source_sha256":SOURCES,"fixture_sha256":FIXTURE,"cases":records}
    with args.out.open("x",encoding="ascii",newline="\n") as out:
        json.dump(report,out,sort_keys=True,indent=2,allow_nan=False)
        out.write("\n")


if __name__ == "__main__":
    main()
