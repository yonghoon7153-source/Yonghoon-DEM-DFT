"""Reproduce the R3 scientific review; never modify the reviewed source.

Run in Linux/WSL with the target requirements and pytest installed:
  python harness_r3_replay.py --target /path/to/bms-balancing --output r3.json

Exit 0 means expected controls/counterexamples were observed, NOT model GO.
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
import tempfile
import time


COMMIT = "a432d239c72c44a780be56679b8d9c1b9aaf3dc0"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    target = args.target.resolve()
    here = Path(__file__).resolve().parent
    git = ["git", "-c", "safe.directory=" + str(target.parent), "-C", str(target.parent)]
    sha = subprocess.check_output(git + ["rev-parse", "HEAD"], text=True).strip()
    if sha != COMMIT:
        raise SystemExit(f"Expected {COMMIT}; found {sha}. Refusing a different review target.")
    before = subprocess.check_output(git + ["status", "--porcelain", "--", "bms-balancing"], text=True)
    env = dict(os.environ)
    env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env.get("PATH", "")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    scripts = ["harness_r3_port_repros.py", "harness_r3_inference_repros.py",
               "harness_r3_shape_repros.py", "harness_r3_artifact_repros.py"]
    runs = []
    with tempfile.TemporaryDirectory(prefix="harness-r3-old-replay-") as temporary:
        old_output = Path(temporary) / "r2-on-r3.json"
        commands = [
            ("baseline_pytest", [sys.executable, "-m", "pytest", "tests/", "-q", "-p", "no:cacheprovider"], 0),
            ("matlab_tests_available_stages", ["bash", "matlab/tests/run_all.sh"], 0),
            ("compare_states", [sys.executable, "scripts/compare_states.py", "pouch=out",
                                "fixedhc=out/cells_pouch_fixedhc", "c168=out/cells_c168", "c171=out/cells_c171"], 0),
            ("original_R2_replay", [sys.executable, "reviews/r2_repros/harness_r2_replay.py",
                                    "--target", str(target), "--output", str(old_output)], 1),
            ("port", [sys.executable, str(here / scripts[0]), "--target", str(target)], 0),
            ("inference", [sys.executable, str(here / scripts[1]), "--root", str(target)], 0),
            ("shape", [sys.executable, str(here / scripts[2]), "--target", str(target)], 0),
            ("artifact_binding", [sys.executable, str(here / scripts[3]), "--target", str(target)], 0),
        ]
        for name, command, expected in commands:
            started = time.monotonic()
            result = subprocess.run(command, cwd=target, env=env, capture_output=True,
                                    text=True, encoding="utf-8", errors="replace", timeout=180)
            row = {"case": name, "command": command, "exit_code": result.returncode,
                   "expected_exit_code": expected, "elapsed_seconds": round(time.monotonic()-started, 3),
                   "stdout": result.stdout, "stderr": result.stderr}
            if name == "original_R2_replay" and old_output.exists():
                row["legacy_report"] = json.loads(old_output.read_text(encoding="utf-8"))
                row["legacy_metadata_caution"] = "Nested reviewed_commit is hardcoded by the old R2 runner; the executed target is the outer R3 commit."
            runs.append(row)
            print(f"{name}: rc={result.returncode}, expected={expected}, {row['elapsed_seconds']}s", flush=True)
    after = subprocess.check_output(git + ["status", "--porcelain", "--", "bms-balancing"], text=True)
    report = {
        "meaning": "Counterexample probes assert defects; expected exit codes do not mean GO.",
        "reviewed_commit": sha, "target": str(target),
        "recorded_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python": sys.version,
        "packages": {p: importlib.metadata.version(p) for p in ("numpy", "scipy", "pandas", "openpyxl", "pytest")},
        "review_script_sha256": {p: hashlib.sha256((here/p).read_bytes()).hexdigest() for p in scripts},
        "tracked_target_before": before, "tracked_target_after": after,
        "runs": runs,
    }
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return int(before != after or any(r["exit_code"] != r["expected_exit_code"] for r in runs))


if __name__ == "__main__":
    sys.exit(main())
