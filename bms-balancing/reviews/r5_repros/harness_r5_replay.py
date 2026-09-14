"""Replay R5 bounded scientific review; rc 0 confirms expected evidence, NOT GO.

Linux/WSL, target requirements plus pytest, and the four sibling probes required.
The reviewed checkout is not edited; numerical fixtures use temporary directories.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import time

COMMIT = "0cb7b7a380a90f61c1f25cabcb28204749b88076"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    target, here = args.target.resolve(), Path(__file__).resolve().parent
    git = ["git", "-c", "safe.directory=" + str(target.parent), "-C", str(target.parent)]
    sha = subprocess.check_output(git + ["rev-parse", "HEAD"], text=True).strip()
    if sha != COMMIT:
        raise SystemExit(f"Expected {COMMIT}; found {sha}")
    status = ["status", "--porcelain", "--", "bms-balancing"]
    before = subprocess.check_output(git + status, text=True)
    env = dict(os.environ)
    env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env.get("PATH", "")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    scripts = ["harness_r5_port_repros.py", "harness_r5_inference_repros.py",
               "harness_r5_claims_repros.py", "harness_r5_execution_repros.py"]
    old = "reviews/r4_repros/"
    commands = [
        ("baseline_pytest", [sys.executable, "-m", "pytest", "tests/", "-q", "-p", "no:cacheprovider"], 0),
        ("matlab_tests_available_stages", ["bash", "matlab/tests/run_all.sh"], 0),
        ("compare_states", [sys.executable, "scripts/compare_states.py", "pouch=out",
                            "fixedhc=out/cells_pouch_fixedhc", "c168=out/cells_c168", "c171=out/cells_c171"], 0),
        ("old_R4_port", [sys.executable, old + "harness_r4_port_repros.py", "--target", str(target)], 1),
        ("old_R4_shape", [sys.executable, old + "harness_r4_shape_repros.py", "--target", str(target)], 1),
        ("old_R4_execution", [sys.executable, old + "harness_r4_execution_repros.py", "--target", str(target)], 1),
        ("old_R4_plateau", [sys.executable, old + "harness_r4_inference_repros.py", "--target", str(target), "--case", "plateau"], 0),
    ]
    commands += [(name, [sys.executable, str(here / script), "--target", str(target)], 0)
                 for name, script in zip(("R5_port", "R5_inference", "R5_claims", "R5_execution"), scripts)]
    runs = []
    for name, command, expected in commands:
        start = time.monotonic()
        run = subprocess.run(command, cwd=target, env=env, capture_output=True,
                             text=True, encoding="utf-8", errors="replace", timeout=180)
        elapsed = round(time.monotonic() - start, 3)
        runs.append({"case": name, "command": command, "exit_code": run.returncode,
                     "expected_exit_code": expected, "elapsed_seconds": elapsed,
                     "stdout": run.stdout, "stderr": run.stderr})
        print(f"{name}: rc={run.returncode}, expected={expected}, {elapsed}s", flush=True)
    after = subprocess.check_output(git + status, text=True)
    result = {
        "meaning": "Expected results include reproduced defects and old assertions that now fail; not a GO verdict.",
        "reviewed_commit": sha, "target": str(target),
        "recorded_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python": sys.version,
        "packages": {p: importlib.metadata.version(p) for p in ("numpy", "scipy", "pandas", "openpyxl", "pytest")},
        "review_script_sha256": {p: hashlib.sha256((here / p).read_bytes()).hexdigest() for p in scripts},
        "tracked_target_before": before, "tracked_target_after": after, "runs": runs,
    }
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return int(before != after or any(r["exit_code"] != r["expected_exit_code"] for r in runs))


if __name__ == "__main__":
    sys.exit(main())
