#!/usr/bin/env python3
"""Reviewer-only R9 aggregation/inventory counterexamples for SHA 29ef5058."""
from __future__ import annotations

import contextlib
import csv
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


WORKSPACE = Path(__file__).resolve().parents[1]
TARGET = WORKSPACE / "work" / "harness-r9-target-wsl" / "bms-balancing"
OUT = WORKSPACE / "outputs"
CASE_ROOT = Path(tempfile.mkdtemp(prefix="r9_aggregation_cases_", dir=OUT))


def signed_meta(path: Path, rid: str, state: str = "100") -> None:
    meta = {
        "artifact": path.name,
        "state": state,
        "run_id": rid,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "env": {"python": "review-fixture"},
        "started_utc": "2026-09-13T00:00:00+00:00",
        "git_commit_at_start": "29ef5058e68c0c64dba840ecc5a7495644cb092e",
        "git_state_changed_during_run": False,
    }
    path.with_name(path.name + ".meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def write_json_unit(path: Path, rid: str, state: str) -> None:
    spans = {"LAM_PE": 2.0, "LAM_NE": 3.0, "LLI": 1.0}
    obj = {
        "run_id": rid,
        "state": state,
        "half_cell": "GITT",
        "si_source": "Li",
        "n_grid": 21,
        "n_samples": 400,
        "env": {"python": "review-fixture"},
        "consumed_inputs": {"full_cell": {"path": "full.xlsx", "sha256": "1" * 64}},
        "inputs_sha": "a" * 12,
        "n_accepted": 1,
        "best_obj": 1.0,
        "best_p": [1, 2, 3, 4, 0.2],
        "ref_p": [1, 2, 3, 4, 0.2],
        "best_modes_percent": {"LAM_PE": 1.0, "LAM_NE": 2.0, "LLI": 3.0},
    }
    for key, span in spans.items():
        obj[key + "_percent"] = {"min": 0.0, "max": span, "span": span}
        obj[key + "_percent_observed_cloud"] = {"min": 0.0, "max": span, "span": span}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    signed_meta(path, rid, state)


def write_legacy_degeneracy(path: Path) -> None:
    obj = {
        "half_cell": "GITT",
        "best_modes_percent": {"LAM_PE": 1.0, "LAM_NE": 2.0, "LLI": 3.0},
        "LAM_PE_percent": {"min": 0.0, "max": 2.0, "span": 2.0},
        "LAM_NE_percent": {"min": 0.0, "max": 3.0, "span": 3.0},
        "LLI_percent": {"min": 0.0, "max": 1.0, "span": 1.0},
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj) + "\n", encoding="utf-8")


def write_csv_unit(path: Path, fieldnames: list[str], rows: list[dict], rid: str, state: str = "100") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    signed_meta(path, rid, state)


def run_cli(*argv: str) -> dict:
    p = subprocess.run(
        [sys.executable, *argv], cwd=TARGET, capture_output=True, text=True, timeout=120
    )
    return {"command": [sys.executable, *argv], "rc": p.returncode, "stdout": p.stdout, "stderr": p.stderr}


def matrix_row(rid: str, gamma: str = "0.25", lli: str = "1.0", provenance: str | None = None) -> dict:
    prov = provenance if provenance is not None else json.dumps(
        {"half_cell": {"path": "half.xlsx", "sha256": "2" * 64}}, separators=(",", ":")
    )
    return {
        "half_cell": "GITT", "si": "Li", "w_dqdv": "0",
        "LAM_PE_pct": "1.0", "LAM_NE_pct": "2.0", "LLI_pct": lli,
        "bounds": "-", "ref_bounds": "-", "gamma_Si": gamma, "ref_gamma_Si": "0.2",
        "run_id": rid, "inputs_sha": "a" * 12, "scale_seed": "0", "n_scale_samples": "50",
        "ref_inputs_sha": "b" * 12 if provenance is None else provenance,
        "consumed_inputs": prov, "ref_consumed_inputs": prov,
    }


MATRIX_FIELDS = list(matrix_row("template"))


def load_ne_shape():
    sys.path.insert(0, str(TARGET))
    sys.path.insert(0, str(TARGET / "scripts"))
    spec = importlib.util.spec_from_file_location("r9_ne_shape", TARGET / "scripts" / "ne_shape.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def run_shape(ns, case: Path, states: list[str], available: set[str], matrix_dir: Path, output_dir: Path) -> dict:
    import numpy as np
    from bms_balancing.model import Blend

    u = np.linspace(0.0, 1.0, 301)
    arrays = ((1.0 - u) ** 2, 0.1 + 0.7 * u, 1.0 - u, 0.1 + 0.7 * u)
    blend = Blend(*arrays, window=11, poly_order=3)
    offsets = {"pristine": 0.0, "100": 0.01, "200": 0.10}

    class FakePath:
        def __init__(self, state: str): self.state = state
        def is_file(self): return self.state in available
        def __str__(self): return self.state

    class FakeInput:
        def __init__(self, path): self.path = path
        def stream(self): return self.path
        def identity(self):
            return {"path": self.path.state, "sha256": hashlib.sha256(self.path.state.encode()).hexdigest()}

    class FakeHalfCell:
        def __init__(self, path, **_): self.state = path.state
        def E_NE(self, x): return blend.E(x, 0.2) + offsets[self.state]
        def E_PE(self, x): return 4.2 - 0.7 * np.asarray(x)

    def fake_literature(_root, _source, identity=None):
        if identity is not None:
            identity.update({"si": {"path": "si.csv", "sha256": "3" * 64},
                             "gr": {"path": "gr.xlsx", "sha256": "4" * 64}})
        return arrays

    ns.D.STATES = states
    ns.D.data_root = lambda *_a, **_k: case
    ns.D.half_cell_path = lambda _root, _source, state: FakePath(state)
    ns.D.read_input = lambda path: FakeInput(path)
    ns.D.load_literature = fake_literature
    ns.HalfCell = FakeHalfCell
    ns.raw_ne_capacity = lambda _path: 1.0

    old_argv = sys.argv
    sys.argv = ["ne_shape.py", "--out-dir", str(matrix_dir), "--write", str(output_dir)]
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            rc = ns.main()
    finally:
        sys.argv = old_argv
    artifact = output_dir / "ne_shape_GITT_Li.csv"
    meta = json.loads(artifact.with_name(artifact.name + ".meta.json").read_text(encoding="utf-8"))
    return {"rc": rc, "stdout": buf.getvalue(), "pairing": meta.get("pairing"),
            "consumed_inputs": meta.get("consumed_inputs")}


def main() -> int:
    results: dict[str, object] = {"target": str(TARGET), "case_root": str(CASE_ROOT)}

    # compare_states: repeated label overwrites the earlier requested root in the parser dict.
    compare = CASE_ROOT / "compare"
    missing = compare / "missing"
    good = compare / "good"
    write_legacy_degeneracy(good / "degeneracy_100_Li.json")
    script = str(TARGET / "scripts" / "compare_states.py")
    results["compare_duplicate_label"] = run_cli(script, f"same={missing}", f"same={good}")
    results["compare_unique_label_control"] = run_cli(script, f"missing={missing}", f"good={good}")

    # check_u14: an artifact present only in the baseline is never inventoried.
    roster = CASE_ROOT / "u14_roster"
    old, new = roster / "old", roster / "new"
    write_json_unit(old / "degeneracy_100_Li.json", "old-100", "100")
    write_json_unit(old / "degeneracy_200_Li.json", "old-200", "200")
    write_json_unit(new / "degeneracy_100_Li.json", "new-100", "100")
    u14 = str(TARGET / "scripts" / "check_u14.py")
    results["u14_missing_new_artifact"] = run_cli(u14, "--new", str(new), "--old", str(old))

    # A core scientific column can disappear because only the intersection is compared and it is not required.
    dropped = CASE_ROOT / "u14_dropped_column"
    old, new = dropped / "old", dropped / "new"
    old_row, new_row = matrix_row("old-drop"), matrix_row("new-drop")
    write_csv_unit(old / "matrix_100.csv", MATRIX_FIELDS, [old_row], "old-drop")
    new_fields = [x for x in MATRIX_FIELDS if x != "LLI_pct"]
    new_row.pop("LLI_pct")
    write_csv_unit(new / "matrix_100.csv", new_fields, [new_row], "new-drop")
    results["u14_dropped_numeric_column"] = run_cli(u14, "--new", str(new), "--old", str(old))

    # Required provenance headers with empty cells are treated as complete.
    blank = CASE_ROOT / "u14_blank_provenance"
    old, new = blank / "old", blank / "new"
    for directory, rid in ((old, "old-blank"), (new, "new-blank")):
        row = matrix_row(rid, provenance="")
        row["ref_inputs_sha"] = ""
        write_csv_unit(directory / "matrix_100.csv", MATRIX_FIELDS, [row], rid)
    results["u14_blank_provenance"] = run_cli(u14, "--new", str(new), "--old", str(old))

    # R8-05 works in comparison mode, but schema-only never runs duplicate-key validation.
    dup = CASE_ROOT / "u14_duplicate"
    old, new = dup / "old", dup / "new"
    write_csv_unit(old / "matrix_100.csv", MATRIX_FIELDS, [matrix_row("old-dup")], "old-dup")
    rows = [matrix_row("new-dup", gamma="0.10", lli="1.0"),
            matrix_row("new-dup", gamma="0.40", lli="8.0")]
    write_csv_unit(new / "matrix_100.csv", MATRIX_FIELDS, rows, "new-dup")
    results["u14_duplicate_schema_only"] = run_cli(u14, "--new", str(new), "--schema-only")
    results["u14_duplicate_compare_control"] = run_cli(u14, "--new", str(new), "--old", str(old))

    # Real ne_shape main/reader: missing input states disappear before `requested`, and conflicting duplicate rows are accepted.
    ns = load_ne_shape()
    shape_missing = CASE_ROOT / "shape_missing_input"
    matrix = shape_missing / "matrix"
    write_csv_unit(matrix / "matrix_100.csv", MATRIX_FIELDS, [matrix_row("shape-100")], "shape-100")
    results["shape_missing_input_state"] = run_shape(
        ns, shape_missing, ["pristine", "100", "200"], {"pristine", "100"}, matrix, shape_missing / "out"
    )

    shape_partial = CASE_ROOT / "shape_partial_control"
    matrix = shape_partial / "matrix"
    write_csv_unit(matrix / "matrix_100.csv", MATRIX_FIELDS, [matrix_row("shape-partial")], "shape-partial")
    results["shape_partial_pair_control"] = run_shape(
        ns, shape_partial, ["pristine", "100", "200"], {"pristine", "100", "200"},
        matrix, shape_partial / "out"
    )

    shape_dup = CASE_ROOT / "shape_duplicate_matrix"
    matrix = shape_dup / "matrix"
    rows = [matrix_row("shape-dup", gamma="0.10"), matrix_row("shape-dup", gamma="0.40")]
    write_csv_unit(matrix / "matrix_100.csv", MATRIX_FIELDS, rows, "shape-dup")
    results["shape_duplicate_matrix_rows"] = run_shape(
        ns, shape_dup, ["pristine", "100"], {"pristine", "100"}, matrix, shape_dup / "out"
    )

    shape_dup_reversed = CASE_ROOT / "shape_duplicate_matrix_reversed"
    matrix = shape_dup_reversed / "matrix"
    write_csv_unit(matrix / "matrix_100.csv", MATRIX_FIELDS, list(reversed(rows)), "shape-dup")
    results["shape_duplicate_matrix_rows_reversed"] = run_shape(
        ns, shape_dup_reversed, ["pristine", "100"], {"pristine", "100"},
        matrix, shape_dup_reversed / "out"
    )

    shape_none = CASE_ROOT / "shape_no_pairs"
    matrix = shape_none / "matrix"
    matrix.mkdir(parents=True)
    results["shape_all_pairs_missing_rc"] = run_shape(
        ns, shape_none, ["pristine", "100"], {"pristine", "100"}, matrix, shape_none / "out"
    )

    report = OUT / "r9_aggregation_results.json"
    report.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
