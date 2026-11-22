"""Local perturbations of the frozen step-228 node; one contact solve per sample, no integration."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def trials(node):
    rng = np.random.default_rng(2282304)
    mass, grad, v = (np.array(node[name], dtype=float) for name in ("mass", "grad", "incoming"))
    span = np.max(np.linalg.norm(v[:, None] - v[None, :], axis=2))
    for size in (0.001, 0.01, 0.05):
        for number in range(16):
            new_mass = mass * rng.uniform(1 - size, 1 + size, size=mass.shape)
            angle = rng.uniform(-size, size, size=len(mass))
            cosine, sine = np.cos(angle), np.sin(angle)
            gradient = np.column_stack((cosine*grad[:, 0] - sine*grad[:, 1],
                                        sine*grad[:, 0] + cosine*grad[:, 1]))
            perturbed = v + span * rng.uniform(-size, size, size=v.shape)
            yield size, number, new_mass, gradient, perturbed


def read_kernel(path):
    spec = importlib.util.spec_from_file_location("tested_node_kernel", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def measure(kernel, mass, gradient, v, centers, mu):
    result = v.copy()
    try:
        kernel.project_contacts(np.arange(len(mass)), np.zeros(len(mass), dtype=int),
                                mass, gradient, result, centers, mu)
    except ArithmeticError:
        if not np.array_equal(result, v):
            raise ValueError("partial write on failure")
        return None
    tolerance = kernel.ABS_SPEED_TOL + kernel.REL_SPEED_TOL * np.linalg.norm(v[:,None]-v[None,:],axis=2).max()
    # Recheck translation-invariant momentum and energy in the incoming COM frame.
    if not np.isfinite(result).all() or np.max(abs(mass @ (result - v))) > mass.sum()*tolerance:
        raise ValueError("momentum residual")
    frame = np.average(v, axis=0, weights=mass)
    initial, final = [np.sum(mass[:,None]*(array-frame)**2) for array in (v,result)]
    if final > initial * (1+1e-11) + mass.sum()*tolerance**2:
        raise ValueError("energy increase")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--capture", type=Path, required=True)
    parser.add_argument("--subject", type=Path, required=True)
    parser.add_argument("--reference", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    data = args.capture.read_bytes()
    if sha(data) != "fca406d296c8a6f2b5bb260784711afdc87a34cda48f71ce93c8abcaf7f1059f":
        parser.error("unexpected capture")
    node, = json.loads(data)["nodes"]
    kernel = read_kernel(args.subject)
    reference = read_kernel(args.reference) if args.reference else None
    records = []
    for scale, number, mass, grad, v in trials(node):
        inputs = (mass, grad, v, np.array(node["centers"]), node["mu"])
        actual = measure(kernel, *inputs)
        record = dict(scale=scale, index=number, accepted=actual is not None)
        if reference is not None:
            old = measure(reference, *inputs)
            record["reference_accepted"] = old is not None
            if old is not None and (actual is None or not np.array_equal(old, actual)):
                raise ValueError("previously accepted velocity changed")
        records.append(record)
    answer = dict(scope="fixed-seed synthetic perturbations of one captured node",
                  capture_sha256=sha(data), subject_sha256=sha(args.subject.read_bytes()),
                  reference_sha256=sha(args.reference.read_bytes()) if reference else None,
                  numpy_version=np.__version__, trials=len(records),
                  accepted=sum(r["accepted"] for r in records), records=records)
    with args.out.open("x", encoding="ascii",newline="\n") as out:
        json.dump(answer,out,indent=2)
        out.write("\n")
    print("accepted",answer["accepted"],"/",len(records))


if __name__ == "__main__":
    main()
