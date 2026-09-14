#!/usr/bin/env python3
"""Executable reviewer counterexamples for the R11 alpha/beta harness.

The target tree is imported read-only.  All generated artifacts live in
TemporaryDirectory instances.  Run with the same Python environment as the
target's test suite:

    python r11_root_repros.py --target /path/to/bms-balancing \
        --output r11_root_results.json
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


def load_target(target: Path):
    sys.path.insert(0, str(target))
    from bms_balancing import schema as S  # noqa: PLC0415
    from bms_balancing import verify as V  # noqa: PLC0415
    return S, V


def receipt(S, digit: str):
    d = {
        "full_cell": {"path": "full.xlsx", "sha256": digit * 64},
        "half_cell": {"path": "half.xlsx", "sha256": str((int(digit) + 1) % 10) * 64},
        "literature": {
            "gr": {"path": "gr.xlsx", "sha256": str((int(digit) + 2) % 10) * 64},
            "si": {"path": "si.csv", "sha256": str((int(digit) + 3) % 10) * 64},
        },
    }
    return d, S.inputs_digest(d)


def profile_row(S, rid: str, digit: str = "1", **changes):
    rec, digest = receipt(S, digit)
    row = {k: "1" for k in S.PROFILE_ROW}
    row.update(
        gamma_Si="0.2",
        obj="1.0",
        obj_ratio_to_best="1.0",
        rmse_pocv="1.0",
        a_PE="1.0",
        b_PE="0.0",
        a_NE="1.0",
        b_NE="0.0",
        bounds="-",
        LAM_PE_pct="0.0",
        LAM_NE_pct="0.0",
        LLI_pct="0.0",
        n_ok="1",
        n_tried="1",
        run_id=rid,
        profile_scale="global",
        inputs_sha=digest,
        ref_inputs_sha=digest,
        consumed_inputs=json.dumps(rec, sort_keys=True),
        ref_consumed_inputs=json.dumps(rec, sort_keys=True),
        gamma_roster=json.dumps({"requested": 1, "succeeded": 1, "missing": []}, sort_keys=True),
    )
    row.update(changes)
    return row


def publish_profile(S, directory: Path, rid: str, digit: str = "1", row_changes=None, meta_changes=None):
    directory.mkdir(parents=True, exist_ok=True)
    art = directory / "profile_gamma_100_Li.csv"
    row = profile_row(S, rid, digit, **(row_changes or {}))
    with art.open("w", encoding="utf-8", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(S.PROFILE_ROW), lineterminator="\n")
        wr.writeheader()
        wr.writerow(row)
    meta = {
        "artifact": art.name,
        "state": "100",
        "half_cell_source": "GITT",
        "si_source": "Li",
        "starts": 24,
        "seed": 0,
        "run_id": rid,
        "sha256": hashlib.sha256(art.read_bytes()).hexdigest(),
        "env": {"python": "3.12", "numpy": "2", "scipy": "1", "pandas": "2", "platform": "linux"},
        "started_utc": "2026-09-13T00:00:00Z",
        "git_commit_at_start": "665c87e",
        "git_state_changed_during_run": False,
        "git_dirty": False,
        "git_modified_code": [],
    }
    meta.update(meta_changes or {})
    art.with_name(art.name + ".meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return art, row


def run_gate(target: Path, *args):
    p = subprocess.run(
        [sys.executable, str(target / "scripts" / "check_u14.py"), *map(str, args)],
        capture_output=True,
        text=True,
    )
    promo = None
    for line in p.stdout.splitlines():
        if line.startswith("PROMOTION "):
            promo = json.loads(line[len("PROMOTION "):])
    return {"rc": p.returncode, "promotion": promo, "tail": p.stdout.splitlines()[-12:], "stderr": p.stderr[-1000:]}


def case_schema_only_promotes(target: Path, S):
    with tempfile.TemporaryDirectory(prefix="r11-schema-only-") as td:
        new = Path(td) / "new"
        publish_profile(S, new, "schema-only")
        got = run_gate(target, "--new", new, "--schema-only")
        assert got["rc"] == 0 and got["promotion"]["promotion_eligible"] is True, got
        return {"case": "schema_only_without_baseline_promotes", **got}


def case_different_input_bytes_promote(target: Path, S):
    with tempfile.TemporaryDirectory(prefix="r11-input-drift-") as td:
        old, new = Path(td) / "old", Path(td) / "new"
        _, old_row = publish_profile(S, old, "old", "1")
        _, new_row = publish_profile(S, new, "new", "5")
        got = run_gate(target, "--new", new, "--old", old)
        assert old_row["inputs_sha"] != new_row["inputs_sha"], (old_row, new_row)
        assert got["rc"] == 0 and got["promotion"]["promotion_eligible"] is True, got
        return {
            "case": "different_consumed_input_bytes_promote",
            "old_inputs_sha": old_row["inputs_sha"],
            "new_inputs_sha": new_row["inputs_sha"],
            **got,
        }


def case_dirty_changed_code_promotes(target: Path, S):
    with tempfile.TemporaryDirectory(prefix="r11-dirty-meta-") as td:
        old, new = Path(td) / "old", Path(td) / "new"
        publish_profile(S, old, "old")
        publish_profile(
            S,
            new,
            "new",
            meta_changes={
                "git_commit_at_start": "different-code",
                "git_state_changed_during_run": True,
                "git_dirty": True,
                "git_modified_code": ["bms_balancing/model.py"],
            },
        )
        got = run_gate(target, "--new", new, "--old", old)
        assert got["rc"] == 0 and got["promotion"]["promotion_eligible"] is True, got
        return {"case": "dirty_and_changed_code_meta_promotes", **got}


def case_invalid_numeric_schema(target: Path, S):
    cases = {}
    for label, changes in (("nonfinite_obj", {"obj": "inf"}), ("nonnumeric_a_NE", {"a_NE": "not-a-number"})):
        with tempfile.TemporaryDirectory(prefix=f"r11-{label}-") as td:
            old, new = Path(td) / "old", Path(td) / "new"
            _, row = publish_profile(S, old, "old", row_changes=changes)
            publish_profile(S, new, "new", row_changes=changes)
            problems = S.check_rows("profile", [row], list(S.PROFILE_ROW))
            got = run_gate(target, "--new", new, "--old", old)
            assert not problems and got["rc"] == 0 and got["promotion"]["promotion_eligible"] is True, (problems, got)
            cases[label] = {"schema_problems": problems, **got}
    return {"case": "invalid_scientific_numeric_values_promote", "subcases": cases}


class FakeObjective:
    scale_audit = None
    n_scale_samples = 50
    c_cell = 1.0

    def __init__(self, S):
        self.consumed_inputs, self.inputs_sha = receipt(S, "1")
        self.scales = {"pocv": 1.0, "dvdq": 1.0, "dqdv": 1.0}

    def __call__(self, _q):
        return 1.0

    def rmse_pocv(self, _q):
        return 1.0

    def _auto_scales(self, *_a, **_k):
        return dict(self.scales)


def case_matrix_authority_shrinks(S, V):
    p = Patch()
    with tempfile.TemporaryDirectory(prefix="r11-matrix-authority-") as td:
        t = Path(td)
        art = t / "matrix_100.csv"

        class Exists:
            def is_file(self):
                return True

        p.set(V.D, "data_root", lambda *_a, **_k: t)
        p.set(V.D, "HALF_FILE", {"GITT": {"100": "a"}, "step_005C": {"100": "b"}})
        p.set(V.D, "HALF_CELL_ABSENT", frozenset())
        p.set(V.D, "SI_SOURCES", ["Li", "Lu"])
        p.set(V.D, "half_cell_path", lambda *_a, **_k: Exists())
        p.set(V, "build", lambda *_a, **_k: FakeObjective(S))
        p.set(V, "multistart", lambda *_a, **_k: (np.array([1.0, 0.0, 1.0, 0.0, 0.2]), 1.0, []))
        p.set(V, "degradation_modes", lambda *_a, **_k: {"LAM_PE": 0.1, "LAM_NE": 0.2, "LLI": 0.3})

        def args(only_source, only_wdqdv, rid):
            return SimpleNamespace(
                data_root=str(t), state="100", source="GITT", only_source=only_source,
                only_wdqdv=only_wdqdv, w_dqdv=0.0, seed=0, starts=0,
                out=str(art), run_id=rid,
            )

        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                rc_full = V.cmd_matrix(args(False, False, "full"))
            n_full = len(list(csv.DictReader(io.StringIO(art.read_text(encoding="utf-8")))))
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                rc_small = V.cmd_matrix(args(True, True, "small"))
            rows_small = list(csv.DictReader(io.StringIO(art.read_text(encoding="utf-8"))))
            problems = S.check_rows("matrix", rows_small, list(rows_small[0]))
        finally:
            p.close()
        result = {
            "case": "matrix_only_flags_shrink_complete_authority",
            "full_rc": rc_full,
            "full_rows": n_full,
            "narrow_rc": rc_small,
            "narrow_rows": len(rows_small),
            "narrow_schema_problems": problems,
            "canonical_replaced_by_narrow_run": n_full > len(rows_small),
        }
        assert rc_full == rc_small == 0 and n_full == 8 and len(rows_small) == 2 and not problems, result
        return result


def case_profile_grid_shrinks(S, V):
    p = Patch()
    with tempfile.TemporaryDirectory(prefix="r11-profile-authority-") as td:
        t = Path(td)
        art = t / "profile_gamma_100_Li.csv"
        p.set(V.D, "data_root", lambda *_a, **_k: t)
        p.set(V, "build", lambda *_a, **_k: FakeObjective(S))
        p.set(V, "multistart", lambda *_a, **_k: (np.array([1.0, 0.0, 1.0, 0.0, 0.2]), 1.0, []))
        p.set(V, "minimize", lambda *_a, **_k: SimpleNamespace(success=True, fun=1.0, x=np.array([1.0, 0.0, 1.0, 0.0])))
        p.set(V, "degradation_modes", lambda *_a, **_k: {"LAM_PE": 0.1, "LAM_NE": 0.2, "LLI": 0.3})

        def args(grid, rid):
            return SimpleNamespace(
                data_root=str(t), source="GITT", state="100", si_source="Li", w_dqdv=0.0,
                seed=0, starts=0, grid=grid, profile_scale="global", tol=0.01,
                out=str(art), run_id=rid,
            )

        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                rc_full = V.cmd_profile(args(3, "full"))
            n_full = len(list(csv.DictReader(io.StringIO(art.read_text(encoding="utf-8")))))
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                rc_small = V.cmd_profile(args(1, "small"))
            rows_small = list(csv.DictReader(io.StringIO(art.read_text(encoding="utf-8"))))
            problems = S.check_rows("profile", rows_small, list(rows_small[0]))
        finally:
            p.close()
        result = {
            "case": "profile_grid_one_shrinks_complete_authority",
            "full_rc": rc_full,
            "full_rows": n_full,
            "narrow_rc": rc_small,
            "narrow_rows": len(rows_small),
            "narrow_roster": json.loads(rows_small[0]["gamma_roster"]),
            "narrow_schema_problems": problems,
            "canonical_replaced_by_narrow_run": n_full > len(rows_small),
        }
        assert rc_full == rc_small == 0 and n_full == 3 and len(rows_small) == 1 and not problems, result
        return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=Path, required=True)
    ap.add_argument("--output", type=Path)
    a = ap.parse_args()
    target = a.target.resolve()
    S, V = load_target(target)
    results = {
        "target": str(target),
        "cases": [
            case_schema_only_promotes(target, S),
            case_different_input_bytes_promote(target, S),
            case_dirty_changed_code_promotes(target, S),
            case_invalid_numeric_schema(target, S),
            case_matrix_authority_shrinks(S, V),
            case_profile_grid_shrinks(S, V),
        ],
    }
    text = json.dumps(results, ensure_ascii=False, indent=2, default=str)
    print(text)
    if a.output:
        a.output.write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
