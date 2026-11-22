"""Run the two F8 development arms. Preserve a native contact stop in the same run."""
import argparse
import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tarfile
import traceback

import numpy as np


CAPTURE_SHA = "90b070d33e84735008035eb399d648acb6065edfb677653f8db9f3c9c61eca18"
NODE_SHA = "525c57f0d73987c7ea6da8cf3324079712fea4b524757cf148a80989c51bc1e6"
OLD_KERNEL = "3b626fce463bf5387ba107ae1aa423d4cffad3b4adaa0133d8825c598850aa86"
CAPTURE_PIN = "f24cce28be28aece96d18cf77173d8fe05a2bfb0"
CAPTURE_HELPER = "docs/reviews/suyoung_u6c_step145_20261122/capture_stop.py"
PAIR_HELPER = "docs/reviews/suyoung_u6c_friction_candidate_20261122/friction_pair.py"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def verify_capture(path, root, pair, capture):
    raw = path.read_bytes()
    capture.check(sha(raw) == CAPTURE_SHA, "CAPTURE_ARCHIVE")
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        origin = dict(line.split("=", 1) for line in
                      tar.extractfile("run/origin.txt").read().decode("ascii").splitlines())
        receipt = json.load(tar.extractfile("run/capture/capture_receipt.json"))
        node_raw = tar.extractfile("run/capture/failing_nodes.json").read()
        trace = tar.extractfile("run/capture/replay/trace.csv").read()
        sums = tar.extractfile("run/SOURCE_SHA256SUMS").read()
    capture.check(origin["release"] == CAPTURE_PIN and origin["source_sums"] == sha(sums)
                  and origin["prior_failure"] == receipt["prior_sha256"] == capture.PRIOR_SHA,
                  "CAPTURE_ORIGIN")
    capture.check(sha(node_raw) == receipt["failing_nodes_sha256"] == NODE_SHA
                  and sha(trace) == receipt["trace_sha256"] == capture.TRACE_SHA,
                  "CAPTURE_NODE_OR_PREFIX")
    node = json.loads(node_raw)
    capture.check(receipt["status"] == "CAPTURED_STEP_145" and not receipt["u6_qualified"]
                  and not receipt["stage3_go"] and receipt["prior_pin"] == capture.HIST_PIN
                  and receipt["completed_steps"] == 144 and receipt["attempted_step"] == node["step"] == 145
                  and node["mapping"] == "ORIGINAL" and node["protocol"] == capture.PROTOCOL
                  and node["native_error"] == capture.EXPECTED and receipt["failed_nodes"] == len(node["nodes"]) == 1,
                  "CAPTURE_BINDING")
    capture.check(sha((root/CAPTURE_HELPER).read_bytes()) == receipt["tool_sha256"], "CAPTURE_HELPER")
    sources = dict(node["source_sha256"])
    capture.check(sources.pop(capture.KERNEL_PATH) == OLD_KERNEL and
                  sha((root/capture.KERNEL_PATH).read_bytes()) != OLD_KERNEL, "KERNEL_BINDING")
    capture.check(PAIR_HELPER in sources and len(sources) == 6 and
                  all(sha((root/name).read_bytes()) == digest for name, digest in sources.items()),
                  "CAPTURE_SOURCE")
    capture.check(all(sha((root/"scripts"/name).read_bytes()) == digest for name,digest in pair.dt.SOURCE.items()),
                  "DRIVER_SOURCES")


def trace_info(path):
    if not path.is_file():
        return {"present": False}
    data = path.read_bytes()
    result = {"present": True, "bytes": len(data), "sha256": sha(data), "last_complete_step": None}
    rows = csv.DictReader(io.StringIO(data.decode("ascii")))
    for index, row in enumerate(rows):
        if None in row or None in row.values() or row.get("step") != str(index):
            result["sequence_valid"] = False
            return result
        result["last_complete_step"] = index
    result["sequence_valid"] = True
    return result


def observe_failure(error, kernel, capture):
    """Use exact failed rows for a native residual; retain scoped inputs for other batch failures."""
    try:
        node_rows = capture.failed_rows(error, kernel)
        return {"scope": "NATIVE_UNRESOLVED_ROWS", "nodes": node_rows}
    except (ValueError, KeyError, IndexError, AttributeError, TypeError):
        pass
    try:
        caller = capture.frame_locals(error, kernel.project_contacts)
        rows = caller["rows"]
        scope = "THROWING_BATCH_INPUTS_INDIVIDUAL_CAUSE_UNRESOLVED"
        if str(error) == "nodal kinetic energy increased":
            batch = capture.frame_locals(error, kernel._simultaneous)
            rows = rows[batch["final_energy"] > batch["initial_energy"] + batch["bound"]]
            scope = "NATIVE_ENERGY_VIOLATION_ROWS"
        elif str(error) == "nonfinite contact velocity":
            bad = ~np.isfinite(caller["result"]).all(axis=(1, 2))
            rows = rows[bad]
            scope = "NATIVE_NONFINITE_RESULT_ROWS"
        records = []
        for row in rows:
            node_ids = caller["nodes"][row]
            capture.check(np.all(node_ids == node_ids[0]), "BATCH_NODE_BINDING")
            ids = caller["ids"][row]
            records.append(dict(node_id=int(node_ids[0]), field_ids=ids.tolist(),
                mass=caller["mass"][row].tolist(), grad=caller["grad"][row].tolist(),
                incoming=caller["vel"][row].tolist(), centers=caller["centers"][ids].tolist(),
                mu=float(caller["friction"])))
        capture.check(bool(records), "NO_BOUND_ROWS")
        return {"scope": scope, "nodes": records}
    except (ValueError, KeyError, IndexError, AttributeError, TypeError) as why:
        return {"scope": "NO_BOUND_NODE_ROWS", "reason": str(why), "nodes": []}


class ObservedProjector:
    def __init__(self, kernel, capture):
        self.kernel = kernel
        self.capture = capture
        self.calls = 0
        self.stop = None

    def project_contacts(self, *args):
        self.calls += 1
        try:
            return self.kernel.project_contacts(*args)
        except (ArithmeticError, ValueError, RuntimeError) as error:
            self.stop = {"attempted_step": self.calls, "exception": type(error).__name__,
                         "message": str(error), "scope": "NO_BOUND_NODE_ROWS", "nodes": []}
            try:
                detail = observe_failure(error, self.kernel, self.capture)
                # Encode any nonfinite diagnostic input as its IEEE name in valid JSON.
                self.stop.update(json.loads(json.dumps(detail), parse_constant=str))
            except (ArithmeticError, ValueError, OSError, TypeError, IndexError, KeyError, AttributeError) as why:
                self.stop["capture_error"] = str(why)
            raise


def run_arm(args, pair, capture):
    root = args.source_dir
    driver = load("node145_fixed_driver", root/"suyoung_u6b_dev.py")
    kernel = load("node145_candidate", root/pair.KERNEL)
    observer = ObservedProjector(kernel, capture)
    if args.out.exists():
        raise FileExistsError(args.out)
    stop = dict(label="DEVELOPMENT_ONLY", mapping=args.mapping, stage3_go=False, u6_qualified=False,
                kernel_sha256=sha((root/pair.KERNEL).read_bytes()), prior_capture_sha256=CAPTURE_SHA)
    try:
        native, observed, calls = pair.integrate(driver, observer, args.mapping, args.budget, args.out)
        if calls:
            pair.dt.write_json(args.out/"candidate.json",
                               pair.receipt(root, args.mapping, native, args.out, calls, observed))
        if native["status"] == "TARGET_BRACKETED" and calls:
            print(native["status"])
            return 0
        stop.update(status="NATIVE_STOP", native_status=native["status"])
    except Exception as error:
        traceback.print_exc()
        stop.update(status="CONTACT_STOP" if observer.stop else "OTHER_EXCEPTION",
                    exception=type(error).__name__, message=str(error))
    args.out.mkdir(exist_ok=True)
    if observer.stop is not None:
        node_sha = capture.write_json(args.out/"contact_stop.json", observer.stop)
        stop.update(attempted_step=observer.stop["attempted_step"], scope=observer.stop["scope"],
                    returned_nodes=len(observer.stop["nodes"]), contact_stop_sha256=node_sha)
    stop["trace"] = trace_info(args.out/"trace.csv")
    capture.write_json(args.out/"stop.json", stop)
    print(stop["status"])
    return 4


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("check", "run"))
    parser.add_argument("--source-dir", required=True, type=Path)
    parser.add_argument("--capture", type=Path)
    parser.add_argument("--wall", type=Path)
    parser.add_argument("--prior-order", type=Path)
    parser.add_argument("--mapping", choices=("ORIGINAL", "REVERSED"))
    parser.add_argument("--budget", type=float, choices=(570.,))
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    root = args.source_dir.resolve(strict=True).parent
    pair = load("node145_pair_adapter", root/PAIR_HELPER)
    capture = load("node145_capture_adapter", root/CAPTURE_HELPER)
    if args.mode == "check":
        if not all((args.capture, args.wall, args.prior_order)):
            parser.error("check requires --capture, --wall, --prior-order")
        verify_capture(args.capture, root, pair, capture)
        _, refs, _ = pair.dt.load_prior(args.wall)
        pair.historical_order(args.prior_order, refs[8])
        print("PRIOR_INPUTS_BOUND")
        return 0
    if not all((args.mapping, args.budget, args.out)):
        parser.error("run requires --mapping, --budget, --out")
    return run_arm(args, pair, capture)


if __name__ == "__main__":
    raise SystemExit(main())
