"""Independent R9 counterexamples for 29ef5058; target sources are never edited."""
from __future__ import annotations

import argparse
import contextlib
import csv
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


REV = "29ef5058e68c0c64dba840ecc5a7495644cb092e"


def boot(target: Path):
    target = target.resolve()
    sys.path[:0] = [str(target), str(target / "tests"), str(target / "scripts")]
    from bms_balancing import verify
    from test_r6_internal import _prov
    from test_r7_codex import _deg, _sign
    from test_r8_codex import _full_matrix_rows, _shape_harness, _pair
    return target, verify, _prov, _deg, _sign, _full_matrix_rows, _shape_harness, _pair


def run_cli(target: Path, script: str, *args):
    return subprocess.run(
        [sys.executable, str(target / "scripts" / script), *map(str, args)],
        cwd=target,
        capture_output=True,
        text=True,
        timeout=180,
    )


def root_alias(target, verify, _deg, _sign):
    with tempfile.TemporaryDirectory(prefix="r9-root-alias-") as td:
        base = Path(td)
        good, empty = base / "good", base / "empty"
        good.mkdir(); empty.mkdir()
        art = good / "degeneracy_100_Li.json"
        modes = {"LAM_PE": 2.0, "LAM_NE": 3.0, "LLI": 1.0}
        verify.atomic_write_json(art, _deg("100", "r9-root", modes))
        _sign(art, "r9-root", "100")

        missing_first = run_cli(target, "compare_states.py", empty, good)
        missing_last = run_cli(target, "compare_states.py", good, empty)
        duplicate_label = run_cli(target, "compare_states.py", f"same={empty}", f"same={good}")
        result = {
            "case": "root_argument_identity_collapse",
            "missing_first_then_good": {
                "rc": missing_first.returncode,
                "roster": [x for x in missing_first.stdout.splitlines() if "요청한 root" in x or "- out:" in x],
                "verdict": [x for x in missing_first.stdout.splitlines() if "항상 가장 좁은가" in x],
            },
            "good_first_then_missing": {
                "rc": missing_last.returncode,
                "roster": [x for x in missing_last.stdout.splitlines() if "요청한 root" in x or "- out:" in x],
                "verdict": [x for x in missing_last.stdout.splitlines() if "항상 가장 좁은가" in x],
            },
            "duplicate_explicit_label": {
                "rc": duplicate_label.returncode,
                "roster": [x for x in duplicate_label.stdout.splitlines() if "요청한 root" in x or "- same:" in x],
                "verdict": [x for x in duplicate_label.stdout.splitlines() if "항상 가장 좁은가" in x],
            },
        }
        assert missing_first.returncode == 0, result
        assert "요청한 root 1 개" in missing_first.stdout and "관측 0" not in missing_first.stdout, result
        assert any(x.rstrip().endswith("예") for x in result["missing_first_then_good"]["verdict"]), result
        assert missing_last.returncode != 0 and "미완" in missing_last.stdout, result
        assert duplicate_label.returncode == 0 and "요청한 root 1 개" in duplicate_label.stdout, result
        return result


def blank_provenance(target, verify, _prov, _sign, _full_matrix_rows):
    with tempfile.TemporaryDirectory(prefix="r9-blank-prov-") as td:
        out = Path(td) / "out"; old = Path(td) / "old"; out.mkdir(); old.mkdir()
        rows = _full_matrix_rows("r9-blank")
        for row in rows:
            row["ref_inputs_sha"] = ""
            row["consumed_inputs"] = ""
            row["ref_consumed_inputs"] = ""
        art = out / "matrix_100.csv"
        verify.atomic_write_csv(art, rows, list(rows[0]))
        _sign(art, "r9-blank", "100", full=True)
        unit = _prov().read_unit(art)
        checked = run_cli(target, "check_u14.py", "--new", out, "--schema-only")

        # The promotion path is weaker still: internally inconsistent but non-empty
        # provenance is excluded from the old/new comparison, so it receives rc 0.
        bogus = _full_matrix_rows("r9-bogus")
        for row in bogus:
            row["ref_inputs_sha"] = "f" * 64
            row["consumed_inputs"] = "{}"
            row["ref_consumed_inputs"] = "{}"
        bogus_art = out / "matrix_200.csv"
        verify.atomic_write_csv(bogus_art, bogus, list(bogus[0]))
        _sign(bogus_art, "r9-bogus", "200", full=True)
        baseline = [dict(row) for row in bogus]
        for row in baseline:
            row.pop("ref_inputs_sha"); row.pop("consumed_inputs"); row.pop("ref_consumed_inputs")
        old_art = old / "matrix_200.csv"
        verify.atomic_write_csv(old_art, baseline, list(baseline[0]))
        _sign(old_art, "r9-bogus", "200", full=True)
        old_only = old / "matrix_100.csv"
        old_only_rows = [{k: v for k, v in row.items()
                          if k not in ("ref_inputs_sha", "consumed_inputs", "ref_consumed_inputs")}
                         for row in _full_matrix_rows("r9-old-only")]
        verify.atomic_write_csv(old_only, old_only_rows, list(old_only_rows[0]))
        _sign(old_only, "r9-old-only", "100", full=True)
        # Keep this comparison focused on the bogus unit.
        (out / "matrix_100.csv").unlink(); (out / "matrix_100.csv.meta.json").unlink()
        promoted = run_cli(target, "check_u14.py", "--new", out, "--old", old)
        result = {
            "case": "provenance_headers_without_values",
            "read_unit": [unit[0], unit[1]],
            "checker_rc": checked.returncode,
            "checker_stdout": checked.stdout,
            "all_provenance_cells_blank": all(
                not row[k] for row in rows for k in ("ref_inputs_sha", "consumed_inputs", "ref_consumed_inputs")
            ),
            "bogus_promotion": {
                "rc": promoted.returncode,
                "stdout": promoted.stdout,
                "ref_inputs_sha": bogus[0]["ref_inputs_sha"],
                "consumed_inputs": bogus[0]["consumed_inputs"],
                "new_artifacts": sorted(p.name for p in out.glob("*.csv")),
                "old_artifacts": sorted(p.name for p in old.glob("*.csv")),
            },
        }
        assert unit[0] is True, result
        assert checked.returncode == 0 and "전부 갖췄다" in checked.stdout, result
        assert promoted.returncode == 0 and "전부 같다" in promoted.stdout, result
        return result


def _run_shape(ns, monkeypatch, matrix: Path, out: Path):
    old_argv = sys.argv
    buf = io.StringIO()
    try:
        monkeypatch.setattr(sys, "argv", ["ne_shape.py", "--out-dir", str(matrix), "--write", str(out)])
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            rc = ns.main()
    finally:
        sys.argv = old_argv
    art = out / "ne_shape_GITT_Li.csv"
    meta = json.loads(art.with_name(art.name + ".meta.json").read_text(encoding="utf-8")) if art.is_file() else None
    return rc, buf.getvalue(), art, meta


def shape_missing_halfcell(target, _shape_harness, _pair):
    import pytest
    with tempfile.TemporaryDirectory(prefix="r9-shape-roster-") as td:
        base = Path(td); matrix = base / "matrix"; out = base / "shape"; matrix.mkdir()
        mp = pytest.MonkeyPatch()
        try:
            offsets = {"pristine": 0.0, "100": 0.01, "200": 0.10}
            ns = _shape_harness(mp, base, offsets)

            class P:
                def __init__(self, state): self.state = state
                def is_file(self): return self.state != "200"

            mp.setattr(ns.D, "half_cell_path", lambda root, src, state: P(state))
            _pair(matrix, "100")
            rc, text, art, meta = _run_shape(ns, mp, matrix, out)
            rows = list(csv.DictReader(art.open(encoding="utf-8")))
            result = {
                "case": "missing_expected_halfcell_removed_before_requested_roster",
                "rc": rc,
                "stdout": text,
                "rows": rows,
                "pairing": meta.get("pairing"),
                "declared_states": list(offsets),
            }
            assert rc == 0, result
            assert [r["state"] for r in rows] == ["100"], result
            assert meta["pairing"] == {"requested": ["100"], "paired": ["100"], "missing": [],
                                        "note": meta["pairing"]["note"]}, result
            assert not any(line.strip().startswith("200 ") for line in text.splitlines()), result
            assert "부분" not in text, result
            return result
        finally:
            mp.undo()


def shape_partial_overwrites_complete(target, _prov, _shape_harness, _pair):
    import pytest
    with tempfile.TemporaryDirectory(prefix="r9-shape-overwrite-") as td:
        base = Path(td); matrix = base / "matrix"; out = base / "shape"; matrix.mkdir()
        mp = pytest.MonkeyPatch()
        try:
            ns = _shape_harness(mp, base, {"pristine": 0.0, "100": 0.01, "200": 0.10})
            _pair(matrix, "100"); _pair(matrix, "200")
            rc1, text1, art, meta1 = _run_shape(ns, mp, matrix, out)
            bytes1 = art.read_bytes()
            assert rc1 == 0 and meta1["pairing"]["missing"] == []

            (matrix / "matrix_200.csv").unlink()
            (matrix / "matrix_200.csv.meta.json").unlink()
            rc2, text2, art, meta2 = _run_shape(ns, mp, matrix, out)
            bytes2 = art.read_bytes()
            unit2 = _prov().read_unit(art)
            result = {
                "case": "partial_run_replaces_prior_complete_canonical_unit",
                "complete_rc": rc1,
                "complete_pairing": meta1["pairing"],
                "partial_rc": rc2,
                "partial_pairing": meta2["pairing"],
                "prior_complete_bytes_replaced": bytes1 != bytes2,
                "partial_unit_verifies": [unit2[0], unit2[1]],
                "partial_stdout_tail": text2[-1000:],
            }
            assert rc2 == 3 and meta2["pairing"]["missing"] == ["200"], result
            assert bytes1 != bytes2 and unit2[0] is True, result
            return result
        finally:
            mp.undo()


def replay_vacuity(target):
    p = subprocess.run(
        [sys.executable, str(target / "reviews" / "r7_repros" / "replay_codex_r7.py"),
         "--target", str(target), "--probes", "DOES_NOT_EXIST"],
        cwd=target, capture_output=True, text=True, timeout=180,
    )
    body = json.loads(p.stdout)
    result = {
        "case": "closure_replay_accepts_empty_unknown_selection",
        "rc": p.returncode,
        "requested": "DOES_NOT_EXIST",
        "reported_probes": body.get("probes"),
    }
    assert p.returncode == 0 and body.get("probes") == {}, result
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=Path, required=True)
    ap.add_argument("--case", choices=("all", "roots", "provenance", "shape-roster", "shape-overwrite", "replay-vacuity"), default="all")
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    target, verify, _prov, _deg, _sign, _full_matrix_rows, _shape_harness, _pair = boot(args.target)
    head = subprocess.check_output(["git", "-c", "safe.directory=" + str(target.parent), "-C", str(target.parent),
                                    "rev-parse", "HEAD"], text=True).strip()
    assert head == REV, (head, REV)
    records = {}
    if args.case in ("all", "roots"):
        records["roots"] = root_alias(target, verify, _deg, _sign)
    if args.case in ("all", "provenance"):
        records["provenance"] = blank_provenance(target, verify, _prov, _sign, _full_matrix_rows)
    if args.case in ("all", "shape-roster"):
        records["shape_roster"] = shape_missing_halfcell(target, _shape_harness, _pair)
    if args.case in ("all", "shape-overwrite"):
        records["shape_overwrite"] = shape_partial_overwrites_complete(target, _prov, _shape_harness, _pair)
    if args.case in ("all", "replay-vacuity"):
        records["replay_vacuity"] = replay_vacuity(target)
    rendered = json.dumps(records, ensure_ascii=False, indent=2)
    print(rendered)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print("R9_ROOT_REPROS_PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
