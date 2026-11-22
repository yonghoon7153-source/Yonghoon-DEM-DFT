"""Enumerate normal/open, stick and two slip-direction branches on a fixed small node."""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

import numpy as np


def evaluate(case, project):
    x, m, v0 = (np.asarray(case[k]) for k in ("x", "m", "vin"))
    n = len(m)
    pairs = list(itertools.combinations(range(n), 2))
    n_pairs = len(pairs)
    # The rows of G give separating normal and tangential relative velocities.
    g = np.zeros((2*n_pairs, 2*n))
    for k, (a,b) in enumerate(pairs):
        normal = x[b] - x[a]
        normal /= np.linalg.norm(normal)
        axes = np.array([normal, [-normal[1],normal[0]]])
        g[2*k:2*k+2,2*a:2*a+2] = -axes
        g[2*k:2*k+2,2*b:2*b+2] = axes
    mass = np.repeat(m,2)
    reduced = np.repeat([m[i]*m[j]/(m[i]+m[j]) for i,j in pairs],2)
    w = (g / mass) @ g.T * reduced[None,:]
    incoming = g @ v0.ravel()
    identity = np.eye(2*n_pairs)
    # Unknowns are pair impulses divided by their reduced mass (speed units).
    solutions = []
    singular = 0
    tol = 1e-8
    mu = .5
    for states in itertools.product(("open","stick","slip+","slip-"), repeat=n_pairs):
        a = identity.copy()
        rhs = np.zeros(2*n_pairs)
        for k, state in enumerate(states):
            j = 2*k
            if state == "open":
                continue
            a[j] = w[j]
            rhs[j] = -incoming[j]
            if state == "stick":
                a[j+1] = w[j+1]
                rhs[j+1] = -incoming[j+1]
            else:
                a[j+1,j] = mu if state == "slip+" else -mu
        q, _, rank, _ = np.linalg.lstsq(a, rhs, rcond=None)
        if rank != 2*n_pairs:
            singular += 1
        if max(np.abs(a@q-rhs)) > tol:
            continue
        vn = incoming + w @ q
        jn, jt = q[::2], q[1::2]
        # Test all constraints using outgoing relative velocity, including
        # separation and Coulomb sign at every purported sliding contact.
        resid_n = np.maximum(0,jn - vn[::2]) - jn
        resid_t = np.clip(jt-vn[1::2],-mu*np.maximum(0,jn),mu*np.maximum(0,jn))-jt
        if np.max(np.maximum(abs(resid_n), abs(resid_t))) > tol:
            continue
        v = v0 + ((g.T @ (q*reduced))/mass).reshape(n,2)
        solutions.append(v)
    if not solutions:
        raise ValueError("No verified branch witness")
    item = {"faces_examined":4**n_pairs, "rank_deficient_faces":singular,
            "witnesses":len(solutions),
            "max_distance_from_first_witness":max(float(np.max(np.linalg.norm(v-solutions[0],axis=1))) for v in solutions)}
    v = v0.copy()
    try:
        project(np.arange(n), np.zeros(n,dtype=int),m,x*m[:,None],v,x,.5)
    except ArithmeticError as exc:
        item.update(candidate="STOP",reason=str(exc))
    else:
        item.update(candidate="RETURNED",nearest_witness=max(0.,min(
            float(np.max(np.linalg.norm(v-u,axis=1))) for u in solutions)))
    return item


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",type=Path,required=True)
    parser.add_argument("--kernel",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("tested_kernel",args.kernel)
    kernel = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kernel)
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    groups = json.loads(args.input.read_bytes())["groups"]
    result = {name:evaluate(g["example"], kernel.project_contacts) for name,g in groups.items() if g["example"]}
    record = {"scope":"feasible sliding-law witnesses on prior nonconverged synthetic examples, no uniqueness claim",
              "source_sha256":sha(args.kernel),"input_sha256":sha(args.input),"records":result}
    with args.out.open("x", encoding="ascii", newline="\n") as stream:
        stream.write(json.dumps(record,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
