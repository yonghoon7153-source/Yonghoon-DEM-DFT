"""R8 evidence audit. Mutations run only in an independently committed temp copy.

Source: a22da3380338f97b8eed2f600ffefad1e398c6c3. No private MATLAB/data claim.
The expected-bad controls are audit-interface checks, not production exploits.
"""
from __future__ import annotations
import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

BASE = Path(__file__).resolve().parents[1]
REV = "a22da3380338f97b8eed2f600ffefad1e398c6c3"


def run(argv, cwd, env):
    r = subprocess.run(list(map(str, argv)), cwd=cwd, env=env, capture_output=True, text=True)
    return {"argv": list(map(str, argv)), "cwd": str(cwd), "returncode": r.returncode,
            "stdout": r.stdout, "stderr": r.stderr}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def make_copy(target, temp, env):
    repo = temp / "review-copy"
    root = repo / "bms-balancing"
    shutil.copytree(target, root, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"))
    for cmd in (["git", "init", "-q"], ["git", "config", "user.email", "fixture@example.invalid"],
                ["git", "config", "user.name", "Numerical audit fixture"], ["git", "add", "."],
                ["git", "commit", "-qm", "R8 content snapshot, isolated mutation copy"]):
        r = run(cmd, repo, env)
        assert r["returncode"] == 0, r
    return root


def adapted(root, env, old):
    program = root / "reviews/r6_repros/codex/replay_codex_r6_adapted.py"
    records = {}
    for name, baseline in (("without_baseline", None), ("with_baseline", old)):
        scoped = dict(env)
        scoped.pop("R6_OLD_OUT", None)
        if baseline is not None:
            scoped["R6_OLD_OUT"] = str(baseline)
        r = run([sys.executable, program, "--target", root], root, scoped)
        r["report"] = json.loads(r["stdout"])
        r["baseline_env"] = str(baseline) if baseline else None
        records[name] = r
    assert records["without_baseline"]["returncode"] == 0
    assert records["without_baseline"]["report"]["mode"].startswith("부분")
    assert records["with_baseline"]["returncode"] == 0
    assert records["with_baseline"]["report"]["mode"] == "full"
    return records


def original_audit(root, env):
    """Exact registered mutants; observation-only capture around pytest output."""
    program = root / "reviews/r6_repros/codex_r6_mutation_audit.py"
    raw = program.read_text(encoding="utf-8")
    record = root.parent / "own_pytest_raw.jsonl"
    needle = "    return r.returncode, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-300:]"
    assert raw.count(needle) == 1
    obs = ("    import json as _obs_json\n"
           f"    with open({str(record)!r}, 'a', encoding='utf-8') as _obs_f:\n"
           "        _obs_f.write(_obs_json.dumps({'selection': k, 'rc': r.returncode, 'stdout': r.stdout, 'stderr': r.stderr}) + '\\n')\n")
    try:
        program.write_text(raw.replace(needle, obs + needle), encoding="utf-8")
        r = run([sys.executable, program], root, env)
    finally:
        program.write_text(raw, encoding="utf-8")
    r["pytest_calls"] = [json.loads(s) for s in record.read_text(encoding="utf-8").splitlines()]
    assert r["returncode"] == 0 and r["stdout"].count("CAUGHT ") == 8, r
    c4 = [x for x in r["pytest_calls"] if x["selection"] == "c6_04"]
    assert len(c4) == 1 and "KeyError: '100'" in c4[0]["stdout"], c4
    return r


def adapted_audit(root, env, old):
    module = load("r8_adapted_audit", root / "reviews/r6_repros/codex/mutation_adapted.py")
    records = []
    def observed():
        with tempfile.TemporaryDirectory(prefix="r8-probe-report-") as tmp:
            out = Path(tmp) / "report.json"
            r = run([sys.executable, module.ADAPTED, "--target", root, "--output", out],
                    root, dict(env, R6_OLD_OUT=str(old)))
            r["report"] = json.loads(out.read_text(encoding="utf-8"))
            records.append(r)
            return {k.split()[0]: v["상태"] for k, v in r["report"]["probes"].items()}
    module.run_adapted = observed
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = module.main()
    result = {"returncode": rc, "stdout": buf.getvalue(), "probe_runs": records}
    assert rc == 0 and result["stdout"].count("CAUGHT ") == 5, result
    assert all(v["상태"] == "닫힘" for v in records[-1]["report"]["probes"].values()), result
    return result


def audit_controls(root, env):
    """Use current main/run, but one safe semantic-no-op registry candidate."""
    program = root / "reviews/r6_repros/codex_r6_mutation_audit.py"
    # Use a harmless comment in an imported numerical reader. Baseline/restored
    # remain exact original selectors; only candidate selector differs.
    common = ("import importlib.util,sys\n"
              f"p={str(program)!r}\n"
              "s=importlib.util.spec_from_file_location('audit_control',p)\n"
              "m=importlib.util.module_from_spec(s);s.loader.exec_module(m)\n"
              "old='MODES = (\"LAM_PE\", \"LAM_NE\", \"LLI\")'\n"
              "new=old+'  # harmless audit control'\n")
    records = {}
    for name, selector in (("selected_noop_is_missed", "c6_04"),
                           ("no_selected_tests_is_caught", "c6_DOES_NOT_EXIST")):
        code = common + f"m.MUTATIONS=[('semantic no-op fixture',{selector!r},'scripts/compare_states.py',old,new)]\nsys.exit(m.main())\n"
        records[name] = run([sys.executable, "-c", code], root, env)
    assert records["selected_noop_is_missed"]["returncode"] == 1, records
    assert "MISSED: 1" in records["selected_noop_is_missed"]["stdout"], records
    bad = records["no_selected_tests_is_caught"]
    assert bad["returncode"] == 0 and "CAUGHT " in bad["stdout"] and "deselected" in bad["stdout"], records
    # Independent child output records what the same nonexistent selector does.
    records["empty_selection_pytest"] = run([sys.executable, "-m", "pytest", "tests/test_r6_internal.py", "-q",
                                               "-p", "no:cacheprovider", "-k", "c6_DOES_NOT_EXIST"], root, env)
    assert records["empty_selection_pytest"]["returncode"] == 5, records
    return records


def disabled_schedule(root, env):
    path = root / "tests/test_r6_internal.py"
    raw = path.read_text(encoding="utf-8")
    needle = '            if n["v"] == k:\n                on_k()'
    assert raw.count(needle) == 1
    try:
        path.write_text(raw.replace(needle, '            if False:  # test-only disabled publication\n                on_k()'), encoding="utf-8")
        r = run([sys.executable, "-m", "pytest", "tests/test_r6_internal.py", "-q", "-p", "no:cacheprovider", "-k", "c6_01"], root, env)
    finally:
        path.write_text(raw, encoding="utf-8")
    assert r["returncode"] == 1 and "AssertionError" in r["stdout"], r
    return r


def partially_disabled_schedule(root, env):
    """Test-only control: disable only metadata-boundary publications.

    The read counter still advances, so it is not an injection counter.
    The unmodified data-boundary schedules can mask the missing schedules.
    """
    path = root / "tests/test_r6_internal.py"
    raw = path.read_text(encoding="utf-8")
    needle = '            if n["v"] == k:\n                on_k()'
    assert raw.count(needle) == 1
    replacement = ('            if n["v"] == k and not target_name.endswith(".meta.json"):\n'
                   '                on_k()')
    try:
        path.write_text(raw.replace(needle, replacement), encoding="utf-8")
        r = run([sys.executable, "-m", "pytest", "tests/test_r6_internal.py", "-q", "-p", "no:cacheprovider", "-k", "c6_01"], root, env)
    finally:
        path.write_text(raw, encoding="utf-8")
    assert r["returncode"] == 0 and "1 passed" in r["stdout"], r
    return r


def r7_package_command(target, env):
    # Exact documented command targets the genuine R8 checkout, not the scratch
    # commit. Its pinned SHA check occurs before any copying or mutation.
    r = run([sys.executable, "reviews/r7_repros/codex/harness_r7_port_repros.py", "--target", ".", "--case", "controls"], target, env)
    assert r["returncode"] == 1 and 'head["stdout"].strip() == REV' in r["stderr"], r
    assert REV in r["stderr"], r
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=Path, default=BASE / "work/harness-r8-target-wsl/bms-balancing")
    ap.add_argument("--old", type=Path, default=BASE / "work/harness-r6-baseline-bfc-parent/bms-balancing/out")
    ap.add_argument("--case", choices=("all", "adapted", "mutations", "controls", "regressions"), default="all")
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    target, old = args.target.resolve(), args.old.resolve()
    env = dict(os.environ)
    env["PYTHONPATH"] = str(BASE / "work/harness-r2-pydeps") + os.pathsep + env.get("PYTHONPATH", "")
    env.update(GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="safe.directory", GIT_CONFIG_VALUE_0=str(target.parent))
    head = run(["git", "-C", target, "rev-parse", "HEAD"], target, env)
    assert head["returncode"] == 0 and head["stdout"].strip() == REV, head
    paths = ("reviews/r6_repros/codex_r6_mutation_audit.py", "reviews/r6_repros/codex/mutation_adapted.py",
             "reviews/r6_repros/codex/replay_codex_r6_adapted.py", "tests/test_r6_internal.py",
             "tests/test_r7_codex.py", "reviews/r7_repros/codex/harness_r7_port_repros.py")
    report = {"source_head": REV, "target": str(target), "old_baseline": str(old),
              "reviewer_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "source_sha256": {p: hashlib.sha256((target / p).read_bytes()).hexdigest() for p in paths}, "cases": {}}
    def save():
        if args.output:
            args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="r8-port-review-") as tmp:
        root = make_copy(target, Path(tmp), env)
        cases = report["cases"]
        if args.case in ("all", "controls"):
            cases["r7_package_exact_command"] = r7_package_command(target, env); save()
            cases["audit_controls"] = audit_controls(root, env); save()
            cases["disabled_schedule"] = disabled_schedule(root, env); save()
            cases["partially_disabled_schedule"] = partially_disabled_schedule(root, env); save()
        if args.case in ("all", "regressions"):
            r = run([sys.executable, "-m", "pytest", "tests/test_r6_internal.py", "tests/test_r7_codex.py", "-q",
                     "-p", "no:cacheprovider", "-k", "c6_01 or c6_04 or c6_q3 or d7_05 or d7_06"], root, env)
            assert r["returncode"] == 0, r
            cases["selected_regressions"] = r; save()
        if args.case in ("all", "adapted"):
            cases["adapted"] = adapted(root, env, old); save()
        if args.case in ("all", "mutations"):
            cases["original_mutation_audit"] = original_audit(root, env); save()
            cases["adapted_mutation_audit"] = adapted_audit(root, env, old); save()
        status = run(["git", "status", "--porcelain", "--untracked-files=no"], root.parent, env)
        report["tracked_scratch_status_after_restore"] = status["stdout"]
        assert status["returncode"] == 0 and not status["stdout"], status
    save()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
