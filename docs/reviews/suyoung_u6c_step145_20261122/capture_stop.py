"""Capture the failing nodes of the historical F8 ORIGINAL step 145, once."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tarfile

import numpy as np


HIST_PIN = "001e5e5e5f3bedde8106b608910e95f5dd1f78cb"
PRIOR_SHA = "c39bbd65d1c0caa5825abc8095611a8d20a8168e5464db3cd2a05743e3abbbeb"
TRACE_SHA = "502694a2fabe7f30db63ac964ce6c97a7ce6efd2ca55a0c53a117bd13a3b4dc0"
SUMS_SHA = "60af64b6d3b2d6ebd1c7da40138cf8a291a21fb382aec15671ad429ff97e41de"
FRICTION_PATH = "docs/reviews/suyoung_u6c_friction_candidate_20261122/friction_pair.py"
KERNEL_PATH = "scripts/suyoung_multicontact_dev.py"
DRIVER_PATH = "scripts/suyoung_u6b_dev.py"
STOP_STEP = 145
EXPECTED = ("multi-contact residual unresolved after 512 updates; "
            "worst unresolved iteration residual / tolerance = 4.00627e+07")
PROTOCOL = "F8-original-stop145-nodes-v1"


def check(condition, reason):
    if not condition:
        raise ValueError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def write_json(path, data):
    raw = (json.dumps(data, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("ascii")
    with path.open("xb") as f:
        f.write(raw)
    return sha(raw)


def original_sources(prior, root):
    check(sha(prior.read_bytes()) == PRIOR_SHA, "WRONG_PRIOR_ARCHIVE")
    with tarfile.open(prior, "r:gz") as archive:
        def member(name):
            return archive.extractfile("run/" + name).read()
        sums = member("SOURCE_SHA256SUMS")
        check(sha(sums) == SUMS_SHA and sha(member("ORIGINAL/trace.csv")) == TRACE_SHA, "PRIOR_CONTENT")
        check(member("origin.txt").startswith(("release=" + HIST_PIN + "\n").encode()), "PRIOR_ORIGIN")
        check(member("ORIGINAL.log").decode().splitlines()[-1] ==
              "RuntimeError: F8 ORIGINAL, step 145, contact solver: " + EXPECTED, "PRIOR_STOP")
    entries = dict(line.split("  ", 1)[::-1] for line in sums.decode().splitlines())
    sources = {p: digest for p, digest in entries.items() if p != "RELEASE"}
    check(len(sources) == 7 and {FRICTION_PATH, KERNEL_PATH, DRIVER_PATH} <= set(sources), "SOURCE_LIST")
    for p, digest in sources.items():
        check(sha((root / p).read_bytes()) == digest, "SOURCE_IDENTITY")
    return sources


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def frame_locals(error, func):
    tb = error.__traceback__
    while tb:
        if tb.tb_frame.f_code is func.__code__:
            return tb.tb_frame.f_locals
        tb = tb.tb_next
    raise ValueError("NATIVE_FRAME_MISSING")


def failed_rows(error, kernel):
    # Read only after the pinned native function has raised. No node is
    # re-solved. The native flag already includes successful face corrections.
    batch = frame_locals(error, kernel._simultaneous)
    caller = frame_locals(error, kernel.project_contacts)
    iteration = batch["iteration"]
    check(iteration == kernel.MAX_ITERATIONS and batch["mu"] == .5, "WRONG_TERMINAL_ITERATE")
    failures = np.flatnonzero(~batch["converged"])
    check(len(failures) > 0, "EMPTY_FAILURE_MASK")
    nodes = []
    for b in failures:
        rows = caller["rows"][b]
        node_id = int(caller["nodes"][rows[0]])
        check(np.all(caller["nodes"][rows] == node_id), "NODE_INDEX")
        check(np.array_equal(caller["vel"][rows], batch["incoming"][b]) and
              np.array_equal(caller["mass"][rows], batch["mass"][b]), "NATIVE_INPUT_ROWS")
        ids = caller["ids"][rows]
        record = {"node_id": node_id, "field_ids": ids.tolist(),
                  "mass": batch["mass"][b].tolist(), "grad": caller["grad"][rows].tolist(),
                  "incoming": batch["incoming"][b].tolist(), "centers": caller["centers"][ids].tolist(),
                  "left": batch["left"].tolist(), "right": batch["right"].tolist(),
                  "normal": batch["normal"][b].tolist(), "mu": float(batch["mu"]),
                  "iteration": int(iteration), "jn_scaled": batch["jn"][b].tolist(),
                  "jt_scaled": batch["jt"][b].tolist(), "closing": batch["closing"][b].tolist(),
                  "slip": batch["slip"][b].tolist(), "residual": float(batch["residual"][b]),
                  "speed_tol": float(batch["speed_tol"][b])}
        check(record["residual"] > record["speed_tol"] > 0., "WRONG_RESIDUAL")
        nodes.append(record)
    return nodes


class ExpectedCapture(Exception):
    """Exit the original driver before completing step 145."""


class StopObserver:
    def __init__(self, kernel, target=STOP_STEP, expected=EXPECTED):
        self.kernel = kernel
        self.target = target
        self.expected = expected
        self.calls = 0
        self.nodes = []

    def project_contacts(self, *args):
        self.calls += 1
        check(self.calls <= self.target, "STEP_CEILING")
        if self.calls < self.target:
            return self.kernel.project_contacts(*args)
        try:
            self.kernel.project_contacts(*args)
        except ArithmeticError as error:
            check(str(error) == self.expected, "CHANGED_STOP_REASON")
            self.nodes = failed_rows(error, self.kernel)
            raise ExpectedCapture from None
        raise ValueError("EXPECTED_STOP_ABSENT")


def execute(source, prior, out):
    root = source.resolve(strict=True).parent
    sources = original_sources(prior, root)
    pair = load("capture_fixed_pair", root / FRICTION_PATH)
    driver = load("capture_fixed_driver", root / DRIVER_PATH)
    kernel = load("capture_fixed_kernel", root / KERNEL_PATH)
    observer = StopObserver(kernel)
    replay = out / "replay"
    try:
        pair.integrate(driver, observer, "ORIGINAL", 120., replay)
    except ExpectedCapture:
        pass
    else:
        raise ValueError("DID_NOT_CAPTURE")
    return publish(observer, sources, out)


def publish(observer, sources, out):
    check(observer.calls == STOP_STEP and observer.nodes, "INCOMPLETE_CAPTURE")
    check(sha((out/"replay"/"trace.csv").read_bytes()) == TRACE_SHA, "TRACE_PREFIX_MISMATCH")
    captured = {"protocol": PROTOCOL, "step": STOP_STEP, "mapping": "ORIGINAL",
                "source_sha256": sources, "nodes": observer.nodes, "native_error": EXPECTED,
                "scope": "unresolved nodes of the throwing batch after attempted face corrections",
                "residual_basis": "last native simultaneous iterate, before failed face correction"}
    node_hash = write_json(out/"failing_nodes.json", captured)
    return {"status": "CAPTURED_STEP_145", "label": "DEVELOPMENT_ONLY", "prior_pin": HIST_PIN,
            "completed_steps": STOP_STEP-1, "attempted_step": STOP_STEP, "failed_nodes": len(observer.nodes),
            "trace_sha256": TRACE_SHA, "prior_sha256": PRIOR_SHA, "failing_nodes_sha256": node_hash,
            "tool_sha256": sha(Path(__file__).read_bytes()), "stage3_go": False, "u6_qualified": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", required=True, type=Path)
    parser.add_argument("--prior", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    args.out.mkdir(exist_ok=False)
    try:
        receipt = execute(args.source_dir, args.prior, args.out)
    except (ArithmeticError, ValueError, RuntimeError, KeyError, TypeError, OSError, tarfile.TarError) as error:
        diagnostic = error.__cause__ if isinstance(error.__cause__, ValueError) else error
        reason = str(diagnostic) if isinstance(diagnostic, ValueError) and str(diagnostic).isupper() else type(error).__name__
        receipt = {"status":"INCOMPLETE", "reason":reason, "stage3_go":False, "u6_qualified":False}
    write_json(args.out/"capture_receipt.json", receipt)
    print(receipt["status"])
    return 0 if receipt["status"] == "CAPTURED_STEP_145" else 4


if __name__ == "__main__":
    raise SystemExit(main())
