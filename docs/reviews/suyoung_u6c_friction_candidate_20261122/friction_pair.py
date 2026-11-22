"""Two one-shot F8 candidate arms and a same-displacement readback of four traces."""
import argparse
import csv
from hashlib import sha256
import importlib.util
import io
import json
from pathlib import Path
import sys
import tarfile


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


HERE = Path(__file__).resolve().parent
ORDER_PATH = HERE.parent / "suyoung_u6c_seed_return_20261122" / "order_control.py"
if sha256(ORDER_PATH.read_bytes()).hexdigest() != "767d6db99338fb26835e4858bcac61cf0d3fb566f4ae1323d8cd89b931c13d6a":
    raise ValueError("HISTORICAL_ORDER_SOURCE")
original = load("fixed_order_library", ORDER_PATH)
dt = original.dt
ORDER_SHA = "8e76ec686e8f384c28c42b5c5304d25256096f0568fe999d602bdec307991e17"
PROTOCOL = "F8-two-id-orders-friction-multicontact-v1"
KERNEL = "suyoung_multicontact_dev.py"
NUM_ATOL = 1e-12  # MPa; double-precision diagnostic, not a physics tolerance
NUM_RTOL = 1e-12


def geometry(mapping):
    dt.require(mapping in ("ORIGINAL", "REVERSED"), "MAPPING")
    expected = dict(original.GEOMETRY)
    if mapping == "ORIGINAL":
        expected["field_ids"] = expected["physical_ids"]
    return expected


def check_calls(count, steps):
    dt.require(type(count) is int and type(steps) is int and count == steps and count > 0,
               "PROJECTOR_CALL_COUNT")


def receipt(source, mapping, native, directory, calls, observed):
    dt.require(observed == geometry(mapping), "SEED_BINDING")
    check_calls(calls, native["steps"])
    trace_sha = dt.sha((directory/"trace.csv").read_bytes())
    dt.require(trace_sha == native["trace_sha256"], "TRACE_BINDING")
    return dict(protocol=PROTOCOL, label="DEVELOPMENT_ONLY", stage3_go=False, u6_qualified=False,
                mapping=mapping, geometry_sha256=observed, candidate_calls=calls,
                candidate_sha256=dt.sha((source/KERNEL).read_bytes()), base_source_sha256=dt.SOURCE,
                adapter_sha256=dt.sha(Path(__file__).read_bytes()), trace_sha256=trace_sha,
                native_result_sha256=dt.sha((directory/"result.json").read_bytes()), status=native["status"])


def integrate(driver, candidate, mapping, budget, out):
    factory = driver.fixed_solver
    solver = factory()
    base_seed, base_project = solver.seed, solver.project_contacts
    observed = {}
    calls = 0

    def seed(cells):
        dt.require(cells == 8 and not observed, "SEED_REQUEST")
        x, ids, volume = base_seed(cells)
        fields = ids if mapping == "ORIGINAL" else original.reverse_ids(ids)
        observed.update(positions=original.array_digest(x, "<f8", (9653, 2)),
                        volume=original.array_digest(volume, "<f8", (9653,)),
                        physical_ids=original.array_digest(ids, "<i8", (9653,)),
                        field_ids=original.array_digest(fields, "<i8", (9653,)))
        dt.require(observed == geometry(mapping), "SEED_BINDING")
        return x, fields, volume

    def project(ids, nodes, mass, grad, velocity, centers, friction):
        nonlocal calls
        dt.require(friction == .5, "CANDIDATE_FRICTION")
        try:
            candidate.project_contacts(ids, nodes, mass, grad, velocity, centers, friction)
        except (ArithmeticError, ValueError, RuntimeError) as exc:
            raise RuntimeError(f"F8 {mapping}, step {calls+1}, contact solver: {exc}") from exc
        calls += 1

    solver.seed, solver.project_contacts = seed, project
    driver.fixed_solver = lambda: solver
    try:
        native = driver.run_arm("F", 8, budget, out)
        return native, observed, calls
    finally:
        driver.fixed_solver = factory
        solver.seed, solver.project_contacts = base_seed, base_project


def run(args):
    driver = load("fixed_friction_driver", args.source_dir/"suyoung_u6b_dev.py")
    candidate = load("fixed_friction_projector", args.source_dir/KERNEL)
    native, observed, calls = integrate(driver, candidate, args.mapping, args.budget, args.out)
    if calls:
        dt.write_json(args.out/"candidate.json", receipt(args.source_dir, args.mapping, native,
                                                         args.out, calls, observed))
    print(native["status"])
    return 0 if native["status"] == "TARGET_BRACKETED" and calls else 4


def read_candidate(source, directory, mapping, ref):
    native = json.loads((directory/"result.json").read_bytes())
    fields = ("status", "arm", "cells", "setting", "protocol", "label", "origin", "points_count")
    dt.require(tuple(native[k] for k in fields) ==
               ("TARGET_BRACKETED", "F", 8, 1, dt.NATIVE, "DEVELOPMENT_ONLY", "new", ref["points_count"]),
               "NATIVE_BINDING")
    dt.require(native["source_sha256"] == {k:v for k, v in dt.SOURCE.items() if k != "suyoung_u6b_dev.py"},
               "NATIVE_SOURCE_BINDING")
    item = json.loads((directory/"candidate.json").read_bytes())
    dt.require(item == receipt(source, mapping, native, directory, native["steps"], geometry(mapping)),
               "CANDIDATE_RECEIPT_BINDING")
    curve = dt.parse_curve((directory/"trace.csv").read_bytes(), native["steps"], ref["dt"], ref["width"], dt.SPEED)
    return curve, item


def historical_order(path, ref):
    raw = path.read_bytes()
    dt.require(dt.sha(raw) == ORDER_SHA, "PRIOR_ORDER_ARCHIVE")
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        native = json.load(tar.extractfile("run/F8_RELABEL/result.json"))
        trace = tar.extractfile("run/F8_RELABEL/trace.csv").read()
    dt.require(native["trace_sha256"] == dt.sha(trace) ==
               "faafadfcb01671f5816e1cc2e2eb04bbef235835616fa0a2d6580c3fe46e97c5", "PRIOR_ORDER_TRACE")
    return dt.parse_curve(trace, native["steps"], ref["dt"], ref["width"], dt.SPEED)


def pair_stats(a, b, count, anchor):
    dt.require(a.u[:count] == b.u[:count], "NATIVE_GRID_MISMATCH")
    def observation(i):
        return dict(step=i, u=a.u[i], original_MPa=a.p[i], reversed_MPa=b.p[i],
                    original_minus_reversed_MPa=a.p[i]-b.p[i])
    worst = observation(max(range(count), key=lambda i: abs(a.p[i]-b.p[i])))
    at_anchor = None
    if a.u[0] <= anchor <= a.u[count-1]:
        left, right = a.at(anchor), b.at(anchor)
        at_anchor = dict(u=anchor, original_MPa=left, reversed_MPa=right, original_minus_reversed_MPa=left-right)
    return dict(samples=count, start_u=a.u[0], end_u=a.u[count-1], first_worst=worst,
                max_abs_MPa=abs(worst["original_minus_reversed_MPa"]), at_fixed_anchor=at_anchor)


def shift_on_common(old, candidate, count):
    i = max(range(count), key=lambda i: abs(candidate.p[i]-old.p[i]))
    shift = candidate.p[i]-old.p[i]
    return dict(step=i, u=old.u[i], candidate_minus_historical_MPa=shift, max_abs_MPa=abs(shift))


def compare(old_a, old_b, new_a, new_b, anchor):
    curves = (old_a, old_b, new_a, new_b)
    counts = [len(curve.u) for curve in curves]
    n = min(counts)
    dt.require(n >= 2 and all(c.u[:n] == old_a.u[:n] for c in curves), "NATIVE_GRID_MISMATCH")
    old = pair_stats(old_a, old_b, min(counts[:2]), anchor)
    new = pair_stats(new_a, new_b, min(counts[2:]), anchor)
    old_joint = pair_stats(old_a, old_b, n, anchor)
    new_joint = pair_stats(new_a, new_b, n, anchor)
    def joint(i):
        return dict(step=i, u=old_a.u[i], old_original_minus_reversed_MPa=old_a.p[i]-old_b.p[i],
                    candidate_original_minus_reversed_MPa=new_a.p[i]-new_b.p[i])
    def fixed(u):
        if u < old_a.u[0] or u > old_a.u[n-1]:
            return dict(u=u, status="NOT_REACHED_BY_ALL_FOUR", pressures_MPa=None)
        oa, ob, na, nb = (c.at(u) for c in curves)
        return dict(u=u, status="REACHED", pressures_MPa=dict(old_original=oa, old_reversed=ob,
                    candidate_original=na, candidate_reversed=nb), old_original_minus_reversed_MPa=oa-ob,
                    candidate_original_minus_reversed_MPa=na-nb,
                    candidate_minus_historical_original_MPa=na-oa, candidate_minus_historical_reversed_MPa=nb-ob)
    same_stop = counts[2] == counts[3]
    close = same_stop and all(abs(a-b) <= NUM_ATOL+NUM_RTOL*max(abs(a), abs(b))
                              for a, b in zip(new_a.p, new_b.p))
    return dict(fixed_u=anchor, historical_pair=old, candidate_pair=new,
                first_cap_steps=dict(zip(("old_original","old_reversed","candidate_original","candidate_reversed"),
                                         (count-1 for count in counts))),
                all_four_common=dict(samples=n, end_u=old_a.u[n-1], old=old_joint, candidate=new_joint,
                                     decrease_in_max_abs_MPa=old_joint["max_abs_MPa"]-new_joint["max_abs_MPa"],
                                     at_old_worst=joint(old_joint["first_worst"]["step"]),
                                     at_candidate_worst=joint(new_joint["first_worst"]["step"]),
                                     original_kernel_change=shift_on_common(old_a, new_a, n),
                                     reversed_kernel_change=shift_on_common(old_b, new_b, n),
                                     fixed_points=[fixed(u) for u in (.1, .11100328595220721, anchor)]),
                candidate_numerical_comparison=dict(exact_samples_and_same_stop=(new_a.p == new_b.p),
                                                   max_abs_on_pair_common_MPa=new["max_abs_MPa"],
                                                   within_diagnostic_tolerance_and_same_stop=close,
                                                   absolute_tolerance_MPa=NUM_ATOL, relative_tolerance=NUM_RTOL,
                                                   qualification_threshold=None))


def read(args):
    report = dict(status="INCOMPLETE", protocol=PROTOCOL, label="DEVELOPMENT_ONLY", stage3_go=False, u6_qualified=False)
    try:
        old, refs, peak = dt.load_prior(args.wall)
        dt.require(peak["at_first_worst_total_gap"]["u"] == original.ANCHOR, "FIXED_ANCHOR")
        old_b = historical_order(args.prior_order, refs[8])
        a, rec_a = read_candidate(args.source_dir, args.arms_dir/"ORIGINAL", "ORIGINAL", refs[8])
        b, rec_b = read_candidate(args.source_dir, args.arms_dir/"REVERSED", "REVERSED", refs[8])
        report.update(status="DEVELOPMENT_READ_BACK", comparison=compare(old[8],old_b,a,b,original.ANCHOR),
                      historical_archive_sha256=dict(wall=dt.PRIOR_SHA, order=ORDER_SHA),
                      receipts=dict(original=rec_a, reversed=rec_b))
    except (ValueError, KeyError, OSError, TypeError, ArithmeticError, csv.Error, tarfile.TarError) as exc:
        report["issue"] = str(exc) if isinstance(exc, ValueError) and str(exc).isupper() else type(exc).__name__
    dt.write_json(args.out, report)
    print(report["status"])
    return 0 if "comparison" in report else 4


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)
    run_parser = sub.add_parser("run")
    read_parser = sub.add_parser("read")
    for group in (run_parser, read_parser):
        group.add_argument("--source-dir", required=True, type=Path)
        group.add_argument("--out", required=True, type=Path)
    run_parser.add_argument("--mapping", required=True, choices=("ORIGINAL", "REVERSED"))
    run_parser.add_argument("--budget", required=True, type=float)
    for name in ("wall", "prior-order", "arms-dir"):
        read_parser.add_argument("--"+name, type=Path, required=True)
    args = parser.parse_args()
    for name, digest in dt.SOURCE.items():
        dt.require(dt.sha((args.source_dir/name).read_bytes()) == digest, "SOURCE_BINDING")
    raise SystemExit(run(args) if args.mode == "run" else read(args))
