#!/usr/bin/env python3
"""Reviewer-only executable counterexamples for R10 snapshot/schema boundaries.

The target tree is imported but never modified.  Every artifact is made under a
TemporaryDirectory.  Run from any directory:

  python r10_snapshot_repros.py --target /path/to/bms-balancing --case all
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import hashlib
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

import numpy as np


def load_target(target: Path):
    sys.path.insert(0, str(target))
    from bms_balancing import schema as S  # noqa: PLC0415
    from bms_balancing import verify as V  # noqa: PLC0415
    return S, V


class Patch:
    def __init__(self):
        self.undo = []

    def set(self, obj, name, value):
        old = getattr(obj, name)
        setattr(obj, name, value)
        self.undo.append((obj, name, old))

    def close(self):
        while self.undo:
            obj, name, old = self.undo.pop()
            setattr(obj, name, old)


def receipt(S, seed: str = "1"):
    d = {
        "half_cell": {"path": "half.xlsx", "sha256": seed * 64},
        "full_cell": {"path": "full.xlsx", "sha256": "2" * 64},
        "literature": {
            "gr": {"path": "gr.xlsx", "sha256": "3" * 64},
            "si": {"path": "si.csv", "sha256": "4" * 64},
        },
    }
    return d, S.inputs_digest(d)


def case_eval_self_overwrite(target: Path):
    """--out == --compare replaces independent MATLAB evidence before reading it."""
    S, V = load_target(target)
    p = Patch()
    with tempfile.TemporaryDirectory(prefix="r10-eval-") as td:
        t = Path(td)
        evidence = t / "matlab.csv"
        original = b"THIS IS DELIBERATELY NOT A VALID MATLAB RECEIPT\n"
        evidence.write_bytes(original)

        ci, digest = receipt(S)

        class FakeObjective:
            consumed_inputs = ci
            inputs_sha = digest
            scale_audit = None

            def rmse_pocv(self, q):
                return 1.0 + float(q[0]) / 100.0

            def rmse_dvdq(self, q):
                return 2.0 + float(q[1]) / 100.0

            def rmse_dqdv(self, q, weighted=True):
                return (3.0 if not weighted else 4.0) + float(q[2]) / 100.0

        anchors = [(name, float(i + 1)) for i, (name, _stage) in enumerate(V.ANCHOR_STAGE)]
        p.set(V.D, "data_root", lambda _x=None: t)
        p.set(V, "build", lambda *_a, **_k: FakeObjective())
        p.set(V, "dd_eval_anchors", lambda *_a, **_k: anchors)
        args = SimpleNamespace(
            data_root=str(t), source="GITT", state="100", si_source="Li",
            w_dqdv=0.0, seed=0, out=str(evidence), compare=str(evidence),
            precision="auto", allow_partial=False,
        )
        out = io.StringIO()
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
                rc = V.cmd_eval(args)
        finally:
            p.close()
        now = evidence.read_bytes()
        result = {
            "case": "eval_self_overwrite",
            "rc": rc,
            "original_sha256": hashlib.sha256(original).hexdigest(),
            "after_sha256": hashlib.sha256(now).hexdigest(),
            "original_destroyed": now != original,
            "reports_complete": "(complete)" in out.getvalue() or "전부 일치" in out.getvalue(),
            "tail": out.getvalue().splitlines()[-8:],
        }
        assert rc == 0 and result["original_destroyed"] and result["reports_complete"], result
        return result


def case_profile_partial_promoted(target: Path):
    """One failed gamma is omitted, yet profile publishes canonical and returns 0."""
    S, V = load_target(target)
    p = Patch()
    with tempfile.TemporaryDirectory(prefix="r10-profile-") as td:
        t = Path(td)
        art = t / "profile_gamma_100_Li.csv"
        old = b"PREVIOUS COMPLETE CANONICAL\n"
        art.write_bytes(old)
        ci, digest = receipt(S)

        class FakeObjective:
            consumed_inputs = ci
            inputs_sha = digest
            scale_audit = None
            n_scale_samples = 50
            scales = {"pocv": 1.0, "dvdq": 1.0, "dqdv": 1.0}
            c_cell = 1.0

            def __call__(self, _q):
                return 1.0

            def rmse_pocv(self, _q):
                return 1.0

            def _auto_scales(self, *_a, **_k):
                return dict(self.scales)

        calls = {"n": 0}

        def fake_minimize(_f, _s, **_kw):
            calls["n"] += 1
            good = calls["n"] == 1  # grid=2, starts=0 => first gamma succeeds, second fails
            return SimpleNamespace(success=good, fun=1.0, x=np.array([1.0, 0.0, 1.0, 0.0]))

        p.set(V.D, "data_root", lambda _x=None: t)
        p.set(V, "build", lambda *_a, **_k: FakeObjective())
        p.set(V, "multistart", lambda *_a, **_k: (np.array([1.0, 0.0, 1.0, 0.0, 0.2]), 1.0, []))
        p.set(V, "minimize", fake_minimize)
        p.set(V, "degradation_modes", lambda *_a, **_k: {"LAM_PE": 0.1, "LAM_NE": 0.2, "LLI": 0.3})
        args = SimpleNamespace(
            data_root=str(t), source="GITT", state="100", si_source="Li", w_dqdv=0.0,
            seed=0, starts=0, grid=2, profile_scale="global", tol=0.01,
            out=str(art), run_id="r10-profile",
        )
        out = io.StringIO()
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
                rc = V.cmd_profile(args)
        finally:
            p.close()
        rows = list(csv.DictReader(io.StringIO(art.read_text(encoding="utf-8"))))
        problems = S.check_rows("profile", rows, list(rows[0]) if rows else [])

        # Exercise the real wrapper's metadata publisher/receipt verifier on the
        # partial bytes (source only the definitions, not the main loop).
        prefix = t / "run_states_defs.sh"
        prefix.write_text("\n".join((target / "scripts" / "run_states.sh").read_text(encoding="utf-8").splitlines()[:218]) + "\n",
                          encoding="utf-8")
        shell = r'''
source "$DEFS"
cd "$TARGET"
STARTS=0; SI=Li; OUT="$(dirname "$ART")"; LAST_RUN_ID=r10-profile
LAST_ARGV='python3 -m bms_balancing.verify profile --state 100 --grid 2'
LAST_PRE_PV='{}'; LAST_STARTED_UTC='2026-09-13T00:00:00Z'
write_meta "$ART" 100 GITT
python3 scripts/provenance.py --verify-unit "$ART" r10-profile
'''
        signed = subprocess.run(
            ["bash", "-c", shell], capture_output=True, text=True,
            env={**__import__("os").environ, "DEFS": str(prefix), "TARGET": str(target),
                 "ART": str(art), "BMS_DATA_ROOT": str(t), "OUT": str(t)},
        )
        result = {
            "case": "profile_partial_promoted",
            "rc": rc,
            "requested_gamma_count": 2,
            "published_gamma_count": len(rows),
            "schema_problems": problems,
            "real_wrapper_signed_and_verified": signed.returncode == 0 and "일치" in signed.stdout,
            "wrapper_stdout": signed.stdout.splitlines()[-3:],
            "wrapper_stderr": signed.stderr.splitlines()[-3:],
            "previous_canonical_destroyed": art.read_bytes() != old,
            "stdout_mentions_skipped": "gamma_all_failed" in out.getvalue() or "저장하지 않는다" in out.getvalue(),
            "tail": out.getvalue().splitlines()[-8:],
        }
        assert rc == 0 and len(rows) == 1 and not problems and result["previous_canonical_destroyed"] \
            and result["real_wrapper_signed_and_verified"], result
        return result


def case_matrix_all_errors_overwrite(target: Path):
    """All model combinations fail; malformed error-only CSV still replaces canonical with rc 0."""
    S, V = load_target(target)
    p = Patch()
    with tempfile.TemporaryDirectory(prefix="r10-matrix-") as td:
        t = Path(td)
        art = t / "matrix_100.csv"
        old = b"PREVIOUS COMPLETE CANONICAL\n"
        art.write_bytes(old)

        class Exists:
            def is_file(self):
                return True

        p.set(V.D, "data_root", lambda _x=None: t)
        p.set(V.D, "half_cell_path", lambda *_a, **_k: Exists())
        p.set(V, "build", lambda *_a, **_k: (_ for _ in ()).throw(RuntimeError("forced build failure")))
        args = SimpleNamespace(
            data_root=str(t), state="100", source="GITT", only_source=True,
            only_wdqdv=False, w_dqdv=0.0, seed=0, starts=0,
            out=str(art), run_id="r10-matrix",
        )
        out = io.StringIO()
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
                rc_obj = V.cmd_matrix(args)
        finally:
            p.close()
        rows = list(csv.DictReader(io.StringIO(art.read_text(encoding="utf-8"))))
        header = list(rows[0]) if rows else []
        problems = S.check_rows("matrix", rows, header)
        result = {
            "case": "matrix_all_errors_overwrite",
            "python_return": rc_obj,
            "effective_process_rc": 0 if rc_obj is None else int(rc_obj),
            "published_rows": len(rows),
            "header": header,
            "schema_problem_count": len(problems),
            "schema_problem_sample": problems[:5],
            "previous_canonical_destroyed": art.read_bytes() != old,
        }
        assert rc_obj is None and rows and problems and result["previous_canonical_destroyed"], result
        return result


def case_stdout_invalid_success(target: Path):
    """Degeneracy stdout mode emits an invalid artifact but returns process success."""
    S, V = load_target(target)
    p = Patch()
    with tempfile.TemporaryDirectory(prefix="r10-stdout-") as td:
        t = Path(td)

        class FakeObjective:
            # Missing consumed_inputs/inputs_sha is the real schema violation.
            c_cell = 1.0
            scale_audit = None

            def __call__(self, _q):
                return 1.0

        modes = {"LAM_PE": 0.1, "LAM_NE": 0.2, "LLI": 0.3}
        ext = {k: {"min": v * 100, "max": v * 100} for k, v in modes.items()}
        p.set(V.D, "data_root", lambda _x=None: t)
        p.set(V, "build", lambda *_a, **_k: FakeObjective())
        p.set(V, "multistart", lambda *_a, **_k: (np.array([1.0, 0.0, 1.0, 0.0, 0.2]), 1.0, []))
        p.set(V, "degradation_modes", lambda *_a, **_k: dict(modes))
        p.set(V, "near_optimal_extrema", lambda *_a, **_k: ext)
        p.set(V, "mode_profile_extrema", lambda *_a, **_k: ext)
        args = SimpleNamespace(
            data_root=str(t), source="GITT", state="100", si_source="Li", w_dqdv=0.0,
            seed=0, starts=0, grid=2, samples=0, tol=0.01,
            out=None, run_id="r10-stdout",
        )
        stdout, stderr = io.StringIO(), io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                rc_obj = V.cmd_degeneracy(args)
        finally:
            p.close()
        j = json.loads(stdout.getvalue())
        problems = S.check_degeneracy(j)
        result = {
            "case": "stdout_invalid_success",
            "python_return": rc_obj,
            "effective_process_rc": 0 if rc_obj is None else int(rc_obj),
            "schema_problems": problems,
            "stderr_warning": stderr.getvalue().strip(),
            "stdout_is_json_object": isinstance(j, dict),
        }
        assert rc_obj is None and problems and isinstance(j, dict), result
        return result


def case_receipt_role_permutation(target: Path):
    """Aggregate digest and validator do not bind a digest to its input role."""
    S, _V = load_target(target)
    good, dg = receipt(S)
    swapped = dict(good)
    swapped["half_cell"], swapped["full_cell"] = good["full_cell"], good["half_cell"]
    ds = S.inputs_digest(swapped)
    result = {
        "case": "receipt_role_permutation",
        "original_digest": dg,
        "swapped_digest": ds,
        "same_aggregate": dg == ds,
        "validator_original": S.validate_receipt(good, dg, "original"),
        "validator_swapped": S.validate_receipt(swapped, ds, "swapped"),
        "roles_changed": good["half_cell"]["sha256"] != swapped["half_cell"]["sha256"],
    }
    assert result["same_aggregate"] and not result["validator_swapped"] and result["roles_changed"], result
    return result


def case_error_column_bypasses_provenance(target: Path):
    """An extra truthy `error` cell disables every matrix row/content check.

    Numeric cells are kept equal to the baseline, while provenance cells are
    blanked.  check_u14 treats the extra column as informational and returns 0.
    """
    S, V = load_target(target)
    with tempfile.TemporaryDirectory(prefix="r10-error-skip-") as td:
        t = Path(td)
        old, new = t / "old", t / "new"
        old.mkdir(); new.mkdir()
        ci, digest = receipt(S)

        def row(rid):
            r = {k: "1" for k in S.MATRIX_ROW}
            r.update(
                half_cell="GITT", si="Li", w_dqdv="0", run_id=rid,
                inputs_sha=digest, ref_inputs_sha=digest,
                consumed_inputs=json.dumps(ci), ref_consumed_inputs=json.dumps(ci),
                scale_audit_target="", scale_audit_ref="", bounds="-", ref_bounds="-",
            )
            return {k: r[k] for k in S.MATRIX_ROW}

        def sign(path, rid):
            meta = {
                "artifact": path.name, "state": "100", "run_id": rid,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "env": {"python": "test"}, "started_utc": "2026-09-13T00:00:00Z",
                "git_commit_at_start": "0" * 40, "git_state_changed_during_run": False,
                "half_cell_source": "GITT", "si_source": "Li", "starts": 24, "seed": 0,
            }
            path.with_name(path.name + ".meta.json").write_text(json.dumps(meta), encoding="utf-8")

        fo = old / "matrix_100.csv"
        V.atomic_write_csv(fo, [row("old")], list(S.MATRIX_ROW)); sign(fo, "old")
        attacked = row("new")
        attacked.update(error="skip all validation", inputs_sha="", ref_inputs_sha="",
                        consumed_inputs="", ref_consumed_inputs="")
        fn = new / "matrix_100.csv"
        V.atomic_write_csv(fn, [attacked], [*S.MATRIX_ROW, "error"]); sign(fn, "new")

        p = subprocess.run(
            [sys.executable, str(target / "scripts" / "check_u14.py"),
             "--new", str(new), "--old", str(old)],
            cwd=target, capture_output=True, text=True,
            env={**__import__("os").environ, "PYTHONPATH": str(target)},
        )
        result = {
            "case": "error_column_bypasses_provenance",
            "rc": p.returncode,
            "direct_schema_problems": S.check_rows("matrix", [attacked], [*S.MATRIX_ROW, "error"]),
            "blank_provenance": all(attacked[k] == "" for k in ("inputs_sha", "ref_inputs_sha", "consumed_inputs", "ref_consumed_inputs")),
            "says_schema_complete": "새 스키마: 전부 갖췄다" in p.stdout,
            "says_numbers_equal": "숫자: 정본" in p.stdout and "전부 같다" in p.stdout,
            "tail": p.stdout.splitlines()[-10:],
        }
        assert p.returncode == 0 and not result["direct_schema_problems"] and result["blank_provenance"], result
        return result


def case_argv_flattening(_target: Path):
    """run_states.sh line 173 stores $*, so distinct argv vectors collapse."""
    code = r'''
f() {
  flat="$*"
  observed="$($@ 2>/dev/null)"
  python3 -c 'import json,sys; print(json.dumps({"flat":sys.argv[1],"observed":sys.argv[2]}))' "$flat" "$observed"
}
# The command is the same, but the two trailing argv vectors are ["A B","C"] and ["A","B C"].
f python3 -c 'import sys;print(sys.argv[1])' 'A B' C
f python3 -c 'import sys;print(sys.argv[1])' A 'B C'
'''
    # Use an explicit shell array to execute correctly; capture the actual $* separately.
    code = r'''
f() {
  flat="$*"
  observed="$("$@")"
  python3 -c 'import json,sys; print(json.dumps({"flat":sys.argv[1],"observed":sys.argv[2]}))' "$flat" "$observed"
}
f python3 -c 'import sys;print(sys.argv[1])' 'A B' C
f python3 -c 'import sys;print(sys.argv[1])' A 'B C'
'''
    p = subprocess.run(["bash", "-c", code], capture_output=True, text=True, check=True)
    rows = [json.loads(x) for x in p.stdout.splitlines() if x.strip()]
    result = {
        "case": "argv_flattening",
        "records": rows,
        "same_recorded_argv": rows[0]["flat"] == rows[1]["flat"],
        "different_execution": rows[0]["observed"] != rows[1]["observed"],
    }
    assert result["same_recorded_argv"] and result["different_execution"], result
    return result


CASES = {
    "eval-self-overwrite": case_eval_self_overwrite,
    "profile-partial": case_profile_partial_promoted,
    "matrix-errors": case_matrix_all_errors_overwrite,
    "stdout-invalid": case_stdout_invalid_success,
    "receipt-roles": case_receipt_role_permutation,
    "error-skip": case_error_column_bypasses_provenance,
    "argv": case_argv_flattening,
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True, type=Path)
    ap.add_argument("--case", choices=["all", *CASES], default="all")
    ap.add_argument("--output", type=Path)
    a = ap.parse_args()
    selected = CASES if a.case == "all" else {a.case: CASES[a.case]}
    out = {}
    for name, fn in selected.items():
        try:
            out[name] = {"ok": True, "result": fn(a.target.resolve())}
        except Exception as exc:  # reviewer runner should preserve the failed case
            out[name] = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
    rendered = json.dumps(out, ensure_ascii=False, indent=2) + "\n"
    if a.output:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if all(x["ok"] for x in out.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
