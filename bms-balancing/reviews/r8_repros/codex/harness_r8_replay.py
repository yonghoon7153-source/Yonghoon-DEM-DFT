"""Bounded R8 adversarial-review replay; the target checkout is never edited."""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import time


COMMIT = "a22da3380338f97b8eed2f600ffefad1e398c6c3"


def run_one(spec, target, env):
    name, command, timeout = spec
    started = time.monotonic()
    try:
        run = subprocess.run(
            command,
            cwd=target,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        rc, stdout, stderr = run.returncode, run.stdout, run.stderr
    except subprocess.TimeoutExpired as exc:
        rc = None
        stdout = exc.stdout or ""
        stderr = (exc.stderr or "") + f"\nREVIEW RUNNER TIMEOUT ({timeout}s); not a pass."
    return {
        "case": name,
        "command": list(map(str, command)),
        "exit_code": rc,
        "expected_exit_code": 0,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "stdout": stdout,
        "stderr": stderr,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=Path, required=True)
    ap.add_argument("--old", type=Path, required=True)
    ap.add_argument("--previous", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    target = args.target.resolve()
    here = Path(__file__).resolve().parent
    git_root = target.parent
    git = ["git", "-c", "safe.directory=" + str(git_root), "-C", str(git_root)]
    sha = subprocess.check_output(git + ["rev-parse", "HEAD"], text=True).strip()
    assert sha == COMMIT, (sha, COMMIT)
    before = subprocess.check_output(git + ["status", "--porcelain"], text=True)

    scripts = ["r8_inference_repros.py", "r8_claims_repros.py", "r8_port_repros.py"]
    script_hashes = {p: hashlib.sha256((here / p).read_bytes()).hexdigest() for p in scripts}
    env = dict(os.environ)
    env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env.get("PATH", "")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = str(here.parent / "work/harness-r2-pydeps") + os.pathsep + env.get("PYTHONPATH", "")

    # These are independent, read-only target checks. The port audit mutates only
    # its own freshly committed temporary copy.
    specs = [
        ("pytest", [sys.executable, "-m", "pytest", "tests/", "-q", "-p", "no:cacheprovider"], 300),
        ("matlab_available_stages", ["bash", "matlab/tests/run_all.sh"], 300),
        ("check_u14_current", [sys.executable, "scripts/check_u14.py", "--new", "out", "--old", "out"], 120),
        ("compare_states_current", [sys.executable, "scripts/compare_states.py", "out"], 120),
        (
            "inference_counterexamples",
            [sys.executable, str(here / scripts[0]), "--target", str(target),
             "--previous", str(args.previous.resolve()), "--old", str(args.old.resolve()), "--case", "all"],
            300,
        ),
        ("claims_counterexamples", [sys.executable, str(here / scripts[1]), "--target", str(target), "--case", "all"], 300),
        (
            "port_evidence_audit",
            [sys.executable, str(here / scripts[2]), "--target", str(target),
             "--old", str(args.old.resolve()), "--case", "all"],
            420,
        ),
    ]
    runs = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(run_one, spec, target, env) for spec in specs]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            runs.append(result)
            print(f"{result['case']}: rc={result['exit_code']} in {result['elapsed_seconds']}s", flush=True)
    order = {spec[0]: i for i, spec in enumerate(specs)}
    runs.sort(key=lambda x: order[x["case"]])

    after = subprocess.check_output(git + ["status", "--porcelain"], text=True)
    current_hashes = {p: hashlib.sha256((here / p).read_bytes()).hexdigest() for p in scripts}
    result = {
        "meaning": "A review-script exit 0 means its expected counterexamples and controls were observed; it is not GO.",
        "reviewed_commit": sha,
        "target": str(target),
        "recorded_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python": sys.version,
        "packages": {p: importlib.metadata.version(p) for p in ("numpy", "scipy", "pandas", "openpyxl", "pytest")},
        "review_script_sha256": script_hashes,
        "review_scripts_unchanged": script_hashes == current_hashes,
        "tracked_target_before": before,
        "tracked_target_after": after,
        "runs": runs,
    }
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return int(before != after or not result["review_scripts_unchanged"] or any(r["exit_code"] != 0 for r in runs))


if __name__ == "__main__":
    raise SystemExit(main())
