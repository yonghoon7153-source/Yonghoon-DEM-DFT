"""Replay bounded R6 scientific review on the exact d431404 target.

Exit 0 means expected observations, not model approval. No target source edits.
The optional --old points to bfc4623^'s bms-balancing/out exported beforehand.
Without it, use Git archive from a normal clone to obtain that read-only baseline.
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
import zipfile

COMMIT = "d4314048c63605fb4613f8b0a91859271fddda98"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--old", type=Path)
    args = ap.parse_args()
    target, here = args.target.resolve(), Path(__file__).resolve().parent
    git = ["git", "-c", "safe.directory=" + str(target.parent), "-C", str(target.parent)]
    sha = subprocess.check_output(git + ["rev-parse", "HEAD"], text=True).strip()
    assert sha == COMMIT, (sha, COMMIT)
    status = ["status", "--porcelain", "--", "bms-balancing"]
    before = subprocess.check_output(git + status, text=True)
    env = dict(os.environ)
    env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env.get("PATH", "")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    scripts = ["harness_r6_final_port_repros.py", "harness_r6_final_claims_repros.py",
               "harness_r6_final_inference_repros.py", "harness_r6_final_execution_repros.py"]
    missing = [str(here / name) for name in scripts if not (here / name).is_file()]
    if missing:
        raise SystemExit("Missing review scripts: " + ", ".join(missing))
    with tempfile.TemporaryDirectory(prefix="harness-r6-replay-") as td:
        temp = Path(td)
        if args.old:
            old = args.old.resolve()
        else:
            archive = temp / "baseline.zip"
            subprocess.run(git + ["archive", "--format=zip", "--output=" + str(archive),
                                  "bfc4623^", "bms-balancing/out"], check=True)
            with zipfile.ZipFile(archive) as z:
                z.extractall(temp / "baseline")
            old = temp / "baseline/bms-balancing/out"
        assert old.is_dir()
        commands = [
            ("baseline_pytest", [sys.executable, "-m", "pytest", "tests/", "-q", "-p", "no:cacheprovider"], 0),
            ("matlab_available_stages", ["bash", "matlab/tests/run_all.sh"], 0),
            ("compare_states", [sys.executable, "scripts/compare_states.py", "pouch=out",
                                "fixedhc=out/cells_pouch_fixedhc", "c168=out/cells_c168", "c171=out/cells_c171"], 0),
            ("old_R5_sig_zero", [sys.executable, "reviews/r5_repros/harness_r5_port_repros.py",
                                 "--target", str(target), "--case", "sig2_zero_false_complete"], 1),
            ("old_R5_named_parameter", [sys.executable, "reviews/r5_repros/harness_r5_port_repros.py",
                                        "--target", str(target), "--case", "parameter_header_swap_false_complete"], 1),
            ("old_R5_exception_count", [sys.executable, "reviews/r5_repros/harness_r5_inference_repros.py",
                                        "--target", str(target), "--case", "exception"], 1),
            ("old_R5_matrix_audit", [sys.executable, "reviews/r5_repros/harness_r5_inference_repros.py",
                                     "--target", str(target), "--case", "matrix"], 1),
            ("R6_port", [sys.executable, str(here / scripts[0]), "--target", str(target)], 0),
            ("R6_libc_formats", [sys.executable, str(here / scripts[0]), "--libc-formats"], 0),
            ("R6_claims", [sys.executable, str(here / scripts[1]), "--target", str(target)], 0),
            ("R6_inference", [sys.executable, str(here / scripts[2]), "--target", str(target), "--old", str(old)], 0),
            ("R6_execution", [sys.executable, str(here / scripts[3]), "--target", str(target)], 0),
        ]
        runs = []
        for name, command, expected in commands:
            start = time.monotonic()
            run = subprocess.run(command, cwd=target, env=env, capture_output=True, text=True,
                                 encoding="utf-8", errors="replace", timeout=240)
            elapsed = round(time.monotonic() - start, 3)
            runs.append({"case": name, "command": command, "exit_code": run.returncode,
                         "expected_exit_code": expected, "elapsed_seconds": elapsed,
                         "stdout": run.stdout, "stderr": run.stderr})
            print(f"{name}: rc={run.returncode}, expected={expected}, {elapsed}s", flush=True)
        after = subprocess.check_output(git + status, text=True)
        result = {
            "meaning": "Expected observations include counterexamples and old assertions that now fail; not GO.",
            "reviewed_commit": sha, "target": str(target), "baseline_revision": "bfc4623^",
            "recorded_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "python": sys.version,
            "packages": {p: importlib.metadata.version(p) for p in ("numpy", "scipy", "pandas", "openpyxl", "pytest")},
            "review_script_sha256": {p: hashlib.sha256((here / p).read_bytes()).hexdigest() for p in scripts},
            "baseline_out_sha256": {str(p.relative_to(old)): hashlib.sha256(p.read_bytes()).hexdigest()
                                    for p in sorted(old.iterdir()) if p.is_file() and p.suffix in (".csv", ".json")},
            "tracked_target_before": before, "tracked_target_after": after, "runs": runs,
        }
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return int(before != after or any(r["exit_code"] != r["expected_exit_code"] for r in runs))


if __name__ == "__main__":
    sys.exit(main())
