#!/usr/bin/env python3
"""Reviewer-only R9 provenance reproductions. Never writes into the target tree."""
from __future__ import annotations

import contextlib
import csv
import hashlib
import importlib.util
import io
import json
import os
import pathlib
import shutil
import subprocess
import sys
from types import SimpleNamespace


ROOT = pathlib.Path(__file__).resolve().parents[1]
TARGET = ROOT / "work" / "harness-r9-target-wsl" / "bms-balancing"
OUT = ROOT / "outputs"
ART = OUT / "r9_provenance_artifacts"
ART.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(TARGET))

from bms_balancing import verify  # noqa: E402


def load(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


prov = load("r9_provenance", TARGET / "scripts" / "provenance.py")
u14 = load("r9_check_u14", TARGET / "scripts" / "check_u14.py")


def run_u14(new: pathlib.Path, old: pathlib.Path, schema_only: bool = False) -> dict:
    argv = [sys.executable, str(TARGET / "scripts" / "check_u14.py"), "--new", str(new), "--old", str(old)]
    if schema_only:
        argv.append("--schema-only")
    p = subprocess.run(argv, cwd=TARGET, text=True, capture_output=True, timeout=120)
    return {"argv": argv, "returncode": p.returncode, "stdout": p.stdout, "stderr": p.stderr}


def sign_like_wrapper(art: pathlib.Path, source_meta: pathlib.Path) -> None:
    meta = json.loads(source_meta.read_text(encoding="utf-8"))
    meta["artifact"] = art.name
    meta["sha256"] = prov.sha256_file(art)
    art.with_name(art.name + ".meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def u18_roster_and_receipt() -> dict:
    canonical = TARGET / "out"
    current_schema = run_u14(canonical, canonical, schema_only=True)

    # Exact, signed production artifact, but only 1/12 of the U18 roster.
    single = ART / "u18_one_of_twelve"
    single.mkdir(exist_ok=True)
    for name in ("degeneracy_100_Li.json", "degeneracy_100_Li.json.meta.json"):
        shutil.copy2(canonical / name, single / name)
    one = run_u14(single, canonical)

    # Use the production CSV publisher to add all required provenance *headers* while
    # leaving every receipt value blank. The production reader verifies the signed unit.
    # check_u14 nevertheless accepts it because it checks header membership only.
    blank = ART / "u18_blank_receipts"
    blank.mkdir(exist_ok=True)
    for old_art in sorted(canonical.glob("degeneracy_*.json")):
        if old_art.name.endswith(".meta.json"):
            continue
        new_art = blank / old_art.name
        shutil.copy2(old_art, new_art)
        sign_like_wrapper(new_art, canonical / (old_art.name + ".meta.json"))
    sample_rows = None
    for old_art in sorted(canonical.glob("matrix_*.csv")) + sorted(canonical.glob("profile_gamma_*.csv")):
        rows = list(csv.DictReader(io.StringIO(old_art.read_text(encoding="utf-8-sig"))))
        fieldnames = list(rows[0])
        for col in u14.PROVENANCE_COLS:
            if col not in fieldnames:
                fieldnames.append(col)
            for row in rows:
                row[col] = ""
        new_art = blank / old_art.name
        verify.atomic_write_csv(new_art, rows, fieldnames)
        sign_like_wrapper(new_art, canonical / (old_art.name + ".meta.json"))
        if old_art.name == "matrix_100.csv":
            sample_rows = rows
    assert sample_rows is not None
    ok, why, _, _ = prov.read_unit(blank / "matrix_100.csv")
    blank_check = run_u14(blank, canonical)

    # A signed JSON can also disagree with its sidecar about the run configuration.
    # These fields are required to exist but are not part of check_u14's comparison.
    config = ART / "u18_config_mismatch"
    config.mkdir(exist_ok=True)
    src_json = canonical / "degeneracy_100_Li.json"
    obj = json.loads(src_json.read_text(encoding="utf-8"))
    before_config = {k: obj.get(k) for k in ("n_starts", "seed", "n_grid", "n_samples", "tol_percent_of_best")}
    obj.update(n_starts=1, seed=731, n_grid=999, n_samples=1, tol_percent_of_best=50.0)
    changed = config / src_json.name
    verify.atomic_write_json(changed, obj)
    sign_like_wrapper(changed, canonical / (src_json.name + ".meta.json"))
    after_config = {k: obj.get(k) for k in before_config}
    config_check = run_u14(config, canonical)

    return {
        "current_out_schema": current_schema,
        "one_of_twelve": one,
        "one_of_twelve_files": sorted(p.name for p in single.iterdir()),
        "blank_receipts": blank_check,
        "blank_unit_verified_by_production_reader": [ok, why],
        "blank_artifact_count": len(list(blank.glob("*.csv"))) + len(
            [p for p in blank.glob("*.json") if not p.name.endswith(".meta.json")]
        ),
        "blank_first_row": {c: sample_rows[0].get(c) for c in u14.PROVENANCE_COLS},
        "config_mismatch": config_check,
        "config_before": before_config,
        "config_after": after_config,
    }


def make_eval_fixture(path: pathlib.Path):
    """A compact full-schema dd_eval fixture matching supplied Python values."""
    P = verify.np.asarray(verify.DD_EVAL_P, dtype=float)
    anchors = {k: float(i + 1) for i, (k, _) in enumerate(verify.ANCHOR_STAGE)}
    cols = ["rmse_pocv", "rmse_dvdq", "rmse_dqdv", "rmse_dqdv_w"]
    vals = {c: [0.001 * (j + 1) * (i + 1) for i in range(len(P))] for j, c in enumerate(cols)}
    lines = ["# printed_format,%.17g"]
    lines += [f"# {k},{v:.17g}" for k, v in anchors.items()]
    header = "a_PE,b_PE,a_NE,b_NE,gamma_Si," + ",".join(cols)
    lines.append(header)
    for i, q in enumerate(P):
        lines.append(",".join([f"{x:.6f}" for x in q] + [f"{vals[c][i]:.17g}" for c in cols]))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return anchors, P, vals, header


def eval_verified_bytes_race() -> dict:
    d = ART / "dd_eval_reread"
    d.mkdir(exist_ok=True)
    p = d / "matlab_eval.csv"
    anchors, P, vals, header = make_eval_fixture(p)
    valid = p.read_text(encoding="utf-8")
    malformed = valid.replace(header + "\n", header + "\n" + header + "\n", 1)
    p.write_text(malformed, encoding="utf-8")

    with contextlib.redirect_stdout(io.StringIO()):
        control = verify._compare_dd_eval(anchors, P, vals, p)

    # Snapshot A (duplicate header) is parsed first. A normal re-export to valid B
    # occurs after that first read. Precision resolution and validation then inspect B.
    p.write_text(malformed, encoding="utf-8")
    original = pathlib.Path.read_text
    reads = {"n": 0, "sha": []}

    def racing_read(self, *args, **kwargs):
        data = original(self, *args, **kwargs)
        if pathlib.Path(self).resolve() == p.resolve():
            reads["n"] += 1
            reads["sha"].append(hashlib.sha256(data.encode()).hexdigest())
            if reads["n"] == 1:
                p.write_text(valid, encoding="utf-8")
        return data

    pathlib.Path.read_text = racing_read
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            raced = verify._compare_dd_eval(anchors, P, vals, p)
    finally:
        pathlib.Path.read_text = original

    return {
        "control_same_malformed_bytes": control["status"],
        "raced_status": raced["status"],
        "read_count": reads["n"],
        "read_sha256": reads["sha"],
        "first_read_was_malformed": reads["sha"][0] == hashlib.sha256(malformed.encode()).hexdigest(),
        "later_reads_were_valid": all(x == hashlib.sha256(valid.encode()).hexdigest() for x in reads["sha"][1:]),
        "raced_compared": raced["compared"],
        "raced_expected": raced["expected"],
    }


def args(root: pathlib.Path, out: pathlib.Path, **overrides):
    obj = SimpleNamespace(
        data_root=str(root), source="GITT", state="100", si_source="Li", w_dqdv=0.0,
        starts=1, seed=0, only_source=True, only_wdqdv=True, out=str(out),
        run_id="r9-production", grid=3, tol=0.01, profile_scale="global", samples=20,
        repeats=1, compare=None, precision="auto", allow_partial=False,
    )
    for key, value in overrides.items():
        setattr(obj, key, value)
    return obj


def production_shared_snapshot_and_profile_receipt() -> dict:
    d = ART / "production"
    d.mkdir(exist_ok=True)
    data_root = d / "data_root"
    subprocess.run(
        [sys.executable, str(TARGET / "matlab" / "tests" / "gen_synth_xlsx.py"), str(data_root)],
        cwd=TARGET, check=True, capture_output=True, text=True, timeout=120,
    )

    # Positive R8-04 closure through the real profile writer and optimizer.
    profile = d / "profile_gamma_100_Li.csv"
    with contextlib.redirect_stdout(io.StringIO()):
        profile_rc = verify.cmd_profile(args(data_root, profile))
    prows = list(csv.DictReader(profile.open(encoding="utf-8")))
    target_ci = json.loads(prows[0]["consumed_inputs"])
    ref_ci = json.loads(prows[0]["ref_consumed_inputs"])
    log = profile.with_name(profile.name + ".log")
    log.write_text("", encoding="utf-8")
    prows_after = list(csv.DictReader(profile.open(encoding="utf-8")))

    # Confirm the currently open Q3 boundary using the real matrix writer/optimizer:
    # re-export the shared full-cell workbook between ref and target build. The row is
    # published without rejection even though target/ref shared-workbook hashes differ.
    wb = data_root / "data" / "full_cell" / "large_cell_033C" / "fullcell_states.xlsx"
    wb_b = wb.with_name("replacement.xlsx")
    import pandas as pd
    frame = pd.read_excel(wb, header=None)
    for col in range(1, frame.shape[1], 2):
        numeric = pd.to_numeric(frame.iloc[2:, col], errors="coerce")
        frame.iloc[2:, col] = numeric + 0.02
    frame.to_excel(wb_b, header=False, index=False)

    matrix = d / "matrix_100.csv"
    original_ms = verify.multistart
    original_sources = verify.D.SI_SOURCES
    calls = {"n": 0}

    def after_reference(obj, *a, **kw):
        result = original_ms(obj, *a, **kw)
        calls["n"] += 1
        if calls["n"] == 1:
            os.replace(wb_b, wb)
        return result

    verify.multistart = after_reference
    verify.D.SI_SOURCES = ["Li"]
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            matrix_rc = verify.cmd_matrix(args(data_root, matrix))
    finally:
        verify.multistart = original_ms
        verify.D.SI_SOURCES = original_sources
    mrow = next(csv.DictReader(matrix.open(encoding="utf-8")))
    mtarget = json.loads(mrow["consumed_inputs"])
    mref = json.loads(mrow["ref_consumed_inputs"])

    return {
        "profile_rc": profile_rc,
        "profile_rows": len(prows),
        "profile_receipts_survive_empty_log": (
            prows_after[0]["consumed_inputs"] == prows[0]["consumed_inputs"]
            and prows_after[0]["ref_consumed_inputs"] == prows[0]["ref_consumed_inputs"]
        ),
        "profile_target_half_hash_matches": target_ci["half_cell"]["sha256"] == prov.sha256_file(target_ci["half_cell"]["path"]),
        "profile_ref_half_hash_matches": ref_ci["half_cell"]["sha256"] == prov.sha256_file(ref_ci["half_cell"]["path"]),
        "matrix_rc": matrix_rc,
        "matrix_rows": 1,
        "shared_full_cell_ref_sha": mref["full_cell"]["sha256"],
        "shared_full_cell_target_sha": mtarget["full_cell"]["sha256"],
        "shared_full_cell_mismatch_accepted": mref["full_cell"]["sha256"] != mtarget["full_cell"]["sha256"],
    }


def main() -> int:
    report = {
        "target_head_expected": "29ef5058e68c0c64dba840ecc5a7495644cb092e",
        "u18_gate": u18_roster_and_receipt(),
        "dd_eval_reread": eval_verified_bytes_race(),
        "production_paths": production_shared_snapshot_and_profile_receipt(),
    }
    destination = OUT / "r9_provenance_repro_results.json"
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
