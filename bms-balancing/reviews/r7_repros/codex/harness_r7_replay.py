"""Bounded R7 review replay. Target sources are never edited by this runner."""
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

COMMIT = "521be85e74acef80feec45bd147dd339e25b8d0a"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--baseline-only", action="store_true")
    ap.add_argument("--old", type=Path)
    ap.add_argument("--previous", type=Path)
    args = ap.parse_args()
    target = args.target.resolve()
    here = Path(__file__).resolve().parent
    git = ["git", "-c", "safe.directory=" + str(target.parent), "-C", str(target.parent)]
    sha = subprocess.check_output(git + ["rev-parse", "HEAD"], text=True).strip()
    assert sha == COMMIT, (sha, COMMIT)
    before = subprocess.check_output(git + ["status", "--porcelain", "--", "bms-balancing"], text=True)
    env = dict(os.environ)
    env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env.get("PATH", "")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    commands = [
        ("baseline_pytest", [sys.executable, "-m", "pytest", "tests/", "-q", "-p", "no:cacheprovider"], 0),
        ("matlab_available_stages", ["bash", "matlab/tests/run_all.sh"], 0),
        ("compare_states", [sys.executable, "scripts/compare_states.py", "pouch=out",
                           "fixedhc=out/cells_pouch_fixedhc", "c168=out/cells_c168", "c171=out/cells_c171"], 0),
    ]
    scripts = []
    if not args.baseline_only:
        scripts = ["harness_r7_execution_repros.py", "harness_r7_claims_repros.py",
                   "harness_r7_inference_repros.py", "harness_r7_port_repros.py"]
        missing = [str(here / p) for p in scripts if not (here / p).is_file()]
        if missing:
            raise SystemExit("Missing review scripts: " + ", ".join(missing))
        for filename in scripts:
            cmd = [sys.executable, str(here / filename), "--target", str(target)]
            if ("inference" in filename or "port" in filename) and args.old:
                cmd += ["--old", str(args.old.resolve())]
            if "inference" in filename and args.previous:
                cmd += ["--previous", str(args.previous.resolve())]
            commands.append((filename, cmd, 0))
    script_hashes = {p: hashlib.sha256((here / p).read_bytes()).hexdigest() for p in scripts}
    runs = []
    for name, command, expected in commands:
        started = time.monotonic()
        try:
            run = subprocess.run(command, cwd=target, env=env, capture_output=True,
                                 text=True, encoding="utf-8", errors="replace", timeout=300)
            rc, stdout, stderr = run.returncode, run.stdout, run.stderr
        except subprocess.TimeoutExpired as exc:
            rc = None
            stdout = (exc.stdout or b"").decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
            stderr = (exc.stderr or b"").decode("utf-8", "replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
            stderr += "\nREVIEW RUNNER TIMEOUT (300 seconds); not a pass."
        elapsed = round(time.monotonic() - started, 3)
        runs.append(dict(case=name, command=command, exit_code=rc, expected_exit_code=expected,
                         elapsed_seconds=elapsed, stdout=stdout, stderr=stderr))
        print(f"{name}: rc={rc}, expected={expected}, {elapsed}s", flush=True)
    after = subprocess.check_output(git + ["status", "--porcelain", "--", "bms-balancing"], text=True)
    result = dict(
        meaning="Exit 0 means expected observations, including counterexamples; not approval.",
        reviewed_commit=sha, target=str(target), recorded_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        python=sys.version, packages={p: importlib.metadata.version(p) for p in ("numpy", "scipy", "pandas", "openpyxl", "pytest")},
        review_script_sha256=script_hashes,
        review_scripts_unchanged=(script_hashes == {p: hashlib.sha256((here / p).read_bytes()).hexdigest() for p in scripts}),
        tracked_target_before=before, tracked_target_after=after, runs=runs,
    )
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return int(before != after or not result["review_scripts_unchanged"]
               or any(r["exit_code"] != r["expected_exit_code"] for r in runs))


if __name__ == "__main__":
    sys.exit(main())
