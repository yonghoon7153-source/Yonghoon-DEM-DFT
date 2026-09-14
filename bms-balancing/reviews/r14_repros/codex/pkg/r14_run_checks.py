"""Read-only R14 scientific artifact checks; no fitting or historical replay."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    target = args.target.resolve()
    args.output.mkdir(parents=True, exist_ok=False)
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=target, text=True).strip()
    if head != "1bb45b358db4850c73e185d5f851e35fbcff9ad6":
        raise SystemExit(f"Wrong review commit: {head}")
    before = subprocess.check_output(["git", "status", "--porcelain"], cwd=target, text=True)
    if before:
        raise SystemExit("Target is not clean")
    cases = {
        "current_schema": ["scripts/check_u14.py", "--new", "out", "--schema-only"],
        "legacy_schema": ["scripts/check_u14.py", "--new", "out/archive/legacy_r6_u14", "--schema-only"],
        "new_vs_legacy": ["scripts/check_u14.py", "--new", "out", "--old", "out/archive/legacy_r6_u14"],
        "new_vs_current_head": ["scripts/check_u14.py", "--new", "out", "--old-rev", "HEAD"],
        "new_vs_prepromotion": ["scripts/check_u14.py", "--new", "out", "--old-rev", "37a889b^"],
        "compare_states": ["scripts/compare_states.py", "out"],
    }
    results = {"target_head": head, "checks": {}}
    for name, argv in cases.items():
        command = [sys.executable, "-B", *argv]
        completed = subprocess.run(command, cwd=target, capture_output=True, timeout=180)
        stdout = completed.stdout.decode("utf-8", errors="replace")
        stderr = completed.stderr.decode("utf-8", errors="replace")
        (args.output / f"{name}.stdout.txt").write_bytes(completed.stdout)
        (args.output / f"{name}.stderr.txt").write_bytes(completed.stderr)
        promotion = next((json.loads(line.removeprefix("PROMOTION "))
                          for line in stdout.splitlines() if line.startswith("PROMOTION ")), None)
        results["checks"][name] = {
            "command": command,
            "child_exit_code": completed.returncode,
            "promotion": promotion,
            "stdout_sha256": hashlib.sha256(completed.stdout).hexdigest(),
            "stderr_sha256": hashlib.sha256(completed.stderr).hexdigest(),
        }
    results["target_status_after"] = subprocess.check_output(
        ["git", "status", "--porcelain"], cwd=target, text=True)
    (args.output / "results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for name, result in results["checks"].items():
        p = result["promotion"] or {}
        print(json.dumps({"case": name, "child_rc": result["child_exit_code"],
                          "promotion_eligible": p.get("promotion_eligible"),
                          "roster": p.get("roster"), "blocked_by": p.get("blocked_by")},
                         ensure_ascii=False))
    print(json.dumps({"target_status_after": results["target_status_after"]}))


if __name__ == "__main__":
    main()
