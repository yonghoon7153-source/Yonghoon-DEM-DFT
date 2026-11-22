"""Inspect one frozen return from the kernel; emit only scalar and mode diagnostics."""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


parser = argparse.ArgumentParser()
for arg in ("kernel", "audit", "capture", "out"):
    parser.add_argument("--"+arg, type=Path, required=True)
args = parser.parse_args()
kernel = load("frozen_kernel", args.kernel)
audit = load("independent_evaluator", args.audit)
node, = json.loads(args.capture.read_bytes())["nodes"]
report = {"guessed": None, "face_trials": 0, "accepted": None}


def inspect(frame, event, arg):
    if event == "return" and frame.f_code.co_name == "on_face":
        ctx = frame.f_locals
        if report["face_trials"] == 0:
            report["guessed"] = list(ctx["modes"])
        report["face_trials"] += 1
        if arg is not None:
            report["accepted"] = list(ctx["modes"])
            report["native_residual"] = float(ctx["error"])
            result = audit.evaluate_impulse(node, ctx["scaled_impulse"])
            report["decimal70_residual"] = result["residual"]
            report["decimal70_energy_bound"] = bool(result["energy_bound_satisfied"])


vin = np.array(node["incoming"])
sys.setprofile(inspect)
try:
    kernel.project_contacts(np.arange(len(vin)), np.zeros(len(vin), dtype=int),
                            np.array(node["mass"]), np.array(node["grad"]), vin.copy(),
                            np.array(node["centers"]), node["mu"])
finally:
    sys.setprofile(None)
report["tol"] = node["speed_tol"]
args.out.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
print(json.dumps(report))
assert report["decimal70_energy_bound"] and report["decimal70_residual"] <= node["speed_tol"]
