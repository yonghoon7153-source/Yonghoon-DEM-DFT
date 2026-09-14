#!/usr/bin/env python3
"""Executable R11 repros for the replay evidence boundary.

Run this against a clean checkout.  Temporary cache/sitecustomize changes are
restored, and the cases that need commits create standalone disposable copies.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib._bootstrap_external as _bootstrap_external
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def run(argv, *, cwd: Path, env: dict[str, str] | None = None, timeout: int = 1800):
    merged = dict(os.environ)
    if env:
        merged.update(env)
    return subprocess.run(
        [str(x) for x in argv], cwd=cwd, env=merged, capture_output=True,
        text=True, timeout=timeout,
    )


def git(target: Path, *args: str, check: bool = True) -> str:
    p = run(["git", *args], cwd=target)
    if check and p.returncode:
        raise RuntimeError(f"git {' '.join(args)} rc={p.returncode}: {p.stderr[-500:]}")
    return p.stdout.strip()


def parse_json(stdout: str) -> dict:
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return {"_raw_tail": stdout[-1200:]}


def runner_cmd(python: Path, target: Path, rel: str, *extra: str) -> list[str]:
    return [str(python), str(target / rel), "--target", str(target),
            "--expected-head", git(target, "rev-parse", "HEAD"), *extra]


def early_gate_pyc(target: Path, python: Path) -> dict:
    """The ignored gate pyc executes before isolate_bytecode() is called."""
    src = target / "reviews/evidence_gate.py"
    pyc = Path(importlib.util.cache_from_source(str(src)))
    old_pyc = pyc.read_bytes() if pyc.exists() else None
    marker_dir = Path(tempfile.mkdtemp(prefix="r11-gate-pyc-marker-"))
    marker = marker_dir / "executed"
    altered = src.read_text(encoding="utf-8") + (
        f"\npathlib.Path({str(marker)!r}).write_text('executed', encoding='utf-8')\n"
    )
    st = src.stat()
    pyc.parent.mkdir(parents=True, exist_ok=True)
    pyc.write_bytes(_bootstrap_external._code_to_timestamp_pyc(
        compile(altered, str(src), "exec"), int(st.st_mtime), st.st_size,
    ))
    try:
        status = git(target, "status", "--porcelain", "--", ".")
        env = {"PYTHONDONTWRITEBYTECODE": "1"}
        env.pop("PYTHONPYCACHEPREFIX", None)
        p = run(runner_cmd(
            python, target, "reviews/r7_repros/replay_codex_r7.py",
            "--probes", "R7-06",
        ), cwd=target, env=env)
        d = parse_json(p.stdout)
        return {
            "source_sha256": hashlib.sha256(src.read_bytes()).hexdigest(),
            "head_blob": git(target, "rev-parse", "HEAD:./reviews/evidence_gate.py"),
            "git_status_porcelain": status,
            "ignored_pyc": str(pyc.relative_to(target)),
            "marker_executed": marker.is_file(),
            "runner_rc": p.returncode,
            "runner_stderr_tail": p.stderr[-500:],
            "dirty": d.get("dirty"),
            "instrument_sealed": d.get("instrument_sealed"),
            "package_digest_ok": d.get("package_digest_ok"),
            "evidence_eligible": d.get("evidence_eligible"),
            "closed": d.get("closed"),
            "false_identity": (
                marker.is_file() and not status and p.returncode == 0
                and d.get("instrument_sealed") is True
                and d.get("evidence_eligible") is True
                and d.get("closed") is True
            ),
        }
    finally:
        if old_pyc is None:
            pyc.unlink(missing_ok=True)
        else:
            pyc.write_bytes(old_pyc)
        marker.unlink(missing_ok=True)
        marker_dir.rmdir()


def abbreviated_expected_commit(target: Path, python: Path) -> dict:
    """The advertised exact expected commit accepts any matching 7+ character prefix."""
    head = git(target, "rev-parse", "HEAD")
    short = head[:7]
    p = run([
        str(python), str(target / "reviews/r7_repros/replay_codex_r7.py"),
        "--target", str(target), "--expected-head", short,
        "--probes", "R7-06",
    ], cwd=target, env={"PYTHONDONTWRITEBYTECODE": "1"})
    d = parse_json(p.stdout)
    return {
        "full_head": head,
        "supplied_expected_head": short,
        "runner_rc": p.returncode,
        "recorded_expected_head": d.get("expected_head"),
        "evidence_eligible": d.get("evidence_eligible"),
        "closed": d.get("closed"),
        "abbreviated_identity_accepted": (
            p.returncode == 0 and d.get("expected_head") == short
            and d.get("evidence_eligible") is True and d.get("closed") is True
        ),
    }


def skip_worktree_not_detected(target: Path, python: Path) -> dict:
    """git ls-files -v uses uppercase S for skip-worktree; gate checks lowercase only."""
    with tempfile.TemporaryDirectory(prefix="r11-skip-worktree-") as td:
        fixture = Path(td) / "bms-balancing"
        shutil.copytree(target, fixture, ignore=shutil.ignore_patterns(
            ".git", "__pycache__", ".pytest_cache", "*.pyc",
        ))
        git(fixture, "init", "-q")
        git(fixture, "add", "-f", ".")
        committed = run([
            "git", "-c", "user.name=R11 Repro", "-c", "user.email=r11@example.invalid",
            "commit", "-qm", "R11 standalone fixture",
        ], cwd=fixture)
        if committed.returncode:
            raise RuntimeError(f"fixture commit rc={committed.returncode}: {committed.stderr[-500:]}")
        rel = "reviews/evidence_gate.py"
        git(fixture, "update-index", "--skip-worktree", rel)
        tag = git(fixture, "ls-files", "-v", "--", rel)
        probe = run(
            [str(python), "-c",
             "import json,pathlib,sys;sys.path.insert(0,str(pathlib.Path('reviews').resolve()));"
             "import evidence_gate as g;print(json.dumps(g.index_skip_flags(pathlib.Path('.'))))"],
            cwd=fixture,
        )
        p = run(runner_cmd(
            python, fixture, "reviews/r7_repros/replay_codex_r7.py",
            "--probes", "R7-06",
        ), cwd=fixture, env={"PYTHONDONTWRITEBYTECODE": "1"})
        d = parse_json(p.stdout)
        return {
            "ls_files_v": tag,
            "gate_index_skip_flags": parse_json(probe.stdout),
            "runner_rc": p.returncode,
            "instrument_sealed": d.get("instrument_sealed"),
            "evidence_eligible": d.get("evidence_eligible"),
            "closed": d.get("closed"),
            "skip_flag_accepted": (
                tag.startswith("S ") and parse_json(probe.stdout) == []
                and p.returncode == 0 and d.get("evidence_eligible") is True
            ),
        }


def materialize_smudge_filter(target: Path, python: Path) -> dict:
    """A local checkout filter changes committed production bytes in the snapshot."""
    with tempfile.TemporaryDirectory(prefix="r11-smudge-filter-") as td:
        root = Path(td)
        fixture = root / "bms-balancing"
        shutil.copytree(target, fixture, ignore=shutil.ignore_patterns(
            ".git", "__pycache__", ".pytest_cache", "*.pyc",
        ))
        attrs = fixture / ".gitattributes"
        attrs.write_text(
            attrs.read_text(encoding="utf-8")
            + "\nbms_balancing/verify.py filter=r11smudge\n",
            encoding="utf-8",
        )
        git(fixture, "init", "-q")
        git(fixture, "add", "-f", ".")
        committed = run([
            "git", "-c", "user.name=R11 Repro", "-c", "user.email=r11@example.invalid",
            "commit", "-qm", "R11 smudge fixture",
        ], cwd=fixture)
        if committed.returncode:
            raise RuntimeError(f"fixture commit rc={committed.returncode}: {committed.stderr[-500:]}")
        marker = root / "smudged-production-executed"
        driver = root / "smudge.py"
        payload = (
            "\n__import__('pathlib').Path("
            + repr(str(marker))
            + ").write_text('executed')\n"
        ).encode()
        driver.write_text(
            "import sys\n"
            "data=sys.stdin.buffer.read()\n"
            "sys.stdout.buffer.write(data)\n"
            f"sys.stdout.buffer.write({payload!r})\n",
            encoding="utf-8",
        )
        git(fixture, "config", "filter.r11smudge.smudge", f"{python} {driver}")
        git(fixture, "config", "filter.r11smudge.clean", "cat")
        head = git(fixture, "rev-parse", "HEAD")
        committed_verify = git(fixture, "rev-parse", "HEAD:./bms_balancing/verify.py")
        p = run(runner_cmd(
            python, fixture, "reviews/r7_repros/replay_codex_r7.py",
            "--probes", "R7-06",
        ), cwd=fixture, env={"PYTHONDONTWRITEBYTECODE": "1"})
        d = parse_json(p.stdout)
        source_status = git(fixture, "status", "--porcelain", "--", ".")
        return {
            "head": head,
            "committed_verify_blob": committed_verify,
            "source_git_status": source_status,
            "source_worktree_clean": source_status == "",
            "smudged_production_executed": marker.is_file(),
            "runner_rc": p.returncode,
            "runner_stderr_tail": p.stderr[-600:],
            "instrument_sealed": d.get("instrument_sealed"),
            "package_digest_ok": d.get("package_digest_ok"),
            "evidence_eligible": d.get("evidence_eligible"),
            "closed": d.get("closed"),
            "materialized_bytes_not_commit_bytes": (
                marker.is_file() and p.returncode == 0
                and d.get("instrument_sealed") is True
                and d.get("evidence_eligible") is True
                and d.get("closed") is True
            ),
        }


def r10_assertion_alias(target: Path, python: Path) -> dict:
    """An unrelated production AssertionError is called a reached counterexample."""
    code = r'''
import importlib.util,json,pathlib,sys
t=pathlib.Path(sys.argv[1]).resolve()
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
rr=load("r10_runner",t/"reviews/r10_repros/replay_codex_r10.py")
snap=load("r10_snapshot",t/"reviews/r10_repros/codex/r10_snapshot_repros.py")
sys.path.insert(0,str(t))
from bms_balancing import schema as S
def unrelated(*a,**k): raise AssertionError("UNRELATED production invariant")
S.inputs_digest=unrelated
rec=rr._classify(lambda:snap.case_receipt_role_permutation(t),t/"reviews/r10_repros/codex")
print(json.dumps(rec,ensure_ascii=False))
'''
    p = run([str(python), "-c", code, str(target)], cwd=target)
    d = parse_json(p.stdout)
    return {
        "process_rc": p.returncode,
        "record": d,
        "unrelated_assertion_certified_closed": (
            p.returncode == 0 and d.get("도달") is True
            and d.get("상태") == "반례 소멸"
            and "UNRELATED production invariant" in str(d.get("세부"))
        ),
    }


def u18_dirty_meta_accepted(target: Path, python: Path) -> dict:
    """Promotion checks git fields for presence, but not unsafe values or commit identity."""
    code = r'''
import importlib.util,io,json,pathlib,sys,tempfile
t=pathlib.Path(sys.argv[1]).resolve()
sys.path[:0]=[str(t),str(t/"tests"),str(t/"scripts")]
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load("r10_u18",t/"reviews/r10_repros/codex/r10_u18_shape_repros.py")
t,S,V,sign,rows,pair,shape=m.boot(t)
with tempfile.TemporaryDirectory(prefix="r11-u18-dirty-meta-") as td:
 root=pathlib.Path(td);old,new=root/"old",root/"new"
 m.publish_matrix(V,sign,old,rows("old"),"old")
 f=m.publish_matrix(V,sign,new,rows("new"),"new")
 mp=f.with_name(f.name+".meta.json");meta=json.loads(mp.read_text())
 meta.update(git_dirty=True,git_modified_code=["bms_balancing/verify.py"],
             git_modified_outputs=[],git_commit_at_start="f"*40,
             git_state_changed_during_run=True)
 mp.write_text(json.dumps(meta))
 p=m.cli(t,"--new",new,"--old",old)
 promotion={}
 for line in p.stdout.splitlines():
  if line.startswith("PROMOTION "): promotion=json.loads(line[len("PROMOTION "):])
 print(json.dumps({"rc":p.returncode,"promotion":promotion,"stdout_tail":p.stdout[-1000:]},ensure_ascii=False))
'''
    p = run([str(python), "-c", code, str(target)], cwd=target)
    d = parse_json(p.stdout)
    promotion = d.get("promotion") or {}
    return {
        "process_rc": p.returncode,
        **d,
        "unsafe_git_meta_promoted": (
            p.returncode == 0 and d.get("rc") == 0
            and promotion.get("promotion_eligible") is True
        ),
    }


def untracked_sitecustomize_clean(target: Path, python: Path) -> dict:
    """Untracked startup code executes while provenance deliberately reports clean."""
    site = target / "sitecustomize.py"
    if site.exists():
        raise RuntimeError(f"fixture path already exists: {site}")
    marker_dir = Path(tempfile.mkdtemp(prefix="r11-sitecustomize-marker-"))
    marker = marker_dir / "executed"
    site.write_text(
        "from pathlib import Path\n"
        f"Path({str(marker)!r}).write_text('executed', encoding='utf-8')\n",
        encoding="utf-8",
    )
    try:
        normal_status = git(target, "status", "--porcelain", "--", "sitecustomize.py")
        code = r'''
import importlib.util,json,pathlib,sys
t=pathlib.Path(sys.argv[1]).resolve()
s=importlib.util.spec_from_file_location("prov",t/"scripts/provenance.py")
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
print(json.dumps(m.git_provenance(str(t))))
'''
        env = {
            "PYTHONPATH": str(target),
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        p = run([str(python), "-c", code, str(target)], cwd=target, env=env)
        d = parse_json(p.stdout)
        return {
            "normal_git_status": normal_status,
            "process_rc": p.returncode,
            "sitecustomize_executed": marker.is_file(),
            "provenance": d,
            "untracked_code_reported_clean": (
                marker.is_file() and p.returncode == 0
                and d.get("git_dirty") is False
                and d.get("git_modified_code") == []
            ),
        }
    finally:
        site.unlink(missing_ok=True)
        marker.unlink(missing_ok=True)
        marker_dir.rmdir()


FAKE_CHILD = r'''#!/usr/bin/env python3
import argparse, json
flags = {
    "optimized-assertions": "false_positive",
    "git-status-error": "false_clean",
    "assume-unchanged": "false_identity",
    "ignored-pyc": "false_identity",
    "argv-binding-mutant": "mutant_survived",
    "package-enforcement-mutant": "corrupt_package_accepted",
    "wrapper-coverage": "claim_gap",
}
ap = argparse.ArgumentParser()
ap.add_argument("--target")
ap.add_argument("--case", choices=flags, required=True)
a = ap.parse_args()
print(json.dumps({"cases": {a.case: {flags[a.case]: False, "sentinel": "child-exits-7"}}}))
raise SystemExit(7)
'''


def r10_child_rc_ignored(target: Path, python: Path) -> dict:
    """The parent uses a parsed flag but never binds the child return code."""
    with tempfile.TemporaryDirectory(prefix="r11-child-rc-") as td:
        fixture = Path(td) / "bms-balancing"
        shutil.copytree(target, fixture, ignore=shutil.ignore_patterns(
            ".git", "__pycache__", ".pytest_cache", "*.pyc",
        ))
        git(fixture, "init", "-q")
        git(fixture, "add", "-f", ".")
        initial = run([
            "git", "-c", "user.name=R11 Repro", "-c", "user.email=r11@example.invalid",
            "commit", "-qm", "R11 standalone fixture",
        ], cwd=fixture)
        if initial.returncode:
            raise RuntimeError(f"initial commit rc={initial.returncode}: {initial.stderr[-500:]}")

        child = fixture / "reviews/r10_repros/codex/r10_evidence_repros.py"
        sums = fixture / "reviews/r10_repros/codex/HARNESS_R10_BD6BA474_SHA256SUMS.txt"
        child.write_text(FAKE_CHILD, encoding="utf-8")
        digest = hashlib.sha256(child.read_bytes()).hexdigest()
        lines = sums.read_text(encoding="utf-8").splitlines()
        matches = [i for i, line in enumerate(lines) if line.endswith("  r10_evidence_repros.py")]
        if len(matches) != 1:
            raise RuntimeError(f"unexpected manifest entries: {matches}")
        lines[matches[0]] = f"{digest}  r10_evidence_repros.py"
        sums.write_text("\n".join(lines) + "\n", encoding="utf-8")
        git(fixture, "add", str(child.relative_to(fixture)), str(sums.relative_to(fixture)))
        commit = run([
            "git", "-c", "user.name=R11 Repro", "-c", "user.email=r11@example.invalid",
            "commit", "-qm", "R11 disposable child-rc repro",
        ], cwd=fixture)
        if commit.returncode:
            raise RuntimeError(f"commit rc={commit.returncode}: {commit.stderr[-500:]}")
        head = git(fixture, "rev-parse", "HEAD")
        child_run = run([str(python), str(child), "--target", str(fixture),
                         "--case", "optimized-assertions"], cwd=fixture)
        parent = run(runner_cmd(
            python, fixture, "reviews/r10_repros/replay_codex_r10.py",
        ), cwd=fixture, timeout=3600)
        d = parse_json(parent.stdout)
        evidence = {
            k: v for k, v in (d.get("probes") or {}).items()
            if k.startswith("evidence:")
        }
        return {
            "disposable_commit": head,
            "direct_child_rc": child_run.returncode,
            "direct_child_json": parse_json(child_run.stdout),
            "parent_rc": parent.returncode,
            "parent_stderr_tail": parent.stderr[-800:],
            "instrument_sealed": d.get("instrument_sealed"),
            "package_digest_ok": d.get("package_digest_ok"),
            "evidence_eligible": d.get("evidence_eligible"),
            "closed": d.get("closed"),
            "evidence_records": evidence,
            "nonzero_children_certified_closed": (
                child_run.returncode == 7 and parent.returncode == 0
                and d.get("evidence_eligible") is True and d.get("closed") is True
                and len(evidence) == 7
                and all(v.get("상태") == "반례 소멸" for v in evidence.values())
            ),
        }


CASES = {
    "early-gate-pyc": early_gate_pyc,
    "abbreviated-head": abbreviated_expected_commit,
    "skip-worktree": skip_worktree_not_detected,
    "materialize-smudge": materialize_smudge_filter,
    "r10-assertion-alias": r10_assertion_alias,
    "u18-dirty-meta": u18_dirty_meta_accepted,
    "untracked-sitecustomize": untracked_sitecustomize_clean,
    "r10-child-rc": r10_child_rc_ignored,
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=Path, required=True,
                    help="disposable clean bms-balancing checkout")
    ap.add_argument("--python", type=Path, default=Path(sys.executable))
    ap.add_argument("--case", choices=["all", *CASES], default="all")
    ap.add_argument("--output", type=Path)
    a = ap.parse_args()
    target = a.target.resolve()
    names = list(CASES) if a.case == "all" else [a.case]
    results = {}
    for name in names:
        # Do not Path.resolve() a venv interpreter: on POSIX it follows the
        # ``bin/python`` symlink to the base interpreter and loses site-packages.
        python = Path(os.path.abspath(a.python))
        results[name] = CASES[name](target, python)
    report = {"target": str(target), "head_after": git(target, "rev-parse", "HEAD"),
              "cases": results}
    text = json.dumps(report, ensure_ascii=False, indent=2)
    print(text)
    if a.output:
        a.output.write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
