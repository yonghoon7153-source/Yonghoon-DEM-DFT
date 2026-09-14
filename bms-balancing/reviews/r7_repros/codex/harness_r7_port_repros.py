"""R7 evidence/precision audit, only mutating an independent temporary copy.

Source SHA: 521be85e74acef80feec45bd147dd339e25b8d0a. The supplied mutation
programs and their probes are run from the scratch copy, never from the target.
Raw subprocess outputs and adapted per-mutant diagnostics can be saved to JSON.
"""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
from unittest.mock import patch

REV = "521be85e74acef80feec45bd147dd339e25b8d0a"
BASE = Path(__file__).resolve().parents[1]


def run(cmd, cwd, env):
    result = subprocess.run([str(x) for x in cmd], cwd=cwd, env=env, capture_output=True, text=True)
    return {"argv": [str(x) for x in cmd], "returncode": result.returncode,
            "stdout": result.stdout, "stderr": result.stderr}


def make_copy(target, temp, env):
    repo = temp / "review-copy"
    root = repo / "bms-balancing"
    shutil.copytree(target, root, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"))
    for command in (["git", "init", "-q"], ["git", "config", "user.email", "audit-fixture@example.invalid"],
                    ["git", "config", "user.name", "Review fixture"], ["git", "add", "."],
                    ["git", "commit", "-q", "-m", "Exact R7 scope snapshot for isolated review"]):
        result = run(command, repo, env)
        assert result["returncode"] == 0, result
    return root


def adapted_runs(root, env, old):
    program = root / "reviews/r6_repros/codex/replay_codex_r6_adapted.py"
    records = {}
    for name, baseline in (("default_environment", None), ("configured_old_baseline", old)):
        scoped = dict(env)
        scoped.pop("R6_OLD_OUT", None)
        if baseline is not None:
            scoped["R6_OLD_OUT"] = str(baseline)
        result = run([sys.executable, program, "--target", root], root, scoped)
        result["baseline"] = str(baseline) if baseline else None
        result["probe_output"] = json.loads(result["stdout"])
        records[name] = result
    assert records["default_environment"]["returncode"] == 1, records
    assert records["configured_old_baseline"]["returncode"] == 0, records
    return records


def own_mutation_audit(root, env):
    """Run original audit, adding observation-only stdout capture per pytest call."""
    script = root / "reviews/r6_repros/codex_r6_mutation_audit.py"
    raw = script.read_text(encoding="utf-8")
    record_file = root.parent / "pytest_mutation_calls.jsonl"
    needle = "    return r.returncode, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-300:]"
    assert raw.count(needle) == 1
    instrument = ("    import json as _audit_json\n"
                  f"    with open({str(record_file)!r}, 'a', encoding='utf-8') as _audit_stream:\n"
                  "        _audit_stream.write(_audit_json.dumps({'selection': k, 'rc': r.returncode, 'stdout': r.stdout, 'stderr': r.stderr}) + '\\n')\n")
    try:
        script.write_text(raw.replace(needle, instrument + needle), encoding="utf-8")
        result = run([sys.executable, script], root, env)
    finally:
        script.write_text(raw, encoding="utf-8")
    result["pytest_calls"] = [json.loads(line) for line in record_file.read_text(encoding="utf-8").splitlines()]
    assert result["returncode"] == 0 and result["stdout"].count("CAUGHT ") == 8, result
    assert len(result["pytest_calls"]) == 10, result
    assert all(r["rc"] == 1 for r in result["pytest_calls"][1:-1]), result
    return result


def adapted_mutation_audit(root, env, old):
    """Run exact mutation registry/main; wrap only run_adapted to retain diagnostics."""
    script = root / "reviews/r6_repros/codex/mutation_adapted.py"
    spec = importlib.util.spec_from_file_location("r7_adapted_audit", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    observations = []

    def observed():
        with tempfile.TemporaryDirectory(prefix="r7-adapted-result-") as tmp:
            output = Path(tmp) / "report.json"
            scoped = dict(env, R6_OLD_OUT=str(old))
            result = run([sys.executable, module.ADAPTED, "--target", root, "--output", output], root, scoped)
            parsed = json.loads(output.read_text(encoding="utf-8"))
            observations.append({"returncode": result["returncode"], "stdout": result["stdout"],
                                 "stderr": result["stderr"], "probe_output": parsed})
            return {key.split()[0]: value["상태"] for key, value in parsed["probes"].items()}

    module.run_adapted = observed
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        rc = module.main()
    result = {"returncode": rc, "stdout": stdout.getvalue(), "probe_runs": observations}
    assert rc == 0 and stdout.getvalue().count("CAUGHT ") == 5 and len(observations) == 7, result
    return result


def missed_exit_control(root, env):
    """Control: one deliberately non-catching candidate, same auditor exit logic.

    Only the copied mutation registry is reduced to the Q3 candidate and its new
    bytes made identical to old bytes. The auditor correctly says MISSED; the
    test asks whether its process then fails. This is not a production mutant.
    """
    program = root / "reviews/r6_repros/codex_r6_mutation_audit.py"
    raw = program.read_text(encoding="utf-8")
    needle = 'rc, last = run("c6_0 or c6_q3")'
    replacement = ('M = [M[-1]]\nM = [(what, k, path, old, old) for what, k, path, old, new in M]\n' + needle)
    try:
        program.write_text(raw.replace(needle, replacement, 1), encoding="utf-8")
        result = run([sys.executable, program], root, env)
    finally:
        program.write_text(raw, encoding="utf-8")
    assert "MISSED: 1" in result["stdout"] and result["returncode"] == 0, result
    return result


def disabled_schedule_control(root, env):
    """Disable only the copied test's event injection, not production behavior."""
    path = root / "tests/test_r6_internal.py"
    raw = path.read_text(encoding="utf-8")
    needle = '            if n["v"] == k:\n                on_k()'
    assert raw.count(needle) == 1
    try:
        path.write_text(raw.replace(needle, '            if False:  # controlled no-publication test fixture\n                on_k()'), encoding="utf-8")
        result = run([sys.executable, "-m", "pytest", "tests/test_r6_internal.py", "-q", "-p", "no:cacheprovider", "-k", "c6_01"], root, env)
    finally:
        path.write_text(raw, encoding="utf-8")
    assert result["returncode"] == 0 and "1 passed" in result["stdout"], result
    return result


def precision_closure(root, env):
    selection = "c6_q3 or i6v_01 or i6v_02 or i6v_03 or i6v_04 or i6v_06 or i6v_07"
    result = run([sys.executable, "-m", "pytest", "tests/test_r6_internal.py", "-q", "-p", "no:cacheprovider", "-k", selection], root, env)
    assert result["returncode"] == 0, result
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=Path, default=BASE / "work/harness-r7-target/bms-balancing")
    ap.add_argument("--old", type=Path, default=BASE / "work/harness-r6-baseline-bfc-parent/bms-balancing/out")
    ap.add_argument("--case", choices=("all", "adapted", "mutation", "controls", "precision"), default="all")
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    target, old = args.target.resolve(), args.old.resolve()
    env = dict(os.environ, PYTHONPATH=str(BASE / "work/harness-r2-pydeps") + os.pathsep + os.environ.get("PYTHONPATH", ""))
    head = run(["git", "-c", f"safe.directory={target.parent}", "-C", target, "rev-parse", "HEAD"], target, env)
    assert head["returncode"] == 0 and head["stdout"].strip() == REV, head
    report = {"source_head": REV, "target": str(target), "old_baseline": str(old), "cases": {}}
    with tempfile.TemporaryDirectory(prefix="r7-port-review-") as tmp:
        root = make_copy(target, Path(tmp), env)
        if args.case in ("all", "adapted"):
            report["cases"]["adapted"] = adapted_runs(root, env, old)
        if args.case in ("all", "mutation"):
            report["cases"]["own_mutation_audit"] = own_mutation_audit(root, env)
            report["cases"]["adapted_mutation_audit"] = adapted_mutation_audit(root, env, old)
        if args.case in ("all", "controls"):
            report["cases"]["missed_exit_control"] = missed_exit_control(root, env)
            report["cases"]["disabled_schedule_control"] = disabled_schedule_control(root, env)
        if args.case in ("all", "precision"):
            report["cases"]["precision_closure"] = precision_closure(root, env)
        status = run(["git", "status", "--porcelain"], root.parent, env)
        report["scratch_tracked_status_after_restore"] = status["stdout"]
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
