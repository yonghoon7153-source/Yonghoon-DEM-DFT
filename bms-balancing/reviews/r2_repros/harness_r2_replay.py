"""Replay the numerical R2 review probes and preserve their actual outputs.

Exit 0 means the asserted review counterexamples reproduced; it does not mean
the reviewed implementation passed those missing requirements.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


def main():
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, default=base.parent / "work/harness-r2-target/bms-balancing")
    parser.add_argument("--output", type=Path, default=base / "harness_r2_replay_results.json")
    args = parser.parse_args()
    jobs = [
        ("port", "harness_r2_port_repros.py", "--target"),
        ("inference", "harness_r2_inference_repros.py", "--root"),
        ("shape", "harness_r2_shape_repros.py", "--root"),
        ("consumed_axis", "harness_r2_consumed_axis_repro.py", "--target"),
    ]
    records = []
    for name, filename, target_arg in jobs:
        command = [sys.executable, str(base / filename), target_arg, str(args.target.resolve())]
        result = subprocess.run(command, text=True, encoding="utf-8", capture_output=True, timeout=90)
        records.append({"case": name, "command": command, "exit_code": result.returncode,
                        "stdout": result.stdout, "stderr": result.stderr})
        print(f"{name}: rc {result.returncode}", flush=True)
    report = {"meaning": "rc 0 reproduces the asserted defects, not GO",
              "reviewed_commit": "abfed8b371c08b4c358f2c2b7e0853056dad838c",
              "python": sys.version, "runs": records}
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Evidence: {args.output.resolve()}")
    return int(any(row["exit_code"] for row in records))


if __name__ == "__main__":
    raise SystemExit(main())
