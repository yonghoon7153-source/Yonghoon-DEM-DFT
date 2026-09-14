#!/usr/bin/env python3
"""Reviewer-only counterexamples for the R10 evidence machinery.

The reviewed checkout is never modified.  Cases that need a dirty or mutant tree
operate on a temporary local clone.
"""
from __future__ import annotations

import argparse
import importlib._bootstrap_external as _be
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def run(cmd, *, cwd, env=None, timeout=300):
    e = dict(os.environ)
    if env:
        e.update(env)
    return subprocess.run(
        [str(x) for x in cmd], cwd=cwd, env=e, text=True,
        capture_output=True, timeout=timeout,
    )


def parse_json(stdout):
    try:
        return json.loads(stdout)
    except Exception:
        return {"_raw_tail": stdout[-1200:]}


def clone_of(target: Path, td: Path) -> Path:
    """Make a self-contained local fixture repo from the reviewed subdirectory.

    The upstream checkout is a promisor+sparse worktree, so a normal local clone
    tries to materialize unrelated missing objects.  A copied subdirectory plus a
    fresh fixture commit is enough to exercise the runner's HEAD/clean contract.
    """
    dst = td / "repo"
    c = dst / "bms-balancing"
    shutil.copytree(target, c, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    # Preserve the reviewed repository-level ignored-bytecode policy; it is
    # precisely part of the ignored-pyc identity counterexample.
    root_ignore = target.parent / ".gitignore"
    if root_ignore.is_file():
        shutil.copy2(root_ignore, dst / ".gitignore")
    for cmd in (
        ["git", "init", "--quiet"],
        ["git", "config", "user.email", "review@example.invalid"],
        ["git", "config", "user.name", "R10 reviewer"],
        ["git", "add", "."],
        ["git", "commit", "--quiet", "-m", "R10 fixture"],
    ):
        p = run(cmd, cwd=dst)
        if p.returncode:
            raise RuntimeError(p.stderr)
    return c


def runner_cmd(target: Path, probe: str):
    return [
        sys.executable, target / "reviews/r9_repros/replay_codex_r9.py",
        "--target", target, "--expected-head", git_head(target),
        "--probes", probe,
    ]


def git_head(target: Path) -> str:
    return run(["git", "rev-parse", "HEAD"], cwd=target).stdout.strip()


def optimized_assertions(target: Path):
    """A delegated pytest usage error is certified as closed under ``python -O``."""
    env = {
        "PYTHONOPTIMIZE": "1",
        "PYTEST_ADDOPTS": "--definitely-invalid-option",
    }
    p = run(runner_cmd(target, "P2-4"), cwd=target, env=env)
    d = parse_json(p.stdout)
    rec = d.get("probes", {}).get("P2-4", {})
    return {
        "runner_rc": p.returncode,
        "closed": d.get("closed"),
        "dirty": d.get("dirty"),
        "package_digest_ok": d.get("package_digest_ok"),
        "reported_status": rec.get("상태"),
        "delegated_summary": rec.get("세부", {}).get("summary"),
        "false_positive": p.returncode == 0 and d.get("closed") is True
                          and "invalid-option" in str(rec.get("세부", {}).get("summary")),
    }


def git_status_error(target: Path):
    """The runner ignores ``git status`` rc/stderr and reports unknown as clean."""
    with tempfile.TemporaryDirectory(prefix="r10-index-dir-") as s:
        index_dir = Path(s)
        env = {"GIT_INDEX_FILE": str(index_dir)}  # a directory: git status rc 128
        raw = run(["git", "status", "--porcelain", "--untracked-files=normal", "--", "."],
                  cwd=target, env=env)
        p = run(runner_cmd(target, "P2-3"), cwd=target, env=env)
    d = parse_json(p.stdout)
    return {
        "direct_git_status_rc": raw.returncode,
        "direct_git_status_stderr": raw.stderr.strip()[-300:],
        "runner_rc": p.returncode,
        "runner_reports_dirty": d.get("dirty"),
        "closed": d.get("closed"),
        "false_clean": raw.returncode != 0 and p.returncode == 0
                       and d.get("dirty") is False and d.get("closed") is True,
    }


def assume_unchanged_identity(target: Path):
    """A modified tracked module executes while HEAD/dirty fields still say exact+clean."""
    head = git_head(target)
    with tempfile.TemporaryDirectory(prefix="r10-assume-") as s:
        td = Path(s)
        c = clone_of(target, td)
        rel = "bms_balancing/verify.py"
        p = run(["git", "update-index", "--assume-unchanged", rel], cwd=c)
        if p.returncode:
            raise RuntimeError(p.stderr)
        marker = td / "modified-module-executed"
        src = c / rel
        src.write_text(src.read_text(encoding="utf-8") +
                       f"\nPath({str(marker)!r}).write_text('executed', encoding='utf-8')\n",
                       encoding="utf-8")
        status = run(["git", "status", "--porcelain", "--", "."], cwd=c)
        rp = run(runner_cmd(c, "P2-3"), cwd=c)
        d = parse_json(rp.stdout)
        return {
            "git_status_rc": status.returncode,
            "git_status_porcelain": status.stdout,
            "runner_rc": rp.returncode,
            "runner_target_head": d.get("target_head"),
            "runner_reports_dirty": d.get("dirty"),
            "closed": d.get("closed"),
            "modified_module_executed": marker.is_file(),
            "false_identity": not status.stdout.strip() and rp.returncode == 0
                              and d.get("dirty") is False and marker.is_file(),
        }


def ignored_pyc_identity(target: Path):
    """Ignored timestamp-valid pyc can execute bytes absent from the commit."""
    head = git_head(target)
    with tempfile.TemporaryDirectory(prefix="r10-pyc-") as s:
        td = Path(s)
        c = clone_of(target, td)
        src = c / "bms_balancing/verify.py"
        marker = td / "ignored-pyc-executed"
        altered = src.read_text(encoding="utf-8") + (
            f"\nPath({str(marker)!r}).write_text('executed', encoding='utf-8')\n"
        )
        code = compile(altered, str(src), "exec")
        st = src.stat()
        pyc = Path(importlib.util.cache_from_source(str(src)))
        pyc.parent.mkdir(parents=True, exist_ok=True)
        pyc.write_bytes(_be._code_to_timestamp_pyc(code, int(st.st_mtime), st.st_size))
        status = run(["git", "status", "--porcelain", "--", "."], cwd=c)
        rp = run(runner_cmd(c, "P2-3"), cwd=c, env={"PYTHONDONTWRITEBYTECODE": "1"})
        d = parse_json(rp.stdout)
        return {
            "pyc": str(pyc.relative_to(c)),
            "git_status_porcelain": status.stdout,
            "runner_rc": rp.returncode,
            "runner_reports_dirty": d.get("dirty"),
            "closed": d.get("closed"),
            "modified_bytecode_executed": marker.is_file(),
            "false_identity": not status.stdout.strip() and rp.returncode == 0
                              and d.get("dirty") is False and marker.is_file(),
        }


def argv_binding_mutant(target: Path):
    """The named P2-4 test bypasses ``run`` and therefore misses argv binding loss."""
    head = git_head(target)
    with tempfile.TemporaryDirectory(prefix="r10-argv-mutant-") as s:
        c = clone_of(target, Path(s))
        f = c / "scripts/run_states.sh"
        text = f.read_text(encoding="utf-8")
        old = '  LAST_ARGV="$*"'
        new = '  LAST_ARGV="FORGED-BY-MUTANT"'
        count = text.count(old)
        f.write_text(text.replace(old, new), encoding="utf-8")
        p = run([sys.executable, "-m", "pytest",
                 "tests/test_r9_codex.py::test_d9_10_matrix_sidecar_seals_the_exact_roster_and_argv",
                 "-q", "--no-header", "-p", "no:cacheprovider"], cwd=c)
        return {
            "mutation_site_count": count,
            "pytest_rc": p.returncode,
            "pytest_tail": p.stdout.strip().splitlines()[-1] if p.stdout.strip() else p.stderr[-300:],
            "mutant_survived": count == 1 and p.returncode == 0,
            "reason": "test calls write_meta directly after assigning LAST_ARGV; production run() is never called",
        }


def argv_flatten_collision(target: Path):
    """Two different argv vectors have the same ``$*`` sidecar representation."""
    code = r'''show () { local LAST_ARGV="$*"; printf '%s\n' "$LAST_ARGV"; }
show cmd "a b" c
show cmd a "b c"
'''
    p = run(["bash", "-c", code], cwd=target)
    lines = p.stdout.splitlines()
    return {
        "vector_a": ["cmd", "a b", "c"],
        "vector_b": ["cmd", "a", "b c"],
        "serialized": lines,
        "collision": p.returncode == 0 and len(lines) == 2 and lines[0] == lines[1],
    }


def package_enforcement_mutant(target: Path):
    """P2-2 regression does not make a package byte mismatch, so enforcement deletion survives."""
    head = git_head(target)
    with tempfile.TemporaryDirectory(prefix="r10-package-mutant-") as s:
        c = clone_of(target, Path(s))
        runner = c / "reviews/r7_repros/replay_codex_r7.py"
        text = runner.read_text(encoding="utf-8")
        old = "return bool(status) and all(v == \"ok\" for v in status.values()), status"
        new = "return True, status  # REVIEW MUTANT: mismatch is not enforced"
        count = text.count(old)
        runner.write_text(text.replace(old, new), encoding="utf-8")
        test = run([sys.executable, "-m", "pytest",
                    "tests/test_r9_codex.py::test_d9_08_r7_runner_rejects_unknown_empty_or_duplicate_probes_and_wrong_head",
                    "-q", "--no-header", "-p", "no:cacheprovider"], cwd=c, timeout=600)
        listed = c / "reviews/r7_repros/codex/HARNESS_R7_521BE85_CODEX_REVIEW.md"
        listed.write_text(listed.read_text(encoding="utf-8") + "\nCORRUPTED\n", encoding="utf-8")
        rp = run([sys.executable, runner, "--target", c, "--expected-head", git_head(c),
                  "--probes", "R7-05", "--allow-dirty"], cwd=c, timeout=600)
        d = parse_json(rp.stdout)
        status = d.get("package_digest", {}).get(listed.name)
        return {
            "mutation_site_count": count,
            "regression_pytest_rc": test.returncode,
            "regression_pytest_tail": test.stdout.strip().splitlines()[-1] if test.stdout.strip() else test.stderr[-300:],
            "corrupted_file_status": status,
            "runner_package_digest_ok": d.get("package_digest_ok"),
            "runner_closed": d.get("closed"),
            "runner_rc": rp.returncode,
            "mutant_survived_test": count == 1 and test.returncode == 0,
            "corrupt_package_accepted": status == "mismatch" and d.get("package_digest_ok") is True and rp.returncode == 0,
        }


def wrapper_coverage(target: Path):
    test = run([sys.executable, "-m", "pytest",
                "tests/test_r9_codex.py::test_d9_11_zero_pair_and_partial_are_distinct_typed_states",
                "-q", "--no-header", "-p", "no:cacheprovider"], cwd=target)
    production = []
    for p in (target / "scripts").glob("*.sh"):
        live = [ln.strip() for ln in p.read_text(encoding="utf-8", errors="ignore").splitlines()
                if ln.strip() and not ln.lstrip().startswith("#")]
        if any("ne_shape" in ln or "EXIT_BY_STATUS" in ln for ln in live):
            production.append(p.name)
    return {
        "named_test_rc": test.returncode,
        "named_test_tail": test.stdout.strip().splitlines()[-1] if test.stdout.strip() else test.stderr[-300:],
        "production_wrapper_consumers": production,
        "claim_gap": test.returncode == 0 and not production,
        "reason": "the test calls ne_shape.main directly and checks meta+documentation; no wrapper is invoked",
    }


CASES = {
    "optimized-assertions": optimized_assertions,
    "git-status-error": git_status_error,
    "assume-unchanged": assume_unchanged_identity,
    "ignored-pyc": ignored_pyc_identity,
    "argv-binding-mutant": argv_binding_mutant,
    "argv-flatten-collision": argv_flatten_collision,
    "package-enforcement-mutant": package_enforcement_mutant,
    "wrapper-coverage": wrapper_coverage,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=Path, required=True)
    ap.add_argument("--case", choices=["all", *CASES], default="all")
    ns = ap.parse_args()
    target = ns.target.resolve()
    names = list(CASES) if ns.case == "all" else [ns.case]
    out = {name: CASES[name](target) for name in names}
    print(json.dumps({"target": str(target), "head": git_head(target), "cases": out},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
