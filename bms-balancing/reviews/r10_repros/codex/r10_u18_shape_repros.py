"""Independent adversarial probes for R10 U18/aggregation/ne_shape changes.

The target checkout is imported and executed but never modified.  Every artifact
created by these probes lives under a TemporaryDirectory.
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile


REV = "bd6ba4749a92f8d441b4d9176eb876bfc6cc287c"


def boot(target: Path):
    target = target.resolve()
    sys.path[:0] = [str(target), str(target / "tests"), str(target / "scripts")]
    from bms_balancing import schema as S
    from bms_balancing import verify
    from test_r7_codex import _sign
    from test_r8_codex import _full_matrix_rows, _pair, _shape_harness
    return target, S, verify, _sign, _full_matrix_rows, _pair, _shape_harness


def cli(target: Path, *args: object):
    return subprocess.run(
        [sys.executable, str(target / "scripts" / "check_u14.py"), *map(str, args)],
        cwd=target,
        capture_output=True,
        text=True,
        timeout=180,
    )


def publish_matrix(verify, sign, directory: Path, rows: list[dict], rid: str,
                   fields: list[str] | None = None) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    f = directory / "matrix_100.csv"
    verify.atomic_write_csv(f, rows, fields or list(rows[0]))
    sign(f, rid, "100", full=True)
    return f


def mutate_meta(f: Path, **changes) -> dict:
    m = f.with_name(f.name + ".meta.json")
    meta = json.loads(m.read_text(encoding="utf-8"))
    for key, value in changes.items():
        if value is DELETE:
            meta.pop(key, None)
        else:
            meta[key] = value
    m.write_text(json.dumps(meta), encoding="utf-8")
    return meta


DELETE = object()


def same_root_is_vacuous(target, verify, sign, full_rows):
    with tempfile.TemporaryDirectory(prefix="r10-u18-same-root-") as td:
        d = Path(td) / "candidate"
        publish_matrix(verify, sign, d, full_rows("same-root"), "same-root")
        p = cli(target, "--new", d, "--old", d)
        result = {
            "case": "candidate_and_baseline_can_be_the_same_directory",
            "rc": p.returncode,
            "same_resolved_directory": True,
            "claims_all_same": "전부 같다" in p.stdout,
            "stdout": p.stdout,
        }
        assert p.returncode == 0 and result["claims_all_same"], result
        return result


def receipt_role_roster_is_not_checked(target, S, verify, sign, full_rows):
    with tempfile.TemporaryDirectory(prefix="r10-u18-receipt-") as td:
        old, new = Path(td) / "old", Path(td) / "new"
        publish_matrix(verify, sign, old, full_rows("receipt-old"), "receipt-old")
        rows = full_rows("receipt-new")
        decoy = {"decoy": {"path": "not-a-model-input.bin", "sha256": "a" * 64}}
        for r in rows:
            r["consumed_inputs"] = json.dumps(decoy)
            r["ref_consumed_inputs"] = json.dumps(decoy)
            r["inputs_sha"] = S.inputs_digest(decoy)
            r["ref_inputs_sha"] = S.inputs_digest(decoy)
        publish_matrix(verify, sign, new, rows, "receipt-new")
        p = cli(target, "--new", new, "--old", old)
        result = {
            "case": "receipt_accepts_a_decoy_instead_of_required_input_roles",
            "rc": p.returncode,
            "recorded_roles": sorted(decoy),
            "missing_producer_roles": ["half_cell", "full_cell", "literature.gr", "literature.si"],
            "claims_schema_complete": "전부 갖췄다" in p.stdout,
            "claims_all_same": "전부 같다" in p.stdout,
            "stdout": p.stdout,
        }
        assert p.returncode == 0 and result["claims_schema_complete"] and result["claims_all_same"], result
        return result


def environment_and_controls_are_not_closed(target, verify, sign, full_rows):
    with tempfile.TemporaryDirectory(prefix="r10-u18-controls-") as td:
        base = Path(td)
        records = {}
        for mode in ("environment_changed", "controls_removed"):
            old, new = base / mode / "old", base / mode / "new"
            publish_matrix(verify, sign, old, full_rows(mode + "-old"), mode + "-old")
            nf = publish_matrix(verify, sign, new, full_rows(mode + "-new"), mode + "-new")
            if mode == "environment_changed":
                mutate_meta(nf, env={"python": "9.9", "numpy": "999", "scipy": "999", "platform": "alien"})
            else:
                mutate_meta(nf, state=DELETE, starts=DELETE)
            p = cli(target, "--new", new, "--old", old)
            records[mode] = {
                "rc": p.returncode,
                "claims_all_same": "전부 같다" in p.stdout,
                "reports_control_mismatch": "실행 조건 불일치" in p.stdout,
                "stdout": p.stdout,
            }
            assert p.returncode == 0 and records[mode]["claims_all_same"], records[mode]
            assert not records[mode]["reports_control_mismatch"], records[mode]
        return {"case": "environment_can_change_and_controls_can_disappear", **records}


def error_column_bypasses_row_validation(target, S, verify, sign, full_rows):
    with tempfile.TemporaryDirectory(prefix="r10-u18-error-bypass-") as td:
        old, new = Path(td) / "old", Path(td) / "new"
        publish_matrix(verify, sign, old, full_rows("error-old"), "error-old")
        rows = full_rows("error-new")
        for r in rows:
            r["inputs_sha"] = ""
            r["ref_inputs_sha"] = ""
            r["consumed_inputs"] = ""
            r["ref_consumed_inputs"] = ""
            r["error"] = "pretend this otherwise-complete row failed"
        publish_matrix(verify, sign, new, rows, "error-new", list(S.MATRIX_ROW) + ["error"])
        p = cli(target, "--new", new, "--old", old)
        result = {
            "case": "extra_error_column_skips_all_required_cell_and_receipt_checks",
            "rc": p.returncode,
            "provenance_cells_blank": all(not r[c] for r in rows for c in
                                           ("inputs_sha", "ref_inputs_sha", "consumed_inputs", "ref_consumed_inputs")),
            "claims_schema_complete": "전부 갖췄다" in p.stdout,
            "claims_all_same": "전부 같다" in p.stdout,
            "stdout": p.stdout,
        }
        assert result["provenance_cells_blank"], result
        assert p.returncode == 0 and result["claims_schema_complete"] and result["claims_all_same"], result
        return result


def run_shape(ns, mp, matrix: Path, out: Path, states: str | None = None):
    argv = ["ne_shape.py", "--out-dir", str(matrix), "--write", str(out)]
    if states is not None:
        argv += ["--states", states]
    buf = io.StringIO()
    mp.setattr(sys, "argv", argv)
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        rc = ns.main()
    f = out / "ne_shape_GITT_Li.csv"
    rows = list(csv.DictReader(io.StringIO(f.read_text(encoding="utf-8")))) if f.is_file() else []
    meta = json.loads(f.with_name(f.name + ".meta.json").read_text(encoding="utf-8")) if f.is_file() else None
    return rc, buf.getvalue(), f, rows, meta


def states_subset_replaces_complete_canonical(pair, shape_harness):
    import pytest
    with tempfile.TemporaryDirectory(prefix="r10-shape-subset-") as td:
        base = Path(td); matrix = base / "matrix"; out = base / "shape"; matrix.mkdir()
        mp = pytest.MonkeyPatch()
        try:
            ns = shape_harness(mp, base, {"pristine": 0.0, "100": 0.01, "200": 0.10})
            pair(matrix, "100"); pair(matrix, "200")
            rc1, text1, f, rows1, meta1 = run_shape(ns, mp, matrix, out)
            complete_bytes = f.read_bytes()
            rc2, text2, f, rows2, meta2 = run_shape(ns, mp, matrix, out, "100")
            result = {
                "case": "states_option_narrows_roster_then_publishes_as_complete_canonical",
                "declared_states": ["100", "200"],
                "first": {"rc": rc1, "rows": [r["state"] for r in rows1], "pairing": meta1["pairing"],
                          "status": meta1["status"]},
                "narrowed": {"rc": rc2, "rows": [r["state"] for r in rows2], "pairing": meta2["pairing"],
                             "status": meta2["status"], "stdout": text2},
                "canonical_replaced": complete_bytes != f.read_bytes(),
            }
            assert rc1 == 0 and [r["state"] for r in rows1] == ["100", "200"], result
            assert rc2 == 0 and [r["state"] for r in rows2] == ["100"], result
            assert meta2["status"] == "complete" and result["canonical_replaced"], result
            return result
        finally:
            mp.undo()


def duplicate_requested_states_are_complete(pair, shape_harness):
    import pytest
    with tempfile.TemporaryDirectory(prefix="r10-shape-duplicates-") as td:
        base = Path(td); matrix = base / "matrix"; out = base / "shape"; matrix.mkdir()
        mp = pytest.MonkeyPatch()
        try:
            ns = shape_harness(mp, base, {"pristine": 0.0, "100": 0.01, "200": 0.10})
            pair(matrix, "100")
            rc, text, _f, rows, meta = run_shape(ns, mp, matrix, out, "100,100")
            result = {
                "case": "duplicate_requested_states_count_twice_and_publish_complete",
                "rc": rc,
                "rows": [r["state"] for r in rows],
                "pairing": meta["pairing"],
                "status": meta["status"],
                "stdout": text,
            }
            assert rc == 0 and result["rows"] == ["100", "100"], result
            assert meta["pairing"]["requested"] == ["100", "100"] and meta["status"] == "complete", result
            return result
        finally:
            mp.undo()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=Path, required=True)
    ap.add_argument("--output", type=Path)
    a = ap.parse_args()
    target, S, verify, sign, full_rows, pair, shape_harness = boot(a.target)
    head = subprocess.check_output(["git", "-C", str(target), "rev-parse", "HEAD"], text=True).strip()
    assert head == REV, (head, REV)
    results = {
        "target": head,
        "same_root": same_root_is_vacuous(target, verify, sign, full_rows),
        "receipt_roles": receipt_role_roster_is_not_checked(target, S, verify, sign, full_rows),
        "controls": environment_and_controls_are_not_closed(target, verify, sign, full_rows),
        "error_bypass": error_column_bypasses_row_validation(target, S, verify, sign, full_rows),
        "shape_subset": states_subset_replaces_complete_canonical(pair, shape_harness),
        "shape_duplicates": duplicate_requested_states_are_complete(pair, shape_harness),
    }
    rendered = json.dumps(results, ensure_ascii=False, indent=2)
    print(rendered)
    if a.output:
        a.output.write_text(rendered + "\n", encoding="utf-8")
    print("R10_U18_SHAPE_REPROS_PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
